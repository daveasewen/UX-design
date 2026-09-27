"""Seat 304-W5b render: builds the page, then renders it at 1440 and 390 with Playwright at Dave's seat
(executable_path = $RENDER_SHELL, file:// goto), checks scroll width, off-edge elements, clipped text
boxes, broken images and page errors, and writes shots to notes/_lanes/304/W5b/shots/. Run from the repo root."""
import os, json, subprocess, sys
ROOT = os.getcwd()
subprocess.check_call([sys.executable, 'notes/_lanes/304/W5b/build.py'])
from playwright.sync_api import sync_playwright
PAGE = os.path.join(ROOT, 'notes/_SITTING-304-tuesday-2026-09-29-v1.html')
SHOTS = os.path.join(ROOT, 'notes/_lanes/304/W5b/shots'); os.makedirs(SHOTS, exist_ok=True)
CHECK = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const off = [], clipped = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1) off.push(el.tagName + '.' + (el.className||'').toString().slice(0,40));
    const cs = getComputedStyle(el);
    if ((cs.overflow === 'hidden' || cs.overflowY === 'hidden') && el.scrollHeight > el.clientHeight + 2 && !el.classList.contains('crop') && !el.matches('textarea'))
      clipped.push(el.tagName + '.' + (el.className||'').toString().slice(0,40) + ' ' + el.scrollHeight + '>' + el.clientHeight);
  }
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
  return { scrollWidth: document.documentElement.scrollWidth, vw, off: off.slice(0,10), clipped: clipped.slice(0,10),
           broken, boxes: document.querySelectorAll('.dd-box').length, calls: document.querySelectorAll('.decide > li').length,
           height: document.documentElement.scrollHeight };
}
"""
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for w in (1440, 390):
        errs = []
        pg = b.new_page(viewport={'width': w, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://' + PAGE); pg.wait_for_timeout(800)
        # force lazy images to load for the check
        pg.evaluate("() => document.querySelectorAll('img[loading]').forEach(i => i.loading='eager')")
        pg.evaluate("async () => { window.scrollTo(0, document.body.scrollHeight); await new Promise(r=>setTimeout(r,600)); window.scrollTo(0,0); }")
        pg.wait_for_timeout(600)
        r = pg.evaluate(CHECK); r['pageerrors'] = errs
        report[w] = r
        if r['height'] < 14000:
            pg.screenshot(path=os.path.join(SHOTS, 'sitting-w%d-full.png' % w), full_page=True)
        else:
            r['full_shot'] = 'skipped, page taller than 14000px; slices only'
        # sliced shots for looking
        h = r['height']; y = 0; n = 0
        while y < h and n < 40:
            pg.evaluate('window.scrollTo(0,%d)' % y); pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(SHOTS, 'sitting-w%d-part%02d.png' % (w, n)))
            y += 1000; n += 1
        pg.close()
    b.close()
json.dump(report, open(os.path.join(SHOTS, 'render_report.json'), 'w'), indent=1)
print(json.dumps(report, indent=1))
