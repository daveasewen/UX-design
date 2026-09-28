# #305 lane L - build a path list; every path checked changed-or-untracked first (C1's #304 finding).
import subprocess, sys, os
out = sys.argv[1]; extra = sys.argv[2:]
fixed = """knowledge/_rulings.json knowledge/_state.json knowledge/_gauge_tokens.py knowledge/_capture_gate.py knowledge/_checkin.py
knowledge/_seam.py knowledge/_RUNBOOK-context-gauge.md knowledge/_RUNBOOK-capture-ritual.md
_CHAIN.md dashboard/index.html knowledge/_memento-index.json knowledge/_node_titles.json notes/_RULINGS.html
reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html knowledge/_graph-mention-map.json tokens/_blast-radius.json _GRAPH-REPORT.md
notes/_KG-EXPLORER.html knowledge/_graph-mark-observations.jsonl
notes/_subreports/2026-09-28-305-L-window-and-summary.md notes/_lanes/305/W/SUMMARY-BULLETS.md
notes/_lanes/305/W/_gitcommit-W5b.log notes/_lanes/305/W/_gitcommit-W5b.term notes/_lanes/305/W/_4c-hygiene.log
notes/_lanes/305/W/_ci-gates-W5b.log notes/_lanes/305/W/_ci-runs-eb2630bb.txt notes/_lanes/305/W/_push-W5b-plain.log
notes/_lanes/305/W/step6-parse-5b.txt""".split()
lane = sorted(os.path.join(dp, f) for dp, dn, fn in os.walk('notes/_lanes/305/L') for f in fn if '/backup' not in dp and '__pycache__' not in dp)
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
