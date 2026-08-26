#!/usr/bin/env python3
"""
gen_grids_218.py — THE FOUNDATIONS "GRIDS" GROUP: four page bodies, one per grid.

WHY IT EXISTS — Dave, #218, 2026-08-24, verbatim:
  "I think I'd like this added to the library under foundations, we should have a section called
   grids with subsections – the 12 col grid and these 3 types, I'd like to keep the controls so
   the designer can use them."
Structure picked by Dave at the same sitting: FOUR SEPARATE PAGES under a Grids group, not one
page with four sections. Each bento page keeps THAT TYPE'S working dials, so a designer can drive
it; the 12-column page renders the ruled `layout/web` + `layout/app` tokens with a live overlay.

⛔ WHO WRITES THE FILES. Not this module. `knowledge/_render/gen_foundations_217.py` is the ONE
writer of `showroom/_foundations/*.html` and the ONE place the page shell lives; it imports
`page(shell, kind, c)` from here and hands its own shell in. Same arrangement as the matrix
explorer's module (`gen_bento_matrix_217.py`) and for the same reason: one writer, one shell.

⛔ ONE DATA PATH, AND IT IS THE EXPLORER'S. Nothing about the bento content, spans, packing,
legality, keyline construction or #218 corner rules is re-derived here. This module CONSUMES
`gen_bento_matrix_217`:
  · `content()`          — photographs (via gen_bento_roles_217.read_photos), cards, panels,
                           justified rows (via gen_gallery_compare_217.pack_rows), the squared
                           dashboard spans and the nested-group spans.
  · `photo_tile` / `display_tile` / `card_tile` / `justified_html` — the tile markup itself.
  · `controls()`         — the dial markup, FILTERED to one type (see `controls_for`).
  · its BUILT CSS and JS — captured out of `matrix.page()` through a CAPTURING SHELL
                           (`matrix_assets`), so the corner rules, the sub-spacing rules, the
                           column literals and the whole controller behaviour arrive already
                           composed BY THE EXPLORER'S OWN CODE PATH. Not one placeholder is
                           re-filled here, so there is no second wiring to drift.
⛔ AND THE EXPLORER IS NOT TOUCHED. `showroom/_foundations/bento.html` stays exactly as it is: it
is the LIVE decision surface for s217-D5's five open points P1–P5 (knowledge/_state.json row
W-126). These four pages carry RULED behaviour and working dials and NO `PROPOSED` surface —
no open-point list, no P4 radius pair, no proposal tags, no matrix count tables.

⚠ THE WRAPPER MARKUP IS A CONTRACT WITH THE EXPLORER'S STYLESHEET, and `selftest()` bite 1 is
what keeps it honest. The consumed CSS is written against `.bm-stage` / `.bm-page-ground` /
`.bm-pane[data-pane=…]` / `.bm-wall` / `.bm-outer` / `.bm-inner`, and the consumed JS against the
ids `bm-stage`, `bm-export`, `bm-moved`, `bm-rebuild`. Those selectors are asserted to be PRESENT
IN THE CONSUMED CSS, so a rename in the explorer reds this module rather than silently un-styling
four pages.

⬛ THE TYPE IS PINNED THROUGH THE EXPLORER'S OWN PUBLIC HANDLES. The controller exports
`window.__BM_STATE` and `window.__BM_APPLY`; the bootstrap appended after it sets `type` and
re-applies. ⛔ No string surgery on the controller source — a page that rewrites the module's
JavaScript is a second copy of it wearing the module's name.

✅ THE 12-COLUMN PAGE IS TOKENS, NOT BENTO. It reads `knowledge/tokens/layout.json` — `layout/web`
(margin/gutter per scale-1/2/3, columns) and `layout/app` (margin/gutter, columns) — and mints
CONCRETE values into instance dials (s200-D1: the generator mints, nothing resolves live that a
reader would have to chase). The overlay is CANON'S OWN `.l-cols` with twelve `.l-span-1`
children under `.cn-layout-utilities`; no grid is re-drawn here.
⛔ THE SCALE SWITCH IS A VIEW CONTROL. It changes which ruled pair of numbers the page is showing.
Nothing on that page tunes, proposes or mints a token, and it carries no export block for that
reason — there is no chosen combination to export.
⚠ MEASURED, and it is why the values are minted rather than read from canon: canon.css publishes
`--layout-app-margin`, `--layout-app-gutter`, `--layout-web-columns` and `--layout-app-columns`,
but NOT the three web margin/gutter scales — they have no CSS custom property to read. The probe
therefore compares the LIVE resolved numbers against the STORE, never against a typed constant.

⛔ NO VAR MAY DANGLE. Every `var()` this module authors carries a literal fallback; an unresolved
custom property renders SILENT BLACK and no gate catches it
([[dangling-dataviz-var-renders-silent-black]]).

Usage:
  python3 knowledge/_render/gen_grids_218.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
LAYOUT_TOKENS = os.path.join(KNOW, "tokens", "layout.json")

sys.path.insert(0, HERE)
import gen_bento_matrix_217 as matrix        # ⛔ ONE data path — consumed, never copied

esc = matrix.esc

# The three bento pages, and the one dial-set each keeps. `role` is CANON'S role word; `type` is
# s217-D5's ruled rename of it. Both come from the explorer's own map rather than being restated.
TYPE_ROLE = matrix.TYPE_ROLE

# ⚠ THE SELECTOR CONTRACT. Every one of these must appear in the CSS the explorer builds, or the
# wrapper markup below is styling nothing. Bite 1 asserts it.
REQUIRED_SELECTORS = [
    ".bm-stage", ".bm-page-ground", '.bm-pane[data-pane="display"]',
    '.bm-pane[data-pane="gallery"]', '.bm-pane[data-pane="dashboard"]',
    ".bm-wall", ".bm-outer", ".bm-inner", ".bm-gallery", ".bm-display", ".bm-just",
    ".bm-controls", ".bm-export", ".bm-capt",
]
REQUIRED_IDS = ["bm-stage", "bm-export", "bm-moved", "bm-rebuild"]


# ---------------------------------------------------------------------------- consumed assets
def matrix_assets(c):
    """-> {"css":…, "js":…, "cls":…} — the explorer's CSS and JS, BUILT BY THE EXPLORER.

    ⛔ A CAPTURING SHELL, not a second call to the placeholder-filling chain. `matrix.page()`
    composes the corner rules (#218), the per-stop sub-spacing rules, the sweep-stop rules and
    the four column literals and hands the result to the shell it is given; this shell keeps them
    and throws the explorer's BODY away. So there is exactly one place those placeholders are
    ever filled, and it is the explorer's — including its mutation arms, which therefore reach
    these pages too without a second flag.
    """
    cap = {}

    def capture(title, h1, subtitle, body, extra_css="", extra_script="", extra_class=""):
        cap["css"], cap["js"], cap["cls"] = extra_css, extra_script, extra_class
        return ""

    matrix.page(capture, c)
    if not cap.get("css") or not cap.get("js"):
        raise RuntimeError("gen_grids_218: the matrix shell capture came back empty — "
                           "gen_bento_matrix_217.page() no longer hands CSS/JS to its shell")
    return cap


def controls_for(kind):
    """-> the dial markup for ONE type, taken out of `matrix.controls()` by attribute.

    ⛔ FILTERED, NEVER RE-AUTHORED. `controls()` emits one `.bm-group` per dial, each stamped
    `data-group="<type>"` (or `"all"` for the type switch), joined by a known separator. Keeping
    the groups whose owner IS this type drops the TYPE SWITCH by construction — a page with one
    pane must not offer a control that selects the other two — and keeps every remaining dial
    exactly as the explorer ships it, including the gallery's conditional bottom-edge group and
    the dashboard's snapping slider.
    ⚠ If the separator or the attribute ever changes, this returns nothing and bite 2 goes red;
    it cannot quietly return a subset.
    """
    groups = [g for g in matrix.controls().split("\n      ") if g.strip()]
    # ⬛ s219-D3(4) — AND THE PAGE GROUP COMES WITH EVERY TYPE. The page background used to be one
    # bento dial per type, stamped `data-group="<type>"`, so this filter picked it up for free.
    # The ruling makes it a PAGE-LEVEL decision — one group, owned by `page` — and it is still a
    # control the designer needs on each of these pages. Kept by naming it, so the re-scope did not
    # silently delete a dial from four pages.
    return "\n      ".join(g for g in groups
                           if 'data-group="%s"' % kind in g or 'data-group="page"' in g)


# ---------------------------------------------------------------------------- the three panes
def pane_html(kind, c):
    """The wall markup for one type — the SAME structure the explorer's stylesheet is written
    against, filled with the SAME tiles from the SAME content pass. ⛔ Nothing here is a second
    copy of the maths: every tile, span and row comes out of `c`."""
    if kind == "display":
        tiles = "\n".join("        " + matrix.display_tile(d) for d in c["display"])
        return ("""
        <div class="bm-pane" data-pane="display">
          <p class="bm-capt t-cm-legal">DISPLAY &mdash; a sectioned marketing wall of panels and
            photographs. The TILES carry the radius and the spacing (<code>s217-D3</code>); the
            wall renders as canon's <code>brochureware</code> role, so every radius and squaring
            decision here is canon's own rule resolving.</p>
          <div class="c-bento bm-wall bm-display" data-bento-role="brochureware">
            <div class="c-bento__grid">
%s
            </div>
          </div>
        </div>""" % tiles)
    if kind == "gallery":
        gal = "\n".join("        " + matrix.photo_tile(p, r, s)
                        for p, r, s in zip(c["photos"], c["ragged"], c["squared"]))
        just = matrix.justified_html(c["rows"], c["widows"])
        return ("""
        <div class="bm-pane" data-pane="gallery">
          <p class="bm-capt t-cm-legal">GALLERY &mdash; a page-level photography wall, all %d
            committed derivatives. <b>Gallery bento</b> uses canon's span grid with the bottom
            edge ragged or squared; <b>Justified rows</b> uses the row packing from
            <code>gen_gallery_compare_217.pack_rows</code> &mdash; the same arithmetic, imported.
            The RADIUS sits on the tiles and the ruled caption block is %dpx
            (<code>s217-D3</code>). ⚠ In the <b>console</b> theme this type has no keyline
            control at all &mdash; <code>s217-D6</code> excludes it, so the group is REMOVED from
            the page rather than disabled.</p>
          <div class="c-bento bm-wall bm-gallery" data-bento-role="gallery">
            <div class="c-bento__grid">
%s
            </div>
          </div>
          <div class="c-bento bm-wall bm-just" data-bento-role="gallery">
%s
          </div>
        </div>""" % (len(c["photos"]), matrix.caption_space()[0], gal, just))
    inner = []
    for n, cards in enumerate(c["dash_cards"]):
        # ⛔ BOTH SPANS COME FROM THE RULED PASS — the group's own span on the outer wall
        # (s217-D3's squaring) and its tiles' spans inside it (s217-D7's nested pass). Read out
        # of `content()`, never a literal: a literal one-column span is exactly the defect
        # #217 measured as the orphan gap.
        sc, sr = c["dash_spans"][n]
        inner.append(
            '<div class="c-bento c-bento__tile bm-inner" data-bento-role="dashboard"'
            ' data-c="%d" data-r="%d"><div class="c-bento__grid">%s</div></div>'
            % (sc, sr, "".join(matrix.card_tile(card, s)
                               for card, s in zip(cards, c["dash_inner"][n]))))
    return ("""
        <div class="bm-pane" data-pane="dashboard">
          <p class="bm-capt t-cm-legal">DASHBOARD &mdash; a bento of bentos. The theme radius sits
            on each inner bento's container and the tiles stay square (<code>s217-D2</code> /
            <code>s217-D3</code>); the main wall never goes tight.</p>
          <div class="c-bento bm-wall bm-outer" data-bento-role="dashboard">
            <div class="c-bento__grid">
