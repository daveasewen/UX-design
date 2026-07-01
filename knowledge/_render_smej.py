import os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
SRC="file://"+os.path.join(HERE,"_fitness-test","sme-journey.html")
OUT="/sessions/magical-practical-einstein/mnt/outputs"
SHOTS=[("smej-overview.png",470,"light","overview"),("smej-review.png",470,"light","review"),
       ("smej-done.png",470,"light","done"),("smej-overview-dark.png",470,"dark","overview"),("smej-320.png",320,"light","overview")]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    for fn,vw,th,scr in SHOTS:
        pg=b.new_page(viewport={"width":vw,"height":920},device_scale_factor=2)
        pg.goto(SRC); pg.evaluate(f"document.body.setAttribute('data-theme','{th}')")
        pg.evaluate(f"document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active',s.dataset.screen==='{scr}'))")
        pg.wait_for_timeout(140)
        ov=pg.evaluate("Math.max(0,document.documentElement.scrollWidth-document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT,fn),full_page=True); print(f"{fn:22} {th} {scr} ov={ov}px")
    b.close()
