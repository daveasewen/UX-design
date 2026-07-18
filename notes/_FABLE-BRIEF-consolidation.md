# FABLE BRIEF — make the knowledge base interrogable

*Written 2026-07-19 by Opus, for a **cold Fable session**. Dave's ask: "make the brief bloody good."*
*Status: **DRAFT — Dave to add candidates before the session runs.** See §7, the running list.*

---

## 0 · Read this first — the reframe that decides the scope

The task was queued as *"consolidate `_LIVE-STATE.md`, it's 1044 lines and has never shrunk."* That
framing is too small, and taking it literally would waste the session on tidying.

**Four separate complaints from the last fortnight are one problem:**

| symptom | when |
|---|---|
| `_LIVE-STATE.md` is 1044 lines — past what a cold agent can read, though it exists to be read cold | ongoing |
| Three solutions in one day to problems the rules had **already answered** | 2026-07-18 |
| `{#type26-019}` was "blocking" for weeks while four tranches breached it — **the glob decided, not the rule** | 2026-07-17 |
| `_validate_assertions.py` fires only when a fact **FLIPS**, so a doc known-wrong-now is never chased | 2026-07-18 |
| A `COLLISION_HOLD` honoured in planning, violated in the write — no gate saw it | 2026-07-19 |

**The unifying diagnosis: we can WRITE to the knowledge base far better than we can INTERROGATE it.**
Every mechanism we have is a *write-side* mechanism — ledgers, tombstones, assertions, rule IDs,
runbooks. The read side is a human remembering to grep. That asymmetry is the actual defect, and
`_LIVE-STATE`'s length is a symptom of it, not the disease.

**So the session's job is not "make the file shorter." It is: make the record answerable.**
A cold agent about to design something must be able to ask *"what already governs this?"* and get a
trustworthy answer in one step. Shortening `_LIVE-STATE` is one means to that end, not the end.

> This reframe is **the brief's central claim and it is a claim, not a fact.** If the Fable session
> reads the evidence and concludes the reframe is wrong — that this really is just a long file needing
> a trim — **say so and do the smaller job.** That is a legitimate outcome, not a failure. Do not
> perform the larger scope out of deference to whoever wrote this.

---

## 1 · Why Fable, and what that buys

Fable is **rationed premium** (`MODEL-ROUTING.md`): big, high-stakes, hands-off jobs where a mistake
across the whole scope is costly and nobody can babysit it. This qualifies because:

- It touches **the cold-start spine itself** — `GOOD-MORNING` → `_LIVE-STATE` → `MEMORY.md`. Damage
  here is not visible in a diff; it shows up weeks later as an agent confidently doing the wrong thing.
- It requires holding **~1044 lines of `_LIVE-STATE` + 465 rules + 9 runbooks + ~110 memories** in view
  at once to spot what is genuinely redundant versus what merely *looks* redundant.
- The failure mode is **confident false inscription** (see §3). A cheaper model consolidating
  aggressively would produce something clean, readable, and subtly wrong — the worst possible artefact,
  because its tidiness is what makes it trusted.

**Run it COLD.** No context from the sessions that produced the mess. If the record cannot be
understood cold, that is the finding, and it should be reported as one rather than patched over with
context the next agent won't have either.

---

## 2 · The one rule that governs everything else here

> **A record is only as good as your ability to find it AT THE MOMENT YOU NEED IT.**

The corollary, which is what makes this hard: **a rule that is written down, correct, well-ID'd, and
never retrieved is indistinguishable from a rule that does not exist.** All three 07-18 failures were
of exactly this kind. Nothing was missing. Everything was findable. Nothing was found.

Optimise for **retrieval at the point of decision**, not for completeness of the archive.

---

## 3 · Non-negotiables — what must survive untouched

*(The Memento discipline: the danger is not forgetting, it is **confident false inscription**.
Deleting a true record is worse than keeping a long one. Read `GOOD-MORNING.md` §A before starting.)*

1. **§A ORIENTATION in `GOOD-MORNING.md` — NEVER drop it, never shorten it to a label.** A
   from-scratch rewrite on 2026-07-18 reduced its standing-instruction note to the words *"Standing
   section"*, losing both the rule and Dave's reason for it. It is reachability-gated by
   `_validate_standing_instructions.py` (STAND-002) — **run that gate after every edit.**
2. **Provenance survives compression.** Records carry *observed vs inferred*, and the WHY, not just
   the WHAT. `dv-019`'s "because Dave saw the dance on a 146° pair" **is the record** — the number is
   not. If compression forces a choice, **keep the why and drop the what.**
