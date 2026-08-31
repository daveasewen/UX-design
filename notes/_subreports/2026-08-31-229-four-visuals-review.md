# Sub-report — #229 four-visuals review page (Opus build sub)

**Brief:** `notes/_briefs/2026-08-31-229-four-visuals-review-brief.md`
**Owned paths, both written, nothing else touched:**
- `reviews/FOUR-VISUALS-2026-08-31-v1.html` (37.4 KB)
- `notes/_subreports/2026-08-31-229-four-visuals-review.md` (this file)

No git operations. No `_rulings.json` access. No W-row, state, memory, regen or `_build_all.py`.
Verified at handover: **0** `.uuid` fontconfig strays in `knowledge/assets/fonts/_desktop/TTF/`, and
the only file under the repo root with a fresh mtime attributable to this sub is the review page.

---

## 1 · What was built

One page, four specimens, all live. Scaffold pattern from
`reviews/FAB-READINGS-2026-08-30-v1.html` (#227) — sticky control bar, live controllers, contained
FAB panes, plain-language notes beside each specimen.

**One deliberate change from that scaffold, and it is an improvement, not an invention.** The #227
page *inlined* copies of canon's short aliases because it did not link `canon.css`. This page **does**
link `knowledge/canon/canon.css` (and `type.css`), so the aliases are read from canon's own
`SEMANTIC ALIASES` block (canon.css §"Declared on `:root` AND `[data-theme]`"). **No hex is authored
anywhere on the page.** That block is also what `apollo-fab.js` probes for at mount — confirmed live,
`tokenMode = "canon"` in both modes, so the FAB inherits the page rather than falling back to its hard
neutral pair.

**Specimens copy the artefacts; nothing is re-drawn.** The reference markup for Search-field and
Segmented-control sits in two `<template>` blocks, lifted verbatim from
`knowledge/snippets/Search-field.reference.html` and
`knowledge/snippets/Segmented-control.reference.html`. Every cell is a `cloneNode` of that one
template — which is what makes the eight cells provably identical to each other *and* to the snippet.
The reference's own two behaviour scripts (the clear-button handler, the sliding-indicator
`moveInd`/`placeAll`) are copied verbatim too. The icon sprite is the snippet's two `<symbol>`s.

**Layout.** Specimens 1 and 2 are shown as the FULL SPREAD — 4 themes × 2 modes, each cell carrying
its own `data-apollo-theme` + `data-theme`, following the approved precedent in
`reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html`. That is why there is **no page-level theme switcher**:
all four themes are on screen at once, pinned, rather than three of them hidden behind a control. The
page-level controllers are: chrome light/dark, "Show the 72 px zone", "Reset page attributes",
"Re-measure".

**Live measured readouts** under each specimen (`getComputedStyle`, recomputed on demand and on any
mutation of the root theme attributes). Every claim the page makes about a number is a number the page
took off itself, not prose.

---

## 2 · What was rendered, and what was SEEN

Render-verify ran in-sandbox, headless Chromium + Playwright, `goto("file://…")` (never
`set_content()`), real HSBC cut asserted with the runbook's **canvas probe and two controls**, not
`fonts.check()`:

| probe | measured | reading |
|---|---|---|
| `HSBC_MtUnivers_Latin` | **347** | the real cut |
| `"Univers Next HSBC"` (type.css `--uf`) | **347** | alias resolves |
| `"Univers Next for HSBC"` (snippet `--font`) | **347** | alias resolves |
| `DejaVu Sans` — control | 375 | genuinely different face |
| nonexistent face — control | 301 | default fallback |

Both aliases land on the target and on neither control. **Font GREEN.**

