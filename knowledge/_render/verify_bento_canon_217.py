#!/usr/bin/env python3
"""
verify_bento_canon_217.py — drives the BENTO-CANON canon demo (its generator's own OUT — #219 seam 5: v6) in FOUR THEMES ×
LIGHT/DARK and measures the eight things s217-D2 (and the #217 squaring proposal) can be wrong
about. Live document, computed styles and measured geometry, never a read of the source.

WHY IT IS IN THE REPO (s191-D2): a verification that lives only in a sandbox is a claim, not
an instrument — it expires with the session. This one can be re-driven.

WHAT IT MEASURES, PER THEME × MODE (8 states)

 1 · THE FONT, WITH CONTROLS — `document.fonts.check()` returns true in both the working and
     the broken fontconfig, so it cannot discriminate. Canvas widths, target vs two controls.
     (knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL.)

 2 · THE GUTTER, IN EVERY THEME — the ONE per-theme bento divergence: 0 in mono and
     supercharge, 24 in legacy and console. ⚠ MEASURED IN ALL FOUR, never inferred from one:
     a theme override that never lands leaves the DNA default silently in force, and a single
     green theme cannot tell you which case you are in.

 3 · THE CONTAINER RADIUS, AND THE CLIP — s217-D2 puts the theme radius on the bento's OUTER
     CONTAINER and leaves the tiles square. So three assertions, not one: the container's
     radius (20 in console, 0 in mono/legacy/supercharge), the TILE's radius (0 everywhere —
     if a tile is rounded the ruling is inverted), and `overflow:hidden` on the container.
     ⚠ THE CLIP IS THE ONE THAT HIDES. A radius without it renders square tile corners poking
     through the curve, which reads as "the radius did not work" and is a different defect.

 4 · THE NESTED PARAMETER SETS — Dave's own example: three 1px-gutter bentos inside a
     40px-gutter outer. Measured on the live grids, in every theme: if inner values were
     inheriting from the outer (or from the theme) these numbers would move.

 5 · THE DANGLING-VAR SWEEP, ALL 8 STATES — every foreign custom property the page's own
     stylesheet reads, resolved in the live document. An empty resolution is a FAILURE, not a
     shrug ([[dangling-dataviz-var-renders-silent-black]]). The four `--bento-*` dials are
     probed by name as well, because they carry NO literal fallback by design.

 6 · THE BAND COLLAPSE — the three fixed-width walls (1000 / 780 / 460) must resolve 3, 2 and
     1 tracks, on one page at one viewport. That is the proof the bands answer the WALL and not
     the window, which is the same property that makes nesting work.

 7 · THE BOTTOM EDGE, AT EVERY BAND (#217, the squaring proposal) — for every wall marked
     `.dx-square`, the RENDERED occupancy is reconstructed from measured geometry: the grid's
     used track sizes give the row and column lines, each tile's own rect is mapped back onto
     those lines, and the wall passes only if NO cell in rows 1..R is empty. That is the
     bottom-edge assertion stated positively — a short last row and a tile hanging below the
     edge both show up as empty cells.
     ⚠ MEASURED AT THREE VIEWPORT WIDTHS (1500 / 900 / 560), in all eight states. A wall square
     at six columns and ragged at three is the SAME defect, later — checking only full width
     would let it ship. And the `.dx-ragged` control must be ragged at at least one width: a
     probe with no positive control cannot tell "square" from "not measuring".

 8 · PORTRAIT IS TWO ROWS (#217, Dave's first question) — every `.dx-shot-portrait` tile must
     measure a two-row span wherever the wall renders at more than one column. ⚠ At ONE column
     canon itself rewrites every `data-r` to 1, so asserting two rows there would fail a page
     that is behaving exactly as ruled.

MUTATION ARM (`--mutate`): regenerates the page with the squaring pass DISABLED and re-runs
assertion 7 against it. The probe must go RED, by name. A gate that has never been seen to fail
is not a gate ([[instrument-without-a-consumer]]).

Chunked, because sandbox bash calls die near 45 s wall:
  python3 knowledge/_render/verify_bento_canon_217.py
  python3 knowledge/_render/verify_bento_canon_217.py --shots /var/tmp/shots-bento-217
  python3 knowledge/_render/verify_bento_canon_217.py --mutate

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
# ⛔ #219 — THE PAGE IS THE GENERATOR'S OWN `OUT`, IMPORTED, NEVER RE-TYPED.
# The #219 re-cut emitted a successor beside the #217 page ([[feedback-version-dont-
# overwrite]]); a probe carrying its own copy of the filename would have gone on
# measuring the stale page and reporting green about a file nobody was looking at.
# One source for the name means the probe cannot address the wrong document.
sys.path.insert(0, HERE)
from gen_bento_canon_217 import OUT as PAGE  # noqa: E402
MUTANT = PAGE.replace(".html", "-NOSQUARE.html")
GEN = os.path.join(HERE, "gen_bento_canon_217.py")
# The viewport widths the wall assertions are measured at. `main` is capped at 1400 with 32px
# padding each side, so a full-width wall measures viewport-64 (or 1336 at the top) — which puts
# these four widths in the 6, 3, 2 and 1 column bands respectively. ⚠ DERIVED FROM THE PAGE, not
# picked: 900 and 560 alone would skip the two-column band entirely, and a wall can be square at
# six and three columns and ragged at two.
WIDTHS = [1500, 900, 680, 560]

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]

# s217-D2: gutter is the ONLY per-theme divergence.
EXPECT_GUTTER = {"mono": 0, "supercharge": 0, "legacy": 24, "console": 24}
# border-radius/container: console overrides to 20; the other three follow the base alias (0).
EXPECT_RADIUS = {"mono": 0, "legacy": 0, "supercharge": 0, "console": 20}
# the per-instance sets the demo declares
EXPECT_OUTER_GUTTER = 40
EXPECT_INNER_GUTTER = 1

# ⬛ #219 — the ruled caption block, READ FROM THE STORE, never typed. `caption_space()` derives the
# line allowance back out of the same number, so the probe cannot assert a space and a clamp that
# disagree.
sys.path.insert(0, os.path.join(KNOW, "canon"))
from gen_canon_bento import caption_space  # noqa: E402
CAPTION_SPACE, CAPTION_LINES = caption_space()
# ⬛ #219 seam 5 — THE PROBE WAS RE-POINTED, NOT WEAKENED. It asserted `s218-D6 (1)`'s DARK mono
# caption as two hard-typed rgb strings, mode-stable. `s219-D2 (1)` retired that ground, so the old
# assertion would have REDDED THE RULING rather than the page (the same re-point lane B made on
# `verify_photography_218`). Three things changed and each is a deliberate choice:
#   1 · The expectation is now READ OFF THE TOKEN, live, in each state — the caption's computed
#       ground must EQUAL the state's own `--surface-subtle`, which is what "the dial says grey"
#       means. Hard-typing a dark-mode rgb would have invented a value nobody ruled.
#   2 · It is NO LONGER MODE-STABLE, and that is a real consequence of the supersession: the #218
#       rider resolved #1A1A1A in mono light AND dark; `--surface-subtle` resolves rgb(240,240,240)
#       in mono light and rgb(31,31,31) in mono dark. Dark falls out of the tokens; nothing here
#       chose it.
#   3 · Mono LIGHT is additionally pinned to the pixel DAVE'S OWN EXPORT measured, so the token
#       identification cannot drift off the colour he actually saw and approved.
# ⚠ DECLARED, and it is lane B's finding 9: in mono DARK, `--surface-subtle` and `--surface-raised`
# both resolve #1F1F1F, so this assertion is honest there but not DISCRIMINATING — a page painted
# with the wrong one of the two would pass in dark and only red in light.
MONO_CAP_GROUND_TOKEN = "--surface-subtle"
MONO_CAP_INK_TOKEN = "--text-secondary"
RECEIPT_MONO_LIGHT_GROUND = "rgb(240, 240, 240)"   # s219-D2 (1), the #219 mono gallery export
UNPAINTED = "rgba(0, 0, 0, 0)"                      # what a NON-mono caption must stay
EXPECT_BANDS = [("dx-w1000", 3), ("dx-w780", 2), ("dx-w460", 1)]

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""

STATE_PROBE = """(props) => {
  const px = v => Math.round(parseFloat(v) || 0);
  const bento = document.querySelector('#defaults .c-bento');
  const grid  = document.querySelector('#defaults .c-bento__grid');
  const tile  = document.querySelector('#defaults .c-bento__tile');
  const outer = document.querySelector('#nested .c-bento.dx-outer');
  const outerGrid = outer && outer.querySelector(':scope > .c-bento__grid');
  const inners = Array.from(document.querySelectorAll('#nested .c-bento.dx-inner'));
  const bands = ['dx-w1000','dx-w780','dx-w460'].map(c => {
    const g = document.querySelector('.' + c + ' .c-bento__grid');
    return g ? getComputedStyle(g).gridTemplateColumns.trim().split(/\\s+/).length : -1;
  });
  // ⬛ #219 — THE RULED CAPTION BLOCK, MEASURED. v2's captions never consumed
  // layout/bento/caption-space (Dave: "we've also missed the extra space for captions"), so v4
  // reads the token directly. THREE readings, because two of them can each be right while the
  // page is wrong: the RENDERED height proves the block is not collapsed; the computed
  // min-height proves the number came from the token rather than from tall content; and the
  // RESOLVED token proves the cascade delivered it rather than a fallback literal standing in.
  const caps = Array.from(document.querySelectorAll('.dx-photo .dx-cap')).map(c => ({
    h: Math.round(c.getBoundingClientRect().height),
    minH: Math.round(parseFloat(getComputedStyle(c).minHeight) || 0),
    clamp: (getComputedStyle(c).getPropertyValue('-webkit-line-clamp') || '').trim(),
    ground: getComputedStyle(c).backgroundColor,
    ink: getComputedStyle(c).color
  }));
  const capToken = Math.round(parseFloat(
    getComputedStyle(document.body).getPropertyValue('--layout-bento-caption-space')) || 0);
  // ⬛ s219-D2 (1) — THE RULED CAPTION TOKENS, RESOLVED IN THIS STATE. A scratch element is used
  // rather than reading the custom property text, because a custom property returns its DECLARED
  // text ("var(--x)" or a hex) while a background-color returns the RESOLVED rgb — and only the
  // resolved value is comparable with what the caption actually paints.
  const _probe = document.createElement('div');
  _probe.style.cssText = 'position:absolute;left:-9999px;top:-9999px;' +
    'background-color:var(--surface-subtle);color:var(--text-secondary)';
  document.body.appendChild(_probe);
  const capTokens = {ground: getComputedStyle(_probe).backgroundColor,
                     ink: getComputedStyle(_probe).color};
  _probe.remove();
  const cs = getComputedStyle(bento);
  const dials = ['--bento-gutter','--bento-columns','--bento-row-unit','--bento-outer-padding',
                 '--bento-packing','--bento-radius'];
  const emptyDials = dials.filter(d => !cs.getPropertyValue(d).trim());
  const emptyProps = props.filter(p => !getComputedStyle(document.body).getPropertyValue(p).trim());
  return {
    theme: document.documentElement.getAttribute('data-apollo-theme'),
    mode: document.body.getAttribute('data-theme'),
    gutter: px(getComputedStyle(grid).columnGap),
    rowGutter: px(getComputedStyle(grid).rowGap),
    radius: px(cs.borderTopLeftRadius),
    overflow: cs.overflowX + '/' + cs.overflowY,
    containerType: cs.containerType,
    tileRadius: tile ? px(getComputedStyle(tile).borderTopLeftRadius) : -1,
    tracks: getComputedStyle(grid).gridTemplateColumns.trim().split(/\\s+/).length,
    outerGutter: outerGrid ? px(getComputedStyle(outerGrid).columnGap) : -1,
    innerGutters: inners.map(i => {
      const g = i.querySelector(':scope > .c-bento__grid');
      return g ? px(getComputedStyle(g).columnGap) : -1; }),
    innerRadii: inners.map(i => px(getComputedStyle(i).borderTopLeftRadius)),
    bands: bands,
    caps: caps,
    capToken: capToken,
    capTokens: capTokens,
    ground: getComputedStyle(document.body).backgroundColor,
    unresolved: emptyProps.concat(emptyDials)
  };
}"""


# ---------------------------------------------------------------------------------------------
# THE WALL PROBE — reconstructs each wall's RENDERED occupancy from measured geometry.
#
# ⚠ WHY NOT READ `data-c` / `data-r`. Those are what the generator INTENDED. The band rules
# rewrite them, a stale stylesheet would ignore them, and a wall can be ragged with perfectly
# correct attributes. The only honest question is where the tiles actually landed, so the tracks
# come from the grid's USED `grid-template-*` and each tile is mapped back onto them by its own
# bounding rect. `unmapped` and `overlap` are reported: a tile that cannot be placed on the track
# lines means the MEASUREMENT failed, which must never be read as "no holes".
# ---------------------------------------------------------------------------------------------
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
  function walls(sel){
    return Array.from(document.querySelectorAll(sel)).map((b,i)=>{
      const g = Array.from(b.children).find(e=>e.classList.contains('c-bento__grid'));
      const o = g ? occupancy(g) : null;
      return o ? {id:(b.id|| (b.closest('section')||{}).id || '?')+'#'+i,
                  cols:o.cols, rows:o.rows, holes:o.holes,
                  unmapped:o.unmapped, overlap:o.overlap, tiles:o.tiles}
               : {id:'?#'+i, cols:-1, rows:-1, holes:-1, unmapped:-1, overlap:-1, tiles:-1};
    });
  }
  // portrait spans, measured — reported with the wall's own column count so the caller can
  // exempt the one-column band, where canon itself rewrites every data-r to 1.
  const pg = document.querySelector('#portrait .c-bento__grid');
  let portrait = [];
  if(pg){
    const o = occupancy(pg);
    if(o) portrait = o.spanList.map((s,i)=>{
      const el = Array.from(pg.children).filter(e=>e.classList.contains('c-bento__tile'))[i];
      return {portrait: !!(el && el.classList.contains('dx-shot-portrait')),
              rows: s ? s.r : -1, cols: o.cols};
    }).filter(z=>z.portrait);
  }
  return {square: walls('.c-bento.dx-square'), ragged: walls('.c-bento.dx-ragged'),
          portrait: portrait};
}"""


