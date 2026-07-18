---
name: spread-review-gaps-2026-07-05
description: "Dave's eyeball review of the first §9 worked spread found real gaps — retrieval-ranking and a missing build-review-correct loop, not just craft polish"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6edd272b-3c99-4240-bfcd-19803afcb6eb
---

Dave reviewed the three actual HTML files from the first §9 worked spread
([[register-inference-ramp]], `knowledge/_fitness-test/register-spread-2026-07-05/`) and found the
"promising" verdict premature. Two concrete findings, plus a process question that exposes a real
gap.

**Finding 1 — sober under-retrieved: "correct components" ≠ "any existing component."**
Verified: sober's cash-position section uses `.c-stat-grid` (a plain hand-authored composition-layer
utility, canon.css line ~614 — a flat 2×2 grid, 1px hairline dividers). Canon *also* contains
`.cn-account-card` — explicitly commented in canon.css as "PROMOTED to a reviewed component... Gap
pattern removed" — a purpose-built, more finished card treatment for exactly this kind of
balance/label display, which the **balanced** band used as its hero. Both classes technically exist
in canon (so retrieval-not-recall held, per the letter of §9), but sober picked the plainer, less-
reviewed one. **Why this matters:** current retrieval instructions only check "does this exist in
canon," with no signal to prefer a gated/reviewed component over a hand-authored utility layer when
both fit the data. Dave's "sober should look more like balanced" reaction is really "sober picked
the worse of two valid retrievals" — a retrieval-*ranking* gap, not a hallucination or curb
violation. **How to apply:** any future retrieval instruction for the ramp should say something like
"when multiple canon artifacts fit, prefer the more reviewed/promoted component over a generic
composition-layer utility" — sober should still mean *don't invent*, not *pick the plainest option*.

**✅ FIXED 2026-07-05, same session.** Canon.css already encodes this as a mechanical, grep-able
naming convention — `.cn-*` = AUTO-COMPONENTS generated from gate-reviewed
`knowledge/snippets/*.reference.html` (canon.css says outright: "do NOT hand-edit... edit the
snippet, the reviewed source of truth"); `.c-*` = the hand-authored alias/utility/gap-pattern layer,
never gate-reviewed. `_TEST-BRIEF-v2-sme-payments.md` §2 now states this as an explicit, checkable
"canon rigour tier" rule (prefer `.cn-*` always when one fits; `.c-*` only as fallback; name what
you ruled out before using a `.c-*` class). This closes finding 1 as a brief-language gap — untested
whether it fixes the actual output; needs a re-run to confirm.

**Finding 2 — expressive needs more actual creative risk, not less.** Dave wants more excitement
from expressive, not less. The self-check already flagged expressive as "at the edge of tactical"
on red-leadership/busyness — Dave's read is the opposite direction: it still reads too safe. Working
hypothesis (unconfirmed): the amount of compliance/caution language in the expressive-band prompt
("never recalled free-hand," "flagged," "derived from a cardinal," repeated) may have suppressed
genuine boldness even though the band is nominally licensed for MAX inference. Needs testing, not
assumed.

**Process question — is there a build→review→correct loop?** Answer: **no, not currently.** The
spread was one isolated generation pass per band, then a separate after-the-fact structural
probe + self-check done by Claude, with no feedback back into generation (no iterate-until-it-
passes step). This is a genuinely new gap — distinct from the three §9a machinery pieces already
named (isolated generation, divergence probe, mode-B self-check). **Flag for the charter/harness
work:** a review-and-correct loop (generate → critique against curbs+principles → patch/regenerate
→ re-check) is not yet named anywhere in §9/§9a and should be, once tested.

**Dave's suggestion — test Opus for generation.** Per [[model-selection-by-phase]] (Opus for
judgment sessions), Opus may exercise better taste on exactly the two failures found: recognising
the better-fit retrieval target (finding 1) and taking a genuinely bold creative swing within the
cardinal leash (finding 2) — both are judgment calls, not throughput work. Untested; the natural
next experiment is a re-run (at least of sober, ideally the full spread) on Opus, possibly combined
with a review-correct step, to separate "was it the model" from "was it the missing loop."

