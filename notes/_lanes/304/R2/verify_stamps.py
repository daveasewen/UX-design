#!/usr/bin/env python3
"""#304 Run 2a — SECOND PASS over the stamps (independent of stamp.py): re-reads the store and proves
(1) count unchanged; (2) every non-stamped ruling is dict-identical to the pre-stamp snapshot; (3) every stamped
ruling differs ONLY in status/evidence, leads with the #304 mark, carries its sha in evidence, and the sha
resolves to a commit dated on/after the ruling; (4) the lead-word census before → after. Args: pre-stamp copy."""
import json, re, subprocess, sys, collections
pre = {r['id']: r for r in json.load(open(sys.argv[1]))['rulings']}
post_l = json.load(open('knowledge/_rulings.json'))['rulings']; post = {r['id']: r for r in post_l}
D = {d['id']: d for d in json.load(open('notes/_lanes/304/R2/decisions.json'))}
MARK = 'ENACTED (back-stamped #304 2026-09-26, Run 2 audit)'
lead = lambda s: (re.match(r'[A-Za-z][A-Za-z-]*', s.strip()) or [''])[0].lower()
errs = []
if len(pre) != len(post): errs.append(f'count {len(pre)} -> {len(post)}')
stamped = [i for i, d in D.items() if d['verdict'] == 'ENACTED']
for i, r in post.items():
    if i in stamped: continue
    if r != pre[i]: errs.append(f'{i}: changed but not stamped')
for i in stamped:
    a, b = pre[i], post[i]
    if {k: v for k, v in a.items() if k not in ('status', 'evidence')} != {k: v for k, v in b.items() if k not in ('status', 'evidence')}:
        errs.append(f'{i}: a frozen field moved')
    sha = D[i]['sha']
    if not b['status'].startswith(MARK) or f'in commit {sha}' not in b['status']: errs.append(f'{i}: status not stamped as decided')
    if not any(sha in e for e in b['evidence']): errs.append(f'{i}: sha {sha} not in evidence')
    if b['evidence'][:len(a['evidence'])] != a['evidence']: errs.append(f'{i}: prior evidence not preserved as a prefix')
    cd = subprocess.run(['git', '--no-optional-locks', 'show', '-s', '--format=%ad', '--date=short', sha + '^{commit}'], capture_output=True, text=True).stdout.strip()
    if not cd or cd < b['date']: errs.append(f'{i}: sha {sha} date {cd!r} vs ruling {b["date"]}')
cb = collections.Counter(lead(r['status']) for r in pre.values()); ca = collections.Counter(lead(r['status']) for r in post.values())
bare_b = sum(1 for r in pre.values() if r['status'].strip().lower() == 'ruled'); bare_a = sum(1 for r in post.values() if r['status'].strip().lower() == 'ruled')
print('rulings', len(pre), '->', len(post), '| stamped', len(stamped))
print('lead words before', dict(cb)); print('lead words after ', dict(ca))
print('bare ruled', bare_b, '->', bare_a)
print('ERRORS', len(errs)); [print('  ', e) for e in errs[:20]]
sys.exit(1 if errs else 0)
