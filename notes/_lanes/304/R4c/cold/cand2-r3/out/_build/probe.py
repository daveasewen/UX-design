import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand2-r3/out')
pages = sys.argv[1].split(',') if len(sys.argv) > 1 else ['index']
js = sys.argv[2] if len(sys.argv) > 2 else "() => document.title"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    ctx = b.new_context(viewport={'width': 1600, 'height': 1000})
    for pg in pages:
        page = ctx.new_page(); errs = []
        page.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
        page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
        page.goto('file://' + W + '/' + pg + '.html'); page.wait_for_timeout(700)
        try: res = page.evaluate(js)
        except Exception as e: res = 'EVAL-ERR ' + str(e)[:300]
        print(json.dumps({'page': pg, 'errors': errs[:12], 'res': res})[:6000])
        page.close()
    b.close()
