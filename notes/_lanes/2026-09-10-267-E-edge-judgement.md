# #267 lane E — edge judgement on the 78 proposed ruling edges (Fable, 2026-09-10)

Brief: `notes/_briefs/2026-09-10-267-edge-judgement-brief.md`. Recommends only; nothing applied, ruled or inscribed.

## DONE
- Extracted the 78 by replicating the mention loop of `knowledge/_build_kg_explorer.py:181-193` read-only (same MENTION_RX, VERB_STEMS, ±80 window, dict-order first match): 284 mentions, 78 with a proposedType — matches the generator's count exactly.
- Read both rulings (`says` + `ruled` + `date` + `status`) for every one of the 78 and judged each.
- Cross-checks: date order (no accepted supersedes/retires/corrects points at a later ruling); both-direction pairs (one: ds-034 ↔ ds-035, kept as #2 only); duplicate pairs with two verbs (none); store corroboration (`s129-D1.superseded_by = s171-D1` backs the #36 reject; `s142-D1.superseded_note_s168_D1` backs #19; s200-D3 status backs #49).
- `reviews/EDGE-JUDGEMENT-267-2026-09-10-v1.html` — swiss idiom, light/dark, TWO-RED LAW (#DA1A00 light / #F6604C dark), ids as text.
- `notes/_lanes/267/E/edge-recs.json` — 78 rows `{n, s, t, proposed, verdict, type, dir, confidence, phrase, tier, reason, flags, s_date, t_date, window}`. `verdict` ∈ ACCEPT / RETYPE / REVERSE / REJECT; `type` is always the FINAL type to inscribe (`mentions` for REJECT); `dir` is `t->s` for the one REVERSE (#40).

## NOT DONE
- No DAVE-verdict edges were needed; instead two vocabulary questions are Tier 3 (Q1 clause-scoped `supersedes`, nine ACCEPTs depend on it; Q2 which node carries a recorded supersession, #41/#42 and #19).
- Generator not fixed (findings below). Missed edges NOT added (not this lane's to add): s171-D1 → s129-D1 (supersedes, from the store's `superseded_by`), s188-D1 → s183-D1 (supersedes P1 clause).
- No render check in a browser (file:// blocked in this session); the HTML was parsed for tag balance (clean, 80 `<tr>` = 78 rows + 2 headers).

## COUNTS
- Verdicts: ACCEPT 26 · RETYPE 20 · REVERSE 1 · REJECT 31 → **52 of 78 wrong if accepted as-is.**
- Tiers: Tier 1 (high) 59 · Tier 2 (medium) 19 · Tier 3 edges 0 (two questions).
- By proposed verb (accept-as-proposed / total): supersedes 10/14 · extends 6/8 · refines 2/3 · enacts 3/12 · confirms 2/8 · corrects 1/5 · retires 1/13 · narrows 1/3 · **overrides 0/12**.

## GENERATOR DEFECTS (findings with line numbers, not fixed)
1. `_build_kg_explorer.py:81` — stem regex has a left `\b` only: `enact` hits "enactment" (#8, #15, #47, #50); `overrid` hits "override sets"/"overrides.json" (all 12 overrides are noun hits); `correct` hits "correctly" (#23); `narrow` hits "NARROWEST" (#32) and a commit subject "roster narrow" (#71); `refin` hits "refinement" (#65); `retir` hits a hex "retired to the note" (#3); `confirm` hits "Dave confirmed" (#54).
2. `:188` — the ±80 window spans neighbouring ids in a list ("s122-D1/D3, s123-D1, s131-D1, s132-D1"): one verb proposed for every id in the list — #13, #25–#28, #37–#39, #56–#57 = 14 edges from four sentences.
3. `:189` — first stem in dict order wins, not nearest to the mention (#16 had three stems in one window; right by luck).
4. `:191` — no direction test: the verb can describe t acting on s (#1) or a third ruling acting on t (#4 "#129", #36 "s171-D1", #41 "s188-D1").
5. `:168` / `:77` — authored, ratified fields are ignored by the derivation: `superseded_by` (s129-D1) and `superseded_note_s168_D1` (s142-D1); MENTION_RX misses the `#NNN-DN` form (12 occurrences in `says`, e.g. ds-034 "Extends his own #107-D1") and the `/D3` shorthand in "s122-D1/D3".

## TOKENS (ESTIMATED)
- Lane FILL ≈ 115K real at the commit (78 edges × both rulings ≈ 70K of reading; build + page ≈ 25K; boot + brief + skill ≈ 20K). Not measured via `message.usage` from inside the lane.
