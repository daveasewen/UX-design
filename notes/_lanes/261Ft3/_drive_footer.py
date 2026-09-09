import os,json,sys
os.environ["LD_LIBRARY_PATH"]="/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
from playwright.sync_api import sync_playwright
R=os.path.abspath(".")
URL="file://"+R+"/knowledge/snippets/Footer.reference.html"
THEMES=[None,"legacy","console","supercharge"]; MODES=["light","dark"]
def lum(c):
    c=c.strip(); 
    if c.startswith("rgb"):
        v=[int(x) for x in c[c.index("(")+1:c.index(")")].split(",")[:3]]
    else:
        v=[int(c[i:i+2],16) for i in (1,3,5)]
    def f(x):
        x/=255; return x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4
    return .2126*f(v[0])+.7152*f(v[1])+.0722*f(v[2])
def cr(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return round((hi+.05)/(lo+.05),2)
JS="""()=>{const o={};document.querySelectorAll('footer.ft').forEach((f,i)=>{
 const r=f.getBoundingClientRect(); const cs=getComputedStyle(f);
 const seats=[];
 f.querySelectorAll('.ft-prod,.ft-ver,.ft-env,.ft-status span:not(.ft-dot),.ft-meta span,.lnk,.ft-copy').forEach(e=>{
   if(!e.textContent.trim())return; const s=getComputedStyle(e);
   let bg='rgba(0, 0, 0, 0)',p=e;
   while(p&&bg==='rgba(0, 0, 0, 0)'){const b=getComputedStyle(p).backgroundColor; if(b!=='rgba(0, 0, 0, 0)'){bg=b;break;} p=p.parentElement;}
   seats.push([e.className.split(' ')[0], s.color, bg, e.textContent.trim().slice(0,18)]);});
 const tg=[...f.querySelectorAll('.lnk')].map(a=>a.getBoundingClientRect().height);
 o['ft'+i]={h:+r.height.toFixed(2), variant:f.className, bg:cs.backgroundColor, ink:cs.color, seats, targets:tg};});
 return o;}"""
rows=[];fails=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':1000})
    for t in THEMES:
        for m in MODES:
            pg.goto(URL); pg.wait_for_timeout(300)
            pg.evaluate("([t,m])=>{if(t)document.documentElement.setAttribute('data-apollo-theme',t);else document.documentElement.removeAttribute('data-apollo-theme');document.body.setAttribute('data-theme',m);document.querySelectorAll('[data-theme]').forEach(e=>{if(e!==document.body)e.setAttribute('data-theme',m)});}",[t,m])
            pg.wait_for_timeout(250)
            d=pg.evaluate(JS)
            tn=t or "mono"
            for k,v in d.items():
                bad=[]
                for cl,fg,bg,tx in v['seats']:
                    r=cr(fg,bg)
                    if r<4.5: bad.append((cl,fg,bg,r,tx)); fails.append((tn,m,k,cl,r,tx))
                small=[h for h in v['targets'] if h<24]
                rows.append((tn,m,k,v['h'],v['bg'],v['ink'],len(v['seats']),len(bad),len(small)))
                if small: fails.append((tn,m,k,'TARGET',min(small),''))
    b.close()
print(f"{'theme':13s}{'mode':6s}{'inst':6s}{'h':8s}{'band':22s}{'ink':22s}seats fail  <24")
for r in rows: print(f"{r[0]:13s}{r[1]:6s}{r[2]:6s}{r[3]:<8}{r[4]:22s}{r[5]:22s}{r[6]:<6}{r[7]:<6}{r[8]}")
print("\nFAILURES:",len(fails))
for f in fails[:20]: print(" ",f)
