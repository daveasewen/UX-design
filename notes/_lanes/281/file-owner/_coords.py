#!/usr/bin/env python3
"""#281 lane FO — what moved between two builds of the explorer, node for node.

Answers the gate's question in the brief: "Coordinate sets byte-identical if no node is added or
removed; if the layout moves, say why." Compares the two embedded graphs — the id set, the edge
multiset and all fourteen baked coordinate keys — and reports the movement per family per key.

  python3 notes/_lanes/281/file-owner/_coords.py <before.html> <after.html> <out.json>
"""
import json, os, sys, collections

KEYS = ['x', 'y', 'x3', 'y3', 'z3', 'y2', 'xf', 'yf', 'zf', 'xo', 'yo', 'xs', 'ys', 'zs']


def kg(p):
    s = open(p, encoding='utf-8').read()
    tag = '<script id="kg" type="application/json">'
    i = s.index(tag) + len(tag)
    return json.loads(s[i:s.index('</script>', i)])


A, B = kg(sys.argv[1]), kg(sys.argv[2])
na = {n['id']: n for n in A['nodes']}
nb = {n['id']: n for n in B['nodes']}
ekey = lambda e: (e['s'], e['t'], e['type'], e.get('fam'))
out = {
    'before': {'version': A.get('version'), 'nodes': len(A['nodes']), 'edges': len(A['edges'])},
    'after': {'version': B.get('version'), 'nodes': len(B['nodes']), 'edges': len(B['edges'])},
    'nodeIdsIdentical': set(na) == set(nb),
    'nodesAdded': sorted(set(nb) - set(na)), 'nodesRemoved': sorted(set(na) - set(nb)),
    'edgeMultisetIdentical': collections.Counter(map(ekey, A['edges'])) == collections.Counter(map(ekey, B['edges'])),
    'famChanged': [{'id': i, 'from': na[i].get('fam'), 'to': nb[i].get('fam')}
                   for i in sorted(na) if i in nb and na[i].get('fam') != nb[i].get('fam')],
}
moved = collections.Counter()
for i in set(na) & set(nb):
    fam = na[i].get('fam') or 'base'
    for k in KEYS:
        if na[i].get(k) != nb[i].get(k): moved[(fam, k)] += 1
fams = sorted({f for f, _ in moved} | {(n.get('fam') or 'base') for n in A['nodes']})
out['movedByFamilyKey'] = {f: {k: moved[(f, k)] for k in KEYS if moved[(f, k)]} for f in fams}
out['movedByFamilyKey'] = {f: v for f, v in out['movedByFamilyKey'].items() if v}
out['unmovedFamilies'] = [f for f in fams if f not in out['movedByFamilyKey']]
json.dump(out, open(sys.argv[3], 'w'), indent=1)
print(f"v{out['before']['version']} → v{out['after']['version']} · ids identical {out['nodeIdsIdentical']}"
      f" · edge multiset identical {out['edgeMultisetIdentical']} · fam changed {len(out['famChanged'])}")
for f, v in out['movedByFamilyKey'].items(): print(f"  moved {f:15} {v}")
print('  UNMOVED (every coordinate byte-identical):', out['unmovedFamilies'])
