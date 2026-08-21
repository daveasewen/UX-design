# Receipt — Lane I, #213: ITINERARY-STATUS re-measurement (v1 → v2)

> Hand-run, not `gen_brief.py`-minted. Session #213 (Fable conductor + Opus/Sonnet subs).
> Nothing here is a ruling. `reviews/ITINERARY-STATUS-2026-08-19-v1.json` is UNTOUCHED (write-once,
> ADR-0017 / `s192-D1`) — this is a NEW dated file beside it: `reviews/ITINERARY-STATUS-2026-08-21-v2.json`
> (+ `.html` sibling). `$session` stamped `"#213"`, `$measured` stamped `"2026-08-21"`.

## Method

The job named "find how v1 was generated (grep for a generator script or derive its schema)".
Found directly: `knowledge/gen_itinerary_status.py`. Its own docstring names the exact defect this
job is re-running the check for — #203's six-lane wave briefed off a hand-maintained Status column
and hit 18/18 already-gated "gaps" (`[[premise-ages-faster-than-rule]]`). The generator is the
existing instrument for exactly this measurement: it derives status from five live probes per row
(snippet file · meta.json · showroom page · radius-ratchet membership · `.cn-` canon rule count),
never from a carried value, and refuses to guess (`UNRESOLVED` when the resolution ladder can't
decide). Re-running the SAME unmodified instrument against today's tree — rather than hand-writing
a new probe set — was the correct move per the generator's own class-fix doctrine (ds-018: fix
lands in the generator, not a hand-patch) and per the brief's fence 10 ("gate the class, not the
row").

Steps taken (all read-only against the repo; nothing in `knowledge/` was edited):

1. `python3 knowledge/gen_itinerary_status.py --check` → **FAIL, OUT OF SYNC** (both outputs).
   This alone proves v1 has drifted from the live tree — the premise named in the job brief,
   confirmed mechanically, not asserted.
2. `python3 knowledge/gen_itinerary_status.py --selftest` → **FAIL, 6 sub-fails**, all in arm 2:
   rows 6, 7, 25, 26, 61, 93 were fixture rows the selftest expects to measure `GAP`; today they
   all measure `GATED`. The selftest's own comment (line ~886) already warns fixture rows "move
   under the test" as waves land — this is that warning materialising, not an instrument defect.
   **Residual declared, not fixed**: the selftest fixture list (arm 2) is itself now stale and
   needs new GAP-class fixture rows; that edit is out of this lane's scope (generator edits are
   not named in this job) and is flagged here for the conductor/Dave.
