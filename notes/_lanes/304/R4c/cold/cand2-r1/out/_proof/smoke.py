import os, json, sys
from playwright.sync_api import sync_playwright
W = os.path.expanduser("~/cold/cand2-r1"); OUT = W + "/out"
pages = sys.argv[1:] or ["index", "accounts", "liquidity", "payments", "fx", "risk", "trade", "reports", "messages", "settings"]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    for name in pages:
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m, errs=errs: errs.append("console." + m.type + ": " + m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e, errs=errs: errs.append("pageerror: " + str(e)))
        pg.goto("file://%s/%s.html" % (OUT, name)); pg.wait_for_timeout(700)
        info = pg.evaluate("""() => {
          const figs = [...document.querySelectorAll('figure.dv')].map(f => ({id: f.id, marks: f.querySelectorAll('svg.dv-svg *').length, rows: f.querySelectorAll('.dv-table tbody tr').length}));
          const kpis = [...document.querySelectorAll('.kpi-tile')].map(k => k.getAttribute('aria-label'));
          const grid = document.getElementById('tbody') ? document.querySelectorAll('#tbody tr[data-id]').length : null;
          const lists = [...document.querySelectorAll('ul.list')].map(u => u.id + ':' + u.children.length);
          return {figs, kpis, grid, lists, title: document.title};
        }""")
        info["errors"] = errs
        res[name] = info
        pg.close()
    b.close()
print(json.dumps(res, indent=1))
