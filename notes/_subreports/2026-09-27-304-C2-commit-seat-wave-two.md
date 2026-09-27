# #304 C2 - the commit seat, wave two: Runs 3, 4a, 4b, 4c and the cold-run scoring landed as `4be130e5`, the two stamps as `aaf3bb7e`, pushed, CI read back: step 6 exactly as predicted, step 5 two new reds

provenance: 304 · 2026-09-26/27 (Saturday night into Sunday) · Opus 5.5 commit seat, delegated by the #304 conductor · mount HEAD `6af293df` at start, `aaf3bb7e` at end
status: observed - every figure below is quoted from a transcript in `notes/_lanes/304/C2/`
window: UNMEASURED (a seat cannot read its own usage)
⚠ This is the FINAL copy. The INTERIM copy rode `4be130e5` so its doc row `W-304c2` had a home; this copy rides the NEXT commit, and with it `W-304c2`'s close condition is met.

## THE ANSWER FIRST

The wave is committed in two and pushed. **`4be130e5`** (wave two, 879 files changed, 281,025 insertions, 949 deletions) and **`aaf3bb7e`** (the stamps, 10 files, 2,446 insertions, 20 deletions), both through `_git_commit.sh` on the declared not-a-wrap path, each in ONE door run, no lock stranded. Push **`6af293df..aaf3bb7e`**, plain `git push origin master`, DECLARED, branch `master`, fast-forward checked first (remote `6af293df` is an ancestor of HEAD). **`git ls-remote origin refs/heads/master` = `aaf3bb7e4f8a687273fb32a54f7b2e785cc72f5b` = local HEAD.**

CI run **`36275037261`** (one run, on the pushed head `aaf3bb7e`; none on `4be130e5`): `release` ✅ 22:04:40 UTC · `gates` ⛔ 22:15:45, steps 5 and 6 · `render` ✅ 22:18:15, verdict taken after it closed.

**Step 6 (`_build_all.py`, 148 steps asked) is exactly the prediction by name:** gate reds `[81] [86] [94] [127] [128] [132]`, advisory `[134] [135] [144]`, could-not-ask `[10] [13] [61] [68] [73] [74] [136] [141] [142]` plus the two new steps `[147] [148]` (exit 77, no browser in the gates job, declared, build continues). `[139]` and `[140]` green. Nothing new red in step 6.

**Step 5 (non-mutating survey of the committed tree) has TWO reds that wave one did not:** 61 pass · 3 FAIL · 5 could-not-ask · 79 not asked (the two new steps count as not asked there).
- `[128]` memento-package delta-audit selftest - predicted, not new.
- ⚠ **`[121]` read chain selftest - NEW, and this wave's doing.** The failing bite is `BUILD-STEP FIGURE IS RE-DERIVED AND MATCHES DISK (148 steps, measured now)`. Cause, read on the mount (`_diag-121-gen_chain-selftest.txt`, rc 1, the same bite): `_CHAIN.md`'s BUILD VERDICT line is generated from the run ledger `notes/_BUILD-VERDICT-LOG.jsonl`, whose newest record is `_build_survey.py` @ `e31aa34b` with `steps_on_disk: 146`; R4b took the step count to 148, and no survey has written a 148 record into the committed tree, so the chain still publishes "of 146 steps" and the bite re-derives 148. In step 6 the same bite is green because the build regenerates first. V2's clone survey could not see it, because its own survey appended a 148 record before `[121]` was asked. Remedy (not made - the survey is fenced off the mount): a survey run over the committed tree whose ledger record is committed, then `_gen_chain.py` regenerated; or the conductor's word on how the ledger gets a record at a step-count change.
- ⚠ **`[13]` capture/provenance selftest - red in step 5, could-not-ask in step 6 of the same job.** Its only line is the fixture's own `GOOD-MORNING.md: no pre-flight: stamp`, exactly the flake V2 recorded once in its clone and could not reproduce. Not this wave's (the selftest reads no changed file, V2 §1); now seen twice, in two environments, so it is a flaky step, not a one-off. Wave one read it could-not-ask in both steps.

Later steps as at wave one: `test_gates.py` 32 tests 0 failures, `test_advisory.py` 19 cases all bite, `_git_commit.sh --selftest` 28 bites OK, the evidence step red-and-continued at `6 lint · 0 unparsed · 3 rc/observation mismatch` (same as wave one), `_gate_artefact_fresh.py` 7 FRESH · 0 STALE. Nothing CI reported was repaired.

## WHAT THIS SEAT DID, IN ORDER

