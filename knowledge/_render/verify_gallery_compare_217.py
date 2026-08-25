#!/usr/bin/env python3
"""
verify_gallery_compare_217.py — drives the GALLERY-COMPARE page (its generator's own OUT — #219: v2) and measures
the things candidate B can be WRONG about, in four themes x light/dark. Live document, computed
styles and measured geometry, never a read of the source.

WHY IT IS IN THE REPO (s191-D2): a verification that lives only in a sandbox is a claim, not an
instrument. This one can be re-driven when Dave rules.

⚠ IT PROVES NOTHING ABOUT WHICH CANDIDATE IS BETTER. That is Dave's call and this page is the
surface for it. What the probe proves is that the specimen he is ruling on is REAL — that B
actually justifies, actually preserves the aspect ratios, and actually switches its widows, and
that A beside it is still canon's own output rather than a drawing of it.

WHAT IT MEASURES

 1 · THE FONT, WITH CONTROLS — `document.fonts.check()` returns true in both the working and the
     broken fontconfig, so it cannot discriminate. Canvas widths, target vs two controls
     (knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL).

 2 · B JUSTIFIES — every non-widow row's tiles plus its gutters must total the container's content
     width to within 1px, at 2+ viewport widths. ⚠ MEASURED FROM THE TILES, not from the row box:
     a row box is a flex container and fills its parent whatever its children do, so measuring the
     row would return "flush" for a wall that is visibly short. The mutation arm exists because
     that is the exact green a lazy probe would produce.

 3 · NATIVE ASPECT PRESERVED — every B image box's RENDERED width/height must equal the
     manifest's own ratio to within 1%, with the manifest ratios passed in from Python. This is
     B's entire claim ("nothing is cropped") and it is the one thing a screenshot cannot settle.

 4 · ROW HEIGHT IS UNIFORM WITHIN A ROW, AND VARIES BETWEEN THEM — the first is what justification
     means; the second is reported, not asserted, because it is the visible difference Dave is
     ruling on and a range of zero would mean the wall had quietly become a fixed grid.

 5 · THE WIDOW SWITCH IS DRIVEN, both ways — unticked, every widow tile must measure ZERO boxes
     (`display:none`, no layout at all); ticked, every one must be back. ⚠ DRIVEN, not read: a
     CSS rule that exists in the stylesheet and never matches is the failure this catches. The
     widow COUNT on the page must equal the number of widow tiles in the document.

 6 · A IS STILL CANON'S OWN OUTPUT — per theme, every A wall's gutter is the theme gutter (0 in
     mono/supercharge, 24 in legacy/console), its tile radius is the theme radius, its container
     radius is 0 and its caption min-height is the ruled 86px, exactly as `s217-D3` says for the
     gallery role. If A drifts, the page stops being a comparison with the ruled thing.
     ⛔ NO BOTTOM-EDGE ASSERTION ON A. s217-D3 rules orphans acceptable in gallery; A's holes are
     COUNTED and reported, never enforced.

 7 · THE DANGLING-VAR SWEEP, ALL 8 STATES — every foreign custom property the page's stylesheet
     reads, resolved in the live document. An empty resolution is a FAILURE, not a shrug
     ([[dangling-dataviz-var-renders-silent-black]]). `--layout-bento-row-unit` is probed by name
     because B's widow width is a `calc()` on it and a dangling one would silently collapse the
     widow row to nothing.

MUTATION ARM (`--mutate`): regenerates the page with the proportional `flex-grow` zeroed — the
justify maths broken — and re-runs assertion 2. It must go RED, by name. A gate that has never
been seen to fail is not a gate ([[instrument-without-a-consumer]]).

Chunked, because sandbox bash calls die near 45 s wall:
  python3 knowledge/_render/verify_gallery_compare_217.py
  python3 knowledge/_render/verify_gallery_compare_217.py --shots /var/tmp/shots-gallery-compare
  python3 knowledge/_render/verify_gallery_compare_217.py --mutate

Env: the render runbook's staging — PLAYWRIGHT_BROWSERS_PATH · PYTHONPATH · LD_LIBRARY_PATH ·
FONTCONFIG_FILE (the /var/tmp SYMLINK FARM, never the repo TTF dir — #138) · TMPDIR.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
sys.path.insert(0, os.path.join(KNOW, "canon"))
sys.path.insert(0, HERE)
from gen_canon_bento import caption_space  # noqa: E402
from gen_gallery_compare_217 import assemble  # noqa: E402

# ⛔ #219 — THE PAGE IS THE GENERATOR'S OWN `OUT`, IMPORTED, NEVER RE-TYPED.
# The #219 re-cut emitted a successor beside the #217 page ([[feedback-version-dont-
# overwrite]]); a probe carrying its own copy of the filename would have gone on
# measuring the stale page and reporting green about a file nobody was looking at.
# One source for the name means the probe cannot address the wrong document.
sys.path.insert(0, HERE)
from gen_gallery_compare_217 import OUT as PAGE  # noqa: E402
MUTANT = PAGE.replace(".html", "-BROKEN.html")
GEN = os.path.join(HERE, "gen_gallery_compare_217.py")

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]
# ⚠ DERIVED FROM THE PAGE. main is capped at 1400 with 32px padding, so a wall measures
# viewport-64: these widths put candidate A in its 6/3/2-column bands and give B three different
# container widths to justify against.
WIDTHS = [1500, 1000, 760]
EXPECT_GUTTER = {"mono": 0, "supercharge": 0, "legacy": 24, "console": 24}
EXPECT_RADIUS = {"mono": 0, "legacy": 0, "supercharge": 0, "console": 20}
CAPTION_SPACE, CAPTION_LINES = caption_space()
FLUSH_TOL = 1.0      # px — the brief's tolerance
ASPECT_TOL = 0.01    # 1% — the brief's tolerance

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""

# --------------------------------------------------------------------------------------------
# THE B PROBE — every justified row, measured from its TILES.
# ⚠ `sum of tile widths + gutters` vs the CONTAINER's content width. Measuring the row element
# itself would be measuring a flex container, which fills its parent whatever its children do —
# it would report a broken wall as flush, which is precisely what the mutation arm proves.
# --------------------------------------------------------------------------------------------
B_PROBE = """() => {
  const wall = document.querySelector('.gc-b');
  if(!wall) return {error:'no candidate-B wall'};
  const wcs = getComputedStyle(wall);
  const inner = wall.getBoundingClientRect().width
              - (parseFloat(wcs.paddingLeft)||0) - (parseFloat(wcs.paddingRight)||0);
  const rows = Array.from(wall.querySelectorAll('.gc-brow')).map((r,i) => {
    const gap = parseFloat(getComputedStyle(r).columnGap) || 0;
    const tiles = Array.from(r.children).filter(e => e.classList.contains('gc-btile'));
    const vis = tiles.filter(t => t.getClientRects().length > 0);
    const boxes = vis.map(t => {
      const b = t.querySelector('.gc-box').getBoundingClientRect();
      return {file: t.dataset.file, ar_declared: parseFloat(t.dataset.ar),
              w: b.width, h: b.height, ar: b.height ? b.width / b.height : 0};
    });
    const total = vis.reduce((a,t) => a + t.getBoundingClientRect().width, 0)
                + Math.max(0, vis.length - 1) * gap;
    return {idx: i, widow: r.classList.contains('gc-brow--widow'),
            tiles: tiles.length, visible: vis.length, gap: gap,
            total: total, inner: inner, boxes: boxes};
  });
  return {inner: inner, rows: rows,
          gutter: Math.round(parseFloat(wcs.getPropertyValue('--bento-gutter')) || 0),
          rowUnit: wcs.getPropertyValue('--layout-bento-row-unit').trim()};
}"""

# --------------------------------------------------------------------------------------------
# THE A PROBE — candidate A must still be canon's own output, and its holes are COUNTED, never
# enforced (s217-D3 rules orphans acceptable for the gallery role).
# --------------------------------------------------------------------------------------------
A_PROBE = """(props) => {
  const px = v => Math.round(parseFloat(v) || 0);
  const num = s => s.trim() ? s.trim().split(/\\s+/).map(parseFloat) : [];
  const walls = Array.from(document.querySelectorAll('.c-bento')).filter(
      b => !b.classList.contains('gc-b')).map((b,i) => {
    const g = Array.from(b.children).find(e => e.classList.contains('c-bento__grid'));
    const cs = getComputedStyle(b);
    const tiles = g ? Array.from(g.children).filter(e => e.classList.contains('c-bento__tile')) : [];
    const t = tiles[0];
    let holes = -1, cols = -1, rows = -1, unmapped = 0;
    if(g){
      const gcs = getComputedStyle(g);
      const C = num(gcs.gridTemplateColumns), R = num(gcs.gridTemplateRows);
      const gapC = parseFloat(gcs.columnGap)||0, gapR = parseFloat(gcs.rowGap)||0;
      const gr = g.getBoundingClientRect();
      const cx=[], rx=[]; let x=0,y=0;
      for(const w of C){ cx.push(x); x += w + gapC; }
      for(const h of R){ rx.push(y); y += h + gapR; }
      const occ=[]; for(let k=0;k<R.length;k++) occ.push(new Array(C.length).fill(0));
      const near=(a,bb)=>Math.abs(a-bb)<=2.5;
      tiles.forEach(tl => {
        const r = tl.getBoundingClientRect();
        const L = r.left-gr.left, T = r.top-gr.top;
        let c0=-1,r0=-1;
        for(let k=0;k<C.length;k++) if(near(cx[k],L)){c0=k;break;}
        for(let k=0;k<R.length;k++) if(near(rx[k],T)){r0=k;break;}
        if(c0<0||r0<0){unmapped++;return;}
        let c1=c0,r1=r0;
        for(let k=c0;k<C.length;k++) if(near(cx[k]+C[k], L+r.width)){c1=k;break;}
        for(let k=r0;k<R.length;k++) if(near(rx[k]+R[k], T+r.height)){r1=k;break;}
        for(let rr=r0;rr<=r1;rr++) for(let cc=c0;cc<=c1;cc++) occ[rr][cc]=1;
      });
      holes = 0; for(const row of occ) for(const v of row) if(!v) holes++;
      cols = C.length; rows = R.length;
    }
    return {idx:i, cls:b.className, role:b.getAttribute('data-bento-role'),
            radius:px(cs.borderTopLeftRadius),
            gutter: g ? px(getComputedStyle(g).columnGap) : -1,
            tileRadius: t ? px(getComputedStyle(t).borderTopLeftRadius) : -1,
            tileBorder: t ? px(getComputedStyle(t).borderTopWidth) : -1,
            imgFit: t && t.querySelector('img') ? getComputedStyle(t.querySelector('img')).objectFit : '?',
            cols:cols, rows:rows, holes:holes, unmapped:unmapped, tiles:tiles.length};
  });
  const caps = Array.from(document.querySelectorAll('.c-bento__caption')).map(c => ({
    minH: Math.round(parseFloat(getComputedStyle(c).minHeight) || 0),
    h: Math.round(c.getBoundingClientRect().height)}));
  const cs0 = getComputedStyle(document.querySelector('.c-bento'));
  const dials = ['--bento-gutter','--bento-columns','--bento-row-unit','--bento-outer-padding',
                 '--bento-packing','--bento-radius','--layout-bento-row-unit'];
  const emptyDials = dials.filter(d => !cs0.getPropertyValue(d).trim());
  const emptyProps = props.filter(p => !getComputedStyle(document.body).getPropertyValue(p).trim());
  return {theme: document.documentElement.getAttribute('data-apollo-theme'),
          mode: document.body.getAttribute('data-theme'),
          ground: getComputedStyle(document.body).backgroundColor,
          walls: walls, caps: caps, unresolved: emptyProps.concat(emptyDials)};
}"""

WIDOW_PROBE = """() => {
  const all = Array.from(document.querySelectorAll('.gc-widow'));
  const box = document.getElementById('gc-widows');
  const label = (document.querySelector('.gc-switchrow') || {}).textContent || '';
  return {declared: all.length,
          laid_out: all.filter(t => t.getClientRects().length > 0).length,
          checked: !!(box && box.checked),
          label: label.replace(/\\s+/g,' ').trim()};
}"""


def foreign_props(src):
    """The CANON properties this page reads — derived from the page's OWN stylesheet, so the probe
    cannot drift from what ships. `--bento-*` and the page's own `--gc-*` are probed by name."""
    css = src.split("<style>", 1)[1].split("</style>", 1)[0]
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    read = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    return sorted(p for p in (read - declared)
                  if not p.startswith("--bento-") and not p.startswith("--gc-"))


