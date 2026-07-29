# Present-but-unkeyed — a filing error, not a vocabulary gap

```
provenance: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367 · 2026-07-29
status: ruled → notes/_MEMENTO-DECISIONS.md § ★ #43
```

*Session #43, 2026-07-29 (Wed evening), Opus solo, Dave live. Small-bite window by Dave's #42
ruling — "small bites, fresh window often, small big wins first" — and it landed deliberately
under the 45–60 band. Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta. Ledger: `notes/_MEMENTO-DECISIONS.md`
§ ★ #43. Enactment: `cd75caf`.*

---

## What this session was opened for, and what it turned out to be

Opened as a cold boot with `_CHAIN.md` and a single question on the board: **#41's 2f fork** —
*"why should the stratum retire?"* — carried into §C·4 as open 7, and marked urgent by a measured
claim that the read chain had **eighteen tape** of headroom left, with `roll_2f` as its only relief
valve.

It became something else within two probes. **The fork's urgency was already false, the fork's
factual premise was already false, and the false premise turned out to be one this project had
now repeated three times.** The window's actual product is one key, one ruling, and three
withdrawn claims.

---

## Finding 1 — the urgency had already expired, and the file says so twice

The chain's own generated text carries **three different figures for itself**: `3,721` in the
footer, `4,482` in the ★ LATEST banner ("EIGHTEEN TAPE"), and `3.7K / 783 under` in the header.
Measured with `tiktoken cl100k_base` at this session's open: **4,119 tape, 381 headroom.**

The header line actually resolves the contradiction if read closely — *"and it was EIGHTEEN
before this wrap's 2c/2d rolls"* — so #42's own rolls bought the headroom back. But the banner
sentence that propagated forward, and that framed open 7 as *the chain's sole source of headroom*,
was written before the rolls and never re-priced after them.

**The lesson is not that the number was wrong.** It is that a banner statement about a *moving*
quantity is a reading with a timestamp, and reading it later as a fact is the standing failure this
project already has a name for — [[premise-ages-faster-than-rule]]. It bit twice more the same
window: `_to_delete/` was claimed at **840K** by #41 and measured **0**; the tree was claimed
*"seven commits local, unpushed"* and was in fact fully pushed to `origin/master`.

⇒ **three aged premises in one short window, all inherited from a handoff written six hours
earlier.** The rate is the finding, not any one of them.

## Finding 2 — the third propagation of a sentence that never said what three sessions read

The 2f fork rests on this: *#38's row is missing from `notes/_GAUGE-LOG.md`.* Against that,
#39 had written, in the log itself:

> *"What is actually missing is only its gauge-log block, now supplied by this line."*

I read that as discharge and told Dave so: *"#38's gauge-log half is not missing, it's unkeyed."*

**It is not discharge.** That sentence is about the **HOLE's status** — #39 withdrawing its own
`HOLE #38` declaration — and says nothing about #38's measurement. #41 had already caught this,
and logged it as its own error (ii): *"an unchecked PRESENCE claim, the mirror of
[[unmatched-grep-is-not-an-absence]], and it had already propagated through #40's fork before I
repeated it."*

So the tally is: **#40 misread it · #41 repeated it to Dave · #43 repeated it a third time** —
each of us reading the same sentence out of the same file, after a correction had been inscribed
at the source.

★ **This is the part worth keeping.** A correction written at the source did not stop the claim.
The propagation guard the project has ([[assertion-propagation-gap]]) fires on a *flip* — a fact
that was true and became false — and this claim was never true, so nothing was ever going to chase
it. **An inscribed correction is not a mechanism.** Naming it here does not fix it either; that
gap is real and still open.

## Finding 3 — Dave's question, and why it settles the fifth-state debate the other way

Dave: *"surely a key is fundamental to this working?"*

Read against the code, yes, and unambiguously. `_capture_gate.py:1109` builds ds-022's `have` as a
**set of session numbers parsed out of `#### <date> #N` headings**, then tests `prev in have`.
Unkeyed prose is invisible to it however true — the reader is a membership test, not a search.

The interesting move is what follows. #41 had raised **PRESENT BUT UNKEYED** as a *fifth vocabulary
state* the log lacks, on the grounds that #40's testimony existed but the parser could not see it,
and that writing `HOLE #40` would therefore be false. **The refusal was right** — `HOLE` is a
positive claim, and forging one would poison the dataset the throttle is re-derived from.

