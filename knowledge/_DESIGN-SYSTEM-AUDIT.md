# Design-system consistency audit
**Date:** 2026-06-20 | **Scope:** `tokens/semantic-colour.json` (116 semantic tokens) + 32 component metas | **Method:** static cross-reference

## Summary
The system is in good shape: **metas are 100% complete**, naming is consistent bar one Figma-mirrored
exception, and every "unused" token is explained (future palette, intentional rebind, or pending wire-in).
**Nothing here is a build-breaking defect** — the items below are deprecation/wire-in decisions for Dave.

## 1. Meta completeness — ✅ 32/32
Every real component meta carries `name`, `category`, `accessibility.relatedSC`, and `tokenValidation`. No gaps.

## 2. Naming consistency — 1 note
- `divider/border/**subsectionInset**` is camelCase among kebab-case siblings (`break`, `section`, `subsection`).
  **Likely faithfully mirrors the Figma variable name** — do NOT rename unilaterally; if the source uses
  camelCase the store should match it. Flag for Dave: confirm against Figma, rename both sides if it's our drift.

## 3. Tokens defined but never referenced (43 of 116) — categorised
Unused ≠ wrong. Breakdown:

**a) Future palette — expected, keep (31):** the entire `data-vis/*` group — `data-chart/{blue,green,orange,pink,purple}-1..4`, `border/on-light|on-dark/*`, `surface/secondary`. No Chart/Data-viz component is built yet; these are the canonical palette waiting for it. No action.

**b) Pending wire-in — tracked (2):** `tabs/hover`, `tabs/pressed` — added in fix #7 for the Tabs rewire; the Tabs snippet still binds primitives. Action already in `_FINDINGS-INDEX.md` (Tabs rewire / Figma write-back).

**c) Intentional snippet rebind — reconcile or deprecate (2):** `tooltip/background`, `tooltip/border`. The gated Tooltip deliberately uses `background/default` + `elevation/border` instead, because the meta-bound `tooltip/*` had a near-invisible dark border (~1.3:1). **Decision for Dave:** either fix the `tooltip/*` dark values and rebind the snippet to them, or deprecate `tooltip/*` in favour of the elevation pattern.

**d) Deprecation-review candidates (8):** button border-state tokens `primary/border/{hover,pressed,disabled}`, `secondary/border/{hover,pressed,disabled}`, `form/border/pressed` — HSBC buttons are filled and don't render border emphasis per-state, so these may be genuinely dead. Plus `tertiary/text/disabled`, `elevation/decorative`, `border/strong` (general-purpose, currently unused by any gated snippet). **Decision for Dave:** confirm dead → move to the deprecation manifest, or keep as reserved.

## 4. Recommendation
Items 3c + 3d are a small **token-hygiene pass** (≈10 tokens) — worth doing *with* the Sutherland migration,
since Sutherland's real usage will confirm which button-border / tooltip tokens are actually consumed. Until
then they're harmless. No gate added: "unused token" is a judgement call (future palette is correctly unused),
so this stays an audit, not a check.
