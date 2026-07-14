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
   Register is the *level of inference* (charter §9); the cardinal curbs hold at every
   band — retrieved, never recalled.
3. **Craft is scored; taste is judged.** Gates and signals compute the evidence;
   the human makes the taste call — packaged small (a brief human decision, not a
   review), never delegated to a model.
4. **Convergent and divergent stay separate.** Gate canon; never gate exploration beyond the cardinal floor (§9) — the road is free, the cardinals always hold.
   Tiers: T1 canon (all retrieved, compose-gate green) · T2 candidate (fixed
   retrieved + derived candidates, flagged for promotion) · T3 expressive — max
   inference within the cardinal curbs (retrieved), divergence-probed (charter §8/§9).
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

- Start at the **latest handoff** the most recent session named (e.g. `GOOD-MORNING.md`),
  then **`_LIVE-STATE.md`** (the live/dead/open supersession ledger — what's true now, what's
  retired, what's parked; `ADR-0007`), then `knowledge/README.md` for the build. Keep these
  entry points current — they are the first things every cold-start agent reads; if stale,
  refresh before continuing. **`_LIVE-STATE.md` is the state-retention spine across sessions:
  trust it for what supersedes what, and refresh it at end of session with the handoff.**
- The method lives in `knowledge/_RUNBOOK-*.md`. Follow the runbooks; improve them
  when they're wrong — curation is part of the job. Do not add new coordination
  docs when an existing one can hold the content.
- One command to trust the knowledge base: `python3 knowledge/_build_all.py`.
- Every session gets a short, distinct title. End substantial sessions with a
  handoff note so a cold-start agent can resume.
- **Model routing (`MODEL-ROUTING.md`).** Name the session's work → pick its model from the
  routing table (Fable = rationed premium · Opus = default/complex · Sonnet = throughput to a
  plan · Haiku = chores). Default down, escalate up. Keep judgment on the strong model but
  **delegate chore/throughput sub-tasks to cheaper subagents** — don't run mechanical work on the
  judgment model. Model choice never moves who promotes/vouches (that's Dave, always).
- Commits are conventional (`feat:`, `fix:`, `docs:`, `chore:`); provide a
  paste-ready summary + description with every commit.
- **Git split (RULED 2026-07-05):** Claude makes ALL commits in the terminal
  (local, no creds) and clears any stale `.git/*.lock` before handoff (via
  `mcp__cowork__allow_cowork_file_delete` if `rm` is blocked). Dave does the
  **push through GitHub Desktop only** — never push from the terminal (it hangs
  on credentials), never commit in Desktop, keep Desktop closed during commits.
  One tool on the auth layer. (Supersedes the 07-02 terminal-only push ruling.)
- **Supersession discipline (non-negotiable).** Any ruling that changes a definition
  or retires an approach must, in the same pass: (a) **tombstone** every artifact it
  kills — a `⚠️ SUPERSEDED <date> — Superseded-by: <ref>` banner at the top of the file
  (so a cold-start grep can't resurrect it); and (b) **log the propagation gap** — which
  downstream docs/mocks still speak the old language — in the relevant memory + handoff.
  `superseded` is a first-class state: a live doc must never point at a dead node. The
  review-dossier "stale" pass is the periodic catch. *(Instituted 2026-07-05 after a cold
  start resurrected the retired looks-based register dial.)*

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

## Imported Claude Cowork project instructions
