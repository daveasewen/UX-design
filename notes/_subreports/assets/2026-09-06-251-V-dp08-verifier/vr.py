import json
from playwright.sync_api import sync_playwright
PAGE='/sessions/bold-focused-hopper/mnt/UX-design/knowledge/snippets/Template-dashboard-bento.reference.html'
OUT='/tmp/v251'
PROBE=r"""()=>{
const r=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {x:+b.left.toFixed(1),y:+(b.top+scrollY).toFixed(1),w:+b.width.toFixed(1),h:+b.height.toFixed(1)}};
const lead=document.querySelector('.tpl-group-lead');
const grid=lead.querySelector(':scope>.c-bento__grid');
const tiles=[...lead.querySelectorAll(':scope>.c-bento__grid>.kpi-tile')];
const boxes=tiles.map(t=>({label:t.getAttribute('aria-label'),...r(t)}));
const rows={};boxes.forEach(b=>{const k=Math.round(b.y);(rows[k]=rows[k]||[]).push(b);});
const rk=Object.keys(rows).map(Number).sort((a,b)=>a-b);
const ws=boxes.map(b=>b.w);
const gcs=getComputedStyle(grid);
const gap=parseFloat(gcs.columnGap)||0;
const gb=grid.getBoundingClientRect();
const pad=parseFloat(gcs.paddingLeft)+parseFloat(gcs.paddingRight);
const last=rows[rk[rk.length-1]].slice().sort((a,b)=>a.x-b.x);
const used=last.reduce((s,b)=>s+b.w,0)+gap*(last.length-1);
// OVERFLOW PROBE: every text-bearing descendant of the lead tiles + strip
const ovf=[];
const scan=[...lead.querySelectorAll(':scope>.c-bento__grid>.kpi-tile *'),...document.querySelectorAll('.tpl-strip *')];
for(const e of scan){ if(e.scrollWidth>e.clientWidth+1 && e.clientWidth>0){ovf.push({el:e.tagName.toLowerCase()+'.'+[...e.classList].join('.'),sw:e.scrollWidth,cw:e.clientWidth,txt:(e.innerText||'').replace(/\s+/g,' ').slice(0,40)});} }
// clipping: any tile child whose rect exceeds its tile rect
const clip=[];
for(const t of tiles){const tb=t.getBoundingClientRect();for(const c of t.querySelectorAll('*')){const cb=c.getBoundingClientRect();if(cb.width===0)continue;if(cb.right>tb.right+0.6||cb.left<tb.left-0.6){clip.push({tile:t.getAttribute('aria-label'),el:c.tagName.toLowerCase()+'.'+[...c.classList].join('.'),over:+(cb.right-tb.right).toFixed(1),txt:(c.innerText||'').replace(/\s+/g,' ').slice(0,30)});}}}
const ctx=document.querySelector('.tpl-group-context');
const cards=[...ctx.querySelectorAll(':scope>.c-bento__grid>.c-bento__tile')];
const na=document.getElementById('dp08-na');
const txt=document.body.innerText;
const fsz=[...lead.querySelectorAll(':scope>.c-bento__grid>.kpi-tile .amt')].map(e=>getComputedStyle(e).fontSize);
return{colsNow:gcs.getPropertyValue('--bento-cols-now').trim(),cols:gcs.gridTemplateColumns,
 tiles:boxes,rows:rk.length,rowSizes:rk.map(k=>rows[k].length),
 maxWdiff:+(Math.max(...ws)-Math.min(...ws)).toFixed(2),gap:gap,lastRowVoid:+((gb.width-pad)-used).toFixed(1),
 ctxCols:getComputedStyle(ctx.querySelector(':scope>.c-bento__grid')).gridTemplateColumns,
 railCards:cards.map(c=>{const h=c.querySelector('h3');return{title:h?h.textContent.trim():'?',...r(c)}}),
 na:r(na),strip:r(document.querySelector('.tpl-strip')),
 chipHref:document.querySelector('[data-dp08-anchor]').getAttribute('href'),
 overflow:ovf,clipped:clip,amtFontSizes:fsz,
 repeats:{aw:(txt.match(/Awaiting approval/g)||[]).length,p14:(txt.match(/14 payments/g)||[]).length,n5:(txt.match(/5 need you/g)||[]).length,NofM:(txt.match(/\d+ of \d+ need you/g)||[]).length,und:(txt.match(/Undrawn facilities/g)||[]).length},
 panels:document.querySelectorAll('[role="tabpanel"]').length,
 page_h:document.documentElement.scrollHeight};}"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for w in (1440,1100,820):
        for th in ('light','dark'):
            k=f"{w}-{th}"; pg=b.new_page(viewport={'width':w,'height':900})
            seen=[]; pg.on("pageerror",lambda e:seen.append(str(e)))
            pg.on("console",lambda m:seen.append("console:"+m.text) if m.type=="error" else None)
            pg.goto(f"file://{PAGE}")
            if th=='dark': pg.evaluate("()=>{document.documentElement.setAttribute('data-theme','dark');document.body.setAttribute('data-theme','dark');}")
            pg.wait_for_timeout(500)
            d=pg.evaluate(PROBE); d['errors']=seen; res[k]=d
            pg.screenshot(path=f"{OUT}/full-{k}.png",full_page=False)
            # crop of the tile row + strip
            el=pg.query_selector('.tpl-group-lead')
            if el: el.screenshot(path=f"{OUT}/tiles-{k}.png")
            st=pg.query_selector('.tpl-strip')
            if st: st.screenshot(path=f"{OUT}/strip-{k}.png")
            print('==',k,'colsNow',d['colsNow'],'rows',d['rows'],d['rowSizes'],'maxWdiff',d['maxWdiff'],'lastRowVoid',d['lastRowVoid'],'gap',d['gap'],'err',len(seen))
            print('   tiles',[(t['label'],t['x'],t['w'],t['h']) for t in d['tiles']])
            print('   NA',d['na'],'strip',d['strip'],'ctxCols',d['ctxCols'])
            print('   rail',[(c['title'],c['y'],c['w'],c['h']) for c in d['railCards']])
            print('   OVERFLOW',len(d['overflow']),d['overflow'][:4])
            print('   CLIPPED',len(d['clipped']),d['clipped'][:4])
            print('   amtFont',d['amtFontSizes'],'page_h',d['page_h'],'repeats',d['repeats'],'panels',d['panels'])
            pg.close()
    b.close()
json.dump(res,open(f"{OUT}/vr.json","w"),indent=1,default=str)
