"""#305 B5: drives the decisions bar once at the seat: tick a chip, type in a compact row, reload (state survives),
then Copy as text (clipboard read back), then clear the browser's store. Run from the repo root, env sourced."""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); OUT = os.path.join(ROOT, 'notes/_lanes/305/B5/drive'); os.makedirs(OUT, exist_ok=True)
PAGE = 'file://' + os.path.join(ROOT, 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': 1440, 'height': 1000})
    try: ctx.grant_permissions(['clipboard-read', 'clipboard-write'])
    except Exception as e: print('grant:', e)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(PAGE); pg.wait_for_timeout(400)
    print('before:', pg.inner_text('#dd-count'))
    pg.locator('#g1-ring-r1 .dd-chip[data-v="Agree: fails"]').click()
    pg.locator('#wr-footer textarea[data-f="decision"]').fill('drive test: accept')
    pg.reload(); pg.wait_for_timeout(400)
    on = pg.evaluate("() => [...document.querySelectorAll('.dd-chip.on')].map(c => c.closest('.dd-box').dataset.id + '=' + c.dataset.v)")
    val = pg.input_value('#wr-footer textarea[data-f="decision"]')
    print('after reload:', pg.inner_text('#dd-count'), on, repr(val))
    pg.click('#dd-copy'); pg.wait_for_timeout(400)
    print('msg:', pg.inner_text('#dd-msg'))
    try: clip = pg.evaluate("() => navigator.clipboard.readText()")
    except Exception as e: clip = 'CLIPBOARD READ FAILED: %s' % e
    open(os.path.join(OUT, 'copy-as-text.md'), 'w').write(clip)
    print('clipboard chars:', len(clip)); print(clip[:900])
    pg.screenshot(path=os.path.join(OUT, 'after-drive.png'))
    pg.evaluate("() => localStorage.clear()")
    print('pageerrors:', errs); b.close()
