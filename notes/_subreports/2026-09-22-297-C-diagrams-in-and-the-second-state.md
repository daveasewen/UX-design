# #297 lane C — the five diagrams go in, slide 11 gets its second state, three causes renamed

provenance: 297 · 2026-09-22 (session date; work done Wed 2026-09-23 ~08:40–10:00 BST) · lane C (Opus 5.5, remote-device seat)
status: observed
tokens: UNMEASURED — this seat has no `message.usage` read

Dave's words are filed by addition at `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (step 0), with the conductor's reading beneath them:
*"these are all good, lets remove the red from three problems slide, on the box, on speed, and remove addressed first."* · *"insert a new state triggered like the next slide advancement where everything we have tackled is highlighted"* · *"Governance need an indicator that it it isn't solved but we have a proposal"* · the three renames.

## VERDICT

**DONE.** Lane B's five diagram proposals are in the plain deck as Dave saw them. Slide 11 has lost its red and its "Addressed first" line, and it has a second state on the next press. The three causes carry his new names on 06 and on 11, and "Lack of user data and research" is renamed on 11. The deck was rebuilt from its source with `build_c.py`; it was never hand-edited, and `build_e.py` was not run.
- **Pixel diff at 1920×1080, all 16 slides against the pre-change render:** only **04, 06, 11, 12, 13** changed. 01–03, 05, 07–10 and 14–16 are SAME.
- **Rail collisions (lane B's bounding-box check), 16 slides plus 11's second state:** **0 at 1920×1080, 0 at 1440×900.** Smallest clearance is 37px at 1440 and 117px at 1920, the same as after lane B.
- **Text overflow:** none at either size. The only flag is the governance note on 11's second state, which sits under the Speed card by design (see below).
- **Keys:** 10 → 11 → 11 second state → 12, then back 12 → 11 second state → 11 → 10. Exact log below.
- **For Dave:** `notes/_lanes/297/C/for-dave.html`, self-contained (700 KB). It shows 04, 06, 11, 11's second state, 12 and 13 as they now are, one per screen, with a caption on each.

## 1 · What changed, slide by slide

| slide | what changed |
|---|---|
| **04** the loop | Lane B's redraw, exactly as shown. The steps are white boxes in the 1px ink line, numbered 01–06 in grey. Red marks only steps 04 and 05 and the dashed way back. The arrows are one ink line with one small head, and the notes stand upright. |
| **06** five causes | Lane B's redraw, exactly as shown, including the 2px red rule over "Small component library". Also three renames and a new standards description (next section). |
| **11** three problems | Lane B's redraw **without its red**. Speed's label and card are ink like the others. "Addressed first" is gone, and so is the old "Addressed first · the library" line. The heading above the middle card reads "Shared by all three". The causes carry the same names as 06, plus "Lack of user data and research". **New: a second state** (section 3). |
| **12** three elements | Lane B's redraw, exactly as shown. The plates show 07's catalogue, 08's graph and 10's brain, cropped to their ink and drawn at one scale, with a gamma so the hairlines stay ink. Numbers are grey, the cell lines #D7D8D6, and the descriptions 16px. The alt text now names the catalogue and the graph. |
| **13** the map | Lane B's redraw, exactly as shown. The twelve file paths go. Titles are bold 16 in sentence case, numbers grey 12, descriptions 13. "In progress" tiles are white with a grey dashed inset. The outer frame is ink, and the red rule under Apollo is the only red. |

**The renames (06 and 11 now name the causes identically):**
- "Governance process" → **"Manual, linear governance process"**
- "Lack of design standards and accessibility knowledge" → **"Lack of standards knowledge"**
- "Low/variable skills" → **"Highly variable design skills"**
- on 11 only: "Lack of data and research" → **"Lack of user data and research"**

**06's standards description, verbatim:**
> Design, accessibility and content standards are not written down, so each decision is made again.

- It is 98 characters and runs to 4 lines at 1920 and 1440; its siblings run to 2–3. The old description was 84 characters.
- I dropped "and accessibility is fixed late", which the brief's example carried, to keep it near its siblings' length.
- I wrote "are not" rather than "aren't" because the deck uses no contractions ("It is a queue", "are not enough").
- The other four descriptions are unchanged.

**The breaks I checked:**
- 06, 18px titles: "Manual, linear / governance process", "Lack of standards / knowledge", "Highly variable / design skills". A non-breaking space keeps "design skills" together; without it, "skills" sat alone on the second line.
- 11: "Manual, linear governance process" fits on one line in the Speed card. The shared column reads "Small / component / library", "Lack of / standards / knowledge", "Highly variable / design skills".

## 2 · How it went in (source, not deck)

- **The text is in the markup of `notes/_lanes/296/C/v14-plain-before-c.html`.** That covers 04's numbers, the renames, 13's sentence case and 12's alt text. Lane B had done these with script, in a copy.
- **The styling is lane B's CSS**, in one `<style data-lane="297-C">` block before `</body>`. It is lane B's rules as written, minus the three red rules on 11 (Speed's label, Speed's card, "Addressed first"), plus the second-state rules.
- **The layout script is in one `<script data-lane="297-C">`.** It draws 04's dashed way back and gives 06's titles one height, as lane B's did.
- **12's plates.** The anatomy IIFE in the source now pulls from ctPrint, shlPrint and brPrint, not gbPrint, bkPrint and brPrint, and runs lane B's crop, one-scale and gamma. It redraws the plates on resize, which lane B's copy did not; that matters when the window goes full screen. `anatomyState()` still answers.
- **`build_c.py` is unchanged.** A fresh build of the edited source is byte-identical to the deck (517,035 bytes). The source and deck diffs are +214 / −48 each.

## 3 · Slide 11's second state

**What it looks like.**
- **Every tackled cause gets a 2px red rule standing upright beside it.** The rule sits in the card's padding, or in the gap between the three shared causes, 12px left of the text. It covers Manual, linear governance process · 2 stage process · Small component library · Lack of standards knowledge · Highly variable design skills · AI generation quality.
- **"Lack of user data and research" gets no mark.** Its text is unchanged.
- **Governance gets the same rule DASHED 5/4.** That is the drawings' "not yet" line, used on 04's way back and 13's in-progress tiles.
- **A note below the Speed card** carries the same dashed rule in the same column: "**Proposal:** sign off the system, / not the outputs — or at least a fast-track." It is 13px, lined up with the card's text, 16px below the card.
- **Why upright rather than 06's rule over the column.** I tried a rule over each cause first and looked at it. A rule between "Lack of user data and research" and "AI generation quality" read as belonging to either one. That is exactly the cause that must read as not highlighted. An upright rule beside the text can only belong to its own cause.
- **Nothing reflows.** The marks sit in existing padding, and the note sits below the cards in empty space. So state 1 and state 2 have one layout: the headline and cards do not move, and only opacity changes (a 0.35s fade, none under reduced motion).
- **The note is `visibility:hidden` in state 1**, so a screen reader does not read it early.

**How it works.** This is a minimal build mechanism; the deck had none.
- **The trigger.** `data-steps="2"` on `#s6b` is the only slide that carries it, so no other slide changes behaviour. CSS keys off `data-step="1|2"`.
- **Keys.** The chassis's keydown asks `window.deckStep` first. The keys are the deck's own: ↓ / Space / PageDown forward and ↑ / PageUp back. The deck has no → key and no click navigation.
- **Wheel and trackpad.** A gesture that *starts* while the deck is settled on 11 steps the build, and the rest of that gesture is absorbed. Anything else scrolls as before.
- **Arriving.** Coming from 10 shows state 1. **Coming back from 12 shows state 2**, the way a build replays in reverse. That is the choice I made. One more "back" then goes to state 1, and another goes to 10.
- **What stays the same.** The counter stays "11 / 16", and the progress bar and the rail follow the scroll as before.

**The key test** (Playwright key presses, 1920×1080, `notes/_lanes/297/C/_work/navtest_c.py`):
```
start deckGo(10) -> slide 10 (10 / 16)
ArrowDown -> slide 11 (11 / 16) state 1
ArrowDown -> slide 11 (11 / 16) state 2   [marks 1, note 1]
ArrowDown -> slide 12 (12 / 16)
ArrowUp   -> slide 11 (11 / 16) state 2
ArrowUp   -> slide 11 (11 / 16) state 1
ArrowUp   -> slide 10 (10 / 16)
```
- The same sequence with Space / Space / PageDown / PageUp ×3 gives the same result.
- Control: from 03, ↓ ↓ goes to 04 then 05, and from 13, ↑ goes to 12, all unchanged.
- **The wheel:** this headless shell never scrolls on wheel input, and the pre-change deck does not move either. So `wheeltest_c.py` checks the handler itself. On 10 a wheel down passes. On 11 a wheel down is taken and gives state 2. On state 2 a wheel down passes (a browser then scrolls to 12). A wheel up on state 2 is taken and gives state 1. On state 1 a wheel up passes. A 20-event fling on 11 is all taken, and gives state 2 once.
- **UNPROVEN:** a real trackpad in a headed browser. The price is one run on Dave's laptop.

## 4 · Checks

- **Renders:** all 16 slides plus 11's second state, at 1920×1080 and 1440×900 (`notes/_lanes/297/C/_work/after-1920/`, `after-1440/`). The harness freezes as lane A's does.
- **Rail:** lane B's `rail_check.py` JS, run on every render. **0 hits at both sizes.**
- **Overflow:** every text line box was checked against the viewport, against its nearest painted box, against every other text line (overlap > 25% of a line), and for any clipped element.
  - **0 at both sizes except 11's second state.** There, the note is "outside" the Speed card box because it is placed below the card on purpose. It touches nothing.
  - The checker's first cut flagged 1.7–2.9px overlaps between two-weight headline lines on 04 and 05 in the *pre-change* deck. That was the tight line-height; the threshold was raised and nothing else changed.
- **I looked** at 04, 06, 11 (both states), 12 and 13 at 1920 in full, and at a 1440 sheet. They match lane B's pairs, apart from 11's ruled changes. One thing was fixed on the way: "Highly variable design / skills" on 06.
- 0 page errors and 0 console errors on every run.

## Deviations

- **The rule on 11's second state stands upright, not over the cause** (see section 3). This is the one design call not in the brief's example list. It is still the deck's red rule, dashed for "not yet".
- **06's description is shorter than the brief's example.** It drops "and accessibility is fixed late" (see section 1).
- **Going back from 12 shows 11's second state.** The brief allowed either; this is the choice.
- **The gearbox and books drawings still bake off-screen** (`#gbHost`, `#bkHost`), unused now that 12 shows the catalogue and the graph. I did not remove them, since that was not asked for and would be a large code removal.
- W-297b (lane B's row) closes when Dave "has ruled on the five diagram proposals … and picked a corrected line for 07". Only the first half is now true, so the row is left open.

## Files

- **Changed:** `notes/_lanes/296/C/v14-plain-before-c.html` (the source) · `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt) · `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (appended)
- **New:** `notes/_lanes/297/C/for-dave.html` · this report · store row W-297c · `_CHAIN.md` (regenerated)
- **Working, not committed:** `notes/_lanes/297/C/_work/`
  - `apply_c.py` and `block_c.html`: the enactment, re-runnable from `source.pre-297C.html`
  - `shoot_c.py`, `navtest_c.py`, `wheeltest_c.py`, `make_for_dave.py`
  - `before-1920/`, `after-1920/`, `after-1440/` and the pre-change copies of the source, builder and deck
