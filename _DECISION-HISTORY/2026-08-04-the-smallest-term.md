# The smallest term — how a session about three stale receipts became a measurement of where the window actually goes

provenance: local_79640f17-6508-4f19-88be-cf1a61052842 · 2026-08-04
status: observed

Spine: `GOOD-MORNING.md` ★ LATEST #90 · Ledger: `notes/_MEMENTO-DECISIONS.md` § ★★ THE THREE STALE
RECEIPTS RE-CHECKED AT HEAD and § ★★ #90 — THE 2f ROLL OWED SINCE #83 IS DISCHARGED.

## Why this session exists

Dave opened with a constraint, not a task: *"P4, P6 and P7 are ruled but their receipts are stale.
If any window picks them up, it needs one re-check each first."* The first useful move was **not to
record it** — it was already inscribed, near-verbatim, at `notes/_MEMENTO-DECISIONS.md:3417`/`:3419`.
The finding was that the inscription is **unreachable**: `_CHAIN.md` has 0 hits for P4/P6/P7, the
caveat has 0 hits in GM / `_LIVE-STATE.md` / `_state.json`, and `_memento_search.py` on the natural
query misses the entry — the same retrieval failure #79 logged for the sibling P-set. Twice now.

There is also a **name collision**: two live P-sets from the same 24 hours both use P4/P6/P7, with
opposite statuses (in the handoff-regime set, P4 is *ruled build now* and P6/P7 are *parked*). A
window acting on Dave's sentence has a coin-flip chance of grabbing the wrong one.

## The three verdicts, and what each one taught

**P4 held and got worse.** The rate itself did not move — 27/49 = 55.1% at HEAD against 21/39 = 53.8%
stale — which is a real vindication of the original measurement across eleven more sessions. But
*"no downward trend"* is now the wrong sign: the last ten sessions carrying a line are 70% none. And
the thing the stale receipt could not see: **#88 and #89 carried no `consult-receipts` line at all.**
That is not a lapse honestly recorded; it is the instrument's input not arriving. Later in the wrap
this resolved — #89's stratum was sitting **unrolled in GM §C**, and 2f moved it. The dataset gap was
a *ritual* gap, not a session gap, which is a distinction the rate could never have drawn on its own.

**P6 held exactly, and inverted into something worse.** The four named terms went from 0 hits to 1 hit
each — and **all four hits are the same line: Dave's own ruling accepting P6.** The destination that
ruling names was still empty. The only thing in the corpus mentioning the three forks was the record
of the decision to home them. A control (fork 1, the one that landed) still had its home, so the zero
was an absence rather than a broken probe.

**P7 died, and the way it died is the lesson.** The stale receipt said the `size:` stamp ran 9–9.5%
*below* the artefact. At HEAD it ran +0.96% *above*. Two things killed it: #82 re-denominated the unit
(tape → real), and #87 re-stamped after a regen. **A receipt can be stale in its UNIT as well as its
STATE.** The important discipline was refusing to let the proposal die with its evidence — P7's
residual clause is structural, not state-dependent, so Dave's ruling on it stands for a different
reason than the receipt gave.

## Dave's question, which outranked the pass

*"Are we getting in trouble all the time because we are trying to fix the tool that the tool is using
to track its progress?"*

The answer is yes, with a specific mechanism worth stating precisely: **every Memento fix ships a new
instrument, and every new instrument needs its own witness, test, home and budget line.** So "nailed"
recedes as fast as we walk toward it. #88 built the state store; #89 then had to build a witness
because the store could not witness itself; that witness had already leaked by #90. Commit-subject
classification over 43 sessions — a crude keyword proxy, declared as such — reads 32 machinery-only,
2 product-only, and 12 of the last 15 = 80% machinery.

## The turn: the fear was right, and it was pointing at the wrong term

Dave's stated fear was boot bloat — *"the boot was so big that we couldn't work on anything within the
context window."* Measured off `git show` in real tokens, no stamp trusted, the chain went **7,160 at
#52 → 13,277 at #89 = +85%, and never once came back down.** The standing claim that the rolls keep
the floor oscillating rather than rising is false at that timescale: #87 cut 5,551 bytes and #88 put
5,926 straight back — in the session that built the state store.

But then the arithmetic relocated the problem entirely:

```
boot ......................  61,854   30.9%
  the read chain ..........  13,277    6.6%   ← what fifteen sessions fought over
  never itemised ..........  48,577   24.3%
wrap floor ................  42,434   21.2%
room to work ..............  95,712   47.9%
```

Halving the chain buys back 3.3% of the window. **The programme has been optimising the smallest of
the three terms.** The wrap floor alone is larger than the entire corpus being trimmed, and the dark
half is nearly four times the chain. That reframing is the session's most useful output, and it is
what set #91's title.

## What was actually built, and the discipline that made it legal

`GM:9`'s `size:` stamp measured **3,055 real — 23% of the entire read chain**, one line, accreting
every session's own arithmetic since #79. #83 declared the roll owed, ran a probe, found GM:9 their
sole home, and correctly refused to cut. It was then deferred five consecutive sessions.

The move was legal only because the probe was **re-run** (17 figures, still sole home), the text moved
**verbatim** through `_gm_move.py`, and only then cut. Move before cut, never the same motion.

## Three things I got wrong, kept because the corrections are the value

**I reproduced the exact defect I had measured that morning.** The first #90 stamp wrote the pre-cut
figures beside the words *"measured AFTER the regen"* — false the instant the cut landed. Caught by
re-reading the artefact, not by any gate. A size claim cannot converge inside the file it measures;
the stamp now iterates write→measure→rewrite to a fixed point, and the chain figure is deliberately
absent, pointing at the generated footer instead.

**My banner ate most of my own cut.** After the cut the chain was 11,029; after my banner and delta it
was 12,379. The banner was +610 over the one it replaced. Measuring that, and shaving it to 2,373 —
below the 2,561 it swaps out — is the session's own rule applied to itself rather than described.

**I misattributed a timeout** to `_build_memento_index.py`, which runs in 0.21s; a 17-pattern
repo-wide grep in the same call was the slow half. Isolate before attributing.

## Found by walking through it

`CHAIN_STAMP_RE` (`_capture_gate.py:816`) exists to forbid a hand-written chain figure in the `size:`
stamp. It binds only the `CHAIN … N K tape|tk` form. #82 retired that unit, and the regex was never
re-scoped — so `chain 13,277 real` walked straight past the check written to forbid it. **Declared,
not fixed.** A rule is only as wide as the form its gate names.

A near-miss at the wrap itself: the size-history block was first keyed `#### 2026-08-04 #90`, which
would have collided with this wrap's own 2f post-mortem key and been refused by the duplicate-key
guard. Converted to the `#### META —` form before 2f ran.

## Resolved state, and what is still open

Resolved: three verdicts inscribed; the 2f roll discharged; the read chain cut 13,277 → 11,638 real
(−12.3% net of my own additions); four #88/#89 deferrals homed by the 2c EXIT CHECK that would
otherwise have rolled out of live state with #88's banner.

Open, and deliberately so: the **48,577 dark half** stays dark — the memory directory is unreachable
from the sandbox, so `MEMORY.md`'s boot cost is unmeasured rather than estimated. The **wrap floor**
has never been attacked. The **reachability** defect Dave's opener was really about is unfixed. And
the `CHAIN_STAMP_RE` scope hole is named but open.
