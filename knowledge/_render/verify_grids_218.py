#!/usr/bin/env python3
"""
verify_grids_218.py — DRIVES the four Foundations "Grids" pages (#218) and the library grouping
that puts them there, and measures what a screenshot cannot tell you.

WHY IT IS IN THE REPO AND NOT A SCRATCH FILE (s191-D2): a verification that lives only in a
sandbox is a claim, not an instrument — it expires with the session. This one can be re-driven.

WHAT IT DRIVES

 1 · THE FONT, WITH TWO CONTROLS — `document.fonts.check()` returns true in BOTH the working and
     the broken fontconfig, so it cannot discriminate. The canvas width of the target face must
     equal both aliases and differ from a REAL control face AND from one that does not exist
     (knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL).

 2 · THE DANGLING-VAR SWEEP, 8 STATES, OVER **EVERY** STYLE BLOCK. ⚠ This is WIDER than
     verify_foundations_217.py's sweep, deliberately: that one splits on the FIRST `<style>` and
     so never sees a page's `extra_css`. These pages are mostly extra_css — the whole consumed
     controller stylesheet arrives there — so a sweep that stopped at the first block would be
     reporting on the page chrome and calling it the page. Every canon property read anywhere in
     the document's own CSS is resolved live, in four themes × light/dark; an empty resolution is
     a FAILURE, because a page-local fallback is a fence AND a trap: a canon property that
     stopped resolving would quietly serve the LIGHT fallback in a DARK theme and no gate would
     fire ([[dangling-dataviz-var-renders-silent-black]]).
     ⚠ `--bento-*` and `--l-*` are excluded from the BODY sweep and probed on their OWN elements:
     they are scoped to `.c-bento` / `.cn-layout-utilities`, so asking the body for them is the
     wrong question and answers EMPTY for a page behaving exactly as ruled.

 3 · THE PAINT FOLLOWED THE THEME — the resolved ground must differ between light and dark for
     every theme. A page that "works" because everything fell back to white passes every textual
     gate; this is what catches it.

 4 · THE CONTROLS DRIVE, MEASURED IN PIXELS — not "the attribute changed", which is a tautology
     over a page that writes its own attributes:
       display   · spacing 40 → 24 → tight, read back as the wall's resolved column-gap.
       gallery   · mode justified vs bento (which container renders), and ragged → square read
                   back as a CHANGE IN A TILE'S RESOLVED grid-column span.
       dashboard · main spacing on the outer wall AND the s217-D6 snapping slider driven in
                   PIXELS with an OFF-SNAP value, the snap read back off the resolved inner
                   gutter. Plus the ruled ABSENCE: no Tight button on main spacing.
     And the type is PINNED: each page renders exactly one pane, and offers no type dial.

 ⬛ 5 · THE DASHBOARD PAGE CARRIES THE #218 CLAUSE, ASSERTED FROM RENDERED POSITIONS.
     Dave, #218: "each tile must have it's own keyline, but the radii should only apply to the
     4 corners of each sub bento (a collection of tiles)".
       ABOVE 1px — every tile's border is 1px, the GROUP's border is 0 (tiles carrying edges plus
         a group frame is the double frame rejected at #217), the four CORNER TILES — identified
         from RENDERED BOXES, never from data-c, because the bands rewrite spans — carry the
         group's own resolved radius on their OUTER corner and 0 on every other, and NOT ONE line
         element renders in any gutter.
       AT 1px — the handover: the group draws the curved 1px border, the tiles' borders are 0,
         and the hairline pair renders. This is the only stop at which a line renders at all.

 ✅ 6 · THE 12-COLUMN PAGE — the overlay's RESOLVED track count must equal the STORE's
     `layout/web/columns` at desktop, and the margin and gutter must resolve, in the live
     document, to the numbers the STORE names for the selected scale. ⛔ Read back off
     `getComputedStyle`, never off the switch: a page that printed what it had just declared
     would agree with itself and with nothing else. Every view is driven.

 ✅ 7 · THE LIBRARY — the Grids group renders in the tier nav with its four entries inside its
     wrapper, `showroom/index.json` round-trips the group on the same four slugs, and every one
     of the four has a thumbnail on disk.

 ⬛ 8 · THE MUTATION ARM. `--group-mutation` drives the NON-REPO copy written by
     `gen_library_214.py --break-groups`, whose tier nav is drawn FLAT. The group assertions in 7
     MUST fail there, BY NAME — a gate that has never been seen to fail is not a gate
     ([[instrument-without-a-consumer]]). With `--group-mutation` the exit code is INVERTED:
     green means the arm went red as required.
     ⚠ THE MUTANT DIR IS `BM_MUTANT_DIR`, and /var/tmp is SHARED ACROSS SESSIONS: a foreign
     mutant is unwritable AND stale, and a stale mutant silently proves yesterday's clause
     (#218 measured that). Pass a session-suffixed directory to BOTH the generator and this.

Chunked, because sandbox bash calls die near 45 s wall:
  python3 knowledge/_render/verify_grids_218.py --page 12col
  python3 knowledge/_render/verify_grids_218.py --page display
  python3 knowledge/_render/verify_grids_218.py --page gallery
  python3 knowledge/_render/verify_grids_218.py --page dashboard [--shots /var/tmp/shots-s218g]
  python3 knowledge/_render/verify_grids_218.py --library
  BM_MUTANT_DIR=/var/tmp/mut-s218g \
    python3 knowledge/_render/verify_grids_218.py --library --group-mutation
  BM_MUTANT_DIR=/var/tmp/mut-s218g \
    python3 knowledge/_render/verify_grids_218.py --dash-mutation
      ⬛ THE SECOND ARM, over `gen_grids_218.py --break-dash` (which flips the EXPLORER'S own
      BREAK_LAYOUT handle, so the corner rules are stripped through the one path that composes
      them). The #218 corner assertions in 5 MUST fail there, BY NAME — bucketed on the name, so
      "something failed" cannot be mistaken for the clause failing. Exit code inverted.
  BM_MUTANT_DIR=/var/tmp/mut-s218g \
    python3 knowledge/_render/verify_grids_218.py --overlay-mutation
      ⬛ THE THIRD ARM (s218-D6 (2)), over `gen_grids_218.py --break-overlay`: the 12-column
      page composed WITHOUT the paint-order pair, i.e. the column wash back on top of the demo
      cards. The `12col overlay` assertions MUST fail there, by that name. Exit code inverted.

 ★ s218-D6 (2) · THE PAINT ORDER, IN PIXELS. On the 12-column page the column overlay paints
     BEHIND the demonstration content ("Behind the content"). It is asserted with a real
     screenshot and two sampled pixels — one inside a demo card (must be the card's own untinted
     surface) and one in the gap between rows (must still carry the wash). Neither a hit test
     (`elementFromPoint` skips `pointer-events:none`) nor a z-index read-back can discriminate;
     see `overlay_paint_order`.

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
import json
import os
import re
import sys
import tempfile                              # s218-D6 (2): the paint-order screenshot lands here

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FOUND = os.path.join(ROOT, "showroom", "_foundations")
SHOWROOM = os.path.join(ROOT, "showroom")
MUT_DIR = os.environ.get("BM_MUTANT_DIR", "/var/tmp")
MUTANT_INDEX = os.path.join(MUT_DIR, "library-index-GROUPS-BROKEN.html")
MUTANT_JSON = os.path.join(MUT_DIR, "library-index-GROUPS-BROKEN.json")
MUTANT_DASH = os.path.join(MUT_DIR, "grids-dashboard-LAYOUT-BROKEN.html")
# ⬛ s218-D6 (2) — the 12-column page with the paint-order pair stripped (`--break-overlay`).
MUTANT_OVERLAY = os.path.join(MUT_DIR, "grids-12col-OVERLAY-BROKEN.html")

sys.path.insert(0, HERE)
import gen_grids_218 as grids               # the STORE values, through the generator's own read
import gen_library_214 as library           # FOUNDATIONS + FOUNDATION_GROUPS — one list

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]
PAGE_FILE = {"12col": "grids-12col.html", "display": "grids-display.html",
             "gallery": "grids-gallery.html", "dashboard": "grids-dashboard.html"}

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""

# ⛔ THE SWEEP IS OVER EVERY STYLE BLOCK. See the header — a sweep that stops at the first block
# never sees `extra_css`, which on these pages is nearly the whole stylesheet.
SCOPED_PREFIXES = ("--bento-", "--l-")


def foreign_props(page_src):
    """The CANON properties this page reads, derived from the page's OWN stylesheets."""
    css = "\n".join(b.split("</style>", 1)[0] for b in page_src.split("<style>")[1:])
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    read = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    return sorted(p for p in (read - declared)
                  if not any(p.startswith(x) for x in SCOPED_PREFIXES))


