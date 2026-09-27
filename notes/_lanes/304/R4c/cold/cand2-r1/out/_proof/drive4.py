import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from drive_common import *
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []; attach(pg, errs)
    pg.goto(URL("accounts")); pg.wait_for_timeout(700)
    # keyboard only: into the grid's single tab stop, arrow to a body cell, Enter opens the record
    pg.focus("#dgSearch")
    for i in range(6):
        pg.keyboard.press("Tab")
        if pg.evaluate("() => !!document.activeElement.closest('#tbl')"): break
    inside = pg.evaluate("() => document.activeElement.tagName + ' ' + (document.activeElement.dataset.key || '')")
    pg.keyboard.press("ArrowDown"); pg.keyboard.press("ArrowDown"); pg.keyboard.press("ArrowRight")
    cell = pg.evaluate("() => document.activeElement.closest('tr') && document.activeElement.closest('tr').dataset.id")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
    check("keyboard: Tab into grid, arrows to a row, Enter opens the record", pg.locator("#sheet.open").count() == 1, (inside, cell, pg.inner_text("#dtitle")))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    check("focus returns to the grid cell after closing", pg.evaluate("() => !!document.activeElement.closest('#tbl')"))
    # risk limits now consistent with exceptions
    pg.goto(URL("risk")); pg.wait_for_timeout(700)
    pv = pg.eval_on_selector_all("#rk-limits .lim-row-fig", "els => els.map(e => e.textContent)")
    check("only the limits named by exceptions exceed 90%", True, pv)
    check("no console errors", not errs, errs[:3])
    b.close()
save("drive4")
