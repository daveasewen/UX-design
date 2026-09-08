# #258 session receipt — every filed report cited BY PATH (`s218-D7`)

provenance: 258 · 2026-09-08
status: observed

*The ★ LATEST banner is capped at 1,193 tape by `s241-D2` and cannot carry fifteen paths, so the
`s218-D7` citation obligation — "the conductor CITES EACH REPORT BY PATH in the session receipt
**or** the ★ LATEST banner" — is discharged here. An uncited pointer is an unread one; this file
is what makes the fifteen visible to the next session and to `subreport_citation_check`.*

## The five cold runs and their review pages

- `notes/_subreports/2026-09-08-258-C-cold-run.md` — **v1**, blind, against the ratified v1.0.7
  zip `13a593de…`: **3/2/0/2** (#246 read 2/2/0/2). Review `reviews/COLDRUN-258-2026-09-08-v1.html`.
- `notes/_subreports/2026-09-08-258-C2-cold-run-2.md` — **v2** against the tree at `e774fb7`:
  **3/2/3/3**, 0 pageerrors, 58/58 controls live, URL state survives reload; one blind-condition
  defect (the Data-grid snippet splices its demo switcher and width dial into the page, grid
  213px). Review `reviews/COLDRUN-258-2026-09-08-v2.html`.
- `notes/_subreports/2026-09-08-258-C3-cold-run-3.md` — **v3** at `5c241f7`: **3/2/3/2**;
  APOLLO-DEMO in page 0, grid 213→760px, compose hex 262→0; three toolbar filters dead on an
  unread `behaviour` contract; the receipt gate never fired. Review `…-v3.html`.
- `notes/_subreports/2026-09-08-258-C4-cold-run-4.md` — **v4** at `84f0a17`: **3/2/3/3**, 0 dead
  controls, receipt PASS after `--mint`; found the fenced `.dg{--dg-max:760px}` in
  `canon.css:10538`. Review `…-v4.html`.
- `notes/_subreports/2026-09-08-258-C5-cold-run-5.md` — **v5** at `c9bf745`: **3/3/3/2, BOTH
  GATES PASS for the first time in the series**, grid 1,328px in a 1,376px tile. Review
  `…-v5.html`.

## The enactment lanes

- `notes/_subreports/2026-09-08-258-L1-skill-rewrite.md` — `s258-D1`/`s258-D2`: rule 2a REMOVED,
  rules 13–17, `_validate_receipt.py` relaxed for authored JS (selftest 41 arms).
- `notes/_subreports/2026-09-08-258-L2-footer-and-bento.md` — footers into side-nav /
  multi-column / bento, and the PREMISE CORRECTION on the bento's "146 hex".
- `notes/_subreports/2026-09-08-258-L3-behaviour-metas.md` — typed `behaviour` metas for
  data-grid / filter-toolbar-bar / sidebar-nav, plus the **51-meta backlog** by name.
- `notes/_subreports/2026-09-08-258-P-demo-chrome-probe.md` — 61 snippets with chrome, 27
  dangerous; the measurement that scoped the `s258-D3` sweep.
- `notes/_subreports/2026-09-08-258-A-demo-fence.md` ·
  `notes/_subreports/2026-09-08-258-B-demo-fence.md` ·
  `notes/_subreports/2026-09-08-258-C-demo-fence.md` — the fencing pass, 53 snippets across the
  three lanes, `--demo-width` reads moved to real component defaults, five template scripts
  split component/chrome.
- `notes/_subreports/2026-09-08-258-G-demo-fence.md` — the skill and gate half: never copy inside
  a fence, `FAIL:DEMO-CHROME-COPIED` (selftest 46 arms), marker grammar homed in
  `_RUNBOOK-compose-from-canon.md`.
- `notes/_subreports/2026-09-08-258-D4-grid-selection-controls.md` — `s258-D4` enacted: 44px
  targets, indeterminate driven, compose gate PASS on a v5 copy, mutation-proved.
- `notes/_subreports/2026-09-08-258-R-chart-recipe.md` — rule 18, the interim chart recipe, and
  the `:where(.cn-chart-*)` wrapper trap that #259's engine must close.

## The wrap

- `notes/_subreports/2026-09-08-258-wrap.md` — this session's delegated capture ritual.

*Rulings: `knowledge/_rulings.json` § `s258-D1` … § `s258-D4` (store 398 → 402).
Commits `70ed8c7..1c9c6ae`. WHY/HOW:
`_DECISION-HISTORY/2026-09-08-258-five-cold-runs-and-the-sentence-2a-forbade.md`.*
