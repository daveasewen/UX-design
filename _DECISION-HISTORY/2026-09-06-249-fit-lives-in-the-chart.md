# #249 — Fit lives in the chart: the debt was analysed before it was built, Dave chose the library engine, the build went green on physics and red on bytes, and the red is his fork

```
provenance: 249 · 2026-09-06
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-06 … #249`. Ledger: `knowledge/_rulings.json`
§ `s249-D1` … `s249-D6` (inscribed by the conductor, 364 → 370, read back at the wrap). Banner: `GOOD-MORNING.md`
§ ★ LATEST #249. Reports: `notes/_subreports/2026-09-06-249-W2-DEBT-conductor.md` ·
`notes/_subreports/2026-09-06-249-DP18-fit-analysis.md` · `notes/_subreports/2026-09-06-249-DP08-status-surface-analysis.md` ·
`notes/_subreports/2026-09-06-249-FIT-lane.md` · `notes/_subreports/2026-09-06-249-META-research.md` ·
`notes/_subreports/2026-09-06-249-wrap.md`. Review surfaces: `reviews/W2-DEBT-DP08-DP18-2026-09-06-v1.html` ·
`reviews/OPTION-SPACE-META-2026-09-06-v1.html`. Carry set: `_CARRIES.md` § `## residual → #250`.*

This is the WHY and HOW. The WHAT — figures, gate exit codes, file paths — is on the spine and in the filed reports,
and nothing here re-measures them.

## 1. Why the day opened as analysis, not as the build the title promised

The forward title was *fit lives in the chart — D2 to the components*: #248 had found that the template's hand-carried
vertical-fit stub fought Chart-line's own engine and was dropped from the composed page, and the obvious next act was
to carry the fit into the components. Dave was out, and his instruction was narrower than the title: *"just analyse and
come back with some proposals, and show me visually."* So the conductor did not build. He briefed two analysis lanes —
DP18 on the fit, DP08 on the status surface (the other debt item from W1) — and composed a review page with three
rendered options for each, so that the decision could be taken by looking, not by reading.

The reason this mattered: the W2 sheet read *met 10 · missed 16*, and a cold reader could take sixteen misses as
sixteen jobs. The conductor's first finding is that thirteen of them belong to waves not yet run (W3 3 · W4 5 · W5 5 ·
W6 1) and only two are debt in waves already run — DP-08 from W1 and DP-18 from W2. The analysis was scoped to those two
because the plan's own wave order says the rest are not yet due.

## 2. Why the fit engine's home was the real question, and what the DP18 lane found the prototype lacked

#248's lane D3 had written the vertical fit inside the template; #248's lane R had watched it lose to Chart-line's
engine. The DP18 lane named the mechanism precisely: two engines subscribed to one selector (`svg.dv-fit`), and the last
writer pins the viewBox back to 260. That is not a bug in either engine; it is what two engines on one element do. The
lane also found that the stub's y-handling was incomplete for line charts — polyline points, circle marks, rect-mark
centres and polygon marks each needed their own re-derivation — and proved a prototype in `__dvBehaviour` itself that
took the composed page's chart from 821×260 with 44px of slack to 821×304 with none, 19/19 on the physics assertion
(labels and strokes unchanged, marks on their lines, live resize returning).

The three options on the page were honest about cost: (a) the library engine plus a physics test; (b) the stub yields —
cheapest, and every composed page with a real chart loses two-axis fit; (c) register the role only — loses VFIT. The
page recommended (a). Dave's answer was five words: *"lets go with your recommendation, it seems the most complete."*
That is `s249-D4`.

## 3. Why the status surface stayed open, and what Dave said in the car

DP08's lane established that two of the six status tiles are states, not series — a count-of-total and a ratio-to-limit
have no period delta to draw — and that the Undrawn sparkline was twelve identical points. No option moved the first
chart's y (710.6 in all seven renders). DP-20 was already over its carrier budget before any option was drawn. The page
offered A (a strip in the masthead), B2 (the head of Needs-attention), both, and C (the in-row kind, built so that a
"no" could be a seen no).

Dave liked A and B and floated their combination with a question mark — *"maybe?"* — and then said something wider
than the item. He had been thinking about the #248 decision to stack tiles rather than sit them side by side at 900px
and called it *"super prescriptive"*: fine for the presentation, where he wants great results, but in factory mode, if a
user asks for three different solutions, *"fussy edges will be needed."* From that came the meta idea — *"'related to'
'interchangeable with' maybe even with weights"* — with his own caveat attached twice: *"it might not be the solution."*
`s249-D1` records the whole of it as OPEN plus a research direction, and the META lane was briefed as research, read-only,
with alternatives and his risk stated on the page. It ruled nothing.

