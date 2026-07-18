---
name: icon-source-rule
description: "Rule — never invent icons; use the real HSBC library (assets/icons/) via a <symbol> sprite + declare in the token-manifest; _validate_icons.py is the advisory check"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 452a0a17-6e63-4feb-ad8c-b23dfebbbd1b
---

**RULE (Dave, 2026-06-22):** never hand-draw / invent an icon in a snippet. Use the real HSBC icon library at `knowledge/assets/icons/` (catalogue + `icons.manifest.json`, exported from Figma; sizes in `tokens/icon-scale.json`, colours `icon/*`). Define icons ONCE as an inline `<symbol>` sprite and `<use>` them; declare them in the snippet's `#token-manifest` `"icons"` block (slug → library file).

**STANDARDS (Dave, 2026-06-23):** HSBC standards forbid creating NEW icons except via the official icon design guide. In the prototyping playground (this KB) using library glyphs is fine, but the FINAL tool will ship ONLY on-standard, design-guide-crafted icons — so `data-bespoke` marks are PLAYGROUND-ACCEPTABLE placeholders, NOT standard; before production each must become a real library glyph (or be crafted via the icon design guide). The ONE sanctioned exception for making new icons is Dave's variable-weight OUTLINE icon sub-project ([[dynamic-weight-icons]], `assets/icons/dynamic-weight/`) — outline icons whose line-weight varies to match font weight, to be PROPOSED to the Brand team when complete. **Bottom line: never invent icons except within that sub-project.**

**Why:** an AI building a snippet will happily draw a plausible-looking SVG instead of the canonical glyph — a silent fidelity + maintenance defect. Found while building Input-fields: my calendar + help icons were invented; the error + success ones happened to match the library byte-for-byte (lucky, not safe).

**How to apply:** pull the path from `assets/icons/<group>/<slug>.svg`; monochrome icons use `currentColor` (inherit `icon/*`); status icons (error/success/warning) may be baked-colour. NOTE the sourcing caveat in `guidelines/icons.md`: these Figma exports are for KB prototyping only; production code sources icons from the **UI Centre**, not our export.

**Check:** `knowledge/_validate_icons.py` (advisory, non-gating) → `_ICON-SOURCE-AUDIT.md`. Byte-matches each snippet's inline `<svg>` path data to the library (746 glyphs indexed). UNKNOWN = invented OR legitimately bespoke (focus ring / control mark) — a human triages. MIGRATED 2026-06-22: 52 → **0 UNKNOWN** (15 verified-bespoke). Content icons (chevrons, close, search, bell, user, play, card, etc.) swapped to library glyphs inline (currentColor, fill — parent CSS sizes/colours); control/animated/tint glyphs (checkbox tick, indeterminate, favourite-star toggle, dropdown selection tick, notification tint-punch marks) marked `data-bespoke="reason"` and the check now verifies those. Done via a one-shot migration script (markers→slug). **PROMOTED TO HARD GATE 2026-06-24:** `_validate_icons.py` now exits non-zero on any UNKNOWN and runs as step 12/15 of `_build_all.py` (build fails on an invented icon). **Circle/rect blind-spot CLOSED:** an `<svg>` built from `<circle>/<rect>/<ellipse>/<polygon>` with NO `<path>` (nothing to byte-match) is now flagged UNKNOWN unless `data-bespoke`. Triaged the two existing cases first: Headers kebab → library `global-controls/menu-more-vertical.svg`; Countdown-timer ring → `data-bespoke` (functional progress graphic). Verified with a negative test (an invented circle-only icon → exit 1). Board: 0 UNKNOWN, 12 verified-bespoke, 746 glyphs.

Relates to [[component-review-program]], [[gate-blindspot-state-contrast]] (sibling "automatable check beats false confidence"), [[token-collection-architecture]].
