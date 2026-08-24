#!/usr/bin/env python3
"""
verify_foundations_217.py — drives the two Foundations pages in FOUR THEMES × LIGHT/DARK and
measures what a screenshot alone cannot tell you.

WHY IT IS IN THE REPO AND NOT A SCRATCH FILE (s191-D2): a verification that lives only in a
sandbox is a claim, not an instrument — it cannot be re-driven after the sandbox is wiped, so
its green expires with the session. This one can be re-run.

WHAT IT MEASURES, PER THEME × MODE (8 states per page)

 1 · THE FONT, WITH CONTROLS — `document.fonts.check()` returns true in BOTH the working and
     the broken fontconfig, so it does not discriminate. The canvas width of the target face
     must equal both aliases and differ from a real control face AND from a nonexistent one.
     (knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL.)

 2 · THE DANGLING-VAR PROBE, AND IT IS THE POINT OF THIS SCRIPT. The pages bind page-local
     names to CANON properties with literal fallbacks, so nothing can render silent black
     ([[dangling-dataviz-var-renders-silent-black]]). But a fallback is a TRAP AS WELL AS A
     FENCE: if a canon property stopped resolving, the page would quietly serve the LIGHT
     fallback in a DARK theme and look merely wrong rather than broken, and no gate would fire.
     So every foreign property the stylesheet reads is resolved IN THE LIVE DOCUMENT, in every
     theme and both modes, and an empty resolution is a FAILURE — not a shrug.

 3 · THE PAINT ACTUALLY FOLLOWED THE THEME — the resolved page background must not be the same
     value in light and dark for a given theme. A theme that "works" because everything fell
     back to white would pass every textual gate; this is what catches it.

 4 · TEXT CONTRAST, MEASURED — body ink on page ground, per state, reported as a ratio. Reported
     rather than gated: these pages author no colour of their own, so a low reading is a TOKEN
     finding for Dave, not a defect this page may fix.

 5 · THE LIGHTBOX IS REACHABLE — the popover is opened by its invoker command and its computed
     display is read back. A lightbox that cannot open is the one defect a still screenshot of
     the grid can never show.

Chunked, because sandbox bash calls die near 45 s wall:
  python3 knowledge/_render/verify_foundations_217.py --page photography
  python3 knowledge/_render/verify_foundations_217.py --page logos
  python3 knowledge/_render/verify_foundations_217.py --page logos --shots /var/tmp/shots-217

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
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FOUND = os.path.join(ROOT, "showroom", "_foundations")
sys.path.insert(0, os.path.join(ROOT, "knowledge", "canon"))
from gen_canon_bento import caption_space  # noqa: E402

# The RULED caption block and the clamp DERIVED from it (s217-D3). Read from the store via the
# canon generator — never retyped here, or the probe and the ruling become two numbers.
CAPTION_SPACE, CAPTION_LINES = caption_space()
THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]

# s217-D3 — the photography wall is role=gallery, so the RADIUS SITS ON THE TILES and the
# container is square. border-radius/container: console overrides to 20, the other three follow
# the base alias (0). ⚠ MEASURED IN EVERY THEME: a role rule that never lands leaves the base
# grammar silently in force, and console is the only theme where the number is non-zero — which
# is exactly why an accidental inversion would hide in the other three.
EXPECT_RADIUS = {"mono": 0, "legacy": 0, "supercharge": 0, "console": 20}

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""


def foreign_props(page_src):
    """The CANON properties this page reads — derived from the page's OWN stylesheet, so the
    probe cannot drift from what actually ships.

    ⚠ `--bento-*` IS EXCLUDED, and the reason is a real false red (#217, s217-D3). This sweep
    resolves every name against `document.body`, which is the right test for a ROOT-tier token.
    The bento dials are not root-tier: canon declares them on `.c-bento` and
    `--bento-caption-lines` on `.c-bento__caption`, so they resolve empty on the body BY DESIGN
    and the sweep reported eight dangles for a page that was behaving exactly as ruled. They are
    probed on their own elements instead (the inline `bento()` probe), which is the honest question — a
    scoped property is not a dangling one. [[unmatched-grep-is-not-an-absence]], element form."""
    css = page_src.split("<style>", 1)[1].split("</style>", 1)[0]
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    read = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    return sorted(p for p in (read - declared) if not p.startswith("--bento-"))


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


def main():
    argv = sys.argv[1:]
    name = "photography"
    shots = None
    for i, a in enumerate(argv):
        if a == "--page":
            name = argv[i + 1]
        if a == "--shots":
            shots = argv[i + 1]
    src = os.path.join(FOUND, name + ".html")
    if not os.path.exists(src):
        sys.exit("verify_foundations_217: no such page — %s" % src)
    props = foreign_props(open(src, encoding="utf-8").read())
    if shots:
        os.makedirs(shots, exist_ok=True)

    from playwright.sync_api import sync_playwright
    fails, lines = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell_path(), headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1180, "height": 900})
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
                pg.evaluate("h => { location.hash = h; }",
                            "#theme=%s&m=%s" % (theme, mode))
                pg.wait_for_timeout(320)
                r = pg.evaluate(
                    """(props) => {
                      const b = document.body, m = document.querySelector('main');
                      const cs = getComputedStyle(m);
                      // s217-D3 — the ROLE, measured on its own elements. The bento dials are
                      // scoped to `.c-bento` / `.c-bento__caption`, so asking the BODY for them
                      // is the wrong question and answers EMPTY for a page behaving as ruled.
                      const px = v => Math.round(parseFloat(v) || 0);
                      const bento = () => {
                        const w = document.querySelector('.c-bento[data-bento-role="gallery"]');
                        if (!w) return null;
                        const g = Array.from(w.children).find(
                            e => e.classList.contains('c-bento__grid'));
                        const t = g && Array.from(g.children).find(
                            e => e.classList.contains('c-bento__tile'));
                        const cap = w.querySelector('.c-bento__caption');
                        return {
                          radius: px(getComputedStyle(w).borderTopLeftRadius),
                          overflow: getComputedStyle(w).overflowX,
                          tileRadius: t ? px(getComputedStyle(t).borderTopLeftRadius) : -1,
                          gutter: g ? px(getComputedStyle(g).columnGap) : -1,
                          capMin: cap ? px(getComputedStyle(cap).minHeight) : -1,
                          capH: cap ? Math.round(cap.getBoundingClientRect().height) : -1,
                          capLines: cap ? getComputedStyle(cap)
                              .getPropertyValue('--bento-caption-lines').trim() : '',
                          tall: Array.from(w.querySelectorAll('[data-r="2"]')).length
                        };
                      };
                      const bad = props.filter(p => !getComputedStyle(b).getPropertyValue(p).trim());
                      const lb = document.querySelector('[popover]');
                      let lbOpen = 'n/a';
                      if (lb) {
                        const btn = document.querySelector('[command="show-popover"]');
                        if (btn) { btn.click();
                          lbOpen = getComputedStyle(lb).display !== 'none' ? 'open' : 'DID NOT OPEN';
                          if (lb.hidePopover) { try { lb.hidePopover(); } catch (e) {} } }
                      }
                      return {theme: document.documentElement.getAttribute('data-apollo-theme'),
                              mode: b.getAttribute('data-theme'),
                              ground: getComputedStyle(b).backgroundColor,
                              ink: cs.color, unresolved: bad, lightbox: lbOpen,
                              bento: bento()};
                    }""", props)
                state = "%s/%s" % (theme, mode)
                if r["theme"] != theme or r["mode"] != mode:
                    fails.append("%s — the hashchange broadcast did not land (got %s/%s)"
                                 % (state, r["theme"], r["mode"]))
                if r["unresolved"]:
                    fails.append("%s — ⛔ DANGLING: %s resolved EMPTY (silent-fallback class)"
                                 % (state, ", ".join(r["unresolved"])))
                bt = r.get("bento")
                if name == "photography":
                    if not bt:
                        fails.append("%s — no role=gallery wall on the photography page: the "
                                     "s217-D3 re-point did not reach the document" % state)
                    else:
                        if bt["radius"] != 0:
                            fails.append("%s — gallery CONTAINER radius %dpx, expected 0: "
                                         "s217-D3 puts this role's radius on the TILES"
                                         % (state, bt["radius"]))
                        if bt["tileRadius"] != EXPECT_RADIUS[theme]:
                            fails.append("%s — gallery TILE radius %dpx, expected %dpx"
                                         % (state, bt["tileRadius"], EXPECT_RADIUS[theme]))
                        if bt["capMin"] != CAPTION_SPACE:
                            fails.append("%s — caption min-height %dpx, expected %dpx (s217-D3). "
                                         "The ruled number did not reach the page from the store."
                                         % (state, bt["capMin"], CAPTION_SPACE))
                        if bt["capH"] < CAPTION_SPACE:
                            fails.append("%s — caption block RENDERS %dpx, below the ruled %dpx"
                                         % (state, bt["capH"], CAPTION_SPACE))
                        if bt["capLines"] != str(CAPTION_LINES):
                            fails.append("%s — --bento-caption-lines resolves %r on the caption, "
                                         "expected %r: the DERIVED clamp did not reach the page"
                                         % (state, bt["capLines"], str(CAPTION_LINES)))
                        # ⚠ THE POSITIVE HALF OF THE GALLERY RULING. Squaring is off here; the
                        # ASPECT mapping is not, and they are different mechanisms.
                        if not bt["tall"]:
                            fails.append("%s — no two-row tile in the gallery wall: the portrait "
                                         "mapping did not survive the squaring exemption" % state)
                if r["lightbox"] == "DID NOT OPEN":
                    fails.append("%s — the popover lightbox did not open" % state)
                g, ink = parse_rgb(r["ground"]), parse_rgb(r["ink"])
                grounds[state] = r["ground"]
                lines.append("  %-22s ground %-22s ink %-22s contrast %-6s lightbox %s"
                             % (state, r["ground"], r["ink"],
                                ratio(g, ink) if (g and ink) else "?", r["lightbox"]))
                if shots:
                    pg.screenshot(path=os.path.join(
                        shots, "%s-%s-%s.png" % (name, theme, mode)))
        b.close()

    print("page: showroom/_foundations/%s.html" % name)
    print("foreign properties probed per state (%d): %s" % (len(props), ", ".join(props)))
    print("\n".join(lines))
    # 3 · the paint must MOVE between light and dark, or the theme did not reach the page.
    for theme in THEMES:
        a, z = grounds["%s/light" % theme], grounds["%s/dark" % theme]
        if a == z:
            fails.append("%s — light and dark paint the SAME ground (%s): the theme did not "
                         "reach the page, or everything fell back" % (theme, a))
    if fails:
        print("\n%d FAILURE(S):" % len(fails))
        for f_ in fails:
            print("  ❌ " + f_)
        sys.exit(1)
    print("\nOK — %d state(s), no dangling property, theme reached the paint in all four."
          % (len(THEMES) * len(MODES)))


if __name__ == "__main__":
    main()
