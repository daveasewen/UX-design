"""W4b: patch _validate_geometry.py — part 1, the in-page measurement (COLLECT_JS)."""
import sys
P = "knowledge/_validate_geometry.py"
s = open(P).read()
def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:90])
    s = s.replace(old, new)

rep("""() => {
  const vw = window.innerWidth;""", """(opts) => {
  opts = opts || {};
  // CAUSE LEVERS (W4b #304, the mutation test of each repaired cause): legacyScroll restores the
  // R4b reading of scroll boxes, legacyLone skips the panels of one-panel groups.
  const LEGACY_SCROLL = !!opts.legacyScroll, LEGACY_LONE = !!opts.legacyLone, MARK_MAX = opts.markMax || 12, LOST_MIN = opts.lostMin || 0.35;
  const vw = window.innerWidth;""")

rep("""  // the part of a box that survives every clipping ancestor (overflow other than visible, any kind)
  const visibleRect = (el, r) => {
    let l = r.l, t = r.t, rr = r.r, b = r.b, e = el.parentElement;
    while (e && e !== document.documentElement) {
      const c = CS(e);
      if (c.overflowX !== 'visible' || c.overflowY !== 'visible') {""", """  const SCROLLS = v => /auto|scroll/.test(v);
  // the box a scroll container's content can be brought into view from (doc coords): from the
  // scroll ORIGIN (padding-box start minus the current scroll offset) out to its scrollable overflow
  const scrollArea = e => { const q = box(e), c = CS(e);
    const l = q.l + (parseFloat(c.borderLeftWidth) || 0) - e.scrollLeft, t = q.t + (parseFloat(c.borderTopWidth) || 0) - e.scrollTop;
    return {l, t, r: l + e.scrollWidth, b: t + e.scrollHeight}; };
  // the part of a box that survives every clipping ancestor (overflow other than visible, any kind)
  const visibleRect = (el, r) => {
    let l = r.l, t = r.t, rr = r.r, b = r.b, e = el.parentElement;
    while (e && e !== document.documentElement) {
      const c = CS(e);
      const sx_ = !LEGACY_SCROLL && SCROLLS(c.overflowX), sy_ = !LEGACY_SCROLL && SCROLLS(c.overflowY);
      if (sx_ || sy_) {
        // a SCROLL box: its content can be scrolled into view up to its scrollable overflow, never
        // past its START edges. Clip to the scroll AREA on a scrolling axis; above this box the only
        // question is whether the scroll box itself can be seen. (W4b #304: an app-shell page scrolls
        // an inner box; clipping to that box's VIEWPORT dropped every run below its fold, and G7 read
        // 0 on thirty colliding axis labels.)
        const sa = scrollArea(e), q = box(e), kx = sx_ ? sa : q, ky = sy_ ? sa : q;
        if (c.overflowX !== 'visible') { l = Math.max(l, kx.l); rr = Math.min(rr, kx.r); }
        if (c.overflowY !== 'visible') { t = Math.max(t, ky.t); b = Math.min(b, ky.b); }
        if (!(rr - l > 0.5 && b - t > 0.5)) return null;
        return visibleRect(e, q) ? {l, t, r: rr, b} : null;
      }
      if (c.overflowX !== 'visible' || c.overflowY !== 'visible') {""")

