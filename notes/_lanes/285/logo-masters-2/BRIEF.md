# #285 lane LM2 — the wordmark is distorted: rigid-move regeneration

**2026-09-18 · one Opus 5 build lane · conductor Fable 5.1 · evidence `notes/_lanes/285/logo-masters-2/`**
**Predecessor:** `notes/_lanes/284/logo-masters/BRIEF.md` · `notes/_subreports/2026-09-18-284-LM-logo-masters.md`

## THE JOB

Dave, on a 4× crop of the #284 masters: *"the word mark is distorted, look at the B"*. Find the
cause in `knowledge/assets/logos/_gen_masters.py`, fix it, regenerate all 40 masters, and put a
BEFORE/AFTER in front of him at 4×.

## PREMISES — measured at this seat, 2026-09-18, not recalled

| premise | reading |
|---|---|
| the named cause | `snap_wordmark()` snapped on-path nodes of straight `H`/`V` segments inside S, B and C to integer px while leaving their cubic control points scaled-only → the bowls kink where a moved node meets an unmoved handle |
| a **second** cause, not in the task | the same function scaled x and y by **different** factors: `kx = (W - Lx)/(R - L)` and `ky = capH/(B - T)`. Measured `kx/ky` per step: 1.0039 · 0.9949 · **1.0436** · 0.9949 · 0.9896 — at h=32 the wordmark was stretched **4.4 % wider than tall**. That is the squash Dave is seeing, more than the node snapping is |
| wordmark box (source) | `masterbrand-light-colour`: L 183.346 · R 314.428 · cap 24.6826 · baseline 60.2494 · cap-height 35.5668 (`dark-mono` is the same geometry shifted 0.346 left, 0.058 down — the generator measures each file) |
| hexagon | untouched: every source coordinate is a multiple of 42.5, maps to `k·h/2`, exact integers at all five steps. Zero rounding error by construction |
| widths | 89 · 104 · 119 · 133 · 148, unchanged; no `viewBox`, unchanged |
| can cap-top **and** baseline both be integers under one uniform scale? | **No.** `35.5668·s` = 10.042 · 11.716 · 13.390 · 15.064 · 16.737 — never an integer. Pinning both requires a y-scale ≠ the file scale, i.e. distortion, which is the thing being fixed |
| what pinning both by a *uniform* rescale `k = round(capS)/(B−T)` would cost | `k/s` = 0.996 · **1.024** · 0.971 · 0.996 · **1.016**: the wordmark would be up to 2.4 % out of size with the hexagon it locks up with, and would run 0.23–0.65 px **past** the file's right edge at h = 28, 36, 40. Declined |

## WHAT I CHANGED

1. **`snap_wordmark()` is now a rigid move and nothing else.** One uniform scale `s = h/85` — the
   same factor the hexagon is drawn at — plus one translation applied to *every* coordinate of
   every wordmark glyph, nodes and control points alike. No coordinate moves relative to any other
   coordinate. Curves cannot kink; the B's bowls cannot squash.
2. **`quantise_runs()` retired** (deleted), and with it the H's whole-pixel/stem-pairing snapping.
   It does **not** qualify for the task's exemption: the #284 report measures it changing the H's
   drawn width by 0.7 px at h=28, which is by definition a move of nodes relative to their
   neighbours. Dropped.
3. **Translation rule.** Left edge → `round(L·s)`, an integer column. Cap line → `round((h − capS)/2)`,
   an integer row, keeping the cap box centred on `h/2` as before. The baseline lands at
   `cap_top + capS` and is *not* on an integer row — declared, with the numbers, in the report.
4. **One fit clamp.** `W` is rounded from `315·s`, so at some steps the artwork's own right edge
   already sits a fraction past `W`; rounding `Lx` up can add half a pixel on top. `Lx` steps down
   one column when that push exceeds `TOL` (0.25 px, the tolerance the hexagon already uses). It
   fires at h=36 only. Resulting hexagon→wordmark gap: 4 · 4 · 5 · 5 · 6 px — monotone.
5. **Unchanged:** the hexagon snapping, the float/kink normalisation, `--check`, `--report`, the
   help-gate header, the filenames, the widths, the absence of `viewBox`.

## FENCES

⛔ No commit. ⛔ Not `_build_all.py`, `gen_kg_icons.py`, `gen_kg_rules.py`, `land_rests_on.py`.
⛔ No edits to the 8 source exports, `_gauge_tokens.py` constants, `logos.md`, `_rulings.json`,
`showroom/`. ⛔ No stray untracked file left under `knowledge/assets/`.

## RETURN

Report at `notes/_subreports/2026-09-18-285-LM2-logo-masters-regen.md`. Contact sheet at
`notes/_lanes/285/logo-masters-2/MASTERS-2026-09-18.html` with a BEFORE/AFTER strip at 4×.
