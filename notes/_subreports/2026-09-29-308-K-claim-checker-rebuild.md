# #308 lane K: the claim-table checker, rebuilt (s308-D29)

COUNTS: rulings inscribed 1 (s308-D29) · rows minted 1 live (W-308k1) + 1 doc (W-308k2) · rows noted 1 (W-308c3) · red rows re-judged 9 (10 with L1-1 twice) · now pass 6 · declared 3 · could-not-ask 1 (WIRE-20) · lint fail 0 · mismatch 0 · selftest arms added 6, each with a planted red · wall at the seat 14.1 s (was 38.6 s) · selftest 2.2 s · commits 2 · pushes 0

## What Dave ruled, and what was recorded
- Call 1 is inscribed as **s308-D29**: "(a) and (b) together", which was not the recommendation. His words are quoted verbatim in `says`, including "Lets do this properly, I'd rather rebuild than patch". The build row is **W-308k1** (live, owner claude). It closes when the rebuilt checker exits 0 over `notes/_claims` at the seat and also in CI's advisory step, read back after a push.
- Call 2 (make the step blocking) is **not ruled**. It is a dated note on **W-308c3**: he chose blocking, asked for the implications, and got the conductor's answer in chat (one advisory CI run first, then blocking). His confirmation is owed. `continue-on-error` is untouched in `.github/workflows/gates.yml`.
- On "you can still argue the other way": the measurement does not argue for it. The rebuild made the step cheaper, not dearer (14 s against 38 s).

