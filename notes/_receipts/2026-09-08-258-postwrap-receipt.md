# #258 post-wrap receipt — three commits after the wrap, one of them swept another lane's files

provenance: 258 · 2026-09-08 · conductor Fable · written at Dave's word: *"if you made changes please leave receipts, there is another lane running"*
status: observed

## What #258 changed after its wrap commit `e3b5626`

| commit | mine | files | what |
|---|---|---|---|
| `2aa8f0c` | yes | `_CARRIES.md` (+1 carry ⑩), `notes/_ideas/2026-09-08-258-context-aware-responsive-behaviours.md` (NEW, later removed), `notes/_REHEARSAL-LOG.jsonl` (+1, instrument) | captured Dave's responsive-behaviours idea — in the WRONG place |
| `c641283` | yes | `knowledge/_memento-index.json` | index rebuilt after the capture (step 2g) |
| `928139f` | **PARTLY** | mine: `_FUTURE-STATE.md` (+14, new ★★ entry), `_CARRIES.md` (pointer fixed), `notes/_ideas/…` (deleted, dir removed), `knowledge/_memento-index.json` (rebuilt) | moved the idea into `_FUTURE-STATE.md`, the forward ledger |

## ⛔ `928139f` ALSO CONTAINS FILES THAT ARE NOT #258's — swept in by `git add -A` while lane #259 was working in the same tree

These were #259's in-progress working-tree changes at the moment of my commit. **They are now committed and pushed under my subject line.** #259: your `git status` will show these CLEAN; they are not lost, they are in `928139f`. I did not read, edit or judge them. Nothing here is a #258 claim.

- `knowledge/canon/dv-render.js` (NEW, 311 ln) · `dv-render-bar.js` (161) · `dv-render-line.js` (32) · `dv-render-stacked-area.js` (31) · `dv-render-donut.js` (31) · `dv-render-sparkline.js` (32) · `dv-render-combo.js` (31)
- `knowledge/_tests/chart-engine/bar.html` (NEW, 197 ln)
- `knowledge/snippets/Chart-bar.reference.html` (+711/−…) · `knowledge/components/chart-bar.meta.json` (+6)
- `knowledge/component-types.json` (+110/−…)
- `knowledge/_rulings.json` (**+16 lines — a ruling inscribed by #259, not by #258; #258's last is `s258-D4` at entry 402**)
- `knowledge/_A11Y-GATE.md`, `_BEHAVIOUR-GATE.md`, `_DATAVIZ-GATE.md` (regenerated ledgers)
- `notes/_GAUGE-LOG.md` (+4) · `notes/_REHEARSAL-LOG.jsonl` (+2) · `notes/_dream/_GRADE-DECISIONS.jsonl` (+2)
- `notes/_subreports/2026-09-08-259-A-engine-core-bar.md` (NEW, 156 ln)

**What I did NOT do:** no revert, no `git checkout`, no `git stash`, no edit to any file above. Reverting would have destroyed #259's work; the honest remedy is this receipt. If #259 wants its own commit boundary, the files are all in one commit and `git log -1 --stat 928139f` names them.

**The rule this breaks, for the record:** two lanes in one working tree ⇒ `git add -A` is never safe; add BY PATH. `[[two-lanes-wiped-each-other-via-git-checkout]]` (#253) now has a sibling: two lanes, one `add -A`, one lane's work under the other's subject.

## This receipt's own commit adds ONLY this file (`git add notes/_receipts/2026-09-08-258-postwrap-receipt.md`).
