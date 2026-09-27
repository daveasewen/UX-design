"""W3a probe: on a page view, toggle every legend switch of the first visible centre-figure chart
one at a time (and then pairs off), reading the centre after each. Usage: probe_legend.py PAGE VIEW"""
import os, sys, json
from playwright.sync_api import sync_playwright
page_path = os.path.abspath(sys.argv[1]); view = sys.argv[2]
JS = """(k)=>{const v=[...document.querySelectorAll('[data-dv-view="value"] .dv-val')].find(e=>e.getClientRects().length);
 let n=v; let sw=[]; while(n&&!(sw=[...n.querySelectorAll('[aria-checked]')]).length){n=n.parentElement;}
 const out=[]; for(let i=0;i<sw.length;i++){ sw[i].click(); out.push(v.textContent); if(k===1) sw[i].click(); } return {n:sw.length,reads:out};}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg = b.new_page(viewport={"width":1440,"height":1000})
    for k in (1, 2):
        pg.goto("file://" + page_path + "#/" + view); pg.wait_for_timeout(1200)
        print(("single toggles" if k == 1 else "cumulative off"), json.dumps(pg.evaluate(JS, k)))
    b.close()
