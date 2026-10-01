# #313 lane AC3 — inscription of Dave's two exports, and the eight reviewed flips (Opus seat lane, the single committer)

COUNTS: rulings inscribed 48 (s313-D1..D48, store 865 → 913), one per call · cohort one 19 (calls 2..18c, all on the recommendation) · pictures 29 (calls 1..29; 27 on the recommendation, call 5 no option picked, call 10 not the recommendation) · stamped enacted 10 (D1, D3, D7, D8, D11, D12, D14, D15, D16 at d1710e4c; D44 at b6a7fb4b) · reviewed flips 8 of 15 (seven left false) · Dave-owned rows opened 4 (W-313d1..d4) · rows closed 8 · rows noted 8 · commits b6a7fb4b (inscription), d1710e4c (flips), then the stamps-and-report commit.

Thu 2026-10-01 evening, Opus 5.5, Dave's seat. Authority: his 17:52 BST export of `notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html` (completing the 16:59 partial, which left calls 2 and 3 not answered) and his 17:49 BST export of `notes/_REVIEW-312-F-the-pictures-you-are-owed-2026-10-01-v1.html`, both saved verbatim under `notes/_lanes/313/` and committed in b6a7fb4b with the 16:59 partial as provenance.

## 1 — Method (AC0's route at #312, lane R's at 2fbc8184)
One entry per call at `notes/_lanes/313/AC3/s313-D{1..48}.entry.json`, built by script from the exports and the page HTML so nothing is retyped: `ruled` = a short headline, then the page's recommendation lifted verbatim from the call's question paragraph (cohort page: the `p.q` with its "Recommendation:" span; pictures page: the `p.q` and the `p.rec`, plus the section headline on single-call sections), then what he chose verbatim, then his comment verbatim or "comment: none". Where a comment spans two lines (pictures call 5), `says` marks the break with " / " and `ruled` joins with a space. Each entry `--dry-run` (reconstruction proof) then `--write` via `knowledge/_inscribe_ruling.py`. `gen_kg_titles.py --write` (913 titled, 0 untitled) and `_render_rulings.py` (913 rulings, 171 sessions) re-run and committed with them.

## 2 — The rulings
Cohort one (17:52): D1 menus = split button, select = dropdown · D2 button Change it · D3 tabs Yes · D4 table Change it · D5 date picker Change it · D6 metric Change it · D7 split button Yes · D8 accordion Yes · D9 slider Change it · D10 switch family Change it · D11 text input (input-fields) Yes · D12 select (dropdown) Yes · D13 dialog (modals) Change it · D14 tooltip Yes · D15 pagination Yes · D16 notification Yes · D17 plain words set by hand per part · D18 each part's own rest word, initial names it · D19 each piece carries its own states (phase 2). Every Change it was chosen with no comment, so each `ruled` says the change is the page's recommendation as written.

Pictures (17:49): D20 section and panel, drop division and sector · D21 nav family is frame · D22 top nav default frame, mega menu for levels · D23 six links the flyout line · D24 third level in the lock-up's tabs, INSCRIBED FOR NOW at his word (no option picked; status says so; W-313d1) · D25 side nav for the workbench only · D26 elevation border on floating surfaces, BOTTOM EDGE ONLY (his comment) · D27 list rule option 1 (natural-order comment → W-313d2) · D28 lock-up option 2 for now (future work → W-313d3) · D29 bento group header B as the default, A an option for the designer (NOT the recommendation, which was A) · D30 two linked subjects as one group, as a variation · D31 ring upper band 280px · D32 the stacked-ring cap · D33 fifth ground word, section · D34 section ground on every bento wall · D35 dark roundels follow the ink · D36 surface/section accepted · D37 notification/contextual/border/alpha accepted · D38 Mono hero sub-line takes the ink · D39 outline border follows the ink · D40 keep terms · D41 keep the four tile kinds · D42 Tabs fills the container · D43 square-corner token · D44 the 4.36 MB evidence folder left as filed, question closed · D45 showroom focus ring bound to the library's token, triggered only by tabbing, not clicks or taps (his comment) · D46 keep and regenerate the canon gallery · D47 runbook index shows the newest runbook change's date · D48 fallback colours follow the base theme, light.

Status: all `ruled` except D1, D3, D7, D8, D11, D12, D14, D15, D16 (enacted at d1710e4c, the reviewed flips) and D44 (enacted at b6a7fb4b, W-307qp closed by it). `s311-D4` is NOT stamped (seven trees pending).

## 3 — Dave-owned open items (store rows, live, owner dave, close conditions in his words)
- W-313d1 — where the third level lives: revisit against his nav strategy doc. Closes when he has checked it against that doc and ruled again or said it matches; his words: "I do have a nav strategy worked out in a sigma file, inscribe for now but I will revist if this doesnt match with the doc." His stated preference: "introducing a simple side nav at this point".
- W-313d2 — is it also a list when a natural order is assumed (transactions in date order). Closes when he has ruled it or parked it; his words: "I think this is something we might have to think through."
- W-313d3 — the page-header lock-up's future work. Closes when he has done it and ruled its shape, or parked it; his words: "this is one component that I want to work on in the future its quite fussy at the moment".
- W-313d4 — switch, checkbox, radio and chip: four metas, or four roots in one meta. The page left it to his comment; he left none. Not decided here.

## 4 — Rows closed and noted (spec `notes/_lanes/313/AC3/rows-inscription.json`, via `_wrap_rows.py`)
Closed by his rulings: W-308iw (D20), W-305e2 (D22..D26), W-305e1 (D27), W-305e3 (D28), W-305e4 (D29), W-305e5 (D30), W-305n2 (D31, D32), W-307qp (D44). Notes added (build rows stay open, only the Dave half of their condition is met): W-305b1 (D36, D37), W-305w2 (D21, D33, D34), W-308ib (D38, D39), W-307ye (D42), W-307qn (D43 — the token's name is his, not given yet), W-307q8 (D45), W-307q2 (D46, D47), W-307q5 (D48).

## 5 — The flips (d1710e4c)
`$extracted.reviewed` false → true with a `$why` naming the ruling and the export, textual edit, on tabs, split-button, accordion, input-fields, dropdown, tooltip, pagination, notifications. Left false for the redo lane: button, table, date-picker, metric, slider, selection-controls, modals. `extract_spec.py` refuses to overwrite a reviewed:true meta without `--force`, so a re-run cannot undo the flips. Checked after: `probe_meta_schema.py --check` 0 findings · `extract_spec.py --report` 15 of 139 at full coverage, 0 refused · `_build_integrity.py` PASS, 138/138 schema valid.

## 6 — Commit notes
- Commit A's gates asked for `_CHAIN.md` (store counts moved: 1129 items, 539 live, 271 Dave's) and the regenerated memento schematic; both staged by name on the re-run.
- Commit B warned the local memento index stale (gitignored since s312-D1); rebuilt locally after, not staged.
- `knowledge/_state.json` load/save round-trip proven byte-identical before any write.

## Found, not fixed
- Call 24's token name is Dave's (the page: "its name is yours"); noted on W-307qn, not filed as a new item.
- A zero-byte untracked `knowledge/_state.json.lock` (08:22) sits in the tree; nothing reads it; left alone.

## Files
`knowledge/_rulings.json` · `knowledge/_state.json` · `knowledge/_node_titles.json` · `notes/_RULINGS.html` · `_CHAIN.md` · `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html` · the eight metas · `notes/_lanes/313/` (three exports, LANE-RULES.md, AC3/) · this report.
