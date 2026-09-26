"""DOM geometry + computed spacing audit, every page, light and dark, at a width. No screenshots used as evidence."""
import os, sys, json
from playwright.sync_api import sync_playwright
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PAGES = ['index', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
JS = r'''() => {
 const R=e=>e.getBoundingClientRect(), px=v=>Math.round(parseFloat(v)*10)/10;
 const wall=document.querySelector('.tpl-wall'), groups=[...wall.querySelectorAll(':scope > .c-bento__grid > .tpl-group')];
 const out={groupGaps:[], innerGaps:[], tilePad:[], clipped:[], overlaps:[], offRail:[]};
 // wall gutters: vertical gap between groups whose rows differ; horizontal gap between side-by-side groups
 for(let i=0;i<groups.length;i++){ for(let j=i+1;j<groups.length;j++){ const a=R(groups[i]), b=R(groups[j]);
   if(Math.abs(a.top-b.top)<1 && b.left>a.right) out.groupGaps.push(['h',Math.round((b.left-a.right)*10)/10]);
   else if(b.top>=a.bottom-1 && b.left<a.right && b.right>a.left && j===i+1) out.groupGaps.push(['v',Math.round((b.top-a.bottom)*10)/10]);
   if(!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top)) out.overlaps.push([i,j]); } }
 groups.forEach(g=>{ const t=[...g.querySelectorAll(':scope > .c-bento__grid > .c-bento__tile')]; for(let i=0;i+1<t.length;i++){ const a=R(t[i]), b=R(t[i+1]);
   if(Math.abs(a.top-b.top)<1) out.innerGaps.push(Math.round((b.left-a.right)*10)/10); else out.innerGaps.push(Math.round((b.top-a.bottom)*10)/10); }
   t.forEach(x=>{ const cs=getComputedStyle(x); out.tilePad.push([x.classList.contains('kpi-tile')?'kpi':'card', px(cs.paddingTop), px(cs.paddingLeft)]); }); });
 // any text clipped by its own box (overflow hidden + content larger), or ink cut (descenders) on labels
 document.querySelectorAll('.sn-label, .t-cm-label, .t-cm-button, .t-cm-caption, .lbl, .ddval, .dv-title, h1, .amt, .t-cm-figure-5, .t-cm-figure-6').forEach(e=>{ const cs=getComputedStyle(e);
   if(e.offsetParent===null) return; if((cs.overflow.includes('hidden')||cs.overflowX==='hidden'||cs.textOverflow==='ellipsis') && (e.scrollWidth>e.clientWidth+1 || e.scrollHeight>e.clientHeight+1)) out.clipped.push((e.className||e.tagName).toString().slice(0,40)+':'+e.textContent.trim().slice(0,30)+':'+e.scrollWidth+'x'+e.scrollHeight+'>'+e.clientWidth+'x'+e.clientHeight); });
 const head=R(document.querySelector('.ceo-head')), h1=R(document.querySelector('h1')), wallR=R(wall), ftb=document.querySelector('#ftb');
 const ground=getComputedStyle(document.querySelector('.ceo-ground')).backgroundColor, card=document.querySelector('.stat-card, .kpi-tile');
 const shc=document.querySelector('.sh-content');
 return {groupGaps:[...new Set(out.groupGaps.map(x=>x.join(':')))], innerGaps:[...new Set(out.innerGaps)], tilePad:[...new Set(out.tilePad.map(x=>x.join(':')))], overlaps:out.overlaps, clipped:out.clipped.slice(0,8),
   align:{h1Left:Math.round(h1.left), wallLeft:Math.round(wallR.left), ftbLeft: ftb?Math.round(R(ftb).left):null, wallRight:Math.round(wallR.right), contentRight:Math.round(R(shc).right)},
   headPad:[px(getComputedStyle(document.querySelector('.ceo-head')).paddingTop),px(getComputedStyle(document.querySelector('.ceo-head')).paddingLeft)],
   groundTop: Math.round(R(document.querySelector('.ceo-ground')).top - R(document.querySelector('.ceo-head')).bottom), wallTopInGround: Math.round(wallR.top - R(document.querySelector('.ceo-ground')).top),
   colours:{ground, card: card?getComputedStyle(card).backgroundColor:null, head:getComputedStyle(document.querySelector('.sh-content')).backgroundColor, text:getComputedStyle(document.querySelector('h1')).color, body:getComputedStyle(document.body).backgroundColor, html:getComputedStyle(document.documentElement).backgroundColor},
   hscroll: shc.scrollWidth>shc.clientWidth, docHscroll: document.documentElement.scrollWidth>document.documentElement.clientWidth};
}'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_context(viewport={'width': W, 'height': 1000}).new_page()
    for theme in ('light', 'dark'):
        for name in PAGES:
            pg.goto('file://' + os.path.join(OUT, name + '.html'))
            if pg.evaluate('document.documentElement.dataset.theme') != theme:
                pg.click('[data-theme-btn="%s"]' % theme)
            pg.wait_for_timeout(350)
            print(theme, name, json.dumps(pg.evaluate(JS)))
    b.close()
