import os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
SRC="file://"+os.path.join(HERE,"_fitness-test","notifications-responsive.html")
OUT="/sessions/magical-practical-einstein/mnt/outputs"
SHOTS=[("notif-wide-light.png",900,"light",False),("notif-wide-dark.png",900,"dark",False),
       ("notif-320-light.png",320,"light",False),("notif-320-dark.png",320,"dark",False)]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    for fn,vw,th,narrow in SHOTS:
        pg=b.new_page(viewport={"width":vw,"height":900},device_scale_factor=2)
        pg.goto(SRC); pg.evaluate(f"document.body.setAttribute('data-theme','{th}')")
        pg.wait_for_timeout(180)
        ov=pg.evaluate("Math.max(0,document.documentElement.scrollWidth-document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT,fn),full_page=True); print(f"{fn:20} vw={vw} {th} h-overflow={ov}px")
    b.close()
