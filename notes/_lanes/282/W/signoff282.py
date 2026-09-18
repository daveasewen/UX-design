#!/usr/bin/env python3
"""#282 wrap, step 1 sibling — feed `knowledge/_REVIEW-SIGNOFF.md` (dream-pass v2 P4).

TWO rows are STRUCK BY ADDITION with their `s183-D1`/`s188-D2` receipts (each carried a claim
this session's own rulings made false) and TWO rows are ADDED for this session's review pages.
⛔ Nothing is deleted and no row is re-typed.
"""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
REG = os.path.join(ROOT, "knowledge", "_REVIEW-SIGNOFF.md")

# ---- the two surgical strikes (title cell only; the row's body is untouched) ---------------
STRIKES = [
 ("| **THE SIX-CELL LAYOUT MATRIX — HIS EYE-CHECK, ASKED AND UNANSWERED** —",
  "| ~~**THE SIX-CELL LAYOUT MATRIX — HIS EYE-CHECK, ASKED AND UNANSWERED**~~ ⛔ **STRUCK AT THE #282 WRAP "
  "(`s183-D1` strike, `s188-D2` receipt): THE EYE-CHECK WAS NEVER OPEN — HE HAD ALREADY SETTLED IT.** His own "
  "words at #282: *\"sorry I though this was settled\"* — and it was, by **`s280-D1`**. The carry was the "
  "CONDUCTOR'S expectation that a cell would be dropped, never Dave's ask. Correction inscribed at: `6bac5e4` · "
  "`_HANDOFF-133-the-rule-notes-land-and-the-logo-is-ruled.md` · row `W-280lm` DONE. The original row follows "
  "unedited —"),
 ("| **HIS 15 NOTES ABOUT THE RULES — FILED, NOT INSCRIBED, AND #282'S FIRST MOVE** —",
  "| ~~**HIS 15 NOTES ABOUT THE RULES — FILED, NOT INSCRIBED, AND #282'S FIRST MOVE**~~ ⛔ **STRUCK AT THE #282 "
  "WRAP (`s183-D1` strike, `s188-D2` receipt): THEY WERE PUT TO HIM AND ELEVEN ARE NOW INSCRIBED.** The notes "
  "became a 15-row decision page (`notes/_lanes/282/rule-notes/RULE-NOTES-2026-09-17.html`) and his export at "
  "19:10Z took **14 of 15 on the recommendation** (`notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json`); "
  "**`s282-D1` (`56c5690`, lane RN) then made 11 guideline edits in his own words across 8 files** plus 2 second "
  "`restsOn` edges. ⛔ **ONE IS NOT TAKEN AND STAYS HIS: `col26-012` → *\"Discuss first\"*.** Correction "
  "inscribed at: `knowledge/_rulings.json` § `s282-D1` · `notes/_subreports/2026-09-17-282-RN-rule-notes-land.md` "
  "· `_HANDOFF-133-the-rule-notes-land-and-the-logo-is-ruled.md`. The original row follows unedited —"),
]

# ---- the two new rows ----------------------------------------------------------------------
ROWS = [
 "| **THE 15 RULE NOTES AS A DECISION PAGE — 14 OF 15 ON THE RECOMMENDATION, AND ELEVEN ARE INSCRIBED** — "
 "`notes/_lanes/282/rule-notes/RULE-NOTES-2026-09-17.html` (one row per note: his note VERBATIM, the rule's "
 "stored text, a recommendation, and what changes if it is taken); his export "
 "`notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json` (19:10Z); report "
 "`notes/_subreports/2026-09-17-282-RN-rule-notes-land.md` | 2026-09-18 #282 · **RULED `s282-D1`** (`56c5690`) "
 "+ **`s282-D2`** (`bb016c6`) | ✅ **CLOSED ON FOURTEEN — 11 guideline edits in his own words across 8 files, "
 "2 second `restsOn` edges (73 → 75), and the `col26-012` ASK closed by `s282-D2` on a cross-reference already "
 "present.** ⛔ **ONE IS OPEN AND IT IS HIS: `col26-012` → *\"Discuss first\"*.** A note on `col26-016` came "
 "back green. Backlog born here: **`W-282a`** (universal icon list) · **`W-282b`** (SC 2.2.2 on `mot-005`). |",

 "| **THE LOGO REVIEW — 12 LOCKUPS PUT TO HIM, 9 ANSWERED, 3 MOOT, AND THE IDENTIFIER LOCKUP SCRAPPED** — "
 "`notes/_lanes/282/logo-review/LOGO-REVIEW-2026-09-17.html` (12 lockups measured, 3 exporter defects named, "
 "6 questions put; verification renders `verify-1280.png`, `verify-390.png`); his export "
 "`notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json` (08:20Z, four notes); reports "
 "`notes/_subreports/2026-09-17-282-LR-logo-review.md`, `notes/_subreports/2026-09-18-282-LL-logo-land.md` | "
 "2026-09-18 #282 · **RULED `s282-D3`** (`0acb019`, corrected `c143a1b`) · **`s282-D4`** (`da9f824`) · "
 "**`s282-D5`** (`eaf1236`) · **`s282-D6`** (`03fe8ff`, corrected `6df8b64`) | ✅ **CLOSED — ONE logo guideline "
 "(`logos.md`), size by RAW HEIGHT in five steps 24/28/32/36/40, masthead full colour on both grounds in all "
 "four themes (`logo26-008` BLOCKING), vertical AND horizontal clear space at 0.25 × height / 0.25 × logomark "
 "width snapped up to 4px (`logo26-009` BLOCKING), hexagon alone on nav-rail head / app tile / favicon "
 "(`logo26-010` ADVISORY); 8 logo nodes bound, 27 → 33 edges.** ⛔ **WHAT IS OPEN IS THE NEXT LANE, NOT THIS "
 "PAGE: the 40 per-size masters (8 lockups × 5 steps, raw pixel height and width, no viewBox) — #283's first "
 "move, and his *\"is it possible to 'hint' svgs so they are as sharp as possible?\"* answered in kind.** |",
]

ANCHOR = "| ~~**HIS 15 NOTES ABOUT THE RULES"

text = open(REG, encoding="utf-8").read()
for old, new in STRIKES:
    assert text.count(old) == 1, ("strike anchor not unique", old[:60], text.count(old))
    text = text.replace(old, new, 1)

i = text.index(ANCHOR)
j = text.index("\n", i) + 1          # append the new rows AFTER the (now struck) 15-notes row
text = text[:j] + "\n".join(ROWS) + "\n" + text[j:]

if "--write" not in sys.argv:
    print("DRY: 2 strikes + 2 new rows would be applied"); sys.exit(0)
open(REG, "w", encoding="utf-8").write(text)
print("WROTE", REG, "— 2 rows STRUCK by addition with receipts, 2 rows added")
