# 2026-09-22 · #296 · Lane C — chapter rail (orientation pattern) in the v14-plain deck

## VERDICT
Built and rendered: 15 slides, 0 page errors, 0 console errors. The rail is fixed to the left edge and does not scroll with the slides. It sits in exactly the same place on every slide from s2 on (box 16,297 · 200×306 on all 15). The right chapter grows on every slide, the sub-page dot lights on all 6 sub-pages, and the rail switches to light ink on all 5 dark slides. The circles and dots stay clear of slide content everywhere, with a 42 px gap on the tightest slides. The TITLES overlap content on 4 slides: s5x, s6, s7 and s8 (px below). No slide content was moved.

## WHAT WAS BUILT
- The deck was edited in place: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (475,614 → 482,745 B). The before-copy is `notes/_lanes/296/C/v14-plain-before-c.html`.
- There are 3 insertions: one `<style data-lane="296-C">`, one empty `<nav id="chrail">` (both placed right after the keyhint, outside `.deck`), and one `<script data-lane="296-C">` placed before `</body>`. The diff shows 0 lines removed or changed and 121 added. Scripts, assets, brain constants, slide markup and footers are byte-identical.
- The script builds the rail from `RAIL`. Build script: `notes/_lanes/296/C/build_c.py`. It is idempotent and rebuilds from the before-copy each run.
- How the current slide is found: by position, the same rule the deck uses. A slide counts as current once its offsetTop is at or above the deck's scroll top plus half a screen. It updates on deck scroll (rAF) and on resize.
- The rail has two classes. Chapter: a 10 px hollow circle; when current it becomes a 28 px circle with the number inside (12 px) and its title to the right in the deck's label type (12 px, .14em, caps, accent red) with a 16 px red rule. Sub-page: a 5 px filled dot; the current sub-page's dot becomes a 9 px accent dot, and its chapter is grown at the same time. The other titles show at 7 px caps in grey. There is a 1 px line through the marker column. Row heights are fixed at 30 px and 16 px and the nav is 200 px wide, so the box never changes.
- Themes: `is-dark` (white ink, #F6604C accent) and `is-grey` (circle fill matches the #F3F3F3 ground) are read from the current section's class.
- Clicking a circle or dot scrolls smoothly to its slide. Tested: chapter 6 → s9, sub-dot 2 → s7. The deck's arrow keys also move the rail (ArrowDown → Response, sub lit).
- Transitions are 200 ms. They are turned off under reduced-motion. The rail is hidden in print.

## THE DATA ARRAY (verbatim)
```
var RAIL = {
  hideOn:     ['s1'],      // rail hidden on these slides (cover); shown everywhere else
  tinyTitles: true,        // first version: every chapter title shown, very tiny
  chapters: [
    {n:1, title:'Observation', id:'s3',  subs:[]},
    {n:2, title:'Problem',     id:'s4p', subs:[]},
    {n:3, title:'Experiment',  id:'s5x', subs:[]},
    {n:4, title:'Results',     id:'s5r', subs:[]},
    {n:5, title:'Response',    id:'s6',  subs:['s6b','s7','s8']},
    {n:6, title:'The build',   id:'s9',  subs:['s10','s10map']},
    {n:7, title:'The ask',     id:'s11', subs:['s12']}
  ]
};
```

## DEFAULTS TAKEN (conductor's, each open to Dave)
The rail is hidden on the cover and shown from the agenda with nothing current. The chapter mapping above is the conductor's. Tiny titles are ON. The rail is on the left, vertically centred, at 16 px from the edge. I moved it from 24 to 16 to widen the gap to content. Chapter circles are hollow; the grown circle is hollow too, with ink border and ink number. Past and future chapters look the same.

## RENDER RECEIPTS
- Errors: pageerror 0, console.error 0 (`notes/_lanes/296/C/measured.json`).
- Rail box, the same on all 15 slides: left 16 · top 297 · 200×306. s1 has opacity 0.
- Grown circle is 28 px. Plain chapter circle is 10 px. Sub dot is 5 px, and 9 px when current. Tiny title is 7 px; current title is 12 px.
- Current chapter per slide: s3 Obs · s4p Prob · s5x Exp · s5r Res · s6/s6b/s7/s8 Response (sub lit on s6b, s7, s8) · s9/s10/s10map The build (sub lit on s10, s10map) · s11/s12 The ask (sub lit on s12). s2 has none.
- Overlap: rail markers end at x=44. Content starts at x=160 on most slides and at x=86.4 on s6, s7 and s8 (split layouts). Measured title-over-content overlap:
  - s5x: the grown "EXPERIMENT" title runs 10.8 px into the lead line's box. On screen it sits just below the lead; the text does not visibly collide.
  - s6: the tiny titles run 32.3 px into the h2 ("The first improvement…"). The grown "RESPONSE" title runs 69.8 px into the body copy and is visibly on top of "125 components".
  - s7: the tiny titles run 32.3 px into the h2 and 11–18 px into the body.
  - s8: the tiny titles run 32.3 px into the label, 27.5 px into the h2 and 9–18 px into the body.
  - No overlap on s2, s3, s4p, s5r, s6b, s9, s10, s10map, s11, s12.
- PNGs (1440×900 @2x): `notes/_lanes/296/C/{s1,s2,s3,s4p,s5x,s5r,s6,s6b,s7,s8,s9,s10,s10map,s11,s12}.png`, `contact-sheet.png`, and DPR 3 crops `rail-s6b.png` and `rail-s5r.png`. All were checked by eye.
- Driver: `notes/_lanes/296/C/shoot.py`.

## UNPROVEN
- Checked only at 1440×900. On narrower screens the content moves further left, so more overlap is likely.
- Smooth-scroll click with the in-file animations was tested headless only, not on Dave's machine.
- Fonts fell back from Univers Next at the seat, so title widths may differ slightly.
- Not tested with a screen reader: aria-current and the button labels are there.

## QUESTIONS FOR DAVE
1. The agenda (s2) now reads Observation · Problem · Analysis · Experiment · Results · Response, and s5x is labelled "Analysis · the experiment". The rail uses the conductor's seven: Observation · Problem · Experiment · Results · Response · The build · The ask. Should the rail match the agenda (add Analysis, and on which slide?), or keep these seven?
2. s6, s7 and s8 have content right against the left edge, so the titles sit on top of it (the worst is the grown "Response" title on s6, 70 px). Options: drop the tiny titles once you've checked the mapping, show only the grown title on those slides, or give those slides more left room?
3. Should the rail show progress, with chapters already passed filled in, or stay neutral as now?
4. Hidden on the cover and shown on the agenda with nothing current: is that right, or should the agenda also hide it?

---

## v2 — Dave's ruling (full-height line, current chapter anchored, masked circles, bigger)
Dave, verbatim: "I'm using a a large screen the collision wont happen. Can we have the line go all the way down the screen, and the items up to the top, the circles with the number have a line running through it, can we remove. Can we somehow have the current slide number in the same position by bunching the others up or something, there is more space to play with if we have the line span the entire height, and the circle and title bigger"

### VERDICT
v2 is built and rendered: 7 slides plus 3 rail crops, 0 page errors, 0 console errors. On every slide that has a current chapter, the grown circle's centre sits at exactly y=342 (38% of 900). The line runs from 0 to 900. No line shows through any circle. The rail inverts on dark slides. Nothing is clipped at the top or bottom. Overlap with slide content is no longer tracked (ruled out by Dave).

### WHAT CHANGED
- The v1 deck is kept at `notes/_lanes/296/C/v14-plain-rail-v1.html` and its build at `build_c_v1.py`. v2 is the same deck, edited in place, 484,707 B. It is still 3 insertions with 0 original lines changed. Only the 296-C style and script differ from v1.
- The nav is fixed from top 0 to bottom 0, 280 px wide. The line is the full viewport height at x=38.
- Every circle is filled with the current slide's ground (white, grey #F3F3F3 or black, read from the section's class). It sits above the line, so the line stops at its edge.
- The rail re-lays out on every slide:
  - The current chapter goes to `anchor × viewport height`.
  - Items before it spread evenly from `anchor − clear` up to `topInset`.
  - Items after it spread evenly from `anchor + clear` down to `viewport − bottomInset`.
  - Sub-page dots move with their chapter.
  - Positions animate over 250 ms. On the agenda (nothing current) the items spread evenly top to bottom.
