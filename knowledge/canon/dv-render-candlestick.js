/* dv-render-candlestick — the CANDLESTICK TYPE PARTIAL for the dv-render engine (s259-D1 fast
   follower, built #260). Hand-authored SOURCE; injected between AUTO-BEHAVIOUR markers by
   gen_component_partials.py. Edit HERE and regenerate — never between a consumer's markers.

   REGISTERS ONE TYPE: `candlestick` — open/high/low/close per period, one candle per session.

   THE SPEC — the RULED SHAPE, UNEXTENDED. OHLC is four numbers per period, and `series` is
   already "n named arrays, one value per category", so the four price points ARE four series:

     { type: "candlestick",
       categories: ["S1", "S2", … "S40"],
       series: [{ name: "Open",  values: […] },
                { name: "High",  values: […] },
                { name: "Low",   values: […] },
                { name: "Close", values: […] }],
       unit?: "£", caption?, categoryLabel?: "Session" }

   That is not a convenience: it is why the a11y answer survives the move to the engine intact.
   The core's `writeTable` emits `Session | Open | High | Low | Close` off this spec — column for
   column, the table the promoted snippet baked by hand — and ds-027 (Dave, #100) makes that
   table THE accessibility fallback ("we're using the table as the fallback position for Ally"),
   not a decoration. One spec, one table, one popover, by construction.

   RULES ENACTED HERE:
     ds-027    SOLID TWO-STATE. Colour is close-vs-open and NOTHING else; both directions are
               FILLED. `data/delta/gain` (close ≥ open) · `data/delta/loss` (close < open), the
               tokens the RAG/delta workstream owns — consumed, never re-derived. The #96-D1 ①
               hollow-up shape channel is RETIRED and is not coming back through this partial.
     OHLC      a candle whose high is not the highest or whose low is not the lowest is not a
               candle, it is a typo. Validated per session, loudly, by name — the one clause
               only this type can enforce.
     s116-D1   RECEIPTED SUB-24. A 40-session body is ~8px wide at 580 and that is the density
               ds-027's standing rule asks for ("all these charts should be fully responsive");
               the body is a READ POINT, not a click target, the same posture Chart-scatter's
               markers carry. Not silently ignored — named.
     DV-D02    fit, never scale: every candle rides a `g[data-fx][data-x0]` that dv-behaviour
               TRANSLATES, so the wick stays 1px and the body stays its own width at every
               container width. Axis furniture rides data-fx/data-fx2/data-dx.
     DEF-003   entry motion is CSS: `.dv-animate g.dv-candle` fades on an authored
               animation-delay. No JS geometry animation, no scale physics.
     dv-017    every colour emitted is a var() token.

   ⚠ TWO CORE WORK-AROUNDS, both already precedented, both filed verbatim in
   knowledge/_tmp/260/candlestick.core-requests.md:

   1. OUR OWN DOMAIN, and OUR OWN FURNITURE. The core clamps `if (lo > 0) { lo = 0; }` after it
      calls `fn.domain` — that is dv-bar-009's zero baseline, which is right for a bar (whose
      LENGTH is the value) and catastrophic for a price series: a run from 90 to 108 drawn
      against a zero floor is a 17%-tall smear at the top of the box. `fn.domain` cannot escape
      the clamp because the clamp runs after it. dv-render-line reported this and left it;
      dv-render-sparkline scaled to its own extent instead. A candlestick has no choice — so
      this partial computes its own nice scale off the series' own extent, discards the core's
      furniture (`ctx.out.length = 0`, the donut/sparkline work-around) and re-emits gridlines,
      tick labels and the baseline against the scale it actually drew.
   2. THE ACCESSIBLE NAME. `autoLabel` enumerates every series × category — 48 phrases for 40
      sessions — which is not a sentence anyone can listen to. ds-027's promised summary is the
      RANGE, the open and the close, so this partial writes it. `__dvLabel` marks the sentence
      as OURS: an author-supplied `label` survives, ours refreshes on every re-render. */