**But the diagnosis inverts once you accept that the key is fundamental.** The existing vocabulary —
`block` · `HOLE` · `ABSENT` — exists for records that **cannot be produced**. #40's could: it wrote
its `tape/bill PAIR #40` and two `META #40` blocks into that very file. What it omitted was the
heading. That is a **filing error**, and a filing error is repaired by filing it.

And there is a cost to getting this wrong in the other direction. `_capture_gate.py:200` already
warns *"do not let ABSENT decay into HOLE's meaning."* A term meaning *"we did not file it"* is
exactly the term that, eighteen sessions on, absorbs real gaps and lets the log read complete when
it is not.

## The hole in my own rule, and Dave's scoping

I put *"same file → key it"* to Dave. He handed it back scoped, and the scope is doing real work:

> **Same file → key it. Another file → that's the roll's job, a separate problem** — rather than
> let it read as covering #38 and quietly authorise a forged row later.

**#38 is precisely the case the unscoped rule would have swallowed.** Its content is in
`GOOD-MORNING.md` §C, not in the log. There is nothing to key *from*; producing a row would mean
moving one, which is `roll_2f`, which the chronological guard correctly refuses. An unscoped rule
would have licensed a heading over an empty space — the forged row the whole vocabulary exists to
prevent.

A second hole surfaced when I pushed on my own framing before inscribing: **"key it" assumes the
content is adequate as a row, and #40's is not** — no band, no fill, no error count. The adequacy
test cannot be delegated to the gate, whose docstring is explicit: *"it checks presence and
continuity — the two things a grep can settle. **Do not teach it to grade prose.**"* So the rule
carries a clause the session must honour by hand: **mark the row PARTIAL where it is partial.**
#40's key says so in writing.

⚠ **Method note, because it nearly went the other way.** Dave's first response was to hand my own
wording back with *"I guess this sounds reasonable."* That is a pick from a set I authored, which
is the `ds-023` shape — an agent's framing ratified because it was the only framing on offer. The
right move was to find the weakest joint in my own proposal and put *that* to him instead. The
PARTIAL clause exists because of that beat and would not exist without it.

## Withdrawn before it reached the record

I suspected `STRATA_BLOCK_RE`'s loose `^####\s` was letting `#### META —` headings consume cap
budget while contributing nothing to the dataset — two parsers for one line format, the drift class
the code's own comment at `:188` admits caused #32.

**Probed and withdrawn.** `BLOCK_RE` is used once, at `_capture_gate.py:837`, and only against
`GOOD-MORNING.md`; `notes/_GAUGE-LOG.md` is never counted by it. The four unkeyed `#### META —`
headings there cost nothing. **No defect.**

Worth recording as a beat rather than deleting: the probe took one call, and the alternative was a
plausible finding entering the record on the strength of two adjacent regex definitions. A
suspicion is not a finding, the same way an unmatched grep is not an absence.

---

## Resolved state

- **RULED (Dave, #43):** present-but-unkeyed is a filing error, not a vocabulary gap — **scoped**:
  same file → key it and mark PARTIAL where partial; another file → `roll_2f`'s problem.
  **§C·4 open 8 CLOSED.** No fifth vocabulary term.
- **ENACTED `cd75caf`**, +4/−0: `#### 2026-07-29 #40` plus provenance. Keyed rows **29 → 30**,
  verified with `STRATA_KEY_RE` rather than by eye. **#38 not keyed, by the scope.**
- **`_to_delete/` cleared** via `mcp__cowork__allow_cowork_file_delete` (runbook step 4b), directory
  and `_stale_locks/` preserved.

## Still open

- **`ds-022` stays RED · strata stack at four · `roll_2f` still refused for #38** by the
  chronological guard. Unchanged by this ruling, and now explicitly outside its scope.
- **Open 7 (the 2f fork) survives, but re-priced.** Its urgency premise is gone — the chain has
  381 tape, not 18 — so it is no longer the top of the board. The three questions inside it are
  still Dave's and still unruled.
- **`_CHAIN.md` states three sizes for itself.** Likely the footer prices the file before writing
  the footer — a self-referential measurement, the same shape as a gate inside its own growth loop.
  **Reported, not diagnosed.**
- **No mechanism chases a claim that was never true.** The propagation guard fires on a flip;
  #39's sentence never flipped, and three sessions re-derived the same misreading from it. Named
  here, unsolved.