- Sizes: the grown circle is 44 px with a 22 px weight-300 numeral in the deck's display weight. The current title is 18 px (label 12 × 1.5), .14em, accent red, with a 24 px red rule. Plain circles are 12 px. Sub-dots are 6 px, and 10 px accent when current. Tiny titles stay at 7 px and on.

### DATA ARRAY (v2, verbatim head; chapters unchanged from v1)
```
var RAIL = {
  hideOn:      ['s1'],
  tinyTitles:  true,
  anchor:      0.38,   // current chapter's centre, fraction of viewport height
  topInset:    40,     // px
  bottomInset: 40,     // px
  clear:       40,     // px gap between grown circle centre and its neighbours
  chapters: [ ...same seven as v1... ]
};
```

### MEASUREMENTS (1440×900, `notes/_lanes/296/C/v2-measured.json`)
- Grown circle centre y: s3 342 · s6 342 · s6b 342 · s5r 342 · s10map 342 · s12 342. s2 has no current chapter, by design. All at x=38.
- Line: top 0, bottom 900 on all 7.
- Sizes: grown circle 44 px, numeral 22px/300, current title 18 px, plain circle 12 px, dot 6 px, current sub-dot 10 px, tiny title 7 px.
- Masking: a pixel on the line's x inside the grown circle, 16 px above and 16 px below its centre, equals the ground on all 6 slides: (0,0,0) dark, (255,255,255) white, (243,243,243) grey. On the line just outside the circle the pixel is (85,85,85) dark or (175–180) light, so the line is there and stops at the circle. The circle fill matches the slide background on every slide.
- Rail items never collide with each other (0 box clashes on all 7). The item extent is 34 → 863 px, so nothing is clipped.
- Current and sub-page state: s6b and s10map have their sub-dot lit, and so does s12 (last chapter, everything above). s3 is the first chapter, with everything below.

