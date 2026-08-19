# #208 — "fix the mechanical loose ends first": three dependency-ordered waves, an adversarial wave that caught its own machinery, and a re-base Dave refused to let become a target

provenance: 208 · 2026-08-19
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #208 · banner: `GOOD-MORNING.md` ★ LATEST #208 ·
ledger: `knowledge/_rulings.json` `s208-D1` · gauge block: `notes/_GAUGE-LOG.md` § #208.
Receipts, all frozen at write time: `notes/_receipts/2026-08-19-208-wave1-ci-legibility.md` ·
`…-wave2-record-hygiene.md` · `…-wave3-externality-repairs.md` · `…-verifier-wave.md` ·
`…-w44-w45-wiring.md`. Claim tables: `notes/_claims/208-wave1-claims.jsonl` ·
`208-wave2-claims.jsonl` · `208-wave3-claims.jsonl` · `208-verifier-challenges.jsonl` ·
`208-wiring-claims.jsonl`. Wrap brief: `notes/_briefs/2026-08-19-208-wrap-brief.md` (row `W-56`).*

---

## The why: an instruction that shaped the whole session

Dave opened the session's real work with one sentence, and it is worth quoting because it is not
a task list — it is an ordering principle:

> *"I want all the mechanical loose ends fixed first, plan against dependancies and externalities"*

Two words in that sentence did the planning. **Dependencies** meant the waves had to run in an
order where each one's premise was already true when it started. **Externalities** meant the
repairs whose blast radius reached outside the repair itself — review pages a human will look at,
CI jobs another session will read, records that are frozen — had to go LAST, after the cheap
internal ones had proved the method.

That produced three waves and then a fourth, adversarial one:

1. **Wave 1 — make CI legible.** Nothing downstream can be trusted while the survey is red for
   reasons nobody can attribute.
2. **Wave 2 — record hygiene.** The backlog of pointer rot, missing rows and stale assertions that
   had been carrying for three sessions.
3. **Wave 3 — externality-bearing repairs.** The review pages, the CI-visible refusal form, and the
   one finding that turned out not to be a repair at all.
4. **The verifier wave** — adversarial, run against the session's own claims, and the first REAL
   drive of the two instruments that had been sitting unwired since #205/#206.

The session's second Dave sentence set the budget shape: *"Efectivly we only have one day left use
subs and fable freely I need to cranck through some work."* Six subs ran, 931,112 tokens of quota.
That is recorded here because the licence does not make the number smaller, and quota is a
different budget from window fill.

---

## Finding 1 — the too-loose matcher was the cause of a red that looked like two reds

`[14]` had been standing red on `_governs.py`'s matcher, and `[13]` had been red-in-CI /
green-locally. The tempting repair on `[13]` is to make it green in CI. Wave 1 did the opposite:
it made `[13]` **honest in both environments**, which turned it into a `COULD-NOT-ASK` in CI — a
verdict that says "this question cannot be asked here" instead of a pass that says "asked and
answered" when it was not.

That is the same shape as `gate-cannot-pass-in-one-environment`, and the reason it is worth a
paragraph is that the honest outcome LOOKS WORSE on a badge and is better in the record. The CI
read-back on `83977f5` shows exactly that trade landing: **SURVEY 47 pass · 2 FAIL · 6
COULD-NOT-ASK**, with `[110]` GREEN and `[13]` in the could-not-ask column.

`[14]` was fixed at the **root cause** in the matcher rather than at the report. The lane also
recorded, and did not fix, a second matcher defect (NEW-4: case-blind matching) — separating "found
while fixing" from "fixed" is the whole reason the residual list is long.

## Finding 2 — the mention-map class got a gate instead of a fourth hand-repair

`[110]` had re-staled three times, each time repaired by hand, each time correctly. The fourth
recurrence was averted by gating the CONDITION (regenerate-last) instead of the instance, and by
teaching `_git_commit.sh` a mention-map freshness check paired with a regenerated-not-staged check
— because the failure mode is not "forgot to regenerate", it is "regenerated and did not stage".

This is `gate-dont-patch` applied to a class that had already earned it three times over.