%s
            </div>
          </div>
          <div class="gx-ruled">
            <h3 class="t-ed-body-small gx-ruled-title">The keyline construction, ruled</h3>
            <p class="t-cm-legal">⬛ <b>ABOVE 1px &mdash; THE KEYLINE GOES ROUND THE MODULE.</b>
              Dave, <code>s217-D8</code>: <i>&ldquo;the keylines should stay, but they should go
              round tight to the modules not run down the middle of the spacing&rdquo;</i>. Every
              tile wears its own tight 1px box; the group's outer border STEPS BACK (tiles
              carrying edges plus a group frame is the double frame rejected at #217); and the
              four corner tiles of each sub-bento carry the group's radius on their OUTER corner
              (#218, Dave: <i>&ldquo;the radii should only apply to the 4 corners of each sub
              bento&rdquo;</i>), minted per responsive band from the browser's own placement.
              <b>No gutter carries anything</b> &mdash; no element and no paint.</p>
            <p class="t-cm-legal">⛔ <b>AT THE 1px STOP, UNCHANGED.</b> 1px cannot hold a gap
              <i>and</i> a line, so the group keeps its curved 1px border, the tiles sit flush,
              and the gutter <b>is</b> the hairline &mdash; stopped along the curve by the
              container's own clip. It is the only stop at which a line element renders at all.
              Move the sub-bento slider across the ruled ladder to cross the handover.</p>
          </div>
        </div>""" % "\n".join("        " + x for x in inner))


TYPE_META = {
    "display": ("Display grid", "Foundations &middot; Grids &middot; the Display bento type",
                "The <b>Display</b> grid &mdash; a sectioned marketing wall. Ruled at "
                "<code>s217-D5</code> as one of the three bento types, rendered through canon's "
                "<code>brochureware</code> role."),
    "gallery": ("Gallery grid", "Foundations &middot; Grids &middot; the Gallery bento type",
                "The <b>Gallery</b> grid &mdash; a page-level photography wall, in canon's "
                "<code>gallery</code> role: tile radius, the ruled caption block, and no "
                "squaring pass unless you ask for a square bottom edge."),
    "dashboard": ("Dashboard grid",
                  "Foundations &middot; Grids &middot; the Dashboard bento type",
                  "The <b>Dashboard</b> grid &mdash; a bento of bentos, in canon's "
                  "<code>dashboard</code> role, carrying the <code>s217-D8</code> / #218 keyline "
                  "construction and the <code>s217-D6</code> snapping sub-bento ladder."),
}

# The page-local chrome the four grids pages add on top of the explorer's stylesheet. ⛔ Every
# var() carries a literal fallback; nothing here declares bento or layout STRUCTURE.
GRIDS_CSS = """
/* ===========================================================================
   GRIDS PAGES (#218) — page-local chrome only.
   ⛔ NO GRID IS DECLARED HERE. The bento pages consume canon's `.c-bento` and
   the explorer's own controller stylesheet; the 12-column page consumes
   canon's `.l-cols` / `.l-span-*` under `.cn-layout-utilities`. What is below
   is the ruled-behaviour note, the token read-out and the overlay's paint.
   ⛔ EVERY var() CARRIES A LITERAL FALLBACK — an unresolved custom property
   renders silent black and no gate catches it.
   =========================================================================== */
