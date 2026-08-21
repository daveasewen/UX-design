# Routing currency check — amendments applied (P1–P7, P9, P10)

*Session #212, ruled `s212-D12` (Dave, 2026-08-21). Source brief:
`notes/_briefs/2026-08-21-212-routing-currency-check-v1.md`. Target: `MODEL-ROUTING.md`.
P8 deliberately NOT applied — the rule-5/verification-scaffolding conflict is flagged in the brief
as Dave's call, not a sub's; nothing touched.*

All edits made by addition (dated, cited inline as `s212-D12`, 2026-08-21) — no ruled text deleted,
only superseded visibly in place, per the file's own STALENESS-CORRECTED house pattern.

| Proposal | Line(s) / cell changed | What was added |
|---|---|---|
| Header | Line 8–16, `*Last updated:*` | Prepended a new dated entry (`2026-08-21 #212 s212-D12`) summarising all nine applied amendments and naming P8 as deliberately left open; prior entries (2026-07-30, 2026-07-25, 2026-07-23) kept intact below it. |
| P1 | Tiers table, **Premium — rationed** row, Notes cell (line 22) | Appended `claude-fable-5` exact string, $10/$50 per MTok, and the usage-credits rationing mechanism (Pro/Max/Team plans), cited to Anthropic 1 Jul 2026. |
| P2 | Tiers table, **Default — complex** row, Model cell (line 23); staleness note below table (new paragraph, lines 42–47) | Model cell: added exact string `claude-opus-5`. Staleness note: appended a new paragraph confirming the 2026-07-30 correction is now independently corroborated by the 24 Jul 2026 Opus 5 announcement and the live models overview, both fetched 2026-08-21. |
| P3 | Tiers table, **Throughput** row Notes cell (line 24) and **Chore** row Notes cell (line 25) | Throughput: added `claude-sonnet-5`, $2/$10 per MTok, 1M context, cache minimum 1,024 tokens (not 512). Chore: added `claude-haiku-4-5-20251001`, $1/$5 per MTok, 200k context, no adaptive thinking/`xhigh`/`max`, and the retirement watch date (not sooner than 15 Oct 2026). |
| P4 | Fable-era notes, "Diagnose before attributing…" bullet (lines 74–84) | Appended a correction: Opus 5 also ships safety classifiers (refusals-and-fallback page); "route it to Opus" is no longer automatically classifier-free; Anthropic's default fallback target for Fable's `cyber` category is Opus 4.8, not Opus 5 — a diagnosed classifier refusal now routes down a generation, not sideways. Diagnose-first discipline left verbatim. |
| P5 | Same bullet, appended directly after the P4 addition (lines 85–93) | Named the five published refusal categories (`cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`), noted `stop_details.category` reports which fired, and added a freshness warning (cyber classifier tightened 1 Jul 2026, biology relaxed 7 Aug 2026, ~85% fewer bio fallbacks) — rates are stale within weeks, category names are the durable part. |
| P6 | Fable-era notes, "Effort is a real second axis…" bullet (lines 59–73) | Appended the corrected five-rung ladder (`low·medium·high·xhigh·max`), noted `high` = API default = omitting the parameter, cited the new `build-with-claude/effort` page, and gave per-model guidance for Fable and Opus 5 (including the "run a fresh effort sweep" quote for Opus 5). The 2026-07-23 OBSERVED Cowork-knob line and the 2026-07-24 correction above it were left untouched. |
| P7 | "How it runs in practice," Mode 3 anti-pattern sentence (line 159) | Broadened "never switch model mid-session" to "never switch model or effort mid-session," with the officially documented effort-cache-invalidation quote from `build-with-claude/effort`, fetched 2026-08-21. |
| P9 | "How it runs in practice," Mode 2 bullet (lines 150–158) | Appended a note that the Opus 5 prompting guide's delegation guidance ("delegate only for large, genuinely independent, parallelizable tasks… keep spawn counts low") independently corroborates the existing Mode 2 ruling, since Opus 5 is Dave's Default tier — while the Fable guide pushes the opposite way. Ruling text left standing, unchanged. |
| P10 | Fable-era notes, new bullet appended after the "Fable is now a spawnable subagent target" bullet (lines 97–105) | No verbatim tokenizer-overhead line existed in canon to correct in place, so this was added as a new dated bullet: the migration guide contradicts the ~30% Verdent practitioner figure as a Fable-vs-Opus-4.8 delta (same tokenizer); the real ~30% figure is the pre-Opus-4.7 tokenizer delta, already absorbed. Fable's true premium over Opus 4.8 — and over Opus 5 — is 2× per token, nothing more. |

## Not applied

- **P8** — untouched, per brief instruction. Rule 5, rule 6, and the "Worked pattern" section's
  rule-5 reference (lines 109–114, 175–176) carry no edits. The three-reading question on
  verification scaffolding remains open for Dave.

## Not touched

No file other than `MODEL-ROUTING.md` and this receipt was modified. `_build_all.py` was not run.
No git operations were performed.