## Per-row verdict (at the seat, 96bd905e)
| Row | Table:line | Before | Now |
|---|---|---|---|
| L1-1 (claim) | 204-buildpm:10 | dead pointer | PASS. `tokens/_blast-radius.json` is quoted from `_build_blast_radius.py`'s output and resolves against the tool's base, as `knowledge/tokens/_blast-radius.json` at 541ffcc3 |
| L1-1 (challenge) | 204-verifier:17 | dead pointer | PASS, the same way |
| W2-13 (challenge) | 208-verifier:29 | dead pointer (truncated) | PASS. The row says "a path that does not exist", so it is judged as an absence, and it is absent at 9d552ddc |
| WIRE-14 | 208-wiring:14 | observation mismatch (166 ≠ 127) | PASS. Re-run at 9d552ddc, it prints "127 steps" |
| WIRE-21 | 208-wiring:21 | observation mismatch (4 ≠ 3) | PASS. Re-run at 9d552ddc, the count is 3 |
| WIRE-20 | 208-wiring:20 | passed at the seat, rc=77 in CI | COULD-NOT-ASK, at the seat and in CI alike. `_governs.py --selftest` at 9d552ddc answers rc=77: three evidence pointers name paths a checkout cannot hold (ds-034's `outputs/…`, which is gitignored) |
| L1-4 | 204-buildpm:13 | s182-D1 | DECLARED (its evidence is row L1-3) |
| C-2 | 204-verifier:29 | s182-D1 | DECLARED (its evidence is bare counts; see finding 3) |
| H-5 | 204-verifier:55 | s182-D1 | DECLARED (its evidence is rows C-6 and L1-10) |

Also in the draw: W1-5 (`_capture_gate.py --selftest`) was a 30 s timeout refusal at HEAD. At 9d552ddc it answers rc=77, so it reads COULD-NOT-ASK. The 8 policy refusals (SIDE-EFFECTS or UNSAFE) are unchanged by design.

Whole run: `0 lint fail · 3 declared · 0 mismatch · 2 could-not-ask · 8 refused by policy · wall 14.1 s`, exit 0. The comparison run with `--at-head` (the old reading, which keeps the other fixes) gives `0 lint · 2 mismatch (WIRE-14, WIRE-21) · 47.3 s`. That is part (a) doing its job.

## What was built (`knowledge/_validate_evidence.py`)
1. **Judge at the commit (a).** `History` runs `git blame --porcelain` per table, per line, because 206-w45 was written in two commits. Pointers resolve in `git ls-tree -r -z <sha>`, one call per commit and cached (the same answer `cat-file -e` gives, without a call per path). A sampled command is re-run in that commit's tree. A row not yet committed, a table outside the repo, or a machine with no git is judged in the working tree, as before. A shallow checkout makes the whole gate COULD-NOT-ASK (77), because blame there would name the boundary commit. `--at-head` gives the old reading.
2. **Not `git worktree add`.** It writes `.git/worktrees/<id>/` inside the repo, and `worktree remove` or `worktree prune` must unlink it there. The mount refuses deletes (checked: `rm` in `outputs/308/K/` gives "Operation not permitted"), and that is the stranded-`index.lock` class. So the tree is a `git clone --shared --no-checkout` outside the repo, which borrows the objects read-only. It is checked out detached, commit by commit, cleaned between commits, and removed whole at the end. Every write-side git call is guarded so it can only run inside that clone. Cost: clone 0.07 s, checkout 0.85 s, about 94 MB per tree.
3. **Where the tree goes.** TMPDIR if it is set, else /dev/shm, else the system temp, whichever first has room. The brief asked for $HOME, but $HOME on the seat measured **126 MB free at 99 % use**, and one tree is 84 MB. No candidate with room means COULD-NOT-ASK; nothing ever writes a partial tree. Re-run commands get their own TMPDIR, which is removed afterwards. Old selftests, including this file's pre-#308 one, used to leave scratch directories in /dev/shm on every run.
4. **Environment is COULD-NOT-ASK, never a mismatch** (`env_failure`). There are exactly four environmental readings: rc=77 from the command itself; rc=126 or 127; a `No module named 'x'` where x is *not a file in that commit's tree*; and a timeout. A verb missing from PATH also reads COULD-NOT-ASK. A local module that fails to import stays a MISMATCH, because that is the code's own defect at that commit. These rows are counted and printed apart, never as a pass.
5. **Tool-relative paths.** A backticked span that is not a command, and comes after a command span, is that command's output. A path in it that fails at the root is tried against the tool's own directory and then its ancestors, nearest first. A path the writer typed in prose never gets this fallback.
6. **Absence in words.** "`<path>`, a path that does not exist" (anchored at the pointer, a narrow grammar) is judged as `absent:`. A quoted error message that merely contains "does not exist" further on (W3-18) is not a claim about the path. The selftest carries that case as a control.
7. **Declared notes (b).** They live in a sidecar, **`notes/_claims/_declared-notes.jsonl`**, and are never written into the tables. Why the sidecar: the tables are dated records (ADR-0017 rule 3). A line appended into one would change its blob, so "byte-identical to what the wave wrote" would stop being provable by git, and it would need a new `kind` in the shared `_claimtable` schema. The sidecar is the notes' one home (rule 1). Each note has an address (table, line, id, kind) and a resolver that landed with it (rule 2): an address that does not resolve is a **hard fail**. A note excuses only the token-less (s182-D1) class. It cannot excuse a dead pointer or a mismatch. It is counted and printed as DECLARED. The file is append-only, and the directory scan skips it.
8. **Selftest, six arms**, each driven in a throwaway two-commit git repo, each with a planted red: judge-at-commit (J-1 passes, fails `--at-head`; planted J-2 and J-3 bite); environment (a missing dependency, rc=77 and a timeout read COULD-NOT-ASK; planted rc=1 and a broken local import stay mismatches); absence in words (planted A-2 on a present path is FALSE ABSENCE); tool base (planted T-2 dead in output and T-3 in prose bite); declared note honoured and counted (planted N-3 dead pointer under a note, N-9 stale address); undeclared token-less row still refused (N-2). All the old arms are still green.

## Findings
1. **The brief's pack premise is stale.** `_validate_evidence.py` does **not** ship in the designer pack. s219 Q6 dropped it as REPO-BOUND, taking the roster from 57 to 55 (`knowledge/_release/_pack_manifest.json`; `_pack_gate_probe.json` verdict REPO-BOUND, exit 77, local imports `_claimtable`, `_could_not_ask`, `_helpgate`). The change adds no local import, and a bare call with no `notes/_claims` still answers 77 before any git call. So no receipt refresh is owed. There is no copy under `memento-package/`.
2. **Two comments are now false**, but I did not edit them: `.github/workflows/gates.yml` around line 293 and `knowledge/_build_all.py` around line 599 still say the frozen tables "carry 6 lint failures + 3 rc mismatches". They belong to the commit that flips the step to blocking.
3. **C-2's pointer is real, but written as a bare file name.** `_REVIEW-SIGNOFF.md:299` is `knowledge/_REVIEW-SIGNOFF.md`, and at 541ffcc3 line 299 does carry "ALL SIX SHIP `PROPOSED`, NOTHING HERE IS RULED" (checked by hand). The path grammar reads only `knowledge/|notes/|…` prefixes, so bare names are invisible. Its note says this plainly. Resolving bare file names would be a further class fix, and I did not build it: it would widen the pointer set across all 336 rows.
4. **A residual false-red risk.** An old command that runs but behaves differently under today's Python or a newer dependency, without one of the four readings, would read as a MISMATCH. None does today.

## Is blocking now safe? My judgement
Yes, after one advisory CI run is read back. It is not safe before that run, because CI has not yet run this code. Seat and CI now judge rows in the same commit tree, so the one known difference between them (WIRE-20) reads the same in both. The frozen tables can no longer go stale, and environmental failures cannot turn the gate red. What would turn it red is a real mismatch or a new token-less row. What remains is Python 3.10 at the seat against 3.12 in CI, and the step's time in CI, which is not yet measured.

## Commits (not pushed)
- `96bd905e`: s308-D29, W-308k1, the note on W-308c3, the checker, the sidecar, Dave's rulings file, and the regen.
- This report: see the second commit.

Housekeeping: `outputs/308/K/_deltest` is an empty file left by the delete test. It is gitignored, and delete is off.
