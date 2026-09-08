/* dv-render-bar — the BAR TYPE PARTIAL for the dv-render engine (s249-D4, built #259).
   Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by gen_component_partials.py.
   Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS FOUR TYPES, all four of the Chart-bar meta's `orientation` enum:
     column            — vertical, single series
     grouped-column    — vertical, n series side by side in each band (D-Q3)
     stacked-column    — vertical, n series stacked to the band total (D-Q3)
     bar               — HORIZONTAL, value runs across x (axis "x")

   ONE ROUTINE, TWO FLAGS. All four are `bars(ctx, horiz, stack)`. That is not compression: a
   grouped column and a horizontal bar are the SAME arithmetic with the band axis and the value
   axis exchanged, and writing them twice is how the two copies drift. `column` and
   `grouped-column` are literally the same registration — one series or six is a band count, not
   a different chart — but both names are registered because `data-dv-type` and the dataviz gate
   both read the author's word for what they meant.

   THE REFERENCE IMPLEMENTATION. This is the file the five sibling type partials are written
   against: it touches nothing in dv-render.js, registers through `dvRender.types`, and takes
   everything it needs — scale, formatting, palette, escaping, the plot frame — off `ctx`.

   RULES ENACTED HERE:
     dv-004    2px of REAL geometry between adjacent filled blocks (grouped neighbours AND
               stacked segments) — a gap, never a painted surface-coloured stroke. The gap is cut
               off the segment BELOW the join, so the topmost segment still reads its true total.
     s116-D1   a bar is a hit target (tabindex=0 + data-tip), so its THICKNESS is floored at 24px
               wherever the band can afford it; below that the band wins, because overlapping
               marks are a worse answer than a small one. Bar LENGTH is the data and is floored
               only at 1px of visible ink.
     DV-D09    the horizontal default fill is data/series/3 — orientation-distinct from the
               column's series/1 — for a single unroled series only; a roled series keeps the
               s184-D3 status ramp and a multi-series bar keeps the palette order.
     dv-bar-007 negatives are for VERTICAL columns only: a negative value on a horizontal bar
               throws, named, rather than drawing left of the baseline.
     §04.3     ≥2 series ⇒ an on-chart LETTER key (.dv-barkey, A/B/C…) per mark, so colour is
               never the only channel. Bar marks are rects; letters are their non-colour channel.
     DEF-003   entry motion is CSS: `.dv-animate` on the figure + data-grow="up"/"right" and a
               45ms stagger in animation-delay. No JS geometry animation. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;
  var KEYS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  /* The mark's words. `sep` is the only difference between the popover text (· separated, the
     kit's) and the accessible name (comma separated, so a screen reader reads a sentence). */
  function words(ctx, si, ci, v, sep) {
    return (ctx.series.length > 1 ? KEYS[si % 26] + sep + ctx.series[si].name + sep : '') +
      ctx.cats[ci] + ': ' + ctx.fmt(v);
  }
  /* The thickness of one mark inside one band: share the band between n lanes with a 2px gap
     between neighbours (dv-004), lift to the 24px hit floor when the band can pay for it
     (s116-D1), and keep a 28% band gutter so neighbouring CATEGORIES read as separate. */
  function thickness(ctx, band, n) {
    var t = (band * 0.72 - ctx.GAP * (n - 1)) / n;
    if (t < ctx.HIT && ctx.HIT * n + ctx.GAP * (n - 1) <= band) { t = ctx.HIT; }
    return t < 1 ? 1 : t;
  }
  /* An on-chart series key. `inset` = drawn INSIDE a horizontal bar, where the 8px offset from
     the baseline must stay 8px on every width — hence data-fx="0" + data-dx, not a fraction. */
  function letter(ctx, si, x, y, inset) {
    return '<text class="dv-barkey t-cm-chart-key" data-series-group="' + (si + 1) +
      '" fill="var(--ink)" x="' + n1(x) + '" y="' + n1(y) + '" text-anchor="' +
      (inset ? 'start" data-fx="0" data-dx="8' : 'middle" data-fx="' + f4(ctx.fx(x))) +
      '">' + KEYS[si % 26] + '</text>';
  }

  /* ---------- THE GEOMETRY. horiz = the value axis runs across x (the core has already drawn
     vertical gridlines for it); stack = the series pile up to the band total instead of sitting
     side by side. Bars grow from the ZERO line, not from the frame edge, so a domain that spans
     zero draws negatives downward with no special case (dv-bar-009 keeps zero in the domain). */
  function bars(ctx, horiz, stack) {
    ctx.horiz = horiz;                  /* picks data-grow="right" over "up" for the CSS entry */
    var ns = ctx.series.length, nc = ctx.cats.length;
    var band = (horiz ? ctx.plotH : ctx.plotW) / nc;
    var lanes = stack ? 1 : ns;
    var th = thickness(ctx, band, lanes);
    var pad = (band - (th * lanes + ctx.GAP * (lanes - 1))) / 2;
    var keys = [], order = 0, ci, si;
    for (ci = 0; ci < nc; ci++) {
      var b0 = (horiz ? ctx.PT : ctx.PL) + ci * band + pad, run = 0;
      for (si = 0; si < ns; si++) {
        var v = ctx.series[si].values[ci];
        if (horiz && v < 0) {
          throw new Error('dv-render-bar: dv-bar-007 — "' + ctx.cats[ci] + '" is ' + v +
            ' and negatives are for VERTICAL columns only; use type "column" for signed data');
        }
        var lane = b0 + (stack ? 0 : si * (th + ctx.GAP));
        var from = stack ? run : 0, to = stack ? run + v : v;
        var cut = stack && si < ns - 1 ? ctx.GAP : 0;   /* dv-004 — 2px off the block BELOW a join */
        var x, y, w, h, cx, cy;
        if (horiz) {
          y = lane; h = th;
          x = ctx.PL + ctx.vf(from) * ctx.plotW;
          w = (ctx.vf(to) - ctx.vf(from)) * ctx.plotW;
          if (w - cut > 1) { w -= cut; }
          if (w < 1) { w = 1; }
          cx = stack ? x + w / 2 : ctx.PL + 8;
          cy = y + th / 2 + 4;
        } else {
          x = lane; w = th;
          var top = ctx.vy(to), foot = ctx.vy(from);
          y = Math.min(top, foot); h = Math.abs(foot - top);
          if (h - cut > 1) { h -= cut; y += cut; }
          if (h < 1) { h = 1; y = v < 0 ? foot : foot - 1; }   /* a real zero keeps a hairline */
          cx = x + th / 2;
          cy = stack ? y + h / 2 + 4 : y - 4;
        }
        /* DV-D09 — the horizontal single-series default is series/3, not the column's series/1 */
        var fill = (horiz && ns === 1 && !ctx.series[0].role) ? 'var(--data-series-3)' : ctx.fill(si);
        ctx.push('<rect class="dv-series"' +
          (ns > 1 ? ' data-series-group="' + (si + 1) + '" data-series-i="' + (si + 1) + '"' : '') +
          ' data-grow="' + (horiz ? 'right' : 'up') + '" style="animation-delay:' + (order++ * 45) + 'ms"' +
          ' fill="' + fill + '" x="' + n1(x) + '" y="' + n1(y) + '" width="' + n1(w) +
          '" height="' + n1(h) + '" data-fx="' + f4(ctx.fx(x)) + '" data-fw="' + f4(w / ctx.plotW) +
          '" tabindex="0" role="img" aria-label="' + esc(words(ctx, si, ci, v, ', ')) +
          '" data-tip="' + esc(words(ctx, si, ci, v, ' · ')) + '"></rect>');
        if (ns > 1 && (!stack || (horiz ? w : h) >= 14)) {
          keys.push(letter(ctx, si, cx, cy, horiz && !stack));
        }
        run += v;
      }
      /* The category name: under its band on a column, in the LEFT GUTTER on a horizontal bar —
         where it rides data-dx so ds-012(b)'s measured gutter (data-pl-fit) sizes itself off it. */
      var lx = horiz ? ctx.PL - 8 : ctx.PL + ci * band + band / 2;
      ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(lx) +
        '" y="' + n1(horiz ? b0 - pad + band / 2 + 4 : ctx.y0 + 16) + '" text-anchor="' +
        (horiz ? 'end" data-fx="0" data-dx="-8' : 'middle" data-fx="' + f4(ctx.fx(lx))) + '">' +
        esc(ctx.cats[ci]) + '</text>');
    }
    for (ci = 0; ci < keys.length; ci++) { ctx.push(keys[ci]); }   /* keys LAST — above the fills */
  }

  /* The stacked domain is the stack TOTAL, not the largest single value — the one thing the core
     cannot infer from the spec, which is why `fn.domain` exists at all. */
  function stackDomain(spec) {
    var lo = 0, hi = 0, ci, si;
    for (ci = 0; ci < spec.categories.length; ci++) {
      var pos = 0, neg = 0;
      for (si = 0; si < spec.series.length; si++) {
        var v = spec.series[si].values[ci];
        if (v < 0) { neg += v; } else { pos += v; }
      }
      if (pos > hi) { hi = pos; }
      if (neg < lo) { lo = neg; }
    }
    return [lo, hi];
  }

  function mk(horiz, stack) {
    var f = function (ctx) { bars(ctx, horiz, stack); };
    f.axis = horiz ? 'x' : 'y';
    if (stack) { f.domain = stackDomain; }
    return f;
  }

  T.column = T['grouped-column'] = mk(false, false);
  T['stacked-column'] = mk(false, true);
  T.bar = mk(true, false);
}());
