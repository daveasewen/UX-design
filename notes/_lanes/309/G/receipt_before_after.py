"""#309 lane G - the receipt page before (HEAD 7e58f84a, lane D's regen) and after lane G's spec fix, light and dark,
full page at 1440, composed side by side. Seat-run: python3 notes/_lanes/309/G/receipt_before_after.py <before.html> <after.html>"""
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
bef, aft = sys.argv[1], sys.argv[2]
out = "notes/_lanes/309/G/receipt-before-after.png"
shots = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for lab, path in (("before", bef), ("after", aft)):
        for mode in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto("file://" + os.path.abspath(path)); pg.wait_for_timeout(500)
            pg.evaluate("m => document.querySelectorAll('[data-theme]').forEach(e => e.setAttribute('data-theme', m))", mode)
            pg.wait_for_timeout(250)
            m = pg.evaluate("() => { const t = document.querySelector('.metric').getBoundingClientRect(); return {docH: document.documentElement.scrollHeight, tileH: Math.round(t.height), tileW: Math.round(t.width), spark: !!document.querySelector('.metric .metric-spark')}; }")
            print(lab, mode, m)
            f = f"/dev/shm/r-{lab}-{mode}.png"; pg.screenshot(path=f, full_page=True); shots[(lab, mode)] = f; pg.close()
    b.close()
ims = {k: Image.open(v) for k, v in shots.items()}
W = 1440; H = max(i.size[1] for i in ims.values()); pad = 48
canvas = Image.new("RGB", (2 * W + pad, 2 * (H + pad) + pad), "white"); d = ImageDraw.Draw(canvas)
for r, mode in enumerate(("light", "dark")):
    for c, lab in enumerate(("before", "after")):
        x, y = c * (W + pad), pad + r * (H + pad)
        d.text((x + 8, y - 36), f"{lab} · {mode}" + ("  (HEAD 7e58f84a: Metric's first tile, trend slot filled)" if lab == "before" else "  (lane G: Metric's compact tile, no trend slot)"), fill="black")
        canvas.paste(ims[(lab, mode)], (x, y))
canvas.save(out); print("wrote", out, canvas.size)
