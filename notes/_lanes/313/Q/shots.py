"""Lane Q, #313: cloud renders (fallback fonts) of the five parts rebuilt by B123 and the dark-roundel snippets, for the review page."""
import sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = pathlib.Path(__file__).resolve().parent / "img"
SNIPS = ["Tree", "Calendar", "Transfer-list", "Rating", "Slider", "Chart-boxplot", "Confirmation", "Notifications", "List-items", "Avatar"]
def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name in SNIPS:
            f = ROOT / "knowledge/snippets" / f"{name}.reference.html"
            if not f.exists(): print("missing", f); continue
            for theme in ("light", "dark"):
                pg = b.new_page(viewport={"width": 900, "height": 700}, device_scale_factor=1)
                pg.goto(f.as_uri()); pg.wait_for_timeout(300)
                pg.evaluate("t=>{document.body.setAttribute('data-theme',t);document.documentElement.setAttribute('data-theme',t)}", theme)
                pg.wait_for_timeout(200)
                # clip to the drawn content: the union of every element's box, with a margin
                box = pg.evaluate("""()=>{let r=0,b=0;for(const el of document.body.querySelectorAll('*')){const c=el.getBoundingClientRect();if(c.width&&c.height){r=Math.max(r,c.right+scrollX);b=Math.max(b,c.bottom+scrollY);}}return [Math.min(900,r+24),b+24];}""")
                h = box[1]
                out = OUT / f"{name.lower()}-{theme}.png"
                pg.screenshot(path=str(out), full_page=True, clip={"x":0,"y":0,"width":box[0],"height":min(h,1400)})
                print(name, theme, h)
                pg.close()
        b.close()
if __name__ == "__main__": main()
