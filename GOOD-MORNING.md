# Good morning, Dave ☕

Here's where we left things — read this first, then dive in.

## Yesterday in one line

We closed the last two structural gaps the Tabs fitness test found (focus + geometry), re-ran the test, and confirmed the Route A–B gap has actually shrunk — the KB now drives a shippable, accessible Tabs in both themes.

## What we shipped (Opus session, fixes #2 + #3)

- **Focus-indicator standard (fix #2)** — searched Figma first: HSBC has **no canonical focus primitive** (it's a CSS-layer concern), so we captured an *inferred* one tagged `review`, grounded in the existing information-blue ramp rather than an invented hex. New `focus/ring` (mode-aware `#305A85`/`#4587A7`, verified ≥3:1), `layout/focus` ring-width/offset (2px/2px), and `guidelines/focus-indicators.md` registered as a **GLOBAL guideline → reaches all 32 components**. Tabs now binds it + carries a focus anti-pattern + cites 2.4.7.
- **Geometry block (fix #3)** — added an optional `dimensions` object to the meta schema and populated Tabs (height 48, padding 20, indicator 3px, track 1px, target 44). The single biggest "had to invent" category is now expressible system-wide.
- **Portability fix (incidental but important)** — every build script had a **hardcoded absolute path** baked from whichever session created it (two different stale mounts). The gate crashed on launch this morning because of it. All 8 generators now derive `ROOT` from `__file__`, so the build is session-portable.
- Re-run #1 recorded in `knowledge/_FITNESS-TEST-tabs.md`. Build gate green: **0 errors, 32/32 schema valid.**

## The headline finding (re-run #1)

All **four structural blockers** that made the first Route B unshippable — broken dark mode, no focus, no geometry, no motion — are now **answered from the KB itself** (verified live, not asserted). The gap shrank from *"correct but fails WCAG in dark + no focus"* to *"shippable and accessible; residual delta is type polish + overflow richness."* The dangerous class of defect (internally-valid-but-unusable) is closed.

## Still open (residual A–B delta — all 🟡, none are WCAG blockers)

The remaining backlog from the fitness test:

1. **Fix #5 — type data-quality nits:** `font-weight` is an unmapped string (`"medium"`), `letter-spacing/font-5` is empty, proprietary font has no fallback stack.
2. **Fix #7 — complete the `tabs/*` group:** no hover/pressed surface tokens, so those states still fall back to flat `tertiary/*` in dark.
3. **Fix #6 — overflow + guideline mapping:** `horizontal-scroll.md` mapped to Tabs is *carousel* guidance, not the tab-overflow pattern; real overflow spec (breakpoint, collapse count, menu a11y) still missing.
4. **Fix #8 — operationalize the angular/square-corner rule** (with Badge + Avatar exemptions).

## Two things waiting on you

- **Commit** — nothing is committed yet this session. When you're ready, the staged changes are: `tokens/semantic-colour.json` (focus group), `tokens/layout.json` (focus dims), `guidelines/focus-indicators.md` (new), `components/meta.schema.json` (dimensions), `components/Tabs.meta.json` (focus + geometry), `_build_xref_index.py` (focus in GLOBAL), and the 8 build scripts (portable ROOT). Suggested message: `feat: add focus-indicator standard (#2) + geometry block (#3); make build scripts session-portable`.
- **Confirm the focus values** with the design/accessibility team — they're `review`-tagged inferred, not canon. That's the one thing standing between "focus standard exists" and "focus standard is signed off."

## Suggested first move

Fix #5 is the cheapest remaining win (pure data-quality in `typography.json`) and removes three more "had to guess" items. Or, if you'd rather prove value over building: a second fitness re-run won't move much until #5–#7 land, so the higher-leverage move may be to **point the test at a different component** (e.g. Dropdown or Input fields) to see whether the focus/geometry fixes generalise — the standards are systemic, so this checks the claim.

Have a good one. Honest state: the KB crossed from "correct" to "can drive a shippable component," at least for Tabs. The open items are refinement, not foundations.
