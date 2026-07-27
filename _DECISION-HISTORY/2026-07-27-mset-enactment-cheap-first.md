# M-set enactment — the cheap-first cut (2026-07-27, session #18)

provenance: local_9ecbcf40-1760-4a5a-9703-f8d2a34c8de9 · 2026-07-27
status: ruled · notes/_MEMENTO-DECISIONS.md

*The WHY and HOW behind § ★ M-SET ENACTED. The ledger holds the WHAT and its pins; this holds the arc,
including the two drafts that were wrong. Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #18. Brief:
`notes/_briefs/2026-07-27-memento-hardening-brief.md`.*

---

## 1. The window opened by refusing to start

The handoff was unambiguous about the job — execute M3→M12 in brief order — and the brief priced itself
at 35–45% of a window. The first thing this session did was **measure its own floor** rather than
inherit the guide figure, per D9. Read chain: GM 12,780 + LS 16,063 + brief 2,389 + the band-table
slice 1,527 = **32,759 tk = 16.4%**, with the harness (system prompt, tool schemas, memory index)
unmeasured on top and declared as such — the #17 datapoint implies ~7%, so **~23–24%**.

Then the arithmetic that mattered. M1 was ruled at #17: **RED = wrap-only.** RED starts at 60% fill.
So the room is `60 − 24 = 36.5` points, less ~6 for the wrap, ⇒ **~30 points of job**. The brief wanted
35–45. **The set could not fit, and would have discovered that at roughly 55% — mid-M4, the most
expensive item.**

This is worth naming precisely, because it is not "the brief was wrong". The brief's price was probably
right *for the work*. It was never measured **against the window it would run in**, and that gap is the
same species the whole M-set exists to close: a number stated in one frame, evidence gathered in
another. Three cuts went to Dave pre-start; he took the cheap-first re-cut (*"2. your recommendation"*):
M3 · M6–M12 now, M4a/M4b/M5 kept together as a build window.

**The transferable bit:** a ruled sequence is not a ruled *fit*. Price the sequence against the measured
floor before the first edit, and fork if the two disagree — the fork is cheap at 24% and expensive at 55%.

## 2. M3 — prove the defect before fixing it

The churn signature (`dangling_citations` swapping key positions, 5 ins / 5 del, zero content) pointed
straight at a set iteration, and it was: `for rid in untagged` where `untagged = declared - idx`. Hash
randomisation seeds the insertion order, `json.dump` writes insertion order, the file churns.

Rather than fix and declare victory, the defect was **reproduced first** — two runs under different
`PYTHONHASHSEED`, diffing exactly as observed at #17 — and only then fixed (sorted iteration *and* a
sorted-key emission, belt and braces, with a provenance comment so a later tidy-up cannot "simplify"
either away). Re-proven: **identical under three seeds**, then **two consecutive `_build_all.py` runs
byte-identical across all seven changed files**.

The file's other emissions were checked once, as the brief instructed — `gate_instruments` builds from
`check_files()` which is already `sorted(os.listdir())`; `rows` follows the rules index; `tally` follows
`rows`. One defect, one fix, no speculative sweep.

Note what did *not* churn: `_INSTRUMENT-FIT.md`. The markdown renderer already sorted its display
(`sorted(gate_inst)`, `", ".join(sorted(dangling))`), so the human-readable artefact looked stable while
the machine-readable one drifted. **A rendered view can hide the disorder in the data behind it.**

## 3. The finding: M10's block was already crossed, and its remedy could not pay

Enacting M10 exactly as ruled produced a FAIL at the wrap: chain 28,843 tk against a 28,000 block. The
brief had predicted a *warn* — but its own quoted figure (29,193) is past 28,000 too, so the prediction
was never available under its own numbers. An arithmetic slip at #17, not a ruling about behaviour.

The second half is the more interesting one. The check's first draft printed the obvious remedy:
*roll `_LIVE-STATE` deltas (ritual step 2d)*. Measuring before believing it:

| region | tk |
|---|---|
| the three retained deltas, all of them | 1,422 |
| the standing body beneath them | 12,694 |
| the SPIN-OFF LANE block alone | 1,692 |

`_LIVE-STATE` was **already at its ruled LATEST+2 retention**, so the prescribed fix was unavailable;
and even breaking that rule and rolling every delta would shed 1,422 tk against a need of 844 while
leaving 79% of the file untouched. **The remedy pointed at the one region that could not pay**, and the
SPIN-OFF block on its own outweighs every delta combined.

That is [[gate-narrows-its-own-rule]] — a gate encoding one mechanism as *the* rule — occurring inside
the gate built to prevent that class. It was caught only because the number was measured rather than the
advice followed.

Forked to Dave. He ruled advisory (*"Ill go with your advice"* to the recommendation): **his numbers
stand untouched, only the tier moves**, 28,000 becomes a promotion threshold on the M9(a) pattern the
brief itself had already chosen, and the LS standing-body trim is queued as the work that arms the block.
The remedy text now reports the measurement and explicitly declines to name a region.

## 4. Two drafts that were wrong, and the bites that caught them

Both are recorded because a reversal inscribed only in its corrected form reads later as agent drift
(the B-D7 precedent).

**(i) M7's suppressor would have silenced M7 forever.** The growth trigger is meant to stay quiet when a
banner line names a §A change — that silence is what honours GM-D7-am's *"not even a guard banner"*. The
first draft scanned the whole banner region for the string "§A". But M7's own persistence mechanism puts
`§A N.NK tk` **into the `size:` stamp**, which lives in that region. So from the very first stamped wrap,
the suppressor would have matched its own bookkeeping and suppressed the trigger permanently — a check
that reports green forever, which is the worst failure shape this corpus knows. The bite failed; the scan
now excludes the stamp line.

**(ii) The M8 fixture was sized from a comment.** `FAT` is documented in the file as "~200 tk of line".
Measured: **240**. The intended *warn* fixture (22 lines ≈ 5,367 tk) therefore sat above the 5,000 block
and bit as a block instead, so the warn path was never exercised. Re-sized from the measurement, and the
measured figure written into the fixture comment.

The pattern is one pattern: **both drafts were written from a description of a thing rather than the
thing.** The instrument is not optional even when the number feels obvious.

## 5. What was built to outlive this window

- **`_capture_gate.py::section_a_digest()`** — the §A hash convention as *code*. #17 lost an abort to a
  wrong-shape probe and had to recover the convention mid-wrap; a convention living in prose is one
  rewrite from gone. Bitten both shapes, since the with- and without-trailing-newline digests must not
  collide. **M5's mover must call it.**
- **Ruled values pinned in the selftest**, tier included. Re-arming M10's block before a wrap has
  measured the chain under 28,000 would reverse Dave's ruling by editing a tuple; the pin fails the build
  if that happens. Bite-the-bite run and restored.
- **M9's proxy is rewrap-immune.** Comparing normalised *regions* rather than lines means re-flowing a
  paragraph — which every compaction pass does — produces no phantom retirements. A line-shaped version
  would have cried wolf at every wrap and been ignored within two.

## 6. Open at close

M4a · M4b · M5 (the build window, kept together on purpose). The `_LIVE-STATE` standing-body trim, which
is now M10's promotion trigger rather than housekeeping. Dave's supervised `memento-dream-pass` fire
before Sunday 08-02 — the scheduled path has still never run. And, unchanged, §C·2's 15 rulings plus the
dataviz sign-off.
