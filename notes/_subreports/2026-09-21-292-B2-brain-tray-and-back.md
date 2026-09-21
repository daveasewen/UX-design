# #292 lane B2 — the brain's tray to the cogs' tray, and the back turned towards us

Dave, verbatim, on lane B's pass-seven render: *"The angles in this preview aren't right, the
cogs and books were fine as they were, as a guide lets angle the tray on the brain to be the
same as the cogs, with the back of the brain angled towards us."*

Read as three instructions, all three executed: **books and gearbox untouched**; the brain's
**tray** set to the gearbox's angle and proportion; the brain turned so its **back**
(occipital / cerebellum / stem, `a > 0`) is the end angled towards the eye.

## WHAT LANDED

- `notes/_lanes/289/illustration/brain.html` — **two constants moved, nothing else**.
  `YAW0 +35° → −35°` (sign flipped, magnitude kept) and `AOV 12 → 33`. `PIT0` was already
  `20°` and was not touched. No geometry, no trace, no ink, no `setView`, no fit.
  A PASS EIGHT comment block above each constant records the reasoning and the sign.
- `notes/_lanes/289/illustration/brain-v7.html` — pass seven preserved byte-for-byte before
  the edit. v1…v6 already existed; v7 is the next number.
- `notes/_lanes/289/illustration/brain-rest.png` — refreshed beside the html, 900×700 @2×.
- `notes/_lanes/292/B2/two-up.png` — **brain (shipped, −35/20) | gearbox (−35/20)**, matched
  height, for the eye ruling.
- `notes/_lanes/292/B2/two-up-alt.png` — the alternate, **brain body at −50°, tray held at
  −35°** (+15° further round onto the back), gearbox beside it at the same size.
- `notes/_lanes/292/B2/brain-rest-alt-yaw-50.png`, `gearbox-rest.png` — the two halves as
  rendered.
- **The deck was NOT touched.** Its constants are reported at the end.

**One camera, not two.** The brief allowed splitting the tray's yaw from the body's if the
brain's axis convention forced it. It does not, at the shipped angle: `a` is the brain's
front-back axis, so the *same* `−35°` that makes the tray the gearbox's tray is also the one
that swings the back towards the eye. Nothing was mirrored and no per-body view matrix was
introduced. The alternate **does** need the split (the body at −50, the tray at −35) — that
is why it is an alternate and not the pick; see the questions below.

## MEASURED (constants before/after, gearbox's beside)

The brain and the gearbox share one camera implementation: `setView(yaw, pit)` and the
projection `sx = m00·a + m02·u`, `sy = m10·a + m11·b + m12·u` are character-for-character
identical in both. So the tray's screen angle is fixed entirely by `YAW0`/`PIT0`, and its
screen proportion entirely by the box extents.

| | **brain (pass 7, was)** | **brain (pass 8, now)** | **gearbox (deck `gb`, L1570)** |
|---|---|---|---|
| file | `289/illustration/brain.html` | same | `_DEMO-SLIDES-…-v12.html` L1570 |
| `YAW0` | **+35°** | **−35°** | **−35°** |
| `PIT0` | 20° | **20°** | **20°** |
| `YAW_R` / `PIT_R` / `TAU` | 25° / 12° / 1.0 | unchanged | 25° / 12° / 1.0 |
| projection | orthographic, no divide | ″ | ″ |
| eye at rest, `a` component | **−0.54** (front towards us) | **+0.54** (back towards us) | n/a |
| tray long axis | `a` | `a` | `a` |
| tray span in `a` | −162.6 … 161.4 = **324** | **−183.6 … 182.4 = 366** | −190 … 214 = **404** |
| tray span in `u` | ±78.2 = **156.4** | unchanged **156.4** | ±86 = **172** |
| **tray plan ratio** | 324 : 156.4 = **2.07 : 1** | 366 : 156.4 = **2.34 : 1** | 404 : 172 = **2.35 : 1** |
| tray overhang past the body in `a` | **12** each end | **33** each end | **64** past the shaft centres |
| tray thickness in `b` | 12 (`BBOT…BTOP`) | unchanged **12** | 14 (`−142…−128`) |
| tray construction | `box(u,a,b)` wireframe | ″ | `box(u,a,b)` wireframe — same idiom |
| controlling constant | `AOV = 12` | **`AOV = 33`** | `S1[0]−64 … S3[0]+64` |

