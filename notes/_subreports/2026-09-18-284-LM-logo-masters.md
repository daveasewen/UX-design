# #284 lane LM — the forty per-size logo masters

**2026-09-18 · opus · brief `notes/_lanes/284/logo-masters/BRIEF.md` · evidence `notes/_lanes/284/logo-masters/`**

The 40 masters exist: `knowledge/assets/logos/masters/<lockup>-<theme>-<mode>-<h>.svg`, eight
lockups across the five raw heights of `s282-D3`. None of them carries a `viewBox`; each carries
its own pixel width and height and nothing else on the root. They are written by
`knowledge/assets/logos/_gen_masters.py` from the eight surviving Figma exports — a generator,
not forty hand files — and `_gen_masters.py --check` regenerates all forty to memory and diffs
them against disk. It exits 0 today.

## The hexagon is exact, and the brief's hedge was unnecessary

Every hexagon coordinate in the source is a multiple of 42.5 on both axes. At height `h` that maps
to `k · h/2`, and all five steps are even, so **every hexagon vertex in all 40 masters is a whole
integer** — no `.5` appears at any step, on any file. The brief's premise allows for "an integer or
a .5 that is a grid line at h/2, h/4"; measured, the `.5` case never arises. Hexagon widths are
`2h` exactly: 48 · 56 · 64 · 72 · 80.

The Figma noise is gone. Per source file the generator normalised **4 off-grid coordinates**: the
two `e-05` y-values of the top triangle and the two coordinates of the `42.3107 84.9311` kink. One
correction to the brief here — the artefact is not one value across the set. Seven files carry
`9.15527e-05`; `hexagon-light-colour.svg` carries `8.58307e-05`. Both are inside the 0.25
tolerance and both normalise to `0`. The kink is removed by normalising `(42.3107, 84.9311)` onto
its true vertex `(42.5, 85)` and then dropping the segment that has collapsed onto its own start
point — **40 kink segments dropped, 160 float coordinates normalised**, one kink and four floats
per master.

`hexagon-light-colour-<h>.svg` and `hexagon-dark-colour-<h>.svg` come out **byte-for-byte
identical at all five steps** — the duplicate pair `s282-D4` names, now with the one distinguishing
float normalised away. Both files are still written. Merging them is Dave's, not this lane's.

## The wordmark box, and three choices I had to make

The wordmark is anchored on four measured lines, read off the artwork rather than assumed: the
wordmark's extreme left and right x, and the cap line and baseline taken from the H — the one glyph
whose path is `M`/`H`/`V`/`Z` only, so its own extremes *are* the cap line and baseline.

| source file | wordmark left | right | cap | baseline | cap-height |
|---|---|---|---|---|---|
| `masterbrand-light-colour` | 183.3460 | 314.4280 | 24.6826 | 60.2494 | 35.5668 |
| `masterbrand-dark-colour` | 183.3460 | 314.4280 | 24.6827 | 60.2494 | 35.5667 |
| `masterbrand-light-mono` | 183.3460 | 314.4280 | 24.6826 | 60.2494 | 35.5668 |
| `masterbrand-dark-mono` | **183.0000** | **314.0820** | **24.7408** | **60.3075** | 35.5667 |

**A premise the brief does not carry:** `masterbrand-dark-mono.svg` is not the same wordmark
geometry as the other three. It is the same wordmark **shifted** — 0.346 left, 0.058 down — with
the identical 131.082 width and 35.567 cap-height. The brief's premise row gives one figure,
"x ≈183–314.4", for all four. Because the generator measures each file's own box rather than
hardcoding one, the shift washes out: all four masterbrands produce identical snapped geometry at
every step, differing only in ink.

Three choices the brief left me, or that the measurement forced:

**1. Width rounds, as instructed.** Measured exact widths are 88.9412 · 103.7647 · 118.5882 ·
133.4118 · 148.2353. **Round** gives **89 · 104 · 119 · 133 · 148**, which is what the masters
carry and what the brief's premise table predicts. The alternative the brief asked me to name —
**floor** — gives **88 · 103 · 118 · 133 · 148**; it differs at three of five steps and would crop
the C's right terminal by up to a pixel at 24 and 28. Round is the better of the two on the
artwork, not just on the arithmetic.

