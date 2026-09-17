#!/usr/bin/env python3
"""#280 wrap, ritual step 1 sibling — feed the sign-off register (dream-pass v2 P4).

TWO new rows APPENDED (the two review artefacts this session leaves awaiting Dave) and ONE
existing row amended BY ADDITION with its receipt — the #279 15-base row, whose "NOT INSCRIBED"
clause was made false by this session's own lanes. The amendment is a STRIKE with the ruling and
the commits named (`s183-D1` strike / `s188-D2` receipt), never a re-type and never a deletion.

Span reconstruction asserted in THIS process before anything is written.
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
P = os.path.join(ROOT, "knowledge", "_REVIEW-SIGNOFF.md")
orig = open(P, encoding="utf-8").read()
text = orig

# ---- (1) the #279 15-base row, amended BY ADDITION -------------------------------------------
OLD = ("⬛ **ANSWERED, NOT INSCRIBED — the inscribe lane is #280's.** 15/15 choose a twin")
NEW = ("~~⬛ **ANSWERED, NOT INSCRIBED — the inscribe lane is #280's.**~~ ✅ **INSCRIBED AT #280 — "
       "FOURTEEN OF FIFTEEN, AND THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` "
       "receipt):** lane IN read his export WHOLE and landed **nine** twins while asking **six** rows "
       "back on a page rather than guessing (`c4d0d22`, `notes/_lanes/280/inscribe-active/"
       "ASK-2026-09-16.html`), and lane IN2 read his ASK export and landed **five** more (`850acbf`); "
       "the exporter-defect list is born at `knowledge/_ICON-GAPS.md` and `gen_kg_icons.py` now "
       "REBUILDS the fourteen from his own exports and REFUSES on disagreement (22/22, mutants "
       "32/32). ⛔ **ONE ROW IS STILL HIS AND IS OPEN BY HIS OWN WORD — `jade-lifestyle` "
       "(`choice: \"open\"`, `twin: null`, *\"think is the most likely the correct icon\"*): nothing "
       "was written into the library for it and his lean sits ON THE NULL.** The original reading "
       "stands below, unaltered. 15/15 choose a twin")
assert text.count(OLD) == 1, ("amend anchor", text.count(OLD))
i = text.find(OLD)
text = text[:i] + NEW + text[i + len(OLD):]
span1 = len(NEW) - len(OLD)

# ---- (2) the two new rows --------------------------------------------------------------------
ROWS = (
 "| **THE SIX-CELL LAYOUT MATRIX — HIS EYE-CHECK, ASKED AND UNANSWERED** — contact sheet "
 "`notes/_lanes/280/layout-matrix/MATRIX-2026-09-16.html` (all six cells of `s280-D1` on one page: "
 "force · strata · shells × 2D · 3D); the option page that preceded it "
 "`notes/_lanes/280/layout/OPTION-strata-2026-09-16.html`; the four sketches his export answered "
 "`notes/_lanes/280/layout-sketches/SKETCHES-2026-09-16.html`; reports "
 "`notes/_subreports/2026-09-16-280-LM-layout-matrix.md`, `…-280-LS-layout-sketches.md`, "
 "`…-280-LY-layout.md` | 2026-09-16 #280 · **RULED `s280-D1`** (`53a91bd`) · built `b5df9c9` · "
 "`eddf87a` · `c3805ec` · `94204dc` | ⬛ **AWAITING DAVE'S EYE — THE MATRIX IS RULED, WHICH CELLS "
 "SURVIVE IS NOT.** His export chose all four sketches plus the original, in 2D and 3D, force the "
 "default, and `s280-D1` is exactly that. ⚠ **The conductor expects Floors (strata-3D) or Orbits "
 "(shells-2D) to go — an EXPECTATION, not a finding, and no lane may thin the matrix on it.** "
 "Storage untouched; the default cell is pixel-identical to 1.16 by canvas md5. Declared out by "
 "the lane: the shells-3D cutaway, and equal plate/ring sizes per layer. Row `W-280lm`. |\n"

 "| **THE ORPHAN CENSUS — TEN RADIOS, AND THE EXPORT HAS NOT ARRIVED** — "
 "`notes/_lanes/280/orphan-census/ORPHANS-2026-09-17.html` (ten sets, each with its cause and its "
 "price, one radio each); report `notes/_subreports/2026-09-17-280-OC-orphan-census.md` | "
 "2026-09-17 #280 · `82359a5` · answers his *\"do we have a plan to wire up the orphans etc?\"* | "
 "⬛ **AWAITING HIS EXPORT — THIS IS #281'S FIRST MOVE, AND THE CENSUS BECOMES THE ORPHAN PLAN ON "
 "EXPORT.** **157 of 4,618 nodes have no line any chip can draw**, four causes, ten sets. His word "
 "on the census itself was *\"cool\"*. ⚠ **The largest set is a switch left off, not a gap in the "
 "vocabulary** — 100 of 145 UX principles are dark, 99 with no edge of any kind in storage, and the "
 "principle generator can already emit the two kinds that would light them (behind `s275-D2` flags). "
 "⛔ **Turning the first on puts a FAMILY NODE on the stage — a new kind of thing, and therefore HIS "
 "word.** The second-largest set is not orphaned at all: 94 base `rule:` dots that light when the "
 "HSBC `rule:` chip goes on. Row `W-280oc`. |\n"
)
assert text.endswith("\n"), repr(text[-20:])
text2 = text + ROWS
span2 = len(ROWS)

# ---- reconstruction proof, before any write ---------------------------------------------------
back = text2[:-span2]
back = back[:i] + OLD + back[i + len(NEW):]
assert back == orig, "REFUSED — reconstruction failed"

if "--write" not in sys.argv:
    print(f"DRY: amend span +{span1} B · 2 new rows +{span2} B; reconstruction PASSED")
    sys.exit(0)
open(P, "w", encoding="utf-8").write(text2)
print(f"WROTE: #279 15-base row amended by addition (+{span1} B) · 2 rows appended (+{span2} B); "
      f"reconstruction PASSED before the write")
