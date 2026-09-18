#!/usr/bin/env python3
"""Drive headless Chromium over the #285 contact sheet and the masters (lane scratch).

goto("file://…") only — never set_content(), which loses relative resolution and
gives the page a different layout box than the file it is standing in for.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
MAST = os.path.join(ROOT, "knowledge", "assets", "logos", "masters")
SHOTS = os.path.join(HERE, "shots")
SHEET = "file://" + os.path.join(HERE, "MASTERS-2026-09-18.html")

CROP = """<!DOCTYPE html><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}
.box{width:%dpx;height:%dpx;overflow:hidden;font-size:0;line-height:0}
.in{transform:scale(%d);transform-origin:top left;font-size:0;line-height:0;
    margin-left:-%dpx;margin-top:-%dpx}</style>
<div class="box"><div class="in">%s</div></div>"""


def crop_page(svg, scale, ox, oy, w, h):
    return CROP % (w, h, scale, ox * scale, oy * scale, svg)


def main():
    os.makedirs(SHOTS, exist_ok=True)
    errs = []
    import tempfile
    tmp = tempfile.mkdtemp(prefix="shoot285-")  # scratch OUTSIDE the repo
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--no-sandbox", "--force-device-scale-factor=1"])
        pg = b.new_page(viewport={"width": 1280, "height": 1400})
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))

        pg.goto(SHEET, wait_until="load")
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(SHOTS, "sheet-full-1280.png"), full_page=True)
        pg.locator("#ba").screenshot(path=os.path.join(SHOTS, "before-after-4x.png"))
        for n in ("masterbrand-light-colour", "masterbrand-dark-colour",
                  "hexagon-light-colour", "masterbrand-light-mono"):
            pg.locator("#" + n).screenshot(path=os.path.join(SHOTS, "panel-" + n + ".png"))
        # the 1:1 rack of every lockup, in one shot
        pg.locator("#masterbrand-light-colour .rack").first.screenshot(
            path=os.path.join(SHOTS, "panel-1x-mb-light-colour.png"))

        # --- 4x crops of the B, per size, cut out of the master itself
        # B sits between the H and the S; window it off the wordmark's left edge.
        # B ink runs measured off the rendered bitmap: 24 x71-78, 32 x94-104, 40 x118-131
        boxes = {24: (69, 5, 13, 15), 32: (92, 7, 16, 19), 40: (116, 9, 19, 23)}
        for h, (ox, oy, w, hh) in boxes.items():
            for tag, d in (("after", MAST), ("before", os.path.join(HERE, "before"))):
                src = os.path.join(d, "masterbrand-light-colour-%d.svg" % h)
                if not os.path.exists(src):
                    continue
                svg = open(src).read()
                f = os.path.join(tmp, "crop-%s-%d.html" % (tag, h))
                open(f, "w").write(crop_page(svg, 8, ox, oy, w * 8, hh * 8))
                pg.set_viewport_size({"width": w * 8 + 20, "height": hh * 8 + 20})
                pg.goto("file://" + f, wait_until="load")
                pg.locator(".box").screenshot(
                    path=os.path.join(SHOTS, "8x-B-%s-%d.png" % (tag, h)))
            # side-by-side whole wordmark at 4x
        for h in (24, 32, 40):
            a = open(os.path.join(MAST, "masterbrand-light-colour-%d.svg" % h)).read()
            bsrc = os.path.join(HERE, "before", "masterbrand-light-colour-%d.svg" % h)
            bb = open(bsrc).read() if os.path.exists(bsrc) else ""
            W = 89 if h == 24 else (119 if h == 32 else 148)
            page = ("<!DOCTYPE html><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
                    "div.r{display:block;width:%dpx;height:%dpx;overflow:hidden;font-size:0;line-height:0}"
                    "div.i{transform:scale(4);transform-origin:top left;font-size:0;line-height:0}"
                    "p{font:500 11px/1.9 Helvetica,Arial,sans-serif;letter-spacing:.14em;margin:6px 0 2px;"
                    "text-transform:uppercase}</style>"
                    "<p>before &mdash; #284</p><div class='r'><div class='i'>%s</div></div>"
                    "<p>after &mdash; #285</p><div class='r'><div class='i'>%s</div></div>"
                    % (W * 4, h * 4, bb, a))
            f = os.path.join(tmp, "ba-%d.html" % h)
            open(f, "w").write(page)
            pg.set_viewport_size({"width": W * 4 + 20, "height": h * 8 + 90})
            pg.goto("file://" + f, wait_until="load")
            pg.screenshot(path=os.path.join(SHOTS, "4x-ba-%d.png" % h))
        b.close()
    print(json.dumps({"console_errors": errs, "n": len(errs)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
