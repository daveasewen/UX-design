---
name: type-rule-sentence-case
description: House typography rule — ALL text is sentence case; never uppercase transform (eyebrows/labels included). EXCEPTION 07-15 the Swiss-design skill keeps all-caps
metadata: 
  node_type: memory
  type: project
  originSessionId: b6d4d256-65cf-4438-9588-8f44138e09e2
---

HSBC Common Toolkit house type rule (Dave, 2026-06-30): **all text is sentence case** — never `text-transform:uppercase`. Distinguish kickers/eyebrows/labels by size, weight and colour, NOT capitalisation.

**SOURCE-BACKED 2026-07-02:** the 2026 brand typography standard states "we don't use uppercase or italics lettering — use sentence case" (`guidelines/typography-standards-2026.md` type26-005). No longer just a house rule — brand-wide, and **italics are banned too**. This is the promotion evidence for the G5 all-caps advisory check and informs Dave's open all-caps scope ruling (source favours canon-wide).

**Why:** brand/house type standard; uppercase reads as shouting and hurts legibility (also dyslexia-unfriendly). Dave reaffirmed 2026-07-15: **eyebrows must be sentence case — it's an accessibility/readability issue he's been advised on.**

**How to apply:** when building/reviewing any component, grep for `text-transform:uppercase` in component CSS; strip it (AND the caps-era `letter-spacing` tracking with it). Applied to Eyebrow (snippet + `.c-eyebrow` util) on promotion.

**RULED + ENACTED 2026-07-02 (Dave):** canon-wide, hard gate. All 14 snippets + gallery chrome swept (uppercase AND caps-era letter-spacing removed — Eyebrow precedent; Divider labels/Button caps re-authored sentence case), canon.css regenerated, advisory signals 18→0. Check PROMOTED advisory → blocking: `_validate_snippets.py` check 4 (CSS transform + visible ALL-CAPS runs, acronym-run allowlist), bite-tested ×2 in `_tests/test_gates.py` (16/16). Advisory still sweeps non-gated `_fitness-test` surfaces. No open violations. See [[review-session-progress]] [[component-review-program]].

**⚠️ EXCEPTION — Swiss design skill keeps all-caps (Dave 2026-07-15).** The no-uppercase rule is canon-wide **except** the `swiss-design-system` skill, where all-caps is a **deliberate, liked** stylistic choice (Swiss/International Style convention). Do NOT strip uppercase from that skill's outputs.

**⚠️ PRO-FORMA SURFACE NOT GATED (found 2026-07-15).** Like the icon gate, the sentence-case gate runs on the snippets/components pipeline, NOT the pro-forma tranche files — so all-caps slipped in there (`.tp-stat` stat labels rendered AVAILABLE/PENDING/BALANCE; the `.h .tag` eyebrow chips rendered ATOM/MOLECULE/ORGANISM). Fixed 2026-07-15 across all 5 tranches (stat labels → sentence case; `.h .tag` → `text-transform:capitalize`, tracking removed). Same "new surface needs its gate wired" lesson as [[icon-source-rule]] / [[proforma-programme]] — a sentence-case check on the pro-forma surface is a TODO.

**DIRECTION (Dave 2026-07-15):** he wants to **use the pro-forma as the basis for HTML docs going forward** — so "stick to these rules for everything." The pro-forma rule-set (sentence case incl.) is becoming the house standard for his HTML output, not just the component library. See [[proforma-programme]].
