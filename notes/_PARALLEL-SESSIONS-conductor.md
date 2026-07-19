# Parallel sessions — the conductor pattern (single-writer for shared state)

*Raised 2026-07-19 when two Cowork sessions ran at once and BOTH tried to commit + rewrite
`GOOD-MORNING.md`. Dave's own diagnosis: "I should be running a cold agent from the main chat."
This note captures the pattern; promote to a runbook + `AGENTS.md` rule in a quiet single session
(that edit touches AGENTS.md, itself shared — do it when only one session is live).*

---

## The problem

Multiple sessions share one repo + one memory store. Three kinds of shared state, by collision risk:

1. **Handoff files — `GOOD-MORNING.md` · `_LIVE-STATE.md` · `MEMORY.md` (+ `_FUTURE-STATE.md`).**
   These get *rewritten*, so it's **last-writer-wins** — one session silently clobbers the other's
   §B/§C. The dangerous one.
2. **Git** — same repo. Disjoint file sets merge fine; the only hazard is `.git/index.lock` if two
   commits fire at the same instant (the sandbox lock-guard, see `_RUNBOOK-git-commit.md`). Serialize
   and it's safe.
3. **New files** (dossiers, reviews, code) — never collide; unique names. Always safe.

## The rule: ONE conductor writes shared state

Exactly one actor owns the handoff files and the merged commit per reconcile. Everyone else only
produces new/append-only files and hands their result up.

- **Workers** (the parallel sessions): do the work, create NEW files only, **never** write
  `GOOD-MORNING`/`_LIVE-STATE`/`MEMORY`/`_FUTURE-STATE`, **never** commit those. Each ends by emitting
  a compact **RECEIPT** — what landed · what's open · files touched · proposed §C queue lines · any
  memory/rule to record — either in chat or as a disjoint file `_receipts/<session>-<date>.md`.
- **Conductor** (the "main chat", ideally a COLD agent): gathers the receipts, merges them into ONE
  `GOOD-MORNING` (§B per-session, one shared §C), ONE `_LIVE-STATE` refresh, ONE `MEMORY` update, and
  does ONE serialized commit. Single writer ⇒ no clobber.

**Why cold:** a fresh conductor carries neither session's bias; it treats the receipts (and, if needed,
the raw transcripts) as source of truth and reconciles neutrally. It's also cheap.

## The hook that makes it real

The conductor doesn't need the workers to still be open. The `session_info` tools read other sessions
directly:
- `mcp__session_info__list_sessions` — lists sessions (`is_child` flags children).
- `mcp__session_info__read_transcript` — reads a session's full transcript.

So a cold conductor can, at reconcile time: list the live/recent sessions → read each transcript (or
its receipt) → distill → write the single handoff + commit. (These are the same tools the context-gauge
uses out-of-band.)

## It stays flexible — the role scales to N=1

This is a **role**, not always a separate agent:
- **One session:** it is its own conductor — writes its own handoff exactly as today. No overhead.
- **Two+ sessions:** the conductor role separates out (the main chat, or a spawned cold agent). Workers
  drop to receipt-only.

Trigger: *if more than one session touched shared state this round, a single conductor does the merge;
otherwise the lone session self-conducts.*

## Guardrails

- Workers commit only their OWN disjoint new files, serialized (never two `git` ops at the same
  instant); the conductor commits the merged handoff. When in doubt, workers don't commit — they hand
  files to the conductor.
- `MEMORY.md` edits are **surgical appends**, never rewrites, so two sessions don't clobber the index.
- A worker that must record a rule writes it to a receipt for the conductor to inscribe — it does not
  edit the shared canon itself mid-flight.

## Next step

Promote to `_RUNBOOK-parallel-conductor.md` + an `AGENTS.md` clause ("worker vs conductor; never write
handoff files as a worker"), and add a `_receipts/` convention. Do it in a single-session slot.
Entry points: `_RUNBOOK-capture-ritual.md` · `_RUNBOOK-git-commit.md` · `git-push-method` (single-writer
split) · `_RUNBOOK-context-gauge.md` (shares the `session_info` out-of-band hook).
