# The read-back offered the wrong options — a motion ruling that reversed itself twenty minutes later

provenance: apollo-sds-2026-07-27-6 · 2026-07-27
status: ruled · knowledge/_proforma/_DATAVIZ-DECISIONS.md § Batch 10

*Session #6, Monday 2026-07-27, Opus 5 solo self-conducting, effort MAX. A capture-only session: three
of Dave's chart observations came in, were recorded before anything was built, were read back as
options, and were ruled. **Nothing was enacted.** The session's finding is about the instrument used to
capture them, not about the charts.*

---

## 1. The session was supposed to be the ruling batch, and became something better

The handoff recommended the 15-item ruling batch. Dave chose it and then added a rider: *"but I want to
make changes to the charts too, I've noticed a couple of missed decisions, please note this."*

**The rider outranked the plan**, for a reason the previous session had just paid for. `ds-017` (logged
the same day) is the finding that a correctly-filed item can have **no path into the handoff that
should carry it** — it cost the start of session #5. A chart observation living only in this chat is
the same defect one step earlier: gone by morning, and no gate would ever report the loss.

So the first action was not to build and not to discuss, but to **write it down where a cold reader
will find it** — `_DATAVIZ-DECISIONS.md` § Open/pending, marked `OBSERVED-BY-DAVE, contents UNSTATED`,
with an explicit *"do not guess which decisions he means."* That placeholder existed for about four
minutes before Dave supplied the contents, which makes it look wasted. It wasn't: the placeholder is
what makes the *existence* of the gap survive a window that ends unexpectedly, and windows do.

## 2. The three flags, and what reading the source added to each

Dave gave three, all by eye, two with a screenshot:

1. *"the stacked chart should animate sequentially from the bottom, same as the pie, ease-in for the
   first, ease-out for the last, and linear for everything in between."*
2. *"the legend behaviour, the isolated key item stays active when I check others on."*
3. *"reset disabled style is set at the hover style."*

**Flag 2 had a cause available for the reading of it.** `canon/dv-legend.js:114` computes
`solo = st.isolated === id`, `:119` toggles `.is-solo` from that, and `:129` documents that checking a
second series *adds* it to the focus set — while `st.isolated` stays pinned to the row that started
the isolation. So the origin row keeps `.is-solo` (ink border, 6% ink fill, `canon.css:3506`) while
three series are showing. **That is the black-bordered "B Savings" in the screenshot, and it is
behaving exactly as written.** Not a bug in the implementation — a gap in the design.

**Flag 3 is more interesting, and was deliberately recorded as a hypothesis rather than a finding.**
The CSS is *correct as authored*: `:hover` is already fenced with `:not(:disabled)`, and `:disabled`
sets `border-color:var(--border-disabled)`. There is no specificity fight to find. So either
`--border-disabled` resolves to something ink-like — a token-value bug — **or it does not resolve at
all**, in which case `border-color` goes invalid-at-computed-value-time and falls back to
`currentColor`, which on this surface is ink. **A failed lookup would produce precisely the hover
appearance, silently.**

That second branch would make this **instance five** of the repo's signature defect class: ds-010
(author CSS beat `fill=`), ds-013 (404 stylesheet re-based by `srcdoc`), the 07-27 black chart keys
(local mirror missing the new var), ds-016 (the index cannot see the rule). In every one, the markup is
correct, the lookup misses, and nothing reports it.

**Both branches were written into `ds-018` with instructions to eliminate one by `getComputedStyle`
rather than by reading CSS.** The temptation to declare the fifth instance of a pattern you have been
collecting all week is exactly the pressure the anti-false-fix discipline exists to resist — and the
tell would be that the "confirmation" arrives without a measurement.

## 3. The finding: a read-back can only offer answers the asker thought of

Flag 1's easing rule was unambiguous. The *motion underneath it* was not, so it was read back as three
options: **serial hand-off** · **one shared rise revealing in order** · **fixed stagger**. Dave picked
serial. It was inscribed as `DV-D16a`.

Twenty minutes later, answering an unrelated question about the donut, he described what he meant:

> *"they all grow at the same time, so they are floating and growing, rather than growing and
> 'handing off' to the next."*

