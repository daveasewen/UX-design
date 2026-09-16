# LANE RIF — FIX REPORT — the three fixes lane RIV ruled, applied

#277 · 2026-09-16 · corrector of `notes/_lanes/277/icons-propose/` · WRITES ONLY IN THIS FOLDER.

Lane RIV's verdict on RI's 5520d43 was **PRESENT WITH THESE 3 FIXES** — R1, A1, A2. All three are
applied. RI's commit stands untouched: `_build_page.py`, `_drive_page.py`, `_page-copy.json`,
`REVIEW-icons-2026-09-16-v1.html` and the eight `ri-*.png` are byte-unchanged, and the correction
ships as a **v2 page** beside them. A3 and A4 are pre-land conditions on the generator and the
schema diff, not on the page, and are NOT touched here.

Nothing under `knowledge/` was written. `notes/_KG-EXPLORER.html` was not rebuilt (mtime holds at
08:50). `_build_kg_explorer.main()` was never called against the live tree. No `git stash`.

---

## R1 — RI-3: the exporter artefact, the missing option, and the sheet

### R1.1 · the lead-figure sentence

**Before**

> **15** bases with more than one "active" glyph — and all 15 of them have a bare `-active`

**After**

> **15** bases with two or three "active" drawings that share ONE Figma name — the `-2`/`-3`
> suffix is `_export-icons.py`'s collision counter, so the bare slug is Figma's enumeration
> order, not a design choice

Source: `knowledge/assets/icons/_export-icons.py:113-118`, re-read live —

```
s, i = base, 2
while s in seen[gslug]:
    s = f"{base}-{i}"; i += 1
```

Re-derived here: all 31 active records across the 15 bases carry a *name* that is identical within
each base (`Dentist Active` ×3, `Alert Active` ×2, …), so the bare slug is guaranteed by
construction and carries no design information.

### R1.2 · the recommendation's evidence

**Before**

> Take (a) … The evidence for it is one file … And it works here: **all 15 of the multi-variant
> bases have a bare `-active`**, so (a) resolves every one of them …

**After** — the tautology is gone; the card now says what (a) actually is, and what it is not:

> (a) is still the safe no-op: it ratifies what `_validate_icons.py` already enforces
> (`active_names()` returns `slug + "-active"`) and **none of these 31 glyphs is used by any
> snippet today**, so nothing breaks either way — but on this evidence it would write down a
> default we can already see is wrong on half the set.

### R1.3 · option (c) restored

IX §5 posed three options; RI shipped two. `(c) I'll pick — the 31 active drawings are on the sheet
at the foot of this card, each beside its base — I look, and I name the 15 defaults myself` is back
on the card, with `RI-3-c` as a real radio and the attribution naming what happened.

### R1.4 · the sheet — and what it changed

The card now carries **46 inline `<svg>`**: the 31 active glyphs of the 15 bases, each beside its
bare inactive sibling. They are the live files under `knowledge/assets/icons/`, read at build time,
with each file's internal ids namespaced so 46 clip-paths can share one document. Nothing is
retouched and no glyph is drawn by hand.

**Then lane RIF looked at it — and the sheet overturns the recommendation.** RIV's correction was
"nobody has looked"; somebody has now, and on at least six of the fifteen the bare `-active` is
plainly not the base's active twin:

| base | `-active` (what (a) would pick) | `-active-2` |
| --- | --- | --- |
| `dentist` | a price tag | the filled tooth |
| `renew` | a stack of lines | the filled circular arrows |
| `user-staff` | a droplet with a bolt | the filled staff figure |
| `employee-banking-solution` | a video camera | the filled person-in-frame |
| `reward` | a shopping bag | the filled gift box |
| `withdraw-overpayment` | a padlock | the filled card |

`contact-chat-ai` and `financial-health-check` read wrong too, at sheet size.

So **Recommended moved from (a) to (c)** on the RI-3 card, attributed to lane RIF and labelled for
what it is: *an eye on a sheet, not a measurement*. RIV explicitly left this open — "keep (a)
Recommended if RI still wants to; the honest recommendation is '(a) now, (c) when you have ten
minutes with the sheet'" — and the sheet makes (c) the honest one, because (a) would now write down
a default we can see is wrong. Every one of the eight is checkable by Dave in five seconds against
the sheet directly below the sentence. **The conductor can overturn this back to (a) by flipping one
flag in `_page-copy-v2.json`; it is the one judgement in this lane that goes past the literal
correction.**

---

## A1 — RI-1 pointed at screenshots that were not on the page

**Embedded, not reworded.** Two explorer renders are now at the foot of the RI-1 card, one per
theme pair, with the icons-and-logos family placed.

**Before**

> That last number is a look, not an argument — judge it on the screenshots below, and if it is too
> much, (d) costs nothing.

**After**

> That last number is a look, not an argument — judge it on the two explorer renders at the foot of
> this card, which are the graph today and the graph with this family's chip on. If it is too much,
> (d) costs nothing.

