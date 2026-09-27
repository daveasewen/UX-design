#!/usr/bin/env python3
"""_validate_geometry.py — the geometry gate for GENERATED pages (the #288 sloppiness class). ADVISORY.

WHY THIS EXISTS
---------------
Dave, #288 (2026-09-19, `_HANDOFF-139`:73), on the first page Apollo composed with the template
fenced off: *"we need to do something about the sloppiness and, its all about alignment spacing
and dimensions"*. What the conductor saw on that render (marked HIS, not Dave's, in the handoff):
KPI tiles with dead space below the sparklines, a half-empty programmes-table card against a
full-height decisions card, two bottom-row cards not sharing a bottom edge, a filter bar narrower
than the table it filters, and column gutters differing between the KPI row and the rows below.
Every existing gate reads CSS TEXT (`_validate_grid.py`: is the declared value a 4px multiple)
or the page's DECLARED grammar (`_validate_composition.py`: orphan cells, gap ladder). None of
them looks at where the boxes actually LANDED. This one does: it loads the page in a real browser
(Playwright, `goto('file://…')`, never `set_content`) at 1440 and 390 and measures rendered boxes.

WHAT IT MEASURES — thirteen clauses, each named for a designer
---------------------------------------------------------
A "tile" is a box the page arranges: a `.c-bento__tile`, or any painted card (its own ground,
3+ borders or a shadow) of at least 120x60 that is a child of a grid or flex container. A "wall"
is a grid/flex container holding two or more tiles. A tile that holds a wall of its own (or wears
`.c-bento`) is a GROUP; any other tile is a LEAF.

  G1 gutters     siblings at one level share one gutter: every column gutter inside one wall is
                 equal (±1px), every row gutter is equal, and sibling walls under one parent wall
                 use the same gutter.
  G1b levels     a wall that mixes GROUPS and bare LEAF cards, where the groups' inner gutter differs
                 from the wall's own gutter — the page then shows sub-spacing gutters in some rows
                 and main-spacing gutters in others (the #288 "gutters differ between the KPI row
                 and the rows below"). The ruled grammar (s217-D3, s219-D1(5)) puts leaves INSIDE
                 inner bentos; the reference bento wraps even a one-panel row as a group.
  G2 scale       every measured gutter and every tile padding is on the spacing scale: gutters of a
                 bento wall on the RULED stop set, read at run time from
                 `knowledge/_render/_bento_edit_rails.json` → `rail.spacing_stops` (s219-D1(4));
                 everything else on the canon 4px grid as `_validate_grid.py` defines it (4n, the
                 2px half-step, 1/3px hairlines, 0). G1 and G2 measure only spacing somebody
                 CHOSE: along an axis where the wall shares out free space (justify/align-content
                 space-between|around|evenly) the distance is content arithmetic and is skipped.
  G3 edges       edges that nearly line up but don't: two tiles of one wall system (the same
                 outermost wall) in different rows whose left (or right) edges differ by more than
                 1px and at most 16px; two tiles in one row whose tops differ the same way.
  G4 bottoms     a tile with nothing below it in its wall must reach the wall's bottom edge (±1px).
  G5 bar width   a filter/tool bar directly above a table (≤32px gap) must be as wide as the table
                 and share both its edges (±2px).
  G6 dead space  an empty horizontal band inside a leaf tile, between measured ink (text line boxes,
                 replaced elements, the marks inside an SVG, painted sub-boxes), of 48px or more.
  G7 overlap     two tiles that overlap, or two runs of text from different elements whose INK
                 overlaps: each line box is shrunk to its string's ink band (canvas measureText, as
                 G8) and to what survives its clipping ancestors, then a collision is >2px across
                 and >max(2px, 15% of the shorter band) deep. Text on an overlay layer (an absolute
                 or fixed box with its own ground: a menu, a popover) covers by design and is skipped;
                 so is anything in a closed <details> (checkVisibility).
  G8 clipped     GLYPH INK cut by an `overflow:hidden|clip` box. The text rect is the font box; the
                 string's real ink box comes from canvas `measureText` (actualBoundingBox vs
                 fontBoundingBox, same metrics), so a cap-trimmed label that loses only empty line
                 space is not flagged and a descender that loses half a pixel is. Bottom or top ink
                 cut ≥0.5px (bottom + the element clipping itself = the leading-trim + overflow trap,
                 ds-005); sides cut ≥2px with no `text-overflow:ellipsis` in force. Where the metric
                 does not match the rendered box, it falls back to the line box (descender glyphs
                 ≥1px, tops ≥3px) and says so.
  G9 overflow    the document is wider than the viewport (horizontal scroll) at 1440 or 390; the
                 outermost offending boxes are named.
  G10 stretched  an `<svg preserveAspectRatio="none">` scaled more than 10% differently in x and y
                 while it holds text, circles/ellipses or strokes without `non-scaling-stroke`; an
                 `<img>` drawn with `object-fit:fill` more than 10% off its natural ratio.
  G11 marks      (W4b) one series of a chart carrying a mark of one kind on EVERY one of more than
                 12 points: point glyphs (circle, ellipse, polygon, `.dv-mk`, 3–16px) grouped by
                 `data-series-group` (or fill), counted only when a line or band in the same chart
                 has exactly that many vertices (2x for a closed band) — so a scatter's points never
                 count; or one letter key repeated more than 12 times on a series that long.
  G12 lost chart (W4b) a chart (an outermost svg of at least 160x100, not `preserveAspectRatio=
                 none`) whose marks' union covers less than 35% of its own box — a ring drawn at its
                 fixed diameter in a box the tile stretched (W3b #304's first-ranked cost).

W4b REPAIRS (#304, Sun 2026-09-27) — three blind spots found on the cold runs, fixed at their cause,
each with a CAUSE LEVER (`--mutate X-…`) that restores the old reading so the selftest can prove it:
  X-lone    G6 never measured the panel of a ONE-PANEL group (a `.c-bento` tile holding one card):
            the wall walk only reaches tiles that sit two-or-more in a grid. v1013-r2's ring tile
            (1,221px, a 260px hole under the ring) read G6 = 0. Lone panels are now leaves.
  X-scroll  a scroll box was read two ways, both wrong. G7 clipped every run to the scroll box's
            VIEWPORT, so on an app-shell page (the content box scrolls, not the window) nothing below
            the inner fold could collide — thirty overlapping axis dates read 0. G8 stopped at any
            scroll box as "reachable", but content past a scroll box's START edge (left of the origin)
            is not: every "00 £m" y-label hung left of a chart's `overflow-x:auto` stage was missed.
            Now: a scroll box clips to its scroll AREA (origin to scrollable overflow); runs unrolled
            through it are compared only with runs in the same scroll frame; the page's inner scroll
            boxes are walked before measuring so lazy parts draw.
  X-own     a text run was clipped only by its ancestors, never its own element: an ellipsis title's
            hidden tail "collided" with the tag beside it (8 false G7 on the snippets, 40 on the
            showroom index once its inner scroll was read). The clean fixture carries a guard for it.

THE TOLERANCES, AND WHY THOSE NUMBERS
-------------------------------------
  ±1px (G1/G4)   fractional `fr` tracks resolve to sub-pixel edges; 1px is the rounding floor, and
                 1px is also the smallest ruled stop, so anything larger is a different gutter.
  1 < d ≤ 16 (G3) below 1px is rounding; 16px is the first ruled stop above the 4px sub-spacing
                 (s219-D1(4): 1,2,4,16,24,40). An offset under 16 reads as an accident; at 16 and
                 above it is the structural spacing the rulings use on purpose.
  48px (G6)      the largest spacing the canon ever places inside a tile is 40 (mainSpacing); 48 is
                 that plus one 8px grid step of slack. An empty band taller than that is space no
                 rule asked for.
  32px (G5)      a bar further than 32px above a table is no longer read as the table's own bar.
  10% (G10)      a 10% non-uniform scale is where circles visibly become ellipses and 12px chart
                 text reads as a different weight; it also absorbs sub-pixel box rounding.
  12 (G11)       no ruling sets a marker density (searched knowledge/_rulings.json, #304). The kit's
                 marker proforma was authored at twelve points (dv-render-line.js: "the kit's Batch-8
                 EASED marker cadence, promoted verbatim from the proforma at twelve points"), and W3b
                 (#304 §3) proposes markers off above ~12. Declared here; Dave may move it.
  35% (G12)      a ring that fits its box covers ~75% of it (its bounding square in a square box plus
                 a leader margin); a line or bar chart covers 80%+ (axes span the plot). Under 35% the
                 box is at least three times the chart. The v1013-r2 ring read 21%; the cand-r2 rings
                 lower. 0 of 137 snippet references and 0 of 138 showroom pages cross it.

VERDICT AND OUTPUT
------------------
Per page: `{"gate":"geometry", "page", "widths":{…}, "verdict":"CLEAN|FINDINGS|UNPROVEN-FONT",
"score":0-3 or null, "findings":[{clause, severity, width, where, measured, expected, fix}], "counts",
"runtime_ms", "font_ok"}` (with `--json`), plus a plain list a designer can act on (stdout, or
`--out` markdown). SCORE (the spec lane 4e executes) counts defect KINDS, not instances: one clause
at one width on one selector shape (quoted text and numbers stripped from `where`) is one kind, so
four KPI labels clipped the same way count once, as a designer would say it. 3 = no kind; 2 = no
MAJOR kind and ≤3 minor kinds; 1 = ≤2 MAJOR kinds (or more than 3 minor); 0 = 3+ MAJOR kinds.
MAJOR = G7 overlap, G8 clipped, G9 overflow, G10 stretched (a reader loses content or sees
distortion); every other clause is minor (G11 and G12 included) (the page reads, but looks unconsidered). `score` is the
score at 1440 (the CEO Common prompt asks for "wide desktop"; the widest width if 1440 was not
measured); `score_by_width` carries every width's, and `kinds` the distinct patterns with counts.
THE FACE: every render measures whether the HSBC face is really drawing (a string's width in
"<face>, monospace" against monospace — `document.fonts.check()` cannot tell, it answers true for a
system family). A fallback face moves every text box, so such a page is UNPROVEN-FONT: its findings
are listed, its score is null. In `--selftest` the fixture and mutation legs are font-independent and
still bind; the reference-bento and #288 legs are declared UNPROVEN-FONT (measured #304: under a
fallback face the reference bento gains a 50px G6 band that the HSBC face does not have).

ADVISORY. Exit 0 whatever it finds, unless `--strict` (exit 1 on any finding). Promotion to
blocking is Dave's (the #304 plan puts "blocking flips" after Tuesday).
Exit 77 COULD-NOT-ASK when Playwright or the headless shell is unavailable (the `_validate_hit_area`
convention, #209/#223) — a fact about the box, never a pass. Exit 2 on a crash or bad usage.

USAGE
  python3 knowledge/_validate_geometry.py PAGE.html [PAGE2.html …]      # 1440 and 390
  python3 knowledge/_validate_geometry.py PAGE.html --widths 1440 --json out.json --out out.md
  python3 knowledge/_validate_geometry.py --selftest     # planted-defect fixture + reference bento
                                                         # + the #288 page + a mutation per clause
  python3 knowledge/_validate_geometry.py --build        # selftest, then the tracked generated
                                                         # pages (what _build_all.py runs)
  python3 knowledge/_validate_geometry.py PAGE --mutate G6   # switch ONE clause off (mutation lever)
  python3 knowledge/_validate_geometry.py PAGE --mutate X-scroll   # restore ONE repaired blind spot (W4b)
Every finding carries `tile` ("T<n>" a tile, "L<n>" a lone panel) so a harness can count affected tiles.

At the seat: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh;
source knowledge/_render/seat_env.sh; python3 knowledge/_validate_geometry.py …` in ONE call.
The browser is `$RENDER_SHELL` when set, else the headless shell found as `_validate_hit_area` finds it.
Built #304 lane R4b. Nothing here writes unless `--json`/`--out` name a path.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import argparse, glob, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAILS = os.path.join(HERE, "_render", "_bento_edit_rails.json")
FIX_DIR = os.path.join(HERE, "_tests", "geometry")
FIX_PLANTED = os.path.join(FIX_DIR, "geometry-planted.html")
FIX_CLEAN = os.path.join(FIX_DIR, "geometry-clean.html")
REFERENCE_BENTO = os.path.join(HERE, "snippets", "Template-dashboard-bento.reference.html")
REAL_288 = os.path.join(ROOT, "notes", "_lanes", "288", "P", "composed-dashboard.html")
# The tracked generated pages the build sweeps (outputs/ is gitignored, so CI can only see these).
BUILD_SWEEP = [
    "notes/_lanes/288/P/composed-dashboard.html",
    "notes/_lanes/292/D/overview-dashboard-oneshot-v1.html",
    "dashboards/international-banking-dashboard.canon.html",
]
CLAUSES = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
# CAUSE LEVERS (W4b #304): not clauses — each restores one repaired blind spot, so the selftest can
# prove the repair is load-bearing. X-scroll: scroll boxes read as R4b read them (inner-scroll
# content dropped by G7, a scroll box's start edge never a clip for G8). X-lone: the panel of a
# one-panel group is not measured by G6.
LEVERS = {"X-scroll": "legacyScroll", "X-lone": "legacyLone", "X-own": "legacyOwn"}
# X-own: a text run is clipped only by its ANCESTORS' overflow, not its own element's (R4b's reading;
# an ellipsis title's hidden tail then "collides" with the tag beside it — 8 false G7 on the snippets).
MAJOR = {"G7", "G8", "G9", "G10"}
NAMES = {
    "G1": "unequal gutters", "G1b": "mixed wall levels", "G2": "off-scale spacing",
    "G3": "edges that nearly line up", "G4": "unshared bottom edge", "G5": "bar narrower than its table",
    "G6": "dead space in a tile", "G7": "overlap", "G8": "clipped text", "G9": "horizontal overflow",
    "G10": "stretched part", "G11": "marks on every point", "G12": "chart lost in its box",
}
# tolerances (justified in the docstring)
TOL_GUTTER = 1.0
NEAR_MIN, NEAR_MAX = 1.0, 16.0
DEAD_MIN = 48.0
BAR_TOL = 2.0
STRETCH_TOL = 0.10
MARK_MAX = 12          # G11: the kit's marker proforma was authored at twelve points (dv-render-line.js)
LOST_MIN = 0.35        # G12: a chart's ink must cover at least 35% of its own box
GRID = 4.0
GRID_EXTRA = (0.0, 1.0, 2.0, 3.0)      # 0 touching · 2 half-step · 1/3 hairlines (_validate_grid.py)


def spacing_stops():
    """The ruled bento stop set, read from its home; None when the rails file is not here."""
    try:
        with open(RAILS) as fh:
            return [float(x) for x in json.load(fh)["rail"]["spacing_stops"]]
    except (OSError, KeyError, ValueError):
        return None


# ───────────────────────────── the in-page measurement ─────────────────────────────
COLLECT_JS = r"""
(opts) => {
  opts = opts || {};
  // CAUSE LEVERS (W4b #304, the mutation test of each repaired cause): legacyScroll restores the
  // R4b reading of scroll boxes, legacyLone skips the panels of one-panel groups.
  const LEGACY_SCROLL = !!opts.legacyScroll, LEGACY_LONE = !!opts.legacyLone, LEGACY_OWN = !!opts.legacyOwn, MARK_MAX = opts.markMax || 12, LOST_MIN = opts.lostMin || 0.35;
  const vw = window.innerWidth;
  const sx = window.scrollX, sy = window.scrollY;
  const isT = s => !s || s === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(s);
  const box = el => { const r = el.getBoundingClientRect();
    return {l: r.left + sx, t: r.top + sy, r: r.right + sx, b: r.bottom + sy, w: r.width, h: r.height}; };
  const rbox = r => ({l: r.left + sx, t: r.top + sy, r: r.right + sx, b: r.bottom + sy, w: r.width, h: r.height});
  const cls = el => (typeof el.className === 'string' ? el.className : (el.getAttribute && el.getAttribute('class')) || '');
  const hasTok = (el, t) => cls(el).split(/\s+/).includes(t);
  const say = el => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    const c = cls(el).trim().split(/\s+/).filter(Boolean).slice(0, 2);
    if (c.length) s += '.' + c.join('.');
    return s;
  };
  const heading = el => {
    const h = el.querySelector('h1,h2,h3,h4,h5,h6,[class*="title"],[class*="label"],caption,legend');
    let t = (h && h.textContent) || el.textContent || '';
    return t.trim().replace(/\s+/g, ' ').slice(0, 48);
  };
  const planted = el => { const p = el.closest && el.closest('[data-planted]'); return p ? p.getAttribute('data-planted') : null; };
  const csCache = new Map();
  const CS = el => { let c = csCache.get(el); if (!c) { c = getComputedStyle(el); csCache.set(el, c); } return c; };
  const shown = el => {
    const c = CS(el);
    if (c.display === 'none' || c.visibility === 'hidden' || c.visibility === 'collapse') return false;
    let e = el; while (e && e.nodeType === 1) { if (parseFloat(CS(e).opacity) === 0) return false; e = e.parentElement; }
    // a closed <details> keeps its content laid out but never paints it (content-visibility on the
    // ::details-content slot); checkVisibility() is Chromium's own answer to "is this drawn"
    if (el.checkVisibility && !el.checkVisibility({contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true})) return false;
    const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0;
  };
  const SCROLLS = v => /auto|scroll/.test(v);
  // the box a scroll container's content can be brought into view from (doc coords): from the
  // scroll ORIGIN (padding-box start minus the current scroll offset) out to its scrollable overflow
  const scrollArea = e => { const q = box(e), c = CS(e);
    const l = q.l + (parseFloat(c.borderLeftWidth) || 0) - e.scrollLeft, t = q.t + (parseFloat(c.borderTopWidth) || 0) - e.scrollTop;
    return {l, t, r: l + e.scrollWidth, b: t + e.scrollHeight}; };
  // the part of a box that survives every clipping ancestor (overflow other than visible, any kind)
  // `own`: start at el itself — a text run is clipped by its OWN element's overflow too (a line-clamped
  // paragraph hides its third line inside itself; W4b #304, found on the showroom index)
  const visibleRect = (el, r, own) => {
    let l = r.l, t = r.t, rr = r.r, b = r.b, e = (own && !LEGACY_OWN) ? el : el.parentElement;
    while (e && e !== document.documentElement) {
      const c = CS(e);
      const sx_ = !LEGACY_SCROLL && SCROLLS(c.overflowX), sy_ = !LEGACY_SCROLL && SCROLLS(c.overflowY);
      if (sx_ || sy_) {
        // a SCROLL box: its content can be scrolled into view up to its scrollable overflow, never
        // past its START edges. Clip to the scroll AREA on a scrolling axis; above this box the only
        // question is whether the scroll box itself can be seen. (W4b #304: an app-shell page scrolls
        // an inner box; clipping to that box's VIEWPORT dropped every run below its fold, and G7 read
        // 0 on thirty colliding axis labels.)
        const sa = scrollArea(e), q = box(e), kx = sx_ ? sa : q, ky = sy_ ? sa : q;
        if (c.overflowX !== 'visible') { l = Math.max(l, kx.l); rr = Math.min(rr, kx.r); }
        if (c.overflowY !== 'visible') { t = Math.max(t, ky.t); b = Math.min(b, ky.b); }
        if (!(rr - l > 0.5 && b - t > 0.5)) return null;
        const up = visibleRect(e, q); if (!up) return null;
        // VIRT: the outermost scroll box this rect lies (partly) beyond the viewport of. Its doc
        // coordinates are where it WOULD sit, unrolled; only runs unrolled through the same box share
        // that frame (G7 compares within one frame only).
        const outside = l < q.l - 0.5 || rr > q.r + 0.5 || t < q.t - 0.5 || b > q.b + 0.5;
        return {l, t, r: rr, b, virt: up.virt || (outside ? e : null)};
      }
      if (c.overflowX !== 'visible' || c.overflowY !== 'visible') {
        const q = box(e);
        if (c.overflowX !== 'visible') { l = Math.max(l, q.l); rr = Math.min(rr, q.r); }
        if (c.overflowY !== 'visible') { t = Math.max(t, q.t); b = Math.min(b, q.b); }
      }
      if (c.position === 'fixed') break;
      e = e.parentElement;
    }
    return (rr - l > 0.5 && b - t > 0.5) ? {l, t, r: rr, b, virt: null} : null;
  };
  const effBg = el => { let e = el; while (e && e.nodeType === 1) { const b = CS(e).backgroundColor; if (!isT(b)) return b; e = e.parentElement; } return 'rgb(255, 255, 255)'; };
  const paints = (el, under) => {
    const c = CS(el); const bg = c.backgroundColor;
    if (!isT(bg) && bg !== under) return true;
    let n = 0; for (const s of ['Top', 'Right', 'Bottom', 'Left'])
      if (parseFloat(c['border' + s + 'Width']) > 0 && c['border' + s + 'Style'] !== 'none' && !isT(c['border' + s + 'Color'])) n++;
    if (n >= 3) return true;
    return !!(c.boxShadow && c.boxShadow !== 'none');
  };
  const NOT_TILE = /^(BUTTON|A|INPUT|SELECT|TEXTAREA|LABEL|SUMMARY|TABLE|THEAD|TBODY|TFOOT|TR|TD|TH|IMG|svg|SVG|CANVAS|VIDEO|IFRAME|UL|OL|LI|DL|DT|DD|P|SPAN|H1|H2|H3|H4|H5|H6)$/;
  const inFlowKids = el => [...el.children].filter(k => { const c = CS(k); return c.position !== 'absolute' && c.position !== 'fixed' && shown(k); });
  const sameRect = (a, b) => Math.abs(a.l - b.l) <= 1 && Math.abs(a.t - b.t) <= 1 && Math.abs(a.r - b.r) <= 1 && Math.abs(a.b - b.b) <= 1;
  // the same-rect chain below a box: tile → card → card body, when each fills its parent
  const chain = el => { const out = [el]; let e = el;
    for (let i = 0; i < 4; i++) { const k = inFlowKids(e); if (k.length !== 1) break; if (!sameRect(box(k[0]), box(e))) break; e = k[0]; out.push(e); }
    return out; };
  const tileMemo = new Map(), wallMemo = new Map();
  const isWallEl = el => {
    if (wallMemo.has(el)) return wallMemo.get(el);
    wallMemo.set(el, false);
    const c = CS(el); let res = false;
    if (/grid|flex/.test(c.display)) { res = inFlowKids(el).filter(k => isTile(k, el)).length >= 2; }
    wallMemo.set(el, res); return res;
  };
  const isTile = (k, parent) => {
    const key = k; if (tileMemo.has(key)) return tileMemo.get(key);
    tileMemo.set(key, false);
    let res = false;
    if (!NOT_TILE.test(k.tagName) && k.namespaceURI === 'http://www.w3.org/1999/xhtml') {
      const r = k.getBoundingClientRect();
      if (hasTok(k, 'c-bento__tile') || hasTok(k, 'c-bento')) res = true;
      else if (r.width >= 120 && r.height >= 60) {
        const under = effBg(parent);
        res = chain(k).some(e => paints(e, under)) || groupWall(k) !== null;
      }
    }
    tileMemo.set(key, res); return res;
  };
  // a tile is a GROUP if it wears .c-bento, or a wall inside it (within 3 levels) covers half its area
  const groupWall = t => {
    const tb = box(t), area = tb.w * tb.h;
    const q = [[t, 0]];
    while (q.length) { const [e, d] = q.shift(); if (d > 3) continue;
      for (const k of inFlowKids(e)) { if (isWallEl(k)) { const b = box(k); if (b.w * b.h >= 0.5 * area) return k; } q.push([k, d + 1]); } }
    return null;
  };
  const all = [...document.querySelectorAll('body *')].filter(e => e.namespaceURI === 'http://www.w3.org/1999/xhtml');
  const walls = [], wallIdx = new Map(), tiles = [], tileIdx = new Map();
  for (const el of all) { if (!shown(el)) continue; if (isWallEl(el)) { wallIdx.set(el, walls.length); walls.push(el); } }
  const W = walls.map((w, i) => {
    const kids = inFlowKids(w).filter(k => isTile(k, w));
    const b = box(w);
    const bento = hasTok(w, 'c-bento__grid') || hasTok(w, 'c-bento') || !!(w.parentElement && hasTok(w.parentElement, 'c-bento'));
    const tl = kids.map(k => {
      const ch = chain(k);
      const pads = []; for (const e of ch) { const c = CS(e); pads.push([c.paddingTop, c.paddingRight, c.paddingBottom, c.paddingLeft].map(parseFloat)); }
      const grp = hasTok(k, 'c-bento') || groupWall(k) !== null;
      const id = tiles.length; tileIdx.set(k, id);
      const t = {id, wall: i, sel: say(k), name: heading(k), rect: box(k), group: grp, pads, planted: planted(k)};
      if (grp) { const gw = groupWall(k); t.innerWall = gw; }
      tiles.push(t); return t;
    });
    let parentWall = null, e = w.parentElement;
    while (e) { if (wallIdx.has(e)) { parentWall = wallIdx.get(e); break; } e = e.parentElement; }
    const wc = CS(w);
    // the wall's OTHER in-flow children (headings, captions, loose text): a gap with one of these
    // inside it is not a gutter between two tiles
    const others = inFlowKids(w).filter(k => !tileIdx.has(k)).map(box);
    return {id: i, sel: say(w), rect: b, bento, parentWall, tiles: tl.map(t => t.id), planted: planted(w), others,
            jc: wc.justifyContent, ac: wc.alignContent, dir: wc.flexDirection, disp: wc.display};
  });
  for (const t of tiles) { if (t.innerWall !== undefined) { t.innerWall = t.innerWall ? wallIdx.get(t.innerWall) : null; } }
  // the OUTERMOST wall each tile belongs to: G3 compares edges within one wall system only
  for (const t of tiles) { let w = t.wall; while (W[w].parentWall !== null) w = W[w].parentWall; t.root = w; }
  // wall ancestry for tiles (to skip ancestor/descendant pairs)
  const tileEls = [...tileIdx.keys()];
  for (const el of tileEls) { const t = tiles[tileIdx.get(el)]; t.anc = []; let e = el.parentElement;
    while (e) { if (tileIdx.has(e)) t.anc.push(tileIdx.get(e)); e = e.parentElement; } }

  // ── ink bands inside LEAF tiles (G6) ──
  const inkOf = el => {
    const tb = box(el); const bands = [];
    const add = r => { if (r.h <= 0 || r.w <= 0) return; if (r.b < tb.t || r.t > tb.b) return; bands.push([Math.max(r.t, tb.t), Math.min(r.b, tb.b)]); };
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let n; while ((n = tw.nextNode())) { if (!n.nodeValue.trim()) continue; const p = n.parentElement; if (!p || !shown(p)) continue;
      const rg = document.createRange(); rg.selectNodeContents(n); for (const r of rg.getClientRects()) add(rbox(r)); }
    const under = effBg(el);
    const ch = new Set(chain(el));
    for (const d of el.querySelectorAll('*')) {
      if (ch.has(d) || !shown(d)) continue;
      const tag = d.tagName.toUpperCase();
      if (/^(IMG|VIDEO|CANVAS|INPUT|SELECT|TEXTAREA|BUTTON|HR|IFRAME|PROGRESS|METER)$/.test(tag)) { add(box(d)); continue; }
      if (d.namespaceURI === 'http://www.w3.org/2000/svg') {
        if (/^(path|line|polyline|polygon|circle|ellipse|text|image|use|rect)$/.test(d.tagName)) {
          const c = CS(d); if (c.display === 'none' || c.visibility === 'hidden') continue;
          const fillNone = c.fill === 'none' || isT(c.fill); const strokeNone = c.stroke === 'none' || isT(c.stroke);
          if (fillNone && strokeNone && d.tagName !== 'text' && d.tagName !== 'image' && d.tagName !== 'use') continue;
          add(box(d)); }
        continue; }
      const db = box(d);
      if (db.w * db.h >= 0.9 * tb.w * tb.h) continue;
      if (paints(d, under)) add(db);
    }
    bands.sort((a, b) => a[0] - b[0]);
    const merged = []; for (const bd of bands) { const m = merged[merged.length - 1]; if (m && bd[0] <= m[1] + 0.5) m[1] = Math.max(m[1], bd[1]); else merged.push([bd[0], bd[1]]); }
    return merged;
  };
  for (const el of tileEls) { const t = tiles[tileIdx.get(el)]; t.key = 'T' + t.id; if (!t.group) t.ink = inkOf(el); }
  // ── the LONE LEAF of a one-panel group (G6, W4b #304) ──
  // A tile wearing .c-bento with no wall inside is a GROUP of one: the reference bento wraps even a
  // one-panel row as a group. Its panel is a leaf, but the wall walk only enumerates tiles that sit
  // two-or-more in a grid, so the panel was never measured — the 351px hole under v1013-r2's ring
  // read G6 = 0. Measure the panel (the first painted or .c-bento__tile box inside, ≤4 levels),
  // or the group itself when it holds no such box.
  const leaves = [], leafIdx = new Map();
  const wallEls = [...wallIdx.keys()];
  if (!LEGACY_LONE) for (const el of tileEls) {
    const t = tiles[tileIdx.get(el)];
    if (!t.group || t.innerWall !== null) continue;
    if (wallEls.some(w => w !== el && el.contains(w))) continue;
    let leaf = null; const q = [[el, 0]];
    while (q.length && !leaf) { const [e, d] = q.shift(); if (d >= 4) continue;
      for (const k of inFlowKids(e)) {
        if (NOT_TILE.test(k.tagName) || k.namespaceURI !== 'http://www.w3.org/1999/xhtml') continue;
        const kb = box(k);
        if (kb.w >= 120 && kb.h >= 60 && (hasTok(k, 'c-bento__tile') || paints(k, effBg(e)))) { leaf = k; break; }
        q.push([k, d + 1]); } }
    const L = leaf || el;
    const pads = []; for (const e of chain(L)) { const c = CS(e); pads.push([c.paddingTop, c.paddingRight, c.paddingBottom, c.paddingLeft].map(parseFloat)); }
    const key = 'L' + leaves.length; leafIdx.set(L, key);
    leaves.push({key, of: t.id, sel: say(L), name: heading(L), rect: box(L), pads, ink: inkOf(L), planted: planted(L), lone: true});
  }
  // the tile (or lone leaf) a finding sits in, so a harness can count AFFECTED TILES, not instances
  const tileKey = el => { let e = el; while (e && e !== document.body) { if (leafIdx.has(e)) return leafIdx.get(e);
    if (tileIdx.has(e)) return 'T' + tileIdx.get(e); e = e.parentElement; } return null; };

  // ── tables and the bar above each (G5) ──
  const tables = [];
  const tabEls = [...document.querySelectorAll('table,[role="grid"],[role="table"]')].filter(e => shown(e) && !(e.parentElement && e.parentElement.closest('table,[role="grid"],[role="table"]')));
  for (const tbl of tabEls) {
    const tb = box(tbl); if (tb.w < 200) continue;
    let best = null;
    for (const c of all) {
      if (c === tbl || c.contains(tbl) || tbl.contains(c) || !shown(c)) continue;
      const b = box(c);
      if (b.b > tb.t + 1 || b.b < tb.t - 32 || b.h < 24 || b.h > 120) continue;
      if (b.r <= tb.l || b.l >= tb.r) continue;
      const cl = cls(c), role = c.getAttribute('role') || '';
      const named = /toolbar|search/.test(role) || /filter|toolbar|toolbelt|facet/i.test(cl);
      const ctl = c.querySelectorAll('button,input,select,[role="button"],a.tag,.tag,.chip').length;
      const barish = named || (ctl >= 2 && paints(c, effBg(c.parentElement || c)));
      if (!barish) continue;
      if (!best || b.b > best.b.b + 8 || (Math.abs(b.b - best.b.b) <= 8 && b.w > best.b.w)) best = {el: c, b};
    }
    tables.push({sel: say(tbl), name: heading(tbl.closest('section,article,.c-bento__tile') || tbl), rect: tb,
                 bar: best ? {sel: say(best.el), rect: best.b, planted: planted(best.el)} : null, planted: planted(tbl)});
  }

  // ── text runs: clipping (G8) and overlap (G7) ──
  const runs = [], clips = [];
  const DESC = /[gjpqyQ,;()\[\]{}|_@$µ]/;
  // [top inset, bottom inset, measured?] between a text node's font box and its string's ink box
  const inkInsets = (p, s, rectH) => { try {
    const c = CS(p); const cx = (window.__gg_ctx = window.__gg_ctx || document.createElement('canvas').getContext('2d'));
    cx.font = [c.fontStyle, c.fontWeight, c.fontSize, c.fontFamily].join(' ');
    const m = cx.measureText(c.textTransform === 'uppercase' ? s.toUpperCase() : s);
    if (Math.abs(m.fontBoundingBoxAscent + m.fontBoundingBoxDescent - rectH) > 1.5) return [0, 0, false];
    return [Math.max(0, m.fontBoundingBoxAscent - m.actualBoundingBoxAscent), Math.max(0, m.fontBoundingBoxDescent - m.actualBoundingBoxDescent), true,
            Math.max(0, -m.actualBoundingBoxLeft), Math.max(0, m.width - m.actualBoundingBoxRight)];
  } catch (e) { return [0, 0, false]; } };
  // an overlay LAYER: an absolutely/fixed-positioned ancestor that paints its own ground (a menu,
  // a popover, a tooltip). Text on a layer covers what is under it by design; it does not collide.
  const layerOf = p => { let e = p; while (e && e !== document.body) { const c = CS(e);
    if ((c.position === 'absolute' || c.position === 'fixed') && !isT(c.backgroundColor)) return e; e = e.parentElement; } return null; };
  const tw2 = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let tn; let rid = 0;
  while ((tn = tw2.nextNode())) {
    const txt = tn.nodeValue; if (!txt.trim()) continue;
    const p = tn.parentElement; if (!p || !shown(p)) continue;
    if (p.closest('script,style,noscript,template,title')) continue;
    const rg = document.createRange(); rg.selectNodeContents(tn);
    const rects = [...rg.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5).map(rbox);
    if (!rects.length) continue;
    // sr-only and friends: a 1px clip box, clip / clip-path
    let hidden = false, clipper = [], ellipsis = false, e = p;
    while (e && e !== document.documentElement) {
      const c = CS(e);
      if ((c.clip && c.clip !== 'auto') || (c.clipPath && c.clipPath !== 'none')) { const b = box(e); if (b.w <= 2 || b.h <= 2 || c.position === 'absolute') { hidden = true; break; } }
      if (c.textOverflow === 'ellipsis') ellipsis = true;
      const ox = c.overflowX, oy = c.overflowY;
      if (/hidden|clip/.test(ox) || /hidden|clip/.test(oy)) {
        const b = box(e);
        if (b.w <= 2 || b.h <= 2) { hidden = true; break; }
        const bl = parseFloat(c.borderLeftWidth) || 0, br = parseFloat(c.borderRightWidth) || 0, bt = parseFloat(c.borderTopWidth) || 0, bb = parseFloat(c.borderBottomWidth) || 0;
        clipper.push({el: e, x: /hidden|clip/.test(ox), y: /hidden|clip/.test(oy), l: b.l + bl, r: b.r - br, t: b.t + bt, b: b.b - bb});
      }
      if (/auto|scroll/.test(c.overflowX) || /auto|scroll/.test(c.overflowY)) {
        // a scroll box: content past its END edges is reachable by scrolling; content past its START
        // edges is not. A y-axis label hung left of a chart's overflow-x:auto stage is cut for good
        // ("00 £m", W3b #304) — so on a scrolling axis the scroll AREA is a clip box, start edges only.
        if (!LEGACY_SCROLL) { const sa = scrollArea(e);
          clipper.push({el: e, x: /auto|scroll/.test(c.overflowX), y: /auto|scroll/.test(c.overflowY), l: sa.l, r: sa.r, t: sa.t, b: sa.b, scroll: true}); }
        break;
      }
      e = e.parentElement;
    }
    if (hidden) continue;
    const id = rid++;
    const s = txt.trim().replace(/\s+/g, ' ');
    // only the VISIBLE part of a run can collide: text clipped away by an overflow box (a chart's
    // data table parked outside its tile, a scrolled-off cell) sits on nothing a reader sees
    // and only INK collides: shrink each line box to the string's ink band (measureText, as G8)
    const ink = inkInsets(p, s, rects[0].h);
    const layer = layerOf(p);
    const hl = rects.length === 1 && ink[2] ? ink[3] : 0, hr = rects.length === 1 && ink[2] ? ink[4] : 0;   // side bearings: one-line runs only
    for (const r of rects) {
      const v = visibleRect(p, {l: r.l + hl, t: r.t + ink[0], r: r.r - hr, b: r.b - ink[1]}, true);
      if (v) runs.push({id, p, l: v.l, t: v.t, r: v.r, b: v.b, fh: r.h - ink[0] - ink[1], layer, virt: v.virt || null});
    }
    // INK, not line box: a text rect spans the font's whole ascent+descent, so a cap-trimmed label
    // loses empty line-box space above its caps without losing a single pixel of glyph. Canvas
    // measureText gives both the font box and the string's actual ink box in the same metrics, so
    // the real glyph cut = the rect cut minus the empty inset on that side.
    const ins = inkInsets(p, s, rects[0].h);
    const insTop = ins[0], insBot = ins[1], metricOk = ins[2];
    for (const cp of clipper) {
      let bot = 0, top = 0, side = 0;
      for (const r of rects) {
        if (cp.y) { if (!cp.scroll) bot = Math.max(bot, (r.b - insBot) - cp.b); top = Math.max(top, cp.t - (r.t + insTop)); }
        if (cp.x) { side = cp.scroll ? Math.max(side, cp.l - r.l) : Math.max(side, r.r - cp.r, cp.l - r.l); }
      }
      // a line wholly outside the clip box is hidden overflow, not a glyph cut
      const wholly = rects.every(r => (cp.y && (r.t >= cp.b || r.b <= cp.t)) || (cp.x && (r.l >= cp.r || r.r <= cp.l)));
      if (wholly) continue;
      const hit = [];
      if (metricOk) {                       // measured ink: any half-pixel of glyph lost counts
        if (bot >= 0.5) hit.push(['bottom', bot]);
        if (top >= 0.5) hit.push(['top', top]);
      } else {                              // no ink metric: fall back to the line box, guarded
        if (bot >= 1 && DESC.test(s)) hit.push(['bottom', bot]);
        if (top >= 3 && /[A-Za-z0-9]/.test(s)) hit.push(['top', top]);
      }
      if (side >= 2 && !ellipsis) hit.push(['side', side]);
      if (hit.length) { clips.push({text: s.slice(0, 40), sel: say(p), clipper: say(cp.el), same: cp.el === p, scroll: !!cp.scroll, cuts: hit.map(h => [h[0], Math.round(h[1] * 10) / 10]), ink: metricOk, planted: planted(p), tile: tileKey(p)}); break; }
    }
  }
  // overlap between text runs of different elements (neither contains the other)
  const overlaps = [];
  runs.sort((a, b) => a.t - b.t);
  for (let i = 0; i < runs.length && overlaps.length < 40; i++) {
    const a = runs[i];
    for (let j = i + 1; j < runs.length; j++) {
      const b = runs[j]; if (b.t >= a.b - 2) break;
      if (a.id === b.id || a.p === b.p || a.p.contains(b.p) || b.p.contains(a.p)) continue;
      if (a.layer !== b.layer) continue;
      if (a.virt !== b.virt) continue;          // different scroll frames: unrolled coordinates are not comparable (W4b)
      const w = Math.min(a.r, b.r) - Math.max(a.l, b.l), h = Math.min(a.b, b.b) - Math.max(a.t, b.t);
      // the runs are INK bands already (a string's extreme ascender-to-descender band); two bands
      // grazing by a pixel or two need not put glyph on glyph, so a collision is more than 2px
      // and more than 15% of the shorter band, and more than 2px across.
      if (w > 2 && h > Math.max(2, 0.15 * Math.min(a.fh, b.fh))) { overlaps.push({kind: 'text', a: say(a.p) + ' "' + (a.p.textContent || '').trim().slice(0, 24) + '"', b: say(b.p) + ' "' + (b.p.textContent || '').trim().slice(0, 24) + '"', w: Math.round(w), h: Math.round(h), planted: planted(a.p) || planted(b.p), tile: tileKey(a.p) || tileKey(b.p)}); if (overlaps.length >= 40) break; }
    }
  }

  // ── charts: marks on every point (G11) and a chart lost in its own box (G12) — W4b #304 ──
  const dense = [], lost = [];
  const painted = d => { const c = CS(d); if (c.display === 'none' || c.visibility === 'hidden' || parseFloat(c.opacity) === 0) return false;
    if (d.closest('defs,clipPath,mask,marker,pattern,symbol')) return false;
    const fn = c.fill === 'none' || isT(c.fill), sn = c.stroke === 'none' || isT(c.stroke);
    return !(fn && sn) || d.tagName === 'text' || d.tagName === 'image' || d.tagName === 'use'; };
  const nverts = d => { const a = d.tagName === 'path' ? (d.getAttribute('d') || '') : (d.getAttribute('points') || '');
    return Math.floor((a.match(/-?\d*\.?\d+(?:e-?\d+)?/gi) || []).length / 2); };
  for (const s of document.querySelectorAll('svg')) {
    if (!shown(s) || (s.parentElement && s.parentElement.closest('svg'))) continue;      // outermost svg only
    const sb = box(s); if (sb.w < 160 || sb.h < 60) continue;
    const nm = heading(s.closest('figure,section,article,.c-bento__tile') || s);
    // G11: one series carrying a mark of one kind on every one of more than MARK_MAX points
    const lines = [...s.querySelectorAll('polyline,polygon,path')].filter(painted).map(nverts);
    const glyph = {}, letter = {};
    for (const d of s.querySelectorAll('circle,ellipse,polygon,rect,path')) {
      if (d.classList.contains('dv-hit') || !painted(d)) continue;
      if ((d.tagName === 'rect' || d.tagName === 'path') && !d.classList.contains('dv-mk')) continue;
      const r = d.getBoundingClientRect(); if (r.width < 3 || r.height < 3 || r.width > 16 || r.height > 16) continue;
      const g = d.closest('[data-series-group]'); const k = g ? 'g' + g.getAttribute('data-series-group') : 'f' + CS(d).fill;
      (glyph[k] = glyph[k] || []).push(d); }
    for (const d of s.querySelectorAll('text')) {
      const x = (d.textContent || '').trim(); if (!/^[A-Z]$/.test(x) || !painted(d)) continue;
      const g = d.closest('[data-series-group]'); const k = (g ? 'g' + g.getAttribute('data-series-group') : '') + x;
      (letter[k] = letter[k] || []).push(d); }
    for (const [k, ds] of Object.entries(glyph)) { const n = ds.length;
      // on EVERY point: a line or band in this chart has exactly n vertices (a line) or 2n (a closed band)
      if (n > MARK_MAX && lines.some(v => Math.abs(v - n) <= 1 || Math.abs(v - 2 * n) <= 2))
        dense.push({kind: 'marker', sel: say(s), name: nm, n, points: n, planted: planted(s), tile: tileKey(s)}); }
    for (const [k, ds] of Object.entries(letter)) { const n = ds.length;
      if (n > MARK_MAX && lines.some(v => v >= n))
        dense.push({kind: 'letter', letter: k.slice(-1), sel: say(s), name: nm, n, points: Math.max(...lines.filter(v => v >= n)), planted: planted(s), tile: tileKey(s)}); }
    // G12: the union of the chart's marks covers less than LOST_MIN of its own box
    if (sb.h >= 100 && !/^none/.test((s.getAttribute('preserveAspectRatio') || '').trim())) {
      let l = 1e9, t = 1e9, r = -1e9, b = -1e9, n = 0;
      for (const d of s.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect,text,image,use')) {
        if (d.classList.contains('dv-hit') || !painted(d)) continue;
        const q = box(d); if (q.w <= 0 && q.h <= 0) continue;
        l = Math.min(l, Math.max(q.l, sb.l)); t = Math.min(t, Math.max(q.t, sb.t)); r = Math.max(r, Math.min(q.r, sb.r)); b = Math.max(b, Math.min(q.b, sb.b)); n++; }
      if (n && r > l && b > t) { const frac = ((r - l) * (b - t)) / (sb.w * sb.h);
        if (frac < LOST_MIN) lost.push({sel: say(s), name: nm, frac: Math.round(frac * 1000) / 1000, iw: Math.round(r - l), ih: Math.round(b - t),
                                        w: Math.round(sb.w), h: Math.round(sb.h), planted: planted(s), tile: tileKey(s)}); } }
  }

  // ── horizontal overflow (G9) ──
  const docW = Math.max(document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0);
  const off = [];
  if (docW > vw + 1) {
    const contained = el => { let e = el.parentElement; while (e && e !== document.body) { const c = CS(e); if (c.overflowX !== 'visible') return true; e = e.parentElement; } return false; };
    const offs = all.filter(el => { if (!shown(el)) return false; const b = el.getBoundingClientRect(); return (b.right > vw + 1 || b.left < -1) && CS(el).position !== 'fixed' && !contained(el); });
    const set = new Set(offs);
    for (const el of offs) { if (set.has(el.parentElement)) continue; const b = box(el); off.push({sel: say(el), name: heading(el), l: Math.round(b.l), r: Math.round(b.r), w: Math.round(b.w), planted: planted(el)}); if (off.length >= 6) break; }
  }

  // ── stretched parts (G10) ──
  const stretched = [];
  for (const s of document.querySelectorAll('svg')) {
    if (!shown(s)) continue;
    const vb = s.viewBox && s.viewBox.baseVal; if (!vb || !vb.width || !vb.height) continue;
    const par = (s.getAttribute('preserveAspectRatio') || '').trim();
    if (!/^none/.test(par)) continue;
    const b = box(s); const kx = b.w / vb.width, ky = b.h / vb.height;
    const ratio = Math.max(kx, ky) / Math.min(kx, ky);
    if (ratio - 1 <= 0.10) continue;
    const shapes = s.querySelectorAll('text,circle,ellipse').length;
    let rawStroke = 0; for (const d of s.querySelectorAll('path,line,polyline,polygon,rect,circle,ellipse')) { const c = CS(d); if (!(c.stroke === 'none' || isT(c.stroke)) && parseFloat(c.strokeWidth) > 0 && c.vectorEffect !== 'non-scaling-stroke') { rawStroke++; } }
    if (!shapes && !rawStroke) continue;
    stretched.push({kind: 'svg', sel: say(s), name: heading(s.closest('section,article,figure,.c-bento__tile') || s), kx: Math.round(kx * 1000) / 1000, ky: Math.round(ky * 1000) / 1000, ratio: Math.round(ratio * 100) / 100, shapes, rawStroke, planted: planted(s)});
  }
  for (const im of document.querySelectorAll('img')) {
    if (!shown(im) || !im.naturalWidth || !im.naturalHeight) continue;
    const c = CS(im); if (c.objectFit && c.objectFit !== 'fill') continue;
    const b = box(im); const nat = im.naturalWidth / im.naturalHeight, got = b.w / b.h;
    const ratio = Math.max(nat, got) / Math.min(nat, got);
    if (ratio - 1 > 0.10) stretched.push({kind: 'img', sel: say(im), name: im.alt || '', ratio: Math.round(ratio * 100) / 100, planted: planted(im)});
  }

  // is the HSBC face really drawing? `document.fonts.check()` answers true for any family with no
  // FontFace in the set (a system font), so it cannot tell. Measure instead: the same string in
  // "<face>, monospace" and in plain monospace — equal widths mean the face fell back.
  const fontOk = (() => { try {
    const c = document.createElement('canvas').getContext('2d'); const s = 'Programmes in flight 0123456789';
    c.font = '16px monospace'; const mono = c.measureText(s).width;
    return ['Univers Next HSBC', 'HSBC_MtUnivers_Latin'].some(f => { c.font = '16px "' + f + '", monospace'; return Math.abs(c.measureText(s).width - mono) > 0.5; });
  } catch (e) { return null; } })();
  return {vw, docW, docH: document.documentElement.scrollHeight, walls: W, tiles: tiles.map(t => { const o = Object.assign({}, t); return o; }),
          tables, clips, overlaps, overflow: off, stretched, fontOk, leaves, dense, lost};
}
"""


SETTLE_JS = r"""
() => { let s = document.documentElement.scrollHeight + ':' + document.documentElement.scrollWidth;
  let acc = 0; for (const e of document.querySelectorAll('svg text, svg path, svg rect, svg circle, svg line, .c-bento__tile')) {
    const r = e.getBoundingClientRect(); acc += Math.round(r.left) * 3 + Math.round(r.top) * 7 + Math.round(r.width) + Math.round(r.height) * 5; }
  return s + ':' + acc; }
