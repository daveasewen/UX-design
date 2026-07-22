# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-22 (morning→midday, FABLE solo): **THE THEMING CLEAN-ROOM RAN END-TO-END — ADR-0014 RULED + BUILT, build 45/45.** The **neutral DNA tier** (`color/neutral/1–15`) is live: ~100 semantic aliases rebound, Mono proven resolution-invariant 3 ways. The **warm ramp is PULLED and inscribed** (`color/warm/1–15`, Figma SVG-fill extraction; step 2 `#13110E` = your ink, confirmed a ramp step; light end `#F7F6F4` warm off-white). **Anchor remap** `neutral/4 → warm/2` (ink ≡ digital-black ≡ action fill). **State mechanism is a theme property** with the blocking **snap gate** (`_validate_state_snap.py`, calibrated on v7 + R-D23 tabs). **Console LOCKED ≡ Mono** (fence in the registry, selftest-enforced). **R-D23 + R-D24 enacted** in tokens/utils — the LAST Mono Legacy-red (`tabs/active`) is evicted. **Supercharge renders WARM end-to-end** (109 paths, 100 component projections). Graph seed reconciled — **zero mismatch** after finding 25 unfed edges spanning 3 sessions. **⚠ AWAITING YOU: `reviews/SC-DARK-MODE-2026-07-22-v1.html`** (SC dark = provisional-agent, no Figma source) **+ 4 held whites.** Render-verify owed (sandbox refused headless-shell). **⚠ RACE NOTE:** the morning Opus session committed its wrap (`5459a4b`, incl. **ruling 3 RULED: tranches fold in as near-canonical + dedup pass**) 14s into this session — reconciled cleanly, receipted; the morning batch is FULLY closed.
> **RENAME THIS CHAT →** `Apollo theming clean-room BUILT — ADR-0014: neutral DNA tier + warm ramp + snap gate · anchor remap · R-D23/24/25 enacted · seed reconciled [FABLE solo]`
> **TITLE THE NEXT (fresh) CHAT →** `Apollo post-ADR-0014 review — Dave rules SC dark sheet + 4 held whites + pro-forma fold-or-keep · enact tweaks · then queue the ADR-0013 clean-room [Opus]`
> *(⚠ Titles are LABELS — the role word comes from your opener line, never from a title. Fresh session: read this file, then `_LIVE-STATE.md` top delta.)*
>
> ---
>
> ## PRIOR — 2026-07-22 (early morning, Opus): tabs RULED (R-D23) + **R-D24** inscribed; **ruling 3 RULED in its wrap `5459a4b`** (*"Pro-forma is Mono in a different name so yes"* — fold in as near-canonical, dedup pass tracked). The morning batch is CLOSED; the dedup pass joins the queue.

---

*Briefing — refreshed 2026-07-22 ~midday BST (date from `date`), session "Apollo theming clean-room"
(FABLE solo; ADR-0014 designed → Dave ruled by number in-chat → built + gated same session).
§A = standing orientation · §B = this session · §C = queue.*

## ⬛ DO THIS FIRST

> **1. ★ DAVE'S REVIEW PASS (cheap window, or rule live in any session):** open
> `reviews/SC-DARK-MODE-2026-07-22-v1.REVIEW.html` (SC dark values + calculated raises — all
> provisional-agent, "we can always change") · the **4 held whites** (`text/on-action`,
> `text/on-inverse`, `icon/on-inverse`, `border/action-strong` — flip to warm = one line each) ·
> `showroom/index.html#theme=supercharge` (the library, warm; Tabs page = bar/badge/fade) ·
> **ruling 3: pro-forma tranches fold-or-keep** (§C·1).
> **2. Then the ADR-0013 CLEAN-ROOM (fresh window, FABLE solo, SERIAL, full budget)** — unblocked,
> scope pinned in ADR-0013's Consequences; ds-008 + ds-009 fixes ride with it (§C·2).

*Standing practice: every handoff carries both names — retrospective + forward — and a **DIVVY
PLAN**. This handoff's plan is SERIAL: Dave's review pass (any model, cheap) → ADR-0013 clean-room
(Fable solo) → only THEN the Phase-2 parallel fan-out (conductor + 2 workers). No shared-file
overlap until fan-out. Steps 4b + 2 in `_RUNBOOK-capture-ritual.md`.*

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
> *(2026-07-22 instance: the warm ramp is OBSERVED (Figma pull, provenance in `colour.json`); every
> Supercharge DARK value is INFERRED (no Figma source) and is marked provisional-agent on the sheet.)*
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** ⇒ **Before designing anything,
> CONSULT: `python3 knowledge/_consult.py "<what you're about to design>"`** (rules · rulings · assertions ·
> gates + where each bites). Runbook: `knowledge/_RUNBOOK-consult.md`. *(Blind spot ds-009 — the
> `_BUTTON-DECISIONS.md` ledger is not in its corpus; fix lands with the ADR-0013 session.)*

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

