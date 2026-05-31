# Pipeline — UI Design / Build & Review (working)

**Phase:** Develop → Deliver. **Status:** working — the first pipeline to make real.

The highest-impact slice: brief + flows → prototype from the component library →
parallel expert/a11y/brand review → taste gate → dev handoff.

## Flow

```
brief + flow_spec
   │
   ▼
[1 Generator] ──► design_candidate ──► (craft gate) ──► [2 Critic] pass?
   │                                                        │ fail → back to Generator (semantic) or escalate
   ▼ pass
   ├──────────────┬──────────────┐   (parallel — orchestrator dispatches)
   ▼              ▼              ▼
[3 Heuristic]  [4 A11y]      [5 Brand]
 review.json    a11y.json     brand.json
   └──────────────┴──────────────┘
                  ▼ join
            (taste gate — HITL: design lead + taste.md)
                  ▼ approve
            [6 Handoff] ──► handoff_spec + prototype ──► (Gate B: final approval)
```

## Spokes

| # | Spoke | Responsibility | Out (contract) |
|---|---|---|---|
| 1 | **Generator** | Produce a component-level design + prototype using only canon components/tokens | `design_candidate` |
| 2 | **Critic (craft gate)** | Score design-system conformance, token usage, anti-pattern violations, contract integrity → `pass` + recommendations | `craft_review` |
| 3 | **Heuristic reviewer** | Evaluate against Nielsen's 10 heuristics; severity-rated issues | `heuristic_review` |
| 4 | **Accessibility reviewer** | WCAG 2.2 AA audit; each finding cites SC + EN 301 549 clause + severity | `a11y_review` |
| 5 | **Brand reviewer** | Check against brand/experience principles (e.g. GTB brand system) | `brand_review` |
| 6 | **Handoff** | Produce dev handoff spec + Code Connect mapping + prototype artifact | `handoff_spec` |

See `spokes.md` for full per-spoke detail.

## Gates

- **Craft gate (automated):** Critic `pass` required before review fan-out.
- **Taste gate (HITL):** design lead reviews the joined review package against `taste.md`; approves, redirects, or waives a11y finding with recorded reason.
- **Gate B (HITL):** final approval before handoff ships.

## Contracts
All spoke I/O validates against schemas in `contracts/`. Synthetic fixtures live
alongside for dry-runs.

## Knowledge access
- Component graph + tokens via canon (synthetic here; Figma MCP + real library on agency machine).
- Compliance graph for the a11y spoke.
- Brand guidelines via RAG; the GTB brand system is the first brand profile.

## Backing skills
`skills/prototype-from-library/`, `skills/design-system-compliance-check/`,
`skills/heuristic-review/`; plus `design:accessibility-review`,
`design:design-critique`, `design:design-handoff`.