def foreign_props(src):
    """The CANON properties this page reads — derived from the page's OWN stylesheet, so the
    probe cannot drift from what ships. The --bento-* dials are excluded here and probed by
    name instead (they are declared by canon, not by this page's block)."""
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


def main():
    shots = None
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--shots":
            shots = argv[i + 1]
    if not os.path.exists(PAGE):
        sys.exit("verify_bento_canon_217: no page — run gen_bento_canon_217.py first (%s)" % PAGE)
    props = foreign_props(open(PAGE, encoding="utf-8").read())
    if shots:
        os.makedirs(shots, exist_ok=True)

    from playwright.sync_api import sync_playwright
    fails, lines, grounds = [], [], {}
    caps_seen = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        # 1400 wide so the default bento's own wall sits ABOVE the 1100 band — otherwise the
        # column count under test is the band's, not the ruled one, and the probe would be
        # measuring the wrong number while looking green.
        pg = b.new_page(viewport={"width": 1500, "height": 1000})
        # ⛔ goto file:// ONLY. set_content() gives the document no URL, so ../knowledge/canon/
        # never resolves and the page renders with canon silently inert.
        pg.goto("file://" + PAGE + "#theme=mono&m=light")
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
                r = pg.evaluate(STATE_PROBE, props)
                state = "%s/%s" % (theme, mode)
                grounds[state] = r["ground"]
                if r["theme"] != theme or r["mode"] != mode:
                    fails.append("%s — the hashchange did not land (got %s/%s)"
                                 % (state, r["theme"], r["mode"]))
                # 2 · the gutter, per theme
                if r["gutter"] != EXPECT_GUTTER[theme] or r["rowGutter"] != EXPECT_GUTTER[theme]:
                    fails.append("%s — GUTTER %s/%s, expected %d (s217-D2). A theme override that "
                                 "never lands leaves the base value silently in force."
                                 % (state, r["gutter"], r["rowGutter"], EXPECT_GUTTER[theme]))
                # 3 · container radius, tile squareness, and the clip
                if r["radius"] != EXPECT_RADIUS[theme]:
                    fails.append("%s — CONTAINER RADIUS %dpx, expected %dpx"
                                 % (state, r["radius"], EXPECT_RADIUS[theme]))
                if r["tileRadius"] != 0:
                    fails.append("%s — TILE RADIUS %dpx: s217-D2 puts the radius on the container, "
                                 "never the tiles" % (state, r["tileRadius"]))
                if "hidden" not in r["overflow"]:
                    fails.append("%s — the container does not CLIP (overflow %s): square tile "
                                 "corners will poke through the curve" % (state, r["overflow"]))
                if "inline-size" not in (r["containerType"] or ""):
                    fails.append("%s — container-type is %r: the bands would answer the window, "
                                 "not the wall, and nesting would not isolate"
                                 % (state, r["containerType"]))
                # 4 · nesting — independent parameter sets
                if r["outerGutter"] != EXPECT_OUTER_GUTTER:
                    fails.append("%s — outer nested gutter %s, expected %d"
                                 % (state, r["outerGutter"], EXPECT_OUTER_GUTTER))
                if r["innerGutters"] != [EXPECT_INNER_GUTTER] * 3:
                    fails.append("%s — inner nested gutters %r, expected %r (the inner walls are "
                                 "inheriting instead of carrying their own set)"
                                 % (state, r["innerGutters"], [EXPECT_INNER_GUTTER] * 3))
                if any(x != EXPECT_RADIUS[theme] for x in r["innerRadii"]):
                    fails.append("%s — inner bento radii %r, expected %d each (each nested bento "
                                 "is a container in its own right)"
                                 % (state, r["innerRadii"], EXPECT_RADIUS[theme]))
                # 4b · #219 — THE RULED CAPTION SPACE, AND THE MONO GROUND ON TOP OF IT
                if not r["caps"]:
                    fails.append("%s — no photo caption blocks found, so the ruled caption space "
                                 "reaches nothing. That is the v2 defect Dave named, unrepaired."
                                 % state)
                if r["capToken"] != CAPTION_SPACE:
                    fails.append("%s — --layout-bento-caption-space resolves to %dpx, expected "
                                 "%dpx. The page is reading a fallback, not the token."
                                 % (state, r["capToken"], CAPTION_SPACE))
                for c in r["caps"]:
                    caps_seen += 1
                    if c["minH"] != CAPTION_SPACE:
                        fails.append("%s — caption min-height %dpx, expected the ruled %dpx "
                                     "(s217-D3, layout/bento/caption-space)"
                                     % (state, c["minH"], CAPTION_SPACE))
                    if c["h"] < CAPTION_SPACE:
                        fails.append("%s — caption block RENDERS %dpx, below the ruled %dpx: "
                                     "authored and collapsed is not enacted"
                                     % (state, c["h"], CAPTION_SPACE))
                    if c["clamp"] and c["clamp"] not in ("none", str(CAPTION_LINES)):
                        fails.append("%s — caption clamp %r, expected the DERIVED %d line(s) — "
                                     "the space and the clamp have drifted apart"
                                     % (state, c["clamp"], CAPTION_LINES))
                    # ⛔ s219-D2 (1) — MONO ONLY, AND IN BOTH MODES. Asserting it only in mono
                    # would pass a page that painted every theme's captions grey; asserting the
                    # other three keeps the scope honest.
                    tok = r.get("capTokens") or {}
                    if theme == "mono":
                        if c["ground"] != tok.get("ground"):
                            fails.append("%s — mono caption ground %s, expected this state's %s "
                                         "= %s (s219-D2(1))"
                                         % (state, c["ground"], MONO_CAP_GROUND_TOKEN,
                                            tok.get("ground")))
                        if c["ink"] != tok.get("ink"):
                            fails.append("%s — mono caption ink %s, expected this state's %s = %s "
                                         "(s219-D2(1))"
                                         % (state, c["ink"], MONO_CAP_INK_TOKEN, tok.get("ink")))
                        # …and in LIGHT, against the pixel Dave's own export resolved.
                        if mode == "light" and c["ground"] != RECEIPT_MONO_LIGHT_GROUND:
                            fails.append("%s — mono/light caption ground %s, but the #219 mono "
                                         "gallery export Dave approved resolved %s: the token "
                                         "identification has drifted off the colour he saw"
                                         % (state, c["ground"], RECEIPT_MONO_LIGHT_GROUND))
                    elif c["ground"] != UNPAINTED:
                        fails.append("%s — a NON-mono caption is painted %s and should be %s: "
                                     "s219-D2(1) is scoped to mono and this page widened it"
                                     % (state, c["ground"], UNPAINTED))
                # 5 · dangling
                if r["unresolved"]:
                    fails.append("%s — ⛔ DANGLING: %s resolved EMPTY (silent-black class)"
                                 % (state, ", ".join(r["unresolved"])))
                # 6 · bands
                got = list(zip([c for c, _ in EXPECT_BANDS], r["bands"]))
                if r["bands"] != [n for _, n in EXPECT_BANDS]:
                    fails.append("%s — BAND COLLAPSE %r, expected %r"
                                 % (state, got, EXPECT_BANDS))
                lines.append("  %-22s gutter %-3d radius %-3d tile %-2d tracks %d  outer %-3d "
                             "inner %-12s bands %-10s clip %s"
                             % (state, r["gutter"], r["radius"], r["tileRadius"], r["tracks"],
                                r["outerGutter"], str(r["innerGutters"]), str(r["bands"]),
                                r["overflow"]))
                if shots:
                    pg.screenshot(path=os.path.join(shots, "bento-%s-%s.png" % (theme, mode)))

        # ---- 7 + 8 · the bottom edge and the portrait spans, at THREE widths × 8 states ----
        wall_lines, ragged_seen, portrait_seen = [], 0, 0
        for width in WIDTHS:
            pg.set_viewport_size({"width": width, "height": 1000})
            pg.wait_for_timeout(220)
            for theme in THEMES:
                for mode in MODES:
                    pg.evaluate("h => { location.hash = h; }", "#theme=%s&m=%s" % (theme, mode))
                    pg.wait_for_timeout(200)
                    w = pg.evaluate(WALL_PROBE)
                    state = "%dpx %s/%s" % (width, theme, mode)
                    for wl in w["square"]:
                        if wl["unmapped"] or wl["overlap"] or wl["cols"] < 0:
                            fails.append("%s — %s: the MEASUREMENT failed (%d unmapped tile(s), "
                                         "%d overlap) — an unmeasured wall must never read as "
                                         "square" % (state, wl["id"], wl["unmapped"], wl["overlap"]))
                        elif wl["holes"]:
                            fails.append("%s — ⛔ ORPHANED COMPARTMENT: %s has %d empty cell(s) in "
                                         "a %d×%d wall. The bottom edge is not straight at this "
                                         "band (the squaring pass did not hold)."
                                         % (state, wl["id"], wl["holes"], wl["rows"], wl["cols"]))
                    ragged_seen += sum(1 for wl in w["ragged"] if wl["holes"] > 0)
                    for pt in w["portrait"]:
                        portrait_seen += 1
                        if pt["cols"] > 1 and pt["rows"] != 2:
                            fails.append("%s — PORTRAIT tile measured %d row(s) at %d columns, "
                                         "expected 2 (s217-D2's 1:1.15 two-row threshold did not "
                                         "reach the page)" % (state, pt["rows"], pt["cols"]))
                    if theme == "mono" and mode == "light":
                        wall_lines.append("  %-6s square walls %2d  holes %s  ragged control holes %s"
                                          % ("%dpx" % width, len(w["square"]),
                                             sum(wl["holes"] for wl in w["square"]),
                                             [wl["holes"] for wl in w["ragged"]]))
        if not ragged_seen:
            fails.append("the .dx-ragged CONTROL was never ragged at any width — the wall probe "
                         "has no positive control, so a green result cannot be distinguished "
                         "from a probe that is not measuring")
        expect_portrait = 3 * len(WIDTHS) * len(THEMES) * len(MODES)
        if portrait_seen < expect_portrait:
            fails.append("only %d portrait tile measurement(s) — expected %d (3 portraits × %d "
                         "widths × 8 states); the portrait section did not render"
                         % (portrait_seen, expect_portrait, len(WIDTHS)))
        b.close()

    print("page: %s" % os.path.relpath(PAGE, ROOT))
    print("foreign properties probed per state (%d): %s" % (len(props), ", ".join(props)))
    print("caption space: %dpx -> %d line(s); %d caption block(s) MEASURED across 8 states "
          "(rendered height + computed min-height + resolved token); mono ground %s / ink %s "
          "READ OFF THE TOKEN in each state, pinned in mono/light to Dave's own export pixel %s, "
          "and the other three REFUSED as unpainted (s219-D2(1), superseding s218-D6(1))"
          % (CAPTION_SPACE, CAPTION_LINES, caps_seen, MONO_CAP_GROUND_TOKEN, MONO_CAP_INK_TOKEN,
             RECEIPT_MONO_LIGHT_GROUND))
    print("\n".join(lines))
    print("bottom edge (mono/light shown; measured in all 8 states at each width):")
    print("\n".join(wall_lines))
    for theme in THEMES:
        a, z = grounds["%s/light" % theme], grounds["%s/dark" % theme]
        if a == z:
            fails.append("%s — light and dark paint the SAME ground (%s): the theme did not reach "
                         "the page, or everything fell back" % (theme, a))
    if fails:
        print("\n%d FAILURE(S):" % len(fails))
        for x in fails:
            print("  ⛔ " + x)
        return 1
    print("\nALL GREEN — 8 states: per-theme gutter · container radius + clip · square tiles · "
          "nested parameter sets · dangling sweep · band collapse · bottom edge at %d widths · "
          "portrait two-row." % len(WIDTHS))
    return 0


