# Body-level twin test: every sample memory line >=60 chars -> 60-char needle; grep the repo corpus for it.
import os, re, subprocess, collections, json
D='notes/_lanes/300/D/'
S=D+'sample/'
needles={}  # needle -> set(memfile)
per=collections.defaultdict(list)
for fn in sorted(os.listdir(S)):
    t=open(S+fn,encoding='utf-8',errors='ignore').read()
    # drop frontmatter
    if t.startswith('---\n'):
        k=t.find('\n---\n',4); t=t[k+5:] if k>0 else t
    for line in t.split('\n'):
        s=re.sub(r'^[\s\-\*>#★⛔✅•·\d\.\)]+','',line).strip()
        if len(s)<60: continue
        n=s[:60]
        needles.setdefault(n,set()).add(fn); per[fn].append(n)
open(D+'body-needles.txt','w').write('\n'.join(needles)+'\n')
print('needles',len(needles),'files',len(per))
