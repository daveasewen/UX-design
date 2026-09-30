"""#310 lane A — the dark tiles as BUILT (s310-D3/D4), rendered at the seat for Dave's eye.
before = HEAD before lane A (git archive into outputs/310/A/before/); after = the live tree.
option = the live tree with data-dark-tiles="grey" on every [data-theme] element.
  python3 render_310A.py demo            banking demo, Console + Supercharge, dark: before/after/option
  python3 render_310A.py snips I N       every Nth snippet from the I-th, Mono dark, before vs after;
                                         pairs that differ are kept, facts -> img/snips/_diff-I.json
"""
import os, sys, json, glob, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
ROOT = os.getcwd(); BEFORE = os.path.join(ROOT, "outputs/310/A/before"); OUT = "notes/_lanes/310/A/img"
SET = """([th,mode,opt])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode);
  document.querySelectorAll('[data-theme]').forEach(e=>{e.setAttribute('data-theme',mode);
    if(opt) e.setAttribute('data-dark-tiles',opt); else e.removeAttribute('data-dark-tiles');});}"""
FACTS = """()=>{const bg=e=>e?getComputedStyle(e).backgroundColor:null;
  const t=document.querySelector('.dashboard-tile');
  return {page:bg(document.body), ground:bg(document.querySelector('.c-bento.dashboard-bento')), tile:bg(t),
    text:getComputedStyle(document.querySelector('.metric-val')).color}}"""

def launch(p):
    return p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])

def demo():
    rel = "dashboards/international-banking-dashboard.canon.html"; facts = {}
    with sync_playwright() as p:
        b = launch(p); pg = b.new_page(viewport={"width": 1440, "height": 900})
        for th in ("console", "supercharge"):
            for state, base, opt in (("before", BEFORE, ""), ("after", ROOT, ""), ("option", ROOT, "grey")):
                pg.goto("file://" + os.path.join(base, rel)); pg.wait_for_timeout(500)
                pg.evaluate(SET, [th, "dark", opt]); pg.wait_for_timeout(900)
                facts[f"{th}-{state}"] = pg.evaluate(FACTS)
                top = pg.query_selector(".dashboard-bento-stack").bounding_box()
                pg.screenshot(path=f"{OUT}/demo-{th}-{state}.png",
                              clip={"x": 0, "y": top["y"] - 10, "width": 1440, "height": 560})
                print(th, state, facts[f"{th}-{state}"])
        b.close()
    json.dump(facts, open(f"{OUT}/demo-facts.json", "w"), indent=1)

def shot(pg, url):
    pg.goto(url); pg.wait_for_timeout(350)
    pg.evaluate(SET, ["", "dark", ""]); pg.wait_for_timeout(450)
    h = min(pg.evaluate("document.documentElement.scrollHeight"), 1600)
    return Image.open(io.BytesIO(pg.screenshot(clip={"x": 0, "y": 0, "width": 1280, "height": h}))).convert("RGB")

def snips(i, n):
    files = sorted(glob.glob("knowledge/snippets/*.reference.html"))[i - 1::n]; res = {}
    with sync_playwright() as p:
        b = launch(p); pg = b.new_page(viewport={"width": 1280, "height": 800})
        for f in files:
            slug = os.path.basename(f).replace(".reference.html", "")
            try:
                a = shot(pg, "file://" + os.path.join(BEFORE, f)); z = shot(pg, "file://" + os.path.join(ROOT, f))
            except Exception as e:
                res[slug] = {"error": str(e)[:200]}; continue
            if a.size != z.size:
                w, h = max(a.size[0], z.size[0]), max(a.size[1], z.size[1])
                a2 = Image.new("RGB", (w, h)); a2.paste(a); z2 = Image.new("RGB", (w, h)); z2.paste(z); a, z = a2, z2
            box = ImageChops.difference(a, z).getbbox()
            if box:
                diff = ImageChops.difference(a, z).convert("L").point(lambda v: 255 if v > 0 else 0)
                frac = sum(diff.histogram()[255:]) / (a.size[0] * a.size[1])
                a.save(f"{OUT}/snips/{slug}-before.png"); z.save(f"{OUT}/snips/{slug}-after.png")
                res[slug] = {"changed": True, "bbox": box, "frac": round(frac, 4)}
            else:
                res[slug] = {"changed": False}
        b.close()
    json.dump(res, open(f"{OUT}/snips/_diff-{i}.json", "w"), indent=1)
    print(i, n, len(files), "changed:", sum(1 for v in res.values() if v.get("changed")), "errors:", sum(1 for v in res.values() if "error" in v))

if __name__ == "__main__":
    demo() if sys.argv[1] == "demo" else snips(int(sys.argv[2]), int(sys.argv[3]))
