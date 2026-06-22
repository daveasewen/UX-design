# Session-starter prompt — paste this into a fresh chat

> Copy everything in the block below into a new conversation to bootstrap it cleanly.

---

Title this chat: HSBC Table → 9/9

We're continuing the HSBC Common Toolkit component-refinement work (Promenaut).
Before anything, read MEMORY.md and these files in the UX-design folder:
GOOD-MORNING.md, knowledge/_RUBRIC-prototype-grade.md, knowledge/_PROTOTYPE-GRADE-AUDIT.md.
Don't re-derive what's already recorded.

WHERE WE ARE: the component-review program is running. THREE components at 9/9 — Tabs,
List-items, Status-indicator. Build green, working tree clean.
- Rubric decision A is LOCKED: a meta may set "interactive": false; the scorer then credits AT via
  role/aria-live/label instead of a keyboard handler (a passive component exposing nothing still
  scores 0). Flagged passive: Status-indicator, Divider, Badge, Loading-indicator.
- Code↔design naming is hub-and-spoke (codeBindings spokes; Figma node id = identity; never guess
  code names) — see _RUNBOOK-onboard-code-library.md.
- Atom-reuse web: List-items reuses Avatar + Tags + Loading-indicator + Status-indicator (its RAG
  tint chip IS the List-items status detail).

TODAY — Table (★, 6.5/9). DECIDE ONE THING BEFORE BUILDING:
The canonical Table (table.meta.json) is a STATIC semantic data table — props headerType /
orientation / cellAlign; NO sort, NO selection. Its a11y is scope/caption/reflow (1.3.1, 1.4.10),
NOT role/aria/keyboard — so the rubric's AT signal doesn't fit (same shape as the passive-atom
question we just solved). Pick:
  (a) treat Table like interactive:false — credit semantic-table AT (caption + th scope + a
      focusable scroll container, role=region + tabindex + aria-label), OR
  (b) build it interactive — sortable <th> buttons + aria-sort + a keyboard handler.
Then build to standard. Gaps to 9/9: states (0.5), AT (0), responsive (0 — overflow-x:auto is NOT
counted; add a real @media/container reflow). table/* tokens are already clean.

THE METHOD (per component): refine in _fitness-test/ (never gated) → I review visually → promote
into snippets/*.reference.html → rebuild green (cd knowledge && python3 _build_all.py). Pull the
real component from Figma (fileKey mI8hvIkV98nquoqWzKh5Kn, get_design_context/get_screenshot; Table
node 547:22693) + real icons from knowledge/assets/icons; reuse canonical atoms. KEEP CANON SIMPLE.

SCORER CHEAT-SHEET (_build_prototype_grade_audit.py, 9 signals): responsive needs ResizeObserver /
matchMedia / container-type / @container / @media min|max-width. states needs >=4 of :hover /
:active / :focus-visible / :disabled / aria-(selected|checked|expanded|current). AT (interactive) =
role + aria + keydown; AT (passive, meta interactive:false) = role / aria-live / aria-label.

WORKING RHYTHM: present files for my visual review; nothing enters canon without my go-ahead; green
build = done; flag reflection checkpoints; commit on my prompt with a paste-ready git summary; write
GOOD-MORNING.md when we wrap; and ALWAYS open the next-session prompt with a short, distinct
"Title this chat: …" line (the recents list needs a clean, specific name — not a generic phrase).

PARKED: Figma dark-mode port (task #19); rag/neutral-tint token gap; the dark hover / text-secondary
$darkFinding (3.34:1, systemic). Full-RAG List-items is DONE.

Start by reading the context files + confirming the build is green, then give me the Table AT
decision (a or b) before building.

---
