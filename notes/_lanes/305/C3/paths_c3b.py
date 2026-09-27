# #305 C3 - the stamps commit's path list; every path checked changed-or-untracked first.
import subprocess
def g(*a):
    return subprocess.run(['git','--no-optional-locks',*a],capture_output=True,text=True)
T = set(l for l in g('diff','--name-only','HEAD').stdout.split('\n') if l)
U = set(l for l in g('ls-files','--others','--exclude-standard').stdout.split('\n') if l)
want = ['knowledge/_rulings.json','notes/_RULINGS.html','_CHAIN.md','reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html',
        'notes/_subreports/2026-09-27-305-C3-commit.md','knowledge/_state.json','dashboard/index.html',
        'knowledge/_memento-index.json','knowledge/_graph-mention-map.json','knowledge/_graph-mark-observations.jsonl',
        'tokens/_blast-radius.json','tokens/_GRAPH-REPORT.md']
paths = [p for p in want if p in T]
paths += sorted(p for p in U if p.startswith('notes/_lanes/305/C3/') and '/__pycache__/' not in p)
for p in paths: assert p in T or p in U, p
open('notes/_lanes/305/C3/paths-c3b.txt','w').write('\n'.join(paths)+'\n')
print('paths', len(paths)); print('\n'.join(paths))
