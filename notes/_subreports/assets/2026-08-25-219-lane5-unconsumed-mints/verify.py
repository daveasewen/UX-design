#!/usr/bin/env python3
"""NON-REPO probe (s191-D2 declared) — drives reviews/UNCONSUMED-MINTS-2026-08-25-v1.html in a real
browser and reads the page's OWN measurements back out. The page computes contrast/padding from
getComputedStyle; this script only reports what the page produced, plus page errors."""
import sys, json
from playwright.sync_api import sync_playwright

URL = "file:///sessions/pensive-cool-galileo/mnt/UX-design/reviews/UNCONSUMED-MINTS-2026-08-25-v1.html"
MUTATE = "--mutate" in sys.argv

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1280, "height": 1000})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console:%s:%s" % (m.type, m.text)) if m.type == "error" else None)
    pg.goto(URL, wait_until="load")
    if MUTATE:
        # MUTATION ARM: break the projection layer's token name. The "wired" cells must change
        # their reading BY NAME — if they do not, the projection was never driving anything.
        pg.add_style_tag(content=".proj .cn-tabs .tab{color:var(--gate-mutant-void)!important;}"
                                 ".proj .cn-cards .card.opt{padding:var(--gate-mutant-void)!important;}")
        pg.evaluate("""() => document.querySelectorAll('.cell').forEach(c => {
            const s=c.querySelector('.stage'), o=c.querySelector('.readout');
            if (s.querySelector('.tab')) meterTab(s,o); else meterPad(s,o); })""")
    pg.wait_for_timeout(700)
    rows = pg.evaluate("""() => [...document.querySelectorAll('.cell')].map(c => ({
        cap: c.querySelector('.cap').innerText.replace(/\\n/g,' | '),
        read: c.querySelector('.readout').innerText.replace(/\\n/g,' ')}))""")
    n_measuring = sum(1 for r in rows if "measuring" in r["read"])
    print("URL: %s   MUTATE=%s" % (URL, MUTATE))
    print("cells: %d   still-unmeasured: %d   page errors: %d" % (len(rows), n_measuring, len(errs)))
    for e in errs[:8]:
        print("   ERROR", e[:160])
    for r in rows:
        print("  %-42s %s" % (r["cap"], r["read"]))
    if not MUTATE:
        pg.screenshot(path="/var/tmp/s219l5/unconsumed-mints.png", full_page=True)
        print("shot: /var/tmp/s219l5/unconsumed-mints.png")
    b.close()
    sys.exit(1 if (n_measuring or errs) else 0)
