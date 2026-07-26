/* dv-behaviour — the dataviz interaction layer (ADR-0015, hand-authored SOURCE).
   ONE file, injected into registered chart snippets between AUTO-BEHAVIOUR markers by
   gen_component_partials.py (registry: knowledge/component-types.json, group "dataviz").
   Edit HERE and regenerate — never between a consumer's markers.

   Modules: value POPOVER (dvTip) · responsive FIT reflow (DV-D02: text never scales) ·
   TABLE-VIEW POPOVER panel · LEGEND-AS-FILTER. Performance contract (GATED by
   _validate_behaviour.py): source ≤16KB raw · no setInterval/network/polling · ONE
   rAF-debounced resize listener · events DELEGATED (document-level, not per-element) ·
   progressive enhancement — every entry wrapped; the baked SVG renders if this never runs.
   DEF-003 boundary: behaviour + data-driven geometry ONLY — no JS scale-physics. */
(function () {
  'use strict';
  if (window.__dvBehaviour) { return; } window.__dvBehaviour = true;

  /* ---------- FIT — responsive width-compression (proforma fitCharts, ported).
     Only HORIZONTAL positions relayout to the container width; height + text are fixed.
     Geometry rides data-fx/data-fw/data-dx/data-x0/data-fx2 + polyline data-fxs/data-ys;
     plot frame per-svg via data-pl/data-pr/data-h (defaults = the kit's 46/12/260).
     JS-ON opt-in: .dv-fit-on lands on the figure, releasing the fixed-width CSS —
     JS-off keeps the DV-D02 static answer (fixed geometry + horizontal scroll). */
  function fitCharts() {
    var svgs = document.querySelectorAll('svg.dv-fit');
    for (var i = 0; i < svgs.length; i++) { fitOne(svgs[i]); }
  }
  function fitOne(svg) {
    try {
      var PL = parseFloat(svg.getAttribute('data-pl') || '46');
      var PR = parseFloat(svg.getAttribute('data-pr') || '12');
      var H  = parseFloat(svg.getAttribute('data-h')  || '260');
      var W = Math.round(svg.getBoundingClientRect().width);
      if (!W) { return; }
      var plotW = W - PL - PR; if (plotW < 90) { plotW = 90; }
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);   /* 1:1 pin — no proportional scaling */
      var X = function (f) { return PL + parseFloat(f) * plotW; };
      var els = svg.querySelectorAll('[data-fx]');
      for (var i = 0; i < els.length; i++) {
        var el = els[i], x = X(el.getAttribute('data-fx')), tag = el.tagName.toLowerCase();
        if (tag === 'rect') {
          el.setAttribute('x', x.toFixed(1));
          var fw = el.getAttribute('data-fw');
          if (fw !== null) { el.setAttribute('width', (parseFloat(fw) * plotW).toFixed(1)); }
        } else if (tag === 'text') {
          var dx = parseFloat(el.getAttribute('data-dx') || '0');
          el.setAttribute('x', (x + dx).toFixed(1));
        } else if (tag === 'line') {
          el.setAttribute('x1', x.toFixed(1));
          var fx2 = el.getAttribute('data-fx2');
          if (fx2 !== null) { el.setAttribute('x2', X(fx2).toFixed(1)); }
        } else if (tag === 'g') {
          var x0 = parseFloat(el.getAttribute('data-x0') || '0');
          el.setAttribute('transform', 'translate(' + (x - x0).toFixed(1) + ',0)');
        }
      }
      var pls = svg.querySelectorAll('polyline[data-fxs]');
      for (var j = 0; j < pls.length; j++) {
        var pl = pls[j];
        var fxs = pl.getAttribute('data-fxs').trim().split(/\s+/);
        var ys  = pl.getAttribute('data-ys').trim().split(/\s+/);
        var pts = [];
        for (var k = 0; k < fxs.length; k++) { pts.push(X(fxs[k]).toFixed(1) + ',' + ys[k]); }
        pl.setAttribute('points', pts.join(' '));
      }
    } catch (e) { /* leave the baked SVG intact */ }
  }
  var dvRAF;   /* the ONE resize listener, rAF-debounced (ADR-0015) */
  window.addEventListener('resize', function () {
    cancelAnimationFrame(dvRAF); dvRAF = requestAnimationFrame(function () { fitCharts(); placeSegs(); });
  });

  /* ---------- POPOVER — real value tip on hover AND keyboard focus of any [data-tip].
     Replaces native <title> tooltips (values stay in sync with the table — one source).
     Edge-flips at the viewport bounds. role=status/aria-live=polite (proforma posture). */
  var dvTip = document.createElement('div');
  dvTip.className = 'dv-tip t-cm-chart-value'; dvTip.id = 'dvTip';   /* type via composite (T-D14 markup class) */
  dvTip.setAttribute('role', 'status'); dvTip.setAttribute('aria-live', 'polite');
  document.body.appendChild(dvTip);
  function tipAt(text, x, y) {
    dvTip.textContent = text; dvTip.classList.add('on');
    var r = dvTip.getBoundingClientRect();
    if (x + r.width  > window.innerWidth  - 8) { x = x - r.width  - 28; }
    if (y + r.height > window.innerHeight - 8) { y = y - r.height - 28; }
    dvTip.style.left = x + 'px'; dvTip.style.top = y + 'px';
  }
  function tipHide() { dvTip.classList.remove('on'); }
  document.addEventListener('pointermove', function (e) {
    var el = e.target.closest && e.target.closest('[data-tip]');
    if (el) { tipAt(el.getAttribute('data-tip'), e.clientX + 14, e.clientY + 14); }
    else { tipHide(); }
  });
  document.addEventListener('focusin', function (e) {
    var el = e.target.closest && e.target.closest('[data-tip]');
    if (!el) { return; }
    var b = el.getBoundingClientRect();
    tipAt(el.getAttribute('data-tip'), b.left + b.width / 2, b.top - 40);
  });
  document.addEventListener('focusout', function () { tipHide(); });

  /* ---------- TABLE-VIEW POPOVER — floating card panel (Dave's mock, 2026-07-23:
     surface ground + border + soft shadow, NOT a frosted drawer). Toggle carries
     aria-controls + aria-expanded; panel is a labelled region, tabindex=-1 for the
     focus hand-off; Esc dismisses and returns focus to its toggle. */
  function tblToggle(btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) { return; }
    var open = panel.hasAttribute('hidden');           /* opening if currently hidden */
    if (open) {
      panel.removeAttribute('hidden');
      /* anchor the panel just BELOW its trigger, never over it — the fixed top was brittle
         once a title pushed the toolbar down (Dave 2026-07-24). Measure after un-hiding so
         offsetParent resolves; fall back gracefully. */
      var op = panel.offsetParent || btn.offsetParent || panel.parentNode;
      if (op) {
        var bt = btn.getBoundingClientRect(), ot = op.getBoundingClientRect();
        panel.style.top = (bt.bottom - ot.top + 6) + 'px';
        /* anchor horizontally UNDER the trigger too — right:0 pinned the panel to the figure's edge,
           wrong when the trigger sits mid-figure (e.g. donut + side legend). Left-align to the
           trigger, clamp so it never spills past the offsetParent's right edge (keeps bar/line right-anchored). */
        var lx = Math.max(0, Math.min(bt.left - ot.left, op.clientWidth - panel.offsetWidth));
        panel.style.left = lx + 'px'; panel.style.right = 'auto';
      }
    } else { panel.setAttribute('hidden', ''); }
    btn.setAttribute('aria-expanded', String(open));   /* label stays static; the solid arrow rotates via CSS (Dave 2026-07-24) */
    if (open) { panel.focus(); }
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('.dv-tbl-toggle');
    if (btn) { tblToggle(btn); return; }
    var vt = e.target.closest && e.target.closest('button[data-dv-toggle]');
    if (vt) { viewToggle(vt); return; }
    var sw = e.target.closest && e.target.closest('button[data-dv-view-btn]');
    if (sw) { segView(sw); return; }
    var cp = e.target.closest && e.target.closest('button.dv-csv');
    if (cp) { copyCsv(cp); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') { return; }
    var panel = e.target.closest && e.target.closest('.dv-tablepanel');
    if (!panel || panel.hasAttribute('hidden')) { return; }
    panel.setAttribute('hidden', '');
    var btn = document.querySelector('.dv-tbl-toggle[aria-controls="' + panel.id + '"]');
    if (btn) { btn.setAttribute('aria-expanded', 'false'); btn.focus(); }   /* label static (Dave 2026-07-24) */
  });

  /* ---------- LEGEND — ⚠ TRANSITIONAL, SUPERSEDED BY DV-D11. DELETE WHEN THE LAST MEMBER MIGRATES.
     The model below (hide-at-0%, shift-click isolate, .dv-quiet highlight) is DEAD as a design:
     DV-D11 replaced it with two render levels (full / ghost-12%, nothing ever disappears), a
     dual-gesture row (swatch=checkbox + label=isolate) and an ADDITIVE focus set. That model
     lives in `canon/dv-legend.js`, the group's second registered behaviour source.

     WHY THIS STILL EXISTS (Dave ruled incremental migration, 2026-07-26): the two models are
     SELECTOR-DISJOINT — this one keys on `button[data-series-toggle]`, dv-legend on
     `.dv-legrow`. A migrated snippet is served only by dv-legend and an unmigrated one only by
     this block: no overlap, no double-binding. The four legend-bearing members can migrate one
     at a time with every commit in a working state.

     END CONDITION — run `knowledge/_check_legend_migration.py` (exit 0 = delete this block; the
     page budget then falls to ~27.7KB). NOT the bare grep this comment used to name: that string
     is in this block's own source, injected into every member, so it matched all five snippets
     the day it was written — migrated donut included. Corrected lane ①, 2026-07-26.
     MIGRATED: Chart-donut · Chart-bar. REMAINING: Chart-combo · Chart-line.
     Do not extend or "improve" anything below — it is scheduled for deletion. */
  function setSeries(btn, show) {
    btn.setAttribute('aria-pressed', String(show));
    var fig = btn.closest('figure') || document;
    var els = fig.querySelectorAll('[data-series-group="' + btn.getAttribute('data-series-toggle') + '"]');
    for (var i = 0; i < els.length; i++) {
      els[i].style.opacity = show ? '' : '0';
      els[i].style.visibility = show ? '' : 'hidden';
      els[i].style.pointerEvents = show ? '' : 'none';
    }
  }
  function legendToggle(btn) { setSeries(btn, btn.getAttribute('aria-pressed') !== 'true'); }
  function isolate(btn) {
    var fig = btn.closest('figure') || document;
    var all = fig.querySelectorAll('button[data-series-toggle]');
    var solo = btn.getAttribute('aria-pressed') === 'true';
    for (var i = 0; i < all.length; i++) {
      if (all[i] !== btn && all[i].getAttribute('aria-pressed') === 'true') { solo = false; }
    }
    for (var j = 0; j < all.length; j++) { setSeries(all[j], solo ? true : all[j] === btn); }
  }
  function setQuiet(fig, group) {
    var els = fig.querySelectorAll('[data-series-group]');
    for (var i = 0; i < els.length; i++) {
      els[i].classList.toggle('dv-quiet', group !== null && els[i].getAttribute('data-series-group') !== group);
    }
  }
  function hlTarget(e) {
    var el = e.target.closest && e.target.closest('.dv-legbtn[data-series-toggle], .dv-marker[data-series-group]');
    if (!el) { return null; }
    return { fig: el.closest('figure') || document,
             group: el.getAttribute('data-series-toggle') || el.getAttribute('data-series-group') };
  }
  document.addEventListener('pointerover', function (e) {
    var t = hlTarget(e); if (t) { setQuiet(t.fig, t.group); }
  });
  document.addEventListener('pointerout', function (e) {
    var t = hlTarget(e); if (t) { setQuiet(t.fig, null); }
  });
  document.addEventListener('dblclick', function (e) {
    var leg = e.target.closest && e.target.closest('button[data-series-toggle]');
    if (leg) { isolate(leg); }
  });
  document.addEventListener('click', function (e) {
    var leg = e.target.closest && e.target.closest('button[data-series-toggle]');
    if (leg) { if (e.shiftKey) { isolate(leg); } else { legendToggle(leg); } }
  });
  /* ---------- end TRANSITIONAL legend block ---------- */

  /* VIEW TOGGLES (menu picks 6/7/9): baked-variant switching — geometry is generated, never
     computed here; behaviour only shows/hides [data-dv-view] groups (.dv-off = display:none). */
  function setView(fig, name, show) {
    var els = fig.querySelectorAll('[data-dv-view~="' + name + '"]');
    for (var i = 0; i < els.length; i++) { els[i].classList.toggle('dv-off', !show); }
  }
  function viewToggle(btn) {
    var on = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', String(!on));
    setView(btn.closest('figure') || document, btn.getAttribute('data-dv-toggle'), !on);
  }
  /* SEGMENTED INDICATOR (Dave, 2026-07-24): the view switch CONSUMES the Segmented-control atom —
     behaviour drives the sliding fill (.ind) the atom's way: measure the pressed button's box and
     slide. rect-based so the 2px inset + 1px border don't offset the measurement (the .ind
     containing block is .seg's padding box — subtract seg.clientLeft). */
  function moveSeg(seg) {
    if (!seg) { return; }
    var ind = seg.querySelector('.ind'); if (!ind) { return; }
    var a = seg.querySelector('button[aria-pressed="true"]'); if (!a) { return; }
    var sr = seg.getBoundingClientRect(), br = a.getBoundingClientRect();
    ind.style.left = (br.left - sr.left - seg.clientLeft) + 'px';
    ind.style.width = br.width + 'px';
  }
  function placeSegs() {
    var segs = document.querySelectorAll('.seg');
    for (var i = 0; i < segs.length; i++) { moveSeg(segs[i]); }
  }
  /* VIEW SWITCH (Dave, 2026-07-23, both messages read together): the scale pair (monthly ⇄ year
     to date) is EXCLUSIVE — two scales can't share a canvas — but the overlays are fully ADDITIVE:
     each view carries its OWN baked variant of every overlay (nested [data-dv-view] groups), and
     an overlay's toggle governs both copies, so it works in whichever view is up. Nothing ever
     disables. */
  function segView(btn) {
    if (btn.getAttribute('aria-pressed') === 'true') { return; }
    var fig = btn.closest('figure') || document;
    var active = btn.getAttribute('data-dv-view-btn');
    var segs = fig.querySelectorAll('button[data-dv-view-btn]');
    for (var i = 0; i < segs.length; i++) {
      var v = segs[i].getAttribute('data-dv-view-btn');
      segs[i].setAttribute('aria-pressed', String(v === active));
      setView(fig, v, v === active);
    }
    moveSeg(btn.closest('.seg'));                 /* slide the indicator to the newly active view */
  }
  /* COPY CSV (menu pick 10): the figure's real table, serialised — no network, table = truth. */
  function copyCsv(btn) {
    var fig = btn.closest('figure') || document;
    var rows = fig.querySelectorAll('table tr');
    var out = [];
    for (var i = 0; i < rows.length; i++) {
      var cells = rows[i].querySelectorAll('th,td'), line = [];
      for (var j = 0; j < cells.length; j++) { line.push('"' + cells[j].textContent.trim().replace(/"/g, '""') + '"'); }
      out.push(line.join(','));
    }
    var csv = out.join('\n');
    function done() {
      /* label stays put; the copy icon swaps to a tick briefly (Dave 2026-07-24) */
      btn.classList.add('is-copied');
      setTimeout(function () { btn.classList.remove('is-copied'); }, 1600);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(csv).then(done, done);
    } else { done(); }
  }

  /* ---------- INIT — opt the page into fit (JS-on releases the fixed width), first pass. */
  var figs = document.querySelectorAll('figure.dv');
  for (var i = 0; i < figs.length; i++) { figs[i].classList.add('dv-fit-on'); }
  fitCharts();
  placeSegs();                                    /* initial indicator position (widths depend on layout) */
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(placeSegs); }   /* re-place once the web font settles */
}());
