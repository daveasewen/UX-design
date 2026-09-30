"""#310 lane B — the tab strip in four contexts (tabs-context.html), two readings:
built = as the tree renders it; container = tabs/background transparent (the strip takes what it sits on)."""
import os, sys, json
from playwright.sync_api import sync_playwright
R=os.getcwd(); OUT="notes/_lanes/310/B/img"; U="file://"+R+"/notes/_lanes/310/B/tabs-context.html"
SET="""([th,mode])=>{const r=document.documentElement;r.setAttribute('data-apollo-theme',th);r.setAttribute('data-theme',mode);
  document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));}"""
CONT=".cn-tabs,.cn-page-header-lockup,.cn-template-detail{--tabs-background:transparent!important}"
MEAS="""()=>[...document.querySelectorAll('.ctx')].map(c=>{const l=c.querySelector('.tablist');let e=l.parentElement,g=null;
  while(e){const b=getComputedStyle(e).backgroundColor;if(b!='rgba(0, 0, 0, 0)'){g=b;break}e=e.parentElement}
  return c.querySelector('.cap').textContent.slice(0,3)+' strip '+getComputedStyle(l).backgroundColor+' on '+g})"""
facts={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":1440,"height":900})
    for th,mode in (("console","light"),("console","dark"),("supercharge","dark")):
        for rd in ("built","container"):
            pg.goto(U); pg.wait_for_timeout(400); pg.evaluate(SET,[th,mode])
            if rd=="container": pg.add_style_tag(content=CONT)
            pg.wait_for_timeout(700); pg.evaluate("place()")
            k=f"{th}-{mode}-{rd}"; facts[k]=pg.evaluate(MEAS); print(k,facts[k])
            h=pg.evaluate("document.querySelector('.grid').getBoundingClientRect().height")
            pg.screenshot(path=f"{OUT}/03-ctx-{k}.png",clip={"x":0,"y":0,"width":1440,"height":h})
    b.close()
json.dump(facts,open(f"{OUT}/tabs-facts.json","w"),indent=1)
