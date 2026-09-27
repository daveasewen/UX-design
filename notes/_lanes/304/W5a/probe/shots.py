"""shots.py <out.png> <page> <needle> [theme] — W5a: screenshot (2x) the figure.dv whose text contains <needle>, at 1440,
normal motion, theme light|dark (data-theme on <html>, then one resize so the engine re-fits)."""
import os, sys
from playwright.sync_api import sync_playwright
out, page, needle = sys.argv[1:4]; theme = sys.argv[4] if len(sys.argv) > 4 else "light"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2); pg.goto("file://" + os.path.abspath(page)); pg.wait_for_timeout(1500)
    if theme == "dark":
        pg.evaluate("() => { document.documentElement.setAttribute('data-theme','dark'); window.dispatchEvent(new Event('resize')); }"); pg.wait_for_timeout(600)
    h = pg.evaluate_handle("""(n) => { for (const f of document.querySelectorAll('figure.dv, figure[data-dv-type]')) { if (f.offsetParent && f.textContent.includes(n)) return f; } return null; }""", needle)
    el = h.as_element()
    if not el: print("NOT FOUND", needle); sys.exit(1)
    el.scroll_into_view_if_needed(); pg.wait_for_timeout(300); el.screenshot(path=out); print("wrote", out)
    b.close()
