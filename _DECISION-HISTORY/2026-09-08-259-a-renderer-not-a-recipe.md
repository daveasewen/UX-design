# A renderer, not a recipe — how #259 put the chart engine in the library, and why it left two gates red

```
provenance: 259 · 2026-09-08
status: observed
```

*Written at the #259 wrap by the DELEGATED Opus wrap sub, from `notes/_briefs/2026-09-08-259-delegated-wrap-brief.md`
and the six filed lane reports. The WHAT lives in `GOOD-MORNING.md`'s ★ LATEST banner and `_LIVE-STATE.md`'s
⏱ LATEST delta; this file holds the WHY and the HOW. Spine entry: `_LIVE-STATE.md` ⏱ delta #259.
Ledger: `knowledge/_rulings.json` § `s259-D1` (entry 403).*

---

## 1. The session was sent to build six charts and found fourteen already built

#258 ended with rule 18 — *"Charts from data, the interim recipe"* — a paragraph of `dv-behaviour` grammar
inside a skill, driven green on a 78-line test page. The carry that came out of it said the library needed
six charts.

A read-only Opus probe was run before any lane was spent, and it moved the premise: **all fourteen registered
dataviz types already exist as components.** What was missing was never the components; it was a **renderer** —
and `s249-D4` had already ruled the renderer's shape (engine in the library, on the dv-behaviour side).

Two smaller corrections came out of the same probe, and both are the class where a document is wrong in a way
nothing chases:

- the **count collision** — the registry holds 14 types where the carry said *"11 / other five"*; nobody had
  reconciled the wording, and the carry had been re-published at that count for several wraps;
- rule 18's `cn-chart-bar` **wrapper trap names the wrong source**: the wrapper is in `canon.css`, not in the
  snippet the rule points a reader at. A trap that misnames where the trap lives sends the reader to the wrong file.

And the receipt rule 18 was proud of turned out never to have been committed: its 78-line green page lived in
`/tmp/r258` and died with the window. *A receipt in scratch is a claim, not a receipt* — the same lesson the
sub-report contract (`s218-D7`) already carries, arriving again from a different direction.

## 2. Why a core had to be written before five lanes could run in parallel

Six chart types, five of them independent, is the shape that invites six parallel lanes. It cannot be run that
way from cold: six lanes writing six renderers produce six private conventions for axes, ticks, fitting, tables
and legends, and the union of them is not an engine.

So the wave was split. **Lane A wrote the core first** — `knowledge/canon/dv-render.js` (311 lines) plus
`dv-render-bar.js` and five stubs — re-pointed Chart-bar at it, and committed `knowledge/_tests/chart-engine/bar.html`.
Only then did **lanes B–F** run in parallel against a core that already existed, each producing a partial, a snippet
that draws from inline DATA, a typed `behaviour` meta, a committed test page, and a Playwright drive across
8/8 themes × light/dark.

The evidence that the split was the right call is in what the lanes asked for rather than what they invented:
every one of them came back with a **request against the core** — a zero-floor clamp escape, a furniture opt-out,
a TOTAL column in `writeTable`, a legend-cache invalidation hook, `dvDonutSweep(figure)` re-entry, a circle branch
in dv-behaviour's fit, `data-series-group` always emitted, `series[i].unit` and `sharedScale` from combo. Six lanes
asking the core for eight things is six lanes that stayed inside one engine. Had the core not existed, those eight
would have been eight private workarounds and no one would have known they were the same eight.

## 3. Driving found the bug that reading could not

Lane A's page was authored with a **2px** gap between bars. Driven, it measured **1.90px**: `dv-fit` rounds x and
w independently, so the gap absorbs both roundings. Nothing in the source says 1.90 anywhere. This is the whole
argument for committed, driven test pages rather than a reviewed diff — and it is why the six pages landed in the
repo instead of in scratch.

## 4. Why two red gates are a ruling and not a defect

At the cut, seven gates were green and two were red.

**The page budget.** `_validate_behaviour` prices a component page against `s250-D1`'s 34,816 budget.
Chart-combo reads **43,518** and Chart-donut **37,787**. The cause is not fat pages: the engine core is priced
**once per member page**, so every chart that composes the engine pays for the whole engine again. Priced once
per PAGE, the combo fits with **607** spare — measured, not estimated. That is three possible answers (price once
per page · raise the budget · drop `dv-legend` from members where the engine draws its own legend) and choosing
between them is a product call about what a page budget is FOR. It is Dave's.

**dv-004 on the donut.** `_validate_dataviz` reads the *static* geometry in the markup; the engine draws the ring
at runtime, and driven it measures **2.199px** — inside tolerance. The gate is not wrong about what it can see;
it is blind to the artefact that now exists. `dv-line-006` and its siblings are the same class, and
[[no-gate-parses-the-artefact]] is now owed twice. The open question is whether driven receipts BECOME the gate
for engine-drawn types, or whether the static gate learns to skip them.

**And so v1.0.8 was not cut.** #257's lesson — a re-bake at the same version launders a hash by the frozen
ledger's own rule — generalises: a release cut over a red gate is the same laundering with a different subject.
The cut waits on the ruling, not on more code.

## 5. What is still open

The eight fast-follower types (`s259-D1`, and his sentence — *"lets not let these be forgotten"* — is the reason
the carry is written by name); the budget ruling; the dv-004 class; the `behaviour.partial` shape (chart-bar names
three partials, the other five name four); `stacked-area` missing from `DTYPE_CANON`, silently skipped since #95;
the donut's five-slice palette cap, its dropped DV-D13 percent column and its baked cd2 labels; the sparkline's
`s182-D3` rag/\*-INK versus `--status-*` rag/\*-GRAPHIC split; rule 18's fate now that the engine exists; and the
≈66 stale showroom pages this wrap declared rather than regenerated.

*Carry set: `_CARRIES.md` § `residual → #260`.*
