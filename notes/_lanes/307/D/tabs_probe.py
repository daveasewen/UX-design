import os, json, sys
from playwright.sync_api import sync_playwright
here=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg=b.new_page(viewport={"width":1440,"height":600})
    pg.goto("file://"+os.path.join(here,"tabs_probe.html"))
    r=pg.evaluate("""()=>{const h=document.getElementById('host').getBoundingClientRect().width;
      const t=document.getElementById('t').getBoundingClientRect().width;
      const pn=document.getElementById('p').getBoundingClientRect().width;
      return {host:h, tabs:t, panel:pn, tabsW:getComputedStyle(document.getElementById('t')).getPropertyValue('--tabs-w')}}""")
    pg.screenshot(path=os.path.join(here,"tabs_probe-1440.png"))
    print(json.dumps(r)); b.close()
