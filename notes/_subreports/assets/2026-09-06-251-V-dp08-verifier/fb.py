from playwright.sync_api import sync_playwright
PAGE='/sessions/bold-focused-hopper/mnt/UX-design/knowledge/snippets/Template-dashboard-bento.reference.html'
SIG=r"""()=>{
const names=['--success','--warning','--error','--info','--up','--down','--spark-up','--spark-down','--success-tint','--warning-tint','--error-tint','--info-tint'];
const pr=document.createElement('span');document.body.appendChild(pr);const rag={};
for(const n of names){pr.style.color=`var(${n})`;const v=getComputedStyle(pr).color;if(v&&v!=='rgba(0, 0, 0, 0)')rag[v]=n;}
pr.remove();const isRag=v=>v&&rag[v]!==undefined;const sig=[];
for(const e of document.querySelectorAll('.tpl-page *, .tpl-header *, .sh-masthead *')){
 const b=e.getBoundingClientRect();if(!b.width||!b.height)continue;const top=b.top+scrollY;if(top>=900)continue;
 const s=getComputedStyle(e);const h=[];
 if(isRag(s.backgroundColor))h.push('bg');
 if(isRag(s.color)&&e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))h.push('color');
 if(e instanceof SVGElement){if(isRag(s.fill)&&s.fill!=='none')h.push('fill');if(isRag(s.stroke)&&s.stroke!=='none')h.push('stroke');}
 if(h.length){const c=e.closest('.status, .kpi-tile')||e;sig.push((c.getAttribute('aria-label')||c.innerText||'').replace(/\s+/g,' ').slice(0,44));}}
return {elements:sig.length,carriers:[...new Set(sig)]};}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for w in (1440,1100,820):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f"file://{PAGE}");pg.wait_for_timeout(400)
        d=pg.evaluate(SIG);print('DP20',w,d['elements'],'/',len(d['carriers']),d['carriers']);pg.close()
    # FALLBACK: JS disabled — does the plain anchor still jump?
    c=b.new_context(viewport={'width':1440,'height':900},java_script_enabled=False)
    pg=c.new_page();pg.goto(f"file://{PAGE}");pg.wait_for_timeout(300)
    pg.click('[data-dp08-anchor]');pg.wait_for_timeout(500)
    c2=b.new_context(viewport={'width':1440,'height':900})
    p2=c2.new_page();p2.goto(f"file://{PAGE}#dp08-na");p2.wait_for_timeout(600)
    print('HASH-NAV(js on) scrollY',p2.evaluate("Math.round(scrollY)"),'active',p2.evaluate("document.activeElement.id||document.activeElement.tagName"))
    b.close()
