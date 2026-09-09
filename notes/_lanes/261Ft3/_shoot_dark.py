import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':900},device_scale_factor=2)
    pg.goto("file://"+R+"/knowledge/snippets/Footer.reference.html"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme','dark'));}")
    pg.wait_for_timeout(300)
    pg.query_selector(".shell").screenshot(path="notes/_lanes/261-Ft3-footer-1920-dark.png")
    b.close(); print("ok")
