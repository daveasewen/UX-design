# Good morning, Dave ☕

*Briefing — written 2026-07-19 16:20 (date from `date`, per the ritual rule), session
**"RAG light fills: proving per-mode, and a tuner I could use for days"** — took the R-D11 parked piece
(light-mode fills) all the way to a locked, reconciled set, turned a per-mode assertion into a proof, and
built a two-mode in-browser colour tuner along the way.*

> ✅ **TWO SESSIONS this round — merged by conductor (this session).** A parallel session ("Context gauge +
> adversarial densify") ran the same day and handed up a RECEIPT (the single-writer **conductor pattern** it
> wrote — `notes/_PARALLEL-SESSIONS-conductor.md`). Both strands are folded into §B/§C below and committed
> together. Its main work landed in its own commit `e7f8b87`; its two trailing files + this handoff are in the
> conductor commit.

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME THIS CHAT → `RAG light fills: proving per-mode, and a tuner I could use for days`** *(opened on
> "read good morning"; became the light-fill pass R-D11 had parked. Locked the light set, PROVED green/blue
> must be per-mode by exhaustive search, reframed fill-contrast as a salience lever not a floor, and built a
> live two-mode OKLCh tuner. Nine review versions v1→v9-LOCKED. Ledger R-D12…R-D14.)*

