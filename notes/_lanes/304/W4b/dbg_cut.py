"""W4b: find svg axis labels whose glyphs leave the visible area (the '00 £m' cut)."""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = r"""() => { const out=[];
 for (const t of document.querySelectorAll('svg text')) {
   const r=t.getBoundingClientRect(); if(!r.width) continue;
   // walk ancestors, find first clipping box
   let e=t.parentElement, clip=null;
   while(e && e!==document.documentElement){ const c=getComputedStyle(e); if(c.overflowX!=='visible'){ const q=e.getBoundingClientRect(); if(r.left<q.left-0.5||r.right>q.right+0.5){clip={tag:e.tagName+'.'+(e.getAttribute('class')||''),l:q.left,r:q.right,ox:c.overflowX}; break;} } e=e.parentElement; }
   if(clip) out.push({txt:t.textContent.slice(0,20), cls:t.getAttribute('class'), l:Math.round(r.left), r:Math.round(r.right), clip});
 }
 return out.slice(0,12); }"""
with G.Harness() as h:
    for page in sys.argv[1:]:
        pg = h.b.new_page(viewport={'width':1440,'height':900}); pg.goto('file://'+os.path.abspath(page)); pg.wait_for_timeout(1500)
        print('==', page[-40:]); [print(x) for x in pg.evaluate(JS)]; pg.close()
