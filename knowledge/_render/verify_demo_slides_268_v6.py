#!/usr/bin/env python3
"""Drive notes/_DEMO-SLIDES-apollo-2026-09-12-v6.html at 1920x1080.

v6 is THE FLY-THROUGH. The Milky Way layer is gone; the graph is
un-folded into its three strata islands along x, and the camera flies a
spline from outside island 1 through all three centroids to beyond
island 3 in 60 s, nudged (never steered) by the mouse and self-centring
when the mouse stops.

Carried forward from v3-v5: font stack, snap, reveals, zero overflow on
all 11, the whole text block unobstructed, reduced motion, print, PDF.

New to v6:

  A  THE BOUND. Synthetic mousemoves to the four viewport corners while
     the fly-through runs; camera offset from the path sampled at 60
     phases and asserted against 0.90 x the local island radius (and
     against the 0.12-per-axis nudge ceiling).
  B  SELF-CENTRING. 600 ms after the last mousemove the offset targets
     zero; 2 s later the residual must be under 5% of the maximum.
  C  THREE PARTS IN SEQUENCE. At t = 10 / 30 / 50 s the island id of the
     nearest visible nodes must be 1, then 2, then 3, and the on-screen
     node-density centroid must be a real reading at each.
  D  60 fps WITH THE MOUSE MOVING.

Usage (same bash call):
  source knowledge/_render/seat_env.sh && \
    python3 knowledge/_render/verify_demo_slides_268_v6.py
"""
import glob
import io as _io
import json
import os
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
DECK = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-12-v6.html"
OUT = REPO / "notes" / "_subreports" / "slides-268-v6"
OUT.mkdir(parents=True, exist_ok=True)

EXPECT_STACK = '"Univers Next", "Helvetica Neue", Helvetica, Arial, sans-serif'


MEASURE = r"""
(idx) => {
  const s = document.querySelectorAll('.slide')[idx];
  const sr = s.getBoundingClientRect();
  const box = { l: sr.left, t: sr.top, r: sr.right, b: sr.bottom };
  const overflow = {
    scrollH: s.scrollHeight, clientH: s.clientHeight,
    scrollW: s.scrollWidth,  clientW: s.clientWidth
  };
  const escapes = [];
  s.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.bottom > box.b + 1 || r.right > box.r + 1 || r.top < box.t - 1 || r.left < box.l - 1) {
      escapes.push({ sel: String(el.className || el.tagName).slice(0, 60),
                     top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1),
                     left: +r.left.toFixed(1), right: +r.right.toFixed(1) });
    }
  });
  const DESC = /[gjpqy]/;
  const clipped = [];
  s.querySelectorAll('.label,.nlab,.ndesc,.n,.stamp,.draft,.switch,.count,.foot,.close-line,th,td,.lead,.body,.ask,.ix,h1,h2,h3')
   .forEach(el => {
    const txt = (el.textContent || '');
    if (!DESC.test(txt)) return;
    const st = getComputedStyle(el);
    const rng = document.createRange();
    rng.selectNodeContents(el);
    const rr = rng.getBoundingClientRect();
    const er = el.getBoundingClientRect();
    const hiddenY = (st.overflow === 'hidden' || st.overflowY === 'hidden');
    const trimmed = (st.textBoxEdge && st.textBoxEdge !== 'auto' && st.textBoxEdge !== 'leading')
                    || (st.textBoxTrim && st.textBoxTrim !== 'none');
    const clipPx = +(rr.bottom - er.bottom).toFixed(2);
    if ((hiddenY && clipPx > 0.01) || trimmed) {
      clipped.push({ sel: String(el.className || el.tagName).slice(0, 60), clipPx,
                     overflow: st.overflow, textBoxEdge: st.textBoxEdge || '',
                     textBoxTrim: st.textBoxTrim || '' });
    }
  });
  const rv = s.querySelectorAll('.rv');
  let revealed = 0;
  rv.forEach(el => { if (el.classList.contains('in')) revealed++; });
  return { id: s.id, overflow, escapes, clipped,
           rv_total: rv.length, rv_in: revealed,
           font: getComputedStyle(s).fontFamily };
}
"""

INK_RECT = r"""
(sel) => {
  const wm = document.querySelector(sel);
  const r = document.createRange(); r.selectNodeContents(wm);
  const b = r.getBoundingClientRect();
  return {x: Math.floor(b.left), y: Math.floor(b.top),
          width: Math.ceil(b.width), height: Math.ceil(b.height)};
}
"""

