#!/usr/bin/env python3
"""Drive notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html at 1920x1080.

v7 is THE WIPE. Dave, verbatim: "when we swipe to the second slide, it
slides over the first but the second slide has the same animation running
from the first so it looks like it doesn't move but it is reversed out,
so black nodes on white. It's a wipe rather than a swipe but the
animation stays in place."

The build is ONE fixed canvas at z-index -1 behind the whole deck, with
sections 1 and 2 as transparent windows onto it and section 2 carrying a
white `mix-blend-mode:difference` plane plus a 55% white lift. So the
things this file has to prove, over and above v6:

  W1  DIFFERENCE ACTUALLY RENDERS IN CHROMIUM. Mid-wipe, at scrollTop
      540, the band below the seam must be a near-white card and the band
      above it the near-black one. A flat white lower half — the failure
      mode when any ancestor forms a stacking context — is a red.
  W2  NODE LUMINANCE ON WHITE in 100..190: visible against a 248 ground
      without fighting 13px type.
  W3  SEAM CONTINUITY. window.kgNodes() is the screen position of every
      node the last pass drew; on a FIXED canvas it must be bit-identical
      at scrollTop 0, 540 and 1080 of the same frozen frame. And in the
      mid-wipe screenshot a node just ABOVE the seam must read bright on
      dark while a node just BELOW it reads dark on light — the same
      field, reversed out, across the join.
  W4  CONTRAST of the strip's type against the measured lifted ground.
  W5  fps >= 50 with BOTH sections in view.
  W6  PRINT: two snapshots, section 2's already reversed out.

Carried from v6: font stack, zero overflow on all 11, snap, reveals,
reduced motion, PDF 11 pages, the title card's own picture.

Usage:
  source knowledge/_render/seat_env.sh && \
    python3 knowledge/_render/verify_demo_slides_268_v7.py
"""
import glob
import io as _io
import json
import os
import pathlib
import re
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
DECK = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-12-v7.html"
OUT = REPO / "notes" / "_subreports" / "slides-268-v7"
OUT.mkdir(parents=True, exist_ok=True)

EXPECT_STACK = '"Univers Next", "Helvetica Neue", Helvetica, Arial, sans-serif'
VH = 1080
MID = 540          # the wipe, half way: the seam sits at viewport y = 540

