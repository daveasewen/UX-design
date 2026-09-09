import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':2200,'height':900})
    pg.goto("file://"+R+"/knowledge/snippets/Footer.reference.html"); pg.wait_for_timeout(400)
    for w in (1600,1440,1280,1024,768,420,375):
        r=pg.evaluate("""(w)=>{const sh=document.querySelector('.shell');sh.style.width=w+'px';sh.style.margin='0';
        const f=sh.querySelector('footer.ft');const a=[...f.querySelectorAll('.lnk')];
        const h=f.getBoundingClientRect().height;
        let gap=null; if(a.length>1){const r1=a[0].getBoundingClientRect(),r2=a[1].getBoundingClientRect();gap=Math.round(r2.left-r1.right);}
        const rows=new Set([...f.querySelectorAll('.ft-id,.ft-meta,.ft-end')].map(e=>Math.round(e.getBoundingClientRect().top)));
        return [Math.round(h), Math.round(a[0].getBoundingClientRect().height), gap, rows.size];}""",w)
        print(w, r, "grid" if r[0]%4==0 else "OFF-GRID")
    b.close()
