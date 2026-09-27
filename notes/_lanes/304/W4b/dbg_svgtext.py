"""W4b: does Range.getClientRects see SVG text? (the G7/G8 svg blind spot)"""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = r"""() => { const out=[]; let n=0;
 for (const t of document.querySelectorAll('svg text.dv-label, svg text.dv-axis')) { if(n++>3) break;
   const tn=[...t.childNodes].find(c=>c.nodeType===3); if(!tn) {out.push('no text node'); continue;}
   const rg=document.createRange(); rg.selectNodeContents(tn); const rs=[...rg.getClientRects()];
   const cs=getComputedStyle(t); let e=t, op=[]; while(e&&e.nodeType===1){ op.push(e.tagName+':'+getComputedStyle(e).opacity); e=e.parentElement; if(op.length>6)break;}
   out.push({txt:tn.nodeValue, rects:rs.map(r=>[r.left|0,r.top|0,r.width|0,r.height|0]), bb:(r=>[r.left|0,r.top|0,r.width|0,r.height|0])(t.getBoundingClientRect()), vis: t.checkVisibility? t.checkVisibility({contentVisibilityAuto:true,opacityProperty:true,visibilityProperty:true}):null, op:op.join(' ')});
 } return out; }"""
with G.Harness() as h:
    for page in sys.argv[1:]:
        pg = h.b.new_page(viewport={'width':1440,'height':900}); pg.emulate_media(reduced_motion='reduce'); pg.goto('file://'+os.path.abspath(page)); pg.wait_for_timeout(1500)
        print('==', page[-40:]); [print(x) for x in pg.evaluate(JS)]; pg.close()
