import os,json
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
JS="""()=>{const o=[];const w=(d,t)=>{const els=[...d.body.querySelectorAll('*')];const f={};els.forEach(e=>{const ff=getComputedStyle(e).fontFamily.split(',')[0];if(e.textContent.trim())f[ff]=(f[ff]||0)+1});o.push([t,f]);};
 if(document.querySelectorAll('iframe').length){document.querySelectorAll('iframe').forEach((fr,i)=>{try{w(fr.contentDocument,fr.getAttribute('title'))}catch(e){}})}else{w(document,'self')} return o;}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page()
    for u in ["/notes/_lanes/261-N-nav-review.html","/knowledge/snippets/Sidebar-nav.reference.html"]:
        try:
            pg.goto("file://"+R+u); pg.wait_for_timeout(900)
            print(u.split('/')[-1], json.dumps(pg.evaluate(JS)))
        except Exception as e: print(u,"ERR",e)
    b.close()
