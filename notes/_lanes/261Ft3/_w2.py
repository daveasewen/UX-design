import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w in (375,768,1024,1280,1440,1600,1920):
        pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto("file://"+R+"/knowledge/snippets/Footer.reference.html"); pg.wait_for_timeout(350)
        r=pg.evaluate("()=>[...document.querySelectorAll('footer.ft')].map(f=>f.getBoundingClientRect().height)")
        print(w, [round(x,2) for x in r], "grid:", all(abs(x/4-round(x/4))<0.01 for x in r))
        pg.close()
    b.close()
