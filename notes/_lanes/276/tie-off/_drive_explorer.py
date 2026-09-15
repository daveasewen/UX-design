"""#276 lane TL — drive notes/_KG-EXPLORER.html (v1.13) once, after the land.

Proves, in the real page: 0 console errors/warnings; the "Guideline rules" chip exists and
is OFF at first paint; clicking the REAL chip (not famOn poked from the console) turns the
family on and draws the 55 sc: nodes (38 before the land) and all 51 `cites` edges — with
ZERO of them landing on a missing target, which is s276-D1/s276-D2 enacted.

  source knowledge/_render/seat_env.sh && python3 notes/_lanes/276/tie-off/_drive_explorer.py
"""
import json, pathlib
from playwright.sync_api import sync_playwright

REPO = "/sessions/stoic-affectionate-cerf/mnt/UX-design"
PAGE = "file://" + REPO + "/notes/_KG-EXPLORER.html"
OUT = REPO + "/notes/_lanes/276/tie-off"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

STATE = """()=>{
  const ids=new Set(NODES.map(n=>n.id));
  const cites=LIVEE.filter(e=>e.type==='cites');
  return {version:(document.querySelector('.brand span')||{}).innerText,
          chipExists:!!document.querySelector('[data-fam="guidelinerules"]'),
          chipLabel:(document.querySelector('[data-fam="guidelinerules"]')||{}).innerText,
          famOn:JSON.parse(JSON.stringify(famOn)),
          scNodes:NODES.filter(n=>String(n.id).startsWith('sc:')).length,
          ruleNodes:NODES.filter(n=>String(n.id).startsWith('rule:')).length,
          cites:cites.length,
          citesUnresolved:cites.filter(e=>!ids.has(e.t)||!e.t).length,
          drawnNodes:(typeof SHOWN!=='undefined')?SHOWN.length:null,
          drawnSc:(typeof SHOWN!=='undefined')?SHOWN.filter(n=>String(n.id).startsWith('sc:')).length:null,
          drawnCites:(typeof SHOWNE!=='undefined')?SHOWNE.filter(e=>e.type==='cites').length:null};
}"""
SETTLE = "()=>{try{spin=false}catch(e){};for(const m of NODES){if(m.tx!==undefined){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}};try{draw()}catch(e){}}"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    errs = []
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text)
          if m.type in ("error", "warning") else None)
    pg.goto(PAGE)
    pg.wait_for_timeout(2500)
    pg.evaluate(SETTLE); pg.wait_for_timeout(300)
    off = pg.evaluate(STATE)
    pg.screenshot(path=OUT + "/screenshot-explorer-chip-off.png")

    pg.click('[data-fam="guidelinerules"]')       # the REAL chip, not famOn poked
    pg.wait_for_timeout(1200)
    # the sc: nodes the 17 criteria minted are built into the GUIDELINES family
    # (_build_kg_explorer.py:305), so the cites edges only become visible with both
    # chips on — this is the pair the ruling is read off, so drive the pair.
    pg.click('[data-fam="guidelines"]')
    pg.wait_for_timeout(1800)
    pg.evaluate(SETTLE); pg.wait_for_timeout(300)
    pg.click("text=Fit"); pg.wait_for_timeout(1200)
    pg.evaluate(SETTLE); pg.wait_for_timeout(300)
    on = pg.evaluate(STATE)
    pg.screenshot(path=OUT + "/screenshot-explorer-rules-on.png")
    b.close()

bites = [
    ("version string is v1.13", "1.13" in str(off["version"])),
    ("the Guideline rules chip exists", off["chipExists"]),
    ("the chip is OFF at first paint", not off["famOn"].get("guidelinerules")),
    ("clicking the REAL chip turns the family on", bool(on["famOn"].get("guidelinerules"))),
    ("the guidelines chip (sc: nodes' family) turns on too", bool(on["famOn"].get("guidelines"))),
    ("all 55 sc: nodes are DRAWN", on["drawnSc"] == 55),
    ("all 51 cites edges are DRAWN — none dropped for a missing target", on["drawnCites"] == 51),
    ("sc: nodes 55 (38 before the land)", off["scNodes"] == 55),
    ("rule: nodes 470", off["ruleNodes"] == 470),
    ("51 cites edges, ZERO unresolved (19 -> 0)", off["cites"] == 51 and off["citesUnresolved"] == 0),
    ("the rules family draws with the chip on", (on["drawnNodes"] or 0) > (off["drawnNodes"] or 0)),
    ("0 console errors / warnings / page errors", not errs),
]
for label, ok in bites:
    print(("  ok    " if ok else "  FAIL  ") + label)
print(json.dumps({"off": off, "on": on, "errors": errs}, indent=1)[:1200])
print("DRIVE PASS" if all(b[1] for b in bites) else "DRIVE FAIL")