### PNGs
`notes/_lanes/296/C/v2-{s2,s3,s6,s6b,s5r,s10map,s12}.png` (DPR 2), `v2-rail-{s3,s6b,s12}.png` (DPR 3, left 320 px, full height), `v2-rail-3up.png`. All checked by eye. Driver: `notes/_lanes/296/C/shoot_v2.py`.

### UNPROVEN (v2)
- The 250 ms slide of the re-layout is set in CSS but was not caught mid-flight. The one mid-animation sample was s6b → s7, which is the same chapter, so nothing moves.
- Items are spread evenly, so with only one or two items below the anchor the gaps are large (s11 has 1 dot below). That is by spec, not tested with Dave.
- On a very short viewport, fewer than about 20 px per item would bunch the dots tight. Not tested.

### QUESTIONS FOR DAVE (v2)
1. The items above and below spread evenly over the whole space, so early chapters sit far apart (on s6b, 170 px between Observation and Problem). Is that right, or should they bunch closer to the current chapter with a fixed step, leaving the line empty towards the edges?
2. Is the anchor at 38% of the height right, or should it be the vertical centre?

---

## v3 — fixed spacing everywhere, tiny titles off
Dave, verbatim: "okay this is looking cool, lets keep the same spacing for items below that we have when we have the final slide so its all laid out and easy to see and remove the title from the chapters apart from the current one"

### VERDICT
v3 is built and rendered: 4 slides plus 3 rail crops, 0 page errors, 0 console errors. The spacing between items is now one fixed value, 22 px, above and below the current chapter on every slide. The only exception is the gap either side of the large circle, which stays at 40 px as in v2. The current chapter still sits at y=342 on all four slides. Only the current chapter shows a title. Nothing runs off the top or bottom.