## Finding 3 — the msgfile door gate, and #207's malformed subject

#207's post-wrap addendum recorded a commit whose subject came out malformed while the
subject-assert **passed anyway**. The cause is in the T3 leg: it mutated the caller's msgfile.
Wave 1 built a **msgfile-prefix door gate** (fresh `printf`, leading-stack counting, a `PREFIX_ACK`
hatch for a declared exception) and stopped T3 mutating the caller's file.

The lesson worth keeping is not the fix, it is what the assert taught: **an assert that compares
the wrong object passes on damage.** #208's wrap therefore reads its subject back from `git log`
**as TEXT**, and this session's wrap is the first commit to cross the new door gate.

## Finding 4 — the verifier caught its own machinery, which is the licence evidence

The adversarial wave returned **55 challenges → 51 CONFIRMED · 2 CONTRADICTED · 2 UNTESTED · 5
NEW**. The two contradictions are worth naming because they are corrections of this session's own
receipts:

- **`W2-20`** — the claim that a seam patch had not been applied. It **had**.
- **`W3-11`** — "non-empty open" counted as 21. It is **18 truthy**.

⛔ **The receipts were NOT edited.** They are frozen records under write-once (ADR-0017), and the
challenge rows in `notes/_claims/208-verifier-challenges.jsonl` **are** the correction. That is the
design and not an omission — but it has a real cost, recorded as a pitfall: a reader who opens the
receipt without the table gets the false claim.

The heaviest finding was the one that blocked the wiring until it was repaired: **the evidence
sampler compared EXIT CODES, not observations**, and had certified two rows whose evidence the
verifier had just proved false. `expect_stdout_contains` / `expect_count` closed it. A sampler that
grades on `rc` alone is `mutation-tests-the-clause-not-the-feature` in instrument form: it proves
the command ran, never that it observed anything.

Two further findings were **priced and not taken**, and they are carried rather than hidden:
`git show HEAD:` is a **moving pointer** (committing a claim table invalidates the table's own
evidence), and `rc` is **one scalar on a row that may cite several commands**.

## Finding 5 — the two idle instruments were wired, and the condition was met rather than waived

