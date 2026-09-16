#!/usr/bin/env python3
"""Lane LY re-implementation of the page's own draw predicate, EX2 §3 method, in Python over the
embedded KG JSON. Chips at PAGE DEFAULTS. Reports the drawn node set, the drawn edge set, the
counts, and every drawn node's x,y (the FORCE coordinates, which #280 must not have touched)."""
import json, sys, re

FAMILY = {}
for fam, ts in [
    ('structure', 'containedBy hasPart composedOf family groupsWith partial reuses delegatesTo'),
    ('usage', 'usedInContext commonPattern'), ('render', 'renderedBy'),
    ('rules', 'governedBy mustNotNeighbour consumes triggeredBy drivesConsumer'),
    ('governance', 'governs evidencedBy ruledIn mentions supersedes supersedesClause retires narrows '
                   'refines corrects enacts extends bounds confirms overrides'),
    ('guidelines', 'appliesTo under enClause boundBy checkedBy verifiedBy'),
    ('guidelinerules', 'definedIn cites enforcedBy flaggedBy'),
    ('uxprinciples', 'tensionWith hasParty touches resolvedBy challengedBy explainedBy'),
    ('assets', 'inGroup activeVariantOf usesIcon usesLogo defaultFor ruledBy')]:
    for t in ts.split(): FAMILY[t] = fam

TYPES = ['component', 'snippet', 'pattern', 'context', 'ruling']
TYPES2 = ['session', 'artefact', 'evidence', 'sc', 'guideline', 'principle', 'policy', 'standard',
          'axe', 'rule', 'ux', 'polarity', 'icon', 'iconGroup', 'logo']
DEFAULT_FAM = {'structure': 1, 'usage': 1, 'render': 1, 'rules': 1, 'governance': 0, 'guidelines': 0,
               'guidelinerules': 0, 'uxprinciples': 0, 'assets': 0, 'designrulings': 1}


def load(p):
    s = open(p).read()
    k = '<script id="kg" type="application/json">'
    i = s.index(k) + len(k); j = s.index('</script>', i)
    return json.loads(s[i:j].replace('<\\/script', '</script'))


def report(path, famOn, typeOn=None):
    kg = load(path)
    N = kg['nodes']; E = kg['edges']
    byId = {n['id']: n for n in N}
    typeOn = typeOn or {t: 1 for t in TYPES + TYPES2}
    alive = lambda o: o.get('born') is None or (o['born'] <= len(kg['snaps']) - 1 and (o.get('died') is None))
    LIVE = [n for n in N if not n.get('dead') and n.get('died') is None]
    LIVEE = [e for e in E if not e.get('dead') and e.get('died') is None]
    famOK = lambda o: (not o.get('fam')) or famOn[o['fam']]
    NODEON = lambda n: typeOn.get(n['type'],0) and famOK(n)
    DR = lambda e: e['type'] == 'governedBy' or e['type'] == 'ruledBy' or (
        e['type'] == 'governs' and re.match(r'^(component|snippet):', e.get('t') or ''))
    EON = lambda e: famOn.get(FAMILY.get(e['type']),0) and (not DR(e) or famOn['designrulings'])
    DRON = lambda e: (not e.get('t')) or (not DR(e)) or famOn['designrulings']
    SHOWN = [n for n in LIVE if famOK(n)]
    SHOWNE = [e for e in LIVEE if famOK(e) and DRON(e) and
              ((not e.get('t')) or (famOK(byId[e['s']]) and famOK(byId[e['t']])))]
    etypes = [t for t in FAMILY if famOn.get(FAMILY.get(t),0) and (famOn['designrulings'] or t not in ('governedBy', 'ruledBy'))]
    nulls = sum(1 for e in LIVEE if not e.get('t') and famOK(e))
    drawnN = {n['id'] for n in LIVE if NODEON(n)}
    drawnE = set()
    for e in E:
        if not e.get('t') or not alive(e): continue
        s, t = byId[e['s']], byId[e['t']]
        if NODEON(s) and NODEON(t) and EON(e): drawnE.add((e['s'], e['t'], e['type']))
    drgov = sum(1 for e in LIVEE if e.get('t') and DR(e) and famOn.get(FAMILY.get(e['type']),0) and famOK(e)
                and famOK(byId[e['s']]) and famOK(byId[e['t']]))
    pos = {i: (byId[i]['x'], byId[i]['y']) for i in drawnN}
    pos3 = {i: (byId[i].get('x3'), byId[i].get('y3'), byId[i].get('z3'), byId[i].get('deg')) for i in drawnN}
    return dict(nodes=len(SHOWN), relations=len(SHOWNE), etypes=len(etypes), nulls=nulls,
                drawnN=drawnN, drawnE=drawnE, drgov=drgov, pos=pos, pos3=pos3,
                comp=sum(1 for n in SHOWN if n['type'] == 'component'))


if __name__ == '__main__':
    old, new = sys.argv[1], sys.argv[2]
    chips = sys.argv[3] if len(sys.argv) > 3 else ''
    famOn = dict(DEFAULT_FAM)
    for c in [c for c in chips.split(',') if c]: famOn[c] = 1
    a = report(old, famOn); b = report(new, famOn)
    print(f"chips on beyond defaults: {chips or '(none — page defaults)'}")
    for k in ('nodes', 'relations', 'etypes', 'nulls', 'comp', 'drgov'):
        print(f"  {k:10} {a[k]:>8} {b[k]:>8}  {'SAME' if a[k]==b[k] else 'DIFF'}")
    print(f"  drawn nodes  {len(a['drawnN'])} {len(b['drawnN'])}  {'SAME SET' if a['drawnN']==b['drawnN'] else 'DIFF SET'}")
    print(f"  drawn edges  {len(a['drawnE'])} {len(b['drawnE'])}  {'SAME SET' if a['drawnE']==b['drawnE'] else 'DIFF SET'}")
    same = [i for i in a['drawnN'] & b['drawnN']]
    bad = [i for i in same if a['pos'][i] != b['pos'][i]]
    bad3 = [i for i in same if a['pos3'][i] != b['pos3'][i]]
    print(f"  x,y of every drawn node: {len(same)} compared, {len(bad)} moved  {'SAME' if not bad else bad[:5]}")
    print(f"  x3,y3,z3,deg of every drawn node: {len(bad3)} moved  {'SAME' if not bad3 else bad3[:5]}")
