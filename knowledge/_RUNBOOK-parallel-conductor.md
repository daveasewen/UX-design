# Runbook — parallel sessions: worker vs conductor (single-writer for shared state)

*Origin 2026-07-19: two Cowork sessions ran at once and BOTH tried to commit + rewrite
`GOOD-MORNING.md`. Dave's diagnosis: "I should be running a cold agent from the main chat." The
receipt→conductor→one-commit path was then proven live (this session handed a receipt; the other
merged it into commit `e15aa25`). Canon lives HERE; `AGENTS.md` and `MEMORY.md` only point at it.*

---

## The one rule

Many sessions may do work, but **only ONE session writes the shared state and commits it.** Shared
state = the handoff files `GOOD-MORNING.md` · `_LIVE-STATE.md` · `MEMORY.md` · `_FUTURE-STATE.md`, and
the merged commit. Everything else a session produces is a NEW file (unique name → never collides).

Why: handoff files are *rewritten*, so two writers = last-writer-wins, silent clobber. New files and
disjoint commits merge cleanly; the only git hazard is `.git/index.lock` if two commits fire at once
(serialize — see `_RUNBOOK-git-commit.md`).

## The trigger — "read good morning" (zero copy-paste)

Dave opens every session by saying **"read good morning"** (optionally with a role word). On that
trigger the session:

1. Reads `GOOD-MORNING.md` as usual, AND resolves its role:
   - If Dave named one ("…worker" / "…conductor" / "…solo"), take it.
   - Else check `mcp__session_info__list_sessions`: if **>1 session looks active**, fire
     **AskUserQuestion** — *Worker · Conductor · Solo* — one click. If only one, proceed **Solo**
     silently (no question).
2. Acts on the role (checklists below).

**Dave's entire job:** say **"read good morning"** in each chat, click the role if asked, and hit
**Push** in GitHub Desktop at the end. **No phrases to paste, no receipts to shuttle** — a conductor
reads the other sessions itself (below).