**Net effect on `_LIVE-STATE.md`:** the "promising, not yet proven" verdict from the first pass
holds — Dave's review is the very thing the audit-deferred caveat was waiting for, and it surfaced
real work, not just polish. Don't over-read the first spread's grep-clean cardinal-curb result as
"the ramp works" — it proves curbs can hold, not that retrieval or craft judgment is good yet.

**✅ DIAGNOSED 2026-07-05 (same session, after the Opus re-run) — why expressive is still a
letdown: permission without gravity.** Dave's hypothesis, confirmed against the actual prompts: all
three expressive-band prompts (Sonnet + Opus) were dominated by compliance language — "derive from a
retrieved cardinal," "flag everything," "never recalled free-hand," "name the source primitive" —
repeated many times, with the *only* inspirational material supplied being internal and fairly
buttonedup (`brand-principles.md`, `colour-usage.md`, `canon.css`). **Zero external creative
reference was ever given.** "Invent freely (within the cardinal leash)" is *permission*, not
*direction* — without a positive creative target to reach for, the model recombines what it already
has (canon + corporate brand docs) rather than reaching further, so expressive drifts toward
"sober, but bigger," not somewhere genuinely new. Confirmed by contrast: `sme-payments-portfolio.html`
(an older, pre-charter, ungoverned "portfolio piece" Dave still finds more expressive) leans hard on
craft dimensions our recent runs barely touched — hover-lift + shadow with spring easing, a radial-
gradient hero glow, count-up/staggered-reveal motion choreography, backdrop-blur modal, avatar
chips, a ribbon-style flag tag — depth/motion/interaction craft, not just static composition/scale.
It also explicitly opted OUT of canon-composition-gate discipline ("Self-contained (custom craft
layer, not the strict canon-composition gate)") and typed brand hex directly rather than deriving
via `var()` — so part of its excitement is *because* it wasn't carrying the retrieval/audit-trail
overhead our governed expressive band carries. **Open design tension for the next move (Dave's own
idea, not yet implemented):** define "gravity" for the inference dial, not just "pull" for canon —
give expressive an explicit external creative target (award-winning fintech/AI/tech-company digital
design) alongside the existing cardinal curbs. Needs care: an inspirational reference must feed
composition/motion/energy, not leak a *different* brand's colour/type into the cardinal layer —
retrieval-not-recall still has to hold for the brand primitives even while recall-from-inspiration is
invited for craft. **✅ IMPLEMENTED + FIRST RE-RUN DONE, same session.** Dave: "I need a plan" + make sure it's on the
state machine — recorded as a `PLANNED / TARGET STATES` entry in `_LIVE-STATE.md` explicitly marked
as **blocking external review of the §9 spread** until resolved. Sourced 5 named references via web
search (not recall): Linear (micro-interaction timing, blur-depth not shadow), Stripe (typographic
rhythm, sparing accent glow, spring easing), Mercury (oversized confident numeral as the one bold
moment), Ramp (single accent doing real state work, not spread thin), award-calibre fintech launches
generally (scroll/morph choreography) — written into `_TEST-BRIEF-v2-sme-payments.md` §2's
Expressive bullet as an explicit "Inference gravity" block with the hard guardrail: pattern only
(pacing/depth/motion-physics/hierarchy), never colour/type/logo, which still resolve through HSBC
canon. Re-ran **only** the expressive band (sober/balanced already fixed, no need to re-spend) on
both Sonnet and Opus as `expressive-v2.html`. Grep-verified against the actual files: motion/
animation mentions roughly doubled-to-tripled per model; `backdrop-filter`/blur depth technique
appears for the first time in either run; `prefers-reduced-motion` still present; zero
`border-radius` violations; zero brand-colour leaks. **Still needs Dave's actual eyeball verdict —
structural counts are a proxy for "more motion/depth exists," not proof it reads as exciting.**
Comparison viewer updated (`register-spread-2026-07-05-compare.html`) with an "Expressive (v2)"
button per model plus a direct link to `sme-payments-portfolio.html` for side-by-side judgment.