> **TITLE TODAY'S CHAT →** `Promote the RAG tokens + nail the status component`
> RAG colour is DONE (light + dark locked, R-D14). Next is the **token promotion** — write `rag/*` (breach +
> watch mode-stable; healthy + info per-mode: light `#5DAC7B`/`#7DABCD`, dark `#43AD6F`/`#5F92B9`) to
> `tokens/semantic-colour.json`, rebind **behind the blast-radius gate**, run `_build_all.py`. Then the **§1
> manifestation** pick (sheet `reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`) + status-component build.
> **Sonnet** for all of it — it's enactment, not ruling. Per §C.

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
python3 knowledge/_build_all.py     # 34 steps, all gates, exits non-zero on any failure
```
Gates (34 steps): a11y · contrast · state-contrast · icon-source · coverage · integrity · rules-index ·
assertions · standing-instructions · **DEF-003** no-JS-motion · **DEF-004** no-hardcoded-styling ·
**DEF-005** 4px grid · **type-binding blast-radius** (guards `canon/type.css`, registry
`canon/_type-bindings.json`) · **descender-clip** (NEW — ds-005; truncating labels must carry
`text-box-edge:text text`) · pro-forma · DataViz · consult-index + selftest (advisory) ·
edge-extremity (advisory). **DEF-006 type-composites exists but is NOT wired** (deliberate — see the non-`/1` batch).

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
- **Every selector appended to `canon/type.css` is GLOBAL** (T-D9 binding). New ones must be registered
  in `canon/_type-bindings.json` or the blast-radius gate fails (UNREGISTERED / ESCAPED / UNWAIVED-BARE).
  Run `_validate_type_blast_radius.py --update` for intentional growth, then review the diff.
- **Truncating labels clip descenders — GATED** (`_DS-IMPROVEMENTS` ds-005, closed 07-19): any label that
  truncates (`text-overflow:ellipsis`) MUST carry `text-box-edge:text text`, or the descender-clip gate reds
  the build. `text text` keeps the ellipsis AND stops the clip; **cap-alphabetic stays the default wherever a
  label does NOT truncate** — it's the icon-alignment mechanism, not a defect. Short non-truncating icon atoms
  (tags) use `cap alphabetic` + `overflow:visible`. ⚠️ **The scattered `text text` overrides ARE the fix, not
  an inconsistency — the gate + its docstring say so; do not "clean them up".** Buttons audited clean (they
  never truncate).
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
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — **run it, don't
  improvise git.** ⚠️ **DO NOT misread the lock error.** `unable to unlink … *.lock` / `tmp_obj_*` /
  `index.lock: Operation not permitted` is the sandbox **delete-guard**, NOT GitHub Desktop holding the repo and
  NOT "sandbox can't commit". The dance: **clear · stage · clear · commit · clear**, moving every `.git/*.lock`
  aside with **`mv` (never `rm`)**, and **judge success by HEAD advancing, not by the warnings** (the commit lands
  despite them). To revert: `git show HEAD:<path> > <path>` (`git checkout` can't unlink); the bulk revert form
  also reverts your uncommitted TOOLING — park it first. Full procedure + gotchas: `_RUNBOOK-git-commit.md`.
  *(Inscribed 2026-07-19 after I stalled on exactly this misread — the runbook was referenced but I didn't run it.)*
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-19 later, "RAG light fills: proving per-mode, and a tuner I could use for days")

**Took the light-mode fill set R-D11 had parked all the way to LOCKED + reconciled, turned the per-mode claim into
a proof, and built a live two-mode colour tuner. Rulings R-D12…R-D14; ledger `_proforma/_RAG-DECISIONS.md`.
Narrative arc (why + how, dead-ends included): dossier `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md`
Session 3. Sheets v1→v9-LOCKED + derivation `reviews/_rag_light_fills_calc.py`.**

## What LANDED

- **✅ LIGHT fills LOCKED (R-D14):** light **green `#5DAC7B`** · **blue `#7DABCD`** (H241, black text). Dark stays
  R-D10 (`#43AD6F`/`#5F92B9`). Red `#B92F1E`/white + amber `#F0B13A`/`#C58900` mode-stable. **NO lines** (R-D12 A) ·
  **black text on states** (R-D12 B). Verified both grounds: every label ≥ AA, green › blue in both.
- **★ Per-mode PROVEN, not asserted.** Exhaustive pair search: no single green/blue keeps green › blue on both
  grounds ("louder" = darker on white, lighter on dark → green can't lead on both). R-D11's thesis is now a proof.
- **Reframe (Dave):** *"its not just about the colour"* — a status cell is a **labelled component**, so fill
  contrast is a **salience/scan lever, NOT an accessibility floor** (the floor is the LABEL, R-D6). This dissolved
  the "washout" worry entirely.
- **★ Built a two-mode in-browser OKLCh TUNER** (v6→v7): wide saturation + fine lightness sliders per hue, live
  hex + contrast + a **ramp-guard** that reds if green ≤ blue on that ground. Dave: *"i could do this for days."*
  Strong **Apollo Labs / Layer-2 controls** candidate (registered).
- **Method finding:** the R-D9 salience metric **inverts on white** (white text = zero distance from a white page,
  so it penalises the cell that should shout) → on white, order by fill-vs-page + chroma. Recorded in the calc tool.

## What I got wrong / watch

- **Re-raised amber-on-white as an open question when R-D6 had already ruled it** (label carries meaning). Dave:
  *"amber is fine… we've ruled on this already, please check."* Classic **stale-reading failure** — the CONSULT
  step exists for exactly this; I should have checked R-D6 before flagging. Corrected in v2 + the ledger.
- **The tuner emerged from too many colour round-trips.** Lesson banked: past ~2 colour round-trips, give the eye
  a live control rather than another static version.
- **Nothing gated touched** — build state unchanged from prev green; no `_build_all.py` run needed. The **token
  promotion** is the first thing that hits the blast-radius gate (deferred, Sonnet).

## Parallel strand — "Context gauge + adversarial densify" (session 2, merged from its receipt)

- **Context fuel-gauge built:** `knowledge/_context_gauge.py` + `_RUNBOOK-context-gauge.md` (tally +
  out-of-band confirm; **Red >70% fires the capture ritual mid-session**). Committed `e7f8b87`.
- **Adversarial densify method:** `_RUNBOOK-densify-adversarial.md` (densifier → adversary gate). **KEY FINDING:
  rewording is a near-dead lever corpus-wide** (ops 3–9%, KB ~2.8% — already terse). **DON'T run a corpus
  densify**; KEEP the adversary gate (it caught 3 losses + 11 fabrications). Real levers = disable unused
  plugins (baseline) + prune/archive (tiering). Memory index pruned; 6 entries → `MEMORY-ARCHIVE.md`.
- **★ REAL BUG found (chase separately):** `gen_rules_index.py` **silently truncates 11+ entries mid-sentence**
  in `knowledge/guidelines/_RECONCILIATION.md` (mot-007, neuro-041/042, pict-014, tov-016, type26-015/026/029,
  webf-017, ctkb-015, icon-015). Silent data loss in the rules index — correctness issue.
- Its memories already surgically updated (`feedback-context-gauge`, `feedback-adversarial-densify`, MEMORY
  index + archive) — conductor did NOT touch those. The **conductor pattern itself** (`notes/_PARALLEL-SESSIONS-conductor.md`)
  is this round's process artefact: single writer for shared state; workers emit receipts. Promote to a runbook
  + `AGENTS.md` clause in a single-session slot.

---

# §C · QUEUE

## 1. ★ RAG token promotion — the next real deliverable (Sonnet, behind the blast-radius gate)
RAG colour is DONE (R-D14). Promote to `tokens/semantic-colour.json` `rag/*`: **breach `#B92F1E` + watch
`#F0B13A`/`#C58900` mode-stable; healthy + info PER-MODE** — light `#5DAC7B`/`#7DABCD`, dark `#43AD6F`/`#5F92B9`;
all states black text, breach white; **no lines**. Rebind components, run `_build_all.py`, expect the blast-radius
gate to bite (that's the point). Also build the **amber gate** (rules 1+2, still unenforced). Reconciled table in
ledger R-D14 + `reviews/RAG-LIGHT-FILLS-2026-07-19-v9-LOCKED`.

## 2. §1 RAG manifestation — canon pick, then the status component build (Sonnet)
Decision sheet built (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`): Status-indicator dot+label (existing
canon) · filled cell/badge · bar/edge; tags+pills EXCLUDED by canon. Awaiting Dave's pick (A / A+B / A+B+C).
Then spec cell/bar as gated components (**cells need more vertical padding** — Dave, R-D11 note).

## 3. Parked in `_FUTURE-STATE` (not urgent)
**Apollo Labs** (the tuner + isoluminant/ramp/halation engine) · whole-palette sweep · edge-triage interface ·
~450 variable-weight target · dual-observer principle.

## 4. From the parallel session (gauge / densify) — merged queue
1. **Fix `gen_rules_index.py` truncation bug** — silent mid-sentence data loss for 11+ rules in the index
   (list in §B). Correctness; do first of these.
2. **Plugin-disable pass** — Dave's toggle in Settings › Capabilities (Figma / pdf-viewer / cowork-plugin-mgmt /
   design connectors): the biggest single context-baseline cut.
3. ✅ **DONE — conductor pattern promoted** → `_RUNBOOK-parallel-conductor.md` + `AGENTS.md` clause, now with
   the **"read good morning"** role trigger (AskUserQuestion Worker/Conductor/Solo; conductor reads workers via
   `session_info`, zero receipts to paste). Commits `a75b452` + `1efb0aa`.
4. **Corpus densify = DON'T** (settled — near-dead lever); keep the adversary gate.

## 5. Carry-overs still open (prior sessions)
Bulk type-binding for ~338 elements (T-D9/T-D11/T-D14) · compliance edges (27 unverified `verified_by`,
advisory) · multi-size countdown · 🕓 Latin webfont pack (waiting on brand, not yours to chase).

> **COMMIT STATE — ONE conductor commit, docs only (NO gated code).** RAG strand: `_proforma/_RAG-DECISIONS.md`
> (R-D12…R-D14), `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md` (Session-3 continuation),
> `reviews/RAG-LIGHT-FILLS-2026-07-19-v1…v9-LOCKED` (+ `.REVIEW`), `reviews/_rag_light_fills_calc.py`. Shared
> handoff: `_LIVE-STATE.md`, `_FUTURE-STATE.md`, `GOOD-MORNING.md`. Merged from the parallel session (its main
> work already in `e7f8b87`): `knowledge/_RUNBOOK-densify-adversarial.md` + `notes/_PARALLEL-SESSIONS-conductor.md`.
> `_to_delete/_dense_test/` is gitignored — excluded. Build state unchanged (no gated sources).
> **Follow-on commits (this session, post-merge — also to push):** `a75b452` (conductor-pattern runbook +
> `AGENTS.md` clause) · `1efb0aa` ("read good morning" role trigger). **You push via GitHub Desktop.**
> **Next session model: Sonnet** (token promotion + component build — enactment, not ruling).
