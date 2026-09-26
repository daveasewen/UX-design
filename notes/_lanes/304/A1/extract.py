import re,html,glob,subprocess,sys,os,json
pats=['_PROPOSAL-*','_PLAN-*','_BRIEF-*','_RESEARCH-*','_REVIEW-*','_TRIAGE-*','_BUILDOUT-STRATEGY*','_MEMENTO-REBUILD*','_PROCESS-DIAGNOSIS*',
'notes/_PROPOSAL-*','notes/_VISION-*','notes/_PLAN-*','notes/_REVIEW-*','notes/_PROPOSED-*','notes/_SEAWORTHINESS*','notes/_STATE-MACHINE*','notes/_STRATEGY-*','notes/_TEST-PLAN*','notes/_FABLE-BRIEF*',
'notes/2026-0*.md','docs/decisions/ADR-*','archive/*.md','archive/apollo-pipeline-spec*.html','digital-experience-transformation/strategy/*.md','memento-package/_PACKAGE-SPEC.md','system-manager/*.html','system-manager/01*.md',
'reviews/TIER-MAP-PROPOSAL*v2*','notes/_lanes/293/J5/jev-recall-proposal.html','notes/_lanes/293/J7-IDEA*','notes/_lanes/281/orphan-plan/ORPHAN-PLAN*.html',
'notes/_briefs/*proposal*','notes/_briefs/*plan*','notes/_briefs/*strategy*','notes/_briefs/*north-star*','notes/_briefs/*programme*','notes/_briefs/*research*','notes/_briefs/*idea*','notes/_briefs/*apollo-on-claude*','notes/_briefs/*parked*']
files=[]
for p in pats:
    for f in sorted(glob.glob(p)):
        if f not in files: files.append(f)
def text(f):
    s=open(f,errors='ignore').read()
    if f.endswith('.html'):
        m=re.search(r'<title>(.*?)</title>',s,re.S); title=html.unescape(m.group(1).strip()) if m else ''
        s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S)
        s=re.sub(r'<br\s*/?>|</(p|div|li|h\d|tr|section)>','\n',s); s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s)
    else:
        title=next((l.strip('# ').strip() for l in s.splitlines() if l.strip()),'')
    s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
    return title,s
out=[]
for f in files:
    t,s=text(f)
    st=[l.strip()[:220] for l in s.splitlines() if re.search(r'\b(status|STATUS|Status)\b',l)][:3]
    lg=subprocess.run(['git','--no-optional-locks','log','--format=%h %cs','--',f],capture_output=True,text=True).stdout.split('\n')
    lg=[x for x in lg if x]
    out.append(dict(f=f,title=t[:160],size=os.path.getsize(f),status=st,first=(lg[-1] if lg else 'untracked'),last=(lg[0] if lg else ''),ncommits=len(lg),head=s[:600].replace('\n',' | ')))
json.dump(out,open('notes/_lanes/304/A1/inventory.json','w'),indent=1)
print(len(out))
