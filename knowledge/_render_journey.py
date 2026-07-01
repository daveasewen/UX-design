import os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
SRC="file://"+os.path.join(HERE,"_fitness-test","payments-journey.html")
OUT="/sessions/magical-practical-einstein/mnt/outputs"
SHOTS=[("jr-dash-light.png",460,"light","dashboard"),("jr-dash-dark.png",460,"dark","dashboard"),
       ("jr-pay-light.png",460,"light","pay"),("jr-review-light.png",460,"light","review"),
       ("jr-review-dark.png",460,"dark","review"),("jr-done-light.png",460,"light","done"),
       ("jr-dash-320.png",320,"light","dashboard")]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox"])
    for fn,vw,th,scr in SHOTS:
        pg=b.new_page(viewport={"width":vw,"height":820},device_scale_factor=2)
        pg.goto(SRC); pg.evaluate(f"document.body.setAttribute('data-theme','{th}')")
        pg.evaluate(f"document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active', s.dataset.screen==='{scr}'))")
        pg.wait_for_timeout(150)
        ov=pg.evaluate("Math.max(0,document.documentElement.scrollWidth-document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT,fn),full_page=True); print(f"{fn:20} vw={vw} {th} {scr} h-overflow={ov}px")
    b.close()
