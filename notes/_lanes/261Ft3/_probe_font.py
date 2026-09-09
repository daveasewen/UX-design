import os,sys,json
p=os.environ.get("APOLLO_PW_LD_LIBRARY_PATH","/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu")
os.environ["LD_LIBRARY_PATH"]=p+":"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R="/sessions/zen-funny-hawking/mnt/UX-design"
targets=[
 ("snippet","file://"+R+"/knowledge/snippets/Sidebar-nav.reference.html",".nv-label"),
 ("review","file://"+R+"/notes/_lanes/261-N-nav-review.html",".nv-label"),
]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page()
    for name,url,sel in targets:
        pg.goto(url); pg.wait_for_timeout(1200)
        if name=="review":
            r=pg.evaluate("""(sel)=>{const out=[];document.querySelectorAll('iframe').forEach((f,i)=>{try{const d=f.contentDocument;const e=d.querySelector(sel);if(e)out.push([i,f.getAttribute('title'),getComputedStyle(e).fontFamily]);}catch(e){}});return out;}""",sel)
        else:
            r=pg.evaluate("""(sel)=>{const e=document.querySelector(sel);return e?[[0,'snippet',getComputedStyle(e).fontFamily]]:'NOT FOUND';}""",sel)
        print(name,json.dumps(r)[:600])
    b.close()
