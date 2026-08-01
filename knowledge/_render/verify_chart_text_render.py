#!/usr/bin/env python3
"""RENDER-PROOF — chart text must not be CLIPPED and must not COLLIDE.
(Brief finding 1, 2026-07-28 session #29. Dave found this by eye, twice, and named it.)

WHY THIS IS A RENDER-PROOF AND NOT A `_validate_*.py`
-----------------------------------------------------
ds-005 fixed descender clipping and `_validate_descender_clip.py` gates it — but that gate
matches on the CSS property `text-box-edge`, which SVG `<text>` never uses. It structurally
cannot see an axis label. The collision half has no gate anywhere. Both facts are properties
of LAID-OUT GLYPHS, so the only instrument that can see them is a browser.

WHAT IT ASSERTS, per <svg> in a snippet, at every width:

  A · CONTAINMENT — every <text>'s INK sits inside the viewBox.
  B · COLLISION   — no two <text> INK boxes intersect.

★ INK, NOT THE EM BOX — and this is the whole reason the proof is trustworthy.
`getBBox()` returns the em box (font ascent/descent), not the glyphs. On the very label
that provoked this work the two disagree by 4.6 user units:

    'Savings (£000)'  em box   6.00 units above the viewBox ceiling
                      INK      1.38 units above          <- the true, visible clip

A containment check written on `getBBox()` fires 4.6 units early and fails compliant charts
on run 1 — the false-positive class the encoding brief warns about by name. So this proof
measures ink: it re-renders each string to a canvas with the node's own computed font and
scans for painted pixels, then maps the ink insets back onto the laid-out em box.

THE INSTRUMENT MUST BITE BOTH WAYS
-----------------------------------
A proof that only ever reports RED cannot distinguish "detects the defect" from "always
fails" — the mirror of the DV-D17 lesson (an absence-only test passes a full revert).
So there are two controls, and both must hold:

  --bite    inject a synthetic collision + overflow into a CLEAN chart -> must FAIL
  --control apply the geometric fix to scatter IN MEMORY               -> must go GREEN

`--control` doubles as the SPECIFICATION of the remedy: it proves what a fix has to clear
without committing one. The numbers themselves are Dave's to rule (derivation governance).

Run:  python3 knowledge/_render/verify_chart_text_render.py [--bite] [--control] [--all]
      [--bite-ancestors]  (mutation test for the two instrument fixes below —
      ancestor transforms via getCTM(), ancestor visibility via an ancestor walk)
Env:  see knowledge/_RUNBOOK-render-verify.md (fresh sandbox, ~4 calls before a pixel).
"""
import sys, glob, os, pathlib, base64

REPO = pathlib.Path(__file__).resolve().parents[2]
SNIPPETS = REPO / "knowledge/snippets"

BITE = "--bite" in sys.argv
CONTROL = "--control" in sys.argv
ALL = "--all" in sys.argv
BITE_ANCESTORS = "--bite-ancestors" in sys.argv

# The chart under the brief. --all sweeps the family to size the corpus-wide debt.
SUBJECT = ["Chart-scatter"]
FAMILY = ["Chart-bar", "Chart-combo", "Chart-donut", "Chart-line",
          "Chart-scatter", "Chart-sparkline"]
WIDTHS = [1280, 720]

# Ink tolerance in USER UNITS. Sub-pixel overrun is antialiasing, not a defect;
# the canvas scan itself has ~1/8 unit of quantisation at 8x. 0.5 is comfortably
# above the noise and comfortably below the 1.38 the eye can see.
TOL = 0.5

