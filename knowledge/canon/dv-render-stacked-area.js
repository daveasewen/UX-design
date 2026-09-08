/* dv-render-stacked-area — the STACKED-AREA TYPE PARTIAL for the dv-render engine (s249-D4,
   built #259 lane C). Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by
   gen_component_partials.py. Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE: "stacked-area" — composition over time. n series pile up to the category
   TOTAL and each becomes a filled BAND between the running total below it and the running total
   including it. The silhouette of the top band is the total; the thickness of a band is its
   series' value at that category. Categories sit at band MIDPOINTS (the baked exemplar's grammar,
   #96-D1 ⑤), so the first and last vertex are inset half a band from the frame.

   THE SEAM (dv-render-bar is the reference implementation; this file copies it, not the core):
   everything comes off `ctx`, marks are pushed as STRINGS, the core joins them, writes the
   <table> spine and dispatches the ONE resize that re-fits. Nothing here touches dv-render.js.

   THE FIT GRAMMAR THIS TYPE USES (dv-behaviour.js fitOne):
     · path[data-fxs] + [data-ys]  — the band fill. dv-behaviour re-emits `d` as M…L…L… Z from the
       x FRACTIONS and the cached y plot-fractions (data-fys, derived from data-ys once), so the
       authored `d` is a bootstrap for the pre-fit paint and never the source of truth.
     · polyline[data-fxs] + [data-ys] — the .dv-band-line top edge (dv-line-011: straight segments
       only, no curve commands — a stacked area must not imply values between its categories).
     · g[data-fx] + [data-x0]      — the vertex markers. ⛔ data-x0 is NOT optional: fitOne writes
       translate(x − x0, 0) onto the <g>, so a <g> that carries data-fx WITHOUT data-x0 gets its
       child's authored cx ADDED to the fitted x and the marker lands at roughly double the
       distance from the gutter. The baked exemplar ships that defect (see the report); every <g>
       this file emits carries data-x0 = the authored cx of its circle.
     · text[data-fx] — the in-fill letter key and the category label; y is cached by fitY.

   RULES ENACTED HERE:
     dv-2px-separation (#96, standing dataviz canon: "2px separation rule for adjacent blocks is
               STANDING dataviz canon (histogram bars, stacked bands, any adjacent filled blocks)")
               — enacted with REAL GEOMETRY, ctx.GAP px cut off the TOP of every band that has a
               band above it, the same "cut the block BELOW the join" convention dv-render-bar uses
               so the TOP band still reads its true total. The canon `.dv-band` rule also paints a
               2px `stroke:var(--page)` — the ruled surface stroke, dv-004 mechanism 1 — so both
               mechanisms are present and the separation survives either reading.
     dv-004    the gate's own wording is "gapless surfaces (donut/stacked segments) carry a
               surface-coloured stroke >=2px", with a second mechanism (`_rect_stack_gap`) that
               measures y[i+1] − (y[i] + h[i]) across RECTS. ⚠ Neither branch grades this type:
               _validate_dataviz.py fires dv-004 only for dtype in ("donut","pie","stacked"), and
               DTYPE_CANON does NOT fold "stacked-area" into "stacked". Reported, not exempted.
     dv-line-011 straight segments only — every path/polyline command emitted here is M or L.
     ds-026    solid canonical palette, no tints, no alpha dial: colour is ctx.fill(i), i.e. a
               var(--data-series-N) or s184-D3 var(--status-*) token and nothing else (DEF-004).
     ds-030    fully horizontally responsive — every x is a FRACTION (data-fxs/data-fx), so the
               fit re-derives it at any width and no pixel constant survives a resize.
     s248-D2   responsive in BOTH axes: y is authored in the data-h coordinate space and cached by
               fitY as a plot fraction, so a taller tile re-scales the stack instead of clipping.
     §04.3     ≥2 series ⇒ an in-fill LETTER key per band, so colour is never the only channel.
     DEF-003   entry motion is CSS only (.dv-animate .dv-band → the canon dvFade keyframes). This
               file writes no transform, no scale, no timing — every number it emits is an SVG
               geometry attribute derived from the data. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;
  var KEYS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var EDGE = 2;    /* .dv-band-line stroke-width in canon.css — the line is drawn HALF of this
                      inside its own band, so its outer edge lands exactly on the fill's top and
                      the ruled separation above it stays the full ctx.GAP of clear ground. */
  var KEYMIN = 14; /* a letter needs this much band to sit in without touching the join */
  var MKR = 4.2;   /* the exemplar's vertex radius */

  /* The mark's words. `sep` is the only difference between the popover text (· separated, the
     kit's) and the accessible name (comma separated, so a screen reader reads a sentence). */
  function words(ctx, si, ci, v, sep) {
    return KEYS[si % 26] + sep + ctx.series[si].name + sep + ctx.cats[ci] + ': ' + ctx.fmt(v);
  }

  /* THE DOMAIN IS THE STACK TOTAL, not the largest single value — the one thing the core cannot
     infer from the spec, which is why `fn.domain` exists (see dv-render-bar's stackDomain).
     A negative throws NAMED: a band that runs backwards down the stack is not a stacked area, and
     drawing it would silently make the total wrong rather than obviously wrong. */
  function stackDomain(spec) {
    var hi = 0, ci, si, v, pos;
    for (ci = 0; ci < spec.categories.length; ci++) {
      pos = 0;
      for (si = 0; si < spec.series.length; si++) {
        v = spec.series[si].values[ci];
        if (v < 0) {
          throw new Error('dv-render-stacked-area: "' + spec.series[si].name + '" is ' + v +
            ' at "' + spec.categories[ci] + '" — a stacked area has no signed band (the total ' +
            'would stop being the silhouette); use type "column" for signed data');
        }
        pos += v;
      }
      if (pos > hi) { hi = pos; }
    }
    return [0, hi];
  }

  function pts(xs, ys) {
    var out = [], i;
    for (i = 0; i < xs.length; i++) { out.push(n1(xs[i]) + ',' + n1(ys[i])); }
    return out;
  }

  function area(ctx) {
    var ns = ctx.series.length, nc = ctx.cats.length;
    var band = ctx.plotW / nc, ci, si, i;
    var px = [], fx = [], cum = [];
    for (ci = 0; ci < nc; ci++) {
      px.push(ctx.PL + (ci + 0.5) * band);          /* the category MIDPOINT */
      fx.push(f4(ctx.fx(px[ci])));
      cum.push(0);                                  /* the running total under the current band */
    }
    var lines = [], mks = [], keys = [];
    for (si = 0; si < ns; si++) {
      var top = [], foot = [], edge = [], tot = 0;
      var lifted = si < ns - 1;                     /* has a band above it ⇒ owns the ruled gap */
      for (ci = 0; ci < nc; ci++) {
        var v = ctx.series[si].values[ci];
        var lo = ctx.vy(cum[ci]), hi = ctx.vy(cum[ci] + v);
        /* dv-2px-separation — ctx.GAP of REAL ground off the TOP of the band BELOW each join.
           GAP is 2.2, not 2: the fit re-derives x and y independently and rounds each to one
           decimal, so up to 0.15px can vanish out of a gap (MEASURED by the #259 core lane). */
        if (lifted) { hi += ctx.GAP; }
        if (hi > lo - 1) { hi = lo - 1; }           /* a zero band still keeps a hairline */
        top.push(hi); foot.push(lo); edge.push(hi + (lifted ? EDGE / 2 : 0));
        cum[ci] += v; tot += v;

        mks.push('<g class="dv-marker" tabindex="0" role="img" aria-label="' +
          esc(words(ctx, si, ci, v, ', ')) + '" data-tip="' + esc(words(ctx, si, ci, v, ' · ')) +
          '" data-fx="' + fx[ci] + '" data-x0="' + n1(px[ci]) + '"><circle class="dv-mk" style="--sc:' +
          ctx.fill(si) + '" cx="' + n1(px[ci]) + '" cy="' + n1(hi + (lifted ? EDGE / 2 : 0)) +
          '" r="' + MKR + '"/></g>');
        if (ns > 1 && lo - hi >= KEYMIN) {
          keys.push('<text class="dv-barkey t-cm-chart-key" data-series-group="' + (si + 1) +
            '" fill="var(--data-text-on-series)" x="' + n1(px[ci]) + '" y="' + n1((hi + lo) / 2 + 4) +
            '" text-anchor="middle" data-fx="' + fx[ci] + '">' + KEYS[si % 26] + '</text>');
        }
      }
      /* THE BAND — up the top edge, back along the foot, closed. Same x fractions in both
         directions, which is why data-fxs is the forward list followed by its reverse. */
      var bx = px.concat(px.slice().reverse()), by = top.concat(foot.slice().reverse());
      var bf = fx.concat(fx.slice().reverse()), p = pts(bx, by);
      ctx.push('<path class="dv-band dv-series" data-series-group="' + (si + 1) +
        '" data-series-i="' + (si + 1) + '" style="--sc:' + ctx.fill(si) +
        '" data-fxs="' + bf.join(' ') + '" data-ys="' + by.map(n1).join(' ') +
        '" d="M' + p.join(' L') + ' Z" tabindex="0" role="img" aria-label="' +
        esc(KEYS[si % 26] + ', ' + ctx.series[si].name + ', total ' + ctx.fmt(tot)) +
        '" data-tip="' + esc(KEYS[si % 26] + ' · ' + ctx.series[si].name + ' · total ' +
        ctx.fmt(tot)) + '"></path>');
      lines.push('<polyline class="dv-band-line" style="--sc:' + ctx.fill(si) +
        '" data-fxs="' + fx.join(' ') + '" data-ys="' + edge.map(n1).join(' ') +
        '" points="' + pts(px, edge).join(' ') + '"/>');
    }
    for (i = 0; i < lines.length; i++) { ctx.push(lines[i]); }   /* edges above every fill */
    for (i = 0; i < mks.length; i++) { ctx.push(mks[i]); }
    for (i = 0; i < keys.length; i++) { ctx.push(keys[i]); }
    for (ci = 0; ci < nc; ci++) {
      ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(px[ci]) +
        '" y="' + (ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + fx[ci] + '">' +
        esc(ctx.cats[ci]) + '</text>');
    }
  }

  area.axis = 'y';
  area.domain = stackDomain;
  T['stacked-area'] = area;
}());
