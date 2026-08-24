#!/usr/bin/env python3
"""Render-verify + drive knowledge/_fitness-test/bento-gallery-showcase-v2.html.

v2 = v1's probe verbatim (it still has to hold) PLUS a FULL-SCALE BENTO leg:
  4. the 12-column split is MEASURED, not asserted -- the rendered width ratio of the a/b tiles
     must match the ratio the control claims (7/5, 8/4, 6/6), to within a gap's worth of pixels.
  5. the two container-query collapses are DRIVEN through the page's own Stage width control
     (not by resizing the viewport), because a @media query could not see that harness at all --
     that is the whole reason the section is written with @container.
  6. the nested tile-level container query is measured: the illustration must sit BESIDE the text
     while the tile is wide and ABOVE it once the tile's own box is narrow.
  7. the var-resolution sweep is extended to the .fs block, so a dangling --fs-* cannot render a
     silently broken grid in one theme.


Homed in-repo per s191-D2 (a throwaway on a sub's outputs mount would have to be declared
NON-REPO; this one does not).

Follows _RUNBOOK-render-verify.md:
  - canvas width probe against TWO CONTROLS, never document.fonts.check() (which cannot fail)
  - env vars re-exported by the caller in EVERY bash call
  - chunked with --stage so no single call approaches the 45 s wall
  - the verdict prints BEFORE any teardown

It does three things a screenshot cannot:
  1. VAR RESOLUTION across 4 themes x light/dark -- every page-local custom property must resolve
     to a non-empty value, because a dangling var renders silent black and no gate sees it.
  2. DRIVES the lightbox by CLICKING the invoker button (not by calling showPopover()), so the
     command/commandfor attribute is what is under test, not the popover API.
  3. Measures the crop that object-fit:cover actually performs, so the aspect-ratio trade-off is a
     number rather than an impression.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob, json, os, sys

REPO = "/sessions/busy-clever-rubin/mnt/UX-design"
PAGE = "file://" + REPO + "/knowledge/_fitness-test/bento-gallery-showcase-v2.html"
OUT = "/sessions/busy-clever-rubin/mnt/outputs"
THEMES = ["mono", "legacy", "console", "supercharge"]

LOCAL_VARS = ["--page", "--surface", "--surface-2", "--surface-3", "--line", "--line-2",
              "--ink", "--ink-2", "--focus", "--focus-w", "--radius", "--radius-ctl",
              "--gutter", "--margin", "--tap"]


def launch(p):
    sh = glob.glob(os.environ["PLAYWRIGHT_BROWSERS_PATH"] + "/chromium_headless_shell-*/chrome-linux/headless_shell")
    return p.chromium.launch(executable_path=sh[0], headless=True,
                             args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])


FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return c.measureText('Handgloves 12345').width; };
  return { target: m('HSBC_MtUnivers_Latin'),
           uf: m('"Univers Next HSBC"'),
           ctrl_dejavu: m('"DejaVu Sans"'),
           ctrl_missing: m('"NoSuchFaceAnywhere"') };
}"""

VAR_PROBE = """(names) => {
  const el = document.querySelector('.bgx');
  const cs = getComputedStyle(el);
  const out = {};
  for (const n of names) out[n] = cs.getPropertyValue(n).trim();
  // also the three things a dangling var would blank
  const tile = document.querySelector('.bx-tile');
  const ts = getComputedStyle(tile);
  out['$body-bg'] = getComputedStyle(document.body).backgroundColor;
  out['$body-ink'] = getComputedStyle(document.body).color;
  out['$tile-bg'] = ts.backgroundColor;
  out['$tile-border'] = ts.borderTopColor;
  out['$tile-radius'] = ts.borderTopLeftRadius;
  // ---- v2: the FULL-SCALE block. A dangling --fs-* would render a broken grid in ONE theme and
  // no gate on this repo would see it, so every one of them is read here, per theme, per mode.
  const fs = document.getElementById('fsGrid');
  const fcs = getComputedStyle(fs);
  for (const n of ['--fs-a','--fs-b','--fs-gap','--fs-pad','--fs-surface'])
    out[n] = fcs.getPropertyValue(n).trim();
  const ft = document.querySelector('#fsGrid .fs-tile');
  const fts = getComputedStyle(ft);
  out['$fs-tile-bg'] = fts.backgroundColor;
  out['$fs-tile-border'] = fts.borderTopColor;
  out['$fs-tile-radius'] = fts.borderTopLeftRadius;
  out['$fs-tile-pad'] = fts.paddingTop;
  out['$fs-h-color'] = getComputedStyle(ft.querySelector('.fs-h')).color;
  out['$fs-link-color'] = getComputedStyle(ft.querySelector('.fs-link')).color;
  return out;
}"""

