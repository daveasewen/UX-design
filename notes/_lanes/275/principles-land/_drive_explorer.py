"""#275 lane RL2 — drive notes/_KG-EXPLORER.html (v1.12) once.

Proves, in the real page: 0 console errors; the UX-principle chip exists and is OFF at
first paint; with it OFF nothing but the base page is drawn; clicking the REAL chip (not
famOn poked from the console) turns the family on and draws 145 ux: + 30 polarity: nodes
and all six ratified edge types.

  source knowledge/_render/seat_env.sh && python3 notes/_lanes/275/principles-land/_drive_explorer.py
"""
import json, pathlib
from playwright.sync_api import sync_playwright

REPO = "/sessions/dazzling-gifted-ritchie/mnt/UX-design"
PAGE = "file://" + REPO + "/notes/_KG-EXPLORER.html"
OUT = REPO + "/notes/_lanes/275/principles-land"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)
SIX = ["tensionWith", "hasParty", "touches", "resolvedBy", "challengedBy", "explainedBy"]

STATE = """(SIX)=>{
  const shown=(typeof SHOWN!=='undefined')?SHOWN.length:null;
  const se=(typeof SHOWNE!=='undefined')?SHOWNE.length:null;
  const drawn={}; SIX.forEach(t=>drawn[t]=(typeof SHOWNE!=='undefined')?SHOWNE.filter(e=>e.type===t).length:null);
  return {famOn:JSON.parse(JSON.stringify(famOn)),
          uxNodes:NODES.filter(n=>n.type==='ux').length,
          polNodes:NODES.filter(n=>n.type==='polarity').length,
          uxDrawnNodes:(typeof SHOWN!=='undefined')?SHOWN.filter(n=>n.type==='ux').length:null,
          polDrawnNodes:(typeof SHOWN!=='undefined')?SHOWN.filter(n=>n.type==='polarity').length:null,
          shown, shownEdges:se, drawn,
          chipExists:!!document.querySelector('[data-fam="uxprinciples"]'),
          chipLabel:(document.querySelector('[data-fam="uxprinciples"]')||{}).innerText,
          typeChips:['ux','polarity'].map(t=>!!document.querySelector('[data-type="'+t+'"]')),
          version:(document.querySelector('.brand span')||{}).innerText};
}"""
SETTLE = "()=>{try{spin=false}catch(e){};for(const m of NODES){if(m.tx!==undefined){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}};try{draw()}catch(e){}}"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    errs, msgs = [], []
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    pg.on("console", lambda m: (msgs.append(m.type), errs.append("console." + m.type + ": " + m.text)
                                if m.type in ("error", "warning") else None))
    pg.goto(PAGE)
    pg.wait_for_timeout(2500)
    pg.evaluate(SETTLE)
    pg.wait_for_timeout(300)

    off = pg.evaluate(STATE, SIX)
    pg.screenshot(path=OUT + "/screenshot-chip-off.png")

    pg.click('[data-fam="uxprinciples"]')          # the REAL chip, not famOn poked
    pg.wait_for_timeout(1800)
    pg.evaluate(SETTLE)
    pg.wait_for_timeout(300)
    on = pg.evaluate(STATE, SIX)
    # the new family is parked left of the base graph, off-canvas at the v1.1 zoom; press the
    # page's own Fit control so the shot actually shows what the chip switched on.
    pg.click("text=Fit")
    pg.wait_for_timeout(1200)
    pg.evaluate(SETTLE)
    pg.wait_for_timeout(300)
    pg.screenshot(path=OUT + "/screenshot-fit.png")
    # camera only: centre on the family's own centroid so the shot shows the 175 nodes the
    # chip switched on. Nothing in the graph is touched — only view.x/view.y/view.k.
    # proj() is screen = W/2 + (world + view.x) * view.k, so view.x/y are WORLD offsets.
    pg.evaluate("""()=>{const g=NODES.filter(n=>n.fam==='uxprinciples');
      const xs=g.map(n=>n.x),ys=g.map(n=>n.y);
      const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
      view.k=Math.min(W/(x1-x0+420),H/(y1-y0+300));
      view.x=-(x0+x1)/2; view.y=-(y0+y1)/2;
      draw();}""")
    pg.wait_for_timeout(500)
    pg.screenshot(path=OUT + "/screenshot.png")

    # 23 of the 96 resolved edges end on a ruling: node, which lives in the governance
    # layer (loads OFF) — #274's finding 2, inherited, not introduced here.
    pg.click('[data-fam="governance"]')
    pg.wait_for_timeout(1800)
    pg.evaluate(SETTLE)
    pg.wait_for_timeout(300)
    both = pg.evaluate(STATE, SIX)
    pg.screenshot(path=OUT + "/screenshot-with-governance.png")

    # a dig on one principle, to prove the panel reads the landed fields (s275-D1)
    dig = pg.evaluate("""()=>{const n=NODES.find(x=>x.id==='ux:pr-fitts')||NODES.find(x=>x.type==='ux');
      if(!n)return{ok:false};
      setFocus(n);const p=document.getElementById('panel')||document.body;
      const txt=p.innerText;
      return {ok:true,id:n.id,keys:Object.keys(n).length,
        fields:['statement','family','originator','year','grade','gradeName','evidence',
                'scope_conditions','known_misreadings','refutation_probe']
               .filter(f=>n[f]!==undefined).length,
        panel:txt.slice(0,320)};}""")
    pg.wait_for_timeout(900)
    pg.evaluate(SETTLE)
    pg.wait_for_timeout(300)
    pg.screenshot(path=OUT + "/screenshot-dig.png")
    b.close()

print("version banner:", off["version"])
print("chip exists:", off["chipExists"], "| label:", (off["chipLabel"] or "").replace("\n", " "))
print("ux/polarity TYPE chips present:", off["typeChips"])
print("first paint famOn.uxprinciples:", off["famOn"]["uxprinciples"], "(0 = loads OFF, as v1.2 layers do)")
print()
print("CHIP OFF :", off["shown"], "nodes /", off["shownEdges"], "relations · ux drawn",
      off["uxDrawnNodes"], "· polarity drawn", off["polDrawnNodes"], "· six types drawn", off["drawn"])
print("CHIP ON  :", on["shown"], "nodes /", on["shownEdges"], "relations · ux drawn",
      on["uxDrawnNodes"], "· polarity drawn", on["polDrawnNodes"])
print("           six edge types drawn:", json.dumps(on["drawn"]), "TOTAL", sum(on["drawn"].values()))
print("+GOVERNANCE:", both["shown"], "nodes /", both["shownEdges"], "relations")
print("           six edge types drawn:", json.dumps(both["drawn"]), "TOTAL", sum(both["drawn"].values()))
print("in payload: ux", on["uxNodes"], "polarity", on["polNodes"])
print("dig:", dig["ok"], dig.get("id"), "· node carries", dig.get("keys"), "keys ·",
      dig.get("fields"), "of the 10 always-present register fields reach the page")
print("     panel:", " ".join((dig.get("panel") or "").split())[:190])
print()
print("console errors/warnings:", len(errs), errs[:5])
# 111 = every edge of the six types, the 15 declared nulls included (the chip's own badge
# counts them too). The builder's "96 edges + 15 declared nulls" is the same 111 split in two.
print("DRIVE PASS" if (not errs and on["uxDrawnNodes"] == 145 and on["polDrawnNodes"] == 30
                       and sum(both["drawn"].values()) == 111 and off["uxDrawnNodes"] == 0
                       and off["shown"] == 939 and off["famOn"]["uxprinciples"] == 0)
      else "DRIVE FAIL")
