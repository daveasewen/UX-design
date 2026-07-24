# 2026-07-24 — Chart fan-out absorb, the per-capability behaviour split, and "dark-mode-in-light" (O1)

*Dossier for the Opus CONDUCTOR window (afternoon→evening). Records the WHY/HOW; the WHAT is in
`_LIVE-STATE` (LATEST DELTA + SAME-WINDOW FOLLOW-UP) and the commits `ecf6e56` (reconcile) + `93c01c1`
(quick wins). Both-way links: spine → this file; brief `notes/_briefs/2026-07-24-dark-in-light-O1-and-chart-followups-brief.md`.*

## Arc 1 — absorbing the three lanes, and re-verifying rather than trusting

The window opened as conductor for the chart fan-out: three worker lanes had landed (bar+scatter,
donut+sparkline, net-new combo) as receipt-only, and the job was absorb → reconcile → ONE commit.
The lane receipts were authored at **Red ~65–68%** (lanes ①③) and Amber ~58% (lane ②). Per the
gauge-stamp practice, Red-authored ⇒ re-verify. So I re-ran every gate from a clean state instead of
trusting the receipts' green claims. Two things this caught that trust would have missed:

- **A stale-file trap.** First build capture redirected to `/tmp/build.log`, which was permission-denied
  (owned by a prior session) — and `grep` then read the STALE file, reporting `65 snippets` / a
  passing build that never ran this turn. The `65` (vs the real `67`) was the tell. Fix: write build
  logs to a session-owned dir (`outputs/`), never a fixed `/tmp` name. Same class as the runbook's
  stale-msgfile trap.
- **The receipts' green was real but incomplete** — see Arc 2.

## Arc 2 — the per-capability behaviour split (the session's real engineering)

**The setup.** dv-behaviour.js (the ADR-0015 single-source JS partial) is injected into each registered
dataviz member, gated by a contract: `requires.{vars, declarations}` + `$manifestBinds`, applied
UNIFORMLY to every member. When only Chart-line was a member, "the contract" was silently just
"everything Chart-line has." Registering the four new charts meant they had to satisfy that same flat
contract — and they legitimately don't.

**The method — measure, don't guess.** I was about to reason about which hooks were universal; instead
I built a **hook matrix** (`grep -c` each hook across all five files). It showed the contract is
effectively a multi-DIMENSIONAL capability space, and the charts sit at different coordinates:
- `data-tip` (popover) — universal (all 5).
- `data-fxs` (polyline fit) — line + combo only (bar/donut fit by rect/arc; sparkline by CSS).
- table + legend hooks (`dv-tbl-toggle` · `data-series-toggle` · `dv-tablepanel`) — all but sparkline.
- (later) the DV-D07 axis/grid **vars + manifestBinds** — line/bar/combo carry axis+grid, donut axis
  only (radial, no gridlines), sparkline neither (axis-free).

**The fix, and the second-pass correction.** The exemplar receipt had pre-authorised this: "split the
contract per-capability THEN, from observed need, not now." Now observed. Implementation: reduce the
universal contract to the one universal hook, move the rest to each member's `$members[…].extraContract`,
and make `check_contracts` merge universal + per-member (an additive optional `extra` param; injection
logic untouched so Chart-line can't regress) + a selftest bite.

The correction that justified the re-verify discipline: my FIRST pass split only `declarations`. The
dry `--check` then failed on donut/sparkline for missing `requires.vars` + `$manifestBinds` — the
axis/grid chrome is ALSO not universal. So `extraContract` had to carry vars + declarations +
manifestBinds, and the universal `requires.vars`/`$manifestBinds` emptied. A declarations-only split
would have shipped a contract that still lied about donut and sparkline. Build then green + idempotent,
5 members, module 14.3KB < the 16KB cap.

**Deferred, cleanly:** the donut SWEEP hook would push dv-behaviour.js to 17,360B > the 16KB cap — but
it's a SEPARATE future hook; the existing under-cap module injects fine, sweep stays baked-static. So
registration did NOT force the cap decision (amend cap vs modularise per family) — that stays Dave's.

## Arc 3 — "dark-mode-in-light-mode" (O1): Dave converged on the architecture

Dave's post-reconcile edits pass ("quick wins, mint but flag later"). The interesting one was the
dark-surface text seam (lane ③'s COMBO-LINE-INVERT R-B/R-C): text on a dark series fill needs light
ink, but `type26-013` (blocking brand: white type is red-only) forbids it.

I offered option 1 = "mint a narrow inverse-ink token." Dave pushed back with the better framing:
*"is this a solid solution for all light-mode-on-dark situations… essentially we need a dark-mode in
Light-mode when the background is dark."* He'd independently named the GENERAL pattern — a dark island
in a light page re-resolves its own ink — which a per-spot token can't be.

The reframe I gave back, and the key finding: **this is not new architecture — it populates an
ADR-0014 slot.** ADR-0014 already classifies surfaces and carries inverse resolution (SC's dark
provisional already remaps its neutral anchor); "dark island re-resolves its ink" is the same move
scoped to a subtree. The honest consequence I had to state: doing it Dave's (correct) way is a **small
ADR, not a quick win**, because a real solution needs BOTH (a) the scoped dark-surface classification
that re-resolves ink and (b) `type26-013` scoped to EXEMPT light ink inside a declared-dark surface —
otherwise the gate correctly blocks the very thing we're minting. I resisted selling it as a quick win.

Dave: *"lets do it but it will probably needs its own sesh."* → RULED: do it as O1, its own fresh
window with render-verify working. Brief cut. This supersedes the old "R-B/R-C open" deferral. This is
the recursive-magpie pattern in memory: Dave's divergence found the real pattern, my job was to
converge it onto the existing ADR slot rather than let it become a carve-out.

## Arc 4 — quick wins + what stayed flagged

- **Popover-over-trigger FIXED** (`93c01c1`): the table panel was pinned at a fixed `top:44px` from the
  figure; a title pushed the toolbar past it so it opened over its own button. Now anchors below the
  trigger (measured via `getBoundingClientRect` vs offset parent). All 5 charts. Render-verify owed.
- **Legend isolate redesign** (Dave's idea, PROPOSED, awaiting confirm): label→radio-isolate,
  swatch→checkbox-toggle, additive. a11y-real (two roles/row) ⇒ flagged, spec in the brief, NOT built.
- **Mini ramp**: confirmed present (T-D15, med/12·med/14·reg/16) + applied (chart text 12/500). Wrinkle:
  charts use parallel composites vs the `ctl-*` ramp; agree at 12/500. Optional unify later.

## Resolved state / still open
LANDED: fan-out absorbed + reconciled (`ecf6e56`); per-capability split enacted; popover fixed
(`93c01c1`); 5 charts wired; build 53/53. OPEN for Dave: dataviz sign-off (5 live panes); O1 session
(next); legend-isolate confirm; sweep 16KB-cap fork; Q2 combo-home; scatter Layer-2; brush spec;
JS-off seg wart; render-verify (standing sandbox blocker). Model: Opus; effort not separately set.
