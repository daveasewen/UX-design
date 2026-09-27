"""k3f.py <sideA> <sideB> <run> <page>... — V5's K3 test (tools/k3.py, same JS, same 4 apollo themes x light/dark,
1440, reduced motion) between two F5 stages; groups every text element whose box height moved >1px by nearest cn- scope,
and splits chart (cn-chart-*) from non-chart."""
import os, sys, collections
from playwright.sync_api import sync_playwright
H=os.environ['HOME']
JS = """() => [...document.body.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType===3 && n.textContent.trim())).map(e => { const r = e.getBoundingClientRect(); let s = e.closest('[class*="cn-"]');
  const sc = s ? [...s.classList].find(c => c.startsWith('cn-')) : '-'; const cs=getComputedStyle(e); return [sc, e.tagName.toLowerCase() + '.' + ((e.getAttribute('class')||'').split(' ')[0]), Math.round(r.height*10)/10, Math.round(r.top*10)/10, cs.textBoxTrim||'', (e.textContent||'').trim().slice(0,30)]; })"""
SA, SB, run = sys.argv[1], sys.argv[2], sys.argv[3]; pages = sys.argv[4:]
themes = [(a,t) for a in ('common','console','mono','supercharge') for t in ('light','dark')]
tot = collections.Counter(); ex = {}; nel=0; nch=0; nnon=0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for pg_name in pages:
        for a,t in themes:
            res=[]
            for S in (SA,SB):
                pg = b.new_page(viewport={"width":1440,"height":900}, reduced_motion="reduce")
                pg.goto("file://%s/f5st/%s/%s/out/%s" % (H,S,run,pg_name)); pg.wait_for_timeout(600)
                pg.evaluate("([a,t])=>{document.documentElement.setAttribute('data-apollo-theme',a);document.documentElement.setAttribute('data-theme',t);}", [a,t]); pg.wait_for_timeout(700)
                res.append(pg.evaluate(JS)); pg.close()
            A,B=res
            if len(A)!=len(B): print("DOM differs", pg_name, a, t, len(A), len(B)); continue
            nel += len(A); c=n=0
            for x,y in zip(A,B):
                if abs(x[2]-y[2])>1.0:
                    k=(x[0],x[1]); tot[k]+=1; ex.setdefault(k,(x[2],y[2],x[4],y[4],x[5]))
                    if x[0].startswith('cn-chart'): c+=1
                    else: n+=1
            nch+=c; nnon+=n
            print("  %-14s %-12s %-5s text-elements %4d  moved>1px chart %3d  non-chart %d" % (pg_name,a,t,len(A),c,n))
    b.close()
print("%s v %s on %s: elements %d · moved chart %d · moved NON-CHART %d" % (SA,SB,run,nel,nch,nnon))
for k,n in tot.most_common(30): print("  %4d %-26s %-34s %s -> %s  trim %s -> %s  '%s'" % (n,k[0],k[1][:34],ex[k][0],ex[k][1],ex[k][2],ex[k][3],ex[k][4]))