**⚠ Titles are LABELS, never role assignments (added 2026-07-21 after a live misfire).** A handoff's
forward title may describe the phase topology (`[conductor + 2 Fable workers]`) — a fresh session that
reads that text as its role will self-seat as a SECOND conductor (it happened; Dave caught it from the
rogue session's routing announcement; the fix was a one-line stand-down that re-seated it as a worker).
**The role comes from Dave's opener line only.** If your opener carries no role word, resolve per the
trigger steps above — never from the chat title, never from §C's description of the coming session.

**The DIVVY PLAN (standing practice, Dave 2026-07-21: "always be thinking about how to divvy up the
tasks in the handoffs, whether it's with subagents or parallel chats").** Every handoff's forward plan
names: what parallelises · lane count + model per lane · what stays SERIAL · **every shared file, each
assigned to ONE lane** (or the conductor). Shared-file races (two workers editing one registry) merged
clean on 2026-07-21 by good behaviour, not by construction — naming the file per lane makes it
construction. Workers may absorb LIVE Dave rulings mid-flight: receipt them with verbatim quotes so
the conductor can inscribe from the receipt alone.

**Optional autonomy clause for unattended lanes (routing audit #9, ratified 2026-07-23).** When a
worker lane will run without Dave watching, its brief may include: *"the user is not watching;
proceed on reversible actions that follow from the brief; an end-of-turn promise is not a
completion — do the work or flag the blocker."* Interactive solo sessions don't need it. Worker
receipts follow the evidence-pointer rule: every "landed" claim names its evidence (gate run,
commit, render, file path — see `_RUNBOOK-capture-ritual.md` step 2).

**N=1:** a lone session is Solo — its own conductor, writes its handoff as normal. The role machinery
only engages at two or more.

## ★★ BOUNDED VERIFICATION — the appetite clause for every sub brief (`s172-D3`, ruled Dave #172)

*Added 2026-08-14 BY ADDITION. Body lives HERE; `knowledge/_rulings.json` § `s172-D3` is the pointer.*

⛔ **READ THE FENCE FIRST, BECAUSE IT IS DAVE'S CONDITION AND NOT A CAVEAT.** His concern, verbatim:
***"careful of externalities, I don't want to fix something only to break other constituent parts."***
⇒ **This section governs THE APPETITE FOR BUILDING NEW INSTRUMENTS IN FUTURE SUB BRIEFS, AND NOTHING
ELSE. IT RETIRES NOTHING.** Every existing gate, law, runbook clause and ruling in this repo stands
exactly as ruled. ⛔ **No existing check may be removed, relaxed, skipped, narrowed or "simplified" by
citing this section** — a brief that cites it to justify not running something is misusing it. The
target is the *next* instrument, never the ones already standing.

**Why it exists, measured at #172:** the B2 sub wrote **474 instrument lines around a 6-line emitter**
and the `_state.py` selftest went **41 → 57 arms** — against the week's REAL catches, which were the
self-comparing assert (#171), the degenerate title parse (#169) and the fixture that passed on its own
mutant (#171). ★ **The catches came from proving ONE seam could fail, not from breadth.** Source for
(a): Anthropic's prompting best-practices guidance, §§ *Overthinking and excessive thoroughness* ·
*Overeagerness* · *Avoid focusing on passing tests and hardcoding* (fetched 2026-08-14; the pointer is
in `s172-D3`'s `evidence`).

**The five clauses. (a) goes into the brief near-verbatim; (b)–(e) are how the brief is written and
how its report is read.**

- **(a) SCOPE BLOCK, near-verbatim in the brief.** *"Use the minimum complexity that solves the
  current task. No abstractions for hypothetical future needs. No defensive code for scenarios that
  cannot occur here. Make the changes requested and those clearly necessary to them — nothing else."*
- **(b) VERIFICATION IS TARGETED.** Prove **the seam THIS deliverable creates**. ⛔ Not *"verify
  everything you touch"* — that instruction has no edge, so it spends the whole window and still
  cannot say what it proved. Name the seam in the brief; the report answers about that seam.
- **(c) DEPTH CAP — ONE LEVEL.** A new check is driven to a **named refusal once**, with a passing
  control [[mutation-tests-the-clause-not-the-feature]]. ⛔ **No checkers checking checkers beyond
  that.** The proof that a check can fail is itself not re-proved by a second instrument.
- **(d) MACHINERY PRICE LINE.** Every sub report declares **instrument-lines vs feature-lines** —
  e.g. `machinery: 474 instrument / 6 feature`. It is a *reported measurement*, not a threshold:
  nothing fails for a bad ratio. It exists so the ratio is **visible at the moment it is chosen**
  rather than discovered three sessions later [[translate-prose-into-machinery]].
- **(e) OBSERVED-FAILURE RULE.** A new test must cite **the failure class it guards** or **the ruling
  it enforces**. A check with neither is speculative: it **QUEUES as a proposal for Dave** and is
  **never built in the same breath as the thing it would watch** [[instrument-without-a-consumer]].

⚠ **NO GATE, and deliberately.** This is discipline, the same class as `s165-D1` — a gate on brief
*prose* would be the exact over-instrumentation the section rules against, and would be the section
breaking its own clause (e). It is enforced by being read at brief-authoring time, which is what this
runbook is for.

## Worker checklist

1. Do the work; create only NEW files (dossiers, reviews, code — unique names).
2. Do NOT write `GOOD-MORNING`/`_LIVE-STATE`/`_FUTURE-STATE`. Touch `MEMORY.md` only as a **surgical
   append**, never a rewrite (a rule you must record → put it in the receipt, let the conductor inscribe).
3. Commit only your OWN disjoint files if you must, serialized; when in doubt, don't commit — hand
   files up.
4. Leave a short **RECEIPT** at the fixed path **`notes/_receipts/<date>-<session-slug>-<topic>.md`**
   (what landed · open · files touched · proposed §C lines · commit state · **author's context-gauge
   reading** — `_RUNBOOK-context-gauge.md` § authoring-time stamp: a scrutiny indicator on the
   receipt's reliability, e.g. `Context gauge at authoring: 🟡 AMBER ~55% (ESTIMATE)`). The session-slug in the
   filename means two workers physically cannot collide. The conductor can also read you directly via
   `session_info`; the receipt is the durable fallback and the anchor its reconcile step (2.5) looks for.

## Conductor checklist

1. **Read the other sessions directly** — `mcp__session_info__list_sessions` → `read_transcript` on
   each worker; distill what each did. This is the DEFAULT (Dave pastes nothing). A written receipt is
   only a fallback if a session isn't readable.
2. Merge into ONE `GOOD-MORNING` structured as a **strand menu + per-strand lanes** — never a flat
   mega-list (see below). Refresh `_LIVE-STATE`, apply any memory/rule from the receipts.
2.5 **Reconcile the working tree before committing.** `git status --short`; every dirty path is yours
   or a known worker's — cross-check against `ls notes/_receipts/`. **Never blind-`git add -A` with
   workers live**; account for each path first. (Same check as `_RUNBOOK-git-commit.md` step 0.5,
   restated here because the conductor is the one holding the commit.)
   ⚠ **A reconcile is STALE the moment another writer exists (#63, measured):** #62's stand-down
   receipt landed BETWEEN #63's reconcile and its stage, so the commit carried a fifth file the
   reconcile never named. Re-run the reconcile immediately before staging when any other session
   was live this window — the gap between "checked" and "staged" is a write window.
3. Make ONE commit (follow `_RUNBOOK-git-commit.md` — run `_git_commit.sh`, never hand-roll).
   *(Paste-ready summary RETIRED — Dave, #63: Claude commits, Dave pushes; he reads it in Desktop.)*
4. Dave pushes via GitHub Desktop only.

## Structuring the merged handoff — N strands, never a mega list

With 2–N parallel sessions, do NOT flatten them into one queue Dave has to wade. Lay `GOOD-MORNING`
out so he **picks a lane**:

- **§A Orientation** — shared, unchanged (whole-project context; not per-strand).
- **STRAND MENU** — one line per session: *name · one-line status · its single next action*. This is
  the chooser; Dave reads it and picks one.
- **Per-strand LANES** — each session gets its own short, self-contained block (what landed · next
  action · its commit). A reader takes one lane and ignores the rest.
- **Shared carry-overs + ONE commit note** at the end.

A strand drops off the menu once its work is done (collapses to a one-line closed note). If a lane
grows big, graduate it to its own `_handoffs/<strand>.md` and leave just its menu line + link —
`GOOD-MORNING` stays a thin router. The rule: **a reader should never scroll an unrelated strand to
find their own.**

## Guardrails

- Never two `git` operations at the same instant (lock contention). Serialize.
- `MEMORY.md` = append surgically, never rewrite, so parallel sessions don't clobber the index.
- A worker never edits shared canon mid-flight — it proposes via the receipt; the conductor decides.
- **Nothing clashes by construction, not by good behaviour:** workers write only NEW files at
  `notes/_receipts/<date>-<session-slug>-<topic>.md` (unique name = no collision); ONE conductor writes
  the handoff + commits; commits are serialized. The only rule left to *trust* is "one conductor" — the
  rest is enforced by naming, location, and the reconcile step (2.5).

## Entry points

`_RUNBOOK-capture-ritual.md` (the conductor runs it once) · `_RUNBOOK-git-commit.md` (serialized
commit + lock dance) · `git-push-method` (single-writer split, Desktop-only push) ·
`_RUNBOOK-context-gauge.md` (shares the `session_info` out-of-band hook) · memory
`feedback-parallel-conductor`.
