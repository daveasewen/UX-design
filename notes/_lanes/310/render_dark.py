"""#310 — the dark ground and tile readings on the banking demo, rendered at the seat.
Readings are token overrides on every [data-theme="dark"] element, nothing else:
  today   — canon as it stands (ground = tiles)
  his     — ground stays the dark grey (--surface-subtle), tiles black (--surface-raised)
  reverse — ground black, tiles the dark grey
"""
import os, json
from playwright.sync_api import sync_playwright
root=os.getcwd(); out="notes/_lanes/310/img"
PAGE="file://"+root+"/dashboards/international-banking-dashboard.canon.html"
BLACK={"console":"#000000","supercharge":"#13110E"}
def readings(th):
    return {"today":"", "his":f"--surface-raised:{BLACK[th]} !important;", "reverse":f"--surface-subtle:{BLACK[th]} !important;"}
facts={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    pg=b.new_page(viewport={"width":1440,"height":900})
    for th in ["console","supercharge"]:
        for name,css in list(readings(th).items())+[("light","")]:
            mode="light" if name=="light" else "dark"
            if th=="supercharge" and name=="light": continue
            pg.goto(PAGE); pg.wait_for_timeout(600)
            pg.evaluate("""([th,mode,css])=>{document.documentElement.setAttribute('data-apollo-theme',th);
              document.documentElement.setAttribute('data-theme',mode);
              document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));
              if(css){const s=document.createElement('style');s.textContent='[data-theme="dark"]{'+css+'}';document.head.appendChild(s);}}""",[th,mode,css])
            pg.wait_for_timeout(900)
            f=pg.evaluate("""()=>{const bg=e=>getComputedStyle(e).backgroundColor;
              const t=document.querySelector('.dashboard-tile');const svg=document.querySelector('.dashboard-tile svg.dv, .dashboard-tile .dv svg');
              const lbl=document.querySelector('.metric-lbl');
              return {ground:bg(document.body), bento:bg(document.querySelector('.c-bento.dashboard-bento')), tile:bg(t),
                label:lbl?getComputedStyle(lbl).color:null, text:getComputedStyle(document.querySelector('.metric-val')).color}}""")
            facts[f"{th}-{name}"]=f; print(th,name,f)
            pg.screenshot(path=f"{out}/{th}-{name}.png", full_page=True)
            top=pg.query_selector('.dashboard-bento-stack').bounding_box()
            pg.screenshot(path=f"{out}/{th}-{name}-top.png", clip={"x":0,"y":top["y"]-10,"width":1440,"height":560})
    b.close()
json.dump(facts,open("notes/_lanes/310/img/facts.json","w"),indent=1)
