#!/usr/bin/env python3
"""#305 H1 — call 38 kinds 1-5 and call 39's three status halves, each stamped through
`knowledge/_inscribe_ruling.py --set-status` (the sanctioned writer; one subprocess per ruling). Every new status keeps
the old one verbatim after ' · was: '. Lead words are from the store's own vocabulary (enacted / superseded / standing /
ruled). Kind 5 (no trace) is NOT stamped: see the H1 report.  python3 rulings_batch.py --dry-run | --write [--only K]"""
import json, subprocess, sys
WRITE = '--write' in sys.argv
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
R = {r['id']: r for r in json.load(open('knowledge/_rulings.json'))['rulings']}
U = {u['id']: u for u in json.load(open('notes/_lanes/304/R2/for_tuesday_uncertain.json'))['uncertain_rulings']}
K = {c['key']: c['ids'] for c in json.load(open('notes/_lanes/304/R6b/counts.json'))['stamps']['classes']}
assert [len(K[k]) for k in ('carried', 'overtaken', 'standing', 'part', 'untraced', 'intree')] == [6, 10, 14, 7, 8, 64]
D38 = "#305 `s305-D38` (Dave, sitting call 38, 14:29 BST, verbatim \"yes to all six\"; kinds by `notes/_lanes/304/R6b/counts.json`)"
D39 = "#305 `s305-D39` (Dave, sitting call 39, 14:29 BST, verbatim \"retire, park, yes\")"
rec = lambda i: U[i]['nearest_receipt']
was = lambda i: f" · was: {R[i]['status']}"
CARRIER = {'s130-D4': ('s149-D1 (mono, as amended)', '0c511016'), 's130-D5': ('s149-D1', '2bc83b44'),
           's135-D2': ('s135-D4 (the 82/82 KG verdicts)', 'b22e16b9'), 's151-D1': ('s158-D1..D4 / s160-D2', 'ee091eff'),
           's151-D2': ('s158 / s160-D2', 'ee091eff'), 's173-D1': ('s210-D1 (one Meter, completes s173-D1)', 'f75d8f55')}
PARK = {'s131-D2': 'P-305-3', 's136-D1': 'P-305-4', 's143-D1': 'P-305-5', 's172-D1': 'P-305-6', 's174-D1': 'P-305-7',
        's177-D1': 'P-305-8', 's273-D2': 'P-305-9'}
jobs = []   # (kind, id, status, sha)
for i in K['carried']:
    who, sha = CARRIER[i]
    jobs.append(('1', i, f"enacted — THROUGH A LATER RULING, not by a commit of its own: carried by {who}, commit {sha} "
                         f"({D38}, kind 1 'done, through a later ruling'). Run 2's receipt: {rec(i)}{was(i)}", sha))
for i in K['overtaken']:
    jobs.append(('2', i, f"superseded — OVERTAKEN OR LAPSED ({D38}, kind 2). What overtook it, as Run 2 recorded it: {rec(i)}{was(i)}", None))
for i in K['standing']:
    jobs.append(('3', i, f"standing — IN FORCE, NOTHING TO BUILD ({D38}, kind 3: a policy, posture, deferral, order of work, schedule or "
                         f"keep-as-is; no code was owed). Run 2's reading: {rec(i)}{was(i)}", None))
for i in K['part']:
    jobs.append(('4', i, f"ruled — PART-ENACTED, the open half PARKED with a tripwire as {PARK[i]} in `knowledge/_parked.json` "
                         f"({D38}, kind 4). The split, as Run 2 recorded it: {rec(i)}{was(i)}", None))
jobs.append(('39', 's135-D3', f"superseded — RETIRED as overtaken by the three-axis model `s136-D1` ({D39}: \"retire\"). The stamps page: "
             f"\"No mechanism was ever designed for it. The three-axis model you ruled the same day is the mechanism the record uses.\"{was('s135-D3')}", None))
jobs.append(('39', 's114-D2', f"ruled — PARKED WITH A TRIPWIRE as P-305-2 in `knowledge/_parked.json` ({D39}: \"park\"): the citation gate "
             f"reopens when the next gate is added. Not built, not retired{was('s114-D2')}", None))
jobs.append(('39', 's246-D3', f"ruled — PARKED WITH A TRIPWIRE as P-305-1 in `knowledge/_parked.json` ({D39}: \"park\"): the spans dial "
             f"reopens when bento edit mode is built. Not built, not retired{was('s246-D3')}", None))
log = []
for kind, i, status, sha in jobs:
    if ONLY and kind != ONLY: continue
    if R[i]['status'] == status: log.append((i, 'already')); continue
    cmd = ['python3', 'knowledge/_inscribe_ruling.py', '--set-status', i, status, '--write' if WRITE else '--dry-run']
    if sha: cmd += ['--evidence-sha', sha]
    p = subprocess.run(cmd, capture_output=True, text=True)
    log.append((i, p.returncode, (p.stdout + p.stderr).strip()[:160]))
    print(kind, i, p.returncode, (p.stdout + p.stderr).strip()[:140])
json.dump(log, open(f"notes/_lanes/305/H1/rulings_batch.{'write' if WRITE else 'dry'}{'.' + ONLY if ONLY else ''}.json", 'w'), indent=1, ensure_ascii=False)
print('rc!=0:', [x for x in log if x[1] not in (0, 'already')])
