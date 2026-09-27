# #304 C4 - the commit seat, wave four: W4a, W4b, J, the V4 report and C3's final copy landed as `3100da99`, pushed, CI read back exactly as predicted; candidate 2 built

provenance: 304 · Sunday 2026-09-27, early hours · Opus 5.5 commit seat, delegated by the #304 conductor · mount HEAD `86249459` at start, `3100da99` at end
status: observed - every figure below is quoted from a transcript in `notes/_lanes/304/C4/`
window: UNMEASURED (a seat cannot read its own usage)
⚠ This is the FINAL copy. The INTERIM copy rode `3100da99` so doc row `W-304c4` had a home; this copy rides the NEXT commit, and with it `W-304c4`'s close condition is met.

## THE ANSWER FIRST

Wave four is one commit, **`3100da99`** (530 files changed, 164,655 insertions, 296 deletions: 529 named paths + the auto-staged `notes/_REHEARSAL-LOG.jsonl`), through `_git_commit.sh` on the declared not-a-wrap path, ONE door run, exit 0, `✓ done — locks clear`. Every named path is in the commit (compared by script, 0 missing). Push **`86249459..3100da99`**, plain `git push origin master`, DECLARED, branch `master`, fast-forward checked first (`ls-remote` read `86249459` before; `merge-base --is-ancestor` true). **`git ls-remote origin refs/heads/master` = `3100da993fc5828d4ae3d9b900ff4792ae2efb88` = local HEAD.**

CI run **`36291750194`** (one run, on `3100da99`): `release` ✅ 03:34:11 UTC · `gates` ⛔ 03:43:10, steps 5 and 6 · `render` ✅ 03:47:41, verdict taken after it closed.

**Step 5: `62 pass · 1 FAIL · 6 COULD-NOT-ASK · 0 unaskable · 79 not asked`.** The one FAIL is `[128]` memento-package delta-audit selftest, as predicted. `[121]` GREEN. `[13]` COULD-NOT-ASK. Could-not-ask set `[13] [61] [74] [136] [141] [142]`, the same as wave three.

