"""#309 lane D - capture the pages that move from the stat card to Metric, at 1440, light and dark.
Run at the seat in ONE call: export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh;
source knowledge/_render/seat_env.sh; python3 notes/_lanes/309/D/capture.py <before|after>
Writes outputs/309/D/<phase>/<page>-<mode>-{ctx,crop}.png and, for the banking demo, the stat row in
all four themes x two modes (<page>-<theme>-<mode>-crop.png). Every style is the page's own + canon."""
import os, sys, json
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
phase = sys.argv[1]
PAGE_ROOT = sys.argv[2] if len(sys.argv) > 2 else ROOT   # before: a `git archive b690a19b` extract in /tmp
OUT = os.path.join(ROOT, "outputs", "309", "D", phase)
os.makedirs(OUT, exist_ok=True)
PAGES = {
  # name: (path, context js -> element or null for full page, crop js -> element)
  "banking-demo": ("dashboards/international-banking-dashboard.canon.html", None,
                   "document.querySelector('.dashboard-stats-bento')"),
  "progress-dashboard": ("dashboard/index.html",
                   "document.querySelector('.cn-stat-card, .cn-metric').closest('section')",
                   "document.querySelector('.cn-stat-card .board, .cn-metric .board')"),
  "receipt-page": ("dashboards/international-banking-dashboard.regen-v2-receipt.html", None,
                   "document.querySelector('.stat-card, .metric')"),
}
MODE_JS = "m => { document.querySelectorAll('[data-theme]').forEach(e => e.setAttribute('data-theme', m)); }"
THEME_JS = "t => document.documentElement.setAttribute('data-apollo-theme', t)"
ARROWS_JS = """() => [...document.querySelectorAll('.delta.up .arrow, .delta.down .arrow, .metric-delta.up .glyph, .metric-delta.down .glyph, .metric-delta.flat .glyph')]
  .map(e => ({dir: e.parentElement.className, ink: getComputedStyle(e).color, op: getComputedStyle(e).opacity,
              bg: (function(n){ while(n){ const c=getComputedStyle(n).backgroundColor; if(c && c!=='rgba(0, 0, 0, 0)') return c; n=n.parentElement;} return 'none'; })(e)}))"""
log = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for name, (path, ctx, crop) in PAGES.items():
        for mode in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            pg.goto("file://" + os.path.join(PAGE_ROOT, path)); pg.wait_for_timeout(400)
            pg.evaluate(MODE_JS, mode); pg.wait_for_timeout(250)
            if ctx is None:
                pg.screenshot(path=os.path.join(OUT, f"{name}-{mode}-ctx.png"), full_page=True)
            else:
                pg.evaluate_handle(ctx).as_element().screenshot(path=os.path.join(OUT, f"{name}-{mode}-ctx.png"))
            log[f"{name}-{mode}"] = pg.evaluate(ARROWS_JS)
            pg.close()
            pz = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=4)
            pz.goto("file://" + os.path.join(PAGE_ROOT, path)); pz.wait_for_timeout(400)
            themes = ["mono", "common", "console", "supercharge"] if name == "banking-demo" else [None]
            for t in themes:
                if t: pz.evaluate(THEME_JS, t)
                pz.evaluate(MODE_JS, mode); pz.wait_for_timeout(250)
                tag = f"{name}-{t}-{mode}" if t else f"{name}-{mode}"
                pz.evaluate_handle(crop).as_element().screenshot(path=os.path.join(OUT, f"{tag}-crop.png"))
                if t: log[tag] = pz.evaluate(ARROWS_JS)
                # the arrows themselves, cropped in: each delta row that carries a direction
                rows = pz.query_selector_all('.delta.up, .delta.down, .metric-delta.up, .metric-delta.down')
                for i, r in enumerate(rows):
                    r.scroll_into_view_if_needed()
                    g = r.query_selector('.arrow, .glyph').bounding_box()
                    pz.screenshot(path=os.path.join(OUT, f"{tag}-arrow{i}.png"),
                                  clip={"x": g["x"] - 8, "y": g["y"] - 8, "width": 104, "height": g["height"] + 16})
            pz.close()
    b.close()
json.dump(log, open(os.path.join(OUT, "arrows.json"), "w"), indent=1)
for k, v in log.items(): print(k, [(a["dir"], a["ink"], a["op"], a["bg"]) for a in v])
