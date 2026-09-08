/* dv-render-sparkline — the SPARKLINE TYPE PARTIAL for the dv-render engine (s249-D4, built #259).
   Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by gen_component_partials.py.
   Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS TWO NAMES for one drawing: `sparkline` and `spark`. `spark` is the word the library
   already says out loud — `data-dv-type="spark"` on the figure, `_validate_dataviz.py`'s dtype
   table, the registry's own `requires.declarations` — and `sparkline` is the component's name.
   Both are registered because `data-dv-type` and the spec's `type` are the author's word for what
   they meant, and a name mismatch should never be the thing that fails.

   ★★ s182-D2 (#182) — THE SPARKLINE IS AN ATOM, ALONE. Dave, verbatim: "this doesn't need a title
   as it will usually live in a card"; "this is just an atom"; "the sparkline is an atom alone, the
   table cta can be optional in the trend card component". ENACTED HERE, three ways:
     · NO AXIS FURNITURE AT ALL. The core draws gridlines, tick labels and a baseline for every
       type BEFORE it calls the partial, and exposes no switch to decline them, so the first
       statement of this drawing empties `ctx.out`. That is a WORKAROUND INSIDE THE PARTIAL, not a
       core edit — the core request ("let a type opt out of furniture") is filed verbatim in the
       lane's subreport. What survives is ONE hairline BASELINE, which is the atom's own promoted
       furniture (meta `tokens.baseline`), classed `dv-base` not `dv-grid`/`dv-axis` so it can
       never be read as an axis: no ticks, no tick labels, no gridlines, no value scale on show.
     · ONE FOCUS STOP. The trend line is the only `tabindex="0"`; the endpoint dot and the optional
       min/max dots are `aria-hidden` glyphs. Per-point stops would fight the axis-free idiom —
       the meta's `accessibility.keyboard` receipts that judgment and this honours it.
     · ONE SERIES. Two series in a spark is a line chart; it throws, named, rather than drawing a
       legend the atom has no room for (the member consumes NO dv-legend, by the brief).

   ★★ s182-D3 (#182) — SPARKLINE COLOUR IS SEMANTIC, NOT PICKED. Dave: "the rules for colours
   should just follow the red and green ink colours for all themes"; "the default ink near-black
   colours are fine for the neutrals, white on dark". ENACTED HERE: the ink is NEVER a series-ramp
   pick (`ctx.fill()` is deliberately not called). The trend is READ FROM THE DATA — first datum vs
   last — and mapped onto the s184-D3 status vocabulary: up → `--status-positive`, down →
   `--status-negative` (which is where the two-red law s151-D1, #DA1A00-on-white / #F6604C-else,
   already lives — this file never names a red), flat → `--status-neutral`. An explicit
   `series[0].role` OVERRIDES the reading, because a series that has been told what it means
   outranks arithmetic about its endpoints; `monitor` is reachable only that way.
   ⚠ THE VOCABULARY COLLIDES WITH THE RULING'S VALUES, and the collision is the consumer's to
   resolve, not this file's: s182-D3 named rag/*-INK, and canon binds `--status-*` to rag/*-GRAPHIC
   (and `--status-neutral` to rag/INFORMATION — a blue, where Dave said near-black). The snippet
   carries the declared, scoped alias that lands the RULED ink; this partial stays on the ruled
   vocabulary. Filed RULING-SHAPED in the subreport — not decided here.

   ★★ s184-D1 (#184) — RESPONSIVE TO ITS ENCLOSURE BY DEFAULT. Dave: "the line should be responsive
   to its enclosure by default". ENACTED HERE: every x is a FRACTION (`data-fxs`) and every y is
   cached as a plot fraction by dv-behaviour from `data-ys`, so the drawing has no width of its own
   at all — it is re-derived from the enclosure on every fit. No fixed width is authored anywhere.

   OUR OWN DOMAIN, and the reason it is ours. The core floors every domain at zero (dv-bar-009 —
   correct for a bar, whose length IS the value). A trend's job is SHAPE: an index running 82→104
   drawn against a zero floor is a flat smear in the top fifth of the box, which is the one thing a
   spark must never be. So this partial scales to the series' OWN extent and does not touch
   ctx.min/ctx.max/ctx.ticks. Second core request, also filed verbatim.

   DEF-003 boundary: entry motion is CSS only — the snippet's `.dv-animate` draw
   (stroke-dasharray/pathLength=2400) and the endpoint fade. No JS geometry animation, no scale
   physics, no press custom properties. Every number written here is an SVG attribute off the data.
   DEF-004 / dv-017: every colour emitted is a var() token. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's own error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;

  var ROLE = { up: 'positive', down: 'negative', flat: 'neutral' };   /* s182-D3 × s184-D3 */
  var WORD = { up: 'rising', down: 'falling', flat: 'flat' };

  /* ONE MARKER GLYPH. dv-behaviour's x pass handles rect / text / line / g — NOT circle — so the
     dot rides inside a `g[data-fx][data-x0]` that translates it, and the circle keeps its own
     radius (that is what `.dv-mk` means: a glyph that moves its centre and never re-scales).
     fitY re-derives `cy` from the fraction it caches off the authored y. */
  function dot(fx, cx, cy, r, ink, tip) {
    return '<g data-fx="' + f4(fx) + '" data-x0="' + n1(cx) + '">' +
      '<circle class="dv-mk dv-series ' + (tip ? 'dv-pt' : 'dv-end') + '" cx="' + n1(cx) +
      '" cy="' + n1(cy) + '" r="' + r + '" fill="' + ink + '" aria-hidden="true"' +
      (tip ? ' data-tip="' + esc(tip) + '"' : '') + '></circle></g>';
  }

  function sparkline(ctx) {
    /* ⛔ s182-D2 — the atom is AXIS-FREE. Drop the core's gridlines, tick labels and axis line
       before drawing anything. See the header: workaround inside the partial, core request filed. */
    ctx.out.length = 0;

    if (ctx.series.length !== 1) {
      throw new Error('dv-render-sparkline: s182-D2 — the sparkline is an ATOM, ALONE: one series, ' +
        'no legend, no axes. Got ' + ctx.series.length + ' series; use type "line" for more.');
    }
    var s = ctx.series[0], v = s.values, n = v.length, i;
    if (n < 2) {
      throw new Error('dv-render-sparkline: a trend needs at least 2 points, got ' + n);
    }

    /* extent + the argmin/argmax, in one pass — the markers want the INDEX, not just the value */
    var mi = 0, ma = 0;
    for (i = 1; i < n; i++) {
      if (v[i] < v[mi]) { mi = i; }
      if (v[i] > v[ma]) { ma = i; }
    }
    var lo = v[mi], hi = v[ma];
    if (hi === lo) { lo -= 1; hi += 1; }     /* a genuinely flat series centres, never divides by 0 */
    var span = hi - lo;

    var PL = ctx.PL, PT = ctx.PT, W = ctx.plotW, H = ctx.plotH;
    var Y = function (val) { return PT + (1 - (val - lo) / span) * H; };
    var FX = function (k) { return k / (n - 1); };
    var X = function (k) { return PL + FX(k) * W; };

    /* s182-D3 — the reading, then the ink. `role` beats the reading; the reading beats a pick. */
    var tr = v[n - 1] > v[0] ? 'up' : v[n - 1] < v[0] ? 'down' : 'flat';
    var ink = 'var(--status-' + (s.role || ROLE[tr]) + ')';
    ctx.svg.setAttribute('data-trend', tr);   /* the atom's declared reading, as the bake carried it */

    /* THE BASELINE HAIRLINE — the atom's own promoted furniture (meta tokens.baseline: "text/default
       at grid alpha"), NOT an axis: no tick, no label, no scale. `dv-base` is the class the inline
       scale already uses, so the two scales style alike. */
    ctx.push('<line class="dv-base" x1="' + n1(PL) + '" y1="' + n1(PT + H) + '" x2="' + n1(PL + W) +
      '" y2="' + n1(PT + H) + '" stroke="var(--ink)" data-fx="0" data-fx2="1"/>');

    /* THE TREND LINE. data-fxs + data-ys is dv-behaviour's polyline grammar: x from the fraction,
       y from a plot fraction it caches off data-ys the first time it fits. dv-line-011 — straight,
       no smoothing, ever. pathLength=2400 is the CSS draw's own unit (DEF-003). */
    var fxs = [], ys = [], pts = [], y;
    for (i = 0; i < n; i++) {
      y = Y(v[i]);
      fxs.push(f4(FX(i))); ys.push(n1(y)); pts.push(n1(X(i)) + ',' + n1(y));
    }
    var a = ctx.cats[0] + ' ' + ctx.fmt(v[0]), b = ctx.cats[n - 1] + ' ' + ctx.fmt(v[n - 1]);
    var label = s.name + ': ' + WORD[tr] + ' from ' + a + ' to ' + b +
      ', low ' + ctx.fmt(v[mi]) + ' at ' + ctx.cats[mi] +
      ', high ' + ctx.fmt(v[ma]) + ' at ' + ctx.cats[ma];
    ctx.push('<polyline class="dv-series" fill="none" stroke="' + ink + '" stroke-width="2.5"' +
      ' stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"' +
      ' pathLength="2400" points="' + pts.join(' ') + '" data-fxs="' + fxs.join(' ') +
      '" data-ys="' + ys.join(' ') + '" tabindex="0" role="img" aria-label="' + esc(label) +
      '" data-tip="' + esc(a + ' → ' + b) + '"></polyline>');

    /* THE LAST-POINT DOT — always, and always decorative: where the series ended is already in the
       line's own accessible name, and a second announcement of it is noise. */
    ctx.push(dot(1, X(n - 1), Y(v[n - 1]), 3.5, ink, ''));

    /* OPTIONAL MIN/MAX MARKERS (`markers: true` on the spec). Hoverable (data-tip), never a focus
       stop (s182-D2 — ONE stop), and skipped where they would sit under the endpoint dot. */
    if (ctx.spec.markers) {
      var pt = function (k, w) {
        if (k === n - 1) { return; }
        ctx.push(dot(FX(k), X(k), Y(v[k]), 2.5, ink, w + ' ' + ctx.cats[k] + ' · ' + ctx.fmt(v[k])));
      };
      pt(ma, 'High'); pt(mi, 'Low');
    }
  }

  sparkline.axis = 'y';
  T.sparkline = T.spark = sparkline;
}());
