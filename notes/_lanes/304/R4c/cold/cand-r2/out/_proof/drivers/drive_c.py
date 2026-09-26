"""Driven proof C — keyboard paths, focus return, the 1440 band, and screenshots FOR THE RECORD ONLY (never evidence)."""
import os, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand-r2'); URL = 'file://' + W + '/out/index.html'
R = []; CON = []
def ok(name, cond, detail=''): R.append({'check': name, 'pass': bool(cond), 'detail': str(detail)[:300]})
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.on('pageerror', lambda e: CON.append(str(e)[:300])); pg.on('console', lambda m: CON.append(m.text[:200]) if m.type == 'error' else None)
    pg.goto(URL + '#/overview'); pg.evaluate("() => { try { localStorage.clear(); } catch(e){} }"); pg.goto(URL + '#/overview'); pg.wait_for_timeout(1200)
    pg.keyboard.press('Tab'); ok('first Tab lands on the skip link', pg.evaluate("() => document.activeElement.classList.contains('sh-skip')"))
    pg.focus('#flt-region-t'); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    ok('Enter opens the region menu and focus enters it', pg.get_attribute('#flt-region-m', 'data-open') == 'true' and pg.evaluate("() => !!document.activeElement.closest('#flt-region-m')"))
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('ArrowDown'); pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
    ok('arrow keys + Enter choose a region; focus returns to the trigger', 'region=' in pg.url and pg.evaluate("() => document.activeElement.id") == 'flt-region-t', pg.url)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(100); pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    ok('Escape closes the menu', pg.get_attribute('#flt-region-m', 'data-open') is None)
    pg.goto(URL + '#/payments'); pg.wait_for_timeout(1000)
    link = pg.locator('[data-grid="payments"] tbody a[data-record]').first
    link.evaluate("el => el.scrollIntoView({block:'center'})"); link.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
    ok('Enter on a record link opens its drawer', pg.locator('.sheet.open').count() == 1)
    for _ in range(25): pg.keyboard.press('Tab')
    ok('Tab stays trapped inside the open drawer', pg.evaluate("() => !!document.activeElement.closest('.sheet')"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('Escape closes the drawer and focus returns to the link', pg.evaluate("() => document.activeElement.matches('a[data-record]')"))
    bar = pg.locator('[data-chart="pm-valuedate"] svg rect[data-tip]').first
    bar.evaluate("el => el.scrollIntoView({block:'center'})"); bar.focus(); pg.wait_for_timeout(200)
    ok('chart marks take keyboard focus and show their tooltip', pg.evaluate("() => { const t = [...document.querySelectorAll('.dv-tip, [class*=tip]')].find(e => getComputedStyle(e).opacity !== '0' && e.textContent.trim()); return !!t; }"))
    # the standard 1440 desktop band: canon re-flows half-width tiles to full rows (bento band <=1100)
    pg.set_viewport_size({'width': 1440, 'height': 900}); pg.goto(URL + '#/overview'); pg.wait_for_timeout(1200)
    g = pg.evaluate("() => { const c = document.querySelector('.sh-content'); return {hscroll: c.scrollWidth - c.clientWidth, kpiTops: [...document.querySelectorAll('[data-kpi]')].map(k => Math.round(k.getBoundingClientRect().top)), tiles: [...document.querySelectorAll('.app-view:not([hidden]) .stat-card')].map(t => Math.round(t.getBoundingClientRect().width))}; }")
    ok('1440: no horizontal scroll, four KPIs on one row', g['hscroll'] == 0 and len(set(g['kpiTops'])) == 1, g)
    R[-1]['geo1440'] = g
    pg.set_viewport_size({'width': 1920, 'height': 1080}); pg.goto(URL + '#/overview'); pg.wait_for_timeout(1200)
    shots = []
    for mode in ['light', 'dark']:
        pg.evaluate("m => document.documentElement.setAttribute('data-theme', m)", mode); pg.wait_for_timeout(400)
        for v in ['overview', 'payments', 'risk']:
            pg.evaluate("v => { location.hash = '#/' + v; }", v); pg.wait_for_timeout(600)
            f = W + '/out/_proof/record-only-%s-%s.png' % (v, mode); os.makedirs(os.path.dirname(f), exist_ok=True); pg.screenshot(path=f); shots.append(os.path.basename(f))
    ok('no console errors in this drive', not CON, CON)
    b.close()
json.dump({'results': R, 'screenshots_record_only': shots}, open(W + '/proof/drive-c.json', 'w'), indent=1)
print('%d/%d pass' % (sum(r['pass'] for r in R), len(R)))
for r in R:
    if not r['pass']: print('FAIL', r)
