#!/usr/bin/env python3
"""#281 lane TV — THE CENSUS RE-RUN, set 08 (`obeys-ux`).

Lane OC's `notes/_lanes/280/orphan-census/_census.py` predicates, re-implemented against ONE page
so the same script reads the page before and after the rebuild. The chip vocabulary (`FAMILY`,
`famOn`) is PARSED out of `knowledge/_kg_explorer.template.html`, never retyped, and the page's two
sub-chip gates are modelled as the page has them: a `designrulings` citation answers to that chip,
a `held` line is drawn at no setting, and — new in 1.24 — a `cited` line answers to `uxcited`
INSTEAD of its storage family (the s281-D4 predicate). The `before` page has no `uxcited` key, so
the parser's own default dict is what decides whether that setting exists at all.

Set 08's own measure, lane OC's: `OBEYS_UX` is the DISTINCT set of `ux:` principles named by a
component meta's `edges.obeys`, and the set is dark while not one of those lines is drawn. Here it
is counted per setting: how many of those principles have ZERO drawn `obeys` line reaching them.

Nothing is written under knowledge/.

  python3 notes/_lanes/281/theory-view/_recensus.py <explorer.html> <out.json> [<template.html>]
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


def load_chips(tpl):
    t = open(tpl, encoding='utf-8').read()
    blk = re.sub(r'//.*', '', t.split('const FAMILY={')[1].split('};')[0])
    fam = dict(re.findall(r"(\w+):'(\w+)'", blk))
    dblk = t.split('const famOn={')[1].split('}')[0]
    return fam, {k: int(v) for k, v in re.findall(r'(\w+):(\d)', dblk)}


def census(path, tpl=TEMPLATE):
    KG = load_kg(path)
    FAMILY, DEFAULTS = load_chips(tpl)
    NODES = [n for n in KG['nodes'] if not n.get('dead') and n.get('died') is None]
    EDGES = [e for e in KG['edges'] if not e.get('dead') and e.get('died') is None]
    BY = {n['id']: n for n in NODES}
    ADD = ['guidelines', 'guidelinerules', 'uxprinciples', 'assets']
    SUB = ['uxcited'] if 'uxcited' in DEFAULTS else []      # absent on the 1.23 page, by design
    SETTINGS = [('defaults', dict(DEFAULTS)),
                ('all', {**DEFAULTS, **{f: 1 for f in ADD + SUB}}),
                ('allconst', {**DEFAULTS, **{f: 1 for f in ADD + SUB}, 'governance': 1})]
    EFAM = lambda e: e.get('fam') or FAMILY.get(e['type'])
    # lane OC's set 08: the DISTINCT ux: principles a component meta names through edges.obeys
    OBEYS_UX = sorted({e['t'] for e in EDGES
                       if e['type'] == 'obeys' and str(e.get('t') or '').startswith('ux:')})

    def DR(e):
        ty = e['type']
        return ty in ('governedBy', 'ruledBy') or (ty == 'governs' and bool(re.match(r'^(component|snippet):', e.get('t') or '')))

    def measure(famOn):
        ok = lambda o: (not o.get('fam')) or famOn.get(o['fam'], 0)
        def eon(e):
            if e.get('held'): return False
            base = famOn.get('uxcited', 0) if e.get('cited') else famOn.get(EFAM(e), 0)
            return bool(base) and ((not DR(e)) or famOn['designrulings'])
        deg = collections.Counter(); drawn = 0
        obeys_ux_deg = collections.Counter()
        for e in EDGES:
            if not e.get('t'): continue
            s, t = BY.get(e['s']), BY.get(e['t'])
            if s and t and ok(s) and ok(t) and eon(e):
                deg[e['s']] += 1; deg[e['t']] += 1; drawn += 1
                if e['type'] == 'obeys' and e['t'] in OBEYS_UX: obeys_ux_deg[e['t']] += 1
        vis = [n for n in NODES if ok(n)]
        zero = [n for n in vis if deg[n['id']] == 0]
        undrawn = [i for i in OBEYS_UX if obeys_ux_deg[i] == 0]
        return vis, zero, drawn, undrawn, sum(obeys_ux_deg.values())

    out = {'page': os.path.relpath(path, REPO), 'template': os.path.relpath(tpl, REPO),
           'version': KG.get('version'), 'nodes': len(KG['nodes']), 'edges': len(KG['edges']),
           'chipDefaults': DEFAULTS, 'obeysUxPrinciples': OBEYS_UX,
           'obeysUxLines': sum(1 for e in EDGES if e['type'] == 'obeys'
                               and str(e.get('t') or '').startswith('ux:')),
           'flags': {'held': sum(1 for e in EDGES if e.get('held')),
                     'cited': sum(1 for e in EDGES if e.get('cited')),
                     'why': sum(1 for e in EDGES if e.get('why'))},
           'settings': {}}
    for name, f in SETTINGS:
        vis, zero, drawn, undrawn, lines = measure(f)
        out['settings'][name] = {
            'shown': len(vis), 'drawn': drawn, 'dark': len(zero),
            'darkByType': dict(collections.Counter(n['type'] for n in zero)),
            'set08_obeys_ux': len(undrawn), 'set08_undrawn': undrawn,
            'set08_lines_drawn': lines}
    return out


if __name__ == '__main__':
    o = census(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 else TEMPLATE)
    json.dump(o, open(sys.argv[2], 'w'), indent=1)
    print(f"{o['page']} v{o['version']} · nodes {o['nodes']} · edges {o['edges']} · flags {o['flags']}")
    print(f"  obeys→ux: {o['obeysUxLines']} lines onto {len(o['obeysUxPrinciples'])} principles {o['obeysUxPrinciples']}")
    for k, v in o['settings'].items():
        print(f"  {k:9} shown {v['shown']:5} drawn {v['drawn']:5} dark {v['dark']:4} "
              f"· set08 obeys-ux {v['set08_obeys_ux']} undrawn, {v['set08_lines_drawn']} lines drawn "
              f"· {v['darkByType']}")
