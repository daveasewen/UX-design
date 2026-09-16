# LANE SC — REPORT — `scope` per guideline file: 34 rows, inference by declared scope, `routed-by-scope` in the reader
#279 · 2026-09-16 · enacting `s277-D9` (with `s274-D11` same-commit consumer, `s274-D12` obeys kept, `s277-D5` no prose joins) · lane SC (Fable 5.1) · judgement lane: every row is a claim graded against the file's own words

**The one line.** 34 rows landed in `knowledge/guidelines/_scope.json` (8 component · 23 facet · 3 declared null), read by `_compose_slice.py` as a fourth obeys class `routed-by-scope` and by ASK Q2. Rules reaching ≥1 component: **107 → 410 of 470** (60 unreached, 24 of them pictogram/illustration rules that nothing in the canon can carry); BLOCKING: **9 → 52 of 59** (7 unreached: the 6 pictogram BLOCKING rules + ill-010). Selftest 43 → 54 bites (11 added, 0 rewritten, 1 allowed-set widened), 0 failed; `_validate_kg.py` rc 0.

## 1. Where it lives, and why there

`knowledge/guidelines/_scope.json` — a **sibling** of `_rules-index.json`, not keys inside it. Reason, checked: `_rules-index.json` is written whole by `knowledge/guidelines/gen_rules_index.py` (`out = {'$description', 'count', 'byDestiny', 'rules'}` → `write_text`, header "GENERATED … do not hand-edit"); any added key is dropped on the next regen. `grep -l _rules-index knowledge/*.py` names seven readers (`_build_consult_index`, `_build_instrument_fit`, `_compose_slice`, `_validate_kg`, `gen_kg_principles`, `gen_kg_rules`, `gen_runbook_index`) and no writer — the writer is the guidelines-dir script. The rows are hand-authored (this lane), never generated; the file says so in `$description` and carries `ruledBy`, `$sourceRule` and `$joinRule` so the join is declared in the store, not hidden in code.

Row shape (as briefed): `{file, kind: component|facet|null, facets[], tokenGroups[] (derived = the union of its facets' groups, so every name is real), components[] (authored only), exceptions[{rule, why}], $source, rules, $why | $note}`.

## 2. The facet set — proposed from the files, closed, 18 names

Each facet declares HOW a component binds it (`facets[f].binds`): token groups (the 43-group tier map `_compose_slice._token_tier_map` reads — the brief's "≈128" is the leaf/group count in `tokens/_blast-radius.json`; the reader's own group map has 43 names and those are the ones used), meta fields, or edge types (`usesIcon`/`usesLogo` from the ratified node files, `renderedBy` from the meta).

| facet | files covered | components binding it | binds |
|---|---|---|---|
| `copy` | 7 | 116 | groups: text |
| `type` | 7 | 116 | groups: text, typography |
| `colour` | 4 | 132 | groups: 26 semantic colour groups + color |
| `dark-mode` | 3 | 132 | groups: 25 semantic colour groups |
| `icons` | 2 | 111 | groups: icon; edges: usesIcon |
| `pictograms` | 1 | 0 | — (declared: nothing binds it today) |
| `illustration` | 2 | 0 | — (declared: nothing binds it today) |
| `imagery` | 4 | 2 | groups: image |
| `logos` | 2 | 9 | edges: usesLogo |
| `motion` | 4 | 46 | groups: motion; meta: motion |
| `elevation` | 1 | 36 | groups: elevation, blur, overlay |
| `layout` | 4 | 85 | groups: layout, breakpoint, gap, padding, size; meta: responsive |
| `interaction` | 5 | 60 | groups: focus, target; meta: interactive, stateModel |
| `markup` | 1 | 137 | edges: renderedBy |
| `forms` | 3 | 49 | groups: form |
| `data-vis` | 2 | 19 | groups: data, data-vis, dataviz |
| `status` | 2 | 54 | groups: rag |
| `media` | 2 | 0 | — (declared: nothing binds it today) |

Three facets bind nothing today — `pictograms`, `illustration`, `media` — and say so in their `$why`. That is the honest shape: a pictogram rule does not reach `button` because no meta carries a pictogram (pict-014 names the library gap). `media` reaches `video-player` only through the authored component on the content-authoring row.

