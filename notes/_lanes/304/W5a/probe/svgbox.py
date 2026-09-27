"""svgbox.py <page>... — W5a: every chart svg: box w x h, viewBox, data-pl/pr fit results, first label font px vs rendered height."""
import json, os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for f in sys.argv[1:]:
        pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(1800)
        print("==", f.split('/w5w/')[-1].split('/stage/')[-1])
        for r in pg.evaluate("""() => [...document.querySelectorAll('svg.dv-svg, svg.dv-fit')].map(s => { const r = s.getBoundingClientRect(); const t = s.querySelector('text');
           return [s.closest('[class*=cn-chart]') ? [...s.closest('[class*=cn-chart]').classList].find(c=>c.startsWith('cn-')) : '-', Math.round(r.width), Math.round(r.height), s.getAttribute('viewBox'),
             t ? Math.round(t.getBoundingClientRect().height*10)/10 : null, getComputedStyle(s).height, s.closest('figure') ? getComputedStyle(s.closest('figure')).display : '']; })"""):
            print("  ", r)
        pg.close()
    b.close()
