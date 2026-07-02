# Smart Design System (project Promenaut)

A **governed design-system engine** for agentic generation: senior design judgment
encoded as executable criteria, enforced by gates that withhold "done".

Generation is a commodity — this repo is the layer around any generator. It holds
four kinds of asset:

- **Canon** — `knowledge/tokens/` (DTCG token stores), `knowledge/snippets/`
  (38 gated reference components), `knowledge/canon/canon.css` (the generated
  composition layer). *Retrieval, never recall:* fixed brand primitives are
  retrieved from the store, so generated work cannot drift off-brand.
- **Criteria** — `knowledge/components/*.meta.json` (per-component judgment:
  token bindings, contrast pairs, required ARIA, states), the rubrics, and
  `knowledge/_FIXED-FLEX-CHARTER.md` (what is fixed, what may flex, and the
  register dial).
- **Gates** — `knowledge/_validate_*.py` orchestrated by `knowledge/_build_all.py`:
  a 15-step build in which a11y, contrast, token fidelity, icon provenance,
  coverage and integrity are **blocking**. Verification = enforcement.
- **Runbooks** — `knowledge/_RUNBOOK-*.md`: the method written down, so a
  cold-start agent can operate the engine without this chat's history.

**The orchestrator is the host agent** (Claude / Cowork / Promenaut runtime). We do
not build or maintain a bespoke pipeline runtime — see
[`docs/decisions/ADR-0005`](docs/decisions/ADR-0005-ratify-knowledge-engine-pivot.md).
The original harness design (2026-05-31) is preserved at `archive/harness-v0.1/`;
its surviving ideas — craft vs taste gates, HITL as a designed component, typed
contracts — live on inside the gates and runbooks.

## Operating model

brief → **criteria contract** (the definition of done, written first — it *becomes*
the gates) → retrieve + generate **N variants** across registers (sober → balanced →
expressive) → **blocking gates** filter (kill the broken) → **advisory signals**
annotate (heuristics, CX, states) → **render + visual QA** → one **human taste
call** (~20 seconds) → winner **promoted to canon** — judgment spent once,
retrieved forever.

## Status

Engine built and green (15/15 build steps). Next milestone: the **calibration
proof** — re-run a completed HSBC project from its original brief, blind, and
compare the engine's output with what actually shipped. Canon/component work is
scoped by that project's journey, not by completeness.

The standing critical review and its eight decisions:
`REVIEW-2026-07-02-critical-regroup.html`.

## Run the build

```
python3 knowledge/_build_all.py
```

Regenerates every derived view in dependency order; exits non-zero on any gate
failure. This is the single command to trust the knowledge base.

## Repo map

```
.
├── README.md                    ← you are here
├── AGENTS.md                    ← operating manual for any agent in this repo
├── knowledge/                   ← THE ENGINE: canon · criteria · gates · runbooks
│   ├── tokens/                  ← DTCG token stores (+ _raw/, untracked — ADR-0005)
│   ├── snippets/                ← gated reference components (source of truth)
│   ├── components/              ← per-component criteria (metas, confidence-tiered)
│   ├── canon/                   ← generated composition layer (canon.css + generators)
│   ├── compliance/              ← WCAG knowledge graph
│   └── _fitness-test/           ← composed screens, journeys, the gallery
├── docs/                        ← research dossier · architecture · ADRs
├── skills/                      ← portable Agent Skills (SKILL.md folders)
├── system-manager/              ← decision-capture design space
├── runs/                        ← historical run artifacts
├── digital-experience-transformation/  ← leadership narrative (separate strand)
└── archive/harness-v0.1/        ← the original harness design (ADR-0005)
```

## Data hygiene (two-machine rule)

Home machine: synthetic + public data. Agency machine: real assets. Raw Figma
exports under `knowledge/tokens/_raw/` are untracked as of ADR-0005; see that
ADR's open item on token-store provenance before adding any real asset here.
