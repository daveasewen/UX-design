# Fork-ban gate — `_validate_token_forks.py`

Enacts **s136-D1 clause D**: *"the three axes are the only sanctioned variation; anything off-axis is
a fork and a gate failure."* Built #139 (2026-08-09). **MEASURED, NOT FIXED** — no fork found here has
been migrated; every one awaits Dave.

## What counts as a fork

The sanctioned axes as they exist in the live cascade:

| axis | carrier in CSS | status |
|---|---|---|
| THEME | `[data-apollo-theme="legacy"\|"console"\|"supercharge"]`, absent = mono | sanctioned — Dave's standing four-theme requirement (`ds-035`, #108-D3) |
| MODE | `[data-theme="light"\|"dark"]` (+ `@media`) | sanctioned |
| anything else | `.cn-*` component scope, `.is-*`, bare classes | **off-axis** |

**FORK = one property NAME resolving to two or more different FINAL values inside a single
(theme, mode).** That is the `--pri-hover` class from #108: *a token NAME is not an ADDRESS.*
Divergence carried by theme or mode is `BENIGN_THEME_AXIS` / `BENIGN_MODE_AXIS` — the feature working.

## It parses, it does not grep

No gate may match names with a regex and call that a measurement
(`no-gate-parses-the-artefact`). This one strips comments preserving line numbers, walks the sheet
character by character with a brace-depth selector stack (so `@media`/`@supports`/`@container` carry
context), splits selector lists, classifies each selector into `(theme, mode, scope)`, then
**resolves `var()` chains the way the browser does** — specificity ladder
`(theme,mode,scope) → (theme,any,scope) → (theme,mode,ROOT) → (theme,any,ROOT) → (mono,…)`, with
cycle detection and a depth cap. Comparison is on FINAL RESOLVED VALUES, so `var(--brand)` and
`#DB0011` compare equal. An unresolvable chain is reported `UNRESOLVED(...)` and is never treated as
equal to anything.

## Glob, and why only that wide

`knowledge/canon/*.css` (canon.css + type.css). This is the only artefact where two declarations of
one name sit in the same document and therefore actually compete. The rule is only as wide as the
glob (`gate-glob-scope-rule`).

- `designer-skills-v1/`, `designer-skills-v2/` — RELEASE PACKS, frozen, deliberately out.
- `knowledge/snippets/*.reference.html` — each is its OWN document. A snippet declaration does not
  compete with canon's unless the snippet links `canon.css`, and #107 measured **zero** that do. They
  are audited only under `--collisions` and reported as CROSS_DOCUMENT, never as an in-cascade fork.

## Ledger

`knowledge/_TOKEN-FORK-LEDGER.json` is the #139 BASELINE of forks that existed before the gate did.
**An entry is not a sanction and not a fix.** Baseline mode (default) fails on forks not in the
ledger; `--strict` fails on all 42. No script may add to the ledger.

## Running it

```
python3 knowledge/_validate_token_forks.py            # baseline gate
python3 knowledge/_validate_token_forks.py --strict   # fail on the 42 too
python3 knowledge/_validate_token_forks.py --selftest # two in-memory bites
python3 knowledge/_validate_token_forks.py --json reviews/…json
python3 knowledge/_validate_token_forks.py --collisions knowledge/snippets/*.reference.html
```

Exit 0 clean · 1 forks · 2 the gate itself failed (loud and named).

## ⛔ CONSUMER STATUS — IT DOES NOT RUN YET

`_validate_wiring.py` names it an ORPHAN: it has no `STEPS` entry in `_build_all.py` and no named
exemption. **A gate that does not run cannot fail.** Wiring is a one-line `STEPS` addition plus the
selftest line, and is the conductor's to make — not made in this lane.

`_validate_wiring.py` reports the SAME orphan verdict for `_validate_kg.py` (the #133 fifth-medium
gate), which has been unwired since it was built. Separate finding, not fixed here.
