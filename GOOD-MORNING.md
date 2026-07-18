# Good morning, Dave ☕

*Briefing — written end of 2026-07-18 afternoon, session **"Univers under the microscope."***

---

## ⬛ DO THESE TWO FIRST (10 seconds)

> **RENAME YESTERDAY'S CHAT →** `Univers under the microscope`
> *(it opened as the 721 rebinds; those never moved — it became a tracking-rules research arc
> and ended with a font-licensing finding)*

> **TITLE TODAY'S CHAT →** `Five sheets and a binding mechanism`

*Standing practice (your ask, 2026-07-18): every handoff carries **both** names — retrospective for
the session that ended, forward for the next. Sessions drift; naming them only at the start records the
intention rather than the work. Step 4b in `_RUNBOOK-capture-ritual.md`. I can't rename a conversation
myself — no tool — so these are ready to copy.*

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
square) · `_retired/` (reverted work with residual value — TRACKED; vs `_to_delete/` which is gitignored rubbish) ·
`_DS-IMPROVEMENTS.md` (logged DS defects — ds-001…003) · `_ICON-GAPS.md` (mislabelled/inverted icon
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

# §B · THIS SESSION (2026-07-18, afternoon)

**Opened as the 721 rebinds. They never moved.** What happened instead was a tracking-rules research
arc, a measured font study, and a licensing finding that now blocks sharing.

## What LANDED (committed, build green 29/29)

**A blocking rule that wasn't biting.** `{#type26-019}` bans uppercase brand-wide on a dyslexia
rationale, promoted to **blocking** by your 2026-07-02 ruling. It was only ever implemented in
`_validate_snippets.py`, which globs `snippets/*.reference.html` — so **`_proforma/` was never scanned**
and Tranche-3/5/6/8 carried `text-transform:uppercase` past it for weeks. Found incidentally while
grepping for letter-spacing. Added the check to `_validate_proforma.py` (which already declares itself
home to "the UNIVERSAL rules"), de-capped all five breaches with their caps tracking, and **bite-tested
it** by reintroducing an uppercase to confirm it fails.
> **Lesson, now in the gate source:** *a rule is only as wide as its gate's glob. "Blocking" describes
> the rule; the glob decides where it bites.* Same class as the type gate scoring clean on the very badge
> that motivated it, and Cards at 9/9 in June.

**`_TYPE-DECISIONS` → T-D1..T-D6.** The session's reasoning, inscribed.

**`ds-004`** — the `Fo` kerning gap is an upstream foundry omission, not HSBC's. Don't raise it with brand.

**Two spin-offs registered** in `_LIVE-STATE`: the fontTools **font-audit instrument**, and **real-font
embedding** for review sheets (candidate to fold into `_make_review.py`).

## ⭐ The ruling that matters most — yours

**Editorial and Component answer to different physics.** Editorial is *read* (fixations, saccades,
word-skipping). Component is *recognised* — nobody saccades through "Pending approval". Therefore:
- **Reading-speed evidence governs Editorial ONLY.** I'd been using it to argue against opening tracking
  on component labels, where it was never in scope.
- **Crowding evidence governs Component MORE** — the Zorzi/dyslexia work measures *letter
  identification*, which is exactly what recognising a label is. I had it filed under the wrong tier.
- **Structural consequence:** the same 40px wants −0.02em in Editorial and −0.01em in Component.
  **Size alone cannot express the rule** — so tracking must live ON the composites, not in a size-indexed
  token ramp. That's the strongest argument yet that the D2/D3 role split is real rather than tidy.
- **Frutiger drew the same line:** he designed *Frutiger* because Univers was "perfect for printed books"
  but wrong for someone crossing an airport at 5mph. He put Univers on the Editorial side of your split.

## Measured, not read (highest evidence tier we've had)

- **Univers is LOOSER than Helvetica** — `n` sidebearing 15.6% of x-height vs Arial 12.4%. The folklore
  "Univers is tight" is about **apertures**, not spacing. **Tracking cannot open a counter**, so the face's
  known glance-reading weakness is *not* fixable by the lever we spent the day designing.
- **Sidebearing/stem collapses 4.60 → 0.46** across the weight range — the largest single effect measured,
  and **no rule accounts for it**. Tracking may need a *weight* term.
- **HSBC's cut ≡ stock Univers Next Pro horizontally.** Sidebearings, advances, 60/60 kerning pairs — all
  identical. Only the **ampersand** differs. Published Univers spacing guidance therefore applies to us
  directly. Vertical metrics differ though: our line box 1.300em vs 1.200em, baseline ~11pp lower.

## ⚠️ Where I was wrong — four times, one of which you caught

1. **Invented a fork the evidence had closed.** Framed `col26-020(c)` as "universal floor vs conditional
   rung" and told you it blocked the retrofit. I'd read the *rule text*, not the *specimen that generated
   it*. → **Read the specimen, not the summary.**
2. **Nearly logged a font defect that doesn't exist.** First kerning parser said "no kerning except
   Medium"; the family uses GPOS *extension lookups* it was skipping. → **A finding that makes a vendor
   look careless deserves a second parser.**
3. **Nearly reported 8% as 30%.** Ascent 1068 vs 750 *looks* decisive; stock carries a 200-unit lineGap
   that HSBC zeroed. → **Compute the derived quantity; never eyeball the component.**
4. **← YOU CAUGHT THIS ONE. Struck a blocker that was right.** I found the Latin *desktop* set and
   declared the "Latin webfont missing" blocker false. **Desktop ≠ webfont licence.** The blocker named
   the webfont, and it was correct. → **A blocker that has stopped work for weeks is exactly the claim
   you WANT to be false, so disproving one deserves MORE scrutiny than confirming it, not less.**

**The pattern across all four: the first answer was tidy and confirmed what I half-expected.** That is
the signal to run it twice.

---

# §C · QUEUE

## ⛔ 0. THE BLOCKER — Latin Univers **webfont** pack. Yours, and it gates sharing.
We hold five *script* webfont packs and **zero Latin**. The desktop set is licensed for design work on a
machine, not for embedding or serving. Without the webfont: **no shareable specimens, no real-face review
docs sent outside, no hosted prototype in brand type.**
**Ask brand for: the Latin "Univers Next for HSBC" webfont pack (WOFF + WOFF2)** — same deliverable
already held for the five script companions.
*Also yours:* four tracked files (`TYPE-SPECIMEN` / `TYPE-COMPOSITES` 2026-07-17, plain + REVIEW) embed
base64 Univers and are pushed. Repo is **private** (404 unauthenticated) and Monotype's prohibition names
*public* repos — so exposure is low but not zero. Options: leave / `git rm --cached` / BFG history purge.
Terms are on file at `knowledge/assets/WebfontUserGuide-2024.pdf`. Full detail: `_LIVE-STATE` top entry.

## 1. FIVE review sheets await your markup — nothing is promoted
| sheet | asks |
|---|---|
| `TRACKING-CONTACT-2026-07-18` | 7 ladders, 47 cells, **renders in real Univers**. My picks marked green. |
| `COMPONENT-MEDIUM-2026-07-18` | are the 100 Component `500`s structural or drift? |
| `TRACKING-DOSSIER-2026-07-18` | evidence tiers + 4 contradictions + 7 questions |
| `UNIVERS-DOSSIER-2026-07-18` | the measured font study |
| `RAG-PROMOTION-2026-07-18` | **from 07-17, still unmarked** — amber trap: `#333` on delta amber = 4.13:1, FAILS |

## 2. ⚠️ TYPE-002 ×721 — BLOCKED, and I under-scoped it
I told you 339 were "safely bindable". True that they *map* to a composite value-wise; **false that the
work is mechanical**. The composites are used in **zero files** — `.t-cm-*` / `.t-ed-*` appear in no
markup anywhere. So binding needs either markup class changes on 339 elements, or a composition mechanism
that doesn't exist. **That's an architectural fork — markup class vs CSS composition vs build-time
inlining — and it's yours.** Exactly the class of decision the T6 revert taught us to ask about first.

## 3. Then: wire DEF-006 and drive to green. Still unwired; would red the build today.

## 4. Carried, unchanged
Q5 (col26-020 scope) still open · triage the 25 edge-extremity findings · rebind the 10 literal `#1A1A1A`
· paste the Figma style description from `neutral-blacks.proposals.json` · **rule→gate coverage: 42 of 54
BLOCKING rules cited by no gate** — today's blind-spot is one instance of exactly that · Tranche 8 comments
· DataViz 🟡 parked.

> **COMMITTED:** `4cc58ff` (gate fix + inscription) · `362be48` (the webfont correction).
> **You have pushed.** Build green 29/29. Nothing uncommitted.
> **Memory changed this session** — worth running your rsync (`knowledge/_agent-memory/README.md`).
