# 304 · J — Jev on the graph's edges and node titles (advisory side-probe)

provenance: session #304, seat J (Opus 5.5), Sunday 2026-09-27 · ADVISORY · governed by `s294-D10` (Jev is a dev-time instrument only, never a blocking dependency; the option of later integration stays open). Nothing in the graph or any canon file was changed. The only shared file touched is `knowledge/_jev-receipts.jsonl`, appended by the adapter: **70 lines** (19 → 89), one per call.

## The answer first

Jev is good at one job here and bad at another. Asked "does this component really obey / fill / answer / take this?", it separates real edges from plausible fakes well: area under the curve **0.954**, and at its extremes it is clean — every edge it scored below 0.2 was a fake (8 of 8), every edge it scored above 0.8 was real (19 of 19). In the middle band it is noisy and leans towards doubting real edges. It fails on edge types whose truth lives in text it was not shown (`yieldsTo`'s condition, `appliesTo`'s interactive parts), on `bindsToken` (a structural fact code already has), and on `tensionWith`, where it cannot tell two principles that pull apart from two that agree.

Recommendation: worth keeping as a **suggester Dave ratifies**, for four edge types only (`obeys`, `providesRole`, `answersIntent`, `hasDataShape`), run by hand as a dev-time sweep with a two-band rule — below 0.2 goes to Dave as "this link looks wrong", 0.2–0.8 is ignored, above 0.8 is silent. Never a gate, never in `_build_all.py`. Node titles are a **mechanical** problem, not a Jev one.

## What was done

1. **Canonical edge list** = the KG explorer's own reader: `knowledge/_build_kg_explorer.py` `extract()` + `extract_extra()` (1,642 base edges + 8,094 extra; 5,102 nodes). No second reader was written.
2. **Sample** (`notes/_lanes/304/J/build_sample.py` → `candidates.json`, seed 304): 40 real edges stratified across eight types (obeys 8, providesRole 6, answersIntent 5, bindsToken 5, hasDataShape 4, yieldsTo 4, appliesTo 4, tensionWith 4) + 10 hand-built plausible-but-false edges (one or two per type, each checked absent from the graph in any direction). A seeded random negative draw was tried first and discarded: it produced trivially false pairs (Pie chart → a notification-banner rule) that test nothing.
3. **Labels frozen before the first call** (`labels.py` → `labels.json`): each TRUE/FALSE with a one-line reason, a receipt (meta / rule / roles.json / chart-intents.json / polarity id) and a firmness (43 firm, 7 soft). sha256 **`911535ada2edee25d3611420707c59e75f4860f84a87e7f6415dbae1f20543ed`**; `analyse.py` refuses to score if the hash moves. labels.json written 2026-09-27T02:00:27Z; first Jev call 02:00:42Z (receipts file).
4. **The question** (one Noul per edge, `run_edges.py`): state = the relation's meaning in plain words + what the source IS + what the target IS (component name and purpose; rule text; principle statement; role / intent / shape definition; sc title and check; token group members). The authored `$why` was **deliberately withheld** — sending it would test whether Jev can read a justification, not whether the edge is true. Target nodes were described by their text, never their title (the J7 limit: `rule:ctkb-003` as a title tells Jev nothing).

## Edge results (threshold 0.5, n = 50)

| | all 50 | firm labels only (43) |
|---|---|---|
| accept precision (Jev says true → is true) | 0.971 | 0.967 |
| accept recall | 0.825 | 0.879 |
| **flag precision** (Jev says false → is false) | **0.562** | 0.692 |
| **flag recall** (fakes caught) | **0.9** | 0.9 |
| accuracy | 0.84 | 0.884 |
| Brier (lower is better) | 0.117 | 0.089 |

At a 0.5 cut Jev raises 16 flags, of which 9 are real fakes. The two-band rule is what makes it usable: **below 0.2 → 8 flags, 8 fakes, zero real edges** (it missed 2 of the 10 fakes). That is n = 50 on one day; treat it as a direction, not a constant.

**Calibration** (Noul probabilities):

| p band | n | mean p | share actually true |
|---|---|---|---|
| 0.0-0.2 | 8 | 0.101 | 0.0 |
| 0.2-0.4 | 5 | 0.274 | 1.0 |
| 0.4-0.6 | 6 | 0.49 | 0.833 |
| 0.6-0.8 | 12 | 0.708 | 0.917 |
| 0.8-1.0 | 19 | 0.887 | 1.0 |

Well calibrated at both ends, **under-confident in 0.2–0.6**: 10 of 11 edges there were real. Jev doubts more than it should in the middle.

**By edge type:**

