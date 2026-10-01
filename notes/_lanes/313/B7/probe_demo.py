import sys, json
from playwright.sync_api import sync_playwright
root = sys.argv[1]
url = "file://%s/dashboards/international-banking-dashboard.canon.html" % root
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for mode in ("light", "dark"):
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(url); pg.wait_for_timeout(400)
        pg.evaluate("m => document.body.dataset.theme = m", mode)
        pg.wait_for_timeout(200)
        r = pg.evaluate("""() => {
          const box = e => { if(!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
          const row = document.querySelector('.cn-filter-toolbar-bar .ftb > div');
          const kids = [...row.children].map(k => ({cls: k.className, box: box(k)}));
          const btns = ['#navSearchTrigger', '#accountTrigger'].map(s => { const e = document.querySelector(s); const sv = e.querySelector('svg');
             return {sel: s, btn: box(e), svg: box(sv), bg: getComputedStyle(e).backgroundColor, color: getComputedStyle(e).color}; });
          return {rowcls: row.className, kids, btns, docH: document.documentElement.scrollHeight};
        }""")
        out[mode] = r
        pg.screenshot(path="/tmp/claude-0/b7/demo-%s-%s.png" % (sys.argv[2], mode), clip={"x": 0, "y": 0, "width": 1440, "height": 420})
        pg.close()
    b.close()
print(json.dumps(out, indent=1))
