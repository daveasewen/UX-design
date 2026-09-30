"""#309 lane G - the looks: the banking demo's filter row and the receipt page (trend slot, stat row, blank space).
Run at the seat: export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh;
python3 notes/_lanes/309/G/look.py <label> <page-root>   (before = a `git archive b690a19b` extract)"""
import os, sys, json
from playwright.sync_api import sync_playwright
label, root = sys.argv[1], sys.argv[2]
out = os.path.join(os.environ.get("LOOK_OUT", "outputs/309/G"), label); os.makedirs(out, exist_ok=True)
FILTER_JS = """() => { const r = document.querySelector('.ftb-row'); if (!r) return null;
  const cs = getComputedStyle(r);
  return {rowDisplay: cs.display, rowWidth: Math.round(r.getBoundingClientRect().width),
    kids: [...r.children].map(k => { const b = k.getBoundingClientRect(); return {cls: k.className.split(' ')[0], x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width)}; })}; }"""
RECEIPT_JS = """() => { const q = s => document.querySelector(s);
  const box = e => { if (!e) return null; const b = e.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y + scrollY), w: Math.round(b.width), h: Math.round(b.height)}; };
  const tiles = [...document.querySelectorAll('.stat-card, .metric')];
  const secs = [...document.querySelectorAll('body > *, main > *, section, .c-bento__tile')].slice(0, 60).map(e => ({tag: e.tagName, cls: (e.className||'').toString().slice(0,60), ...box(e)}));
  return {docH: document.documentElement.scrollHeight, tiles: tiles.map(t => ({cls: t.className, ...box(t), parent: t.parentElement.className, sparks: t.querySelectorAll('svg').length})),
    sparks: [...document.querySelectorAll('.spark-inline, .metric-spark, [class*=spark]')].map(s => ({cls: (s.className.baseVal ?? s.className), ...box(s), trend: s.getAttribute('data-trend')})),
    secs}; }"""
pages = {"banking": ("dashboards/international-banking-dashboard.canon.html", FILTER_JS),
         "receipt": ("dashboards/international-banking-dashboard.regen-v2-receipt.html", RECEIPT_JS)}
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for name, (path, js) in pages.items():
        for mode in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto("file://" + os.path.abspath(os.path.join(root, path))); pg.wait_for_timeout(500)
            pg.evaluate("m => document.querySelectorAll('[data-theme]').forEach(e => e.setAttribute('data-theme', m))", mode)
            pg.wait_for_timeout(250)
            res[f"{name}-{mode}"] = pg.evaluate(js)
            pg.screenshot(path=os.path.join(out, f"{name}-{mode}.png"), full_page=True)
            pg.close()
    b.close()
json.dump(res, open(os.path.join(out, "look.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k.startswith("banking-light")}, indent=0)[:1500])
