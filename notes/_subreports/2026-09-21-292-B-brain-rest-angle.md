# #292 lane B — the brain's starting angle, against the books and the cogs

Dave, verbatim: *"can we have the starting angle of the the same as the books and the cogs."*
Read as: the brain card's REST view should sit with the other two drawing cards.

## WHAT LANDED

- `notes/_lanes/289/illustration/brain.html` — **two constants moved, nothing else**.
  `YAW0 10° → 35°`, `PIT0 8° → 20°`. No geometry, no trace, no plinth, no ink touched.
  A PASS SEVEN comment block above the constants records why, including the sign.
- `notes/_lanes/289/illustration/brain-v6.html` — pass six preserved byte-for-byte
  before the edit (v1…v5 already existed; v6 is the next number).
- `notes/_lanes/289/illustration/brain-rest.png` — refreshed beside the html, 900×700 @2×.
- `notes/_lanes/292/B/three-up.png` — **brain (new) | books | gearbox**, all three at
  rest, matched height, for the eye ruling.
- `notes/_lanes/292/B/books-rest.png`, `gearbox-rest.png` — the two references as rendered.
- `notes/_lanes/292/B/alt-brain-yaw-minus35.png`, `alt-brain-yaw-145.png`,
  `alt-four-up.png` — the two rejected candidates, so the ruling can be re-taken by eye.
  *(Housekeeping: the same three files also exist under their `_`-prefixed working names —
  `_alt-brain-145.png`, `_alt-brain-minus35.png`, `_four-up.png`, plus a stale `_trial-yaw.png`.
  The sandbox refused `rm` in this lane; they are duplicates/stale and can be deleted.)*
- **The deck was NOT touched** — see the last section.

Render recipe: `knowledge/_RUNBOOK-render-verify.md`'s Chromium/Playwright path. ⚠ At this
seat `outputs/_render-env-229` does **not** exist, so `knowledge/_render/seat_env.sh` fails
`envdir absent`, and **no `headless_shell` existed anywhere on the box** — lane D's `shoot.py`
recipe as written cannot launch here. It was made to run by
`NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium-headless-shell`
(the plain install dies on `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` — a TLS-intercepting proxy),
plus `LD_LIBRARY_PATH=outputs/syslibs/usr/lib/aarch64-linux-gnu`. Fonts were **not** set up
via `seat_env.sh`, so the labels in these PNGs are in a fallback face — irrelevant to an
angle ruling, but do not read type quality off them.

## MEASURED (constants before/after)

The three drawings share one camera implementation. `setView(yaw, pit)` is **character-for-
character identical** in all three files, and so is the projection:
`sx = m00*a + m02*u`, `sy = m10*a + m11*b + m12*u`, with the model axes in the same roles —
`a` the in-plane long axis, `u` the thin/lateral axis, `b` up. So the entire difference was
the two rest numbers.

| | **brain (was)** | **brain (now)** | **books** | **gearbox (deck `gb`)** |
|---|---|---|---|---|
| file | `289/illustration/brain.html` L405 | same, L425 | `289/illustration/books.html` L178 | `_DEMO-SLIDES-…-v12.html` L1570 |
| `YAW0` | **10°** | **35°** | **−35°** | **−35°** |
| `PIT0` | **8°** | **20°** | **20°** | **20°** |
| `YAW_R` (mouse range) | 25° | 25° | 25° | 25° |
| `PIT_R` | 12° | 12° | 12° | 12° |
| `TAU` (spring) | 1.0 | 1.0 | 1.0 | 1.0 |
| projection | orthographic, no perspective divide | ″ | ″ | ″ |
| `setView` matrix | identical | identical | identical | identical |
| plinth in `u` | `±HALF = ±(2·WMAX+GMAX)·1.15 = ±78.2` | unchanged | `±PU = ±(MAXD/2 + 54)` | `SH0…SH1` (shaft span) |
| plinth in `a` | rim extent `+AOV−PADF = +6` net **0 beyond the padded rim** | unchanged | `±PA = ±(MAXW/2 + 54)` | `S1[0]−64 … S3[0]+64` |
| plinth thickness in `b` | **12** | unchanged | **11** | **14** (`−142…−128`) |
| plinth construction | `box(u,a,b)` wireframe | ″ | `boxEdges(±PA, ±PU, …)` | `box(u,a,b)` wireframe — same idiom as the brain |

**What differed: `YAW0` and `PIT0`, and nothing else.** `YAW_R = 25` being the same literal
in brain and books is a red herring — that is the mouse-orbit *range*, not the rest pose.
Pass six's `8°` pitch was the bigger offender: it put the eye almost level with the plinth,
which is why the brain's plate read as a thin sliver while the books' and the gearbox's read
as three-quarter slabs.

**Why the yaw sign is flipped, not copied.** Yaw magnitude is matched at 35°. The sign is
not, because `a` is not the same feature in the two bodies: for the books `a` is the cover
**width** (yaw 0 = covers square on), for the brain `a` is the **front-back** axis
(yaw 0 = the traced lateral profile square on). Three candidates were rendered against the
books at rest (`alt-four-up.png`):

