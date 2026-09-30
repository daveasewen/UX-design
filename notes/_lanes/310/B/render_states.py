"""#310 lane B — Supercharge dark tile rest/hover/pressed/active, before and after s310-D5."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image
R=os.getcwd(); OUT="notes/_lanes/310/B/img"; U="file://"+R+"/notes/_lanes/310/B/states.html"
BEFORE="../../../../outputs/310/B/before/knowledge/canon/canon.css"
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":1020,"height":140})
    for css,when in ((BEFORE,"before (%2313110E)"),("","after (s310-D5, interim)")):
        q=f"?label=Supercharge%20dark%20{when}"+(f"&css={css}" if css else "")
        pg.goto(U+q); pg.wait_for_timeout(300)
        pg.evaluate("()=>document.documentElement.setAttribute('data-apollo-theme','supercharge')"); pg.wait_for_timeout(300)
        pg.evaluate("()=>document.querySelectorAll('.sw').forEach(e=>{const m=getComputedStyle(e).backgroundColor.match(/\\d+/g).slice(0,3).map(n=>(+n).toString(16).padStart(2,'0')).join('').toUpperCase();e.querySelector('span').textContent='#'+m})")
        f=f"{OUT}/_st-sc-{len(ims)}.png"; pg.screenshot(path=f,clip={"x":0,"y":0,"width":1020,"height":140}); ims.append(Image.open(f))
        print(when, pg.evaluate("()=>[...document.querySelectorAll('.sw span')].map(s=>s.textContent).join(' ')"))
    b.close()
s=Image.new("RGB",(1020,140*len(ims)))
for i,im in enumerate(ims): s.paste(im,(0,140*i))
s.save(f"{OUT}/01-sc-tile-states.png"); print("ok")
