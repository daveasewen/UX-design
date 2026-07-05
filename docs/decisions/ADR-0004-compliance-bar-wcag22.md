# ADR-0004 — Compliance bar: build to WCAG 2.2 AA, version as a parameter

**Status:** accepted · **Date:** 2026-05-31

> **AUDIT 2026-07-05 (Tier A batch 2, Dave): decision VOUCHED + rationale amended.** The decision
> (build to 2.2 AA, superset-safe, clause-cited) is correct and built. Amend adds the **foundational
> driver the ADR originally omitted**: HSBC's aspiration to be **the most digitally accessible bank
> in the world** — the bar exists to *lead*, not merely to comply; 2.2 AA is the floor of that
> aspiration, not its ceiling (it should ratchet over time). Legal floor is the backstop beneath the
> aspiration, not the primary reason. See `knowledge/_DECISION-AUDIT.md`.

## Context
Regulated financial-services context with a mixed compliance surface. The
European Accessibility Act is enforceable since 28 June 2025 and covers banking;
EN 301 549 currently incorporates WCAG 2.1 AA and is being updated to 2.2.

## Decision
- **Engineering target: WCAG 2.2 AA.**
- **Legal floor acknowledged: EN 301 549 / WCAG 2.1 AA** (today).
- **WCAG version is a config parameter** (`a11y_review.wcag_version`), default `2.2-AA`.
- Every a11y finding cites the **success criterion** and the **EN 301 549 clause** (compliance graph).

## Rationale
**Primary (foundational) driver:** HSBC's aspiration to be **the most digitally accessible bank in
the world.** The bar is set to *lead*, not merely to satisfy a floor — so the engineering target
sits above the legal minimum by design and is expected to ratchet upward over time (AAA where
feasible, WCAG 3.0 readiness) as the aspiration demands.

**Backstop:** building to 2.2 AA now also avoids rework when EN 301 549 folds in 2.2, gives
audit-grade headroom, and 2.2 is a superset of 2.1. EAA fines reach €500k, so the legal floor is
non-negotiable — but it is the floor *beneath* the aspiration, not the reason for the bar.

## Consequence
The accessibility spoke blocks handoff on any non-waived AA failure; waivers are
human-approved at the taste gate with a recorded reason.
