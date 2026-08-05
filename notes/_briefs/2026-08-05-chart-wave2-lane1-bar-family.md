# Wave-2 lane ① — Chart-butterfly-h · Chart-butterfly-v · Chart-histogram (bar-family geometry)

*Cut 2026-08-05 #94 by the conductor. Worker model: **Sonnet** (conductor replays your receipt).
**Read first, in order:** this brief → `snippets/Chart-bar.reference.html` (THE bar-family
pattern — port, don't reinvent; D-Q3 grouped/stacked machinery + sort-toggle idiom live there) →
`snippets/Chart-line.reference.html` (the exemplar's six refinements + state model + a11y
constraint are CANON) → `notes/_receipts/2026-07-24-wave-lane1-bar-scatter.md` →
`_DATAVIZ-DECISIONS.md` DV-D07/08/09 · ADR-0015.*

## Scope

1. **Chart-butterfly-h** (`snippets/Chart-butterfly-h.reference.html` + `components/Chart-butterfly-h.meta.json`)
   — paired horizontal bars, mirrored axis, two series; legend-as-filter/highlight from the bar
   pattern; series fills `data/series/*` tokens (h-bar default = `data/series/3` per DV-D09 — cite it).
2. **Chart-butterfly-v** — same contract rotated; shared meta notes may cross-reference, files stay separate.
3. **Chart-histogram** — single-series column, contiguous bins (no inter-bar gap: derive bin gap
   from the bar geometry, receipt the token you bind); static legend keys (single-series rule).

## Fences

**Yours:** the three new `snippets/*.reference.html` · their `components/*.meta.json` · your
receipt `notes/_receipts/2026-08-05-wave2-lane1-bar-family.md`. **NOT yours:**
`component-types.json` (hand `$members`/hook JSON via receipt) · `dv-behaviour.js` (missing hook
⇒ RECEIPT the need) · `MIGRATED_SNIPPETS`/`CATEGORIES` · spine docs · existing snippets · git.
**ds-020:** copy mark contract + toolbar, NOT the axis/grid CSS; receipt the inherited gap.

## Checklist (the exemplar's, applied)

Type composites from `type.css` only, never raw shorthand (gate-enforced). DataViz gate 0
blocking; parity (chart↔table↔tips↔aria); render-verify ≥2 widths + dark + HC + filtered +
JS-off per `_RUNBOOK-render-verify.md` (if the sandbox kills the browser, declare render-verify
OWED with compensating evidence — the 07-24 precedent); census/radius/coverage green; controls
NEVER dim-only (hollow-swatch off-state recipe, follow exactly). Receipt: what landed, what's
OWED, every serial-file need, named.
