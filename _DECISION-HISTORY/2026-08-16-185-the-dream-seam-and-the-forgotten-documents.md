# #185 — the dream-pass seam, and the two documents nobody was carrying

provenance: local_636c11b3 · 2026-08-16
status: observed

*The WHY and HOW of session #185. The WHAT lives on the `★ LATEST` banner in `GOOD-MORNING.md`
and the `⏱ LATEST DELTA` in `_LIVE-STATE.md`; this file holds the arc, including the two things
the conductor got wrong. ⛔ **Nothing here is ruled** — `knowledge/_rulings.json` was not written
this session and no `s185-D*` exists.*

---

## Finding 1 — the opener said the dream pass was unverified, and the evidence was already on the page

The session opened by reporting that the scheduled dream pass could not be confirmed. It had in
fact **fired at 06:10Z**, and the evidence was on the check-in's **own GRADES line** — the same
output the opener had just read.

This is [[refusal-names-the-first-obstacle]] in its plain form: the refusal named the first
obstacle it met (no explicit pass banner) rather than the binding one (nobody had looked at the
line that answers the question). The conductor owned the miss in chat.

**Why the remedy is a seam and not a resolution.** "Read the GRADES line next time" is a memory
feat; a boot block is a mechanism. So `knowledge/_checkin.py` now prints a **DREAM block at boot**:
the newest proposals file, identified by mtime **and** header, plus a **git-log enact probe**,
resolving into three branches (pass ran and was enacted / pass ran and is unenacted / no pass).
It was **mutation-proven** — the pass-9 probe returns empty, so the block's empty branch is the
observed behaviour and not an assumption. Commit **`ccc3d45`**.

The wider point: pass 8 turned out to be **entirely clean** — P1–P5 all promoted at `s183-D1` and
enacted at `eaaee37`. The instrument was built on a session where the answer was "nothing is
outstanding", which is exactly when a verification instrument is cheapest to trust and hardest to
motivate. What IS outstanding is older: **pass 6 P1–P5 floated, pass 7 P1 deferred**.

## Finding 2 — DV-J2b was the next build, and it had already been ruled out of existence

The lane queue named **DV-J2b** (sparkline toggle markup + CSS) as queued work, dated 2026-07-28.
`s182-D2` (#182) had since made the sparkline **an atom alone** and moved the table CTA into a
future trend-card component that is **floated, not ruled**.

The survey-before-build habit caught it before a line was written. The lesson is the one already
inscribed: **when the queue and canon disagree, the queue is the defect** — the lane record is a
copy that rots, the ruling is the record. `knowledge/_lanes.json` is amended (state `superseded`,
step text verbatim, receipt appended with the successors named).

⚠ **And the conductor's second error is here:** it announced in chat that the lane had been marked
superseded **before the edit existed**. A statement is not a receipt [[ritual-output-is-not-evidence]].
The edit is real as of this wrap; the gap is recorded rather than quietly closed.

## Finding 3 — two documents had been sitting unread for weeks, and the reason is structural

Dave surfaced both by hand:

1. **`_MEMENTO-REBUILD-PROPOSAL-2026-08-02-v1.md`** (#85). Parts 1–3 were built — the state store
   and the generated chain. **Parts 4–5 were never done**: GM still measures **71,928 real** and
   boot **56,069**, against the proposal's promised **~2K**.
2. **`_BRIEF-compaction-strategy-2026-08-15-v1.html`**. Its **five §06 questions were never put to
   Dave at all**, only parked.

**Neither had a row in `knowledge/_state.json`.** That is the whole explanation, and it is a class
rather than two oversights: a document with no store row cannot appear on a residual carry, cannot
be aged, and cannot be closed — it can only be remembered, which is the mode this whole system
exists to stop relying on. Call it the **forgotten-document class**.

The remedy proposed for Phase 2 gates the **presence**, not the drift: any new proposal / brief /
research doc must carry a store row, or a declared "receipt-only, closes never" stamp
[[gate-inside-the-growth-loop]].

## What landed as a result — the close-out programme

Dave approved the programme in chat: ***"okay sounds good … go for it"***. That is approval of a
SHAPE, not of its contents, so the plan is inscribed at `status: standing` and every verdict inside
it stays open for the Phase 1 sitting. Three phases: **1** words-only ruling sitting · **2**
enactment crank including the store-row gate · **3** rebuild parts 4–5, timeboxed to one session
and **dropped rather than carried** if unfinished.

Two store rows were opened through `_state.add()` — the gate's own writer, never a hand-guessed
schema — each with a `closes_when`, because the store refuses an item that cannot end: **`W-17`**
(rebuild parts 4–5) and **`W-18`** (the compaction five questions).

Three externalities were deliberately written as **dated returns rather than open items**: the B3
return-with-numbers after the 2026-08-23 pass, the AGING-grade half after five weekly cycles, and
compaction Q3 when compaction is live. An item that cannot act until a date is not a carry; making
it one is how residuals grow without anything happening.

## The small one — a commit subject that doubled

The wrap's msgfile headline carried its **own** `#N <date> — ` prefix; T3 generates the session
prefix itself, so `git log` came out with the subject twice. Repaired by amending from a **fresh**
msgfile (`ccc3d45` is the amended result — the stale-msgfile trap avoided by never reusing one).

Inscribed the same session, into `knowledge/_RUNBOOK-git-commit.md` step 3, because the repair is
worthless as a memory and cheap as a rule.

## Resolved state, and what is still open

**Resolved:** the dream-seam block exists and is committed; pass 8 is confirmed clean; DV-J2b is
marked superseded; the close-out plan and its two rows are inscribed; the runbook line is added.

**Open, and all of it is Phase 1's:** compaction Q1/Q2/Q4/Q5 (Q3 parked with a trigger) · dream
pass 6 P1–P5 · dream pass 7 P1 · ratification of `W-17`/`W-18`'s close conditions. **Open and
not Phase 1's:** the `#174` adjudication, the trend card, and every carry on the #185 residual.