## 3. The 34 rows

Kinds: **8 component** (the 4 Common-Toolkit family files + the 4 data-visualisation files — exactly the 8 the ruling counts as binding a component) · **23 facet** · **3 declared null** (`accessibility-framework.md` — its own scope sentence is product-level, "applies to all external-facing HSBC digital products worldwide"; `accessibility-qa-cx-testing.md` — "this is the METHOD page"; `generative-ai-brand.md` — "This is GOVERNANCE, not visual rules"). The ruling said "26 bind a facet"; 23 + 3 nulls = those 26 — the nulls are the three whose prose binds a product, a method or a tool, not a facet a meta can bind. Under-specified by the ruling; chosen and said here.

`reach` = components the row reaches today (authored ∪ facet-bound), from `--measure-scope`.

| # | file | kind | facets | groups | authored components | exceptions | rules | reach |
|---|---|---|---|---|---|---|---|---|
| 1 | `accessibility-client-side-dev.md` | facet | markup, interaction, forms, media, motion | 4 | — | 0 | 15 | 137 |
| 2 | `accessibility-content-authoring.md` | facet | copy, media | 1 | video-player | 0 | 12 | 116 |
| 3 | `accessibility-framework.md` | **null** | — | 0 | — | 0 | 1 | 0 |
| 4 | `accessibility-information-architecture.md` | facet | copy | 1 | — | 0 | 1 | 116 |
| 5 | `accessibility-interaction-design.md` | facet | interaction, layout, forms, copy | 9 | — | 0 | 14 | 133 |
| 6 | `accessibility-qa-cx-testing.md` | **null** | — | 0 | — | 0 | 1 | 0 |
| 7 | `accessibility-standards-hub.md` | facet | interaction | 2 | — | 0 | 1 | 60 |
| 8 | `accessibility-visual-design.md` | facet | colour, type, imagery, interaction, motion | 29 | — | 1 | 7 | 135 |
| 9 | `app-foundations.md` | facet | type | 2 | — | 1 | 3 | 116 |
| 10 | `brand-refresh-assets.md` | facet | logos, imagery | 1 | — | 3 | 7 | 11 |
| 11 | `colour-standards-2026.md` | facet | colour, data-vis, status | 27 | — | 3 | 21 | 132 |
| 12 | `colour-usage.md` | facet | colour, status, dark-mode, data-vis, illustration | 27 | — | 1 | 13 | 132 |
| 13 | `common-toolkit-buttons.md` | component | — | 0 | button, icon-button | 1 | 14 | 2 |
| 14 | `common-toolkit-foundations.md` | facet | layout, type, dark-mode | 31 | headers, footer | 0 | 4 | 135 |
| 15 | `common-toolkit-links.md` | component | — | 0 | links | 0 | 15 | 1 |
| 16 | `common-toolkit-notifications.md` | component | — | 0 | notifications | 0 | 17 | 1 |
| 17 | `common-toolkit-tags-chips.md` | component | — | 0 | tags, selection-controls | 0 | 23 | 2 |
| 18 | `copywriting.md` | facet | copy | 1 | button, links, modals, progress-tracker | 0 | 55 | 116 |
| 19 | `data-visualisation-bar-charts.md` | component | — | 0 | chart-bar, Chart-histogram, Chart-butterfly-h, Chart-butterfly-v | 0 | 10 | 4 |
| 20 | `data-visualisation-line-charts.md` | component | — | 0 | chart-line, chart-sparkline | 0 | 11 | 2 |
| 21 | `data-visualisation-pie-charts.md` | component | — | 0 | chart-pie, chart-donut | 0 | 11 | 2 |
| 22 | `data-visualisation.md` | component | — | 0 | Chart-boxplot, Chart-bullet, Chart-butterfly-h, Chart-butterfly-v, Chart-candlestick, Chart-histogram, Chart-scatter, chart-bar, chart-combo, chart-donut, chart-line, chart-pie, chart-sparkline, chart-stacked-area, legend | 0 | 19 | 15 |
| 23 | `generative-ai-brand.md` | **null** | — | 0 | — | 0 | 6 | 0 |
| 24 | `icons.md` | facet | icons | 1 | — | 3 | 17 | 111 |
| 25 | `illustration-standards.md` | facet | illustration | 0 | — | 1 | 10 | 0 |
| 26 | `motion-standards.md` | facet | motion | 1 | — | 1 | 7 | 46 |
| 27 | `naming.md` | facet | copy | 1 | — | 0 | 5 | 116 |
| 28 | `neurodiversity.md` | facet | layout, colour, type, copy, imagery, motion, interaction | 34 | — | 3 | 26 | 135 |
| 29 | `pictograms.md` | facet | pictograms | 0 | — | 1 | 14 | 0 |
| 30 | `tone-of-voice.md` | facet | copy | 1 | — | 0 | 40 | 116 |
| 31 | `typography-standards-2026.md` | facet | type | 2 | — | 5 | 24 | 116 |
| 32 | `typography-usage.md` | facet | type | 2 | — | 0 | 8 | 116 |
| 33 | `visual-assets.md` | facet | imagery, icons, logos | 2 | empty-state, confirmation | 0 | 20 | 111 |
| 34 | `web-foundations.md` | facet | dark-mode, elevation, layout, type, forms | 33 | — | 7 | 18 | 135 |

