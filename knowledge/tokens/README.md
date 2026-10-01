# Tokens

Design tokens in **DTCG** JSON (W3C Design Tokens Community Group format), each
with an **intent description** ("when to use"). Tokens are load-bearing in an
agentic system — the agent reasons in token intent, not raw values.

> **⚠️ Open token gaps & wiring issues:** see [`_manifests/_DESIGN-SYSTEM-GAPS.md`](_manifests/_DESIGN-SYSTEM-GAPS.md) — the prioritised list (P1–P5) of missing tokens (subtle-surface family, `rag/neutral-tint`), namespace questions (`interactive/on-light/*`), and components wired to the wrong tokens (Tabs, `color/primary` primitive leaks), distilled from the full component-ingest sweep. Per-token rebinds are in `_manifests/depricate-replacement-map.json`; per-page findings in `_INGEST-NOTES.md`.

## Rules

- Name by **intent, not implementation**: `color.action.primary`, `emphasis`, `subtle` — not `blue-1`, `primary`, `tertiary`.
- Every token has a one-line "when to use" description.
- Components bind tokens by intent (see `knowledge/components/meta.schema.json` → `tokens`).

## Source

Populated on the agency machine from the real Figma variables (via Dev Mode MCP)
and the React library's token source. The GTB brand tokens (red `#DB0011`, the
grey ramp, the 8px spacing scale, the type scale) are the first profile — see the
GTB brand system for the canonical values and their WCAG notes.

## Example (DTCG shape)

```json
{
  "color": {
    "action": {
      "primary": { "$value": "#DB0011", "$type": "color", "$description": "Primary CTA / single decisive action. Accent only — never a page background." }
    },
    "text": {
      "default": { "$value": "#000000", "$type": "color", "$description": "Default body and heading colour. When in doubt, use black." },
      "subtle": { "$value": "#767676", "$type": "color", "$description": "Minimum safe text colour on white (4.48:1). Secondary nav, footer." }
    }
  }
}
```

## DTCG 2025.10 — the stable format (s311-D8, #312)

Since s311-D8 the ten base files here are W3C DTCG **2025.10**, not near it. What that means
on disk: an alias is the token's `$value` as a `{group.token}` reference (`"{color.neutral.15}"`);
the dark value of a token lives in `modes/dark/<file>.json`, bound by the Resolver Module
document `apollo.resolver.json` (set `base` = the ten files, modifier `color-scheme` = light |
dark); a dimension or duration is a value object (`{"value": 16, "unit": "px"}`); a cubicBezier
is `[x1, y1, x2, y2]`; and every Apollo annotation (`note`, `contrast`, `confidence`, `label`,
`darkNote`, `webStack`, `metrics`, a kept `alias` whose target disagrees with the stored hex)
lives under `$extensions.apollo`. `com.apollo.sds` (s141-D1 (B), s217-D4) and `apollo.state`
(ADR-0009) are the older vendor keys and are untouched.

The generator is `gen_dtcg.py` (dry run by default, `--write` to land, `--receipt DIR` to compare
the inverse against pre-s311 files). Readers do not walk this shape yet: they read the pre-s311
view through `knowledge/_dtcg_load.load_legacy(path)`, the one read-site seam (same idea as
`_dtcg_units.py`). `knowledge/_validate_tokens_dtcg.py` proves on every build that the
canon.css spine and all 137 snippet theme blocks re-render byte-equal and that every moved key
comes back from `$extensions`. Not moved yet: the theme override sets under `themes/` (owed as
a `theme` modifier of the resolver) and the Figma `scale-1/2/3/1-200` leaves (owed as a `scale`
modifier); colours stay hex strings.
