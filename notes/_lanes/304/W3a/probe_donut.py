"""W3a probe: donut/legend centre figures across a page's #/ views, before and after a legend click.
Usage: probe_donut.py PAGE [view ...]"""
import os, sys, json
from playwright.sync_api import sync_playwright
page_path = os.path.abspath(sys.argv[1]); views = sys.argv[2:] or [""]
READ = """()=>[...document.querySelectorAll('[data-dv-view="value"] .dv-val')].filter(e=>e.getClientRects().length).map(e=>e.textContent)"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg = b.new_page(viewport={"width":1440,"height":1000})
    for v in views:
        pg.goto("file://" + page_path + (("#/" + v) if v else "")); pg.wait_for_timeout(1200)
        first = pg.evaluate(READ)
        if not first: continue
        clicked = pg.evaluate("""()=>{const f=[...document.querySelectorAll('[data-dv-view="value"] .dv-val')].find(e=>e.getClientRects().length).closest('figure,.dv,[class*=chart]');
          const host=(f&&f.parentElement||document).querySelector('[role=switch],.dv-legend button,[aria-checked]'); if(host){host.click();return host.textContent.trim().slice(0,30);} return null;}""")
        pg.wait_for_timeout(500)
        print(json.dumps({"view": v or "(entry)", "centre": first, "clicked": clicked, "after_click": pg.evaluate(READ)}))
    b.close()
