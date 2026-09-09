#!/usr/bin/env python3
"""#261 K3 — drive the showroom kpi-tile page across 4 themes x 2 modes.

Reads the delta-arrow and spark-stroke colours off the DOM in each pane and shoots the first
board. goto file:// only. Lane fragment, not a gate.
"""
import json, os, pathlib

for extra in ("/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu",
              "/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/x86_64-linux-gnu"):
    if os.path.isdir(extra):
        os.environ["LD_LIBRARY_PATH"] = extra + ":" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright

ARGS = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--force-color-profile=srgb"]
ROOT = pathlib.Path("/sessions/zen-funny-hawking/mnt/UX-design")
PAGE = ROOT / "showroom/kpi-tile.html"
OUT = ROOT / "notes/_lanes/261K3"

READ = """() => {
  const g = (s) => { const e = document.querySelector(s); return e ? getComputedStyle(e) : null; };
  const up = g('.kpi-delta.up .glyph'), dn = g('.kpi-delta.down .glyph');
  const su = g('.spark-inline[data-trend="up"] .dv-series'),
        sd = g('.spark-inline[data-trend="down"] .dv-series');
  return {arrow_up: up && up.color, arrow_down: dn && dn.color,
          spark_up: su && su.stroke, spark_down: sd && sd.stroke};
}"""

res = {}
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS)
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.goto(PAGE.as_uri())
    pg.wait_for_timeout(300)
    for theme in ["mono", "legacy", "console", "supercharge"]:
        for mode in ["light", "dark"]:
            pg.evaluate("""([t,m]) => {
              const r = document.documentElement;
              if (t === 'mono') r.removeAttribute('data-apollo-theme');
              else r.setAttribute('data-apollo-theme', t);
              r.setAttribute('data-theme', m);
              document.body.setAttribute('data-theme', m);
              for (const f of document.querySelectorAll('iframe')) {
                try {
                  const d = f.contentDocument;
                  if (t === 'mono') d.documentElement.removeAttribute('data-apollo-theme');
                  else d.documentElement.setAttribute('data-apollo-theme', t);
                  d.body.setAttribute('data-theme', m);
                } catch (e) {}
              }
            }""", [theme, mode])
            pg.wait_for_timeout(120)
            fr = pg.frames[-1] if len(pg.frames) > 1 else pg.main_frame
            res[f"{theme}/{mode}"] = fr.evaluate(READ)
            el = fr.query_selector(".board")
            if el:
                el.screenshot(path=str(OUT / f"pane-{theme}-{mode}.png"))
    b.close()
print(json.dumps(res, indent=1))
