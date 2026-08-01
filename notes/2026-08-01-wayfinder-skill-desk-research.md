# `/wayfinder` (aihero.dev / mattpocock) — desk research on its claims, and what Memento can take

**Date:** 2026-08-01 (stamped from `date`, 17:05 BST) · **Register: FLOATED — desk research. Nothing ruled, nothing enacted, no gate touched.**

```
provenance: notes/_receipts/2026-08-01-wayfinder-research-worker.md · 2026-08-01
status: floated
```

**Origin:** Dave, opener verbatim: *"I want you to research something for memento. take a look at this and do some desk research around its claims. https://www.aihero.dev/skills-wayfinder — leave receipts for another window to pick up for the commit."*

**Context gauge at authoring: 🟡 AMBER ~48% — ESTIMATE, NOT A MEASUREMENT.** No addressable handle exists for a running parent session ([[cowork-gauge-transcript-crack]], #68 DISPROVEN), so the denominator is Dave's 200K and the numerator is my own count of what entered the window (system + memory index + 7 fetches). Per [[feedback-measuring-tool-must-not-guess]] the gap is **declared, not defaulted**: treat every number in this note as re-checkable, and re-measure before building on §4.

**Path:** this note + its receipt. **No** `_MEMENTO-DECISIONS.md` entry, **no** `_FUTURE-STATE.md` entry, **no** §C queue edit — nothing here is ruled, and per [[feedback-dont-launder-a-premise-into-a-ruling]] a survey does not get to write into the ledger.

---

## ⛔ CORRECTION LOG — 2026-08-01, same window, ~1 hour after first draft

**Trigger:** Dave posted the repo URL — `https://github.com/mattpocock/skills/tree/main` — with no comment. Per [[silent-lookup-failure-class]] (*contradicts what Dave SAW ⇒ suspect the measurement*) that was read as a signal to re-probe, not as agreement.

**What the re-probe found: my fetch layer, not his repo, was the stale thing.**

| Probe | Result |
|---|---|
| `api.github.com/repos/mattpocock/skills` | `pushed_at: 2026-05-20`, `updated_at: 2026-05-21` — **a ~2.5-month-old snapshot** |
| `api.github.com/.../contents/skills/engineering` (a *different* endpoint) | same old skill set, no `wayfinder`, no `research` |
| `raw.../main/skills/engineering/to-spec/SKILL.md` (a file that can only exist post-v1.1) | ✅ **exists, current content** |
| `raw.../main/skills/engineering/to-prd/SKILL.md` (its pre-v1.1 predecessor) | ✅ **also resolves — and returns the OLD May-era body** |
| `aihero.dev/skills.md` changelog | **v1.1 "/wayfinder, /to-spec, /to-tickets" released Jul 8 2026**; v1.0 Jun 18 2026 |

**Diagnosis (now well-evidenced):** the fetch layer serves **per-path caches of different ages**. A path that existed when the cache filled (`README.md`, `to-prd`) returns a **stale May body**; a path created afterwards (`wayfinder`, `research`, `to-spec`) has no cache entry and returns **fresh**. Both arrive through the same channel, indistinguishably.

**Consequence: §5 of this note is RETRACTED.** Its rewritten replacement is below. §2, §3, §4, §6 and §7 **survive** — see §5 for why each does.

---

## §0 — Exec summary

`/wayfinder` is a planning skill: it turns a too-big, too-foggy effort into a **map issue** on your tracker whose child issues are **decisions to settle** (not slices to build), and resolves them one per session until nothing is left to decide. It is a good, well-written artefact and it is **built on the same premises Memento is built on** — an index that is not a store, a frontier, an explicit register of what you cannot yet specify.

Four things came out of the desk check that are worth Dave's time:

1. **The published page is not the skill.** Three load-bearing mechanisms appear on aihero.dev that are **absent from the `SKILL.md` an agent actually installs** — the research-subagent, the "research tickets excepted" carve-out on the one-ticket-per-session rule, and the throwaway `research/<name>` branch. If we cite wayfinder, cite the `SKILL.md`, not the page. §2, §3.
2. **Its two hard caps are picked, not derived** — "sized to one 100K token agent session" and "never more than one ticket per session" — and the same repo has a written, reasoned refusal to pick a cap in a neighbouring case. This is [[m8-cap-at-its-own-floor]] arriving from outside. §4.
3. ~~**The sharpest finding is accidental.** The repo's `README.md` doesn't mention `wayfinder`…~~ ⛔ **RETRACTED — it was my instrument, not his repo.** The replacement finding is better and it is about us: **three GitHub API endpoints agreed with each other and all three were 2.5 months stale.** Concordance between endpoints of one system is **one reading, not three** — and I banked it as corroboration. §5.
4. **One idea is worth stealing outright**, and it is not the map. It is the **fog-vs-ticket test**: *"whether you can state the question precisely now — not whether you can answer it now."* That is [[feedback-check-ran-never-reached-plan]] (*an honest UNPROVEN is a PRICED TODO*) derived independently, from a different direction, and it gives us a sharper *word* for the thing than we currently have. §7.

### Next steps, in order — priced, none started

| # | Step | Price | Why now |
|---|---|---|---|
| 1 | **Nothing.** Read §7 and rule whether "fog" earns a place in the fixed vocabulary. | 1 read | Cheapest possible move; the rest hangs off it. |
| 2 | Grep our corpus for a *gate* on `MEMORY.md` index↔file drift. **Survives the §5 retraction intact — it never depended on his repo.** | ~15 min, one sub | [[read-chain-is-where-staleness-is-free]] says this is exactly where staleness is free. |
| 3 | If §7's "fog" lands, add **one** row to `_FIXED-FLEX-CHARTER.md` — not a section. | small | [[gate-inside-the-growth-loop]]: shave my own additions. |
| 4 | Leave the map machinery alone. | 0 | §7.3 — we have a tracker-shaped thing already and it is called `§C`. |

---

## §1 — What was actually fetched (OBSERVED, 2026-08-01)

| # | Artefact | URL | Fetched | Status |
|---|---|---|---|---|
| A | The page under review | `https://www.aihero.dev/skills-wayfinder` | 2026-08-01 | ✅ full text; page meta `updatedAt: 2026-07-07` |
| B | **The skill itself** | `raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/wayfinder/SKILL.md` | 2026-08-01 | ✅ full text |
| C | The `/research` skill | `.../skills/engineering/research/SKILL.md` | 2026-08-01 | ✅ full text (10 lines) |
| D | Repo README on `main` | `.../main/README.md` | 2026-08-01 | ⛔ **STALE — a May body served from cache.** Do not cite. Re-fetched at `HEAD` and got the same stale body, which is *not* a second reading. |
| E | Repo tree | `api.github.com/.../git/trees/main?recursive=1` | 2026-08-01 | ⛔ **STALE — `sha b8be62f` is the 2026-05-20 snapshot.** `truncated:false` made it *look* authoritative. Do not cite. |
| F | Author's own out-of-scope note | `.../main/.out-of-scope/question-limits.md` | 2026-08-01 | ⚠️ **SUSPECT** — this path existed in May, so it may be a cached body. Content is coherent and unaffected by v1.1, but **re-fetch before repeating §4's tension**. |
| G | Prior art — Shape Up ch.5 | `basecamp.com/shapeup/1.4-chapter-05` | 2026-08-01 | ✅ via search summary, not full fetch |
| — | **Probe that returned nothing** | `api.github.com/.../commits?per_page=3` | 2026-08-01 | ⚠️ **empty response.** In the first draft this was recorded as "cause stays UNPROVEN" — correct, and then reasoned past anyway. ★ **The empty probe was the warning.** |
| H | Repo metadata | `api.github.com/repos/mattpocock/skills` | 2026-08-01 | ⛔ **STALE** — but it is what broke the case open: `pushed_at: 2026-05-20`. Star/fork counts from it are May figures. |
| I | Contents endpoint | `api.github.com/.../contents/skills/engineering` | 2026-08-01 | ⛔ **STALE**, and it *agreed* with E — the false triangulation. §5.3 |
| J | **The existence probe that settled it** | `raw.../main/skills/engineering/to-spec/SKILL.md` + `.../to-prd/SKILL.md` | 2026-08-01 | ✅ **both resolve** ⇒ the view is cached, not live. Two fetches, decisive. |
| K | **The different-well source** | `https://www.aihero.dev/skills.md` | 2026-08-01 | ✅ changelog: **v1.1 Jul 8 2026** (`/wayfinder`, `/to-spec`, `/to-tickets`), v1.0 Jun 18 2026. Also: a Claude Code plugin install path, `claude plugins install mattpocock-skills`, and a `/resolving-merge-conflicts` skill not otherwise seen. |

**Retrieval-first note.** Before searching outward I re-read our own record, per [[memento-mset-hardening]]: `notes/2026-07-29-context-degradation-research.md` §1d/§2, and `notes/2026-07-28-memento-jit-context-research.md` §4/§7. §4 and §7 of this note quote those rather than re-deriving them.

---

## §2 — The page against the skill, claim by claim

Method: every claim below is the **page's** wording, checked against artefact **B** (the `SKILL.md` an agent installs). "Quote the line" per [[unmatched-grep-is-not-an-absence]].

| Page claim | Verdict | Evidence |
|---|---|---|
| "the agent won't reach for it on its own" | ✅ **VERIFIED — mechanically** | Frontmatter: `disable-model-invocation: true`. Not prose, a flag. |
| Map is a single issue labelled `wayfinder:map`; tickets are its child issues | ✅ **VERIFIED** | *"a single issue … labelled `wayfinder:map` — the canonical artifact. Its tickets are child issues of the map."* |
| "It's an **index, not a store**" — decision lives in exactly one place, map gists and links | ✅ **VERIFIED, verbatim** | *"The map is an **index**, not a store … a decision lives in exactly one place — its ticket — so the map never restates it, only gists it and links."* |
| Refer by name, never a bare `#42` | ✅ **VERIFIED** | Whole "Refer by name" section; *"A wall of `#42, #43, #44` is illegible."* |
| Naming the destination is the first act, before any ticket | ✅ **VERIFIED** | Chart-the-map step 1; *"The destination fixes the scope, so it's settled first."* |
| Fog-vs-ticket test = can you state it precisely, not answer it | ✅ **VERIFIED, verbatim** | *"The test is whether you can state the question precisely now — **not** whether you can answer it now."* |
| Frontier = open, unblocked, unclaimed; rendered by the tracker's native blocking | ✅ **VERIFIED** | Plus a detail the page drops: *"Only a tracker that lacks native blocking falls back to a body convention."* |
| Out-of-scope work never graduates | ✅ **VERIFIED** | *"the frontier stops at the destination."* |
| No fog surfaced ⇒ stop, skip the map | ⚠️ **VERIFIED WITH A SHIFT** | Skill: *"Stop and **ask the user how they'd like to proceed**."* Page: *"stops and **tells you** the journey is small enough."* Ask ≠ tell. Minor, but it is the difference between a HITL and an AFK act — in the one skill that makes that distinction load-bearing. |
| "It **plans, it doesn't do** … produces decisions, not deliverables" | ⚠️ **TRUE BUT MIS-SCOPED — two named exceptions dropped** | The skill states the rule *and its exceptions*: (i) *"An effort can override this in its **Notes** — carrying execution into the map itself"*; (ii) the **Task** ticket type — *"This is the one type that *does* rather than decides."* The page states the rule absolutely and drops both. See §3.1. |
| Every ticket is HITL or AFK; the agent never answers its own questions | ✅ **VERIFIED** | *"a grilling agent that answers its own questions has broken this."* |
| "a session doesn't stop and read: it **fires a `/research` subagent** … in parallel" | ⚠️ **HALF-SOURCED** | The **`/research` skill** does say *"Spin up a **background agent**"* (artefact C). But **wayfinder's own `SKILL.md` says none of it** — its Research type reads only *"Creates a markdown summary as a linked asset."* The parallelism the page attributes to *wayfinder* lives in a *different* skill, and wayfinder never invokes it by that mechanism. See §3.2. |
| "A session resolves at most one ticket **(research tickets excepted)**" | ❌ **NOT IN THE SKILL** | Skill, bolded, no carve-out: *"Either way, **never resolve more than one ticket per session.**"* The exception is the page's. See §3.3. |
| "captures the findings on a throwaway `research/<name>` branch" | ❌ **NOT FOUND — three probes named** | Absent from B, C, and D. The `/research` skill says the opposite in spirit: *"Save it where the repo already keeps such notes; match the existing convention."* ⚠️ **NOT SWEPT:** `setup-matt-pocock-skills/SKILL.md` and the three `issue-tracker-*.md` docs. Per [[unmatched-grep-is-not-an-absence]] this is **"not found in the places I looked"**, not "does not exist". |

---

## §3 — The three page-only additions, and why they matter to us

### 3.1 The absolute rule that isn't absolute

The page's headline is *"It **plans**, it doesn't do."* The skill's is the same sentence followed by a **closed list of two exceptions** — a Notes-level override, and the `task` ticket type, which the skill is careful to fence: *"it earns its place by unblocking a decision, not by delivering the destination."*

That fencing is good work, and the page throws it away. It is the identical shape as [[m8-cap-at-its-own-floor]] #58: **when the floor is a closed list, name the exceptions.** The skill does. The page does not, and the page is what most people will read.

**For us:** if a wayfinder idea ever enters our canon, it enters quoting `SKILL.md`. Marketing prose is a secondary write-up, and the `/research` skill's own first instruction is *"not a secondary write-up."*

### 3.2 Parallelism attributed to the wrong artefact

The page's throughput story — fan research out to subagents, keep the frontier moving — is the bit that most resembles our own [[delegation-inversion-ruled]] (#57, subs by default). It is also the bit wayfinder does not contain. What wayfinder actually says about concurrency is much weaker and entirely human-driven:

> *"The **user** may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently."*

That is a **claim-and-race note**, not a delegation model. The claim mechanism is real and cheap (assign-before-work; *"That assignee _is_ the claim"*), and it is genuinely good — it is the same job our conductor's DIVVY PLAN does ([[feedback-parallel-conductor]]), done with one field instead of a document.

**The gap, named:** wayfinder has **no replay step**. Our #57 ruling is *"REPLAY what a sub reports"*. Wayfinder's research ticket closes on an agent's own markdown summary with nothing that re-derives it. A resolution comment written by the agent that did the research, closing a ticket the same agent claimed, is [[check-after-its-own-remedy]] wearing a ticket's clothes — **a green that cannot fail**. The skill catches this failure class precisely for HITL tickets and does not extend the catch to AFK ones.

### 3.3 The carve-out that changes the whole cost model

"One ticket per session" is the skill's only throughput discipline. The page's silent "(research tickets excepted)" is not a footnote — it is the difference between a bounded session and an unbounded one, since research is the ticket type most likely to arrive in bulk. **Whichever is right, they are not the same skill.**

---

## §4 — Two caps, picked not derived — and the author's own argument against doing that

The skill sets two hard numbers, neither with a derivation:

1. **"Its body is the question, sized to one 100K token agent session"** — a ticket-sizing cap.
2. **"never resolve more than one ticket per session"** — a session cap.

Neither is accompanied by a measurement, a unit definition (100K tokens *of which tokenizer?* — cf. [[tape-is-openai-not-claude]], where that exact question moved our numbers by ×1.559), or an instrument that could tell you at authoring time whether a ticket has breached it. **There is no gauge in the skill.** A cap with no reader is [[instrument-without-a-consumer]]: it cannot fail, so it cannot bind.

What makes this worth writing down rather than shrugging at is artefact **F** — the author's own `.out-of-scope/question-limits.md`, where he **refuses** to add a numeric cap to grilling, and gives this reason:

> *"A fixed cap would either cut off useful exploration on hard problems or feel arbitrary on easy ones … natural-language steering is the intended control surface, not a numeric limit."*

⚠️ **Scoped honestly:** these are not the same cap. His refusal governs *questions inside an open-ended dialogue*; the 100K governs *the size of a unit of work* and the 1-per-session governs *session hygiene*. Two of the three are defensible on different grounds. But **the argument form he uses to reject the first applies verbatim to the other two**, and nothing in the repo reconciles them. Per [[feedback-dont-launder-a-premise-into-a-ruling]] I am recording a **tension to test**, not a verdict.

**Where we already stand on this,** quoted rather than re-derived, from `notes/2026-07-29-context-degradation-research.md` §1d:

> arXiv 2509.21361 — *"Some top-of-the-line models failed with as little as 100 tokens in context, with most experiencing severe degradation in accuracy by 1000 tokens."* … **stated in absolute tokens, not percentages.**

and

> Chroma, *Context Rot* — 18 frontier models, **every one degrades as input grows, non-uniformly, well before the documented limit.**

So the *direction* of wayfinder's caps is well supported by the literature — an effort really can exceed what one session holds, and degradation really does start early. What is unsupported is **the number**. Our own note's verdict on exactly this pattern applies unchanged: the fraction/round-number framing *"is the paste's own"*. **100K is a round number, not a finding.**

---

## §5 — ⛔ RETRACTED, and replaced by a better finding: the stale read that wore a drift finding's clothes

### 5.1 What I claimed, and why it was wrong

I claimed the repo's `README.md` had drifted from the skills it ships — no mention of `wayfinder` or
`research`, predecessors still listed under old names — and I called it "the sharpest finding",
an index lying about its store *in the repo whose flagship skill is about indexes not lying".

**It was my fetch layer.** See the Correction Log at the head of this note for the five probes. The
decisive pair: `to-spec/SKILL.md` (v1.1, Jul 8) and `to-prd/SKILL.md` (its replaced predecessor)
**both resolve at `main`** — and `to-prd` comes back with its May body. A live tree cannot hold both.
A per-path cache of mixed ages can, and does.

**No evidence of README drift in the live repo survives.** Two further minor points built on the same
stale fetch are withdrawn with it: the "22 skills doesn't reconcile" arithmetic, and the
"README says Linear, tree says GitLab" inconsistency. Both were counted off a May artifact. The
star/fork counts quoted anywhere from that metadata are May figures too.

### 5.2 What survives, and why each

| § | Status | Why |
|---|---|---|
| §2, §3 — page vs `SKILL.md` | ✅ **SURVIVES** | `wayfinder/SKILL.md` **could not have been in the May cache** — the skill didn't exist until v1.1 (Jul 8). So that fetch was necessarily fresh. The page is dated Jul 7. Both artefacts are current-era, and the comparison is sound. |
| §4 — picked caps | ✅ **SURVIVES** on the same reasoning | "100K token agent session" and "one ticket per session" are quoted from that same fresh file. ⚠ **One downgrade:** `.out-of-scope/question-limits.md` **was** in the May tree, so my copy may be stale. The §4 tension still holds as written, but re-fetch that file before repeating it. |
| §6 — prior art | ✅ SURVIVES | Shape Up, ADRs, WIP-limits — unaffected by repo state. |
| §7 — what to take/refuse | ✅ SURVIVES | Rests on §2/§4 and on our own record. |
| §5 (this) | ⛔ RETRACTED | Above. |

### 5.3 ★ The replacement finding, and it is about us

**Three GitHub API endpoints — repo metadata, `git/trees`, and `contents` — agreed with each other
perfectly, and all three were the same 2.5-month-old snapshot.** I read that concordance as
triangulation. It was not: **agreement between endpoints of one system is one reading, not three.**
This extends a rule we already hold — [[unmatched-grep-is-not-an-absence]] (*a complete list of
MATCHES is not a complete list of SOURCES*) — to a case it doesn't currently cover: *several
independent-looking probes can share a single upstream, and then their agreement is worth exactly
one probe.*

What actually broke the tie was **a different kind of source**: the author's own changelog
(`aihero.dev/skills.md` — *"v1.1: /wayfinder, /to-spec, /to-tickets … Jul 8, 2026"*), plus a targeted
**existence probe on a file that could only exist if the new version were live**. Not more reads of
the same well — one read of a different one, and one prediction that could fail.

**Three things this costs us, in order of seriousness:**

1. **A stale read is shaped exactly like a drift finding.** "The index doesn't match the store" is the
   conclusion you reach *both* when the index is stale *and* when your view of the index is stale.
   Memento's whole job is telling current from not-current, and this failure mode produces a
   confident, well-evidenced, entirely false inscription — [[memento-framing]]'s named worst case.
   ⚠ **Ask of any drift finding: could this be my view that is frozen?** That question was never asked.
2. **I predicted this exact failure and it bit me anyway.** §9 risk 4 of the first draft reads: *"every
   convergence in §7 is one I already believed; per [[attribute-the-diff]] that is the condition under
   which a control is most needed **and I ran none**."* I wrote the risk, named the remedy, and did not
   run it — because the finding flattered a lesson I already held. [[instruction-right-cause-wrong]]:
   ★★ **documenting a defect is not immunity to it.** This is now demonstrated, not just asserted.
3. **The freshest and the stalest evidence arrived through the same channel, indistinguishably.** No
   timestamp, no warning, no failure. The only tell was a `pushed_at` field I did not read until Dave
   pointed at the repo — [[silent-lookup-failure-class]] with a new instance.

**The one control that would have caught it, cheap enough to make standing:** before reasoning about
whether a remote artefact is current, **fetch one thing whose existence the claim predicts**, and one
thing it predicts is *gone*. Both resolving means the view is cached, not live. That is a two-fetch
gate and it is the only concrete process change this note earns.

**Not enacted. Dave's to rule** — it belongs in `_RUNBOOK-*` territory if it belongs anywhere, and per
[[gate-inside-the-growth-loop]] I am not adding a section to buy back my own mistake.

### 5.4 What is left of the point I was trying to make

The *underlying* observation about wayfinder is untouched and still worth a line: its map is an index
maintained **by the agent, by hand, one append per resolved ticket**, with no generation step, no
reconcile step, and no check that a `Decisions so far` line still matches the ticket it points at.
That is a real structural difference from `_CHAIN.md`, which is **generated every build**. But it is
now an observation about *design*, with **no incident behind it** — and the version with an incident
behind it was mine, not his.

⚠ **The one action that survives intact, because it never depended on his repo:** `MEMORY.md` is
hand-appended, exactly like `Decisions so far`. Whether any gate checks it for index↔file drift is
still unknown and still ~15 minutes to find out. §0 step 2 stands.

## §6 — Prior art: how novel is this?

| Wayfinder term | Prior art | Relationship |
|---|---|---|
| Destination fixes scope | Shape Up — **appetite** | Shape Up bounds by *time*; wayfinder bounds by *outcome*. Different axis, same job. |
| **Out of scope**, never graduates | Shape Up — **no-gos**: *"functionality or use cases intentionally not being covered … to make the problem tractable"* | Near-identical, including the reason. |
| **Fog of war** / *Not yet specified* | Shape Up — **rabbit holes**: *"technical unknowns, unsolved design problems, or misunderstood interdependencies"* | ⭐ **Closest thing to novelty.** Shape Up *removes* rabbit holes before betting; wayfinder **writes the fog down as a first-class map section and graduates it incrementally.** Shape Up has no register for "known unknown, not yet sharp". |
| Plan, don't do; shaping precedes betting | Shape Up — *"a shaped project should be as free of holes as possible"* before it is bet on | Same doctrine. |
| One decision per ticket, resolution recorded | ADRs (and the repo ships `docs/adr/`) | Wayfinder = ADRs with a dependency graph and a frontier query. |
| Frontier / claim-before-work | Kanban WIP limit = 1, plus a pull signal | Standard, executed cleanly. |
| Fog of war, frontier | RTS games | Where the metaphor comes from; it is load-bearing, not decorative. |

**Verdict on novelty:** wayfinder is **Shape Up's shaping phase, ported to agent sessions, with the artefact moved onto the issue tracker so the tracker's own blocking UI renders the frontier for free.** That last move is the cleverest engineering in it — it is [[instrument-without-a-consumer]] solved by *not building the reader*, and borrowing one that already exists and is already on the human's screen. The genuinely new idea is **writing the fog down**.

---

## §7 — What Memento should actually take (and refuse)

### 7.1 ⭐ TAKE: the fog test, as vocabulary

> *"The test is whether you can state the question precisely now — not whether you can answer it now."*

This is our own [[feedback-check-ran-never-reached-plan]] ruling (*an honest UNPROVEN is a PRICED TODO*) reached from the opposite direction — and it is **sharper as a word than as a rule**, because it names the *state* rather than the *duty*. It also gives a clean three-way sort we currently do in prose each time:

| Wayfinder | Ours today |
|---|---|
| Ticket | a priced TODO / an open `§C` item |
| **Not yet specified** (fog) | ⚠️ **no single word** — currently "floated", "unruled", "UNPROVEN", "owed" depending on who wrote it |
| Out of scope | `_FUTURE-STATE.md` / ruled-out, but with **no rule that it never graduates** |

The middle row is a real vocabulary gap in `_FIXED-FLEX-CHARTER.md`, and the third row is a *missing property*, not a missing word: wayfinder's "never graduates, returns only as a fresh effort if the destination is redrawn" is a **stronger** guarantee than anything we hold. **Dave's to rule** — one row in the charter, not a section.

### 7.2 TAKE, with our gate attached: HITL/AFK

*"The agent never stands in for the human's side of it"* is the same law as [[check-after-its-own-remedy]] and [[gate-must-quote-what-it-forbids]]. Wayfinder states it beautifully **and ships no enforcement** — it is prose where [[translate-prose-into-machinery]] says the deliverable is the added code. If we adopt the vocabulary we should adopt it the way we adopt everything: **with a gate, mutation-tested at birth** ([[gate-must-quote-what-it-forbids]]). Otherwise we have imported a sentence.

### 7.3 REFUSE: the map machinery

We do not need a `wayfinder:map` issue. We have `§C`, `_MEMENTO-DECISIONS.md`, `_FUTURE-STATE.md`, and a generated `_CHAIN.md`, and per `notes/2026-07-28-memento-jit-context-research.md` §4 *"most of the stack exists"*. Importing a second index would violate the very rule wayfinder is built on — **a decision lives in exactly one place**.

One asymmetry worth naming in wayfinder's favour, because it is architectural and not stylistic: **an issue tracker gives granular fetch for free.** Wayfinder's *"zoom as needed: fetch the full body of any related or closed ticket on demand"* is cheap because one issue is one fetch. Our equivalent constraint is ruled and harsher — [[chain-cut-on-paper-not-in-the-tool]]: **`Read` cannot read less than a file.** We bought our way out of that with `_memento_search.py --fetch <id>`, which is the right organ. **So the index-not-store pattern is only cheap if retrieval is granular** — and that is the argument for `_memento_search.py` restated by a stranger, which is the most useful kind of corroboration.

### 7.4 NOTE, don't act: the unmeasured throughput claim

*"keeping the frontier fast"*, *"more than one agent session can hold"* — no measurement exists anywhere in the page or the repo. This is precisely the risk our own JIT note flagged against ourselves (§7.3: *"The win assumes most reference is unread most sessions — **UNMEASURED**"*). Same defect class, someone else's artefact. **Do not import the claim; import the discipline of noticing it is a claim.**

---

## §8 — UNPROVEN, with named probes and prices

| # | What is unproven | The probe that would settle it | Price |
|---|---|---|---|
| U1 | Whether the `research/<name>` branch and the "research excepted" carve-out exist anywhere in the repo | Fetch `setup-matt-pocock-skills/SKILL.md` + the three `issue-tracker-*.md` and grep both strings | 2 fetches |
| U2 | Whether the README/tree drift is README-stale or CDN-stale, and how old | Commits API (returned empty today) or the GitHub UI commit list | 1 fetch, may fail again |
| U3 | Whether wayfinder works — no adoption evidence, no trial report, no post-mortem was sought or found | Out of scope for desk research; would need a trial | not priced |
| U4 | Whether "100K" means cl100k, o200k, or Claude's tokenizer | Not answerable from the artefact; the skill does not say | unanswerable as written — **which is the finding** |
| U5 | Whether `MEMORY.md` has any index↔file drift gate on our side | `grep` our gates for `MEMORY.md` | ~15 min ⇒ §0 step 2 |

---

## §9 — Risks in this note itself

1. **The page may have been right and the repo behind it.** I treated `SKILL.md` as canon over the page. If Matt ships from a branch and the page documents the newer thing, my §3 inverts — the page would be *ahead*, not wrong. Either way §2's finding stands: **they disagree, and the installable artefact is the one that runs.**
2. **§6's Shape Up mapping rests on a search summary, not a full fetch** of chapter 5. The quoted phrases are from that summary. Treat the *table* as sound and any single quotation as needing a re-fetch before it is repeated in anything public.
3. **§4's tension is an argument-form parallel, not an inconsistency proof.** I have scoped it in-line. Do not let it harden into "he contradicts himself" — he does not, quite.
4. **⛔ THIS RISK FIRED — see §5.3 point 2. Left standing verbatim as the evidence.** I have been generous to Memento throughout. Every convergence in §7 is one I already believed; per [[attribute-the-diff]] that is the condition under which a control is most needed and I ran none. The one place I turned it on us — §5's `MEMORY.md` — is the only place this note earns its cost.
5. **The gauge figure in the header is an estimate** and [[planning-estimate-is-not-a-measurement]] applies: it flips no decision here, but do not carry it into anything that needs a measured band.

---

## Sources

- [The /wayfinder Skill — aihero.dev](https://www.aihero.dev/skills-wayfinder) (page under review; meta `updatedAt` 2026-07-07)
- [`skills/engineering/wayfinder/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md) — the installable artefact, and the canon for §2
- [`skills/engineering/research/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md)
- [`README.md`](https://github.com/mattpocock/skills/blob/main/README.md) — §5
- [`.out-of-scope/question-limits.md`](https://github.com/mattpocock/skills/blob/main/.out-of-scope/question-limits.md) — §4
- [Shape Up — Risks and Rabbit Holes](https://basecamp.com/shapeup/1.4-chapter-05) and [Write the Pitch](https://basecamp.com/shapeup/1.5-chapter-06) — §6
- Ours, quoted not re-derived: `notes/2026-07-29-context-degradation-research.md` §1d/§2 · `notes/2026-07-28-memento-jit-context-research.md` §4/§7
