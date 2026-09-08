/* dv-render-boxplot — the BOX PLOT TYPE PARTIAL for the dv-render engine (s259-D1 fast follower,
   built #260). Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by
   gen_component_partials.py. Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE:
     boxplot — one box per category: median, the IQR box, whiskers to min/max, outlier dots

   THE SPEC, WITHOUT EXTENDING THE SPEC. s249-D4's contract is `series: [{name, values}]` with ONE
   value per category, and a box plot needs FIVE numbers per category. It does NOT need a new
   field: the five-number summary IS five series, one value each, in a fixed ORDER —

       series[0] minimum · [1] lower quartile · [2] median · [3] upper quartile · [4] maximum

   and every further series is an OUTLIER CANDIDATE. That mapping costs the spec nothing, and it
   pays twice: the core's own `writeTable` then emits exactly the five-number-summary table the
   baked snippet authored by hand (Category | Min | Q1 | Median | Q3 | Max | …), and the core's
   validator already guarantees one finite value per category per series before this file runs.

   OUTLIERS, THE SAME WAY. An outlier count varies per category and the spec has no ragged array,
   so an outlier series carries one value per category and a value that falls INSIDE the whiskers
   is not drawn — which is not a fudge, it is the definition: a point within [min, max] is not an
   outlier. A category with no outlier therefore carries any in-range number (the median is the
   readable choice) and draws nothing. ⚠ A category with TWO outliers needs a second outlier
   series; the type takes as many as the author supplies.

   RULES ENACTED HERE:
     DV-D02 / DV-D02-A  a box plot is CARTESIAN, so its canvas KEEPS `dv-fit` and every mark is
               authored in the fit grammar — rect data-fx + data-fw, line data-fx + data-fx2,
               text data-fx + data-dx, and the outlier pair inside a `g` with data-fx + data-x0,
               because dv-behaviour's x pass moves rect/text/line/g and NOT a bare circle. The
               circles' cy is re-derived by the same file's fitY pass, so the dot rides the box.
     s116-D1   the box is a hit target (tabindex=0 + data-tip), so its WIDTH is floored at 24px
               wherever the band can pay for it; the outlier's hit circle is a transparent r=12
               over an r=5.5 glyph, the Chart-scatter enlarged-marker contract, so a 5.5px dot is
               never a 5.5px target.
     dv-004    NOT APPLICABLE and deliberately not claimed. dv-004 governs ADJACENT FILLED BLOCKS
               (donut/pie/stacked); a box plot draws ONE filled block per category separated by
               more than half a band of empty plot. `_validate_dataviz.py` scopes the rule to
               ("donut", "pie", "stacked") and this type is not in it. The boxes are nonetheless
               kept ≥2px apart by the 0.45 band share — measured in the driven receipt.
     dv-017 / DEF-004  the box fill is `ctx.fill(0)` — a var() token, the solid categorical
               palette. Whiskers, caps and median are INK strokes carried by canon.css
               (`.dv-whisker`, `.dv-cap`, `.dv-median`), never author colour: this file emits
               classes for them and no `stroke` attribute at all.
     §04.3     no letter keys and no `data-series-group`. The five series are ONE distribution in
               ONE colour, so there is no colour channel to disambiguate — emitting five series
               groups would tell dv-legend and the §04.3 advisory that this chart has five
               colours, which is a lie about the artefact.
     DEF-003   entry motion is CSS: `.dv-animate g.dv-boxgroup` / `g.dv-marker` fade with a
               staggered animation-delay. No JS geometry animation. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;
  var FIVE = ['minimum', 'lower quartile (Q1)', 'median', 'upper quartile (Q3)', 'maximum'];

  function bad(msg) { throw new Error('dv-render-boxplot: ' + msg); }

  /* The box WIDTH inside one band: 45% of the band, lifted to the 24px hit floor when the band
     can pay for it (s116-D1), and never below 4px of visible ink. The rest of the band is the
     gutter that makes neighbouring categories read as separate distributions. */
  function width(band) {
    var w = band * 0.45;
    if (w < 24 && band * 0.72 >= 24) { w = 24; }
    return w < 4 ? 4 : w;
  }

  /* ⛔ pointer-events="none" IS LOAD-BEARING, and driving found it. The median is 2px of ink
     across the MIDDLE of the box — exactly where a pointer lands — and dv-behaviour's popover is
     `e.target.closest('[data-tip]')`. A bare <line> sibling therefore SWALLOWED the hover and the
     tip went blank at the box's centre while working at its edges. Whiskers, caps and the median
     are decoration; the rect is the hit target (s116-D1), so they opt out of hit-testing. */
  function line(ctx, cls, x1, x2, y1, y2) {
    return '<line class="' + cls + '" pointer-events="none" x1="' + n1(x1) + '" y1="' + n1(y1) +
      '" x2="' + n1(x2) + '" y2="' + n1(y2) + '" data-fx="' + f4(ctx.fx(x1)) +
      '" data-fx2="' + f4(ctx.fx(x2)) + '"/>';
  }

  function draw(ctx) {
    var ns = ctx.series.length, nc = ctx.cats.length, i, ci;
    if (ns < 5) {
      bad('a box plot is the FIVE-NUMBER SUMMARY — spec.series must be [' + FIVE.join(', ') +
        '] in that order, and any further series are outlier candidates; got ' + ns +
        ' series (' + ctx.series.map(function (s) { return s.name; }).join(', ') + ')');
    }
    var band = ctx.plotW / nc, w = width(band), half = w / 2;

    for (ci = 0; ci < nc; ci++) {
      var lo = ctx.series[0].values[ci], q1 = ctx.series[1].values[ci];
      var md = ctx.series[2].values[ci], q3 = ctx.series[3].values[ci];
      var hi = ctx.series[4].values[ci];
      /* The five numbers are a SUMMARY, and a summary out of order is data corruption, not a
         drawing problem: q3 below q1 would draw a negative-height box and read as a valid one. */
      for (i = 1; i < 5; i++) {
        var prev = ctx.series[i - 1].values[ci], now = ctx.series[i].values[ci];
        if (now < prev) {
          bad('"' + ctx.cats[ci] + '" has ' + FIVE[i] + ' ' + now + ' below ' + FIVE[i - 1] +
            ' ' + prev + ' — the five-number summary must not decrease');
        }
      }
      var cx = ctx.PL + (ci + 0.5) * band, x = cx - half;
      var yhi = ctx.vy(hi), yq3 = ctx.vy(q3), ymd = ctx.vy(md), yq1 = ctx.vy(q1), ylo = ctx.vy(lo);
      var h = yq1 - yq3; if (h < 1) { h = 1; }        /* a zero IQR keeps a hairline of ink */
      var says = ctx.cats[ci] + ': median ' + ctx.fmt(md) + ', IQR ' + ctx.fmt(q1) + ' to ' +
        ctx.fmt(q3) + ', whiskers ' + ctx.fmt(lo) + ' to ' + ctx.fmt(hi);

      var g = ['<g class="dv-boxgroup" style="animation-delay:' + (ci * 90) + 'ms">'];
      g.push(line(ctx, 'dv-whisker', cx, cx, yhi, yq3));
      g.push(line(ctx, 'dv-cap', cx - half / 2, cx + half / 2, yhi, yhi));
      g.push(line(ctx, 'dv-whisker', cx, cx, yq1, ylo));
      g.push(line(ctx, 'dv-cap', cx - half / 2, cx + half / 2, ylo, ylo));
      g.push('<rect class="dv-box dv-series" fill="' + ctx.fill(0) + '" x="' + n1(x) + '" y="' +
        n1(yq3) + '" width="' + n1(w) + '" height="' + n1(h) + '" data-fx="' + f4(ctx.fx(x)) +
        '" data-fw="' + f4(w / ctx.plotW) + '" tabindex="0" role="img" aria-label="' + esc(says) +
        '" data-tip="' + esc(says.replace(': ', ' · ').replace(', IQR', ' · IQR')) + '"></rect>');
      g.push(line(ctx, 'dv-median', x, x + w, ymd, ymd));

      /* OUTLIERS — series 5..n, drawn only where the value escapes the whiskers. The pair sits
         in a `g[data-fx][data-x0]` because dv-behaviour moves a g by transform and leaves a bare
         circle's cx alone; cy is re-derived by fitY on the circles themselves. */
      for (i = 5; i < ns; i++) {
        var ov = ctx.series[i].values[ci];
        if (ov >= lo && ov <= hi) { continue; }
        var oy = ctx.vy(ov), ot = ctx.cats[ci] + ' outlier: ' + ctx.fmt(ov);
        g.push('<g class="dv-marker" data-fx="' + f4(ctx.fx(cx)) + '" data-x0="' + n1(cx) +
          '"><circle class="dv-series dv-pt" fill="' + ctx.fill(0) + '" cx="' + n1(cx) +
          '" cy="' + n1(oy) + '" r="5.5"></circle><circle class="dv-hit" fill="transparent" cx="' +
          n1(cx) + '" cy="' + n1(oy) + '" r="12" tabindex="0" role="img" aria-label="' + esc(ot) +
          '" data-tip="' + esc(ot) + '"/></g>');
      }
      g.push('</g>');
      ctx.push(g.join(''));

      ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(cx) +
        '" y="' + n1(ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + f4(ctx.fx(cx)) + '">' +
        esc(ctx.cats[ci]) + '</text>');
    }
  }

  /* The domain is the WHOLE distribution, outliers included — the core's default min/max would
     already find them, but stating it here is what makes an outlier series that is *only* a
     placeholder (an in-range value, never drawn) harmless: it can never widen the axis past the
     whiskers it sits inside. */
  function domain(spec) {
    var lo = Infinity, hi = -Infinity, si, ci, v;
    for (si = 0; si < spec.series.length; si++) {
      for (ci = 0; ci < spec.series[si].values.length; ci++) {
        v = spec.series[si].values[ci];
        if (si >= 5 && v >= spec.series[0].values[ci] && v <= spec.series[4].values[ci]) { continue; }
        if (v < lo) { lo = v; }
        if (v > hi) { hi = v; }
      }
    }
    return [lo, hi];
  }

  draw.axis = 'y';
  draw.domain = domain;
  T.boxplot = draw;
}());