STATE_PROBE = """(props) => {
  const b = document.body, m = document.querySelector('main');
  const bad = props.filter(p => !getComputedStyle(b).getPropertyValue(p).trim());
  return {theme: document.documentElement.getAttribute('data-apollo-theme'),
          mode: b.getAttribute('data-theme'),
          ground: getComputedStyle(b).backgroundColor,
          ink: getComputedStyle(m).color,
          unresolved: bad,
          panes: Array.from(document.querySelectorAll('.bm-pane'))
                      .filter(p => getComputedStyle(p).display !== 'none')
                      .map(p => p.getAttribute('data-pane')),
          typeDial: document.querySelectorAll('.bm-group[data-dial="type"]').length};
}"""

# ⛔ THE SCOPED DIALS, ASKED ON THEIR OWN ELEMENTS. `--bento-*` lives on `.c-bento`, `--l-*` on
# `.cn-layout-utilities` — a body-level question answers EMPTY for a page behaving as ruled.
SCOPED_PROBE = """() => {
  const out = [];
  const ask = (sel, names) => {
    const e = document.querySelector(sel);
    if (!e) return;
    const cs = getComputedStyle(e);
    names.forEach(n => { if (!cs.getPropertyValue(n).trim()) out.push(sel + ' ' + n); });
  };
  ask('.c-bento', ['--bento-columns', '--bento-gutter', '--bento-row-unit']);
  ask('.cn-layout-utilities', ['--l-margin', '--l-gutter']);
  return out;
}"""

CLICK = """([dial, value]) => {
  const g = document.querySelector('.bm-group[data-dial="' + dial + '"]');
  if (!g) return 'NO GROUP ' + dial;
  const b = g.querySelector('button[data-value="' + value + '"]');
  if (!b) return 'NO BUTTON ' + dial + ':' + value;
  if (b.disabled) return 'DISABLED ' + dial + ':' + value;
  b.click();
  return 'ok';
}"""

WALL = """(sel) => {
  const w = document.querySelector(sel);
  if (!w) return null;
  const g = w.querySelector(':scope > .c-bento__grid');
  const cs = g ? getComputedStyle(g) : null;
  const t = g ? Array.from(g.children).find(x => x.classList.contains('c-bento__tile')) : null;
  const px = v => Math.round(parseFloat(v) || 0);
  return {gutter: cs ? px(cs.columnGap) : -1,
          cols: cs ? cs.gridTemplateColumns.split(' ').filter(Boolean).length : -1,
          tileBorder: t ? px(getComputedStyle(t).borderTopWidth) : -1,
          // ⚠ AT TIGHT THE LINE IS NOT A BORDER. The tight+keylines construction draws an INSET
          // BOX-SHADOW on the tile's right and bottom edge (1px cannot hold a gap and a line, so
          // the tiles go flush and the seam moves inside them) and the WALL draws its own top and
          // left. Asserting a border there asked the wrong question and reported 0px on a page
          // rendering the construction exactly ([[mutation-tests-the-clause-not-the-feature]] —
          // a probe must be written for the clause the page actually enacts).
          tileShadow: t ? (getComputedStyle(t).boxShadow || 'none') : 'none',
          wallEdge: [px(getComputedStyle(w).borderTopWidth),
                     px(getComputedStyle(w).borderLeftWidth)],
          tileSpan: t ? getComputedStyle(t).gridColumnStart : ''};
}"""

