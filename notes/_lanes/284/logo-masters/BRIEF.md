# #284 lane LM — the 40 per-size logo masters

**2026-09-18 · one Opus 5 build lane · conductor Fable 5.1 · evidence dir `notes/_lanes/284/logo-masters/`**

## THE JOB

Draw the 40 per-size logo masters that `s282-D3` calls for: **8 lockups × 5 height steps**, each
file carrying its **raw pixel height AND width as its own `width`/`height` attributes, with NO
`viewBox`**, coordinates absolute in that pixel space, **stems and horizontals snapped to the
pixel grid**. Source of truth is the 8 surviving Figma exports in `knowledge/assets/logos/`.

Dave's words (#282): *"no view boxes, just the raw height"* · *"and width obviously"*.

## PREMISES — measured at the brief seat, 2026-09-18

| premise | reading |
|---|---|
| exports present | 8 files: `{hexagon,masterbrand}-{light,dark}-{colour,mono}.svg` — identifier files are gone (`s282-D4`) |
| hexagon artwork | `width="170" height="85" viewBox="0 0 170 85"` — 2:1, all vertices at x ∈ {0, 42.5, 85, 127.5, 170}, y ∈ {0, 42.5, 85}; one vertex has a `9.15527e-05` float artefact and one edge a `42.3107 84.9311` kink — both Figma noise, not design |
| masterbrand artwork | `width="315" height="85" viewBox="0 0 315 85"` — the same hexagon at x 0–170, the wordmark HSBC at x ≈183–314.4, y ≈24–61; the H is straight lines only; S, B, C are cubic paths with straight stems/bars |
| colour files | hexagon: white square `M42.5 85H127.5V0H42.5V85Z` under four `#DB0011` triangles; masterbrand adds wordmark in `white` (dark) / `black` (light) |
| mono files | four triangles only, `white` (dark) / `black` (light); wordmark same ink |
| known, NOT blocking | `hexagon-light-colour` ≡ `hexagon-dark-colour` byte-for-byte except one float (the "duplicate pair") — draw both anyway, name it in the report |
| steps by RAW HEIGHT | **24 · 28 · 32 · 36 · 40** (`s282-D3` as corrected at `c143a1b`) |
| hexagon widths | 2 × h → 48 · 56 · 64 · 72 · 80 — every vertex lands on an integer or a .5 that is a grid line at h/2, h/4: at all five steps h/4 ∈ {6,7,8,9,10}, so the hexagon snaps exactly with no distortion |
| masterbrand widths | 315/85 × h = 88.94 · 103.76 · 118.59 · 133.41 · 148.24 → **round to the nearest integer px** (89 · 104 · 119 · 133 · 148); the wordmark, not the hexagon, absorbs the sub-pixel |
| disk / fill | `/sessions` 0.1% · FILL 147,056 real at cut — a render step is affordable |

## WHAT TO BUILD

1. **`knowledge/assets/logos/_gen_masters.py`** — a generator, not 40 hand files. Reads the 8 exports,
   emits the 40 masters. Re-runnable; idempotent; `--check` mode that regenerates to memory and diffs
   against disk (exit 1 on drift). Help-gate header like `_export-logos.py` (the `_helpgate` pattern).
2. **`knowledge/assets/logos/masters/<lockup>-<theme>-<mode>-<h>.svg`** × 40, e.g.
   `masterbrand-light-colour-32.svg`. Each: `<svg width="W" height="H" xmlns=…>` — **no viewBox**,
   no `fill="none"` on the root unless needed, paths in absolute px. Strip the Figma float noise
   (`9.15527e-05` → `0`, the `42.3107 84.9311` kink → the true vertex).
3. **Snapping rules** (report exactly what was snapped, per file, as counts):
   - Hexagon: every vertex to its exact grid position (h/4 multiples) — zero rounding error by
     construction.
   - Wordmark: the H is all `H`/`V` line commands — snap every coordinate to integer px so both stems
     and the crossbar are whole-pixel. For S, B, C: snap the coordinates of straight `H`/`V`
     segments (the B's stem and bars, the C's and S's terminals where they are flat) to integer px;
     **leave curve control points scaled but unsnapped** — do not reshape curves.
   - Snap the wordmark's overall left edge (x≈183 scaled) and the cap-height/baseline (y≈24 / y≈61
     scaled) to integer px first, then stems inside that box. Record the resulting cap-height in px
     per step.
   - Do not snap the hexagon-to-wordmark gap by moving the hexagon; the hexagon is fixed at x=0.
4. **`notes/_lanes/284/logo-masters/MASTERS-2026-09-18.html`** — the contact sheet for Dave's eye.
   Reuse the head/CSS idiom of `notes/_lanes/282/logo-review/LOGO-REVIEW-2026-09-17.html` (Swiss,
   sticky nav, `.label` eyebrow). Inline all 40 SVGs **at 1:1, `image-rendering` untouched, no CSS
   scaling**, on the correct ground per theme (light files on white, dark files on black), one row
   per lockup×variant, five steps across, height labelled under each. A second panel shows each step
   at **4× via `transform: scale(4)` with `transform-origin: top left`** so stem crispness is
   inspectable. ⚠ Obey the label-crop rule: no line-height that crops glyph ascenders/descenders in
   labels; test at the smallest label size. Console errors 0.
5. **Screenshots** with the sandbox Chromium (see `chromium-in-sandbox-recipe` in project memory if
   needed; `goto("file://…")`, never `set_content()`): the 1:1 panel at 1280 light, and one 4× crop of
   `masterbrand-light-colour-24` — into `notes/_lanes/284/logo-masters/shots/`. **Then look at
   them** and say in the report what you saw, per lockup: crisp / soft / broken.
6. **Probe file** `notes/_lanes/284/logo-masters/PROBE.txt` — the output of a one-liner that parses all
   40 with an XML parser and prints `name width height viewBox(None) paths`.

## FENCES

- ⛔ Do NOT run `_build_all.py`, `gen_kg_icons.py`, `land_rests_on.py`, `gen_kg_rules.py` — the four
  generators that undo hand-authored state. The masters are NOT registered in `_logo_nodes.json` by
  this lane; say so in the report as a follow-on.
- ⛔ Do NOT edit the 8 source exports, `logos.md`, `_rulings.json`, or anything under `showroom/`.
- ⛔ Do NOT commit. The conductor commits via `knowledge/_git_commit.sh`.
- ⛔ No pip installs beyond what the recipe needs; scratch only under this lane's dir or `~/tmp`.
- No `viewBox` on any master. No `<g transform>` scaling — coordinates are literal.

## DO NOT RULE

- Whether any lockup may render under x-small (24 px) — open by `s282-D3`.
- Clear space — ruled `s282-D5`/`D6`; the masters carry NO padding, clear space is the consumer's.
- The hexagon duplicate pair — Dave's; do not merge the files.
- Whether the sub-pixel masterbrand width should round or floor — take **round**, name it as a
  choice in the report, and give the alternative's numbers.

## RETURN CONTRACT

File the full report at **`notes/_subreports/2026-09-18-284-LM-logo-masters.md`** (the #282 LL
report is the shape: title, byline with brief + evidence paths, prose sections, a measured-counts
footer line). Return to the conductor ONLY: the report path, the file count on disk, the `--check`
exit code, the probe line for `masterbrand-light-colour-24`, and one sentence on what the
screenshots showed. Every number measured, none recalled; where a measurement disagrees with this
brief, publish both.
