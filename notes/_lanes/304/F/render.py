"""Seat 304-F render + checks (copied from lane M's render.py; paths and crops changed). Run from the repo
root at Dave's seat after ensure_env/seat_env. Full-page shots at 1440 and 390 wide, sliced for eyeballing;
layout checks printed as JSON."""
import os, json
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.getcwd()
PAGE = os.path.join(ROOT, 'notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html')
SHOTS = os.path.join(ROOT, 'notes/_lanes/304/F/shots')
os.makedirs(SHOTS, exist_ok=True)

CHECK = r"""() => {
  const de = document.documentElement, vw = de.clientWidth;
  const over = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('.dd-bar')) return;
    const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 1) over.push((el.tagName + '.' + (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className)).slice(0,60) + ' right=' + Math.round(r.right));
  });
  const clipped = [];
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (el.closest('.dd-bar') || el.tagName === 'svg' || el.closest('svg')) return;
    if ((cs.overflowX !== 'visible' || cs.overflowY !== 'visible') && (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) && el.tagName !== 'TEXTAREA')
      clipped.push(el.tagName + '.' + el.className);
  });
  const wide = getComputedStyle(document.querySelector('.diag .wide')).display;
  const tall = getComputedStyle(document.querySelector('.diag .tall')).display;
  const svg = document.querySelector(wide !== 'none' ? '.diag .wide' : '.diag .tall');
  const vb = svg.viewBox.baseVal, sr = svg.getBoundingClientRect();
  // svg text overflowing its box: compare each text's bbox to the rect before it
  const svgOver = [];
  svg.querySelectorAll('text').forEach(t => {
    const prev = t.previousElementSibling; let rect = null, p = t;
    while (p && !(p.tagName === 'rect')) p = p.previousElementSibling;
    if (!p) return; const bb = t.getBBox(), rb = p.getBBox();
    if (bb.x + bb.width > rb.x + rb.width - 2) svgOver.push(t.textContent + ' +' + Math.round(bb.x + bb.width - (rb.x + rb.width)));
  });
  return { vw, scrollW: de.scrollWidth, bodyScrollW: document.body.scrollWidth, docH: de.scrollHeight,
           overflowRight: over.slice(0, 20), overflowCount: over.length, clipped: clipped.slice(0, 20),
           diagram: { shown: wide !== 'none' ? 'wide' : 'tall', renderedW: Math.round(sr.width), scale: +(sr.width / vb.width).toFixed(3),
                      min12pxText: +(12 * sr.width / vb.width).toFixed(1), textOverBox: svgOver },
           ddBoxes: document.querySelectorAll('.dd-box').length, decisions: document.querySelectorAll('.decide > li').length,
           h1: document.querySelector('h1').textContent };
}"""

def slice_png(path, tag, h):
    im = Image.open(path); W, H = im.size; out = []
    for i, y in enumerate(range(0, H, h)):
        p = os.path.join(SHOTS, '%s-part%02d.png' % (tag, i + 1))
        im.crop((0, y, W, min(H, y + h))).save(p); out.append(os.path.basename(p))
    return out

report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for w, h, tag, sl in ((1440, 900, 'w1440', 1600), (390, 844, 'w390', 1600)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
        pg.goto('file://' + PAGE); pg.add_style_tag(content='.dd-bar{position:static!important}'); pg.wait_for_timeout(400)
        res = pg.evaluate(CHECK); res['errors'] = errs
        full = os.path.join(SHOTS, 'plan-304-v1-%s-full.png' % tag)
        pg.screenshot(path=full, full_page=True)
        res['full'] = os.path.basename(full); res['slices'] = slice_png(full, tag, sl)
        ctx2 = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg2 = ctx2.new_page(); pg2.goto('file://' + PAGE); pg2.add_style_tag(content='.dd-bar{position:static!important}'); pg2.wait_for_timeout(300)
        pg2.locator('.diag').screenshot(path=os.path.join(SHOTS, 'diagram-%s@2x.png' % tag))
        pg2.locator('#run4 table').screenshot(path=os.path.join(SHOTS, 'run4-table-%s@2x.png' % tag))
        pg2.locator('.stats').screenshot(path=os.path.join(SHOTS, 'stats-%s@2x.png' % tag))
        ctx2.close(); ctx.close()
        report[tag] = res
    b.close()
print(json.dumps(report, indent=1))
