# #194 — the standing 44 did not reproduce, and the a11y duty turned out to be label+glyph

provenance: 194 · 2026-08-17
status: observed

*Links both ways: spine entry `_LIVE-STATE.md` ⏱ LATEST DELTA #194 · ledger `knowledge/_rulings.json`
§ `s194-D1` and § `s194-D2` · banner `GOOD-MORNING.md` ★ LATEST #194 · worker receipt
`notes/_receipts/2026-08-17-194-apollo-on-claude-worker.md`. Written by the delegated OPUS wrap sub from the
conductor's brief and the repo's own record; ⛔ nothing here is ruled by this document, and both rulings were
inscribed by the conductor before this file existed.*

---

## Why the session went where it went

#193 closed on a claim it had every reason to believe: the first full 120-step chained build had reported a
**standing 44 never-green steps**, and that number went onto the banner as residual ①, marked DAVE'S. The
opener chose it. Dave's words picked the triage first, then the mono fix, and his words governed the rest —
including the moment, later, when he redirected the parallel worker off the lane the divvy recommended.

The session ran as a FABLE conductor with four OPUS subs: two build, one warn-tier, and this wrap.

## Finding 1 — the 44 was bookkeeping, not failure

The premise did not reproduce. A **chunked 120-step composed pass at the #193 HEAD `2c2f481`**, with coverage
verified **1–120 contiguous**, measured **four** not-green steps:

- `[34]` the contrast gate — the parked base red 30, a known and ruled park;
- `[59]` dashboard sync — stale, and regenerated in-session;
- `[70]` / `[71]` — honest **exit-77** refusals at the browser tier, green in CI.

The 44 was **visibility debt**: steps that had never appeared inside a green verdict, counted by bookkeeping
rather than by failing. That is a completely different object from 44 live failures, and it is the kind of
number that becomes a programme if nobody re-measures it.

⚠ The honest limit, declared rather than smoothed: **the CI log is the arbiter for the CI count, and it was
never read from the sandbox.** Four is a LOCAL measurement. A later session that quotes 4 as the CI figure will
be repeating the same mistake this finding corrects, one level down [[measure-dont-convert-units]].

## Finding 2 — the first shape of the mono fix was stopped, and that refusal is why a ruling exists

The `[34]` row that mattered was mono's white-on-error pair. The first shape of the fix was **row removal by
exclusion** — make the row not appear. A build sub **stopped it against `s149-D1`**, and did the arithmetic that
made the stop non-negotiable: **no darkened red passes both white text and dark ink** — the window is
arithmetically empty, and `#B92F1E` fails black at **2.89**.

That is the whole value of the six-beat ladder in one beat: the measurement, not the preference, closed the
option.

Dave then ruled the third way — **warn, not error** — and cited his own precedent trail while doing it:
`s169-D1`, `s172-D1`(6), `s116-D5`, `s114-D3`. Retrieval **confirmed all four inscribed**. He was not proposing a
new principle; he was pointing at one he had already ruled four times [[retrieval-default-hides-the-ruling]].

## What `s194-D1` actually says, and what it cost to enact

The duty attaches to **label + glyph, never roundel chrome**. Mono white-on-error is an **abolished state** inside
the `s149-D1` scope. Pairs of that kind **report at WARN (minor), non-gating, never silenced**.

Enacted in `036e014`: a severity vocabulary **pass / minor / gating** in `_build_surface_contrast_audit.py`;
theme-scoped `MINOR_PAIRS` in `_contrast_utils.py`; a **first-match bug in `_excluded_surfaces` fixed** (found
while building, not while looking for it); **31 selftest arms**; **both mutation directions proven**. The gate is
green **with the mono row visible as ⚠ minor** — which is the point of the tier: the defect is reported, not
hidden.

⚠ The sha is **post-amend**. A window-2 file slipped into the staged set through a **case-blind grep filter**, was
un-staged by the documented amend-from-a-fresh-msgfile remedy, and the amend rewrote `3e8ab15` into `036e014`.
The brief this wrap was handed still carried the pre-amend sha; `git log` is what settled it
[[ritual-output-is-not-evidence]].

## Finding 3 — the parallel window went somewhere the divvy did not recommend, on Dave's word

The worker window produced the **Apollo-on-Claude architecture brief** (`W-34`), committed by the conductor at
`1829386` with its receipts. The override of the divvy's recommended lane is **declared in the receipt itself**,
which is the only way a later reader can tell a redirection from a drift.

`s194-D2` then ruled the shape: **Apollo-on-Claude IS a lane, and it is PARKED**, with the trigger being the
**Claude-design POC at Dave's work**. D2–D5 — private plugin, read-only engine first, crescent probably,
design-Apollo initially with Memento-as-product floated — are **recorded LEANINGS**. ⛔ They are not rulings and
must never be laundered into rulings [[feedback-dont-launder-a-premise-into-a-ruling]].

## Two reconcile misses, both caught, both declared

1. the worker's `knowledge/_state.json` `W-34` row was swept into `036e014` **mis-attributed**;
2. the **doc-row gate refused the conductor's own unrowed divvy brief** — the forgotten-document class caught
   **live, by its own gate**, which is what a gate is for [[forgotten-document-class]] — closed by adding `W-35`.

Both are the same underlying defect: **staging by grep filter instead of by git pathspec**. That is written on
the banner as a pitfall because it has now cost two catches in one window.

## What is still open

The ds-0nn chart-intent reconciliation was **not opened for a third consecutive session** — priced and
deliberate, on Dave's own word (*"wrap"*), and it is #195's titled opener on its own terms, governed by
ADR-0017. The CI count remains unread. `2c2f481` was already on `origin` at this session's boot while #193's
summary recorded it as awaiting Dave's push word — **declared to him, unexplained, and this wrap does not
adjudicate it**. The per-theme dedup leak (a theme adopting mono's exact error hex would inherit the MINOR
silently) is **flagged, not fenced**.

⚠ And the consequence that outlives the session: **the WARN tier is a route for real defects to become unread
warnings.** The fences today are the A7b/A7d arms plus the exit-code construction, and **exactly one row is
minor**. A second minor row deserves suspicion before it deserves a rubber stamp
[[instrument-without-a-consumer]].
