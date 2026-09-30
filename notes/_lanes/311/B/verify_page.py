"""#311 lane B — verify the review page in context: broken images, side scroll, Copy as text returns every call."""
import os
from playwright.sync_api import sync_playwright
R=os.getcwd(); U="file://"+R+"/notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w in (1440,390):
        pg=b.new_page(viewport={"width":w,"height":900}); pg.goto(U); pg.wait_for_timeout(1200)
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(800)
        r=pg.evaluate("""()=>({imgs:document.images.length,broken:[...document.images].filter(i=>!i.complete||i.naturalWidth==0).map(i=>i.src),
          side:document.documentElement.scrollWidth-document.documentElement.clientWidth,links_png:[...document.querySelectorAll('a')].filter(a=>/\\.png$/i.test(a.href)).length})""")
        print(w,r)
        if w==1440:
            pg.click('.call[data-id=icons] .chip[data-v="Yes, it stands"]'); pg.click('.call[data-id=scpage] .chip >> nth=1')
            pg.fill('.call[data-id=scpage] textarea','test comment'); pg.fill('.call[data-id=page] textarea','page note')
            print(pg.evaluate("window.__reviewText()"))
            pg.click('#clear') if False else None
            pg.screenshot(path="outputs/311/B/page-1440.png",full_page=False)
        else:
            pg.screenshot(path="outputs/311/B/page-390.png",full_page=False)
        pg.close()
    b.close()
