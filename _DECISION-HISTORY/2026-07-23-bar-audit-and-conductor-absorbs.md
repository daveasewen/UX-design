# 2026-07-23 — The bar audit, three rulings, and the first two-lane conduct (evening session)

*Dated from `date` (Thu 23 Jul 2026, ~20:00 BST). Session: opened as the Chart-line exemplar build,
became the bar audit + conductor window — the drift is the story. Spine: `_LIVE-STATE.md` LATEST
delta 2026-07-23 evening. Ledger: `_DATAVIZ-DECISIONS.md` DV-D08 · DV-D09 · D-Q3. Sheet:
`reviews/BAR-CHART-AUDIT-2026-07-23-v1(.REVIEW).html`. Commits: `db36e72 · db1ed1b · f887efd`.*

## The arc

**Dave's two hunches beat the record again.** Mid-question he said the last bar work "lost a few
things" and later "I think we might have lost the responsive behaviour." Both checked TRUE — but the
deeper find was that MY Q8 framing was itself contaminated: I offered "mint one 12/500 composite"
as the recommended option, which would have INSCRIBED the very flattening the 07-22 label snap
caused (kit ladder 400/600/700 → uniform 500, `99fcb6d`). He caught it with "I didn't answer Q8
properly." Lesson, same class as attribute-the-diff: **when a decision option was derived from a
possibly-degraded state, audit the state before offering the option.**

**Method that worked:** git archaeology (file sizes across history proved the proforma intact;
the snap diff isolated the flattening) + mechanical feature counts (`data-fx` per section: proforma
bar 24/23 wired, ALL FIVE canon snippets zero) — so every audit claim carried a number, not a vibe.

**"Review sheet, not tuning sheet" (Dave, mid-flight).** Yesterday's Q6 sheet was a dial-heavy
decision instrument; today he wanted findings to READ and pin. The distinction is now real in the
repo: tuner = live controls for value choices; review sheet = categorised evidence (chips:
Lost/Restore-planned · Needs-ruling · Flag) + live specimens + numbered asks.

**The file:// iframe wall + the borrow.** First render: perfect chrome, three BLANK panes —
Chromium blocks `file://`→`file://` subframes, and Dave's Finder-open would hit the same. The
showroom already solved this (base64 payload iframes); borrowed it, inlining `../canon/type.css`
into the canon payload (a data: document can't resolve relative hrefs). Render at 1400 + 840 then
SHOWED the finding itself: proforma reflows, canon clips. Runbook's ≥2-widths rule earned its keep
on its second outing.

## The rulings (why-shape, values in the ledger)

- **DV-D08:** Dave's floor instinct won over kit-fidelity for labels ("at 12 — medium is the
  floor"), but emphasis SURVIVES as 700 — his donut image's legend alphas were the tiebreak. The
  600 collision was surfaced, not silently mapped: he chose 700 over amending the weight canon.
- **DV-D09:** B3 as asked ("revert to the green") was answered with a REFRAME — he doesn't care
  about the hue, he cares that orientations LOOK DIFFERENT by default, because the planned Apollo
  EDIT MODE makes the hue a designer choice post-generation. dv-014 survives as a journey rule.
  A component-default vs journey-consistency distinction now exists that didn't this morning.
- **D-Q3:** one word ("yes") — promotion rides the wave's bar lane.

## The conduct

Dave's "another session" turned out to be the ROUTING SIDEQUEST, not the chart-line worker. Its
receipt was complete (13/13 ratified + enacted in-session at Dave's override); absorb = attribute
every dirty path (one unlisted path, `_LIVE-STATE.md`, resolved as MY build's auto-lifecycle block
— the name-every-path reflex again), commit theirs with their handed message, then mine. One
history surprise: `a2acc9e` landed mid-conduct (the afternoon session filing the sidequest lane
post-wrap) — no conflict, but "single writer" now demonstrably includes idle-but-open windows.
Receipt duties executed: Mode-2 memory hooks demoted to DELIBERATE, harness-template spin-out
registered in `_FUTURE-STATE`.

## Open at wrap

Chart-line worker window NOT yet started (opener line standing in the handoff). Dave's remaining
set: the 15-Q batch (D-Q3 struck) + dataviz sign-off + revisit Q2–5, 7 + scatter eyeball.
Q8 is RESOLVED (DV-D08) — struck from every queue this wrap touches.
