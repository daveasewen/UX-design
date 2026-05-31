# Prompt 2 — Ingest the real design system into the knowledge layer

Paste this after the agent is oriented (Prompt 1). Fill in the three blanks first.

---

We are now building the knowledge layer (canon) from real company assets. Follow
`harness/state/canon.md` and `knowledge/README.md`. Conform exactly to the schemas
already in the repo — do not invent new fields.

Inputs:
- Published design-standards site: **<PASTE URL>**
- React component library: **<PASTE local path or Git URL>**
- Figma library: connected via the Figma Dev Mode MCP. Use it for variables,
  tokens, components, variants, and Code Connect mappings.

Work in small batches, and stop for my review between batches.

**Batch 1 — one component (the button), end to end:**
1. Read the button from Figma (MCP) and from the React library source.
2. Write `knowledge/components/button.meta.json` conforming to
   `knowledge/components/meta.schema.json`. Fill props, variants, tokens,
   relationships, accessibility, and — most important — `antiPatterns` and
   `provenance` (real Figma node id + code path).
3. Validate it against the schema and show me the file.

Then **pause.** I will correct the anti-patterns and any generic content before
you continue — those are the rules only I know.

**Batch 2 (after my OK) — tokens + compliance:**
- Populate `knowledge/tokens/` from the real Figma variables (DTCG shape, with
  intent descriptions).
- Add the most relevant accessibility rules to `knowledge/compliance/` using
  `rule.schema.json`, each citing the WCAG success criterion and the EN 301 549
  clause. Start with contrast, focus visible, target size, name/role/value.

**Batch 3 (after my OK) — the next 5–10 components**, same pattern as Batch 1.

Rules:
- Name tokens and variables by **intent, not implementation** (`emphasis`,
  `color.action.primary`), and give every token a one-line "when to use".
- Every component record must carry real `provenance`.
- If the source is messy or ambiguous, tell me — don't guess.

Coverage target for today: enough real components to run one real example. Quality
over breadth.
