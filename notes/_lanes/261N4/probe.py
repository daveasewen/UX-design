import os, sys, pathlib, json
os.environ["LD_LIBRARY_PATH"] = "/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright
f = "/sessions/zen-funny-hawking/mnt/UX-design/knowledge/snippets/Sidebar-nav.reference.html"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1280,"height":900})
    pg.goto("file://" + f)
    print(json.dumps(pg.evaluate("""()=>[...document.querySelectorAll('.sn-product')].map(el=>{
      const cs=getComputedStyle(el);const r=el.getBoundingClientRect();
      return {h:el.clientHeight, rh:r.height, trim:cs.textBoxTrim, edge:cs.textBoxEdge, lh:cs.lineHeight,
              fs:cs.fontSize, ancestor:el.parentElement.className, gp:el.parentElement.parentElement.className};
    })"""), indent=1))
    b.close()
