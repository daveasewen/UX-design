#!/usr/bin/env python3
"""#281 lane PH — THE CENSUS RE-RUN, against the rebuilt page (principles get a home).

This is lane OC's `notes/_lanes/280/orphan-census/_census.py` measure() and nothing else: the same
two readers (the embedded `<script id="kg">` out of notes/_KG-EXPLORER.html, the FAMILY map and the
famOn defaults out of knowledge/_kg_explorer.template.html, parsed, never retyped), the same three
chip settings, the same three predicates. It is a SEPARATE FILE for the same reason lane CM's copy was: a lane may not write inside another
lane's folder, and running _census.py itself would rewrite lane OC's dated page and facts.json — a
lane's filed evidence is dated history.

ONE thing is tightened on top of lane CM's copy. v1.22's EON reads an edge's OWN `fam` when it
carries one and falls back to the type map only when it does not (`e.fam || FAMILY[e.type]`) — which
is what recount()/famOK has always done for the counts, and what INSPECT's edge door has done since
v1.21. It matters here because `evidencedBy` is one storage type with two families: 1,254 governance
edges (a ruling and its evidence) and, from #281, 134 uxprinciples edges (a principle and the source
it was graded on). A type-keyed predicate would draw the second lot only under the Constitution chip
while the header counted them under the Explanation chip.

TWO things are tightened. (1) v1.21's EON also refuses a HELD edge, so an edge marked `held` is drawn
at no setting, and the predicate says so. (2) lane OC's measure() took "every type chip is on in all
three settings" as given; it was true of every type OC's ten sets named and false of three it did
not — `shape`, `intent` and `role` had no type chip in the template at all, so the page's NODEON was
`undefined` for them whatever the family chips said. A drawn line now needs BOTH ends' type chips as
well, which is what the page has always done. `visible` keeps OC's own family-only meaning so the
before/after rows compare like with like; `no-chip` is the new column that names the second gate.

MEASURES only. Writes facts-after.json beside this file and prints the table.

  python3 notes/_lanes/281/principles-home/_recensus.py [<explorer.html>] [<out.json>] [<template.html>]

The THIRD argument is what makes the before/after table honest: the chip vocabulary must be read
from the template that SHIPPED with the page being measured, never from the live one. The "before"
row is taken with HEAD's page AND HEAD's template.
"""
import json, os, re, sys, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
K = os.path.join(REPO, 'knowledge')
EXPLORER = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'notes', '_KG-EXPLORER.html')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'facts-after.json')
TEMPLATE = sys.argv[3] if len(sys.argv) > 3 else os.path.join(K, '_kg_explorer.template.html')


def load_kg(p):
    src = open(p, encoding='utf-8').read()
    tag = '<script id="kg" type="application/json">'
    i = src.index(tag) + len(tag)
    j = src.index('</script>', i)
    kg = json.loads(src[i:j])
    ver = re.search(r'v(\d+\.\d+)\s*·', src)
    kg['_version'] = ver.group(1) if ver else kg.get('version', '?')
    return kg


def load_chips():
    t = open(TEMPLATE, encoding='utf-8').read()
    blk = re.sub(r'//.*', '', t.split('const FAMILY={')[1].split('};')[0])
    fam = dict(re.findall(r"(\w+):'(\w+)'", blk))
    dblk = t.split('const famOn={')[1].split('}')[0]
    defaults = {k: int(v) for k, v in re.findall(r'(\w+):(\d)', dblk)}
    lblk = re.sub(r'//.*', '', t.split('const FAMLABEL={')[1].split('};')[0])
    labels = dict(re.findall(r"(\w+):'([^']+)'", lblk))
    # #281 lane CM: lane OC's measure() assumed "every type chip is on in all three settings", which
    # was true of every type it looked at and false of three it did not — shape/intent/role had no
    # chip at all, so typeOn[t] was undefined and NODEON was false whatever the families said. The
    # type row is therefore parsed too, and a node with no chip can hold no drawn line.
    types = []
    for name in ('TYPES', 'TYPES2'):
        blk = re.sub(r'//.*', '', t.split('const %s=[' % name)[1].split('];')[0])
        types += re.findall(r"'([^']+)'", blk)
    return fam, defaults, labels, types


KG = load_kg(EXPLORER)
FAMILY, DEFAULTS, FAMLABEL, TYPECHIPS = load_chips()
TYPEON = set(TYPECHIPS)
NODES = [n for n in KG['nodes'] if not n.get('dead') and n.get('died') is None]
EDGES = [e for e in KG['edges'] if not e.get('dead') and e.get('died') is None]
BY = {n['id']: n for n in NODES}
FAMOF = lambda n: n.get('fam') or 'base'

ADDITIVE = ['guidelines', 'guidelinerules', 'uxprinciples', 'assets']
SETTINGS = [
    ('defaults', 'Page defaults', dict(DEFAULTS)),
    ('all', 'Every chip on', {**DEFAULTS, **{f: 1 for f in ADDITIVE}}),
    ('allconst', 'Every chip on + Constitution', {**DEFAULTS, **{f: 1 for f in ADDITIVE}, 'governance': 1}),
]


