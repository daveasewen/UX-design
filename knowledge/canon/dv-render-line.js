/* dv-render-line — the LINE TYPE PARTIAL for the dv-render engine (s249-D4, built #259).
   Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by gen_component_partials.py.
   Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS TWO TYPES, both of Chart-line's `data-dv-type` vocabulary:
     line       — the cartesian value path, one series
     multiline  — the same routine with n series overlaid (Chart-line's second canvas)
   ONE ROUTINE. A single line and three overlaid lines are a SERIES COUNT, not a different chart —
   the same reason dv-render-bar registers `column` and `grouped-column` off one function. Both
   names are registered because `data-dv-type` and _validate_dataviz.py both read the author's own
   word for what the figure means.

   THE CATEGORY BAND IS THE COLUMN'S. A point sits at the CENTRE of its band — PL + i·band +
   band/2, band = plotW/nc — which is exactly where dv-render-bar puts a column's centre. That is
   not a detail: it is the whole reason a COMBO can hand this function a ctx and overlay a line on
   its own columns and have the two agree about where "Q3" is. Edge-to-edge point placement (the
   pre-engine baked geometry, PL → PL+plotW) would put every line point half a band left of its
   column, and the combo lane would have to re-implement this file to fix it.

   RULES ENACTED HERE:
     s116-D1   a marker is a hit target, so it carries a 24px HIT TIER — a transparent
               `circle.dv-hit` sized min(24, band), clamped so neighbouring categories cannot
               swallow each other. The VISIBLE glyph stays the kit's 11px shape (the promoted
               Chart-line receipt: "markers are focus/read points, not click targets"); the tier is
               the invisible target around it, which is what WCAG 2.5.8 actually measures and what
               `_validate_a11y.py` reads off the `<g>` wrapper (union of its shape children).
     §04.3     ≥2 series ⇒ TWO non-colour channels, both mirrored by the snippet's legend: the
               marker SHAPE cycles circle · square · diamond (the legend's sw-circle/sw-square/
               sw-diamond swatches are the same three), and a LETTER end-key lands at the end of
               each line (DV-D10 keeps Chart-line's end-key; only the combo's was ruled off).
     ds-026    every stroke and glyph fill is a SOLID palette token via ctx.fill(i) — var() only,
               no tint, no alpha (dv-017 / DEF-004 have no other legal answer).
     ds-030 /  the x of every mark is a FRACTION (data-fx on the marker <g>, data-fxs on the
     s248-D2   polyline) and its y is re-derived from the cached plot fraction, so the chart is
               responsive in BOTH axes with the viewBox pinned 1:1 — reflow, never viewBox stretch.
               Text and strokes keep their size: the glyphs are `.dv-mk` (dv-behaviour's
               size-preserving mark contract) and the strokes are vector-effect non-scaling.
     dv-line-011 straight lines: a <polyline>, which cannot carry a curve command.
     DEF-003   entry motion is CSS — `.dv-animate` draws the pathLength=2400 dash and fades each
               marker in on an authored animation-delay. The cadence below is the kit's OBSERVED
               Batch-8 easing, resampled to whatever category count the data actually has. No JS
               geometry animation, no scale physics, no press physics.

   ⚠ CORE REQUEST (reported, NOT worked around): dv-render.js clamps `if (lo > 0) { lo = 0; }`
   for every type. That is dv-bar-009's zero baseline, and dv-line-001's asymmetry says it MUST
   NOT fire on lines — a balance series of 82…104 should be free to fill the plot. A type's own
   `fn.domain` cannot escape it either, because the clamp runs after the domain call. Left alone;
   the zero-based line matches the promoted snippet, so nothing regressed. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;
  var KEYS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var R = 5.5;    /* the kit's marker glyph radius — 11px across, receipted sub-24 by design */
  /* The kit's Batch-8 EASED marker cadence, promoted verbatim from the proforma at twelve points.
     Resampled by fraction so eight categories or twenty keep the same shape of entry rather than
     a linear stagger; the last marker always lands with the 2400ms draw. */
  var CAD = [0, 369, 507, 616, 716, 815, 921, 1041, 1183, 1365, 1628, 2400];
  function delay(i, n) {
    if (n < 2) { return 0; }
    var t = i / (n - 1) * (CAD.length - 1), k = Math.floor(t);
    if (k >= CAD.length - 1) { return CAD[CAD.length - 1]; }
    return Math.round(CAD[k] + (CAD[k + 1] - CAD[k]) * (t - k));
  }

  /* The mark's words. `sep` is the only difference between the popover text (· separated, the
     kit's) and the accessible name (comma separated, so a screen reader reads a sentence). */
  function words(ctx, si, ci, v, sep) {
    return (ctx.series.length > 1 ? KEYS[si % 26] + sep + ctx.series[si].name + sep : '') +
      ctx.cats[ci] + ': ' + ctx.fmt(v);
  }
  /* The glyph: circle · square · diamond, cycling with the series index, mirroring the legend's
     swatch shapes. `.dv-mk` is dv-behaviour's size-preserving contract — the fit moves the centre
     and leaves the shape alone, which is why a square is authored as x/y and not width-fractions. */
  function glyph(si, x, y, fill) {
    var a = ' class="dv-mk" style="--sc:' + fill + '"', k = si % 3;
    if (k === 1) {
      return '<rect' + a + ' x="' + n1(x - R) + '" y="' + n1(y - R) + '" width="11" height="11"/>';
    }
    if (k === 2) {
      return '<polygon' + a + ' points="' + n1(x) + ',' + n1(y - 6.5) + ' ' + n1(x + 6.5) + ',' +
        n1(y) + ' ' + n1(x) + ',' + n1(y + 6.5) + ' ' + n1(x - 6.5) + ',' + n1(y) + '"/>';
    }
    return '<circle' + a + ' cx="' + n1(x) + '" cy="' + n1(y) + '" r="' + R + '"/>';
  }

  /* ---------- THE GEOMETRY. One polyline per series in the fit grammar's path form
     (data-fxs + data-ys), one focusable marker group per point. Order matters: the lines go down
     first, then the labels, then the markers and the end-keys on top — SVG has no z-index. */
  function line(ctx) {
    var ns = ctx.series.length, nc = ctx.cats.length;
    var band = ctx.plotW / nc;                      /* THE COLUMN'S BAND — see the header */
    var hit = Math.min(ctx.HIT, band) / 2;          /* s116-D1, clamped so bands don't overlap */
    if (hit < R) { hit = R; }
    var cx = [], marks = [], keys = [], i, si, ci;
    for (ci = 0; ci < nc; ci++) { cx.push(ctx.PL + ci * band + band / 2); }

    for (si = 0; si < ns; si++) {
      var fill = ctx.fill(si), pts = [], fxs = [], ys = [], sg = ' data-series-group="' + (si + 1) + '"';
      for (ci = 0; ci < nc; ci++) {
        var v = ctx.series[si].values[ci], x = cx[ci], y = ctx.vy(v), fx = f4(ctx.fx(x));
        pts.push(n1(x) + ',' + n1(y)); fxs.push(fx); ys.push(n1(y));
        marks.push('<g class="dv-marker"' + sg + ' tabindex="0" role="img" aria-label="' +
          esc(words(ctx, si, ci, v, ', ')) + '" data-tip="' + esc(words(ctx, si, ci, v, ' · ')) +
          '" data-fx="' + fx + '" data-x0="' + n1(x) + '" style="animation-delay:' +
          delay(ci, nc) + 'ms"><circle class="dv-hit" fill="none" pointer-events="all" cx="' +
          n1(x) + '" cy="' + n1(y) + '" r="' + n1(hit) + '"/>' + glyph(si, x, y, fill) + '</g>');
      }
      ctx.push('<polyline class="dv-series"' + sg + ' data-series-i="' + (si + 1) +
        '" pathLength="2400" fill="none" stroke="' + fill + '" stroke-width="2.5" ' +
        'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke" points="' +
        pts.join(' ') + '" data-fxs="' + fxs.join(' ') + '" data-ys="' + ys.join(' ') + '"/>');
      /* The end-key rides the LAST point's fraction with a fixed 10px offset, so it stays 10px
         from the line end on every width — and inside the plot, where the old baked x=580 sat on
         the frame edge. INK, not the series hue: 12px text in a series colour sits below the AA
         floor on dark, which is the day's own a11y line. */
      if (ns > 1) {
        var ly = ctx.vy(ctx.series[si].values[nc - 1]);
        keys.push('<text class="dv-endkey t-cm-chart-key"' + sg + ' fill="var(--ink)" x="' +
          n1(cx[nc - 1] + 10) + '" y="' + n1(ly + 4) + '" text-anchor="start" data-fx="' +
          f4(ctx.fx(cx[nc - 1])) + '" data-dx="10" data-dy="4">' + KEYS[si % 26] + '</text>');
      }
    }
    for (ci = 0; ci < nc; ci++) {
      ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(cx[ci]) +
        '" y="' + n1(ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + f4(ctx.fx(cx[ci])) + '">' +
        esc(ctx.cats[ci]) + '</text>');
    }
    for (i = 0; i < marks.length; i++) { ctx.push(marks[i]); }
    for (i = 0; i < keys.length; i++) { ctx.push(keys[i]); }
  }

  line.axis = 'y';
  T.line = T.multiline = line;
}());