FS_VARS = ['--fs-a', '--fs-b', '--fs-gap', '--fs-pad', '--fs-surface']


def stage_probe(pg):
    """Numeric assertions. Returns (ok, report)."""
    rep, ok = [], True

    f = pg.evaluate(FONT_PROBE)
    font_ok = (round(f["target"], 2) == round(f["uf"], 2)
               and abs(f["target"] - f["ctrl_dejavu"]) > 1
               and abs(f["target"] - f["ctrl_missing"]) > 1)
    ok &= font_ok
    rep.append("FONT   %s target=%.2f uf=%.2f dejavu=%.2f missing=%.2f"
               % ("PASS" if font_ok else "FAIL", f["target"], f["uf"], f["ctrl_dejavu"], f["ctrl_missing"]))

    # capability badges, measured
    caps = pg.evaluate("""() => ({
        command: 'command' in HTMLButtonElement.prototype,
        popover: HTMLElement.prototype.hasOwnProperty('popover'),
        masonry: CSS.supports('grid-template-rows','masonry')})""")
    rep.append("CAPS   command=%s popover=%s nativeMasonry=%s" % (caps["command"], caps["popover"], caps["masonry"]))
    ok &= caps["command"] and caps["popover"]

    # var resolution across 4 themes x light/dark
    for th in THEMES:
        for mode in ("light", "dark"):
            pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);"
                        "document.documentElement.setAttribute('data-theme',m);}", [th, mode])
            pg.wait_for_timeout(90)
            v = pg.evaluate(VAR_PROBE, LOCAL_VARS)
            names = LOCAL_VARS + FS_VARS
            empty = [k for k in names if not v[k]]
            same = v["$body-bg"] == v["$tile-bg"]
            flat_ink = v["$body-ink"] == v["$body-bg"]
            # a full-scale tile whose heading or link ink equals its own surface is a silent black
            fs_flat = (v["$fs-h-color"] == v["$fs-tile-bg"]) or (v["$fs-link-color"] == v["$fs-tile-bg"])
            bad = bool(empty) or flat_ink or fs_flat
            ok &= not bad
            rep.append("VARS   %-11s %-5s %s empty=%s bodybg=%s tilebg=%s%s border=%s r=%s ink=%s"
                       % (th, mode, "PASS" if not bad else "FAIL", empty or "none",
                          v["$body-bg"], v["$tile-bg"], "  <-- SAME AS PAGE" if same else "",
                          v["$tile-border"], v["$tile-radius"], v["$body-ink"]))
            rep.append("FSVARS %-11s %-5s %s a/b=%s/%s gap=%s pad=%s | tile bg=%s border=%s r=%s pad=%s h=%s link=%s"
                       % (th, mode, "PASS" if not (empty or fs_flat) else "FAIL",
                          v["--fs-a"], v["--fs-b"], v["--fs-gap"], v["--fs-pad"],
                          v["$fs-tile-bg"], v["$fs-tile-border"], v["$fs-tile-radius"],
                          v["$fs-tile-pad"], v["$fs-h-color"], v["$fs-link-color"]))

    pg.evaluate("()=>{document.documentElement.setAttribute('data-apollo-theme','mono');"
                "document.documentElement.setAttribute('data-theme','light');}")

    # DRIVE the lightbox via the invoker button -- the clause under test is command/commandfor
    lb = pg.locator("#lb-3")
    before = pg.evaluate("()=>document.getElementById('lb-3').matches(':popover-open')")
    pg.locator('button[commandfor="lb-3"]').first.click()
    pg.wait_for_timeout(280)
    during = pg.evaluate("()=>document.getElementById('lb-3').matches(':popover-open')")
    pg.locator('#lb-3 button[command="hide-popover"]').click()
    pg.wait_for_timeout(280)
    after = pg.evaluate("()=>document.getElementById('lb-3').matches(':popover-open')")
    lb_ok = (before is False and during is True and after is False)
    ok &= lb_ok
    rep.append("LIGHTBOX %s closed=%s -> opened-by-command=%s -> closed-by-command=%s"
               % ("PASS" if lb_ok else "FAIL", before, during, after))

    # negative control: a button whose commandfor points nowhere must NOT open anything
    ctrl = pg.evaluate("""() => {
      const b = document.createElement('button');
      b.setAttribute('command','show-popover'); b.setAttribute('commandfor','lb-does-not-exist');
      document.body.appendChild(b); b.click();
      const n = document.querySelectorAll(':popover-open').length; b.remove(); return n; }""")
    ok &= (ctrl == 0)
    rep.append("NEGCTRL %s dangling commandfor opened %d popover(s) (expect 0)"
               % ("PASS" if ctrl == 0 else "FAIL", ctrl))

    # object-fit:cover crop, measured -- the aspect-ratio trade-off as a number
    pg.evaluate("()=>{const g=document.getElementById('glMain');g.setAttribute('data-mode','grid');"
                "g.setAttribute('data-aspect','1/1');g.style.setProperty('--gl-ar','1/1');}")
    pg.wait_for_timeout(200)
    crop = pg.evaluate("""() => {
      const out = [];
      for (const sel of ['lb-3','lb-8','lb-9']) {}
      document.querySelectorAll('#glMain .gl-img').forEach((im,i) => {
        const r = im.getBoundingClientRect();
        const nat = im.naturalWidth / im.naturalHeight;
        const box = r.width / r.height;
        const visible = nat > box ? (box/nat) : (nat/box);
        out.push({n:i+1, alt:im.alt, nat:+nat.toFixed(3), box:+box.toFixed(3),
                  kept:+(visible*100).toFixed(1)});
      });
      return out; }""")
    worst = min(crop, key=lambda c: c["kept"])
    rep.append("CROP@1:1 worst=%s keeps %.1f%% of the frame; median kept=%.1f%%"
               % (worst["alt"], worst["kept"],
                  sorted(c["kept"] for c in crop)[len(crop)//2]))
    rep.append("CROP@1:1 detail=" + json.dumps(crop))

    # horizontal overflow, both modes, at this viewport
    for mode in ("masonry", "grid"):
        pg.evaluate("(m)=>document.getElementById('glMain').setAttribute('data-mode',m)", mode)
        pg.wait_for_timeout(150)
        ov = pg.evaluate("()=>document.documentElement.scrollWidth - document.documentElement.clientWidth")
        ok &= (ov <= 0)
        rep.append("OVERFLOW %s %-8s horizontal overflow = %dpx" % ("PASS" if ov <= 0 else "FAIL", mode, ov))

    return ok, rep


GEOM = """() => {
  const g = document.getElementById('fsGrid');
  const gap = parseFloat(getComputedStyle(g).columnGap) || 0;
  const rows = [];
  const tiles = [...g.querySelectorAll('.fs-tile')].map(t => {
    const r = t.getBoundingClientRect();
    const body = t.querySelector('.fs-body').getBoundingClientRect();
    const art  = t.querySelector('.fs-art').getBoundingClientRect();
    return { n:+t.dataset.n, w:+t.dataset.w, flip:t.dataset.flip||'no',
             x:+r.x.toFixed(1), y:+r.y.toFixed(1), width:+r.width.toFixed(1),
             // 'beside' when the two children share a horizontal band; 'above' when stacked
             // BESIDE vs ABOVE is decided by whether the two boxes OVERLAP HORIZONTALLY.
             // The first draft compared top edges against half the shorter box's height, which
             // is a heuristic and it misclassified a tile -- a wrong instrument, not a wrong
             // page. Non-overlap in x is the definition of side-by-side and cannot be fudged.
             layout: (art.right <= body.x + 1 || body.right <= art.x + 1) ? 'beside' : 'above',
             // SIDE IS ONLY MEANINGFUL WHEN THE TWO SIT BESIDE EACH OTHER. Stacked, both boxes
             // share an x and a sub-pixel difference would decide it. Report n/a instead.
             artSide: (art.right <= body.x + 1) ? 'left'
                    : (body.right <= art.x + 1) ? 'right' : 'n/a',
             contentW: +(r.width - 2 * parseFloat(getComputedStyle(t).paddingLeft)
                         - 2 * parseFloat(getComputedStyle(t).borderLeftWidth)).toFixed(1) };
  });
  // group by top edge -> visual rows
  const byY = {};
  for (const t of tiles) { const k = Math.round(t.y); (byY[k] = byY[k] || []).push(t); }
  for (const k of Object.keys(byY).sort((a,b)=>a-b)) rows.push(byY[k].sort((a,b)=>a.x-b.x));
  return { gap:+gap.toFixed(1), tiles, rows: rows.map(r => r.map(t => t.width)),
           perRow: rows.map(r => r.length),
           overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth };
}"""


def stage_palette(pg):
    """NO RED AND NO GREEN, measured in HUE rather than asserted in prose.

    This check exists because the claim was WRONG the first time it was made. v1's store row says
    'no red and no green appears on the page, including in the placeholder photographs, whose
    palette is cool-only by construction'. It is not: `_gen-photos.py`'s own palette comment lists
    'GREENS' among the duotones it draws from, and three of the fourteen placeholders
    (p02-ridge, p07-canopy, p10-estuary) carry hues in the green band. Three of the six the
    full-scale section first reached for were exactly those three -- caught by LOOKING at the
    render, then confirmed by converting every hex in the files to HLS. This is the instrument
    that stops it recurring: it parses the SVGs the page actually references and classifies every
    colour by hue angle.
    ⚠ SCOPE, DECLARED: it covers the FULL-SCALE section's images only. The other 8 placeholders,
    including the 3 green ones, are still used by v1 and by section 2 of this page -- REPORTED,
    NOT SWEPT, because changing section 2's images would change what Dave already has in front of
    him, and that is a change to make deliberately rather than in passing.
    """
    import colorsys, re
    rep, ok = [], True
    srcs = pg.evaluate("()=>[...document.querySelectorAll('#fsGrid .fs-art img')].map(i=>i.getAttribute('src'))")
    base = REPO + "/knowledge/_fitness-test/"
    for s in srcs:
        text = open(base + s).read()
        bad = []
        for h in sorted(set(re.findall(r"#[0-9A-Fa-f]{6}", text))):
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
            hue, light, sat = colorsys.rgb_to_hls(r, g, b)
            deg = hue * 360
            if sat < 0.08:
                continue                      # achromatic
            if 75 <= deg <= 170:
                bad.append(h + " GREEN")
            elif deg < 20 or deg > 340:
                bad.append(h + " RED")
            elif 20 <= deg < 75:
                bad.append(h + " YELLOW/ORANGE")
        ok &= not bad
        rep.append("PALETTE %s %-34s %s" % ("PASS" if not bad else "FAIL", s.split("/")[-1],
                                            "cool only" if not bad else "OFFENDING: " + ", ".join(bad)))
    # and nothing in the page's own CSS may author a colour either
    hexes = pg.evaluate("""() => {
      const css = [...document.querySelectorAll('style')].map(s=>s.textContent).join('\\n');
      return (css.match(/#[0-9A-Fa-f]{3,8}\\b/g) || []); }""")
    ok &= (len(hexes) == 0)
    rep.append("NO-AUTHORED-COLOUR %s the page's own <style> contains %d hex literal(s)%s"
               % ("PASS" if not hexes else "FAIL", len(hexes),
                  "" if not hexes else " -> " + ", ".join(hexes)))
    return ok, rep


def stage_fullscale(pg):
    """The v2 leg. Everything here is a MEASUREMENT of the rendered box, never a read-back of the
    attribute we just set -- an attribute poke proves the attribute, not the layout."""
    rep, ok = [], True

    def setw(v):
        """Drive the page's OWN Stage width control. The point of @container is that this harness
        works on a wide viewport; setting the viewport instead would not test the clause."""
        pg.locator('#rvWidth button[data-v="%s"]' % v).click()
        pg.wait_for_timeout(320)

    def seg(box, v):
        pg.locator('#%s button[data-v="%s"]' % (box, v)).click()
        pg.wait_for_timeout(320)

    pg.locator("#fullscale").scroll_into_view_if_needed()
    setw("100%")

    # --- 1. the split ratio, MEASURED. 12 columns, gap g: an n-span tile is
    #        n/12 * (W + g) - g wide, so width_a + g over width_b + g must equal a/b.
    for ratio, a, b in (("7-5", 7, 5), ("8-4", 8, 4), ("6-6", 6, 6)):
        seg("fsRatio", ratio)
        gm = pg.evaluate(GEOM)
        first = gm["rows"][0]
        got = (first[0] + gm["gap"]) / (first[1] + gm["gap"])
        want = a / b
        good = abs(got - want) < 0.03 and gm["perRow"] == [2, 2, 2]
        ok &= good
        rep.append("FS-SPLIT %s ratio=%-4s rows=%s widths=%s measured=%.3f expected=%.3f"
                   % ("PASS" if good else "FAIL", ratio, gm["perRow"],
                      [r for r in gm["rows"]], got, want))
    seg("fsRatio", "7-5")

    # --- 2. the ALTERNATION is a real side swap, not a class that paints nothing
    seg("fsAlt", "on")
    on = pg.evaluate(GEOM)["tiles"]
    seg("fsAlt", "off")
    off = pg.evaluate(GEOM)["tiles"]
    # only the tiles that actually place art BESIDE text have a side to alternate
    sides_on = [(t["n"], t["artSide"]) for t in on if t["artSide"] != "n/a"]
    sides_off = [(t["n"], t["artSide"]) for t in off if t["artSide"] != "n/a"]
    flip = {t["n"]: t["flip"] for t in on}
    alt_ok = (all(s == "right" for _, s in sides_off)
              and all(s == ("left" if flip[n] == "yes" else "right") for n, s in sides_on)
              and any(s == "left" for _, s in sides_on))
    ok &= alt_ok
    rep.append("FS-ALT   %s on=%s off=%s (flip map=%s)"
               % ("PASS" if alt_ok else "FAIL", sides_on, sides_off, flip))
    seg("fsAlt", "on")

    # --- 3. DOM order never diverges from visual order here (unlike section 1's dense packing).
    #        Measured in both alternation states: source n must ascend left-to-right, row by row.
    order = [t["n"] for t in sorted(pg.evaluate(GEOM)["tiles"], key=lambda t: (t["y"], t["x"]))]
    ord_ok = order == sorted(order)
    ok &= ord_ok
    rep.append("FS-ORDER %s visual order = %s (source order ascending = %s)"
               % ("PASS" if ord_ok else "FAIL", order, ord_ok))

    # --- 4. the two STAGE-level container collapses, driven through the harness
    for w, want_rows, label in (("100%", [2, 2, 2], "full 7/5 alternation"),
                                ("900px", [2, 2, 2], "2-up EQUAL"),
                                ("640px", [1, 1, 1, 1, 1, 1], "single column")):
        setw(w)
        gm = pg.evaluate(GEOM)
        equal = (len(set(round(x) for row in gm["rows"] for x in row)) == 1)
        good = gm["perRow"] == want_rows and gm["overflow"] <= 0
        if w == "900px":
            good = good and equal          # 2-up must be EQUAL, not a squeezed 7/5
        if w == "100%":
            good = good and not equal      # full width must still be ASYMMETRIC
        ok &= good
        rep.append("FS-CQ    %s stage=%-6s perRow=%s equalWidths=%s overflow=%dpx  (%s)"
                   % ("PASS" if good else "FAIL", w, gm["perRow"], equal, gm["overflow"], label))

    # --- 5. the NESTED tile-level container query: beside while wide, above once narrow
    setw("100%")
    wide = pg.evaluate(GEOM)["tiles"]
    setw("380px")
    narrow = pg.evaluate(GEOM)["tiles"]
    # THE CLAUSE IS PER-TILE, NOT PER-PAGE, and that is the point of the nested container:
    # at full stage width the 7-span tiles are wide enough to place art beside text and the
    # 5-span tiles are NOT, so the two halves of the same row resolve DIFFERENTLY. A viewport
    # query cannot express that at all. Threshold is 520px of the tile's CONTENT box.
    def expect(t):
        return "beside" if t["contentW"] > 520 else "above"
    nest_ok = (all(t["layout"] == expect(t) for t in wide)
               and all(t["layout"] == "above" for t in narrow)
               and len({t["layout"] for t in wide}) == 2)   # both outcomes present at full width
    ok &= nest_ok
    rep.append("FS-NEST  %s wide=%s (contentW=%s) narrow=%s"
               % ("PASS" if nest_ok else "FAIL",
                  [(t["n"], t["layout"]) for t in wide], [t["contentW"] for t in wide],
                  [t["layout"] for t in narrow]))

    # --- 6. NEGATIVE CONTROL: if the container query were doing nothing, forcing the stage narrow
    #        while REMOVING container-type would leave the wide layout. Prove the query is load-
    #        bearing by killing it and seeing the collapse disappear, then restoring it.
    pg.evaluate("()=>{document.getElementById('stage').style.containerType='normal';}")
    pg.wait_for_timeout(320)
    killed = pg.evaluate(GEOM)["perRow"]
    pg.evaluate("()=>{document.getElementById('stage').style.containerType='';}")
    pg.wait_for_timeout(320)
    restored = pg.evaluate(GEOM)["perRow"]
    neg_ok = killed == [2, 2, 2] and restored == [1, 1, 1, 1, 1, 1]
    ok &= neg_ok
    rep.append("FS-NEGCTL %s container-type killed -> perRow=%s (expect 2,2,2 i.e. NO collapse); "
               "restored -> %s (expect all 1)" % ("PASS" if neg_ok else "FAIL", killed, restored))

    setw("100%")
    return ok, rep


def shoot(pg, name, theme, mode, width, actions=None, clip_sel=None):
    """Theme and mode are set by CLICKING the real controls, not by setting the attribute.
    Driving the thing is the point: an attribute poke would leave the chrome's aria-pressed
    state stale and the screenshot would misreport which theme it is showing."""
    pg.set_viewport_size({"width": width, "height": 1100})
    pg.locator('#rvTheme button[data-v="%s"]' % theme).click()
    pg.locator('#rvDark button[data-v="%s"]' % mode).click()
    pg.wait_for_timeout(120)
    if actions:
        actions(pg)
    pg.wait_for_timeout(450)
    if clip_sel:
        el = pg.locator(clip_sel).first
        el.scroll_into_view_if_needed()
        pg.wait_for_timeout(250)
    pg.screenshot(path=os.path.join(OUT, name + ".png"))
    return name


def main():
    from playwright.sync_api import sync_playwright
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1400, "height": 1100})
        pg.goto(PAGE)
        pg.wait_for_timeout(900)

        if stage in ("probe", "all"):
            ok, rep = stage_probe(pg)
            print("\n".join(rep))
            print("\nVERDICT: " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("probe-palette", "all"):
            ok, rep = stage_palette(pg)
            print("\n".join(rep))
            print("\nVERDICT(palette): " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("probe-fs", "all"):
            ok, rep = stage_fullscale(pg)
            print("\n".join(rep))
            print("\nVERDICT(full-scale): " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("shots-fs", "all"):
            def fs(q):
                q.evaluate("()=>document.getElementById('fullscale').scrollIntoView()")
            # >=2 themes light, 1 dark, plus the two collapses driven through the stage harness
            shoot(pg, "v2-fs-mono-light", "mono", "light", 1400, actions=fs, clip_sel="#fsGrid")
            shoot(pg, "v2-fs-console-light", "console", "light", 1400, actions=fs, clip_sel="#fsGrid")
            shoot(pg, "v2-fs-supercharge-light", "supercharge", "light", 1400, actions=fs, clip_sel="#fsGrid")
            shoot(pg, "v2-fs-legacy-dark", "legacy", "dark", 1400, actions=fs, clip_sel="#fsGrid")

        if stage in ("shots-fs2", "all"):
            def stagew(v):
                def f(q):
                    q.locator('#rvWidth button[data-v="%s"]' % v).click()
                    q.wait_for_timeout(350)
                    q.evaluate("()=>document.getElementById('fullscale').scrollIntoView()")
                return f
            shoot(pg, "v2-fs-mid-900-collapse", "mono", "light", 1400,
                  actions=stagew("900px"), clip_sel="#fsGrid")
            shoot(pg, "v2-fs-narrow-380-collapse", "mono", "light", 1400,
                  actions=stagew("380px"), clip_sel="#fsGrid")
            shoot(pg, "v2-fs-narrow-viewport-430", "console", "light", 430,
                  actions=stagew("100%"), clip_sel="#fsGrid")

        if stage in ("shots-a",):
            for th in THEMES:
                shoot(pg, "bg-%s-light-bento" % th, th, "light", 1400, clip_sel="#bxGrid")

        if stage in ("shots-b",):
            shoot(pg, "bg-mono-dark-bento", "mono", "dark", 1400, clip_sel="#bxGrid")
            shoot(pg, "bg-supercharge-dark-gallery", "supercharge", "dark", 1400,
                  actions=lambda q: q.evaluate("()=>document.getElementById('glMain').setAttribute('data-mode','masonry')"),
                  clip_sel="#glMain")
            shoot(pg, "bg-mono-light-gallery-grid-1x1", "mono", "light", 1400,
                  actions=lambda q: q.evaluate("()=>{const g=document.getElementById('glMain');"
                                               "g.setAttribute('data-mode','grid');g.setAttribute('data-aspect','1/1');"
                                               "g.style.setProperty('--gl-ar','1/1');}"),
                  clip_sel="#glMain")

        if stage in ("shots-c",):
            # narrow: BOTH a narrow viewport and the stage-width harness
            shoot(pg, "bg-narrow-420-viewport", "console", "light", 420, clip_sel="#bxGrid")
            def stage380(q):
                q.set_viewport_size({"width": 1400, "height": 1100})
                q.evaluate("()=>{const s=document.getElementById('stage');"
                           "s.style.setProperty('--rv-stage-w','380px');s.setAttribute('data-framed','yes');}")
            shoot(pg, "bg-stage380-harness", "legacy", "light", 1400, actions=stage380, clip_sel="#bxGrid")
            # lightbox OPEN, driven by the command attribute
            def openlb(q):
                q.evaluate("()=>{const s=document.getElementById('stage');"
                           "s.style.removeProperty('--rv-stage-w');s.setAttribute('data-framed','no');}")
                q.locator('button[commandfor="lb-9"]').first.click()
            shoot(pg, "bg-lightbox-open-portrait", "mono", "light", 1400, actions=openlb)
            def openlb2(q):
                q.keyboard.press("Escape")
                q.wait_for_timeout(200)
                q.locator('button[commandfor="lb-8"]').first.click()
            shoot(pg, "bg-lightbox-open-dark-console", "console", "dark", 1400, actions=openlb2)

        print("SHOTS: " + " ".join(sorted(os.path.basename(f)
                                          for f in glob.glob(OUT + "/v2-*.png") + glob.glob(OUT + "/bg-*.png"))))
        b.close()


if __name__ == "__main__":
    main()
