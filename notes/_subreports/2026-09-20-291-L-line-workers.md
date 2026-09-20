# 291-L · Two workers, one conveyor

Lane L, Apollo session #291, 2026-09-20.
Dave's ask, verbatim: "the line slide - 4. could I have two workers in overalls
in the place of the robots that are on slide 05. so two drawings one with
humans and one with robots"

## VERDICT

Built and rendered. `line-workers.html` is the humans; `line.html` is the
robots and is byte-for-byte untouched, so the pair can be shown as a pair. The
same card, camera, orbit spring, conveyor, base plate, ink rules, hidden-line
pipeline and probe surface; only the actors change. Two figures in overalls
stand at the belt at the robots' own along-belt stations — the near one holding
a part out over the line, the far one reaching down onto the red workpiece.
Nought page errors across three render passes. Three things in the drawing are
pose and proportion judgements rather than geometry, and they are questions for
Dave below; nothing here has been accepted by anyone.

## WHAT LANDED

**Files**

- `notes/_lanes/289/illustration/line-workers.html` — new, 44.7 KB.
- `notes/_lanes/289/illustration/line-workers-rest.png` — 680×500 @2×.
- `notes/_lanes/289/illustration/line-workers-orbit.png` — 680×500 @2×.
- `notes/_lanes/289/illustration/line.html` — NOT touched (mtime still 15:08,
  and `git status` shows it unmodified).

**Carried over from line.html unchanged**

Projection and camera (rest yaw 35 / pitch 20, mouse ±25 yaw and ±12 pitch,
critically damped tau = 1.0 s, stays where the mouse left it); the conveyor
(bed, four legs, two end rollers, creeping painted centre dashes, heading
PHI = 12°); the base plate; the fit sweep; the back-face test, the white-fill
painter's pass and the three-class 3D ray classifier; `#111` hairline ink,
`#BDBDBD` dashed for a line inside its own solid, `#9B9B9B` dash-dot for the
same line in the open, one red `#DA1A00`; the 13 s idle and the
prefers-reduced-motion suppression; the probe names.

**Changed vs line.html**

- `makeArm` → `makeWorker(Fb, pose, tag, o0, opt)`. Same contract: placement
  frame with local +x facing the belt, a pose, a tag, a first ordinal; returns
  primitives, three drawn axes, a tip. Two placements, two poses, one drawing.
- The figure is only boxes and N-gon prisms: boots, legs, torso, neck, head,
  and per arm a shoulder ball, upper arm, elbow ball, forearm and hand. No new
  primitive kind, no faces, no shading, no colour.
- Overalls are edge lines, not fill — `deco` polylines seated on named torso
  faces and drawn only when that face is visible: bib and fly seam on the
  front, two strap runs over the top, crossed straps on the back. The figure
  seen from behind reads as overalls too.
- Standoff moved in: `WK_D = 118` against the arms' `ARM_D = 250`, because
  shoulder-to-fingertip here is ~200 units and a person left at the robot's
  station would be miming. Along-belt stations `ARM_SA = -200` and
  `ARM_SB = 66` are the robots' own, so the pair keeps its spacing.
- Poses solved, not drawn: `reachArm(fx, fz)` is the two-link closed form in
  the figure's sagittal plane, taking the NEGATIVE elbow root (elbow behind,
  upper arm hanging, forearm forward). The positive root put the elbow above
  the shoulder and read as a salute.
- The red part's station is read off the solved hand, projected onto the belt
  axis, rather than from a written-down offset.
- The housing-axle dashed pair is gone (a person has no axle in a casting);
  `G.axles` is empty and the block no-ops. The `#BDBDBD` dashed language is
  carried by the standing centre line and the shoulder axis inside the torso
  and the elbow axis inside the elbow.
- **Both of line.html's painter's re-seats are gone, and `reseat()` with
  them.** Plain centroid depth, no special case anywhere. Reasoning is in the
  file at `paintOrder`: re-seating permutes a group into the SLOTS the global
  sort handed it, and with people standing a body's width from the belt rather
  than an arm's reach those slots straddle the conveyor — v1 carried the near
  leg and near arm over the bed and the end roller, and pushed the bed behind
  worker B's legs, which it stands in front of.
- The two black parts moved downstream to s = 20 and 250. A box on the belt
  sorts correctly against the long bed only while `k·s + sp·Δz > 0`; at the
  binding orbit corner (yaw −60 / pitch 8) that reads s > −7. This is what
  buys the no-special-case painter's order.