SLIDER_DRIVE = """(raw) => {
  const r = document.getElementById('bm-subSpacing');
  if (!r) return 'NO SLIDER';
  r.value = String(raw);
  r.dispatchEvent(new Event('input', {bubbles: true}));
  return 'ok';
}"""

# ⬛ #218 — THE CORNER CLAUSE, FROM RENDERED POSITIONS. Corner tiles are identified from the
# BOXES the browser laid out, never from data-c/data-r: the responsive bands rewrite the spans,
# so the authored attributes describe a rung the page may not be standing on.
DASH_PROBE = """() => {
  const px = v => Math.round(parseFloat(v) || 0);
  const pane = document.querySelector('.bm-pane[data-pane="dashboard"]');
  if (!pane) return {error: 'no dashboard pane'};
  const groups = Array.from(pane.querySelectorAll('.bm-outer > .c-bento__grid > .bm-inner'));
  const lines = Array.from(pane.querySelectorAll('.bm-gapline'))
    .filter(l => getComputedStyle(l).display !== 'none')
    .filter(l => { const r = l.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
  return {lines: lines.length, groups: groups.map((g, gi) => {
    const cs = getComputedStyle(g);
    const grid = g.querySelector(':scope > .c-bento__grid');
    const tiles = Array.from(grid.children).filter(t => t.classList.contains('c-bento__tile'));
    const boxes = tiles.map(t => t.getBoundingClientRect());
    const L = Math.min.apply(null, boxes.map(b => b.left));
    const R = Math.max.apply(null, boxes.map(b => b.right));
    const T = Math.min.apply(null, boxes.map(b => b.top));
    const B = Math.max.apply(null, boxes.map(b => b.bottom));
    const near = (a, b) => Math.abs(a - b) <= 1.5;
    return {index: gi + 1,
            radius: px(cs.borderTopLeftRadius),
            border: px(cs.borderTopWidth),
            tiles: tiles.map((t, ti) => {
              const b = boxes[ti], s = getComputedStyle(t);
              return {i: ti + 1,
                      border: px(s.borderTopWidth),
                      holds: [near(b.left, L) && near(b.top, T),
                              near(b.right, R) && near(b.top, T),
                              near(b.right, R) && near(b.bottom, B),
                              near(b.left, L) && near(b.bottom, B)],
                      corners: [px(s.borderTopLeftRadius), px(s.borderTopRightRadius),
                                px(s.borderBottomRightRadius), px(s.borderBottomLeftRadius)]};
            })};
  })};
}"""

# ✅ THE 12-COLUMN READ-BACK. Resolved off the live document, on the elements canon's own layout
# utilities style — never off the switch that was just clicked.
TWELVE_PROBE = """(view) => {
  const stage = document.getElementById('gx-stage');
  const b = document.querySelector('.gx-seg button[data-view="' + view + '"]');
  if (!b) return {error: 'no view button ' + view};
  b.click();
  const overlay = document.querySelector('.gx-frame .l-cols.gx-overlay');
  const container = document.querySelector('.gx-stage .l-container');
  const demo = document.querySelector('.gx-demo');
  const cs = getComputedStyle(overlay);
  const px = v => Math.round(parseFloat(v) || 0);
  return {view: stage.getAttribute('data-view'),
          tracks: cs.gridTemplateColumns.split(' ').filter(Boolean).length,
          gutter: px(cs.columnGap),
          margin: px(getComputedStyle(container).paddingLeft),
          bars: overlay.children.length,
          demoTracks: demo
            ? getComputedStyle(demo).gridTemplateColumns.split(' ').filter(Boolean).length : -1,
          readout: {
            columns: document.querySelector('[data-read="columns"]').textContent.trim(),
            margin: document.querySelector('[data-read="margin"]').textContent.trim(),
            gutter: document.querySelector('[data-read="gutter"]').textContent.trim()}};
}"""


def lum(rgb):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])


