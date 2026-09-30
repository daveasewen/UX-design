import os,json,sys
from playwright.sync_api import sync_playwright
R=os.getcwd()
SET="""([th,mode,opt])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode);
  document.querySelectorAll('[data-theme]').forEach(e=>{e.setAttribute('data-theme',mode);
    if(opt) e.setAttribute('data-dark-tiles',opt); else e.removeAttribute('data-dark-tiles');});}"""
PROBE="""()=>{const out={};const tiles=[...document.querySelectorAll('.dashboard-tile')];
 const tb=getComputedStyle(tiles[0]).backgroundColor;
 tiles.forEach(t=>t.querySelectorAll('*').forEach(e=>{const tx=[...e.childNodes].filter(n=>n.nodeType==3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
   if(!tx) return; const cs=getComputedStyle(e); const k=cs.color+' | '+cs.fontSize+' '+cs.fontWeight;
   (out[k]=out[k]||{n:0,ex:[],cls:new Set()}); out[k].n++; if(out[k].ex.length<4) out[k].ex.push(tx.slice(0,30)); out[k].cls.add((e.className&&e.className.baseVal===undefined?e.className:'svg')+'');}));
 const vars={}; const cs=getComputedStyle(tiles[0]); for(const v of ['--text-default','--text-secondary','--text-tertiary','--rag-success','--rag-error','--rag-warning','--rag-success-ink','--rag-error-ink','--text-muted','--muted','--ink','--surface']) vars[v]=cs.getPropertyValue(v).trim();
 return {tile:tb, vars, inks:Object.fromEntries(Object.entries(out).map(([k,v])=>[k,{n:v.n,ex:v.ex,cls:[...v.cls].slice(0,6)}]))}}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":1440,"height":900})
    pg.goto("file://"+R+"/dashboards/international-banking-dashboard.canon.html"); pg.wait_for_timeout(600)
    pg.evaluate(SET,[sys.argv[1] if len(sys.argv)>1 else "console","dark",""]); pg.wait_for_timeout(900)
    print(json.dumps(pg.evaluate(PROBE),indent=1))
    b.close()