**Why the sign was the whole complaint.** At `+35°` the tray's long edge runs upper-left to
lower-right; the gearbox's, the books' and the other five deck cards' run lower-left to
upper-right. Pass seven matched the yaw *magnitude* to save the traced lateral profile and
paid for it with a mirrored plate — which is exactly the thing Dave's eye caught. At `−35°`
the plate is the gearbox's plate, edge for edge.

**Why the same sign also answers "back angled towards us".** The eye direction is
`(−cos·pit·sin·yaw, sin·pit, cos·pit·cos·yaw)` in `(a, b, u)`. The trace puts the frontal
pole at `a = −150.6` and the occipital lobe / cerebellum at `a = +115`. At `+35°` the eye's
`a` component is **−0.54** — the front was angled towards us, which is what pass seven
shipped and what Dave rejected. At `−35°` it is **+0.54**: the back, 35° round from the
lateral, tray unmoved. The profile foreshortens; per the brief, that is the ask.

**`AOV 12 → 33` is the proportion half of the ask.** 33 is not an eye-pick: it is the value
that puts the brain's plate at `2.34 : 1` in plan against the gearbox's `2.35 : 1`. At 12 the
plate was a plank the brain stood on; the gearbox's is a plinth the train sits on.

**Rest poses rendered and judged:** +35 (pass seven, for reference), −20, −35, −50, −65, −90,
plus −35 at `AOV` 12 and 33, plus −50 and −20 with the tray split off at −35. Nine frames.
−65 and −90 are the brain square-on from behind — symmetric, the longitudinal fissure down
the centre, the profile gone entirely; both read as a specimen photograph rather than a
drawing and neither is in the deck's idiom.

## RULING-SHAPED QUESTIONS

1. **−35 or −50? −35 is the pick.** `two-up.png` is −35, `two-up-alt.png` is −50.
   −35 is the gearbox's literal constant, so the tray matches with **one** camera and the
   mouse orbit stays coherent. −50 turns the back further towards us and, as it happens,
   sits the body more squarely inside the plate with less of the plate's far edge crossing
   the cerebellum — but it needs the tray pinned at −35 while the body sits at −50, i.e. a
   second view matrix, and the orbit then has to carry the −15° offset through `yawOff` or
   the two shear apart under the mouse. **Dave: is −35 enough "angled towards us", or is the
   extra 15° worth the split?**
2. **The plate now crosses the body, and there is no hidden-line removal between them.**
   The tray is drawn as a plain wireframe; the brain does not occlude it. At `+35` the
   plate's edges passed behind the narrow brainstem and it did not show. At `−35` the near
   long edge cuts across the temporal lobe and the far one across the cerebellum, so the
   brain reads as hovering rather than resting. Geometrically it **is** resting — the lowest
   rim point is `b = −176.6` and the plate top is `b = −178.6` — but the eye does not know
   that. **Dave: fix by occluding the plate against the body (a real change to the ink
   pass), or leave it as the drawing-convention wireframe the gearbox also uses?**
3. **The silhouette solver speckles on the far rim at this angle.** Short detached dashes
   scatter along the occipital edge where the rim turns away and the facing test flips —
   visible at full size in `brain-rest.png`. This is the same mechanism as pass six's
   "doubled outline", reopened by the foreshortening. It is a solver question, not an angle
   question, and was left alone. **Dave: worth a lane?**
4. **Tray thickness is still 12 against the gearbox's 14.** Not asked for, not moved; at a
   27:1 length-to-thickness ratio the difference is under a pixel at card size.
5. **The deck is now two passes out of step with the drawing file** — see below.

## COUNTS:

