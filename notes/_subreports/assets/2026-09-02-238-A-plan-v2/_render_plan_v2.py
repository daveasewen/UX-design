#!/usr/bin/env python3
"""_render_plan_v2.py — #238 lane A render receipt for `_PLAN-designers-brain-2026-09-02-v2.html`.

Modelled on knowledge/_render/render.py (s191-D2, the canonical shape) but WITHOUT its HSBC-face
assertion — this page declares "Helvetica Neue" and ships no font. Font evidence is a CANVAS PROBE
(three measured widths), never document.fonts.check (the runbook says it lies).

Per render: emulate the colour scheme, set the viewport, load via file:// (never set_content),
measure scrollWidth vs clientWidth on <html> (the overflow probe), shoot the full page, and shoot
legible crops of named sections. Everything is appended to render-receipt.json beside the PNGs.

Usage (env staged per the runbook's seventh stratum, SAME bash call):
  python3 _render_plan_v2.py <theme:light|dark> <width> [<crop-section-id> ...]
"""
import datetime as _dt
import glob
import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PAGE = os.path.join(REPO, "_PLAN-designers-brain-2026-09-02-v2.html")
RECEIPT = os.path.join(HERE, "render-receipt.json")


def main(theme, width, crops):
    height = 1400 if width >= 1000 else 844
    shell = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))
    if not shell:
        print("REFUSED: no headless_shell under ~/.cache/ms-playwright")
        return 2
    out = {"theme": theme, "width": width, "at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
           "seat": os.environ.get("PWD", "") or os.getcwd(), "page": os.path.relpath(PAGE, REPO), "files": []}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0], headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        ctx = b.new_context(viewport={"width": width, "height": height}, color_scheme=theme, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto("file://" + PAGE)
        pg.wait_for_timeout(800)
        probe = pg.evaluate("""() => {
          const d = document.documentElement;
          const c = document.createElement('canvas').getContext('2d');
          const w = f => { c.font = '16px ' + f; return Math.round(c.measureText('The designer\\u2019s brain — programme plan v2').width*10)/10; };
          return {scrollWidth: d.scrollWidth, clientWidth: d.clientWidth, scrollHeight: d.scrollHeight,
                  bodyBg: getComputedStyle(document.body).backgroundColor,
                  accent: getComputedStyle(document.querySelector('.label')).color,
                  canvas: {helveticaNeue: w('"Helvetica Neue"'), sansSerif: w('sans-serif'), serif: w('serif'), monospace: w('monospace')}};
        }""")
        out["probe"] = probe
        out["overflow"] = "NONE" if probe["scrollWidth"] <= probe["clientWidth"] else f"OVERFLOW {probe['scrollWidth']} > {probe['clientWidth']}"
        full = os.path.join(HERE, f"plan-v2-{theme}-{width}.png")
        pg.screenshot(path=full, full_page=True)
        out["files"].append(os.path.basename(full))
        for sec in crops:
            r = pg.evaluate("""(id) => { const e = document.getElementById(id); const r = e.getBoundingClientRect();
                                 return {x: 0, y: Math.round(r.top + window.scrollY), h: Math.round(r.height)}; }""", sec)
            h = min(r["h"], 2600)
            path = os.path.join(HERE, f"crop-{theme}-{width}-{sec}.png")
            pg.screenshot(path=path, full_page=True, clip={"x": 0, "y": r["y"], "width": width, "height": h})
            out["files"].append(os.path.basename(path))
        b.close()
    rec = json.load(open(RECEIPT)) if os.path.exists(RECEIPT) else {"$description": "#238 lane A render receipt — one entry per (theme, width) render; overflow is scrollWidth vs clientWidth on <html>; canvas widths are the font probe (never fonts.check).", "renders": []}
    rec["renders"] = [r for r in rec["renders"] if not (r["theme"] == theme and r["width"] == width)] + [out]
    json.dump(rec, open(RECEIPT, "w"), indent=1)
    print(json.dumps(out, indent=1))
    return 0 if out["overflow"] == "NONE" else 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], int(sys.argv[2]), sys.argv[3:]))
