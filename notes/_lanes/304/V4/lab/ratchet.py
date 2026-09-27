import os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for f in sys.argv[1:]:
        c = b.new_context(viewport={'width': 1440, 'height': 1000}); pg = c.new_page(); pg.goto('file://' + os.path.abspath(f)); pg.wait_for_timeout(1500)
        hs = [pg.evaluate("() => [...document.querySelectorAll('svg.dv-svg')].map(s => Math.round(s.getBoundingClientRect().height))")]
        for i in range(3):
            pg.evaluate("() => window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(500)
            hs.append(pg.evaluate("() => [...document.querySelectorAll('svg.dv-svg')].map(s => Math.round(s.getBoundingClientRect().height))"))
        c2 = b.new_context(viewport={'width': 1440, 'height': 1000}); pg2 = c2.new_page(); pg2.goto('file://' + os.path.abspath(f)); pg2.wait_for_timeout(1500)
        pg2.set_viewport_size({'width': 1200, 'height': 1000}); pg2.wait_for_timeout(600); pg2.set_viewport_size({'width': 1440, 'height': 1000}); pg2.wait_for_timeout(600)
        real = pg2.evaluate("() => [...document.querySelectorAll('svg.dv-svg')].map(s => Math.round(s.getBoundingClientRect().height))")
        print(os.path.basename(os.path.dirname(os.path.dirname(f))), os.path.basename(f), 'load+3 synthetic resizes:', hs, '| real viewport 1440->1200->1440:', real); c.close(); c2.close()
    b.close()
