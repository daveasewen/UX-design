#!/usr/bin/env python3
"""304-J: build the stratified edge sample from the KG explorer's OWN extract (canonical edge list).
Read-only over knowledge/. Writes candidates.json beside itself. Seeded; deterministic."""
import sys, os, json, random, re
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
K = os.path.join(REPO, 'knowledge'); sys.path.insert(0, K)
sys.argv = ['x', '/dev/null']
import _build_kg_explorer as B
n, e = B.extract(); r = B.extract_extra(n, e); xn, xe = r[0], r[1]
N = {x['id']: x for x in n}; N.update({x['id']: x for x in xn}); E = e + xe
rules = {x['id']: x for x in json.load(open(os.path.join(K, '_rule_nodes.json')))['nodes'] if x['id'].startswith('rule:')}
roles = json.load(open(os.path.join(K, 'roles.json')))['roles']
intents = json.load(open(os.path.join(K, 'chart-intents.json')))['chart-intent']
shapes = json.load(open(os.path.join(K, 'shapes.json')))['shapes']
import glob
UX = {x['id']: x for x in json.load(open(os.path.join(K, '_ux_principle_nodes.json')))['nodes']}
sc = {}
for f in glob.glob(os.path.join(K, 'compliance/rules/*.json')):
    d = json.load(open(f)); sc['sc:' + d['sc']] = d

def desc(nid):
    kind, key = nid.split(':', 1); x = N.get(nid, {})
    if kind == 'component':
        return {'kind': 'UI component', 'name': x.get('label'), 'purpose': x.get('purpose', '')}
    if kind == 'rule':
        return {'kind': 'design-system rule', 'id': key, 'text': (rules.get(nid, {}).get('text') or '')[:700]}
    if kind == 'ux':
        return {'kind': 'UX principle', 'name': key.replace('pr-', '').replace('-', ' '), 'statement': UX.get(nid, {}).get('statement', '')}
    if kind == 'role':
        ro = roles.get(key, {}); return {'kind': 'layout role (a job a slot asks a component to do)', 'name': key, 'definition': ro.get('definition', '')}
    if kind == 'intent':
        it = intents.get(key, {}); return {'kind': 'chart intent (the question a chart answers)', 'name': key, 'definition': it.get('definition', ''), 'not_for': it.get('notFor', '')}
    if kind == 'shape':
        s = shapes.get(key, {}); return {'kind': 'data shape (what data a component takes)', 'name': key, 'definition': s.get('definition', '')}
    if kind == 'token':
        return {'kind': 'design-token group', 'name': key, 'tier': x.get('tier'), 'source': x.get('source'),
                'example_members': [b['token'] for b in (x.get('blastTop') or [])][:6]}
    if kind == 'sc':
        d = sc.get(nid, {}); return {'kind': 'WCAG success criterion', 'id': key, 'title': d.get('title'), 'check': (d.get('check') or {}).get('description', '')[:500]}
    return {'kind': kind, 'name': key}

PLAN = {'obeys': 8, 'providesRole': 6, 'answersIntent': 5, 'hasDataShape': 4, 'yieldsTo': 4,
        'bindsToken': 5, 'appliesTo': 4, 'tensionWith': 4}
NEG = {'obeys': 2, 'providesRole': 2, 'answersIntent': 1, 'hasDataShape': 1, 'yieldsTo': 1,
       'bindsToken': 1, 'appliesTo': 1, 'tensionWith': 1}
HAND = {'obeys': [('component:links', 'rule:ctkb-003'), ('component:eyebrow', 'ux:pr-fitts')],
        'providesRole': [('component:amount-display', 'role:headline-metric'), ('component:table', 'role:chart-panel')],
        'answersIntent': [('component:Chart-histogram', 'intent:comparison')],
        'hasDataShape': [('component:Chart-histogram', 'shape:categories × series')],
        'yieldsTo': [('component:eyebrow', 'component:badge')],
        'bindsToken': [('component:footer', 'token:data')],
        'appliesTo': [('sc:2.5.8', 'component:eyebrow')],
        'tensionWith': [('ux:pr-hick', 'ux:pr-choice-overload')]}
rng = random.Random(304)
out = []
for t, k in PLAN.items():
    pool = sorted([x for x in E if x['type'] == t and x.get('t')], key=lambda x: (x['s'], x['t']))
    if t == 'obeys':   # stratify within obeys: half rule targets, half ux targets
        a = [x for x in pool if x['t'].startswith('rule:')]; b = [x for x in pool if x['t'].startswith('ux:')]
        pick = rng.sample(a, k // 2) + rng.sample(b, k - k // 2)
    else:
        pick = rng.sample(pool, k)
    for x in pick:
        out.append({'edge_type': t, 'origin': 'real', 's': x['s'], 't': x['t'], 'source': desc(x['s']), 'target': desc(x['t']),
                    'authored_why': x.get('why') or x.get('note') or ''})
    # negatives: same source kind, a same-kind target the source does NOT link to under this type
    linked = {(x['s'], x['t']) for x in pool}
    tgts = sorted({x['t'] for x in pool if not (t == 'obeys' and x['t'].startswith('rule:') and not rules.get(x['t']))})
    srcs = sorted({x['s'] for x in pool})
    for i in range(NEG[t]):
        for _ in range(500):
            s = rng.choice(srcs); tt = rng.choice(tgts)
            if (s, tt) not in linked and s != tt: break
        # the seeded draw above is KEPT (so the real sample stays byte-stable) but DISCARDED:
        # random unlinked pairs were mostly trivially false (Pie chart -> a notification rule).
        # The negatives are hand-constructed to be PLAUSIBLE-but-false; each checked absent from E.
        s, tt = HAND[t][i]; assert not [x for x in E if {x['s'], x['t']} == {s, tt}], (s, tt)
        out.append({'edge_type': t, 'origin': 'constructed-negative', 's': s, 't': tt, 'source': desc(s), 'target': desc(tt), 'authored_why': ''})
for i, o in enumerate(out): o['eid'] = 'E%02d' % (i + 1)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'candidates.json'), 'w'), indent=1, ensure_ascii=False)
print(len(out), 'edges;', sum(o['origin'] == 'real' for o in out), 'real')
