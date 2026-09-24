# #302 B: the benefits slide (new 15 of 17)

**Dave, 11:28 BST, verbatim:** "I want to add another slide probably between 11 and 12, but you might have other ideas: Benefits beyond speed, quality and consistency / Building our own code-first agents lets us reduce reliance on traditional third-party design tools that we have limited control over. We can: / * Build specifically for our needs, controlling and refining Apollo content directly / * Align teams around shared ways of working, converging on best practices and design systems other business can adopt / * Reduce licence costs (Figma alone cost $3.2m in 2025-26, before any AI add ons)"

**DONE.** The new slide sits after the demo ("Let's see what it's made", 14) and before the ask. The ask is now 16 and the close is 17. The callipers were not touched.

## The slide (`id="s11pre"`, grey ground)
- **Ground:** grey, between the dark demo and the white ask.
- **Label:** "Beyond the three".
- **Headline (h2):** "Benefits **beyond speed, quality and consistency**", with the phrase in bold as the deck does. There is no full stop, because his wording has none.
- **Lead:** his sentence, ending "We can:".
- **Three numbered columns (01 02 03):** built on the deck's number-card rules (`.nums`), with the accent-red index numbers the deck already uses.
  - Each column carries his point verbatim, apart from the agreed typographic fixes: "other businesses", "2025–26", "add-ons", and non-breaking spaces against widows.
- **The figure:** column 3 carries **$3.2m** large, in the deck's own figure style (`.fig`: light weight, 48–88 px). No new colours.
  - It sits under his full sentence, which also states $3.2m, so his words stay whole. The large figure is `aria-hidden`, so a screen reader doesn't read it twice.
  - If Dave wants it said once, the option is to drop "$3.2m" from the sentence. That would be a wording change, so it is his call.
- **Reveal:** the same `.rv d1–d4` stagger as its neighbours. It has no data-steps.
- **Styling:** scoped in `<style data-lane="302-B">`.
  - The columns are pinned three-up at every width, as `#s10 .grid4` is. The deck's phone rule (`max-width:820px`) also fires in print, where it stacked the columns and pushed the slide past its page.
  - Print sizes are set explicitly.

## Mechanics
- **Source:** `notes/_lanes/296/C/v14-plain-before-c.html`, backed up first as `notes/_lanes/302/B/v14-plain-before-c.BEFORE-B.html`. The edit script is `notes/_lanes/302/B/edit_slide.py`, and two small CSS follow-ups are recorded in `source.diff`.
- **Pagenums:** all 17 now read NN / 17, and the ask and close are 16 and 17. The prose note "s6b (11 / 16)" in the data-steps script now reads 11 / 17.
- **Navigation:** it is positional (`querySelectorAll('.slide')`) in both scripts, and nothing hardcodes the count or the ids. The id `s11pre` was unused. The print rule `.slide:last-of-type` still lands on the close.
- **Rail:** in `build_c.py`, chapter 5 "Result" now has `subs:['s11pre']`, with a dated v10 comment quoting Dave.
  - The chapters are unchanged, so **slide 02's order of play needs no change** (confirmed; it is untouched).
- **Deck:** rebuilt with `build_c.py` only. `build_e.py` was not run; no git, no Project memory.

## Checks
- **Full deck at 1600x900** (`shoot_w.py`): **17 renders, 0 rail hits, 0 overflow, 0 errors.**
  - One overflow was found and fixed on the way: the $3.2m glyphs sat 2.5 px past the columns' box.
- **At 1280x720**, via `notes/_lanes/302/B/shoot_one.py`, which scrolls to the slide directly: 14, 15 (new) and 16 each have **0 text outside the slide, 0 rail hits and 0 errors**. The nearest approach to the rail is 71.5 px on the new slide.
  - The full-deck driver can't check 1280x720. From slide 12 on its shots drift, because 12's content is taller than 720, and it flags the pagenums of 12–16 as off-viewport.
  - This happens identically on the pre-edit deck (`shots-1280-before`), so it is pre-existing and not this slide.
- **Print:** a PDF from the deck's own print CSS (A4 landscape) has **17 pages**. With print media, every slide's text sits inside its slide box. Page 15 was looked at: three columns, everything on the page.
- **Pixel diff against the pre-edit deck at 1600,** with the rail band, pagenum and progress bar masked (they are meant to move):
  - Slides 1–14 are the same.
  - The old 15 and 16 (the ask and the close) are the same as the new 16 and 17.
  - The only content change is the new slide.
- **By eye:** 14, 15 and 16 at 1600 and at 1280. The rail shows the new slide as Result's sub-dot.

## Files (under notes/_lanes/302/B/)
- **`new-slide.png`: 14, 15 (new) and 16 in a row, labelled**
- `shots-1600/` (the full deck, after), `s9-1280.png`, `s11pre-1280.png`, `s11-1280.png`, `shots-1280/`, `shots-1280-before/`
- `deck-print.pdf`, `print-15b.png`
- `source.diff`, `edit_slide.py`, `shoot_one.py`, `build_c.BEFORE-B.py`, `deck.BEFORE-B.html`

---

# Revision: a headword on every column (Dave, 11:44 BST)

**Dave:** "okay lets, have the figure at the top of the panel under 03. lets add, in the the a consistent but large type-scale -- Tailored, Aligned, $3.2m or maybe Economic with the 3.2 highlighted in a different way"

**DONE. In the deck: reading A.**

## The change
- **Headwords:** every column now has a large headword straight under its number and above his sentence.
  - All three are set at **one size, the deck's existing `.fig.small` step**: the number card's second figure, 30–54 px on screen and 44 px in print, light weight.
  - In the browser the font renders the light weight near regular. That is the same for all three, so they match.
- **The $3.2m at the foot** of column 3 is gone.
- **Reading A (in the deck):** Tailored · Aligned · **$3.2m**. The figure is the third headword, and his sentence under it is unchanged.
- **Reading B (ready):** Tailored · Aligned · **Economic**. The "$3.2m" inside his sentence is set in **the labels' accent red** (medium weight).
  - I chose red over bold because red is the one device the deck already uses for emphasis at small sizes (labels, the 01 02 03 numbers). Bold would read as a second heading inside the sentence.
- **Swap:** `python3 notes/_lanes/302/B/swap_benefits.py A|B` swaps the two strings and rebuilds with build_c.py. It is safe to run twice.
- **Script:** `edit_headwords.py`. The pre-revision source is `v14-plain-before-c.PRE-HEADWORDS.html`, and the two built decks are `deck.hwA.html` and `deck.hwB.html`.

## Checks
- **Full deck at 1600x900, A:** **17 renders, 0 rail hits, 0 overflow, 0 errors.**
- **Slide 15 at 1600x900 and 1280x720, both A and B:** 0 text outside the slide, 0 rail hits, 0 errors.
- **Print:** both PDFs have 17 pages, and page 15 was looked at for each. The headwords sit at 44 px, three columns, everything on the page.
- **By eye:** 1600 and 1280.

## Files (under notes/_lanes/302/B/)
- **`headwords-A-B.png`:** A and B at 1600, and each as printed, labelled
- `hwA-1600x900.png`, `hwA-1280x720.png`, `hwB-*.png`
- `print-hwA.pdf`, `print-hwB.pdf`
- `shots-hwA/` (the full deck)
- no git, no build_e.py, no Project memory
