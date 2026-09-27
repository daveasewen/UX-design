"""V3: Kpi-tile before/after — 1440 light+dark, 4x crop of the first tile, and the lock-up measured.
Usage: kpi_pair.py <before.html> <after.html> <outdir>"""
import os, sys, json
from playwright.sync_api import sync_playwright
before, after, out = [os.path.abspath(a) for a in sys.argv[1:4]]
os.makedirs(out, exist_ok=True)
DARK = """()=>{const els=[...document.querySelectorAll('[data-theme]')]; if(!els.length) document.documentElement.setAttribute('data-theme','dark'); els.forEach(e=>e.setAttribute('data-theme','dark'));}"""
MEAS = r"""()=>{const rows=[]; const cv=document.createElement('canvas').getContext('2d');
 for(const t of [...document.querySelectorAll('.kpi-tile')].slice(0,8)){
  const l=t.querySelector('.kpi-lbl'), v=t.querySelector('.kpi-val'), d=t.querySelector('.kpi-delta');
  if(!l||!v) continue; const lr=l.getBoundingClientRect(), vr=v.getBoundingClientRect(), tr=t.getBoundingClientRect();
  const cs=getComputedStyle(l); cv.font=cs.font; const m=cv.measureText(l.textContent.trim());
  const rng=document.createRange(); rng.selectNodeContents(l); const ink=rng.getBoundingClientRect();
  rows.push({lbl:l.textContent.trim().slice(0,22), tileH:+tr.height.toFixed(2), lblBoxH:+lr.height.toFixed(2),
   trim:cs.textBoxTrim, edge:cs.textBoxEdge, lh:cs.lineHeight,
   lblTop_in_tile:+(lr.top-tr.top).toFixed(2), valTop_in_tile:+(vr.top-tr.top).toFixed(2),
   lbl_to_val_boxTop:+(vr.top-lr.top).toFixed(2), lbl_to_val_offsetTop:(v.offsetTop-l.offsetTop),
   val_to_delta_offsetTop: d? (d.offsetTop-v.offsetTop):null,
   descCut:+Math.max(0,(ink.bottom-lr.bottom)).toFixed(2), inkDesc:+m.actualBoundingBoxDescent.toFixed(2)});
 }
 const first=document.querySelector('.kpi-tile'); const r=first.getBoundingClientRect();
 return {rows, clip:{x:Math.max(0,r.left-8), y:Math.max(0,r.top-8+scrollY), width:Math.min(r.width+16,700), height:r.height+16}};}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    res = {}
    for tag, path in (("before", before), ("after", after)):
        for mode in ("light", "dark"):
            for dsf in (1, 4):
                pg = b.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=dsf)
                pg.goto("file://" + path); pg.wait_for_timeout(900)
                if mode == "dark": pg.evaluate(DARK); pg.wait_for_timeout(500)
                info = pg.evaluate(MEAS)
                if dsf == 1:
                    h = min(pg.evaluate("document.documentElement.scrollHeight"), 2400)
                    pg.screenshot(path=f"{out}/kpi-{tag}-{mode}-1440.png", clip={"x":0,"y":0,"width":1440,"height":h}, full_page=True)
                    res[f"{tag}-{mode}"] = info["rows"]
                else:
                    pg.screenshot(path=f"{out}/kpi-{tag}-{mode}-tile1-4x.png", clip=info["clip"], full_page=True)
                pg.close()
    b.close()
json.dump(res, open(f"{out}/kpi-lockup-measure.json","w"), indent=1)
for k,v in res.items():
    print(k); [print("  ", json.dumps(r)) for r in v[:4]]
