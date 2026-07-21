# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-21 (late night #3, FABLE solo): **THE ARCHITECTURE CALL IS RULED — ADR-0013.** Composition = **generated partials** (atoms declare rule-blocks; a generator injects them into consuming snippets between AUTO-PARTIAL markers; sync + ratchet gates make local re-implementation a build failure) + the **component-type tier** — ONE registry (`knowledge/component-types.json`) carrying a group's **values (parameter tokens) AND rules (partials)**; resolution = one new hop in the alias chain (component → type-group → semantic role → default). **Mechanism lands BEFORE Phase-2 fan-out** — the radius ratchet priced retro-fit at 21 files/three sessions; fan-out first would re-book that at ~90. The T-D9/T-D12 symmetry sealed it: partials are the box-side twin of the type-composite system. Also: **ds-009** (CONSULT corpus omits `_BUTTON-DECISIONS.md` — B-D rulings were unfindable) and **the gauge's Half-2 measurement is BROKEN** (wrong session + stub transcripts — warning inscribed; in-head tally governs). Ruling batch was NOT run — it moved to the next window by the gauge call (~52% mid-Amber wrap).
> **RENAME THIS CHAT →** `Apollo architecture RULED — ADR-0013: composition = generated partials + component-type tier (one registry, values+rules) · mechanism BEFORE Phase-2 · ds-009 + gauge Half-2 broken [FABLE solo]`
> **TITLE THE NEXT (fresh) CHAT →** `Apollo ruling batch on the showroom — Console px · Legacy AA-fidelity ×2 · pro-forma fold-or-keep · tabs/active · bigplay — then queue the ADR-0013 clean-room`
> *(⚠ Titles are LABELS — the role word comes from your opener line, never from a title.)*

---

*Briefing — refreshed 2026-07-21 ~23:15 BST (date from `date`), session **"Apollo rulings + architecture"**
(FABLE solo; the composition/atom-retrieval + flex-tier strategy call, taken first at Dave's
instruction — the ruling batch moved to the next window). §A = standing orientation · §B = this
session · §C = queue.*

## ⬛ DO THIS FIRST

> **1. Push 1 commit** (GitHub Desktop): the ADR-0013 wrap.
> **2. The RULING BATCH is still owed (§C·1)** — all five items visible on the harness
> (`showroom/index.html`). Short window, Opus. Then the enact-queue (§C·3).
> **3. Then open the ADR-0013 CLEAN-ROOM (§C·2) as its own fresh window — Fable solo, SERIAL,
> full budget** (the Phase-0 precedent). The build scope is pinned in ADR-0013's Consequences.

*Standing practice: every handoff carries both names — retrospective + forward — and a **DIVVY
PLAN** (what parallelises, lanes + models, what stays serial, shared files per lane). This handoff's
plan is SERIAL: batch window (Opus) → clean-room (Fable solo) → only THEN the Phase-2 parallel
fan-out (conductor + 2 workers). No shared-file overlap until fan-out. Steps 4b + 2 in
`_RUNBOOK-capture-ritual.md`.*

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
>
> **The real danger is not forgetting — it is confident false inscription.** Records carry provenance
> and confidence, not just content. Corrections get inscribed as loudly as the original claim. **Mark
> what was OBSERVED versus what was INFERRED.** The ritual stamps dates from `date`, never from belief.
> *(Live example, 2026-07-21 late night #3: the gauge's own out-of-band measurement read the WRONG
> session off a stub transcript and reported 19% — then rationalised it. Caught against the in-head
> tally, discarded, and the failure mode is now inscribed in the gauge runbook itself.)*
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** ⇒ **Before designing anything,
> CONSULT: `python3 knowledge/_consult.py "<what you're about to design>"`** (rules · rulings · assertions ·
> gates + where each bites). Runbook: `knowledge/_RUNBOOK-consult.md`. *(And know its current blind spot:
> ds-009 — `_BUTTON-DECISIONS.md` is not yet in its corpus; fix lands with the ADR-0013 session.)*

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* New-starter style: assume the reader has no context.
> **Update it when the shape of the project changes, not every session — but never drop it, and never
> shorten it to a label.** *(Also step 2 of `_RUNBOOK-capture-ritual.md`; reachability-gated by
> `_validate_standing_instructions.py`.)*

