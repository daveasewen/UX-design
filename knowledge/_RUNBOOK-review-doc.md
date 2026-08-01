# Runbook — decision review docs (the two-register rule)

*Ruled by Dave, live, 2026-08-01 #66 (ledger § ★ #66, D5): every decision review doc leads each
decision with PLAIN PROSE and folds the machinery beneath it. Exemplar:
`reviews/MOLECULES-KEYFILTER-LOCKUP-2026-08-01-v2.html`.*

## The shape, per decision block

1. **Plain prose first** — what this decision means and what changes, in words a non-specialist
   reads once. No file paths, no token names, no byte counts, no gate names. If a number matters
   at this register, say it in words ("about seventeen thousand characters of dead weight").
2. **`<details><summary>Technical detail</summary>`** — the machinery: measured numbers, file:line,
   ADR references, budgets, the probe that proved each claim. Everything the plain paragraph
   asserts must be backed here; nothing here may contradict the paragraph above it.
3. **Then the options** — radio controls, recommended option marked, never pre-selected.

## Standing rules that still apply (this runbook adds to them, replaces none)

- Plain summary above folded evidence + For/Against + one control per open choice
  (the decision-pack shape that ruled 22 in one pass).
- Live specimens: the thing under decision shown ALIVE (iframes of real snippets), light/dark +
  responsive where relevant.
- Version, don't overwrite: `-vN` filenames; supersession named in the footer.
- Measured figures carry their measurement date and are re-measured on the artefact, never
  recalled from the record.
- Selections aren't persisted — the doc says so, and rulings land in chat + the ledger.

## Hard lessons inscribed #66 (both bit Dave the same evening)

- **The review pair is MANDATORY, not optional:** run
  `python3 knowledge/_review/_make_review.py <path>` so picks + comment pins are capturable.
  A review doc with radio buttons and no export made Dave screenshot his own rulings.
- **Live specimens must be tested IN THE REVIEW DOC'S OWN CONTEXT, not just standalone.**
  `file://` iframes that traverse UP (`src="../…"`) are treated as cross-origin by Chrome:
  scripts silently fall back to JS-off and interactive behaviour reads as broken. Specimens
  are copied INTO the review's directory (or the doc lives beside them), and one interaction
  is proven via the render sandbox ON THE REVIEW PAGE ITSELF before presenting. A "working"
  label on an untested-in-context specimen is a CLAIMED, and it lied within the hour.
