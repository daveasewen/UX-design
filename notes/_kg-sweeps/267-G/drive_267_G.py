"""#267 lane G — drive notes/_KG-EXPLORER.html (v1.10) once: 0 console errors, and a dig on
ruling s151-D1 shows its AUTHORED edges. Run: python3 notes/_kg-sweeps/267-G/drive_267_G.py"""
import json, pathlib
from playwright.sync_api import sync_playwright

REPO = "/sessions/friendly-clever-sagan/mnt/UX-design"
PAGE = "file://" + REPO + "/notes/_KG-EXPLORER.html"
OUT = REPO + "/notes/_kg-sweeps/267-G"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

DIG = """(label)=>{
  for(const k in famOn){famOn[k]=1}
  try{recount();renderLegend();renderStats()}catch(e){}
  spin=false;
  const n=NODES.find(x=>x.label===label&&x.type==='ruling');
  if(!n) return {ok:false};
  setFocus(n);
  for(const m of NODES){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}
  draw();
  const rel=adj.get(n.id).filter(x=>alive(x.e));
  const authored=rel.filter(x=>x.e.authored&&!x.e.derived&&x.e.ratified);
  return {ok:true,id:n.id,relations:rel.length,
    authored:authored.map(x=>({type:x.e.type,dir:x.out?'out':'in',other:x.other,ratified:x.e.ratified})),
    types:[...new Set(rel.map(x=>x.e.type))],
    panelText:(document.getElementById('panel')||document.body).innerText.slice(0,4000)};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    errs = []
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto(PAGE)
    pg.wait_for_timeout(2500)
    stats = pg.evaluate("()=>({nodes:NODES.length,edges:EDGES.length,"
                        "authoredRuling:EDGES.filter(e=>e.ratified==='s267-D3').length,"
                        "clause:EDGES.filter(e=>e.type==='supersedesClause').length,"
                        "mentions:EDGES.filter(e=>e.type==='mentions').length,"
                        "proposed:EDGES.filter(e=>e.proposedType).length})")
    r = pg.evaluate(DIG, "s151-D1")
    pg.wait_for_timeout(400)
    pg.screenshot(path=OUT + "/s151-D1-dig-v110.png")
    pg.evaluate("()=>{document.documentElement.dataset.theme='dark';palette();draw()}")
    pg.wait_for_timeout(400)
    pg.screenshot(path=OUT + "/s151-D1-dig-v110-dark.png")
    b.close()

print(json.dumps({"stats": stats, "dig": {k: v for k, v in r.items() if k != 'panelText'},
                  "console_errors": errs}, indent=1))
print("--- panel head ---")
print((r.get('panelText') or '')[:1200])
json.dump({"stats": stats, "dig": r, "console_errors": errs},
          open(OUT + "/drive-267-G.json", "w"), indent=1)
