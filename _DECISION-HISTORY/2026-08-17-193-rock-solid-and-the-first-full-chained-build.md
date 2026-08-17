# #193 — "rock solid": the CI read-back, the third verdict, and the first full 120-step chained build

provenance: 193 · 2026-08-17
status: observed

*Links both ways: spine entry `_LIVE-STATE.md` ⏱ LATEST DELTA #193 · ledger `knowledge/_rulings.json` § `s193-D1` ·
banner `GOOD-MORNING.md` ★ LATEST #193. Written by the delegated OPUS wrap sub from the conductor's brief and the
repo's own record; ⛔ nothing here is ruled by this document.*

---

## Why the session went where it went

The opener chose #192's residual ① — the CI read-back of the first BLOCKING-var-gate chained build. That was
priced as a small read. It was not: the read-back exposed a chain of defects, and Dave's two sentences then
governed everything that followed —

> *"whatever fixes this without patching, lets wire it all properly"*
> *"okay I want this rock solid"*

Those words converted a triage into a class-fix lane. Sixteen work commits and five delegated Opus build subs
later, the session's own TITLED item — the ds-0NN chart-intent reconciliation — had never been opened. That is
recorded as a consequence of his instruction, not as drift, and the item carries forward on its own terms.

## Finding 1 — a refusal is not a failure, and the survey had no word for it

The tier- and reach-dependent gates (`[59]` `[71]` `[109]` `[112]` `[113]`) could each reach a state where they
genuinely could not ask the question they exist to ask — no browser tier, no reachable root, no fetch depth. With
only PASS and FAIL available, every such state landed in CI's FAIL column, which is a confident false claim about
the repo. The remedy was a **third verdict**: `knowledge/_could_not_ask.py`, **exit 77 plus a self-naming first
line**, wired across those gates, read by `_build_survey.py` (refusals counted, non-blocking) and by
`_build_all.py` (77 = continue). The assertion gate joined the class in the same shape at `48f545e` —
RootUnreachable is 77, an unknown root is still a FAIL, and M2 stayed intact.

The honest residual of this fix is written on the banner: each new refusal was mutation-proven in the FAIL
direction **once**, on one plant. None has yet refused wrongly, and none has been driven by a consumer that
disagrees with it. A green that has not failed is an assertion.

## Finding 2 — the evidence could be legalized without retyping anything

`s193-D1`(a): `_inscribe_ruling.py` gained a sanctioned `--amend-evidence` mode carrying the same byte-
reconstruction proof as append, with the `says` field **unreachable by construction** — the amendment can touch the
evidence array and nothing else. That let the `s176-D2`/`s178-D1` and `s175-D1`/`s176-D1` evidence entries be
given factual pointers with nothing retyped: delta-audit 8 → 0 (`f773cc2`), and the remaining five provenance
reds closed at `711bfd1`, taking the capture gate's `_governs` reds 11 → 0.

`s193-D1`(b) is the narrower half and the one most likely to be misread later: the memento-package VERBATIM SET
re-sync was **authorized once, for #193**, on Dave's explicit yes, against his own #64 release boundary. It is
**not** a standing rule and must never be quoted as one.

## Finding 3 — the fix shipped with two defects of its own, and both were found

This is the part worth remembering. The wiring that made the gates honest introduced:

1. **Unbounded recursion** in the state-contrast selftest — a planted-playwright child spawned grandchildren.
   Symptom: 40s+ and climbing. After: a 0.045s refusal.
2. A capture-gate **checkout-cannot-hold** refusal keyed on the wrong thing; it is now keyed on
   `git check-ignore`.

Both were mutation-proven in both directions (`27f5342`). The lesson is not that the fixes were sloppy — it is
that a class-fix lane is itself a change surface, and the same discipline has to be turned on it immediately.

## Finding 4 — the build had never once run to the end, so nobody knew what it would say

The chained Knowledge-build had been dying at step 8. Getting past that exposed three help-gate offenders
(`render.py`, `_recheck_119_sweep.py`, `_gate_doc_rows.py` — `3eca292`/`7b335ef`/`165f17b`) and then two debts
that were **four sessions old and invisible**: ASSERT-009 re-measured 76 → 77 metas, the 77th being
`progress-bar.meta.json` from #174 (`5e552d5`), and the KG edge gate, where progress-bar had never joined the
graph (`b83d792`). The schematic caption geometry was class-fixed for the tape tier at `23519bb`/`86c85b8`, and
the memento index plus schematic were reconciled to a fixed point twice (`b123372`/`8f41ed2`) — the "index LAST"
lesson paid, again, in one session.

**The deliverable, stated exactly:** survey GREEN (0 FAIL, honest ⊘ refusals), render job GREEN with the recursion
fix proven at browser tier, and the chained build **ran through all 120 steps for the first time in the repo's
history**. What it now reports is the STANDING 44 never-green step debt — for example `[34]`, the text/icon
contrast audit, which is red locally too. ⛔ **Full build green is a programme, not this session's claim.** The
achievement is that the build now gets far enough to tell us the truth.

## What is still open, and whose it is

- **The standing-44 debt is now visible in CI on every push.** Triage is owed, and it is **Dave's reading**.
  ⚠ Until it is triaged, every push will read "failure" — a future session must not read that as a regression.
- **ds-034/ds-035 cite gitignored `outputs/` artefacts** — permanently unverifiable from any clone. The refusal
  names it. HOME-OR-DECLARE per `s191-D2`. **Dave's.**
- **The ds-0NN chart-intent reconciliation was never opened** — carried from #192, still owed on its own terms.
- **The compliance builder is destructive run standalone** (it strips `verified_by` joins without upstream
  artifacts; the conductor reproduced it and restored via git). A guard is a priced candidate, and *"just run the
  builder"* is now dangerous out of chain order.
- **`[71]`'s browser-tier selftest arms were proven in CI only**, never in-sandbox.

## The wrap's own conditions

FILL at wrap-open was **215,597 real** — past the 150,929 advisory by 64,668 and past the 200,000 working line,
with the 256,000 wall binding. The wrap was delegated for that reason. Sub spend: **496,124 tokens, n=5,
measured**; this wrap sub's own spend is excluded and unknowable from inside. One declared incident on the commit
path: sub 3's first commit subject-doubled (the #185 class) and was repaired in-session by the documented
amend-from-a-fresh-msgfile remedy — the runbook needed no change, only obedience.
