# #305 C3 - build the wave-three path list from F1's, W2's and P1's reports; every path checked changed-or-untracked first.
import subprocess, sys
def g(*a):
    return subprocess.run(['git','--no-optional-locks',*a],capture_output=True,text=True)
T = set(l for l in g('diff','--name-only','HEAD').stdout.split('\n') if l)
U = set(l for l in g('ls-files','--others','--exclude-standard').stdout.split('\n') if l)
want_tracked = """knowledge/_release/_gen_pack_manifest.py knowledge/_validate_package_delta.py
knowledge/guidelines/web-foundations.md knowledge/guidelines/_rules-index.json knowledge/_validate_own_size.py
knowledge/_instrument-fit.json knowledge/_INSTRUMENT-FIT.md knowledge/_rule_nodes.json knowledge/_node_titles.json
notes/_KG-EXPLORER.html knowledge/_validate_a11y.py knowledge/_jev-receipts.jsonl
knowledge/_state.json _CHAIN.md reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html dashboard/index.html
notes/_RULINGS.html tokens/_blast-radius.json tokens/_GRAPH-REPORT.md knowledge/_memento-index.json
knowledge/_graph-mention-map.json knowledge/_graph-mark-observations.jsonl""".split()
paths, clean = [], []
for p in want_tracked:
    (paths if p in T else clean).append(p)
UEXACT = {'notes/_subreports/2026-09-27-305-F1-ci-reds.md','notes/_subreports/2026-09-27-305-W2-remaining.md',
          'notes/_subreports/2026-09-27-305-P1-push-ci.md','notes/_subreports/2026-09-27-305-C3-commit.md',
          'notes/_lanes/305/W2/OWNS.txt','notes/_lanes/305/W2/work/rails.fresh.json','notes/_lanes/305/W2/work/ifit-pre.diff'}
UPRE = ('notes/_lanes/305/F1/','notes/_lanes/305/P1/','notes/_lanes/305/C3/','notes/_jev-link-check/',
        'notes/_lanes/305/W2/backup/','notes/_lanes/305/W2/motion/')
held = []
for p in sorted(U):
    if p in UEXACT or p.startswith(UPRE):
        (held if '/__pycache__/' in p else paths).append(p)
    elif p.startswith('notes/_lanes/305/W2/'):
        held.append(p)
for p in paths:
    assert p in T or p in U, p
open(sys.argv[1] if sys.argv[1:] else 'notes/_lanes/305/C3/paths-c3.txt','w').write('\n'.join(paths)+'\n')
print('paths', len(paths), '| tracked-wanted-but-clean', clean)
print('held W2 scratch', len(held), held[:6])
print('tracked dirty not taken:', sorted(t for t in T if t not in paths))
