# Runbook — end-of-session capture ritual

*The insurance policy decided in `notes/_SEAWORTHINESS-PLAN_2026-07-05.md` ("The capture ritual / gate").
Stood up 2026-07-05 as a fixed, repeatable sequence — the enforcing script (`_capture_gate.py`) is
deferred to the PM-KG MVP build, but the ritual itself is free and starts now. Anchor: ADR-0007
(temporal decision-graph); principle: don't archive every transcript (rebuilds the haystack) — invest
in a *reliable* end-of-session distillation instead, because that's where the actual risk sits.*

---

## When to run this

At the end of **every** session that changed project state — decisions, rulings, code, docs. Skip
only for pure Q&A sessions that touched nothing. If in doubt, run it; it's cheap.

**Two-tier mid-session firing (ruled 2026-07-21, `_RUNBOOK-context-gauge.md`):** at **Amber** run
**step 1 only** — a light `_LIVE-STATE.md` spine-flush, session continues (no `GOOD-MORNING`, no
rename, no fresh window); at **Red** run the whole thing 1→5 + open fresh.

**Also run it mid-session when the context gauge reads Red (>70%)** — don't wait for a natural end.
The gauge (`_RUNBOOK-context-gauge.md`) exists precisely to fire this ritual *while there's still
clean budget to author the handoff well*; a `GOOD-MORNING.md` written at 95% full is the confidently
wrong handoff we most want to avoid. Red cue line, ready to use:
> **Title this chat: `<retrospective title>` — context is Red (~NN%). Running the capture ritual, then
> open fresh with: `<forward title>`.**

## The steps, in order (1, 1b, 2, 3, 4, 4b, 5)

1. **Refresh `_LIVE-STATE.md`** — and its siblings where touched: `_FUTURE-STATE.md` (ideas /
   side-quests / resurrection candidates) and `_DECISION-HISTORY/` (narrative >10 lines relocates
   there at write time — the spine discipline, ruled 2026-07-18). Update LIVE / SUPERSEDED-DEAD /
   OPEN / PLANNED-TARGET for anything that changed. Bump the `*Last refreshed:*` line —
   ⚠️ **take the date from running `date`, never from the session's own belief**: the T-D12 handoff
   self-dated "2026-07-19" while its commits landed 07-18 evening; commit timestamps caught it.
   Confident false inscription of something as small as a date still poisons the record.
   If a ruling killed something, tombstone the artifact **and** log the propagation gap in the
   same pass (supersession discipline, non-negotiable per `AGENTS.md`).
