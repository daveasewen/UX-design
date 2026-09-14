# #271 — Ratify the atoms, widen the net: one word, a whole-library harvest, and the closing of dream pass 12

provenance: `local_65fc845a-6b17-429a-9467-930c00478fa0` · 2026-09-14
status: observed

*The WHY and HOW of session #271. The WHAT is in `knowledge/_rulings.json` (`s270-D2`, `s271-D1`…`s271-D4`),
`_LIVE-STATE.md`'s ⏱ LATEST DELTA and `GOOD-MORNING.md`'s ★ LATEST banner; this file holds the arc those
records cannot carry. Written by the delegated wrap sub at ritual step 1b. Both-way links: spine entry =
`_LIVE-STATE.md` § ⏱ LATEST DELTA #271 · ledger = `knowledge/_rulings.json` §§ `s270-D2`, `s271-D1`–`s271-D4`
· handoff = `_HANDOFF-122-ratify-the-atoms-widen-the-net.md` · Dave's words = `notes/_lanes/271/DAVE-RULINGS-2026-09-14.md`.*

---

## The shape of the day, and why it is unusual

#271 did three unrelated things and did all of them to completion: it landed a vocabulary extension that had
been waiting at the door since #269, it harvested the whole component library against thirteen external
design systems, and it closed a dream pass by enacting every one of its proposals on the same day they were
ruled. Sessions here normally do one of those and carry the rest.

The through-line is not a theme, it is a discipline: almost nothing in the day was an agent's judgement call.
The edge types landed because Dave said *"ratify"*. The stop line became one number because he explained,
unprompted, **why** 180 had replaced 150. The demo dates stayed undecided because he said they were a guess
and the record was made to say "a guess". The 115 harvest rows — the largest single body of findings the
project has produced — were built into a decision surface instead of being turned into rulings. The DO-NOT-RULE
list in the handoff is longer than the ruled list, and that is the session's actual output.

## Finding 1 — the one word, and what a closed vocabulary costs

`s270-D2` is the first extension of the knowledge-graph vocabulary since #75 closed it. #270 had built
`gen_kg_roles_desk.py`, dry-run it to 115 edges and 45 nodes, proved that `--land` refuses without a recorded
ruling id, and then deliberately stopped. That stop is why #271's opener could be a single word.

**Why it mattered that the generator refused.** A generator that *can* land without a ruling will eventually
land without one — not through malice but because a lane under time pressure reaches for the flag that makes
the red go away. #270 mutation-proved the refusal rather than documenting it, and the payoff arrived here: the
word *"ratify"* was enough, because there was nothing else to check.

**What landed and what did not.** 115 edges (`providesRole` 24 · `answersIntent` 28 · `hasDataShape` 26 ·
`yieldsTo` 37) across 26 metas, three node kinds, the `meta.schema.json` enum, a validator that resolves
against the three existing stores rather than inventing registry files, three hue variables per theme so the
new kinds render at all, and a regen to 935 nodes / 1,292 relations. What did **not** land: the `roles.json`
membership drift the landing itself re-reported — 108 memberships against 24 metas carrying `provides`, four
roles with no provider anywhere. Fixing it inside the landing commit would have put two unrelated changes in
one act, so it was reported and carried. ⚠ The three hue variables are the quiet debt: they were chosen so the
build would not render invisible nodes, and *a colour that shipped to make a build green is not a colour that
was chosen*. That is now a carry, marked Dave's.

## Finding 2 — the harvest, and the difference between a green verifier and a review

Three Opus lanes read the whole component library against thirteen external systems under
`knowledge/_RUNBOOK-external-claims.md`: 132 components, 485 verbatim quotes each under fifteen words, and a
result set that splits into 69 non-unanimous rows, 15 unanimous, 31 with no source at all, 11 findings where
`component` resolved to `null`, and 8 internal clashes.

