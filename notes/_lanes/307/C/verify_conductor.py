# #307 conductor: the picture page after the cold-run slot was filled — images, console, copy-as-text, 390 overflow.
import os, re
from playwright.sync_api import sync_playwright
P = "file://" + os.path.abspath("notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w in (1440, 390):
        pg = b.new_page(viewport={"width": w, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.add_init_script("window.__c=null;Object.defineProperty(navigator,'clipboard',{value:{writeText:t=>{window.__c=t;return Promise.resolve()}}});")
        pg.goto(P); pg.wait_for_load_state("networkidle")
        broken = pg.evaluate("[...document.images].filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src'))")
        n = pg.evaluate("document.images.length")
        over = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        calls = pg.evaluate("document.querySelectorAll('.dd-call').length")
        if w == 1440:
            pg.get_by_role("button", name=re.compile("Copy as text")).click(); pg.wait_for_timeout(300)
            t = pg.evaluate("window.__c") or ""
            print("copy: chars", len(t), "| mentions c6/fresh-session:", ("fresh-session" in t) or ("Make the three fixes" in t))
            pg.locator("#item-6").screenshot(path="notes/_lanes/307/C/check-item6-1440.png")
        print(w, "images", n, "broken", broken, "| calls", calls, "| h-overflow px", over, "| errors", errs[:3])
    b.close()
