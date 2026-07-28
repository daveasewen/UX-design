# DV-D02 amended, and the first gate built on the encoding brief — the arc

provenance: local_7a4f5e6f-dea7-478b-8b7a-9e1b05d42f7f · 2026-07-28
status: ruled — `knowledge/_proforma/_DATAVIZ-DECISIONS.md` § Standing decisions, DV-D02 / DV-D02-A

*Session #28 (Opus solo, Dave live). Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA 2026-07-28 #28.
Ledger: `knowledge/_proforma/_DATAVIZ-DECISIONS.md` (DV-D02-A). Brief this session consumed:
`notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md`.*

---

## Why this session existed

Session #27 landed the DV-J2 scatter half. Dave then looked at the result and found four defects by
eye in under a minute — every one a rule Apollo already **holds** but does not **enforce**. #27 was
Amber and post-wrap, so it wrote the brief instead of acting, with a sequencing argument attached:
the chart-expansion wave is eight more charts, so encoding after the wave means fixing nine times.

#28 opened on that brief. The brief's own step 1 was not a build: **amend DV-D02 first, because you
cannot gate a rule that has a defect in it.**

---

## Finding 1 — the brief said the KB title rule was "not located". It is located, and it is the
## wrong rule

The brief was careful here, and its carefulness paid: it said *"Do not conclude it is absent — #27's
search was narrow. Find the KB rule first, quote it, then gate it."*

Found: `data-visualisation.md:28` `{#dv-006}` [ADVISORY/TASTE] — *"Labelling: title must reflect the
main insight…"*. Also `dv-bar-001` [TASTE] — *"Title: descriptive, reflects the main insight."*

**Both govern what a title SAYS. Neither says a chart must HAVE one.** And `data-visualisation-line-charts.md:41`
carries an explicit counter-case for spark charts: *"Structure (mostly optional): title; …"*.

So the brief's fallback branch was the live one: the presence rule genuinely is not written down, and
**a gate would have invented it.** That went to Dave rather than into code.

Measured distribution at the time: bar 7 · line 4 · combo 2 · donut 2 · **scatter 0 · sparkline 0** —
and sparkline's zero is *correct* under the written exception. A naive presence gate would have
red-flagged a compliant chart on its first run.

## Finding 2 — `dv-fit` on scatter: the machinery is wired and inert

#27 recorded, and Dave corrected, a false inscription claiming scatter's missing `dv-fit` was
deliberate. This session measured what "missing" actually means:

- scatter **has** the fit machinery — the injected behaviour queries `svg.dv-fit` and adds
  `dv-fit-on` to the figure;
- scatter has **no `<svg>` carrying the class**, and no CSS release rule.

So the code runs, finds nothing, and does nothing. Not "not adopted" — **wired and inert**.

**And then the same error class repeated, by me, an hour after reading the brief that documents it.**
On the strength of a grep count I told Dave the fix was "one class + one CSS line". It is not.
`fit()` relayouts elements by reading `data-fx` / `data-fw` / `data-pl` attributes. Measured:
Chart-bar 167 `data-fx`, Chart-line 111, Chart-combo 54, **Chart-scatter 0**. Adopting fit on scatter
therefore moves every gridline and every mark — which is precisely the ds-020 fence Dave set in #27
(*"it ships with a paired before/after control or not at all"*).

The lesson is not new and that is the point: **a count is not a measurement of the thing you care
about.** I counted occurrences of a string and inferred a mechanism's state from it.

## Finding 3 — the fifth finding the brief told us to expect

The brief's first line warns the list is open (Dave: *"There maybe more than I've stated too"*).
It surfaced on the first pass:

- `{#dv-007}` says *"horizontal scroll only as a last resort"*; scatter's DV-D02 fallback comment is
  literally *"fixed geometry, scroll"*. The safe fallback is the thing the KB calls a last resort.
- `{#dv-007}` also says *"titles must scale with text-resize"* while DV-D02 says *"TEXT MUST NOT
  SCALE"*. These are compatible — user text-zoom versus stretching with the container — but they sit
  one grep apart and a gate author will conflate them. Recorded rather than resolved.

---

## The ruling — DV-D02-A

Three questions went to Dave in plain language, deliberately **not** as an option-select: #27's first
option-select was refused for being mechanism-shaped, and the standing lesson (ds-D16) is that a pick
from an incomplete set reads exactly like a ruling. Each question described what he would *see*.

**(a) Horizontal bar — FIRM.** *"horizontal bars is fine, this must have been a rot problem or
miscommunication. This earlier example was responsive and I was happy with it apart from the text
cropping."* He attached a screenshot of a responsive h-bar showing clipped labels.

