import os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
SRC="file://"+os.path.join(HERE,"_fitness-test","tags-responsive.html")
OUT="/sessions/magical-practical-einstein/mnt/outputs"
SHOTS=[("tags-wide-light.png",900,"light",False),("tags-wide-dark.png",900,"dark",False),
       ("tags-narrow-light.png",900,"light",True),("tags-320-dark.png",320,"dark",False)]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    for fn,vw,th,narrow in SHOTS:
        pg=b.new_page(viewport={"width":vw,"height":700},device_scale_factor=2)
        pg.goto(SRC); pg.evaluate(f"document.body.setAttribute('data-theme','{th}')")
        if narrow: pg.evaluate("document.getElementById('filterbar').style.setProperty('--demo-width','320px')")
        pg.wait_for_timeout(180)
        ov=pg.evaluate("Math.max(0,document.documentElement.scrollWidth-document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT,fn),full_page=True); print(f"{fn:22} vw={vw} {th} narrow={narrow} h-overflow={ov}px")
    b.close()