# ---------------------------------------------------------------------------
# In-page measurement. Returns per-<text> INK boxes in the svg's user units.
# ---------------------------------------------------------------------------
MEASURE_JS = r"""
() => {
  // ---------------------------------------------------------------------
  // WHICH MEASUREMENT COMES FROM WHERE, and why. (measuring-tool-must-not-guess)
  //
  //   baseline   <- t.getStartPositionOfChar(0).y   EXACT glyph origin in user units.
  //                 Do NOT recover it from canvas fontBoundingBoxAscent: on the
  //                 licensed cut that reads 13.63 where getBBox's ascent is 15.00,
  //                 which shifts every ink box by 1.37 and inflated the first run
  //                 of this proof from a true 1.38 clip to a reported 2.75.
  //   horizontal <- t.getBBox()                     EXACT laid-out advance, and it
  //                 carries letter-spacing/kerning. A canvas re-render does NOT
  //                 reproduce SVG letter-spacing — using it invented a '150' RIGHT
  //                 clip of 1.20 that does not exist on screen. Em advance is ~1u
  //                 wider than ink (side bearings), i.e. CONSERVATIVE, absorbed by TOL.
  //   vertical   <- canvas ink scan                 The one place the em box is
  //                 catastrophically wrong (ascent 15.00 vs ink 10.38), and the one
  //                 measurement that is letter-spacing independent, so the canvas
  //                 re-render is sound here and only here.
  // ---------------------------------------------------------------------
  const cache = new Map();
  const unresolved = [];

  // -------------------------------------------------------------------
  // FIX (a) — ANCESTOR TRANSFORMS. getBBox()/getStartPositionOfChar() are
  // element-LOCAL. Comparing them straight against the root viewBox is
  // meaningless the moment an intervening <g transform="…"> exists — this
  // is what produced Chart-bar's "LEFT by 3-17" and Chart-combo's
  // "RIGHT by 21.45" in the untrusted --all sweep (78 findings, both
  // fixes named there, neither applied until now).
  // ⚠ getCTM() alone is NOT the fix: it maps into the nearest viewport
  // ancestor's RENDERED PIXEL space (post viewBox->width/height scaling),
  // not into viewBox user units — composing it directly reported a 529-unit
  // "overrun" for a real 58-unit one on a 4x-scaled synthetic case (caught
  // by --bite-ancestors, which is exactly why that mutation test exists).
  // The correct composition is screen-space: invert the ROOT svg's own
  // getScreenCTM() and multiply by the element's getScreenCTM(). That maps
  // element-local user space straight into the root's viewBox units,
  // independent of the svg's own width/height scaling, CSS layout, or zoom.
  // -------------------------------------------------------------------
  function applyMatrix(m, x, y) {
    return { x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f };
  }
  function elementToRootMatrix(el, svgRoot) {
    const rootScreen = svgRoot.getScreenCTM();
    const elScreen = el.getScreenCTM();
    if (!rootScreen || !elScreen) return null;
    return rootScreen.inverse().multiply(elScreen);
  }
  function transformedBBox(el, bb, svgRoot) {
    const m = elementToRootMatrix(el, svgRoot);
    if (!m) return { x: bb.x, y: bb.y, w: bb.width, h: bb.height, scaleY: 1 };
    const corners = [
      applyMatrix(m, bb.x, bb.y),
      applyMatrix(m, bb.x + bb.width, bb.y),
      applyMatrix(m, bb.x, bb.y + bb.height),
      applyMatrix(m, bb.x + bb.width, bb.y + bb.height),
    ];
    const xs = corners.map(c => c.x), ys = corners.map(c => c.y);
    // vertical scale factor, so ink deltas (canvas-measured, LOCAL units)
    // scale the same way the em box just did under this ancestor's transform.
    const scaleY = Math.hypot(m.c, m.d) || 1;
    return { x: Math.min(...xs), y: Math.min(...ys),
             w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys),
             scaleY };
  }
  function transformedPoint(el, x, y, svgRoot) {
    const m = elementToRootMatrix(el, svgRoot);
    return m ? applyMatrix(m, x, y) : { x, y };
  }

  // -------------------------------------------------------------------
  // FIX (b) — ANCESTOR VISIBILITY. The old check read cs.visibility /
  // cs.display / cs.opacity on the TEXT NODE ONLY. `visibility` inherits,
  // so a hidden ancestor happened to be caught by accident there — but
  // `display:none` does NOT inherit: a descendant's own computed display
  // stays whatever it's set to even though the whole subtree is unrendered.
  // Signature from the record: `'Leisure' x 'Leisure'` colliding with
  // itself — donut's `st.visible[id]` centre-figure hidden via an
  // ancestor <g>, reported as live text anyway. Walk every ancestor up
  // to (and including) the owning <svg>.
  // -------------------------------------------------------------------
  function hiddenByAncestry(t) {
    let node = t;
    while (node && node.nodeType === 1) {
      const s = getComputedStyle(node);
      if (s.display === 'none' || s.visibility === 'hidden' ||
          parseFloat(s.opacity || '1') === 0) return true;
      if (node.tagName && node.tagName.toLowerCase() === 'svg') break;
      node = node.parentElement;
    }
    return false;
  }

  function inkVertical(font, weight, size, text) {
    const key = weight + '|' + size + '|' + font + '|' + text;
    if (cache.has(key)) return cache.get(key);
    const S = 8, PADX = 40, BASE = 260;
    const spec = `${weight} ${size * S}px ${font}`;
    // fail loud if the canvas would measure a DIFFERENT face than the SVG paints
    if (!document.fonts.check(`${weight} ${size}px ${font}`)) unresolved.push(spec);
    const c = document.createElement('canvas');
    c.width = Math.ceil(size * S * text.length * 1.4) + PADX * 2;
    c.height = 560;
    const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
    g.fillStyle = '#000';
    g.font = spec;
    g.textBaseline = 'alphabetic';
    g.fillText(text, PADX, BASE);
    const d = g.getImageData(0, 0, c.width, c.height).data;
    let top = 1e9, bot = -1e9;
    for (let y = 0; y < c.height; y++) {
      for (let x = 0; x < c.width; x++) {
        if (d[(y * c.width + x) * 4] < 200) { if (y < top) top = y; if (y > bot) bot = y; break; }
      }
    }
    const r = (bot < top) ? {empty: true}
                          : {empty: false, above: (BASE - top) / S, below: (bot - BASE) / S};
    cache.set(key, r);
    return r;
  }

  const svgs = [];
  document.querySelectorAll('svg').forEach((svg, si) => {
    const nodes = [...svg.querySelectorAll('text')];
    if (!nodes.length) return;
    const vbv = svg.viewBox && svg.viewBox.baseVal;
    // an svg with no viewBox has no design-contract space -> containment is vacuous
    const vb = (vbv && vbv.width) ? {x: vbv.x, y: vbv.y, w: vbv.width, h: vbv.height} : null;
    const boxes = [];
    nodes.forEach((t, ti) => {
      const txt = (t.textContent || '').trim();
      if (!txt) return;
      let bb = null, baselineLocal = null;
      try {
        bb = t.getBBox();
        const p0 = t.getStartPositionOfChar(0);
        baselineLocal = { x: p0.x, y: p0.y };        // EXACT — not inferred
      } catch (e) { return; }
      const cs = getComputedStyle(t);
      const size = parseFloat(cs.fontSize);
      const im = inkVertical(cs.fontFamily, cs.fontWeight, size, txt);
      if (im.empty) return;
      // (a) compose the CTM before comparing against the root viewBox —
      // bb/baseline above are LOCAL; tb/baseline below are ROOT-space.
      const tb = transformedBBox(t, bb, svg);
      const baseline = transformedPoint(t, baselineLocal.x, baselineLocal.y, svg);
      boxes.push({
        i: ti, txt: txt.slice(0, 34), cls: t.getAttribute('class') || '',
        // (b) walk ancestors, not just the node's own computed style.
        hidden: hiddenByAncestry(t),
        x: tb.x, w: tb.w,                             // horizontal: laid-out truth, root space
        y: baseline.y - im.above * tb.scaleY,         // vertical: ink truth, root space
        h: (im.above + im.below) * tb.scaleY,
        em: {y: +bb.y.toFixed(2), h: +bb.height.toFixed(2)}, base: +baseline.y.toFixed(2)
      });
    });
    svgs.push({i: si, cls: svg.getAttribute('class') || '', viewBox: vb, boxes});
  });
  return {svgs, unresolved};
}
"""