- **−35° / 20° (the literal copy)** — the brain turns toward end-on and tips nose-down;
  the traced profile is lost and the crown groove reopens into the doubled outline that
  pass six existed to close. Rejected. → `alt-brain-yaw-minus35.png`
- **145° / 20°** (= −35° seen from the other lateral side; gives a plinth whose edges are
  *exactly* the books'/gearbox's lines) — the brain again tips nose-down and mirrors.
  Rejected. → `alt-brain-yaw-145.png`
- **+35° / 20°** — plinth and body present the same three-quarter, the frontal pole still
  faces the way Dave's reference does, the profile and the cerebellar folia survive.
  **Shipped.** → `three-up.png`

## RULING-SHAPED QUESTIONS

1. **The plinth is mirrored, and that is the only thing left that is not identical.**
   At `+35°` the brain's plate is the **mirror image** of the books'/gearbox's plate:
   their `+a` runs right-and-**down** the screen, the brain's runs right-and-**up**. The
   eye can read that as "one of these is lit from the other side". The only ways to remove
   it are the two rejected candidates, both of which cost the brain's readable profile.
   **Dave: is a mirrored three-quarter "the same angle", or does the brain have to turn
   the same way as the cogs even at the cost of the traced profile?** `alt-four-up.png`
   shows all three options against the gearbox.
2. **Plinth proportion — camera only was done, deliberately.** The brain's plate has
   **zero net overhang** along `a` (`AOV 12 − PADF 6` = +6, which only undoes the padding
   already added to the rim), while the books' plate overhangs by **+54** model units and
   the gearbox's by **+64**. That is why the brain looks like it is standing on a plank and
   the other two on a plinth. It is a *proportion*, not an angle, so it was left alone.
   **Dave: fold the overhang in too?** One line, `var AOV = 12` → ~`54`.
3. **Plinth thickness** is already effectively matched (12 vs 11 vs 14) — no action asked.
4. **The deck is now out of step with the drawing file** — see below.

## COUNTS:

- Files edited: **1** (`brain.html`), constants changed **2**, geometry changed **0**.
- Files created: **8** (`brain-v6.html`, `brain-rest.png` refreshed, `three-up.png`,
  `books-rest.png`, `gearbox-rest.png`, 3 alt PNGs; plus 4 `_`-prefixed duplicates/stale
  that the sandbox would not let me delete).
- Candidate rest poses rendered and judged: **5** (10/8, 10/20, −35/20, +35/20, 145/20).
- Deck IIFEs carrying their own `YAW0/PIT0`: **8** (L1570 gearbox, L2351 books, L3012 brain,
  L4305, L5125, L5847, L6492, L7231). **7 of the 8 rest at −35 / 20. The brain, at L3012, is
  the only one that does not** — which is, in one grep, the whole of Dave's complaint.
- Git: **not touched** (no add, no commit).

## REPLAY-THESE:

```bash
cd /sessions/<seat>/mnt/UX-design
export TMPDIR=/dev/shm
export LD_LIBRARY_PATH=$PWD/outputs/syslibs/usr/lib/aarch64-linux-gnu
# once per box, only if no headless_shell exists (the plain form dies on the TLS proxy):
NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium-headless-shell
# rest PNGs at 900x700 @2x, then compose three-up.png at matched height
python3 - <<'PY'
from playwright.sync_api import sync_playwright
import base64
R="<repo>"; ILL=R+"/notes/_lanes/289/illustration"; B=R+"/notes/_lanes/292/B"
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"])
    for u,out in [("file://%s/brain.html"%ILL, ILL+"/brain-rest.png"),
                  ("file://%s/books.html"%ILL, B+"/books-rest.png")]:
        pg=br.new_page(viewport={"width":900,"height":700},device_scale_factor=2)
        pg.goto(u,wait_until="load"); pg.wait_for_timeout(2800)
        pg.screenshot(path=out); pg.close()
    # the gearbox lives ONLY in the deck and is drawn off-screen at x=-3000,
    # so an element screenshot captures the wrong slide — read the canvas instead.
    pg=br.new_page(viewport={"width":1440,"height":900},device_scale_factor=2)
    pg.goto("file://%s/notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html"%R,wait_until="load")
    pg.wait_for_timeout(5000)
    d=pg.evaluate("()=>{const c=document.getElementById('gb');return c&&c.toDataURL('image/png');}")
    open(B+"/gearbox-rest.png","wb").write(base64.b64decode(d.split(",")[1]))
    br.close()
PY
```

**THE DECK CARRIES ITS OWN COPY — NOT EDITED, AS BRIEFED.**
`notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` inlines the brain IIFE at **line 3012** with
its own `var YAW0 = 10*Math.PI/180, PIT0 = 8*Math.PI/180;` and pass six's comment above it,
i.e. the deck still shows the OLD rest angle. The gearbox (L1570) and the books (L2351) are
inlined there too, both at `−35 / 20`. If Dave rules the new brain angle in, the deck needs
the same two-number change at L3012 — **one line, by whoever owns the deck.**
