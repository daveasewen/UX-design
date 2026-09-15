import pathlib, json
from playwright.sync_api import sync_playwright
ROOT="/sessions/confident-clever-ritchie/mnt/UX-design"
OUT=ROOT+"/notes/_lanes/272/cut"
PAGE=pathlib.Path(OUT,"_REVIEW-cut-rulings-2026-09-15.html").as_uri()
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in ((1280,1000),(400,900)):
        for scheme in ("light","dark"):
            pg=b.new_page(viewport={"width":w,"height":h},color_scheme=scheme)
            errs=[]; pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
            pg.goto(PAGE); pg.wait_for_timeout(500)
            over=pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
            res[f"{w}-{scheme}"]={"scrollW":over[0],"innerW":over[1],
                                  "overflow":over[0]>over[1],"console_errors":errs}
            pg.screenshot(path=f"{OUT}/shot-{w}-{scheme}.png", full_page=True)
            pg.close()
    b.close()
print(json.dumps(res,indent=1))
