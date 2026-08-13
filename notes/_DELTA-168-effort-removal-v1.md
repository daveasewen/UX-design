# Ranking delta — the effort criterion removed (#168 DC2)

**PROPOSAL delta, not a ruling.** Dave's #168 review export, decision **DC2**: drop the
`effort` term (`1 − len(body)/1200`, weight 0.15) from `priorities()` in
`knowledge/gen_dashboard.py` until real `effort` values exist. `s168-D1` is **PENDING** —
it is minted at the #168 wrap, not by this lane, and nothing here is ratified.

## What changed, exactly

- The **length-proxy term is gone**, and gone rather than zeroed: there is no
  `sub["effort"]` and no `CRITERIA` row for it. A criterion scored 0.0 for every item is
  still a criterion, still prints, and still invites the question of why its column is dead.
- **Remaining weight: PROPORTIONAL RENORMALIZATION.** Leaving the five raw weights as-is is
  not an available option — they sum to 0.85, and the build gate refuses a score presented
  as /100 whose weights are not a weighted mean. Re-typing five new absolute weights would
  be re-weighting Dave's criteria under cover of a deletion, and he accepted the ranking
  SHAPE at DC3 in the same export. So the raw ratios **30 : 20 : 15 : 10 : 10** are kept
  verbatim in `_CRITERIA_RAW` and divided by their own sum. Every surviving pair of criteria
  stands in exactly the relationship it did before; only the removed 0.15 left the
  denominator. The division is COMPUTED, never typed.

| Criterion | Weight before | Weight now |
|---|---:|---:|
| Unlock | 0.30 | 0.353 |
| Rot risk | 0.20 | 0.235 |
| Effort (inverse) | 0.15 | **REMOVED** |
| Deadline | 0.15 | 0.176 |
| Risk reduction | 0.10 | 0.118 |
| Decision relief | 0.10 | 0.118 |
| **TOTAL** | **1.00** | **1.000** |

- The **gated optional `effort` FIELD mechanism is intact and untouched**: `_state.py` still
  validates it, `EFFORT_SCORE` still exists, and the page still COUNTS how many items carry
  one. What no longer exists is a code path that READS it into the score. If a real `effort`
  value lands, whether and how it re-enters the ranking is a **design question for Dave** —
  the field is left unread on purpose.

## Control — the delta is attributable to the effort removal ALONE

Baseline sub-scores were captured from the pre-edit module and re-derived after. For all
**33** ranked live items, every surviving criterion (`unlock`, `rot`, `deadline`, `risk`,
`load`) is **bit-identical to baseline — 0 rows of drift** — and `effort` is absent from
every sub-score dict. Same store (`_state.json` byte-identical, unmodified by this lane),
same session (`168`), same item population (33 before, 33 after), zero overrides in both.
The only inputs that moved are the ones DC2 named.

## Movement summary

- 33 ranked rows · **4 unmoved** · mean absolute move **3.88** places · largest move **21**.
- Scores compress: the top score falls 35 → 29, because the removed criterion was scoring
  near 1.0 for most items (short bodies) and was quietly acting as a **flat bonus** rather
  than a discriminator. Removing it does not just re-rank — it reveals that ~13 points of
  every item's score was body length.
- Biggest risers are long-bodied items the proxy had been punishing for being well
  described: `W-08` (+21), `W-0b` (+17), `W-10` (+7).
- Biggest fallers are short-bodied items the proxy had been rewarding for saying little:
  `G6` (8 → 18, −10), `G2` (6 → 15, −9), `G4` (7 → 16, −9), `G15` (4 → 12, −8).

⚠ That direction is the point of DC2: under the proxy, **writing more about a job lowered
its priority**. Nothing about the fallers got less important; they stop being paid for
brevity.

## Full table — new rank order

