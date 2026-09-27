#!/usr/bin/env python3
"""304-J step 3a: MECHANICAL node-title check (no Jev) over the explorer's own node set.
Class A opaque code · B path/URL · C bare machine slug · D readable. A and B say nothing about what the node IS;
C says a little to someone who knows the vocabulary; D is prose."""
import sys, os, json, re, random
from collections import Counter, defaultdict
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
K = os.path.join(REPO, 'knowledge'); sys.path.insert(0, K); sys.argv = ['x', '/dev/null']
import _build_kg_explorer as B
n, e = B.extract(); r = B.extract_extra(n, e)
N = {x['id']: x for x in n}; N.update({x['id']: x for x in r[0]})
CODE = re.compile(r'^(?:[a-z]{2,5}(?:-[a-z]{2,5})?-\d{2,4}[a-z]?|s\d{2,3}-D\d+|[A-Z]{1,4}-D?\d+(?:-[A-Za-z0-9]+)?|ADR-\d{4}.*|[a-z]{2}-\d{2}|\d+(?:\.\d+)+|ds-\d{3}|#?\d+)$')
def cls(label):
    L = (label or '').strip()
    # B = a bare path/URL and nothing else (a path followed by ' - prose' says what it is -> D)
    if ' ' not in L and re.match(r'^(https?://\S+|(?:knowledge|notes|showroom|tokens|\.github)/\S+|\S+\.(py|json|md|html|css|svg|js|jsonl|sh)(?::\d+)?)$', L): return 'B'
    if re.match(r'^[A-Z0-9]+(?:_[A-Z0-9]+)+$', L): return 'C'   # SHOUTY_SNAKE constant: a machine name
    if CODE.match(L): return 'A'
    if ' ' not in L and re.match(r'^[a-z0-9]+(?:[-_/][a-z0-9]+)*$', L): return 'C'
    return 'D'
rows = []
for nid, x in N.items():
    rows.append({'id': nid, 'type': x.get('type'), 'label': x.get('label') or '', 'class': cls(x.get('label'))})
by = defaultdict(Counter)
for r_ in rows: by[r_['type']][r_['class']] += 1
tot = Counter(r_['class'] for r_ in rows)
here = os.path.dirname(os.path.abspath(__file__))
json.dump({'total': len(rows), 'by_class': tot, 'by_type': {k: dict(v) for k, v in sorted(by.items())},
           'rows': sorted(rows, key=lambda z: (z['class'], z['type'], z['id']))}, open(os.path.join(here, 'node-titles-mechanical.json'), 'w'), indent=1, ensure_ascii=False)
print(len(rows), dict(tot))
for k, v in sorted(by.items(), key=lambda kv: -sum(kv[1].values())): print(' ', k, dict(v))
# stratified 20 for the Jev comparison: 5 per class, spread across types, seeded
rng = random.Random(3041); samp = []
for c in 'ABCD':
    pool = [z for z in rows if z['class'] == c]
    types = sorted({z['type'] for z in pool}); rng.shuffle(types)
    pick = []
    for t in types:
        if len(pick) == 5: break
        pick.append(rng.choice([z for z in pool if z['type'] == t]))
    while len(pick) < 5: pick.append(rng.choice(pool))
    samp += pick
json.dump(samp, open(os.path.join(here, 'node-titles-sample.json'), 'w'), indent=1, ensure_ascii=False)
for s in samp: print(s['class'], s['type'], '|', s['label'][:90])
