"""fitrate.py <n> <page>... — W5a: load each page n times in fresh pages; count loads where any chart svg's viewBox width
differs from its box width by >2px (the fit did not land: the svg is scaled)."""
import os, sys
from playwright.sync_api import sync_playwright
n = int(sys.argv[1])
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for f in sys.argv[2:]:
        bad = 0; det = []
        for i in range(n):
            pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion=os.environ.get("RM", "no-preference")); pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(1500)
            r = pg.evaluate("""() => [...document.querySelectorAll('svg.dv-fit')].filter(s => { const v = s.viewBox.baseVal; const w = s.getBoundingClientRect().width;
                 return v && w && Math.abs(v.width - w) > 2 && !s.closest('[data-dv-type=donut],[data-dv-type=pie]'); }).length""")
            bad += 1 if r else 0; det.append(r); pg.close()
        print("%-60s %d/%d loads unfitted %s" % (f.split('/w5w/')[-1].split('/stage/')[-1], bad, n, det))
    b.close()
