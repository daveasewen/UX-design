# Masthead build + six review rounds (2026-07-16)

> STANDING: decision-history file — provenance record, never edited after landing.
> **Relocated VERBATIM from `_LIVE-STATE.md` (lines 521–558) on 2026-07-18**, per the ruled
> consolidation (`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`). Spine summary: `_LIVE-STATE.md` → LIVE masthead line.
> **STATUS (Dave, 2026-07-18): shipped as an MLP** — iteration expected later, not a defect. This arc exists nowhere else in the repo; preserve whole.

---

- **🟢 BUILT + LIVE (2026-07-16) — unified Masthead shipped, all gates green.**
  `knowledge/_proforma/Masthead-interactive.html`: ONE `.masthead` driven by `data-mode`
  (`minimal/exposed/exposed-mega/trigger`) + modifiers (`data-prominence primary|index`, `data-affordance
  burger|menu-search`, `data-search/-account on|off`) + a **switch row** that reconfigures the one live
  instance across the **5 recipes** (`App-minimal · L1 exposed · L1 + mega · Trigger mega · Dashboard-index`).
  **Folds in + SUPERSEDES the T7 `gheader` + `mm-masthead` demos** (they can be retired from Tranche-7).
  CSS-only motion (mega grid-reveal), search-finesse working (bar search icon hides when the panel carries
  search), priority+ → hamburger→modal-drawer responsive, disclosure a11y (aria-expanded/controls, ink
  underbar current, Esc-return, focus-trapped drawer). **All 4 pro-forma gates PASS + full `_build_all.py`
  (24 steps) green**; render-verified all 5 recipes + responsive, 0 console errors. Labels as signed off
  (D1 kept provisional · D2 Shell + optional footer → T8 · D3 recipe names). Docs: model dossier
  `reviews/MASTHEAD-MODEL-2026-07-16.html` + KB `_MASTHEAD-MODEL.md` (rule 16 pair); component review copy
  `knowledge/_review/Masthead-interactive-REVIEW.html`. **REVIEW ROUND 1 APPLIED (Dave, 2026-07-16):**
  dropped App-minimal (responsive covers it; app builds get their own components later) + the axis controls;
  merged Dashboard-index → **Trigger mega** (now 3 recipes: L1 exposed · L1 + mega · Trigger mega); trigger +
  account moved to the RIGHT; bar search + narrow hamburger now collapse into ONE drawn **combined
  menu-search glyph** (`i-menu-search`, flagged `provisional`/`bespoke`, logged to `_ICON-GAPS.md` — replace
  with a real HSBC asset later); removed the "All products" button (exposed-mega L1 links open the mega
  themselves); frame is bottom-border-only + account dropdown no longer clipped. All 4 gates + full
  `_build_all.py` still green; re-rendered all 3 recipes + narrow, 0 errors. **REVIEW ROUND 2 APPLIED
  (Dave, 2026-07-16):** (a) **bow+arrow brand mark** (`i-brand-apollo`, provisional/bespoke — Apollo the archer);
  (b) desktop trigger shows **separate menu + search** icons that **combine into the one menu-search glyph on
  mobile**; (c) **NEW drill-down side-nav drawer variant** (`.drawer.drilldown` — horizontal push nav, each
  submenu a full panel with title + back button, reflecting the mega IA; modal focus-trap scoped to the active
  level via `inert`; CSS-only slide) opened by the mobile combined glyph — the simple `.navacc` accordion
  variant is RETAINED in Tranche 7 (Dave: keep both); (d) masthead **underline** moved to `.masthead-bar` so it
  shows in every mode. 2 provisional glyphs logged to `_ICON-GAPS.md`. All 4 gates + full board green; rendered
  desktop/narrow/drill-down push+back, 0 errors.
  **REVIEW COMPLETE (Dave, 2026-07-16 — "done at last") after ~6 rounds.** Final state: **3 recipes**
  (App-minimal + the axis controls dropped; Dashboard-index merged into Trigger mega); **brand = extreme
  crescent** `i-brand-apollo` (provisional; picked from a 2-option render — bow-arrow & moon-craters rejected);
  desktop = separate menu+search, **combine into one menu-search glyph on mobile → drill-down drawer**; search
  finesse tied to **mega-open state** (bar search present, goes TRANSPARENT — not display:none, so no jump —
  when the mega is invoked); mega search = white bg + clear-on-active; masthead **underbar on `.masthead-bar`**;
  nav labels **wrapped in `<span>`** so leading-trim applies inside the flex `<a>` (memory
  `leading-trim-label-decision` gotcha #4); **all-caps purged** (`.dd-group-h`); brand icon↔wordmark gap 4px.
  Provisional icons `i-brand-apollo` (crescent) + `i-menu-search` await real assets (`_ICON-GAPS.md`).
  **NEXT** = Tranche 8 (+ Shell/footer template tier) or the type-token system on Figma arrival.
