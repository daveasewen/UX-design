# #246 lane O brief — the SAME baseline, run by OPUS 5 (the GPT-proxy arm)

**Model: Opus. Conductor: Fable (#246). Dated period record (ADR-0017). Read-only against canon/knowledge — MOVES NOTHING in the library, RULES NOTHING.**

## WHY (Dave, 2026-09-05)

> "Because these results are not dissimilar to VS, this makes me more confident we can test agency-side, this will be much quicker, we need to test with Opus 5, its probably closer in capability to GPT."

Lane B (Fable) ran this brief already: `notes/_briefs/2026-09-05-246-lane-B-baseline-brief.md` — **read it and follow it exactly**, with these overrides:

1. **Output root is `outputs/baseline-246-opus/`** (not `outputs/baseline-246/`). Never write into lane B's folders; never read lane B's dashboards, logs or review before BOTH your arms are frozen — the point is an independent run. You MAY read lane B's review AFTER measuring, for the comparison section only.
2. Review page: `reviews/BASELINE-246-OPUS-2026-09-05-v1.html`. Subreport: `notes/_subreports/2026-09-05-246-O-opus-baseline.md`.
3. Add ONE section to the review, after the scores: **Opus vs Fable** — same tables side by side (inventory, chart completeness, interactions, scores), and the differences named as facts. No verdict on which model is "better"; state what each did differently and what the library did to both.
4. Playwright: lane B installed it in this sandbox already — check `python3 -c "import playwright"` first; if the sandbox is fresh, follow `knowledge/_ROBUSTNESS-PORTABILITY.md`.
5. Do NOT write into `knowledge/` at all, including `knowledge/_screen-gate/` — if a gate insists on writing there, run it with its output redirected or copy the gate's output from stdout; declare what you did.

Same frozen prompt. Same two arms, A blind first and frozen, then B sighted (cap 3 iterations). Same measurements. Same rules: no edits to canon/showroom/skills/snippets/metas, no `_build_all.py`, no commit, no push, no ruling of Dave's questions.

Return: review path, subreport path, both dashboard paths, four scores per arm, top three differences from lane B in one line each, tokens used.
