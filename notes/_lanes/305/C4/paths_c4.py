# #305 C4 - build the day-two path list from A2's, B6's, B5's and D1's reports plus the brief; every path checked changed-or-untracked first.
import subprocess, sys
def g(*a):
    return subprocess.run(['git','--no-optional-locks',*a],capture_output=True,text=True)
T = set(l for l in g('diff','--name-only','HEAD').stdout.split('\n') if l)
U = set(l for l in g('ls-files','--others','--exclude-standard').stdout.split('\n') if l)
want_tracked = """knowledge/_rulings.json knowledge/_state.json
notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md notes/_lanes/305/A/CALL-MAP.json
knowledge/components/button.meta.json knowledge/components/filter-toolbar-bar.meta.json knowledge/components/footer.meta.json
knowledge/components/template-dashboard-bento.meta.json knowledge/when-fields.json
notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html
notes/_subreports/2026-09-27-305-D1-ci-release-divergence.md
_CHAIN.md reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html notes/_RULINGS.html tokens/_blast-radius.json tokens/_GRAPH-REPORT.md
knowledge/_memento-index.json knowledge/_graph-mention-map.json notes/_KG-EXPLORER.html dashboard/index.html knowledge/_node_titles.json
knowledge/_graph-mark-observations.jsonl""".split()
paths, clean = [], []
for p in want_tracked:
    (paths if p in T else clean).append(p)
UEXACT = {'notes/_subreports/2026-09-28-305-A2-loose-ends.md','notes/_subreports/2026-09-28-305-B6-names-and-rules.md',
          'notes/_subreports/2026-09-27-305-B5-loose-ends.md','notes/_subreports/2026-09-28-305-C4-commit.md',
          'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html','notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md',
          'notes/_lanes/305/D1/_ci-gates-D1c.log','notes/_lanes/305/D1/_ci-runs-01fb005a.txt','notes/_lanes/305/D1/_gitcommit-D1c.log',
          'notes/_lanes/305/D1/_gitcommit-D1c.term','notes/_lanes/305/D1/_msg-D1c.txt.t3-rendered','notes/_lanes/305/D1/_push-D1c.log',
          'notes/_lanes/305/D1/step6-parse-c.txt'}
UPRE = ('notes/_lanes/305/A2/','notes/_lanes/305/B6/','notes/_lanes/305/B5/','notes/_lanes/305/C4/')
EXCL = ('notes/_lanes/305/A2/backup/','notes/_lanes/305/B5/shots/')
held = []
for p in sorted(U):
    if p in UEXACT or p.startswith(UPRE):
        if p.startswith(EXCL) or '/__pycache__/' in p:
            held.append(p)
        else:
            paths.append(p)
missing = [p for p in UEXACT if p not in U and p not in T]
for p in paths:
    assert p in T or p in U, p
open(sys.argv[1] if sys.argv[1:] else 'notes/_lanes/305/C4/paths-c4.txt','w').write('\n'.join(paths)+'\n')
print('paths', len(paths), '| tracked-wanted-but-clean', clean, '| exact-missing', missing)
print('held inside the fence', len(held), sorted(set(p.rsplit('/',1)[0] for p in held)))
print('tracked dirty not taken:', sorted(t for t in T if t not in paths))
