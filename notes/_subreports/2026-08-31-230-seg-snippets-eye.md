# Sub-report — #230 Lane B: the four fixed seg snippets, rendered for Dave's eye

**Brief:** `notes/_briefs/2026-08-31-230-seg-snippets-eye-brief.md` · row W-313 · conductor Fable
**Deliverable:** `reviews/SEG-SNIPPETS-2026-08-31-v1.html` (54,356 bytes, 773 lines)

**W-307's close condition is now servable: all four snippets it fixed are on a page, rendered live
from the real artefacts, four themes × light/dark, with a REAL `:hover` driven and asserted. The two
reasoned `$exempt` members sit beside them as three-way decision cards.** No git operations, no
`_rulings.json`, no W-rows, no `_state.json`, no memory writes, no snippet/canon edits, no change to
W-307.

---

## COUNTS:

```
COUNTS: page 1 (reviews/SEG-SNIPPETS-2026-08-31-v1.html, 54,356 B, 773 lines) · specimens 6
  spliced verbatim + 2 calibration controls · cells 50 (6 spreads × 8 theme/mode + 1 calibration
  spread × 2) · segmented controls rendered 62 · radius readings taken 32/32 on the four fixed
  (8px/6px/6px console, 0/0/0 mono+legacy+supercharge) · real-hover assertions 6/6 hovered:true
  with the held-hover switch OFF · hover-contrast measurements 8 · PNGs produced 38, READ BY EYE 16
  distinct files (19 reads) · sandbox bash calls 24 · files written 3 (1 page + 1 report +
  1 gitignored builder pair) · files written outside outputs/ + notes/_subreports/: 0 ·
  git operations 0 · rulings 0
```

---

## 1 · What is on the page, and why it is not a drawing

Six specimens. **Every one is spliced VERBATIM out of its reference file** by a balanced-tag
extractor in `outputs/_gen-230/build.py` (gitignored scratch) — no markup was retyped, reformatted or
reconstructed. Style comes entirely from the built `knowledge/canon/canon.css`, reached through the
generated `.cn-*` scopes and `[data-apollo-theme]`/`[data-theme]` — the path a real Apollo page takes.
The page authors **one** rule of its own, and it paints a hover *background* with canon's own
`var(--hover)`; it authors no geometry, no radius and no colour anywhere.

| # | specimen | source | what it adds |
|---|---|---|---|
| 1 | View options | `View-options.reference.html` | the smallest surface; 2 segments |
| 2 | Template — dashboard | `Template-dashboard.reference.html` | **two** controls in one file — the check that the injected contract reaches every instance, not just the first |
| 3 | Template — list index | `Template-list-index.reference.html` | icon + label, widest segments |
| 4 | Template — report | `Template-report.reference.html` | pressed segment sits **between** two others, so both thumb ends are interior |
| C | **Calibration** | atom `.seg.s` + View-options + atom `.seg.m` | see §4 — a question the numbers raised, put in pixels |
| 5 | `$exempt` Table | `Table.reference.html` | demo-harness switcher + decision card |
| 6 | `$exempt` Tab-bar | `Tab-bar.reference.html` | mobile pill lozenge + decision card |

Controls: page-chrome light/dark, a **Held hover** switch (default on), and Re-measure. Every number
on the page is read off the live boxes at runtime; nothing is transcribed.

## 2 · The repair, measured — 32/32

Read off the live render, per specimen × theme × mode, `track / thumb / hover-box`:

| theme | mode | all four specimens |
|---|---|---|
| mono | light · dark | `0 / 0 / 0` |
| legacy | light · dark | `0 / 0 / 0` |
| **console** | **light · dark** | **`8px / 6px / 6px`** |
| supercharge | light · dark | `0 / 0 / 0` |

