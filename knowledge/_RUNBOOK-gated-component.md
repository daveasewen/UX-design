# Runbook — build a gated component

The repeatable procedure for turning a component meta into a **gated reference snippet**
(`snippets/<Name>.reference.html`). Written 2026-06-20 to capture the method (it had lived only
in-session). Trigger: a component needs a canonical, token-faithful, build-verified implementation.

## Steps

1. **Read the meta** (`components/<name>.meta.json`) — note its `tokens` bindings, `accessibility`
   (relatedSC, roles, focus), `antiPatterns`, and any `tokenValidation` deprecated bindings.
2. **Resolve token values** for every binding, **light AND dark**, from `tokens/semantic-colour.json`
   (and `colour.json` for primitives). Watch for:
   - **Deprecated bindings** → rebind to the live semantic token; record the rebind as a meta `$finding`.
   - **Primitive bindings** (e.g. `color/primary`) → prefer the semantic equivalent (`primary/background/default`).
   - **Inverting surfaces** (secondary/selected/checked fills that flip light↔dark) → label with
     `text/on-inverse` (#FFF light / #333 dark), not flat `text/reverse`.
   - **Elevation** → shadow in light (`elevation/functional`), grey outline in dark (`elevation/border`).
3. **Check contrast before building** — run pairs through `_contrast_utils.contrast_ratio`. Anything
   that fails (e.g. yellow `rag/warning` on white, red error text on the black page) is a **finding**:
   carry meaning another way (label/icon/shape) and don't declare it as a gated pair.
4. **Author the snippet** — single self-contained HTML, both themes via `[data-theme]` + a toggle,
   CSS vars = the resolved token values, real semantics/ARIA, `:focus-visible` for interactive parts,
   standard-ease motion only (richer motion is exploration, not canon). Square corners (angular rule)
   except Badge + Avatar (round).
5. **Embed the `#token-manifest`** JSON: `vars` (CSS var → token path), `contrastPairs`
   (fg/bg/context — only pairs that PASS), `requiredAria`. This manifest IS the proof-of-done.
6. **Gate it:** `python3 knowledge/_validate_snippets.py` then `python3 knowledge/_build_all.py`.
   Fix until green: declared values must match the store (light+dark), ARIA present, contrast passes,
   a real focus indicator exists (interactive only).
7. **Record findings** in the meta (`$finding` / `$darkDecision` / `$rebind`) — the rebinds, contrast
   caveats, and any defect surfaced. If a real **design decision** is needed (layout/structure not in
   canon), build a sensible baseline and **flag for review** rather than inventing canon.

## Invariants (don't violate)
- Colours are resolved **semantic tokens**, never invented hexes (exception: a flagged `review`-tagged
  proposal, kept local/annotated).
- The build must end **green** (6 gates: contrast ×2, dark-surface flatness, snippet, a11y, coverage, integrity).
  A new snippet must carry a `prefers-reduced-motion` block if it animates (a11y gate) and a meta whose
  `name` matches its manifest `component` (coverage gate).
- Motion stays standard-ease; divergent motion lives in `_fitness-test/` per `_PROMOTION-QUEUE.md`.

## Companion
`_RUNBOOK-reconcile-dark-tokens.md` (TODO) — fixing a token group that's flat/wrong in dark.
See `README.md` for the gate definitions and `_NEXT-SESSION.md` for the broader backlog.
