# Compliance knowledge graph

The audit-grade compliance graph: **rule → component → check → success criterion → legal clause**. It links every component to the WCAG success criteria it must satisfy, with an automatable/manual check, severity, and the authoritative sources.

## Conformance basis

Graded against **WCAG 2.2 AA** — the minimum set by **HSBC's digital accessibility framework**, governed by **Group Digital Experience and Accessibility** (mandatory on all HSBC digital projects). See `knowledge/guidelines/digital-accessibility-standards.md` and `knowledge/components/_ACCESSIBILITY-CONFORMANCE.md`.

## Files

```
compliance/
├── rule.schema.json          # contract for a single rule node (one checkable SC)
├── EXAMPLE-contrast-rule.json # synthetic example (kept for reference)
├── rules/                     # one schema-conformant rule per WCAG SC (31 files)
│   └── wcag-<sc>-<slug>.json
├── graph-index.json          # both-way adjacency: by_sc {SC -> [components]}, by_component {component -> [SCs]}
└── _build_compliance_kg.py   # generator (regenerates rules/ + index from component metas)
```

## How it's built (reproducible)

`_build_compliance_kg.py` reads every `knowledge/components/*.meta.json` `accessibility.relatedSC` array, parses the leading SC number, and derives the **`applies_to` edges straight from source-of-truth** (so the graph never drifts from the components). It then attaches each SC's metadata (title, level, WCAG versions, check type/threshold, severity, WCAG URL, EN 301 549 clause, internal policy ref) and writes one rule file per SC plus the index. Re-run after editing component metas:

```
python3 knowledge/compliance/_build_compliance_kg.py
```

## Current graph (generated 2026-06-18)

- **31 rules** across **32 components**, all validated against `rule.schema.json` (0 failures).
- **Levels:** 15 × A, 14 × AA, 2 × AAA (`2.3.3 Animation from Interactions`, `2.4.8 Location` — beyond the AA bar, cited as best practice).
- **Severities:** 3 critical (`2.1.1 Keyboard`, `2.1.2 No Keyboard Trap`, `4.1.2 Name/Role/Value`), 24 serious, 4 minor.
- **WCAG 2.2-new SCs in the graph:** `2.4.11 Focus Not Obscured` (Modals, Navigations, Search field, Tabs, Tooltip), `2.5.7 Dragging Movements` (List items, Quick actions, Reorder, Slider), `2.5.8 Target Size (Minimum)` (all interactive components).

## Traversing the graph

- **Component → obligations:** `graph-index.json` → `by_component["Modals"]` → `["1.4.3","2.1.2","2.4.3","2.4.11","2.5.8","4.1.2"]` → load `rules/wcag-<sc>-*.json` for the check, severity, threshold and sources.
- **SC → affected components:** `by_sc["2.4.11"]` → `["Modals","Navigations","Search field","Tabs","Tooltip"]`.
- Each rule carries `sources.wcag_url` (Understanding page), `sources.en301549_clause` (EN 301 549 9.x.x.x; 2.2-only SCs flagged pending alignment), and `sources.internal_policy_ref`.

## Notes / future
- EN 301 549 clauses mirror WCAG SC numbering (9.x.x.x); the three WCAG-2.2-only SCs are flagged "pending EN 301 549 alignment to WCAG 2.2."
- `check.type` is the *gradeability* hint for an automated audit harness (automated / semi-automated / manual). Thresholds are set where machine-checkable (contrast 4.5:1/3:1, non-text 3:1, target 24px, reflow 320px, resize 200%).
- As more components are ingested, re-run the generator — the graph stays in sync with the component metas.
