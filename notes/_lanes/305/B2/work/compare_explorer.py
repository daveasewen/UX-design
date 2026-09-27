#!/usr/bin/env python3
"""305 B2 — compare two baked explorers (v1.29 builder vs v1.30 builder, SAME tree): what moved, by field."""
import json, os, sys, collections, kgdata
A, B = kgdata.load(sys.argv[1]), kgdata.load(sys.argv[2])
na = {n['id']: n for n in A['nodes']}; nb = {n['id']: n for n in B['nodes']}
added = sorted(set(nb) - set(na)); removed = sorted(set(na) - set(nb))
COORD = {'x', 'y', 'x3', 'y3', 'z3', 'y2', 'xf', 'yf', 'zf', 'xo', 'yo', 'xs', 'ys', 'zs'}
diffk = collections.Counter(); moved_types = collections.Counter(); lab = []
for i in set(na) & set(nb):
    a, b = na[i], nb[i]
    for k in set(a) | set(b):
        if a.get(k) != b.get(k):
            diffk[k] += 1
            if k in COORD: moved_types[(k, a['type'], a.get('fam'))] += 1
    if a.get('label') != b.get('label'): lab.append((i, a.get('label'), b.get('label')))
ek = lambda e: (e['s'], e.get('t'), e['type'])
ea = collections.Counter(ek(e) for e in A['edges']); eb = collections.Counter(ek(e) for e in B['edges'])
out = {"version": [A.get('version'), B.get('version')], "nodes": [len(na), len(nb)], "edges": [len(A['edges']), len(B['edges'])],
       "added_nodes_by_type": dict(collections.Counter(nb[i]['type'] for i in added)), "removed_nodes": removed,
       "edges_added_by_type": dict(collections.Counter(k[2] for k in (eb - ea).elements())),
       "edges_removed_by_type": dict(collections.Counter(k[2] for k in (ea - eb).elements())),
       "node_fields_changed": dict(diffk), "coords_moved_by": {"%s|%s|%s" % k: v for k, v in sorted(moved_types.items())[:40]},
       "labels_changed": len(lab), "labels_changed_by_type": dict(collections.Counter(i.split(':')[0] for i, _, _ in lab)),
       "label_samples": lab[:8],
       "top_level_keys_changed": [k for k in A if k not in ('nodes', 'edges') and A[k] != B.get(k)]}
print(json.dumps(out, indent=1, ensure_ascii=False))
