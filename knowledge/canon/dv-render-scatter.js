/* dv-render-scatter — the SCATTER TYPE PARTIAL for the dv-render engine (s259-D1 fast follower,
   built #260). Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by
   gen_component_partials.py. Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE: `scatter` — the relationship between two continuous variables.

   ⛔ THE NUMERIC X AXIS, AND THE ONE PLACE THIS TYPE STRAINS THE RULED SPEC. Every other
   registered type reads `spec.categories` as a BAND axis: n equal slots, order only. A scatter's
   x is a MEASUREMENT — the distance between 28 and 35 has to be smaller than the distance between
   122 and 140, or the chart is not a scatter, it is a dot plot. The s249-D4 spec has no numeric x
   field, so this partial reads one out of what it has: when EVERY category parses as a finite
   number the x axis is that number on a nice linear scale; when any one does not, the categories
   fall back to evenly spaced band centres and the chart is an honest ordinal dot plot. The
   fallback is not the interesting half — the numeric read is a LOCAL WORKAROUND for a missing
   core field, and the core request is filed verbatim in
   knowledge/_tmp/260/scatter.core-requests.md. Do not read the workaround as the design.

   WHAT THE CORE DOES NOT DRAW FOR US. `dvRender` emits furniture for ONE axis — for `axis: "y"`
   the horizontal gridlines, the value tick labels and the zero baseline. A cartesian scatter needs
   the OTHER axis too, so the vertical gridlines, the x tick labels and the left axis rule are
   emitted here, off `dvRender.util.nice` — the same tick chooser the core uses, so the two axes
   are ticked by one rule and cannot drift apart.

   RULES ENACTED HERE:
     DV-D02 / DV-D02-A  the canvas keeps `dv-fit` (scatter is cartesian, and the #72 discharge
               makes a scatter without the fit hooks BLOCKING). Every point is wrapped in
               `<g class="dv-marker" data-fx data-x0>` because `fitOne()` branches on TAG and has
               no `circle` branch — a bare re-classed circle would not move. That wrapper is the
               exact shape #72 proved by mutation, and it is re-driven here.
     s116-D1 / AA 2.5.8  the visible glyph is 9px and unreadable as a target, so every point
               carries an invisible `circle.dv-hit` of r=12 — a 24px target — and the interactive
               attributes (tabindex, role, aria-label, data-tip) ride the TARGET, not the glyph.
     §04.3     colour is never the only channel: series 1..n take circle, square, diamond,
               triangle in order, so two segments differ by SHAPE before they differ by hue. The
               letter keys live in the consumer's `dv-legend` rows, which bind by
               `data-series-group` — emitted on both the group and the glyph so show/hide and
               isolate reach the whole point.
     .dv-mk    a square or a triangle must keep its GLYPH when the plot re-flows; dv-behaviour
               re-scales a plain rect by its cached height fraction and translates a `.dv-mk` one
               instead. Circles need no class (only `cy` is fitted) and polygons are translated
               wholesale, but the class is emitted on every glyph so the contract reads as one
               rule rather than three exceptions.
     dv-017    every fill is a var() token, from `ctx.fill(i)`.
     DEF-003   entry motion is CSS: `.dv-animate g.dv-marker` fades on a stagger. No JS motion. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc, nice = U.nice;
  var R = 4.5;        /* the visible glyph's radius — 9px across, the baked scatter's size */
  var HITR = 12;      /* AA 2.5.8 — a 24px target around a 9px mark */

  /* ---------- THE X READ. Numbers if every category is one, else band centres. `ok` is what the
     rest of the partial branches on, and it is also what the x tick labels are drawn from: an
     ordinal fallback ticks the CATEGORIES, a numeric axis ticks the SCALE. */
  function xread(ctx) {
    var xs = [], i, v, lo = Infinity, hi = -Infinity;
    for (i = 0; i < ctx.cats.length; i++) {
      v = parseFloat(ctx.cats[i]);
      if (!isFinite(v) || String(ctx.cats[i]).trim() === '') { return { ok: false }; }
      xs.push(v);
      if (v < lo) { lo = v; }
      if (v > hi) { hi = v; }
    }
    /* The x axis starts at ZERO unless the data goes below it — the same floor the core applies
       to the value axis (dv-bar-009's argument is about reading a magnitude off a length, and a
       scatter's x distance is read the same way), and the same axis the baked specimen shipped. */
    var sc = nice(lo < 0 ? lo : 0, hi, 4);
    var span = sc.max - sc.min || 1;
    return {
      ok: true, xs: xs, ticks: sc.ticks, min: sc.min,
      f: function (n) { return (n - sc.min) / span; }
    };
  }

  /* ---------- THE SECOND AXIS. Vertical gridlines + x tick labels + the left axis rule, in the
     same fit grammar the core uses for its own furniture: a line rides data-fx/data-fx2, a text
     rides data-fx (+ data-dx where the offset must survive a re-fit unscaled). */
  function xfurniture(ctx, X) {
    var i, p, x, lab;
    var n = X.ok ? X.ticks.length : ctx.cats.length;
    for (i = 0; i < n; i++) {
      p = X.ok ? X.f(X.ticks[i]) : (i + 0.5) / ctx.cats.length;
      lab = X.ok ? String(X.ticks[i]) : String(ctx.cats[i]);
      x = ctx.PL + p * ctx.plotW;
      ctx.push('<line class="dv-grid" x1="' + n1(x) + '" y1="' + ctx.PT + '" x2="' + n1(x) +
        '" y2="' + ctx.y0 + '" stroke="var(--data-grid)" data-fx="' + f4(p) +
        '" data-fx2="' + f4(p) + '"/>');
      ctx.push('<text class="dv-axis t-cm-chart-value" fill="var(--data-axis)" x="' + n1(x) +
        '" y="' + (ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + f4(p) + '">' +
        esc(lab) + '</text>');
    }
    ctx.push('<line class="dv-axis" x1="' + ctx.PL + '" y1="' + ctx.PT + '" x2="' + ctx.PL +
      '" y2="' + ctx.y0 + '" stroke="var(--data-axis)" data-fx="0" data-fx2="0"/>');
    /* AXIS TITLES. The x title is the spec's own `categoryLabel` (what the numbers along the
       bottom ARE); the y title is the single series' name, which is the measure on the value
       axis. With two or more series the series names belong in the legend, not on the axis. */
    if (ctx.spec.categoryLabel) {
      ctx.push('<text class="dv-label t-cm-caption" fill="var(--data-axis)" x="' +
        n1(ctx.PL + ctx.plotW / 2) + '" y="' + (ctx.VH - 2) + '" text-anchor="middle" data-fx="0.5">' +
        esc(ctx.spec.categoryLabel) + '</text>');
    }
    if (ctx.series.length === 1) {
      ctx.push('<text class="dv-label t-cm-caption" fill="var(--data-axis)" x="' + ctx.PL +
        '" y="' + (ctx.PT - 3) + '" data-fx="0">' + esc(ctx.series[0].name) + '</text>');
    }
  }

  /* ---------- THE GLYPH. Four shapes, in series order, so the non-colour channel arrives before
     the fifth palette slot does. Every one is `.dv-series .dv-pt .dv-mk`: dv-series is what the
     legend and the gate read, dv-pt is what canon.css paints, dv-mk is what tells the fit to move
     the glyph rather than stretch it. */
  function glyph(si, cx, cy, fill) {
    var g = si % 4, a = 'class="dv-series dv-pt dv-mk" data-series-group="' + (si + 1) +
      '" data-series-i="' + (si + 1) + '" fill="' + fill + '"';
    if (g === 0) { return '<circle ' + a + ' cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + R + '"></circle>'; }
    if (g === 1) {
      return '<rect ' + a + ' x="' + n1(cx - R) + '" y="' + n1(cy - R) + '" width="' + (R * 2) +
        '" height="' + (R * 2) + '"></rect>';
    }
    var pts = g === 2
      ? [[cx, cy - R - 0.6], [cx + R + 0.6, cy], [cx, cy + R + 0.6], [cx - R - 0.6, cy]]        /* diamond */
      : [[cx, cy - R - 1], [cx + R + 0.8, cy + R * 0.8], [cx - R - 0.8, cy + R * 0.8]];         /* triangle */
    return '<polygon ' + a + ' points="' + pts.map(function (p) {
      return n1(p[0]) + ',' + n1(p[1]);
    }).join(' ') + '"></polygon>';
  }

  /* The mark's words — BOTH coordinates, always, because a point on a scatter means nothing
     without its x. One rule, no series-count branch: the x half is named by the spec's
     categoryLabel and the y half by the series name, which is also what the two axis titles say,
     so the popover and the axes read the same words. `sep` is the only difference between the
     popover text (· separated, the kit's) and the accessible name (comma separated, a sentence). */
  function words(ctx, si, ci, v, sep) {
    var xl = ctx.spec.categoryLabel;
    return (xl ? xl + ' ' : '') + ctx.cats[ci] + sep + ctx.series[si].name + ' ' + ctx.fmt(v);
  }

  function scatter(ctx) {
    var X = xread(ctx), si, ci, order = 0;
    xfurniture(ctx, X);
    for (si = 0; si < ctx.series.length; si++) {
      for (ci = 0; ci < ctx.cats.length; ci++) {
        var v = ctx.series[si].values[ci];
        var p = X.ok ? X.f(X.xs[ci]) : (ci + 0.5) / ctx.cats.length;
        var cx = ctx.PL + p * ctx.plotW, cy = ctx.vy(v);
        var tip = words(ctx, si, ci, v, ' · ');
        /* data-x0 is the AUTHORED x of the group's contents; fitOne translates by (fitted − x0),
           so the glyph and its hit target move together and neither is re-authored. */
        ctx.push('<g class="dv-marker" data-series-group="' + (si + 1) + '" data-fx="' + f4(p) +
          '" data-x0="' + n1(cx) + '" style="animation-delay:' + (order++ * 45) + 'ms">' +
          glyph(si, cx, cy, ctx.fill(si)) +
          '<circle class="dv-hit" fill="transparent" cx="' + n1(cx) + '" cy="' + n1(cy) +
          '" r="' + HITR + '" tabindex="0" role="img" aria-label="' +
          esc(words(ctx, si, ci, v, ', ')) + '" data-tip="' + esc(tip) + '"></circle></g>');
      }
    }
  }

  scatter.axis = 'y';
  T.scatter = scatter;
}());
