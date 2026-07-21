# 2026-07-21 — worker: designer pack v2 (Apollo-designer-skills-v2.zip)

The parked **"designer-skills-v1 revisit"** queue item, run as a WORKER (conductor live in the other
session — Phase-0 build-out). New files only; no git run; no shared-state writes. Worker protocol per
`knowledge/_RUNBOOK-parallel-conductor.md`, read this session.

## Dave's rulings (in-session, AskUserQuestion, confirmed)
1. **Baked KB, no script in the zip.** His brief ("the shell script… doesn't work for them, so it must
   be included in the pack") = testers can't run the generator, so the *generated KB* ships pre-baked.
   The (fixed) script stays repo-side only.
2. **Refresh the pack's existing 4 skills** — do NOT rebase on the newer root `skills/` versions.

## What landed
- **`designer-skills-v2/build-designer-kb.sh`** — v1's copy-list had gone stale: never shipped
  `canon/type.css` (snippets bind `.t-cm-*` composites post-T-D12) nor `tokens/themes/` (ADR-0011).
  Fixed both, dropped the icon exporter `.py` from the copy, added a PROVENANCE stamp env. Repo-side
  tool; **excluded from the zip**.
- **`designer-skills-v2/knowledge/`** — baked **from HEAD `7071538` (build green 38/38), NOT the dirty
  working tree**, via `git archive` — the conductor's mid-flight edits (canon.css, Button snippet,
  tranches, themes) are untouched and deliberately not captured. 843 files: 40 snippets, 40 metas
  (incl. the two new: Amount-display, Icon-button), canon.css + type.css, tokens + themes registry,
  49 guidelines, 658 icon SVGs, compliance graph. Zero machinery (no .py/.sh).
- **4 SKILL.md refreshed** (surgical, kept lean): generate-from-canon + draft-a-new-pattern gain the
  type-composites rule, Mono-baseline theme framing (#B92F1E status-only, sentence case, square
  corners), real-icons rule; check-against-design-system gains 4 drift classes (raw-type, theme-leak
  w/ registry ownsHexes, invented-icon, case-drift). usability-review unchanged (copied verbatim).
- **`designer-skills-v2/README.md`** — v2; "What's new" block; script mentions removed; "ask us for a
  fresh pack" replaces "re-run the script".
- **`Apollo-designer-skills-v2.zip`** (repo root) — AGENTS.md + designer-skills-v2/ (876 files, **0
  shell scripts**). AGENTS.md = the v1-zip copy, which is HEAD minus the parallel-sessions block
  (verified only diff) — session machinery is the wrong audience for testers.

## Verification (all green, run on the zip stage)
Every path the skills reference exists in-pack · all 9 snippet-used composite classes resolve in
packed type.css/canon.css · sampled JSON parses (registry, graph-index, manifest, metas) · both new
components present · the check-skill's hex claims match `_themes.json` ownsHexes exactly.

## Flags for the conductor
1. **`_themes.json` dangles at HEAD:** it references `themes/apollo-legacy.overrides.json`, which
   exists only as your untracked Phase-0 work. Pack ships the registry only — harmless for testers
   (Mono baseline, `overrideSet: null`), but after the Phase-0 commit a **v2.1 re-bake is 2 commands**
   (script + re-zip) if the override sets should ship.
2. **Reconcile step 2.5:** my dirty paths are exactly — `designer-skills-v2/` (7 files + knowledge/
   tree) · `Apollo-designer-skills-v2.zip` · this receipt. Nothing else is mine. v1 folder + v1 zip
   untouched (version-don't-overwrite).
3. **Memory (conductor to inscribe, per runbook):** update the designer-pack memory
   (`apollo-rename-and-red-rule-2026-07-14`) or add a line — v2 built 2026-07-21, baked-KB-no-script
   model, provenance-stamped from HEAD.

## Proposed §C line
- **Designer pack v2 SHIPPED** (`Apollo-designer-skills-v2.zip`): baked KB from `7071538`, no script
  in zip (Dave's ruling), 4 skills refreshed for type-composites/themes/new drift checks. Follow-on:
  optional v2.1 re-bake after Phase-0 commit to pick up theme override sets.

## Commit state
None — worker made no git operations. All files new/disjoint; yours to fold into the ONE commit.
