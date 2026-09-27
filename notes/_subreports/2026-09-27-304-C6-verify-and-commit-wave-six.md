# #304 C6 - verify-and-commit seat, wave six: W6's reduced-motion fit fix and the [117] live-state row verified independently, then committed, pushed, CI read back

provenance: 304 · Sunday 2026-09-27 · Opus 5.5 verify-and-commit seat, delegated by the #304 conductor; built none of W6 · mount HEAD `52049781` at start · stage `$HOME/c6st/{head,w6}` (copies of F5's `$HOME/f5st/f5/c2r1`, engine swapped on the W6 side only) · fresh clone `$HOME/c6s` (`git clone --shared` of the mount at `52049781`) · no `git status` on the mount, no Project memory
status: observed - every figure below was printed by a probe, a gate or the survey at the seat; receipts in `notes/_lanes/304/C6/verify/`
window: UNMEASURED (a seat cannot read its own usage)
⚠ INTERIM COPY. It rides the wave-six commit so `W-304c6` has a home. The FINAL copy (sha, push range, CI by job) rides the NEXT commit and closes `W-304c6`.

## THE ANSWER FIRST

**Verify verdict: PASS on all three counts. Nothing failed, so the commit went ahead.**

1. **The reduced-motion fit fix is safe and does what W6 says.** Reproduced with my own probe (`verify/c6fit.py`, same unfitted criterion as W5a's, plus a viewBox MutationObserver from document start), cand2-r1 overview, 1440, 10 fresh loads each: reduced motion HEAD **9/10 unfitted** v W6 **0/10**; motion HEAD 0/10 v W6 0/10. viewBox writes per load: reduced motion 17 v 24 (one extra pass of 7 writes for 3 canvases), motion 17 v 17 (no extra pass); **0 writes after 1.5 s on any load, either side** (no loop). Budget: `_validate_behaviour.py` on the mount and in the clone: **Chart-combo 34,777 code-only bytes of 34,816 (34 KB)**, PASS; HEAD's committed ledger reads 34,768; selftest OK.
2. **[117] option (a) is exactly what W6 says.** The mount's `_LIVE-STATE.md` differs from HEAD by one changed line (the Last-refreshed stamp, dream pass 13 -> 14) and one added line (the §🔀 dream pass 14 status row), `--numstat 2 1`, and the live diff is byte-identical to W6's saved `dream14-live-state.diff`. The precedent is real: `96c2f454` (#268 wrap) carries dream pass 12's row and stamp, `77a77eea` (#289 wrap) carries pass 13's. The dream pass's own commit `ff382c0b` touched only the proposals file, the rehearsal log and the schematic; runbook step 7b (line 40) writes the row after the lane commit.
3. **Survey spot-check in a fresh clone, W6's 33 files + the mount's `_LIVE-STATE.md` overlaid, serial run:** clean `52049781` `_build_memento_index.py --check` STALE (CI's red reproduced); with the overlay, nothing rebuilt, **current (2,333 records)**. Chunks 31:70, 71:100, 101:127 (97 steps): **`[117]` ✅**, non-green only `[61] [68]` could-not-ask, `[73]` timeout, `[81] [90] [98]` FAIL, **0 steps differ from W6's survey by step**, so 0 green->red. Chart receipts in the clone: `_drive_chart_engine.py --check` 27/27 FRESH; `gen_component_partials --check` OK; `gen_showroom --check` OK (137 + index).

## 1 · THE FIX, READ

`knowledge/canon/dv-behaviour.js` (the only hand edit): the resize body becomes `refit()` (still ONE `addEventListener('resize'`, rAF-debounced by `cancelAnimationFrame`), and one document-level `transitionend` listener calls `refit()` when `e.target.matches('svg.dv-fit,:has(svg.dv-fit)')`. `fitCharts`/`placeSegs` walk with `NodeList.forEach` (same list, same order; `fitOne(svg)`/`moveSeg(seg)` ignore the extra arguments).

- **No loop.** `fitOne` writes SVG attributes only (`viewBox`, `x`, `width`, `x1`, `x2`, `transform`, `points`/`d`, `data-fys`) and `thinLabels` hides labels inside the svg; none of these targets is a canvas or holds one, and the svg's own size follows its viewBox through `height:auto`, which cannot transition. Measured: 0 viewBox writes after 1.5 s on 40 loads.
- **No thrash.** Every trigger goes through the one rAF-debounced path, so a burst of transitionends in a frame is one pass.
- **Not every unrelated transition** (`verify/c6unrelated.py`, motion on, after a 2 s settle): a 60 ms background transition on an element that holds no chart **0 writes**; 20 pointer moves **0 writes**; a background transition on the chart's own figure **one pass (7 writes)**; a 100% -> 90% width transition on the figure **one pass, and the fit lands (889 v box 889), where HEAD strands it (990 v box 889)**; quiet for 1.5 s after.
- **What remains true, declared:** `:has(svg.dv-fit)` matches every ancestor of a chart (the figure, the tile, `main`, `body`), so a transition that ends on any of them (a hover shadow on a tile, a theme colour fade on the page root) costs one extra fit pass. Bounded and idempotent, not a loop. In a browser without `:has()` (Firefox before 121, Safari before 15.4) `matches` throws inside the listener: a console error per transitionend and no re-fit there, the rest of the engine untouched. canon.css already depends on `:has()`.

## 2 · RECEIPTS (`notes/_lanes/304/C6/verify/`)

- `c6fit.py`, `fitrate-c6.txt` - the reproduction, both motion settings.
- `c6unrelated.py`, `unrelated-c6.txt` - the unrelated/ancestor/width transitions.
- `live-state-c6.txt` - the `_LIVE-STATE.md` diff lines, the identity with W6's saved diff, the precedent stats, the runbook lines.
- `memento-check-c6.txt` - `[117]` STALE at clean `52049781`, current with the overlay.
- `clone-serial-c6.txt` - the serial in the clone, all rc 0 (moved `_CHAIN.md`, `_RULINGS.html` date line, schematic: the clone class).
- `survey/after_{31_70,71_100,101_127}.log`, `survey/compare-w6-c6.txt` - the chunks and the by-step compare.
- `receipts-clone-c6.txt` - receipts FRESH, budget, partials/showroom checks; `_gate_artefact_fresh.py --check` 5 FRESH · 2 STALE (`_validate_advisory`, `_build_instrument_fit`) at the overlay, **the same two STALE at clean `52049781`** (advisory, exit 0, not W6's).

Housekeeping: W6's idle work clone `$HOME/w6` (1.2 GB, VM-local, outside the mount; its 33 files are byte-identical on the mount) was removed to make room for the fresh clone. W6's survey clone `$HOME/w6s` was left.

## 3 · THE COMMIT, PUSH AND CI

(filled in the FINAL copy)

REPLAY-THESE: § THE ANSWER FIRST · § 1 · § 3
