"""Item 4 — the eight form parts wave-3 lane alpha was sent to build and found already built.
Each reference snippet opened as a file, light, first screen at 960 x 640, 1x — thumbnails that prove
the part exists, not specimens for ruling. Also measures File-upload's aria-invalid (alpha's question 4)."""
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _lib import *
PARTS = ["Form-layout", "Date-picker", "Date-range-picker", "Time-picker", "Amount-input",
         "File-upload", "Secure-entry", "Textarea"]
res = {}
with sync_playwright() as p:
    b = launch(p)
    for part in PARTS:
        pg = b.new_page(viewport={"width": 960, "height": 640}, device_scale_factor=1)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url(f"knowledge/snippets/{part}.reference.html")); fonts_ready(pg); pg.wait_for_timeout(150)
        pg.screenshot(path=str(OUT / f"4-{part.lower()}.png"))
        res[part] = {"errors": errs, "aria_invalid_attrs": pg.evaluate("() => document.querySelectorAll('[aria-invalid]').length")}
        pg.close()
    b.close()
save_json("4-formparts-measures.json", res)
for k, v in res.items(): print(k, v)
