import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/v1013-r3/out')
PAGES = ['index','accounts','liquidity','payments','fx','risk','trade','reports','messages','settings']
JS = open(os.path.expanduser('~/cold/v1013-r3/tools/geosweep.js')).read()
vw = int(sys.argv[1]) if len(sys.argv) > 1 else 1440; theme = sys.argv[2] if len(sys.argv) > 2 else 'light'
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': vw, 'height': 900})
    ctx.add_init_script("localStorage.setItem('apollo-ceo-proto-v1', JSON.stringify({theme:'%s'}))" % theme)
    for n in PAGES:
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)[:200])); pg.on('console', lambda m, errs=errs: errs.append(m.text[:200]) if m.type == 'error' else None)
        pg.goto('file://' + W + '/' + n + '.html'); pg.wait_for_timeout(900)
        r = pg.evaluate(JS); r['errors'] = errs; res[n] = r; pg.close()
    b.close()
out = os.path.expanduser('~/cold/v1013-r3/proof/geo-%d-%s.json' % (vw, theme)); json.dump(res, open(out, 'w'), indent=1)
for n, r in res.items():
    print(n, 'err=%d' % len(r['errors']), 'hscroll=%s' % r['hscroll'], 'align=%s' % r['align'], 'navFit=%s' % r['navFit'], 'labelOverlaps=%s' % r['labelOverlaps'], 'textClip=%s' % r['textClip'][:3], 'small=%s' % r['smallTargets'][:3], 'tileGap=%s' % r['tileGaps'], 'pad=%s' % r['tilePad'])
