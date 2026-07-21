# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-21 (good-morning): RAG sets COMPLETE (R-D20) + glyph rule sharpened (R-D6 A′) + the decision-graph tasked to Fable. READ THIS FIRST — it supersedes the block + names below.
> **RENAME THIS CHAT →** `RAG error/warning/info completed (R-D20, 1a5bc94) + R-D6 A′ glyph-contrast sharpening (1bb09f9) + decision-graph audit tasked to Fable`
> **TITLE THE NEXT (fresh) CHAT →** `Decision-graph: audit the record corpus → author the typed-edge convention (ADR-0007's unbuilt half) → generator + conflict gate [FABLE, cold]`
>
> **★ NEXT SESSION = FABLE, cold.** The decision-graph edge convention (ADR-0007's unbuilt generator half). Brief is
> in `_FUTURE-STATE.md` (★ Decision-graph section) + `_DECISION-HISTORY/2026-07-21-rag-completion-and-decision-graph.md`
> (thread 3). Shape: audit the ~35 decision nodes (4 ledgers + 11 ADRs + REVIEW rules) whose cross-refs are prose →
> author typed edges (`refines · supersedes · subsumes · bounds · conflicts-with · verified-by` + status + validation)
> → build the generator (LIVE/DEAD/OPEN + reconciliation view + "what-touches-this" map) + a **conflict gate**. **Two
> guardrails:** genuine conflicts the audit surfaces are **queued for Dave, never auto-resolved** (promotion is Dave's,
> routing rule 2); open sub-call — Fable authors all edges vs stops at spec+gate and hands edge-authoring to Sonnet —
> **decided after the audit**. Why Fable: big/high-stakes/hands-off, wrong taxonomy = corpus-wide rot. Why now: today's
> icon-011↔R-D6↔R-D3 reconciliation was hand archaeology — the pain that justifies the build.
>
> **What landed today (2 commits, ahead 2, Dave to push via GitHub Desktop; build green 37/37):**
> - **R-D20 (`1a5bc94`)** — error/warning/information sets completed, the R-D18 success move for the last three. Dave
>   ruled the message tints on a cloned live tuner: error `#F1E0DC`/`#2C120D` · warning `#F6E5CC`/`#3C2C13` (lifted the
>   dark to stay amber, not brown) · info `#D6E3EC`/`#092131`. Bare roles rebased off Legacy → track the glyph.
>   **6 Mono snippets swept**; **Notifications NOT converted** (Legacy ref, §A-AUTH — `driftAllow`-waived). Unblocks
>   Alert/Banner/Toast. Signal colours were already ruled and were NOT re-decided.
> - **R-D6 A′ (`1bb09f9`)** — Dave sharpened glyph-contrast: the only coloured icons are RAG statuses, each labelled or
>   black/white-marked → colour is never the sole channel → **no status glyph is held to 4.5**; the 3:1 floor governs.
>   4.5's live domain = the meaning-exclusive glyph (arrow-as-datum). Bounds `{#icon-011}`; subsumes the R-D3 amber
>   exemption. Reconciled corpus-wide.
>
> **Still open (NOT this session's next):** theme-provenance gate stays **advisory** (58 foreign hexes / 67 files —
> parked archived-file cleanup); `tabs/active` + `progress/complete` unruled (archived consumers); Notifications
> Legacy-theme retag (future build). **Spine flag (small, separate):** `text/on-success` = `color/black` should be
> `color/mono/4` (`#1A1A1A`) digital black.

---

*Briefing — refreshed 2026-07-21 ~15:20 BST (date from `date`), session
**"RAG completion (R-D20) + glyph-contrast sharpening (R-D6 A′) + decision-graph tasked to Fable"** — opened as a
good-morning; ran the RAG-completion tuner (Dave ruled the three message tints), then Dave sharpened the glyph
rule, then desk research on the record structure itself. **SOLO / self-conductor.** All names + the full landed
list are in the ★ LATEST block above — that block is authoritative; the sections below are the standing
orientation (§A) + this-session detail (§B) + queue (§C).*

## ⬛ DO THIS FIRST

> The two names are at the top (★ LATEST). **Next session opens on FABLE, cold** — the decision-graph edge
> convention. Everything a cold reader needs to start it is in `_FUTURE-STATE.md` (★ Decision-graph) +
> `_DECISION-HISTORY/2026-07-21-rag-completion-and-decision-graph.md` (thread 3). Don't start it inside a loaded
> session — it's a fresh-context audit (routing rule 6).

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
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D16) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D19; R-D19 = red is themed) · `knowledge/_STYLE-PROVENANCE.md` (theme-era record) · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
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

