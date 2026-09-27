"""V1 k3.py — every element with its own text: box h/w (>1px) AND computed color / background / border-color, before v after canon, 4 themes x 2 modes, 1440."""
import os, sys, json, collections
from playwright.sync_api import sync_playwright
V = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JS = """()=>[...document.body.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())||e.matches('.note,.nv-count,.c-bento__tile,.kpi-tile,.sh')).map(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);const s=e.closest('[class*="cn-"]');const sc=s?[...s.classList].find(c=>c.startsWith('cn-')):'-';
 return [sc,e.tagName.toLowerCase()+'.'+((e.getAttribute('class')||'').split(' ')[0]),Math.round(r.height*10)/10,Math.round(r.width*10)/10,cs.color,cs.backgroundColor,cs.borderTopColor,cs.opacity,(e.textContent||'').trim().slice(0,20)];})"""
pages = sys.argv[1:]
tot = collections.Counter(); detail = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for name in pages:
        for th in ("mono","common","console","supercharge"):
            for m in ("light","dark"):
                res=[]
                for tag in ("before","after"):
                    pg=b.new_page(viewport={"width":1440,"height":900},reduced_motion="reduce"); pg.goto("file://"+os.path.join(V,tag,"pages",name)); pg.wait_for_timeout(700); pg.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important}")
                    pg.evaluate("([a,t])=>{document.documentElement.setAttribute('data-apollo-theme',a);document.documentElement.setAttribute('data-theme',t);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',t));}",[th,m]); pg.wait_for_timeout(1200)
                    res.append(pg.evaluate(JS)); pg.close()
                X,Y=res
                if len(X)!=len(Y): print(name,th,m,"DOM differs",len(X),len(Y)); continue
                c=collections.Counter()
                for x,y in zip(X,Y):
                    geo = abs(x[2]-y[2])>1.0 or abs(x[3]-y[3])>1.0
                    col = x[4:8]!=y[4:8]
                    if (geo or col) and not x[0].startswith("cn-chart"):
                        c["%s %s %s %s"%(x[0],x[1],'GEO' if geo else '','COL %s->%s bg %s->%s bc %s->%s'%(x[4],y[4],x[5],y[5],x[6],y[6]) if col else '')]+=1
                chart=sum(1 for x,y in zip(X,Y) if (abs(x[2]-y[2])>1.0 or abs(x[3]-y[3])>1.0 or x[4:8]!=y[4:8]) and x[0].startswith("cn-chart"))
                print(name,th,m,len(X),"non-chart moved:",sum(c.values()),"chart moved:",chart); 
                for k,v in c.most_common(8): print("   ",v,k[:230])
    b.close()
