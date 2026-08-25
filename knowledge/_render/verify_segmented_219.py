#!/usr/bin/env python3
"""
verify_segmented_219.py — DRIVES the segmented control's minted concentric pair in a real browser
and refuses a console theme that renders square (#219 lane 1).

WHY IT IS IN THE REPO AND NOT A SCRATCH FILE (s191-D2): a verification that lives only in a sandbox
is a claim, not an instrument. This one can be re-driven after any token or snippet change.

THE FINDING IT EXISTS FOR. The per-theme segmented radius tokens were minted at #200-#202 and then
CONSUMED BY NOTHING — the canon `.cn-segmented-control` block set no border-radius at all, so every
theme rendered square and no gate could see it ([[instrument-without-a-consumer]], the inverted
form: an OUTPUT nothing reads). A textual gate cannot catch this, because there is no wrong value
anywhere: the token is right, the CSS simply never mentions it. Only a rendered document can tell
you that `border-top-left-radius` resolved to 0px on a console segmented track.

WHAT IT DRIVES

 1 · THE FONT, WITH TWO CONTROLS. `document.fonts.check()` returns true in BOTH the working and the
     broken fontconfig, so it cannot discriminate. The canvas width of the target face must equal
     both aliases and differ from a real control face AND from one that does not exist
     (knowledge/_RUNBOOK-render-verify.md, ASSERT WITH A CONTROL).

 2 · THE CONCENTRIC PAIR, FOUR THEMES x LIGHT/DARK x FOUR SCALES, READ OFF getComputedStyle —
     never off the token file, which would only prove the file agrees with itself. The TRACK's
     resolved radius must equal the theme's minted `border-radius/segmented-container/<scale>` and
     the sliding thumb's must equal `border-radius/segmented-thumb/<scale>`, both read FROM THE
     STORE by this script so a re-mint cannot leave the assertion behind.

 3 · CONSOLE IS NOT SQUARE — stated separately and by name, because it is the actual defect. A
     resolved 0px on a console track at scale s/m/l is a REFUSAL, not a mismatch (the #218 grids
     probe precedent: the clause gets its own named bucket so "something failed" can never be
     mistaken for "the clause failed").

 4 · THE SQUARE THEMES ARE STILL SQUARE. s201-D5: mono / legacy / supercharge floor at 0. A fix
     that rounded everything would satisfy 3 and break the ruling.

 5 · THE HIT ZONE IS THE RULED GEOMETRY — max(44, visual height) read off the ::before's resolved
     min-height (s201-D2 hit zone not visual height; s201-D3 natural above the floor). xs and s
     expand to 44, m sits at 44, l keeps 48.

 6 · THE DIMENSIONS ARE THE MINTED ONES — each scale's resolved track height equals
     `size/segmented-control/<scale>` from the store.

 ⬛ 7 · THE MUTATION ARM. `--mutation` renders a COPY of the review page with one minted radius
     token overwritten to 0 in an injected stylesheet (console, scale s: 8px -> 0). Assertions 2
     and 3 MUST go red there, by name. With `--mutation` the exit code is INVERTED: green means the
     arm went red as required. A gate that has never been seen to fail is not a gate
     ([[instrument-without-a-consumer]]); and this arm bites the CLAUSE (a console track that
     resolves 0), not merely the feature ([[mutation-tests-the-clause-not-the-feature]]).
     ⚠ The mutant is written under BM_MUTANT_DIR (default /var/tmp) and /var/tmp is SHARED ACROSS
     SESSIONS — a foreign mutant is stale and may be unwritable. Use a session-suffixed dir.

Usage:
  python3 knowledge/_render/verify_segmented_219.py
  BM_MUTANT_DIR=/var/tmp/mut-s219l1 python3 knowledge/_render/verify_segmented_219.py --mutation

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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TOK = os.path.join(ROOT, "knowledge", "tokens")
PAGE = os.path.join(ROOT, "reviews", "SEGMENTED-ADOPTION-2026-08-25-v1.html")
MUT_DIR = os.environ.get("BM_MUTANT_DIR", "/var/tmp")
MUTANT = os.path.join(MUT_DIR, "SEGMENTED-ADOPTION-RADIUS-BROKEN.html")
MUTANT_CSS = os.path.join(MUT_DIR, "canon-SEG-RADIUS-BROKEN.css")

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]
SCALES = ["xs", "s", "m", "l"]

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""

MEASURE = """() => {
  const out = [];
  document.querySelectorAll('section.theme').forEach(sec => {
    const th = sec.dataset.apolloTheme, md = sec.dataset.theme;
    ['xs','s','m','l'].forEach(sc => {
      const seg = sec.querySelector('.tier:not(.before-tier) .seg.' + sc);
      if (!seg) return;
      const cs = getComputedStyle(seg);
      const ind = seg.querySelector('.ind');
      const btn = seg.querySelector('button');
      out.push({theme: th, mode: md, scale: sc,
                track: cs.borderTopLeftRadius,
                height: cs.height,
                thumb: ind ? getComputedStyle(ind).borderTopLeftRadius : null,
                hit: btn ? getComputedStyle(btn, '::before').minHeight : null});
    });
  });
  return out;
}"""


def store(name):
    return json.load(open(os.path.join(TOK, name)))


def px(v):
    """DTCG value -> the string getComputedStyle returns ('0px', '8px')."""
    if isinstance(v, str):
        v = v[:-2] if v.endswith("px") else v
    return "%gpx" % float(v)


def expected():
    """The per-theme truth, READ FROM THE STORE — base layout.json overlaid by the theme file.

    Reading it here rather than typing it in is what stops the assertion outliving a re-mint
    ([[conclusions-are-debt-s129-d5]]): re-tune the tokens and this probe re-tunes with them.
    """
    layout, spacing = store("layout.json"), store("spacing.json")
    base = {}
    for sc in SCALES:
        base[sc] = {
            "track": px(layout["border-radius"]["segmented-container"][sc]["$value"]),
            "thumb": px(layout["border-radius"]["segmented-thumb"][sc]["$value"]),
            "height": px(layout["size"]["segmented-control"][sc]["$value"]),
            "pad": px(spacing["padding"]["segmented-control"][sc]["$value"]),
        }
    hit_floor = float(layout["target"]["min"]["$value"][:-2])
    out = {}
    for theme in THEMES:
        out[theme] = {sc: dict(base[sc]) for sc in SCALES}
        ov = os.path.join(TOK, "themes", "apollo-%s.overrides.json" % theme)
        if os.path.exists(ov):
            paths = json.load(open(ov)).get("overrides", {})
            for sc in SCALES:
                for key, tp in (("track", "border-radius/segmented-container/%s" % sc),
                                ("thumb", "border-radius/segmented-thumb/%s" % sc),
                                ("height", "size/segmented-control/%s" % sc)):
                    if tp in paths:
                        out[theme][sc][key] = px(paths[tp]["$value"])
        for sc in SCALES:
            h = float(out[theme][sc]["height"][:-2])
            out[theme][sc]["hit"] = "%gpx" % max(hit_floor, h)
    return out


def shell_path():
    for r in [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
              os.path.expanduser("~/.cache/ms-playwright")]:
        if r:
            hit = glob.glob(os.path.join(
                r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
            if hit:
                return hit[0]
    return None


def write_mutant():
    """THE ONE BROKEN THING: console's scale-s container radius, 8px -> 0, in a MUTANT COPY of the
    generated canon.css — never in the tree.

    ⚠ WHY IT IS THE FLATTENED LITERAL AND NOT THE TOKEN VAR. `gen_theme_cascade.py` PROJECTS each
    component's manifest vars per theme, so `[data-apollo-theme="console"] .cn-segmented-control`
    carries `--seg-rad-s: 8px` as a CONCRETE number at specificity (0,2,0). That projection
    short-circuits `--border-radius-segmented-container-s` entirely: overriding the token var, as
    the first version of this arm did, changed nothing and the arm reported a false negative. The
    delivered value IS the projected literal, so that is what a mutation must break. (This is
    s200-D1's mint-time derivation working exactly as ruled — the disk carries plain numbers — and
    it is worth knowing that the .cn-* scope does not read the token var at runtime.)

    ⛔ THE HREFS ARE ABSOLUTISED. The mutant lives in BM_MUTANT_DIR, not beside the page, so the
    review page's `../knowledge/canon/canon.css` would resolve nowhere and the mutant would render
    with canon SILENTLY INERT. The first version did exactly that and went "green" on the failures
    of an unstyled document — a mutation arm that goes red for the wrong reason proves nothing
    ([[mutation-tests-the-clause-not-the-feature]]). The contamination guard in main() is the other
    half of that lesson: exactly one cell may fail, or the arm is worthless.
    """
    os.makedirs(MUT_DIR, exist_ok=True)
    canon = open(os.path.join(ROOT, "knowledge", "canon", "canon.css")).read()
    before = canon.count("  --seg-rad-s: 8px;")
    if before == 0:
        raise SystemExit("verify_segmented_219: REFUSED — no projected `--seg-rad-s: 8px` in "
                         "canon.css to break; the projection shape changed, fix the arm.")
    open(MUTANT_CSS, "w").write(canon.replace("  --seg-rad-s: 8px;", "  --seg-rad-s: 0;"))
    src = open(PAGE).read()
    reviews = os.path.dirname(os.path.abspath(PAGE))
    src = src.replace('href="../knowledge/canon/canon.css"', 'href="file://' + MUTANT_CSS + '"')
    src = src.replace('href="../knowledge/',
                      'href="file://' + os.path.dirname(reviews) + '/knowledge/')
    open(MUTANT, "w").write(src)
    print("mutant: %s (canon copy with %d projected `--seg-rad-s` forced to 0)" % (MUTANT, before))
    return MUTANT


def main():
    mutation = "--mutation" in sys.argv
    src = write_mutant() if mutation else PAGE
    if not os.path.exists(src):
        print("REFUSED — no page at %s" % src)
        sys.exit(1)
    exp = expected()
    from playwright.sync_api import sync_playwright
    fails, lines = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1400, "height": 1000})
        # ⛔ goto file:// ONLY — set_content() gives the document no URL, so ../knowledge/canon/
        # never resolves and the page renders with canon silently inert.
        pg.goto("file://" + os.path.abspath(src))
        pg.wait_for_timeout(900)
        f = pg.evaluate(FONT_PROBE)
        if not (f["target"] == f["alias_uf"] == f["alias_font"]
                and f["target"] != f["control_real"] and f["target"] != f["control_absent"]):
            print("REFUSED — the font probe cannot discriminate: %r" % f)
            b.close()
            sys.exit(1)
        print("font probe (controls pass): %r" % f)
        rows = pg.evaluate(MEASURE)
        b.close()

    if not rows:
        print("REFUSED — the page rendered no measurable segmented control")
        sys.exit(1)

    for r in rows:
        e = exp[r["theme"]][r["scale"]]
        tag = "%s/%s/%s" % (r["theme"], r["mode"], r["scale"])
        if r["track"] != e["track"]:
            fails.append("radius-pair  %s track %s != minted %s" % (tag, r["track"], e["track"]))
        if r["thumb"] != e["thumb"]:
            fails.append("radius-pair  %s thumb %s != minted %s" % (tag, r["thumb"], e["thumb"]))
        if r["height"] != e["height"]:
            fails.append("dimension    %s height %s != minted %s" % (tag, r["height"], e["height"]))
        if r["hit"] != e["hit"]:
            fails.append("hit-zone     %s ::before min-height %s != max(44, %s) = %s"
                         % (tag, r["hit"], e["height"], e["hit"]))
        # THE CLAUSE, IN ITS OWN BUCKET — a console track that resolves square is the defect.
        if r["theme"] == "console" and e["track"] != "0px" and r["track"] == "0px":
            fails.append("console-square  %s renders SQUARE — the minted %s was not consumed"
                         % (tag, e["track"]))
        if r["theme"] != "console" and r["track"] != "0px":
            fails.append("squares-stay-square  %s resolved %s; s201-D5 floors it at 0"
                         % (tag, r["track"]))
        lines.append("  %-28s track %-5s thumb %-5s h %-5s hit %-5s" %
                     (tag, r["track"], r["thumb"], r["height"], r["hit"]))

    print("\n".join(lines))
    print("\n%d measurement(s) across %d theme x mode x scale cells" % (len(rows) * 4, len(rows)))
    if fails:
        print("\nFAIL — %d:" % len(fails))
        for x in fails:
            print("  x " + x)
    else:
        print("\nPASS — every track and thumb radius equals its theme's minted token; console "
              "rounds, the three square themes stay square, hit zone = max(44, height).")

    if mutation:
        # THE ARM MUST BITE THE CLAUSE AND NOTHING ELSE. Exactly one token was broken, so exactly
        # the console scale-s cells may fail; any OTHER failure means the mutant is contaminated
        # (a stale /var/tmp copy, or canon.css not resolving) and its red is worthless.
        named = [x for x in fails if ("console/light/s" in x or "console/dark/s" in x)
                 and x.startswith(("radius-pair", "console-square"))]
        stray = [x for x in fails if not ("console/light/s" in x or "console/dark/s" in x)]
        if stray:
            print("\nMUTATION ARM CONTAMINATED — %d failure(s) outside the one broken cell; the "
                  "mutant is not a one-token delta, so its red proves nothing. First 3:" % len(stray))
            for x in stray[:3]:
                print("  ! " + x)
            sys.exit(1)
        if named:
            print("\nMUTATION ARM GREEN — the probe went RED on the broken token, BY NAME and "
                  "ONLY there (%d failure(s), all in console scale s)." % len(named))
            sys.exit(0)
        print("\nMUTATION ARM FAILED — the probe did NOT catch a console scale-s radius forced "
              "to 0. The assertion is decorative.")
        sys.exit(1)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
