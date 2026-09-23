import json, tiktoken, hashlib
enc=tiktoken.get_encoding('cl100k_base')
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
snaps=[]
with open(P) as f:
    for i,line in enumerate(f):
        d=json.loads(line)
        if d.get('type')=='attachment' and d['attachment'].get('type')=='cowork_memory_context':
            snaps.append((i,d['attachment']))
for i,a in snaps:
    c=a['content']
    print('line',i,'version',a.get('version'),'content type',type(c).__name__)
    if isinstance(c,str):
        print(' chars',len(c),'cl100k',len(enc.encode(c)),'sha',hashlib.sha1(c.encode()).hexdigest()[:12],'lines',c.count('\n')+1)
    else:
        print(' json',json.dumps(c)[:300])
# save both for local analysis
for i,a in snaps:
    open(f'snap_{i}.txt','w').write(a['content'] if isinstance(a['content'],str) else json.dumps(a['content']))
