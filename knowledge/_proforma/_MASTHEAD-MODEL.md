---
title: Masthead — a switchable model (three layers)
source: Synthesised 2026-07-16 with Dave, from a research pass across NN/g, IBM Carbon, Shopify Polaris, USWDS, Material 3
type: pattern-model
status: labels signed off 2026-07-16 (Dave) — Shell + optional footer; recipes named; mode labels provisional pending feedback
captured: 2026-07-16
related: _PROFORMA-RULES.md, _TRANCHE-7-SPEC.md, Tranche-7-interactive.html, ../reviews/NAV-PATTERN-CATALOG-2026-07-15.html, ../reviews/MASTHEAD-MODEL-2026-07-16.html
relations:
  refines: nav-pattern-catalog          # tightens the catalog's GlobalHeader + MegaMenu entries into one model
  informs: masthead-build               # this is the spec the unified .masthead component is built from
  built_as: Masthead-interactive.html   # BUILT 2026-07-16 — data-mode + 5 recipes, all 4 gates green
  governed_by: proforma-rules           # mono / tokenise-everything / CSS-motion / real-icons all still apply
  supersedes: [gheader-as-standalone, mm-masthead-as-standalone]  # the two T7 demos fold into one component
  sibling_layer: shell-template         # Layer 1 (Shell) is a template-tier concern, not the masthead
dossier: ../reviews/MASTHEAD-MODEL-2026-07-16.html
---

# Masthead — a switchable model

The **Global header** and the **content-heavy masthead** are **one pattern**, not two components. What
felt tangled was that **three separate layers** were being decided as one. Untangle them and the
"god-component" risk goes away: the masthead owns only one of the three.

Full reviewable write-up + diagrams: `../reviews/MASTHEAD-MODEL-2026-07-16.html`.

## The three layers (graph nodes)

1. **Shell** *(Layer 1 — the page frame, TEMPLATE-TIER)* — NAME CONFIRMED (Dave: "it's what I've always
   called it"). Which nav regions coexist on the page: masthead + optional side nav / in-page nav /
   breadcrumb / **footer** (the footer is optional and will carry its own **variants** — ties to Tranche-8
   FooterNav). Driven by **IA depth**, NOT by the masthead.
   Precedent: Carbon "UI Shell" (header-only vs header+left-panel by depth), Polaris "Frame".
   → This is a Tranche-8 / template-tier concern. The masthead never knows the side nav exists.
2. **Roles** *(Layer 2 — what each region is FOR)* — labels, not components:
   **global/primary · local/secondary · utility · in-page/contextual · breadcrumb**. (NN/g + Carbon.)
3. **Masthead mode** *(Layer 3 — the ONLY axis the masthead owns)* — how the bar reveals its primary nav.

## Layer 3 — the masthead's own axes

**Reveal mode** = a small closed ladder of increasing IA depth (NOT free parameterisation):

- `minimal` — brand + utility only; nav lives elsewhere. (Polaris Frame.)
- `exposed` — L1 links inline, no panels; shallow ≤~6 one-level IA. (USWDS basic header.)
- `exposed-mega` — L1 inline, each opens a mega; broad + deep. (USWDS mega header — the "exposed header
  that also invokes a mega" Dave wanted.)
- `trigger` — one door opens a panel holding the nav; deepest / most flexible. Carries the modifiers below.

**`trigger` modifiers** (this is where the earlier "extra modes" actually live):

- **prominence**: `primary` (nav is the star) | `index` (deliberately tucked, low-frequency — the
  well-configured dashboard case). **`index` is a SUBSET of `trigger`, not a peer** (Dave) — prominence
  only means something once nav is behind a door.
- **affordance**: `burger` | `menu+search` (combined control opening a search-led panel; common on mobile;
  pairs best with `index`).
- **panel-layout**: `cols` (1 level) · `featured` (+ journeys rail) · `tabbed-vertical` (3 levels:
  L1 tabs → L2 cols → L3 links) · `tabbed-horizontal`. **This sub-axis carries IA depth** — a 3-level
  structure lives here, not in a new top-level mode.

**tuck-by-intent ≠ collapse-by-necessity**: `index` tucks at ALL widths (nav is incidental); the automatic
responsive→drawer collapse happens under EVERY mode at narrow widths (no room). Same drawer, different reason.

## Designer-facing = intent recipes (not raw dials)

Axes are for the machine; **recipes are for the designer** — this is the guardrail against a god-component.

Names kept **simple + descriptive + channel-neutral** (Dave 2026-07-16 — they serve app interfaces AND
public sites; richer *intent-based* naming PARKED for later).

| Recipe | reveal | prominence | affordance | panel | utilities |
|---|---|---|---|---|---|
| App-minimal | minimal | — | — | — | account |
| L1 exposed | exposed | primary | — | — | search + account |
| L1 + mega | exposed-mega | primary | — | tabbed-h | search + account |
| Trigger mega | trigger | primary | burger | featured | account (search in panel) |
| Dashboard-index | trigger | index | menu+search | tabbed (deep) | account (search in panel) |

## Search rule (RULED with Dave 2026-07-16)

- Two **global** searches (bar + panel/mega) is acceptable — in trigger/index modes the bar is stripped,
  so they never compete.
- **Finesse (Dave):** the masthead search ICON DISAPPEARS when the panel/mega search is present/open — so
  two global searches are never shown at once.
- `menu+search` combined affordance folds the two into one door.
- a11y: two search fields = two landmarks → distinct accessible names, or expose only one to the a11y tree.
- **Scope**: settled as "same global" for now. A section-SCOPED panel search (e.g. "Search payments") is a
  legitimate future variant but must be labelled to show the difference. PARKED, not adopted.

## Naming decisions — SIGNED OFF 2026-07-16 (Dave)

- **D1** mode labels: **KEPT** `minimal / exposed / exposed-mega / trigger` — fine for now, open to change
  after user feedback (provisional, not frozen).
- **D2** Layer-1 name: **Shell** (confirmed). + optional **footer** region with variants (see Layer 1 above).
- **D3** recipe names: **RENAMED** simple/descriptive/channel-neutral → `App-minimal · L1 exposed · L1 + mega ·
  Trigger mega · Dashboard-index`. Intent-based naming PARKED for later. (`Trigger mega` = the old
  "content-heavy masthead": trigger + featured panel, no exposed L1.)

## BUILT 2026-07-16 — `Masthead-interactive.html`

One `.masthead` driven by `data-mode` + modifiers, with a **switch row** that reconfigures the single live
instance across all 5 recipes. **Folds in + supersedes** the T7 `gheader` + `mm-masthead` demos. Motion is
CSS-only (mega grid-reveal); the switch row only sets `data-*` (behaviour). Search-finesse works (bar search
icon hides in trigger family, panel carries search). Responsive priority+ → hamburger → focus-trapped modal
drawer. **All 4 pro-forma gates PASS + full `_build_all.py` green**; render-verified all 5 recipes + responsive,
0 console errors. Review copy: `../_review/Masthead-interactive-REVIEW.html`.

## Why it matters

One `.masthead` skeleton reconfiguring across 5 real intents via `data-mode` + a small prop set **is** the
pro-forma "one skeleton, N modes" thesis made visible — now demonstrated live. The component API fell straight
out of the model. This doc is also the first entry in the eventual Swiss-aesthetic HTML component catalog.