| type | n | accuracy | mean p, true edges | mean p, false edges | verdict |
|---|---|---|---|---|---|
| obeys | 10 | 1.00 | 0.748 | 0.075 | useful |
| providesRole | 8 | 0.88 | 0.873 | 0.33 | useful, missed the one near-miss negative |
| answersIntent | 6 | 1.00 | 0.892 | 0.07 | useful |
| hasDataShape | 5 | 1.00 | 0.9 | 0.15 | useful |
| yieldsTo | 5 | 0.60 | 0.44 | 0.16 | weak — cannot see the `when` condition |
| bindsToken | 6 | 0.83 | 0.644 | 0.14 | pointless — code already knows from the tokens block |
| appliesTo | 5 | 0.60 | 0.573 | 0.09 | weak — cannot see the component's interactive parts |
| tensionWith | 5 | 0.60 | 0.51 | 0.47 | no separation — cannot tell tension from agreement |

**Every disagreement:**

| edge | type | pair | my label | Jev p |
|---|---|---|---|---|
| E17 | providesRole | amount-display → headline-metric | FALSE (firm) | 0.61 |
| E31 | yieldsTo | breadcrumbs → tabs | TRUE (firm) | 0.21 |
| E32 | yieldsTo | chart-line → Chart-candlestick | TRUE (firm) | 0.42 |
| E36 | bindsToken | template-dashboard-bento → form | TRUE (soft) | 0.22 |
| E41 | appliesTo | 2.4.7 → template-error | TRUE (firm) | 0.29 |
| E43 | appliesTo | 1.4.13 → Chart-histogram | TRUE (firm) | 0.36 |
| E48 | tensionWith | pr-aesthetic-usability → pr-nng-visibility | TRUE (soft) | 0.29 |
| E49 | tensionWith | pr-f-pattern → pr-information-scent | TRUE (soft) | 0.45 |

Failure modes, separated as the skill asks:

- **Missing evidence, not model error** — E31, E32 (`yieldsTo`) and E41, E43 (`appliesTo`). The yield is true *under a condition* that lives in the meta's `when` prose; the success criterion applies because the error page has links and the histogram has hover popovers, neither of which the purpose text says. Give Jev the `when` text or the snippet's control list and these would likely move; that is a second probe, not this one.
- **Model can't make the distinction** — `tensionWith`. Hick's law vs choice overload (they agree) scored 0.47; aesthetic–usability vs visibility (a real, if indirect, polarity) scored 0.29. The label itself needs the polarity's mediating variable to judge; Jev at this shape is a coin.
- **Near-miss negative accepted** — E17, Amount display → headline-metric, 0.61. The one fake built to be genuinely close got through.
- **Soft edges drift low** — Jev's three lowest-scoring real edges outside the evidence gaps (E36, E48, E49) are all ones I had marked soft. That is the useful half of the signal: where Jev hesitates on a real edge, a human hesitates too.

**Cost measured:** 50 calls, **29,129 input / 1,000 output tokens**, latency median **350.2 ms** (range 308.6–453.7), faster than #293's 579–621 ms. A full sweep of the four useful types (168 obeys + 108 providesRole + 28 answersIntent + 26 hasDataShape = 330 edges) would be ≈ 330 calls, ≈ 190k input tokens, ≈ 2 minutes serial.

## Node titles

**Mechanical check, no Jev** (`node_titles.py` → `node-titles-mechanical.json`), over all 5,102 explorer nodes. Classes: **A** opaque code, **B** bare path/URL, **C** bare machine slug, **D** readable.