## What Apollo is
A **governed design-system engine** for agentic UI generation. The bet: *generation is a commodity* — the value
is the layer around any generator. Two principles run through everything:
- **Retrieval, not recall.** Brand values are retrieved from token stores, so generated work can't drift off-brand.
- **Verification = enforcement.** Judgment is encoded as **blocking gates**; "done" is withheld until they pass.
  If a rule isn't gated, assume it will be broken.

Tagline: **"lovable on rails."** Four phases: **Discover** → **Create** (what's being built now) → **Craft**
(the review-overlay docs ARE this) → **Dispatch**.

## ★ ONE token store · ONE baseline library · FOUR themes (R-D15 → wired as **ADR-0011** override sets, 2026-07-20)
*Themes are **override sets at the semantic tier** (Mono = base · Legacy = populated override · Console +
Supercharge = declared nullable slots — **Supercharge carries its FIRST populated path since R-D22:**
`progress/complete`). Registry `tokens/themes/_themes.json`; record `knowledge/_STYLE-PROVENANCE.md`; advisory
theme-provenance gate. **Red is themed (R-D19):** Legacy red `#DB0011`/`#A8000B` = Legacy only; Mono's only red
`#B92F1E` = status/RAG/dataviz only. Since R-D22, `tabs/active` is the LAST role still resolving a Legacy red in
the Mono base (archived consumer).*
The library is **theme-agnostic**: components bind a semantic role ("success", a grey ink); the **active theme's
override set** decides the hex. Nothing hardcodes a theme's colour. **Adding a theme = adding an override set,
never forking.** The four themes (Dave's canonical order):
- **Apollo Legacy** — carries the **teals** (`rag/success` #00847F …) AND the HSBC brand grey scale
  `color/grey/100–800`. Retained for legacy interfaces; superseded over time, never deleted.
- **★ Apollo Mono** — the baseline we build NOW. **"Very mono": monochrome throughout — colour appears ONLY
  in RAG status + data-vis.** Its neutral scale = the new `color/mono/1–15` ramp (NOT `color/grey/*`).
- **Apollo Console** (was Apollo UI, the branded HSBC library) · **Apollo Supercharge** (SC, the brand-uplift
  work). Both carry the broader new-colour palette — that's the **parked** colour/theming build ("later").

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores — the retrieval source
    colour.json       primitives: brand grey/100-800 (Legacy) + NEW color/mono/1-15 (Mono ramp)
    semantic-colour.json  rag/* fills + progress/complete ink pair + component tiers
    themes/           ★ the four override sets (ADR-0011): _themes.json registry + apollo-*.overrides.json
  snippets/           40 gated reference components = CANON (all on role radius tokens since Phase 1)
  canon/              canon.css (three AUTO blocks: token spine · components · ★ AUTO-THEMES cascade)
                      + type.css (HAND-AUTHORED composites) + the generators (gen_canon_tokens ·
                      gen_canon_components ⚠ NOT in the build YET — joins it per ADR-0013 ruling 4 ·
                      ★ gen_theme_cascade — the [data-apollo-theme] layer)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (465, generated)
  _proforma/          Apollo Mono tranches T1–T9 + Masthead + DataViz + the decisions ledgers
  _consult.py         ★ "what governs X?" — RUN IT before designing (ds-009 blind spot: B-D ledger)
  _validate_*.py      the gates; orchestrated by _build_all.py (42 steps)
  gen_showroom.py     ★ generates showroom/ from snippets + tokens + cascade — never hand-edit showroom
showroom/             ★ THE LIBRARY, browsable: 40 harness pages + categorised index
reviews/              scratch/archive (demoted by the showroom ruling) + the review sheets you mark up
notes/_receipts/      ★ conventioned worker-receipt dir (parallel-session reconcile trail)
notes/_briefs/        ★ conductor-written worker briefs
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative, relocated verbatim
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 42 steps, all gates, exits non-zero on any failure
```

## Rules that actually bite (unchanged core + this session's)
- **CONSULT before designing** (see the Memento block) — then **survey before build**.
- **★ ADR-0013 (ruled, build pending): organisms RETRIEVE atom rules via partials — never re-type a
  sub-atom.** Once the clean-room lands, a local re-implementation of a registered partial FAILS the
  build (ratchet gate). Until then: do not add new local button recipes to any snippet.
- **Grey-tint standing check** (Dave 2026-07-19): when a grey turns up, **surface it with its numbers** —
  Dave usually rules "make it black" but **checks first; never auto-swap.**
- **type26-013 (BLOCKING): white type is red-only (emphasis); black/dark-grey everything else.** R-D22's
  arithmetic reconfirmed the badge numeral stays WHITE (black fails both Mono reds).
- **R-D6: glyph contrast is by ROLE** — label-paired glyph 3:1; meaning-alone glyph 4.5.
- **`RULED_PAIR_EXCLUSIONS`** (in `_contrast_utils.py`): ruling-forbidden pairs are excluded from the audit.
- **canon.css** — generated only *between* the AUTO markers; type.css is HAND-AUTHORED throughout.
  ⚠ **Until ADR-0013 ruling 4 is built, snippet RULE-text changes still need `gen_canon_components.py`
  run by hand** (values self-heal via the projectors; rule text does NOT).
- **Every selector appended to `canon/type.css` is GLOBAL** — register in `_type-bindings.json` or the
  blast-radius gate fails.
- **Icons: real assets only** · **4px grid** · **sentence case** · **square corners in Mono** (radius = ROLE
  tokens `border-radius/control|surface|indicator`, taxonomy ratified, values per theme) · **weights: five
  licensed only — 100/300/400/500/700, NO 600.**
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
- **Spine discipline** — state lines in `_LIVE-STATE`; narrative >10 lines → `_DECISION-HISTORY/` at write time.

## Standing instructions for the agent
- **Announce the model/routing split at the START of every substantive task** (`MODEL-ROUTING.md`).
- **Verify before asking** (read the repo / run the gates). **Reflect back before recording** a ruling — a lean
  is not a ruling; British understatement, "quite good" is not approval.
- **Decision-heavy / material-referring choices ship as a review-template HTML** (`_make_review.py`) — but only
  for GENUINELY OPEN questions. (Architecture calls are the exception: the ADR-0012/0013 model — options +
  firm recommendations in-chat, Dave rules, inscribe same hour.)
- **Surface spin-off candidates**; register ideas in `_FUTURE-STATE.md`. **Run the capture ritual unasked**
  at session end; **stamp dates from `date`**. **Memory accelerates; the repo is the record.**

## The other standing documents (REACHABILITY-GATED by `_validate_standing_instructions.py` STAND-002 — keep every one referenced here)
`_STANDARDS.md` (★ the standards hub — 3-tier tokens, WCAG floor, authoring rules) · `AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D14) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D22; R-D19 = red is themed; R-D22 = progress is structure) · `knowledge/_STYLE-PROVENANCE.md` (theme-era record) · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`docs/decisions/ADR-0012-decision-graph-edge-convention.md` (ACCEPTED — the edge convention; seed `notes/_decision-graph-seed-2026-07-21.json`, generator `knowledge/_build_decision_graph.py`) ·
`docs/decisions/ADR-0013-component-type-tier-composition.md` (★ ACCEPTED 2026-07-21 — composition via
generated partials + the component-type tier; build pending, §C·2) ·
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…B-D5; Mono primary + state-styling, ADR-0009 — ⚠ ds-009: not yet in the CONSULT corpus) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` · `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` · `docs/decisions/ADR-0011-four-theme-token-architecture.md` ·
`knowledge/_DS-IMPROVEMENTS.md` (…ds-007 leak-resolve gap · ds-008 radius prose trip · ds-009 CONSULT corpus gap) · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` · `knowledge/guidelines/_rules-index.json`. **Runbooks** are indexed by the
generated `knowledge/_RUNBOOKS.md`. *(This list was dropped in a from-scratch GOOD-MORNING rewrite once and
STAND-002 red-flagged it — do not prune it.)*

## Parallel-session model (PROVEN in full 2026-07-21 — conductor + 2 workers)
On "read good morning", role is picked (Worker / Conductor / Solo). **ONE conductor** is the single writer for
shared state (commit + `GOOD-MORNING`/`_LIVE-STATE`); **workers** emit receipts to `notes/_receipts/` and don't
run git. Conductor reconciles the shared tree before committing (`_RUNBOOK-git-commit.md` step 0.5 /
`_RUNBOOK-parallel-conductor.md` step 2.5 — **account for every dirty path; never blind `git add -A` with
workers live**). **⚠ Titles are LABELS, never role assignments — the role word comes from Dave's opener line
only.** **Every handoff carries a DIVVY PLAN:** lanes · model per lane · what stays serial · **shared files
named and assigned to ONE lane**. Workers can absorb LIVE Dave rulings mid-flight — receipt them with verbatim
quotes so the conductor can inscribe (R-D22 was written from a receipt).

## Renders — REAL FONT, in-sandbox
Playwright headless-shell works on ARM64: `apt-get download` the ~19 libs → `dpkg -x` → point
`LD_LIBRARY_PATH` at `.../aarch64-linux-gnu` + set `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`. Copy the HSBC
TTFs to `~/.fonts` + `fc-cache -f`; CSS `font-family:"HSBC_MtUnivers_Latin"`. Full recipe: memory
`sandbox-html-rendering`. HTML is what Dave reviews; PNGs are for my own verification.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`_make_review.py <file>`).
- **Live tuners beat static versions past ~2 colour round-trips** — give the eye a control.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — **run it, don't
  improvise git.** The `unable to unlink … *.lock` warnings are the delete-guard, not failure; judge by HEAD.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-21 late night #3 — "the architecture call: ADR-0013 ruled in one pass")

*Arc with the why: `_DECISION-HISTORY/2026-07-21-composition-architecture-call.md`. Dave took the
strategy call BEFORE the ruling batch ("2 then 1"); the batch then moved to the next window when the
gauge read mid-Amber.*

## What LANDED (this wrap's commit)
- **✅ ADR-0013 ACCEPTED + inscribed** — the four firm rulings (sequence · generated partials ·
  one registry for values+rules · `gen_canon_components` into the build), decided under Dave's
  stated principle: correctness over expedience. `_FUTURE-STATE` tiered-flex entry GRADUATED.
- **✅ The case, quantified:** 13/40 local button recipes · 7 scale-press copies · 4 drifted
  `translateY` (Selection-controls carries both). T-D9/T-D12 named as the precedent — partials =
  the box-side twin of the type-composite system.
- **✅ ds-009 logged** (CONSULT corpus omits `_BUTTON-DECISIONS.md`; B-D1…B-D5 unfindable —
  surfaced by Dave's mid-flight question). Fix + selftest fold into the ADR-0013 session.
- **✅ Gauge Half-2 found BROKEN + inscribed** (wrong session + stub transcript + the subagent
  rationalising the bad number — the confident-false-inscription class, caught by the tally).
  Warning now lives in `_RUNBOOK-context-gauge.md`; Half 1 governs.
- **🐛 What I got wrong:** dispatched the runbook's Half-2 subagent prompt as-written and got
  garbage back TWICE before discarding the instrument — the sniff test (3,250 tokens ≠ this
  session) should have fired before the second dispatch, not after it.

---

# §C · QUEUE

## 1. ★ THE RULING BATCH (Dave, on the harness — `showroom/index.html`; Opus window, short)
**(a) Console radius px** — base/control 8 · surface 12, both still placeholders (roles ratified).
**(b) Legacy fidelity-vs-AA family — TWO members, rule together:** `text/on-success` black-as-built
(6.06:1 AA) vs historical white-on-teal (3.47:1 fail) · badge white-on-`#DB0011` (~4.02:1). One
principle decides both: does historical fidelity outrank AA *inside the Legacy theme*?
**(c) Pro-forma tranches** — fold into the finalised set or stay a pattern library.
**(d) `tabs/active`** — the LAST unruled red (Mono = ink per §A-AUTH lean; archived consumer).
**(e) Video-player bigplay** — on-scrim white enacted, your eyeball owed (incl. Legacy-white question).

## 2. ★ THE ADR-0013 CLEAN-ROOM (fresh window, FABLE solo, SERIAL, full budget — Phase-0 precedent)
Scope pinned in ADR-0013 Consequences: `component-types.json` registry · partial generator
(AUTO-PARTIAL injection + provenance comments) · sync gate + ratchet gate (+ selftests) ·
`gen_canon_components` into `_build_all` (regenerate-always + `--check`) · ds-008 + ds-009 fixes ·
motion tokens (button-family press factors) · proofs **Button → Modals → Progress-tracker**
(Back/Next press VISIBLY changes translateY→scale — Dave's eyeball) **→ Icon-button**.
**Exit gate:** change a factor once in Button; every consumer moves; no local recipe in the proofs;
build green with new gates blocking. Rider: the stepper collapse (canon dots `273d18c~1`) folds into
canon Progress-tracker here.

## 3. Enact-queue (cheap, post-rulings; Sonnet-able unless marked)
**(a)** F1: Legacy `button/primary/icon/default` = #FFFFFF (mirror of the label override) — fixes
Icon-button legacy-dark glyph ~1.8:1; render-verify then Dave promotes. **(b)** F2: Legacy
`rag/error-tint` from the R-D20 eviction record. **(c)** Tag-atom radius role reconcile (canon
splits by context; Dave lean or reflect-back). **(d)** F5: Dropdown's 6 manifest-dodging locals
(Legacy-era greys) — needs Dave (values would visibly change). **(e)** Designer-pack **v2.1
re-bake** (2 commands, in the v2 receipt). *(ds-008 + ds-009 + `gen_canon_components` wiring moved
INTO §C·2 per ADR-0013.)*

## 4. RAG follow-ons (unchanged) + parked
Seed Legacy error/amber/navy into `LEGACY_ONLY_HEXES` + flip theme-provenance advisory→blocking —
both still gated on the broader foreign-hex cleanup. Mono null slots await the ADR-0010 §3 gate.
Console/Supercharge palettes parked (hooks live). Dedup pass. T9 review. Sutherland field test
(ADR-0008 #1). Full-review backlog (`_REVIEW-SIGNOFF.md` — Video-player fast-follower).
`_FUTURE-STATE`: Apollo Labs tuners, bulk type-binding, icon-015 mechanisation, μX edit-mode,
blast-radius gate v2, style-builder.

> **COMMIT STATE.** This wrap = **1 commit ahead** (ADR-0013 + spine + dossier + runbook warning +
> ds-009 + memory) — **Dave pushes via GitHub Desktop.** Build was green 42/42 at session start;
> no token/snippet/generator files touched this session (docs + records only), so the build
> contract is unchanged. Next: the ruling batch (§C·1), then the clean-room (§C·2).