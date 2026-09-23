import json, re, sys, collections
sys.argv=['x',sys.argv[1] if len(sys.argv)>1 else '/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl']
import importlib.util
spec=importlib.util.spec_from_file_location('aw','attribute_window.py'); aw=importlib.util.module_from_spec(spec); spec.loader.exec_module(aw)
T=aw.T
A=json.load(open('out/attribution.json')); rt,rs=A['rt'],A['rs']; mem_real=A['resend']['mem_real']
rows=aw.load(sys.argv[1]); snap=aw.snapshot_with_tools(rows); sp=snap['systemPrompt']; tools=snap['tools']
tool={t['name']:T(aw.render_tool(t))*rt for t in tools}
b0=sp[0]
sec={n.strip():t for d,n,t,s,e in aw.xml_sections(b0,2)}
b2=sp[2]; ium=b2.find('<user_memory>')
def sect(h):
    i=b2.find(h); j=b2.find('\n# ',i+3); j=ium if (j<0 or j>ium) else j
    return T(b2[i:j])
chrome=sect('# Claude in Chrome browser automation'); remote=sect('# Your current remote execution environment')
um=T(b2[ium:])
att={}
for i,r in enumerate(rows[:22]):
    if r.get('type')=='attachment':
        s=aw.render_attachment(r['attachment'],aw.ENV_PROXY)
        if s: att[r['attachment']['type']]=s
mcp=rows[12]['attachment']['addedBlocks']; mcp_chrome=T(mcp[0]); mcp_mem=T(mcp[1])
defl=rows[10]['attachment']['addedLines']
def dn(pred): return sum(T(l)+1 for l in defl if pred(l))
skills=rows[13]['attachment']['content']
def sk(names): 
    tot=0
    for it in re.split(r'(?m)^- ',skills):
        if any(it.startswith(n+':') for n in names): tot+=T('- '+it)
    return tot
sc=rows[19]['attachment']['context']
F=collections.OrderedDict()
F['Project memory (snapshot, guidance, 5 tools, MCP note)']=dict(snapshot=mem_real, guidance=um*rs, tools=sum(v for k,v in tool.items() if k.startswith('mcp__memory__')), mcp_note=mcp_mem*rs, deferred=dn(lambda l:l.startswith('mcp__memory'))*rs)
F['Widgets (17 mcp__widgets__ tools)']=dict(tools=sum(v for k,v in tool.items() if k.startswith('mcp__widgets__')))
F['Artifacts (tool, prompt section, skills, deferred names)']=dict(tool=tool['Artifact'], prompt=sec.get('artifacts',0)*rs, skills=sk(['artifact-capabilities','artifact-design','artifact-diagramming'])*rs, deferred=dn(lambda l:l.startswith('Artifact'))*rs)
F['Mac link (remote-devices tools, bridge + env sections, link and folder notes)']=dict(tools=sum(v for k,v in tool.items() if k.startswith('mcp__remote-devices__')), prompt=(sec.get('device_bridge',0)+remote)*rs, deferred=dn(lambda l:l.startswith('mcp__remote-devices') and 'computer_' not in l and 'Claude_Browser' not in l)*rs, link_note=T(rows[2]['message']['content'])*rs, folders=T(att['file'])*rs)
F['Scheduled tasks (triggers, ScheduleWakeup, Cron names, prompt section)']=dict(tools=sum(v for k,v in tool.items() if k.startswith('mcp__claude-code-remote__'))+tool['ScheduleWakeup'], prompt=sec.get('scheduled_tasks',0)*rs, deferred=dn(lambda l:l.startswith('Cron'))*rs)
F['Skills (listing, Skill/propose/suggest tools, prompt sections)']=dict(listing=T(att['skill_listing'])*rs, tools=tool['Skill']+tool['propose_skills']+tool['SuggestSkills'], prompt=(sec.get('skills',0)+T(sp[1]))*rs, deferred=dn(lambda l:l in('ListSkills','SearchSkills'))*rs)
F['claude.ai chat tools (search chats, research, images, time, end)']=dict(tools=sum(v for k,v in tool.items() if k.startswith('mcp__claude_ai__')))
F['Browsers + computer use (Chrome section, MCP note, 22+43+17 names, browser skills)']=dict(prompt=(chrome+sec.get('browsers',0)+sec.get('desktop_computer_use',0))*rs, mcp_note=mcp_chrome*rs, deferred=dn(lambda l:l.startswith('mcp__claude-in-chrome') or 'computer_' in l or 'Claude_Browser' in l)*rs, skills=sk(['anthropic-skills:chrome-browser','anthropic-skills:built-in-browser','anthropic-skills:computer-use','claude-in-chrome'])*rs)
F['Projects tool']=dict(tool=tool['Projects'])
F['Onboarding + review UI (role picker, ReportFindings)']=dict(tools=tool['ShowOnboardingRolePicker']+tool['ReportFindings'])
F['Tasks (TaskCreate/TaskUpdate)']=dict(tools=tool['TaskCreate']+tool['TaskUpdate'])
F['Our Project instructions (session_context attachedProject)']=dict(text=T(sc['attachedProject'])*rs)
tot=0
for k,v in F.items():
    s=sum(v.values()); tot+=s
    print(f"{s:8,.0f}  {k}   ", {a:round(b) for a,b in v.items()})
print(f"{tot:8,.0f}  total attributed to named features (the mapping is INFERENCE; whether each is switchable is lane B's)")
core=['Agent','AskUserQuestion','Bash','Edit','Glob','Grep','ListAgents','Read','ReadNotifications','RefreshMcpTools','SendUserFile','SendUserMessage','ToolSearch','WebFetch','WebSearch','Write']
print(f"{sum(tool[c] for c in core):8,.0f}  core tools not listed above: {', '.join(core)}")
print('claude_behavior',round(sec['claude_behavior']*rs),'agentic_behavior',round(sec['agentic_behavior']*rs))
print({k:round(sec[k]*rs) for k in ['situation','the_work','workspace_and_tools','send_user_message_tool','how_a_task_runs','device_bridge','artifacts','skills','browsers','connectors','scheduled_tasks','desktop_computer_use','workspace','where_files_live','delivering_files','questions_and_task_list','web_content'] if k in sec})
