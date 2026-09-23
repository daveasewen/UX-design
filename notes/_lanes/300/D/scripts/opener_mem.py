import json, tiktoken
enc=tiktoken.get_encoding('cl100k_base')
def tk(s): return len(enc.encode(s, disallowed_special=()))
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
uses={}; rows=[]
for i,line in enumerate(open(P)):
    d=json.loads(line); m=d.get('message',{}); c=m.get('content') if isinstance(m,dict) else None
    if not isinstance(c,list): continue
    for b in c:
        if b.get('type')=='tool_use':
            uses[b['id']]=(i,b['name'],tk(json.dumps(b.get('input'),ensure_ascii=False)))
        if b.get('type')=='tool_result' and b.get('tool_use_id') in uses:
            ui,name,intk=uses[b['tool_use_id']]
            cc=b.get('content'); t=cc if isinstance(cc,str) else '\n'.join(x.get('text','') for x in (cc or []) if isinstance(x,dict))
            rows.append((ui,name,intk,tk(t)))
tot_in=tot_out=0
for ui,name,a,r in rows:
    if 'memory' in name:
        print(ui,name,'input cl100k',a,'result cl100k',r); tot_in+=a; tot_out+=r
print('memory tool traffic total: inputs',tot_in,'results',tot_out,'sum',tot_in+tot_out)
