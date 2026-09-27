import os, sys, json
from playwright.sync_api import sync_playwright
path, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
MEAS = r"""()=>{const t=document.querySelector('.kpi-tile'); const l=t.querySelector('.kpi-lbl'), v=t.querySelector('.kpi-val');
 l.textContent='Pending payments awaiting approval across all accounts and entities (long label to force the ellipsis)';
 const lr=l.getBoundingClientRect(), tr=t.getBoundingClientRect(); const cs=getComputedStyle(l);
 const rng=document.createRange(); rng.selectNodeContents(l); const ink=rng.getBoundingClientRect();
 return {lblBoxH:lr.height, ovx:cs.overflowX, ovy:cs.overflowY, to:cs.textOverflow, lbl_to_val:(v.offsetTop-l.offsetTop), truncated:l.scrollWidth>l.clientWidth,
   inkBelowBox:+(ink.bottom-lr.bottom).toFixed(2), tileH:tr.height, clip:{x:tr.left-8,y:tr.top-8+scrollY,width:Math.min(tr.width+16,700),height:tr.height+16}};}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for mode in ("light","dark"):
        pg = b.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=4)
        pg.goto("file://"+path); pg.wait_for_timeout(800)
        if mode=="dark": pg.evaluate("()=>{[...document.querySelectorAll('[data-theme]')].forEach(e=>e.setAttribute('data-theme','dark')); if(!document.querySelector('[data-theme]')) document.documentElement.setAttribute('data-theme','dark');}"); pg.wait_for_timeout(400)
        info = pg.evaluate(MEAS); pg.wait_for_timeout(200)
        pg.screenshot(path=f"{out}/kpi-ALT-clip-visible-{mode}-tile1-4x.png", clip=info.pop("clip"), full_page=True)
        print(mode, json.dumps(info))
        pg.close()
    b.close()