## 4. Why the headline row is "whatever the data dictates", and what that does to the column question

Decide item 2 asked whether a headline row may be four tiles at four tracks or must stay on six-track multiples. Dave's
answer (`s249-D2`) cut under the question: the headline row holds whatever count the data dictates — five is fine — and
the 12-column grid is *"desirable only"*, not necessarily the internal structure of a functional element. This does not
close #248's 12-vs-6 vocabulary collision; it changes its shape. The layout grid's vocabulary is still one question (META's
RSQ 2 asks for one vocabulary before any `fits` tag can be authored), but the headline row is no longer bound to it.
Both are carried as his.

## 5. Why the build is green on physics and red on bytes, and why the lane did not clear the red

Lane FIT did the seven steps as briefed and every physics figure is in its report. What it found first is the finding
that matters for #250: the dataviz page budget was at exactly its cap before the lane touched anything — the three
sources summed to 34,816 bytes against a `PAGE_BYTES` of 34,816. Zero headroom. Any byte added to any source fails the
gate. VFIT's code is 3,697 bytes with every comment stripped, and `dv-behaviour.js` alone now exceeds its per-source cap
too.

The lane recognised the shape: Dave re-dialled this same cap from 32 to 34 KB at #96 for the last extension to
`fitOne`, after that code had been "shaved twice". The options are the same four as then — re-dial, a marked waiver, a
shave of existing comments (which are provenance text, and not a lane's to cut), or park — and the lane wrote them as
his fork and stopped. It did not raise the constant. That is the correct refusal shape: an ADR-0015 budget is a ruled
number, and a lane that moved it to make its own work land would be paying with a constant it does not own.

Two side-effects are declared rather than hidden. Registering the template as a dataviz member was the only way the
generator could inject the engine (the stub's own comment prescribed it), and it makes the template a full behaviour
consumer — popover, table panel, everything — where it carried a fit-only stub; if Dave wants it lighter, the alternative
is a `consumes: []` member with no fit at all, not a stub. And `_assemble_b.py` copies by hard-coded line ranges that have
all shifted; it cannot be re-run, and the composed page was rebuilt by marker-delimited swap instead.

## 6. Why the wrap commits the lane's nineteen files with a red gate riding

The capture ritual commits the session's changed state; the `--reconciled` form is an attestation that every dirty path
is accounted for, and the #248 precedent committed three lanes' snippet edits with the composition gate red ×3 (C9's law,
Dave's). The FIT lane's work is the session's principal output, its physics gate is green, and its red is a ruled
constant's — leaving it uncommitted would not make the fork any less his, it would only put the day's work at the mercy
of a mount. So the nineteen files ride, the red is named in the commit body, and the CI verdict on push will be red on
the behaviour gate by construction until Dave forks. The `s203-D1` read-back will say so.

## 7. Why the ceiling arm stays red and the commit is again the #243 form

#249's boot at the opener was 71,113 — a fourth post-diet reading over the 70,000 ceiling. The arm graded #248's 70,974 at
this wrap's 2f roll, as #248's wrap said it would; the `s244-D1` discharge form needs a post-breach reading under the
ceiling and there is none. So `--wrap` is refused at the seam and the commit is made as `after #249`, DECLARED not-a-wrap,
the `--wrap` FINAL owed — the third wrap in this state. The ceiling literal was not moved. The remedy the gate names is
to cut the boot, and how is Dave's (residual → #244 ⑤'s three options are still his).

## 8. What the lanes cost, and what the wrap could not see

Five subs by the conductor's declared harness figures, ≈605K quota in total; the wrap sub's own spend is unmeasured. The
conductor's transcript reads 201,881 real at this seat — past the 200,000 wall, not just the advisory — which is the
reason every step here was delegated and why his brief could quote the runbook but not read it. Nothing at this seat
read memory or wrote it; step 3 is his.

## Resolved state, and what is open

Resolved: six rulings in his words, in the store; DP-18 proposal (a) built and physics-gated; the template's stub gone;
canon.css carrying both the `height:auto` release and rule 6b; the option space inventoried as options.

Open, all Dave's: the byte-gate fork · DP-08 A+B · the extra signal for R and A · item 6 laid out visually · the seven
META questions · the template as a full member · the 200px floor · mark-vs-bar by class or attribute · C9's law · the
column vocabulary · which tile leads · the ceiling arm.
