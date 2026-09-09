import os,json
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page()
    errs=[]
    pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("requestfailed",lambda r: errs.append("FAIL "+r.url))
    pg.goto("file://"+R+"/notes/_lanes/261-N-nav-review.html"); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const o=[];document.querySelectorAll('iframe').forEach((f,i)=>{try{const d=f.contentDocument;const e=d.body.querySelector('a,button,li')||d.body;o.push([i,f.getAttribute('title'),getComputedStyle(e).fontFamily.slice(0,24)]);}catch(e){o.push([i,'ERR',''+e]);}});return o;}""")
    print(json.dumps(r,indent=0))
    print("console/network errors:",len(errs), errs[:5])
    b.close()
