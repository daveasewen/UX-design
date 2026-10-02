import json,sys,re
g=sys.argv[1]; root=f'/home/claude/cr/{g}/Apollo-Spider-v1.0.15'
calls=[]
for l in open(f'/home/claude/cr/{g}.stream.jsonl'):
    e=json.loads(l)
    if e.get('type')=='assistant':
        for c in e['message'].get('content',[]):
            if c.get('type')=='tool_use': calls.append((c['name'],c['input']))
flags=[]
for n,i in calls:
    s=json.dumps(i)
    if n=='Read':
        p=i.get('file_path','')
        if not p.startswith(root) or re.search(r'/_[^/]*\.py$',p) or re.search(r'/(notes|reviews|_DECISION-HISTORY)/|_rulings\.json|_CHAIN|GOOD-MORNING|_LIVE-STATE',p): flags.append(('READ',p))
    if n=='Bash':
        cmd=i.get('command','')
        if re.search(r'(cat|head|tail|less|sed -n|grep)[^|;&]*_[A-Za-z0-9_]+\.py',cmd) and not re.search(r'python3?\s',cmd.split('|')[0]): flags.append(('BASH-READPY',cmd[:200]))
        if re.search(r'/home/claude/(apollo|w-|cr/(cand|G[123]/(?!Apollo)))|playwright|chromium|_validate_|run-gates|screenshot|_screen_load|_rulings|notes/|_memento_search',cmd): flags.append(('BASH',cmd[:200]))
    if n in('Glob','Grep'):
        p=i.get('path','') or ''
        if p and not p.startswith(root): flags.append((n,s[:200]))
print(g,'calls',len(calls)); 
for f in flags: print(' FLAG',f)
