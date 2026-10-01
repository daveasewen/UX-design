#!/usr/bin/env python3
"""#313 lane DV — the node and edge counts of the knowledge graph at each step of the edge-register work.

Extracts the graph (the explorer's own extract() + extract_extra(), as _validate_edges.py does) from the `knowledge/`
tree at six commits — before D1, after D1, D2, D3, D4, and HEAD — and prints the delta between each step by edge type
and by node kind. Read-only: every tree is a `git archive` into a scratch directory, deleted after.

Usage: python3 notes/_lanes/313/DV/dv_counts.py [--json OUT]   (run from the repo root; needs the commits in history)
       python3 notes/_lanes/313/DV/dv_counts.py --per-commit   every commit from before D1 to HEAD that moves a count, by type
"""
import json, os, shutil, subprocess, sys, tempfile
from collections import Counter

STEPS = [('before D1', '3756e3ec'), ('D1 why+maker', 'ccc094fe'), ('D2 outside+fold', 'e7e2f863'),
         ('D3 five edges+theme', 'a7fdf39d'), ('D4 consumers read register', 'be42df55'), ('HEAD', 'HEAD')]

PROBE = r'''
import contextlib, io, json, sys, types
from collections import Counter
K = sys.argv[1]; sys.path.insert(0, K)
try:
    import numpy
except ImportError:
    sys.modules['numpy'] = types.ModuleType('numpy')
with contextlib.redirect_stdout(io.StringIO()):
    import _build_kg_explorer as B
    n, e = B.extract(K=K)
    xn, xe, _ = B.extract_extra(n, e, K=K)
nodes = {x['id']: x for x in n + xn}
E = e + xe
print(json.dumps({'nodes': len(nodes), 'edges': len(E),
                  'byType': Counter(x['type'] for x in E),
                  'byKind': Counter(str(i).split(':', 1)[0] for i in nodes),
                  'nulls': sum(1 for x in E if x.get('t') is None)}))
'''


def measure(rev, scratch):
    d = os.path.join(scratch, rev.replace('/', '_'))
    os.makedirs(d)
    a = subprocess.run(['git', 'archive', rev, 'knowledge', ':(exclude)knowledge/assets'], capture_output=True, check=True)
    subprocess.run(['tar', '-x', '-C', d], input=a.stdout, check=True)
    p = subprocess.run([sys.executable, '-c', PROBE, os.path.join(d, 'knowledge')], capture_output=True, text=True)
    shutil.rmtree(d, ignore_errors=True)
    if p.returncode:
        return {'error': p.stderr.strip()[-300:]}
    return json.loads(p.stdout.strip().splitlines()[-1])


def per_commit():
    revs = subprocess.run(['git', 'rev-list', '--reverse', STEPS[0][1] + '..HEAD'], capture_output=True, text=True).stdout.split()
    s = tempfile.mkdtemp(prefix='dv-counts-')
    try:
        prev = measure(STEPS[0][1], s)
        for r in revs:
            m = measure(r, s)
            if 'error' in m:
                print(r[:8], 'ERROR', m['error']); continue
            if (m['nodes'], m['edges'], m['nulls'], m['byType'], m['byKind']) != (prev['nodes'], prev['edges'], prev['nulls'], prev['byType'], prev['byKind']):
                subj = subprocess.run(['git', 'log', '-1', '--format=%s', r], capture_output=True, text=True).stdout.strip()[:90]
                print(f"{r[:8]} nodes {m['nodes'] - prev['nodes']:+d} edges {m['edges'] - prev['edges']:+d} nulls {m['nulls'] - prev['nulls']:+d} | {subj}")
                for key, lab in (('byType', 'edge'), ('byKind', 'node')):
                    for k in sorted(set(m[key]) | set(prev[key])):
                        a, b = prev[key].get(k, 0), m[key].get(k, 0)
                        if a != b: print(f"     {lab} {k}: {a} -> {b} ({b - a:+d})")
            prev = m
        print(f"({len(revs)} commits read; the ones not listed move no count)")
    finally:
        shutil.rmtree(s, ignore_errors=True)
    return 0


def main(argv):
    if '--per-commit' in argv:
        return per_commit()
    scratch = tempfile.mkdtemp(prefix='dv-counts-')
    out = []
    try:
        for name, rev in STEPS:
            m = measure(rev, scratch); m['step'] = name; m['rev'] = rev; out.append(m)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    for m in out:
        print(f"{m['step']:28} {m['rev']:9} " + (f"nodes {m['nodes']:6}  edges {m['edges']:6}  nulls {m['nulls']}" if 'error' not in m else 'ERROR ' + m['error']))
    for a, b in zip(out, out[1:]):
        if 'error' in a or 'error' in b: continue
        print(f"\n== {a['step']} → {b['step']}: nodes {b['nodes'] - a['nodes']:+d}, edges {b['edges'] - a['edges']:+d}")
        for lab, key in (('edge type', 'byType'), ('node kind', 'byKind')):
            A, B = Counter(a[key]), Counter(b[key])
            for k in sorted(set(A) | set(B)):
                if A[k] != B[k]:
                    print(f"   {lab:9} {k:22} {A[k]:6} → {B[k]:6}  ({B[k] - A[k]:+d})")
    if '--json' in argv:
        json.dump(out, open(argv[argv.index('--json') + 1], 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
