"""#311 lane R — verify the revised wave-2 plan page: side scroll at 1440 and 390, Copy as text returns every call, screenshots."""
import os, json
from playwright.sync_api import sync_playwright
R=os.getcwd(); U="file://"+R+"/notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html"
OUT=R+"/notes/_lanes/311/R/shots"; os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w in (1440,390):
        pg=b.new_page(viewport={"width":w,"height":900}); pg.goto(U); pg.wait_for_timeout(1000); pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(400)
        r=pg.evaluate("""()=>({side:document.documentElement.scrollWidth-document.documentElement.clientWidth,
          calls:document.querySelectorAll('.call').length,
          overflow:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1 && getComputedStyle(e).position!='fixed' && !e.closest('.scroll')).slice(0,5).map(e=>e.tagName+'.'+e.className)})""")
        print(w, json.dumps(r))
        if w==1440:
            for i in range(1,6):
                pg.click('.call[data-id=c%d] .chip >> nth=0' % i)
            pg.fill('.call[data-id=c3] textarea','test comment'); pg.fill('.call[data-id=page] textarea','page note')
            t=pg.evaluate("window.__reviewText()"); print(t)
            qs=pg.evaluate("[...document.querySelectorAll('.call')].map(e=>e.dataset.q)")
            missing=[q for q in qs if q not in t and q!='Note on the page']
            print("COPY-AS-TEXT every call present:", "OK" if not missing and "Note on the page: page note" in t else "MISSING "+str(missing))
            print("count:", pg.inner_text('#count'))
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            pg.screenshot(path=OUT+"/plan-1440-top.png", full_page=False)
            pg.evaluate("document.querySelector('#day svg').scrollIntoView()"); pg.wait_for_timeout(600)
            pg.screenshot(path=OUT+"/plan-1440-day.png", full_page=False)
            pg.evaluate("document.getElementById('calls').scrollIntoView()"); pg.wait_for_timeout(600)
            pg.screenshot(path=OUT+"/plan-1440-calls.png", full_page=False)
        else:
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            pg.screenshot(path=OUT+"/plan-390-top.png", full_page=False)
            pg.evaluate("document.getElementById('jobs').scrollIntoView()"); pg.wait_for_timeout(600)
            pg.screenshot(path=OUT+"/plan-390-jobs.png", full_page=False)
        pg.close()
    b.close()
