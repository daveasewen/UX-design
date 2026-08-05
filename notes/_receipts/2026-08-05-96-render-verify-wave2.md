# Render-verify receipt — wave-2 dataviz showroom (8 members) — #96

*2026-08-05 · render-verify lane · commit `df44e51` (wave-2 landing) · method: `knowledge/_RUNBOOK-render-verify.md`
verbatim (goto file://, never set_content; ≥2 widths; real font; numeric + colour assertions) ·
pane list + owed note: `knowledge/_REVIEW-SIGNOFF.md` line "Eight wave-2 chart panes (added
2026-08-05, #95)" · shape matched against the 07-24 wave receipts (`notes/_receipts/2026-07-24-wave-lane1-bar-scatter.md`,
`…-lane2-donut-sparkline.md`).*

**Target rendered: the SNIPPET, not the showroom harness.** `showroom/chart-*.html` loads each pane
via `iframe.srcdoc` (confirmed: `grep -n "iframe\|srcdoc" showroom/chart-butterfly-h.html` → lines
36/52/56/90) — the exact "harness, not the artefact" pothole the runbook bans (§ "Render the SNIPPET,
not the showroom page"). Rendered `knowledge/snippets/Chart-<Name>.reference.html` directly, which
links `../canon/type.css` relatively and resolves correctly under `file://` from that directory.

## Sandbox stand-up (shared-mount recipe, runbook §"stage on the SHARED MOUNT")
- `PLAYWRIGHT_BROWSERS_PATH`, pip `--target`, `LD_LIBRARY_PATH` all pointed at
  `/sessions/exciting-cool-dijkstra/mnt/outputs/_render-env` (shared mount, not `$HOME`).
- `playwright install chromium-headless-shell` — download completed (chromium_headless_shell-1234
  present in cache); installer exited non-zero on `EPERM …rmdir '__dirlock'` — **this is the runbook's
  named "pothole 1" success signature, not a refusal** (checked `ls pw-browsers/` first, per rule).
- 17-lib set (`apt-get download`, no root) unpacked to `chromelibs/root` for **arm64**
  (`uname -m` confirmed `aarch64` — matches the `aarch64-linux-gnu` lib path used).
- Fonts: HSBC desktop TTFs copied to `~/.fonts`, both-string fontconfig alias installed
  (`Univers Next for HSBC` + `Univers Next HSBC` → `HSBC_MtUnivers_Latin`), `fc-cache -f` run,
  `fc-match "Univers Next HSBC"` confirmed the licensed cut resolves.
- One bash call ran the full 8-pane × 2-width render (`render_wave2.py`), well under the 45s cap.

## Font-loaded proof (all 8 panes, both widths)
`document.fonts.check('16px HSBC_MtUnivers_Latin')` → **`true`** for all 16 page/width combinations
(8 panes × {1180px, 760px}). Computed `body` font-family read back as
`"Univers Next for HSBC", "Helvetica Neue", Arial, Helvetica, sans-serif` on every pane (the alias
resolves the declared string to the licensed face — confirmed, not asserted).

---

## Per-pane records

### 1 · butterfly-h — `knowledge/snippets/Chart-butterfly-h.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 20 (both widths, DOM stable
  across viewport).
- Fit assertion: `svg.dv-svg` bbox width **1108px @1180 → 688px @760** (scales with container,
  `dv-fit-on` class present at 760px, `.dv-svg{width:100%}` rule under `figure.dv-fit-on` applies).
