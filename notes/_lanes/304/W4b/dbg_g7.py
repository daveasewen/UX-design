"""W4b: G7 model dump — overlaps and the runs for a named string."""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = G.COLLECT_JS.replace("if (v) runs.push({id, p, l: v.l", "window.__RUNS=(window.__RUNS||[]); if (v) window.__RUNS.push({s, l: v.l, t: v.t, r: v.r, b: v.b, ink}); if (v) runs.push({id, p, l: v.l")
with G.Harness() as h:
    pg = h.b.new_page(viewport={'width':1440,'height':900}); pg.emulate_media(reduced_motion='reduce'); pg.goto('file://'+os.path.abspath(sys.argv[1])); pg.wait_for_timeout(1500)
    m = pg.evaluate(JS, G.collect_opts())
    print('overlaps', m['overlaps'][:5])
    print(pg.evaluate("() => (window.__RUNS||[]).filter(r => /Aug/.test(r.s)).slice(0,6)"))
    print(pg.evaluate("() => { const t=[...document.querySelectorAll('svg text')].find(x=>/30 Aug/.test(x.textContent)); const c=getComputedStyle(t); return [c.fontStyle,c.fontWeight,c.fontSize,c.fontFamily, c.textTransform] }"))
