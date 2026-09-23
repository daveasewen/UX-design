import json, re
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb/subagents/agent-a23a3fec975143ffe.jsonl'
PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
pat=re.compile(r'^(/\S+)\s+\((\d+) bytes, updated (\S+)\)$')
prev={}
with open(P) as f:
    for line in f:
        d=json.loads(line); m=d.get('message',{})
        c=m.get('content') if isinstance(m,dict) else None
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')!='tool_result': continue
            cc=b.get('content'); texts=[cc] if isinstance(cc,str) else [x.get('text','') for x in (cc or []) if isinstance(x,dict)]
            for t in texts:
                ls=t.split('\n')
                for i,l in enumerate(ls):
                    mm=pat.match(l.strip())
                    if mm and i+1<len(ls) and ls[i+1].startswith('  ') and not pat.match(ls[i+1].strip()):
                        prev[mm.group(1)]=ls[i+1].strip()
print('previews',len(prev))
rows=[l.rstrip('\n').split('\t') for l in open('/mnt/user-data/outputs/D-store-census.tsv')]
hdr=rows[0]+['preview']; out=[hdr]
for r in rows[1:]:
    full=(PRJ+r[1]) if r[0]=='project' else r[1]
    out.append(r+[prev.get(full,'').replace('\t',' ')])
open('/mnt/user-data/outputs/D-store-census.tsv','w').write('\n'.join('\t'.join(x) for x in out)+'\n')
print('missing previews',sum(1 for x in out[1:] if not x[-1]))