### WHAT CHANGED
- The v2 deck is kept at `notes/_lanes/296/C/v14-plain-rail-v2.html` and its build at `build_c_v2.py`. v3 is the same deck, edited in place, 485,203 B. The only change is inside the 296-C script.
- New one-line setting `step: 22`. It comes from the v2 layout on s12 at 900 px height: (342 − 40 − 40) / 12 = 21.8 px between items above the anchor, rounded to 22.
- Items before the current chapter stack upward from `anchor − clear` in 22 px steps. Items after it stack downward from `anchor + clear` in 22 px steps.
- The line is still full height, and it runs bare past the ends of the stack.
- The agenda (s2, nothing current) still spreads the items evenly. That was left unchanged.
- `tinyTitles: false` means only the current chapter's title shows. Setting it to true brings the tiny titles back.
- Nothing else changed: sizes, masking, colours, anchor, transitions and the click and keyboard behaviour are the same as v2.

### MEASUREMENTS (1440×900, `notes/_lanes/296/C/v3-measured.json`)
Gaps between the centres of consecutive items, top to bottom:
- s3: 40, then 22 × 11
- s6b: 22, 22, 22, 40, 40, 22 × 7
- s10map: 22 × 7, 40, 40, 22 × 3
- s12: 22 × 10, 40, 40

So every gap is 22 px except the two either side of the large circle, which are 40 px.
- Large circle centre y: 342 on s3, s6b, s10map and s12, unchanged.
- **Extent (from item centres):**
  - s3: the first chapter is at the anchor and the stack runs down to a last dot centred at 624. The dot ends at about 627, well above the 900 px edge.
  - s12: the stack starts with a circle centred at 82 (top edge at 76) and ends with the lit sub-dot at 382.

  Nothing is clipped. At 22 px spacing the full stack is 13 items tall, so it fits on screens down to about 560 px high.
- Titles visible: s3 Observation, s6b Response, s10map The build, s12 The ask. There is one title per slide.
- Line top 0 and bottom 900. 0 collisions between rail items. The circle interior matches the slide ground on all four slides. The rail inverts on s3 and s12.
- The re-layout animates. Going from s3 to s9, chapter 6's centre was at 366 px 120 ms after the jump and settled at 342 px.
- PNGs: `notes/_lanes/296/C/v3-{s3,s6b,s10map,s12}.png` (DPR 2), `v3-rail-{s3,s6b,s12}.png` (DPR 3), `v3-rail-3up.png` (s3 · s6b · s12). All checked by eye. Driver: `shoot_v3.py`.
- One thing in the log to ignore: the JSON's `itemsTop` shows 0 because the hidden titles report empty boxes. The extent above is taken from the item centres instead.

### QUESTION FOR DAVE (v3)
1. The large circle keeps a 40 px gap to its neighbours, and everything else is 22 px apart. Should that gap tighten to 22 px as well, or keep the breathing room?

---

## v4 — more air, hidden on the agenda, eyebrow-size title
Dave, verbatim: "don't worry about the gap right now, its looking pretty good, we need a bit more space between the progress points, it's looking a bit congested and the rest of the deck is pretty minimal. Lets just remove it from slide 2, and I think the circle title was better smaller, maybe same size as the eyebrow text on the slides themselves"

### VERDICT
v4 is built and rendered: s1, s2, s3, s6b, s12 plus 3 rail crops, 0 page errors, 0 console errors. The rail is now hidden on s1 and s2. The current title matches the slide eyebrow exactly. The spacing target is now 34 px, but at 900 px high the full stack does not fit at 34, so the rail uses the largest spacing that does: 26.2 px. On a screen 1105 px high or more it gets the full 34 px (proven at 1920×1200).

### CORRECTION TO v3
The v3 section said the s12 spacing was (342−40−40)/12 = 21.8, rounded to 22. That was wrong. There are 11 items above the anchor on s12, so 10 gaps, and the true v2 spacing was 262/10 = 26.2 px. v3 therefore ran tighter (22) than the "final slide" spacing Dave asked for.

