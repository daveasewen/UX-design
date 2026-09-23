import json, re
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb/subagents/agent-a23a3fec975143ffe.jsonl'
pat=re.compile(r'^(/\S+)\s+\((\d+) bytes, updated (\S+)\)$')
seen={}
with open(P) as f:
    for line in f:
        d=json.loads(line)
        m=d.get('message',{})
        c=m.get('content') if isinstance(m,dict) else None
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')=='tool_result':
                cc=b.get('content')
                texts=[]
                if isinstance(cc,str): texts=[cc]
                elif isinstance(cc,list): texts=[x.get('text','') for x in cc if isinstance(x,dict)]
                for t in texts:
                    for l in t.split('\n'):
                        mm=pat.match(l.strip())
                        if mm: seen[mm.group(1)]=(int(mm.group(2)),mm.group(3))
rows=sorted(seen.items())
with open('store_listing.tsv','w') as o:
    for p,(b,u) in rows: o.write(f'{p}\t{b}\t{u}\n')
PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
prj=[r for r in rows if r[0].startswith(PRJ)]
acc=[r for r in rows if not r[0].startswith('/projects/')]
oth=[r for r in rows if r[0].startswith('/projects/') and not r[0].startswith(PRJ)]
print('total files',len(rows),'project',len(prj),'account',len(acc),'other-projects',len(oth))
print('bytes total',sum(b for _,(b,_) in rows),'project bytes',sum(b for _,(b,_) in prj),'account bytes',sum(b for _,(b,_) in acc))
print('account files:',[p for p,_ in acc])
