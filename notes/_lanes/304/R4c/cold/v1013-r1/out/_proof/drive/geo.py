import os, sys, json
from playwright.sync_api import sync_playwright
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
page_name = sys.argv[1]; js = open(sys.argv[2]).read(); w = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': w, 'height': 1000})
    pg.goto('file://' + os.path.join(OUT, page_name)); pg.wait_for_timeout(900)
    print(json.dumps(pg.evaluate(js), indent=1))
    b.close()