PNGs (NON-REPO: `/sessions/determined-affectionate-euler/mnt/outputs/_r229`, `_r229b`, `_r229c`),
25 + 17 + 10 shots across four passes. **Every one listed below was read back by eye.** Two viewport
widths, 1440 and 700; light and dark chrome; and a throwaway `full_page` shot before each measured
capture (#217 reflow pothole).

### Specimen 1 — L8, the underline stays straight — **SEEN light + dark**
`01/02/03/04`. Console light and console dark: the **boxed** field carries a visible 8 px corner; the
**underline** below it is a straight stroke with square ends. Mono light and Supercharge dark as
controls: both variants square. The difference Dave overruled the precedent on is plainly visible in
the console column and absent everywhere else, which is exactly the shape of the ruling.

Measured, all eight cells, **all `as canon`**:

```
theme        mode   .search (underline)   .search.boxed
mono         light  0px                   0px
mono         dark   0px                   0px
legacy       light  0px                   0px
legacy       dark   0px                   0px
console      light  0px                   8px
console      dark   0px                   8px
supercharge  light  0px                   0px
supercharge  dark   0px                   0px
```

### Specimen 2 — s227-D7, concentric thumbs at m and l — **SEEN light + dark**
`05/06/07/08/09/10/10b`. Console light and console dark, all four scales: track and thumb both
rounded, and the thumb's curve sits inside the track's. The `l · 48` crop (`10`) beside the same
control in mono (`10b`) is the pair that carries the verdict — 12 px track / 8 px thumb versus square
on both. Mono light and Legacy dark are square at every scale, as s201-D5 requires. **No 8 px appeared
in any non-console column**, which the brief asked me to stop and report if it did.

Measured, all eight cells, **all `as canon`** (`track / thumb` per scale):

```
theme        mode   xs         s          m           l
mono         *      0/0        0/0        0/0         0/0
legacy       *      0/0        0/0        0/0         0/0
console      light  6px/4px    8px/6px    10px/8px    12px/8px
console      dark   6px/4px    8px/6px    10px/8px    12px/8px
supercharge  *      0/0        0/0        0/0         0/0
```

Worth Dave's eye, stated as an observation and **not** a defect: the m and l thumbs are the *same*
number (8 px) although their tracks differ (10 and 12). That is the concentric rule doing its job —
10 − 2 and 12 − 4 both land on 8, because the l pad is 4 and the m pad is 2. Two different tracks,
one thumb radius, and it is correct.

### Specimen 3 — the library icon on the FAB face — **SEEN light + dark**
`11/12/B/H`. The face is the real overlay's, mounted with `reveal:'always'` **in that pane only** so
the glyph can be looked at without hunting; the page says so beside it. Zoom crop `12` shows the
settings glyph clean at 24 px in the 56 px disc. Read off the live DOM: face `<svg>` viewBox
`0 0 18 18`, **path count 1** — the library file's single evenodd path, not a hand-assembled glyph.
Dark pass (`H`): the FAB re-themes with the page, dark surface and light glyph.

**One thing the render taught me and the page now says:** the disc is *ink*, not brand red, because
`--af-pri` resolves `button/primary/background/default` and **this page is mono, whose primary action
is ink**. Measured: `--pri` on the root is `#DB0011`, but the button's computed background is
`rgb(26,26,26)`. That is the overlay inheriting the host correctly. Dave will otherwise reasonably
expect red, so a sentence was added beside the specimen naming the token and saying that the FAB's own
**Common** button turns it red.

### Specimen 4 — the hot-corner reveal — **SEEN light + dark, and DRIVEN with two negative controls**
`13/14/15/C/D/E/F/O`. This pane is mounted with **no `reveal` and no `cornerSize` argument at all**, so
it is showing the file's own defaults rather than a configuration I chose. Read back live:
`fabCorner.reveal = "hotcorner"`, `ApolloFAB.CORNER_DEFAULT = 72`, `fabCorner.cornerSize = 72`,
`ApolloFAB.version = "1.0.1-228"`.

Driven with `page.mouse.move`, four positions, in order:

| pointer at | `data-revealed` |
|---|---|
| (page load, no move) | `false` |
| centre of the pane — control | `false` |
| 100 px in from each edge, i.e. **just outside the 72 px zone** — control | `false` |
| 24 px in from each edge, **inside the zone** | **`true`** |

Button opacity `0 → 1` across that move. **The instrument can fail and did not** — the two negative
controls are what make the positive mean something. `15`/`D` show the 72 px zone drawn by the page's
hint toggle; `F` shows the panel opened, legible, with the theme/mode/inspect controls. The page names
the corner in words (bottom-right), states the 72 px number, tells Dave to move his mouse, and carries
an on-canvas "the corner is here ↘" marker.

### Page itself
- **Light and dark chrome both seen** (`A`/`G` bar, `L` intro both modes, `I` footer dark,
  `K`/`J` readouts both modes). Legible throughout.
- **Responsive seen at 700 px** (`M`/`N`/`O`/`R`): the spread and the FAB grid collapse to one column,
  and the readout tables scroll **inside their own container** — the body never scrolls horizontally.
- **Verdict ink corrected during the build.** The readout first used `--ok`/`--err` (RAG *fill* tokens).
  Changed to the background-keyed pair `--rag-success-ink` / `--rag-error-ink` — the two-red law
  (s151-D1) and its green mirror (s155-D1). Measured after the fix: `#137F3C` on light, `#66CC8D` on
  dark. Both declared in canon on `:root` and `[data-theme="dark"]`, so they re-resolve per chrome block.
- **Mutation test on the readout.** Forced `border-radius:10px` onto one mono `.seg.m` and re-measured:
  that row went `DIFFERS`, tinted, naming `10px / 0px ≠ 0px / 0px`. The green in the tables is a green
  that **can** go red.
- **Console errors:** exactly two, both the expected `file://` fetch refusal for
  `apollo-fab-meta.json`. That is the overlay's documented default-safe path, not a failure. Zero
  page errors.

---

## 3 · Two authoring defects the render caught, both fixed

Recorded because neither was visible in the source and both were only found by looking at pixels.

1. **The FAB stages inherited none of the specimen layout.** The template is cloned into two places —
   the spread cells and the FAB stages — but the layout rules were scoped `.cell …` only. In the
   stages the labels rendered at body size and the `.row` lost its flex, so the pane content stacked
   and overflowed. Fixed by scoping those rules to `.cell` **and** `.stage`.
2. **Two scale labels read wrong outside console.** `m · 44 — thumb 8px in console` was correct but
   confusing where the thumb is square. Reduced to `m · 44` / `l · 48`; the console fact stays in the
   specimen's prose and in the measured table.

---

## 4 · The one behaviour Dave must be told about, and it is on the page

**The FAB's Theme buttons write `data-apollo-theme` onto `<html>`, and canon has no
`[data-apollo-theme="mono"]` block.** Mono *is* the base, so there is nothing to reset to, and a theme
set at the root inherits straight down into the four pinned columns. **Driven and confirmed:** clicking
the FAB's **Console** turned every column's segmented control to `6/8/10/12` + `4/6/8/8`, and the
measured table correctly reported four themes as `DIFFERS`. **Reset page attributes** restored all
eight rows to `as canon`.

I deliberately **did not** guard against this by pinning values into the page. The brief says: *"if you
see 8px on mono, something is wrong; stop and say so rather than 'fixing' it."* A guard that forced 0
on mono would have hidden exactly the fault I was told to report. Instead the page (a) warns in plain
words before Dave touches the FAB, (b) offers **Reset page attributes**, and (c) re-measures on any
root attribute mutation, so the table can never quietly disagree with the pixels.

---

## 5 · UNPROVEN — declared, not estimated

- **Dave's real browser.** Everything above is headless Chromium in the Linux sandbox at 1440 and 700.
  Not seen in Chrome on the Mac.
- **Touch.** The tap-in-the-corner path (`pointerdown`, non-mouse `pointerType`) was **not driven** —
  no touch device. Only the mouse path is proven.
- **Served over HTTP.** `apollo-fab-meta.json` cannot be fetched on `file://`, so the inspector's
  **full** meta state — category, purpose, token verdict — is unproven here. Only the default-safe
  class-name path was exercised, and only implicitly.
- **Inspect components.** The inspector's hover highlight and tooltip over the in-stage `cn-*`
  components were **not driven**. The switch was seen in the open panel; its behaviour was not.
- **Focus-visible rings** on the review chrome and on the specimens: not driven.
- **`prefers-reduced-motion`** branch: not driven.
- **Third viewport.** Two widths only. Nothing is claimed about intermediate widths.
- **Print / high-contrast / forced-colors:** not looked at.

---

## 6 · RULING-SHAPED — undecided, for the conductor

Nothing here is ruled by me; each is put as a question.

1. **`REVEAL_DEFAULT` is not on the exported API surface.** `ApolloFAB` exports `CORNER_DEFAULT` and
   `Z_DEFAULT` but not `REVEAL_DEFAULT`. A consumer can only learn the default reveal by mounting an
   instance with no `reveal` and reading `.reveal` back — which is what this page does. Should the
   third constant be exported alongside its two siblings? Not mine.
2. **Canon has no `mono` reset block.** §4 above is a general property, not a property of this page:
   any consumer that sets `data-apollo-theme` on a *subtree* is defenceless against a theme set at the
   root, because mono is the absence of a block rather than a block of base values. A
   `[data-apollo-theme="mono"]` block re-declaring the base would close it. Whether that is worth
   doing — and whether it belongs to the theme generator lane — is a decision, not a build.
3. **The `.seg.lg` ordinal-vs-nearest-height map** is still marked PROPOSED in both the snippet and
   canon (`reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html` draws both readings). This page shows only
   the minted `xs/s/m/l` grammar, which is what the brief named; the legacy mini ramp is untouched and
   that disagreement is still open. Flagged so it is not assumed closed by this page's greens.

---

## 7 · REPLAY-THESE — sandbox, for the conductor

**The sixth-stratum recipe in `knowledge/_RUNBOOK-render-verify.md` could not be followed verbatim:
this sandbox is FRESH.** `/var/tmp/pylibs`, `/var/tmp/pw-browsers-220` and `<MOUNT>/outputs/syslibs`
**do not exist** — #227's orphaned survivors are gone. Disk was healthy (`/` 50 %, 4.9 G free;
`/sessions` 67 %, 3.2 G), so this was a rebuild, not an ENOSPC. The runbook's own stated CLASS FIX
("wheels unzipped to the MOUNT, browsers path on a MOUNT dir, libs `dpkg -x`'d to the MOUNT") is what
worked, and this is what it looks like in practice:

