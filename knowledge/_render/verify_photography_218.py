#!/usr/bin/env python3
"""
verify_photography_218.py — DRIVES `showroom/_foundations/photography.html` and measures the
per-theme gallery settings Dave ruled at #218, plus the 251-photograph lazy wall.

WHY IT IS IN THE REPO AND NOT A SCRATCH FILE (s191-D2): a verification that lives only in a
sandbox is a claim, not an instrument — it expires with the session. This one can be re-driven.

WHAT IT DRIVES

 1 · THE FONT, WITH TWO CONTROLS — `document.fonts.check()` returns true in BOTH the working and
     the broken fontconfig, so it cannot discriminate. The canvas width of the target face must
     equal both aliases and differ from a REAL control face AND from one that does not exist
     (knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL).

 2 · THE DANGLING-VAR SWEEP, 8 STATES, OVER **EVERY** STYLE BLOCK — including the compiled
     settings block, which is where this page's newest `var()` calls live. An empty resolution is
     a FAILURE: a page-local fallback is a fence AND a trap, because a canon property that stopped
     resolving would quietly serve the LIGHT fallback in a DARK theme and no gate would fire
     ([[dangling-dataviz-var-renders-silent-black]]).
     ⚠ `--bento-*` is excluded from the BODY sweep and probed on the WALL: it is scoped to
     `.c-bento`, so asking the body for it is the wrong question and answers EMPTY for a page
     behaving exactly as ruled.

 3 · THE PAINT FOLLOWED THE THEME — the resolved page ground must DIFFER between light and dark
     in every theme. A page that "works" because everything fell back to white passes every
     textual gate; this is what catches it. ⚠ It is asked EVEN THOUGH the ruled `pageBg` dial is
     `white`: "white" is the explorer's word for `--surface-raised`, which is white in light and
     the theme's raised dark surface in dark. A dial word is not a promise of a hex.

 4 · ⬛ THE #218 SETTINGS, RESOLVED LIVE, FOUR THEMES × TWO MODES. Read off `getComputedStyle`,
     never off the declaration — a page that printed what it had just declared would agree with
     itself and with nothing else. Per theme:
       gutter        · the wall's resolved `column-gap` — 1 / 24 / 24 / 24 px.
       keylines OFF  · EVERY tile and EVERY opener resolves a 0px border and no box-shadow, and
                       NOT ONE line element renders anywhere on the wall. ⚠ Asked of all 251, not
                       of a sample: one tile carrying a stray edge is exactly what a sample misses.
       rounding      · tile radius 0 and the PICTURE carrying canon's own container radius —
                       that is what `4 corners of the image` means, and it is the half a
                       radius-equals-0 assertion cannot tell apart in a theme whose radius is 0.
       grounds       · page and bento resolve to the theme's `--surface-raised`, and in LIGHT
                       mode to `rgb(255, 255, 255)` — which is what Dave's four export receipts
                       measured, all four of them in light mode.
       caption       · `rgba(0, 0, 0, 0)` in supercharge / console / legacy; in mono the RIDER —
                       `rgb(26, 26, 26)` ground with `rgb(255, 255, 255)` ink, in BOTH modes,
                       because a ground ruled by eye must not invert when the mode flips.
       caption space · canon's ruled 86px, unrestated by the page.

 5 · THE 251-PHOTOGRAPH LAZY WALL — 251 tiles; every `src` on the page resolves to a file ON
     DISK; every one of the 502 images carries `loading="lazy"` AND `decoding="async"`; and the
     count of tiles equals the manifest's own derivative count.
     ★ AND, SINCE s218-D6 (4), THE WALL IS SQUARED: zero holes at every band of its 4/3/2/1
     ladder, re-derived from the `data-c`/`data-r` PARSED BACK OUT OF THE SHIPPED MARKUP. This
     expectation FLIPPED — the wall was ragged-tolerant under s217-D3 (role=gallery) and holes
     were acceptable; Dave reopened the edge on this page ("Reopen — square it"), so ragged is
     now a failure HERE. The gallery ROLE's exemption elsewhere is untouched.

 ⬛ 6 · THE MUTATION ARM. `--settings-mutation` drives the NON-REPO copy written by
     `gen_foundations_217.py --break-settings`, whose compiled settings block is ABSENT. The
     assertions in 4 MUST fail there, BY NAME — bucketed on the name, so "something failed"
     cannot be mistaken for the clause failing. A gate that has never been seen to fail is not a
     gate ([[instrument-without-a-consumer]]). With `--settings-mutation` the exit code is
     INVERTED: green means the arm went red as required.
     ⚠ THE MUTANT DIR IS `BM_MUTANT_DIR`, and /var/tmp is SHARED ACROSS SESSIONS: a foreign
     mutant is unwritable AND stale, and a stale mutant silently proves yesterday's clause.
     Pass a session-suffixed directory to BOTH the generator and this.

Chunked, because sandbox bash calls die near 45 s wall:
  python3 knowledge/_render/verify_photography_218.py --static
  python3 knowledge/_render/verify_photography_218.py --themes mono,legacy
  python3 knowledge/_render/verify_photography_218.py --themes console,supercharge
  BM_MUTANT_DIR=/var/tmp/mut-<session> \
    python3 knowledge/_render/verify_photography_218.py --settings-mutation

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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, "showroom", "_foundations", "photography.html")
MANIFEST = os.path.join(ROOT, "knowledge", "_PHOTOGRAPHY-MANIFEST.json")
MUT_DIR = os.environ.get("BM_MUTANT_DIR", "/var/tmp")
MUTANT = os.path.join(MUT_DIR, "photography-SETTINGS-BROKEN.html")
# ⬛ #219 — THE MINTED-DEFAULT ARM'S subject. The settings block is INTACT in this one and exactly
# one ruled default is wrong (mono's caption ground), so only an assertion that asks whether the
# CAPTION GROUND IS THE TOKEN THE DIAL NAMES can see it.
MUTANT_DEFAULT = os.path.join(MUT_DIR, "photography-DEFAULT-BROKEN.html")

sys.path.insert(0, HERE)
import gen_foundations_217 as foundations   # the RULED settings, through the generator's own read

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]
# The bucket every settings assertion is filed under, so the mutation arm can require THESE and
# not merely "something".
SETTINGS_BUCKET = "SETTINGS"

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""

SCOPED_PREFIXES = ("--bento-",)


def foreign_props(page_src):
    """The CANON properties this page reads, derived from the page's OWN stylesheets."""
    css = "\n".join(b.split("</style>", 1)[0] for b in page_src.split("<style>")[1:])
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    read = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    return sorted(p for p in (read - declared)
                  if not any(p.startswith(x) for x in SCOPED_PREFIXES))


