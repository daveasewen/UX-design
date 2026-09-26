"""Quick load probe: console errors, chart fill, horizontal overflow. Usage: probe.py page.html [w h] [theme]"""
import os, sys, json
from playwright.sync_api import sync_playwright
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
page_name = sys.argv[1]; w = int(sys.argv[2]) if len(sys.argv) > 2 else 1600; h = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': w, 'height': h})
    errs = []
    pg.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.goto('file://' + os.path.join(OUT, page_name)); pg.wait_for_timeout(900)
    r = pg.evaluate('''() => {
      const figs=[...document.querySelectorAll('figure.dv')].map(f=>{const s=f.querySelector('svg.dv-svg'); const b=s? s.getBoundingClientRect():null;
        return {id:f.id, type:f.dataset.dvType, marks:s? s.querySelectorAll('.dv-series, [data-tip]').length:0, w:b?Math.round(b.width):0, h:b?Math.round(b.height):0, rows:f.querySelectorAll('table.dv-table tbody tr').length}});
      const doc=document.documentElement; const sc=document.querySelector('.sh-content');
      const over=[...document.querySelectorAll('.c-bento__tile, figure, table, .dg')].filter(e=>e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflowX==='visible').map(e=>(e.id||e.className).toString().slice(0,50)+':'+e.scrollWidth+'>'+e.clientWidth).slice(0,10);
      return {title:document.title, figs, kpis:[...document.querySelectorAll('.kpi-tile .amt')].map(e=>e.textContent), hscroll: sc? sc.scrollWidth>sc.clientWidth : null, over,
        theme: doc.dataset.theme, groundBg: getComputedStyle(document.querySelector('.ceo-ground')).backgroundColor, headBg: getComputedStyle(document.querySelector('.ceo-head')).backgroundColor,
        tileBg: (()=>{const t=document.querySelector('.stat-card, .kpi-tile'); return t? getComputedStyle(t).backgroundColor:null})()};
    }''')
    print(json.dumps(r, indent=1)); print('ERRORS:', json.dumps(errs, indent=1))
    pg.screenshot(path=os.path.join(OUT, '_proof', 'drive', page_name.replace('.html', '') + '-%dx%d.png' % (w, h)), full_page=False)
    b.close()
