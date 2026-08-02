/* dv-legend — the LEGEND INTERACTION MODEL (DV-D11 · DV-D13), hand-authored SOURCE.
   The SECOND registered behaviour source for the dataviz group: dv-behaviour.js carries
   fit/tip/table/seg/csv, this file carries the legend. Injected into registered chart snippets
   between AUTO-BEHAVIOUR dv-legend markers by gen_component_partials.py — edit HERE and
   regenerate, never between a consumer's markers.

   WHY A SECOND SOURCE (Dave ruled 2026-07-26, ADR-0015 §4 amended): this model is ~14KB and
   dv-behaviour.js already sat at 15.5KB of the 16KB per-source cap. The split came WITH a
   re-scoped gate — a per-PAGE sum budget — so the cap stayed a page constraint instead of
   silently becoming a per-file one.

   ⛔ DV-D12 (the donut radial sweep) LIVES NEXT DOOR in canon/dv-donut-sweep.js as of
   2026-08-02 (#76-D1, Dave) — this file was 651 B over the ADR-0015 per-source cap. Do NOT
   re-merge it: the seam is DV-D12's own (zero references to the interaction model), and the
   group's 32 KB page budget means merging back buys nothing and re-breaks the per-source cap.

   Reference implementation: reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html.
   The models are inscribed in _proforma/_DATAVIZ-DECISIONS.md — this file ENACTS them and does
   not restate the arc. Source contract still binds per ADR-0015: no polling/network, DELEGATED
   events (no per-row listeners), progressive enhancement — the baked SVG renders if this never
   runs — and the DEF-003 boundary (no JS scale-physics). */
