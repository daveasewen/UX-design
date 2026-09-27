"""V1 cold.py — candidate 2 run 3 pages against V1's before/after canon dirs; 1440 light+dark. Measures the real Kpi-tile spark in the bento (41b), the ring tile (8), the ground (9), the label (5/10)."""
import os, json
from playwright.sync_api import sync_playwright
V = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); ROOT = os.path.abspath(os.path.join(V, *[".."]*4))
SRC = os.path.join(ROOT, "notes/_lanes/304/R4c/cold/cand2-r3/out")
LIB = open(os.path.join(V, "tools/measure.py")).read().split('LIB = r"""')[1].split('"""')[0]
M = r"""()=>{const q=s=>document.querySelector(s);const hx=el=>el?__v1.hex(__v1.ground(el)):null;
 const kt=[...document.querySelectorAll('.cn-kpi-tile .kpi-tile')].slice(0,4).map(t=>{const l=t.querySelector('.kpi-lbl'),v=t.querySelector('.kpi-val'),s=t.querySelector('.spark-inline');return {h:+t.getBoundingClientRect().height.toFixed(2),spark:s?+s.getBoundingClientRect().height.toFixed(1):null,l2v:l&&v?+(v.getBoundingClientRect().top-l.getBoundingClientRect().top).toFixed(2):null,ovY:l?getComputedStyle(l).overflowY:null,lbl:l?__v1.contrast(l).ratio:null};});
 const rings=[...document.querySelectorAll('figure.dv[data-dv-type=donut],figure.dv[data-dv-type=pie]')].map(f=>{const t=f.closest('.c-bento__tile');const tr=t?t.getBoundingClientRect():null;const fr=f.getBoundingClientRect();const sib=t?[...t.parentElement.children].filter(c=>c!==t&&c.classList.contains('c-bento__tile')):[];
  return {tileH:tr?+tr.height.toFixed(1):null,tileW:tr?+tr.width.toFixed(1):null,figH:+fr.height.toFixed(1),slack:tr?+(tr.bottom-fr.bottom).toFixed(1):null,padB:t?getComputedStyle(t).paddingBottom:null,alignSelf:t?getComputedStyle(t).alignSelf:null,rowMaxH:sib.length?Math.max(...sib.map(c=>+c.getBoundingClientRect().height.toFixed(1))):null,leaf:t?!t.querySelector('.c-bento__tile'):null};});
 const main=q('main.tpl-page')||q('.tpl-page')||q('main');const hdr=q('.tpl-header');
 return {body:hx(document.body),header:hx(hdr),section:hx(main),kpi:kt,rings};}"""
res={}
with sync_playwright() as p:
    br=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for tag in ("before","after"):
        cdir=os.path.join(V,tag,"canon"); stage=os.path.join(V,tag,"cold"); os.makedirs(stage,exist_ok=True)
        for name in ("index.html","trade.html","liquidity.html"):
            h=open(os.path.join(SRC,name),encoding="utf-8").read().replace('href="../pack/knowledge/canon/canon.css"','href="file://%s/canon.css"'%cdir).replace('href="../pack/knowledge/canon/type.css"','href="file://%s/type.css"'%cdir)
            path=os.path.join(stage,name); open(path,"w",encoding="utf-8").write(h)
            for mode in ("light","dark"):
                c=br.new_context(viewport={"width":1440,"height":1000},reduced_motion="reduce"); pg=c.new_page(); pg.goto("file://"+path); pg.wait_for_timeout(1000); pg.evaluate(LIB)
                pg.evaluate("m=>{document.documentElement.setAttribute('data-theme',m);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',m));}",mode); pg.wait_for_timeout(1500)
                res["%s-%s-%s"%(tag,name,mode)]=pg.evaluate(M)
                if mode=="light" and name=="index.html": pg.screenshot(path=os.path.join(V,"renders",tag,"cold-index-light.png"),full_page=True)
                c.close()
    br.close()
json.dump(res,open(os.path.join(V,"renders","cold-measure.json"),"w"),indent=1)
for k in sorted(res): print(k, json.dumps(res[k])[:500])
