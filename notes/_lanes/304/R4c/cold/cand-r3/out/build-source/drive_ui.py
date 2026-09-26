# navigation: every destination, h1, aria-current, document title, URL
for v, h in [('accounts', 'Accounts and transactions'), ('liquidity', 'Liquidity and funding'), ('payments', 'Payments and approvals'), ('fx', 'FX and markets'),
             ('risk', 'Risk and limits'), ('trade', 'Trade finance'), ('reports', 'Reports'), ('messages', 'HSBC messages and service requests'), ('settings', 'Settings'), ('overview', 'Overview')]:
    pg.click('#nav-app a.sn-link[data-nav="%s"]' % v); pg.wait_for_timeout(700)
    ok = txt(pg, '#page-h1') == h and ev(pg, "v => document.querySelector('#nav-app a[data-nav=\"' + v + '\"]').getAttribute('aria-current')", v) == 'page' and ('#/' + v) in pg.url and document_title_ok if False else None
    check('nav to %s: heading, aria-current, URL, title' % v, txt(pg, '#page-h1') == h and ev(pg, "v => document.querySelector('#nav-app a[data-nav=\"' + v + '\"]').getAttribute('aria-current')", v) == 'page'
          and ('#/' + v) in pg.url and pg.title().startswith(h), [txt(pg, '#page-h1'), pg.title()])
# sidebar collapse toggle (App-shell-side-nav script)
pg.click('[data-navtoggle="shell-app"]'); pg.wait_for_timeout(400)
check('sidebar collapses to its rail and says so', ev(pg, "() => document.getElementById('shell-app').getAttribute('data-nav')") == 'rail' and ev(pg, "() => document.querySelector('[data-navtoggle]').getAttribute('aria-expanded')") == 'false')
pg.click('[data-navtoggle="shell-app"]'); pg.wait_for_timeout(400)
# theme
bg0 = ev(pg, "() => getComputedStyle(document.querySelector('[data-kpi=\"ov-cash\"]')).backgroundColor")
pg.click('#ftbTheme [data-theme-set="dark"]'); pg.wait_for_timeout(500)
bg1 = ev(pg, "() => getComputedStyle(document.querySelector('[data-kpi=\"ov-cash\"]')).backgroundColor")
check('theme switch sets data-theme=dark on <html> and the tiles repaint', ev(pg, "() => document.documentElement.getAttribute('data-theme')") == 'dark' and bg0 != bg1, [bg0, bg1])
logo = ev(pg, "() => [...document.querySelectorAll('.sh-mark')].map(i => [i.getAttribute('data-mode'), getComputedStyle(i).display])")
check('the dark masterbrand is the one shown in dark mode', ['dark', 'block'] in logo or ['dark', 'inline'] in logo, logo)
pg.reload(); pg.wait_for_timeout(1300)
check('theme persists across reload', ev(pg, "() => document.documentElement.getAttribute('data-theme')") == 'dark' and ev(pg, "() => document.querySelector('#ftbTheme [aria-pressed=true]').getAttribute('data-theme-set')") == 'dark')
gd = ev(pg, "() => getComputedStyle(document.querySelector('.ceo-view:not([hidden]) .ceo-ground')).backgroundColor")
check('the bento section ground follows the theme (dark wall ground)', gd != 'rgb(240, 240, 240)', gd)
pg.click('#ftbTheme [data-theme-set="light"]'); pg.wait_for_timeout(400)
# chart behaviour: tooltip on hover, legend isolate, table view, sort seg
pg.goto(URL + '#/accounts'); pg.wait_for_timeout(1300)
m = pg.locator('[data-chart="ac-ccyflow"] rect.dv-series').first; m.hover(); pg.wait_for_timeout(400)
tip = ev(pg, "() => { const t = [...document.querySelectorAll('.dv-tip, [class*=tip]')].find(e => getComputedStyle(e).opacity !== '0' && getComputedStyle(e).visibility !== 'hidden' && e.textContent.trim()); return t ? t.textContent.trim() : null; }")
check('hovering a bar shows the value popover', tip is not None and ':' in tip, tip)
leg = pg.locator('[data-chart="ac-ccyflow"] .dv-leg-item').first; leg.click(); pg.wait_for_timeout(400)
iso = ev(pg, "() => [...document.querySelectorAll('[data-chart=\"ac-ccyflow\"] [data-series-group]')].filter(e => e.classList.contains('is-ghost') || e.classList.contains('is-faded') || getComputedStyle(e).opacity < 0.5).length")
check('clicking a legend name isolates its series (others ghost)', iso > 0 and ev(pg, "() => !document.querySelector('[data-chart=\"ac-ccyflow\"] .dv-leg-reset').disabled"), iso)
pg.click('[data-chart="ac-ccyflow"] .dv-leg-reset'); pg.wait_for_timeout(300)
pg.click('[data-chart="ac-ccyflow"] summary.dv-tbl-toggle'); pg.wait_for_timeout(300)
check('"View as table" opens the data table built from the same numbers', ev(pg, "() => document.querySelector('[data-chart=\"ac-ccyflow\"] details.dv-tbl').open && document.querySelectorAll('[data-chart=\"ac-ccyflow\"] table.dv-table tbody tr').length > 0"))
pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
pg.goto(URL + '#/trade'); pg.wait_for_timeout(1300)
o1 = ev(pg, "() => [...document.querySelectorAll('[data-chart=\"tf-expiry\"] table.dv-table tbody td')].map(t => +t.textContent)")
pg.click('[data-chart="tf-expiry"] button[data-dv-view-btn="desc"]'); pg.wait_for_timeout(500)
o2 = ev(pg, "() => [...document.querySelectorAll('[data-chart=\"tf-expiry\"] table.dv-table tbody td')].map(t => +t.textContent)")
check('the column chart sort switch re-renders in descending order', o2 == sorted(o1, reverse=True) and o1 != o2, [o1, o2])
# KPI whole-tile link
pg.goto(URL + '#/overview'); pg.wait_for_timeout(1200)
pg.click('[data-kpi="ov-liq"] .kpi-link'); pg.wait_for_timeout(800)
check('a KPI tile links to its view', '#/liquidity' in pg.url, pg.url)
# skip link
pg.goto(URL + '#/overview'); pg.reload(); pg.wait_for_timeout(1300); pg.keyboard.press('Tab')
check('first Tab reaches the skip link', ev(pg, "() => document.activeElement.classList.contains('sh-skip')"))