**Exceptions — 27 across 13 files**, one class dominates: a `[REVIEW]` rule that records a tension about the source, the register or the token store (webf-029..034, neuro-041/042/044, icon-015/016/017, type26-015/016/025/026/029, ill-007, pict-014, mot-007, hex26-002/005, bra26-001, appf-008, col26-001/007, col25-008, ctkb-015) is not an obligation a component can obey; plus two rule-specific ones — `avd-008` (journey-level redundant entry) and `col26-021` (a rule on the token store / Figma style descriptions). Each carries its `why` in the row. `ctkb-015` is the one rule reached by obeys alone (a meta authored it) — authored wins, the exception only stops the inference.

**Every `$source` is a verbatim span of its file**, matched as a substring after collapsing whitespace runs (the files hard-wrap at ~90 columns; `$sourceRule` in the store says so). 34/34 pass in bite 45; bite 46 proves the check bites by mutating one word. Two rows rest on a title line rather than a body sentence (`accessibility-visual-design.md`, whose scope IS its role; and the data-vis subfiles rest on the named type — "Doughnut", "Spark (sparkline)"); the `$why` on each says what else the row leans on.

## 4. The consumer, same commit (`s274-D11`) — `_compose_slice.py`

Added (261 lines, 7 changed — `git diff --numstat` in § 8): a "declared scope" section (`_meta_token_groups`, `component_facets`, `scope_reach`, `rule_reach`, `measure_scope`), `g["scope"]` in `load_graph`, the `routed-by-scope` leg at the end of `obeys_for` (BLOCKING rules only, mirroring `routed`; class priority authored > derived > routed > routed-by-scope — a row never downgrades), a `_reduce` step that drops routed-by-scope rows BEFORE routed ones (inference goes first under budget), the class in `explain()`, ASK Q2 `routedByScope` (the full 470-rule reach, all destinies, kept apart from the `obeys` answer; nulls and exceptions DECLARED in `declared[]`), `--measure-scope`, and the docstring. `routed` (vocabulary) is untouched and stays distinct; `RULE_FILE_ROUTES` unchanged.

On the worked dashboard task the seed now carries **15 routed-by-scope BLOCKING rows** (col26-004/008/009/011/012/015/016/017/018, logo26-001, photo26-002, mot-005, neuro-026, tov-038, appf-002) that no path reached before; seed 28,621 → **31,536** cl100k (ratio vs the 31 metas 3.89× → 3.53×) — the RD report's 3.89× is now the pre-scope figure. `notes/_lanes/279/scope/seed-dashboard-explain.txt`.

Not touched: `_build_kg_explorer.py`, `_KG-EXPLORER.html` (lane EX live). The explorer's 'inference by declared scope' chip is EX's to draw from `scope_reach(g)` — one import.

## 5. Measured — before / after, with the command

Command: `python3 knowledge/_compose_slice.py --measure-scope` → `notes/_lanes/279/scope/measure-scope.json`.

