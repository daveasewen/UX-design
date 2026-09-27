"""k3b.py <pageA> <pageB> — same page rendered from two trees (paths differ by tree root); text elements whose height changed >1px, grouped by nearest cn- scope, excluding cn-chart-*."""
import os,sys,collections
from playwright.sync_api import sync_playwright
JS = """() => [...document.body.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType===3 && n.textContent.trim())).map(e => { const r = e.getBoundingClientRect(); let s = e.closest('[class*="cn-"]');
  const sc = s ? [...s.classList].find(c => c.startsWith('cn-')) : '-'; return [sc, e.tagName.toLowerCase() + '.' + ((e.getAttribute('class')||'').split(' ')[0]), Math.round(r.height*10)/10, (e.textContent||'').trim().slice(0,24)]; })"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for pa,pb in zip(sys.argv[1::2], sys.argv[2::2]):
        for theme in ('light','dark'):
            res=[]
            for f in (pa,pb):
                pg=b.new_page(viewport={"width":1440,"height":900},reduced_motion="reduce"); pg.goto("file://"+os.path.abspath(f)); pg.wait_for_timeout(600)
                pg.evaluate("t=>document.documentElement.setAttribute('data-theme',t)",theme); pg.wait_for_timeout(500)
                res.append(pg.evaluate(JS)); pg.close()
            A,B=res; c=collections.Counter(); ex={}
            if len(A)!=len(B): print('DOM differs'); continue
            for x,y in zip(A,B):
                if abs(x[2]-y[2])>1.0: k=(x[0],x[1]); c[k]+=1; ex.setdefault(k,(x[2],y[2],x[3]))
            print('==',os.path.basename(pa),theme,'text elements',len(A),'changed',sum(c.values()),'non-chart',sum(v for k,v in c.items() if not k[0].startswith('cn-chart')))
            for k,n in c.most_common(60):
                if not k[0].startswith('cn-chart'): print('   %3d %-24s %-30s %s -> %s  %r'%(n,k[0],k[1][:30],ex[k][0],ex[k][1],ex[k][2]))
    b.close()
