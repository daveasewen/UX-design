"""crops.py — F5: Stat-card and Account-selector on canon-gallery.canon.html, today (root default as HEAD) v the held-back W5a root default, 2x, light."""
import os
from playwright.sync_api import sync_playwright
H=os.environ['HOME']; O=H+'/f5w/notes/_lanes/304/F5/renders'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for side in ('f5','heldback'):
        pg=b.new_page(viewport={"width":1440,"height":900},device_scale_factor=2,reduced_motion="reduce")
        pg.goto('file://%s/f5t/%s/knowledge/_fitness-test/canon-gallery.canon.html'%(H,side)); pg.wait_for_timeout(900)
        for sel,nm in (('.cn-stat-card','stat-card'),('.cn-account-selector','account-selector')):
            el=pg.locator(sel).first; el.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
            bb=el.bounding_box(); print(side,nm,bb)
            el.screenshot(path='%s/trim-%s-%s.png'%(O,nm,'today' if side=='f5' else 'heldback'))
        pg.close()
    b.close()
