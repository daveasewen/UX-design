# Style consolidation → the four-theme token architecture (2026-07-20, evening 2)

*Narrative dossier (capture-ritual step 1b — the why/how, not just the what). Spine entry:
`_LIVE-STATE.md` LATEST DELTA 2026-07-20 (evening 2). Rulings: **R-D19** (`_proforma/_RAG-DECISIONS.md`),
**ADR-0011** (`docs/decisions/`). Record: `knowledge/_STYLE-PROVENANCE.md`. Commit `a1b9fbb`. Both-way
links back from each. Validation state of R-D19 + ADR-0011: **unaudited** (seeded, not self-promoted).*

## How the session actually moved (it drifted a long way from "good morning")

Opened as a routine good-morning. I read the handoff and offered the obvious next itinerary picks
(Textarea / Empty state / Alert). **Dave: "we have done all these already — dig deeper."** That was the
first correction and it set the tone: the handoff's surface frame (grind out more atoms) was not the
work. Verifying against the repo, the itinerary statuses were partly stale, and the real gaps were
structural — composition tier, the RAG-role rulings, the generation machine.

Dave then pointed me at four directories (`_fitness-test`, `_proforma`, `_review`, `snippets`) and the
real ask emerged: **"consolidate, align to Apollo Mono, with Apollo Legacy in mind — some of these were
built on old styles — and have a clear record. This is too loose."** Not a build task; a *consolidation
+ record* task.

## The finding that reframed everything: the token store had no theme dimension

I scanned all 121 HTML files by style-era, then — Dave: "look at the tokens too" — traced the drift to
its source. **The semantic token store carries only `light`/`dark` modes; it has no theme dimension at
all.** So Legacy red (`#DB0011`), teal (`#00847F`), and the Legacy grey ramp live in the *same flat
roles* that Apollo Mono resolves against. The only reason a Mono button isn't red is that it was rebound
to a *new* decoupled role (`button/primary/*`) — divergence by forking, which R-D15 explicitly said not
to do. **The looseness was a missing architecture, not sloppy files.** That is the pivot the whole
session turns on, and it's why "align to Mono" was unenforceable: nothing separated the two themes.

## The rulings, and the corrections that shaped them

- **"no red is legacy" → R-D19.** My first classifier treated snippet red as "legit-but-pending
  rag/error." Dave corrected: red is a *Legacy* signal. Reflected back (I don't override a locked ruling
  silently — R-D14 breach red is `#B92F1E`), and Dave pinned it: *"these reds are valid for Legacy only;
  we have a new red for Mono, only used for status and RAG."* So Legacy red `#DB0011`/`#A8000B` = Legacy
  theme only; Mono's one red `#B92F1E` = status/RAG/dataviz only, never action/nav. This is what makes
  "red = drift in a Mono surface" a definition rather than a judgement call.
- **"wire this up properly with the themes" → ADR-0011.** Themes become **override sets at the semantic
  tier**: Mono = base, Legacy = populated override, Console + Supercharge = *declared nullable slots*
  (reusing ADR-0010's declared-but-unset pattern, so they're wired and waiting, not forked later). This
  mechanises R-D15's intent for the first time. Registry `tokens/themes/_themes.json` = the single source
  of truth for which hex belongs to which theme.
- **"when there are duplicate patterns I need to compare visually."** A text ledger can't carry a
  keep/migrate/archive decision Dave makes by eye. Built a cluster generator that groups duplicates and
  renders old exploration *beside* canon.
- **"SME-payments journey ignore — test pages" → then "actually I was wrong, there's good work in
  \_fitness-test."** I over-corrected first (crude "exclude all fitness-test"), Dave pulled it back. Final
  scope: `_fitness-test` splits into *exploration (mine + supersede)* / *research (preserve — it carries
  findings)* / *journeys (ignore)*. The compare page is the instrument that lets Dave make this call
  himself, which is why it had to show everything, tagged, not pre-filter.
- **"iframes too small … review screen … launch full screen."** v1 was a horizontal-scroll strip — wrong.
  v2 is a proper review screen: per-cluster picker, a wrapping grid (no h-scroll), column/height/bg
  controls, and **Open ↗ / ⤢ fullscreen** per variant. Then the review overlay injected (`_make_review.py`)
  so Dave can pin markup per card.

## A method note worth keeping

The raw scan over-reported drift twice: it counted hexes in *comments / token-manifests*, and it counted
the *ruled* Mono red `#B92F1E` as if it were Legacy red. Both would have condemned clean files. The fix —
strip comments and exclude ruled-Mono colours **before** classifying — is the same discipline as
[[attribute-the-diff]]: don't judge a difference you haven't isolated. The advisory gate bakes this in
(comments + manifests stripped; only foreign-theme hexes counted).

## Resolved state / still open

**Landed (committed `a1b9fbb`, build green 37/37):** ADR-0011, R-D19, the `_STYLE-PROVENANCE.md` record +
`_style-clusters.json` mirror, the v2 review screen (+ overlay copy), and the **advisory** theme-provenance
gate (found 68 hardcoded foreign-theme hexes across 61 Mono files — the blind spot the token leak gate
can't see). Deliberately *advisory* so the canonical build stays green through migration.

**Open (record §backlog):** rule the **Mono values for `tabs/active` + `progress/complete`** (they only
ever held Legacy red; Mono ≠ red) before their Legacy red can be gate-seeded blocking; the Sonnet sweep
that aligns the 19 drifting snippets + 12 tranches against ADR-0011, then regenerates the `_review`
copies; then promote the gate to blocking. Console/Supercharge override sets fill their null slots when
their palettes are ruled. Minor: the review-overlay chrome uses `#DB0011` (tooling, not a Mono surface) —
tooling-exempt from R-D19; note if it shows in the advisory report.
