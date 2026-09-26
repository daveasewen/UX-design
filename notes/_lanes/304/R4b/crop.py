import os, sys
from playwright.sync_api import sync_playwright
f,w,text,out=sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4]
pad=float(sys.argv[5]) if len(sys.argv)>5 else 40
JS="""(t)=>{const want=t; const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while((n=tw.nextNode())){if(n.nodeValue.trim()===t && n.parentElement.namespaceURI.includes('svg')===(!!window.__svg)){const r=n.parentElement.getBoundingClientRect(); if(r.width>0) return [r.left+scrollX,r.top+scrollY,r.width,r.height];}}return null}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],headless=True,args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":w,"height":900},device_scale_factor=3); pg.emulate_media(reduced_motion="reduce")
    pg.goto("file://"+os.path.abspath(f)); pg.evaluate("()=>{window.__svg=true}"); pg.wait_for_timeout(600)
    r=pg.evaluate(JS,text); pg.evaluate("(y)=>window.scrollTo(0,Math.max(0,y-300))", r[1]); pg.wait_for_timeout(800); r=pg.evaluate(JS,text); print(r)
    pg.screenshot(path=out,full_page=True,clip={"x":max(0,r[0]-pad),"y":max(0,r[1]-pad/2),"width":r[2]+2*pad+60,"height":r[3]+pad})
    b.close()