```bash
M=<MOUNT>/outputs/_render-env-229
pip install --no-cache-dir --target $M/pylibs playwright      # TMPDIR=/dev/shm
export TMPDIR=/dev/shm PYTHONPATH=$M/pylibs PLAYWRIGHT_BROWSERS_PATH=$M/pw-browsers
export NODE_TLS_REJECT_UNAUTHORIZED=0 NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
python3 -m playwright install chromium-headless-shell        # exits 1 on __dirlock EPERM — LANDED
export LD_LIBRARY_PATH=$M/chromelibs/root/usr/lib/aarch64-linux-gnu
export FONTCONFIG_FILE=$M/fonts.conf                          # farm + cachedir on the MOUNT, never the repo
```

**Three things the runbook does not currently say, all first-hand today:**

1. **`apt-get download` has NO SOURCES on this box.** It exits **100** with
   *"Can't find a source to download version … of libxcomposite1:arm64"* for every package — which
   reads as "the recipe is broken" and is not. The deb must be fetched directly:
   `curl -fsSL http://ports.ubuntu.com/ubuntu-ports/pool/main/libx/libxdamage/libxdamage1_1.1.5-2build2_arm64.deb`
   then `dpkg -x`. **`ldd` first**: only `libXdamage.so.1` was missing, exactly as at #227 — one deb,
   ~7 KB, not the eleven-package set.