# ⛔ ONE EVALUATE PER STATE, AND IT WALKS EVERY TILE. 251 round-trips would not survive the wall;
# and the keyline question is only honest if it is asked of every tile, because the failure mode
# is one stray edge, not a uniform one.
STATE_PROBE = """(props) => {
  const px = v => Math.round(parseFloat(v) || 0);
  const b = document.body;
  const wall = document.querySelector('.c-bento.fx-wall-photo');
  const grid = wall ? wall.querySelector(':scope > .c-bento__grid') : null;
  const tiles = grid ? Array.from(grid.children).filter(t => t.classList.contains('c-bento__tile')) : [];
  const cs = e => getComputedStyle(e);
  const borders = new Set(), shadows = new Set(), tileRadii = new Set(),
        imgRadii = new Set(), capBg = new Set(), capInk = new Set(), capMin = new Set(),
        edgeInk = new Set();
  tiles.forEach(t => {
    const o = t.querySelector('.px-open'), i = t.querySelector('.px-img'),
          c = t.querySelector('.px-cap');
    tileRadii.add(px(cs(t).borderTopLeftRadius));
    borders.add(px(cs(t).borderTopWidth));
    if (o) { borders.add(px(cs(o).borderTopWidth)); borders.add(px(cs(o).borderRightWidth));
             borders.add(px(cs(o).borderBottomWidth)); borders.add(px(cs(o).borderLeftWidth));
             shadows.add(cs(o).boxShadow || 'none');
             // ⬛ #219 — the keyline's own COLOUR, so `keylines: on` can be asserted as a line
             // that RENDERS rather than as a width that is merely declared.
             if (px(cs(o).borderTopWidth)) edgeInk.add(cs(o).borderTopColor); }
    if (i) imgRadii.add(px(cs(i).borderTopLeftRadius));
    if (c) { capBg.add(cs(c).backgroundColor); capInk.add(cs(c).color);
             capMin.add(px(cs(c).minHeight)); }
  });
  // A LINE ELEMENT ANYWHERE ON THE WALL — the keyline construction's own vocabulary. Zero is
  // what 'keylines: off' means, and 'no such class in the markup' is not the same claim.
  const lines = wall ? Array.from(wall.querySelectorAll('.bm-gapline, .c-bento__keyline'))
                            .filter(l => cs(l).display !== 'none') : [];
  // ⬛ #219 — THE TOKENS THE RULED DIALS NAME, RESOLVED IN THIS STATE. The assertions compare the
  // paint against THESE, never against a literal: `grey` is a token, and a token's value is a
  // property of the theme and the mode. A probe that compared against #F0F0F0 would fail
  // supercharge (which resolves its own warm grey) for behaving exactly as ruled.
  const tok = {};
  ['--surface-subtle', '--surface-raised', '--background-default', '--text-secondary',
   '--text-default', '--border-subtle'].forEach(n => {
     tok[n] = cs(b).getPropertyValue(n).trim(); });
  return {theme: document.documentElement.getAttribute('data-apollo-theme'),
          mode: b.getAttribute('data-theme'),
          pageGround: cs(b).backgroundColor,
          bentoGround: wall ? cs(wall).backgroundColor : null,
          surfaceRaised: cs(b).getPropertyValue('--surface-raised').trim(),
          tokens: tok,
          containerRadius: px(cs(b).getPropertyValue('--border-radius-container') || '0'),
          gutter: grid ? px(cs(grid).columnGap) : -1,
          gutterVar: wall ? cs(wall).getPropertyValue('--bento-gutter').trim() : '',
          tiles: tiles.length,
          borders: Array.from(borders).sort((x, y) => x - y),
          shadows: Array.from(shadows),
          tileRadii: Array.from(tileRadii).sort((x, y) => x - y),
          imgRadii: Array.from(imgRadii).sort((x, y) => x - y),
          capBg: Array.from(capBg), capInk: Array.from(capInk),
          edgeInk: Array.from(edgeInk),
          capMin: Array.from(capMin).sort((x, y) => x - y),
          lines: lines.length,
          unresolved: props.filter(p => !cs(b).getPropertyValue(p).trim()),
          scoped: wall ? ['--bento-columns', '--bento-gutter', '--bento-row-unit']
                          .filter(n => !cs(wall).getPropertyValue(n).trim()) : ['NO WALL']};
}"""


