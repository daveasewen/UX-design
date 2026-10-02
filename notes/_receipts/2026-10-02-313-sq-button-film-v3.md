# #313 side-quest receipt — film B v3 (continues `2026-10-01-313-sq-button-film.md`)

provenance: 313-sq · 2026-10-02 08:18 BST · Opus 5.5 side-quest WORKER seat (cloud, linked to Dave's computer)
status: v3 built, put to Dave · commit state: UNCOMMITTED, for the #313 conductor · rulings: none

## His words, verbatim (Fri 08:18 BST)

> Okay, the button becomes one of the particles and become black on every case, it dissolves onto the graphics and then returns to the centre as a red dot.
>
> The start is just the text, the text appears as singe words in the centre, the sentence stays centred and centre justified. the last word has a red full-stop. the text fades and the fullstop moves to the centre of the screen and becomes a button.
>
> lets keep the text in the centre of the screen the graphics will have to make space for the text.

## Landed (in `notes/_lanes/313-sq/button-film/`, all new)
`button-film-v3.src.html` + `build_button_film_v3.py` → `button-film-a-v3.html` (89.1 s, scrub bar + comments under its own key `apollo-button-film-v3-comments`), `stills-a-v3/` (31), `contact-a-v3.png`, `check-v3.png`. Font check true, page errors 0. v1 and v2 untouched.
- The red dot has its own track: on each beat it travels to one dot of the drawing, turns black at that dot's size, and comes home red.
- Every line sits at the screen's centre and re-centres as each word or phrase arrives; drawings clear a band for it (compact ones sit above it, the wheel / crowd / disc / shells part around it, the screen sits above at two-thirds size).
- The open: words one at a time, red full stop with the last word, the words fade, the stop goes to the centre and grows into the button, pressed, shrinks to the dot.
Seat's calls, his to reverse: on the lines over the dot alone (One simple thing / What if it lived in one? / Many things. In one.) the red dot IS the full stop (on the question, the point of the ?) and rides the end of the line as it builds; the close mirrors the open (the stop becomes the button) with "Apollo" beneath it; the shells no longer turn (they turned into the words).
Seat fault, caught: one push of the source to the seat reported written but had not landed; the first v3 contact sheet was from the earlier source. Caught by checksum; rebuilt and re-checked.
Context gauge at authoring: 🟡 AMBER ~40% (ESTIMATE)

## ADDENDUM — v4, Fri 08:42 BST, by addition

> so the effect I'm going for is the red dot emitting the others and dissolving rather than just moving.
>
> the red full-stops have to be about half the size, remove the easing upwards animation.
>
> the fullstop just appears at the end, no need for it to move from teh centre

LANDED (new, uncommitted): `button-film-v4.src.html` + `build_button_film_v4.py` → `button-film-a-v4.html` (89.1 s; comments key `apollo-button-film-v4-comments`), `stills-a-v4/` (31), `contact-a-v4.png`, `check-v4.png` (six frames of the colour beat: emit, dissolve, words, the dots flying home, the dot re-forming; and the open). Font true, page errors 0.
- Each bloom: the red dot stays at the centre and gives off the drawing's dots in a stream; they leave red-hot and cool to their own colour while the red shrinks and darkens away. The fold back: they fly home, warm to red, and the dot forms again. No dot is held back for the red any more (the i's dot, the tick's tip, the chain's last link are back as ordinary dots).
- Red full stops at half size (≈ a Univers full stop at 46 px); no upward drift on any word; the stop appears with the last word on every line (on the lines over the dot alone, the centre dot first dissolves, then the stop appears at the end, then goes home to the centre after the line fades).
- Found and fixed on the way: a line that arrives as one phrase was sliding in from the centre (centring followed its fade); single phrases now never slide, and multi-word lines re-centre over .3 s.
Seat fault: pushing a changed file over an existing one on the seat reported written twice and did not land (checksum unchanged); pushed to a new name and moved it into place instead. Every build here was checked against the source checksum.

## ADDENDUM — v5, Fri 12:35 BST, by addition

His 18 scrub-bar comments on v4, verbatim: `notes/_lanes/313-sq/button-film/DAVE-COMMENTS-v4.md`.
LANDED (new, uncommitted): `button-film-v5.src.html` + `build_button_film_v5.py` → `button-film-a-v5.html` (114.1 s; comments key `apollo-button-film-v5-comments`), `stills-a-v5/` (30), `contact-a-v5.png`, `check-v5-shapes.png`. Font true, page errors 0, 1.5 ms a frame.
Taken as asked: the dot travels in an arc; button half size (190 x 52); colour rings fill the screen and twist, slower towards the edge; dots coalesce — they redden as they near the point and the dot is built from what arrives (and the dot spends itself as it gives them off), across the piece; the label beat is the button with Continue; one message at a time throughout; A shape. (tooltip, square button, circle, toggle, card, pill flash up) · A size. (small, large, back) · A corner. (square to fully rounded); It waits. (a deeper box, a line across the middle) · It listens. (the red scans left to right) · It answers. (a blip, then the tick); the big spiral now turns; the many places are a map — towns, a faint grid, every road feeding one hub; copy: "What if it lived in one place?", "One place" then "that knows what everything is." then "And why.", "So every project starts with everything we know.", "Thousands" / "and thousands" / "of pieces, in one place."; no Apollo text; the end button says Get started, is pressed, and ends on the dot (loopable).
Seat's calls, his to reverse: the twist (slower outward) rather than opposite directions; the map's hub sits above the words (the words keep the centre); on the last line the thousands coalesce into its full stop, which then travels home and becomes the Get started button; the words' band is kept clear by fading dots as they pass through it, so turning drawings can turn.
Seat faults, caught: (1) dots born near the centre stayed red at rest — fixed (they cool fully as they land); (2) the coalescing cloud crossed the last line's words — fixed; (3) a push reused a staged path and delivered stale bytes — every push now goes from a freshly named staged copy, checked by checksum before the build.