**2. The wordmark's right edge is set flush to W, not to `round(R·s)`.** The two agree at four of
the five steps. They part at h=32, where `round(314.428 · 32/85) = 118` but `W = 119` — taking the
rounded value would leave the master with a one-pixel empty column down its right edge. The masters
carry no padding (`s282-D5`/`D6` are the consumer's), so a trailing transparent column is a defect,
not clear space. Flush.

**3. The cap box is centred on h/2, and the cap-height is rounded before the lines are.** The naive
reading — round the scaled cap line and the scaled baseline independently — was tried and measured
first. It gives cap-heights of **10 · 12 · 14 · 16 · 16**: the wordmark does not grow at all between
the 36 and 40 steps, because 24.6826·s rounds up at 40 and 60.2494·s rounds down. Rounding the
cap-height first and centring the box on h/2 (the source cap box is centred on 85/2 to within 0.034
units) gives **10 · 12 · 13 · 15 · 17** — monotone. That is what shipped.

## What was snapped, counted

| step | W | wordmark left | cap top | baseline | cap-height | H stems | H crossbar |
|---|---|---|---|---|---|---|---|
| 24 | 89 | 52 | 7 | 17 | **10** | 2 / 2 | 2 |
| 28 | 104 | 60 | 8 | 20 | **12** | 3 / 3 | 2 |
| 32 | 119 | 69 | 10 | 23 | **13** | 3 / 3 | 2 |
| 36 | 133 | 78 | 11 | 26 | **15** | 3 / 3 | 2 |
| 40 | 148 | 86 | 12 | 29 | **17** | 4 / 4 | 3 |

Identical for all four masterbrand files, including the shifted `dark-mono`.

Per master (masterbrand): **12 H-glyph nodes** snapped on the whole-pixel ladder, **20 S/B/C nodes**
snapped to integer px because they sit on a straight `H`/`V` segment, **24 nodes and 58 control
points left scaled and untouched**. Across the 40 files: 240 H-glyph nodes, 400 curve-glyph nodes,
480 free nodes, 1,160 free control points. No control point anywhere was snapped; no curve was
reshaped by anything other than the sub-pixel move of an endpoint that a straight segment shares.

**One departure from the brief's letter, declared.** "Snap every coordinate to integer px" on the H,
read as independent nearest-integer rounding of each coordinate, was implemented, measured, and
rejected: at h=28 it produced an H with a **3px left stem and a 2px right stem**, because 2.583px
rounds one way at one phase and the other way at the other. What ships instead is delta
quantisation along each axis — anchor the first coordinate, then round each successive gap — with
the y-axis far end pinned to the baseline so the accumulated residual goes into a counter and never
into a stem. Both stems are equal at every step and the baseline lands exactly on its integer at
every step. The cost is that the H's overall width can differ from the pure-scaled width by up to
0.7px (h=28: 11px drawn against 10.315px scaled). I judged a symmetric H worth 0.7px of width.

A second, smaller mechanical fix: where a closed subpath's last on-path point coincides with its
`M` — the B's bowls and the H itself — the two are folded onto one shared node before snapping.
Without that, snapping moves the two apart and tears the outline open at the seam.

## What the screenshots show

Sandbox Chromium ran (Chrome Headless Shell 153, arm64). The recipe in project memory needed two
additions today, both recorded below. Console errors on the contact sheet: **0**, on two separate
loads.

At 1:1, 1280, all eight lockups on their correct grounds: **every lockup is crisp at every step.**
The hexagon reads as four clean triangles at 24 in both colour and mono, on white and on black; the
two diagonals are the only soft edges anywhere in the hexagon, which is geometry, not snapping — a
pixel probe of `hexagon-light-mono` finds exactly `4 · h` anti-aliased pixels per file (96 at h=24,
160 at h=40), i.e. the four diagonal edges and nothing else. Every vertical and horizontal edge in
every hexagon master is hard.

The wordmark, probed the same way: **zero anti-aliased pixels inside the H's box at every one of
the five steps**, with ink runs of 2/2 · 3/3 · 3/3 · 3/3 · 4/4 measured off the rendered bitmap.
The stems are genuinely whole-pixel, not nearly.

At 4× the wordmark is well-formed at all five steps — S, B and C all hold their counters, and the
masterbrand at 24 is legible. The one flaw visible at 4× and invisible at 1:1 is **inconsistent
horizontal stroke weight between letters**, which is what per-letter rounding of the S/B/C
`H`/`V` nodes buys: at h=24 the B's top and bottom strokes land at 1px while its middle bar and the
H's crossbar land at 2px (true scaled weights 1.49 and 1.42 — the *lighter* stroke got the extra
pixel); at h=40 the B's bar is 2px while its top and bottom are 3px and the H's crossbar is 3px.
Per lockup: hexagon-light-colour, hexagon-light-mono, hexagon-dark-colour, hexagon-dark-mono —
**crisp**; masterbrand-light-colour, masterbrand-light-mono, masterbrand-dark-colour,
masterbrand-dark-mono — **crisp at 1:1, crisp stems at 4×, with the B's horizontals a pixel off the
H's at 24 and 40**. Nothing broken anywhere.

