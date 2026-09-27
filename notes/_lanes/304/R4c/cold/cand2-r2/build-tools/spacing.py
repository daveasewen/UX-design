"""Computed spacing and DOM geometry, every page, at the wide-desktop widths (1440 and 1920), light.
Reads boxes from the DOM (never a screenshot). usage: python3 spacing.py <out-dir>"""
import json, os, sys
from playwright.sync_api import sync_playwright
OUT = os.path.abspath(sys.argv[1])
PAGES = ['index', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
JS = r"""() => {
  const R = e => { const b = e.getBoundingClientRect(); return {x: b.left, y: b.top, r: b.right, b: b.bottom, w: b.width, h: b.height}; };
  const px = (e, p) => getComputedStyle(e).getPropertyValue(p);
  const out = {issues: [], gutters: {inner: [], outer: []}, wallPad: px(document.querySelector('.ceo-wall'), 'padding'),
               filterGap: px(document.querySelector('.ceo-filters'), 'gap'), mainGap: px(document.querySelector('.sh-main'), 'row-gap'),
               stackGaps: [...new Set([...document.querySelectorAll('.ceo-stack')].map(s => px(s, 'row-gap')))]};
  // tiles in each group: same-row tops/bottoms equal, column and row gutters
  document.querySelectorAll('section.tpl-group > .c-bento__grid').forEach(g => {
    const tiles = [...g.children].map(R);
    const rows = {}; tiles.forEach(t => { const k = Math.round(t.y); (rows[k] = rows[k] || []).push(t); });
    Object.values(rows).forEach(row => {
      const bs = row.map(t => Math.round(t.b)); if (Math.max(...bs) - Math.min(...bs) > 1) out.issues.push('ragged row bottoms ' + bs.join('/'));
      row.sort((a, b) => a.x - b.x); for (let i = 1; i < row.length; i++) out.gutters.inner.push(Math.round((row[i].x - row[i - 1].r) * 10) / 10);
    });
    const ys = Object.keys(rows).map(Number).sort((a, b) => a - b);
    for (let i = 1; i < ys.length; i++) { const prevB = Math.max(...rows[ys[i - 1]].map(t => t.b)); out.gutters.inner.push(Math.round((ys[i] - prevB) * 10) / 10); }
  });
  const groups = [...document.querySelectorAll('.tpl-wall > .c-bento__grid > section.tpl-group')].map(R);
  for (let i = 1; i < groups.length; i++) out.gutters.outer.push(Math.round((groups[i].y - groups[i - 1].b) * 10) / 10);
  // filter bar: every control's bottom edge on one line
  const fb = [...document.querySelectorAll('.ceo-filters > *')].map(e => Math.round(R(e.querySelector('.trigger, .seg, .btn') || e).b));
  if (Math.max(...fb) - Math.min(...fb) > 1) out.issues.push('filter controls bottoms differ ' + fb.join('/'));
  out.filterBottoms = fb;
  // horizontal overflow of the content column and of every tile
  const sc = document.querySelector('.sh-content'); if (sc.scrollWidth > sc.clientWidth + 1) out.issues.push('content column scrolls sideways ' + sc.scrollWidth + '>' + sc.clientWidth);
  document.querySelectorAll('.tpl-group > .c-bento__grid > .c-bento__tile').forEach(t => {
    [...t.querySelectorAll('*')].forEach(e => { const b = R(e), tb = R(t); if (b.w > 0 && (b.r > tb.r + 1 || b.x < tb.x - 1) && !e.closest('.dg-scroll') && !e.closest('.dv-tablepanel') && getComputedStyle(e).position !== 'fixed' && getComputedStyle(e).position !== 'absolute')
      out.issues.push('overflows its tile: ' + e.tagName + '.' + (e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className) + ' by ' + Math.round(Math.max(b.r - tb.r, tb.x - b.x)) + 'px'); });
  });
  // grid rows the geometry gate reports as overlapping: are they clipped by the grid's own scroll box?
  const ds = document.querySelector('.dg-scroll');
  if (ds) { const s = R(ds); const hidden = [...ds.querySelectorAll('tbody tr')].filter(tr => R(tr).y >= s.b - 1).length;
    out.grid = {scrollBox: Math.round(s.h), tableH: Math.round(R(ds.querySelector('table')).h), rowsBelowFold: hidden, overflowY: px(ds, 'overflow-y'),
      hintOnTop: (() => { const h = document.getElementById('dgHint'); if (!h) return null; const hb = R(h); const e = document.elementFromPoint(hb.x + 20, hb.y + 6); return e ? (e.closest('#dgHint') ? 'hint visible above clipped rows' : e.tagName) : 'offscreen'; })()}; }
  out.shell = {sh: Math.round(R(document.querySelector('.sh')).h), nav: Math.round(R(document.querySelector('.sh-body > .sn')).w)};
  return out;
}"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for w in (1440, 1920):
        pg = b.new_page(viewport={'width': w, 'height': 1000})
        for name in PAGES:
            pg.goto('file://%s/%s.html' % (OUT, name)); pg.wait_for_timeout(700)
            # scroll the shell's content column to the grid so elementFromPoint sees it
            pg.evaluate("(() => { const h = document.getElementById('dgHint'); if (h) h.scrollIntoView({block: 'center'}); })()"); pg.wait_for_timeout(150)
            r = pg.evaluate(JS); res['%s@%d' % (name, w)] = r
            inner = sorted(set(r['gutters']['inner'])); outer = sorted(set(r['gutters']['outer']))
            print('%-10s @%d inner gutters %s · outer %s · wall pad %s · filter gap %s · filter bottoms %s · issues %d %s %s' % (
                name, w, inner, outer, r['wallPad'], r['filterGap'], sorted(set(r['filterBottoms'])), len(r['issues']), r['issues'][:3], r.get('grid', '')))
        pg.close()
    b.close()
json.dump(res, open(os.path.join(os.path.dirname(OUT), 'proof', 'spacing.json'), 'w'), indent=1)
