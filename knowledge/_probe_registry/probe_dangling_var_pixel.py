#!/usr/bin/env python3
"""probe_dangling_var_pixel.py — P-3: dangling-var SILENT BLACK, measured FROM PIXELS (W-45).

THE CLASS, from the receipts: `s184-D3`, #184 — a `rect` carrying `fill="var(--status-breach)"`
with the custom property declared NOWHERE paints **pure black**, and **thirteen of thirteen
gates reported a pass** (`knowledge/_DS-IMPROVEMENTS.md:1973`). Black is a plausible chart
colour, so the defect has no signature for a reader who was not hunting it. The static gate
`knowledge/_gate_dataviz_vars.py` (built #190) parses the markup for this class and is the
right first line — but it declares two blind spots in its own docstring: **per-SELECTOR scope**
("declared in the file ⇒ counted as reachable — catching a selector-scope miss needs a render")
and anything a script sets at runtime. THIS PROBE IS THAT RENDER. It asks the BROWSER what the
property resolved to on the element, in the element's own cascade, and then asks the PIXEL what
was actually painted.

TWO LEGS, and the second is the one that makes it a pixel probe:
  LEG 1 · CASCADE — in-page, for every colour-bearing SVG presentation attribute containing
    `var(--x)`: `getComputedStyle(el).getPropertyValue('--x')`. Empty AND no fallback arm ⇒
    SUSPECT. ⚠ The fallback arm is checked because the #204 verifier's own first pass produced
    a FALSE POSITIVE on `width:var(--demo-width, 460px)` — "a regex that ignores the fallback
    arm is exactly how this class gets mis-reported"
    (`notes/_receipts/2026-08-19-204-verifier-challenge-table.md:32`).
  LEG 2 · PIXEL — for each suspect, the rendered PNG is sampled at the element's centre and
    the RGB is REPORTED. A suspect painting `rgb(0,0,0)` is the #184 signature, MEASURED.
    A positive control (a var that DOES resolve) is sampled on every run and printed, so a
    green result cannot come from a sampler that reads black everywhere or nothing anywhere.

GLOB — rules only as wide as [[gate-glob-scope-rule]]:
    knowledge/snippets/Chart-*.reference.html · knowledge/snippets/DataViz-interactive.html
(the dataviz surfaces; the static gate's glob is wider and cheaper — this one costs a render).
⚠ MEASURED #206: `knowledge/snippets/DataViz-interactive.html` DOES NOT EXIST on disk today,
though `_gate_dataviz_vars.py`'s own glob names it. Kept in this glob deliberately so the file
is picked up if it returns; recorded here because an unmatched pattern is not an absence
[[unmatched-grep-is-not-an-absence]] and the static gate's stale glob entry is a live finding
for the conductor, not something this lane may edit.

⛔ ENVIRONMENT SPLIT, DECLARED (#173): this probe needs Chromium + Playwright per
`knowledge/_RUNBOOK-render-verify.md`. It runs in the SANDBOX today. It is **UNPROVEN in CI** —
`s204-D1` item 5 owns the CI pixel leg, not this lane. When the browser is absent the probe
REFUSES by name and exits **77 COULD-NOT-ASK** (`knowledge/_could_not_ask.py`, #193) with a
first line carrying its own reason — ⛔ #208: it used to exit 1, which a CI consumer reads as a
MEASURED failure; an honest refusal now has a legal form no consumer can confuse with a red.
A real failure still exits 1. It never reports a pass it did not measure
[[feedback-measuring-tool-must-not-guess]]. Env vars it needs (runbook §sandbox):
    PYTHONPATH=/var/tmp/pylibs  PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-<n>
    LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu  TMPDIR=/var/tmp

⛔ WHAT IT CANNOT SEE: a var that resolves to the WRONG colour (presence, not correctness) ·
an element with zero area (nothing to sample — reported as PIXEL-UNSAMPLED, never as clean) ·
colours set by script AFTER the settle window · themes other than the page's default (the
four-theme sweep is the review pages' job, not this glob's) · anything outside the glob.
⚠ Transitions: the page is settled with `*{transition:none!important;animation:none!important}`
BEFORE reading, per the 2026-07-27 runbook pothole (a value read in the same task as a class
change is the PRE-transition value).

USAGE
  python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check
  python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check --glob '<pattern>'
  python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --selftest
EXIT: 0 clean · 1 findings (a MEASURED failure) · 77 COULD-NOT-ASK (a declared environment
refusal — the browser could not be reached, so the question was never asked).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob as globmod, io, os, re, shutil, sys, tempfile
import _could_not_ask as cna  # noqa: E402 — the #193 convention: 77 + a `COULD-NOT-ASK:` line

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_GLOBS = ["knowledge/snippets/Chart-*.reference.html",
                 "knowledge/snippets/DataViz-interactive.html"]

JS = r"""
() => {
  const ATTRS = ['fill','stroke','stop-color','flood-color','lighting-color','color'];
  const suspects = [], controls = [];
  for (const el of document.querySelectorAll('*')) {
    if (!el.getAttribute) continue;
    for (const a of ATTRS) {
      const raw = el.getAttribute(a);
      if (!raw || raw.indexOf('var(') === -1) continue;
      const cs = getComputedStyle(el);
      const re = /var\(\s*(--[A-Za-z0-9_-]+)\s*(,)?/g;
      let m;
      while ((m = re.exec(raw)) !== null) {
        const name = m[1], hasFallback = !!m[2];
        const resolved = (cs.getPropertyValue(name) || '').trim();
        const r = el.getBoundingClientRect();
        const rec = {tag: el.tagName, attr: a, raw: raw, name: name,
                     fallback: hasFallback, resolved: resolved,
                     painted: cs.getPropertyValue(a === 'stop-color' ? 'stop-color' : a),
                     x: r.left + window.scrollX, y: r.top + window.scrollY,
                     w: r.width, h: r.height,
                     html: el.outerHTML.slice(0, 110)};
        if (resolved === '' && !hasFallback) suspects.push(rec);
        else if (controls.length < 1 && r.width > 2 && r.height > 2) controls.push(rec);
      }
    }
  }
  return {suspects: suspects, controls: controls,
          n: document.querySelectorAll('*').length};
}
"""


def _browser_env():
    """Return (launcher_kwargs, refusal). A missing browser is a DECLARED refusal."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        return None, ("NOT-IN-THIS-ENVIRONMENT: playwright is not importable. Stage it per "
                      "knowledge/_RUNBOOK-render-verify.md (PYTHONPATH=/var/tmp/pylibs). "
                      "REFUSED — not a pass.")
    pats = [os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
                         "chromium_headless_shell-*/chrome-linux/headless_shell"),
            os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/"
                               "chrome-linux/headless_shell"),
            "/var/tmp/pw-browsers-*/chromium_headless_shell-*/chrome-linux/headless_shell"]
    for pat in pats:
        hits = sorted(globmod.glob(pat)) if pat.strip("/") else []
        if hits:
            return {"executable_path": hits[0]}, None
    return None, ("NOT-IN-THIS-ENVIRONMENT: no chromium headless_shell found (looked in "
                  "PLAYWRIGHT_BROWSERS_PATH, ~/.cache/ms-playwright, /var/tmp/pw-browsers-*). "
                  "REFUSED — not a pass.")


