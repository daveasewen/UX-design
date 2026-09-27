"""figshots.py <out-prefix> <file> [navtext] — element shots of every figure.dv, light and dark, dsf 2."""
import os, sys
from playwright.sync_api import sync_playwright
OUT, FILE = sys.argv[1], sys.argv[2]; NAV = sys.argv[3] if len(sys.argv) > 3 else None
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for theme in ('light', 'dark'):
        c = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2, reduced_motion='reduce'); pg = c.new_page()
        pg.goto('file://' + os.path.abspath(FILE)); pg.wait_for_timeout(1200)
        if NAV:
            pg.locator('nav a, nav button, .sn a, aside a, [role=navigation] a, [role=navigation] button').filter(has_text=NAV).first.click(); pg.wait_for_timeout(1500)
        pg.evaluate("t => { document.documentElement.setAttribute('data-theme', t); }", theme); pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(2000)
        figs = pg.locator('figure.dv'); n = 0
        for i in range(figs.count()):
            f = figs.nth(i)
            if not f.is_visible(): continue
            f.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
            f.screenshot(path='%s-%s-fig%02d.png' % (OUT, theme, i), timeout=8000); n += 1
        print(theme, 'figs', n); c.close()
    b.close()