- Files edited: **1** (`brain.html`). Constants changed **2** (`YAW0`, `AOV`), geometry
  changed **0**, `setView`/projection/fit changed **0**.
- Files created: **5** — `brain-v7.html`, `292/B2/two-up.png`, `292/B2/two-up-alt.png`,
  `292/B2/brain-rest-alt-yaw-50.png`, `292/B2/gearbox-rest.png`. Plus `brain-rest.png`
  refreshed in place.
- Candidate rest poses rendered and judged by eye: **9**.
- Deck IIFEs carrying their own `YAW0`/`PIT0`: **8**. Seven rest at `−35 / 20`. The brain, at
  L3012, still rests at `10 / 8` and its `AOV` at L2976 is still `12`.
- Books and gearbox files: **0 reads that changed anything, 0 edits**.
- Git: **not touched** (no add, no commit, no status-changing command).

## REPLAY-THESE:

```bash
cd /sessions/<seat>/mnt/UX-design
export TMPDIR=/dev/shm
export LD_LIBRARY_PATH=$PWD/outputs/syslibs/usr/lib/aarch64-linux-gnu
# once per box — the plain form dies on the TLS-intercepting proxy with
# UNABLE_TO_GET_ISSUER_CERT_LOCALLY, and no headless_shell ships on this seat:
NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium-headless-shell
python3 - <<'PY'
from playwright.sync_api import sync_playwright
import base64
R="<repo>"; ILL=R+"/notes/_lanes/289/illustration"; B2=R+"/notes/_lanes/292/B2"
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"])
    pg=br.new_page(viewport={"width":900,"height":700},device_scale_factor=2)
    pg.goto("file://%s/brain.html"%ILL,wait_until="load"); pg.wait_for_timeout(2800)
    pg.screenshot(path=ILL+"/brain-rest.png"); pg.close()
    # the gearbox lives ONLY in the deck and is drawn off-screen at x=-3000,
    # so an element screenshot captures the wrong slide — read the canvas instead.
    pg=br.new_page(viewport={"width":1440,"height":900},device_scale_factor=2)
    pg.goto("file://%s/notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html"%R,wait_until="load")
    pg.wait_for_timeout(5000)
    d=pg.evaluate("()=>{const c=document.getElementById('gb');return c&&c.toDataURL('image/png');}")
    open(B2+"/gearbox-rest.png","wb").write(base64.b64decode(d.split(",")[1]))
    br.close()
PY
```

Alternate rest poses need no file edit: `brain.html` exposes `window.brSet(yawOffDeg,
pitOffDeg)`, which parks the view and redraws. Offsets beyond `YAW_R = 25°` fall outside the
fit sweep and can clip. The `−50` alternate in `two-up-alt.png` was rendered from a scratch
copy of the file with two hooks patched in — a `__Y0` override on `YAW0` and a save/restore
of the view matrix around the `HOUSING.forEach` block so the tray keeps `−35` while the body
moves. That patch is **not** in the shipped file.

**Fonts were not set up** (`knowledge/_render/seat_env.sh` still fails `envdir absent` —
`outputs/_render-env-229` does not exist at this seat), so the labels in these PNGs are in a
fallback face. Irrelevant to an angle ruling; do not read type quality off them.

**THE DECK CARRIES ITS OWN COPY — NOT EDITED, AS BRIEFED.**
`notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` inlines the brain IIFE with its own
constants, still at pass six:

- **L3012** — `var YAW0 = 10*Math.PI/180, PIT0 = 8*Math.PI/180;`
- **L2976** — `var HALF = (2*WMAX+GMAX)*1.15, AOV = 12;`
- **L2983** — `var HOUSING = box(-HALF, HALF, AMIN-AOV+PADF, AMAX+AOV-PADF, BBOT, BTOP);`

The gearbox (L1570) and the books (L2351) are inlined there at `−35 / 20` and were not read
for anything but these numbers. If Dave rules pass eight in, the deck needs the **same two
numbers** at L3012 and L2976 — `10 → −35`, `8 → 20`, `12 → 33` — **by whoever owns the deck.**
