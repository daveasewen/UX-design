# #116 — the hit-area checker redesign, and the molecule Dave's question found

**2026-08-06 · Opus conductor · Dave live · ONE window · 1 Opus build sub · commit `2a231f9`**

## What this session was for, and what it became

#116 was titled for `s114-D5` (the hit-area checker measurement redesign) and `s114-D2` (the citation
gate). It delivered D5 and did NOT reach D2. What it also delivered was not on the list: **a
correction to `s114-D6`'s premise**, and **a JS-off accessibility gap on four of five charts** that
nobody was looking for.

## The opener, and two mispricings of the same number

Dave picked "fresh — plenty of room" on quota, then sent the actual reading: **78% used, resets in
3h49m**. The conductor read that as a day allowance nearly spent and **clamped delegation off**.
Dave then sent the full panel: **that 78% was the WEEKLY bucket, resetting in 3h46m; the session
window was at 8%.** ⇒ 22% of a weekly allowance expiring in under four hours is **use-it-or-lose-it**,
which is the OPPOSITE of scarcity. The clamp was wrong in direction and delegation went back on.

★ **The lesson is one already written down and still not applied in time:** NAME WHICH BUDGET BINDS
before picking a posture [[budget-vs-quota-vocabulary]]. The conductor had the rule and still reached
for the number without first asking what it measured. **Twice** — once taking a stated pick at face
value against an available reading, once taking a reading without identifying its unit.

## The tally (⑧) — evidence, and a verdict of "not ripe"

`_graph_edges.py --tally`: **15 lines, ALL dated 2026-08-06, all from #115.** The window had not
advanced. **11 of 15 came from the query `supersedes`** — the word that GUARANTEES the mark fires —
and all 4 ⛔ results carry the same `ADR-0015-A1`/`A2` pair. ⇒ **the sample is self-selecting and
cannot support a demote ruling.** Demotion stays NOT RULED. Granularity is date-only, so #115 and
#116 collapse into one bucket — which bit today, both being 2026-08-06.

⚠ **A near-miss inside the probe:** the conductor searched for a `ts` field, found none, and briefly
held "the recorder emits no timestamp" as a DEFECT. The field is `date`, populated at
`_graph_edges.py:171`. **An unmatched grep is not an absence** [[unmatched-grep-is-not-an-absence]] —
and the wrong key name looks exactly like a missing feature.

## Dave's question, and what it exposed

The conductor priced a **padding patch** for the sparkline's `<summary>`. Dave asked:
*"why is it different? the table button and pop-over should be a molecule consumed by all of teh
charts."*

Chasing that question produced the session's real finding. **`.dv-tablepanel` ships with the `hidden`
attribute in markup (`Chart-bar.reference.html:367`) and ONLY `dv-behaviour.js` removes it.** With JS
off, the table fallback is **UNREACHABLE on bar/combo/donut/line**. The sparkline's native
`<details>` works without JS.

⇒ **The sparkline was not the odd one out because it was worse. It was the only one that was right.**

And it lands on `#116-D1`: Dave let data marks pass at 24 *because* "all chats cary the table fall
back for Ally". They carry it — but on 4 of 5 it was JS-gated, so **the justification was half-true
until D2's convergence repaired it.** The conductor's padding patch would have left that intact and
invisible [[instruction-right-cause-wrong]].

## A premise laundered, and caught

Searching whether "data marks exempt" was already ruled, the conductor hit
`2026-07-25-legend-v5.1-…-brief.md:66` quoting *"every interactive CONTROL presents ≥ target/min via
invisible `::before` + 9-point pin; data-marks exempt"* — which READS as a Dave verbatim. It is
prefixed **"likely INSCRIBE:"** under **"Recommend: … CONFIRM with Dave."** An agent's proposal
wearing a ruling's clothes, caught only by reading the surrounding lines rather than the matched one
[[feedback-dont-launder-a-premise-into-a-ruling]]. Had it stood, the conductor would have "confirmed"
to Dave a ruling he never made — and Dave in fact ruled **STRICTER** (24 floor, not exempt).

## The build, and the two counts the conductor got wrong

Delegated to an Opus sub (203,210 quota; **a sub costs nothing in this window's FILL** — that is what
made a 45-file build fit inside 25K of runway [[delegation-cost-inversion-110]]).