Mono, Legacy and Supercharge stay 0 everywhere as ruled (`s201-D5`). Console rounds. Template-dashboard
contributes **two** controls per cell and both read identically, so the partial's contract reaches the
second instance in a file. The hover column is read off an **unpressed button's own** computed radius,
so it is true with the held-hover switch off.

## 3 · SEEN — and the real hover, asserted not assumed

The held-hover switch is a mirror, not a proof. The proof was driven: **switch OFF**
(`forced:false`), synthetic pointer on a real segment, `el.matches(':hover')` asserted in the same
`evaluate` as the computed read, screenshot taken in **viewport space** (never `full_page` — it drops
the hover, replayed from #229 and held).

| shot | `hovered` | `background` | `border-radius` |
|---|---|---|---|
| View-options · console · light | **true** | `rgb(240,240,240)` | **6px** |
| View-options · console · dark | **true** | `rgb(35,35,35)` | **6px** |
| View-options · **mono** · light | **true** | `rgb(240,240,240)` | **0px** — the control |
| Template-report · console · light | **true** | `rgb(240,240,240)` | **6px** |
| Template-list-index · console · light | **true** | `rgb(240,240,240)` | **6px** |
| Template-dashboard · console · light | **true** | `rgb(240,240,240)` | **6px** |

`ASSERT hovered-all: True`, 6/6.

**Looked at, by eye** (16 distinct PNGs, 19 reads, all in `outputs/_shots-230/`, gitignored):
`realhover-view-options-console-{light,dark}.png` and `realhover-view-options-mono-light.png` are the
decisive pair — the console shot shows the grey hover fill and the black thumb meeting with two 6 px
corners and a lens of light between them; the mono shot is the same control, same real hover, dead
square. `crop-report-thumb-corner.png` is a 1600-px magnification of Template-report's interior thumb
corner: unambiguously rounded on all four corners. Plus both `top-{light,dark}.png`, six `sec-*` section
sheets, and two console zooms.

---

## 4 · RULING-SHAPED QUESTIONS — found, NOT decided, NOT touched

**① The two `$exempt` members — the decision the brief asked for. Both are on the page as cards.**

- **`Table` — the demo-harness switcher.** Renders square in all four themes; `border-left` dividers,
  no `.ind`, active by background + `disabled`. Options laid out: **join** (interior corners would round
  *against* the dividers, and a thumb radius lands on a control with no thumb — likely forces the
  dividers out too), **stay exempt** (nothing moves; reads as demo scaffolding not product surface),
  **restyle onto the atom's construction then join** (changes shape and gains motion in *every* theme).
- **`Tab-bar` — the mobile pill.** `999px` on track and indicator, in **every** theme — it is not on the
  ramp at all. Options: **join** (the lozenge stops being a lozenge in Mono/Legacy/Supercharge, which mint
  0 — the most visible change available on this page, and it would reverse Dave 2026-07-24), **stay
  exempt** (nothing moves, but the **name collision** stays: two unrelated atoms both call their track
  `.seg`, and the membership scan must carry a written exemption forever), **rename then stay exempt**
  (`.pill`/`.navpill` — no pixels move, the collision goes, the exemption entry can be *deleted* rather
  than maintained). *My reading, not a ruling: the third option is the only one that removes the finding
  rather than restating it — but it is Dave's.*

**② ★ NEW — the four repaired controls are 42 px tall and wear the 36 px rung's corner.**
Measured on this lane, not previously reported. The minted ramp is `xs 28 · s 36 · m 44 · l 48`, and
Console mints container/thumb pairs `6/4 · 8/6 · 10/8 · 12/8`. All four snippets bind the **`s`** pair
and so take **8/6** — but their `.seg button{height:40px}` inside a 1 px frame puts the control at
**42 px**, six above the `s` rung and two below `m`. Nothing is broken: the binding is consistent and
the number on the box equals the number in the store. The question is only whether a 42 px control
should wear the 36 px rung's corner or the 44 px rung's. **The calibration strip on the page puts all
three side by side in Console light and dark so it can be answered by eye rather than argued.**

**③ ★ NEW — and the height itself is a raw literal.** `height:40px` is hardcoded in all four
`.seg button` rules. These files never read `--seg-h`/`--size-segmented-control-*` at all, so they are
not on the size ramp in any sense — only the radius joined the group. Whether the segmented **height**
should be minted too is unasked; the partial group's scope is deliberately narrow (radius only) and
widening it is Dave's, not a generator's.

**④ The flush-vs-inset construction, now visible rather than described.** The atom carries a 2 px
track padding so its thumb floats with a gap all round; all four repaired files are **flush**, the
thumb inset only by the 1 px border. The minted pair is a *tuned dial* (container − 2, `s202-D2`), not
a strict derivation, so a flush thumb lands ~1 px under exact concentricity and an inset one ~1 px
over — the same tolerance the eight files repaired at #227 already ship. Their headers say so and flag
adopting the atom's inset as *not taken*. The calibration strip makes the difference legible for the
first time.

**⑤ ★ NEW — the hover state is 1.05:1 against its own track in EVERY dark theme.** The corner is
correct in dark (6 px, measured). The **fill carrying it is all but invisible.** Measured live off the
two painted boxes:

| theme | light | dark |
|---|---|---|
| mono | 1.14:1 | **1.05:1** |
| legacy | 1.14:1 | **1.05:1** |
| console | 1.14:1 | **1.05:1** |
| supercharge | 1.24:1 | **1.05:1** |

This is **not** a #229 or #230 regression — `tertiary/background/hover` has always been this. But it
means the hover affordance Dave asked about in #229 is, in dark mode, something a user cannot see at
all, let alone judge the shape of. It is measured and surfaced **on the page**, above the specimens,
because it governs what his eye can honestly report there. Whether the hover step should widen is a
token decision and is untouched.

**⑥ Carried forward, unresolved, from #229 §6 — not re-litigated here.** The focus ring rounds with the
hover box (same box); the FAB shadow/press-physics/panel divergences; `fab/size` still untokened; the
legacy ordinal map still PROPOSED.

---

## 5 · UNPROVEN — declared, not hidden

1. **The four snippets were verified as RENDERED THROUGH CANON, not as standalone files.** Opening
   `View-options.reference.html` directly gives its own mono-base `--seg-rad-s:0`, so the console corner
   only exists on the canon path. That is the correct path and the one a product page takes — but a
   reader who opens the snippet in a browser will see squares, and nothing on this page says so.
2. **`Template-settings`, the charts and `Filter-toolbar-bar` are not on this page.** They were #227's
   and #229's scope. This lane shows the four that were missed, plus the atom twice as calibration.
3. **No gate was run.** This lane is a render/eye lane; it changed no source, so `_validate_*`,
   `--assert-mint` and the regen serial were deliberately not invoked. Their green from the Lane A fix
   stands on that lane's evidence, not mine.
4. **The decision cards' radio buttons write to nothing.** They are a local scratchpad; the page says so.
5. **Responsive was not driven.** The page has breakpoints at 1000 px and 860 px; only the 1400 px
   viewport was rendered.
6. **Focus-visible was not photographed.** The focus ring shares the box and therefore the corner, but I
   drove `:hover` only, and I am not calling reasoning a proof.

---

## 6 · REPLAY-THESE

1. **★ The persisted render env is SESSION-PATH BOUND, and it fails SILENTLY.**
   `outputs/_render-env-229/` *did* survive on the mount this time (contradicting #229's REPLAY note —
   the pylibs, `pw-browsers` and `chromelibs` legs all worked verbatim, saving ~4 calls). But its
   `fonts.conf` hardcodes `/sessions/determined-affectionate-euler/...` and **every font symlink points
   at the old session path**, so the whole HSBC farm was dangling. The font control probe caught it:
   `HSBC 608.03 == nonexistent 608.03`, Arial differing — i.e. the real cut was NOT resolving and every
   pixel would have shipped with fallback metrics while looking perfectly plausible. Rebuild
   `fonts/` + `fonts.conf` per session (2 minutes); after that, `HSBC 701.57 / Arial 679.47 /
   nonexistent 608.03`, differing from both controls. **Run the three-way font probe before believing
   any type on any shot.**
2. **★ canon has NO `[data-theme="light"]` block.** Light is defined on `:root`; only dark is a
   selector. So a cell pinned `data-theme="light"` **inside** a dark ancestor inherits dark and
   silently mislabels itself — my first dark pass produced a spread whose cells said LIGHT and rendered
   black. Stamp the chrome theme onto chrome blocks (`[data-chrome]`), **never onto `<html>`**. This is
   exactly what `reviews/FOUR-VISUALS-2026-08-31-v2.html` already does at line 646, for this reason, and
   I re-derived it the expensive way instead of reading the approved page's toggle first.
3. **`element.screenshot()` re-scrolls its element and undoes a prior `scrollBy`.** A sticky control bar
   therefore lands painted over the section head in every section shot. Un-stick the bar for the shot
   (`style.position='static'`); scrolling around it does not work.
4. **A themed chrome block must span the page.** `max-width` on the *themed element* leaves a light
   gutter beside it in dark mode. Cap the measure on its **children** instead.
5. **A shrink-to-fit cell silently squashes a full-width mobile control, and no number catches it.**
   The Tab-bar lozenge collapsed to 106 px with its four 24 px glyphs overlapping — while the readout
   cheerfully reported `999px / 999px`, correct and useless. **Only the eye caught it.** When a specimen
   is a mobile full-width component, give its scope box `width:100%` and let the snippet's own
   `max-width` do the capping.
6. `full_page=True` drops a synthetic `:hover` — #229's finding, replayed and held. Viewport-space
   `clip=`, and assert `matches(':hover')` in the same evaluate.
7. **PIL is available in the sandbox.** `from PIL import Image` works, so a suspect corner can be
   cropped and magnified from an existing PNG without another browser call. This settled a "does that
   thumb actually round?" doubt in one call instead of a re-shoot.

---

## 7 · Files written — nothing else

**Mine, authored:**
- `reviews/SEG-SNIPPETS-2026-08-31-v1.html` — the deliverable (54,356 B)
- `notes/_subreports/2026-08-31-230-seg-snippets-eye.md` — this file
- `outputs/_gen-230/{build.py,shoot.py}` — the generator and the render harness (**gitignored**;
  `build.py` is the page's provenance and is cited on the page itself)
- `outputs/_shots-230/*.png` — 38 shots (**gitignored**)
- `outputs/_render-env-230/{fonts.conf,fonts/,fccache/}` — the per-session font farm (**gitignored**)

**Touched: nothing else.** Verified by `find -newermt`: the only file outside `outputs/` with my
mtime is the review page. `knowledge/_rulings.json` (15:50), `knowledge/_state.json` (15:58),
`_CHAIN.md` (15:53), the briefs and `reviews/DEMO-TRIAGE-2026-08-31-v1.html` (16:12) all predate my
first write and are **not mine**. No `knowledge/snippets/*` or `knowledge/canon/*` byte moved.
No git command was run.

## 8 · Cost line

- **Token spend: UNOBSERVABLE from inside this sub.** No instrument for my own window here and I will
  not estimate one; the conductor's `_checkin.py` at the seam is the only honest figure. This line
  exists so it is not silently omitted.
- **Observable proxies:** 24 sandbox bash calls — 2 environment repair, 9 render passes, the rest
  reading canon/snippets/the registry/the approved review page and building. 38 PNGs produced, **16
  distinct read by eye** (19 reads; three files were read twice, before and after a fix). 1 page +
  1 report + 2 scratch scripts written. No call-boundary loss; every render pass ran well inside one
  call.
