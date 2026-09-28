"""#305 B5: builds, then renders the loose-ends page at 1440 and 390, light and dark, at the seat. Run from the repo root:
export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/305/B5/render.py"""
import os, json, sys, subprocess
ROOT = os.getcwd()
subprocess.check_call([sys.executable, 'notes/_lanes/305/B5/build.py'])
from playwright.sync_api import sync_playwright
PAGE = 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html'
SHOTS = os.path.join(ROOT, 'notes/_lanes/305/B5/shots'); os.makedirs(SHOTS, exist_ok=True)
CHECK = r"""() => { const vw = document.documentElement.clientWidth; const off = [];
  for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') off.push(el.tagName + '.' + (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className||'').toString().slice(0,40)); }
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
  const wrap = document.querySelector('header .wrap'); const pad = wrap ? getComputedStyle(wrap).paddingLeft : null;
  return { scrollWidth: document.documentElement.scrollWidth, vw, off: off.slice(0,10), broken, imgs: document.images.length,
    boxes: document.querySelectorAll('.dd-box').length, compact: document.querySelectorAll('.dd-box.dd-compact').length,
    height: document.documentElement.scrollHeight, gutter: pad, bg: getComputedStyle(document.body).backgroundColor }; }"""
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for w in (1440, 390):
        for mode in ('light', 'dark'):
            errs = []
            pg = b.new_page(viewport={'width': w, 'height': 1000}, color_scheme=mode)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('file://' + os.path.join(ROOT, PAGE)); pg.wait_for_timeout(600)
            pg.evaluate("() => document.querySelectorAll('img[loading]').forEach(i => i.loading='eager')")
            pg.wait_for_timeout(900)
            r = pg.evaluate(CHECK); r['pageerrors'] = errs
            tag = 'w%d-%s' % (w, mode); report[tag] = r
            h = r['height']; y = 0; n = 0
            while y < h and n < 80:
                pg.evaluate('window.scrollTo(0,%d)' % y); pg.wait_for_timeout(100)
                pg.screenshot(path=os.path.join(SHOTS, '%s-part%02d.png' % (tag, n)))
                y += 1000; n += 1
            r['parts'] = n
            pg.close()
    b.close()
json.dump(report, open(os.path.join(SHOTS, 'render_report.json'), 'w'), indent=1)
for k, v in report.items(): print(k, v)
