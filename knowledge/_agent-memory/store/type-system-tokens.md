---
name: type-system-tokens
description: "SCHEDULED (Dave 2026-07-15): from a Figma file, new Apollo TYPE tokens (3 responsive scales × 9 sizes + line-heights, 4px-aligned) → 2 component LABELING-style families (editorial/multiline + UI); the SAME Figma file also has new COLOUR tokens applying to all 3 modes (mono/UI/SC). Dave to share the Figma file."
metadata:
  node_type: memory
  type: project
---

**SCHEDULED WORK — new Apollo type + colour tokens, from Figma (Dave 2026-07-15).** Recorded as a TARGET in the state
machine (`_LIVE-STATE.md`). Dave will share a **Figma file** containing both; execute when it lands.

**SOURCE:** one **Figma file** (Dave to share) carrying BOTH the new type styles AND new colour tokens.

**Type tokens:**
- **THREE responsive scales** (align with KB `semantic-scale` scale-1/2/3 viewport modes), **9 sizes each**, every size with
  a **line-height**, all aligned to the **4px grid**.
- Don't use raw sizes in components — derive a curated set of **labeling / type styles** (named roles) in **TWO families**:
  1. **Multiline copy / editorial** (prose; comfortable line-heights).
  2. **UI elements** (buttons, labels, inputs, chips; tighter line-heights; trim matters).
- Standard pattern: raw scale → semantic type styles → editorial-vs-UI split. Maps onto `tokens/typography.json`.

**Colour tokens (SAME Figma file):** new colour tokens that apply to **ALL THREE modes** (Apollo mono / UI / SC). Fold into
the same pass. Fits the mode-governance model ([[apollo-mono]]): modes are token-value overrides — these new colour tokens
extend/replace the current semantic-colour set across all three.

**Leading-trim ties in:** `text-box-trim` ([[leading-trim-label-decision]]) also **aligns text to the 4px grid** (not just
optical centring). Current gap (Dave flagged): the trim `:is(…)` rule **excludes `input`/`textarea`** → placeholder/field
text isn't trimmed/grid-aligned ("lost placeholder trimming"); and the interim `.f-field` `min-height:51px` is off-grid
(51%4=3). Left as-is until the scale lands (don't guess grid values).

**Execution plan (when the Figma file lands):** ingest type + colour tokens (extend `tokens/typography.json` + the colour
token set) → define the 2 labeling-style families → apply across the pro-forma (field heights on-grid, trim extended to UI
text/inputs, everything 4px-aligned) → wire into the modes → gate. See [[type-rule-sentence-case]], [[token-collection-architecture]], [[apollo-mono]].

---

**📝 ALSO NOTED (Dave 2026-07-15, parked):** *"we might have to build out more for LEGACY libraries."* Future consideration,
flagged so it's not lost — scope TBD (supporting/reflecting older component libraries within the Apollo system). Recorded in
`_LIVE-STATE.md`. Revisit when we get there.
