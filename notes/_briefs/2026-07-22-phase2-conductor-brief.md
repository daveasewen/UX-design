# Phase-2 Conductor brief — fan-out wave 1 (forms lane + feedback lane)

*Cut by the review-pass session, 2026-07-22 (date from `date`). You are the CONDUCTOR per
`knowledge/_RUNBOOK-parallel-conductor.md` — the ONLY writer for shared state + the ONLY committer.
Model: Fable. Read this, then `GOOD-MORNING.md` §A if cold, then the two worker briefs beside this
file. Dave's role assignment comes from his OPENER LINE only — titles are labels.*

## The divvy (this wave)

| Lane | Model | Scope | Source files touched |
|---|---|---|---|
| Worker A | Fable | Forms & entry — brief `2026-07-22-phase2-worker-A-brief.md` (9 items, ordered) | NEW `snippets/*.reference.html` only + receipt |
| Worker B | Fable | Feedback & data — brief `2026-07-22-phase2-worker-B-brief.md` (11 items, ordered) | NEW `snippets/*.reference.html` only + receipt |
| Conductor (you) | Fable | Everything shared — below | registry · gates · gen_showroom · handoff · git |

**SERIAL set (yours alone):** `knowledge/component-types.json` · `MIGRATED_SNIPPETS` in
`_validate_radius.py` · `CATEGORIES` in `gen_showroom.py` · `GOOD-MORNING.md` / `_LIVE-STATE.md` /
`_FUTURE-STATE.md` / `MEMORY.md` · all git. Workers are fenced to NEW files by brief — the fence is
construction, but verify at reconcile anyway.

## Your loop

1. **Seat check:** confirm you are the only conductor (`mcp__session_info__list_sessions`). Workers
   run their ordered lists independently; you don't gate their starts.
2. **Absorb as receipts land** (`notes/_receipts/2026-07-22-phase2-worker-{A,B}-*.md`, or read
   transcripts directly). Per receipt:
   a. **Registry merges:** add proposed `$members` entries to `component-types.json` (selector-mapped,
      per the Button/Modals/Icon-button precedent) → `python3 knowledge/gen_component_partials.py`
      (injection lands physics in the workers' empty marker pairs; activate any
      `<!-- PROPOSED-PARTIAL -->` comments first) → contracts `--check`.
   b. **Gate membership:** add new basenames to `MIGRATED_SNIPPETS` (flips them strict on radius).
   c. **Showroom categories:** map new slugs in `CATEGORIES` (else they rot in 'More').
   d. **Accretion watch (ADR-0013 ruling 3):** if BOTH workers' receipts show the same duplicated
      shape (e.g. field-chrome, close-button), that's OBSERVED duplication — a new registry group
      candidate. Propose to Dave, don't auto-promote. The 32-rule census (`_PARTIALS-GATE.md`) is the
      standing worklist; new components must not grow it.
   e. **Token proposals:** collect, put to Dave — promotion is his alone. Same for icon gaps.
3. **Dave's overlay exports may arrive mid-wave** (showroom pins → exported prompts, each item
   stamped `[mode · theme]` + a selector, rv-file names the snippet). Route: token edits → you;
   worker-owned new snippets → pass into that worker's lane or hold for reconcile.
4. **Reconcile before committing (runbook step 2.5):** `git status --short` — name every path against
   the receipts; never blind `git add -A` with workers live. Then the FULL serial
   `python3 knowledge/_build_all.py` — your run is authoritative (worker builds may have interleaved
   writes on generated surfaces; deterministic regen self-heals, your green run proves it).
5. **ONE commit** per `_RUNBOOK-git-commit.md` — the lock dance, msgfile UNIQUE under outputs/
   (`head -1` before `-F`; see the 2026-07-22 stale-msgfile gotcha). Paste-ready summary for Dave;
   he pushes via GitHub Desktop.
6. **Capture ritual** (`_RUNBOOK-capture-ritual.md`) at wrap: handoff as STRAND MENU + lanes (never a
   mega-list) · both names (retrospective + forward) · a forward DIVVY PLAN (wave 2: remaining P1s —
   Data grid (51) + Charts kit (53) are lane-sized on their own; then P2 depth / Layer-2
   templates+shells, the load-bearing gap) · dates from `date`.

## Quality contract (unchanged from the strategy)

Nothing counts until: build green (51+ steps, non-zero on fail) · renders clean 4 themes ×
light/dark in the showroom · token-wired colour AND shape · no census growth · type composites ·
AA. Workers self-verify per component; you re-verify at reconcile. Render-verify remains OWED
in-sandbox (headless-shell refusal) — Dave reviews live HTML, now WITH pin-comments in every pane.

## Standing context you inherit

Theme posture: **Legacy FROZEN · Mono/Console/SC in design development.** B-D7 press physics =
pixel-true, theme-dialled (Legacy+SC zero it) — new pressables inherit via partials, zero JS ever.
SC dark values + 4 held whites + Console radius px are provisional-agent AWAITING Dave — value-level
only; do not block on them; his rulings retro-propagate as token edits. Button-states finesse pass
is QUEUED (§C·3b), NOT this wave — don't let workers drift into it.