**Step 6, 148 of 148 asked, exactly the prediction by name** (parsed by `step6parse.py`, which reads C3's log to the same three lists): gate reds `[81] [86] [94] [127] [128] [132]`; advisory `[134] [135] [144]`; could-not-ask `[10] [13] [61] [68] [73] [74] [136] [141] [142] [147] [148]` (`[147]`/`[148]` exit 77, declared, build continues). `[127]` still reads `367 line(s) differ` (unchanged since wave three). Nothing new red in any step.

Later steps: `test_gates.py` 32 tests 0 failures · `test_advisory.py` 19 cases all bite · `_git_commit.sh --selftest` 28 bites OK · `_gate_artefact_fresh.py` 7 FRESH · 0 STALE · the evidence step red-and-continued at `6 lint · 0 unparsed · 4 rc/observation mismatch` (wave three: 3). **The fourth is not new substance:** `RC MISMATCH W1-5 — _capture_gate.py --selftest → rc=77, row declares rc=0`. In wave three's run the sampler drew the same row and it was `REFUSED [DOES-NOT-TERMINATE] … did not exit within 30s`; this time it finished inside 30 s and returned 77, which is `[13]`'s declared could-not-ask since W3c. The row's `rc=0` declaration is what is stale; not repaired. Nothing CI reported was repaired.

## WHAT THIS SEAT DID, IN ORDER

1. **Store rows minted before the first attempt** (`mint_304c4.py`, `_state.check()` ok, items 880 → 885, `_state.json` +93/−1): `W-304ga` (W4a, its own spec; body carries V4's unruled-thinning line), `W-304gb` (W4b, its own spec), `W-304jv` (J, owner Dave, closes on his three rulings), `W-304v4`, `W-304c4`. **`W-304c3` closed** (`done`, `closed_by` names its final copy and transcripts riding this commit). An interim copy of this report was written first so `W-304c4` had a home. No `DOC_ROW_ACK`.
2. **Regen serial on the mount, in order** (`step2-regen.log`): `_render_rulings.py` → `knowledge/tokens/_build_blast_radius.py` → `_build_memento_index.py` → `_build_graph_mention_map.py` → `_gen_chain.py` → `_gen_schematic.py`; every `--check` FRESH. Moved: `_CHAIN.md` (7,797 tk) and the schematic. `notes/_RULINGS.html` moved by its date line only and was restored from `HEAD` (no index write); `--check` FRESH after. `_gen_chain.py --selftest` all bites pass. `_drive_chart_engine.py --check` 27/27 FRESH; no receipt regenerated. No survey, no `_build_all.py` on the mount.
3. **The door, one run** (`commit_c4.sh`, `paths-c4.txt`, every path changed-or-untracked by construction; no lock present before or after). Doc rows PASS, session witness agrees, mention map and schematic fresh. `⚠ wrap gate RED — visible, not blocking: DECLARED not-a-wrap`, three fails: the boot-ceiling breach (72,768 against #297–#302) and the two NEW-TODAY date zones (`_LIVE-STATE.md` "Last refreshed", `GOOD-MORNING.md` header), as C3 foresaw. `149 dirty path(s) NOT staged`, deliberate.
4. **Exclusions by name** (declared in the message body): the four `notes/_lanes/304/W4b/*.pre-W4b.py.txt` and four `notes/_lanes/304/W3a/*.pre-W3a.*.txt` rollback copies; `notes/_dream/_GRADE-DECISIONS.jsonl`, `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md`, `notes/_lanes/294/WRAP-MEMORY-HOOK.md`, `notes/_subreports/2026-09-22-297-A-plain-deck-brain-and-footnotes.md` (stay dirty per `_HANDOFF-154`); the #304 side quest (`notes/_lanes/304-sq/`, `notes/_subreports/2026-09-26-304sq-A1-animation-storyboard.md`). C3's FINAL copy and its eight transcripts RODE.
5. **The message body DECLARES** that W4a's tick-label thinning (its existence, the 8px clearance, the anchor on the last category) is enacted WITHOUT a ruling on V4's recommendation and goes to Dave on Tuesday.
6. **Push and read-back** as above. The push log carries no credential.

## CI, BY NAME, AGAINST THE PREDICTION

| | predicted | CI `36291750194` | new? |
|---|---|---|---|
| step 5 FAIL | `[128]` | `[128]` | no |
| `[121]` | GREEN | GREEN | no |
| `[13]` | could-not-ask | could-not-ask (exit 77) | no |
| step 6 gate reds | `[81] [86] [94] [127] [128] [132]` | the same six | no |
| step 6 advisory | `[134] [135] [144]` | the same three | no |
| `[147]` / `[148]` | exit 77 | exit 77, declared | no |
| evidence step | red-and-continued | 4 mismatches (was 3) | no: W1-5 is `[13]`'s 77, which timed out last run |

## CANDIDATE 2

Built from `3100da99` with R4a's recipe at the seat, one step per call (`cand2-*.log`): `prep 3100da99…` → scratch candidate commit **`28b85afe`** over `3100da99` (VERSION/MEMENTO_CUT_VERSION v1.0.14 and the four literals swept; the skill overlay is identical to HEAD, since the skill is committed) → `full` (1.1 GB) → `probe` complete in one call, **57/57 gates** → `manifest`: 43 RUNNABLE · 10 REPO-BOUND · 4 NEEDS-DEP, 1,781 files, manifest sha256 `77ce068c3a51d852…`, differential arm ARMED → `bake` rc 0 → `check`.

- **Zip:** `notes/_lanes/304/R4a/cand/Apollo-Spider-v1.0.14-candidate-2.zip`, **sha256 `8a75ce321a0a481553d5dfbd7fc3a10b833df018624cecbe4d90bbee7aff47e3`**, 21 MB, gitignored by the existing `notes/_lanes/304/R4a/cand/` pattern (`.gitignore:86`, confirmed with `check-ignore`). The scratch original is at `$HOME/r4a-scratch/cand/out/`.
- **Contents** (the recipe's count line): 1,786 entries, reader present, 638 rulings, `brain_files 0`, `_ux_principle_nodes.json` present, 137 metas (provides 108 · when 39 · obeys 10), skill does not splice the template. The pack's `knowledge/canon/dv-behaviour.js` is byte-identical to the tree's and carries `thinLabels`, so wave four's engine is in it.
- **`--check` is RED, as R4a reported and not fixed:** `1 file(s) differ from the commit's blobs, first: ['knowledge/_rulings.json']` (the builder's Gumdrop stamp rewrites three historical rulings). Pack-docs `--strict`: 220 findings, exit 1 (advisory in the bake, same count as candidate 1). `brain_files 0` is R4a's second known gap.
- **Brief:** `notes/_lanes/304/R4c/cold/brief-candidate-2.md`, a copy of `brief-candidate.md` with only the zip path (two places), the sha256 and the run-id list (`cand2-r1`, `cand2-r2`, `cand2-r3`) changed; `diff` shows those four lines and nothing else.

## FOR THE NEXT COMMIT

**Rides the next commit:** this report (final copy, closes `W-304c4`); `notes/_lanes/304/R4c/cold/brief-candidate-2.md`; and in `notes/_lanes/304/C4/`: `_gitcommit-C4.log`, `_gitcommit-C4.term`, `_msg-C4.txt.t3-rendered`, `_push-C4-plain.log`, `_ci-runs-3100da99.txt`, `_ci-gates-C4.log`, `ci304.py`, `cilog304.py`, `step6parse.py`, `cand2-{prep,full,probe,manifest,bake,check}.log`.

- The two date-zone fails will stay on every door run today until the wrap ritual refreshes `_LIVE-STATE.md` and `GOOD-MORNING.md`.
- The evidence claim row W1-5 declares `rc=0` for `_capture_gate.py --selftest`, which has returned 77 in CI since W3c; whichever of the two is right is a later seat's to settle.
- Scratch at the seat: `$HOME/r4a-scratch/cand/` now holds candidate 2 (candidate 1's scratch was replaced by `prep`; its zip copy is still at `notes/_lanes/304/R4a/cand/Apollo-Spider-v1.0.14-candidate.zip`). Disk had 1.9 GB free after `full`; V4's 1.9 GB clone `$HOME/v4` was left alone.

REPLAY-THESE: § THE ANSWER FIRST · § CI, BY NAME · § CANDIDATE 2 · § FOR THE NEXT COMMIT
