import os, json
from playwright.sync_api import sync_playwright
R=os.path.expanduser("~/mnt/Projects--UX-design"); OUT=R+"/notes/_lanes/308/D/"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for th,mode in (("mono","light"),("supercharge","dark")):
        pg=b.new_page(viewport={"width":1280,"height":900})
        fails=[]; errs=[]
        pg.on("requestfailed", lambda r: fails.append(r.url)); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://"+R+"/showroom/_foundations/logos.html#theme=%s&mode=%s"%(th,mode)); pg.wait_for_timeout(1200)
        pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.body.setAttribute('data-theme',m)}",[th,mode])
        pg.wait_for_timeout(300)
        info=pg.evaluate("()=>({tiles:document.querySelectorAll('#bento .lg-tile').length, broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length, warn:document.body.innerText.includes('missing from disk'), ds045:document.body.innerText.includes('ds-045'), sw:document.documentElement.scrollWidth})")
        pg.screenshot(path=OUT+"D2-logos-%s-%s.png"%(th,mode), full_page=True)
        print(th,mode,info,fails,errs)
    b.close()
