# Good morning, Dave ☕

*Briefing — written 2026-07-19 19:46 (date from `date`), session
**"Apollo Mono: the money atom, digital-black as the new #000, and the greys ruled onto the ramp"** — built the
first P1 money-format atom, ruled digital-black the GENERAL new `#000` (swept all 38 components), and turned the
whole semantic-grey set into rulings (R-D16) against the new Mono ramp.*

> ✅ **CONDUCTOR (continued).** The same-day PRIOR strand is already committed + pushed (RAG fills promoted,
> four-theme **R-D15**, the `color/mono/1–15` grey ramp — see §A). **This session** then added the
> **`Amount-display`** P1 atom + figure rungs `.t-cm-figure-4/5/6`, the **digital-black `#1A1A1A` library sweep**
> (all 38 components' dark grounds — committed), and **R-D16** (every semantic grey ruled onto the Mono ramp —
> RULED, enactment PENDING). It also **caught + fixed a STAND-002 red build** the prior GOOD-MORNING rewrite had
> committed (it dropped the standing-docs reachability list). This chat's own commit = R-D16 + the grey review
> sheet + these handoff updates — see COMMIT STATE.

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME THIS CHAT → `Apollo Mono: the money atom, digital-black as the new #000, and the greys ruled onto the ramp`**
> *(opened as a components worker, promoted to conductor mid-session; built Amount-display + figure rungs, ruled
> digital-black the general new #000 and swept 38 components, surfaced all 79 semantic greys and Dave ruled them
> onto the mono ramp as R-D16, then caught a STAND-002 red build in the capture ritual.)*

> **TITLE TODAY'S CHAT →** `Enact the Mono grey wiring (R-D16), then OTP/PIN`
> Everything for R-D16 is ruled and recorded — this is pure enactment: write the Mono grey values into
> `semantic-colour.json`, **sync the 38 component declarations** to the tokens (like the `#1A1A1A` ground sweep),
> regenerate `canon.css`, re-gate; annotate `col25-011` with the Mono override. Then the next P1 atom, **OTP/PIN**.
> **Sonnet** — enactment, not ruling.

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
`AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
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

# §B · THIS SESSION (2026-07-19, "Apollo Mono: the money atom, digital-black as the new #000, and the greys ruled onto the ramp")

## What LANDED (this session)
- **✅ `Amount-display` — first P1 money atom, BUILT + gated.** Money-format primitive (currency-before-no-space
  copy-025, tabular figures, U+2212 sign, redacted state); snippet + meta + review; monochrome (colour deferred).
  Added figure rungs **`.t-cm-figure-4/5/6`** (32/16/14, tabular); atom fully composite-bound (no raw font). COMMITTED.
- **★ "Digital black `#1A1A1A` is the new `#000`" (Dave) — GENERAL, not just reverse-text.** Swept all 38 components'
  dark grounds + `background/default` dark → `#1A1A1A` (shadows/overlays stay pure `#000`). COMMITTED. `#1A1A1A`=`mono/4`.
