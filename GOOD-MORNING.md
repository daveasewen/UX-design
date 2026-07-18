# Good morning, Dave ☕

*Briefing — written end of 2026-07-19, session **"Splitting type from box."***

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME YESTERDAY'S CHAT →** `The box was the line-height all along`
> *(it opened as the type/box split and got it — but the ruling that actually decided the batch was
> one nobody had queued: where `line-height` lives. It then spent its back half closing the font
> licence thread, and ended by scoping the Fable session.)*

> **TITLE TODAY'S CHAT →** `Making the record answerable`

> **🅕 THIS SESSION IS THE FABLE RUN — start it on FABLE, COLD.** No warm-up, no re-reading this
> conversation. **First action: open `notes/_FABLE-BRIEF-consolidation.md` and execute it**, §0
> first. The brief is self-contained and written to be run cold; if it can't be understood cold,
> that is finding #1, report it. Everything in §C below is context for AFTER the brief, or for a
> different session — **do not let it pull you off the consolidation.** (Dave, 2026-07-19:
> *"assume the fable briefing and run is kicked off by the handoff."*)

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
    _TYPE-DECISIONS.md   type rulings ledger (T-D1…T-D12)
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
- **TYPE and BOX are separate lists** (T-D12). `.t-cm-<size>` = family/size/weight/**line-height:1**,
  safe anywhere. `.t-cm-slot` = display/align/min-height/cap-trim, **opt-in, only where the element
  already declares flex.** Slotting anything else is a per-component ruling, never a sweep.
- **A diff you cannot attribute is not evidence.** Before calling a change good or bad, isolate it
  with a control (see `NO_SNAP` in `apply_type_bind.py`). Pixel count alone condemns correct work.
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
`knowledge/_proforma/_DATAVIZ-DECISIONS.md` (DataViz rulings) ·
`notes/_FABLE-BRIEF-consolidation.md` (**the scoped Fable session** + the running candidate list) ·
`knowledge/_DS-IMPROVEMENTS.md`
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

# §B · THIS SESSION (2026-07-19, "Splitting type from box")

**The queued ruling landed in the first hour. Then a question nobody had queued turned out to be the
one that decided the batch — and the back half closed a licence thread that had been mis-recorded
for weeks.**

## What LANDED

**⭐ T-D12 · TYPE and BOX are separate lists. RULED, and verified before asking.**
`.t-cm-<size>` carries family/size/weight/**line-height:1** — safe anywhere. `.t-cm-slot` carries
display/align/min-height/cap-trim — **opt-in**, bound only where the element already declares a flex
display. The slot height rides on `--slot`; a custom property is inert unless read, which is what
makes the two lists independent. **13/21 pixel-identical, zero page-height changes**, real HSBC
Univers. Closes T-D11. Commit `9fb1381`.

**⭐ The ruling that actually decided it was not on the queue.** §C1 asked "type or box". The real
question was **where `line-height` lives.** With it in the BOX, type-only bindings silently DROPPED
the `/1` the old shorthand carried — `.stateLabel` fell to `line-height:normal`, h 12→16. Moving it
into TYPE took the result 11/21 → 13/21 and removed the last page-height change.
**The queued question was the right area and the wrong question.**

**🕓 The webfont thread — closed on distribution, reframed on the rest.** Repo is private and
everything in it is shared only to HSBC employees, so the distribution worry is **CLOSED, ruled
"leave"** — no `git rm`, no BFG purge. The licence itself is **renewal-pending, procedural, low-risk**
(your call, recorded as made — don't let me re-litigate it). What survives is **not a risk item**:
**zero Latin `.woff`/`.woff2` files exist**, so shareable real-face material is blocked by
asset-delivery, not permission.

**📋 The Fable session is now scoped** — `notes/_FABLE-BRIEF-consolidation.md`, with a running
candidate list for you to add to.

## What I got wrong, and what caught it

**Two defects in my own enactment — NEITHER caught by a gate, both by inspection.**
1. **A hold honoured in planning was violated in the write.** `.tag` was correctly skipped as a
   collision, then stripped anyway: removal used a global `str.replace`, and `.tag` carries the
   identical declaration text as the bound `.chip`. **A hold that exists only in the planning stage
   is not a hold.**
2. **The slot list patched 1 of 3 `.t-cm-slot` occurrences**, so a slotted selector could have got
   the box *without* the cap-trim — a different bug wearing the same clothes.

**I designed the split before checking whether line-height was already ruled anywhere.** That is the
07-18 stale-reading failure again, one day later, by the agent who wrote the warning. It cost two
render cycles rather than a day, but the shape is identical.

**I also mis-ranked the Fable task**, listing the consolidation ninth as housekeeping until you
pushed back. It isn't housekeeping — see §C.

## What you caught

1. **"I thought we had a big task set up for fable"** — I'd buried it. It's the only Fable-designated
   task in the repo and it deserved the top of the list, not the bottom.
2. **"it's checked already, this is a private repo"** and **"only shared to other HSBC employees"** —
   two facts that closed a thread I was still treating as an open risk.
3. **The licence is procedural, not a blocker** — I had been citing `WebfontUserGuide-2024.pdf` as if
   it were the entitlement record. **It isn't one** — it's generic usage guidance with no schedule.
   Our "we hold no Latin webfont" claim has always rested on absence of files. Now recorded as such.

---

# §C · QUEUE

## 1. 🅕 THE FABLE SESSION — THIS IS THE RUN, not a decision to make
**Per Dave's ruling 2026-07-19, the handoff kicks off the Fable run: opening this session cold IS
starting it.** Go straight to `notes/_FABLE-BRIEF-consolidation.md` and execute §0 onward. The brief
argues the task is not "shorten `_LIVE-STATE`" but **"make the record answerable"** — four complaints
from one fortnight are one problem: *we can write to the KB far better than we can interrogate it.*
It carries the running **candidate-task list** (§7, Dave adds to it) and my argument that
**"turbo-charge the KB" is four tasks, of which retrieval is the unlock.**
**Do not warm-start, do not detour into §§2–6 first.** If the record can't be read cold, that is the
first thing to report, not to paper over.

## 2. Small picks — yours, no analysis needed
| what | detail |
|---|---|
| **matting rung, green + blue** | `as now` / `−15%` / `−28%` / `−40%` · `reviews/RAG-MATTING-2026-07-18.html`. Sitting unmarked since 07-18. **No numerical tell — I must not guess.** |
| **`.tag` collision** | 14px canonical vs 12px "reused". **Actively blocks bindings.** One atom one size, or `.tag--sm`? |
| **`.num` 24px** | no Component rung at 24px. Add one, or snap to 20/32? |
| **`{#dv-017}`(a)** | permits red/green for deltas while naming **"RAG-style cells"** — RAG includes amber. **The rule permits a palette it also excludes.** |

## 3. 🔴 The binding blast-radius gate — my view: BEFORE the next batch
The selector-list mechanism puts **bare, unscoped selectors** (`h2`, `.label`, `.status`, `.chip`)
into a globally-linked stylesheet. It holds only because component CSS loads second — **load order
doing safety-critical work across ~460 selectors, ungated.** `.tag` was the first collision.
**This does not reopen T-D9**; it's the missing guard-rail. Opus-sized.

## 4. The non-`/1` batch — and why DEF-006 stays unwired
61 non-`/1` shorthands left in `snippets/`; the bulk of the remaining **690 TYPE-002** are in the
pro-forma tranches. They carry line-heights of 1.1–1.6, so binding **moves things** — needs its own
reviewed batch with T-D12's before/after pixel discipline. **DEF-006 is 780 → 729 and stays unwired
until then**: a build that is red on known work trains everyone to ignore a red build.

## 5. Gates owed
Amber rules 1 + 2 · `type.css` load order · dark-mode green `#1AA05C` (3.37) · dark-mode red/blue as
TEXT glyphs on `#111` (3.97 / 4.15).

## 6. 🕓 Waiting on brand — the Latin webfont pack
Not a blocker, not yours to chase beyond the ask. **Two things clear it:** the `.woff`/`.woff2` files
landing in `knowledge/assets/fonts/`, and brand confirming whether **Ultralight** is in scope.
⚠️ **Ultralight is not a detail** — the script packs ship Th/Lt/Rg/Md/Bd ≡ 100/300/400/500/700, so an
Ultralight sits BELOW Thin and is a **sixth weight**: a change to the canon ramp, therefore a **type
ruling, not an asset drop.** Expect it; don't discover it in a diff.

> **COMMITTED:** `9fb1381` (T-D12 + verification + the two script fixes). This handoff is a second
> commit below. Build green, all 30 steps; DEF-006 fails by design.
> **Next session model:** **§1 IS the session — Fable, cold, from the brief.** §§3–4 are later
> sessions (Opus for §3; Sonnet for §4 once §3 is ruled), NOT this one.