1. **V2's fixes and the exclusions.** Three commented `.gitignore` lines (wave one's pattern, nothing deleted): `notes/_lanes/304/R4a/cand/` (the 21.8 MB candidate zip, sha256 `2e827237…`, rebuilt by `build_candidate.sh`), `notes/_lanes/304/R4c/cold/*/pack/` (no pack folder exists on disk today; the line guards the duplicate binaries), `notes/_lanes/304/R4b/_build_all.pre-R4b.py.txt` (R4b: "Do not stage it"). `runs/_to_delete/` is already ignored by the repo-wide `_to_delete/` line and stays untracked. The largest file in the commit is the pre-existing `notes/_KG-EXPLORER.html` (4.8 MB); nothing new over 5 MB. The gen_kg_tokens debt is named in `W-304r3` (body and `closes_when`); the skill path is on `W-333`'s links with a body line, and the row stays open.
2. **The six pre-wave dirty files, by name.** RIDES: `notes/_subreports/2026-09-26-304-C1-commit-seat-wave-one.md` (its final copy, declared to ride this commit, with the C1 transcripts; W-304c1's close condition is now met) and `knowledge/_graph-mark-observations.jsonl` (the committed memento schematic counts its lines, so leaving it out would commit a schematic that disagrees with the committed log). STAYS DIRTY by `_HANDOFF-154`'s declaration: `notes/_dream/_GRADE-DECISIONS.jsonl`, `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md`, `notes/_lanes/294/WRAP-MEMORY-HOOK.md`, `notes/_subreports/2026-09-22-297-A-plain-deck-brain-and-footnotes.md`. Also left untracked: the #304 side quest (`notes/_lanes/304-sq/`, `notes/_subreports/2026-09-26-304sq-A1-animation-storyboard.md`, two `notes/_receipts/2026-09-26-304-sq-*` files), `notes/_context/2026-09-24-302-context-curve-dave-paste.md`, lanes 297-303, the nested `UX-design/`.
3. **Seven doc rows minted before the first attempt** (`mint_304c2.py`, `_state.check()` ok, items 868 → 875): `W-304r3` as its report specifies plus V2's debt; `W-304ra` (R4a), `W-304rb` (R4b, its report's spec with the id changed: `W-304r4b` is illegal under `ID_RE`, which allows two suffix characters), `W-304rc` (R4c; its report's own spec used a `doc-304-…` id and another shape), `W-304rs` (R4s, the review page as a link), `W-304v2`, `W-304c2`. No `DOC_ROW_ACK`.
4. **Regen serial, on the mount, in order:** `_render_rulings.py` → `tokens/_build_blast_radius.py` → `_build_memento_index.py` → `_build_graph_mention_map.py` → `_gen_chain.py` → `_gen_schematic.py`; every `--check` FRESH after (`step3-regen.log`). Only `_CHAIN.md` and the schematic moved. Canon, showroom, chart receipts and the explorer were NOT regenerated on the mount (R3: they are the surveyed bytes). No survey and no `_build_all.py` on the mount.
5. **The door, one run.** Every one of the 155 named paths checked changed-or-untracked first (C1's lock trap); `_gitcommit-C2.log` exit 0, `✓ done — locks clear`. Gates in the run: chain fresh, doc rows PASS, showroom in sync, polarity gate green, mention map and schematic fresh, session witness agrees; the capture gate's one fail is the boot-ceiling breach (72,768 against #297-#302 readings), `⚠ wrap gate RED — visible, not blocking: DECLARED not-a-wrap`; `notes/_REHEARSAL-LOG.jsonl` auto-staged (#261 M2).
6. **The stamps.** `_inscribe_ruling.py --set-status s245-D10 enacted --evidence-sha 4be130e5… --dry-run` then `--write`, the same for `s277-D12`; both reconstruction proofs PASSED (`step5-stamps.log`). Nothing else stamped. `_render_rulings.py` regenerated (the page went stale); `_gen_chain.py` and `_gen_schematic.py --check` FRESH. Second door run `_gitcommit-C2b.log`, exit 0, locks clear.
7. **Push and read-back** as above. Transcripts `_push-C2-plain.log` (URL without credentials), `_ci-runs-aaf3bb7e.txt`, `_ci-gates-C2.log` (the whole gates job log). Scripts `ci304.py`, `cilog304.py` copied from C1.

## CI, BY NAME, AGAINST THE PREDICTION

| | predicted | CI `36275037261` | new? |
|---|---|---|---|
| step 5 FAIL | `[128]` | `[128]` · `[121]` read chain selftest · `[13]` capture/provenance selftest | `[121]` NEW (this wave's step count, ledger not re-recorded) · `[13]` flaky, not this wave's |
| step 5 could-not-ask | wave one's six | `[61] [74] [136] [141] [142]` | `[13]` moved to FAIL |
| step 6 reach | step 148 | `[148/148]` asked | the two new steps |
| step 6 gate reds | `[81] [86] [94] [127] [128] [132]` | the same six by name | no |
| step 6 advisory | `[134] [135] [144]` | the same | no |
| `[147]` / `[148]` | COULD-NOT-ASK, advisory | exit 77, declared, build continues | as designed |
| `[139]` / `[140]` | green | green | no |

## FOR THE NEXT WAVE

- ⚠ **`[121]` stays red in CI's step 5 until the verdict ledger carries a 148-step record from a survey of the committed tree** and `_CHAIN.md` is regenerated from it. Any wave that changes `len(STEPS)` will hit this; a door gate or the step-count change itself should force the re-record.
- `[13]` is now a two-environment flake with one signature; worth a look before anyone reads it as a verdict.
- `gen_kg_tokens.py --check/--selftest` is unwired (W-304r3 names it). The pack-roster question (58 → 60 via the `_validate_*` glob) bites at the v1.0.14 cut and is Dave's (W-304rb).
- The door still sends `git add`'s stderr to `/dev/null` and strands a lock on an unchanged named path (C1's finding, unfixed); the pre-check loop worked again.
- **Rides the next commit:** this report (final copy), and in `notes/_lanes/304/C2/`: `_gitcommit-C2b.log` and `.term`, `_msg-C2b.txt.t3-rendered` if present, `_push-C2-plain.log`, `_ci-runs-aaf3bb7e.txt`, `_ci-gates-C2.log`, `_diag-121-gen_chain-selftest.txt`, `ci304.py`, `cilog304.py`. `W-304c2` closes when this copy is committed.

REPLAY-THESE: § THE ANSWER FIRST · § CI, BY NAME · § FOR THE NEXT WAVE
