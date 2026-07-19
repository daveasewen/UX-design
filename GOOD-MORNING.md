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

> **RENAME THIS CHAT → `Apollo Mono: R-D16 enacted, snippets styled by tokens, and the three-tier stack (elevation exemplar)`**
> *(read good-morning solo; enacted R-D16 — greys onto the ramp + 2 a11y carve-outs; built `gen_snippet_tokens.py`
> so snippets are styled BY the tokens, no hand-sync; Dave ruled the strict THREE-TIER token architecture → wrote
> `_STANDARDS.md` + `_validate_token_tiers.py` gate + dark-elevation as the exemplar (`surface/raised #1F1F1F`,
> dialled on a live tuner). Two commits pushed. Then turned composer: scoped Tranche-9 + wrote the T1–T8 tokenize brief.)*

> **TITLE TODAY'S CHAT →** `Tranche 9 · Secure entry — build it token-driven (composer); kick the T1–T8 tokenize worker`
> Build **T9 · Secure entry** (OTP/PIN, password Show/Hide + strength, memorable-word, re-auth) as the FIRST
> **token-driven** tranche — it carries a `#token-manifest` + current values (mirror T6's format, add the manifest).
> In parallel kick the worker brief `notes/_BRIEF-tranche-tokenize-T1-T8.md`. First ruling owed: the **mono
> primary-action token** (`action/primary/*`) — no token exists for the near-black primary button. **Opus** (build + ruling).

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

# §B · THIS SESSION (2026-07-19 afternoon, "R-D16 enacted, snippets styled by tokens, three-tier stack")

## What LANDED (this session — TWO commits, both pushed)
- **✅ R-D16 ENACTED — commit `dba719b`, pushed.** 90 semantic greys re-based onto `color/mono/*` (text ink
  `#1A1A1A`, secondary collapsed to the single ink, mechanical dark greys); `$alias` repointed to `color/mono/N`.
  **★ TWO a11y carve-outs the contrast gate FORCED** (provenance `_proforma/_RAG-DECISIONS.md` R-D16 — do NOT
  revert to nearest-step): dark borders/dividers → `mono/8 #808080` (`mono/7` = 2.76:1 on the `#1A1A1A` ground);
  text-bearing pressed fills → `mono/7 #626262` (white label on `mono/8` = 3.95). Residual `#333` UI → `#1A1A1A`;
  `text/on-inverse` + 6 data-vis greys LEFT. `col25-011` annotated.
- **★ `gen_snippet_tokens.py` (NEW) — snippets are STYLED BY the tokens** (Dave: "the snippets need to be styled by
  the tokens"). Projects `semantic-colour.json` → each snippet's `[data-theme]` blocks + `canon.css .cn-*` via the
  snippet's own `#token-manifest`. Idempotent, self-verifying, `driftAllow`-aware, fails loud. No more hand-sync.
- **★★ THREE-TIER TOKEN ARCHITECTURE RULED (Dave) — component → semantic → primitive; a component NEVER references
  a primitive.** NEW standing hub **`_STANDARDS.md`** (§1) + ADR `_DECISION-HISTORY/2026-07-19-token-tier-architecture.md`
  + memory `token-tier-architecture`. Storage: `$alias` = source of truth, `$value` = gate-verified cache. NEW
  blocking gate **`_validate_token_tiers.py`** (component→semantic + `$value == resolve($alias)`), wired in (now 35 steps).
- **★ Dark elevation = the 3-tier reference example — commit `e69b75f`, pushed.** Primitives `color/mono/raise-1/2/3`
  = `#1F1F1F / #232323 / #272727` (Dave dialled on the **v2 live tuner**) → semantic `surface/raised`, `surface/subtle`,
  `surface/raised-hover` → the 9 surface components R-D16 flattened onto the ground. Press recedes to ground (valid).
  `gen_canon_tokens.py` emits the real `var()` chain.
- **Live-controller preference banked** (memory `feedback-live-controller`): for feel-dials default to a slider tuner.

## What I got wrong / watch
- **Mis-called `gen_canon_tokens.py` "orphaned"** — it's in `canon/`, I looked in `knowledge/`. Corrected. Verify a
  path before declaring something missing.
- **Nearly over-deferred the component work** (kept doing foundations); Dave rightly pushed to build. Momentum.
- **Fuel gauge UNDER-reads:** the Haiku reading said GREEN 23.5% but the transcript export compacts tool results (a
  single file read this session was bigger than the whole transcript it counted) → treat as a floor; real fill is
  higher (low-mid amber). Candidate fix: gauge from something closer to the live window.

## Composer setup (session tail — turned conductor at Dave's "you're the boss now")
- **Tranche 9 · Secure entry & verification PICKED** (OTP/PIN, password Show/Hide + strength, memorable-word,
  re-auth). Icons verified in the sprite (`security-password/secure-key/secure/face/digital-identity`); password
  toggle = **"Show/Hide" text** (no eye glyph — more device-agnostic, tov-038). NOT built (queued §C1).
- **Worker brief WRITTEN:** `notes/_BRIEF-tranche-tokenize-T1-T8.md` — the 8 tranches hardcode pre-R-D16 values with
  no manifest (drifted); tokenize them (add `#token-manifest`, project via `gen_snippet_tokens`, gate, receipt).
  Worktree-isolated, **no-commit**, receipt for the composer to reconcile.

---

# §C · QUEUE

## 1. ★ BUILD Tranche-9 · Secure entry (composer, next real deliverable)
The **first token-driven tranche**: carries a `#token-manifest` + the CURRENT token values (mirror T6's format —
`_proforma/Tranche-6-interactive.html` — but add the manifest so it's projectable, per `_STANDARDS.md` §4).
Components: **OTP/PIN** (segmented numeric boxes, auto-advance, paste, error/complete) · **password** (Show/Hide
text toggle + strength meter) · **memorable-word / security field** · **re-auth prompt**. Real sprite icons only.
Monochrome; the one hue is the RAG error state (like T1's amount-input error). Gate green.

## 2. ★ KICK the T1–T8 tokenize worker
Brief: `notes/_BRIEF-tranche-tokenize-T1-T8.md`. Worktree-isolated subagent (values are ruled → mechanical +
flagged). It files a receipt in `notes/_receipts/`; composer reconciles the worktree + commits (git-commit runbook
step 0.5 — account for every dirty path, never blind `git add -A` with a worker live).

## 3. ★ RULING owed — the mono PRIMARY-ACTION token (surfaced by the tranche work)
The near-black primary button (`--pri/--pri-h/--pri-lbl` in the tranches) has **no semantic token** — likely needs
new `action/primary/*` tokens. Also the ambiguous tranche vars (`--disi`, `--line2`, `--surf`, `--scrim`,
`--shadow`) flagged in the brief for a binding decision.

## 4. Deferred store migration + latent bugs
The REST of the store is still 2-tier (components alias primitives) — migrate onto proper tiers deliberately
(elevation proved the pattern). `_validate_token_tiers` **advisory** lists **4 legacy alias bugs** to fix:
`border/strong`, `form/border/default`, `form/border/pressed` (dark) → alias should be `color/mono/8`;
`primary/border/hover` (dark).

## 5. Carry-forward (still open, pre-today) + memory
§1 RAG manifestation pick + status-component build · amber rules gate · component RAG rebind (blast-radius). Parked
(`_FUTURE-STATE`): broader colour/theming, Apollo Labs tuners, bulk type-binding, compliance edges, Latin webfont.
**Memory index compaction is DUE** (~19.6KB; the hook flagged it) — run it early next session or in the ritual.

> **COMMIT STATE.** **TWO commits this session, BOTH pushed by Dave:** `dba719b` (R-D16 enacted + snippets styled by
> tokens + `gen_snippet_tokens.py`) and `e69b75f` (three-tier token architecture + `_STANDARDS.md` + elevation
> exemplar + `_validate_token_tiers.py`). **THIS wrap commit (docs/handoff only, build GREEN 35/35):**
> `notes/_BRIEF-tranche-tokenize-T1-T8.md`, `_LIVE-STATE.md`, `GOOD-MORNING.md` (+ memory files, outside the repo).
> No gated-code change. **You push via GitHub Desktop.**
> **Next session model: Opus** (T9 build + the mono-primary ruling); the tokenize worker can be Sonnet.
