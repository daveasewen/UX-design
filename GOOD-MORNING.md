# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-22 (evening, ONE FABLE CONDUCTOR session ran BOTH waves + 5 worker windows): **PHASE-2 WAVES 1+2 LANDED — 24 components in one day, library 40→64, registry 4→18 members, census 32→32 across everything, build 51/51.** Wave 1: A forms 4/9 + B feedback 10/11 (14 landed). Wave 2: **A-continuation 5/5 — the forms brief is COMPLETE 9/9** (incl. the library's FIRST calendar panel + first determinate progress bar) · **C Data-grid 1/1** (APG semantics, 4-control `:is()` member) · **D Charts 4/4 — the parked dataviz kit PROMOTED to canon snippets, ALL PROVISIONAL-AGENT awaiting your sign-off.** The ADR-0013 protocol compounds: wave-2 workers PRE-LANDED the partials contracts → injections clean first try; dataviz gate now WIRED to chart snippets; census never moved. **Gates earned their keep:** token-sync caught 4 recall-written values (Stepper) · blast-radius caught a `.seg` reuse · type26-013 blocked a white-letter donut variant. **A's fence-breach flag RESOLVED as misread of MY mid-wave absorb — fences held all day** (reconcile receipt has the full account). **⚠ AWAITING YOU: 16 numbered questions + the DATAVIZ SIGN-OFF (§C·2) + the standing eyeball set now spanning 24 new components (§C·3).** Field-family accretion evidence: **≥10 files, overwhelming.**
> **RENAME THIS CHAT →** `Apollo Phase-2 CONDUCTED, both waves — 24 components (forms 9/9 · feedback 10 · Data-grid · Charts kit) · library 40→64 · registry 18 members · census zero-growth all day · 5 commits [FABLE conductor]`
> **TITLE THE NEXT (fresh) CHAT →** `Apollo post-fan-out — Dave's ruling batch (16 Qs + dataviz sign-off + eyeball across 64) · then wave 3 survey (~26 gaps) or the templates+shells clean-room`
> *(⚠ Titles are LABELS — the role word comes from your opener line, never from a title. Fresh session: read this file, then `_LIVE-STATE.md` top delta.)*
>
> ---
>
> ## PRIOR — 2026-07-22 (afternoon, FABLE solo): **ADR-0013 BUILT** (partials + ratchet + registry; B-D7 press physics pixel-true + theme-dialable, both beats inscribed; stepper folded; ds-008/ds-009 closed) — then the review-pass window put the **review overlay in every showroom pane** and cut the wave-1 briefs. **Still awaiting you across sessions:** the eyeball set (§C·3) — B-D7 motion deltas + `reviews/SC-DARK-MODE-2026-07-22-v1.REVIEW.html` + 4 held whites + Console radius px — all NON-BLOCKING (your ruling: foundations first; everything retro-propagates as token edits).

---

*Briefing — refreshed 2026-07-22 18:12 BST (date from `date`), session "Phase-2 CONDUCTOR, both
waves" (one FABLE conductor + 5 FABLE worker windows across the day; all receipts + 2 reconcile
receipts in `notes/_receipts/2026-07-22-phase2-*`). §A = orientation · §B = session · §C = queue.*

## ⬛ DO THIS FIRST

