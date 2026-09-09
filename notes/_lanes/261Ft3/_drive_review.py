import os
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
def lum(c):
    v=[int(x) for x in c[c.index("(")+1:c.index(")")].split(",")[:3]]
    def f(x):
        x/=255; return x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4
    return .2126*f(v[0])+.7152*f(v[1])+.0722*f(v[2])
def cr(a,b):
    la,lb=lum(a),lum(b); return round((max(la,lb)+.05)/(min(la,lb)+.05),2)
JS="""()=>{const o=[];document.querySelectorAll('footer.ft').forEach(ft=>{const cs=getComputedStyle(ft);const seats=[];
 ft.querySelectorAll('.ft-prod,.ft-ver,.ft-env,.ft-status span:not(.ft-dot),.ft-meta span,.lnk,.ft-copy').forEach(e=>{
  if(!e.textContent.trim())return;const s=getComputedStyle(e);let bg='rgba(0, 0, 0, 0)',p=e;
  while(p&&bg==='rgba(0, 0, 0, 0)'){const b=getComputedStyle(p).backgroundColor;if(b!=='rgba(0, 0, 0, 0)'){bg=b;break;}p=p.parentElement;}
  seats.push([s.color,bg,e.textContent.trim().slice(0,14)]);});
 o.push({h:+ft.getBoundingClientRect().height.toFixed(2),bg:cs.backgroundColor,seats});});return o;}"""
errs=[];tot=0;bad=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1500,'height':1200})
    pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("requestfailed",lambda r: errs.append("FAIL "+r.url))
    for t in ["mono","legacy","console","supercharge"]:
        for m in ["light","dark"]:
            pg.goto("file://"+R+"/notes/_lanes/261-Ft-footer-review.html"); pg.wait_for_timeout(400)
            pg.evaluate("([t,m])=>{document.querySelector('#themes button[data-theme-key=\"'+t+'\"]').click();document.querySelector('#modes button[data-mode=\"'+m+'\"]').click();}",[t,m])
            pg.wait_for_timeout(500)
            d=pg.evaluate(JS)
            for f in d:
                tot+=len(f['seats'])
                for fg,bg,tx in f['seats']:
                    r=cr(fg,bg)
                    if r<4.5: bad.append((t,m,r,tx,fg,bg))
            print(f"{t:12s}{m:6s} footers={len(d)} heights={sorted({f['h'] for f in d})} band={sorted({f['bg'] for f in d})}")
            if t=="mono" and m=="light": pg.screenshot(path="notes/_lanes/261-Ft3-review-mono-light.png",full_page=False)
            if t=="supercharge" and m=="dark": pg.screenshot(path="notes/_lanes/261-Ft3-review-supercharge-dark.png",full_page=False)
    b.close()
print(f"\nseats={tot} FAILURES={len(bad)}  console/network errors={len(errs)}")
for x in bad[:8]: print(" ",x)
for e in errs[:4]: print("  err:",e)
