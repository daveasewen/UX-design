"""W4b: walk one svg label's ancestors as G7/G8 do."""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = r"""(pat) => { const t=[...document.querySelectorAll('svg text')].find(x=>new RegExp(pat).test(x.textContent));
 const out=[]; const r=t.getBoundingClientRect(); out.push(['self',r.left,r.top,r.right,r.bottom]);
 let e=t; while(e && e!==document.documentElement){ const c=getComputedStyle(e); const q=e.getBoundingClientRect();
   out.push([e.tagName+'.'+(e.getAttribute('class')||'').slice(0,25), 'ox='+c.overflowX,'oy='+c.overflowY,'clip='+c.clip,'cp='+c.clipPath,'pos='+c.position,'op='+c.opacity, [q.left|0,q.top|0,q.right|0,q.bottom|0]]); e=e.parentElement; }
 return out; }"""
with G.Harness() as h:
    pg = h.b.new_page(viewport={'width':1440,'height':900}); pg.emulate_media(reduced_motion='reduce'); pg.goto('file://'+os.path.abspath(sys.argv[1])); pg.wait_for_timeout(1500)
    for x in pg.evaluate(JS, sys.argv[2]): print(x)
