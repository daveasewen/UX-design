# Findings index

One place for the findings scattered across meta `$finding`/`$darkNote` notes, the dark-mode audit,
and the deprecation report. Built 2026-06-20. The per-component detail still lives in each meta;
this is the map.

## 1. Dark-token reconciliations — DONE (gate-verified, mapped to primitives)
| Group | Defect | Fix |
|---|---|---|
| `form/*` | flat #FFFFFF in dark; `background/default` lost its alpha | grey/dark-mode primitives; alpha restored |
| `tabs/*`, `tertiary/*` | flat-white surfaces in dark | raised dark greys |
| 24-token surface sweep | borders/dividers/table/tooltip/scrollbar/timer/disabled flat-white | dark-mode greys; buttons (primary red / secondary inverts) |
| `progress/complete` + `incomplete` | BOTH #FFFFFF in dark (segments indistinguishable) | complete=#DB0011, incomplete=#404040 |
| `tooltip/background` | #FFFFFF both modes (white tooltip in dark) | dark=#1D1D1D |
| Slider handle, Modal surface (snippets) | bound to `background/default` → invisible on #000 | rebound to raised surface + visible border |
| 7 remaining whites | intentional inversions / active emphasis / on-light | annotated `$darkNote` (gate allowlist) |

**Audit conclusion (full store scan, 2026-06-20):** clean of real dark defects. Remaining flat-whites are
*foregrounds* (text/icon/neutral/scrollbar/timer fills) that correctly invert to white; flat-blacks are
page surfaces; 30 "identical both modes" are intentional (brand red, the mode-independent data-viz palette,
overlays). The `dark-surface` gate was tightened to also catch white-in-dark when light is white too.