"""


# ───────────────────────────── the verdict (pure Python over the model) ─────────────────────────────
# Entry motion is CSS (DEF-003: markers fade in on staggered delays, rings sweep): a mark read mid-
# animation has a smaller box, and a staggered delay can start AFTER two equal settle reads. Finish
# every finite animation before measuring — the page's own end state, nothing restyled (W4b #304:
# a v1013-r3 ring read 162px on one pass and full size on the next).
FINISH_ANIMATIONS_JS = r"""
() => { let n = 0; for (const a of (document.getAnimations ? document.getAnimations() : [])) { try { a.finish(); n++; } catch (e) {} } return n; }
"""


INNER_WALK_JS = r"""
async () => { for (const e of document.querySelectorAll('body *')) {
    const c = getComputedStyle(e); if (!/auto|scroll/.test(c.overflowY) || e.scrollHeight <= e.clientHeight + 50) continue;
    for (let y = 0; y < e.scrollHeight; y += 700) { e.scrollTop = y; await new Promise(r => requestAnimationFrame(() => r())); }
    e.scrollTop = 0; } }
"""


def collect_opts(levers=()):
    o = {"markMax": MARK_MAX, "lostMin": LOST_MIN}
    for lv in levers:
        o[LEVERS[lv]] = True
    return o


def _r(v):
    return round(v, 1)


def _vov(a, b):
    return min(a["b"], b["b"]) - max(a["t"], b["t"])


def _hov(a, b):
    return min(a["r"], b["r"]) - max(a["l"], b["l"])


def _name(t):
    n = t.get("name") or ""
    return ("'%s'" % n) if n else t["sel"]


def _adjacent(tl, others=()):
    """Column and row gutters between neighbouring tiles of one wall: [(a, b, gap)]. A pair with
    any other in-flow child of the wall (a heading, loose text) inside the gap is not a gutter."""
    cols, rows = [], []

    def blocked(gap):
        return any(min(gap["r"], o["r"]) - max(gap["l"], o["l"]) > 0.5 and
                   min(gap["b"], o["b"]) - max(gap["t"], o["t"]) > 0.5 for o in others)

    for a in tl:
        ra = a["rect"]
        right = [b for b in tl if b is not a and b["rect"]["l"] >= ra["r"] - 0.5
                 and _vov(ra, b["rect"]) >= 0.5 * min(ra["h"], b["rect"]["h"])]
        if right:
            b = min(right, key=lambda b: b["rect"]["l"])
            rb = b["rect"]
            if not blocked({"l": ra["r"], "r": rb["l"], "t": max(ra["t"], rb["t"]), "b": min(ra["b"], rb["b"])}):
                cols.append((a, b, rb["l"] - ra["r"]))
        below = [b for b in tl if b is not a and b["rect"]["t"] >= ra["b"] - 0.5
                 and _hov(ra, b["rect"]) >= 0.5 * min(ra["w"], b["rect"]["w"])]
        if below:
            b = min(below, key=lambda b: b["rect"]["t"])
            rb = b["rect"]
            if not blocked({"l": max(ra["l"], rb["l"]), "r": min(ra["r"], rb["r"]), "t": ra["b"], "b": rb["t"]}):
                rows.append((a, b, rb["t"] - ra["b"]))
    return cols, rows


def _modal(vals):
    if not vals:
        return None
    rounded = [round(v) for v in vals]
    return max(set(rounded), key=rounded.count)


def _on_grid(v):
    v = abs(v)
    if any(abs(v - x) <= 0.25 for x in GRID_EXTRA):
        return True
    return abs(v / GRID - round(v / GRID)) * GRID <= 0.25


_DISTRIBUTE = ("space-between", "space-around", "space-evenly")


def _distributed(w):
    """(columns distributed?, rows distributed?) — where the container SHARES OUT free space, the
    distance between two tiles is content arithmetic, not a spacing anybody chose; G1/G2 measure
    only spacing somebody chose. A flex column's main axis is vertical."""
    col_axis = w.get("jc", "") if not ("flex" in w.get("disp", "") and "column" in w.get("dir", "")) else w.get("ac", "")
    row_axis = w.get("ac", "") if not ("flex" in w.get("disp", "") and "column" in w.get("dir", "")) else w.get("jc", "")
    return any(d in (col_axis or "") for d in _DISTRIBUTE), any(d in (row_axis or "") for d in _DISTRIBUTE)