def parse_rgb(s):
    n = [float(x) for x in re.findall(r"[\d.]+", s or "")[:3]]
    return tuple(n) if len(n) == 3 else None


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def shell_path():
    for r in [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
              os.path.expanduser("~/.cache/ms-playwright")]:
        if r:
            hit = glob.glob(os.path.join(
                r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
            if hit:
                return hit[0]
    return None


# ---------------------------------------------------------------------------- the library half
def library_checks(mutation):
    """-> (fails, lines). Static: the shipped index markup + the shipped JSON + the thumbnails.

    ⛔ ASKED OF THE ARTEFACT, NOT THE CONFIG. `FOUNDATIONS` says what SHOULD be grouped; these
    read what the generator actually shipped. A group declared and not drawn is the whole
    failure mode this is here to catch.
    """
    fails, lines = [], []
    if mutation:
        for p in (MUTANT_INDEX, MUTANT_JSON):
            if not os.path.exists(p):
                sys.exit("verify_grids_218: no mutant at %s — run\n"
                         "  BM_MUTANT_DIR=%s python3 knowledge/_render/gen_library_214.py"
                         " --break-groups" % (p, MUT_DIR))
        index_html = open(MUTANT_INDEX, encoding="utf-8").read()
        index_json = json.load(open(MUTANT_JSON, encoding="utf-8"))
        lines.append("  driving the MUTANT index: %s" % MUTANT_INDEX)
    else:
        index_html = open(os.path.join(SHOWROOM, "index.html"), encoding="utf-8").read()
        index_json = json.load(open(os.path.join(SHOWROOM, "index.json"), encoding="utf-8"))

    want = sorted(f["slug"] for f in library.FOUNDATIONS if f.get("group") == "Grids")
    tree = index_html.split('id="tree-type"', 1)[-1].split('id="tree-usage"', 1)[0]

    # 7a — the group LABEL is drawn in the tier nav.
    if '<div class="grp" data-group="Grids">' not in tree:
        fails.append("GROUP NAV — the Grids group wrapper is not in the Type tree: the group is "
                     "declared and not drawn")
    if "<span class=\"grpl\">Grids" not in tree:
        fails.append("GROUP LABEL — no 'Grids' label renders over the group in the tier nav")
    # 7b — all four entries sit INSIDE the wrapper, not merely somewhere on the page.
    # ⛔ AND THE ABSENT WRAPPER IS ITS OWN FAILURE, not a fall-through. Splitting on a marker that
    # is not there returns the WHOLE tree, and the membership test then passes on links that are
    # merely present — measured on the --break-groups arm, where this read green while the group
    # was gone. A probe whose split can silently widen is not asking its own question
    # ([[unmatched-grep-is-not-an-absence]]).
    marker = '<div class="grp" data-group="Grids">'
    if marker not in tree:
        fails.append("GROUP MEMBERS — cannot be asked: there is no group wrapper to be inside of")
    else:
        inside = sorted(re.findall(r'data-slug="(foundation-grids-[a-z0-9]+)"',
                                   tree.split(marker, 1)[1].split("</div>", 1)[0]))
        if inside != want:
            fails.append("GROUP MEMBERS — inside the wrapper: %r, expected %r" % (inside, want))
    # 7c — the JSON index round-trips the group.
    jgroup = sorted(c["slug"] for c in index_json["components"] if c.get("group") == "Grids")
    if jgroup != want:
        fails.append("GROUP JSON — index.json carries group=Grids on %r, expected %r"
                     % (jgroup, want))
    if index_json.get("$foundation_groups") != list(library.FOUNDATION_GROUPS):
        fails.append("GROUP WORD-SET — index.json $foundation_groups is %r, expected %r"
                     % (index_json.get("$foundation_groups"),
                        list(library.FOUNDATION_GROUPS)))
    # 7d — a page and a thumbnail on disk for every member (a card with no pixels degrades).
    for f in library.FOUNDATIONS:
        if f.get("group") != "Grids":
            continue
        pg = os.path.join(FOUND, f["file"])
        th = os.path.join(SHOWROOM, "_thumbs", f["slug"] + ".png")
        if not os.path.exists(pg):
            fails.append("GROUP PAGE — %s is not on disk" % f["file"])
        if not os.path.exists(th):
            fails.append("GROUP THUMB — %s has no thumbnail (#217 residual class: a thumbnail "
                         "that predates its page is the other half of this)" % f["slug"])
        elif not mutation:
            lines.append("  %-28s page %6d bytes · thumb %6d bytes"
                         % (f["slug"], os.path.getsize(pg), os.path.getsize(th)))
    return fails, lines


# ---------------------------------------------------------------------------- the driven half
def drive(name, shots, dash_mutation=False, overlay_mutation=False):
    src = os.path.join(FOUND, PAGE_FILE[name])
    if dash_mutation:
        src = MUTANT_DASH
        if not os.path.exists(src):
            sys.exit("verify_grids_218: no mutant at %s — run\n"
                     "  BM_MUTANT_DIR=%s python3 knowledge/_render/gen_grids_218.py --break-dash"
                     % (src, MUT_DIR))
    if overlay_mutation:
        src = MUTANT_OVERLAY
        if not os.path.exists(src):
            sys.exit("verify_grids_218: no mutant at %s — run\n"
                     "  BM_MUTANT_DIR=%s python3 knowledge/_render/gen_grids_218.py "
                     "--break-overlay" % (src, MUT_DIR))
    if not os.path.exists(src):
        sys.exit("verify_grids_218: no such page — %s" % src)
    props = foreign_props(open(src, encoding="utf-8").read())
    if shots:
        os.makedirs(shots, exist_ok=True)
    store = grids.layout_store()
    views = grids.views(store)

    from playwright.sync_api import sync_playwright
    fails, lines = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1280, "height": 960})
        # ⛔ goto file:// ONLY. set_content() gives the document no URL, so ../../knowledge/canon/
        # never resolves and the page renders with canon and the type composites silently inert.
        pg.goto("file://" + src + "#theme=mono&m=light")
        pg.wait_for_timeout(900)
        f = pg.evaluate(FONT_PROBE)
        if not (f["target"] == f["alias_uf"] == f["alias_font"]
                and f["target"] != f["control_real"] and f["target"] != f["control_absent"]):
            print("REFUSED — the font probe cannot discriminate: %r" % f)
            b.close()
            sys.exit(1)
        print("font probe (controls pass): %r" % f)

        grounds = {}
        for theme in THEMES:
            for mode in MODES:
                pg.evaluate("h => { location.hash = h; }", "#theme=%s&m=%s" % (theme, mode))
                pg.wait_for_timeout(300)
                r = pg.evaluate(STATE_PROBE, props)
                state = "%s/%s" % (theme, mode)
                if r["theme"] != theme or r["mode"] != mode:
                    fails.append("%s — the hashchange broadcast did not land (got %s/%s)"
                                 % (state, r["theme"], r["mode"]))
                if r["unresolved"]:
                    fails.append("%s — ⛔ DANGLING: %s resolved EMPTY (silent-fallback class)"
                                 % (state, ", ".join(r["unresolved"])))
                scoped = pg.evaluate(SCOPED_PROBE)
                if scoped:
                    fails.append("%s — ⛔ DANGLING (scoped): %s" % (state, ", ".join(scoped)))
                if name == "12col":
                    if r["panes"] or r["typeDial"]:
                        fails.append("%s — the 12-column page carries bento panes/dials: it is a "
                                     "token page and tunes nothing" % state)
                else:
                    # ⛔ THE TYPE IS PINNED. One pane, and no control that selects another type.
                    if r["panes"] != [name]:
                        fails.append("%s — panes rendered %r, expected exactly ['%s']"
                                     % (state, r["panes"], name))
                    if r["typeDial"]:
                        fails.append("%s — a TYPE dial is on a single-type page (%d group(s)): "
                                     "it would select a pane that is not here"
                                     % (state, r["typeDial"]))
                g, ink = parse_rgb(r["ground"]), parse_rgb(r["ink"])
                grounds[state] = r["ground"]
                lines.append("  %-22s ground %-22s ink %-22s contrast %s"
                             % (state, r["ground"], r["ink"],
                                ratio(g, ink) if (g and ink) else "?"))
                if shots:
                    pg.screenshot(path=os.path.join(shots, "%s-%s-%s.png"
                                                    % (name, theme, mode)),
                                  full_page=(theme == "mono"))
        # 3 — the paint must MOVE between light and dark, or the theme never reached the page.
        for theme in THEMES:
            if grounds["%s/light" % theme] == grounds["%s/dark" % theme]:
                fails.append("%s — light and dark paint the SAME ground (%s): the theme did not "
                             "reach the page, or everything fell back"
                             % (theme, grounds["%s/light" % theme]))

        pg.evaluate("h => { location.hash = h; }", "#theme=console&m=light")
        pg.wait_for_timeout(320)

        if name == "12col":
            fails += twelve_col_drive(pg, views, store, lines)
        elif name == "display":
            fails += display_drive(pg, lines)
        elif name == "gallery":
            fails += gallery_drive(pg, lines)
        else:
            fails += dashboard_drive(pg, lines)
        b.close()

    print("page: showroom/_foundations/%s" % PAGE_FILE[name])
    print("foreign properties probed per state (%d): %s" % (len(props), ", ".join(props)))
    print("\n".join(lines))
    return fails


