import os, sys, json
from playwright.sync_api import sync_playwright
f, w, text = sys.argv[1], int(sys.argv[2]), sys.argv[3]
JS = r"""(t) => { const out=[]; const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n;
 while((n=tw.nextNode())){ if(n.nodeValue.trim()!==t) continue; let e=n.parentElement; const chain=[];
  while(e && e!==document.body){ const c=getComputedStyle(e); const r=e.getBoundingClientRect();
   chain.push([e.tagName+'.'+(typeof e.className==='string'?e.className:'').slice(0,30), c.position, c.display, c.visibility, c.opacity, c.clip, c.clipPath, c.overflow, c.zIndex, c.transform.slice(0,30), Math.round(r.left)+','+Math.round(r.top)+' '+Math.round(r.width)+'x'+Math.round(r.height), e.hidden, e.getAttribute('aria-hidden'), c.contentVisibility]);
   e=e.parentElement; }
  out.push(chain); if(out.length>=1) break; }
 return out; }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],headless=True,args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":w,"height":900}); pg.goto("file://"+os.path.abspath(f)); pg.wait_for_timeout(500)
    for ch in pg.evaluate(JS, text):
        for x in ch: print(x)
    b.close()
