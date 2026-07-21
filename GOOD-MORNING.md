# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-21 (late night, FABLE conductor): **PHASE 0 IS BUILT.** The theme-resolution layer is LIVE — one attribute (`data-apollo-theme`) switches all four themes; **Console renders rounded, Legacy renders red-CTA + teal, Supercharge proven ≡ Mono by pixel-diff**; radius is a real flex slot (37 canon hardcodes evicted); the **showroom exists** (`showroom/index.html` — open it: 40 harness pages, each 4 themes × light/dark side-by-side × width slider × live variant spread). Four new BLOCKING build steps (projection sync · cascade sync · radius gate · showroom sync) → **build green 42/42**. The projector run also surfaced + fixed **silent drift** (T1–T9 still on pre-R-D20 error reds; 4 stale `.cn-button` literals) — that class of rot is now gated forever. Rulings today: **Legacy = square (Dave)** · Console **8px = PROVISIONAL, Dave to rule on the harness** · Legacy `text/on-success` kept **black** (AA) vs historical white-on-teal — **Dave's call queued**. Phase 1 is GO.
> **RENAME THIS CHAT →** `Apollo build-out Phase 0 BUILT — theme cascade live (4 themes × 40 components), radius flex slot + showroom + universal harness, 4 new gates, 42/42 [FABLE conductor]`
> **TITLE THE NEXT (fresh) CHAT →** `Apollo build-out Phase 1 — finalise the 40 through the harness: radius migration (21-file ratchet in _RADIUS-GATE.md) + theme-response audit + showroom sign-off [conductor + 2 Fable workers]`
>
> **★ AMENDED same evening (Dave, on the pushed result): radius is a semantic TIER — "8px can't be
> universal; cards differ from buttons; maximum flexibility; ultimately we build a THEME GENERATOR."**
> Enacted before Phase 1: `layout.json` now carries **default + control/surface/indicator** roles
> (alias-fallback → default; taxonomy PROVISIONAL-agent, refine by evidence); the cascade is
> **alias-aware** (dial the base, roles follow; dial a role, it wins); canon rebound by role; **Cards
> migrated as the second proof — render-verified Console: cards 12px vs buttons 8px.**
>
> **Phase-1 worker brief, turnkey:** per component — (1) rebind radius onto the **ROLE token**
> (`border-radius/control|surface|indicator` — judgment call per element, see the canon census in the
> dossier addendum; snippet CSS + theme-block declarations + manifest) and add the file to
> `MIGRATED_SNIPPETS` in `_validate_radius.py` **in the same change**; (2) eyeball its showroom page
> across 4 themes × both modes — hunt roles the theme SHOULD override but doesn't (the Button
> success-background miss + the Cards red-accent drift are the patterns); (3) `python3
> knowledge/gen_snippet_tokens.py && python3 knowledge/canon/gen_theme_cascade.py && python3
> knowledge/gen_showroom.py` then full build green; (4) receipt to `notes/_receipts/`, no git
> (conductor commits). The 20-file worklist is enumerated in `knowledge/_RADIUS-GATE.md`.
>
> **✅ Dave's parallel worker DELIVERED mid-capture: designer pack v2 SHIPPED** (`Apollo-designer-skills-v2.zip`,
> baked KB from `7071538`, no script in the zip per Dave's ruling, 4 skills refreshed for
> type-composites/themes/drift checks; receipt `notes/_receipts/2026-07-21-worker-designer-pack-v2.md`,
> verification green). Committed separately by the conductor. **Follow-on (cheap): v2.1 re-bake after this
> push so the pack picks up the theme override sets** — the packed `_themes.json` references them but they
> were untracked at the worker's bake commit; 2 commands per the receipt.

---

