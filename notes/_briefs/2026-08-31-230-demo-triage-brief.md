# Brief — #230 Lane A (Opus): demo triage of the dashboard-diff findings

provenance: 230 · 2026-08-31 · conductor Fable · row W-312
Context: Dave presents Apollo live in VS Code + Copilot TOMORROW (2026-09-01, row W-308).
Goal: "get to my result quicker" — shrink the ~5 fettling rounds his cold run needed.

## The question, exactly

Of the 25 regen-diff findings and the 32 decision cards, WHICH ones stand between a cold
seat and Dave's fettled dashboard — and of those, which are safely adoptable TODAY?

## Inputs (read, never rebuild)

- `notes/_subreports/2026-08-30-227-dashboard-regen-diff.md` — 25 findings (3 generation
  defects · 14 canon gaps · 8 dave-improvements).
- `reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html` — the 32 cards.
- `notes/_subreports/2026-08-29-224-copilot-forensics.md` § GPT'S CODE — the 8 design files
  modified in Dave's pack copy (`_to_delete/Apollo-Spider-v1.0.2/`): search-field radius,
  chart tooltip re-parenting, dv-title ink. These are ALSO port-back candidates; say for
  each whether it is already answered in canon at HEAD (grep first — some may have landed
  since, e.g. radius work at #227–#229).
- `notes/_briefs/2026-08-31-230-demo-day-brief.md` — the demo frame.

## Output

1. `reviews/DEMO-TRIAGE-2026-08-31-v1.html` — a decision page in the established review-page
   idiom (COPY the shell of an existing reviews/ page, e.g. DASHBOARD-DIFF-DECISIONS —
   specimens copy the approved artefact, never re-draw). Every card graded on ONE axis:
   **reached cold already / adoptable today (priced) / needs Dave's design word / not a
   demo blocker**. The "adoptable today" set is the headline — ordered, each with its
   file-level price and its risk named.
2. Filed report `notes/_subreports/2026-08-31-230-demo-triage.md` with COUNTS:,
   REPLAY-THESE:, and RULING-SHAPED QUESTIONS sections (mandatory even if "none").
   Chat gets a STUB only.

## DO-NOT-RULE

No rulings, no `_rulings.json`, no W-rows, no memory writes, no git operations of any kind,
no canon/snippet/token edits, no `_build_all.py`, no release machinery, no adoption of any
card — this lane produces a DECISION SURFACE; adoption is Dave's, enactment is a later lane.
⛔ Before marking any card "needs Dave's word", grep `knowledge/_rulings.json` for it — the
store trumps every banner and row (#229's declared miss; the grep is owed PER ITEM).

## Pitfalls — replayed (consequences, not vibes)

- A card presented as open that Dave already ruled = the #229 miss repeated; he catches it
  and trust is the cost. Grep the store per item.
- Sandbox: nothing survives a tool-call boundary (~178s wall); tiktoken install FIRST if you
  measure anything; `TMPDIR=/dev/shm`; renders per the mount-side recipe receipted in
  `notes/_subreports/2026-08-31-229-eye-repairs.md` — but this lane should not need renders.
- The two-red law + ink rules are RULED — if the page shows status colours, use the review
  idiom's existing tokens, never invent.
- "Adoptable today" must be priced against the FULL ordered regen serial (ramp first, index
  last) — a change that skips the serial is a patch, and Dave has ruled on patches.
