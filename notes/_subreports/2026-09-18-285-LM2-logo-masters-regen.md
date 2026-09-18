# #285 lane LM2 — the wordmark was distorted; it now moves rigidly

**2026-09-18 · opus · brief `notes/_lanes/285/logo-masters-2/BRIEF.md` · evidence `notes/_lanes/285/logo-masters-2/`**
**Predecessor:** `notes/_subreports/2026-09-18-284-LM-logo-masters.md`

Dave, on a 4× crop of the #284 masters: *"the word mark is distorted, look at the B"*. He is right,
and there were **two** causes in `snap_wordmark()`, not one. Both are gone. All 40 masters are
regenerated, `--check` exits 0, and the before/after is on the contact sheet at 4× for his eye.

## Two causes, the second one worse than the named one

**The named cause — per-node snapping inside curved glyphs.** The old code marked every on-path node
that took part in a straight `H`/`V` segment inside S, B and C and rounded it to whole pixels, while
leaving the cubic control points scaled only. A bowl leaves the stem at such a node. Move the node
half a pixel and leave its handle behind and the curve kinks at the join and flattens on the way
out. That is the lumpy counter Dave is looking at.

**The cause the task did not name — the wordmark was not scaled uniformly.** The old code computed
two scale factors and used them on the two axes:

```
kx = (W - Lx) / (R - L)        ky = capH / (B - T)
```

Measured `kx / ky` per step: **1.0039 · 0.9949 · 1.0436 · 0.9949 · 0.9896**. At h=32 the wordmark was
drawn **4.4 % wider than it was tall** — a genuine horizontal stretch of every glyph in the lockup,
independent of any snapping. That is the squash. It was invisible to the #284 lane's own probes
because those probes counted anti-aliased pixels and stem runs, neither of which can see an aspect
error.

## The diff, in one paragraph

`knowledge/assets/logos/_gen_masters.py`: `quantise_runs()` **deleted** (32 lines) and with it the H's
whole-pixel / stem-pairing ladder. `snap_wordmark()` **rewritten** (43 lines → 30) as a rigid move:
one uniform scale `s = h/85` — the same factor the hexagon is drawn at, so the lockup relationship is
exact — plus one translation `(dx, dy)` applied to every coordinate the path model yields, **nodes
and control points alike**, through the existing `coords()` iterator. No coordinate is moved relative
to any other coordinate; the wordmark that comes out is the wordmark that went in, at a different
size and place. Tally keys changed from `h_nodes` / `curve_nodes` / `free_nodes` / `free_controls` to
`rigid_nodes` / `rigid_controls` / `snapped_nodes` (which is `0`, and is there so the report can
assert it). The module docstring says what the file now does and why. `snap_hex()`, the float/kink
normalisation, `--check`, `--report`, the help-gate header, the filenames, the widths and the absence
of a `viewBox` are **untouched**.

**The H is not exempt.** The task allowed keeping the H's whole-pixel snapping only if it could be
shown not to move a node relative to its neighbours differently from the rigid move. It cannot: the
#284 report itself measures the delta quantisation changing the H's drawn width by **0.7 px at h=28**
(11 px drawn against 10.315 px scaled). That is by definition a relative move. Dropped.

## Snapping, before and after

| what | #284 (before) | #285 (after) |
|---|---|---|
| hexagon vertices | exact on `k·h/2`, integer at all 5 steps | **unchanged** |
| hexagon float artefacts | 160 normalised, 40 kink segments dropped | **unchanged** |
| wordmark x-scale | `kx = (W − Lx)/(R − L)` | `s = h/85` |
| wordmark y-scale | `ky = capH/(B − T)` | `s = h/85` |
| x-scale ÷ y-scale | 1.0039 · 0.9949 · **1.0436** · 0.9949 · 0.9896 | **1.0000** at every step |
| H-glyph nodes snapped | 12 per master (delta-quantised ladder) | **0** |
| S/B/C nodes snapped | 20 per master (nearest integer) | **0** |
| control points snapped | 0 | 0 |
| nodes moved rigidly | — | **56 nodes + 58 controls** per masterbrand master |
| left edge | `round(L·s)`, integer | `round(L·s)`, integer (one −1 clamp, see below) |
| right edge | forced flush to `W` (this is what made `kx ≠ ky`) | falls where the rigid move puts it |
| cap line | integer row | integer row |
| baseline | integer row | `cap_top + 35.5668·s` — **not** an integer row |

### The wordmark box as it now measures (identical for all four masterbrand files)

