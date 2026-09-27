"""trim_rules.py <page> [selector ...] — W5a: for each selector's FIRST element, list the matched CSS rules that
declare text-box-trim / text-box-edge (CDP CSS.getMatchedStylesForNode), its computed trim, its height, and the
chain of cn- scopes above it. Prints JSON lines; writes nothing."""
import json, os, sys
from playwright.sync_api import sync_playwright
page, sels = sys.argv[1], sys.argv[2:] or ["button.dv-leg-item", "button.dv-leg-item > span"]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg.goto("file://" + os.path.abspath(page)); pg.wait_for_timeout(1500)
    cdp = pg.context.new_cdp_session(pg); cdp.send("DOM.enable"); cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})["root"]["nodeId"]
    for sel in sels:
        nid = cdp.send("DOM.querySelector", {"nodeId": root, "selector": sel})["nodeId"]
        if not nid:
            print(json.dumps({"sel": sel, "found": False})); continue
        m = cdp.send("CSS.getMatchedStylesForNode", {"nodeId": nid})
        rules = []
        for r in m.get("matchedCSSRules", []):
            props = [(q["name"], q["value"]) for q in r["rule"]["style"]["cssProperties"] if q["name"].startswith("text-box")]
            if props:
                sl = r["rule"]["selectorList"]
                matched = [sl["selectors"][i]["text"] for i in r["matchingSelectors"]]
                rules.append({"sel": " || ".join(matched)[:160], "props": props,
                              "line": r["rule"]["style"].get("range", {}).get("startLine")})
        info = pg.evaluate("""(s) => { const e = document.querySelector(s); const cs = getComputedStyle(e);
            const sc = []; for (let a = e; a; a = a.parentElement) for (const c of a.classList) if (c.startsWith('cn-')) sc.push(c);
            return {h: e.getBoundingClientRect().height, trim: cs.textBoxTrim, edge: cs.textBoxEdge, scopes: sc}; }""", sel)
        print(json.dumps({"sel": sel, **info, "rules": rules}))
    b.close()
