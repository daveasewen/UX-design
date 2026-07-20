# Good morning, Dave ☕

*Briefing — refreshed 2026-07-20 evening (date from `date`), session
**"Mono primary-action token + ADR-0009 state-styling (live-editor loop)"** — opened to clear token debt so
Dave could build more components; the owed **mono primary-action ruling** grew into a full **state-styling
architecture** (ADR-0009) via a fast live-editor loop (v1→v7). Primary ladder minted + settled, two bugs
fixed, all committed (`b895c40`), build green 35/35.*

> ✅ **SOLO / self-conductor.** No other live session — single writer for shared state. **This session**
> minted the Mono **primary-action** token ladder (closes the owed ruling), formalised **ADR-0009** (colour =
> universal per-state substrate · opacity = optional operational layer · mechanism a per-state set
> {colour|opacity|both} · chromatic modes are override sets), fixed the **invisible disabled label** + **3
> Legacy border greys**, and promoted **live-controls-in-reviews** to a standing principle. Narrative arc in
> `_DECISION-HISTORY/2026-07-20-mono-primary-state-styling.md`. See COMMIT STATE.

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME THIS CHAT → `Mono primary-action token + ADR-0009 state-styling (live-editor loop)`**
> *(minted `button/primary/*` — completes the button ladder, monochrome NO red [B-D1]; settled on the v7 live
> editor: default #1A1A1A/#FAFAFA · hover opacity 0.70 (colour-equiv #626262/#B7B7B7) · pressed #000000/#FFFFFF ·
> disabled label #9D9D9D/#808080. Wrote **ADR-0009 state-styling**; fixed the invisible disabled label + 3 Legacy
> border greys; promoted **live-controls-in-reviews** to a principle. Commit `b895c40`, build green 35/35.)*

> **TITLE TODAY'S CHAT →** `button/* snippet rebind (render Mono red-free + opacity hover) — then carry on the component build-out`
> Pick the next real deliverable from the now-current §C queue. **Strongest = the `button/*` snippet rebind**
> (queue #1): the tokens are minted but the *rendered* Mono button still shows **red primary** and hover isn't
> operationally opacity yet — this is the blocker to clear before building more components on the primary. Then
> the wider **component build-out** Dave came in for. Also live: **T9 secure-entry review**, the parked **Sutherland
> field test** (repo not yet available) + **designer-skills-v1** revisit. **Opus** for the rebind; build-out varies.

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
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…B-D5; Mono primary + state-styling, ADR-0009) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` ·
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

# §B · THIS SESSION (2026-07-20 evening, "Mono primary-action token + ADR-0009 state-styling")

## What LANDED (committed `b895c40`, build green 35/35)
- **✅ Mono PRIMARY-ACTION ruling CLOSED — `button/primary/*` minted, completing the button ladder.** Component →
  semantic (`surface/action-primary{,-hover,-pressed}`, `icon/on-inverse`, `text/on-disabled`) → `color/mono/*`.
  **Monochrome — NO red** (B-D1: red is *out of bounds* for Mono, not just Legacy-only). Settled values (Dave, on
  the v7 live editor): default `#1A1A1A`/`#FAFAFA` · hover **opacity 0.70** + colour-equiv `#626262`/`#B7B7B7` ·
  pressed `#000000`/`#FFFFFF` · disabled fill `#E1E1E1`/`#484848`, label `#9D9D9D`/`#808080`. Ledger:
  **`knowledge/_proforma/_BUTTON-DECISIONS.md`** (B-D1…B-D5, in the STAND-002 list).
- **✅ ADR-0009 — state-styling architecture.** Colour token = universal per-state substrate (chromatic modes =
  override sets); opacity = optional operational layer; **mechanism a per-state set `{colour|opacity|both}`**;
  colour-alone first-class; AA invariant. Wired **non-breaking** via `$extensions.apollo.state` on the hover token.
- **✅ Two bugs fixed.** (a) **invisible disabled label** (`text/disabled` `#E1E1E1` == the disabled ground) →
  minted `text/on-disabled` visible ghost, **exempt but never invisible** (B-D4). (b) **3 dark border greys** off
  the Legacy primitive → `color/mono/8` (`border/strong`, `form/border/{default,pressed}`). Legacy alias advisories
  now **1** (was 4; the remaining `primary/border/hover` dark = Legacy red, intentionally left).
- **✅ Principle: live-controls-in-reviews** — every review carries a *decision control per open choice*; Dave edits
  in place, not an AskUserQuestion round-trip. In `_FUTURE-STATE` + memory; the v7 editor is the reference impl.
  **Style-builder interface** added to `_FUTURE-STATE` (harness-side home of ADR-0009).

## What I got wrong (see the dossier)
Matched the sibling buttons on disabled and imported their **invisible-label** bug; over-constrained the disabled
control with a hard 2:1 guard (Dave's exempt call — made it informational instead). Arc, dead-ends + corrections:
`_DECISION-HISTORY/2026-07-20-mono-primary-state-styling.md`.

---

# §C · QUEUE

## 1. ★ `button/*` SNIPPET REBIND — the blocker before more component work
Tokens are minted but the **rendered** Mono button still shows **red primary** and hover isn't operationally
opacity yet. Rebind the button snippet(s) off the legacy/red vars onto `button/{primary,secondary,tertiary,
quaternary}/*`, render hover as the **0.70 opacity** (per ADR-0009), and the disabled label via `text/on-disabled`.
Batched across all tiers (the secondary/tertiary/quaternary rebind was also deferred — `notes/_receipts/2026-07-20-worker-button-3tier.md`).
**Do this before building more components on the primary.** **Opus.**

## 2. Component build-out (what Dave came in for)
After the rebind, continue growing the library. Also flagged: the **other button tiers likely share the
invisible-disabled-label defect** (`button/{secondary,tertiary,quaternary}/label/disabled` → `text/disabled`) — fold
the `text/on-disabled` fix across them in the same pass.

## 3. Deferred token work
Opacity → a **first-class number/opacity token** (currently `$extensions.apollo.state`) with the style-builder.
Rest of the store still 2-tier (deferred migration). The style-builder interface itself (`_FUTURE-STATE`).

## 4. Parked / carry-forward
**T9 secure entry awaits Dave review.** **Sutherland field test** (ADR-0008 case #1) — repo not yet available.
**`designer-skills-v1`** revisit (no-Python assumption overturned). Full-review backlog (`_REVIEW-SIGNOFF.md`).
Parked (`_FUTURE-STATE`): broader colour/theming, Apollo Labs tuners, bulk type-binding, compliance edges, Latin webfont.

> **COMMIT STATE.** **✅ committed `b895c40`** (35 files: `semantic-colour.json`, `_contrast_utils.py`,
> `_validate_token_tiers.py`, `ADR-0009`, `_BUTTON-DECISIONS.md`, `_FUTURE-STATE`, `GOOD-MORNING`, the v1–v7 editor
> sheets + regenerated build artifacts). Build GREEN 35/35, tier gate 0 strict. **NOT yet pushed — Dave pushes via
> GitHub Desktop.** A capture-ritual follow-up commit (this handoff refresh + `_LIVE-STATE` + the dossier) will be a
> second small commit — fold both into one push.
> **Next session model: Opus** for the snippet rebind; component build-out varies by task.
