# Good morning, Dave ☕

*Briefing — refreshed 2026-07-20 ~18:35 BST (date from `date`), session
**"Style consolidation → four-theme token architecture"** — opened as good-morning, became the consolidation of
`snippets`/`_proforma`/`_review`/`_fitness-test` onto Apollo Mono. The pivot: **the token store had no theme
dimension**, so Legacy and Mono shared the same flat roles — that was the "too loose" root cause. Ruled **R-D19**
(red is themed), wrote **ADR-0011** (themes = override sets), built the **`_STYLE-PROVENANCE.md`** record, a visual
review screen, and an advisory **theme-provenance gate**. Committed `a1b9fbb`, build green 37/37.*

> ✅ **SOLO / self-conductor.** No other live session — single writer for shared state. **This session** found the
> missing theme layer, ruled red as Legacy-owned (Mono's only red = `#B92F1E`, status/RAG/dataviz), mechanised the
> four themes as semantic-tier override sets (Console/Supercharge = nullable slots), and stood up the record + gate
> that make "align to Mono" enforceable rather than a manual chase. Also built the per-cluster **visual review
> screen** (Dave: "duplicate patterns I need to compare visually") + review overlay. Narrative arc:
> `_DECISION-HISTORY/2026-07-20-style-consolidation-four-themes.md`. See COMMIT STATE.

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME THIS CHAT → `Four-theme token architecture (ADR-0011) + red=Legacy (R-D19) + style-provenance record & gate`**
> *(Opened as good-morning; became a consolidation of `snippets`/`_proforma`/`_review`/`_fitness-test` onto Apollo
> Mono. Root cause of the "too loose" drift: **the token store had no theme dimension** — Legacy red/teal/grey and
> Mono shared the same flat roles. Ruled **R-D19** [red is themed: Legacy `#DB0011`/`#A8000B` = Legacy only; Mono's
> one red `#B92F1E` = status/RAG/dataviz only]. Wrote **ADR-0011** [themes = semantic-tier override sets; Mono base,
> Legacy override, Console/Supercharge nullable slots]. Built the record `_STYLE-PROVENANCE.md`, the v2 visual review
> screen [+ overlay], and an **advisory** theme-provenance gate [68 hardcoded foreign hexes / 61 Mono files].
> Commit `a1b9fbb`, build green 37/37.)*

> **TITLE THIS CHAT →** `Pre-flight for Mono sweep — record de-risked, worklist pinned (§A-AUTH), sweep handed to fresh Sonnet session`
> **TITLE THE NEXT (fresh) CHAT →** `Mono alignment sweep — teal→green (Masthead + T2–9), grey inks, regen _review; red held for a tuner`
> **✅ STYLE-CONSOLIDATION RULINGS COMPLETE (committed `4e5b1b6`).** All 88 components ruled; authoritative align list is
> now **`knowledge/_STYLE-PROVENANCE.md` §A-AUTH** (the mid-doc "backlog A" was stale — superseded this session).
> Machine source of truth: `reviews/gen_style_consolidation_review.py` (`SINGLETON_RULINGS` + clusters) →
> `reviews/_style-consolidation-decisions-2026-07-20.json`. Tally: keep 7 · **align 39** · experiment 2 · legacy-ref 1 · archive 32 · 7 dupes hidden.
>
> **★ START HERE next session (Sonnet, cold) — read `_STYLE-PROVENANCE.md` §A-AUTH first, it's turnkey:**
> **(a) teal→green** — Masthead + `Tranche-2…9` (T1 has none): `#00847F` success → Mono `rag/success-glyph #4A9568`
> (dark ground), **prefer tokenising over a hardcode**. ⚠️ **OPEN sub-decision, don't blind-swap:** the `#i-success`
> SVG is a filled circle with a WHITE tick — under **type26-013** it likely becomes BLACK (cf. `on-success`=black);
> rule it (a one-control tuner) before touching the tick. **(b) grey inks** (`Avatar`,`Quick-actions`)→`color/mono/*`
> **via the grey-tint check** (surface the numbers to Dave BEFORE swapping — never auto-swap). **(c) regenerate**
> `_review` copies via `_make_review.py`. **HELD for a tuner (all red):** bare `rag/error` (R-D17), plus the two owed
> Mono values `tabs/active` + `progress/complete` (R-D19). Only after red is ruled → flip
> `_validate_theme_provenance.py` to **blocking**. **DO NOT ALIGN** the 5 archived files (Hero, Navigations,
> Progress-tracker, Tab-bar, Tabs, +`_proforma/Icon-button`); **DO NOT CONVERT** Notifications (its `#A8000B` is
> correct Legacy red). Then the **duplicate-dedup pass** Dave flagged.

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

# §B · THIS SESSION (2026-07-20, "Style consolidation → four-theme token architecture")

*Full narrative arc (why/how, the mid-turn corrections): `_DECISION-HISTORY/2026-07-20-style-consolidation-four-themes.md`.*

## What LANDED (commit `a1b9fbb`, build green 37/37)
- **✅ ADR-0011 — the four themes are now an ARCHITECTURE, not just intent.** Themes = **override sets at the semantic
  tier**: Apollo Mono = base · Apollo Legacy = populated override (reds/teal/grey ramp) · Apollo Console + Supercharge =
  **declared nullable slots** (ADR-0010 pattern). Registry `tokens/themes/_themes.json` = single source of truth for
  hex→theme ownership. **Root cause it fixes:** the semantic store had NO theme dimension (only light/dark), so Legacy
  red + Mono lived in the same flat roles — the "too loose" cause.
- **✅ R-D19 — red is THEMED.** Legacy red `#DB0011`/`#A8000B` = Apollo **Legacy only** (CTA, `tabs/active`,
  `progress/complete`, Legacy error). Apollo **Mono's only red = `#B92F1E`**, status/RAG/dataviz **only**, never
  action/nav. Any Legacy red in a Mono surface = **drift** (a definition, not a judgement). Source: Dave.
- **✅ THE RECORD — `knowledge/_STYLE-PROVENANCE.md`** (Dave: "clear record … too loose"). Classifies every artefact by
  theme-era; scopes library (align) vs `_fitness-test` (exploration=mine · research=preserve · **SME journeys=ignore**).
  Machine mirror `reviews/_style-clusters.json`.
- **✅ VISUAL REVIEW SCREEN — `reviews/STYLE-CONSOLIDATION-REVIEW-2026-07-20-v2.html`** (+ overlay copy
  `…-v2.REVIEW.html`). Per-cluster picker, wrapping grid (no h-scroll), Open↗/⤢-fullscreen per variant, old
  exploration beside canon. (v1 COMPARE = first cut, superseded — was a horizontal strip Dave rejected.)
- **✅ ADVISORY GATE — `_validate_theme_provenance.py`** (wired into `_build_all.py`). Flags **hardcoded** foreign-theme
  hexes in Mono surfaces — the blind spot the token leak gate can't see. First run: **68 across 61 files** →
  `_THEME-PROVENANCE-GATE.md`. Advisory now; **blocking after migration** (ADR-0011).

## What I got wrong (see the dossier)
Offered shallow itinerary picks at the open ("dig deeper"). Over-corrected `_fitness-test` to "all test pages" — Dave:
"there's good work in there" (it's exploration + research + journeys, not one bin). Shipped v1 as a horizontal-scroll
strip before Dave asked for a real review screen. And the raw drift scan over-reported twice (counted comment/manifest
hexes + the *ruled* Mono red) — fixed by stripping comments + excluding ruled colours before judging ([[attribute-the-diff]]).

---

# §C · QUEUE

## 1. ★ RULE THE CLUSTERS + the two owed Mono values (start here)
Open the review screen (overlay) `reviews/STYLE-CONSOLIDATION-REVIEW-2026-07-20-v2.REVIEW.html` and rule each duplicate
cluster keep/migrate/archive. Then the **two rulings owed** so the gate can go blocking: **Mono values for
`tabs/active` + `progress/complete`** — both only ever held Legacy red, and Mono ≠ red (R-D19), so each needs its own
value (ink indicator? green?) before its Legacy red can be seeded. **Opus** (token-precise). Full context:
`knowledge/_STYLE-PROVENANCE.md` §backlog.

## 2. Mono-alignment sweep (Sonnet, against ADR-0011)
Re-home the drift: **19 snippets** (mostly bare `rag/error` red + a few grey inks) + **12 proforma tranches**
(pre-R-D18 teal + Legacy red) onto Mono values; then **regenerate the `_review` copies** (`_make_review.py`) since
they're derivative. Then flip `_validate_theme_provenance.py` to **blocking**. Ties to §3 (RAG roles).

## 3. RAG error/warning/info roles — still Legacy-drifted (R-D17, unchanged)
Bare `rag/error` (`#A8000B`/`#DB0011`), `rag/warning` (`#FFBB33`), `rag/information` (navy) still resolve Legacy; R-D14
values live in their `-background`/`-glyph` tokens. Rule the sets on a tuner → rebind → these become Mono overrides.
**Needed before Alert / Banner / Toast.** This is the same work as §2's snippet red.

## 4. Parked / carry-forward
Console + Supercharge override sets (fill their null slots when palettes ruled). **T9 secure entry** awaits review.
**Sutherland field test** (ADR-0008 #1). **`designer-skills-v1`** revisit. Full-review backlog (`_REVIEW-SIGNOFF.md`).
Parked (`_FUTURE-STATE`): broader colour/theming, Apollo Labs tuners, bulk type-binding.

> **COMMIT STATE.** **✅ `a1b9fbb`** (four-theme architecture + R-D19 + record + review + advisory gate, 13 files, build
> green 37/37). **NOT yet pushed — Dave pushes via GitHub Desktop.** A capture-ritual follow-up commit (this handoff +
> dossier + `_LIVE-STATE` refresh line + the v2.REVIEW overlay copy) is the second small commit — **fold both into one
> push.** **Next session model: Opus** for the two Mono-value rulings; the alignment sweep (§2) is Sonnet.