def _sample(png_bytes, x, y, w, h):
    """Sample the element's rendered CROP, not one centre pixel.

    ⚠ WHY A CROP: the first build of this probe sampled the bbox centre and the selftest went
    RED — the planted element was an axis `<text>`, whose bbox centre falls BETWEEN glyph
    strokes and reads as page background. A centre pixel measures text, thin strokes and
    hollow shapes WRONG, so it would have called a real #184 silent black clean.
    Returns {'black': <count of exact rgb(0,0,0) pixels>, 'total': n, 'modal': (r,g,b)} or
    None (declared, never guessed)."""
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    x0 = int(max(0, min(im.width - 1, x)))
    y0 = int(max(0, min(im.height - 1, y)))
    x1 = int(max(x0 + 1, min(im.width, x + max(1.0, w))))
    y1 = int(max(y0 + 1, min(im.height, y + max(1.0, h))))
    crop = im.crop((x0, y0, x1, y1))
    px = list(crop.getdata())
    if not px:
        return None
    from collections import Counter
    counts = Counter(px)
    return {"black": counts.get((0, 0, 0), 0), "total": len(px),
            "modal": counts.most_common(1)[0][0]}


def drive(paths, verbose=True, viewport=(1180, 1400)):
    """Render each page and return (findings, controls, refusal)."""
    kwargs, refusal = _browser_env()
    if refusal:
        return None, None, refusal
    from playwright.sync_api import sync_playwright
    findings, controls = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
                              **kwargs)
        pg = b.new_page(viewport={"width": viewport[0], "height": viewport[1]})
        for path in paths:
            rel = os.path.relpath(path, ROOT) if path.startswith(ROOT) else path
            pg.goto("file://" + os.path.abspath(path))
            # SETTLE BEFORE READING (runbook 2026-07-27): kill transitions, then let layout land
            pg.add_style_tag(content="*{transition:none!important;animation:none!important}")
            pg.wait_for_timeout(300)
            res = pg.evaluate(JS)
            shot = pg.screenshot(full_page=True)
            for rec in res["suspects"]:
                pix = (_sample(shot, rec["x"], rec["y"], rec["w"], rec["h"])
                       if rec["w"] > 0 and rec["h"] > 0 else None)
                rec["pix"] = pix
                rec["file"] = rel
                findings.append(rec)
                if verbose:
                    print("  ⛔ DANGLING-VAR %s · <%s %s=%r> · %s resolves to NOTHING in this "
                          "element's cascade · computed=%s · PIXELS=%s"
                          % (rel, rec["tag"].lower(), rec["attr"], rec["raw"], rec["name"],
                             rec["painted"],
                             ("%d/%d pure black, modal rgb%s%s"
                              % (pix["black"], pix["total"], pix["modal"],
                                 "  ← #184 SILENT BLACK, MEASURED" if pix["black"] else ""))
                             if pix else "UNSAMPLED (zero-area or no PIL) — declared, not clean"))
            ctrl = res["controls"][0] if res["controls"] else None
            if ctrl:
                ctrl["pix"] = _sample(shot, ctrl["x"], ctrl["y"], ctrl["w"], ctrl["h"])
                ctrl["file"] = rel
                controls.append(ctrl)
            if verbose:
                print("  %-3s %-56s elements=%4d var-suspects=%d control=%s"
                      % ("⛔" if res["suspects"] else "OK", rel[-56:], res["n"],
                         len(res["suspects"]),
                         ("%s→modal rgb%s" % (ctrl["name"], ctrl["pix"]["modal"]))
                         if ctrl and ctrl.get("pix") else "NONE"))
        b.close()
    return findings, controls, None


