# Knowledge base — Promenaut design-to-code canon

The authoritative, portable knowledge the Promenaut pipeline queries to use the **HSBC Common Toolkit** design system correctly — built from the Figma library ("Gaps and edits" branch, fileKey `Cgbtrmfp15ruNFkIAClpkI`) and the design standards on create.hsbc.

It has two halves: **authored canon** (hand-curated, the source of truth) and **derived views** (generated from the canon, never edited by hand). Everything regenerates and self-validates from one command: `python3 knowledge/_build_all.py`.

## Architecture — five layers, representation per stage

Each kind of knowledge is stored in the representation that suits how it's queried:

| Layer | Representation | Lives in | How the pipeline uses it |
|---|---|---|---|
| **Components** | Component graph — one `*.meta.json` node per component (props, variants, token bindings, relationships, anti-patterns, a11y, token-validation, provenance) | `components/` (32 metas) | Look up a component's contract before generating code; traverse `relationships` edges |
| **Tokens** | DTCG-style store with intent descriptions; semantic tokens carry `light`+`dark` modes | `tokens/` (7 stores) | Resolve a binding to a value; check dark-mode coverage; drive the Sutherland migration |
| **Compliance** | Knowledge graph — rule → component → check → WCAG SC → EN 301 549 clause | `compliance/` (31 rules) | Given a component, list its WCAG 2.2 AA obligations + automatable checks |
| **Guidelines** | RAG over Markdown (brand, voice, patterns, platform, a11y) | `guidelines/` (23 docs) | Retrieve prose guidance at generation time |
| **Live Figma / code** | MCP at runtime — **not stored here** | — | Pull current nodes/variables/code on demand |

create.hsbc is **not** a runtime dependency: its content is captured into `guidelines/` as the RAG layer, and reference URLs in the docs are provenance only.

## Authored canon (source of truth — edit these)

```
components/
  meta.schema.json              # contract for a component node (reconciled to the canon 2026-06-18)
  <component>.meta.json          # 32 component nodes
  _ACCESSIBILITY-CONFORMANCE.md  # WCAG 2.2 AA basis + 2.2-new SC mapping
tokens/
  colour.json semantic-colour.json elevation.json layout.json
  spacing.json typography.json icon-scale.json
  _manifests/                    # depricate→canonical replacement map, Sutherland diffs
  _INGEST-NOTES.md               # per-page ingest findings
  README.md
compliance/
  rule.schema.json               # contract for a rule node
  README.md
guidelines/
  *.md (23)                      # the RAG corpus
  README.md
_CONFIDENCE.md                   # confidence vocabulary: asserted | inferred | review
```

