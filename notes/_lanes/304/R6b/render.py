"""Seat 304-R6b render + checks for the three decision pages. Run from the repo root at Dave's seat, in the
same call as ensure_env + seat_env. Full-page shots at 1440 and 390, sliced; layout checks printed as JSON.
The pages use the house Helvetica stack by design; the badge photographs inside the CI page were taken in
the forced HSBC face by render_badge.py."""
import os, json
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.getcwd(); SHOTS = os.path.join(ROOT, 'notes/_lanes/304/R6b/shots'); os.makedirs(SHOTS, exist_ok=True)
PAGES = [('ci', 'notes/_DECIDE-304-ci-calls-2026-09-26-v1.html'), ('stamps', 'notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html'),
         ('house', 'notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html')]
CHECK = r"""() => {
  const de = document.documentElement, vw = de.clientWidth, over = [], clipped = [], tight = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('.dd-bar')) return;
    const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1) over.push((el.tagName + '.' + el.className).slice(0, 60) + ' right=' + Math.round(r.right));
    const cs = getComputedStyle(el);
    if ((cs.overflowX !== 'visible' || cs.overflowY !== 'visible') && (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) && el.tagName !== 'TEXTAREA')
      clipped.push(el.tagName + '.' + el.className);
    // descender risk: text elements whose line-height is under 1.2x font-size
    if (el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) {
      const fs = parseFloat(cs.fontSize), lh = parseFloat(cs.lineHeight);
      if (lh && lh < fs * 1.08) tight.push(el.tagName + '.' + el.className + ' fs=' + fs + ' lh=' + lh);
    }
  });
  const imgs = [...document.images].map(i => ({src: i.getAttribute('src').split('/').pop(), ok: i.complete && i.naturalWidth > 0}));
  const links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
  return { vw, scrollW: de.scrollWidth, docH: de.scrollHeight, overflowCount: over.length, overflow: over.slice(0, 10),
           clipped: clipped.slice(0, 10), tightLines: [...new Set(tight)].slice(0, 10), imgs, links,
           ddBoxes: document.querySelectorAll('.dd-box').length, decisions: document.querySelectorAll('.decide > li').length,
           h1: document.querySelector('h1').textContent };
}"""
def slice_png(path, tag, h):
    im = Image.open(path); W, H = im.size; out = []
    for i, y in enumerate(range(0, H, h)):
        p = os.path.join(SHOTS, '%s-part%02d.png' % (tag, i + 1)); im.crop((0, y, W, min(H, y + h))).save(p); out.append(os.path.basename(p))
    return out
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for key, rel in PAGES:
        for w, h in ((1440, 900), (390, 844)):
            tag = '%s-w%d' % (key, w)
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto('file://' + os.path.join(ROOT, rel)); pg.add_style_tag(content='.dd-bar{position:static!important}'); pg.wait_for_timeout(500)
            res = pg.evaluate(CHECK); res['errors'] = errs
            full = os.path.join(SHOTS, '%s-full.png' % tag); pg.screenshot(path=full, full_page=True)
            res['slices'] = slice_png(full, tag, 1500)
            report[tag] = res; ctx.close()
    b.close()
print(json.dumps(report, indent=1))