def DR(e):
    t = e['type']
    return t in ('governedBy', 'ruledBy') or (t == 'governs' and bool(re.match(r'^(component|snippet):', e.get('t') or '')))


def measure(famOn):
    # `ok` is lane OC's own visibility predicate — the FAMILY chips only — kept exactly as it was so
    # the before/after table compares like with like. `nodeon` is the page's NODEON: a node is drawn
    # only if its TYPE chip exists and is on as well, which is the second gate #281 had to open.
    ok = lambda o: (not o.get('fam')) or famOn.get(o['fam'], 0)
    nodeon = lambda o: ok(o) and o['type'] in TYPEON
    efam = lambda e: e.get('fam') or FAMILY.get(e['type'])
    eon = lambda e: famOn.get(efam(e), 0) and ((not DR(e)) or famOn['designrulings']) and not e.get('held')
    deg, nul, drawn = collections.Counter(), collections.Counter(), 0
    for e in EDGES:
        if not e.get('t'):
            if ok(e):
                nul[e['s']] += 1
            continue
        s, t = BY.get(e['s']), BY.get(e['t'])
        if s and t and nodeon(s) and nodeon(t) and eon(e):
            deg[e['s']] += 1
            deg[e['t']] += 1
            drawn += 1
    vis = [n for n in NODES if ok(n)]
    zero = [n for n in vis if deg[n['id']] == 0]
    return dict(vis=vis, zero=zero, deg=deg, nul=nul, drawn=drawn,
                nochip=[n for n in vis if n['type'] not in TYPEON],
                nullonly=[n for n in zero if nul[n['id']] > 0])


M = {k: measure(f) for k, _, f in SETTINGS}
HOMELESS = sorted({e['type'] for e in EDGES} - set(FAMILY))
HELD = [e for e in EDGES if e.get('held')]
ETC = collections.Counter(e['type'] for e in EDGES)

WATCH = ['ux', 'family', 'evidence', 'polarity', 'shape', 'intent', 'role', 'rule', 'logo', 'component', 'snippet']
facts = {
    'generated': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'explorer': KG['_version'], 'kg_generated': KG.get('generated'), 'commit': KG.get('commit'),
    'page': os.path.relpath(EXPLORER, REPO), 'template': TEMPLATE,
    'settings': [{'key': k, 'name': n, 'visible': len(M[k]['vis']), 'zero': len(M[k]['zero']),
                  'nullonly': len(M[k]['nullonly']), 'nochip': len(M[k]['nochip']),
                  'drawn': M[k]['drawn']} for k, n, _ in SETTINGS],
    'type_chips': sorted(TYPEON),
    'types_with_no_chip': sorted({n['type'] for n in NODES} - TYPEON),
    'homeless_edge_types': HOMELESS,
    'held': {'n': len(HELD), 'types': dict(collections.Counter(e['type'] for e in HELD)),
             'targets': sorted({e['t'] for e in HELD})},
    'edge_type_counts': {t: ETC[t] for t in sorted(ETC)},
    'watch': {},
    'dark_everywhere_by_type': dict(collections.Counter(
        n['type'] for n in M['allconst']['zero'])),
}
for t in WATCH:
    facts['watch'][t] = {k: {'visible': sum(1 for n in M[k]['vis'] if n['type'] == t),
                            'dark': sum(1 for n in M[k]['zero'] if n['type'] == t),
                            'lit': sum(1 for n in M[k]['vis'] if n['type'] == t and M[k]['deg'][n['id']] > 0)}
                        for k, _, _ in SETTINGS}
json.dump(facts, open(OUT, 'w'), indent=1)

print(f"explorer v{facts['explorer']} · {facts['page']} · commit {facts['commit']}")
print(f"{'setting':<12}{'visible':>9}{'dark':>7}{'null-only':>11}{'no-chip':>9}{'drawn':>8}")
for s in facts['settings']:
    print(f"{s['key']:<12}{s['visible']:>9}{s['zero']:>7}{s['nullonly']:>11}{s['nochip']:>9}{s['drawn']:>8}")
print('node types with no chip at all: ' + (', '.join(facts['types_with_no_chip']) or 'NONE'))
print('homeless edge types (no family anywhere): ' + (', '.join(HOMELESS) or 'NONE'))
print('held (drawn at no setting): %d · %s → %s' % (
    facts['held']['n'], facts['held']['types'], ', '.join(facts['held']['targets'])))
print("the dot sets this lane owns (degree > 0 at 'every chip on'):")
for t in ('ux', 'family', 'evidence'):
    c = facts['watch'][t]['all']
    print(f"  {t:<8} visible {c['visible']:>4} · lit {c['lit']:>4} · dark {c['dark']:>4}")
print(f"wrote {OUT}")
