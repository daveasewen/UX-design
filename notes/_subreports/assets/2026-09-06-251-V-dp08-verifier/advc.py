from playwright.sync_api import sync_playwright
PAGE='/sessions/bold-focused-hopper/mnt/UX-design/knowledge/snippets/Template-dashboard-bento.reference.html'
J=r"""()=>{const lead=document.querySelector('.tpl-group-lead');const g=lead.querySelector(':scope>.c-bento__grid');
const t=[...lead.querySelectorAll(':scope>.c-bento__grid>.kpi-tile')].map(e=>{const b=e.getBoundingClientRect();return{l:e.getAttribute('aria-label'),x:+b.left.toFixed(1),y:+(b.top+scrollY).toFixed(1),w:+b.width.toFixed(1)}});
const rows={};t.forEach(b=>{const k=Math.round(b.y);(rows[k]=rows[k]||[]).push(b)});
const rk=Object.keys(rows).map(Number).sort((a,b)=>a-b);const cs=getComputedStyle(g);const gap=parseFloat(cs.columnGap)||0;
const gb=g.getBoundingClientRect();const pad=parseFloat(cs.paddingLeft)+parseFloat(cs.paddingRight);
const last=rows[rk[rk.length-1]];const used=last.reduce((s,b)=>s+b.w,0)+gap*(last.length-1);
return{rows:rk.length,rowSizes:rk.map(k=>rows[k].length),lastRowVoid:+((gb.width-pad)-used).toFixed(1),cols:cs.gridTemplateColumns};}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for w in (1440,1100,820):
        pg=b.new_page(viewport={'width':w,'height':900}); pg.goto(f"file://{PAGE}"); pg.wait_for_timeout(400)
        print('ADV-C',w,pg.evaluate(J)); pg.close()
    b.close()
