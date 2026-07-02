# Prompt 3 — Run the UX/UI build & review pipeline on a real example

Paste this once the knowledge layer has enough real components. Fill the blank.

---

Run the UX/UI build & review pipeline on a real example, following
`disciplines/ui-design/pipeline.md` and `disciplines/ui-design/spokes.md`. You act
as the orchestrator and each spoke in turn; I am the human at the gates.

The example to design: **<DESCRIBE one screen or feature — keep it small>**

Proceed step by step, pausing for me at every gate:

1. **Framing** — turn my description (plus any requirements) into a `brief` with
   success criteria. **Pause for Gate A** — I approve or redirect the brief.
2. **Generator** — produce a `design_candidate` using ONLY components and tokens
   from `knowledge/`. If a needed pattern is missing, list it in `open_gaps` and
   stop — do not improvise. Build the prototype as React (preferred) or Figma Make.
3. **Critic (craft gate)** — score it with the `design-system-compliance-check`
   skill. Show me the `craft_review`. If it fails, regenerate. Do not proceed past
   a failing craft gate.
4. **Parallel review** — run all three and show me each:
   - `heuristic-review` skill (Nielsen's 10, severity-rated)
   - accessibility review (WCAG 2.2 AA; each finding cites the SC + EN 301 549 clause)
   - brand review (against the GTB system / guidelines)
5. **Pause for the taste gate** — I review the joined package and approve,
   redirect, or waive a specific a11y finding with a recorded reason.
6. **Handoff** — produce the `handoff_spec` (dev spec + Code Connect mapping +
   prototype) and a rolled-up review summary. **Pause for Gate B** — final approval.

Validate every spoke output against its contract in
`disciplines/ui-design/contracts/`. Keep a checkpoint after each step. At the end,
tell me honestly where the pipeline felt thin or where canon needs more detail.
