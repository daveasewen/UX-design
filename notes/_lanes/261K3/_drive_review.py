#!/usr/bin/env python3
"""#261 K3 — drive the review page: console errors, the Columns toggle, 4 themes x 2 modes."""
import json, os, pathlib
for e in ("/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu",):
    if os.path.isdir(e):
        os.environ["LD_LIBRARY_PATH"] = e + ":" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright
ARGS = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--force-color-profile=srgb"]
R = pathlib.Path("/sessions/zen-funny-hawking/mnt/UX-design")
P = R / "notes/_lanes/261-K-kpi-tile-review.html"
OUT = R / "notes/_lanes/261K3"
errs, res = [], {}
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS)
    pg = b.new_page(viewport={"width": 1500, "height": 1100})
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(P.as_uri()); pg.wait_for_timeout(1200)
    res["cols_default"] = pg.eval_on_selector_all(".pair > .col",
        "els => els.filter(e => getComputedStyle(e).display !== 'none').length")
    for t in ["mono", "legacy", "console", "supercharge"]:
        pg.click(f'#themeseg button[data-theme-name="{t}"]')
        for m in ["light", "dark"]:
            pg.click(f'#modeseg button[data-mode="{m}"]')
            pg.wait_for_timeout(350)
            res[f"{t}/{m}"] = pg.evaluate("""() => {
              const f = document.getElementById('fK3').contentDocument;
              const g = s => { const e = f.querySelector(s); return e ? getComputedStyle(e) : null; };
              const u = g('.kpi-delta.up .glyph'), d = g('.kpi-delta.down .glyph');
              const su = g('.spark-inline[data-trend=\"up\"] .dv-series');
              return {arrow_up: u && u.color, arrow_down: d && d.color, spark_up: su && su.stroke};
            }""")
            pg.screenshot(path=str(OUT / f"review-{t}-{m}.png"))
    pg.click('#showseg button[data-show="all"]'); pg.wait_for_timeout(500)
    res["cols_working"] = pg.eval_on_selector_all(".pair > .col",
        "els => els.filter(e => getComputedStyle(e).display !== 'none').length")
    pg.screenshot(path=str(OUT / "review-show-working.png"))
    b.close()
res["console_errors"] = errs
print(json.dumps(res, indent=1))
