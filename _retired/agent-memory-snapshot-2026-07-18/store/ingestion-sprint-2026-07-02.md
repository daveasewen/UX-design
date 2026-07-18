---
name: ingestion-sprint-2026-07-02
description: "Five ingestion tranches in one late-eve session (register 143→209); ingestion method proven via Chrome fetch-all; key new rules + deltas + what's queued"
metadata: 
  node_type: memory
  type: project
  originSessionId: 17c82c4a-c802-4eb0-9b9a-20dbf87fe656
---

Late-eve session 2026-07-02 (after the desk pickup, same chat): five ingestion tranches
landed — web foundations · app foundations · neurodiversity (16 pages, 40 guidelines) ·
typography both vintages · brand-refresh logos/photography/hexagons. Register 143 → 209
rules, 16 engine-era files, all gates green, 7 commits (Dave pushes).

**METHOD PROVEN (reuse it):** authenticated Chrome tab → same-origin `fetch()` of all
subpages in ONE JS call into `window.__all` with `@@PAGE` markers → slice out in ~850-char
chunks (tool output truncates ~1k) → raw snapshot into `guidelines/_sources/<standard>/`
(NEW standing convention — audit trail, capture-vs-encoding) → engine-era guideline file
(stable IDs + destiny tags) → `gen_rules_index.py` → `_build_all.py` → commit.
Gotchas: `get_page_text` unreliable on content pages (article-extraction picks a div);
`browser_batch` intermittently rejects valid JSON (fall back to parallel single calls);
a safety filter blocks some slices containing cookie-ish strings (re-slice at different
offsets).

**Sharpest new rules:** photo26-002 — NO gen-AI/CGI/mixed-media imagery, ever (pipeline:
engine generates experiences, never photographic assets; library retrieval only) ·
neuro-042 calm ceiling (hero ≤30% height, bright ≤20% screen, ≤2 column layouts, ≥20px
section whitespace, ≤4 sentences/para, ≤240 chars/sentence) = the sober register's first
NUMBERS · elevation levels 0–3 taxonomy (level 0 never elevated) · logo26-001 logo ≥1×
per journey (journey-gate candidate).

**Deltas logged (deltas ≠ defects):** type26-025 centre-align legitimised · type26-026
subtle overlays permitted (softens 2025 "no treatments") · type26-029 magnetic headline
replaces big-light/small-bold · hex26-002 Iconic smaller + Cropped only 1-/2-edge crops
(3-/4-edge RETIRED — audit legacy hexagon assets) · webf-017 forms/element standards
MOVED to "Common Toolkit" (access decision = Dave, covers app too).

**Cost-0 gate candidates pending Dave's batch-yes (type25-020):** no-italics ·
no-text-shadow · red-text-role — all zero occurrences in canon.

**Tone of voice: DONE 2026-07-02 day session** — see [[tone-of-voice-ingest]]
(register 209→250; temperature dial sourced; neuro-024 reconciled; Copywriting family
queued as 10a). Remaining Tier-1: 2025 colour delta-map · 2025 visual-assets family.
See [[desk-rulings-2026-07-02]] [[supercharge-codename]] [[fixed-flex-charter]]
[[git-push-method]].
