/* dv-donut-sweep — the DONUT RADIAL-SWEEP INTRO (DV-D12), hand-authored SOURCE.
   THIRD behaviour source for the dataviz group; split out of dv-legend.js 2026-08-02 (#76-D1,
   Dave) when that file hit 17,035 B against ADR-0015's 16 KB per-source cap. Cut along DV-D12's
   own seam: these three functions hold ZERO references to the legend interaction model.
   ⚠ The split buys NO headroom and the GATE enforces that, not this comment — the group's
   32 KB page budget sums every registered source (the 2026-07-26 re-scoping).

   ★ The motion law is SHARED with the stacked bar and only this half is built; they share a
   LAW, not an implementation. Full record: _DATAVIZ-DECISIONS.md § ★ #76 — not restated here.
   ⚠ ZERO resize listeners is CORRECT: that is a GROUP invariant, held by dv-behaviour.js. */
(function () {
  'use strict';
  if (window.__dvDonutSweep) { return; } window.__dvDonutSweep = true;

  /* ---------- DV-D12 — the donut radial-sweep intro. Trapezoidal angular-velocity profile
     keyed to the SEGMENT SPANS, not a global bezier: ease-IN across exactly the first
     segment's arc, LINEAR through the middle, ease-OUT across exactly the last's. Cruise
     V=(S+w1+wN)/dur makes accel+cruise+decel sum to dur. A long first segment therefore gives
     a long ramp BY DESIGN (Dave saw 147°/~441ms and signed off without a tune). */
  function pt(cx, cy, r, a) { var t = a * Math.PI / 180; return [cx + r * Math.cos(t), cy + r * Math.sin(t)]; }
  function arcPath(cx, cy, ro, ri, a1, a2) {
    var big = (a2 - a1) > 180 ? 1 : 0;
    var o1 = pt(cx, cy, ro, a1), o2 = pt(cx, cy, ro, a2), i2 = pt(cx, cy, ri, a2), i1 = pt(cx, cy, ri, a1);
    return 'M' + o1[0].toFixed(2) + ' ' + o1[1].toFixed(2) +
      ' A' + ro + ' ' + ro + ' 0 ' + big + ' 1 ' + o2[0].toFixed(2) + ' ' + o2[1].toFixed(2) +
      ' L' + i2[0].toFixed(2) + ' ' + i2[1].toFixed(2) +
      ' A' + ri + ' ' + ri + ' 0 ' + big + ' 0 ' + i1[0].toFixed(2) + ' ' + i1[1].toFixed(2) + ' Z';
  }
  function sweepDonut(fig) {
    var segs = [].slice.call(fig.querySelectorAll('path.dv-series[data-a1]'));
    if (!segs.length) { return; }
    var annos = [].slice.call(fig.querySelectorAll('.dv-anno'));
    var data = segs.map(function (el) {
      return { el: el, cx: +el.getAttribute('data-cx'), cy: +el.getAttribute('data-cy'),
        ro: +el.getAttribute('data-ro'), ri: +el.getAttribute('data-ri'),
        a1: +el.getAttribute('data-a1'), a2: +el.getAttribute('data-a2'),
        grp: el.getAttribute('data-series-group'), full: el.getAttribute('d') };
    });
    var start = Math.min.apply(null, data.map(function (d) { return d.a1; }));
    var end = Math.max.apply(null, data.map(function (d) { return d.a2; }));
    /* reduced motion: land on the final frame, never animate (the baked answer) */
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      data.forEach(function (d) { d.el.setAttribute('d', d.full); d.el.style.opacity = ''; });
      annos.forEach(function (a) { a.classList.add('show'); a.style.opacity = ''; });
      return;
    }
    annos.forEach(function (a) { a.classList.remove('show'); a.style.opacity = '0'; });
    data.forEach(function (d) { d.el.style.opacity = '1'; d.el.setAttribute('d', arcPath(d.cx, d.cy, d.ro, d.ri, d.a1, d.a1)); });
    var dur = 850, t0 = null;
    var S = end - start;
    var f1 = data.reduce(function (m, d) { return d.a1 < m.a1 ? d : m; }, data[0]);
    var fN = data.reduce(function (m, d) { return d.a2 > m.a2 ? d : m; }, data[0]);
    var w1 = f1.a2 - f1.a1, wN = fN.a2 - fN.a1;
    var mid = S > w1 + wN + 1e-6;                  /* needs an interior to hold constant speed */
    var V = (S + w1 + wN) / dur;                   /* cruise angular speed, deg/ms */
    var ta = 2 * w1 / V, td = 2 * wN / V, tc = (S - w1 - wN) / V;
    function angAt(t) {
      if (!mid) { var q = t / dur; q = q < 0.5 ? 2 * q * q : 1 - Math.pow(-2 * q + 2, 2) / 2; return start + S * q; }
      if (t <= ta) { return start + V * t * t / (2 * ta); }
      if (t <= ta + tc) { return start + w1 + V * (t - ta); }
      var tau = t - (ta + tc);
      return end - wN + V * tau - V * tau * tau / (2 * td);
    }
    function frame(ts) {
      if (t0 === null) { t0 = ts; }
      var t = Math.min(ts - t0, dur), ang = angAt(t);
      data.forEach(function (d) {
        if (ang <= d.a1) { d.el.setAttribute('d', arcPath(d.cx, d.cy, d.ro, d.ri, d.a1, d.a1)); }
        else if (ang >= d.a2) { d.el.setAttribute('d', d.full); }
        else { d.el.setAttribute('d', arcPath(d.cx, d.cy, d.ro, d.ri, d.a1, ang)); }
      });
      annos.forEach(function (a) {
        var g = a.getAttribute('data-series-group');
        var seg = data.filter(function (d) { return d.grp === g; })[0];
        if (seg && ang >= seg.a2) { a.classList.add('show'); a.style.opacity = ''; }
      });
      if (t < dur) { requestAnimationFrame(frame); }
      else {
        data.forEach(function (d) { d.el.setAttribute('d', d.full); d.el.style.opacity = ''; });
        annos.forEach(function (a) { a.classList.add('show'); a.style.opacity = ''; });
      }
    }
    requestAnimationFrame(frame);
  }

  /* ---------- INIT — run the sweep on every donut figure.
     Wrapped: a malformed figure must never take the baked SVG down with it. */
  try {
    var figs = document.querySelectorAll('figure.dv');
    for (var j = 0; j < figs.length; j++) { sweepDonut(figs[j]); }
  } catch (e) { /* leave the baked SVG intact */ }
}());