### WHAT CHANGED
- The v3 deck is kept at `notes/_lanes/296/C/v14-plain-rail-v3.html` and its build at `build_c_v3.py`. v4 is the same deck, edited in place, 485,878 B. The only changes are inside the 296-C style and script.
- `hideOn: ['s1','s2']`.
- `step: 34` is now a target:
  - The script works out one spacing per screen height and uses it on every slide.
  - It is either 34 or the largest value that still fits the two worst cases: last chapter current (10 gaps above, stopping 40 px from the top) and first chapter current (11 gaps below, stopping 40 px from the bottom).
  - At 900 px high the top case limits it to (342 − 40 − 40)/10 = 26.2 px. The bottom case would allow 43.5 px.
  - It reaches 34 px at about 1105 px high.
- Current title: 12 px, weight 500, .14em tracking (1.68 px), uppercase, line-height 1.4, with a 24 px red rule and an 8 px gap. That is exactly the deck's `.label` rule. The 44 px circle is unchanged.
- The 40 px gap either side of the large circle and everything else are as in v3.

### MEASUREMENTS (`notes/_lanes/296/C/v4-measured.json`)
- Spacing at 1440×900:
  - s3: 40, then 26.2 × 11
  - s6b: 26.2 × 3, 40, 40, 26.2 × 7
  - s12: 26.2 × 10, 40, 40

  One value throughout, apart from the 40 px either side of the large circle.
- Spacing at 1920×1200: s3 and s12 have gaps of only {34, 40}. The anchor is at 456 there. s12's top centre is at 76 and s3's last centre is at 870, both inside the 1200 px screen.
- Title against the slide eyebrow, on s3, s6b and s12: rail title [12px, 500, 1.68px, uppercase, rule 24px], slide `.label` [12px, 500, 1.68px, uppercase, rule 24px]. They match.
- Stack extents at 900 px:
  - s3: current chapter at 342, last dot centred at 670.2 (edge about 673). Clear of the bottom.
  - s12: top circle centred at 40 (edge 34), last lit dot at 382. Clear of the top.
- Large circle centre y: 342 on s3, s6b and s12. Line from 0 to 900. 0 collisions between rail items. The circles still hide the line on all three.
- Rail absent: s1 and s2 both have opacity 0 and 0 clickable rows.
- PNGs: `notes/_lanes/296/C/v4-{s1,s2,s3,s6b,s12}.png` (DPR 2), `v4-rail-{s3,s6b,s12}.png` (DPR 3), `v4-rail-3up.png`. All checked by eye. Driver: `shoot_v4.py`.

### QUESTION FOR DAVE (v4)
1. At 900 px high the spacing can only reach 26 px, because the current chapter sits 38% of the way down. Lowering it to about 45% would give the full 34 px on a 900 px screen too. Keep 38% (34 px on your large screen), or lower the anchor?

---

## v5 — everything but the current chapter faded
Dave, verbatim: "okay one last thing for this, I'd really like anything other than the current chapter to be faded so that it looks less congested, lets use a much lighter grey on the white backgrounds and a darker on the dark, lets really make the everything other than the current chapter stand out"

### VERDICT
v5 is built and rendered: s3, s6b and s12 plus 3 rail crops, 0 page errors, 0 console errors. Everything that is not the current chapter is now faded: the line, the other circles and the other chapters' dots. The current chapter stays at full strength. Its own sub-dots sit at mid-grey so it reads as a group, and the current sub-page's dot stays red. The faded marks are still visible in all three crops, as a faint guide.

### COLOURS (deck neutral tokens only, from :root)
- Light and grey slides:
  - faded = `--g3` #D7D8D6, for the line, other circles and other chapters' dots
  - current chapter's own sub-dots = `--g5` #9B9B9B
- Dark slides:
  - faded = `--g8` #333333
  - current chapter's own sub-dots = `--g6` #767676
- The line no longer has opacity .55. It is a solid 1 px line in the faded colour.

