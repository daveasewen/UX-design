# Brief addendum — Wave 3b: the verified work, six Opus lanes

*Written #203, 2026-08-19, FABLE conductor, AFTER wave 3a's six lanes proved the itinerary's
Status column five weeks stale (18/18 briefed "gaps" already existed). This wave is briefed off
FIRST-HAND probes, not the snapshot. Rules nothing; Dave decides.*
*Dave's word this session: "lets get All models caught up" — the sub pool is the spend target.
Panel: All models 47% used · Fable 61% · resets Thu 11pm.*

**This addendum EXTENDS `_BRIEF-wave3-foundations-2026-08-19-v1.md` — its §2 (read-first), §3
(step-0 premise table), §4 (the fence), §5 (pixel rules), §6 (PROPOSED vs RULED + DO-NOT-RULE),
§7 (pitfalls), §8 (autonomy), §10 (report ≤300 words this wave) ALL BIND unless overridden here.**

## Overrides and additions

1. **⛔ MANDATORY step 0, hardened:** before building ANY component, prove each of your itinerary
   rows absent: `ls knowledge/snippets/ | grep -i <name>` AND `ls knowledge/components/` AND a
   grep for plausible alternate slugs (wave 3a found row 17/19/52/89 under different names).
   Quote the probes in your receipt. **A component that exists = your lane re-points to a
   four-theme REVIEW-203 spread of it** (the wave-3a pivot pattern — see any
   `notes/_receipts/2026-08-19-203-wave3-lane*.md`).
2. **Generator surface is Lane G's EXCLUSIVELY this wave.** No other lane runs ANY generator,
   even `--check` (Lane G's regeneration makes checks racy). Component lanes: snippets + metas +
   review pages + receipt, full stop. Filtered validators on your own files still fine
   (`_validate_snippets.py` etc. read snippets; expect the audit-file side effect — declared).
3. Receipts: `notes/_receipts/2026-08-19-203-wave3b-lane<X>-<topic>.md`.

## The lanes

**Lane G — the canon dark-drop repair (machinery).** Lane C measured `gen_canon_components.py:76`
silently dropping dark-mode component rules: `startswith("[data-theme")` catches harness var
blocks AND real rules like `[data-theme="dark"] .se-msg .ic{…}` — **33 rules across 19 snippets**
(receipt: `2026-08-19-203-wave3-laneC-money-secure.md`, finding 1). Fix the drop test so
component rules survive while harness var blocks still don't; regenerate canon components;
verify the 33 rules present by count and by grep; run every `--check` generator to sync; build
`reviews/REVIEW-203-canon-dark-repair-before-after-v1.html` — the affected components rendered
dark, before vs after, for Dave's eye. Drive it: a mutation test on the drop test itself
(the clause, AND the feature — render one repaired component dark and screenshot it).
You own: `knowledge/canon/gen_canon_components.py` + all regenerated outputs. EXCLUSIVE.

**Lane H — the itinerary class-fix (machinery).** The Status column is hand-maintained and rotted.
Build `knowledge/gen_itinerary_status.py`: derives per-row status from the store (snippet exists ·
meta exists · in MIGRATED_SNIPPETS · showroom page) with an alternate-slug map, emits
`reviews/ITINERARY-STATUS-2026-08-19-v1.html` (+ a machine-readable sidecar JSON). ⛔ Do NOT edit
the 2026-07-14 files — history is frozen (`ADR-0017` write-once); this is a NEW dated derivation.
Include the verified TRUE-gap list (wave 3a suggests: row 86 brand-mark + most P2/P3) — that list
is next wave's brief input, so every row's verdict carries its probe. Fail LOUD on unparseable
rows, never guess.

**Lane I — navigation depth (components, P2).** Rows 35 command palette · 36 sidebar/nav rail ·
37 anchor/scrollspy. Step-0 verify each (row 36 may collide with gated Nav/Menu — check and say).
Build the verified-absent ones through the full gated-component route (#174's walked example).

**Lane J — input depth (components, P2).** Rows 21 combobox/autocomplete · 22 multi-select ·
23 tags input. Same verification-then-build. Shared listbox/chip grammar across the three —
copy from gated Select/Tags snippets, never re-draw.

**Lane K — data-display depth (components, P2).** Rows 55 KPI/trend tile · 56 timeline/activity
feed · 57 avatar group. Row 55 must state in its meta how it differs from gated Stat-card (wave
3a found Stat-card already carries delta semantics — and its arrow binding is a LIVE two-red
question, Dave's; do not resolve it, inherit the current binding and flag).

**Lane L — the 44px hit-area consumer (machinery, ADVISORY).** The token is minted at base tier;
no gate reads it; wave 3a measured two REAL breaches (Amount-input 39px standard field · OTP cell
42px ≤480px — Lane C receipt). Build `knowledge/_validate_hit_area.py`, ADVISORY tier, driven on
rendered geometry (the render-verify runbook's harness), and prove it catches BOTH known breaches
and passes a known-good (Button 44). ⛔ Do NOT wire it into `_build_all.py` (conductor/Dave);
⛔ do NOT fix the breaches (component edits = shared artefacts, and the remedy may be Dave's
call). Report the full advisory sweep table. An instrument is only real once it has run on real
data and caught the known failures — that IS your acceptance test.

## Report back: ≤300 words, decisions-needed list, gate rcs, probes quoted.
