# ROLES DRIFT — `roles.json` vs the metas (#270 lane 1, measured 2026-09-14)

Every number here came from a script run against the working tree today. Corpus = the **137**
non-EXAMPLE metas under `knowledge/components/`. Nothing in this file is a ruling.

## The headline

| | roles.json | the metas |
|---|---|---|
| roles | 12 | 8 carry at least one provider |
| component→role memberships | **108** | **24** |
| memberships with a `when` predicate | 81 of 108 (75%) | 24 of 24 — but only 26 metas carry `when` at all |

**The metas are the ruled canon (s251-D12, s254-D2 item 3) and they carry 22% of the membership
roles.json claims.** The generator reads the metas, as the handoff directs, so the graph lands 24
`providesRole` edges — not 108. That gap is the finding, not a generator bug.

All 108 roles.json provider slugs **do** have a meta file (0 dangling slugs — the cross-check is
sound about *what exists*). **84 of those 108 metas simply carry no `provides` key.**

## Roles with ZERO providers in the metas (4 of 12)

`feedback` · `input` · `overlay` · `record-list`

roles.json gives them 11 / 27 / 7 / 8 providers respectively — 53 of the 108 entries, half the
membership, invisible to the graph. `input` is also the one role where **every** roles.json
provider carries `when: null` (it alone accounts for all 27 of the 27 null-`when` entries).

## Roles in the metas that are absent from roles.json

**None.** No meta invents a role. The drift is one-directional: the canon is thin, not wrong.

## Per-role, roles.json membership vs meta membership

| role | roles.json | metas | in metas |
|---|---|---|---|
| headline-metric | 4 | 4 | Chart-bullet · kpi-tile · runway-bar · stat-card |
| chart-panel | 16 | 16 | the 16 chart metas |
| status-surface | 4 | 2 | status-indicator · summary |
| wayfinding | 8 | 2 | breadcrumbs · navigations |
| action | 8 | 1 | button |
| arrangement | 8 | 1 | layout-utilities |
| page-frame | 7 | 1 | app-shell-top-nav |
| page-title | 4 | 1 | headers |
| feedback | 11 | 0 | — |
| input | 27 | 0 | — |
| overlay | 7 | 0 | — |
| record-list | 8 | 0 | — |

*(headline-metric and chart-panel are the only roles where the two homes agree exactly.)*

## `when` coverage — the #269 figure re-measured

- **roles.json: 81 of 108 provider entries carry a non-null `when`.** The #269 proposal page's
  81/108 **reproduces exactly**. (Lane A's original 108/108 claim stays wrong.)
- **Metas: 26 of 137 carry a top-level `when`**, and all 26 split on an em-dash, so all 26 carry a
  prose beats/yields half (s253-D1). The other 111 metas carry no gate at all.
- The 26 `when`-carrying metas are the same 26 that carry `answers` and `shape`; 24 of them carry
  `provides`. The two that carry the DESK address without a role are **`chart-sparkline`**
  (answers change-over-time; its own prose says it is "normally a complement of headline-metric
  rather than a chart-panel in its own right") and **`legend`** (answers what-is-this). Both are
  declared gaps, not generator misses.

## `intent` vs `answers` (the chart metas' two fields)

15 metas carry the legacy chart `intent` field. **All 15 equal their `answers` value** — zero drift.
The resolver's equality assertion holds today; `answersIntent` is derived from `answers` only, so
`intent` stays a legacy field with no second edge.

## `yieldsTo` — why 37, not lane B's 69

Lane B measured 69 pairs across 26 components by substring-matching all 137 component stems against
the **whole** `when` string. That count includes (a) the gate half, (b) names introduced by `beats`,
which is the sibling's fact and not this meta's edge, and (c) repeated mentions. This lane parses
only the prose half, only the `yields to` segments, and de-duplicates per meta: **35 resolved pairs
across 22 components, plus 2 anaphoric ref:null entries = 37 edges across 23 components.** Both
numbers are reproducible; they are answers to different questions, and the narrower one is the one
that can become an edge without guessing.

## The two unresolved edges (ref:null + $note, never invented)

| meta | prose | why null |
|---|---|---|
| `Chart-boxplot.meta.json` | "yields to **it** when variables=1 and the bin shape is the claim" | anaphora — the sibling (Chart-histogram) is named only in the preceding `beats` clause |
| `Chart-bullet.meta.json` | "yields to **both** when no target exists" | anaphora — "both" = stat-card and kpi-tile, named in the preceding `beats` clause |

Resolving these is a **prose fix in the two metas** (name the sibling), not a generator change.
Dave's-eye, not a lane's.

## Commands

```
python3 knowledge/gen_kg_roles_desk.py                # the dry run these numbers come from
python3 - <<'EOF'   # the drift table
import json,glob,collections
roles=json.load(open('knowledge/roles.json'))['roles']
prov=collections.defaultdict(list)
for f in sorted(glob.glob('knowledge/components/*.meta.json')):
    if 'EXAMPLE-' in f: continue
    d=json.load(open(f))
    if 'provides' in d: prov[d['provides']].append(f.split('/')[-1][:-10])
for r,v in roles.items(): print(r, len(v['providers']), len(prov.get(r,[])))
EOF
```
