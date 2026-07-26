# 2026-07-26 — Legend wave lane ①: Chart-bar migrated, ds-010 closed by render, and three corrections to a Red-authored record

provenance: local_b5710d97-4b9f-4452-9164-7ffae8ac43f9 · 2026-07-26
status: observed — enactment of DV-D11/12/13 (ruled `_proforma/_DATAVIZ-DECISIONS.md`) and closure of ds-010; the three record corrections are findings, not rulings

Spine entry: `_LIVE-STATE.md` ⏱ LATEST 2026-07-26 (evening, legend-wave lane ① session).
Predecessor: `_DECISION-HISTORY/2026-07-26-behaviour-cap-fork-and-legend-enactment.md` (the session
this one re-verified). Commit: `aabe617`.

---

## Why this dossier exists

The session opened to run three mechanical lanes and instead spent most of its value on something
else: **the handoff it inherited was authored at 🔴 ~72%, and three of its claims were wrong.** All
three were wrong in the same quiet way — plausible, specific, and load-bearing for the work three
more lanes were about to do. The Red-scrutiny rule caught them because it was actually run, not
because anything looked suspicious. That is the finding worth keeping.

---

## 1. The re-verify earned its keep — and what "re-verify" has to mean

The rule says a Red-authored handoff gets re-verified before anyone builds on it. The cheap reading
of that rule is "re-run the gates". Doing only that would have passed cleanly and taught nothing:
`_build_all.py` came back **55/55 GREEN** and `_verify_dv_legend.js` **27/27**, exactly as claimed.

The claims that failed were the ones **no gate covers** — prose instructions and quoted numbers:

- the executable end condition, which no gate runs;
- the byte figures, which the gate recomputes but never compares against what a document *says*;
- the copy-source's own header prose, which every downstream lane reads and no parser touches.

⇒ **A Red re-verify has to include the assertions a gate cannot see.** Gates protect the mechanical
surface; the handoff's *narrative* surface is exactly where Red-authored error concentrates, because
that is the part written last and under the most heat. Re-running the build is necessary and not
close to sufficient.

## 2. The end condition could never fire — and my own first framing of that was too strong

The handoff instructed: delete the transitional block when

```
grep -l data-series-toggle knowledge/snippets/Chart-*.reference.html
```

returns nothing. Run cold, it matched **all five** snippets — including `Chart-donut`, which had
been fully migrated the session before. Cause: the transitional block's own source contains the bare
string (`button[data-series-toggle]`, `getAttribute('data-series-toggle')`), and
`gen_component_partials.py` injects that source into every registered member between the
AUTO-BEHAVIOUR markers. The check could only go quiet *after* the deletion it was meant to authorise.

**The correction to my own correction.** My first write-up said a grep "cannot" discriminate. Building
the replacement tool disproved that: grepping the **markup form** `data-series-toggle="` (with the
equals-quote) discriminates perfectly today, because no injected JS spells it that way. Both columns
are printed side by side by `--verbose` in the new script, so the claim is checkable rather than
asserted.

That is a materially different — and weaker — finding than "grep cannot work", and it went into the
record that way. The reason to still prefer a script is narrower and worth stating precisely: **the
grep works on punctuation luck, and it fails in the dangerous direction.** If the markup form ever
changes shape, the check reports COMPLETE and authorises deleting a block four members still depend
on. A deletion gate should not hinge on a coincidence of punctuation.

⇒ `knowledge/_check_legend_migration.py` strips the injected regions — the distinction actually being
drawn — and reports per member. Exit 0 is the authorisation. Current output: donut ✅ bar ✅, scatter
and sparkline carry no legend, **combo and line remain**.