def judge(model, width, off=(), stops=None):
    """Return the findings for one page at one width. `off` switches clauses off (mutation lever)."""
    F = []
    tiles = model["tiles"]
    walls = model["walls"]
    T = {t["id"]: t for t in tiles}

    def add(clause, where, measured, expected, fix, planted=None, tile=None):
        if clause in off:
            return
        F.append({"clause": clause, "name": NAMES[clause],
                  "severity": "major" if clause in MAJOR else "minor", "width": width,
                  "where": where, "measured": measured, "expected": expected, "fix": fix,
                  "planted": planted, "tile": tile})

    gut = {}
    for w in walls:
        tl = [T[i] for i in w["tiles"]]
        cols, rows = _adjacent(tl, w.get("others", ()))
        dc, dr = _distributed(w)
        cols, rows = ([] if dc else cols), ([] if dr else rows)
        gut[w["id"]] = (cols, rows)
        # G1 within one wall
        for kind, pairs in (("column", cols), ("row", rows)):
            vals = [g for _, _, g in pairs]
            if len(vals) >= 2 and max(vals) - min(vals) > TOL_GUTTER:
                lo = min(pairs, key=lambda p: p[2]); hi = max(pairs, key=lambda p: p[2])
                add("G1", "%s (%s)" % (w["sel"], ", ".join(sorted({_name(p[0]) for p in pairs}))[:120]),
                    "%s gutters range %gpx–%gpx: %gpx between %s and %s, %gpx between %s and %s"
                    % (kind, _r(lo[2]), _r(hi[2]), _r(lo[2]), _name(lo[0]), _name(lo[1]),
                       _r(hi[2]), _name(hi[0]), _name(hi[1])),
                    "one %s gutter for every tile in this wall" % kind,
                    "Set one gap on the wall and remove per-tile margins, so every %s gutter is the same."
                    % kind,
                    planted=lo[0].get("planted") or hi[0].get("planted") or hi[1].get("planted") or w.get("planted"))
    # G1 sibling walls under one parent wall
    by_parent = {}
    for w in walls:
        if w["parentWall"] is not None:
            by_parent.setdefault(w["parentWall"], []).append(w)
    for pid, sibs in by_parent.items():
        modes = [(w, _modal([g for _, _, g in gut[w["id"]][0]])) for w in sibs]
        modes = [(w, m) for w, m in modes if m is not None]
        if len({m for _, m in modes}) > 1:
            add("G1", "walls inside %s" % walls[pid]["sel"],
                "sibling walls use different column gutters: " + ", ".join(
                    "%s %gpx" % (w["sel"], m) for w, m in modes),
                "sibling walls at one level share one gutter",
                "Give every inner wall at this level the same gap (the theme's sub-spacing).",
                planted=next((w.get("planted") for w, _ in modes if w.get("planted")), None))
    # G1b mixed levels
    for w in walls:
        tl = [T[i] for i in w["tiles"]]
        groups = [t for t in tl if t["group"]]
        leaves = [t for t in tl if not t["group"]]
        if not groups or not leaves:
            continue
        cols, rows = gut[w["id"]]
        own = _modal([g for _, _, g in cols + rows])
        inner = [_modal([g for _, _, g in gut[t["innerWall"]][0] + gut[t["innerWall"]][1]])
                 for t in groups if t.get("innerWall") is not None and t["innerWall"] in gut]
        inner = [m for m in inner if m is not None]
        if own is None or not inner or all(abs(m - own) <= TOL_GUTTER for m in inner):
            continue
        add("G1b", "%s" % w["sel"],
            "this wall holds %d nested wall(s) (inner gutter %s) beside %d bare card(s) (%s) at the wall's own %gpx gutter"
            % (len(groups), "/".join("%gpx" % m for m in sorted(set(inner))), len(leaves),
               ", ".join(_name(t) for t in leaves)[:120], own),
            "every row of one wall at the same level: bare cards go inside an inner wall",
            "Wrap the bare cards in an inner bento like their neighbours, so every row shows the same gutter.",
            planted=next((t.get("planted") for t in leaves if t.get("planted")), w.get("planted")))
    # G2 scale
    seen = set()
    for w in walls:
        cols, rows = gut[w["id"]]
        for a, b, g in cols + rows:
            if g < -0.5:
                continue
            if w["bento"] and stops:
                ok = any(abs(g - s) <= 0.25 for s in stops) or abs(g) <= 0.25
                scale = "the ruled bento stops %s" % "/".join("%g" % s for s in stops)
            else:
                ok = _on_grid(g)
                scale = "the 4px grid (4n, 2px half-step, 1/3px hairlines)"
            key = ("gap", w["id"], round(g, 1))
            if not ok and key not in seen:
                seen.add(key)
                add("G2", "%s, between %s and %s" % (w["sel"], _name(a), _name(b)),
                    "gutter %gpx" % _r(g), "a gutter on %s" % scale,
                    "Snap this gap to the nearest step on %s." % scale,
                    planted=a.get("planted") or b.get("planted") or w.get("planted"))
        for t in (T[i] for i in w["tiles"]):
            for pads in t["pads"]:
                bad = [p for p in pads if not _on_grid(p)]
                if bad:
                    key = ("pad", t["sel"], tuple(pads))
                    if key in seen:
                        break
                    seen.add(key)
                    add("G2", "%s padding" % _name(t), "padding %s" % " ".join("%gpx" % _r(p) for p in pads),
                        "padding on the 4px grid", "Snap the tile padding to the 4px grid (e.g. 16 or 24).",
                        planted=t.get("planted"))
                    break
    # G3 near-miss edges (page-wide, not ancestor/descendant)
    reported = set()
    for i, a in enumerate(tiles):
        for b in tiles[i + 1:]:
            if b["id"] in a.get("anc", []) or a["id"] in b.get("anc", []):
                continue
            if a.get("root") != b.get("root"):
                continue
            ra, rb = a["rect"], b["rect"]
            if _vov(ra, rb) <= 0:   # different rows: compare left and right edges
                for side in ("l", "r"):
                    d = abs(ra[side] - rb[side])
                    if NEAR_MIN < d <= NEAR_MAX:
                        key = (side, round(min(ra[side], rb[side])), round(max(ra[side], rb[side])))
                        if key in reported:
                            continue
                        reported.add(key)
                        add("G3", "%s and %s" % (_name(a), _name(b)),
                            "%s edges at x=%g and x=%g, %gpx apart" % ("left" if side == "l" else "right",
                                                                     _r(ra[side]), _r(rb[side]), _r(d)),
                            "edges in one column line up exactly (or differ by a deliberate ≥16px)",
                            "Put both on the same column line: use one column grid for both rows.",
                            planted=a.get("planted") or b.get("planted"))
            elif _vov(ra, rb) > 0 and _hov(ra, rb) <= 0:   # one row: compare tops
                d = abs(ra["t"] - rb["t"])
                if NEAR_MIN < d <= NEAR_MAX:
                    key = ("t", round(min(ra["t"], rb["t"])), round(max(ra["t"], rb["t"])))
                    if key not in reported:
                        reported.add(key)
                        add("G3", "%s and %s" % (_name(a), _name(b)),
                            "tops at y=%g and y=%g, %gpx apart" % (_r(ra["t"]), _r(rb["t"]), _r(d)),
                            "tiles in one row share a top edge",
                            "Align the row's tops (align-items: stretch/start on the wall).",
                            planted=a.get("planted") or b.get("planted"))
    # G4 unshared bottom edge
    for w in walls:
        tl = [T[i] for i in w["tiles"]]
        if len(tl) < 2:
            continue
        floor = max(t["rect"]["b"] for t in tl)
        for t in tl:
            r = t["rect"]
            below = [u for u in tl if u is not t and u["rect"]["t"] >= r["b"] - 0.5 and _hov(r, u["rect"]) > 1]
            if below:
                continue
            d = floor - r["b"]
            if d > TOL_GUTTER:
                nb = max(tl, key=lambda u: u["rect"]["b"])
                add("G4", "%s in %s" % (_name(t), w["sel"]),
                    "ends at y=%g, %gpx above the wall's bottom edge (%s ends at y=%g)"
                    % (_r(r["b"]), _r(d), _name(nb), _r(floor)),
                    "the last tile in each column reaches the wall's bottom edge",
                    "Stretch this tile to the row (align-self: stretch) or rebalance the row so both end together.",
                    planted=t.get("planted"))
    # G5 bar narrower than its table
    for tb in model["tables"]:
        bar = tb.get("bar")
        if not bar:
            continue
        a, b = bar["rect"], tb["rect"]
        dl, dr = abs(a["l"] - b["l"]), abs(a["r"] - b["r"])
        if dl > BAR_TOL or dr > BAR_TOL:
            add("G5", "%s above %s (%s)" % (bar["sel"], tb["sel"], tb.get("name", "")[:40]),
                "bar %gpx wide (x=%g–%g) over a %gpx table (x=%g–%g)"
                % (_r(a["w"]), _r(a["l"]), _r(a["r"]), _r(b["w"]), _r(b["l"]), _r(b["r"])),
                "the bar spans its table, both edges",
                "Make the filter bar full width of the table it filters (width:100% in the same column).",
                planted=bar.get("planted") or tb.get("planted"))
    # G6 dead space in a leaf tile — and in the lone panel of a one-panel group (W4b #304)
    for t in [t for t in tiles if not t["group"]] + list(model.get("leaves") or []):
        if not t.get("ink"):
            continue
        r = t["rect"]
        pads = t["pads"]
        pt = max(p[0] for p in pads); pb = max(p[2] for p in pads)
        ink = t["ink"]
        gaps = [(ink[0][0] - (r["t"] + pt), "above the first content")]
        gaps += [(ink[i + 1][0] - ink[i][1], "between content blocks at y=%g and y=%g"
                  % (_r(ink[i][1]), _r(ink[i + 1][0]))) for i in range(len(ink) - 1)]
        gaps.append(((r["b"] - pb) - ink[-1][1], "below the last content (y=%g)" % _r(ink[-1][1])))
        g, where = max(gaps, key=lambda x: x[0])
        if g >= DEAD_MIN:
            add("G6", "%s (%gx%g)" % (_name(t), _r(r["w"]), _r(r["h"])),
                "%gpx of empty band %s" % (_r(g), where),
                "no empty band of %gpx or more inside a tile" % DEAD_MIN,
                "Let the tile hug its content, fill it (a chart that fills its tile), or give the row a shorter tile.",
                planted=t.get("planted"), tile=t.get("key"))
    # G7 overlap: tiles, then text
    for i, a in enumerate(tiles):
        for b in tiles[i + 1:]:
            if b["id"] in a.get("anc", []) or a["id"] in b.get("anc", []):
                continue
            w, h = _hov(a["rect"], b["rect"]), _vov(a["rect"], b["rect"])
            if w > 1 and h > 1:
                add("G7", "%s and %s" % (_name(a), _name(b)), "boxes overlap by %gx%gpx" % (_r(w), _r(h)),
                    "tiles never overlap", "Remove the negative margin / fixed height that pushes one tile over the other.",
                    planted=a.get("planted") or b.get("planted"))
    for o in model["overlaps"]:
        add("G7", "%s over %s" % (o["a"], o["b"]), "text runs overlap by %dx%dpx" % (o["w"], o["h"]),
            "text never sits on other text", "Give the labels room (wrap, shorten, or move one).",
            planted=o.get("planted"), tile=o.get("tile"))
    # G8 clipped text
    for c in model["clips"]:
        cuts = ", ".join("%s %gpx" % (s, v) for s, v in c["cuts"])
        trap = " — the leading-trim + overflow trap (ds-005)" if c["same"] and any(s == "bottom" for s, _ in c["cuts"]) else ""
        if c.get("scroll"):
            add("G8", "'%s' in %s (cut at the start edge of scroll box %s)" % (c["text"], c["sel"], c["clipper"]),
                "glyph ink cut: %s — past the scroll origin, where no scrolling can reach it" % cuts,
                "no glyph cut by an overflow box",
                "Give the label room inside its box (a chart: fit the axis gutter to the widest label, data-pl-fit).",
                planted=c.get("planted"), tile=c.get("tile"))
            continue
        add("G8", "'%s' in %s (clipped by %s)" % (c["text"], c["sel"], c["clipper"]),
            "glyph ink cut: %s%s%s" % (cuts, trap, "" if c.get("ink") else " (line-box reading: no ink metric)"),
            "no glyph cut by an overflow box",
            "Add `text-box-edge: text text` to a truncating label, or drop `overflow:hidden` / the fixed height.",
            planted=c.get("planted"), tile=c.get("tile"))
    # G9 overflow
    if model["docW"] > model["vw"] + 1:
        names = "; ".join("%s %s (x=%d–%d)" % (o["sel"], ("'%s'" % o["name"][:30]) if o["name"] else "", o["l"], o["r"])
                          for o in model["overflow"]) or "no single box named"
        add("G9", "page at %dpx" % model["vw"],
            "document is %dpx wide in a %dpx viewport — it scrolls sideways; widest: %s"
            % (model["docW"], model["vw"], names),
            "no horizontal scroll at 1440 or 390",
            "Let the named box shrink (min-width:0, max-width:100%) or wrap its table in a scroll box.",
            planted=next((o.get("planted") for o in model["overflow"] if o.get("planted")), None))
    # G10 stretched
    for s in model["stretched"]:
        if s["kind"] == "svg":
            meas = "scaled x%g by y%g (%gx off), %d text/circle and %d raw-stroke mark(s) distorted" % (
                s["kx"], s["ky"], s["ratio"], s["shapes"], s["rawStroke"])
        else:
            meas = "drawn %gx off its natural ratio" % s["ratio"]
        add("G10", "%s %s" % (s["sel"], ("in '%s'" % s["name"][:36]) if s.get("name") else ""),
            meas, "parts keep their proportions (≤10%% non-uniform)",
            "Let the chart re-derive its geometry for the box (the fit engine) instead of preserveAspectRatio=\"none\"; for images use object-fit:cover.",
            planted=s.get("planted"))
    # G11 marks on every point of a dense series (W4b #304)
    for d in model.get("dense") or []:
        what = "point markers" if d["kind"] == "marker" else "copies of the letter key '%s'" % d.get("letter", "")
        add("G11", "%s in '%s'" % (d["sel"], d["name"][:36]),
            "%d %s on one series of %d points" % (d["n"], what, d["points"]),
            "at most %d marks of one kind on one series (above that, one end key and no point markers)" % MARK_MAX,
            "Drop the per-point markers above %d points; key each series once, at the line's end." % MARK_MAX,
            planted=d.get("planted"), tile=d.get("tile"))
    # G12 a chart lost in its own box (W4b #304)
    for x in model.get("lost") or []:
        add("G12", "%s in '%s'" % (x["sel"], x["name"][:36]),
            "the chart's ink covers %d%% of its box (ink %gx%g in a %gx%g box)" % (round(100 * x["frac"]), x["iw"], x["ih"], x["w"], x["h"]),
            "a chart's ink covers at least %d%% of its own box" % round(100 * LOST_MIN),
            "Size the chart's box from the chart (a ring's box is its diameter), or put it in a tile of its own shape.",
            planted=x.get("planted"), tile=x.get("tile"))
    return F


