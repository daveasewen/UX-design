"""Item 3 — the other eight wave-3 parts (and the transaction row for reference), each its own
reference snippet opened as a file, light and dark by the snippet's own body[data-theme] switch.
Full page at 960 wide; the page crops to the top of each (its default specimen) where it is long."""
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _lib import *
PARTS = ["Standing-order-mandate-row", "Limits-meter", "Range-slider", "Rating", "Transfer-list",
         "Split-button", "Fab", "Back-to-top", "Transaction-row"]
res = {}
with sync_playwright() as p:
    b = launch(p)
    for part in PARTS:
        for mode in ["light", "dark"]:
            pg = b.new_page(viewport={"width": 960, "height": 760}, device_scale_factor=2)
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(url(f"knowledge/snippets/{part}.reference.html")); fonts_ready(pg)
            pg.evaluate("m => document.body.setAttribute('data-theme', m)", mode); pg.wait_for_timeout(150)
            h = pg.evaluate("() => document.documentElement.scrollHeight")
            pg.screenshot(path=str(OUT / f"3-{part.lower()}-{mode}-full.png"), full_page=True)
            pg.screenshot(path=str(OUT / f"3-{part.lower()}-{mode}.png"))   # the first screen: the default specimen
            res[f"{part}-{mode}"] = {"height": h, "errors": errs}
            pg.close()
    # close-ups of two things the pictures show wrong, light only, 4x
    pg = b.new_page(viewport={"width": 960, "height": 760}, device_scale_factor=4)
    pg.goto(url("knowledge/snippets/Rating.reference.html")); fonts_ready(pg)
    pg.locator(".display[role=img]").first.screenshot(path=str(OUT / "3-rating-aggregate-4x.png"))
    pg.goto(url("knowledge/snippets/Transfer-list.reference.html")); fonts_ready(pg)
    ub = pg.evaluate("() => { const r=Array.from(document.querySelectorAll('.move-btn')).map(b=>b.getBoundingClientRect()); return [Math.min(...r.map(x=>x.left)), Math.min(...r.map(x=>x.top)), Math.max(...r.map(x=>x.right)), Math.max(...r.map(x=>x.bottom))]; }")
    pg.screenshot(path=str(OUT / "3-transfer-list-buttons-4x.png"), clip={"x": ub[0]-8, "y": ub[1]-8, "width": ub[2]-ub[0]+16, "height": ub[3]-ub[1]+16})
    res["transfer-list-move-labels"] = pg.evaluate("() => Array.from(document.querySelectorAll('.move-btn')).map(b => [b.id, b.querySelector('use').getAttribute('href'), b.querySelector('use').href ? 1:1, (document.querySelector(b.querySelector('use').getAttribute('href'))||{}).innerHTML ? document.querySelector(b.querySelector('use').getAttribute('href')).querySelectorAll('path').length : 0])")
    pg.goto(url("knowledge/snippets/Back-to-top.reference.html")); fonts_ready(pg)
    res["back-to-top-demo-font"] = pg.evaluate("() => { const el = Array.from(document.querySelectorAll('p,div')).find(e => e.textContent.trim().startsWith('Scroll this frame')); return el ? getComputedStyle(el).fontFamily : null; }")
    pg.close()
    b.close()
# trim each full-page picture to its content (the page's own ground colour taken from the corner)
from PIL import Image, ImageChops
for f in OUT.glob("3-*-full.png"):
    im = Image.open(f).convert("RGB"); bg = Image.new("RGB", im.size, im.getpixel((2, 2)))
    bb = ImageChops.difference(im, bg).getbbox()
    if bb:
        pad = 40; bb = (max(0, bb[0]-pad), max(0, bb[1]-pad), min(im.width, bb[2]+pad), min(im.height, bb[3]+pad))
        im.crop(bb).save(f.with_name(f.name.replace("-full", "-trim")))
# the mandate row's reference page is long: the page shows its first specimen (the default list) only
for m in ["light", "dark"]:
    im = Image.open(OUT / f"3-standing-order-mandate-row-{m}-trim.png"); im.crop((0, 0, im.width, 1580)).save(OUT / f"3-standing-order-mandate-row-{m}-top.png")
save_json("3-wave3-measures.json", res)
for k, v in res.items(): print(k, v)
