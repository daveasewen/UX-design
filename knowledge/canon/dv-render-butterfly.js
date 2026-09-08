/* dv-render-butterfly — the BUTTERFLY TYPE PARTIAL for the dv-render engine (s249-D4 engine,
   s259-D1 fast follower, built #260 lane F4). Hand-authored SOURCE; injected between
   AUTO-BEHAVIOUR markers by gen_component_partials.py. Edit HERE and regenerate — never
   between a consumer's markers.

   REGISTERS TWO TYPES, the two orientations of one idea:
     butterfly-h — mirrored HORIZONTAL bars, left wing and right wing, category names in a
                   shared CENTRE GUTTER between the two baselines (axis "x")
     butterfly-v — mirrored VERTICAL columns, up wing and down wing, one shared horizontal
                   baseline through the middle of the plot, category names below it (axis "y")

   ONE FILE, ONE PAIR OF ROUTINES — and that is the cheaper answer for BOTH members, because the
   two orientations share the domain, the validation, the DV-D09 fill rule, the mark writer and
   the wing arithmetic; only the axis assignment differs. Two files would have duplicated ~1.6 KB
   of that into each, and the member page budget prices a member for the type partial it consumes,
   not for the file count. Byte arithmetic is in the lane subreport.

   ⛔ THE MIRROR IS THE SECOND SERIES, NOT A SIGN. A butterfly plots two POSITIVE measures in
   opposed directions; it is not a signed column. So the domain is SYMMETRIC — [-M, +M] over the
   largest magnitude in either wing — which is what makes both wings share ONE scale (a butterfly
   that scaled its halves independently would misrepresent the data, Chart-butterfly-v's own
   header note), and a negative value inside a wing THROWS, named, rather than drawing backwards
   through the gutter. That is the meta's antiPattern stated as an error message.

   ⛔ NO CARTESIAN FURNITURE, and it is a geometry choice with a receipt, not a shortcut. Both
   reference implementations draw NO gridlines and NO value-axis tick labels — "a butterfly's
   shared centre gutter substitutes for a value axis" (Chart-butterfly-h header, ds-020 declared
   gap, gated green at #95). Keeping the core's furniture here would also be WRONG, not merely
   redundant: the symmetric domain makes the lower/left half of every tick NEGATIVE, and a tick
   reading "-40" under a wing whose value is 40 is a misstatement. `dvRender` calls `furniture()`
   unconditionally, so this partial opens by DISCARDING what the core has already pushed — the
   same move `dv-render-donut` makes, and this lane SECONDS its core request (an `fn.axis="none"`
   opt-out). See knowledge/_tmp/260/butterfly.core-requests.md.

   RULES ENACTED HERE:
     dv-004    2px of REAL geometry between adjacent filled blocks. On butterfly-v the two wings
               MEET at the baseline — the reference bake had 0.0px there — so half a GAP is cut
               off each wing and the pair is separated by the full 2.2px. On butterfly-h the
               centre gutter (19.6% of the plot) is the separation, and it is enormous.
     s116-D1   a bar is a hit target: thickness is floored at 24px wherever the band can pay for
               it, and every mark carries tabindex=0 + role=img + aria-label + data-tip.
     DV-D09    the two wings bind data/series/1 and data/series/3 — the orientation-distinct pair
               both reference snippets and both #token-manifest contrastPairs already declare.
               A series carrying an s184-D3 `role` keeps the status ramp instead.
     DV-D02    responsive = compress width, never scale text. Every x is authored as data-fx /
               data-fw, INCLUDING the centre gutter, which is a FRACTION of the plot (0.196 —
               the reference's own 90/460) precisely so the fit can re-derive it.
     §04.3     on-chart letter keys are DELIBERATELY OMITTED: direction (left/right, up/down) is
               already a non-colour channel, so a third one is redundant. Receipted as a delta
               from the bar contract in both metas since #95; repeated here, not re-decided.
     DEF-003   entry motion is CSS: data-grow="left"/"right"/"up"/"down" + a 45ms per-category
               stagger in animation-delay. No JS geometry animation. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's "no type partial" error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc;

  /* The centre gutter of the horizontal butterfly, as a FRACTION of the plot width. The reference
     bake is 90px of a 460px plot = 0.1957: the gutter has to be proportional because the fit
     re-derives every rect x AND width from fractions, so a fixed-px gutter could not survive it. */
  var GUT = 0.196;

  function bad(msg) { throw new Error('dv-render-butterfly: ' + msg); }

  function check(ctx) {
    if (ctx.series.length !== 2) {
      bad('a butterfly mirrors a PAIR — got ' + ctx.series.length + ' series. The mirrored-gutter ' +
        'geometry only reads for two; use "grouped-column" or "bar" for three or more');
    }
    for (var s = 0; s < 2; s++) {
      for (var i = 0; i < ctx.cats.length; i++) {
        var v = ctx.series[s].values[i];
        if (v < 0) {
          bad('"' + ctx.cats[i] + '" is ' + v + ' in "' + ctx.series[s].name + '" — the MIRROR ' +
            'already encodes the second series, so a negative inside a wing is ambiguous; use ' +
            'type "column" for signed data');
        }
      }
    }
  }

  /* DV-D09 — wing 1 = data/series/1, wing 2 = data/series/3. A roled series keeps s184-D3. */
  function fillAt(ctx, si) {
    return ctx.series[si].role ? ctx.fill(si) : 'var(--data-series-' + (si ? 3 : 1) + ')';
  }
  /* The mark's words. `sep` is the only difference between the popover (· separated, the kit's)
     and the accessible name (comma separated, so a screen reader reads a sentence). */
  function words(ctx, si, ci, v, sep) {
    return ctx.cats[ci] + sep + ctx.series[si].name + ': ' + ctx.fmt(v);
  }
  /* One band holds ONE pair (the wings are opposed, not side by side), so the band is not shared:
     keep a 28% gutter between neighbouring CATEGORIES and lift to the 24px hit floor if it fits. */
  function thickness(ctx, band) {
    var t = band * 0.72;
    if (t < ctx.HIT && ctx.HIT <= band) { t = ctx.HIT; }
    return t < 1 ? 1 : t;
  }
  /* A value as its share of ONE wing, in [0, 1]. The domain is symmetric with zero at vf 0.5, so
     twice the distance from the centre IS the wing share — no second scale is introduced. */
  function wing(ctx, v) {
    var k = (ctx.vf(v) - 0.5) * 2;
    return k < 0 ? 0 : k > 1 ? 1 : k;
  }

  function mark(ctx, si, ci, v, grow, x, y, w, h) {
    ctx.push('<rect class="dv-series" data-series-group="' + (si + 1) + '" data-series-i="' + (si + 1) +
      '" data-grow="' + grow + '" style="animation-delay:' + (ci * 45) + 'ms" fill="' + fillAt(ctx, si) +
      '" x="' + n1(x) + '" y="' + n1(y) + '" width="' + n1(w) + '" height="' + n1(h) +
      '" data-fx="' + f4(ctx.fx(x)) + '" data-fw="' + f4(w / ctx.plotW) +
      '" tabindex="0" role="img" aria-label="' + esc(words(ctx, si, ci, v, ', ')) +
      '" data-tip="' + esc(words(ctx, si, ci, v, ' · ')) + '"></rect>');
  }
  function label(ctx, x, y, fx, text) {
    ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(x) +
      '" y="' + n1(y) + '" text-anchor="middle" data-fx="' + f4(fx) + '">' + esc(text) + '</text>');
  }

  /* ---------- HORIZONTAL. Two baselines either side of the centre gutter; the left wing flows
     LEFT from the left baseline, the right wing RIGHT from the right one, and the category name
     sits in the gutter between them, where no bar can ever run over it. */
  function horizontal(ctx) {
    ctx.out.length = 0;                 /* discard the core's furniture — see the header */
    check(ctx);
    var nc = ctx.cats.length, half = GUT / 2, span = 0.5 - half;
    var band = ctx.plotH / nc, th = thickness(ctx, band), pad = (band - th) / 2;
    var ci, si, i, fx;
    for (i = 0; i < 2; i++) {
      fx = 0.5 + (i ? half : -half);
      ctx.push('<line class="dv-axis" x1="' + n1(ctx.PL + fx * ctx.plotW) + '" y1="' + ctx.PT +
        '" x2="' + n1(ctx.PL + fx * ctx.plotW) + '" y2="' + n1(ctx.y0) +
        '" stroke="var(--baseline)" data-fx="' + f4(fx) + '" data-fx2="' + f4(fx) + '"/>');
    }
    for (ci = 0; ci < nc; ci++) {
      var y = ctx.PT + ci * band + pad;
      for (si = 0; si < 2; si++) {
        var v = ctx.series[si].values[ci];
        var w = wing(ctx, v) * span * ctx.plotW;
        if (w < 1) { w = 1; }           /* a real zero still keeps a hairline of ink */
        var edge = ctx.PL + (0.5 + (si ? half : -half)) * ctx.plotW;
        mark(ctx, si, ci, v, si ? 'right' : 'left', si ? edge : edge - w, y, w, th);
      }
      label(ctx, ctx.PL + 0.5 * ctx.plotW, y + th / 2 + 4, 0.5, ctx.cats[ci]);
    }
  }

  /* ---------- VERTICAL. One shared baseline through the middle of the plot; the first series
     grows UP from it, the second DOWN, on the same scale. dv-004: half a gap off each wing, so
     the pair that MEETS at the baseline is separated by the full 2.2px of real geometry. */
  function vertical(ctx) {
    ctx.out.length = 0;
    check(ctx);
    var nc = ctx.cats.length, band = ctx.plotW / nc;
    var th = thickness(ctx, band), pad = (band - th) / 2;
    var mid = ctx.vy(0), cut = ctx.GAP / 2, full = ctx.plotH / 2, ci, si;
    ctx.push('<line class="dv-axis" x1="' + ctx.PL + '" y1="' + n1(mid) + '" x2="' +
      n1(ctx.PL + ctx.plotW) + '" y2="' + n1(mid) +
      '" stroke="var(--baseline)" data-fx="0" data-fx2="1"/>');
    for (ci = 0; ci < nc; ci++) {
      var x = ctx.PL + ci * band + pad;
      for (si = 0; si < 2; si++) {
        var v = ctx.series[si].values[ci];
        var h = wing(ctx, v) * full - cut;
        if (h < 1) { h = 1; }
        mark(ctx, si, ci, v, si ? 'down' : 'up', x, si ? mid + cut : mid - cut - h, th, h);
      }
      label(ctx, x + th / 2, ctx.y0 + 16, ctx.fx(x + th / 2), ctx.cats[ci]);
    }
  }

  /* The SYMMETRIC domain — the one thing the core cannot infer, and the reason both wings share
     one scale. The core's `if (lo > 0) lo = 0` cannot disturb it: lo is never positive here. */
  function domain(spec) {
    var m = 0, si, i, a;
    for (si = 0; si < spec.series.length; si++) {
      for (i = 0; i < (spec.series[si].values || []).length; i++) {
        a = Math.abs(spec.series[si].values[i]);
        if (a > m) { m = a; }
      }
    }
    return m ? [-m, m] : [-1, 1];
  }

  function mk(fn, axis) { fn.axis = axis; fn.domain = domain; return fn; }

  T['butterfly-h'] = mk(function (ctx) { horizontal(ctx); }, 'x');
  T['butterfly-v'] = mk(function (ctx) { vertical(ctx); }, 'y');
}());