### WHAT CHANGED
- The v4 deck is kept at `notes/_lanes/296/C/v14-plain-rail-v4.html` and its build at `build_c_v4.py`. v5 is the same deck, edited in place, 486,906 B. The only changes are inside the 296-C style and script.
- Two new rail colours, `--rfade` and `--rmid`, are set per theme.
- Each circle and dot now records which chapter it belongs to. On every slide change the current chapter's sub-dots are marked `is-grp`, which gives them the mid-grey. The mark is cleared when the chapter changes.
- Nothing else changed: spacing, anchor, sizes, title, masking and hiding on s1 and s2 are all as in v4.

### COMPUTED COLOURS (`notes/_lanes/296/C/v5-measured.json`)

| element | s6b (light/grey) | s3 / s12 (dark) |
|---|---|---|
| line | rgb(215,216,214), opacity 1 | rgb(51,51,51), opacity 1 |
| non-current circle | rgb(215,216,214) | rgb(51,51,51) |
| non-current sub-dot | rgb(215,216,214) | rgb(51,51,51) |
| current-chapter sub-dot | rgb(155,155,155) | #767676 by rule; not measured: neither dark slide has a non-current sibling sub-dot |
| current sub-page dot | rgb(218,26,0) | rgb(246,96,76) (s12) |
| current circle stroke / number | rgb(0,0,0) / rgb(0,0,0) | rgb(255,255,255) / rgb(255,255,255) |
| current title / rule | rgb(218,26,0) | rgb(246,96,76) |

Unchanged from v4: large circle centre y is 342 on all three, the line runs 0 to 900, no rail items collide, spacing is 26.2 px at 900 high, and the circles still hide the line.

### VISIBILITY (checked by eye, DPR 3 crops)
- **s6b (grey ground):** the #D7D8D6 circles and line are faint but clearly legible. The two Response sub-dots after the red one show mid-grey and read as belonging to chapter 5.
- **s3 and s12 (black ground):** the #333 circles, dots and line are faint but legible. Nothing is lost.
- Not rendered this round: a pure-white slide. #D7D8D6 on white has a little more contrast than on #F3F3F3, so it should be at least as visible as on the grey slide.

### PNGs
`notes/_lanes/296/C/v5-{s3,s6b,s12}.png` (DPR 2), `v5-rail-{s3,s6b,s12}.png` (DPR 3), `v5-rail-3up.png`. Driver: `shoot_v5.py`.

---

## v6 — the s2 → s3 jump, fixed (plain deck)
Dave, verbatim: "there is a strange jump with the rail from slide 2 to 3, I think that the rail on two is very spaced out but the visibility is set to zero so there is movement on the transition from 2 to 1."

### CAUSE
On s2, the rail was hidden (opacity 0) but still laid out with the items spread evenly over the full height, because no chapter was current. Entering s3 animated that spread layout into the stacked one while it faded in. Leaving s3 did the reverse.

### FIX
- On any hidden or unmapped slide (s1, s2), the rail now takes on the FIRST chapter's exact state: the same positions, the same grown circle and the same theme (s3's dark).
- So s2 → s3 changes only opacity (and makes the rail clickable). The rail simply fades in.
- `aria-current` is set only when the rail is visible.
- The evenly-spread layout remains only as a fallback if no chapter is current, which no longer happens.
- The v5 deck is kept at `notes/_lanes/296/C/v14-plain-rail-v5.html` and its build at `build_c_v5.py`.
- `build_c.py` is now a module: `build(src, dst, chapters)`, which asserts "you can bank on" after building. Its source `v14-plain-before-c.html` already carries Dave's new closing line. I checked that the live plain deck with the rail stripped equals that file byte-for-byte, so nothing was reverted. The rebuilt deck is 487,227 B and contains "you can bank on".

### MEASURED (plain, 1440×900, `notes/_lanes/296/C/v6-plant-measured.json`)
- Item positions on s2 (hidden) and on s3: identical, all 13 items (centre y and size).
  s3: [342/44, 382, 408.2, 434.4, 460.6, 486.8, 513, 539.2, 565.4, 591.6, 617.8, 644, 670.2].
