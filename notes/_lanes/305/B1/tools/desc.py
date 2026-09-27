"""desc.py — 4x crops of the Kpi-tile labels with descenders ('Card spend', 'Pending payments'), before/after, common light + dark."""
import os
from playwright.sync_api import sync_playwright
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for tag in ("before", "after"):
        for m in ("light", "dark"):
            c = br.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=4); pg = c.new_page()
            pg.goto("file://" + os.path.join(B, "fix", tag, "Kpi-tile.html")); pg.wait_for_timeout(800)
            pg.evaluate("m=>{document.documentElement.setAttribute('data-apollo-theme','common');document.documentElement.setAttribute('data-theme',m);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',m));}", m)
            pg.wait_for_timeout(400)
            bb = pg.evaluate("""()=>{const ls=[...document.querySelectorAll('.kpi-lbl')].filter(l=>/Card spend|Pending payments/.test(l.textContent)).slice(0,2);
              const r=ls.map(l=>l.closest('.kpi-tile').getBoundingClientRect()); const x=Math.min(...r.map(a=>a.left)), y=Math.min(...r.map(a=>a.top));
              const R=Math.max(...r.map(a=>a.right)); return {x:x, y:y+scrollY, width:Math.min(R-x,900), height:70};}""")
            pg.screenshot(path=os.path.join(B, "renders", tag, "kpi-labels-descender-common-%s-4x.png" % m), clip=bb, full_page=True); c.close()
    br.close()
print("ok")
