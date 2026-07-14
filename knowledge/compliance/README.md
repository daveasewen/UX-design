# Compliance knowledge graph

The audit-grade compliance graph: **rule → component → check → success criterion → legal clause**. It links every component to the WCAG success criteria it must satisfy, with an automatable/manual check, severity, and the authoritative sources.

## Conformance basis

Graded against **WCAG 2.2 AA** — the minimum set by **HSBC's digital accessibility framework**, governed by **Group Digital Experience and Accessibility** (mandatory on all HSBC digital projects). See `knowledge/guidelines/digital-accessibility-standards.md` and `knowledge/components/_ACCESSIBILITY-CONFORMANCE.md`.

## Files

```
compliance/
├── rule.schema.json                # contract for a single rule node (one checkable SC)
├── EXAMPLE-contrast-rule.json       # synthetic example (kept for reference)
├── rules/                           # one schema-conformant rule per WCAG SC (31 files)
│   └── wcag-<sc>-<slug>.json
├── graph-index.json                # both-way adjacency + verification{} + external_automatable_refs{}
├── _build_compliance_kg.py         # generator (applies_to index from component metas)
├── _build_verification_edges.py    # generator (verified_by — OUR checks, OUR build; advisory)
├── _import_axe_rules.py            # generator (external_automatable_refs — off-the-shelf tooling that EXISTS; advisory)
└── _vendor/                         # vendored external registry snapshots (offline, reproducible)
    ├── axe-core-rules-snapshot.json
    └── _INGEST-NOTES.md            # provenance + how to refresh each snapshot
```

## How it's built (reproducible)

`_build_compliance_kg.py` reads every `knowledge/components/*.meta.json` `accessibility.relatedSC` array, parses the leading SC number, and derives the **`applies_to` edges straight from source-of-truth** (so the graph never drifts from the components). It then attaches each SC's metadata (title, level, WCAG versions, check type/threshold, severity, WCAG URL, EN 301 549 clause, internal policy ref) and writes one rule file per SC plus the index. Re-run after editing component metas:

```
python3 knowledge/compliance/_build_compliance_kg.py
```

Two more generators layer additional edges onto the same rule files + index, both advisory (never gate the build), both re-run via `knowledge/_build_all.py`:

- `_build_verification_edges.py` — runs LATE (after the contrast audits + a11y gate) and records `verified_by`: is an executable check wired into **our** build, and does it currently pass.
- `_import_axe_rules.py` — runs right after step 1 and records `external_automatable_refs`: does an off-the-shelf tool (axe-core) **exist** that could check this SC, whether or not we've adopted it. Reads a vendored, offline snapshot — see `_vendor/_INGEST-NOTES.md` to refresh it.

## Current graph (generated 2026-06-18; verification + external-refs added 2026-07-14)

- **31 rules** across **32 components** (accessibility-tagged; 38 components total), all validated against `rule.schema.json` (0 failures).
- **Levels:** 15 × A, 14 × AA, 2 × AAA (`2.3.3 Animation from Interactions`, `2.4.8 Location` — beyond the AA bar, cited as best practice).
- **Severities:** 3 critical (`2.1.1 Keyboard`, `2.1.2 No Keyboard Trap`, `4.1.2 Name/Role/Value`), 24 serious, 4 minor.
- **WCAG 2.2-new SCs in the graph:** `2.4.11 Focus Not Obscured` (Modals, Navigations, Search field, Tabs, Tooltip), `2.5.7 Dragging Movements` (List items, Quick actions, Reorder, Slider), `2.5.8 Target Size (Minimum)` (all interactive components).

## Three edge types

`applies_to` is the **claimed** edge — a component meta asserts it satisfies a WCAG SC. Derived straight from source-of-truth, so it never drifts, but nothing runs to check it's true.

`verified_by` is the **verified** edge (built 2026-07-14): non-null only where an executable check runs in **our** build (`_build_all.py`) and its current result is recorded. Today that's **4 of 31 SCs**:

