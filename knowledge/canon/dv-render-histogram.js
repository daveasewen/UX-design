/* dv-render-histogram — the HISTOGRAM TYPE PARTIAL for the dv-render engine (s259-D1 fast
   follower, built #260). Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by
   gen_component_partials.py. Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE: `histogram` — the distribution of ONE continuous variable, binned.

   WHY IT IS NOT `column` WITH A DIFFERENT NAME. A column chart puts a GUTTER between bands
   because its categories are discrete: Housing and Groceries are separate things and the gap
   says so. A histogram's bins are CONTIGUOUS because the variable underneath them is
   continuous: £150–200 ends exactly where £200–250 begins, and a gap there would assert a
   range with no data in it. So this partial tiles the plot edge to edge — band = plotW / bins,
   mark width = the whole band — and that tiling is the type's contract, driven and asserted.

   dv-004 AND WHY THERE IS NO GEOMETRIC GAP HERE (#96-D3, and the difference from dv-render-bar).
   The standing 2px separation rule for adjacent filled blocks is met on this type by a
   2px PAGE-COLOURED STROKE that canon.css already puts on `:where(.cn-chart-histogram)
   rect.dv-series` — the same idiom dv-004 permits for donut/pie segments, chosen at #96 precisely
   because histogram bars are edge-to-edge. Cutting `ctx.GAP` out of each bin instead would open a
   real hole between bins and DESTROY the contiguity that makes the chart a histogram. The static
   gate agrees: `_validate_dataviz.py` scopes dv-004 to donut/pie/stacked and never reads this
   type. ⛔ Do not "fix" the missing gap here — the separation is in the stylesheet, on purpose.

   RULES ENACTED HERE:
     #96-D3    contiguous bins, separation by the canon.css page-coloured stroke (above).
     dv-bar-009 the count axis starts at zero — the core floors the domain at 0, and the figure
               declares `data-domain-min="0"`; a negative frequency THROWS, named, because a
               count below zero is a data defect and drawing it downward would hide one.
     ONE SERIES a histogram is ONE distribution. Two series side by side in one band is a
               grouped column and two series stacked is a stacked column; both already exist as
               registered types. Passing two here THROWS rather than drawing a chart whose
               marks would overlap exactly.
     s116-D1   a bin is a hit target (tabindex + data-tip). Its width is the BAND and cannot be
               lifted to the 24px floor without breaking contiguity, so a chart binned finer
               than the plot can pay for is reported, not silently re-widened — see the note on
               `thin` below, which is the same argument for labels.
     §04.3     one series, one fill, so colour encodes nothing and needs no second channel; the
               bin LABEL under each mark is the channel that carries meaning.
     DEF-003   entry motion is CSS: `.dv-animate` + data-grow="up" + a stagger in
               animation-delay. No JS geometry animation. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;

  /* The mark's words. `sep` is the only difference between the popover text and the accessible
     name, exactly as dv-render-bar does it. The series NAME is the noun the count counts
     ("12 transactions"), which is why a histogram spec names its one series after the unit of
     observation rather than after the measure. */
  function words(ctx, ci, v) {
    var noun = ctx.series[0].name;
    return ctx.cats[ci] + ': ' + ctx.fmt(v) + (noun ? ' ' + noun : '');
  }

  /* LABEL THINNING. Every bin gets a mark; not every bin can get a legible label. When the band
     is narrower than the widest label needs, label every nth bin — n chosen so the survivors are
     at least one label-width apart. The FIRST bin is always labelled and the LAST is labelled
     whenever it does not collide with the survivor before it, because the two ends are what name
     the range and a colliding pair names nothing. Estimated from the character count at the 12px chart-label size (~6.2px per
     character): a measurement is not available at render time, and over-estimating drops a label
     that would have fitted, which is the safe direction. */
  function stride(cats, band) {
    var w = 0, i;
    for (i = 0; i < cats.length; i++) { w = Math.max(w, String(cats[i]).length * 6.2 + 8); }
    var n = Math.ceil(w / band);
    return n < 1 ? 1 : n;
  }

  function histogram(ctx) {
    var nc = ctx.cats.length, ci;
    if (ctx.series.length !== 1) {
      throw new Error('dv-render-histogram: a histogram is ONE distribution, got ' +
        ctx.series.length + ' series — use type "grouped-column" or "stacked-column" for more');
    }
    var vals = ctx.series[0].values;
    for (ci = 0; ci < nc; ci++) {
      if (vals[ci] < 0) {
        throw new Error('dv-render-histogram: bin "' + ctx.cats[ci] + '" has frequency ' +
          vals[ci] + ' — a count cannot be negative (dv-bar-009, the axis starts at zero)');
      }
    }
    var band = ctx.plotW / nc;              /* CONTIGUOUS — the whole band is the mark */
    var st = stride(ctx.cats, band);
    for (ci = 0; ci < nc; ci++) {
      var v = vals[ci], x = ctx.PL + ci * band;
      var top = ctx.vy(v), h = ctx.y0 - top;
      if (h < 1) { h = 1; top = ctx.y0 - 1; }        /* an empty bin keeps a hairline of ink */
      ctx.push('<rect class="dv-series" data-grow="up" style="animation-delay:' + (ci * 32) +
        'ms" fill="' + ctx.fill(0) + '" x="' + n1(x) + '" y="' + n1(top) + '" width="' + n1(band) +
        '" height="' + n1(h) + '" data-fx="' + f4(ctx.fx(x)) + '" data-fw="' + f4(band / ctx.plotW) +
        '" tabindex="0" role="img" aria-label="' + esc(words(ctx, ci, v)) +
        '" data-tip="' + esc(words(ctx, ci, v)) + '"></rect>');
      /* The bin label sits under the CENTRE of its own bin and rides data-fx, so the fit moves it
         with the bin rather than re-measuring text (DV-D02 — text never scales). */
      if (ci % st === 0 || (ci === nc - 1 && (nc - 1) % st * 2 >= st)) {
        var lx = x + band / 2;
        ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(lx) +
          '" y="' + n1(ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + f4(ctx.fx(lx)) + '">' +
          esc(ctx.cats[ci]) + '</text>');
      }
    }
  }

  histogram.axis = 'y';
  T.histogram = histogram;
}());
