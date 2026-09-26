import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/v1013-r3/out')
pages = sys.argv[1].split(',') if len(sys.argv) > 1 else ['index','accounts','liquidity','payments','fx','risk','trade','reports','messages','settings']
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    for name in pages:
        pg = ctx.new_page(); errs = []
        pg.on('console', lambda m, errs=errs: errs.append(m.type + ': ' + m.text[:300]) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e, errs=errs: errs.append('PAGEERROR: ' + str(e)[:300]))
        pg.goto('file://' + W + '/' + name + '.html'); pg.wait_for_timeout(700)
        info = pg.evaluate('''() => ({charts: [...document.querySelectorAll('figure.dv')].map(f => f.id + ':' + f.querySelectorAll('svg *').length),
          sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})''')
        print(name, 'errors=%d' % len(errs), 'hscroll=%s' % (info['sw'] > info['cw']), info['charts'])
        for e in errs[:8]: print('   ', e)
        pg.close()
    b.close()
