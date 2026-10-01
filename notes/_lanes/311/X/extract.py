import json, glob, os, sys, datetime
base='/root/.claude/projects/-home-claude/0b1b95b8-58ce-5893-b9c8-d6756fa9a585'
files=[base+'.jsonl']+glob.glob(base+'/subagents/*.jsonl')
rows=[]
for f in files:
    agent=os.path.basename(f).replace('.jsonl','')
    if agent.startswith('0b1b'): agent='conductor'
    pending={}
    with open(f) as fh:
        for line in fh:
            try: d=json.loads(line)
            except: continue
            t=d.get('type'); msg=d.get('message') or {}
            content=msg.get('content')
            ts=d.get('timestamp')
            if t=='assistant' and isinstance(content,list):
                for c in content:
                    if c.get('type')=='tool_use' and c.get('name')=='mcp__remote-devices__device_bash':
                        pending[c['id']]={'agent':agent,'start':ts,'timeout_ms':c['input'].get('timeout_ms'),'cmd':c['input'].get('command','')[:160]}
            if t=='user' and isinstance(content,list):
                for c in content:
                    if c.get('type')=='tool_result' and c.get('tool_use_id') in pending:
                        p=pending.pop(c['tool_use_id'])
                        p['end']=ts
                        rc=c.get('content')
                        txt=''
                        if isinstance(rc,list):
                            txt=' '.join(x.get('text','') for x in rc if isinstance(x,dict))
                        elif isinstance(rc,str): txt=rc
                        p['is_error']=c.get('is_error',False)
                        p['result']=txt[:400]
                        # tool result metadata may be in toolUseResult
                        rows.append(p)
    for k,p in pending.items():
        p['end']=None; p['is_error']=None; p['result']='(no result recorded)'; rows.append(p)
def parse(ts): return datetime.datetime.fromisoformat(ts.replace('Z','+00:00')) if ts else None
for r in rows:
    s=parse(r['start']); e=parse(r['end'])
    r['dur_s']=round((e-s).total_seconds(),1) if s and e else None
rows.sort(key=lambda r:r['start'])
json.dump(rows,open('calls.json','w'),indent=1,default=str)
print(len(rows),'calls')
