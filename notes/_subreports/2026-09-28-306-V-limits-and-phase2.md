# #306 lane V — the eleven limits adopted (s306-D10), and phase 2 built: the summary at the push, one CI wait

session: `#306` · 2026-09-28
window: lane V (Opus 5.5, at Dave's seat through device bash)
sub index: `V`
brief: the conductor's launch message (verbatim in the conductor's transcript); Dave's words it relays are held at `notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md`
provenance: 306 · 2026-09-28
status: observed
tokens: UNMEASURED — this seat cannot read its own transcript while it is still growing

His words, 16:58 BST, verbatim: "go on both", to the conductor's "1. Adopt the proposed limits into the design? … 2. Build phases 1 and 2 now …".

## VERDICT

DONE. `s306-D10` is inscribed, status `ruled` (711 → 712): all eleven limits from lane U's report § 3 are adopted into the design, each named with the phase that enacts it. Phase 2 of the wrap redesign is built and wired, not yet proven: a permanent CI read-back tool, a new runbook order with one CI wait and the summary at the push, and a blocking wrap-gate arm for the handoff's `CI owed:` line. `s306-D7` stays `ruled` until tonight's wrap runs in the new order. Nothing was pushed.

COUNTS: rulings inscribed `1` · new tools `1` · gate arms added `1` · selftest bites added `25` (16 + 9) · build steps `154 → 155` · UNPROVEN `2`

## 1. `s306-D10`, what it says

The eleven limits are READ from `notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md` § 3 by `notes/_lanes/306/V/build_entry.py`, never retyped, and each carries the phase named in the report's own parenthesis:

