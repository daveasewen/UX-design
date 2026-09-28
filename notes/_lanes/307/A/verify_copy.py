# #307 conductor: prove "Copy as text" (the artifact's handback path) carries all 78 after take-all.
import os, re
from playwright.sync_api import sync_playwright
P = "file://" + os.path.abspath("notes/_SITTING-307-reopened-78-2026-09-28-v1.html")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script("window.__copied=null;Object.defineProperty(navigator,'clipboard',{value:{writeText:t=>{window.__copied=t;return Promise.resolve()}}});")
    pg.goto(P); pg.click("#take-page"); pg.wait_for_timeout(300)
    btn = pg.get_by_role("button", name=re.compile("Copy as text"))
    btn.click(); pg.wait_for_timeout(300)
    t = pg.evaluate("window.__copied") or ""
    open("notes/_lanes/307/A/TEST-COPY-by-conductor.txt", "w").write(t)
    print("copied chars", len(t), "| entries W-ids", len(set(re.findall(r"\bW-[0-9a-z]+\b", t))),
          "| answered line:", pg.locator("#tl-done").inner_text() if pg.locator("#tl-done").count() else "?", "| errors", errs)
    b.close()
