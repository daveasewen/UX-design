/* dv-render-combo — the COMBO TYPE PARTIAL for the dv-render engine (s249-D4, built #259).
   Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by gen_component_partials.py.
   Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE: `combo` — columns on the PRIMARY (zero-based) value axis plus a line
   overlay on an optional SECONDARY value axis, over ONE shared band axis.

   ⛔ IT DRAWS NOTHING ITSELF. Not one rect, not one polyline. `combo` is a COMPOSER: it splits
   the spec's series into a column group and a line group, builds a sub-ctx for each — same
   `push`, same `out`, same plot frame, that group's series, that group's scale and that group's
   palette indices — and calls `dvRender.types.column` and `dvRender.types.line` on them. Re-
   implementing bars or lines here would be two more copies of arithmetic that already exists in
   two files, and the copies are what drift. The only marks this file authors are the SECONDARY
   AXIS furniture and the optional TARGET rule, because neither belongs to either delegate.

   THE SPEC EXTENSION (everything else is the core's contract, unchanged):
     series[i].kind    "column" | "line".  Absent ⇒ series 0 is the column, the rest are lines.
     series[i].unit    per-series unit for tips/labels — a combo's two axes carry two units
                       (dv-line-006), and one `spec.unit` cannot say "£000" and "%" at once.
     spec.sharedScale  true ⇒ ONE value axis for both groups, no right-edge rule (same-unit combo).
     spec.target       a number on the SECONDARY scale (primary when sharedScale) ⇒ the dashed
                       [data-dv-view="target"] group dv-behaviour's segmented toggle shows/hides.
     spec.targetLabel  its label. Default "Target <formatted value>".

   THE TWO AXES (dv-line-006 honoured, DV-D07 roles kept):
     PRIMARY   the columns'. `combo.domain` returns the COLUMN series' range only, floored at zero
               (dv-bar-009 blocking) — so the core's gridlines, left tick labels and ink baseline
               are the BARS' scale. Bars own the plot floor and own the grid.
     SECONDARY the line's, computed here with the core's own `nice()` and deliberately NOT floored
               at zero (dv-line-001: zero is optional where floating aids interpretation). Drawn
               as a RIGHT-EDGE rule in the quieter data/axis role plus a full suffixed tick run,
               which is what keeps a floating floor explicit instead of silent.

   RE-KEYING, and why a composer needs it. A delegate numbers its marks 1..n WITHIN its own group
   (`data-series-group="1"`), and `dv-render-bar` omits the attribute altogether for a single
   series. dv-legend filters on the SPEC's series number, so every mark a delegate pushed is
   re-keyed to its spec index here. The line delegate's repeat of the category labels is dropped
   in the same pass — the column delegate already wrote them, on the same band centres.

   RULES ENACTED HERE:
     dv-line-006  dual axes for different UNITS only; the legend names the axis per series
                  (snippet markup), the tick run carries the unit suffix.
     dv-line-001  the secondary axis may float; the primary may not.
     dv-bar-009   the column domain floors at zero, always.
     DV-D07       secondary rule = data/axis (chrome), primary baseline = --baseline (plot floor).
     dv-017/DEF-004  every colour is a var() token — ctx.fill(i) and --data-axis, nothing named.
     ADR-0015 §4  no listener, no timer, no external src; the core dispatches the one resize.

   THE SEAM IT CONSUMES (unchanged from dv-render-bar, the reference implementation): marks carry
   their x as a fraction — rect `data-fx`+`data-fw`, polyline `data-fxs="…"`+`data-ys`, g
   `data-fx`+`data-x0` — plus `data-tip`, `tabindex="0"`, `role="img"` and `aria-label`. This file
   never touches those attributes except to re-key `data-series-group`. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's own error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, esc = U.esc;

  /* series -> [columnGroup, lineGroup]; each entry keeps its SPEC INDEX, which is the palette
     slot, the legend's number and the re-key target. Default: series 0 columns, the rest lines. */
  function split(series) {
    var col = [], lin = [], i, k;
    for (i = 0; i < series.length; i++) {
      k = series[i].kind || (i === 0 ? 'column' : 'line');
      if (k !== 'column' && k !== 'line') {
        throw new Error('dv-render-combo: spec.series[' + i + '].kind "' + k +
          '" is not "column" or "line"');
      }
      (k === 'column' ? col : lin).push({ s: series[i], i: i });
    }
    return [col, lin];
  }

  /* One group's formatter. `series[i].unit` beats `spec.unit`, because the whole point of a
     combo's second axis is that the two groups are measured in different things. */
  function fmtr(spec, s) {
    var o = { format: s.format || spec.format, unit: s.unit === undefined ? spec.unit : s.unit };
    return function (v) { return U.fmt(o, v); };
  }

  /* The sub-ctx. Prototype-linked to the real ctx so push/out/cats/PL/plotW/HIT/GAP and the rest
     are the SAME objects — a delegate cannot tell it is drawing half a chart — with only the
     series, the palette mapping, the formatter and (for the line) the scale exchanged. */
  function sub(ctx, grp, sc) {
    var o = Object.create(ctx), i, span = sc ? (sc.max - sc.min) || 1 : 1;
    o.series = [];
    for (i = 0; i < grp.length; i++) { o.series.push(grp[i].s); }
    o.fill = function (k) { return ctx.fill(grp[k].i); };
    o.fmt = fmtr(ctx.spec, grp[0].s);
    if (sc) {
      o.min = sc.min; o.max = sc.max; o.step = sc.step; o.ticks = sc.ticks;
      o.vf = function (v) { return (v - sc.min) / span; };
      o.vy = function (v) { return ctx.y0 - (v - sc.min) / span * ctx.plotH; };
    }
    return o;
  }

  /* Re-key everything a delegate pushed since `from` to the spec's series numbers, and (drop)
     bin the second copy of the category labels. */
  function rekey(ctx, from, grp, drop) {
    function up(a, d) { return 'data-series-group="' + (grp[d - 1].i + 1) + '"'; }
    for (var i = from; i < ctx.out.length; i++) {
      var s = ctx.out[i];
      if (drop && s.indexOf('class="dv-label') > -1) { ctx.out[i] = ''; }
      else if (s.indexOf('data-series-group="') > -1) {
        ctx.out[i] = s.replace(/data-series-group="(\d+)"/g, up);
      } else if (/class="(dv-series|dv-casing|dv-marker|dv-endkey)/.test(s)) {
        ctx.out[i] = s.replace('class="', 'data-series-group="' + (grp[0].i + 1) + '" class="');
      }
    }
  }

  /* THE COMBO'S INTERSECTION MECHANISM (dv-016, both modes). ds-026's categorical palette is
     ISOLUMINANT BY DESIGN, so a line crossing a bar sits at about 1.04:1 against it — no pair of
     series colours can ever separate that crossing, and picking "better" ones is not an option a
     partial has. A PAGE-COLOUR CASING under the line (6.5px beneath the delegate's 2.5px series
     stroke) makes every crossing boundary page-vs-bar-fill instead, which is the bar's own
     gate-checked ≥3:1. The casing is the delegate's OWN polyline restroked, so the two can never
     come to describe different geometry; `polyline.dv-casing{stroke:var(--page)}` is in canon.css
     and the presentation stroke is dropped so the token wins. */
  function casing(ctx, from) {
    for (var i = from; i < ctx.out.length; i++) {
      var s = ctx.out[i];
      if (s.indexOf('<polyline class="dv-series"') === 0) {
        ctx.out[i] = s.replace('class="dv-series"', 'class="dv-casing"')
          .replace(/ stroke="[^"]*"/, '').replace('stroke-width="2.5"', 'stroke-width="6.5"')
          .replace(/ data-series-i="\d+"/, '') + '\n' + s;
      }
    }
  }

  /* SECONDARY AXIS — right-edge rule + suffixed ticks, in the fit grammar (data-fx="1" pins it to
     the plot's right edge at every width; data-dx keeps the 8px label offset a real 8px). */
  function axis2(ctx, sc, f) {
    var span = (sc.max - sc.min) || 1, x = ctx.PL + ctx.plotW, i, t, y;
    ctx.push('<line class="dv-axis2" x1="' + n1(x) + '" y1="' + ctx.PT + '" x2="' + n1(x) +
      '" y2="' + ctx.y0 + '" stroke="var(--data-axis)" data-fx="1" data-fx2="1"/>');
    for (i = 0; i < sc.ticks.length; i++) {
      t = sc.ticks[i]; y = ctx.y0 - (t - sc.min) / span * ctx.plotH;
      ctx.push('<text class="dv-axis t-cm-chart-value" fill="var(--data-axis)" x="' + n1(x + 8) +
        '" y="' + n1(y + 3) + '" text-anchor="start" data-fx="1" data-dx="8" data-dy="3">' +
        esc(f(t)) + '</text>');
    }
  }

  /* The TARGET overlay — a dv-behaviour view group, shipped hidden; the figure's segmented
     toggle is what shows it. Its label anchors LEFT: the right end is the endkey and the
     secondary tick zone, and the last point often sits on the target. */
  function target(ctx, sc, f) {
    var t = ctx.spec.target;
    if (typeof t !== 'number') { return; }
    var span = (sc.max - sc.min) || 1;
    var y = n1(ctx.y0 - (t - sc.min) / span * ctx.plotH);
    ctx.push('<g data-dv-view="target" class="dv-off"><line class="dv-target" x1="' + ctx.PL +
      '" y1="' + y + '" x2="' + n1(ctx.PL + ctx.plotW) + '" y2="' + y +
      '" data-fx="0" data-fx2="1"/><text class="dv-target-label t-cm-chart-label" x="' +
      n1(ctx.PL + 4) + '" y="' + n1(y - 4) + '" text-anchor="start" data-fx="0" data-dx="4">' +
      esc(ctx.spec.targetLabel || ('Target ' + f(t))) + '</text></g>');
  }

  function combo(ctx) {
    var g = split(ctx.series), col = g[0], lin = g[1], i, j, v;
    if (!col.length || !lin.length) {
      throw new Error('dv-render-combo: a combo needs at least one kind:"column" series AND one ' +
        'kind:"line" series — got ' + col.length + ' column and ' + lin.length + ' line');
    }
    if (typeof T.column !== 'function' || typeof T.line !== 'function') {
      throw new Error('dv-render-combo: combo COMPOSES the column and line type partials — load ' +
        'canon/dv-render-bar.js and canon/dv-render-line.js beside the core');
    }
    var f2 = fmtr(ctx.spec, lin[0].s), sc = null;
    if (!ctx.spec.sharedScale) {
      var lo = Infinity, hi = -Infinity;
      for (i = 0; i < lin.length; i++) {
        for (j = 0; j < lin[i].s.values.length; j++) {
          v = lin[i].s.values[j];
          if (v < lo) { lo = v; } if (v > hi) { hi = v; }
        }
      }
      sc = U.nice(lo, hi, 4);      /* dv-line-001 — NOT floored at zero: the second axis may float */
      axis2(ctx, sc, f2);
    }
    var at = ctx.out.length;
    T.column(sub(ctx, col, null));
    rekey(ctx, at, col, false);
    target(ctx, sc || { min: ctx.min, max: ctx.max }, sc ? f2 : ctx.fmt);
    at = ctx.out.length;
    T.line(sub(ctx, lin, sc));     /* LAST — the line reads over the bars, casing and all */
    casing(ctx, at);
    rekey(ctx, at, lin, true);
  }

  /* The primary domain is the COLUMNS' range, floored at zero (dv-bar-009). Without this the core
     would scale the bars against the line's numbers — a percentage and a payment volume share a
     band axis, never a value axis. */
  combo.domain = function (spec) {
    var col = split(spec.series)[0], lo = 0, hi = 0, i, j, v;
    for (i = 0; i < col.length; i++) {
      for (j = 0; j < col[i].s.values.length; j++) {
        v = col[i].s.values[j];
        if (v < lo) { lo = v; } if (v > hi) { hi = v; }
      }
    }
    return [lo, hi];
  };
  combo.axis = 'y';
  T.combo = combo;
}());