3. Wrote a small out-of-repo wrapper (`/tmp/w/gen_v2.py`, not committed, not part of the repo) that
   imports `gen_itinerary_status` unmodified, calls its own `build()` (the exact function that
   produces v1's data), and writes the result to new v2 paths with `$session`/`$measured`/
   `$prior_snapshot` fields added. **The derivation logic itself was not touched** — every row
   verdict below came from the same probes v1 used, run fresh today.
4. Diffed v1.json against v2.json programmatically (counts, per-row `derived`, `evidence_line`,
   `$orphan_snippets`, `$radius_ratchet_advisory`).

## Premise table

| probe | result | timestamp |
|---|---|---|
| `--check` against v1 outputs | FAIL — both OUT OF SYNC | 2026-08-21 |
| `--selftest` | FAIL — arm 2, 6 rows moved GAP→GATED since #203 fixture was written | 2026-08-21 |
| re-run `build()` on live tree, 124 rows | 0 UNRESOLVED, 1 TRUE gap (row 86, unchanged) | 2026-08-21 |
| `ls knowledge/snippets/ \| grep -iE 'shell\|template\|lockup'` | 20 files present that did not exist / were not claimed by any row at v1 | 2026-08-21 |
| spot-probe `app-shell-doormat` / `template-dashboard` / `cta-lockup` / `card-header-lockup` | all four: meta.json present, showroom page present, `.cn-` canon rules present (43–176 rules) | 2026-08-21 |

## Delta summary, v1 → v2

**Headline: no row flipped between Gap-class and Built/Gated-class.** `$true_gaps` is `[86]` in
both v1 and v2 (Brand-mark: assets exist, no component — unchanged verdict, unchanged evidence).
`$unresolved` is `[]` in both. Per-row `derived` status is identical for all 124 rows
(0 rows changed GAP↔BUILT↔GATED↔PARTIAL). So: **zero Gap→Built transitions, zero Built→Gap
regressions** at the row level the generator currently measures.

That "nothing moved" headline needs the finding below attached, or it reads as more settled than
it is:

**Finding — the Layer-2 premise itself has moved, and the generator can't see it.**
`$orphan_snippets` (store components no itinerary row claims) grew from **1** (`meter`) in v1 to
**28** in v2. 20 of the 27 new orphans are `App-shell-*` (7), `*-lockup` (7), and `Template-*`
(11) snippets — the exact artefact class the generator's own `LAYER2_NOTE` asserts does not exist:
*"No artefact class for these exists in the store yet — not a snippet, not a meta, not a showroom
page."* That sentence was true at #203/v1 and is **measurably false now** — spot-probes on 4 of
the 20 show full routing (snippet + meta + showroom + dozens of canon `.cn-` rules each). The
generator's `resolve()` still early-returns every Layer-2 row (97–124, `layer-2` basis) to
`NO-ARTEFACT-CLASS` without probing the store at all, so none of this shows up as a per-row status
change — it shows up only as new orphans. **This is exactly the class of defect the generator was
built to catch (a hand-carried premise outliving the tree), now sitting inside the generator's own
Layer-2 shortcut.** Not fixed here — generator edits are outside this job's scope and this repo's
DO-NOT-RULE fence — but it is the single most load-bearing finding in this re-measurement and is
named loudly rather than left to erode `$orphan_snippets` silently.

**Secondary drift — canon rule counts, minor:** 9 rows' `evidence_line` canon-rule counts ticked
up between v1 and v2 (form-layout 128→129, date-picker 111→113, combobox 94→95, multi-select
102→103, tags-input 90→91, transfer-list 72→73, banner 72→77, icons svg count 658→659) and one
ticked down (layout-utilities 117→116). Two rows — **status-indicator (rows 47 and 88, which
share one artefact)** — jumped 67→86 canon rules, the largest single delta; not investigated
further here (out of this job's scope — a Layer-1 canon-count change, not a status flip) but named
as the largest single-artefact churn observed.

**Counts identical, drift-class identical:** `$counts` (GATED 94, ASSET-SYSTEM 1, ASSET-ONLY 1,
NO-ARTEFACT-CLASS 28) and `$drift_counts` (AGREES 67, STALE-understates 57) are byte-identical
between v1 and v2. The `--check` FAIL that opened this job was driven entirely by the canon-rule
and orphan drift above, not by any row's derived verdict changing.

## Residuals declared

- Selftest arm-2 fixture rows (6, 7, 25, 26, 61, 93) are stale against the live tree — a generator
  edit, out of this job's scope, named for the conductor.
- The Layer-2 "no artefact class" premise is stale (finding above) — the generator's ROW_MAP has
  no entries for rows 97–124 at all, so this can't self-repair without a generator change. PROPOSED,
  not ruled: rows 97–124 likely need their own ROW_MAP entries (or a Layer-2-specific resolution
  rung) now that 20 shell/template/lockup snippets exist — Dave's / conductor's call, not mine.
- status-indicator's 67→86 canon-rule jump is observed, not diagnosed.

## Evidence pointers

- Generator: `knowledge/gen_itinerary_status.py` (unmodified, read-only import)
- v1 (untouched): `reviews/ITINERARY-STATUS-2026-08-19-v1.json`
- v2 (this job's output): `reviews/ITINERARY-STATUS-2026-08-21-v2.json`, `reviews/ITINERARY-STATUS-2026-08-21-v2.html`
- Orphan spot-probes: `ls knowledge/snippets/ | grep -iE 'shell|template|lockup'`; per-file meta/showroom/canon checks quoted in the premise table above.
