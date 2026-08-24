#!/usr/bin/env python3
"""
gen_bento_roles_217.py — the BENTO ROLES demo page (s217-D3, #217). For Dave's eye.

Builds `reviews/BENTO-CANON-2026-08-23-v3.html`: one section per ROLE — dashboard,
brochureware, gallery — in four themes x light/dark, with **console as the opening theme**
because console is the only theme whose radius token is non-zero and therefore the only one
where the difference between the three roles is VISIBLE. (The grammar is identical in all
four; elsewhere the same rules resolve to 0 and nothing moves. The page says so, and the
theme switch lets Dave prove it.)

⚠ v3, NOT an overwrite of v2. `BENTO-CANON-2026-08-23-v2.html` is the s217-D2 page and stays
exactly as it is, with its own generator and its own probe. This page is the s217-D3 refinement.

WHAT EACH SECTION SHOWS (s217-D3, Dave's own three cases)
  1 · DASHBOARD — a bento of bentos. The theme radius sits on each INNER bento's container,
      its tiles are square and 1px apart, and the OUTER wall keeps the theme gutter. That last
      clause is the whole point of the role and the easiest thing to get wrong: a blanket 1px
      would collapse the structure the role exists to describe.
  2 · BROCHUREWARE — the TILES carry the radius and the spacing; the container is square and
      does not clip.
  3 · GALLERY — radius and spacing as brochureware, the generous caption space, and the
      squaring pass RELAXED: orphans are acceptable here.

⬛ THE KEYLINE-LESS GALLERY IS A TRIAL — **PROPOSED, NOT RULED**. Dave's word was "lets… try":
keylines dropped entirely, nothing but a 1px gutter and row space. It is shown SIDE BY SIDE
with the ruled keylined gallery so he can rule by eye. Every declaration that belongs to the
trial names `.dx-trial` in its selector, and `--selftest` bite 6 enforces that — a trial that
leaks its styles into the ruled variant would be a decision taken by accident.

⛔ THE PAGE MINTS NOTHING. Every structural rule comes from canon.css's AUTO-BENTO block. The
page-local stylesheet styles TILE CONTENT and chrome, declares no grid, no gap, no bento radius
and no role rule of its own.

⚠ SQUARING IS ASKED, NEVER RE-DECIDED. `canon/gen_canon_bento.square_wall_for_role()` is the one
place the ruled policy lives; this page passes a role and takes what it is given. An
`if role == "gallery"` here would be a second source for a ruled fact.

✅ AND THE INNER WALLS RUN IT TOO (s217-D7). The dashboard section mints BOTH levels in ONE call
to `square_nested_wall()` — the outer wall of sections and every inner wall's tiles. Two separate
calls would leave exactly the hole #217 measured: the level somebody remembered gets squared and
the level nobody looked at keeps its authored literals.

⚠ EXEMPT FROM SQUARING IS NOT EXEMPT FROM THE ASPECT MAPPING. The gallery walls still run
`span_for()`, so portraits are still two rows tall — that mapping IS the "appropriate layout for
portrait and landscape images" the role asks for. They are different mechanisms.

Usage:
  python3 knowledge/_render/gen_bento_roles_217.py
  python3 knowledge/_render/gen_bento_roles_217.py --wrong-role   # mutation arm -> *-WRONGROLE.html
  python3 knowledge/_render/gen_bento_roles_217.py --selftest
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
from gen_canon_bento import (params, span_for, emphasise, roles, role_policy,  # noqa: E402
                             caption_space, square_wall_for_role, is_rectangular,
                             band_ladder, place, band_clamp, square_nested_wall,
                             inner_ladder)

OUT = os.path.join(ROOT, "reviews", "BENTO-CANON-2026-08-23-v3.html")
# The inner instances' column dial, declared ONCE. ⚠ It must agree with `.dx-dash-inner`'s
# `--bento-columns` in the stylesheet below, or the pass squares a wall the page never renders.
DASH_INNER_COLS = 3
PHOTO_MANIFEST = os.path.join(KNOW, "_PHOTOGRAPHY-MANIFEST.json")
UP = "../"
SENTINEL = "<!-- APOLLO BENTO-ROLES DEMO (gen_bento_roles_217.py) — s217-D3 -->"

# ⬛ THE MUTATION HANDLE. Rewrites every role attribute the page emits to ONE wrong role, so the
# per-role probe can be seen to go RED. A gate that has never been seen to fail is not a gate
# ([[instrument-without-a-consumer]]). Never writes over the real page.
WRONG_ROLE = None
SQUARE_REPORTS = []


def esc(s):
    return htmlmod.escape(str(s if s is not None else ""), quote=True)


def role_attr(role):
    """The role attribute, honouring the mutation handle. ⚠ ONE emission point: a role written
    by hand anywhere else in this file would be invisible to `--wrong-role`, and the mutation
    arm would go green while the page it built was not actually mutated."""
    return ' data-bento-role="%s"' % esc(WRONG_ROLE or role)


# ---------------------------------------------------------------------------- photographs
def read_photos():
    """The manifest's own rows that carry a committed derivative. Spans DERIVED."""
    if not os.path.exists(PHOTO_MANIFEST):
        return [], {"manifest": "MISSING"}
    d = json.load(open(PHOTO_MANIFEST, encoding="utf-8"))
    rows, missing = [], []
    web = os.path.join(KNOW, "assets", "photography-web")
    for r in d.get("rows", []):
        deriv = r.get("derivative")
        if not deriv:
            continue
        if not os.path.exists(os.path.join(web, deriv)):
            missing.append(deriv)
            continue
        px = r.get("derivative_px") or ""
        w = h = None
        if "x" in px:
            try:
                w, h = (int(x) for x in px.split("x", 1))
            except ValueError:
                w = h = None
        desc = r.get("exif_description") or "UNKNOWN"
        rows.append({"file": deriv, "w": w, "h": h,
                     "orient": r.get("orientation") or "UNKNOWN",
                     "licence": r.get("licence_source") or "UNKNOWN",
                     "desc": desc if len(desc) <= 130 else desc[:129].rsplit(" ", 1)[0] + "…"})
    rows.sort(key=lambda r: r["file"])
    p = params()
    for i, r in enumerate(rows, 1):
        r["span"] = emphasise(span_for(r["w"], r["h"], p), i, p)
    return rows, {"missing_derivative_file": missing}