**The screenshot turned the ruling into a measurement.** Its aria-label matches
`Chart-bar.reference.html:387` exactly, and that svg has carried `class="dv-svg dv-fit"` since it was
built. **The implementation never agreed with the ledger.** So DV-D02's h-bar exclusion was never
enacted and was never Dave's — it is recorded as a **correction, not a reversal**, and the original
text is kept verbatim so the correction cannot later read as agent drift.

**(b) The donut graphic — NOT ruled, and deliberately left that way.** *"the chart graphic will
probably never have to scale, but I'm not 100% sure. there may be a case to start and stop scaling
between break points… should probably happen while or after we work on the 12 column grid and
breakpoints."* Hedged, and deferred by his instruction. The amendment records the hedge verbatim with
an explicit *do not harden "never" into a rule*. His separate #27 point — the donut's **lockup** with
its legend *is* responsive — is recorded as composition-level and ADR-shaped, not gate-shaped.

**(c) Titles — a direction, not a rule.** *"the title should be optional if it is a molecule that is
used in bigger organs and lockups… I'm not sure right now so make parameterised I think."*

That is the better rule — presence depends on whether the chart stands alone or is titled by its
container — and it **cannot be built today**: the registry injects *fixed* partial blocks, not slots
with varying contents. So (c) converges with the brief's finding 4 (legend-as-molecule) and with the
templates/shells zero tier. One missing capability, three symptoms. **The title gate was dropped from
this session's scope rather than approximated.**

---

## What was built

`_validate_dataviz.py::DV-D02-A`. Design notes worth keeping:

**It bites both ways.** A cartesian plot *missing* `dv-fit` fails; an excluded chart *carrying* it
also fails. The second direction was added on #27's evidence that a manifest bites hardest where the
author predicts it will pass — "someone adds fit to the donut" is exactly that shape.

**The scope partition is TOTAL and asserted at import.** `CARTESIAN_DTYPES ∪ NON_CARTESIAN_DTYPES`
must cover `KNOWN_DTYPES` or the module raises `ImportError`. This is the dv-vocab lesson applied
before it could bite again: a new dtype must not be able to land in neither bucket and skip the rule
in silence. **Mutation-controlled** — adding `sunburst` to `KNOWN_DTYPES` alone was run and did raise.

**Exclusions carry their reasons in the code, not just the ledger** — Dave's standing terms are *"I
lean to correctness, standardisation with flexibility rather than expediency"*, and a gate that
encodes a rule without its principled exceptions is a future false positive. `donut` carries the
hedge; `spark` carries *vacuously out of scope, not excluded — do not "fix" it by adding dv-fit*.

**Scatter is WAIVED, not fixed.** Blocking demoted to advisory, with a reason and a clears-when:
*"ds-020 is enacted with its control — then delete this waiver and the check goes blocking."* This
respects Dave's fence instead of stepping over it, and converts ds-020 from a note into a
gate-enforced obligation.

**The green control was already there.** `GOOD_BAR` gained `dv-fit`, which makes the pre-existing
"GOOD column passes blocking" case the proof the check stays silent on a compliant chart. Five new
bites, 27/27 selftest green.

---

## Receipts

- Build `[72/72]` exit 0 · DataViz gate PASS over 7 chart surfaces, 0 blocking.
- Debt measured: **17 cartesian figures, 14 compliant, 3 non-compliant — all scatter.** Nothing else
  was hiding.
- **Independent receipt:** the enactment register (generated, not authored) moved `DV-D02` from
  **UNPROVEN → PROVEN** and the corpus total from 7 → 8 proven / 57 → 56 unproven. DV-D02 had no
  instrument before this session.
- Retrieval dogfood: `_consult.py --fetch DV-D02` returns the amended text — the ruling is reachable,
  not just written.

## Still open, and whose

- **ds-020** — scatter's DV-D07 axis/grid catch-up, fenced; now also the waiver's clears-when.
- **The donut hedge** — Dave's, deferred to the 12-column-grid + breakpoints task.
- **The composition tier** — parameterised title slot · legend-as-molecule · control cluster with
  varying contents. One ADR, three symptoms. Dave's direction, not yet scoped.
- **T-D15 for charts** — the 12/14/16 mini ramp is minted and live, but it was minted for the
  segmented control and is a *fixed* ramp a class picks one rung from. Chart text stepping 14→12 at
  narrow widths would be a **new application**, not the untested half of an existing one. Dave raised
  it (*"we never tested it"*); recorded so it is not quietly assumed.
- **Findings 1 (cropping/collision) and 4 (legend behaviours)** from the brief — unstarted. Finding 1
  is a render-proof, deferred to a cold window by the brief's own don't-build-instruments-hot rule.
- **`{#dv-007}` vs DV-D02 wording seam** — new this session, unresolved.
