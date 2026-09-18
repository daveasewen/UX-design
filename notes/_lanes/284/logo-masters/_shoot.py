import sys, json
from playwright.sync_api import sync_playwright
ROOT="/sessions/dazzling-dreamy-darwin/mnt/UX-design"
LANE=ROOT+"/notes/_lanes/284/logo-masters"
url="file://"+LANE+"/MASTERS-2026-09-18.html"
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(channel=None, args=["--no-sandbox","--disable-gpu"])
    pg=b.new_page(viewport={"width":1280,"height":1000}, device_scale_factor=1)
    pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: "+str(e)))
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(400)
    # 1:1 panel: each lockup's first rack
    for n in ["hexagon-light-colour","hexagon-light-mono","hexagon-dark-colour","hexagon-dark-mono",
              "masterbrand-light-colour","masterbrand-light-mono","masterbrand-dark-colour","masterbrand-dark-mono"]:
        pg.locator(f"#{n} .rack").first.screenshot(path=f"{LANE}/shots/1x-{n}.png")
    pg.screenshot(path=f"{LANE}/shots/page-1280-light.png", full_page=False)
    # 4x crop of masterbrand-light-colour-24 (first zoom cell of that lockup)
    pg.locator("#masterbrand-light-colour .zrack .zc").first.screenshot(path=f"{LANE}/shots/4x-masterbrand-light-colour-24.png")
    pg.locator("#masterbrand-light-colour .zrack").screenshot(path=f"{LANE}/shots/4x-masterbrand-light-colour-all.png")
    print("console errors:", len(errs), errs[:5])
    b.close()