**Constants** (model units ≈ 4 mm, unchanged from the arms' scale)

| | |
|---|---|
| figure height | 402 (≈ 1.61 m) |
| belt surface `TOP` | 183 (≈ 0.73 m) |
| standoff `WK_D` | 118 |
| stations along belt | A −200, B 66 |
| boots | 44 × 30 × 26, toe offset x = 6 |
| legs | r 20, z 26…214, at y = ±27 |
| torso | 52 × 104 × 126, z 206…332 |
| neck / head | r 13 to z 344 / r 30 to z 402 |
| shoulders | `SH_Y` 52, `SH_Z` 318, ball r 15 |
| arm | upper 92 (r 13), elbow ball r 14, forearm 88 (r 11), hand 24×18×24 |
| bib | y ±34, z 252…306; straps at y ±40 |
| held part | 44 × 86 × 44, at the FK of worker A's pose |
| workpieces | s = 20, 250 black; red at s = 118 (from B's hand) |
| poses | A both arms 155° / −76°; B hanging 174° / −14°, reaching 166.9° / −82.0° |
| idle | period 13 s, ±2.5° at B's reaching shoulder and elbow, belt creep 15 |

**Probes** all still answer: `lineStats()`, `lineView()`, `linePose()`,
`lineAxisRuns()`, `lineOrder()`, `lineSetMouse()`, `lineSetTime()`,
`lineStill()`, `lineStop()`, `lineStart()`. `linePose()` now reports both arms
per figure plus `red_station`, `stand_off` and `figure_height`; `lineView()`
reports `workerA_axis_depth` / `workerB_axis_depth`; `lineAxisRuns()` names
`A-STAND`, `A-SHOULDER`, `A-ELBOW`, `B-*`, `BELT`.

At rest: 45 primitives, 608 vertices, 197 faces drawn, 197 culled, 565 edges
inked, 19 free lines, scale 0.5695, draw box [24.8, 37.4, 575.2, 382.6] in the
600×420 card.

## RULING-SHAPED QUESTIONS

1. Is worker A's job the right one? He holds a part out in front of him at
   chest height over the belt, which was my reading of "holding/inspecting" —
   would you rather he had both hands down on the belt, or a hand on a part
   that is resting on it?
2. Is the held part the right size? At 44 × 86 × 44 it is a crate held two
   hands wide; v1 was thinner and read as a plank. Should it be smaller, or
   should it go altogether and leave his hands empty?
3. Does the figures' scale against the belt look right to you? They stand
   402 units — about 1.61 m at the arms' 4 mm — with the belt surface at
   0.73 m, so the line comes to just below the hip. Taller figures would
   dominate the card more; shorter ones would stoop.
4. Do the overalls read as overalls at 600 × 420, or do they need more — a
   waistband, knee seams, a cap — at the cost of line density?
5. Is a plain cylinder head acceptable in this idiom, next to the gearbox and
   the callipers? It is a lay-figure head, and I did not want to introduce a
   face or a hat into a drawing that has no features anywhere else.
6. Is the standoff change the right trade? The figures stand at 118 from the
   belt centre rather than the robots' 250, so the two drawings do not overlay
   exactly — the along-belt stations do match. Would you rather the figures
   sat at 250 and leaned in, or that the robots' scene moved?
7. Is losing the far half of the belt's furniture acceptable? The two black
   parts moved from s = −258 and −20 to s = 20 and 250 to make the painter's
   order come out honest without any special case. The far half of the belt is
   now bare behind worker A.
8. Should worker B reach with the arm on the camera side, as he now does? The
   robot scene's note argued for the far side; within a figure that put the
   whole shoulder and elbow behind his own chest and all that emerged was a bar
   through the bib.

## COUNTS:

- files written: 3 (1 HTML, 2 PNG)
- files modified: 0 — `line.html` untouched, deck untouched, nothing committed
- renders: 3 passes × 2 PNGs, plus 2 zoom crops per pass for inspection
  (crops written to the session outputs folder, not the repo)
- page errors: 0 (0 on every pass; `pageerror` and console-error both collected)
- iterations: 3
- strays moved to `_to_delete/291-strays/`: 0

## REPLAY-THESE:

```bash
# sandbox, once
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
pip install playwright --break-system-packages -q
python3 -m playwright install chromium-headless-shell
cd ~ && apt-get download libxdamage1 && dpkg-deb -x libxdamage1_*.deb ~/.local/xd
mkdir -p ~/.local/lib && cp ~/.local/xd/usr/lib/aarch64-linux-gnu/libXdamage.so.1* ~/.local/lib/

# every shell
export LD_LIBRARY_PATH=$HOME/.local/lib
ldd ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux-arm64/chrome-headless-shell | grep "not found"   # expect nothing

# the renders
cat > ~/work/shot.py <<'EOF'
import asyncio, json
from playwright.async_api import async_playwright
SRC = "/sessions/<session>/mnt/UX-design/notes/_lanes/289/illustration/line-workers.html"
OUT = "/sessions/<session>/mnt/UX-design/notes/_lanes/289/illustration/"
async def main():
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":680,"height":500}, device_scale_factor=2)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console:"+m.text) if m.type=="error" else None)
        await pg.goto("file://"+SRC)                      # never set_content
        await pg.wait_for_timeout(1200)
        await pg.evaluate("window.lineStop(); window.lineSetTime(0); window.lineStill(); window.lineSetTime(0);")
        await pg.wait_for_timeout(200)
        await pg.screenshot(path=OUT+"line-workers-rest.png")
        await pg.evaluate("window.lineStart();")
        await pg.mouse.move(150, 130)                     # off-centre
        await pg.wait_for_timeout(1600)                   # let the spring settle
        await pg.screenshot(path=OUT+"line-workers-orbit.png")
        print(json.dumps({"pageerrors":len(errs),
                          "stats":await pg.evaluate("[lineStats(), lineView(), linePose(), lineAxisRuns()]")}))
        await b.close()
asyncio.run(main())
EOF
python3 ~/work/shot.py
```
