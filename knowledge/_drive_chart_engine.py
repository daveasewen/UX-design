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

  /* #261 D3 — butterfly-v's BASELINE JOIN. The two wings meet at y=0; dv-render cuts half a GAP
     off each wing so the pair is separated by the full 2.2px. That number was provable and
     UNGATED (nothing measured it), so it is measured here, on the drawn bounding boxes, exactly
     as a rect stack is: the minimum vertical clearance between adjacent marks in one column. */
  function baselineJoin(svg, marks) {
    const g = stackGap(svg, marks);
    return { px: g.px, note: g.px === null ? g.note : ('baseline join, ' + g.note) };
  }

  /* ---------- #261 D3: THE VACUOUS SIBLINGS, read off the DRAWN DOM -------------------------
     dv-009 / dv-016 / dv-017 / dv-line-011 all read static markup, and an engine canvas has no
     static marks — so every one of them was vacuous (proved by _tests/chart-engine/
     _probe_fail_open.py: 0/6 venues bit). These read the same facts from the rendered tree. */

  function rgbOf(str) {
    const m = /rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,/\s]+([\d.]+))?/i.exec(str || '');
    if (!m) { return null; }
    const a = m[4] === undefined ? 1 : parseFloat(m[4]);
    return [parseFloat(m[1]), parseFloat(m[2]), parseFloat(m[3]), a];
  }

  function lum(c) {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
  }

  /* the painted surface behind the figure: first ancestor with a non-transparent background */
  function surfaceOf(el) {
    let n = el;
    while (n && n.nodeType === 1) {
      const c = rgbOf(getComputedStyle(n).backgroundColor);
      if (c && c[3] > 0.01) { return c; }
      n = n.parentElement;
    }
    return [255, 255, 255, 1];
  }

  /* composite a possibly-translucent paint over the surface, then contrast it against it */
  function ratioOn(paint, surf) {
    if (!paint || paint[3] <= 0.01) { return null; }
    const a = paint[3];
    const over = [paint[0] * a + surf[0] * (1 - a), paint[1] * a + surf[1] * (1 - a),
                  paint[2] * a + surf[2] * (1 - a)];
    const l1 = lum(over), l2 = lum(surf);
    const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
    return R3((hi + 0.05) / (lo + 0.05));
  }

  const HEX = /^#[0-9a-fA-F]{3,8}$/;

  function siblings(fig, svg, marks) {
    const surf = surfaceOf(fig);
    const out = {
      /* dv-009 — flat fills */
      gradients: 0, patterns: [],
      /* dv-017 — palette-only fills: the RAW attribute the engine wrote, per mark */
      series_paint_attrs: [], series_rogue_hex: [],
      /* dv-016 — >=3:1 RENDERED contrast, computed from getComputedStyle, not from a token table */
      contrast_series_min: null, contrast_axis_min: null, contrast_grid_min: null,
      contrast_note: '',
      /* dv-line-011 — straight lines */
      curve_series: 0,
      /* the surface the ratios are against, for the receipt to be readable by a human */
      surface_rgb: surf.slice(0, 3).join(',')
    };
    if (!svg) { return out; }
    out.gradients = svg.querySelectorAll('linearGradient,radialGradient,filter').length;
    svg.querySelectorAll('pattern[id]').forEach((p) => out.patterns.push(p.id));

    const paints = new Set(), rogue = new Set();
    let cs = Infinity;
    for (const m of marks) {
      const st = getComputedStyle(m);
      for (const attr of ['fill', 'stroke']) {
        const raw = (m.getAttribute(attr) || '').trim();
        if (raw && raw !== 'none') {
          paints.add(raw);
          if (HEX.test(raw)) { rogue.add(raw); }
        }
      }
      /* dv-016 grades the mark's OWN colour — its FILL, or its STROKE when it is unfilled (a line
         or a spark). ⛔ NEVER the stroke of a filled mark: that stroke is dv-004's separating
         stroke, painted in the SURFACE colour on purpose, and reading it as a series colour scores
         a correct donut at 1.00:1. Found by driving Chart-donut's static figure, #261 D3. */
      const fillRaw = (m.getAttribute('fill') || '').trim();
      const use = (fillRaw && fillRaw !== 'none') ? 'fill' : 'stroke';
      const useRaw = (m.getAttribute(use) || '').trim();
      if (useRaw && useRaw !== 'none') {
        const r = ratioOn(rgbOf(st[use]), surf);
        if (r !== null && r < cs) { cs = r; }
      }
      if (m.tagName.toLowerCase() === 'path' && /[CSQTcsqt]/.test(m.getAttribute('d') || '')) {
        out.curve_series++;
      }
    }
    out.series_paint_attrs = Array.from(paints).sort();
    out.series_rogue_hex = Array.from(rogue).sort();
    out.contrast_series_min = isFinite(cs) ? cs : null;

    const worst = (sel) => {
      let w = Infinity, n = 0;
      svg.querySelectorAll(sel).forEach((el) => {
        const st = getComputedStyle(el);
        for (const attr of ['fill', 'stroke']) {
          const raw = (el.getAttribute(attr) || '').trim();
          if (!raw || raw === 'none') { continue; }
          const r = ratioOn(rgbOf(st[attr]), surf);
          if (r !== null) { n++; if (r < w) { w = r; } }
        }
      });
      return [isFinite(w) ? w : null, n];
    };
    const ax = worst('.dv-axis,.dv-label,.dv-baseline');
    const gr = worst('.dv-grid');
    out.contrast_axis_min = ax[0];
    out.contrast_grid_min = gr[0];
    out.contrast_note = marks.length + ' marks, ' + ax[1] + ' axis/label paints, ' + gr[1] +
                        ' gridline paints, over surface rgb(' + out.surface_rgb + ')';
    return out;
  }

  const RADIAL = { donut: 1, pie: 1 };
  const STACK = { stacked: 1, 'stacked-column': 1, 'stacked-bar': 1 };
  const JOIN = { 'butterfly-v': 1 };

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
      } else if (JOIN[dtype]) {
        const g = baselineJoin(svg, marks);
        out.dv004_px = g.px; out.dv004_note = g.note;
      }
    }
    const sib = siblings(fig, svg, marks);
    for (const k in sib) { out[k] = sib[k]; }
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

