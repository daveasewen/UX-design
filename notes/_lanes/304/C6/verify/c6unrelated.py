"""c6unrelated.py <label=page>... — #304 C6: does the W6 transitionend re-fit fire on unrelated transitions, and does it settle?
After a 2 s settle (motion on), count viewBox writes caused by: (a) a 60 ms background transition on an element that holds
no chart (expect 0), (b) the same on a chart's own figure, an element that holds one (expect ONE pass = one write per canvas
per property-end, debounced), (c) a 60 ms width transition on the figure 100%->90% and back (expect a re-fit, then quiet),
(d) 20 pointer moves over the page (expect 0)."""
import os, sys
from playwright.sync_api import sync_playwright
INIT = """window.__vb=[];new MutationObserver(ms=>{for(const m of ms){if(m.attributeName==='viewBox')window.__vb.push(performance.now())}}).observe(document,{subtree:true,attributes:true,attributeFilter:['viewBox']});"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for arg in sys.argv[1:]:
        lab, f = arg.split("=", 1)
        pg = b.new_page(viewport={"width": 1440, "height": 900}); pg.add_init_script(INIT)
        pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(2000)
        ncv = pg.evaluate("document.querySelectorAll('svg.dv-fit').length")
        def delta(js, wait=600):
            a = pg.evaluate("window.__vb.length"); pg.evaluate(js); pg.wait_for_timeout(wait); return pg.evaluate("window.__vb.length") - a
        a = delta("""(()=>{const e=[...document.querySelectorAll('body *')].find(x=>!x.querySelector('svg.dv-fit')&&!x.closest('svg')&&x.offsetWidth>40);
             e.style.transition='background-color 60ms';void e.offsetWidth;e.style.backgroundColor='rgb(255,0,0)';})()""")
        bb = delta("""(()=>{const f=document.querySelector('svg.dv-fit').closest('figure')||document.querySelector('svg.dv-fit').parentElement;
             f.style.transition='background-color 60ms';void f.offsetWidth;f.style.backgroundColor='rgb(250,250,200)';})()""")
        c = delta("""(()=>{const f=document.querySelector('svg.dv-fit').closest('figure')||document.querySelector('svg.dv-fit').parentElement;
             window.__f=f;f.style.transition='width 60ms';f.style.width=f.getBoundingClientRect().width+'px';void f.offsetWidth;f.style.width=(f.getBoundingClientRect().width*0.9)+'px';})()""")
        unf = pg.evaluate("""(()=>{const s=window.__f.querySelector('svg.dv-fit');return Math.round(s.viewBox.baseVal.width)+' vs box '+Math.round(s.getBoundingClientRect().width)})()""")
        quiet = delta("0", 1500)
        d = pg.evaluate("window.__vb.length")
        for i in range(20): pg.mouse.move(100 + i * 60, 300 + (i % 5) * 80)
        pg.wait_for_timeout(600); d = pg.evaluate("window.__vb.length") - d
        print("%s canvases=%d | (a) non-holder bg transition: %d writes | (b) holder bg transition: %d writes | (c) holder width 90%%: %d writes, after: %s | quiet 1.5s after: %d | (d) 20 pointer moves: %d" % (lab, ncv, a, bb, c, unf, quiet, d))
        pg.close()
    b.close()
