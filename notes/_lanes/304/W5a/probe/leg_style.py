"""leg_style.py <page> — W5a: first legend button: its box, and each child's tag/class/box/font-size/line-height/display."""
import json, os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width": 1440, "height": 900}); pg.goto("file://" + os.path.abspath(sys.argv[1])); pg.wait_for_timeout(1200)
    print(json.dumps(pg.evaluate("""() => { const b = document.querySelector('button.dv-leg-item'); if (!b) return null; const f = e => { const c = getComputedStyle(e);
      return {tag: e.tagName, cls: e.getAttribute('class'), h: Math.round(e.getBoundingClientRect().height*10)/10, fs: c.fontSize, lh: c.lineHeight, disp: c.display, trim: c.textBoxTrim, pad: c.paddingTop + ' ' + c.paddingBottom, ff: c.fontFamily.slice(0,20)}; };
      return [f(b)].concat([...b.children].map(f)); }""")))
    b.close()
