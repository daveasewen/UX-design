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

**N=1:** a lone session is Solo — its own conductor, writes its handoff as normal. The role machinery
only engages at two or more.

## Worker checklist

1. Do the work; create only NEW files (dossiers, reviews, code — unique names).
2. Do NOT write `GOOD-MORNING`/`_LIVE-STATE`/`_FUTURE-STATE`. Touch `MEMORY.md` only as a **surgical
   append**, never a rewrite (a rule you must record → put it in the receipt, let the conductor inscribe).
3. Commit only your OWN disjoint files if you must, serialized; when in doubt, don't commit — hand
   files up.
4. Leave a short **RECEIPT** at the fixed path **`notes/_receipts/<date>-<session-slug>-<topic>.md`**
   (what landed · open · files touched · proposed §C lines · commit state). The session-slug in the
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
3. Make ONE commit (follow `_RUNBOOK-git-commit.md` lock dance); hand Dave a paste-ready summary.
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
