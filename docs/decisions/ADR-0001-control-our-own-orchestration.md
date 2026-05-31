# ADR-0001 — We control our own orchestration

**Status:** accepted · **Date:** 2026-05-31

## Context
The harness will be deployed on Promenaut ("the operating system for the digital
workforce"). We could inherit their orchestration model, or own a portable one.

## Decision
**We own a self-contained, portable orchestrator spec** (`harness/orchestrator.md`).
Promenaut (and LangGraph/CrewAI) are treated as **swappable execution engines**,
not the source of truth. The contracts, state stores and gate model are the
invariant.

## Rationale
- Portability across machines and models (Claude → GPT‑5.5 → Promenaut) is a hard requirement.
- Anthropic's guidance: don't marry a heavyweight framework; keep abstractions thin and understood.
- It protects us if the deployment target changes.

## Consequence / follow-up
- Interrogate Promenaut's documentation (their `/platform/controls` and docs) to
  confirm how our orchestrator spec maps onto their runtime, and what they
  provide for free (state, logging, HITL). Do this on the agency machine or via
  the browser tools. Record findings as ADR-0005.
