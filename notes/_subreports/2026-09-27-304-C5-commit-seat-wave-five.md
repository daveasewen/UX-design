# #304 C5 - the commit seat, wave five: W5a as narrowed by F5, W5c with the KG wiring, the Tuesday sitting page, candidate 2's runs and scores, V5, F5 and C4's final copy landed as `52049781`, pushed, CI read back; one red outside the prediction, by name

provenance: 304 · Sunday 2026-09-27 · Opus 5.5 commit seat, delegated by the #304 conductor · mount HEAD `ff382c0b` at start (the scheduled dream pass 14 commit on top of `3100da99`), `52049781` at end
status: observed - every figure below is quoted from a transcript in `notes/_lanes/304/C5/`
window: UNMEASURED (a seat cannot read its own usage)
⚠ This is the FINAL copy. The INTERIM copy rode `52049781` so doc row `W-304c5` had a home; this copy rides the NEXT commit, and with it `W-304c5`'s close condition is met.

## THE ANSWER FIRST

Wave five is one commit, **`52049781`** (799 files changed, 249,200 insertions, 640 deletions: 798 named paths + the auto-staged `notes/_REHEARSAL-LOG.jsonl`), through `_git_commit.sh` on the declared not-a-wrap path, ONE door run, exit 0, `✓ done — locks clear`. Every named path is in the commit (compared by script: 0 missing, the one extra is the auto-staged log). Push **`3100da99..52049781`** (the range carries the dream pass's `ff382c0b`, which had not been pushed), plain `git push origin master`, DECLARED, branch `master`, fast-forward checked first (`merge-base --is-ancestor origin/master HEAD` true). **`git ls-remote origin refs/heads/master` = `52049781fade1a6f464575af6ab15d457797d0cf` = local HEAD.**

CI run **`36306939769`** (one run, on `52049781`): `release` ✅ 08:41:16 UTC · `gates` ⛔ 08:50:38, steps 5 and 6 · `render` ✅ 08:54:55, verdict taken after it closed.

The wiring moved every step from old `[86]` up by four (`[86]`–`[89]` are the four new KG steps). The brief's expected numbers are in the old numbering; mapped, they are: step 5 `[132]`; step 6 reds `[81] [90] [98] [131] [132] [136]`, advisory `[138] [139] [148]`, `[151]`/`[152]` exit 77.

**Step 5: `65 pass · 2 FAIL · 6 COULD-NOT-ASK · 0 unaskable · 79 not asked`.** FAIL `[132]` memento-package delta-audit selftest (old `[128]`, expected) and **`[117]` memento index determinism check — NEW, not in the prediction.** Could-not-ask `[13] [61] [74] [140] [145] [146]` (= wave four's `[13] [61] [74] [136] [141] [142]` renumbered).

**Step 6, 152 of 152 asked, the prediction exactly by name after renumbering** (`step6parse.py`, generalised to any step total): gate reds `[81] [90] [98] [131] [132] [136]`; advisory `[138] [139] [148]`; could-not-ask `[10] [13] [61] [68] [73] [74] [140] [145] [146] [151] [152]` (`[151]`/`[152]` exit 77). **The four newly wired steps pass in both steps:** `[86]` KG token-group generator drift check ✅ · `[87]` its selftest (8 bites) ✅ · `[88]` KG node-title generator drift check ✅ · `[89]` its selftest (12 bites) ✅. `[132]` still reads `367 line(s) differ`.

Later steps: `test_gates.py` 32 tests 0 failures · `test_advisory.py` 19 cases all bite · `_git_commit.sh --selftest` 28 bites OK · `_gate_artefact_fresh.py` 7 FRESH · 0 STALE · 0 COULD-NOT-ASK · the evidence step red-and-continued at `6 lint · 0 unparsed · 3 rc/observation mismatch` (wave four: 4; W1-5 is back to `REFUSED [DOES-NOT-TERMINATE]`, the wave-three shape) · inline-style parse gate advisory, exit 0.

## THE NEW RED, `[117]`, AND ITS CAUSE

`python3 knowledge/_build_memento_index.py --check` exit 1 in step 5 (the committed tree), green in step 6 (after the build regenerates it). Cause, read not repaired: **the regen serial ran on a mount whose `_LIVE-STATE.md` carried the scheduled dream pass 14's uncommitted touch** (its "Last refreshed" stamp and a §🔀 status row, file time 06:29 UTC, left dirty by the dream pass's own commit `ff382c0b`). `_build_memento_index.py` indexes `_LIVE-STATE.md`, so the committed `knowledge/_memento-index.json` holds text the committed `_LIVE-STATE.md` does not: `grep "dream pass 14" knowledge/_memento-index.json` finds both lines; the same grep on `ff382c0b`'s index finds 0. This seat left `_LIVE-STATE.md` out as another seat's (the dream pass's) work, and so committed an index built from a tree that is not the commit's. The local `--check` read FRESH because it compares against the working tree.

**Fix for the next commit, one of two (the conductor's):** commit the dream pass's `_LIVE-STATE.md` touch with the index (it is the dream pass's own record, and `_memento-index.json` already reflects it), or restore `_LIVE-STATE.md` to HEAD and re-run `_build_memento_index.py` before committing. The class: a derived artefact regenerated over a dirty input that the commit then leaves out — every file the serial reads must be either committed or at HEAD.

## WHAT THIS SEAT DID, IN ORDER

1. **HEAD `ff382c0b` confirmed**, no lock under `.git/` before or after any step.
2. **Wiring** (`step1-wire.log`): `python3 notes/_lanes/304/W5c/tools/wire_kg_generators.py .` → `wired 4 steps + 4 GATE routes`; `--check` → already wired; `_build_all.py --selftest` PASS over 152 steps; STEPS 152, ROUTE_ROWS 152; `_build_all.py` +19 lines.
3. **Store rows minted before the first attempt** (`mint_304c5.py`, `step2-mint.log`; `_state.check()` ok, items 885 → 892): `W-304fa` (W5a's spec, title and body amended for F5's narrowing and the held-back root version, call 41c; link to the held-back patch added), `W-304fb` (W5b's spec + F5's corrections), `W-304fc` (W5c's spec from its prose, body written by this seat from the report's counts and F5's fix), `W-304v5` (V5's spec; **V5 wrote `W-304fv5`, which `ID_RE` refuses — three suffix characters — so the id is `W-304v5`**), `W-304s2` (R4s2's spec), `W-304f5` (F5's spec), `W-304c5` (this seat, interim-report pattern). **`W-304c4` closed** (`done`, `closed_by` names its final copy and transcripts riding this commit). No `DOC_ROW_ACK`.
4. **Regen serial on the mount, in order** (`step3-regen.log`, `step3-checks.log`), every rc 0 and every `--check` FRESH: `_render_rulings.py` → `tokens/_build_blast_radius.py` → `_build_memento_index.py` (2,333 records) → `_build_graph_mention_map.py` (102 of 102) → `_gen_chain.py` (7,799 tk; the verdict line reads `of 152 steps`) → `_gen_schematic.py`. `notes/_RULINGS.html` moved by its date line only and was restored from `HEAD` by `git show` redirect (no index write); `--check` FRESH after. No survey, no `_build_all.py` build on the mount.
5. **The door, one run** (`commit_c5.sh`, `paths-c5.txt`, 798 paths, every one changed-or-untracked by construction and checked by `comm` against `diff --name-only HEAD` + `ls-files --others --exclude-standard`). Doc rows PASS. `⚠ wrap gate RED — visible, not blocking: DECLARED not-a-wrap`, fails named: the boot-ceiling breach (72,768 against #297–#302) and `GOOD-MORNING.md`'s NEW-TODAY date zone. `151 dirty path(s) NOT staged`, deliberate.
6. **Exclusions by name** (declared in the message body): the four `notes/_lanes/304/W4b/*.pre-W4b.py.txt` and four `notes/_lanes/304/W3a/*.pre-W3a.*.txt` rollback copies; the dream pass's uncommitted `_LIVE-STATE.md` and `notes/_dream/_MEMORY-GRADES.json`; `notes/_dream/_GRADE-DECISIONS.jsonl`, `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md`, `notes/_lanes/294/WRAP-MEMORY-HOOK.md`, `notes/_subreports/2026-09-22-297-A-plain-deck-brain-and-footnotes.md` (other seats, `_HANDOFF-154`); the #304 side quest (`notes/_lanes/304-sq/`, its A1 report, `notes/_receipts/2026-09-26-304-sq-*`); untracked lane work under `notes/_lanes/297`–`303`. **In:** `notes/_lanes/304/W5a/held-back/` (Dave's option, call 41c); the three cand2 runs whole (`RUN-REPORT.md`, `out/`, and cand2-r2's `proof/` and `build-tools/`, 34 files, under 0.5 MB — nothing oversize; `pack/` stays out by `.gitignore:88`); R4s2 whole including `qa/`; F5's `*-W5b-original.*` copies (F5's record of what it changed, not `*.pre-*.txt`). Largest lane file under 5 MB; all lane adds together 55 MB across 733 files.
7. **The message body DECLARES** the right-gutter computation ships under ds-012(b) by reading, with the provisional PL_MAX_FRAC / PL_EDGE_PAD constants, for ratification under the sitting page's call 6; and that W5a's root trim version is held back, not enacted (call 41c).
8. **Push and read-back** as above. The push log carries no credential; the CI log's only token lines are GitHub's own `***` masks.

## CI, BY NAME, AGAINST THE PREDICTION (new numbering)

| | predicted (old → new) | CI `36306939769` | new? |
|---|---|---|---|
| step 5 FAIL | `[128]` → `[132]` | `[132]` and **`[117]`** | **`[117]` yes** — cause above |
| step 5 could-not-ask | wave four's six, renumbered | `[13] [61] [74] [140] [145] [146]` | no |
| step 6 gate reds | `[81] [86] [94] [127] [128] [132]` → `[81] [90] [98] [131] [132] [136]` | the same six | no |
| step 6 advisory | `[134] [135] [144]` → `[138] [139] [148]` | the same three | no |
| `[147]`/`[148]` → `[151]`/`[152]` | exit 77 | exit 77 | no |
| four new KG steps `[86]`–`[89]` | pass or declare | ✅ ✅ ✅ ✅ (steps 5 and 6) | new, green |
| evidence step | red-and-continued | 3 mismatches (was 4) | no |

Nothing CI reported was repaired.

## FOR THE NEXT COMMIT

**Rides the next commit:** this report (final copy, closes `W-304c5`); in `notes/_lanes/304/C5/`: `_gitcommit-C5.log`, `_gitcommit-C5.term`, `_push-C5-plain.log`, `_ci-runs-52049781.txt`, `_ci-gates-C5.log`, `ci304.py`, `cilog304.py`, `step6parse.py`, `step6-parse.txt`, and `_msg-C5.txt.t3-rendered` if the door left one.

- **`[117]` goes green only when the committed `_LIVE-STATE.md` and `_memento-index.json` agree** — see the fix above.
- The date-zone fail (`GOOD-MORNING.md`) stays on every door run today until the wrap ritual refreshes it.
- Evidence row W1-5 (`_capture_gate.py --selftest`, declared rc=0) swings between 77 and a 30 s timeout run to run; which is right is a later seat's to settle.

REPLAY-THESE: § THE ANSWER FIRST · § THE NEW RED · § CI, BY NAME · § FOR THE NEXT COMMIT