| SC | Mechanism | Granularity |
|---|---|---|
| `1.4.3` Contrast (Minimum) | our token-level dark-mode contrast audit, gates the build | token |
| `1.4.11` Non-text Contrast | our token-level dark-mode contrast audit, gates the build | token |
| `2.3.3` Animation from Interactions | our a11y gate scans every snippet for missing `prefers-reduced-motion`, gates the build | component |
| `2.5.8` Target Size (Minimum) | our a11y gate measures every control's CSS box against the 24px floor, gates the build | component |

`external_automatable_refs` is the **available** edge (built 2026-07-14, the other half of the 2026-07-10 "cheap-now slice"): does an off-the-shelf tool exist for this SC, regardless of whether we run it. Imported from axe-core v4.12.1 (vendored snapshot, no live network at build time). **15 of 31 SCs have at least one axe-core rule tagged against them** — see `knowledge/_EXTERNAL-AUTOMATABLE-REFS.md` for the full breakdown, which splits those 15 into:

- **13 "easy wins"** — axe-core covers it, we haven't wired it up (e.g. `1.1.1`, `1.3.1`, `4.1.2`, `2.4.4`).
- **2 already wired** — `1.4.3` and `2.5.8` show up in both `verified_by` and axe-core's coverage (we built our own check independently; axe-core confirms the SC is automatable in principle).
- **16 have no OSS axe-core coverage at all**, including two we already verify ourselves (`1.4.11`, `2.3.3`) — our bespoke dark-mode contrast audit and reduced-motion scan cover ground the open-source axe-core rule set doesn't. Worth knowing: our custom gates aren't redundant with off-the-shelf tooling here.

**A correction the verification pass surfaced:** `2.3.3`'s `check.type` was hand-typed as `manual` in `_build_compliance_kg.py`'s SC lookup table, but the a11y gate has enforced it (gating) since before this change — the metadata just hadn't caught up. Corrected to `semi-automated`.

## Traversing the graph

- **Component → obligations:** `graph-index.json` → `by_component["Modals"]` → `["1.4.3","2.1.2","2.4.3","2.4.11","2.5.8","4.1.2"]` → load `rules/wcag-<sc>-*.json` for the check, severity, threshold, sources, `verified_by`, and `external_automatable_refs`.
- **SC → affected components:** `by_sc["2.4.11"]` → `["Modals","Navigations","Search field","Tabs","Tooltip"]`.
- **SC → is this actually enforced (by us):** `graph-index.json` → `verification.by_sc["1.4.3"]` → the `verified_by` object or `null`.
- **SC → could this be enforced off-the-shelf:** `graph-index.json` → `external_automatable_refs.by_sc["1.1.1"]` → the list of axe-core rules, or `[]`.
- Each rule carries `sources.wcag_url` (Understanding page), `sources.en301549_clause` (EN 301 549 9.x.x.x; 2.2-only SCs flagged pending alignment), and `sources.internal_policy_ref`.

## Notes / future

- EN 301 549 clauses mirror WCAG SC numbering (9.x.x.x); the three WCAG-2.2-only SCs are flagged "pending EN 301 549 alignment to WCAG 2.2."
- `check.type` is the *gradeability* hint (automated / semi-automated / manual) — treat it as intent, `verified_by` as evidence of what we actually enforce, `external_automatable_refs` as evidence of what's possible off-the-shelf.
- As more components are ingested, re-run the generators — the graph stays in sync with the component metas.
- **W3C ACT Rules Format** — checked 2026-07-14, **not ingested**: no structured JSON/CSV/API export found without scraping ~500 individual rule pages (no `act-rules` npm package, no `_data/*.json` in the GitHub repo). Deferred approach logged in `_vendor/_INGEST-NOTES.md`: parse the per-rule markdown frontmatter directly from `github.com/act-rules/act-rules.github.io` rather than scraping the rendered site.
- **Next for the verification/external-refs layer** (not this pass): (1) the token→component join via `tokens/_blast-radius.json` to lift `1.4.3`/`1.4.11` from token to component granularity; (2) decide whether any of the 13 "easy win" SCs are worth actually wiring an axe-core check into the build (this import only catalogs availability, it doesn't adopt anything); (3) the ACT ingest, if it earns its own session.
