#!/usr/bin/env python3
"""
_bento_recut_219.py — THE ONE HOME FOR THE BENTO DECISION LEDGER (#219, 2026-08-25).

WHY THIS FILE EXISTS. Dave opened the #217-era bento decision pages
(`reviews/BENTO-CANON-2026-08-23-v2.html` / `-v3.html`, `reviews/GALLERY-COMPARE-2026-08-23-v1.html`)
and said, correctly: *"we've already decided all of this in previous sessions"* and *"we've also
missed the extra space for captions."* Those pages were built BEFORE `s217-D5`, `s217-D8`, `s218-D1`
and `s218-D6`, so every one of them still puts a SETTLED question to him as an open choice. Re-asking
a ruled question is the laundering defect ([[feedback-dont-launder-a-premise-into-a-ruling]]); it is
also how a ruling gets quietly reversed by an accidental click.

⛔ THIS MODULE RULES NOTHING AND MINTS NOTHING. Every `clause` below is a VERBATIM slice of the
`says` field of the named ruling in `knowledge/_rulings.json`, copied at #219 and quotable back to
it. Where a #217 question is only PARTIALLY covered, the entry carries BOTH the ruled part and the
`residue` — never rounded either way.

⚠ WRITE-ONCE (ADR-0017). The ledger lives HERE, once, and the three successor pages RENDER it. Three
copies of "what is still open" is three chances for the pages to disagree with each other in front of
Dave, which is the failure this whole re-cut exists to repair.

Consumed by:
  · knowledge/_render/gen_bento_canon_217.py    -> reviews/BENTO-CANON-2026-08-25-v4.html
  · knowledge/_render/gen_bento_roles_217.py    -> reviews/BENTO-CANON-2026-08-25-v5.html
  · knowledge/_render/gen_gallery_compare_217.py-> reviews/GALLERY-COMPARE-2026-08-25-v2.html
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import html as htmlmod

RECUT_DATE = "2026-08-25"

# States. RULED = the question is closed and is STRUCK on the page, with its receipt.
#         PARTIAL = a named part is closed and STRUCK; the residue stays a live control.
#         OPEN = nothing rules it; it stays a live control, owned by Dave.
RULED, PARTIAL, OPEN = "RULED", "PARTIAL", "OPEN"

# ---------------------------------------------------------------------------------------------
# THE LEDGER. `pages` names which successor page carries the row: "canon" (v4), "roles" (v5),
# "compare" (GALLERY-COMPARE v2).
# ⚠ `clause` is VERBATIM from knowledge/_rulings.json. `mints` is what a Dave answer would create —
# it is written as a QUESTION'S CONSEQUENCE, never as a recommendation.
# ---------------------------------------------------------------------------------------------
LEDGER = [
    dict(
        key="Q1", pages=("canon",), state=RULED, receipt="s217-D3",
        question="May tile spans be adjusted at mint time at all — i.e. does the squaring pass "
                 "exist?",
        asked_as="BENTO-CANON v2, § “No orphaned compartments” — badged “Proposed — not "
                 "ruled”.",
        clause="SQUARING PASS RATIFIED for dashboard and brochureware roles (Dave: 'is very cool', "
               "with gallery exempted in the same breath).",
    ),
    dict(
        key="Q2", pages=("canon",), state=OPEN, owner="Dave",
        question="When the pass runs, may only the TAIL of a wall move, or the whole wall?",
        asked_as="BENTO-CANON v2, § “What is yours to decide”.",
        note="No ruling reaches this. The shipped pass moves the last few tiles only "
             "(`tail_cap=6` in `canon/gen_canon_bento.square_wall`) — that is an IMPLEMENTATION "
             "choice standing in for a decision, and it is still standing in.",
        mints="a ruling on the squaring pass's mutation scope: tail-only, or the whole wall.",
    ),
    dict(
        key="Q3", pages=("canon", "compare"), state=PARTIAL, receipt="s218-D6 (4)",
        question="What may a photograph be re-cropped into when a wall is squared?",
        asked_as="BENTO-CANON v2, § “What is yours to decide”.",
        clause="THE PHOTOGRAPHY GALLERY WALL IS SQUARED — Dave reopened the edge on the page his "
               "exports already marked edge:square: the squaring pass runs on the photography "
               "page's gallery wall and last-row photos may re-span to close holes.",
        residue="Ruled for the photography page's wall ONLY, and only for LAST-ROW photographs. "
                "What a photograph anywhere else may be re-spanned into — and whether a portrait "
                "may ever be laid on its side to close a hole — is untouched.",
        owner="Dave",
        mints="a bound on the crop a squaring pass may pay, applying to every wall rather than to "
              "one page.",
    ),
    dict(
        key="Q4", pages=("roles", "compare"), state=RULED, receipt="s217-D5",
        question="Does the gallery keep its keylines, drop them for the 1px gutter, or get both as "
                 "a dial?",
        asked_as="BENTO-CANON v3, § “The keyline trial” — badged “Proposed — not ruled”; "
                 "and GALLERY-COMPARE v1, wall A3.",
        clause="GALLERY: same three spacings; keylines on/off; caption background colour on/off",
        also=("s218-D3", "supercharge spacing 1, console/legacy/mono spacing 24, keylines off, "
              "bento mode, white grounds, transparent captions"),
        also_note="…so the photography page's own answer is already recorded too: keylines OFF in "
                  "all four themes.",
    ),
    dict(
        key="Q5", pages=("compare",), state=RULED, receipt="s217-D5",
        question="Does the gallery stay a span grid with orphan tolerance, or become justified rows "
                 "with a widow switch?",
        asked_as="GALLERY-COMPARE v1 — the whole page. This was THE question the page was built to "
                 "put.",
        clause="mode is 'Justified rows' OR 'Gallery bento', the bento mode carrying a sub-option "
               "ragged or square bottom (this turns s217-D3's gallery squaring exemption into a "
               "per-instance choice)",
        also=("s218-D3", "bento mode"),
        also_note="…and the photography page's mode is recorded as BENTO in all four of Dave's "
                  "exports. A or B was answered “both, as a dial, per instance”.",
    ),
    dict(
        key="Q6", pages=("roles", "compare"), state=PARTIAL, receipt="s217-D5",
        question="Ragged or square bottom edge on a gallery wall?",
        asked_as="BENTO-CANON v3, § Gallery (“This wall is ragged, and that is the ruling”); "
                 "GALLERY-COMPARE v1, A's hole counts.",
        clause="the bento mode carrying a sub-option ragged or square bottom (this turns s217-D3's "
               "gallery squaring exemption into a per-instance choice)",
        residue="The DIAL is ruled and one instance is set — `s218-D6 (4)` squares the photography "
                "page's wall and scopes itself: “the GALLERY ROLE's s217-D3 exemption elsewhere is "
                "untouched until he says wider.” Whether the ROLE's default flips from ragged to "
                "square is the part still open.",
        owner="Dave",
        mints="an amendment to `s217-D3`'s gallery squaring exemption — the role default, not one "
              "page's dial.",
    ),
    dict(
        key="Q7", pages=("canon", "roles", "compare"), state=RULED, receipt="s218-D6 (1)",
        question="What ground and ink does a mono caption take?",
        asked_as="Carried as the conductor's PROPOSED shade at #218 (`s218-D3`), Dave's eye owed.",
        clause="The mono caption ground is RATIFIED at the proposed shade: #1A1A1A via "
               "--surface-digital-black with --text-reverse white ink - 'Yes - that's the one'. "
               "The s218-D3 PROPOSED marker on the shade is discharged.",
        baked="Baked into this page: switch the theme to MONO and every caption takes the ruled "
              "ground and the reverse ink, in light and dark alike.",
    ),
    dict(
        key="Q8", pages=("canon", "roles", "compare"), state=RULED, receipt="s217-D3",
        question="How much space does a gallery caption get?",
        asked_as="Ruled at #217 and DERIVED to 86px — but `BENTO-CANON v2` never consumed it, which "
                 "is the gap Dave named: “we've also missed the extra space for captions.”",
        clause="GALLERY ADDITIONS: more generous caption space (ruled)",
        baked="Baked into this page from `layout/bento/caption-space` in "
              "`knowledge/tokens/layout.json` — the token, never a literal. The three-line clamp is "
              "derived back out of the same number at mint time, so the space and the clamp cannot "
              "disagree.",
    ),
    dict(
        key="Q9", pages=("canon", "roles"), state=PARTIAL, receipt="s218-D1",
        question="Where does the corner radius sit when every tile is keylined?",
        asked_as="Not asked on these pages at all — recorded here so nothing on them can be read as "
                 "re-opening it.",
        clause="each tile must have it's own keyline, but the radii should only apply to the 4 "
               "corners of each sub bento (a collection of tiles) … Scope option-selected by Dave "
               "the same sitting: DASHBOARD ONLY for now - brochureware/gallery keep their s217-D3 "
               "radius behaviour until he extends it.",
        residue="DASHBOARD ONLY. Brochureware and gallery keep their `s217-D3` radius behaviour "
                "until Dave extends it — so nothing on these pages carries the corner-keyline "
                "construction outside a dashboard.",
        owner="Dave",
        mints="a widening of `s218-D1`'s scope to brochureware and/or gallery.",
        enacted_in="The construction itself lives in `knowledge/_render/gen_bento_matrix_217.py` "
                   "(the matrix explorer), which owns it. This page records the ruling and its "
                   "scope; it does not re-draw it.",
    ),
    dict(
        key="Q10", pages=("roles", "compare"), state=RULED, receipt="s217-D8",
        question="May a keyline run down the middle of the spacing?",
        asked_as="Not asked on these pages — recorded so no keyline treatment shown here can be "
                 "read as re-opening it.",
        clause="With keylines ON in a dashboard bento, the keyline goes tight around each module "
               "(tile) - a 1px border on the tile box at every spacing stop - never a line centred "
               "in the gutter. … The centred-gutter 'treatment C' construction is retired for "
               "dashboards.",
    ),
    dict(
        key="Q11", pages=("compare",), state=OPEN, owner="Dave",
        question="If justified rows are used, do the rows RE-PACK as the container narrows, or keep "
                 "their mint-time membership and simply shorten?",
        asked_as="GALLERY-COMPARE v1 declared the cost but never put the question.",
        note="`s217-D5` rules the MODE into existence and says nothing about re-packing. Today's "
             "wall is minted once at the page's own content width: the rows stay flush at every "
             "width, but they stay THE SAME ROWS. Flickr re-packs at runtime. Narrow the window on "
             "candidate B below and both behaviours are visible.",
        mints="a ruling on justified-row responsiveness: mint-per-band, a runtime pass, or "
              "shortening accepted.",
    ),
    dict(
        key="Q12", pages=("compare",), state=OPEN, owner="Dave",
        question="Do justified rows carry an emphasis rhythm at all?",
        asked_as="GALLERY-COMPARE v1 named it in the comparison table as “a separate question if "
                 "you go this way”. It stayed separate.",
        note="The span grid promotes every 6th tile to 2×2 (`s217-D2`). Justified rows have no "
             "equivalent here; Flickr's is a full-width breakout every n rows, guarded to "
             "landscape pictures.",
        mints="a ruling on whether justified rows get an emphasis rhythm, and what guards it.",
    ),
]

# ⬛ UNPROVEN, not open — declared so it is not mistaken for a decision waiting on Dave.
UNPROVEN = [
    ("compare", "Whether candidate B NESTS. B is a flex column, not a grid, so it is not known "
                "whether it can be a tile of another bento. That is a measurement nobody has "
                "taken, not a call anybody is waiting on."),
]


def esc(s):
    return htmlmod.escape(str(s if s is not None else ""), quote=True)


def rows_for(page):
    return [r for r in LEDGER if page in r["pages"]]


def counts_for(page):
    rs = rows_for(page)
    return {
        "struck": sum(1 for r in rs if r["state"] in (RULED, PARTIAL)),
        "open": sum(1 for r in rs if r["state"] in (OPEN, PARTIAL)),
        "ruled": sum(1 for r in rs if r["state"] == RULED),
        "partial": sum(1 for r in rs if r["state"] == PARTIAL),
        "total": len(rs),
    }


# ---------------------------------------------------------------------------------------------
# THE PAGE BLOCK
# ---------------------------------------------------------------------------------------------
def ledger_html(page, title="What was already decided"):
    """The struck-and-open ledger, rendered for ONE page.

    ⚠ A RULED question is STRUCK, never dropped. Deleting it would leave Dave unable to tell a
    question that was answered from a question somebody forgot to ask — and he would have to
    re-derive the answer to find out which."""
    rs = rows_for(page)
    c = counts_for(page)
    S = ['<section id="decided">']
    S.append('<h2 class="t-ed-heading-3">%s</h2>' % esc(title))
    S.append('<p class="lede t-ed-body">These pages were built at <b>#217</b>, before '
             '<code>s217-D5</code>, <code>s217-D8</code>, <code>s218-D1</code> and '
             '<code>s218-D6</code>. Everything <s>struck through</s> below is <b>a question this '
             'page used to ask you and no longer does</b>, with the ruling that closed it. '
             '<b>%d struck, %d still live.</b> A struck question is shown, not deleted: a decision '
             'surface that quietly drops what it answered cannot be told apart from one that '
             'forgot to ask.</p>' % (c["struck"], c["open"]))
    S.append('<table class="rcut t-ed-body-small"><thead><tr>'
             '<th>The question</th><th>Where it stands</th></tr></thead><tbody>')
    for r in rs:
        state = r["state"]
        cls = {RULED: "rcut-ruled", PARTIAL: "rcut-part", OPEN: "rcut-open"}[state]
        q = esc(r["question"])
        qcell = ("<s>%s</s>" % q) if state == RULED else q
        S.append('<tr class="%s">' % cls)
        S.append('<td><span class="rcut-key t-cm-legal">%s</span> %s'
                 '<span class="rcut-asked t-cm-legal">%s</span></td>'
                 % (esc(r["key"]), qcell, esc(r.get("asked_as", ""))))
        cell = []
        if state == RULED:
            cell.append('<span class="rcut-tag rcut-tag-r t-cm-legal">Ruled &middot; %s</span>'
                        % esc(r["receipt"]))
            cell.append('<span class="rcut-clause t-ed-body-small">&ldquo;%s&rdquo;</span>'
                        % esc(r["clause"]))
        elif state == PARTIAL:
            cell.append('<span class="rcut-tag rcut-tag-p t-cm-legal">Part ruled &middot; %s'
                        '</span>' % esc(r["receipt"]))
            cell.append('<span class="rcut-clause t-ed-body-small">&ldquo;%s&rdquo;</span>'
                        % esc(r["clause"]))
            cell.append('<span class="rcut-res t-ed-body-small"><b>Residue, still yours:</b> %s'
                        '</span>' % esc(r["residue"]))
        else:
            cell.append('<span class="rcut-tag rcut-tag-o t-cm-legal">Open &middot; yours</span>')
            cell.append('<span class="rcut-res t-ed-body-small">%s</span>' % esc(r.get("note", "")))
        if r.get("also"):
            cell.append('<span class="rcut-clause t-ed-body-small"><b>%s</b> also records: '
                        '&ldquo;%s&rdquo; %s</span>'
                        % (esc(r["also"][0]), esc(r["also"][1]), esc(r.get("also_note", ""))))
        if r.get("baked"):
            cell.append('<span class="rcut-baked t-ed-body-small">%s</span>' % esc(r["baked"]))
        if r.get("enacted_in"):
            cell.append('<span class="rcut-res t-ed-body-small">%s</span>' % esc(r["enacted_in"]))
        if r.get("mints"):
            cell.append('<span class="rcut-mints t-ed-body-small"><b>Owner: %s.</b> An answer '
                        'mints %s</span>' % (esc(r.get("owner", "Dave")), esc(r["mints"])))
        S.append('<td>%s</td>' % "".join(cell))
        S.append('</tr>')
    S.append('</tbody></table>')
    un = [t for pg, t in UNPROVEN if pg == page]
    for t in un:
        S.append('<p class="note t-ed-body-small"><b>&#11036; Unproven, and not waiting on you:</b> '
                 '%s</p>' % esc(t))
    S.append('<p class="note t-ed-body-small">Every quotation above is a verbatim slice of the '
             'named ruling in <code>knowledge/_rulings.json</code>. Nothing on this page rules '
             'anything, and no control below offers a choice that one of those rulings has already '
             'made.</p>')
    S.append('</section>')
    return "\n".join(S)


def open_control_html(key, extra=""):
    """The live control for ONE genuinely-open question, wherever it belongs in the page body.

    ⚠ It carries its OWNER and the RULING IT WOULD MINT on its face. A control that does not say
    what answering it creates is an invitation to answer it by accident."""
    r = next((x for x in LEDGER if x["key"] == key), None)
    if r is None:
        raise KeyError("no ledger row %r" % key)
    if r["state"] not in (OPEN, PARTIAL):
        raise AssertionError(
            "REFUSED: %s is %s — a settled question may not be re-put as a live control "
            "([[feedback-dont-launder-a-premise-into-a-ruling]])" % (key, r["state"]))
    body = r.get("residue") if r["state"] == PARTIAL else r.get("note", "")
    return ('<div class="rcut-live">'
            '<span class="rcut-tag rcut-tag-o t-cm-legal">Open &middot; %s &middot; yours to rule'
            '</span>'
            '<p class="rcut-live-q t-ed-body"><b>%s</b></p>'
            '<p class="rcut-live-b t-ed-body-small">%s</p>'
            '<p class="rcut-live-b t-ed-body-small"><b>Answering it mints</b> %s</p>%s</div>'
            % (esc(r["key"]), esc(r["question"]), esc(body), esc(r["mints"]), extra))


# ---------------------------------------------------------------------------------------------
# SHARED CSS
# ⚠ NO STRUCTURE, NO BENTO DIAL, NO RULED NUMBER. Every selector here is page chrome; none of them
# names `.c-bento`, a `--bento-*` dial or a tile class, so none of them can reach a wall.
# ---------------------------------------------------------------------------------------------
RECUT_CSS = """
/* ---- #219 RE-CUT — the decision ledger's own chrome. Page chrome only. --------------------- */
table.rcut{border-collapse:collapse; margin:var(--sp-4) 0 0; width:100%;}
table.rcut th, table.rcut td{border-bottom:1px solid var(--line,#D7D8D6);
  padding:var(--sp-3) var(--sp-4); text-align:left; vertical-align:top; color:var(--ink-2,#545454);}
table.rcut th{color:var(--ink,#1A1A1A); white-space:nowrap;}
table.rcut td:first-child{color:var(--ink,#1A1A1A); width:38%;}
table.rcut s{color:var(--ink-2,#545454);}
.rcut-key{display:inline-block; border:1px solid var(--line-2,#767676); color:var(--ink,#1A1A1A);
  padding:1px 6px; margin-right:var(--sp-2); letter-spacing:0.1em;}
.rcut-asked{display:block; margin-top:var(--sp-2); color:var(--ink-2,#545454);}
.rcut-clause{display:block; margin-top:var(--sp-2); color:var(--ink-2,#545454);}
.rcut-res, .rcut-baked, .rcut-mints{display:block; margin-top:var(--sp-2);
  color:var(--ink-2,#545454);}
.rcut-mints{color:var(--ink,#1A1A1A);}
.rcut-tag{display:inline-block; padding:2px 8px; letter-spacing:0.12em; text-transform:uppercase;}
.rcut-tag-r{border:1px solid var(--line-2,#767676); color:var(--ink-2,#545454);}
.rcut-tag-p{border:1px solid var(--ink,#1A1A1A); color:var(--ink,#1A1A1A);}
.rcut-tag-o{border:1px solid var(--ink,#1A1A1A); background:var(--ink,#1A1A1A);
  color:var(--page,#FFFFFF);}
.rcut-live{border:1px solid var(--ink,#1A1A1A); padding:var(--sp-4) var(--sp-5);
  margin:var(--sp-5) 0 0; max-width:74ch;}
.rcut-live-q{margin:var(--sp-2) 0 0; color:var(--ink,#1A1A1A);}
.rcut-live-b{margin:var(--sp-2) 0 0; color:var(--ink-2,#545454);}
"""


def mono_caption_css(pairs):
    """The `s218-D6 (1)` mono caption ground, per page.

    `pairs` is a list of (caption-selector, [ink-child-selectors]). ⛔ TOKENS, NEVER A RAW HEX as the
    operative value: `--surface-digital-black` is #1A1A1A in mono in BOTH modes and `--text-reverse`
    is #FFFFFF in both, which is the point — a ground Dave ruled by eye must not invert when the mode
    flips. The literals are FALLBACKS only ([[dangling-dataviz-var-renders-silent-black]]).
    ⚠ The construction is COPIED from `gen_foundations_217.settings_css`'s rider, which is the
    ratified enactment ([[specimen-starts-from-reference]]) — not re-derived here."""
    sel = '[data-apollo-theme="mono"] '
    L = ["/* ---- s218-D6 (1) — THE MONO CAPTION GROUND, RATIFIED (Dave: “Yes — that's the one”).",
         "   Dave's words at #218: “But with the darkest grey for the captions and white for the",
         "   text.” Mode-stable tokens, both modes, mono only. */"]
    for cap, inks in pairs:
        L.append("%s%s{background:var(--surface-digital-black,#1A1A1A); "
                 "color:var(--text-reverse,#FFFFFF);}" % (sel, cap))
        if inks:
            L.append("%s{color:var(--text-reverse,#FFFFFF);}"
                     % ", ".join("%s%s" % (sel, i) for i in inks))
    return "\n".join(L)


def selftest():
    """5 bites: every row states verbatim · no settled row can be re-put as a control ·
    every open row names an owner and what it mints · every page carries rows · the ledger
    renders."""
    ids = [r["key"] for r in LEDGER]
    assert len(ids) == len(set(ids)), "bite 1 FAIL: duplicate ledger keys — %r" % ids
    for r in LEDGER:
        if r["state"] in (RULED, PARTIAL):
            assert r.get("receipt") and r.get("clause"), \
                "bite 2 FAIL: %s is %s with no receipt/clause — a strike with no ruling behind " \
                "it is a decision taken by the page" % (r["key"], r["state"])
        if r["state"] == PARTIAL:
            assert r.get("residue") and r.get("mints"), \
                "bite 2b FAIL: %s is PARTIAL with no residue — a partial ruling rounded to a " \
                "whole one is the defect this ledger exists to prevent" % r["key"]
        if r["state"] == OPEN:
            assert r.get("owner") and r.get("mints"), \
                "bite 3 FAIL: %s is OPEN with no owner or no consequence named" % r["key"]
    # a settled row MUST be refused as a live control
    ruled = [r["key"] for r in LEDGER if r["state"] == RULED]
    assert ruled, "bite 4a FAIL: nothing is struck, so the re-cut did nothing"
    try:
        open_control_html(ruled[0])
    except AssertionError:
        pass
    else:
        raise AssertionError("bite 4 FAIL: a RULED question was accepted as a live control — that "
                             "is exactly the laundering this module exists to refuse")
    for pg in ("canon", "roles", "compare"):
        assert rows_for(pg), "bite 5a FAIL: page %r carries no ledger rows" % pg
        h = ledger_html(pg)
        assert "<s>" in h and "rcut-tag" in h, "bite 5b FAIL: page %r rendered no strike" % pg
    for r in LEDGER:
        if r["state"] in (OPEN, PARTIAL):
            open_control_html(r["key"])
    c = {pg: counts_for(pg) for pg in ("canon", "roles", "compare")}
    print("_bento_recut_219 selftest OK (5 bites) — struck/open per page: %s"
          % " · ".join("%s %d/%d" % (k, v["struck"], v["open"]) for k, v in c.items()))


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
    else:
        for _r in LEDGER:
            print("%-4s %-8s %s" % (_r["key"], _r["state"], _r["question"]))
