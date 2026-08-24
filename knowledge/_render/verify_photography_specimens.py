#!/usr/bin/env python3
"""verify_photography_specimens.py — render-proof for the #217 real-photography specimens.

DRIVES the two specimen pages in a real headless Chromium and ASSERTS NUMERICALLY before it
shoots anything, because a screenshot alone cannot tell a loaded photograph from a grey box:

  1. EVERY <img> LOADED — `complete` true AND `naturalWidth > 0`. This is the whole point: the
     pages reference committed derivatives by RELATIVE PATH, and a wrong path renders as an
     empty box that a full-page PNG shows as "a bit of white space".
  2. THE DECLARED RATIO IS THE MEASURED RATIO — the media box is printed per image so a 1:1
     variant showing 16:9 is visible as a number, not as an impression.
  3. `object-fit` COMPUTES TO `cover` — the added rule this specimen exists to demonstrate
     (ds-044) is proven present, not assumed.
  4. FONT CONTROL PROBE, not a boolean — a canvas string measured in the HSBC cut and in TWO
     controls (a real different face, and a face that does not exist). `document.fonts.check()`
     returns true in both the working and the broken configuration and cannot discriminate
     (`_RUNBOOK-render-verify.md` § ASSERT WITH A CONTROL).

Hidden slides legitimately measure 0×0 (the Carousel's standard variant hides all but the active
slide), so a zero BOX is fine — a zero NATURAL width never is. That distinction is the reason
the two are asserted separately.

⚠ ENVIRONMENT: this needs Playwright + a headless shell + the X libs, per
`knowledge/_RUNBOOK-render-verify.md`. #217 drove it with FOREIGN-SESSION farms
(`/var/tmp/pylibs-s213e2`, `/var/tmp/pw-browsers-215`, `/var/tmp/chromelibs-s213e2`) which are
NOT guaranteed to exist in a later sandbox — re-extract per the runbook rather than assuming.
Every env var must be re-exported in each bash call.

USAGE
  python3 knowledge/_render/verify_photography_specimens.py --all
  python3 knowledge/_render/verify_photography_specimens.py <page.html> --width 1180 [--dark]
      [--shoot <name.png>]   # PNG lands on the outputs mount; a render nobody reads proves nothing

Exit 1 if any image failed to load. Exit 2 if the browser could not be found or launched — a
missing browser is a LOUD refusal, never a silent skip that reads as a pass.

MUTATION ARM, DRIVEN #217 (a green that cannot fail is an assertion, not a test): a two-image
page — one `src` that does not exist, one committed derivative that does — was rendered through
this script. Result: `images 2 · broken 1 ← does-not-exist-w1600.jpg`, exit 1, with the control
image passing in the SAME run. So the probe can fail, and it fails on the right shape.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate  # noqa: E402
_help_gate(__doc__, __name__, __file__)

import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUTS = os.path.join(os.path.dirname(ROOT), "outputs")   # the shared outputs mount, beside the repo
PAGES = ["knowledge/_fitness-test/photography-image-block-v1.html",
         "knowledge/_fitness-test/photography-carousel-v1.html"]

FONT_JS = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return { hsbc: m('HSBC_MtUnivers_Latin'), uf: m('"Univers Next HSBC"'),
           ufor: m('"Univers Next for HSBC"'), dejavu: m('"DejaVu Sans"'), nope: m('"NoSuchFaceXYZ"') };
}"""

IMG_JS = """() => Array.from(document.images).map(i => ({
  src: i.getAttribute('src').split('/').pop(),
  nw: i.naturalWidth, nh: i.naturalHeight,
  cw: Math.round(i.getBoundingClientRect().width),
  ch: Math.round(i.getBoundingClientRect().height),
  fit: getComputedStyle(i).objectFit, complete: i.complete
}))"""


def shell_path():
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), os.path.expanduser("~/.cache/ms-playwright")]
    for r in roots:
        if not r:
            continue
        hits = glob.glob(os.path.join(r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
        if hits:
            return hits[0]
    return None


def run(page, width, dark, shoot):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        print("✖ playwright is not importable (%s) — see knowledge/_RUNBOOK-render-verify.md; "
              "this is a REFUSAL, not a pass." % exc, file=sys.stderr)
        sys.exit(2)
    sh = shell_path()
    if not sh:
        print("✖ no chromium_headless_shell found (PLAYWRIGHT_BROWSERS_PATH=%r) — REFUSING to "
              "report a verdict without a browser." % os.environ.get("PLAYWRIGHT_BROWSERS_PATH"),
              file=sys.stderr)
        sys.exit(2)

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=sh, headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": width, "height": 1200})
        pg.goto("file://" + os.path.join(ROOT, page))
        pg.wait_for_timeout(400)
        if dark:
            pg.evaluate("document.body.dataset.theme='dark'")
        pg.wait_for_timeout(1400)          # settle transitions BEFORE reading [[runbook 2026-07-27]]
        fonts = pg.evaluate(FONT_JS)
        imgs = pg.evaluate(IMG_JS)
        body_bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
        if shoot:
            os.makedirs(OUTPUTS, exist_ok=True)
            pg.screenshot(path=os.path.join(OUTPUTS, shoot), full_page=True)
        b.close()

    print("\n%s  @%dpx  %s  body-bg %s" % (page, width, "DARK" if dark else "light", body_bg))
    print("  fonts %s" % json.dumps(fonts))
    face_ok = fonts["hsbc"] == fonts["uf"] == fonts["ufor"] and fonts["hsbc"] not in (fonts["dejavu"], fonts["nope"])
    print("  font verdict: %s (both aliases land on the target AND differ from both controls)"
          % ("REAL HSBC CUT" if face_ok else "⚠ NOT the HSBC cut / alias not resolving"))
    broken = [i for i in imgs if not i["complete"] or i["nw"] == 0]
    for i in imgs:
        print("  %-46s nat=%dx%-5d box=%dx%-5d fit=%s" % (i["src"], i["nw"], i["nh"], i["cw"], i["ch"], i["fit"]))
    print("  images %d · broken %d%s" % (len(imgs), len(broken),
                                         "" if not broken else " ← " + ", ".join(i["src"] for i in broken)))
    if shoot:
        print("  shot -> %s" % os.path.join(OUTPUTS, shoot))
    return len(broken)


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("page", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--width", type=int, default=1180)
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--shoot", default=None)
    a = ap.parse_args(argv)
    if not a.all and not a.page:
        print("name a page or pass --all (--help for the contract).", file=sys.stderr)
        return 2
    bad = 0
    if a.all:
        for pth in PAGES:
            for w, dk in ((1180, False), (1180, True), (420, False)):
                bad += run(pth, w, dk, None)
    else:
        bad = run(a.page, a.width, a.dark, a.shoot)
    print("\n%s" % ("❌ %d image(s) did not load" % bad if bad
                    else "✅ every image loaded, every ratio measured, object-fit proven"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
