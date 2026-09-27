"""Smoke drive: load every page at 1440x900 in light and dark, collect console errors and page
errors, count drawn charts / grid rows / list rows. usage: python3 smoke.py <out-dir> [page ...]"""
import json, os, sys
from playwright.sync_api import sync_playwright

OUT = os.path.abspath(sys.argv[1])
PAGES = sys.argv[2:] or ['index', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
PROBE = """() => {
  const figs = [...document.querySelectorAll('figure.dv')].map(f => ({id: f.id, marks: f.querySelectorAll('svg.dv-svg > *').length,
     w: Math.round(f.getBoundingClientRect().width), rows: f.querySelectorAll('table.dv-table tbody tr').length, empty: f.hasAttribute('data-empty')}));
  return {theme: document.documentElement.getAttribute('data-theme'), figs,
    kpis: [...document.querySelectorAll('.kpi-tile')].map(k => k.querySelector('.kpi-val').textContent.trim()),
    gridRows: document.querySelectorAll('#tbody tr[data-id]').length, gridCount: (document.getElementById('dgCount')||{}).textContent,
    listRows: [...document.querySelectorAll('ul.list')].map(u => u.id + ':' + u.children.length),
    font: getComputedStyle(document.body).fontFamily.slice(0, 40)};
}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    res = {}
    for pg in PAGES:
        for theme in ('light', 'dark'):
            ctx = b.new_context(viewport={'width': 1440, 'height': 900})
            page = ctx.new_page(); errs = []
            page.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text[:300]) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:300]))
            page.goto('file://%s/%s.html?theme=%s' % (OUT, pg, theme)); page.wait_for_timeout(900)
            r = page.evaluate(PROBE); r['errors'] = errs
            res[pg + ':' + theme] = r
            ctx.close()
    b.close()
for k, r in res.items():
    bad = [f['id'] for f in r['figs'] if f['marks'] == 0]
    print(k, '| theme', r['theme'], '| figs', len(r['figs']), 'undrawn', bad, '| kpis', r['kpis'], '| grid', r['gridRows'], r['gridCount'], '| lists', r['listRows'], '| errors', len(r['errors']))
    for e in r['errors'][:6]:
        print('    ', e)
json.dump(res, open(os.path.join(os.path.dirname(OUT), 'proof', 'smoke.json'), 'w'), indent=1)
