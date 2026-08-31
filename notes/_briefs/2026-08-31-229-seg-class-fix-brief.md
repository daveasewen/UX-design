# Brief — #229 seg class-fix (Opus enact sub): four radius-less .seg snippets + the segmented PARTIAL group

**Dave's words at #229, banked verbatim — the contract:**

> "This looks perfect. 1. lets get this fixed 2. fix the class the other solution is a patch
> not a solution. Wrap"

Item 1 = the four radius-less `.seg` snippets found by the eye-repairs sub (report
`notes/_subreports/2026-08-31-229-eye-repairs.md`, its "found NOT touched" item):
`View-options`, `Template-dashboard`, `Template-list-index`, `Template-report` — their whole
segmented control is square in every theme including console. Item 2 = the M-band structural
fix that report priced: the **segmented PARTIAL group**, chosen by Dave over the S-band
validator, which he called a patch.

## Item 1 — the four snippets

- Read the eye-repairs report §F1 first — the fix pattern is established there (bind to the
  same minted local the thumb uses, on the BASE rule so focus inherits; source snippets, never
  generated files). Mirror it exactly; this is the same class the #227 A1 sweep missed.
- Sweep for a FIFTH instance while you are in there — the finding was "missed by the sweep",
  so re-run the sweep logic across ALL snippets and state the count you checked.
- Full ordered regen serial after: `gen_radius_derive · gen_snippet_tokens ·
  canon/gen_canon_tokens · canon/gen_canon_components · canon/gen_theme_cascade · gen_showroom
  · gen_component_partials`.
- Prove: assert-mint-style table (all four themes × four scales, hover included) + your EYE on
  a render of at least console light+dark for each of the four snippets.

## Item 2 — the segmented PARTIAL group (the class fix)

- The eye-repairs report priced this as the structural fix; read its pricing section and build
  THAT — a `segmented` partial group so segmented-control styling has ONE source and a member
  snippet cannot drift from the minted radii. Follow how existing PARTIAL groups are built
  (`gen_component_partials` in the serial — study its existing groups before adding one).
- ⛔ An instrument without a consumer is a zombie: the group must be WIRED so the regen serial
  actually enforces it, DRIVEN on the real tree, and MUTATION-PROVEN — plant a radius-less
  .seg in a scratch copy and show the machinery catches or regenerates it; then show the real
  tree passes. A gate/generator that has never failed has never been tested.
- RCA discipline (`s228-D7`): the permanent fix is this group; say in the report what class of
  future drift it closes and what it still cannot see.

## Regions you own

Source snippets (the four + any fifth found), the partial-group machinery under
`knowledge/_render/` (or wherever `gen_component_partials`'s groups live — follow the existing
pattern), regenerated outputs from the serial, and
`notes/_subreports/2026-08-31-229-seg-class-fix.md`. Nothing else. No git operations, no
`_rulings.json`, no W-rows, no memory, no `_build_all.py`, no release machinery, no review
pages (Dave has ruled off v2; #230 presents your work fresh).

## Render-verify

Recipe receipted in `notes/_subreports/2026-08-31-229-eye-repairs.md` (mount-side rebuild,
~4 calls; the env does NOT persist between sessions/calls). All exports + `TMPDIR=/dev/shm` in
the SAME call; `set_content()` banned — `goto("file://…")`; ⚠ `full_page=True` silently drops
a synthetic `:hover` and reads as a failed fix (first-hand, that report). Look at your PNGs.

## Pitfalls — replayed

- Nothing survives a tool-call boundary (~178s wall); everything mount-side.
- An alias-repoint can strip a theme override SILENTLY; a dangling var renders SILENT BLACK.
  After regen, grep that the console override survived.
- The regen serial order is the trap — ramp first, index last, whole serial per wave.
- Sandbox can't `rm` — `mv` aside.
- Green regen ≠ proof: the table + your eye + the mutation drive are the proof.

## Report + stub

Report: RCA, what changed (files/rules counts), the sweep count, the mutation-drive receipt,
assert table, SEEN-state light+dark per snippet, UNPROVEN declared, RULING-SHAPED undecided,
REPLAY-THESE, wrap-handover cost line. Final chat message = STUB: report path, one line per
item (FIXED+SEEN / BUILT+DRIVEN+MUTATION-PROVEN), sweep count, cost line.
