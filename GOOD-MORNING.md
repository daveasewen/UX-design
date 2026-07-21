# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-21 (afternoon, FABLE): decision-graph convention AUTHORED — ADR-0012 proposed, generator + conflict gate BUILT, 8 rulings + 2 conflicts wait on YOUR SHEET. READ THIS FIRST — it supersedes the block + names below.
> **RENAME THIS CHAT →** `Decision-graph: corpus audited (69 nodes/88 edges) → ADR-0012 edge convention + generator/conflict gate built → 8 rulings + 2 conflicts queued on the sheet [FABLE]`
> **TITLE THE NEXT (fresh) CHAT →** `Decision-graph: enact the sheet rulings → inscribe the seed edges (Sonnet, generator-verified) + wire the advisory gate`
>
> **★ DAVE'S ACTION FIRST: rule on `reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.REVIEW.html`** — 8 decision
> controls, **defaults = my recommendations**, live export block (copy the ruling block into the next chat).
> The two that are genuinely yours: **C1** — R-D2 ruled "red/green/blue hold the SAME value in both roles", but
> R-D18/R-D20 split glyph vs background values (recommend: confirm claim superseded); **C2** — R-D7 "red =
> mode-stable, one value" vs R-D20's per-mode error-glyph `#B92F1E`/`#CC4333` (recommend: bound R-D7 to the
> fill role). **Nothing is inscribed into any ledger and the gate is NOT wired until you rule.**
>
> **What landed this session (FABLE, cold — the pinned decision-graph session; build green 37/37 untouched):**
> - **The audit, done by reading not grepping:** 69 nodes / 88 edges (the "~35" estimate was ~2× light). Found
>   THREE edge vocabularies already live (DataViz front-matter `refines/governs/gated_by` · ADR `Extends/Relates` ·
>   target-doc §6) → reconciled via **alias map in the generated view; source files keep their syntax**.
> - **ADR-0012 (proposed):** 7 edge types + `scope=`/`claim=` qualifiers (audit-forced: R-D16 supersedes
>   col25-011 *for Mono only*; R-D11 kills only R-D10's mode-stable *claim* → **AMENDED** state) +
>   **`diverges-from`** for recorded deliberate divergence (DEF-005⇹DEF-006 "do not reconcile" — without it the
>   conflict gate would flag that pair forever).
> - **`knowledge/_build_decision_graph.py`** — generator (LIVE/AMENDED/DEAD/OPEN · reconciliation view ·
>   what-touches-this · validation rollup → `_DECISION-GRAPH.md`) + conflict gate (`--strict`). Selftest bites on
>   unresolved/open/orphan; queued + divergence stay green. Seed: `notes/_decision-graph-seed-2026-07-21.json`.
> - **Sub-call resolved by the audit:** the expensive half of edge-authoring is the JUDGMENT, and the audit did
>   it (the seed). Inscription is mechanical + machine-verifiable → recommend **Sonnet transcribes, generator
>   diffs against the seed** (Decision 7).
>
> **Carried open (unchanged from the morning):** theme-provenance gate advisory (58 hexes / 67 files, parked
> cleanup); `tabs/active` + `progress/complete` unruled; Notifications Legacy retag; `text/on-success` →
> `color/mono/4` spine flag. Errata E1 (GOOD-MORNING's "T-D1…T-D16" vs real T-D1..14) **fixed this capture**.

---

*Briefing — refreshed 2026-07-21 ~15:50 BST (date from `date`), session
**"Decision-graph: audit → ADR-0012 convention → generator + conflict gate"** — the pinned FABLE cold session,
run exactly to its brief; reflect-back guardrail held end-to-end (no ledger inscription, gate unwired).
**SOLO / self-conductor.** All names + the full landed list are in the ★ LATEST block above — that block is
authoritative; the sections below are the standing orientation (§A) + this-session detail (§B) + queue (§C).*

## ⬛ DO THIS FIRST

> The two names are at the top (★ LATEST). **Dave's action gates everything: rule on the 8-control sheet**
> `reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.REVIEW.html` (defaults = recommendations; the export block
> emits a paste-ready ruling set for the next chat). **Next session (Sonnet-able):** enact the rulings —
> inscribe the seed's edges into ledger entries/ADR headers (generator verifies the diff against
> `notes/_decision-graph-seed-2026-07-21.json`), wire `_build_decision_graph.py` advisory into `_build_all.py`,
> add the edge-at-ruling-time step to the capture ritual. Turnkey context: ADR-0012 + the seed + dossier
> `_DECISION-HISTORY/2026-07-21-decision-graph-edge-convention.md`.

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
  snippets/           38 gated reference components = CANON (all now on #1A1A1A dark grounds)
  canon/              canon.css (GENERATED between AUTO markers) + type.css (HAND-AUTHORED composites)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (465, generated)
  _proforma/          Apollo Mono tranches T1–T8 + Masthead + DataViz + the decisions ledgers
  _consult.py         ★ "what governs X?" — RUN IT before designing (index generated every build)
  _validate_*.py      the gates; orchestrated by _build_all.py (34 steps)
reviews/              consumable outputs + the review sheets you mark up (+ the grey-ramp tuner)
notes/_receipts/      ★ conventioned worker-receipt dir (parallel-session reconcile trail)
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative, relocated verbatim
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 34 steps, all gates, exits non-zero on any failure
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

# §B · THIS SESSION (2026-07-21 afternoon, FABLE cold — "the decision-graph edge convention")

*Full narrative arc (why/how, five findings): `_DECISION-HISTORY/2026-07-21-decision-graph-edge-convention.md`.
The morning session's arc (R-D20 + R-D6 A′): `_DECISION-HISTORY/2026-07-21-rag-completion-and-decision-graph.md`.*

## What LANDED (new files only — no ledger/canon edits; build green 37/37 untouched)
The pinned Fable session, run to its brief: **audit → convention → build**, reflect-back guardrail held.
- **✅ The audit** — all 4 ledgers read in full + 11 ADRs + the REVIEW register: **69 nodes / 88 edges**
  (census corrected from "~35"). Regex found 38 candidate lines; the read found 88 real edges — verbless prose
  relations are invisible to pattern matching, which is why inscription verifies against the seed, never re-derives.
- **✅ ADR-0012 (proposed)** — 7 edge types + `scope=`/`claim=` qualifiers + **AMENDED** lifecycle state +
  `diverges-from`; alias map reconciles the three pre-existing vocabularies without rewriting sources.
- **✅ `_build_decision_graph.py` + seed + rulings sheet** — generator + `--strict` conflict gate (selftest green,
  runs clean: 2 conflicts queued, 1 divergence intentional); `notes/_decision-graph-seed-2026-07-21.json`;
  `reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.html` (+ .REVIEW) with 8 controls + export block.
- **🟡 Queued for Dave:** C1 (R-D2 role-uniformity claim vs R-D18/R-D20 splits) · C2 (R-D7 mode-stable scope vs
  R-D20 per-mode error-glyph). Errata E1 (this file's T-D range) fixed in this capture.

## Process notes
CONSULT ran but its lexicon is design-layer (it expanded the query to "dataviz") — the decisions layer has no
consult surface, which is itself evidence for the build; folding the graph JSON into the consult index is queued.
Survey-before-build caught the DataViz front-matter prototype + the ADR header proto-edges before any invention.
Capture ritual + git runbook read and followed, not reconstructed.

---

# §C · QUEUE

## 0. ★ DAVE — rule on the decision-graph sheet
`reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.REVIEW.html`: 8 controls, defaults = recommendations, export
block emits the paste-ready ruling set. C1 + C2 are the two genuinely-yours calls; the rest confirm defaults.

## 1. ★ NEXT SESSION (Sonnet-able, after the sheet) — enact the decision-graph rulings
Inscribe the seed's edges (`notes/_decision-graph-seed-2026-07-21.json`) into ledger entries + ADR headers per
the accepted grammar; **verify by generator diff against the seed** (never re-derive); flip ADR-0012 proposed→
accepted; wire `_build_decision_graph.py` **advisory** into `_build_all.py` (37→38 steps); add the
edge-at-ruling-time step to `_RUNBOOK-capture-ritual.md` step 4; record C1/C2 resolutions per Dave's picks;
fold the graph JSON into the consult index (kills the "CONSULT is design-layer-only" gap). Horizon (separate):
ADR-0007 part 2 — generate `_LIVE-STATE` LIVE/DEAD blocks from the same parse.

## 2. RAG follow-ons (not blocked on Dave; Sonnet-able)
Seed the Legacy error/amber/navy hexes into `LEGACY_ONLY_HEXES` (needs a Notifications waiver in the leak gate) + flip
`_validate_theme_provenance.py` advisory→blocking — **both gated on** the broader foreign-hex cleanup (58 hexes / 67
files, the parked archived-file relocation). `tabs/active` + `progress/complete` still unruled (archived consumers).
Notifications Legacy-theme retag = future build. Small spine flag: `text/on-success` = `color/black` should be
`color/mono/4` (`#1A1A1A`).

## 3. Parked / carry-forward
**Duplicate-dedup pass** (relocate archived files out of Mono scope). Console + Supercharge override sets (when palettes
ruled). **T9 secure entry** awaits review. **Sutherland field test** (ADR-0008 #1). **`designer-skills-v1`** revisit.
Full-review backlog (`_REVIEW-SIGNOFF.md`). Parked (`_FUTURE-STATE`): broader colour/theming, Apollo Labs tuners, bulk
type-binding, `icon-015` mark-vs-roundel mechanisation (supercharge).

> **COMMIT STATE.** Morning commits (`1a5bc94` · `1bb09f9` · capture `b9aef79`) are **PUSHED** (verified level with
> origin at this session's open). This session adds ONE capture commit (new files: ADR-0012 + seed + generator +
> sheet pair + dossier + these spine refreshes) — **ahead 1, Dave to push via GitHub Desktop.** Build green 37/37
> (graph generator deliberately NOT wired — Decision 8 on the sheet). **Next session model: Sonnet** (enactment is
> mechanical + generator-verified), opened AFTER Dave's sheet rulings; paste the sheet's export block into it.
