# ADR-0005 — Ratify the pivot: the knowledge engine is the product; orchestration is inherited

**Date:** 2026-07-02 · **Status:** accepted

## Context

The repo was founded (2026-05-31) as a portable multi-discipline agentic harness:
bespoke orchestrator, typed spokes, seven discipline pipelines. That layer received
one dry-run (`runs/dryrun-001`) and no commits after 2026-06-02, while 53 of 54
commits built the knowledge layer: DTCG token stores, 38 gated reference components,
a 15-step enforcement build, a generated composition layer (`canon.css`), runbooks,
and the fixed/flex governance charter.

Market context (2026): orchestration and agent runtimes are commoditising rapidly
(agent SDKs, 30+ spec-driven frameworks, Promenaut itself). Design-system
**enforcement at generation time** remains unoccupied — the ecosystem's own
assessment of the state of the art is "mapped, but not dynamically enforced".
Full analysis: `REVIEW-2026-07-02-critical-regroup.html` (root).

## Decision

1. **The product is the engine:** canon + criteria + gates + runbooks — versioned
   files operated by a host agent (Claude / Cowork / Promenaut runtime).
2. **We do not build or maintain a bespoke orchestrator/runtime.** The host agent
   orchestrates. `harness/` and the discipline pipelines move to
   `archive/harness-v0.1/` (git history preserved via `git mv`).
3. **Surviving harness ideas stay in force where they already live:** the
   craft-vs-taste gate split, HITL as a designed component, tiered checks, the
   error-taxonomy mindset. Typed contracts return if a production runtime is ever
   justified — *on top of* the engine, not instead of it.
4. **State discipline is re-imported as files and conventions** (checkpoints,
   resumption, handoffs) during the calibration proof — where the pain is real —
   not as speculative runtime machinery.
5. **Disciplines are criteria packs on one engine, not pipelines.** New checks
   (CX, heuristics, content) enter at the **advisory** tier and earn promotion to
   blocking by being bite-tested.

## Open item — token-store provenance (two-machine rule) — ✅ RESOLVED 2026-07-02

**Ruling (Dave, desk pickup 2026-07-02):** the premise was wrong — this is an
**agency machine with company access**, not a home machine. Real brand values are
cleared to live in this repo (route (a): machine cleared, `AGENTS.md` amended);
calibration materials may land here under the same clearance. **History purge
DEFERRED** — raw exports remain in git history; accepted risk while the repo is
private; revisit if visibility or host changes. Original item preserved below.

`knowledge/tokens/_raw/` (raw Figma exports, including real brand variable files)
is now **untracked** (`.gitignore` + `git rm --cached`; files remain on local
disk). **Note:** git *history* still contains them — a full purge requires
`git-filter-repo` + force push; that is Dave's call. Separately, the derived
stores (`tokens/*.json`) still carry real brand values, which the entire gate
suite validates against. Options:

- (a) obtain explicit clearance for this machine and amend the rule in `AGENTS.md`; or
- (b) re-base the home stores to synthetic values and validate against real values
  only on the agency machine.

**Owner: Dave.** Until resolved, do not add further raw exports to this repo.

## Consequences

- `README.md`, `AGENTS.md`, `docs/architecture.md` rewritten around the engine
  (this change-set). Cold-start agents get the true mission.
- `skills/design-system-compliance-check` schema pointer updated to the archive path.
- The model-portability claim becomes **testable** (same brief, cold run by another
  model, gates score the output) rather than asserted.
- The calibration proof (re-run a completed HSBC project from its brief; compare
  with what shipped) is the next milestone; canon work is scoped by its journey.