## ★ ONE token store · ONE baseline library · FOUR themes (R-D15 → ADR-0011 → ★ ADR-0014, 2026-07-22)
*Themes are **override sets at the semantic tier**, and since ADR-0014 they carry **their own neutral
primitive ramps** through the **neutral DNA tier**: semantic roles alias `color/neutral/1–15` (never
`color/mono/*` directly); base binds neutral→mono; a theme swaps its whole neutral substrate in one
15-line override block. **Neutral indices are SEMANTIC POSITIONS** (neutral/4 = the anchor: ink ≡
digital-black ≡ action fill) — themes bind by index and REMAP where their ramp's shape demands
(Supercharge anchor → its step 2). **State mechanism is a THEME PROPERTY** (registry `stateMechanism`)
with one test, gated blocking: opacity-for-states is allowed IFF the composite snaps to a step of the
active theme's `neutralRamp` (`_validate_state_snap.py`). **Sibling pairs (Dave's spine):** {Mono,
Console} share neutrals/opacity/status/dataviz — **Console is FENCED** from diverging (registry
`fencedPaths`, selftest-enforced); {Legacy, Supercharge} are structural siblings, different palettes.
**Red is themed (R-D19 → completed by R-D23):** zero Legacy reds remain in the Mono base.*
The four themes (Dave's canonical order):
- **Apollo Legacy** — faithful reproduction of the existing HSBC system: brand red `#DB0011`, teals,
  `color/grey/*` (+ its 6-step dark set). **AA-EXEMPT as-built (R-D24)** — pairs surface as EXEMPTED
  (documented), never passes. Does NOT ride the DNA tier (explicit per-path overrides). Never deleted.
- **★ Apollo Mono** — the baseline we build NOW. "Very mono": colour ONLY in RAG status + dataviz.
  Neutral scale = `color/mono/1–15`; only red `#B92F1E` (status/RAG/dataviz).
- **Apollo Console** — branded HSBC library. **LOCKED ≡ Mono** on neutrals/opacity/status/dataviz
  (fence); live divergence = rounded corners (radius overrides, values provisional). Chromatic layer parked.
- **Apollo Supercharge** — brand-uplift. **Carries its OWN warm ramp** `color/warm/1–15` (OBSERVED,
  Figma pull 2026-07-22; ink = `warm/2 #13110E`; light end `#F7F6F4` ≠ white). States = COLOUR by
  default (hued ramp — fades drag hue off-ramp). **Dark mode = provisional-agent, awaiting Dave.**

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores — the retrieval source
    colour.json       primitives: mono/1-15 · ★ neutral/1-15 (the DNA tier, aliases mono) ·
                      ★ warm/1-15 (Supercharge, OBSERVED w/ provenance) · grey/100-800 + dark-mode/1-6 (Legacy)
    semantic-colour.json  roles alias color/neutral/* (ADR-0014) + rag/* + component tiers + $extensions.apollo.state
    themes/           the four override sets + _themes.json registry (★ now: stateMechanism ·
                      load-bearing neutralRamp · siblingPairs · console fencedPaths)
  snippets/           40 gated reference components = CANON
  canon/              canon.css (token spine · components · AUTO-THEMES cascade — 147 paths) +
                      type.css (HAND-AUTHORED) + generators (gen_canon_tokens · gen_theme_cascade —
                      ★ override sets may carry $alias · gen_canon_components ⚠ joins the build per ADR-0013)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (generated)
  _proforma/          Apollo Mono tranches T1–T9 + Masthead + DataViz + the decisions ledgers
  _consult.py         ★ "what governs X?" — RUN IT before designing (ds-009 blind spot: B-D ledger)
  _validate_*.py      the gates — ★ incl. _validate_state_snap.py (ADR-0014, blocking, selftest wired)
  gen_showroom.py     ★ generates showroom/ — never hand-edit showroom
showroom/             ★ THE LIBRARY, browsable: 40 harness pages + index (#theme=supercharge = warm)
reviews/              review sheets — ★ AWAITING DAVE: SC-DARK-MODE-2026-07-22-v1(.REVIEW).html
notes/_receipts/      worker-receipt dir · notes/_briefs/ conductor briefs
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative — ★ 2026-07-22 dossier = the clean-room arc + Figma method
```

## The one command that matters
```
python3 knowledge/_build_all.py     # ★ 45 steps (42→45: cascade selftest + snap gate + snap selftest), exits non-zero on any failure
```

## Rules that actually bite (core + this session's)
- **CONSULT before designing** — then **survey before build**. *(This session it caught a stale-RED
  selftest and two already-inscribed rulings the handoff denied.)*
- **★ ADR-0014: semantic neutrals alias `color/neutral/*`, NEVER `color/mono/*` directly** — the DNA
  tier is how themes re-align. Whites are classified: substrate → `neutral/15`; absolute (on-status,
  dataviz, type26-013 emphasis) → `color/white`, pinned.
- **★ ADR-0014: opacity states must SNAP** — stored colour = exact step of the active theme's ramp,
  flatten within 8/255 luma (`_validate_state_snap.py`, blocking). Mechanism per theme: Mono+Console
  opacity · SC colour · Legacy explicit (no fades).
- **★ Selftests are BUILD STEPS** — a selftest that only runs by hand rots (the stale Supercharge-empty
  assertion sat red a day). New gates ship selftests AND wire them.
- **★ ADR-0013 (ruled, build pending): organisms RETRIEVE atom rules via partials — never re-type a
  sub-atom.** Until the clean-room lands: no new local button recipes in any snippet.
- **Grey-tint standing check:** surface a grey with its numbers; Dave usually rules "black" but CHECKS.
  *(Generalised this session: the 4 held whites were surfaced, not auto-swapped.)*
- **type26-013 (BLOCKING): white type is red-only (emphasis)** · **R-D6: glyph contrast by ROLE** ·
  **`RULED_PAIR_EXCLUSIONS`** + ★ **`LEGACY_THEME_EXEMPTIONS`/`legacy_exemption()`** (R-D24 —
  theme-aware audits MUST route Legacy pairs through it, recorded EXEMPTED never passed).
- **canon.css** — generated only between AUTO markers; type.css HAND-AUTHORED. ⚠ Until ADR-0013 ruling 4
  is built, snippet RULE-text changes still need `gen_canon_components.py` by hand.
- **Every selector appended to `canon/type.css` is GLOBAL** — register in `_type-bindings.json` or the
  blast-radius gate fails.
- **Icons: real assets only** · **4px grid** · **sentence case** · **square corners in Mono** (radius =
  ROLE tokens, per-theme) · **weights: 100/300/400/500/700 only, NO 600.**
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
  *(SC dark values are agent-derived and therefore AWAIT him.)*
- **Spine discipline** — state lines in `_LIVE-STATE`; narrative >10 lines → `_DECISION-HISTORY/`.
- **Inscription prose is PARSER-VISIBLE:** the decision-graph parser reads ADR headers/Edges lines —
  a prose parenthetical naming a node creates a phantom edge (bitten 2026-07-22; header reworded).

## Standing instructions for the agent
- **Announce the model/routing split at the START of every substantive task** (`MODEL-ROUTING.md`).
- **Verify before asking** (read repo / run gates) — **including your own flags** (the "Legacy dark ink
  OPEN" flag was already answered in the override set). **Reflect back before recording** a ruling.
- **Decision-heavy / material-referring choices ship as review HTML** (`knowledge/_review/_make_review.py`
  — note the path; it is NOT at knowledge/ root). Architecture calls = the ADR-0012/0013/0014 model:
  options + firm recommendations in-chat, Dave rules by number, inscribe same hour.
- **Surface spin-off candidates**; register ideas in `_FUTURE-STATE.md`. **Run the capture ritual
  unasked**; **stamp dates from `date`**. **Memory accelerates; the repo is the record.**

## The other standing documents (REACHABILITY-GATED by `_validate_standing_instructions.py` STAND-002 — keep every one referenced here)
`_STANDARDS.md` (★ the standards hub) · `AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D14) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…**R-D25**; R-D23 tabs · R-D24 Legacy AA-exempt · R-D25 = the ADR-0014 pointer) ·
`knowledge/_STYLE-PROVENANCE.md` · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`docs/decisions/ADR-0012-decision-graph-edge-convention.md` (seed `notes/_decision-graph-seed-2026-07-21.json` —
★ reconciled 2026-07-22, zero mismatch; feed it EVERY inscription, or `--verify` drifts silent) ·
`docs/decisions/ADR-0013-component-type-tier-composition.md` (build = §C·2) ·
**★ `docs/decisions/ADR-0014-per-theme-neutral-primitives-state-snap.md`** (the DNA tier + snap test — this session) ·
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…B-D5 — ⚠ ds-009: not in the CONSULT corpus) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` · `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` · `docs/decisions/ADR-0011-four-theme-token-architecture.md` ·
`knowledge/_DS-IMPROVEMENTS.md` (ds-007 · ds-008 · ds-009) · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` · `knowledge/guidelines/_rules-index.json`. **Runbooks** indexed by `knowledge/_RUNBOOKS.md`.
*(This list was dropped in a rewrite once and STAND-002 red-flagged it — do not prune it.)*

## Parallel-session model (PROVEN 2026-07-21)
On "read good morning", role is picked (Worker / Conductor / Solo) — **from Dave's opener line ONLY;
titles are labels.** ONE conductor = single writer for shared state; workers emit receipts to
`notes/_receipts/`, no git. Conductor reconciles the shared tree before committing (never blind
`git add -A` with workers live). Every handoff carries a **DIVVY PLAN**. Workers can absorb live Dave
rulings mid-flight — receipt verbatim.

## Renders — REAL FONT, in-sandbox
Playwright headless-shell recipe: memory `sandbox-html-rendering` (apt-get download libs → dpkg -x →
LD_LIBRARY_PATH + PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1; HSBC TTFs → ~/.fonts). ⚠ **2026-07-22:
this sandbox REFUSED the headless-shell download** (node error at install) — render-verify for the
ADR-0014 work is OWED; verification stood on the 3 mechanical proofs + selftests. HTML is what Dave
reviews; PNGs are for my own verification.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`knowledge/_review/_make_review.py <file>`).
- **Live tuners beat static versions past ~2 colour round-trips.** Sheets read canon.css LIVE, never retype.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — run it,
  don't improvise. `unable to unlink … *.lock` warnings = the delete-guard, not failure; judge by HEAD.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-22 — "the theming clean-room: ADR-0014 ruled + built in one pass")

*Arc with the why: `_DECISION-HISTORY/2026-07-22-theming-cleanroom-adr-0014.md`. Dave ruled the
7-point reflect-back by number in-chat; everything below landed the same session.*

- **✅ ADR-0014** — neutral DNA tier (~100 rebinds, Mono invariant ×3 proofs) · warm ramp pulled
  (SVG-fill extraction; ink=step 2 cross-check) · anchor remap (indices = semantic positions) ·
  snap gate blocking + calibrated · sibling pairs + Console fence · selftests wired (build 42→45).
- **✅ R-D23 + R-D24 enacted** (tabs tokens + Legacy as-built overrides + `legacy_exemption()`);
  the last Mono Legacy-red evicted. **R-D25** inscribed as the ledger pointer.
- **✅ Graph seed reconciled** — 25 unfed edges across 3 sessions found by hand-run `--verify`;
  zero mismatch now; promote-verify-to-blocking queued as an open question.
- **🐛 Wrong:** PNG-fetched an SVG; flagged an already-answered "OPEN"; a prose parenthetical made
  a phantom edge. **Owed:** render-verify (sandbox refused headless-shell).

---

# §C · QUEUE

## 1. ★ DAVE'S REVIEW PASS (cheap; rule live or in an Opus window)
**(a) SC dark sheet** `reviews/SC-DARK-MODE-2026-07-22-v1.REVIEW.html` — dark values, 3 calculated
raises, all provisional-agent. **(b) The 4 held whites** (on-action / on-inverse ×2 /
action-strong) — flip to warm is one line each. **(c) Showroom under `#theme=supercharge`** —
whole-library warm eyeball; Tabs page = R-D23 bar/badge/fade. **(d) ~~Ruling 3~~ RULED in `5459a4b`** (fold in as
near-canonical — the **reconcile/dedup pass** it mandates joins §C·3). **(e) Console radius px**
(8/12 provisional) + **bigplay eyeball** — both still open from earlier queues.

## 2. ★ THE ADR-0013 CLEAN-ROOM (fresh window, FABLE solo, SERIAL, full budget)
Scope pinned in ADR-0013 Consequences: `component-types.json` registry · partial generator
(AUTO-PARTIAL injection) · sync + ratchet gates (+selftests) · `gen_canon_components` into
`_build_all` · ds-008 + ds-009 fixes · motion tokens · proofs Button → Modals → Progress-tracker →
Icon-button. Exit gate: change a factor once in Button; every consumer moves; build green.

## 3. Enact-queue (cheap, post-rulings)
F1 Legacy icon/default white · F2 Legacy `rag/error-tint` · tag-atom radius reconcile · F5
Dropdown's 6 locals · designer-pack **v2.1 re-bake** · ★ NEW: enact whatever §C·1 changes
(SC dark tweaks = token edits; white flips = one-liners) · consider `--verify` blocking.

## 4. Parked (unchanged)
Legacy hex seeding + provenance-gate flip (post foreign-hex cleanup) · Console/Supercharge
chromatic palettes · dedup pass · T9 review · Sutherland field test · full-review backlog
(`_REVIEW-SIGNOFF.md`) · `_FUTURE-STATE` items (theme-generator now has its substrate).

> **COMMIT STATE.** This wrap = **1 commit** on top of the morning's 2 — **Dave pushes 3 via
> GitHub Desktop.** Build green **45/45** at wrap; tokens/generators/gates all touched this
> session, projection + cascade + showroom all regenerated + in sync.
