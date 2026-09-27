"""#305 B4: builds, then renders both pages at 1440 and 390, light and dark, at the seat. Run from the repo root:
export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/305/B4/render.py [page1|page2]"""
import os, json, sys, subprocess
ROOT = os.getcwd()
subprocess.check_call([sys.executable, 'notes/_lanes/305/B4/build.py'])
from playwright.sync_api import sync_playwright
PAGES = {'page1': 'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html', 'page2': 'notes/_SCAN-305-parked-questions-2026-09-27-v1.html'}
which = sys.argv[1:] or list(PAGES)
SHOTS = os.path.join(ROOT, 'notes/_lanes/305/B4/shots'); os.makedirs(SHOTS, exist_ok=True)
CHECK = r"""() => { const vw = document.documentElement.clientWidth; const off = [];
  for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed') off.push(el.tagName + '.' + (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className||'').toString().slice(0,40)); }
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
  return { scrollWidth: document.documentElement.scrollWidth, vw, off: off.slice(0,10), broken, imgs: document.images.length,
    boxes: document.querySelectorAll('.dd-box').length, ticks: document.querySelectorAll('input[data-k]').length,
    rows: new Set([...document.querySelectorAll('.pr')].map(e=>e.dataset.id)).size, height: document.documentElement.scrollHeight,
    bg: getComputedStyle(document.body).backgroundColor }; }"""
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for key in which:
        for w in (1440, 390):
            for mode in ('light', 'dark'):
                errs = []
                pg = b.new_page(viewport={'width': w, 'height': 1000}, color_scheme=mode)
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.goto('file://' + os.path.join(ROOT, PAGES[key])); pg.wait_for_timeout(700)
                pg.evaluate("() => document.querySelectorAll('img[loading]').forEach(i => i.loading='eager')")
                pg.evaluate("async () => { window.scrollTo(0, document.body.scrollHeight); await new Promise(r=>setTimeout(r,700)); window.scrollTo(0,0); }")
                pg.wait_for_timeout(500)
                r = pg.evaluate(CHECK); r['pageerrors'] = errs
                tag = '%s-w%d-%s' % (key, w, mode); report[tag] = r
                h = r['height']; y = 0; n = 0
                while y < h and n < 60:
                    pg.evaluate('window.scrollTo(0,%d)' % y); pg.wait_for_timeout(120)
                    pg.screenshot(path=os.path.join(SHOTS, '%s-part%02d.png' % (tag, n)))
                    y += 1000; n += 1
                r['parts'] = n
                pg.close()
    b.close()
json.dump(report, open(os.path.join(SHOTS, 'render_report-%s.json' % '-'.join(which)), 'w'), indent=1)
for k, v in report.items(): print(k, {x: v[x] for x in ('scrollWidth', 'vw', 'off', 'broken', 'imgs', 'boxes', 'ticks', 'rows', 'height', 'pageerrors', 'parts', 'bg')})
