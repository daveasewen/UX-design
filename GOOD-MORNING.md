# Good morning, Dave ☕

*Briefing — written end of 2026-07-18 (date from `date`, per the new ritual rule), session
**"Making the record answerable"** — the Fable consolidation run.*

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME YESTERDAY'S CHAT → `Making the record answerable`** *(no change — it already carries this
> name, and for once it earned it: the session did exactly what it was opened for — ran the Fable
> brief cold, you ruled the 11 pins, and the whole consolidation was enacted the same day.)*

> **TITLE TODAY'S CHAT →** `A gate for the blast radius`
> Next session = the binding blast-radius gate, **Opus**, per the queue below.

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
> rewritten often) · the chat = gone by morning. **Never let a durable rule live only on a Polaroid** —
> that is how §A's own standing instruction nearly died on 2026-07-18.
>
> **The real danger is not forgetting — it is confident false inscription.** Records carry provenance
> and confidence, not just content. Corrections get inscribed as loudly as the original claim. **Mark
> what was OBSERVED versus what was INFERRED.** It reaches even the small things: the T-D12 handoff
> dated itself "2026-07-19" while its commits landed 07-18 evening — so the ritual now stamps dates
> from `date`, never from the session's own belief.
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** Three times in one day a
> solution was designed to a problem the system had already answered. `_validate_assertions.py`
> catches a fact that flips; **nothing used to catch a rule we forgot we had — now something does:**
> ⇒ **Before designing anything, CONSULT: `python3 knowledge/_consult.py "<what you're about to
> design>"`** (557 records: rules · rulings · assertions · gates + where each bites). Paste the
> receipt (query + retrieved ids) into the work's review sheet or meta. Advisory tier for now;
> lexicon grows one line per miss. Runbook: `knowledge/_RUNBOOK-consult.md`.

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* Written new-starter style: assume the reader has
> no context and no memory of prior sessions. **Update it when the shape of the project changes, not
> every session — but never drop it, and never shorten it to a label.** *(Also step 2 of
> `_RUNBOOK-capture-ritual.md`, so it no longer depends on this file surviving. It is
> reachability-gated by `_validate_standing_instructions.py` — the gate caught a dropped reference
> again on 2026-07-18, which is the system working.)*

## What Apollo is
A **governed design-system engine** for agentic UI generation. The bet: *generation is a commodity* — the value
is the layer around any generator. Two principles run through everything:
- **Retrieval, not recall.** Brand values are retrieved from token stores, so generated work can't drift off-brand.
- **Verification = enforcement.** Judgment is encoded as **blocking gates**; "done" is withheld until they pass.
  If a rule isn't gated, assume it will be broken.

