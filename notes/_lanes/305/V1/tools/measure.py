"""V1 measure.py <tag> — independent re-measure of the B1 calls on V1's own fixtures. 1440, 4 themes x 2 modes."""
import os, sys, json
from playwright.sync_api import sync_playwright
TAG = sys.argv[1]
V = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); FIX = os.path.join(V, TAG, "fix"); OUT = os.path.join(V, "renders", TAG); os.makedirs(OUT, exist_ok=True)
THEMES = ["mono", "common", "console", "supercharge"]; MODES = ["light", "dark"]
LIB = r"""window.__v1=(function(){
 const px=s=>{const m=(s||'').match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};};
 const lum=c=>{const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);};return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);};
 const over=(fg,bg)=>({r:fg.r*fg.a+bg.r*(1-fg.a),g:fg.g*fg.a+bg.g*(1-fg.a),b:fg.b*fg.a+bg.b*(1-fg.a),a:1});
 const hex=o=>'#'+[o.r,o.g,o.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join('');
 function ground(el){const st=[];for(let e=el;e;e=e.parentElement){const c=px(getComputedStyle(e).backgroundColor);if(c&&c.a>0){st.push(c);if(c.a>=1)break;}} let g={r:255,g:255,b:255,a:1}; for(let i=st.length-1;i>=0;i--) g=over(st[i],g); return g;}
 function opac(el){let o=1;for(let e=el;e;e=e.parentElement){o*=parseFloat(getComputedStyle(e).opacity);}return o;}
 function contrast(el){const cs=getComputedStyle(el);const c=px(cs.color);const g=ground(el);const fg=over({...c,a:c.a*opac(el)},g);const L1=lum(fg),L2=lum(g);
  return {ratio:+((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)).toFixed(2),ink:hex(fg),ground:hex(g),color:cs.color,opacity:+opac(el).toFixed(3),size:cs.fontSize};}
 function face(){const cv=document.createElement('canvas').getContext('2d');const s='Hamburgefonstiv 0123456789';cv.font='16px "Univers Next for HSBC", monospace';const a=cv.measureText(s).width;cv.font='16px monospace';const b=cv.measureText(s).width;return Math.abs(a-b)>1;}
 return {contrast,ground,hex,face};})();"""
def theme(pg, th, m):
    pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.documentElement.setAttribute('data-theme',m);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',m));}", [th, m]); pg.wait_for_timeout(300)
KPI = r"""()=>{const rows=[];for(const t of [...document.querySelectorAll('.kpi-tile')].slice(0,4)){const l=t.querySelector('.kpi-lbl'),v=t.querySelector('.kpi-val'),p=t.querySelector('.kpi-per');if(!l||!v)continue;
 const lr=l.getBoundingClientRect(),vr=v.getBoundingClientRect(),tr=t.getBoundingClientRect(),cs=getComputedStyle(l);
 rows.push({lbl:l.textContent.trim().slice(0,20),tileH:+tr.height.toFixed(2),lblBoxH:+lr.height.toFixed(2),lblToVal:+(vr.top-lr.top).toFixed(2),ovX:cs.overflowX,ovY:cs.overflowY,tov:cs.textOverflow,lh:cs.lineHeight,fs:cs.fontSize,
  lblC:__v1.contrast(l),perC:p?__v1.contrast(p):null,spark:t.querySelector('.spark-inline')?+t.querySelector('.spark-inline').getBoundingClientRect().height.toFixed(1):null});}
 const t0=document.querySelector('.kpi-tile .kpi-lbl');let ell=null;if(t0){const k=t0.textContent;t0.textContent='A very long label that cannot possibly fit inside this tile at all ever gpy';ell={sw:t0.scrollWidth,cw:t0.clientWidth,trunc:t0.scrollWidth>t0.clientWidth};t0.textContent=k;}
 return {rows,ell};}"""
DESC = r"""()=>{const ls=[...document.querySelectorAll('.kpi-lbl')].filter(l=>/Card spend|Pending payments/.test(l.textContent)).slice(0,2);const r=ls.map(l=>l.closest('.kpi-tile').getBoundingClientRect());
 const x=Math.min(...r.map(a=>a.left)),y=Math.min(...r.map(a=>a.top));const R=Math.max(...r.map(a=>a.right));return {x:x,y:y+scrollY,width:Math.min(R-x,900),height:70};}"""
