# #305 C4 - stamp-commit path list: the stamp, the serial tail, the explorer, the report and the C4 lane tail; each checked changed-or-untracked.
import subprocess
def g(*a): return subprocess.run(['git','--no-optional-locks',*a],capture_output=True,text=True)
T = set(l for l in g('diff','--name-only','HEAD').stdout.split('\n') if l)
U = set(l for l in g('ls-files','--others','--exclude-standard').stdout.split('\n') if l)
want = """knowledge/_rulings.json notes/_RULINGS.html _CHAIN.md reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html notes/_KG-EXPLORER.html
tokens/_blast-radius.json tokens/_GRAPH-REPORT.md knowledge/_memento-index.json knowledge/_graph-mention-map.json dashboard/index.html
knowledge/_node_titles.json knowledge/_graph-mark-observations.jsonl notes/_subreports/2026-09-28-305-C4-commit.md""".split()
paths = [p for p in want if p in T or p in U]
clean = [p for p in want if p not in paths]
paths += sorted(p for p in (T | U) if p.startswith('notes/_lanes/305/C4/') and p not in paths)
open('notes/_lanes/305/C4/paths-c4b.txt','w').write('\n'.join(paths)+'\n')
print('paths', len(paths), paths); print('clean', clean)
