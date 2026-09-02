# #238 — LANE B: L2 — THE BEHAVIOUR ADDRESS (`s234-D5`), built for Dave's eye before it populates

Read `notes/_briefs/2026-09-02-238-COMMON-lane-rules.md` first.

## GROUND FIRST
`notes/_briefs/2026-09-02-234-v106-brief.md` (L2 at line 31; line 47: schema changes are Dave's — ratify at his eye BEFORE populate) · `knowledge/_rulings.json` `s234-D4`, `s234-D5`, `s234-D6`, `s235-D1`, `s235-D2`, `s237-D10` · `notes/_subreports/2026-09-02-235-L1-receipt-gate.md` and `_DECISION-HISTORY/2026-09-02-235-the-receipt-and-the-entry-gate.md` (L1: `_validate_receipt.py`, `_validate_screen.py` step 0; "the three questions L1 left behind" — find and quote them) · `knowledge/components/*.meta.json` (the 20 prose `behaviour` values — count them, name them) · `gen_component_partials.py` (`#token-manifest` block is the model) · the pack SKILL.md rule 2.

## DELIVERABLES
1. **Schema** for `behaviour` → `{script: <address>, partial: <id|null>, events: [...], fallback: <text>}` as a JSON Schema fragment + the meta-schema change, migration BY ADDITION (prose kept under `$note`).
2. **Migration PROPOSAL, not applied:** `assets/…/behaviour-migration.json` — the 20 values, old prose → proposed typed object, with the quote each field came from; UNPROVEN where the prose does not settle a field. ⛔ Do NOT write the 20 meta files — Dave ratifies at his eye first.
3. **A review page** `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` (swiss idiom, light+dark, 1440+390): each of the 20 side by side, old → proposed, plus the three L1 questions with options and your recommendation — NOT a ruling.
4. **Generator + gate, built and driven on a fixture:** `gen_component_partials.py` emits a `#behaviour-manifest` block beside `#token-manifest`; SKILL.md rule 2a drafted as a PROPOSED text block in the report (not written into the pack); L1's gate extended to read the meta address and check the page loads it — drive it on one screen under `/dev/shm` with a mutation arm (address present / absent / wrong).
5. **Report** counts: **metas with behaviour 20 · migrated-proposed n · UNPROVEN n · gate arms n (red n/n) · L1 questions 3 (carried)**.

## DO NOT RULE
The three L1 questions · any pack version bump (v1.0.5 HELD, `s234-D1`) · populating the metas · deleting any prose · anything under `apollo-spider/` except reading.

## PITFALLS
1. Regen serial reds if a generator runs partially — never run `_build_all.py`; drive your generator on a fixture copy. 2. Building the likeliest reading of an ambiguous prose value — mark UNPROVEN, show it in the review. 3. A gate that checks the meta and not the page (or the reverse).

## FILING
`X = B`, slug `L2-behaviour-address`. Stub back to chat per COMMON.