def shell_path():
    for r in [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
              os.path.expanduser("~/.cache/ms-playwright")]:
        if r:
            hit = glob.glob(os.path.join(r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
            if hit:
                return hit[0]
    return None


def check_b(r, state, ratios, fails, heights):
    """Assertions 2, 3 and 4 for one state at one width."""
    if r.get("error"):
        fails.append("%s — %s" % (state, r["error"]))
        return
    for row in r["rows"]:
        tag = "%s row %d%s" % (state, row["idx"] + 1, " (widows)" if row["widow"] else "")
        if not row["visible"]:
            continue
        if not row["widow"]:
            # 2 · FLUSH
            if abs(row["total"] - row["inner"]) > FLUSH_TOL:
                fails.append("%s — ⛔ NOT JUSTIFIED: tiles+gutters total %.2fpx against a %.2fpx "
                             "container (%.2fpx short/over, tolerance %.1f). B's whole claim is "
                             "that rows end flush at both edges."
                             % (tag, row["total"], row["inner"],
                                row["total"] - row["inner"], FLUSH_TOL))
            # 4 · one height per row
            hs = [b["h"] for b in row["boxes"]]
            if hs and max(hs) - min(hs) > 1.0:
                fails.append("%s — the boxes in one justified row measure %s: a justified row has "
                             "ONE height by definition" % (tag, [round(x, 1) for x in hs]))
            if hs:
                heights.append(round(sum(hs) / len(hs), 1))
        else:
            # widows must NOT be scaled up to justify
            if row["total"] - row["inner"] > FLUSH_TOL:
                fails.append("%s — the widow row totals %.2fpx against %.2fpx: widows are being "
                             "blown up to justify, which is the behaviour the rule exists to stop"
                             % (tag, row["total"], row["inner"]))
        # 3 · NATIVE ASPECT — measured box vs the MANIFEST's ratio
        for b in row["boxes"]:
            want = ratios.get(b["file"])
            if want is None:
                fails.append("%s — a tile names %r, which is not a manifest row: the two "
                             "candidates would not be showing the same photographs"
                             % (tag, b["file"]))
                continue
            if b["h"] < 1 or b["w"] < 1:
                fails.append("%s — %s measured %.1fx%.1f: the box collapsed"
                             % (tag, b["file"], b["w"], b["h"]))
                continue
            if abs(b["ar"] - want) / want > ASPECT_TOL:
                fails.append("%s — ⛔ ASPECT LOST: %s renders %.4f, manifest says %.4f (%.2f%% "
                             "off). B's claim is that nothing is cropped; a box whose ratio is "
                             "not the picture's ratio crops it."
                             % (tag, b["file"], b["ar"], want, abs(b["ar"] - want) / want * 100))


def check_a(r, theme, state, fails, holes_seen):
    """Assertion 6 — candidate A is still canon's own output. Its RAGGEDNESS is counted only."""
    seen = 0
    for w in r["walls"]:
        tag = "%s A#%d" % (state, w["idx"])
        if w["role"] != "gallery":
            fails.append("%s — carries role %r; every wall on this page is the gallery role"
                         % (tag, w["role"]))
            continue
        seen += 1
        trial = "gc-atrial" in (w["cls"] or "")
        want_gutter = 1 if trial else EXPECT_GUTTER[theme]
        if w["gutter"] != want_gutter:
            fails.append("%s — GUTTER %spx, expected %dpx: candidate A has drifted from canon's "
                         "gallery role and the comparison is no longer against the ruled thing"
                         % (tag, w["gutter"], want_gutter))
        if w["radius"] != 0:
            fails.append("%s — CONTAINER radius %dpx; s217-D3 puts the gallery role's radius on "
                         "the TILES" % (tag, w["radius"]))
        if w["tileRadius"] != EXPECT_RADIUS[theme]:
            fails.append("%s — TILE radius %dpx, expected %dpx"
                         % (tag, w["tileRadius"], EXPECT_RADIUS[theme]))
        if trial and w["tileBorder"] != 0:
            fails.append("%s — the keyline TRIAL wall still carries a %dpx border"
                         % (tag, w["tileBorder"]))
        if not trial and w["tileBorder"] < 1:
            fails.append("%s — the ruled A wall has NO keyline: the trial has leaked into the "
                         "variant beside it" % tag)
        if w["imgFit"] != "cover":
            fails.append("%s — A's images render object-fit:%s. A's crop cost IS `cover`; a page "
                         "that quietly stopped cropping would flatter A into a different layout"
                         % (tag, w["imgFit"]))
        if w["unmapped"]:
            fails.append("%s — %d tile(s) could not be mapped onto the track lines: an unmeasured "
                         "wall must never read as square" % (tag, w["unmapped"]))
        # ⛔ NO ASSERTION on holes: s217-D3 rules them acceptable for gallery. Counted only.
        if w["holes"] > 0:
            holes_seen.append("%s:%d" % (tag, w["holes"]))
    return seen


def main():
    shots = None
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--shots":
            shots = argv[i + 1]
    if not os.path.exists(PAGE):
        sys.exit("verify_gallery_compare_217: no page — run gen_gallery_compare_217.py first")
    src = open(PAGE, encoding="utf-8").read()
    props = foreign_props(src)
    photos, rows, widows, reps, _res = assemble()
    ratios = {p["file"]: p["ar"] for p in photos}
    if shots:
        os.makedirs(shots, exist_ok=True)

    from playwright.sync_api import sync_playwright
    fails, lines, grounds, holes_seen, heights = [], [], {}, [], []
    caps_seen = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1500, "height": 1000})
        # ⛔ goto file:// ONLY. set_content() gives the document no URL, so ../knowledge/canon/
        # never resolves and the page renders with canon silently inert.
        pg.goto("file://" + PAGE + "#theme=console&m=light")
        pg.wait_for_timeout(900)
        f = pg.evaluate(FONT_PROBE)
        if not (f["target"] == f["alias_uf"] == f["alias_font"]
                and f["target"] != f["control_real"] and f["target"] != f["control_absent"]):
            print("REFUSED — the font probe cannot discriminate: %r" % f)
            b.close()
            sys.exit(1)
        print("font probe (controls pass): %r" % f)

        # ---- 1 · the eight states, at the widest viewport --------------------------------
        for theme in THEMES:
            for mode in MODES:
                pg.evaluate("h => { location.hash = h; }", "#theme=%s&m=%s" % (theme, mode))
                pg.wait_for_timeout(300)
                state = "%s/%s" % (theme, mode)
                r = pg.evaluate(A_PROBE, props)
                if r["theme"] != theme or r["mode"] != mode:
                    fails.append("%s — the hashchange did not land (got %s/%s)"
                                 % (state, r["theme"], r["mode"]))
                grounds[state] = r["ground"]
                n = check_a(r, theme, state, fails, holes_seen)
                if not r["caps"]:
                    fails.append("%s — no caption blocks: the ruled space reaches nothing" % state)
                for c in r["caps"]:
                    caps_seen += 1
                    if c["minH"] != CAPTION_SPACE:
                        fails.append("%s — caption min-height %dpx, expected the ruled %dpx. Both "
                                     "candidates must carry the SAME caption regime or the "
                                     "comparison is of two different things."
                                     % (state, c["minH"], CAPTION_SPACE))
                if r["unresolved"]:
                    fails.append("%s — ⛔ DANGLING: %s resolved EMPTY (silent-black class)"
                                 % (state, ", ".join(r["unresolved"])))
                bb = pg.evaluate(B_PROBE)
                check_b(bb, "1500px %s" % state, ratios, fails, heights)
                lines.append("  %-22s A walls %d  A gutter %s  B rows %d (%d widow)  B gutter %s"
                             % (state, n, [w["gutter"] for w in r["walls"]],
                                len(bb.get("rows", [])),
                                sum(1 for x in bb.get("rows", []) if x["widow"]),
                                bb.get("gutter")))
                if shots:
                    pg.screenshot(path=os.path.join(shots, "gc-%s-%s.png" % (theme, mode)),
                                  full_page=True)

        # ---- 2 · B justifies at MORE THAN ONE WIDTH --------------------------------------
        width_lines = []
        for width in WIDTHS:
            pg.set_viewport_size({"width": width, "height": 1000})
            pg.wait_for_timeout(260)
            for theme in ("console", "mono"):     # the 24px and the 0px gutter regimes
                pg.evaluate("h => { location.hash = h; }", "#theme=%s&m=light" % theme)
                pg.wait_for_timeout(220)
                bb = pg.evaluate(B_PROBE)
                check_b(bb, "%dpx %s/light" % (width, theme), ratios, fails, heights)
                hs = [round(sum(x["h"] for x in row["boxes"]) / max(1, len(row["boxes"])), 1)
                      for row in bb["rows"] if not row["widow"] and row["boxes"]]
                width_lines.append("  %-6s %-12s inner %.1fpx  gutter %s  row heights %s"
                                   % ("%dpx" % width, theme, bb["inner"], bb["gutter"], hs))

        # ---- 3 · the widow switch, DRIVEN both ways --------------------------------------
        pg.set_viewport_size({"width": 1500, "height": 1000})
        pg.wait_for_timeout(200)
        on = pg.evaluate(WIDOW_PROBE)
        pg.click("#gc-widows")
        pg.wait_for_timeout(200)
        off = pg.evaluate(WIDOW_PROBE)
        bb_off = pg.evaluate(B_PROBE)
        pg.click("#gc-widows")
        pg.wait_for_timeout(200)
        back = pg.evaluate(WIDOW_PROBE)
        if on["declared"] != len(widows):
            fails.append("the page declares %d widow tile(s); the packing minted %d"
                         % (on["declared"], len(widows)))
        if str(len(widows)) not in on["label"]:
            fails.append("the widow COUNT label %r does not carry the minted count %d"
                         % (on["label"], len(widows)))
        if on["laid_out"] != len(widows):
            fails.append("switch ON: %d of %d widow tiles are laid out"
                         % (on["laid_out"], len(widows)))
        if off["laid_out"] != 0:
            fails.append("⛔ THE WIDOW SWITCH DOES NOT HIDE: %d widow tile(s) still occupy layout "
                         "with the box unticked. A CSS rule that exists and never matches is the "
                         "exact failure this drive exists to catch." % off["laid_out"])
        if any(r["widow"] and r["visible"] for r in bb_off["rows"]):
            fails.append("switch OFF: the widow ROW still reports visible tiles")
        if back["laid_out"] != len(widows):
            fails.append("switch back ON: %d of %d widow tiles returned"
                         % (back["laid_out"], len(widows)))
        b.close()

    print("page: %s" % os.path.relpath(PAGE, ROOT))
    print("%d photographs, one data path; %d justified row(s) + %d widow(s) minted at %dpx target"
          % (len(photos), len(rows), len(widows), 320))
    print("caption space: %dpx -> %d line(s); %d caption block(s) measured across 8 states"
          % (CAPTION_SPACE, CAPTION_LINES, caps_seen))
    print("foreign properties probed per state (%d): %s" % (len(props), ", ".join(props)))
    print("\n".join(lines))
    print("B justified at three widths x two gutter regimes:")
    print("\n".join(width_lines))
    if heights:
        print("B row heights measured across ALL widths: %.0f–%.0fpx (the per-width ranges are the "
              "line above; one number across widths would conflate two effects)"
              % (min(heights), max(heights)))
        if max(heights) - min(heights) < 1:
            fails.append("every B row measured the same height — the wall is behaving like a "
                         "fixed grid, so it is not showing the layout being ruled on")
    print("A raggedness EXERCISED, not asserted (s217-D3 rules orphans acceptable): %s"
          % (", ".join(holes_seen[:8]) or "no holes measured"))
    print("widow switch driven: ON %d laid out · OFF %d · ON again %d  (label %r)"
          % (on["laid_out"], off["laid_out"], back["laid_out"], on["label"][:60]))
    for theme in THEMES:
        a, z = grounds["%s/light" % theme], grounds["%s/dark" % theme]
        if a == z:
            fails.append("%s — light and dark paint the SAME ground (%s): the theme did not reach "
                         "the page, or everything fell back" % (theme, a))
    if fails:
        print("\n%d FAILURE(S):" % len(fails))
        for x in fails[:60]:
            print("  ⛔ " + x)
        if len(fails) > 60:
            print("  … and %d more" % (len(fails) - 60))
        return 1
    print("\nALL GREEN — 8 states: B justifies flush to the container at 3 widths x 2 gutter "
          "regimes · native aspect preserved to 1% on every box · one height per justified row · "
          "widows unscaled and the switch driven both ways · A still canon's own output (gutter, "
          "radius, cover, caption) · A's raggedness counted not enforced · dangling sweep.")
    return 0


