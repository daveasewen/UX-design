"""W3a before/after shots. Usage: shots.py PAGE OUTPREFIX [--wait ms]
Writes OUTPREFIX-{light,dark}-1440.png (viewport shot, 1440x1000, full page capped 2400px) and
OUTPREFIX-{light,dark}-kpilbl-4x.png (4x crop of the first three .kpi-lbl) and -donut-4x.png
(4x crop of the first donut centre text, if any). Dark = every [data-theme] set to dark (or <html>)."""
import os, sys, json
from playwright.sync_api import sync_playwright
page_path = os.path.abspath(sys.argv[1]); pre = sys.argv[2]
wait = int(sys.argv[sys.argv.index("--wait")+1]) if "--wait" in sys.argv else 900
DARK = """()=>{const els=[...document.querySelectorAll('[data-theme]')]; if(!els.length) document.documentElement.setAttribute('data-theme','dark'); els.forEach(e=>e.setAttribute('data-theme','dark'));}"""
INFO = """()=>{const o={};
 const l=[...document.querySelectorAll('.kpi-lbl')].slice(0,3).map(e=>e.getBoundingClientRect());
 if(l.length){const x0=Math.min(...l.map(r=>r.left))-6,y0=Math.min(...l.map(r=>r.top))-8,x1=Math.max(...l.map(r=>r.right))+6,y1=Math.max(...l.map(r=>r.bottom))+8;
  o.lbl={x:Math.max(0,x0),y:Math.max(0,y0+scrollY),width:Math.min(x1-x0,1400),height:y1-y0};}
 const d=[...document.querySelectorAll('svg text')].filter(t=>/total|^[0-9.,£$€ kKmM%-]+$/i.test(t.textContent.trim())&&t.closest('[class*=donut],[data-chart*=donut],[data-type*=donut],figure'));
 const texts=[...document.querySelectorAll('[class*=donut] text, [class*=donut] .dv-centre, [class*=donut] [class*=centre], [class*=donut] [class*=center]')];
 o.donutTexts=texts.slice(0,6).map(t=>t.textContent.trim().slice(0,40));
 const t0=texts.find(t=>/\\d/.test(t.textContent));
 if(t0){const r=(t0.closest('svg')||t0).getBoundingClientRect(); o.donut={x:r.left,y:r.top+scrollY,width:Math.min(r.width,600),height:Math.min(r.height,600)};}
 return o;}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for mode in ("light", "dark"):
        for dsf in (1, 4):
            pg = b.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=dsf)
            pg.goto("file://" + page_path); pg.wait_for_timeout(wait)
            pg.add_style_tag(content=".sh{height:auto!important;max-height:none!important;overflow:visible!important}"); pg.wait_for_timeout(300)
            if mode == "dark": pg.evaluate(DARK); pg.wait_for_timeout(wait)
            info = pg.evaluate(INFO)
            if dsf == 1:
                h = min(pg.evaluate("document.documentElement.scrollHeight"), 2400)
                pg.screenshot(path=f"{pre}-{mode}-1440.png", clip={"x":0,"y":0,"width":1440,"height":h}, full_page=True)
                print(mode, json.dumps(info))
            else:
                for key, nm in (("lbl","kpilbl"),("donut","donut")):
                    if info.get(key):
                        try: pg.screenshot(path=f"{pre}-{mode}-{nm}-4x.png", clip=info[key], full_page=True)
                        except Exception as e: print("crop skipped", key, str(e)[:80])
            pg.close()
    b.close()
