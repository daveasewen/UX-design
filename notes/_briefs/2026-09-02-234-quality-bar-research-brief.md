# #234 — QUALITY-BAR RESEARCH: three strands, working back from the goal

*Written 2026-09-02 by the Fable conductor. Three Opus research subs, one strand each. Reports file at `notes/_subreports/2026-09-02-234-r{A,B,C}-<slug>.md` per `s218-D7`; chat gets a STUB.*

## THE GOAL (ruled `s234-D2`, Dave's words)

> "the goal is to create a quality output ranked against solid UI/UX standards, A11y and code standards that is ready to hand to a dev for the wiring" — and "we need to solve the bento and behavior work as part of it."

Extends `s230-D1` (the demo goal: built from canon, bento-first or asks, snippet markup with nothing invented, grill-me fires). **Pass condition: a developer takes the page straight to wiring — nothing needs redesigning, only connecting.**

## WHAT THIS IS FOR

The v1.0.5 cold test (#233) found ONE class: the pack has NO BEHAVIOUR CONTRACT. Agents authored their own dropdown JS instead of the snippet's `<script>`; the line chart shipped without its engine (JS-off fallback); bento was grouped by taste. One level up, Dave named the two missing layers: the designer's **composition rules** (grouping is the example) and a **contract** where retrieval is exact and components flex ONLY through their own props/variants/slots. The meta files already carry the flex (135/137 `props`, 124 `variants`, 34 `slots`, 20 `behaviour`) — the pack never tells the agent to use it.

This research feeds the v1.0.6 brief (`W-338`). It is RESEARCH + ANALYSE (six-beat ladder `s63-D1`) — nothing is built, nothing is ruled.

## GROUND IN THE REPO FIRST (each sub, ~10 min, before any web search)

Read: `apollo-spider/cold-start/DESIGN-CONTRACT.md` · `apollo-spider/skills/generate-from-canon/SKILL.md` · `apollo-spider/skills/check-with-gates/SKILL.md` · three meta files of your choosing from `knowledge/components/*.meta.json` (one component, one chart, one template — e.g. `dropdown.meta.json`, `chart-line.meta.json`, `template-dashboard-bento.meta.json`) · `notes/_briefs/2026-09-01-233-delegated-wrap-brief.md` (the finding set). Do NOT read `GOOD-MORNING.md`.

## THE THREE STRANDS

**rA — THE STANDARDS BAR.** What must a hand-off-ready page satisfy? Sources: WCAG 2.2 (AA, and which AAA are cheap), HTML semantic conventions, ARIA Authoring Practices, dev-handoff conventions mature systems publish (GOV.UK Design System, IBM Carbon, Atlassian, Shopify Polaris, USWDS, Material). Output: a candidate RUBRIC — each criterion machine-checkable or explicitly "eye only", with the check named. Say which criteria the repo's existing gates already cover (grep `knowledge/_validate_*.py` by name — list them, do not run them) and which are uncovered.

**rB — THE DESIGNER'S COMPOSITION RULES.** What rules do mature systems WRITE DOWN for composing a page or journey — grouping, hierarchy, reading order, density, spacing rhythm, when a page becomes a flow — and what do they leave to taste? Same source set as rA plus Nielsen Norman on grouping/proximity, Gestalt in DS docs, dashboard-specific guidance (Carbon dashboards, Atlassian data patterns, any published bento/card-grid grouping rules). Output: a candidate list of ~10 rules stated as CHECKABLE conditions, each with "what a gate could see" vs "what only Dave's eye sees", and specifically what a WHEN-TO-GROUP rule for a KPI/chart/rail bento would say. Include how row-height/tile-sizing is handled elsewhere (fixed unit vs floor vs auto) — REPORT, do not recommend; Dave has a floated ladder and three renders are owed before any decision.

**rC — THE CONTRACT: exact retrieval + bounded flex.** How do AI-consumable design systems make an agent fetch the exact component and vary it ONLY through declared props/variants/slots — and carry its behaviour with it? Sources: Figma Code Connect, Figma MCP / design-system MCP servers, Storybook/CSF + component manifests, Web Components custom-elements manifest, Carbon/Polaris AI docs, any "design system for agents" writing (2025–26). Output: (1) the shapes others use for a retrieval RECEIPT / provenance record; (2) how behaviour (JS) travels with markup in those systems; (3) how "variant, not invention" is enforced — schema, gate, or prompt; (4) what of this maps onto the repo's meta schema as it stands, field by field.

## FILING RULES

- Copy `notes/_subreports/_TEMPLATE.md`; `sub index` = `rA` / `rB` / `rC`; `brief:` = this file.
- Every finding carries its probe: URL + the quoted line, or repo path + line. **A finding with no probe is an opinion — label it as one.**
- ADR-0016 vocabulary: `CLAIMED` / `UNPROVEN` with the price of proving.
- Close with a section **"WHAT APPLIES TO A FACTORY"** — a design-system factory that generates pages, not a codebase — ≤ 12 lines, plain prose.
- Chat stub only: verdict + COUNTS line + file path + token spend + REPLAY-THESE (≤ 5 items).

## DO NOT RULE

No ruling, no decision, no recommendation phrased as settled. Specifically not: the bento row-height model · the v1.0.6 shape · which gate to build first · any change to `DESIGN-CONTRACT.md`, `SKILL.md`, any meta file, `_rulings.json`, `_state.json`. **Read-only in the repo except your own report and its `assets/` folder.** No git operations.

## PITFALLS (consequences replayed, `#165`)

- Reading `GOOD-MORNING.md` costs ~41K tape for nothing you need. Don't.
- A rule that sounds checkable but isn't ("visual balance") wastes the next lane — mark it "eye only".
- Quoting a source's marketing page as its standard. Quote the spec/doc page.
- Recommending. Dave rules; the conductor puts options in prose with renders. Your job ends at "here is what exists, here is what maps."
- Evidence in `/tmp` evaporates at the call boundary. Evidence beside the report or not at all.
