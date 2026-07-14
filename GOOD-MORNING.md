# Good morning, Dave ☕

*Session briefing — written end of 2026-07-14, session "Presentations + housekeeping: designer pack,
sponsor deck, Apollo rename, red-rule fix, restructure, repo map." Read this, then `_LIVE-STATE.md`
(LIVE + OPEN), then pick the next session's focus from the queue below.*

## The session in one line

A big deliver-and-tidy day: shipped the designer skill pack + a clean handover zip, finished the
review toolkit, built the Apollo sponsor deck (Lisa loved it; PPTX ported), renamed the project
Promenaut → **Apollo**, corrected the red rule, restructured the repo for human-readability, and
built an interactive repo map. Everything committed **and pushed** (origin/master = b08c96e).

## What landed this session

- **Designer pack ready to hand over.** `designer-skills-v1/` = 4 skills + built KB (839 files),
  packaged as **`Apollo-designer-skills.zip`** (938 KB, build script stripped, no stale name).
  Delivery = Agent Skills for VS Code + GitHub Copilot; **no Python needed for v1**.
- **Review toolkit complete** (`review-skills/`): review-dossier (Technical/Standard — Standard
  reframed to reading-level ~16, tech-literate-but-not-AI-native), component-review (light+dark
  gallery + before/after diff mode), swiss-design-system.
- **Sponsor deck** — `reviews/PRESENTATION-2026-07-14-apollo-sponsor.html` (+ `.pptx`). Balanced
  narrative, **craft-over-build** hero, honest-footing slide. Lisa: "loved it as is."
- **Apollo rename** — Promenaut → Apollo repo-wide (51 files + 3 renames); "Smart Design System"
  descriptor dropped → "Apollo". archive/ included. Commit be3c364.
- **Red rule corrected** — red = the **PRIMARY-action accent, used once per screen** (NOT
  destructive-only). Charter §4 superseded; BRAND-1 gate rewritten. Commit f8e05e5. Memory:
  `apollo-rename-and-red-rule-2026-07-14`.
- **Restructure** — root cleared to operating essentials; `reviews/ notes/ projects/` created;
  README repo-map refreshed; cross-refs fixed. Commit 70d38f6.
- **Interactive repo map** — `docs/repo-map.html` (+ artifact). Swiss node-map: hover to trace
  dependencies, click for detail, filter by layer.
- **Teams intro** finalised — `notes/designer-pack-intro-teams.md`.

## On your desk

- **Send the designer intro (for ~the 20th):** attach `Apollo-designer-skills.zip`, paste
  `notes/designer-pack-intro-teams.md`. Confirm the exact Copilot skills-folder path with the team.
- **NEW working-model rule (2026-07-14):** deliverables land straight to the live repo via the
  desktop bridge *as they're made* — not cloud scratch. Memory: `working-model-cloud-vs-device`.
- **Git:** keep **GitHub Desktop CLOSED** while Claude commits — lock contention caused friction
  this session (per the git-split rule). Claude commits local; you push via Desktop.
- Everything committed AND pushed; working tree clean.

## Queue next (fresh session — context was getting long, so start cold)

1. **Designer live-fire** — get Lisa to run one skill on her machine before the 24th. The one thing
   we could NOT test, and the only real risk to the release. If it doesn't fire, it's folder placement.
2. **Real calibration test** — the 3 Figma projects; prioritised plan in
   `reviews/PLAN-2026-07-13-calibration-test.html`. The engine's first proper trial on novel work.
3. **"What does the §9 spread actually reveal?"** — still TOP-PRIORITY engine research in
   `_LIVE-STATE` OPEN; a dedicated fresh Opus session. Prep tooling (knowledge-usage trace) already built.
4. **KB edges / knowledge-graph** — your standing thin-edges concern; import W3C ACT / axe-core
   rather than hand-roll (overlay-index, not GraphRAG).
5. Off critical path: sponsor meeting (date TBD), multi-mode + settings UI, ingestion Phase 1 (Sutherland).

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING → `_LIVE-STATE.md`
> (LIVE + OPEN) → then the relevant plan/charter for whichever item you pick.
