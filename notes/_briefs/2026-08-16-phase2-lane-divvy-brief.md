# Phase 2 lane divvy — #187

provenance: #187 conductor · 2026-08-16 · promoted work only (`s186-D1` · `s186-D2`)
store rows: `W-19`–`W-25` (the work) · `W-26` (the compaction brief, registered) · `W-27` (this document)
status: DRAFT — lanes proposed by the conductor; Dave vetoes/reorders, he does not need to ratify

⛔ **Nothing on this page is a ruling.** Every item here was ruled at #186; this page only sequences
and assigns it. Pass 8's P1–P5 are **floated, not promoted** — they are deliberately absent and go to
Dave at the return-with-numbers, not into these lanes.

---

## Order dependency — one, ruled

`W-25` (the liveness check of the four STANDING CARRY items) runs **FIRST** — that is `s186-D2`'s own
word, not a preference. Everything after it is order-independent between lanes; within Lane C, `W-20`
should drive against `W-26`'s offender *as it was before the row existed* (the proof it can fail),
which is why the git history of `_state.json` matters to that lane.

## Lane A — ritual/runbook surface (conductor or one Opus sub)

1. `W-25` — liveness check FIRST; four STANDING CARRY items probed live-or-dead with receipts;
   the two bare ordinals **deleted, never re-stamped**.
2. `W-21` — re-checker for the 21 frozen `#119`-sweep status strings.
3. `W-23` — the two remaining stale lines in `_RUNBOOK-git-commit.md`; cite the #141 part-moot
   receipt so only the true remainder (line-7 summary + call-form block) is touched.

## Lane B — check-in machinery (one Opus sub)

4. `W-19` — the fired-compaction declared line in `_checkin.py` output. Mutation-proven: removing
   the clause must fail the selftest. Surface budget ~105 real (measured precedent, not ruled).
5. `W-22` — verify-dirties-tree over the three instrumentation appends. Mechanism only; the POLICY
   on whether they may dirty baseline stays Dave's.
6. `W-24` — expiry stamp + refusal reword. **Token-scope region byte-identical before/after — show
   the diff.** The scope itself is Dave's.

## Lane C — the gate (conductor's seat, not delegated)

7. `W-20` — new-doc-needs-a-store-row gate. Held at the conductor because a gate must be *driven to
   fail* before it is trusted [[instrument-without-a-consumer]], and the known offender's
   pre-row state lives in git history the sub would have to be taught.

## DO-NOT-RULE list (binds every sub brief cut from this page)

- ⛔ Any promotion of pass-8 P1–P5 — floated, Dave's alone.
- ⛔ The `#174` canon.css adjudication (three options delivered; he did not pick).
- ⛔ Token scopes, the 30-day AGING threshold, the grader's grading unit (pass-8 P1's two calls),
  the dirty-tree POLICY, the crank-up decision, anything marked DAVE'S in the store.
- ⛔ Push — Dave's word, never a sub's.
- ⛔ No new close conditions on `G*`/legacy rows.

## Generator regions (declare before any sub runs)

- ⛔ `_build_all.py` — **never run**, any partial run strands the tree (chain §STATE).
- `_CHAIN.md` — generated; edit `GOOD-MORNING.md`/`_LIVE-STATE.md` and regenerate.
- `_rulings.json` — written only by `_inscribe_ruling.py`.
- `_MEMORY-GRADES.json` — written only by `_gardener.py --refresh`.
- `_state.json` — written only through `_state.load()/check()/save()`.

## Consequences and pitfalls (mandatory, Dave #165)

**(a)** Lane B touches `_checkin.py`, which every session's boot depends on — a defect there is paid
at every future boot; the mutation proof is the fence, not optional polish. **(b)** `W-24`'s reword
sits one line from a region that is Dave's; the byte-diff requirement exists because a "small tidy"
is exactly how scope creep would arrive. **(c)** The residual list this plan descends from is the
surface pass-8 P2/P3 found defective — which is why every item here cites its **store row**, not its
carry-list wording. **(d)** Three lanes ≤ the 3-window cap; if run as subs, each brief carries this
page's DO-NOT-RULE list verbatim plus the generator regions.