_KIND_STRIP = re.compile(r"'[^']*'|\"[^\"]*\"|#[\w-]+|-?\d+(?:\.\d+)?")   # quoted text, ids, numbers


def kinds(findings):
    """Distinct defect PATTERNS: one clause at one width on one selector shape counts once, so four
    KPI labels clipped the same way are one defect, as a designer would say it. {key: count}."""
    out = {}
    for f in findings:
        k = "%s@%s %s" % (f["clause"], f["width"], re.sub(r"\s+", " ", _KIND_STRIP.sub("", f["where"])).strip())
        out[k] = out.get(k, 0) + 1
    return out


def score(findings):
    """0-3 over defect KINDS (see `kinds`): 3 none · 2 no major kind and ≤3 minor kinds ·
    1 ≤2 major kinds · 0 three or more major kinds."""
    ks = kinds(findings)
    major = sum(1 for k in ks if k.split("@")[0] in MAJOR)
    minor = len(ks) - major
    if not ks:
        return 3
    if major == 0 and minor <= 3:
        return 2
    if major <= 2:
        return 1
    return 0


# ───────────────────────────── the browser ─────────────────────────────
def _shell_path():
    if os.environ.get("RENDER_SHELL") and os.path.exists(os.environ["RENDER_SHELL"]):
        return os.environ["RENDER_SHELL"]
    roots = []
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        roots.append(os.environ["PLAYWRIGHT_BROWSERS_PATH"])
    roots += glob.glob("/var/tmp/pw-browsers*")
    roots.append(os.path.expanduser("~/.cache/ms-playwright"))
    for root in roots:
        for pat in (("chromium_headless_shell-*", "chrome-linux", "headless_shell"),
                    ("chromium_headless_shell-*", "chrome-headless-shell-linux-*", "chrome-headless-shell"),
                    ("chromium-*", "chrome-linux", "chrome")):
            hits = sorted(glob.glob(os.path.join(root, *pat)))
            if hits:
                return hits[-1]
    return None


