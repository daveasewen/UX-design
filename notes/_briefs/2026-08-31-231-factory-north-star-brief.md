# #231 BANKED — Factory mode's north-star question, Dave's words verbatim

provenance: #231 · 2026-08-31 · chat, banked same turn. Row W-329. Status: BANKED, nothing ruled.

## Dave, verbatim

> "In Factory mode, which is the foundation of Apollo and what we are working towards right
> now, there should be a fidelity to the UI and to code that can go straight to a dev team
> to build, how that is delivered is unsure now, is it a set of HTML, do we design with
> react components, do we deliver a 'translation' file, is there a transformation layer.
>
> It seems to me the simplest and most mechanical version is designing with built ready
> components that flex against rules and rails that are predefined, but i dont have all the
> answers. We'll have to work through this together.
>
> The question we need to answer is, 'is the code it produces useful to a dev team, is it
> build ready?'"

## Reading (conductor's, declared — NOT a ruling)

- The north-star question is CHECKABLE: "build ready" = a cold dev seat ships the output in
  their stack without re-drawing; measured by logging edit CLASSES + counts on a real output.
- The four delivery shapes differ in where they put the PARAPHRASE SEAM (the v1.0.2 finding
  generalised): HTML set → seam at the dev desk; translation file → second source of truth,
  rots unless generated; transformation layer → a generator, biggest build; built-ready
  components → no seam, output is instantiation. Dave's stated leaning is the last — a
  LEANING, explicitly not ruled ("i dont have all the answers").
- Honest gap named before any shape hardens: canon today = markup + tokens; no state,
  behaviour, or data-binding contracts — most of what a dev team builds.
- Proposed probe (post-demo, W-308 first): dev-seat edit-class measurement on the demo's own
  dashboard output; real colleague preferred, cold sub = declared approximation. The #231
  detector (`_detect_retrieval.py`) generalises into the fidelity gate for whichever shape wins.

## Open, Dave's

Whether this becomes a named programme scoped after the demo · the delivery-shape ruling
itself (only after the probe) · whether a visual decision surface (four shapes, seams marked)
is wanted first.
