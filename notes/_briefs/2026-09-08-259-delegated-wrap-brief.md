# #259 delegated-wrap brief — cut by the conductor at ~146K real FILL, 5K under the 150,929 advisory

provenance: 259 · 2026-09-08 · conductor Fable · wrap DELEGATED to an Opus sub (the #258 shape). Model of the wrap = `notes/_briefs/2026-09-08-258-delegated-wrap-brief.md` and the runbook `knowledge/_RUNBOOK-capture-ritual.md` — READ BOTH FIRST; this brief is the CONTENT, the runbook is the PROCEDURE.

## Title lines (both go in chat at the end — the conductor relays)
- THIS chat was: `Apollo - #259: the chart engine — six data-driven charts in the library; v1.0.8 cut`
- NEXT chat: `Apollo - #260: the budget ruling, the eight fast-follower charts; v1.0.8 cut`

## What #259 did (session facts — quote, do not embellish)
1. **Opener.** Boot 68,994 real (`_checkin.py`); ceiling breach #256 DISCHARGED by declaration per `s244-D1` in `notes/_GAUGE-LOG.md` (`#### 2026-09-08 #259 — ceiling discharge`); #255 70,127 still red (later breach after it). Dave: *"just run it as you've planned"*.
2. **Premise probe (Opus lane, read-only).** All 14 dataviz types ALREADY exist as components; the gap was a renderer, and `s249-D4` already ruled the shape (engine in the library, dv-behaviour side). Count collision: registry 14 · carry "11 / other five" · rule 18's 78-line green page was NEVER committed (lived in /tmp/r258). Rule 18's `cn-chart-bar` wrapper trap names a wrong source (wrapper is in canon.css, not the snippet).
3. **Ruling `s259-D1` (entry 403), Dave's words verbatim:** *"okay do the 6 types but i want the rest as a fast follower, lets not let these be forgotten"* — six now; scatter, pie, histogram, boxplot, bullet, candlestick, butterfly-h, butterfly-v = FAST FOLLOWER carry.
4. **Engine-core lane A** → `knowledge/canon/dv-render.js` (311 ln, 9,309 code-only B) + `dv-render-bar.js` (4,613 B, column/grouped/stacked/bar) + five stubs; Chart-bar re-pointed; `knowledge/_tests/chart-engine/bar.html` (the receipt rule 18 never had). Drive found a real bug: authored 2px gap rendered 1.90px (fit rounds x and w independently) → GAP 2.2. Report `notes/_subreports/2026-09-08-259-A-engine-core-bar.md`.
5. **Five parallel type lanes B–F** (line 3,616 B · stacked-area 4,248 · donut 3,807 · sparkline 3,235 · combo 5,198), each: partial + snippet drawing from inline DATA + typed `behaviour` meta + committed test page + Playwright drive 8/8 themes×modes, 0 pageerrors, filter changes marks AND table rows, resize moves x, mutants red. Reports `…-259-B-line.md`, `-C-stacked-area.md`, `-D-donut.md`, `-E-sparkline.md`, `-F-combo.md`.
6. **Commits.** Early #259 files were swept under #258's `928139f` (its `git add -A`; receipt `notes/_receipts/2026-09-08-258-postwrap-receipt.md`). The rest: `f6f762a` "during #259 — THE CHART ENGINE". Conductor cleared lane F's first obstacle (registry `declarations` `data-dv-type="line"` on the type partials → `[]`).
7. **Gates at the cut.** GREEN: gen_component_partials --check, gen_canon_components --check, snippets, dataviz-vars, no-hardcode, a11y, compose. RED, DECLARED, RULING-SHAPED: `_validate_behaviour` page budget — Chart-combo 43,518 · Chart-donut 37,787 > 34,816 (`s250-D1`; the core is priced once per member page; priced once per page combo fits with 607 spare); `_validate_dataviz` dv-004 on Chart-donut (gate reads static geometry; driven 2.199px inner). `gen_showroom --check` stale ≈66 (60 pre-existing + 6 chart pages) — NOT regenerated. `_validate_screen.py` NOT run (carry ⑤).
8. **v1.0.8 NOT CUT** — red gates ⇒ a cut would be laundering (#257 lesson). Carries.
9. **Gauge.** Conductor FILL 144,935 real at the last check-in (18 turns → later), seam check-ins at opener, after lane A, after lanes B–F. Subs: A 256,651 · B 208,439 · C 185,108 · D 204,762 · E 202,238 · F 172,010 · probe 108,738 — QUOTA never FILL. Fable bucket 68% used at opener.

## RULING-SHAPED — Dave's, collected from all lanes (put in the ⏱ delta STILL-HIS line; do NOT rule)
- Page budget `s250-D1`: core priced once per page vs raise vs drop dv-legend where the engine draws legends.
- dv-004 / dv-line-006 etc.: gates that parse static geometry are blind to engine-drawn canvases ([[no-gate-parses-the-artefact]] owed twice) — driven receipts as the gate?
- `behaviour.partial` shape: chart-bar names 3, others name 4 (full consumes) — one ruling.
- Sparkline: `s182-D3` ruled rag/*-INK but `--status-*` binds rag/*-GRAPHIC; snippet re-points at `.cn-chart-sparkline` scope; `dv-fit` refused on spark by DV-D02-A.
- Donut: slice cap is 5 (palette) not 6; engine table spine drops DV-D13 percent column; cd2 labels stay baked.
- `stacked-area` missing from `DTYPE_CANON` (silent skip since #95).
- Rule 18: strike or keep as escape hatch now the engine exists; fix its wrong source citation.
- Count: registry 14 vs carry 11 — which wording stands.
- Core requests from lanes (verbatim in their reports): zero-floor clamp escape (`fn.zero===false`), furniture opt-out (`fn.furniture=false`), TOTAL column in writeTable, legend cache invalidation hook, `dvDonutSweep(figure)` re-entry, circle branch in dv-behaviour fit, `data-series-group` always emitted by bar, `series[i].unit`/`sharedScale` minted by combo.
- `_validate_screen.py` clobber (carry ⑤) · the boot-ceiling arm (#255 still red).

## Carries → #260 (add to `_CARRIES.md § residual → #260` by ONE programmatic pass, never re-typed)
① the budget ruling (blocks v1.0.8) · ② the EIGHT fast-follower types (`s259-D1`, Dave's "lets not let these be forgotten") · ③ v1.0.8 cut + sixth cold run · ④ the core requests (one lane) · ⑤ his rulings page (fourth session, store 403) · ⑥ 60+6 stale showroom pages · ⑦ the 51 blank behaviour metas (now 45 — six chart metas typed) · everything from #258's set.

## Declared skips at this wrap (state each with its size)
no `_build_all.py` · no recall plant · `_CARRIES.md` never read whole · `_validate_screen.py` not run · showroom not regenerated · memory: the conductor writes its own hook (D1a scope).

## Procedure
Run the runbook steps in order (1 → 2a…2g → 3 → 4 → 5), regenerate `_CHAIN.md` to a fixed point, `_checkin.py --wrap` will REFUSE on #255 → commit in the #243 form ("after #259 …"). Rebuild `_memento-index.json` LAST. Add BY PATH — another lane may share the tree. Then write `notes/_subreports/2026-09-08-259-W-wrap.md` and return ≤400 words: what landed, both title lines, gate tail, anything you could not do.