3. **Rulings are Dave's and are never re-derived.** Consolidation may reorganise, cross-link, and
   tombstone. It may **not** re-decide, quietly widen, or "clean up" a ruling into a tidier one.
   Derivation governance: the engine never derives-and-promotes.
4. **Corrections stay as loud as the original claim.** Every ledger has entries of the form "I was
   wrong about X, Dave caught it." **These are the most valuable content in the repo and the most
   likely to be compressed away as noise.** They are not noise; they are the calibration record.
5. **Supersession discipline.** Anything killed gets a tombstone **and** its propagation gap logged in
   the same pass (`AGENTS.md`).
6. **Green build at the end.** `python3 knowledge/_build_all.py` — 30 steps. DEF-006 is *expected* to
   fail and is deliberately unwired; nothing else may.

---

## 4 · Scope — do these, in this order

### 4.1 AUDIT FIRST, CUT SECOND *(do not skip; the audit is the deliverable even if nothing is cut)*
Before removing a line, classify every section of `_LIVE-STATE.md` as:
**LIVE** (true now, load-bearing) · **HISTORICAL** (true, but its value is provenance not state) ·
**SUPERSEDED** (tombstone it) · **DUPLICATE** (says what another file says better) ·
**ORPHANED** (nothing references it and nothing would notice its absence).

Output that classification as a table **before** editing. If Dave disagrees with a call, he disagrees
with it cheaply, at the classification stage, not after 400 lines are gone.

### 4.2 SPLIT STATE FROM HISTORY
The file conflates *"what is true now"* (a cold agent needs this in ~150 lines) with *"how we got
here"* (valuable, rarely needed at decision time). **Propose a split**, e.g. `_LIVE-STATE.md` as a
genuine spine plus a dated `_DECISION-HISTORY/` archive. Cross-link both ways so nothing is orphaned.
**Do not delete history to achieve brevity — relocate it.**

### 4.3 THE READ-SIDE MECHANISM — the real prize
Design the thing that would have prevented the three 07-18 failures. This is open-ended by intent;
you are being trusted to invent it, not to implement someone else's sketch. Prompts, not answers:
- A **problem-domain → governing-rules index**, so "I am about to design an amber indicator" resolves
  to the rules that already govern it. (`_rules-index.json` has 465 rules with stable IDs — the spine
  exists; the *entry point by problem* does not.)
- A **pre-flight protocol** encoded as a gate or runbook step: *before designing, state which rules
  you retrieved.* Compare with `_trace_knowledge_usage.py` (retrieved-vs-invented), which already does
  something adjacent — **reuse before building.**
- The **gate-glob coverage audit**: which of the 465 rules have a gate, and where does each glob
  actually bite? The generalised form of `{#type26-019}` and of today's DEF-006 finding.
- **Assertion gate blind spot**: it fires on FLIP, so a claim registered as already-true is never
  re-chased. Should assertions carry a **re-test date** as well as a predicate?

**Pick the highest-leverage one and design it properly. Do not sketch four.**

### 4.4 RULE ON THE MEMORY MIRROR — it is explicitly deferred to this session
`knowledge/_agent-memory/store/` mirrors the agent's memory into the repo. **Dave challenged the
premise and was right:** the store held 115 files against 110 live — it has already become the third
source of truth its own README forbids. Deeper: the mirror exists because we do not trust our own rule
that *"memory is an accelerator, the repo is the record."* If that rule held, losing memory would cost
nothing worth backing up. **Rule it: delete the mirror, or keep it and make it honest.** Do not invest
in mirroring machinery before ruling. (`_RUNBOOK-capture-ritual.md` step 3.)

> ⚠️ **DECLARED DEVIATION, 2026-07-19.** The capture ritual's mirror-on-write step was **deliberately
> NOT performed** this session. Three memories changed (`type-binding-mechanism`,
> `attribute-the-diff`, `fable-consolidation-brief`) and none were copied into the store. Reason:
> mirroring only two of three would deepen exactly the inconsistency that makes the mirror suspect,
> and the ritual itself defers this question here. **The live memory files are the current copy; the
> store is now known-stale by at least three entries.** Flagging rather than silently skipping —
> if the ruling is "keep", this deviation is a small debt to repay, not a hidden one.

### 4.5 REPORT WHAT YOU COULD NOT UNDERSTAND COLD
Keep a running list of everything that needed context you did not have. **That list is a primary
deliverable, not an appendix** — it is the only direct measurement we have of how well the cold-start
spine actually works.

---

## 5 · What "done" looks like