def shell_path():
    for r in [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
              os.path.expanduser("~/.cache/ms-playwright")]:
        if r:
            hit = glob.glob(os.path.join(
                r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
            if hit:
                return hit[0]
    return None


# ---------------------------------------------------------------------------- the static half
def static_checks(src):
    """-> (fails, lines). Asked of the SHIPPED FILE and of the disk, never of the generator."""
    fails, lines = [], []
    man = json.load(open(MANIFEST, encoding="utf-8"))
    derivs = [r for r in man["rows"] if r.get("derivative")]

    tiles = src.count('class="c-bento__tile"')
    if tiles != len(derivs):
        fails.append("TILE COUNT — %d tiles on the page, %d manifest rows carry a derivative"
                     % (tiles, len(derivs)))
    imgs = re.findall(r"<img[^>]*>", src)
    bad = [i for i in imgs if 'loading="lazy"' not in i or 'decoding="async"' not in i]
    if bad:
        fails.append("LAZY — %d of %d images lack loading=\"lazy\" and/or decoding=\"async\": %s"
                     % (len(bad), len(imgs), bad[0][:120]))
    if len(imgs) != tiles * 2:
        fails.append("IMAGE COUNT — %d images for %d tiles; the wall and its lightboxes should be "
                     "one picture each" % (len(imgs), tiles))
    srcs = sorted({s for s in re.findall(r'src="\.\./\.\./(knowledge/assets/[^"]+)"', src)})
    absent = [s for s in srcs if not os.path.exists(os.path.join(ROOT, s))]
    if absent:
        fails.append("SRC — %d src(s) name a file that is not on disk: %s"
                     % (len(absent), ", ".join(absent[:5])))
    if len(srcs) != tiles:
        fails.append("SRC SPREAD — %d distinct srcs for %d tiles" % (len(srcs), tiles))
    # the derivative population, MEASURED off the disk rather than off the manifest's own count
    web = os.path.join(ROOT, "knowledge", "assets", "photography-web")
    on_disk = [n for n in os.listdir(web) if n.lower().endswith((".jpg", ".jpeg"))]
    total = sum(os.path.getsize(os.path.join(web, n)) for n in on_disk)
    if len(on_disk) != len(derivs):
        fails.append("DERIVATIVES — %d file(s) on disk, %d manifest row(s) name one"
                     % (len(on_disk), len(derivs)))
    lines.append("  derivatives: %d file(s), %.1f MB total, %.1f KB mean"
                 % (len(on_disk), total / 1048576.0, total / max(1, len(on_disk)) / 1024.0))
    over = sorted((n for n in on_disk
                   if os.path.getsize(os.path.join(web, n)) > 300 * 1024), reverse=False)
    lines.append("  over the ruled 300 KB ceiling (DECLARED RESIDUAL, spec unchanged): %d — %s"
                 % (len(over), ", ".join(over) if over else "none"))
    # the zero-JavaScript lightbox, still true at 251
    if src.count("<script") != 1:
        fails.append("SCRIPT COUNT — %d script tags; the lightbox must ship none"
                     % src.count("<script"))
    if 'command="show-popover"' not in src:
        fails.append("LIGHTBOX — the popover invoker command is gone")
    # ★ s218-D6 (4) — THE WALL IS SQUARED, AND THE HOLE TOLERANCE IS NOW ZERO.
    # This wall used to be RAGGED-TOLERANT (role=gallery, s217-D3): holes were acceptable and
    # nothing here asked about them. Dave reopened the edge on this page — "Reopen — square it" —
    # so the expectation flips: ZERO holes at EVERY band of the wall's own ladder.
    # ⛔ MEASURED OFF THE SHIPPED MARKUP, not off the generator's report and not off its selftest:
    # the spans are parsed back out of each tile's `data-c`/`data-r` and re-placed with canon's
    # own `is_rectangular`. A generator that reported "squared" and emitted something else is
    # exactly the failure `square_wall`'s docstring names, and only a parse of the artefact can
    # see it ([[no-gate-parses-the-artefact]]).
    # ⚠ SCOPE: this asserts THE PHOTOGRAPHY PAGE'S wall. s217-D3's gallery-role exemption is
    # untouched elsewhere and no other wall is asked this question.
    spans = [(int(c), int(r)) for c, r in
             re.findall(r'class="c-bento__tile" data-c="(\d+)" data-r="(\d+)"', src)]
    if len(spans) != tiles:
        fails.append("SPAN PARSE — %d tiles but %d parsed data-c/data-r pairs: the zero-hole "
                     "assertion below would be measuring a different wall" % (tiles, len(spans)))
    else:
        rect, at_cols, holes = foundations.is_rectangular(spans, foundations.PHOTO_LADDER)
        if not rect:
            fails.append("SQUARED — the shipped wall is NOT an exact rectangle: %d hole(s) at %d "
                         "columns (ladder %s). s218-D6 squares this wall; ragged is no longer "
                         "tolerated here"
                         % (holes, at_cols or foundations.PHOTO_LADDER[0],
                            foundations.PHOTO_LADDER))
        lines.append("  squared (s218-D6): %d hole(s) over ladder %s — %d tile(s) parsed from the "
                     "shipped markup" % (holes, foundations.PHOTO_LADDER, len(spans)))

    # the settings block is IN the shipped file, between its own markers
    _, block = foundations.split_settings(src)
    if not block:
        fails.append("%s BLOCK — the compiled per-theme settings block is not in the shipped page"
                     % SETTINGS_BUCKET)
    lines.append("  tiles %d · images %d · distinct srcs %d · settings block %d bytes"
                 % (tiles, len(imgs), len(srcs), len(block)))
    return fails, lines


# ---------------------------------------------------------------------------- the driven half
def drive(path, themes, shots=None):
    """-> (fails, lines). Every settings failure is prefixed with SETTINGS_BUCKET."""
    src = open(path, encoding="utf-8").read()
    props = foreign_props(src)
    fails, lines = [], []
    if shots:
        os.makedirs(shots, exist_ok=True)
    url = "file://" + path

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto(url)
        f = pg.evaluate(FONT_PROBE)
        # ⛔ TWO CONTROLS. `fonts.check()` cannot discriminate; the widths can.
        if not (f["target"] == f["alias_uf"] == f["alias_font"]
                and f["target"] != f["control_real"] and f["target"] != f["control_absent"]):
            fails.append("FONT — the HSBC face is not the one rendering: %r" % f)
        lines.append("  font: target %d = aliases %d/%d, controls %d (real) / %d (absent)"
                     % (f["target"], f["alias_uf"], f["alias_font"],
                        f["control_real"], f["control_absent"]))

        grounds = {}
        for theme in themes:
            ruled = foundations.GALLERY_SETTINGS[theme]
            want_gutter = int(foundations.spacing_px(ruled["spacing"]).replace("px", ""))
            for mode in MODES:
                pg.goto("%s#theme=%s&m=%s" % (url, theme, mode))
                pg.wait_for_timeout(120)
                s = pg.evaluate(STATE_PROBE, props)
                tag = "%s/%s" % (theme, mode)
                if s["theme"] != theme or s["mode"] != mode:
                    fails.append("STATE — asked for %s, the document reports %s/%s"
                                 % (tag, s["theme"], s["mode"]))
                if s["unresolved"]:
                    fails.append("DANGLING — %s: %d canon property(ies) resolve EMPTY on the "
                                 "body: %s" % (tag, len(s["unresolved"]), s["unresolved"]))
                if s["scoped"]:
                    fails.append("DANGLING (scoped) — %s: %s resolve EMPTY on the wall"
                                 % (tag, s["scoped"]))
                grounds.setdefault(theme, {})[mode] = s["pageGround"]

                # ---- 4 · THE RULED SETTINGS, LIVE ------------------------------------------
                # ⛔ EVERY EXPECTATION BELOW IS READ OFF THE RULED DIAL, never typed. At #218 this
                # block asserted one shape for all four themes (white grounds, corners, keylines
                # off, transparent captions bar the mono rider). s219-D1/D2 make the defaults
                # DIFFER BY THEME — capsule in console, keylines on in legacy, grey captions in
                # two — so a probe built from one shape would red the ruling rather than the page.
                if s["gutter"] != want_gutter:
                    fails.append("%s GUTTER — %s: resolved column-gap %dpx, ruled %dpx"
                                 % (SETTINGS_BUCKET, tag, s["gutter"], want_gutter))
                if ruled["keylines"] == "off":
                    if s["borders"] != [0]:
                        fails.append("%s KEYLINES — %s: keylines are ruled OFF but resolved border "
                                     "widths across %d tiles are %s"
                                     % (SETTINGS_BUCKET, tag, s["tiles"], s["borders"]))
                    if s["edgeInk"]:
                        fails.append("%s KEYLINES — %s: a tile edge renders in %s with keylines "
                                     "ruled OFF" % (SETTINGS_BUCKET, tag, s["edgeInk"]))
                else:
                    # ⬛ s219-D2 (4) — ON in legacy. The export resolves `tileBorderPx: 1`, so the
                    # widths across all 251 tiles must be exactly {0 (the tile), 1 (the opener)},
                    # and the line must RENDER — a 1px border in a transparent colour is a width
                    # nobody can see, which a width-only assertion cannot tell from a keyline.
                    if s["borders"] != [0, 1]:
                        fails.append("%s KEYLINES — %s: keylines are ruled ON (tileBorderPx 1) but "
                                     "resolved border widths across %d tiles are %s"
                                     % (SETTINGS_BUCKET, tag, s["tiles"], s["borders"]))
                    if not s["edgeInk"] or any(_rgb_a(c) == 0 for c in s["edgeInk"]):
                        fails.append("%s KEYLINES — %s: keylines are ruled ON but no visible edge "
                                     "colour renders (%s)" % (SETTINGS_BUCKET, tag, s["edgeInk"]))
                if s["shadows"] != ["none"]:
                    fails.append("%s KEYLINES — %s: an opener carries a box-shadow: %s"
                                 % (SETTINGS_BUCKET, tag, s["shadows"]))
                if s["lines"]:
                    fails.append("%s KEYLINES — %s: %d line element(s) render on the wall"
                                 % (SETTINGS_BUCKET, tag, s["lines"]))
                # ⬛ s219-D2 (3) — ROUNDING IS PER THEME NOW. `corners` rounds the PICTURE and
                # leaves the tile square; `capsule` moves canon's container radius onto the TILE
                # and the picture stays square inside it. Both halves are asserted, because either
                # one alone passes in a theme whose radius is 0.
                if ruled["rounding"] == "corners":
                    want_tile, want_img = [0], [s["containerRadius"]]
                else:
                    want_tile, want_img = [s["containerRadius"]], [0]
                if s["tileRadii"] != want_tile:
                    fails.append("%s ROUNDING — %s: rounding is ruled `%s`, so the TILE radius must "
                                 "be %s; resolved %s"
                                 % (SETTINGS_BUCKET, tag, ruled["rounding"], want_tile,
                                    s["tileRadii"]))
                if s["imgRadii"] != want_img:
                    fails.append("%s ROUNDING — %s: rounding is ruled `%s`, so the PICTURE radius "
                                 "must be %s (canon's container radius is %dpx); resolved %s"
                                 % (SETTINGS_BUCKET, tag, ruled["rounding"], want_img,
                                    s["containerRadius"], s["imgRadii"]))
                # ---- the three grounds, each against the TOKEN ITS OWN DIAL NAMES ------------
                for what, dial, got in (("PAGE", "pageBg", s["pageGround"]),
                                        ("BENTO", "bentoBg", s["bentoGround"]),
                                        ("CAPTION", "capBg", (s["capBg"] or [None])[0])):
                    word = ruled[dial]
                    want, why = _want_ground(what, word, s["tokens"])
                    if what == "CAPTION" and len(set(s["capBg"])) > 1:
                        fails.append("%s CAPTION — %s: the 251 captions do not share one ground "
                                     "(%s)" % (SETTINGS_BUCKET, tag, s["capBg"]))
                    if not _same_colour(got, want):
                        fails.append("%s %s GROUND — %s: dial says `%s` (%s), resolved %s"
                                     % (SETTINGS_BUCKET, what, tag, word, why, got))
                # ⚠ THE LITERAL CROSS-CHECK, ASKED WHERE THE RECEIPT CAN ANSWER IT. The twelve #219
                # exports were each taken in the theme they name (unlike two of the #218 four), so
                # the light-mode readback IS evidence here — for every ground EXCEPT a transparent
                # page, where this page deliberately compiles the document ground instead of the
                # keyword (a page body that paints nothing falls through to the UA canvas). That
                # divergence is DECLARED, not skipped in silence.
                rec = foundations.RECEIPT_RESOLVED["gallery"][theme]
                if mode == "light":
                    if ruled["pageBg"] != "transparent":
                        if not _same_colour(s["pageGround"], rec["pageBackground"]):
                            fails.append("%s PAGE GROUND — %s: Dave's export resolved %s; the page "
                                         "resolves %s" % (SETTINGS_BUCKET, tag,
                                                          rec["pageBackground"], s["pageGround"]))
                    else:
                        lines.append("     ⚠ %s: the export resolved pageBackground %s "
                                     "(transparent); this page compiles the DOCUMENT ground "
                                     "instead — declared divergence, %s"
                                     % (theme, rec["pageBackground"], s["pageGround"]))
                    if not _same_colour((s["capBg"] or [None])[0], rec["captionBackground"]):
                        fails.append("%s CAPTION — %s: Dave's export resolved captionBackground "
                                     "%s; the page resolves %s"
                                     % (SETTINGS_BUCKET, tag, rec["captionBackground"],
                                        (s["capBg"] or [None])[0]))
                # ---- the caption INK, and its CONTRAST — the sweep is BLOCKING (#219) --------
                want_ink = s["tokens"].get(foundations.CAP_INK[0])
                if len(set(s["capInk"])) != 1 or not _same_colour(s["capInk"][0], want_ink):
                    fails.append("%s CAPTION INK — %s: the ruled ink is %s (%s); resolved %s"
                                 % (SETTINGS_BUCKET, tag, foundations.CAP_INK[0], want_ink,
                                    s["capInk"]))
                # The caption's EFFECTIVE ground: its own, unless that is transparent — in which
                # case the ink sits on whatever is behind it (the bento ground, itself possibly
                # transparent, then the page). Measured through the same fallback chain the eye
                # sees, never assumed to be the caption's own declaration.
                eff = _effective_ground([(s["capBg"] or [None])[0], s["bentoGround"],
                                         s["pageGround"]])
                cr = ratio(_rgb(s["capInk"][0]), _rgb(eff)) if (s["capInk"] and eff) else None
                if cr is not None and cr < 4.5:
                    fails.append("%s CONTRAST — %s: caption ink %s on %s is %.2f:1, below WCAG AA "
                                 "4.5:1 for body text" % (SETTINGS_BUCKET, tag, s["capInk"][0],
                                                          eff, cr))
                if s["capMin"] != [86]:
                    fails.append("%s CAPTION SPACE — %s: canon's ruled gallery caption block is "
                                 "86px (s217-D3); resolved %s"
                                 % (SETTINGS_BUCKET, tag, s["capMin"]))
                lines.append("  %-22s gutter %3dpx (var %-5s) · tiles %3d · borders %s · "
                             "tileR %s · imgR %s · page %s · bento %s · cap %s ink %s · "
                             "contrast %s · space %s"
                             % (tag, s["gutter"], s["gutterVar"] or "-", s["tiles"], s["borders"],
                                s["tileRadii"], s["imgRadii"], s["pageGround"], s["bentoGround"],
                                s["capBg"], s["capInk"], cr, s["capMin"]))
                if shots:
                    pg.screenshot(path=os.path.join(shots, "photography-%s-%s.png"
                                                    % (theme, mode)), full_page=False)

        # ---- 3 · THE PAINT FOLLOWED THE THEME ------------------------------------------------
        for theme, g in grounds.items():
            if g.get("light") == g.get("dark"):
                fails.append("THEME PAINT — %s: light and dark resolve the SAME page ground (%s); "
                             "a page that fell back everywhere would read exactly like this"
                             % (theme, g.get("light")))
        b.close()
    return fails, lines


def _rgb(s):
    n = [int(float(x)) for x in re.findall(r"[\d.]+", s or "")[:3]]
    return tuple(n) if len(n) == 3 else None


def _rgb_a(s):
    """-> the alpha channel of an rgb()/rgba() paint; 1 when none is stated. A 1px border in a
    fully transparent colour is a WIDTH, not a keyline, and only alpha can tell them apart."""
    n = re.findall(r"[\d.]+", s or "")
    return float(n[3]) if len(n) >= 4 else 1.0


def _effective_ground(chain):
    """-> the first paint in `chain` that is not fully transparent, i.e. what the eye actually sees
    behind the ink. ⛔ NOT the caption's own declaration: a transparent caption's ink sits on the
    bento ground, and on the page ground when that is transparent too. Asking the declaration
    would score the contrast of a colour nothing renders in."""
    for c in chain:
        if c and _rgb_a(c) > 0:
            return c
    return None


def lum(rgb):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])