## 2. Token gaps / DECISIONS for Dave
- **`text/secondary` token — ADDED 2026-06-20 (review-tagged, awaiting Dave's sign-off).** `#545454` light
  (grey/700, 7.6:1 on white) / `#9B9B9B` dark (grey/500, 7.6:1 on black) — both comfortably ≥4.5:1 and clearly
  dimmer than `text/default`. List items + Cards now bind their secondary text to it (was a literal grey).
  Same pass token-tracked the focus ring (`focus/ring`) in 5 snippets that used it but hadn't declared it
  (Avatar, Dropdown, Selection controls, Tags, Tooltip) — now gated. ACTION: confirm or adjust the two values.
- **`rag/warning` (#FFBB33)** is ~1.6:1 on white and on its tint — fails 1.4.11 as a standalone dot/accent.
  Meaning is carried by icon shape + text; acceptable, but a stand-alone warning dot needs an outline/icon.
- **`focus/ring`** — ✅ **SIGNED OFF as canon (Dave, 2026-06-20).** Promoted `review`→`asserted` in
  `semantic-colour.json` (focus/ring) + `layout.json` (focus/ring-width|offset); guideline status updated.
  No canonical Figma primitive exists; agreed standard stands until one is introduced.
- **Inverting label pattern** (`text/on-inverse` #FFF/#333) used by secondary Button, checked controls,
  View options, ghosted disabled — confirm as canon.
- **Tabs rewire** — the Tabs component still binds primitives/`tertiary/*`; `tabs/hover`+`tabs/pressed` now
  exist (fix #7) so it can rewire fully. Part of the Figma dark write-back (pending go-ahead).

## 3. Components flagged as BASELINES (need design review, not finished canon)
**Navigations** (masthead only — no logged-in/out, mega-menu, mobile/tab-bar), **Headers** (content+display;
other variants simplified), **Hero** (text-on-surface; on-image variant needs an image + scrim),
**Video player** (controls are literals — must hold contrast over any frame), **Table** (built 2026-06-20 —
semantic/tokens/contrast gated; sort affordance + small-screen reflow strategy need design review).
Coverage is now **32/32 real components** gated (Table was the last gap; EXAMPLE-button is a template).

## 4. Deprecated-binding migration backlog (parked for Sutherland)
Top clusters of deprecated bindings: Selection controls (13), Dropdown (9), Tags (9 — no `tag/*` group),
Hero (8), Button (7 — on-dark heavy), Pagination (7), Avatar (6), Navigations (6), Quick actions (6).
Recurring sets: `interactive(depricate)/on-light/surface/primary/*` (list/nav/quick-actions surfaces) and the
`active-surface` set (chip-selected / switch-on). 12 components are fully clean. Worklist = each meta's
`tokenValidation.depricateUsage` + `tokens/_manifests/`.

## 5. Tooling / canon changes this session
- `dark-surface` gate broadened (white-in-dark regardless of light; `on-dark` excluded).
- `tabs/hover` + `tabs/pressed` tokens added (fix #7).
- Angular rule operationalized in `guidelines/brand-principles.md` (fix #8: square corners; Badge+Avatar exempt).
- Tabs guideline mis-map fixed (fix #6: removed carousel `horizontal-scroll.md`).
- `text/secondary` token added + adopted (List items, Cards); focus ring token-tracked in 5 more snippets.
- **A11y gate added** (`_validate_a11y.py`, build step 10/11): reduced-motion required when a snippet
  animates (gating); sub-24px interactive targets reported. Full audit in `_A11Y-AUDIT.md`.
- A11y fixes applied: `prefers-reduced-motion` added to 28 snippets; 24×24 hit-area expanders on Tags
  dismiss + Tooltip trigger (2.5.8). Static a11y now clean + enforced; AT/zoom pass queued (`_VISUAL-CHECK-QUEUE.md`).
- **Coverage gate added** (`_validate_coverage.py`, build step 11): every real meta must have a name-matched
  gated snippet; orphans/renames fail the build. Keeps "32/32 gated" honest. Build now runs **6 gates**.
- Keyboard audit (2.1.1/2.4.3) — all PASS (explicit handlers for combobox/modal/tabs; native semantics elsewhere); in `_A11Y-AUDIT.md`.
- Design-system audit — `_DESIGN-SYSTEM-AUDIT.md`: metas 32/32 complete; naming clean bar 1 Figma-mirrored
  camelCase; 43 unused tokens categorised (31 future data-viz palette, 2 pending Tabs wire-in, 2 tooltip rebind, 8 deprecation candidates).
- **States-completeness probe added (advisory, NON-gating)** — `_build_states_probe.py`, build step 5/14.
  Maps which snippets demonstrate empty/loading/error/overflow vs. a curated applicability map; emits
  `_STATES-COMPLETENESS.md` + `tokens/_manifests/states-probe.json`. 41/51 applicable states shown; 10
  advisory gaps (mostly empty/loading — token-canon shows the populated/default visual). Applicability calls
  are heuristic — confirm in `STATE_APPLICABILITY`. Always exits 0; never gates (tiering is strategy-owned).
- **Integrity warnings de-noised (20 → 3)** — `_build_integrity.py` TOKENS pass now skips deprecated/migration
  prose (the §4 backlog notes record OLD paths that are *expected* not to resolve). WARNING pass only —
  ERROR/REBIND logic + exit codes unchanged. Fixed 2 plain-English false matches (button `(primary/secondary)`,
  hero `blur/surface` shorthand; no token/appearance change). Residual 3 are intentional: Modals Figma-name
  note + Tabs proposed `focus/ring` tokens (→ §6 sign-off). Full triage in `_INTEGRITY-WARNINGS-TRIAGE.md`.
- **`focus/ring` signed off (Dave, 2026-06-20)** — promoted colour (`semantic-colour.json` focus/ring) +
  geometry (`layout.json` focus/ring-width|offset) from `review`→`asserted`; guideline status flipped to CANON.
  Fixed a `layout/focus/*`→`focus/*` path typo in `tabs.meta` (the path was wrong, not the token). Integrity
  warnings now **1** (was 3): only the intentional Modals Figma-name note remains.

## 6. Open items needing Dave (consolidated)
- **DECIDE:** `text/secondary` values (V1), inverting-label canon, `rag/warning` standalone-dot rule. (`focus/ring` ✅ signed off 2026-06-20 — see §2.)
- **VISUAL/AT:** 4 baseline organisms (V2), screen-reader + keyboard pass (V3), zoom/reflow (V4) — see `_VISUAL-CHECK-QUEUE.md`.
- **PARKED:** deprecated-binding migration (§4) → Sutherland; Figma dark write-back → pending go-ahead.
- **TOKEN HYGIENE (from `_DESIGN-SYSTEM-AUDIT.md`):** confirm 8 dead button-border/misc tokens; verify the
  `subsectionInset` camelCase against Figma. Bundle with Sutherland (real usage confirms what's actually consumed).
- **DECIDE — `tooltip/*` deprecation (re-assessed 2026-06-20):** the gated Tooltip uses the mode-aware **elevation
  pattern** (shadow in light, `elevation/border` outline in dark) — same as Dropdown. The dedicated `tooltip/background`
  + `tooltip/border` tokens are redundant with it, and *adopting* them would change appearance (dark surface
  #000→#1D1D1D, a border appearing in light) — so this is NOT a silent fix. **Recommendation: deprecate `tooltip/*`**
  in favour of the elevation pattern. Needs Dave's confirm (or a deliberate choice to make the tooltip a raised surface).
