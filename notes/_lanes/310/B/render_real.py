"""#310 lane B — the two real templates that carry the tab strip, reference snippets as they stand (Mono, their native form).
readings: built (as is) | container (--tabs-background: transparent, the strip takes whatever it sits on)."""
import os, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
R=os.getcwd(); OUT="notes/_lanes/310/B/img"
SET="""(mode)=>{document.documentElement.setAttribute('data-theme',mode);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));}"""
CONT=":root,[data-theme],[data-theme] *{--tabs-background:transparent!important}"
JOBS=[("Template-detail",0,560),("Page-header-lockup",0,420)]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":1440,"height":900})
    for slug,y,h in JOBS:
        for mode in sys.argv[1].split(","):
            ims=[]
            for rd in ("built","container"):
                pg.goto("file://"+R+f"/knowledge/snippets/{slug}.reference.html"); pg.wait_for_timeout(400)
                pg.evaluate(SET,mode)
                if rd=="container": pg.add_style_tag(content=CONT)
                pg.wait_for_timeout(700)
                info=pg.evaluate("""()=>{const t=document.querySelector('.tablist');const r=t.getBoundingClientRect();let e=t.parentElement,g=null;while(e){const c=getComputedStyle(e).backgroundColor;if(c!='rgba(0, 0, 0, 0)'){g=c;break}e=e.parentElement}
                   const pnl=document.querySelector('[role=tabpanel]:not([hidden])');let pe=pnl,pb=null;while(pe){const c=getComputedStyle(pe).backgroundColor;if(c!='rgba(0, 0, 0, 0)'){pb=c+' '+(pe.className||pe.tagName);break}pe=pe.parentElement}
                   return {y:r.top,strip:getComputedStyle(t).backgroundColor,sits_on:g,panel_on:pb,page:getComputedStyle(document.body).backgroundColor}}""")
                print(slug,mode,rd,info)
                top=max(0,info["y"]-h//2) if y==0 else y
                ims.append(Image.open(io.BytesIO(pg.screenshot(clip={"x":0,"y":top,"width":1440,"height":h}))))
            s=Image.new("RGB",(1440,h*2+12),(128,128,128)); s.paste(ims[0],(0,0)); s.paste(ims[1],(0,h+12)); s.save(f"{OUT}/03-real-{slug}-{mode}.png")
    b.close()
