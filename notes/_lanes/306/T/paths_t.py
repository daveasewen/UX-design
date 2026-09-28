# #306 lane T - build a path list; every path checked changed-or-untracked first (the committer strands the lock on an unchanged path).
import subprocess, sys, os
out = sys.argv[1]; extra = sys.argv[2:]
fixed = """knowledge/_state.json knowledge/_rulings.json _CARRIES.md _CHAIN.md dashboard/index.html knowledge/_memento-index.json
notes/_RULINGS.html reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html knowledge/_graph-mention-map.json tokens/_blast-radius.json
_GRAPH-REPORT.md knowledge/_graph-mark-observations.jsonl knowledge/_node_titles.json
notes/_subreports/2026-09-28-306-S-parked-check.md notes/_subreports/2026-09-28-306-T-parked-enact.md
notes/_CHECK-306-parked-superseded-2026-09-28-v1.html notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md
notes/_lanes/306/S/parked-102-check.json notes/_lanes/306/S/parked-102-pack.json""".split()
lane = sorted(os.path.join(dp, f) for dp, dn, fn in os.walk('notes/_lanes/306/T') for f in fn if '/backup' not in dp and '__pycache__' not in dp)
keep, skip = [], []
for p in fixed + lane + extra:
    if not os.path.exists(p):
        skip.append((p, 'absent')); continue
    tracked = subprocess.run(['git', '--no-optional-locks', 'ls-files', '--error-unmatch', p], capture_output=True).returncode == 0
    if tracked:
        same = subprocess.run(['git', '--no-optional-locks', 'diff', '--quiet', 'HEAD', '--', p]).returncode == 0
        (skip if same else keep).append((p, 'unchanged') if same else p)
    else:
        ign = subprocess.run(['git', '--no-optional-locks', 'check-ignore', '-q', p]).returncode == 0
        (skip if ign else keep).append((p, 'ignored') if ign else p)
keep = list(dict.fromkeys(keep))
open(out, 'w').write('\n'.join(keep) + '\n')
print(len(keep), 'named'); [print('  skip', s) for s in skip]
