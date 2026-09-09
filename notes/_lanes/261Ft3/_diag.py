import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1500,'height':1000})
    pg.goto("file://"+R+"/notes/_lanes/261-Ft-footer-review.html"); pg.wait_for_timeout(500)
    print(pg.evaluate("""()=>{const f=[...document.querySelectorAll('footer.ft')].find(x=>x.classList.contains('minimal'))||document.querySelector('footer.ft');
    const i=f.querySelector('.ft-inner'); const cs=getComputedStyle(i);
    return {cls:f.className, fh:f.getBoundingClientRect().height, ih:i.getBoundingClientRect().height, pad:[cs.paddingTop,cs.paddingBottom], mh:cs.minHeight, box:cs.boxSizing,
      kids:[...i.children].map(c=>[c.className.split(' ')[0], +c.getBoundingClientRect().height.toFixed(2)])};}"""))
    b.close()
