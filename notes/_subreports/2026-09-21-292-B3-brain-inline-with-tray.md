# #292 lane B3 — the brain back inline with its tray, at the alternate's angle

Dave, verbatim, on lane B2's pair: *"two up alt is better but we need to orientate the brain so
its inline with the tray as it was before, but this is the right angle."*

Read as: **the alternate's angle is accepted**; what is wrong is that the brain's long axis no
longer runs along the tray's long edge. Restore the alignment without moving the angle.

## WHAT LANDED

- `notes/_lanes/289/illustration/brain.html` — **one constant moved, nothing else.**
  `YAW0 −35° → −50°`. `PIT0`, `YAW_R`, `PIT_R`, `TAU`, `AOV`, `setView`, the projection, the
  fit, the trace, the ink: all untouched. A PASS NINE comment block above the constant records
  the measurement and the cost.
- `notes/_lanes/289/illustration/brain-v8.html` — pass eight preserved byte-for-byte before the
  edit. v1…v7 already existed; v8 is the next number.
- `notes/_lanes/289/illustration/brain-rest.png` — refreshed beside the html, 900×700 @2×.
- `notes/_lanes/292/B3/two-up.png` — **brain (shipped, −50/20) | gearbox (−35/20)**, matched
  height, for the eye ruling.
- `notes/_lanes/292/B3/top-check.png` — the **plan proof**, pitch 88, B2's alternate beside pass
  nine. Left: the body's footprint sits 15° skew inside the plate. Right: it sits square.
- `notes/_lanes/292/B3/alt-body-23-tray-35.png` — the **alternate for the ruling** (see Q1):
  tray held at the gearbox's −35, body rotated to −23.43 in the model.
- `notes/_lanes/292/B3/axis-overlay.png` — v7 / pass eight / B2's alternate / pass nine, each
  with the body's pole-to-pole axis (red) and the plate's long edge (blue) drawn over it.
- `notes/_lanes/292/B3/gearbox-rest.png` — the gearbox half as rendered.
- **The deck was NOT touched.** Its brain copy is separate and stale by design; reported below.

**The diagnosis, and why it is one constant.** `a` is *both* the brain's front-back axis *and*
the tray's long axis — the tray is `box(u, a, b)` over the same `a` the trace runs along. So
under **one** camera the two long axes are parallel by construction, at every yaw. B2's
alternate was not one camera: it drew the body at −50 while holding the tray at −35, which is a
**15° rotation of the body about `b` relative to the tray**. That relative rotation is the whole
of the defect, and it is the only thing the alternate introduced. The fix is to put it back to
zero **while leaving the body exactly where the alternate had it** — so the tray follows the
body to −50, rather than the body being dragged back to −35 (which is pass eight, the frame
Dave did not pick). The brain in `two-up.png` is pixel-identical to `two-up-alt.png`'s brain.

**The rotation was computed, not eyeballed.** Rendering `brain.html` with `YAW0` swept in 10°
steps and the tray split off showed the plate's screen angle depends only on the tray's yaw and
the body's pole line only on the body's yaw; the residual is minimised at zero relative yaw.
Confirmed by the plan render, where the footprint is square in the plate to within the line
width.

## MEASURED

Projection is orthographic and identical in the brain and the gearbox: `sx = cos(yaw)·a +
sin(yaw)·u`, `sy = sin(pit)sin(yaw)·a + cos(pit)·b − sin(pit)cos(yaw)·u`, drawn as `y = OY −
sy·SC`. Two angles follow in closed form.

- **plate long edge**, screen: `atan2(−sin(pit)·sin(yaw_tray), cos(yaw_tray))`
- **body long axis**, screen: pole to pole, frontal `a = −150.63` → occipital `a = +149.37`
  (`Δa = 299.97`, `Δb = −26.73`), i.e. `atan2(−(sin(pit)sin(yaw_body)·Δa + cos(pit)·Δb),
  cos(yaw_body)·Δa)`

| | body yaw | tray yaw | body axis | plate edge | **screen residual** | **plan split** | eye·a |
|---|---|---|---|---|---|---|---|
| pass six (`brain-v6`) | 10 (pit 8) | 10 | — | — | **5.1°** | 0° | −0.17 |
| pass seven (`brain-v7`) | +35 | +35 | −7.82° | −13.47° | **5.65°** | 0° | −0.54 |
| pass eight (`brain-v8`, B2 shipped) | −35 | −35 | +18.87° | +13.47° | **5.40°** | 0° | +0.54 |
| **B2's alternate** (`two-up-alt.png`) | **−50** | **−35** | +28.27° | +13.47° | **14.81°** | **15.0°** | +0.72 |
| **pass nine (shipped)** | **−50** | **−50** | +28.27° | +22.18° | **6.10°** | **0°** | +0.72 |
| alternate for the ruling (Q1) | −23.43 | −35 | +13.45° | +13.47° | **0.01°** | 11.6° | +0.37 |