def mutate():
    """⬛ THE MUTATION ARM. Regenerate with the proportional flex-grow zeroed and re-run the FLUSH
    assertion. It must go RED, by name."""
    import subprocess
    r = subprocess.run([sys.executable, GEN, "--break-justify"], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(MUTANT):
        print("REFUSED — could not build the mutant page:\n%s\n%s" % (r.stdout, r.stderr))
        return 1
    photos, rows, widows, reps, _res = assemble()
    ratios = {p["file"]: p["ar"] for p in photos}
    from playwright.sync_api import sync_playwright
    fails, heights = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1500, "height": 1000})
        pg.goto("file://" + MUTANT + "#theme=console&m=light")
        pg.wait_for_timeout(800)
        check_b(pg.evaluate(B_PROBE), "MUTANT 1500px console/light", ratios, fails, heights)
        b.close()
    flush = [x for x in fails if "NOT JUSTIFIED" in x]
    print("mutant: %s" % os.path.relpath(MUTANT, ROOT))
    for x in fails[:8]:
        print("  ⛔ " + x)
    if not flush:
        print("\n⛔ THE MUTATION ARM WENT GREEN. The flush assertion cannot see a broken justify "
              "maths, so a green run on the real page proves nothing about it.")
        return 1
    print("\nMUTATION ARM RED as required — %d row(s) failed the flush assertion with the "
          "proportional flex-grow zeroed. The gate has been seen to fail." % len(flush))
    return 0


if __name__ == "__main__":
    if "--mutate" in sys.argv:
        sys.exit(mutate())
    sys.exit(main())
