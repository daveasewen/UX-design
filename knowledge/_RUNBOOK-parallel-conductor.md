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

## Quickstart (the two phrases)

- **To each work session:** *"You're a WORKER — build X. Make only your own new files. Don't write
  GOOD-MORNING or commit it. Give me a RECEIPT when done."*
- **To the one you pick as boss:** *"You're the CONDUCTOR — here are the receipts [paste], merge them,
  write the one GOOD-MORNING, make one commit."*

That's the whole ceremony. **N=1: if only one session is live, ignore all this** — a lone session is
its own conductor and writes its handoff as normal. This only engages at two or more.

## Worker checklist

1. Do the work; create only NEW files (dossiers, reviews, code — unique names).
2. Do NOT write `GOOD-MORNING`/`_LIVE-STATE`/`_FUTURE-STATE`. Touch `MEMORY.md` only as a **surgical
   append**, never a rewrite (a rule you must record → put it in the receipt, let the conductor inscribe).
3. Commit only your OWN disjoint files if you must, serialized; when in doubt, don't commit — hand
   files up.
4. End with a **RECEIPT**: what landed · what's open · files touched · proposed §C queue lines · any
   memory/rule to record · what's committed vs uncommitted.

## Conductor checklist

1. Gather the receipts. (Don't need the workers still open — `mcp__session_info__list_sessions` +
   `read_transcript` read other sessions directly; the same out-of-band hook the context-gauge uses.)
2. Merge into ONE `GOOD-MORNING` (a §B per session, one shared §C), refresh `_LIVE-STATE`, apply any
   memory/rule from the receipts.
3. Make ONE commit (follow `_RUNBOOK-git-commit.md` lock dance); hand Dave a paste-ready summary.
4. Dave pushes via GitHub Desktop only.

## Guardrails

- Never two `git` operations at the same instant (lock contention). Serialize.
- `MEMORY.md` = append surgically, never rewrite, so parallel sessions don't clobber the index.
- A worker never edits shared canon mid-flight — it proposes via the receipt; the conductor decides.

## Entry points

`_RUNBOOK-capture-ritual.md` (the conductor runs it once) · `_RUNBOOK-git-commit.md` (serialized
commit + lock dance) · `git-push-method` (single-writer split, Desktop-only push) ·
`_RUNBOOK-context-gauge.md` (shares the `session_info` out-of-band hook) · memory
`feedback-parallel-conductor`.
