/* dv-render — THE DATA-DRIVEN CHART ENGINE, core (s249-D4, built #259, hand-authored SOURCE).
   ONE file, injected into registered chart snippets between AUTO-BEHAVIOUR markers by
   gen_component_partials.py (registry: knowledge/component-types.json, group "dataviz").
   Edit HERE and regenerate — never between a consumer's markers.

   WHAT IT IS. `window.dvRender(figureEl, spec)` turns a DATA SPEC into exactly the SVG grammar
   `canon/dv-behaviour.js` already fits — rect `data-fx`+`data-fw`, line `data-fx`+`data-fx2`,
   text `data-fx`+`data-dx`, g `data-fx`+`data-x0`, `.dv-mk` for glyphs that must keep their
   size — plus `data-tip` on every mark and a real `<table>` spine. It REPLACES rule 18 of
   `ADS-generate-from-canon` (the interim "author the geometry yourself" recipe): the library
   owns the arithmetic, the author owns the data.
   ⚠ THE TWO FIT PASSES ARE NOT SYMMETRIC (#260 A9, reported by scatter and boxplot): dv-behaviour's
   `fitOne` moves rect/text/line/g and NOT `circle`, while `fitY` moves `circle` and NOT `g` — so a
   POINT-MARK type must wrap its glyphs in `g[data-fx][data-x0]` and let the circle inside carry its
   own y; a bare `<circle data-fx>` will not move in x, and a `<g>` alone will not move in y.

   THE SPEC (the whole contract):
     { type:       "column" | "bar" | "grouped-column" | "stacked-column" | …   (a registered type)
       categories: ["Q1", "Q2", …],                     (the band axis, ≥1)
       series:     [{ name: "Savings", values: [40, 45, …], role?: "positive" }, …],
       format?:    "plain" | "compact" | "percent",     (default "plain")
       unit?:      "£" | "%" | "k" | …,                 (1 char ⇒ prefix, else suffix)
       caption?:   "…",  categoryLabel?: "…",  label?:  "…"   (a11y sentence; derived if absent) }

   THE DIVISION OF LABOUR. This file owns everything that is the same for every chart: spec
   VALIDATION (fail loud, named), the linear value SCALE with nice ticks, the band axis, the
   AXIS/GRIDLINE/TICK-LABEL furniture, the `<table>` spine, the accessible name, the single
   `resize` dispatch that hands the fresh marks to dv-behaviour, and the TYPE REGISTRY. A type
   partial (`dv-render-bar` and its siblings) owns the MARKS only, and registers itself as
   `dvRender.types["<name>"] = fn(ctx)`. That seam is why six type partials can be built in
   parallel without any of them touching this file or each other.

   PERFORMANCE CONTRACT (ADR-0015 §4, gated by _validate_behaviour.py): ≤16 KB code-only per
   source · no setInterval / network / polling · NO NEW RESIZE LISTENER — re-fit is
   `dispatchEvent(new Event('resize'))`, dv-behaviour's one rAF-debounced listener does the work ·
   no external <script src> · events stay delegated at the document (dv-behaviour's, not ours).

   PROGRESSIVE ENHANCEMENT (ADR-0015 §4). The SVG a consumer ships is EMPTY and this fills it, so
   with JS off there is no chart — which is why the `<table>` spine is not optional and not
   generated: the consumer ships a real `<table class="dv-table">` inside the figure (dv-005),
   and this engine REWRITES its rows to match the render. JS off ⇒ the table is the answer.

   DEF-004 / dv-017 — NO HARDCODED STYLING. Every colour this file emits is a var() token:
   `--data-grid`, `--data-axis`, `--baseline`, `--data-series-1…5` (ds-026 solid palette) and the
   s184-D3 status vocabulary `--status-positive|negative|monitor|neutral`. The two-red law
   (s151-D1, #DA1A00-on-white / #F6604C-else) rides `--status-negative` → `--rag-error-graphic`,
   which is where the per-theme pair already lives; this file never names a red.

   DEF-003 boundary: data-driven geometry ONLY. No press-physics custom properties, no scale
   transform assignment, no scale-physics of any kind — every number this file writes is an SVG
   attribute derived from the data. Entry motion stays CSS (`.dv-animate` + `data-grow`). */
