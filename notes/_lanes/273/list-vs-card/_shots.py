import os
from playwright.sync_api import sync_playwright
REPO=os.environ.get("RENDER_REPO", os.getcwd())
PAGE="file://"+os.path.join(REPO,"notes","_PROPOSAL-list-vs-card-2026-09-15-v1.html")
OUT=os.path.join(REPO,"notes","_lanes","273","list-vs-card")
shots=[("shot-1280-light.png",1280,1000,"light"),
       ("shot-1280-dark.png",1280,1000,"dark"),
       ("shot-400-light.png",400,900,"light")]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],args=["--no-sandbox","--font-render-hinting=none"])
    for name,w,h,scheme in shots:
        ctx=b.new_context(viewport={"width":w,"height":h},color_scheme=scheme,device_scale_factor=1)
        pg=ctx.new_page()
        errs=[]; pg.on("console",lambda m: errs.append(m.type+": "+m.text) if m.type=="error" else None)
        pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
        pg.goto(PAGE,wait_until="load"); pg.wait_for_timeout(500)
        ow=pg.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
        print(name,"scrollWidth",ow,"viewport",w,"HORIZONTAL OVERFLOW" if ow>w+1 else "no body overflow","| console errors:",errs or 0)
        pg.screenshot(path=os.path.join(OUT,name),full_page=True)
        ctx.close()
    b.close()
print("ok")