def twelve_col_drive(pg, views, store, lines):
    """✅ EVERY VIEW DRIVEN, and the numbers compared to the STORE — never to a constant here."""
    fails = []
    for v in views:
        r = pg.evaluate(TWELVE_PROBE, v["key"])
        if r.get("error"):
            fails.append("12col — %s" % r["error"])
            continue
        want_cols = int(store["web_columns"])
        if r["tracks"] != want_cols:
            fails.append("12col %s — the overlay resolved %d tracks, the STORE's "
                         "layout/web/columns is %d" % (v["key"], r["tracks"], want_cols))
        if r["bars"] != want_cols:
            fails.append("12col %s — the overlay draws %d .l-span-1 bars, expected %d"
                         % (v["key"], r["bars"], want_cols))
        if r["demoTracks"] != want_cols:
            fails.append("12col %s — a demonstration row resolved %d tracks, expected %d: the "
                         "demo is not standing on the same grid the overlay draws"
                         % (v["key"], r["demoTracks"], want_cols))
        want_m, want_g = int(v["margin"].rstrip("px")), int(v["gutter"].rstrip("px"))
        if r["margin"] != want_m:
            fails.append("12col %s — margin resolved %dpx in the live document, the STORE says "
                         "%s" % (v["key"], r["margin"], v["margin"]))
        if r["gutter"] != want_g:
            fails.append("12col %s — gutter resolved %dpx in the live document, the STORE says "
                         "%s" % (v["key"], r["gutter"], v["gutter"]))
        # the read-out panel must agree with the document it claims to be reading
        if (r["readout"]["columns"] != str(r["tracks"])
                or r["readout"]["margin"] != "%dpx" % r["margin"]
                or r["readout"]["gutter"] != "%dpx" % r["gutter"]):
            fails.append("12col %s — the read-out says %r but the document resolved "
                         "%d cols / %dpx margin / %dpx gutter"
                         % (v["key"], r["readout"], r["tracks"], r["margin"], r["gutter"]))
        lines.append("  view %-14s tracks %2d · margin %2dpx · gutter %2dpx  (store %s/%s)"
                     % (v["key"], r["tracks"], r["margin"], r["gutter"],
                        v["margin"], v["gutter"]))
    # ⛔ THE COLLAPSE IS CANON'S, AND IT IS REAL — asserted by narrowing, not by reading the rule.
    ms = int((store["breakpoints"].get("ms") or {}).get("$value", "760px").rstrip("px"))
    pg.set_viewport_size({"width": ms - 60, "height": 900})
    pg.wait_for_timeout(250)
    # ⚠ READ `gridColumnStart`, NOT `gridColumnEnd`. `grid-column: span 6` is shorthand for
    # `grid-column-start: span 6; grid-column-end: auto`, so the END side reads 'auto' at every
    # width and an assertion on it can neither pass nor discriminate (measured #218 — it read
    # 'auto' on a page whose collapse was working perfectly).
    narrow = pg.evaluate("""() => {
      const d = document.querySelector('.gx-demo > .l-span-6');
      return d ? getComputedStyle(d).gridColumnStart : 'NONE'; }""")
    if narrow != "span 12":
        fails.append("12col — below breakpoint/ms (%dpx) a .l-span-6 resolved %r, expected "
                     "'span 12': canon's collapse did not reach this page" % (ms, narrow))
    lines.append("  below breakpoint/ms (%dpx): .l-span-6 resolves %r" % (ms, narrow))
    pg.set_viewport_size({"width": 1280, "height": 960})
    pg.wait_for_timeout(200)
    fails += overlay_paint_order(pg, lines)
    return fails


# ✅ s218-D6 (2) — THE OVERLAY PAINTS BEHIND THE DEMO CONTENT, MEASURED IN PIXELS.
#
# ⛔ WHY NOT A HIT TEST: `elementFromPoint`/`elementsFromPoint` SKIP `pointer-events:none`, and
#    the overlay has always carried it — so a hit-test "proof" returns the demo card whether the
#    wash is in front or behind. It cannot discriminate, and it would have read green on the
#    defect. ⛔ WHY NOT READING BACK `z-index`: that asserts the rule the generator just wrote,
#    which is the document-vs-document trap this file exists to avoid.
# So: one real screenshot, two sampled pixels, and BOTH directions asserted —
#    (a) a pixel inside a demo card must be the card's OWN resolved background. Under the defect
#        the 10% accent wash composites over it and the pixel is measurably red-shifted.
#    (b) a pixel in the gap BETWEEN two demo rows must still be washed. "Behind" must not have
#        quietly become "gone" — a `display:none` or a negative z-index behind an opaque ancestor
#        would satisfy (a) perfectly and destroy the page.
PAINT_POINTS = """() => {
  const frame = document.querySelector('.gx-frame');
  const bars = [...document.querySelectorAll('.gx-overlay > i')];
  const rows = [...document.querySelectorAll('.gx-frame > .gx-rows > .gx-demo')];
  if (!frame || bars.length < 2 || rows.length < 2) return {error: 'frame/bars/rows not found'};
  frame.scrollIntoView({block: 'center'});
  const card = rows[0].firstElementChild;      // the .l-span-12 row: it covers every bar
  const c = card.getBoundingClientRect(), b0 = bars[0].getBoundingClientRect();
  const r0 = rows[0].getBoundingClientRect(), r1 = rows[1].getBoundingClientRect();
  // ⛔ THE SAMPLE X IS A BAR'S CENTRE, NOT THE CARD'S. MEASURED: the card's own centre lands on
  // the boundary between column 6 and column 7 — a GUTTER, where no bar is painted in either
  // arm. Sampled there the probe read pure white with the fix in AND with it stripped, and the
  // mutation arm refused to go red. A pixel proof must sample where the two states differ.
  const x = Math.round(b0.left + b0.width / 2);
  return {
    card: [x, Math.round(c.top + c.height / 2)],
    cardBg: getComputedStyle(card).backgroundColor,
    overBar: x >= Math.round(c.left) && x <= Math.round(c.right),
    gap: [x, Math.round((r0.bottom + r1.top) / 2)],
    gapPx: +(r1.top - r0.bottom).toFixed(1),
  };
}"""


