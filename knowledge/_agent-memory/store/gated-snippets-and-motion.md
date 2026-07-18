---
name: gated-snippets-and-motion
description: The render-fallback approach — gated canonical reference snippets + the two-tier canon/exploration model and motion-promotion workflow
metadata: 
  node_type: memory
  type: project
  originSessionId: b984ef19-8715-4451-a36d-b781e96d0089
---

To make the KB drive output (until Sutherland lands), Dave chose **gated reference snippets** (option 3) over a generator — see [[promenaut-fitness-test-plan]]. Per-component cost is craft-linear, not tooling; reuse compounds (e.g. `text/on-inverse` reused across Button/Selection/Links).

**Coverage (2026-06-20): 32/32 real components gated** in `knowledge/snippets/*.reference.html` (Table was the last gap, built 2026-06-20; EXAMPLE-button is just a template). Each token-faithful, both themes, validated by `_validate_snippets.py`. They double as **Sutherland acceptance fixtures**. **5 BASELINES** need design review (not finished canon): Navigations, Headers, Hero (on-image), Video player, Table (sort + small-screen reflow) — tracked in `_VISUAL-CHECK-QUEUE.md`.

**Build gates (now SIX, via `_build_all.py`):** text/icon contrast, indicator contrast, **dark-surface flatness** (`_validate_dark_surfaces.py`; `$darkNote` allowlist), snippet gate, **a11y gate** (`_validate_a11y.py` — reduced-motion required when a snippet animates = hard fail, sub-24px targets reported; bite-tested), **coverage gate** (`_validate_coverage.py` — every real meta has a name-matched snippet; orphans/renames fail), + integrity. All bite-tested. Tokens: `text/on-inverse` (#FFF/#333, inverting surfaces); **`text/secondary`** (#545454/#9B9B9B, review-tagged — de-emphasised body text, used by List items + Cards). A11y work captured in `_A11Y-AUDIT.md`; 1.4.1 use-of-colour rule lives in `guidelines/digital-accessibility-standards.md`. Review items consolidated in `_FINDINGS-INDEX.md §6` + `_VISUAL-CHECK-QUEUE.md`.

**Canon model (decided, `_PROMOTION-QUEUE.md`):** two tiers — gated reference = **canon** (conservative, accessible, standard ease); `_fitness-test/*-AB-showcase.html` Route A = **exploration menu** (richer motion), NOT canon. Promote a treatment only on Dave's explicit OK: tokenise motion → meta `motion` block → gated reference. **A review pass is owed** to walk the queue (Dropdown V2 accent, Button lift/squish+morph, Selection spring, etc.).

**Motion themes draft (`_MOTION-THEMES.md`)** — to review together and extract a reusable family: Reveal (grow-from-anchor), Settle (spring/overshoot — use sparingly), Tactile (press physics), Roll-off (fast-in/slow-out trail — chosen for Dropdown V2), Attention (pulse), Transform (morph). Needs ~3 new `motion/*` easings + 2 durations when promoting.
