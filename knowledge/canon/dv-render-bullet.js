/* dv-render-bullet — the BULLET TYPE PARTIAL for the dv-render engine (s259-D1 fast follower,
   built #260). Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by
   gen_component_partials.py. Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE: `bullet` — one KPI per ROW, a measure bar read against a comparative
   target marker and, behind both, the qualitative performance bands. The value axis runs ACROSS
   x (`fn.axis = "x"`, the horizontal-bar arm of the core's furniture switch); the rows run down y.

   THE SPEC, and the ONE extension it needs:
     { type: "bullet",
       categories: ["Revenue", "Satisfaction", "Retention"],      one KPI per row
       series:     [{ name: "Measure", values: [82, 58, 91] },    series[0] IS the measure
                    { name: "Target",  values: [75, 70, 85] }],   series[1] IS the target marker
       ranges:     [40, 60, 100],                                 ⚠ EXTENSION — see below
       unit?, format?, caption?, categoryLabel? }

   ⚠ `ranges` IS AN EXTENSION TO THE s249-D4 SPEC, and it is declared rather than smuggled. A
   bullet chart without its qualitative bands is a horizontal bar; the bands are the component's
   whole reason to beat stat-card and kpi-tile (Chart-bullet.meta `when`: "when the BENCHMARK …
   is the point"). The core's `validate()` neither knows nor rejects extra keys, so this partial
   validates `ranges` ITSELF, loudly and by name, exactly as the core validates what it owns.
   Whether the ruled spec grows a `ranges` field is Dave's, not a lane's — filed RULING-SHAPED.

   RULES ENACTED HERE:
     #96-D1 ②  ROW PITCH = 60px, the RULED CONSTANT, and the canvas height formula that falls out
               of it: H = 80 + (rowCount−1)·60 with data-pt="4" data-pb="16", because then
               plotH = H − 20 = 60·rowCount EXACTLY and the band arithmetic below needs no
               special case. The pitch is CAPPED, never stretched (`Math.min`), so filtering a
               row out leaves the survivors' bands IDENTICAL — which is the ruling's own words,
               "a single row keeps the SAME 60px band/appearance".
     #96-D1 ③  the qualitative bands take the CANON greys `--dv-range-1/2/3`. Minted nothing;
               canon.css already carries the pair per mode inside `.cn-chart-bullet`.
     brief-ruled  measure = data/series/1 · target marker = ink. The measure rect carries
               `fill="var(--data-series-1)"` as a presentation attribute so the dataviz gate can
               READ it (it reads `fill` off `.dv-series`); canon.css's `.dv-measure{fill:…}`
               rule wins at paint time and binds the SAME token, so the two cannot disagree.
     z-order   bands → bar → marker, which in SVG is DOM order and nothing else. The push order
               below IS the z-order; there is no z-index to get wrong.
     dv-005    the value the popover says is the value the table says, because the core writes
               both off one spec. See the RULING-SHAPED note about the range columns.
     DEF-003   entry motion is CSS: `.dv-animate .dv-row` fades on an authored animation-delay
               and `.dv-animate rect.dv-measure` grows from the axis. No JS geometry animation.
     dv-017    every colour emitted is a var() token.

   ⚠ THE CORE'S CARTESIAN FURNITURE IS DISCARDED (`ctx.out.length = 0`), the same WORK-AROUND
   dv-render-donut and dv-render-sparkline already carry, for the same reason: `dvRender` calls
   `furniture()` unconditionally before `draw(ctx)` and offers no opt-out. A bullet reads against
   its BANDS, not against gridlines and tick labels — the promoted component has never carried
   either — so drawing them and then painting opaque greys over them would be paying for ink
   nobody sees. The core request ("honour fn.axis = 'none' / fn.furniture = false") is filed
   verbatim in knowledge/_tmp/260/bullet.core-requests.md. This partial emits the one piece of
   furniture the component does own: the vertical zero baseline. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's own error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;

  /* #96-D1 ② — the RULED row geometry, in the coordinate space the ruling states it in:
     row band 32 tall, measure bar 16 tall, target tick 48 tall, all inside a 60px pitch. */
  var PITCH = 60, ROW_H = 32, MEAS_H = 16, TICK_H = 48;
  var TINTS = 3;      /* --dv-range-1/2/3 — three canon greys exist and no fourth is minted */

  function bad(msg) { throw new Error('dv-render-bullet: ' + msg); }

  /* The qualitative breakpoints, validated the way the core validates its own fields: say the
     field, say what it wanted. An ABSENT `ranges` is legal and draws a bare measure/target row. */
  function bands(spec) {
    var r = spec.ranges;
    if (r === undefined || r === null) { return []; }
    if (!Array.isArray(r) || !r.length) {
      bad('spec.ranges must be a non-empty array of ascending breakpoints, or absent');
    }
    if (r.length > TINTS) {
      bad('spec.ranges has ' + r.length + ' breakpoints — #96-D1 ③ mints THREE qualitative tints ' +
        '(--dv-range-1/2/3) and a fourth band would bind a token that does not exist');
    }
    for (var i = 0; i < r.length; i++) {
      if (typeof r[i] !== 'number' || !isFinite(r[i])) {
        bad('spec.ranges[' + i + '] is not a finite number');
      }
      if (r[i] <= (i ? r[i - 1] : 0)) {
        bad('spec.ranges must ascend from zero — ranges[' + i + '] is ' + r[i] +
          ' and the band before it ends at ' + (i ? r[i - 1] : 0));
      }
    }
    return r;
  }

  /* The domain is the RANGE TOP, not the largest measure — a bullet is read against its bands,
     so a chart whose worst KPI is 58 must still show the whole 0–100 scale. This is exactly the
     case `fn.domain` exists for: the core cannot infer it from `series` alone. */
  function domain(spec) {
    var hi = 0, i, j, v;
    for (i = 0; i < spec.series.length; i++) {
      for (j = 0; j < spec.series[i].values.length; j++) {
        v = spec.series[i].values[j];
        if (v > hi) { hi = v; }
      }
    }
    var r = bands(spec);
    if (r.length && r[r.length - 1] > hi) { hi = r[r.length - 1]; }
    return [0, hi];
  }

  function bullet(ctx) {
    ctx.out.length = 0;                 /* ⚠ the core's cartesian furniture — see the header */

    var ns = ctx.series.length, nc = ctx.cats.length, i, j;
    if (ns > 2) {
      bad('a bullet row is ONE measure against AT MOST ONE target — got ' + ns +
        ' series. Expected [measure] or [measure, target]; use type "bar" for a multi-series ' +
        'horizontal comparison');
    }
    var rs = bands(ctx.spec);
    var meas = ctx.series[0], tgt = ns > 1 ? ctx.series[1] : null;

    /* #96-D1 ② — CAPPED, never stretched. With the ruled canvas (data-h = 80 + (n−1)·60,
       data-pt="4", data-pb="16") plotH is exactly 60·n and the cap is inert; on any other
       canvas the rows keep their 60px appearance and sit top-aligned in the space there is. */
    var pitch = Math.min(PITCH, ctx.plotH / nc);
    var k = pitch / PITCH;                          /* the one scale factor, applied to all three */
    var rh = ROW_H * k, mh = MEAS_H * k, th = TICK_H * k;
    var X = function (v) { return ctx.PL + ctx.vf(v) * ctx.plotW; };
    var W = function (a, b) { return (ctx.vf(b) - ctx.vf(a)) * ctx.plotW; };

    for (i = 0; i < nc; i++) {
      var cy = ctx.PT + i * pitch + pitch / 2;
      ctx.push('<g class="dv-row" style="animation-delay:' + (i * 90) + 'ms">');

      /* The KPI name, in the LEFT GUTTER — data-fx="0" + data-dx so the 8px clearance stays 8px
         on every width, and so ds-012(b)'s measured gutter (data-pl-fit) can size itself off it. */
      ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' +
        n1(ctx.PL - 8) + '" y="' + n1(cy + 4) + '" text-anchor="end" data-fx="0" data-dx="-8">' +
        esc(ctx.cats[i]) + '</text>');

      /* ① the qualitative bands, FIRST = furthest back (SVG paint order is the z-order) */
      var from = 0;
      for (j = 0; j < rs.length; j++) {
        ctx.push('<rect class="dv-range-' + (j + 1) + '" fill="var(--dv-range-' + (j + 1) +
          ')" x="' + n1(X(from)) + '" y="' + n1(cy - rh / 2) + '" width="' + n1(W(from, rs[j])) +
          '" height="' + n1(rh) + '" data-fx="' + f4(ctx.vf(from)) + '" data-fw="' +
          f4(W(from, rs[j]) / ctx.plotW) + '"></rect>');
        from = rs[j];
      }

      /* ② the measure bar, over the bands. Its words carry the DOMAIN and the TARGET, because a
         bullet's reading is a comparison — a bare number is the one thing this chart is not. */
      var v = meas.values[i];
      var w = W(0, v); if (w < 1) { w = 1; }
      var words = ctx.cats[i] + ': ' + ctx.fmt(v) + ' of ' + ctx.fmt(ctx.max) +
        (tgt ? ', target ' + ctx.fmt(tgt.values[i]) : '');
      ctx.push('<rect class="dv-series dv-measure" data-series-i="1" fill="' + ctx.fill(0) +
        '" data-grow="right" style="animation-delay:' + (i * 90) + 'ms" x="' + n1(X(0)) +
        '" y="' + n1(cy - mh / 2) + '" width="' + n1(w) + '" height="' + n1(mh) +
        '" data-fx="' + f4(ctx.vf(0)) + '" data-fw="' + f4(w / ctx.plotW) +
        '" tabindex="0" role="img" aria-label="' + esc(words) + '" data-tip="' +
        esc(words) + '"></rect>');

      /* ③ the comparative marker, LAST = on top of everything. Ink, 3px, spanning the row —
         the conventional bullet target indicator, and brief-ruled ("marker = ink"). */
      if (tgt) {
        var tv = tgt.values[i];
        ctx.push('<line class="dv-target" x1="' + n1(X(tv)) + '" y1="' + n1(cy - th / 2) +
          '" x2="' + n1(X(tv)) + '" y2="' + n1(cy + th / 2) + '" data-fx="' + f4(ctx.vf(tv)) +
          '" data-fx2="' + f4(ctx.vf(tv)) + '"/>');
      }
      ctx.push('</g>');
    }

    /* The one piece of furniture a bullet owns: the vertical baseline the bars grow from. */
    ctx.push('<line class="dv-axis" x1="' + n1(X(0)) + '" y1="' + n1(ctx.PT - 8) + '" x2="' +
      n1(X(0)) + '" y2="' + n1(ctx.PT + nc * pitch + 8) + '" stroke="var(--baseline)" data-fx="' +
      f4(ctx.vf(0)) + '" data-fx2="' + f4(ctx.vf(0)) + '"/>');
  }

  bullet.axis = 'x';        /* the value runs ACROSS — the same switch the horizontal bar throws */
  bullet.domain = domain;
  T.bullet = bullet;
}());
