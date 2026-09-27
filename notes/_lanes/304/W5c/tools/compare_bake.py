#!/usr/bin/env python3
"""304 W5c: compare two baked explorers' KG data — before (HEAD builder) vs after (v1.29).
Proves only `label` and `titleFrom` move, and counts bare-code titles with seat J's own classifier.
usage: compare_bake.py BEFORE.html AFTER.html"""
import json, re, sys
from collections import Counter
def kg(p):
    h = open(p, encoding='utf-8').read(); j = h.index('{"generated"')
    return json.JSONDecoder().raw_decode(h[j:])[0]
A, B = kg(sys.argv[1]), kg(sys.argv[2])
print('versions', A['version'], '->', B['version'])
na = {n['id']: n for n in A['nodes']}; nb = {n['id']: n for n in B['nodes']}
print('node ids identical:', set(na) == set(nb), len(na))
diffk = Counter()
for i, n in na.items():
    m = nb[i]
    for k in set(n) | set(m):
        if n.get(k) != m.get(k): diffk[k] += 1
print('node fields that differ (count of nodes):', dict(diffk))
print('edges identical:', A['edges'] == B['edges'], len(A['edges']))
print('other top-level keys that differ:', [k for k in A if k not in ('nodes', 'edges') and A[k] != B.get(k)])
# seat J's classifier, verbatim (notes/_lanes/304/J/node_titles.py)
CODE = re.compile(r'^(?:[a-z]{2,5}(?:-[a-z]{2,5})?-\d{2,4}[a-z]?|s\d{2,3}-D\d+|[A-Z]{1,4}-D?\d+(?:-[A-Za-z0-9]+)?|ADR-\d{4}.*|[a-z]{2}-\d{2}|\d+(?:\.\d+)+|ds-\d{3}|#?\d+)$')
def cls(label):
    L = (label or '').strip()
    if ' ' not in L and re.match(r'^(https?://\S+|(?:knowledge|notes|showroom|tokens|\.github)/\S+|\S+\.(py|json|md|html|css|svg|js|jsonl|sh)(?::\d+)?)$', L): return 'B'
    if re.match(r'^[A-Z0-9]+(?:_[A-Z0-9]+)+$', L): return 'C'
    if CODE.match(L): return 'A'
    if ' ' not in L and re.match(r'^[a-z0-9]+(?:[-_/][a-z0-9]+)*$', L): return 'C'
    return 'D'
def bare(n):
    code = n['id'].split(':', 1)[1]
    return n['label'].strip() == (('#' + code) if n['type'] == 'session' else code)
THREE = ('ruling', 'rule', 'session')
for name, D in (('BEFORE', A), ('AFTER', B)):
    live = [n for n in D['nodes'] if not n.get('dead')]
    byc = Counter(cls(n['label']) for n in live)
    a3 = Counter(n['type'] for n in live if n['type'] in THREE and cls(n['label']) == 'A')
    b3 = Counter(n['type'] for n in D['nodes'] if n['type'] in THREE and bare(n))
    print(f"{name}: live nodes {len(live)} · J classes {dict(sorted(byc.items()))}"
          f"\n   class A in the three kinds: {dict(a3)} = {sum(a3.values())}"
          f"\n   label == bare code, three kinds (live + dead): {dict(b3)} = {sum(b3.values())}")
dead = [(n['id'], n['label']) for n in B['nodes'] if n.get('dead') and n['type'] in THREE]
print('dead (history-only) nodes of the three kinds:', dead)
