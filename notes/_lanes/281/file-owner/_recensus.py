#!/usr/bin/env python3
"""#281 lane FO — THE CENSUS RE-RUN, set 06 (`rules-in-the-constitution`).

MEASURES only. Lane OC's `notes/_lanes/280/orphan-census/_census.py` predicates, re-implemented
against ONE page so the same script can read the page before and after the rebuild, and with
1.22's EON: an edge's family is its OWN `fam` first, the type map second, and a `held` line is
drawn by nothing. Reads the embedded `<script id="kg">` out of whichever explorer it is given and
the chip vocabulary (`FAMILY`, `famOn`) out of `knowledge/_kg_explorer.template.html` — parsed,
never retyped. Nothing is written under knowledge/.

  python3 notes/_lanes/281/file-owner/_recensus.py <explorer.html> <out.json>
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
TEMPLATE = os.path.join(REPO, 'knowledge', '_kg_explorer.template.html')


def load_kg(path):
    s = open(path, encoding='utf-8').read()
    tag = '<script id="kg" type="application/json">'
    i = s.index(tag) + len(tag)
    return json.loads(s[i:s.index('</script>', i)])


def load_chips():
    t = open(TEMPLATE, encoding='utf-8').read()
    blk = re.sub(r'//.*', '', t.split('const FAMILY={')[1].split('};')[0])
    fam = dict(re.findall(r"(\w+):'(\w+)'", blk))
    dblk = t.split('const famOn={')[1].split('}')[0]
    return fam, {k: int(v) for k, v in re.findall(r'(\w+):(\d)', dblk)}


def census(path):
    KG = load_kg(path)
    FAMILY, DEFAULTS = load_chips()
    NODES = [n for n in KG['nodes'] if not n.get('dead') and n.get('died') is None]
    EDGES = [e for e in KG['edges'] if not e.get('dead') and e.get('died') is None]
    BY = {n['id']: n for n in NODES}
    ADD = ['guidelines', 'guidelinerules', 'uxprinciples', 'assets']
    SETTINGS = [('defaults', dict(DEFAULTS)),
                ('all', {**DEFAULTS, **{f: 1 for f in ADD}}),
                ('allconst', {**DEFAULTS, **{f: 1 for f in ADD}, 'governance': 1})]
    EFAM = lambda e: e.get('fam') or FAMILY.get(e['type'])

    def DR(e):
        ty = e['type']
        return ty in ('governedBy', 'ruledBy') or (ty == 'governs' and bool(re.match(r'^(component|snippet):', e.get('t') or '')))

    def measure(famOn):
        ok = lambda o: (not o.get('fam')) or famOn.get(o['fam'], 0)
        eon = lambda e: famOn.get(EFAM(e), 0) and ((not DR(e)) or famOn['designrulings']) and not e.get('held')
        deg = collections.Counter(); drawn = 0
        for e in EDGES:
            if not e.get('t'): continue
            s, t = BY.get(e['s']), BY.get(e['t'])
            if s and t and ok(s) and ok(t) and eon(e):
                deg[e['s']] += 1; deg[e['t']] += 1; drawn += 1
        vis = [n for n in NODES if ok(n)]
        zero = [n for n in vis if deg[n['id']] == 0]
        return vis, zero, drawn

    out = {'page': os.path.relpath(path, REPO), 'version': KG.get('version'),
           'nodes': len(KG['nodes']), 'edges': len(KG['edges']), 'settings': {}}
    for name, f in SETTINGS:
        vis, zero, drawn = measure(f)
        d = {'shown': len(vis), 'drawn': drawn, 'dark': len(zero),
             'darkByType': dict(collections.Counter(n['type'] for n in zero)),
             'darkIds': sorted(n['id'] for n in zero)}
        if name == 'all':
            dr = {n['id'] for n in zero if n['type'] == 'rule'}
            byfile = collections.Counter(e['t'] for e in EDGES if e['type'] == 'definedIn' and e['s'] in dr)
            d['set06_rules_in_the_constitution'] = len(dr)
            d['set06_by_file'] = dict(byfile)
        out['settings'][name] = d
    # the tie itself, read off the page
    out['tied'] = {n['id']: {'fam': n.get('fam'), 'claimedBy': n.get('claimedBy'),
                             'fileKind': n.get('fileKind'), 'tie': n.get('tie')}
                   for n in NODES if n.get('claimedBy')}
    out['guideline_artefact_fams'] = dict(collections.Counter(
        n.get('fam') for n in NODES if n['id'].startswith('artefact:knowledge/guidelines/')))
    return out


if __name__ == '__main__':
    o = census(sys.argv[1])
    json.dump(o, open(sys.argv[2], 'w'), indent=1)
    print(f"{o['page']} v{o['version']} · nodes {o['nodes']} · edges {o['edges']}")
    for k, v in o['settings'].items():
        print(f"  {k:9} shown {v['shown']:5} drawn {v['drawn']:5} dark {v['dark']:4} {v['darkByType']}"
              + (f" · set06 {v['set06_rules_in_the_constitution']} {v['set06_by_file']}" if 'set06_by_file' in v else ''))
    print(f"  tied nodes on the page: {len(o['tied'])} · artefact:knowledge/guidelines/* by family {o['guideline_artefact_fams']}")
