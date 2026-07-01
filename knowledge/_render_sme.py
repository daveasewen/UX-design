import os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
SRC="file://"+os.path.join(HERE,"_fitness-test","sme-payments.html")
OUT="/sessions/magical-practical-einstein/mnt/outputs"
SHOTS=[("sme-light.png",470,"light",False),("sme-dark.png",470,"dark",False),
       ("sme-confirm.png",470,"light",True),("sme-320.png",320,"light",False)]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    for fn,vw,th,modal in SHOTS:
        pg=b.new_page(viewport={"width":vw,"height":900},device_scale_factor=2)
        pg.goto(SRC); pg.evaluate(f"document.body.setAttribute('data-theme','{th}')")
        if modal: pg.evaluate("document.getElementById('overlay').classList.add('open')")
        pg.wait_for_timeout(150)
        ov=pg.evaluate("Math.max(0,document.documentElement.scrollWidth-document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT,fn),full_page=True); print(f"{fn:16} vw={vw} {th} modal={modal} h-overflow={ov}px")
    b.close()
