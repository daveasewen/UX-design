# Runbook — end-of-session capture ritual

*The insurance policy decided in `notes/_SEAWORTHINESS-PLAN_2026-07-05.md` ("The capture ritual / gate").
Stood up 2026-07-05 as a fixed, repeatable sequence — the enforcing script (`_capture_gate.py`)
was BUILT 2026-07-26 under the Memento dream-pass lane (§ "The gate" below; rulings
`notes/_MEMENTO-DECISIONS.md`). Anchor: ADR-0007
(temporal decision-graph); principle: don't archive every transcript (rebuilds the haystack) — invest
in a *reliable* end-of-session distillation instead, because that's where the actual risk sits.*

---

## When to run this

At the end of **every** session that changed project state — decisions, rulings, code, docs. Skip
only for pure Q&A sessions that touched nothing. If in doubt, run it; it's cheap.

**Two-tier mid-session firing (ruled 2026-07-21, `_RUNBOOK-context-gauge.md`):** at **Amber** run
**step 1 only** — a light `_LIVE-STATE.md` spine-flush, session continues (no `GOOD-MORNING`, no
rename, no fresh window); at **Red** run the whole thing 1→5 + open fresh.

**Also run it mid-session when the context gauge reads Red (≥60%)** — don't wait for a natural end.
The gauge (`_RUNBOOK-context-gauge.md`) exists precisely to fire this ritual *while there's still
clean budget to author the handoff well*; a `GOOD-MORNING.md` written at 95% full is the confidently
wrong handoff we most want to avoid. Red cue line, ready to use:
> **Title this chat: `<retrospective title>` — context is Red (~NN%). Running the capture ritual, then
> open fresh with: `<forward title>`.**

## The steps, in order (1, 1b, 2, 2c, 2d, 2e, 2f, 3, 4, 4b, 5, 5b)

*Steps **2e** and **2f** were added 2026-07-27 (GM-D1…D9, `notes/_MEMENTO-DECISIONS.md` § GM
growth-contracts ruling). They extend the 2c/2d pattern — cap + archive sibling + verbatim move +
EXIT CHECK — to the two `GOOD-MORNING.md` regions that had no roll rule and were therefore absorbing
~97% of the file's growth. **The architecture in one line: every GM section declares a growth contract
(what it may contain · cap · roll target · retirement test); §A alone is standing and uncapped.***