- [ ] Classification table for every `_LIVE-STATE` section, produced **before** any cut.
- [ ] `_LIVE-STATE.md` is a spine a cold agent reads in full without skimming. **No target line count
      is set on purpose** — a number would be optimised for instead of the goal. Report the figure
      you reached and defend it.
- [ ] Nothing true was lost: relocated, cross-linked, or tombstoned — never silently dropped.
- [ ] One read-side mechanism designed to build-ready depth (§4.3).
- [ ] The memory-mirror question RULED (§4.4).
- [ ] "Could not understand cold" list delivered (§4.5).
- [ ] `_validate_standing_instructions.py` green; `_build_all.py` green; §A intact.
- [ ] **Every judgement call surfaced for Dave, not absorbed.** A consolidation that quietly makes
      forty small decisions is worse than one that makes thirty-five and flags five.

---

## 6 · Traps, specific and earned

1. **Tidiness reads as authority.** A clean file is trusted more than a messy one *regardless of
   accuracy*. Compression that loses a caveat produces something more dangerous than what it replaced.
2. **"This looks redundant" usually means "I don't have the context."** Several entries look like
   duplicates and are not — they record the same fact at different confidence levels, or the same
   ruling before and after a correction. **Check before merging.**
3. **The corrections are not noise** (see §3.4). Any instinct to strip "I was wrong about X" entries
   is the instinct to delete the most valuable content in the repo.
4. **Do not re-litigate settled commercial calls.** The webfont/licence thread is Dave's judgement,
   recorded as made. It reads like an open risk. It is not. Leave it.
5. **The brief itself may be wrong.** §0 is a claim. Test it against the evidence; report if it fails.

---

## 7 · 🗒️ RUNNING LIST — candidate Fable tasks

*Dave: "we probably need to think about fable tasks… I want to turbo charge the KB, can you think of
anything else? I'll note down anything as I think of them." **Add freely below; this list is the
point.** Ranked by my read of leverage — argue with the ranking.*

| # | candidate | why Fable | state |
|---|---|---|---|
| **1** | **This brief — consolidation + the read-side mechanism** | touches the cold-start spine; failure is invisible and delayed | **scoped, ready** |
| **2** | **Gate-coverage audit — all 465 rules × their globs** | needs the whole rule corpus in view at once; the generalised form of a bug we have now hit three times | strong candidate, unscoped |
| **3** | **Run the decision audit (ADR-0007 §5)** | *designed and never run*; explicitly specified as "run cold"; Tier A batch 1 first | **spec exists** — `_RUNBOOK-decision-audit.md` |
| **4** | **KB turbo-charge — but SCOPE IT FIRST** | Dave's ask; currently a direction not a task | ⚠️ see note below |
| **5** | **Binding blast-radius gate** | today's T-D12 §5 finding; wanted BEFORE the 690 remaining bind | small enough for Opus — listed so it isn't lost |

**⚠️ On #4, "turbo-charge the KB" — I don't think it is one task, and naming it as one would burn the
ration.** It currently spans at least four different things, which want different models:
- **Coverage** — finish Tier-2/3 ingestion (channels still deferred). *Sonnet, to the tranche runbook.*
- **Structure** — the unified knowledge graph, typed edges, ADR-0007 PM-KG MVP. *Fable-shaped.*
- **Retrieval** — §4.3 above; making the KB answerable. *Fable-shaped, and #1 already covers it.*
- **Interface** — the chat-to-KB bot, so people query it without an agent. *A build, once retrieval works.*

**My recommendation: do not run #4 as written.** Ask Dave which of those four he means — and my read
is that *retrieval* is the one that unlocks the others, which means **#1 already is the KB
turbo-charge**, wearing a duller name. Structure and interface both get better answers once retrieval
is solved; neither improves much while the read side is a human remembering to grep.

**Dave's additions:**
- *(add here)*

---

## 8 · Entry points, in reading order

`GOOD-MORNING.md` (§A first — the standing orientation) · `_LIVE-STATE.md` (the subject) ·
`AGENTS.md` (repo contract, supersession, git split) · `MODEL-ROUTING.md` ·
`_RUNBOOK-capture-ritual.md` (step 3 = the mirror question) · `_RUNBOOK-decision-audit.md` ·
`knowledge/_RUNBOOKS.md` (generated index of all runbooks) ·
`knowledge/guidelines/_rules-index.json` (465 rules) · `knowledge/_ASSERTIONS.md` ·
`knowledge/_trace_knowledge_usage.py` (existing retrieved-vs-invented tooling — **reuse, don't rebuild**).
