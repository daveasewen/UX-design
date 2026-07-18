---
name: proforma-programme
description: "Apollo pro-forma programme = 'Apollo mono' (unbranded user-testing base). Tranches 1–7 BUILT + gated in knowledge/_proforma/ (T7 = navigation, 2026-07-15). FOUR gates: universal + DEF-003 (CSS-governed motion) + DEF-004 (no-hardcode styling) all in _build_all.py. Fully tokenised (colour/motion/spacing/border/radius). Taxonomy: Apollo mono/UI/SC. Type-token system = scheduled TARGET (waiting on Dave's Figma)."
metadata:
  node_type: memory
  type: project
---

**Pro-forma programme = "Apollo mono".** Building the whole component inventory as a lightly-styled **monochrome
pro-forma** base, then expressing it in modes (see [[apollo-component-library-itinerary]], [[apollo-mono]]).
Working LOCAL via the desktop bridge (repo `/Users/daviewen/Documents/Claude/Projects/UX-design`).

**Architecture (RULED):** ONE component skeleton, N token modes. Base = **monochrome** (KB tokens, bind by
intent). Primary = **near-black #1A1A1A** / near-white; **no brand red at base** — colour is meaning-only.
HSBC-brand mode re-adds red + red-once; business-line mode adds rounded + own type + data-viz. Same skeleton,
different skin = the cascade proof.

**Sibling-library taxonomy (Dave, 2026-07-15):** **Apollo mono** = the unbranded monochrome base here (user-testing +
Figma target). **Apollo UI** = the new branded library where varying radii etc. live. **Apollo SC** = the prior branded
work ("keep the ideas, don't copy the solutions"). All three are the SAME skeleton governed by **modes** — see the
FOUNDATIONAL ruling below.

**⭐ FOUNDATIONAL RULING (Dave 2026-07-15):** *"we shouldn't hard code any styling going forward, must be tokenised and
all the sibling libraries should be governed by modes — I want it to be very flexible and future-proof."* Every styling
value is a token so a MODE can override it. Enforced by gates (colour, motion, spacing/border/radius). Geometry/dimensions
are a separate axis (not gated). This is why DEF-004 exists.

**Tranches BUILT (1–7) in `knowledge/_proforma/` as one interactive file each** (light/dark + width slider, live
behaviours, container-responsive to 320px, WCAG 2.2 AA, all gates GREEN, rendered/inspected):
- **T1**: Icon button · Empty state · Skeleton · Amount input · Stepper · Drawer.
- **T2**: Toast · Alert/callout · Date picker (+ from/to date-range picker) · File upload.
- **T3**: Checkbox (tri-state) · Radio · Switch · Segmented · custom Select/listbox.
- **T4**: Tabs · Breadcrumb · Pagination · Accordion · Tooltip — APPROVED as-is.
- **T5**: Card · Badge/Tag · Progress (bar/ring) · Avatar · Banner.
- **T6**: **Text entry & forms** — text field (+ quiet-filled variant) · textarea · search · number/stepper/masked/password ·
  inline validation · form layout. Signature mono idea = **the BORDER carries state** (grey→near-black on focus-within, no
  colour/shadow/shift). Shared atoms `.f-label/.f-hint/.f-count/.f-msg/.f-dot`. Real error TRIANGLE (`status-icons/error.svg`)
  + roundel success/warn/info; re-themeable RAG dot. **Review-fixed with Dave (2026-07-15):** uniform 51px field height in every
  state, no size-jump when the search clear-icon appears, no layout-jump when error rows appear (`.f-msg{min-height}`), thick-field
  padding fixed, status icons un-boxed.
- **T7**: **Navigation** (2026-07-15) — Popover/NavToggle · GlobalHeader · SideNav (+ icon-rail) · MegaMenu (cols/featured/tabbed) ·
  Drawer+NavAccordion. Disclosure a11y spine throughout. See [[nav-pattern-catalog]] for the full spec + the research catalog behind it.
Artifacts `apollo-proforma-tranche-1..5`, `apollo-tranche-7-navigation` (+ nav catalog). ~30 components.

**FULLY TOKENISED (all value-preserving, gated).** Colour (`[data-theme]` blocks) · **motion** (CSS scale tokens
`--btn/--ib/--card/--qa/--chip/--accent-*` + easings — JS motion removed everywhere incl. snippet canon, DEF-003) ·
**spacing** (`--space-*` ladder) · **border-width** (`--bw-sm/md/lg` = 1/2/4 + `--bw-1_5` = 1.5px) · **radius** (mode token
`--radius:0` + `--radius-round:50%` + `--radius-pill:999px`). DEF-004 caught real 1.5px leaks (T2 upload, T3 ×2) → the `--bw-1_5` token.

**Gates (all wired into `_build_all.py`, 24 steps green):** `_check_proforma.py` (single-file dev) · **`_validate_proforma.py`**
(universal: real-icons · no-hardcode-colour · refs-resolve · icon-buttons-named · manifest-path-is-real) · **`_validate_css_governed.py`**
(DEF-003, no JS-driven motion) · **`_validate_no_hardcode.py`** (DEF-004, no raw px in spacing/border-stroke/radius; skips token defs,
@media, transparent borders, var() fallbacks). Universal-vs-mode SPLIT: mode rules (monochrome/near-black/square/colour=meaning)
deliberately NOT gated. `_PROFORMA-DEFECTS.md` tracker.

**DEF taxonomy:** DEF-001 (state-cluster) · DEF-002 (glyph-presence) · DEF-003 (CSS-governed motion) · DEF-004 (no-hardcode styling).

**Rules (in `_PROFORMA-RULES.md`):** 10 roundel carve-out · 11 common interactive state cluster · 12 glyph presence ·
13 **reuse calibration** (COLLABORATIVE — ASK Dave what he valued first, see [[feedback-reuse-calibration]]) · 14 **CSS + tokens
govern styling; JS behaviour-only** · 15 **no-hardcode styling / mode-governed** (DEF-004, the FOUNDATIONAL ruling).

**SCHEDULED TARGET (blocked on Dave's Figma file):** the **type-token system** — 3 responsive scales × 9 sizes each with
line-heights, 4px-grid aligned → distilled into **2 labelling-style sets** (multiline/editorial + UI). The same Figma file also
carries **new colour tokens for all 3 modes**. When it lands: restore placeholder leading-trim (also fixes the off-grid 51px field
height → on-grid) and apply type tokens across the pro-forma. See [[type-system-tokens]]. Also NOTED for later: **legacy-libraries** build-out.

**Future ideas noted:** asset/icon metadata + catalog (`_icon-index.json` + gallery, to speed icon discovery — Dave's ask after the
error-triangle hunt) · git post-commit hook running the staleness gate · extend DEF-003 to scan snippets · rationalise `--bw-1_5` and
the flat `--space` ladder at Figma stage · extend the icon gate to compare glyph GEOMETRY to the asset (not just filename).

**OPEN / NEXT:** Tranche 8 (BottomTabBar+More · InPageNav/scroll-spy · FooterNav · RelatedLinks/Cards · Stepper) OR the type-token
system once the Figma file arrives. See [[apollo-mono]], [[nav-pattern-catalog]].