rep("""  for (const el of tileEls) { const t = tiles[tileIdx.get(el)]; if (!t.group) t.ink = inkOf(el); }
""", """  for (const el of tileEls) { const t = tiles[tileIdx.get(el)]; t.key = 'T' + t.id; if (!t.group) t.ink = inkOf(el); }
  // ── the LONE LEAF of a one-panel group (G6, W4b #304) ──
  // A tile wearing .c-bento with no wall inside is a GROUP of one: the reference bento wraps even a
  // one-panel row as a group. Its panel is a leaf, but the wall walk only enumerates tiles that sit
  // two-or-more in a grid, so the panel was never measured — the 351px hole under v1013-r2's ring
  // read G6 = 0. Measure the panel (the first painted or .c-bento__tile box inside, ≤4 levels),
  // or the group itself when it holds no such box.
  const leaves = [], leafIdx = new Map();
  const wallEls = [...wallIdx.keys()];
  if (!LEGACY_LONE) for (const el of tileEls) {
    const t = tiles[tileIdx.get(el)];
    if (!t.group || t.innerWall !== null) continue;
    if (wallEls.some(w => w !== el && el.contains(w))) continue;
    let leaf = null; const q = [[el, 0]];
    while (q.length && !leaf) { const [e, d] = q.shift(); if (d >= 4) continue;
      for (const k of inFlowKids(e)) {
        if (NOT_TILE.test(k.tagName) || k.namespaceURI !== 'http://www.w3.org/1999/xhtml') continue;
        const kb = box(k);
        if (kb.w >= 120 && kb.h >= 60 && (hasTok(k, 'c-bento__tile') || paints(k, effBg(e)))) { leaf = k; break; }
        q.push([k, d + 1]); } }
    const L = leaf || el;
    const pads = []; for (const e of chain(L)) { const c = CS(e); pads.push([c.paddingTop, c.paddingRight, c.paddingBottom, c.paddingLeft].map(parseFloat)); }
    const key = 'L' + leaves.length; leafIdx.set(L, key);
    leaves.push({key, of: t.id, sel: say(L), name: heading(L), rect: box(L), pads, ink: inkOf(L), planted: planted(L), lone: true});
  }
  // the tile (or lone leaf) a finding sits in, so a harness can count AFFECTED TILES, not instances
  const tileKey = el => { let e = el; while (e && e !== document.body) { if (leafIdx.has(e)) return leafIdx.get(e);
    if (tileIdx.has(e)) return 'T' + tileIdx.get(e); e = e.parentElement; } return null; };
""")

rep("""      if (/auto|scroll/.test(c.overflowX) || /auto|scroll/.test(c.overflowY)) break;   // a scroll box: content is reachable""",
"""      if (/auto|scroll/.test(c.overflowX) || /auto|scroll/.test(c.overflowY)) {
        // a scroll box: content past its END edges is reachable by scrolling; content past its START
        // edges is not. A y-axis label hung left of a chart's overflow-x:auto stage is cut for good
        // ("00 £m", W3b #304) — so on a scrolling axis the scroll AREA is a clip box, start edges only.
        if (!LEGACY_SCROLL) { const sa = scrollArea(e);
          clipper.push({el: e, x: /auto|scroll/.test(c.overflowX), y: /auto|scroll/.test(c.overflowY), l: sa.l, r: sa.r, t: sa.t, b: sa.b, scroll: true}); }
        break;
      }""")

rep("""        if (cp.y) { bot = Math.max(bot, (r.b - insBot) - cp.b); top = Math.max(top, cp.t - (r.t + insTop)); }
        if (cp.x) { side = Math.max(side, r.r - cp.r, cp.l - r.l); }""",
"""        if (cp.y) { if (!cp.scroll) bot = Math.max(bot, (r.b - insBot) - cp.b); top = Math.max(top, cp.t - (r.t + insTop)); }
        if (cp.x) { side = cp.scroll ? Math.max(side, cp.l - r.l) : Math.max(side, r.r - cp.r, cp.l - r.l); }""")

rep("""clips.push({text: s.slice(0, 40), sel: say(p), clipper: say(cp.el), same: cp.el === p, cuts: hit.map(h => [h[0], Math.round(h[1] * 10) / 10]), ink: metricOk, planted: planted(p)}); break; }""",
"""clips.push({text: s.slice(0, 40), sel: say(p), clipper: say(cp.el), same: cp.el === p, scroll: !!cp.scroll, cuts: hit.map(h => [h[0], Math.round(h[1] * 10) / 10]), ink: metricOk, planted: planted(p), tile: tileKey(p)}); break; }""")

rep("""w: Math.round(w), h: Math.round(h), planted: planted(a.p) || planted(b.p)}); if (overlaps.length >= 40) break; }""",
"""w: Math.round(w), h: Math.round(h), planted: planted(a.p) || planted(b.p), tile: tileKey(a.p) || tileKey(b.p)}); if (overlaps.length >= 40) break; }""")

