# #163 — the provisional warn that closed through its own condition

provenance: 163 · 2026-08-12
status: ruled — `knowledge/_rulings.json` § `s163-D1`

*The WHY and HOW of session #163. The WHAT lives in `knowledge/_rulings.json` (`s163-D1`),
`knowledge/_state.json` (G18), `knowledge/_capture_gate.py` (the regex and the wired call), the
★ LATEST banner in `GOOD-MORNING.md` and the ⏱ LATEST delta in `_LIVE-STATE.md`. Both-way links:
those entries point back here; this file points at them.*

---

## 1. The session's job was a loose end that had been written down as one

`s161-D2` ratified `retired_unit_prose_audit` at WARN, and Dave said what he was doing while he did
it: *"warn but lets return to thsi soon, I dont want any loose ends"*. The wrap that recorded it did
the thing that makes a provisional ratification survivable — it opened **G18** in
`knowledge/_state.json` with an explicit close condition, *"Dave confirms warn as final or flips to
block"*, so the provisional half could not evaporate into a settled-looking record.

#162 explained the item to Dave with five measured live hits and **recommended** the flip. It took no
ruling, and its banner said so in as many words. That restraint is why #163 had a clean thing to do:
the item arrived with its evidence attached and its exit condition already written, and nobody had
quietly upgraded a recommendation into a decision.

**The finding worth keeping:** a provisional ratification is discharged **through the condition it
wrote for itself**, not by a later session judging the matter settled. Two sessions carried it, one
put it, and Dave closed it — and every step is separately readable in the record.

## 2. Three of the five hits were never the same kind of thing as the other two

The audit's five live hits looked homogeneous in a count. They were not.

- **Two were a homonym.** `duct tape` is not the retired unit `tape`. #84 had already named this as
  *"a REGEX defect … cheaply fixable, not a refutation of the design"* — and then the item sat
  parked, with the defect known and unfixed, for seventy-nine sessions. The remedy is two
  lookbehinds, `(?<!duct )(?<!duct-)`, fixing the **word sense** and nothing else: bare `tape` still
  matches everywhere it did before.
- **Three were real occurrences of the retired unit in dated prose** — the `_BANKRUPTCY-ARCHIVE.md`
  #87 batch, quoted verbatim from a triage, and the `ds-021` status block, which #84 had named as the
  audit's true positive in that file.

The second group is where the interesting constraint sits: **the remedy could not be to rewrite the
sentences.** `#82-D1` rules that dated text is not re-denominated; re-phrasing those blocks to please
a gate would have destroyed the exact record the gate exists to keep honest. So the hits were cleared
by **declaration** — a marker saying, in the region's own voice, that the unit words are the unit
that was live when the text was written. The audit is built for this: it pins **where** the words may
appear, never **how** a sentence is phrased, so a faithful declaration passes and a silent
re-denomination is what it refuses.

## 3. The parked state was the actual defect, and the flip is what consumed it

The audit had existed, tested, since #84, and had never once been able to fail: it was not called.
An instrument with no consumer cannot report anything, and a session reading the codebase sees a
function that looks like a gate. #84 named two conditions for wiring it — fix the homonym, clear the
live hits — and both were discharged in this window, in the order that makes the wiring safe: fix the
regex first (so the clearing is not doing the homonym's work), then declare the three, then wire.

The comment block at the call site records that discharge, so the next reader learns why the call
exists rather than inferring it.

## 4. What the gate still does not do — carried forward unsoftened

The scope statement is repeated in the ruling, the banner, the delta and here, on purpose:

- it covers **`tape` / `bill` only**; the retired **percentage band is OUT OF SCOPE**, blocked on
  `ds-023`;
- it catches **stale indexes, not false claims** — prose that names a retired unit, not prose that
  states a wrong number in a current one;
- the **cross-instrument claim check** remains the open successor, and it is **Dave's**. No close
  condition was invented for it here.

A gate that does not say what it excludes is read, one session later, as *"the prose is gated"* —
which is this whole thread's founding defect. Flipping the tier does not shrink the caveat.

## 5. How it was verified, and what could not be

The instrument was **driven**, not asserted: a planted undeclared `tape` line in a scratch corpus
produced exactly **one** failure, naming file, line, region and both legal remedies; removing it
produced **zero**; a control file containing `duct tape` and `duct-tape` stayed **exempt in both
runs**, which is what proves the lookbehinds fixed a word sense rather than punching a hole;
`selftest_retired_unit_prose()` passed; and the **live tree measures 0 fails / 0 warns** with the
call wired blocking. A mutation test proves the clause — so the thing was also run on the real repo.

What resisted verification, declared rather than smoothed: the **five-hit pre-fix measurement** is
the conductor's account of its own window — after the fix the tree reads zero, and a wrap sub can
only measure the tree it is given. The **gauge figures** are relayed. **Dave's words** come from the
conductor's brief, not from a transcript this sub read.

## 6. Open at the close

G18 is closed and consumed. The next session's top item is not this thread at all: the `s142-D1`
wave's **value-level aesthetic leg**, where only `tooltip` has ever been rendered and seen, and the
other 113 rows are unseen. It was deferred out of #163 by the gauge, not by a judgement — and it can
only be closed by Dave's eye.
