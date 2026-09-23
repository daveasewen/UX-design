import os, re, collections
D='notes/_lanes/300/D/'; S=D+'sample/'
per=collections.defaultdict(list); nmap=collections.defaultdict(set)
for fn in sorted(os.listdir(S)):
    t=open(S+fn,encoding='utf-8',errors='ignore').read()
    if t.startswith('---\n'):
        k=t.find('\n---\n',4); t=t[k+5:] if k>0 else t
    for line in t.split('\n'):
        s=re.sub(r'^[\s\-\*>#★⛔✅•·\d\.\)]+','',line).strip()
        if len(s)<60: continue
        per[fn].append(s[:60]); nmap[s[:60]].add(fn)
found=collections.defaultdict(set)
for l in open(D+'hits-body.txt',encoding='utf-8',errors='ignore'):
    l=l.rstrip('\n')
    # path:needle  (path has no ':' in this repo? split on first ':')
    p,_,n=l.partition(':')
    found[n].add(p)
def kind(p):
    if '_retired/agent-memory-snapshot' in p: return 'retired-0718'
    if '/WRAP-MEMORY-HOOK' in p: return 'wrap-hook'
    if '_memento-index' in p: return 'memento-index'
    if p.startswith('./_CARRIES') or p.startswith('./_GM-ARCHIVE'): return 'carries/gm-archive'
    return 'other'
print(f"{'memory file':62s} lines found  where")
tot=totf=0
for fn,ns in per.items():
    f=[n for n in ns if n in found]
    kinds=collections.Counter(kind(p) for n in f for p in found[n])
    tops=collections.Counter(p for n in f for p in found[n]).most_common(2)
    tot+=len(ns); totf+=len(f)
    print(f"{fn[:62]:62s} {len(ns):4d} {len(f):4d}  {dict(kinds)} {[t[0][-60:] for t in tops]}")
print('TOTAL lines',tot,'found',totf, '%.0f%%'%(100*totf/max(tot,1)))