def resolve(patterns):
    out = []
    for pat in patterns:
        out += sorted(globmod.glob(os.path.join(ROOT, pat)))
    return out


def check(patterns=None):
    patterns = patterns or DEFAULT_GLOBS
    paths = resolve(patterns)
    if not paths:
        print("⚠ THE GLOB MATCHED NOTHING — an empty population is not a pass.")
        print("PROBE P-3 — findings=1")
        return 1
    findings, controls, refusal = drive(paths)
    if refusal:
        # ⛔ #208: a refusal used to exit 1, which every consumer reads as a MEASURED failure.
        # It now carries the #193 legal form — exit 77 + a `COULD-NOT-ASK:` first line naming
        # the input it could not reach. A real failure below still exits 1
        # [[honest-refusal-needs-a-legal-form]]. The refusal is keyed on the UNREACHABLE INPUT
        # (playwright / headless_shell), NEVER on "am I in CI" — see _could_not_ask.py.
        rc = cna.refuse("P-3 dangling-var PIXEL test", refusal)
        print("PROBE P-3 — findings=UNKNOWN (environment refused, exit %d)" % rc)
        return rc
    black = [f for f in findings if f.get("pix") and f["pix"]["black"] > 0]
    unsampled = [c for c in controls if not c.get("pix")]
    print("P-3 dangling-var pixel test: %d page(s) rendered over %s · %d suspect(s), %d of them "
          "painting PURE BLACK · %d positive control(s), %d unsampled"
          % (len(paths), patterns, len(findings), len(black), len(controls), len(unsampled)))
    if controls and not any(c.get("pix") for c in controls):
        print("  ⛔ THE PIXEL LEG COULD NOT SAMPLE ANY CONTROL — a green here would be a "
              "sampler failure wearing a pass. Treated as a finding.")
        print("PROBE P-3 — findings=%d" % (len(findings) + 1))
        return 1
    print("PROBE P-3 — findings=%d" % len(findings))
    return 1 if findings else 0


