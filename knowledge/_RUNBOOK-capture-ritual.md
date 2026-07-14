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

## The five steps, in order

1. **Refresh `_LIVE-STATE.md`.** Update LIVE / SUPERSEDED-DEAD / OPEN / PLANNED-TARGET sections for
   anything that changed this session. Bump the `*Last refreshed: YYYY-MM-DD*` line at the top to
   today. If a ruling killed something, tombstone the artifact **and** log the propagation gap in the
   same pass (supersession discipline, non-negotiable per `AGENTS.md`).
2. **Write/refresh `GOOD-MORNING.md`.** Session-in-one-line → what landed → on-your-desk (commit
   state) → queue next (numbered, actionable). This is the cold-start entry point for the *next*
   session — write it for a reader with zero memory of this one.
3. **Update memory.** Any `feedback` / `project` / `user` / `reference` memory that's new or changed
   this session, plus the one-line pointer in `MEMORY.md`. Check for stale memories the session
   disproved and correct or remove them.
4. **Record decision nodes with supersession discipline.** Any new ruling gets logged where decisions
   live (ADR, charter section, or `_LIVE-STATE`), cross-linked both ways, seeded as `unaudited`
   per the decision-audit method (`_RUNBOOK-decision-audit.md`) — never self-promoted to `vouched`.
5. **Commit + push.** Claude commits in terminal with a paste-ready summary + description, clears any
   stale `.git/*.lock` files. **Dave pushes via GitHub Desktop only** — never terminal push, never a
   Desktop commit, Desktop closed while Claude commits (memory `git-push-method`).

## What "done" looks like

All five steps complete = the session is safely captured. The transcript never has to be the source
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
`_RUNBOOK-decision-audit.md` (validation-state discipline for step 4).
