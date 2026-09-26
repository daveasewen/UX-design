import os, sys, json
from playwright.sync_api import sync_playwright
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PAGES = ['index', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
w = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
theme = sys.argv[2] if len(sys.argv) > 2 else 'light'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': w, 'height': 1000})
    pg = ctx.new_page()
    for name in PAGES:
        errs = []
        pg.on('console', lambda m, errs=errs: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        pg.goto('file://' + os.path.join(OUT, name + '.html'))
        if theme == 'dark':
            pg.click('[data-theme-btn="dark"]')
        pg.wait_for_timeout(700)
        r = pg.evaluate('''() => ({figs:[...document.querySelectorAll('figure.dv')].map(f=>{const s=f.querySelector('svg.dv-svg');const b=s.getBoundingClientRect();return f.id+':'+s.querySelectorAll('[data-tip]').length+':'+Math.round(b.width)+'x'+Math.round(b.height)+(f.querySelector('.ceo-empty')?':EMPTY':'')}),
          kpis:[...document.querySelectorAll('.kpi-tile .amt')].map(e=>e.textContent).join(' | '), grids:[...document.querySelectorAll('.dg')].map(d=>d.id+':'+d.querySelectorAll('tbody tr').length+':'+document.getElementById(d.id+'-count').textContent),
          hscroll: document.querySelector('.sh-content').scrollWidth > document.querySelector('.sh-content').clientWidth,
          wide:[...document.querySelectorAll('.c-bento__tile')].filter(t=>t.scrollWidth>t.clientWidth+1).map(t=>(t.id||t.className.slice(0,30))+':'+t.scrollWidth+'>'+t.clientWidth)})''')
        print(name, json.dumps(r)); print('   ERR', errs[:6])
        pg.remove_listener('console', pg.listeners('console')[0]) if hasattr(pg, 'listeners') else None
    b.close()