| phase | limits (U's numbering) |
|---|---|
| 2 | 8 — the opener's CI read prints the run summary only, never the gates log |
| 3 | 2 (handoff ceiling, handoff counted in the boot figure), 6 (chain takes nothing new), 7 (freshness arm checks the newest wrap only), 11 (one memory note per wrap) |
| 4 | 9 — one-line returns for the story and mechanics seats; one shared brief |
| 5 | 10 — the full carried list generated on read, never committed; `_CARRIES.md` grows at most 20,000 B a wrap |
| 6 | 1 (draft never on the boot chain), 3 (one tally block, replaced), 4 (his words verbatim, exports cited by path), 5 (the seam prints one line) |

The question said "phases 3 and 6"; that holds for eight of the eleven, and the ruling says so. `says` quotes the question and "go on both" verbatim (chat #306, Mon 2026-09-28 16:58 BST). Dry run then write, reconstruction proof passed both times (`notes/_lanes/306/V/inscribe-dry.log`, `inscribe.log`). The scheduling half ("build phases 1 and 2 now") is not a ruling: it is on `W-305wr` by addition.

## 2. Phase 2, what changed

**(a) `knowledge/_ci_readback.py` (new).** Modelled on `notes/_lanes/305/C1/ci305.py`, `cilog305.py`, `_ghtok.py`. `--sha <sha-or-ref>`, `--owed`, `--poll SECONDS` (≤170, one tool call), `--selftest`. It prints per run: id, workflow, status/conclusion; per job: status/conclusion and failing step names; and only for a failed job, the blocking lines parsed out of its log (≤12 per failing step, 220 chars each, timestamps stripped). The token comes from `git credential fill` and is never printed; the log endpoint's redirect is fetched without the Authorization header. Exit codes 0 green · 1 red · 2 running · 3 no run · 5 API unreachable. argparse, so the help gate is satisfied.
- **Live reads at the seat:** `3b4cae5d` → GREEN, rc 0 (4 lines). `dcb76d81` (the red of today's P lane) → RED, rc 1, 1,391 bytes (`notes/_lanes/306/V/live-read-dcb76d81.txt`), naming `❌ [88] KG node-title generator drift check` and `[88/154] … → ❌ KG node titles are STALE (exit 1)`, against a gates log of ~505,663 bytes (`notes/_lanes/306/P/_ci-gates-P1.log`).
- **One parser lesson, found live and fixed before commit:** in a CI log, `_build_all.py`'s children's output is interleaved with its own buffered prints, so a child's `❌`/`⛔` line lands under whatever `=== [i/N]` header precedes it (the evidence linter's `⛔ EVIDENCE GATE FAIL` printed under step [74]). Inside a build step the parser now keeps only the build's own verdict lines (`❌ … (exit N)`, `❌ step … failed`, `❌ build gate failed`). Bitten.
- **Why `--owed`:** the 5b addendum is committed in the 5b commit, and a commit cannot carry its own sha. So the handoff line names `--owed`, which resolves the sha as the last commit that touched the newest `_HANDOFF-*.md` (by number, not string). `--sha <hex>` stays legal for any other case, and the conductor says the 5b sha in chat.
- **Registration.** The house rule for a new `knowledge/` tool's selftest is a `_build_all.py` STEPS entry plus an exact-label ROUTE_ROWS row in the same edit (the `_gm_move.py` / `_roll_state.py` precedent), ABORT tier. Done, appended LAST so no step number moves: step 155, "CI read-back selftest — canned API JSON, no network; the token never printed (s306-D7, built #306)". `_build_survey.py` picks it up as a non-mutating `--selftest`. `_validate_wiring.py` does not apply (its population is `_validate_*`/`_gate_*`). No ds-021 declaration: it counts no tokens.

**(b) `knowledge/_RUNBOOK-capture-ritual.md`, by addition.** A new block `### ★ THE ORDER AFTER THE COMMIT — ONE CI WAIT, THE SUMMARY AT THE PUSH (s306-D7 …)` before § FILED SUB-REPORTS; steps 5, 5b, 5c are left as written, the 5c precedent. The old second wait is written struck through beside it: it lived in the wrap briefs and the handoffs' 5b addenda, never in this runbook. **The new order in one line:** 5 commit + push → read the wrap commit's CI (`_ci_readback.py --sha <wrap sha> --poll 170`, the one wait) → 5c summary to Dave → 5b addendum with the wrap CI verdict and the `CI owed:` line → commit + push the 5b, no wait → 4c last → the next opener reads the owed CI. `knowledge/_RUNBOOK-git-commit.md` step 5 gains one paragraph by addition: the 5b push is the one timing exception to `s203-D1`'s read-back in chat.

**(c) The opener line.** There is no handoff template file (handoffs are hand-written per wrap brief), so the handoff carries the line through the runbook's 5b beat, and the gate enforces it: `_capture_gate.py::ci_owed_check`, wired in `wrap_checks` for plain and lane wraps, BLOCKING in wrap mode (`CI_OWED_BLOCKING = True`). From `_HANDOFF-157` on, a newest handoff with a `POST-WRAP ADDENDUM (5b)` heading must carry, inside that section, `CI owed: … _ci_readback.py --owed` or `--sha <hex>`. It binds on the 5b commit's committer run; before 157 it is out of scope by date and says so. On today's tree it notes `_HANDOFF-156 … NOT graded`.

**(d) Any arm that required the second CI read.** None. `_capture_gate.py` does not read `_HANDOFF-*.md` or any CI result anywhere (grep for `ci-runs`, `read-back`, `actions/runs`, `s203-D1`: no arm). `_git_commit.sh` does not either. The second wait was practice (wrap briefs, handoff addenda, `s203-D1`'s chat read-back), never a gate. So nothing needed relaxing; the adjustment is the new arm, whose bites prove the new order passes and the old failure class fails.

## 3. Selftests

- `python3 knowledge/_ci_readback.py --selftest` → PASS, 16 bites. Meta-mutation at the seat: three mutants (indented `❌ FAIL` read as a verdict; the token sent to the redirect host; a log fetched for every job) each turn at least one bite red.
- `python3 knowledge/_capture_gate.py --selftest` → rc 0 in 141 s, "all failure classes bite; green control passes", 9 new `ci-owed` bites among them: no handoff ⇒ SKIPPED not a pass · 156 out of scope · 157 with no 5b ⇒ nothing owed · NEW ORDER green control · `--sha <hex>` legal · OLD FAILURE CLASS (5b with no owed line) ⇒ FAIL naming the runbook · placeholder `--sha <sha>` ⇒ FAIL · the line under a later heading ⇒ FAIL · newest by number (157 over 99).
- `python3 knowledge/_build_all.py --selftest` → PASS over 155 steps.
- `python3 knowledge/_validate_wiring.py` → rc 0. `python3 knowledge/_validate_help_gate.py` → its one red is `knowledge/_tmp/wrap261/carry262.py`, gitignored (`.gitignore:79`), not in CI and not this lane's.
- Store, regen and gate: in the commit's own log, `notes/_lanes/306/V/`.

## 4. The sentence Dave could add to the Project instructions (a suggestion; his text, not edited)

At the end of step 1: "In the same shell call, also run python3 knowledge/_ci_readback.py --owed; it prints only a short CI summary for the commit the last wrap pushed without waiting, and a red there is the session's first beat."

## UNPROVEN, named

1. **The new order on a real wrap.** Tonight's wrap is the first. `s306-D7` stays `ruled` until then; the proof is the minutes from launch to his summary (about 59 at #305) measured again.
2. **`--owed` on a real 5b commit.** Driven only on a fixture repo and on today's tree, where it resolves `fe780924`, which was not the tip of its push and so has no run of its own ("NO RUN YET … or it was not the tip of its push"). The 5b commit is its push's tip, so it will have a run.

## Also noted

- The evidence step (`_validate_evidence.py notes/_claims`) ends `##[error]` on every run but the job does not fail on it; the tool prints it under the failed job because the log alone cannot map a section to the API's step conclusion. About 3 lines.

REPLAY-THESE: `python3 knowledge/_ci_readback.py --selftest` · `python3 knowledge/_ci_readback.py --sha dcb76d81` · `python3 knowledge/_ci_readback.py --owed` · `python3 notes/_lanes/306/V/build_entry.py`
