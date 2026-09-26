import os, sys
from playwright.sync_api import sync_playwright
R=os.getcwd()
jobs=[("knowledge/snippets/Template-dashboard-bento.reference.html",1440,4,"svg.spark-inline","ref-spark-1440.png"),
      ("notes/_lanes/288/P/composed-dashboard.html",1440,4,"p.kpi-lbl","288-kpilbl-1440.png"),
      ("knowledge/snippets/Template-dashboard-bento.reference.html",390,1,None,"ref-390.png")]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],headless=True,args=["--no-sandbox"])
    for f,w,dpr,sel,out in jobs:
        pg=b.new_page(viewport={"width":w,"height":900},device_scale_factor=dpr)
        pg.emulate_media(reduced_motion="reduce")
        pg.goto("file://"+os.path.join(R,f)); pg.wait_for_timeout(500)
        o="notes/_lanes/304/R4b/"+out
        if sel: pg.locator(sel).first.screenshot(path=o)
        else: pg.screenshot(path=o, full_page=True)
        print(o)
    b.close()
