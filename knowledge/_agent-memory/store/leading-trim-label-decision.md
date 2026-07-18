---
name: leading-trim-label-decision
description: text-box-trim adopted for label alignment; native metric-aware; headings/body excluded; Firefox degradation accepted
metadata: 
  node_type: memory
  type: project
  originSessionId: b6d4d256-65cf-4438-9588-8f44138e09e2
---

DECISION 2026-06-29: adopt native CSS `text-box-trim:trim-both; text-box-edge:cap alphabetic` to trim half-leading on UI labels for vertical alignment (dot+label rows, key/value, eyebrows, list/table text). Chosen over the pseudo-element `calc(-0.5lh + Xem)` hack because native is metric-aware (reads the font's own cap/baseline — no font-specific magic numbers, which matters since our render only ever has the Arial fallback, NOT Univers Next for HSBC).

**Why:** Dave: "really helps with alignment." Headings + body copy are EXCLUDED (kept comfortable) per Dave's explicit ask.

**How to apply:** lives in `canon.css` BASE hand-layer — element-scoped `.canon :is(button,a,label,span,small,strong,em,b,i,th,td,dt,dd,li,figcaption,legend,caption,summary,output,time)` + the `.c-*` label utilities + a `.u-trim` opt-in — AND injected into each snippet's `<style>` (the standalone review surface, which doesn't consume canon.css). Rolled in per-tranche during the component review (Tranche 1 done 2026-06-29). Firefox unsupported as of 2026-06 → graceful degradation (keeps today's leading), accepted (Dave: Firefox "isn't necessarily for now"). Static gates all green; change is contrast-neutral so the rendered state-contrast gate is unaffected. Font = Univers Next for HSBC (fallback Helvetica Neue/Arial). See [[sandbox-html-rendering]] [[gallery-and-gap-pattern-frontier]] [[component-review-program]].

GOTCHAS found during the review (all fixed): (1) ICON-WRAPPERS — trimming a bare `span`/`button` that holds an `<svg>` shifts the glyph (Search-field magnifier sat high); rule hardened globally to `…):not(:has(svg))`. (2) TRUNCATING LABELS — `text-box-edge:cap alphabetic` + `overflow:hidden` (ellipsis) CLIPS descenders/ascenders (List-items g,y,p cut off); for those use `text-box-edge:text text` (still trims leading, keeps full glyph box). (3) STACK SPACING — trim removes the inter-label leading, so stacked title/desc pairs read too tight; add an EXPLICIT tokenised gap (canon `gap/fixed/content` = 2/4/8/12px), don't rely on line-height. Standard remedies as trim rolls through later tranches. (4) FLEX CONTAINERS — **`text-box-trim` is IGNORED on a flex/inline-flex element**, so a label that is itself `display:inline-flex` (e.g. a nav `.navlink` with `align-items:center`) does NOT get trimmed even though the global `:is(a,span,…)` rule matches it → it sits ~1px high next to a trimmed sibling (found 2026-07-16 on the Masthead bar: nav labels vs the brand span). FIX: put the label TEXT in its own `<span>` inside the flex element — the span is blockified as a flex item (`display:block`) and DOES get trimmed. Rule of thumb: **trimmed labels that live inside flex need the text in a child span.** Worth baking into the canon guidance.
