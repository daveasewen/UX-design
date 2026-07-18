# Good morning, Dave ☕

*Briefing — written end of 2026-07-18, session **"Amber, and the box inside the composite."***

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME YESTERDAY'S CHAT →** `Amber, and the box inside the composite`
> *(it opened as the binding-mechanism ruling and got it — then spent most of its length solving
> amber, and ended by discovering that the type composite has a BOX hiding inside it.)*

> **TITLE TODAY'S CHAT →** `Splitting type from box`

*Standing practice (your ask, 2026-07-18): every handoff carries **both** names — retrospective for
the session that ended, forward for the next. Step 4b in `_RUNBOOK-capture-ritual.md`. I can't rename
a conversation myself, so these are ready to copy.*

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
> **The trust hierarchy is the tattoo/Polaroid distinction:** memory files + runbooks = tattoos (durable,
> survive any single rewrite) · `GOOD-MORNING` + `_LIVE-STATE` = Polaroids (working state, rewritten often)
> · the chat = gone by morning. **Never let a durable rule live only on a Polaroid** — that is how §A's own
> standing instruction nearly died on 2026-07-18.
>
> **The real danger is not forgetting — it is confident false inscription.** Leonard's tragedy is that he
> writes a *false* tattoo and then trusts it absolutely, because he cannot remember writing it. So: records
> carry provenance and confidence, not just content. Corrections get inscribed as loudly as the original
> claim. **Mark what was OBSERVED versus what was INFERRED** — `dv-019`'s 135° leg says *"because Dave saw
> the dance on a 146° pair"*, and that sentence is the tattoo, not the number.
>
> **NEW, 2026-07-18 (second session) — there is a SECOND failure mode, and it cost more than the first.**
> Three times in one day I designed a solution to a problem the system had **already answered**: a dark
> ochre glyph (the 1.4.1 label-carries-meaning waiver was already canon in five snippets) · a 49-file
> inline sweep (portability had never actually been tested) · "no Univers in-sandbox" (the licensed fonts
> have been in the repo all along). **Not stale FACTS — a stale READING of our own rules.**
> `_validate_assertions.py` catches a fact that flips. **Nothing catches a rule we forgot we had.**
> ⇒ **Before designing anything: grep the guidelines and read the gates.** The answer is often already
> written down.

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* Written new-starter style: assume the reader has
> no context and no memory of prior sessions. **Update it when the shape of the project changes, not
> every session — but never drop it, and never shorten it to a label.**
>
> *(Restored 2026-07-18 after a from-scratch rewrite reduced this note to the words "Standing section",
> losing both the instruction and Dave's reason for it. The rule had been surviving only by being copied
> forward, so a rewrite silently degraded it. It is now also step 2 of `_RUNBOOK-capture-ritual.md`, so it
> no longer depends on this file surviving.)*

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
  tokens/             DTCG token stores — the retrieval source
    _proposals/       HOLDING PEN: structured, provenanced, NOT promoted
  snippets/           38 gated reference components = CANON
  components/*.meta.json   per-component CRITERIA
  canon/              canon.css (GENERATED — see the CAVEAT) + type.css (composites, HAND-AUTHORED)
  guidelines/         the ingested + Apollo-added RULES, each with a stable {#id} and a destiny tag
    _rules-index.json   GENERATED machine-readable rule spine (465 rules)
  _proforma/          Apollo mono tranches T1–T8 + Masthead + DataViz  ← in-flight build surface
    _TYPE-DECISIONS.md   type rulings ledger (T-D1…T-D11)
    _RAG-DECISIONS.md    colour rulings ledger (R-D1…R-D3)   ← NEW 2026-07-18
  _review/            review-overlay copies (+ _make_review.py). Gates never scan here.
  _assertions.json    environment claims + predicates, re-tested every build
  _validate_*.py      the gates; orchestrated by _build_all.py
reviews/              consumable outputs + the review sheets you mark up
_LIVE-STATE.md        LIVE / DEAD / OPEN — read second, always
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 30 steps, all gates, exits non-zero on any failure
```
Gates: a11y · contrast · state-contrast · icon-source · coverage · integrity · rules-index ·
assertions · **DEF-003** no-JS-motion · **DEF-004** no-hardcoded-styling · **DEF-005** 4px grid ·
pro-forma · DataViz · edge-extremity (advisory). **DEF-006 type-composites exists but is NOT wired.**

## Rules that actually bite
- **Survey before build** — grep `snippets/` + metas + tranches BEFORE building.
- **⚠️ canon.css** — "generated, never hand-edit" applies only *between the AUTO-COMPONENTS markers*.
  The **`.c-*` composition layer above that marker is hand-authored and has NO snippet source.**
- **⚠️ type.css is HAND-AUTHORED** — its "generated" header was false and is gone (2026-07-18).
- **Icons: real assets only.** Filenames are not trustworthy — render-verify before binding.
- **4px grid** (DEF-005) · **sentence case** · **square corners in mono** · **red = primary-action
  accent, once per screen** (brand modes only).
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
- **ATOMISE** — build at the true atomic level and compose up.
- **Weights: five licensed only — 100/300/400/500/700. THERE IS NO 600.**
- **A rule is only as wide as its gate's glob.** "Blocking" describes the rule; the glob decides where
  it bites. `{#type26-019}` was blocking for weeks while four tranches breached it.
- **Supersession discipline** — a ruling that kills something tombstones the artefact **and** logs the
  propagation gap in the same pass. Non-negotiable per `AGENTS.md`.

## Standing instructions for the agent (not the artefact)
- **Announce the model/routing split at the START of every substantive task, unprompted** (`MODEL-ROUTING.md`).
- **Verify before asking.** Answer state-questions by reading the repo or running the gates — not by asking Dave.
- **Reflect back before recording.** Restate the interpretation and confirm firmness **before** writing a ruling
  into a ledger. British understatement — "quite good" is not approval. **A lean is not a ruling.**
- **Ask what Dave valued in prior work BEFORE proposing mine-vs-fresh.** Change-by-change; this cost a reverted T6.
- **Decision-heavy or material-referring choices ship as a review-template HTML** (`_make_review.py`), not as
  `AskUserQuestion`.
- **Log rulings in the per-pillar decisions ledger**, with the WHY.
- **Surface spin-off candidates mid-chat**; register in `_LIVE-STATE`.
- **Suggest reflection checkpoints**; run the capture ritual unasked at session end.
- **Memory is NOT backed up.** It lives outside the repo and dies with the Cowork space.
  **Memory is an accelerator; the repo is the record.**

## The other standing documents
*(This paragraph is REACHABILITY-GATED by `_validate_standing_instructions.py` (STAND-002) — every
one of these must stay referenced from the cold-start spine. **My 2026-07-18 rewrite dropped four of
them and the gate caught it**, which is the §A-degradation failure the capture runbook predicts.
Do not prune this list.)*

`AGENTS.md` (repo agent contract, git split, supersession) · `MODEL-ROUTING.md` (which model for
which work) · `knowledge/_proforma/_PROFORMA-RULES.md` (Apollo mono mode rules: monochrome,
`surface/digital-black`, colour=meaning, square) · `knowledge/_proforma/_TYPE-DECISIONS.md` (type
rulings T-D1…T-D11) · `knowledge/_proforma/_RAG-DECISIONS.md` (colour rulings R-D1…R-D3) ·
`knowledge/_proforma/_DATAVIZ-DECISIONS.md` (DataViz rulings) · `knowledge/_DS-IMPROVEMENTS.md`
(logged DS defects — ds-001…004) · `knowledge/_ICON-GAPS.md` (mislabelled/inverted icon assets) ·
`knowledge/_ASSERTIONS.md` + `knowledge/_assertions.json` (environment claims + predicates, 6 live) ·
`knowledge/guidelines/_rules-index.json` (465 rules, the machine-readable spine) · `_retired/`
(reverted work with residual value — TRACKED; vs `_to_delete/`, gitignored rubbish).

**Runbooks** — the method written down so a cold agent can operate the engine:
`_RUNBOOK-capture-ritual.md` (end of session) · `_RUNBOOK-git-commit.md` (**the sandbox lock dance —
read it before any git**) · `_RUNBOOK-gated-component.md` · `_RUNBOOK-compose-from-canon.md` ·
`_RUNBOOK-toolkit-tranche.md` · `_RUNBOOK-criteria-contract.md` · `_RUNBOOK-decision-audit.md` ·
`_RUNBOOK-reconcile-dark-tokens.md` · `_RUNBOOK-onboard-code-library.md`.
**`knowledge/_RUNBOOKS.md` is the runbook of runbooks** — GENERATED each build, so it cannot rot.

## Renders — REAL FONT, in-sandbox (updated 2026-07-18)
**The old "no Univers in-sandbox, layout only" caveat is DEAD.** Renders use the real HSBC cut:
```bash
pip3 install playwright --break-system-packages
NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium
mkdir -p ~/.fonts && cp knowledge/assets/fonts/_desktop/TTF/*.ttf ~/.fonts/ && fc-cache -f
# CSS: font-family:"HSBC_MtUnivers_Latin"  ·  verify: document.fonts.check('16px HSBC_MtUnivers_Latin')
```
**Always the HSBC cut, never stock Univers Next Pro** (Dave, 2026-07-18) — both are in
`assets/fonts/_desktop/`, metrically identical horizontally, but only one is the brand font.
Chrome also needs ~17 libs via `apt-get download` → `dpkg -x` → `LD_LIBRARY_PATH`. Full recipe in
memory `sandbox-html-rendering`. ⚠️ The browser cache can be **wiped between bash calls** — just re-run.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`_make_review.py <file>`).
- **Sheets are instruments, not proposals.** Build them able to return a **null result**.
- **A specimen must reproduce the CONDITION its rule names, not merely the ELEMENT.** Ground-dependent
  effects (halation, vibration) need the ground at real extent. *(New 2026-07-18 — family A's specimen
  was a small chip on a white page, which under-tests halation.)*
- **Thresholds come from what Dave can SEE**, not from theory.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md`.
  ⚠️ **The sandbox cannot unlink** — `git checkout` FAILS. To revert: `git show HEAD:<path> > <path>`.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION (2026-07-18, second)

**Opened on the binding-mechanism ruling and got it in the first hour. Then spent most of its length
on amber — and ended by finding a box hiding inside the type composite.**

## What LANDED — ruled and built

**⭐ T-D9 · The binding mechanism.** Components bind by being **appended to their composite's
selector list** in `type.css`. Plain CSS, no generator, no build step, **no markup change**. Your
words: *"so the JSON is for generation but A would just work with CSS and HTML??"* — which found the
simplification. The generator is deferred, not required.

**T-D8 · Variant D, OBSERVED not reasoned.** Cap-trim does **not** need the `.txt` child; it applies
to the element directly. Rendered in real HSBC Univers, four variants × three button shapes, all
h=20. `.btn` bound and **pixel-diff verified** — the only difference was the loading spinner caught
at a different animation frame.

**T-D10 · Component Medium is drift.** 88 declarations snap to 400, **zero new composites**. Settled
by **pin POSITION** — all 19 pins sat on the 400 column, none on the 500.

**⭐ R-D3 · AMBER SOLVED.** `amber/background` **`#F0B13A`** (ink 9.16) + `amber/graphic`
**`#C58900`** (3.02 white, 6.25 dark). Two rules: *always paired with black text*; *not a
directional delta colour, but valid for status and tolerance*. Ledger: **`_RAG-DECISIONS.md`** (new).

## What FAILED, usefully

**T-D11 · The 21-file batch — reverted.** I predicted the 208 `/1` declarations would bind as a
no-op like `.btn`. **13 of 21 files moved, 2 changed page height.** `.btn` was already
`inline-flex` so the composite told it nothing new about its BOX; `.eyebrow`, `.badge`, `h2`,
`.status` are block or inline, so binding handed them a layout change wearing a type change's
clothing. **The pixel diff caught it before it shipped.**

## What you caught, and were right about

1. **"Can't you use the desktop fonts in assets?"** — killed a 16-month-old false caveat I'd repeated
   three times *that session*.
2. **"The entire project must be portable"** — reversed my 49-file inline sweep; it solved a problem
   that doesn't exist and would have created 49 copies to keep in sync.
3. **"Contrast with a white background is a luxury, the label carries the meaning"** — already canon
   in five snippets. I'd built a dark ochre glyph to satisfy a rule we had deliberately waived.
4. **"This is for finance, we might not get away with this one"** — correctly narrowed my rule from
   "amber is not a data colour" to "not a *directional* delta colour".
5. **"I'm getting a little frustrated, we're going round in circles"** — you were right, and I should
   have caught it first.

## The thing to know before §C1

**`.t-cm` conflates TYPE with BOX.** Type = family/size/weight, safe anywhere. Box = `inline-flex`,
`align-items:center`, `line-height:1`, `min-height`, cap-trim — only safe where the element is
already a single-line control. **That is the whole reason the batch failed.** Split them and it
becomes a genuine no-op.

---

# §C · QUEUE

## 1. ⭐ SPLIT TYPE FROM BOX — one small ruling, ~460 selectors unblocked
Propose: `.t-cm-*` keeps **type only**; a new `.t-cm-slot` carries the **box**. Elements already
shaped like controls take both; everything else takes type only and keeps its own box.
Then: `python3 knowledge/apply_type_bind.py --apply` re-derives the batch in one command →
wire DEF-006 → drive to green. **Opus for the ruling; Sonnet for the rebind.**

## 2. Small picks — yours, no analysis needed
| what | detail |
|---|---|
| **matting rung, green + blue** | `as now` / `−15%` / `−28%` / `−40%` · `reviews/RAG-MATTING-2026-07-18.html`. **No numerical tell — I must not guess.** |
| **`.tag` collision** | 14px canonical vs 12px "reused" — one atom one size, or `.tag--sm`? |
| **`.num` 24px** | no Component rung at 24px. Add one, or snap to 20/32? |
| **`{#dv-017}`(a)** | permits red/green for deltas while naming **"RAG-style cells"** — RAG includes amber. **The rule permits a palette it also excludes.** |

## 3. Gates owed — rules that exist but don't bite
Amber rules 1 + 2 · `type.css` load order · **DEF-006 still unwired** · dark-mode green `#1AA05C`
(3.37) · dark-mode red/blue as TEXT glyphs on `#111` (3.97 / 4.15).

## 4. ⛔ YOURS — the Latin Univers **webfont** pack
Ask brand for **WOFF + WOFF2**. Gated as `ASSERT-001` — when it lands the build goes red and names
every doc that says otherwise. *(Unchanged. The desktop set being usable in-sandbox does NOT affect
this: desktop ≠ webfont.)*

## 5. 🧹 CONSOLIDATION — separate track, **Fable, cold**
`_LIVE-STATE.md` is now **~1044 lines** and has still never shrunk. Today added to it.
**New input for that session:** the failure mode is not only stale *facts* (the assertion gate
handles those) but stale *readings* — rules we have and forget. And: **the review overlay loses row
identity**, which cost two rounds today and is a product fix, not a process one.

> **COMMITTED:** nothing yet — one paste-ready commit below.
> Build: DEF-006 fails by design (unwired). Everything else green.
> **Next session model:** Opus for §1; Sonnet once the split is ruled. **Fable + cold for §5 only.**
