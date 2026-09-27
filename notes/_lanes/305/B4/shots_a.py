"""#305 B4: renders for the call-27 visuals page, half (a). Run from the repo root at the seat:
export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/305/B4/shots_a.py"""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); IMG = os.path.join(ROOT, 'notes/_lanes/305/B4/img')
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    # 1. the own-size fixture pair (canon parts; planted = the page sizes the parts)
    for name in ('own-size-clean', 'own-size-planted'):
        pg = b.new_page(viewport={'width': 900, 'height': 400}, device_scale_factor=2)
        pg.goto('file://' + os.path.join(ROOT, 'knowledge/_tests/geometry/%s.html' % name)); pg.wait_for_timeout(600)
        m = pg.evaluate("""() => { const q = s => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect();
             const cs = getComputedStyle(e); return {t: e.textContent.trim().slice(0,20), w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10, fs: cs.fontSize}; });
             return {buttons: q('.btn'), th: q('thead th'), fonts: document.fonts.check('16px "HSBC Univers Next"')}; }""")
        out[name] = m
        pg.screenshot(path=os.path.join(IMG, 'a1-%s.png' % name), clip={'x': 24, 'y': 16, 'width': 820, 'height': 250})
        pg.close()
    # 2. #288's composed dashboard: the .mini buttons as the page drew them, and with the page's .mini class taken off
    page288 = 'file://' + os.path.join(ROOT, 'notes/_lanes/288/P/composed-dashboard.html')
    for state in ('as-drawn', 'own-size'):
        pg = b.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=2)
        pg.goto(page288); pg.wait_for_timeout(1200)
        if state == 'own-size':
            pg.evaluate("() => document.querySelectorAll('.btn.mini').forEach(e => { e.setAttribute('data-was-mini',''); e.classList.remove('mini'); })")
            pg.wait_for_timeout(300)
        box = pg.evaluate("""() => { const els = [...document.querySelectorAll('.btn')].filter(e => e.closest('.cn-button') || true);
             const minis = [...document.querySelectorAll('%s')];
             const r = minis.map(e => e.getBoundingClientRect());
             return {n: minis.length, list: minis.map(e => ({t: e.textContent.trim().slice(0,24), w: Math.round(e.getBoundingClientRect().width*10)/10,
                     h: Math.round(e.getBoundingClientRect().height*10)/10, x: Math.round(e.getBoundingClientRect().x), y: Math.round(e.getBoundingClientRect().y + scrollY)})),
                     x0: Math.min(...r.map(a=>a.left)), y0: Math.min(...r.map(a=>a.top+scrollY)), x1: Math.max(...r.map(a=>a.right)), y1: Math.max(...r.map(a=>a.bottom+scrollY))}; }"""
             % ('.btn.mini' if state == 'as-drawn' else '.btn[data-was-mini], .btn.mini'))
        out['288-' + state] = box
        pg.screenshot(path=os.path.join(IMG, 'a2-288-%s.png' % state), clip={'x': 964, 'y': 548, 'width': 440, 'height': 320})
        pg.close()
    b.close()
json.dump(out, open(os.path.join(IMG, '..', 'shots_a.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