Tagline: **"lovable on rails."** Four phases: **Discover** → **Create** (what's being built now) → **Craft**
(the review-overlay docs ARE this) → **Dispatch**.

## The three libraries = ONE skeleton, three modes
One component skeleton; **modes are token-override sets**. Adding a library = adding a mode, **never forking**.
- **Apollo mono** — monochrome base (square, near-black primary, colour = meaning only). *"Pro-forma" = Apollo mono.*
- **Apollo UI** — the branded HSBC library. · **Apollo SC** — Supercharge, the prior branded work.

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores — the retrieval source (_proposals/ = holding pen)
  snippets/           38 gated reference components = CANON
  components/*.meta.json   per-component CRITERIA
  canon/              canon.css (GENERATED between AUTO markers) + type.css (HAND-AUTHORED composites)
  guidelines/         the rules, each with a stable {#id} + destiny tag; _rules-index.json (465, generated)
  _proforma/          Apollo mono tranches T1–T8 + Masthead + DataViz + the decisions ledgers
  _review/            review-overlay copies (+ _make_review.py). Gates never scan here.
  _consult.py         ★ NEW — "what governs X?" in one step; index generated every build
  _assertions.json    environment claims + predicates, re-tested every build
  _validate_*.py      the gates; orchestrated by _build_all.py (31 steps)
reviews/              consumable outputs + the review sheets you mark up
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always (402 lines, spine discipline)
_FUTURE-STATE.md      ★ NEW — side-quests, ideas, RESURRECTION candidates (the forward ledger)
_DECISION-HISTORY/    ★ NEW — dated narrative, relocated verbatim; RESURRECT tags; see its README
_retired/             reverted/retired work with residual value (incl. the memory-mirror snapshot)
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 31 steps, all gates, exits non-zero on any failure
```
Gates: a11y · contrast · state-contrast · icon-source · coverage · integrity · rules-index ·
assertions · standing-instructions · **DEF-003** no-JS-motion · **DEF-004** no-hardcoded-styling ·
**DEF-005** 4px grid · pro-forma · DataViz · consult-index + selftest (advisory) · edge-extremity
(advisory). **DEF-006 type-composites exists but is NOT wired** (deliberate — see the non-`/1` batch).

## Rules that actually bite
- **CONSULT before designing** (see the Memento block above) — then **survey before build**: grep
  `snippets/` + metas + tranches before building anything.
- **⚠️ canon.css** — "generated, never hand-edit" applies only *between the AUTO markers*; the `.c-*`
  layer above is hand-authored. **type.css is HAND-AUTHORED** throughout.
- **TYPE and BOX are separate lists** (T-D12). `.t-cm-<size>` = type incl. `line-height:1`, safe
  anywhere. `.t-cm-slot` = box, **opt-in, only where the element already declares flex.** Widening is
  a ruling, never a sweep.
- **A diff you cannot attribute is not evidence.** Isolate with a control (`NO_SNAP` pattern) before
  judging.
- **Icons: real assets only** — render-verify before binding; filenames lie.
- **4px grid** (DEF-005) · **sentence case** · **square corners in mono** · **red = primary-action
  accent, once per screen** (brand modes) · **weights: five licensed only — 100/300/400/500/700,
  THERE IS NO 600.**
- **A rule is only as wide as its gate's glob.** Bite-test every check.
- **Theme-dependent alias blocks use the same selector list as the tokens they wrap — never bare
  `:root`** (inscribed 2026-07-18; `_RUNBOOK-compose-from-canon.md`).
- **Run the gate as the LAST step before presenting** — a hand-built "canon" claim is what the gate
  exists to check (same runbook).
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
- **ATOMISE** — build at the true atomic level and compose up.
- **Supersession discipline** — tombstone + propagation gap in the same pass (`AGENTS.md`).
- **Spine discipline** (NEW 2026-07-18) — state lines in `_LIVE-STATE`; narrative >10 lines goes to
  `_DECISION-HISTORY/` at write time.

## Standing instructions for the agent (not the artefact)
- **Announce the model/routing split at the START of every substantive task, unprompted** (`MODEL-ROUTING.md`).
- **Verify before asking.** Answer state-questions by reading the repo or running the gates — not by asking Dave.
- **Reflect back before recording.** Restate the interpretation and confirm firmness **before** writing a ruling
  into a ledger. British understatement — "quite good" is not approval. **A lean is not a ruling.**
- **Ask what Dave valued in prior work BEFORE proposing mine-vs-fresh.** Change-by-change.
- **Decision-heavy or material-referring choices ship as a review-template HTML** (`_make_review.py`), not as
  `AskUserQuestion`.
- **Log rulings in the per-pillar decisions ledger**, with the WHY.
- **Surface spin-off candidates mid-chat**; register ideas/side-quests in `_FUTURE-STATE.md`.
- **Suggest reflection checkpoints**; run the capture ritual unasked at session end; **stamp dates
  from `date`**.
- **Memory is an accelerator; the repo is the record.** The repo mirror of memory was DELETED by
  ruling 2026-07-18 (snapshot in `_retired/`): durable content gets **inscribed** in its proper repo
  home in the same pass — never photocopied, never memory-only.

## The other standing documents
*(REACHABILITY-GATED by `_validate_standing_instructions.py` (STAND-002) — every one of these must
stay referenced from the cold-start spine. Do not prune this list.)*

`AGENTS.md` (repo agent contract, git split, supersession) · `MODEL-ROUTING.md` ·
`_FUTURE-STATE.md` (forward ledger) · `_DECISION-HISTORY/README.md` (the archive's rules) ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D12) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D3) · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`notes/_FABLE-BRIEF-consolidation.md` (**executed 2026-07-18** — kept for its §7 candidate list) ·
`knowledge/_DS-IMPROVEMENTS.md` · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` (6 live) · `knowledge/guidelines/_rules-index.json` (465 rules) ·
`_retired/` (tracked; vs `_to_delete/`, gitignored).

**Runbooks** — the method written down so a cold agent can operate the engine:
`_RUNBOOK-capture-ritual.md` (end of session — step 3 amended 07-18: inscribe, don't mirror) ·
`_RUNBOOK-consult.md` (★ NEW — the pre-flight protocol) · `_RUNBOOK-git-commit.md` (**the sandbox
lock dance — read before any git**) · `_RUNBOOK-gated-component.md` · `_RUNBOOK-compose-from-canon.md`
(now carries the two inscribed restyle lessons) · `_RUNBOOK-toolkit-tranche.md` ·
`_RUNBOOK-criteria-contract.md` · `_RUNBOOK-decision-audit.md` · `_RUNBOOK-reconcile-dark-tokens.md` ·
`_RUNBOOK-onboard-code-library.md`.
**`knowledge/_RUNBOOKS.md` is the runbook of runbooks** — GENERATED each build, so it cannot rot.

## Renders — REAL FONT, in-sandbox
Renders use the real HSBC cut (never stock Univers Next Pro — both are in `assets/fonts/_desktop/`):
```bash
pip3 install playwright --break-system-packages
NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium
mkdir -p ~/.fonts && cp knowledge/assets/fonts/_desktop/TTF/*.ttf ~/.fonts/ && fc-cache -f
# CSS: font-family:"HSBC_MtUnivers_Latin"  ·  verify: document.fonts.check('16px HSBC_MtUnivers_Latin')
```
Chrome needs ~17 libs via `apt-get download` → `dpkg -x` → `LD_LIBRARY_PATH`; full recipe in memory
`sandbox-html-rendering`. ⚠️ The browser cache can be wiped between bash calls — just re-run.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`_make_review.py <file>`).
- **Sheets are instruments, not proposals** — build them able to return a **null result**.
- **A specimen must reproduce the CONDITION its rule names, not merely the ELEMENT.**
- **Thresholds come from what Dave can SEE**, not from theory.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md`.
  ⚠️ The sandbox cannot unlink — to revert: `git show HEAD:<path> > <path>`; renames (`mv`) work.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-18, "Making the record answerable")

**The Fable consolidation run — opened cold from the brief, and for once the session did exactly
what it was opened for.**

## What LANDED

**⭐ The brief's central claim was tested and UPHELD, on cold evidence** — then the whole
consolidation was ruled (your 11 pins on `reviews/CONSOLIDATION-AUDIT-2026-07-18.html`) and enacted
same-day:
- **`_LIVE-STATE.md`: 1104 → 402 lines.** Nothing deleted: ~580 lines relocated **verbatim** to
  `_DECISION-HISTORY/` (7 dated files + README, with **RESURRECT tags** — your ruling that the old
  experiments feed the future Create modes); duplicates → pointers; two entries removed on their own
  recorded instructions. **Masthead recorded as shipped MLP.**
- **`_FUTURE-STATE.md` created** — your "future-state machine": side-quests, feature ideas,
  resurrection candidates (incl. the new **DataViz → colleague presentation** candidate).
- **The memory mirror is DELETED** (your ruling, pin 11): it was the third source of truth its own
  README forbade (115 vs 110, five ghosts). Dated snapshot in `_retired/agent-memory-snapshot-2026-07-18/`;
  ritual step 3 now says **inscribe, don't photocopy**.
- **The consult tool is BUILT** (pin 10; delegated to **Sonnet** per MODEL-ROUTING mode 2):
  `knowledge/_consult.py` over a 557-record generated index — rules, rulings, assertions, gates
  **with where each bites** ("gated by X over N files" vs "asserted only"). Selftest replays the
  three 07-18 stale-reading failures and passes honestly. Wired into the build (now 31 steps).
- **Two lessons inscribed as rules** (bare-`:root` alias trap · gate-as-last-step) in
  `_RUNBOOK-compose-from-canon.md`; **stale assertion prose fixed** (ASSERT-001/005 no longer speak
  the pre-ruling licence framing).

## Found cold (the §4.5 list — full version in the audit sheet §5)

1. **The record mis-dated itself**: the T-D12 handoff said "written end of 2026-07-19"; its commits
   landed 07-18 19:51–20:23. Fixed forward: dates from `date`.
2. **"1044 lines" had rotted to 1104** inside the very banner warning about growth.
3. **The assertion register nearly re-opened your closed licence thread** — stale consequence prose
   behind passing predicates. Fixed; the FLIP blind spot is real and now documented.
4. Pro-forma≡Apollo-mono naming, invisible LIVE-section stratigraphy, and the spine's unnamed
   guardian gate — all addressed structurally by the split + §A updates.

## What to watch (honesty over tidiness)

- **The spine rewrite was a full-file rewrite** — the operation class that degraded §A once before.
  Mitigations: relocations were verbatim `sed` extractions, not retypes; STAND-002 + the full build
  are green; the audit sheet records every cut. Residual risk: the new spine *summaries* are mine
  and **unaudited** — if one reads wrong against its ledger, the ledger wins.
- The consult tool's enforcement column is **keyword-fuzzy** ("possibly gated by…") — good enough
  for advisory tier; the gate-glob audit (Fable candidate #2) is the rigorous version, re-scope it
  after the tool beds in.

---

# §C · QUEUE

## 1. 🔴 The binding blast-radius gate — **next session, Opus**
Unchanged from the T-D12 handoff: bare selectors in a globally-linked stylesheet, load order doing
safety-critical work across ~460 selectors, ungated. Wanted BEFORE the non-`/1` batch binds 690 more.
`_LIVE-STATE.md` → OPEN has the candidate check.

## 2. Small picks — yours, no analysis needed
| what | detail |
|---|---|
| ~~matting rungs~~ | **RULED R-D4 same evening: green + blue matted 15%, red as-is; role tokens promoted.** |
| **`.tag` collision** | one atom one size, or `.tag--sm`? Actively blocks bindings |
| **`.num` 24px** | add a Component rung at 24, or snap to 20/32? |
| **`{#dv-017}`(a)** | the rule permits a palette it also excludes |

## 3. The non-`/1` batch (Sonnet, after #1)
61 shorthands in snippets + the tranche bulk; things move; DEF-006 stays unwired until it lands.

## 4. Consult protocol — bed it in
Use it at the top of every design task; paste receipts; grow the lexicon one line per miss. When it
has earned trust, promote the receipt check from advisory to blocking, and re-scope the **gate-glob
audit** (Fable candidate #2) against what the bite column already answers.

## 5. 🕓 Waiting on brand — the Latin webfont pack
Unchanged: files land in `knowledge/assets/fonts/` + Ultralight scope confirmed (= a type ruling,
not an asset drop). Not yours to chase beyond the ask.

> **COMMIT STATE:** this session's work is committed in-sandbox (paste-ready summary handed in chat);
> **you push via GitHub Desktop**, as ever. Build green, 31 steps; DEF-006 unwired by design.
> **Next session model: Opus** (§1 is judgment work). The audit sheet + REVIEW copy stay in
> `reviews/` as the session's record.
