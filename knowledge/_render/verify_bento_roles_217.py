#!/usr/bin/env python3
"""
verify_bento_roles_217.py — drives the BENTO-CANON roles demo (its generator's own OUT — #219: v5) in FOUR THEMES ×
LIGHT/DARK and measures the things `s217-D3` can be wrong about. Live document, computed styles
and measured geometry, never a read of the source.

WHY IT IS IN THE REPO (s191-D2): a verification that lives only in a sandbox is a claim, not an
instrument — it expires with the session. This one can be re-driven.

⚠ IT DOES NOT REPLACE `verify_bento_canon_217.py`. That probe still owns the s217-D2 page (v2)
and its assertions. This one owns the ROLE refinement and the v3 page.

WHAT IT MEASURES, PER THEME × MODE (8 states)

 1 · THE FONT, WITH CONTROLS — `document.fonts.check()` returns true in both the working and the
     broken fontconfig, so it cannot discriminate. Canvas widths, target vs two controls.
     (knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL.)

 2 · RADIUS PLACEMENT, PER ROLE — the heart of s217-D3, and three assertions per role, not one:
       dashboard    → CONTAINER radius = the theme radius (20 in console, 0 elsewhere),
                      TILE radius = 0, and the container CLIPS.
       brochureware → CONTAINER radius = 0, TILE radius = the theme radius.
       gallery      → as brochureware.
     ⚠ MEASURED IN EVERY THEME, never inferred from console. A role rule that never lands leaves
     the base grammar silently in force, and one green theme cannot tell you which case you are
     in. Console is where the number is non-zero; the other three are where an accidental
     inversion would hide.

 3 · SPACING, PER ROLE — dashboard INNER walls at 1px, the dashboard OUTER wall at the THEME
     gutter (0 in mono/supercharge, 24 in legacy/console). ⚠ THAT SPLIT IS THE ROLE. A blanket
     1px would read green on the inner walls and collapse Dave's bento-of-bentos, so the outer
     wall is asserted explicitly and against the theme's own number.
     Brochureware and gallery walls: the theme gutter.

 4 · THE SQUARING PASS, WHERE IT IS RATIFIED — for every dashboard and brochureware wall the
     RENDERED occupancy is reconstructed from measured geometry (used track sizes give the row
     and column lines; each tile's own rect is mapped back onto them) and the wall passes only
     if NO cell in rows 1..R is empty. Measured at four viewport widths, in all eight states —
     a wall square at six columns and ragged at three is the same defect, later.
     ⛔ NO BOTTOM-EDGE ASSERTION ON GALLERY. s217-D3 exempts it: orphans are acceptable there.
     What IS asserted for gallery is the tolerance itself — the wall is measured, its holes are
     REPORTED, and the run stays green with holes present. An assertion there would enforce a
     rule Dave exempted the role from in the same breath he ratified it.

 5 · PORTRAIT IS STILL TWO ROWS IN THE GALLERY — the positive half of the exemption. Squaring
     OFF and aspect-mapping ON are DIFFERENT MECHANISMS, and the failure mode of turning one off
     is quietly taking the other with it. Every `data-r="2"` gallery tile must MEASURE two rows
     wherever the wall renders at more than one column. ⚠ At one column canon rewrites every
     `data-r` to 1, so asserting two rows there would fail a page behaving exactly as ruled.

 6 · THE CAPTION SPACE — the gallery caption block must measure at least the ruled number
     (86px, s217-D3), and its computed `min-height` must BE that number, read from the token.
     Both: the rendered height proves it is not collapsed, the min-height proves the number came
     from canon rather than from content that happens to be tall.

 7 · THE TRIAL DOES NOT LEAK — measured, not read. The trial wall's tiles must have a ZERO
     border width and a 1px gutter; the ruled gallery wall's tiles beside it must have a
     NON-ZERO border and the theme gutter. ⚠ Asserting only the trial would pass a page where
     the keylines had been dropped everywhere, which is the exact accident the trial risks.

 8 · THE DANGLING-VAR SWEEP, ALL 8 STATES — every foreign custom property the page's stylesheet
     reads, resolved in the live document. An empty resolution is a FAILURE, not a shrug
     ([[dangling-dataviz-var-renders-silent-black]]). The `--bento-*` dials are probed by name as
     well, because they carry no literal fallback by design.

MUTATION ARM (`--mutate`): regenerates the page with EVERY ROLE REWRITTEN to `brochureware` and
re-runs the per-role radius and spacing assertions. They must go RED, by name — the dashboard
section loses its container radius and its 1px spacing. A gate that has never been seen to fail
is not a gate ([[instrument-without-a-consumer]]).

Chunked, because sandbox bash calls die near 45 s wall:
  python3 knowledge/_render/verify_bento_roles_217.py
  python3 knowledge/_render/verify_bento_roles_217.py --shots /var/tmp/shots-bento-roles-217
  python3 knowledge/_render/verify_bento_roles_217.py --mutate

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
from gen_canon_bento import caption_space, role_policy, roles  # noqa: E402

# ⛔ #219 — THE PAGE IS THE GENERATOR'S OWN `OUT`, IMPORTED, NEVER RE-TYPED.
# The #219 re-cut emitted a successor beside the #217 page ([[feedback-version-dont-
# overwrite]]); a probe carrying its own copy of the filename would have gone on
# measuring the stale page and reporting green about a file nobody was looking at.
# One source for the name means the probe cannot address the wrong document.
sys.path.insert(0, HERE)
from gen_bento_roles_217 import OUT as PAGE  # noqa: E402
MUTANT = PAGE.replace(".html", "-WRONGROLE.html")
GEN = os.path.join(HERE, "gen_bento_roles_217.py")

# ⚠ DERIVED FROM THE PAGE, not picked. `main` is capped at 1400 with 32px padding each side, so a
# full-width wall measures viewport-64 — which puts these four widths in the 6, 3, 2 and 1 column
# bands. 900 and 560 alone would skip the two-column band entirely.
WIDTHS = [1500, 900, 680, 560]

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]

# s217-D2: gutter is the ONLY per-theme divergence.
EXPECT_GUTTER = {"mono": 0, "supercharge": 0, "legacy": 24, "console": 24}
# border-radius/container: console overrides to 20; the other three follow the base alias (0).
EXPECT_RADIUS = {"mono": 0, "legacy": 0, "supercharge": 0, "console": 20}
TIGHT = 1          # s217-D3 dashboard inner spacing
CAPTION_SPACE, CAPTION_LINES = caption_space()

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
# THE ROLE PROBE — every bento on the page, reported BY ITS OWN ROLE ATTRIBUTE and by whether it
# is an outer wall (its tiles are themselves bentos) or a leaf wall.
# ⚠ The role is read off the DOCUMENT, not assumed from the section it sits in: that is what lets
# the mutation arm be seen — a mutated page reports `brochureware` everywhere and the expectations
# below stop matching what a dashboard must be.
# --------------------------------------------------------------------------------------------
ROLE_PROBE = """(props) => {
  const px = v => Math.round(parseFloat(v) || 0);
  const bentos = Array.from(document.querySelectorAll('.c-bento'));
  const out = bentos.map((b, i) => {
    const g = Array.from(b.children).find(e => e.classList.contains('c-bento__grid'));
    const tiles = g ? Array.from(g.children).filter(e => e.classList.contains('c-bento__tile')) : [];
    const t = tiles[0];
    const cs = getComputedStyle(b);
    return {
      idx: i,
      role: b.getAttribute('data-bento-role'),
      section: (b.closest('section') || {}).id || '?',
      cls: b.className,
      outer: tiles.some(x => x.classList.contains('c-bento')),
      gutter: g ? px(getComputedStyle(g).columnGap) : -1,
      rowGutter: g ? px(getComputedStyle(g).rowGap) : -1,
      radius: px(cs.borderTopLeftRadius),
      overflow: cs.overflowX + '/' + cs.overflowY,
      containerType: cs.containerType,
      tileRadius: t ? px(getComputedStyle(t).borderTopLeftRadius) : -1,
      tileBorder: t ? px(getComputedStyle(t).borderTopWidth) : -1,
      tracks: g ? getComputedStyle(g).gridTemplateColumns.trim().split(/\\s+/).length : -1
    };
  });
  // the gallery caption blocks — rendered height AND the computed min-height
  const caps = Array.from(document.querySelectorAll(
      '.c-bento[data-bento-role="gallery"] .c-bento__caption')).map(c => ({
    h: Math.round(c.getBoundingClientRect().height),
    minH: Math.round(parseFloat(getComputedStyle(c).minHeight) || 0),
    lines: (getComputedStyle(c.querySelector('.dx-desc') || c).getPropertyValue('-webkit-line-clamp')||'').trim()
  }));
  const anyBento = document.querySelector('.c-bento');
  const cs0 = getComputedStyle(anyBento);
  const dials = ['--bento-gutter','--bento-columns','--bento-row-unit','--bento-outer-padding',
                 '--bento-packing','--bento-radius'];
  const emptyDials = dials.filter(d => !cs0.getPropertyValue(d).trim());
  const emptyProps = props.filter(p => !getComputedStyle(document.body).getPropertyValue(p).trim());
  return {
    theme: document.documentElement.getAttribute('data-apollo-theme'),
    mode: document.body.getAttribute('data-theme'),
    bentos: out, caps: caps,
    ground: getComputedStyle(document.body).backgroundColor,
    unresolved: emptyProps.concat(emptyDials)
  };
}"""

# --------------------------------------------------------------------------------------------
# THE WALL PROBE — reconstructs each wall's RENDERED occupancy from measured geometry.
# ⚠ WHY NOT READ `data-c`/`data-r`: those are what the generator INTENDED. The band rules rewrite
# them and a stale stylesheet would ignore them. `unmapped`/`overlap` are reported, because a tile
# that cannot be placed on the track lines means the MEASUREMENT failed — which must never read
# as "no holes".
# --------------------------------------------------------------------------------------------
WALL_PROBE = """() => {
  const num = s => s.trim() ? s.trim().split(/\\s+/).map(parseFloat) : [];
  function occupancy(grid){
    const cs = getComputedStyle(grid);
    const cols = num(cs.gridTemplateColumns), rows = num(cs.gridTemplateRows);
    if(!cols.length || !rows.length) return null;
    const gapC = parseFloat(cs.columnGap)||0, gapR = parseFloat(cs.rowGap)||0;
    const gr = grid.getBoundingClientRect();
    const padL = parseFloat(cs.paddingLeft)||0, padT = parseFloat(cs.paddingTop)||0;
    const cx=[], rx=[];
    let x=0; for(const w of cols){ cx.push(x); x += w + gapC; }
    let y=0; for(const h of rows){ rx.push(y); y += h + gapR; }
    const C=cols.length, R=rows.length;
    const occ=[]; for(let i=0;i<R;i++) occ.push(new Array(C).fill(0));
    const near=(a,b)=>Math.abs(a-b)<=2.5;
    let unmapped=0, overlap=0;
    const tiles=Array.from(grid.children).filter(e=>e.classList.contains('c-bento__tile'));
    const spans=[];
    tiles.forEach(t=>{
      const r=t.getBoundingClientRect();
      const L=r.left-gr.left-padL, T=r.top-gr.top-padT;
      let c0=-1,r0=-1;
      for(let i=0;i<C;i++) if(near(cx[i],L)) { c0=i; break; }
      for(let i=0;i<R;i++) if(near(rx[i],T)) { r0=i; break; }
      if(c0<0||r0<0){ unmapped++; spans.push(null); return; }
      let c1=c0, r1=r0;
      for(let i=c0;i<C;i++) if(near(cx[i]+cols[i], L+r.width)) { c1=i; break; }
      for(let i=r0;i<R;i++) if(near(rx[i]+rows[i], T+r.height)) { r1=i; break; }
      for(let rr=r0; rr<=r1; rr++) for(let cc=c0; cc<=c1; cc++){
        if(occ[rr][cc]) overlap++; occ[rr][cc]=1; }
      spans.push({el:t, c:c1-c0+1, r:r1-r0+1});
    });
    let holes=0; for(const row of occ) for(const v of row) if(!v) holes++;
    return {cols:C, rows:R, holes:holes, unmapped:unmapped, overlap:overlap,
            tiles:tiles.length, spanList:spans};
  }
  const walls = Array.from(document.querySelectorAll('.c-bento')).map((b,i)=>{
    const g = Array.from(b.children).find(e=>e.classList.contains('c-bento__grid'));
    const o = g ? occupancy(g) : null;
    // ✅ s217-D7 — IS THIS WALL A NESTED ONE? An inner bento is a `.c-bento` with a `.c-bento`
    // ancestor. The flag exists so the nested walls can be COUNTED: an orphan assertion that
    // never met an inner wall would be a coverage claim with no evidence behind it.
    const base = {id:((b.closest('section')||{}).id||'?')+'#'+i,
                  role:b.getAttribute('data-bento-role'),
                  nested: !!(b.parentElement && b.parentElement.closest('.c-bento')),
                  section:(b.closest('section')||{}).id||'?'};
    if(!o) return Object.assign(base, {cols:-1, rows:-1, holes:-1, unmapped:-1, overlap:-1, tiles:-1});
    // portrait tiles measured IN THIS WALL — the aspect half of the gallery ruling
    const tiles = Array.from(g.children).filter(e=>e.classList.contains('c-bento__tile'));
    const tall = [];
    o.spanList.forEach((s,j)=>{
      const el = tiles[j];
      if(el && el.getAttribute('data-r')==='2') tall.push({rows: s ? s.r : -1, cols:o.cols});
    });
    return Object.assign(base, {cols:o.cols, rows:o.rows, holes:o.holes,
                                unmapped:o.unmapped, overlap:o.overlap, tiles:o.tiles, tall:tall});
  });
  return {walls: walls};
}"""


def foreign_props(src):
    """The CANON properties this page reads — derived from the page's OWN stylesheet, so the probe
    cannot drift from what ships. The --bento-* dials are excluded here and probed by name."""
    css = src.split("<style>", 1)[1].split("</style>", 1)[0]
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    read = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    return sorted(p for p in (read - declared) if not p.startswith("--bento-"))


def shell_path():
    for r in [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
              os.path.expanduser("~/.cache/ms-playwright")]:
        if r:
            hit = glob.glob(os.path.join(r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
            if hit:
                return hit[0]
    return None


def check_roles(r, theme, state, fails):
    """Assertions 2 + 3 for every bento in one state. Returns the number of bentos checked."""
    seen = 0
    for b in r["bentos"]:
        role, tag = b["role"], "%s %s#%d" % (state, b["section"], b["idx"])
        if role not in ("dashboard", "brochureware", "gallery"):
            fails.append("%s — bento carries role %r, which s217-D3 does not rule" % (tag, role))
            continue
        seen += 1
        pol = role_policy(role)
        want_container = EXPECT_RADIUS[theme] if pol["radius"] == "container" else 0
        want_tile = EXPECT_RADIUS[theme] if pol["radius"] == "tile" else 0
        if b["radius"] != want_container:
            fails.append("%s [%s] — CONTAINER radius %dpx, expected %dpx (s217-D3 puts this "
                         "role's radius on the %s)"
                         % (tag, role, b["radius"], want_container, pol["radius"]))
        # ⚠ AN OUTER WALL'S "TILES" ARE INNER BENTOS, and an inner bento's radius is its own
        # CONTAINER radius — measuring it here would assert the opposite of the ruling. What the
        # outer wall owes is that its inner containers ARE rounded, which is checked on those
        # bentos in their own right (they appear in this same list).
        if b["outer"]:
            if b["tileRadius"] != EXPECT_RADIUS[theme]:
                fails.append("%s [%s OUTER] — its inner bento measured a %dpx radius, expected "
                             "%dpx: the outer wall's tile rule has squared off the very "
                             "containers the dashboard role exists to round"
                             % (tag, role, b["tileRadius"], EXPECT_RADIUS[theme]))
        elif b["tileRadius"] != want_tile:
            fails.append("%s [%s] — TILE radius %dpx, expected %dpx (s217-D3 puts this role's "
                         "radius on the %s)" % (tag, role, b["tileRadius"], want_tile, pol["radius"]))
        if pol["radius"] == "container" and "hidden" not in b["overflow"]:
            fails.append("%s [%s] — the container does not CLIP (overflow %s): square tile "
                         "corners will poke through the curve" % (tag, role, b["overflow"]))
        if "inline-size" not in (b["containerType"] or ""):
            fails.append("%s [%s] — container-type is %r: the bands would answer the window, not "
                         "the wall, and nesting would not isolate"
                         % (tag, role, b["containerType"]))
        # --- spacing ------------------------------------------------------------------------
        # ⚠ THE DASHBOARD SPLIT. Tight INSIDE the inner walls; the OUTER wall (its tiles are
        # themselves bentos) keeps the theme gutter — asserted explicitly, because a blanket 1px
        # reads green on the inner walls and collapses the structure the role exists to describe.
        if role == "dashboard" and not b["outer"]:
            want_gutter = TIGHT
        else:
            want_gutter = EXPECT_GUTTER[theme]
        # a page-local instance dial may legitimately override the gutter; only the TRIAL does.
        if "dx-trial" in (b["cls"] or ""):
            want_gutter = 1
        if b["gutter"] != want_gutter or b["rowGutter"] != want_gutter:
            fails.append("%s [%s%s] — GUTTER %s/%s, expected %d"
                         % (tag, role, " OUTER" if b["outer"] else "",
                            b["gutter"], b["rowGutter"], want_gutter))
        # --- 7 · the trial must not leak, and the ruled variant must not be bare -------------
        if role == "gallery" and b["tileBorder"] >= 0:
            if "dx-trial" in (b["cls"] or ""):
                if b["tileBorder"] != 0:
                    fails.append("%s — the TRIAL wall's tiles still carry a %dpx keyline; the "
                                 "specimen is not showing what Dave asked to see"
                                 % (tag, b["tileBorder"]))
            elif b["tileBorder"] < 1:
                fails.append("%s — the RULED gallery wall's tiles have NO keyline (%dpx). The "
                             "trial has leaked into the variant beside it, so the comparison "
                             "Dave is ruling on is of a thing with itself"
                             % (tag, b["tileBorder"]))
    return seen


def main():
    shots = None
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--shots":
            shots = argv[i + 1]
    if not os.path.exists(PAGE):
        sys.exit("verify_bento_roles_217: no page — run gen_bento_roles_217.py first (%s)" % PAGE)
    props = foreign_props(open(PAGE, encoding="utf-8").read())
    if shots:
        os.makedirs(shots, exist_ok=True)

    from playwright.sync_api import sync_playwright
    fails, lines, grounds = [], [], {}
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

        for theme in THEMES:
            for mode in MODES:
                pg.evaluate("h => { location.hash = h; }", "#theme=%s&m=%s" % (theme, mode))
                pg.wait_for_timeout(320)
                r = pg.evaluate(ROLE_PROBE, props)
                state = "%s/%s" % (theme, mode)
                grounds[state] = r["ground"]
                if r["theme"] != theme or r["mode"] != mode:
                    fails.append("%s — the hashchange did not land (got %s/%s)"
                                 % (state, r["theme"], r["mode"]))
                n = check_roles(r, theme, state, fails)
                # --- 6 · the caption space ------------------------------------------------
                if not r["caps"]:
                    fails.append("%s — no gallery caption blocks found: the ruled space reaches "
                                 "nothing" % state)
                for c in r["caps"]:
                    caps_seen += 1
                    if c["minH"] != CAPTION_SPACE:
                        fails.append("%s — caption min-height %dpx, expected %dpx (s217-D3). The "
                                     "ruled number did not reach the page from the token store."
                                     % (state, c["minH"], CAPTION_SPACE))
                    if c["h"] < CAPTION_SPACE:
                        fails.append("%s — caption block RENDERS %dpx, below the ruled %dpx — the "
                                     "space is being collapsed by something above it"
                                     % (state, c["h"], CAPTION_SPACE))
                # --- 8 · dangling ----------------------------------------------------------
                if r["unresolved"]:
                    fails.append("%s — ⛔ DANGLING: %s resolved EMPTY (silent-black class)"
                                 % (state, ", ".join(r["unresolved"])))
                by_role = {}
                for x in r["bentos"]:
                    by_role.setdefault(x["role"], []).append(x)
                lines.append("  %-22s %d bentos  dash c/t %s  broch c/t %s  gal c/t %s  "
                             "dash gutters %s  gal gutter %s"
                             % (state, n,
                                _ct(by_role.get("dashboard")), _ct(by_role.get("brochureware")),
                                _ct(by_role.get("gallery")),
                                [x["gutter"] for x in by_role.get("dashboard", [])],
                                [x["gutter"] for x in by_role.get("gallery", [])]))
                if shots:
                    pg.screenshot(path=os.path.join(shots, "roles-%s-%s.png" % (theme, mode)),
                                  full_page=True)

        # ---- 4 + 5 · the bottom edge (where ratified) and the portrait spans ----------------
        wall_lines, gallery_holes_seen, tall_seen = [], 0, 0
        nested_seen, nested_holes = 0, 0        # ✅ s217-D7 coverage, counted not assumed
        for width in WIDTHS:
            pg.set_viewport_size({"width": width, "height": 1000})
            pg.wait_for_timeout(220)
            for theme in THEMES:
                for mode in MODES:
                    pg.evaluate("h => { location.hash = h; }", "#theme=%s&m=%s" % (theme, mode))
                    pg.wait_for_timeout(200)
                    w = pg.evaluate(WALL_PROBE)
                    state = "%dpx %s/%s" % (width, theme, mode)
                    for wl in w["walls"]:
                        squared = role_policy(wl["role"])["squaring"] \
                            if wl["role"] in ("dashboard", "brochureware", "gallery") else True
                        if wl["unmapped"] or wl["overlap"] or wl["cols"] < 0:
                            fails.append("%s — %s [%s]: the MEASUREMENT failed (%s unmapped, %s "
                                         "overlap) — an unmeasured wall must never read as square"
                                         % (state, wl["id"], wl["role"], wl["unmapped"],
                                            wl["overlap"]))
                            continue
                        if wl.get("nested") and squared:
                            nested_seen += 1
                            nested_holes += wl["holes"]
                        if squared and wl["holes"]:
                            fails.append("%s — ⛔ ORPHANED COMPARTMENT%s: %s [%s] has %d empty "
                                         "cell(s) in a %d×%d wall. The squaring pass is RATIFIED "
                                         "for this role (s217-D3%s) and did not hold."
                                         % (state, " (NESTED)" if wl.get("nested") else "",
                                            wl["id"], wl["role"], wl["holes"],
                                            wl["rows"], wl["cols"],
                                            ", extended to inner walls by s217-D7"
                                            if wl.get("nested") else ""))
                        if not squared:
                            # ⛔ NO ASSERTION. Ragged is RULED ACCEPTABLE here; the holes are
                            # counted so the tolerance is exercised and visible, never enforced.
                            gallery_holes_seen += wl["holes"]
                        # 5 · portrait tiles still measure two rows above the one-column band
                        for t in wl.get("tall") or []:
                            tall_seen += 1
                            if t["cols"] > 1 and t["rows"] != 2:
                                fails.append("%s — %s [%s]: a data-r=2 tile MEASURED %d row(s) at "
                                             "%d columns. s217-D2's portrait mapping is a "
                                             "DIFFERENT mechanism from squaring and must survive "
                                             "the gallery exemption."
                                             % (state, wl["id"], wl["role"], t["rows"], t["cols"]))
                    if theme == "console" and mode == "light":
                        wall_lines.append(
                            "  %-6s walls %2d  squared-role holes %d  gallery holes %s"
                            % ("%dpx" % width, len(w["walls"]),
                               sum(x["holes"] for x in w["walls"]
                                   if x["role"] != "gallery" and x["holes"] > 0),
                               [x["holes"] for x in w["walls"] if x["role"] == "gallery"]))
        # ✅ s217-D7 — THE COVERAGE CLAIM NEEDS POSITIVE EVIDENCE. The orphan assertion above walks
        # every `.c-bento`, inner ones included; if it never MET one, a green run would say nothing
        # about nested walls at all ([[unmatched-grep-is-not-an-absence]]).
        if not nested_seen:
            fails.append("no NESTED wall was measured in any state — s217-D7 rules the squaring "
                         "pass ON for inner bentos and this run carries no evidence that any "
                         "inner wall was looked at")
        if not tall_seen:
            fails.append("no two-row tile was measured anywhere — the portrait half of the "
                         "gallery ruling has no positive evidence, so a green run proves nothing "
                         "about it")
        b.close()

    print("page: %s" % os.path.relpath(PAGE, ROOT))
    print("roles ruled: %s" % ", ".join(sorted(k for k in roles() if not k.startswith("$"))))
    print("caption space: %dpx -> %d line(s); %d caption block(s) measured across 8 states"
          % (CAPTION_SPACE, CAPTION_LINES, caps_seen))
    print("foreign properties probed per state (%d): %s" % (len(props), ", ".join(props)))
    print("\n".join(lines))
    print("bottom edge (console/light shown; measured in all 8 states at each width):")
    print("\n".join(wall_lines))
    print("gallery raggedness EXERCISED, not asserted: %d hole(s) counted across all states — "
          "s217-D3 rules that acceptable." % gallery_holes_seen)
    print("✅ s217-D7 nested squaring: %d inner wall measurement(s) across all states, %d empty "
          "cell(s) — inner bentos run the pass." % (nested_seen, nested_holes))
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
    print("\nALL GREEN — 8 states: per-role radius placement + clip · per-role spacing (incl. the "
          "dashboard inner/outer split) · squaring where ratified · gallery ragged-tolerance "
          "exercised · portrait two-row survives the exemption · caption space · trial does not "
          "leak · dangling sweep.")
    return 0


def _ct(group):
    if not group:
        return "-"
    return "/".join("%d:%d" % (x["radius"], x["tileRadius"]) for x in group[:1]) \
        + ("+%d" % (len(group) - 1) if len(group) > 1 else "")


def mutate():
    """⬛ THE MUTATION ARM FOR THE ROLE SELECTOR. Regenerate the page with every role rewritten to
    `brochureware` and re-run the per-role assertions. They must go RED, by name."""
    import subprocess
    r = subprocess.run([sys.executable, GEN, "--wrong-role"], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(MUTANT):
        print("REFUSED — could not build the mutant page:\n%s\n%s" % (r.stdout, r.stderr))
        return 1
    props = foreign_props(open(MUTANT, encoding="utf-8").read())
    from playwright.sync_api import sync_playwright
    fails = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1500, "height": 1000})
        pg.goto("file://" + MUTANT + "#theme=console&m=light")
        pg.wait_for_timeout(800)
        # ⚠ THE EXPECTATIONS ARE THE PAGE'S OWN STRUCTURE, not the mutant's attributes. The
        # dashboard section is still a bento-of-bentos; only its ROLE was falsified. So the probe
        # asks what the dashboard section MUST look like and finds it does not.
        r = pg.evaluate(ROLE_PROBE, props)
        for x in r["bentos"]:
            if x["section"] != "dashboard":
                continue
            if x["outer"]:
                continue
            if x["radius"] != EXPECT_RADIUS["console"]:
                fails.append("dashboard#%d — CONTAINER radius %dpx, expected %dpx"
                             % (x["idx"], x["radius"], EXPECT_RADIUS["console"]))
            if x["gutter"] != TIGHT:
                fails.append("dashboard#%d — inner GUTTER %dpx, expected %dpx"
                             % (x["idx"], x["gutter"], TIGHT))
            if x["tileRadius"] != 0:
                fails.append("dashboard#%d — TILE radius %dpx, expected 0"
                             % (x["idx"], x["tileRadius"]))
        b.close()
    # ⚠ The mutant has to live in reviews/ — the page reaches canon.css by `../knowledge/…`, so a
    # copy anywhere else renders with canon silently inert and would measure nothing. It is
    # removed again here so a deliberately broken page cannot be mistaken for a review artefact.
    try:
        os.remove(MUTANT)
        removed = "removed after measuring"
    except OSError as e:                                             # noqa: BLE001
        removed = "⚠ COULD NOT REMOVE (%s) — delete it by hand, it is not a review" % e
    print("mutant: %s (%s)" % (os.path.relpath(MUTANT, ROOT), removed))
    for h in fails[:12]:
        print("  ⛔ " + h)
    if not fails:
        print("\n❌ MUTATION ARM FAILED — with every role rewritten to `brochureware` the per-role "
              "assertions stayed GREEN. The probe cannot see the defect it exists to catch, so "
              "its green result on the real page proves nothing.")
        return 1
    print("\n✅ MUTATION ARM PASSES — %d role assertion(s) went red with the role selector "
          "falsified; the per-role probe is capable of failing, by name." % len(fails))
    return 0


if __name__ == "__main__":
    sys.exit(mutate() if "--mutate" in sys.argv else main())