| figure | before (obeys only) | after (obeys ∪ scope) |
|---|---|---|
| of 470 rules, reach ≥1 component | 107 (363 reach none) | **410** (60 reach none) |
| of 59 BLOCKING, reach ≥1 component | 9 (50 reach none; 46 counting the rule→cites→sc→appliesTo→component path, which is the ruling's figure — that path is not counted here) | **52** (7 reach none) |
| by scope alone / obeys alone / both — all rules | — | 303 / 1 / 106 |
| by scope alone / obeys alone / both — BLOCKING | — | 43 / 0 / 9 |

The 60 unreached: pictograms 14 · illustration-standards 10 · web-foundations 7 (all REVIEW exceptions) · generative-ai-brand 6 (null) · typography-2026 5 (REVIEW) · brand-refresh 3 · colour-2026 3 · icons 3 · neuro 3 · one each in app-foundations, qa-cx (null), visual-design (avd-008), framework (null), colour-usage, motion. The 7 BLOCKING unreached: pict-001/007/008/009/010/011 + ill-010 — every one a rule on an asset class no component carries.

## 6. Gates — every line

```
$ python3 knowledge/_compose_slice.py --selftest
  54 bites, 0 failed   (1–43 as at d6bd57b; bite 18's allowed class set widened by one name — the only touch to an existing bite;
                        44 every file has a row or declared null · 45 every $source is a live substring 34/34 · 46 a mutated $source fails
                        · 47 every group/facet/component/exception exists · 48 routed-by-scope never fires on a null file (137 metas forced)
                        · 49 never passed off as authored/routed · 50 MUTATION planted exception suppresses its rule, live file untouched
                        · 51 MUTATION row flipped to null routes nothing · 52 the two paths sum · 53 ASK Q2 scope path ≤1K (116 comps, 656 tok)
                        · 54 ASK Q2 on a null file declares the null)
$ python3 knowledge/_validate_kg.py            → OK … rc 0
$ python3 knowledge/_validate_help_gate.py     → 15 PRE-EXISTING misses, _compose_slice.py not among them (same as RD) — declared, not mine
$ python3 knowledge/_compose_slice.py --measure → seed 31,536 / 111,468 (3.53×); step-1-before-wiring 31.89×
$ python3 knowledge/_compose_slice.py --measure-scope → § 5
$ python3 knowledge/_compose_slice.py --ask "which components does rule:copy-012 bind?" → 116 components by scope, obeys [], 656 tokens (notes/_lanes/279/scope/ask-q2-copy-012.json)
```

## 7. Not done, with size — and where the ruling under-specified

1. **The explorer chip** ('inference by declared scope' with an exception row, on the page) — `s277-D9`'s own wording, but `_build_kg_explorer.py` is lane EX's file this session. Size: ~25 lines (import `scope_reach`, one edge family `routedByScope` rule→component, one chip). Left for EX or the next explorer touch.
2. **Facet grain is file grain.** A file with five facets (neurodiversity) routes a flashing rule to a text-only component via `type`. The ruling chose per-file scope; per-rule facets would be 470 rows. Exceptions carry the worst cases; the rest is the ruling's own coarseness, declared. Size to refine: a per-rule `facet` override key (~10 lines in the reader, rows on demand).
3. **`≈128 token groups`** in the brief vs the 43 the reader's tier map holds. I used the reader's 43 (the brief says "the groups `_compose_slice.py` reads"); the 128-ish figure is `_blast-radius.json`'s. Size: 0 — a naming note.
4. **Three facets bind nothing** (pictograms, illustration, media) → 24 rules unreached by design. A pictogram/illustration component or token group is a component lane (pict-014 already logs it). Size: that lane.
5. **RD's 3.89× figure** is now 3.53× (the seed grew by 15 rows). W-279rd's closes_when names 3.9×; the store row for this lane says so. Size: 0.
6. **msgfile in /tmp** — as briefed; the script's header says a session dir; it does not enforce (RD hit the same).
7. `.git/index.lock` found 23 min old, 0 bytes (15:11 +0100), no git process — moved to `.git/_orphan-locks/` per the brief before staging.

## 8. Shipped sha and `git diff --numstat` from it

(appended after the commit)
