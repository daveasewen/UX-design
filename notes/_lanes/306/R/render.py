#!/usr/bin/env python3
"""306 R: render-check the decision page at 1440 and 390, light and dark (file:// goto, $RENDER_SHELL)."""
import os, json
from playwright.sync_api import sync_playwright
ROOT=os.path.expanduser("~/mnt/Projects--UX-design")
PAGE=os.path.join(ROOT,"notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html")
OUT=os.path.join(ROOT,"notes/_lanes/306/R/renders"); os.makedirs(OUT,exist_ok=True)
res=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w in (1440,390):
        for scheme in ("light","dark"):
            ctx=b.new_context(viewport={"width":w,"height":900},color_scheme=scheme)
            pg=ctx.new_page(); errs=[]
            pg.on("pageerror",lambda e: errs.append(str(e)))
            pg.on("console",lambda m: errs.append("console:"+m.text) if m.type=="error" else None)
            pg.goto("file://"+PAGE); pg.wait_for_timeout(300)
            ov=pg.evaluate("""()=>{const d=document.documentElement;const off=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.right>d.clientWidth+1||r.left<-1)&&getComputedStyle(e).position!=='fixed'){let a=e;let inScroll=false;while(a=a.parentElement){if(a.classList&&a.classList.contains('tw')){inScroll=true;break}}off.push((inScroll?'[in .tw] ':'')+e.tagName+'.'+e.className+' '+Math.round(r.right))}});
              const tw=[...document.querySelectorAll('.tw')].map(t=>t.scrollWidth-t.clientWidth);
              return {sw:d.scrollWidth,cw:d.clientWidth,off:off.slice(0,8),tw:tw}}""")
            chk={}
            if w==390 and scheme=="light":
                pg.click('.chips[data-d="one"] .chip[data-a="a"]'); pg.click('.chips[data-d="ci"] .chip[data-a="b"]'); pg.click('.chips[data-d="report"] .chip[data-a="yes"]')
                pg.fill('textarea[data-g="page"]','test words')
                chk["on"]=pg.evaluate("document.querySelectorAll('.chip.on').length")
                chk["count"]=pg.inner_text("#dd-count")
                md=pg.evaluate("window.__ddMarkdown()")
                chk["md_has_q1"]="Write the session's story once, and generate every other view from it, the handoff included?" in md
                chk["md_has_ans"]="a · Yes, story plus measured figures, all views generated" in md and "b · Summary at the push, but still wait" in md
                chk["md_words"]="> test words" in md
                pg.click("#dd-copy"); pg.wait_for_timeout(200); chk["msg"]=pg.inner_text("#dd-msg")
                pg.reload(); pg.wait_for_timeout(200); chk["persist_on"]=pg.evaluate("document.querySelectorAll('.chip.on').length")
                open(os.path.join(OUT,"export-sample.md"),"w").write(md)
                pg.click("#dd-clear")
            shot=os.path.join(OUT,f"page-{w}-{scheme}.png")
            pg.screenshot(path=shot,full_page=True)
            svg=pg.locator("figure").first; svg.screenshot(path=os.path.join(OUT,f"svg-{w}-{scheme}.png"))
            res.append({"w":w,"scheme":scheme,"errors":errs,"scrollW":ov["sw"],"clientW":ov["cw"],"hscroll":ov["sw"]>ov["cw"],"offedge":ov["off"],"table_inner_scroll":ov["tw"],**chk})
            ctx.close()
    b.close()
print(json.dumps(res,indent=1))
json.dump(res,open(os.path.join(OUT,"render-check.json"),"w"),indent=1)
