#!/usr/bin/env python3
"""_probe_fail_open.py — the MUTATION PROBE behind #261 D3 (s260-D3 driver scope).

WHO CONSUMES THIS. Nobody automatically — it is a HAND-RUN mutation test, and that is the point:
`_validate_dataviz.py` is the thing under test, so a probe wired into the gate would grade itself.
It exists so any reviewer can re-prove, in one command, the clause #261 D3 closed:

    a dataviz rule that reads SOURCE TEXT cannot see an artefact the engine draws at RUNTIME.

WHAT IT DOES. For each named venue it takes a TEMP COPY of a shipped `Chart-*.reference.html`
snippet (which inlines the whole engine), mutates the INLINED ENGINE so the RENDERED DOM violates
the rule, proves the violation in a real Chromium, then runs the shipped dataviz gate over the
mutated copy and reports whether the gate saw it.

    python3 knowledge/_tests/chart-engine/_probe_fail_open.py            all venues
    python3 knowledge/_tests/chart-engine/_probe_fail_open.py dv-017     one venue
    python3 knowledge/_tests/chart-engine/_probe_fail_open.py --expect red    non-zero unless ALL bite

BEFORE #261 D3 every venue printed FAILS OPEN (GREEN). After it, every venue must print RED — that
is what `--expect red` asserts, and it is the only proof the route actually reads the pixels.
The mutated copy is RE-DRIVEN into its own temp receipt first, so what bites is the RULE and not
merely the freshness arm. (Grading the mutated copy against the pristine receipt is also RED, via
`self_sha256` — that is a second, weaker proof, and it is not the one this probe makes.)

ENVIRONMENT. Same as `_drive_chart_engine.py`: Playwright + Chromium, and
`APOLLO_PW_LD_LIBRARY_PATH` if the sandbox is missing libXdamage and friends.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SNIPPETS = os.path.join(ROOT, "knowledge", "snippets")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DOM_JS = r"""
(need) => {
  const figs = Array.from(document.querySelectorAll('figure.dv'));
  let grads = 0, rogue = [], curves = 0, marks = 0, roleless = 0, labelless = 0;
  let join = null;
  for (const fig of figs) {
    const svg = fig.querySelector('svg.dv-svg'); if (!svg) { continue; }
    grads += svg.querySelectorAll('linearGradient,radialGradient,filter').length;
    const series = Array.from(svg.querySelectorAll('.dv-series'));
    marks += series.length;
    for (const m of series) {
      for (const v of [m.getAttribute('fill'), m.getAttribute('stroke')]) {
        if (v && /^#[0-9a-f]{3,8}$/i.test(v.trim())) { rogue.push(v.trim()); }
      }
      if (m.tagName.toLowerCase() === 'path' && /[CSQTcsqt]/.test(m.getAttribute('d') || '')) { curves++; }
      if (!m.getAttribute('role')) { roleless++; }
      if (!m.getAttribute('aria-label')) { labelless++; }
    }
    if (fig.getAttribute('data-dv-type') === 'butterfly-v' && series.length) {
      const ctm = svg.getScreenCTM();
      const k = ctm ? (Math.sqrt(Math.abs(ctm.a * ctm.d - ctm.b * ctm.c)) || 1) : 1;
      const cols = {};
      for (const m of series) { const b = m.getBBox(); const key = Math.round(b.x * 100) / 100;
        (cols[key] = cols[key] || []).push(b); }
      let best = Infinity;
      for (const key in cols) { const c = cols[key].sort((a, b) => a.y - b.y);
        for (let i = 0; i < c.length - 1; i++) { const g = c[i + 1].y - (c[i].y + c[i].height);
          if (g < best) { best = g; } } }
      if (isFinite(best)) { join = Math.round(best * k * 1000) / 1000; }
    }
  }
  const html = document.documentElement.outerHTML;
  return { figures: figs.length, marks: marks, gradients: grads,
           rogue_hex: Array.from(new Set(rogue)), curve_series: curves,
           marks_without_role: roleless, marks_without_aria_label: labelless,
           butterfly_v_join_px: join,
           aria_missing_from_dom: (need || []).filter((n) => html.indexOf(n) < 0) };
}
"""


def render(path, need=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True, channel="chromium",
                                args=["--no-sandbox", "--disable-gpu", "--force-device-scale-factor=1"])
        pg = br.new_context(viewport={"width": 1180, "height": 900},
                            reduced_motion="reduce").new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + path, wait_until="load")
        pg.wait_for_timeout(400)
        out = pg.evaluate(DOM_JS, need or [])
        br.close()
    out["pageerrors"] = len(errs)
    return out


def required_aria(path):
    html = open(path, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="token-manifest">(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1)).get("requiredAria", [])
    except Exception:
        return []


# ---- the mutations. Each one edits the INLINED ENGINE, never the markup the gate reads. --------
def m_rogue(h):
    return h.replace("return 'var(--data-series-' + ((i % PAL) + 1) + ')';", "return '#ff2200';", 1)


def m_lowcon(h):
    return h.replace("return 'var(--data-series-' + ((i % PAL) + 1) + ')';", "return '#f2f2f2';", 1)


def _wrap(h, body):
    """Wrap dvRender with a post-render mutation, before the type registry is published."""
    return h.replace("  dvRender.types = TYPES;",
                     "  var _p261 = dvRender;\n"
                     "  dvRender = function (f, s) { var r = _p261(f, s);\n" + body +
                     "\n    return r; };\n"
                     "  dvRender.types = TYPES;", 1)


def m_grad(h):
    return _wrap(h, "    var sv = f.querySelector('svg.dv-svg');\n"
                    "    if (sv) { sv.insertAdjacentHTML('afterbegin', '<defs><linear' + 'Gradient "
                    "id=\"probe261\"><stop offset=\"0\"/></linear' + 'Gradient></defs>'); }")


def m_curve(h):
    return _wrap(h, "    var sv = f.querySelector('svg.dv-svg');\n"
                    "    if (sv) { sv.insertAdjacentHTML('beforeend', '<path class=\"dv-series\" "
                    "fill=\"none\" stroke=\"var(--data-series-1)\" d=\"M10 10 C 20 20, 40 20, 50 10\"/>'); }")


def m_aria(h):
    return _wrap(h, "    f.querySelectorAll('[role],[aria-label],[aria-labelledby]').forEach(function (e) {\n"
                    "      e.removeAttribute('role'); e.removeAttribute('aria-label');\n"
                    "      e.removeAttribute('aria-labelledby'); });")


def m_join(h):
    return h.replace("var GAP = 2.2;", "var GAP = 0.0;", 1)


VENUES = {
    # key            snippet                            mutation   rule the gate must name
    "dv-017":      ("Chart-line.reference.html",        m_rogue,   "dv-017"),
    "dv-016":      ("Chart-line.reference.html",        m_lowcon,  "dv-016"),
    "dv-009":      ("Chart-line.reference.html",        m_grad,    "dv-009"),
    "line-011":    ("Chart-line.reference.html",        m_curve,   "dv-line-011"),
    "bfly-v-join": ("Chart-butterfly-v.reference.html", m_join,    "dv-004"),
    "aria":        ("Chart-scatter.reference.html",     m_aria,    "requiredAria"),
}


def redrive(dst, tmp, drv):
    """Drive the MUTATED copy and write a receipt for it, so the gate grades the RULE and not just
    the staleness. (Grading it against the pristine receipt is also RED — by `self_sha256` — but
    that proves the freshness arm, not the rule; both matter and only this one is the rule.)"""
    version, pages = drv.drive([dst], verbose=False)
    rec = {"chromium": version, "driven": "probe", "themes": list(drv.THEMES),
           "modes": list(drv.MODES), "pages": pages}
    path = os.path.join(tmp, "_receipts.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    return path


def run(key, vdv, drv):
    snippet, mutate, rule = VENUES[key]
    src = os.path.join(SNIPPETS, snippet)
    tmp = tempfile.mkdtemp(prefix="probe261-")
    dst = os.path.join(tmp, snippet)
    shutil.copy(src, dst)
    html = open(dst, encoding="utf-8").read()
    new = mutate(html)
    if new == html:
        print("VENUE %-12s ❌ mutation did not apply to %s" % (key, snippet))
        return False
    open(dst, "w", encoding="utf-8").write(new)

    dom = render(dst, required_aria(dst))
    vdv.RECEIPTS_PATH = redrive(dst, tmp, drv)
    vdv._RECEIPTS_CACHE.clear()
    results, _fadv = vdv.check_file(dst)
    B = [b for _t, _i, bs, _a in results for b in bs]
    hits = [b for b in B if rule in b or "STALE" in b]
    print("VENUE %-12s %-34s DOM: marks=%s grads=%s rogue=%s curves=%s join=%s "
          "no-role=%s no-label=%s aria-missing=%s errs=%s"
          % (key, snippet, dom["marks"], dom["gradients"], dom["rogue_hex"], dom["curve_series"],
             dom["butterfly_v_join_px"], dom["marks_without_role"], dom["marks_without_aria_label"],
             dom["aria_missing_from_dom"], dom["pageerrors"]))
    print("      gate blocking=%d  matched=%d  -> %s"
          % (len(B), len(hits), "RED (bites)" if hits else "FAILS OPEN (GREEN)"))
    for b in hits[:2]:
        print("      ✗", b[:170])
    return bool(hits)


def main():
    ap = argparse.ArgumentParser(prog="python3 knowledge/_tests/chart-engine/_probe_fail_open.py",
                                 description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("venue", nargs="*", default=None, help="venue key(s); default all: " + ", ".join(VENUES))
    ap.add_argument("--expect", choices=("green", "red"), default=None,
                    help="red: exit non-zero unless EVERY venue bites (post-#261-D3 state)")
    args = ap.parse_args()

    extra = os.environ.get("APOLLO_PW_LD_LIBRARY_PATH")
    if extra and extra not in os.environ.get("LD_LIBRARY_PATH", ""):
        os.environ["LD_LIBRARY_PATH"] = extra + ":" + os.environ.get("LD_LIBRARY_PATH", "")

    vdv = _load("vdv", os.path.join(ROOT, "knowledge", "_validate_dataviz.py"))
    drv = _load("drv", os.path.join(ROOT, "knowledge", "_drive_chart_engine.py"))
    keys = args.venue or list(VENUES)
    bad = [k for k in keys if k not in VENUES]
    if bad:
        print("❌ unknown venue(s) %s — known: %s" % (bad, ", ".join(VENUES)))
        return 2
    bites = [run(k, vdv, drv) for k in keys]
    print("\n%d/%d venue(s) BITE." % (sum(bites), len(bites)))
    if args.expect == "red" and not all(bites):
        print("❌ expected every venue RED — %d still fail open." % (len(bites) - sum(bites)))
        return 1
    if args.expect == "green" and any(bites):
        print("❌ expected every venue GREEN — %d bite." % sum(bites))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
