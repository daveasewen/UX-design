---
name: gate-blindspot-state-contrast
description: "Failure mode — a 9/9 prototype-grade score gave false confidence; the contrast gate only checks AUTHOR-DECLARED pairs, so undeclared state×theme combos (dark hover, pressed) hid real a11y defects"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 452a0a17-6e63-4feb-ad8c-b23dfebbbd1b
---

**SPOTTED 2026-06-22 (Dave), on Cards.** Cards scored 9.0/9 several times while carrying real, visible accessibility defects — and they ALL hid in state×theme combinations the snippet never DECLARED: dark **hover** (text/secondary 3.34:1, red arrow 1.78:1 on #474747) and **pressed** (description 1.67:1, arrow 1.15:1, a dark icon on #767676). Only manual visual review — specifically in dark mode + the pressed state — caught them.

**Root cause:** the scorer measures PROXIES, not the rendered result. It checks signal PRESENCE (a `:focus-visible` exists; ≥4 state selectors) and the contrast of HAND-DECLARED pairs only. Undeclared state×theme pairs are blind spots, and purely semantic/visual quality (a heading that should be a link; type weight too thin in Chrome) isn't scored at all. So **9/9 ≠ done — it means "passed the automatable checks."** The rising score created false confidence.

**Why:** verification was opt-in (you only get checked on what you declare), and the gate never rendered the actual states.

**Fix — BUILT 2026-06-22: `knowledge/_validate_state_contrast.py`.** Renders each snippet light+dark, drives REAL hover/pressed per interactive element, measures computed foreground vs effective (composited) background. TEXT < 4.5/3.0 FAILS; svg icons WARN; disabled + `.demo-controls` excluded; transitions disabled during measurement (a mid-transition frame gave a false 1.06 — must kill transitions). Writes `_STATE-CONTRAST-AUDIT.md`. ~3s/snippet.
- Validated: ✅ clean on Cards/Modals/Tabs; correctly CATCHES List-items' parked dark-hover 3.34:1 — i.e. it finds the real issues the declared-pairs gate missed.
- DevTools `CSS.forcePseudoState` was tried first and is unreliable (applies the forced colour but NOT the forced background) — use real hover.
- LIMITATION: depends on the headless-Chromium setup ([[sandbox-html-rendering]]), which is SESSION-SPECIFIC (libXdamage extract etc.), so it does NOT run inside the lightweight `_build_all.py`. Use it as a per-component **promotion gate** (run on the component before promoting; would've blocked Cards until fixed).
- DARK-HOVER FIX DONE (2026-06-22): `tertiary/background/hover` dark #474747 → **#212121** (color/grey/dark-mode/500) — #474747 was too light (text/secondary 3.34:1, brand red 1.78:1). Updated the 12 snippets that bind it; build green; the gate re-verified List-items / Quick-actions / Reorder / Accordion now CLEAN. **The parked List-items $darkFinding is resolved.**
- BOARD-WIDE HARD GATE now only pending: bake the headless-Chromium render env into the build/CI so the gate can run for everyone (the contrast side is fixed).

**FIRST FULL SWEEP RAN 2026-07-03** (render path revived: libXdamage user-space +
skip-validate, see [[sandbox-html-rendering]] + `_ROBUSTNESS-PORTABILITY.md`; run in
13 batches — background jobs die-with-parent, /tmp is per-call). All 38 snippets:
**one REAL catch** — Selection-controls label 4.02:1 light hover/pressed on the same
'Accept terms & conditions' row copy-022 flagged (ONE component touch, Dave's eyes) —
and **one GATE BUG**: View-options 'List' measured 1:1/1.33:1 but screenshot-verified
LEGIBLE (black pill + white text); the effective-background walk misses the
absolutely-positioned sliding indicator. Docket: z-layer-aware background resolver;
check why Tab-bar B (same mechanism) passed. 20 icon warns = known judgment class.

**Also reframe the score:** 9/9 = "automatable checks passed", NOT done; human visual review stays the backstop for semantic/aesthetic judgement.

Relates to [[procedural-debt-and-method]] (verification = enforcement) and [[component-review-program]]. Distinct from, but compounding with, the AT band-aid debt + the dark-hover-token finding (both logged in `_RUBRIC-prototype-grade.md`).
