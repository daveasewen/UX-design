#!/usr/bin/env python3
"""Snapshot the component KG at every day it changed — the scrub line's data.

  python3 knowledge/_kg_history.py            # → knowledge/_kg_history.json (incremental: only new days)
  python3 knowledge/_kg_history.py --rebuild  # from scratch

One snapshot per calendar day (the day's LAST commit touching knowledge/components or
knowledge/_rulings.json), extracted with `git archive` into a scratch dir and parsed by
_build_kg_explorer.extract() — same reader as the live page, so the history is the same graph
seen earlier, not a different reading of it. Read-only against the repo. Born #266.
"""
import json, os, subprocess, sys, tempfile, tarfile, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'knowledge'); OUT = os.path.join(K, '_kg_history.json')
sys.path.insert(0, K)
import _build_kg_explorer as B

def days():
    log = subprocess.run(['git', 'log', '--format=%ad %H', '--date=short', '--', 'knowledge/components', 'knowledge/_rulings.json'],
                         cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
    seen = {}
    for l in log:
        if not l.strip(): continue
        d, h = l.split()
        seen.setdefault(d, h)  # log is newest-first: first hit per day = last commit of that day
    return sorted(seen.items())

def snapshot(commit):
    with tempfile.TemporaryDirectory(dir='/dev/shm' if os.path.isdir('/dev/shm') else None) as tmp:
        tar = subprocess.run(['git', 'archive', commit, 'knowledge/components'], cwd=ROOT, capture_output=True).stdout
        if not tar: return None
        tarfile.open(fileobj=io.BytesIO(tar)).extractall(tmp)
        r = subprocess.run(['git', 'archive', commit, 'knowledge/_rulings.json'], cwd=ROOT, capture_output=True).stdout
        if r: tarfile.open(fileobj=io.BytesIO(r)).extractall(tmp)
        nodes, edges = B.extract(os.path.join(tmp, 'knowledge'))
        return {'nodes': sorted(n['id'] for n in nodes), 'edges': sorted({f"{e['s']}|{e['t']}|{e['type']}" for e in edges if e['t']}),
                'unresolved': sum(1 for e in edges if not e['t'])}

def main():
    hist = {} if '--rebuild' in sys.argv else (json.load(open(OUT)) if os.path.exists(OUT) else {})
    for d, h in days():
        if d in hist and hist[d]['commit'] == h: continue
        s = snapshot(h)
        if s is None: continue
        hist[d] = {'commit': h[:7], **s}
        print(f"{d} {h[:7]} nodes {len(s['nodes'])} edges {len(s['edges'])}")
    json.dump(dict(sorted(hist.items())), open(OUT, 'w'), separators=(',', ':'))
    print(f"wrote {OUT} · {len(hist)} days · {os.path.getsize(OUT):,} B")

if __name__ == '__main__':
    main()
