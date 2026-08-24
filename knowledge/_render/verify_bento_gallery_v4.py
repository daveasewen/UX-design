#!/usr/bin/env python3
"""Render-verify + drive knowledge/_fitness-test/bento-gallery-showcase-v4.html.

v4 = v3's probe verbatim (every earlier leg still has to hold) PLUS a GALLERY MASTHEAD leg:
  14. the SCALED BENTO MASTHEAD (`#glHead`) is MEASURED, not asserted: the 6/3/3 column spans are
      read off the rendered boxes as a ratio, the composition is asserted to be exactly TWO row
      units tall at full width, and both container collapses (640 -> six columns, 380 -> three)
      are driven through the page's OWN Stage width control, never by resizing the viewport.
  15. every masthead image is asserted to render with `object-fit:cover` and its crop is reported
      as a percentage of the frame kept -- the same measurement section 2 makes for the gallery.
  16. the var sweep is extended to the `.gh` block (--gh-row, --gh-gap, --gh-c, --gh-r) across
      4 themes x light/dark, so a dangling --gh-* cannot render a collapsed masthead in one theme.
  17. the PALETTE leg now also sweeps the masthead's images. This is the leg that polices the
      green band: p02-ridge, p07-canopy and p10-estuary must never appear in `#glHead`, and the
      check reads the `src` attributes off the RENDERED page rather than off this file's memory.

v3 = v2's probe verbatim (every earlier leg still has to hold) PLUS a BENTO DESIGNER leg:
  8.  the SNAP DESIGNER is DRIVEN with synthetic pointer events -- a tile is drawn by dragging on
      the lattice, then moved, then resized by a corner handle. After each the MODEL is read back
      and asserted to hold whole-column / whole-row-unit values. An attribute poke would prove the
      attribute; a mouse drag proves the snap.
  9.  the GENERATOR's determinism is proven as BYTE EQUALITY of the exported JSON: two different
      seeds must differ, and the same seed visited twice must produce identical bytes.
  10. the EXPORT ROUND-TRIP: export -> paste into the import box -> load -> export again must be
      byte-identical. A recipe that does not round-trip cannot be stored, diffed or reviewed.
  11. the KEYBOARD path is driven: focus a tile, arrow-move, shift-arrow-resize, Delete.
  12. the var sweep is extended to the .dz block (4 themes x light/dark), so a dangling --dz-* var
      cannot render a silently broken canvas in one theme.
  13. the PALETTE leg is extended to every image section 4 can reach (the green-free six).

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
PAGE = "file://" + REPO + "/knowledge/_fitness-test/bento-gallery-showcase-v4.html"
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
  // ---- v3: the BENTO DESIGNER block. Same argument as the .fs block: a dangling --dz-* would
  // render a canvas with no lattice / no row rhythm in ONE theme and no gate would see it.
  const dz = document.getElementById('dzCanvas');
  const dcs = getComputedStyle(dz);
  for (const n of ['--dz-gap','--dz-row','--dz-gap-base','--dz-row-base'])
    out[n] = dcs.getPropertyValue(n).trim();
  out['$dz-canvas-border'] = dcs.borderTopColor;
  out['$dz-canvas-radius'] = dcs.borderTopLeftRadius;
  const dt = document.querySelector('#dzCanvas .dz-tile');
  if (dt) {
    const dts = getComputedStyle(dt);
    out['$dz-tile-bg'] = dts.backgroundColor;
    out['$dz-tile-border'] = dts.borderTopColor;
    out['$dz-tile-ink'] = dts.color;
  }
  const lat = document.querySelector('#dzCanvas .dz-lattice > i');
  out['$dz-lattice-line'] = getComputedStyle(lat).borderLeftColor;
  const gh = document.getElementById('dzGhost');
  out['$dz-ghost-border'] = getComputedStyle(gh).borderTopColor;
  const chip = document.querySelector('#dzCanvas .dz-chip');
  if (chip) out['$dz-chip-bg'] = getComputedStyle(chip).backgroundColor;
  const hnd = document.querySelector('#dzCanvas .dz-h');
  if (hnd) out['$dz-handle-bg'] = getComputedStyle(hnd).backgroundColor;
  // ---- v4: the GALLERY MASTHEAD block. A dangling --gh-row would collapse every tile to a
  // content height and the masthead would silently stop being a masthead in that one theme.
  const ghd = document.getElementById('glHead');
  const gcs = getComputedStyle(ghd);
  for (const n of ['--gh-gap','--gh-row']) out[n] = gcs.getPropertyValue(n).trim();
  const gt = document.querySelector('#glHead .gh-tile');
  const gts = getComputedStyle(gt);
  out['--gh-c'] = gts.getPropertyValue('--gh-c').trim();
  out['--gh-r'] = gts.getPropertyValue('--gh-r').trim();
  out['$gh-tile-bg'] = gts.backgroundColor;
  out['$gh-tile-border'] = gts.borderTopColor;
  out['$gh-tile-radius'] = gts.borderTopLeftRadius;
  out['$gh-tile-h'] = gt.getBoundingClientRect().height.toFixed(1);
  const ta = document.getElementById('dzOutJson');
  out['$dz-textarea-bg'] = getComputedStyle(ta).backgroundColor;
  out['$dz-textarea-ink'] = getComputedStyle(ta).color;
  return out;
}"""

