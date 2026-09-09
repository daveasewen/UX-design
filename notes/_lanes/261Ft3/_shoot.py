import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w in (1440,1920,375):
        pg=b.new_page(viewport={'width':w,'height':900},device_scale_factor=2)
        pg.goto("file://"+R+"/knowledge/snippets/Footer.reference.html"); pg.wait_for_timeout(500)
        el=pg.query_selector("footer.ft")
        # shoot the shell containing the default footer, so the plate reads against the page
        sh=pg.query_selector(".shell")
        sh.screenshot(path=f"notes/_lanes/261-Ft2-footer-{w}.png")
        print(w,"shot", round(el.bounding_box()['height'],2))
        pg.close()
    b.close()
