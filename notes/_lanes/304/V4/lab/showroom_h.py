import os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for f in sys.argv[1:]:
        c = b.new_context(viewport={'width': 1440, 'height': 1000}); pg = c.new_page(); pg.goto('file://' + os.path.abspath(f)); pg.wait_for_timeout(2500)
        fr = [x for x in pg.frames if x != pg.main_frame]
        res = [x.evaluate("() => [...document.querySelectorAll('svg.dv-svg')].map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height), s.getAttribute('viewBox')]; })") for x in fr]
        print(f, res); c.close()
    b.close()
