import json, sys, csv, importlib.util
spec=importlib.util.spec_from_file_location('aw','attribute_window.py'); aw=importlib.util.module_from_spec(spec); spec.loader.exec_module(aw)
T=aw.T
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
A=json.load(open('out/attribution.json')); rs=A['rs']
rows=aw.load(P); msgs=aw.messages(rows)
items=[]
# boot items from CSV (tools, system sections, attachments)
BY={'Artifact':'feature: Artifacts','Projects':'feature: Projects (claude.ai Project binding)',
    'ScheduleWakeup':'feature: scheduled tasks (inference)','TaskUpdate':'harness: task list','TaskCreate':'harness: task list',
    'AskUserQuestion':'harness: questions','SendUserFile':'harness: file delivery','Grep':'harness: core'}
for r in csv.DictReader(open('out/boot_items.csv')):
    name=r['item']; g=r['group']; real=float(r['real_est'])
    if g.startswith('tool: mcp__widgets'): by='feature: in-chat widgets (inference)'
    elif g.startswith('tool: mcp__claude-code-remote'): by='feature: scheduled tasks (inference)'
    elif g.startswith('tool: mcp__remote-devices'): by='connector: the Mac link (device bridge)'
    elif g.startswith('tool: mcp__memory'): by='feature: Project memory'
    elif g.startswith('tool: mcp__claude_ai'): by='feature: claude.ai chat tools (inference)'
    elif g=='system prompt':
        by={'agentic_behavior':'harness: agent/Cowork base prompt (fixed, inference)','claude_behavior':'harness: claude.ai base prompt (fixed)',
            '<user_memory> guidance (block 2)':'feature: Project memory','Your current remote execution environment (block 2)':'connector: the Mac link + cloud container',
            'Claude in Chrome browser automation (block 2)':'setting: Claude in Chrome (inference)','Saving skills (block 1)':'feature: skills'}.get(name,'harness')
    elif name=='att:cowork_memory_context': by='feature: Project memory (cloud leg); content = our store listing'
    elif name=='att:skill_listing': by='setting: skills enabled (22; four are Dave\'s own)'
    elif name=='att:deferred_tools_delta': by='harness: tool search (114 deferred names)'
    elif name=='att:session_context': by='our own instruction: Project instructions (+ email line)'
    else: by=BY.get(name,'harness')
    band='HARNESS' if r['band']!='OPENER' else 'OPENER'
    items.append((real,'boot',name,by,int(r['tape_cl100k'])))
LAB={30:('ls of the mount','opener: conductor finding the repo'),31:('memory_read index.md','our own instruction (step 3)'),
     33:('dave-voice skill body','our own instruction (reply in dave-voice)'),42:('ls repo root','opener: conductor finding the handoff'),
     46:('cat _HANDOFF-150','our own instruction (step 1)'),54:('cat _CHAIN.md','our own instruction (step 2)'),
     55:('memory_list page','our own instruction (step 3)'),66:('cat #299 WRAP-MEMORY-HOOK.md','our own instruction (step 6)'),
     77:('memory_read MEMORY-ARCHIVE-3 + presentation area','opener: conductor\'s judgment (index pointers)'),
     110:('git log + rulings read','opener: conductor\'s judgment'),118:('grep for "the ask"','opener: conductor\'s judgment'),
     130:('memory snapshot RE-SENT (byte-identical)','feature: Project memory, triggered by the opener\'s store writes'),
     128:('Dave\'s #300 message','Dave'),139:('tiktoken check of the window','conductor at work')}
for m in msgs:
    pass
for i,r in enumerate(rows):
    if i in LAB and r.get('type') in ('user','attachment'):
        if r['type']=='user': t=T(aw.user_text(r))
        else: t=T(aw.render_attachment(r['attachment'],''))
        real=t*rs if i!=130 else A['resend']['mem_real']
        items.append((real,'opener' if i<126 else 'running',LAB[i][0],LAB[i][1],t))
OUTLAB={7:('hook placement turn: memory_write/append/str_replace + thinking','our own instruction (step 6)'),
        13:('the first beat: reply + thinking','our own instruction (first beat in dave-voice)'),
        14:('conductor reasoning on Dave\'s "think hard" message (thinking retained)','the conductor thinking in-seat (retained in window)'),
        16:('writing BRIEF-300 in-seat + message + thinking','our procedure: brief written at the conductor'),
        9:('index.md str_replace (hook cut)','our own instruction (step 6)'),12:('grep for the ask + thinking','conductor at work')}
for k,m in enumerate(msgs[:-1]):
    n=k+1
    if n in OUTLAB:
        items.append((m['out'],'opener' if n<=13 else 'running','output of msg %d: %s'%(n,OUTLAB[n][0]),OUTLAB[n][1],None))
items.sort(key=lambda x:-x[0])
with open('out/top_items.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['rank','real_est','band','item','brought_in_by','tape'])
    for i,(real,band,name,by,t) in enumerate(items,1): w.writerow([i,round(real),band,name,by,t if t is not None else 'REAL (output_tokens)'])
for i,(real,band,name,by,t) in enumerate(items[:30],1):
    print(f"{i:2d} {real:8,.0f} {band:7s} {name[:62]:62s} | {by}")
