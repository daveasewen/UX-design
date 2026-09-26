"""Driven, part 3: does every chart, KPI and grid move with each shared filter (rule 14)? Plus
keyboard-only dropdown use, and a phone-width pass (menu sheet, no horizontal scroll)."""
import os, json
from playwright.sync_api import sync_playwright
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
U = lambda n: 'file://' + os.path.join(OUT, n)
PAGES = ['index', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
SNAP = """() => ({charts: Object.fromEntries([...document.querySelectorAll('figure.dv')].map(f=>[f.id, (f.querySelector('table.dv-table')||{}).textContent || ''])),
  kpis: [...document.querySelectorAll('.kpi-tile .amt')].map(e=>e.textContent).join('|'), grids: Object.fromEntries([...document.querySelectorAll('.dg')].map(d=>[d.id, document.getElementById(d.id+'-count').textContent]))})"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': 1600, 'height': 1000}); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(U('index.html')); pg.evaluate('localStorage.clear()')
    for n in PAGES:
        snaps = {}
        for label, q in [('base', ''), ('region', '?region=ap'), ('entity', '?entity=HLU'), ('days', '?days=7')]:
            pg.evaluate('localStorage.clear()'); pg.goto(U(n + '.html') + q); pg.wait_for_timeout(350)
            snaps[label] = pg.evaluate(SNAP)
        row = {}
        for f in ('region', 'entity', 'days'):
            same = [c for c in snaps['base']['charts'] if snaps[f]['charts'].get(c) == snaps['base']['charts'][c]]
            row[f] = {'charts_unchanged': same, 'kpis_changed': snaps[f]['kpis'] != snaps['base']['kpis'], 'grids': {g: snaps['base']['grids'][g] + ' -> ' + snaps[f]['grids'].get(g, '') for g in snaps['base']['grids']}}
        res[n] = row; print(n, json.dumps(row))
    # keyboard-only: open the region menu with Enter, arrow to an option, Enter selects, focus returns
    pg.evaluate('localStorage.clear()'); pg.goto(U('index.html')); pg.wait_for_timeout(400)
    pg.focus('#dd-region-t'); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    f1 = pg.evaluate("document.activeElement.getAttribute('data-value')")
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('ArrowDown'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
    kb = {'focusedOnOpen': f1, 'regionNow': pg.evaluate("new URLSearchParams(location.search).get('region')"), 'focusBack': pg.evaluate("document.activeElement.id")}
    pg.focus('#dd-days-t'); pg.keyboard.press('Enter'); pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    kb['escapeCloses'] = pg.get_attribute('#dd-days-m', 'data-open') == 'false' and pg.evaluate("document.activeElement.id") == 'dd-days-t'
    print('KEYBOARD', json.dumps(kb))
    # phone width
    ph = b.new_context(viewport={'width': 390, 'height': 844}).new_page(); ph.on('pageerror', lambda e: errs.append(str(e)))
    out = {}
    for n in PAGES:
        ph.goto(U(n + '.html')); ph.wait_for_timeout(300)
        out[n] = ph.evaluate("({docH: document.documentElement.scrollWidth > document.documentElement.clientWidth, content: document.querySelector('.sh-content').scrollWidth > document.querySelector('.sh-content').clientWidth, nav: getComputedStyle(document.querySelector('.sh-body > .sn')).display})")
    ph.goto(U('index.html')); ph.wait_for_timeout(300); ph.click('[data-menu="shell"]'); ph.wait_for_timeout(300)
    out['sheetOpens'] = ph.evaluate("document.getElementById('sheet').classList.contains('open') && getComputedStyle(document.getElementById('sheet')).visibility === 'visible'")
    print('PHONE', json.dumps(out)); print('ERRORS', errs)
    b.close()
json.dump({'filters': res, 'keyboard': kb, 'phone': out, 'errors': errs}, open(os.path.join(OUT, '_proof', 'drive', 'drive3.json'), 'w'), indent=1)