NAV = r"""()=>[...document.querySelectorAll('.nv-count')].filter(e=>e.getBoundingClientRect().width>0).slice(0,10).map(e=>({t:e.textContent.trim(),w:+e.getBoundingClientRect().width.toFixed(2),h:+e.getBoundingClientRect().height.toFixed(2),pl:getComputedStyle(e).paddingLeft,pr:getComputedStyle(e).paddingRight}))"""
GRP = r"""()=>[...document.querySelectorAll('.sn-group-label')].filter(e=>e.getBoundingClientRect().width>0).slice(0,2).map(e=>__v1.contrast(e))"""
NOTE = r"""()=>[...document.querySelectorAll('.note')].filter(e=>e.getBoundingClientRect().width>0).map(e=>{const cs=getComputedStyle(e);return {cls:e.className,bw:cs.borderTopWidth,bc:cs.borderTopColor,h:+e.getBoundingClientRect().height.toFixed(2)};})"""
SHELL = r"""()=>{const s=document.querySelector('.sh');if(!s)return null;const a=s.getBoundingClientRect().height;s.classList.add('is-full');const b=s.getBoundingClientRect().height;const cssH=getComputedStyle(s).height;s.classList.remove('is-full');return {plain:+a.toFixed(1),isFull:+b.toFixed(1),cssH};}"""
BENTO = r"""()=>{const q=s=>document.querySelector(s);const g=el=>el?__v1.hex(__v1.ground(el)):null;const own=el=>el?getComputedStyle(el).backgroundColor:null;const tile=q('.c-bento__tile');
 const kpis=[...document.querySelectorAll('.kpi-tile')].map(t=>({h:+t.getBoundingClientRect().height.toFixed(1),spark:t.querySelector('.spark-inline')?+t.querySelector('.spark-inline').getBoundingClientRect().height.toFixed(1):null,lbl:t.querySelector('.lbl16')?__v1.contrast(t.querySelector('.lbl16')):null}));
 const rings=[...document.querySelectorAll('figure.dv[data-dv-type=donut],figure.dv[data-dv-type=pie]')].map(f=>{const t=f.closest('.c-bento__tile');const tr=t?t.getBoundingClientRect():null;const fr=f.getBoundingClientRect();const sib=t?[...t.parentElement.children].filter(c=>c!==t):[];
  return {type:f.getAttribute('data-dv-type'),tileH:tr?+tr.height.toFixed(1):null,tileW:tr?+tr.width.toFixed(1):null,figH:+fr.height.toFixed(1),slack:tr?+(tr.bottom-fr.bottom).toFixed(1):null,alignSelf:t?getComputedStyle(t).alignSelf:null,cssH:t?getComputedStyle(t).height:null,sibMaxH:sib.length?Math.max(...sib.map(c=>+c.getBoundingClientRect().height.toFixed(1))):null};});
 const pg=q('.tpl-page');const hd=q('.tpl-header');
 return {body:g(document.body),bodyOwn:own(document.body),header:g(hd),headerOwn:own(hd),page:g(pg),pageOwn:own(pg),pagePadTop:pg?getComputedStyle(pg).paddingTop:null,tile:g(tile),tileOwn:own(tile),kpis,rings};}"""
DENSE = r"""(n)=>{const figs=[...document.querySelectorAll('figure.dv')].filter(f=>/line|stacked/.test(f.getAttribute('data-dv-type')||''));const out=[];
 for(const f of figs){const sp=f.__dvSpec;if(!sp){out.push('nospec');continue;}const cats=[];for(let i=0;i<n;i++)cats.push((i+1)+' Sep');
  const series=sp.series.slice(0,3).map((s,j)=>({name:s.name,values:cats.map((c,i)=>Math.round(40+20*j+12*Math.sin(i/3+j)+i*0.8))}));
  try{window.dvRender(f,Object.assign({},sp,{categories:cats,series:series}));out.push('ok');}catch(e){out.push(String(e).slice(0,120));}} return out;}"""
