"""Ad-hoc DOM probe: python3 probe.py <page.html> <width> "<js expression returning JSON-able>" """
import json, os, sys
from playwright.sync_api import sync_playwright
page_path, width, expr = sys.argv[1], int(sys.argv[2]), sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': width, 'height': 900})
    pg.goto('file://' + os.path.abspath(page_path)); pg.wait_for_timeout(900)
    print(json.dumps(pg.evaluate(expr), indent=0)[:6000])
    b.close()