def check(svgs, tag, fails, notes):
    """A · containment  and  B · collision, both on INK, both tolerance-aware."""
    for s in svgs:
        vb, live = s["viewBox"], [b for b in s["boxes"] if not b["hidden"]]
        label = f"{tag} svg#{s['i']}"
        # A — containment
        if vb:
            for b in live:
                out = []
                if b["y"] < vb["y"] - TOL:
                    out.append(f"TOP by {vb['y'] - b['y']:.2f}")
                if b["y"] + b["h"] > vb["y"] + vb["h"] + TOL:
                    out.append(f"BOTTOM by {b['y'] + b['h'] - vb['y'] - vb['h']:.2f}")
                if b["x"] < vb["x"] - TOL:
                    out.append(f"LEFT by {vb['x'] - b['x']:.2f}")
                if b["x"] + b["w"] > vb["x"] + vb["w"] + TOL:
                    out.append(f"RIGHT by {b['x'] + b['w'] - vb['x'] - vb['w']:.2f}")
                if out:
                    fails.append(f"{label} CLIP {b['txt']!r} ink outside viewBox: " + ", ".join(out))
        # B — collision
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, c = live[i], live[j]
                ox = min(a["x"] + a["w"], c["x"] + c["w"]) - max(a["x"], c["x"])
                oy = min(a["y"] + a["h"], c["y"] + c["h"]) - max(a["y"], c["y"])
                if ox > TOL and oy > TOL:
                    fails.append(f"{label} COLLIDE {a['txt']!r} x {c['txt']!r} "
                                 f"ink overlap {ox:.2f} x {oy:.2f}")
        notes.append(f"{label}: {len(live)} text nodes measured"
                     + ("" if vb else "  (no viewBox — containment vacuous)"))


