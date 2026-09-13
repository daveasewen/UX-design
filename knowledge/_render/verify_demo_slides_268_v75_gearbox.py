#!/usr/bin/env python3
"""Drive section 3 of notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html at 1920x1080.

v7.5 is the ART-DIRECTION pass on v7.4's gearbox. The engineering was
right and the picture was a tangle, so this driver gates the PICTURE as
well as the mechanism:

  G0  THE PICTURE READS. The three shafts are COPLANAR and in a row
      (input left, intermediate centre, output right); the resting view
      opens the gear faces (|cos p cos y| >= 0.7, so a gear is a disc and
      not an edge-on comb); and the ink is a DRAWING, not a wireframe —
      solid in [600, 1200], dashed in [4, 120].
  G1  THE TRAIN IS REAL. 12/30/14/36, i = 6.43:1, and each centre
      distance EQUALS the sum of the two pitch radii — the mesh is
      geometry, not a look.
  G2  NO TOOTH PASSES THROUGH ANOTHER. Both tooth polygons of a mesh are
      convex trapezoids in the SAME plane, so window.gbMesh() clips them
      exactly, at 12 phases, at both mesh points. Gate: worst overlap
      < 2% of one tooth's area.
  G3  HIDDEN-LINE RENDERING IS ACTUALLY THERE. A known back-face edge of
      the output gear must read DASHED (#BDBDBD, gaps in the pixels) and
      a known front-face edge SOLID (#111, continuous) — asserted by
      sampling the screenshot along the two segments the page hands back.
  G4  fps >= 55 WITH THE MOUSE MOVING.
  G5  THE DRAWING SITS INSIDE THE CARD with >= 6% margin on every side.
  G6  THE ORBIT OBEYS ITS RANGE and does NOT return to centre on idle.
  G7  THE CARD IS OPAQUE — the fly-through canvas does not read through.
  G8  THE LOOP PAUSES when the section is out of view; reduced motion is
      a still frame at the resting view; the print <img> is baked.
  Carried: zero overflow on all 11 sections, PDF 11 pages.

Usage:
  source knowledge/_render/seat_env.sh && \
    python3 knowledge/_render/verify_demo_slides_268_v75_gearbox.py
"""
import glob
import json
import math
import os
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
DECK = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-12-v7.html"
OUT = REPO / "notes" / "_subreports" / "slides-268-v7"
OUT.mkdir(parents=True, exist_ok=True)
VH = 1080
VW = 1920
S3 = 2          # zero-based index of section 3


def chromium():
    shell = os.environ.get("RENDER_SHELL")
    if shell and os.path.exists(shell):
        return shell
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
    for pat in ("chromium*/chrome-linux/*/chrome", "chromium*/chrome-linux/chrome",
                "chromium_headless_shell-*/chrome-linux/headless_shell"):
        hits = sorted(glob.glob(os.path.join(root, pat)))
        if hits:
            return hits[-1]
    return None


def sample_edge(img, seg, name):
    """Walk the segment, inset 12% each end, and read the darkest pixel in a
    3px perpendicular window at each step. Returns the run profile."""
    x0, y0, x1, y1 = seg["x0"], seg["y0"], seg["x1"], seg["y1"]
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    n = max(8, int(L))
    lums, cols = [], []
    for i in range(n):
        t = 0.12 + 0.76 * (i / (n - 1))
        cx, cy = x0 + dx * t, y0 + dy * t
        best, bestc = 255.0, (255, 255, 255)
        for k in (-1.2, -0.6, 0.0, 0.6, 1.2):
            sx, sy = int(round(cx + px * k)), int(round(cy + py * k))
            if 0 <= sx < img.width and 0 <= sy < img.height:
                r, g, b = img.getpixel((sx, sy))[:3]
                L2 = 0.299 * r + 0.587 * g + 0.114 * b
                if L2 < best:
                    best, bestc = L2, (r, g, b)
        lums.append(best)
        cols.append(bestc)
    ink = [l < 235 for l in lums]
    dark = [l < 120 for l in lums]
    runs, cur = [], 0
    for v in ink:
        if v:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    gaps, cur = [], 0
    for v in ink:
        if not v:
            cur += 1
        elif cur:
            gaps.append(cur)
            cur = 0
    if cur:
        gaps.append(cur)
    inked = [c for c, v in zip(cols, ink) if v]
    mean_ink = [round(sum(c[j] for c in inked) / len(inked), 1) for j in range(3)] if inked else None
    return {"name": name, "samples": n, "len": round(L, 1),
            "ink_fraction": round(sum(ink) / n, 3),
            "dark_fraction": round(sum(dark) / n, 3),
            "gap_count": len(gaps), "runs": len(runs),
            "mean_ink_rgb": mean_ink}


