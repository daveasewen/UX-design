# #308 lane L — one render per changed surface: the Common label on the pickers, and the explorer's defaultActive lines.
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); OUT = os.path.join(ROOT, 'notes/_lanes/308/L')
which = sys.argv[1:] or ['tree', 'index', 'bento']
pages = {'tree': 'showroom/tree.html', 'index': 'showroom/index.html', 'bento': 'showroom/_foundations/bento.html'}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for k in which:
        pg = b.new_page(viewport={'width': 1280, 'height': 800})
        pg.goto('file://' + os.path.join(ROOT, pages[k])); pg.wait_for_timeout(1200)
        sel = '#themes button[data-theme="legacy"], #themes button[data-theme-attr="legacy"]'
        btn = pg.locator(sel).first
        txt = btn.inner_text(); btn.click(); pg.wait_for_timeout(900)
        att = pg.evaluate("()=>[document.documentElement.getAttribute('data-apollo-theme'), (document.getElementById('meta')||{}).textContent||'']")
        pg.screenshot(path=os.path.join(OUT, 'L-%s-common.png' % k), clip={'x': 0, 'y': 0, 'width': 1280, 'height': 420})
        print(k, 'button reads', repr(txt), '| html data-apollo-theme after click', att[0], '| meta', att[1][:60])
        pg.close()
    b.close()