def wall(spans, role, columns=None):
    """-> (spans, report) for ONE wall, at its own instance ladder and its ROLE'S policy.

    ⚠ The ladder follows the INSTANCE column dial, not canon's default — a 3-column inner bento
    never renders at 6, and squaring it against 6 would refuse a wall that is rectangular at
    every width it is ever seen at."""
    p = params()
    ladder = band_ladder(p if columns is None else dict(p, columns=columns))
    out, rep = square_wall_for_role(spans, role, ladder=ladder)
    rep["wall_role"] = role
    SQUARE_REPORTS.append(rep)
    return out, rep


# ---------------------------------------------------------------------------- tiles
def photo_tile(r, extra_class="", caption=True):
    c, rw = r["span"]
    cap = ('<figcaption class="c-bento__caption dx-cap">'
           '<span class="dx-desc t-ed-caption">%s</span>'
           '<span class="dx-lic t-cm-legal">%s</span></figcaption>'
           % (esc(r["desc"]), esc(r["licence"]))) if caption else ""
    return ('<figure class="c-bento__tile dx-photo %s" data-c="%d" data-r="%d">'
            '<img class="dx-img" src="%sknowledge/assets/photography-web/%s" alt="%s"'
            ' loading="lazy" width="%s" height="%s">%s</figure>'
            % (extra_class, c, rw, UP, esc(r["file"]), esc(r["desc"]),
               r["w"] or "", r["h"] or "", cap))


CARDS = [
    ("Balance", "Current account", "£18,420.66", 2, 1),
    ("Runway", "at today’s burn", "7.4 months", 1, 1),
    ("Payments due", "next 30 days", "14", 1, 1),
    ("FX exposure", "GBP / USD / EUR", "3 pairs", 2, 2),
    ("Approvals", "waiting on you", "5", 1, 1),
    ("Cards", "active", "27", 1, 1),
    ("Invoices", "overdue", "2", 2, 1),
    ("Sweep", "nightly", "on", 1, 1),
    ("Nostro", "reconciled", "99.2%", 1, 1),
]

# Brochureware panels — authored spans, marketing rhythm rather than a data wall.
PANELS = [
    ("Discover", "Bring the brief, the brand and the constraints into one place.", 3, 1),
    ("Create", "Generate real, on-rails candidates instead of a blank canvas.", 3, 1),
    ("Craft", "Tune every dial by eye, with the system holding the guard-rails.", 2, 1),
    ("Dispatch", "Ship the artefact and the record of how it was decided, together.", 2, 1),
    ("On rails", "Nothing you build can leave the design system behind.", 2, 1),
]


def card_tile(card, extra_class=""):
    label, sub, fig, c, r = card
    return ('<div class="c-bento__tile dx-card %s" data-c="%d" data-r="%d">'
            '<span class="dx-eyebrow t-cm-legal">%s</span>'
            '<span class="dx-sub t-cm-legal">%s</span>'
            '<span class="dx-fig t-ed-heading-4">%s</span></div>'
            % (extra_class, c, r, esc(label), esc(sub), esc(fig)))


def panel_tile(panel, span, extra_class=""):
    label, body, _c, _r = panel
    return ('<div class="c-bento__tile dx-panel %s" data-c="%d" data-r="%d">'
            '<span class="dx-eyebrow t-cm-legal">%s</span>'
            '<span class="dx-body t-ed-body">%s</span></div>'
            % (extra_class, span[0], span[1], esc(label), esc(body)))


