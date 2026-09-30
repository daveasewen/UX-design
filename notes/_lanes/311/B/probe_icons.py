"""#311 lane B — count pure-white icon paint on the banking demo in dark, per theme.
An icon = an <svg> that is not a chart canvas (.dv-svg), or anything inside it; painted white = computed fill or
stroke rgb(255,255,255) on a visible shape. Also reports ::before/::after mask/background icons painting white.
Usage: python3 probe_icons.py [before-canon-path]   (run at the seat after seat_env.sh)"""
import os, sys, json
from playwright.sync_api import sync_playwright
R=os.getcwd(); DEMO=f"file://{R}/dashboards/international-banking-dashboard.canon.html"
ARGS=[a for a in sys.argv[1:] if not a.startswith("-")]
if ARGS: DEMO=ARGS[0]
SET="""([th,mode])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode); document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));}"""
PROBE="""()=>{const W='rgb(255, 255, 255)'; const out=[];
 const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
 const desc=e=>{const s=e.closest('svg');const host=s?s.parentElement:e;return (s?('svg.'+(s.getAttribute('class')||'').split(' ').join('.')):e.tagName)+' in '+host.tagName.toLowerCase()+'.'+(host.className&&host.className.baseVal===undefined?String(host.className).split(' ').slice(0,2).join('.'):'')};
 document.querySelectorAll('svg').forEach(s=>{ if(s.closest('.dv-svg')) return;
   [s,...s.querySelectorAll('path,circle,rect,line,polyline,polygon,ellipse,use,text')].forEach(e=>{ if(!vis(e)) return; const cs=getComputedStyle(e);
     const f=cs.fill, st=cs.stroke; const hit=(e!==s)&&((f===W&&cs.fillOpacity!=='0')||(st===W&&st!=='none'&&cs.strokeWidth!=='0px'));
     if(hit) out.push({kind:'svg-shape',where:desc(e),fill:f,stroke:st,color:cs.color});});});
 const pseudo=[]; document.querySelectorAll('body *').forEach(e=>{ if(!vis(e)) return; for(const p of ['::before','::after']){const cs=getComputedStyle(e,p); if(cs.content==='none'||cs.content==='normal') continue;
   const m=cs.maskImage||cs.webkitMaskImage; if(m&&m!=='none'&&cs.backgroundColor===W) pseudo.push({kind:'mask'+p,where:e.tagName.toLowerCase()+'.'+String(e.className).split(' ').slice(0,2).join('.')});}});
 const icons=[...document.querySelectorAll('svg')].filter(s=>!s.closest('.dv-svg')&&vis(s)).map(s=>({cls:s.getAttribute('class'),color:getComputedStyle(s).color,host:s.parentElement.className}));
 return {white:out,pseudo,icons}}"""
THEMES=[("mono",""),("console","console"),("common","legacy"),("supercharge","supercharge")]
res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":1440,"height":900})
    for nm,th in THEMES:
        pg.goto(DEMO); pg.wait_for_timeout(400); pg.evaluate(SET,[th,"dark"]); pg.wait_for_timeout(600)
        r=pg.evaluate(PROBE); res[nm]=r
        print(nm,"white shapes",len(r["white"]),"white mask pseudos",len(r["pseudo"]),"icons",len(r["icons"]))
        for w in r["white"][:40]: print("   ",w)
        for w in r["pseudo"][:20]: print("   ",w)
        if "-v" in sys.argv:
            for i in r["icons"]: print("     icon",i)
    b.close()
json.dump(res,open(os.environ.get("OUTJSON","/dev/shm/probe.json"),"w"),indent=1)
