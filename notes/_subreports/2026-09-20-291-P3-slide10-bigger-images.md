# 291 · P3 — slide 10's three drawings get markedly bigger

Provenance. Dave, looking at slide 10 (the P2 three-up: 01 Parts / gearbox,
02 Knowledge / books, 03 Proficiency / brain) with a crop of the three cells,
said verbatim:

> lets make better use of the space here, the images could be bigger

That sentence and the crop are the whole of the instruction. Everything below
that is not a mechanical consequence of it is listed under RULING-SHAPED
QUESTIONS; **nothing here has been accepted by Dave.**

## VERDICT

Landed. `notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` — edited in place, the
pre-edit file preserved byte-for-byte at
`notes/_lanes/291/P3/v12-before-p3.html` (md5 `cde6432f…`) — now draws the
three anatomy pictures at **87.9% of the cell width** (gearbox and books), up
from **51.7%**. The image box went **340 × 135 → 340 × 229.5 CSS px**; the
drawn picture went **192.9 × 135 → 327.9 × 229.5** for 01 and 02, and
**145.5 × 135 → 247.3 × 229.5** for 03 (the brain is a squarer drawing —
1474 × 1368 — so at the same box height it reaches 66.3% of the cell width;
the height, the baseline of the `01 / 02 / 03` row and the copy below stay
level across the three).

The room came entirely out of the slide's top/bottom slack: **159.1 / 160.1 px
→ 111.9 / 112.9 px**. No type shrank, no copy moved within its cell, the gap
between the headline and the row is unchanged at 32 px, the rule box and the
three equal 373 px columns are intact. **No overflow** at 1440 × 900 (inner
675.3 px inside the 900 px slide; `scrollHeight` does not exceed it).
**0 page errors.** Slides 4 and 6 re-shot as regression — slide 6's PNG is
**byte-identical** to the pre-edit shot.

**No re-bake was needed.** The largest new device-pixel demand at DPR 2 is
656 × 459 (01 and 02); the baked snaps are 900 × 630 (`gbPrint`) and
1200 × 840 (`bkPrint`), and 03 needs 495 × 459 against `brPrint`'s
1474 × 1368. All three have headroom, measured in the page — so the off-screen
hosts were left exactly as P2 set them and nothing is upscaled.

## WHAT LANDED

One script, `notes/_lanes/291/P3/build_p3.py`, **2 substitutions**, both
asserted on a unique anchor. v12: 7642 → **7649 lines** (+7, of which 6 are
comment). The whole change is two CSS declarations.

**1 · The image box (the one number that matters).**

    .grid5 .pic{ … height:clamp(96px,15vh,150px) … }      →
    .grid5 .pic{ … height:clamp(150px,25.5vh,240px) … }

`display:block`, `width:100%`, `object-fit:contain`, `margin:0 0 var(--s3)`
and `mix-blend-mode:multiply` are **untouched** — so the drawings keep their
aspect ratio exactly, nothing is cropped, nothing is stretched, and the gap to
the `01` number below is the same `var(--s3)` it was.

At 1440 × 900 the middle term governs: 25.5vh = 229.5 px. The clamp's floor
(150 px) and ceiling (240 px) keep the box sane on shorter and taller
viewports; the ceiling is set so the widest-aspect drawings (1.4286) never
exceed the 340 px content box — at 240 px the drawn width would be 342.9, so
`object-fit:contain` would letterbox on height instead. The picture is never
cropped at any viewport.

**2 · A print guard, so nothing but the screen moves.**

Inside the existing `@media print` block, beside `#bkHost`/`#gbHost`:

    .grid5 .pic{height:clamp(96px,15vh,150px)}

The printed slide is a fixed 1280 × 720 box with its own type scale; growing
the picture there is a different, unasked question, so print keeps the exact
declaration it had. The print block sits after the base rule in the file, so
it wins on order at equal specificity.

**Constants, before → after (measured in Chromium at 1440 × 900, DPR 2):**

| | before | after |
|---|---|---|
| `.pic` box (CSS px) | 340 × 135 | **340 × 229.5** |
| drawn, 01 Parts (gearbox) | 192.9 × 135 | **327.9 × 229.5** |
| drawn, 02 Knowledge (books) | 192.9 × 135 | **327.9 × 229.5** |
| drawn, 03 Proficiency (brain) | 145.5 × 135 | **247.3 × 229.5** |
| drawn width as % of cell | 51.7 / 51.7 / 39.0 | **87.9 / 87.9 / 66.3** |
| cell height | 329.7 | **424.2** |
| cell width | 373 | 373 (unchanged) |
| grid columns | 373px 373px 373px | 373px 373px 373px |
| inner height | 580.8 | **675.3** |
| slack above / below inner | 159.1 / 160.1 | **111.9 / 112.9** |
| headline → row gap | 32 | 32 (unchanged) |
| band under the last copy line | 53.1 / 33 / 53.1 | 53.1 / 33 / 53.1 |
| overflow at 1440 × 900 | none | **none** |