*Briefing — refreshed 2026-07-21 ~20:12 BST (date from `date`), session **"Apollo build-out Phase 0"**
(FABLE conductor; Dave's designer-skills-v2 worker parallel). Ran `_BUILDOUT-STRATEGY-2026-07-21.md`
Phase 0 serially, CONSULT-first, exit gate met + render-verified. All names + the landed list are in the
★ LATEST block above; §A = standing orientation · §B = this session · §C = queue.*

## ⬛ DO THIS FIRST

> **Open `showroom/index.html` in your browser** — that's Phase 0, live: pick any component, flip the four
> themes, both grounds side-by-side, drag the width. Then three quick rulings queued for you (§C·2):
> **Console's radius px** (8 is my placeholder — the harness shows it), **Legacy `text/on-success`**
> (black AA-pass as-built vs historical white-on-teal AA-fail), and **fold-or-keep for the 12 pro-forma
> tranches**. Then spin **Phase 1** with the next-chat title above — the worker brief is turnkey in the
> ★ LATEST block, the 21-file worklist is `knowledge/_RADIUS-GATE.md`.

*Standing practice: every handoff carries both names — retrospective + forward. Step 4b in
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
> *(This session caught a live example: the `four-theme-architecture` memory referenced "R-D15" that had
> never been inscribed in the ledger — a memory-only record, the anti-pattern. Now inscribed + dated.)*
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** ⇒ **Before designing anything,
> CONSULT: `python3 knowledge/_consult.py "<what you're about to design>"`** (rules · rulings · assertions ·
> gates + where each bites). *(This session's misstep: I built a review sheet to "decide" the RAG text/glyph
> model when R-D6 + `type26-013` + R-D12 B already governed it — skipped CONSULT, retread settled ground.
> Dave caught it. The sheet was binned. CONSULT is not optional.)* Runbook: `knowledge/_RUNBOOK-consult.md`.

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
*Themes are **override sets at the semantic tier** (Mono = base · Legacy = populated override · Console + Supercharge =
declared nullable slots). Registry `tokens/themes/_themes.json`; record `knowledge/_STYLE-PROVENANCE.md`; advisory
theme-provenance gate. **Red is themed (R-D19):** Legacy red `#DB0011`/`#A8000B` = Legacy only; Mono's only red
`#B92F1E` = status/RAG/dataviz only.*
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
    semantic-colour.json  rag/*-background now = R-D14 fills (promoted this session)
    themes/           ★ the four override sets (ADR-0011): _themes.json registry + apollo-*.overrides.json
  snippets/           38 gated reference components = CANON (all now on #1A1A1A dark grounds)
  canon/              canon.css (three AUTO blocks: token spine · components · ★ AUTO-THEMES cascade)
                      + type.css (HAND-AUTHORED composites) + the generators (gen_canon_tokens ·
                      ★ gen_theme_cascade — the [data-apollo-theme] layer)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (465, generated)
  _proforma/          Apollo Mono tranches T1–T8 + Masthead + DataViz + the decisions ledgers
  _consult.py         ★ "what governs X?" — RUN IT before designing (index generated every build)
  _validate_*.py      the gates; orchestrated by _build_all.py (42 steps)
  gen_showroom.py     ★ generates showroom/ from snippets + tokens + cascade — never hand-edit showroom
showroom/             ★ THE LIBRARY, browsable (RULED 2026-07-21): 40 harness pages + categorised index
reviews/              scratch/archive (demoted by the showroom ruling) + the review sheets you mark up
notes/_receipts/      ★ conventioned worker-receipt dir (parallel-session reconcile trail)
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative, relocated verbatim
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 42 steps, all gates, exits non-zero on any failure
```

## Rules that actually bite (unchanged core + this session's)
- **CONSULT before designing** (see the Memento block) — then **survey before build**. *(Both cost me this
  session — I skipped CONSULT and retread the RAG text/glyph model. Don't.)*
- **Grey-tint standing check** (NEW, Dave 2026-07-19): when a grey turns up (grey ink, mid-grey), **surface it**
  with its numbers — Dave usually rules "make it black" but **checks first; never auto-swap.** Memory
  `feedback-grey-tint-check`.
- **type26-013 (BLOCKING): white type is red-only (emphasis); black/dark-grey everything else.** This governs
  RAG text — white on breach, black on every other state. Not a per-case decision.
- **R-D6: glyph contrast is by ROLE** — a glyph paired with a meaning-carrying label needs only 3:1; a glyph that
  carries the meaning alone (arrow, bare number) needs 4.5. Colour is secondary when a label is present.
- **`RULED_PAIR_EXCLUSIONS`** (in `_contrast_utils.py`): pairs a *ruling* forbids (white text × amber/green/blue
  fill) are excluded from the audit — they can't occur, so testing them is testing a non-existent state.
- **canon.css** — generated only *between* the AUTO markers; type.css is HAND-AUTHORED throughout.
- **Every selector appended to `canon/type.css` is GLOBAL** — register in `_type-bindings.json` or the
  blast-radius gate fails.
- **Icons: real assets only** · **4px grid** · **sentence case** · **square corners in Mono** · **weights: five
  licensed only — 100/300/400/500/700, NO 600.**
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
- **Spine discipline** — state lines in `_LIVE-STATE`; narrative >10 lines → `_DECISION-HISTORY/` at write time.

## Standing instructions for the agent
- **Announce the model/routing split at the START of every substantive task** (`MODEL-ROUTING.md`).
- **Verify before asking** (read the repo / run the gates). **Reflect back before recording** a ruling — a lean
  is not a ruling; British understatement, "quite good" is not approval.
- **Decision-heavy / material-referring choices ship as a review-template HTML** (`_make_review.py`) — but only
  for GENUINELY OPEN questions. *(Don't build one to re-decide something already ruled — that's this session's
  binned misstep.)*
- **Surface spin-off candidates**; register ideas in `_FUTURE-STATE.md`. **Run the capture ritual unasked** at
  session end; **stamp dates from `date`**. **Memory accelerates; the repo is the record** — inscribe durable
  content in its repo home, never memory-only.

## The other standing documents (REACHABILITY-GATED by `_validate_standing_instructions.py` STAND-002 — keep every one referenced here)
`_STANDARDS.md` (★ the standards hub — 3-tier tokens, WCAG floor, authoring rules) · `AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D14) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D20; R-D19 = red is themed) · `knowledge/_STYLE-PROVENANCE.md` (theme-era record) · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`docs/decisions/ADR-0012-decision-graph-edge-convention.md` (PROPOSED — the edge convention; seed `notes/_decision-graph-seed-2026-07-21.json`, generator `knowledge/_build_decision_graph.py`) ·
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…B-D5; Mono primary + state-styling, ADR-0009) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` · `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` · `docs/decisions/ADR-0011-four-theme-token-architecture.md` ·
`knowledge/_DS-IMPROVEMENTS.md` · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` · `knowledge/guidelines/_rules-index.json`. **Runbooks** are indexed by the
generated `knowledge/_RUNBOOKS.md`. *(This list was dropped in a from-scratch GOOD-MORNING rewrite and STAND-002
red-flagged it — do not prune it.)*

## Parallel-session model (you were CONDUCTOR this round)
On "read good morning", role is picked (Worker / Conductor / Solo). **ONE conductor** is the single writer for
shared state (commit + `GOOD-MORNING`/`_LIVE-STATE`); **workers** emit receipts to `notes/_receipts/` and don't
run git. Conductor reconciles the shared tree before committing (`_RUNBOOK-git-commit.md` step 0.5 /
`_RUNBOOK-parallel-conductor.md` step 2.5 — **account for every dirty path; never blind `git add -A` with
workers live**). Both were HARDENED this round by the rules-index worker.

## Renders — REAL FONT, in-sandbox
Playwright headless-shell works on ARM64: `apt-get download` the ~19 libs → `dpkg -x` → point
`LD_LIBRARY_PATH` at `.../aarch64-linux-gnu` + set `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`. Copy the HSBC
TTFs to `~/.fonts` + `fc-cache -f`; CSS `font-family:"HSBC_MtUnivers_Latin"`. Full recipe: memory
`sandbox-html-rendering`. HTML is what Dave reviews; PNGs are for my own verification.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`_make_review.py <file>`).
- **Live tuners beat static versions past ~2 colour round-trips** — give the eye a control (the grey-ramp tuner
  this session, the OKLCh tuner before it). Apollo Labs / Layer-2 candidate.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — **run it, don't
  improvise git.** The `unable to unlink … *.lock` warnings are the delete-guard, not failure; judge by HEAD.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-21 late night, FABLE conductor — "Phase 0: the theme-resolution layer")

*Full narrative arc (six findings + the bug): `_DECISION-HISTORY/2026-07-21-phase0-theme-resolution-layer.md`.*

## What LANDED (build 38/38 → 42/42 green)
- **✅ Theme override sets** — `tokens/themes/apollo-legacy.overrides.json` (21 paths, every value from the
  R-D16/R-D18/R-D20 eviction records + registry ownsHexes, per-line `$note` provenance) ·
  `apollo-console.overrides.json` (radius 8px PROVISIONAL) · `apollo-supercharge.overrides.json` (deliberately
  empty = renders as Mono) · registry gains `attr` + `declaredSlots` (Mono null slots kept OUT of the live
  store until the ADR-0010 §3 gate exists).
- **✅ `canon/gen_theme_cascade.py`** — the `[data-apollo-theme]` cascade into canon.css (AUTO-THEMES block):
  root canonical vars + per-component re-projections via each snippet's #token-manifest (root vars can't reach
  the projected literals in `.cn-*` — the survey finding that shaped the design). Both modes always emitted;
  specificity proof in the docstring; selftest green.
- **✅ Radius de-hardcoded** — 37 canon declarations → `var(--border-radius-default)`; Button migrated
  end-to-end (proof); both `resolve()` fns route layout.json; 50%/999px circle+pill idioms stay literal.
- **✅ `gen_showroom.py` → `showroom/`** — 40 generated harness pages + categorised index; theme switch ×
  light/dark panes × width slider × live variant spread; `#theme=` carries index→page (hashchange fixed).
- **✅ Four new BLOCKING build steps** — projection sync · cascade sync · radius gate (strict/advisory
  ratchet, 21-file worklist) · showroom sync.
- **🐛 Caught + fixed same hour:** `project_canon` stomped AUTO-THEMES values on re-run (optional-prefix
  regex) — fenced in the projector; the new cascade `--check` is what caught it. Also caught: silent
  projection drift (T1–T9 pre-R-D20 error reds + 4 stale canon literals) — corrected to ruled values,
  committed separately for attribution.
- **✅ Exit gate verified in-sandbox** (headless shell + real HSBC TTFs): Legacy red CTA + teal (needed
  `rag/success-background` added — caught AT the gate) · Console rounded · Supercharge ≡ Mono by pixel-diff.

## Process notes
CONSULT + survey ran FIRST and paid for themselves twice (the projected-literal finding; the manifests as the
theme join). Both runbooks read + followed at capture. Conductor discipline held: every dirty path named
before staging; Dave's parallel worker tree (designer-skills-v2/) left untouched, receipt awaited.

---

# §C · QUEUE

## 1. ★ NEXT SESSION — Phase 1: finalise the 40 (conductor + 2 Fable workers)
The worker brief is turnkey in the ★ LATEST block. Batching: split the 21 radius-hardcode files
(`knowledge/_RADIUS-GATE.md`) between the two workers; per component also audit its showroom page across
4 themes × both modes (does anything bind a role Legacy should override but doesn't? — the Button
success-background miss is the pattern to hunt) and sign off into the showroom. Conductor reconciles +
commits per `_RUNBOOK-parallel-conductor.md`. **Reconcile Dave's designer-skills-v2 worker (receipt) first.**
Then Phase 2: the ~50 itinerary gaps at pace.

## 2. Rulings queued for Dave (all visible in the harness — open `showroom/button.html`)
**(a) Console radius values** — now TWO dials, both provisional-mine: base/default 8px (controls follow) +
surface 12px (cards/dialogs rounder — your own example, demonstrated on `showroom/cards.html`); rule the
values (+ the role taxonomy if you want different cuts) in `apollo-console.overrides.json` + regenerate. **(b) Legacy `text/on-success`** — kept BLACK as-built
(6.06:1 AA-pass on teal); historical Legacy was white-on-teal (3.47:1 AA-fail) — your call whether
historical fidelity outranks AA inside the Legacy theme. **(c) Pro-forma tranches** — fold into the
finalised set or stay a pattern library (strategy doc open confirmation). **(d)** Later, with (a): Legacy
`rag/warning` amber #FFBB33 is in the override set from the eviction record — sanity-check it in the
harness when a warning-bearing component migrates.

## 3. RAG follow-ons (unchanged; Sonnet-able)
Seed Legacy error/amber/navy into `LEGACY_ONLY_HEXES` (+ Notifications waiver) + flip
`_validate_theme_provenance.py` advisory→blocking — both gated on the broader foreign-hex cleanup (58/67,
parked archived-file relocation). `tabs/active` + `progress/complete` unruled (archived consumers).
Notifications Legacy retag. Spine flag: `text/on-success` `color/black` → `color/mono/4`.

## 4. Parked / carry-forward
Mono null slots into the live store once the ADR-0010 §3 gate is built. Console/Supercharge palettes (when
ruled — the hooks are live). **Designer pack v2.1 re-bake** (post-push, picks up the override sets — receipt
has the 2 commands). Dedup pass. T9 review. Sutherland field test (ADR-0008 #1). Full-review backlog.
`_FUTURE-STATE`: Apollo Labs tuners, bulk type-binding, icon-015 mechanisation.

> **COMMIT STATE.** Ahead of origin by **5**: the two pre-session commits (`4a6f442` + `7071538`) +
> this session's three — `d32a763` (T1–T9 projection catch-up to ruled values) · the Phase-0 commit
> (theme layer + gates + showroom + this capture) · the worker's designer-pack v2 (folded by the
> conductor from the receipt) — **Dave pushes via GitHub Desktop.** Build green **42/42**.
> Next session: **Phase 1, conductor + 2 Fable workers** per the strategy.
