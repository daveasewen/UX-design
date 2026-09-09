#!/usr/bin/env python3
"""#261 N4 — apply the identical label-crop + selected-state edits to the three nav snippets."""
import pathlib, sys

FILES = ["Sidebar-nav", "Navigations", "Tab-bar"]
ROOT = pathlib.Path("/sessions/zen-funny-hawking/mnt/UX-design/knowledge/snippets")

TRIM_OLD = """/* leading-trim (label alignment) — native text-box-trim, metric-aware, progressive
   enhancement; headings/body excluded. */
:is(button,a,label,span,"""
TRIM_NEW = """/* leading-trim (label alignment) — native text-box-trim, metric-aware, progressive
   enhancement; headings/body excluded.
   ⚠ #261 N4 — the list is wrapped in :where(), exactly as canon.css wraps it, and for the same
   reason (canon.css "#215 — `:where(.canon)`, NOT `.canon`"): this is a DEFAULT, not an authoring
   decision. Bare, the :is() list took its specificity from its heaviest branch (input[type=text])
   and sat at (0,1,1) — ABOVE every one-class ds-005 override in this file, so `.nv-label
   {text-box-edge:text text}` was cascade-dead and every label computed `cap alphabetic`: the box
   ended at the baseline and overflow:hidden cut the descender off "Payments and transfers".
   :where() contributes zero specificity and matches identically. ⛔ Do not unwrap it. */
:where(button,a,label,span,"""

LABEL_OLD = """  .nv-label{flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
    text-align:left; text-box-edge:text text;}"""
LABEL_NEW = """  /* THE LABEL IS A TRUNCATING LABEL, so it takes the canon truncating-label treatment
     (canon.css, `.row .title`): keep the trim's tightness but trim to the FULL text box
     (`text text`, over-edge to under-edge) — `cap alphabetic` ends the box ON the baseline, and
     the overflow:hidden that ellipsis needs then crops every descender (g, y, p). The trim is
     restated here, not inherited, so the pair is read as one decision. Driven at #261 N4:
     16px label, box 11px → 16.5px, descender clipped 5.5px → 0px, all 3 surfaces × 4 themes
     × 2 modes. ⛔ never pair `cap alphabetic` with `overflow:hidden` on a label. */
  .nv-label{flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
    text-align:left; text-box-trim:trim-both; text-box-edge:text text;}"""

CUR_OLD = """  .nv-item[aria-current="page"]{background:var(--nav-hover);}"""
CUR_NEW = """  /* #261 N4, Dave verbatim: "remove the background grey on the selected state". The current row
     no longer takes a fill on ANY of the three surfaces — the fill was the hover state's own
     signal, and a row wearing it permanently left hover with nothing of its own to say. The
     indicator bar (a SHAPE) and the label's weight step carry current; the fill now means hover
     and only hover. */
  .nv-item[aria-current="page"]{background:transparent;}
  .nv-item[aria-current="page"] .nv-label{font-weight:500;}"""

CARRIER_OLD = """       3. a surface change to tertiary/background/hover"""
CARRIER_NEW = """       3. a WEIGHT step on the label (400 -> 500) — a shape, not a hue, and not a fill
          (#261 N4: the current row's grey fill is REMOVED; grey is hover's word now)"""

EDITS = [(TRIM_OLD, TRIM_NEW), (LABEL_OLD, LABEL_NEW), (CUR_OLD, CUR_NEW),
         (CARRIER_OLD, CARRIER_NEW)]

rc = 0
for name in FILES:
    p = ROOT / f"{name}.reference.html"
    t = p.read_text()
    for old, new in EDITS:
        if t.count(old) != 1:
            print(f"FAIL {name}: {t.count(old)}x for {old[:48]!r}")
            rc = 1
            break
        t = t.replace(old, new)
    else:
        p.write_text(t)
        print(f"ok {name}")
sys.exit(rc)
