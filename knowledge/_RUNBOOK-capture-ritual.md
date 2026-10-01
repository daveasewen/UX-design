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

**Also run it mid-session at the IN-FLIGHT STOP LINE — `60 − the priced wrap`, NOT at a reading of 60**
(~50–52 at today's 8–10 point wraps; `_RUNBOOK-context-gauge.md` § ds-023). ⛔ **60 IS WHERE THE WRAP
HAS FINISHED, NOT WHERE IT STARTS.** ⚠ **THIS LINE USED TO SAY "when the gauge reads Red (≥60%)" and
that was WRONG** — it put the entire wrap price on top of 60, which is #28's and #29's recorded cause.
Corrected #54 on Dave's own words: *"the 60% is the total with the wrap included, it was never supposed
to be 60 plus wrap."* ★ The stop line MOVES with the wrap price and is not its own constant — an
expensive wrap must stop the session earlier. Don't wait for a natural end.
The gauge (`_RUNBOOK-context-gauge.md`) exists precisely to fire this ritual *while there's still
clean budget to author the handoff well*; a `GOOD-MORNING.md` written at 95% full is the confidently
wrong handoff we most want to avoid. Red cue line, ready to use:
> **Title this chat: `<retrospective title>` — context is Red (~NN%). Running the capture ritual, then
> open fresh with: `<forward title>`.**

## The steps, in order (1, 1b, 2, 2c, 2d, 2e, 2f, 2g, 3, 4, 4b, 4c, 4d, 5, 5b)

*Steps **2e** and **2f** were added 2026-07-27 (GM-D1…D9, `notes/_MEMENTO-DECISIONS.md` § GM
growth-contracts ruling). They extend the 2c/2d pattern — cap + archive sibling + verbatim move +
EXIT CHECK — to the two `GOOD-MORNING.md` regions that had no roll rule and were therefore absorbing
~97% of the file's growth. **The architecture in one line: every GM section declares a growth contract
(what it may contain · cap · roll target · retirement test); §A alone is standing and uncapped.***

### ★ PHASE 1 — THE WRAP RUNS TOOLS, NOT SCRIPTS (`s306-D4`, #306, 2026-09-28; added by addition — no step below is rewritten)

Dave, 16:58 BST, *"go on both"*, to *"Build phases 1 and 2 now: turn the wrap's throwaway scripts into permanent tools"*
(`notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md`). Built by #306 lane W1 (`notes/_subreports/2026-09-28-306-W1-phase1-tools.md`).
Each step below still says WHAT to write; this says HOW. **Write no script in `_work/`: every command takes files and arguments.**
Each tool: `--help`, `--selftest`, dry run unless `--write` / `--run`. `s306-D4` stays `ruled` until one real wrap proves
scripts 11 → 0, move files 9 → 1, rebuilds 5 → 1 (#305's counts).
> ★ **#307 ADDITIONS (Dave, Mon 2026-09-28 19:58 BST, `notes/_lanes/307/DAVE-WORDS-2026-09-28-1958.md`; nothing in this block is rewritten):**
> 1. **The rebuild target is 1 PER COMMIT, not 1.** The 5b follow-up commit needs its own rebuild, because its line lands in the ⏱ delta that `_CHAIN.md` slices. That is intended. #306 met it: 1 for the wrap commit, 1 for the 5b.
> 2. **`_wrap_regen.py` now runs 4b itself** (`_gen_titles.py --session N`, its step 0) **and REQUIRES `--session N`**: `_wrap_regen.py --run --session N --log … --paths-out …`. Without it, the tool refuses before anything writes. Do not run `_gen_titles.py` by hand. The verdict calls the titles receipt STALE unless it was written for session N.
> 3. **Placeholders: write `{{SECTION_SIZES}}` / `{{ROLL_STATE}}` bare on their line.** Both generated lines already start `> `. `_wrap_ops.py` now folds a `> {{…}}` at the start of a line into ONE `> `, so it can no longer come out `> >`, but bare is the form.
> 4. `_wrap_commit.py` flushes every print, so its lines stay in order when its output goes to a file.

| step | command |
|---|---|
| every figure (fill, subs, rulings, store, carries, sizes, shas) | `_wrap_facts.py --out <n>/W/FACTS.json --session N --rulings-base <opener sha> --since <last wrap sha> --transcript <conductor jsonl> --until <launch ISO> --subagents-dir <dir> --exclude <own jsonl>` |
| 2, 2c, 2d, 2f (banner, rolls, stratum, delta, stamp, title) | prose in files (a line `{{SECTION_SIZES}}` / `{{ROLL_STATE}}` is measured for you) → `_wrap_ops.py --session N --date D --banner --stratum --delta --stamp [--title] [--date-split] --out <n>/W/_ops-NW.json` → `_gm_move.py --ops … --dry-run`, then without |
| carries | `_wrap_carries.py roll --from N --to N+1 --new new.txt` · `strike --section N+1 --title '**…**' --note-file f` · `count`; `--write` to write |
| state rows | `_wrap_rows.py --spec rows.json`, then `--write` (mint born closed, close/reopen by addition) |
| 2g, 4b titles, 4d, the chain | `_wrap_regen.py --run --log <n>/W/_regen.log --paths-out <n>/W/paths.txt` — ONCE, after the last edit |
| 5 | `_wrap_commit.py msg --out … --line1 …` · `paths --out … --dir notes/_lanes/<n>/W …` · `commit --session N --msg … --paths … --log …`; a stranded lock: `unlock --tag <n>-W` |
| 5 CI, 5b | `_ci_readback.py` (block below, `s306-D7`) · the 5b line: `_wrap_ops.py --fill-token … --fill-file _LIVE-STATE.md --fill-text 5b.md --out …` |

(`<n>/W` = `notes/_lanes/<n>/W`; every tool is `python3 knowledge/<tool>`.) Unchanged: `_gm_move.py`, `_roll_state.py`,
`_gen_size_stamp.py --write`, `_state.py`, `_capture_gate.py`, `_git_commit.sh`. Still hand-written until phase 3: the prose (handoff, dossier,
W report, memory payload, summary). ★ #312: phase 3 is BUILT — see `★ PHASE 3` below; the prose becomes ONE story file and every view is generated.

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
   - **The NEXT SESSION TITLE first** (see step 4b) — the forward title, and only that, at the very top.
     ⚠️ **AMENDED — ruled Dave #28, 2026-07-28, enacted #30: the RETROSPECTIVE RENAME is delivered in
     CHAT at wrap and is NEVER written into `GOOD-MORNING.md`** (it applies to the conversation that is
     ENDING, so a cold reader can do nothing with it). The superseded *"two names first — rename + next
     title, at the very top"* instruction stood here unamended for 37 sessions and was quoted back at
     Dave as live authority at #71, sixteen lines above the amendment that killed it. Full text: step 4b.
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
   - **The read-chain contract, stamped in the file (GM-D7(a) — ★★ AMENDED 2026-07-28 #33: GM-D7-am
     CUT on Dave's ruling).** ⚠ **This step said, until #33: "chain (GM + `_LIVE-STATE.md`) ≤ ~24K tk".
     That referent is retired.** The chain is now **header → ★ LATEST banner → the ⏱ LATEST delta of
     `_LIVE-STATE.md`** — measured **3,487 tk cl100k / ~5,405 charged / 2.6 pts** at the cut, down from
     **34,094 / 52,846 / 26.4 pts**. **§A and §C STAY IN THE FILE**; they left the CHAIN, not the record,
     and are reached by `_memento_search.py "<q>"` → `--fetch <id>`. *(The old wording was found by #33
     while following this very step — the assertion-propagation class: a doc known-wrong-now that
     nothing chases. Amended in the same pass that made it wrong.)*
     GM still states its own budget and the chain's, both files carrying a gate-checked size stamp so
     drift is visible rather than discovered; the wrap publishes **the CORPUS beside the chain, always**,
     because the cut DEFERRED 34K tokens rather than deleting them. **Everything cited
     beyond the chain is RETRIEVAL** — `_consult.py`, a grep, a targeted read — **never a reading list.**
     ⚠️ The old open-ended *"then the decision files it points to"* was a selective instruction pretending
     to be complete: the chain cites 112 asset paths, ~312K tk resolvable, 1.5× a window. Say the
     selectivity out loud or the next cold reader will try to obey it.
     **The stamp, in the file's header block, one canonical form** (the `K` is required — without it
     `GM 25618 tk` parses as 25.6M and passes a drift check by accident):
     ```
     > **size:** GM 25.6K tk · chain 43.5K tk · measured <date> (tiktoken cl100k_base)
     ```
     ⛔★ **THE FIGURES ARE NOT TYPED — RUN THE GENERATOR. `s294-D8` (Dave, ruled #294), the same ruling
     shape as `s125-D1`:** the GM / LS / corpus figures, their unit word and the `measured <date>` date are
     written by a script, **at this step, DECLARE-LAST**, with the fixed-point iteration included (the stamp
     measures a region that contains it, the #240 lesson):
     ```
     python3 knowledge/_gen_size_stamp.py --write     # then read its stdout into the residual
     python3 knowledge/_gen_size_stamp.py --check      # the build step (`_build_all.py`, wired #294)
     ```
     ⚠️ **It writes ONLY the figures, the unit word and the date** — every other word on that line, including
     the drift narration and the §A probe, is yours. **§A is NOT generated** (a different instrument,
     `_gm_usage.py`; the two are never reconciled or averaged) and **neither is the session ordinal** (a label,
     not a measurement). ⚠️ If it REFUSES (exit 77 `COULD-NOT-ASK`, or an oscillation refusal) **publish the
     refusal in the residual and do not hand-type the figure it would not write** — that is the act the ruling
     forbids by name, and `--check`'s form arm reports it.
     The gate **measures the file and checks the stamp against its own measurement** (>10% drift = FAIL),
     so a stale stamp is caught rather than believed. ⚠️ **Measure, never convert by rule of thumb:** this
     corpus runs at **3.53 bytes/token**, not the customary 4 — its ★ ⚠ ⛔ · — load makes it ~13% denser,
     so every chars/4 estimate of these files has read LOW, including the ones in the proposal that set
     the budget.
     ⚠️ **DECLARE-LAST, AND DECLARE THE SIZE OF WHAT YOU SKIPPED — ruled Dave 2026-08-02 (dream pass 4,
     P7 "ACCEPTED, smallest version"), enacted #128. NO GATE.** The stamp is written LAST, after 2c/2d/2f
     have run, because those steps change the very files it measures. **When 2c, 2d or 2f are SKIPPED, the
     residual may not simply say they were skipped — it must state the SIZE of the skip:** that the `size:`
     stamp being carried is therefore the PRIOR session's (#N−1's), and roughly how far the artefact has
     moved since — a re-measure is one call, `chain_file_tk('.')`. *Why: "skipped 2c" reads as
     housekeeping; "the stamp is #N−1's and the chain has moved by roughly X since" reads as what it is —
     a number in the read chain that is no longer about this session's file.* ⚠️ **Flagged by Dave at the
     ruling itself: this is the third or fourth "declare it in the residual" clause. Watch the residual
     becoming the place things go to be declared and then forgotten.**

   **2c. Compact the banner stack — keep ★ LATEST + 1 PRIOR, roll the rest to `_GM-ARCHIVE.md`.**
   → **Execute every move via `python3 knowledge/_gm_move.py --ops <ops.json>` — never hand-edit a roll** (M5, 2026-07-28: line-START anchors · §A digest asserted · caps imported, warn ≠ block · all-or-nothing · stdout receipts).
   ⛔ **THE OPS FILE IS A MSGFILE — GIVE IT A UNIQUE NAME AND ASSERT IT EXISTS BEFORE THE MOVER READS IT.**
   *(Inscribed at the #166 wrap's EXIT CHECK, from the defect #165 caused and repaired: a heredoc to a
   shared fixed path `/var/tmp/ops1.json` failed with `PermissionError` while the command chain
   continued, and the mover consumed a **STALE ops file from #139** and printed **green receipts for
   someone else's ops**.)* ★ **This is the stale-msgfile trap of `_RUNBOOK-git-commit.md` in a different
   tool — same shape, same cause: a shared `/tmp`-class path, a fixed name, and a write failure that does
   not stop the chain.** Write the ops from a **session-owned, uniquely-named** path, assert
   `os.path.exists` + a size floor **in the writing process**, and read the receipts back against the
   ops you meant to run. ⚠ **The only working restore on this mount is `git show <sha>:<path> > <path>`.**
   ⚠ **And the sibling, banked #166: `git stash@{N}` INDICES RESHUFFLE after every `git stash drop`** —
   a drop-by-index dance loses the wrong entry. For reading a file as it was at another commit, use
   **`git show <sha>:<path>`**, never a stash sequence.
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
   ⚠️ **EVERY CARRIED ITEM IS WRITTEN WITH ITS AGE — ruled Dave 2026-08-08 (#128, dream pass 5 P2).
   FORMAT ONLY: no threshold, no cap, no gate.** An item carried on a banner or in a residual gets a
   bracketed age in **sessions since it was ruled or declared**, immediately after its id — e.g.
   `89-D2 [38]` · `ds-021 [74]` · `P7 [52]`.
   *Why: a carried item reads identically at one session old and at thirty-eight. The age is the only
   part of a carry a cold reader cannot reconstruct, and it is the part that decides whether the carry
   is a hand-off or a fossil. Writing it costs a bracket; NOT writing it is how "89-D2, still owed"
   survived thirty-eight wraps without anyone reading the number that made it alarming.*
   ⚠️ **The age is REPORTED, never ACTED ON here** — no age triggers anything, nothing expires, and
   nothing may be dropped for being old. What to do about an old carry is Dave's, every time.
   ⛔ **A RETRACTED CARRY IS STRUCK, NEVER RE-TYPED — ruled `s183-D1` (dream pass 8, P2).**
   **"WORDING UNCHANGED holds for every carry EXCEPT one whose claim was corrected or retracted
   since it was written; a retracted carry is struck with its retraction named (session + where
   the correction is inscribed), never re-typed."**
   *Why: the 2c EXIT CHECK verifies PRESENCE — that nothing was orphaned — and has no test for
   TRUTH. A correction is the one event that MUST change wording, and "AGES +1, WORDING UNCHANGED"
   forbids exactly that [[invariant-cannot-discriminate-reversal]]. #181 asserted the Monday slot
   was unscheduled · #182 retracted it (Dave caught it) · #183 re-published it verbatim at a
   correct age. Struck, not deleted: a silently vanished item is indistinguishable from a dropped
   one, which is what the EXIT CHECK exists to prevent [[feedback-header-wins-over-audit]].*
   ⛔ **AND THE RETRACTION MUST CITE ITS RECEIPT — ruled `s188-D2` (#188), a STRENGTHENING
   AMENDMENT to `s183-D1` P2, not a reversal.** A carried claim's wording may change ONLY to
   record a retraction, and the edit must name **the session that proved it false AND where the
   correction is inscribed** (a ruling id, a repo path, or a commit sha) — the same way a repo
   claim cites `git log`. **A wording change without a receipt is REFUSED at the wrap.**
   *Machinery, built #189: `carry_wording_check()` in `knowledge/_capture_gate.py`, BLOCKING,
   wired inside `wrap_checks()`. It pairs each aged carry on the ★ PRIOR banner's `residual → #N`
   line with the same carry on ★ LATEST (`[N]`→`[N+1]`, matched on the title before the em dash),
   passes identical wording silently, and quotes both texts when it refuses. ⚠ It does NOT see a
   DROPPED carry — that is this step's EXIT CHECK above, which stays prose. ⚠ Nor does it see a
   carry made BY REFERENCE ("PRIOR CARRIES, AGES +1, WORDING UNCHANGED" pointing at the PRIOR
   banner instead of re-typing the list); it DECLARES that case unmeasured rather than reporting
   a clean run. Measured before it was wired: 11 un-receipted rewordings across the ten wraps
   archived before #189, every sampled one a carry truncated as it aged, dropping the evidence
   pointer it was born with.*
   ⛔ **THE CARRY SET DOES NOT GO ON THE BANNER ANY MORE — IT GOES IN `_CARRIES.md`, AND THE
   BANNER GETS A POINTER + A PROBEABLE COUNT. RULED `s225-D2` (Dave, #225).**
   *The measurement that forced it: at #225 the carry line was **24,873 tape — 89.3% of the whole
   ★ LATEST banner**, and because `_gen_chain.py` slices that banner OUT of GM to build `_CHAIN.md`
   the line sat on **BOTH SIDES** of that generator's chain/GM ratio. The ratio read **52.5%**
   against a **`<40%`** floor and took CI red at build step 13. Dave's word: "the chain carry list
   moves to its own generated home with receipts; the banner carries a pointer + count."*
   **WHAT A WRAP DOES NOW, in place of re-typing the list onto the banner:**
   - **(i) Write the session's whole carry set into `_CARRIES.md`** as a new `## residual → #N`
     section, **NEWEST FIRST**, mirroring `_GM-ARCHIVE.md`. Everything 2c already demands still
     binds, unchanged and in that file: **AGES +1 · WORDING UNCHANGED · a retraction STRUCK with
     its `s188-D2` receipt · nothing dropped for being old.** ⛔ **The home changed; the rules did
     not.** If a carry line already stands on the banner, **MOVE it — `python3
     knowledge/_gm_move.py --ops <ops.json>`, one `{"op": "move"}`, byte-identical, receipt on
     stdout — never a copy-then-delete and never a hand-edit.** (`_CARRIES.md` already exists, so
     the mover's "NEVER creates a file" rule is satisfied; if it is ever absent, **STOP** — write
     its contract header first.)
   - **(ii) Put ONE pointer line on the banner**, at line start, keeping the `> **residual → #N:**`
     home form — **three gates and one generator find the hand-off by that prefix and a pointer
     that drops it silently breaks all four**. The line carries, in this order: the **⬛ top item's
     headline** (⚠ **`_gen_titles.py` derives NEXT-TITLE from the first ⬛ bullet's bolded clause on
     this line — it is the ONE piece of the carry set that must stay on the banner, and
     `title_generation_check()` is BLOCKING**) · the **path** `_CARRIES.md` and its section · the
     **retrieval id** `carries:residual-<N>` · the **count** · and **the command that recomputes
     the count**, because a typed count is a claim and this one gets probed
     [[roll-pointer-is-not-an-absence]]. The count's ONE definition is the gate's own:
     `_capture_gate._carry_items()`. Copy the #225 pointer line's shape verbatim; do not invent a
     second form.
   - **(iii) Re-stamp `size:` (step 2, which already runs LAST).** Moving the carry set takes tens
     of thousands of tape out of GM in one line; the stamp is graded against the gate's own
     measurement at 10% tolerance and would fail loudly on the old figure.
   ⚠ **DECLARED, NOT DISCOVERED LATER — `carry_wording_check()` ABOVE IS NOW BLIND, AND IT GOES
   QUIET RATHER THAN LOUD.** It pairs `[N]`→`[N+1]` between the **GOOD-MORNING.md** ★ PRIOR and
   ★ LATEST residual lines. With both lists in `_CARRIES.md` there is nothing on those two lines to
   pair: at #225 it still says *"NOTHING PAIRED — ⛔ THAT IS NOT A PASS"* because the PRIOR banner
   still holds #224's list, but from #226 both sides are empty and it reports a clean-looking
   `0 aged carries`. ⛔ **Re-pointing it at `_CARRIES.md`'s two newest sections is OWED and is not
   done** — [[instrument-without-a-consumer]]; scope, the exact change and the reason it was not
   made in the same motion are in `notes/_subreports/2026-08-30-225-carries-home.md`. Until it
   lands, **the `s188-D2` invariant is prose again, and a wrap must hold it by hand.**
   ⛔ **AND THE RATIO THIS MOVE FIXED WILL COME BACK RED AT #226 — MEASURED, NOT FEARED.** The
   `<40%` assertion divides the WHOLE `_CHAIN.md` file by the WHOLE of GM, and **12,741 tape of
   that file is `_gen_chain.py`'s own wrapper — a FIXED cost, in the numerator only, that no edit
   to GM or `_LIVE-STATE.md` can move** (the generator says so itself in the warn it prints).
   After this move GM reads **62,569** and the chain **21,346 → 34.1%**. At the next wrap the
   #224 ★ PRIOR banner (**27,210 tape**, most of it its own carry line) rolls to `_GM-ARCHIVE.md`
   and GM falls to **≈38,700** while the chain barely moves: **≈55%, RED again.** ⛔ **A leaner GM
   makes this ratio WORSE, which is the whole trouble with it** — so do NOT reach for the carry
   move a second time, and do NOT touch the `0.40`: that is Dave's constant. The remaining lever
   inside the machinery is the **wrapper** itself. Priced and open — see
   `notes/_subreports/2026-08-30-225-carries-home.md` § RULING-SHAPED QUESTIONS.
   ★ **The circled numerals number THIS session's new items only; carried items are identified by
   age** (`s183-D1`, dream pass 8 P3 — prose form; carried blocks arrive with their own ①–⑦ and
   collide with the session's, so the age bracket `s128-D2` defines is the durable identifier).

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

   **2g. Rebuild the retrieval index — LAST, after every GM/LS edit is final.**
   *(Added 2026-07-28 #32. Order is the whole point: the index must be built from the files as they
   will be COMMITTED, not as they were when the session's last `_build_all.py` ran.)*
   ```
   python3 knowledge/_build_memento_index.py     # built, NEVER staged — gitignored since s312-D1
   ```
   ★ **#312 (s312-D1): the index is built, never committed.** `knowledge/_memento-index.json` is in
   `.gitignore`; the opener (`ensure_env.sh` step 5) and CI's gates job build it. Run the command so the
   local copy the later regen steps read is fresh, and do NOT stage it (git refuses the ignored path;
   `_wrap_regen.py` names no output for this step). The freshness check below still refuses a stale
   local copy at the wrap.
   **Why this step exists, measured at #32's opener:** `_memento_search.py --fetch gm:LATEST` returned
   **#29's banner** while the file carried #31's — because the index regenerates inside `_build_all.py`
   and the wrap rewrites GM/LS *afterwards*. Retrieval was structurally one session behind, and
   RETRIEVAL-FIRST is standing: the door was confidently quoting a superseded record.
   ⚠️ **Deeper cause, and the reason this is a gated step and not advice:** the index could not rebuild at
   all — #30's ds-022 repair wrote a `#### ` block in a form the builder refuses, so `_build_all.py` was
   **RED for two sessions and both wraps committed over it, because the wrap gate does not run the build.**
   `_capture_gate.py::index_freshness_check` now closes that: it rebuilds in-process and byte-compares,
   **BLOCKING**. If it fires, run the command above — do not close over it.
   *(It compares CONTENT, never mtimes: an mtime check reads green on a reverted file.)*

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
     ⛔ **THE PRE-FLIGHT LINE IS GENERATED NOW — DO NOT HAND-TYPE IT AND NEVER COPY THE PREVIOUS
     SESSION'S (#293, dream pass 9 P1).** `python3 knowledge/_checkin.py --preflight-line <N>`
     prints the line, reading the CONDUCTOR'S top-level transcript at
     `/sessions/*/mnt/.claude/projects/*/*.jsonl` — which a sub seat CAN read, and always could.
     The arm appends to no log and logs no grade row, so taking the reading moves no counted
     dataset; paste what it prints. ★ Why this exists: the hand-typed `⛔ NOT CAPTURED` ran for
     **93 consecutive sessions (#199 → #291, 185 occurrences)**, each one copying the last with
     the ordinal bumped (*"Reason unchanged from #199…#<n-1>"*), and the stated reason — *"a sub
     cannot read its own `message.usage`"* — was answering a question nobody asked: the line
     wants the CONDUCTOR'S window, not the sub's price. Several of those same strata say
     `_checkin.py` WAS run on the conductor's transcript in the paragraph that refuses.
     ⚠ **The refusal form survives and is still legal** — but it must name the cause the arm
     ACTUALLY met at the moment of the call, in one clause. A bare "NOT CAPTURED" is the defect.
     ### ★ THE OPTIONAL `subs` LINE IN A GAUGE-LOG BLOCK (Dave #168, option 2 — "small gate")

     A block MAY carry ONE extra line recording what the session spent on **delegated subs**:

     ```
     subs <N> tokens (n=<count>)          e.g.   subs 128,400 tokens (n=3)
     ```

     - **`<N>` = total delegated sub tokens for the session**; `<count>` = how many subs. Both are
       **positive integers**; comma-grouping is allowed in `<N>`. Bold/quote markdown around the line
       is fine (`> **subs 128,400 tokens (n=3)**`).
     - ⚠️ **UNIT: REAL Claude tokens, and they are QUOTA — not window FILL.** A sub is nearly free in
       this window's budget and 5–10× in the weekly quota [[budget-vs-quota-vocabulary]], so this
       figure is **never added to the block's fill numbers and never graded against the stop line**.
       It answers a different question: what did delegating actually cost.
     - ⛔ **ABSENT IS LEGAL, AND ABSENCE IS NEVER DEFAULTED.** A wrap with no sub figures — no subs,
       or subs whose cost was not measured — **writes nothing**. There is no zero-line and no "n/a"
       line; an UNKNOWN is never turned into a number [[feedback-measuring-tool-must-not-guess]].
       ⚠️ Do NOT delete a line you have figures for, and do NOT invent figures to satisfy the gate:
       a missing line is honest, a wrong number is not.
     - ⛔ **The word `job` MUST NOT appear anywhere on this line.** This is containment, not style:
       `gen_dashboard.py`'s `_JOB_RE` (`\bjob <number>\b`) sweeps this whole file and every match
       becomes a datapoint in the corpus the **S/M/L effort-rung band edges** are derived from. A
       subs line spelled with `job` would move a band edge **silently** — no error, no crash, no
       reader [[instrument-without-a-consumer]].

     **And the guard on it (`_capture_gate.py::gauge_log_subs_line`, BLOCKING at birth):** when the
     line is ABSENT the check is a silent pass that says so; when it is PRESENT it must match the form
     exactly, or the wrap fails with a NAMED refusal that quotes the expected form back. `job` on the
     line is its own named refusal. ⚠️ The tier is a DECLARED choice (`SUBS_LINE_BLOCKING`), not a
     ruling — Dave ruled the line and the gate; blocking is chosen because the damage it prevents is
     invisible. There is **no writer** for these blocks: the conductor hand-writes them, and every
     production path only READS this file.

     ### ★ THE DELEGATED-WRAP CONDUCTOR-COST LINES (`s214-D5`, 2026-08-21 — closes the schema hole the #212 mining named)

     A gauge-log block for a **DELEGATED** wrap carries these terms, each MEASURED or declared
     `unobservable (<reason>)` — never omitted silently, never guessed
     [[feedback-measuring-tool-must-not-guess]]:

     ```
     wrap-handover: brief-cut <N> real (conductor) · sub-cut <N> real (first-hand) · delta <N> real · replay <N or unobservable (<reason>)> real
     ```

     - **brief-cut** = the conductor's FILL when the wrap brief was cut (the conductor DECLARES it in
       the brief). **sub-cut** = the wrap sub's own first-hand `_checkin.py` reading of the
       conductor's transcript. **delta** = sub-cut − brief-cut (the hand-over's cost). **replay** =
       what reading the sub's report back cost the conductor, if measurable at write time — usually
       it is NOT (the wrap sub cannot see it), and `unobservable (conductor-side, post-wrap)` is the
       honest form; the conductor may append the measured figure at the NEXT opener.
     - ⚠️ UNIT: REAL tokens, FILL moments — stated separately, never summed, never averaged into one
       "wrap cost" [[measure-dont-convert-units]]. An IN-WINDOW wrap writes no such line.
     - WHY: the advisory-line re-derivation (`s214-D4`) is STAGED on this field reaching n≥2 — the
       hand-over reserve must be a measurement before it may replace the 49,071 wrap term.
     - ⚠️ No gate parses this line yet — the consumer is the `s214-D4` staging check and the re-base
       sitting, both human-read. A `_capture_gate.py` guard is a priced candidate, not built.
     - ⛔ **`delta` IS ONLY MEANINGFUL WHEN BOTH TERMS READ THE SAME WINDOW — OTHERWISE IT IS
       `unobservable`, NOT A SUBTRACTION.** *(Homed here by ADDITION at the #272 wrap's 2f EXIT
       CHECK, from the lesson carried in #271's stratum before that stratum rolled; provenance:
       272 · 2026-09-15 · status: observed.)* `brief-cut` is the CONDUCTOR'S declared FILL and
       `sub-cut` is the wrap sub's own `_checkin.py` reading. The subtraction means something only
       when `_checkin.py` at the wrap seat is reading **the conductor's transcript** — the same
       window his declaration describes. #270 declared `delta` **unobservable** because its wrap
       sub read a separately-windowed transcript; #271 and #272 COMPUTED it (11,466 and 3,079)
       and each said which transcript and how many turns. ⇒ **Name the window, or write
       `unobservable (<reason>)`; never subtract two numbers that describe different things**
       [[measure-dont-convert-units]].
     - ⛔ **A STRAY'S PROVENANCE IS A SEAT LIMIT UNTIL IT IS SEARCHED** *(dream-11 P3(b), #256 — #247's
       wrap sub published "`_tools/` … provenance unknown" 11 times across 7 surfaces while #246's own
       chat names the directory, its build command and its purpose)*: a stray may be declared
       **UNCOMMITTED** from any seat, but it may only be declared **UNKNOWN** after
       `grep -rn "<path>"` over `notes/`, `_DECISION-HISTORY/` and the last two sessions' briefs
       returns nothing; otherwise write **"provenance not established from this seat"** — the honest
       form of a blind spot, never a claim about the world.

     ### ★ BANNER DISCIPLINE (`s214-D6` — the boot-reduction pair, half 1)

     Every wrap brief carries this clause: **the ★ LATEST banner is written toward a `_CHAIN.md` of
     ~10–12K real** (it measured 21,323 at #213 — doubled since #109, and the chain IS mostly the
     banner). The clause commands **SHORTER, never decide-what-to-drop**: a wrap sub compresses
     girth — tighter sentences, pointers instead of restatement — and NEVER omits an item, a carry,
     a declared skip, or a receipt name; roll-to-archive already preserves every prior banner
     verbatim, so nothing is ever lost by writing the new one tight. The chain's generated footer is
     the measurement; quote it at the wrap. *(Half 2 of the pair — MEMORY.md compaction at owed
     openers — lives in the memory-compaction mechanics, not here.)*
     ⚠ **AND QUOTE IT AFTER THE DECLARE-LAST `size:` STAMP, NOT BEFORE — the stamp is itself inside the
     chain slice.** *(Homed here by ADDITION at the #241 wrap's 2f EXIT CHECK, from #239's lesson
     re-observed at #240 inside a stratum that was about to roll into a dated home; provenance: 241 ·
     2026-09-02 · status: observed.)* #240 measured `_CHAIN.md` at **11,074 tape** mid-wrap and at
     **11,319** once the stamp landed — one wrap, two figures, and only the second is the one the next
     session pays. ⇒ **A wrap that shortens its banner can still hand the next session a BIGGER chain
     through its header**, so the `s214-D6` figure is RE-GENERATED after 2c/2d/2f and after the stamp,
     and that final reading is the one the stratum carries. ⛔ **Related, declared at #240 and still NOT
     repaired:** `grep -c 'BANNER-DISCIPLINE MEASUREMENT' notes/_GAUGE-LOG.md` and the newest ORDINAL
     NAMED in that file disagree by two — the count is re-derivable, the naming is not. Report both; do
     not invent a third.

     ⛔ **`> **COMMIT STATE` IS NO LONGER A UNIQUE ANCHOR IN `GOOD-MORNING.md` — DRIVE `roll_2f` WITH THE
     SESSION-QUALIFIED FORM `> **COMMIT STATE #<N>:**`.** *(Homed here by ADDITION at the #241 wrap's 2f
     EXIT CHECK; measured at #240 and re-measured at #241 — `grep -c "^> \*\*COMMIT STATE" GOOD-MORNING.md`
     reads **4**: the rolling stratum's, plus the three EXEMPT #40/#41/#42 blocks (Dave's #58 ruling).
     Provenance: 241 · 2026-09-02 · status: observed.)* The bare anchor in the `roll_2f` example above
     matches all four, and the mover REFUSES it — correctly, and loudly.

   - **commit-states → `_GM-ARCHIVE.md`**, under the same `<date> <session#>` batch key as 2c.

   ### ★★ ds-022 (ENACTED #34) — THIS ROLL IS NO LONGER DONE BY HAND

   **Run it through the mover.** One op, and it is the only supported way:

   ```bash
   python3 knowledge/_gm_move.py --ops - <<'JSON'
   [{"op": "roll_2f", "session": 33,
     "pm_start": "#### 2026-07-28 #33", "pm_end": "> **COMMIT STATE",
     "cs_start": "> **COMMIT STATE",    "cs_end": "## <the next heading>"}]
   JSON
   ```

   **Why it stopped being a hand-roll.** Measured #30: **#26, #28 and #29 rolled WHOLE into
   `_GM-ARCHIVE.md` and never reached the log** · **#9/#10/#11/#19 are absent with no HOLE line**, so the
   file cannot say whether a stratum ever existed · **#27's block was PREPENDED**, against this file's own
   append-only contract. Three wraps in a row got the same step wrong — the gate-don't-patch trigger.
   **#29 is the expensive loss:** the only 🔴 RED session on the board, the only one with a measured
   overrun cause, and its band lived on a Polaroid and never reached the tattoo.

   **What `roll_2f` makes impossible, rather than merely discouraged:** a half-done split (an empty half
   is refused, and nothing is written) · a prepend (**both destinations append at true EOF; there is no
   anchor argument, because that argument is what produced #27**) · a duplicate session key · a block
   appended behind a later one · a post-mortem with no `#### <date> #<N>` key, which would be invisible
   to the check below.

      ### ★ THREE STATES, NOT TWO (ruled by Dave, #34)

   | marker | what it CLAIMS | gate |
   |---|---|---|
   | a `#### <date> #<N>` block | the 2f split landed | passes |
   | **`HOLE #<N> — <why>`** | **that session wrote no stratum, and we know it** — a positive claim | passes |
   | **`ABSENT #<N> — …`** | **no block was found; whether one was ever written is UNKNOWN** — a claim about the RECORD, not the session | **WARNS** |

   ⚠️ **`ABSENT` IS NOT A POLITE `HOLE`.** #9/#10/#11/#19 had no block and no note; writing `HOLE` for them
   would have made this log read complete **at the price of four invented facts** — confident false
   inscription, committed in order to tidy a file. `ABSENT` makes them **countable as unknowns** with no
   fabricated cause, which is why the dataset now accounts for every session 6→33 with zero gaps.
   ⚠️ **It WARNS rather than passing silently, on purpose:** a silent `ABSENT` would become a free skip for
   step 2f — `HOLE` with the honesty removed. **If YOU wrote no stratum, the honest marker is `HOLE`.**
   After #34 there should never be a new `ABSENT`.

   **And the guard on it (ds-022 (a), BLOCKING at birth):** `_capture_gate.py::gauge_log_continuity` —
   **a wrap FAILS unless session N−1 has a block, or an explicit `HOLE #<N> — <why>` line**, in
   `notes/_GAUGE-LOG.md`. ⚠️ **The HOLE hatch is load-bearing, not politeness:** without it the check
   would block a wrap whose predecessor legitimately wrote no stratum, and a gate that fails on correct
   behaviour teaches sessions to **fake blocks** — which would poison the very dataset the 15% reserve is
   waiting to be re-derived from.

   ### ⛔ AND THE FOURTH STATE IS PREVENTED, NOT NAMED (ds-022 (d), ruled by Dave #54, built #55)

   ★★ **WHY THIS ONE IS ENFORCED AND NOT MERELY DOCUMENTED — Dave, #55, and it is the general form:**
   *"An unenforced key turned into a false claim in the record, and the false claim turned into a wasted
   session. Close the first and the chain doesn't start."* ⇒ **the cost of an unenforced convention is
   not the convention being broken — it is the repair someone improvises, which becomes a fact.**

   **There is no fourth row above, and its absence is the ruling.** A session whose *testimony* reached
   `notes/_GAUGE-LOG.md` — a `META #<N>`, an `ERRORS #<N>`, a `tape/bill PAIR #<N>` — **without a
   `#### <date> #<N>` key above it** was invisible to every parser here, so ds-022 (a) reported that the
   session *"left NO block"* and invited a `HOLE` line that would have been **false**. #41 raised the
   state, declined to write that line, and forked it; it stayed open thirteen sessions.
   ⬛ **Dave's ruling (#54): gate it shut, and mark the three.** *"A vocabulary term for a state that
   should not be possible is a permanent tax; prevention is not."* ⇒ `_capture_gate.py::unkeyed_testimony`,
   **BLOCKING at birth** — testimony in this file with no key and no `HOLE`/`ABSENT` line **fails the
   wrap**. ★ **Testimony and key are ONE act; write the key above the entry as you write the entry.**
   ⚠️ **Do NOT reach for `HOLE` when it fires** — the evidence disproving it is the line the gate quoted
   back at you. ⚠️ **Do NOT reach for `roll_2f` either:** the mover cannot produce this state (it refuses a
   post-mortem with no key), so it is never the repair — and once a key exists here the duplicate-key
   guard refuses, correctly. **The repair is the missing key, nothing else.**
   ⚠️ **SCOPED TO THIS FILE, per the #43 ruling.** A stratum still sitting in `GOOD-MORNING.md` §C is a
   different state — an unrolled block, i.e. 2f's job and ds-022 (a)'s alarm — and this check must not
   annex it. ★ **The three that already reached the state (#40 #41 #42) are named once**, in this log's
   `#### META — UNKEYED #40 #41 #42` block, and **must not be rolled**: their keys were added
   retroactively, so the duplicate-key guard refuses them and is right to. That retroactive patch is why
   #53's handoff said *"roll all 12"* when the record said **9**.

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
   ⛔ **THE STORE IS `Project instructions + cloud memory` SINCE #278 (2026-09-16), NOT the
   sandbox-mounted auto-memory this step was written for** — #278's conductor promised this wording
   change on the record in the session that caused the move; it is paid here at #293 (lane E1, dream
   pass 13 P2). `MEMORY.md` named above is the OLD store's index and has no path on disk any more;
   read the naming as "the memory index, wherever the store now lives". ⚠ Only the conductor's seat
   can read or write that store — a sub-lane cannot, and must say so rather than report silence.
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

   - ⛔ **AN "OPEN, DAVE'S" ITEM WRITTEN BEFORE HIS ANSWER IS A QUESTION PUT, NOT A STATE OF THE
     WORLD — AND THE LIST IS RE-READ AT THE END, NEVER TRUSTED** *(`s271-D4`, #271, enacting
     dream-12 P4(a) — Dave, choosing between A (re-check) / B (write after) / later: "A.
     re-check")*: the hook is written at this step, which is **before** Dave answers the
     session's last questions, so every open item in it is a claim about a world that is still
     moving. At #267 it moved in **five minutes thirty-eight seconds**: the hook's first open
     item (*"lane N changed `_validate_compose.py:87` … a gate change without a ruling,
     flagged"*) was closed by `s267-D4`, inscribed at 21:26:49 against the file's 21:21 mtime,
     and a third item shipped as the v1.0.11 fast follower — **2 of 3 false**, while
     `notes/_dream/_MEMORY-GRADES.json` graded the file **FRESH**, because `s188-D1` grades
     whether the hook's **paths resolve**, not whether its **claims are true**
     [[no-gate-parses-the-artefact]]. ⇒ **Two obligations, and the write ORDER is unchanged**
     (writing the hook after the last ruling was offered at P4(b) and **NOT taken** — the
     current order is what makes the hook survive a wrap that runs out of window):
     1. **WRITE IT AS THE QUESTION IT IS.** Any item put into the hook before his answer is
        landed carries the words **"put to Dave at the wrap call"** — never a bare assertion
        that a thing is open. An unanswered question recorded as a question cannot go stale; the
        same question recorded as a state of the world is false the moment he speaks.
     2. **RE-READ THE LIST AS THE RITUAL'S FINAL STEP** — after 5/5b, once every ruling of the
        session is inscribed — against `knowledge/_rulings.json`, and **strike what the
        session's own rulings closed: BY ADDITION, naming the ruling id** — the form is
        `… — CLOSED by s267-D4`, appended to the item, never a silent deletion of the
        line. The machine half is
        `_capture_gate.py::hook_open_items_recheck` (`s271-D4`, **ADVISORY** — it names the
        item and the ruling; it can never edit the store, which is read-only from every seat).
     ⚠ **The gate arm is a signal, not the judgement.** A same-day ruling on the same subject is
     a strong match, not a proof — read both before striking, and a strike that is wrong is
     worse than an item that is merely stale.
   ### ★ THE MEMORY DIRECTORY IS THE CLAUDE.AI PROJECT MEMORY, AND THE SEAT LIMIT IS NOW STRUCTURAL (#278, 2026-09-16 — ADDED BY ADDITION; nothing above is rewritten)

   The Cowork memory directory this step describes **is now the claude.ai Project memory** (import
   2026-09-16 03:14–17Z, `sources: [cowork-import]`). **Only the CONDUCTOR'S seat can write it** — a
   delegated wrap sub cannot reach the store at all, so at a delegated wrap this step is a SEAT
   LIMIT and never a skip: **the sub writes `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md`** — the index
   line plus the file body, in the `s271-D4` form — **and the CONDUCTOR places it at the NEXT
   opener**, at a cold seat for ≈4K tokens. Proven at #278: #277's hook was placed exactly that way
   (`d7b8d72`), with the receipt appended to the hook file itself. ⚠ Three properties of the new
   store that the hand-checks at this step must respect: it is **account-wide on READ** (other
   Projects' subtrees are visible) and **Apollo-only on WRITE**, so keep Apollo files Apollo-only;
   the index file **caps at 49,152 B**, so periodic compaction is owed and the dream pass is its
   seat; and the forward risk is **one-way** — a re-import could overwrite cloud-only lines.
   ⛔ **THE RULE ITSELF IS UNCHANGED AND IS NOT RESTATED HERE: the repo is the record, memory is the
   accelerator.** That is what the paragraphs above already say; the cloud move gave it a new place
   to point at and moved nothing else. ⚠ **There is NO `MEMORY.md` in the repo and there never
   was** (`git ls-files` reads 0) — the file this step's older prose names was the Cowork LOCAL
   index, and its cloud successor is `index.md` inside the Project store.

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
   ⛔ **SUPERSEDED #60/#61 — RULED (Dave): the title is now a capped LABEL, ≤120 tape,
   GATE-ENFORCED (BLOCKING).** The advisory-only posture above is the exact mechanism that let the
   title grow to 1,073 tape / 3,950 chars — 18% of the read chain, ZERO consumers — over the
   thirty-two sessions since #28: *"a rule with no gate is a preference."* Written by ADDITION,
   the #28 text above stays verbatim. Ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #60-D8. Gate:
   `knowledge/_capture_gate.py`'s `TITLE_CAP_TAPE`/`TITLE_LINE_RE` check in `check_budgets()`.
   ⚠ **Titles are LABELS, never role assignments** (2026-07-21: a forward title's `[conductor + 2
   workers]` seated a second conductor). If the coming session runs the parallel model, say so in the
   §C brief and let the ROLE come from Dave's opener line — and include the **DIVVY PLAN** (lanes ·
   model per lane · serial set · shared files assigned per lane) in the forward brief, per
   `_RUNBOOK-parallel-conductor.md`.

4c. **Scratch hygiene — clean the VM disk WHILE YOUR USER STILL EXISTS.** *(Added #227,
   2026-08-30, measured cause: the sandbox VM disk (~9.6G) PERSISTS across sessions but every
   session runs as a throwaway Linux user; `/var/tmp` is sticky and there is no root, so scratch
   that outlives its owner is PERMANENTLY UNDELETABLE from inside. At #227 boot the VM was 100%
   full — 3.2G of dead-session orphans, chiefly the #220 playwright browsers at 984M — and
   `useradd` itself ENOSPC'd five times: no shell at all until a host restart.)*
   Run `python3 knowledge/_gate_scratch_hygiene.py` (ADVISORY, born #227 — promotion is Dave's):
   it names every `/var/tmp` + `/tmp` + `~/tmp` + `~/.cache` entry the CURRENT user owns and the VM
   fill %. Remove what you own (`--clean --wrap` does it, and `--wrap` adds `~/.local` — the session
   home sits on the same persistent disk and is never removed when the user dies; #283 counted 127
   dead homes holding 4.8G, `s283-D1`), because the next session cannot. ⛔ `--clean` NEVER touches
   `/tmp/gitshim` — that is `_seam.py`'s keep-list and the #282 4c collision. Orphans owned by dead sessions
   are reported as a total only — drift visibility, not action. ⚠ The wrap is the LAST moment
   this cleanup is possible; a skipped 4c is a permanent squatter, not a deferral.

4d. **Re-render the rulings page — a STALE `notes/_RULINGS.html` is RED and BLOCKS the wrap.**
   *(Added #263, `s263-D10`, ruled Dave: "`knowledge/_render_rulings.py --check` becomes a
   WRAP-RITUAL GATE: the wrap fails if `notes/_RULINGS.html` is stale against `_rulings.json`.")*
   ```
   python3 knowledge/_render_rulings.py            # rebuild, then stage notes/_RULINGS.html
   python3 knowledge/_render_rulings.py --check     # must print FRESH … (exit 0)
   ```
   The page is a **GENERATOR's output that Dave READS**, and `--check` compares the
   `source-sha256` embedded in the on-disk HTML against the current sha256 of `_rulings.json` —
   **content, never mtimes**, for the DV-D17 reason 2g gives. A wrap that inscribes a ruling and
   does not re-render leaves the surface Dave consults one session behind: the #32 shape (2g's
   retrieval index), on the record where being behind is worst. ⚠ **`--check` alone is not the
   step** — it only reports; the rebuild is what closes it. **BLOCKING at birth by Dave's word**,
   and wired the way 2g's freshness check is: `_capture_gate.py::rulings_page_freshness_check`
   calls the renderer's OWN `check()` **in-process** (no subprocess — the sandbox call-boundary
   lesson), so `--wrap` goes RED on stale and one implementation of the freshness rule exists.
   It runs for **LANE wraps too**: `_rulings.json` is repo-wide and any seat can stale the page.

5. **Commit + push.** Claude commits via `_git_commit.sh` (see `_RUNBOOK-git-commit.md`), which
   handles the lock dance. **Dave pushes via GitHub Desktop only** — never terminal push, never a
   Desktop commit, Desktop closed while Claude commits (memory `git-push-method`).
   *(The old "hand Dave a paste-ready summary + description" beat is RETIRED — Dave, #63: it dated
   from the era when the sandbox could not commit at all; `_git_commit.sh` ended that. He reads the
   commit in Desktop when pushing. Claude commits, Dave pushes — nothing to paste.)*
5b. **Post-wrap addendum (dream-pass-3 P6, ruled 2026-07-28; applied to its own ruling the hour it
   was made, #21).** A ruling that lands AFTER the wrap gate has run gets an explicit addendum beat:
   append it to the ★ LATEST banner (a one-line "post-wrap addendum" under the banner is enough),
   re-run the wrap gate, then commit. The banner is the session record (GM-D4) — inscribing the
   tattoos while the record stays silent is how #21's hunt-list ruling went missing from its own
   session while #20's identical shape propagated; discipline, not design, is what made it a class.
   ⛔ **AND THIS IS WHERE THE `s271-D4` RE-READ HAPPENS — the ritual's FINAL beat, by addition.**
   A post-wrap ruling is exactly the thing that falsifies the memory hook's "Open, Dave's" list,
   so after the addendum and before the session is called done, re-read that list against
   `knowledge/_rulings.json` and strike what this session's own rulings closed, **naming the
   ruling id** — the rule, its evidence and its advisory gate arm are at step 3.
   ⚠ Do NOT promote a spec/ledger to Polaroid duty in compensation (A-D3: the spec stays the single
   source); the beat only makes the record SAY the source changed.
5c. **The summary for Dave — short bullets: decisions, outputs, problems (`s305-D63`, 2026-09-28; added
   by addition after 5b — the step list in the heading above is left as written).** Dave, verbatim: *"lt's turn
   the summary into shorter bullets just outlining decisions, outputs and problems, less verbose."*
   ~~After every wrap, give Dave a plain-prose narrative of the session, five to seven paragraphs, no bullets,
   no landmarks (his ask at #250, 2026-09-06).~~ *(Struck by `s305-D63`. The #250 practice lived in Project
   memory and the conductor's wrap briefs, never in this runbook; it is written here only so the strike has a
   home. Older `NARRATIVE.md` files stay as the record they are.)*
   **The form:** a file `notes/_lanes/<n>/W/SUMMARY-BULLETS.md` (provenance and status lines as any lane note),
   then three headings in this order — **Decisions** · **Outputs** · **Problems** — one short line per bullet,
   about 20 bullets in all at most, no narrative paragraphs. A decision carries its ruling id where one exists;
   an output its path, sha or run; a problem what is open and whose it is. Figures are copied off the handoff
   and the wrap report, never retyped from memory. The conductor gives it to Dave after the wrap; the
   narrative dossier of step 1b is unchanged (it is the WHY and HOW for the record, not the summary for him).

### ★ THE ORDER AFTER THE COMMIT — ONE CI WAIT, THE SUMMARY AT THE PUSH (`s306-D7`, #306, 2026-09-28; added by addition — steps 5, 5b and 5c above are left as written)

Dave, verbatim, call 4 of the wrap-redesign page (`notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html`,
export 16:01 BST): *"a · Yes, the next opener reads the follow-up's CI"*, to *"Give you the summary as soon
as the wrap is pushed, and stop waiting on CI for the small follow-up commit?"* Built at #306 by lane V as
PHASE 2 of the redesign (his *"go on both"*, 16:58 BST); `s306-D7` stays `ruled` until one real wrap has run
in this order and the minutes from launch to his summary are measured again (about 59 at #305,
`notes/_subreports/2026-09-28-306-R-wrap-redesign.md`). Where this block and the text of 5, 5b or 5c above
disagree about WHEN, this block wins; what each step writes is unchanged.

**The order, from the wrap commit on:**

1. **5 — commit the wrap, push it** (`bash knowledge/_git_commit.sh --push`, the conductor's judgement,
   `s207-D1`; the "Dave pushes via GitHub Desktop" sentence in step 5 above is the pre-#141 text, corrected in
   `_RUNBOOK-git-commit.md` step 5).
2. **Read the wrap commit's CI back — THE ONE WAIT THE WRAP KEEPS.**
   `python3 knowledge/_ci_readback.py --sha <wrap sha> --poll 170`, repeated call by call until it exits 0
   (green) or 1 (red). It prints a short run summary only: run id, per-job status and conclusion, failing
   step names, and for a failed job the blocking lines parsed out of its log — never the log (limit 8 of
   `s306-D10`). Save what it prints to `notes/_lanes/<n>/W/_ci-runs-<sha8>.txt`.
3. **5c — the summary goes to Dave NOW**, straight after that read, with the CI verdict as one of its
   Outputs (or Problems, if red). Nothing after this point changes what he is told.
4. **5b — the post-wrap addendum**, as written above (the banner addendum if a ruling landed late, the
   `s271-D4` re-read), plus the wrap commit's CI verdict from step 2, plus this line, verbatim in form:
   `CI owed: this addendum's own commit — read by the next opener with python3 knowledge/_ci_readback.py --owed`
   A commit cannot carry its own sha, so the line names the tool's `--owed` form, which resolves the sha as
   the last commit that touched the newest `_HANDOFF-*.md`. If the follow-up is ever a different commit from
   the one carrying the addendum, write `--sha <that sha>` instead. The conductor also says the 5b sha in chat.
5. **Commit the 5b addendum and push it — WITHOUT WAITING ON ITS CI.** Its CI is owed, not skipped: the next
   opener reads it and relays the verdict in that session's chat (`s203-D1`'s read-back, one session late,
   by Dave's word).
6. **4c — scratch hygiene, LAST**, as before (it deletes the tiktoken cache every gate needs).

**The gate.** `knowledge/_capture_gate.py::ci_owed_check` (wrap mode, BLOCKING in that mode, born #306):
from `_HANDOFF-157` on, a handoff carrying a `POST-WRAP ADDENDUM (5b)` heading must carry a `CI owed:` line
naming `_ci_readback.py` with `--owed` or `--sha <hex>`. It runs inside the 5b commit's committer, so a 5b
addendum pushed without the line shows red there. Handoffs before 157 are out of scope by date, not graded.

**The next opener.** After reading the newest handoff, if it carries `CI owed:`, run the command on that line
once and put its summary in the first reply. A red there is the session's first beat.

~~After the 5b commit and push, read its CI back to completion before the session is called done.~~ *(Struck by
`s306-D7`. The second wait lived in the conductors' wrap briefs and in the handoffs' 5b addenda, never in this
runbook; it is written here only so the strike has a home. At #303–#305 it cost 9.4, 14.9 and 14.0 minutes.)*

### ★ PHASE 3 — ONE STORY, EVERY VIEW GENERATED (`s306-D4`, `s306-D5`, `s306-D8`, `s306-D10`; #311/#312, 2026-10-01; added by addition — the PHASE 1 table above is unchanged and its inputs are now generated)

Designed by #311 lane E0 (`notes/_lanes/312/E/DESIGN.md`), built by #312 lane E-build (`notes/_subreports/2026-10-01-312-E-build.md`).
Nothing in steps 1–5b above is rewritten: phase 3 sits UPSTREAM of the PHASE 1 table and writes its inputs.

**The two-file rule, one writer each.** The wrap seat writes ONE file by hand, `notes/_lanes/<n>/W/STORY.md`, and measures
ONE file by tool, `notes/_lanes/<n>/W/FACTS.json`. A figure lives in `FACTS.json` and nowhere else; a sentence lives in
`STORY.md` and nowhere else; the story names a figure as `{facts.fill.now:,}` or `{d.hard_line:,}` and never types it (a
typed figure that `FACTS.json` also holds WARNS, naming the placeholder). `python3 knowledge/_wrap_views.py --session N`
reads both and writes every other file of the wrap into `notes/_lanes/<n>/W/views/`: banner, delta, stratum, stamp,
datesplit (on a date split), 5b (stage post), handoff, the prior handoff's STRUCK addendum, dossier, W report, the ONE
memory hook file, `new.txt` + `strike-<k>.txt` + the carries delta block, `rows.json`, the commit msgfile, the summary.
Dry run by default (sizes against limits, diff against disk); `--write` writes `views/` and places handoff, dossier,
report, memory hook and summary at their homes. The generated W report IS the filed report (`s306-D5`).

**The story's sections** (the grammar is `DESIGN.md` § 2; the parser refuses an unknown `## @name` and a second `## @tally`):

| section | one item is |
|---|---|
| front block | `key: value` between `---` lines: session, headline (lower case), one_sentence, opened_word, wrap_word[, wrap_word_context], conductor, wrap_seat, lanes, first_beat, next_title, words_files, lane_reports[, prior_handoff_struck, co_authored_by, claude_session] |
| `## @words` | `- HH:MM — his line verbatim *(context)*`, or `- HH:MM — export `path`: what each call chose, quoted` (chat lines only; exports by path, limit 4) |
| `## @rulings` | `- `sNNN-Dk` — his phrase, verbatim — gloss — RULED\|ENACTED\|RULED NOT ENACTED[, note]` (or `None this session.`) |
| `## @summary` | `### decisions` / `### outputs` / `### problems`, 1–4 lines each in Dave's register (`s305-D63`); shown to him verbatim |
| `## @did` | `### TITLE IN CAPS` + one paragraph, 3–6 blocks (the delta's paragraphs, the handoff's WHAT THE SESSION DID) |
| `## @problems` | `- ⚠ sentence` (the delta's ⚠ paragraph; the banner's ③ takes the first) |
| `## @owed` | `- MARK owner: **question?** — body`, owner ∈ mine/dave/future/found/standing; item 1 is the first beat; `(carried)` marks an item already in `_CARRIES.md` |
| `## @new` | `- MARK **TITLE IN CAPS** [DAVE'S] — body` — the generator inserts `[NEW — 0]`; may be ABSENT (derived from `@owed`: ⬛ items owned mine/dave/future, not `(carried)`) |
| `## @struck` | `- **TITLE AS IT STANDS IN _CARRIES.md** — ANSWERED\|BUILT\|DECIDED\|DROPPED\|SUPERSEDED — receipt sentence` |
| `## @rows` | `- close\|note\|reopen W-id — text` (the four mints h/dh/w/wk are derived, never written) |
| `## @cold` | `- ⛔★★ **LESSON.** sentence` — the session's own lines; the eleven standing lines are a constant in the tool |
| `## @why` | `### k. title` + paragraphs; last block `### Resolved, and still open` — the dossier, verbatim |
| `## @findings` `## @questions` `## @unproven` | the W report's § 3, its ruling-shaped questions, its UNPROVEN (`None.` allowed) |
| `## @skips` `## @section_usage` | one paragraph each — the stratum's DECLARED SKIPS line and the seat's self-report |
| `## @tally` | RESERVED for phase 6 (`s306-D9`); empty until then |

**The command order (the PHASE 1 table from `_wrap_ops.py` on is unchanged; its inputs are read from `views/`):**

1. `_wrap_facts.py --out <n>/W/FACTS.json --session N --rulings-base <opener sha> --since <last wrap sha> --transcript <conductor jsonl> --until <his word's ISO> --subagents-dir <dir> --exclude <own jsonl> --gate-log <n>/W/_gate-open.log [--ci-owed <the opener's saved _ci-runs file> | --ci-owed-typed SHA8:GREEN] [--ci-red SHA8:STEP:FIXED_BY …]` — the phase-3 keys (dates, commits, handoff number, CI, chain size, the gate verdict) are measured here; `--tz` defaults to Europe/London.
2. Write `<n>/W/STORY.md` by hand (the worked example: `knowledge/_tests/wrap_views/310/STORY.md`).
3. `_wrap_views.py --session N` (dry run: every view's size against its limit; a limit that BLOCKS refuses the write, naming the view and the longest bullet), then `--write`.
4. The PHASE 1 table from `_wrap_ops.py` on, its files now `views/banner.md`, `views/stratum.md`, `views/delta.md`, `views/stamp.md` (`--date-split views/datesplit.md` on a split); carries from `views/new.txt` and `views/strike-<k>.txt` (see THE CARRIES PATH below); rows from `views/rows.json`; one regen; the commit with `--msg views/msg.txt` (the trailers come from the front block's `co_authored_by` / `claude_session`, or `_wrap_commit.py msg --trailer`).
5. Push; `_ci_readback.py` (the `s306-D7` order above); the summary to Dave is `views/SUMMARY.md` — at the push, regenerated at step 7 with the push and CI line.
6. `_wrap_facts.py --post --facts <n>/W/FACTS.json --wrap-sha S --seat-sha S --gate-wrap "N in scope · N fail · N warn" --push-range A..B --pushed-at ISO --launched-at ISO --ci-runs <n>/W/_ci-runs-<sha8>.txt --prepush-dir <n>/W --title-brief "<next title>"` — the `post` block, by addition (the pre-commit keys are checked byte-identical first).
7. `_wrap_views.py --session N --stage post --write` — writes `views/5b.md` and `views/msg-5b.txt`, and regenerates handoff, report and memory hook WITH their post-wrap blocks, refusing if the pre-commit part on disk is not byte-identical to the stage-wrap text ("by addition, nothing above is rewritten", as a check). Then the 5b line by `_wrap_ops.py --fill-token … --fill-text views/5b.md`, one regen, the 5b commit with `--msg views/msg-5b.txt`.

**The freshness arm (limit 7).** `_wrap_views.py --check` regenerates the NEWEST wrap's views (the newest `_HANDOFF-*.md` names it) and compares with disk — `views/` and the homes of handoff, dossier, report and memory hook — red on any hand edit, naming the file and the first differing line, and runs every limit. It is a check-only step of `_wrap_regen.py` (after the nine), so every regen runs it; a newest wrap without a `STORY.md` (the phase-1 path) is a declared skip. Its one call in `_capture_gate.py` (wrap mode, blocking) is the conductor's to land; until then the seat runs it by hand before the commit.

**The carries path (`s306-D8`, phase 5, built at #312).** `_wrap_carries.py delta --from N --to N+1 --block views/carries-delta.md --write` APPENDS one small block (base, wrap date, new items, strikes with receipts) instead of a whole copied line; `render --section N+1` materialises the full line (ages +1, strikes in the `s183-D1` form, new first) and `count --section N+1` reads the rendered line; `rebase --section M --write` commits a FULL line every twenty wraps (picked). Proven at #312 on the real #309→#310, #310→#311 and #311→#312 lines, byte-identical. ⛔ **UNTIL `_capture_gate._resolve_residual_pointer` resolves a delta section by calling `_wrap_carries.resolve_line()` (one call, the conductor's), a wrap that writes ONLY a delta block fails the 2c carry gate** — so the wrap seat keeps the `roll --new views/new.txt` + `strike --note-file views/strike-<k>.txt` path of the PHASE 1 table, and may ALSO append the delta block (harmless; the full line is still the one the gate reads). The `[NEW — 0]` count defect (`_capture_gate._AGE_RE` never matches `[NEW — 0]`, so new items count from #N+2) is fixed in `_wrap_carries.AGE_RE`; `count` prints both readings and says which regex the gate's figure uses; the one-line gate change is the conductor's.

**Which path the wrap seat takes, and why.** The phase-3 path when `_wrap_views.py --selftest` is green AND the replay (`notes/_lanes/312/E/replay/<n>/`, lane E-replay) is green on #309, #310 and #311 — the replay verdict, by session, is filed there with its residue explained; the PHASE 1 path otherwise, exactly as #309–#311 ran it, its hand-written views becoming the next replay fixture. Either way the phase-1 tools are the ones that move files, so a failure in phase 3 never leaves a wrap without a path. `W-305wr` stays open until a real wrap has run on phase 3 and its counts (hand-written files before and after; homes per figure) are measured.

**★ THE REPLAY VERDICT (#312 lane E-replay, 2026-10-01, by addition): GREEN on #309, #310 and #311 — the #312 wrap takes the PHASE-3 path.** `notes/_lanes/312/E/replay/<n>/REPLAY.md` grades every generated view against the hand-written one on figures, his words, headings and size (`DESIGN.md` § 8): 18 of 18, 20 of 20 and 19 of 19 views GREEN, the generated carries delta block reconstructing each hand-rolled FULL line byte for byte (`s183-D1`), with the grading choices and the declared figures (the post-roll count, a figure typed from the committer's log, the chain after the 5b regen) printed in each REPLAY.md. The three stories are frozen as fixtures at `knowledge/_tests/wrap_views/{309,310,311}/` and `_wrap_views.py --selftest` regenerates them byte-exact. What the replay ADDED, all by addition, and what the #312 story seat therefore writes:

- **`@did` may carry a SECOND paragraph** after a blank line: the delta prints the first paragraph only (the chain's register, under limit 3/6), the handoff prints both (the lanes' shas, counts and paths go in the second). Three or four blocks; the delta's paragraph count is graded.
- **`@struck` titles are copied AS THEY STAND on the `_CARRIES.md` line, circled number included** (`**① BUILD THE …**`); the VERDICT may be any short CAPS phrase (#310's `THE ROUTE CAME BACK`). The receipt is printed verbatim in `strike-<k>.txt`, the prior handoff's addendum and the delta block, so one text, one writer.
- **The `lanes:` front line may carry each lane's commits** (`A `6faaca8d`..`ac779ad3` · B …`); the banner's ② prints it whole, the delta's header without the shas.
- **`@problems`:** the banner's ③ prints the CI reds from `facts.ci.reds` (give each a cause: `--ci-red SHA8:STEP:FIXED_BY:cause`) and takes from the story only a line that starts `⛔` (a breach); write the CI line as `- ⚠ CI: …` for the delta.
- **`_wrap_facts.py` measures more:** `--launched-at ISO` gives `fill.launch` (the fill at the message that launched the seat; the handoff, stratum and report print it, no second facts file); `subs.each` (every sub's fill by transcript; the stratum lists them); `--fill-source PATH` (the cloud transcript the copy came from, typed and marked so); `--ci-owed-at-wrap FILE` (a CI run still owed when the seat sat, read before the commit, #309's case); `--ci-push SHA8:GREEN|RED[:STEP]` (the session's pushes, #311's three); `rulings.by_date` (the date-split line says which rulings carry which day); the pre-push logs' step ids, advisory steps and, when `_prepush-committed-*.txt` exist, the committed-tree half (#311's two-half form, "step 119 green").
- **What no generated view carries, declared, not hidden:** the post-roll carries count (the banner names the probe instead), the chain figure after the regen that follows the views, the committer's run seconds and path counts, a memory AREA payload (no story section; see the E-replay report's Found-not-fixed). The freshness arm now allows ONE appended suffix on the handoff home — the next wrap's `## ⬛ STRUCK AT THE #N WRAP — BY ADDITION` block — and reads any other appended text as red (EV-9).

**The limits (`s306-D10`, lane U's eleven; the numbers marked picked are not his):**

| # | limit | where it bites | number |
|---|---|---|---|
| 1 | the story draft is never on the boot chain | selftest bite on `_gen_chain.py`'s source; the name rule | — |
| 2 | ceiling on the generated handoff | `_wrap_views.py` refuses the write; `--check` | warn 6,500 (picked) · block 8,106 cl100k |
| 3 | the tally is one block, replaced | the parser refuses a second `## @tally` | (phase 6) |
| 4 | his words verbatim with times; exports by path | `@words` grammar; warn over 3,000 cl100k; exports over 4 warn | 3,000 |
| 5 | the seam prints one line | phase 6 | — |
| 6 | the chain takes only banner and delta | by construction (`_gen_chain.py` untouched); banner ≤ 10 lines, ≤ 1,200; delta ≤ 1,513 | existing + 1,513 |
| 7 | freshness checks the newest wrap only | `--check` reads the newest handoff's N and refuses another | — |
| 8 | the opener's CI read prints the summary | phase 2, done | — |
| 9 | one shared brief, one line per seat | phase 4 | — |
| 10 | the full carried list is generated on read; `_CARRIES.md` ≤ 20,000 B a wrap | `_wrap_carries.py delta` refuses a larger block; `render` | 20,000 B |
| 11 | one memory file per wrap | the memory hook is ONE file with the index line, front block and body under marked headings; description ≤ 800 B (picked) | — |

## ★ FILED SUB-REPORTS — what every sub brief must now say (`s218-D7`, 2026-08-25)

*Ruled by Dave at #218; the ruling's own body lives in `knowledge/_rulings.json` § `s218-D7` and
is not restated here. This section is the OPERATIONAL half: what a brief must contain, what the
sub owes, and what the conductor owes at reconcile.*

**In the brief.** Every sub brief — build, research, wrap, lane — carries these four lines
alongside the existing DO-NOT-RULE list:

1. **The file:** `notes/_subreports/YYYY-MM-DD-<session no>-<sub index>-<slug>.md`, written to
   the skeleton at `notes/_subreports/_TEMPLATE.md`. **One writer per file** — the window and
   the sub index are in the name so two parallel subs can never collide on one path.
2. **The stub:** what comes back to chat is VERDICT + the COUNTS line + the file pointer + token
   spend + REPLAY-THESE, and nothing else. Every figure in the stub is **copied off the file**,
   never retyped — the file is the sole authority.
3. **Evidence beside the report:** `notes/_subreports/assets/<report-stem>/`. ⛔ Never session
   scratch (`/tmp`, `/var/tmp`): scratch dies with the window and a report whose evidence has
   evaporated is a claim, not a receipt.
4. **RULING-SHAPED QUESTIONS is a mandatory section**, even when the answer is "none". It is
   what stops a sub's generated prose from arriving as a decision.

**At reconcile, the conductor CITES EACH REPORT BY PATH** in the session receipt (or the ★
LATEST banner). This is not bookkeeping — a stub hands the window a pointer, and an uncited
pointer is an unread one: the window closes believing the lane reported and the finding set goes
into history unread. Reports are **dated history** (ADR-0017 / `s192-D1`): live facts flow OUT of
a report to their one home at reconcile, and the report keeps the reading it took on the day.

**Two gates enforce it** (both listed under "The gate" below): the doc-row gate's glob now covers
`notes/_subreports/*.md`, so a filed report with no `_state.json` row fails exactly like a brief;
and the wrap's citation check warns on any report filed since the last wrap that this session's
own record does not name by path.

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
- **★ Filed sub-reports (`s218-D7`, added #218) — two checks, two scripts:**
  - **`knowledge/_gate_doc_rows.py --check`** — its glob now covers `notes/_subreports/*.md`
    (flat, `.md` only; `_TEMPLATE.md` exempt by name, `assets/**` is evidence not a document).
    A filed report with no `_state.json` row FAILS exactly as an unrowed brief does. One
    directory home, `notes/_subreports/`, rows every report beneath it — that is the intended
    shape for a busy conductor window.
  - **Wrap mode's `subreport_citation_check`** — a report filed since the last capture-ritual
    commit (`after #<n>`) that this session's own record does not name **by path** warns. The
    citation surface is scoped to this session: the ★ LATEST banner regions of `GOOD-MORNING.md`
    / `_CHAIN.md` and the receipts changed since that commit — a prior session's receipt does not
    cite anything for this one. It also PARSES each report's `COUNTS:` / `REPLAY-THESE:` lines
    and its `RULING-SHAPED QUESTIONS` heading, because the stub's figures are copied off them.
    ⛔ **ADVISORY AT BIRTH** — it warns, it does not fail. Promotion to blocking is **Dave's
    word**; the tier is the one line `SUBREPORT_CITE_BLOCKING` in `_capture_gate.py`.
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
