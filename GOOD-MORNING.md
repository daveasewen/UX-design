# Good morning, Dave ☕

*Briefing — written end of 2026-07-19 00:46 (date from `date`, per the ritual rule), session
**"A gate for the blast radius"** — built the gate, then rode it through a chain of cleanups.*

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME THIS CHAT → `The button-label audit that became a gate`** *(it opened as the ds-005
> button-label clip audit — a Sonnet-scoped sweep — and the buttons came back CLEAN: `.btn`/`.cta`/`.qbtn`
> centre their labels and never truncate, so no clip (null result). But the sweep surfaced the real
> instances elsewhere: 7 truncating labels (Tranche-2/3/4/7/8 + Masthead `.dd-title`/`.navitem-tx`) that
> DO clip descenders (render-confirmed: "Savings"→"Savin*q*s"). You ruled against a case-by-case patch AND
> against blanket-CSS — "do it right": a blocking descender-clip GATE, keeping cap-alphabetic as the
> default. ds-005 GATED + CLOSED; commit `3af1696`.)*

> **TITLE TODAY'S CHAT →** `Clearing the small-picks desk`
> Next session = the §2 small picks now ds-005 is closed (`.num` 24px rung · `{#dv-017}`(a) ·
> Tag colour/RAG) + the non-`/1` / DEF-006 batch. **Sonnet** for the batch; **Opus** if a ruling
> surfaces. Per §C.

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
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md`.
  ⚠️ The sandbox cannot unlink — to revert: `git show HEAD:<path> > <path>`; renames (`mv`) work.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-19 late, "The button-label audit that became a gate")

**Opened as the ds-005 follow-on — a Sonnet-scoped sweep to audit `.btn`/`.cta`/`.qbtn` for the descender
clip. The buttons came back CLEAN. But the sweep found the clip live elsewhere, and your ruling turned a
recurring one-line patch into a permanent gate.**

## What LANDED (one commit, `3af1696`)

- **Buttons CLEAN — null result.** `.btn`/`.cta`/`.qbtn` centre their labels (`justify-content:center`,
  no `overflow:hidden` on any label) → they never truncate → no clip. ds-005's "next-most-likely" suspects
  don't carry the condition. The sheet returned null, as a good instrument should.
- **The real debt was 7 truncating labels — render-confirmed** (real HSBC cut) that `cap alphabetic` +
  `overflow:hidden` clips descenders: "Savings"→"Savin*q*s". Instances: Masthead `.dd-title` (live) +
  `.navitem-tx` (defined-but-unused here — nav labels render as `.menulink`, which don't truncate — fixed
  defensively), plus `.dp-title`/`.uz-name` (T2), `.sel-value`/`.sel-opt-lbl` (T3), `.crumb-current` (T4),
  `.navitem-tx` (T7/T8). List-items + canon were already safe.
- **🔴→✅ New blocking gate `_validate_descender_clip.py` (step 27/34).** Every `text-overflow:ellipsis`
  label must carry `text-box-edge:text text` (or `overflow:visible`). High-precision — keys off `ellipsis`,
  so containers + sr-only patterns are ignored. Bite-tested both ways; selftest covers same-rule /
  comma-group / overflow-visible overrides + container/sr-only exclusion. **All 7 fixed, ZERO waivers.**
- **Provenance against false-fixing (your explicit ask).** Inline `/* ds-005 */` comments · ds-005
  GATED+CLOSED in the ledger · gate indexed in consult · and a "these overrides ARE the fix, do not remove"
  note in the gate docstring **and** the red-build message. A cold session can't quietly revert them.

## The ruling (yours, this session)

- **"do it right — use your suggestion": GATE the condition, don't blanket the CSS.** Blanket `text text`
  would have undone cap-alphabetic alignment everywhere; the gate enforces the rule only where a label
  truncates, keeping cap-alphabetic as the default. Logged as the ds-005 decision-tree extension.

## What I got wrong / watch

- My first instinct was apply-and-commit; you redirected twice — first to reflect the ellipsis+icon+
  descender trilemma back before editing (right), then to gate rather than patch (righter). **Lesson: when
  a fix recurs across files, the durable move is the gate, not the Nth patch.**
- `.navitem-tx` is defined-but-unused in the demo files — fixed defensively; flag if the side-nav variant
  gets instantiated for real.

---

# §C · QUEUE

## 1. Small picks — desk-clear — **next session** (yours, no analysis needed)
| what | detail |
|---|---|
| **`.num` 24px** | add a Component rung at 24, or snap to 20/32? |
| **`{#dv-017}`(a)** | the rule permits a palette it also excludes |
| **Tag colour/RAG** | deferred by you — layer status colour onto the atom when ready. |

## 2. The non-`/1` batch (Sonnet)
61 shorthands in snippets + the tranche bulk; things move; DEF-006 stays unwired until it lands.

## 3. Consult protocol — bed it in
Use it at the top of every design task **including the mechanics, not just the decision**. Paste receipts;
grow the lexicon per miss. Promote receipt-check advisory→blocking once trusted.

## 4. 🕓 Waiting on brand — the Latin webfont pack
Unchanged: files land in `knowledge/assets/fonts/` + Ultralight scope confirmed. Not yours to chase.

> **COMMIT STATE:** work committed in-sandbox at `3af1696` (the gate + 7 fixes); the ritual docs
> (`_LIVE-STATE`, `GOOD-MORNING`, `_DS-IMPROVEMENTS`, memory) commit next. Locks clear; **you push via
> GitHub Desktop**. Build green, **34 steps**; DEF-006 unwired by design. **Next session model: Sonnet**
> (small-picks desk-clear). Session record: `reviews/` + `_DS-IMPROVEMENTS` ds-005 + this handoff.
