// probe.js — the render-phase measurement, evaluated in the page. Arg: {themeVars:[...], full:bool}
(arg) => {
  const R = {};
  const vis = el => { if (!el) return false; const s = getComputedStyle(el); const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.01 && r.width > 0 && r.height > 0; };
  const rootCS = getComputedStyle(document.documentElement);
  const desc = el => (el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
      (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : '')).slice(0, 90);
  R.title = document.title;
  R.root = { cls: document.documentElement.className, theme: document.documentElement.getAttribute('data-theme'),
             apollo: document.documentElement.getAttribute('data-apollo-theme') };
  R.h_overflow = Math.max(0, document.documentElement.scrollWidth - window.innerWidth);
  R.doc_h = document.documentElement.scrollHeight;
  // ---- theme tokens, and how many vars the theme attribute actually moves
  R.theme_tokens = {};
  for (const n of (arg.tokenNames || [])) R.theme_tokens[n] = rootCS.getPropertyValue(n).trim();
  const tv = arg.themeVars || [];
  const before = tv.map(n => rootCS.getPropertyValue(n).trim());
  const had = document.documentElement.getAttribute('data-apollo-theme');
  let changed = null;
  if (had !== null) {
    document.documentElement.removeAttribute('data-apollo-theme');
    const after = tv.map(n => getComputedStyle(document.documentElement).getPropertyValue(n).trim());
    document.documentElement.setAttribute('data-apollo-theme', had);
    changed = tv.filter((n, i) => before[i] !== after[i]).length;
  }
  R.theme_vars_changed = { attr: had, changed, of: tv.length };
  // ---- charts
  const figs = [...document.querySelectorAll('figure.dv, figure[data-dv-type]')];
  R.charts = figs.map((f, i) => {
    const r = f.getBoundingClientRect();
    const svg = f.querySelector('svg.dv-svg') || f.querySelector('svg');
    let marks = 0, mb = null;
    if (svg) {
      for (const e of svg.querySelectorAll('rect,path,circle,line,polyline,polygon,ellipse')) {
        const cl = (e.getAttribute('class') || '');
        if (/dv-grid|dv-axis|dv-base|dv-tick/.test(cl) || e.closest('.dv-grid,.dv-axis,defs,clipPath,mask')) continue;
        const b = e.getBoundingClientRect();
        if (b.width <= 0 && b.height <= 0) continue;
        marks++;
        mb = mb ? { l: Math.min(mb.l, b.left), t: Math.min(mb.t, b.top), r: Math.max(mb.r, b.right), b: Math.max(mb.b, b.bottom) }
                : { l: b.left, t: b.top, r: b.right, b: b.bottom };
      }
    }
    const sr = svg ? svg.getBoundingClientRect() : r;
    // CLIP 1: an ancestor that hides overflow cuts the figure (or its svg)
    let clip = null;
    const target = svg ? sr : r;
    for (let a = f.parentElement; a && a !== document.body; a = a.parentElement) {
      const s = getComputedStyle(a);
      if (/(hidden|clip)/.test(s.overflowX + ' ' + s.overflowY)) {
        const ar = a.getBoundingClientRect();
        const ex = Math.max(ar.left - target.left, target.right - ar.right, ar.top - target.top, target.bottom - ar.bottom);
        if (ex > 2) { clip = { by: desc(a), px: Math.round(ex) }; break; }
      }
    }
    // CLIP 2: the figure itself hides overflow and its content is taller/wider
    if (!clip) {
      const s = getComputedStyle(f);
      if (/(hidden|clip)/.test(s.overflowX + ' ' + s.overflowY) && (f.scrollHeight - f.clientHeight > 2 || f.scrollWidth - f.clientWidth > 2))
        clip = { by: 'figure overflow', px: Math.max(f.scrollHeight - f.clientHeight, f.scrollWidth - f.clientWidth) };
    }
    // CLIP 3: marks outside the svg viewport (svg clips by default)
    if (!clip && svg && mb) {
      const ex = Math.max(sr.left - mb.l, mb.r - sr.right, sr.top - mb.t, mb.b - sr.bottom);
      if (ex > 3 && getComputedStyle(svg).overflow !== 'visible') clip = { by: 'svg viewport', px: Math.round(ex) };
    }
    const tbl = f.querySelector('table');
    const legend = !!(f.querySelector('.dv-legend,[class*="legend"]') ||
                      (f.parentElement && f.parentElement.querySelector(':scope > .dv-legend, :scope > [class*="legend"], :scope .cn-legend')));
    return { i, id: f.id || '', type: f.getAttribute('data-dv-type') || '', w: Math.round(r.width), h: Math.round(r.height),
             svg_w: Math.round(sr.width), svg_h: Math.round(sr.height), marks, visible: vis(f),
             legend, table: !!tbl, table_rows: tbl ? tbl.querySelectorAll('tbody tr').length : 0,
             clipped: !!clip, clip_by: clip && clip.by, clip_px: clip && clip.px };
  });
  // ---- records and pager
  R.max_table_rows = Math.max(0, ...[...document.querySelectorAll('table')].filter(t => !t.closest('figure.dv'))
                                   .map(t => t.querySelectorAll('tbody tr').length));
  R.pager = !!document.querySelector('.cn-pagination, [aria-label*="pagination" i], [aria-label*="page" i] button, nav[aria-label*="page" i]');
  // ---- clipped elements (not charts): overflow hidden/clip that actually hides content
  const clippedEls = [];
  for (const el of document.querySelectorAll('body *')) {
    if (clippedEls.length > 400) break;
    const s = getComputedStyle(el);
    if (s.display === 'inline' || !/(hidden|clip)/.test(s.overflowX + s.overflowY)) continue;
    if (el.classList.contains('sr-only') || el.clientHeight <= 2 || el.clientWidth <= 2 || !vis(el)) continue;
    const dy = el.scrollHeight - el.clientHeight, dx = el.scrollWidth - el.clientWidth;
    if (dy > 2 || dx > 2) clippedEls.push({ el: desc(el), dy, dx, ellipsis: s.textOverflow === 'ellipsis' });
  }
  R.clipped_elements = { count: clippedEls.filter(c => !c.ellipsis).length, ellipsis: clippedEls.filter(c => c.ellipsis).length,
                         sample: clippedEls.filter(c => !c.ellipsis).slice(0, 10) };
  // ---- errors are collected by the driver; components rendered
  R.components_rendered = [...new Set([...document.querySelectorAll('[class*="cn-"]')].filter(vis)
      .flatMap(e => (e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(/\s+/)).filter(c => /^cn-[a-z]/.test(c)))].sort();
  if (!arg.full) return R;
  // ---- native geometry signals (advisory; 4b owns the geometry score)
  const G = { grids: [], dead_tiles: [], unshared_bottoms: 0, unequal_gutter_grids: 0, filter_table_mismatch: [] };
  let grids = [...document.querySelectorAll('.c-bento__grid')].filter(vis);
  if (!grids.length) grids = [...document.querySelectorAll('main *, body > *')].filter(g => {
      const s = getComputedStyle(g); if (s.display !== 'grid' || !vis(g)) return false;
      const k = [...g.children].filter(c => vis(c) && c.getBoundingClientRect().width >= 120); return k.length >= 3; }).slice(0, 12);
  for (const g of grids) {
    const tiles = [...g.children].filter(vis).map(t => { const r = t.getBoundingClientRect(); return { t, l: r.left, r: r.right, top: r.top, b: r.bottom, h: r.height, w: r.width }; });
    const rows = {};
    for (const x of tiles) { const k = Math.round(x.top / 3); (rows[k] = rows[k] || []).push(x); }
    const gut = []; let unshared = 0;
    for (const k in rows) {
      const row = rows[k].sort((a, b) => a.l - b.l);
      for (let i = 1; i < row.length; i++) gut.push(Math.round(row[i].l - row[i - 1].r));
      const hs = row.map(x => x.h); const bs = row.map(x => x.b);
      if (row.length > 1 && Math.max(...bs) - Math.min(...bs) > 2) {
        // bottoms differ: a defect unless every height is a whole number of row units (a deliberate span)
        const gap = parseFloat(getComputedStyle(g).rowGap) || 0; const unit = Math.min(...hs);
        const offGrid = hs.some(h => { const k = Math.max(1, Math.round((h + gap) / (unit + gap))); return Math.abs(k * (unit + gap) - gap - h) > 3; });
        if (offGrid) unshared++;
      }
    }
    const vg = []; const tops = [...new Set(tiles.map(x => Math.round(x.top)))].sort((a, b) => a - b);
    for (let i = 1; i < tops.length; i++) {
      const above = tiles.filter(x => Math.round(x.top) === tops[i - 1]); const minB = Math.min(...above.map(x => x.b));
      if (minB < tops[i]) vg.push(Math.round(tops[i] - Math.max(...above.filter(x => x.b <= tops[i] + 1).map(x => x.b).concat([minB]))));
    }
    const gpos = gut.filter(x => x >= 0);
    const uneq = gpos.length > 1 && Math.max(...gpos) - Math.min(...gpos) > 1;
    if (uneq) G.unequal_gutter_grids++;
    G.unshared_bottoms += unshared;
    G.grids.push({ grid: desc(g), tiles: tiles.length, gutters: [...new Set(gpos)].sort((a, b) => a - b), row_gaps: [...new Set(vg)].sort((a, b) => a - b), unequal_gutters: uneq, unshared_bottom_rows: unshared });
    for (const x of tiles) {
      let lowest = 0;
      const walk = el => { const leaf = el.children.length === 0 || el.tagName.toLowerCase() === 'svg';
        if (leaf && (el.textContent.trim().length || el.tagName.toLowerCase() === 'svg' || /^(IMG|HR|INPUT)$/.test(el.tagName)) && !el.classList.contains('sr-only')) {
          const b = el.getBoundingClientRect(); if (b.height > 0 && getComputedStyle(el).visibility !== 'hidden' && b.bottom > lowest && b.bottom <= x.b + 1) lowest = b.bottom; }
        if (el.tagName.toLowerCase() !== 'svg') [...el.children].forEach(walk); };
      [...x.t.children].forEach(walk);
      const dead = lowest ? x.b - lowest : x.h;
      if (dead > 48 && dead > 0.35 * x.h) G.dead_tiles.push({ tile: desc(x.t), dead_px: Math.round(dead), tile_h: Math.round(x.h) });
    }
  }
  for (const fb of [...document.querySelectorAll('.cn-filter-toolbar-bar, .ftb-outer, [class*="filter-bar"]')].filter(vis)) {
    const host = fb.closest('.c-bento__tile, section, article') || fb.parentElement;
    const tb = host && [...host.querySelectorAll('table, .dg, .cn-data-grid')].filter(vis)[0];
    if (tb) { const a = fb.getBoundingClientRect(), b = tb.getBoundingClientRect();
      if (Math.abs(a.width - b.width) > 4 || Math.abs(a.left - b.left) > 4) G.filter_table_mismatch.push({ bar: desc(fb), bar_w: Math.round(a.width), table_w: Math.round(b.width), dx: Math.round(a.left - b.left) }); }
  }
  const btnH = [...document.querySelectorAll('button, .btn, [role="button"]')].filter(vis).map(b => Math.round(b.getBoundingClientRect().height)).sort((a, b) => a - b);
  const thH = [...document.querySelectorAll('th')].filter(vis).map(b => Math.round(b.getBoundingClientRect().height)).sort((a, b) => a - b);
  G.own_size_hint = { buttons: btnH.length, button_h_min: btnH[0] || null, button_h_median: btnH[Math.floor(btnH.length / 2)] || null,
                      th: thH.length, th_h_min: thH[0] || null, th_h_median: thH[Math.floor(thH.length / 2)] || null };
  G.summary = { grids: G.grids.length, unequal_gutter_grids: G.unequal_gutter_grids, unshared_bottom_rows: G.unshared_bottoms,
                dead_tiles: G.dead_tiles.length, filter_table_mismatch: G.filter_table_mismatch.length, own_size_hint: G.own_size_hint };
  R.geometry = G;
  // ---- rendered a11y
  const ctrls = [...document.querySelectorAll('button, a[href], input:not([type="hidden"]), select, textarea, [role="button"], [role="tab"], [role="switch"], [role="checkbox"], [role="menuitem"], [role="link"], [role="option"]')].filter(vis);
  const nameOf = el => {
    const al = el.getAttribute('aria-label'); if (al && al.trim()) return al.trim();
    const lb = el.getAttribute('aria-labelledby'); if (lb) { const t = lb.split(/\s+/).map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim(); if (t) return t; }
    if (el.id) { const l = document.querySelector('label[for="' + CSS.escape(el.id) + '"]'); if (l && l.textContent.trim()) return l.textContent.trim(); }
    const wl = el.closest('label'); if (wl && wl.textContent.trim()) return wl.textContent.trim();
    const t = (el.innerText || el.textContent || '').trim(); if (t) return t;
    if (el.title && el.title.trim()) return el.title.trim();
    const img = el.querySelector('img[alt]'); if (img && img.alt.trim()) return img.alt.trim();
    const st = el.querySelector('svg title'); if (st && st.textContent.trim()) return st.textContent.trim();
    return '';
  };
  const unnamed = ctrls.filter(e => !nameOf(e));
  const small = ctrls.filter(e => { const r = e.getBoundingClientRect(); const inl = getComputedStyle(e).display === 'inline' && e.tagName === 'A';
    return !inl && (r.width < 24 || r.height < 24); });
  const ids = {}; for (const e of document.querySelectorAll('[id]')) ids[e.id] = (ids[e.id] || 0) + 1;
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).map(h => +h.tagName[1]);
  let skips = 0; for (let i = 1; i < hs.length; i++) if (hs[i] > hs[i - 1] + 1) skips++;
  R.a11y = { summary: { controls: ctrls.length, unnamed_controls: unnamed.length, small_targets: small.length,
             img_no_alt: [...document.querySelectorAll('img:not([alt])')].length, lang: document.documentElement.lang || null,
             duplicate_ids: Object.values(ids).filter(n => n > 1).length, h1: hs.filter(h => h === 1).length, heading_skips: skips,
             landmarks: { main: document.querySelectorAll('main,[role=main]').length, nav: document.querySelectorAll('nav,[role=navigation]').length } },
             unnamed_sample: unnamed.slice(0, 8).map(desc), small_sample: small.slice(0, 8).map(e => desc(e) + ' ' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height)) };
  return R;
}