- Frame 120 ms after jumping s2 → s3: positions identical to s3. Opacity was 0.93 at that moment, so the rail was mid-fade with nothing moving.
- 120 ms after going back s3 → s2: identical. The rail only fades out.
- s2 state: opacity 0, 0 clickable rows, 0 aria-current. s3: opacity 1, current chapter "1 Observation", centre y 342.
- 0 page errors, 0 console errors.
- PNGs: `v6-rail-s2.png` (s2 with the hidden rail forced visible for the picture only, to show it already sits in its s3 state, dark theme included), `v6-rail-s3.png`, and `v6-rail-s2-s3.png` side by side.

---

## plant — the same rail in the plant deck
Dave, verbatim: "after this is fixed can you add the same progress indicator to the plant deck too"

### WHAT WAS BUILT
- Deck: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plant.html` (484,245 B). The pre-rail copy is `notes/_lanes/296/C/v14-plant-before-rail.html`.
- Builder: `notes/_lanes/296/C/build_c_plant.py`. It imports `build_c` and inserts the same three blocks (style, `<nav id="chrail">`, script) with only the chapters list changed.
- The builder asserts that the rail code is byte-identical between the two decks, chapters list excluded: style + nav 5,040 B, script minus chapters 6,169 B. The assertion passes.
- "you can bank on" is asserted present in the plant deck as well.
- Chapters list (plant):
```
  chapters: [
    {n:1, title:'Why now',               id:'s3',        subs:[]},
    {n:2, title:'Systemised design',     id:'s4',        subs:[]},
    {n:3, title:'The experiment',        id:'s5',        subs:[]},
    {n:4, title:'The insight',           id:'s5insight', subs:[]},
    {n:5, title:'The breakdown',         id:'s5break',   subs:[]},
    {n:6, title:'What we built',         id:'s6',        subs:['s7','s8']},
    {n:7, title:'The build and the ask', id:'s9',        subs:['s10','s10map','s11','s12']}
  ]
```
- Hidden on s1 and s2 through the shared `hideOn`. Every other setting is the shared one.
- The comment in the shared settings that quotes "26.2px at 900px" is true for the plain deck only. The plant deck's last chapter has fewer items above it (7 gaps), so it gets the full 34 px at 900 px high.

### MEASURED (plant, 1440×900)
- 0 page errors, 0 console errors.
- Rail present and current on every slide from s3. Large circle centre y is 342 and diameter 44 on all 13 shown slides.
- Current chapter per slide:
  - s3 Why now
  - s4 Systemised design
  - s5 The experiment
  - s5insight The insight
  - s5break The breakdown
  - s6, s7, s8 What we built (sub-dot lit on s7 and s8)
  - s9, s10, s10map, s11, s12 The build and the ask (sub-dot lit on s10, s10map, s11 and s12)
- s1 and s2: opacity 0 and 0 clickable rows, sitting in the chapter-1 state.
- Spacing: 34 px (s3 gaps 40, then 34 × 11). The last item is centred at 756, so the stack fits.
- Title fit: every title is 12 px on one line (height 16.8 = 12 × 1.4, no overflow). "The build and the ask" is 211.8 px wide on one line and does not wrap.
- Inversion: `is-dark` on s3, s9 and s12. `is-grey` on s5insight, s10 and s10map.
- Faded palette:
  - light: line, other circles and dots are rgb(215,216,214); the group dots are rgb(155,155,155); the current dot is rgb(218,26,0)
  - dark: line, other circles and dots are rgb(51,51,51); the group dots are rgb(118,118,118); the current dot is rgb(246,96,76)
- No jump s2 → s3: s2 and s3 positions are identical, the frame 120 ms after the jump is identical, and so is the way back.
- Checked by eye (contact sheet and crops): the rail shows on every slide from s3, the grown chapter is correct, the faded marks are visible, and nothing is clipped. The current title overlaps some slide headlines at 1440, which Dave ruled not a concern.

### PNGs
`notes/_lanes/296/C/plant-{s1,s2,s3,s5insight,s6,s7,s9,s11,s12}.png`, `plant-contact-sheet.png`, `plant-rail-{s3,s7,s12}.png`, `plant-rail-3up.png`. Driver: `shoot_v6.py`.
