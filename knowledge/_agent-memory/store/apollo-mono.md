---
name: apollo-mono
description: "Apollo = THREE libraries (mono/UI/SC). FOUNDATIONAL: no hardcoded styling — all tokens, sibling libs governed by MODES. Apollo mono fully tokenised + gated as of 2026-07-15 (colour/motion/spacing/border/radius). JS-free."
metadata:
  node_type: memory
  type: project
---

**APOLLO LIBRARY TAXONOMY — three libraries (NAMED Dave 2026-07-15):**
- **Apollo mono** — the monochrome pro-forma (Tranches 1–5). Unbranded, colour = meaning only. The **base**,
  the **user-testing** build, and the **Figma-transfer target**. This note.
- **Apollo UI** — a NEW library. **Varying radii live HERE** (rounded); usability-first "big-sister".
- **Apollo SC** — the **branded** build worked on previously (HSBC-brand expression). Likely home for the
  **"supercharge"** brand-uplift rework (Input-fields uplift, Ultra Light weight, `:visited`, icon mark-tokens —
  see [[supercharge-codename]]); rolling supercharge in = defining that mode's token values, a separate later job
  (the tokenisation below is what makes it a mode-override rather than a rebuild). Confirm SC-vs-own-mode later.

**FOUNDATIONAL RULING (Dave 2026-07-15): no hardcoded styling; everything TOKEN + MODE governed; flexible + future-proof.**
ALL styling is a token; the three libraries are governed purely by MODES (token-value overrides over the ONE
skeleton); adding a library = adding a mode, never forking components. Enforced by **DEF-004**. Geometry/dimensions
(width/height, CSS-triangle arrows) are a separate axis. Recorded in the state machine `_LIVE-STATE.md` as we go.

---

**TOKEN-GOVERNANCE COVERAGE — Apollo mono is FULLY TOKENISED + GATED as of 2026-07-15.**

**✅ Done + gated:**
- **Colour** — `[data-theme]` token blocks; universal gate fails on any hardcoded hex.
- **Interaction motion** — size-bucketed (`--btn/--ib/--card-grow/press`) + accent pops (`--accent-*`); pure CSS,
  no JS; **DEF-003** enforces it.
- **Spacing** — all padding/margin/gap → `--space-*` (value-preserving; computed spacing identical on 1,474 elements).
  Flat ladder for the mono representation; full semantic-responsive KB map (`tokens/spacing.json`) = Figma-stage.
- **Border-width** — `--bw-sm/md/lg` = 1/2/4 (+ `--bw-1_5`, off-KB-scale, candidate to snap to 1/2 later).
- **Radius** — a MODE TOKEN: `--radius:0` (mono/square) · `--radius-round:50%` · `--radius-pill:999px`. **Apollo UI
  overrides `--radius`** to round corners without forking.
- **Motion timing** — `--ease/--spring/--press/--drawer`.
- **DEF-004 gate** (`_validate_no_hardcode.py`, wired into `_build_all.py`, full build green 24/24): flags raw px in
  spacing/radius/border-stroke in component CSS. Rule 15 in `_PROFORMA-RULES.md`. Caught 3 real `1.5px` leaks.
- **✅ JS-free everywhere** — the snippet-canon holdout (`sizeScale()` GROW=7/PRESS=9 in Button/Modals/Quick-actions/
  Selection-controls) migrated to CSS scale-factor tokens (`--btn/--qa/--chip-grow/press`); `canon.css` regenerated
  value-preserving; compose gate PASS. No JS-driven motion anywhere.

**Later / Figma-stage:**
- **Type-scale** → bind to KB `typography.json` (like spacing — Figma-stage).
- **Mode mechanism** — once ready, add `[data-lib="ui"|"sc"]` token-override blocks so mono/UI/SC are pure mode switches.
- **Optional hardening** — extend DEF-003 to scan `snippets/` too (the JS holdout escaped it because it's scoped to `_proforma`).
- **--bw-1_5 + spacing ladder** rationalisation = a Figma-stage tidy (don't disrupt approved mono layouts pre-Figma).

**Decisions captured in:** the **state machine** `_LIVE-STATE.md`, project memory (this + [[interaction-motion-experiment]]),
on-disk `_PROFORMA-RULES.md` (rules 1–15) + `_PROFORMA-DEFECTS.md` (DEF-001..004), and the gates.
