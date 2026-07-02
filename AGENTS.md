# AGENTS.md — Smart Design System

> Root operating manual for any agent working in this repository. The nearest
> `AGENTS.md` wins; this is the root. Conforms to the open
> [AGENTS.md](https://agents.md/) format.

## What this project is

A **governed design-system engine**: canon (tokens + gated components) + criteria
(metas, rubrics, charter) + gates (executable checks) + runbooks (the method).
**The orchestrator is you, the host agent.** There is no bespoke runtime — see
`docs/decisions/ADR-0005`. The original harness design is archived at
`archive/harness-v0.1/`.

## Core principles (non-negotiable)

1. **Verification = enforcement.** Definitions of done are executable and withhold
   "done" by exiting non-zero. Never weaken a gate to make work pass; fix the work,
   or take an allow-list entry with a written reason.
2. **Retrieval, not recall.** Brand primitives (colour, type, spacing, motion) are
   retrieved from `knowledge/tokens/` and `canon.css`. Never type brand values from
   memory. Never invent a hex, an icon, or a component that retrieval can supply.
3. **Craft is scored; taste is judged.** Gates and signals compute the evidence;
   the human makes the taste call — packaged small (a ~20-second decision), never
   delegated to a model.
4. **Convergent and divergent stay separate.** Gate canon; never gate exploration.
   Tiers: T1 canon (all retrieved, compose-gate green) · T2 candidate (fixed
   retrieved + derived candidates, flagged for promotion) · T3 exploration (no
   gate — a signal, not a deliverable).
5. **Checks are tiered.** Few blocking objective gates; many cheap advisory
   signals; a small set of human taste calls. New checks (CX, heuristics, content)
   enter at the **advisory** tier and earn promotion by being bite-tested.
6. **Fix the snippet, not the output.** Snippets are the reviewed source of truth;
   `canon.css` AUTO blocks are generated. Edit snippet → regenerate → re-gate.
   Never hand-edit generated blocks.
7. **Confidence is explicit.** Assert only what was observed; mark the rest
   `inferred` or `REVIEW` (see `knowledge/_CONFIDENCE.md`).
8. **Render and look.** Green gates mean "automatable checks passed", not "done".
   Every substantive visual change gets rendered and inspected — every real defect
   to date was visual and passed the static gates.

## How to work

- Start at `knowledge/_NEXT-SESSION.md` (or the handoff doc the session names),
  then `knowledge/README.md` for the build.
- The method lives in `knowledge/_RUNBOOK-*.md`. Follow the runbooks; improve them
  when they're wrong — curation is part of the job. Do not add new coordination
  docs when an existing one can hold the content.
- One command to trust the knowledge base: `python3 knowledge/_build_all.py`.
- Every session gets a short, distinct title. End substantial sessions with a
  handoff note so a cold-start agent can resume.
- Commits are conventional (`feat:`, `fix:`, `docs:`, `chore:`); provide a
  paste-ready summary + description with every commit.

## Data hygiene

- **RESOLVED (Dave, ADR-0005 close-out):** this is an **agency machine with
  company access** — the old "home machine = synthetic only" premise was wrong.
  Real design-system values (tokens, palettes, Figma exports) are cleared to
  live in this repo. Calibration project materials may land here too.
- `knowledge/tokens/_raw/` stays untracked (keeps the repo lean; raw exports
  live on disk only). Git *history* still contains earlier raw exports — purge
  via git-filter-repo DEFERRED by ruling (accepted risk, private repo; revisit
  if the repo ever changes visibility or host).

## Compliance bar

Build to **WCAG 2.2 AA** (engineering target); **EN 301 549 / WCAG 2.1 AA** is the
legal floor. WCAG version is a config parameter. See `docs/decisions/ADR-0004`.

## Definition of done (any piece of work)

The relevant gates pass (or an allow-list entry exists with a written reason);
anything visual has been rendered and looked at; new judgment is captured in the
meta/criteria layer (not only in CSS or chat); and the handoff/runbook trail lets
a cold-start agent pick up where you left off.
