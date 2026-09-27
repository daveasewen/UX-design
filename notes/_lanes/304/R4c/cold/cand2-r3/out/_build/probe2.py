import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand2-r3')
pages = sys.argv[1].split(','); js = open(sys.argv[2]).read(); vw = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
theme = sys.argv[4] if len(sys.argv) > 4 else None
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    ctx = b.new_context(viewport={'width': vw, 'height': 1000})
    for pg in pages:
        page = ctx.new_page(); errs = []
        page.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
        page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
        page.goto('file://' + W + '/out/' + pg + '.html' + ('?theme=' + theme if theme else '')); page.wait_for_timeout(900)
        res = page.evaluate(js)
        print(json.dumps({'page': pg, 'errors': errs[:10], 'res': res}))
        page.close()
    b.close()
