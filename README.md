# Apollo

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
  an 18-step build in which a11y, contrast, token fidelity, icon provenance,
  coverage and integrity are **blocking**. Verification = enforcement.
- **Runbooks** — `knowledge/_RUNBOOK-*.md`: the method written down, so a
  cold-start agent can operate the engine without this chat's history.

**The orchestrator is the host agent** (Claude / Cowork / Apollo runtime). We do
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
call** (a brief human decision) → winner **promoted to canon** — judgment spent once,
retrieved forever.

## Status

Engine built and green (18/18 build steps). Next milestone: the **first real test**
— a scoped novel-work screen with an external stakeholder (a colleague, not us), the
engine bounded to generate → enforce → compose → register → promote; the **calibration
re-run** (a completed project, blind, compared with what shipped) stays as the rigour
backstop. Canon/component work is scoped by that project's journey, not by completeness.

The standing critical review and its eight decisions:
`reviews/REVIEW-2026-07-02-critical-regroup.html`.

## Run the build

```
python3 knowledge/_build_all.py
```

Regenerates every derived view in dependency order; exits non-zero on any gate
failure. This is the single command to trust the knowledge base.

## Repo map

```
.
├── README.md                    ← you are here (front door + this map)
├── AGENTS.md                    ← operating manual for any agent in this repo
├── GOOD-MORNING.md              ← latest session handoff (cold-start reads this first)
├── _LIVE-STATE.md               ← live / dead / open ledger — what is true now
├── MODEL-ROUTING.md             ← which model for which work
│
├── knowledge/                   ← THE ENGINE: canon · criteria · gates · runbooks
│   ├── tokens/                  ← DTCG token stores (+ _raw/, untracked — ADR-0005)
│   ├── snippets/                ← gated reference components (source of truth)
│   ├── components/              ← per-component criteria (metas, confidence-tiered)
│   ├── canon/                   ← generated composition layer (canon.css + generators)
│   ├── compliance/              ← WCAG knowledge graph
│   └── _fitness-test/           ← composed screens, journeys, the gallery
│
├── reviews/                     ← consumable outputs: REVIEW-* · PLAN-* · PRESENTATION-* · dossier renders
├── notes/                       ← thinking: _VISION-* · _STRATEGY-* · test plans · Swiss-design reference
├── projects/                    ← project inputs (e.g. payments/ — calibration brief, guides, assets)
│
├── skills/                      ← the engine's gated Agent Skills (SKILL.md folders)
├── designer-skills-v1/          ← designer Copilot pack (skills + built KB; KB gitignored, rebuild via script)
├── review-skills/               ← review toolkit: review-dossier · component-review · swiss-design-system
│
├── docs/                        ← research dossier · architecture · ADRs (decisions/)
├── runs/                        ← historical run artifacts (proofs, contracts, dryruns)
├── system-manager/              ← decision-capture design space
├── second-system-govuk/         ← GOV.UK second-system probe
├── digital-experience-transformation/  ← leadership narrative (separate strand)
├── archive/                     ← superseded docs + original harness-v0.1 design (ADR-0005)
└── _to_delete/                  ← staging for removal (gitignored; bridge cannot delete)
```

## Data hygiene

Resolved (ADR-0005): this is an **agency machine with company access** — the
"home = synthetic only" premise was wrong; real brand values (tokens, palettes,
Figma exports) are cleared to live here. Raw exports under `knowledge/tokens/_raw/`
stay untracked (keeps the repo lean); git *history* still holds earlier raw exports —
purge deferred by ruling (accepted risk while the repo is private).
