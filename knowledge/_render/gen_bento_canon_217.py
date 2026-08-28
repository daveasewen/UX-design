#!/usr/bin/env python3
"""
gen_bento_canon_217.py — the BENTO CANON demo page (s217-D2, #217). For Dave's eye.

⛔ #219 RE-CUT. This generator now writes `reviews/BENTO-CANON-2026-08-25-v6.html`. Dave opened v2
and said *"we've already decided all of this in previous sessions"* and *"we've also missed the
extra space for captions."* Both were true of v2: its squaring section still badged a RATIFIED
mechanism "Proposed — not ruled" (`s217-D3`), and its captions never consumed the ruled
`layout/bento/caption-space`. The re-cut STRIKES the settled questions with their receipts (never
drops them), BAKES IN the ruled caption block and the ruled mono caption ground, and leaves only
the genuinely open residue as a live control. The ledger is `_bento_recut_219.py` — one home, three
pages. ⚠ v2 is untouched on disk.

⛔ v6, AND WHY IT EXISTS THE SAME DAY AS v4. `s219-D1` and `s219-D2` were inscribed hours after v4
was written, and `s219-D2 (1)` RETIRED the `s218-D6 (1)` dark mono caption ground this page was
painting. v4 therefore shows Dave a superseded ground beside a ledger calling it settled law
(lane B's finding 12). v6 is that page rebuilt off the updated ledger; **v4 stays on disk exactly
as it was written** ([[feedback-version-dont-overwrite]]).

Builds the canon bento grammar rendered as itself,
in four themes x light/dark, with the bento-of-bentos Dave described in as many words —
"a page section that had three bentos each with 1px spacing within a larger one that had
40px spacing".

v2 (#217) answers Dave's two mid-session questions:
  * "if photo is portrait could it default to a taller compartment?" — it already does; the
    s217-D2 two-row threshold (taller than 1:1.15) rules it. v2 PROVES it visibly: three
    portrait derivatives were minted and land as two-row tiles beside their landscape
    neighbours. Nothing was ruled to make that happen.
  * "Is there a way to avoid orphaned compartments so the bento is always cohesively
    rectangular?" — the SQUARING PASS, `canon/gen_canon_bento.square_wall()`. ⬛ PROPOSED, NOT
    RULED: the page shows a deliberately awkward tile count ragged and squared side by side,
    and the mechanism is Dave's to ratify.

⛔ THE PAGE MINTS NOTHING. Every structural rule it uses comes from canon.css's AUTO-BENTO
block (canon/gen_canon_bento.py, from tokens/layout.json). The page-local stylesheet styles
TILE CONTENT — cards, captions, chrome — and declares no grid, no gap and no bento radius.
That is the test as well as the demo: if the bento grammar were not really canon, this page
could not lay out.

⚠ EVERY var() CARRIES A LITERAL FALLBACK for the page's own chrome
([[dangling-dataviz-var-renders-silent-black]]) — except the four `--bento-*` dials, which are
DELIBERATELY bare: a fallback there would hide exactly the failure the probe exists to catch.

The photographs are the twelve committed web derivatives (s217-D1 manifest); their spans are
DERIVED by canon/gen_canon_bento.span_for + emphasise, never arranged by eye. Card spans are
AUTHORED — the aspect thresholds are photography-only (s217-D2).

Usage:
  python3 knowledge/_render/gen_bento_canon_217.py
  python3 knowledge/_render/gen_bento_canon_217.py --no-square   # mutation arm -> *-NOSQUARE.html
  python3 knowledge/_render/gen_bento_canon_217.py --selftest
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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
sys.path.insert(0, os.path.join(KNOW, "canon"))
sys.path.insert(0, HERE)
from gen_canon_bento import (params, span_for, emphasise,  # noqa: E402
                             square_wall, is_rectangular, band_ladder, place, band_clamp,
                             caption_space)
import _bento_recut_219 as recut  # noqa: E402  ⚠ THE ONE HOME for the decision ledger

# ⚠ v6, NOT an overwrite. `BENTO-CANON-2026-08-23-v2.html` (Dave's #217 page) and
# `BENTO-CANON-2026-08-25-v4.html` (the pre-s219 re-cut) both stay on disk exactly as they were
# written; this is the #219 seam-5 successor, re-cut against `s219-D1` / `s219-D2`
# ([[feedback-version-dont-overwrite]]).
# ⚠ THE VERSION SERIES IS SHARED with gen_bento_roles_217 — both write BENTO-CANON-<date>-vN, so
# the next free numbers are taken in pairs (v4/v5 at the re-cut, v6/v7 at seam 5).
OUT = os.path.join(ROOT, "reviews", "BENTO-CANON-%s-v6.html" % recut.RECUT_DATE)
PHOTO_MANIFEST = os.path.join(KNOW, "_PHOTOGRAPHY-MANIFEST.json")
UP = "../"
SENTINEL = "<!-- APOLLO BENTO-CANON DEMO (gen_bento_canon_217.py) — s217-D2, RE-CUT #219 -->"


def esc(s):
    return htmlmod.escape(str(s if s is not None else ""), quote=True)


# ---------------------------------------------------------------------------- photographs
def read_photos():
    """The manifest's own rows that carry a committed derivative. Spans DERIVED.

    ⬛ #218 CONSEQUENCE — DECLARED. Dave ruled ALL 251 photographs onto the Foundations
    photography page, so every manifest row now carries a derivative. This page is a #217 DEMO
    surface built and ratified against the fifteen committed derivatives of that day, and it
    calls `square_wall`, whose exhaustive tail search is instant at 15 tiles and MEASURED at
    ~45 minutes at 251 — the page becomes unbuildable, not merely slow.
    ⛔ THIS IS ALSO THE PRICE OF A SECOND READER. `gen_bento_roles_217.read_photos()` is the ONE
    data path and it took the specimen cap in one place; this private copy did not, and had to be
    told separately. The cap SIZE is imported from there so there is at least one number, not two.
    """
    from gen_bento_roles_217 import SPECIMEN_N
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
                     "desc": desc if len(desc) <= 90 else desc[:89].rsplit(" ", 1)[0] + "…"})
    rows.sort(key=lambda r: r["file"])
    population = len(rows)
    specimen = None
    if population > SPECIMEN_N:
        # ⛔ #218 CORRECTION, SAME SITTING — PINNED BY NAME, with the ONE data path's own list.
        # The first cut sliced by filename order and MEASURED against the ratified set that swap
        # replaced 14 of 15 photographs on the live decision surfaces; this page then also needed
        # a portrait extension the pinned set makes unnecessary — the RATIFIED s217-D1 set
        # already carries the three portrait derivatives the portrait proof (bite 5a) needs,
        # because #217 minted them FOR that proof. [[specimen-starts-from-reference]]
        from gen_bento_roles_217 import SPECIMEN_FILES
        rows = [r for r in rows if r["file"] in SPECIMEN_FILES]
        specimen = {"shown": len(rows), "population": population,
                    "basis": "the RATIFIED s217-D1 specimen set, PINNED BY NAME (#218) — "
                             "includes the three portrait derivatives bite 5a needs",
                    "missing_pinned": sorted(set(SPECIMEN_FILES) - {r["file"] for r in rows})}
    p = params()
    for i, r in enumerate(rows, 1):
        r["span"] = emphasise(span_for(r["w"], r["h"], p), i, p)
    return rows, {"missing_derivative_file": missing, "specimen": specimen}


# ---------------------------------------------------------------------------- the squaring pass
# ✅ RATIFIED s217-D3 for dashboard + brochureware (#219 correction: it was still labelled
# "PROPOSED, NOT RULED" here after the ruling landed). SQUARE is a MUTATION HANDLE, not a
# preference: the probe
# regenerates this page with --no-square and requires its bottom-edge assertion to go RED. A
# gate that has never been seen to fail is not a gate ([[instrument-without-a-consumer]]).
SQUARE = True
SQUARE_REPORTS = []


def wall(spans, columns=None):
    """-> (spans, report) for ONE bento wall, squared at its own instance ladder.

    `columns` is the wall's INSTANCE column dial (the `--bento-columns` its rule declares), not
    canon's default — a 3-column inner bento never renders at 6, and squaring it against 6 would
    refuse a wall that is rectangular at every width it is ever seen at."""
    p = params()
    ladder = band_ladder(p if columns is None else dict(p, columns=columns))
    if not SQUARE:
        ok, cols, holes = is_rectangular(spans, ladder)
        rep = {"squared": ok, "adjusted": 0, "changed": [], "ladder": ladder, "disabled": True,
               "rows": {c: place(band_clamp(spans, c), c)[0] for c in ladder},
               "reason": None if ok else "squaring pass DISABLED (--no-square)"}
        SQUARE_REPORTS.append(rep)
        return list(spans), rep
    out, rep = square_wall(spans, ladder=ladder)
    rep["disabled"] = False
    SQUARE_REPORTS.append(rep)
    return out, rep


def photo_tile(r, extra_class=""):
    c, rw = r["span"]
    return ('<figure class="c-bento__tile dx-photo %s" data-c="%d" data-r="%d">'
            '<img class="dx-img" src="%sknowledge/assets/photography-web/%s" alt="%s"'
            ' loading="lazy" width="%s" height="%s">'
            '<figcaption class="c-bento__caption dx-cap t-cm-legal">%s</figcaption></figure>'
            % (extra_class, c, rw, UP, esc(r["file"]), esc(r["desc"]),
               r["w"] or "", r["h"] or "", esc(r["desc"])))


# ---------------------------------------------------------------------------- cards
# AUTHORED spans (s217-D2: card spans are authored; the aspect thresholds are photography-only).
CARDS = [
    ("Balance", "Current account", "£18,420.66", 2, 1),
    ("Runway", "at today’s burn", "7.4 months", 1, 1),
    ("Payments due", "next 30 days", "14", 1, 1),
    ("FX exposure", "GBP / USD / EUR", "3 pairs", 2, 2),
    ("Approvals", "waiting on you", "5", 1, 1),
    ("Cards", "active", "27", 1, 1),
    ("Invoices", "overdue", "2", 2, 1),
    ("Sweep", "nightly", "on", 1, 1),
]

# ELEVEN tiles, authored to orphan. Eleven is the point: it is not a multiple of six, of three
# or of two, so the last row is short at EVERY band — and the tall tile in the middle leaves a
# compartment hanging below the bottom edge, which is the shape in Dave's screenshot.
AWKWARD = [
    ("Sterling", "cleared", "£4.1m", 2, 1),
    ("Euro", "cleared", "€2.7m", 1, 1),
    ("Dollar", "cleared", "$3.3m", 1, 1),
    ("Yen", "cleared", "¥310m", 1, 1),
    ("Breaks", "unmatched", "6", 1, 1),
    ("Nostro", "reconciled", "99.2%", 2, 1),
    ("Cut-off", "London", "16:00", 1, 1),
    ("Cut-off", "New York", "17:30", 1, 1),
    ("Holidays", "next 14 days", "3", 1, 1),
    ("Alerts", "open", "1", 1, 1),
    # LAST, and two rows tall — this is the tile hanging below the bottom edge in the screenshot.
    ("Settlement", "T+1 queue", "38", 1, 2),
]


def card_tile(card, extra_class=""):
    label, sub, fig, c, r = card
    return ('<div class="c-bento__tile dx-card %s" data-c="%d" data-r="%d">'
            '<span class="dx-eyebrow t-cm-legal">%s</span>'
            '<span class="dx-sub t-cm-legal">%s</span>'
            '<span class="dx-fig t-ed-heading-4">%s</span></div>'
            % (extra_class, c, r, esc(label), esc(sub), esc(fig)))


# ---------------------------------------------------------------------------- page-local CSS
# ⛔ NO GRID, NO GAP, NO BENTO RADIUS HERE. Structure is canon's (AUTO-BENTO in canon.css).
CSS = """
/* ===========================================================================
   BENTO CANON DEMO — page-local styles, scoped to `.dx`.
   ⛔ STRUCTURE IS NOT DECLARED HERE. The bento container, the grid, the span
   vocabulary and the responsive bands all come from canon.css's AUTO-BENTO
   block. This file styles TILE CONTENT and page chrome only — which is why
   the page is a test of the canon grammar and not a re-drawing of it.
   ⚠ Every var() below carries a literal fallback, EXCEPT the --bento-* dials
   in the instance blocks: a fallback there would mask the very failure the
   probe is looking for (a theme override that never landed).
   =========================================================================== */
