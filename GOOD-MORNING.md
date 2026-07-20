# Good morning, Dave ☕

> ## ★ LATEST — 2026-07-20 (evening 5): the Mono teal→green sweep is DONE. READ THIS FIRST, it supersedes the block + the two names below.
> **RENAME THIS CHAT →** `Mono teal→green sweep DONE (Sonnet exec, Opus vouched) — proforma teal→0, committed d6e3d89; red tuner next`
> **NEXT (fresh) CHAT TITLE →** `Red tuner (Dave-in-the-loop) — rule Mono rag/error #B92F1E + tabs/active + progress/complete, then flip theme-provenance gate to blocking`
>
> The pre-flighted sweep executed cleanly in one pass — **Mode-2 delegation** (a Sonnet subagent ran the
> verified map; Opus verified the diff, re-ran the build, and vouched — routing rule 5). **Committed `d6e3d89`
> — ahead 1, Dave to push via GitHub Desktop.** Build green 37/37; theme-provenance teal `#00847F` in
> `_proforma`: **22 → 0**.
>
> **What changed (all in `knowledge/_proforma/`):** Change 1 — `--success`/`--success-t` vars on all 9
> (Masthead + Tranche-2…9): light `#2B7E4F`/`#DCEDE3`, dark `#4A9568`/`#12291D` (= `rag/success` + `-tint`,
> R-D18). Change 2 — `#i-success` badge on Tranche-2…5 only: hardcoded circle `#00847F` + white tick →
> tokenised `currentColor` circle + `style="fill:var(--mark)"` tick (the T6–9/Masthead pattern). Regenerated
> `_review` copies (3 updated + 6 created). **Reds / warning / info HELD** (untouched) — that's the red tuner.
>
> ★ **The open dark-`--success` sub-decision is CLOSED: green `#4A9568`** (small inline dot), NOT the white
> flip — verified against the aligned `snippets/Status-indicator`. The prior handoff's "tick → black under
> type26-013" worry does not bite this small dot (it uses `--mark=--page`); that's the big-roundel case.
>
> ★ **NEXT = the red tuner (§C·2, Dave-in-the-loop).** All red is held pending a live controller: bare
> `rag/error` (Mono `#B92F1E`) + owed Mono `tabs/active` + `progress/complete` (each needs a non-red Mono
> value). Only after red is ruled → flip `_validate_theme_provenance.py` to blocking. **Also still open (Sonnet-able,
> not blocked on Dave): the 27 drifting snippet aligns + grey inks — §C·1b.** Full arc: sweep map
> `_DECISION-HISTORY/2026-07-20-mono-sweep-map-and-bad-day.md`; state `_LIVE-STATE.md` LATEST DELTA (evening 5).
> **Spine flag (separate, for the token/red session):** `text/on-success` = `color/black` should be `color/mono/4`
> (`#1A1A1A`) digital black.

---

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

# §B · THIS SESSION (2026-07-20, evening 3 — "Pre-flight for the Mono alignment sweep")

*Full narrative arc (why/how, both procedure corrections): `_DECISION-HISTORY/2026-07-20-preflight-mono-sweep.md`.
The four-theme session that preceded this one: `_DECISION-HISTORY/2026-07-20-style-consolidation-four-themes.md`.*

