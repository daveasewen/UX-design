"""legcrop.py <out.png> <page> [theme] — W5a: 4x crop of the first visible chart legend (ul.dv-leg) at 1440."""
import os, sys
from playwright.sync_api import sync_playwright
out, page = sys.argv[1:3]; theme = sys.argv[3] if len(sys.argv) > 3 else "light"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=4); pg.goto("file://" + os.path.abspath(page)); pg.wait_for_timeout(1500)
    if theme == "dark":
        pg.evaluate("() => document.documentElement.setAttribute('data-theme','dark')"); pg.wait_for_timeout(500)
    h = pg.evaluate_handle("() => [...document.querySelectorAll('ul.dv-leg')].find(u => u.offsetParent)")
    el = h.as_element(); el.scroll_into_view_if_needed(); pg.wait_for_timeout(300); el.screenshot(path=out); print("wrote", out)
    b.close()
