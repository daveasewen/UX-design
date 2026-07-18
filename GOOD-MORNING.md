# Good morning, Dave ☕

*Briefing — written end of 2026-07-18, session **"Halation, chroma and the rule nobody wrote down."***

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME YESTERDAY'S CHAT →** `Halation, chroma and the rule nobody wrote down`
> *(it opened as the type retrofit; the retrofit was ~15% of it)*

> **TITLE TODAY'S CHAT →** `Type retrofit part 2 — the 721 rebinds`

*New standing practice (your ask, 2026-07-18): every handoff now carries **both** names at the top —
retrospective for the session that just ended, forward for the next. Sessions drift; naming them only
at the start records the intention rather than the work. Recorded as step 4b in
`_RUNBOOK-capture-ritual.md`. I can't rename a conversation myself — no tool — so these are ready to copy.*

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
> writes a *false* tattoo and then trusts it absolutely, because he cannot remember writing it. On
> 2026-07-18 I wrote "38% of the rule corpus is silently missing" with full confidence; it was wrong, and
> had Dave not challenged it, it would have entered the ledger as fact and been trusted by every session
> after. **So: records carry provenance and confidence, not just content. Corrections get inscribed as
> loudly as the original claim. Mark what was OBSERVED versus what was INFERRED** — `dv-019`'s 135° leg
> says *"because Dave saw the dance on a 146° pair"*, and that sentence is the tattoo, not the number.

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* Written new-starter style: assume the reader has
> no context and no memory of prior sessions. **Update it when the shape of the project changes, not
> every session — but never drop it, and never shorten it to a label.**
>
> *(Restored 2026-07-18 after I rewrote this file and reduced this note to the words "Standing section",
> losing both the instruction and Dave's reason for it. The rule had been surviving only by being copied
> forward, so a from-scratch rewrite silently degraded it — the same failure as the `#1A1A1A` rationale.
> It is now also step 2 of `_RUNBOOK-capture-ritual.md`, so it no longer depends on this file surviving.)*

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
    _proposals/       HOLDING PEN: structured, provenanced, NOT promoted (the pattern for recording
                      a decision without enacting it — see neutral-blacks.proposals.json)
  snippets/           38 gated reference components = CANON
  components/*.meta.json   per-component CRITERIA
  canon/              canon.css (GENERATED — but see the CAVEAT below) + type.css (composites)
  guidelines/         the ingested + Apollo-added RULES, each with a stable {#id} and a destiny tag
    _rules-index.json   GENERATED machine-readable rule spine (465 rules) — gates/judge/promotion queue
  _proforma/          Apollo mono tranches T1–T8 + Masthead + DataViz  ← in-flight build surface
  _review/            review-overlay copies (+ _make_review.py). Gates never scan here.
  _validate_*.py      the gates; orchestrated by _build_all.py
reviews/              consumable outputs + the review sheets you mark up
_LIVE-STATE.md        LIVE / DEAD / OPEN — read second, always
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 29 steps, all gates, exits non-zero on any failure
```
Gates: a11y · contrast · state-contrast · icon-source · coverage · integrity · rules-index ·
**DEF-003** no-JS-motion · **DEF-004** no-hardcoded-styling · **DEF-005** 4px grid · pro-forma · DataViz ·
**{#col26-020} edge-extremity (advisory, new 07-18)**. **DEF-006 type-composites exists but is NOT wired** —
it would red the build until the 721 rebinds land.

## Rules that actually bite
- **Survey before build** — grep `snippets/` + metas + tranches BEFORE building. (Skipping this duplicated
  Tab-bar + Stepper in T8.)
- **⚠️ canon.css — the rule as usually stated is WRONG.** "Generated, never hand-edit" is imprecise: the
  generator's marker says *do not hand-edit **between the AUTO-COMPONENTS markers***. The **`.c-*` composition
  layer above that marker is hand-authored and has NO snippet source** — edits there must be made in
  `canon.css` directly or they are lost at regeneration. Cost most of an hour on 07-18. `apply_type_snap.py`
  is region-aware; copy its approach.
- **Icons: real assets only.** Filenames are not trustworthy — render-verify before binding.
- **4px grid** (DEF-005) · **sentence case** · **square corners in mono** (roundels are the carve-out) ·
  **red = primary-action accent, once per screen** (brand modes only).
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
- **ATOMISE** — build at the true atomic level and compose up.
- **Weights: five licensed only — 100/300/400/500/700. THERE IS NO 600** (`type25-004`; the OTF set ships no
  SemiBold, so a 600 is browser-synthesised faux-bold). This nearly got enacted on 07-18.
- **Supersession discipline** — a ruling that kills something tombstones the artefact **and** logs the
  propagation gap in the same pass. Non-negotiable per `AGENTS.md`.

## Standing instructions for the agent (not the artefact)
*Added 2026-07-18 after an audit found these lived only in memory — i.e. one tattoo deep, no backup.*
- **Announce the model/routing split at the START of every substantive task, unprompted** (`MODEL-ROUTING.md`).
- **Verify before asking.** Answer state-questions by reading the repo or running the gates — not by asking Dave.
- **Reflect back before recording.** Restate the interpretation and confirm firmness **before** writing a ruling
  into a ledger. British understatement — "quite good" is not approval.
- **Ask what Dave valued in prior work BEFORE proposing mine-vs-fresh.** Change-by-change; this cost a reverted T6.
- **Decision-heavy or material-referring choices ship as a review-template HTML** (`_make_review.py`), not as
  `AskUserQuestion` — that tool is for simple questions only.
- **Log rulings in the per-pillar decisions ledger**, with the WHY, so iterative feedback survives —
  `_proforma/_TYPE-DECISIONS.md` and `_proforma/_DATAVIZ-DECISIONS.md` today; one per pillar as they appear.
- **Surface spin-off candidates mid-chat** — reusable tools worth generalising; register in `_LIVE-STATE`.
- **Suggest reflection checkpoints**; run the capture ritual unasked at session end.
- **Memory is NOT backed up.** It lives outside the repo, at
  `~/Library/Application Support/Claude/local-agent-mode-sessions/…/spaces/<space-uuid>/memory/` — local files,
  not cloud, but keyed to the Cowork space —
  is invisible to the shell and every gate, and dies with the Cowork space. **Memory is an accelerator; the repo is
  the record.** Mirror instructions: `knowledge/_agent-memory/README.md` — Dave's one rsync, worth running whenever
  memories changed.


## The other standing documents
`AGENTS.md` (repo agent contract, git split, supersession) · `MODEL-ROUTING.md` (which model for which work) ·
`_proforma/_PROFORMA-RULES.md` (Apollo mono mode rules: monochrome, `surface/digital-black`, colour=meaning,
square) · `_DS-IMPROVEMENTS.md` (logged DS defects — ds-001…003) · `_ICON-GAPS.md` (mislabelled/inverted icon
assets) · `guidelines/_rules-index.json` (465 rules, the machine-readable spine).

**Runbooks** — the method written down so a cold agent can operate the engine:
`_RUNBOOK-capture-ritual.md` (end of session) · `_RUNBOOK-git-commit.md` (**the sandbox lock dance — read it
before any git**) · `_RUNBOOK-gated-component.md` · `_RUNBOOK-compose-from-canon.md` (the `.c-*` composition
layer) · `_RUNBOOK-toolkit-tranche.md` · `_RUNBOOK-criteria-contract.md` · `_RUNBOOK-decision-audit.md` ·
`_RUNBOOK-reconcile-dark-tokens.md` · `_RUNBOOK-onboard-code-library.md`.

**`knowledge/_RUNBOOKS.md` is the runbook of runbooks** — GENERATED from the filesystem each build
(`gen_runbook_index.py`), so adding a runbook lists it automatically and the index cannot rot. Read that
rather than this paragraph if you want the current set with purposes.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`_make_review.py <file>`). Edits apply to the
  clean source; the review copy is regenerated, never hand-edited.
- **Sheets are instruments, not proposals.** Build them able to return a **null result** — the 07-18 specimen
  said outright that if lightness rather than chroma were the driver, the honest outcome was *no new rule*.
- **Thresholds come from what Dave can SEE**, not from theory (dv-019's 135°; the 0.72 ceiling). A perceptual
  rule with no observed number is a preference, not a gate.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox via `_RUNBOOK-git-commit.md` — **clear locks
  → stage → clear → commit → clear** (`mv`, never `rm`).
- **Comms:** exec summary + numbered next steps first, detail below.
- **Renders:** in-sandbox Playwright works (`pip install playwright` + `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`
  + `apt-get download` the libs and `dpkg-deb -x` them into `LD_LIBRARY_PATH`). **No Univers in-sandbox** — renders
  verify layout, never brand type. HTML is what Dave reviews.

---

# §B · THIS SESSION (2026-07-18)

**Started as the type retrofit. Became something more useful.**

**Type retrofit — half done.** DEF-006 gate written first (your ruling), baseline **1183 violations / 50 of 50
files**. All 17 review rulings applied via `apply_type_snap.py`: **342 values snapped**, TYPE-003 **412 → 11**
(the 11 are DataViz SVG text, deferred under rule 4C — SVG text px is viewBox-relative, so snapping it to the
CSS ramp measures the wrong thing). **TYPE-002 ×721 — the actual composite rebinding — has not moved.**

**Then the badge "danced."** Chasing it produced the session's real work:
- Ran it through **our own** `vibration()` — scores **0/3 legs**, correctly. It is **not** `{#dv-019}`.
- Built a specimen sheet able to falsify itself; your control pair (equal lightness, different saturation)
  proved **chroma is the driver, not lightness**.
- You asked where the anti-halation black was stored. It was `#1A1A1A` — **in no token store, gated by nothing,
  still marked "open to confirm" since ~07-04, and its rationale never written down.** The value survived; the
  reason didn't.
- That unified the whole thing: **"reduce the extremity of the edge"** — two levers, **chroma** on coloured
  grounds, **luminance extremity** on neutral. Both had been operating for weeks, unrecognised as one rule.

**Landed:** `surface/digital-black` promoted · rules **{#col26-020}** + **{#col26-021}** written into the KB
prose and indexed · `_validate_edge_extremity.py` built and wired (advisory) · thresholds quantified from your
observation (**sat ≤0.72**; weight **500 @ 12–16px, 300 @ 20px**, nothing below 12) · `_PROFORMA-RULES` rule 1's
stale line closed · capture-ritual step 4b added.

**Three times I was wrong, corrected in the ledger:**
1. Claimed the rules index silently drops 38% of rules. **It doesn't** — `IN FORCE`/`RECORDED`/`PROCESS` are
   deliberately non-indexed, blessed by you 2026-07-03. Your challenge caught it. The *real* hole is narrower:
   **42 of 54 BLOCKING rules are cited by no gate.**
2. Blamed the spidery badge on my `700→500` collapse. **The weight was always fine** (Medium is the floor at
   14px) — the **ground** was the fault.
3. Invoked `type25-008` ("Emphasis = Bold only") to argue for 700. It governs keywords in running text, not
   badge counts. No bearing.

**And the gate lied on its first build** — reported "clean across 50 files" because snippets write
`background:var(--surface)` and I skipped anything with a `var()`. It was green on the very badge that motivated
it. Fixed with custom-property resolution + a regression test. Same blind spot that let Cards score 9/9 with
real failures in June. **With sight restored: 25 findings across 9+ components** — which answered scope
empirically: library-wide, not badges.

---

# §C · QUEUE

1. **TYPE-002 ×721 — the composite rebinding.** The big one, untouched. Per-component judgement:
   **single-line → `.t-cm-*`, wrapping → `.t-ed-*`** (multi-line Component text drifts off-grid — the N1
   caveat). Then wire DEF-006 into `_build_all.py` and drive to green.
2. **RAG promotion sheet** — `reviews/RAG-PROMOTION-2026-07-18.REVIEW.html`, awaiting your markup. The delta
   family is saturation-normalised at 0.72 across all four hues; the incumbent is 1.00/1.00/1.00/0.47.
   **The amber dependency runs through it:** you ruled amber takes dark text, but `#333333` on the delta amber
   is **4.13:1 and FAILS** — only `#1A1A1A` or `#000` pass.
3. **Triage the 25 edge-extremity findings**, then decide whether the check becomes blocking.
4. **Rebind the 10 literal `#1A1A1A` usages** to `surface/digital-black` (the token exists; the literals don't
   reference it).
5. **Apply the Figma style description** — ready-to-paste text in
   `tokens/_proposals/neutral-blacks.proposals.json` → `$carriers.figmaStyleDescription`. Your action. The
   styles panel is the only place a designer sees the condition; an empty description is the exact failure
   this record exists to prevent.
6. **Rule→gate coverage report** — **42 of 54 BLOCKING rules are cited by no gate**, including `type25-008`.
   `verified_by` already exists for WCAG SCs in the compliance graph; extend it to house rules and the unknown
   becomes a triaged list. *This is the mechanism for "I don't want these things to be missed."*
7. **Rule 4A** — `.arrow--sm/md/lg` + Tags size modifiers as candidates in `_review/` for your promotion call.
8. **Tranche 8 comments** — still deferred, twice now.
9. **DataViz** — still 🟡 parked. Carries an open question now: should the type ramp gain a **viewBox-relative
   expression** so chart type is governed in the units it actually renders in?

> **UNCOMMITTED:** nothing — all six commits landed (`bd21398`, `a6b3dc8`, `c84a08e`, `095b817`, `cf012ec`,
> `58c0561`, `a580ffb`). Build green **27/27**. Push via Desktop.
