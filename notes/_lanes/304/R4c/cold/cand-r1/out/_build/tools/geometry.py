"""Driven DOM geometry + computed spacing for every view. Usage: geometry.py WIDTH [theme] -> JSON to stdout."""
import os, sys, json
from playwright.sync_api import sync_playwright
W=os.path.expanduser('~/cold/cand-r1'); URL='file://'+W+'/out/index.html'
width=int(sys.argv[1]) if len(sys.argv)>1 else 1440; theme=sys.argv[2] if len(sys.argv)>2 else 'light'
VIEWS=['overview','accounts','liquidity','payments','fx','risk','trade','reports','messages','settings']
JS = r"""(v)=>{
 const R=e=>{const b=e.getBoundingClientRect();return {x:b.left,y:b.top,w:b.width,h:b.height,r:b.right,b:b.bottom}};
 const out={view:v, issues:[], walls:[], spacing:{}};
 const sec=document.querySelector('#view-'+v);
 const grids=[...sec.querySelectorAll('.c-bento__grid')];
 grids.forEach((g,gi)=>{
   const cs=getComputedStyle(g); const cols=cs.gridTemplateColumns.split(' ').length, cgap=parseFloat(cs.columnGap), rgap=parseFloat(cs.rowGap);
   const tiles=[...g.children].filter(t=>t.classList.contains('c-bento__tile')).map(t=>({id:t.id||t.getAttribute('aria-label')||t.className, ...R(t)}));
   const rows={}; tiles.forEach(t=>{const k=Math.round(t.y); (rows[k]=rows[k]||[]).push(t)});
   const rowKeys=Object.keys(rows).map(Number).sort((a,b)=>a-b);
   const gr=R(g);
   rowKeys.forEach((k,ri)=>{ const row=rows[k].sort((a,b)=>a.x-b.x);
     const bottoms=row.map(t=>Math.round(t.b)); if(Math.max(...bottoms)-Math.min(...bottoms)>1) out.issues.push('RAGGED row in grid '+gi+': bottoms '+bottoms.join('/')+' ('+row.map(t=>t.id).join(', ')+')');
     for(let i=1;i<row.length;i++){ const gap=row[i].x-row[i-1].r; if(Math.abs(gap-cgap)>1) out.issues.push('GUTTER '+gap.toFixed(1)+' vs '+cgap+' between '+row[i-1].id+' and '+row[i].id); }
     const used=row.reduce((s,t)=>s+t.w,0)+cgap*(row.length-1); if(Math.abs(used-gr.w)>2) out.issues.push('ROW NOT FULL in grid '+gi+': '+used.toFixed(0)+' of '+gr.w.toFixed(0)+' ('+row.map(t=>t.id).join(', ')+')');
     if(ri>0){ const prevB=Math.max(...rows[rowKeys[ri-1]].map(t=>t.b)); const vg=k-prevB; if(Math.abs(vg-rgap)>1.5) out.issues.push('ROW GAP '+vg.toFixed(1)+' vs '+rgap+' in grid '+gi); }
   });
   out.walls.push({grid:gi, cols, cgap, rgap, w:Math.round(gr.w), tiles:tiles.map(t=>t.id+'@'+Math.round(t.x-gr.x)+','+Math.round(t.y-gr.y)+' '+Math.round(t.w)+'x'+Math.round(t.h))});
 });
 // tiles: overflow + dead space
 [...sec.querySelectorAll('[id^="t-"]')].forEach(t=>{
   const tr=R(t); if(t.scrollWidth>t.clientWidth+1) out.issues.push('H-OVERFLOW '+t.id+' scrollWidth '+t.scrollWidth+' > '+t.clientWidth);
   let maxB=tr.y; let overR=[]; t.querySelectorAll('*').forEach(e=>{ if(e.closest('.scroll,.dg-scroll,.dv-stage,.dv-tablepanel,template,[hidden],.menu,.colmenu')) return; const r=e.getBoundingClientRect(); if(!r.width&&!r.height) return; if(getComputedStyle(e).visibility==='hidden'||getComputedStyle(e).position==='absolute') return; maxB=Math.max(maxB,r.bottom); if(r.right>tr.r+1) overR.push(e.tagName+'.'+(e.className.baseVal!==undefined?e.className.baseVal:e.className)+' +'+(r.right-tr.r).toFixed(0)); });
   if(overR.length) out.issues.push('CHILD PAST RIGHT EDGE in '+t.id+': '+overR.slice(0,3).join(' | '));
   const pb=parseFloat(getComputedStyle(t).paddingBottom)||0; const dead=tr.b-pb-maxB; if(dead>48) out.issues.push('DEAD SPACE '+dead.toFixed(0)+'px under content in '+t.id);
 });
 // clipping of short labels
 sec.querySelectorAll('.kpi-lbl, .kpi-val, .dv-title, .t-cm-section-label, .lim-label, h3').forEach(e=>{ if(e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflow!=='visible') out.issues.push('TEXT CLIPPED '+e.textContent.slice(0,40)); });
 const g=sec.querySelector('.ceo-ground'), cs=getComputedStyle(g); out.spacing.ground={padding:cs.padding, bg:cs.backgroundColor};
 const st=sec.querySelector('.tpl-page'); out.spacing.stackGap=getComputedStyle(st).rowGap;
 const sc=sec.querySelector('.stat-card'); if(sc) out.spacing.statCardPadding=getComputedStyle(sc).padding;
 const kp=sec.querySelector('.kpi-tile'); if(kp) out.spacing.kpi={padding:getComputedStyle(kp).padding, h:Math.round(R(kp).h)};
 const h2=sec.querySelector('.tpl-page > h2'); const wall=sec.querySelector('.tpl-wall'); if(h2&&wall) out.spacing.headingToWall=(R(wall).y-R(h2).b).toFixed(1);
 return out; }"""
res={'width':width,'theme':theme,'views':[],'console':[]}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx=b.new_context(viewport={'width':width,'height':900}); pg=ctx.new_page()
    pg.on('console', lambda m: res['console'].append((m.type, m.text)) if m.type in ('error','warning') else None); pg.on('pageerror', lambda e: res['console'].append(('pageerror', str(e))))
    for v in VIEWS:
        pg.goto(URL+'?view='+v+'&theme='+theme); pg.wait_for_timeout(900)
        r=pg.evaluate(JS, v); r['renderErrors']=pg.evaluate("()=>CEO_APP.renderErrors.concat(CEO_APP.chartErrors)"); res['views'].append(r)
    b.close()
print(json.dumps(res, indent=1))
