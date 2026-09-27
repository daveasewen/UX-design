#!/usr/bin/env python3
"""#305 H1 — call 38 kind 6: read each of the 64 at HEAD. For each ruling, locate the receipt line Run 2 named
(file + a quoted fragment), re-find it at HEAD by CONTENT (line numbers drift), print +-4 lines of context and the
commit that introduced that line (git blame --porcelain at HEAD). Read-only. Output: probe64.txt / probe64.json."""
import json, re, subprocess, os
U = {u['id']: u for u in json.load(open('notes/_lanes/304/R2/for_tuesday_uncertain.json'))['uncertain_rulings']}
K = {c['key']: c['ids'] for c in json.load(open('notes/_lanes/304/R6b/counts.json'))['stamps']['classes']}
R = {r['id']: r for r in json.load(open('knowledge/_rulings.json'))['rulings']}
out = []; txt = []
for i in K['intree']:
    rec = U[i]['nearest_receipt']
    m = re.match(r"([\w./-]+\.\w+):(\d+) '(.{0,60})", rec)
    row = {'id': i, 'receipt': rec, 'file': None}
    txt.append(f"\n=================== {i}\nSAYS: {R[i]['says'][:700]}\nR2: {rec[:300]}")
    if m:
        f, ln, frag = m.group(1), int(m.group(2)), m.group(3).split("'")[0][:50]
        row['file'] = f
        if os.path.exists(f):
            L = open(f, encoding='utf-8', errors='replace').read().split('\n')
            hits = [n for n, l in enumerate(L, 1) if frag[:40] in l]
            n = min(hits, key=lambda h: abs(h - ln)) if hits else None
            row['line_now'] = n
            if n:
                b = subprocess.run(['git', '--no-optional-locks', 'blame', '--porcelain', '-L', f'{n},{n}', 'HEAD', '--', f], capture_output=True, text=True).stdout
                sha = b.split()[0][:8] if b else None
                subj = subprocess.run(['git', '--no-optional-locks', 'log', '-1', '--format=%h %ad %s', '--date=short', sha], capture_output=True, text=True).stdout.strip() if sha else ''
                row['blame'] = sha; row['blame_subj'] = subj[:160]
                ctx = '\n'.join(f"   {k}: {L[k-1][:220]}" for k in range(max(1, n - 4), min(len(L), n + 4) + 1))
                txt.append(f"AT HEAD {f}:{n} (R2 said :{ln}) blame {sha} — {subj[:140]}\n{ctx}")
            else:
                txt.append(f"AT HEAD: fragment NOT FOUND in {f}")
        else:
            txt.append(f"AT HEAD: {f} MISSING")
    out.append(row)
open('notes/_lanes/305/H1/probe64.txt', 'w').write('\n'.join(txt)); json.dump(out, open('notes/_lanes/305/H1/probe64.json', 'w'), indent=1)
print(sum(1 for r in out if r.get('blame')), 'located of', len(out))
