#!/usr/bin/env python3
"""
verify_dv_gutter_render.py — the ds-012(b) RENDER PROOF: no category label is clipped.

WHY IT IS A RENDER PROOF AND NOT A GATE (ds-012 enactment point 5, Dave 2026-07-27)
------------------------------------------------------------------------------------
The assertion is "no `text.dv-label` has `getBBox().x < 0`". That is a property of a
RENDERED document in a REAL face — the static dataviz gate cannot see it, and putting it
there would report a cheerful pass forever (the instrument-fit error the 07-27 pass
measured). So it lives here, with the other `verify_dv_*` render proofs.

TWO SIDES, because a one-sided proof of an absence is not a proof
-----------------------------------------------------------------
  STEP 0 · FACE CONTROL. `document.fonts.check()` LIES — it returns true in broken
           fontconfig setups. So we measure: canvas measureText of the SAME string in
           the licensed cut, in DejaVu Sans, and in a face that CANNOT exist. If the
           licensed number equals the bogus number the page is in FALLBACK and the run
           EXITS 2 — geometry measured in the wrong face is not evidence.
  STEP 1 · THE RULING. Every `text.dv-label` in every gutter-fitted svg must have
           getBBox().x >= 0 AND a client rect left >= the svg's left edge.
  STEP 2 · SENSITIVITY (`--bite`). Re-points `data-pl-fit` at a selector that matches
           NOTHING and re-fires the fit — i.e. the pre-ds-012 gutter, live in the same
           page (canon is never mutated; the LIVE DOM is, which is why no copy is written
           into the tree it measures). That run MUST FAIL step 1. A green here with a
           green --bite means the probe is blind.

USAGE
    python3 knowledge/_render/verify_dv_gutter_render.py                       # snippet + showroom
    python3 knowledge/_render/verify_dv_gutter_render.py --file <path>
    python3 knowledge/_render/verify_dv_gutter_render.py --bite                # sensitivity
EXIT 0 = green · 1 = a check failed · 2 = the probe could not measure (never a pass)
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_TARGETS = [
    ("snippet", os.path.join(ROOT, "knowledge/snippets/Chart-bar.reference.html")),
    ("showroom", os.path.join(ROOT, "showroom/chart-bar.html")),
]
WIDTHS = (1180, 480)
PROBE_STRING = "Groceries Housing"

FONT_JS = """(s) => {
  const c = document.createElement('canvas').getContext('2d');
  const m = (f) => { c.font = '12px ' + f; return +c.measureText(s).width.toFixed(3); };
  return { hsbc: m('"HSBC_MtUnivers_Latin"'), dejavu: m('"DejaVu Sans"'),
           bogus: m('"__NoSuchFaceAtAll__"'), check: document.fonts.check('16px HSBC_MtUnivers_Latin') };
}"""

# Measured inside whichever document actually carries the chart (page or showroom iframe).
MEAS_JS = """() => {
  const out = [];
  document.querySelectorAll('svg[data-pl-fit], svg.dv-fit').forEach((svg, si) => {
    const sr = svg.getBoundingClientRect();
    const labs = [...svg.querySelectorAll('text.dv-label')]
      .filter(t => t.getAttribute('text-anchor') === 'end');   /* the LEFT gutter labels */
    if (!labs.length) { return; }
    out.push({ svg: si, fitted: svg.hasAttribute('data-pl-fit'),
      w: +sr.width.toFixed(1), pl: svg.getAttribute('data-pl'),
      labels: labs.map(t => { const bb = t.getBBox(), r = t.getBoundingClientRect();
        return { t: t.textContent.trim(), bbx: +bb.x.toFixed(2), bbw: +bb.width.toFixed(2),
                 ovr: +(r.left - sr.left).toFixed(2) }; }) });
  });
  return out; }"""

BITE_JS = """() => {
  /* the pre-ds-012 world: the gutter marker survives (so the chart stays IN SCOPE) but
     resolves to nothing, so gutterPL() returns the baked data-pl floor. */
  const svgs = [...document.querySelectorAll('svg[data-pl-fit]')];
  svgs.forEach(s => s.setAttribute('data-pl-fit', 'text.__matches_nothing__'));
  window.dispatchEvent(new Event('resize'));
  return new Promise(r => setTimeout(() => r(svgs.length), 600)); }"""

SHOWROOM_JS = """(w) => {
  const s = document.getElementById('w');
  if (s) { s.value = w; s.dispatchEvent(new Event('input', { bubbles: true })); }
  return new Promise(r => setTimeout(() => r(true), 1200)); }"""


def run(targets, expect_fail):
    sys.path.insert(0, "/var/tmp/pylibs")
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:                                  # a crash is not a fail
        print("PROBE UNAVAILABLE (playwright): %s" % e); return 2
    shells = glob.glob("/var/tmp/pw-browsers-*/chromium_headless_shell-*/chrome-linux/headless_shell")
    if not shells:
        print("PROBE UNAVAILABLE: no chromium shell found"); return 2

    fails, checks, ev = [], 0, []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shells[0], headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        for kind, path in targets:
            if not os.path.exists(path):
                print("PROBE UNAVAILABLE: missing %s" % path); b.close(); return 2
            for W in WIDTHS:
                pg = b.new_page(viewport={"width": max(W, 1280) if kind == "showroom" else W, "height": 900})
                pg.goto("file://" + path); pg.wait_for_timeout(1400)
                frame = pg
                if kind == "showroom":
                    pg.evaluate(SHOWROOM_JS, W)
                    fr = [f for f in pg.frames if f is not pg.main_frame]
                    if not fr:
                        print("PROBE UNAVAILABLE: no showroom pane frame"); b.close(); return 2
                    frame = fr[0]
                if expect_fail and not frame.evaluate(BITE_JS):
                    print("PROBE UNAVAILABLE: nothing to neuter in %s" % path); b.close(); return 2
                f = frame.evaluate(FONT_JS, PROBE_STRING)
                if abs(f["hsbc"] - f["bogus"]) < 0.01:
                    print("FALLBACK FACE — refusing to measure geometry. %s" % json.dumps(f))
                    b.close(); return 2
                ev.append({"target": kind, "w": W, "font": f})
                for svg in frame.evaluate(MEAS_JS):
                    if not svg["fitted"]:
                        continue                              # only gutter-fitted charts are in scope
                    for l in svg["labels"]:
                        checks += 2
                        if l["bbx"] < 0:
                            fails.append("%s@%d svg%d %s getBBox().x=%.2f" % (kind, W, svg["svg"], l["t"], l["bbx"]))
                        if l["ovr"] < -0.5:
                            fails.append("%s@%d svg%d %s clientLeft-svgLeft=%.2f" % (kind, W, svg["svg"], l["t"], l["ovr"]))
                    ev.append({"target": kind, "w": W, "svgW": svg["w"], "labels": svg["labels"]})
                pg.close()
        b.close()

    if not checks:
        print("PROBE MEASURED NOTHING — no gutter-fitted chart found. Not a pass."); return 2
    print(json.dumps(ev, indent=1))
    print("%d check(s) · %d failure(s)" % (checks, len(fails)))
    for x in fails:
        print("  FAIL " + x)
    if expect_fail:
        if fails:
            print("BITE OK — the neutered copy fails, so the probe is sensitive."); return 0
        print("BITE FAILED — the neutered copy PASSED. The probe is blind."); return 1
    return 1 if fails else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--bite", action="store_true")
    a = ap.parse_args()
    tg = [("snippet" if "snippets" in a.file else "showroom", a.file)] if a.file else DEFAULT_TARGETS
    sys.exit(run(tg, a.bite))
