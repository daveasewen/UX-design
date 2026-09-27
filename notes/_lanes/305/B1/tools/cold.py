"""cold.py — candidate 2 run 3 pages (the pack's own cold run, #304 R4c) restaged against the BEFORE
(backup) and AFTER (live) canon.css + type.css, then measured at 1440 in light and dark: the ground
(call 9), a real Kpi-tile's spark inside the bento (41b), the Kpi label (5/10), the ring tile (8)."""
import os, sys, json, re
from playwright.sync_api import sync_playwright
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.join(B, *[".."] * 4))
SRC = os.path.join(ROOT, "notes/_lanes/304/R4c/cold/cand2-r3/out")
CANON = {"before": os.path.join(B, "backup/knowledge/canon"), "after": os.path.join(ROOT, "knowledge/canon")}
PAGES = sys.argv[1:] or ["index.html", "trade.html", "liquidity.html"]
res = {}
LIB = open(os.path.join(B, "tools/look.py"), encoding="utf-8").read().split('LIB = r"""')[1].split('"""')[0]
M = r"""()=>{const hex=o=>o?'#'+[o.r,o.g,o.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join(''):null; const q=s=>document.querySelector(s);
 const kt=[...document.querySelectorAll('.cn-kpi-tile .kpi-tile')].slice(0,4).map(t=>{const l=t.querySelector('.kpi-lbl'), v=t.querySelector('.kpi-val'), s=t.querySelector('.spark-inline');
   return {h:+t.getBoundingClientRect().height.toFixed(2), spark:s?+s.getBoundingClientRect().height.toFixed(1):null, lblToVal:l&&v?(v.getBoundingClientRect().top-l.getBoundingClientRect().top).toFixed(2):null,
     ovY:l?getComputedStyle(l).overflowY:null, lbl:l?__b1.contrast(l):null}; });
 const rings=[...document.querySelectorAll('figure.dv[data-dv-type=donut], figure.dv[data-dv-type=pie]')].map(f=>{const t=f.closest('.c-bento__tile'); const row=t?[...t.parentElement.children].filter(c=>c!==t&&c.classList.contains('c-bento__tile')):[];
   const tr=t?t.getBoundingClientRect():null; const fr=f.getBoundingClientRect();
   return {tileH:tr?+tr.height.toFixed(1):null, tileW:tr?+tr.width.toFixed(1):null, figH:+fr.height.toFixed(1), slack:tr?+(tr.bottom-fr.bottom).toFixed(1):null, alignSelf:t?getComputedStyle(t).alignSelf:null,
     rowMaxH: row.length? Math.max(...row.map(c=>+c.getBoundingClientRect().height.toFixed(1))):null}; });
 const main=q('main.tpl-page')||q('main'); const hdr=q('.tpl-header'); const tile=q('.cn-template-dashboard-bento .c-bento__tile .kpi-tile, .cn-template-dashboard-bento .c-bento__tile');
 return {theme:document.documentElement.getAttribute('data-apollo-theme'), body:hex(__b1.ground(document.body)), header:hdr?hex(__b1.ground(hdr)):null, section:main?hex(__b1.ground(main)):null,
   kpiTiles:kt, rings};}"""
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for tag, cdir in CANON.items():
        stage = os.path.join(B, "work/cold", tag); os.makedirs(stage, exist_ok=True)
        for pg_name in PAGES:
            h = open(os.path.join(SRC, pg_name), encoding="utf-8").read()
            h = h.replace('href="../pack/knowledge/canon/canon.css"', 'href="file://%s/canon.css"' % cdir)
            h = h.replace('href="../pack/knowledge/canon/type.css"', 'href="file://%s/type.css"' % cdir)
            path = os.path.join(stage, pg_name); open(path, "w", encoding="utf-8").write(h)
            for mode in ("light", "dark"):
                c = br.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce"); pg = c.new_page()
                pg.goto("file://" + path); pg.wait_for_timeout(1000); pg.evaluate(LIB)
                pg.evaluate("m=>{document.documentElement.setAttribute('data-theme',m); document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',m));}", mode)
                pg.wait_for_timeout(1500)
                res["%s-%s-%s" % (tag, pg_name, mode)] = pg.evaluate(M)
                pg.screenshot(path=os.path.join(B, "renders", tag, "cold-c2r3-%s-%s-1440.png" % (pg_name.replace(".html", ""), mode)), full_page=True)
                c.close()
    br.close()
json.dump(res, open(os.path.join(B, "renders/cold-c2r3-measure.json"), "w"), indent=1)
for k in sorted(res): print(k, json.dumps(res[k])[:600])
