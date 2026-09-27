"""W3a probe: computed style + box + ink of every .kpi-lbl on a page (1440). Usage: probe_kpi.py PAGE [css-to-inject-file]"""
import os, sys, json
from playwright.sync_api import sync_playwright
page_path = os.path.abspath(sys.argv[1]); extra = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
JS = r"""(extra)=>{ if(extra){const s=document.createElement('style');s.textContent=extra;document.head.appendChild(s);}
 const out=[]; const cv=document.createElement('canvas').getContext('2d');
 for(const el of document.querySelectorAll('.kpi-lbl')){ const cs=getComputedStyle(el); const r=el.getBoundingClientRect();
  cv.font=cs.font; const m=cv.measureText(el.textContent.trim());
  const rng=document.createRange(); rng.selectNodeContents(el); const tr=rng.getBoundingClientRect();
  out.push({t:el.textContent.trim().slice(0,24), cls:el.className, fs:cs.fontSize, lh:cs.lineHeight, fam:cs.fontFamily.slice(0,30),
   trim:cs.textBoxTrim, edge:cs.textBoxEdge, ov:cs.overflow, h:+r.height.toFixed(2), top:+r.top.toFixed(2), textRangeH:+tr.height.toFixed(2), textRangeTop:+tr.top.toFixed(2),
   fontAsc:+m.fontBoundingBoxAscent.toFixed(2), fontDesc:+m.fontBoundingBoxDescent.toFixed(2), inkAsc:+m.actualBoundingBoxAscent.toFixed(2), inkDesc:+m.actualBoundingBoxDescent.toFixed(2)}); }
 return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto("file://" + page_path); pg.wait_for_timeout(600)
    for row in pg.evaluate(JS, extra)[:6]: print(json.dumps(row))
    b.close()