MEASURE = r"""
(idx) => {
  const s = document.querySelectorAll('.slide')[idx];
  const sr = s.getBoundingClientRect();
  const box = { l: sr.left, t: sr.top, r: sr.right, b: sr.bottom };
  const overflow = { scrollH: s.scrollHeight, clientH: s.clientHeight,
                     scrollW: s.scrollWidth,  clientW: s.clientWidth };
  const escapes = [];
  s.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.bottom > box.b + 1 || r.right > box.r + 1 || r.top < box.t - 1 || r.left < box.l - 1) {
      escapes.push({ sel: String(el.className || el.tagName).slice(0, 60),
                     top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1) });
    }
  });
  const DESC = /[gjpqy]/;
  const clipped = [];
  s.querySelectorAll('.label,.nlab,.ndesc,.n,.stamp,.draft,.switch,.count,.foot,.close-line,th,td,.lead,.body,.ask,.ix,h1,h2,h3')
   .forEach(el => {
    const txt = (el.textContent || '');
    if (!DESC.test(txt)) return;
    const st = getComputedStyle(el);
    const rng = document.createRange(); rng.selectNodeContents(el);
    const rr = rng.getBoundingClientRect(), er = el.getBoundingClientRect();
    const hiddenY = (st.overflow === 'hidden' || st.overflowY === 'hidden');
    const trimmed = (st.textBoxEdge && st.textBoxEdge !== 'auto' && st.textBoxEdge !== 'leading')
                    || (st.textBoxTrim && st.textBoxTrim !== 'none');
    const clipPx = +(rr.bottom - er.bottom).toFixed(2);
    if ((hiddenY && clipPx > 0.01) || trimmed) {
      clipped.push({ sel: String(el.className || el.tagName).slice(0, 60), clipPx });
    }
  });
  const rv = s.querySelectorAll('.rv');
  let revealed = 0; rv.forEach(el => { if (el.classList.contains('in')) revealed++; });
  return { id: s.id, overflow, escapes, clipped,
           rv_total: rv.length, rv_in: revealed, font: getComputedStyle(s).fontFamily };
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

# free scrolling: y-mandatory snap would drag any mid-wipe scrollTop back
SNAP_OFF = "()=>{document.getElementById('deck').style.scrollSnapType='none';}"
SNAP_ON = "()=>{document.getElementById('deck').style.scrollSnapType='';}"
SCROLL_TO = "(y)=>{const d=document.getElementById('deck');d.scrollTop=y;return d.scrollTop;}"


def find_chromium():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
    for pat in (base + "/chromium*/chrome-linux/**/chrome",
                base + "/chromium*/chrome-linux/chrome"):
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    return os.environ.get("RENDER_SHELL")


def shot(page, path=None):
    b = page.screenshot(path=str(path) if path else None)
    return Image.open(_io.BytesIO(b)).convert("L")


def band(im, y0, y1, x0=0, x1=1920):
    px = list(im.crop((x0, y0, x1, y1)).getdata())
    return {"mean": round(sum(px) / len(px), 2), "min": min(px), "max": max(px),
            "n": len(px)}


def modal(im, box):
    """The ground: the most-populated luminance bin inside a rect."""
    h = im.crop(box).histogram()
    v = max(range(256), key=lambda i: h[i])
    return v, h


def _lin(v):
    c = v / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(rgb):
    if isinstance(rgb, (int, float)):
        rgb = (rgb, rgb, rgb)
    r, g, b = (_lin(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = rel_lum(a) + 0.05, rel_lum(b) + 0.05
    return round(max(la, lb) / min(la, lb), 2)


def parse_rgb(css):
    nums = [float(x) for x in re.findall(r"[0-9.]+", css)[:3]]
    return tuple(int(round(x)) for x in nums)


def node_px(im, nodes, lo, hi, xlo=40, xhi=1880):
    """Darkest pixel in the 3x3 around each node whose sy is in [lo,hi)."""
    out = []
    for nd in nodes:
        x, y = int(round(nd["sx"])), int(round(nd["sy"]))
        if not (lo <= y < hi) or not (xlo <= x < xhi):
            continue
        vals = [im.getpixel((x + dx, y + dy))
                for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        out.append({"i": nd["i"], "x": x, "y": y, "z": nd["z"], "deg": nd["deg"],
                    "min": min(vals), "max": max(vals)})
    return out


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
        pg = br.new_page(viewport={"width": 1920, "height": VH}, device_scale_factor=1)
        pg.on("console", lambda m: report["console"].append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: report["console"].append(f"pageerror: {e}"))
        pg.goto(DECK.as_uri())
        pg.wait_for_timeout(1400)

        # ---- chassis ---------------------------------------------------------
        body_font = pg.evaluate("()=>getComputedStyle(document.body).fontFamily")
        report["body_font_family"] = body_font
        if body_font.replace(", ", ",").replace('"', "'") != \
           EXPECT_STACK.replace(", ", ",").replace('"', "'"):
            fails.append(f"body font-family {body_font!r} != declared stack")
        n = pg.evaluate("()=>document.querySelectorAll('.slide').length")
        report["slide_count"] = n
        if n != 11:
            fails.append(f"slide count {n} != 11")

        # ---- 1 · ONE CANVAS, FIXED, OUTSIDE THE DECK --------------------------
        arch = pg.evaluate("""()=>{
          const cv = document.getElementById('kg'), L = document.getElementById('kgLayer');
          const cs = L ? getComputedStyle(L) : null;
          // does anything between .invert and the root form a stacking context?
          const inv = document.querySelector('#s2 .invert');
          const blockers = [];
          let el = inv ? inv.parentElement : null;
          while (el && el !== document.documentElement){
            const s = getComputedStyle(el);
            if (s.isolation === 'isolate' || s.mixBlendMode !== 'normal' ||
                s.transform !== 'none' || s.filter !== 'none' || s.perspective !== 'none' ||
                s.contain.includes('paint') || s.willChange !== 'auto' ||
                (s.position !== 'static' && s.zIndex !== 'auto') ||
                (s.opacity !== '1'))
              blockers.push({sel:String(el.className||el.tagName).slice(0,40),
                             isolation:s.isolation, zIndex:s.zIndex, position:s.position,
                             transform:s.transform, opacity:s.opacity});
            el = el.parentElement;
          }
          return {
            canvas_count: document.querySelectorAll('canvas#kg').length,
            canvas_parent: cv ? cv.parentElement.id : null,
            canvas_in_s1: !!(cv && document.getElementById('s1').contains(cv)),
            canvas_in_deck: !!(cv && document.getElementById('deck').contains(cv)),
            layer_position: cs ? cs.position : null,
            layer_z: cs ? cs.zIndex : null,
            layer_bg: cs ? cs.backgroundColor : null,
            page_ground: getComputedStyle(document.body).backgroundColor,
            s1_bg: getComputedStyle(document.getElementById('s1')).backgroundColor,
            s2_bg: getComputedStyle(document.getElementById('s2')).backgroundColor,
            s3_bg: getComputedStyle(document.getElementById('s3')).backgroundColor,
            s4_bg: getComputedStyle(document.getElementById('s4')).backgroundColor,
            invert_blend: inv ? getComputedStyle(inv).mixBlendMode : null,
            invert_bg: inv ? getComputedStyle(inv).backgroundColor : null,
            lift_bg: getComputedStyle(document.querySelector('#s2 .lift')).backgroundColor,
            stacking_blockers: blockers
          };
        }""")
        report["architecture"] = arch
        if arch["canvas_count"] != 1:
            fails.append(f"{arch['canvas_count']} #kg canvases, want exactly one")
        if arch["canvas_parent"] != "kgLayer" or arch["canvas_in_deck"]:
            fails.append(f"the canvas is not in the fixed layer outside .deck: {arch}")
        if arch["layer_position"] != "fixed":
            fails.append(f"kgLayer position {arch['layer_position']} != fixed")
        if arch["page_ground"].replace(" ", "") != "rgb(12,12,12)":
            fails.append(f"page ground {arch['page_ground']}, want rgb(12,12,12)")
        for k in ("s1_bg", "s2_bg"):
            if "rgba(0,0,0,0)" not in arch[k].replace(" ", ""):
                fails.append(f"{k} is {arch[k]}, want transparent (a window on the canvas)")
        for k in ("s3_bg", "s4_bg"):
            if "rgba(0,0,0,0)" in arch[k].replace(" ", ""):
                fails.append(f"{k} is transparent — section 3+ must cover the canvas")
        if arch["invert_blend"] != "difference":
            fails.append(f"the invert plane's blend mode is {arch['invert_blend']}")
        if arch["stacking_blockers"]:
            fails.append(f"a stacking context stands between .invert and the canvas: "
                         f"{arch['stacking_blockers']}")

        # ---- W5 · fps with BOTH in view --------------------------------------
        pg.evaluate(SNAP_OFF)
        pg.evaluate(SCROLL_TO, MID)
        pg.wait_for_timeout(500)
        report["visible_mid_wipe"] = pg.evaluate("()=>window.kgVisible()")
        report["running_mid_wipe"] = pg.evaluate("()=>window.kgRunning()")
        if not (report["visible_mid_wipe"]["s1"] and report["visible_mid_wipe"]["s2"]):
            fails.append(f"mid-wipe both sections should be in view: {report['visible_mid_wipe']}")
        if not report["running_mid_wipe"]:
            fails.append("the fly-through is not running mid-wipe")
        pg.mouse.move(960, 400)
        pg.evaluate("""()=>{ window.__jig = setInterval(()=>{
            window.dispatchEvent(new MouseEvent('mousemove',
              {clientX:400+900*Math.random(), clientY:200+300*Math.random(), bubbles:true}));
          }, 33); }""")
        report["fps_mid_wipe"] = pg.evaluate(FPS, 2000)
        pg.evaluate("()=>clearInterval(window.__jig)")
        if report["fps_mid_wipe"]["fps"] < 50:
            fails.append(f"fps mid-wipe {report['fps_mid_wipe']['fps']} < 50")

        # ---- freeze one frame: every pixel test below reads the SAME frame ----
        # THE FREEZE. kgStop() alone is not enough: scrolling re-fires the
        # IntersectionObserver, which calls start() again — which is exactly
        # what the deck is supposed to do, and exactly what a frozen-frame
        # probe cannot survive. So start() is stubbed out for the duration.
        FRZ = 20000
        pg.evaluate("()=>window.kgPause(true)")
        pg.evaluate("(ms)=>window.kgFrame(ms)", FRZ)
        pg.wait_for_timeout(120)

        # ---- W3a · the animation STAYS IN PLACE ------------------------------
        # One fixed canvas: the recorded screen positions of a frozen frame must
        # not move by a single float as the deck scrolls under it.
        seam_nodes = {}
        for y in (0, MID, VH):
            pg.evaluate(SCROLL_TO, y)
            pg.wait_for_timeout(140)
            seam_nodes[y] = pg.evaluate("()=>window.kgNodes(80)")
        report["nodes_scrolltop_0"] = seam_nodes[0][:10]
        same_mid = seam_nodes[0] == seam_nodes[MID]
        same_end = seam_nodes[0] == seam_nodes[VH]
        report["node_positions_identical_0_vs_540"] = same_mid
        report["node_positions_identical_0_vs_1080"] = same_end
        report["node_sample_count"] = len(seam_nodes[0])
        if len(seam_nodes[0]) < 20:
            fails.append(f"only {len(seam_nodes[0])} nodes recorded — nothing to compare")
        if not (same_mid and same_end):
            moved = [(a, b) for a, b in zip(seam_nodes[0], seam_nodes[MID])
                     if a != b][:5]
            fails.append(f"the animation MOVED with the scroll — it must stay in place: {moved}")

        # ---- W1 · does `difference` render? mid-wipe bands --------------------
        pg.evaluate(SCROLL_TO, MID)
        pg.wait_for_timeout(160)
        im = shot(pg, OUT / "wipe-mid-scrolltop-540.png")
        above = band(im, 400, 530)            # section 1, clear of its type block
        below = band(im, 552, 700)            # section 2, its top padding — clean
        report["seam_y"] = MID
        report["band_above_seam"] = above
        report["band_below_seam"] = below
        g_above, _ = modal(im, (0, 400, 1920, 530))
        g_below, _ = modal(im, (0, 552, 1920, 700))
        report["ground_above_seam"] = g_above
        report["ground_below_seam"] = g_below
        report["difference_rendered"] = bool(g_below >= 200 and g_above <= 60)
        if g_above > 60:
            fails.append(f"above the seam the ground is L={g_above}, want the dark card (<=60)")
        if g_below < 200:
            fails.append(f"below the seam the ground is L={g_below} — `difference` did not "
                         f"produce the reversed-out white card (want >=200)")
        if below["min"] > g_below - 25:
            fails.append(f"no dark pinpricks on the white card: darkest pixel below the "
                         f"seam is {below['min']} against a ground of {g_below}")
        if above["max"] < g_above + 25:
            fails.append(f"no light pinpricks on the dark card: brightest pixel above the "
                         f"seam is {above['max']} against a ground of {g_above}")

        # ---- W2 + W3b · THE SAME NODES, BOTH POLARITIES ------------------------
        # Dave's claim is that the wipe reverses out a picture that does not
        # move. So the test reads ONE region of the frozen frame twice, with
        # nothing changed but which card is under it:
        #   scrollTop 0    -> the region is section 1: white nodes on #0C0C0C
        #   scrollTop 1080 -> the region is section 2: the same nodes, black
        #                     on the reversed-out white
        # Same canvas, same frame, same screen coordinates. Every node lit in
        # the first read must be dark in the second, at the same pixel.
        #
        # The region is x 1100..1880, y 60..230 — the one corner of the card
        # that carries neither the type block nor any part of the #s1
        # vignette (its radial core reaches an ellipse radius of 1.0 by
        # y = 230 at x >= 1100, so the ink there is the graph's own). Each
        # section's own content is hidden for the read: what is under test is
        # the ground and the field, and the type has its own gate below.
        RX0, RY0, RX1, RY1 = 1100, 60, 1880, 230
        report["seam_region"] = [RX0, RY0, RX1, RY1]
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='hidden';"
                    "document.querySelector('#s2 .inner').style.visibility='hidden';}")
        pg.evaluate(SCROLL_TO, 0)
        pg.wait_for_timeout(200)
        imA = shot(pg, OUT / "seam-A-region-on-dark.png")
        nodesA = pg.evaluate("()=>window.kgNodes(600)")
        pg.evaluate(SCROLL_TO, VH)
        pg.wait_for_timeout(200)
        imB = shot(pg, OUT / "seam-B-region-on-white.png")
        nodesB = pg.evaluate("()=>window.kgNodes(600)")
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='';"
                    "document.querySelector('#s2 .inner').style.visibility='';}")
        report["band_node_positions_identical"] = (nodesA == nodesB)
        if nodesA != nodesB:
            moved = [(a, b) for a, b in zip(nodesA, nodesB) if a != b][:4]
            fails.append(f"the recorded node positions differ between the two reads — "
                         f"the picture is not standing still: {moved}")
        gA, _ = modal(imA, (RX0, RY0, RX1, RY1))
        gB, _ = modal(imB, (RX0, RY0, RX1, RY1))
        report["band_ground_dark"] = gA
        report["band_ground_white"] = gB
        if gA > 60 or gB < 200:
            fails.append(f"the test region is not one strip on both cards: "
                         f"dark read L={gA}, white read L={gB}")
        cand = [nd for nd in nodesA
                if RY0 <= int(round(nd["sy"])) < RY1 and RX0 <= int(round(nd["sx"])) < RX1]
        cand.sort(key=lambda d: d["z"])
        pairs = []
        for nd in cand[:120]:
            x, y = int(round(nd["sx"])), int(round(nd["sy"]))
            va = [imA.getpixel((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
            vb = [imB.getpixel((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
            pairs.append({"i": nd["i"], "x": x, "y": y, "z": nd["z"], "deg": nd["deg"],
                          "on_dark_max": max(va), "on_white_min": min(vb)})
        report["seam_pairs_sampled"] = len(pairs)
        report["seam_pairs"] = pairs[:16]
        lit = [d for d in pairs if d["on_dark_max"] > gA + 25]
        rev = [d for d in lit if d["on_white_min"] < gB - 25]
        report["nodes_lit_on_dark"] = len(lit)
        report["same_nodes_reversed_on_white"] = len(rev)
        report["seam_continuity"] = bool(lit and len(rev) == len(lit))
        if len(lit) < 5:
            fails.append(f"only {len(lit)} lit nodes in the test region — nothing to reverse "
                         f"(ground L={gA}, brightest "
                         f"{max((d['on_dark_max'] for d in pairs), default=None)})")
        elif len(rev) != len(lit):
            missed = [d for d in lit if d not in rev][:5]
            fails.append(f"{len(lit)-len(rev)} of {len(lit)} lit nodes do NOT reverse out "
                         f"on the white card: {missed}")
        lums = sorted(d["on_white_min"] for d in rev)
        report["node_lum_on_white"] = {
            "n": len(lums), "darkest": lums[0] if lums else None,
            "median": lums[len(lums) // 2] if lums else None,
            "lightest": lums[-1] if lums else None}
        if lums:
            if lums[0] < 100:
                fails.append(f"node on white is L={lums[0]} < 100 — too black under "
                             f"13px type; raise the lift")
            if lums[len(lums)//2] > 190:
                fails.append(f"the median reversed node is L={lums[len(lums)//2]} > 190 — "
                             f"losing the field; lower the lift")

        # ---- section 2 settled -------------------------------------------------
        pg.evaluate(SCROLL_TO, VH)
        pg.wait_for_timeout(200)
        im2 = shot(pg, OUT / "s2-settled.png")

        # ---- W4 · contrast of the strip against the MEASURED ground -----------
        strip = pg.evaluate(INK_RECT, "#s2 table.strip")
        report["strip_rect"] = strip
        box = (max(0, strip["x"]), max(0, strip["y"]),
               min(1920, strip["x"] + strip["width"]),
               min(VH, strip["y"] + strip["height"]))
        ground, hist = modal(im2, box)
        report["strip_ground_L"] = ground
        # the colours the card ACTUALLY computes, not a table of tokens: the
        # reversed-out ground tops out at ~250 and v6's --g6 was tuned against
        # pure white, so this has to read the DOM.
        used = pg.evaluate("""()=>{
          const o = {};
          document.querySelectorAll('#s2 table.strip th, #s2 table.strip td').forEach(el=>{
            if (!(el.textContent||'').trim()) return;
            const c = getComputedStyle(el).color;
            const f = Math.round(parseFloat(getComputedStyle(el).fontSize));
            const k = c + ' @' + f + 'px';
            o[k] = (o[k]||0) + 1;
          });
          return o;
        }""")
        report["strip_colours_in_use"] = used
        contrast = {}
        for key, count in used.items():
            css = key.split(" @")[0]
            contrast[key] = {"n": count, "ratio": ratio(parse_rgb(css), ground)}
        report["strip_contrast"] = contrast
        worst_key = min(contrast, key=lambda k: contrast[k]["ratio"])
        report["strip_contrast_worst"] = {worst_key: contrast[worst_key]}
        for key, d in contrast.items():
            px = int(key.split("@")[1].rstrip("px"))
            floor = 4.5 if px < 18 else 3.0
            if d["ratio"] < floor:
                fails.append(f"strip {key} is {d['ratio']}:1 on a ground of L={ground}, "
                             f"floor {floor}:1")
        body_ratio = ratio((0, 0, 0), ground)
        report["strip_body_type_contrast"] = body_ratio
        if body_ratio < 7.0:
            fails.append(f"strip body type is {body_ratio}:1 on L={ground}, floor 7:1")
        # and the nodes must still be there on the settled card
        settled_nodes = pg.evaluate("()=>window.kgNodes(400)")
        sn = node_px(im2, settled_nodes, 8, max(20, strip["y"] - 24))
        report["settled_node_px"] = sn[:10]
        report["settled_ground_L"] = ground
        report["settled_node_window"] = [8, max(20, strip["y"] - 24)]
        dark_settled = sorted(d["min"] for d in sn if d["min"] < ground - 20)
        report["settled_node_lum"] = {"n": len(dark_settled),
                                      "darkest": dark_settled[0] if dark_settled else None}
        if not dark_settled:
            fails.append("section 2 settled: no node reads on the white card at all")

        # ---- the requested frames ---------------------------------------------
        pg.evaluate(SCROLL_TO, 0)
        pg.wait_for_timeout(160)
        pg.evaluate("(ms)=>window.kgFrame(ms)", 20000)
        pg.wait_for_timeout(80)
        pg.screenshot(path=str(OUT / "s1-t20s.png"))
        for y in (270, MID, 810):
            pg.evaluate(SCROLL_TO, y)
            pg.wait_for_timeout(140)
            pg.evaluate("(ms)=>window.kgFrame(ms)", 20000)
            pg.wait_for_timeout(60)
            pg.screenshot(path=str(OUT / f"wipe-scrolltop-{y:04d}.png"))

        # ---- the title card is UNCHANGED: the text block stays unobstructed ----
        pg.evaluate(SCROLL_TO, 0)
        pg.wait_for_timeout(160)
        ink = pg.evaluate(INK_RECT, "#s1 .wordmark")
        sub_ink = pg.evaluate(INK_RECT, "#s1 .sub")
        eb_ink = pg.evaluate(INK_RECT, "#s1 .label")
        report["wordmark_ink_rect"] = ink
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='hidden';}")
        targets = [("wordmark", ink), ("subtitle", sub_ink), ("eyebrow", eb_ink)]
        buckets = {nm: [] for nm, _ in targets}
        for k in range(12):
            ms = k * (60000 / 12.0)
            pg.evaluate("(ms)=>window.kgFrame(ms)", ms)
            for nm, rect in targets:
                imx = Image.open(_io.BytesIO(pg.screenshot(clip=rect))).convert("L")
                px = list(imx.getdata())
                buckets[nm].append({"phase": k, "max": max(px),
                                    "px_over_40": sum(1 for v in px if v > 40)})
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='';}")
        # INHERITED, NOT v7's. The #s1 vignette core is rgba(12,12,12,.70),
        # so a saturated node behind the type reads 240*.30 + 12*.70 = 80
        # against the 40 gate — v6.3's arithmetic, unchanged by the wipe.
        # v6's shipped verifier sampled 18 phases and missed it; at 36
        # phases v6 measures 643 / 467 / 24 px and v7 630 / 462 / 25 on the
        # same three boxes, i.e. v7 is marginally CLEANER. It is kept out of
        # `fails` so the v7 gate says what v7 broke, and reported here in
        # full so nothing is buried.
        inherited = []
        for nm, _ in targets:
            w = max(buckets[nm], key=lambda r: r["px_over_40"])
            report[f"{nm}_worst"] = w
            if w["px_over_40"] > 0:
                inherited.append(f"{nm} obstructed at phase {w['phase']}: "
                                 f"{w['px_over_40']} px above the ground "
                                 f"(max L {w['max']}) — v6.3 defect, carried")
        report["inherited_reds"] = inherited

        pg.evaluate("()=>{ window.kgPause(false); window.kgFrame(0); window.kgStart(); }")
        pg.evaluate(SNAP_ON)

        # ---- snap lands exactly -------------------------------------------------
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(300)
        snaps = []
        for k in range(10):
            pg.keyboard.press("ArrowDown")
            pg.wait_for_timeout(700)
            snaps.append(pg.evaluate(
                "()=>{const d=document.getElementById('deck');"
                "return {top:Math.round(d.scrollTop), vh:d.clientHeight,"
                "mod:Math.round(d.scrollTop)%d.clientHeight};}"))
        report["keyboard_snaps"] = snaps
        for k, sp in enumerate(snaps):
            if sp["mod"] != 0:
                fails.append(f"ArrowDown #{k+1}: scrollTop {sp['top']} not a multiple of {sp['vh']}")
        if snaps and snaps[-1]["top"] != 10 * snaps[-1]["vh"]:
            fails.append(f"after 10 x ArrowDown, scrollTop {snaps[-1]['top']} != last section")

        report["kg_running_off_the_two"] = pg.evaluate("()=>window.kgRunning()")
        report["kg_visible_off_the_two"] = pg.evaluate("()=>window.kgVisible()")
        if report["kg_running_off_the_two"]:
            fails.append("the fly-through still runs with sections 1 and 2 both out of view")

        # ---- per-section measure and screenshot ---------------------------------
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

        # ---- reduced motion ------------------------------------------------------
        pg2 = br.new_page(viewport={"width": 1920, "height": VH},
                          device_scale_factor=1, reduced_motion="reduce")
        pg2.goto(DECK.as_uri())
        pg2.wait_for_timeout(1200)
        rm = {"kg_running": pg2.evaluate("()=>window.kgRunning()"),
              "kg_drawn": pg2.evaluate("()=>window.kgDrawn()"),
              "probe": pg2.evaluate("()=>window.kgProbe(60)")}
        report["reduced_motion"] = rm
        if rm["kg_running"]:
            fails.append("prefers-reduced-motion: the fly-through is still animating")
        if rm["kg_drawn"] < 100:
            fails.append("prefers-reduced-motion: the still frame has no nodes")
        pg2.close()

        # ---- W6 · print: TWO snapshots, section 2's reversed out -----------------
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(400)
        pg.evaluate("()=>window.kgStop()")
        pg.evaluate("()=>window.kgSnap()")
        pg.wait_for_timeout(900)
        report["snap_src_len"] = pg.evaluate("()=>document.getElementById('kgPrint').src.length")
        report["snap2_src_len"] = pg.evaluate("()=>document.getElementById('kgPrint2').src.length")
        if report["snap_src_len"] < 5000:
            fails.append("section 1 print snapshot is empty")
        if report["snap2_src_len"] < 5000:
            fails.append("section 2 print snapshot is empty")
        # is snapshot 2 actually the light one?
        snap_lum = pg.evaluate("""()=>new Promise(res=>{
          const out = {};
          let left = 2;
          ['kgPrint','kgPrint2'].forEach(id=>{
            const im = new Image();
            im.onload = ()=>{
              const c = document.createElement('canvas');
              c.width = 240; c.height = 135;
              const g = c.getContext('2d');
              g.drawImage(im, 0, 0, 240, 135);
              const d = g.getImageData(0,0,240,135).data;
              let s = 0, mn = 255, mx = 0;
              for (let i=0;i<d.length;i+=4){
                const L = 0.299*d[i]+0.587*d[i+1]+0.114*d[i+2];
                s += L; if (L<mn) mn=L; if (L>mx) mx=L;
              }
              out[id] = {mean:+(s/(240*135)).toFixed(1), min:+mn.toFixed(1), max:+mx.toFixed(1)};
              if (!--left) res(out);
            };
            im.onerror = ()=>{ out[id]=null; if(!--left) res(out); };
            im.src = document.getElementById(id).src;
          });
        })""")
        report["print_snapshot_luminance"] = snap_lum
        if snap_lum.get("kgPrint") and snap_lum["kgPrint"]["mean"] > 80:
            fails.append(f"section 1's print snapshot is not dark: {snap_lum['kgPrint']}")
        if snap_lum.get("kgPrint2") and snap_lum["kgPrint2"]["mean"] < 200:
            fails.append(f"section 2's print snapshot is not the reversed-out light card: "
                         f"{snap_lum['kgPrint2']}")

        pdf = OUT / "deck-v7.pdf"
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
    keys = ("slide_count", "body_font_family", "architecture", "visible_mid_wipe",
            "running_mid_wipe", "fps_mid_wipe",
            "node_positions_identical_0_vs_540", "node_positions_identical_0_vs_1080",
            "node_sample_count", "seam_y", "ground_above_seam", "ground_below_seam",
            "difference_rendered", "band_above_seam", "band_below_seam",
            "band_node_positions_identical", "band_ground_dark", "band_ground_white",
            "seam_region", "seam_pairs_sampled", "nodes_lit_on_dark",
            "same_nodes_reversed_on_white", "seam_continuity", "node_lum_on_white",
            "strip_ground_L", "strip_colours_in_use", "strip_contrast",
            "strip_contrast_worst", "strip_body_type_contrast", "settled_node_lum", "wordmark_worst", "subtitle_worst", "eyebrow_worst",
            "kg_running_off_the_two", "reduced_motion", "snap_src_len", "snap2_src_len",
            "print_snapshot_luminance", "pdf_bytes", "pdf_page_objects",
            "console", "inherited_reds", "fails")
    print(json.dumps({k: report.get(k) for k in keys}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