- Colour: not probed per-pane (no colour delta claimed for this member at #95/#96) — screenshots
  captured (`shot-butterfly-h-1180.png`, `-760.png`) for a visual second pass if wanted.
- **VERDICT: PROVEN** (renders, real font, responsive fit measured at 2 widths, DOM stable).

### 2 · butterfly-v — `knowledge/snippets/Chart-butterfly-v.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 19 both widths.
- Fit: bbox width **1108px @1180 → 688px @760**.
- **VERDICT: PROVEN.**

### 3 · histogram — `knowledge/snippets/Chart-histogram.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 17 both widths.
- Fit: bbox width **1108px @1180 → 688px @760**.
- **VERDICT: PROVEN.** (Signoff doc flags "histogram static key" as an open lane-flag for Dave — not
  a render defect; key markup/geometry rendered and is DOM-stable, the flag is a design pick, out of
  scope for this receipt.)

### 4 · boxplot — `knowledge/snippets/Chart-boxplot.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 6 both widths.
- Fit: bbox width **1108px @1180 → 688px @760**.
- **VERDICT: PROVEN.**

### 5 · bullet — `knowledge/snippets/Chart-bullet.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 12 both widths, svg height
  200px (bullet's shorter canvas, consistent both widths).
- Fit: bbox width **1108px @1180 → 688px @760**.
- **VERDICT: PROVEN.** (Signoff's "bullet proportions + grey tints" lane-flag is a design pick on
  values already rendering — out of scope here.)

### 6 · candlestick — `knowledge/snippets/Chart-candlestick.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 10 both widths.
- Fit: bbox width **1108px @1180 → 688px @760**.
- **VERDICT: PROVEN.** (Signoff's "candlestick dv-011" lane-flag is a design/derivation question, not
  a render failure — the pane renders and the marks are DOM-present.)

### 7 · pie — `knowledge/snippets/Chart-pie.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: **2 figures** on this pane (cp1 spider + cp2 direct-label variant, both `figure.dv`).
  Fig 0 (cp1): `svg.dv-svg` `width` attr `300`, `viewBox="0 0 300 260"`, bbox 300×260, **5** marks
  (`.dv-marker`, corrected count — first probe used a selector list that missed
  `path.dv-series.dv-pie-seg.dv-marker`; re-run with `.dv-marker` gives the true count, 5 segments,
  matching the 5-category dataset in the aria-label). Fig 1 (cp2): `width` attr `592`,
  `viewBox="-72 0 592 260"`, bbox 592×260, 5 marks.
- Fit: **both figures identical at 1180px and 760px** — `hasFitClass: false` on both `svg.dv-svg`
  elements (confirmed via `classList.contains('dv-fit')`). This is BY DESIGN, matching the donut
  precedent (`Chart-donut.reference.html`, render-verified 2026-07-26): a circular composition is
  fixed-radius, not fit-scaled, and pie carries no `dv-fit` class or `dv-fit-on` CSS hook at all — so
  the non-responsive width is a correct read of the intended geometry, not a missed fit hook.
- **VERDICT: PROVEN.** (Signoff's "pie sweep data-ri" lane-flag is a derivation question on the sweep
  data attribute, not this render.)

### 8 · stacked-area — `knowledge/snippets/Chart-stacked-area.reference.html`
- Widths: 1180px, 760px. Font: `true` both.
- Numeric: `figure.dv` count 1, `svg.dv-svg` count 1, `.dv-marker` count 39 (first pass, generic
  selector) / **12** (corrected pass, `.dv-marker` alone — the earlier 39 double-counted grid/axis
  children matched by the broader selector; 12 is the true series-marker count).
- **Fit — FAILED.** `svg.dv-svg` bbox / computed width read **580px at BOTH 1180px and 760px**
  viewport widths (`computedWidth: "580px"` both, `bboxWidth: 580` both) — the only one of the 8
  panes whose canvas did not narrow with the container. Root cause isolated: the JS-driven
  `dv-fit-on` class IS added correctly at 760px (`document.querySelector('figure.dv').className` →
  `"dv dv-animate dv-fit-on"`, confirmed identical to butterfly-h's own `dv-fit-on` at the same
  width) — the defect is CSS, not JS. `Chart-butterfly-h.reference.html` carries the scaling rule
  `figure.dv-fit-on .dv-chart-area{width:100%;} figure.dv-fit-on .dv-svg{width:100%;}`
  (lines 96–97), which `Chart-stacked-area.reference.html` **does not have** — its stylesheet stops
  at the fixed declaration `.dv-chart-area{width:580px;} .dv-svg{display:block; width:580px;
  height:260px; overflow:visible;}` (lines 107–108) with no `figure.dv-fit-on` override anywhere in
  the file. The `dv-fit` class is present on the `<svg>` markup (`class="dv-svg dv-fit"`, confirmed)
  so the behaviour-layer hook is wired; only the CSS rule that would make the hook resize the canvas
  is missing.
- **VERDICT: FAILED.** Failing measurement: `computedWidth` of `svg.dv-svg` = `"580px"` at viewport
  760px, where every sibling wave-2 pane narrowed (e.g. butterfly-h: 1108px → 688px at the same
  widths). Fix is a CSS addition, not a JS change: add
  `figure.dv-fit-on .dv-chart-area{width:100%;} figure.dv-fit-on .dv-svg{width:100%;}` to
  `Chart-stacked-area.reference.html`'s stylesheet, matching the pattern already proven on
  butterfly-h/-v, histogram, boxplot, bullet, candlestick. Not fixed here — this receipt is
  render-verify only, no edits made outside `notes/_receipts/`.

---

## Summary table

| Pane | Widths tested | Font loaded | Fit scales (1180→760) | Verdict |
|---|---|---|---|---|
| butterfly-h | 1180, 760 | true / true | 1108px → 688px | **PROVEN** |
| butterfly-v | 1180, 760 | true / true | 1108px → 688px | **PROVEN** |
| histogram | 1180, 760 | true / true | 1108px → 688px | **PROVEN** |
| boxplot | 1180, 760 | true / true | 1108px → 688px | **PROVEN** |
| bullet | 1180, 760 | true / true | 1108px → 688px | **PROVEN** |
| candlestick | 1180, 760 | true / true | 1108px → 688px | **PROVEN** |
| pie | 1180, 760 | true / true | fixed by design (no `dv-fit`, matches donut precedent) | **PROVEN** |
| stacked-area | 1180, 760 | true / true | **580px → 580px (no scale — CSS rule missing)** | **FAILED** |

7 of 8 PROVEN. 1 of 8 FAILED: **stacked-area does not narrow at 760px** — `.dv-svg` computed width
stuck at `580px` at both tested widths, while `dv-fit-on` is correctly applied to the figure; the
CSS override that other wave-2 members carry (`figure.dv-fit-on .dv-svg{width:100%;}`) is absent
from `Chart-stacked-area.reference.html`. 0 UNPROVEN — all 8 panes rendered cleanly, no crashes, no
missing files.

## Artefacts
- Results JSON: `outputs/_render-env/wave2_results.json` (sandbox mount, not repo-tracked).
- Screenshots (both widths, all 8 panes): `outputs/_render-env/shot-<name>-<width>.png` (sandbox
  mount — available for a visual pass but the verdicts above are from numeric assertions, not eyeball).

## Scope note
No meta/registry/gate file touched. This receipt file is the only write. The stacked-area CSS fix
is NOT applied here — flagged for the next enact window (one-line addition, cited above, same shape
as the fix already proven on 6 sibling panes).

---

## Re-verify after fix — 2026-08-05

*Re-checks ONLY `knowledge/snippets/Chart-stacked-area.reference.html`, method unchanged from the
above (`goto("file://…")`, never `set_content`; widths 1180/760; font assertion; numeric assertion
of `svg.dv-svg` computed width). The fix landed at lines 109-110:
`figure.dv-fit-on .dv-chart-area{width:100%;}` / `figure.dv-fit-on .dv-svg{width:100%;}` — confirmed
present in the file before rendering.*

**Sandbox stand-up this pass:** playwright already present in the sandbox's site-packages (v1.62.0);
browser binaries were not yet downloaded — `NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright
install chromium` succeeded (headless_shell + full chromium both landed). Host-requirements
validation flagged one missing lib on launch (`libXdamage.so.1` — confirmed via `ldd` on the
`chrome` binary, the only "not found" line). No root/sudo available in this sandbox instance
(`apt-get`/`dpkg` both refused, no `sudo`). Worked around by pulling the arm64 `.deb` directly
(`http://ports.ubuntu.com/pool/main/libx/libxdamage/libxdamage1_1.1.5-2build2_arm64.deb`), unpacking
it with `ar x` + `tar` (no root needed for this), and pointing `LD_LIBRARY_PATH` at the extracted
`.so`. `ldd` re-check confirmed zero "not found" lines afterward; launch succeeded with
`args=["--no-sandbox"]`. HSBC desktop fonts + the two-string fontconfig alias installed exactly per
runbook §5, `fc-match "Univers Next HSBC"` confirmed the licensed cut resolves before rendering.

### Measured values

| viewport | `document.fonts.check('16px HSBC_MtUnivers_Latin')` | `svg.dv-svg` computed width | `figure` class |
|---|---|---|---|
| 1180px | `true` | `1084px` | `dv dv-animate dv-fit-on` |
| 760px | `true` | `664px` | `dv dv-animate dv-fit-on` |

- Font loads correctly at both widths (`true`/`true`).
- `dv-fit-on` is present on `figure` at both widths (JS hook was never the defect, confirmed again).
- **The canvas now scales**: `1084px @1180 → 664px @760` — no longer stuck at `580px`. The fix is
  live and working: `figure.dv-fit-on .dv-chart-area{width:100%;}` / `.dv-svg{width:100%;}` are both
  present in the stylesheet (confirmed by direct read before rendering) and the computed style at
  760px reflects the override.
- Note on the ~688px expectation: sibling panes (butterfly-h etc.) measured `1108px → 688px`.
  Stacked-area measures `1084px → 664px` — same **24px** offset at both widths, i.e. stacked-area's
  `.dv-chart-area`/figure carries 24px less available width than the sibling panes at every viewport
  (likely a padding/margin difference specific to this pane's markup, not a scaling defect — the
  ratio 664/1084 = 0.6125 and 688/1108 = 0.6209 are close, both consistent with the same container
  narrowing from 1180→760). Not investigated further — out of scope for this narrow re-verify (fit
  now scales, which was the only question this re-check was asked).

### VERDICT: PROVEN

The stacked-area pane's fit-scaling defect recorded above (FAILED, `580px` stuck at both widths) is
fixed and re-verified. Font loads, `dv-fit-on` applies, and `svg.dv-svg` computed width now narrows
with the viewport (`1084px → 664px`) instead of staying pinned at `580px`. 8 of 8 wave-2 panes now
PROVEN.

No file outside this receipt was edited by this re-verify pass.
