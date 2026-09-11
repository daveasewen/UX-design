#!/usr/bin/env python3
"""Drive notes/_DEMO-SLIDES-apollo-2026-09-11-v3.html at 1920x1080.

v3 sits on the designer-community-v3 chassis: y-mandatory scroll snap,
keyboard stepping, IntersectionObserver reveals. So the probes are:

  1. body font-family resolves to the declared reference stack, and the
     fallback face renders without clipped descenders (driven Range
     measurement, not a source grep — #261 label-crop rule);
  2. scroll snap lands each section EXACTLY: after ten ArrowDown presses
     scrollTop % clientHeight == 0 at every step;
  3. reveal classes (.rv.in) are applied on every section once in view;
  4. zero overflow per section (scroll size <= client size, and every
     descendant rect inside the section box);
  5. the title canvas is lit (non-black pixels) and its rAF loop is
     PAUSED once the title scrolls out of view;
  6. the wordmark is unobstructed across 18 phases of the revolution —
     sample the canvas under the wordmark's glyph box at each phase and
     assert the vignette holds it black;
  7. print: one section per landscape page, 11 pages.

Usage (same bash call):
  source knowledge/_render/seat_env.sh && \
    python3 knowledge/_render/verify_demo_slides_268_v3.py
"""
import glob
import json
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
DECK = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-11-v3.html"
OUT = REPO / "notes" / "_subreports" / "slides-268-v3"
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

  // descender clip — driven, against the element's own box
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

  // reveals: every .rv inside this section should have .in once seen
  const rv = s.querySelectorAll('.rv');
  let revealed = 0;
  rv.forEach(el => { if (el.classList.contains('in')) revealed++; });

  return { id: s.id, overflow, escapes, clipped,
           rv_total: rv.length, rv_in: revealed,
           font: getComputedStyle(s).fontFamily };
}
"""

# The wordmark's INK rect (a Range over the text node, not the full-width
# block box), used to clip the composited screenshot.
INK_RECT = r"""
() => {
  const wm = document.querySelector('#s1 .wordmark');
  const r = document.createRange(); r.selectNodeContents(wm);
  const b = r.getBoundingClientRect();
  return {x: Math.floor(b.left), y: Math.floor(b.top),
          width: Math.ceil(b.width), height: Math.ceil(b.height)};
}
"""


def find_chromium():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
    for pat in (base + "/chromium*/chrome-linux/**/chrome",
                base + "/chromium*/chrome-linux/chrome"):
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    return os.environ.get("RENDER_SHELL")


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
        pg.wait_for_timeout(900)

        # ---- 1 · the font line -------------------------------------------------
        body_font = pg.evaluate("()=>getComputedStyle(document.body).fontFamily")
        report["body_font_family"] = body_font
        norm = body_font.replace(", ", ",").replace('"', "'")
        want = EXPECT_STACK.replace(", ", ",").replace('"', "'")
        if norm != want:
            fails.append(f"body font-family {body_font!r} != declared stack")
        report["font_used_first_available"] = pg.evaluate(
            "()=>{const c=document.createElement('canvas').getContext('2d');"
            "c.font='40px \"Univers Next\"'; const a=c.measureText('Apollo').width;"
            "c.font='40px \"Helvetica Neue\", Helvetica, Arial, sans-serif';"
            "return {univers:+a.toFixed(2), fallback:+c.measureText('Apollo').width.toFixed(2)};}")

        n = pg.evaluate("()=>document.querySelectorAll('.slide').length")
        report["slide_count"] = n
        if n != 11:
            fails.append(f"slide count {n} != 11")

        # ---- 5a · the title canvas is lit -------------------------------------
        lit = pg.evaluate(
            "()=>{const cv=document.getElementById('sky');"
            "const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;"
            "let b=0; for(let i=0;i<d.length;i+=4){if(Math.max(d[i],d[i+1],d[i+2])>40)b++;}"
            "return {px:cv.width*cv.height, bright:b, w:cv.width, h:cv.height};}")
        report["title_canvas"] = lit
        if lit["bright"] < 500:
            fails.append(f"title canvas not lit: only {lit['bright']} bright px")
        report["sky_running_on_title"] = pg.evaluate("()=>window.skyRunning()")
        if not report["sky_running_on_title"]:
            fails.append("star field is not running while the title is in view")

        # ---- 6 · wordmark unobstructed across 18 phases ------------------------
        # The honest test is the COMPOSITED result: freeze a phase, hide the
        # type layer, and screenshot exactly the glyph-ink rect. Whatever is
        # left is field + vignette. If the shade holds, nothing there is
        # materially brighter than the #0C0C0C ground, so no node can ever
        # cross the wordmark.
        from PIL import Image
        import io as _io

        ink = pg.evaluate(INK_RECT)
        report["wordmark_ink_rect"] = ink
        pg.evaluate("()=>window.skyStop()")
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='hidden';}")
        phases = []
        PERIOD = 90000
        for k in range(18):
            ms = k * (PERIOD / 18.0)
            pg.evaluate("(ms)=>window.skyFrame(ms)", ms)
            shot = pg.screenshot(clip=ink)
            im = Image.open(_io.BytesIO(shot)).convert("L")
            px = list(im.getdata())
            mx = max(px)
            over = sum(1 for v in px if v > 40)
            phases.append({"phase": k, "ms": int(ms), "max": mx,
                           "px_over_40": over, "px": len(px)})
            if k in (0, 9):
                im.save(str(OUT / f"wordmark-phase-{k:02d}.png"))
        pg.evaluate("()=>{document.querySelector('#s1 .type').style.visibility='';}")
        report["wordmark_phases"] = phases
        worst = max(phases, key=lambda r: r["px_over_40"])
        report["wordmark_worst"] = worst
        if worst["px_over_40"] > 0:
            fails.append(
                f"wordmark obstructed at phase {worst['phase']}: "
                f"{worst['px_over_40']} px above the ground (max {worst['max']})")
        pg.evaluate("()=>window.skyFrame(62000)")   # back to the opening phase
        pg.evaluate("()=>window.skyStart()")

        # ---- 2 · scroll snap lands exactly ------------------------------------
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

        # ---- 5b · the field is paused once the title is gone ------------------
        report["sky_running_off_title"] = pg.evaluate("()=>window.skyRunning()")
        if report["sky_running_off_title"]:
            fails.append("star field still running with the title out of view")

        # ---- 3 + 4 · per-section measure and screenshot ------------------------
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

        # ---- 7 · print -------------------------------------------------------
        pg.evaluate("()=>window.deckGo(0)")
        pg.wait_for_timeout(300)
        pg.evaluate("()=>window.skySnap()")
        pg.wait_for_timeout(400)
        pdf = OUT / "deck-v3.pdf"
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
                      ("slide_count", "body_font_family", "font_used_first_available",
                       "title_canvas", "sky_running_on_title", "sky_running_off_title",
                       "wordmark_ink_rect", "wordmark_worst",
                       "pdf_bytes", "pdf_page_objects", "console", "fails")}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
