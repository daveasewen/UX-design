# System Manager — design-system governance & evolution

> A separate strand of work about the **continual development of the design
> system itself**: how it changes over time, who decides, how decisions are
> captured, and how changes propagate to the projects that consume it.

**Status:** exploratory · started 2026-06-22 (Dave) · **deliberately isolated**

## Why this folder exists

The rest of the repo is about *running* the pipeline (build a component →
review it → promote it → hand it off). This folder is about *governing the
system over time* — the meta-layer. It is the operating manual for the
"design system manager" role and the processes that keep the system coherent
as it feeds several projects.

## Isolation (important)

Nothing here is wired into `AGENTS.md`, the harness, or any pipeline yet. It
does not change how any current run behaves. It is a design space. When a
proposal here is ready to become real, it graduates by an explicit edit to the
engine docs / ADRs — not by sitting in this folder.

## Subjects (one file each)

| # | Subject | File | Status |
|---|---|---|---|
| 01 | Capturing design decisions | [`01-capturing-design-decisions.md`](01-capturing-design-decisions.md) | draft for review |

`decisions/` will hold worked examples (a Design Decision Record template +
samples) if subject 01 is adopted.
