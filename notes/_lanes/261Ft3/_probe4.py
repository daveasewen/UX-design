import os,json
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
JS="""()=>{const o=[];document.querySelectorAll('*').forEach(e=>{const ff=getComputedStyle(e).fontFamily;if(ff.indexOf('Times')===0&&e.children.length===0&&e.textContent.trim()){const inNav=!!e.closest('nav,.nv,[class*=nav]');o.push([inNav,e.tagName+'.'+e.className, e.textContent.trim().slice(0,30)])}});return o.slice(0,400);}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page()
    pg.goto("file://"+R+"/knowledge/snippets/Sidebar-nav.reference.html"); pg.wait_for_timeout(900)
    r=pg.evaluate(JS)
    innav=[x for x in r if x[0]]
    print("serif leaf nodes:",len(r),"INSIDE nav:",len(innav))
    print(json.dumps(innav[:8],indent=0))
    print(json.dumps([x[1] for x in r[:6]]))
    b.close()
