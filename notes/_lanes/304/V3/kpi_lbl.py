import os, sys
from playwright.sync_api import sync_playwright
pairs = [a.split("=",1) for a in sys.argv[1:-1]]; out = os.path.abspath(sys.argv[-1])
JS = """()=>{const ls=[...document.querySelectorAll('.kpi-lbl')].slice(1,3).map(e=>e.getBoundingClientRect());
 const x0=Math.min(...ls.map(r=>r.left))-6,y0=Math.min(...ls.map(r=>r.top))-10,x1=Math.max(...ls.map(r=>r.right))+6,y1=Math.max(...ls.map(r=>r.bottom))+10;
 return {x:x0,y:y0+scrollY,width:x1-x0,height:y1-y0};}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for tag, path in pairs:
        for mode in ("light","dark"):
            pg = b.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=4)
            pg.goto("file://"+os.path.abspath(path)); pg.wait_for_timeout(800)
            if mode=="dark": pg.evaluate("()=>{[...document.querySelectorAll('[data-theme]')].forEach(e=>e.setAttribute('data-theme','dark')); if(!document.querySelector('[data-theme]')) document.documentElement.setAttribute('data-theme','dark');}"); pg.wait_for_timeout(400)
            pg.screenshot(path=f"{out}/kpi-{tag}-{mode}-labels-descender-4x.png", clip=pg.evaluate(JS), full_page=True); pg.close()
    b.close()
print("ok")
