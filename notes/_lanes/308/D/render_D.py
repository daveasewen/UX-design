import os, json
from playwright.sync_api import sync_playwright
R=os.path.expanduser("~/mnt/Projects--UX-design"); S=os.path.expanduser("~/scratch308D/root")
OUT=R+"/notes/_lanes/308/D/"
SRC={"committed":R+"/showroom/_foundations/","regen":S+"/showroom/_foundations/"}
log={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    # A. logos
    for k,base in SRC.items():
        pg=b.new_page(viewport={"width":1280,"height":900})
        broken=[]
        pg.on("requestfailed", lambda r, broken=broken: broken.append(r.url.split("/")[-1]))
        pg.goto("file://"+base+"logos.html"); pg.wait_for_timeout(1200)
        pg.locator("#bento").screenshot(path=OUT+"D-logos-%s.png"%k)
        info=pg.evaluate("""()=>({tiles:document.querySelectorAll('#bento .lg-tile').length,
          broken:[...document.querySelectorAll('#bento img')].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src.split('/').pop())})""")
        info["requestfailed"]=broken
        w=pg.locator("li", has_text="missing from disk")
        if w.count():
            w.first.locator("xpath=..").screenshot(path=OUT+"D-logos-%s-notes.png"%k)
            info["warning_shot"]=True
        log["logos-"+k]=info; pg.close()
    # B. caption, supercharge dark, darkgrey caption ground
    for canon in ("canon","nocanon"):
        for k,base in SRC.items():
            ctx=b.new_context(viewport={"width":1280,"height":900}, device_scale_factor=2)
            pg=ctx.new_page()
            if canon=="nocanon":
                pg.route("**/canon.css", lambda r: r.abort())
            pg.goto("file://"+base+"bento.html"); pg.wait_for_timeout(1000)
            res=pg.evaluate("""()=>{document.documentElement.setAttribute('data-apollo-theme','supercharge');
              document.body.setAttribute('data-theme','dark');
              const s=document.querySelector('.bm-stage'); s.setAttribute('data-type','gallery'); s.setAttribute('data-cap-bg','darkgrey');
              const c=[...s.querySelectorAll('.bm-cap')].find(e=>e.getBoundingClientRect().width>80);
              c.id='d-cap'; c.scrollIntoView({block:'center'});
              const r=c.getBoundingClientRect();
              return {bg:getComputedStyle(c).backgroundColor, page:getComputedStyle(document.documentElement).backgroundColor,
                      neutral5:getComputedStyle(document.body).getPropertyValue('--color-neutral-5'),
                      text:c.textContent.trim().slice(0,60), x:r.x,y:r.y,w:r.width,h:r.height}}""")
            pg.wait_for_timeout(300)
            r=pg.evaluate("()=>{const r=document.getElementById('d-cap').getBoundingClientRect();return [r.x,r.y,r.width,r.height]}")
            if canon=="canon":
                pad=28; clip={"x":max(0,r[0]-pad),"y":max(0,r[1]-pad*3),"width":min(420,r[2]+2*pad),"height":r[3]+pad*4}
            else:
                clip={"x":r[0],"y":r[1],"width":min(420,r[2]),"height":r[3]}
            pg.screenshot(path=OUT+"D-caption-%s-%s.png"%(k,canon), clip=clip)
            log["caption-%s-%s"%(k,canon)]=res; ctx.close()
    b.close()
print(json.dumps(log,indent=1))
json.dump(log,open(OUT+"D-render-log.json","w"),indent=1)
