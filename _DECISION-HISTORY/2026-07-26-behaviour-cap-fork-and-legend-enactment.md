# 2026-07-26 — The behaviour-cap fork, and the first enactment of the legend model

provenance: local_681bb3eb-656a-4a3f-9f2c-4c8e723e0169 · 2026-07-26
status: ruled — ADR-0015 § Amendment (2026-07-26); registry `component-type/dataviz/$behaviour/dv-legend`

Spine entry: `_LIVE-STATE.md` ⏱ LATEST 2026-07-26 (evening, legend-wave session).
Sibling: `_DECISION-HISTORY/2026-07-26-legend-signoff-additive-isolate.md` (the sign-off this enacts).

---

## Why this session exists

The window opened to enact DV-D11/12/13 — signed off ninety minutes earlier — into
`dv-behaviour.js` and the chart snippets. The handoff called it mechanical: *"lanes ①②③ = Sonnet,
default effort (mechanical enactment of inscribed specs)."* It was not mechanical, and the reason
is worth recording, because the same shape will recur.

## Finding 1 — the enactment was blocked by a constraint nobody had priced

`dv-behaviour.js` measured **15,526 B against a 16 KB blocking cap** — 858 bytes of headroom. The
v5.5 controller is ~14,100 B. Three arrangements were measured before concluding, rather than one:

| arrangement | result |
|---|---|
| port as written | 26,615 B |
| strip every comment | 22,364 B |
| strip comments AND abandon DV-D12's sweep | 21,327 B |

None passed. **Measuring three ways mattered** — the cheap answer ("strip the comments") is the one
a hurried session takes, and it would have failed the gate anyway after destroying the provenance
trail. A single measurement would have looked like a tuning problem; three showed it was structural.

The question was already in the record twice — as §C·2 #18, and inside the registry's own
`$description` ("DEFERRED to Dave: amend the cap vs modularise per family"). It had simply never
been on the critical path before. **A deferral is not a decision, and the queue is not a place
where questions go to resolve themselves.**

## Finding 2 — the fork, and why "split only" was the wrong half of the answer

Two things were verified before putting options to Dave, and both changed the recommendation:

- The generator and the gate **already iterated** `$behaviour` entries (`for bname, beh in
  behs.items()`), with the marker regex keyed per name. A second source therefore cost a registry
  entry and a marker pair — no tooling change. That made splitting far cheaper than assumed.
- Which is exactly why splitting alone was dangerous. **Two sources each under 16 KB pass a 16 KB
  per-source gate while the page doubles.** The constraint would have degraded from a page budget
  to a file budget, silently, and the gate would have read green throughout.