def _absolutise(src, dst):
    """Copy an HTML file OUT of the repo with its relative links rewritten to file:// URLs, so
    a plant never has to be written inside the tree (owned-regions fence + the sandbox cannot
    unlink under the repo mount)."""
    base = os.path.dirname(os.path.abspath(src))
    text = open(src, encoding="utf-8", errors="replace").read()

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http", "data:", "#", "file:", "/")):
            return m.group(0)
        return '%s="file://%s"' % (attr, os.path.normpath(os.path.join(base, url)))

    text = re.sub(r'\b(href|src)="([^"]+)"', fix, text)
    open(dst, "w", encoding="utf-8").write(text)
    return text


def selftest():
    """PLANT-THEN-DETECT, both directions, DRIVING THE BROWSER on a REAL chart snippet with a
    REAL dangling var — the #104 rule: the test must drive the thing, not assert its clause."""
    fails = []
    kwargs, refusal = _browser_env()
    if refusal:
        rc = cna.refuse("P-3 selftest", refusal)
        print("   This is a DECLARED environment gap (#173), reported as rc=%d COULD-NOT-ASK — "
              "never a pass, and distinguishable from the rc=1 a real red returns." % rc)
        return rc
    tmp = tempfile.mkdtemp(prefix="p3-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    src = os.path.join(ROOT, "knowledge", "snippets", "Chart-bar.reference.html")
    if not os.path.exists(src):
        src = sorted(globmod.glob(os.path.join(ROOT, "knowledge", "snippets",
                                               "Chart-*.reference.html")))[0]
    clean = os.path.join(tmp, "clean.html")
    text = _absolutise(src, clean)

    # direction 1 — the CLEAN page must be silent (and its control must sample)
    base, base_ctrl, _ = drive([clean], verbose=False)
    print("  · baseline on an out-of-tree copy of %s: %d suspect(s), control=%s"
          % (os.path.basename(src), len(base),
             ("%s→modal rgb%s, %d black px"
              % (base_ctrl[0]["name"], base_ctrl[0]["pix"]["modal"], base_ctrl[0]["pix"]["black"]))
             if base_ctrl and base_ctrl[0].get("pix") else "NONE"))
    if base:
        fails.append("BASELINE NOT CLEAN: %d suspect(s) on an unplanted real snippet — the "
                     "plant arm below cannot be attributed" % len(base))
    if not base_ctrl or not base_ctrl[0].get("pix"):
        fails.append("PIXEL LEG DEAD: no positive control sampled on the clean page — a green "
                     "run would prove nothing about the sampler")

    # direction 2 — PLANT the exact #184 shape: rename one real fill var to a nonexistent one
    m = re.search(r'fill="var\(\s*(--[A-Za-z0-9_-]+)\s*\)"', text)
    if not m:
        print("⛔ selftest cannot run: no `fill=\"var(--x)\"` in %s (declared)."
              % os.path.basename(src))
        return 1
    planted_path = os.path.join(tmp, "planted.html")
    open(planted_path, "w", encoding="utf-8").write(
        text.replace(m.group(0), 'fill="var(--w45-selftest-nonexistent)"'))
    found, ctrl, _ = drive([planted_path], verbose=False)
    if not found:
        fails.append("PLANT NOT CAUGHT: `fill=\"var(--w45-selftest-nonexistent)\"` planted in "
                     "place of %s produced no suspect" % m.group(1))
    else:
        black_px = sum(f["pix"]["black"] for f in found if f.get("pix"))
        with_black = [f for f in found if f.get("pix") and f["pix"]["black"] > 0]
        print("  ✅ plant caught: %d suspect(s), first=%s computed=%s"
              % (len(found), found[0]["name"], found[0]["painted"]))
        if not with_black:
            fails.append("PIXEL LEG DID NOT CONFIRM THE CLASS: not one planted element's "
                         "rendered crop carries a pure-black pixel. #184's whole signature is "
                         "the black paint — DECLARED, not dismissed.")
        else:
            print("  ✅ pixel leg confirms the #184 signature: %d pure-black pixel(s) across "
                  "%d/%d planted element(s), measured from the PNG, not inferred"
                  % (black_px, len(with_black), len(found)))
            print("  ⚠ HONEST RESIDUAL: %d planted element(s) sampled NO exact-black pixel — "
                  "small antialiased glyphs can carry no pixel at exactly rgb(0,0,0). The "
                  "cascade leg still names them; the pixel leg is corroboration, not the gate."
                  % (len(found) - len(with_black)))
        # CONTROL for the pixel leg itself: the SAME element, unplanted, must NOT be black
        clean_same, _c2, _ = drive([clean], verbose=False)
        base_black = sum(1 for f in clean_same if f.get("pix") and f["pix"]["black"])
        if base_black:
            fails.append("PIXEL CONTROL FIRED: the unplanted page also reports black suspects "
                         "(%d) — the black reading cannot be attributed to the plant"
                         % base_black)
        else:
            print("  ✅ pixel control: the same page unplanted reports no black suspect, so the "
                  "black reading is attributable to the plant")

    # direction 3 — REMOVE the plant, the probe must go silent again
    after, _c, _ = drive([clean], verbose=False)
    if after != base:
        fails.append("REMOVAL NOT GREEN: the unplanted page gave %d suspect(s), baseline %d"
                     % (len(after), len(base)))
    else:
        print("  ✅ removal green: the unplanted page returns to baseline (%d suspect(s))"
              % len(base))

    # CONTROL — a var WITH a fallback arm must NOT be reported (#204's own false positive)
    fb = os.path.join(tmp, "fallback.html")
    open(fb, "w", encoding="utf-8").write(
        text.replace(m.group(0), 'fill="var(--w45-selftest-nonexistent, #DA1A00)"'))
    fb_found, _c, _ = drive([fb], verbose=False)
    if fb_found:
        fails.append("FALLBACK CONTROL FIRED: `var(--x, #DA1A00)` was reported as dangling — "
                     "that is the #204 verifier's own false positive, rebuilt")
    else:
        print("  ✅ fallback control held: `var(--nonexistent, #DA1A00)` is NOT a finding")

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-3 selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ P-3 selftest PASS — a REAL dangling var planted in a REAL chart was detected in "
          "the browser AND measured as a pure-black pixel; removal green; fallback control held.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    pats = [argv[i + 1] for i, a in enumerate(argv) if a == "--glob"]
    sys.exit(check(pats or None))
