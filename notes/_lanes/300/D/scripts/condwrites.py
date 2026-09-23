import json
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
seen=set(); n=0
for i,line in enumerate(open(P)):
    d=json.loads(line); m=d.get('message',{})
    if d.get('type')=='attachment':
        a=d['attachment']; 
        if a.get('type') in ('cowork_memory_context','prompt_snapshot','session_context'): print(i,'ATTACH',a.get('type'),d.get('timestamp'))
        continue
    c=m.get('content') if isinstance(m,dict) else None
    if d.get('type')=='assistant' and isinstance(m,dict):
        u=m.get('usage',{}); mid=m.get('id')
        if mid not in seen:
            seen.add(mid); n+=1
            fill=u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0)
            print(i,'ASSIST#%d'%n,'fill',fill,'(in %s cc %s cr %s)'%(u.get('input_tokens'),u.get('cache_creation_input_tokens'),u.get('cache_read_input_tokens')),d.get('timestamp'))
    if isinstance(c,list):
        for b in c:
            if b.get('type')=='tool_use':
                inp=b.get('input',{}); 
                desc={k:(v if k in('path','if_version','cursor','method','query','action','url') else (f'<{len(json.dumps(v))} chars>')) for k,v in (inp.items() if isinstance(inp,dict) else [])}
                print(i,'  TOOL_USE',b.get('name'),json.dumps(desc)[:230])
    if d.get('type')=='user' and isinstance(c,str):
        print(i,'USER-TEXT',len(c),'chars',d.get('timestamp'))
    if d.get('type')=='user' and isinstance(c,list) and any(b.get('type')=='text' for b in c):
        print(i,'USER-TEXT-BLOCKS',sum(len(b.get('text','')) for b in c if b.get('type')=='text'),'chars',d.get('timestamp'))