Fixing that would mean quantising the vertical ladder jointly across all four glyph paths rather
than per path. The brief scopes S/B/C snapping to "the coordinates of straight H/V segments" within
each path, so I did not reach across paths. It is a named follow-on, not a defect I hid.

## What this lane did not do

- The masters are **not registered in `_logo_nodes.json`**. That is a follow-on, deliberately left:
  the four generators that undo hand-authored state were fenced and none was run.
- Whether any lockup may render at the 24px step stays open (`s282-D3`). The two measurements above
  that bear on it are published and not resolved here: the wordmark's cap-height at 24 is 10px with
  2px stems, and the B's horizontals sit a pixel under the H's crossbar.
- Clear space is the consumer's (`s282-D5`/`D6`); the masters carry none.
- The hexagon duplicate pair is untouched and still two files.
- No source export, `logos.md`, `_rulings.json` or anything under `showroom/` was edited. Nothing
  committed.

## Evidence

`notes/_lanes/284/logo-masters/` — `MASTERS-2026-09-18.html` (the contact sheet: 1:1 rack and a
`transform:scale(4)` rack per lockup, 0 console errors), `PROBE.txt` (all 40 parsed with
`xml.etree`, `name width height viewBox paths`), `_shoot.py` (the Chromium driver), `shots/`
(`panel-1x-1280.png`, `page-1280-light.png`, eight `1x-<lockup>.png`,
`4x-masterbrand-light-colour-24.png`, `4x-masterbrand-light-colour-all.png`, three `_z-` 3×
nearest-neighbour blow-ups of the 1:1 racks, and `zz.png`, a 4× crop of the 24px wordmark).

**Chromium recipe, two corrections for `chromium-in-sandbox-recipe`:** (1) `playwright install
chromium` fails today with `unable to get local issuer certificate` — node does not pick up the
sandbox CA bundle. `export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` fixes it, and
`chromium-headless-shell` is the smaller target that succeeds. (2) `apt-get download libxdamage1`
fails with `Unable to locate package` (no apt lists); fetching
`deb.debian.org/debian/pool/main/libx/libxdamage/libxdamage1_1.1.6-1_arm64.deb` directly and
`dpkg-deb -x`-ing it works, and `LD_LIBRARY_PATH=$HOME/.local/lib` is still the one library needed.

---

**Measured:** 40 masters on disk · 53,957 bytes · 0 files with a `viewBox` · 0 files with `fill` on
the root · 5 byte-identical pairs (the hexagon colour duplicate, at all five steps) · 160 float
artefacts normalised · 40 kink segments dropped · 240 H-glyph nodes and 400 curve-glyph nodes
snapped to integer px · 1,160 control points left unsnapped · 0 anti-aliased pixels inside the H's
box at all five steps · 0 console errors · `_gen_masters.py --check` exit 0 · 0 commits.
