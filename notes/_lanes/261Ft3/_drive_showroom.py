import os,json
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
JS="""()=>{const fr=[...document.querySelectorAll('iframe')];const o=[];
fr.forEach(f=>{const d=f.contentDocument; if(!d)return;
 d.querySelectorAll('footer.ft').forEach(ft=>{const cs=getComputedStyle(ft);const seats=[];
  ft.querySelectorAll('.ft-prod,.ft-ver,.ft-env,.ft-status span:not(.ft-dot),.ft-meta span,.lnk,.ft-copy').forEach(e=>{
   if(!e.textContent.trim())return;const s=getComputedStyle(e);let bg='rgba(0, 0, 0, 0)',p=e;
   while(p&&bg==='rgba(0, 0, 0, 0)'){const b=getComputedStyle(p).backgroundColor;if(b!=='rgba(0, 0, 0, 0)'){bg=b;break;}p=p.parentElement;}
   seats.push([s.color,bg,e.textContent.trim().slice(0,14)]);});
  o.push({h:+ft.getBoundingClientRect().height.toFixed(2),bg:cs.backgroundColor,ink:cs.color,seats});});});
return o;}"""
tot=0;bad=[];panes=0
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1600,'height':1200})
    for t in ["mono","legacy","console","supercharge"]:
        for m in ["light","dark"]:
            pg.goto("file://"+R+"/showroom/footer.html"); pg.wait_for_timeout(500)
            pg.evaluate("([t,m])=>{document.querySelector('#themes button[data-theme=\"'+t+'\"]').click();const mb=document.querySelector('#modes button[data-mode=\"'+m+'\"]')||[...document.querySelectorAll('button')].find(b=>b.textContent.trim().toLowerCase()===m);if(mb)mb.click();}",[t,m])
            pg.wait_for_timeout(900)
            d=pg.evaluate(JS); panes+=1
            for f in d:
                tot+=len(f['seats'])
                for fg,bg,tx in f['seats']:
                    r=cr(fg,bg)
                    if r<4.5: bad.append((t,m,r,tx,fg,bg))
            hs=sorted({f['h'] for f in d}); bands=sorted({f['bg'] for f in d})
            print(f"{t:12s}{m:6s} footers={len(d)} heights={hs} band={bands} grid={all(abs(h/4-round(h/4))<0.01 for h in hs)}")
    b.close()
print(f"\npanes={panes} text seats measured={tot} FAILURES={len(bad)}")
for x in bad[:10]: print(" ",x)