*(This is the second time in two sessions that a first-pass framing needed walking back inside the
same hour — cf. B-D7's two beats. Both beats stay in the record; that is the point.)*

## 3. The byte figures were predictions wearing the clothes of measurements

The handoff quoted per-source **12,682 + 15,650** and page **31,268 B (95%)**. On disk:
**15,618 + 15,719**, page **31,337 B (96%)**.

The second number was 69 B out — rounding-adjacent, ignorable. The first was out by **2,936 B**, and
the shape of the error explains itself: 15,618 − 3,569 (the transitional block, measured) = **12,049**,
which is within ~600 B of the quoted 12,682. **The figure quoted as *current* was the *predicted
post-deletion* size.** The conclusion it supported was sound; the number attached to it was not
measuring what its label said.

⇒ Post-deletion actually lands at **~27,768 B (85%)**, not the 28,332 B (86%) written down. Small
absolutely, but it is the number the next three lanes would have planned headroom against.

⇒ **Predicted values and measured values must not share a sentence without a word marking which is
which.** Under context heat the distinction is the first casualty, and neither is falsifiable later
without re-measuring.

## 4. The copy-source was documenting a model it no longer ran

`Chart-donut.reference.html` is the wave's designated copy-source: three lanes were told to read it,
not the prototype. Two of its comments were wrong.

- **Header §3** still described the SUPERSEDED legend — `data-series-toggle` buttons, shift-click
  isolate, `.dv-quiet` highlight, "centre total keeps the FULL total" — as the live behaviour. Every
  clause of that had been reversed by DV-D11/DV-D13 the session before.
- **The migration comment** claimed the file's dead `.dv-legend*` rules "still serve
  Chart-bar/combo/line, which have not migrated yet". They cannot. Snippet CSS is hoisted into
  `canon.css` **namespaced per component** (`.cn-chart-donut .dv-legend{…}`), so it can never reach
  another member — each carries its own copy. `.dv-quiet` is the one real exception, because the
  injected transitional block still references it.

Neither error would have failed a gate. Both would have been faithfully copied three times.

⇒ **A file promoted to "copy-source" needs its prose re-read at promotion time.** Its comments stop
being documentation and start being instructions the moment other lanes are pointed at it.

## 5. Chart-bar: what was actually mechanical, and what wasn't

Genuinely mechanical: the dual-gesture markup, the `.dv-leg*` CSS port, the ladder, the live regions,
the Reset, the `extraContract` swap. Not mechanical, and not visible from the divvy:

**(a) Bar has TWO legends on one page.** The donut had one, so nothing had ever tested whether
per-legend state was really per-legend. Reading `dv-legend.js` first showed it *should* hold — state
keys on the host `.dv-leg`, the figure resolves via `closest('figure')`, events delegate through
`closest('.dv-leg')`. Rather than trust the reading, the new suite drives both legends and asserts
non-interference directly: toggling cb4 must not ghost a mark in cb5, must not enable cb5's Reset,
must not write to cb5's live region. It held, 8/8. **Reading the source is a hypothesis; the test is
the evidence.**

**(b) The swatch shape channel.** Bar's legend carried `.sw-circle` / `.sw-square` / `.sw-diamond`.
The donut model's swatch is a plain square with `--sc`. Porting naively deletes a non-colour channel
— normally an accessibility regression. Checked the marks: bar's are `<rect>`, and its actual
non-colour channel is the **letter key** drawn on the bars (`.dv-barkey` A/B/C), exactly as on the
donut. The swatch shapes encoded nothing; a diamond swatch promised a diamond mark that never
existed. Dropped, and **registered as a visible delta for Dave** rather than decided silently.
**Chart-line's markers genuinely are circle/square/diamond** — lane ③ earns shape modifiers there,
where real geometry backs them. Deliberately not built speculatively in lane ①.

**(c) The typed-tip step didn't apply.** Bar's only seg is SORT (`orig`/`asc`/`desc`), not
value⇄percent. Confirmed by reading the DV-D13 handler that it no-ops on an unknown mode
(`fig.querySelectorAll('[data-tip-orig]')` → empty) rather than clearing tips.

## 6. ds-010: closed, and closed the way it was found

ds-010 was a **render** finding, so a reasoning-only closure would have been the wrong currency. The
fix is one deleted line — `rect.dv-series{fill:var(--sc,var(--data-series-1));}`, author CSS beating
each rect's `fill=` presentation attribute while `--sc` was set on no rect, collapsing everything to
the fallback.

Playwright was staged from scratch per `_RUNBOOK-render-verify.md` (the runbook held; no new
potholes). Proof at 1180px **and** 760px in the licensed cut, reading `getComputedStyle(rect).fill`
per figure rather than eyeballing pixels:

| figure | distinct fills | reading |
|---|---|---|
| cb1 column | 1 | `rgb(118,102,130)` series-1 ✓ |
| cb2 horizontal | 1 | `rgb(87,124,120)` series-3 — **DV-D09 restored** |
| cb3 status | 4 | `rgb(185,47,30)` #B92F1E · `rgb(197,137,0)` #C58900 · green · blue — **R-D9 ramp restored** |
| cb4 / cb5 | 3 each | the three series ✓ |

Before the fix, every one of those was a single purple.

A comment now occupies the deleted line's place, saying why a CSS `fill` must never return. **The
anti-false-fix provenance matters more than the deletion** — without it the line reads like dead code
and comes back.

## 7. ds-012 — the same render, the next defect down

With the pipeline up, the render also showed **all six horizontal-bar category labels clipped at the
left edge**: "Groceries" → "oceries", "Utilities" → "Jtilities". Measured per label via `getBBox()`
rather than described: labels sit at `x="38"`, `text-anchor="end"`, so they grow leftward out of a
viewBox whose origin is 0. Worst case "Groceries" needs 54.8px against a 38px gutter — **16.8px of
overflow**, six of six clipped.

This is [[univers-measured-facts]] biting **geometry**: the HSBC cut is looser than Helvetica, so a
gutter sized against a fallback face fits and the same gutter against the licensed face does not. It
is invisible in any render that falls back — which is precisely why the runbook asserts
`document.fonts.check('16px HSBC_MtUnivers_Latin')` before shooting.

**Deliberately not fixed in lane ①.** Widening the gutter re-bakes every `x`/`width` on the figure —
a geometry change to a reviewed artefact, not a legend migration. Logged as ds-012 with two candidate
shapes for Dave and a recommended gated assertion (`no text.dv-label has getBBox().x < 0`), together
with the honest note that such a gate must run in a browser and today cannot.

⇒ Standing pattern, now twice: **ds-010 and ds-012 were both found by rendering the real snippet in
the real cut, and neither is reachable by any static gate we have.** Two of two suggests the render
step is not a nicety on this pillar.

## 8. What this cost, and the call at the end

The three corrections were not in the plan and consumed most of the window. Chart-bar landed
complete, verified 54/54 and render-proven; **combo and line did not start.**

Offered Dave the choice at ~65% (Amber, edging Red) and recommended wrapping rather than pushing
through. The reasoning is this session's own evidence: everything it had to correct was authored by a
capable session running past its clean budget, and the errors were not sloppy — they were *specific,
plausible, and load-bearing*. Producing two more members at the same heat, on the file three lanes
copy from, would trade a day of someone else's trust for an hour of tonight's throughput. **He took
the wrap.**

---

## Resolved state

- **Chart-bar MIGRATED** — both legends, verified **54/54** (`_verify_dv_legend_members.js`),
  render-verified 1180 + 760 in the licensed cut. Commit `aabe617`.
- **ds-010 CLOSED**, render-proven; **ds-012 LOGGED**, not fixed.
- **End condition now executable** — `_check_legend_migration.py`; the broken grep is corrected in
  `dv-behaviour.js`, in this dossier and in `GOOD-MORNING`.
- **Copy-source prose corrected** on `Chart-donut.reference.html` (both errors).
- **Donut render-verify owed → discharged.**
- Build **55/55**, exemplar **27/27**, page budget **31,490 B (96%)**.

## Still open

- **Lanes ② and ③** — Chart-combo (+ DV-D10 lockups), Chart-line (+ shape modifiers, 3 rows). Then
  the transition closes: delete the transitional block, promote `class="dv-legrow` to the universal
  contract, drop it from the four extraContracts, delete each member's dead `.dv-legend*`/`.dv-quiet`
  CSS. Authorisation = `_check_legend_migration.py` exit 0.
- **Dave's eye:** the swatch-shape delta (reversible on request) · ds-012's fix shape · the two v5.5
  gate-forced deltas still outstanding from the prior session. All in `_REVIEW-SIGNOFF.md`.
- **`_verify_dv_legend*.js` remain unwired** from the build (need jsdom). Two suites now, not one —
  wiring them as advisory is a bigger prize than it was this morning.
- **dv-legend.js has ~665 bytes of headroom.** Every lane must stay snippet-side; the moment one needs
  the shared source, the cap fork reopens mid-wave.
