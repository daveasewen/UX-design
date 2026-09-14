#!/usr/bin/env python3
"""#271 harvest — recount every number a RECEIPT.md claims, straight from the lane JSONs.

Usage:  python3 notes/_lanes/271/harvest/_recount.py A|B|C
Read-only. Touches nothing under knowledge/.

Unanimity uses THE REVIEW PAGE'S TEST: a proposal is unanimous when its
`disagreements` field opens with the word "none". Silence is recorded, never
counted as agreement, so "expected silence" is reported as its own number.
"""
import json, os, sys, collections

SYSTEMS = ['GOV.UK', 'USWDS', 'Material', 'Carbon', 'Polaris', 'Spectrum',
           'Atlassian', 'Ant', 'Fluent', 'Apple', 'NN/g', 'Datawrapper', 'FT ']
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))


def flat(v):
    return ' | '.join(map(str, v)) if isinstance(v, list) else str(v)


def comps_of(row):
    """A row's component field may name one stem, a comma list, or an 'a / b' pair."""
    c = row.get('components', row.get('component'))
    items = c if isinstance(c, list) else str(c).split(',')
    out = set()
    for it in items:
        it = it.strip()
        if not it:
            continue
        parts = [p.strip() for p in it.split(' / ') if p.strip()]
        out |= set(parts) if len(parts) > 1 else {it}
    return out


def main(slice_):
    d = os.path.join(HERE, slice_)
    src = json.load(open(os.path.join(d, 'SOURCES.json')))
    prop = json.load(open(os.path.join(d, 'PROPOSED-WHEN.json')))['proposals']
    rows = json.load(open(os.path.join(d, 'DECISION-TABLE.json')))['rows']

    stems = {os.path.basename(p)[:-len('.meta.json')]
             for p in os.listdir(os.path.join(ROOT, 'knowledge', 'components'))
             if p.endswith('.meta.json')}

    quotes = [e['quote'] for e in src['external']]
    lens = [len(q.split()) for q in quotes]
    over = [q for q, n in zip(quotes, lens) if n >= 15]

    names = [p['component'] for p in prop]
    unanimous = [p['component'] for p in prop
                 if flat(p['disagreements']).strip().lower().startswith('none')]
    silence = [p['component'] for p in prop
               if 'silence' in flat(p['disagreements']).lower()]
    conf = collections.Counter(p['confidence'] for p in prop)
    no_ext = [p['component'] for p in prop
              if not any(k in flat(p['sources']) for k in SYSTEMS)]
    rowcomps = set().union(*[comps_of(r) for r in rows]) if rows else set()
    touched = [n for n in names if n in rowcomps]
    internal = [r['id'] for r in rows if str(r.get('kind', '')).startswith('internal')]

    bad_comp = sorted({c for e in src['external'] if e.get('component')
                       for c in [e['component']] if c.split(' / ')[0] not in stems}
                      | {p['component'] for p in prop
                         if p['component'].split(' / ')[0] not in stems}
                      | {c for r in rows for c in comps_of(r) if c not in stems})

    print('SLICE %s' % slice_)
    print('  SOURCES     ours %d · external %d · refused %d'
          % (len(src['ours']), len(src['external']), len(src['refused'])))
    print('  quotes      longest %d words · at-or-over the <15 cap: %d' % (max(lens), len(over)))
    print('  proposals   %d' % len(prop))
    print('  confidence  ' + ' · '.join('%s %d' % (k, conf[k]) for k in
          ('canon', 'consensus-external', 'single-external', 'none') if k in conf))
    print('  unanimous   %d  (page test: `disagreements` opens with "none") -> %s'
          % (len(unanimous), ', '.join(unanimous)))
    print('  expected silence recorded in `disagreements`: %d -> %s'
          % (len(silence), ', '.join(silence)))
    print('  decision rows %d · distinct components named by a row %d · proposals a row touches %d'
          % (len(rows), len(rowcomps), len(touched)))
    print('  rows flagged kind=internal: %d -> %s' % (len(internal), ', '.join(internal)))
    print('  system-disagreement rows: %d' % (len(rows) - len(internal)))
    print('  proposals citing NO external system in `sources`: %d' % len(no_ext))
    print('  component values that are not an existing meta stem: %d%s'
          % (len(bad_comp), (' -> ' + ', '.join(bad_comp)) if bad_comp else ''))
    print('  external findings with component: null: %d'
          % sum(1 for e in src['external'] if e.get('component') is None))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'A')
