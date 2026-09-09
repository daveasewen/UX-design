# #263 lane C (conductor seat) — chart-engine re-drive after type.css moved

**Why.** `4cc4204` (#261 F2, 10:58) changed `knowledge/canon/type.css`; every driven receipt in
`knowledge/_tests/chart-engine/_receipts.json` (driven 09:54, `0420197`) pinned the old hash
`295b2867…`, so `_validate_dataviz.py` read STALE on all 27 pages — the s263-D11 gate for
`requiredAria` was blocking-on-stale, grading nothing.

**Did it affect v1.0.9?** v1.0.9 (`dd129e8`, 15:51) SHIPS the new type.css. The dataviz gate is NOT
one of the nine release gates, and the `_DATAVIZ-GATE.md` committed at `81ce08f` (12:56) reads
PASS / 0 STALE although HEAD's type.css already differed from the receipts' hash — a report
committed from a tree that did not match HEAD (the #253 two-lanes-wiping pattern). So at the cut,
no chart had been driven against the type.css that shipped. FINDING, ruling-shaped: should
`_validate_dataviz.py` (or a receipts-fresh check) join the release gate set?

**Fix.** Chromium 151 installed in the sandbox (playwright + `libXdamage.so.1` extracted locally,
no root); `python3 knowledge/_drive_chart_engine.py` re-drove 27 pages × 8 theme×mode combos.

**Test.**
- `_validate_dataviz.py` → `✅ DataViz gate passed (15 chart surface file(s))`, 0 STALE, 0 blocking.
- Receipts diff, old (HEAD) vs new: same Chromium 151.0.7922.34, **0 differing measured fields**
  across all pages/combos — marks, rows, contrast, rogue hex, gradients, curve, aria all identical.
  The type.css change moved nothing a chart measures. ⇒ v1.0.9's charts are retroactively clean.
- STALE arm proven live by observation (it fired on the real tree before the re-drive; lane A drove
  its RED on a mutant receipt earlier today).
- `requiredAria [driven]`: every page reads n/n present in all 8 combos.
