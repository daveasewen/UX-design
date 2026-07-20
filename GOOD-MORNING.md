# Good morning, Dave ☕

*Briefing — refreshed 2026-07-20 (date from `date`), session
**"Canonical-core ADR + doc/memory housekeeping"** — the record itself was overdue: this file had gone TWO
sessions stale (still listed T9 / tokenize as "do first" when both had long landed). This session cleaned that
up, drafted the **ADR-0008 canonical-core/adapter strategy** Dave had approved but that ran out of context to
write, and compacted the memory index.*

> ✅ **SOLO / self-conductor.** No other live session this round — single writer for shared state. The two
> strands that landed BEFORE this session (both committed + pushed): the **button ladder as a 3-tier token
> stack** (`button/{secondary,tertiary,quaternary}` → `surface/action*` → `color/mono/*`, commit `ded4900`)
> and the **★ canonical-core STRATEGY LOCK** (Apollo = canonical source, consumers via automated adapters —
> commit `200c2ec` carried the first-principle note). **This session** turned that strategy into the formal
> **ADR-0008**, refreshed this handoff + `_LIVE-STATE`, and ran the memory compaction that was flagged DUE.
> See COMMIT STATE.

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME THIS CHAT → `Canonical-core ADR-0008, GOOD-MORNING un-stale, memory compacted`**
> *(read good-morning solo; drafted **`docs/decisions/ADR-0008-canonical-core-and-adapters.md`** — Apollo =
> canonical source, consumers via automated adapters, "diverge for quality, keep every divergence machine-mappable",
> the button ladder as its reference divergence; refreshed this handoff + `_LIVE-STATE`; compacted the ~20KB memory
> index. Housekeeping session — no gated-code change; build stays green.)*

> **TITLE TODAY'S CHAT →** `Sutherland field-test + designer-skills-v1 revisit; or the mono primary-action ruling`
> Pick the next real deliverable from the now-current §C queue. Strongest candidates: **(a)** the ground-truth
> Sutherland field test (run Apollo in VS Code beside the real Sutherland repo → build the real Apollo↔Sutherland
> map — case #1 for "serve any codebase", per ADR-0008); **(b)** revisit **`designer-skills-v1`** before it ships
> (it assumes no-Python; the strategy now says designers run the full architecture); **(c)** the owed **mono
> primary-action token ruling** (`action/primary/*`). **Opus** for (a)/(c); (b) is Sonnet-grade.

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

## ★ ONE token store · ONE baseline library · FOUR themes (R-D15, 2026-07-19 — firmed up this session)
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
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D16) · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
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

# §B · THIS SESSION (2026-07-20, "Canonical-core ADR + doc/memory housekeeping")

## What LANDED (this session — housekeeping, no gated-code change)
- **✅ ADR-0008 DRAFTED — `docs/decisions/ADR-0008-canonical-core-and-adapters.md`.** Turns Dave's 2026-07-20
  strategy lock into the formal anchor: **Apollo = canonical source** (well-formed superset, not a mirror of any
  consumer); **quality is the vote-winner, never inherit a flaw to match a consumer** (proof = the decoupled
  `button/*` tier instead of the overloaded `secondary`=checkbox token); **respect but don't follow** — consumers
  reached by an automated adapter layer (seed: `tokens/_manifests/sutherland-diffs.json` + hub-and-spoke
  `codeBindings`); operating principle **"diverge for quality, keep every divergence machine-mappable"**; designers
  run the **full architecture** (revisit `designer-skills-v1`). Extends ADR-0002/0005/0006.
- **✅ GOOD-MORNING un-staled.** It had gone two sessions stale (listed T9/tokenize as "do first" — both done).
  Refreshed to current truth; §A orientation + the STAND-002 standing-docs list left intact.
- **✅ Memory index compacted** — was flagged DUE (~20KB). (See COMMIT STATE for what moved.)

## For context — what landed in the TWO sessions just BEFORE this one (already pushed)
- **Button ladder → 3-tier tokens (commit `ded4900`).** `button/{secondary,tertiary,quaternary}` → `surface/action*`
  · `text/on-action` · `border/action-strong` → `color/mono/*`; tier gate enforces it. Secondary = grey filled
  per-mode (L `#626262`/white · D `#808080`/black, label flips by mode); red primary = **Legacy only**. The
  overloaded legacy `secondary/tertiary/primary` were left UNTOUCHED (they carry checked-state/surface roles).
- **Tranche-9 · Secure entry BUILT + gated** (OTP/PIN, password Show/Hide + strength, memorable-word, re-auth) and
  **T1–T8 all tokenised** (each carries a `#token-manifest`; `gen_snippet_tokens.py` projects all 9). **T9 NOT yet
  Dave-reviewed.** The visible focus-ring went blue on tokenisation (`focus/ring`) — flag if a mono ring is wanted.
- **Canonical-core strategy LOCKED (Dave 2026-07-20)** — now formalised as ADR-0008 above.

---

# §C · QUEUE

## 1. ★ Ground-truth Sutherland field test (ADR-0008 case #1)
Run Apollo in **VS Code + Copilot beside the real Sutherland repo** → read the actual components/tokens → build the
real Apollo↔Sutherland map, and field-test "serve any codebase" against it. Doubles as the first live-fire of the
designer pack. Seed already exists: `tokens/_manifests/sutherland-diffs.json` + hub-and-spoke `codeBindings`.

## 2. ★ Revisit `designer-skills-v1` before it ships
It was shaped around a **no-Python** assumption that ADR-0008 decision 5 overturns — designers run the full
architecture (gates + generators, in-editor), not a guidance-only cut. Reshape before release. **Sonnet-grade.**

## 3. ★ RULING owed — the mono PRIMARY-ACTION token
The near-black primary button has **no semantic token**; the worker verified `--pri-lbl`→`text/reverse` gives
1.0:1 in dark (primary ground inverts by mode). Fix = mint `action/primary/{background,background-hover,label}`
(+ an `icon/on-inverse`); `text/on-inverse` (#FFFFFF/#333333) is the ready label candidate. **Promotion is Dave's.**

## 4. Deferred store migration + latent bugs
The REST of the store is still 2-tier (components alias primitives) — migrate onto proper tiers deliberately
(elevation proved the pattern). `_validate_token_tiers` **advisory** lists **4 legacy alias bugs** to fix:
`border/strong`, `form/border/default`, `form/border/pressed` (dark) → alias should be `color/mono/8`;
`primary/border/hover` (dark). Also the legacy `secondary/tertiary` → `button/*` migration + snippet-button rebind
(the eventual adapter/cleanup — flagged in `notes/_receipts/2026-07-20-worker-button-3tier.md`).

## 5. Review backlog + carry-forward
**T9 secure entry awaits Dave review**; the button-ladder greys/tiers go on the full-review backlog
(`knowledge/_REVIEW-SIGNOFF.md`). Parked (`_FUTURE-STATE`): broader colour/theming, Apollo Labs tuners, bulk
type-binding, compliance edges, Latin webfont. Earlier open items: §1 RAG manifestation pick + status-component
build · amber rules gate · component RAG rebind (blast-radius).

> **COMMIT STATE.** Prior sessions' commits are already pushed (`ded4900` button ladder, `200c2ec` canonical-core
> first-principle note). **THIS session's wrap commit (docs/handoff only, build GREEN):**
> `docs/decisions/ADR-0008-canonical-core-and-adapters.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md` (+ memory files,
> outside the repo). No gated-code change. **You push via GitHub Desktop.**
> **Next session model: Opus** for the Sutherland field test / mono-primary ruling; the `designer-skills-v1`
> revisit can be Sonnet.
