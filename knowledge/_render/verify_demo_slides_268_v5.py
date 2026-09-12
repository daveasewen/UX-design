#!/usr/bin/env python3
"""Drive notes/_DEMO-SLIDES-apollo-2026-09-12-v5.html at 1920x1080.

v5 is THE BRIDGE: two layers on the title card, at deliberately
different rates —

  background  the v4.1 Milky Way panorama, composited at 50% opacity,
              one revolution every 240 s;
  foreground  the original v2/v3 knowledge graph, white nodes only,
              no family colours and no edges, one revolution every 90 s.

So this run carries the v3/v4 probes forward (font stack, snap, reveals,
zero overflow, wordmark unobstructed, print) and adds the three that are
new to v5:

  A  the background really is at half strength — mean luminance of the
     background-only render OUTSIDE the vignette, measured against the
     same rect on v4.1 (want ~half of it, 9..16);
  B  the foreground really is present all the way round — white node
     pixels in >= 8 of 12 azimuth sectors at every one of 18 phases;
  C  both layers animate and the pair still holds >= 50 fps.

Usage (same bash call):
  source knowledge/_render/seat_env.sh && \
    python3 knowledge/_render/verify_demo_slides_268_v5.py
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
DECK = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-12-v5.html"
PREV = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-11-v4.html"
OUT = REPO / "notes" / "_subreports" / "slides-268-v5"
OUT.mkdir(parents=True, exist_ok=True)

EXPECT_STACK = '"Univers Next", "Helvetica Neue", Helvetica, Arial, sans-serif'

# A rect well clear of the vignette core (which is radial, 52% x 44% at
# 31% / 50%): the top-right corner band of a 1920x1080 frame.
LUM_RECT = {"x": 1420, "y": 40, "width": 460, "height": 300}

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

        # ---- A · background at half strength, against v4.1 --------------------
        pg.goto(PREV.as_uri())
        pg.wait_for_timeout(1400)
        pg.evaluate("()=>window.skyStop()")
        pg.evaluate("()=>window.skyFrame(0)")
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='hidden';"
                    "document.querySelector('#s1 .vignette').style.display='none';}")
        v4_lum = mean_lum(pg, LUM_RECT)
        report["v41_background_luminance"] = v4_lum

        pg.goto(DECK.as_uri() + "?bg=1")
        pg.wait_for_timeout(1400)
        pg.evaluate("()=>window.skyStop()")
        pg.evaluate("()=>window.skyFrame(0)")
        pg.screenshot(path=str(OUT / "title-layer-background-only.png"))
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='hidden';"
                    "document.querySelector('#s1 .vignette').style.display='none';}")
        # The gate is on the LIGHT THE FIELD EMITS, so the card's own #0C0C0C
        # ground is taken out from under it: the v4.1 canvas is opaque and
        # paints that ground itself, so this is exactly like-for-like.
        pg.evaluate("()=>{document.getElementById('s1').style.background='#000';}")
        v5_lum = mean_lum(pg, LUM_RECT)
        pg.evaluate("()=>{document.getElementById('s1').style.background='';}")
        v5_on_card = mean_lum(pg, LUM_RECT)
        report["v5_background_luminance"] = v5_lum
        report["v5_background_luminance_over_card_ground"] = v5_on_card
        report["background_ratio"] = round(v5_lum["mean"] / max(v4_lum["mean"], 0.01), 3)
        if not (9.0 <= v5_lum["mean"] <= 16.0):
            fails.append(f"background mean luminance {v5_lum['mean']} outside 9..16")
        if not (0.44 <= report["background_ratio"] <= 0.56):
            fails.append(f"background ratio {report['background_ratio']} is not ~half of v4.1")

        # ---- foreground alone, for the art director --------------------------
        pg.goto(DECK.as_uri() + "?fg=1")
        pg.wait_for_timeout(1400)
        pg.evaluate("()=>window.kgStop()")
        pg.evaluate("()=>window.kgFrame(0)")
        pg.screenshot(path=str(OUT / "title-layer-foreground-only.png"))
        report["fg_only_node_count"] = pg.evaluate("()=>window.kgDrawn()")

        # ---- the deck proper --------------------------------------------------
        pg.goto(DECK.as_uri())
        pg.wait_for_timeout(1200)

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

        report["periods_ms"] = pg.evaluate("()=>window.kgPeriods()")
        report["kg_total_nodes"] = pg.evaluate("()=>window.kgTotal()")
        report["sky_opacity"] = pg.evaluate(
            "()=>getComputedStyle(document.getElementById('sky')).opacity")

        # ---- both canvases lit -------------------------------------------------
        lit = pg.evaluate(
            "(id)=>{const cv=document.getElementById(id);"
            "const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;"
            "let b=0; for(let i=0;i<d.length;i+=4){if(Math.max(d[i],d[i+1],d[i+2])>40&&d[i+3]>8)b++;}"
            "return {px:cv.width*cv.height, bright:b, w:cv.width, h:cv.height};}", "sky")
        report["sky_canvas"] = lit
        if lit["bright"] < 500:
            fails.append(f"background canvas not lit: {lit['bright']} bright px")
        litk = pg.evaluate(
            "(id)=>{const cv=document.getElementById(id);"
            "const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;"
            "let b=0; for(let i=0;i<d.length;i+=4){if(d[i+3]>8&&Math.max(d[i],d[i+1],d[i+2])>40)b++;}"
            "return {px:cv.width*cv.height, bright:b, w:cv.width, h:cv.height};}", "kg")
        report["kg_canvas"] = litk
        if litk["bright"] < 500:
            fails.append(f"foreground canvas not lit: {litk['bright']} bright px")

        report["sky_running_on_title"] = pg.evaluate("()=>window.skyRunning()")
        report["kg_running_on_title"] = pg.evaluate("()=>window.kgRunning()")
        if not report["sky_running_on_title"]:
            fails.append("background field is not running while the title is in view")
        if not report["kg_running_on_title"]:
            fails.append("foreground graph is not running while the title is in view")

        # ---- C · fps with BOTH layers running ----------------------------------
        report["fps"] = pg.evaluate(FPS, 2000)
        if report["fps"]["fps"] < 50:
            fails.append(f"fps {report['fps']['fps']} < 50")
        if report["fps"]["fps"] > 61:
            fails.append(f"fps {report['fps']['fps']} > 60 cap")

        # ---- B · foreground present round the frame, 18 phases -----------------
        pg.evaluate("()=>{window.skyStop(); window.kgStop();}")
        secs = []
        FG_PERIOD = 90000
        for k in range(18):
            ms = k * (FG_PERIOD / 18.0)
            pg.evaluate("(ms)=>window.kgFrame(ms)", ms)
            r = pg.evaluate("()=>window.kgSectors(12)")
            r["phase"] = k
            r["ms"] = int(ms)
            secs.append(r)
        report["kg_sectors"] = secs
        worst_s = min(secs, key=lambda r: r["occupied"])
        report["kg_sectors_worst"] = worst_s
        report["kg_drawn_min"] = min(r["drawn"] for r in secs)
        report["kg_drawn_max"] = max(r["drawn"] for r in secs)
        bad = [r["phase"] for r in secs if r["occupied"] < 8]
        if bad:
            fails.append(f"foreground occupies < 8/12 azimuth sectors at phases {bad}")

        # ---- TEXT BLOCK unobstructed across 18 phases, BOTH layers -------------
        # v5.1: the wordmark alone was never the whole of what the vignette has
        # to protect. The subtitle went to one line at 34em and ran out past the
        # old ellipse, so a foreground node landed on "speed." at t=60 s. Every
        # line of the block — eyebrow, wordmark, subtitle — is probed here.
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
            ms = k * (FG_PERIOD / 18.0)
            pg.evaluate("(ms)=>{window.skyFrame(ms); window.kgFrame(ms);}", ms)
            for name, rect in targets:
                shot = pg.screenshot(clip=rect)
                im = Image.open(_io.BytesIO(shot)).convert("L")
                px = list(im.getdata())
                buckets[name].append({"phase": k, "ms": int(ms), "max": max(px),
                                      "px_over_40": sum(1 for v in px if v > 40),
                                      "px": len(px)})
                if name == "wordmark" and k in (0, 9):
                    im.save(str(OUT / f"wordmark-phase-{k:02d}.png"))
                if name == "subtitle" and k in (0, 9, 12):
                    im.save(str(OUT / f"subtitle-phase-{k:02d}.png"))
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='';}")
        report["wordmark_phases"] = buckets["wordmark"]
        for name, _ in targets:
            worst_n = max(buckets[name], key=lambda r: r["px_over_40"])
            report[f"{name}_worst"] = worst_n
            if worst_n["px_over_40"] > 0:
                fails.append(
                    f"{name} obstructed at phase {worst_n['phase']}: "
                    f"{worst_n['px_over_40']} px above the ground (max {worst_n['max']})")

        # ---- the three title frames t = 0 / 30 / 60 s --------------------------
        for t in (0, 30000, 60000):
            pg.evaluate("(ms)=>{window.skyFrame(ms); window.kgFrame(ms);}", t)
            pg.wait_for_timeout(120)
            pg.screenshot(path=str(OUT / f"title-t{t//1000:02d}s.png"))

        pg.evaluate("()=>{window.skyFrame(0); window.kgFrame(0); window.skyStart(); window.kgStart();}")

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

        report["sky_running_off_title"] = pg.evaluate("()=>window.skyRunning()")
        report["kg_running_off_title"] = pg.evaluate("()=>window.kgRunning()")
        if report["sky_running_off_title"]:
            fails.append("background field still running with the title out of view")
        if report["kg_running_off_title"]:
            fails.append("foreground graph still running with the title out of view")

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

        # ---- reduced motion: the title is a still ------------------------------
        pg2 = br.new_page(viewport={"width": 1920, "height": 1080},
                          device_scale_factor=1, reduced_motion="reduce")
        pg2.goto(DECK.as_uri())
        pg2.wait_for_timeout(1200)
        report["reduced_motion"] = {
            "sky_running": pg2.evaluate("()=>window.skyRunning()"),
            "kg_running": pg2.evaluate("()=>window.kgRunning()"),
            "kg_drawn": pg2.evaluate("()=>window.kgDrawn()")}
        if report["reduced_motion"]["sky_running"] or report["reduced_motion"]["kg_running"]:
            fails.append("prefers-reduced-motion: a layer is still animating")
        if report["reduced_motion"]["kg_drawn"] < 100:
            fails.append("prefers-reduced-motion: the still frame has no foreground nodes")
        pg2.screenshot(path=str(OUT / "title-reduced-motion.png"))
        pg2.close()

        # ---- print --------------------------------------------------------------
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(400)
        pg.evaluate("()=>window.skySnap()")
        pg.wait_for_timeout(500)
        report["snap_src_len"] = pg.evaluate(
            "()=>document.getElementById('skyPrint').src.length")
        if report["snap_src_len"] < 5000:
            fails.append("print snapshot is empty")
        pdf = OUT / "deck-v5.pdf"
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
                      ("slide_count", "body_font_family", "periods_ms", "sky_opacity",
                       "kg_total_nodes", "kg_drawn_min", "kg_drawn_max",
                       "v41_background_luminance", "v5_background_luminance",
                       "v5_background_luminance_over_card_ground",
                       "background_ratio", "kg_sectors_worst", "fps",
                       "sky_canvas", "kg_canvas",
                       "sky_running_on_title", "kg_running_on_title",
                       "sky_running_off_title", "kg_running_off_title",
                       "reduced_motion", "wordmark_worst", "subtitle_worst",
                       "eyebrow_worst", "snap_src_len",
                       "pdf_bytes", "pdf_page_objects", "console", "fails")}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