1. **Refresh `_LIVE-STATE.md`** — and its siblings where touched: `_FUTURE-STATE.md` (ideas /
   side-quests / resurrection candidates) and `_DECISION-HISTORY/` (narrative >10 lines relocates
   there at write time — the spine discipline, ruled 2026-07-18). Update LIVE / SUPERSEDED-DEAD /
   OPEN / PLANNED-TARGET for anything that changed. Bump the `*Last refreshed:*` line —
   ⚠️ **take the date from running `date`, never from the session's own belief**: the T-D12 handoff
   self-dated "2026-07-19" while its commits landed 07-18 evening; commit timestamps caught it.
   Confident false inscription of something as small as a date still poisons the record.
   If a ruling killed something, tombstone the artifact **and** log the propagation gap in the
   same pass (supersession discipline, non-negotiable per `AGENTS.md`).
   **Feed the sign-off register (dream-pass v2 P4, ruled 2026-07-26):** if the session leaves a
   review artefact awaiting Dave (a `reviews/*.html`, a proposal brief, a showroom pane), its PATH
   goes into `knowledge/_REVIEW-SIGNOFF.md`'s running list in the same pass — not only into the
   banner. Banners compact (2c/2d); the register is the durable queue.
   **Save cited uploads (dream-pass v2 P5(b), ruled 2026-07-26):** any uploaded/attached document
   the record will CITE gets written into the repo (`notes/`, verbatim + field lines) in the same
   session — a chat-only attachment is an un-retrievable citation. Worked precedent both ways: the
   `lamish-…` transcript was saved and nothing that cites it ever blocked; the convergence note was
   not, and its `-v2` blocked three consecutive sessions on "re-attach".
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
   **Provenance fields (added 2026-07-26, Memento §4.1 — D1a/D2, `notes/_MEMENTO-DECISIONS.md`):** every
   new dossier — and every new dated note in `notes/` — carries two plain lines in its header block at
   write time, mechanical, never authored as prose:

   ```
   provenance: <session-id> · <YYYY-MM-DD>     # id from the session's own path; date from `date`, never belief
   status: observed | inferred | ruled | floated | standing
   ```

   `ruled` is reserved — writable only with a pointer to its ledger/ADR entry after the value
   (promotion is Dave's alone). `standing` = long-lived Dave-owned hypothesis, neither floated-and-
   forgotten nor ruled. **Enforced by `_capture_gate.py` in every build** (blocking, files dated
   ≥ 2026-07-26 — no corpus retrofit).
2. **Write/refresh `GOOD-MORNING.md`.** The cold-start entry point for the *next* session — write it
   for a reader with zero memory of this one. **Required structure, in order:**
   - **The two names first** (see step 4b) — rename + next title, at the very top.
   - **§A ORIENTATION — STANDING. Carry it forward EVERY time.** The whole project on one page,
     new-starter style, at Dave's request 2026-07-17: *"orientate a new starter — wider context helps."*
     What Apollo is · the three-libraries-one-skeleton model · where things live · the one command ·
     the rules that actually bite · how we work. **Update it when the shape of the project changes, not
     every session — but NEVER drop it, and never shorten it to a label.**
     ⚠️ **§A is EXEMPT from every cap and every roll rule in 2c–2f** — standing and uncapped, by ruling
     (GM-D1…D9 invariant, 2026-07-27). No cap, no roll, no rewrite, not even a guard banner. The reason
     is at the foot of this family (the 07-18 incident); it is the one section a growth contract must
     never touch, because its cost is the point.
   - **The ★ LATEST banner IS the session record — there is no §B.** *(GM-D4(a), ruled 2026-07-27:
     §B deleted, its spec formally absorbed here. This amends a previously ratified required-structure
     and changed only on Dave's ruling. Practice had already voted — §B's own STALE notice declared the
     banners authoritative while §B accreted "retained for context" strata; it was a duplicate register.)*
     The banner carries, and must carry, everything §B was required to: what landed, what was found,
     **what I got wrong**; **every "landed/done" claim names its evidence** — gate run, commit hash,
     render, file path (routing audit #7, ratified 2026-07-23; same discipline for worker receipts);
     evidence lines written `provenance:`-shaped (`<source> · <date>`) so they can later be machine-read
     (2026-07-26, Memento §4.1 — spirit unchanged, format converges); the session's **model, and effort
     if it was actually set** (#8 — effort is only settable via agent definitions today; record it when
     known, omit otherwise); and the **context-gauge stamp** (below). Banner stack rolls per **2c**.
   - **§C queue** — numbered, actionable, plus commit/push state. **Contract (GM-D6(a)):** §C·1–4
     entries are **pointer + state + owner** — no method bodies. Method lives in the brief or ledger the
     pointer names; an entry that restates it is duplicating a document that will drift out from under
     it. Parked list stays as-is. **Cap 150 lines**, excluding the 2f stratum stack.
     **Stamp the author's context-gauge reading in the commit-state block**
     (`_RUNBOOK-context-gauge.md` § authoring-time stamp) — a scrutiny indicator on this handoff's
     reliability, not a quality score. Format: `Context gauge at authoring: 🟢/🟡/🔴 BAND ~NN% (ESTIMATE)`.
   - **The read-chain contract, stamped in the file (GM-D7(a)).** GM states its own budget and the
     chain's: **GM ≤ ~8K tk · chain (GM + `_LIVE-STATE.md`) ≤ ~24K tk (~12% of a window)**, both files
     carrying a gate-checked size stamp so drift is visible rather than discovered. **Everything cited
     beyond the chain is RETRIEVAL** — `_consult.py`, a grep, a targeted read — **never a reading list.**
     ⚠️ The old open-ended *"then the decision files it points to"* was a selective instruction pretending
     to be complete: the chain cites 112 asset paths, ~312K tk resolvable, 1.5× a window. Say the
     selectivity out loud or the next cold reader will try to obey it.
     **The stamp, in the file's header block, one canonical form** (the `K` is required — without it
     `GM 25618 tk` parses as 25.6M and passes a drift check by accident):
     ```
     > **size:** GM 25.6K tk · chain 43.5K tk · measured <date> (tiktoken cl100k_base)
     ```
     The gate **measures the file and checks the stamp against its own measurement** (>10% drift = FAIL),
     so a stale stamp is caught rather than believed. ⚠️ **Measure, never convert by rule of thumb:** this
     corpus runs at **3.53 bytes/token**, not the customary 4 — its ★ ⚠ ⛔ · — load makes it ~13% denser,
     so every chars/4 estimate of these files has read LOW, including the ones in the proposal that set
     the budget.

   **2c. Compact the banner stack — keep ★ LATEST + 1 PRIOR, roll the rest to `_GM-ARCHIVE.md`.**
   → **Execute every move via `python3 knowledge/_gm_move.py --ops <ops.json>` — never hand-edit a roll** (M5, 2026-07-28: line-START anchors · §A digest asserted · caps imported, warn ≠ block · all-or-nothing · stdout receipts).
   *(Added 2026-07-25, Dave: "make good morning more efficient… keep improving Memento." First run the
   same day cut `GOOD-MORNING.md` by 35%.)*
   The stacked PRIOR banners are Polaroids: they accrete every session and, unpruned, become the single
   biggest cold-start read cost (2026-07-25 measure: the old-banner pile was **35% of the file**, ~3.9k
   tokens re-read every session for history already recorded elsewhere). At each wrap, **before** writing
   the new ★ LATEST banner, move every banner older than **★ LATEST + 1 PRIOR** into `_GM-ARCHIVE.md` —
   **verbatim, newest-first, a move never a rewrite** (mirrors `MEMORY.md` → `MEMORY-ARCHIVE.md`).
   **Batch key = `<date> <session#>`, never a serial** (GM-D5(a), 2026-07-27). Serials collided twice —
   two "Batch 11", two "Batch 6" — because parallel sessions mint them independently and none can see
   the others' numbering. A date plus the session number is derivable from inside a single session,
   which is the only vantage point a session actually has.
   ⚠️ **Precondition, do not skip:** confirm each rolled banner's durable content already lives in its
   proper home — `_DECISION-HISTORY/` (the WHY/HOW), `notes/_receipts|_briefs/`, the decision ledgers, or
   git. The archive is a **convenience copy, never a tattoo**: it must hold no rule, threshold or rationale
   that isn't already inscribed elsewhere. Only then is it safe to trim.
   ⚠️ **EXIT CHECK (dream-pass v2 P1, ruled 2026-07-26):** before a banner rolls, scan it for
   **⚠ / ⬛ / "AWAITING" / "OPEN CALL" / "DEFERRED TO DAVE"** lines. Each such item must already
   appear in a **standing** section (GM §C·2/§C·3/§C·4, a register, or `_FUTURE-STATE.md`) — if it
   doesn't, copy it up FIRST, then roll. The 07-24 chart banner rolled 6 of 7 numbered deferrals out
   of live state; only the one with a standing home survived. Dated homes (briefs, receipts,
   `_DECISION-HISTORY/`) do NOT count — a cold session reads none of them.

   **2d. Compact the `_LIVE-STATE` delta stack — keep ⏱ LATEST + 2 PRIOR, roll the rest to
   `_LIVE-STATE-ARCHIVE.md`.**
   → **Execute every move via `_gm_move.py` — the 2c pointer's contract, same mover, same ops file.**
   *(Added 2026-07-26 — dream-pass P1, Dave ruled accept-enact-now. First
   roll same day cut `_LIVE-STATE.md` 205KB→62KB; it had exceeded a single Read call.)*
   Exact sibling of 2c: at each wrap that adds a new ⏱ LATEST delta, move every delta older than
   **LATEST + 2 PRIOR** into `_LIVE-STATE-ARCHIVE.md` — **verbatim, newest-first, a move never a
   rewrite** — and trim the *Last refreshed* `Previous:` chain at the same boundary (tail appends to
   the archive's chain section). Same precondition as 2c: rolled deltas are convenience copies — the
   durable WHY/rules must already live in `_DECISION-HISTORY/`, ledgers, notes or git before rolling.
   **Same EXIT CHECK as 2c** (dream-pass v2 P1): Dave-owed ⚠/⬛/AWAITING/OPEN-CALL items inside a
   rolling delta must live in a standing section before the delta moves.
   After editing `_LIVE-STATE.md`, run `python3 knowledge/_validate_standing_instructions.py` (STAND-002).

   **2e. Enforce the DO-FIRST contract — typed content · LATEST+1 roll · retirement tests.**
   *(Added 2026-07-27 — GM-D1(a) / GM-D2 / GM-D3(a). DO-FIRST had no roll rule and was, with the §C
   tail, absorbing ~97% of the file's growth.)*

   **What DO-FIRST may contain — four types, nothing else:**
   **(i)** the current worklist · **(ii)** live supersession notices whose target text is still visible
   on a live surface · **(iii)** closure tombstones inside their term (table below) · **(iv)** one-line
   POINTERS to standing canon — **never restated bodies.**
   ⚠️ **(iv) is the one that bleeds.** Throttle canon, model routing, known potholes, read-order — all
   inscribed in their own homes, all found restated here at length. That is recall creeping back into the
   file whose entire design is retrieval. A pointer is one line; if you are writing the third line, you
   are restating.

   **Roll:** at each wrap, strata older than **LATEST + 1 session** move verbatim to `_GM-ARCHIVE.md`,
   **EXIT CHECK first** — the same check as 2c, not a second one; do not re-derive it.
   → **Execute every move via `_gm_move.py` — the 2c pointer's contract, same mover, same ops file.**
   **Cap: 120 lines (warn) · 180 (block).** A contract-compliant DO-FIRST runs ≈ 60–80.

   **The retirement tests — the answer to "when does this stop earning its place?" (GM-D2, all four):**

   | Notice type | Dies when |
   |---|---|
   | **Supersession** (*"X is DONE, stop planning it"*) | It lives **exactly as long as the text it negates remains on a live surface** (GM or `_LIVE-STATE.md`; archives excluded). When the dead stratum rolls, **the notice rolls with it, in the same batch — they are one move.** A warning label may not outlive the thing it warns about, and must not die before it. |
   | **Closure tombstone** (*"✅ CLOSED, do not re-open"*) | Term = **LATEST + 2 sessions** (mirrors 2d). To persist beyond term it must name a **structural guard** — a gate that enforces the closure, or a ledger closed-register line. After term it rolls and §C keeps one aggregate line. ⚠️ **A tombstone that must live forever is evidence a gate is missing** — gate-don't-patch, applied to the record itself. |
   | **Record correction** (*"the collision DOES NOT EXIST"*) | Same test as a supersession notice, **plus** the correction must be struck through **at the source of the wrong claim** before the notice may roll. Otherwise the wrong claim outlives its own correction. |
   | **Perishable reading** (pace/panel, quota, counts) | **Replaced at the next wrap, never stacked.** Already dated. A second reading beside the first is two readings, not a history — if the delta matters, the delta is the finding and gets written as one. |

   **Why tests and not judgment:** notices had no lifecycle, so nothing could ever retire, so the only
   legal way to kill text was to pile a notice on top of it — **supersession by addition**, under which
   dead spec *and* its warning label both bill full price on every cold read. Each test above keys on
   something **checkable** — is the target still visible? has the term elapsed? is the source struck?
   is it dated? — which is what makes this a checklist instead of a memory feat.

   **Lifecycle tags (GM-D3(a)) — on NEW entries only.** Every new notice or tombstone carries one
   machine-readable suffix so the gate can list what is retirement-due:
   ```
   [born #12 · guards: <target> · until: <condition|session>]
   ```
   ⚠️ **Existing entries are NEVER retro-tagged.** That would be a rewrite of ratified text, and verbatim
   discipline outranks tidiness. They retire instead via **one supervised audit pass at first enactment**,
   checked one by one against the table above, with receipts in the batch header.

   **2f. Roll the stratum stack — GM keeps LATEST only.**
   *(Added 2026-07-27 — GM-D5(a).)*
   The pre-flight / post-mortem / commit-state blocks that accumulate under §C are a stratum generator
   with no roll rule: four sessions deep at ruling time, two of them hand-marked *"[SUPERSEDED — kept for
   the record]"*. **The author felt the pressure to roll and no rule licensed the move** — that phrase is
   the diagnostic signature. If you catch yourself writing "kept for the record", this is the rule you want.

   **The stack lives under an explicit marker, and one date-keyed block per session:**
   ```
   ### ⏱ SESSION STRATA
   #### <date> #<session#>
   ```
   **The stratum also carries `section-usage` + `section-sizes` lines** (#23, ruled 2026-07-28):
   emit sizes via `python3 knowledge/_gm_usage.py --sizes --session <N>`, self-report usage U/R/C —
   contract + vocabulary in that script's docstring, probe BLOCKING since #24. **And a
   `consult-receipts` line** (#25 — the KG forcing function, Dave mid-flight): the window's
   retrieval testimony, `> **consult-receipts #N:** "query" → id · id ; …` or the honest negative
   `none — <why>` — format lives in `_search_core.py` (the only copy), probe ADVISORY at birth
   (`_capture_gate.py::consult_receipt_probe`; promotion = Dave's word). One line each, no more here.
   *(Enactment detail, 2026-07-27 — flagged as such. D6(a) caps §C **"excluding the D5 stack"**, which is
   only checkable if the stack is delimited; **the stack being UNLABELLED is what let it grow in the first
   place**. This is the minimum mechanism that makes an already-ruled cap enforceable, not a new rule.)*
   ⚠️ **The exclusion does not make it un-governed** — that would be splitting buying headroom. §C's cap
   skips these lines; **D5's own rule governs them, and the gate counts BLOCKS, not lines: more than one
   is a FAIL.** "LATEST only" is the entire contract, and one block is what it looks like.

   **GM keeps the LATEST pre-flight/post-mortem and the LATEST commit-state** (the handoff's freshness and
   trust stamp). Everything older moves at wrap:
   - **post-mortems → `notes/_GAUGE-LOG.md`** — append-only, one block per session. These are
     **measurements, not narrative**: pre-flight estimate vs closed band, overrun and its cause. The
     throttle programme keeps reasoning from n=1; the log is what makes it a countable dataset.
     **Record-FIRST-then-quote (dream-pass-3 P1(a), ruled 2026-07-28):** the closed band is written to
     this record FIRST and the chat wrap message QUOTES it — one number, one source. The #18 block is
     the counter-example: record 52%, chat ~62%, nothing reconciled the two, and neither can be
     adjudicated after the fact.
     **A missing stratum is logged as a HOLE (P1(b), same ruling):** a session that writes no stratum
     gets a dated gap line in `_GAUGE-LOG.md`, the way #19's absence was flagged — the dataset's gaps
     stay visible to the next reader; #14's unflagged absence is what made them silent.
   - **commit-states → `_GM-ARCHIVE.md`**, under the same `<date> <session#>` batch key as 2c.

   **EXIT CHECK applies and it bites here:** a stratum carrying a lesson — e.g. *"the fork rule failed
   mid-enactment"* — must have that lesson inscribed in `_RUNBOOK-context-gauge.md` **before** the stratum
   may roll. A lesson living only in a post-mortem block is a lesson in a dated home, and dated homes do
   not count.

   ⚠️ **Splitting never buys headroom** (ADR-0015's phrase, ruled into GM-D8). Content may not escape a cap
   by moving to a new un-governed file: a new file must declare its own contract, or the gate fails.
   `notes/_GAUGE-LOG.md` is licensed here because this step declares its contract — append-only,
   measurements only, not in the read chain.

   ⚠️ **§A is the section most at risk, because it is the only one that doesn't change each session.**
   On 2026-07-18 a from-scratch rewrite of `GOOD-MORNING.md` reduced §A's standing-instruction note to
   the two words "Standing section", dropping both the carry-forward rule and Dave's reason for it —
   caught only because Dave asked. The instruction had been surviving *only* by being copied forward
   inside the file it governs, which is not survival, it is luck. That is why it is written here too:
   a rule that lives only in the artefact it governs dies the first time that artefact is rewritten.
3. **Update memory — AND mirror anything durable into the repo.** Any `feedback` / `project` / `user` /
   `reference` memory that's new or changed this session, plus the one-line pointer in `MEMORY.md`.
   Check for stale memories the session disproved and correct or remove them.
   **Provenance fields on memory files (2026-07-26, Memento §4.1 — D1a):** every new/changed memory
   file gets two keys under its existing frontmatter `metadata:` — `provenance: <session-id> · <date>`
   and `status:` (same five-value vocab as step 1b). ⚠️ **Ritual discipline, NOT gate-enforced** — the
   store is invisible to every gate (below), so the session checks these by hand here, at this step.
   Per the gate-glob-scope rule the enforced rule is only as wide as `_capture_gate.py`'s repo-side
   glob; claiming the memory side is "gated" would be a false inscription. With provenance pointing
   back to the session/dossier, inline "Why:" justification prose can shrink to the fact + the
   pointer — the reasoning is retrievable, not re-inscribed. Status words in `MEMORY.md` index hooks
   are NOT deletable (the hook is what's loaded at recall — trust-the-spine).

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
   was ~15% of it). So the wrap delivers **two** names — but they go to **two different places**:
   - **RENAME THIS SESSION → `<retrospective title>`** — what it turned out to be, written with hindsight.
     **DELIVERED IN CHAT AT WRAP, never written into `GOOD-MORNING.md`.** ⚠️ **AMENDED — ruled Dave #28,
     2026-07-28 (post-wrap addendum, step 5b), superseding the both-names-at-the-top instruction above.**
     The reason: the rename applies to the conversation that is ENDING, so a cold reader of the next
     handoff can do nothing with it — it was billing cold-start tokens to every future session to carry
     an instruction only the outgoing one could act on. **ENACTED here #30** (owed since #28; the ruling
     had been living only on a rolling banner, which the 2c EXIT CHECK caught one wrap before it rolled).
   - **NEXT SESSION TITLE → `<forward title>`** — the opener for tomorrow. **This one stays at the TOP of
     `GOOD-MORNING.md`**, where Dave acts on it first, not buried at the bottom.
   Write both as ready-to-use lines, not as suggestions needing reformatting. Claude cannot rename a
   conversation itself — no tool for it — so the line exists to make Dave's action one copy, not a
   re-read of the whole handoff to work out what the session became.
   ⚠️ **Title SIZE is a DISCIPLINE, NOT A GATE — ruled Dave #28** (*"not a hard cap if it impacts
   context… not necessarily a strict cap"*), knowingly exceedable when a longer title aids HIS recall.
   He flagged unease at an ungated rule and was right: #28 broke it by 19% (295→352 tk) in the session
   that made it, and MEASUREMENT caught it, not a gate. **An ADVISORY report that names the size and
   never fails is offered and remains HIS call** — un-blocked, not ungated. Still owed as of #30.
   ⚠ **Titles are LABELS, never role assignments** (2026-07-21: a forward title's `[conductor + 2
   workers]` seated a second conductor). If the coming session runs the parallel model, say so in the
   §C brief and let the ROLE come from Dave's opener line — and include the **DIVVY PLAN** (lanes ·
   model per lane · serial set · shared files assigned per lane) in the forward brief, per
   `_RUNBOOK-parallel-conductor.md`.

5. **Commit + push.** Claude commits in terminal with a paste-ready summary + description, clears any
   stale `.git/*.lock` files. **Dave pushes via GitHub Desktop only** — never terminal push, never a
   Desktop commit, Desktop closed while Claude commits (memory `git-push-method`).
5b. **Post-wrap addendum (dream-pass-3 P6, ruled 2026-07-28; applied to its own ruling the hour it
   was made, #21).** A ruling that lands AFTER the wrap gate has run gets an explicit addendum beat:
   append it to the ★ LATEST banner (a one-line "post-wrap addendum" under the banner is enough),
   re-run the wrap gate, then commit. The banner is the session record (GM-D4) — inscribing the
   tattoos while the record stays silent is how #21's hunt-list ruling went missing from its own
   session while #20's identical shape propagated; discipline, not design, is what made it a class.
   ⚠ Do NOT promote a spec/ledger to Polaroid duty in compensation (A-D3: the spec stays the single
   source); the beat only makes the record SAY the source changed.

## What "done" looks like

All steps complete = the session is safely captured. The transcript never has to be the source
of truth — a cold-start agent can reconstruct full context from `GOOD-MORNING` → `_LIVE-STATE` →
`knowledge/README.md` → `MEMORY.md` alone.

## The gate (`_capture_gate.py` — BUILT 2026-07-26, Memento §4.1; rulings D1a/D2/D3 `notes/_MEMENTO-DECISIONS.md`)

One script (D3), two modes:

- **Build mode** (default — wired into `_build_all.py` with its selftest, **blocking**):
  provenance/status fields on new capture surfaces — `notes/YYYY-MM-DD-*.md` (non-underscore)
  and `_DECISION-HISTORY/YYYY-MM-DD-*.md`, dated ≥ **2026-07-26** (cutover — gate the flip,
  don't chase history). FAIL: missing `status:` · unknown value · `ruled` without a ledger
  pointer · `provenance:` with no parseable date. WARN: missing `provenance:` (session-id is
  soft) · ruled-pointer matching no file.
- **Wrap mode** (`--wrap` — **the session runs it at this ritual's close**, not the build):
  adds the original capture checks — FAIL if `_LIVE-STATE.md` "Last refreshed" ≠ today or
  `GOOD-MORNING.md` header ≠ today; WARN on uncommitted changes.
  **Plus, since 2026-07-27 (GM-D8(a)/D7(a)), the section growth contracts:** per-section line counts
  for `GOOD-MORNING.md` (DO-FIRST 120/180 · §C 150/225, §A exempt and unmeasured) and the chain size
  stamps (GM ≤ ~8K tk · GM + `_LIVE-STATE.md` ≤ ~24K tk). **WARN at cap · FAIL at cap + 50%.**
  ⚠️ **Wrap mode, not build mode, and the reason is sequencing:** these budgets describe the state the
  *wrap* must leave behind. In build mode they would fail every build from the moment they shipped until
  the first compaction pass ran — a gate red for a reason no build can fix. Wrap mode is still blocking
  in its mode (the "Last refreshed" check FAILs; none of this is advisory).
  ⚠️ **Failure text names the runbook step and nothing else.** No advice list, no "now do X" — that prose
  ages while the exit code doesn't, and a stale `print()` inside a gate has already sent one session to
  redo finished work (2026-07-27 #7). **The exit code is the evidence; this file is the advice.**
- **Honest scope (D1a):** the memory store is invisible to the shell and to every gate (step 3)
  — dangling `MEMORY.md` pointers and memory-file fields are checked *by the session, by hand,
  at step 3*. The script prints this as an explicit SKIP so the boundary can't silently blur.

Green = safely captured. The wrap-mode run replaces nothing in this runbook — the ritual is
still the sequence; the gate is its receipt.

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