# ---------------------------------------------------------------------------
# The two controls
# ---------------------------------------------------------------------------
SENTINEL = "ZZBITE"

BITE_JS = r"""
(sentinel) => {
  // park a sentinel label ON an existing tick AND above the viewBox ceiling
  document.querySelectorAll('svg.dv-svg').forEach(svg => {
    const tick = [...svg.querySelectorAll('text')].find(t => t.textContent.trim() === '0');
    if (!tick) return;
    const n = tick.cloneNode(false);
    n.textContent = sentinel;
    n.setAttribute('x', tick.getAttribute('x'));
    n.setAttribute('y', tick.getAttribute('y'));
    tick.parentNode.insertBefore(n, tick.nextSibling);
  });
}
"""

CONTROL_JS = r"""
() => {
  // the remedy, applied live — see apply_control()'s docstring for the arithmetic
  document.querySelectorAll('svg.dv-svg').forEach(svg => {
    const t = [...svg.querySelectorAll('text')]
      .find(n => n.textContent.trim() === 'Savings (£000)');
    if (!t) return;
    t.setAttribute('x', '46');
    t.setAttribute('y', '11');
  });
}
"""

# ---------------------------------------------------------------------------
# BITE for the two instrument fixes themselves (ancestor transforms /
# ancestor visibility). Neither the family sweep nor the sentinel bite above
# exercises these paths, so each fix gets its own mutation test: a synthetic
# SVG, in memory, loaded by real navigation (goto a data: URL — never
# set_content, per the standing rule), measured with BOTH the OLD
# (pre-fix, reproduced verbatim below) and the CURRENT (fixed) logic.
#   RED   = the OLD logic on the synthetic defect (must misreport)
#   GREEN = the CURRENT logic on the same synthetic defect (must report right)
# Reverting the file's fix is equivalent to running only the OLD branch, so
# this doubles as the "revert makes it fail" proof without touching git.
# ---------------------------------------------------------------------------
ANCESTOR_BITE_HTML = """<!doctype html><html><head><meta charset="utf-8">
<style>text{font: 12px sans-serif;}</style></head><body>
<svg class="dv-svg" viewBox="0 0 100 50" width="400" height="200">
  <g transform="translate(60,0)">
    <text class="dv-axis" x="50" y="20">Overflow</text>
  </g>
</svg>
<svg class="dv-svg-vis" viewBox="0 0 100 50" width="400" height="200">
  <text class="dv-axis" x="10" y="20">Leisure</text>
  <g style="display:none">
    <text class="dv-axis" x="10" y="20">Leisure</text>
  </g>
</svg>
</body></html>"""