**Runbooks (the methods, written down so they don't live only in-session):**

```
_RUNBOOK-gated-component.md       # turn a meta into a gated reference snippet
_RUNBOOK-reconcile-dark-tokens.md # fix a token group that's flat/wrong in dark
_RUNBOOK-onboard-code-library.md  # map the canon to a NEW code library (hub-and-spoke codeBindings)
```

## Derived views (generated — do not hand-edit)

Run the generator (or `_build_all.py`) instead of editing these:

```
compliance/rules/*.json          # ← _build_compliance_kg.py   (31 rule files)
compliance/graph-index.json      # ← _build_compliance_kg.py   (by_sc + by_component)
tokens/_blast-radius.json        # ← _build_blast_radius.py     (token → components + god-nodes)
_GRAPH-REPORT.md                 # ← _build_blast_radius.py     (health dashboard)
_XREF-INDEX.json / .md           # ← _build_xref_index.py       (per-component hub, all layers)
_REVIEW-QUEUE.json / .md         # ← _build_review_queue.py     (confidence-tagged worklist)
_DARK-MODE-AUDIT.json / .md      # ← _build_dark_mode_audit.py  (primitive-leak report)
_INTEGRITY-REPORT.md             # ← _build_integrity.py        (the CI gate)
```

## Build — one command, dependency-ordered, self-gating

```
python3 knowledge/_build_all.py
```

Runs the ten generators in order (later ones read earlier outputs):

1. **compliance KG** — rules + graph index from each meta's `relatedSC`.
2. **blast-radius + graph report** — token → component reverse index; god-nodes.
3. **cross-reference index** — joins tokens · god-nodes · SCs · guidelines · anti-patterns · deprecated bindings into one hub per component. *(needs 1 + 2)*
4. **review queue** — every non-asserted assertion, tiered (see `_CONFIDENCE.md`).
5. **dark-mode audit** — components binding raw primitives that can't re-theme. *(needs 2)*
6. **text/icon contrast audit** — every text/icon token's dark value tested against the worst-case dark surface it sits on (resolved from the store). **Gates** on any non-allowlisted token below 4.5:1 (text) / 3:1 (icon).
7. **indicator/accent contrast audit** — brand red, RAG, interactive-state tokens tested at 3:1 (1.4.11) against their resolved dark surface. **Gates** on any non-allowlisted failure.
8. **dark-surface flatness gate** — surface/background/border/divider tokens that resolve to a flat `#FFFFFF` in dark (a white block hiding content). **Gates**; intentional inversions are exempt via a per-token `$darkNote` annotation (the reviewable allowlist).
9. **snippet gate** — authored reference snippets in `snippets/` validated against the store: declared token values match (light+dark), required ARIA present, contrast pairs pass, real focus indicator. **Gates** on drift.
10. **integrity lint** — schema-validates every meta, checks SC/rebind/guideline references resolve. **Exits non-zero on any error.**

**Four gates, not one:** the contrast audits (6–7), the dark-surface gate (8), the snippet gate (9) and integrity (10) all run to completion, then the build exits non-zero if any failed. A green build now means *internally consistent, legible in dark mode, surfaces not flat-white, and every authored snippet still matches canon* — closing the gap where the old gate passed a white-on-white component. Allowlists: disabled-state tokens in `_contrast_utils.py`; intentional dark inversions via `$darkNote`; `*/on-light` tokens excluded as light-only.

Always regenerate after editing a meta, a token, or the compliance/guideline maps — the derived views are only as fresh as the last build.

## Multi-hop traversal (start points)

Quickest path is the query harness (joins all indexes live):

```
python3 knowledge/query.py "Tabs"            # full component hub
python3 knowledge/query.py --token text/default   # blast radius
python3 knowledge/query.py --sc 2.4.11       # SC + rule + components
python3 knowledge/query.py --leaks           # dark-mode primitive leaks
python3 knowledge/query.py --list            # all components
```

Or read the indexes directly:

- **Component → everything:** `_XREF-INDEX.json` `components["Modals"]`.
- **Token → components affected:** `tokens/_blast-radius.json` (`ranking` / `by_component`).
- **WCAG SC → components:** `compliance/graph-index.json` `by_sc`.
- **What needs human verification:** `_REVIEW-QUEUE.md` (🔴 review / 🟡 inferred).
- **Dark-mode defects:** `_DARK-MODE-AUDIT.md`.
- **Migration coupling:** components sharing a `god_nodes_touched` entry in the xref move together — rebind/test as a set.

## Conformance basis

Accessibility is graded against **WCAG 2.2 AA** — the bar set by HSBC's digital accessibility framework (Group Digital Experience and Accessibility). See `guidelines/digital-accessibility-standards.md` and `components/_ACCESSIBILITY-CONFORMANCE.md`.

## Parked

The **Sutherland** token migration (Sutherland = the HSBC React library; its tokens become canon) is on hold until its JSON lands (~late June / early July 2026). When it arrives: import as modes → rebind in-use deprecated tokens (worklist in `_REVIEW-QUEUE.md` + `tokens/_manifests/`) → re-verify zero references → delete. The blast-radius, review queue, and dark-mode audit are the safety tooling for that rebind.
