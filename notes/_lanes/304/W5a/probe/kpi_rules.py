"""kpi_rules.py <page> — W5a: first Kpi-tile's height, its spark's height and every matched rule declaring
height on the spark (CDP), plus the cn- scope chain. Writes nothing."""
import json, os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg.goto("file://" + os.path.abspath(sys.argv[1])); pg.wait_for_timeout(1500)
    cdp = pg.context.new_cdp_session(pg); cdp.send("DOM.enable"); cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})["root"]["nodeId"]
    for sel in (".kpi-tile .spark-inline", ".kpi-tile .kpi-lbl"):
        nid = cdp.send("DOM.querySelector", {"nodeId": root, "selector": sel})["nodeId"]
        if not nid: print(sel, "none"); continue
        m = cdp.send("CSS.getMatchedStylesForNode", {"nodeId": nid})
        rules = [{"sel": " || ".join(r["rule"]["selectorList"]["selectors"][i]["text"] for i in r["matchingSelectors"])[:110],
                  "props": [(q["name"], q["value"]) for q in r["rule"]["style"]["cssProperties"] if q["name"] in ("height", "text-box-trim", "text-box-edge", "line-height")],
                  "line": r["rule"]["style"].get("range", {}).get("startLine")} for r in m.get("matchedCSSRules", [])]
        rules = [r for r in rules if r["props"]]
        info = pg.evaluate("""(s) => { const e = document.querySelector(s); const t = e.closest('.kpi-tile');
          const sc = []; for (let a = e; a; a = a.parentElement) for (const c of a.classList) if (c.startsWith('cn-')) sc.push(c);
          return {h: e.getBoundingClientRect().height, tile: t.getBoundingClientRect().height, scopes: sc}; }""", sel)
        print(json.dumps({"sel": sel, **info, "rules": rules}))
    b.close()