def overlay_paint_order(pg, lines):
    fails = []
    try:
        from PIL import Image
    except ImportError:                      # named refusal, never a silent skip
        return ["12col overlay — ⛔ COULD-NOT-ASK: pillow is not importable, so the s218-D6 "
                "paint-order proof was never driven (it is a PIXEL assertion by construction)"]
    p = pg.evaluate(PAINT_POINTS)
    if p.get("error"):
        return ["12col overlay — %s" % p["error"]]
    if not p.get("overBar"):
        return ["12col overlay — the sampled column bar does not lie inside the demo card, so the "
                "card pixel could not tell 'wash behind' from 'no wash here at all'"]
    if p["gapPx"] < 4:
        return ["12col overlay — the row gap measured %.1fpx, too thin to sample a pixel in: the "
                "wash half of the proof would be vacuous" % p["gapPx"]]
    pg.wait_for_timeout(150)
    shot = os.path.join(tempfile.mkdtemp(dir=os.environ.get("TMPDIR", "/var/tmp")), "12col.png")
    pg.screenshot(path=shot)                 # viewport, scale 1 — CSS px map 1:1 to image px
    im = Image.open(shot).convert("RGB")
    card_px, gap_px = im.getpixel(tuple(p["card"])), im.getpixel(tuple(p["gap"]))
    want = parse_rgb(p["cardBg"])
    if not want:
        return ["12col overlay — the demo card resolved no opaque background (%r); the sample "
                "point proves nothing" % p["cardBg"]]
    want = tuple(int(round(v)) for v in want)
    if max(abs(a - b) for a, b in zip(card_px, want)) > 2:
        fails.append("12col overlay — a pixel INSIDE a demo card measured rgb%s but the card's own "
                     "background is rgb%s: the column wash is painting ON TOP of the content "
                     "(s218-D6 rules it BEHIND)" % (card_px, want))
    if card_px == gap_px:
        fails.append("12col overlay — the pixel in the row gap rgb%s is identical to the pixel "
                     "inside the card: the overlay is not painting at all, so 'behind' has become "
                     "'gone'" % (gap_px,))
    elif gap_px[0] <= max(gap_px[1], gap_px[2]):
        fails.append("12col overlay — the pixel in the row gap rgb%s carries no accent wash "
                     "(red is not the dominant channel): the columns stopped being drawn"
                     % (gap_px,))
    # ⚠ the line REPORTS, it does not assert — it prints in the mutant arm too, so it must not
    # word itself as a verdict ("== its own surface" would be a lie on the arm that just failed).
    lines.append("  paint order: card pixel rgb%s (card surface rgb%s) · row-gap pixel rgb%s "
                 "(washed) · gap %.1fpx" % (card_px, want, gap_px, p["gapPx"]))
    return fails


def display_drive(pg, lines):
    fails, seen = [], {}
    for value, want in (("40", 40), ("24", 24), ("1", 0)):
        # tight + keylines ON is the ruled P1 reading: the gap collapses to 0 and the line moves
        # INTO the tiles. Both halves are read back, in pixels.
        pg.evaluate(CLICK, ["spacing", value])
        pg.wait_for_timeout(200)
        w = pg.evaluate(WALL, ".bm-pane[data-pane='display'] .bm-display")
        seen[value] = w
        if w["gutter"] != want:
            fails.append("display spacing=%s — resolved column-gap %dpx, expected %dpx"
                         % (value, w["gutter"], want))
    # at the OPEN spacings the keyline is a plain 1px tile border …
    for value in ("40", "24"):
        if seen[value]["tileBorder"] != 1:
            fails.append("display spacing=%s + keylines — tile border %dpx, expected 1px"
                         % (value, seen[value]["tileBorder"]))
    # … and at TIGHT it is the inset seam plus the wall's own top and left edge. Both halves are
    # asserted, because either alone would pass a page drawing only the other.
    if seen["1"]["tileShadow"] in ("none", ""):
        fails.append("display tight+keylines — the tiles draw no inset seam (box-shadow %r): the "
                     "flush construction did not land" % seen["1"]["tileShadow"])
    if seen["1"]["wallEdge"] != [1, 1]:
        fails.append("display tight+keylines — the wall's own top/left edge resolved %r, "
                     "expected [1, 1]: the inset group has no outer edge"
                     % seen["1"]["wallEdge"])
    lines.append("  display spacing 40/24/tight -> gutter %d/%d/%d px · open tile border %dpx · "
                 "tight: tile inset seam %s, wall edge %r"
                 % (seen["40"]["gutter"], seen["24"]["gutter"], seen["1"]["gutter"],
                    seen["24"]["tileBorder"],
                    "present" if seen["1"]["tileShadow"] not in ("none", "") else "ABSENT",
                    seen["1"]["wallEdge"]))
    pg.evaluate(CLICK, ["spacing", "24"])
    return fails


