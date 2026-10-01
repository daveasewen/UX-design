"""#311 lane M3 — verify the proposal page in context: side scroll at 1440 and 390, Copy as text returns every call, screenshots."""
import os, json
from playwright.sync_api import sync_playwright
R=os.getcwd(); U="file://"+R+"/notes/_PROPOSAL-311-apollo-for-other-libraries-2026-10-01-v1.html"
OUT=R+"/notes/_lanes/311/M/shots"; os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w in (1440,390):
        pg=b.new_page(viewport={"width":w,"height":900}); pg.goto(U); pg.wait_for_timeout(1200); pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(600)
        r=pg.evaluate("""()=>({side:document.documentElement.scrollWidth-document.documentElement.clientWidth,
          calls:document.querySelectorAll('.call').length,
          wide_visible:[...document.querySelectorAll('svg.wide')].filter(s=>getComputedStyle(s).display!='none').length,
          tall_visible:[...document.querySelectorAll('svg.tall')].filter(s=>getComputedStyle(s).display!='none').length,
          overflow:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1 && getComputedStyle(e).position!='fixed' && !e.closest('.scroll')).slice(0,5).map(e=>e.tagName+'.'+e.className)})""")
        print(w, json.dumps(r))
        if w==1440:
            for i in range(1,8):
                pg.click('.call[data-id=c%d] .chip >> nth=%d' % (i, 0 if i%2 else 1))
            pg.fill('.call[data-id=c3] textarea','test comment'); pg.fill('.call[data-id=page] textarea','page note')
            t=pg.evaluate("window.__reviewText()"); print(t)
            qs=pg.evaluate("[...document.querySelectorAll('.call')].map(e=>e.dataset.q)")
            missing=[q for q in qs if q not in t and not q.startswith('8.')]
            print("COPY-AS-TEXT every call present:", "OK" if not missing and "8. Note on the page: page note" in t else "MISSING "+str(missing))
            print("count:", pg.inner_text('#count'))
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            pg.screenshot(path=OUT+"/page-1440-top.png", full_page=False)
            for sec in ("today","options","arch","plan"):
                pg.evaluate("document.querySelector('#%s .diag, #%s .phase').scrollIntoView()" % (sec,sec)); pg.wait_for_timeout(900)
                pg.screenshot(path=OUT+"/page-1440-%s.png" % sec, full_page=False)
            pg.evaluate("document.getElementById('calls').scrollIntoView()"); pg.wait_for_timeout(900)
            pg.screenshot(path=OUT+"/page-1440-calls.png", full_page=False)
        else:
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            pg.screenshot(path=OUT+"/page-390-top.png", full_page=False)
            pg.evaluate("document.getElementById('arch').scrollIntoView()"); pg.wait_for_timeout(900)
            pg.screenshot(path=OUT+"/page-390-arch.png", full_page=False)
        pg.close()
    b.close()
