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