def gallery_drive(pg, lines):
    fails = []
    pg.evaluate(CLICK, ["mode", "justified"])
    pg.wait_for_timeout(200)
    vis = pg.evaluate("""() => Array.from(
      document.querySelectorAll('.bm-pane[data-pane="gallery"] .c-bento.bm-wall'))
      .filter(w => getComputedStyle(w).display !== 'none')
      .map(w => w.classList.contains('bm-just') ? 'just' : 'bento')""")
    if vis != ["just"]:
        fails.append("gallery mode=justified — visible walls %r, expected ['just']" % vis)
    pg.evaluate(CLICK, ["mode", "bento"])
    pg.wait_for_timeout(200)
    ragged = pg.evaluate(WALL, ".bm-pane[data-pane='gallery'] .bm-gallery")
    # ⛔ THE RAGGED/SQUARE DIAL IS A SPAN SWAP — read back as a CHANGE IN A RESOLVED SPAN, not as
    # an attribute that the page itself wrote.
    pg.evaluate(CLICK, ["edge", "square"])
    pg.wait_for_timeout(250)
    squared = pg.evaluate("""() => {
      const w = document.querySelector('.bm-pane[data-pane="gallery"] .bm-gallery');
      return Array.from(w.querySelectorAll('.c-bento__tile'))
        .map(t => getComputedStyle(t).gridColumnStart + '/' + getComputedStyle(t).gridRowStart)
        .join(' '); }""")
    ragged_spans = pg.evaluate("""() => {
      const w = document.querySelector('.bm-pane[data-pane="gallery"] .bm-gallery');
      return Array.from(w.querySelectorAll('.c-bento__tile'))
        .map(t => t.getAttribute('data-ragged')).join(' '); }""")
    pg.evaluate(CLICK, ["edge", "ragged"])
    pg.wait_for_timeout(250)
    ragged_now = pg.evaluate("""() => {
      const w = document.querySelector('.bm-pane[data-pane="gallery"] .bm-gallery');
      return Array.from(w.querySelectorAll('.c-bento__tile'))
        .map(t => getComputedStyle(t).gridColumnStart + '/' + getComputedStyle(t).gridRowStart)
        .join(' '); }""")
    if squared == ragged_now:
        fails.append("gallery bottom edge — square and ragged resolved the SAME spans (%r): the "
                     "dial moved an attribute and nothing else" % squared[:80])
    lines.append("  gallery justified/bento swap OK · ragged wall gutter %dpx, span sets differ "
                 "(ragged attrs present: %s)" % (ragged["gutter"], bool(ragged_spans.strip())))
    return fails


def dashboard_drive(pg, lines):
    """⬛ s217-D8 + #218, driven at the ruled stops in the theme where the radius is non-zero."""
    fails = []
    # ⛔ THE RULED ABSENCE. Dashboard main spacing has NO Tight button — ruled out, not disabled.
    tight = pg.evaluate("""() => {
      const g = document.querySelector('.bm-group[data-dial="mainSpacing"]');
      return g ? g.querySelectorAll('button[data-value="1"]').length : -1; }""")
    if tight != 0:
        fails.append("dashboard main spacing — %d Tight button(s) present; s217-D5 rules tight "
                     "OUT of the main wall, so it must be ABSENT, not disabled" % tight)
    for value, want in (("40", 40), ("24", 24)):
        pg.evaluate(CLICK, ["mainSpacing", value])
        pg.wait_for_timeout(200)
        w = pg.evaluate(WALL, ".bm-pane[data-pane='dashboard'] .bm-outer")
        if w["gutter"] != want:
            fails.append("dashboard mainSpacing=%s — outer wall resolved %dpx, expected %dpx"
                         % (value, w["gutter"], want))
    # ⬛ s217-D6 — the SNAP, driven in PIXELS with an OFF-SNAP value so the snap is a real
    # operation the probe can land, not an unfalsifiable claim about indices.
    for raw, want in ((7, 8), (13, 12), (22, 20), (40, 24), (1, 1)):
        pg.evaluate(SLIDER_DRIVE, raw)
        pg.wait_for_timeout(260)
        got = pg.evaluate("""() => {
          const i = document.querySelector('.bm-pane[data-pane="dashboard"] .bm-inner');
          const g = i.querySelector(':scope > .c-bento__grid');
          return {gutter: Math.round(parseFloat(getComputedStyle(g).columnGap) || 0),
                  out: document.getElementById('bm-subSpacing-out').textContent.trim(),
                  state: window.__BM_STATE.dashboard.subSpacing}; }""")
        if got["gutter"] != want or got["out"] != "%dpx" % want or got["state"] != str(want):
            fails.append("dashboard sub-spacing %d → expected the %dpx stop, got gutter %dpx / "
                         "read-out %s / state %s"
                         % (raw, want, got["gutter"], got["out"], got["state"]))
        d = pg.evaluate(DASH_PROBE)
        if d.get("error"):
            fails.append("dashboard — %s" % d["error"])
            continue
        if want == 1:
            # AT 1px — the handover. The group draws the curved border, the tiles draw none, and
            # this is the ONLY stop at which a line element renders at all.
            for g in d["groups"]:
                if g["border"] != 1:
                    fails.append("⛔ 1px HANDOVER — group %d border %dpx, expected 1px: at the "
                                 "1px stop the GROUP carries the curved border"
                                 % (g["index"], g["border"]))
                bad = [t["i"] for t in g["tiles"] if t["border"] != 0]
                if bad:
                    fails.append("⛔ 1px HANDOVER — group %d tiles %r carry a border; at 1px the "
                                 "gutter IS the hairline and a tile edge would double every seam"
                                 % (g["index"], bad))
            if d["lines"] == 0:
                fails.append("⛔ 1px HANDOVER — no line element renders at the 1px stop; it is "
                             "the one stop where the hairline pair is drawn")
            lines.append("  sub 1px  · groups border 1px, tiles 0px, %d line element(s) — the "
                         "flush regime" % d["lines"])
            continue
        # ⛔ THE CONTROL FOR THE CORNER CLAUSE. It is driven in CONSOLE because console is the one
        # theme whose container radius is non-zero; if the group's radius reads 0 here, "the
        # corner tile carries the radius, the others carry 0" is 0-vs-0 and cannot discriminate —
        # exactly how a mutant that failed to load canon read GREEN (#218, measured). A probe that
        # cannot fail must REFUSE, not pass.
        flat = [g["index"] for g in d["groups"] if g["radius"] == 0]
        if flat:
            fails.append("⛔ #218 CORNER KEYLINE (sub %dpx) — group(s) %r resolve a 0px container "
                         "radius in CONSOLE: the corner clause cannot be discriminated at 0, so "
                         "this is a REFUSAL, not a pass (canon did not reach the page, or the "
                         "role rule did not land)" % (want, flat))
        # ABOVE 1px — the s217-D8 construction and the #218 corner clause.
        if d["lines"] != 0:
            fails.append("⛔ s217-D8 (sub %dpx) — %d line element(s) render; above 1px NO gutter "
                         "carries anything, inner or outer" % (want, d["lines"]))
        for g in d["groups"]:
            if g["border"] != 0:
                fails.append("⛔ s217-D8 (sub %dpx) — group %d draws a %dpx border beside tiles "
                             "that carry their own: that is the double frame Dave rejected"
                             % (want, g["index"], g["border"]))
            bare = [t["i"] for t in g["tiles"] if t["border"] != 1]
            if bare:
                fails.append("⛔ s217-D8 (sub %dpx) — group %d tiles %r carry no 1px box; the "
                             "keyline must go round tight to the module"
                             % (want, g["index"], bare))
            corners = [0, 0, 0, 0]
            for t in g["tiles"]:
                for k in range(4):
                    exp = g["radius"] if t["holds"][k] else 0
                    if t["corners"][k] != exp:
                        fails.append(
                            "⛔ #218 CORNER KEYLINE (sub %dpx) — group %d tile %d corner %d "
                            "resolved %dpx, expected %dpx (the group's own radius is %dpx and "
                            "this tile %s that corner of the sub-bento)"
                            % (want, g["index"], t["i"], k, t["corners"][k], exp, g["radius"],
                               "holds" if t["holds"][k] else "does not hold"))
                    if t["holds"][k]:
                        corners[k] += 1
            if corners != [1, 1, 1, 1]:
                fails.append("⛔ #218 CORNER KEYLINE (sub %dpx) — group %d: the four corners of "
                             "the sub-bento are held by %r tiles, expected one each"
                             % (want, g["index"], corners))
        lines.append("  sub %-3s · groups border 0px, every tile boxed 1px, radius %dpx on the "
                     "4 corner tiles only, %d line element(s)"
                     % ("%dpx" % want, d["groups"][0]["radius"], d["lines"]))
    return fails


