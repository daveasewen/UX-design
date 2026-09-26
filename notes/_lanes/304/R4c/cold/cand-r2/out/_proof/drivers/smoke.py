import os, json, sys
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand-r2'); URL = 'file://' + W + '/out/index.html'
out = {'console': [], 'pageerrors': []}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()
    pg.on('console', lambda m: out['console'].append([m.type, m.text[:300]]) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: out['pageerrors'].append(str(e)[:400]))
    pg.goto(URL); pg.wait_for_timeout(1200)
    views = ['overview','accounts','liquidity','payments','fx','risk','trade','reports','messages','settings']
    res = {}
    for v in views:
        pg.evaluate("v => { location.hash = '#/' + v; }", v); pg.wait_for_timeout(500)
        res[v] = pg.evaluate("""v => { const sec = document.querySelector('.app-view[data-view="'+v+'"]');
          const figs=[...sec.querySelectorAll('figure.dv')].map(f=>({k:f.dataset.chart, marks:f.querySelectorAll('svg.dv-svg [data-tip]').length, empty:f.dataset.empty||'', w:Math.round(f.getBoundingClientRect().width)}));
          const grids=[...sec.querySelectorAll('.dg')].map(g=>({k:g.dataset.grid, rows:g.querySelectorAll('tbody tr').length, count:g.querySelector('.dg-count').textContent}));
          return {hidden: sec.hidden, figs, grids, title: document.querySelector('.ph-title').textContent}; }""", v)
    pg.screenshot(path=W + '/proof/smoke-settings.png')
    print(json.dumps(res, indent=0)[:6000])
    print(json.dumps(out, indent=0)[:3000])
    b.close()