# §B · THIS SESSION (2026-07-21, good-morning — "RAG completion + glyph sharpening + the decision-graph question")

*Full narrative arc (why/how, all three threads): `_DECISION-HISTORY/2026-07-21-rag-completion-and-decision-graph.md`.*

## What LANDED (commits `1a5bc94` + `1bb09f9`, build green 37/37, ahead 2 — Dave to push)
Opened as a good-morning; Dave green-lit the queued RAG-completion tuner, then two follow-on questions turned it into
three threads.
- **✅ R-D20 — error/warning/information sets completed** (the R-D18 success move for the last three). CONSULT +
  token survey first; cloned the success tuner to three sets (glyph + fill locked, only the message **tint** open).
  Dave ruled the tints on the live controller: error `#F1E0DC`/`#2C120D` · warning `#F6E5CC`/`#3C2C13` (lifted the
  dark seed to keep it **amber, not brown** — the one judgement the tuner surfaced) · info `#D6E3EC`/`#092131`. Bare
  roles rebased off Legacy → track the glyph; `$alias` dropped on the tints. **6 Mono snippets swept**; **Notifications
  NOT converted** — it's a Legacy reference (§A-AUTH), so its RAG vars are `driftAllow`-waived, not swept. Unblocks
  Alert/Banner/Toast.
- **✅ R-D6 A′ — glyph-contrast sharpening.** Dave's instinct was right (it's R-D6 Ruling A verbatim): the only
  coloured icons are RAG statuses, each labelled or black/white-marked, so colour is never the sole channel → no
  status glyph is held to 4.5; the 3:1 floor governs. 4.5's live domain = the meaning-exclusive glyph. Bounded
  `{#icon-011}`, subsumed the R-D3 amber roundel-leg exemption, reconciled corpus-wide (also folded into `{#icon-015}`
  so `_RECONCILIATION.md` regenerates it).
- **✅ Decision-graph desk research → tasked to Fable.** The manual icon-011↔R-D6↔R-D3 reconciliation exposed that
  records cross-reference in prose. Research confirmed ADR-0007 already decided the fix (temporal decision-graph);
  the unbuilt half = the typed-edge convention + generator + conflict gate. Rejected replicate (rot) + graph-DB
  (tool-temptation). Pinned as the next (Fable, cold) session — see ★ LATEST + `_FUTURE-STATE.md`.

## Process notes
Both runbooks (`_RUNBOOK-git-commit.md`, this capture ritual) run by the book — no reconstructing from hooks. One small
catch: tried to hand-edit the **generated** `_RECONCILIATION.md`; the rebuild wiped it — correct mechanism is to edit the
REVIEW-tagged rule and let it regenerate.

---

# §C · QUEUE

## 1. ★ NEXT (FABLE, cold) — the decision-graph edge convention (ADR-0007's unbuilt half)
Audit the ~35 decision nodes (4 ledgers + 11 ADRs + REVIEW rules) whose cross-refs are prose → author typed edges
(`refines · supersedes · subsumes · bounds · conflicts-with · verified-by` + `status` + `validation`) → build the
generator (LIVE/DEAD/OPEN + **reconciliation view** + "what-touches-this" map) + a **conflict gate**. **Guardrails:**
conflicts the audit surfaces are **queued for Dave, never auto-resolved** (routing rule 2); open sub-call — Fable
authors all edges vs stops at spec+gate and hands edge-authoring to Sonnet — **decided after the audit**. Turnkey brief:
`_FUTURE-STATE.md` (★ Decision-graph) + dossier thread 3 + `docs/decisions/ADR-0007` + `notes/_STATE-MACHINE-TARGET.md`.

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

> **COMMIT STATE.** **HEAD `1bb09f9` — ahead 2, Dave to push via GitHub Desktop** (+ this capture commit, which will be
> ahead 3). Today: `1a5bc94` (R-D20 — tokens + 6 snippets swept + Notifications waived) · `1bb09f9` (R-D6 A′ — glyph
> rule + reconciliation). Build green 37/37; `_LIVE-STATE-CHECK.md` 2 pre-existing info notes (not blocking). **Next
> session model: FABLE, cold** — the decision-graph audit is big/high-stakes/hands-off (routing rule 6: judgment/audit
> runs cold + on the decide tier; here the decide tier is Fable, not Opus, per Dave). Set Fable to its **highest
> reasoning level** — this is an architecture + corpus-audit job where depth pays.