- **★ R-D16 — every semantic grey RULED onto `color/mono/*`** (sheet `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1`):
  text ink→`mono/4 #1A1A1A` (**SUPERSEDES `col25-011`** for Mono; Grey-8=Legacy) · **DROP** secondary text grey
  (hierarchy=weight/size) · `#767676`→`mono/8` · tinted `#D7D8D6`→`mono/12` · mechanical maps approved. **RULED,
  enactment PENDING (Sonnet — §C1).** CONSULT surfaced col25-011 (didn't retread the binned-sheet mistake).
- **✅ STAND-002 red build CAUGHT + FIXED.** The prior GOOD-MORNING rewrite dropped the standing-docs reachability
  list → 5 docs orphaned → build committed red. Restored the list in §A; build green. The gate did its job.
- Dossier: `_DECISION-HISTORY/2026-07-19-amount-display-and-mono-greys.md` (the why/how).

## Same-day PRIOR strand (already committed + pushed — context)
- **✅ RAG fills PROMOTED** to `semantic-colour.json` `*-background` + `canon.css`: light `#5DAC7B`/`#7DABCD`,
  dark `#43AD6F`/`#5F92B9`, breach `#B92F1E` mode-stable, watch `#F0B13A`. `rag/text` polarity enacted via the
  existing `RULED_PAIR_EXCLUSIONS` (white×green/blue forbidden, like amber). **Components NOT rebound** — they
  render RAG as dots (glyphs, R-D6 fine) + chips (tints); `-background` fills await the §1 manifestation pick.
- **★ FOUR-THEME ARCHITECTURE inscribed — R-D15.** One token store, one baseline library, 4 themes
  (Legacy/Mono/Console/Supercharge). Baseline = **Apollo Mono, "very mono"** (colour only in RAG + data-vis).
  Legacy carries teals + brand `grey/100–800`. Closed a memory-only-inscription gap (memory had R-D15, ledger
  didn't). Ledger `_proforma/_RAG-DECISIONS.md`; memory `four-theme-architecture`.
- **★ Apollo Mono grey ramp = `color/mono/1…15`.** Dual-end brightness curve (γ=1.7, 15 stable index steps),
  packing resolution to both ends, thinning mid-greys; `#1A1A1A` = `mono/4`. Dave dialled it live on the tuner
  `reviews/APOLLO-MONO-GREY-CURVE-2026-07-19-v2.html`. In `colour.json` + canon; build green.
- **✅ `gen_rules_index` truncation FIXED** (the `chunk[:500]` cap) — full rule text now flows to
  `_RECONCILIATION.md` + `_consult.py` (icon-015 was losing ~2300 chars). Worker-verified.
- **Grey-tint standing check** banked (memory `feedback-grey-tint-check`).

## What I got wrong / watch
- **Retread a settled ruling.** Built a whole review sheet to "decide" the RAG text/glyph model — but R-D6 +
  `type26-013` + R-D12 B already governed it. Skipped CONSULT. Dave: *"the decision is made already… read
  deeper, i don't want to retread old footsteps."* Sheet binned (`_to_delete/binned-review-docs/`). **Lesson:
  CONSULT first, every time.**
- **Over-checkpointed early**, then course-corrected. Dave wants momentum; reflect-back should be tight.

## Merged from the two workers (receipts in `notes/_receipts/`)
- **rules-index worker:** the truncation fix (verified) + hardened `_RUNBOOK-git-commit.md` (step 0.5) &
  `_RUNBOOK-parallel-conductor.md` (step 2.5) with the `notes/_receipts/` convention + `_HOW-TO-RUN-SESSIONS.md`.
- **components-expansion worker:** rebound **all 38 components' dark grounds to `#1A1A1A`**, added money number
  styles (14/16), and built the new **`Amount-display`** component (meta + snippet + review). Build green.
  **★ Large change — eyeball the diff before pushing** (worker flagged it "to review when fresh").

---

# §C · QUEUE

## 1. ★ ENACT R-D16 — the Mono greys onto the ramp (Sonnet, next real deliverable — RULED, just execute)
The rulings are made (**R-D16**, ledger `_proforma/_RAG-DECISIONS.md`); this is pure enactment. Steps:
(1) write the Mono grey values into `tokens/semantic-colour.json` — text ink `#1A1A1A`, **drop** secondary
(collapse to ink), `#767676`→`#808080`, `#D7D8D6`→`#E1E1E1`, mechanical maps (`#1D1D1D`→`#1A1A1A`, `#EDEDED`→`#F0F0F0`,
`#707070`→`#626262`, `#404040`→`#484848`, `#9B9B9B`→`#9D9D9D`, …); (2) **sync the 38 component declarations to the
tokens** (same shape as the `#1A1A1A` ground sweep — change the declared hex, or the gate drifts); (3) regen
`canon.css`; (4) re-gate. (5) **Propagation owed:** annotate `col25-011` / `guidelines/colour-usage.md` with the
Mono override (text = `#1A1A1A`; Grey-8 = Legacy). ⚠️ Dropping secondary makes muted text full-ink — a visible
change; that's the ruling. Sheet + `reviews/gen_mono_grey_sheet.py` carry the full table.

## 2. §1 RAG manifestation pick, then the status-component build (Sonnet)
Decision sheet built earlier (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`): dot+label (canon) · filled
cell/badge · bar. Awaiting Dave's pick. Only the filled-cell manifestation consumes the new `-background` fills;
that's when the component rebind happens. Then spec cell/bar as gated components (cells need more vertical
padding, R-D11 note).

## 3. Gates owed
- **Amber rules gate** (rules 1+2 still unenforced). · **Component RAG rebind** behind the blast-radius gate
  (waits on the manifestation pick).

## 4. Parked (`_FUTURE-STATE`)
Broader colour/theming build (Console + Supercharge palettes; the 4-theme toggle machinery) — "deal with colours
later." · **Apollo Labs** (the grey-ramp + OKLCh tuners → Layer-2 in-browser controls). · Bulk type-binding for
~338 elements · compliance edges (27 unverified `verified_by`, advisory) · 🕓 Latin webfont (waiting on brand).

## 5. After R-D16 — the next P1 atom
**OTP/PIN entry** is next on the P1 foundations list (the banking-auth atom generic systems lack). The
38-component `#1A1A1A` ground sweep is already committed + pushed; a fresh-eyes glance at it in the diff is still
worth it.

> **COMMIT STATE — this chat's commit.** *(The prior 3-strand conductor commit — RAG fills, R-D15, mono ramp,
> Amount-display, the 38-component `#1A1A1A` sweep — is ALREADY committed + pushed.)* **This commit (docs +
> review only, NO gated-code change — build GREEN 34/34):** `_proforma/_RAG-DECISIONS.md` (R-D16),
> `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1.html` + `.REVIEW.html` + `reviews/gen_mono_grey_sheet.py`,
> `_DECISION-HISTORY/2026-07-19-amount-display-and-mono-greys.md`, `_LIVE-STATE.md`, `GOOD-MORNING.md` (incl. the
> **STAND-002 FIX** — restored the standing-docs reachability list the prior rewrite dropped). No token/snippet
> edits here — R-D16 is ruled, not yet enacted. **You push via GitHub Desktop.**
> **Next session model: Sonnet** (enact R-D16, then OTP/PIN).