**"Rather than growing and handing off to the next" is a direct rejection of the option he had
selected**, in the option's own vocabulary. The correct answer — every segment animating concurrently
on one timeline, upper segments *floating* upward because their baselines rise as the segments below
them grow, with per-segment easing curves rather than per-segment timelines — **was in none of the
three options offered.**

⇒ **A selection from an incomplete option set is indistinguishable from a ruling.** This is worth
stating carefully, because the instrument is not bad: the option-select read-back is what produced
the correction, and it produced it fast. The defect is narrower and sharper — **it manufactures
confidence in proportion to how well-formed the options look.** Three tidy, mutually-exclusive,
plausibly-exhaustive options read as a complete space. They were not one.

**The mitigation is cheap and is now standing in the ledger: when reading back a MOTION or a FEEL
decision, describe the resulting sensation, not the mechanism.** *"The top blocks float upward as the
bottom one grows"* would have been recognised or rejected on sight. *"Segment 2 starts when segment 1
lands"* was not — it is a correct description of a mechanism, and mechanisms are not what anyone
perceives.

Sibling of `feedback-clarify-reflect-back`: the reflect-back *happened*, correctly, and still
under-determined the answer. Doing the ritual is not the same as the ritual working.

## 4. A justification that quietly changed hands

Dave capped stacked segments at 6 (`DV-D18`), matching the donut's existing `dv-pie-009`. **The cap was
proposed as the answer to a duration problem** — under serial motion, total time scales with segment
count, and a 9-segment stack is a slow chart.

**The reversal to concurrent motion dissolved that problem entirely.** One timeline; N does not affect
duration. The open duration ruling (fixed per-segment vs fixed total) closed itself — not by being
answered, but by ceasing to exist.

**The cap still stands, because Dave ruled it.** But it now rests on **legibility alone**, and the
ledger says so rather than inheriting the original rationale. A ruling whose justification has silently
been replaced is a ruling nobody can re-examine honestly later — and re-derivation is the whole point
of keeping the ledger.

## 5. The rider on the cap, which is the load-bearing half

> *"all bucketed 'other' segments should be expandable, through some mechanism we'll explore later."*

Filed FLOATED to `_FUTURE-STATE.md`, unscoped, deliberately. The reason it is flagged rather than
noted: **`DV-D18` is only defensible because of it.** A cap with no route to the bucketed detail is
data loss presented as legibility. Dave paired the constraint and the remedy in one sentence; the
failure mode is shipping the constraint and leaving the remedy floated — which is **already the state
of the donut**, capping at ≤6 today with no expansion route.

## 6. What was measured, and one measurement that changed a ruling's cost

Dave chose *"every stacked surface"* over *"Chart-bar only"* for `DV-D16`'s scope. Checking rather than
assuming: `stacked` appears **12×** in `Chart-bar.reference.html` and **0×** in `Chart-combo` and
`Chart-line`; stacked area is unbuilt; the grouped/stacked promotion (D-Q3) is ruled but not enacted.

⇒ **"Every stacked surface" is today a set of one.** The broader scope costs nothing extra now — it
makes the ruling **forward-binding**, which is a different and better thing than a bigger job. It also
creates a new way to lose it: a future wave building stacked area without reading this ledger. Carried
into the chart-expansion brief for that reason.

## 7. Resolved state

**RULED, none enacted:** `DV-D16` (concurrent/floating motion, per-segment easing, every stacked
surface, reduced-motion ships with it) · `DV-D17` (release isolation entirely on the second check-on) ·
`DV-D18` (≤6 cap). **LOGGED:** `ds-018`. **FLOATED:** expandable "Other" buckets.

**Still open and named:** does the donut actually sequence today (answerable by reading the repo — do
not ask Dave) · `ds-018`'s two competing causes, to be separated by render · `DV-D17`'s three
enactment bites (restore to `visible[]` not all-on · Reset must not self-disable while filtered ·
`dv-sr` must announce release on the add path).

**The window was flushed rather than continued.** Pricing at the point of decision: fill ~43%,
enactment ~30%, wrap ~5% ⇒ **~78%, Red**. Even `DV-D17` alone landed on the 60% boundary. Per the
throttle ruled the previous session, that is a fork put to Dave, not a call made silently from inside
the work; he chose flush. **The first session where the throttle was applied to stopping work that was
already going well**, which is the case it was actually built for.
