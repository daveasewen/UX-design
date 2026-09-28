# #306 lane U - build a path list; every path checked changed-or-untracked first (T's paths_t.py, U's set).
import subprocess, sys, os
out = sys.argv[1]; extra = sys.argv[2:]
fixed = """knowledge/_state.json knowledge/_rulings.json _CHAIN.md dashboard/index.html knowledge/_memento-index.json
notes/_RULINGS.html reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html knowledge/_graph-mention-map.json tokens/_blast-radius.json
_GRAPH-REPORT.md knowledge/_graph-mark-observations.jsonl knowledge/_node_titles.json
notes/_subreports/2026-09-28-306-R-wrap-redesign.md notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md
notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html notes/_lanes/306/DAVE-RULINGS-2026-09-28-wrap-redesign.md""".split()
lane = sorted(os.path.join(dp, f) for d in ('notes/_lanes/306/R', 'notes/_lanes/306/U')
              for dp, dn, fn in os.walk(d) for f in fn if '/backup' not in dp and '__pycache__' not in dp)
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