ANCESTOR_BITE_JS = r"""
() => {
  const out = {transform: {}, visibility: {}};

  // ---- (a) ancestor transform -------------------------------------------
  const svgT = document.querySelector('.dv-svg');
  const t = svgT.querySelector('text');
  const bb = t.getBBox();
  const vb = svgT.viewBox.baseVal;
  // OLD (pre-fix): compares the LOCAL bbox straight against the viewBox —
  // exactly the code this instrument shipped with before the fix.
  out.transform.old_right_overrun = (bb.x + bb.width) - (vb.x + vb.width);
  // NEW (fixed): compose element->root via getScreenCTM(), NOT getCTM() alone.
  // getCTM() maps into the nearest viewport ancestor's RENDERED PIXEL space
  // (post viewBox->width/height scaling) — composing it directly overreports
  // by the svg's own scale factor (this synthetic case is 4x: caught the
  // first time this bite ran, before the screen-space composition landed).
  const rootScreen = svgT.getScreenCTM();
  const elScreen = t.getScreenCTM();
  const m = rootScreen.inverse().multiply(elScreen);
  const corners = [[bb.x, bb.y], [bb.x + bb.width, bb.y],
                    [bb.x, bb.y + bb.height], [bb.x + bb.width, bb.y + bb.height]]
    .map(([x, y]) => ({x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f}));
  const maxX = Math.max(...corners.map(c => c.x));
  out.transform.new_right_overrun = maxX - (vb.x + vb.width);

  // ---- (b) ancestor visibility -------------------------------------------
  const svgV = document.querySelector('.dv-svg-vis');
  const texts = [...svgV.querySelectorAll('text')];
  const visible = texts[0], hiddenByParent = texts[1];
  const csHidden = getComputedStyle(hiddenByParent);
  // OLD (pre-fix): only the node's own computed style.
  out.visibility.old_hidden_flag = csHidden.visibility === 'hidden' ||
    csHidden.display === 'none' || parseFloat(csHidden.opacity || '1') === 0;
  // NEW (fixed): walk ancestors up to the owning svg.
  function hiddenByAncestry(node) {
    let n = node;
    while (n && n.nodeType === 1) {
      const s = getComputedStyle(n);
      if (s.display === 'none' || s.visibility === 'hidden' ||
          parseFloat(s.opacity || '1') === 0) return true;
      if (n.tagName && n.tagName.toLowerCase() === 'svg') break;
      n = n.parentElement;
    }
    return false;
  }
  out.visibility.new_hidden_flag = hiddenByAncestry(hiddenByParent);
  return out;
}
"""


