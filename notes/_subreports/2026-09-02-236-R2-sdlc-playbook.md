# `#236`-`R2` — the AI-native SDLC playbook, read and mapped onto Memento, the packs, and Discover

session: `#236` · 2026-09-02
window: lane R2 (research sub; sibling lane R1 = principles survey)
sub index: `R2`
brief: `notes/_briefs/2026-09-02-236-R2-sdlc-playbook-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`. SHAPE: 29 tool calls — **4 web fetches**
(3 returned inline; the blog spilled to a local tool-result file, read in 3 ranges + 1 heading
sweep) · **1 web search** (to locate the academy course) · **1 ToolSearch** · **12 repo bash
probes** · **4 reads** (the brief + 3 ranges of the spilled article) · **1 grep** · **3 writes** ·
**3 edits**.

## VERDICT

**All six deliverables DONE; nothing is UNPROVEN that mattered to the mapping.** The blog post
fetched whole (1,975 lines, read 100%) and the academy course is **free and reachable** — no
paywall, no sign-in wall on the content; two of its fourteen lessons were fetched and found
equivalent to their blog sections, and the course's one material addition is a *dependency graph
described in alt-text* that the blog only shows as an image. The playbook is **twelve plays across
six stages**, and its actual spine is not the stages — it is a rule that every stage ends by
committing a file the next stage reads, so the chain of commits becomes the audit trail.

**The headline, and it is not the flattering one.** The thing the playbook is *most* proud of is
the thing Apollo ruled against nine hours ago. `intent.md` → `spec.md` → `plan.md` → the diff →
`REVIEW.md` → the incident record is a **COPY chain**: the spec restates the intent, the plan
restates the spec, the review re-checks the diff against both. `s234-D1`'s design principle says
rules up a chain are valid when the chain GENERATES and a defect when it COPIES — *"Never the same
fact twice."* So the playbook does not port. **What ports is its second half**: the deterministic
tier (hooks, bands, gates), the honest advisory/deterministic split, and one structural move
Memento is missing entirely — a breached band writing an artefact that re-enters the loop.

**Three things the conductor must not skim.** (1) The nearest structural rhyme to Memento in the
whole document is **Stage 6, not Stage 1** — `bands.yaml` is the context gauge with the loop
closed. (2) **Apollo has no hooks.** `.claude/` holds `agents/` and nothing else; every
deterministic rule Memento owns fires at commit or CI time, never at the moment the agent acts —
which is exactly where the two rules that break most often would bite. (3) **Target 3 is already
occupied.** `apollo-spider/skills/grill-me/` ships a first-phase brief skill with a template and a
`briefs/` home that `generate-from-canon` reads at step 0; the playbook's opening move arrives as
a *second* route, and this report shows it beside two others as Dave asked.

COUNTS: practices 12 · ADOPT/ADAPT/REJECT per target = 1/9/2 · 3/8/1 · 2/4/6 · non-transfers 8 · collisions 5 · first-phase options 3 · ideas 10 · findings 14 · ruling-shaped 6 · UNPROVEN 5

## What was done

Region by region, in the brief's order.

- **GROUND FIRST** — `knowledge/_RUNBOOK-capture-ritual.md` (first 80 lines) · `MODEL-ROUTING.md`
  (first 60) · `notes/_briefs/2026-09-02-234-v106-brief.md` (first 70) ·
  `notes/_subreports/2026-09-02-235-L1-receipt-gate.md` §VERDICT · the Apollo framing grep (home
  found: `_LIVE-STATE.md:296-303`) · `apollo-spider/` top level · `git log --oneline -15` · the ADR
  index (`docs/decisions/`, ADR-0001…0017) · `knowledge/_rulings.json` (311 rows; `s192-D1`,
  `s200-D1`, `s204-D1`, `s215-D3`, `s218-D7`, `s234-D1`, `s235-D1`, `s235-D2` pulled by id).
- **Deliverable 1** — the playbook in our words, below, with a fetched receipt per row.
- **Deliverable 2** — the 12 × 3 borrow matrix, below, and machine-readable at
  `notes/_subreports/assets/2026-09-02-236-R2-sdlc-playbook/borrow-matrix.json`.
- **Deliverables 3–6** — non-transfers, collisions, the three first-phase options, ideas.
- **Files written** (three, all inside `notes/_subreports/`, per the DO NOT RULE fence):
  this report · `assets/2026-09-02-236-R2-sdlc-playbook/borrow-matrix.json` ·
  `assets/2026-09-02-236-R2-sdlc-playbook/fetch-receipts.json`. **No other repo file changed. No
  git commands run.**