| step | W | left | gap to hexagon | cap top | cap height | baseline | right | right − W |
|---|---|---|---|---|---|---|---|---|
| 24 | 89 | 52 | 4 | 7 | 10.0424 | 17.0424 | 89.0114 | +0.0114 |
| 28 | 104 | 60 | 4 | 8 | 11.7161 | 19.7161 | 103.1800 | −0.82 |
| 32 | 119 | 69 | 5 | 9 | 13.3899 | 22.3899 | 118.3485 | −0.65 |
| 36 | 133 | **77** | 5 | 10 | 15.0636 | 25.0636 | 132.5171 | −0.48 |
| 40 | 148 | 86 | 6 | 12 | 16.7373 | 28.7373 | 147.6856 | −0.31 |

`W` is rounded down from `315·s` at some steps, so the artwork's own right edge can already sit a
fraction past `W`; rounding the left edge up then adds to it. One clamp steps the left edge down a
column when that push exceeds `TOL` (0.25 px, the tolerance the hexagon already uses). **It fires at
h=36 only** (78 → 77), and it happens to make the hexagon→wordmark gap monotone: 4 · 4 · 5 · 5 · 6.
Worst remaining overflow is **0.0114 px at h=24** — one percent of one pixel of coverage on the C's
right terminal.

### The one thing I could not give the task, declared

The task asked for the left edge on an integer column **and cap-top and baseline on integer rows**.
Under one uniform scale that is over-determined: `35.5668 · s` is **10.0424 · 11.7161 · 13.3899 ·
15.0636 · 16.7373** — never an integer at any step. Two ways to force it, both measured and both
declined:

1. **Rescale y only** (`ky = round(capS)/(B−T)`) — that is exactly the bug being fixed. No.
2. **Rescale both uniformly** by `k = round(capS)/(B−T)`. Uniform, so no aspect distortion, but
   `k/s` = 0.996 · **1.024** · 0.971 · 0.996 · **1.016**: the wordmark would be up to **2.4 % out of
   size with the hexagon it locks up with**, and would run **0.23–0.65 px past the file's right
   edge** at h = 28, 36 and 40 — a clipped C. No.

So: the cap line is pinned to an integer row, the baseline is not. The cost is a soft bottom edge
(measured below); the alternative is a distorted or clipped wordmark. If Dave would rather have a
hard baseline than an exact aspect ratio, that is a ruling, not a bug, and option 2 is the build.

## What the shots show, per size

Driven with the sandbox Chromium (`chrome-headless-shell` 1243, arm64), `goto("file://…")` throughout,
never `set_content()`. **Console errors on the contact sheet: 0**, on three separate loads.

**The B's bowls — the thing Dave asked about.** `shots/Bzoom-24.png`, `-32.png`, `-40.png` put the
before and after B side by side at 24×. At every one of the three sizes the difference is not subtle:

- **24 px — was broken, now smooth.** Before: the upper counter has a flat notch cut into its
  top-left and a straight chord where the bowl should curve; the lower counter has a visible step on
  its left flank and the two counters are different shapes. After: both counters are clean rounded
  forms and they are the same shape as each other.
- **32 px — was broken, now smooth.** Before: a pronounced dent on the inner right of the upper
  counter and a lumpy lower-left on the lower one. After: both bowls run smoothly out of the stem and
  back; the join at the stem is a clean tangent.
- **40 px — was wobbly, now smooth.** Before: both counters show small flat facets top and bottom
  where a snapped node dragged the outline off its own curve. After: no facets at either counter.

**Do the B's horizontals meet the H's crossbar?** Measured off the rendered bitmap, coverage per row
in a column through the H's crossbar against a column through the B's middle bar:

| step | H crossbar rows (coverage) | B middle-bar rows (coverage) | meet? |
|---|---|---|---|
| 24 | 11 (1.00) · 12 (0.75) | 11 (0.76) · 12 (0.50) | **yes — same rows** |
| 32 | 14 (0.50) · 15 (1.00) · 16 (0.75) | 14 (0.50) · 15 (1.00) · 16 (0.50) | **yes — same rows** |
| 40 | 18 (0.25) · 19 (1.00) · 20 (1.00) · 21 (0.50) | 18 (0.20) · 19 (1.00) · 20 (1.00) · 21 (0.27) | **yes — same rows** |

They meet **by construction** now, not by luck: one rigid move preserves the source's own relation
between the H's crossbar and the B's bar exactly. The #284 masters did not — at h=40 the before shows
the B's bar spilling into row 18 at 0.06 coverage while the H's crossbar started at row 19, the
"B's horizontals sit a pixel under the H's crossbar" that the #284 report named as a follow-on. That
follow-on is closed.

**The cost, stated plainly: the edges are softer than they were.** The old masters bought hard
1.00/0.00 edges on every stem and bar by moving the outline onto the pixel grid. This one does not
move the outline at all, so horizontal strokes land where the maths puts them and are anti-aliased:
0.75 and 0.50 coverage rows appear at the top and bottom of every bar. Per size, at 1:1:
**24 px — legible, correct in shape, softest of the five** · **28 / 32 px — soft edges, well-formed**
· **36 / 40 px — soft edges, well-formed, indistinguishable from good type at reading distance**.
Nothing is broken at any size, and every lockup renders. The hexagon is unchanged and still has
exactly four anti-aliased edges (its diagonals) and hard verticals and horizontals everywhere.