COUNT = r"""()=>[...document.querySelectorAll('figure.dv')].filter(f=>/line|stacked/.test(f.getAttribute('data-dv-type')||'')).map(f=>{const painted=e=>{const c=getComputedStyle(e);return c.display!=='none'&&c.visibility!=='hidden'&&e.getBoundingClientRect().width>0;};
 let mk=0,lt=0;f.querySelectorAll('.dv-mk').forEach(e=>{if(painted(e))mk++;});f.querySelectorAll('text.dv-barkey').forEach(e=>{if(painted(e))lt++;});
 const cats=(f.__dvSpec||{}).categories;return {type:f.getAttribute('data-dv-type'),cats:cats?cats.length:null,series:(f.__dvSpec||{}).series?f.__dvSpec.series.length:null,markers:mk,letters:lt,focus:f.querySelectorAll('g.dv-marker[tabindex]').length,tips:f.querySelectorAll('[data-tip]').length,mkAll:f.querySelectorAll('.dv-mk').length};})"""
res = {}
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    def page(path, dsf=1, h=1000):
        c = br.new_context(viewport={"width":1440,"height":h}, device_scale_factor=dsf, reduced_motion="reduce"); pg = c.new_page(); pg.goto("file://"+path); pg.wait_for_timeout(900); pg.evaluate(LIB); return c, pg
    c, pg = page(os.path.join(FIX,"Kpi-tile.html")); res["face"] = pg.evaluate("__v1.face()")
    for th in THEMES:
        for m in MODES:
            theme(pg, th, m); res["kpi-%s-%s"%(th,m)] = pg.evaluate(KPI)
    c.close()
    for m in MODES:
        c, pg = page(os.path.join(FIX,"Kpi-tile.html"), dsf=4); theme(pg,"common",m); bb=pg.evaluate(DESC); pg.screenshot(path=os.path.join(OUT,"kpi-desc-common-%s-4x.png"%m), clip=bb, full_page=True); c.close()
    for name in ("Sidebar-nav","Navigations","Tab-bar"):
        c, pg = page(os.path.join(FIX,name+".html")); theme(pg,"common","light"); res["nav-%s"%name] = pg.evaluate(NAV)
        if name=="Sidebar-nav":
            for th in THEMES:
                for m in MODES: theme(pg,th,m); res["grp-%s-%s"%(th,m)] = pg.evaluate(GRP)
        c.close()
    c, pg = page(os.path.join(FIX,"App-shell-side-nav.html")); theme(pg,"common","light"); res["shell"] = pg.evaluate(SHELL)
    for th in THEMES:
        for m in MODES: theme(pg,th,m); res["shellgrp-%s-%s"%(th,m)] = pg.evaluate(GRP)
    c.close()
    c, pg = page(os.path.join(FIX,"Notifications.html"))
    for th in THEMES:
        for m in MODES: theme(pg,th,m); res["note-%s-%s"%(th,m)] = pg.evaluate(NOTE)
    c.close()
    c, pg = page(os.path.join(FIX,"Template-dashboard-bento.html"), h=1400)
    for th in THEMES:
        for m in MODES:
            theme(pg,th,m); pg.wait_for_timeout(600); res["bento-%s-%s"%(th,m)] = pg.evaluate(BENTO)
            if th in ("mono","supercharge"): pg.screenshot(path=os.path.join(OUT,"bento-%s-%s.png"%(th,m)), full_page=True)
    c.close()
    for name in ("Chart-line","Chart-stacked-area","Chart-combo"):
        c, pg = page(os.path.join(FIX,name+".html")); theme(pg,"common","light"); res["dense-%s-own"%name]=pg.evaluate(COUNT)
        r = pg.evaluate(DENSE, 30); pg.wait_for_timeout(800); res["dense-%s-30"%name]={"render":r,"count":pg.evaluate(COUNT)}
        pg.screenshot(path=os.path.join(OUT,"dense-%s-30.png"%name), full_page=True); c.close()
    br.close()
json.dump(res, open(os.path.join(OUT,"measure.json"),"w"), indent=1)
for k in res: print(k, json.dumps(res[k])[:700])
