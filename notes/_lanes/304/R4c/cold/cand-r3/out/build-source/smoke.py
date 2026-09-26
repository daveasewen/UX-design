import os, json, sys, time
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand-r3'); URL = 'file://' + W + '/out/index.html'
VIEWS = ['overview', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
width = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': width, 'height': 900})
    errs = []
    pg.on('console', lambda m: errs.append(('console.' + m.type, m.text)) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(('pageerror', str(e))))
    pg.goto(URL + '#/overview'); pg.wait_for_timeout(1200)
    out = {}
    for v in VIEWS:
        pg.evaluate("h => location.hash = h", '#/' + v); pg.wait_for_timeout(900)
        out[v] = pg.evaluate("""v => { const s = document.querySelector('.ceo-view[data-view="'+v+'"]');
          const figs = [...s.querySelectorAll('[data-chart]')].map(slot => { const f = slot.querySelector('figure');
            const svg = f && f.querySelector('svg.dv-svg'); const r = svg && svg.getBoundingClientRect();
            return [slot.getAttribute('data-chart'), f ? f.getAttribute('data-dv-type') : null, svg ? svg.querySelectorAll('.dv-series').length : 0, r ? Math.round(r.width)+'x'+Math.round(r.height) : null]; });
          const kpis = [...s.querySelectorAll('[data-kpi]')].map(k => [k.getAttribute('data-kpi'), k.querySelector('.kpi-val').textContent, k.querySelector('.kpi-delta').textContent]);
          const grids = [...s.querySelectorAll('.dg')].map(g => [g.id, g.querySelectorAll('tbody tr').length, (g.querySelector('.dg-range')||{}).textContent]);
          return {figs, kpis, grids, h1: document.getElementById('page-h1').textContent}; }""", v)
    json.dump({'errors': errs, 'views': out}, open(W + '/proof/smoke-%d.json' % width, 'w'), indent=1)
    print('ERRORS', len(errs)); [print(e) for e in errs[:30]]
    for v in VIEWS:
        o = out[v]; print('##', v, o['h1']); print('  figs', o['figs']); print('  kpis', o['kpis']); print('  grids', o['grids'])
    b.close()