Landed: `knowledge/_a11y_target.py` (new markup-driven engine — DOM, subject-aware cascade, resolved
custom properties, SVG mark geometry) · `_validate_a11y.py` rebuilt onto it with a 25-clause selftest
· **13 charts / 21 panels** converged to native `<details>` · `dv-behaviour.js` table module rebuilt
as clamp + focus + Escape ONLY · **`Video-player` `.scrub`** (`role="slider"`, **4px**) — the one
genuine control the 75-file sweep surfaced, **passing by omission for the entire life of the gate**
because the old allowlist had no name for it. That single find is the sweep earning its keep.

**Conductor error 1:** priced the conversion at **4 charts**. It is **13**.
**Conductor error 2:** the render-verifier asserted `.dv-tbl-toggle count == 0` and reported **12
FAILS**. The class was **RETAINED on `<summary>`** for styling; **zero legacy `<button>` remain**. A
matched class asserted as an element type. ★ **Both errors are one shape: trusting a COUNT instead of
measuring the thing** [[measure-dont-convert-units]].

## The verification the sub declared undone

The sub's own words: *"No render/visual check of the `<details>` conversion — structural assertion
only."* A structural claim is the same shape as a mutation test that proves the CLAUSE and not the
FEATURE [[mutation-tests-the-clause-not-the-feature]]. **The conductor drove it.**

bar/donut/line/sparkline × {1280, 375} × {JS-OFF, JS-ON}: **JS-OFF geometry byte-identical to
JS-ON** · **0 panels `[hidden]`** · summary hit **44×113** (sparkline 44×84) · no overflow at 375
(right 339 < 375). The progressive-enhancement claim is now DRIVEN, not asserted.

⚠ Getting there cost **four wrong attempts** — `chromium` instead of `chromium-headless-shell`,
`--with-deps` (needs root), missing TLS vars, and reading an EXPECTED non-zero host-validation exit
as a failure. **All four are documented in `_RUNBOOK-render-verify.md`, which the conductor read only
after the third.** [[feedback-read-the-runbook]]

## `s114-D6` — a ruling whose premise had aged

The 44-promote was ruled on a **six-failure** premise. The rebuilt gate measured **72 controls in the
24–43 band**, mostly 36×36 and 24×24 expanders the old gate **blind-exempted because it could not see
them**. Dave: *re-price it, don't auto-promote.* ⇒ **`#116-D4`**. His ruling stands; its premise gets
corrected first. ★ **A ruling enforced against a falsified premise is not the ruling Dave made**
[[premise-ages-faster-than-rule]].

Similarly **107 data marks measure below 24** across 6 files, +11 UNMEASURED. Dave: leave at `warn`,
bring the detail ⇒ **`#116-D5`**. **The 11 unmeasured are not clean — they are unmeasured.**

## Declared, not fixed

`_validate_behaviour.py --selftest` is **RED AT HEAD**, pre-existing: page budget **32.9KB reported
PASS against a 32 cap**. The sub kept its JS +6 bytes and did NOT touch the cap — correct, because a
cap raised to clear its own gate is not a cap [[sub-ruled-daves-open-item-110]].

`2a231f9` carries **#115's** banner subject — **third consecutive session**. Verify by hash and diff,
never by subject [[wrap-skipped-chain-certifies-wrong-session]].

## Gauge

Check-in at the D5 seam: **FILL 113,963** vs the **150,929** stop line. The build was delegated
rather than run in-window precisely because 45 files would not fit in 25,770 of runway. Wrap opened
at the seam, not ridden past it. Sub quota: **203,210**. Weekly bucket at 78%, resetting within the
session — the reason delegation was correct rather than extravagant.

## → #117

① **characterise the 72 controls** (`#116-D4`) — costed list before any 44-promote · ② **characterise
the 107 sub-24 marks** (`#116-D5`) + a rendered example · ③ **`s114-D2` citation gate**, four binding
conditions, NOT REACHED #116 · ④ **attribution re-probe (#111-D3) — FOURTH CONSECUTIVE ROLL** ·
⑤ `_validate_behaviour.py` 32.9-vs-32 pre-existing red · ⑥ inscribe the hit-area rule into the a11y
guideline + `_DATAVIZ-DECISIONS` (the sub left the record in the brief only) · ⑦ **form fields
declared UNSWEPT, not clean** — sweeping them re-created the phantom shape · ⑧ P4 `_CHAIN.md` trim
11,345 · ⑨ the 19 `_state.LEGACY_IDS` · ⑩ Apollo enact queue, still PARKED by Dave · ⑪ the
observation-window tally needs VARIED queries before demote can be ruled.
