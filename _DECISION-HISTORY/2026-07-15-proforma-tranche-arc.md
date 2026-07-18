# Pro-forma tranche arc T1–T7 (2026-07-14/15)

> STANDING: decision-history file — provenance record, never edited after landing.
> **Relocated VERBATIM from `_LIVE-STATE.md` (lines 153–181) on 2026-07-18**, per the ruled
> consolidation (`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`). Spine summary: `_LIVE-STATE.md` → LIVE pro-forma programme.


---

- **Component library = Apollo pro-forma programme** (STARTED 2026-07-14, in flight). Building the
  *whole* inventory as a lightly-styled **pro-forma** (generate → iterate; styling cascades via
  tokens), then expressing it in MODES: Mode 1 = current HSBC brand (KB tokens as-is); Mode 2 = a new
  **business-line "big sister"** (rounded corners, monochrome, usability-first — colour only where
  meaningful, own type stack + DataViz), captured as a divergence **token mode**, never canon edits.
  ONE component skeleton, N modes — the cascade IS the proof of the factory. Chose **A** (KB-as-base;
  binds by intent so a neutral sub-floor can slide under later). Correctness = a **scramble-test** idea
  (wrong token values → anything that doesn't move is hardcoded). Reviewable build list =
  `reviews/ITINERARY-2026-07-14-apollo-component-library.{html,xlsx}` (124 items: 38 gated / 7 partial /
  79 gaps; 23 P1). IN FLIGHT: proof batch of 6 net-new **atomic** foundations (Icon button, Empty
  state, Skeleton loader, Amount/currency input, Stepper, Drawer) through the gated pipeline to
  validate the pro-forma contract + factory struct-mode. Memory `apollo-component-library-itinerary`. **UPDATE 07-14 eve — TRANCHE 1 DONE** (all 6 as one interactive MONOCHROME file `knowledge/_proforma/Tranche-1-interactive.html`; near-black primary, colour=meaning, real HSBC icons ENFORCED via `_check_proforma.py`; `_PROFORMA-RULES.md` living; artifact `apollo-proforma-tranche-1`). LESSON: a new surface needs its gate wired. Full: [[proforma-programme]].
  **UPDATE 2026-07-15 — library NAMED "Apollo mono" + Tranches 1–7 all built & gated.** Dave named this monochrome
  base **Apollo mono** (unbranded user-testing + Figma target), one of a THREE-library taxonomy governed by MODES:
  **Apollo mono** (here) · **Apollo UI** (new branded, varying radii) · **Apollo SC** (prior branded — "keep the ideas,
  don't copy the solutions"). **FOUNDATIONAL RULING (Dave):** *"we shouldn't hard code any styling going forward, must be
  tokenised and all the sibling libraries should be governed by modes — very flexible and future-proof."* Now enforced.
  **T6 (text entry & forms)** built + review-fixed with Dave (border-as-state-channel; uniform 51px field height every state;
  real error triangle; no size/layout jumps). **T7 (navigation)** built from a deep-research nav catalog
  (`reviews/NAV-PATTERN-CATALOG-2026-07-15.html` + artifact) — Popover/NavToggle · GlobalHeader · SideNav · MegaMenu
  (cols/featured/tabbed) · Drawer+NavAccordion; disclosure a11y spine; artifact `apollo-tranche-7-navigation`.
  **FULLY TOKENISED** (colour · motion via CSS scale tokens, JS motion removed incl. snippet canon · spacing `--space-*` ·
  border `--bw-sm/md/lg/1_5` · radius mode-token). **FOUR gates in `_build_all.py`:** universal `_validate_proforma.py` ·
  **DEF-003** `_validate_css_governed.py` (no JS motion) · **DEF-004** `_validate_no_hardcode.py` (no raw px in
  spacing/border/radius — caught real 1.5px leaks). DEF taxonomy 001 state-cluster / 002 glyph / 003 motion / 004 styling.
  **SCHEDULED TARGET (blocked on Dave's Figma):** type-token system = 3 responsive scales × 9 sizes + line-heights, 4px-grid →
  2 labelling-style sets (editorial + UI); same Figma file carries new colour tokens for all 3 modes; restore placeholder
  leading-trim (fixes off-grid 51px field). NOTED: legacy-libraries build-out. NEXT = Tranche 8 (BottomTabBar · InPageNav ·
  FooterNav · RelatedLinks · Stepper) OR type-tokens on Figma arrival. Full: [[proforma-programme]], [[nav-pattern-catalog]], [[apollo-mono]].