That is the same failure shape already inscribed in this project: *a gate measuring the proxy
instead of the thing* (the declared-pairs-only contrast blind spot, where 9/9 meant "checks
passed", not "done"). Naming the precedent is what made the recommendation firm rather than
balanced. Dave ruled **split AND re-scope**.

The same defect was then found a second time in the same function: the "exactly ONE rAF-debounced
resize listener" check was also per-source, and would have failed `dv-legend.js` for carrying
**zero** — which is correct for a source with nothing to reflow. It moved to group level under the
same ruling, as a consequence rather than a new decision.

## Finding 3 — minification, asked and declined

Dave asked mid-build whether minifying would help. It would have — the numbers are real: 28,332 B
raw → **9,622 B gzipped**, and gzip is free at the transport layer. The answer was still no, and
the reason is the point of the whole session: **the cap is a complexity forcing function, not a
wire-weight budget.** ADR-0015's own words are "headroom, not a target" against a 9.9 KB baseline.
Minifying shrinks the number without simplifying the thing, and lets the source sprawl while the
gate reads green — the identical error we had just closed. Three narrower costs sat behind it: the
reference snippets carry the injected block inline and must stay readable; the comments are the
provenance trail; and a minifier adds version-drift to a byte-exact `--check`, days after the dream
pass fixed emitter determinism.

## Finding 4 — two things the divvy plan had wrong, found by looking

- **The wave is four members, not three.** `Chart-line` carries a legend (3 rows). The handoff's
  lanes were donut/bar/combo — the prototype only ever exercised bar and donut, so line was never
  in view. Removing the old model would have left line's legend as inert markup.
- **`.lg` collides with canon.** The prototype's legend list class means "legend"; canon's
  `.seg.lg` means "large". The blast-radius gate caught it on first build — the family was renamed
  `.dv-leg*`. The state classes kept their names, because DV-D11 inscribes `.is-ghost` /
  `.is-faded` / `.is-peek` verbatim; renaming them would have contradicted a signed-off ruling to
  satisfy a naming preference.

Both are arguments for *surveying before building* even when the brief says mechanical. Neither
was discoverable from the handoff; both were one grep away.

## Finding 5 — the transition, and why coexistence beat a big-bang

Stripping the old legend left four snippets with dead markup — an uncommittable state. The
alternative to "migrate all four tonight" turned out to be structural rather than a compromise:
**the two models are selector-disjoint.** The old one keys on `button[data-series-toggle]`, the new
on `.dv-legrow`. A migrated snippet is served only by the new model, an unmigrated one only by the
old, with no overlap and no double-binding. So members migrate one at a time with every commit
working, and the old block carries an explicit end condition rather than a vague intention:

> delete when `grep -l data-series-toggle knowledge/snippets/Chart-*.reference.html` returns nothing.

The registry's universal contract for `dv-legend` is **empty by design** during this window —
there is no hook every member carries yet — with the hooks riding each migrated member's
`extraContract`, and a written instruction to promote the hook when the last member arrives. An
empty contract that says why is honest; one that pretends to be universal would not be.

## Finding 6 — gates bit the resurrected work, exactly as the rule says they should

The v5.5 prototype was signed off but never gate-bound. On first build it failed the 4px grid
(`padding:5px 9px`) and the radius gate (`border-radius:2px` hardcoded). Corrected to 4px/8px and
`var(--border-radius-default)`. This is the standing rule working — *resurrect-verbatim is not
gate-exempt* — and it is the second time it has bitten a Dave-approved artefact (the 273d18c~1
stepper's 13px/3px → 12px/4px). ⚠ **The corrected paddings are a small visual delta from what Dave
signed off** and are flagged for his eye, not buried.

## What landed

- `knowledge/canon/dv-legend.js` — 15,650 B, the DV-D11/12/13 model, delegated events, no per-row
  listeners, progressive enhancement preserved.
- `knowledge/canon/dv-behaviour.js` — legend logic isolated behind a marked TRANSITIONAL block with
  its deletion condition; core (fit/tip/table/seg/csv) unchanged.
- `_validate_behaviour.py` — `check_group` + `PAGE_BYTES`; five new selftest bites including the
  evasion case. Selftest OK, gate green.
- `component-types.json` — `dv-legend` registered; donut's contract migrated to the new hooks;
  the deferral in the old `$description` marked RULED rather than deleted.
- `Chart-donut.reference.html` — legend rebuilt to the dual-gesture model, typed tips, live region,
  Reset; four other members carry the (inert) marker pair.
- `knowledge/_verify_dv_legend.js` — **27/27**, driving the real source against the real snippet in
  jsdom, including Dave's signed-off figures (950/41%, 1250/54%).
- Build **55/55 GREEN**.

## Open, carried forward

1. **`Chart-sparkline` carries an inert 15.6 KB payload** — injection is group-wide and the
   registry has no per-member behaviour opt-in. Flagged to Dave, not decided.
2. **Page budget is at 86%** post-transition (95% during it). The next behaviour addition faces
   this same fork — by design.
3. **Bar, combo and line still to migrate**; the transitional block and the empty universal
   contract both close when they do.
4. **`_verify_dv_legend.js` is unwired** — it needs jsdom, which is not a build dependency. Wiring
   it as an advisory step, or vendoring the check, is an open call.
5. **The grid-corrected paddings** await Dave's eye (Finding 6).