(function () {
  'use strict';
  if (!window.dvRender) { return; }   /* core absent — dvRender's own error is the loud one */
  var T = window.dvRender.types, U = window.dvRender.util;
  var n1 = U.n1, f4 = U.f4, esc = U.esc, nice = U.nice;

  var WANT = ['open', 'high', 'low', 'close'];
  var BODY = 0.62;    /* body width as a share of the session band — the promoted bake's 8.1/13.05 */
  var DOJI = 1.2;     /* a session that opened and closed flat still has to be visible ink */
  var STAGGER = 300;  /* ms across the whole series, so 40 sessions stagger like 12 do */

  function bad(msg) { throw new Error('dv-render-candlestick: ' + msg); }

  /* THE FOUR SERIES, BY NAME AND IN ORDER. Positional-only would let a build hand over
     high/low/open/close and get a chart that is wrong in a way nothing can see. */
  function ohlc(ctx) {
    if (ctx.series.length !== 4) {
      bad('OHLC is FOUR series — open, high, low, close, in that order. Got ' +
        ctx.series.length + ': ' + ctx.series.map(function (s) { return s.name; }).join(', '));
    }
    var out = {}, i;
    for (i = 0; i < 4; i++) {
      var got = String(ctx.series[i].name).trim().toLowerCase();
      if (got !== WANT[i]) {
        bad('spec.series[' + i + '].name is "' + ctx.series[i].name + '" — position ' + i +
          ' of a candlestick spec is "' + WANT[i] + '" (open, high, low, close, in that order)');
      }
      out[WANT[i]] = ctx.series[i].values;
    }
    for (i = 0; i < ctx.cats.length; i++) {
      var o = out.open[i], h = out.high[i], l = out.low[i], c = out.close[i];
      if (h < o || h < c || h < l) {
        bad('"' + ctx.cats[i] + '" has high ' + h + ' below open ' + o + ' / close ' + c +
          ' / low ' + l + ' — the HIGH is the session\'s highest price, always');
      }
      if (l > o || l > c) {
        bad('"' + ctx.cats[i] + '" has low ' + l + ' above open ' + o + ' / close ' + c +
          ' — the LOW is the session\'s lowest price, always');
      }
    }
    return out;
  }

  function candlestick(ctx) {
    ctx.out.length = 0;                 /* ⚠ the core's zero-floored furniture — see the header */

    var S = ohlc(ctx), n = ctx.cats.length, i;
    if (n < 1) { bad('a price series needs at least one session'); }

    /* OUR OWN SCALE — the series' own extent, nice-stepped by the core's own routine so the
       ticks read the way every other chart's do. NOT floored at zero: see the header. */
    var lo = Infinity, hi = -Infinity;
    for (i = 0; i < n; i++) {
      if (S.low[i] < lo) { lo = S.low[i]; }
      if (S.high[i] > hi) { hi = S.high[i]; }
    }
    if (hi === lo) { lo -= 1; hi += 1; }        /* a genuinely flat run centres, never /0 */
    var sc = nice(lo, hi, 4), span = sc.max - sc.min;
    var Y = function (v) { return ctx.y0 - (v - sc.min) / span * ctx.plotH; };

    /* FURNITURE, re-emitted against the scale actually drawn — the core's grammar verbatim
       (gridline data-fx/data-fx2, tick label data-fx="0"+data-dx, baseline in --baseline). */
    for (i = 0; i < sc.ticks.length; i++) {
      var ty = Y(sc.ticks[i]);
      ctx.push('<line class="dv-grid" x1="' + n1(ctx.PL) + '" y1="' + n1(ty) + '" x2="' +
        n1(ctx.PL + ctx.plotW) + '" y2="' + n1(ty) +
        '" stroke="var(--data-grid)" data-fx="0" data-fx2="1"/>');
      ctx.push('<text class="dv-axis t-cm-chart-value" fill="var(--data-axis)" x="' +
        n1(ctx.PL - 8) + '" y="' + n1(ty + 3) + '" text-anchor="end" data-fx="0" data-dx="-8" ' +
        'data-dy="3">' + esc(ctx.fmt(sc.ticks[i])) + '</text>');
    }
    ctx.push('<line class="dv-axis" x1="' + n1(ctx.PL) + '" y1="' + n1(ctx.y0) + '" x2="' +
      n1(ctx.PL + ctx.plotW) + '" y2="' + n1(ctx.y0) +
      '" stroke="var(--baseline)" data-fx="0" data-fx2="1"/>');

    /* THE CANDLES. One <g> per session carrying data-fx (fractional centre) + data-x0 (the baked
       centre): dv-behaviour translates the group, so nothing inside it is ever re-scaled. */
    var band = ctx.plotW / n, bw = band * BODY;
    if (bw < 1) { bw = 1; }
    for (i = 0; i < n; i++) {
      var o = S.open[i], h = S.high[i], l = S.low[i], c = S.close[i];
      var cx = ctx.PL + (i + 0.5) * band, up = c >= o;
      var top = Y(Math.max(o, c)), bh = Math.abs(Y(o) - Y(c));
      if (bh < DOJI) { bh = DOJI; }             /* a doji is still a session, and still ink */
      var words = ctx.cats[i] + ': open ' + ctx.fmt(o) + ', high ' + ctx.fmt(h) +
        ', low ' + ctx.fmt(l) + ', close ' + ctx.fmt(c);
      ctx.push('<g class="dv-candle" data-fx="' + f4((i + 0.5) / n) + '" data-x0="' + n1(cx) +
        '" style="animation-delay:' + Math.round(i * STAGGER / n) + 'ms">' +
        '<line class="dv-wick" x1="' + n1(cx) + '" y1="' + n1(Y(h)) + '" x2="' + n1(cx) +
        '" y2="' + n1(Y(l)) + '"></line>' +
        /* ds-027 — SOLID both ways; the class carries the state and the fill attribute carries
           the same token, so the dataviz gate can read a colour it would otherwise never see. */
        '<rect class="dv-body dv-series ' + (up ? 'dv-up' : 'dv-down') + '" data-series-i="' +
        (up ? 1 : 2) + '" fill="var(--data-delta-' + (up ? 'gain' : 'loss') + ')" x="' +
        n1(cx - bw / 2) + '" y="' + n1(top) + '" width="' + n1(bw) + '" height="' + n1(bh) +
        '" tabindex="0" role="img" aria-label="' + esc(words) + '" data-tip="' + esc(words) +
        '"></rect></g>');
    }

    /* PERIOD LABELS. Forty ticks would collide into a grey smear, so past a dozen sessions only
       the FIRST and LAST are drawn — the promoted bake's own answer, and the table is the rest. */
    for (i = 0; i < n; i++) {
      if (n > 12 && i !== 0 && i !== n - 1) { continue; }
      var lx = ctx.PL + (i + 0.5) * band;
      ctx.push('<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" x="' + n1(lx) +
        '" y="' + n1(ctx.y0 + 16) + '" text-anchor="middle" data-fx="' + f4((i + 0.5) / n) +
        '">' + esc(ctx.cats[i]) + '</text>');
    }

    /* ds-027's promised summary, not a 48-phrase enumeration — see the header. */
    if (ctx.spec.label === undefined || ctx.spec.__dvLabel) {
      ctx.spec.label = (ctx.spec.caption || 'Price') + '. Ranges from a low of ' + ctx.fmt(lo) +
        ' to a high of ' + ctx.fmt(hi) + ', opening ' + ctx.fmt(S.open[0]) + ' and closing ' +
        ctx.fmt(S.close[n - 1]) + ' across ' + n + ' session' + (n === 1 ? '' : 's') + '.';
      ctx.spec.__dvLabel = true;
    }
  }

  candlestick.axis = 'y';   /* value runs UP, sessions along x — the cartesian default */
  T.candlestick = candlestick;
}());
