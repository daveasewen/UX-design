provenance: tender-stoic-clarke · 2026-08-12
status: observed

# Receipt — designer community presentation (worker lane, declared retrospectively)

*Dave opened without a role word; ran as de-facto worker (Cowork session `tender-stoic-clarke`).
Role declared retrospectively by Dave at end of session: "I forgot to declare you as a worker —
leave receipts." Worker rules honoured: NEW files only, no shared-state writes, no commit.*

## What landed

Three versions of an HTML slide deck for the **designer community call (2026-08-13)** — a promotion
piece introducing Memento and Apollo to AI-inexperienced designers, in the sponsor deck's visual
system (accent `#DB0011`, Univers Next, scroll-snap deck, entrance animations, progressive-disclosure
blocks). Sources: `reviews/PRESENTATION-2026-07-14-apollo-sponsor.html` ·
`memento-package/WHAT-MEMENTO-IS.md` (Dave-ratified voice) · `designer-skills-v2/README.md`.
Public-positioning rule applied: copy abstract, no gate/token mechanics.

- **v1** — 12 slides, Apollo + Memento entwined.
- **v2** — restructured on Dave's direction into TWO SEPARATE PRODUCTS (his words: *"lets treat them
  as separate product rather than them being intrinsically entwined, this is my methodology"*).
  Chapters 01 Memento (any project) / 02 Apollo (designers). Added modular building-block diagrams
  (tap-to-expand) and staged process flows for each system.
- **v3** — final. Added on Dave's instruction:
  - Component trajectory stat row: **75 components today → ~135 near future → ~300 horizon,
    "enabling autonomous production for low-risk projects"** (Dave's figures, this session).
  - New slide 13 **"Lovable, on rails"** — final harness: **brief builder + edit mode** (coming),
    plus the four modes A Factory / B Creative / C Component dev / D Explore.
  - "Updates to both systems are coming regularly" in Apollo Now.

## Files touched (all NEW, disjoint)

- `reviews/PRESENTATION-2026-08-12-designer-community-v1.html`
- `reviews/PRESENTATION-2026-08-12-designer-community-v2.html`
- `reviews/PRESENTATION-2026-08-12-designer-community-v3.html`
- this receipt

## Verbatim Dave statements a conductor may want to inscribe (NOT rulings unless Dave confirms)

- Apollo is at **75 components** currently; extension to **~135 near future**, **~300 future**,
  enabling **autonomous production for low-risk projects**.
- Final harness will have an **edit mode and brief builder**, as well as the 4 modes
  ("remember the lovable on rails ambition").
- Memento and Apollo are **separate products**; the shared part is "my methodology".

## Open

- **Dave's eye pass on v3** — render not screenshot-verified in-sandbox (playwright absent this
  session; HTML structure parse clean for all three files). Sign-off queue candidate:
  `reviews/PRESENTATION-2026-08-12-designer-community-v3.html` → propose adding to
  `knowledge/_REVIEW-SIGNOFF.md` (left to conductor; worker did not touch shared registers).
- Flagged to Dave: the ~300/autonomous-production line is the deck's most forward-leaning public
  claim; soften on request before the call.
- v1/v2 retained per version-don't-overwrite; candidates for `_to_delete` after the call if unused.

## Proposed §C lines (for the conductor's GOOD-MORNING merge)

- Designer-community deck v3 READY for the 2026-08-13 call —
  `reviews/PRESENTATION-2026-08-12-designer-community-v3.html`; awaiting Dave's eye pass; not committed.
- New Dave figures in the room: 75 components now, ~135 near, ~300 horizon (autonomous low-risk
  production); harness = brief builder + edit mode + 4 modes. Check against `_LIVE-STATE` /
  ledgers — inscribe or float as appropriate.

## Commit state

**Nothing committed.** All four files are untracked working-tree additions, handed up for the
conductor's single reconciled commit.

Context gauge at authoring: ESTIMATE only — `_checkin.py` refused (tiktoken uninstallable in this
sandbox, declared at session open); believed 🟢/low-🟡 by turn count, unmeasured.