---

## 1 · THE PLAYBOOK, IN OUR WORDS

**What it is.** A guide published 21 August 2026 by Anthropic's Applied AI team (author Louis
Claxton) plus a free 14-lesson Claude Academy course of the same name. Its audience is stated
plainly: engineering, platform and security leads at large, *regulated* enterprises — the course
page says the situation it exists for is one where *"the review queue cannot be allowed to build
and code cannot ship under-reviewed"*
([academy.claude.com/courses/ai-native-sdlc-playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook)).
Its premise is that agents collapsed the build stage and left the human-speed stages on either
side of it as the constraint.

**The shape.** Six stages — Plan, Design, Build, Test, Deploy, Maintain — arranged not as a line
but as a loop: *"the process becomes a loop, and AI is embedded at each point"*
([intro](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction)). Twelve
**plays** hang off those stages, each with the same five parts: what changes · getting started ·
how to execute it · governance considerations · how to measure it. Adoption order is a
**dependency graph, not the stage order** — the course figure is described in alt-text as a
*"Dependency graph of the twelve plays in five rows"*, with six plays needing no prerequisite at
all (intro, same URL).

**The spine, and it is one sentence.** Every stage ends by committing a file and the next stage
begins by reading it — *"Each stage ends by writing one to version control"*
([blog](https://claude.com/blog/the-ai-native-sdlc-playbook)) — so the commit history *is* the
audit trail. That, not the six stages, is the thing the playbook is actually arguing for.

### The twelve plays

| # | stage | play, in our words | receipt (≤15 words, fetched) |
|---|---|---|---|
| 1 | Plan | The originator states the want in their own words; Claude turns it into a short committed file; the product owner corrects and accepts it. | *"Claude synthesizes pain points straight from the sources and captures them within intent.md"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 2 | Design | Requirements and design stop being two phases; one session produces a spec, constrained by the org's skills, with concerns flagged for their policy owner. | *"Requirements and design compressed into one working session with an agent"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 3 | Build | Nothing is written until a plan naming files, order and proof is approved; the plan is committed and later checked against the diff. | *"Nothing is implemented without an accepted plan."* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 4 | Build | The repo's rails file carries what a new joiner needs; it is short, versioned, and grows only from repeat mistakes. | *"When Claude makes a mistake twice, the correction goes into CLAUDE.md"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 5 | Build | Institutional policy becomes skills — versioned, centrally updated — and the playbook is honest that this tier does not bind. | *"A skill is a control, though an advisory one."* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 6 | Build | One person runs several sessions in isolated worktrees, and recurring jobs become subagents with their own context and tool limits. | *"Two or three sessions is a sensible starting point."* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 7 | Test | Every session is given a way to check its own work before a human sees it — and the check itself is protected from the agent fixing the code. | *"an agent fixing code must not be able to weaken the check"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 8 | Test | A suite of 20–50 real tasks regression-tests the agent's *configuration*, triggered by any change to it. | *"Continuous evals woven through implementation"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 9 | Deploy | Review runs both ways, to a written policy with named passes and a nit cap; approval stays human and structurally separate. | *"the agent that wrote the code has no way to approve it"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 10 | Deploy | Hooks are the deterministic layer under the advisory one; they allow, ask, or block *as the agent acts*, and the non-negotiable ones are admin-owned. | *"Governance is enforced as the AI acts, with hooks as approval gates"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 11 | Deploy | The agent runs non-interactively in the pipeline, sandboxed, with deployment exposed as scoped tools and autonomy tiered per environment. | *"The agent may act up to the production gate and cannot pass it"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |
| 12 | Maintain | A deterministic script watches a metric, and a breach of a named band invokes the agent at a tiered permission — whose finding re-enters the loop as a new intent file. | *"detection stays entirely deterministic, with no model involved"* — [blog](https://claude.com/blog/the-ai-native-sdlc-playbook) |

**Four sections in the blog are NOT plays** and have no course lesson: *auto mode* (a sub-move of
play 3), *hooks as build-time guardrails* (folded into play 10), a sidebar on legacy systems as the
source of truth, and two Stage-6 product sections (scheduled codebase scans, and Claude in a chat
channel). The legacy-systems sidebar is the one worth carrying: it says name **one** system as the
source of truth per artefact and let everything else hold a copy or a link — which is ADR-0017
under another name, arrived at independently.

**Roles it assumes.** Product owner · engineer · tech lead / architect · platform engineer ·
security lead · release manager · service owner / on-call. **Seven.**

**Tooling it assumes.** Git with branch protection and PRs · a CI platform · worktrees ·
`.claude/` config (settings, hooks, agents, skills) · managed/MDM settings · MCP servers for
deployment · a metrics store · an incident tracker · OpenTelemetry export.

**Closing line, quoted because it is the governing idea:** *"The loop keeps running. Human
judgement stays above it."*
([blog](https://claude.com/blog/the-ai-native-sdlc-playbook))

---

## 2 · THE BORROW MATRIX

**Vocabulary.** `ADOPT` = take as written · `ADAPT` = take *with the named change* (a cell with no
named change is a REJECT written politely — the brief's own pitfall) · `REJECT` = don't ·
**(ALREADY)** = Apollo runs this today; the cell says what the reading adds, if anything.
**Nothing here is ruled.** Machine-readable twin:
`notes/_subreports/assets/2026-09-02-236-R2-sdlc-playbook/borrow-matrix.json`.

| # | play | **M · Memento** | **D · the packs as releases** | **P · Discover, one option of a few** |
|---|---|---|---|---|
| 1 | intent.md | **ADAPT** — briefs are a PLAN, not an INTENT; Dave's own words are a prose convention, not a parsed field. *Change:* make the "Dave's words" block a named field the wrap asserts. Sits beside `notes/_briefs/` (160 files) and capture-ritual step 1. | **REJECT** — a release is triggered by a ruling (`s234-D1`), not a file; an intent artefact per release is a second home for one fact. | **ADAPT** — this IS the Discover option. *Change:* it arrives as a second route beside `apollo-spider/skills/grill-me/brief-template.md`, never as a replacement. |
| 2 | requirements+design → spec | **REJECT** — no requirements/design split exists here to collapse; the brief already is the collapsed artefact. | **ADAPT** — the v1.0.6 brief IS the spec. *Change:* make its `STILL DAVE'S` list **blocking** — no lane opens while its own rows are unanswered. | **ADAPT** — the generator reads the brief but emits no reviewable spec before pixels. *Change:* a one-screen spec the designer accepts before `generate-from-canon` runs. |
| 3 | plan mode → plan.md | **ADAPT** — the plan exists; the plan-vs-outcome **diff** does not. *Change:* the wrap asserts each brief region against the report's "What was done". | **ADAPT** — L1–L5 is an ordered plan with no committed record of departures. *Change:* a departing lane records the departure in the same commit. **See COLLISION 2.** | **ADOPT** — plan-before-build is already Apollo's own rule (`feedback-mock-the-readings-before-building`); nothing to change. |
| 4 | CLAUDE.md | **ADAPT (ALREADY)** — no root `CLAUDE.md`; `AGENTS.md` + `MEMORY.md` are the analogue and the twice-wrong rule is already Memento's. *Change:* swap the "under a page" heuristic for the **measured** boot band. | **ADAPT (ALREADY)** — the pack ships `CLAUDE.md` and `AGENTS.md`. *Change:* none here; the pack's gap is the behaviour contract, so the effort belongs in L2. | **REJECT** — writing the designer's own rails file is not a first-phase move. *(Floated separately as idea 9.)* |
| 5 | skills as policy | **ADAPT (ALREADY)** — `dave-voice` exists. The clause worth taking is the honest one: a skill is advisory and needs something deterministic behind it. *Change:* write the pairing rule down — every skill rule that must hold **names its gate**. **See COLLISION 3.** | **ADOPT (ALREADY)** — six shipped skills, versioned as releases, Dave-ratified. | **ADOPT (ALREADY)** — `grill-me` and `generate-from-canon` are this play at product level. |
| 6 | parallel sessions + subagents | **ADOPT (ALREADY, and further along)** — delegation by default (#57), filed reports (`s218-D7`), adversarial verifier at a different seat (`s204-D1`, `s215-D3`), `.claude/agents/` × 3. | **ADAPT** — lanes share one tree and reconcile by hand. *Change:* run L1–L3 in **git worktrees** so lane collisions are structural, not clerical. | **REJECT** — a designer running three parallel sessions is not a first-phase move. |
| 7 | feedback loop | **ADAPT** — the loop exists (49 gates + `_checkin.py`); the clause **absent** is that the loop must be protected from the thing it grades. *Change:* a lane may not edit the gate it is graded by — a wrap check. | **ADOPT (ALREADY, and stronger)** — the pack ships the loop *to the customer* with an honest refusal code (exit 77, `COULD-NOT-ASK`). | **ADAPT** — `check-with-gates` is the mechanical loop; the **visual** loop is missing. *Change:* add a mock-diff round to the three browser gates. |
| 8 | continuous evals | **ADAPT** — `_recall_probe.py` is a blind eval of the seat; 29 of 49 gates carry `--selftest`. Missing half is the **trigger**. *Change:* run the regression on any change to `MEMORY.md` or a skill. | **ADAPT** — nothing regression-tests the *pack's behaviour*, which is precisely the #233 finding. *Change:* freeze Dave's cold tests as the 20–50 real tasks. | **REJECT** — a factory concern; a designer's first phase does not run evals. |
| 9 | PR review loop / REVIEW.md | **ADAPT** — `_REVIEW-SIGNOFF.md` (265KB) has no severity vocabulary, so everything reads at one weight. *Change:* take REVIEW.md's **shape** only — named passes, an Important-vs-Nit line, a nit cap, a do-not-report list. | **ADAPT** — the pack's review policy is implicit across six skills. *Change:* one written policy file naming what an Apollo review must check, shipped in the pack. | **REJECT** — review is **Craft**, phase 3 (`_LIVE-STATE.md:299`), not the first phase. |
| 10 | hooks as gates | **ADAPT** — **no hooks exist.** The deterministic layer runs at commit/CI time, never at tool-call time. *Change:* express the two most-breached rules as `PreToolUse` hooks, where they would actually bite. | **ADOPT (ALREADY, arguably better)** — a gate is *deleted honestly* rather than hidden behind `continue-on-error`. | **ADAPT** — the a11y floor is described as a mode **setting** an admin tunes, not as a gate that runs. *Change:* express the non-removable floor as a hook — and note it spans all four phases, not just Discover. |
| 11 | CI/CD + tiered autonomy | **REJECT** — Memento deploys nothing; its release is a commit and a push at wrap. Environment tiers have no referent. | **ADAPT** — CI runs the gates, but a **HOLD lives only in a ruling** and the build cannot see it. *Change:* a release-authorisation file `build-designer-pack.sh` reads, so `HELD` is machine-checkable. | **REJECT** — Dispatch, phase 4 (`_LIVE-STATE.md:301`), not Discover. |
| 12 | closing the loop (bands) | **ADAPT** — the closest structural rhyme in the document. *Change:* a band breach **mints a row**, not only a wrap. Sits beside `_checkin.py`, `_gauge_tokens.py`, `_recall_probe.py`. | **ADAPT** — the findings register exists but the loop deliberately does **not** close: promotion is Dave-only. *Change:* take step 7 only — when a fix ships, add the eval for its class. | **REJECT** — no production to monitor in a design task's first phase. |

**Totals.** M = 1 ADOPT / 9 ADAPT / 2 REJECT · D = 3 / 8 / 1 · P = 2 / 4 / 6.

---

## 3 · WHAT DOES NOT TRANSFER, AND WHY

A design-system factory is a generator, a wall of gates, and one human ruler. Eight assumptions in
the playbook break against that shape.

1. **Seven roles, one Dave.** Every governance clause routes a decision to a *different* person —
   the tech lead sets the threshold, the policy owner signs the skill change, the release manager
   authorises production. Here they collapse onto one person, so the playbook's stated guarantee
   at review — that the writer cannot approve — has no organisational mechanism.
   **What Memento does instead:** separation by **seat and by time** — an adversarial verifier at a
   different seat (`s204-D1`; `s215-D3` makes it model-conditional), and `_rulings.json` as the
   record of who ruled what and when.
2. **PR flow and branch protection.** The playbook's strongest control is that everything the agent
   writes arrives as a PR with no route to main. This repo commits and pushes to **master**
   directly (`knowledge/_RUNBOOK-git-commit.md`; memory hook `git-push-method`). There is no PR to
   attach a review to. **Instead:** `_capture_gate.py` at commit time, plus the read-back-the-
   subject assert at every wrap.
3. **The test pyramid.** There is no unit/integration/e2e ladder. Apollo's tests are **gates over
   artefacts** — 49 `_validate_*.py` — and a gate's own unit test is its `--selftest` (29 of 49
   carry one). The play's "wrap it in one `make test`" has a real analogue in
   `apollo-spider/ci-template/run-gates.py`; "write the failing test first" maps onto the
   mutation-proof discipline; the pyramid itself does not exist.
4. **Deployment targets.** No dev/staging/production. The "environments" here are **pack
   versions** — v1.0.4 ratified, v1.0.5 held, v1.0.6 building — and the gate is Dave's cold test on
   a proving zip, not a release manager on a change ticket.
5. **Code-review culture.** The playbook assumes the review object is a **diff**. Apollo's review
   object is a **rendered page seen by eye** (`review-layer-product-feature`,
   `feedback-review-live-variant-spread`). Every "the reviewer reads the change" step needs
   re-founding on a render, not a patch.
6. **Policy ownership outside the repo.** Skills are said to be written from "the policy owner's
   source of truth". Apollo's policies **are** the repo — canon, tokens, ADRs — and promotion into
   them is ruled Dave-only (`knowledge/_DS-IMPROVEMENTS.md` § Governance, RULED 2026-07-03).
7. **Telemetry.** Every one of the twelve "how to measure it" halves reads a system Apollo does not
   have: the OpenTelemetry export, PR metadata, an incident tracker, DORA. **12 of 12 measurement
   halves are unavailable as written.** The only real instruments on Apollo's own process are the
   token gauge and the recall probe.
8. **The bottleneck premise itself.** The playbook's whole argument is that build collapsed and the
   human-speed stages around it became the constraint. Here the constraint is **Dave's eye**, which
   is not a process step waiting to be automated — it is the acceptance function of the product.
   **Instead:** Memento spends the window *buying decisions* (landmarked chunks, mocked readings,
   live controllers, priced deferments) rather than speeding stages.

---

## 4 · COLLISIONS WITH EXISTING RULINGS

Raw, as the brief asked. A collision is a finding, not a defect.

1. **★ The artefact chain is a COPY chain — `s234-D1`'s design principle.** The playbook's proudest
   structure has the spec restate the intent, the plan restate the spec, and the review re-check
   the diff against both. The v1.0.6 brief rules: *"rules up the whole chain are VALID when the
   chain is a GENERATION chain and a DEFECT when it is a COPY chain. One home, derived consumers,
   one gate. Never the same fact twice"*
   (`notes/_briefs/2026-09-02-234-v106-brief.md`, the D4–D6 design principle). Adopting the chain
   wholesale re-opens the principle that #234 was built on. *(This is why the matrix borrows the
   playbook's deterministic tier and not its artefact ladder.)*
2. **A live `plan.md` vs write-once — ADR-0017 / `s192-D1`.** Play 3 step 7 says that when
   implementation departs from the plan, `plan.md` is updated in the same commit. `s192-D1`
   promoted WRITE-ONCE to ADR-0017: live facts get one home, history gets frozen copies — and
   `notes/_subreports/_TEMPLATE.md` states *"Reports are dated HISTORY (ADR-0017 / `s192-D1`)"* and
   are not re-edited by later sessions. **Briefs are not explicitly named by that rule**, so this
   is an open edge rather than a settled conflict — and the D-column cell in row 3 sits exactly on
   it. Whether a brief is history or a live fact is Dave's (question 2 below).
3. **The advisory-control tier vs "an instrument without a consumer".** The playbook accepts an
   advisory tier as a legitimate control: *"A skill is a control, though an advisory one"*
   ([blog](https://claude.com/blog/the-ai-native-sdlc-playbook)). Apollo has ruled the other way
   repeatedly (`instrument-without-a-consumer`, `feedback-gate-dont-patch`), and #234's own rB lane
   found the cost live: **59 BLOCKING guideline rules in `_rules-index` with no consumer**
   (`notes/_briefs/2026-09-02-234-v106-brief.md`, rB summary). Importing the advisory tier as
   written legitimises the exact class Apollo fenced. *(The playbook's own answer — pair every
   must-hold skill with a hook — is the reconciling clause, and it is what row 5/M borrows.)*
4. **Automatic skill-version pickup vs `s234-D1` HELD.** Play 5 step 6 has engineers pick up a new
   skill version automatically in their next session. `s234-D1` holds v1.0.5 on Dave's word — *"it
   waits for 06"* — with the hold recorded in `_rulings.json` and nowhere a build can read it.
   Auto-pickup, adopted as written, ships a held version. *(Row 11/D's release-authorisation file
   is the fix.)*
5. **"Keep it under a page" vs a measured boot band.** Play 4 caps the rails file by page count.
   Apollo measures its boot instead (`knowledge/_gauge_tokens.py`; `boot-floor-measured-109`:
   read the constant, never a hook figure) and deliberately structures `MEMORY.md` as an index with
   overflow files. A page-count heuristic where a measurement exists is `measure-dont-convert-units`
   in miniature.

---

## 5 · THE DISCOVER OPTION, SKETCHED — beside two alternatives

Dave's framing: *"one of a few options for the first phase of a design task."* Three options,
sketched at the same grain so they can be compared. **Sketch only; nothing built, no UI.**
Option B is not hypothetical — it is what the pack ships today.

### Option A — the INTENT route (the playbook's opening move, ported)

- **Inputs:** the designer says, in their own words, what they cannot do today, who is affected,
  what better looks like, what is out of scope. No form, no vocabulary.
- **The move:** Apollo asks the questions an analyst would — scope, users, constraints, success —
  until the ask is concrete, then writes it back as a short file the designer *corrects*.
- **Output:** `intent-<task>.md` — problem · proposed outcome · affected users and surfaces ·
  constraints · open questions. Dated, authored, in the project.
- **How long:** ~10 minutes of conversation; the file is a screen.
- **What it hands to Create:** a stated *problem* and a stated *out-of-scope*, which is the one
  thing the grill brief does not capture — the grill asks how it should look, not what it is for.
- **Cost:** a second artefact in the project, which is where collision 1 bites. It is only worth it
  if the intent **generates** the brief rather than sitting beside it.

### Option B — the GRILL route (SHIPPED; `apollo-spider/skills/grill-me/`)

- **Inputs:** six standard questions that decide expensive things — theme, light/dark, density and
  width, brand assets, data, and what is fixed or off-limits — then open discovery, one question at
  a time, until the brief is exhausted.
- **The move:** any question may be skipped, and *a skipped question is written down as skipped*;
  a default is announced out loud before anything is built.
- **Output:** `briefs/<date>-grill.md` on `brief-template.md`'s shape — the six rows, plus
  `Skipped:`, `Defaults used:` and `Notes:` in the designer's own words.
- **How long:** the skill says about two minutes for the six, then unbounded discovery —
  deliberately uncapped, because *a cap would end the questioning at the cap, not at the brief*.
- **What it hands to Create:** `generate-from-canon` reads it at step 0 and **cites** which brief
  and which rows it used (`generate-from-canon/SKILL.md:129–130`).
- **Cost:** it captures *how it should look*, not *what problem it solves* — the gap Option A fills.

### Option C — the PATTERN-FIRST route (the retrieval-native one; not built)

- **Inputs:** the designer names the surface ("a treasury overview for corporate banking") and
  Apollo *retrieves* two or three real assemblies from canon rather than asking anything.
- **The move:** the designer reacts to something concrete — keep this, drop that, wrong density —
  and the brief is **derived from the reactions**, not elicited before them.
- **Output:** the same `briefs/*-grill.md` shape, minted from the accept/reject trail, with a
  provenance line naming the specimens shown.
- **How long:** ~5 minutes, because reacting is faster than specifying.
- **What it hands to Create:** a brief whose every row already has a *rendered* precedent, so the
  first generation starts from an accepted reference rather than an interpretation.
- **Cost:** it needs a retrieval set good enough to show three plausible starts on demand; and it
  is the only one of the three that could put the wrong thing in the designer's head first.

**How they relate, in one line:** A asks *what for*, B asks *how it should look*, C asks *is this
it*. They are not exclusive — A→B is a sequence, and C could feed either.

---

## 6 · IDEAS FOR OTHER TASKS

One line each, with what it depends on. None of these is in scope for #236.

1. **A hook layer for the two rules that break most** — `git add -A` and the skipped wrap, as
   `PreToolUse` hooks. *Depends on:* creating `.claude/settings.json`; nothing exists today.
2. **Freeze Dave's cold tests as an eval suite over the pack.** *Depends on:* the v1.0.6 behaviour
   contract landing (L2), so there is behaviour to assert.
3. **A release-authorisation file the pack build reads**, so `HELD` is a state a machine sees.
   *Depends on:* nothing — one file plus a check in `build-designer-pack.sh`.
4. **A severity vocabulary for reviews** — Important / Nit / do-not-report — for
   `_REVIEW-SIGNOFF.md` and for sub-reports. *Depends on:* Dave ruling the passes.
5. **Lane worktrees for v1.0.6 L1–L3.** *Depends on:* nothing; retires the reconcile-by-hand class.
6. **"You may not edit the gate you are graded by."** *Depends on:* nothing; it is a wrap check.
7. **Close the gauge loop** — a band breach mints a row, not only a wrap. *Depends on:*
   `_checkin.py`'s output shape.
8. **A visual feedback round for the product** — screenshot vs the approved mock. *Depends on:* the
   three browser gates already in the pack.
9. **Ship a rails-file writer as a pack skill**, so a designer's project gets its own
   `CLAUDE.md`/`AGENTS.md`. *Depends on:* nothing.
10. **Apollo's own "shifts" table** — traditional design-system work vs AI-native — as pack framing.
    *Depends on:* the standing positioning rule (public copy stays abstract, never gate mechanics).

---

## Findings

Each carries its probe.

1. **The blog fetched whole and the course is FREE.** No paywall, no sign-in wall on lesson
   content. Probe: `mcp__workspace__web_fetch` on the course root returned the full lesson index
   and learning objectives; `.../capture-intent` returned the complete lesson body. The only gated
   affordance on the page is "Sign in to save progress".
2. **The course adds one thing the blog does not: the dependency graph in words.** The blog shows
   it as an image with a caption; the course's alt-text enumerates it — *"Dependency graph of the
   twelve plays in five rows"*, six plays with no prerequisites, dotted arrows for "helps but not
   required". Probe: the `introduction` fetch.
3. **Twelve plays, not six stages, is the unit of adoption.** Probe: same alt-text, and the course
   index lists exactly twelve play lessons plus intro and closing = 14.
4. **The playbook's real thesis is the committed artefact, not the stage model.** Probe: blog
   line 453 and the identical paragraph in the course intro — *"Each stage ends by writing one to
   version control"*.
5. **That artefact chain is a COPY chain and collides with `s234-D1`.** Probe: the v1.0.6 brief's
   design principle, quoted in COLLISION 1.
6. **Apollo has NO hooks.** Probe: `ls -a .claude/` → `.`, `..`, `agents` — and only three agent
   definitions inside (`opus-fast.md`, `dreamer.md`, `opus-deep.md`). No `settings.json`, no
   `hooks/`. Every deterministic rule fires at commit or CI time.
7. **The nearest structural rhyme to Memento is Stage 6, not Stage 1.** `bands.yaml` — a
   deterministic detector, a rolling baseline, tiered responses by σ, no model in the detection —
   is the context gauge with the loop closed. Probe: `knowledge/_checkin.py`,
   `knowledge/_gauge_tokens.py`, and `_recall_probe.py`'s own docstring: *"One miss CLOSES the band
   for that session and judgment work stops immediately."*
8. **Apollo's release discipline is ahead of the playbook's on one axis: honest refusal.**
   `apollo-spider/ci-template/gates.yml` header: a gate exits 77 with `COULD-NOT-ASK:` and that is
   a refusal, not a failure — and turning a check off means **deleting its step**, never
   `continue-on-error`. The playbook has no equivalent vocabulary.
9. **Target 3 is already occupied by a shipped skill.** Probe: `apollo-spider/skills/grill-me/`
   contains `SKILL.md` and `brief-template.md`; `generate-from-canon/SKILL.md:129–130` reads the
   newest `briefs/*-grill.md` and cites it. The playbook's opening move is a *second* route.
10. **The grill and the intent capture different things.** The grill's six questions are theme,
    light/dark, density/width, brand assets, data, fixed-and-off-limits — all *how it should look*.
    `intent.md`'s five headings are problem, proposed outcome, affected users and systems,
    constraints, open questions — all *what it is for*. Probe: `brief-template.md` rows 1–6 vs the
    blog's intent example.
11. **12 of 12 measurement halves are unavailable as written.** Every play's leading and lagging
    indicators read OpenTelemetry, PR metadata, CI history or an incident tracker. Probe: the "How
    to measure it" block of each play in the fetched article; and `.github/workflows/gates.yml` is
    the repo's only CI, running gates — it emits no such series.
12. **29 of 49 gates carry a `--selftest`.** Probe: `grep -l -- "--selftest" knowledge/_validate_*.py | wc -l`
    → `29`; `ls knowledge/ | grep -c _validate_` → 49 gate files. This is the eval-analogue, and it
    tests gates, not the pack's behaviour.
13. **The playbook independently reinvents ADR-0017.** Its legacy-systems sidebar says name one
    system as the source of truth per artefact, everything else holds a copy or a link. That is
    write-once/one-home arrived at from a different direction — a corroboration, not a collision.
14. **The playbook is explicit that skills do not bind, and pairs each must-hold skill with a
    hook.** This is the single most directly importable idea in the document and it needs no
    adaptation to Apollo's vocabulary — it is `feedback-gate-dont-patch` stated by someone else.

## RULING-SHAPED QUESTIONS

1. **Does anything from the playbook's artefact chain enter Apollo at all, given collision 1?**
   (a) Nothing — take only the deterministic tier (hooks, bands, the advisory/deterministic pairing)
   and leave the intent→spec→plan ladder alone. (b) One artefact only — the *intent*, and only if it
   **generates** the brief rather than sitting beside it. (c) The whole ladder, accepting the copy
   chain for the product even though the factory rejects it.
   **Recommend (b)**, because it is the only version that survives `s234-D1` — but the generation
   has to be real, not a convention.
2. **Is a `notes/_briefs/*.md` file HISTORY or a LIVE fact?** (a) History — frozen at write, like a
   sub-report, and a departure lands in the report instead. (b) Live — amendable in the same commit
   as the departure, per play 3 step 7. The template rules reports are history and is silent on
   briefs. **Recommend (a)** for consistency with ADR-0017, with the departure recorded in the
   filed report. This is Dave's because it changes how every lane closes.
3. **Which first-phase option, and is it a menu or a sequence?** A (intent) · B (grill, shipped) ·
   C (pattern-first). **Recommend: B stays the default, A is offered when the designer cannot yet
   say what the thing is for, C is the research build.** But "menu vs sequence" is a product
   decision, not a research one.
4. **Do hooks enter Memento at all?** (a) Yes — start with two `PreToolUse` hooks for the two
   most-breached rules. (b) No — commit-time gating is the ruled posture and a tool-call hook is a
   new enforcement surface with its own failure mode. **Recommend (a) as a trial on two rules
   only**, because the class it catches (`git add -A`, the skipped wrap) is the class that has cost
   the most sessions.
5. **Does `HELD` become machine-readable?** A release-authorisation file the pack build reads would
   make `s234-D1` checkable rather than remembered. Cheap; but it creates a second home for a fact
   whose home is `_rulings.json`, so it must be **derived** from the store, not typed.
   **Recommend: derive it.**
6. **Do Dave's cold tests become a frozen eval suite?** (a) Yes, after L2 lands. (b) No — the cold
   test's value is that it is *cold*, and freezing it turns it into something the generator can be
   tuned against. **Genuinely two-sided; recommend (a) for the mechanical arms only**, keeping
   Dave's eye unfrozen.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** *That the other twelve academy lessons match their blog sections.* Two of fourteen
  were fetched and found equivalent (light copy-edit only); the rest are assumed. Price to prove:
  ~12 fetches.
- **UNPROVEN:** *What Dave actually watched.* The blog and course link no video; a search surfaced
  a third-party YouTube explainer that was **not** opened and is **not** Anthropic's. Nothing in
  this report is sourced from a video. Price: Dave names the link.
- **UNPROVEN:** *That no hook layer exists anywhere on this machine.* The probe covers the **repo**
  (`ls -a .claude/` → `agents` only). User-level (`~/.claude/settings.json`) and managed settings
  were not probed and are outside the repo. Price: one `ls`, but outside this lane's fence.
- **CLAIMED:** *That `apollo-spider/CLAUDE.md` and `AGENTS.md` play the rails-file role.* Their
  **existence** is probed (`ls apollo-spider/` lists both); their **contents** were not read.
  Re-read costs ~3–4K.
- **UNPROVEN:** *Whether ADR-0017 itself covers briefs.* The write-once statement quoted is from
  `notes/_subreports/_TEMPLATE.md`, which speaks about **reports**. `docs/decisions/ADR-0017-write-once-live-facts.md`
  was located but not read. Price: ~1.5K. This is what makes question 2 a question.

## Evidence

`notes/_subreports/assets/2026-09-02-236-R2-sdlc-playbook/` —
**`borrow-matrix.json`** (the 12 × 3 matrix machine-readable: verdict, why-clause, named change,
and the Apollo file/gate/ruling each cell sits beside; totals block for the counts line) and
**`fetch-receipts.json`** (every URL retrieved with its size and verdict, every URL *not*
retrieved with the reason and the price of proving it — including the twelve unfetched lessons and
the unidentified video).

REPLAY-THESE: `notes/_subreports/2026-09-02-236-R2-sdlc-playbook.md` §2 the borrow matrix (~2,600 tk — the 36 cells are the deliverable and do not compress) · §4 COLLISIONS, all five (~700 tk — collision 1 decides whether anything is borrowed at all) · §5 the three first-phase options (~900 tk — Dave rules the menu) · `assets/…/borrow-matrix.json` (~2,900 tk — only if a gate or a later lane needs the cells parsed rather than read)
