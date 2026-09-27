# #304 F5 — wave-five fixes: the trim narrowed to the charts (root default held back for Dave), session titles count every ruling, the sitting page corrected and its slot filled; fresh-clone survey 152 steps, 0 green→red

provenance: 304 · Sunday 2026-09-27 · seat F5 (Opus 5.5) · mount HEAD `ff382c0b` · work clone `$HOME/f5w` (`git clone --shared` at `ff382c0b`, W5a's 41 + W5c's 5 overlaid from the mount, clone commits `c16a4f30` overlay → `db590601` trim → title fix) · survey clone `$HOME/f5s` (fresh, same method, `e9396b6e` overlay → `9a77abe5` wiring → `ef1eaa31` serial) · stages `$HOME/f5st/{head,w5a,f5}` (candidate 2's three runs restaged per side) · writes on the mount: the 7 tracked files in §1–2, `notes/_lanes/304/W5a/held-back/`, `notes/_lanes/304/W5b/{page.src.html,build.py,shots/}`, `notes/_SITTING-304-tuesday-2026-09-29-v1.html`, `notes/_lanes/304/F5/`, this report · no `git status`, no git writes on the mount, no `_build_all.py`/survey/`--wrap` on the mount, wiring NOT applied to the mount, no Project memory, nothing committed
status: observed — every figure below was printed by a gate, a selftest, the survey, the harness or a browser probe at the seat, receipts under `notes/_lanes/304/F5/`

## THE ANSWER FIRST

1. **Trim, conservative route, done.** canon.css's ROOT leading-trim default is back to HEAD's behaviour (byte-identical rule line); the fix is narrowed to the 14 chart scopes by the generator (`gen_canon_components.chart_restore`: one rule per `Chart-*` scope putting `text-box-trim:none;text-box-edge:auto` back over the root default's exact element set, zero-specificity lower boundary). W5a's 111 bounded copies and its other four fixes are untouched. Own-size on candidate 2's three runs: **82 / 104 / 146 → 0 / 0 / 0** (980 / 900 / 861 parts matched, same as W5a). K3 against HEAD: **0 non-chart text parts moved on 88 pages** (V5's sample: 6,136 elements, 4 themes × light/dark; all 58 `_fitness-test` pages; all 30 cand2 pages). W5a's root version is saved as a one-hunk patch in `notes/_lanes/304/W5a/held-back/` for Dave (sitting call 41c).
2. **W5c title bug fixed.** A session now counts every ruling whose `ruled` starts `#n` with no digit after (the builder's own SESSION_RX reading, the one that draws the `ruledIn` edge) OR whose id starts `s<n>-`, in `gen_kg_titles.py` and the template's `sessionTab`. Six "0 rulings" titles become true (#31 1, #57 1, #76 **7**, #79 1, #81 1, #82 1); #245 goes 10 → 11 (s244-D2's `ruled` begins "#245 RUNS THE REDS FIRST…", and the graph already links it to #245). No session reads "0 rulings" now. Selftest 12/12, bite 12 widened and mutation-tested (the W5c form fails it). Explorer rebuilt: vs the mount's v1.29 bytes, 7 labels + the one template line + the commit stamp move, nothing else.
3. **Sitting page corrected and the slot filled**, rendered at 1440 and 390 and looked at: 0 off-edge, 0 clipped, 0 broken images, 0 page errors; 53 calls unchanged in number and id, 58 decision boxes (55 + 41b, 41c, 41e).
4. **Survey, fresh clone, whole wave-five tree + wiring + serial: all 152 steps.** 137 pass · 9 FAIL · 5 could-not-ask · 1 timeout. **0 green→red against V4 by step name; every red detail block identical to V4's** (`[139]` reads 4 rc/observation mismatch, as V4). `[128]`/`[129]` in one chunk: schematic determinism ✅. The four wired steps ✅. `_build_all.py --selftest` PASS over 152 steps. The survey re-dirtied none of the wave's files.

## 1 · TRIM — chart-only narrowing

**Change (work clone, copied byte-identical to the mount):**
- `knowledge/canon/gen_canon_components.py`: `TRIM_ELEMENTS`, `TRIM_RESTORE_BODY`, `wants_chart_restore(name, style)` (a `Chart-*` snippet carrying no trim copy of its own — all 14 today), `chart_restore(scope)` (selector `:where(.cn-chart-x) :where(<root list>):not(:has(svg))` + `trim_bounded`, so (0,0,1) like the root default and later in the file; any one-class authored rule still beats it; a component nested inside a chart keeps the root's trim). Appended after the chart's own rules in `gen_one`. W5a's `is_trim_scaffold`/`trim_bounded` unchanged.
- `knowledge/canon/canon.css`: the root rule line is HEAD's exactly (the diff HEAD→F5 touches no root selector); W5a's comment replaced by an F5 comment saying why and where the held-back version is (⛔ do not bound without Dave's ruling on call 23). Regenerated: 137 components, 14 restore rules, 111 bounded copies. HEAD→F5 canon.css: 111 copies bounded (W5a) + 14 restores + comments, nothing else.
- `knowledge/_tests/chart-engine/_receipts.json`: 13 receipts hash canon.css, so all 13 re-driven with R3's `drive_shim.py` (two batches). vs W5a's committed-to-be copy: **14 changed leaves = 13 canon.css hashes + the `driven` stamp; 0 measurement values changed.** `--check` 27/27 FRESH.

**Proof (all at the seat, 1440, HSBC face):**

| | HEAD | W5a (root bounded) | F5 (chart-only) |
|---|---|---|---|
| own-size, cand2 r1/r2/r3 | 82 / 104 / 146 | 0 / 0 / 0 | **0 / 0 / 0** |
| K3 V5 sample (cand2-r1 index+payments, 8 theme/mode) non-chart moved v HEAD | — | 0 | **0** (6,136 elements; chart 2,698) |
| canon-gallery non-chart moved v HEAD (light, dark) | — | 49, 49 | **0, 0** |
| nio-dash-console-v1 non-chart moved v HEAD | — | 3, 3 | **0, 0** |
| all 58 `_fitness-test` pages, light, non-chart moved v HEAD | — | — | **0** (7,862 elements; chart 916) |
| all 30 cand2 pages, light, non-chart moved v HEAD | — | — | **0** (10,549 elements; chart 4,097) |
| harness views cand2 r1/r2/r3 (dead·cut·coll·size·markers) | — | 18 · 8 · 37 | **18 · 8 · 37** = 1.8 / 0.8 / 3.7, mean 2.10 |

- W5a v F5 on the V5 sample: 0 non-chart; 160 chart elements differ and every one is SVG text 16 → 27px (glyphs ×1.7) on identical engine bytes — the reduced-motion fit flake V5 §2d / W5a Q3 names, not the canon change. Every chart HTML part (legend buttons 20px, spans 12px, data-table cells, Reset 22px) is identical to W5a's.
- Held-back version ≡ W5a: canon-gallery W5a v (F5 + the held-back patch) → 0 elements moved, light and dark.
- 13 chart test pages + 58 `_fitness-test` screens own-size: HEAD 238 · W5a 249 · F5 259. Explained to the part: F5 = W5a on every chart part (canon-gallery's legend items 1 → 2 findings each are W5a's declared true findings — that page links canon.css without type.css) and = HEAD on every non-chart part (Account-selector trigger, Drawer, Modal-lightbox, Popover ×3, Toast ×2 back to their HEAD finding, 1 each). Not a regression: the eight are the unruled root question, exactly as at HEAD.
- Gates on the mount after the copy: `gen_canon_components --check` OK (137) · `gen_component_partials --check` OK · `gen_showroom --check` OK · `_validate_behaviour` OK · `_drive_chart_engine --check` 27 FRESH · `_validate_descender_clip` PASS, specificity ratchet at zero · `_validate_dataviz` PASS (15).
- Not re-run on F5 (CSS-independent, unchanged from W5a): receipt gate reds 6/6/10 → 0/0/10, icon-source, geometry fixes, `test_icons_markup.py`, `_validate_receipt --selftest`, `_validate_geometry --selftest` (V5 re-ran them on W5a's identical bytes).

**Held back for Dave:** `notes/_lanes/304/W5a/held-back/root-default-bounded.patch` (one hunk, `git apply --check` clean on the F5 tree; outside the generated block, so `gen_canon_components --check` stays OK; the 14 restores stay and become redundant) and `canon-root-default.W5a.css` (the rule as W5a wrote it, with what it changes, V5's measured examples, how to take it: apply, then re-drive the 13 receipts). Crops of the choice: `notes/_lanes/304/F5/renders/trim-{stat-card,account-selector}-{today,heldback}.png` (canon gallery, 2x; Stat-card rows grow ~29px).

## 2 · W5c — session titles

- `knowledge/gen_kg_titles.py` `session_rulings`: `re.compile(r"^#%d(?!\d)" % n)` on `ruled`, OR `^s<n>-` on the id. `ruled == "#n"` missed `#79-D1`, `#81-D1`, `#82-D1` (V5's three) and also `#76 (dream pass 4)` (7 rulings), `#31/#34`, `#57 / #60-D1`.
- `knowledge/_kg_explorer.template.html` `sessionTab`: the same reading (`new RegExp('^#'+n+'(?!\\d)')`), so the "What was ruled" tab lists what the title counts.
- `--write` → `_node_titles.json` (7 titles changed: sessions 31, 57, 76, 79, 81, 82, 245); `--check` OK on the mount; `--selftest` 12/12; mutation (W5c's equality restored) → bite 12 FAILS.
- `notes/_KG-EXPLORER.html` rebuilt in the clone with HEAD soft-set to `ff382c0b` (so the stamp and history are the mount's, not a clone sha): vs the mount's previous bytes, 22 diff lines = the stamp (`3100da99` → `ff382c0b`, V5's declared class), 7 session labels, the template's two lines. Node ids, edges, coordinates unchanged.

## 3 · W5b — the sitting page

Edited `notes/_lanes/304/W5b/page.src.html` and `build.py` on the mount (originals kept as `notes/_lanes/304/F5/{page.src.W5b-original.html,build.W5b-original.py}`), `render.py` run at the seat.

**V5's corrections, applied:**
1. **Call 1**: the rec no longer says wave five changes no rendered page; it says what renders differently (legends/Reset/chart tables to own size, right-edge labels whole; canon.css, engine, 30 regenerated pages), that nothing outside the charts moves (F5's 88 pages), and what stands in for the cold run (own-size 82/104/146 → 0, ink 5.10 → 2.10, receipt reds 6/6/10 → 0/0/10 with run 3's ten = call 4). The trace figures are attributed to candidate 1 v v1.0.13 (W3b), and candidate 2's trace is declared unmeasured. The top stat tile carrying 0.38 → 0.18 got the same attribution.
2. **Call 5**: the "generator scope leak, fixed either way" sentence is replaced — it is not a generator fix, it is Dave's, call 41b.
3. **Call 6**: the right-hand twin is built (W5a, ds-012 b, same provisional constants) — a yes ratifies it; W5a's region before/after pair added.
4. **Call 11**: six of nine.
5. **Call 53**: rewritten as ratify-or-reverse of what W5c built (1,203 → 0 in three kinds; 49 left: 30 polarities, 13 guidelines, 6 artefacts; 45 hand-checked titles, none misstated; F5's count fix), pointing at 41e. Group 6's header no longer says nothing touches a build.
6. **Call 4**: W5a's sharper wording folded in (the mint takes the first registered AUTO-BEHAVIOUR name in document order; options (a)/(b); both recommend (a)).

**The slot (41a–41e), its own list so the 53 ids/numbers do not move; three decision boxes added through one extra overlay target keyed by element id:**
- 41a note → call 4 (Q1).
- 41b decision: Kpi-tile spark in the bento 40 or 44px (W5a Q2), recommended 40 (this seat's reading from call 23; flagged as such).
- 41c decision: the root trim default — today's (chart-only) v the held-back W5a version, V5's measured examples in text, Stat-card and Account-selector today/held-back pairs, W5a's legend before/after pair; recommended keep today's through the cut, take the held-back one only with a yes to call 23. Call 23 got a one-line pointer to 41c.
- 41d note: Q3 reduced-motion fit bug, seen, pre-existing (payments 6/10 → 2/10), being fixed separately.
- 41e decision: canvas code-only v code+title (W5c's dug-canvas render embedded), and title the 49; recommended code alone on the canvas, title everywhere else, yes to the 49.

**Declared, beyond V5's list (to keep the page from contradicting itself):** the "running next without a ruling" line in What stays parked (wave five settled the right-hand cut, legend buttons, token-node wiring; KPI 44px is 41b); "What runs next" call 1 (wave five commits first); Technical (dream pass 14 at `ff382c0b`, 8 proposals, 0 ruled, waits for the dream ritual — V5's context line; wave five and its survey; W5a's slot line); the footer (53 + three in the slot, not taken by the whole-page yes). **Fixed on sight, pre-existing W5b bug:** `.specs.one` also matched the black "one decision" box rule `.one`, so call 5's three descender crops sat on a black band; one CSS line (`.specs.one{…background:none…}`) in `build.py`.

**Render:** 1440 h 42,455px, 390 h 69,254px; scrollWidth = viewport both; 0 off-edge, 0 clipped, 0 broken, 0 page errors; calls 53, boxes 58; slot boxes read "Decision 41b/41c/41e", call 53's box still "Decision 53". Looked at: slot (1440, 390), calls 1, 5, 6 (390), 53, the stat row — element shots in `notes/_lanes/304/F5/shots/` (driver `notes/_lanes/304/F5/look.py`). W5b's slice shots in `notes/_lanes/304/W5b/shots/` were overwritten by the re-render (the sandbox cannot delete; stale slices past part 39 at 390 are not produced by this render).

## 4 · SURVEY — fresh clone, whole wave five

`$HOME/f5s` at `ff382c0b` + 51 overlay files (`notes/_lanes/304/F5/survey/overlay-files.txt`: W5a's 41 with F5's canon/generator/receipts, W5c's 5, the sitting page, the W5a/W5b/W5c/V5 reports) + lane dirs W5a, W5b, W5c, V5, F5 → `wire_kg_generators.py .` (4 steps + 4 GATE routes; `--check` idempotent) → C1 serial (`_render_rulings` → `tokens/_build_blast_radius` → `_build_memento_index` → `_build_graph_mention_map` → `_gen_chain` (7,799 tk) → `_gen_schematic`, all rc 0, `survey/serial.log`) → `_build_survey.py --include-mutating --resume --timeout 60` in chunks **1:30 · 31:70 · 71:100 · 101:127 · 128:141 · 142:152** (128 and 129 together).

- FAIL: `[81]` 4px-grid · `[90]` fork-ban · `[98]` roles/answers · `[131]` `[132]` delta-audit ×2 · `[136]` integrity lint · `[138]` probe registry · `[139]` claim-table linter · `[148]` pack ship-list — V4's/V5's nine. Could-not-ask `[10] [13] [61] [68] [140]`; timeout `[73]`.
- `compare-v4-f5.txt` (V5's `v5cmp.py`, V4's `notes/_lanes/304/V4/logs/after_*.log`): all 10 red blocks **identical**. By step name: 0 green→red, 0 red→green, 4 new steps all ✅ (`[86]`–`[89]`).
- Not in the overlay (V5 did not include them either): the cand2 outputs/RUN-REPORTs, `_REVIEW-304-candidate-2-*`, R4s2, C4's report and brief. They are notes the commit seat adds; no step was seen to read them.

## FOR THE COMMIT SEAT

**Order:** (1) nothing to regenerate — the mount bytes are the surveyed bytes (every tracked file below cmp-equal to `$HOME/f5s` at `e9396b6e`); (2) `python3 notes/_lanes/304/W5c/tools/wire_kg_generators.py .` (mount `_build_all.py` == HEAD; not applied here by fence); (3) the C1 serial as above, then `--check`s (`_gen_chain` reads 152 steps; `_CHAIN.md` moves); (4) mint the rows; (5) commit on `ff382c0b`; (6) CI read-back by name — the four new steps, `[129]` never chunk-split in a local re-run.

**Tracked, modified (44):**
- W5a sources (6 + harness): `knowledge/_validate_receipt.py`, `knowledge/_validate_screen.py`, `knowledge/_validate_geometry.py`, `knowledge/canon/gen_canon_components.py` (W5a + F5), `knowledge/canon/canon.css` (W5a copies + F5 root/restores), `knowledge/canon/dv-behaviour.js`, `notes/_lanes/304/R4c/harness/views.py`
- W5a regenerated (34): `knowledge/snippets/Chart-{bar,boxplot,bullet,butterfly-h,butterfly-v,candlestick,combo,donut,histogram,line,pie,scatter,sparkline,stacked-area}.reference.html`, `knowledge/snippets/Template-dashboard-bento.reference.html`, `showroom/chart-{same 14}.html`, `showroom/template-dashboard-bento.html`, `knowledge/_BEHAVIOUR-GATE.md`, `knowledge/_tests/chart-engine/_receipts.json` (re-driven by F5), `knowledge/_tests/geometry/geometry-{clean,planted}.html`
- W5c (3): `knowledge/_build_kg_explorer.py`, `knowledge/_kg_explorer.template.html` (W5c + F5), `notes/_KG-EXPLORER.html` (rebuilt by F5, stamp `ff382c0b`)
- by the wiring step: `knowledge/_build_all.py`; by the serial: `_CHAIN.md`, `knowledge/_memento-index.json`, `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html` (+ `notes/_RULINGS.html` if its date line moves — C4 restored it from HEAD)

**New (add explicitly):** `knowledge/gen_kg_titles.py` (W5c + F5), `knowledge/_node_titles.json`, `notes/_SITTING-304-tuesday-2026-09-29-v1.html`, `notes/_subreports/2026-09-27-304-{W5a-gate-bugs-and-trim,W5b-tuesday-sitting,W5c-node-titles,V5-verifier-wave-five,F5-wave-five-fixes}.md`, lane dirs `notes/_lanes/304/{W5a,W5b,W5c,V5,F5}/` (W5a now carries `held-back/`), plus V5's list (cand2 outputs/RUN-REPORTs, `_REVIEW-304-candidate-2-*`, `notes/_lanes/304/R4s2/`, R4s2's report, C4's report and brief).

**Rows to mint** (each carries its spec in its report unless noted):
- `W-304fa` — W5a's spec (its report §`_state` row spec); amend the title/body: "leading-trim scaffold stops at the next component scope (111 copies); the ROOT default change was narrowed by F5 to a chart-only restore and held back for Dave (call 41c)".
- `W-304fb` — W5b's spec; add to body "corrected by F5 per V5 (calls 1, 4, 5, 6, 11, 23 pointer, 53; slot 41a–41e; 58 boxes)".
- `W-304fc` — W5c's spec; add "session count fixed by F5 (#n-Dk and '#n (…)' forms)"; its closes_when names the wiring, which lands in this commit.
- `W-304v5` — V5's spec (V5 wrote the id as `W-304fv5`; the brief names `W-304v5` — use one, say which).
- `W-304s2` — R4s2's spec, `notes/_subreports/2026-09-27-304-R4s2-candidate-2-scores.md` line 68.
- `W-304f5` — below.
- `W-304c5` — the commit seat's own row, written by the commit seat (interim-report pattern as C4).

## LIMITS

Everything at the arm64 seat, 1440 for K3/own-size/views (390 only for the page); K3 on the 88 pages ran light only (V5's sample ran all 8 theme/mode pairs); the receipt and screen gates were not re-run on the F5 canon (they do not read CSS); the survey baseline is V4's after logs; x64 CI unproven until the push. `$HOME/f5w`, `$HOME/f5s`, `$HOME/f5st`, `$HOME/f5t`, `$HOME/f5runs`, `$HOME/f5m` die with the VM; W5a's idle clone `$HOME/w5a` was removed to make room (its receipts are in `notes/_lanes/304/W5a/`).

## `_state` row spec

```json
{"id":"W-304f5","title":"#304 F5 wave-five fixes - trim narrowed to a generated chart-only restore (root default back to HEAD, W5a's root version held back for Dave as call 41c), session titles count #n-Dk and '#n (...)' rulings (six '0 rulings' titles true), sitting page corrected per V5 with slot 41a-41e filled; fresh-clone survey 152 steps 0 green-to-red","home":"notes/_subreports/2026-09-27-304-F5-wave-five-fixes.md","links":["knowledge/canon/gen_canon_components.py","knowledge/canon/canon.css","notes/_lanes/304/W5a/held-back/root-default-bounded.patch","knowledge/gen_kg_titles.py","notes/_SITTING-304-tuesday-2026-09-29-v1.html","notes/_lanes/304/F5/measure/k3/","notes/_lanes/304/F5/survey/compare-v4-f5.txt"],"project":"apollo","opened":304,"state":"open","owner":"claude","condition":"stated","body":"s218-D7 filed report. Own-size cand2 82/104/146 -> 0/0/0; K3 v HEAD 0 non-chart text parts moved on 88 pages (V5 sample 6,136 elements x 8 theme/modes, 58 fitness pages, 30 cand2 pages); harness ink 1.8/0.8/3.7 (= W5a); 13 receipts re-driven, 0 measurement changes. Titles: #76 7 rulings, #31/#57/#79/#81/#82 1 each, #245 10->11; selftest 12/12, bite 12 mutation-tested. Page: 53 calls, 58 boxes, 0 overflow at 1440/390; pre-existing .specs.one black band fixed. Survey: same nine reds, blocks identical to V4, four new steps green, 128/129 one chunk.","closes_when":"the wave-five commit lands on ff382c0b with the wiring applied and CI read back by name (four new steps green, no green-to-red), and Dave has answered 41c (root trim default: today's or the held-back version)"}
```