- Every frame the eye has accepted sits at a **5–6° screen residual**; the frame Dave rejected
  sits at **14.8°**, and it is the only one with a non-zero plan split. Pass nine puts both back:
  **6.10° screen, 0° plan**, against pass seven's 5.65° / 0°.
- **`eye·a = +0.72`** — the back is turned *further* towards us than pass eight's +0.54, which is
  what the alternate bought and what Dave kept. The eye vector is
  `(−cos(pit)sin(yaw), sin(pit), cos(pit)cos(yaw))` in `(a, b, u)`.
- **Body foreshortening**, `sqrt(1 − (eye·a)²)`: pass seven 0.842, pass eight 0.842, pass nine
  **0.694**. The brain is 18% shorter on screen than at −35. It is the price of the extra
  back-turn and it is in the frame Dave picked.
- **Plate plan proportion is unchanged** — `366 : 156.4 = 2.34 : 1` against the gearbox's
  `404 : 172 = 2.35 : 1`. `AOV` stayed at 33. Only the yaw moved.
- **Plate screen angle** moved `+13.47° → +22.18°`; the gearbox's stays at `+13.47°`.
- Candidate poses rendered and judged: **51** — a 36-frame body-yaw sweep at 10° with the tray
  split off (silhouette PCA and tray-aligned bounding box measured on each), plus 15 full frames.
- Blob PCA of the body silhouette was tried as the alignment metric and **discarded**: at every
  useful yaw the brain's elongation is 1.0–1.3, so the principal axis is noise. The pole line
  against the plate edge is the metric in the table, and the plan render is the check on it.

## RULING-SHAPED QUESTIONS