rep("""  // ── horizontal overflow (G9) ──""", r"""  // ── charts: marks on every point (G11) and a chart lost in its own box (G12) — W4b #304 ──
  const dense = [], lost = [];
  const painted = d => { const c = CS(d); if (c.display === 'none' || c.visibility === 'hidden' || parseFloat(c.opacity) === 0) return false;
    if (d.closest('defs,clipPath,mask,marker,pattern,symbol')) return false;
    const fn = c.fill === 'none' || isT(c.fill), sn = c.stroke === 'none' || isT(c.stroke);
    return !(fn && sn) || d.tagName === 'text' || d.tagName === 'image' || d.tagName === 'use'; };
  const nverts = d => { const a = d.tagName === 'path' ? (d.getAttribute('d') || '') : (d.getAttribute('points') || '');
    return Math.floor((a.match(/-?\d*\.?\d+(?:e-?\d+)?/gi) || []).length / 2); };
  for (const s of document.querySelectorAll('svg')) {
    if (!shown(s) || (s.parentElement && s.parentElement.closest('svg'))) continue;      // outermost svg only
    const sb = box(s); if (sb.w < 160 || sb.h < 60) continue;
    const nm = heading(s.closest('figure,section,article,.c-bento__tile') || s);
    // G11: one series carrying a mark of one kind on every one of more than MARK_MAX points
    const lines = [...s.querySelectorAll('polyline,polygon,path')].filter(painted).map(nverts);
    const glyph = {}, letter = {};
    for (const d of s.querySelectorAll('circle,ellipse,polygon,rect,path')) {
      if (d.classList.contains('dv-hit') || !painted(d)) continue;
      if ((d.tagName === 'rect' || d.tagName === 'path') && !d.classList.contains('dv-mk')) continue;
      const r = d.getBoundingClientRect(); if (r.width < 3 || r.height < 3 || r.width > 16 || r.height > 16) continue;
      const g = d.closest('[data-series-group]'); const k = g ? 'g' + g.getAttribute('data-series-group') : 'f' + CS(d).fill;
      (glyph[k] = glyph[k] || []).push(d); }
    for (const d of s.querySelectorAll('text')) {
      const x = (d.textContent || '').trim(); if (!/^[A-Z]$/.test(x) || !painted(d)) continue;
      const g = d.closest('[data-series-group]'); const k = (g ? 'g' + g.getAttribute('data-series-group') : '') + x;
      (letter[k] = letter[k] || []).push(d); }
    for (const [k, ds] of Object.entries(glyph)) { const n = ds.length;
      // on EVERY point: a line or band in this chart has exactly n vertices (a line) or 2n (a closed band)
      if (n > MARK_MAX && lines.some(v => Math.abs(v - n) <= 1 || Math.abs(v - 2 * n) <= 2))
        dense.push({kind: 'marker', sel: say(s), name: nm, n, points: n, planted: planted(s), tile: tileKey(s)}); }
    for (const [k, ds] of Object.entries(letter)) { const n = ds.length;
      if (n > MARK_MAX && lines.some(v => v >= n))
        dense.push({kind: 'letter', letter: k.slice(-1), sel: say(s), name: nm, n, points: Math.max(...lines.filter(v => v >= n)), planted: planted(s), tile: tileKey(s)}); }
    // G12: the union of the chart's marks covers less than LOST_MIN of its own box
    if (sb.h >= 100 && !/^none/.test((s.getAttribute('preserveAspectRatio') || '').trim())) {
      let l = 1e9, t = 1e9, r = -1e9, b = -1e9, n = 0;
      for (const d of s.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect,text,image,use')) {
        if (d.classList.contains('dv-hit') || !painted(d)) continue;
        const q = box(d); if (q.w <= 0 && q.h <= 0) continue;
        l = Math.min(l, Math.max(q.l, sb.l)); t = Math.min(t, Math.max(q.t, sb.t)); r = Math.max(r, Math.min(q.r, sb.r)); b = Math.max(b, Math.min(q.b, sb.b)); n++; }
      if (n && r > l && b > t) { const frac = ((r - l) * (b - t)) / (sb.w * sb.h);
        if (frac < LOST_MIN) lost.push({sel: say(s), name: nm, frac: Math.round(frac * 1000) / 1000, iw: Math.round(r - l), ih: Math.round(b - t),
                                        w: Math.round(sb.w), h: Math.round(sb.h), planted: planted(s), tile: tileKey(s)}); } }
  }

  // ── horizontal overflow (G9) ──""")

rep("""          tables, clips, overlaps, overflow: off, stretched, fontOk};""",
"""          tables, clips, overlaps, overflow: off, stretched, fontOk, leaves, dense, lost};""")
open(P, "w").write(s)
print("JS patched")
