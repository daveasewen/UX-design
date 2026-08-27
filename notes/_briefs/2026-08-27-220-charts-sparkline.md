# #220 sub brief — charts lane: DV-J2b sparkline (premise-verified) Layer-2 catch-up

**Model: Opus. Budget: sub spend is QUOTA and today quota is use-it-or-lose-it — be thorough. FILL discipline inside your own window still applies.**

## Mission
§C·1 names two queued chart strands: **DV-J2b sparkline** and **DV-J1 table-idiom**. That queue has gone stale THREE recorded times (#26, #196, #199 — items marked open that had landed). So:

**STEP 0 — VERIFY THE PREMISE BEFORE BUILDING (survey-before-build).** For sparkline (then table-idiom if sparkline is already done): search the repo for existing artefacts — `_memento_search.py "DV-J2b sparkline"` AND `--all`, grep `knowledge/_rulings.json` for related rulings BEFORE presenting anything as open, grep snippets/registry/`knowledge/_REVIEW-SIGNOFF.md`, `ls` the component dirs. If the strand already landed: report DISCHARGED-BY-MEASUREMENT with the receipts and STOP that strand — a measurement that closes the lane is a full success today.

If genuinely open: build the sparkline Layer-2 catch-up following the SCATTER exemplar pattern — **copy the mark contract and the toolbar, NOT the axis/grid CSS** (that idiom is fenced as ds-020, gate-enforced). Retrieve the DV-J2 scatter receipts first and name the files you pattern from.

## Method / colour law
- Four themes (mono · legacy · console · supercharge), light+dark — test PER THEME; flexibility IS the requirement.
- Dataviz vars: a dangling dataviz var renders SILENT BLACK and 13 gates are blind to it — resolve every var you mint/consume against canon and SAY you did. Alias-repoints can strip a theme override silently — check overrides per theme after any alias touch.
- Two-red law + mono error ink camp UNTOUCHED. Type composites `.t-cm-*`/`.t-ed-*`; shrink-only ratchet — debt may only shrink.
- Mint-time derivation (s200-D1): generators mint concrete values, never live derivation.
- Render proofs per `knowledge/_RUNBOOK-render-verify.md` (read it first): `goto("file://…")`, canvas font probe, steps driven individually (~178s call wall).
- Gates: run the RELEVANT named gates on your outputs (name each gate and the regions it owns before running; none that write outside your regions). `_build_all.py` is FORBIDDEN (partial run strands the tree).

## Regions you own
New sparkline snippet/reference files + their meta under the components tree (NEW files only), your review page `reviews/SPARKLINE-2026-08-27-v1.html` if one is warranted, and your filed report. Registry/spine/index edits (registry · MIGRATED_SNIPPETS · CATEGORIES · spine) are the CONDUCTOR'S serial set — list the exact edits needed in your report; do NOT make them ([[regen-serial-set-is-ordered]]).

## DO-NOT-RULE / DO-NOT-TOUCH
- ⛔ `knowledge/_proforma/DataViz-interactive.html` is AHEAD of its own generator (W-176) — never regenerate it; a blind regen deletes ~7KB and flips the dark ground to #000000.
- No git. No memory. No `_rulings.json` / `_state.json`. No promotions. No edits to existing gated snippets (findings go in the report). Heatmaps are PARKED — out of scope.
- Version-don't-overwrite (`-vN`); mv not rm.

## Pitfalls / consequences (mandatory, Dave #165)
- Building on a stale queue premise wastes the lane — STEP 0 exists because it has happened three times.
- Copying scatter's axis/grid CSS imports the ds-020 gap into a new component.
- A green selftest cannot see scope — drive the new instrument on real data.

## Report
FILE at `notes/_subreports/2026-08-27-220-charts-sparkline.md`: `COUNTS:` line, premise-verification evidence, conductor serial-set edit list, `RULING-SHAPED QUESTIONS` (Dave's), `REPLAY-THESE`. Chat gets a STUB (≤6 lines).
