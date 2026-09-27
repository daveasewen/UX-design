"""shots.py <variant> <run> <file> <navtext|-> <tag> [mock] — element shots of every figure.dv in one view at 1440,
light and dark, plus the viewport. mock=markers applies the RENDER-ONLY marker/letter option (not canon)."""
import os, sys, json
from playwright.sync_api import sync_playwright
V, RUN, FILE, NAV, TAG = sys.argv[1:6]; MOCK = sys.argv[6] if len(sys.argv) > 6 else ''
OUT = os.path.expanduser('~/w4a/shots'); os.makedirs(OUT, exist_ok=True)
MOCK_JS = r"""() => {
  let n = 0;
  for (const svg of document.querySelectorAll('figure.dv svg.dv-svg')) {
    const lines = svg.querySelectorAll('polyline.dv-series[data-fxs]');
    const bands = svg.querySelectorAll('path.dv-band[data-fxs]');
    let pts = 0; if (lines.length) pts = lines[0].getAttribute('data-fxs').trim().split(/\s+/).length;
    else if (bands.length) pts = bands[0].getAttribute('data-fxs').trim().split(/\s+/).length / 2;
    if (pts <= 12) continue;
    const mk = [...svg.querySelectorAll('g.dv-marker')];
    const maxfx = Math.max(...mk.map(g => parseFloat(g.getAttribute('data-fx') || '0')));
    mk.forEach(g => { if (Math.abs(parseFloat(g.getAttribute('data-fx') || '0') - maxfx) > 1e-6) { g.style.display = 'none'; n++; } });
    const keys = {}; svg.querySelectorAll('text.dv-barkey').forEach(t => { (keys[t.getAttribute('data-series-group')] = keys[t.getAttribute('data-series-group')] || []).push(t); });
    for (const k in keys) { const L = keys[k]; const keep = L[Math.floor(L.length / 2)]; L.forEach(t => { if (t !== keep) { t.style.display = 'none'; n++; } }); }
  }
  return n; }"""
HUG_JS = r"""() => { let n = 0; for (const f of document.querySelectorAll('figure.dv[data-dv-type=donut], figure.dv[data-dv-type=pie]')) {
  let t = f.closest('.c-bento__tile'); while (t) { t.style.alignSelf = 'start'; t.style.height = 'auto'; n++; t = t.parentElement && t.parentElement.closest('.c-bento__tile'); } }
  window.dispatchEvent(new Event('resize')); return n; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for theme in ('light', 'dark'):
        c = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2); pg = c.new_page()
        pg.goto('file://' + os.path.expanduser('~/w4a/st/%s/cold-%s/out/%s' % (V, RUN, FILE))); pg.wait_for_timeout(1200)
        if NAV != '-':
            (pg.locator('a[href="%s"]' % NAV).first if NAV.endswith('.html') else pg.locator('nav a, nav button, .sn a, aside a, [role=navigation] a').filter(has_text=NAV).first).click(); pg.wait_for_timeout(1500)
        pg.evaluate("t => { document.documentElement.setAttribute('data-theme', t); }", theme)
        pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(2600)
        if MOCK == 'markers': print('mock hid', pg.evaluate(MOCK_JS))
        if MOCK == 'hug': print('mock hug', pg.evaluate(HUG_JS))
        figs = pg.locator('figure.dv')
        info = []
        for i in range(figs.count()):
            f = figs.nth(i)
            if not f.is_visible(): continue
            f.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
            name = '%s-%s-%s-%s-fig%02d.png' % (TAG, V + ('-' + MOCK if MOCK else ''), theme, RUN, i)
            try:
                f.screenshot(path=os.path.join(OUT, name), timeout=5000)
                bb = f.bounding_box(); info.append((name, f.get_attribute('data-dv-type'), [round(x) for x in (bb['width'], bb['height'])]))
            except Exception as e: info.append((name, 'ERR', str(e)[:80]))
        pg.evaluate("() => { const s = document.querySelector('.sh-content, main, #main'); if (s) s.scrollTop = 0; window.scrollTo(0,0); }")
        pg.screenshot(path=os.path.join(OUT, '%s-%s-%s-%s-full.png' % (TAG, V + ('-' + MOCK if MOCK else ''), theme, RUN)), full_page=True)
        print(theme, json.dumps(info)); c.close()
    b.close()