**The correction that matters more than the counts.** The verifier went RED: 22 over-cap quotes in lane A,
five receipt mismatches, a comma-stem defect at B-24, and — the serious one — **one sentence falsely attributed
to Dave** (*"no access today"*). A repair lane fixed all of it and the record says **GREEN BY ADDITION**, not
GREEN. The distinction is load-bearing. #268's art-director clause exists because four lanes passed their gates
and failed on sight; the same shape repeated here, one layer down, inside a verifier that was itself a gate.
The lesson is not "add another verifier"; it is that a false quotation is invisible to every mechanical check
that does not hold the original beside it, which is exactly what `_quote_gate.py` (built at #269) is for and
what a harvest at this volume should route through by default.

**The finding under the finding.** Across thirteen systems, the *kind* of criterion is near-unanimous and the
*number* almost never is. Navigation breaks at five items or seven. Toasts dismiss at four, five or ten
seconds. Pie charts cap at five slices or six. This is why the 69 are Dave's and not a lane's: the external
corpus agrees on what to measure and disagrees on where to cut, and a cut chosen by averaging thirteen
opinions is a number nobody holds.

## Finding 3 — dream pass 12, and a proposal that had to be explained twice

Four proposals, four answers, and one of them arrived as *"Im not sure I understand this"*.

- **P1 → `s271-D1`.** Dave did not just pick 180 over 150; he said **why**: *"180 was decided because we use a
  sub for the wrap the 150 number was chosen before we started this strategy"*. That sentence retires 150,929
  as a figure from a different operating model rather than overruling it, which is a cleaner supersession than
  the ruling itself would have been. Enacted as one constant, `_gauge_tokens.STOP_LINE_TK`, with `_checkin.py`
  reading it and a **disagreement detector** beside the declared fallback — so a future divergence between the
  code and the chain is reported rather than silently preferred.
- **P2 → `s271-D2`.** *"yep like it"* accepted the warn arm. Whether it ever blocks was **not** asked and is
  **not** ruled, so `FILL_CEILING_BLOCKING` is False by a declared choice, not by inference. Six selftest arms,
  mutation-proven, and on today's record it reads four declared breaches and zero silent ones without a line
  of history being edited — which was the design constraint, because a retroactive rule would have fired
  twenty-one times at birth and been routed around by the second wrap.
- **P3 → `s271-D3`.** The valuable half of his answer is the hedging: *"this a guess for date 2"*. The record
  now carries "none decided", a window (w/c 09-21 or 09-28), a range for Rice (one to three weeks after), and
  the word "guess" in his own voice. Nothing may print a fixed date.
- **P4 → `s271-D4`, after a re-explanation.** The proposal was about the memory hook's "Open, Dave's" list
  being written *before* his last answers land. He did not understand it as first put; re-explained in plain
  words with the options named A / B / later, he chose **"A. re-check"**. The evidence that made it real: at
  #267 the world moved in five minutes thirty-eight seconds and two of three open items in the hook were false
  by the time anyone read them, while `_MEMORY-GRADES.json` graded the file FRESH — because `s188-D1` grades
  whether a hook's *paths resolve*, not whether its *claims are true*. The enactment's first live run
  immediately flagged the #270 hook's edge-types item, which `s270-D2` had closed that same morning. An
  instrument that catches something on its first run is the rarest kind of receipt.

**The dead end worth recording.** P4(b) — write the hook *after* the last ruling — was offered and **not
taken**. The reason is sequencing, not preference: the current write order is what makes the hook survive a
wrap that runs out of window. Moving it later would trade a stale item for no item at all.

## Finding 4 — the sheet, because he asked for it mid-turn

The v1 review page presented 115 rows and static "Your word" boxes. Dave interrupted: *"can you redraft … so I
can record my decision and notes, it's easier. can you add a side nav and filters for the reds and completed
etc"*. That is a usability complaint about a document, and the answer was to stop treating it as a document.

v2 wires every row to a real control, keeps notes per row, tracks decided/total per role in a side nav, filters
on status / most-contested / slice / role / free text, persists to `localStorage`, exports and imports JSON,
bulk-ratifies the 15 unanimous in one click, and takes j/k/1-9/r/l/d/n from the keyboard. It was driven in
chromium — persistence across reload, filter counts — and checked for zero dropped strings against v1. The
static hint boxes were removed **because a real control replaced them**, which is the only legitimate reason
to delete text Dave has seen.

★ The structural point: its **Export JSON is the input to #272's rulings**. The sheet is not a report, it is a
data-entry surface whose output feeds a generator. That is the first time a review artefact in this project has
had a machine-readable return path, and it is what makes "one ruling per decided row" a lane's work rather than
a transcription exercise.

## What went wrong, and what it cost

- **FILL.** The conductor cut the handoff at ≈195,000 real, past the 180,000 stop line ruled *that same
  session*. The wrap seat measured 206,466 — 6,466 over the 200,000 working ceiling. Both are declared, neither
  is smoothed, and both were taken on Dave's explicit *"no panic until we get to 256"*. ⚠ That sentence is
  ruling-shaped and was **deliberately not inscribed**: a sentence that reads like permission is the most
  dangerous kind to turn into a ruling from a wrap seat, so it goes to him as one word at #272's opener.
- **Boot 80,474 — a seventh consecutive breach** of a shrink-only literal, and the series is rising
  (70,260 · 70,442 · 70,717 · 71,939 · 78,777 · 79,592 · 80,474). Nothing in seven sessions has reversed it and
  no wrap may raise the number.
- **The memory store was read-only from the wrap seat again** — the #269 shape recurring. The difference is
  that this time the hook text exists in full, in the `s271-D4` form, at
  `notes/_lanes/271/WRAP-MEMORY-HOOK-DRAFT.md`, one copy away from the store, rather than being owed.
- **Two inherited double-counts stayed unrepaired**, for the reason three wraps have now given: the gauge log
  is append-only and both blocks are another session's testimony. #269's separation still holds — #264's is a
  real restatement, #243's is a mis-attribution and therefore a gate defect.

## The resolved state, and what is still open

**Resolved.** The graph has role, intent and shape atoms. The stop line is one number the machine reads. The
FILL arm and the open-list re-check exist, are mutation-proven and are advisory by declaration. The demo dates
are recorded as undecided with his hedge intact. Dream pass 12 is closed. Ten `_governs.py` evidence-pointer
reds are in legal form.

**Open, and all of it his.** The 69 harvest decisions and the 15 unanimous on the v2 sheet. The blocking tier
of both new gate arms. The three explorer node hues. The "256" clause. The 108-vs-24 `roles.json` drift. Door
v2 (handoff-121 § C). The Common Toolkit specs into `_INGESTION-QUEUE.md`. All of handoff-121 § D's remainder —
the door's step-1 switch, the `when`s onto the metas, splitting `selection-controls`, multi-select, combobox —
and every #119 open, unchanged.