> **1. ★ DAVE: the RULING BATCH (§C·2)** — 16 numbered questions + the **DATAVIZ SIGN-OFF** (flips
> D's 4 chart snippets provisional→canon). Rule by number, any window; everything retro-propagates.
> The **field-family accretion** (Q6) is the material one — evidence ≥10 files.
> **2. The eyeball set (§C·3)** — now spans all 24 new components × 4 themes (non-blocking, async
> via pane pins).
> **3. Then wave 3 or the templates+shells clean-room (§C·1)** — next session surveys and cuts.

*Standing practice: every handoff carries both names — retrospective + forward — and a **DIVVY PLAN**.
This handoff's plan: §C·1. Steps 4b + 2 in `_RUNBOOK-capture-ritual.md`.*

*Read: **§A Orientation** (skip if you're in context) → **§B This session** → **§C Queue**.
Then `_LIVE-STATE.md` → the decision files it points to.*

---

# §A · ORIENTATION — the whole project in one page

> **Why this file is called GOOD-MORNING** *(Dave's framing — keep it, it explains the architecture)*
> **Memento.** Leonard has anterograde amnesia: every morning he reconstitutes himself from a record he
> built when he still remembered — Polaroids for working state, **tattoos for the facts he cannot afford
> to lose**. That is this project's operating model, not a metaphor for it. A session starts with no
> memory and rebuilds from artefacts.
>
> **The trust hierarchy is the tattoo/Polaroid distinction:** repo rules + runbooks + ledgers = tattoos
> (durable, survive any single rewrite) · `GOOD-MORNING` + `_LIVE-STATE` = Polaroids (working state,
> rewritten often) · the chat = gone by morning. **Never let a durable rule live only on a Polaroid.**
> *(Live example, 2026-07-22: this file said the tabs ruling was "NOT yet inscribed" — the ledger already
> carried R-D23 AND R-D24. The ledger was right. Read the ledger.)*
>
> **The real danger is not forgetting — it is confident false inscription.** Records carry provenance
> and confidence, not just content. Corrections get inscribed as loudly as the original claim. **Mark
> what was OBSERVED versus what was INFERRED.** The ritual stamps dates from `date`, never from belief.
> *(2026-07-22 afternoon instance: B-D7 was ruled in TWO beats — "shared 4%", reversed within the hour
> to pixel-true. BOTH are in the ledger, so the reversal can never read as agent drift.)*
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** ⇒ **Before designing anything,
> CONSULT: `python3 knowledge/_consult.py "<what you're about to design>"`** (rules · rulings · assertions ·
> gates + where each bites). Runbook: `knowledge/_RUNBOOK-consult.md`. *(ds-009 CLOSED 2026-07-22: the
> corpus is now DISCOVERED — every `_proforma/_*-DECISIONS.md` indexes or the build fails.)*

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* New-starter style: assume the reader has no context.
> **Update it when the shape of the project changes, not every session — but never drop it, and never
> shorten it to a label.** *(Also step 2 of `_RUNBOOK-capture-ritual.md`; reachability-gated by
> `_validate_standing_instructions.py`.)*

## What Apollo is
A **governed design-system engine** for agentic UI generation. The bet: *generation is a commodity* — the value
is the layer around any generator. Two principles run through everything:
- **Retrieval, not recall.** Brand values are retrieved from token stores, so generated work can't drift off-brand.
  **Since ADR-0013 (built 2026-07-22) retrieval reaches RULES too:** organisms consume atoms' rule-blocks
  as generated partials — never re-type a sub-atom.
- **Verification = enforcement.** Judgment is encoded as **blocking gates**; "done" is withheld until they pass.
  If a rule isn't gated, assume it will be broken.

Tagline: **"lovable on rails."** Four phases: **Discover** → **Create** (what's being built now) → **Craft**
(the review-overlay docs ARE this) → **Dispatch**.

## ★ ONE token store · ONE baseline library · FOUR themes (R-D15 → ADR-0011 → ADR-0014 → ★ ADR-0013)
*Themes are **override sets at the semantic tier**; since ADR-0014 they carry **their own neutral primitive
ramps** through the **neutral DNA tier** (semantic roles alias `color/neutral/1–15`, never `color/mono/*`
directly; indices are SEMANTIC POSITIONS — SC remaps its anchor). **State mechanism is a THEME PROPERTY**
(registry `stateMechanism` + blocking snap gate). **★ Since ADR-0013, MOTION is a theme dial too (B-D7):**
`motion/press/{travel,darken}` — Mono carries the movement (pixel-true 2px), **Console inherits it**,
**Legacy + Supercharge zero it** (colour-only state feedback); tuning = a token edit, zero JS.
**Sibling pairs:** {Mono, Console} share neutrals/opacity/status/dataviz — Console FENCED (colour;
motion is inherited-not-fenced, flag if it should join); {Legacy, Supercharge} = structural siblings.*
The four themes (Dave's canonical order):
- **Apollo Legacy** — faithful reproduction of the existing HSBC system: brand red `#DB0011`, teals,
  `color/grey/*`. **AA-EXEMPT as-built (R-D24)**; explicit per-path overrides, no DNA tier, **no press movement**.
- **★ Apollo Mono** — the baseline we build NOW. "Very mono": colour ONLY in RAG status + dataviz.
  Neutral scale = `color/mono/1–15`; only red `#B92F1E` (status/RAG/dataviz). Carries the B-D7 press physics.
- **Apollo Console** — branded HSBC library. **LOCKED ≡ Mono** on neutrals/opacity/status/dataviz (fence);
  inherits Mono's motion; live divergence = rounded corners (radius overrides, values provisional).
- **Apollo Supercharge** — brand-uplift. **OWN warm ramp** `color/warm/1–15` (OBSERVED, Figma pull);
  states = COLOUR; **no press movement**; dark mode = provisional-agent, awaiting Dave.

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores — the retrieval source
    colour.json       primitives: mono/1-15 · neutral/1-15 (DNA tier) · warm/1-15 (SC) · grey/* (Legacy)
    semantic-colour.json  roles alias color/neutral/* + rag/* + component tiers + $extensions.apollo.state
    motion.json       durations · easings · ★ press/{travel,darken} (B-D7 — the theme-dialable physics)
    themes/           the four override sets + _themes.json registry (stateMechanism · neutralRamp ·
                      siblingPairs · console fencedPaths · ★ Legacy/SC motion kills)
  ★ component-types.json  THE ADR-0013 REGISTRY — one file, both halves: component-type/<group>/<param>
                      tokens ($alias→semantic + cached $value) + $members (selector map) + $partials
                      (source atom · rootSelector · requires/matchValues/declarations · $manifestBinds)
  snippets/           64 gated reference components = CANON (40 + Phase-2's 24). Atoms carry
                      PARTIAL blocks; consumers carry generated AUTO-PARTIAL blocks (provenance-
                      commented, sync-gated). Multi-control members = :is() selector lists (wave-1
                      convention); mixed sizes = local --phys-size override
  ★ gen_component_partials.py  injects partials into consumers; --check = build gate; selftest 8 bites
  ★ _validate_partials.py      the re-implementation RATCHET (strict on members · census = accretion
                      worklist) → _PARTIALS-GATE.md
  canon/              canon.css (token spine · components · AUTO-THEMES cascade) + type.css (HAND-AUTHORED)
                      + generators (gen_canon_tokens · gen_theme_cascade · ★ gen_canon_components — now
                      IN the build: regenerate-always + determinism --check, ADR-0013 ruling 4)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (generated)
  _proforma/          Apollo Mono tranches T1–T9 + the decisions ledgers (near-canonical per ruling 3)
  _consult.py         "what governs X?" — RUN IT before designing (corpus now DISCOVERED, ds-009 closed)
  _validate_*.py      the gates — incl. _validate_state_snap.py (ADR-0014) + ★ _validate_partials.py
  gen_showroom.py     generates showroom/ — never hand-edit showroom
showroom/             THE LIBRARY, browsable: 64 harness pages + index w/ live count (#theme=… all four)
reviews/              review sheets — ★ AWAITING DAVE: SC-DARK-MODE-2026-07-22-v1(.REVIEW).html
notes/_receipts/      worker-receipt dir · notes/_briefs/ conductor briefs
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative — ★ 2026-07-22: the ADR-0014 arc AND the ADR-0013/B-D7 arc
```

## The one command that matters
```
python3 knowledge/_build_all.py     # ★ 51 steps (45→51: partials sync+selftest · canon-components
                                    #   regenerate+determinism · ratchet+selftest), exits non-zero on any failure
```

## Rules that actually bite (core + this session's)
- **CONSULT before designing** — then **survey before build**. *(This session the survey found Icon-button's
  physics was a REVIEWED refinement, not drift — which became B-D7.)*
- **★ ADR-0013 (BUILT): never re-type a sub-atom.** A registered partial's rule may exist ONLY in the
  atom's PARTIAL block or a generated AUTO-PARTIAL block — the ratchet gate blocks members' local
  re-implementations; the census lists everyone else's (accrete from OBSERVED duplication, ruling 3).
  Joining a family = markers + required vars + manifest binds + registry entry, and the generator
  fails loud on any missing piece.
- **★ B-D7: press physics is pixel-true and theme-dialable.** Travel/darken are TOKENS
  (`motion/press/*` → group caches); `--phys-size` is LOCAL geometry (buttons 120, icon 44); Legacy/SC
  zero the dial. **No JS in physics — ever** (Dave's constraint; DEF-003 posture). Tuning = token edit.
- **ADR-0014: semantic neutrals alias `color/neutral/*`, NEVER `color/mono/*` directly** · whites are
  classified (substrate → `neutral/15`; absolute → `color/white`, pinned).
- **ADR-0014: opacity states must SNAP** (`_validate_state_snap.py`, blocking, 7 checks incl. the
  text-state AA floor — inactive ≠ disabled).
- **Selftests are BUILD STEPS** — every new gate ships one AND wires it (partials + ratchet did).
- **Resurrect-verbatim is NOT gate-exempt** — the 273d18c~1 stepper's 13px/3px hit the grid gate on
  re-entry; corrected 12px/4px. Old reviewed artefacts re-enter through the same door as new work.
- **Grey-tint standing check** · **type26-013 (BLOCKING): white type is red-only** · **R-D6 glyph
  contrast by ROLE** · **`LEGACY_THEME_EXEMPTIONS`** (R-D24 — EXEMPTED, never passed).
- **canon.css** — generated only between AUTO markers; type.css HAND-AUTHORED. *(The ruling-4 gap is
  CLOSED: snippet RULE-text now self-heals into canon every build.)*
- **Every selector appended to `canon/type.css` is GLOBAL** — register in `_type-bindings.json` or the
  blast-radius gate fails.
- **Icons: real assets only** · **4px grid** · **sentence case** · **square corners in Mono** (radius =
  ROLE tokens, per-theme) · **weights: 100/300/400/500/700 only, NO 600.**
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
  *(SC dark values agent-derived → AWAIT him; B-D7's enacted values are HIS ruling, verbatim-quoted.)*
- **Spine discipline** — state lines in `_LIVE-STATE`; narrative >10 lines → `_DECISION-HISTORY/`.
- **Inscription prose is PARSER-VISIBLE** — no node names in ADR-header parentheticals (phantom edges).

## Standing instructions for the agent
- **Announce the model/routing split at the START of every substantive task** (`MODEL-ROUTING.md`).
- **Verify before asking** (read repo / run gates) — including your own flags. **Reflect back before
  recording** a ruling — and when a ruling REVERSES, inscribe both beats (B-D7 is the model).
- **Decision-heavy / material-referring choices ship as review HTML** (`knowledge/_review/_make_review.py`
  — NOT at knowledge/ root). Architecture calls = the ADR-0012/0013/0014 model: options + firm
  recommendations in-chat, Dave rules by number, inscribe same hour, **feed the graph seed same hour**.
- **Surface spin-off candidates**; register ideas in `_FUTURE-STATE.md`. **Run the capture ritual
  unasked**; **stamp dates from `date`**. **Memory accelerates; the repo is the record.**

## The other standing documents (REACHABILITY-GATED by `_validate_standing_instructions.py` STAND-002 — keep every one referenced here)
`_STANDARDS.md` (★ the standards hub) · `AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D14) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D25) ·
`knowledge/_STYLE-PROVENANCE.md` · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`docs/decisions/ADR-0012-decision-graph-edge-convention.md` (seed `notes/_decision-graph-seed-2026-07-21.json` —
★ 124/124 zero mismatch after B-D7; feed it EVERY inscription, or `--verify` drifts silent) ·
`docs/decisions/ADR-0013-component-type-tier-composition.md` (★ BUILT 2026-07-22 — Consequences updated) ·
`docs/decisions/ADR-0014-per-theme-neutral-primitives-state-snap.md` ·
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…★ **B-D7**; in the CONSULT corpus since ds-009 closed) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` · `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` · `docs/decisions/ADR-0011-four-theme-token-architecture.md` ·
`knowledge/_DS-IMPROVEMENTS.md` (ds-007 open · ds-008 ✅ · ds-009 ✅) · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` · `knowledge/guidelines/_rules-index.json` · ★ `knowledge/component-types.json` (the ADR-0013 registry) ·
`knowledge/_PARTIALS-GATE.md` (the ratchet report — census = Phase-2's accretion worklist). **Runbooks** indexed by `knowledge/_RUNBOOKS.md`.
*(This list was dropped in a rewrite once and STAND-002 red-flagged it — do not prune it.)*

## Parallel-session model (PROVEN 2026-07-21)
On "read good morning", role is picked (Worker / Conductor / Solo) — **from Dave's opener line ONLY;
titles are labels.** ONE conductor = single writer for shared state; workers emit receipts to
`notes/_receipts/`, no git. Conductor reconciles the shared tree before committing (never blind
`git add -A` with workers live). Every handoff carries a **DIVVY PLAN**. Workers can absorb live Dave
rulings mid-flight — receipt verbatim.

## Renders — REAL FONT, in-sandbox
Playwright headless-shell recipe: memory `sandbox-html-rendering`. ⚠ **2026-07-22: this sandbox
REFUSED the headless-shell download** (both sessions) — render-verify for ADR-0014 AND ADR-0013 is
OWED; verification stood on mechanical proofs + selftests + gates. HTML is what Dave reviews.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`knowledge/_review/_make_review.py <file>`).
- **Live tuners beat static versions past ~2 colour round-trips.** Sheets read canon.css LIVE, never retype.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — run it,
  don't improvise. `unable to unlink … *.lock` warnings = the delete-guard, not failure; judge by HEAD.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-22 evening — "Phase-2, BOTH waves: one conductor, five worker windows")

*The record lives in the receipts (5 worker + 2 conductor-reconcile, `notes/_receipts/2026-07-22-
phase2-*`) — no separate dossier; the receipts ARE the narrative, judgment calls included.*

- **✅ 24 components in one day** (W1: A-forms 4 + B-feedback 10 · W2: A-continuation 5 — **forms
  brief COMPLETE 9/9** — + C Data-grid + D Charts 4). Library 40→64, registry 4→18 members,
  radius 45-strict, **census 32→32 across everything**, 51/51 green at every reconcile. Firsts:
  calendar panel (Date-picker, composed from surveyed parts) · determinate progress bar
  (File-upload, ink-on-neutral) · Charts = the parked kit PROMOTED (provisional-agent, sign-off
  yours). Conventions minted: `:is()` multi-control members · local `--phys-size` on mixed sizes ·
  `proforma-promotion` provenance class · dataviz gate wired to chart snippets (new-surface rule).
- **✅ The protocol COMPOUNDS:** wave-1 absorb completed 7 lanes' contracts by hand (they fire only
  on registration — fails-loud proven); wave-2 workers READ that lesson and pre-landed contracts →
  both wave-2 absorbs injected clean first try. Fences held all day; A's wave-2 breach flag =
  misread of MY mid-wave absorb of C (resolved + inscribed in the wave-2 reconcile receipt —
  the name-every-path reflex worked, the inference didn't).
- **✅ Dave's in-flight asks handled by the hot-clause:** showroom header count SHIPPED (live 64) ·
  card thumbnails NOTED (`_FUTURE-STATE`, `#bare`-mode shape) · theme "outage" diagnosed as
  wrong-file + payload-is-base64 (pages were correct; Legacy's small delta on data components =
  architecture, not bug).
- **🐛 Wrong/caught:** Drawer close 44→36 (file beat receipt) · my pkill self-match (twice-class,
  receipted for the runbook) · one stale-cascade red per wave (my own serial edits, regen healed).
  **Owed:** render-verify (headless-shell, standing).

---

# §C · QUEUE

## 1. ★ NEXT STRANDS (~~wave 2~~ DONE — pick one per window; role from the opener line)
**(a) Wave 3 fan-out** — ~26 itinerary gaps remain (`reviews/ITINERARY-2026-07-14…`); the next
conductor SURVEYS the itinerary + cuts lane briefs (wave-1/2 briefs = the pattern; candidates:
navigation/menu family + remaining P2 depth). Serial set unchanged (registry · MIGRATED_SNIPPETS ·
CATEGORIES · spine · git = conductor only, ONE commit; workers = NEW files + receipts, no git).
**(b) Templates+shells clean-room (Layer-2, the load-bearing gap)** — solo Fable ADR-style session
(the ADR-0013 precedent). Best AFTER the ruling batch: field-family, stepper-fold and delta-seam
answers shape it.
**(c) Enact window (cheap)** — absorb §C·2 rulings as token/registry edits + the §C·4 queue;
new candidates: mint `data/axis`+`data/grid` · R-D9 ramp promotion · field-family group build if
ruled yes · Stat-card `spark` slot (D's composition seam, pairs with B-Q6).

## 2. ★ DAVE: THE RULING BATCH — 16 numbered + the ★ DATAVIZ SIGN-OFF (rule by number; all
retro-propagate). **The sign-off first:** D promoted the PARKED kit verbatim into
Chart-bar/line/donut/sparkline — your review flips them provisional-agent→canon (open-014).
**New this wave, 8–16:**
8. **(A-Q5)** Calendar day-cells + Stepper done-dots carry NO press physics (judged selection
   targets / structural markers, the Tabs class) — confirm, or extend the family.
9. **(A-Q6)** File-upload built the library's FIRST determinate progress bar (ink-on-neutral,
   R-D22 spirit) — accretion candidate when a second consumer appears.
10. **(A-Q7)** Stepper consumes Progress-tracker's visuals by copy — fold to one snippet, or
    accrete a stepper-visuals partial at a third consumer?
11. **(A-Q8)** Date-range = restart-on-earlier-pick (inscribed as reference behaviour) — flag if
    the HSBC source says swap-endpoints.
12. **(D-Q1)** Line markers: Background fill (promoted default, theme-adaptive) vs White — the
    kit toggle never ruled.
13. **(D-Q2)** Donut labelling default: spider vs direct; letters-on-segments HELD (white letters
    on series fills — type26-013).
14. **(D-Q3)** Promote the kit's grouped/stacked bars next wave?
15. **(D-Q4)** Status-watch amber light-mode = 3.02:1 vs page — the R-D3 graphic floor with zero
    margin. Comfortable for charts, or lift?
16. **(D-Q5)** TWO delta conventions now live (charts `data/delta/gain·loss` vs Stat-card's R-D5
    rag arrows) — one canon convention, or a deliberate chart/card split?

## 2b. WAVE-1 RULINGS 1–7 (unchanged, rule with the above)
1. **Form-label weight** — the `.t-cm-label` composite renders 400; gated Input-fields labels are
   16/500. Rule 400 (Input-fields migrates later) or mint a 500 form-label composite (one type.css
   line + binding).
2. **`input-error` null slot** — the ADR-0010 slot you anticipated is NOT declared; all four form
   components bind semantic `rag/error` directly. Declare the null slot?
3. **Toast dark glyphs** — coloured shapes on the ELEVATED NEUTRAL ground (all ≥3.55); the
   white-shape dark ruling was made on TINTED grounds. Confirm or extend.
4. **Modal family fold** — Modal-lightbox extends Modals as a separate snippet; fold into one
   modal-family snippet later, or keep split + a dialog-mechanics partial when a group accretes?
5. **Figure vouch** — figure-4/5/6 composites still "PREPARED, awaiting vouch"; vouching flips
   Amount-display candidate→canon + hardens Stat-card's value type.
6. **★ Field-family accretion** (ADR-0013 ruling 3, cross-lane OBSERVED duplication — the
   wave's standout): field chrome (hover fill · focus black border + 4px stroke · error stroke)
   now consumed by copy across ≥7 files (Input-fields, Dropdown, Search-field + A's four +
   Account-selector). Accrete `field-family` as registry group #2 next wave?
7. **Showroom Overlays split** — B proposes Overlays (Drawer/Popover/Lightbox/Modals/Tooltip) +
   Data-display buckets; wave 1 filed into existing buckets. Re-bucket?
   *(Minor, flag-if-wrong: conductor decided the mixed-size idiom = local `--phys-size` override,
   inscribed in the registry; Secure-entry holds figure-3/24 in its 40px narrow cells (A-Q3);
   fl-summary ≈ Alert filed to the dedup pass (A-Q4); linked Stat-card variant awaits the
   press/link posture question (B-Q6).)*

## 3. ★ THE STANDING EYEBALL SET (NON-BLOCKING — your "foundations first" ruling; pin-comments
now live in every showroom pane, so it's async)
**(a) B-D7 motion:** Button/Modals presses calm down · Progress-tracker scale press + dots↔line
collapse through 520px · Icon-button identical · `#theme=legacy`/`#theme=supercharge` = colour-only.
**(b)** SC dark sheet `reviews/SC-DARK-MODE-2026-07-22-v1.REVIEW.html` + 4 held whites + Console
radius px + bigplay. **(c) NEW from Phase-2:** all 24 new components across 4 themes × light/dark — the Charts 4 double
as the dataviz sign-off (§C·2).

## 4. Enact-queue (cheap, post-rulings)
F1 Legacy icon/default white · F2 Legacy `rag/error-tint` · tag-atom radius reconcile · F5 Dropdown's
6 locals · designer-pack v2.1 re-bake · **pro-forma dedup pass (ruling 3 — now also carries wave-1's
fl-summary≈Alert + B's observation that Tranche-1/2 hold earlier empty-state/toast sketches)** ·
composite motion tokens (would retire the matchValues pin) · enact whatever §C·2/§C·3 rulings change ·
consider `--verify` blocking.

## 4b. ★ QUEUED: button-states finesse pass (Dave 2026-07-22, "not now — follow up") *(was §C·3b — the wave-1 briefs/receipts + prior deltas point here under that number)*
Full brief in `_FUTURE-STATE.md` §button-states-finesse. Headlines: **Legacy state-mechanism fidelity
question** (as-built may be OPACITY, we render colours — VERIFY against source, don't flip on
recollection; "Legacy shouldn't change" = the design is frozen, our reproduction of it can be
corrected) · **Mono+Console pressed = darker pressed fill** (ties to the open tertiary/quaternary
pressed-token gap; B-D7's softer darken makes this more visible) · **SC keeps the opacity option
open, probably won't change** · **loader ATOM for all loading states** (registry group candidate #2;
Button's `.spin` = first consumer). Theme posture, Dave: Legacy frozen; Mono/SC/Console all in
design development. Natural shape: one session = fidelity check + pressed-tint tuner (review HTML,
rule live) + loader accretion.

## 5. Parked (unchanged)
Legacy hex seeding + provenance-gate flip · Console/Supercharge chromatic palettes · T9 review ·
Sutherland field test · full-review backlog (`_REVIEW-SIGNOFF.md`) · `_FUTURE-STATE` items ·
spot-illustration/empty-state icon set (`_ICON-GAPS.md`, wave-1's only gap).

> **COMMIT STATE.** Everything pre-wave is **PUSHED ✓**. This wave = **2 commits pending push via
> GitHub Desktop**: **`60e4dc1`** (Phase-2 wave 1 — 92 files, the 14 components + conductor serials)
> + the wrap commit carrying this handoff. Build green **51/51** (54 snippets / 54 metas); census
> 32→32; radius 35-strict clean.
