"""c6fit.py <n> <label=page>... — #304 C6 verifier's own probe (independent of W5a's fitrate.py, same unfitted criterion).
Per load (fresh page, 1440x900, RM env = reduced|no-preference): after 1500 ms count non-ring svg.dv-fit whose viewBox width
differs from its box width by >2 px (unfitted); also count viewBox writes over the first 3000 ms (MutationObserver from
document start) and the writes that land AFTER 1500 ms (a loop or thrash would keep writing)."""
import os, sys
from playwright.sync_api import sync_playwright
INIT = """window.__vb=[];new MutationObserver(ms=>{for(const m of ms){if(m.attributeName==='viewBox'&&m.target.matches&&m.target.matches('svg.dv-fit'))window.__vb.push(performance.now())}}).observe(document,{subtree:true,attributes:true,attributeFilter:['viewBox']});"""
UNF = """() => [...document.querySelectorAll('svg.dv-fit')].filter(s => { const v = s.viewBox.baseVal; const w = s.getBoundingClientRect().width;
     return v && w && Math.abs(v.width - w) > 2 && !s.closest('[data-dv-type=donut],[data-dv-type=pie]'); }).length"""
n = int(sys.argv[1]); rm = os.environ.get("RM", "no-preference")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for arg in sys.argv[2:]:
        lab, f = arg.split("=", 1)
        bad = 0; det = []; writes = []; late = []
        for i in range(n):
            pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion=rm); pg.add_init_script(INIT)
            pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(1500)
            r = pg.evaluate(UNF); w15 = pg.evaluate("window.__vb.length")
            pg.wait_for_timeout(1500); w30 = pg.evaluate("window.__vb.length")
            bad += 1 if r else 0; det.append(r); writes.append(w30); late.append(w30 - w15); pg.close()
        print("%-10s RM=%-13s %d/%d loads unfitted %s | viewBox writes/load %s | writes after 1.5s %s" % (lab, rm, bad, n, det, writes, late))
    b.close()