**How they were made.** `_build_kg_explorer.py` and `_kg_explorer.template.html` were copied to a
scratch directory. The copy refuses by name to write anywhere inside the repo, its `ROOT` is
read-only, and it was fed this lane's own `_icon_nodes.json` / `_logo_nodes.json` behind a fifth
family chip (`Icons & logos`). `main()` was never called against the live tree; the live explorer's
mtime is unchanged.

Measured off the scratch explorer's own stats strip, not typed — and carried into the page from
`explorer-renders.json`, so the figure on the card is read, not asserted:

```
chip OFF   1050 nodes · 1,642 relations · 16 edge types
chip ON    1738 nodes · 2,933 relations · 22 edge types
```

1738 − 1050 = 688, the proposal's node count exactly. 2,933 − 1,642 = 1,291, which is the 1,299 new
edges less the 8 `ruledBy` whose target is a `ruling:` node in the governance family (chip off).

**Declared limit, on the card in the page's own words:** the new family is parked in its own column,
and *which* column is lane RIF's layout choice, not a measurement. The squeeze on the left of the
chip-on render is the cost of that choice as much as of the family. The strip at the top of each
render is the part that is measured. The scratch `fit()` was also changed to frame the shown nodes'
real bounding box, because the shipped one is a fixed divisor that puts a far column off-screen.

---

## A2 — the driver's residue shipped inside RI's PNGs

**Before.** `ri-decisions-light/dark.png` showed `(a)` ticked on RI-1 and `ri-RI3-light/dark.png`
showed `a note that must survive a reload` in RI-3's notes box. RI's driver *did* call
`localStorage.clear()` at `_drive_page.py:305` — and it did not help, because the page writes the
DOM back to storage on its way out, so the reload that follows the clear restores the very residue
the clear removed. That is why RIV found it.

**After.** Two changes, and the second is the one that works:

1. `localStorage.clear()` + reload on first load, before a single assertion runs.
2. **The whole screenshot pass runs in a fresh browser context that has never been driven.** The
   page that took the clicks and the reload test is closed first.

And it is now asserted rather than hoped for, twice:

```
ok  first load with empty storage: no radio checked, no note written
    16 radios, 0 checked · 0 note(s) with text · said '0 of 4 decided'
ok  the screenshot context is virgin: 0 ticked, 0 notes, before a single PNG
    0 ticked · 0 note(s) · said '0 of 4 decided · saved —'
```

Both confirmed by eye in `ri2-RI3-light.png` and `ri2-RI3-dark.png`: every radio is empty and the
notes box is empty.

---

## The driver

`_drive_page_v2.py` — a copy of RI's `_drive_page.py`, re-aimed at the v2 page. RI's driver is not
edited, because editing it in place would break it against the v1 page it still drives. Every check
RI wrote is kept. Three are added:

* **15. THE SHEET** — the RI-3 card carries at least one inline `<svg>` per glyph on the sheet, the
  sheet sits *inside* the card, every `<svg>` paints at ≥ 24px, there is one row per multi-variant
  base, and option (c) exists. The expected count is read from the page's own `#measured` block
  (`n_sheet_glyphs`), never typed.
* **15b. THE RENDERS** — RI-1 carries two explorer renders that are *visible in this theme* and
  actually decoded (`naturalWidth`/`naturalHeight`), each with a real `alt`, and the string
  "screenshots below" appears nowhere on the page.
* **16. NOTHING PRE-TICKED** — on a first load with empty storage, no radio anywhere is checked and
  no notes box carries text.

```
DRIVE PASS — 28 checks, 0 fail, both themes, 1280 and 390, fresh context
```

---

## What shipped

```
REVIEW-icons-2026-09-16-v2.html     the page  (46 inline <svg> on RI-3, 4 renders on RI-1)
_build_page_v2.py                   the builder — copy of RI's, three fixes, no integer typed
_page-copy-v2.json                  the copy — RI's, with R1.2/R1.3 and the A1 sentence
_drive_page_v2.py                   the driver — copy of RI's, +3 checks, fresh-context shots
explorer-renders.json               the scratch explorer's stats strip, read not typed
ri-explorer-chip-{on,off}-{light,dark}.png   the four A1 renders
ri2-{light,dark}-1280.png           full page, both themes, 1280
ri2-390-{light,dark}.png            full page, both themes, 390
ri2-decisions-{light,dark}.png      the decisions block
ri2-RI3-{light,dark}.png            the RI-3 card
ri2-RI3-sheet-{light,dark}.png      the sheet, full height
ri2-RI1-renders-{light,dark}.png    the two explorer renders in place
FIX-REPORT.md                       this file
```

INSERT-ONLY. Nothing of RI's was edited or deleted.

## Known, not fixed

* The page carries four duplicate element ids (`RI-1`…`RI-4`: the radio group name and the notes
  box). **Present identically in RI's v1** — it is not a regression and it is not one of the three
  fixes, so it is named here rather than changed.
* A3 (the `defaultFor` substring-over-English residue) and A4 (live integers in
  `meta.schema.diff`) are RIV's pre-land conditions on the generator and the schema text, not on the
  page. Untouched.
