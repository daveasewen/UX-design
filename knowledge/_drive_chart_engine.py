#!/usr/bin/env python3
"""_drive_chart_engine.py — the COMMITTED driver behind the DRIVEN RECEIPT (s260-D3).

WHO CONSUMES THIS (an instrument without a consumer is a zombie — [[instrument-without-a-consumer]]).
--------------------------------------------------------------------------------------------------
`knowledge/_validate_dataviz.py` consumes the file this script writes,
`knowledge/_tests/chart-engine/_receipts.json`, as the EVIDENCE for dv-004 on charts that no
longer exist in the markup. Dave's ruling `s260-D3` (2026-09-08):

    "DRIVEN RECEIPTS BECOME THE GATE FOR ENGINE-DRAWN CHARTS. Where a dataviz rule reads static
     geometry (dv-004 and its siblings) and the chart is drawn at runtime by
     knowledge/canon/dv-render.js, _validate_dataviz accepts a COMMITTED driven receipt (a
     Playwright measurement recorded from knowledge/_tests/chart-engine/) as the evidence for that
     rule — the gate is 'static OR driven', never skipped. Option (b), an engine-emitted
     self-report marker trusted by the static gate, is REFUSED."

So the chain is: this script DRIVES a real Chromium over the six committed test pages, MEASURES
the drawn geometry, and COMMITS the numbers; the gate READS them and refuses to grade anything it
cannot tie back to the current bytes of the engine. The receipt is not a claim the engine makes
about itself (that is the refused option (b)) — it is a measurement a browser made of the pixels.

WHAT IS MEASURED, per page × 4 themes (mono, legacy, console, supercharge) × 2 modes (light, dark):
  · pageerrors and console errors on load and after a re-render;
  · every `figure.dv`: its dtype, its MARK COUNT, its table-spine ROW COUNT;
  · dv-004 — the minimum separation, in CSS px, between any two drawn segments of a radial or
    stacked chart, computed from the DRAWN PATH (getPointAtLength sampling / getBBox), never from
    the `data-a1`/`data-a2` attributes the engine wrote. For a ring the figure is read at the
    INNER edge (the narrow one, r = ri); for a pie, which has no inner edge, at the same reference
    radius the type partial itself uses, 0.35·ro. Stacked rect columns are measured as the gap
    between adjacent rect bounding boxes.
  · the FILTER: one category unticked, then whether the mark count AND the table row count both
    moved (rule 14 — the a11y answer is never stale).

FRESHNESS. Each page records `sources`: the sha256 of the test page and of every local file it
loads (each `<script src>` and `<link href>` resolved on disk). Change `dv-render-donut.js` and the
receipt is STALE — the gate then fails BLOCKING and names the file, rather than grading new code
with an old measurement.

USAGE
  python3 knowledge/_drive_chart_engine.py            drive everything, rewrite the receipts
  python3 knowledge/_drive_chart_engine.py --check    re-hash sources only; print FRESH/STALE
  python3 knowledge/_drive_chart_engine.py --page donut.html      drive one page (merges)

ENVIRONMENT. Needs Playwright + Chromium. On a sandbox missing libXdamage and friends, fetch the
runtime .debs (`apt-get download libxdamage1 …`), `dpkg-deb -x` them into a prefix and export
`LD_LIBRARY_PATH`; the script honours `APOLLO_PW_LD_LIBRARY_PATH` and adds it for you.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGES_DIR = os.path.join(HERE, "_tests", "chart-engine")
RECEIPTS = os.path.join(PAGES_DIR, "_receipts.json")

THEMES = ("mono", "legacy", "console", "supercharge")
MODES = ("light", "dark")

# ---------------------------------------------------------------------------------------------
# sources + hashing
# ---------------------------------------------------------------------------------------------
_SRC_RE = re.compile(r'<script\b[^>]*\bsrc="([^"]+)"', re.I)
_HREF_RE = re.compile(r'<link\b[^>]*\bhref="([^"]+)"', re.I)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sources_for(page_path):
    """{repo-relative path: sha256} for the page and every LOCAL file it loads."""
    html = open(page_path, encoding="utf-8").read()
    base = os.path.dirname(page_path)
    out = {os.path.relpath(page_path, ROOT): sha256_of(page_path)}
    for ref in _SRC_RE.findall(html) + _HREF_RE.findall(html):
        if ref.startswith(("http:", "https:", "//", "data:", "#")):
            continue
        p = os.path.normpath(os.path.join(base, ref.split("?")[0].split("#")[0]))
        if os.path.isfile(p):
            out[os.path.relpath(p, ROOT)] = sha256_of(p)
    return dict(sorted(out.items()))


def freshness(receipts):
    """[(page, 'FRESH'|'STALE', [stale files])] against the CURRENT bytes on disk."""
    rows = []
    for page in sorted(receipts.get("pages", {})):
        rec = receipts["pages"][page]
        stale = []
        for rel, want in sorted(rec.get("sources", {}).items()):
            p = os.path.join(ROOT, rel)
            got = sha256_of(p) if os.path.isfile(p) else None
            if got != want:
                stale.append(rel + (" (missing)" if got is None else ""))
        rows.append((page, "STALE" if stale else "FRESH", stale))
    return rows


# ---------------------------------------------------------------------------------------------
# the in-page measurement — deliberately reads DRAWN geometry, never the engine's own data-* claims
# ---------------------------------------------------------------------------------------------
MEASURE_JS = r"""
() => {
  const R3 = (v) => (v === null || v === undefined || !isFinite(v)) ? null : Math.round(v * 1000) / 1000;

  /* sample a path element in USER units; each entry is [x, y, arc-length] */
  function sample(el, n) {
    const L = el.getTotalLength();
    const out = [];
    for (let i = 0; i <= n; i++) {
      const s = L * i / n;
      const p = el.getPointAtLength(s);
      out.push([p.x, p.y, s]);
    }
    return out;
  }

  function scaleOf(svg) {
    const m = svg.getScreenCTM();
    return m ? Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)) || 1 : 1;
  }

  /* dv-004 for a radial chart, measured on the DRAWN path.
     Centre + outer radius come from the union bbox of the drawn marks; the reference radius is
     the ring's inner edge (the narrow one), or 0.35*ro for a pie, which has no inner edge. */
  function radialGap(svg, marks) {
    if (marks.length < 2) { return { px: null, note: 'fewer than 2 drawn segments' }; }
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    const clouds = [];
    for (const m of marks) {
      const pts = sample(m, 1600);
      clouds.push(pts);
      for (const p of pts) {
        if (p[0] < x0) x0 = p[0];
        if (p[0] > x1) x1 = p[0];
        if (p[1] < y0) y0 = p[1];
        if (p[1] > y1) y1 = p[1];
      }
    }
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    const ro = Math.max(x1 - x0, y1 - y0) / 2;
    let rmin = Infinity;
    for (const pts of clouds) {
      for (const p of pts) {
        const r = Math.hypot(p[0] - cx, p[1] - cy);
        if (r < rmin) rmin = r;
      }
    }
    const isRing = rmin > 0.05 * ro;
    const rr = isRing ? rmin : 0.35 * ro;           /* the engine's own reference radius for a pie */
    const W = 1.0;                                   /* the reference-radius band, in user units */
    const inBand = (p) => Math.abs(Math.hypot(p[0] - cx, p[1] - cy) - rr) < W;
    const band = clouds.map((pts) => pts.filter(inBand));

    /* Coarse sampling alone OVERSTATES the gap by up to the sample spacing, so every candidate
       pair is refined by coordinate descent on the two arc-length parameters (band-constrained).
       That is what makes the recorded px stable to 3dp across runs and machines. */
    function refine(elA, elB, sA, sB, win) {
      const LA = elA.getTotalLength(), LB = elB.getTotalLength();
      const at = (el, s, L) => { const p = el.getPointAtLength(Math.max(0, Math.min(L, s))); return [p.x, p.y]; };
      let a = at(elA, sA, LA), b = at(elB, sB, LB);
      let best = Math.hypot(a[0] - b[0], a[1] - b[1]);
      for (let k = 0; k < 40; k++) {
        for (const side of [0, 1]) {
          const el = side ? elB : elA, L = side ? LB : LA, s0 = side ? sB : sA;
          for (let t = -8; t <= 8; t++) {
            const s = s0 + win * t / 8;
            if (s < 0 || s > L) { continue; }
            const p = at(el, s, L);
            if (!inBand(p)) { continue; }
            const o = side ? a : b;
            const d = Math.hypot(p[0] - o[0], p[1] - o[1]);
            if (d < best) { best = d; if (side) { sB = s; b = p; } else { sA = s; a = p; } }
          }
        }
        win /= 2;
        if (win < 1e-6) { break; }
      }
      return best;
    }

    let best = Infinity;
    for (let i = 0; i < band.length; i++) {
      for (let j = i + 1; j < band.length; j++) {
        if (!band[i].length || !band[j].length) { continue; }
        let cd = Infinity, ci = 0, cj = 0;
        for (const p of band[i]) {
          for (const q of band[j]) {
            const d = (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1]);
            if (d < cd) { cd = d; ci = p[2]; cj = q[2]; }
          }
        }
        const step = marks[i].getTotalLength() / 1600 + marks[j].getTotalLength() / 1600;
        const d = refine(marks[i], marks[j], ci, cj, step * 2);
        if (d < best) { best = d; }
      }
    }
    if (!isFinite(best)) { return { px: null, note: 'no sampled points at the reference radius' }; }
    return {
      px: R3(best * scaleOf(svg)),
      note: (isRing ? 'inner edge r=' : 'pie reference radius r=') + R3(rr) +
            ', ro=' + R3(ro) + ', ' + marks.length + ' segments, min over all pairs'
    };
  }

  /* dv-004 for a rect stack: the gap between adjacent rects within a column */
  function stackGap(svg, marks) {
    const cols = {};
    for (const m of marks) {
      const b = m.getBBox();
      const k = Math.round(b.x * 100) / 100;
      (cols[k] = cols[k] || []).push(b);
    }
    let best = Infinity, n = 0;
    for (const k in cols) {
      const col = cols[k].sort((a, b) => a.y - b.y);
      for (let i = 0; i < col.length - 1; i++) {
        n++;
        const g = col[i + 1].y - (col[i].y + col[i].height);
        if (g < best) { best = g; }
      }
    }
    if (!n) { return { px: null, note: 'no adjacent pair in any column' }; }
    return { px: R3(best * scaleOf(svg)), note: n + ' adjacent pairs across ' + Object.keys(cols).length + ' columns' };
  }

  const RADIAL = { donut: 1, pie: 1 };
  const STACK = { stacked: 1, 'stacked-column': 1, 'stacked-bar': 1 };

  function readFigure(fig) {
    const dtype = fig.getAttribute('data-dv-type') || '?';
    const svg = fig.querySelector('svg.dv-svg');
    const marks = svg ? Array.prototype.slice.call(svg.querySelectorAll('.dv-series')) : [];
    const rows = fig.querySelectorAll('table.dv-table tbody tr').length;
    const out = { dtype: dtype, marks: marks.length, table_rows: rows, dv004_px: null, dv004_note: 'not a gapless surface' };
    if (svg && marks.length) {
      if (RADIAL[dtype]) {
        const g = radialGap(svg, marks.filter((m) => typeof m.getTotalLength === 'function'));
        out.dv004_px = g.px; out.dv004_note = g.note;
      } else if (STACK[dtype]) {
        const g = stackGap(svg, marks);
        out.dv004_px = g.px; out.dv004_note = g.note;
      }
    }
    return out;
  }

  const figs = {};
  let marks = 0, rows = 0;
  document.querySelectorAll('figure.dv').forEach((f, i) => {
    const key = f.id || ('fig-' + i);
    const r = readFigure(f);
    figs[key] = r;
    marks += r.marks; rows += r.table_rows;
  });
  return { figures: figs, total_marks: marks, total_rows: rows };
}
"""

FILTER_JS = r"""
() => {
  const boxes = Array.prototype.slice.call(
    document.querySelectorAll('#filter input[type=checkbox]')).filter((b) => b.checked);
  if (!boxes.length) { return { ok: false, note: 'no checked #filter checkbox on this page' }; }
  boxes[0].checked = false;
  boxes[0].dispatchEvent(new Event('change', { bubbles: true }));
  return { ok: true, note: 'unticked ' + (boxes[0].value || boxes[0].id || 'first category') };
}
"""

THEME_INIT = r"""
(function () {
  var T = '__THEME__', M = '__MODE__';
  function paint() {
    if (document.documentElement) { document.documentElement.setAttribute('data-apollo-theme', T); }
    if (document.body) { document.body.setAttribute('data-theme', M); return true; }
    return false;
  }
  if (!paint()) {
    var mo = new MutationObserver(function () { if (paint()) { mo.disconnect(); } });
    mo.observe(document.documentElement || document, { childList: true, subtree: true });
  }
}());
"""


def drive(pages, verbose=True):
    from playwright.sync_api import sync_playwright

    out_pages = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, channel="chromium",
                                     args=["--no-sandbox", "--disable-gpu",
                                           "--force-device-scale-factor=1"])
        version = browser.version
        for page_path in pages:
            name = os.path.basename(page_path)
            combos = {}
            for theme in THEMES:
                for mode in MODES:
                    key = "%s/%s" % (theme, mode)
                    ctx = browser.new_context(viewport={"width": 1180, "height": 900},
                                              device_scale_factor=1,
                                              reduced_motion="reduce",
                                              color_scheme=mode)
                    ctx.add_init_script(THEME_INIT.replace("__THEME__", theme).replace("__MODE__", mode))
                    page = ctx.new_page()
                    errs, cerrs = [], []
                    page.on("pageerror", lambda e: errs.append(str(e)))
                    page.on("console", lambda m: cerrs.append(m.text) if m.type == "error" else None)
                    page.goto("file://" + page_path, wait_until="load")
                    # re-assert the theme and redraw, so a theme-dependent throw is caught too
                    page.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);"
                                  "document.body.setAttribute('data-theme',m);"
                                  "if(typeof window.draw==='function'){window.draw();}}", [theme, mode])
                    page.wait_for_timeout(220)
                    before = page.evaluate(MEASURE_JS)
                    filt = page.evaluate(FILTER_JS)
                    page.wait_for_timeout(220)
                    after = page.evaluate(MEASURE_JS)
                    combos[key] = {
                        "pageerrors": len(errs),
                        "pageerror_texts": sorted(set(errs))[:5],
                        "console_errors": len(cerrs),
                        "console_error_texts": sorted(set(cerrs))[:5],
                        "figures": before["figures"],
                        "marks": before["total_marks"],
                        "table_rows": before["total_rows"],
                        "filter": {
                            "driven": bool(filt.get("ok")),
                            "note": filt.get("note", ""),
                            "marks_before": before["total_marks"],
                            "marks_after": after["total_marks"],
                            "rows_before": before["total_rows"],
                            "rows_after": after["total_rows"],
                            "moved_marks": before["total_marks"] != after["total_marks"],
                            "moved_rows": before["total_rows"] != after["total_rows"],
                        },
                    }
                    ctx.close()
                    if verbose:
                        f = combos[key]
                        px = [v["dv004_px"] for v in f["figures"].values() if v["dv004_px"] is not None]
                        print("    %-28s %-24s errs %d/%d  marks %d->%d  rows %d->%d  dv-004 %s"
                              % (name, key, f["pageerrors"], f["console_errors"],
                                 f["filter"]["marks_before"], f["filter"]["marks_after"],
                                 f["filter"]["rows_before"], f["filter"]["rows_after"],
                                 ("min %.3fpx" % min(px)) if px else "n/a"))
            out_pages[name] = {"sources": sources_for(page_path), "combos": combos}
        browser.close()
    return version, out_pages


def load_receipts():
    if os.path.isfile(RECEIPTS):
        return json.load(open(RECEIPTS, encoding="utf-8"))
    return {}


def main():
    ap = argparse.ArgumentParser(
        prog="python3 knowledge/_drive_chart_engine.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="re-hash the recorded sources and report FRESH/STALE per page; drives nothing")
    ap.add_argument("--page", action="append", default=None,
                    help="drive only this page (basename, e.g. donut.html); repeatable, merges into the receipts")
    args = ap.parse_args()

    if args.check:
        rec = load_receipts()
        if not rec:
            print("❌ no receipts at %s — run: python3 knowledge/_drive_chart_engine.py"
                  % os.path.relpath(RECEIPTS, ROOT))
            return 1
        rows = freshness(rec)
        stale = 0
        for page, state, files in rows:
            print("  [%s] %s" % (state, page))
            for f in files:
                print("      stale source: %s" % f)
            stale += 1 if state == "STALE" else 0
        recorded = set(rec.get("pages", {}))
        found = {os.path.basename(p) for p in glob.glob(os.path.join(PAGES_DIR, "*.html"))}
        for missing in sorted(found - recorded):
            print("  [MISSING] %s — no receipt at all" % missing)
            stale += 1
        if stale:
            print("\n❌ %d page(s) STALE/MISSING — re-drive: python3 knowledge/_drive_chart_engine.py" % stale)
            return 1
        print("\n✅ all %d receipt(s) FRESH (driven %s, Chromium %s)."
              % (len(rows), rec.get("driven", "?"), rec.get("chromium", "?")))
        return 0

    all_pages = sorted(glob.glob(os.path.join(PAGES_DIR, "*.html")))
    if args.page:
        want = set(args.page)
        all_pages = [p for p in all_pages if os.path.basename(p) in want]
        if not all_pages:
            print("❌ no test page matched %s" % sorted(want))
            return 1
    extra = os.environ.get("APOLLO_PW_LD_LIBRARY_PATH")
    if extra and extra not in os.environ.get("LD_LIBRARY_PATH", ""):
        os.environ["LD_LIBRARY_PATH"] = extra + ":" + os.environ.get("LD_LIBRARY_PATH", "")

    print("Driving %d chart-engine test page(s) × %d themes × %d modes …"
          % (len(all_pages), len(THEMES), len(MODES)))
    version, driven = drive(all_pages)

    rec = load_receipts()
    pages = rec.get("pages", {})
    pages.update(driven)
    rec = {
        "_consumer": "knowledge/_validate_dataviz.py — dv-004 on engine-drawn charts (s260-D3). "
                     "Re-drive with: python3 knowledge/_drive_chart_engine.py",
        "chromium": version,
        "driven": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "themes": list(THEMES),
        "modes": list(MODES),
        "pages": pages,
    }
    with open(RECEIPTS, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\n✅ wrote %s (Chromium %s, %d page(s))."
          % (os.path.relpath(RECEIPTS, ROOT), version, len(driven)))
    print("   Consumer: python3 knowledge/_validate_dataviz.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
