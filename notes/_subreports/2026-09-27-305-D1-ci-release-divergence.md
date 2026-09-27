# #305 D1 - the CI-only ship-list divergence: git 2.55 prints a zero offset as Z (INTERIM)

provenance: 305 · 2026-09-27 · D1 (Opus 5.5 sub of the #305 conductor), at Dave's seat through `device_bash`; no `git status` in any form, no Project memory.
status: observed (INTERIM copy, second - rides the D25 status commit; the final copy with the full CI verdict and the W-305k close replaces it)
machinery: 0 instrument / 1 feature (commit_date() in the generator)

## The field

`commit_date`. git 2.55 (CI's runner) formats `%cI` for a +0000 commit as `2026-09-27T16:36:40Z`; git 2.34 (seat) and 2.43 print `2026-09-27T16:36:40+00:00`. Reproduced in the cloud container: a full clone of origin at e4ff4284, Python 3.12, git 2.55.0 built from source gives fresh sha256 `d1c0a01837f33126`, CI's exact hash; the unified diff against the committed manifest is that one line and nothing else. git 2.43 in the same clone gives PASS `a5b00c14`.

## The fix

`knowledge/_release/_gen_pack_manifest.py` `commit_date()` formats the date itself from `--date=raw` (epoch and offset), which reproduces the old `%cI` byte for byte on all 1,650 commits (+0000 and +0100). The committed RATIFIED v1.0.14 manifest is unchanged; the gate PASSES under git 2.34, 2.43 and 2.55.

## First push and the release job

Commit `9c3f4663` (on top of C3's `7b544593`), pushed `e4ff4284..9c3f4663` by plain `git push origin master`, fast-forward checked first. CI run `36347602064`: release job SUCCESS at 20:20:17Z; its log shows `git version 2.55.0` on the runner and step 7 `PASS ... sha256 a5b00c1450dc83c8`.

## s305-D25 and s305-D24

- s305-D25 (call 24, the modal rule): status returned from `enacted` to `ruled` with `_inscribe_ruling.py --set-status s305-D25 ruled` (dry run clean, then written), and one evidence line added with `--amend-evidence`, naming 568e2534 (C1's wave-one stamps commit, which stamped it against 27efb7b6) and the reason: call 24 left the wording to Dave and the metas carry R4a's draft (F3). The tool allowed the move back: `ruled` is in the store's own vocabulary.
- s305-D24 (call 23, own size): left `enacted`. The sitting page's call 23 does not leave the wording to Dave (call 24 says "the wording is yours"; call 23 says only "this is the rule it enforces"), and the inscribed ruling carries no wording reservation. The #304 when-rules page did offer the sentence "Proposed wording, for yours" (question 5, the same phrase as question 6). That is a judgement, named for the conductor; W2's report already says the wording is his to amend.
