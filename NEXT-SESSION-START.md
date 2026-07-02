# Session-starter prompt — paste this into a fresh chat

> Copy everything in the block below into a new conversation to bootstrap it cleanly.

---

Title this chat: North-star mock — the front end as a goal list

We're building the Smart Design System's north-star front-end mock (Promenaut).
Before anything, read MEMORY.md, then in the UX-design folder:
GOOD-MORNING.md · docs/decisions/ADR-0005-ratify-knowledge-engine-pivot.md ·
README.md (rewritten 2026-07-02) · REVIEW-2026-07-02-critical-regroup.html (the
standing review — exec summary is enough). Don't re-derive what's recorded.

THE TASK — one screen, one day, fenced as VISION (not a build backlog):
a mock of the tool's front end in which **every region maps to an engine
capability that exists or is named**:

1. Brief in (+ research attachments) — the intake surface
2. Criteria contract — the definition-of-done the user agrees BEFORE generation
   (it becomes the gates)
3. Register spread — N generated variants side by side (sober → balanced →
   expressive), same fixed curbs
4. Gate report — blocking results (a11y, contrast, tokens, icons) + advisory
   signals (heuristics, CX, states), tiered exactly as the engine tiers them
5. The taste call — the ~20-second human decision, framed as evidence + diff +
   A/B, never a blank canvas
6. Promote — winner enters canon; show what "judgment spent once" looks like

METHOD: sketch as a single HTML file (Swiss or canon styling, Dave's call at
kickoff). The point is GOAL SETTING: any region we can't map to a real or named
capability is a gap in the goal list — log those gaps explicitly at the bottom
of the file. Dave drives the layout; render + look before showing (his rule:
present live HTML, not PNGs).

DON'T: build components, touch the canon, or start the tool shell. This is the
"define just enough target" artifact from the 2026-06-20 strategy lock.

WAITING ELSEWHERE (don't pick up unless Dave says so): calibration project
materials (colleague), token-provenance ruling (ADR-0005 open item, Dave),
Q3 primary customer call (Dave, after the calibration run).