.dx{
  --page:      var(--background-default,#FFFFFF);
  --surface:   var(--tertiary-background-default,#FFFFFF);
  --surface-2: var(--tertiary-background-hover,#F0F0F0);   /* #221: was #F3F3F3 */
  --line:      var(--border-subtle,#D7D8D6);
  --line-2:    var(--border-strong,#808080);               /* #221: was #767676 */
  --ink:       var(--text-default,#1A1A1A);
  --ink-2:     var(--text-secondary,#545454);
  --focus:     var(--focus-ring,#305A85);                  /* #221: was #1A1A1A */
  --focus-w:   var(--focus-ring-width,2px);
  --radius-ctl:var(--border-radius-control,0px);
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px; --sp-7:48px;
  background:var(--page); color:var(--ink); -webkit-font-smoothing:antialiased;
}
.dx *{box-sizing:border-box;}
.dx :focus-visible{outline:var(--focus-w) solid var(--focus); outline-offset:2px;}
html,body{margin:0;}
body{background:var(--background-default,#FFFFFF);}
/* ⚠ the ink is restated on a CHILD of the themed element — measured #217 on the Foundations
   pages: an element that BOTH carries data-theme and reads --text-default disagreed with its
   own children in supercharge dark. */
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
  background:var(--surface-2,#F0F0F0); padding:0 .3em;}
.note{margin:var(--sp-3) 0 0; color:var(--ink-2); max-width:74ch;}
.note b{color:var(--ink);}

/* ---- the ONE thing that makes the container radius visible: a ground behind the bento ---- */
/* ⚠ The bento container paints nothing of its own in canon — a structural component must not
   decide a surface (that is out of scope per s217-D2). So the DEMO gives it a ground, which is
   also what lets a rounded container read as rounded at all. */
.dx .c-bento{background:var(--surface-2,#F0F0F0);}

/* ---- tile content ---- */
.dx-photo{margin:0; display:grid; grid-template-rows:1fr auto; overflow:hidden;
  background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);}
.dx-img{display:block; width:100%; height:100%; min-height:0; object-fit:cover;
  background:var(--surface-2,#F0F0F0);}
/* ⬛ #219 — THE RULED CAPTION BLOCK, WHICH v2 MISSED. Dave: "we've also missed the extra space
   for captions." `s217-D3` ruled the gallery caption more generous and it was DERIVED into
   `layout/bento/caption-space`; canon exposes it as `--layout-bento-caption-space`. v2's photo
   captions consumed neither the token nor canon's `.c-bento__caption` slot, so they rendered at
   whatever the two clamped lines happened to be.
   ⛔ THE TOKEN, NEVER THE NUMBER. The literal in the fallback is MINTED HERE at build time from
   `caption_space()` (s200-D1), not typed — so this page cannot become a second source for a
   ruled number. Same for the line allowance, which canon derives back out of the same figure.
   ⚠ Canon's own `min-height` rule is scoped to `[data-bento-role="gallery"]`; this page's walls
   carry no role (it is the s217-D2 defaults demo and giving them one would change what it
   demonstrates), so the token is consumed directly here instead. */
.dx-cap{padding:var(--sp-3); color:var(--ink-2,#545454);
  min-height:var(--layout-bento-caption-space,__CAPSPACE__px);
  display:-webkit-box; -webkit-line-clamp:var(--bento-caption-lines,__CAPLINES__);
  -webkit-box-orient:vertical; overflow:hidden;
  /* ds-005/ds-048: a clamped label must opt out of the cap/alphabetic trim or its last
     visible line loses its descenders. */
  text-box-edge:text text;}
__MONOCAP__
__RECUT__
.dx-card{background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);
  padding:var(--sp-4); overflow:hidden; display:flex; flex-direction:column; gap:var(--sp-1);}
.dx-eyebrow{color:var(--ink,#1A1A1A);}
.dx-sub{color:var(--ink-2,#545454);}
.dx-fig{margin-top:auto; font-variant-numeric:tabular-nums;}

/* ---- INSTANCE PARAMETER SETS — declared rules, never a style="" attribute -------------- */
/* ⚠ DECLARED, and the reason is measured (#217 Foundations): an inline custom property is
   invisible to every instrument that resolves the stylesheet against the document, so an
   inline-only dial reads EMPTY in all eight states. It also beats container queries outright.
   Declared rules are probeable AND cascade correctly. This block is the whole per-instance
   override surface — four names, no new classes. */
.dx-outer{--bento-gutter:40px; --bento-columns:6; --bento-row-unit:auto; --bento-outer-padding:24px;}
.dx-inner{--bento-gutter:1px; --bento-columns:3; --bento-row-unit:150px; --bento-outer-padding:0px;}
/* the portrait wall runs at three columns so three tall tiles can sit side by side and be read
   against their landscape neighbours at a glance */
.dx-portrait{--bento-columns:3; --bento-row-unit:150px;}
.dx-awkward{--bento-row-unit:110px;}

/* ---- the squaring comparison: two walls, same eleven tiles, side by side ---------------- */
/* ⚠ STACKED, NOT SIDE BY SIDE, and the reason is measured. Two half-width walls sit BELOW the
   820 band, so both render at two columns — where eleven tiles happen to be rectangular anyway,
   and the control came out square. A control that cannot show the defect is worse than no
   control. Full width puts both walls at six columns, which is where the ragged edge lives.
   Flex, not grid: the page's own selftest bans every grid declaration in this stylesheet. */
.dx-2up{display:flex; flex-direction:column; gap:var(--sp-5);}
.dx-2up > div{min-width:0;}
/* ⚠ a MARKER class only — it declares no structure. It exists so the probe can tell the
   deliberately ragged control apart from the walls that must be square, by name rather than by
   position. A probe that identifies its control by document order breaks the day a section moves. */
.dx-ragged{}
.dx-square{}
.badge{display:inline-block; border:1px solid var(--line-2,#808080); color:var(--ink,#1A1A1A);
  padding:2px 8px; letter-spacing:0.12em; text-transform:uppercase; margin:0 0 var(--sp-3);}

/* the band demonstration — three bento walls at fixed widths, so the CONTAINER queries fire
   at 1100 / 820 / 520 without moving the window */
.dx-band-row{display:flex; flex-wrap:wrap; gap:var(--sp-5); align-items:flex-start;}
.dx-w1000{width:1000px; max-width:100%;}
.dx-w780{width:780px; max-width:100%;}
.dx-w460{width:460px; max-width:100%;}
.dx-band-row .c-bento{--bento-row-unit:120px;}
.dx-caption{color:var(--ink-2,#545454); margin:var(--sp-2) 0 0; display:block;}

@media (prefers-reduced-motion: reduce){
  .dx *,.dx *::before,.dx *::after{transition-duration:.01ms !important;
    animation-duration:.01ms !important;}
}
"""

SCRIPT = """
(function(){
  var THEMES=['mono','legacy','console','supercharge'];
  var state={theme:'mono',mode:'light',chrome:'1'};
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
<html lang="en" data-apollo-theme="mono">
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
      <button type="button" data-theme-attr="mono" aria-pressed="true">Mono</button>
      <button type="button" data-theme-attr="legacy" aria-pressed="false">Legacy</button>
      <button type="button" data-theme-attr="console" aria-pressed="false">Console</button>
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
    S = []
    A = S.append

    # ---- 0 · #219 — WHAT IS ALREADY DECIDED ---------------------------------------------
    # ⛔ FIRST ON THE PAGE, deliberately. v2 opened with a demo and buried a settled question in a
    # "Proposed — not ruled" badge four sections down. A decision surface has to say what it is NOT
    # asking before it shows anything, or the reader re-derives the answers to find out.
    A(recut.ledger_html("canon"))

    # ---- 1 · the grammar at its ruled defaults -----------------------------------------
    A('<section id="defaults">')
    A('<h2 class="t-ed-heading-3">The bento, at the parameters you ruled</h2>')
    A('<p class="lede t-ed-body">Six columns, %s row unit, dense packing, outer padding 0 &mdash; '
      'shared by all four themes. <b>The gutter is the only thing that moves between themes</b>: '
      '0 in mono and supercharge, 24 in legacy and console. Switch the theme above and watch the '
      'space between tiles open and close while nothing else does.</p>'
      % "320px")
    A('<div class="sublabel t-ed-caption">Photography &mdash; %d committed derivatives, spans derived</div>'
      % len(photos))
    dspans, drep = wall([r["span"] for r in photos])
    A('<div class="c-bento dx-square"><div class="c-bento__grid">')
    for r, s in zip(photos, dspans):
        A(photo_tile(dict(r, span=s)))
    A('</div></div>')
    A('<p class="note t-ed-body-small"><b>Nothing here is arranged by eye.</b> Every derivative is '
      '1600&times;1067 (1.50:1), which is below the %.2f:1 two-column threshold, so the aspect rule '
      'alone would draw a plain grid. The mixed emphasis you can see is the <b>rhythm</b>: every '
      '%dth tile from tile %d is promoted to 2&times;2. Position, not preference. '
      '<b>The aspect thresholds are photography-only</b> &mdash; card spans below are authored.</p>'
      % (p["aspect2"], p["emph_every"], p["emph_from"]))
    A('<p class="note t-ed-body-small">This wall has also been through the <b>squaring pass</b> '
      '(below): %d of its %d tiles were re-spanned so the bottom edge is straight at every band. '
      'It fills exactly %s rows at 6, 3, 2 and 1 columns.</p>'
      % (len(drep["changed"]), len(photos),
         " / ".join(str(drep["rows"][c]) for c in drep["ladder"])))
    A('</section>')

    # ---- 1b · PORTRAIT — Dave's first question, already ruled ---------------------------
    ports = [r for r in photos if r["orient"] == "portrait"]
    lands = [r for r in photos if r["orient"] != "portrait"]
    mixed = []
    for i in range(max(len(ports), 3)):
        if i < len(ports):
            mixed.append(ports[i])
        if i < len(lands):
            mixed.append(lands[i])
    # spans DERIVED from each photograph's own aspect, no rhythm — the point of this wall is the
    # threshold and nothing else.
    pspans, prep = wall([span_for(r["w"], r["h"], p) for r in mixed], columns=3)
    A('<section id="portrait">')
    A('<h2 class="t-ed-heading-3">A portrait photograph gets a taller compartment</h2>')
    A('<p class="lede t-ed-body">You asked whether a portrait could default to a taller '
      'compartment. <b>It already does, and you ruled it</b> &mdash; <code>s217-D2</code> carries '
      'a two-row threshold at <b>taller than 1:%.2f</b>. Nothing was decided to make this wall; '
      'three portrait derivatives were minted from the library and the derivation put them where '
      'you can see them. Portrait tiles are <b>two rows tall</b>, landscape tiles one.</p>'
      % p["aspect_tall"])
    A('<div class="c-bento dx-portrait dx-square"><div class="c-bento__grid">')
    for r, s in zip(mixed, pspans):
        # ⚠ The caption carries the ORIENTATION here, and only here. One of the library's
        # landscape photographs has "Portrait of a young man…" as its own EXIF description —
        # in a section about portrait orientation that reads as a contradiction. Labelling the
        # tile is honest; quietly dropping the photograph to avoid the coincidence is not.
        A(photo_tile(dict(r, span=s, desc="%s · %s" % (r["orient"].upper(), r["desc"])),
                     extra_class="dx-shot-%s" % esc(r["orient"])))
    A('</div></div>')
    A('<p class="note t-ed-body-small">%s'
      '<b>Measured, not asserted.</b> %s of these %d photographs are portrait '
      '(%s), and each resolves to <code>data-r="2"</code>. The threshold is read from '
      '<code>tokens/layout.json</code>, so it is the same number the stylesheet comment quotes.</p>'
      % ("", len(ports), len(mixed),
         ", ".join("%s&times;%s" % (r["w"], r["h"]) for r in ports) or "none on disk"))
    A('</section>')

    # ---- 2 · cards, authored spans -----------------------------------------------------
    A('<section id="cards">')
    A('<h2 class="t-ed-heading-3">The same grammar, mixed cards</h2>')
    A('<p class="lede t-ed-body">One grammar covers all four bento types. These spans are '
      '<b>authored</b> &mdash; <code>data-c</code> / <code>data-r</code> on the tile &mdash; which '
      'is what a preset or a snap-designer export produces.</p>')
    cspans, _crep = wall([(c[3], c[4]) for c in CARDS])
    A('<div class="c-bento dx-square"><div class="c-bento__grid">')
    for c, s in zip(CARDS, cspans):
        A(card_tile((c[0], c[1], c[2], s[0], s[1])))
    A('</div></div>')
    A('</section>')

    # ---- 2b · THE SQUARING PASS — Dave's second question, PROPOSED --------------------
    rag_spans = [(c[3], c[4]) for c in AWKWARD]
    rag_ok, rag_cols, rag_holes = is_rectangular(rag_spans, band_ladder(p))
    sq_spans, sq_rep = wall(rag_spans)
    A('<section id="squaring">')
    A('<h2 class="t-ed-heading-3">No orphaned compartments</h2>')
    # ⛔ #219 — THE BADGE IS GONE, AND IT HAD TO GO. v2 badged this section "Proposed — not ruled".
    # `s217-D3` RATIFIED the pass for dashboard and brochureware in the same sitting v2 was built,
    # so the badge was inviting Dave to re-decide something he had decided
    # ([[feedback-dont-launder-a-premise-into-a-ruling]]). What remains open is narrower and named.
    A('<p class="badge t-cm-legal">Ruled &mdash; s217-D3 (%s)</p>' % esc("Q1"))
    A('<p class="lede t-ed-body">Your second question at #217: <i>&ldquo;Is there a way to avoid '
      'orphaned compartments so the bento is always cohesively rectangular?&rdquo;</i> Yes, and '
      '<b>you ratified it</b> &mdash; <code>s217-D3</code>: <i>&ldquo;SQUARING PASS RATIFIED for '
      'dashboard and brochureware roles&rdquo;</i>, with gallery exempted in the same breath. It '
      'has to be decided when the wall is built, not patched afterwards: CSS can back-fill holes '
      'but it cannot resize a tile, so no stylesheet and no script can straighten that bottom '
      'edge. <b>The mechanism below is ruled. What is still yours is narrower, and it is stated '
      'underneath rather than implied by a badge over the whole thing.</b></p>')
    A('<div class="dx-2up">')
    A('<div><div class="sublabel t-ed-caption">Eleven tiles, as authored</div>'
      '<div class="c-bento dx-awkward dx-ragged"><div class="c-bento__grid">')
    for c, s in zip(AWKWARD, rag_spans):
        A(card_tile((c[0], c[1], c[2], s[0], s[1])))
    A('</div></div><span class="dx-caption t-cm-legal">Ragged &mdash; %d empty cell(s) at %d '
      'columns, and the last row is short at every band.</span></div>' % (rag_holes, rag_cols or 6))
    A('<div><div class="sublabel t-ed-caption">The same eleven tiles, squared</div>'
      '<div class="c-bento dx-awkward dx-square"><div class="c-bento__grid">')
    for c, s in zip(AWKWARD, sq_spans):
        A(card_tile((c[0], c[1], c[2], s[0], s[1])))
    A('</div></div><span class="dx-caption t-cm-legal">Square &mdash; %s rows at 6 / 3 / 2 / 1 '
      'columns, no empty cell in any of them. %d tile(s) re-spanned.</span></div>'
      % (" / ".join(str(sq_rep["rows"][c]) for c in sq_rep["ladder"]), len(sq_rep["changed"])))
    A('</div>')
    A('<p class="note t-ed-body-small"><b>How it works, in one breath.</b> The generator '
      'simulates the browser&rsquo;s own dense placement, asks whether every cell down to the '
      'last row is filled, and if not re-spans the <b>last few tiles</b> until it is &mdash; '
      'testing every column count the responsive bands produce, not just the wide one. A wall '
      'that is square at six columns and ragged at three is the same defect, later. '
      'Photographs get a say: laying a portrait on its side to square a wall costs more than '
      'nudging a card, so the pass avoids it. It is deterministic &mdash; the same tiles always '
      'give the same wall &mdash; and when a wall genuinely cannot be a rectangle at every band '
      '(three tiles at six columns cannot) it <b>says so by name</b> rather than shipping a '
      'ragged edge quietly.</p>')
    # ⬛ THE TWO GENUINELY-OPEN RESIDUES, each carrying its owner and what an answer would mint.
    # v2 asked three things here in one paragraph; one of the three was already ruled and the
    # other two were buried behind it.
    A(recut.open_control_html("Q2"))
    A(recut.open_control_html("Q3"))
    A('</section>')

    # ---- 3 · the bento of bentos -------------------------------------------------------
    A('<section id="nested">')
    A('<h2 class="t-ed-heading-3">A bento of bentos</h2>')
    A('<p class="lede t-ed-body">Your example, built: <b>three bentos at 1px gutter inside one '
      'outer bento at 40px</b>. Each level carries its own parameter set &mdash; the inner walls '
      'are not inheriting the outer’s tuning, and the outer is not inheriting the theme’s. '
      'No JavaScript, no new classes: an inner bento is a tile that is also a bento.</p>')
    # ⚠ EACH LEVEL IS SQUARED AT ITS OWN LADDER. The outer wall's tiles are the three inner
    # bentos; the inner walls run at three columns, so they are squared against 3/2/1 and the
    # outer against 6/3/2/1. Squaring an inner wall against canon's six would refuse a wall that
    # is rectangular at every width it is ever rendered at.
    out_spans, _ = wall([(3, 1), (3, 1), (6, 1)])
    A('<div class="c-bento dx-outer dx-square"><div class="c-bento__grid">')
    # inner A — photography, spans 3 of 6 outer columns
    a_spans, _ = wall([(1, 1)] * 6, columns=3)
    A('<div class="c-bento__tile c-bento dx-inner dx-square" data-c="%d" data-r="%d">'
      '<div class="c-bento__grid">' % out_spans[0])
    for r, s in zip(photos[:6], a_spans):
        A(photo_tile(dict(r, span=s)))
    A('</div></div>')
    # inner B — cards, spans 3 of 6
    b_spans, _ = wall([(1, 1)] * 6, columns=3)
    A('<div class="c-bento__tile c-bento dx-inner dx-square" data-c="%d" data-r="%d">'
      '<div class="c-bento__grid">' % out_spans[1])
    for c, s in zip(CARDS[:6], b_spans):
        A(card_tile((c[0], c[1], c[2], s[0], s[1])))
    A('</div></div>')
    # inner C — full width of the outer, mixed
    c_spans, _ = wall([(1, 1)] * 6, columns=3)
    A('<div class="c-bento__tile c-bento dx-inner dx-square" data-c="%d" data-r="%d">'
      '<div class="c-bento__grid">' % out_spans[2])
    mix = [("photo", r) for r in photos[6:9]] + [("card", c) for c in CARDS[2:5]]
    for (kind, item), s in zip(mix, c_spans):
        A(photo_tile(dict(item, span=s)) if kind == "photo"
          else card_tile((item[0], item[1], item[2], s[0], s[1])))
    A('</div></div>')
    A('</div></div>')
    A('<p class="note t-ed-body-small"><b>What to look at in console.</b> The corner radius is on '
      'each bento’s <b>outer container</b> &mdash; four rounded containers (the outer, plus the '
      'three inner walls), and every tile inside them square. That is your ruling rendered: '
      '<i>&ldquo;the corner radius only on the outer container of each bento rather than the '
      'individual blocks&rdquo;</i>. The container clips, which is why the square tile corners do '
      'not poke through the curve.</p>')
    A('</section>')

    # ---- 4 · the bands -----------------------------------------------------------------
    A('<section id="bands">')
    A('<h2 class="t-ed-heading-3">The bands answer the wall, not the window</h2>')
    A('<p class="lede t-ed-body">Three identical bentos at three fixed widths, on one page at one '
      'viewport. They collapse at <b>%d &rarr; 3</b>, <b>%d &rarr; 2</b> and <b>%d &rarr; 1</b> '
      'because each bento is its own container &mdash; which is also the reason nesting works.</p>'
      % (p["band_wide"], p["band_mid"], p["band_narrow"]))
    band_spans, _ = wall([(2, 1)] * 4)
    A('<div class="dx-band-row">')
    for cls, label in (("dx-w1000", "1000px wall &mdash; below 1100, so 3 columns"),
                       ("dx-w780", "780px wall &mdash; below 820, so 2 columns"),
                       ("dx-w460", "460px wall &mdash; below 520, so 1 column")):
        A('<div class="%s"><div class="c-bento dx-square"><div class="c-bento__grid">' % cls)
        for c, s in zip(CARDS[:4], band_spans):
            A(card_tile((c[0], c[1], c[2], s[0], s[1])))
        A('</div></div><span class="dx-caption t-cm-legal">%s</span></div>' % label)
    A('</div>')
    A('</section>')

    # ---- 5 · what this page is ---------------------------------------------------------
    A('<section id="provenance">')
    A('<h2 class="t-ed-heading-3">What is canon here, and what is this page</h2>')
    A('<p class="lede t-ed-body">Canon: the container, the grid, the span vocabulary, the bands '
      'and the radius model &mdash; all of it generated into <code>knowledge/canon/canon.css</code> '
      'by <code>canon/gen_canon_bento.py</code> from <code>tokens/layout.json</code> '
      '(<code>layout/bento</code>). The gutter override lives in the legacy and console override '
      'sets. This page declares <b>no grid, no gap and no bento radius of its own</b> &mdash; it '
      'styles tile content and its own chrome, and nothing else.</p>')
    if residuals.get("missing_derivative_file"):
        A('<p class="note t-ed-body-small">⚠ Manifest rows naming a derivative that is not on '
          'disk: %s</p>' % esc(", ".join(residuals["missing_derivative_file"])))
    A('</section>')
    return "\n".join(S)


def recut_css():
    """The page stylesheet with the #219 re-cut baked in: the ruled caption block (token, with a
    MINT-TIME literal fallback), the `s219-D2 (1)` mono caption ground, and the ledger's chrome."""
    space, lines = caption_space()
    return (CSS
            .replace("__CAPSPACE__", str(space))
            .replace("__CAPLINES__", str(lines))
            .replace("__MONOCAP__", recut.mono_caption_css([(".dx-cap", [])]))
            .replace("__RECUT__", recut.RECUT_CSS))


def page(photos, residuals):
    return ((HEAD
             .replace("__TITLE__", "Apollo &mdash; the bento, promoted to canon")
             .replace("__SENTINEL__", SENTINEL)
             .replace("__UP__", UP)
             .replace("__CSS__", recut_css())
             .replace("__H1__", "The bento, promoted to canon")
             .replace("__SUBTITLE__",
                      "s217-D2 &middot; re-cut #219 &middot; four themes &times; light/dark"))
            + build(photos, residuals) + TAIL.replace("__SCRIPT__", SCRIPT))


def main():
    global SQUARE
    out = OUT
    argv = sys.argv[1:]
    if "--no-square" in argv:
        # ⬛ THE MUTATION HANDLE. Disables the PROPOSED squaring pass so the probe can prove its
        # bottom-edge assertion is capable of going red. Never writes over the real page.
        SQUARE = False
        out = OUT.replace(".html", "-NOSQUARE.html")
    for i, a in enumerate(argv):
        if a == "--out":
            out = argv[i + 1]
    del SQUARE_REPORTS[:]
    photos, residuals = read_photos()
    if not photos:
        print("⚠ no committed photography derivatives found — the photography bento will be empty")
    html = page(photos, residuals)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    ports = [r for r in photos if r["orient"] == "portrait"]
    print("Wrote %s  (%d photo tiles — %d portrait, %d card tiles)"
          % (out, len(photos), len(ports), len(CARDS)))
    print("  squaring pass: %s" % ("DISABLED (--no-square, mutation arm)" if not SQUARE
                                   else "ON — RATIFIED s217-D3 (dashboard + brochureware)"))
    for i, rep in enumerate(SQUARE_REPORTS, 1):
        print("    wall %d  ladder %-12s rows %-16s %s"
              % (i, str(rep["ladder"]),
                 " / ".join(str(rep["rows"][c]) for c in rep["ladder"]),
                 ("squared, %d tile(s) re-spanned" % len(rep["changed"])) if rep["squared"]
                 else "⛔ NOT SQUARE — %s" % rep["reason"]))
    unsq = [r for r in SQUARE_REPORTS if not r["squared"]]
    if unsq and SQUARE:
        print("❌ DECLARED RESIDUAL: %d wall(s) could not be squared — see the reasons above"
              % len(unsq))
    if residuals.get("missing_derivative_file"):
        print("  residual — manifest rows with no file: %s"
              % ", ".join(residuals["missing_derivative_file"]))
    return 0


def selftest():
    """8 bites: canon-only structure · nesting shape · derived vs authored spans · dial surface ·
    portrait two-row · squaring pass + its ragged control · every wall square · mutation handle."""
    photos, res = read_photos()
    del SQUARE_REPORTS[:]
    h = page(photos, res)
    css = h.split("<style>", 1)[1].split("</style>", 1)[0]
    import re as _re
    body = _re.sub(r"/\*.*?\*/", "", css, flags=_re.S)
    for banned in ("grid-template-columns", "grid-auto-rows", "grid-auto-flow"):
        assert banned not in body, \
            "bite 1 FAIL: the page declares %s — structure must come from canon, not here" % banned
    # a rule that TARGETS a bento may not declare structure or a radius — page chrome (.seg
    # etc.) is free to round itself, and blanket-banning `border-radius` would have said the
    # opposite of what is meant.
    for sel, decls in _re.findall(r"([^{}]+)\{([^{}]*)\}", body):
        if "c-bento" in sel and "border-radius" in decls:
            raise AssertionError("bite 1b FAIL: %r declares a bento radius of its own" % sel.strip())
    assert h.count('class="c-bento__tile c-bento dx-inner dx-square"') == 3, \
        "bite 2 FAIL: the bento-of-bentos must carry exactly three inner bentos"
    assert "--bento-gutter:1px" in css and "--bento-gutter:40px" in css, \
        "bite 2b FAIL: Dave's 1px-inside-40px example is not what the page declares"
    p = params()
    assert span_for(1600, 1067, p) == (1, 1), "bite 3 FAIL: the derivation moved under us"
    assert 'class="c-bento__tile dx-card ' in h and 'data-c="2"' in h, \
        "bite 3b FAIL: authored card spans are not being emitted"
    dials = set(_re.findall(r"(--bento-[a-z-]+)\s*:", css))
    assert dials <= {"--bento-gutter", "--bento-columns", "--bento-row-unit", "--bento-outer-padding",
                     "--bento-packing", "--bento-radius"}, \
        "bite 4 FAIL: the page invented a bento dial canon does not define — %r" % dials

    # --- bite 5: PORTRAIT lands two rows tall, on the page, not just in the derivation --------
    ports = [r for r in photos if r["orient"] == "portrait"]
    assert len(ports) >= 3, \
        "bite 5a FAIL: fewer than three portrait derivatives on disk — the portrait section " \
        "cannot prove anything (%d found)" % len(ports)
    psec = h.split('<section id="portrait">', 1)[1].split("</section>", 1)[0]
    shots = _re.findall(r'dx-shot-(\w+)" data-c="(\d)" data-r="(\d)"', psec)
    assert shots, "bite 5b FAIL: the portrait section drew no tiles"
    for orient, c, r in shots:
        if orient == "portrait":
            assert r == "2", "bite 5c FAIL: a portrait tile rendered data-r=%s — the s217-D2 " \
                             "two-row threshold did not reach the page" % r
    assert sum(1 for o, _, _ in shots if o == "portrait") >= 3, \
        "bite 5d FAIL: fewer than three portrait tiles in the section that exists to show them"

    # --- bite 6: the squaring pass, its control, and its PROPOSED marking --------------------
    ssec = h.split('<section id="squaring">', 1)[1].split("</section>", 1)[0]
    assert "dx-ragged" in ssec and "dx-square" in ssec, \
        "bite 6a FAIL: the squaring section must show BOTH the ragged control and the squared " \
        "wall — one wall on its own proves nothing"
    # ⛔ #219 REVERSED THIS BITE, AND THE REVERSAL IS THE POINT. It used to require the words
    # "not ruled" in this section. `s217-D3` RATIFIED the pass, so the old assertion was pinning a
    # settled question open — a gate enforcing the laundering defect. It now requires the RECEIPT,
    # and forbids the page re-putting the ruled mechanism as a choice.
    assert "s217-D3" in ssec, \
        "bite 6b FAIL: the squaring section does not carry the ruling that closed it — a struck " \
        "question with no receipt beside it reads as a question somebody forgot to ask"
    assert "not ruled" not in ssec.lower(), \
        "bite 6b2 FAIL: the squaring pass is RULED (s217-D3) and this section still says it is " \
        "not — re-putting a settled ruling as an option is the defect the #219 re-cut exists to fix"
    for k in ("Q2", "Q3"):
        assert 'rcut-tag-o t-cm-legal">Open &middot; %s' % k in ssec, \
            "bite 6b3 FAIL: the open residue %s lost its live control, so the part that IS still " \
            "Dave's would disappear along with the part that is not" % k
    rag = [(int(a), int(b)) for a, b in
           _re.findall(r'data-c="(\d)" data-r="(\d)"',
                       ssec.split('dx-ragged', 1)[1].split("</div></div>", 1)[0])]
    assert rag and not is_rectangular(rag, band_ladder(p))[0], \
        "bite 6c FAIL: the CONTROL wall is already square — it cannot show the defect it exists " \
        "to show (%r)" % rag
    sq = [(int(a), int(b)) for a, b in
          _re.findall(r'data-c="(\d)" data-r="(\d)"',
                      ssec.split('dx-awkward dx-square', 1)[1].split("</div></div>", 1)[0])]
    assert len(sq) == len(rag) == len(AWKWARD), \
        "bite 6d FAIL: the two walls must carry the SAME tiles — %d vs %d" % (len(rag), len(sq))
    assert is_rectangular(sq, band_ladder(p))[0], \
        "bite 6e FAIL: the squared wall is not a rectangle at every band — %r" % (sq,)

    # --- bite 7: EVERY non-control wall on the page is square, at its own ladder -------------
    unsq = [i for i, rep in enumerate(SQUARE_REPORTS, 1) if not rep["squared"]]
    assert not unsq, "bite 7 FAIL: wall(s) %r shipped ragged — a wall believed square and " \
                     "rendered ragged is the defect with a green banner over it" % unsq

    # --- bite 7b (#219): THE RULED CAPTION BLOCK IS CONSUMED, AND AS A TOKEN -------------------
    # ⚠ THE GAP DAVE NAMED. v2 rendered captions that read the ruled number from nowhere.
    space, lines = caption_space()
    capdecls = body.split(".dx-cap{", 1)[1].split("}", 1)[0]
    assert "min-height:var(--layout-bento-caption-space" in capdecls.replace(" ", ""), \
        "bite 7b FAIL: the caption block does not consume layout/bento/caption-space — the ruled " \
        "space reaches nothing, which is exactly what Dave caught on v2"
    assert "var(--bento-caption-lines" in capdecls, \
        "bite 7c FAIL: the clamp is not reading the DERIVED line allowance, so the space and the " \
        "clamp can disagree"
    assert "%dpx" % space in capdecls and str(lines) in capdecls, \
        "bite 7d FAIL: the fallbacks were not minted from caption_space() at build time"
    assert 'class="c-bento__caption dx-cap' in h, \
        "bite 7e FAIL: the photo captions are not in canon's caption slot"
    # ⬛ #219 seam 5 — BITE 7f FLIPPED WITH THE RULING, and it now asserts BOTH halves: the enacted
    # ground is present AND the retired one is nowhere. Asserting only the presence of the new
    # ground would have passed a page that painted both and let the cascade decide which Dave saw.
    _g, _i = recut._cap_tokens()
    assert "var(%s," % _g[0] in body and "var(%s," % _i[0] in body, \
        "bite 7f FAIL: the s219-D2(1) mono caption ground (%s / %s) is not on the page" \
        % (_g[0], _i[0])
    for _dead in (recut.RETIRED_MONO_CAPTION_218["ground"][0],
                  recut.RETIRED_MONO_CAPTION_218["ink"][0]):
        assert "var(%s," % _dead not in body, \
            "bite 7f2 FAIL: the RETIRED %s is still painted — s219-D2 (1) superseded it and a " \
            "review page may not put a superseded ground to Dave" % _dead

    # --- bite 7g (#219): the ledger is present, struck, and nothing settled is a live control --
    dsec = h.split('<section id="decided">', 1)[1].split("</section>", 1)[0]
    assert "<s>" in dsec, "bite 7g FAIL: no question is struck — the re-cut did nothing"
    for r in recut.rows_for("canon"):
        if r["state"] == recut.RULED:
            assert 'Open &middot; %s' % r["key"] not in h, \
                "bite 7h FAIL: %s is RULED and is being offered as a live control" % r["key"]

    # --- bite 8: the mutation handle actually mutates ----------------------------------------
    global SQUARE
    try:
        SQUARE = False
        del SQUARE_REPORTS[:]
        page(photos, res)
        broke = [i for i, rep in enumerate(SQUARE_REPORTS, 1) if not rep["squared"]]
    finally:
        SQUARE = True
        del SQUARE_REPORTS[:]
    assert broke, "bite 8 FAIL: with the squaring pass DISABLED every wall was still square — " \
                  "the mutation arm cannot discriminate, so a green probe proves nothing"

    print("gen_bento_canon_217 selftest OK (8 bites: canon-only structure · nesting · spans · "
          "dials · portrait two-row · squaring + control · every wall square · mutation handle)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        sys.exit(main())
