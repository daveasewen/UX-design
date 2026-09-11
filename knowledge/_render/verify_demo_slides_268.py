#!/usr/bin/env python3
"""Drive notes/_DEMO-SLIDES-david-rice-2026-09-11-v1.html at 1920x1080.

Asserts, per slide: no content overflow (scrollHeight <= clientHeight, and every
descendant rect inside the slide box), and no clipped descenders on any label
(driven Range measurement, not a source grep — #261 label-crop rule).
Screenshots every slide, then prints one PDF to confirm page breaks.

Usage (same bash call):
  source knowledge/_render/seat_env.sh && python3 knowledge/_render/verify_demo_slides_268.py
"""
import json, os, pathlib, sys
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
DECK = REPO / "notes" / "_DEMO-SLIDES-david-rice-2026-09-11-v1.html"
OUT = REPO / "notes" / "_subreports" / "slides-268"
OUT.mkdir(parents=True, exist_ok=True)

MEASURE = r"""
(idx) => {
  const s = document.querySelectorAll('.slide')[idx];
  const sr = s.getBoundingClientRect();
  const cs = getComputedStyle(s);
  const padL = parseFloat(cs.paddingLeft), padR = parseFloat(cs.paddingRight);
  const padT = parseFloat(cs.paddingTop), padB = parseFloat(cs.paddingBottom);
  const box = { l: sr.left, t: sr.top, r: sr.right, b: sr.bottom };

  // 1. content overflow of the slide box itself
  const overflow = {
    scrollH: s.scrollHeight, clientH: s.clientHeight,
    scrollW: s.scrollWidth,  clientW: s.clientWidth
  };

  // 2. any descendant escaping the slide's own rect (1px tolerance)
  const escapes = [];
  s.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.bottom > box.b + 1 || r.right > box.r + 1 || r.top < box.t - 1 || r.left < box.l - 1) {
      escapes.push({ sel: el.className || el.tagName,
                     top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1),
                     left: +r.left.toFixed(1), right: +r.right.toFixed(1) });
    }
  });

  // 3. descender clip — driven: measure the ink range against the element's own box
  const DESC = /[gjpqy]/;
  const clipped = [];
  const labelish = s.querySelectorAll('.label,.nlab,.ndesc,.n,.stamp,.draft,.switch,.plot,.count,th,td,.foot span,.meta,.k');
  labelish.forEach(el => {
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
      clipped.push({ sel: el.className || el.tagName, clipPx,
                     overflow: st.overflow, textBoxEdge: st.textBoxEdge || '',
                     textBoxTrim: st.textBoxTrim || '' });
    }
  });

  return { id: s.id, overflow, escapes, clipped,
           pad: [padT, padR, padB, padL] };
}
"""


def main():
    shell = os.environ.get("RENDER_SHELL")
    if not shell:
        import glob
        g = glob.glob(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "") + "/chromium*/chrome-linux/**/chrome",
                      recursive=True) or glob.glob(
            os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "") + "/chromium*/chrome-linux/headless_shell")
        shell = g[0] if g else None
    if not shell:
        print("FAIL: no chromium executable found")
        return 2

    report = {"deck": str(DECK.relative_to(REPO)), "slides": [], "console": []}
    fails = []

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=shell, args=["--no-sandbox", "--font-render-hinting=none"])
        pg = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        pg.on("console", lambda m: report["console"].append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: report["console"].append(f"pageerror: {e}"))
        pg.goto(DECK.as_uri())
        pg.wait_for_timeout(400)
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        report["slide_count"] = n

        for i in range(n):
            pg.evaluate("(i)=>window.deckGo(i)", i)
            pg.wait_for_timeout(120)
            m = pg.evaluate(MEASURE, i)
            m["index"] = i + 1
            ov = m["overflow"]
            if ov["scrollH"] > ov["clientH"]:
                fails.append(f"slide {i+1} ({m['id']}): vertical overflow {ov['scrollH']} > {ov['clientH']}")
            if ov["scrollW"] > ov["clientW"]:
                fails.append(f"slide {i+1} ({m['id']}): horizontal overflow {ov['scrollW']} > {ov['clientW']}")
            if m["escapes"]:
                fails.append(f"slide {i+1} ({m['id']}): {len(m['escapes'])} element(s) outside the slide rect")
            if m["clipped"]:
                fails.append(f"slide {i+1} ({m['id']}): {len(m['clipped'])} label(s) with clipped descenders")
            report["slides"].append(m)
            pg.screenshot(path=str(OUT / f"slide-{i+1:02d}.png"))

        # ? overlay
        pg.evaluate("()=>window.deckGo(0)")
        pg.keyboard.press("?")
        pg.wait_for_timeout(150)
        help_on = pg.evaluate("()=>document.getElementById('help').classList.contains('on')")
        report["help_overlay_toggles"] = bool(help_on)
        if not help_on:
            fails.append("? overlay did not open")
        pg.screenshot(path=str(OUT / "help-overlay.png"))
        pg.keyboard.press("Escape")

        # arrow keys
        pg.evaluate("()=>window.deckGo(0)")
        pg.keyboard.press("ArrowRight")
        pg.wait_for_timeout(80)
        a = pg.evaluate("()=>document.querySelector('#counter').textContent")
        pg.keyboard.press("ArrowLeft")
        pg.wait_for_timeout(80)
        b = pg.evaluate("()=>document.querySelector('#counter').textContent")
        report["keys"] = {"after_right": a.strip(), "after_left": b.strip()}
        if a.strip() != "02 / 10" or b.strip() != "01 / 10":
            fails.append(f"arrow keys: right->{a!r} left->{b!r}")

        # print to PDF
        pdf = OUT / "deck.pdf"
        pg.pdf(path=str(pdf), landscape=True, format="A4",
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
               print_background=True)
        report["pdf_bytes"] = pdf.stat().st_size

        # count printed pages cheaply
        raw = pdf.read_bytes()
        report["pdf_page_objects"] = raw.count(b"/Type /Page\n") + raw.count(b"/Type/Page/")
        br.close()

    report["fails"] = fails
    (OUT / "verify.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in
                      ("slide_count", "help_overlay_toggles", "keys", "pdf_bytes",
                       "pdf_page_objects", "console", "fails")}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
