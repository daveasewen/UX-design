# #306 lane V - build a path list; every path checked changed-or-untracked first (U's paths_u.py, V's set).
import subprocess, sys, os
out = sys.argv[1]
fixed = """knowledge/_state.json knowledge/_rulings.json _CHAIN.md dashboard/index.html knowledge/_memento-index.json
notes/_RULINGS.html reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html knowledge/_graph-mention-map.json tokens/_blast-radius.json
_GRAPH-REPORT.md knowledge/_graph-mark-observations.jsonl knowledge/_node_titles.json
knowledge/_ci_readback.py knowledge/_build_all.py knowledge/_capture_gate.py
knowledge/_RUNBOOK-capture-ritual.md knowledge/_RUNBOOK-git-commit.md
notes/_subreports/2026-09-28-306-V-limits-and-phase2.md""".split()
lane = sorted(os.path.join(dp, f) for dp, dn, fn in os.walk('notes/_lanes/306/V') for f in fn
              if '/backup' not in dp and '__pycache__' not in dp)
keep, skip = [], []
for p in fixed + lane:
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