(function () {
  'use strict';
  if (window.__dvLegend) { return; } window.__dvLegend = true;

  var GHOST = 'is-ghost', FADE = 'is-faded', PEEK = 'is-peek';

  /* ---------- STATE — one record per legend, parked on the host element. Delegated listeners
     resolve host → record, so no per-row listener ever exists (the ADR-0015 events clause). */
  function rec(host) {
    if (host.__dv) { return host.__dv; }
    var rows = [].slice.call(host.querySelectorAll('.dv-legrow'));
    var st = {
      host: host, fig: host.closest('figure') || document, rows: rows,
      ids: rows.map(function (r) { return r.getAttribute('data-series'); }),
      visible: {}, isolated: null, focus: null, lastHi: null, vals: null, total: 0,
      /* ★ DV-D19 — the MODE is LATCHED, never derived. See isSolo(). */
      mode: 'rest',
      live: document.getElementById(String(host.id).replace('-legend', '-live')),
      reset: host.querySelector('.dv-leg-reset')
    };
    st.ids.forEach(function (id) { st.visible[id] = true; });
    centreData(st);
    host.__dv = st;
    return st;
  }
  function series(st, id) { return st.fig.querySelectorAll('[data-series-group="' + id + '"]'); }
  /* ★ DV-D19 — 'rest' reads visible[]; BOTH focus modes read the focus set, so moving from
     isolate to check does not move a single mark. Nothing jumps: the focus set BECOMES the
     checked set (Dave refused reverting to the pre-isolation mix). */
  function active(st) { return st.mode === 'rest' ? st.visible : st.focus; }
  /* ★ DV-D19 (Dave, #75; enacted #76) — ISOLATION AND CHECK ARE MODES, NEVER SIMULTANEOUS.
     Verbatim: "as soon as the user checks a swatch the whole set change to check mode.
     check-mode and isolation-mode never occur at the same time."
     ⛔ WHAT WAS BROKEN WAS THE RETURN PATH, NOT THE TWO STATES. DV-D18 rightly de-seeded the
     marker and derived it from set size — but a DERIVED predicate can become true AGAIN:
     `isolate D -> check E -> uncheck E` put count(focus) back to 1, so D's emphasis returned
     while the user was plainly in check mode. * A PREDICATE CAN BECOME TRUE AGAIN; A MODE CANNOT.
     => emphasis is now a read of a LATCHED mode. DV-D19 REFINES DV-D18, it does not reverse it:
     the additive focus set (DV-D11/DV-D18) is untouched, and DV-D17's original complaint — "the
     isolated key item stays active when I check others on" — is still answered, now by a latch
     that cannot un-latch rather than by a count that can.
     ANTI-FALSE-FIX: do NOT restore `count(st, st.focus) === 1` here. It reads EQUIVALENT on the
     first two clicks of every sequence and diverges only on the RETURN — the one path Dave
     reported. The mutation test re-enacts exactly that. */
  function isSolo(st, id) { return st.mode === 'isolate' && !!st.focus && !!st.focus[id]; }
  function count(st, m) { var n = 0; st.ids.forEach(function (id) { if (m[id]) { n++; } }); return n; }
  function nameOf(st, id) {
    var el = st.host.querySelector('.dv-legrow[data-series="' + id + '"] .dv-leg-name');
    return el ? el.textContent : id;
  }
  function announce(st, msg) { if (st.live) { st.live.textContent = msg; } }

  /* ---------- DV-D13 — the centre figure follows the SELECTION. Values parse ONCE from each
     series' data-tip-value (LAST number in the string, so a series name may carry digits);
     percent = the active sum's share of the GRAND total. No-ops where a figure has no centre
     readout, so the one source serves donut, bar and combo alike. */
  function centreData(st) {
    if (!st.fig.querySelector('[data-dv-view="value"] .dv-val')) { return; }
    var vals = {}, n = 0;
    st.ids.forEach(function (id) {
      var el = st.fig.querySelector('.dv-series[data-series-group="' + id + '"]');
      var raw = el && el.getAttribute('data-tip-value');
      var all = raw && raw.match(/\d[\d,]*(?:\.\d+)?/g);
      if (all) { vals[id] = parseFloat(all[all.length - 1].replace(/,/g, '')); n++; }
    });
    if (n !== st.ids.length) { return; }
    st.vals = vals;
    st.ids.forEach(function (id) { st.total += vals[id]; });
  }
  function updateCentre(st) {
    if (!st.vals || !st.total) { return; }
    var m = active(st), sum = 0;
    st.ids.forEach(function (id) { if (m[id]) { sum += st.vals[id]; } });
    var v = st.fig.querySelector('[data-dv-view="value"] .dv-val');
    var p = st.fig.querySelector('[data-dv-view="percent"] .dv-val');
    if (v) { v.textContent = String(sum); }
    if (p) { p.textContent = Math.round(sum / st.total * 100) + '%'; }
  }

  /* ---------- DV-D11 — TWO render levels only: full · ghost(12%). Nothing ever fully
     disappears, so an unchecked series and an isolate-ghosted one are visually identical
     mid-chart; the legend row disambiguates. Opacity lives in CSS (decorative motion stays
     CSS); layout is preserved, so the chart never reflows under a toggle. */
  function paint(st, id, ghost) {
    var els = series(st, id);
    for (var i = 0; i < els.length; i++) {
      els[i].classList.toggle(GHOST, ghost);
      els[i].style.pointerEvents = ghost ? 'none' : '';
    }
  }
  function clearFade(st) {
    var f = st.fig.querySelectorAll('.' + FADE + ', .' + PEEK);
    for (var i = 0; i < f.length; i++) { f[i].classList.remove(FADE); f[i].classList.remove(PEEK); }
    st.lastHi = null;
  }
  /* Hover fires in BOTH modes: hovering an ACTIVE row fades the other actives to 24% (ghosts
     stay at 12%); hovering a GHOSTED row PEEKS it at 24% — a preview of what checking would do. */
  function highlight(st, id) {
    if (st.lastHi === id) { return; }
    clearFade(st);
    st.lastHi = id;
    var m = active(st), els, i;
    if (m[id]) {
      if (count(st, m) <= 1) { return; }
      st.ids.forEach(function (x) {
        if (!m[x] || x === id) { return; }
        var e = series(st, x);
        for (var j = 0; j < e.length; j++) { e[j].classList.add(FADE); }
      });
    } else {
      els = series(st, id);
      for (i = 0; i < els.length; i++) { els[i].classList.add(PEEK); }
    }
  }
  function render(st) {
    var m = active(st);
    st.rows.forEach(function (r) {
      var id = r.getAttribute('data-series'), solo = isSolo(st, id);
      var sw = r.querySelector('.dv-leg-sw'), it = r.querySelector('.dv-leg-item');
      /* in isolate the boxes show MEMBERSHIP of the focus set — blank until added (DV-D11) */
      if (sw) { sw.setAttribute('aria-checked', String(!!m[id])); }
      if (it) { it.setAttribute('aria-pressed', String(solo)); }
      r.classList.toggle('is-solo', solo);
    });
    st.ids.forEach(function (id) { paint(st, id, !m[id]); });
    if (st.reset) { st.reset.disabled = (count(st, st.visible) === st.ids.length && st.mode === 'rest'); }
    updateCentre(st);
    clearFade(st);
  }

  /* ---------- GESTURES. SWATCH = checkbox (show/hide) · LABEL = isolate. Isolate is a
     ONE-SERIES MODE the next swatch click ENDS (★ DV-D17; additive until 2026-07-27).
     visible[] is untouched while isolated, so release restores the prior mix by construction. */
  function toggleSwatch(st, id) {
    var m = active(st);
    /* ★ DV-D18 (Dave, 2026-08-01, #70) — THE ADDITIVE BRANCH IS BACK, and it is ONE path for
       both modes: while isolated `m` IS st.focus, so this grows and shrinks the focus SET;
       visible[] stays untouched, so release restores the prior mix by construction (DV-D17's
       bite (i) survives untouched). The stale-marker complaint DV-D17 was raised for is handled
       in isSolo() instead — the moment the set stops being a singleton, NO row reads solo.
       ⚠ DV-D17's release-on-add branch is DELETED, not commented: left in place it pre-empts
       this path on the very first click. Arc: _DATAVIZ-DECISIONS.md § Batch 10 + § ★ #70. */
    /* ★ DV-D19 — THE LATCH. A swatch click while isolated moves the WHOLE SET to check mode
       and it never returns. The set itself is untouched, so nothing jumps. */
    if (st.mode === 'isolate') { st.mode = 'check'; }
    if (m[id] && count(st, m) === 1) {
      announce(st, st.isolated ? 'At least one series must stay in the focus' : 'At least one series must stay shown');
      return;
    }
    m[id] = !m[id];
    announce(st, nameOf(st, id) + (st.isolated
      ? (m[id] ? ' added to the focus' : ' removed from the focus')
      : (m[id] ? ' shown' : ' dimmed')));
    render(st);
  }
  function isolate(st, id) {
    /* ★ DV-D19 — the gesture split, Dave's words: "clicking on the label is isolation-mode and
       clicking on the swatch is check-mode." A label re-click releases; any other label click
       ENTERS isolation, including out of check mode — which is how the user gets back. */
    /* ⚠ THE RELEASE TEST IS SEED-BASED AND STAYS SO — it is NOT gated on the mode. Gating it
       on `mode === 'isolate'` was tried at enactment and the member verifier refused it (check 22,
       4 members): after `isolate a -> check b`, the mode is 'check', so a re-click on `a` fell to
       the ELSE branch and RE-ISOLATED instead of releasing, destroying DV-D17 bite (i) — release
       restores visible[], not all-on. DV-D19 refines DV-D18; it reverses neither it nor DV-D17. */
    if (st.isolated === id) {
      st.mode = 'rest'; st.isolated = null; st.focus = null; announce(st, 'Isolation released');
    } else {
      st.mode = 'isolate'; st.isolated = id; st.focus = {}; st.focus[id] = true;
      announce(st, 'Showing only ' + nameOf(st, id) + ' — check a blank swatch to add a series');
    }
    render(st);
  }
  function resetAll(st) {
    st.mode = 'rest'; st.isolated = null; st.focus = null;
    st.ids.forEach(function (id) { st.visible[id] = true; });
    announce(st, 'All series shown');
    render(st);
  }

  /* ---------- DELEGATED EVENTS — document-level, resolved to a legend by closest('.dv-leg'). */
  function hostOf(el) { return el && el.closest ? el.closest('.dv-leg') : null; }
  document.addEventListener('click', function (e) {
    var t = e.target, host = hostOf(t);
    if (!host) { return; }
    var sw = t.closest('.dv-leg-sw');
    if (sw) { toggleSwatch(rec(host), sw.closest('.dv-legrow').getAttribute('data-series')); return; }
    var it = t.closest('.dv-leg-item');
    if (it) { isolate(rec(host), it.getAttribute('data-series')); return; }
    var rs = t.closest('.dv-leg-reset');
    if (rs && !rs.disabled) { resetAll(rec(host)); }
  });
  /* swatch keyboard: Space / Enter toggles the checkbox (it is a role=checkbox span, so the
     native button activation the label gets for free has to be supplied here). */
  document.addEventListener('keydown', function (e) {
    if (e.key !== ' ' && e.key !== 'Spacebar' && e.key !== 'Enter') { return; }
    var sw = e.target.closest && e.target.closest('.dv-leg-sw');
    var host = hostOf(sw);
    if (!sw || !host) { return; }
    e.preventDefault();
    toggleSwatch(rec(host), sw.closest('.dv-legrow').getAttribute('data-series'));
  });
  /* hover / focus preview — keyed off the whole ROW (either control) and off the marks
     themselves. pointerover/out delegate where mouseenter/leave cannot (they do not bubble);
     the lastHi guard makes the repeated child-to-child crossings idempotent. */
  function hiTarget(e) {
    var el = e.target.closest && e.target.closest('.dv-legrow, .dv-series[data-series-group]');
    if (!el) { return null; }
    var host = el.classList.contains('legrow') ? hostOf(el)
      : (el.closest('figure') || document).querySelector('.dv-leg');
    if (!host || !host.querySelector('.dv-legrow')) { return null; }
    return { st: rec(host), id: el.getAttribute('data-series') || el.getAttribute('data-series-group') };
  }
  document.addEventListener('pointerover', function (e) {
    var t = hiTarget(e); if (t) { highlight(t.st, t.id); }
  });
  document.addEventListener('pointerout', function (e) {
    var t = hiTarget(e);
    if (t && !(e.relatedTarget && e.relatedTarget.closest && hiTarget({ target: e.relatedTarget }))) {
      clearFade(t.st);
    }
  });
  document.addEventListener('focusin', function (e) {
    var t = hiTarget(e); if (t) { highlight(t.st, t.id); }
  });
  document.addEventListener('focusout', function (e) {
    var t = hiTarget(e); if (t) { clearFade(t.st); }
  });

  /* ---------- DV-D13 — the Value⇄Percent seg rewrites each mark's data-tip from
     data-tip-value / data-tip-percent, so the tip carries ONLY the selected number-type.
     dv-behaviour reads data-tip live at hover-time, so this needs no re-wire there.
     aria-labels deliberately keep BOTH forms: a screen-reader user should not lose data to a
     toggle they may never perceive (flagged in DV-D13, confirm at the a11y pass). */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('button[data-dv-view-btn]');
    if (!btn) { return; }
    var fig = btn.closest('figure'); if (!fig) { return; }
    var mode = btn.getAttribute('data-dv-view-btn');
    var els = fig.querySelectorAll('[data-tip-' + mode + ']');
    for (var i = 0; i < els.length; i++) {
      els[i].setAttribute('data-tip', els[i].getAttribute('data-tip-' + mode));
    }
  });

  /* ---------- INIT — discover every legend and render its resting state.
     Wrapped: a malformed legend must never take the baked SVG down with it. */
  try {
    var legs = document.querySelectorAll('.dv-leg');
    for (var i = 0; i < legs.length; i++) {
      if (legs[i].querySelector('.dv-legrow')) { render(rec(legs[i])); }
    }
  } catch (e) { /* leave the baked SVG intact */ }
}());