def main():
    shell = chromium()
    if not shell:
        print("FAIL: no chromium executable found")
        return 2
    report = {"deck": str(DECK.relative_to(REPO)), "chromium": shell, "console": []}
    fails = []

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=shell,
                               args=["--no-sandbox", "--font-render-hinting=none"])
        pg = br.new_page(viewport={"width": VW, "height": VH}, device_scale_factor=1)
        pg.on("console", lambda m: report["console"].append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: report["console"].append(f"pageerror: {e}"))
        pg.goto(DECK.as_uri())
        pg.wait_for_timeout(1600)
        pg.evaluate("(i)=>window.deckGo(i)", S3)
        pg.wait_for_timeout(1200)

        # ---- G1 · the train ------------------------------------------------
        st = pg.evaluate("()=>window.gbStats()")
        report["stats"] = st
        if [st["teeth"][k] for k in "ABCD"] != [12, 30, 14, 36]:
            fails.append(f"tooth counts {st['teeth']} != 12/30/14/36")
        want = (30 / 12) * (36 / 14)
        if abs(st["ratio"] - want) > 1e-3:
            fails.append(f"ratio {st['ratio']} != {want:.4f}")
        if abs(st["centre_distance_1"] - st["pitch_sum_1"]) > 1e-2:
            fails.append(f"stage 1 centre distance {st['centre_distance_1']} != "
                         f"pitch sum {st['pitch_sum_1']}")
        if abs(st["centre_distance_2"] - st["pitch_sum_2"]) > 1e-2:
            fails.append(f"stage 2 centre distance {st['centre_distance_2']} != "
                         f"pitch sum {st['pitch_sum_2']}")
        # ---- G0 · the picture ------------------------------------------------
        if not st["shafts_coplanar"]:
            fails.append(f"the three shafts are not coplanar: {st['shaft_row_a']}")
        row = st["shaft_row_a"]
        if not (row[0] < row[1] < row[2]):
            fails.append(f"the shafts are not in a row left->right: {row}")
        if st["solid_segments"] < 600 or st["solid_segments"] > 1200:
            fails.append(f"{st['solid_segments']} solid segments — want 600..1200")
        if st["hidden_segments"] < 4 or st["hidden_segments"] > 120:
            fails.append(f"{st['hidden_segments']} dashed segments — want 4..120 "
                         "(v7.4's 572 is the wireframe look v7.5 cut)")

        # ---- G2 · interpenetration ------------------------------------------
        mesh = pg.evaluate("()=>window.gbMesh(12)")
        report["mesh"] = mesh
        for k in ("stage1", "stage2"):
            if mesh[k]["ratio"] > 0.02:
                fails.append(f"{k}: teeth interpenetrate, overlap "
                             f"{mesh[k]['ratio']*100:.2f}% of a tooth at {mesh[k]['at']}")

        # ---- G4 · fps with the mouse moving ---------------------------------
        pg.evaluate("()=>{window.__f=0;const t=n=>{window.__f++;requestAnimationFrame(t);};"
                    "requestAnimationFrame(t);window.__t0=performance.now();}")
        for i in range(40):
            x = 700 + int(500 * math.sin(i / 4.0))
            y = 420 + int(200 * math.cos(i / 3.0))
            pg.mouse.move(x, y)
            pg.wait_for_timeout(25)
        fps = pg.evaluate("()=>window.__f/((performance.now()-window.__t0)/1000)")
        report["fps_mouse_moving"] = round(fps, 1)
        report["view_after_sweep"] = pg.evaluate("()=>window.gbView()")
        if fps < 55:
            fails.append(f"fps with the mouse moving {fps:.1f} < 55")

        # ---- G6 · the orbit range, and no return to centre -------------------
        # tau = 1.0 s critically damped: (1+wt)e^-wt, so 6.5 s is 1.2%
        # of the step still to run. Anything shorter reads as a shortfall
        # that is only the spring still arriving.
        pg.mouse.move(4, 540)
        pg.wait_for_timeout(6500)
        far_left = pg.evaluate("()=>window.gbView()")
        pg.screenshot(path=str(OUT / "gearbox-mouse-far-left.png"))
        pg.wait_for_timeout(3000)
        idle = pg.evaluate("()=>window.gbView()")
        report["view_far_left"] = far_left
        report["view_after_3s_idle"] = idle
        want_l = -far_left["yaw_range_deg"] * abs(far_left["mouse"][0]) * 0.96
        if far_left["yaw_off_deg"] > want_l:
            fails.append(f"mouse hard left only reached yaw offset "
                         f"{far_left['yaw_off_deg']} deg, want <= {want_l:.2f}")
        if abs(idle["yaw_off_deg"] - far_left["yaw_off_deg"]) > 0.6:
            fails.append("the view drifted back toward centre on idle "
                         f"({far_left['yaw_off_deg']} -> {idle['yaw_off_deg']}) — "
                         "Dave ruled that out in section 1")

        pg.mouse.move(VW - 4, 4)
        pg.wait_for_timeout(6500)
        tr = pg.evaluate("()=>window.gbView()")
        report["view_top_right"] = tr
        pg.screenshot(path=str(OUT / "gearbox-mouse-top-right.png"))
        want_y = tr["yaw_range_deg"] * abs(tr["mouse"][0]) * 0.96
        want_p = tr["pitch_range_deg"] * abs(tr["mouse"][1]) * 0.96
        if tr["yaw_off_deg"] < want_y or tr["pitch_off_deg"] < want_p:
            fails.append(f"mouse top-right reached yaw {tr['yaw_off_deg']} / pitch "
                         f"{tr['pitch_off_deg']}, want >= {want_y:.2f} / {want_p:.2f}")

        # ---- rest + the time series -----------------------------------------
        pg.evaluate("()=>{window.gbStop();window.gbStill();}")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / "gearbox-rest.png"))
        report["view_rest"] = pg.evaluate("()=>window.gbView()")

        # ---- G0b · the resting view opens the faces --------------------------
        if report["view_rest"]["face_opening"] < 0.70:
            fails.append(f"the resting view foreshortens the gear faces to "
                         f"{report['view_rest']['face_opening']} — a gear must read "
                         "as a disc, not an edge-on comb")

        # ---- G5 · the bbox inside the card ----------------------------------
        bb = pg.evaluate("()=>window.gbBBox()")
        sec = pg.evaluate("()=>{const r=document.getElementById('s3').getBoundingClientRect();"
                          "return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,"
                          "w:r.width,h:r.height};}")
        report["ink_bbox"] = bb
        report["section_rect"] = sec
        mx, my = sec["w"] * 0.06, sec["h"] * 0.06
        margins = {"left": bb["left"] - sec["left"], "right": sec["right"] - bb["right"],
                   "top": bb["top"] - sec["top"], "bottom": sec["bottom"] - bb["bottom"]}
        report["ink_margins_px"] = {k: round(v, 1) for k, v in margins.items()}
        report["margin_gate_px"] = {"x": round(mx, 1), "y": round(my, 1)}
        for k, v in margins.items():
            gate = mx if k in ("left", "right") else my
            if v < gate:
                fails.append(f"drawing bbox margin {k} {v:.1f}px < 6% ({gate:.1f}px)")

        # ---- G3 · hidden-line spot check -------------------------------------
        probes = pg.evaluate("()=>window.gbEdgeProbe()")
        report["edge_probe"] = probes
        img = Image.open(OUT / "gearbox-rest.png").convert("RGB")
        edge_read = {}
        for k in ("solid", "hidden"):
            if not probes.get(k) or probes[k]["len"] < 15:
                fails.append(f"no {k} probe edge long enough to sample at rest: "
                             f"{probes.get(k)}")
                continue
            edge_read[k] = sample_edge(img, probes[k], k)
        # v7.4 audited the output gear's two faces (180 solid / 180 dashed).
        # v7.5 draws the away face as an OUTLINE, so that audit no longer
        # describes the drawing; the edge counts above carry the claim.
        report["edge_counts"] = probes.get("counts")
        report["edge_readings"] = edge_read
        sr, hr = edge_read.get("solid"), edge_read.get("hidden")
        if sr:
            if sr["ink_fraction"] < 0.95:
                fails.append(f"the visible edge is not continuous: {sr}")
            if sr["dark_fraction"] < 0.8 or sr["mean_ink_rgb"][0] > 130:
                fails.append(f"the visible edge is not the #111 hairline: {sr}")
        if hr:
            if hr["gap_count"] < 2:
                fails.append(f"the hidden edge has no dashes ({hr['gap_count']} gaps): {hr}")
            if hr["ink_fraction"] > 0.92:
                fails.append(f"the hidden edge reads continuous: {hr}")
            if hr["mean_ink_rgb"] and not (150 <= hr["mean_ink_rgb"][0] <= 215):
                fails.append(f"the hidden edge is not the #BDBDBD hidden-line grey: {hr}")
            if hr["dark_fraction"] > 0.2:
                fails.append(f"the hidden edge reads as black ink, not hidden line: {hr}")

        # ---- the time series -------------------------------------------------
        for t in (0, 5, 10):
            pg.evaluate("(t)=>{window.gbStill();window.gbSetTime(t);}", t)
            pg.wait_for_timeout(160)
            pg.screenshot(path=str(OUT / f"gearbox-t{t}s.png"))
        report["mesh_at_t10"] = pg.evaluate("()=>window.gbMesh(6)")

        # ---- G7 · the card is opaque -----------------------------------------
        pg.evaluate("()=>window.deckGo(2)")
        pg.wait_for_timeout(500)
        opaque = pg.evaluate("""()=>{
          const s = document.getElementById('s3'), cs = getComputedStyle(s);
          const cv = document.getElementById('gb');
          return {bg: cs.backgroundColor, opacity: cs.opacity,
                  kg_running: window.kgRunning(), gb_running: window.gbRunning(),
                  canvas_w: cv.width, canvas_h: cv.height};
        }""")
        report["opacity"] = opaque
        if opaque["bg"] != "rgb(255, 255, 255)":
            fails.append(f"section 3 ground is {opaque['bg']}, want white")
        if opaque["kg_running"]:
            fails.append("the fly-through is still running under section 3")
        px = Image.open(OUT / "gearbox-rest.png").convert("RGB")
        corner = px.getpixel((VW - 30, VH - 200))
        report["card_corner_rgb"] = corner
        if min(corner) < 250:
            fails.append(f"section 3's ground is not white at the corner: {corner}")

        # ---- G8 · pause out of view, reduced motion, print --------------------
        pg.evaluate("()=>window.deckGo(6)")
        pg.wait_for_timeout(800)
        report["gb_running_off_section"] = pg.evaluate("()=>window.gbRunning()")
        if report["gb_running_off_section"]:
            fails.append("the gearbox still turns with section 3 out of view")
        pg.evaluate("()=>window.deckGo(2)")
        pg.wait_for_timeout(700)
        report["gb_running_back_in_view"] = pg.evaluate("()=>window.gbRunning()")
        if not report["gb_running_back_in_view"]:
            fails.append("the gearbox does not restart when section 3 comes back")

        pg.evaluate("()=>window.gbSnap()")
        pg.wait_for_timeout(700)
        report["gb_print_src_len"] = pg.evaluate(
            "()=>document.getElementById('gbPrint').src.length")
        if report["gb_print_src_len"] < 5000:
            fails.append("section 3's print snapshot is empty")

        # ---- carried: overflow on all 11, PDF 11 pages ------------------------
        n = pg.evaluate("()=>document.querySelectorAll('.slide').length")
        report["slide_count"] = n
        over = []
        for i in range(n):
            pg.evaluate("(i)=>window.deckGo(i)", i)
            pg.wait_for_timeout(420)
            m = pg.evaluate("""(i)=>{const s=document.querySelectorAll('.slide')[i];
              const r=s.getBoundingClientRect();const esc=[];
              s.querySelectorAll('*').forEach(el=>{const b=el.getBoundingClientRect();
                if(b.width===0&&b.height===0)return;
                if(b.bottom>r.bottom+1||b.right>r.right+1||b.top<r.top-1||b.left<r.left-1)
                  esc.push(String(el.className||el.tagName).slice(0,40));});
              return {id:s.id,sh:s.scrollHeight,ch:s.clientHeight,
                      sw:s.scrollWidth,cw:s.clientWidth,esc:esc};}""", i)
            over.append(m)
            if m["sh"] > m["ch"] + 1 or m["sw"] > m["cw"] + 1:
                fails.append(f"section {i+1} ({m['id']}): overflow {m}")
            if m["esc"]:
                fails.append(f"section {i+1} ({m['id']}): {len(m['esc'])} element(s) escape")
        report["sections"] = over

        pg2 = br.new_page(viewport={"width": VW, "height": VH},
                          device_scale_factor=1, reduced_motion="reduce")
        pg2.goto(DECK.as_uri())
        pg2.wait_for_timeout(1400)
        pg2.evaluate("(i)=>window.deckGo(i)", S3)
        pg2.wait_for_timeout(900)
        rm = {"running": pg2.evaluate("()=>window.gbRunning()"),
              "view": pg2.evaluate("()=>window.gbView()"),
              "stats": pg2.evaluate("()=>window.gbStats()")}
        report["reduced_motion"] = rm
        if rm["running"]:
            fails.append("prefers-reduced-motion: the gearbox is still turning")
        if abs(rm["view"]["yaw_off_deg"]) > 0.01 or abs(rm["view"]["pitch_off_deg"]) > 0.01:
            fails.append(f"prefers-reduced-motion: not the resting view — {rm['view']}")
        if rm["stats"]["solid_segments"] < 600:
            fails.append("prefers-reduced-motion: the still frame is empty")
        pg2.screenshot(path=str(OUT / "gearbox-reduced-motion.png"))
        pg2.close()

        pdf = OUT / "deck-v75.pdf"
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(500)
        pg.pdf(path=str(pdf), landscape=True, format="A4",
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
               print_background=True)
        report["pdf_bytes"] = pdf.stat().st_size
        raw = pdf.read_bytes()
        pages = raw.count(b"/Type /Page\n") + raw.count(b"/Type/Page/") + raw.count(b"/Type /Page/")
        report["pdf_page_objects"] = pages
        if pages != 11:
            fails.append(f"PDF has {pages} page objects, want 11")
        br.close()

    errs = [c for c in report["console"] if c.startswith(("error", "pageerror"))]
    if errs:
        fails.append(f"console errors: {errs[:3]}")
    report["fails"] = fails
    (OUT / "verify-gearbox.json").write_text(json.dumps(report, indent=2))
    keys = ("stats", "mesh", "fps_mouse_moving", "view_rest", "view_far_left",
            "view_after_3s_idle", "view_top_right", "ink_margins_px", "margin_gate_px",
            "edge_readings", "edge_counts", "opacity", "card_corner_rgb", "gb_running_off_section",
            "gb_running_back_in_view", "gb_print_src_len", "reduced_motion",
            "pdf_page_objects", "console", "fails")
    print(json.dumps({k: report.get(k) for k in keys}, indent=2, default=str))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
