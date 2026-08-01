# #70 — DV-D18 splits what DV-D17 conflated, a check that survives its own reversal proves nothing, and the review radios get wired at last

provenance: 70 · 2026-08-01
status: ruled → knowledge/_proforma/_DATAVIZ-DECISIONS.md § ★ #70

*Session #70, Sat 2026-08-01, Opus 5 (Cowork) conductor, Dave live. Ledger:
`knowledge/_proforma/_DATAVIZ-DECISIONS.md` § ★ #70 · state: `_LIVE-STATE.md` ⏱ LATEST DELTA #70 ·
commit (hash at wrap). #69 closed owing Dave three things, all his: (a) D3 legend lockup NEEDS
REWORK, (b) D4 — his wording ("additive like a checkbox") against ★ DV-D17 (swatch ENDS isolate),
(c) the review-export defect, recurred from #66. His reference for (a) and (b), given at the #69
wrap: `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html` — *"has all the correct
behaviours for the legend interaction and how the charts should behave."*

## Finding 1 — the prototype's date was wrong, and the error flattered the wrong side

Both `_CHAIN.md:42` and the ledger (`_DATAVIZ-DECISIONS.md` § ★ #69 POST-WRAP ADDENDUM) recorded
v5.5 as "dated 07-24, three days BEFORE DV-D17 (07-27)." Measured: the file's mtime is
2026-07-26 19:10 and its own `<title>` reads *"prototype, 2026-07-26 v5.5."* One day before, not
three — 07-24 is the series' start (its filename), not v5.5's own date. The correction matters
because "three days" framed the reference as a stale artefact, easy to discount; one day makes it
the immediately-preceding ruled state — DV-D11 landed 2026-07-26, the same day. Naming this first
because it is the rare correction that strengthens Dave's position rather than the agent's.

## Finding 2 — "additive" was not a memory slip. It was his own ruling

DV-D11 (2026-07-26): *"the LEGEND MODEL — dual gesture, two fade levels, additive isolate."*
DV-D17 (2026-07-27) deleted that code path one day later; `knowledge/canon/dv-legend.js:145`
(pre-#70, since superseded) said so outright — *"the isolated-mode ' added'/' removed' branch is
GONE, not merely unreachable."* Dave's #69 wording wasn't loose recall of an old model; it was
DV-D11, verbatim, set against a ruling that overwrote it a day later.

## Finding 3 — but v5.5 did not have "all the correct behaviours"

It carried the exact defect DV-D17 was raised to kill. Its controller: `function isSolo(id){
return isolated === id; }`, with `isolated` pinned to the seed while `focus` grows additively —
the seed row keeps `.is-solo` (black border) while other series check on. Same shape as Dave's
DV-D17 complaint, verbatim: *"the legend behaviour, the isolated key item stays active when I
check others on."* The reference could not simply be adopted as-is.

## Finding 4 — ★ DV-D18, ruled: solo is a SET SIZE, not a seed identity

The two behaviours were separable, and DV-D17 had conflated them. The additive focus set (what
Dave wanted, DV-D11) and the stale solo marker (what he objected to) are independent — DV-D17
fixed the marker by deleting the additive model outright, when it didn't have to. **Ruled by
Dave: solo is a SET SIZE, not a seed identity.** `isSolo()` (`knowledge/canon/dv-legend.js:48`)
now requires the focus set to be a singleton containing this id; the additive branch in
`toggleSwatch()` returns; DV-D17's release-on-add branch is deleted, not commented — left in
place it pre-empts the new path on the first click. DV-D17's bite (i) — release restores
`visible[]`, never all-on — survives completely and is asserted unchanged (check 22).

## Finding 5 — D4 was not new. It was the #7 open item, 63 sessions later

`knowledge/_REVIEW-SIGNOFF.md:21`, dated 2026-07-27: *"★ NEW 2026-07-27 (#7) — TWO FELT
CONSEQUENCES OF DV-D17, NEITHER RULED, BOTH NEED DAVE'S EYE LIVE,"* including (b): isolate
Housing (950/41%), check a second series — under DV-D17 the centre returns to 2320/100% instead
of growing to 1250/54%. v5.5's own headline is *"centre figure follows selection."* Dave pointing
at v5.5 at the #69 wrap was, in effect, him finally answering a question the record had been
carrying, unanswered, for 63 sessions.

## Finding 6 — a gate blind spot: the screen reader lied for 43 sessions

`isolate()` has announced *"Showing only X — check a blank swatch to add a series"*
(`knowledge/canon/dv-legend.js:160`) since DV-D17 landed, while `toggleSwatch()` released instead
of adding — the announcement described a behaviour the code no longer had. Neither
`_verify_dv_legend_members.js` nor `_verify_dv_legend.js` asserts this string against what
actually happens next; the 108/108 + 27/27 suites proved the *behaviour*, never the
*announcement's honesty about it*. It is true again under DV-D18 — restored because the additive
branch returned, not because anyone targeted the announcement itself. Recorded as an a11y
gate-blindspot class, sibling to the archived [[gate-blindspot-state-contrast]] entry: a suite can
sit fully green while a screen-reader user is told something false about what just happened, and
nothing in the gate is shaped to catch that class of lie.

## ★★ Finding 7 — the method finding: an invariant that survives a reversal cannot discriminate it

Check 20 was rewritten from DV-D17's wording to DV-D18's. Two mutants, built in `/tmp` via the
suite's own `DVLEGEND` env override — canon never mutated to prove it:

- **Mutant A** (`isSolo` reverted to seed identity) — 4 failures, check 20 red, `solo=true`.
- **Mutant B** (DV-D17's release-on-add branch re-inserted, DV-D18's `isSolo` kept) — 97/108,
  checks 20/21/22 red, reporting `restGhosted=[false] solo=false`.

Mutant B is the sharp one. `solo=false` means the `!soloRow()` clause — the exact invariant
Dave's DV-D17 complaint named, and DV-D17 existed to protect — **passes under both rulings**:
release the mode entirely (DV-D17) or shrink the live focus set to one (DV-D18), and no row reads
solo either way. A check asserting only that clause would have gone green on a mutant carrying
DV-D17's mechanism wholesale, and proved nothing about which ruling was actually live. Check 20
only became capable of failing once it also asserted what CHANGED — series outside the focus set
stay ghosted after the add (`restGhosted`), true under DV-D18, false under DV-D17's release. That
second clause is the whole check's power; without it the suite goes green under either ruling and
proves neither, which is exactly what mutant B demonstrates directly.

This is a sharper corollary of standing canon, not a restatement of it. [[six-beat-ladder-ruled]]
holds that a green that can't fail is an assertion; [[gate-must-quote-what-it-forbids]] holds that
a check is unproven without a mutation test. Here the check WAS mutation-tested and *still* nearly
failed to discriminate — because the clause it inherited asserted the half both rulings share. An
invariant common to the old ruling and the new one is not evidence for either; only the assertion
on what the ruling actually changed can tell them apart. Worth carrying forward as its own rule:
when a check survives a rewrite from one ruling's wording to its replacement's, ask which clause
would fail if the replacement had never happened — if none would, the check hasn't been rewritten,
it's been renamed.

## Finding 8 — the review radios were never wired, in any review doc

Not a #66 regression — an absence. A Sonnet sub diagnosed it; the finding was replayed and
confirmed independently before being trusted. `knowledge/_review/_review-overlay.html`'s
`buildPrompt()` built from `comments[]` only; zero radio reads anywhere in the overlay. #66's fix
repaired comment-pin export under a sentence in `knowledge/_RUNBOOK-review-doc.md:31` that claimed
to make picks + comment pins "capturable" — one sentence conflating two different problems, so the
#69 recurrence was inevitable, not unlucky. A working `picks{}` pattern had existed since
2026-07-30 in `reviews/MEMENTO-DECISION-PACK-2026-07-30-v1.html` and was never reused.

Compounding factor, from the fix's own comment (`_review-overlay.html:154`): the capture-phase
click handler `preventDefault()`s any non-overlay click while Review mode is on, so a radio click
was swallowed AND popped a comment composer — the control didn't fail silently, it actively did
the wrong thing.

**Fixed:** `scanPicks()` added to the overlay (`_review-overlay.html:325`), reporting unruled
groups explicitly as *"(not ruled)"* rather than omitting them — a silent gap is how a decision
goes missing; a declared one cannot. `isDecisionControl()` (`:157`) exempts native radio/checkbox
controls, and the `<label>` wrapping one, from the review-mode click interception. Diagnosed and
fixed in code; not yet seen live by Dave. The shape is one this project keeps meeting —
[[instrument-without-a-consumer]] — closed here in the review layer the way #69 named it.

## Finding 9 — a probe that invalidated my own worry

Suspected the snippet↔canon seam was ungated: five shipped chart snippets (bar, combo, donut,
line, scatter) carry an INJECTED copy of `knowledge/canon/dv-legend.js`, so canon could change
while snippets kept shipping the old behaviour underneath. Probed it rather than assumed it:
`gen_component_partials.py --check` is wired at `knowledge/_build_all.py:91` and blocks the build
on divergence. The seam IS gated — a stale snippet would have gone red at the next push, before
this session touched anything. Recorded because the result was negative, per
[[feedback-check-ran-never-reached-plan]]: after any probe, say what it invalidates. This one
invalidates the worry, not the mechanism.

## Evidence / verification (all run this session)

- `node knowledge/_verify_dv_legend_members.js` → **108/108 green**.
- Mutant A (`isSolo` reverted to seed identity) → 4 failures, check 20 red, `solo=true`.
- Mutant B (DV-D17 release-on-add re-inserted) → 97/108, checks 20/21/22 red.
- Both mutants built in `/tmp` via the suite's own `DVLEGEND` env override — canon never mutated
  to prove it.
- `gen_component_partials.py` re-injected all 5 consumer snippets; `--check` OK.
- `_validate_dataviz.py` → green, 7 chart surface files.

## Rulings this session (Dave)

- ★ **DV-D18 — solo is a SET SIZE, not a seed identity.** Enacted in
  `knowledge/canon/dv-legend.js` (`isSolo`, `toggleSwatch`), injected into all 5 consumer
  snippets. DV-D17's invariant (bite i) kept whole; its mechanism (release-on-add) deleted.
- **Budget fork, declared rather than spent silently:** ~140K of the 200K Dave's-line spent; a
  review pair for DV-D18 priced to land ~205K. Dave deferred the review pair to #71 rather than
  let the session run over.
- **D3 (lockup layout rework)** — NOT addressed this session. Detail still owed; never given.
- **Memento "worker tree"** — Dave floated *behavioural instructions for each type of model*,
  FLOATED, not ruled. Reads as scoping worklist item 9, DELEGATION TOPOLOGY. Kept separate from
  anything enacted here, per [[feedback-dont-launder-a-premise-into-a-ruling]].

## Resolved state / still open

**Resolved:**
- D4 (swatch-during-isolate collision) — ★ RULED as DV-D18, enacted, 108/108 green plus the two
  mutation controls red exactly as designed.
- Review-export defect (recurred from #66) — root cause diagnosed and independently confirmed;
  fixed in `knowledge/_review/_review-overlay.html` (`scanPicks`, `isDecisionControl`). Not yet
  seen live by Dave.
- Snippet↔canon staleness worry (Finding 9) — probed, disproven; the gate already covers it.

**Still open:**
- D3 legend lockup layout — NEEDS REWORK stands; Dave's detail was never given this session.
- The DV-D18 review pair — deferred to #71 by Dave's explicit budget ruling.
- Memento "worker tree" — FLOATED only; unscoped.
- Untouched carryovers from #69's own close, unaffected by this session: fit-hook adoption,
  four-theme chart-canvas wiring, the Mono/Console review-control switcher, colleague's Copilot
  verdict, CI glance at the next push, radius tuner verdict, render-30 + a11y-8 triage.
