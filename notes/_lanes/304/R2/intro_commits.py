#!/usr/bin/env python3
"""R2: for each UNCERTAIN ruling whose id is carried by a governed (non-record) file at HEAD, find the
commit that INTRODUCED the id into that file (git log -S, oldest). Read-only git. Resumable (cache)."""
import json, subprocess, sys, time, os
A = json.load(open(sys.argv[1])); cache_p = sys.argv[2]
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
t0 = time.time()
for o in A:
    if not o['tree_governs']: continue
    for f, ln, txt in o['tree_governs'][:2]:
        k = o['id'] + '|' + f
        if k in cache: continue
        if time.time() - t0 > 90: print('TIME; resume'); json.dump(cache, open(cache_p, 'w'), indent=0); sys.exit(0)
        out = subprocess.run(['git', '--no-optional-locks', 'log', '--reverse', '--date=short',
                              '--format=%H\x1f%ad\x1f%s', '-S', o['id'], '571d458c', '--', f],
                             capture_output=True, text=True).stdout.strip().split('\n')
        first = out[0].split('\x1f') if out and out[0] else None
        cache[k] = {'intro': first, 'n': len([x for x in out if x])}
        json.dump(cache, open(cache_p, 'w'), indent=0)
json.dump(cache, open(cache_p, 'w'), indent=0)
print('done', len(cache))
