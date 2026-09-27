# #305 D1 - the CI-only ship-list divergence: git 2.55 prints a zero offset as Z (INTERIM)

provenance: 305 · 2026-09-27 · D1 (Opus 5.5 sub of the #305 conductor), at Dave's seat through `device_bash`; no `git status` in any form, no Project memory.
status: observed (INTERIM copy - rides the fix commit; the final copy with shas, push range and CI verdict replaces it)
machinery: 0 instrument / 1 feature (commit_date() in the generator)

## The field

`commit_date`. git 2.55 (CI's runner) formats `%cI` for a +0000 commit as `2026-09-27T16:36:40Z`; git 2.34 (seat) and 2.43 print `2026-09-27T16:36:40+00:00`. Reproduced in the cloud container: a full clone of origin at e4ff4284, Python 3.12, git 2.55.0 built from source gives fresh sha256 `d1c0a01837f33126`, CI's exact hash; the unified diff against the committed manifest is that one line and nothing else. git 2.43 in the same clone gives PASS `a5b00c14`.

## The fix

`knowledge/_release/_gen_pack_manifest.py` `commit_date()` formats the date itself from `--date=raw` (epoch and offset), which reproduces the old `%cI` byte for byte on all 1,650 commits (+0000 and +0100). The committed RATIFIED v1.0.14 manifest is unchanged; the gate PASSES under git 2.34, 2.43 and 2.55.
