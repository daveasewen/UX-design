import json, glob, re, os
base='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb'
files=[base+'.jsonl']+sorted(glob.glob(base+'/subagents/*.jsonl'))
os.makedirs('memfiles',exist_ok=True)
got={}
for P in files:
    uses={}
    for line in open(P):
        d=json.loads(line); m=d.get('message',{})
        c=m.get('content') if isinstance(m,dict) else None
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')=='tool_use' and 'memory' in b.get('name',''):
                uses[b['id']]=(b['name'],b.get('input'))
            if b.get('type')=='tool_result' and b.get('tool_use_id') in uses:
                name,inp=uses[b['tool_use_id']]
                if not name.endswith('memory_read'): 
                    continue
                cc=b.get('content'); t=cc if isinstance(cc,str) else '\n'.join(x.get('text','') for x in (cc or []) if isinstance(x,dict))
                # split multi-file results
                parts=re.split(r'^=== (/\S+) ===\n',t,flags=re.M)
                if len(parts)>1:
                    for i in range(1,len(parts),2): got.setdefault(parts[i],(os.path.basename(P),parts[i+1]))
                else:
                    pth=inp.get('path') if isinstance(inp,dict) else None
                    if isinstance(pth,list): pth=pth[0]
                    got.setdefault(pth,(os.path.basename(P),t))
for k,(src,t) in got.items(): print(src[:28], len(t), k)