def ratio(a, b):
    """-> WCAG 2.1 contrast ratio, computed here rather than imported so the probe carries no
    dependency a CI runner might not have. Cross-checked against knowledge/_contrast_utils.py."""
    if not a or not b:
        return None
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


# The token behind each background dial word — the explorer's OWN palette, read from the module
# that owns it, so this probe cannot hold a fourth opinion about what `grey` means.
# ⚠ `transparent` has no token; on the PAGE it compiles to the document ground (see
# gen_foundations_217.page_bg_decl) and everywhere else it stays the keyword.
def _want_ground(what, word, tokens):
    """-> (expected colour, why) for one ground in one state."""
    if word == "transparent":
        if what == "PAGE":
            return (tokens.get("--background-default"),
                    "a transparent PAGE ground compiles to --background-default: a body that "
                    "paints nothing falls through to the UA canvas")
        return ("rgba(0, 0, 0, 0)", "transparent")
    for value, _label, token in foundations.matrix.BACKGROUNDS:
        if value == word:
            return (tokens.get(token), token)
    raise KeyError("background %r is not a ruled dial word" % word)


def _css_rgb(hexs):
    h = hexs.lstrip("#")
    return "rgb(%d, %d, %d)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _same_colour(a, b):
    """`--surface-raised` arrives as a hex from the custom property and as rgb() from a paint."""
    if not a or not b:
        return False
    if b.startswith("#"):
        b = _css_rgb(b)
    return _rgb(a) == _rgb(b)


