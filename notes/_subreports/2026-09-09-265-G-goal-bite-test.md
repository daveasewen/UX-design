# `#265`-`G` — the `/goal` bite-test: the clause bites on HOLD, not on CONFIRM

session: `#265` · 2026-09-09
window: conductor (Fable) + two Opus driver lanes, blind to each other and to the repo
sub index: `G`
brief: none filed — ruled *"do it"* at the #264 opener, carry `residual → #265` item ①
tokens: drivers 48,453 + 49,700 real (Agent `usage`); conductor share UNMEASURED at filing — `_checkin.py` at the seam

## VERDICT

DONE. `knowledge/_bite_goal.py` emits two boots — INTACT `COPILOT-BOOT.md` and a MUTATED copy with
option 3's `/goal` clause stripped (the 5-line "Take it the way Claude Code takes `/goal` … list of
tasks." span; the strip is asserted) — plus a 4-turn scenario. Two blind Opus lanes each played the
assistant from ONE boot. Grading the transcripts: **INTACT GREEN (2/2 counted), MUTATED RED (1/2)** —
the clause bites, and it bites on exactly one arm: **G2, holding the goal against a drift**. With the
clause, T2's "just build me a transactions list" was checked against *make rent* by name and
re-shaped; without it, the list was built. G1 (confirm before build) passed in BOTH arms — it is not
this clause's, it is rule 7a's bento question. G3 (report against the goal) cannot be told apart
by regex — both arms name the goal at T4 — and is demoted to ADVISORY, a rubric item for a reader.

COUNTS: findings 3 · ruling-shaped 2 · UNPROVEN 2

## What was done

1. `knowledge/_bite_goal.py` — `--emit DIR [--mutate]` / `--grade transcript.json`. Mutation is
   a span cut with an assertion that `/goal` is gone from option 3.
2. `notes/_lanes/265/{intact,mutated}/` — `boot.md`, `scenario.json`, `transcript.json` from the
   lanes. Copied VERBATIM to this report's assets with both grade outputs.
3. `claude -p` in the sandbox → `terminal_reason: api_error` (no auth), so the driver is an Agent
   lane, not a script. The harness is driver-agnostic; only the driving is not yet scriptable.

## Findings

1. **The clause is load-bearing for HOLD only.** Probe: `grade-intact.txt` G2 PASS vs
   `grade-mutated.txt` G2 FAIL. Intact T2: *"One check against the goal, then I'll do as you say
   … It does not answer 'will I make rent this month' at a glance"* — then two priced options.
   Mutated T2: *"The shape I'd build: the answer on top, the list under it … Say go and I'll build
   it."* — the drift absorbed, never named as a drift.
2. **Confirm-before-build is NOT the clause's.** Both T1s end in *"Dashboard bento — is that
   right?"* — rule 7a fires regardless. If the clause were deleted, nothing in the confirm step
   would notice. G1 stays counted because it is what s262-D5 says, but it does not discriminate.
3. **"Against the goal, not a task list" is un-regexable, and the transcripts show why.** Intact
   T4 opens *"Against the goal — … The answer reads at a glance — not yet."* (progress as met /
   not-met). Mutated T4 opens *"Where we are: 1. Goal stated 2. Page built …"* (a done-list that
   happens to name the goal). A reader tells them apart in one glance; `GOAL_TERMS` cannot.
   Demoted to advisory with the reason in the source. [[no-gate-parses-the-artefact]] holds
   even for a transcript — halfway.

## RULING-SHAPED QUESTIONS

1. **Does this bite-test join `test_gates.py` CASES, or stay a standalone instrument?** (a) join —
   but CASES needs a scripted driver, and the sandbox has none (api_error), so in CI it would be
   a `fresh_copy` + emit + a driver that does not exist; (b) standalone, run by a lane at each
   release that touches `COPILOT-BOOT.md`, receipts filed. Recommend (b) until a driver with auth
   exists; a case that cannot run in one env is the [[gate-cannot-pass-in-one-environment]] class.
2. **Is G3 accepted as rubric-only (a reader grades T4), or is `/goal`'s "report against the
   goal" accepted as unenforceable guidance?** Recommend rubric-only: the assets carry both T4s,
   and one glance grades them.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** stability — ONE drive per arm. A second pair would cost ≈100K sub tokens. The
  G2 split could be sampling; the two T2s read like different rules, not different dice, but that
  is a reading.
- **UNPROVEN:** a Copilot (the real host) behaves as an Opus lane did. The boot is written for
  Copilot; the driver was Claude.
- **CLAIMED:** `claude -p` has no auth in the sandbox — one probe, `api_error`, not diagnosed.

## Evidence

`notes/_subreports/assets/2026-09-09-265-G-goal-bite-test/` — `intact/` and `mutated/` each hold
`boot.md` (the exact instructions the lane read), `scenario.json`, `transcript.json`;
`grade-intact.txt` GREEN, `grade-mutated.txt` RED. Replay:
`python3 knowledge/_bite_goal.py --grade notes/_subreports/assets/2026-09-09-265-G-goal-bite-test/mutated/transcript.json`.
