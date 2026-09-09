import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w in (1440,1920):
        pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto("file://"+R+"/knowledge/snippets/Footer.reference.html"); pg.wait_for_timeout(400)
        print(w, pg.evaluate("""()=>{const f=document.querySelector('footer.ft');const i=f.querySelector('.ft-inner');
        const kids=[...i.children].map(c=>[c.className.split(' ')[0], Math.round(c.getBoundingClientRect().width)]);
        return {inner:Math.round(i.getBoundingClientRect().width), h:i.getBoundingClientRect().height, kids};}"""))
        pg.close()
    b.close()