FPS = r"""
(ms) => new Promise(res => {
  let n = 0; const t0 = performance.now();
  function tick(){ n++; if (performance.now() - t0 < ms) requestAnimationFrame(tick);
                   else res({frames:n, ms:+(performance.now()-t0).toFixed(1),
                             fps:+(n/((performance.now()-t0)/1000)).toFixed(1)}); }
  requestAnimationFrame(tick);
})
"""


def find_chromium():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
    for pat in (base + "/chromium*/chrome-linux/**/chrome",
                base + "/chromium*/chrome-linux/chrome"):
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    return os.environ.get("RENDER_SHELL")


def mean_lum(page, rect):
    shot = page.screenshot(clip=rect)
    im = Image.open(_io.BytesIO(shot)).convert("L")
    px = list(im.getdata())
    return {"mean": round(sum(px) / len(px), 2), "max": max(px), "px": len(px)}




def main():
    shell = find_chromium()
    if not shell:
        print("FAIL: no chromium executable found")
        return 2

    report = {"deck": str(DECK.relative_to(REPO)), "chromium": shell,
              "slides": [], "console": []}
    fails = []

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=shell,
                               args=["--no-sandbox", "--font-render-hinting=none"])
        pg = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        pg.on("console", lambda m: report["console"].append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: report["console"].append(f"pageerror: {e}"))

        pg.goto(DECK.as_uri())
        pg.wait_for_timeout(1400)

        # ---- the deck chassis ------------------------------------------------
        body_font = pg.evaluate("()=>getComputedStyle(document.body).fontFamily")
        report["body_font_family"] = body_font
        norm = body_font.replace(", ", ",").replace('"', "'")
        want = EXPECT_STACK.replace(", ", ",").replace('"', "'")
        if norm != want:
            fails.append(f"body font-family {body_font!r} != declared stack")

        n = pg.evaluate("()=>document.querySelectorAll('.slide').length")
        report["slide_count"] = n
        if n != 11:
            fails.append(f"slide count {n} != 11")

        # ---- the Milky Way layer is GONE --------------------------------------
        report["sky_canvas_present"] = pg.evaluate("()=>!!document.getElementById('sky')")
        report["sky_globals"] = pg.evaluate(
            "()=>['skyStart','skyFrame','skyStats','skySnap'].filter(k=>k in window)")
        if report["sky_canvas_present"]:
            fails.append("#sky canvas is still in the document")
        if report["sky_globals"]:
            fails.append(f"sky globals survive: {report['sky_globals']}")
        report["card_ground"] = pg.evaluate(
            "()=>getComputedStyle(document.getElementById('s1')).backgroundColor")
        if report["card_ground"].replace(" ", "") != "rgb(12,12,12)":
            fails.append(f"title ground is {report['card_ground']}, want rgb(12,12,12)")

        # ---- the three islands -------------------------------------------------
        isl = pg.evaluate("()=>window.kgIslands()")
        report["islands"] = isl
        report["kg_total_nodes"] = pg.evaluate("()=>window.kgTotal()")
        report["path_len"] = round(pg.evaluate("()=>window.kgPathLen()"), 1)
        report["timing"] = pg.evaluate("()=>window.kgTiming()")
        if sum(isl["counts"]) != report["kg_total_nodes"]:
            fails.append("island counts do not sum to the node total")
        if min(isl["counts"]) < 20:
            fails.append(f"island counts {isl['counts']}: a part is too small to fly through")
        # the split must be a real separation, not a forced k=3
        cxs = sorted(c[0] for c in isl["centroids"])
        seps = [round(cxs[1] - cxs[0], 1), round(cxs[2] - cxs[1], 1)]
        report["centroid_separations_x"] = seps
        report["island_gaps_x"] = [round(g, 1) for g in isl["gaps"]]
        if min(seps) < max(isl["radii"]):
            fails.append(f"centroid separations {seps} smaller than the largest island radius")

        # ---- D · fps WITH THE MOUSE MOVING --------------------------------------
        pg.mouse.move(960, 540)
        pg.evaluate("""()=>{ window.__jig = setInterval(()=>{
            const e = new MouseEvent('mousemove', {clientX: 400 + 900*Math.random(),
              clientY: 300 + 400*Math.random(), bubbles:true});
            window.dispatchEvent(e); }, 33); }""")
        report["fps_mouse_moving"] = pg.evaluate(FPS, 2000)
        pg.evaluate("()=>clearInterval(window.__jig)")
        if report["fps_mouse_moving"]["fps"] < 50:
            fails.append(f"fps with the mouse moving {report['fps_mouse_moving']['fps']} < 50")
        if report["fps_mouse_moving"]["fps"] > 61:
            fails.append(f"fps {report['fps_mouse_moving']['fps']} > 60 cap")

        report["kg_running_on_title"] = pg.evaluate("()=>window.kgRunning()")
        if not report["kg_running_on_title"]:
            fails.append("the fly-through is not running while the title is in view")
        lit = pg.evaluate(
            "()=>{const cv=document.getElementById('kg');"
            "const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;"
            "let b=0; for(let i=0;i<d.length;i+=4){if(d[i+3]>8&&Math.max(d[i],d[i+1],d[i+2])>40)b++;}"
            "return {px:cv.width*cv.height, bright:b, w:cv.width, h:cv.height};}")
        report["kg_canvas"] = lit
        if lit["bright"] < 500:
            fails.append(f"graph canvas not lit: {lit['bright']} bright px")

        # ---- A · THE BOUND, driven to the four corners, 60 phases ---------------
        # The mouse DWELLS at each corner for 15 phases (~1.4 s) before moving
        # on: the spring's time constant is 0.8 s, so flicking corner to
        # corner every 90 ms would hold the offset near zero and prove
        # nothing about the bound.
        CORNERS = [(40, 40), (1880, 40), (1880, 1040), (40, 1040)]
        samples = []
        for k in range(60):
            cx_, cy_ = CORNERS[k // 15]
            # jitter so every sample is a genuine mousemove, not a repeat
            pg.mouse.move(cx_ + (k % 7) - 3, cy_ + (k % 5) - 2)
            pg.wait_for_timeout(90)
            c = pg.evaluate("()=>window.kgCam()")
            c["phase"] = k
            c["corner"] = [cx_, cy_]
            samples.append(c)
        report["bound_samples"] = samples
        worst = max(samples, key=lambda s: s["ratio"])
        report["bound_worst"] = worst
        report["bound_max_ratio"] = round(worst["ratio"], 4)
        over_bound = [s["phase"] for s in samples if s["ratio"] > 0.90 + 1e-6]
        if over_bound:
            fails.append(f"camera outside 0.90 x local island radius at phases {over_bound}")
        # the nudge ceiling: +-12% per axis, so |offset| <= 0.12*sqrt(2)*R
        ceil_ = 0.12 * (2 ** 0.5) + 1e-3
        over_nudge = [s["phase"] for s in samples if s["ratio"] > ceil_]
        if over_nudge:
            fails.append(f"nudge exceeded 12% per axis at phases {over_nudge} "
                         f"(max ratio {report['bound_max_ratio']}, ceiling {round(ceil_,4)})")
        if report["bound_max_ratio"] < 0.02:
            fails.append("the mouse nudge never moved the camera off the path at all")
        # a frame with the mouse parked top-right
        pg.mouse.move(1880, 40)
        pg.wait_for_timeout(400)
        report["cam_parked_top_right"] = pg.evaluate("()=>window.kgCam()")
        pg.screenshot(path=str(OUT / "title-mouse-parked-top-right.png"))

        # ---- B · SELF-CENTRING: back on the path within 2 s ---------------------
        pg.wait_for_timeout(600 + 2000)        # idle window + the settle
        settled = pg.evaluate("()=>window.kgCam()")
        report["cam_after_return"] = settled
        report["return_residual_ratio"] = round(settled["ratio"], 5)
        if settled["live"]:
            fails.append("the camera still thinks the mouse is live 2.6 s after the last move")
        if settled["ratio"] > 0.05 * (0.12 * (2 ** 0.5)) + 0.002:
            fails.append(f"camera did not return to the path: residual ratio "
                         f"{report['return_residual_ratio']} of the local radius")
        pg.screenshot(path=str(OUT / "title-mouse-returned.png"))

        # ---- C · THREE PARTS IN SEQUENCE, t = 10 / 30 / 50 s --------------------
        pg.evaluate("()=>window.kgStop()")
        seq = []
        for t in (10000, 30000, 50000):
            pg.evaluate("(ms)=>window.kgFrame(ms)", t)
            r = pg.evaluate("()=>window.kgProbe(60)")
            r["t_s"] = t // 1000
            r["cam_x"] = round(pg.evaluate("()=>window.kgCam().path[0]"), 1)
            seq.append(r)
        report["island_sequence"] = seq
        got = [r["island"] for r in seq]
        report["island_sequence_ids"] = got
        if got != [1, 2, 3]:
            fails.append(f"the traverse does not pass through three parts in order: {got}")
        if len(set(got)) != 3:
            fails.append(f"the traverse does not reach three DISTINCT populations: {got}")
        # The floor is 8, not 20, and the reason is DATA, not tolerance:
        # island 3 is 124 nodes over a 1,600-unit span (4.4% of the graph in
        # 28% of the axis), so the last leg of the traverse is genuinely
        # thin. What must hold is that there IS a population there and it is
        # island 3's; the count is reported so the thinness is visible.
        for r in seq:
            if r["densityX"] is None or r["visible"] < 8:
                fails.append(f"t={r['t_s']}s: no on-screen node population to measure "
                             f"({r['visible']} visible)")
            if r["visibleIsland"] != r["island"]:
                fails.append(f"t={r['t_s']}s: nearest nodes are island {r['island']} "
                             f"but the screen shows island {r['visibleIsland']}")
        # how much ink is actually on the card at each of the three phases
        ink_seq = []
        for t in (10000, 30000, 50000):
            pg.evaluate("(ms)=>window.kgFrame(ms)", t)
            ink_seq.append({"t_s": t // 1000, "bright_px": pg.evaluate(
                "()=>{const cv=document.getElementById('kg');"
                "const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;"
                "let b=0; for(let i=0;i<d.length;i+=4){if(d[i+3]>8&&Math.max(d[i],d[i+1],d[i+2])>40)b++;}"
                "return b;}")})
        report["island_ink"] = ink_seq
        if min(r["bright_px"] for r in ink_seq) < 200:
            fails.append(f"a traverse phase renders almost no ink: {ink_seq}")

        # ---- the four traverse frames ------------------------------------------
        for t in (5000, 20000, 35000, 50000):
            pg.evaluate("(ms)=>window.kgFrame(ms)", t)
            pg.wait_for_timeout(120)
            pg.screenshot(path=str(OUT / f"title-t{t//1000:02d}s.png"))

        # ---- the TEXT BLOCK unobstructed across 18 phases of the traverse -------
        ink = pg.evaluate(INK_RECT, "#s1 .wordmark")
        sub_ink = pg.evaluate(INK_RECT, "#s1 .sub")
        eb_ink = pg.evaluate(INK_RECT, "#s1 .label")
        report["wordmark_ink_rect"] = ink
        report["subtitle_ink_rect"] = sub_ink
        report["eyebrow_ink_rect"] = eb_ink
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='hidden';}")
        targets = [("wordmark", ink), ("subtitle", sub_ink), ("eyebrow", eb_ink)]
        buckets = {name: [] for name, _ in targets}
        for k in range(18):
            ms = k * (60000 / 18.0)
            pg.evaluate("(ms)=>window.kgFrame(ms)", ms)
            for name, rect in targets:
                shot = pg.screenshot(clip=rect)
                im = Image.open(_io.BytesIO(shot)).convert("L")
                px = list(im.getdata())
                buckets[name].append({"phase": k, "ms": int(ms), "max": max(px),
                                      "px_over_40": sum(1 for v in px if v > 40),
                                      "px": len(px)})
                if name == "wordmark" and k in (0, 9):
                    im.save(str(OUT / f"wordmark-phase-{k:02d}.png"))
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='';}")
        report["wordmark_phases"] = buckets["wordmark"]
        for name, _ in targets:
            worst_n = max(buckets[name], key=lambda r: r["px_over_40"])
            report[f"{name}_worst"] = worst_n
            if worst_n["px_over_40"] > 0:
                fails.append(
                    f"{name} obstructed at phase {worst_n['phase']}: "
                    f"{worst_n['px_over_40']} px above the ground (max {worst_n['max']})")

        pg.evaluate("()=>{window.kgFrame(0); window.kgStart();}")

        # ---- scroll snap lands exactly -----------------------------------------
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(200)
        snaps = []
        for k in range(10):
            pg.keyboard.press("ArrowDown")
            pg.wait_for_timeout(700)
            snaps.append(pg.evaluate(
                "()=>{const d=document.getElementById('deck');"
                "return {top:Math.round(d.scrollTop), vh:d.clientHeight,"
                "mod:Math.round(d.scrollTop)%d.clientHeight};}"))
        report["keyboard_snaps"] = snaps
        for k, s in enumerate(snaps):
            if s["mod"] != 0:
                fails.append(f"ArrowDown #{k+1}: scrollTop {s['top']} not a multiple of {s['vh']}")
        if snaps and snaps[-1]["top"] != 10 * snaps[-1]["vh"]:
            fails.append(f"after 10 x ArrowDown, scrollTop {snaps[-1]['top']} != last section")

        report["kg_running_off_title"] = pg.evaluate("()=>window.kgRunning()")
        if report["kg_running_off_title"]:
            fails.append("the fly-through is still running with the title out of view")

        # ---- per-section measure and screenshot --------------------------------
        for i in range(n):
            pg.evaluate("(i)=>window.deckGo(i)", i)
            pg.wait_for_timeout(900)
            m = pg.evaluate(MEASURE, i)
            m["index"] = i + 1
            ov = m["overflow"]
            if ov["scrollH"] > ov["clientH"] + 1:
                fails.append(f"section {i+1} ({m['id']}): vertical overflow {ov['scrollH']} > {ov['clientH']}")
            if ov["scrollW"] > ov["clientW"] + 1:
                fails.append(f"section {i+1} ({m['id']}): horizontal overflow {ov['scrollW']} > {ov['clientW']}")
            if m["escapes"]:
                fails.append(f"section {i+1} ({m['id']}): {len(m['escapes'])} element(s) outside the section rect")
            if m["clipped"]:
                fails.append(f"section {i+1} ({m['id']}): {len(m['clipped'])} label(s) with clipped descenders")
            if m["rv_total"] and m["rv_in"] != m["rv_total"]:
                fails.append(f"section {i+1} ({m['id']}): reveals {m['rv_in']}/{m['rv_total']}")
            report["slides"].append(m)
            pg.screenshot(path=str(OUT / f"{i+1:02d}-{m['id']}.png"))

        # ---- reduced motion: a still from the middle of island 2 ----------------
        pg2 = br.new_page(viewport={"width": 1920, "height": 1080},
                          device_scale_factor=1, reduced_motion="reduce")
        pg2.goto(DECK.as_uri())
        pg2.wait_for_timeout(1200)
        rm = {"kg_running": pg2.evaluate("()=>window.kgRunning()"),
              "kg_drawn": pg2.evaluate("()=>window.kgDrawn()"),
              "cam": pg2.evaluate("()=>window.kgCam()"),
              "probe": pg2.evaluate("()=>window.kgProbe(60)")}
        report["reduced_motion"] = rm
        if rm["kg_running"]:
            fails.append("prefers-reduced-motion: the fly-through is still animating")
        if rm["kg_drawn"] < 100:
            fails.append("prefers-reduced-motion: the still frame has no nodes")
        if rm["probe"]["island"] != 2:
            fails.append(f"prefers-reduced-motion: the still is among island "
                         f"{rm['probe']['island']}, want island 2")
        pg2.screenshot(path=str(OUT / "title-reduced-motion.png"))
        pg2.close()

        # ---- print ---------------------------------------------------------------
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(400)
        pg.evaluate("()=>window.kgStop()")
        pg.evaluate("()=>window.kgSnap()")
        pg.wait_for_timeout(600)
        report["snap_src_len"] = pg.evaluate(
            "()=>document.getElementById('kgPrint').src.length")
        if report["snap_src_len"] < 5000:
            fails.append("print snapshot is empty")
        # kgSnap() leaves the still on the canvas when the loop was stopped,
        # so this reads the SNAPSHOT's population, not a live frame.
        report["snap_probe"] = pg.evaluate("()=>window.kgProbe(60)")
        report["snap_island"] = report["snap_probe"]["island"]
        if report["snap_island"] != 2:
            fails.append(f"print snapshot is among island {report['snap_island']}, "
                         f"want the middle of island 2")
        pdf = OUT / "deck-v6.pdf"
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

    report["fails"] = fails
    (OUT / "verify.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in
                      ("slide_count", "body_font_family", "sky_canvas_present",
                       "sky_globals", "card_ground", "islands", "kg_total_nodes",
                       "path_len", "timing", "centroid_separations_x", "island_gaps_x",
                       "fps_mouse_moving", "kg_canvas",
                       "kg_running_on_title", "kg_running_off_title",
                       "bound_max_ratio", "bound_worst", "cam_parked_top_right",
                       "return_residual_ratio", "cam_after_return",
                       "island_sequence", "island_sequence_ids", "island_ink",
                       "reduced_motion", "wordmark_worst", "subtitle_worst",
                       "eyebrow_worst", "snap_src_len", "snap_island",
                       "pdf_bytes", "pdf_page_objects", "console", "fails")}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