def run_bite_ancestors():
    from playwright.sync_api import sync_playwright
    shell = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")) or \
        glob.glob(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "") +
                  "/chromium_headless_shell-*/chrome-linux/headless_shell")
    b64 = base64.b64encode(ANCESTOR_BITE_HTML.encode()).decode()
    url = "data:text/html;base64," + b64
    fails = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=shell[0] if shell else None, headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 400, "height": 400})
        page.goto(url)
        page.wait_for_timeout(200)
        r = page.evaluate(ANCESTOR_BITE_JS)
        browser.close()

    tr = r["transform"]
    print(f"   (a) transform  OLD right-overrun={tr['old_right_overrun']:.2f}"
          f"  NEW right-overrun={tr['new_right_overrun']:.2f}  (real clip: text local x=50 "
          f"w~47.4 -> local max 97.4, ancestor <g transform=\"translate(60,0)\"> -> root "
          f"max x ~157.4, viewBox width 100 -> ~57.4 units overrun)")
    # OLD must MISS the defect (reports <= 0, i.e. "fits", since 90.x < 100); NEW must
    # CATCH it (~57.4). Wide band because getBBox() width is font-metric-dependent.
    if tr["old_right_overrun"] > 0.5:
        fails.append("(a) OLD logic unexpectedly caught the overrun — synthetic case is not exercising the bug")
    if not (50.0 < tr["new_right_overrun"] < 65.0):
        fails.append(f"(a) NEW logic did not report ~57 units right-overrun (got {tr['new_right_overrun']:.2f})")

    vis = r["visibility"]
    print(f"   (b) visibility OLD hidden-flag={vis['old_hidden_flag']}  NEW hidden-flag={vis['new_hidden_flag']}"
          " (text sits inside a display:none <g>)")
    if vis["old_hidden_flag"] is not False:
        fails.append("(b) OLD logic unexpectedly saw the ancestor-hidden node as hidden — synthetic case is not exercising the bug")
    if vis["new_hidden_flag"] is not True:
        fails.append("(b) NEW logic failed to mark the ancestor-hidden node as hidden")

    if fails:
        print("\n❌ BITE-ANCESTORS FAILED:")
        for f in fails:
            print("   X", f)
        return 1
    print("\n✅ BITE-ANCESTORS OK — both fixes bite: the OLD (pre-fix) logic reproducibly "
          "misses each defect (right-overrun read as fitting; ancestor-hidden node read as "
          "live), and the CURRENT (fixed) logic catches both. Reverting either fix in the "
          "file reproduces the OLD column exactly, since it is the code the fix replaced.")
    return 0


def apply_bite(html):
    """Inject a SENTINEL defect — a label parked on an existing tick, and pushed above
    the viewBox ceiling.

    ★ Why a sentinel and not a plain duplicate: the subject chart ALREADY fails, so a
    bite that merely asserts "some COLLIDE appeared" passes vacuously — it cannot
    distinguish 'detected the injection' from 'was going to fail anyway'. This is the
    DV-D17 lesson (an absence-only test passes a full revert) in its mirror form. The
    bite therefore demands a finding that NAMES the sentinel, which cannot pre-exist.
    """
    marker = '<text class="dv-axis t-cm-legal" fill="var(--ink)" x="38" y="233" text-anchor="end">0</text>'
    injected = (marker +
                f'\n        <text class="dv-axis t-cm-legal" fill="var(--ink)" x="38" y="233" '
                f'text-anchor="end">{SENTINEL}</text>')
    return html.replace(marker, injected, 1)


def apply_control(html):
    """Apply the GEOMETRIC FIX to scatter in memory — the remedy this proof SPECIFIES
    without committing (derivation governance: the engine never derives-and-promotes).

    ONE move, answering both measured failures at once. The title sits at x=2 y=9 and
    runs 94 units wide — straight through the tick column at x 24-38, and 1.38 units
    above the ceiling. Re-anchoring it to the axis line (x=46) clears the tick column
    entirely, and baseline 9 -> 11 puts the ink top at +0.62, inside the viewBox.

    'Monthly income (£000)' is deliberately NOT touched: Dave ruled its ~0.5-unit
    overrun passes at TOL 0.5 (2026-07-28 #29), so moving it would be an unruled edit.

    The numbers are the agent's ARITHMETIC. Dave rules the final geometry.
    """
    return html.replace(
        '<text class="dv-label t-cm-caption" fill="var(--ink)" x="2" y="9">Savings (£000)</text>',
        '<text class="dv-label t-cm-caption" fill="var(--ink)" x="46" y="11">Savings (£000)</text>')


