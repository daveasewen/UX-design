"""W3a probe: computed --bento-dashboard-main/sub and the rendered wall/group gaps. Usage: probe_gutter.py PAGE [theme-override]"""
import os, sys, json
from playwright.sync_api import sync_playwright
page_path = os.path.abspath(sys.argv[1]); th = sys.argv[2] if len(sys.argv) > 2 else None
JS = """(th)=>{ if(th){document.querySelectorAll('[data-apollo-theme]').forEach(e=>e.setAttribute('data-apollo-theme',th));}
 const t=document.querySelector('[data-apollo-theme]')||document.documentElement; const cs=getComputedStyle(t);
 const walls=[...document.querySelectorAll('.tpl-wall,[data-bento-role="dashboard"]')].slice(0,2).map(w=>({cls:w.className.slice(0,50),gap:getComputedStyle(w).columnGap+'/'+getComputedStyle(w).rowGap}));
 const groups=[...document.querySelectorAll('[class*="tpl-group"]')].slice(0,2).map(w=>({cls:w.className.slice(0,50),gap:getComputedStyle(w).columnGap}));
 const w=document.querySelector('.tpl-wall'); const kids=w?[...w.children].map(k=>k.getBoundingClientRect()).filter(r=>r.width>0):[]; const gaps=[]; for(let i=1;i<kids.length;i++){const a=kids[i-1],b=kids[i]; gaps.push(Math.abs(b.top-a.bottom)<Math.abs(b.left-a.right)&&b.top>=a.bottom-1?+(b.top-a.bottom).toFixed(1):+(b.left-a.right).toFixed(1));}
 return {wallGaps:gaps, bentoGutter:w?getComputedStyle(w).getPropertyValue('--bento-gutter'):null, theme:t.getAttribute('data-apollo-theme'), main:cs.getPropertyValue('--bento-dashboard-main'), sub:cs.getPropertyValue('--bento-dashboard-sub'), walls, groups}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto("file://" + page_path); pg.wait_for_timeout(900)
    print(json.dumps(pg.evaluate(JS, th))); b.close()