`W-44` (#205) and `W-45` (#206) had both been BUILT and both been left UNWIRED, by `s204-D1`'s own
rule: *not until driven in ≥1 real verifier wave*. The temptation across two sessions was to wire
them anyway, because an unwired instrument looks like unfinished work.

What actually happened is the honest sequence: **the wave ran first**, on real claims, and produced
findings including one that blocked the wiring. Then Dave said *"lets do it : W-44/W-45 — wire them
today"*, and they went in at `9d552dd` — `_build_all.py` steps 125/126/127 each with `ROUTE_ROWS`,
the linter ADVISORY in the CI gates job, the registry in the CI render job, and a
`_governs --selftest` gate.

⚠ The instruments have now run **exactly once each in CI, and that run is unread**. The wiring's
own verdict is in the two runs (`9d552dd`, `805e258`) nobody has opened; those verdicts are owed at
the #209 opener and are not invented here.

## Finding 6 — wave 3's best work was the repair it refused to make

`P-2`'s anchor-ID class went **46 findings → 0 across 7 review pages**, and — because review pages
are Dave's surfaces — the zero-visual-change claim was **PROVEN byte-identical under masking**
rather than asserted. `P-3`'s honest environment refusal was given a **legal form**: `rc=77
COULD-NOT-ASK`, with the probe registry's `verdict()` taught to read it. Before that, CI would have
read an honest refusal as a failure — the `honest-refusal-needs-a-legal-form` class, closed for
this probe.

The third finding was the interesting one. `s204-D1` had specified a filter for "rulings tagged
Dave's". The measurement at #207 was that it selects **204 of 204**; at #208 it is **205 of 205**.
There is no predicate. The field is a constant.

Dave's reaction, verbatim: *"thsiis concerning 'all 205 rulings carry Dave by construction'"* — and
the answer given was that the field is **true-but-uninformative**, which is a property of the
schema and not a fault in the record.

⛔ **The lane STOPPED rather than repairing it**, and that is the finding worth inscribing. Any
repair requires choosing what "Dave's" MEANS — which rulings are his in a sense that discriminates
— and that is a ruling, not a mechanical fix. Four options were priced instead, with A recommended
(source the Dave's-decisions view from `knowledge/_state.json`'s `owner` field). **The call is
Dave's.**

## Finding 7 — the boot re-base, and the rider that makes it not a target move

Boot had run above the `s171-D1` band (55,309–57,007) for three consecutive sessions with one
sign: #206 at 57,133, #207 at 57,903, #208 at 57,050. #206 had published its reading as "in band"
and it was not, which #207 caught.

The proposal was a re-base by the same method as `s129-D1`/`s171-D1` — an n=7 mean with a
half-range error bar wide enough to cover the whole series. Dave's answer carried the ruling AND a
condition on it:

> *"yes, re-base, same method as last time, this is fine for now, but I don't what it to go up, if
> anything i want it down, I don't want to move the goals just so the system stops complaining"*

`s208-D1` is therefore **56,749 ± 1,154** (n=7, samples #199–#208) **plus a binding rider**:

- a re-base is **measurement honesty, never target acceptance**;
- the **boot-REDUCTION** work (worklist item 24, the #110 boot-rent plan) **stays open**;
- **the next re-base proposal must arrive with a boot-reduction option priced beside it.**

That rider is the whole reason this finding gets a section. A constant that tracks the measurement
is honest; a constant that tracks the measurement *and nothing else ever pushes back on it* is a
ratchet. Dave named the ratchet before it formed. The enactment went into
`knowledge/_gauge_tokens.py` **by addition** — the `s171-D1` and `s129-D1` blocks stand untrimmed
as history.

★ And the same rule that survived `s171-D1` survived this one: **a costlier boot moves the ROOM,
never the LINE.** The 150,929 advisory stop line, `BUDGET_WORKING`, `BUDGET_AMBER` and
`BUDGET_HARD` did not move.

## Finding 8 — the session's own red, and the blind-harness class for the third time

`[16]` went red on the harness because the mention-map generator was **stubbed in the fixture**.
Third recurrence of the blind-harness class: a test harness that stubs the thing under test passes
for a reason unrelated to the thing under test. Repaired at `805e258` — generator unstubbed, **32
arms green, no gate weakened** — and the memento index rebuild cleared `[106]` with it.

Recorded here rather than smoothed because both of the CI fails on `83977f5` were **ours**, made
this session and repaired this session. A session that generates its own reds and clears them is a
different fact from a session that inherited them.

---

## Where this leaves the record

**Settled:** `s208-D1` and its rider · `W-44`/`W-45` wired with the condition met · `[110]`, `[13]`,
`[14]` no longer standing reds · `P-2` at zero across the review pages · `P-3` with a legal
refusal · the three-session record-hygiene backlog (ASSERT-001, ASSERT-009, the #204 back-link, the
`W-55` row, the argv guard, the doc-row blindspot).

**Open, and Dave's:** the one remaining `W-46` call (the mint-time brief generator) · the `s204-D1`
non-filter option call · triage of the frozen claim-table lint residuals · `s202-D3`'s
governs-nothing re-scope and the 32 slashed directory entries · the instrumentation-appends policy
(floated) · the boot-REDUCTION plan · the `W-51` promotion-vocabulary question, unchanged since
#207.

**Owed, and not invented:** the CI verdicts on `9d552dd` and `805e258`, at the #209 opener.

**Declared residuals:** `W2-13` is a dead pointer in the verifier's own table (reported, not
repaired — the file was read-only for the wiring sub) · `_validate_hit_area.py` is still an orphan
and a full build still stops there · `test_gates.py`'s a11y bite is RED at pristine HEAD,
pre-existing and untouched · `_governs` case-blind matching (NEW-4) recorded not fixed · the
doc-row matcher divergence (`_gate_doc_rows` substring vs `P-4` exact) is live · `/tmp` sits at 92%
in this sandbox and has already killed one clone with ENOSPC.
