#!/usr/bin/env python3
"""
gen_gallery_compare_217.py — THE GALLERY DECISION PAGE (#217). For Dave's eye.

Dave's #217 question, answered by showing it —

    "whether gallery stays a span grid with orphan tolerance, or becomes justified rows with a
     widow switch — would this be visually different, id like to see these two side by side"

⛔ #219 RE-CUT — AND THIS PAGE'S OWN QUESTION IS THE ONE THAT WAS ANSWERED. It now writes
`reviews/GALLERY-COMPARE-2026-08-25-v2.html`. `s217-D5` settled A-or-B with a third answer:
*"mode is 'Justified rows' OR 'Gallery bento', the bento mode carrying a sub-option ragged or
square bottom"* — BOTH, as a per-instance dial. `s218-D3` then set the Foundations photography
page's instance (bento mode, keylines off, all four themes) and `s218-D6 (4)` squared that page's
wall. So A and B are no longer candidates: they are the two positions of a ruled dial, and what is
still open is narrower and named. Ledger: `_bento_recut_219.py`. ⚠ v1 is untouched on disk. This
generator still writes ONE review file and touches no canon, no token and no ruling.

THE TWO CANDIDATES, ON THE SAME 15 PHOTOGRAPHS IN THE SAME ORDER
  A · THE RULED GALLERY ROLE — `.c-bento[data-bento-role="gallery"]` exactly as canon renders it:
      aspect-derived spans, the every-6th rhythm, squaring OFF (orphans tolerated), keylines, the
      ruled 86px caption space. Shown at canon's DEFAULT 6 columns **and** at the 4-column dial the
      #217 roles page used — because the crop cost of A is a function of that dial, and showing
      only the harsh one would be a strawman.
      A also carries the s217-D3 keyline-less TRIAL variant (1px gutter, no borders), which is
      itself PROPOSED, not ruled.
  B · JUSTIFIED ROWS, FLICKR-STYLE — packed HERE, at mint time (s200-D1), never at runtime:
      photographs are taken in order into a row until the row's height would fall below the target,
      the row is scaled to justify flush to both container edges, and NOTHING IS CROPPED — every
      box carries its own native aspect ratio. Row HEIGHT varies; row WIDTH never does.
      The final short row are WIDOWS (Flickr's own word): they are NOT scaled up, they are counted,
      and a no-JavaScript switch (checkbox + CSS) shows or hides them.

⚠ ONE DATA PATH, DELIBERATELY. Both candidates consume `gen_bento_roles_217.read_photos()` — the
same rows, the same order, the same derived spans as the ruled page. Two data paths would make the
comparison a lie, and it is the cheapest possible lie to tell by accident.

THE TARGET ROW HEIGHT IS NOT A TASTE PICK: it is `layout/bento/row-unit` = 320px, the ruled row
unit (s217-D2) — which is also, independently, Flickr's own `targetRowHeight` default. Read from
the store, never typed here.

THE NOMINAL PACKING WIDTH is the page's own content width (1400 max − 2×32 padding = 1336px).
⬛ DECLARED CONSEQUENCE, and it belongs in the decision: a MINT-TIME packing fixes which photographs
share a row. The rows stay flush at every width (that is what the flex maths guarantees) but they
get SHORTER as the container narrows, because the membership cannot change. Flickr re-packs at
runtime. A shipped B would need either a per-band mint or a runtime pass; A re-flows for free.

Usage:
  python3 knowledge/_render/gen_gallery_compare_217.py
  python3 knowledge/_render/gen_gallery_compare_217.py --break-justify  # mutation -> *-BROKEN.html
  python3 knowledge/_render/gen_gallery_compare_217.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import html as htmlmod
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
sys.path.insert(0, os.path.join(KNOW, "canon"))
sys.path.insert(0, HERE)
from gen_canon_bento import (store, params, caption_space, band_ladder,  # noqa: E402
                             band_clamp, place, role_policy, square_wall, is_rectangular)
from gen_bento_roles_217 import read_photos  # noqa: E402  ⚠ THE SINGLE DATA PATH
import _bento_recut_219 as recut  # noqa: E402  ⚠ THE ONE HOME for the decision ledger

# ⚠ v2, NOT an overwrite. `GALLERY-COMPARE-2026-08-23-v1.html` stays on disk exactly as Dave saw
# it; this is its #219 successor ([[feedback-version-dont-overwrite]]).
OUT = os.path.join(ROOT, "reviews", "GALLERY-COMPARE-%s-v2.html" % recut.RECUT_DATE)
UP = "../"
SENTINEL = "<!-- APOLLO GALLERY COMPARE (gen_gallery_compare_217.py) — RE-CUT #219 -->"

# ⚠ THE NOMINAL PACKING WIDTH. Derived from the page's own chrome (main is capped at 1400 with
# 32px padding each side), not picked: packing against a width the page never renders at would
# produce rows that are flush in theory and wrong on screen.
NOMINAL_W = 1336.0
# The gutter used for the MINT-TIME row-break arithmetic. The four themes diverge on gutter alone
# (0 / 24), and the packing has to assume one; console — the opening theme — is the wider case, so
# rows minted here never over-fill the tighter themes. The RENDERED justification is exact in both,
# because flex distributes whatever free space the real gutter leaves.
PACK_GUTTER = 24.0

BREAK_JUSTIFY = False   # ⬛ the mutation handle — see main()


def esc(s):
    return htmlmod.escape(str(s if s is not None else ""), quote=True)


def target_row_height():
    """The ruled row unit, read from the store. ⚠ NOT a local constant: 320 is `layout/bento/
    row-unit` (s217-D2), and it is also Flickr's own default target. Typing it here would make the
    page a second source for a ruled number."""
    return float(str(store()["row-unit"]["$value"]).replace("px", ""))


# ------------------------------------------------------------------ B · the justified packing
def pack_rows(photos, container=NOMINAL_W, gutter=PACK_GUTTER, target=None):
    """FLICKR'S ROW ALGORITHM, at mint time. -> (rows, widows).

    Take photographs in order into the current row. A row of aspect ratios a_1..a_n in a container
    of width W with n-1 gutters justifies at height h = (W - (n-1)g) / Σa. Adding a photograph
    always LOWERS h; the row closes when the next photograph would take h below the target, and the
    candidate closer to the target wins — that is the whole of it, and it is why row HEIGHT varies
    and row WIDTH never does.

    ⚠ THE LAST ROW IS NOT A ROW. Whatever is left over cannot justify without being blown up past
    the target, so it is returned separately as WIDOWS and rendered at the target height, unscaled.
    """
    target = target or target_row_height()

    def height(row):
        return (container - (len(row) - 1) * gutter) / sum(p["ar"] for p in row)

    rows, cur = [], []
    for p in photos:
        cand = cur + [p]
        if cur and height(cand) < target and abs(height(cur) - target) <= abs(height(cand) - target):
            rows.append(cur)
            cur = [p]
        elif height(cand) < target:
            rows.append(cand)
            cur = []
        else:
            cur = cand
    return rows, cur


def crop_fraction(box_ar, img_ar):
    """How much of the photograph `object-fit:cover` throws away in a compartment of aspect
    `box_ar`. 0 when the compartment matches the picture. This is A's currency: A fits pictures to
    compartments, B fits compartments to pictures."""
    return 1.0 - (min(box_ar, img_ar) / max(box_ar, img_ar))


def a_wall_report(photos, cols, gutter=PACK_GUTTER, container=NOMINAL_W):
    """What candidate A costs, measured rather than asserted: the crop per tile at `cols` columns,
    and where the ragged edge sits (the squaring pass is OFF for gallery — s217-D3)."""
    space, _ = caption_space()
    unit = target_row_height()
    crops = []
    for p in photos:
        c, r = p["span"]
        c = min(c, cols)
        cw = (container - (cols - 1) * gutter) / cols * c + (c - 1) * gutter
        ch = unit * r + (r - 1) * gutter - space
        crops.append(crop_fraction(cw / ch, p["ar"]) if ch > 0 else 1.0)
    spans = [p["span"] for p in photos]
    holes = {}
    for band in band_ladder(dict(params(), columns=cols)):
        rows_used, hole, _ = place(band_clamp(spans, band), band)
        holes[band] = (hole, rows_used)
    return {"cols": cols, "crops": crops, "holes": holes,
            "mean": sum(crops) / len(crops), "worst": max(crops),
            "cropped": sum(1 for x in crops if x > 0.02)}


# ---------------------------------------------------------------------------------- tiles
def a_tile(p, caption=True):
    c, r = p["span"]
    cap = ('<figcaption class="c-bento__caption gc-cap">'
           '<span class="gc-desc t-ed-caption">%s</span>'
           '<span class="gc-lic t-cm-legal">%s</span></figcaption>'
           % (esc(p["desc"]), esc(p["licence"]))) if caption else ""
    return ('<figure class="c-bento__tile gc-atile" data-c="%d" data-r="%d">'
            '<img class="gc-img" src="%sknowledge/assets/photography-web/%s" alt="%s"'
            ' loading="lazy" width="%s" height="%s">%s</figure>'
            % (c, r, UP, esc(p["file"]), esc(p["desc"]), p["w"] or "", p["h"] or "", cap))


def b_tile(p, idx, widow=False):
    """⚠ NO INLINE STYLE. The per-photograph aspect and flex-grow are DECLARED rules minted into
    the page stylesheet (`.gc-p<i>`): an inline custom property is invisible to every instrument
    that resolves the stylesheet against the document, and this page exists to be measured."""
    return ('<figure class="gc-btile gc-p%d%s" data-ar="%.6f" data-file="%s">'
            '<span class="gc-box"><img class="gc-img" '
            'src="%sknowledge/assets/photography-web/%s" alt="%s" loading="lazy" '
            'width="%s" height="%s"></span>'
            '<figcaption class="c-bento__caption gc-cap">'
            '<span class="gc-desc t-ed-caption">%s</span>'
            '<span class="gc-lic t-cm-legal">%s</span></figcaption></figure>'
            % (idx, " gc-widow" if widow else "", p["ar"], esc(p["file"]),
               UP, esc(p["file"]), esc(p["desc"]), p["w"] or "", p["h"] or "",
               esc(p["desc"]), esc(p["licence"])))


def photo_rules(photos):
    """The minted per-photograph rules: native aspect + the flex-grow that justifies the row.

    flex-grow proportional to the aspect ratio, on a zero basis, is the CSS statement of the same
    arithmetic `pack_rows` does: each box takes a share of the row's free space in proportion to
    its own width-to-height, so every box in the row lands on the SAME height and the row ends
    exactly at the container edge. ⚠ The maths is therefore enforced by the browser at the real
    width, not baked to a pixel figure that would be wrong at every other width.
    """
    out = []
    for i, p in enumerate(photos, 1):
        if BREAK_JUSTIFY:
            # ⬛ THE MUTATION. Every tile is sized like a WIDOW — a real box at the target height,
            # with neither growth nor shrink — so the wall still renders photographs at their native
            # aspect and simply MISSES the container edge (here it overruns it). ⚠ Deliberately not a
            # collapse to zero: a mutation that destroys the layout is caught by any assertion at
            # all, and would tell us nothing about whether the FLUSH assertion can see the defect
            # it exists for ([[mutation-tests-the-clause-not-the-feature]]).
            out.append(".gc-p%d{--gc-ar:%.6f; --gc-arn:%.6f; flex-grow:0; flex-basis:auto; "
                       "flex-shrink:0; width:calc(var(--layout-bento-row-unit) * %.6f);}"
                       % (i, p["ar"], p["ar"], p["ar"]))
        else:
            out.append(".gc-p%d{--gc-ar:%.6f; --gc-arn:%.6f; flex-grow:%.6f;}"
                       % (i, p["ar"], p["ar"], p["ar"]))
    return "\n".join(out)


# ------------------------------------------------------------------------------ page-local CSS
CSS_HEAD = """
/* ===========================================================================
   GALLERY COMPARE — page-local styles, scoped to `.gc`.
   ⬛ EVERYTHING HERE IS PROPOSED. CANDIDATE A declares NO structure of its own —
   its grid, spans, bands, role rules and caption space all come from canon.css's
   AUTO-BENTO block, which is the point: A must be canon's own output or the
   comparison is against a drawing of A rather than A.
   ⚠ CANDIDATE B DOES declare structure, unavoidably: justified rows are not a
   grid and canon has no grammar for them. Every such declaration is named
   `.gc-b…`, and the selftest enforces that none of them can reach a `.c-bento__grid`
   — a proposal that quietly restyled the ruled variant beside it would make the
   side-by-side a comparison of a thing with itself.
   =========================================================================== */
