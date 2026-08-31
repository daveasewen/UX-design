# Brief — #230 Lane B (Opus): the four fixed seg snippets, rendered for Dave's eye

provenance: 230 · 2026-08-31 · conductor Fable · row W-313

## The job

W-307's close condition owes Dave a look at the four snippets its lane fixed but he never
saw (they landed after he ruled off v2): `View-options` · `Template-dashboard` ·
`Template-list-index` · `Template-report`. Plus the two reasoned `$exempt` members he must
rule on: `Table.reference.html` (demo-harness switcher) · `Tab-bar` (mobile pill, 999px).

## Output

1. `reviews/SEG-SNIPPETS-2026-08-31-v1.html` — the four snippets rendered live (COPY the
   approved artefacts/snippets into the page's iframes or embed per the FOUR-VISUALS pages'
   established pattern — never re-draw), console light + dark minimum, with the `$exempt`
   pair shown as they stand and the join/stay/restyle choice laid out as a decision card
   each. Real `:hover` driven where radii are the point.
2. PNG evidence per the receipted recipe; LOOK at your PNGs.
3. Filed report `notes/_subreports/2026-08-31-230-seg-snippets-eye.md` with COUNTS:,
   REPLAY-THESE:, RULING-SHAPED QUESTIONS. Chat gets a STUB.

## Render-verify (the hard-won recipe — follow, don't re-derive)

Receipts: `notes/_subreports/2026-08-31-229-eye-repairs.md` §render + the seam findings in
the #229 banner ⑭. Mount-side everything; env survives on the mount, `/dev/shm` and sandbox
home DIE between calls; `TMPDIR=/dev/shm` exports in the SAME call as the run;
`set_content()` BANNED — `goto("file://…")`; ⚠ `full_page=True` silently drops synthetic
`:hover` — assert `el.matches(':hover')` before believing an image; `page.screenshot(clip=…)`
clips in VIEWPORT space unless `full_page=True`; the `chromelibs` path has NO `root/`
segment; `apt-get download` is broken — `curl` the deb + `dpkg -x` if needed; fonts farm on
the OUTPUTS mount; canvas probe not `fonts.check()`. ~178s call wall — drive steps
individually. tiktoken first if anything measures.

## DO-NOT-RULE

No rulings, no `_rulings.json`, no W-rows, no memory, no git operations, no snippet/canon
edits (the fixes are DONE — this lane only shows them), no closing/rewording W-307, no
release machinery. Decision surface only; the exempt-pair choice is Dave's.

## Pitfalls — replayed

- Hand-rolling a specimen invents defects the eye then wrongly rules on — copy the artefact.
- A dangling dataviz var renders SILENT BLACK; if a page section comes out black, suspect
  the var chain before the snippet.
- Light/dark + the four themes are the requirement when a treatment varies per theme; here
  console light+dark is the minimum, mono if the page touches it.