(function () {
  'use strict';
  if (window.dvRender) { return; }

  /* ---------- the type registry. A type partial does `dvRender.types.column = fn` and may hang
     two optional properties on its own function:
       fn.axis   — "y" (default: value runs UP, categories along x) or "x" (value runs ACROSS,
                   categories down y — the horizontal bar). Decides which furniture is drawn.
       fn.domain — fn(spec) -> [lo, hi]. Only stacked types need it (the domain is the stack
                   TOTAL, not the largest single value). Absent ⇒ the min/max of every value.
       fn.furniture — THE DIAL, not the switch (#260 A1, FIVE reporters: donut, sparkline, bullet,
                   butterfly, histogram). true/absent (default) ⇒ gridlines + tick labels + baseline,
                   exactly as before. "axis" ⇒ tick labels + baseline, NO gridlines. false ⇒ nothing,
                   the plot is the partial's alone. `fn.axis = "none"` is the same as false, because
                   that is the spelling four of the five reporters asked for. The four copies of
                   `ctx.out.length = 0` in donut/sparkline/bullet/butterfly are what this replaces —
                   they stay legal (the buffer is still theirs) and are their own lanes' to remove. */
  var TYPES = {};

  var ROLES = { positive: 1, negative: 1, monitor: 1, neutral: 1 };   /* s184-D3 status vocabulary */
  var FORMATS = { plain: 1, compact: 1, percent: 1 };
  var PAL = 5;        /* ds-026 — data/series/1…5, the solid categorical palette */
  /* dv-004 — 2px between adjacent filled blocks, REAL geometry, never a painted stroke. The rule
     is 2px MINIMUM RENDERED, and the constant carries a 0.2px rounding budget on top of it: the
     fit re-derives a mark's x and its width INDEPENDENTLY from data-fx/data-fw and rounds each to
     one decimal, so up to 0.15px can vanish out of the gap between them. MEASURED at #259 — an
     authored 2.0 landed at 1.90px in the browser and the driven check went red, which is the whole
     reason this is 2.2 and not 2. It is not a fudge of the rule; it is the rule stated in the
     coordinate space the rule is actually judged in. */
  var GAP = 2.2;
  var HIT = 24;       /* s116-D1 — a mark that is a hit target wants 24px, where the band allows */

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return c === '&' ? '&amp;' : c === '<' ? '&lt;' : c === '>' ? '&gt;' : '&quot;';
    });
  }
  function n1(v) { return (Math.round(v * 10) / 10).toFixed(1); }
  function f4(v) { return v.toFixed(4); }
  function attr(el, key, dflt) { var v = parseFloat(el.getAttribute(key)); return isFinite(v) ? v : dflt; }

  /* ---------- NICE TICKS. A 1 / 2 / 2.5 / 5 / 10 × 10ⁿ step chosen against a target tick count,
     then the domain WIDENED to whole steps. dv-bar-009's zero baseline is enforced by the caller
     (bar-family domains floor at 0); a domain that genuinely spans zero keeps zero as a tick. */
  function nice(lo, hi, want) {
    if (!(hi > lo)) { hi = lo + (Math.abs(lo) || 1); }
    var step = Math.pow(10, Math.floor(Math.log((hi - lo) / want) / Math.LN10));
    var k = (hi - lo) / want / step;
    step *= k <= 1 ? 1 : k <= 2 ? 2 : k <= 2.5 ? 2.5 : k <= 5 ? 5 : 10;
    var min = Math.floor(lo / step) * step, max = Math.ceil(hi / step) * step;
    var ticks = [], v = min;
    while (v <= max + step * 1e-9) { ticks.push(Math.round(v * 1e9) / 1e9); v += step; }
    return { min: min, max: max, step: step, ticks: ticks };
  }

  /* ---------- VALUE FORMATTING. Display only — the table's <td> always carries the RAW number,
     because _validate_dataviz.py reads the table for dv-bar-007 (no negative horizontals) and
     dv-pie-010 (slice sum), and a "£1.2k" cell would read as 1.2 to that gate. */
  function fmt(spec, v) {
    var s;
    if (spec.format === 'percent') { s = (Math.round(v * 10) / 10) + '%'; }
    else if (spec.format === 'compact' && Math.abs(v) >= 1000) {
      s = (Math.round(v / 100) / 10).toFixed(1).replace(/\.0$/, '') + 'k';
    } else { s = String(Math.round(v * 1000) / 1000); }
    var u = spec.unit || '';
    return !u ? s : u.length === 1 ? u + s : s + ' ' + u;
  }

  /* ---------- FILL. A series with a `role` takes the status vocabulary (s184-D3) — that is the
     salience ramp, and it is NEVER the isoluminant categorical set (R-D9). Everything else takes
     data/series/N, wrapping at 5. Both are var() tokens: dv-017 has no other legal answer. */
  function fillOf(s, i) {
    if (s.role) { return 'var(--status-' + s.role + ')'; }
    return 'var(--data-series-' + ((i % PAL) + 1) + ')';
  }

  /* ---------- VALIDATION — fail loud and NAMED. Every message says the field and what it wanted,
     because this is the surface a build gets wrong and the only place it can be told so. */
  function bad(msg) { throw new Error('dv-render: ' + msg); }

  function validate(spec) {
    if (!spec || typeof spec !== 'object') { bad('spec must be an object'); }
    if (typeof spec.type !== 'string' || !spec.type) { bad('spec.type must be a non-empty string'); }
    var c = spec.categories;
    if (!Array.isArray(c) || !c.length) { bad('spec.categories must be a non-empty array'); }
    var s = spec.series;
    if (!Array.isArray(s) || !s.length) { bad('spec.series must be a non-empty array'); }
    if (spec.format && !FORMATS[spec.format]) {
      bad('spec.format "' + spec.format + '" is not one of plain|compact|percent');
    }
    for (var i = 0; i < s.length; i++) {
      var one = s[i], at = 'spec.series[' + i + ']';
      if (!one || typeof one !== 'object') { bad(at + ' must be an object'); }
      if (typeof one.name !== 'string' || !one.name) { bad(at + '.name must be a non-empty string'); }
      if (!Array.isArray(one.values)) { bad(at + '.values must be an array'); }

      if (one.values.length !== c.length) {
        bad(at + '.values has ' + one.values.length + ' for ' + c.length +
            ' categories — one value per category, always');
      }
      for (var j = 0; j < one.values.length; j++) {
        if (typeof one.values[j] !== 'number' || !isFinite(one.values[j])) {
          bad(at + '.values[' + j + '] is not a finite number');
        }
      }
      if (one.role && !ROLES[one.role]) {
        bad(at + '.role "' + one.role + '" is not s184-D3 (positive|negative|monitor|neutral)');
      }
    }
  }

  /* ---------- THE TABLE SPINE (dv-005 + the a11y spine). Written into the figure's EXISTING
     <table class="dv-table">, so the consumer's caption/lockup/table-popover chrome is untouched;
     created inside .dv-tablepanel (else the figure) only when the consumer shipped none. The rows
     are the render's own numbers, so popover value == table value by construction, not by care. */
  function writeTable(fig, spec) {
    var t = fig.querySelector('table.dv-table');
    if (!t) {
      t = document.createElement('table');
      t.className = 'dv-table t-cm-legal';
      (fig.querySelector('.dv-tablepanel') || fig).appendChild(t);
    }
    var cap = spec.caption;
    if (!cap) { var fc = fig.querySelector('figcaption'); cap = fc ? fc.textContent.trim() : 'Chart data'; }
    var head = '<caption>' + esc(cap) + '</caption><thead><tr><th scope="col">' +
               esc(spec.categoryLabel || 'Category') + '</th>';
    var i, j;
    for (i = 0; i < spec.series.length; i++) {
      head += '<th scope="col">' + esc(spec.series[i].name) +
              (spec.unit ? ' (' + esc(spec.unit) + ')' : '') + '</th>';
    }
    head += '</tr></thead><tbody>';
    for (i = 0; i < spec.categories.length; i++) {
      head += '<tr><th scope="row">' + esc(spec.categories[i]) + '</th>';
      for (j = 0; j < spec.series.length; j++) { head += '<td>' + spec.series[j].values[i] + '</td>'; }
      head += '</tr>';
    }
    t.innerHTML = head + '</tbody>';
    return t;
  }

  /* ---------- THE ACCESSIBLE NAME. A full sentence, the way the baked snippets read: the subject,
     then every category and its value. Capped so a 40-category chart does not read for a minute;
     the table is the complete answer past that point. */
  function autoLabel(spec) {
    var out = [], i, j, ns = spec.series.length, n = Math.min(spec.categories.length, 12);
    for (i = 0; i < n; i++) {
      for (j = 0; j < ns; j++) {
        out.push((ns > 1 ? spec.series[j].name + ' ' : '') + spec.categories[i] + ' ' +
                 fmt(spec, spec.series[j].values[i]));
      }
    }
    return (spec.caption || 'Chart') + '. ' + out.join(', ') +
           (n < spec.categories.length ? ', and more in the table' : '') + '.';
  }

  /* ---------- AXIS FURNITURE. Emitted by the CORE, identically for every type, in the fit
     grammar: gridlines are lines with data-fx/data-fx2, tick labels are texts with data-fx/data-dx,
     the baseline is a line in --baseline. `axis === "x"` swaps the two roles for horizontal bars. */
  function furniture(ctx, axis, bare) {
    var i, t, p, x, y;
    if (axis === 'x') {
      for (i = 0; i < ctx.ticks.length; i++) {
        t = ctx.ticks[i]; p = ctx.vf(t); x = ctx.PL + p * ctx.plotW;
        if (!bare) {
          ctx.push('<line class="dv-grid" x1="' + n1(x) + '" y1="' + ctx.PT + '" x2="' + n1(x) +
                   '" y2="' + ctx.y0 + '" stroke="var(--data-grid)" data-fx="' + f4(p) +
                   '" data-fx2="' + f4(p) + '"/>');
        }
        ctx.push('<text class="dv-axis t-cm-chart-value" fill="var(--data-axis)" x="' + n1(x) +
                 '" y="' + (ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + f4(p) + '">' +
                 esc(ctx.fmt(t)) + '</text>');
      }
      ctx.push('<line class="dv-axis" x1="' + ctx.PL + '" y1="' + ctx.PT + '" x2="' + ctx.PL +
               '" y2="' + ctx.y0 + '" stroke="var(--baseline)" data-fx="' + f4(ctx.vf(0)) +
               '" data-fx2="' + f4(ctx.vf(0)) + '"/>');
      return;
    }
    for (i = 0; i < ctx.ticks.length; i++) {
      t = ctx.ticks[i]; y = ctx.vy(t);
      if (!bare) {
        ctx.push('<line class="dv-grid" x1="' + ctx.PL + '" y1="' + n1(y) + '" x2="' + n1(ctx.PL + ctx.plotW) +
                 '" y2="' + n1(y) + '" stroke="var(--data-grid)" data-fx="0" data-fx2="1"/>');
      }
      ctx.push('<text class="dv-axis t-cm-chart-value" fill="var(--data-axis)" x="' + (ctx.PL - 8) +
               '" y="' + n1(y + 3) + '" text-anchor="end" data-fx="0" data-dx="-8" data-dy="3">' +
               esc(ctx.fmt(t)) + '</text>');
    }
    var zy = ctx.vy(Math.min(Math.max(0, ctx.min), ctx.max));
    ctx.push('<line class="dv-axis" x1="' + ctx.PL + '" y1="' + n1(zy) + '" x2="' + n1(ctx.PL + ctx.plotW) +
             '" y2="' + n1(zy) + '" stroke="var(--baseline)" data-fx="0" data-fx2="1"/>');
  }

  /* ---------- THE ENGINE. Idempotent by construction: everything inside the <svg> and everything
     inside the <table> is REPLACED, so a filter re-render (rule 14) is one more call with a
     smaller spec, never a diff. The cached fit fractions (data-fy/data-fh) go with the old marks,
     which is exactly right — they described geometry that no longer exists. */
  function dvRender(fig, spec) {
    if (!fig || !fig.querySelector) { bad('first argument must be the <figure> element'); }
    validate(spec);
    var draw = TYPES[spec.type];
    if (typeof draw !== 'function') {
      bad('no type partial registered for "' + spec.type + '" — have: ' +
          (Object.keys(TYPES).sort().join(', ') || '(none)'));
    }
    var svg = fig.querySelector('svg.dv-fit') || fig.querySelector('svg.dv-svg');
    if (!svg) { bad('figure has no <svg class="dv-fit"> canvas to render into'); }

    /* Geometry comes from the canvas's own data-* frame (the kit's 46/12/14/30/260 defaults), and
       the value axis is authored in the data-h coordinate space — NEVER the live viewBox height.
       dv-behaviour's fitY caches every y as a fraction of `data-h − PT − PB`; authoring into a
       already-fitted taller box would cache fractions that describe the wrong plot. */
    var PL = attr(svg, 'data-pl', 46), PR = attr(svg, 'data-pr', 12);
    var PT = attr(svg, 'data-pt', 14), PB = attr(svg, 'data-pb', 30);
    var VH = attr(svg, 'data-h', 260);
    /* ⛔ THE WIDTH IS THE RENDERED ONE, not the authored viewBox. fitOne re-pins the viewBox 1:1
       to the element's CSS width, so one viewBox unit IS one device-independent pixel after a fit
       — and only then is a 2px dv-004 gap actually 2px. Authoring into a 580-wide box that then
       fits to 496 shrank every constant by 5%: MEASURED at #259, the grouped gap landed at 1.90px
       and the driven check went red. Read the box first, author into it, and the constant survives
       the fit. Falls back to the authored viewBox when the element has no layout yet (display:none,
       an unattached figure) — then the first resize does the honest thing. */
    var vb = (svg.getAttribute('viewBox') || '').trim().split(/\s+/);
    var VW = Math.round(svg.getBoundingClientRect().width);
    if (!(VW > 0)) { VW = parseFloat(vb[2]); }
    if (!isFinite(VW) || VW <= 0) { VW = 580; }

    var lo = Infinity, hi = -Infinity, i, j, v;
    if (typeof draw.domain === 'function') { v = draw.domain(spec); lo = v[0]; hi = v[1]; }
    else {
      for (i = 0; i < spec.series.length; i++) {
        for (j = 0; j < spec.series[i].values.length; j++) {
          v = spec.series[i].values[j];
          if (v < lo) { lo = v; } if (v > hi) { hi = v; }
        }
      }
    }
    if (lo > 0) { lo = 0; }                      /* dv-bar-009 — the baseline is zero, always */
    var sc = nice(lo, hi, 4);
    var plotW = VW - PL - PR, plotH = VH - PT - PB, y0 = VH - PB;
    var span = sc.max - sc.min || 1;

    var ctx = {
      fig: fig, svg: svg, spec: spec, cats: spec.categories, series: spec.series,
      PL: PL, PR: PR, PT: PT, PB: PB, VW: VW, VH: VH,
      plotW: plotW, plotH: plotH, y0: y0,
      min: sc.min, max: sc.max, step: sc.step, ticks: sc.ticks,
      GAP: GAP, HIT: HIT, esc: esc, n1: n1, f4: f4,
      fmt: function (n) { return fmt(spec, n); },
      fill: function (k) { return fillOf(spec.series[k] || {}, k); },
      vy: function (n) { return y0 - (n - sc.min) / span * plotH; },   /* value -> px, y axis */
      vf: function (n) { return (n - sc.min) / span; },                /* value -> plot FRACTION */
      fx: function (px) { return (px - PL) / plotW; },                 /* px -> data-fx fraction */
      out: []
    };
    ctx.push = function (s) { ctx.out.push(s); };

    /* #260 A1 — the dial. Default true: every type registered before this line is unchanged. */
    var fu = draw.furniture === undefined ? draw.axis !== 'none' : draw.furniture;
    if (fu) { furniture(ctx, draw.axis === 'x' ? 'x' : 'y', fu === 'axis'); }
    draw(ctx);

    svg.setAttribute('viewBox', '0 0 ' + VW + ' ' + VH);
    svg.innerHTML = ctx.out.join('\n');
    svg.setAttribute('aria-label', spec.label || autoLabel(spec));
    writeTable(fig, spec);

    /* THE ONLY re-fit hook (ADR-0015 §4: no second resize listener anywhere in the group).
       dv-behaviour's one rAF-debounced listener re-derives x from data-fx and caches y. */
    window.dispatchEvent(new Event('resize'));
    return fig;
  }

  dvRender.types = TYPES;
  dvRender.util = { esc: esc, n1: n1, f4: f4, nice: nice, fmt: fmt, fill: fillOf };
  window.dvRender = dvRender;
}());
