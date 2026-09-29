# #309 lane C — the two rulings, the reclass, Metric built properly, the explorer

COUNTS: rulings inscribed 2 (s309-D1, s309-D2; store 834 → 836) · stamped enacted 3 (s309-D1 at daf855ac; s308-D42 and s309-D2 at 879f9aae) · metas reclassed 3 (tabs, accordion, popover → block) · accepts check real-tree refusals 5 → 0 (110 of 110 containedBy lines accepted) · new meta 1 (metric) · alias seats 2 (stat-card, kpi-tile) · snippets renamed 1 (Kpi-tile → Metric) · canon blocks added 1 (.cn-metric) + 1 generated alias (.cn-kpi-tile, byte-identical to before but for its header line) · chart receipts re-driven 27 of 27 green (13 pages, 0 errors, no measurement moved) · explorer v1.34 → v1.35 · rows closed 1 (W-308iu) · rows noted 1 (W-308is) · commits 4b64f0e8, daf855ac, 879f9aae, ccb917c4 + this report's · pushed no

machinery: 1 instrument (the coverage gate reads an alias seat as drawn by its owner) / 3 feature (Metric, the one block; the generated scope alias in gen_canon_components.py + gen_theme_cascade.py; the kind on the explorer's component nodes)

Asked: the conductor, #309, on Dave's "1. good" / "2. go" (chat, 21:37 BST, `notes/_lanes/309/DAVE-WORDS-2026-09-29-2137.md`). Brief: `notes/_lanes/309/C/BRIEF.md`.

## 1. The two rulings (4b64f0e8)

s309-D1 and s309-D2 through `_inscribe_ruling.py` (dry run, then write; reconstruction proof passed both times). Lane I's shape: `ruled` opens with the answer in capitals; his words verbatim ("good", "go"), said to be given **in chat**; the conductor's two calls verbatim from the words file; `says` = chat #309 21:37 BST + the words file; `governs` = W-308is and the three metas (D1), W-308iu (D2), + `knowledge/_state.json`; `evidence` = the chat, the words file, lane B's report. Entries: `notes/_lanes/309/C/entries/`.

## 2. Tabs, accordion and popover are blocks (daf855ac)

The three metas take kind `block`; the register's `$assigned` note records the ruling by addition. `_validate_edges.py --check`: **109 of 109 lines accepted, by class none** (lane B's control had 5 refusals) — `notes/_lanes/309/C/seam-control.txt`. After Metric landed the tree reads 110 of 110 (Metric's containedBy Summary). `--selftest` 34 of 34. s309-D1 stamped enacted at daf855ac.

## 3. Metric (879f9aae sources, ccb917c4 generated)

**The one block.** `snippets/Kpi-tile.reference.html` became `snippets/Metric.reference.html` (git mv). The KPI tile was the superset (the stat card's label · value · delta · period, plus the spark and target slots, four states and two affordance rivals), so it is the one reference; its class and symbol vocabulary is renamed `kpi-tile` → `metric`, `kpi-*` → `metric-*`, and nothing in the drawing moved. The trend is the optional `.metric-spark` slot. `knowledge/components/metric.meta.json` holds the one spec (kind block, provides headline-metric, priority 60, the stat card's relationships and group count folded in; `$merged` says what came from where). `roles.json`: headline-metric is provided by `metric`; the old two provider lines are kept verbatim in `$mergedProviders`.

**The old names, kept as aliases.**
- Metas: `stat-card.meta.json` (reading: without trend) and `kpi-tile.meta.json` (reading: with trend) are s210-D5 alias seats, `aliasOf component:metric`, 11 keys each, no spec. Both resolve (`notes/_lanes/309/C/alias-resolve.txt`); `_compose_slice` hands the headline-metric role to component:metric.
- Canon: `.cn-kpi-tile` is **generated from the Metric snippet** with the rename undone (manifest `scopeAliases`; `gen_canon_components.py` and `gen_theme_cascade.py`). It is byte-identical to HEAD's block except its header line, so the two nio-dash fitness pages (which the compose gate reads) render as they did. The Common guards exist for both scopes.
- `.cn-stat-card`: **`Stat-card.reference.html` is kept byte-untouched.** Its markup differs from Metric's (triangle arrow on the FILL seat, auto-fill board), and three pages are built on it: the #227 banking demo (`dashboards/international-banking-dashboard.canon.html`, measured by `_validate_geometry.py` and `_validate_own_size.py`), the provenance-receipt tests, and the progress dashboard. Moving them onto Metric's markup moves their arrow to the ink seat — a look change that is Dave's to see. Until then canon keeps `.cn-stat-card` and the showroom its page. This is declared in the stat-card alias's `$snippetDisposition`.

**Canon is additive.** Against HEAD, canon.css loses 2 lines (the Kpi-tile header line; the bento stop line, now `:where(.cn-metric *, .cn-kpi-tile *)`) and gains the `.cn-metric` block and its theme projections. No other component's CSS moved.

**The 27 chart receipts.** Re-driven at the seat through `outputs/308/drive_seat.py` (bar.html alone, then the other 12 pages in one call): 0 page errors, every mark, row, dv-004 and contrast figure identical — only the source hashes moved. `_drive_chart_engine.py --check`: all 27 FRESH. `_validate_dataviz.py`: passed, 15 surfaces. Receipt: `notes/_lanes/309/C/receipts-redriven.txt`.

**The close condition's render.** `notes/_lanes/309/C/metric-with-without-trend.png` (1440 px; page `metric-with-without-trend.html`, driver `render_metric.py`): the same Metric with its trend slot filled and left out, light and dark. The markup is Metric's own; every style comes from canon (`.cn-metric` measured: 16px padding, border/subtle, ink-seat arrow #137F3C light / #66CC8D dark; 155px with the trend, 103px without). **Dave's eye is owed on it.**

W-308iu closed: its condition — one block, Metric, trend optional, old slugs as aliases, shown by its meta, a render with and without the trend, the aliases resolving — is met.

**Designer pack.** `designer-skills-v2/` is not rebuilt: its metas do not carry lane B's kinds either, so it is a frozen release, and the pack manifest (`_release/_pack_manifest.json`, cut at 0ef30746) still names Kpi-tile. Re-cutting is Dave's (s219-D4(2)); `_gate_release_audit.py --check` passes, `--drift` is the standing advisory.

## 4. The explorer (this commit)

`notes/_KG-EXPLORER.html` rebuilt at v1.35: `role:chart-panel` 0 (was 1), `role:chart` present, component:metric present, and each component node now carries its kind (block 98 · layout 28 · record 5 · housing 4 · part 1), shown beside the category in the inspector (a one-line builder change and a one-span template change). The builder runs past the shell cap in one call, so `notes/_lanes/309/C/kg_explorer_chunked.py` runs it unchanged with its slow pure functions (the three force layouts, the extra-family placement, the strata/floors/orbits/shells passes) cached on disk; a run the cap kills resumes. Proof that the cache is honest: the 110 s placement recomputed fresh equals the cached result exactly.

## Gates (after, against a baseline taken at the start)

- `_build_survey.py` non-mutating, all five ranges: the same verdicts as the baseline — [11] assertions selftest FAIL (environment, pre-existing), [13]/[127] time out, [126]/[131] red only from the survey's own verdict-log append; everything else passes. The verdict log was restored from HEAD after each run.
- Run by hand (mutating form): coverage, compose, snippets, radius, descender-clip, a11y, icons, integrity (138/138 schema), binds ratchet/resolve, token tiers/forks, DTCG, roles resolve, property-resolves --strict, dataviz vars, KG, edges --check/--coverage/--selftest, gen_kg_sources/gen_kg_tokens (landed under s305-D26 / s277-D12), geometry --build and own-size --build (advisory counts as before), state-contrast on Metric, the bento template and Stat card (rc 0). `_compose_slice --selftest`: the same six pre-existing reds (46, 57, 60, 62, 71, 73).
- Not run whole: `_validate_state_contrast.py` over every snippet needs more than 165 s at the seat; `_validate_hit_area.py --all` cannot find its browser at the seat (COULD-NOT-ASK). CI runs both.
- Stale-at-HEAD generated reports I did not own (`_XREF-INDEX`, `_consult-index`, `_SCREEN-GATE`, `_ADVISORY-SIGNALS`, `_STATE-CONTRAST-AUDIT`) were restored from HEAD rather than committed. `_rule_nodes.json`'s one flaggedBy line from the renamed snippet was re-pointed by hand (gen_kg_rules.py stays unrun: it would drop the hand-authored restsOn block).

## Open

- **Stat card's retirement** — moving the banking demo, the progress dashboard and the receipt tests onto Metric's markup, then retiring `Stat-card.reference.html` and `showroom/stat-card.html`. Dave's to see (the arrow moves to the ink seat).
- **Dave's eye on the with/without-trend render.**
- W-308iw (container types) untouched; it is Dave's.