| Item | New rank | Old rank | Move | New score | Old score | Title |
|---|---:|---:|---:|---:|---:|---|
| `W-0b` | 1 | 18 | +17 | 29 | 33 | ★★ ENCODE BEFORE THE WAVE |
| `W-10` | 2 | 9 | +7 | 29 | 34 | ✅ PER-GATE TEST PLAN |
| `W-05` | 3 | 1 | -2 | 25 | 35 | Instrument-fit remainder |
| `W-06` | 4 | 2 | -2 | 25 | 35 | ds-016, UNRULED |
| `W-08` | 5 | 26 | +21 | 25 | 24 | STILL OWED, unchanged, none superseded |
| `G1` | 6 | 3 | -3 | 24 | 34 | Worklist-index cap DOFIRST_INDEX_TK_MAX = 700 (_capture_gate.py:1403,… |
| `G10` | 7 | 10 | +3 | 24 | 33 | The "70%/95%" stray band (GM:36 |
| `G11` | 8 | 11 | +3 | 24 | 33 | DS-018 recessive value |
| `G12` | 9 | 12 | +3 | 24 | 33 | Charter §4b tone-of-voice temperature map, PROVISIONAL 2026-07-02… |
| `G13b` | 10 | 13 | +3 | 24 | 33 | menu-search combined glyph, PROVISIONAL 2026-07-16 (_ICON-GAPS.md; the |
| `G14` | 11 | 14 | +3 | 24 | 33 | Icon-button dark bindings |
| `G15` | 12 | 4 | -8 | 24 | 34 | DV-D13 donut centre figure + st.visible[id]=true release wiring… |
| `G16` | 13 | 5 | -8 | 24 | 34 | The _proforma/_DATAVIZ-DECISIONS.md:567 enactment call (agent's, not… |
| `G17` | 14 | 15 | +1 | 24 | 33 | RAG status manifestation… |
| `G2` | 15 | 6 | -9 | 24 | 34 | TAPE_TO_BILL = 1.57 at n=2 (_capture_gate.py:371; RATIO_FIRM_N = 4 per |
| `G4` | 16 | 7 | -9 | 24 | 34 | GM §C measured 191 > 150 warn cap (_capture_gate.py:2864,… |
| `G5` | 17 | 16 | -1 | 24 | 33 | Four advisory size caps as a set (_capture_gate.py:4843–4858 |
| `G6` | 18 | 8 | -10 | 24 | 34 | DEFER_STREAK = 6 (_gm_usage.py:353) + USAGE_HISTORY_BLOCKING = False |
| `G9` | 19 | 17 | -2 | 24 | 33 | ds-023 re-measurement programme |
| `W-01` | 20 | 19 | -1 | 21 | 32 | ds-018 C2 follow-through |
| `W-02` | 21 | 20 | -1 | 21 | 32 | dv-legend/dv-behaviour CEILING |
| `W-09` | 22 | 21 | -1 | 21 | 30 | DELEGATION TOPOLOGY, UNSCOPED |
| `W-11` | 23 | 22 | -1 | 21 | 28 | THE 2c-ROLL / INDEX-VOCABULARY DEADLOCK |
| `W-03` | 24 | 23 | -1 | 14 | 26 | ds-012(b) gutter-relative plot area |
| `W-04` | 25 | 24 | -1 | 14 | 26 | DV-D16 floating growth |
| `W-07` | 26 | 25 | -1 | 14 | 26 | ds-017, UNRULED |
| `W-12` | 27 | 27 | — | 14 | 24 | THE #57 1b DOSSIER |
| `W-13` | 28 | 28 | — | 14 | 22 | /tmp RUNBOOK EXPOSURE, UNFIXED |
| `W-0c` | 29 | 29 | — | 13 | 19 | NEXT BUILD CANDIDATES |
| `W-0d` | 30 | 31 | +1 | 13 | 18 | ✅ THE #67 ENACT WAVE |
| `W-14` | 31 | 33 | +2 | 13 | 14 | ⬛ DAVE'S FOUNDING PRINCIPLE |
| `W-16` | 32 | 32 | — | 13 | 18 | UNHOMED PAIR, copied up at the #78 2c EXIT CHECK |
| `W-15` | 33 | 30 | -3 | 9 | 19 | LEDGER § ★ #59 |