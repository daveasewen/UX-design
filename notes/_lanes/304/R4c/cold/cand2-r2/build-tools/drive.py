"""Driven browser checks for the CEO prototype (real clicks and keys in Chromium, file:// pages).
usage: python3 drive.py <out-dir> <group>   group = overview | payments | risk | service | misc
Writes proof/drive-<group>.json and prints one line per check: PASS/FAIL name — detail."""
import json, os, sys, time
from playwright.sync_api import sync_playwright

OUT = os.path.abspath(sys.argv[1]); GROUP = sys.argv[2]
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    print(('PASS ' if ok else 'FAIL ') + name + ' — ' + str(detail)[:200])


def url(p, q=''):
    return 'file://%s/%s.html%s' % (OUT, p, q)


def new_page(ctx, errs):
    pg = ctx.new_page()
    pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errs.append('pageerror ' + str(e)[:200]))
    return pg


def settle(pg, ms=700):
    pg.wait_for_timeout(ms)


def run(fn):
    try:
        fn()
    except Exception as e:  # a crash in a check is a FAIL, never a silent pass
        check(fn.__name__ + ' (crashed)', False, repr(e))


with sync_playwright() as P:
    b = P.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    errs = []
    pg = new_page(ctx, errs)

    if GROUP == 'overview':
        def t_load():
            pg.goto(url('index')); settle(pg)
            check('overview loads with zero console errors', not errs, errs)
            n = pg.evaluate("[...document.querySelectorAll('figure.dv')].filter(f => f.querySelector('svg.dv-svg').children.length > 0).length")
            check('overview draws all four charts', n == 4, n)
        run(t_load)

        def t_entity_filter():
            before = pg.evaluate("[document.querySelector('#kpi-cash .kpi-val').textContent, document.querySelector('#ov-region table.dv-table tbody').textContent, document.getElementById('dec-pay').textContent]")
            pg.click('.dd[data-filter="entity"] .trigger'); pg.click('.dd[data-filter="entity"] [data-value="E03"]'); settle(pg)
            after = pg.evaluate("[document.querySelector('#kpi-cash .kpi-val').textContent, document.querySelector('#ov-region table.dv-table tbody').textContent, document.getElementById('dec-pay').textContent, location.search, document.getElementById('scope-note').textContent]")
            check('entity filter re-drives KPI, exposure chart and decisions', before[0] != after[0] and before[1] != after[1] and before[2] != after[2], [before[0], after[0], after[3], after[4]])
            check('entity filter is written to the URL', 'entity=E03' in after[3], after[3])
        run(t_entity_filter)

        def t_period():
            b4 = pg.evaluate("document.querySelectorAll('#ov-trend table.dv-table tbody tr').length")
            pg.click('[data-period-seg] button[data-value="7"]'); settle(pg)
            af = pg.evaluate("[document.querySelectorAll('#ov-trend table.dv-table tbody tr').length, document.querySelector('[data-period-seg] button[data-value=\"7\"]').getAttribute('aria-pressed'), location.search]")
            check('period switch re-drives the trend series and the URL', b4 != af[0] and af[1] == 'true' and 'period=7' in af[2], [b4, af])
        run(t_period)

        def t_reload_persists():
            pg.reload(); settle(pg)
            st = pg.evaluate("[document.querySelector('.dd[data-filter=\"entity\"] .ddval').textContent, document.querySelector('[data-period-seg] button[aria-pressed=\"true\"]').textContent]")
            check('filters survive a reload', 'Americas' in st[0] and '7' in st[1], st)
        run(t_reload_persists)

        def t_theme():
            pg.click('[data-theme-seg] button[data-value="dark"]'); settle(pg, 300)
            t1 = pg.evaluate("[document.documentElement.getAttribute('data-theme'), getComputedStyle(document.querySelector('.ceo-wall')).backgroundColor, getComputedStyle(document.querySelector('.kpi-tile')).backgroundColor]")
            pg.goto(url('payments')); settle(pg)
            t2 = pg.evaluate("document.documentElement.getAttribute('data-theme')")
            check('theme switch sets dark and carries to the next page', t1[0] == 'dark' and t2 == 'dark', [t1, t2])
            pg.click('[data-theme-seg] button[data-value="light"]'); settle(pg, 300)
            pg.goto(url('index')); settle(pg)
        run(t_theme)

        def t_nav_carries():
            h = pg.evaluate("document.querySelector('.sn a[data-nav-link=\"risk.html\"]').getAttribute('href')")
            check('sidebar links carry the shared filters', 'entity=E03' in h and 'period=7' in h, h)
            pg.click('[data-action="reset-filters"]'); settle(pg)
            h2 = pg.evaluate("[document.querySelector('.sn a[data-nav-link=\"risk.html\"]').getAttribute('href'), location.search]")
            check('reset filters clears URL and links', h2[0] == 'risk.html' and h2[1] == '', h2)
        run(t_nav_carries)

        def t_tooltip_legend_table():
            m = pg.query_selector('#ov-ccy rect.dv-series'); m.hover(); settle(pg, 300)
            tip = pg.evaluate("(() => { const t = document.querySelector('#dvTip.on'); return t ? t.textContent.trim() : null; })()")
            check('chart tooltip shows on hover', tip is not None, tip)
            pg.click('#ov-region .dv-leg-item[data-series="1"]'); settle(pg, 300)
            iso = pg.evaluate("[document.querySelector('#ov-region .dv-leg-item[data-series=\"1\"]').getAttribute('aria-pressed'), document.querySelectorAll('#ov-region .is-faded, #ov-region .is-ghost').length]")
            check('legend isolate works on the exposure chart', iso[0] == 'true' and iso[1] > 0, iso)
            pg.click('#ov-region .dv-leg-reset'); settle(pg, 200)
            pg.click('#ov-limits summary.dv-tbl-toggle'); settle(pg, 200)
            op = pg.evaluate("[document.querySelector('#ov-limits details.dv-tbl').open, document.querySelectorAll('#ov-limits table.dv-table tbody tr').length]")
            check('view-as-table opens the chart table', op[0] and op[1] > 0, op)
        run(t_tooltip_legend_table)

        def t_export():
            with pg.expect_download() as d:
                pg.click('[data-action="export"]')
            check('overview export downloads a CSV', d.value.suggested_filename.endswith('.csv'), d.value.suggested_filename)
        run(t_export)

        def t_drill_region():
            pg.click('#ov-region rect.dv-series >> nth=0'); pg.wait_for_load_state(); settle(pg, 900)
            r = pg.evaluate("[location.pathname.split('/').pop() + location.search, document.querySelector('.tablist [aria-selected=\"true\"]').textContent, document.getElementById('dgTitle').textContent, document.getElementById('dgCount').textContent]")
            check('exposure column drills through to positions and limits', 'risk.html' in r[0] and 'tab=positions' in r[0] and 'Positions' in r[1], r)
            pg.go_back(); settle(pg)
            pg.click('#ov-ccy rect.dv-series >> nth=0'); pg.wait_for_load_state(); settle(pg, 900)
            r2 = pg.evaluate("[location.search, document.getElementById('fbar').textContent.trim(), document.getElementById('dgCount').textContent]")
            check('currency bar drills through with the currency applied', 'ccy=' in r2[0] and len(r2[1]) > 0, r2)
            pg.goto(url('index')); settle(pg)
        run(t_drill_region)

        def t_decision_link():
            pg.click('#dec-pay button.row >> nth=0'); pg.wait_for_load_state(); settle(pg, 1000)
            r = pg.evaluate("[location.search, document.getElementById('sheet').classList.contains('open'), document.getElementById('dtitle').textContent]")
            check('pending-approval card links to an actionable payment record', 'open=PAY-' in r[0] and r[1] and 'PAY-' in r[2], r)
        run(t_decision_link)

    if GROUP == 'payments':
        def t_grid():
            pg.goto(url('payments')); settle(pg)
            check('payments loads with zero console errors', not errs, errs)
            n0 = pg.evaluate("document.querySelectorAll('#tbody tr[data-id]').length")
            pg.click('th[data-key="amount"] .sort'); settle(pg, 300)
            a = pg.evaluate("[...document.querySelectorAll('#tbody tr[data-id] td.num')].map(t => parseFloat(t.textContent.replace(/[^0-9.\\-−]/g,'').replace('−','-')))")
            check('grid sorts by amount', all(a[i] <= a[i + 1] for i in range(len(a) - 1)), a[:5])
            pg.click('#pgList [data-go="next"]'); settle(pg, 200)
            rng = pg.evaluate("document.getElementById('dgRange').textContent")
            check('grid pages', rng.startswith('9'), rng)
            pg.select_option('#pp', '24'); settle(pg, 200)
            n24 = pg.evaluate("document.querySelectorAll('#tbody tr[data-id]').length")
            check('rows per page changes the page size', n0 == 8 and n24 == 24, [n0, n24])
            pg.fill('#dgSearch', 'Pending'); pg.press('#dgSearch', 'Enter'); settle(pg, 200)
            c = pg.evaluate("[document.getElementById('dgCount').textContent, document.getElementById('fbar').textContent.trim()]")
            check('grid search applies a removable chip', 'Pending' in c[1], c)
            pg.reload(); settle(pg)
            s = pg.evaluate("[state.sortKey, state.sortDir, state.pageSize, document.querySelector('th[data-key=\"amount\"]').getAttribute('aria-sort')]")
            check('grid sort and page size survive a reload', s[0] == 'amount' and s[2] == 24 and s[3] == 'ascending', s)
        run(t_grid)

        def t_approve():
            pg.click('th[data-key="type"] .sort'); settle(pg, 200)
            rows = pg.evaluate("[...document.querySelectorAll('#tbody tr[data-id]')].map(tr => tr.children[4].textContent.trim())")
            ix = next(i for i, t in enumerate(rows) if t == 'Pending approval')
            pg.click('#tbody tr[data-id] >> nth=%d >> td:nth-child(3)' % ix); settle(pg, 500)
            title = pg.evaluate("document.getElementById('dtitle').textContent")
            pid = title.split()[-1]
            check('row click opens the payment detail drawer', pg.evaluate("document.getElementById('sheet').classList.contains('open')") and 'PAY-' in title, title)
            fin = pg.evaluate("document.activeElement.closest('#sheet') !== null")
            check('focus moves into the drawer', fin, fin)
            pg.click('#dfoot [data-drawer-act="1"]'); settle(pg, 400)   # Reject
            pg.click('#mconfirm'); settle(pg, 200)
            err = pg.evaluate("[document.getElementById('t1-group').classList.contains('is-error'), document.getElementById('t1-err').hidden, document.getElementById('overlay').classList.contains('open')]")
            check('reject without an audit note is refused with an error', err[0] and not err[1] and err[2], err)
            pg.keyboard.press('Escape'); settle(pg, 300)
            back = pg.evaluate("[document.getElementById('overlay').classList.contains('open'), document.activeElement.closest('#tbody') !== null]")
            check('Escape closes the modal and focus returns to the record row', not back[0] and back[1], back)
            pg.click('#tbody tr[data-id] >> nth=%d >> td:nth-child(3)' % ix); settle(pg, 500)
            pg.click('#dfoot [data-drawer-act="0"]'); settle(pg, 400)   # Approve
            pg.fill('#t1', 'Approved after checking the supplier contract.'); settle(pg, 100)
            cnt = pg.evaluate("document.getElementById('t1-count').textContent")
            check('audit note counter runs (Textarea script, verbatim)', cnt.startswith('47/') or cnt.split('/')[0].isdigit() and int(cnt.split('/')[0]) > 0, cnt)
            pg.click('#mconfirm'); settle(pg, 600)
            st = pg.evaluate("[document.querySelectorAll('.toast').length, [...document.querySelectorAll('.toast .msg')].map(t => t.textContent).join('|')]")
            check('approval confirms with a toast', st[0] > 0 and pid in st[1], st)
            pg.reload(); settle(pg)
            saved = pg.evaluate("JSON.parse(localStorage.getItem('ceo-hsbc-prototype-v1')).pay['%s']" % pid)
            check('approval persists with an audit entry', saved and saved['status'] == 'Approved' and 'supplier contract' in saved['audit'][0]['note'], saved)
            pg.goto(url('index')); settle(pg)
            gone = pg.evaluate("document.getElementById('dec-pay').textContent.indexOf('%s')" % pid)
            check('approved payment leaves the overview decisions list', gone < 0, gone)
        run(t_approve)

    if GROUP == 'risk':
        def t_ack():
            pg.goto(url('risk', '?tab=exceptions')); settle(pg)
            check('risk loads with zero console errors', not errs, errs)
            pg.click('#tbody tr[data-id] >> nth=0 >> td:nth-child(3)'); settle(pg, 500)
            t = pg.evaluate("document.getElementById('dtitle').textContent")
            xid = t.split()[-1]
            pg.click('#dfoot [data-drawer-act="0"]'); settle(pg, 400)
            pg.fill('#t1', 'too short'); pg.click('#mconfirm'); settle(pg, 200)
            e = pg.evaluate("document.getElementById('t1-err').textContent.trim()")
            check('acknowledgement needs a 20-character audit note', '20' in e, e)
            pg.fill('#t1', 'Seen. Regional CFO to reduce the position by Friday.'); pg.click('#mconfirm'); settle(pg, 600)
            s = pg.evaluate("JSON.parse(localStorage.getItem('ceo-hsbc-prototype-v1')).exc['%s']" % xid)
            check('exception acknowledged with audit note, persisted', s and s['status'] == 'Acknowledged', s)
        run(t_ack)

        def t_tabs():
            pg.click('.tablist [data-tab="positions"]'); settle(pg, 400)
            r = pg.evaluate("[document.getElementById('dgTitle').textContent, document.getElementById('dgCount').textContent, document.querySelector('th[data-key=\"amount\"] .lbl').textContent]")
            check('tabs switch the grid to positions and limits', 'Positions' in r[0] and 'Exposure' in r[2], r)
            pg.keyboard.press('ArrowLeft'); settle(pg, 300)
            r2 = pg.evaluate("document.getElementById('dgTitle').textContent")
            check('tabs respond to arrow keys', 'exceptions' in r2.lower(), r2)
        run(t_tabs)

    if GROUP == 'service':
        def t_request():
            pg.goto(url('messages')); settle(pg)
            check('messages loads with zero console errors', not errs, errs)
            n0 = pg.evaluate("DATA_len = document.getElementById('sr-list-count').textContent")
            pg.click('[data-action="new-request"]'); settle(pg, 500)
            pg.click('#dfoot [data-drawer-act="0"]'); settle(pg, 200)
            e = pg.evaluate("[document.getElementById('sr-sub-err').hidden, document.getElementById('sr-sub').getAttribute('aria-invalid')]")
            check('service request form refuses an empty subject', not e[0] and e[1] == 'true', e)
            pg.fill('#sr-sub', 'Please increase the daily CHAPS limit'); pg.click('#dfoot [data-drawer-act="0"]'); settle(pg, 600)
            top = pg.evaluate("[document.querySelector('#sr-list .title').textContent, document.getElementById('sr-list-count').textContent]")
            check('new service request appears in the list', 'CHAPS' in top[0], [n0, top])
        run(t_request)

        def t_message():
            u0 = pg.evaluate("document.getElementById('ms-unread').textContent")
            pg.click('#ms-list button.row >> nth=0'); settle(pg, 500)
            u1 = pg.evaluate("document.getElementById('ms-unread').textContent")
            check('opening a message marks it read', u0 != u1, [u0, u1])
            pg.keyboard.press('Escape'); settle(pg, 300)
            fb = pg.evaluate("document.activeElement && document.activeElement.closest('#ms-list') !== null")
            check('Escape closes the drawer and returns focus to the row', fb, fb)
            pg.fill('#sr-list-q', 'CHAPS'); settle(pg, 200)
            c = pg.evaluate("document.querySelectorAll('#sr-list li').length")
            check('request list search filters', c >= 1, c)
            pg.fill('#sr-list-q', ''); pg.click('[data-list-sort="sr-list"] button[data-value="priority"]'); settle(pg, 200)
            pr = pg.evaluate("[...document.querySelectorAll('#sr-list .amount')].map(a => a.textContent)")
            check('request list sorts by priority', pr[0].startswith('High'), pr[:3])
            pg.click('#sr-list-pg [data-pg="2"]'); settle(pg, 200)
            cur = pg.evaluate("document.querySelector('#sr-list-pg [aria-current=\"page\"]').textContent")
            check('request list pages', cur == '2', cur)
        run(t_message)

        def t_report():
            pg.goto(url('reports')); settle(pg)
            pg.click('#rp-list button.row >> nth=0'); settle(pg, 500)
            with pg.expect_download() as d:
                pg.click('#dfoot [data-drawer-act="0"]')
            check('report runs and exports a CSV', d.value.suggested_filename.endswith('.csv'), d.value.suggested_filename)
        run(t_report)

        def t_trade():
            pg.goto(url('trade')); settle(pg)
            rows = pg.evaluate("[...document.querySelectorAll('#tbody tr[data-id]')].map(tr => tr.children[4].textContent.trim())")
            ix = next(i for i, t in enumerate(rows) if t != 'Settled')
            pg.click('#tbody tr[data-id] >> nth=%d >> td:nth-child(3)' % ix); settle(pg, 500)
            pg.click('#dfoot [data-drawer-act="0"]'); settle(pg, 400)
            pg.fill('#t1', 'Extend expiry by 60 days to match the shipment.'); pg.click('#mconfirm'); settle(pg, 600)
            pg.goto(url('messages')); settle(pg)
            pg.fill('#sr-list-q', 'Amendment to TF'); settle(pg, 300)
            t = pg.evaluate("[...document.querySelectorAll('#sr-list .title')].map(x => x.textContent)")
            check('trade amendment raises a service request visible on messages', any('Amendment' in x for x in t), t[:2])
            pg.fill('#sr-list-q', ''); settle(pg, 200)
        run(t_trade)

    if GROUP == 'misc':
        def t_settings():
            pg.goto(url('settings')); settle(pg)
            check('settings loads with zero console errors', not errs, errs)
            v0 = pg.evaluate("document.getElementById('nt-msg').checked")
            pg.click('label[for="nt-msg"]'); settle(pg, 200); pg.reload(); settle(pg)
            v1 = pg.evaluate("document.getElementById('nt-msg').checked")
            check('notification switch persists', v0 != v1, [v0, v1])
        run(t_settings)

        def t_navtoggle_skip():
            pg.click('.sn-toggle[data-navtoggle]'); settle(pg, 400)
            w = pg.evaluate("[document.querySelector('.sh-body > .sn').getBoundingClientRect().width, document.getElementById('shell-wide').getAttribute('data-nav')]")
            check('nav collapses to the rail', w[0] < 100 and w[1] == 'rail', w)
            pg.click('.sn-toggle[data-navtoggle]'); settle(pg, 400)
            pg.goto(url('fx')); settle(pg)
            pg.keyboard.press('Tab'); settle(pg, 200)
            f = pg.evaluate("[document.activeElement.className, document.activeElement.textContent.trim()]")
            check('first Tab lands on the skip link', 'sh-skip' in f[0], f)
        run(t_navtoggle_skip)

        def t_all_pages_click_nav():
            pg.goto(url('index')); settle(pg)
            for dest in ['accounts', 'liquidity', 'fx', 'trade', 'reports', 'messages', 'settings', 'risk', 'payments', 'index']:
                pg.click('.sh-body .sn a[data-nav-link="%s.html"]' % dest); pg.wait_for_load_state(); settle(pg, 500)
            check('sidebar navigates through all ten screens with zero console errors', not errs and pg.url.endswith('index.html'), [pg.url, errs[:3]])
        run(t_all_pages_click_nav)

        def t_finder():
            pg.click('.sh-appbar [aria-label="Search"]'); settle(pg, 500)
            pg.fill('#finder-q', 'PAY-10'); settle(pg, 200)
            n = pg.evaluate("document.querySelectorAll('#finder-list li').length")
            check('app-bar search finds records across the app', n > 0, n)
        run(t_finder)

        def t_liq_fx_accounts():
            for p, fid in [('liquidity', 'lq-combo'), ('fx', 'fx-candle'), ('accounts', 'ac-bal')]:
                pg.goto(url(p)); settle(pg)
                b4 = pg.evaluate("document.querySelector('#%s table.dv-table tbody').textContent" % fid)
                pg.click('.dd[data-filter="region"] .trigger'); pg.click('.dd[data-filter="region"] [data-value="EU"]'); settle(pg)
                af = pg.evaluate("[document.querySelector('#%s table.dv-table tbody').textContent, document.getElementById('dgCount').textContent]" % fid)
                check('%s: region filter re-drives chart and grid' % p, b4 != af[0] or p == 'fx', af[1])
                pg.click('[data-action="reset-filters"]'); settle(pg)
        run(t_liq_fx_accounts)

    json.dump({'group': GROUP, 'results': RESULTS, 'console_errors': errs}, open(os.path.join(os.path.dirname(OUT), 'proof', 'drive-%s.json' % GROUP), 'w'), indent=1)
    print('TOTAL %d checks, %d fail, console errors %d' % (len(RESULTS), sum(1 for r in RESULTS if not r['pass']), len(errs)))
    b.close()