.gc{
  --page:      var(--background-default,#FFFFFF);
  --surface:   var(--tertiary-background-default,#FFFFFF);
  --surface-2: var(--tertiary-background-hover,#F3F3F3);
  --line:      var(--border-subtle,#D7D8D6);
  --line-2:    var(--border-strong,#767676);
  --ink:       var(--text-default,#1A1A1A);
  --ink-2:     var(--text-secondary,#545454);
  --focus:     var(--focus-ring,#1A1A1A);
  --focus-w:   var(--focus-ring-width,2px);
  --radius-ctl:var(--border-radius-control,0px);
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px; --sp-7:48px;
  background:var(--page); color:var(--ink); -webkit-font-smoothing:antialiased;
}
.gc *{box-sizing:border-box;}
.gc :focus-visible{outline:var(--focus-w) solid var(--focus); outline-offset:2px;}
html,body{margin:0;}
body{background:var(--background-default,#FFFFFF);}
/* ⚠ the ink is restated on a CHILD of the themed element — measured #217: an element that BOTH
   carries data-theme and reads --text-default disagreed with its own children in supercharge. */
.gc, header.app{color:var(--text-default,#1A1A1A);}

header.app{display:flex; flex-wrap:wrap; gap:var(--sp-4); align-items:center;
  padding:var(--sp-3) var(--sp-6); border-bottom:1px solid var(--line);
  background:var(--page); position:sticky; top:0; z-index:10;}
body[data-chrome="0"] header.app{display:none;}
header.app h1{margin:0; white-space:nowrap;}
header.app .spacer{flex:1 1 auto;}
.ctl{display:flex; align-items:center; gap:var(--sp-2); color:var(--ink-2);}
.seg{display:inline-flex; border:1px solid var(--ink); color:var(--ink);
  border-radius:var(--radius-ctl); overflow:hidden;}
.seg button{font-family:inherit; font-size:12px; font-weight:500; letter-spacing:0.06em;
  text-transform:uppercase; padding:7px 12px; border:0; background:transparent; color:inherit;
  cursor:pointer; border-right:1px solid var(--line);}
.seg button:last-child{border-right:0;}
.seg button[aria-pressed="true"]{background:var(--ink); color:var(--page);}

main{padding:var(--sp-6); max-width:1400px;}   /* 1400 - 2x32 = the 1336px packing width */
section{margin:0 0 var(--sp-7); scroll-margin-top:80px;}
h2{margin:0 0 var(--sp-1);}
h3{margin:var(--sp-6) 0 var(--sp-2);}
p.lede{margin:0 0 var(--sp-5); color:var(--ink-2); max-width:74ch;}
.sublabel{color:var(--ink-2); text-transform:uppercase; letter-spacing:0.14em;
  margin:var(--sp-5) 0 var(--sp-3); display:flex; align-items:center; gap:var(--sp-2);}
.sublabel::before{content:''; width:20px; height:1px; background:var(--line);}
.gc a{color:inherit;}
.gc code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:12px;
  background:var(--surface-2,#F3F3F3); padding:0 .3em;}
.note{margin:var(--sp-3) 0 0; color:var(--ink-2); max-width:74ch;}
.note b{color:var(--ink);}
.badge{display:inline-block; border:1px solid var(--line-2,#767676); color:var(--ink,#1A1A1A);
  padding:2px 8px; letter-spacing:0.12em; text-transform:uppercase; margin:0 0 var(--sp-3);}
.gc-tag{display:inline-block; border:1px solid var(--ink,#1A1A1A); color:var(--page,#FFFFFF);
  background:var(--ink,#1A1A1A); padding:2px 10px; letter-spacing:0.12em;
  text-transform:uppercase; margin:0 var(--sp-2) var(--sp-2) 0;}
table.gc-diff{border-collapse:collapse; margin:var(--sp-4) 0 0; width:100%; max-width:960px;}
table.gc-diff th, table.gc-diff td{border-bottom:1px solid var(--line,#D7D8D6);
  padding:var(--sp-3) var(--sp-4); text-align:left; vertical-align:top; color:var(--ink-2);}
table.gc-diff th{color:var(--ink); white-space:nowrap;}
table.gc-diff td:first-child{color:var(--ink); width:22%;}

/* ---- shared tile CONTENT (both candidates), so only LAYOUT differs -----------------------
   ⚠ The caption's SPACE is canon's (`.c-bento__caption`, s217-D3, 86px). What is here is only
   its inline padding, its colour and its clamp. Restating the ruled height would let the two
   drift, and the whole page would be comparing two different caption regimes. */
.gc-cap{padding-inline:var(--sp-3); color:var(--ink-2,#545454); display:flex;
  flex-direction:column; gap:2px; justify-content:center;}
.gc-desc{display:-webkit-box; -webkit-line-clamp:var(--bento-caption-lines,3);
  -webkit-box-orient:vertical; overflow:hidden; text-box-edge:text text;}
.gc-lic{color:var(--ink-2,#545454);}
__MONOCAP__
__RECUT__
.gc-img{display:block; width:100%; height:100%; min-height:0;
  background:var(--surface-2,#F3F3F3);}

/* ---- CANDIDATE A · tile chrome only. NO GRID, NO GAP, NO SPAN, NO ROLE RULE. ------------- */
.gc-atile{margin:0; display:grid; grid-template-rows:1fr auto;
  background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);}
/* ⛔ THE CROP LIVES HERE, and it is A's whole cost: the compartment is decided by the span
   vocabulary, so the picture has to be cut to fit it. */
.gc-atile .gc-img{object-fit:cover;}
/* instance dials — `.c-bento` in the selector so they out-specify canon's (0,2,0) role rules */
.c-bento.gc-a6{}                                   /* canon's own default: 6 columns, 320px rows */
.c-bento.gc-a4{--bento-columns:4;}
.c-bento.gc-atrial{--bento-columns:4; --bento-gutter:1px;}
.gc-atrial .gc-atile{border:0;}
.gc-atrial .gc-cap{padding-inline:var(--sp-2);}

/* ---- CANDIDATE B · JUSTIFIED ROWS — ⬛ PROPOSED, NOT RULED --------------------------------
   The container is still a `.c-bento` carrying the gallery role, so it takes the SAME per-theme
   gutter and the SAME ruled caption space as A. What it does not take is the grid: there is no
   `.c-bento__grid` here, and that is exactly the proposal. */
.c-bento.gc-b{display:flex; flex-direction:column; gap:var(--bento-gutter);}
.gc-brow{display:flex; gap:var(--bento-gutter); align-items:flex-start; min-width:0;}
/* flex-basis 0 + grow proportional to aspect = the row justifies flush and every box in it lands
   on one height. `min-width:0` or a long caption would push the row past the container. */
.gc-btile{margin:0; flex:0 1 0; min-width:0; display:flex; flex-direction:column;
  background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);}
.gc-box{display:block; width:100%; aspect-ratio:var(--gc-ar); overflow:hidden;}
/* ⛔ NOT `cover`. The box already carries the picture's own aspect, so there is nothing to crop —
   this is the one line that states B's claim, and `contain` makes a broken aspect VISIBLE as
   letterboxing instead of hiding it behind a silent crop. */
.gc-box .gc-img{object-fit:contain;}
/* THE WIDOWS. Flickr's word, and Flickr's rule: they are NOT blown up to justify. Each keeps the
   target row height, so a short last row simply ends where it ends. */
.gc-brow--widow .gc-btile{flex:0 1 auto;
  width:calc(var(--layout-bento-row-unit) * var(--gc-arn));}
/* the no-JavaScript widow switch: a checkbox and a sibling combinator, nothing else */
.gc-switch{width:16px; height:16px; margin:0; accent-color:var(--ink,#1A1A1A);}
.gc-switchrow{display:flex; align-items:center; gap:var(--sp-2); margin:0 0 var(--sp-4);
  color:var(--ink);}
.gc-switch:not(:checked) ~ .gc-b .gc-brow--widow{display:none;}
.gc-switch:not(:checked) ~ .gc-switchrow .gc-when-on{display:none;}
.gc-switch:checked ~ .gc-switchrow .gc-when-off{display:none;}
.gc-switchrow label{cursor:pointer;}

@media (prefers-reduced-motion: reduce){
  .gc *,.gc *::before,.gc *::after{transition-duration:.01ms !important;
    animation-duration:.01ms !important;}
}

/* ---- MINTED PER-PHOTOGRAPH RULES (s200-D1: the value is decided here, not resolved live) --- */
"""

SCRIPT = """
(function(){
  var THEMES=['mono','legacy','console','supercharge'];
  var state={theme:'console',mode:'light',chrome:'1'};
  function apply(){
    document.documentElement.setAttribute('data-apollo-theme',state.theme);
    document.body.setAttribute('data-theme',state.mode);
    document.body.setAttribute('data-chrome',state.chrome);
    document.querySelectorAll('#themes button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.themeAttr===state.theme)); });
    document.querySelectorAll('#modes button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.mode===state.mode)); });
  }
  var t=document.getElementById('themes'), m=document.getElementById('modes');
  if(t) t.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return; state.theme=b.dataset.themeAttr; apply(); });
  if(m) m.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return; state.mode=b.dataset.mode; apply(); });
  function fromHash(){
    var h={};
    location.hash.replace(/^#/,'').split('&').forEach(function(kv){
      var p=kv.split('='); if(p[0]) h[p[0]]=decodeURIComponent(p[1]||''); });
    if(THEMES.indexOf(h.theme)>=0) state.theme=h.theme;
    if(h.m==='light'||h.m==='dark') state.mode=h.m;
    if(h.chrome==='0'||h.chrome==='1') state.chrome=h.chrome;
    apply();
  }
  window.addEventListener('hashchange',fromHash);
  fromHash();
})();
"""

HEAD = """<!doctype html>
<html lang="en" data-apollo-theme="console">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
__SENTINEL__
<link rel="stylesheet" href="__UP__knowledge/canon/type.css">
<link rel="stylesheet" href="__UP__knowledge/canon/canon.css">
<style>__CSS__</style>
</head>
<body data-theme="light" data-chrome="1" class="gc canon">
<header class="app">
  <h1 class="t-ed-heading-4">__H1__</h1>
  <span class="t-ed-caption">__SUBTITLE__</span>
  <span class="spacer"></span>
  <div class="ctl"><span class="t-ed-caption">Theme</span>
    <div class="seg" id="themes" role="group" aria-label="Theme">
      <button type="button" data-theme-attr="mono" aria-pressed="false">Mono</button>
      <button type="button" data-theme-attr="legacy" aria-pressed="false">Legacy</button>
      <button type="button" data-theme-attr="console" aria-pressed="true">Console</button>
      <button type="button" data-theme-attr="supercharge" aria-pressed="false">Supercharge</button>
    </div>
  </div>
  <div class="ctl"><span class="t-ed-caption">Mode</span>
    <div class="seg" id="modes" role="group" aria-label="Light or dark">
      <button type="button" data-mode="light" aria-pressed="true">Light</button>
      <button type="button" data-mode="dark" aria-pressed="false">Dark</button>
    </div>
  </div>
</header>
<main>
"""

TAIL = """</main>
<script>__SCRIPT__</script>
</body>
</html>
"""


def build(photos, rows, widows, reps):
    space, lines = caption_space()
    unit = target_row_height()
    S = []
    A = S.append
    r6, r4 = reps["a6"], reps["a4"]
    heights = [(NOMINAL_W - (len(r) - 1) * PACK_GUTTER) / sum(p["ar"] for p in r) for r in rows]
    # ⬛ #219 — `s218-D6 (4)`: the photography page's INSTANCE edge dial at SQUARE, minted with the
    # ratified role-blind pass (`square_wall`), which is the same pass `gen_foundations_217` runs on
    # that wall. ⚠ `square_wall_for_role` is NOT used here on purpose: it would answer "exempt" for
    # every gallery, which is still true of the ROLE and is exactly the fact this wall is not about.
    sq_spans, sq_rep = square_wall([p["span"] for p in photos],
                                   ladder=band_ladder(dict(params(), columns=4)))

    # ---- 0 · #219 — WHAT IS ALREADY DECIDED ------------------------------------------------
    A(recut.ledger_html("compare"))

    # ---- 0b · the question, and the answer it already got ----------------------------------
    A('<section id="intro">')
    # ⛔ #219 — THE BADGE IS GONE. v1 badged the whole page "Proposed — not ruled" and s217-D5 had
    # already answered the question the page was built to put.
    A('<p class="badge t-cm-legal">Ruled &mdash; s217-D5 &middot; Q5</p>')
    A('<h2 class="t-ed-heading-3">Is a justified gallery visually different from a span gallery?</h2>')
    A('<p class="lede t-ed-body">You asked whether the gallery should stay a <b>span grid with '
      'orphan tolerance</b> or become <b>justified rows with a widow switch</b>, and whether that '
      'would even look different. <b>It looks very different, and the difference has one name: '
      'cropping.</b> A decides the compartment first and cuts the photograph to fit it. B decides '
      'the photograph first and builds the compartment around it.</p>')
    A('<p class="lede t-ed-body">Both walls below hold the <b>same %d photographs in the same '
      'order</b>, read from the same manifest rows, with the same %dpx caption space and the same '
      'per-theme gutter. Only the layout differs. The page opens in <b>console</b>; the theme and '
      'mode switches are above and everything is live in all four.</p>' % (len(photos), space))
    A('<p class="lede t-ed-body"><b>And you answered it &mdash; with a third option.</b> '
      '<code>s217-D5</code>: <i>&ldquo;mode is &lsquo;Justified rows&rsquo; OR &lsquo;Gallery '
      'bento&rsquo;, the bento mode carrying a sub-option ragged or square bottom&rdquo;</i>. '
      'Neither A nor B won; <b>both became positions of a per-instance dial</b>. Then at #218 you '
      'set the first instance: the Foundations photography page ships <b>bento mode</b>, keylines '
      'off, in all four themes (<code>s218-D3</code>), and its wall is <b>squared</b> '
      '(<code>s218-D6&nbsp;(4)</code>). <b>This page is now a reference for what each position '
      'looks like, not a choice waiting on you</b> &mdash; the two questions still open are marked '
      'as such, in their own boxes, and there are only two.</p>')
    A('</section>')

    # ---- A -------------------------------------------------------------------------------
    A('<section id="candidate-a">')
    A('<p class="gc-tag t-cm-legal">Candidate A</p>')
    A('<h2 class="t-ed-heading-3">The ruled gallery role &mdash; span grid, orphans tolerated</h2>')
    A('<p class="lede t-ed-body">Canon exactly as it renders today: each photograph&rsquo;s aspect '
      'ratio picks a compartment (3 columns at 6:1 and wider, 2 columns at 2.6:1, 2 rows for '
      'portraits), every 6th tile is promoted to 2&times;2, and the squaring pass is <b>off</b> so '
      'the bottom edge may be ragged. The picture is then fitted to the compartment with '
      '<code>object-fit: cover</code> &mdash; which means it is <b>cut</b>.</p>')

    A('<div class="sublabel t-ed-caption">A1 &mdash; canon&rsquo;s own default: 6 columns, %dpx row '
      'unit</div>' % unit)
    A('<div class="c-bento gc-a6" data-bento-role="gallery"><div class="c-bento__grid">')
    for p in photos:
        A(a_tile(p))
    A('</div></div>')
    A('<p class="note t-ed-body-small"><b>Where the cropping happens: everywhere.</b> At six '
      'columns a 1&times;1 compartment is taller than it is wide, so a 3:2 landscape loses '
      'roughly <b>%d%%</b> of its area (mean across the set <b>%d%%</b>, worst <b>%d%%</b>, '
      '<b>%d of %d</b> pictures cropped by more than 2%%). Portraits are cut too, in the other '
      'direction. Nothing on this wall is showing you the whole photograph.</p>'
      % (round(r6["crops"][1] * 100), round(r6["mean"] * 100), round(r6["worst"] * 100),
         r6["cropped"], len(photos)))
    A('<p class="note t-ed-body-small"><b>Where the ragged edge sits:</b> at the bottom, and also '
      '<i>inside</i> the wall &mdash; a tall portrait leaves a hole beside it that dense packing '
      'may or may not backfill. Measured on this set: %s. That is the ruled tolerance doing '
      'exactly what you exempted it for.</p>'
      % esc(" &middot; ".join("%d col: %d empty cell(s) over %d rows"
                              % (c, h[0], h[1]) for c, h in r6["holes"].items())).replace("&amp;", "&"))

    A('<div class="sublabel t-ed-caption">A2 &mdash; the same role dialled to 4 columns (what the '
      'roles page used)</div>')
    A('<div class="c-bento gc-a4" data-bento-role="gallery"><div class="c-bento__grid">')
    for p in photos:
        A(a_tile(p))
    A('</div></div>')
    A('<p class="note t-ed-body-small"><b>The dial is most of A&rsquo;s crop cost, so both are '
      'here.</b> At four columns the compartment is much closer to 3:2 and the mean crop falls '
      'from <b>%d%%</b> to <b>%d%%</b> (worst <b>%d%%</b>). Judging A on the six-column wall alone '
      'would be judging a strawman &mdash; but note that even at its kindest, A still crops, and '
      'the amount depends on a dial rather than on the picture.</p>'
      % (round(r6["mean"] * 100), round(r4["mean"] * 100), round(r4["worst"] * 100)))

    # ⬛ #219 — A4, NEW. `s218-D6 (4)` squares the Foundations photography page's wall, and none of
    # v1's walls showed what that looks like. It is drawn at the SAME 4-column dial as A2 so the
    # only variable between them is the squaring pass.
    # ⛔ SCOPED EXACTLY AS THE RULING SCOPES ITSELF: this is the photography page's INSTANCE, not
    # the gallery ROLE. A1/A2/A3 above stay ragged, because `s217-D3`'s role exemption is untouched
    # ("until he says wider") and squaring them here would enact a widening nobody ruled.
    A('<div class="sublabel t-ed-caption">A4 &mdash; the same 4-column wall with the edge dial at '
      'SQUARE, as the Foundations photography page now ships it (s218-D6&nbsp;(4))</div>')
    A('<div class="c-bento gc-a4" data-bento-role="gallery"><div class="c-bento__grid">')
    for p, s in zip(photos, sq_spans):
        A(a_tile(dict(p, span=s)))
    A('</div></div>')
    A('<p class="note t-ed-body-small"><b>This is the ruled instance, not a proposal.</b> Your '
      'four #218 exports all carried <code>edge: square</code> and you reopened it in as many '
      'words &mdash; <i>&ldquo;Reopen &mdash; square it&rdquo;</i>. <b>%d of %d photographs were '
      're-spanned</b> to close the wall; A2 above, the same wall with the dial at ragged, leaves '
      '<b>%s</b>. <b>The scope is the ruling&rsquo;s own:</b> <i>&ldquo;this enacts edge:square for '
      'the photography page&rsquo;s wall; the GALLERY ROLE&rsquo;s s217-D3 exemption elsewhere is '
      'untouched until he says wider&rdquo;</i> &mdash; which is why A1, A2 and A3 are still '
      'ragged, and still correct.</p>'
      % (len(sq_rep["changed"]), len(photos),
         esc(" &middot; ".join("%d col: %d hole(s)" % (c, hv[0])
                               for c, hv in r4["holes"].items())).replace("&amp;", "&")))
    # ⚠ NAMED, NOT SUMMARISED. "2 tiles re-spanned" hides whether one of them was a PORTRAIT
    # squashed into a single row to close a hole — which is precisely the cost Q3 is about. The
    # pass is cost-ordered to avoid it and it can still happen; if it did, it says so here.
    moved = []
    for i, (old, new) in enumerate(zip([p["span"] for p in photos], sq_spans), 1):
        if old != new:
            p = photos[i - 1]
            moved.append("%s (%s) %d&times;%d &rarr; %d&times;%d"
                         % (esc(p["file"]), esc(p["orient"]), old[0], old[1], new[0], new[1]))
    if moved:
        squashed = [m for m in moved if "(portrait)" in m and m.endswith("&times;1")]
        A('<p class="note t-ed-body-small"><b>What the squaring cost, tile by tile:</b> %s. %s</p>'
          % ("; ".join(moved),
             ("<b>&#9888; %d of those is a PORTRAIT flattened to one row</b> to close a hole "
              "&mdash; the pass is cost-ordered to avoid exactly that and it still happened here. "
              "That is the open question below, seen rather than argued." % len(squashed))
             if squashed else "No portrait was flattened to close a hole on this set."))
    A(recut.open_control_html("Q6"))

    A('<div class="sublabel t-ed-caption">A5 &mdash; the keyline dial at OFF: no borders, 1px '
      'gutter (s217-D5; the photography page&rsquo;s ruled setting, s218-D3)</div>')
    A('<div class="c-bento gc-atrial" data-bento-role="gallery"><div class="c-bento__grid">')
    for p in photos:
        A(a_tile(p))
    A('</div></div>')
    # ⛔ #219 — v1 called this "still proposed, still not ruled". It is not: `s217-D5` made
    # keylines a per-instance dial and `s218-D3` set the photography instance to OFF.
    A('<p class="note t-ed-body-small">Your #217 &ldquo;let&rsquo;s try dropping the '
      'keylines&rdquo; wall &mdash; <b>and you ruled it in, as a dial</b> (<code>s217-D5</code>: '
      '&ldquo;keylines on/off&rdquo;), then set the photography page to OFF in all four themes '
      '(<code>s218-D3</code>). Note what it does to the crop question: nothing. Removing the '
      'keylines makes the wall read as one surface, which arguably makes the inconsistent '
      'cropping <i>more</i> visible, not less.</p>')
    A(recut.open_control_html("Q3"))
    A('</section>')

    # ---- B -------------------------------------------------------------------------------
    A('<section id="candidate-b">')
    A('<p class="gc-tag t-cm-legal">Candidate B</p>')
    A('<h2 class="t-ed-heading-3">Justified rows &mdash; Flickr-style, with a widow switch</h2>')
    A('<p class="lede t-ed-body">Photographs are taken in order into a row until the row would '
      'drop below the <b>target height of %dpx</b>, then the whole row is scaled so it ends flush '
      'at both edges. <b>Row height varies; row width never does.</b> Every box carries its '
      'picture&rsquo;s own aspect ratio, so <b>nothing is cropped anywhere on this wall</b>.</p>'
      % unit)
    A('<p class="lede t-ed-body">The target is not a taste pick: <b>%dpx is the ruled row unit</b> '
      '(<code>layout/bento/row-unit</code>, s217-D2) and it is also Flickr&rsquo;s own default '
      'target row height. The two agree by coincidence, and the coincidence is worth knowing.</p>'
      % unit)
    A('<p class="lede t-ed-body">The last %d photographs cannot fill a row at that height. '
      'Flickr calls them <b>widows</b>, counts them, and gives you a switch. They are '
      '<b>not blown up</b> to justify &mdash; they keep the target height and the row simply ends '
      'where it ends.</p>' % len(widows))
    A('<input type="checkbox" id="gc-widows" class="gc-switch" checked>')
    A('<p class="gc-switchrow t-ed-body"><label for="gc-widows">'
      '<b>Widow count: %d</b> &mdash; <span class="gc-when-on">showing the short last row; '
      'untick to hide it</span><span class="gc-when-off">hidden, so every visible row is '
      'justified; tick to show it</span></label></p>' % len(widows))
    A('<div class="c-bento gc-b" data-bento-role="gallery">')
    idx = 0
    for r in rows:
        A('<div class="gc-brow">')
        for p in r:
            idx += 1
            A(b_tile(p, photos.index(p) + 1))
        A('</div>')
    if widows:
        A('<div class="gc-brow gc-brow--widow">')
        for p in widows:
            A(b_tile(p, photos.index(p) + 1, widow=True))
        A('</div>')
    A('</div>')
    A('<p class="note t-ed-body-small"><b>Where the row heights vary:</b> %d justified rows at '
      '%s &mdash; a range of <b>%dpx</b> around the %dpx target (%.0f%% either side). The row '
      'holding the portrait is the tall one: a portrait eats far less width per unit of height, '
      'so its row has to grow to fill the container. <b>That variation is the mechanism, not a '
      'defect</b> &mdash; it is what buys the flush edges.</p>'
      % (len(rows), esc(" / ".join("%dpx" % round(h) for h in heights)),
         round(max(heights) - min(heights)), unit,
         max(abs(max(heights) - unit), abs(unit - min(heights))) / unit * 100))
    A('<p class="note t-ed-body-small"><b>Where the ragged edge sits:</b> in one place only, the '
      'last row, and it is switchable. There are no holes anywhere else &mdash; that is the whole '
      'point of justification, and it is the sharpest visible difference from A.</p>')
    A('<p class="note t-ed-body-small"><b>The honest cost of doing this at mint time.</b> The row '
      'membership is decided here, in the generator, against the page&rsquo;s own %dpx content '
      'width. The rows stay flush at every width &mdash; the browser redistributes the space '
      '&mdash; but they stay <i>the same rows</i>, so they get shorter as the window narrows '
      'instead of re-packing. Flickr re-packs at runtime. A shipped B would need either a packing '
      'per responsive band or a runtime pass; <b>A re-flows for free</b>. Narrow your window and '
      'you will see both behaviours.</p>' % int(NOMINAL_W))
    # ⬛ THE TWO GENUINELY-OPEN QUESTIONS ON THIS PAGE. v1 declared both costs in prose and put
    # neither as a question, so both were invisible as decisions.
    A(recut.open_control_html("Q11"))
    A(recut.open_control_html("Q12"))
    A('</section>')

    # ---- the differences, side by side ----------------------------------------------------
    A('<section id="differences">')
    A('<h2 class="t-ed-heading-3">The differences, as measured</h2>')
    A('<table class="gc-diff t-ed-body-small"><thead><tr><th></th>'
      '<th>A &mdash; span grid (ruled)</th><th>B &mdash; justified rows (proposed)</th>'
      '</tr></thead><tbody>')
    for k, a, b in [
        ("Cropping",
         "Every picture, %d%% of area on average at 6 columns and %d%% at 4 &mdash; "
         "worst tile %d%%." % (round(r6["mean"] * 100), round(r4["mean"] * 100),
                               round(r6["worst"] * 100)),
         "None. The compartment is minted from the picture&rsquo;s own ratio."),
        ("Side edges", "Flush &mdash; the grid guarantees it.", "Flush &mdash; the scaling "
         "guarantees it."),
        ("Bottom edge", "Ragged, and holes may also appear mid-wall beside a tall portrait. "
         "Ruled acceptable (s217-D3).",
         "Ragged in the last row only, never mid-wall, and hideable with the switch."),
        ("Row height", "Fixed &mdash; the %dpx row unit for every row." % unit,
         "Varies: %s on this set." % " / ".join("%dpx" % round(h) for h in heights)),
        ("Portraits", "Two rows tall, cropped to a 1&times;2 compartment.",
         "Full height, uncropped, and they make their row taller."),
        ("Emphasis rhythm", "Every 6th tile promoted to 2&times;2 (s217-D2).",
         "None here. Flickr&rsquo;s equivalent is a full-width breakout every n rows, guarded to "
         "landscape pictures &mdash; a separate question if you go this way."),
        ("Responsive", "Re-flows at the 1100 / 820 / 520 bands for free.",
         "Rows keep their membership and shorten; a per-band mint or a runtime pass would be owed."),
        ("Nesting", "Works &mdash; it is a bento, so it can be a tile of another bento.",
         "Untested. B is a flex column, not a grid; whether it nests is an open question."),
    ]:
        A('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (k, a, b))
    A('</tbody></table>')
    # ⛔ #219 — v1 closed this table by re-putting the whole A-or-B question ("If the answer is no,
    # A cannot do it at any dial and B is the layout"). `s217-D5` had already answered it. The
    # replacement states the ruling and points at what a real instance chooses.
    A('<p class="note t-ed-body-small"><b>What this table is now for.</b> Not choosing between A '
      'and B &mdash; <code>s217-D5</code> made both of them positions of a per-instance <b>mode</b> '
      'dial, so the table is what an instance is choosing between when somebody sets that dial. '
      'The real question underneath, and it is a per-instance one, is whether <i>that</i> gallery '
      'of licensed photography may crop its photographs: where the answer is no, A cannot do it at '
      'any column count and B is the mode. The Foundations photography page&rsquo;s answer is '
      'already recorded &mdash; <b>bento mode, squared</b> (<code>s218-D3</code>, '
      '<code>s218-D6&nbsp;(4)</code>).</p>')
    A('</section>')

    # ---- provenance -----------------------------------------------------------------------
    A('<section id="provenance">')
    A('<h2 class="t-ed-heading-3">What is canon here and what is proposed</h2>')
    A('<p class="lede t-ed-body"><b>Canon, untouched:</b> candidate A&rsquo;s container, grid, '
      'span vocabulary, responsive bands, gallery role rule and the %dpx caption space all come '
      'from <code>knowledge/canon/canon.css</code>. This page declares no grid, no span and no '
      'role rule for A. <b>Proposed:</b> everything in candidate B, whose rows are a page-local '
      'flex layout because canon has no grammar for justified rows &mdash; that is what the '
      'decision would create.</p>' % space)
    A('<p class="note t-ed-body-small">Both candidates read the same manifest rows through the '
      'same function as the ruled roles page (<code>gen_bento_roles_217.read_photos</code>), so '
      'the photographs, their order and their derived spans cannot differ between them. '
      'Photographs are the committed web derivatives (s217-D1); licences are on every caption.</p>')
    A('<p class="note t-ed-body-small">Probe: <code>knowledge/_render/verify_gallery_compare_217.py'
      '</code> &mdash; drives this page in all four themes &times; light/dark, measures every B '
      'row flush to the container at several widths, checks every rendered box against its '
      'manifest ratio, drives the widow switch, and has a mutation arm that breaks the justify '
      'maths and must go red.</p>')
    A('</section>')
    return "\n".join(S)


def page(photos, rows, widows, reps):
    # ⚠ THE RE-CUT BLOCKS GO IN THE HEAD, before the minted per-photograph rules: the s218-D6(1)
    # mono ground is tile CONTENT and must not out-order the per-photograph geometry.
    css = (CSS_HEAD
           .replace("__MONOCAP__",
                    recut.mono_caption_css([(".gc-cap", [".gc-cap .gc-desc", ".gc-cap .gc-lic"])]))
           .replace("__RECUT__", recut.RECUT_CSS)
           + photo_rules(photos) + "\n")
    return ((HEAD
             .replace("__TITLE__", "Apollo &mdash; gallery: span grid or justified rows")
             .replace("__SENTINEL__", SENTINEL)
             .replace("__UP__", UP)
             .replace("__CSS__", css)
             .replace("__H1__", "Gallery &mdash; A or B")
             .replace("__SUBTITLE__",
                      "PROPOSED &middot; span grid vs justified rows &middot; four themes"))
            + build(photos, rows, widows, reps) + TAIL.replace("__SCRIPT__", SCRIPT))


def assemble():
    photos, residuals = read_photos()
    for p in photos:
        p["ar"] = (float(p["w"]) / float(p["h"])) if (p["w"] and p["h"]) else 1.0
    rows, widows = pack_rows(photos)
    reps = {"a6": a_wall_report(photos, 6), "a4": a_wall_report(photos, 4)}
    return photos, rows, widows, reps, residuals


def main():
    global BREAK_JUSTIFY
    argv = sys.argv[1:]
    out = OUT
    if "--break-justify" in argv:
        # ⬛ THE MUTATION HANDLE. Every non-widow tile loses its proportional flex-grow, so the rows
        # stop justifying and end short of the container edge. The probe's flush assertion must go
        # RED — a gate never seen to fail is not a gate ([[instrument-without-a-consumer]]).
        BREAK_JUSTIFY = True
        out = OUT.replace(".html", "-BROKEN.html")
    for i, a in enumerate(argv):
        if a == "--out":
            out = argv[i + 1]
    photos, rows, widows, reps, residuals = assemble()
    if not photos:
        sys.exit("REFUSED — no committed photography derivatives; both walls would be empty")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page(photos, rows, widows, reps))
    heights = [(NOMINAL_W - (len(r) - 1) * PACK_GUTTER) / sum(p["ar"] for p in r) for r in rows]
    print("Wrote %s  (%d photographs, %d landscape / %d portrait)"
          % (out, len(photos),
             sum(1 for p in photos if p["orient"] == "landscape"),
             sum(1 for p in photos if p["orient"] == "portrait")))
    if BREAK_JUSTIFY:
        print("  ⬛ MUTATION ARM — flex-grow zeroed; B's rows must measure SHORT of the container")
    print("  A: squaring %s (s217-D3) · crops mean/worst — 6 col %.0f%%/%.0f%% · 4 col %.0f%%/%.0f%%"
          % ("OFF" if not role_policy("gallery")["squaring"] else "ON",
             reps["a6"]["mean"] * 100, reps["a6"]["worst"] * 100,
             reps["a4"]["mean"] * 100, reps["a4"]["worst"] * 100))
    for cols, rep in (("6", reps["a6"]), ("4", reps["a4"])):
        print("     %s-col holes by band: %s" % (cols, dict((k, v[0]) for k, v in rep["holes"].items())))
    print("  B: target %.0fpx (layout/bento/row-unit) at nominal %.0fpx — %d row(s) %s, %d widow(s)"
          % (target_row_height(), NOMINAL_W, len(rows),
             "/".join("%.0f" % h for h in heights), len(widows)))
    print("     row membership: %s | widows: %s"
          % (" | ".join(",".join(p["orient"][:4] for p in r) for r in rows),
             ",".join(p["orient"][:4] for p in widows)))
    # ⚠ B's STRESS CASE, reported by position: a portrait inside a JUSTIFIED row is what pushes
    # that row's height away from the target. A set where every portrait fell into the widow row
    # would leave B's row maths untested, so this is printed, never assumed.
    mid = ["row %d position %d of %d" % (i, j, len(r))
           for i, r in enumerate(rows, 1)
           for j, p in enumerate(r, 1) if p["orient"] == "portrait"]
    print("     portrait inside a justified row: %s"
          % ("; ".join(mid) if mid else "NONE — B's stress case is UNTESTED on this set"))
    if residuals.get("missing_derivative_file"):
        print("  residual — manifest rows with no file: %s"
              % ", ".join(residuals["missing_derivative_file"]))
    return 0


def selftest():
    """8 bites: A declares no structure · B cannot reach A · one data path · the packing justifies
    arithmetically · widows are not scaled · the widow switch is CSS-only · the ruled numbers come
    from canon · the mutation handle actually mutates."""
    global BREAK_JUSTIFY
    photos, rows, widows, reps, res = assemble()
    h = page(photos, rows, widows, reps)
    css = h.split("<style>", 1)[1].split("</style>", 1)[0]
    body = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules = re.findall(r"([^{}]+)\{([^{}]*)\}", body)

    # --- bite 1: candidate A's structure is CANON'S, not this page's -------------------------
    for sel, decls in rules:
        if "gc-b" in sel or "gc-brow" in sel or "gc-box" in sel:
            continue
        for banned in ("grid-template-columns", "grid-auto-rows", "grid-auto-flow", "gap:"):
            assert banned not in decls or "gc-a" not in sel, (
                "bite 1a FAIL: %r declares %s — candidate A must be canon's own output, or the "
                "comparison is against a drawing of A" % (sel.strip(), banned))
        if "c-bento" in sel and "border-radius" in decls:
            raise AssertionError("bite 1b FAIL: %r declares a bento radius of its own" % sel.strip())

    # --- bite 2: candidate B's declarations cannot reach candidate A -------------------------
    # ⚠ THE FAILURE THIS CATCHES: a proposal that restyles the ruled variant beside it turns the
    # side-by-side into a comparison of a thing with itself.
    for sel, decls in rules:
        if any(t in sel for t in ("gc-brow", "gc-box", "gc-btile", "gc-widow", "gc-switch")):
            assert "gc-atile" not in sel and "c-bento__grid" not in sel, \
                "bite 2 FAIL: %r is a candidate-B rule that reaches candidate A" % sel.strip()
    assert ".c-bento.gc-b{" in body.replace(" ", "") or ".c-bento.gc-b {" in body, \
        "bite 2b FAIL: B's container dial is not written at (0,2,0) and canon's role rule would " \
        "beat it silently"

    # --- bite 3: ONE data path — the same files in the same order in both candidates ---------
    asec = h.split('<section id="candidate-a">', 1)[1].split("</section>", 1)[0]
    bsec = h.split('<section id="candidate-b">', 1)[1].split("</section>", 1)[0]
    a_files = re.findall(r'photography-web/([^"]+)"', asec)
    b_files = re.findall(r'photography-web/([^"]+)"', bsec)
    a_first = a_files[:len(photos)]
    assert a_first == b_files, \
        "bite 3 FAIL: A and B are not showing the same photographs in the same order — the " \
        "comparison would be a lie (A %r vs B %r)" % (a_first[:3], b_files[:3])
    assert len(b_files) == len(photos), \
        "bite 3b FAIL: B renders %d of %d photographs" % (len(b_files), len(photos))

    # --- bite 4: the packing ARITHMETIC justifies -------------------------------------------
    # Every non-widow row, at the nominal width, must land within 0.5px of the container.
    for i, r in enumerate(rows, 1):
        avail = NOMINAL_W - (len(r) - 1) * PACK_GUTTER
        hgt = avail / sum(p["ar"] for p in r)
        widths = sum(hgt * p["ar"] for p in r) + (len(r) - 1) * PACK_GUTTER
        assert abs(widths - NOMINAL_W) < 0.5, \
            "bite 4 FAIL: minted row %d totals %.2fpx against a %.0fpx container" % (i, widths, NOMINAL_W)
        assert hgt >= target_row_height() * 0.5, \
            "bite 4b FAIL: minted row %d is %.0fpx, less than half the target — the packing " \
            "closed a row it should have kept filling" % (i, hgt)
    assert widows, "bite 4c FAIL: no widows on this set, so the widow switch has nothing to " \
                   "drive and a green probe would prove nothing about it"

    # --- bite 5: portraits are the stress case and must sit INSIDE a justified row -----------
    assert any(p["orient"] == "portrait" for r in rows for p in r), \
        "bite 5 FAIL: every portrait landed in the widow row — B's row maths is untested against " \
        "the shape that stresses it"

    # --- bite 6: the widow switch is CSS-only and the widows are NOT scaled up ---------------
    script = h.split("<script>", 1)[1]
    assert "gc-widow" not in script and "checkbox" not in script, \
        "bite 6a FAIL: the widow switch has reached the script — it is specified as no-JavaScript"
    assert ".gc-switch:not(:checked) ~ .gc-b .gc-brow--widow{display:none;}" in body, \
        "bite 6b FAIL: the CSS-only widow switch rule is missing"
    wid = [d for s, d in rules if "gc-brow--widow" in s and "gc-btile" in s]
    assert wid and "flex:0 1 auto" in wid[0].replace(" ", " ") and "row-unit" in wid[0], \
        "bite 6c FAIL: widows do not keep the target height — a widow row that is allowed to grow " \
        "is exactly the behaviour Flickr's rule exists to prevent (%r)" % wid

    # --- bite 7: the ruled numbers are canon's, never restated here ---------------------------
    space, _ = caption_space()
    capdecls = " ".join(d for s, d in rules if "gc-cap" in s)
    assert "min-height" not in capdecls, \
        "bite 7a FAIL: the page restates the ruled caption height; it must come from canon"
    assert str(space) not in body, \
        "bite 7b FAIL: the ruled caption number %d appears in the page stylesheet" % space
    assert "var(--layout-bento-row-unit)" in body, \
        "bite 7c FAIL: the widow width is not reading the ruled row unit from the token cascade"
    assert "c-bento__caption" in asec and "c-bento__caption" in bsec, \
        "bite 7d FAIL: one candidate is not using canon's caption slot, so the two are being " \
        "compared with different caption regimes"

    # --- bite 7e (#219): the ledger, the mono ground, and nothing settled offered as a control --
    dsec = h.split('<section id="decided">', 1)[1].split("</section>", 1)[0]
    assert "<s>" in dsec, "bite 7e FAIL: no question is struck — the re-cut did nothing"
    assert "not ruled" not in h.split('<section id="intro">', 1)[1].split("</section>", 1)[0].lower(), \
        "bite 7f FAIL: the intro still calls this page unruled. s217-D5 answered A-or-B with a " \
        "per-instance dial; re-putting it is the #219 defect"
    assert "surface-digital-black" in body and "text-reverse" in body, \
        "bite 7g FAIL: the s218-D6(1) mono caption ground is not on the page"
    assert "s218-D6" in asec, \
        "bite 7h FAIL: candidate A does not show the ruled squared instance — the page would " \
        "still be showing a ragged edge as the only thing a gallery wall can do"
    for r in recut.rows_for("compare"):
        if r["state"] == recut.RULED:
            assert 'Open &middot; %s' % r["key"] not in h, \
                "bite 7i FAIL: %s is RULED and is being offered as a live control" % r["key"]
    # ⚠ THE SCOPE ASSERTION. A4 is the photography page's INSTANCE. A1/A2/A3/A5 must stay ragged,
    # or this page would have widened s218-D6(4) to the gallery ROLE by drawing it that way.
    p4 = params()
    a_walls = re.findall(r'<div class="c-bento gc-a\w*" data-bento-role="gallery">'
                         r'<div class="c-bento__grid">(.*?)</div></div>', asec, re.S)
    assert len(a_walls) == 4, "bite 7j FAIL: expected four A walls, found %d" % len(a_walls)
    ragged = [w for w in (a_walls[0], a_walls[1], a_walls[3])]
    for i, w in enumerate(ragged):
        sp = [(int(a), int(b)) for a, b in re.findall(r'data-c="(\d)" data-r="(\d)"', w)]
        assert sp == [p["span"] for p in photos], \
            "bite 7k FAIL: A wall %d was squared. s218-D6(4) scopes itself to the photography " \
            "page's wall and leaves the GALLERY ROLE's s217-D3 exemption untouched — squaring " \
            "these would enact a widening nobody ruled" % (i + 1)

    # --- bite 8: the mutation handle actually mutates ------------------------------------------
    try:
        BREAK_JUSTIFY = True
        mut = page(photos, rows, widows, reps)
    finally:
        BREAK_JUSTIFY = False
    mcss = mut.split("<style>", 1)[1].split("</style>", 1)[0]
    assert "flex-grow:0;" in mcss and "flex-grow:1.4" not in mcss, \
        "bite 8a FAIL: --break-justify left the proportional grow in place, so the mutation arm " \
        "would go green against a page that was never mutated"
    assert "flex-basis:auto" in mcss and "var(--layout-bento-row-unit)" in mcss, \
        "bite 8b FAIL: the mutant does not size its boxes at all — a mutation that collapses the " \
        "layout is caught by any assertion and proves nothing about the FLUSH one"

    print("gen_gallery_compare_217 selftest OK (8 bites: A is canon's own output · B cannot reach "
          "A · ONE data path, same photos same order · the packing justifies arithmetically · a "
          "portrait sits mid-row · the widow switch is CSS-only and widows are unscaled · the "
          "ruled numbers come from canon · the mutation handle mutates)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        sys.exit(main())
