# #297 lane D — the cover strap, Evolution as its own chapter, Components · Knowledge · Judgment, and the graph at the heart of the map

provenance: 297 · 2026-09-22 (session date; work done Wed 2026-09-23 ~09:05–10:05 BST) · lane D (Opus 5.5, remote-device seat)
status: observed
tokens: UNMEASURED — this seat has no `message.usage` read

Dave's four messages (08:41, 08:44, 08:48, 08:50 BST) are filed verbatim, by addition, at `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md`, with the conductor's reading beneath them.

## VERDICT

**DONE.** All four are in the plain deck. The deck was rebuilt from its source with `build_c.py`; it was never hand-edited, and `build_e.py` was not run.
- **Rail collisions (lane B's bounding-box check), 16 slides plus 11's second state:** **0 at 1920×1080, 0 at 1440×900.**
- **Overflow:** none at either size. The only flag is the governance note on 11's second state. It sits under the Speed card by design, and was flagged the same way before this change.
- **Pixel diff at 1920×1080 against HEAD 38be9376's render:** content changed on **01, 02, 12 and 13 only**. The rail changed on every slide it shows on (list in section 5). **08's drawing is SAME.**
- **Keys:** 10 → 11 → 11 second state → 12 and back behave exactly as in lane C's log.
- **For Dave:** `notes/_lanes/297/D/for-dave.html`. It is self-contained (0.9 MB) and shows five screens: 01, 02, the rail on 06 → 07, 12 and 13.

## 1 · What changed, slide by slide

| slide | what changed |
|---|---|
| **01** cover | The strap is now two lines: "A smart design engine powered by AI" / "on brand, on standard, accessible, at speed". Same style (`#s1 .sub`), with a line break between the lines. The stray comma after the first "on" is dropped, and the second line is lowercase as he typed it. **No full stop at the end**, as he typed it; the old strap had one. Because the strap is one line taller, the type block re-centres about 19px higher. |
| **02** order of play | Five chapters, in the same style: 1 Problem · 2 Research · 3 Evaluation · **4 Evolution** · 5 The result. **Evaluation's descriptor is new copy: "what else is slowing design"**, from 06's own headline. Evolution takes the old "the library · the graph · the gates". The ask is not on 02, as before. |
| **06 → 13** rail | A new chapter. **Evolution (4) runs 07–13; Evaluation (3) is now 06 alone.** The rail has six chapters and the same 14 items. "EVOLUTION" is shorter than "EVALUATION", so the 200px column still holds it. |
| **12** three elements | Titles: **Components · Knowledge · Judgment** (his spelling). Judgment's line is new (section 2). Components' line is unchanged. The note under the plates now reads "**Components**, knowledge and the judgement to compose from them." (it said "Parts, …"; see section 3). The plates are unchanged. |
| **13** the map | **08's knowledge-graph drawing is now the hub**, without its tray. "Apollo", the red rule and "Smart design system" are kept, set beneath the drawing. The tiles, ticks and frame are unchanged. |

**Chapter labels on 07–13:** none of the eyebrows name Evaluation ("The component library", "The knowledge graph", "Gates and evals", "The designer's brain", "Speed, consistency, and quality", "The main constituents", "A smart design system"). Nothing to change there.

## 2 · The lines for 12, verbatim

- **In the deck (Judgment):** "The brain: what to build, and how to compose it."
  - It follows "The library: …" in the Components line, since each line names the thing on its plate.
  - It sits on one line at 1920 and at 1440. A non-breaking space keeps "it." from wrapping on its own.
- **Alternative 1:** "Knowing what to build, and how."
- **Alternative 2:** "Deciding what to build, and composing it well."
- **Components, not changed; one alternative that does not repeat the noun:** "The library: 137 building blocks in code."

## 3 · "Parts" and "Proficiency" elsewhere

Every rendered occurrence, before this change:

| where | text | the element label? | done |
|---|---|---|---|
| 12 title | "Parts" | yes | → **Components** (ruled) |
| 12 title | "Proficiency" | yes | → **Judgment** (ruled) |
| 12 note under the plates | "Parts, knowledge and the judgement to compose from them." | yes: it lists the three labels | **"Parts" → "Components"**, because it would now contradict the title above it |
| 10 lead | "The parts and the knowledge are not enough on their own — the brain is the judgement to compose from them, …" | no: a plain noun, in copy he accepted ("this copy is fine") | unchanged |
| 06, cause 03 | "Too few parts, so designers draw the rest from scratch." | no | unchanged |
| 05 headline | "… the agents invented parts — and got them wrong." | no | unchanged |
| 13 tile 03 | "Page templates — the shape before the parts." | no | unchanged |
| 13, the map's screen-reader label | "Twelve parts of a design system around one core" | no | unchanged |

- **"Proficiency" appears nowhere else.** Neither word appears on 02 or on the rail.
- Some source *comments* (not rendered) still say "01 Parts". They are left as history.
- **⚠ Spelling, for him to decide:** the title is "Judgment" (his spelling there), but the deck's copy says "judgement" three times: 10's headline, 10's lead and 12's note. His own message uses both spellings. I changed none of the three.

## 4 · How 13's hub was done

- **The same drawing.** The shells script that draws 08 now also draws 13's hub. It uses the same shells, nodes, edges, rings, rest angle (−35 / 20), ink and 1px weights.
  - It is drawn once at rest into `<img id="hubShl">` (object-fit: contain), and again whenever the hub changes size.
  - So it never stretches, it prints as it shows, and it is deterministic for the harness.
  - After each draw, 08's canvas, view, scale, stroke and print are put back exactly as they were. The pixel diff shows **08 SAME**.
- **What is left out, on 13 only:** the tray, meaning the plate and the ground cross drawn on it.
  - **The vertical axis stays.** It now runs as far below the centre as above it (34 units past the outer shell each way). On 08 it runs down through the tray.
- **One stroke difference (not a drawing difference).** 08 strokes each ring as 120 short pieces, and the 5/4 dash restarts on every piece. At the hub's smaller scale a piece is shorter than a dash, so the hidden rings came out solid grey. I looked at this and fixed it: on 13 the pieces are joined, so the hidden runs stay dashed 5/4.
- **Size and type.** At 1920×1080 the sphere is about 225px across, and "Apollo" and the strap keep their #296 sizes (58 / 17).
  - At 1440×900 the hub is only 329px tall. With the type at full size the sphere was about 125px across and cramped (I looked).
  - So the hub's words now scale with the hub's height (container units). At 1440 "Apollo" is about 43 and the strap 14, and the sphere is about 163px across.
  - "Apollo"'s line-height in the hub goes from 1.25 to 1.1, and the rule's margins from 18 to about 13, at both sizes.
- **Markup:** one `<div class="hubkg"><img id="hubShl" alt="Line drawing of the knowledge graph"></div>` before "Apollo". **Styling:** one `<style data-lane="297-D">` before `</body>`. **Script:** inside the shells IIFE, before `window.shlReady`. It exposes `shlHubState()`.

## 5 · Checks

- **Renders:** all 16 slides plus 11's second state, at 1920×1080 and 1440×900, with lane C's harness (freezes as lane A's). They are in `notes/_lanes/297/D/_work/after-1920/` and `after-1440/`; the baseline is `before-1920/`, rendered from the committed deck at HEAD 38be9376.
- **Rail, 0 hits at both sizes.** Smallest clearance:
  - at 1920: 123.5px on 07–10 (was 117), 237px elsewhere;
  - at 1440: 37px (06, 14), 43.5px on 07–13 (was 37), 47.9 on 04–05, 57.5 on 03, 65.5 on 15–16.
- **Overflow: 0 at both sizes**, except 11's second-state note (by design; flagged the same way before this change). 0 page errors and 0 console errors.
- **Pixel diff at 1920 vs HEAD**, split into the rail band (x < 200) and the content:

| slide | rail band | content |
|---|---|---|
| 01, 02 | (hidden) | **DIFF**: 01 the strap and the re-centred block (400,403)–(1255,674); 02 columns 2–5 (623,570)–(1513,665) |
| 03 04 05 · 14 15 16 | DIFF, the marker column only (x 32–44) | SAME |
| 06 | DIFF, the marker column only (x 32–44) | SAME |
| 07 08 09 10 11 11b | DIFF (x 32–161): "4 EVOLUTION" for "3 EVALUATION" | SAME |
| 12 | DIFF (x 32–161) | **DIFF** (400,678)–(1502,866): titles, the Judgment line, the note. The plates are SAME |
| 13 | DIFF (x 32–161) | **DIFF** (848,404)–(1072,790): the hub only |

  - **Outside the expected list:** the rail's marker column on 03–05 and 14–16. The rail lists every chapter on every slide, so the dot that was 07 is now a circle there too. It is the rail only; no content moved.
- **I looked at** 01, 02, 06, 07, 12 and 13 at 1920, and at 02, 12 and 13 at 1440, plus the hub at 2× at both sizes. On 02 all five descriptors sit on one line at both sizes. The widest ("the library · the graph · the gates") keeps the 32px column gap.
- **Keys** (`notes/_lanes/297/D/_work/navtest_d.py`, lane C's test, 1920×1080):
```
start deckGo(10) -> slide 10 (10 / 16)
ArrowDown -> 11 (11 / 16) state 1
ArrowDown -> 11 (11 / 16) state 2   [marks 1, note 1]
ArrowDown -> 12 (12 / 16)
ArrowUp   -> 11 state 2 · ArrowUp -> 11 state 1 · ArrowUp -> 10
```
  - Space / Space / PageDown / PageUp ×3 give the same result.
  - Controls: 03 ↓↓ gives 04 then 05, and 13 ↑ gives 12, unchanged.
  - The wheel does not scroll in this headless shell, the same as before (lane C's note).

## Deviations

1. **13's type scales at 1440, and is set a little tighter at both sizes** (section 4). It is not a ruled change. It is the price of keeping the drawing at the centre of a 329px-tall hub.
2. **13's axis is symmetric**, and **13's hidden rings are stroked continuously** (section 4).
3. **12's note under the plates** changed "Parts" → "Components" (section 3). This is within the brief's rule, but it is a change he did not name.
4. **02 uses near-equal columns** (`minmax(max-content,1fr)`: about 192–218px) rather than exactly equal ones. With exactly equal columns, two descriptors wrap by 1–19px. Evaluation's descriptor "what else is slowing design" is new copy.
5. **The cover strap has no full stop**, as he typed it.
6. **W-297c (lane C's row) is left open.** His 08:41–08:50 messages ask for changes to the deck, and closing it is the conductor's call.

## Files

- **Changed:**
  - `notes/_lanes/296/C/v14-plain-before-c.html` (the source)
  - `notes/_lanes/296/C/build_c.py` (the rail's chapters)
  - `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt, 522,693 bytes)
  - `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (appended)
- **New:** `notes/_lanes/297/D/for-dave.html` · this report · store row W-297d
- **Working, not committed:** `notes/_lanes/297/D/_work/`
  - `apply_d.py`: re-runnable from `source.pre-297D.html` and `build_c.pre-297D.py`
  - `shoot_d.py`, `one.py`, `navtest_d.py`, `make_for_dave_d.py`
  - the before and after renders
