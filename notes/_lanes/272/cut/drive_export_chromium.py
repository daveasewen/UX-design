import json, os, pathlib
from playwright.sync_api import sync_playwright
ROOT = "/sessions/confident-clever-ritchie/mnt/UX-design"
PAGE = pathlib.Path(ROOT, "notes/_REVIEW-when-harvest-whole-library-2026-09-14-v2.html").as_uri()
OUT  = os.path.join(ROOT, "notes/_lanes/272/cut/synthetic-export-B-driven.json")

# 3 decided non-unanimous (one lane-B row, to prove the B-id family is carried), 1 unanimous, 1 later
PLAN = [
    ("R-A-01", "option", "3", "one primary per layout region, that is the one our own gate can walk"),
    ("B-01",   "ratify", None, "180 was decided because we use a sub for the wrap"),
    ("N-tags-input", "ratify", None, ""),          # NOTE-ABSENT + guess-source
    ("U-alert", "ratify", None, "yep like it"),
    ("R1",     "later",  None, "not yet"),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1280,"height":900})
    errs=[]; pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.goto(PAGE); pg.wait_for_timeout(600)
    pg.evaluate("localStorage.removeItem('apollo-harvest-271-v2')")
    pg.reload(); pg.wait_for_timeout(600)
    for rid, dec, idx, note in PLAN:
        tb = pg.locator(f'tbody.row[data-rid="{rid}"]')
        assert tb.count()==1, f"{rid} not found on the page ({tb.count()})"
        sel = f'.db[data-v="{dec}"]' + (f'[data-i="{idx}"]' if idx else ':not([data-i])')
        btn = tb.locator(sel).first
        btn.scroll_into_view_if_needed(); btn.click()
        if note:
            ta = tb.locator("textarea.dnote").first
            ta.click(); ta.fill(note); ta.blur()
        pg.wait_for_timeout(60)
    pg.wait_for_timeout(300)
    # reload to prove persistence, then export THROUGH THE PAGE'S OWN BUTTON
    pg.reload(); pg.wait_for_timeout(700)
    pg.locator("#btnExport").click(); pg.wait_for_timeout(600)
    js = pg.locator("#expjson").input_value()
    obj = json.loads(js)
    open(OUT,"w").write(json.dumps(obj, indent=2, ensure_ascii=False)+"\n")
    print("EXPORTED (via the page's own Export button, after a reload):", sorted(obj))
    print("console errors:", errs[:5] or "none")
    b.close()
