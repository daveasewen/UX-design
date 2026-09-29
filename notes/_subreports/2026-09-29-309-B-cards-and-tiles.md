# #309 lane B — the cards and tiles, built

COUNTS: rulings enacted 5 of 6 (s308-D39, D40, D41, D43, D44; D42 stopped) + s308-D34 re-expressed · metas carrying a kind 136 of 136 (+2 alias seats, their owner's kind) · kinds: block 95 · layout 28 · housing 7 · record 5 · part 1 · containedBy lines judged 109 · accepted 104 · real-tree refusals 5 (advisory) · selftest 34 of 34 bites (9 new) · role renamed 1 (chart-panel → chart; 13 metas, 2 readers) · rows closed 4 (W-308ir, is, it, iv) · row noted 1 (W-308iu) · commits 94ba3c73, d84169d3, 92d859e1, 18cdc11b, 4abdb8eb + this report's · pushed no

machinery: 1 instrument (the accepts check inside `_validate_edges.py --check`, 8 classes) / 3 feature (the kinds and `$containers` block; Carousel's `slides` slot; the chart role rename)

Asked: the conductor, #309, on Dave's "go" (20:50 BST). His words: `notes/_lanes/308/DAVE-RULINGS-2026-09-29-1856-cards-and-tiles.md`, rulings s308-D39..D44 in `knowledge/_rulings.json`.

## What landed

1. **Definitions and the five kinds (W-308ir; s308-D39, s308-D44).** `knowledge/_edge_register.json` gains `$containers`: Dave's words verbatim per ruling; the terms card, tile, cell, container, surface and panel; the five kinds (layout, housing, record, block, part), each with what it accepts; the limits; and `tiles` (empty: no component is a tile today — the bento's tiles live only in the dashboard-bento template's markup). "Housing", not "holder". `meta.schema.json` gains `kind` (enum of five), `surface` (ground, border, none), slot `accepts.kind` and `sameKind`. Every non-alias meta carries one `kind`, spliced by text after `category` (`notes/_lanes/309/B/kinds.py`). The two alias seats (limits-meter, progress-bar) take their owner's kind — progress-bar is at the alias fence's 14-key cap.
2. **The accepts check (W-308is; s308-D40).** Folded into `_validate_edges.py --check` (build step 164, already ADVISORY, 0.7 s), so it needed no new step. A line naming a `part`, or a subcomponent of its own parent, is accepted by the parent's part row. Otherwise the parent's kind-bearing slots decide; if it has none, its kind does. Classes: NOT-ACCEPTED, CARD-HOLDS, TOO-MANY, TILE-IN-TILE, MIXED-SLOTS, MISSING, NO-KIND, and LONE-CARD, which warns and never turns the exit red.
3. **Container, surface, panel (W-308it; s308-D41).** Container and panel are defined in the register's terms; no component is named "container". Surface is a meta property, and Cards carries `surface: border`. The role `chart-panel` is now `chart` in `roles.json` (`$renamedFrom`; the definition's "in a panel" is kept in `$definitionBefore`). The rename reaches 12 chart metas (provides and providesRole), legend's `with` slug, `_compose_slice.py` and `_validate_roles_resolve.py`. History prose (the sparkline `$provides` note, its `when` string, a context id) is left as it was.
4. **Metric (W-308iu; s308-D42) — STOPPED on the probe, as the brief ordered.** See the blast radius below.
5. **The four limits (W-308iv; s308-D43).** CARD-HOLDS, TOO-MANY with TILE-IN-TILE, and MIXED-SLOTS refuse; LONE-CARD warns. Each was driven red once (selftest bites 27–34).
6. **s308-D34, re-expressed.** Carousel gains a `slides` slot: it accepts kind record or block, is multiple and has `sameKind`. With Cards declaring `record`, the check derives "a carousel holds cards" (the line is accepted through `slides`, bite 26), and the reverse is refused as CARD-HOLDS. The containedBy line from Cards' livesInside stays as data; no pair is authored.

## The seam (one level deep)

- **Mutant:** s308-D34's removed line (a Carousel inside Cards) was put back in carousel.meta.json. `--check` refused it once, by name: `CARD-HOLDS component:carousel → component:cards` (CARD-HOLDS 3 → 4). The file was then restored. Receipt: `notes/_lanes/309/B/seam-mutant.txt`.
- **Control:** on the real tree 104 of 109 lines are accepted and D34's pair is derived (`notes/_lanes/309/B/seam-control.txt`). ⚠ The control is NOT clean. There are 5 advisory refusals, and all come from one judgement call of mine:
  - tabs, accordion and popover are housings, because each frames one thing or one sequence with its own behaviour (s308-D44's definition);
  - so tabs→Cards, accordion→Cards and popover→Cards refuse as CARD-HOLDS;
  - and popover→table and popover→summary refuse as NOT-ACCEPTED.
  **Dave's call:** either those three are blocks, or a card should not hold them. I did not bend the kinds to make the tree pass.

## Piece 4 — blast radius (stopped, not argued)

Merging the stat card and the KPI tile into one block, Metric, is not a metas-only change:
- `knowledge/canon/canon.css` carries 193 mentions (`.cn-kpi-tile` 134, `.kpi-tile` 35, `.cn-stat-card` 25, `.stat-card` 20). canon.css is pinned by the 27 chart receipts.
- 11 snippets use the classes: Stat-card, Kpi-tile, Stats-band-lockup, Hero-variants, and seven templates, among them Dashboard, Dashboard-bento, Detail and Report. 26 snippets name them.
- Generated pages: `showroom/stat-card.html`, `showroom/kpi-tile.html`, the showroom index and a foundations page.
- Also affected: 21 metas that mention them, the headline-metric providers in `roles.json`, 11 `_render` scripts, the legacy theme overrides, and 38 files in the designer pack.

The row's close condition asks for "a render with and without the trend". That means a Metric snippet, and so a canon regeneration. Even the lightest form (a Metric meta with the two old metas as alias seats, markup untouched) moves the specs into a new meta under the alias fence and regenerates the two showroom pages and the pack manifest. That is Dave's scale question from #308.

## Owed

- **The explorer was not rebuilt.** `_build_kg_explorer.py` needs more than 175 s of CPU at the seat, so it dies at the shell cap twice. A cloud build was refused (the repo cannot leave the seat). `notes/_KG-EXPLORER.html` still names `role:chart-panel` once. The graph the checks read is live and correct. The page needs one rebuild wherever a longer run is possible.
- A 95 MB archive, `outputs/309/B/kn.tgz` (ignored), is left from that attempt. Deleting is off.
- W-308iw (container types) is untouched; it is Dave's.

## Verification

- `_validate_edges`: `--check` shows ends 11,583 of 11,583 and shape 0; accepts as above. `--coverage` OK. `--selftest` 34 of 34.
- `_validate_kg` OK, including idempotency. `gen_kg_edges` leaves the metas byte-identical. `gen_kg_sources --check` in sync.
- `_build_integrity`: schema valid 137 of 137. A planted `kind: "holder"` and a slot `kind: ["tile"]` are both refused by the schema.
- `_validate_roles_resolve` PASS, selftest PASS. `_compose_slice --selftest`: the same six pre-existing reds (46, 57, 60, 62, 71, 73).
- `gen_showroom --check` OK. `gen_dashboard --check` OK.
- Memento index rebuilt and current; graph mention map current.
- `_wrap_regen --checks-only`: `_gen_titles` refuses until the wrap, as expected. `_gen_chain --check` fails at the seat on the tiktoken estimate fallback, which is the environment, not this lane.