**Looked at the screenshots.** s10: the three drawings now carry the cell —
the gearbox's `30T / 12T / 14T / 36T` callouts and the `i = 6.43 : 1` scale bar
are legible where before they were specks, the books' page edges separate, the
brain's gyri read as lines rather than a smudge. Nothing is clipped at any
edge; the red accents (the pitch circle, the top book's spine, the brain's
artery) survive `mix-blend-mode:multiply` as before. The `01 / 02 / 03`
numbers sit level across the three columns, the titles and copy are in the
same type at the same rhythm, and there is still a comfortable band under the
copy before the cell's bottom rule. The rule box closes on the third cell.
s4: the workers at the conveyor, unchanged. s6: the catalogue on its stand,
pixel-identical.

## RULING-SHAPED QUESTIONS

1. **How big is big?** The drawings now reach 87.9% of the cell width — the
   top of the band the brief asked for. Going further means eating the cell's
   `var(--s2)` side padding, which is also what holds the copy off the rules.
   Is 88% the size, or should the picture run rule-to-rule?
2. **The brain is squarer than the other two** (1474 × 1368 against 900 × 630
   and 1200 × 840), so at a shared box height it reaches 66% of its cell where
   the others reach 88%. Equal box height keeps the three `01 / 02 / 03`
   baselines level. Equal *drawn width* instead would make the brain
   ~95 px taller than its neighbours and break that line. Which matters more —
   level baselines, or three pictures of the same apparent size?
3. **The white space that is left.** 112 px above and below the block, and the
   ~53 px band under the copy inside cells 01 and 03 (cell 02's two-line copy
   sets the row height). Is that the breathing room the slide wants, or is
   there another pass here — a taller row, or copy that fills the cell?
4. **Print was deliberately frozen** at the old 135 px box. The printed deck
   now shows the anatomy smaller than the screen does. Should print follow the
   screen, and if so at what height inside its fixed 1280 × 720 slide?
5. **The bake resolution was not raised** — it did not need to be at this
   size (measured, all three have 2× headroom). If the pictures grow again
   past ~450 px of box height, `gbPrint` at 900 × 630 runs out first. Worth
   raising `#gbHost` now against a future pass, or leave it until it bites?
6. Nothing on any other slide moved, per the brief. The same `.pic` treatment
   exists only on 10, so this change is contained — but slide 10 is now
   visibly the heaviest card in the deck. Does that sit right in the run?

Nothing above is settled and Dave has accepted none of it; the only thing he
said is quoted at the top.

## COUNTS:

- slides (`section.slide` in the DOM): **12** (before: 12)
- `class="slide"` occurrences in the file: **13**; `<section` occurrences:
  **13** (both unchanged)
- `<section>` in the DOM: **12**; pagenum blocks: **12**; slide 10 still reads
  `10 / 12`
- page errors (Chromium `pageerror` + console `error`, load + scroll through
  s4/s6/s10, 1440 × 900, DPR 2): **0** (before the edit: **0**)
- anatomy cells on 10: **3/3 filled** — an1←gbPrint 197,890 B (900 × 630),
  an2←bkPrint 427,198 B (1200 × 840), an3←brPrint 353,558 B (1474 × 1368)
  (all unchanged — no re-bake)
- resolution headroom at DPR 2: an1 needs 656 × 459 of 900 × 630 ✓ ·
  an2 needs 656 × 459 of 1200 × 840 ✓ · an3 needs 495 × 459 of 1474 × 1368 ✓
- `#s10 .grid4` computed columns: **373px 373px 373px** (unchanged)
- image box: **340 × 135 → 340 × 229.5** CSS px
- cell height: **329.7 → 424.2** CSS px
- slide 10 inner: **580.8 → 675.3** px inside a 900 px slide; overflow **false**,
  `scrollHeight` overflow **false**
- substitutions: **2/2 ok**; file **7642 → 7649 lines** (+7)
- screenshots: **6** — `s10-before.png` / `s10.png`, `s4-before.png` /
  `s4.png`, `s6-before.png` / `s6.png` in `notes/_lanes/291/P3/`.
  `s6-before.png` and `s6.png` are **byte-identical** (350,554 B each).
- iterations: **1** (the first geometry measured into the target band)

## REPLAY-THESE:

    # preserve, then build (idempotent from the preserved copy)
    cd /sessions/.../mnt/UX-design
    cp notes/_lanes/291/P3/v12-before-p3.html \
       notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html
    python3 notes/_lanes/291/P3/build_p3.py        # 2 ok lines, 7642 -> 7649

    # counts
    grep -c 'class="slide' notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html   # 13
    grep -c '<section'     notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html   # 13
    grep -n 'grid5 .pic'   notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html   # 2 hits

    # render + measure (Chromium in the sandbox)
    export LD_LIBRARY_PATH=$HOME/.local/lib
    python3 notes/_lanes/291/P3/shoot.py           # 0 page errors; s4/s6/s10.png
    python3 notes/_lanes/291/P3/shoot.py -before   # same, with a -before suffix

    # in the page, by hand
    getComputedStyle(document.getElementById('an1')).height       // '229.5px'
    (i=>[i.naturalWidth,i.naturalHeight])(document.getElementById('an1'))
    document.querySelector('#s10 .grid5>div').getBoundingClientRect().height

Files changed: `notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` (in place, 2
CSS declarations). Files added: `notes/_lanes/291/P3/v12-before-p3.html` (the
preserved pre-edit copy), `notes/_lanes/291/P3/build_p3.py`,
`notes/_lanes/291/P3/shoot.py`, six screenshots in the same directory, and
this report. Nothing committed; no `rm`, no `git checkout --`; no strays.