2. **The font farm works on the OUTPUTS mount**, not only `/var/tmp`. `<MOUNT>/outputs/_render-env-229/fonts`
   with `<cachedir>` alongside it: 404 faces visible (so the `<include>` took), 10 HSBC, and **0**
   `.uuid` strays in the repo TTF dir afterwards. Preserves #138's whole point without needing `/var/tmp`.
3. **`page.screenshot(clip=…)` clips in VIEWPORT space unless `full_page=True`.** An element below the
   fold raises *"Clipped area is either empty or outside the resulting image"*, which reads as a bad
   selector. Take document-space coordinates (`rect + scrollX/scrollY`) and pass `full_page=True`.
   Cost one wasted pass. Pairs with the #217 note already in the runbook rather than replacing it.

I did not edit the runbook — outside my two paths.

---

## 8 · Cost line

- **Token spend: UNOBSERVABLE from inside this sub.** I have no instrument for my own window here and
  will not estimate one. The conductor's `_checkin.py` at the seam is the only honest figure; this
  line exists so it is not silently omitted.
- **Observable proxies:** 1 page authored (37.4 KB) + 1 report. ~33 sandbox bash calls, of which 4 were
  render passes, 8 were environment build-out and the rest were reading the artefacts and canon.
  52 PNGs written, **26 read back by eye** (the remainder are throwaways and duplicate crops of a shot
  already seen). 5 file-tool edits to the page after the first render pass. 0 git operations, 0 writes
  outside the two owned paths.
- **Wall:** the environment rebuild (pip → browser → lib → fonts) was ~4 calls before the first pixel;
  each render pass ran well inside one call. No call-boundary loss.
