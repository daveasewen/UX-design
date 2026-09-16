"""#277 lane LL — drive notes/_KG-EXPLORER.html (v1.14) once, after the land.

Proves, in the real page: 0 console errors/warnings/pageerrors; the version string is v1.14;
the "Guideline rules" chip exists, is OFF at first paint, and turning it on (the REAL chip,
clicked, never `famOn` poked) draws the rules family. s277-D1..D3 put 87 `edges.obeys` entries
on the four chart metas — the explorer does NOT yet read `edges.obeys` (the gap #276 declared
and s277 did not ask to close), so the corpus count is read off the metas on disk INSIDE this
drive and asserted 168 (81 before the land), next to the page bites, rather than pretended
to be a page fact.

  source knowledge/_render/seat_env.sh && python3 notes/_lanes/277/land/_drive_explorer.py
"""
import glob, json, os, pathlib
from playwright.sync_api import sync_playwright

REPO = os.environ.get("RENDER_REPO") or str(pathlib.Path(__file__).resolve().parents[4])
PAGE = "file://" + REPO + "/notes/_KG-EXPLORER.html"
OUT = REPO + "/notes/_lanes/277/land"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

# --- the corpus fact, measured on disk, not on the page ---------------------
CHART = ("chart-line", "chart-pie", "chart-bar", "chart-donut")
obeys_total, obeys_metas, obeys_chart = 0, 0, {}
for p in sorted(glob.glob(REPO + "/knowledge/components/*.meta.json")):
    o = json.loads(pathlib.Path(p).read_text(encoding="utf-8")).get("edges", {}).get("obeys")
    if o:
        obeys_total += len(o); obeys_metas += 1
        stem = pathlib.Path(p).name[:-len(".meta.json")]
        if stem in CHART:
            obeys_chart[stem] = len(o)
whys_ok = all(len(e["$why"]) >= 40
              for p in glob.glob(REPO + "/knowledge/components/*.meta.json")
              for e in json.loads(pathlib.Path(p).read_text(encoding="utf-8")).get("edges", {}).get("obeys", []))

STATE = """()=>{
  const ids=new Set(NODES.map(n=>n.id));
  return {version:(document.querySelector('.brand span')||{}).innerText,
          chipExists:!!document.querySelector('[data-fam="guidelinerules"]'),
          famOn:JSON.parse(JSON.stringify(famOn)),
          scNodes:NODES.filter(n=>String(n.id).startsWith('sc:')).length,
          ruleNodes:NODES.filter(n=>String(n.id).startsWith('rule:')).length,
          chartNodes:NODES.filter(n=>['component:chart-line','component:chart-pie','component:chart-bar','component:chart-donut'].includes(String(n.id))).length,
          totalNodes:NODES.length, totalEdges:LIVEE.length,
          drawnNodes:(typeof SHOWN!=='undefined')?SHOWN.length:null};
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
    pg.click('[data-fam="guidelines"]')
    pg.wait_for_timeout(1800)
    pg.evaluate(SETTLE); pg.wait_for_timeout(300)
    pg.click("text=Fit"); pg.wait_for_timeout(1200)
    pg.evaluate(SETTLE); pg.wait_for_timeout(300)
    on = pg.evaluate(STATE)
    pg.screenshot(path=OUT + "/screenshot-explorer-rules-on.png")
    b.close()

bites = [
    ("version string is v1.14 (v1.13 before the land)", "1.14" in str(off["version"])),
    ("the Guideline rules chip exists", off["chipExists"]),
    ("the chip is OFF at first paint", not off["famOn"].get("guidelinerules")),
    ("clicking the REAL chip turns the rules family on", bool(on["famOn"].get("guidelinerules"))),
    ("the guidelines chip turns on too", bool(on["famOn"].get("guidelines"))),
    ("the rules family draws with the chip on", (on["drawnNodes"] or 0) > (off["drawnNodes"] or 0)),
    ("rule: nodes 470 (unmoved — this land mints no rule node)", off["ruleNodes"] == 470),
    ("sc: nodes 55 (unmoved — this land mints no criterion)", off["scNodes"] == 55),
    ("all four chart components are in the graph", off["chartNodes"] == 4),
    ("corpus edges.obeys = 168 (81 before the land, +87)", obeys_total == 168),
    ("edges.obeys now on 10 metas (6 before the land, +4 charts)", obeys_metas == 10),
    ("the four charts carry 24/25/27/11 = 87",
     obeys_chart == {"chart-line": 24, "chart-pie": 25, "chart-bar": 27, "chart-donut": 11}),
    ("every $why clears the schema's minLength 40", whys_ok),
    ("0 console errors / warnings / page errors", not errs),
]
for label, okb in bites:
    print(("  ok    " if okb else "  FAIL  ") + label)
print(json.dumps({"off": off, "on": on, "obeys_chart": obeys_chart,
                  "obeys_total": obeys_total, "errors": errs}, indent=1)[:1000])
print("DRIVE PASS" if all(x[1] for x in bites) else "DRIVE FAIL")