class Harness:
    """One browser for a whole run. HARNESS UNAVAILABLE → exit 77 upstream, never a pass."""

    def __enter__(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError("GEOMETRY: HARNESS UNAVAILABLE — playwright not importable (%s). "
                               "Install it with `pip install playwright && playwright install chromium`; "
                               "at the seat, source knowledge/_render/seat_env.sh. This is NOT a pass." % exc)
        shell = _shell_path()
        if not shell:
            raise RuntimeError("GEOMETRY: HARNESS UNAVAILABLE — no chromium headless shell found "
                               "($RENDER_SHELL, PLAYWRIGHT_BROWSERS_PATH, ~/.cache/ms-playwright). NOT a pass.")
        self._pw = sync_playwright().start()
        try:
            self.b = self._pw.chromium.launch(executable_path=shell, headless=True,
                                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        except Exception as e:
            self._pw.stop()
            raise RuntimeError("GEOMETRY: HARNESS UNAVAILABLE — the headless shell would not launch (%s). "
                               "NOT a pass." % str(e).splitlines()[0][:200])
        return self

    def __exit__(self, *a):
        try:
            self.b.close()
        finally:
            self._pw.stop()

    def model(self, path, width, levers=()):
        pg = self.b.new_page(viewport={"width": width, "height": 900})
        try:
            pg.emulate_media(reduced_motion="reduce")
            pg.goto("file://" + os.path.abspath(path))     # ⛔ never set_content()
            pg.evaluate("() => document.fonts ? document.fonts.ready.then(() => 1) : 1")
            # walk the page once so observer-driven parts (charts on scroll) draw, then return to top
            pg.evaluate("async () => { const h = document.documentElement.scrollHeight;"
                        " for (let y = 0; y < h; y += 700) { window.scrollTo(0, y);"
                        " await new Promise(r => requestAnimationFrame(() => r())); }"
                        " window.scrollTo(0, 0); }")
            # …and every INNER scroll box too (an app shell scrolls its content box, not the window),
            # then return each to its origin (W4b #304)
            pg.evaluate(INNER_WALK_JS)
            pg.wait_for_timeout(350)
            pg.evaluate(FINISH_ANIMATIONS_JS)
            # SETTLE: charts fit themselves to their boxes after load (resize observers, the fit
            # engine), so one early read can catch a chart mid-fit — measured #304, one dashboard
            # read 8 then 10 findings on identical runs. Read a layout signature until two reads
            # 200ms apart agree (at most ~2s), then measure.
            prev = None
            for _ in range(10):
                sig = pg.evaluate(SETTLE_JS)
                if sig == prev:
                    break
                prev = sig
                pg.wait_for_timeout(200)
            return pg.evaluate(COLLECT_JS, collect_opts(levers))
        finally:
            pg.close()


def run_pages(h, paths, widths, off=(), stops=None, quiet=False):
    levers = [x for x in off if x in LEVERS]
    off = {x for x in off if x not in LEVERS}
    out = []
    for p in paths:
        t0 = time.time()
        rec = {"gate": "geometry", "page": os.path.relpath(p, ROOT), "widths": {}, "findings": []}
        for w in widths:
            m = h.model(p, w, levers)
            f = judge(m, w, off, stops)
            rec["widths"][str(w)] = {"docW": m["docW"], "docH": m["docH"], "walls": len(m["walls"]),
                                     "tiles": len(m["tiles"]), "leaves": len(m.get("leaves") or []),
                                     "leaf_tiles": sum(1 for t in m["tiles"] if not t["group"]) + len(m.get("leaves") or []),
                                     "tables": len(m["tables"]),
                                     "font_ok": m.get("fontOk"), "findings": len(f)}
            rec["findings"] += f
        rec["runtime_ms"] = int((time.time() - t0) * 1000)
        rec["counts"] = {c: sum(1 for f in rec["findings"] if f["clause"] == c) for c in CLAUSES}
        rec["font_ok"] = all(v.get("font_ok") for v in rec["widths"].values())
        # a fallback face moves every text box: its findings are listed, never scored
        # THE score is at the design width: the CEO Common prompt asks for "wide desktop", so 1440
        # (or the widest width measured). Every width's score is reported beside it.
        by_w = {str(w): score([f for f in rec["findings"] if f["width"] == w]) for w in widths}
        rec["score_by_width"] = by_w if rec["font_ok"] else {w: None for w in by_w}
        rec["kinds"] = kinds(rec["findings"])
        rec["score"] = by_w[str(1440 if 1440 in widths else max(widths))] if rec["font_ok"] else None
        rec["verdict"] = ("UNPROVEN-FONT" if not rec["font_ok"] else "FINDINGS" if rec["findings"] else "CLEAN")
        out.append(rec)
        if not quiet:
            print(render_text(rec))
    return out


def render_text(rec):
    L = ["", "GEOMETRY %s — %s · score %s/3 · %d finding(s) · %d ms%s" % (
        rec["page"], rec["verdict"], "-" if rec["score"] is None else rec["score"], len(rec["findings"]), rec["runtime_ms"],
        "" if rec.get("font_ok") else " · ⚠ HSBC face NOT in use (fallback render)")]
    for f in sorted(rec["findings"], key=lambda f: (f["severity"] != "major", f["clause"], f["width"])):
        L.append("  %s %-4s @%-4s %s — %s" % ("✖" if f["severity"] == "major" else "⚠", f["clause"], f["width"],
                                              f["name"], f["where"]))
        L.append("         measured: %s" % f["measured"])
        L.append("         fix: %s" % f["fix"])
    return "\n".join(L)


def render_md(recs):
    L = ["# Geometry gate — advisory report", "",
         "Generated by `knowledge/_validate_geometry.py`. Clauses and tolerances: the script's docstring.", ""]
    for rec in recs:
        L.append("## %s — %s, score %s/3" % (rec["page"], rec["verdict"], "-" if rec["score"] is None else rec["score"]))
        L.append("")
        if not rec["findings"]:
            L.append("No findings.")
        for f in rec["findings"]:
            L.append("- **%s %s** at %spx — %s. Measured: %s. Fix: %s" % (
                f["clause"], f["name"], f["width"], f["where"], f["measured"], f["fix"]))
        L.append("")
    return "\n".join(L)


# ───────────────────────────── selftest: planted defects, clean pages, the real #288 page, mutations ──
PLANTED_EXPECT = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
# W4b #304: planted SUB-CASES — each a blind spot found on the cold runs, planted under its own
# marker so it is proven separately from its clause's original case. (clause, data-planted value,
# the cause lever that must let it through — None when the clause switch is the only lever)
PLANTED_SUB = [("G6", "G6-lone", "X-lone"), ("G7", "G7-shell", "X-scroll"), ("G8", "G8-scroll", "X-scroll"),
               ("G11", "G11-letters", None)]
# the #288 page is the ARTEFACT THE FINDING CAME FROM ([[conflated-fix-guarantees-recurrence]]):
# four of the conductor's five observations must be named on it. (The fifth, "two bottom-row
# cards not sharing a bottom edge", does not reproduce at today's canon: measured, both end at
# the wall's floor — reported in the R4b sub-report, not faked here.)
REAL_EXPECT = ["G1b", "G3", "G5", "G6"]
# The reference bento is NOT clean, and saying so is the gate working. At 1440 its four KPI
# sparklines are `preserveAspectRatio="none"` SVGs (viewBox 200x48 drawn ~309x44) whose end dot is
# a `<circle r="3">`: it renders as a ~9x5.5 ellipse (render-confirmed #304 R4b, 4x crop at
# notes/_lanes/304/R4b/ref-spark-1440.png). Nothing else at 1440. At 390 the template is not
# built for the width (the masthead scrolls sideways, KPI figures overlap and clip) — reported in
# the sub-report, not asserted here. (clause, substring of `where`)
REFERENCE_KNOWN_TRUE = [("G10", "svg.spark-inline")]
# W3b's receipt (#304): v1013-r2's overview at 1440 holds a ring chart in a 1,221px full-width tile
# with a hole under the ring that the R4b gate read as G6 = 0 (a one-panel group's panel was never
# measured). The real page is the frozen cold run beside the v1.0.13 pack it links (../pack/…);
# the selftest stages the two into $TMPDIR and asserts the gate now names the hole (G6) and the
# ring lost in its box (G12) on that tile. Absent run or pack = the leg is SKIPPED and said so.
REAL_W3B_RUN = os.path.join(ROOT, "notes", "_lanes", "304", "R4c", "cold", "v1013-r2", "out")
REAL_W3B_PACK = os.path.join(ROOT, "apollo-spider", "dist", "Apollo-Spider-v1.0.13.zip")
REAL_W3B_EXPECT = [("G6", "Cash by currency"), ("G12", "Cash by currency")]


def _stage_w3b():
    """Stage W3b's real page (frozen run + its pack) under $TMPDIR; None when either is absent."""
    import hashlib, shutil, tempfile, zipfile
    if not (os.path.isdir(REAL_W3B_RUN) and os.path.exists(REAL_W3B_PACK)):
        return None
    h = hashlib.sha256(open(REAL_W3B_PACK, "rb").read()).hexdigest()[:12]
    root = os.path.join(tempfile.gettempdir(), "geometry-w3b-" + h)
    if not os.path.exists(os.path.join(root, ".ok")):
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(os.path.join(root, "zip"))
        zipfile.ZipFile(REAL_W3B_PACK).extractall(os.path.join(root, "zip"))
        tops = [d for d in os.listdir(os.path.join(root, "zip")) if os.path.isdir(os.path.join(root, "zip", d))]
        src = os.path.join(root, "zip", tops[0]) if len(tops) == 1 else os.path.join(root, "zip")
        os.rename(src, os.path.join(root, "pack"))
        open(os.path.join(root, ".ok"), "w").write(h)
    shutil.rmtree(os.path.join(root, "out"), ignore_errors=True)
    shutil.copytree(REAL_W3B_RUN, os.path.join(root, "out"), ignore=shutil.ignore_patterns("_to_delete"))
    return os.path.join(root, "out", "index.html")


def selftest(h, stops, verbose=True):
    fails = []
    t0 = time.time()
    widths = [1440, 390]
    models = {}
    for key, path in (("planted", FIX_PLANTED), ("clean", FIX_CLEAN), ("reference", REFERENCE_BENTO),
                      ("real288", REAL_288)):
        if not os.path.exists(path):
            fails.append("fixture missing: %s" % os.path.relpath(path, ROOT))
            continue
        models[key] = {w: h.model(path, w) for w in widths}
    if fails:
        return fails, None
    allf = lambda k, off=(): [f for w in widths for f in judge(models[k][w], w, off, stops)]
    # 1. every planted defect is named, on the planted element
    pf = allf("planted")
    for c in PLANTED_EXPECT:
        hit = [f for f in pf if f["clause"] == c and f["planted"] == c]
        if not hit:
            fails.append("PLANTED %s (%s) NOT CAUGHT on the planted element" % (c, NAMES[c]))
        elif verbose:
            print("  ✓ planted %-4s %-28s caught: %s" % (c, NAMES[c], hit[0]["measured"][:90]))
    for c, sub, lever in PLANTED_SUB:
        hit = [f for f in pf if f["clause"] == c and f["planted"] == sub]
        if not hit:
            fails.append("PLANTED %s (%s) NOT CAUGHT on the planted element" % (sub, NAMES[c]))
        elif verbose:
            print("  ✓ planted %-11s %-21s caught: %s" % (sub, NAMES[c], hit[0]["measured"][:84]))
    stray = [f for f in pf if not f["planted"]]
    if stray:
        fails.append("PLANTED page: %d finding(s) on UNPLANTED elements, e.g. %s %s"
                     % (len(stray), stray[0]["clause"], stray[0]["where"][:80]))
    # 2. clean pages pass: the clean fixture at both widths with ZERO findings; the reference bento
    #    at its design width with nothing but its KNOWN TRUE findings (named below, evidenced in
    #    the R4b sub-report). Anything else on either is a false positive and fails the selftest.
    cf = allf("clean")
    if cf:
        fails.append("CLEAN fixture: %d finding(s), e.g. %s %s — %s" % (len(cf), cf[0]["clause"],
                                                                        cf[0]["where"][:60], cf[0]["measured"][:80]))
    elif verbose:
        print("  ✓ clean fixture passes at 1440 and 390 (0 findings)")
    face = all(models[k][w].get("fontOk") for k in ("reference", "real288") for w in widths)
    if not face:
        print("  ⊘ the HSBC face is NOT drawing: the reference-bento and real-#288 legs are UNPROVEN-FONT "
              "(their text boxes move with the face), not failed. Planted, clean and mutation legs still hold.")
    rf0 = judge(models["reference"][1440], 1440, (), stops) if face else []
    unknown = [f for f in rf0 if not any(f["clause"] == c and s in f["where"] for c, s in REFERENCE_KNOWN_TRUE)]
    known = [f for f in rf0 if f not in unknown]
    if unknown:
        fails.append("REFERENCE bento @1440: %d finding(s) beyond the known-true list, e.g. %s %s — %s"
                     % (len(unknown), unknown[0]["clause"], unknown[0]["where"][:60], unknown[0]["measured"][:80]))
    elif verbose and face:
        print("  ✓ reference bento @1440: only its %d known-true finding(s) (%s)"
              % (len(known), ", ".join(sorted({f["clause"] + " " + f["name"] for f in known}))))
    # 3. the real #288 page: the conductor's observations are named
    rf = allf("real288")
    for c in (REAL_EXPECT if face else []):
        if not any(f["clause"] == c for f in rf):
            fails.append("REAL #288 page: %s (%s) not named" % (c, NAMES[c]))
        elif verbose:
            print("  ✓ real #288 %-4s named: %s" % (c, next(f for f in rf if f["clause"] == c)["measured"][:80]))
    # 4. a mutation per clause: switching the clause off lets its planted defect through
    for c in PLANTED_EXPECT:
        mf = allf("planted", off={c})
        if any(f["clause"] == c for f in mf):
            fails.append("MUTATION %s: clause switched off but its finding still appears" % c)
        others = {f["clause"] for f in mf if f["planted"] == f["clause"]}
        if others != set(PLANTED_EXPECT) - {c}:
            fails.append("MUTATION %s: switching it off changed other clauses' catches: %s"
                         % (c, sorted(set(PLANTED_EXPECT) - {c} - others)))
    # 5. the CAUSE levers (W4b): restoring each repaired blind spot lets exactly its sub-cases through
    #    and moves nothing else on the planted page
    base_keys = sorted((f["clause"], f["planted"], f["where"]) for f in pf)
    for lever in sorted(LEVERS):
        subs = {sub for c, sub, lv in PLANTED_SUB if lv == lever}
        lm = [f for w in widths for f in judge(h.model(FIX_PLANTED, w, [lever]), w, (), stops)]
        still = {f["planted"] for f in lm} & subs
        if still:
            fails.append("LEVER %s: the cause restored but %s still caught — the repair is not what catches it" % (lever, sorted(still)))
        guard = {"X-own": {"guard-own"}}.get(lever, set())      # a guard lever re-opens its own guard, nothing else
        rest = sorted((f["clause"], f["planted"], f["where"]) for f in lm if f["planted"] not in guard)
        expect = [k for k in base_keys if k[1] not in subs]
        if rest != expect:
            fails.append("LEVER %s: other findings moved (%d → %d outside the sub-cases)" % (lever, len(expect), len(rest)))
        elif verbose and not still:
            print("  ✓ cause lever %-8s %s" % (lever, ("restores the blind spot: %s slip through, nothing else moves" % ", ".join(sorted(subs)))
                                                if subs else "moves nothing on the planted page but its own false-positive guard"))
    # 5b. the FALSE-POSITIVE guard (W4b): the clean page holds an ellipsis title beside a tag; with the
    #     own-clip repair switched off (X-own) its hidden tail collides — the guard must then fire
    gm = [f for w in widths for f in judge(h.model(FIX_CLEAN, w, ["X-own"]), w, (), stops)]
    if not any(f["clause"] == "G7" and f["planted"] == "guard-own" for f in gm):
        fails.append("GUARD X-own: switching the own-clip repair off did not bring back the ellipsis-tail G7 — the guard proves nothing")
    elif verbose:
        print("  ✓ false-positive guard: X-own switched on, the clean page's ellipsis title reads as a collision (the repair is what clears it)")
    # 6. W3b's real page: the ring hole the R4b gate read as G6 = 0
    real = _stage_w3b()
    if real is None:
        print("  ⊘ W3b real-page leg SKIPPED: %s or %s is absent" % (os.path.relpath(REAL_W3B_RUN, ROOT), os.path.relpath(REAL_W3B_PACK, ROOT)))
    else:
        mw = h.model(real, 1440)
        wf = judge(mw, 1440, (), stops)
        if not mw.get("fontOk"):
            print("  ⊘ W3b real-page leg UNPROVEN-FONT (the HSBC face is not drawing)")
        for c, name in REAL_W3B_EXPECT:
            hit = [f for f in wf if f["clause"] == c and name in f["where"]]
            if not hit and mw.get("fontOk"):
                fails.append("REAL W3b page (v1013-r2): %s (%s) not named on '%s'" % (c, NAMES[c], name))
            elif hit and verbose:
                print("  ✓ real v1013-r2 %-4s named on '%s': %s" % (c, name, hit[0]["measured"][:70]))
        lw = judge(h.model(real, 1440, ["X-lone"]), 1440, (), stops)
        if any(f["clause"] == "G6" and "Cash by currency" in f["where"] for f in lw):
            fails.append("REAL W3b page: with the lone-leaf repair switched off, G6 still names the ring tile — the repair is not the cause")
        elif verbose:
            print("  ✓ real v1013-r2: X-lone switched on, the ring tile's G6 disappears (R4b's reading reproduced)")
    if verbose:
        print("  ✓ %d mutations: each clause switched off lets exactly its own planted defect through"
              % len(PLANTED_EXPECT) if not any(x.startswith("MUTATION") for x in fails) else "  ✖ mutation leg failed")
        print("  selftest runtime %d ms (4 pages × 2 widths)" % int((time.time() - t0) * 1000))
    return fails, face


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--widths", default="1440,390")
    ap.add_argument("--json", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--mutate", default="", help="comma list of clauses to switch OFF")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    stops = spacing_stops()
    off = {x.strip() for x in a.mutate.split(",") if x.strip()}
    bad = off - set(CLAUSES) - set(LEVERS)
    if bad:
        print("✖ GEOMETRY: unknown clause(s) %s — known: %s" % (sorted(bad), ", ".join(CLAUSES)), file=sys.stderr)
        return 2
    if stops is None:
        print("⚠ GEOMETRY: %s not found — bento gutters are held to the 4px grid only (stop set UNPROVEN)"
              % os.path.relpath(RAILS, ROOT))
    if not (a.selftest or a.build or a.files):
        print("✖ GEOMETRY: no input files. Pass pages, --selftest or --build (`--help` for the contract).", file=sys.stderr)
        return 2
    widths = [int(x) for x in a.widths.split(",") if x.strip()]
    with Harness() as h:
        rc = 0
        if a.selftest or a.build:
            print("Geometry selftest — planted fixture (%d clauses + %d sub-cases), clean fixture, reference bento, "
                  "the #288 page, W3b's v1013-r2 page, %d clause mutations + %d cause levers"
                  % (len(PLANTED_EXPECT), len(PLANTED_SUB), len(PLANTED_EXPECT), len(LEVERS)))
            fails, face = selftest(h, stops)
            for f in fails:
                print("  ✖ " + f)
            if fails:
                print("GEOMETRY SELFTEST FAILED — %d problem(s). The INSTRUMENT is broken, not the pages." % len(fails))
                rc = 1
            elif not face:
                print("GEOMETRY SELFTEST OK — PARTIAL: fixture and mutation legs proven; the reference-bento and "
                      "#288 legs UNPROVEN-FONT (the HSBC face is not drawing on this box)")
            else:
                print("GEOMETRY SELFTEST OK")
        files = list(a.files)
        if a.build:
            files += [os.path.join(ROOT, p) for p in BUILD_SWEEP if os.path.exists(os.path.join(ROOT, p))]
        if files:
            recs = run_pages(h, files, widths, off, stops)
            n = sum(len(r["findings"]) for r in recs)
            print("\nADVISORY: %d page(s), %d finding(s); scores %s"
                  % (len(recs), n, ", ".join("%s=%s" % (os.path.basename(r["page"]), "-" if r["score"] is None else r["score"]) for r in recs)))
            if a.json:
                with open(a.json, "w") as fh:
                    json.dump(recs if len(recs) > 1 else recs[0], fh, indent=1)
                print("wrote %s" % a.json)
            if a.out:
                with open(a.out, "w") as fh:
                    fh.write(render_md(recs))
                print("wrote %s" % a.out)
            if n and a.strict:
                rc = rc or 1
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        if "HARNESS UNAVAILABLE" in str(e):
            print("COULD-NOT-ASK: %s" % e, file=sys.stderr)
            sys.exit(77)
        print("✖ %s" % e, file=sys.stderr)
        sys.exit(2)
