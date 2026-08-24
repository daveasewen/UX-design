#!/usr/bin/env python3
"""
gen_bento_matrix_217.py — THE BENTO MATRIX EXPLORER, the page body for the Foundations entry
`showroom/_foundations/bento.html`.

WHY IT EXISTS — `s217-D5` (#217, Dave, 2026-08-23), verbatim from the ruling:
  "The bento system lives in the showroom's Foundations/Layout section as a MATRIX of options
   over three TYPES … DISPLAY … GALLERY … DASHBOARD."
Dave's closing words on the same message: "lets see this for now. this is a lot, you might want
to check my logic". So this page is an INSTRUMENT for his eye, not a promotion: it renders the
ruled option matrix live, over real content, in four themes × light/dark, and exports the chosen
combination as CONCRETE VALUES for a future ruling.

⛔ WHO WRITES THE FILE. Not this module. `knowledge/_render/gen_foundations_217.py` is the ONE
writer of `showroom/_foundations/*.html` and the ONE place the page shell lives; it imports
`page(shell, …)` from here and hands its own shell in. Keeping the matrix in its own module keeps
the foundations generator readable; keeping the WRITE there keeps one writer and one shell.

⛔ ONE DATA PATH. The photographs come from `gen_bento_roles_217.read_photos()` — the same
function `gen_gallery_compare_217` consumes — and the cards and panels are that module's `CARDS`
and `PANELS`. The justified-rows arithmetic is `gen_gallery_compare_217.pack_rows`, imported, not
re-derived. Nothing about the content or the packing is typed here.

⛔ TYPES ARE CANON'S ROLES. `s217-D5` renames `s217-D3`'s roles to TYPES and renames brochureware
to DISPLAY. The rename is a WORD, not a second grammar: Display renders as `data-bento-role=
"brochureware"`, Gallery as `"gallery"`, Dashboard as `"dashboard"`, so every radius/spacing/
squaring decision on this page is canon's own rule resolving, never a page-local re-statement.
The type→role map is the ONE place the rename is expressed (`TYPE_ROLE` below).

⬛ WHAT IS RULED AND WHAT IS PROPOSED, AND THE PAGE SAYS SO ON ITS FACE.
RULED by `s217-D5`: the three types; the spacing sets (1/24/40, dashboard main NEVER tight); the
keylines toggle; the gallery mode pair and its ragged/square sub-option; the two console image-
rounding options; the grey / white / transparent background palette for page, bento and caption;
and the caption inversion constraint. PROPOSED-NOT-RULED, each labelled `PROPOSED` on the page and
each the conductor's reading of one of the ruling's five OPEN POINTS:
  P1  tight + keylines ON  = flush tiles with hairline separators (the inset-group pattern),
      because 1px cannot hold a gap AND a line. Tight + keylines OFF = the 1px show-through.
  P2  a caption colour is judged against its IMMEDIATE ground (the bento background behind the
      tile). Same-on-same is refused; transparent is always legal.
  P3  the full capsule requires a caption background OR keylines — otherwise the capsule has no
      edge to be a capsule of.
  P4  at Display tight the standard tile radius may pinch, so the standard radius and a
      stepped-down concentric alternative are drawn SIDE BY SIDE at that spacing only.
  P5  the grey/white/transparent palette is applied to all three types' selectors.

⬛ THE KEYLINE CONSTRUCTION FOR DASHBOARDS — `s217-D8` (#217, Dave, 2026-08-24), RULED:
"the keylines should stay, but they should go round tight to the modules not run down the middle
of the spacing". What the dashboard pane draws, at every stop of the s217-D6 slider:
  · ABOVE 1px — every TILE wears its own tight 1px keyline box; the GROUP'S OUTER BORDER STEPS
    BACK (tiles carrying edges plus a group frame is the DOUBLE FRAME Dave rejected earlier in the
    same session); the group is still expressed by its background and its clipped radius; the
    tiles are inset from the container by the gutter, so no straight edge arrives at the curve.
    NO LINE IN ANY GUTTER, inner or outer — no element and no paint.
  · AT 1px — unchanged: the rounded group border with flush tiles, the gutter itself the hairline,
    stopped along the curve by the container's own `overflow:hidden`. The ONLY stop on the pane
    where a line element renders at all.
⛔ WHAT WAS RETIRED WITH THE RULING, AND WHY IT IS NOT JUST RE-CAPTIONED:
  · THE A/B/C DECISION SPREAD (`spread_html`, `SPREAD`) — three treatments of the double frame at
    identical settings. It existed to get ONE question answered by Dave's eye, and the answer is
    `s217-D8`. A decision surface for a settled question keeps a retired construction on the page
    and invites the question to be re-opened. Replaced by a compact ruled-behaviour NOTE, keyed to
    the same two dials the spread was (`.bm-sp-strip`, `.bm-sp-open`, `.bm-sp-note`).
  · THE SWEEP'S 1px CONTROL ROW (`sweep_reference_html`) — it drew the pre-C flush construction
    beside C at the same stop so the CONVERGENCE of the two could be differenced. With C retired
    there is nothing to converge; the 1px row of the strip IS the flush construction now.
  · THE MAIN-WALL COUNTER-EXAMPLE (`mainwall_html(True)`) — it drew a hairline down the middle of
    the main wall's gutter, which is the retired construction. The inside-only PROPOSAL stays.
⬛ WHAT SURVIVED, AND WHY: the SWEEP (`sweep_html`) — one group per ruled stop, labelled, full
width, stacked (ds-054). Dave's question "what happens with sub-bento spacing?" was asked of C, but
the RHYTHM story it answers is a property of the ladder, not of the construction. The strip now
draws the ruled construction at every stop, with the 1px row showing the flush regime.

⛔ NO STATE THAT RENDERS NOTHING. Every reachable combination draws something. Where a ruling
makes a combination illegal the control is visibly disabled WITH ITS REASON (P2, P3); where the
ruling removes an option entirely it is ABSENT, not disabled — dashboard main spacing has no
tight button at all, because tight is ruled out rather than temporarily unavailable, and the
gallery bottom-edge dial exists only under Gallery-bento.

ONE STATE OBJECT, TWO CONSUMERS (s200-D1, the tuner's discipline). `STATE` drives the preview and
the export in the same `apply()` pass. The export carries the dial values AND the values RESOLVED
out of the live document in the current theme × mode — concrete pixels and concrete colours, no
`var()` chain — so it can be read as a proposal without the reader having to resolve anything.

⛔ NO VAR MAY DANGLE. Every `var()` this page authors carries a literal fallback; an unresolved
custom property renders SILENT BLACK and no gate catches it
([[dangling-dataviz-var-renders-silent-black]]).

COLOUR. No hue is authored. Every surface, ink, line and radius resolves through a canon token,
so all four themes and both modes are canon.css's own cascade. The controller chrome is NEUTRAL
only — no red, no yellow, no green — because those hues are unstable for Dave.

Usage:
  python3 knowledge/_render/gen_bento_matrix_217.py --selftest
  python3 knowledge/_render/gen_bento_matrix_217.py --break-legality [--out /var/tmp]
  python3 knowledge/_render/gen_bento_matrix_217.py --break-keylines [--out /var/tmp]
      ⬛ the s217-D8 MUTATION handle: writes a NON-REPO copy whose dashboard wall draws the
      RETIRED centred-gutter keyline at the open stops, so the ruled assertions can be seen to
      go RED by name.
      ⬛ the MUTATION handle: writes a NON-REPO copy of the page whose legality function always
      returns "legal", so the probe's refusal assertions can be seen to go RED by name. It never
      writes over the real page and never writes inside the repo.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import html as htmlmod
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
sys.path.insert(0, os.path.join(KNOW, "canon"))
sys.path.insert(0, HERE)
from gen_canon_bento import (params, band_ladder, square_wall,  # noqa: E402
                             square_wall_for_role, square_inner_wall, square_nested_wall,
                             is_rectangular, inner_ladder, caption_space, roles)
from gen_bento_roles_217 import read_photos, CARDS, PANELS      # noqa: E402  ONE DATA PATH
from gen_gallery_compare_217 import pack_rows                   # noqa: E402  ONE PACKING MATHS

UP = "../../"

# ⬛ THE MUTATION HANDLES — see the module docstring. Never true for the shipped page.
BREAK_LEGALITY = False
# ⬛ s217-D6 SECOND ARM: puts BOTH of Dave's #217 defects back, so the assertions written against
# them can be seen to go RED by name. `--break-layout` restores (a) the side-by-side P4 pair,
# which halves each wall's container and trips the responsive bands, and (b) the literal
# one-column dashboard span, which skips the ruled squaring pass and leaves an orphan cell.
BREAK_LAYOUT = False
# ⬛ s217-D7 THIRD ARM: disables the NESTED squaring pass only, so every inner wall on the page
# falls back to its authored spans and the inner-group assertions can be seen to go red BY NAME —
# separately from the outer-wall arm above, which would otherwise mask them.
BREAK_INNER = False
# ⬛ THE FOURTH ARM — `--break-keylines` (s217-D8). It puts the RETIRED CENTRED-GUTTER LINE back on
# the live dashboard wall at the open stops: the tiles go bare, the group takes its border again
# and the hairline pair renders centred in every gutter. That is the exact construction Dave
# rejected ("running down the middle of the of the spacing"), so the s217-D8 assertions — tile
# border box, group border 0, zero line nodes and zero line PAINT in the gutters — must go red BY
# NAME. A gate that has never been seen to fail is not a gate ([[instrument-without-a-consumer]]).
BREAK_KEYLINES = False

# s217-D5 renames s217-D3's roles to TYPES; brochureware becomes DISPLAY. THE ONE PLACE the
# rename is expressed. Everything downstream asks canon for the role's behaviour.
TYPE_ROLE = {"display": "brochureware", "gallery": "gallery", "dashboard": "dashboard"}

# The RULED option sets. Every list here is a quotation of s217-D5, not a preference.
SPACINGS = [("1", "Tight", "1px"), ("24", "Standard", "24px"), ("40", "Generous", "40px")]
# ⛔ DASHBOARD MAIN SPACING HAS NO TIGHT MEMBER — "NEVER tight" is ruled, so the button is ABSENT
# rather than disabled. A disabled control reads as "not right now"; this is "not ever".
DASH_MAIN = [s for s in SPACINGS if s[0] != "1"]
BACKGROUNDS = [("grey", "Lightest grey", "--surface-subtle"),
               ("white", "White", "--surface-raised"),
               ("transparent", "Transparent", "(none)")]
GALLERY_MODES = [("justified", "Justified rows"), ("bento", "Gallery bento")]
BOTTOM_EDGE = [("ragged", "Ragged"), ("square", "Square")]
ROUNDINGS = [("corners", "4 corners of the image"), ("capsule", "Full capsule")]
ONOFF = [("on", "On"), ("off", "Off")]

# ⬛ s217-D6 (#217, Dave, 2026-08-23) — DASHBOARD SUB-BENTO SPACING IS A SNAPPING SLIDER. The
# ladder is Dave's, verbatim: "a slider that snaps to 1,2,4,8,12, 16, 20, 24". It REPLACES the
# three-stop control, so 40px is no longer reachable on a sub-bento.
# ⛔ THE STOPS ARE THE WHOLE VOCABULARY. The slider is driven in PIXELS and snapped to the nearest
# stop before anything downstream sees it, so an off-snap number cannot exist in the state object,
# in the CSS (eight declared rules, one per stop — never a style="" attribute), or in the export.
SUB_STOPS = [1, 2, 4, 8, 12, 16, 20, 24]

# ⬛ s217-D6 — THE GALLERY TYPE IN THE CONSOLE THEME EXCLUDES KEYLINES COMPLETELY. Dave:
# "gallery-console should exclude keylines completely". ABSENT, not disabled — the same discipline
# the dashboard's missing Tight button already carries: a disabled control reads "not right now",
# and this is "not ever, here". The control node LEAVES THE DOCUMENT in that theme.
# ⚠ THE CONSEQUENCE THE PAGE MUST OWN: the reachable count is now THEME-DEPENDENT, so a single
# total on the page would be a lie in one theme out of four. Counted per theme below.
KEYLINE_EXCLUDED = [("gallery", "console")]
THEMES = ["mono", "legacy", "console", "supercharge"]


def keylines_for(type_, theme):
    """-> the keyline values REACHABLE for this type in this theme (s217-D6). Where the control is
    excluded the wall draws none, so the single reachable value is 'off' — not zero values, which
    would make the type unreachable rather than keyline-free."""
    if (type_, theme) in KEYLINE_EXCLUDED:
        return ["off"]
    return [o[0] for o in ONOFF]


def snap(px):
    """-> the ruled stop nearest `px` (s217-D6). THE ONE SNAP, mirrored into the page's JS.
    ⚠ TIES GO TO THE LOWER STOP, DECLARED rather than incidental: 6 lands on 4, 10 on 8, 14 on 12,
    22 on 20. A tie-break that is merely whatever `min` happened to do is a rule nobody can
    hand-compute against, and the selftest hand-computes against this sentence."""
    return min(SUB_STOPS, key=lambda s: (abs(s - float(px)), s))

# Instance dials for the walls on this page — a preview pane, not a full-bleed wall.
GALLERY_COLS, DISPLAY_COLS, DASH_COLS, INNER_COLS = 4, 4, 2, 3

# ✅ s217-D7 — EVERY INNER WALL ON THIS PAGE MINTS ITS SPANS HERE, and there is no other way to
# get one: `card_tile()` now REQUIRES a span and no longer reads the authored literal off the card.
# ⛔ THE DEFECT CLASS THIS CLOSES: the outer dashboard wall was fixed at the ratification and the
# INNER walls kept their authored spans, so a group of (2x1, 1x1, 1x1) in three tracks left two
# empty cells — a visible orphan, and under treatment C a hairline running into blank space.
# Four walls on this page are nested dashboards (the live wall, the keyline spread, the spacing
# sweep and the main-wall question) and every one of them went through the authored literal.
INNER_SQUARE_REPORTS = []


def inner_wall(spans, cols=INNER_COLS, role=None, label=""):
    """-> the spans for ONE nested wall, run through canon's ratified pass at the INNER ladder.
    A refusal is kept, named and printed rather than silently shipped as squared."""
    spans = [(min(int(c), cols), int(r)) for (c, r) in spans]
    if BREAK_INNER:
        return spans                       # ⬛ ARM: the authored literal, exactly as the defect had it
    out, rep = square_inner_wall(spans, role or TYPE_ROLE["dashboard"], cols=cols)
    rep["wall"] = label
    INNER_SQUARE_REPORTS.append(rep)
    if not (rep.get("squared") and not rep.get("exempt")):
        return spans                       # REFUSED and said why — never silently squared
    return out


def card_spans(cards, cols=INNER_COLS, label=""):
    """-> minted spans for a group of CARDS, from their authored spans through the pass."""
    return inner_wall([(c, r) for (_l, _s, _f, c, r) in cards], cols=cols, label=label)


def esc(s):
    return htmlmod.escape(str(s if s is not None else ""), quote=True)


# --------------------------------------------------------------- ⬛ #218 CORNER KEYLINES
# Dave, #218: "each tile must have it's own keyline, but the radii should only apply to the
# 4 corners of each sub bento (a collection of tiles)". The corner a tile holds depends on the
# band's column count, so the assignment is computed from the browser's own dense placement —
# tile identity kept — and emitted per band. Never read off data-c: the bands rewrite spans.

# (cols, max-width literal) — the literals mirror canon's compiled $bands (a @container
# condition cannot read a custom property; same reason canon compiles them). None = base.
CORNER_BANDS = ((INNER_COLS, None), (2, 820), (1, 520))


def _band_clamp(spans, cols):
    """Canon's band clamp: spans capped at the band's columns; the 1-column band flattens BOTH
    axes (canon's 520 rule rewrites data-r to span 1 as well)."""
    if cols == 1:
        return [(1, 1)] * len(spans)
    return [(max(1, min(int(c), cols)), max(1, int(r))) for c, r in spans]


def _tile_cells(spans, cols):
    """Dense placement with TILE IDENTITY — the same rows-then-columns scan `place()` runs, but
    recording WHICH tile fills each cell, so a corner is read off the occupancy the browser will
    actually render. `spans` must already be band-clamped."""
    occ = []

    def ensure(r):
        while len(occ) <= r:
            occ.append([None] * cols)

    def fits(r, c, cs, rs):
        for rr in range(r, r + rs):
            ensure(rr)
            for cc in range(c, c + cs):
                if occ[rr][cc] is not None:
                    return False
        return True

    for i, (cs, rs) in enumerate(spans):
        cs, rs = max(1, min(int(cs), cols)), max(1, int(rs))
        r, placed = 0, False
        while not placed:
            ensure(r)
            for c0 in range(0, cols - cs + 1):
                if fits(r, c0, cs, rs):
                    for rr in range(r, r + rs):
                        for cc in range(c0, c0 + cs):
                            occ[rr][cc] = i
                    placed = True
                    break
            r += 1
    while occ and all(x is None for x in occ[-1]):
        occ.pop()
    return occ


_CORNER_KEYS = ("top-left", "top-right", "bottom-right", "bottom-left")


def corner_map(spans, cols):
    """-> {tile_index: set(corner keys)} for one band. A corner cell left empty by a ragged wall
    assigns nothing — honest absence, not a guess (the live groups are squared, so in practice
    all four assign)."""
    occ = _tile_cells(_band_clamp(spans, cols), cols)
    out = {i: set() for i in range(len(spans))}
    if occ:
        last = len(occ) - 1
        for key, (rr, cc) in (("top-left", (0, 0)), ("top-right", (0, cols - 1)),
                              ("bottom-right", (last, cols - 1)), ("bottom-left", (last, 0))):
            if occ[rr][cc] is not None:
                out[occ[rr][cc]].add(key)
    return out


def corner_rules(dash_inner):
    """-> the generated CSS block replacing __CORNER_RULES__. Per group, per band, an EXPLICIT
    all-four-corners declaration for EVERY tile — the group's radius (`--bento-radius`, canon's
    own container token, 20 console / 0 elsewhere) on the outer corner a tile holds, 0 on every
    corner it does not. Explicit everywhere so the band blocks never depend on source order or
    specificity to override one another. Scoped to keylines ON at the OPEN stops on the LIVE
    wall only (`.bm-outer >`): the 1px stop keeps the container-border construction, and the
    sweep/main-wall exhibits keep their own rules."""
    scope = '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"])'
    blocks = ["/* ⬛ #218 CORNER KEYLINES — the four corner tiles of each sub-bento carry the "
              "group's radius on their OUTER corner; minted per band from dense placement. */"]
    for gi, spans in enumerate(dash_inner, 1):
        sel_g = ("%s .bm-outer > .c-bento__grid > .bm-inner:nth-child(%d)" % (scope, gi))
        for cols, band in CORNER_BANDS:
            cm = corner_map(spans, cols)
            rules = []
            for i in range(len(spans)):
                decl = "; ".join(
                    "border-%s-radius:%s" % (k, "var(--bento-radius,0px)" if k in cm[i] else "0")
                    for k in _CORNER_KEYS)
                rules.append("%s > .c-bento__grid > .bm-tile:nth-child(%d){%s;}"
                             % (sel_g, i + 1, decl))
            body = "\n".join(rules)
            blocks.append(body if band is None
                          else "@container bento (max-width:%dpx){\n%s\n}" % (band, body))
    return "\n".join(blocks)


# ---------------------------------------------------------------------------- LEGALITY
# ⛔ THE ONE STATEMENT OF THE RULES, IN PYTHON, MIRRORED INTO THE PAGE'S JS BELOW. The count on
# the page and the refusals in the browser must be the same rules or the page lies about its own
# matrix — so the enumeration below and the JS `legality()` are written from this one comment
# block, and the selftest drives the Python side against hand-computed answers.
#   P2 · a caption background equal to its immediate ground (the bento background) is ILLEGAL,
#        unless it is transparent — transparent has no ground of its own to collide with.
#   P3 · the full capsule needs an edge: a caption background OR keylines.
def caption_legal(cap_bg, bento_bg):
    return not (cap_bg != "transparent" and cap_bg == bento_bg)


def capsule_legal(rounding, cap_bg, keylines):
    return not (rounding == "capsule" and cap_bg == "transparent" and keylines == "off")


def enumerate_matrix(theme="mono"):
    """-> {type: [state dicts]} FOR ONE THEME. EVERY REACHABLE COMBINATION, so the page can report
    a MEASURED dimension count instead of a claimed one. Illegal combinations are excluded here
    exactly as the controls refuse them in the browser.
    ⚠ THEME IS A PARAMETER AND NOT A DEFAULT-AND-FORGET (s217-D6): gallery-in-console has no
    keyline control, so the count genuinely differs by theme. A caller that does not name a theme
    gets `mono` and the page never uses that path without saying which theme it means."""
    bg = [b[0] for b in BACKGROUNDS]
    out = {"display": [], "gallery": [], "dashboard": []}
    for sp, kl, pb, bb in itertools.product([s[0] for s in SPACINGS],
                                            keylines_for("display", theme), bg, bg):
        out["display"].append({"spacing": sp, "keylines": kl, "pageBg": pb, "bentoBg": bb})
    for sp, kl, mode, rnd, pb, bb, cb in itertools.product(
            [s[0] for s in SPACINGS], keylines_for("gallery", theme),
            ["justified", "bento:ragged", "bento:square"],
            [r[0] for r in ROUNDINGS], bg, bg, bg):
        if not caption_legal(cb, bb) or not capsule_legal(rnd, cb, kl):
            continue
        out["gallery"].append({"spacing": sp, "keylines": kl, "mode": mode, "rounding": rnd,
                               "pageBg": pb, "bentoBg": bb, "capBg": cb})
    # ⬛ s217-D6 — the sub-bento dimension is the SNAP LADDER, eight stops, not three buttons.
    for ms, ss, kl, pb, bb in itertools.product([s[0] for s in DASH_MAIN], SUB_STOPS,
                                                keylines_for("dashboard", theme), bg, bg):
        out["dashboard"].append({"mainSpacing": ms, "subSpacing": str(ss), "keylines": kl,
                                 "pageBg": pb, "bentoBg": bb})
    return out


def matrix_counts(theme="mono"):
    return {k: len(v) for k, v in enumerate_matrix(theme).items()}


def counts_by_theme():
    """-> {theme: {type: n, …, '$total': n}}. THE HONEST SHAPE (s217-D6). One total for the page
    would be true in three themes and false in the fourth."""
    out = {}
    for t in THEMES:
        c = matrix_counts(t)
        c["$total"] = sum(c.values())
        out[t] = c
    return out


# ---------------------------------------------------------------------------- content
def content():
    """The page's content, from the ONE data path. -> dict."""
    photos, residuals = read_photos()
    for p in photos:
        p["ar"] = (float(p["w"]) / float(p["h"])) if (p["w"] and p["h"]) else 1.0
    prm = params()
    gal_ladder = band_ladder(dict(prm, columns=GALLERY_COLS))
    # RAGGED is the derived wall as-is (the gallery role's own policy — squaring OFF, s217-D3).
    # SQUARE is `square_wall`, the ratified pass, run at THIS wall's ladder. Both span sets are
    # minted here and carried on every tile; the dial swaps which one is in force by rewriting
    # `data-c`/`data-r` — canon's own vocabulary, so the responsive bands keep working. A second
    # page-local span vocabulary would out-specify the bands and silently break the collapse.
    ragged = [p["span"] for p in photos]
    squared, sq_report = square_wall(list(ragged), ladder=gal_ladder)
    rows, widows = pack_rows(photos)
    # DISPLAY — mixed content, panels and photographs together, squared by its role's own policy
    # (brochureware: squaring ON, s217-D3) rather than by a decision taken here.
    disp = []
    for i, panel in enumerate(PANELS):
        disp.append({"kind": "panel", "panel": panel,
                     "span": (min(panel[2], DISPLAY_COLS), panel[3])})
    for p in photos[:7]:
        disp.append({"kind": "photo", "photo": p,
                     "span": (min(p["span"][0], DISPLAY_COLS), p["span"][1])})
    disp_ladder = band_ladder(dict(prm, columns=DISPLAY_COLS))
    disp_spans, disp_report = square_wall_for_role([d["span"] for d in disp],
                                                   TYPE_ROLE["display"], ladder=disp_ladder)
    if disp_report.get("squared") and not disp_report.get("exempt"):
        for d, s in zip(disp, disp_spans):
            d["span"] = s
    # DASHBOARD — the OUTER wall of the bento-of-bentos. Its role's squaring policy is ON
    # (s217-D3, ratified: Dave "is very cool"), and it must run HERE, at mint time, because the
    # pass rewrites spans and CSS cannot express it.
    # ⛔ THE DEFECT THIS REPLACES, NAMED: the three groups were written with a literal
    # `data-c="1"` straight into the markup, so `square_wall_for_role` was never asked and the
    # ruled pass never ran on this wall. Three 1x1 groups at two columns leave the second row
    # half empty — the orphan gap in Dave's screenshot. Asked properly, the pass promotes the
    # third group to a two-column span and the wall closes.
    # ✅ s217-D7 — AND THE INNER WALLS RUN IT TOO, IN THE SAME CALL. `square_nested_wall` mints the
    # outer group spans AND each group's tile spans, so neither level can be left on a literal.
    dash_ladder = band_ladder(dict(prm, columns=DASH_COLS))
    dash_cards = [CARDS[i:i + 3] for i in range(0, 9, 3)]
    dash_groups = [(1, 1)] * len(dash_cards)
    dash_spans, dash_inner, nested_report = square_nested_wall(
        [[(c, r) for (_l, _s, _f, c, r) in g] for g in dash_cards],
        TYPE_ROLE["dashboard"], outer_spans=dash_groups,
        outer_cols=DASH_COLS, inner_cols=INNER_COLS)
    dash_report = nested_report["outer"]
    INNER_SQUARE_REPORTS.extend(nested_report["inner"])
    if BREAK_LAYOUT:
        dash_spans = dash_groups          # ⬛ ARM: the literal span, exactly as the defect had it
    if BREAK_INNER:
        # ⬛ ARM: every group back on its AUTHORED spans — the s217-D7 defect, one level down.
        dash_inner = [[(min(c, INNER_COLS), r) for (_l, _s, _f, c, r) in g] for g in dash_cards]
    return {"photos": photos, "ragged": ragged, "squared": squared, "sq_report": sq_report,
            "rows": rows, "widows": widows, "display": disp, "display_report": disp_report,
            "dash_spans": dash_spans, "dash_report": dash_report, "dash_ladder": dash_ladder,
            "dash_cards": dash_cards, "dash_inner": dash_inner, "nested_report": nested_report,
            "residuals": residuals, "gal_ladder": gal_ladder}


# ---------------------------------------------------------------------------- tiles
def photo_tile(p, ragged, squared, extra=""):
    """A gallery tile. Both minted span sets ride on the tile; `data-c`/`data-r` open on RAGGED
    (the gallery role's ruled default) and the dial rewrites them."""
    return ('<figure class="c-bento__tile bm-tile bm-gtile %s" data-c="%d" data-r="%d"'
            ' data-ragged="%d,%d" data-square="%d,%d">'
            '<span class="bm-imgbox"><img class="bm-img" src="%sknowledge/assets/photography-web/%s"'
            ' alt="%s" loading="lazy" width="%s" height="%s"></span>'
            '<figcaption class="c-bento__caption bm-cap">'
            '<span class="bm-desc t-ed-caption">%s</span>'
            '<span class="bm-lic t-cm-legal">%s</span></figcaption></figure>'
            % (extra, ragged[0], ragged[1], ragged[0], ragged[1], squared[0], squared[1],
               UP, esc(p["file"]), esc(p["desc"]), p["w"] or "", p["h"] or "",
               esc(p["desc"]), esc(p["licence"])))


def display_tile(d):
    c, r = d["span"]
    if d["kind"] == "panel":
        label, body, _c, _r = d["panel"]
        return ('<div class="c-bento__tile bm-tile bm-panel" data-c="%d" data-r="%d">'
                '<span class="bm-eyebrow t-cm-legal">%s</span>'
                '<span class="bm-body t-ed-body">%s</span></div>'
                % (c, r, esc(label), esc(body)))
    p = d["photo"]
    return ('<figure class="c-bento__tile bm-tile bm-dphoto" data-c="%d" data-r="%d">'
            '<span class="bm-imgbox"><img class="bm-img" src="%sknowledge/assets/photography-web/%s"'
            ' alt="%s" loading="lazy" width="%s" height="%s"></span></figure>'
            % (c, r, UP, esc(p["file"]), esc(p["desc"]), p["w"] or "", p["h"] or ""))


# ⬛ #217 — THE HAIRLINE PAIR, ONE MINT. Every tile that can carry treatment C's grid hairlines
# emits the SAME two elements: a vertical line for the gutter to its right and a horizontal line
# for the gutter below it. They are `display:none` until a rule turns them on, so a tile that is
# not under a C-bearing wall carries two inert nodes and paints nothing.
# ⛔ ELEMENTS, NOT A PAINTED GRID GROUND — the reason is a measured defect and it is restated at
# the CSS. A line-coloured background on the grid shows through the orphan cell of any group whose
# tiles do not fill its tracks, as a solid block (MEASURED #217, mono, third group).
GAPLINES = ('<i class="bm-gapline" data-axis="v" aria-hidden="true"></i>'
            '<i class="bm-gapline" data-axis="h" aria-hidden="true"></i>')


def card_tile(card, span, lines=True):
    """⛔ s217-D7 — THE SPAN IS A REQUIRED ARGUMENT, and the authored `card[3:5]` is deliberately
    NOT read here. A card tile can only be drawn with a span some caller obtained, and the only
    way to obtain one on this page is `inner_wall()` / `card_spans()`, which run the ratified
    pass. That is the class fix: a new group cannot mint an unsquared inner wall by omission."""
    label, sub, fig, _c, _r = card
    c, r = span
    return ('<div class="c-bento__tile bm-tile bm-card" data-c="%d" data-r="%d">'
            '<span class="bm-eyebrow t-cm-legal">%s</span>'
            '<span class="bm-sub t-cm-legal">%s</span>'
            '<span class="bm-fig t-ed-heading-4">%s</span>%s</div>'
            % (min(int(c), INNER_COLS), int(r), esc(label), esc(sub), esc(fig),
               GAPLINES if lines else ""))


# ------------------------------------------------------------------- the RULED keyline behaviour
# ⬛ s217-D8 RETIRED THE DECISION SPREAD. The A / B / C strip (three treatments of the double frame,
# at identical settings) existed to get ONE question answered by Dave's eye — who draws the line
# above 1px. He answered it: "the keylines should stay, but they should go round tight to the
# modules not run down the middle of the spacing". A decision surface for a settled question is
# worse than none: it invites the question to be re-opened and it keeps a retired construction
# alive on the page. What replaces it is a COMPACT NOTE, still conditional on the same two dials,
# saying what the wall above is doing and which ruling made it do that.
# ⛔ THE NOTE STAYS INSIDE THE DASHBOARD PANE, for the reason the spread did: the behaviour is a
# property of that wall at those settings, and a note parked in its own section reads as a
# different subject.


# ------------------------------------------------------------------- the sub-bento spacing sweep
# ⬛ #217, DAVE'S QUESTION VERBATIM: "what happens with sub-bento spacing?" — first asked of
# treatment C, and the question SURVIVES s217-D8 even though the construction did not. The rhythm
# story is what the strip is for: the SAME group drawn once at every ruled snap stop, labelled with
# its pixel value, so one glance covers the whole ladder. It now draws the RULED construction —
# tile-hugging boxes at every open stop, and the flush hairline construction at 1px.
# ⛔ FULL-WIDTH STACKED ROWS, NOT A COLUMNED CONTACT SHEET. Every `.c-bento` is a size container;
# eight walls side by side would each land near 140px, trip canon's 520px band, collapse to one
# column and answer a question about BANDS instead of about spacing (ds-054, and Dave's own first
# #217 defect). The label sits ABOVE its wall for the same reason — a label in a left-hand column
# takes width off the container it labels.
# ⛔ s217-D7 — AND THE SWEEP'S GROUP IS A NESTED WALL LIKE ANY OTHER. Its authored spans
# (2x1, 1x1, 1x1, 2x2, 1x1, 1x1) orphan TWO cells in three tracks, and under the retired centred
# construction the hairlines ran into that blank space — the symptom Dave saw. The pass is asked
# here, once, and
# every row of the strip inherits the same squared group, so the strip still compares SPACING and
# nothing else.
SWEEP_TILES = CARDS[0:6]


def sweep_spans():
    """-> the sweep group's spans, minted once so all eight rows are the SAME picture."""
    return card_spans(SWEEP_TILES, label="spacing sweep")


def sweep_html():
    """-> one labelled row per ruled snap stop, under the s217-D8 construction. ⛔ THE GUTTER IS
    DECLARED PER
    ROW in the stylesheet (one rule per stop, mirroring the live wall's eight), never a style=""
    attribute — an inline custom property is invisible to every instrument that reads the
    stylesheet against the document, and this strip exists to be measured."""
    out = []
    sw = sweep_spans()
    for s in SUB_STOPS:
        out.append(
            '<div class="bm-sw-row" data-stop="%d">'
            '<p class="bm-sw-label t-cm-legal"><b>%dpx</b>&nbsp; sub-bento spacing</p>'
            '<div class="bm-sw-ground">'
            '<div class="c-bento bm-sw-inner" data-bento-role="dashboard">'
            '<div class="c-bento__grid">%s</div></div></div></div>'
            % (s, s, "".join(card_tile(card, sp)
                             for card, sp in zip(SWEEP_TILES, sw))))
    return "\n      ".join(out)


# ------------------------------------------------------------------ the MAIN-WALL question (#217)
# ⬛ PROPOSED, NOT RULED, AND IT SURVIVES s217-D8: keylines live INSIDE groups only; the main wall's
# gutters between groups stay LINE-FREE, because space is what separates one group from the next.
# ⛔ THE COUNTER-EXAMPLE IS RETIRED (s217-D8). It drew a hairline down the middle of the main wall's
# gutter — the exact construction the ruling retires — so leaving it up would have kept a retired
# picture on the page as if it were still a live alternative. The PROPOSAL stays, drawn alone; what
# it proposes is now an absence of lines between groups in a wall whose tiles already carry their
# own edges, which is a smaller claim than it was.
MW_GROUPS = [CARDS[0:3], CARDS[3:6]]


def mainwall_html():
    """-> a two-group main wall: keylines round each module inside each group, and nothing in the
    main wall's own gutter."""
    cells = []
    for i, g in enumerate(MW_GROUPS):
        # ✅ s217-D7 — the main-wall question's own groups are nested walls too. The first one is
        # the measured orphan shape (2x1, 1x1, 1x1 in three tracks); asked, the pass closes it.
        spans = card_spans(g, label="main-wall group %d" % (i + 1))
        cells.append(
            '<div class="c-bento__tile bm-mw-cell" data-c="1" data-r="1">'
            '<div class="c-bento bm-mw-group" data-bento-role="dashboard">'
            '<div class="c-bento__grid">%s</div></div></div>'
            % "".join(card_tile(card, s, lines=False) for card, s in zip(g, spans)))
    return ('<div class="c-bento bm-mw-wall" data-bento-role="dashboard">'
            '<div class="c-bento__grid">%s</div></div>' % "".join(cells))


def justified_html(rows, widows):
    """Candidate B's justified rows — the SAME arithmetic as reviews/GALLERY-COMPARE (imported
    `pack_rows`), rendered the same way: flex-basis 0 with flex-grow proportional to the picture's
    own aspect, so the browser justifies at the real width instead of a baked pixel figure."""
    out, idx = [], 0
    for row in rows:
        cells = []
        for p in row:
            idx += 1
            cells.append(
                '<figure class="bm-jtile bm-p%d" data-ar="%.6f">'
                '<span class="bm-jbox"><img class="bm-img" src="%sknowledge/assets/photography-web/%s"'
                ' alt="%s" loading="lazy" width="%s" height="%s"></span>'
                '<figcaption class="c-bento__caption bm-cap">'
                '<span class="bm-desc t-ed-caption">%s</span>'
                '<span class="bm-lic t-cm-legal">%s</span></figcaption></figure>'
                % (idx, p["ar"], UP, esc(p["file"]), esc(p["desc"]), p["w"] or "", p["h"] or "",
                   esc(p["desc"]), esc(p["licence"])))
        out.append('<div class="bm-jrow">%s</div>' % "".join(cells))
    if widows:
        cells = []
        for p in widows:
            idx += 1
            cells.append(
                '<figure class="bm-jtile bm-widow bm-p%d" data-ar="%.6f">'
                '<span class="bm-jbox"><img class="bm-img" src="%sknowledge/assets/photography-web/%s"'
                ' alt="%s" loading="lazy" width="%s" height="%s"></span>'
                '<figcaption class="c-bento__caption bm-cap">'
                '<span class="bm-desc t-ed-caption">%s</span>'
                '<span class="bm-lic t-cm-legal">%s</span></figcaption></figure>'
                % (idx, p["ar"], UP, esc(p["file"]), esc(p["desc"]), p["w"] or "", p["h"] or "",
                   esc(p["desc"]), esc(p["licence"])))
        out.append('<div class="bm-jrow bm-jwidows">%s</div>' % "".join(cells))
    return "\n".join(out)


def photo_rules(photos):
    """The minted per-photograph flex-grow rules. DECLARED rules, never a `style=""` attribute —
    an inline custom property is invisible to every instrument that resolves the stylesheet
    against the document, and this page exists to be measured."""
    return "\n".join(".bm-p%d{--bm-ar:%.6f; flex-grow:%.6f;}" % (i, p["ar"], p["ar"])
                     for i, p in enumerate(photos, 1))


# ---------------------------------------------------------------------------- page-local CSS
# ⛔ NO BENTO STRUCTURE IS DECLARED HERE. The grid, the span vocabulary, the responsive bands, the
# role rules and the caption space are canon's (AUTO-BENTO, s217-D2/D3). What is here is (a) the
# INSTANCE DIALS the matrix turns, expressed as custom properties, (b) tile CONTENT, (c) the
# controller chrome, and (d) the justified-rows layout, which is not a grid and which canon has no
# grammar for — every one of those rules is named `.bm-j…`.
# ⚠ SPECIFICITY IS DELIBERATE THROUGHOUT. Canon's role rules are (0,2,0) and its tile rules
# (0,4,0); a dial written as a bare class would lose to them silently, in one theme, at one
# width. Every dial below names `.c-bento` (or more) so it out-specifies its own canon rule.
CSS = """
/* ===========================================================================
   BENTO MATRIX EXPLORER — page-local, scoped to `.bm`.
   ⬛ Everything the ruling did not say in words is marked PROPOSED on the page.
   ⛔ Every var() carries a literal fallback (silent-black class).
   =========================================================================== */
.bm{--bm-line:var(--border-subtle,#D7D8D6); --bm-line-2:var(--border-strong,#767676);
  --bm-ink:var(--text-default,#1A1A1A); --bm-ink-2:var(--text-secondary,#545454);
  --bm-page:var(--background-default,#FFFFFF);
  --bm-grey:var(--surface-subtle,#F0F0F0);
  --bm-white:var(--surface-raised,#FFFFFF);
  --bm-radius-ctl:var(--border-radius-control,0px);
  --bm-container-radius:var(--border-radius-container,0px);}

/* ---- controller chrome. NEUTRAL HUES ONLY — no red, no yellow, no green. ---- */
.bm-controls{border:1px solid var(--bm-line,#D7D8D6); padding:var(--sp-4,16px);
  display:flex; flex-wrap:wrap; gap:var(--sp-5,24px); align-items:flex-start;
  background:var(--bm-page,#FFFFFF); position:sticky; top:0; z-index:9;}
.bm-group{display:flex; flex-direction:column; gap:6px; min-width:0;}
.bm-group[hidden]{display:none;}
.bm-glabel{color:var(--bm-ink-2,#545454); text-transform:uppercase; letter-spacing:0.12em;}
.bm-why{color:var(--bm-ink-2,#545454); max-width:34ch; min-height:1.2em;}
.bm-seg{display:inline-flex; border:1px solid var(--bm-ink,#1A1A1A);
  color:var(--bm-ink,#1A1A1A); border-radius:var(--bm-radius-ctl,0px); overflow:hidden;}
.bm-seg button{font-family:inherit; font-size:12px; font-weight:500; letter-spacing:0.06em;
  text-transform:uppercase; padding:7px 12px; border:0; background:transparent; color:inherit;
  cursor:pointer; border-right:1px solid var(--bm-line,#D7D8D6); min-height:32px;}
.bm-seg button:last-child{border-right:0;}
.bm-seg button[aria-pressed="true"]{background:var(--bm-ink,#1A1A1A); color:var(--bm-page,#FFFFFF);}
/* a REFUSED option: visibly out, with its reason printed beside the group. Neutral only —
   the refusal is carried by weight and a strike, never by a hue. */
.bm-seg button[disabled]{color:var(--bm-ink-2,#545454); opacity:.45; cursor:not-allowed;
  text-decoration:line-through;}
.bm-seg button[disabled][aria-pressed="true"]{background:transparent;}
/* ---- ⬛ s217-D6 THE SNAP SLIDER. NEUTRAL HUES ONLY — the track, the thumb, the ticks and the
   read-out are all ink/line/surface, no red, no yellow, no green (Dave is astigmatic and those
   hues are unstable for him). The read-out prints the SNAPPED PIXEL VALUE, which is the same
   number the export carries — there is no second copy of it anywhere. ---- */
.bm-slider{display:flex; align-items:center; gap:var(--sp-3,12px); min-height:32px;}
.bm-range{-webkit-appearance:none; appearance:none; width:220px; max-width:46vw; height:32px;
  background:transparent; margin:0; cursor:pointer; color:var(--bm-ink,#1A1A1A);}
.bm-range:focus-visible{outline:2px solid var(--bm-ink,#1A1A1A); outline-offset:2px;}
.bm-range::-webkit-slider-runnable-track{height:2px; background:var(--bm-line-2,#767676);}
.bm-range::-moz-range-track{height:2px; background:var(--bm-line-2,#767676);}
.bm-range::-webkit-slider-thumb{-webkit-appearance:none; appearance:none; width:16px; height:16px;
  margin-top:-7px; background:var(--bm-ink,#1A1A1A); border:0;
  border-radius:var(--bm-radius-ctl,0px);}
.bm-range::-moz-range-thumb{width:16px; height:16px; background:var(--bm-ink,#1A1A1A); border:0;
  border-radius:var(--bm-radius-ctl,0px);}
.bm-out{min-width:5ch; color:var(--bm-ink,#1A1A1A); font-variant-numeric:tabular-nums;
  border:1px solid var(--bm-line-2,#767676); padding:3px 8px; text-align:center;}
.bm-stops{display:flex; gap:6px; color:var(--bm-ink-2,#545454); letter-spacing:0.06em;}

/* ---- the stage ---- */
.bm-stage{border:1px solid var(--bm-line,#D7D8D6); margin-top:var(--sp-4,16px);}
.bm-page-ground{padding:var(--sp-5,24px);}
.bm-stage[data-page-bg="grey"] .bm-page-ground{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-page-bg="white"] .bm-page-ground{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-page-bg="transparent"] .bm-page-ground{background:transparent;}
.bm-pane{display:none;}
.bm-stage[data-type="display"] .bm-pane[data-pane="display"],
.bm-stage[data-type="gallery"] .bm-pane[data-pane="gallery"],
.bm-stage[data-type="dashboard"] .bm-pane[data-pane="dashboard"]{display:block;}
.bm-capt{color:var(--bm-ink-2,#545454); margin:0 0 var(--sp-2,8px);}

/* ---- the WALL grounds. `.c-bento` in the selector so a bento background beats nothing but
   still reads at the same weight as a role rule. ---- */
.bm-stage[data-bento-bg="grey"] .c-bento.bm-wall{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-bento-bg="white"] .c-bento.bm-wall{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-bento-bg="transparent"] .c-bento.bm-wall{background:transparent;}

/* ---- SPACING — the instance dial, per type. (0,3,0), so it beats canon's (0,2,0) role rule. */
.bm-stage[data-spacing="1"]  .c-bento.bm-wall{--bento-gutter:1px;}
.bm-stage[data-spacing="24"] .c-bento.bm-wall{--bento-gutter:24px;}
.bm-stage[data-spacing="40"] .c-bento.bm-wall{--bento-gutter:40px;}
/* ⬛ P1, PROPOSED — TIGHT + KEYLINES ON. 1px cannot hold a gap AND a line, so the tiles go
   FLUSH (gutter 0) and the line becomes a hairline separator drawn INSIDE each tile's right and
   bottom edge, with the wall drawing its own top and left. That is the inset-group pattern, and
   it is why the wall's own edge is not doubled. */
.bm-stage[data-spacing="1"][data-keylines="on"] .c-bento.bm-wall{--bento-gutter:0px;}
/* ⛔ CHILD COMBINATOR, AND IT IS NOT COSMETIC — canon learned this on the span vocabulary and the
   explorer had not: `.bm-wall .bm-tile` is a DESCENDANT selector, and `.bm-outer` is also a
   `.bm-wall`, so the display wall's keyline rules reached every tile of every NESTED dashboard
   group and out-specified the dashboard's own. MEASURED #217 — the flush dashboard tiles were
   carrying a 1px border from a rule about a different wall. A wall's keylines belong to the tiles
   of ITS OWN grid. */
.bm-stage[data-spacing="1"][data-keylines="on"] .bm-wall > .c-bento__grid > .bm-tile{
  box-shadow:inset -1px 0 0 0 var(--bm-line,#D7D8D6),
             inset 0 -1px 0 0 var(--bm-line,#D7D8D6);}
.bm-stage[data-spacing="1"][data-keylines="on"] .c-bento.bm-wall{
  border-top:1px solid var(--bm-line,#D7D8D6);
  border-left:1px solid var(--bm-line,#D7D8D6);}
/* keylines at the two open spacings: a plain 1px tile border. */
.bm-stage[data-keylines="on"]:not([data-spacing="1"]) .bm-wall > .c-bento__grid > .bm-tile{
  border:1px solid var(--bm-line,#D7D8D6);}
/* keylines OFF at tight is the RULED behaviour: the 1px gap shows the ground through. */

/* ---- DASHBOARD spacing: main on the outer wall, sub on the inner ones. The outer selector
   carries five classes/attributes because canon's `:has(> .c-bento__grid > .c-bento)`
   carve-out for a bento-of-bentos is (0,4,0) and would otherwise win. ---- */
.bm-stage[data-main-spacing="24"] .bm-outer.c-bento[data-bento-role="dashboard"]{--bento-gutter:24px;}
.bm-stage[data-main-spacing="40"] .bm-outer.c-bento[data-bento-role="dashboard"]{--bento-gutter:40px;}
/* ⬛ s217-D6 — THE SUB-BENTO SNAP LADDER, ONE DECLARED RULE PER STOP. The slider can only land on
   a stop, so these eight rules are the complete vocabulary; a ninth value cannot be written and
   would render nothing if it were. DECLARED, never a style="" attribute — an inline custom
   property is invisible to every instrument that reads the stylesheet against the document. */
__SUB_SPACING_RULES__
/* ⛔ THE ROUNDED GROUP DRAWS ITS OWN OUTER EDGE; A TILE ONLY EVER SEPARATES (Dave, #217:
   "on – dashboard-keylines on – the corners are cropped so that the keylines are also cropped").
   THE CAUSE: the dashboard role puts the theme radius on the CONTAINER and CLIPS it (canon,
   s217-D2/D3, `overflow:hidden`). A keyline painted by a TILE at the group's edge is a straight
   line arriving at a curve, so the clip slices it and every corner reads with chopped line-ends —
   at 1px the last column/row's inset hairlines ran the full right and bottom edge, and at the open
   stops each edge tile's square border box was cut at all four corners. The only line that can
   follow a rounded corner is the ROUNDED BOX'S OWN BORDER, so with keylines ON the group takes a
   1px border and NO tile ever paints the outer edge. ⚠ ONE RULE, FOUR THEMES: mono, legacy and
   supercharge resolve `--border-radius-container` to 0, where the group border draws exactly the
   square rectangle the edge tiles used to draw — the same picture, from the container instead.
   ⬛ s217-D8 RULED (#217, 2026-08-24) — KEYLINES HUG THE MODULES; NO LINE EVER RUNS DOWN THE
   MIDDLE OF THE SPACING. Dave, rejecting the centred construction at open spacing twice: "the
   keylines are still running down the middle of the of the spacing" … "the keylines should stay,
   but they should go round tight to the modules not run down the middle of the spacing". The
   treatment-C centred-gutter construction is RETIRED for dashboards. What the wall draws now:
     · ABOVE 1px — every TILE wears its own tight 1px keyline box, and the GROUP'S OUTER BORDER
       STEPS BACK. That is not a preference: with the tiles carrying edges, a group border would
       re-create the DOUBLE FRAME Dave rejected earlier this session.
       ⬛ AMENDED #218 (2026-08-24), DAVE'S WORDS: "each tile must have it's own keyline, but the
       radii should only apply to the 4 corners of each sub bento (a collection of tiles)". The
       gutter-inset construction is RETIRED — he read it as "all that happens is that you add
       padding to the main bento and we loose the corner radii". What draws now: outer padding
       returns to 0, and the FOUR CORNER TILES of each group carry the group's own radius
       (`--bento-radius`) on their OUTER corner alone, so the tiles' keylines DRAW the rounded
       silhouette themselves — concentric with the container's clip, nothing straight ever meets
       the curve, and the radius is VISIBLE again on any ground (the padding construction hid it:
       border 0 + unpainted ground left the radius as a clip on an invisible box).
       ⛔ THE CORNER ASSIGNMENT IS MINTED PER BAND from the same dense placement the browser runs
       (`place()`-semantics, tile identity kept) — the responsive bands re-seat which tile holds
       a corner, so a single static assignment would round the wrong tile at 2 and 1 columns.
       See `corner_rules()`; the literals 820/520 mirror canon's compiled $bands.
     · AT 1px — UNCHANGED. Flush tiles cannot carry their own boxes without doubling every seam,
       so the s217-D6-era construction stands: the group keeps its 1px rounded border, the gutter
       is the hairline, and the container's own `overflow:hidden` stops it ALONG THE CURVE. This
       is the ONLY stop at which a line element renders anywhere on the dashboard pane.
     · ⛔ AND THE GUTTERS ABOVE 1px CARRY NOTHING AT ALL — no element, no paint. The hairline pair
       is `display:none` there, and `verify_bento_matrix_217.py` asserts the absence twice over:
       zero rendered line nodes in any gutter, and zero line-coloured pixels in the gutter
       interiors of the live wall. An absence asserted only on the node would pass a page that
       painted the retired line with a background. */
.bm-stage[data-keylines="on"][data-sub-spacing="1"] .bm-inner.c-bento[data-bento-role="dashboard"]{
  border:1px solid var(--bm-line,#D7D8D6); --bento-outer-padding:0px;}
/* ⛔ THE SUPPRESSION IS DECLARED, NOT LEFT AS AN ABSENCE. `.bm-outer` also carries `.bm-wall`, so
   the wall's own keyline rules above reach these tiles by descent; a tile that paints no edge here
   must be SAID to paint none. `overflow:visible` is what lets the line leave the tile at all —
   `.bm-tile` clips by default so its content cannot escape its own box. */
.bm-stage[data-keylines="on"][data-sub-spacing="1"] .bm-inner > .c-bento__grid > .bm-tile{
  border:0; box-shadow:none; overflow:visible; position:relative;}
.bm-stage[data-keylines="on"][data-sub-spacing="1"] .bm-inner > .c-bento__grid > .bm-tile
  > .bm-gapline{display:block;}
/* ⬛ s217-D8, THE OPEN STOPS — the tile-hugging box, and the group border stepping back. Weight
   is (0,4,0) on the group and (0,5,0) on the tile so both beat canon's role and tile rules. */
.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"])
  .bm-inner.c-bento[data-bento-role="dashboard"]{
  border:0; --bento-outer-padding:0px;}
.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-inner
  > .c-bento__grid > .bm-tile{
  border:1px solid var(--bm-line,#D7D8D6); box-shadow:none; overflow:hidden; position:relative;}
/* ⛔ AND THE RETIRED LINE IS SAID TO BE GONE, not left to be absent. The hairline pair is minted on
   every card tile (one mint, three consumers historically); above 1px it renders nowhere. */
.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-inner
  > .c-bento__grid > .bm-tile > .bm-gapline{display:none;}
__CORNER_RULES__
/* ⛔ THE MAIN WALL'S GUTTERS STAY LINE-FREE — PROPOSED (#217), and DECLARED rather than left as an
   absence. `.bm-outer`'s tiles ARE the groups, and a group is a clipped bento, so a line hung on
   one would be eaten by its own clip before it reached the main gutter. Space separates groups;
   lines separate tiles. */
.bm-stage .bm-outer > .c-bento__grid > .c-bento > .bm-gapline{display:none;}
.bm-stage[data-bento-bg="grey"] .c-bento.bm-inner{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-bento-bg="white"] .c-bento.bm-inner{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-bento-bg="transparent"] .c-bento.bm-inner{background:transparent;}

/* ---- INSTANCE DIALS: columns and row unit. A wall never renders wider than its own dial. ---- */
.c-bento.bm-gallery{--bento-columns:__GALLERY_COLS__; --bento-row-unit:240px;}
.c-bento.bm-display{--bento-columns:__DISPLAY_COLS__; --bento-row-unit:200px;}
.c-bento.bm-outer{--bento-columns:__DASH_COLS__; --bento-row-unit:auto;}
.c-bento.bm-inner{--bento-columns:__INNER_COLS__; --bento-row-unit:120px;}

/* ---- tile CONTENT ---- */
.bm-tile{margin:0; display:flex; flex-direction:column; min-width:0; overflow:hidden;
  background:var(--tertiary-background-default,#FFFFFF);}
/* ⛔ A GALLERY TILE PAINTS NO GROUND, AND THAT IS WHAT MAKES P2 A REAL QUESTION. The picture
   supplies its own ground, so the CAPTION's immediate ground is the wall — the bento background.
   Paint the tile instead and the caption would sit on the tile's surface, the bento background
   would never be the thing behind a caption, and the ruled inversion constraint ("white captions
   require a grey ground and the inverse") would be comparing the caption against a colour it
   never touches. MEASURED #217: with the tile painted, caption-white on bento-grey rendered
   white-on-white and the rule reported it legal. ⬛ PROPOSED — the ruling does not say where a
   gallery tile's ground comes from. A card or panel tile DOES keep its surface, which is what
   the ruled 1px show-through needs something to show through of. */
.bm-gtile, .bm-jtile{background:transparent;}
.bm-imgbox{display:block; flex:1 1 auto; min-height:0; overflow:hidden;}
.bm-img{display:block; width:100%; height:100%; object-fit:cover;
  background:var(--surface-subtle,#F0F0F0);}
.bm-cap{padding-inline:var(--sp-3,12px); color:var(--bm-ink-2,#545454); display:flex;
  flex-direction:column; gap:2px; justify-content:center;}
.bm-desc{display:-webkit-box; -webkit-line-clamp:var(--bento-caption-lines,3);
  -webkit-box-orient:vertical; overflow:hidden;}
.bm-panel,.bm-card{padding:var(--sp-4,16px); gap:var(--sp-2,8px); justify-content:flex-end;}
.bm-eyebrow{color:var(--bm-ink-2,#545454); text-transform:uppercase; letter-spacing:0.12em;}
.bm-body,.bm-fig{color:var(--bm-ink,#1A1A1A);}
.bm-sub{color:var(--bm-ink-2,#545454);}

/* ---- CAPTION GROUNDS (P2's subject). The caption's IMMEDIATE ground is the tile, which takes
   the bento background — so these two are what the legality rule compares. ---- */
.bm-stage[data-cap-bg="grey"] .bm-cap{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-cap-bg="white"] .bm-cap{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-cap-bg="transparent"] .bm-cap{background:transparent;}

/* ---- CONSOLE IMAGE ROUNDING (gallery). Both options are canon's container radius; what moves
   is WHAT IS ROUNDED. `4 corners of the image` rounds the picture and leaves the caption square
   and unclipped; `full capsule` rounds and clips the whole tile so caption and image are one
   block. The selectors carry six classes/attributes because canon's gallery tile rule is
   (0,4,0). ---- */
.bm-stage[data-rounding="corners"] .c-bento[data-bento-role="gallery"] >
  .c-bento__grid > .c-bento__tile.bm-gtile{border-radius:0; overflow:visible;}
.bm-stage[data-rounding="corners"] .c-bento[data-bento-role="gallery"] >
  .c-bento__grid > .c-bento__tile.bm-gtile .bm-imgbox{
  border-radius:var(--bm-container-radius,0px); overflow:hidden;}
.bm-stage[data-rounding="capsule"] .c-bento[data-bento-role="gallery"] >
  .c-bento__grid > .c-bento__tile.bm-gtile{
  border-radius:var(--bm-container-radius,0px); overflow:hidden;}

/* ---- ⬛ P4, PROPOSED — the stepped-down concentric radius, shown ONLY at Display tight. ---- */
/* ⛔ THE COMPARISON IS STACKED, NOT SIDE BY SIDE, AND THAT IS A CLASS RULE ON THIS PAGE:
   NOTHING IN THE EXPLORER MAY PRESENT A COMPARISON BY SHRINKING THE CONTAINER A BAND RESPONDS TO.
   Every `.c-bento` is `container-type:inline-size` (canon), so the responsive bands answer the
   WALL's width, not the window's. The first cut of P4 put the two walls in a two-column grid; at
   1280px each wall landed at ~571px, tripped the 820px band, and collapsed to two columns — so
   Display TIGHT rendered a DIFFERENT COMPOSITION from Display standard/generous and read as a
   different layout rather than the same one at 1px. MEASURED #217, and it is exactly Dave's
   words: "I expected display-tight to just be like standard and generous but just loosing the
   big padding. it seems to align to two columns."
   Stacking is the honest presentation: both walls get the SAME full container width, so the same
   band is in force on both and the ONLY variable between them is the radius — which is what the
   comparison is of. A toggle on one wall would have been honest too but shows one side at a time;
   a corner inset crop would compare a detail, not the composition. ⚠ THE INVARIANT IS PROBED:
   `verify_bento_matrix_217.py` asserts the tight wall's resolved column count EQUALS the standard
   wall's at the same viewport, and the selftest refuses any multi-column container holding a
   `.bm-wall`. */
.bm-alt{display:none;}
.bm-stage[data-type="display"][data-spacing="1"] .bm-alt{display:block;}
.bm-pair{display:flex; flex-direction:column; gap:var(--sp-5,24px);}
.bm-pair > *{min-width:0;}
/* the stepped alternative: half the container radius, so a tile corner inside a 1px group reads
   as concentric with the wall rather than as a second full-size curve. PROPOSED, not ruled. */
.c-bento.bm-display-stepped > .c-bento__grid > .c-bento__tile{
  border-radius:calc(var(--bm-container-radius,0px) / 2);}

/* ---- JUSTIFIED ROWS — not a grid; canon has no grammar for it. Every rule names `.bm-j`. ---- */
.bm-just{display:none; flex-direction:column; gap:var(--bento-gutter,24px);}
.bm-stage[data-mode="justified"] .bm-just{display:flex;}
.bm-stage[data-mode="justified"] .bm-gallery{display:none;}
.bm-stage[data-mode="bento"] .bm-just{display:none;}
.bm-jrow{display:flex; gap:var(--bento-gutter,24px); align-items:flex-start; min-width:0;}
.bm-jtile{margin:0; flex:0 1 0; min-width:0; display:flex; flex-direction:column;
  overflow:hidden;}
.bm-jbox{display:block; width:100%; aspect-ratio:var(--bm-ar,1.5); overflow:hidden;}
.bm-jbox .bm-img{object-fit:contain;}
/* THE WIDOWS — Flickr's rule and gen_gallery_compare_217's: whatever is left over is NOT blown
   up to justify. Each keeps its own aspect at the target row height. */
.bm-widow{flex:0 0 auto; width:calc(var(--layout-bento-row-unit,320px) * var(--bm-ar,1.5));}
.bm-stage[data-keylines="on"] .bm-jtile{border:1px solid var(--bm-line,#D7D8D6);}
.bm-stage[data-spacing="1"] .bm-just{--bento-gutter:1px;}
.bm-stage[data-spacing="24"] .bm-just{--bento-gutter:24px;}
.bm-stage[data-spacing="40"] .bm-just{--bento-gutter:40px;}
.bm-stage[data-rounding="capsule"] .bm-jtile{border-radius:var(--bm-container-radius,0px);}
.bm-stage[data-rounding="corners"] .bm-jbox{border-radius:var(--bm-container-radius,0px);}

/* ---- export + matrix table ---- */
.bm-export{border:1px solid var(--bm-line-2,#767676); margin-top:var(--sp-5,24px);}
.bm-exhead{display:flex; flex-wrap:wrap; gap:var(--sp-3,12px); align-items:center;
  padding:var(--sp-3,12px) var(--sp-4,16px); border-bottom:1px solid var(--bm-line,#D7D8D6);}
.bm-export pre{margin:0; padding:var(--sp-4,16px); overflow-x:auto;
  background:var(--bm-page,#FFFFFF); color:var(--bm-ink,#1A1A1A);}
.bm-tag{display:inline-block; border:1px solid var(--bm-line-2,#767676);
  color:var(--bm-ink,#1A1A1A); padding:2px 8px; letter-spacing:0.12em; text-transform:uppercase;}
.bm-btn{font:inherit; font-family:inherit; cursor:pointer; min-height:var(--tap,44px);
  border:1px solid var(--bm-line-2,#767676); background:transparent; color:var(--bm-ink,#1A1A1A);
  padding:0 var(--sp-4,16px); border-radius:var(--bm-radius-ctl,0px);}
/* ============================================================================================
   ⬛ THE KEYLINE NOTE — s217-D8, RULED. What stood here was the A / B / C DECISION SPREAD: three
   treatments of Dave's double-frame screenshot at identical settings, so he could rule by eye. He
   ruled: "the keylines should stay, but they should go round tight to the modules not run down the
   middle of the spacing". The spread is RETIRED — a decision surface for a settled question keeps
   a retired construction on the page and invites the question to be re-opened. What remains is a
   compact note, conditional on the SAME two dials the spread was, saying what the wall above is
   doing and naming the ruling that made it do it.
   ⛔ THE NOTE LIVES INSIDE THE DASHBOARD PANE, for the reason the spread did: the behaviour is a
   property of that wall at those settings.
     · keylines OFF          — no note at all; there is no keyline behaviour to describe.
     · keylines ON, sub >1px — the open-spacing note: tiles carry their own boxes, group border
                               steps back, gutters carry nothing.
     · keylines ON, sub 1px  — the flush note: the group keeps its curved border and the gutter IS
                               the hairline, stopped along the curve by the container's own clip.
   ============================================================================================ */
.bm-sp-strip{display:none; margin-top:var(--sp-6,32px);
  border-top:1px solid var(--bm-line,#D7D8D6); padding-top:var(--sp-5,24px);}
.bm-stage[data-type="dashboard"][data-keylines="on"] .bm-sp-strip{display:block;}
.bm-sp-intro{display:flex; flex-direction:column; gap:var(--sp-2,8px);}
.bm-sp-intro p{margin:0; color:var(--bm-ink-2,#545454); max-width:88ch;}
.bm-sp-title{margin:0; color:var(--bm-ink,#1A1A1A); display:flex; flex-wrap:wrap;
  gap:var(--sp-3,12px); align-items:baseline;}
/* the two ruled-behaviour notes, one per regime. Exactly one is on screen whenever the strip is. */
.bm-sp-open, .bm-sp-note{display:none; color:var(--bm-ink-2,#545454); margin:var(--sp-3,12px) 0 0;
  border-left:2px solid var(--bm-line-2,#767676); padding:var(--sp-3,12px) var(--sp-4,16px);}
.bm-stage[data-sub-spacing="1"] .bm-sp-note{display:block;}
.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-sp-open{display:block;}
/* ⛔ THE HAIRLINE GEOMETRY, AND IT NOW HAS ONE CONSUMER REGIME ONLY — the 1px flush stop, on the
   live wall and on the sweep's 1px row. Above 1px, s217-D8 retires it: no line runs down the
   middle of any spacing, so these elements render nowhere.
   ⛔ THE OFFSET IS (gutter + 1px) / 2, AND THE +1px IS THE WHOLE POINT — it was `gutter / 2` and
   that is HALF A PIXEL OFF CENTRE. `right` measures from the tile's edge to the LINE'S RIGHT EDGE,
   not to its centre. At g = 1 the offset is exactly 1px, so the line occupies [edge, edge + 1] —
   the whole of a 1px gutter, which is what makes the flush stop flush rather than centred.
   ⛔ ELEMENTS, NOT A PAINTED GRID GROUND. A line-coloured background on the grid is the shorter
   rule and it renders a DEFECT: a group whose tiles do not fill its tracks shows the ground
   through the orphan cell as a solid block (MEASURED #217, mono, third group). */
.bm-gapline{display:none; position:absolute; pointer-events:none;
  background:var(--bm-line,#D7D8D6);}
.bm-gapline[data-axis="v"]{
  width:1px; right:calc((var(--bento-gutter,24px) + 1px) / -2);
  top:calc((var(--bento-gutter,24px) + 1px) / -2);
  bottom:calc((var(--bento-gutter,24px) + 1px) / -2);}
.bm-gapline[data-axis="h"]{
  height:1px; bottom:calc((var(--bento-gutter,24px) + 1px) / -2);
  left:calc((var(--bento-gutter,24px) + 1px) / -2);
  right:calc((var(--bento-gutter,24px) + 1px) / -2);}

/* ============================================================================================
   ⬛ THE SUB-BENTO SPACING SWEEP — #217, Dave's question: "what happens with sub-bento spacing?"
   The same group, drawn once at every ruled snap stop, labelled with its pixel value, full width
   and stacked. The question was first asked of the retired centred construction; the RHYTHM story
   is what it was for, and it survives s217-D8 — so the strip now draws the RULED construction:
   tile-hugging boxes at every open stop, and the flush hairline at 1px.
   ⛔ FULL WIDTH, STACKED, AND THAT IS A CLASS RULE ON THIS PAGE (ds-054). Every `.c-bento` is
   `container-type:inline-size`; eight walls in a row would each land near 140px, trip canon's
   520px band and collapse to a single column — the strip would then answer a question about
   RESPONSIVE BANDS while claiming to answer one about spacing.
   ============================================================================================ */
.bm-sweep{display:none; margin-top:var(--sp-6,32px);
  border-top:1px solid var(--bm-line,#D7D8D6); padding-top:var(--sp-5,24px);}
.bm-stage[data-type="dashboard"][data-keylines="on"] .bm-sweep{display:block;}
.bm-sw-strip{display:flex; flex-direction:column; gap:var(--sp-5,24px);
  margin-top:var(--sp-5,24px);}
.bm-sw-row{display:flex; flex-direction:column; gap:var(--sp-2,8px);}
.bm-sw-label{color:var(--bm-ink-2,#545454);}
.bm-sw-label b{color:var(--bm-ink,#1A1A1A); font-variant-numeric:tabular-nums;}
.bm-sw-ground{background:var(--bm-grey,#F0F0F0); padding:var(--sp-4,16px);}
.bm-stage[data-page-bg="white"] .bm-sw-ground{background:var(--bm-white,#FFFFFF);}
/* ⬛ s217-D8 — EVERY ROW DRAWS THE RULED CONSTRUCTION. Above 1px the tiles wear their own boxes,
   the group's border steps back and the tiles are inset from the container by the gutter, so no
   straight edge arrives at the curve. The group is still expressed: background and clipped radius.
   ⛔ THE 1px ROW IS THE OTHER REGIME, DECLARED — the group takes the border, the tiles go flush
   and the gutter IS the hairline, clipped along the curve. Two regimes, one per row, and the
   strip's whole subject is the rhythm between them. */
.bm-sw-inner.c-bento[data-bento-role="dashboard"]{
  --bento-columns:__INNER_COLS__; --bento-row-unit:96px;
  --bento-outer-padding:var(--bento-gutter,24px);
  background:var(--bm-white,#FFFFFF); border:0;}
.bm-sw-inner > .c-bento__grid > .bm-tile{
  border:1px solid var(--bm-line,#D7D8D6); box-shadow:none; overflow:hidden; position:relative;}
.bm-sw-inner > .c-bento__grid > .bm-tile > .bm-gapline{display:none;}
.bm-sw-row[data-stop="1"] .bm-sw-inner.c-bento[data-bento-role="dashboard"]{
  --bento-outer-padding:0px; border:1px solid var(--bm-line,#D7D8D6);}
.bm-sw-row[data-stop="1"] .bm-sw-inner > .c-bento__grid > .bm-tile{
  border:0; box-shadow:none; overflow:visible;}
.bm-sw-row[data-stop="1"] .bm-sw-inner > .c-bento__grid > .bm-tile > .bm-gapline{display:block;}
/* ⛔ ONE DECLARED RULE PER RULED STOP — the same discipline as the live wall's eight. A ninth
   value cannot be written here and would render nothing if it were. */
__SWEEP_STOP_RULES__

/* ---- ⬛ THE MAIN-WALL QUESTION — PROPOSED, NOT RULED: keylines inside the groups, and nothing
   in the main wall's own gutter between them.
   ⛔ THE COUNTER-EXAMPLE IS RETIRED (s217-D8). It hung a hairline down the middle of the main
   wall's gutter — the construction the ruling retires — and needed an UNCLIPPED WRAPPER CELL to do
   it, because a group is a bento with `overflow:hidden`. Keeping it would have kept a retired
   picture on the page as a live alternative. `.bm-mw-cell` stays as the wrapper the wall's cells
   already are; it now hangs nothing. ---- */
.bm-mw{display:flex; flex-direction:column; gap:var(--sp-5,24px); margin-top:var(--sp-5,24px);}
.bm-mw-case{display:flex; flex-direction:column; gap:var(--sp-2,8px);}
.bm-mw-ground{background:var(--bm-grey,#F0F0F0); padding:var(--sp-4,16px);}
.bm-stage[data-page-bg="white"] .bm-mw-ground{background:var(--bm-white,#FFFFFF);}
.bm-mw-wall.c-bento[data-bento-role="dashboard"]{
  --bento-columns:2; --bento-row-unit:auto; --bento-gutter:24px; background:transparent;}
.bm-mw-cell{position:relative; overflow:visible; display:flex; background:transparent;}
/* the groups draw the s217-D8 construction at their own 8px sub-spacing: tile boxes, no group
   border, tiles inset from the container by the gutter. */
.bm-mw-group.c-bento[data-bento-role="dashboard"]{
  --bento-columns:__INNER_COLS__; --bento-row-unit:96px; --bento-gutter:8px;
  --bento-outer-padding:var(--bento-gutter,8px); width:100%;
  background:var(--bm-white,#FFFFFF); border:0;}
.bm-mw-group > .c-bento__grid > .bm-tile{
  border:1px solid var(--bm-line,#D7D8D6); box-shadow:none; overflow:hidden; position:relative;}
.bm-mw-group > .c-bento__grid > .bm-tile > .bm-gapline{display:none;}

@media (prefers-reduced-motion: reduce){
  .bm *,.bm *::before,.bm *::after{transition-duration:.01ms !important;
    animation-duration:.01ms !important;}
}
__PHOTO_RULES__
"""


# ---------------------------------------------------------------------------- page-local JS
# ⛔ ONE STATE OBJECT, TWO CONSUMERS. `apply()` writes the stage attributes AND renders the export
# in the same pass; there is no second copy of the dial values anywhere in the page.
SCRIPT = r"""
(function(){
  var STATE = {
    type: 'display',
    display:  {spacing:'24', keylines:'on',  pageBg:'white', bentoBg:'grey'},
    gallery:  {spacing:'24', keylines:'on',  mode:'bento', edge:'ragged', rounding:'corners',
               pageBg:'white', bentoBg:'grey', capBg:'white'},
    dashboard:{mainSpacing:'24', subSpacing:'1', keylines:'on', pageBg:'grey', bentoBg:'white'}
  };
  var stage = document.getElementById('bm-stage');
  var out   = document.getElementById('bm-export');

  // ⬛ s217-D6 — THE SNAP LADDER, mirrored from gen_bento_matrix_217.SUB_STOPS. ONE ladder, and
  // the CSS carries one declared rule per member, so a value off the ladder cannot render.
  var SUB_STOPS = __SUB_STOPS__;
  function snap(px){
    var v = parseFloat(px); if (isNaN(v)) v = SUB_STOPS[0];
    return SUB_STOPS.reduce(function(a, b){
      return (Math.abs(b - v) < Math.abs(a - v)) ? b : a; });
  }

  // ⬛ s217-D6 — GALLERY IN CONSOLE EXCLUDES KEYLINES. ABSENT, NOT DISABLED, and 'absent' is only
  // an honest word if the node is really gone: the group is lifted OUT of the document and an
  // anchor comment is left where it stood, so it can be put back exactly when the theme changes.
  // Hiding it would leave a probe unable to tell exclusion from a collapsed control.
  var KEYLINE_EXCLUDED = __KEYLINE_EXCLUDED__;
  var PARKED = {};
  Array.prototype.forEach.call(
    document.querySelectorAll('.bm-group[data-dial="keylines"]'), function(g){
      var t = g.getAttribute('data-group');
      var anchor = document.createComment('bm-keylines-' + t);
      g.parentNode.insertBefore(anchor, g);
      PARKED[t] = {node: g, anchor: anchor};
    });
  function keylinesExcluded(type){
    var theme = document.documentElement.getAttribute('data-apollo-theme');
    for (var i = 0; i < KEYLINE_EXCLUDED.length; i++)
      if (KEYLINE_EXCLUDED[i][0] === type && KEYLINE_EXCLUDED[i][1] === theme) return true;
    return false;
  }
  function syncExclusions(){
    Object.keys(PARKED).forEach(function(t){
      var e = PARKED[t], present = !!e.node.parentNode;
      if (keylinesExcluded(t)) {
        // ⛔ AND THE STATE MOVES WITH THE CONTROL. Leaving `keylines:'on'` in the state object
        // while the control is gone would export a dial the page no longer offers.
        if (STATE[t]) STATE[t].keylines = 'off';
        if (present) e.node.parentNode.removeChild(e.node);
      } else if (!present) {
        e.anchor.parentNode.insertBefore(e.node, e.anchor.nextSibling);
      }
    });
  }

  // ⛔ THE LEGALITY RULES — the browser-side statement of the SAME two rules the page's matrix
  // count is computed from (P2, P3). A reason string is a REFUSAL; '' is legal.
  function legality(){
    var g = STATE.gallery, r = {};
    __LEGALITY_BODY__
    return r;
  }

  function repair(){
    // ⛔ NO REACHABLE STATE MAY RENDER NOTHING, and no dial may sit on a refused value. If a
    // change makes the current selection illegal, the page MOVES the selection to the legal
    // neighbour and SAYS SO — silence here would leave a control pressed on an option the page
    // refuses to draw.
    var l = legality(), moved = [];
    if (l['capBg:' + STATE.gallery.capBg]) { STATE.gallery.capBg = 'transparent';
      moved.push('caption background moved to Transparent'); }
    l = legality();
    if (l['rounding:' + STATE.gallery.rounding]) { STATE.gallery.rounding = 'corners';
      moved.push('image rounding moved to 4 corners'); }
    return moved;
  }

  function resolved(){
    // s200-D1 — CONCRETE VALUES, read out of the live document in the state on screen. No var()
    // chain reaches the export; where a dial says "the theme token", the exporter writes down the
    // number the theme actually resolved.
    var pane = stage.querySelector('.bm-pane[data-pane="' + STATE.type + '"]');
    var wall = pane ? pane.querySelector('.c-bento') : null;
    var grid = wall ? wall.querySelector('.c-bento__grid') : null;
    var tile = grid ? grid.querySelector('.c-bento__tile') : null;
    var cap  = pane ? pane.querySelector('.bm-cap') : null;
    var ground = stage.querySelector('.bm-page-ground');
    var px = function(v){ return Math.round(parseFloat(v) || 0); };
    return {
      theme: document.documentElement.getAttribute('data-apollo-theme'),
      mode: document.body.getAttribute('data-theme'),
      role: wall ? wall.getAttribute('data-bento-role') : null,
      gutterPx: grid ? px(getComputedStyle(grid).columnGap) : null,
      containerRadiusPx: wall ? px(getComputedStyle(wall).borderTopLeftRadius) : null,
      tileRadiusPx: tile ? px(getComputedStyle(tile).borderTopLeftRadius) : null,
      tileBorderPx: tile ? px(getComputedStyle(tile).borderTopWidth) : null,
      pageBackground: ground ? getComputedStyle(ground).backgroundColor : null,
      bentoBackground: wall ? getComputedStyle(wall).backgroundColor : null,
      captionBackground: cap ? getComputedStyle(cap).backgroundColor : null,
      captionSpacePx: cap ? px(getComputedStyle(cap).minHeight) : null
    };
  }

  function spans(){
    // The ragged/square dial is a MINT-TIME span swap, not a second CSS vocabulary: it rewrites
    // canon's own `data-c`/`data-r`, so the responsive bands keep working underneath it.
    var want = (STATE.gallery.mode === 'bento' && STATE.gallery.edge === 'square')
             ? 'square' : 'ragged';
    Array.prototype.forEach.call(stage.querySelectorAll('.bm-gtile'), function(t){
      var v = (t.getAttribute('data-' + want) || '1,1').split(',');
      t.setAttribute('data-c', v[0]); t.setAttribute('data-r', v[1]);
    });
  }

  function syncSlider(){
    // ⛔ THE STATE IS THE TRUTH AND THE CONTROL IS REDRAWN FROM IT. The snap happens here, once,
    // BEFORE the stage attribute is written — so the CSS, the thumb, the read-out and the export
    // are four views of one snapped number and cannot disagree.
    var v = snap(STATE.dashboard.subSpacing);
    STATE.dashboard.subSpacing = String(v);
    var range = document.getElementById('bm-subSpacing');
    if (range) {
      if (String(range.value) !== String(v)) range.value = v;
      range.setAttribute('aria-valuetext', v + 'px');
    }
    var o = document.getElementById('bm-subSpacing-out');
    if (o) o.textContent = v + 'px';
  }

  function apply(){
    syncExclusions();
    syncSlider();
    var s = STATE[STATE.type], moved = repair();
    stage.setAttribute('data-type', STATE.type);
    stage.setAttribute('data-keylines', s.keylines);
    stage.setAttribute('data-page-bg', s.pageBg);
    stage.setAttribute('data-bento-bg', s.bentoBg);
    if (STATE.type === 'dashboard') {
      stage.setAttribute('data-spacing', s.mainSpacing);
      stage.setAttribute('data-main-spacing', s.mainSpacing);
      stage.setAttribute('data-sub-spacing', s.subSpacing);
      stage.removeAttribute('data-cap-bg');
    } else {
      stage.setAttribute('data-spacing', s.spacing);
      stage.removeAttribute('data-main-spacing');
      stage.removeAttribute('data-sub-spacing');
    }
    if (STATE.type === 'gallery') {
      stage.setAttribute('data-mode', STATE.gallery.mode);
      stage.setAttribute('data-edge', STATE.gallery.edge);
      stage.setAttribute('data-rounding', STATE.gallery.rounding);
      stage.setAttribute('data-cap-bg', STATE.gallery.capBg);
      spans();
    } else {
      stage.removeAttribute('data-mode'); stage.removeAttribute('data-edge');
      stage.removeAttribute('data-rounding');
    }
    var l = legality();
    // groups: show the ones this type owns, and the conditional ones only when their condition
    // holds. An option removed by a RULING is absent from the markup entirely; an option refused
    // by a legality rule is present and disabled WITH ITS REASON.
    Array.prototype.forEach.call(document.querySelectorAll('.bm-group'), function(g){
      var owner = g.getAttribute('data-group');
      var when = g.getAttribute('data-when');
      var on = (owner === 'all' || owner === STATE.type);
      if (on && when) {
        var kv = when.split(':');
        on = (STATE[STATE.type][kv[0]] === kv[1]);
      }
      g.hidden = !on;
      var dial = g.getAttribute('data-dial');
      var why = g.querySelector('.bm-why'), reasons = [];
      Array.prototype.forEach.call(g.querySelectorAll('button[data-value]'), function(b){
        var v = b.getAttribute('data-value');
        var reason = l[dial + ':' + v] || '';
        b.disabled = !!reason;
        b.setAttribute('aria-disabled', String(!!reason));
        var cur = (dial === 'type') ? STATE.type : STATE[STATE.type][dial];
        b.setAttribute('aria-pressed', String(cur === v));
        if (reason) reasons.push(reason);
      });
      if (why) why.textContent = reasons.length ? reasons[0] : '';
    });
    var note = document.getElementById('bm-moved');
    if (note) note.textContent = moved.length
      ? ('Adjusted so the combination stays legal — ' + moved.join('; ') + '.') : '';
    render();
  }

  function render(){
    var payload = {
      "$proposed": true,
      "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
      "ruling": "s217-D5",
      "type": STATE.type,
      "state": STATE[STATE.type],
      "resolved": resolved()
    };
    if (out) out.textContent = JSON.stringify(payload, null, 2);
  }

  document.addEventListener('click', function(e){
    var b = e.target.closest ? e.target.closest('.bm-seg button[data-value]') : null;
    if (!b || b.disabled) return;
    var g = b.closest('.bm-group'), dial = g.getAttribute('data-dial');
    if (dial === 'type') STATE.type = b.getAttribute('data-value');
    else STATE[STATE.type][dial] = b.getAttribute('data-value');
    apply();
  });
  // ⬛ s217-D6 — the slider. `input` (not `change`), so the snap lands while the thumb is moving
  // rather than on release; the raw pixel value is snapped before anything downstream sees it.
  document.addEventListener('input', function(e){
    var r = e.target;
    if (!r || !r.classList || !r.classList.contains('bm-range')) return;
    var g = r.closest('.bm-group'), dial = g && g.getAttribute('data-dial');
    if (!dial) return;
    STATE[g.getAttribute('data-group')][dial] = String(snap(r.value));
    apply();
  });
  var re = document.getElementById('bm-rebuild');
  if (re) re.addEventListener('click', function(){ apply(); });
  // the theme/mode chrome re-renders the export, because the RESOLVED half of it is theme-bound
  window.addEventListener('hashchange', function(){ setTimeout(apply, 60); });
  document.addEventListener('click', function(e){
    if (e.target.closest && e.target.closest('#themes, #modes')) setTimeout(apply, 60);
  });
  apply();
  window.__BM_STATE = STATE;           // the probe reads the SAME object the preview renders from
  window.__BM_APPLY = apply;
  window.__BM_LEGALITY = legality;
})();
"""

LEGALITY_JS_REAL = """
    // P2 — a caption colour is judged against its IMMEDIATE ground (the bento background behind
    // the tile). Transparent is always legal: it has no ground of its own to collide with.
    ['grey','white','transparent'].forEach(function(v){
      r['capBg:' + v] = (v !== 'transparent' && v === g.bentoBg)
        ? ('Illegal — the caption would be ' + v + ' on ' + v + ', its own ground. '
           + 'A white caption needs a grey ground, and the inverse (s217-D5).')
        : '';
    });
    // P3 — the full capsule needs an edge: a caption background OR keylines.
    r['rounding:capsule'] = (g.capBg === 'transparent' && g.keylines === 'off')
      ? 'Illegal — a capsule with a transparent caption and no keylines has no edge to round. '
        + 'Turn keylines on, or give the caption a background. PROPOSED (open point 3).'
      : '';
    r['rounding:corners'] = '';
"""

LEGALITY_JS_BROKEN = """
    // ⬛ MUTATION ARM — the legality rules are GONE. Every option reports legal, so the refusals
    // the probe asserts must go RED by name. This variant is NON-REPO and never shipped.
    ['grey','white','transparent'].forEach(function(v){ r['capBg:' + v] = ''; });
    r['rounding:capsule'] = ''; r['rounding:corners'] = '';
"""


# ---------------------------------------------------------------------------- controls markup
def seg(group, dial, options, label, when=None, sub=""):
    btns = "".join('<button type="button" data-value="%s">%s</button>' % (esc(v), esc(t))
                   for v, t in options)
    return ('<div class="bm-group" data-group="%s" data-dial="%s"%s>'
            '<span class="bm-glabel t-cm-legal">%s</span>'
            '<div class="bm-seg" role="group" aria-label="%s">%s</div>'
            '<span class="bm-why t-cm-legal">%s</span></div>'
            % (esc(group), esc(dial), (' data-when="%s"' % esc(when)) if when else "",
               esc(label), esc(label), btns, esc(sub)))


def slider(group, dial, stops, label, sub=""):
    """⬛ s217-D6 — the SNAPPING SLIDER that replaces the three-stop sub-bento control.
    ⚠ THE RANGE IS DRIVEN IN PIXELS, min..max over the ladder, step 1 — NOT in stop indices. An
    index-only slider would be snapped by arithmetic that never happened, and 'snaps to' would be
    unfalsifiable: there would be no off-snap value to land. Driven in pixels, the snap is a real
    operation the probe can drive (set 7, assert 8) and the datalist gives the stops their ticks."""
    ticks = "".join('<option value="%d" label="%d"></option>' % (s, s) for s in stops)
    return ('<div class="bm-group bm-group--slider" data-group="%s" data-dial="%s"'
            ' data-stops="%s">'
            '<span class="bm-glabel t-cm-legal">%s</span>'
            '<div class="bm-slider">'
            '<input type="range" class="bm-range" id="bm-%s" name="bm-%s" min="%d" max="%d"'
            ' step="1" value="%d" list="bm-%s-ticks" aria-label="%s"'
            ' aria-valuetext="%dpx">'
            '<datalist id="bm-%s-ticks">%s</datalist>'
            '<output class="bm-out t-cm-legal" id="bm-%s-out" for="bm-%s">%dpx</output></div>'
            '<span class="bm-why bm-stops t-cm-legal">Snaps to %s</span>'
            '<span class="bm-why t-cm-legal">%s</span></div>'
            % (esc(group), esc(dial), esc(",".join(str(s) for s in stops)), esc(label),
               esc(dial), esc(dial), stops[0], stops[-1], stops[0], esc(dial), esc(label),
               stops[0], esc(dial), ticks, esc(dial), esc(dial), stops[0],
               esc(" · ".join("%dpx" % s for s in stops)), esc(sub)))


def controls():
    bg = [(v, t) for v, t, _tok in BACKGROUNDS]
    sp = [(v, "%s %s" % (t, px)) for v, t, px in SPACINGS]
    dm = [(v, "%s %s" % (t, px)) for v, t, px in DASH_MAIN]
    g = []
    g.append(seg("all", "type", [("display", "Display"), ("gallery", "Gallery"),
                                 ("dashboard", "Dashboard")], "Type"))
    for t in ("display", "gallery"):
        g.append(seg(t, "spacing", sp, "Spacing"))
    g.append(seg("dashboard", "mainSpacing", dm, "Main bento spacing"))
    g.append(slider("dashboard", "subSpacing", SUB_STOPS, "Sub-bento spacing"))
    for t in ("display", "gallery", "dashboard"):
        # ⬛ s217-D6 — the gallery keyline group is EXCLUDED in console. It is authored here (the
        # other three themes keep it) and REMOVED FROM THE DOCUMENT at runtime when console is in
        # force; a probe asking "is the control there?" therefore gets the truth, in every theme.
        g.append(seg(t, "keylines", ONOFF, "Keylines"))
    g.append(seg("gallery", "mode", GALLERY_MODES, "Mode"))
    g.append(seg("gallery", "edge", BOTTOM_EDGE, "Bottom edge", when="mode:bento"))
    g.append(seg("gallery", "rounding", ROUNDINGS, "Console image rounding"))
    for t in ("display", "gallery", "dashboard"):
        g.append(seg(t, "pageBg", bg, "Page background"))
    for t in ("display", "gallery", "dashboard"):
        g.append(seg(t, "bentoBg", bg, "Bento background"))
    g.append(seg("gallery", "capBg", bg, "Caption background"))
    return "\n      ".join(g)


# ---------------------------------------------------------------------------- the page body
def body(c):
    # ⛔ THE COUNT IS THEME-DEPENDENT NOW AND THE PAGE SAYS SO ON ITS FACE (s217-D6). Gallery in
    # console has NO keyline control, so a single headline total would be true in three themes
    # and false in the fourth. `base` is the three themes that keep the control; `console` is
    # counted on its own and the difference is printed rather than averaged away.
    by_theme = counts_by_theme()
    counts = matrix_counts("mono")            # the three unexcluded themes agree
    console = matrix_counts("console")
    space, lines = caption_space()
    photos = c["photos"]
    gal = "\n".join("      " + photo_tile(p, r, s)
                    for p, r, s in zip(photos, c["ragged"], c["squared"]))
    disp = "\n".join("      " + display_tile(d) for d in c["display"])
    inner = []
    for n, cards in enumerate(c["dash_cards"]):
        # ⛔ BOTH SPANS COME FROM THE RULED PASS, never from a literal — the group's own span on
        # the outer wall (s217-D3) and its tiles' spans inside it (s217-D7). See content().
        sc, sr = c["dash_spans"][n]
        inner.append(
            '<div class="c-bento c-bento__tile bm-inner" data-bento-role="dashboard"'
            ' data-c="%d" data-r="%d"><div class="c-bento__grid">%s</div></div>'
            % (sc, sr, "".join(card_tile(card, s)
                               for card, s in zip(cards, c["dash_inner"][n]))))
    dash = "\n".join("      " + x for x in inner)
    just = justified_html(c["rows"], c["widows"])
    total = sum(counts.values())
    console_total = sum(console.values())
    r = roles()

    open_points = [
        ("P1", "Tight + keylines ON",
         "1px cannot hold both a gap and a line, so tight + keylines renders as FLUSH tiles with "
         "hairline separators — the inset-group pattern. Tight + keylines OFF is the ruled "
         "behaviour: a 1px gap with the ground showing through. Turn Spacing to Tight and toggle "
         "Keylines to see both."),
        ("P2", "The caption inversion rule",
         "Read as judged against the caption's IMMEDIATE ground — the bento background behind the "
         "tile. Grey on grey and white on white are refused with the reason printed beside the "
         "control; transparent is always legal."),
        ("P3", "The full capsule",
         "Proposed to REQUIRE a caption background or keylines: with neither, the capsule has no "
         "edge to be a capsule of. Enforced in the selector, not just described."),
        ("P4", "Console tile radius at tight spacing",
         "The standard radius may pinch at 1px. At Display tight the page draws the standard "
         "radius and a stepped-down concentric alternative (half the container radius) SIDE BY "
         "SIDE, so the pinch is a comparison rather than an assertion."),
        ("P5", "One palette on all three types",
         "The lightest grey / white / transparent palette is applied to Display and Dashboard "
         "selectors by extension from the gallery's ruled list."),
    ]
    points_html = "".join(
        '<li><b>%s &middot; %s</b> <span class="bm-tag t-cm-legal">Proposed</span><br>%s</li>'
        % (esc(k), esc(t), esc(d)) for k, t, d in open_points)

    counts_rows = "".join(
        "<tr><td>%s</td><td class='num'>%d</td><td class='num'>%d</td><td>%s</td></tr>"
        % (esc(k.title()), counts[k], console[k], dims)   # dims is authored here, not user data
        for k, dims in (
            ("display", "spacing 3 × keylines 2 × page background 3 × bento background 3"),
            ("gallery", "spacing 3 × keylines <b>2, or 1 in console</b> × mode 3 (justified · "
                        "bento ragged · bento square) × rounding 2 × page 3 × bento 3 × caption 3, "
                        "MINUS the combinations the two legality rules refuse"),
            ("dashboard", "main spacing 2 (never tight) × sub-bento spacing <b>8</b> (the "
                          "s217-D6 snap ladder) × keylines 2 × page 3 × bento 3")))
    theme_rows = "".join(
        "<tr><td>%s</td><td class='num'>%d</td><td class='num'>%d</td><td class='num'>%d</td>"
        "<td class='num'><b>%d</b></td></tr>"
        % (esc(t), by_theme[t]["display"], by_theme[t]["gallery"], by_theme[t]["dashboard"],
           by_theme[t]["$total"]) for t in THEMES)

    return """
  <section id="intro">
    <h2 class="t-ed-heading-3">Bento</h2>
    <p class="t-ed-body lede">A Foundations tier entry, not a component. The bento system as a
      <b>live matrix of options over three types</b> &mdash; <b>Display</b>, <b>Gallery</b> and
      <b>Dashboard</b> &mdash; exactly as ruled at <code>s217-D5</code>. Turn the dials; the
      preview and the export block at the foot of the page are rendered in the same pass from the
      same state object, so the export cannot describe a combination you did not see.</p>
    <p class="t-ed-body-small lede"><b>The types are canon's roles under their ruled names.</b>
      Display renders as <code>brochureware</code>, Gallery as <code>gallery</code>, Dashboard as
      <code>dashboard</code> &mdash; so every radius, spacing and squaring decision on this page is
      canon's own rule resolving (<code>s217-D2</code> / <code>s217-D3</code>), never a second copy
      of a ruled fact. The caption block is the ruled %dpx with its %d-line clamp derived back out
      of it. Console is the theme where the rounding options are visible, because it is the only
      theme whose radius token is non-zero &mdash; the grammar is the same in all four.</p>
    <p class="t-ed-body-small lede"><span class="bm-tag t-cm-legal">Proposed &mdash; not ruled</span>
      &nbsp;Everything beyond the ruling's own words is a conductor's reading of one of its five
      OPEN POINTS, marked <b>PROPOSED</b> here and on the control it governs. Dave's closing words
      on the matrix were <i>&ldquo;lets see this for now. this is a lot, you might want to check my
      logic&rdquo;</i> &mdash; so this page is an instrument for his eye, and nothing on it is
      promoted.</p>
  </section>

  <section id="controls">
    <div class="sublabel t-ed-caption">The matrix &mdash; %d reachable combinations in mono,
      legacy and supercharge; %d in <b>console</b>, where Gallery has no keyline control at all
      (<code>s217-D6</code>)</div>
    <div class="bm-controls">
      %s
    </div>
    <p class="bm-capt t-cm-legal" id="bm-moved"></p>

    <div class="bm-stage" id="bm-stage" data-type="display" data-spacing="24" data-keylines="on"
         data-page-bg="white" data-bento-bg="grey">
      <div class="bm-page-ground">

        <div class="bm-pane" data-pane="display">
          <p class="bm-capt t-cm-legal">DISPLAY &mdash; a sectioned marketing wall. The tiles carry
            the radius and the spacing (<code>s217-D3</code>), mixed panels and photographs.
            &mdash; At <b>Tight</b> a second wall appears <b>BELOW</b> this one with the
            stepped-down radius (P4). ⛔ <b>Stacked, never side by side.</b> Halving the container
            to hold two walls trips the responsive bands &mdash; each wall is its own
            container-query container &mdash; and Display tight would render a different
            composition from Display standard, which is not the comparison. Full width for both
            means the same band is in force on each and the only variable is the radius.
            ⚠ The two read as different only where the theme radius is non-zero, which
            today is <b>console</b>; in the other three both sides resolve to 0 and the pair is
            deliberately identical.</p>
          <div class="bm-pair">
            <div>
              <p class="bm-capt t-cm-legal">Standard tile radius (ruled)</p>
              <div class="c-bento bm-wall bm-display" data-bento-role="brochureware">
                <div class="c-bento__grid">
%s
                </div>
              </div>
            </div>
            <div class="bm-alt">
              <p class="bm-capt t-cm-legal">Stepped-down concentric radius
                <span class="bm-tag t-cm-legal">Proposed &mdash; P4</span></p>
              <div class="c-bento bm-wall bm-display bm-display-stepped"
                   data-bento-role="brochureware">
                <div class="c-bento__grid">
%s
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bm-pane" data-pane="gallery">
          <p class="bm-capt t-cm-legal">GALLERY &mdash; a page-level photography wall, all %d
            committed derivatives. <b>Gallery bento</b> uses canon's span grid with the bottom edge
            ragged or squared; <b>Justified rows</b> uses the row packing from
            <code>gen_gallery_compare_217.pack_rows</code>, the same arithmetic, imported.</p>
          <div class="c-bento bm-wall bm-gallery" data-bento-role="gallery">
            <div class="c-bento__grid">
%s
            </div>
          </div>
          <div class="c-bento bm-wall bm-just" data-bento-role="gallery">
%s
          </div>
        </div>

        <div class="bm-pane" data-pane="dashboard">
          <p class="bm-capt t-cm-legal">DASHBOARD &mdash; a bento of bentos. The theme radius sits
            on each inner bento's container and the tiles stay square (<code>s217-D2</code> /
            <code>s217-D3</code>); the main wall never goes tight.</p>
          <div class="c-bento bm-wall bm-outer" data-bento-role="dashboard">
            <div class="c-bento__grid">
%s
            </div>
          </div>

          <div class="bm-sp-strip" id="keyline-behaviour">
            <div class="bm-sp-intro">
              <h3 class="t-ed-body-small bm-sp-title">Keylines, ruled
                <span class="bm-tag t-cm-legal">s217-D8 &mdash; ruled</span></h3>
              <p class="t-cm-legal">⬛ <b>THE KEYLINE GOES ROUND THE MODULE.</b> Dave, #217:
                <i>&ldquo;the keylines should stay, but they should go round tight to the modules
                not run down the middle of the spacing&rdquo;</i>. The A&nbsp;/&nbsp;B&nbsp;/&nbsp;C
                decision spread that stood here is <b>retired</b> along with the centred-gutter
                construction it was offering &mdash; the question it existed to ask has an
                answer.</p>
            </div>
            <p class="bm-sp-open t-cm-legal">⬛ <b>ABOVE 1px &mdash; EVERY TILE WEARS ITS OWN TIGHT
              1px BOX, AND THE FOUR CORNER TILES CARRY THE SUB-BENTO'S RADIUS ON THEIR OUTER
              CORNER (#218, Dave's words: <i>&ldquo;the radii should only apply to the 4 corners
              of each sub bento&rdquo;</i>).</b> The group's outer border <b>steps back</b>: with
              the tiles carrying edges, a group frame would re-create the double frame rejected
              at #217. The tiles' own keylines draw the rounded silhouette &mdash; concentric with
              the container's clip, so nothing straight ever meets the curve, nothing is cropped,
              and the radius reads on any ground. No gutter carries anything, and the corner
              assignment moves with the responsive bands (minted per band from the browser's own
              placement).</p>
            <p class="bm-sp-note t-cm-legal">⛔ <b>AT THE 1px STOP, UNCHANGED.</b> 1px cannot hold a
              gap <i>and</i> a line, so flush tiles cannot carry their own boxes without doubling
              every seam. The group keeps its curved 1px border, the tiles sit flush, and the
              gutter <b>is</b> the hairline &mdash; stopped along the curve by the container's own
              clip. This is the only stop on the pane at which a line element renders at all.</p>
          </div>

          <div class="bm-sweep" id="sub-bento-sweep">
            <div class="bm-sp-intro">
              <h3 class="t-ed-body-small bm-sp-title">Sub-bento spacing under C &mdash; the whole
                ladder, at a glance
                <span class="bm-tag t-cm-legal">Proposed &mdash; not ruled</span></h3>
              <p class="t-cm-legal">Dave's question: <i>&ldquo;what happens with sub-bento
                spacing?&rdquo;</i> One group, drawn once at every ruled snap stop
                (<code>s217-D6</code>: 1 &middot; 2 &middot; 4 &middot; 8 &middot; 12 &middot; 16
                &middot; 20 &middot; 24), in the <b>ruled</b> construction
                (<code>s217-D8</code>). The keyline is always 1px and always <b>tight round the
                module</b>; what moves is the air between the boxes. The slider on the live wall
                above drives the same construction.</p>
              <p class="t-cm-legal">⬛ <b>AND HERE IS THE HONEST ANSWER, BEFORE YOU LOOK.</b> The
                <b>seam never changes weight</b>: it is 1px at every stop. What the slider moves is
                the <b>air between the boxes</b> and, with it, the group's height &mdash; the tiles
                grow apart while the tracks narrow by a pixel or two. So the ladder reads as a
                rhythm control, not as a line control. ⚠ One place to look hard: where two tiles
                sit side by side, the gutter shows <b>two tile edges with space between them</b>,
                which in the square themes is the heaviest seam on the wall &mdash; and it gets
                lighter, not heavier, as the gutter widens.</p>
              <p class="t-cm-legal">⛔ <b>Full width and stacked, never a row of thumbnails.</b>
                Every bento is a size container: eight walls side by side would each land near
                140px, trip canon's 520px band and collapse to one column, and the strip would be
                answering a question about responsive bands while claiming to answer one about
                spacing (<code>ds-054</code>, and Dave's own first #217 defect).</p>
              <p class="t-cm-legal">⛔ <b>THE 1px ROW IS THE OTHER REGIME, AND IT IS THE FIRST ROW
                OF THE STRIP.</b> Flush tiles cannot carry their own boxes without doubling every
                seam, so at 1px the group keeps its curved border and the gutter <b>is</b> the
                hairline, stopped along the curve by the container's own clip. Every other row
                shows the tile-hugging box with the group's border stepped back. Both regimes are
                driven and measured by <code>verify_bento_matrix_217.py</code> rather than trusted
                from this paragraph.</p>
            </div>
            <div class="bm-sw-strip">
              %s
            </div>

            <div class="bm-mw" id="main-wall-question">
              <div class="bm-sp-intro">
                <h3 class="t-ed-body-small bm-sp-title">And the main wall?
                  <span class="bm-tag t-cm-legal">Proposed &mdash; not ruled</span></h3>
                <p class="t-cm-legal">⬛ <b>PROPOSED: keylines live INSIDE groups only.</b> Every
                  module wears its box (<code>s217-D8</code>); the main wall's gutters between
                  groups stay line-free &mdash; space separates groups, boxes separate modules.</p>
                <p class="t-cm-legal">⛔ <b>The counter-example is retired.</b> It drew a hairline
                  down the middle of the main wall's gutter, which is the construction
                  <code>s217-D8</code> retires, and it needed an unclipped wrapper cell around
                  every group to do it at all &mdash; a group is a bento with
                  <code>overflow:hidden</code>, canon's dashboard role, where the clip is what
                  makes the container radius read. A retired picture kept on the page reads as a
                  live alternative, so it is gone rather than captioned.</p>
              </div>
              <div class="bm-mw-case">
                <p class="bm-sw-label t-cm-legal"><b>Proposed</b>&nbsp; keylines round the modules
                  inside each group; the main wall's gutter is space alone</p>
                <div class="bm-mw-ground">%s</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div class="bm-export">
      <div class="bm-exhead">
        <span class="bm-tag t-cm-legal">Export &mdash; proposed, not ruled</span>
        <span class="t-cm-legal">Concrete values, resolved in the theme and mode on screen
          (<code>s200-D1</code>) &mdash; no <code>var()</code> chain.</span>
        <button class="bm-btn t-cm-ctl-14" type="button" id="bm-rebuild">Rebuild export</button>
      </div>
      <pre><code id="bm-export" class="t-cm-legal"></code></pre>
    </div>
  </section>

  <section id="matrix">
    <h2 class="t-ed-heading-4">What is reachable, counted</h2>
    <p class="t-ed-body-small lede">Enumerated at build time from the same two legality rules the
      controls enforce, so the number below and the refusals in the browser cannot disagree.
      <b>Every reachable combination renders.</b> An option a ruling removes is ABSENT (dashboard
      main spacing carries no Tight button, and the bottom-edge dial exists only under Gallery
      bento); an option a legality rule refuses is PRESENT and disabled, with its reason.</p>
    <p class="t-ed-body-small lede">⛔ <b>THE COUNT IS THEME-DEPENDENT, AND ONE HEADLINE NUMBER
      WOULD BE A LIE IN ONE THEME OUT OF FOUR.</b> <code>s217-D6</code> removes the keyline control
      from <b>Gallery in the console theme</b> entirely &mdash; absent, not disabled, the same
      discipline as the dashboard's missing Tight button. So gallery has one keyline value in
      console (none) and two everywhere else, and the reachable total moves with the theme. Both
      numbers are counted from the same enumeration, per theme, and printed.</p>
    <div class="tablewrap">
      <table class="t-cm-legal">
        <thead><tr><th>Type</th><th>Reachable &mdash; mono / legacy / supercharge</th>
          <th>Reachable &mdash; console</th><th>Dimensions</th></tr></thead>
        <tbody>%s<tr><td><b>Total</b></td><td class="num"><b>%d</b></td>
          <td class="num"><b>%d</b></td><td></td></tr></tbody>
      </table>
    </div>
    <div class="tablewrap">
      <table class="t-cm-legal">
        <thead><tr><th>Theme</th><th>Display</th><th>Gallery</th><th>Dashboard</th>
          <th>Total</th></tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>
  </section>

  <section id="points" class="notes">
    <h2 class="t-ed-heading-4">The five open points, and what this page proposes</h2>
    <p class="t-ed-body-small"><code>s217-D5</code> names five open points and rules none of them.
      Each is implemented here as a PROPOSAL so Dave can rule by eye rather than from prose.</p>
    <ul class="t-ed-body-small">%s</ul>
  </section>

  <section id="notes" class="notes">
    <h2 class="t-ed-heading-4">What this page is, and is not</h2>
    <ul class="t-ed-body-small">
      <li><b>Nothing is re-drawn and nothing is re-derived.</b> The %d photographs are the
        committed web derivatives read through
        <code>gen_bento_roles_217.read_photos()</code>; the cards and panels are that module's own
        <code>CARDS</code> and <code>PANELS</code>; the justified rows are
        <code>gen_gallery_compare_217.pack_rows</code>. One data path, one packing maths.</li>
      <li><b>No bento structure is declared here.</b> The grid, the span vocabulary, the responsive
        bands, the three role rules and the caption space are canon's. What this page declares is
        instance dials (custom properties), tile content, the controller chrome, and the justified
        rows &mdash; which are not a grid and which canon has no grammar for.</li>
      <li><b>The ragged/square dial swaps canon's own span attributes</b>, because the squaring
        pass is a mint-time rewrite of spans. Both span sets are minted at build time and ride on
        each tile; the dial rewrites <code>data-c</code>/<code>data-r</code>. A second page-local
        span vocabulary would out-specify canon's container-query bands and break the collapse
        silently, at one width, in one theme.</li>
      <li>⬛ <b>A gallery tile paints no ground of its own &mdash; PROPOSED, and it is what makes
        the caption rule a real question.</b> The picture supplies its own ground, so a caption's
        immediate ground is the wall, which is the bento background the ruling names. Paint the
        tile instead and a white caption on a grey bento renders white-on-white while the rule
        calls it legal (measured, #217). A card or panel tile <i>does</i> keep a surface &mdash;
        the ruled 1px show-through needs something to show through of.</li>
      <li><b>No colour is authored.</b> Every ground is <code>--surface-subtle</code> (the lightest
        grey), <code>--surface-raised</code> (white) or nothing at all. The controller chrome is
        neutral only.</li>
      <li>⚠ <b>Measured, and it is Dave's to weigh:</b> in dark mode several themes resolve
        <code>--surface-subtle</code> and <code>--surface-raised</code> to the SAME value, so the
        grey/white distinction the palette offers collapses there while both remain legal by the
        rule. Surfaced, not fixed &mdash; a token change is not this page's to make.</li>
      <li><b>The squaring report is printed, not hidden.</b> Gallery-bento ragged is the gallery
        role's ruled default; square is <code>square_wall</code>, the ratified pass, run at this
        wall's own %s ladder.</li>
      <li>⛔ <b>The dashboard's OUTER wall runs the ruled squaring pass, and it did not before.</b>
        <code>s217-D3</code> rules squaring ON for the dashboard role, but this page wrote the
        three groups with a literal one-column span, so <code>square_wall_for_role</code> was never
        asked and three groups at two columns left the second row half empty &mdash; the orphan
        gap. Asked properly it reports <code>%s</code> at this wall's %s ladder, and the wall
        closes.</li>
      <li>⛔ <b>A nested bento used to be a rounded container taller than its own content.</b>
        Canon stretches a bento that is a tile of another bento so a row of groups reads as one
        band; its own grid has fixed rows, is top-aligned, and did not grow with it. The moment two
        groups in a row had different natural heights, the shorter one carried a dead band under
        its last tile &mdash; a rounded top and a FLAT BOTTOM, measured here as a 360px cell
        holding a 240px grid. Fixed in <b>canon</b>, where the stretch lives, not patched here.</li>
      <li><b>The role table is canon's:</b> %s.</li>
    </ul>
  </section>
""" % (space, lines, total, console_total, controls(), disp, disp, len(photos), gal, just, dash,
       sweep_html(), mainwall_html(),
       counts_rows, total, console_total, theme_rows, points_html, len(photos),
       "/".join(str(x) for x in c["gal_ladder"]),
       esc(json.dumps(c["dash_report"].get("changed"))),
       "/".join(str(x) for x in c["dash_ladder"]),
       ", ".join("%s (radius on the %s)" % (k, r[k]["radius"])
                 for k in sorted(k for k in r if not k.startswith("$"))))


def page(shell, c=None):
    """-> the whole HTML page. `shell` is gen_foundations_217.shell — the ONE page shell."""
    c = c or content()
    sub_rules = "\n".join(
        '.bm-stage[data-sub-spacing="%d"] .bm-inner.c-bento[data-bento-role="dashboard"]'
        '{--bento-gutter:%dpx;}' % (s, s) for s in SUB_STOPS)
    sweep_rules = "\n".join(
        '.bm-sw-row[data-stop="%d"] .bm-sw-inner.c-bento[data-bento-role="dashboard"]'
        '{--bento-gutter:%dpx;}' % (s, s) for s in SUB_STOPS)
    css = (CSS.replace("__PHOTO_RULES__", photo_rules(c["photos"]))
              .replace("__SUB_SPACING_RULES__", sub_rules)
              .replace("__SWEEP_STOP_RULES__", sweep_rules)
              # ⬛ #218 — corner keylines; the layout arm ships the block EMPTY so the corner
              # assertion in verify_bento_matrix_217.py goes RED by name (Dave's symptom back:
              # square boxes everywhere, the radius invisible).
              .replace("__CORNER_RULES__",
                       "/* ⛔ ARM: #218 corner rules STRIPPED */" if BREAK_LAYOUT
                       else corner_rules(c["dash_inner"]))
              .replace("__GALLERY_COLS__", str(GALLERY_COLS))
              .replace("__DISPLAY_COLS__", str(DISPLAY_COLS))
              .replace("__DASH_COLS__", str(DASH_COLS))
              .replace("__INNER_COLS__", str(INNER_COLS)))
    if BREAK_LAYOUT:
        # ⬛ ARM: the halved container is back. The walls now answer the 820px band and Display
        # tight renders a DIFFERENT COMPOSITION from Display standard — the shape of the defect.
        css = css.replace(".bm-pair{display:flex; flex-direction:column;",
                          ".bm-pair{display:grid; "
                          "grid-template-columns:repeat(auto-fit,minmax(320px,1fr));")
        # ⬛ ARM, THIRD SYMPTOM: canon's nested-bento FILL is undone from the page side, so the
        # dead band comes back without touching canon.css. Without this the flat-bottom assertion
        # would never have been seen to fail, and an assertion that cannot fail is not a gate
        # ([[instrument-without-a-consumer]]). This is the EXACT pre-fix declaration.
        css += ("\n/* ⬛ MUTATION ARM — canon's nested-bento fill removed. */\n"
                ".bm-inner.c-bento.c-bento__tile > .c-bento__grid{"
                "flex:0 0 auto; grid-auto-rows:var(--bento-row-unit);}\n")
        # ⬛ ARM, FOURTH SYMPTOM: THE CROPPED KEYLINE IS BACK (Dave, #217, "the corners are cropped
        # so that the keylines are also cropped"). The group draws no edge of its own and the TILES
        # draw right/bottom INSET hairlines, so the last column and last row paint the group's outer
        # edge — inside the tile, where the rounded clip cannot help — and every corner reads with
        # chopped line-ends. At the open stops the tiles go back to sitting flush against the curve.
        # This is the EXACT pre-fix declaration, appended last so it wins on order at equal weight.
        # ⚠ AND IT TAKES THE HAIRLINES AWAY TOO, or the arm would be a page carrying BOTH
        # constructions and the pre-fix assertions could pass on C's lines instead of failing.
        css += ("\n/* ⬛ MUTATION ARM — the pre-fix keyline emission for the dashboard role. */\n"
                '.bm-stage[data-keylines="on"] .bm-inner.c-bento[data-bento-role="dashboard"]'
                "{border:0;}\n"
                '.bm-stage[data-keylines="on"] .bm-inner > .c-bento__grid > .bm-tile'
                " > .bm-gapline{display:none;}\n"
                '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"])'
                ' .bm-inner.c-bento[data-bento-role="dashboard"]{--bento-outer-padding:0px;}\n'
                '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-inner'
                " > .c-bento__grid > .bm-tile{border:1px solid var(--bm-line,#D7D8D6);}\n"
                '.bm-stage[data-sub-spacing="1"][data-keylines="on"]'
                ' .bm-inner.c-bento[data-bento-role="dashboard"]{--bento-gutter:0px;}\n'
                '.bm-stage[data-sub-spacing="1"][data-keylines="on"] .bm-inner'
                " > .c-bento__grid > .bm-tile{"
                "box-shadow:inset -1px 0 0 0 var(--bm-line,#D7D8D6),"
                "inset 0 -1px 0 0 var(--bm-line,#D7D8D6);}\n")
        # ⬛ ARM, FIFTH SYMPTOM: THE KEYLINE NOTE IS UNGATED (#217, second pass; the ruled note
        # inherits the arm the retired spread had). The strip is shown whatever the dials say, and
        # BOTH regime notes stand at the 1px stop — so the page describes two constructions at
        # once, one of which the wall is not drawing. Without this, the gate assertions could never
        # be seen to go red, and a gate that cannot fail is not a gate
        # ([[instrument-without-a-consumer]]).
        css += ("\n/* ⬛ MUTATION ARM — the ruled keyline note, ungated. */\n"
                ".bm-stage .bm-sp-strip{display:block;}\n"
                '.bm-stage[data-sub-spacing="1"] .bm-sp-open{display:block;}\n')
        # ⛔ THE SIXTH SYMPTOM IS RETIRED WITH ITS SUBJECT (s217-D8). It restored the
        # band-assuming axis suppression on the MAIN-WALL COUNTER-EXAMPLE — a hairline down the
        # middle of the main wall's gutter — and that counter-example is gone from the page. An arm
        # over a construction the page no longer draws is an arm that cannot be run.
    if BREAK_KEYLINES:
        # ⬛ ARM (s217-D8): THE CENTRED GUTTER LINE IS BACK ON THE LIVE WALL AT THE OPEN STOPS.
        # This is the EXACT retired declaration — the tiles go bare, the group keeps its own border
        # with zero outer padding, and the hairline pair renders centred in every gutter. Appended
        # last so it wins on order at equal weight.
        css += ("\n/* ⬛ MUTATION ARM — the RETIRED centred-gutter construction, restored. */\n"
                '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"])'
                ' .bm-inner.c-bento[data-bento-role="dashboard"]'
                "{border:1px solid var(--bm-line,#D7D8D6); --bento-outer-padding:0px;}\n"
                '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-inner'
                " > .c-bento__grid > .bm-tile"
                "{border:0; box-shadow:none; overflow:visible; position:relative;}\n"
                '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-inner'
                " > .c-bento__grid > .bm-tile > .bm-gapline{display:block;}\n")
    js = (SCRIPT.replace("__LEGALITY_BODY__",
                         LEGALITY_JS_BROKEN if BREAK_LEGALITY else LEGALITY_JS_REAL)
                .replace("__SUB_STOPS__", json.dumps(SUB_STOPS))
                .replace("__KEYLINE_EXCLUDED__",
                         json.dumps([list(x) for x in KEYLINE_EXCLUDED])))
    return shell("Bento — Apollo library (Foundations)", "Bento",
                 "Foundations &middot; the s217-D5 option matrix &middot; PROPOSED, not ruled",
                 body(c), extra_css=css, extra_script=js, extra_class="bm")


# ---------------------------------------------------------------------------- selftest
def selftest():
    fails, ran = [], []

    def bite(name, got, want):
        ran.append(name)
        if got != want:
            fails.append("%s\n     got:  %r\n     want: %r" % (name, got, want))

    c = content()
    import gen_foundations_217 as f
    html = page(f.shell, c)

    bite("1 · the three TYPES map onto canon's three ROLES — the rename is a word, not a grammar",
         sorted(TYPE_ROLE.values()),
         sorted(k for k in roles() if not k.startswith("$")))
    bite("2 · dashboard MAIN spacing has NO tight member — ruled out, so ABSENT not disabled",
         [s[0] for s in DASH_MAIN], ["24", "40"])
    # ⬛ s217-D6 — the sub-bento control is a SNAPPING SLIDER now, not three buttons.
    bite("3 · sub-bento spacing is a SLIDER over the ruled ladder, driven in pixels",
         ('data-dial="subSpacing"' in html,
          'class="bm-range"' in html,
          'min="1"' in html and 'max="24"' in html and 'step="1"' in html,
          all('<option value="%d" label="%d">' % (s, s) in html for s in SUB_STOPS),
          'data-value="40"' in html.split('data-dial="subSpacing"', 1)[1].split("</div>", 1)[0]),
         (True, True, True, True, False))
    # hand-computed against the DECLARED tie-break ("ties go to the LOWER stop"), never read back.
    bite("3b · the snap lands on a STOP from anywhere — midpoints, ends and off the ends",
         [snap(0), snap(1), snap(3), snap(6), snap(7), snap(10), snap(14), snap(22), snap(99)],
         [1, 1, 2, 4, 8, 8, 12, 20, 24])
    bite("3b2 · every integer across the range snaps ONTO the ladder, none between",
         sorted({snap(x) for x in range(0, 40)}), SUB_STOPS)
    bite("3c · every stop has a DECLARED gutter rule — the CSS is the whole vocabulary",
         [('[data-sub-spacing="%d"]' % s) in html and ("--bento-gutter:%dpx" % s) in html
          for s in SUB_STOPS], [True] * len(SUB_STOPS))
    bite("3d · the JS snap ladder is the SAME list, not a second copy that can drift",
         json.dumps(SUB_STOPS) in html, True)
    # P2/P3 hand-computed against the ruling, never read back from the function under test.
    bite("4 · P2 — a caption may not sit on its own colour; transparent is always legal",
         [caption_legal("white", "white"), caption_legal("grey", "grey"),
          caption_legal("white", "grey"), caption_legal("transparent", "transparent")],
         [False, False, True, True])
    bite("5 · P3 — a capsule needs a caption background OR keylines",
         [capsule_legal("capsule", "transparent", "off"),
          capsule_legal("capsule", "transparent", "on"),
          capsule_legal("capsule", "white", "off"),
          capsule_legal("corners", "transparent", "off")],
         [False, True, True, True])
    counts = matrix_counts("mono")
    bite("6 · the reachable matrix is the hand-computed one",
         (counts["display"], counts["dashboard"]),
         (3 * 2 * 3 * 3, 2 * len(SUB_STOPS) * 2 * 3 * 3))
    # gallery, computed by hand from the ruling: 3 spacing x 2 keylines x 3 modes x
    # (rounding x caption/bento pairs, minus the two refusals) x 3 page grounds.
    legal_pairs = sum(1 for cb in ("grey", "white", "transparent")
                      for bb in ("grey", "white", "transparent") if caption_legal(cb, bb))
    illegal_capsule = sum(1 for kl in ("on", "off")
                          for cb in ("grey", "white", "transparent")
                          for bb in ("grey", "white", "transparent")
                          if caption_legal(cb, bb) and not capsule_legal("capsule", cb, kl))
    bite("7 · gallery's reachable count equals the legality rules applied by hand",
         counts["gallery"],
         3 * 2 * 3 * (2 * legal_pairs) * 3 - 3 * 3 * 3 * illegal_capsule)
    # ⛔ NO STATE THAT RENDERS NOTHING: every enumerated combination must name a pane that exists
    # and a mode whose markup is on the page.
    panes = [p for p in ("display", "gallery", "dashboard")
             if 'data-pane="%s"' % p in html]
    bite("8 · every type in the matrix has a pane on the page", sorted(panes),
         sorted(enumerate_matrix("mono")))
    # ⬛ s217-D6 — GALLERY IN CONSOLE HAS NO KEYLINE OPTION. Hand-computed: the keyline dimension
    # drops from 2 to 1, and with keylines pinned OFF the capsule rule (P3) refuses every
    # transparent-caption combination instead of half of them.
    con = matrix_counts("console")
    legal_pairs_c = sum(1 for cb in ("grey", "white", "transparent")
                        for bb in ("grey", "white", "transparent") if caption_legal(cb, bb))
    bite("8b · gallery-in-console is counted with ONE keyline value, and the other types are not",
         (con["gallery"],
          con["display"] == counts["display"], con["dashboard"] == counts["dashboard"]),
         (3 * 1 * 3 * (2 * legal_pairs_c) * 3 - 3 * 3 * 3 * 3, True, True))
    bite("8c · the console total genuinely differs — the page cannot print ONE headline number",
         sum(con.values()) != sum(counts.values()), True)
    bite("8d · the page PRINTS both totals, so the theme-dependence is on its face",
         (str(sum(counts.values())) in html, str(sum(con.values())) in html,
          "console" in html.split('id="matrix"', 1)[1][:2000]), (True, True, True))
    bite("8e · the three unexcluded themes agree with one another",
         len({sum(matrix_counts(t).values()) for t in ("mono", "legacy", "supercharge")}), 1)
    bite("9 · both gallery modes have markup — neither can select into an empty stage",
         ("bm-just" in html and "bm-gallery" in html and "bm-jrow" in html), True)
    bite("10 · both span sets ride on every gallery tile, so the edge dial can never blank a wall",
         (html.count('data-ragged="'), html.count('data-square="')),
         (len(c["photos"]), len(c["photos"])))
    # ⚠ THE SECOND STYLE BLOCK, deliberately. The first is the shared Foundations stylesheet,
    # which this module does not own and must not be judged for; the second is this page's own.
    css = html.split("<style>")[2].split("</style>", 1)[0]
    import re as _re
    rules = _re.sub(r"/\*.*?\*/", "", css, flags=_re.S)
    declared = set(_re.findall(r"(--[a-z0-9-]+)\s*:", rules))
    bare = sorted({m for m in _re.findall(r"var\((--[a-z0-9-]+)\s*\)", rules)
                   if m not in declared})
    bite("11 · ⛔ no foreign var() without a literal fallback (silent-black class)", bare, [])
    hexes = sorted({x.upper() for x in _re.findall(r"#[0-9A-Fa-f]{6}", rules)})
    chromatic = [x for x in hexes
                 if max(int(x[1:3], 16), int(x[3:5], 16), int(x[5:7], 16))
                 - min(int(x[1:3], 16), int(x[3:5], 16), int(x[5:7], 16)) > 8]
    bite("12 · every authored colour is a NEUTRAL — no red, no yellow, no green in the chrome",
         (chromatic, "#000000" in hexes), ([], False))
    # the page must not re-declare bento STRUCTURE (s217-D2 owns it)
    structure = [sel.strip() for sel, decls in _re.findall(r"([^{}]+)\{([^{}]*)\}", rules)
                 if "c-bento" in sel
                 and _re.search(r"grid-template-columns|grid-auto-rows|grid-auto-flow", decls)]
    bite("13 · no bento STRUCTURE is declared here — canon owns the grid", structure, [])
    # ⛔ THE CLASS FIX FOR DAVE'S FIRST DEFECT, AS A GATE RATHER THAN A CORRECTION.
    # NOTHING IN THE EXPLORER MAY PRESENT A COMPARISON BY SHRINKING THE CONTAINER A BAND RESPONDS
    # TO. Every `.c-bento` is `container-type:inline-size`, so a wall in a half-width column
    # answers a different band than the same wall full width, and Display TIGHT rendered a
    # different composition from Display standard. The rule the page must keep is structural: no
    # ancestor of a `.bm-wall` may declare a multi-track column axis. Probed by reading the
    # page's OWN stylesheet, so a future side-by-side re-introduces the defect only over a red.
    multicol = []
    for sel, decls in _re.findall(r"([^{}]+)\{([^{}]*)\}", rules):
        s, d = sel.strip(), decls
        if not s.startswith(".bm-pair") and "bm-pair" not in s and ".bm-stack" not in s:
            continue
        m = _re.search(r"grid-template-columns\s*:([^;]*)", d)
        if m and "1fr" in m.group(1) and "repeat" in m.group(1):
            multicol.append(s)
    bite("13b · ⛔ the P4 comparison is STACKED — no multi-track column axis may hold a bento wall",
         (multicol, "flex-direction:column" in rules.split(".bm-pair{", 1)[1][:120]), ([], True))
    # ⛔ THE DASHBOARD OUTER WALL RUNS THE RULED SQUARING PASS (s217-D3). The literal span this
    # replaces is what left the orphan cell; the assertion is that the pass RAN and MOVED a span,
    # not that a function was imported.
    bite("13c · ⛔ the dashboard OUTER wall's spans come from square_wall_for_role, and it moved",
         (c["dash_report"].get("squared"), c["dash_report"].get("exempt"),
          bool(c["dash_report"].get("changed")), c["dash_spans"] != [(1, 1)] * 3),
         (True, False, True, True))
    from gen_canon_bento import place as _place
    _rows, _holes, _ = _place(c["dash_spans"], DASH_COLS)
    bite("13d · ⛔ and the squared dashboard wall has ZERO empty cells at its own column count",
         _holes, 0)
    # ---------------------------------------------------------- ✅ s217-D7 · THE NESTED PASS
    # ⛔ THE DEFECT REPRODUCED FIRST, so the bite below proves a FIX and not a coincidence: the
    # third group's authored spans (2x1, 1x1, 1x1) leave two empty cells in three tracks.
    _auth3 = [(min(cc, INNER_COLS), rr) for (_l, _s, _f, cc, rr) in c["dash_cards"][2]]
    bite("13e · the measured inner-group defect is REPRODUCIBLE from the authored spans",
         (_auth3, is_rectangular(_auth3, inner_ladder(INNER_COLS))[0],
          _place(_auth3, INNER_COLS)[1]),
         ([(2, 1), (1, 1), (1, 1)], False, 2))
    bite("13f · ✅ s217-D7 — EVERY inner group squares at the inner ladder, zero empty cells",
         ([_place(g, INNER_COLS)[1] for g in c["dash_inner"]],
          [is_rectangular(g, inner_ladder(INNER_COLS))[0] for g in c["dash_inner"]]),
         ([0, 0, 0], [True, True, True]))
    bite("13g · the nested pass was asked in ONE call and refused nothing",
         (c["nested_report"]["squared"], c["nested_report"]["refusals"],
          len(c["nested_report"]["inner"])), (True, [], 3))
    # ⛔ AND EVERY OTHER NESTED WALL ON THE PAGE, not just the live one — the sweep and the
    # main-wall groups are inner dashboards too, and each went through the authored literal.
    # ⚠ THE SPREAD'S TWO WALLS ARE GONE FROM THIS LIST because the spread is (s217-D8), not
    # because the pass stopped being asked of them.
    bite("13h · every nested wall the page mints went through the pass and squares",
         (sorted({r["wall"] for r in INNER_SQUARE_REPORTS if r.get("wall")}),
          [r["squared"] for r in INNER_SQUARE_REPORTS]),
         (["main-wall group 1", "main-wall group 2", "spacing sweep"],
          [True] * len(INNER_SQUARE_REPORTS)))
    bite("13i · ⛔ card_tile REFUSES to draw without a minted span — the class fix, not a habit",
         (card_tile.__code__.co_argcount, card_tile.__defaults__), (3, (True,)))
    bite("14 · ONE state object: the export is rendered from STATE, never from the DOM's dials",
         ("__BM_STATE" in html and "JSON.stringify(payload" in html
          and html.count("var STATE = {") == 1), True)
    bite("15 · the mutation handle actually removes the rules it claims to remove",
         ("bentoBg" in LEGALITY_JS_REAL, "bentoBg" in LEGALITY_JS_BROKEN), (True, False))
    bite("16 · the ruled backgrounds resolve through TOKENS, never a literal grey",
         (["--surface-subtle" in rules, "--surface-raised" in rules],
          "#F0F0F0" in rules.split("--bm-grey:", 1)[1][:60]),
         ([True, True], True))
    bite("17 · every photograph in the ONE data path reached the gallery wall",
         all(p["file"] in html for p in c["photos"]), True)
    bite("18 · the five open points are each labelled PROPOSED on the page",
         (html.count("Proposed") >= 5, "P4" in html and "P1" in html), (True, True))
    bite("19 · residuals are declared, never defaulted away",
         c["residuals"].get("missing_derivative_file"), [])
    # ------------------------------------------- the RULED keyline behaviour (s217-D8, #217)
    # ⛔ THE BITES THAT ASSERTED THE RETIRED CONSTRUCTION ARE GONE, AND THEY ARE NAMED HERE RATHER
    # THAN QUIETLY DROPPED: 20 / 20a / 20b / 20c / 20d / 20e / 20f / 20g / 20h asserted the A/B/C
    # decision spread — three treatments on the page, each labelled, pairwise distinct in the
    # stylesheet, gap lines only in C. s217-D8 answered the question the spread asked, so the
    # spread and every assertion over it is retired with it. What replaces them asserts the RULED
    # construction and the absence of the retired one.
    # ⚠ NORMALISED AND ACCUMULATED, not a plain dict comprehension. A selector wrapped over two
    # source lines carries a newline and would never match a typed key, and TWO rules may share a
    # selector (a stop's declared gutter and its construction) — a plain dict keeps only the last
    # and the assertion would read an absence that is not one. MEASURED here at the 1px sweep row.
    _decl = {}
    for _sel, _dec in _re.findall(r"([^{}]+)\{([^{}]*)\}", rules):
        _k = _re.sub(r"\s+", " ", _sel).strip()
        _decl[_k] = _decl.get(_k, "") + _dec
    bite("20 · ⛔ the A/B/C decision spread is GONE from the page — a settled question keeps no "
         "decision surface, and a retired construction keeps no specimen",
         ("data-treat=" in html, "bm-sp-case" in html, "bm-spread" in html,
          "bm-sp-letter" in rules),
         (False, False, False, False))
    bite("20a · the ruled note is in its place, conditional on the SAME two dials, and it names "
         "the ruling",
         ('id="keyline-behaviour"' in html, "s217-D8" in html,
          '.bm-stage[data-type="dashboard"][data-keylines="on"] .bm-sp-strip' in rules),
         (True, True, True))
    bite("20b · exactly one regime note is reachable at a time — open above 1px, flush at 1px",
         ('.bm-stage[data-sub-spacing="1"] .bm-sp-note{display:block;}' in rules,
          '.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) '
          '.bm-sp-open{display:block;}' in rules,
          "display:none" in _decl.get(".bm-sp-open, .bm-sp-note", "")),
         (True, True, True))
    _open_group = ('.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) '
                   '.bm-inner.c-bento[data-bento-role="dashboard"]')
    _open_tile = ('.bm-stage[data-keylines="on"]:not([data-sub-spacing="1"]) .bm-inner '
                  '> .c-bento__grid > .bm-tile')
    _flush_group = ('.bm-stage[data-keylines="on"][data-sub-spacing="1"] '
                    '.bm-inner.c-bento[data-bento-role="dashboard"]')
    _flush_tile = ('.bm-stage[data-keylines="on"][data-sub-spacing="1"] .bm-inner '
                   '> .c-bento__grid > .bm-tile')
    bite("20c · ⬛ s217-D8 + #218 ABOVE 1px — the TILE wears the box, the GROUP border steps "
         "back, and the outer padding is GONE (#218: the corner tiles carry the radius, so the "
         "gutter-inset that protected the curve is retired)",
         ("border:1px solid" in _decl.get(_open_tile, ""),
          "border:0" in _decl.get(_open_group, ""),
          "--bento-outer-padding:0px" in _decl.get(_open_group, ""),
          "--bento-outer-padding:var(--bento-gutter" not in _decl.get(_open_group, ""),
          "display:none" in _decl.get(_open_tile + " > .bm-gapline", "")),
         (True, True, True, True, True))
    # ⬛ #218 · CORNER KEYLINES — hand-computed fixture, never the generator's own output as its
    # own expectation. Fixture wall: [(2,1),(1,1),(1,1)] at 3 cols places t0 across the top,
    # t1 top-right, t2 alone on row 2 (ragged on purpose: the empty BR cell must assign NOTHING).
    # At 1 col everything stacks: t0 takes both top corners, t2 both bottom corners.
    _cm3 = corner_map([(2, 1), (1, 1), (1, 1)], 3)
    _cm1 = corner_map([(2, 1), (1, 1), (1, 1)], 1)
    bite("20c2 · ⬛ #218 corner assignment — 3-col fixture: t0 TL, t1 TR, t2 BL, BR unassigned "
         "(ragged hole assigns nothing)",
         (_cm3[0], _cm3[1], _cm3[2]),
         ({"top-left"}, {"top-right"}, {"bottom-left"}))
    bite("20c3 · ⬛ #218 corner assignment — 1-col band re-seats the corners: t0 both top, "
         "t2 both bottom (a static assignment would round the wrong tile here)",
         (_cm1[0], _cm1[1], _cm1[2]),
         ({"top-left", "top-right"}, set(), {"bottom-left", "bottom-right"}))
    _cr = corner_rules([[(2, 1), (1, 1), (1, 1)]])
    bite("20c4 · ⬛ #218 corner CSS — per-band blocks emitted (base + 820 + 520 mirroring "
         "canon's compiled $bands), every declaration explicit, radius from canon's own token, "
         "scoped to the LIVE wall at open stops only",
         ("@container bento (max-width:820px)" in _cr,
          "@container bento (max-width:520px)" in _cr,
          "border-top-left-radius:var(--bento-radius,0px)" in _cr,
          ':not([data-sub-spacing="1"])' in _cr and ".bm-outer > " in _cr,
          _cr.count("border-bottom-right-radius:0")),
         (True, True, True, True, 7))
    bite("20d · ⬛ s217-D8 AT 1px — unchanged: the group keeps its border, the tiles go bare and "
         "the gutter IS the hairline",
         ("border:1px solid" in _decl.get(_flush_group, ""),
          "--bento-outer-padding:0px" in _decl.get(_flush_group, ""),
          "border:0" in _decl.get(_flush_tile, ""),
          "display:block" in _decl.get(_flush_tile + " > .bm-gapline", "")),
         (True, True, True, True))
    # ⛔ THE ABSENCE, DECLARED RATHER THAN INFERRED. Every rule that turns a gap line ON is listed,
    # and the list must contain nothing but the two 1px consumers: the live wall and the sweep's
    # 1px row. A third would be a gutter carrying a line at an open stop.
    _line_on = sorted(_re.sub(r"\s+", " ", sel).strip()
                      for sel, decls in _re.findall(r"([^{}]+)\{([^{}]*)\}", rules)
                      if "bm-gapline" in sel and "display:block" in decls)
    bite("20e · ⛔ NO LINE IN ANY GUTTER ABOVE 1px — every rule that shows a gap line is a 1px "
         "consumer, and there are exactly two",
         _line_on,
         [_flush_tile + " > .bm-gapline",
          '.bm-sw-row[data-stop="1"] .bm-sw-inner > .c-bento__grid > .bm-tile > .bm-gapline'])
    bite("20f · the retired centred construction has a MUTATION ARM, so its absence is a gate "
         "that can be seen to fail",
         ("--break-keylines" in __doc__, "BREAK_KEYLINES" in rules), (True, False))
    # ------------------------------ ⬛ #217 · THE 1px HAIRLINE, THE SWEEP, THE MAIN WALL
    # ⛔ THE HAIRLINE OFFSET IS (gutter + 1px)/2 AND IT IS ASSERTED AS A STRING, because the half
    # pixel is the whole finding: `gutter/2` puts a 1px line's CENTRE at (g-1)/2, half a pixel off
    # centre, and it is also what stops the 1px stop converging on the ruled flush band.
    bite("21 · ⛔ the hairline sits at (gutter + 1px)/2 — at g=1 that is the WHOLE 1px gutter, "
         "which is what makes the flush stop flush",
         ("calc((var(--bento-gutter,24px) + 1px) / -2)" in rules,
          "calc(var(--bento-gutter,24px) / -2)" in rules),
         (True, False))
    # ⚠ COUNTED ON THE DECLARATIONS, not on the selector text — the display toggles name the axis
    # too, and counting selectors reported two copies of a geometry declared once (measured).
    _geo = [sel.strip() for sel, decls in _re.findall(r"([^{}]+)\{([^{}]*)\}", rules)
            if "bm-gapline" in sel and "calc((var(--bento-gutter" in decls]
    bite("21a · the geometry is declared ONCE per axis and read by every consumer — no second copy",
         (len(_geo), sorted(_geo)),
         (2, ['.bm-gapline[data-axis="h"]', '.bm-gapline[data-axis="v"]']))
    # ⛔ RETIRED HERE TOO, AND NAMED: bite 22 asserted "the live dashboard wall draws C — bare
    # tiles, gap lines, zero outer padding, and NO rule anywhere carrying a gutter-wide outer
    # padding", and 22a asserted that no sub-spacing stop drew a tile keyline box. Both asserted
    # the retired construction; s217-D8 inverts them, and bites 20c–20e above are the inversion.
    bite("22 · ⛔ the live wall's OPEN stops draw a tile box at every ruled stop above 1px",
         sorted({st for st in SUB_STOPS if st != 1
                 if ('[data-sub-spacing="%d"]' % st) in rules}),
         [st for st in SUB_STOPS if st != 1])
    # ⬛ THE SWEEP — every ruled stop, once, with a declared gutter rule and a printed label.
    bite("23 · the sweep draws one row per RULED stop, each labelled with its pixel value",
         ([('.bm-sw-row[data-stop="%d"]' % s) in html for s in SUB_STOPS],
          [('<b>%dpx</b>' % s) in html for s in SUB_STOPS],
          html.count('class="bm-sw-row"')),
         ([True] * len(SUB_STOPS), [True] * len(SUB_STOPS), len(SUB_STOPS)))
    bite("23a · every sweep stop has a DECLARED gutter rule — the CSS is the whole vocabulary",
         [('.bm-sw-row[data-stop="%d"] .bm-sw-inner' % s) in rules
          and ("--bento-gutter:%dpx" % s) in rules for s in SUB_STOPS],
         [True] * len(SUB_STOPS))
    # ⛔ RETIRED: bite 23b asserted a NINTH row — the pre-C flush construction drawn as a CONTROL
    # beside C at the 1px stop, so the convergence of the two could be differenced. With C retired
    # there is nothing to converge on; the strip's own 1px row IS the flush construction.
    bite("23b · ⬛ s217-D8 — the sweep draws tile boxes at every open stop and the FLUSH "
         "construction at 1px; the retired control row is gone",
         ("bm-sw-flush" in html or "bm-sw-ref" in html,
          "border:1px solid" in _decl.get(".bm-sw-inner > .c-bento__grid > .bm-tile", ""),
          "border:0" in _decl.get('.bm-sw-inner.c-bento[data-bento-role="dashboard"]', ""),
          "border:1px solid" in _decl.get(
              '.bm-sw-row[data-stop="1"] .bm-sw-inner.c-bento[data-bento-role="dashboard"]', ""),
          "border:0" in _decl.get(
              '.bm-sw-row[data-stop="1"] .bm-sw-inner > .c-bento__grid > .bm-tile', "")),
         (False, True, True, True, True))
    # ⛔ ds-054 — the sweep may not shrink a container a band answers.
    sw_multicol = [sel.strip() for sel, decls in _re.findall(r"([^{}]+)\{([^{}]*)\}", rules)
                   if ("bm-sw-strip" in sel or "bm-sweep" in sel)
                   and _re.search(r"grid-template-columns|flex-direction\s*:\s*row", decls)]
    bite("23c · ⛔ the sweep is STACKED FULL WIDTH — ds-054, a band-answering container is never "
         "shrunk to make a comparison",
         (sw_multicol, "flex-direction:column" in rules.split(".bm-sw-strip{", 1)[1][:120]),
         ([], True))
    # ⬛ THE MAIN-WALL QUESTION — the proposal alone. ⛔ RETIRED: bite 24 asserted the PAIR (the
    # proposal and its lined counter-example) and 24a asserted the `.bm-mw-lined` rule that drew a
    # hairline down the middle of the main wall's gutter. That is the construction s217-D8 retires.
    bite("24 · the main-wall proposal stands ALONE — the lined counter-example is retired",
         (html.count('class="bm-mw-case"'), "bm-mw-lined" in html, "bm-mw-lined" in rules,
          mainwall_html().count("bm-gapline")),
         (1, False, False, 0))
    bite("24a · ⛔ the main wall's own gutters are line-free, and its groups wear the ruled boxes",
         ('.bm-stage .bm-outer > .c-bento__grid > .c-bento > .bm-gapline{display:none;}' in rules,
          "border:1px solid" in _decl.get(".bm-mw-group > .c-bento__grid > .bm-tile", ""),
          "border:0" in _decl.get('.bm-mw-group.c-bento[data-bento-role="dashboard"]', ""),
          "display:none" in _decl.get(
              ".bm-mw-group > .c-bento__grid > .bm-tile > .bm-gapline", "")),
         (True, True, True, True))

    if fails:
        print("gen_bento_matrix_217 --selftest: %d BITE(S) FAILED" % len(fails))
        for x in fails:
            print("  ❌ " + x)
        sys.exit(1)
    print("gen_bento_matrix_217 --selftest OK — %d bites." % len(ran))
    for t in THEMES:
        cc = matrix_counts(t)
        print("   reachable %-12s %s (total %d)%s"
              % (t, cc, sum(cc.values()),
                 "   ⬛ gallery keylines EXCLUDED (s217-D6)"
                 if ("gallery", t) in KEYLINE_EXCLUDED else ""))
    print("   dashboard squaring (s217-D3): spans %s · %s"
          % (c["dash_spans"], c["dash_report"].get("changed")))
    print("   content: %d photograph(s), %d display tile(s), %d card(s), %d justified row(s) "
          "+ %d widow(s)" % (len(c["photos"]), len(c["display"]), len(CARDS), len(c["rows"]),
                             len(c["widows"])))


def main():
    global BREAK_LEGALITY, BREAK_LAYOUT, BREAK_INNER, BREAK_KEYLINES, UP
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()
    if "--break-keylines" in argv:
        # ⬛ THE FOURTH MUTATION ARM (s217-D8). NON-REPO by construction, same discipline as the
        # other three. ONLY the dashboard keyline construction is reverted to the retired centred
        # gutter line, so the s217-D8 assertions must go red ON THEIR OWN NAME.
        outdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")  # #218: shared-/var/tmp class fix
        for i, a in enumerate(argv):
            if a == "--out":
                outdir = argv[i + 1]
        BREAK_KEYLINES = True
        UP = "file://" + ROOT + "/"
        import gen_foundations_217 as f
        target = os.path.join(outdir, "bento-matrix-KEYLINE-BROKEN.html")
        html = page(f.shell).replace('href="../../knowledge/',
                                     'href="file://%s/knowledge/' % ROOT)
        open(target, "w", encoding="utf-8").write(html)
        print("⬛ MUTATION ARM written (NON-REPO): %s" % target)
        print("   the RETIRED centred-gutter keyline is back at the open stops — the s217-D8 "
              "assertions must go RED by name.")
        return 0
    if "--break-inner" in argv:
        # ⬛ THE THIRD MUTATION ARM (s217-D7). NON-REPO by construction, same discipline as the
        # other two. ONLY the nested pass is disabled — the outer wall stays squared, so the
        # inner-group assertions must go red ON THEIR OWN NAME and cannot be credited to the
        # outer-wall defect.
        outdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")  # #218: shared-/var/tmp class fix
        for i, a in enumerate(argv):
            if a == "--out":
                outdir = argv[i + 1]
        BREAK_INNER = True
        UP = "file://" + ROOT + "/"
        import gen_foundations_217 as f
        target = os.path.join(outdir, "bento-matrix-INNER-BROKEN.html")
        html = page(f.shell).replace('href="../../knowledge/',
                                     'href="file://%s/knowledge/' % ROOT)
        open(target, "w", encoding="utf-8").write(html)
        print("⬛ MUTATION ARM written (NON-REPO): %s" % target)
        print("   the s217-D7 nested squaring pass is OFF — every inner wall is back on its "
              "authored spans and the inner-group assertions must go RED by name.")
        return 0
    if "--break-layout" in argv:
        # ⬛ THE SECOND MUTATION ARM. NON-REPO by construction, same discipline as the first.
        outdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")  # #218: shared-/var/tmp class fix
        for i, a in enumerate(argv):
            if a == "--out":
                outdir = argv[i + 1]
        BREAK_LAYOUT = True
        UP = "file://" + ROOT + "/"
        import gen_foundations_217 as f
        target = os.path.join(outdir, "bento-matrix-LAYOUT-BROKEN.html")
        html = page(f.shell).replace('href="../../knowledge/',
                                     'href="file://%s/knowledge/' % ROOT)
        open(target, "w", encoding="utf-8").write(html)
        print("⬛ MUTATION ARM written (NON-REPO): %s" % target)
        print("   BOTH of Dave's #217 defects are back — the halved P4 container and the "
              "un-squared dashboard wall. The layout assertions must go RED by name.")
        return 0
    if "--break-legality" in argv:
        # ⬛ THE MUTATION ARM. NON-REPO by construction: the file is written outside the repo and
        # its asset addresses are rewritten to absolute paths, so it can never be mistaken for a
        # shipped artefact and never needs deleting from a tree.
        outdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")  # #218: shared-/var/tmp class fix
        for i, a in enumerate(argv):
            if a == "--out":
                outdir = argv[i + 1]
        BREAK_LEGALITY = True
        UP = "file://" + ROOT + "/"
        import gen_foundations_217 as f
        target = os.path.join(outdir, "bento-matrix-BROKEN.html")
        html = page(f.shell).replace('href="../../knowledge/', 'href="file://%s/knowledge/' % ROOT)
        open(target, "w", encoding="utf-8").write(html)
        print("⬛ MUTATION ARM written (NON-REPO): %s" % target)
        print("   the legality rules always return LEGAL — the probe's refusal assertions must "
              "go RED by name.")
        return 0
    print("gen_bento_matrix_217 is the page BODY for showroom/_foundations/bento.html.\n"
          "The file is written by knowledge/_render/gen_foundations_217.py — run that.\n"
          "  python3 knowledge/_render/gen_bento_matrix_217.py --selftest\n"
          "  python3 knowledge/_render/gen_bento_matrix_217.py --break-legality")
    return 0


if __name__ == "__main__":
    main()