# #261 D3 — requiredAria, read off the RENDERED DOM.
# `_validate_snippets.py` asks "is this string somewhere in the file", which a JS STRING LITERAL
# satisfies: six shipped snippets pass a requiredAria string that way today, and stripping every
# role/aria-label at runtime leaves that gate green (4th venue of [[no-gate-parses-the-artefact]]).
# The receipt records which of the manifest's own strings survive into the tree the browser built,
# plus the figure-level a11y spine, so the route can read pixels instead of source text.
ARIA_JS = r"""
(need) => {
  const html = document.documentElement.outerHTML;
  const figs = Array.prototype.slice.call(document.querySelectorAll('figure.dv'));
  const per = {};
  figs.forEach((f, i) => {
    const svg = f.querySelector('svg.dv-svg');
    per[f.id || ('fig-' + i)] = {
      fig_role: f.getAttribute('role') || null,
      fig_label: f.getAttribute('aria-label') || f.getAttribute('aria-labelledby') || null,
      svg_role: svg ? (svg.getAttribute('role') || null) : null,
      svg_label: svg ? (svg.getAttribute('aria-label') || svg.getAttribute('aria-labelledby') || null) : null,
      table_rows: f.querySelectorAll('table.dv-table tbody tr').length
    };
  });
  return {
    required: (need || []).slice(),
    present: (need || []).filter((n) => html.indexOf(n) >= 0),
    missing: (need || []).filter((n) => html.indexOf(n) < 0),
    figures: per
  };
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


_ARIA_MANIFEST_RE = re.compile(
    r'<script type="application/json" id="token-manifest">(.*?)</script>', re.S)


def required_aria_of(path):
    """The snippet's OWN `requiredAria` list, from its #token-manifest. [] for a test page."""
    try:
        m = _ARIA_MANIFEST_RE.search(open(path, encoding="utf-8").read())
        return json.loads(m.group(1)).get("requiredAria", []) if m else []
    except Exception:
        return []


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
            need = required_aria_of(page_path)
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
                    aria = page.evaluate(ARIA_JS, need)
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
                        "aria": aria,
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
                        cs = [v["contrast_series_min"] for v in f["figures"].values()
                              if v.get("contrast_series_min") is not None]
                        rogue = sum(len(v.get("series_rogue_hex", [])) for v in f["figures"].values())
                        grad = sum(v.get("gradients", 0) for v in f["figures"].values())
                        curve = sum(v.get("curve_series", 0) for v in f["figures"].values())
                        print("    %-34s %-18s errs %d/%d  marks %d->%d  rows %d->%d  dv-004 %s  "
                              "contrast %s  rogue %d  grad %d  curve %d  aria %d/%d"
                              % (name, key, f["pageerrors"], f["console_errors"],
                                 f["filter"]["marks_before"], f["filter"]["marks_after"],
                                 f["filter"]["rows_before"], f["filter"]["rows_after"],
                                 ("min %.3fpx" % min(px)) if px else "n/a",
                                 ("min %.2f:1" % min(cs)) if cs else "n/a",
                                 rogue, grad, curve, len(aria["present"]), len(aria["required"])))
            # `self_sha256` is the hash of the artefact ITSELF (#261 D3). `sources` proves the code
            # behind the receipt has not moved; this proves the FILE UNDER JUDGMENT is the file
            # that was driven. Without it a receipt found by BASENAME is evidence for whatever
            # bytes happen to share the name — which is how a mutated copy stayed green.
            out_pages[name] = {"sources": sources_for(page_path),
                               "self_sha256": sha256_of(page_path),
                               "combos": combos}
        browser.close()
    return version, out_pages


SNIPPETS_GLOB = os.path.join(HERE, "snippets", "Chart-*.reference.html")


def all_artefacts():
    """Every artefact the receipt must cover: the 13 engine TEST PAGES **and** the 14 shipped
    `Chart-*.reference.html` SNIPPETS (#261 D3).

    ⛔ WHY THE SNIPPETS. Before #261 D3 the receipt measured only the test pages, while
    `_validate_dataviz.py` GRADES the snippets — so the evidence was for a different file than the
    one under judgment, and any engine fault living in a snippet's inlined copy was invisible. The
    snippets are self-contained (the engine is injected into them), so driving them is driving the
    artefact that actually ships. Both are keyed by basename in the same `pages` map; the test
    pages stay because they exercise the engine's LINKED canon files, whose hashes are what make a
    canon edit go STALE.
    """
    return sorted(glob.glob(os.path.join(PAGES_DIR, "*.html")) + glob.glob(SNIPPETS_GLOB))


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
        found = {os.path.basename(p) for p in all_artefacts()}
        for missing in sorted(found - recorded):
            print("  [MISSING] %s — no receipt at all" % missing)
            stale += 1
        if stale:
            print("\n❌ %d page(s) STALE/MISSING — re-drive: python3 knowledge/_drive_chart_engine.py" % stale)
            return 1
        print("\n✅ all %d receipt(s) FRESH (driven %s, Chromium %s)."
              % (len(rows), rec.get("driven", "?"), rec.get("chromium", "?")))
        return 0

    all_pages = all_artefacts()
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
