# ADR-0004 — Compliance bar: build to WCAG 2.2 AA, version as a parameter

**Status:** accepted · **Date:** 2026-05-31

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
Building to 2.2 AA now avoids rework when EN 301 549 folds in 2.2, gives
audit-grade headroom, and 2.2 is a superset of 2.1. EAA fines reach €500k, so the
floor is non-negotiable.

## Consequence
The accessibility spoke blocks handoff on any non-waived AA failure; waivers are
human-approved at the taste gate with a recorded reason.
