# Architecture

The engine is **data + executables, operated by a host agent**. There is no bespoke
runtime (ADR-0005). The original two-layer harness design (2026-05-31) is preserved
at `archive/harness-v0.1/` and in `research-dossier.md` (historical).

```
┌──────────── HOST AGENT (Claude / Cowork / Promenaut) ────────────┐
│ orchestration · state · context assembly · retries — inherited    │
└───────────────────────────────────────────────────────────────────┘
        ▼ operates via runbooks (knowledge/_RUNBOOK-*.md)
┌────────────────────────────── ENGINE ─────────────────────────────┐
│ CANON      tokens/ (DTCG stores) · snippets/ (gated references)   │
│            canon/canon.css (generated composition layer)          │
│ CRITERIA   components/*.meta.json · rubrics · _FIXED-FLEX-CHARTER │
│ GATES      _validate_*.py · _build_all.py (15 steps, blocking)    │
│ RUNBOOKS   the method, written down                               │
└───────────────────────────────────────────────────────────────────┘
```

**Flow:** brief → criteria contract (becomes the gates) → retrieve + generate
N variants (register dial) → blocking gates → advisory signals → render + visual
QA → human taste call → promote winner to canon.

## Check tiers

- **Blocking** (withhold "done"): a11y, contrast ×2, token fidelity, icon source,
  dark-surface, coverage, integrity, compose.
- **Advisory** (annotate, never block): states-completeness probe, heuristics,
  CX/journey signals — candidates earn promotion by bite-testing.
- **Human taste call**: the one judged gate; kept cheap and rare by everything above.

## Invariants vs replaceables

- **Invariant (the value):** token stores, criteria, gates, runbooks — versioned
  files, model-independent. "Portable data, adapted operator."
- **Replaceable (the engine room):** the operating agent/model and its host
  platform. The gates make a model swap *testable*: same brief, cold run, gates
  score the output.

## State discipline (open work)

Checkpoints, resumption and handoff conventions are currently informal (handoff
docs + memory). ADR-0005 §4: re-import the original design's state discipline as
files and conventions during the calibration proof.
