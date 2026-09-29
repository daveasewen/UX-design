# #308 lane L — the explorer (1.32) with the assets chip on, dug on icon:alert: its defaultActive line to alert-active is drawn.
import os
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); OUT = os.path.join(ROOT, 'notes/_lanes/308/L')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto('file://' + os.path.join(ROOT, 'notes/_KG-EXPLORER.html')); pg.wait_for_timeout(4000)
    before = pg.evaluate("()=>LIVEE.filter(e=>e.type==='defaultActive'&&e.t&&EON(e)).length")
    pg.locator('.chip[data-fam="assets"]').first.click(); pg.wait_for_timeout(1500)
    r = pg.evaluate("""()=>{const all=LIVEE.filter(e=>e.type==='defaultActive');
      const on=all.filter(e=>e.t&&EON(e)).length; setFocus(byId.get('icon:alert')); return [all.length, all.filter(e=>e.t).length, on]}""")
    pg.wait_for_timeout(2500)
    pg.screenshot(path=os.path.join(OUT, 'L-kg-explorer-defaultActive.png'))
    print('defaultActive in page', r[0], '| with a target', r[1], '| drawn with assets chip on', r[2], '| drawn at defaults', before)
    b.close()