FS_VARS = ['--fs-a', '--fs-b', '--fs-gap', '--fs-pad', '--fs-surface']
DZ_VARS = ['--dz-gap', '--dz-row', '--dz-gap-base', '--dz-row-base']
GH_VARS = ['--gh-gap', '--gh-row', '--gh-c', '--gh-r']


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

    # v3: put tiles on the designer canvas BEFORE the sweep, so the tile/handle/chip properties are
    # real reads rather than absent ones. An absent element cannot fail a colour check.
    pg.locator("#dzSeed3").click()
    pg.wait_for_timeout(200)

    # var resolution across 4 themes x light/dark
    for th in THEMES:
        for mode in ("light", "dark"):
            pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);"
                        "document.documentElement.setAttribute('data-theme',m);}", [th, mode])
            pg.wait_for_timeout(90)
            v = pg.evaluate(VAR_PROBE, LOCAL_VARS)
            names = LOCAL_VARS + FS_VARS + DZ_VARS + GH_VARS
            empty = [k for k in names if not v[k]]
            same = v["$body-bg"] == v["$tile-bg"]
            flat_ink = v["$body-ink"] == v["$body-bg"]
            # a full-scale tile whose heading or link ink equals its own surface is a silent black
            fs_flat = (v["$fs-h-color"] == v["$fs-tile-bg"]) or (v["$fs-link-color"] == v["$fs-tile-bg"])
            # v3: the designer's own silent-black cases. A lattice line the colour of the canvas, a
            # ghost the colour of the canvas, a handle the colour of the tile it sits on, or a
            # textarea whose ink equals its own field, are each an invisible tool and a green gate.
            dz_flat = (v["$dz-lattice-line"] == v["$body-bg"]
                       or v["$dz-ghost-border"] == v["$body-bg"]
                       or v.get("$dz-handle-bg") == v.get("$dz-tile-bg")
                       or v["$dz-textarea-ink"] == v["$dz-textarea-bg"]
                       or v.get("$dz-tile-ink") == v.get("$dz-tile-bg"))
            # v4: a masthead tile whose hairline is the colour of the page is an invisible edge,
            # and a tile shorter than one row unit means --gh-row failed to resolve in this theme.
            gh_flat = (v["$gh-tile-border"] == v["$gh-tile-bg"]
                       or float(v["$gh-tile-h"]) < 40)
            bad = bool(empty) or flat_ink or fs_flat or dz_flat or gh_flat
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
            rep.append("GHVARS %-11s %-5s %s gap=%s row=%s span=%s/%s | tile bg=%s border=%s r=%s h=%s"
                       % (th, mode, "PASS" if not (empty or gh_flat) else "FAIL",
                          v["--gh-gap"], v["--gh-row"], v["--gh-c"], v["--gh-r"],
                          v["$gh-tile-bg"], v["$gh-tile-border"], v["$gh-tile-radius"],
                          v["$gh-tile-h"]))
            rep.append("DZVARS %-11s %-5s %s gap=%s row=%s (base %s/%s) | tile bg=%s ink=%s "
                       "lattice=%s ghost=%s handle=%s chip=%s textarea=%s/%s"
                       % (th, mode, "PASS" if not (empty or dz_flat) else "FAIL",
                          v["--dz-gap"], v["--dz-row"], v["--dz-gap-base"], v["--dz-row-base"],
                          v.get("$dz-tile-bg"), v.get("$dz-tile-ink"), v["$dz-lattice-line"],
                          v["$dz-ghost-border"], v.get("$dz-handle-bg"), v.get("$dz-chip-bg"),
                          v["$dz-textarea-bg"], v["$dz-textarea-ink"]))

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
    ⚠ SCOPE, DECLARED (v4): it covers the FULL-SCALE section's images, section 4's reachable set,
    and the v4 GALLERY MASTHEAD's images. The other 8 placeholders,
    including the 3 green ones, are still used by v1 and by section 2 of this page -- REPORTED,
    NOT SWEPT, because changing section 2's images would change what Dave already has in front of
    him, and that is a change to make deliberately rather than in passing.
    """
    import colorsys, re
    rep, ok = [], True
    # v3: the sweep now covers SECTION 4's whole reachable image set as well as section 3's. The
    # designer/generator can render any of the six the script names, not only the ones on screen
    # right now, so the list is read off the SCRIPT's own array -- an on-screen-only sweep would
    # pass while a green image sat one kind-cycle away.
    srcs = pg.evaluate("""() => {
      const s = new Set([...document.querySelectorAll('#fsGrid .fs-art img')].map(i=>i.getAttribute('src')));
      // v4: the MASTHEAD's images, read off the rendered page. This is the leg that polices the
      // green band for the new header -- p02-ridge, p07-canopy, p10-estuary must not be here.
      for (const i of document.querySelectorAll('#glHead .gh-img')) s.add(i.getAttribute('src'));
      const js = [...document.querySelectorAll('script')].map(x=>x.textContent).join('\\n');
      const m = js.match(/var PHOTOS = \\[([^\\]]*)\\]/);
      if (m) for (const q of m[1].match(/"([^"]+)"/g) || []) s.add('assets-bento-gallery/' + q.slice(1,-1));
      return [...s].sort(); }""")
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


# ============================================================================================
# v3 — THE BENTO DESIGNER LEGS
# ============================================================================================

DZ_METRICS = """() => {
  const c = document.getElementById('dzCanvas');
  const cs = getComputedStyle(c), r = c.getBoundingClientRect();
  const bl = parseFloat(cs.borderLeftWidth), bt = parseFloat(cs.borderTopWidth);
  const br = parseFloat(cs.borderRightWidth);
  const pl = parseFloat(cs.paddingLeft), pt = parseFloat(cs.paddingTop), pr = parseFloat(cs.paddingRight);
  const gap = parseFloat(cs.columnGap) || 0;
  const rowH = parseFloat(cs.getPropertyValue('--dz-row'));
  const innerW = r.width - bl - br - pl - pr;
  const colStep = (innerW - 11 * gap) / 12 + gap;
  return { left: r.left + bl + pl, top: r.top + bt + pt, colStep, rowStep: rowH + gap, gap, rowH };
}"""

# The MODEL, read off the rendered grid placement -- not off a JS variable we could have been
# handed. If the DOM says `grid-column: 3 / span 4` then the snap happened; a private variable
# saying so would only prove the variable.
DZ_MODEL = """(sel) => [...document.querySelectorAll(sel + ' .dz-tile')].map(t => {
  const cs = getComputedStyle(t);
  const c = cs.gridColumnStart, cE = cs.gridColumnEnd, r = cs.gridRowStart, rE = cs.gridRowEnd;
  return { kind: t.dataset.kind, col: c, colEnd: cE, row: r, rowEnd: rE,
           raw: t.style.gridColumn + ' | ' + t.style.gridRow };
})"""


def _cell(m, col, row, fx=0.5, fy=0.5):
    """Client coordinates of a point inside grid cell (col,row), 1-based."""
    x = m["left"] + (col - 1) * m["colStep"] + fx * (m["colStep"] - m["gap"])
    y = m["top"] + (row - 1) * m["rowStep"] + fy * m["rowH"]
    return x, y


def stage_designer(pg):
    """DRIVE the snap designer with real pointer events and assert the SNAPPED model."""
    rep, ok = [], True
    pg.locator('#rvWidth button[data-v="100%"]').click()
    pg.wait_for_timeout(250)
    pg.locator("#designer").scroll_into_view_if_needed()
    pg.locator("#dzClear").click()
    pg.wait_for_timeout(150)

    def model():
        return pg.evaluate(DZ_MODEL, "#dzCanvas")

    # --- 1. DRAW. Press inside cell (2,1), drag to cell (5,2), release. Expect col 2 span 4,
    #        row 1 span 2 -- and expect it EXACTLY, because snap has no tolerance to give.
    m = pg.evaluate(DZ_METRICS)
    x0, y0 = _cell(m, 2, 1, 0.3, 0.3)
    x1, y1 = _cell(m, 5, 2, 0.7, 0.7)
    pg.mouse.move(x0, y0)
    pg.mouse.down()
    pg.mouse.move((x0 + x1) / 2, (y0 + y1) / 2, steps=4)
    pg.mouse.move(x1, y1, steps=4)
    pg.mouse.up()
    pg.wait_for_timeout(200)
    t = model()
    drew = (len(t) == 1 and t[0]["col"] == "2" and t[0]["colEnd"] == "span 4"
            and t[0]["row"] == "1" and t[0]["rowEnd"] == "span 2")
    ok &= drew
    rep.append("DZ-DRAW   %s drag (2,1)->(5,2) gave %s" % ("PASS" if drew else "FAIL", t))

    # --- 2. MOVE. Grab the tile's middle and drop it two columns right, one row down.
    m = pg.evaluate(DZ_METRICS)
    gx, gy = _cell(m, 3, 1, 0.5, 0.5)
    dx, dy = _cell(m, 5, 2, 0.5, 0.5)
    pg.mouse.move(gx, gy)
    pg.mouse.down()
    pg.mouse.move((gx + dx) / 2, (gy + dy) / 2, steps=4)
    pg.mouse.move(dx, dy, steps=4)
    pg.mouse.up()
    pg.wait_for_timeout(200)
    t = model()
    moved = (len(t) == 1 and t[0]["col"] == "4" and t[0]["colEnd"] == "span 4"
             and t[0]["row"] == "2" and t[0]["rowEnd"] == "span 2")
    ok &= moved
    rep.append("DZ-MOVE   %s +2 cols +1 row gave %s" % ("PASS" if moved else "FAIL", t))

    # --- 3. RESIZE by the SE corner handle. Drag it to cell (9,4): expect span 6 x 3 from col 4.
    box = pg.locator('#dzCanvas .dz-tile .dz-h[data-dir="se"]').first.bounding_box()
    m = pg.evaluate(DZ_METRICS)
    tx, ty = _cell(m, 9, 4, 0.5, 0.5)
    pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    pg.mouse.down()
    pg.mouse.move(tx, ty, steps=6)
    pg.mouse.up()
    pg.wait_for_timeout(200)
    t = model()
    resized = (len(t) == 1 and t[0]["col"] == "4" and t[0]["colEnd"] == "span 6"
               and t[0]["row"] == "2" and t[0]["rowEnd"] == "span 3")
    ok &= resized
    rep.append("DZ-RESIZE %s SE handle to (9,4) gave %s" % ("PASS" if resized else "FAIL", t))

    # --- 4. EVERY VALUE IS AN INTEGER SPAN. The point of the whole tool: no pixel ever reaches
    #        the model, so nothing can be half a column.
    integral = all(v["col"].isdigit() and v["row"].isdigit()
                   and v["colEnd"].startswith("span ") and v["colEnd"][5:].isdigit()
                   and v["rowEnd"].startswith("span ") and v["rowEnd"][5:].isdigit()
                   for v in t)
    ok &= integral
    rep.append("DZ-SNAP   %s every placement is a whole column / whole row unit: %s"
               % ("PASS" if integral else "FAIL", [v["raw"] for v in t]))

    # --- 5. KEYBOARD. Focus the tile, arrow-move, shift-arrow-resize, K-cycle, Delete.
    pg.locator("#dzCanvas .dz-tile").first.focus()
    before_kind = model()[0]["kind"]
    pg.keyboard.press("ArrowRight")
    pg.wait_for_timeout(120)
    after_move = model()
    pg.keyboard.press("Shift+ArrowDown")
    pg.wait_for_timeout(120)
    after_res = model()
    pg.keyboard.press("k")
    pg.wait_for_timeout(120)
    after_kind = model()[0]["kind"]
    kb_move = after_move[0]["col"] == "5"
    kb_res = after_res[0]["rowEnd"] == "span 4"
    kb_kind = after_kind != before_kind
    pg.keyboard.press("Delete")
    pg.wait_for_timeout(150)
    kb_del = len(model()) == 0
    kb_ok = kb_move and kb_res and kb_kind and kb_del
    ok &= kb_ok
    rep.append("DZ-KEYS   %s arrow-move col->%s · shift-arrow-resize rowSpan->%s · K %s->%s · Delete left %d tiles"
               % ("PASS" if kb_ok else "FAIL", after_move[0]["col"], after_res[0]["rowEnd"],
                  before_kind, after_kind, 0 if kb_del else -1))

    # --- 6. NEGATIVE CONTROL for the snap claim: a drag that ends 3px from where it started must
    #        still produce a WHOLE 1x1 tile, never a fractional one. If any pixel leaked into the
    #        model this is where it would show.
    m = pg.evaluate(DZ_METRICS)
    x0, y0 = _cell(m, 7, 3, 0.5, 0.5)
    pg.mouse.move(x0, y0)
    pg.mouse.down()
    pg.mouse.move(x0 + 3, y0 + 3, steps=2)
    pg.mouse.up()
    pg.wait_for_timeout(180)
    t = model()
    tiny = (len(t) == 1 and t[0]["col"] == "7" and t[0]["colEnd"] == "span 1"
            and t[0]["row"] == "3" and t[0]["rowEnd"] == "span 1")
    ok &= tiny
    rep.append("DZ-NEGCTL %s a 3px drag still mints a whole 1x1 at (7,3): %s"
               % ("PASS" if tiny else "FAIL", t))

    # --- 7. OVERFLOW, with the canvas populated
    pg.locator("#dzSeed3").click()
    pg.wait_for_timeout(200)
    ov = pg.evaluate("()=>document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok &= (ov <= 0)
    rep.append("DZ-OVERFLOW %s horizontal overflow with a drawn canvas = %dpx"
               % ("PASS" if ov <= 0 else "FAIL", ov))

    # --- 8. THE STAGE HARNESS REACHES THE CANVAS. 12 columns is the law and must NOT change;
    #        what must change is the row unit and the gap. Both halves are asserted, because
    #        "responds to the harness" is only half the claim.
    def dzvars():
        return pg.evaluate("""() => {
          const c = document.getElementById('dzCanvas'), cs = getComputedStyle(c);
          return { cols: cs.gridTemplateColumns.split(' ').length,
                   row: cs.getPropertyValue('--dz-row').trim(),
                   gap: cs.getPropertyValue('--dz-gap').trim(),
                   overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }""")
    wide = dzvars()
    pg.locator('#rvWidth button[data-v="380px"]').click()
    pg.wait_for_timeout(400)
    narrow = dzvars()
    pg.locator('#rvWidth button[data-v="100%"]').click()
    pg.wait_for_timeout(400)
    cq_ok = (wide["cols"] == 12 and narrow["cols"] == 12
             and narrow["row"] != wide["row"] and narrow["gap"] != wide["gap"]
             and narrow["overflow"] <= 0)
    ok &= cq_ok
    rep.append("DZ-CQ     %s full: 12 cols row=%s gap=%s | stage380: 12 cols row=%s gap=%s overflow=%dpx"
               % ("PASS" if cq_ok else "FAIL", wide["row"], wide["gap"],
                  narrow["row"], narrow["gap"], narrow["overflow"]))
    return ok, rep


def stage_generator(pg):
    """Seed determinism + export/import round-trip, both as BYTE EQUALITY."""
    rep, ok = [], True
    pg.locator("#designer").scroll_into_view_if_needed()

    def set_seed(n):
        pg.fill("#pgSeed", str(n))
        pg.wait_for_timeout(250)

    def export_from(which):
        pg.locator('#dzSrc button[data-v="%s"]' % which).click()
        pg.locator("#dzExport").click()
        pg.wait_for_timeout(200)
        return pg.input_value("#dzOutJson"), pg.input_value("#dzOutCode")

    # --- 1. two seeds must DIFFER
    set_seed(2026)
    j_a, c_a = export_from("generated")
    set_seed(7)
    j_b, _ = export_from("generated")
    differ = j_a != j_b
    ok &= differ
    rep.append("GEN-SEEDS  %s seed 2026 (%d bytes) vs seed 7 (%d bytes) differ = %s"
               % ("PASS" if differ else "FAIL", len(j_a), len(j_b), differ))

    # --- 2. the SAME seed twice must be BYTE-IDENTICAL. Revisited through a DIFFERENT seed in
    #        between, so a cached value cannot fake it.
    set_seed(2026)
    j_a2, c_a2 = export_from("generated")
    same = (j_a == j_a2) and (c_a == c_a2)
    ok &= same
    rep.append("GEN-DETERM %s seed 2026 revisited after seed 7: JSON byte-equal=%s CSS byte-equal=%s"
               % ("PASS" if same else "FAIL", j_a == j_a2, c_a == c_a2))

    # --- 3. the "designed" constraints hold: AT MOST ONE HERO, and the hero leads.
    import json as _json
    d = _json.loads(j_a)
    heroes = [t for t in d["tiles"] if t["colSpan"] >= 8 and t["rowSpan"] >= 2]
    hero_ok = len(heroes) <= 1
    ok &= hero_ok
    rep.append("GEN-HERO   %s %d hero tile(s) in a %d-tile layout (rule: at most 1); rowUnit=%s grid=%s"
               % ("PASS" if hero_ok else "FAIL", len(heroes), len(d["tiles"]), d["rowUnit"], d["grid"]))

    # --- 4. no OVERLAP anywhere in a generated layout -- the packer's own correctness, measured
    occ = set()
    overlap = 0
    for t in d["tiles"]:
        for y in range(t["row"], t["row"] + t["rowSpan"]):
            for x in range(t["col"], t["col"] + t["colSpan"]):
                if (x, y) in occ:
                    overlap += 1
                occ.add((x, y))
    inbounds = all(1 <= t["col"] and t["col"] + t["colSpan"] - 1 <= 12 for t in d["tiles"])
    ok &= (overlap == 0 and inbounds)
    rep.append("GEN-PACK   %s overlapping cells=%d, all tiles inside 12 columns=%s"
               % ("PASS" if overlap == 0 and inbounds else "FAIL", overlap, inbounds))

    # --- 5. FILL-HOLES. ⚠ THE OBVIOUS ASSERTION IS FALSE AND WAS DRIVEN RED BEFORE IT WAS WEAKENED.
    #        "dense must be at least as dense as sparse AT EVERY SEED" is NOT a theorem: greedy
    #        first-fit is not optimal, and back-filling an early hole can leave the tail worse. It
    #        went red at seed 2026 (ON 0.720 vs OFF 0.792) — the page was right and the assertion
    #        was wrong. What IS true, and is what is asserted here: the toggle is load-bearing (the
    #        two layouts differ at the same seed), and ACROSS a fixed seed set the mean density is
    #        higher with fill on. Both readings are printed, per seed, so the claim can be re-read.
    SEEDS = (1, 7, 42, 99, 2026, 31337, 555, 808)

    def density():
        dd = _json.loads(pg.input_value("#dzOutJson"))
        rows = max(t["row"] + t["rowSpan"] - 1 for t in dd["tiles"])
        return sum(t["colSpan"] * t["rowSpan"] for t in dd["tiles"]) / float(rows * 12)

    runs = {}
    for mode in ("on", "off"):
        pg.locator('#pgFill button[data-v="%s"]' % mode).click()
        pg.wait_for_timeout(200)
        vals, jsons = [], []
        for s in SEEDS:
            set_seed(s)
            j, _ = export_from("generated")
            vals.append(round(density(), 3))
            jsons.append(j)
        runs[mode] = (vals, jsons)
    pg.locator('#pgFill button[data-v="on"]').click()
    pg.wait_for_timeout(200)
    mean_on = sum(runs["on"][0]) / len(SEEDS)
    mean_off = sum(runs["off"][0]) / len(SEEDS)
    differs = sum(1 for a, b in zip(runs["on"][1], runs["off"][1]) if a != b)
    fill_ok = (mean_on > mean_off) and differs >= len(SEEDS) // 2
    ok &= fill_ok
    rep.append("GEN-FILL   %s mean density over %d seeds: ON=%.3f OFF=%.3f; the toggle changed the "
               "layout at %d/%d seeds"
               % ("PASS" if fill_ok else "FAIL", len(SEEDS), mean_on, mean_off, differs, len(SEEDS)))
    rep.append("GEN-FILL   detail ON =%s" % (runs["on"][0],))
    rep.append("GEN-FILL   detail OFF=%s  (ON is NOT higher at every seed, and is not asserted to be)"
               % (runs["off"][0],))

    # --- 6. ROUND-TRIP. export -> import -> export must be byte-identical, and the CSS recipe too.
    set_seed(2026)
    j1, c1 = export_from("generated")
    pg.fill("#dzIn", j1)
    pg.locator("#dzImport").click()
    pg.wait_for_timeout(300)
    j2, c2 = export_from("designer")
    trip = (j1 == j2) and (c1 == c2)
    ok &= trip
    rep.append("IO-ROUNDTRIP %s generated -> JSON -> designer -> JSON byte-equal=%s ; CSS byte-equal=%s (%d bytes)"
               % ("PASS" if trip else "FAIL", j1 == j2, c1 == c2, len(j1)))

    # --- 7. THE EXPORTED ARTEFACT IS JS-FREE, and that is parsed rather than asserted.
    #        s200-D1: the generator mints CONCRETE VALUES. So: no <script>, no var(--dz-*), no
    #        `random`, and every grid placement is a literal integer.
    import re as _re
    scriptless = ("<script" not in c1.lower()) and ("javascript:" not in c1.lower()) \
        and ("random" not in c1.lower()) and ("onclick" not in c1.lower())
    spans = _re.findall(r"grid-column: (\d+) / span (\d+); grid-row: (\d+) / span (\d+);", c1)
    concrete = len(spans) == len(_json.loads(j1)["tiles"]) and len(spans) > 0
    hexes = _re.findall(r"#[0-9A-Fa-f]{3,8}\b", c1)
    ok &= scriptless and concrete and not hexes
    rep.append("IO-MINTED  %s exported recipe: script-free=%s, %d concrete span rules for %d tiles, "
               "hex literals=%d (colour is tokens only)"
               % ("PASS" if scriptless and concrete and not hexes else "FAIL",
                  scriptless, len(spans), len(_json.loads(j1)["tiles"]), len(hexes)))

    # --- 8. NEGATIVE CONTROL on the importer: junk must be REFUSED and SAID, not silently ignored.
    pg.fill("#dzIn", '{"grid": 8, "rowUnit": 96, "tiles": []}')
    pg.locator("#dzImport").click()
    pg.wait_for_timeout(200)
    msg = pg.text_content("#dzIoStatus") or ""
    still = pg.evaluate("()=>document.querySelectorAll('#dzCanvas .dz-tile').length")
    refuse_ok = msg.startswith("Could not import") and still > 0
    ok &= refuse_ok
    rep.append("IO-NEGCTL  %s a grid:8 recipe was refused with %r and left %d tiles standing"
               % ("PASS" if refuse_ok else "FAIL", msg, still))
    return ok, rep


GH_GEOM = """() => {
  const g = document.getElementById('glHead');
  const cs = getComputedStyle(g);
  const gap = parseFloat(cs.columnGap) || 0;
  const rowH = parseFloat(cs.getPropertyValue('--gh-row'));
  const gr = g.getBoundingClientRect();
  const tiles = [...g.querySelectorAll('.gh-tile')].map(t => {
    const r = t.getBoundingClientRect();
    const im = t.querySelector('img');
    const ir = im.getBoundingClientRect();
    const nat = im.naturalWidth / im.naturalHeight, box = ir.width / ir.height;
    return { k:+t.dataset.k, span:t.dataset.span, src:im.getAttribute('src').split('/').pop(),
             x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1),
             fit:getComputedStyle(im).objectFit,
             kept:+(((nat > box ? box/nat : nat/box)) * 100).toFixed(1) };
  });
  const byY = {};
  for (const t of tiles) { const k = Math.round(t.y); (byY[k] = byY[k] || []).push(t); }
  const rows = Object.keys(byY).sort((a,b)=>a-b).map(k => byY[k].sort((a,b)=>a.x-b.x));
  return { gap:+gap.toFixed(1), rowH, width:+gr.width.toFixed(1), height:+gr.height.toFixed(1),
           tiles, perRow: rows.map(r=>r.length), rowWidths: rows.map(r=>r.map(t=>t.w)),
           overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth };
}"""


def stage_masthead(pg):
    """The v4 leg. Every number is read off the RENDERED box, never off the attribute just set."""
    rep, ok = [], True

    def setw(v):
        pg.locator('#rvWidth button[data-v="%s"]' % v).click()
        pg.wait_for_timeout(340)

    pg.locator("#gallery").scroll_into_view_if_needed()
    setw("100%")
    gm = pg.evaluate(GH_GEOM)

    # --- 1. the 6/3/3 SPANS, measured. 12 columns, gap g: an n-span tile is n/12*(W+g)-g wide,
    #        so (hero + g) / (unit + g) must be exactly 2.
    hero = [t for t in gm["tiles"] if t["span"] == "hero"][0]
    unit = [t for t in gm["tiles"] if t["span"] == "unit"][0]
    tall = [t for t in gm["tiles"] if t["span"] == "tall"][0]
    ratio = (hero["w"] + gm["gap"]) / (unit["w"] + gm["gap"])
    span_ok = abs(ratio - 2.0) < 0.03 and abs(tall["w"] - unit["w"]) < 1.5
    ok &= span_ok
    rep.append("GH-SPAN  %s hero=%.1f tall=%.1f unit=%.1f gap=%.1f -> hero/unit=%.3f (expect 2.000)"
               % ("PASS" if span_ok else "FAIL", hero["w"], tall["w"], unit["w"], gm["gap"], ratio))

    # --- 2. TWO ROW UNITS TALL. This is the whole claim of the word 'masthead' on this page: if
    #        --gh-row failed to resolve the tiles would take their content height and this fails.
    want_h = 2 * gm["rowH"] + gm["gap"]
    h_ok = abs(gm["height"] - want_h) < 2 and abs(hero["h"] - want_h) < 2
    ok &= h_ok
    rep.append("GH-ROWS  %s rowUnit=%.0f measured height=%.1f (expect %.1f = 2 units + gap); hero h=%.1f"
               % ("PASS" if h_ok else "FAIL", gm["rowH"], gm["height"], want_h, hero["h"]))

    # --- 3. HERO-LEFT is the STARTING POSITION, reported as such. Measured so the page's note and
    #        the render cannot drift apart; it is NOT a ruling and the probe does not treat it as one.
    left_most = min(gm["tiles"], key=lambda t: t["x"])
    rep.append("GH-SIDE  INFO hero sits %s (x=%.1f); mirror is equally available -- UNRULED"
               % ("LEFT" if left_most["span"] == "hero" else "RIGHT", hero["x"]))

    # --- 4. object-fit:cover on every tile, with the crop as a number rather than an impression.
    fit_ok = all(t["fit"] == "cover" for t in gm["tiles"])
    ok &= fit_ok
    rep.append("GH-COVER %s %s" % ("PASS" if fit_ok else "FAIL",
               ", ".join("%s %s keeps %.1f%%" % (t["span"], t["src"], t["kept"]) for t in gm["tiles"])))

    # --- 5. the two container collapses, DRIVEN THROUGH THE PAGE'S OWN STAGE CONTROL.
    #        A @media query could not see that harness at all -- the viewport never changes.
    for w, want, label in (("100%", [3, 1], "12-col: hero + tall + unit, unit beneath"),
                           ("900px", [3, 1], "12-col holds, row unit shrinks"),
                           ("640px", [1, 3], "six columns: hero band over three equal tiles"),
                           ("380px", [1, 3], "three columns: same shape, shorter unit")):
        setw(w)
        g2 = pg.evaluate(GH_GEOM)
        good = g2["perRow"] == want and g2["overflow"] <= 0
        ok &= good
        rep.append("GH-CQ    %s stage=%-6s perRow=%s rowUnit=%.0f widths=%s overflow=%dpx  (%s)"
                   % ("PASS" if good else "FAIL", w, g2["perRow"], g2["rowH"],
                      g2["rowWidths"], g2["overflow"], label))

    # --- 6. NEGATIVE CONTROL: kill container-type and the 380 collapse must DISAPPEAR, proving the
    #        @container rule is load-bearing rather than coincidence.
    setw("380px")
    pg.evaluate("()=>{document.getElementById('stage').style.containerType='normal';}")
    pg.wait_for_timeout(340)
    killed = pg.evaluate(GH_GEOM)["perRow"]
    pg.evaluate("()=>{document.getElementById('stage').style.containerType='';}")
    pg.wait_for_timeout(340)
    restored = pg.evaluate(GH_GEOM)["perRow"]
    neg_ok = killed == [3, 1] and restored == [1, 3]
    ok &= neg_ok
    rep.append("GH-NEGCTL %s container-type killed -> perRow=%s (expect [3, 1], i.e. NO collapse); "
               "restored -> %s (expect [1, 3])" % ("PASS" if neg_ok else "FAIL", killed, restored))

    setw("100%")
    return ok, rep


def shoot_el(pg, name, theme, mode, width, sel, actions=None):
    """Screenshot the ELEMENT, not the viewport. A generated wall can be taller than 1100px, and a
    viewport shot of it silently crops the bottom third — which is exactly the part where a packer
    goes wrong. Element shots make the whole artefact reviewable."""
    pg.set_viewport_size({"width": width, "height": 1100})
    pg.locator('#rvTheme button[data-v="%s"]' % theme).click()
    pg.locator('#rvDark button[data-v="%s"]' % mode).click()
    pg.wait_for_timeout(120)
    if actions:
        actions(pg)
    pg.wait_for_timeout(450)
    pg.locator(sel).first.screenshot(path=os.path.join(OUT, name + ".png"))
    return name


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

        if stage in ("probe-gh", "all"):
            ok, rep = stage_masthead(pg)
            print("\n".join(rep))
            print("\nVERDICT(masthead): " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("probe-fs", "all"):
            ok, rep = stage_fullscale(pg)
            print("\n".join(rep))
            print("\nVERDICT(full-scale): " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("probe-dz", "all"):
            ok, rep = stage_designer(pg)
            print("\n".join(rep))
            print("\nVERDICT(designer): " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("probe-gen", "all"):
            ok, rep = stage_generator(pg)
            print("\n".join(rep))
            print("\nVERDICT(generator+io): " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("shots-dz",):
            def draw(q):
                """Draw five tiles with the mouse, so the shot shows the TOOL working, not a
                pre-baked arrangement pasted in."""
                q.evaluate("()=>document.getElementById('designer').scrollIntoView()")
                q.wait_for_timeout(200)
                q.locator("#dzClear").click()
                m = q.evaluate(DZ_METRICS)
                for (c0, r0, c1, r1) in ((1, 1, 7, 2), (8, 1, 12, 1), (8, 2, 12, 2),
                                         (1, 3, 4, 3), (5, 3, 12, 4)):
                    x0, y0 = _cell(m, c0, r0, 0.4, 0.4)
                    x1, y1 = _cell(m, c1, r1, 0.6, 0.6)
                    q.mouse.move(x0, y0); q.mouse.down()
                    q.mouse.move(x1, y1, steps=3); q.mouse.up()
                    q.wait_for_timeout(90)
                q.evaluate("()=>document.getElementById('dzCanvas').scrollIntoView({block:'center'})")
            shoot(pg, "v3-dz-mono-light", "mono", "light", 1400, actions=draw, clip_sel="#dzCanvas")
            shoot(pg, "v3-dz-console-light", "console", "light", 1400, actions=draw, clip_sel="#dzCanvas")
            shoot(pg, "v3-dz-supercharge-dark", "supercharge", "dark", 1400, actions=draw, clip_sel="#dzCanvas")

        if stage in ("shots-gen",):
            def gen(seed):
                def f(q):
                    q.evaluate("()=>document.getElementById('designer').scrollIntoView()")
                    q.fill("#pgSeed", str(seed))
                    q.wait_for_timeout(320)
                    q.evaluate("()=>document.getElementById('pgCanvas').scrollIntoView({block:'center'})")
                return f
            shoot_el(pg, "v3-gen-seed2026-mono-light", "mono", "light", 1400, "#pgCanvas", actions=gen(2026))
            shoot_el(pg, "v3-gen-seed7-mono-light", "mono", "light", 1400, "#pgCanvas", actions=gen(7))
            shoot_el(pg, "v3-gen-legacy-dark", "legacy", "dark", 1400, "#pgCanvas", actions=gen(2026))

        if stage in ("shots-dz2",):
            def stagew(v, seed=True):
                def f(q):
                    q.locator('#rvWidth button[data-v="%s"]' % v).click()
                    q.wait_for_timeout(400)
                    if seed:
                        q.locator("#dzSeed3").click()
                        q.wait_for_timeout(200)
                    q.evaluate("()=>document.getElementById('dzCanvas').scrollIntoView({block:'center'})")
                return f
            shoot(pg, "v3-dz-mid-900", "mono", "light", 1400, actions=stagew("900px"), clip_sel="#dzCanvas")
            shoot(pg, "v3-dz-narrow-380", "mono", "light", 1400, actions=stagew("380px"), clip_sel="#dzCanvas")

        if stage in ("shots-io",):
            def io(q):
                q.locator('#rvWidth button[data-v="100%"]').click()
                q.wait_for_timeout(300)
                q.locator("#dzSeed3").click()
                q.locator('#dzSrc button[data-v="designer"]').click()
                q.locator("#dzExport").click()
                q.wait_for_timeout(250)
                q.evaluate("()=>document.querySelector('.dz-io').scrollIntoView({block:'center'})")
            shoot(pg, "v3-export-mono-light", "mono", "light", 1400, actions=io, clip_sel=".dz-io")

        if stage in ("shots-gh", "all"):
            def gh(q):
                q.evaluate("()=>document.getElementById('gallery').scrollIntoView()")
            shoot(pg, "v4-gh-mono-light", "mono", "light", 1400, actions=gh, clip_sel="#glHead")
            shoot(pg, "v4-gh-console-dark", "console", "dark", 1400, actions=gh, clip_sel="#glHead")
            def ghnarrow(q):
                q.locator('#rvWidth button[data-v="380px"]').click()
                q.wait_for_timeout(400)
                q.evaluate("()=>document.getElementById('glHead').scrollIntoView({block:'center'})")
            shoot(pg, "v4-gh-narrow-380", "mono", "light", 1400, actions=ghnarrow, clip_sel="#glHead")
            def ghwide(q):
                q.locator('#rvWidth button[data-v="100%"]').click()
                q.wait_for_timeout(400)
                q.evaluate("()=>document.getElementById('gallery').scrollIntoView()")
            shoot(pg, "v4-gh-in-context-mono-light", "mono", "light", 1400, actions=ghwide)

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
              for f in glob.glob(OUT + "/v3-*.png") + glob.glob(OUT + "/v4-*.png"))))
        b.close()


if __name__ == "__main__":
    main()