# ---------------------------------------------------------------------------- main
def main():
    argv = sys.argv[1:]
    mutation = "--settings-mutation" in argv
    default_mutation = "--default-mutation" in argv
    themes = THEMES
    if "--themes" in argv:
        themes = [t.strip() for t in argv[argv.index("--themes") + 1].split(",") if t.strip()]
        unknown = [t for t in themes if t not in THEMES]
        if unknown:
            sys.exit("verify_photography_218: unknown theme(s) %s" % unknown)
    shots = argv[argv.index("--shots") + 1] if "--shots" in argv else None

    fails, lines = [], []
    if mutation:
        if not os.path.exists(MUTANT):
            sys.exit("verify_photography_218: no mutant at %s — run\n"
                     "  BM_MUTANT_DIR=%s python3 knowledge/_render/gen_foundations_217.py "
                     "--break-settings" % (MUTANT, MUT_DIR))
        print("verify_photography_218 — ⬛ MUTATION ARM, driving %s" % MUTANT)
        fails, lines = drive(MUTANT, themes, shots)
    elif default_mutation:
        if not os.path.exists(MUTANT_DEFAULT):
            sys.exit("verify_photography_218: no mutant at %s — run\n"
                     "  BM_MUTANT_DIR=%s python3 knowledge/_render/gen_foundations_217.py "
                     "--break-default" % (MUTANT_DEFAULT, MUT_DIR))
        print("verify_photography_218 — ⬛ MINTED-DEFAULT ARM, driving %s" % MUTANT_DEFAULT)
        fails, lines = drive(MUTANT_DEFAULT, themes, shots)
    elif "--static" in argv:
        print("verify_photography_218 — static half, over the SHIPPED file")
        fails, lines = static_checks(open(PAGE, encoding="utf-8").read())
    else:
        print("verify_photography_218 — driving %s, themes %s" % (PAGE, ",".join(themes)))
        fails, lines = drive(PAGE, themes, shots)

    for l in lines:
        print(l)

    if default_mutation:
        # ⛔ THE SHARPER ARM. The block is intact and ONE ruled default is wrong, so the required
        # red is not "a SETTINGS assertion" but specifically the CAPTION one, in the theme that was
        # mutated. Anything else failing means the arm changed something it should not have; the
        # caption assertion NOT failing means the probe is measuring "a block exists"
        # ([[mutation-tests-the-clause-not-the-feature]]).
        named = [f for f in fails if f.startswith("%s CAPTION" % SETTINGS_BUCKET)]
        print()
        for f in fails:
            print("  %s %s" % ("⬛" if f in named else "·", f))
        if not named:
            print("\n❌ MINTED-DEFAULT ARM DID NOT GO RED — mono's caption ground was moved off the "
                  "ruled token and not one %s CAPTION assertion failed. The probe is testing that "
                  "a settings block exists, not that the RULED DEFAULT reached the paint."
                  % SETTINGS_BUCKET)
            return 1
        print("\n✅ MINTED-DEFAULT ARM RED AS REQUIRED — %d %s CAPTION assertion(s) failed by name"
              % (len(named), SETTINGS_BUCKET))
        return 0

    if mutation:
        # ⛔ THE ARM MUST GO RED FOR THE RIGHT REASON. Bucketed on the name: "something failed" in
        # a mutant is worthless evidence — the mutant differs from the page and something always
        # could. What is REQUIRED is that the SETTINGS assertions are the ones that broke.
        named = [f for f in fails if f.startswith(SETTINGS_BUCKET)]
        print()
        for f in fails:
            print("  %s %s" % ("⬛" if f.startswith(SETTINGS_BUCKET) else "·", f))
        if not named:
            print("\n❌ MUTATION ARM DID NOT GO RED — the settings block was stripped and not one "
                  "%s assertion failed. The assertions are not testing the clause." % SETTINGS_BUCKET)
            return 1
        buckets = sorted({f.split(" —")[0] for f in named})
        print("\n✅ MUTATION ARM RED AS REQUIRED — %d %s assertion(s) failed, by name: %s"
              % (len(named), SETTINGS_BUCKET, "; ".join(buckets)))
        return 0

    if fails:
        print("\n❌ verify_photography_218: %d FAILURE(S)" % len(fails))
        for f in fails:
            print("  ✖ " + f)
        return 1
    print("\n✅ verify_photography_218 OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
