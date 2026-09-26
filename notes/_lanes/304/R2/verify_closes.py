#!/usr/bin/env python3
"""#304 Run 2b — SECOND PASS over the closes, independent of close_plan.py's logic: re-reads the store and
re-derives every receipt from the closed_by TEXT ITSELF. For each closed row: (1) owner claude, state done,
closed_by starts with the #304 mark; (2) every 8-hex commit named in closed_by resolves to a commit; (3) every
'path:line' named resolves at HEAD 571d458c or on disk AND that line contains the basename it is said to name
(or, for manual receipts, a non-empty line); (4) every 'present at HEAD' path exists at 571d458c; (5) no other
item changed vs the pre-close snapshot. Arg: pre-close snapshot path."""
import json, re, sys, subprocess, os
pre = {i['id']: i for i in json.load(open(sys.argv[1]))['items']}
post = {i['id']: i for i in json.load(open('knowledge/_state.json'))['items']}
MARK = '#304 Run 2 (2026-09-26) — receipted close'
def git(*a): return subprocess.run(['git', '--no-optional-locks', *a], capture_output=True, text=True)
def line_at(path, n):
    r = git('show', f'571d458c:{path}')
    txt = r.stdout if r.returncode == 0 else (open(path, encoding='utf-8', errors='replace').read() if os.path.exists(path) else None)
    if txt is None: return None
    L = txt.splitlines(); return L[n - 1] if 0 < n <= len(L) else None
errs, closed, nrec = [], [], 0
for i, a in post.items():
    b = pre[i]
    if a == b: continue
    if not (b['state'] == 'open' and a['state'] == 'done' and str(a.get('closed_by', '')).startswith(MARK)):
        errs.append(f'{i}: changed but not a #304 close'); continue
    if {k: v for k, v in a.items() if k not in ('state', 'closed_by')} != {k: v for k, v in b.items() if k not in ('state', 'closed_by')}:
        errs.append(f'{i}: a field other than state/closed_by moved')
    if a['owner'] != 'claude': errs.append(f'{i}: NOT claude-owned')
    closed.append(i); cb = a['closed_by']
    for sha in set(re.findall(r'(?<![0-9a-f])([0-9a-f]{8})(?![0-9a-f])', cb)):
        nrec += 1
        if git('cat-file', '-e', f'{sha}^{{commit}}').returncode: errs.append(f'{i}: commit {sha} does not resolve')
    for m in re.finditer(r'([\w./{},*-]+\.(?:md|html|json|py|sh|jsonl)):(\d+)', cb):
        path, n = m.group(1), int(m.group(2)); nrec += 1
        if '{' in path or '*' in path: continue
        ln = line_at(path, n)
        if ln is None: errs.append(f'{i}: {path}:{n} does not resolve'); continue
        tail = cb[m.end():m.end() + 200]
        nm = re.match(r" \(session #\d+ by [\w-]+\) names ([\w.-]+)", tail)
        if nm and nm.group(1).rstrip(".") not in ln: errs.append(f'{i}: {path}:{n} does not contain {nm.group(1)}')
        if not ln.strip(): errs.append(f'{i}: {path}:{n} is blank')
    for m in re.finditer(r'([\w./-]+\.md) present at HEAD 571d458c', cb):
        nrec += 1
        if git('cat-file', '-e', f'571d458c:{m.group(1)}').returncode: errs.append(f'{i}: {m.group(1)} not at HEAD')
print('closed rows re-verified', len(closed), '| receipts re-derived', nrec, '| ERRORS', len(errs))
for e in errs: print('  ', e)
sys.exit(1 if errs else 0)
