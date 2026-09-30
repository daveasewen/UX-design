"""#309 lane G - measure the Chart-line figure on receipt pages (the blank space look). Seat-run; args: html paths."""
import os, sys, json
from playwright.sync_api import sync_playwright
JS = """() => { const f = document.querySelector('figure.dv'); if (!f) return null;
  const walk = (e, d) => d > 3 ? [] : [...e.children].flatMap(c => { const b = c.getBoundingClientRect();
     return [{d, tag: c.tagName, cls: ((c.className && c.className.baseVal !== undefined) ? c.className.baseVal : c.className).toString().slice(0,50), h: Math.round(b.height), w: Math.round(b.width),
              ar: getComputedStyle(c).aspectRatio, hcss: getComputedStyle(c).height}].concat(b.height > 150 ? walk(c, d+1) : []); });
  const b = f.getBoundingClientRect(); return {figH: Math.round(b.height), figW: Math.round(b.width), kids: walk(f, 0)}; }"""
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for path in sys.argv[1:]:
        pg = br.new_page(viewport={"width": 1440, "height": 900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.goto("file://" + os.path.abspath(path)); pg.wait_for_timeout(600)
        r = pg.evaluate(JS); print("==", path, "errors", errs); print(json.dumps(r, indent=0)[:1800])
        pg.close()
    br.close()
