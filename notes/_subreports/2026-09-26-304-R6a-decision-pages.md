# #304 Run 6 seat R6a: three decision pages for Tuesday

provenance: 304 · 2026-09-26 (Sat evening) · seat R6a (Opus 5.5) · repo HEAD read-only, no git writes, no git status, no Project memory
status: three pages written, rendered at 1440 and 390, checked by eye and by script. Nothing ruled, nothing in canon or the stores.

## Pages
- `notes/_DECIDE-304-schema-2026-09-26-v1.html` (plan page 1): six questions
- `notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html` (plan page 3): three questions
- `notes/_DECIDE-304-when-rules-2026-09-26-v1.html` (plan page 5, with R5's when-rule questions): six questions

Each: house CSS (both style blocks) and Dave's decisions overlay COPIED from `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` by `notes/_lanes/304/R6a/build.py`. Overlay changes, and only these: page id/title/path; section boxes switched off (`skip` returns true) so there is exactly one box per question plus the whole-page box; the decision target's title reads the `h2` (the question) instead of the first `b`. One CSS line added so the whole-page box spans the footer (`footer .dd-box{flex-basis:100%}`).

## Questions and recommendations
Schema page:
1. Accept part states? Widen the schema, one shape (`states` list + one sentence per state, `"simple"|"full"` kept); legend and filter bar move onto it. The 4 published errors.
2. The other nine errors? Bring all back: data-grid 6 `with` strings to `{slug}` (s251-D6); data-grid `relationships.composes` to the existing `subComponents`; legend provenance `hand-authored` to `code` (#265-C precedent); legend `with/0.when` to a note + `rel: recommends`.
3. Where a part's words come from (45 parts)? A field on the part (label, title, items, rows, trail), not an A2UI Text child.
4. A container? Give Apollo's bento wall a tiles slot (accepts by capability, s140-D1), not A2UI Row/Column.
5. Setting vs slot of the same name (27)? One rule: data is a setting bound to a shape; a slot only holds parts. Sort shown: 16 setting, 7 slot, 4 for his eye (data-grid, lightbox, stepper, tab-bar); the sort is this seat's reading.
6. Beta parts in the PoC catalogue? Yes, all five, marked as proposals, record names each; KPI tile's s182-D2 "haven't decided yet" quoted, not laundered.

Delivery-shape page:
1. Order: hosts first (catalogue + renderer), minted CSS with snippets-as-test second, adapters and emitters parked (F's order).
2. Tripwire for the parked two: a technology team names itself as owner of a consumer (replaces P-277-5's release-cut trigger if taken; ADR-0008 stands).
3. "Build ready" test: hand the PoC dashboard to a cold developer, count edits by kind (the #231 brief's probe).

When-rules page:
1. Two chart-line clauses (`units = same`, `shape = time-series × 1–5-series`): yes. Candlestick case shown with real renders.
2. Chooser reads each part's own answers/shape (variant B): yes.
3. Data grid rule `records ≥ 2 AND needs in (sort, filter, select, edit)`, new field "needs": yes.
4. Bento ground: yes, in light mode: page and title area white, bento section lightest grey; dark leg stays open. Shown side by side, real template.
5. Own size: a proposed rule plus a size check against reference renders.
6. Lightest pattern: proposed rule with modal-yields-to split-button/drop-down edges; wording his.

## Findings worth carrying
- The bento clash is narrower than A3/F state. `s219-D3` (4)(5), same day as `s219-D1`, already moved `pageBg` out of the bento grammar (a page decision: white or the light greys) and made `bentoBg` the section ground. Dave's Thursday sentence changes `s219-D1`'s shipped dashboard default (`pageBg=grey`, `bentoBg=transparent`) within `s219-D3`'s rails; it does not contradict `s219-D3`. The dark leg collision (surface/subtle dark = module surface, 1.00:1) is still open.
- Date: the plan calls the full-page grey "the ruling of 22 August"; the store dates `s219-D1` 2026-08-25. The page uses 25 August.
- The schema already has `subComponents` (object or array), so the data grid's `composes` needs no schema change.
- A2UI's own basic Button takes its words as a Text child; the page says so on option B of question 3.
- With the two clauses, the rules-only chooser picks 19/20 in R5's what-if; the 20th is W18 (data grid, no rule).
- R5 decision 6 (reduced-motion clause blind on composed pages) is not on these pages; it belongs with the MCP decisions. Named in the schema page's footer.

## Specimens (copied, never redrawn)
`notes/_lanes/304/R6a/specimens/*.png` by `specimens.py`, screenshots of `knowledge/snippets/*.reference.html` at Dave's seat (Playwright, `RENDER_SHELL`, `goto file://`, seat fonts). Stated overrides: bento shots hide the demo bar; `bento-his-top.png` adds three style lines (page white, header white, `main.tpl-page` on `--wall-ground`) in the render only; `chart-line.png` has `dv-fit-on` removed (the JS-off height; with fit on the figure grows to about 1,100px tall); the modal was opened by clicking its trigger. `survey/` holds the first full-page survey shots.

## Render checks
`notes/_lanes/304/R6a/render.py` (builds then renders): all six renders scrollWidth equal to viewport (1440, 390), 0 elements past the right edge, 0 clipped overflow boxes, 0 broken images, 0 page errors; boxes 7/4/7 (questions + whole page). Shots in `notes/_lanes/304/R6a/shots/` (full, sliced, and 390 contact sheets). Looked at by eye at both widths. Page text uses the house Helvetica stack, as the v2 proposal page does; the specimens carry the real face.

## Not done
No schema, meta, store or canon change. No commit. No verifier (the plan puts Fable on pages 1 and 3). The 27-name sort and the proposed wordings (questions 5 and 6 of the when page) are this seat's drafts.

## Files for the commit seat
`notes/_DECIDE-304-schema-2026-09-26-v1.html`, `notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html`, `notes/_DECIDE-304-when-rules-2026-09-26-v1.html`, `notes/_lanes/304/R6a/` (build.py, render.py, specimens.py, survey.py, page-*.src.html, specimens/, shots/, survey/), this report.
