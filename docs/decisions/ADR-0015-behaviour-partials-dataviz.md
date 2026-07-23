# ADR-0015 — Behaviour partials: the dataviz interaction layer as generated JS

**Date:** 2026-07-23 · **Status:** accepted (Dave, in-chat, confirming the brief's Decision #1 recommendation: *"I think [that] was the decision initially — as long as the JS is light. I want this to be fast and responsive"*) · **Extends:** ADR-0013 (component-type tier — retrieval now reaches BEHAVIOUR, not only CSS rules) · **Relates:** DV-D07 (the two-channel chrome roles this behaviour styles against) · DEF-003 (CSS-governed-motion boundary, unchanged by this ADR)

## Context

The chart-revisit programme (brief 2026-07-23) lifts all five canon chart snippets to the proforma's
Layer-2: interactive value popover, responsive `fitCharts()` reflow, table-view popover,
legend-as-filter, optional title, full motion parity. The proforma proves all of it in **one shared
script — measured 2026-07-23: 9.9 KB raw / 3.2 KB gzipped for the entire kit.** Five snippets each
re-typing that script is the exact anti-pattern ADR-0013 closed for CSS: a shared rule living as
N diverging local copies. Option (b) (a `<script src>` shared module) was rejected because snippets
must stay **self-contained single-file artefacts**; option (c) (inline ×5) rejected per ADR-0013.

## Decision

1. **One source of truth.** The behaviour lives in ONE hand-authored source file (home:
   `knowledge/canon/dv-behaviour.js` — the `type.css` precedent: hand-authored, generator-consumed).
   Modules: popover (`dvTip`) · fit reflow · table-view popover · legend-filter · shared helpers.
2. **Generated injection.** The partials generator injects it into each registered chart snippet
   between `AUTO-BEHAVIOUR` markers with a provenance comment, exactly the ADR-0013 CSS contract:
   regenerate-always where cheap, `--check` sync gate in the build, fails loud, byte-exact.
   Snippets remain portable AFTER generation — the injected block travels with the file.
3. **One registry, both halves — same file.** Chart snippets register in
   `knowledge/component-types.json` (a `dataviz` group): members + the behaviour partial contract
   (markers present · required hooks · manifest binds). Contracts fire on registration (ADR-0013
   posture); the ratchet walks census → advisory → blocking as consumers migrate.
4. **Performance contract (Dave's constraint — GATED, not aspirational):**
   - **Size gate (blocking):** source ≤ **16 KB raw** (observed baseline 9.9 KB covers the full kit;
     the cap is headroom, not a target).
   - **Banned patterns (blocking):** `setInterval` · network calls (`fetch`/XHR) · external
     `<script src>` · DOM polling. Resize handling = a **single rAF-debounced listener**; events
     **delegated** at the figure root, not per-element.
   - **Progressive enhancement:** the baked SVG must render with JS off (the proforma's try/catch
     posture); behaviour only ever *adds*.
   - **DEF-003 boundary restated:** behaviour + data-driven geometry only — no JS scale-physics,
     no `--hs`/`--ps`, no `transform:scale` assignment.
5. **Decorative motion stays CSS** (draws, fades, grows). JS touches geometry only where data
   demands it (fit reflow, arc growth, popover position).

## Consequences

- The gate work rides the Chart-line exemplar build: size + pattern checks + sync `--check` +
  selftest, wired into `_build_all` (selftests-are-build-steps rule).
- The showroom needs no change: snippet `<script>` already executes inside pane payloads (the
  review-overlay precedent).
- Legend/toolbar controls become pressables with a **quiet utility state** — deliberately NOT
  B-D7 press physics (chart-revisit Q5; flagged to Dave, standing).
- When the theme builder arrives, behaviour joins the partial bin like everything else — one more
  organ the tool absorbs (see `_FUTURE-STATE` theme-generator entry).
