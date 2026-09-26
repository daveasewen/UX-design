"""Seat 304-R6a: build the three decision pages, then render each at 1440 and 390 (full page, sliced),
and print layout checks as JSON: horizontal overflow, clipped boxes, broken images, decision boxes.
Run from the repo root at Dave's seat after ensure_env + seat_env."""
import os, sys, json, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.getcwd()
subprocess.run([sys.executable, 'notes/_lanes/304/R6a/build.py'], check=True)
SHOTS = os.path.join(ROOT, 'notes/_lanes/304/R6a/shots'); os.makedirs(SHOTS, exist_ok=True)
PAGES = {'schema': 'notes/_DECIDE-304-schema-2026-09-26-v1.html',
         'delivery': 'notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html',
         'when': 'notes/_DECIDE-304-when-rules-2026-09-26-v1.html'}
only = sys.argv[1:] or list(PAGES)
CHECK = r"""() => {
  const de = document.documentElement, vw = de.clientWidth, over = [], clipped = [], broken = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('.dd-bar')) return;
    const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1) over.push((el.tagName + '.' + el.className).slice(0,60) + ' right=' + Math.round(r.right));
    const cs = getComputedStyle(el);
    if ((cs.overflowX !== 'visible' || cs.overflowY !== 'visible') && el.tagName !== 'TEXTAREA' && el.tagName !== 'BODY' && el.tagName !== 'HTML'
        && (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1)) clipped.push(el.tagName + '.' + el.className);
  });
  document.querySelectorAll('img').forEach(i => { if (!i.complete || !i.naturalWidth) broken.push(i.getAttribute('src')); });
  return { vw, scrollW: de.scrollWidth, docH: de.scrollHeight, overflowCount: over.length, overflow: over.slice(0, 12), clipped: clipped.slice(0, 12),
           broken, ddBoxes: document.querySelectorAll('.dd-box').length, decisions: document.querySelectorAll('.decide > li').length,
           titles: [...document.querySelectorAll('.dd-box .dd-label')].map(x => x.textContent) };
}"""
def slice_png(path, tag, h):
    im = Image.open(path); W, H = im.size; out = []
    for i, y in enumerate(range(0, H, h)):
        p = os.path.join(SHOTS, '%s-part%02d.png' % (tag, i + 1))
        im.crop((0, y, W, min(H, y + h))).save(p); out.append(os.path.basename(p))
    return out
rep = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for key in only:
        page = os.path.join(ROOT, PAGES[key])
        for w, h, sl in ((1440, 900, 1800), (390, 844, 1800)):
            tag = '%s-w%d' % (key, w)
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto('file://' + page); pg.add_style_tag(content='.dd-bar{position:static!important}')
            pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(800)
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(600); pg.evaluate("window.scrollTo(0,0)")
            res = pg.evaluate(CHECK); res['errors'] = errs
            full = os.path.join(SHOTS, tag + '-full.png'); pg.screenshot(path=full, full_page=True)
            res['slices'] = slice_png(full, tag, sl)
            rep[tag] = res; ctx.close()
    b.close()
print(json.dumps(rep, indent=1))
