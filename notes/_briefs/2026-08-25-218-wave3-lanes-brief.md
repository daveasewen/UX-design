# #218 build brief — wave-3, three lanes (ADOPTED s218-D4, from the W2 receipt's measured draft)

Adopted by Dave in full: **lane α — forms** (form layout+validation · date · date-range · time ·
number/currency · file upload · OTP · textarea, 8 components, one family idiom, heavy a11y) ·
**lane β — feedback** (alert · toast · drawer · popover · skeleton, 5 — overlay/announce idioms
shared) · **lane γ — data-display** (data grid · stat/metric card · empty state — and FIRST
verify whether the charts-kit gap row is a register artefact before briefing/building it; if it
is, name it and build 3). Navigation family is SEQUENCED LATER — do not touch. Layer-2
(shells/templates/lock-ups) held for the ADR — do not touch.

**Per lane (each lane = one sub, lanes run in parallel):**
- Build each component as a `knowledge/snippets/<Name>.reference.html` in the established idiom —
  START FROM REFERENCE: read 2–3 existing gated snippets of similar shape first (e.g. Input
  fields family for α; Modal/Drawer precedents for β; Table/Data-grid kin for γ) and copy the
  conventions (header block, token manifest, type composites `.t-cm-*`/`.t-ed-*` FIRM,
  states, four-theme correctness, ≤ byte budgets, behaviour inline ARIA-first where the markup
  promises it — no phantom controls, per s218-D4).
- Per-lane verify script (`verify_wave3_<lane>_218.py`), green arms + a break arm RED by name,
  driven both ways before reporting.
- ⛔ **THE REGEN SERIAL IS THE CONDUCTOR'S.** Do NOT touch the registry, MIGRATED_SNIPPETS,
  CATEGORIES, the spine, `gen_showroom` page-set, the library index, or any `_build_all` route —
  lanes return SNIPPET FILES + verifies + a receipt; the conductor runs the whole ordered serial
  once at reconcile (#210's lesson, ~6 CI reds).
- Receipt at `notes/_receipts/2026-08-25-wave3-<lane>.md`: components, decisions-for-Dave list
  (every judgment call named, none decided), verify tails, residuals priced.

Fence: no rulings, no tokens/canon edits (needs → `knowledge/_DS-IMPROVEMENTS.md` rows), no
registry/serial (above), no store/lane/GM/LS/memory edits, no commit/push. Render env recipe in
`notes/_briefs/2026-08-24-218-photography-theme-settings-brief.md` § pitfalls; /var/tmp
session-suffixed; 45s-and-real-178s call discipline; four themes × light/dark or declare.
