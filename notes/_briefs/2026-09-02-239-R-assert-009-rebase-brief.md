# #239 — CHORE R: re-base `ASSERT-009` 136 → 137 BY ADDITION (Dave: "Okay rebase")

Read `notes/_briefs/2026-09-02-239-COMMON-lane-rules.md` first. Then `knowledge/_assertions.json` entry `ASSERT-009` in full (its `provenance` carries the exact re-base form used six times before — COPY that form, do not invent one) and `knowledge/_validate_assertions.py --help`.

## THE FACT
`ls knowledge/components/*.meta.json | wc -l` = **137** (was 136). Directory entries **141** (were 140), the same four non-meta files. The 137th meta is `knowledge/components/template-dashboard-bento.meta.json`, added at commit `e7cf3db` (after #231, 2026-08-31). CI run #478 (and every run since e7cf3db) aborts at build step 10/142 on this assertion: `[✗] ASSERT-009 environment count=137 (want eq 136)`.

## DO — measure first, then edit
1. Re-measure both counts in-sandbox and quote the commands + outputs in the report. If either differs from the FACT line above, STOP and report.
2. `knowledge/_assertions.json` → `ASSERT-009`: move the expected count to **137** in whichever field the gate reads (find it in `_validate_assertions.py`, do not guess); update the `claim` text's "136 files" and "140 entries" to 137 / 141; APPEND to `provenance` (never rewrite it) one sentence in the established form: `Re-based #239 2026-09-02 (BY ADDITION; the growth is the bento dashboard template — template-dashboard-bento.meta.json @ e7cf3db, after #231; Dave: 'Okay rebase, do both'): 136 -> 137 measured in-sandbox (ls knowledge/components/*.meta.json | wc -l = 137). Dir entries 140 -> 141, same four non-meta files. README updated same commit.`
3. `knowledge/README.md:13` — `136 metas` → `137 metas`, keep the "count registered as ASSERT-009, re-tested not repeated" pointer intact.
4. The other `asserted_in` homes the gate lists — `_LIVE-STATE.md`, `notes/_MEMENTO-DECISIONS.md`, `_DECISION-HISTORY/2026-08-08-131-the-legacy-rag-fills-and-the-design-kg-nothing-checks.md`: for EACH, `grep -n` the figure and classify every hit as **LIVE** (a present-tense statement of the corpus size) or **HISTORY** (a dated stratum / ledger entry saying what the count WAS). Edit LIVE hits by repointing to `ASSERT-009` (the #207 README pattern — a pointer, not a retyped figure). Leave HISTORY hits UNTOUCHED (ADR-0017 freezes history; `_DECISION-HISTORY/` is dated by construction). If a file has zero LIVE hits, say so and touch nothing; if `asserted_in` then names a file with no live figure, report that as a proposed `asserted_in` trim — do NOT trim it yourself.
5. Run `python3 knowledge/_validate_assertions.py` → must end `ASSERTION GATE PASS` (or the gate's own green wording — quote it) with ASSERT-009 `[✓]`. If the gate has `--selftest`, run it too and quote the last line.
6. Run `python3 -c "import json;json.load(open('knowledge/_assertions.json'))"` — the file must still parse.

## NEVER
No git. No edit to any file not named above. No change to any other assertion. No rewrite of existing provenance text. No `_build_all.py`.

## FILING
`X = R`, slug `assert-009-rebase`. Report from `_TEMPLATE.md`, short; include the per-file LIVE/HISTORY table with line numbers, a PITFALLS section (owner per row — e.g. "the count will flip again on the next component wave; the assertion refuses again and that refusal is correct"), and REPLAY-THESE (≤5 lines). Stub back to chat ≤10 lines: report path · gate verdict line quoted · files touched with line numbers · anything you STOPPED on.
