"""W4b: the v1013-r3 Trade page's ring is BISTABLE in the page itself — eight fresh loads (args: run, page) (reduced motion),
each reached by clicking the nav from the overview, each read at 100ms..3s. Prints [ring w, ring h, svg w]."""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = """() => { const out=[]; for (const f of document.querySelectorAll('figure.dv')) { const s=f.querySelector('svg.dv-svg'); if(!s) continue; const ty=f.getAttribute('data-dv-type')||f.className; if(!/donut|pie/.test(ty)) continue;
  let l=1e9,t=1e9,r=-1e9,b=-1e9; for (const p of s.querySelectorAll('path,circle')) { const q=p.getBoundingClientRect(); if(!q.width) continue; l=Math.min(l,q.left); t=Math.min(t,q.top); r=Math.max(r,q.right); b=Math.max(b,q.bottom);}
  out.push([Math.round(r-l), Math.round(b-t), s.getBoundingClientRect().width|0]); } return out; }"""
RUN = sys.argv[1] if len(sys.argv) > 1 else 'v1013-r3'
PAGE = sys.argv[2] if len(sys.argv) > 2 else 'trade.html'
with G.Harness() as h:
    for trial in range(8):
        ctx = h.b.new_context(viewport={'width':1440,'height':900}); pg = ctx.new_page(); pg.emulate_media(reduced_motion='reduce')
        pg.goto('file://'+os.path.expanduser('~/r4c/stage/cold-%s/out/index.html' % RUN)); pg.wait_for_timeout(900)
        pg.locator('a[href="%s"]' % PAGE).first.click(); pg.wait_for_load_state('load')
        seq=[]
        for t in (100, 400, 900, 1600, 3000):
            pg.wait_for_timeout(t - (seq[-1][0] if seq else 0)); seq.append((t, pg.evaluate(JS)))
        print("load", trial, seq)
        ctx.close()
