import re, os, json, glob
F='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb/tool-results/mcp-memory-memory_read-1790176546093.txt'
t=open(F).read()
print('first 200 chars:',repr(t[:200]))
parts=re.split(r'^=== (/\S+) ===\n',t,flags=re.M)
out='/mnt/user-data/outputs/D-sample'; os.makedirs(out,exist_ok=True)
PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
n=0
for i in range(1,len(parts),2):
    p=parts[i]; body=parts[i+1]
    # drop the [updated..][version..] header line
    body=re.sub(r'^\[updated: [^\]]*\] \[version: [^\]]*\][^\n]*\n','',body)
    name=p.replace(PRJ,'').replace('/','__')
    open(os.path.join(out,name),'w').write(body); n+=1
print('split',n)
# add conductor reads + my earlier reads from transcripts
base='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb'
for P in [base+'.jsonl', base+'/subagents/agent-a23a3fec975143ffe.jsonl']:
    uses={}
    for line in open(P):
        d=json.loads(line); m=d.get('message',{}); c=m.get('content') if isinstance(m,dict) else None
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')=='tool_use' and b.get('name','').endswith('memory_read'): uses[b['id']]=b.get('input')
            if b.get('type')=='tool_result' and b.get('tool_use_id') in uses:
                cc=b.get('content'); tt=cc if isinstance(cc,str) else '\n'.join(x.get('text','') for x in (cc or []) if isinstance(x,dict))
                if 'exceeds maximum allowed tokens' in tt: continue
                ps=re.split(r'^=== (/\S+) ===\n',tt,flags=re.M)
                if len(ps)==1:
                    inp=uses[b['tool_use_id']]; pth=inp.get('path'); pth=pth[0] if isinstance(pth,list) else pth
                    ps=['',pth,tt]
                for i in range(1,len(ps),2):
                    body=re.sub(r'^\[updated: [^\]]*\] \[version: [^\]]*\][^\n]*\n','',ps[i+1])
                    name=ps[i].replace(PRJ,'').replace('/','__')
                    fn=os.path.join(out,name)
                    if not os.path.exists(fn): open(fn,'w').write(body); print('added',name,len(body))
print(sorted(os.listdir(out)))
