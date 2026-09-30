import os
from playwright.sync_api import sync_playwright
root=os.getcwd(); P="file://"+root+"/notes/_REVIEW-310-the-dark-ground-2026-09-30-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w in [1440,390]:
        pg=b.new_page(viewport={"width":w,"height":900})
        pg.goto(P); pg.wait_for_timeout(800)
        broken=pg.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth==0).map(i=>i.src)")
        sw=pg.evaluate("document.documentElement.scrollWidth")
        print(w,"images",pg.evaluate("document.images.length"),"broken",broken,"scrollWidth",sw)
        if w==1440:
            pg.click('.call[data-id=ground] .chip >> nth=0'); pg.fill('.call[data-id=ground] textarea','test note')
            print(pg.evaluate("window.__reviewText()"))
            print(pg.inner_text('#count'))
        pg.screenshot(path=f"outputs/310/review-{w}.png",full_page=True)
        pg.close()
    b.close()
