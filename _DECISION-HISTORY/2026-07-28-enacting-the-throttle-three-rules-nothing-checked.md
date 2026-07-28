# Enacting the throttle: three rules that existed, were correct, and were never checked

provenance: local_33b76974-259f-4fd6-b5c4-441acf8bfa6f · 2026-07-28
status: ruled — `knowledge/_DS-IMPROVEMENTS.md` ds-021 / ds-022 / ds-023

*Session #34, 2026-07-28 (Tue evening), Opus solo, Dave live. Spine entry: `_LIVE-STATE.md`
⏱ LATEST DELTA. Ledger: ds-021 · ds-022 · ds-023, all three moved OPEN → ENACTED in this window.*

---

## The shape of it, before the detail

Three defects were raised in one session (#30) and ruled in another (#31, on delegation). They
looked like three unrelated problems: a unit error, a missing log entry, a mis-read reserve. They
are the same defect three times.

> **The rule existed. The rule was correct. The rule was ratified. Nothing checked it.**

ds-021's caps were denominated in `tape` while the window charged in `bill` — the gate was never
*wrong*, it was **precise in the wrong unit**. ds-022's step 2f said the stratum splits in two, and
three consecutive wraps rolled it whole. ds-023's reserve was ring-fenced by canon in three separate
verbatim passages, and every session added it back in as headroom.

That is why they were enacted together rather than one per window. Enacting one and leaving two
would have been the fourth demonstration of the same thing.

---

## Finding 1 — the units, and the thing that made naming them hard

Dave delegated the names (*"you choose"*). The obvious pairing was semantic — `counted` / `charged`,
or `count` / `charge` — and both were rejected for the same reason: **Dave is dyslexic, and near-
homographs that rhyme are the worst possible pair for a number you must read at a glance.** Shape
distinctness beat semantic elegance.

`tick` was the first pick and would have been a mistake: **118 collisions** in the corpus, measured
before choosing rather than after. `ruler` scored zero collisions and was *still* wrong — it reads
as `RULED`, and this repo is built out of the word "ruled". The pair that survived was **`tape` /
`bill`**, 4 and 5 hits, and the mnemonic came out of the choice rather than being bolted on:

> **The tape is not the bill.**

**The honest disclosure, made at enactment rather than discovered later:** today the change is
*arithmetically identical* to what it replaced. Both sides of every comparison convert through the
same provisional ratio, so the conversion cancels. Two things are still bought — nobody can read a
`tape` figure as a cost again, and the moment a *real* `bill` measurement exists the cap binds on a
measured quantity and the ratio stops mattering. Saying this out loud matters more than the change:
an enactment that quietly implies more than it delivers is the CLAIMED-vs-UNPROVEN problem
(ADR-0016), and CLAIMED lies while UNPROVEN is honest.

The ratio was pinned at **1.57, GM's own measured pair, deliberately not the 1.55 corpus average** —
every cap it converts is GM-derived, and averaging would have loosened a GM cap by ~1% while looking
like tidying up.

## Finding 2 — the roll, and the argument that had to not exist

ds-022's remedy was ruled *(c) guarded by (a)*: fold the roll into the mover, and gate the result.

The design decision worth recording is a *removal*. Two `move` ops could always have expressed the
2f split — the mover has been able to do this since #21. What two `move` ops **cannot express is that
the second one is mandatory**, and that is the entire failure: #26, #28 and #29 all did the first
half. So `roll_2f` takes both halves in one op and refuses if either is empty.

The second removal is sharper. #27's block was **prepended** to an append-only file, by a
hand-written `insert` with a top-of-file anchor. The fix was not to validate the anchor — it was to
**delete the anchor argument entirely**. Both destinations append at true EOF, so the mistake is no
longer *expressible*. A guard you can get wrong is weaker than a parameter that does not exist.

**The HOLE escape hatch is load-bearing and was nearly designed out.** A continuity check with no
way to say *"this session legitimately wrote nothing"* would block a wrap whose predecessor was
correct — and a gate that fails on correct behaviour teaches sessions to **fake blocks**, which
would poison the exact dataset the 15% reserve is waiting to be re-derived from. #14 is the proof
it works: its absence was declared, so #14 is countable. #9/#10/#11/#19 are absent in silence and
cannot be reasoned about at all.

**Not done, deliberately:** backfilling HOLE lines for #9/#10/#11/#19. A HOLE line asserts *"this
session wrote no stratum."* What exists is evidence of **absence**, not evidence of that assertion.
Inscribing the stronger claim to tidy a dataset is exactly the confident-false-inscription failure
this whole programme is built against. Flagged to Dave; left alone.

## Finding 3 — the ceiling, and the correction that came from running it

ds-023 was the one Dave described in the plainest terms: *"this is making me suffer unduly."*

The arithmetic falls out of his own ratified numbers and is not a new threshold: if RED at 60 is a
hard stop and the ~15% reserve is ring-fenced *inside* it, any pre-flight must project to finish
GREEN — `fill + job + wrap ≤ 45`. In flight the stop line is `60 − the priced wrap`, and **it moves
with the wrap price**, which is bitten for explicitly: a 15-point wrap must stop the session at 45,
not at the 52 an 8-point wrap allows.

**Then it was run against the real repo, and it failed — on #33's stamp.** And #33 had done the
right thing. Its stamp reads *"was REFUSED against the 45 ceiling and forked to Dave"* — the correct
behaviour, in the wrong words. The strict marker was kept (a gate matching free prose cannot tell a
declared spend from a passing mention), but this is **`gate-narrows-its-own-rule` appearing at
birth**: a disciplined session wrote the correct thing and would still have failed. The remedy was
not to loosen the regex but to **document the magic string where the rule lives**, not only where
the regex lives. A gate requiring an undocumented literal is a trap, not an enforcement.

**One point of slack, flagged not settled:** the ruling says `≤ 45`, but 45 reads AMBER on the band
table (GREEN is `< 45`). *"Must project to finish GREEN"* and *"≤ 45"* disagree by exactly one point.
The **literal ruling** is what shipped. Dave's to close.

---

## Two corrections, neither found by re-reading code

**Eighth consecutive session in which the corrections came from running things, not from reading
them.**

1. `roll_2f` validated *where the block goes* before *what the block is*, so a mis-typed `session`
   argument was refused by the **chronological** check and reported as an ordering problem. The
   message named the wrong defect — a test caught it because the assertion checked the *message*,
   not just the exit code. Reordered: validate what is being rolled, then where it goes.
2. The existing pre-flight "green control" fixture (`= 57% AMBER`) **stopped being green** the moment
   the ceiling shipped. It was a valid control for a FORM check and an invalid one for a check that
   also asks whether the plan is *permitted*. It is kept in a comment rather than deleted, because
   *"the control used to pass"* is the evidence that the ceiling actually changed something.

## The session's own pre-flight, as a worked example

Priced at **48 against a 45 ceiling** and declared to Dave *before* starting — *"that is over the
ceiling I'm enacting for you in this very window"* — with job 1 (make the usage data bite) **dropped
rather than squeezed in**. He ruled it a spend: *"I can live with 48 if it only crawls over 60."*

So the first live subject of the new rule was the window that built it, and the escape hatch was
exercised the way it is meant to be: **declared in advance, forked to Dave, marked in the stamp** —
not discovered at 62% and confessed afterwards, which is what #30, #31, #32 and #33 all did.

## Open, and Dave's

- the `≤ 45` / `< 45` one-point slack
- HOLE lines for #9/#10/#11/#19 — evidence of absence only
- the `tape`→`bill` ratio at n≥4 (the gate forks automatically)
- whether the strict `RESERVE SPEND — forked to Dave` marker stays strict
- **job 1 — make the usage data bite — displaced to #35, not abandoned**
