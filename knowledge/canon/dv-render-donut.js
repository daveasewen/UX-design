/* dv-render-donut — the DONUT / PIE TYPE PARTIAL for the dv-render engine (s249-D4, built #259).
   Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by gen_component_partials.py.
   Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS TWO TYPES:
     donut  — a ring, ri = 0.6 · ro, with the total in the hole
     pie    — the same arithmetic with ri = 0, drawn as wedges from the centre

   THE RADIAL EXCEPTION. Every other type partial draws INTO the core's cartesian frame. A ring
   has no band axis, no value axis, no gridlines and no baseline, so the first thing this file
   does is DISCARD the furniture the core has already pushed (`ctx.out.length = 0`). That is a
   WORK-AROUND, not a design: `dvRender` calls `furniture()` unconditionally before `draw(ctx)`
   and offers no switch. The core request is stated verbatim in this lane's subreport.

   RULES ENACTED HERE:
     ds-030 (#103 amendment)  circular charts are the exception to fluid-plot scaling: FLUID
               CONTAINER, FIXED-DIAMETER CENTRED PLOT. The diameter is derived from the canvas's
               data-h (VH) alone — ro = (VH − 60) / 2 — so it CANNOT track the width; the centre
               is VW/2, so the ring RE-CENTRES and never re-scales. The consumer's <svg> keeps a
               fixed width/viewBox and `.dv-svg{flex:none; margin-inline:auto}` does the
               centring, which is why a donut canvas must NOT carry `dv-fit` (DV-D02-A makes
               that BLOCKING) and why nothing here is authored as a plot fraction: there is no
               fit pass to re-derive it.
     ds-031    the legend offset STAYS. The ring sits ~109px left of true container centre in the
               legend variant because `.dv-donut-row` centres the svg+legend GROUP. Option A was
               ruled at #106; this file emits geometry into the svg's own box and touches the row
               not at all, so the offset is preserved by construction.
     DV-D12    the sweep-intro easing is keyed to SEGMENT SPANS, and `canon/dv-donut-sweep.js`
               reads that off the marks: every arc carries data-cx/-cy/-ro/-ri/-a1/-a2 and its
               full `d`, and every annotation carries data-seq + data-series-group and the
               `.dv-anno` class. The sweep is an INTRO and its IIFE runs once at load, so a
               consumer must inject/load it AFTER its dvRender() bootstrap — see the snippet.
     dv-004    2px of REAL GEOMETRY between adjacent segments — an angular gap, not a painted
               surface-coloured stroke. The gap is measured at the INNER edge (the narrow one):
               a slice cut by GAP/ri radians is ≥GAP px apart everywhere on the ring, and wider
               (ro/ri = 1.67×) at the outside. ⚠ The static dataviz gate cannot measure an arc
               and falls back to demanding the stroke — reported, not worked around.
     dv-pie-009 ≤6 slices. This is the reason a donut spec carries 6 categories where the other
               types carry 8+: the type does not allow more, and the gate counts table rows.
     §04.3     letters A–F on SPIDER LEADERS, never on the segments (letters-on-segments stays
               HELD — type26-013, white type on series fills). Colour is never the only channel.
     DV-D13    the centre readout follows the legend selection: `<g data-dv-view="value">` and
               `<g data-dv-view="percent">` each hold a `.dv-val`, and every mark carries
               data-tip-value / data-tip-percent so dv-legend's seg can retarget data-tip.
     ds-026 / dv-017 / DEF-004   fills are var() tokens only, via ctx.fill(i) — the solid
               categorical palette, never an opacity tint.
     DEF-003   no scale-physics here. The sweep is data-driven geometry (an SVG arc's angular
               extent is not CSS-animatable — Batch 3 #7) and lives in its own source. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var U = window.dvRender.util, n1 = U.n1, esc = U.esc;
  var KEYS = 'ABCDEF', RAD = Math.PI / 180;

  function pt(cx, cy, r, a) { return [n1(cx + r * Math.cos(a * RAD)), n1(cy + r * Math.sin(a * RAD))]; }
  /* ri = 0 draws a PIE wedge (centre → arc → centre); anything else draws a ring segment. */
  function arc(cx, cy, ro, ri, a1, a2) {
    var b = a2 - a1 > 180 ? 1 : 0;
    var head = 'M' + pt(cx, cy, ro, a1).join(' ') + ' A' + n1(ro) + ' ' + n1(ro) + ' 0 ' + b + ' 1 ' +
      pt(cx, cy, ro, a2).join(' ');
    if (!ri) { return head + ' L' + n1(cx) + ' ' + n1(cy) + ' Z'; }
    return head + ' L' + pt(cx, cy, ri, a2).join(' ') + ' A' + n1(ri) + ' ' + n1(ri) + ' 0 ' + b +
      ' 0 ' + pt(cx, cy, ri, a1).join(' ') + ' Z';
  }

  function ring(ctx, hole) {
    ctx.out.length = 0;                 /* ⚠ the core's cartesian furniture — see the header */
    var cats = ctx.cats, nc = cats.length, i, v;
    if (ctx.series.length !== 1) {
      throw new Error('dv-render-donut: part-to-whole takes ONE series, got ' + ctx.series.length +
        ' — a ring divides a single whole');
    }
    if (nc > 6) {
      throw new Error('dv-render-donut: dv-pie-009 — ' + nc + ' slices, donut/pie is capped at 6');
    }
    var vals = ctx.series[0].values, total = 0;
    for (i = 0; i < nc; i++) {
      v = vals[i];
      if (v < 0) {
        throw new Error('dv-render-donut: "' + cats[i] + '" is ' + v +
          ' — a part cannot be negative; use type "column" for signed data');
      }
      total += v;
    }
    if (!total) { throw new Error('dv-render-donut: every value is zero — there is no whole to divide'); }

    /* ds-030 — the diameter is a HEIGHT fact, the centre is a WIDTH fact. Nothing else. */
    var cx = ctx.VW / 2, cy = ctx.VH / 2, ro = (ctx.VH - 60) / 2, ri = hole ? ro * 0.6 : 0;
    var gap = ctx.GAP / (ri || ro * 0.35) / RAD;   /* dv-004 — 2px at the narrow edge, in degrees */
    var a = -90, annos = [];                       /* -90 = twelve o'clock, sweeping clockwise */
    for (i = 0; i < nc; i++) {
      var span = vals[i] / total * 360;
      var a1 = a + gap / 2, a2 = a + span - gap / 2;
      if (a2 - a1 < 0.4) { a2 = a1 + 0.4; }        /* a real slice keeps a hairline of ink */
      var pc = Math.round(vals[i] / total * 100);
      var lead = KEYS[i % 6] + ' · ' + cats[i] + ': ';
      ctx.push('<path class="dv-series dv-donut-seg dv-marker" data-series-group="' + (i + 1) +
        '" data-cx="' + n1(cx) + '" data-cy="' + n1(cy) + '" data-ro="' + n1(ro) + '" data-ri="' + n1(ri) +
        '" data-a1="' + n1(a1) + '" data-a2="' + n1(a2) + '" fill="' + ctx.fill(i) +
        '" d="' + arc(cx, cy, ro, ri, a1, a2) + '" tabindex="0" role="img" aria-label="' +
        esc(KEYS[i % 6] + ', ' + cats[i] + ': ' + ctx.fmt(vals[i]) + ', ' + pc + ' per cent') +
        '" data-tip="' + esc(lead + ctx.fmt(vals[i])) +
        '" data-tip-value="' + esc(lead + ctx.fmt(vals[i])) +
        '" data-tip-percent="' + esc(lead + pc + '%') + '"></path>');
      /* §04.3 — the letter rides a leader OUTSIDE the ring; data-seq is the sweep's reveal order */
      var am = (a1 + a2) / 2, tip = pt(cx, cy, ro + 22, am);
      annos.push('<polyline class="dv-leader dv-anno show" data-seq="' + i + '" data-series-group="' +
        (i + 1) + '" points="' + pt(cx, cy, ro + 2, am).join(',') + ' ' +
        pt(cx, cy, ro + 14, am).join(',') + '"/>');
      annos.push('<text class="dv-key-el dv-anno show t-cm-chart-key" data-seq="' + i +
        '" data-series-group="' + (i + 1) + '" fill="var(--ink)" text-anchor="middle" x="' + tip[0] +
        '" y="' + n1(parseFloat(tip[1]) + 4) + '">' + KEYS[i % 6] + '</text>');
      a += span;
    }
    for (i = 0; i < annos.length; i++) { ctx.push(annos[i]); }   /* annotations LAST — above the fills */

    /* DV-D13 — the centre pair. RAW numbers, because dv-legend rewrites them with String(sum)
       when the selection changes: a formatted total here would flip to an unformatted one on the
       first legend click. The unit lives in the table header and the tip. */
    var mid = 'class="dv-val t-cm-figure-3" fill="var(--ink)" x="' + n1(cx) + '" y="' + n1(cy + 8) +
      '" text-anchor="middle">';
    ctx.push('<g data-dv-view="value"><text ' + mid + esc(String(total)) + '</text></g>');
    ctx.push('<g data-dv-view="percent" class="dv-off"><text ' + mid + '100%</text></g>');
  }

  window.dvRender.types.donut = function (ctx) { ring(ctx, true); };
  window.dvRender.types.pie = function (ctx) { ring(ctx, false); };
}());
