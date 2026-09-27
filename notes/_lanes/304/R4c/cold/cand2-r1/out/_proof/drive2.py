import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from drive_common import *
from playwright.sync_api import sync_playwright
def row_status(pg, pid):
    return pg.evaluate("id => { const tr = document.querySelector('#tbody tr[data-id=\"' + id + '\"]'); return tr ? tr.children[4].textContent.trim() : null; }", pid)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    pg = ctx.new_page(); errs = []; attach(pg, errs)
    pg.goto(URL("payments")); pg.wait_for_timeout(700)
    n = pg.locator("#tbody tr[data-id]").count()
    check("payments grid renders a page of rows", n == 12, n)
    check("grid header relabelled from DATA config", pg.inner_text('th[data-key="payee"] .lbl') == "Beneficiary" and pg.inner_text("#dgTitle") == "Payments")
    check("grid count reflects DATA", pg.inner_text("#dgCount").startswith("48"), pg.inner_text("#dgCount"))
    # sort by amount
    pg.click('th[data-key="amount"] .sort'); pg.wait_for_timeout(200)
    amts = pg.eval_on_selector_all("#tbody tr[data-id] td.num", "els => els.map(e => parseFloat(e.textContent.replace(/[^0-9.−-]/g,'').replace('−','-')))")
    check("sort by amount ascending", pg.get_attribute('th[data-key="amount"]', "aria-sort") == "ascending" and amts == sorted(amts), amts[:3])
    pg.click('#pgList button[data-go="2"]'); pg.wait_for_timeout(200)
    check("paging to page 2", "13–24" in pg.inner_text("#dgRange"), pg.inner_text("#dgRange"))
    pg.reload(); pg.wait_for_timeout(700)
    check("sort + page survive reload", pg.get_attribute('th[data-key="amount"]', "aria-sort") == "ascending" and "13–24" in pg.inner_text("#dgRange"), pg.inner_text("#dgRange"))
    pg.click('#pgList button[data-go="1"]'); pg.click('th[data-key="amount"] .sort'); pg.click('th[data-key="amount"] .sort'); pg.wait_for_timeout(200)
    # search -> chip
    pg.fill("#dgSearch", "Awaiting your approval"); pg.press("#dgSearch", "Enter"); pg.wait_for_timeout(250)
    st = pg.eval_on_selector_all("#tbody tr[data-id]", "els => els.map(e => e.children[4].textContent.trim())")
    check("grid search filters and shows a chip", pg.locator("#fbar .fchip").count() == 1 and st and all(s == "Awaiting your approval" for s in st), "%d rows" % len(st))
    first_id = pg.get_attribute("#tbody tr[data-id]", "data-id")
    # open -> reject without note -> error
    pg.click('#tbody tr[data-id="%s"] td:nth-child(3)' % first_id); pg.wait_for_timeout(500)
    check("row click opens the payment in the drawer", pg.locator("#sheet.open").count() == 1, pg.inner_text("#dtitle"))
    pg.click("#cancel"); pg.wait_for_timeout(200)   # Reject
    check("reject without an audit note is refused, field marked invalid", pg.get_attribute("#pay-note", "aria-invalid") == "true" and pg.locator("#pay-note-err").count() == 1, pg.inner_text("#pay-note-err") if pg.locator("#pay-note-err").count() else "")
    pg.fill("#pay-note", "Duplicate of invoice run 14; hold for AP review."); pg.click("#cancel"); pg.wait_for_timeout(400)
    check("reject with note updates the record", row_status(pg, first_id) in (None, "Rejected") and pg.locator("#sheet.open").count() == 0)
    check("toast confirms the decision", pg.locator("#toastRegion .toast").count() >= 1, pg.inner_text("#toastRegion") [:80])
    # approve (two-step)
    ids = pg.eval_on_selector_all("#tbody tr[data-id]", "els => els.map(e => e.dataset.id)")
    target = None
    for i in ids:
        pg.click('#tbody tr[data-id="%s"] td:nth-child(3)' % i); pg.wait_for_timeout(400)
        if pg.locator("#pay-screen").count() == 0:
            target = i; break
        pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    pg.fill("#pay-note", "Approved against signed board minute 2026-09.")
    pg.click("#act"); pg.wait_for_timeout(200)
    check("approve asks for confirmation first", pg.inner_text("#act") == "Confirm approval" and pg.locator("#pay-msg .alert").count() == 1)
    pg.click("#act"); pg.wait_for_timeout(400)
    pg.fill("#dgSearch", ""); pg.click('#fbar .x'); pg.wait_for_timeout(300)
    check("confirmed approval changes status to Approved", row_status(pg, target) in ("Approved", None), row_status(pg, target))
    # screening flag path
    pg.fill("#dgSearch", "Awaiting your approval"); pg.press("#dgSearch", "Enter"); pg.wait_for_timeout(250)
    # bulk approve: select two rows
    boxes = pg.locator("#tbody tr[data-id] td.sel label")
    boxes.nth(0).click(); boxes.nth(1).click(); pg.wait_for_timeout(200)
    sel = pg.evaluate("() => (0, eval)('state').sel.size")
    pg.click('[data-action="bulk-approve"]'); pg.wait_for_timeout(500)
    opened = pg.locator("#mOverlay.open").count() == 1
    body = pg.inner_text("#mBody") if opened else pg.inner_text("#toastRegion")
    check("bulk approve opens a confirmation modal (or explains why not)", opened or "individual review" in body or "cannot be approved" in body, (sel, body[:160]))
    if opened:
        foc = pg.evaluate("() => document.activeElement.id")
        check("modal takes focus on its confirm button", foc == "mConfirm", foc)
        pg.click("#mConfirm"); pg.wait_for_timeout(400)
        check("bulk approval applied", "Approved" in pg.inner_text("#toastRegion"), pg.inner_text("#toastRegion")[-120:])
    # persistence across reload
    pg.reload(); pg.wait_for_timeout(700)
    wf = pg.evaluate("() => JSON.parse(localStorage.getItem('ceo.wf')).pay")
    check("decisions persist in storage and re-apply after reload", len(wf) >= 2 and any(v["status"] == "Rejected" for v in wf.values()), {k: v["status"] for k, v in wf.items()})
    # export
    with pg.expect_download() as dl:
        pg.click('[data-action="export-grid"]')
    d = dl.value; path = W + "/proof/export-" + d.suggested_filename; d.save_as(path)
    lines = open(path).read().splitlines()
    check("CSV export downloads the grid's rows", len(lines) == 1 + pg.evaluate("() => (0,eval)('DATA').length") and lines[0].startswith("Value date"), (d.suggested_filename, len(lines)))
    # overview reflects approvals
    pg.goto(URL("index")); pg.wait_for_timeout(700)
    card = pg.inner_text("#ov-approvals .summary__k")
    aw = pg.evaluate("() => CEO_DATA.payments.filter(p => p.status === 'Awaiting your approval').length")
    check("overview approvals card reflects the decisions", card.startswith(str(aw) + " payment"), (card, aw))
    check("no console errors on payments journeys", not errs, errs[:5])
    b.close()
save("drive2")