def mutate():
    """⬛ THE MUTATION ARM. Regenerate the page with the squaring pass DISABLED and re-run the
    bottom-edge assertion against it. It must go RED, by name. A gate that has never been seen
    to fail is not a gate."""
    import subprocess
    r = subprocess.run([sys.executable, GEN, "--no-square"], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(MUTANT):
        print("REFUSED — could not build the mutant page:\n%s\n%s" % (r.stdout, r.stderr))
        return 1
    from playwright.sync_api import sync_playwright
    hits = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": WIDTHS[0], "height": 1000})
        pg.goto("file://" + MUTANT + "#theme=mono&m=light")
        pg.wait_for_timeout(700)
        for width in WIDTHS:
            pg.set_viewport_size({"width": width, "height": 1000})
            pg.wait_for_timeout(250)
            w = pg.evaluate(WALL_PROBE)
            for wl in w["square"]:
                if wl["holes"] > 0:
                    hits.append("%dpx — %s: %d empty cell(s) in a %d×%d wall"
                                % (width, wl["id"], wl["holes"], wl["rows"], wl["cols"]))
        b.close()
    # ⚠ The mutant has to live in reviews/ — the page reaches canon.css by `../knowledge/...`,
    # so a copy anywhere else renders with canon silently inert and would measure nothing. It is
    # removed again here so a deliberately broken page cannot be mistaken for a review artefact.
    try:
        os.remove(MUTANT)
        removed = "removed after measuring"
    except OSError as e:                                             # noqa: BLE001
        removed = "⚠ COULD NOT REMOVE (%s) — delete it by hand, it is not a review" % e
    print("mutant: %s (%s)" % (os.path.relpath(MUTANT, ROOT), removed))
    for h in hits[:12]:
        print("  ⛔ ORPHANED COMPARTMENT: " + h)
    if not hits:
        print("\n❌ MUTATION ARM FAILED — with the squaring pass DISABLED the bottom-edge "
              "assertion stayed GREEN. The probe cannot see the defect it exists to catch, so "
              "its green result on the real page proves nothing.")
        return 1
    print("\n✅ MUTATION ARM PASSES — %d ragged wall(s) detected with the pass disabled; the "
          "bottom-edge assertion is capable of going red, by name." % len(hits))
    return 0


if __name__ == "__main__":
    sys.exit(mutate() if "--mutate" in sys.argv else main())
