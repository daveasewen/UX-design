"""#310 lane A — the tile's rest/hover/pressed/active in dark, before and after, Mono and Supercharge."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image
R=os.getcwd(); OUT="notes/_lanes/310/A/img"; U="file://"+R+"/notes/_lanes/310/A/states.html"
BEFORE="../../../../outputs/310/A/before/knowledge/canon/canon.css"
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":1020,"height":140})
    for th,name in (("","Mono"),("supercharge","Supercharge")):
        for css,when in ((BEFORE,"before"),("","after")):
            q=f"?label={name}%20{when}"+(f"&css={css}" if css else "")
            pg.goto(U+q); pg.wait_for_timeout(300)
            pg.evaluate("t=>{if(t)document.documentElement.setAttribute('data-apollo-theme',t)}",th); pg.wait_for_timeout(300)
            pg.evaluate("()=>document.querySelectorAll('.sw').forEach(e=>{const m=getComputedStyle(e).backgroundColor.match(/\\d+/g).slice(0,3).map(n=>(+n).toString(16).padStart(2,'0')).join('').toUpperCase();e.querySelector('span').textContent='#'+m})")
            f=f"{OUT}/_st-{name}-{when}.png"; pg.screenshot(path=f,clip={"x":0,"y":0,"width":1020,"height":140}); ims.append(Image.open(f))
    b.close()
s=Image.new("RGB",(1020,140*len(ims)))
for i,im in enumerate(ims): s.paste(im,(0,140*i))
s.save(f"{OUT}/tile-states.png"); print("ok")
