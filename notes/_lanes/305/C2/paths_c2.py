# #305 C2 - build the wave-two path list; every path checked changed-or-untracked first.
import subprocess, os, sys
def g(*a):
    return subprocess.run(['git','--no-optional-locks',*a],capture_output=True,text=True)
tracked = [l for l in g('diff','--name-only','HEAD').stdout.split('\n') if l]
untracked = [l for l in g('ls-files','--others','--exclude-standard').stdout.split('\n') if l]
T = set(tracked); U = set(untracked)
want_tracked = """_CARRIES.md _CHAIN.md dashboard/index.html
knowledge/_RUNBOOK-context-gauge.md knowledge/_TOKEN-FORK-LEDGER.json knowledge/_capture_gate.py knowledge/_checkin.py
knowledge/_gauge_tokens.py knowledge/_git_commit.sh knowledge/_graph-mention-map.json knowledge/_memento-index.json
knowledge/_parked.json knowledge/_rulings.json knowledge/_seam.py knowledge/_state.json knowledge/_state.py
memento-package/claude-plugin/memento/machinery/_MACHINERY-MANIFEST.md memento-package/claude-plugin/memento/machinery/_gen_chain.py
memento-package/machinery/_MACHINERY-MANIFEST.md memento-package/machinery/_gen_chain.py
notes/_RULINGS.html notes/_subreports/2026-09-27-305-K-cut.md reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html
tokens/_blast-radius.json tokens/_GRAPH-REPORT.md knowledge/_graph-mark-observations.jsonl""".split()
for v in ['','_v3','_v5','_v6','_v7','_v74_gearbox','_v75_gearbox']:
    want_tracked.append(f'knowledge/_render/verify_demo_slides_268{v}.py')
paths, skipped = [], []
for p in want_tracked:
    (paths if p in T else skipped).append(p)
HOLD_PREFIX = ('notes/_lanes/305/H2/_stray/','notes/_lanes/305/H2/backup/','notes/_lanes/305/V2/cold/','notes/_lanes/305/V2/cold13/')
HOLD_EXACT = {'notes/_lanes/305/H1/backup/_state.json.pre-H1','notes/_lanes/305/H1/backup/_rulings.json.pre-H1','notes/_lanes/305/H1/backup/_parked.json.pre-H1'}
UPRE = ('_retired/deck-v7-slide-checkers-268/','notes/_lanes/305/H1/','notes/_lanes/305/H2/','notes/_lanes/305/V2/','notes/_lanes/305/C2/')
UEXACT = {'notes/_subreports/2026-09-27-305-H1-records.md','notes/_subreports/2026-09-27-305-H2-code.md',
          'notes/_subreports/2026-09-27-305-V2-verifier-cut.md','notes/_subreports/2026-09-27-305-C2-commit.md',
          'notes/_lanes/305/K/real-frozen-post-Y2.txt','notes/_lanes/305/K/real-frozen-post-Y2-commit-arm.txt'}
held = []
for p in sorted(U):
    if p in UEXACT or p.startswith(UPRE):
        if p in HOLD_EXACT or p.startswith(HOLD_PREFIX) or '/__pycache__/' in p:
            held.append(p)
        else:
            paths.append(p)
for p in paths:
    assert p in T or p in U, p
open('notes/_lanes/305/C2/paths-c2.txt','w').write('\n'.join(paths)+'\n')
print('paths', len(paths), '| tracked-wanted-but-clean', skipped, '| held-in-scope', len(held))
for h in held[:12]: print('  held', h)
print('tracked dirty not taken:', [t for t in tracked if t not in paths])
