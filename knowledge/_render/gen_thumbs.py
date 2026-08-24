#!/usr/bin/env python3
"""
gen_thumbs.py — one small screenshot per component, into showroom/_thumbs/.

s215-D5 (3), Dave 2026-08-22: thumbnail-first browsing ships. The library index
(knowledge/_render/gen_library_214.py) ADDRESSES `_thumbs/<slug>.png`; this script is what
actually puts the pixels there. A component with no thumbnail degrades to a "no thumbnail"
placeholder on its card — nothing is ever faked.

WHAT IT SHOOTS — the REAL page, never a re-drawing [[specimen-starts-from-reference]]
  `file://…/showroom/<slug>.html#theme=mono&m=light&chrome=0` — the component's own generated
  showroom page in embed mode, so the page's own bar is hidden and the pane fills the frame.
  ⛔ `goto file://` ONLY. `page.set_content()` is BANNED here: it gives the document no URL,
  so `../knowledge/canon/type.css` never resolves and the shot renders with the type composites
  silently inert (the srcdoc base-URL trap, gen_showroom.py's big comment block).

LIGHT MODE, ONE WIDTH, SMALL — the ruling asks for no more. 640×400 CSS px at
device_scale_factor 0.5 = a 320×200 PNG straight out of chromium, no resampling step and no
Pillow dependency.

THE FONT PROBE IS A CONTROL PROBE, NOT A BOOLEAN — knowledge/_RUNBOOK-render-verify.md.
`document.fonts.check()` returns true in both the working and the broken fontconfig, so this
measures a canvas string in the target face and in two controls (a real different face, and a
face that does not exist) and requires the target to differ from BOTH. It runs ONCE per
invocation, before any shot, and refuses the run if it cannot discriminate.

SANDBOX CALLS DIE AT ~45s WALL — so this is CHUNKED and RESUMABLE:
  python3 knowledge/_render/gen_thumbs.py --range 0:20      # slugs [0,20) of the sorted list
  python3 knowledge/_render/gen_thumbs.py --resume --range 0:20   # …skipping ones already shot
  python3 knowledge/_render/gen_thumbs.py --list            # print the sorted slug list + count
Env (see the runbook; every bash call must re-export them):
  PLAYWRIGHT_BROWSERS_PATH · PYTHONPATH · LD_LIBRARY_PATH · FONTCONFIG_FILE · TMPDIR
  THUMB_SHELL — optional explicit path to headless_shell.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SHOWROOM = os.path.join(ROOT, "showroom")
THUMBS = os.path.join(SHOWROOM, "_thumbs")

WIDTH, HEIGHT, SCALE = 640, 400, 0.5      # -> 320×200 PNG
SETTLE_MS = 900                            # let CSS entry motion settle before the shot

FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return Math.round(c.measureText('Handgloves 12345').width); };
  return {target: m('HSBC_MtUnivers_Latin'),
          alias_uf: m('"Univers Next HSBC"'),
          alias_font: m('"Univers Next for HSBC"'),
          control_real: m('DejaVu Sans'),
          control_absent: m('"No Such Face Anywhere XYZ"')};
}"""


def pages():
    """slug -> page path RELATIVE to showroom/, for everything the library index addresses.

    #217 — the library gained a Foundations tier whose entries are NOT components: they have no
    snippet and their pages live in `showroom/_foundations/` (a subdirectory, deliberately, so
    gen_showroom.py's non-recursive orphan prune cannot delete them). They carry `_thumbs/<slug>.png`
    like every other card, so they are shot here. The list of them is imported from
    gen_library_214.FOUNDATIONS — ONE list, never a second copy.
    ⚠ They sort into the middle of the slug list, so a `--range` chunk boundary from a run before
    #217 no longer covers the same pages. Ranges were always ad-hoc; this is the caveat.
    """
    out = {os.path.basename(p)[:-5]: os.path.basename(p)
           for p in glob.glob(os.path.join(SHOWROOM, "*.html"))
           if os.path.basename(p) != "index.html"}
    sys.path.insert(0, HERE)
    import gen_library_214 as library
    for f in library.FOUNDATIONS:
        out[f["slug"]] = "%s/%s" % (library.FOUNDATION_DIR, f["file"])
    return out


def slugs():
    return sorted(pages())


def shell_path():
    explicit = os.environ.get("THUMB_SHELL")
    if explicit:
        return explicit
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
             os.path.expanduser("~/.cache/ms-playwright")]
    for r in roots:
        if not r:
            continue
        hit = glob.glob(os.path.join(r, "chromium_headless_shell-*/chrome-linux/headless_shell"))
        if hit:
            return hit[0]
    return None


def check_font(page):
    """Control probe — the runbook's rule: assert against controls, never a boolean."""
    m = page.evaluate(FONT_PROBE)
    ok = (m["target"] == m["alias_uf"] == m["alias_font"]
          and m["target"] != m["control_real"]
          and m["target"] != m["control_absent"])
    if not ok:
        print("gen_thumbs REFUSES THE RUN — the font probe cannot discriminate: %r" % m)
        print("  Both aliases must land on the target width and on NEITHER control.")
        print("  See knowledge/_RUNBOOK-render-verify.md § ASSERT WITH A CONTROL.")
        sys.exit(1)
    return m


def main():
    argv = sys.argv[1:]
    if "--list" in argv:
        ss = slugs()
        print("\n".join(ss))
        print("# %d page(s) the library index addresses (components + foundations)" % len(ss))
        return
    lo, hi = 0, None
    for a in argv:
        if a.startswith("--range"):
            spec = a.split("=", 1)[1] if "=" in a else argv[argv.index(a) + 1]
            lo, _, h = spec.partition(":")
            lo = int(lo or 0)
            hi = int(h) if h else None
    resume = "--resume" in argv

    PAGES = pages()
    todo = slugs()[lo:hi]
    if resume:
        todo = [s for s in todo if not os.path.exists(os.path.join(THUMBS, s + ".png"))]
    if not todo:
        print("gen_thumbs: nothing to do (range %s:%s, resume=%s)" % (lo, hi, resume))
        return

    from playwright.sync_api import sync_playwright     # imported late: --list needs no browser
    sh = shell_path()
    os.makedirs(THUMBS, exist_ok=True)
    done, failed = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=sh, headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=SCALE)
        probed = False
        for slug in todo:
            url = ("file://" + os.path.join(SHOWROOM, PAGES[slug])
                   + "#theme=mono&m=light&chrome=0")
            try:
                pg.goto(url)                            # goto file:// ONLY — never set_content
                pg.wait_for_timeout(SETTLE_MS)
                if not probed:
                    print("gen_thumbs: font probe %r" % (check_font(pg),))
                    probed = True
                pg.screenshot(path=os.path.join(THUMBS, slug + ".png"))
                done.append(slug)
            except Exception as e:                      # a crash is not a fail — name it
                failed.append((slug, type(e).__name__ + ": " + str(e)[:120]))
        b.close()
    print("gen_thumbs: %d shot, %d failed -> showroom/_thumbs/" % (len(done), len(failed)))
    for slug, why in failed:
        print("   ❌ %s — %s" % (slug, why))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
