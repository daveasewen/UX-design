# HANDOFF → #86 · READ ONLY THIS FILE

⛔ **Do NOT read `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md` or the ledger at boot.**
This file is the whole contract for this job. It is deliberately a **prototype of the #85
proposal** — structured state, no prose to re-read — and how well it works IS a test result.

---

## RULED BY DAVE, #85 — two picks, both firm

1. **Backlog → bankruptcy, then re-open by hand.** Archive, don't delete. Items return only
   when named, and each gets a `closes_when` on the way in.
2. **Sequencing → build next session, Apollo at #87.**

⚠ Dave asked me to *explain* bankruptcy before committing, and I raised an **asymmetry he has
not yet ruled on**: work-items and queued-decisions are not the same pile. That distinction is
this session's job to measure, not to assume.

---

## THE JOB — one deliverable, then stop

Produce a **one-page tick-list** for Dave. One line per item. Nothing else.

**Step 1 · Split the queued decisions into two classes.**

- **GOVERNING** — the marker sits over code that is already written and running on a
  provisional choice. Archiving it makes a provisional value silently permanent.
- **INERT** — an open question nobody is blocked on.

Known GOVERNING exemplar, use it to calibrate: `knowledge/_capture_gate.py:1404`
— `DOFIRST_INDEX_TK_MAX` raised 420 → 700, marked *"AGENT-PICKED AND PROVISIONAL, awaiting Dave"*.
Live, in force, and would vanish under bankruptcy.

**Step 2 · Classify by reading the CALL SITE, never the marker.** A marker is a claim about
code; only the code settles it. [[instruction-right-cause-wrong]]

**Step 3 · Output.** GOVERNING items become real records with a drafted `closes_when` for Dave
to accept or strike. INERT items are listed for archive in one block, uncounted individually.

**Do NOT build the store, the graph extension or the generator this session.** That is #86's
second half or #87 — only after Dave has ticked.

---

## THE PREDICTION ON RECORD — falsify it, don't confirm it

I guessed the split is **~15 GOVERNING / ~85 INERT**. That is **a guess, explicitly not a
measurement.** If the real number comes back near 15, say so *and say it was predicted*; if it
comes back at 60, the bankruptcy ruling may not survive it and **that is a finding for Dave,
not a problem to smooth over.** [[planning-estimate-is-not-a-measurement]]

---

## WHERE THINGS ARE

| what | where |
|---|---|
| the markers to classify | `UNRULED` ×67 · `FORKED` ×24 · `awaiting Dave` ×11 · `PROVISIONAL` ×16, all in `GOOD-MORNING.md` + `notes/_MEMENTO-DECISIONS.md` — **grep for them, do not read the files whole** |
| the 19 open work-items | `GOOD-MORNING.md` § ⬛ DO THIS FIRST — retrieve via `_memento_search.py --fetch gm:DOFIRST` |
| Dave's opener list (a)–(j) | `_CHAIN.md` ★ LATEST, last bullet |
| the diagnosis | `_PROCESS-DIAGNOSIS-2026-08-02-v1.md` |
| the proposal | `_MEMENTO-REBUILD-PROPOSAL-2026-08-02-v1.md` |

---

## THE THREE FINDINGS THIS JOB RESTS ON — measured #85, do not re-derive

1. **The open-worklist is a regex over prose** (`_capture_gate.py:1401`, `DOFIRST_ITEM_RE`).
   Items have no id, no state, no age, and **no close condition**. That is the root fault.
2. **66.3% of the read chain is arithmetic about its own size; 0.0% is Apollo.**
3. **The PM layer asks a session to handle 577,343 B ≈ 144,000 tokens** — 72% of the 200,000
   working budget before any product work. Apollo has been flat at 68 components since 26 July.

---

## CLOSES WHEN

> Dave has a one-page tick-list in front of him, with every GOVERNING item carrying a drafted
> `closes_when`, and the GOVERNING/INERT count stated as a measurement against the ~15/85
> prediction.

**Not** when the store is built. **Not** when anything is archived. This item is finished at the
tick-list and no later.

---

## BUDGET

#85 closed at **166,821 real measured (84% of 200,000), conversation half only — boot half
UNMEASURED, ds-025 item 1 stands.** Amber crossed. The triage was deferred on that basis:
a declared stop, not a skip.

Price this job at the opener before starting: `python3 knowledge/_checkin.py --window 200000`.
