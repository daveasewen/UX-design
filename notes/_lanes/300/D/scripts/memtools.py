import json, tiktoken, re
enc=tiktoken.get_encoding('cl100k_base')
def tk(s): return len(enc.encode(s, disallowed_special=()))
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
sp=None; tl=None
for i,line in enumerate(open(P)):
    d=json.loads(line)
    if d.get('type')=='attachment' and d['attachment'].get('type')=='prompt_snapshot':
        a=d['attachment']; print('line',i,'keys',list(a.keys()))
        if a.get('systemPrompt') is not None and sp is None: sp=a['systemPrompt']
        if a.get('tools') is not None and tl is None: tl=a['tools']
if isinstance(tl,str): tl=json.loads(tl)
print('tools n',len(tl))
mem=[t for t in tl if isinstance(t,dict) and 'memory' in t.get('name','')]
tot=0
for t in mem:
    s=json.dumps(t,ensure_ascii=False); n=tk(s); tot+=n; print('  tool',t.get('name'),'cl100k',n)
print('memory tools total cl100k',tot, '| all tools cl100k', tk(json.dumps(tl,ensure_ascii=False)))
txt='\n'.join((x.get('text','') if isinstance(x,dict) else str(x)) for x in sp) if isinstance(sp,list) else sp
print('system prompt cl100k',tk(txt))
for kw in ['<user_memory>','</user_memory>','## memory','Persistent memory tools','user_memory_snapshot','memory_write']:
    idx=[m.start() for m in re.finditer(re.escape(kw),txt)]
    print('kw',repr(kw),'hits',len(idx),idx[:6])
open('sysprompt.txt','w').write(txt)