- **A = 1,135 nodes say nothing about what they are**: all 617 rulings (`s133-D1`), 377 rules (`dv-line-008`), 92 sessions (`#165`), 30 polarities (`pl-25`), 13 guidelines (`3.2`). The text exists in each case (`_rule_nodes.json` has every rule's text, rulings carry `says`, polarities a mediating variable) — the explorer label just doesn't use it.
- **B = 525** bare paths (356 artefacts, 169 evidence); **C = 1,150** slugs (666 icons, 145 ux principles, 64 axe rules, 43 token groups, 12 roles, 14 intents); **D = 2,292** readable.
- The first regex pass misfiled `Dialog/Modal` as a path and `BOOT_FIRSTTURN_ERR` as readable; fixed and re-run before the sample was drawn. A regex has no sense of meaning, which is where the comparison below comes in.

**Jev on 20 (5 per class)**, hand-labelled "does the title alone say what this is?" before the calls (hash `e632e344ca33364e…`):

| class | type | title | my label | Jev p |
|---|---|---|---|---|
| A | guideline | 3.2 | no | 0.03 |
| A | ruling | s133-D1 | no | 0.03 |
| A | polarity | pl-25 | no | 0.04 |
| A | rule | dv-line-008 | no | 0.05 |
| A | session | #165 | no | 0.03 |
| B | evidence | notes/2026-08-02-81-cross-instrument-gate-blast-radius.md | yes | 0.51 |
| B | artefact | knowledge/_ICON-GAPS.md | yes | 0.45 |
| B | artefact | knowledge/assets/icons/icons.manifest.json | yes | 0.76 |
| B | artefact | reviews/ITINERARY-STATUS-2026-08-21-v3.html | yes | 0.63 |
| B | evidence | knowledge/tokens/palettes/rag/console-supercharge.json | no | 0.28 |
| C | artefact | BUDGET_WORKING | no | 0.52 |
| C | principle | perceivable | no | 0.06 |
| C | ruling | showroom-one-bar-chrome | no | 0.49 |
| C | token | focus | no | 0.05 |
| C | shape | parts-of-whole | no | 0.34 |
| D | iconGroup | Touch | no | 0.09 |
| D | artefact | empty-state.body -> text-param floated set | no | 0.13 |
| D | context | Budget vs actual views | yes | 0.76 |
| D | sc | 1.4.8 Visual Presentation | yes | 0.50 |
| D | evidence | chat #201 2026-08-18 - Dave picked 'Floor at 0 - squares stay square'  | yes | 0.39 |

Agreement with my labels: **Jev 17/20, mechanical 14/20**. Jev adds nothing on class A (5/5 both — codes are trivially codes) and its gain is at the edges of the regex: self-describing paths (`icons.manifest.json`) and readable-looking but empty titles (`Touch`, `empty-state.body -> text-param floated set`). It misread `BUDGET_WORKING` as a yes and a dated chat evidence line as a no.

So the title problem is **1,135 code-only labels**, fixable by code (label = code + first clause of the text already on the node), with no model involved. That fix is also the precondition for any future Jev-over-the-graph work (J7: "Jev is literal, so node titles must say what nodes ARE").

## Recommendation, in plain words for Dave

1. **Useful, for four edge types.** On `obeys`, `providesRole`, `answersIntent` and `hasDataShape` Jev told the fakes from the real links almost perfectly on this sample. As a periodic, hand-run check it could hand you a short list of "these links look wrong" to rule — nothing more.
2. **As a suggester, never a gate.** Its middle band doubts real links too often to block anything, and `s294-D10` rules it out anyway. It proposes; you ratify; the graph changes only by your word.
3. **Not for `yieldsTo`, `appliesTo`, `bindsToken`, `tensionWith`** at this question shape. The first two might recover with richer evidence (a second probe); `bindsToken` is already a fact in the metas; `tensionWith` is a judgement Jev can't make.
4. **Portability cost: none, if it stays where this probe ran.** A script under `notes/` or a `--jev` flag on an audit tool that prints "no oracle" and exits clean without a key. A colleague without a key loses the suggestions, not the graph. The cost appears only if a call site enters a build, gate or boot path — which is exactly what `s294-D10` forbids.
5. **Do the title fix first, without Jev.** 1,135 nodes are labelled with bare codes; that is mechanical, and it helps every reader — you, the explorer, and any later model.
6. **Side observation, mechanical, for you to rule:** `knowledge/roles.json` lists `amount-display` (the money-format display primitive) as a provider of the `input` role with no `when`. That looks like a misfile — it may be deliberate; not changed.

## Files

`notes/_lanes/304/J/` — `build_sample.py`, `candidates.json` (the 50 edges and the exact state sent), `labels.py`, `labels.json` (frozen, hashed), `run_edges.py`, `results-edges.jsonl` (raw answers + request ids), `analyse.py`, `results.json` (all metrics, per-row), `node_titles.py`, `node-titles-mechanical.json`, `node-titles-sample.json`, `run_titles.py`, `results-titles.json`.

## _state row spec

- id: `W-304jv`
- title: Jev edge + node-title probe — advisory; four edge types usable as a suggester, titles are a mechanical fix
- state: open (owed: Dave's ruling on whether to (a) cut a hand-run advisory sweep over obeys/providesRole/answersIntent/hasDataShape with the two-band rule, (b) cut the mechanical title fix for the 1,135 code-only labels, (c) look at `amount-display` in `roles.json` input providers)
- evidence: `notes/_subreports/2026-09-27-304-J-jev-edge-node-probe.md`, `notes/_lanes/304/J/results.json`
- governs: none (advisory; `s294-D10` holds)

Calls used: **70 of 80** (50 edges + 20 titles), 0 errors, 0 retries. Key never printed.