## What LANDED (commits `6af6501` + `4d0716b`, build green 37/37, all pushed) — ZERO canon/token/component edits
Opened good-morning to run the sweep; Dave's steer ("be careful, I don't want to lose anything" + context discipline)
turned it into a pre-flight + record-repair. Deliberately no canon edits — the sweep goes to a fresh session.
- **✅ INTEGRITY — nothing lost.** All 88 round-1→3 consolidation rulings are durable (21 clustered in
  `reviews/_style-consolidation-decisions-2026-07-20.json`; 20 singletons in the generator's `SINGLETON_RULINGS`).
  Authoritative **align = 39** = 27 snippets + 1 `_review` (reconciled tab/stepper) + 11 `_proforma`.
- **✅ THE RECORD DE-RISKED — `knowledge/_STYLE-PROVENANCE.md` §A-AUTH.** The mid-doc pre-round-3 "backlog A" was
  STALE — it named Hero/Navigations/Progress-tracker/Tabs as align targets (round 3 **archived** all four) and listed
  Notifications (which is keep-legacy: its `#A8000B` is *correct* Legacy red). Marked it superseded (struck-through,
  kept for audit); wrote **§A-AUTH** = the authoritative 39-item align list + DO-NOT-ALIGN (5 archived) + DO-NOT-CONVERT
  (Notifications) + per-item drift type. Machine source of truth = the generator + JSON.
- **✅ STATE-MANAGER FIX — the freshness-drift check can read the stamp again** (`_build_live_state.py`, `4d0716b`).
  Its regex expected a bare date, but every `Last refreshed:` stamp is bolded (`**2026-07-20**`), so the drift-catcher
  had been silently blind for multiple sessions. One-line fix (`[^\d\n]*` before the date); verified it still fires on a
  genuinely stale stamp. `_LIVE-STATE-CHECK.md`: 1 warning → 0 (2 pre-existing info notes remain).

## What I got wrong (both caught by Dave — see the dossier)
Improvised git — and misdiagnosed the delete-guard's 0-byte `index.lock` as "GitHub Desktop is open" — instead of running
`_RUNBOOK-git-commit.md`; hand-rolled the handoff instead of running `_RUNBOOK-capture-ritual.md`. Same failure:
reconstructing a *procedure* from memory hooks — the "context rot" Dave flags. Corrected: re-read both runbooks and ran
them by the book. New memory `feedback-read-the-runbook` (read the runbook, not the hook).

---

# §C · QUEUE

## 1. Mono-alignment sweep — ✅ (a) proforma teal→green DONE (evening 5, `d6e3d89`); (b) grey inks + 27 snippet aligns REMAIN
**✅ (a) DONE this session** — proforma teal→green (Masthead + Tranche-2…9): `--success` light `#2B7E4F`/dark `#4A9568`,
tints `#DCEDE3`/`#12291D`; `#i-success` badge tokenised on T2–5; dark-`--success` sub-decision CLOSED = green `#4A9568`
(small dot, not the white flip); `_review` regenerated; teal in `_proforma` 22→0; build green 37/37. **STILL REMAINING
(Sonnet-able, not blocked on Dave):** the 27 drifting snippets + (b) grey inks. Original brief kept below for those:
The 88-component consolidation is RULED (align = 39) — clusters no longer need ruling. Remaining sweep items:
**(a) teal→green** — Masthead + `Tranche-2…9` (T1 has none): `#00847F` success → Mono `rag/success-glyph #4A9568`
(dark ground), **prefer tokenising over a hardcode**. ⚠️ **OPEN sub-decision, don't blind-swap:** the `#i-success` SVG
is a filled circle with a WHITE tick — under **type26-013** it likely becomes BLACK (cf. `on-success`=black); rule it
(one-control tuner) before touching the tick. **(b) grey inks** (`Avatar`,`Quick-actions`)→`color/mono/*` **via the
grey-tint check** (surface numbers to Dave FIRST — never auto-swap). **(c) regenerate** `_review` copies
(`_make_review.py`). **DO NOT ALIGN** the 5 archived files (Hero, Navigations, Progress-tracker, Tab-bar, Tabs,
+`_proforma/Icon-button`); **DO NOT CONVERT** Notifications (its `#A8000B` is correct Legacy red).

## 2. The red tuner + the two owed Mono values (Dave-in-the-loop — R-D19, feedback-live-controller)
ALL red is HELD until ruled on a live tuner: bare `rag/error` (Mono `#B92F1E`, rebinds with error/warning/info per
R-D17) + the two owed Mono values `tabs/active` + `progress/complete` (each needs its own **non-red** Mono value — ink?
green?). Only after red is ruled → flip `_validate_theme_provenance.py` to **blocking**.

## 3. RAG error/warning/info roles — still Legacy-drifted (R-D17, unchanged)
Bare `rag/error` (`#A8000B`/`#DB0011`), `rag/warning` (`#FFBB33`), `rag/information` (navy) still resolve Legacy; R-D14
values live in their `-background`/`-glyph` tokens. Rule the sets on the §2 tuner → rebind → these become Mono overrides.
**Needed before Alert / Banner / Toast.** Same work as §2's red.

## 4. Parked / carry-forward
**Duplicate-dedup pass** (relocate the archived files out of Mono scope so the gate stops scanning them). Console +
Supercharge override sets (fill null slots when palettes ruled). **T9 secure entry** awaits review. **Sutherland field
test** (ADR-0008 #1). **`designer-skills-v1`** revisit. Full-review backlog (`_REVIEW-SIGNOFF.md`). Parked
(`_FUTURE-STATE`): broader colour/theming, Apollo Labs tuners, bulk type-binding.

> **COMMIT STATE.** **HEAD `d6e3d89` — ahead 1, tree clean; Dave to push via GitHub Desktop.** Recent line:
> `4d0716b` (evening 3: state-manager freshness fix) → `2cf1ad7` (evening 4: bad-day non-start capture +
> verified sweep map, 0 code edits) → `d6e3d89` (evening 5: the teal→green sweep — 9 `_proforma` + regen
> `_review`, teal in `_proforma` 22→0). Build green 37/37. Two pre-existing info notes remain in
> `_LIVE-STATE-CHECK.md` (a `_NEXT-SESSION.md` dead-artifact mention + one orphan supersession edge) — tidy
> when convenient, not blocking. **Next session model: Opus** — the red tuner (§C·2) is Dave-in-the-loop
> judgment on a live controller, not throughput.