That is the real trade this lane makes, and it is Dave's to accept: **#284 was crisper and wrong;
#285 is correct and slightly softer.** The shape error was visible at 4×; the softness is visible at
4×. At 1:1 neither is, which is why the 4× panel exists.

## The contact sheet

`notes/_lanes/285/logo-masters-2/MASTERS-2026-09-18.html`, same idiom as the #284 sheet (Swiss,
sticky nav, `.label` eyebrow), rebuilt by `_sheet.py` from the files on disk so it cannot drift.
Three fixes to the #284 sheet:

- **The 4× grid.** Every 4× shot now sits in a wrapper box whose CSS width and height are exactly 4×
  the file's raw width and height, so layout reserves the painted area instead of the unscaled one
  (`transform: scale(4)` still does the painting). That alone straightens the grid.
- **Labels in one row per set.** Each cell is a grid whose art row is a fixed 160 px (4 × the tallest
  step) with the box bottom-aligned in it, so every label in a rack starts on the same line.
- **A BEFORE / AFTER strip**, first section, `#ba`: `masterbrand-light-colour-24` and `-40` at 4×,
  the #284 file (recovered with `git show HEAD:`) beside the file on disk now, on a wider wrapper so
  both fit side by side at 40. Label-crop rule obeyed — labels are `.6875rem/1.9`, no ascender or
  descender is cropped at any size on the sheet.

## Paths touched

**Edited**
- `knowledge/assets/logos/_gen_masters.py`

**Regenerated** (20 files; the 20 hexagon masters are byte-identical to before and show as unmodified)
- `knowledge/assets/logos/masters/masterbrand-{light,dark}-{colour,mono}-{24,28,32,36,40}.svg`

**Created**
- `notes/_lanes/285/logo-masters-2/BRIEF.md`
- `notes/_lanes/285/logo-masters-2/MASTERS-2026-09-18.html`
- `notes/_lanes/285/logo-masters-2/_sheet.py`, `_sheet.css`, `_shoot.py`
- `notes/_lanes/285/logo-masters-2/before/masterbrand-light-colour-{24,32,40}.svg` (from `git show HEAD:`)
- `notes/_lanes/285/logo-masters-2/shots/` — `sheet-full-1280.png`, `before-after-4x.png`,
  `panel-{masterbrand-light-colour,masterbrand-dark-colour,masterbrand-light-mono,hexagon-light-colour}.png`,
  `panel-1x-mb-light-colour.png`, `Bzoom-{24,32,40}.png`, `8x-B-{before,after}-{24,32,40}.png`,
  `4x-ba-{24,32,40}.png`
- `notes/_subreports/2026-09-18-285-LM2-logo-masters-regen.md` (this file)

**Not touched:** the 8 source exports, `_gauge_tokens.py`, `logos.md`, `_rulings.json`, `showroom/`,
`_logo_nodes.json`. The four fenced generators were not run. Nothing committed.
`knowledge/_seam.py` shows as modified in `git status` — that is **not** this lane; it was already
dirty when I arrived.

## What I could not do

- **`notes/_lanes/285/logo-masters-2/_tmp/`** — nine scratch HTML files written by the first pass of
  `_shoot.py` that the sandbox will not let me delete (`rm`, `shutil.rmtree` → `Operation not
  permitted`). It is under `notes/`, **not** under `knowledge/assets/`, so it does not trip the
  blocking stray gate. `_shoot.py` now writes its scratch to a `tempfile.mkdtemp()` outside the repo,
  so it will not come back. Someone with delete rights should remove the directory.
- **No stray under `knowledge/assets/`.** `git status --porcelain knowledge/assets` lists 21 modified
  tracked files and **zero untracked** — checked.
- The masters are still **not registered in `_logo_nodes.json`** — the #284 follow-on stands, and the
  fenced generators were not run here either.
- The hexagon duplicate pair is still two files, still byte-identical at all five steps.

---

**Measured:** 40 masters on disk · 0 with a `viewBox` · widths 89/104/119/133/148 unchanged · 20
masterbrand files rewritten, 20 hexagon files byte-identical · **0 nodes and 0 control points snapped
inside any glyph** · x-scale ÷ y-scale = **1.0000** at all five steps (was up to 1.0436) · max right-edge
overflow 0.0114 px · B's bar and H's crossbar on the same rows at 24/32/40 · 0 console errors on three
loads · `_gen_masters.py --check` **exit 0** · 0 commits.
