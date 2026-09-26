import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/v1013-r3/out')
name, js = sys.argv[1], sys.argv[2]
vw = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': vw, 'height': 900})
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200])); pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
    pg.goto('file://' + W + '/' + name + '.html'); pg.wait_for_timeout(600)
    print(json.dumps(pg.evaluate(js), indent=0)[:4000]); print('errors', errs)
    b.close()