1b. **Author the session NARRATIVE DOSSIER — the why and how, not just the what.** *(Added 2026-07-19,
   Dave: "a narrative dossier would be good for many chats, I like recording the why and how not just
   saving the what — maybe this should be part of the closing ritual." Model example:
   `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md`.)*
   For any session that produced real **reasoning** — a method, a multi-step decision arc, findings, a
   design exploration — write a dated `_DECISION-HISTORY/YYYY-MM-DD-<thread>.md` that records the ARC:
   the why behind each finding, the dead-ends and corrections, how the thinking moved, not only the final
   values. **This complements, never replaces, the terse records:** the ledgers / ADRs / `_LIVE-STATE`
   hold the WHAT (the ruling + its pin); the dossier holds the WHY and HOW (the narrative that the ledger
   line can't carry and that evaporates with the chat). Group by finding, each with its rationale; end with
   the resolved state and what's still open. Obey the archive rules (`_DECISION-HISTORY/README.md`): **lands
   whole, dated from `date`, never silently edited after; both-way links** to its spine entry and ledger.
   **Trigger:** substantive/reasoning-heavy sessions. **Skip** for trivial or purely mechanical ones — the
   test is "would a cold reader need to know *why* we did this, not just *what* we landed on?" If yes, write it.
2. **Write/refresh `GOOD-MORNING.md`.** The cold-start entry point for the *next* session — write it
   for a reader with zero memory of this one. **Required structure, in order:**
   - **The two names first** (see step 4b) — rename + next title, at the very top.
   - **§A ORIENTATION — STANDING. Carry it forward EVERY time.** The whole project on one page,
     new-starter style, at Dave's request 2026-07-17: *"orientate a new starter — wider context helps."*
     What Apollo is · the three-libraries-one-skeleton model · where things live · the one command ·
     the rules that actually bite · how we work. **Update it when the shape of the project changes, not
     every session — but NEVER drop it, and never shorten it to a label.**
   - **§B this session** — what landed, what was found, what I got wrong. **Every "landed/done"
     claim names its evidence** — gate run, commit hash, render, file path (routing audit #7,
     ratified 2026-07-23; same discipline for worker receipts). The header records the session's
     **model, and effort if it was actually set** (#8 — effort is only settable via agent
     definitions today; record it when known, omit otherwise).
   - **§C queue** — numbered, actionable, plus commit/push state. **Stamp the author's context-gauge
     reading in the commit-state block** (`_RUNBOOK-context-gauge.md` § authoring-time stamp) — a
     scrutiny indicator on this handoff's reliability, not a quality score. Format:
     `Context gauge at authoring: 🟢/🟡/🔴 BAND ~NN% (ESTIMATE)`.

   ⚠️ **§A is the section most at risk, because it is the only one that doesn't change each session.**
   On 2026-07-18 a from-scratch rewrite of `GOOD-MORNING.md` reduced §A's standing-instruction note to
   the two words "Standing section", dropping both the carry-forward rule and Dave's reason for it —
   caught only because Dave asked. The instruction had been surviving *only* by being copied forward
   inside the file it governs, which is not survival, it is luck. That is why it is written here too:
   a rule that lives only in the artefact it governs dies the first time that artefact is rewritten.
3. **Update memory — AND mirror anything durable into the repo.** Any `feedback` / `project` / `user` /
   `reference` memory that's new or changed this session, plus the one-line pointer in `MEMORY.md`.
   Check for stale memories the session disproved and correct or remove them.

   ⚠️ **Memory is NOT a backup and NOT the source of truth.** It lives outside the repo: not in git, not
   pushed by GitHub Desktop, invisible to the shell and to every gate, and lost if the Cowork space is
   reset. It is also *mine* — a terminal session or another tool won't have it. And it can hold stale
   facts confidently (on 2026-07-18 a memory still said "26 gates"; it was 29 by end of day).
   **So: memory is an accelerator, the repo is the record.** Anything that must survive — a rule, a
   rationale, a threshold, a convention — gets written into the repo in the same pass, not just into
   memory. `_validate_standing_instructions.py` enforces reachability **repo-side only**; nothing can
   check that a memory-only rule was ever mirrored, which makes this step the weakest link in the chain
   and the one to do deliberately rather than at speed.

   **THE MIRROR IS DELETED — RULED (Dave, 2026-07-18, consolidation session; the open question this
   step used to carry is settled).** `knowledge/_agent-memory/store/` had become the third source of
   truth its own README forbade (115 stored vs 110 live, five ghosts, three known-unmirrored
   changes). It exists no more; there is **no mirror-on-write and no rsync**. Final dated snapshot,
   non-authoritative, recovery-only: `_retired/agent-memory-snapshot-2026-07-18/`.
   ⇒ **The rule that replaces it: durable content is INSCRIBED, not photocopied.** If something in
   memory must survive — a rule, a rationale, a threshold, a convention — write it into its proper
   repo home *in the same pass*: rules → `GOOD-MORNING.md` §A / a runbook / a guidelines `{#id}`;
   checkable facts → `knowledge/_assertions.json`; rulings → the decisions ledgers. Memory then stays
   what it is declared to be: an accelerator, genuinely disposable, because the repo is the record.

   **Also: if you wrote a checkable claim about the environment, register it.** Anything of the form
   "X exists / X is missing / there are N of Y" belongs in `knowledge/_assertions.json` with a predicate,
   so `_validate_assertions.py` re-tests it every build and names every document that repeats it when it
   flips. Prose asserting a fact with no way to re-test it is exactly how "the sandbox has no Univers"
   survived sixteen months.
4. **Record decision nodes with supersession discipline.** Any new ruling gets logged where decisions
   live (ADR, charter section, or `_LIVE-STATE`), cross-linked both ways, seeded as `unaudited`
   per the decision-audit method (`_RUNBOOK-decision-audit.md`) — never self-promoted to `vouched`.
4b. **Name the session — BOTH directions.** *(Added 2026-07-18, Dave: "add a rename instruction into the
   good morning going forward, it's more efficient than copy and pasting your suggestion.")*
   Sessions drift — they routinely end up being about something other than what they were opened for
   (2026-07-18 opened as the type retrofit and became the halation/edge-extremity discovery; the retrofit
   was ~15% of it). So the handoff carries **two** names, and both go at the TOP of `GOOD-MORNING.md`
   where Dave acts on them first, not buried at the bottom:
   - **RENAME THIS SESSION → `<retrospective title>`** — what it turned out to be, written with hindsight.
     Dave applies it to the finished conversation.
   - **NEXT SESSION TITLE → `<forward title>`** — the opener for tomorrow.
   Write them as ready-to-use lines, not as a suggestion needing reformatting. Claude cannot rename a
   conversation itself — no tool for it — so the line exists to make Dave's action one copy, not a
   re-read of the whole handoff to work out what the session became.
   ⚠ **Titles are LABELS, never role assignments** (2026-07-21: a forward title's `[conductor + 2
   workers]` seated a second conductor). If the coming session runs the parallel model, say so in the
   §C brief and let the ROLE come from Dave's opener line — and include the **DIVVY PLAN** (lanes ·
   model per lane · serial set · shared files assigned per lane) in the forward brief, per
   `_RUNBOOK-parallel-conductor.md`.

5. **Commit + push.** Claude commits in terminal with a paste-ready summary + description, clears any
   stale `.git/*.lock` files. **Dave pushes via GitHub Desktop only** — never terminal push, never a
   Desktop commit, Desktop closed while Claude commits (memory `git-push-method`).

## What "done" looks like

All steps complete = the session is safely captured. The transcript never has to be the source
of truth — a cold-start agent can reconstruct full context from `GOOD-MORNING` → `_LIVE-STATE` →
`knowledge/README.md` → `MEMORY.md` alone.

## The gate (spec only — not yet built)

A light, enforceable check, `_capture_gate.py`, to build **alongside the PM-KG MVP** (same
front-matter/date-parsing machinery as `_build_live_state.py`):

- **FAIL** if `_LIVE-STATE.md` "Last refreshed" ≠ today.
- **FAIL** if `GOOD-MORNING.md` date ≠ today.
- **WARN** on dangling `MEMORY.md` pointers (an index line or `[[link]]` with no matching file).
- **WARN** if uncommitted changes remain (nudge to commit before close).

Green = safely captured. Until the script exists, this runbook **is** the gate — run it by hand,
every session, no exceptions.

## Why this exists

The seaworthiness plan's failure-mode finding: **tracking rots silently** (the Sutherland manifest
said "blocked" three weeks after the blocker cleared; a suspected 39-vs-38 compliance-KG drift this
same session turned out to be a miscount — see `_LIVE-STATE.md` Phase 0 entry). A fixed ritual, not
an ad hoc "remember to update things," is the cheapest available defence. The enforcing gate is the
next layer once PM-KG infrastructure exists to build it on.

## Entry points

`notes/_SEAWORTHINESS-PLAN_2026-07-05.md` (§ "The capture ritual / gate" — origin of this spec) ·
`_LIVE-STATE.md` · `GOOD-MORNING.md` · `MEMORY.md` · `AGENTS.md` (supersession discipline, git split) ·
`_RUNBOOK-decision-audit.md` (validation-state discipline for step 4) ·
`_RUNBOOK-context-gauge.md` (the fuel gauge that decides *when* to fire this ritual mid-session).