def main():
    argv = sys.argv[1:]
    name, shots = None, None
    for i, a in enumerate(argv):
        if a == "--page":
            name = argv[i + 1]
        if a == "--shots":
            shots = argv[i + 1]
    mutation = "--group-mutation" in argv
    if "--library" in argv or mutation:
        fails, lines = library_checks(mutation)
        print("library: the #218 Grids group")
        print("\n".join(lines))
        if mutation:
            # ⬛ INVERTED. Green here means the arm went RED as required.
            if not fails:
                print("\n⛔ MUTATION ARM DID NOT GO RED — the grouping was stripped and every "
                      "group assertion still passed. A gate that cannot fail is not a gate.")
                sys.exit(1)
            print("\n✅ MUTATION ARM RED AS REQUIRED — %d assertion(s), by name:" % len(fails))
            for f_ in fails:
                print("  ❌ " + f_)
            return
        if fails:
            print("\n%d FAILURE(S):" % len(fails))
            for f_ in fails:
                print("  ❌ " + f_)
            sys.exit(1)
        print("\nOK — the Grids group renders, four entries inside it, index.json round-trips, "
              "four thumbnails on disk.")
        return
    dash_mutation = "--dash-mutation" in argv
    if dash_mutation:
        name = "dashboard"
    overlay_mutation = "--overlay-mutation" in argv
    if overlay_mutation:
        name = "12col"
    if name not in PAGE_FILE:
        sys.exit("verify_grids_218: --page must be one of %s (or use --library)"
                 % ", ".join(sorted(PAGE_FILE)))
    fails = drive(name, shots, dash_mutation, overlay_mutation)
    if overlay_mutation:
        # ⬛ INVERTED, AND BUCKETED BY NAME. The arm strips the s218-D6 paint-order pair, so the
        # wash goes back OVER the demo cards. What must fail is the PAINT-ORDER clause on its own
        # name — "something failed" would also be satisfied by a mutant that simply failed to
        # load ([[mutation-tests-the-clause-not-the-feature]]).
        named = [f_ for f_ in fails if f_.startswith("12col overlay")]
        if not named:
            print("\n⛔ MUTATION ARM DID NOT GO RED — the s218-D6 z-index pair was stripped and "
                  "the paint-order assertion still passed. A gate that cannot fail is not a gate. "
                  "(%d other failure(s): %s)" % (len(fails), fails[:1]))
            sys.exit(1)
        print("\n✅ MUTATION ARM RED AS REQUIRED — %d paint-order assertion(s) by name "
              "(of %d total failures):" % (len(named), len(fails)))
        for f_ in named:
            print("  ❌ " + f_)
        return
    if dash_mutation:
        # ⬛ INVERTED. Green here means the #218 corner assertions went RED as required. ⚠ Bucketed
        # BY NAME: the arm also puts back other #217 defects, so "something failed" is not the
        # test — what must fail is the CORNER clause on its own name
        # ([[mutation-tests-the-clause-not-the-feature]]).
        named = [f_ for f_ in fails if "#218 CORNER KEYLINE" in f_]
        if not named:
            print("\n⛔ MUTATION ARM DID NOT GO RED — the #218 corner rules were stripped and the "
                  "corner assertion still passed. A gate that cannot fail is not a gate. "
                  "(%d other failure(s): %s)" % (len(fails), fails[:1]))
            sys.exit(1)
        print("\n✅ MUTATION ARM RED AS REQUIRED — %d corner assertion(s) by name "
              "(of %d total failures). First three:" % (len(named), len(fails)))
        for f_ in named[:3]:
            print("  ❌ " + f_)
        return
    if fails:
        print("\n%d FAILURE(S):" % len(fails))
        for f_ in fails:
            print("  ❌ " + f_)
        sys.exit(1)
    print("\nOK — %d state(s), no dangling property, theme reached the paint in all four, "
          "controls driven." % (len(THEMES) * len(MODES)))


if __name__ == "__main__":
    main()