# ---------------------------------------------------------------------------- page-local CSS
# ⛔ NO GRID, NO GAP, NO BENTO RADIUS, NO ROLE RULE HERE. Structure and role are canon's.
CSS = """
/* ===========================================================================
   BENTO ROLES DEMO — page-local styles, scoped to `.dx`.
   ⛔ STRUCTURE AND ROLE ARE NOT DECLARED HERE. The container, the grid, the
   span vocabulary, the responsive bands, the three role rules and the gallery
   caption space all come from canon.css's AUTO-BENTO block. This file styles
   TILE CONTENT and page chrome only — which is why the page is a test of the
   role grammar and not a re-drawing of it.
   ⚠ Every var() below carries a literal fallback EXCEPT the --bento-* dials in
   the instance blocks: a fallback there would mask the very failure the probe
   exists to catch (a theme override or a role rule that never landed).
   =========================================================================== */
.dx{
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
.dx *{box-sizing:border-box;}
.dx :focus-visible{outline:var(--focus-w) solid var(--focus); outline-offset:2px;}
html,body{margin:0;}
body{background:var(--background-default,#FFFFFF);}
/* ⚠ the ink is restated on a CHILD of the themed element — measured #217: an element that BOTH
   carries data-theme and reads --text-default disagreed with its own children in supercharge. */
.dx, header.app{color:var(--text-default,#1A1A1A);}

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

main{padding:var(--sp-6); max-width:1400px;}
section{margin:0 0 var(--sp-7); scroll-margin-top:80px;}
h2{margin:0 0 var(--sp-1);}
p.lede{margin:0 0 var(--sp-5); color:var(--ink-2); max-width:74ch;}
.sublabel{color:var(--ink-2); text-transform:uppercase; letter-spacing:0.14em;
  margin:0 0 var(--sp-3); display:flex; align-items:center; gap:var(--sp-2);}
.sublabel::before{content:''; width:20px; height:1px; background:var(--line);}
.dx a{color:inherit;}
.dx code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:12px;
  background:var(--surface-2,#F3F3F3); padding:0 .3em;}
.note{margin:var(--sp-3) 0 0; color:var(--ink-2); max-width:74ch;}
.note b{color:var(--ink);}
.badge{display:inline-block; border:1px solid var(--line-2,#767676); color:var(--ink,#1A1A1A);
  padding:2px 8px; letter-spacing:0.12em; text-transform:uppercase; margin:0 0 var(--sp-3);}

/* ---- the ONE thing that makes the CONTAINER radius visible: a ground behind the bento ----
   ⚠ A structural component must not decide a surface (out of scope, s217-D2), so the DEMO gives
   the container a ground. Without it a rounded container has nothing to round. It is given to
   the DASHBOARD role only — that is the role whose radius lives on the container, and painting
   a ground behind a brochureware wall would draw a box the role does not have. */
.dx .c-bento[data-bento-role="dashboard"]{background:var(--surface-2,#F3F3F3);}

/* ---- tile content ---- */
.dx-photo{margin:0; display:grid; grid-template-rows:1fr auto;
  background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);}
.dx-img{display:block; width:100%; height:100%; min-height:0; object-fit:cover;
  background:var(--surface-2,#F3F3F3);}
/* ⚠ the caption's SPACE is canon's (`.c-bento__caption`, s217-D3). What is here is only its
   inline padding, its colour and its clamp — the block height and the line allowance are the
   ruled numbers and this page must not restate them. */
.dx-cap{padding-inline:var(--sp-3); color:var(--ink-2,#545454); display:flex;
  flex-direction:column; gap:2px; justify-content:center;}
.dx-desc{display:-webkit-box; -webkit-line-clamp:var(--bento-caption-lines,2);
  -webkit-box-orient:vertical; overflow:hidden;
  /* ds-005/ds-048: a clamped label opts out of the cap/alphabetic trim or its last visible
     line loses its descenders. */
  text-box-edge:text text;}
.dx-lic{color:var(--ink-2,#545454);}
.dx-card{background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);
  padding:var(--sp-4); overflow:hidden; display:flex; flex-direction:column; gap:var(--sp-1);}
.dx-panel{background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);
  padding:var(--sp-5); overflow:hidden; display:flex; flex-direction:column; gap:var(--sp-3);}
.dx-eyebrow{color:var(--ink,#1A1A1A);}
.dx-sub{color:var(--ink-2,#545454);}
.dx-body{color:var(--ink-2,#545454);}
.dx-fig{margin-top:auto; font-variant-numeric:tabular-nums;}

/* ---- INSTANCE PARAMETER SETS — declared rules, never a style="" attribute ---------------
   ⚠ DECLARED, and the reason is measured (#217): an inline custom property is invisible to
   every instrument that resolves the stylesheet against the document, and it beats container
   queries outright, which would make the canon bands silently inert.
   ⚠ AND THEY CARRY `.c-bento` IN THE SELECTOR. The role rules in canon are (0,2,0); a bare
   class is (0,1,0) and the role would win. `.c-bento.dx-…` matches the role's specificity and
   this stylesheet loads after canon.css, so the instance dial takes it on source order. */
/* ⚠ THE OUTER WALL'S ROWS ARE INTRINSIC, and the reason is measured (#217, seen in a render):
   with canon's fixed 320px row unit the outer row is shorter than the inner wall inside it, and
   `overflow:hidden` — which the dashboard role needs for its container radius — CLIPS the inner
   wall's last row without a scrollbar or any other symptom. An outer wall whose tiles are whole
   bentos has to size to them. */
.c-bento.dx-dash-outer{--bento-row-unit:auto;}
.c-bento.dx-dash-inner{--bento-columns:__DASH_INNER_COLS__; --bento-row-unit:150px;}
.c-bento.dx-broch{--bento-row-unit:200px;}
.c-bento.dx-gal{--bento-columns:4; --bento-row-unit:200px;}

/* ---- THE KEYLINE TRIAL — ⬛ PROPOSED, NOT RULED (s217-D3, Dave: "lets… try") ------------
   Keylines dropped entirely; nothing but a 1px gutter and row space. EVERY declaration below
   names `.dx-trial`, and --selftest bite 6 enforces that: a trial that leaks its styles into
   the ruled gallery variant beside it would be a decision taken by accident, and the
   side-by-side comparison Dave is ruling on would be comparing a thing with itself. */
.c-bento.dx-trial{--bento-columns:4; --bento-row-unit:200px; --bento-gutter:1px;}
.dx-trial .dx-photo{border:0;}
.dx-trial .dx-cap{padding-inline:var(--sp-2);}

/* the two galleries, one above the other at full width — ⚠ NOT half-width columns: two
   half-width walls sit below the 820 band and would both collapse to two columns, so the
   comparison would be of two collapsed walls rather than the layouts being ruled on. */
.dx-2up{display:flex; flex-direction:column; gap:var(--sp-6);}
.dx-2up > div{min-width:0;}
.dx-caption{color:var(--ink-2,#545454); margin:var(--sp-2) 0 0; display:block;}

@media (prefers-reduced-motion: reduce){
  .dx *,.dx *::before,.dx *::after{transition-duration:.01ms !important;
    animation-duration:.01ms !important;}
}
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
  // a fragment-only navigation does not re-run this script — the probe drives the page by hash
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
<body data-theme="light" data-chrome="1" class="dx canon">
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


def build(photos, residuals):
    p = params()
    space, lines = caption_space()
    S = []
    A = S.append

    # ---- 0 · what a role is -------------------------------------------------------------
    A('<section id="intro">')
    A('<h2 class="t-ed-heading-3">Three roles, one grammar</h2>')
    A('<p class="lede t-ed-body">You said a page-level bento and a sectioned one are not the '
      'same thing. They are now three <b>roles</b>, and the role decides where the corner radius '
      'sits, what the spacing is, and whether the wall is squared off. Everything else &mdash; '
      'the columns, the bands, the span vocabulary, the portrait rule &mdash; is unchanged and '
      'shared.</p>')
    A('<p class="lede t-ed-body"><b>The page opens in console on purpose.</b> Console is the only '
      'theme whose corner radius is not zero, so it is the only theme where you can <i>see</i> '
      'the difference between the three roles. The grammar is identical in all four: switch the '
      'theme above and the same rules simply resolve to a radius of 0. Nothing else moves.</p>')
    A('</section>')

    # ---- 1 · DASHBOARD ------------------------------------------------------------------
    A('<section id="dashboard">')
    A('<h2 class="t-ed-heading-3">Dashboard &mdash; radius on each inner container, tiles 1px apart</h2>')
    A('<p class="lede t-ed-body">A sectioned app: a bento of bentos. <b>The radius sits on each '
      'inner bento&rsquo;s container</b> and the tiles inside it are square and one pixel apart, '
      'so each section reads as one rounded slab of information. The <b>outer</b> wall keeps the '
      'theme gutter &mdash; it is holding the sections apart, not the tiles.</p>')
    # ✅ s217-D7 — ONE CALL MINTS BOTH LEVELS. The outer wall of sections AND each inner wall's
    # tiles run the ratified pass, so neither level can be left on an authored literal.
    # ⚠ THE INNER TILES ARE PINNED UNIFORM ON THIS PAGE and that is a content decision, not an
    # exemption: this page demonstrates WHERE THE RADIUS AND SPACING SIT, and three sections of
    # differently-shaped tiles would compare shapes instead. Pinned still goes through the pass —
    # if the pinning ever changes to a shape that orphans, the pass closes it.
    inner_sets = [("photo", photos[:6]), ("card", CARDS[:6]),
                  ("mixed", [("photo", r) for r in photos[6:9]] + [("card", c) for c in CARDS[2:5]])]
    out_spans, inner_spans, nested = square_nested_wall(
        [[(1, 1)] * len(items) for _k, items in inner_sets], "dashboard",
        outer_spans=[(3, 1), (3, 1), (6, 1)], inner_cols=DASH_INNER_COLS)
    SQUARE_REPORTS.append(dict(nested["outer"], wall_role="dashboard"))
    for _r in nested["inner"]:
        SQUARE_REPORTS.append(dict(_r, wall_role="dashboard"))
    if nested["refusals"]:
        # ⚠ NAMED, NEVER SILENT — a nested wall believed square and shipped ragged is the #217
        # defect recurring one level down.
        print("⬛ s217-D7 nested squaring REFUSED: %s" % "; ".join(nested["refusals"]))
    A('<div class="c-bento dx-dash-outer"%s><div class="c-bento__grid">' % role_attr("dashboard"))
    for (kind, items), sp, ispans in zip(inner_sets, out_spans, inner_spans):
        A('<div class="c-bento__tile c-bento dx-dash-inner"%s data-c="%d" data-r="%d">'
          '<div class="c-bento__grid">' % (role_attr("dashboard"), sp[0], sp[1]))
        for item, s in zip(items, ispans):
            if kind == "photo":
                A(photo_tile(dict(item, span=s), caption=False))
            elif kind == "card":
                A(card_tile((item[0], item[1], item[2], s[0], s[1])))
            else:
                k, it = item
                A(photo_tile(dict(it, span=s), caption=False) if k == "photo"
                  else card_tile((it[0], it[1], it[2], s[0], s[1])))
        A('</div></div>')
    A('</div></div>')
    A('<p class="note t-ed-body-small"><b>What to look at in console.</b> Four containers, three '
      'of them rounded and holding square tiles a hairline apart, and the outer one holding those '
      'three sections a full gutter apart. <b>The two spacings are the role, not a per-instance '
      'tweak</b> &mdash; canon works out which wall is which by whether its tiles are themselves '
      'bentos.</p>')
    A('</section>')

    # ---- 2 · BROCHUREWARE ----------------------------------------------------------------
    A('<section id="brochureware">')
    A('<h2 class="t-ed-heading-3">Brochureware &mdash; the tiles carry the radius and the spacing</h2>')
    A('<p class="lede t-ed-body">A sectioned marketing page. Here the <b>tiles themselves</b> are '
      'the rounded objects and the container is square and paints nothing &mdash; the wall reads '
      'as a set of cards on the page rather than one slab.</p>')
    pspans, _ = wall([(x[2], x[3]) for x in PANELS], "brochureware")
    A('<div class="c-bento dx-broch"%s><div class="c-bento__grid">' % role_attr("brochureware"))
    for panel, s in zip(PANELS, pspans):
        A(panel_tile(panel, s))
    A('</div></div>')
    A('<p class="note t-ed-body-small">The squaring pass is <b>on</b> here, as you ratified: the '
      'bottom edge is straight at every band, no orphaned compartments.</p>')
    A('</section>')

    # ---- 3 · GALLERY ---------------------------------------------------------------------
    gal = photos
    gspans, grep = wall([r["span"] for r in gal], "gallery", columns=4)
    A('<section id="gallery">')
    A('<h2 class="t-ed-heading-3">Gallery &mdash; ragged is allowed, captions are roomier</h2>')
    A('<p class="lede t-ed-body">Page-level photography. Radius and spacing sit on the tiles, as '
      'brochureware &mdash; but the <b>squaring pass relaxes</b>. Orphans are acceptable here; the '
      'only requirement is a layout that suits portrait and landscape pictures, and that is the '
      'aspect rule, which is untouched. Portraits are still two rows tall.</p>')
    A('<p class="lede t-ed-body"><b>The caption space is more generous.</b> It is now '
      '<b>%dpx</b>, up from 62 &mdash; %+dpx, about %d%%. That is not a taste pick: it buys one '
      'more line of description (two &rarr; %d) and steps the padding one rung up the 4px ladder '
      '(8 &rarr; %d). The clamp is derived from the space, so the two can never disagree.</p>'
      % (space, space - 62, round((space - 62) / 62 * 100), lines, 12))
    A('<div class="sublabel t-ed-caption">Ruled &mdash; keylines, theme spacing, generous captions</div>')
    A('<div class="c-bento dx-gal"%s><div class="c-bento__grid">' % role_attr("gallery"))
    for r, s in zip(gal, gspans):
        A(photo_tile(dict(r, span=s)))
    A('</div></div>')
    if grep.get("exempt") and not grep["squared"]:
        A('<p class="note t-ed-body-small"><b>This wall is ragged, and that is the ruling.</b> '
          '%d cell(s) are empty at %d columns. In dashboard or brochureware that would be a '
          'failure and the pass would straighten it; in gallery it is what you asked for.</p>'
          % (grep["holes"], grep["at_cols"] or 4))
    else:
        A('<p class="note t-ed-body-small">This wall happens to come out rectangular on its own. '
          'The squaring pass is <b>off</b> here either way &mdash; nothing straightened it.</p>')
    A('</section>')

    # ---- 3b · THE KEYLINE TRIAL ----------------------------------------------------------
    A('<section id="trial">')
    A('<h2 class="t-ed-heading-3">The keyline trial, beside the ruled gallery</h2>')
    A('<p class="badge t-cm-legal">Proposed &mdash; not ruled</p>')
    A('<p class="lede t-ed-body">Your words were &ldquo;<i>can we try dropping the keylines and '
      'just have a 1px gutter and row space</i>&rdquo;. Here it is, with the same photographs and '
      'the same derived spans, directly under the ruled variant so you can rule by eye. '
      '<b>Nothing about the trial has been adopted</b> &mdash; it is a specimen with its own '
      'styles, and none of them touch the wall above.</p>')
    A('<div class="dx-2up">')
    A('<div><div class="sublabel t-ed-caption">Ruled &mdash; keylines and theme spacing</div>')
    A('<div class="c-bento dx-gal dx-gal-b"%s><div class="c-bento__grid">' % role_attr("gallery"))
    for r, s in zip(gal, gspans):
        A(photo_tile(dict(r, span=s)))
    A('</div></div>')
    A('<span class="dx-caption t-cm-legal">Keylines on every tile; tiles spaced at the theme '
      'gutter; caption block %dpx.</span></div>' % space)
    A('<div><div class="sublabel t-ed-caption">Trial &mdash; no keylines, 1px gutter and row space</div>')
    A('<div class="c-bento dx-trial"%s><div class="c-bento__grid">' % role_attr("gallery"))
    for r, s in zip(gal, gspans):
        A(photo_tile(dict(r, span=s)))
    A('</div></div>')
    A('<span class="dx-caption t-cm-legal">No borders at all; 1px gutter and row space; the same '
      '%dpx caption block, because the caption space is ruled and the trial is not about '
      'that.</span></div>' % space)
    A('</div>')
    A('<p class="note t-ed-body-small"><b>What is yours to decide.</b> Whether the gallery keeps '
      'its keylines, drops them for the 1px gutter, or gets both as a dial. Say the word and it '
      'becomes a ruling; say no and the trial block comes out in three lines.</p>')
    A('</section>')

    # ---- 4 · provenance ------------------------------------------------------------------
    A('<section id="provenance">')
    A('<h2 class="t-ed-heading-3">What is canon here, and what is this page</h2>')
    A('<p class="lede t-ed-body">Canon: the container, the grid, the span vocabulary, the bands, '
      'the three role rules and the gallery caption space &mdash; all generated into '
      '<code>knowledge/canon/canon.css</code> by <code>canon/gen_canon_bento.py</code> from '
      '<code>tokens/layout.json</code> (<code>layout/bento</code>, including the new '
      '<code>$roles</code> block and <code>caption-space</code>). The role is an '
      '<code>data-bento-role</code> attribute on the instance &mdash; no JavaScript, no new '
      'class. This page declares <b>no grid, no gap, no bento radius and no role rule of its '
      'own</b>.</p>')
    A('<p class="note t-ed-body-small">Still <b>not</b> ruled and deliberately untouched: '
      '<code>ds-051</code> (the packing token has no legal DTCG type), which keeps the build '
      'gate red until you rule it.</p>')
    if residuals.get("missing_derivative_file"):
        A('<p class="note t-ed-body-small">⚠ Manifest rows naming a derivative that is not on '
          'disk: %s</p>' % esc(", ".join(residuals["missing_derivative_file"])))
    A('</section>')
    return "\n".join(S)


def page(photos, residuals):
    return ((HEAD
             .replace("__TITLE__", "Apollo &mdash; bento roles")
             .replace("__SENTINEL__", SENTINEL)
             .replace("__UP__", UP)
             .replace("__CSS__", CSS.replace("__DASH_INNER_COLS__", str(DASH_INNER_COLS)))
             .replace("__H1__", "Bento roles")
             .replace("__SUBTITLE__",
                      "s217-D3 &middot; dashboard / brochureware / gallery &middot; four themes"))
            + build(photos, residuals) + TAIL.replace("__SCRIPT__", SCRIPT))


def main():
    global WRONG_ROLE
    out = OUT
    argv = sys.argv[1:]
    if "--wrong-role" in argv:
        # ⬛ THE MUTATION HANDLE for the ROLE SELECTOR. Every wall is emitted as `brochureware`,
        # so the dashboard section loses its container radius and its 1px spacing and the
        # per-role probe must go RED. Never writes over the real page.
        WRONG_ROLE = "brochureware"
        out = OUT.replace(".html", "-WRONGROLE.html")
    for i, a in enumerate(argv):
        if a == "--out":
            out = argv[i + 1]
    del SQUARE_REPORTS[:]
    photos, residuals = read_photos()
    if not photos:
        print("⚠ no committed photography derivatives found — the gallery walls will be empty")
    html = page(photos, residuals)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    space, lines = caption_space()
    print("Wrote %s  (%d photo tiles, %d cards, %d panels)"
          % (out, len(photos), len(CARDS), len(PANELS)))
    if WRONG_ROLE:
        print("  ⬛ MUTATION ARM — every role rewritten to %r" % WRONG_ROLE)
    print("  roles: %s" % " · ".join(
        "%s(squaring %s)" % (k, "on" if v["squaring"] else "OFF")
        for k, v in roles().items() if not k.startswith("$")))
    print("  gallery caption space %dpx -> %d description line(s)" % (space, lines))
    for i, rep in enumerate(SQUARE_REPORTS, 1):
        print("    wall %-2d %-13s ladder %-12s rows %-14s %s"
              % (i, rep["wall_role"], str(rep["ladder"]),
                 " / ".join(str(rep["rows"][c]) for c in rep["ladder"]),
                 "EXEMPT (%s)" % ("rectangular anyway" if rep["squared"]
                                  else "%d hole(s) — ragged-tolerant" % rep["holes"])
                 if rep.get("exempt") else
                 ("squared, %d tile(s) re-spanned" % len(rep["changed"]) if rep["squared"]
                  else "⛔ NOT SQUARE — %s" % rep["reason"])))
    unsq = [r for r in SQUARE_REPORTS if not r["squared"] and not r.get("exempt")]
    if unsq:
        print("❌ DECLARED RESIDUAL: %d non-exempt wall(s) could not be squared" % len(unsq))
    if residuals.get("missing_derivative_file"):
        print("  residual — manifest rows with no file: %s"
              % ", ".join(residuals["missing_derivative_file"]))
    return 0


def selftest():
    """9 bites: canon-only structure · one role attribute per wall · the three roles present ·
    dial surface · instance dials out-specify the role rules · the trial does not leak ·
    gallery unsquared but still aspect-mapped · non-exempt walls square · mutation handle."""
    global WRONG_ROLE
    photos, res = read_photos()
    del SQUARE_REPORTS[:]
    h = page(photos, res)
    css = h.split("<style>", 1)[1].split("</style>", 1)[0]
    body = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    # --- bite 1: the page declares no structure, no bento radius, and NO ROLE RULE ----------
    for banned in ("grid-template-columns", "grid-auto-rows", "grid-auto-flow"):
        assert banned not in body, \
            "bite 1a FAIL: the page declares %s — structure must come from canon" % banned
    for sel, decls in re.findall(r"([^{}]+)\{([^{}]*)\}", body):
        if "c-bento" in sel and "border-radius" in decls:
            raise AssertionError("bite 1b FAIL: %r declares a bento radius of its own" % sel.strip())
        if "data-bento-role" in sel and ("--bento-gutter" in decls or "overflow" in decls):
            raise AssertionError(
                "bite 1c FAIL: %r re-declares role behaviour — the role rules are canon's, and a "
                "page-local copy would let the page and canon disagree silently" % sel.strip())

    # --- bite 2: every wall names a role, and every role attribute came from role_attr() ----
    walls = re.findall(r'class="([^"]*\bc-bento\b[^"]*)"([^>]*)>', h)
    for cls, rest in walls:
        assert "data-bento-role=" in rest, \
            "bite 2a FAIL: a bento with classes %r carries NO role — it would silently take the " \
            "default, which is a decision made by omission" % cls.strip()
    found = set(re.findall(r'data-bento-role="(\w+)"', h))
    assert found == {"dashboard", "brochureware", "gallery"}, \
        "bite 2b FAIL: the page must show all three s217-D3 roles — found %r" % sorted(found)

    # --- bite 3: dials the page invents ------------------------------------------------------
    dials = set(re.findall(r"(--bento-[a-z-]+)\s*:", css))
    assert dials <= {"--bento-gutter", "--bento-columns", "--bento-row-unit",
                     "--bento-outer-padding", "--bento-packing", "--bento-radius",
                     "--bento-caption-space", "--bento-caption-lines"}, \
        "bite 3 FAIL: the page invented a bento dial canon does not define — %r" % dials

    # --- bite 4: instance dials must out-specify the ROLE rules ------------------------------
    # canon's role rules are (0,2,0); a bare `.dx-…{--bento-columns:…}` is (0,1,0) and would LOSE.
    for sel, decls in re.findall(r"([^{}]+)\{([^{}]*)\}", body):
        # ⚠ SETS, not READS. `var(--bento-caption-lines,2)` inside a tile-content rule is a
        # consumer and is fine; only a DECLARATION of a dial has a cascade fight to lose.
        sets = re.findall(r"(?:^|;)\s*(--bento-[a-z-]+)\s*:", decls)
        if sets and "c-bento" not in sel and "data-bento-role" not in sel:
            raise AssertionError(
                "bite 4 FAIL: %r sets a --bento-* dial from a bare class (0,1,0). Canon's role "
                "rules are (0,2,0) and would beat it — silently, in one theme, at one width. "
                "Write it as `.c-bento.%s`." % (sel.strip(), sel.strip().lstrip(".")))

    # --- bite 5: the caption space is canon's, not restated here -----------------------------
    space, lines = caption_space()
    assert "min-height" not in body.split(".dx-cap", 1)[1].split("}", 1)[0], \
        "bite 5a FAIL: the page restates the caption block height — the ruled number must come " \
        "from canon or the two can drift apart"
    assert "c-bento__caption" in h, "bite 5b FAIL: no caption slot, so the ruled space reaches nothing"
    assert ("var(--bento-caption-lines" in body), \
        "bite 5c FAIL: the clamp is not reading canon's DERIVED line allowance"

    # --- bite 6: the TRIAL does not leak into the ruled gallery ------------------------------
    trial_rules = [sel for sel, _ in re.findall(r"([^{}]+)\{([^{}]*)\}", body)
                   if "dx-trial" in sel]
    assert trial_rules, "bite 6a FAIL: the trial declares nothing — there is no specimen to rule on"
    # ⚠ SCOPED TO TILE RULES. Page chrome (`.seg button`) is free to have no border of its own;
    # a blanket ban on `border:0` would have said the opposite of what is meant
    # ([[gate-glob-scope-rule]]).
    for sel, decls in re.findall(r"([^{}]+)\{([^{}]*)\}", body):
        touches_tile = any(t in sel for t in ("dx-photo", "dx-card", "dx-panel", "c-bento__tile"))
        if touches_tile and ("border:0" in decls.replace(" ", "")
                             or "border:none" in decls.replace(" ", "")):
            assert "dx-trial" in sel, \
                "bite 6b FAIL: %r drops a keyline OUTSIDE the trial — the keyline-less variant " \
                "is PROPOSED, and leaking it into the ruled gallery is a decision by accident" % sel.strip()
    tsec = h.split('<section id="trial">', 1)[1].split("</section>", 1)[0]
    assert "not ruled" in tsec.lower(), \
        "bite 6c FAIL: the trial is PROPOSED — the page must say so where Dave reads it"
    assert 'class="c-bento dx-gal dx-gal-b"' in tsec and 'class="c-bento dx-trial"' in tsec, \
        "bite 6d FAIL: the trial must sit BESIDE the ruled gallery — one wall alone is not a " \
        "comparison and cannot be ruled on by eye"

    # --- bite 7: gallery is NOT squared, and is STILL aspect-mapped --------------------------
    p = params()
    gal_reports = [r for r in SQUARE_REPORTS if r["wall_role"] == "gallery"]
    assert gal_reports and all(r["exempt"] for r in gal_reports), \
        "bite 7a FAIL: a gallery wall went through the squaring pass — s217-D3 exempts it"
    assert span_for(1000, 1600, p) == (1, 2), \
        "bite 7b FAIL: the portrait two-row mapping is gone — gallery's SQUARING exemption must " \
        "not disable the ASPECT mapping; they are different mechanisms"
    ports = [r for r in photos if r["orient"] == "portrait"]
    assert ports, "bite 7c FAIL: no portrait derivatives, so the gallery cannot show the mapping"
    gsec = h.split('<section id="gallery">', 1)[1].split("</section>", 1)[0]
    assert 'data-r="2"' in gsec, \
        "bite 7d FAIL: no two-row tile in the gallery — the portrait mapping did not reach the " \
        "page, which is the half of the ruling the exemption must NOT have taken with it"

    # --- bite 8: every NON-exempt wall is square ---------------------------------------------
    bad = [i for i, rep in enumerate(SQUARE_REPORTS, 1)
           if not rep.get("exempt") and not rep["squared"]]
    assert not bad, "bite 8 FAIL: wall(s) %r shipped ragged in a role that is squared" % bad

    # --- bite 9: the role mutation handle actually mutates ------------------------------------
    try:
        WRONG_ROLE = "brochureware"
        del SQUARE_REPORTS[:]
        mut = page(photos, res)
    finally:
        WRONG_ROLE = None
        del SQUARE_REPORTS[:]
    # ⚠ THE MARKUP, not the whole file: the page's own stylesheet names the dashboard role in a
    # selector (the ground behind the container), and that string is not a wall.
    mut_markup = mut.split("</style>", 1)[1]
    assert 'data-bento-role="dashboard"' not in mut_markup and \
           'data-bento-role="brochureware"' in mut_markup, \
        "bite 9 FAIL: --wrong-role did not rewrite every role, so the mutation arm would go " \
        "green against a page that was never actually mutated"

    print("gen_bento_roles_217 selftest OK (9 bites: canon-only structure · every wall names a "
          "role · all three roles present · dial surface · instance dials out-specify the role "
          "rules · the trial does not leak · gallery unsquared but still aspect-mapped · "
          "non-exempt walls square · role mutation handle)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        sys.exit(main())
