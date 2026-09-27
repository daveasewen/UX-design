"""#305 B4: drives the decisions bar on both pages at the seat: tick/type, reload (state survives), export."""
import os, sys, subprocess
subprocess.check_call([sys.executable, 'notes/_lanes/305/B4/build.py'])
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); out = os.path.join(ROOT, 'notes/_lanes/305/B4/drive'); os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL']); ctx = b.new_context(accept_downloads=True)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + ROOT + '/notes/_SCAN-305-parked-questions-2026-09-27-v1.html'); pg.wait_for_timeout(400)
    pg.locator('#flags input[data-k="W-206"]').check(); pg.locator('input[data-k="W-63"]').check()
    pg.locator('textarea[data-g="T6"]').fill('drive test note'); pg.reload(); pg.wait_for_timeout(400)
    both = pg.evaluate("() => [...document.querySelectorAll('input[data-k=\"W-206\"]')].map(i=>i.checked)")
    print('scan: W-206 ticked in both places after reload:', both, '| count:', pg.inner_text('#dd-count'))
    with pg.expect_download() as d: pg.click('#dd-dl')
    d.value.save_as(os.path.join(out, 'scan-export.md')); pg.click('#dd-copy'); pg.wait_for_timeout(200); print('msg:', pg.inner_text('#dd-msg'))
    pg.evaluate("() => localStorage.clear()")
    pg2 = ctx.new_page(); pg2.on('pageerror', lambda e: errs.append(str(e)))
    pg2.goto('file://' + ROOT + '/notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html'); pg2.wait_for_timeout(400)
    pg2.locator('#call27-a .dd-chip[data-v="Inscribe"]').click(); pg2.locator('#call27-b textarea[data-f="decision"]').fill('drive test decision')
    pg2.reload(); pg2.wait_for_timeout(400); print('review count:', pg2.inner_text('#dd-count'))
    with pg2.expect_download() as d: pg2.click('#dd-dl')
    d.value.save_as(os.path.join(out, 'review-export.md'))
    pg2.evaluate("() => localStorage.clear()")
    print('pageerrors:', errs); b.close()