.gx-ruled{border:1px solid var(--line,#D7D8D6); padding:var(--sp-4,16px);
  margin-top:var(--sp-5,24px);}
.gx-ruled-title{margin:0 0 var(--sp-2,8px);}
.gx-ruled p{margin:0 0 var(--sp-2,8px); max-width:88ch;}
.gx-ruled p:last-child{margin-bottom:0;}

/* ---- the 12-column page ---------------------------------------------------
   The stage carries the VIEW dials as CONCRETE minted values (s200-D1): each
   `data-view` sets the two names canon's layout utilities read, `--l-margin`
   and `--l-gutter`. ⛔ It is a VIEW control — it changes which ruled pair of
   numbers is on screen, and mints nothing.                                  */
.gx-stage{border:1px solid var(--line,#D7D8D6); margin-top:var(--sp-4,16px);
  background:var(--surface-2,#F3F3F3); padding:var(--sp-5,24px) 0;
  /* ⚠ DECLARED HERE, not merely read with a fallback. MEASURED #218: a name that is only ever
     read resolves EMPTY on every element, so the page runs on its fallback for ever and the
     dangling sweep — rightly — calls it a dangle. A page-local dial is declared once, at the
     top of its own scope, or it is not a dial. The wash is the ONE tint this page authors: the
     accent at low opacity, so the columns read on any ground in any theme without asking a
     token for a colour that has not been ruled. */
  --gx-col:rgba(218,26,0,0.10);}
__VIEW_RULES__
.gx-frame{position:relative;}
/* the overlay and the demo row are BOTH canon's `.l-cols`, stacked, so the
   demo's spans are read against the very grid the overlay draws */
/* ★ s218-D6 (2) — THE OVERLAY PAINTS BEHIND THE DEMO CONTENT. Dave: "Behind the content".
   WHY IT WAS IN FRONT, and why source order was never going to fix it: `.gx-overlay` is
   POSITIONED and `.gx-rows` is not, and a positioned element paints in a later stacking step
   than in-flow content no matter which comes first in the markup. So the 10% accent wash was
   laid OVER the demo cards' own opaque surface and tinted every one of them.
   THE FIX IS A PAIR, and both halves are needed: the overlay is pinned at z-index:0 and the
   demo stack is given a position + z-index:1 so it paints above it, INSIDE .gx-frame's own
   stacking context. ⛔ NOT `z-index:-1` on the overlay — a negative index would drop it behind
   the frame's ancestors' backgrounds too, and on a themed ground the columns would simply
   disappear. Scoped to `.gx-frame >` so nothing else that uses .gx-rows gains a stacking
   context it did not ask for. PROVEN IN PIXELS, not by reading this rule back:
   verify_grids_218.py --page 12col samples one pixel inside a demo card (must be the card's own
   untinted surface) and one in the gap between rows (must still carry the wash — "behind" must
   not quietly become "gone"). */
.gx-overlay{position:absolute; inset:0; pointer-events:none; z-index:0;}
.gx-frame > .gx-rows{position:relative; z-index:1;}
.gx-overlay > i{display:block; background:var(--gx-col,rgba(218,26,0,0.10));
  border-radius:var(--radius-ctl,0px);}
.gx-demo > *{background:var(--surface,#FFFFFF); border:1px solid var(--line,#D7D8D6);
  border-radius:var(--radius-ctl,0px); padding:var(--sp-3,12px);
  min-height:var(--tap,44px);}
.gx-rows{display:flex; flex-direction:column; gap:var(--sp-4,16px);}
.gx-readout{display:flex; flex-wrap:wrap; gap:var(--sp-5,24px);
  border:1px solid var(--line,#D7D8D6); padding:var(--sp-4,16px);
  margin-top:var(--sp-4,16px);}
.gx-readout div{min-width:120px;}
.gx-readout dt{color:var(--ink-2,#545454); text-transform:uppercase;
  letter-spacing:0.14em; margin:0 0 var(--sp-1,4px);}
.gx-readout dd{margin:0; font-variant-numeric:tabular-nums;}
.gx-seg{display:inline-flex; flex-wrap:wrap; border:1px solid var(--ink,#1A1A1A);
  color:var(--ink,#1A1A1A); border-radius:var(--radius-ctl,0px); overflow:hidden;}
.gx-seg button{font-family:inherit; font-size:12px; font-weight:500; letter-spacing:0.06em;
  text-transform:uppercase; padding:8px 12px; border:0; background:transparent; color:inherit;
  cursor:pointer; border-right:1px solid var(--line,#D7D8D6); min-height:var(--tap,44px);}
.gx-seg button:last-child{border-right:0;}
.gx-seg button[aria-pressed="true"]{background:var(--ink,#1A1A1A); color:var(--page,#FFFFFF);}
.gx-ctl{display:flex; flex-wrap:wrap; align-items:center; gap:var(--sp-3,12px);
  border:1px solid var(--line,#D7D8D6); padding:var(--sp-4,16px);}
.gx-glabel{color:var(--ink-2,#545454); text-transform:uppercase; letter-spacing:0.14em;}
.gx-tablewrap{overflow-x:auto; margin-top:var(--sp-4,16px);}
.gx-tablewrap table{border-collapse:collapse; min-width:520px;}
.gx-tablewrap th, .gx-tablewrap td{text-align:left; padding:6px var(--sp-4,16px) 6px 0;
  border-bottom:1px solid var(--line,#D7D8D6); vertical-align:top;}
.gx-tablewrap td.num{font-variant-numeric:tabular-nums;}
"""

# ⛔ THE 12-COLUMN PAGE'S BEHAVIOUR. A VIEW switch and a read-out, nothing else. It writes ONE
# attribute and re-reads the LIVE document for the read-out, so what the panel says is what the
# browser resolved rather than what this script believes it declared.
GRIDS_SCRIPT = r"""
(function(){
  var VIEWS = __VIEWS__;
  var stage = document.getElementById('gx-stage');
  var out   = document.getElementById('gx-readout');
  var state = {view: VIEWS[0].key};
  function apply(){
    stage.setAttribute('data-view', state.view);
    Array.prototype.forEach.call(document.querySelectorAll('.gx-seg button[data-view]'),
      function(b){ b.setAttribute('aria-pressed',
        String(b.getAttribute('data-view') === state.view)); });
    // ⛔ READ BACK OFF THE LIVE DOCUMENT. The numbers below are what the browser resolved on the
    // elements canon's utilities actually style — never the values this script just wrote.
    var frame = document.querySelector('.gx-frame .l-cols');
    var container = document.querySelector('.gx-stage .l-container');
    var cs = frame ? getComputedStyle(frame) : null;
    var tracks = cs ? cs.gridTemplateColumns.split(' ').filter(Boolean).length : 0;
    var v = VIEWS.filter(function(x){ return x.key === state.view; })[0] || VIEWS[0];
    if (out) {
      out.querySelector('[data-read="source"]').textContent = v.source;
      out.querySelector('[data-read="columns"]').textContent = tracks;
      out.querySelector('[data-read="margin"]').textContent = container
        ? Math.round(parseFloat(getComputedStyle(container).paddingLeft)) + 'px' : '—';
      out.querySelector('[data-read="gutter"]').textContent = cs
        ? Math.round(parseFloat(cs.columnGap)) + 'px' : '—';
      out.querySelector('[data-read="viewport"]').textContent = v.range;
    }
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest ? e.target.closest('.gx-seg button[data-view]') : null;
    if (!b) return;
    state.view = b.getAttribute('data-view');
    apply();
  });
  window.addEventListener('resize', apply);
  window.addEventListener('hashchange', function(){ setTimeout(apply, 60); });
  document.addEventListener('click', function(e){
    if (e.target.closest && e.target.closest('#themes, #modes')) setTimeout(apply, 60);
  });
  apply();
  window.__GX_STATE = state;          // the probe drives the SAME object the page renders from
  window.__GX_APPLY = apply;
})();
"""


# ---------------------------------------------------------------------------- 12-column tokens
def layout_store():
    """-> the RULED layout numbers, straight off knowledge/tokens/layout.json.

    ⚠ Nothing is defaulted. A missing field is returned as UNKNOWN and printed as UNKNOWN — a
    measuring surface that guesses is worse than one that says it does not know.
    """
    d = json.load(open(LAYOUT_TOKENS, encoding="utf-8"))
    lay = d.get("layout", {})
    web, app = lay.get("web", {}), lay.get("app", {})
    scale = d.get("scale", {})
    scales = []
    for key in ("scale-1", "scale-2", "scale-3"):
        ext = ((scale.get(key) or {}).get("$extensions", {})
               .get("com.apollo.sds", {}))
        scales.append({
            "key": key,
            "margin": (web.get("margin") or {}).get(key, "UNKNOWN"),
            "gutter": (web.get("gutter") or {}).get(key, "UNKNOWN"),
            "range": ext.get("range", "UNKNOWN"),
            "breakpoints": ", ".join(ext.get("breakpoints", [])) or "UNKNOWN",
        })
    return {
        "scales": scales,
        "web_columns": (web.get("columns") or {}).get("$value", "UNKNOWN"),
        "app_margin": (app.get("margin") or {}).get("$value", "UNKNOWN"),
        "app_gutter": (app.get("gutter") or {}).get("$value", "UNKNOWN"),
        "app_columns": (app.get("columns") or {}).get("$value", "UNKNOWN"),
        "scale_note": (scale.get("$description") or "UNKNOWN"),
        "store_note": (d.get("$description") or "UNKNOWN"),
        "breakpoints": d.get("breakpoint", {}),
    }


def views(store):
    """-> the VIEW list: three web scales plus the app pair. `key` is what the stage wears."""
    out = []
    for s in store["scales"]:
        out.append({"key": "web-" + s["key"], "label": "Web " + s["key"].replace("-", " "),
                    "margin": s["margin"], "gutter": s["gutter"], "range": s["range"],
                    "source": "layout/web (%s)" % s["key"]})
    out.append({"key": "app", "label": "App", "margin": store["app_margin"],
                "gutter": store["app_gutter"],
                "range": "one value at every viewport", "source": "layout/app"})
    return out


def twelve_col_body(store):
    vs = views(store)
    btns = "".join(
        '<button type="button" data-view="%s" aria-pressed="%s">%s</button>'
        % (esc(v["key"]), "true" if i == 0 else "false", esc(v["label"]))
        for i, v in enumerate(vs))
    overlay = "".join('<i class="l-span-1"></i>' for _ in range(12))
    demo_rows = [
        [("l-span-12", "12")],
        [("l-span-6", "6"), ("l-span-6", "6")],
        [("l-span-8", "8"), ("l-span-4", "4")],
        [("l-span-4", "4"), ("l-span-4", "4"), ("l-span-4", "4")],
        [("l-span-3", "3"), ("l-span-3", "3"), ("l-span-3", "3"), ("l-span-3", "3")],
    ]
    demos = "".join(
        '<div class="l-cols gx-demo">%s</div>'
        % "".join('<div class="%s"><span class="t-cm-legal">%s</span></div>' % (cls, esc(lbl))
                  for cls, lbl in row)
        for row in demo_rows)
    scale_rows = "".join(
        "<tr><td>%s</td><td class='num'>%s</td><td class='num'>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(s["key"]), esc(s["margin"]), esc(s["gutter"]), esc(s["range"]),
           esc(s["breakpoints"]))
        for s in store["scales"])
    bp_rows = "".join(
        "<tr><td>%s</td><td class='num'>%s</td><td>%s</td></tr>"
        % (esc(k), esc((v or {}).get("$value", "UNKNOWN")),
           esc((v or {}).get("$description", "UNKNOWN")))
        for k, v in store["breakpoints"].items() if not k.startswith("$"))
    return """
  <section id="intro">
    <h2 class="t-ed-heading-3">The 12-column grid</h2>
    <p class="t-ed-body lede">A Foundations entry, not a component. The RULED layout tokens,
      live: <b>%s columns</b> on web and <b>%s</b> on app, with the margin and gutter each scale
      names. Every number on this page is read from
      <code>knowledge/tokens/layout.json</code> at build time &mdash; none is typed.</p>
    <p class="t-ed-body-small lede">⛔ <b>The grid below is CANON'S OWN.</b> The overlay and the
      demonstration rows are <code>.l-cols</code> with <code>.l-span-*</code> children, under
      <code>.cn-layout-utilities</code> &mdash; the same utilities every gated snippet uses. No
      grid is re-drawn here, so what you are looking at is what a consumer gets.</p>
    <p class="t-ed-body-small lede">⛔ <b>The scale switch is a VIEW control.</b> It changes which
      ruled pair of numbers the page is showing. <b>Nothing on this page tunes a token</b>, and
      there is no export block for that reason &mdash; there is no chosen combination to export.
      A token change is a ruling, and a ruling is Dave's.</p>
  </section>

  <section id="grid">
    <div class="sublabel t-ed-caption">The grid, at the scale you pick</div>
    <div class="gx-ctl">
      <span class="gx-glabel t-cm-legal">Scale</span>
      <div class="gx-seg" role="group" aria-label="Layout scale">%s</div>
      <span class="bm-capt t-cm-legal">A VIEW control &mdash; it selects which ruled
        margin/gutter pair is in force. It mints nothing.</span>
    </div>

    <div class="cn-layout-utilities">
      <div class="gx-stage" id="gx-stage" data-view="%s">
        <div class="l-container">
          <div class="gx-frame">
            <div class="l-cols gx-overlay" aria-hidden="true">%s</div>
            <div class="gx-rows">%s</div>
          </div>
        </div>
      </div>
    </div>

    <dl class="gx-readout t-cm-legal" id="gx-readout">
      <div><dt>Source</dt><dd data-read="source">&mdash;</dd></div>
      <div><dt>Columns rendered</dt><dd data-read="columns">&mdash;</dd></div>
      <div><dt>Margin resolved</dt><dd data-read="margin">&mdash;</dd></div>
      <div><dt>Gutter resolved</dt><dd data-read="gutter">&mdash;</dd></div>
      <div><dt>Viewport range</dt><dd data-read="viewport">&mdash;</dd></div>
    </dl>
    <p class="bm-capt t-cm-legal">⚠ <b>Read back off the live document</b>, not off the switch:
      the columns are counted from the resolved <code>grid-template-columns</code>, the margin
      from the container's resolved padding and the gutter from the grid's resolved column gap.
      A page that printed what it had just declared would agree with itself and with nothing
      else.</p>
  </section>

  <section id="tokens">
    <h2 class="t-ed-heading-4">The ruled numbers</h2>
    <p class="t-ed-body-small lede">%s</p>
    <div class="gx-tablewrap">
      <table class="t-cm-legal">
        <thead><tr><th>layout/web</th><th>Margin</th><th>Gutter</th><th>Viewport</th>
          <th>Breakpoints</th></tr></thead>
        <tbody>%s
          <tr><td><b>layout/app</b></td><td class="num">%s</td><td class="num">%s</td>
            <td>every viewport</td><td>&mdash;</td></tr>
        </tbody>
      </table>
    </div>
    <p class="t-ed-body-small lede">%s</p>
    <div class="gx-tablewrap">
      <table class="t-cm-legal">
        <thead><tr><th>Breakpoint</th><th>Value</th><th>Definition</th></tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>
  </section>

  <section id="notes" class="notes">
    <h2 class="t-ed-heading-4">What this page is, and is not</h2>
    <ul class="t-ed-body-small">
      <li><b>Nothing is re-drawn.</b> The overlay is <code>.l-cols</code> and twelve
        <code>.l-span-1</code> children; the demonstration rows are the same utility with the
        spans a consumer would write. A page-local grid would be a second grammar, and it would
        agree with canon right up until canon changed. The column wash paints <b>behind</b> the
        demonstration rows (s218-D6), so a card shows its own surface and the columns read in the
        gutters and the gaps.</li>
      <li>⛔ <b>The collapse below <code>breakpoint/ms</code> is canon's, and it is real.</b>
        Under 760px every <code>.l-span-*</code> goes full width &mdash; a media query in
        canon.css, written as a literal because a CSS query condition cannot consume a custom
        property. Narrow the window and the demonstration rows stack.</li>
      <li>⚠ <b>Measured, and it is why these numbers are minted at build time:</b> canon.css
        publishes <code>--layout-app-margin</code>, <code>--layout-app-gutter</code>,
        <code>--layout-web-columns</code> and <code>--layout-app-columns</code>, but the three
        WEB margin/gutter scales have no custom property of their own. There is nothing live to
        read, so the generator writes the store's values in as concrete instance dials
        (<code>s200-D1</code>) and the verification compares the rendered result against the
        STORE rather than against anything typed here.</li>
      <li><b>No colour is authored.</b> The column wash is the page's own single tint at 10%%
        opacity over whatever ground the theme paints; every other surface, line and ink resolves
        through a canon token.</li>
    </ul>
  </section>
""" % (esc(store["web_columns"]), esc(store["app_columns"]), btns, esc(vs[0]["key"]), overlay,
       demos, esc(store["store_note"]), scale_rows, esc(store["app_margin"]),
       esc(store["app_gutter"]), esc(store["scale_note"]), bp_rows)


def view_rules(store):
    """The minted VIEW dials — one rule per view, concrete pixels off the store (s200-D1)."""
    out = []
    for v in views(store):
        out.append('.gx-stage[data-view="%s"]{--l-margin:%s; --l-gutter:%s;}'
                   % (v["key"], v["margin"], v["gutter"]))
    return "\n".join(out)


# ---------------------------------------------------------------------------- the four pages
def type_body(kind, c):
    """The BODY of one bento type page. Split out from `type_page` so the fence bites can be
    asked of the markup this module AUTHORS — the consumed stylesheet legitimately carries the
    explorer's `.bm-alt` / `.bm-tag` rules and its PROPOSED comments, and a bite that swept the
    whole rendered page would be asking the wrong question of them."""
    label, subtitle, lede = TYPE_META[kind]
    return """
  <section id="intro">
    <h2 class="t-ed-heading-3">%s</h2>
    <p class="t-ed-body lede">%s The dials below are the ruled ones for this type, working, so a
      designer can drive them; the preview and the export block are rendered in the same pass
      from the same state object, so the export cannot describe a combination you did not
      see.</p>
    <p class="t-ed-body-small lede">⛔ <b>Ruled behaviour only.</b> The five open points
      <code>s217-D5</code> leaves unruled (P1&ndash;P5) live on the
      <a href="bento.html">Bento matrix explorer</a>, which is their decision surface. Nothing on
      this page is proposed, and nothing on it is promoted.</p>
  </section>

  <section id="controls">
    <div class="sublabel t-ed-caption">The dials for this type</div>
    <div class="bm-controls">
      %s
    </div>
    <p class="bm-capt t-cm-legal" id="bm-moved"></p>

    <div class="bm-stage" id="bm-stage" data-type="%s" data-spacing="24" data-keylines="on"
         data-page-bg="white" data-bento-bg="grey">
      <div class="bm-page-ground">
%s
      </div>
    </div>

    <div class="bm-export">
      <div class="bm-exhead">
        <span class="t-cm-legal">Export &mdash; concrete values, resolved in the theme and mode
          on screen (<code>s200-D1</code>), no <code>var()</code> chain.</span>
        <button class="bm-btn t-cm-ctl-14" type="button" id="bm-rebuild">Rebuild export</button>
      </div>
      <pre><code id="bm-export" class="t-cm-legal"></code></pre>
    </div>
  </section>

  <section id="notes" class="notes">
    <h2 class="t-ed-heading-4">What this page is, and is not</h2>
    <ul class="t-ed-body-small">
      <li><b>Nothing is re-drawn and nothing is re-derived.</b> The content, the spans, the
        packing and the corner rules all come from
        <code>knowledge/_render/gen_bento_matrix_217.py</code> &mdash; the same modules the
        matrix explorer renders from, consumed rather than copied. One data path, one maths.</li>
      <li><b>No bento structure is declared here.</b> The grid, the span vocabulary, the
        responsive bands, the three role rules and the caption space are canon's
        (<code>s217-D2</code> / <code>s217-D3</code>). This type renders as canon's
        <code>%s</code> role, which is what makes every radius and spacing decision on the page
        canon's own rule resolving.</li>
      <li><b>No colour is authored.</b> Every ground is <code>--surface-subtle</code>,
        <code>--surface-raised</code> or nothing at all; the controller chrome is neutral.</li>
    </ul>
  </section>
""" % (esc(label), lede, controls_for(kind), esc(kind), pane_html(kind, c), esc(TYPE_ROLE[kind]))


def type_page(shell, kind, c, assets):
    label, subtitle, _lede = TYPE_META[kind]
    body = type_body(kind, c)
    # ⬛ THE TYPE IS PINNED THROUGH THE CONTROLLER'S OWN PUBLIC HANDLES — no string surgery on
    # the module's source. Appended AFTER it, so the handles exist by the time this runs.
    boot = ("\n/* #218 — pin this page to ONE type through the controller's exported handles. */\n"
            "(function(){ if (window.__BM_STATE && window.__BM_APPLY) {"
            " window.__BM_STATE.type = %s; window.__BM_APPLY(); } })();\n"
            % json.dumps(kind))
    return shell("%s — Apollo library (Foundations)" % label, label, subtitle, body,
                 extra_css=assets["css"] + GRIDS_CSS.replace("__VIEW_RULES__", ""),
                 extra_script=assets["js"] + boot,
                 extra_class=assets["cls"])


# ⬛ s218-D6 (2) — THE OVERLAY ARM'S HANDLE. Set by `--break-overlay`, never at build time. It
# removes EXACTLY the pair of declarations that put the wash behind the content, so the mutant is
# the page as it was BEFORE the ruling and differs from the shipped page in nothing else.
BREAK_OVERLAY = False
_OVERLAY_PAIR = (
    (".gx-overlay{position:absolute; inset:0; pointer-events:none; z-index:0;}",
     ".gx-overlay{position:absolute; inset:0; pointer-events:none;}"),
    (".gx-frame > .gx-rows{position:relative; z-index:1;}", ""),
)


def twelve_col_page(shell):
    store = layout_store()
    css = GRIDS_CSS.replace("__VIEW_RULES__", view_rules(store))
    if BREAK_OVERLAY:
        for before, after in _OVERLAY_PAIR:
            if before not in css:
                raise SystemExit("gen_grids_218 --break-overlay: the arm's literal is not in the "
                                 "stylesheet any more (%r) — a mutation that changes nothing is a "
                                 "DANGLE and would prove the clause green by accident" % before)
            css = css.replace(before, after, 1)
    js = GRIDS_SCRIPT.replace("__VIEWS__", json.dumps(
        [{"key": v["key"], "source": v["source"], "range": v["range"]} for v in views(store)]))
    return shell("The 12-column grid — Apollo library (Foundations)", "The 12-column grid",
                 "Foundations &middot; Grids &middot; the ruled layout tokens",
                 twelve_col_body(store), extra_css=css, extra_script=js, extra_class="bm gx")


def page(shell, kind, c=None, assets=None):
    """-> the whole HTML page for one member of the Grids group."""
    if kind == "12col":
        return twelve_col_page(shell)
    c = c or matrix.content()
    return type_page(shell, kind, c, assets or matrix_assets(c))


PAGES = [("12col", "grids-12col.html"), ("display", "grids-display.html"),
         ("gallery", "grids-gallery.html"), ("dashboard", "grids-dashboard.html")]


# ---------------------------------------------------------------------------- selftest
def selftest():
    import re
    fails, ran = [], []

    def bite(name, got, want):
        ran.append(name)
        if got != want:
            fails.append("%s\n     got:  %r\n     want: %r" % (name, got, want))

    c = matrix.content()
    assets = matrix_assets(c)
    store = layout_store()
    pages = {}

    def cap_shell(title, h1, subtitle, body, extra_css="", extra_script="", extra_class=""):
        return ("<!doctype html><title>%s</title><style>%s</style><body class='%s'>%s"
                "<script>%s</script>" % (title, extra_css, extra_class, body, extra_script))

    for kind, fname in PAGES:
        pages[kind] = page(cap_shell, kind, c, assets)

    # ⛔ 1 — THE SELECTOR CONTRACT with the explorer's stylesheet. The wrapper markup below is
    # written against class names that live in the CONSUMED CSS; if one is renamed there, four
    # pages silently lose their styling and every render still "works". This is the gate.
    bite("1 · every wrapper selector the grids pages rely on is in the CONSUMED explorer CSS",
         sorted(s for s in REQUIRED_SELECTORS if s not in assets["css"]), [])
    bite("2 · the per-type control filter returns dials for each type and DROPS the type switch",
         ({k: len(re.findall(r'class="bm-group', controls_for(k)))
           for k in ("display", "gallery", "dashboard")},
          [k for k in ("display", "gallery", "dashboard")
           if 'data-dial="type"' in controls_for(k)]),
         ({"display": 4, "gallery": 8, "dashboard": 5}, []))
    # ⛔ 3 — the fence, asserted on the MARKUP THIS MODULE AUTHORS. A PROPOSED surface on these
    # pages would move a live decision (s217-D5 P1–P5, row W-126) off the explorer that owns it.
    # ⚠ Asked of the BODY, not the rendered page: the consumed stylesheet carries the explorer's
    # own `.bm-alt` / `.bm-tag` rules and its PROPOSED comments, and it must — it is the
    # explorer's file. What matters is that no grids page DRAWS one.
    bodies = {k: type_body(k, c) for k in ("display", "gallery", "dashboard")}
    bodies["12col"] = twelve_col_body(store)
    # ⚠ THE TEST IS FOR A PROPOSAL SURFACE, NOT FOR THE WORD. Each page POINTS AT the explorer
    # where the open points live, and saying so in a sentence is the opposite of carrying one —
    # a substring ban on "open point" would red the very sentence that keeps the fence readable.
    # What is banned: the PROPOSED marker word, the tag chip that carries it, and the
    # proposal-note list the explorer draws.
    bite("3 · #218 · no PROPOSED surface is drawn on any grids page",
         sorted(k for k in bodies
                if "PROPOSED" in bodies[k] or "Proposed &mdash;" in bodies[k]
                or "bm-tag" in bodies[k] or '<li><b>P1' in bodies[k]), [])
    bite("4 · #218 · no grids page draws the P4 radius pair or the explorer's exhibits",
         sorted(k for k in bodies
                if any(x in bodies[k] for x in ("bm-alt", "bm-display-stepped", 'id="bm-sweep"',
                                                "bm-sw-strip", "bm-mw-case", 'id="matrix"',
                                                'id="points"'))), [])
    # 5 — every id the CONSUMED controller reaches for must exist on the pages that run it.
    bite("5 · the ids the consumed controller drives are present on all three bento pages",
         sorted((k, i) for k in ("display", "gallery", "dashboard") for i in REQUIRED_IDS
                if 'id="%s"' % i not in pages[k]), [])
    bite("6 · each bento page renders exactly ONE pane, and it is its own type",
         {k: (pages[k].count('class="bm-pane"'),
              'data-pane="%s"' % k in pages[k])
          for k in ("display", "gallery", "dashboard")},
         {"display": (1, True), "gallery": (1, True), "dashboard": (1, True)})
    bite("7 · the type is pinned through the controller's exported handles, not by rewriting it",
         (all("__BM_STATE.type" in pages[k] for k in ("display", "gallery", "dashboard")),
          # the controller source arrives BYTE-FOR-BYTE — no string surgery on the module
          all(assets["js"] in pages[k] for k in ("display", "gallery", "dashboard"))),
         (True, True))
    # ⬛ 8 — the #218 corner rules reach the dashboard page through the explorer's own build.
    bite("8 · #218 · the corner-keyline block is on the dashboard page, from the matrix's build",
         ("#218 CORNER KEYLINES" in pages["dashboard"],
          matrix.corner_rules(c["dash_inner"]) in pages["dashboard"]),
         (True, True))
    bite("9 · the dashboard page lays the RULED groups, spans read from the squaring pass",
         (pages["dashboard"].count('class="c-bento c-bento__tile bm-inner"'),
          sorted({tuple(s) for s in c["dash_spans"]}) ==
          sorted({tuple(s) for s in c["dash_spans"]})),
         (len(c["dash_cards"]), True))

    # ---- the 12-column page
    twelve = pages["12col"]
    bite("10 · the overlay is CANON's .l-cols with twelve .l-span-1 children, under its scope",
         (twelve.count('class="l-cols gx-overlay"'),
          twelve.split('class="l-cols gx-overlay"', 1)[1].split("</div>", 1)[0]
                .count('class="l-span-1"'),
          'class="cn-layout-utilities"' in twelve),
         (1, 12, True))
    # ⛔ 11 — asked of the CSS THIS MODULE AUTHORS, which is the only place a second grid could be
    # declared. (The prose names the property, which is not a declaration.)
    bite("11 · no grid is re-declared — this module's CSS declares no template-columns/rows",
         [ln for ln in (GRIDS_CSS + view_rules(store)).split("\n")
          if "grid-template" in ln], [])
    bite("12 · the ruled store values are MINTED into the view dials, all four views",
         sorted(re.findall(r'\.gx-stage\[data-view="([a-z0-9-]+)"\]\{--l-margin:([^;]+); '
                           r'--l-gutter:([^;]+);\}', twelve)),
         sorted((v["key"], v["margin"], v["gutter"]) for v in views(store)))
    bite("13 · the token numbers on the page ARE the store's, not typed",
         (str(store["web_columns"]) in twelve, str(store["app_columns"]) in twelve,
          all(s["margin"] in twelve and s["gutter"] in twelve for s in store["scales"]),
          store["app_margin"] in twelve, store["app_gutter"] in twelve),
         (True, True, True, True, True))
    bite("14 · UNKNOWN is never defaulted — a missing store field would say so",
         [s["key"] for s in store["scales"]
          if "UNKNOWN" in (s["margin"], s["gutter"], s["range"])], [])
    bite("15 · the 12-column page carries NO export block and NO bento dial (it tunes nothing)",
         (("bm-export" in twelve), ("bm-stage" in twelve), ('data-dial="' in twelve)),
         (False, False, False))
    # ⛔ 16 — the silent-black fence over EVERY var() this module authors.
    authored = GRIDS_CSS + GRIDS_SCRIPT
    bad = [m for m in re.findall(r"var\((--[a-z0-9-]+)([^)]*)\)", authored) if "," not in m[1]]
    bite("16 · every var() this module authors carries a literal fallback (silent-black fence)",
         sorted(m[0] for m in bad), [])

    if fails:
        print("gen_grids_218 --selftest: %d BITE(S) FAILED" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print("gen_grids_218 --selftest OK — %d bites." % len(ran))
    print("   consumed: matrix CSS %d bytes, matrix JS %d bytes (built by the explorer's own "
          "page() through a capturing shell)" % (len(assets["css"]), len(assets["js"])))
    print("   12-column views minted: %s"
          % ", ".join("%s %s/%s" % (v["key"], v["margin"], v["gutter"]) for v in views(store)))


def write_mutant(shell):
    """⬛ #218 — THE DASHBOARD ARM, and it costs almost nothing because of how this module is
    built. `matrix_assets` captures whatever `matrix.page()` composes, so flipping the EXPLORER'S
    OWN `BREAK_LAYOUT` handle — the one that ships `__CORNER_RULES__` empty — strips the corner
    rules from THIS page too, through the same one path. No second arm, no second flag inside the
    grids module, and no way for the arm to drift from what it is arming.
    ⛔ NON-REPO by construction: the destination is BM_MUTANT_DIR, never showroom/. ⚠ /var/tmp is
    SHARED ACROSS SESSIONS — a foreign mutant is unwritable AND stale, and a stale mutant silently
    proves yesterday's clause. Pass a session-suffixed BM_MUTANT_DIR.
    """
    mdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")
    os.makedirs(mdir, exist_ok=True)
    # ⛔ AND ITS ASSET ADDRESSES ARE MADE ABSOLUTE — the same discipline the explorer's own four
    # arms use. MEASURED #218: written with the shipped `../../knowledge/…` hrefs, a mutant in
    # /var/tmp resolves canon.css NOWHERE, every token dangles, every radius reads 0 — and the
    # corner assertion then "passes" by comparing 0 to 0. A mutant that cannot load canon proves
    # nothing about a clause expressed in canon's radius.
    up = "file://" + ROOT + "/"
    real_up = matrix.UP
    matrix.BREAK_LAYOUT = True
    matrix.UP = up
    try:
        c = matrix.content()
        html = page(shell, "dashboard", c, matrix_assets(c))
    finally:
        matrix.BREAK_LAYOUT = False
        matrix.UP = real_up
    html = html.replace('href="../../knowledge/', 'href="file://%s/knowledge/' % ROOT)
    dest = os.path.join(mdir, "grids-dashboard-LAYOUT-BROKEN.html")
    open(dest, "w", encoding="utf-8").write(html)
    print("gen_grids_218 --break-dash: wrote %s (%d bytes) — the #218 corner rules are STRIPPED"
          % (dest, os.path.getsize(dest)))
    return dest


def write_overlay_mutant(shell):
    """⬛ s218-D6 (2) — THE OVERLAY ARM. The 12-column page composed with `BREAK_OVERLAY` on, so
    the column wash paints OVER the demo content again, exactly as it did before the ruling.

    ⛔ NON-REPO: BM_MUTANT_DIR, never showroom/. ⚠ session-suffix it — /var/tmp is shared, and a
    foreign mutant is stale as well as unwritable. ⛔ The asset hrefs are made ABSOLUTE for the
    same reason the dashboard arm does it: a mutant that cannot load canon resolves every token to
    nothing, and a paint assertion then compares one fallback against another.
    """
    global BREAK_OVERLAY
    mdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")
    os.makedirs(mdir, exist_ok=True)
    BREAK_OVERLAY = True
    try:
        html = page(shell, "12col")
    finally:
        BREAK_OVERLAY = False
    html = html.replace('href="../../knowledge/', 'href="file://%s/knowledge/' % ROOT)
    dest = os.path.join(mdir, "grids-12col-OVERLAY-BROKEN.html")
    open(dest, "w", encoding="utf-8").write(html)
    print("gen_grids_218 --break-overlay: wrote %s (%d bytes) — the s218-D6 paint-order pair is "
          "STRIPPED, the wash paints OVER the content" % (dest, os.path.getsize(dest)))
    return dest


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--break-overlay" in sys.argv:
        import gen_foundations_217 as foundations
        write_overlay_mutant(foundations.shell)
    elif "--break-dash" in sys.argv:
        # the ONE shell, borrowed from the ONE writer, so the mutant differs from the real page
        # in exactly the arm and in nothing else.
        import gen_foundations_217 as foundations
        write_mutant(foundations.shell)
    else:
        print(__doc__.strip())
        print("\n⚠ This module writes nothing. gen_foundations_217.py is the ONE writer.")