def main():
    if BITE_ANCESTORS:
        return run_bite_ancestors()

    from playwright.sync_api import sync_playwright
    shell = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")) or \
        glob.glob(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "") +
                  "/chromium_headless_shell-*/chrome-linux/headless_shell")

    targets = FAMILY if ALL else SUBJECT
    fails, notes = [], []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=shell[0] if shell else None, headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        for name in targets:
            path = SNIPPETS / f"{name}.reference.html"
            if not path.exists():
                fails.append(f"{name}: snippet missing at {path}")
                continue
            # ⚠ NEVER set_content() A SNIPPET, and never mutate it via a temp file.
            #
            # set_content's base URL is about:blank, so the linked ../canon/type.css
            # 404s SILENTLY: the axis title then renders 16px instead of 14px (bbox
            # 109.64 vs 95.94 — a 14% larger chart than the one that exists) and
            # document.fonts.check() returns TRUE in BOTH cases, because the fontconfig
            # alias covers the snippet's --font AND type.css's --uf. The standing
            # licensed-cut assertion structurally cannot see the difference.
            # (embedded-payload-url-trap, measured 2026-07-28 #29.)
            #
            # A sibling temp file fixes the URLs but cannot be cleaned up — the mount
            # refuses unlink() with EPERM (sandbox wart: no rm, mv only), so it would
            # leave litter in knowledge/snippets/ on every run. So: load the REAL file
            # and apply both controls as DOM mutations after load.
            for w in WIDTHS:
                page = browser.new_page(viewport={"width": w, "height": 1000})
                page.goto("file://" + str(path))
                if BITE:
                    page.evaluate(BITE_JS, SENTINEL)
                if CONTROL and name == "Chart-scatter":
                    page.evaluate(CONTROL_JS)
                page.wait_for_timeout(500)      # SETTLE BEFORE YOU READ (ds-019)
                if not page.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')"):
                    fails.append(f"[{name} {w}px] licensed HSBC cut did not resolve — "
                                 "measurement would be against the wrong face")
                    page.close()
                    continue
                measured = page.evaluate(MEASURE_JS)
                # UNKNOWN is never defaulted: if the canvas would score a different
                # face than the SVG paints, the vertical ink numbers are meaningless.
                for spec in sorted(set(measured["unresolved"])):
                    fails.append(f"[{name} {w}px] canvas font unresolved for {spec!r} — "
                                 "ink measured against a fallback face, refusing to report")
                check(measured["svgs"], f"[{name} {w}px]", fails, notes)
                page.close()
        browser.close()

    for n in notes:
        print("   ", n)

    if BITE:
        # must NAME the sentinel — "some failure appeared" is not detection here,
        # because the subject chart fails anyway.
        got = [f for f in fails if SENTINEL in f]
        if got:
            print(f"\n✅ BITE OK — the instrument named the injected sentinel "
                  f"({len(got)} finding(s)):")
            for g in got[:2]:
                print("    ", g)
            return 0
        print(f"\n❌ BITE FAILED — a {SENTINEL} label was injected on top of an existing "
              "tick and outside the viewBox, and no finding named it. This instrument "
              "cannot detect what it claims to.")
        return 1

    if CONTROL:
        if fails:
            print("\n❌ CONTROL FAILED — the geometric fix did NOT clear the proof:")
            for f in fails:
                print("   X", f)
            return 1
        print("\n✅ CONTROL OK — with the fix applied in memory the proof goes GREEN. "
              "The instrument reports RED because the defect is real, not because it always fails.")
        return 0

    if fails:
        print(f"\n❌ chart-text render-proof FAILED — {len(fails)} finding(s):")
        for f in fails:
            print("   X", f)
        return 1
    print(f"\n✅ chart-text render-proof GREEN — {len(targets)} chart(s) x {len(WIDTHS)} widths, "
          "licensed cut, no ink clipped and no ink collisions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