1. **The plate is no longer the gearbox's literal −35, and that was Dave's own earlier ask**
   (*"lets angle the tray on the brain to be the same as the cogs"*, #292 B2). Pass nine keeps
   the plate's construction, proportion and idiom but turns it 15° further round with the body,
   because "inline" and "the alternate's body angle" cannot both hold with the plate pinned at
   −35 — the two are the same axis. The alternate that keeps the plate at −35 is
   `alt-body-23-tray-35.png`: tray at the gearbox's −35, body at −23.43, screen residual 0.01°,
   and the brain reads lengthwise along the plate the way pass six and seven did. Its costs are
   an **11.6° plan split** (the footprint sits skew in the plate, as B2's alternate did) and a
   **second view matrix** for the orbit. **Dave: plate follows the brain to −50 (shipped), or
   plate holds the cogs' −35 and the brain turns 11.6° in its own axes (alternate)?**
2. **The brain overhangs the plate's near-right edge at −50.** At the shorter on-screen length
   the body's silhouette runs past the plate's corner. Geometrically it still rests on the plate
   — the lowest rim point is `b = −176.6`, the plate top `b = −178.6` — but the far edge crosses
   the cerebellum and the near edge the temporal lobe, unchanged from pass eight. **Dave: widen
   `AOV` past 33 so the plate reads as catching the body, or leave the proportion matched to the
   gearbox's 2.35 : 1?**
3. **The silhouette solver still speckles on the far rim**, and slightly more at −50 than at −35
   — short detached dashes along the occipital edge where the facing test flips. Same mechanism
   as pass six's doubled outline, reopened by the foreshortening. Solver question, not an angle
   question; left alone. **Dave: worth a lane?** (carried from B2 Q3, unruled)
4. **Tray thickness is still 12 against the gearbox's 14.** Not asked for, not moved. (carried
   from B2 Q4, unruled)
5. **The deck is now three passes out of step with the drawing file** — see below.

## COUNTS:

- Files edited: **1** (`brain.html`). Constants changed **1** (`YAW0`). Geometry **0**,
  `setView` / projection / fit **0**, trace **0**, ink **0**. View matrices still **1**.
- Files created: **6** — `brain-v8.html`, `292/B3/two-up.png`, `292/B3/top-check.png`,
  `292/B3/alt-body-23-tray-35.png`, `292/B3/axis-overlay.png`, `292/B3/gearbox-rest.png`.
  Plus `brain-rest.png` refreshed in place.
- Candidate poses rendered and measured: **51**.
- Deck IIFEs carrying their own `YAW0`/`PIT0`: **8**. Seven rest at `−35 / 20`. The brain, at
  L3012, still rests at `10 / 8` and its `AOV` at L2976 is still `12`.
- Books and gearbox files: **0 edits** (the deck was read for the `gb` canvas only).
- Git: **not touched** (no add, no commit, no status-changing command).
- `_build_all.py`: **not run**. `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md`, `_state.json`,
  `_rulings.json`, the deck: **not edited**.

## REPLAY-THESE:

```bash
cd /sessions/<seat>/mnt/UX-design
export TMPDIR=/dev/shm
export LD_LIBRARY_PATH=$PWD/outputs/syslibs/usr/lib/aarch64-linux-gnu
# once per box — the plain form dies on the TLS-intercepting proxy with
# UNABLE_TO_GET_ISSUER_CERT_LOCALLY, and no headless_shell ships on this seat:
NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium-headless-shell
```

**Chromium cannot read `/dev/shm` on this seat** — `file:///dev/shm/...` returns
`ERR_FILE_NOT_FOUND` even though the file is there. Scratch HTML for a render has to live under
the repo mount. Bash calls are also independent here, so `/dev/shm` is empty again on the next
call: generate the scratch files and render them **in one call**.

```python
from playwright.sync_api import sync_playwright
import base64
R="<repo>"; ILL=R+"/notes/_lanes/289/illustration"; B3=R+"/notes/_lanes/292/B3"
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
    open(B3+"/gearbox-rest.png","wb").write(base64.b64decode(d.split(",")[1]))
    br.close()
```

**The two angles, in four lines** — no render needed to re-derive the table:

```python
import math
P=math.radians(20); DA=299.97; DB=-26.73          # pole to pole, frontal -150.63 -> occipital +149.37
tray = lambda Yt: math.degrees(math.atan2(-math.sin(P)*math.sin(math.radians(Yt)), math.cos(math.radians(Yt))))
pole = lambda Yb: math.degrees(math.atan2(-(math.sin(P)*math.sin(math.radians(Yb))*DA + math.cos(P)*DB),
                                          math.cos(math.radians(Yb))*DA))
# residual = abs(pole(body_yaw) - tray(tray_yaw));  plan split = abs(body_yaw - tray_yaw)
```

**The split-camera patch** (for the Q1 alternate, and for any future body/tray split) is a
save/restore of the view matrix around the `HOUSING.forEach` block in the collect pass, with
`yawOff`/`pitOff` added to *both* yaws so the mouse orbit stays rigid:

```js
var __sv=[m00,m02,m10,m11,m12,m20,m21,m22];
setView((-35)*Math.PI/180 + yawOff, PIT0 + pitOff);
HOUSING.forEach(...);                       // unchanged
m00=__sv[0];m02=__sv[1];m10=__sv[2];m11=__sv[3];m12=__sv[4];m20=__sv[5];m21=__sv[6];m22=__sv[7];
```

That patch is **not** in the shipped file — pass nine is one camera. Plan renders are the same
scratch copy with `PIT0` at 88. Alternate rest poses need no file edit at all:
`window.brSet(yawOffDeg, pitOffDeg)` parks the view and redraws; offsets beyond `YAW_R = 25°`
fall outside the fit sweep and can clip.

**Fonts were not set up** (`knowledge/_render/seat_env.sh` still fails `envdir absent` —
`outputs/_render-env-229` does not exist at this seat), so the labels in these PNGs are in a
fallback face. Irrelevant to an angle ruling; do not read type quality off them.

**THE DECK CARRIES ITS OWN COPY — NOT EDITED, AS BRIEFED.**
`notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` inlines the brain IIFE with its own constants,
still at pass six:

- **L3012** — `var YAW0 = 10*Math.PI/180, PIT0 = 8*Math.PI/180;`
- **L2976** — `var HALF = (2*WMAX+GMAX)*1.15, AOV = 12;`

If Dave rules pass nine in, the deck needs `10 → −50`, `8 → 20`, `12 → 33` at those two lines —
**by whoever owns the deck.** If he rules the Q1 alternate in instead, the deck needs `−35 / 20`
plus the split patch above, which is a structural change and not a constant swap.
