# #305 D1 - the CI-only ship-list red named and closed: git 2.55 prints a zero offset as `Z`; CI green on all three jobs; W-305k closed

provenance: 305 · 2026-09-27 · D1 (Opus 5.5 sub of the #305 conductor), at Dave's seat through `device_bash`, plus the cloud container for the reproduction (a clone of the public origin, nothing written to the mount from there); no `git status` in any form, no Project memory
status: observed (FINAL copy - rides the close commit; that commit's own sha and CI run are in the hand-back, not here)
CITES: `notes/_lanes/305/_COMMON-BRIEF.md` · `_HANDOFF-155-*.md` § THINGS A COLD SEAT SHOULD KNOW · `2026-09-27-305-C3-commit.md` · `2026-09-27-305-F1-ci-reds.md` · `2026-09-27-305-V1-verifier-wave-one.md` (F3) · `2026-09-27-305-W2-remaining.md` · `2026-09-27-305-V2-verifier-cut.md`
machinery: 0 instrument / 1 feature (`commit_date()` in the generator)

## The answer first

- **The field is `commit_date`.** CI's runner has git **2.55.0**, which prints `%cI` for a +0000 commit as `2026-09-27T16:36:40Z`. git 2.34 (the seat) and 2.43 print `2026-09-27T16:36:40+00:00`. The committed RATIFIED manifest was generated at the seat, so it carries `+00:00`; CI's fresh generation carried `Z`. Nothing else differed.
- **The fix** is in `knowledge/_release/_gen_pack_manifest.py` `commit_date()`: it reads `--date=raw` (epoch and ±hhmm), which is stable across git versions, and formats with `datetime.isoformat()`. That equals the old `%cI` byte for byte on all 1,650 commits in the history (74 at +0000, 1,576 at +0100). **The v1.0.14 manifest did not move** (a5b00c14 before and after).
- **CI is green on every job** for both pushes: runs `36347602064` (9c3f4663) and `36347858414` (fd607c74).
- **s305-D25 is back to `ruled`**, with one evidence line naming 568e2534. **s305-D24 is left `enacted`** (a judgement; see below).
- **W-305k is closed**, and so is D1's own row W-305d1.

## How the field was found

The seat, C3's shared clone (py3.12.14 aarch64) and my own full clone from GitHub in the cloud container (x86_64, git 2.43, py3.12.3) all PASS. That clone also passed after running the release job's steps 5 and 6 first. That ruled out the architecture, a full against a shared clone, the checkout path and HOME, the Python patch level, and an earlier step dirtying the tree. The one difference left was git itself. I built **git 2.55.0 from source** in the cloud container and ran `--check` in the same clone: **FAIL, fresh `d1c0a01837f33126`**, CI's exact hash. A unified diff of that fresh manifest against the committed one is a single line:

```
-  "commit_date": "2026-09-27T16:36:40+00:00",
+  "commit_date": "2026-09-27T16:36:40Z",
```

`git show -s --format='%cI | %aI | %cd' --date=iso-strict 0ef30746`: git 2.43 prints `+00:00` in all three; git 2.55 prints `Z` in all three. The runner's version is confirmed in the CI log itself (`git version 2.55.0`, release job of run 36347602064, `_ci-release-D1a.log`). Because the field was named by reproduction, **no diagnostic change was made to the workflow or the gate**.

This also explains P1's run: its fresh `931bf09e` against the seat's `09927aed` was this same `Z`, sitting under the status-line difference F1 fixed.

## The fix, verified before the push

With the patched generator:
- `--check` PASS a5b00c14 at the seat (git 2.34, py3.10), and in the clone under git 2.43 and 2.55 (py3.12).
- Release-audit `--selftest` 10/0; the generator's own `--selftest` 248/0.
- Under git 2.55 in the clone, every later release-job step is green: `--pack`, ci-template `--check` and `--selftest`, `build-designer-pack.sh --selftest`, and the cold-start projections. `--drift` stays advisory as before.

**Not changed, and named for the conductor:** `apollo-spider/build-designer-pack.sh:258` reads `%cI` the same way, for the baked README and the PROVENANCE date. It is in no CI red. It would bite only at the next bake on git 2.55 or later, where a re-bake of the same commit would stamp `Z` and stop byte-matching an earlier bake. The same one-line change there would close it. That is machinery the frozen ledger leaves editable, but it is outside this brief.

## Commits and pushes

1. **`9c3f4663`** carries the fix, the W-305d1 doc row (925 items), the regen serial (`_CHAIN.md`, the schematic), a dashboard re-run, the D1 lane dir and C3's stamps-commit transcripts (`_gitcommit-C3b.{log,term}`, `_msg-C3b.txt.t3-rendered`, `paths-c3b.txt`). It went through `_git_commit.sh` on the declared not-a-wrap path: exit 0, `✓ done — locks clear`.
   - Push: `e4ff4284..9c3f4663`, a plain `git push origin master`. I checked first that the branch was `master` and the push was a fast-forward. It took C3's `7b544593` stamps commit with it. `ls-remote` = local HEAD (`_push-D1.log`).
2. **`fd607c74`** carries the s305-D25 status and evidence, the serial run (`_RULINGS.html`, `_CHAIN.md`, the schematic), this report's interim copy and the lane tail.
   - Push: `9c3f4663..fd607c74`, fast-forward, `ls-remote` = local HEAD (`_push-D1b.log`).
3. **The close commit** carries W-305k and W-305d1 as done, the serial run and this final report. Its sha and CI are in the hand-back.

No lock was stranded at any point, and nothing was moved to `_orphan-locks/`.

## CI, read to completion (verdicts taken after `render` closed)

| run | sha | release | gates | render |
|---|---|---|---|---|
| 36347602064 | 9c3f4663 | ✅ 20:20:17Z | ✅ 20:31:38Z | ✅ 20:33:44Z |
| 36347858414 | fd607c74 | ✅ 20:24:19Z | ✅ 20:35:39Z | ✅ 20:37:54Z |

- **Release step 7:** `PASS — … byte-identical to a fresh generation at 0ef307460dcf (1781 files, sha256 a5b00c1450dc83c8)` in both runs. Steps 5–13 all ran.
- **Gates step 5:** `SURVEY: 69 pass · 0 FAIL · 6 COULD-NOT-ASK · 0 unaskable · 79 not asked` in both runs. `[145]` and `[146]` pass. Could-not-ask: `[13] [61] [74] [142] [147] [148]`.
- **Gates step 6: all 154 of 154 asked, 0 gate reds.** Advisory: `[140] [141] [150]`. Could-not-ask: `[10] [13] [61] [68] [73] [74] [142] [147] [148] [153] [154]`. `[147]`–`[154]` were asked for the first time since the cut; none is red.
- **Red by name: none that fails a job.** The advisory evidence-linter step reads its usual `⛔ EVIDENCE GATE FAIL — 6 lint · 0 unparsed · 3 rc/observation mismatch` and continues, the same as #304's run. Artefact freshness is `7 FRESH · 0 STALE`.
- Logs are in `notes/_lanes/305/D1/`: `_ci-release-D1{a,b}.log`, `_ci-gates-D1{a,b}.log`, `step6-parse-{a,b}.txt` and `_ci-runs-*.txt`.

## s305-D25 and s305-D24

- **s305-D25** (call 24, the modal rule) was stamped `enacted` in **568e2534**, C1's wave-one stamps, which pointed it at 27efb7b6.
  - I ran `_inscribe_ruling.py --set-status s305-D25 ruled`: a clean dry run, then `--write`, `enacted → ruled`, with the reconstruction proof passing. **The tool allows a move back:** its vocabulary check reads lead words from the store, and `ruled` is one of them.
  - Then `--amend-evidence` added one line (5 → 6 lines). It names 568e2534 and says the status was returned to ruled because call 24 left the wording to Dave ("the wording is yours") and the metas carry R4a's draft (F3). `says`, `ruled` and `governs` are untouched by construction.
- **s305-D24** (call 23, own size) was **left `enacted`**. This is a judgement, and I name it for the conductor.
  - The sitting page Dave answered does not leave call 23's wording to him. Call 24 says "the wording is yours"; call 23 says only "this is the rule it enforces". The inscribed s305-D24 also reserves no wording.
  - Against that, the fuller #304 when-rules page put the sentence as "Proposed wording, for yours" (question 5), in the same phrase it used for question 6. W2's report already records that the wording is his to amend.
  - If the conductor reads "for yours" as reserving the wording, the same two tool calls apply to D24, with 7b544593 as the sha where it was stamped.
- ⚠ `notes/_KG-EXPLORER.html` bakes statuses and was not rebuilt (about 157 s). It will show D25 as it last baked until the next rebuild.

## W-305k: CLOSED

Every limb of its `closes_when` is met, and each one is receipted in `closed_by`:
- V2 opened the real zip and filed its report.
- X, Y1 and Y2 are on origin, and CI is read back green.
- s305-D2 reads enacted.

⚠ **V2's verdict, DO NOT SHIP to the audience (s279-D1 against W-305n6), is Dave's and stays open. Closing this row does not settle it.** W-305d1 is closed too.

**W-305f1 has now met its own `closes_when`** ([133], [134], [145], [146] and release step 7 are green). It is not mine to close, so I name it here.

## Paths written by this seat

- `knowledge/_release/_gen_pack_manifest.py`
- `knowledge/_rulings.json` (through the tool only)
- `knowledge/_state.json` (the W-305d1 row, then two closes)
- The regen outputs: `_CHAIN.md`, `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html`, `dashboard/index.html`, `notes/_RULINGS.html`
- This report and `notes/_lanes/305/D1/**`

`backup/_rulings.json.pre-D1` (1.1 MB) is held and not committed: git has the prior version.

## Addendum, by addition (after the close commit; this addendum itself is NOT committed)

The close commit is **`01fb005a`**, pushed `fd607c74..01fb005a` (fast-forward, `ls-remote` = local HEAD, `_push-D1c.log`). CI run **`36349147952`**: release ✅ 20:45:15Z · gates ✅ 20:57:11Z (survey 69 pass · 0 FAIL; step 6 154/154 asked, 0 gate red, advisory [140] [141] [150]) · render ✅ 20:59:07Z. Uncommitted tail for the next commit seat: this addendum, `notes/_lanes/305/D1/{_ci-gates-D1c.log, _ci-runs-01fb005a.txt, _gitcommit-D1c.{log,term}, _msg-D1c.txt.t3-rendered, _push-D1c.log, step6-parse-c.txt}`; `backup/_rulings.json.pre-D1` held.
