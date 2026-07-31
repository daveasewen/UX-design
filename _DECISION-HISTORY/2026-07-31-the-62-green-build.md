provenance: session #62 (Fable solo) · 2026-07-31
status: observed

# #62 — the green build, and the gutting reattributed

**Spine entries:** `_LIVE-STATE.md` ⏱ LATEST DELTA #62 · GM ★ LATEST #62 · commits `ace3ed3`, `18c7789`.
**Brief consumed:** `notes/_briefs/2026-07-31-62-brief.md` (#61's, followed in order).

## The arc

**1. The survey ran first and immediately disagreed with its own brief.** #61 measured 2 FAIL;
the first #62 survey read **3** — `[8] _capture_gate --selftest`, exit 1, first line "Traceback".
Two standalone runs passed (EXIT=0, via `PIPESTATUS` not the pipe's code) and a re-survey
reproduced #61's exact 23/2. The failing run was the survey's FIRST subprocess in a fresh
sandbox. Chasing the cause was impossible: `_build_survey.py` keeps only the first line
matching `✗/❌/FAIL/Error/Traceback` and DISCARDS the full output — the traceback is gone.
Declared UNPROVEN, two TODOs parked (§C·4). The premise-ages lesson ran in both directions:
#61's "2 FAIL" was right *now* and wrong *at first measurement*.

**2. [10] was two correct behaviours colliding, and the fix was vocabulary.** The parser
correctly refused non-numeric testimony; #55's wrap correctly refused to invent a number for
#54. Nobody had taught the format that not-measuring is something a session may truthfully
say. Fix: `UNMEASURED_RE` scoped to the EXACT line in the record (`> **section-usage #54:**
⛔ **NOT CAPTURED — UNMEASURED.**`) — legal at the wrap gate and in the corpus reader; a
near-miss still refuses; a session may not testify both codes and UNMEASURED (refusal in both
orders); an UNMEASURED session contributes no table column and is named in notes, never
flattened into a record gap. NOT repaired data, NOT a loosened parser. 9 bites both ways.

**3. [66] was one line of diagnosis.** `--check: STALE` — #61's five commits changed the
corpus after the last index rebuild, and the write-then-check pairing (`_build_all.py:160-161`)
means CI could never have seen it. Regenerated: 365 records, current.

**4. The 45-second wall, and --range.** The full build measures ~49s (6.4 + 17.7 + 3.1 +
21.6 across chunks); the sandbox kills any call at ~45s and nothing survives a call boundary.
#47's build died at step 73 by exactly this wall. So the survey gained `--range A:B`:
consecutive chunks in STEPS order across calls — the TREE persists between calls, so the
serial build is reproduced. Out-of-range steps get their own bucket and a partial-verdict
warning, never blended into "not asked".

**5. The chunk boundary landed inside the documented wound — and reattributed it.** After
chunk 1:12, 33 compliance files were stripped of `external_automatable_refs` — the exact
shape of #61's "gutting", with every step GREEN. The diff was attributed before staging, and
`_build_all.py`'s own docstring (lines 5–21) documents it: step 1 rewrites compliance
wholesale; `verification{}` and the external refs are rebuilt by LATER steps. **The stripped
state is the intermediate of a non-atomic build. The abort never caused the gutting — it left
the window open, and a partial run (including a chunk boundary) strands the tree there. A
complete pass heals it: 29/33 healed, 4 re-dated `checked: 2026-07-31`.** #61's restore was a
correct remedy for the state and a wrong theory of the mechanism. Four sessions read the
wound; none read the docstring — read-the-runbook, again.

**6. --resume declares, never blesses.** The dirty-tree refusal fired on chunk 2 — right
guard, wrong case: the dirt WAS the prior chunk's regeneration. `--resume` continues over
exactly that state and PRINTS the dirt it resumes over, keeping damage attribution baselined
against the last commit. The plain refusal still stands and now names `--resume` instead of
silently blessing anything.

**7. The verdict, stated at its true strength.** 75/75 green at step level, on one tree, in
build order, via the same invocation `_build_all.py` itself uses (`:214` — same
`subprocess.run([sys.executable, path] + args)`). The single-process run is structurally
impossible in this sandbox; CI has no such cap. "CI green" is therefore DECLARED UNPROVEN
here — an honest residual, not a claimed green.

## Resolved / still open

Resolved: [10] · [66] · all 75 steps have verdicts · the gutting mechanism · the local build
method. Open (all parked, priced, Memento-internal — each fails "does it unblock Apollo?"):
survey persists full failure output · [8] transient cause · `_gauge_tokens.py` boot model
(prints 28,619 ± 8,000 vs the measured 61,775 constant) · the loose DO-FIRST detector
(brief item 4). **#63 opens on Apollo.**
