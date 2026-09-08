#!/usr/bin/env python3
"""DataViz gate — the new-surface gate that lands WITH the first chart (never after).

Charts are semantic SVG in the DOM, styled by tokens, animated by CSS, described by a real
<table> (method: _proforma/_DATAVIZ-METHOD.md; ratified dossier reviews/DATAVIZ-METHOD-2026-07-16.html
§06). SVG-in-DOM is what makes the KB's chart rules statically / render-checkable — a canvas chart
would be invisible to every gate we run.

Discovers knowledge/_proforma/*.html that carry the DataViz signature (the string APOLLO-DATAVIZ)
and gates every chart <figure class="dv" data-dv-type="..."> inside them. Writes _DATAVIZ-GATE.md;
exits non-zero on any BLOCKING failure. Run `--selftest` to bite-test each check against inline
good/broken fixtures (a deliberately broken chart MUST fail) — no files touched.

CHART DOM CONTRACT (what a compliant chart looks like — enforced below):
  <figure class="dv" data-dv-type="kpi|column|bar|grouped|stacked|line|multiline|spark|donut|combo"
          [data-domain-min="0"]      bar-family only — zero baseline (dv-bar-009)
          [data-total="…"]           donut/pie only — sum-to-total (dv-pie-010/011)
          [data-surface="page|raised"] which mode surface the chart sits on (contrast base)
          role="group" aria-labelledby="…">
    <svg class="dv-svg" aria-hidden="true"> series els class="dv-series" fill="var(--data-series-N)" … </svg>
    <table class="dv-table"> real data </table>                (dv-005)
    <ul class="dv-legend"> <li><span class="dv-key">A</span> … </li> </ul>   (letters, §04.3)

RULE → CHECK → MODE (dossier §06). BLOCKING rows reuse check-classes already proven elsewhere
(rogue-hex, contrast, counts, gradients, baselines, slice caps, straight lines). Genuinely-new
checks enter ADVISORY-first (ADR-0005 §5) and promote after a bite-test:

  BLOCKING
    dv-009      flat fills — no <linearGradient>/<radialGradient>/<filter>; <=1 <pattern>, chevron only
    dv-017      palette-only fills — every series fill/stroke is a var() token; 0 rogue hex
    dv-016      >=3:1 RENDERED contrast — series fills + axis/label vs the surface, per mode,
                computed from the RESOLVED token value (NOT an author-declared pair — the 9/9 blind-spot fix)
    dv-004      >=2px separation — gapless surfaces (donut/stacked segments) carry a surface-coloured stroke >=2px
    dv-bar-009  zero baseline — bar-family only, data-domain-min="0"; MUST NOT fire on lines (dv-line-001 asymmetry)
    dv-bar-007  negative values vertical only — horizontal bar + a negative table value = fail
    dv-pie-009  <=6 slices — donut/pie segment count
    dv-pie-010  sum = total — donut segment values sum to the displayed centre total (rounding tolerated)
    dv-line-011 straight lines — series <path>/<polyline> carry no curve commands (C/S/Q/T); arcs (A) legal in donut only

  ADVISORY (→ blocking after bite-test)
    dv-005      tabular alternative — chart contains a real <table>
    §04.3       letters — series>=2 => letter keys on legend rows
    dv-line-009 spark aspect — spark viewBox aspect within tolerance
    dv-014      journey consistency — same series index => same fill across a view (advisory, view-scope)
    vibration   vibrating boundaries (Apollo, Dave 2026-07-16) — adjacent series-fill pairs:
                value-ratio<1.25 AND hue-sep>=135 AND both sats>=0.5 (skip pairs with a dv-004 gap)

  INHERITED (existing gates, unchanged): DEF-003 CSS-only motion · DEF-004 no-hardcode · icon-source · sentence case.

  GRIDLINES: dv-016 as written also names gridlines. Gridlines are non-essential/decorative (WCAG
  1.4.11 exempts them) and 3:1 gridlines are visually heavy — so gridline contrast is ADVISORY here,
  series-fill + axis/label contrast is BLOCKING. Standing default (dossier §08-style), movable before it bites.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, json, os, glob, sys, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA_DIR = os.path.join(HERE, "_proforma")
SIGNATURE = "APOLLO-DATAVIZ"
BAR_FAMILY = {"column", "bar", "grouped", "stacked", "combo"}

# ---- dtype vocabulary (ds-014 → ADR-0016, 2026-07-27) --------------------------------------
# The corpus FORKED without anyone noticing: `stacked` AND `stacked-column`, `grouped` AND
# `grouped-column` both ship, and `scatter` was never taught to this gate at all. Every
# dtype-keyed branch below tested only the short forms, so dv-004, dv-bar-009 and dv-line-011
# were INERT on the long ones — which is how a stacked column with 0.0px separation passed a
# BLOCKING ">=2px" rule for weeks and had to be caught by Dave's eye.
# Fixed STRUCTURALLY, not by enumeration: normalise once, here, and FAIL LOUD on any dtype this
# gate has never heard of. Enumerating the three known synonyms would only postpone the next
# miss — an unknown dtype must not be able to slip past five branches in silence again.
DTYPE_CANON = {
    "stacked-column": "stacked",
    "stacked-bar":    "stacked",
    "grouped-column": "grouped",
    "grouped-bar":    "grouped",
}
KNOWN_DTYPES = {
    "column", "bar", "grouped", "stacked", "combo",
    "line", "multiline", "spark", "kpi", "donut", "pie", "scatter",
    # Chart wave 2 (2026-08-05, #95) — placed in the DV-D02-A partition below in the same change,
    # per the import-time totality assertion (a new dtype must not skip the rule in silence):
    "butterfly-h", "butterfly-v", "histogram",
    "boxplot", "bullet", "candlestick", "stacked-area",
}

# ---------------------------------------------------------------------------
# DV-D02-A · dv-fit scope (ruled Dave 2026-07-28, session #28)
# ---------------------------------------------------------------------------
# DV-D02 says responsive = compress width, never scale proportionally, text must not scale —
# enacted as `class="dv-svg dv-fit"` on the plot svg, which the injected fit() picks up.
#
# The ledger USED to read "Cartesian charts only; horizontal bar + donut excluded". The h-bar half
# was ROT: Chart-bar.reference.html's horizontal bar has carried `dv-fit` since it was built, so the
# implementation never agreed with the text. Dave, asked directly: "horizontal bars is fine, this
# must have been a rot problem or miscommunication." Amended as DV-D02-A.
#
# The partition below is TOTAL over KNOWN_DTYPES and asserted at import. That is deliberate and it
# is the dv-vocab lesson (see the comment above DTYPE_CANON): a new dtype must not be able to land
# in neither bucket and skip this rule in silence. Adding a dtype to KNOWN_DTYPES without placing it
# here is an ImportError, not a silent pass.
CARTESIAN_DTYPES = {
    "column", "bar", "grouped", "stacked", "combo", "line", "multiline", "scatter",
    # Chart wave 2 (2026-08-05, #95): all seven new frames are x/y plots — width-compression with
    # non-scaling text applies exactly as DV-D02 states. Measured on the artefacts, not assumed:
    # every one carries a 580-wide cartesian plot region (bullet's is 580x200, receipted).
    "butterfly-h", "butterfly-v", "histogram",
    "boxplot", "bullet", "candlestick", "stacked-area",
}
# Out of scope — and the REASON travels with the exclusion, per Dave's standing terms
# ("correctness, standardisation with flexibility rather than expediency"). A gate that encodes a
# rule without its principled exceptions is not standardisation, it is a future false positive.
NON_CARTESIAN_DTYPES = {
    "donut": "compressing a circle distorts it (DV-D02). ⚠ Dave-HEDGED, not firm: 'probably never "
             "have to scale, but I'm not 100% sure' — deferred to the 12-column-grid + breakpoints "
             "task by his instruction. Do not harden 'never' into a rule.",
    "pie":   "same circle argument as donut (DV-D02).",
    "spark": "VACUOUSLY out of scope, not excluded: a sparkline carries no text, so the "
             "non-scaling-text constraint has nothing to bind. Its fit rides a separate CSS release "
             "(figure.dv-fit-on .spark-standalone), receipted in the registry $note. Do not 'fix' "
             "it by adding dv-fit.",
    "kpi":   "a KPI figure is a number, not a plot — it has no value axis to relayout.",
}
# Waivers: cartesian, genuinely non-compliant, but non-compliant BY RULING rather than by accident.
# A waiver demotes blocking -> advisory and must carry both a reason and the condition that clears it.
DV_FIT_WAIVED = {
    # EMPTY — a state with a history, not an oversight.
    #
    # "scatter" lived here from #27 to #72 and was deleted 2026-08-01 (#72) because its RE-SCOPED
    # clears-when was met on BOTH surfaces this gate scans. Provenance, so a later session cannot
    # mistake a discharge for a quiet drop:
    #   · #27 FENCED it (Dave): adopting fit moves every gridline, so it ships with a paired
    #     before/after control or not at all.
    #   · #69 PART-DISCHARGED it — the ds-020 axis/grid COLOUR migration landed with that control.
    #     It STAYED because one label hid TWO conditions: the check also reads the data-fx hooks.
    #   · #71 did the SNIPPET half and ATTEMPTED discharge. REVERTED — the clears-when named a
    #     CONDITION but not a SCOPE, so it read as met the moment one surface met it while
    #     _proforma/DataViz-interactive.html was still 0-of-1. #71 re-scoped it to name the proforma.
    #   · #72 did the PROFORMA half and discharged for real. The 12 bare <circle>s were WRAPPED in
    #     <g class="dv-marker" data-fx data-x0> — fitOne()/fitCharts() branch on TAG and there is no
    #     `circle` branch, so re-classing alone would have done nothing. Render-proven at 600/1180:
    #     viewBox 544/864, no longer pinned at 580, tick labels 12px at BOTH widths. canon/ untouched.
    #
    # ⚠ MUTATION-TESTED AT DISCHARGE, and it DISCRIMINATES — two arms, two different failures,
    # which is exactly what #71's invalid test lacked:
    #     CONTROL                  viewBox 544 | 12/12 markers translated
    #     dv-fit stripped          viewBox 580 (PINNED) | 0 translated
    #     marker data-fx stripped  viewBox 544 (tracks) | 0 translated
    #
    # ⚠ SCOPE, stated because this waiver died of an unstated one: the scan is exactly two globs
    # (_proforma/*.html carrying the signature + snippets/Chart-*.reference.html). Three other repo
    # files hold a scatter figure and are NOT gated — snippets/_REVIEW-66-scatter-title-before.html
    # and reviews/_specimen-chart-scatter-69.html are FROZEN before/specimen artefacts whose value
    # is being unfixed; __tmp_moved.html at the repo root is debris. A scatter added to a gated glob
    # without the hooks is now BLOCKING.
}
_unplaced = KNOWN_DTYPES - CARTESIAN_DTYPES - set(NON_CARTESIAN_DTYPES)
if _unplaced:
    raise ImportError(
        "DV-D02-A partition is not total: %s in KNOWN_DTYPES but in neither CARTESIAN_DTYPES nor "
        "NON_CARTESIAN_DTYPES. Place it (with a reason, if excluded) — an unplaced dtype would skip "
        "the dv-fit rule in silence, which is the dv-vocab defect this gate already learned once."
        % sorted(_unplaced))
if set(DV_FIT_WAIVED) - CARTESIAN_DTYPES:
    raise ImportError("DV_FIT_WAIVED may only waive cartesian dtypes; got %s"
                      % sorted(set(DV_FIT_WAIVED) - CARTESIAN_DTYPES))


def _seg_has_surface_stroke(seg):
    """dv-004, mechanism 1: a >=2px stroke painted in the surface colour."""
    sw = re.search(r'stroke-width="?\s*([\d.]+)', seg) or re.search(r'stroke-width:\s*([\d.]+)', seg)
    stroke = re.search(r'stroke="([^"]+)"', seg)
    return bool(sw and float(sw.group(1)) >= 2 and stroke
                and ("page" in stroke.group(1) or "raised" in stroke.group(1) or "surf" in stroke.group(1)))


def _rect_stack_gap(segs, minimum=2.0):
    """dv-004, mechanism 2: REAL geometric separation in a rect stack.

    Returns (True | False | None, detail). None = not statically measurable (arcs/paths, or a
    horizontal stack whose columns don't group by x) — in which case the caller falls back to
    demanding the stroke, so an unmeasurable chart fails SAFE rather than passing silently.

    Vertical stacks group by x; within a column, segments sorted by y ascending run top-to-bottom,
    so the gap below segment i is y[i+1] - (y[i] + h[i]). dv-004 says MINIMUM 2px — a larger gap
    passes, which is the point Dave made when he ruled the geometry route on 2026-07-27.
    """
    cols = {}
    for seg in segs:
        x = re.search(r'\bx="([\d.]+)"', seg)
        y = re.search(r'\by="([\d.]+)"', seg)
        h = re.search(r'\bheight="([\d.]+)"', seg)
        if not (x and y and h):
            return (None, "segments are not measurable rects")
        cols.setdefault(x.group(1), []).append((float(y.group(1)), float(h.group(1))))
    worst = None
    for x, rows in cols.items():
        if len(rows) < 2:
            continue
        rows.sort()
        for (y1, h1), (y2, _h2) in zip(rows, rows[1:]):
            gap = y2 - (y1 + h1)
            if worst is None or gap < worst[0]:
                worst = (gap, x)
    if worst is None:
        return (None, "no column carries 2+ segments")
    gap, x = worst
    if gap + 1e-6 >= minimum:
        return (True, "smallest measured gap %.2fpx at x=%s" % (gap, x))
    return (False, "smallest measured gap is %.2fpx at x=%s (needs >=%.0fpx)" % (gap, x, minimum))
CURVE_CMDS = re.compile(r'[CSQTcsqt]')

# ---------------------------------------------------------------------------------------------
# DRIVEN RECEIPTS — dv-004 on an ENGINE-DRAWN chart (s260-D3, Dave, 2026-09-08)
# ---------------------------------------------------------------------------------------------
# "DRIVEN RECEIPTS BECOME THE GATE FOR ENGINE-DRAWN CHARTS. Where a dataviz rule reads static
#  geometry (dv-004 and its siblings) and the chart is drawn at runtime by knowledge/canon/
#  dv-render.js, _validate_dataviz accepts a COMMITTED driven receipt (a Playwright measurement
#  recorded from knowledge/_tests/chart-engine/) as the evidence for that rule — the gate is
#  'static OR driven', never skipped. Option (b), an engine-emitted self-report marker trusted by
#  the static gate, is REFUSED."
#
# WHY THIS EXISTS. #259 emptied Chart-donut's spider canvas: `dvRender(fig, DATA)` now draws every
# arc at runtime, so there is NO `path.dv-series` in the file for the static rule to read. The
# chart met dv-004 by real geometry in a browser and the gate failed it anyway — the second visit
# of [[no-gate-parses-the-artefact]] in one session.
#
# THE ROUTE IS NEVER A SKIP. An engine-drawn chart with no receipt, an unmapped snippet, a receipt
# whose recorded source hashes no longer match the bytes on disk, or ANY of the 8 theme×mode
# combinations measuring below 2.0px is a BLOCKING failure that names what to do about it. A chart
# that still carries its marks in the markup keeps the static route, untouched.
RECEIPTS_PATH = os.path.join(HERE, "_tests", "chart-engine", "_receipts.json")
DRIVE_CMD = "python3 knowledge/_drive_chart_engine.py"
DV004_MIN_PX = 2.0

# snippet basename -> the driven test page that exercises the SAME engine + type partial.
# Explicit, not inferred: a mapping you can read is a mapping a reviewer can falsify.
ENGINE_TEST_PAGE = {
    "Chart-donut.reference.html":       "donut.html",
    "Chart-pie.reference.html":         "donut.html",   # pie is the ri=0 arm of the same partial
    "Chart-bar.reference.html":         "bar.html",
    "Chart-line.reference.html":        "line.html",
    "Chart-combo.reference.html":       "combo.html",
    "Chart-sparkline.reference.html":   "sparkline.html",
    "Chart-stacked-area.reference.html": "stacked-area.html",
    # ---- s259-D1 fast follower, #260. Every engine-drawn member maps to ITS OWN test page, so a
    #      receipt is never evidence for code the snippet does not load. Chart-pie is the one
    #      exception above and it is a COMPOSITION, not a shortcut: Chart-pie consumes
    #      dv-render-donut (there is no dv-render-pie.js) and donut.html exercises both arms.
    "Chart-scatter.reference.html":      "scatter.html",
    "Chart-histogram.reference.html":    "histogram.html",
    "Chart-boxplot.reference.html":      "boxplot.html",
    "Chart-bullet.reference.html":       "bullet.html",
    "Chart-candlestick.reference.html":  "candlestick.html",
    "Chart-butterfly-h.reference.html":  "butterfly-h.html",
    "Chart-butterfly-v.reference.html":  "butterfly-v.html",
}

_RECEIPTS_CACHE = {}


def _load_receipts(path=None):
    path = path or RECEIPTS_PATH
    if path not in _RECEIPTS_CACHE:
        try:
            _RECEIPTS_CACHE[path] = json.load(open(path, encoding="utf-8"))
        except Exception:
            _RECEIPTS_CACHE[path] = None
    return _RECEIPTS_CACHE[path]


def _sha256(path):
    h = __import__("hashlib").sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_engine_drawn(segs, page_html):
    """No series marks in the markup + the page drives the engine => the chart is drawn at runtime."""
    if segs:
        return False
    if not page_html:
        return False
    return ("dvRender(" in page_html) or ("dv-render" in page_html)


def driven_dv004(page_html_path, dtype, raw_dtype, receipts_path=None, root=None):
    """dv-004 via a COMMITTED driven receipt. Returns (ok, message).

    ok is True only when: a receipt file exists, the snippet maps to a test page, that page has a
    receipt, every recorded source still hashes to the bytes on disk, a figure of this dtype was
    measured, all 8 theme x mode combinations are present, and every one of them is >= 2.0px.
    Anything else is False — a BLOCKING failure that names the first obstacle.
    """
    root = root or os.path.dirname(HERE)
    rec = _load_receipts(receipts_path)
    where = os.path.relpath(receipts_path or RECEIPTS_PATH, root)
    if not rec:
        return (False, "dv-004: %s is ENGINE-DRAWN (no marks in the markup) and there is no driven "
                       "receipt at %s. Record one: %s" % (raw_dtype, where, DRIVE_CMD))
    base = os.path.basename(page_html_path or "")
    page = ENGINE_TEST_PAGE.get(base)
    if not page:
        return (False, "dv-004: %s is ENGINE-DRAWN but %s is not mapped to a chart-engine test page "
                       "(ENGINE_TEST_PAGE in this file). Add the mapping and drive it: %s"
                       % (raw_dtype, base or "this file", DRIVE_CMD))
    entry = (rec.get("pages") or {}).get(page)
    if not entry:
        return (False, "dv-004: %s is ENGINE-DRAWN and maps to %s, but %s holds no driven receipt "
                       "for that page. Record one: %s" % (raw_dtype, page, where, DRIVE_CMD))
    for rel, want in sorted((entry.get("sources") or {}).items()):
        p = os.path.join(root, rel)
        got = _sha256(p) if os.path.isfile(p) else None
        if got != want:
            return (False, "dv-004: the driven receipt for %s is STALE — %s has changed since it was "
                           "driven%s. Re-drive: %s"
                           % (page, rel, " (file is missing)" if got is None else "", DRIVE_CMD))
    combos = entry.get("combos") or {}
    if not combos:
        return (False, "dv-004: the driven receipt for %s records no theme x mode combination. "
                       "Re-drive: %s" % (page, DRIVE_CMD))
    want_combos = len(rec.get("themes") or []) * len(rec.get("modes") or []) or 8
    if len(combos) < want_combos:
        return (False, "dv-004: the driven receipt for %s covers %d of %d theme x mode combinations. "
                       "Re-drive: %s" % (page, len(combos), want_combos, DRIVE_CMD))
    seen = []
    for combo in sorted(combos):
        figs = (combos[combo].get("figures") or {})
        hit = [(fid, f) for fid, f in sorted(figs.items())
               if f.get("dtype") == dtype and f.get("dv004_px") is not None]
        if not hit:
            return (False, "dv-004: the driven receipt for %s carries no measured %s figure in combo "
                           "%s — the receipt cannot stand in for the static rule it replaces. "
                           "Re-drive: %s" % (page, dtype, combo, DRIVE_CMD))
        for fid, f in hit:
            px = float(f["dv004_px"])
            seen.append((px, combo, fid))
            if px < DV004_MIN_PX:
                return (False, "dv-004: driven receipt FAILS — %s/%s measured %.3fpx of separation "
                               "in combo %s (rule is >=%.1fpx). Source: %s"
                               % (page, fid, px, combo, DV004_MIN_PX, where))
    worst = min(seen)
    return (True, "dv-004: PASSED by driven receipt — %s/%s measured %.3fpx (worst of %d "
                  "measurements across %d theme x mode combos, rule >=%.1fpx), driven %s on "
                  "Chromium %s. Source: %s"
                  % (page, worst[2], worst[0], len(seen), len(combos), DV004_MIN_PX,
                     rec.get("driven", "?"), rec.get("chromium", "?"), where))


def driven_dv004_recorded(page_html_path, raw_dtype, receipts_path=None, root=None):
    """s260-D3, the SECOND half: grade a dv-004 figure the receipt ACTUALLY MEASURED, whatever
    the dtype. Returns (ok, message) or (None, None) when there is nothing measured to grade.

    The dtype-scoped route above answers "does this chart owe dv-004 and can it prove it". This
    one answers a narrower and strictly-additive question: the driver measured a separation on
    this page and WROTE IT DOWN — so if that number is below 2.0px in any combination, the gate
    goes red. `dv-004 and its siblings … static OR driven, never skipped`: a recorded figure that
    nothing reads is a skip wearing a receipt.

    ⛔ IT DELIBERATELY DOES NOT WIDEN THE RULE. An UNMAPPED snippet, or a receipt whose figures all
    carry `dv004_px: null` (the driver only measures radial and stacked joins) => (None, None), no
    opinion, no failure. The no-opinion arm can only ever be reached by a receipt that EXISTS and is
    FRESH.

    #260 — ORDER IS THE WHOLE POINT. The freshness arms run FIRST, for any member the map names:
    an engine page whose receipt is missing, or whose recorded source hashes no longer match the
    bytes on disk, is BLOCKING before we ever ask whether a dv-004 figure was measured. Ordering it
    the other way (V2's finding) meant 12 of the 13 engine pages — every type whose join the driver
    does not measure — took the (None, None) exit ahead of the STALE arm, so editing an engine
    source and never re-driving left the gate GREEN and only `--check` caught it. That is `static
    OR driven, never skipped` failing on the "driven" side.
    """
    base = os.path.basename(page_html_path or "")
    page = ENGINE_TEST_PAGE.get(base)
    if not page:
        return (None, None)
    root = root or os.path.dirname(HERE)
    where = os.path.relpath(receipts_path or RECEIPTS_PATH, root)
    rec = _load_receipts(receipts_path)
    if not rec:
        return (False, "dv-004: %s is ENGINE-DRAWN and maps to the chart-engine test page %s, but "
                       "there is no driven receipt at %s. Record one: %s"
                       % (raw_dtype, page, where, DRIVE_CMD))
    entry = (rec.get("pages") or {}).get(page)
    if not entry:
        return (False, "dv-004: %s is ENGINE-DRAWN and maps to %s, but %s holds no driven receipt "
                       "for that page. Record one: %s" % (raw_dtype, page, where, DRIVE_CMD))
    for rel, want in sorted((entry.get("sources") or {}).items()):
        p = os.path.join(root, rel)
        got = _sha256(p) if os.path.isfile(p) else None
        if got != want:
            return (False, "dv-004: %s is ENGINE-DRAWN and its driven receipt (%s) is STALE — %s "
                           "has changed since it was driven%s. Re-drive: %s"
                           % (raw_dtype, page, rel, " (file is missing)" if got is None else "",
                              DRIVE_CMD))
    combos = entry.get("combos") or {}
    seen = []
    for combo in sorted(combos):
        for fid, f in sorted((combos[combo].get("figures") or {}).items()):
            if f.get("dv004_px") is not None:
                seen.append((float(f["dv004_px"]), combo, fid))
    if not seen:
        return (None, None)
    worst = min(seen)
    if worst[0] < DV004_MIN_PX:
        return (False, "dv-004: driven receipt FAILS — %s/%s measured %.3fpx of separation in "
                       "combo %s (rule is >=%.1fpx). The figure is RECORDED, so the rule is "
                       "graded whatever the dtype (s260-D3). Source: %s"
                       % (page, worst[2], worst[0], worst[1], DV004_MIN_PX, where))
    return (True, "dv-004: PASSED by driven receipt — %s/%s measured %.3fpx (worst of %d recorded "
                  "measurements across %d theme x mode combos, rule >=%.1fpx). Source: %s"
                  % (page, worst[2], worst[0], len(seen), len(combos), DV004_MIN_PX, where))


# ---------------------------------------------------------------------------------------------
# #261 D3 — THE DRIVER SCOPE. The siblings dv-009 / dv-016 / dv-017 / dv-line-011 and requiredAria
# ---------------------------------------------------------------------------------------------
# s260-D3 built the driven route and pointed it at dv-004 only. #260's wrap named what was left:
#
#   "only donut.html measures dv-004; butterfly-v's 2.200px baseline join is provable and ungated;
#    siblings dv-016/017/009/line-011 vacuous on an engine canvas (2nd + 3rd venue).
#    `requiredAria`/`requiredDeclarations` pass on a JS string literal — fails OPEN (4th/5th
#    venue of [[no-gate-parses-the-artefact]])."
#
# PROVED, not assumed. `_tests/chart-engine/_probe_fail_open.py` mutates the INLINED engine on a
# temp copy of a shipped snippet so the RENDERED DOM violates each rule, shows the violation in a
# real Chromium, and runs this gate over it. Before this block: 0 of 6 venues bit — a runtime
# `#ff2200`, a runtime `<linearGradient>`, curved series paths, a butterfly-v baseline join driven
# from 2.200px to -0.000px, and a DOM with every role/aria-label stripped were all GREEN.
#
# THE FIX IS THE SAME ROUTE, NOT A NEW ONE. The driver now records, per figure per theme x mode,
# the facts each of those rules reads — the paint ATTRIBUTES the engine wrote, the contrast of the
# RESOLVED colours against the painted surface, gradient/pattern counts, curve commands, and which
# of the snippet's own `requiredAria` strings survive into the built tree. This gate grades those
# recorded numbers exactly as it grades the static ones: static OR driven, NEVER skipped.
#
# ⛔ IT INVENTS NO RULE. Every arm below is silent unless the receipt carries the fact; what it
# refuses to do is pass a chart because the fact was unreadable. A missing receipt, an unmapped
# artefact, a stale source hash or a short combo set is BLOCKING and names the remedy.
DRIVEN_CONTRAST_MIN = 3.0
CHEVRON_ONLY = "chevron"
_LINEISH = ("line", "multiline", "spark", "column", "bar", "grouped", "stacked", "kpi", "combo")


def _resolve_receipt(page_html_path, receipts_path=None, root=None):
    """(key, entry, where, error) — the receipt entry for the artefact actually under judgment.

    PREFERS the artefact's OWN receipt (the driver now drives the shipped snippets themselves) and
    falls back to the ENGINE_TEST_PAGE mapping for anything only the test pages cover. `error` is a
    ready-made blocking sentence when there is nothing to grade against; (None, None, where, None)
    means "this artefact is not in the driven set at all" — the caller stays silent.
    """
    base = os.path.basename(page_html_path or "")
    root = root or os.path.dirname(HERE)
    where = os.path.relpath(receipts_path or RECEIPTS_PATH, root)
    rec = _load_receipts(receipts_path)
    key = base if base in ((rec or {}).get("pages") or {}) else ENGINE_TEST_PAGE.get(base)
    if not key:
        return (None, None, where, None)
    if not rec:
        return (key, None, where,
                "%s is ENGINE-DRAWN and maps to %s, but there is no driven receipt at %s. "
                "Record one: %s" % (base, key, where, DRIVE_CMD))
    entry = (rec.get("pages") or {}).get(key)
    if not entry:
        return (key, None, where,
                "%s is ENGINE-DRAWN and maps to %s, but %s holds no driven receipt for it. "
                "Record one: %s" % (base, key, where, DRIVE_CMD))
    for rel, want in sorted((entry.get("sources") or {}).items()):
        p = os.path.join(root, rel)
        got = _sha256(p) if os.path.isfile(p) else None
        if got != want:
            return (key, None, where,
                    "the driven receipt for %s is STALE — %s has changed since it was driven%s. "
                    "Re-drive: %s" % (key, rel, " (file is missing)" if got is None else "", DRIVE_CMD))
    # #261 D3 — the receipt must be evidence for THESE BYTES. The lookup is by basename, so without
    # this a receipt vouches for any file that happens to share the name. (Found by the mutation
    # probe: a mutated copy of a snippet was graded green on the pristine snippet's receipt.)
    want_self = entry.get("self_sha256")
    if want_self and page_html_path and os.path.isfile(page_html_path):
        if _sha256(page_html_path) != want_self:
            return (key, None, where,
                    "the driven receipt for %s is STALE — the artefact itself has changed since it "
                    "was driven. Re-drive: %s" % (key, DRIVE_CMD))
    combos = entry.get("combos") or {}
    want_n = len(rec.get("themes") or []) * len(rec.get("modes") or []) or 8
    if len(combos) < want_n:
        return (key, None, where,
                "the driven receipt for %s covers %d of %d theme x mode combinations — a partial "
                "receipt is not evidence. Re-drive: %s" % (key, len(combos), want_n, DRIVE_CMD))
    return (key, entry, where, None)


def _fig_records(entry, fig_id, fig_index):
    """[(combo, figure record)] for one figure across every recorded combo. The driver keys a
    figure by its id, falling back to `fig-<index>` — the same order this gate walks them in."""
    out = []
    for combo in sorted(entry.get("combos") or {}):
        figs = (entry["combos"][combo].get("figures") or {})
        rec = figs.get(fig_id) if fig_id else None
        if rec is None:
            rec = figs.get("fig-%d" % fig_index)
        if rec is not None:
            out.append((combo, rec))
    return out


def driven_dv004_figure(page_html_path, raw_dtype, fig_id, fig_index,
                        receipts_path=None, root=None):
    """dv-004 for ONE figure, from that figure's OWN driven record. (ok, message); ok None = silent.

    ⛔ WHY FIGURE-SCOPED. `driven_dv004_recorded` takes the MINIMUM across every figure on the
    receipted page. That was safe while the receipts only covered the engine test pages, which
    carry one chart each. It is NOT safe now the driver drives the shipped snippets: Chart-donut
    ships an engine-drawn donut (2.109px of real geometry) NEXT TO a markup-authored donut that
    meets dv-004 by the other legal mechanism — a surface-coloured separating stroke, hence a
    measured gap of 0.000px. Mixing them fails a correct chart on its neighbour's evidence. Each
    figure is graded on its own record, and the static figure keeps the static route it always had.
    """
    key, entry, where, err = _resolve_receipt(page_html_path, receipts_path, root)
    if key is None or os.path.basename(page_html_path or "") != key:
        return (None, None)          # no receipt of its OWN — the page-scoped arms still apply
    if err:
        return (False, "dv-004: " + err)
    recs = _fig_records(entry, fig_id, fig_index)
    measured = [(float(r["dv004_px"]), combo) for combo, r in recs if r.get("dv004_px") is not None]
    if not measured:
        return (None, None)          # nothing measured for this figure: no rule invented
    worst = min(measured)
    if worst[0] < DV004_MIN_PX:
        return (False, "dv-004: driven receipt FAILS — %s figure %s measured %.3fpx of separation "
                       "in combo %s (rule is >=%.1fpx). Source: %s"
                       % (raw_dtype, fig_id or ("fig-%d" % fig_index), worst[0], worst[1],
                          DV004_MIN_PX, where))
    return (True, "dv-004: PASSED by driven receipt — %s figure %s measured %.3fpx (worst of %d "
                  "measurements across %d theme x mode combos, rule >=%.1fpx). Source: %s"
                  % (raw_dtype, fig_id or ("fig-%d" % fig_index), worst[0], len(measured),
                     len(entry.get("combos") or {}), DV004_MIN_PX, where))


def driven_siblings(page_html_path, dtype, raw_dtype, fig_id, fig_index,
                    receipts_path=None, root=None):
    """dv-009 / dv-017 / dv-016 / dv-line-011 from the DRIVEN receipt. Returns (blocking, advisory).

    The static arms of these four rules read `class="dv-series"` elements out of the markup. On an
    engine canvas there are none, so each rule iterates an EMPTY list and passes — vacuously. These
    arms read the browser's answer instead, and are BLOCKING on the same thresholds.
    """
    B, A = [], []
    key, entry, where, err = _resolve_receipt(page_html_path, receipts_path, root)
    if key is None:
        return (B, A)
    if err:
        B.append("dv-009/016/017/line-011: " + err)
        return (B, A)
    recs = _fig_records(entry, fig_id, fig_index)
    if not recs:
        B.append("dv-009/016/017/line-011: %s is ENGINE-DRAWN and %s has a receipt for %s, but no "
                 "record for figure %s — the siblings would grade nothing. Re-drive: %s"
                 % (raw_dtype, where, key, fig_id or ("fig-%d" % fig_index), DRIVE_CMD))
        return (B, A)

    seen_marks = max(r.get("marks") or 0 for _c, r in recs)
    if not seen_marks:
        B.append("dv-009/016/017/line-011: %s is ENGINE-DRAWN and its receipt records ZERO drawn "
                 "marks for figure %s — the engine drew nothing, so every sibling rule would pass "
                 "on an empty set. Source: %s" % (raw_dtype, fig_id or fig_index, where))
        return (B, A)

    for combo, r in recs:
        # --- dv-009 flat fills, in the DRAWN svg ---
        if r.get("gradients"):
            B.append("dv-009 [driven]: %d <linearGradient>/<radialGradient>/<filter> in the DRAWN "
                     "chart SVG in %s — fills must be flat. Source: %s" % (r["gradients"], combo, where))
        pats = r.get("patterns") or []
        if len(pats) > 1:
            B.append("dv-009 [driven]: %d <pattern>s drawn in %s — at most ONE (chevron). Source: %s"
                     % (len(pats), combo, where))
        for pid in pats:
            if CHEVRON_ONLY not in str(pid).lower():
                B.append("dv-009 [driven]: drawn <pattern id=\"%s\"> in %s — the one permitted "
                         "pattern is the chevron. Source: %s" % (pid, combo, where))

        # --- dv-017 palette-only fills, on the paint the ENGINE ACTUALLY WROTE ---
        for hexv in (r.get("series_rogue_hex") or []):
            B.append("dv-017 [driven]: the engine painted series `%s` — a raw hex, in %s. Must "
                     "resolve to a data/* or building-block token. Source: %s" % (hexv, combo, where))
        for paint in (r.get("series_paint_attrs") or []):
            if paint in ("none", "currentColor") or paint.startswith(("var(", "url(")):
                continue
            if HEX_RE.fullmatch(paint) or HEX_RE.search(paint):
                continue  # already named above
            B.append("dv-017 [driven]: the engine painted series `%s` in %s — palette-only means a "
                     "token or a url(). Source: %s" % (paint, combo, where))

        # --- dv-016 >=3:1 RENDERED contrast, computed by the browser from the resolved colours ---
        for label, field, block in (("series", "contrast_series_min", True),
                                    ("axis/label", "contrast_axis_min", True),
                                    ("gridline", "contrast_grid_min", False)):
            v = r.get(field)
            if v is None:
                continue
            if v < DRIVEN_CONTRAST_MIN:
                msg = ("dv-016 [driven, %s]: worst drawn %s contrast is %.2f:1 (<%.1f:1) in %s — %s. "
                       "Source: %s" % (label, label, v, DRIVEN_CONTRAST_MIN, combo,
                                       r.get("contrast_note", ""), where))
                (B if block else A).append(msg)

        # --- dv-line-011 straight lines, on the drawn `d` ---
        if dtype in _LINEISH and r.get("curve_series"):
            B.append("dv-line-011 [driven]: %d drawn series <path>(s) carry a curve command "
                     "(C/S/Q/T) in %s — series lines must be straight. Source: %s"
                     % (r["curve_series"], combo, where))

    B = list(dict.fromkeys(B))
    A = list(dict.fromkeys(A))
    if not B:
        A.append("dv-009/016/017/line-011: PASSED by driven receipt — figure %s, %d drawn marks, "
                 "worst series contrast %.2f:1, 0 gradients, 0 rogue hex, 0 curved series, across "
                 "%d theme x mode combos. Source: %s"
                 % (fig_id or ("fig-%d" % fig_index), seen_marks,
                    min([r.get("contrast_series_min") or 99 for _c, r in recs]), len(recs), where))
    return (B, A)


REQUIRED_ARIA_RE = re.compile(
    r'<script type="application/json" id="token-manifest">(.*?)</script>', re.S)


def required_aria_of(html):
    """The file's own `requiredAria` list, from its #token-manifest — [] when it declares none."""
    m = REQUIRED_ARIA_RE.search(html or "")
    if not m:
        return []
    try:
        return json.loads(m.group(1)).get("requiredAria", []) or []
    except Exception:
        return []


def driven_aria(page_html_path, html, receipts_path=None, root=None):
    """requiredAria against the RENDERED DOM. Returns (blocking, advisory).

    ⛔ THE VENUE THIS CLOSES. `_validate_snippets.py` asks whether each requiredAria string appears
    anywhere in the file's TEXT (minus the manifest block). A JS STRING LITERAL satisfies that, and
    six shipped snippets pass a requiredAria string exactly that way TODAY — `role="img"` on five,
    `aria-pressed` on Chart-histogram, present only inside the injected engine. The probe strips
    every role and aria-label from the built tree at runtime and that gate stays green.

    This arm grades the strings the BROWSER ended up with. It is deliberately implemented here and
    not in `_validate_snippets.py`: that file is outside this lane's fence (#261 D3 constraints),
    and the receipt route it would need already lives in this module. Named as an obstacle in the
    subreport — the source-text arm over there is still open and still fails open on its own.
    """
    B, A = [], []
    need = required_aria_of(html)
    if not need:
        return (B, A)  # nothing declared: no rule to answer, and none invented
    key, entry, where, err = _resolve_receipt(page_html_path, receipts_path, root)
    if key is None:
        return (B, A)  # not an artefact the driver covers — the static gate keeps it
    if err:
        B.append("requiredAria [driven]: " + err)
        return (B, A)
    worst = None
    for combo in sorted(entry.get("combos") or {}):
        aria = (entry["combos"][combo].get("aria") or {})
        if not aria.get("required"):
            B.append("requiredAria [driven]: the receipt for %s records no requiredAria measurement "
                     "in %s, but the manifest declares %d string(s). Re-drive: %s"
                     % (key, combo, len(need), DRIVE_CMD))
            return (B, A)
        missing = [n for n in need if n not in (aria.get("present") or [])]
        if missing and (worst is None or len(missing) > len(worst[1])):
            worst = (combo, missing)
    if worst:
        B.append("requiredAria [driven]: %d of %d declared ARIA string(s) are MISSING FROM THE "
                 "RENDERED DOM in %s — %s. They may still be present in the file as JS string "
                 "literals; a gate that reads source text cannot tell. Source: %s"
                 % (len(worst[1]), len(need), worst[0], ", ".join(worst[1]), where))
    else:
        A.append("requiredAria [driven]: PASSED — all %d declared string(s) present in the RENDERED "
                 "DOM across %d theme x mode combos. Source: %s"
                 % (len(need), len(entry.get("combos") or {}), where))
    return (B, A)


# ---------------- the static-or-driven MATRIX (the #261 D3 receipt) ----------------
# Every (artefact, figure, rule) the gate visited, tagged with the route that answered it. A rule
# that answered "n-a" says so because the dtype does not owe it; a rule that answered nothing at
# all would show up as a missing row, which is the whole point of printing it.
ROUTES = []
MATRIX_RULES = ("dv-004", "dv-009", "dv-016", "dv-017", "dv-line-011", "requiredAria")


def route(artefact, figure, rule, how):
    ROUTES.append((os.path.basename(artefact or "?"), figure or "?", rule, how))


# ---------------- colour maths (lifted from _review/_gen_series_renders.py — one source) ----------------
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexs):
    h = hexs.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    a, b = max(a, b), min(a, b)
    return (a + 0.05) / (b + 0.05)

def _hex_to_hsl(hexs):
    h = hexs.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hdeg = ((g - b) / d + (6 if g < b else 0)) * 60
    elif mx == g:
        hdeg = ((b - r) / d + 2) * 60
    else:
        hdeg = ((r - g) / d + 4) * 60
    return hdeg % 360, s, l

def _hue_sep(a, b):
    ha, hb = _hex_to_hsl(a)[0], _hex_to_hsl(b)[0]
    d = abs(ha - hb) % 360
    return min(d, 360 - d)

def vibration(a, b):
    """The shimmer needs ALL THREE legs: near-equal VALUE + near-complementary HUES + both SATURATED.
    Thresholds (advisory, tunable): value-ratio<1.25 · hue-sep>=135° · min sat>=0.5. Hue leg 135° not
    150° because Dave observed the dance on the D2 dark red/green pair (146°)."""
    lr = ratio(a, b)
    hs = _hue_sep(a, b)
    smin = min(_hex_to_hsl(a)[1], _hex_to_hsl(b)[1])
    legs = sum([lr < 1.25, hs >= 135, smin >= 0.5])
    level = "HIGH" if legs == 3 else ("moderate" if legs == 2 else "low")
    return {"lum_ratio": lr, "hue_sep": hs, "sat_min": smin, "legs": legs, "level": level}

# ---------------- token / theme resolution ----------------
HEX_RE = re.compile(r'#[0-9A-Fa-f]{3,8}\b')

def theme_vars(css, theme):
    """Return {var-name: hex} for one [data-theme="…"] block (the sanctioned colour-definition zone)."""
    m = re.search(r'\[data-theme="%s"\]\s*\{(.*?)\}' % theme, css, re.S)
    out = {}
    if not m:
        return out
    for name, val in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', m.group(1)):
        hx = HEX_RE.search(val)
        if hx:
            out[name.strip()] = hx.group(0)
    return out

def resolve(varexpr, vars_):
    """var(--x) or var(--x, fallback) -> hex, using a theme's var map. None if unresolved/not a colour."""
    if not varexpr:
        return None
    m = re.match(r'var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)', varexpr.strip())
    if not m:
        hx = HEX_RE.fullmatch(varexpr.strip())
        return hx.group(0) if hx else None
    name, fb = m.group(1), m.group(2)
    if name in vars_:
        return vars_[name]
    if fb:
        return resolve(fb.strip(), vars_)
    return None

# ---------------- chart extraction ----------------
def find_charts(html):
    """Return list of (attrs_dict, inner_html) for each <figure class="… dv …" data-dv-type=…>."""
    charts = []
    for m in re.finditer(r'<figure\b([^>]*\bclass="[^"]*\bdv\b[^"]*"[^>]*)>', html):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        if "data-dv-type" not in attrs:
            continue
        # balanced-ish: take until the matching-depth </figure>
        start = m.end()
        depth = 1
        i = start
        for fm in re.finditer(r'<(/?)figure\b', html[start:]):
            depth += -1 if fm.group(1) else 1
            if depth == 0:
                i = start + fm.start()
                break
        charts.append((attrs, html[start:i]))
    return charts

def table_values(inner):
    """Numeric values from the chart's real <table> (first numeric cell per data row)."""
    tm = re.search(r'<table\b.*?</table>', inner, re.S)
    if not tm:
        return None
    vals = []
    for row in re.findall(r'<tr\b.*?</tr>', tm.group(0), re.S):
        if re.search(r'<th\b', row) and not re.search(r'<td\b', row):
            continue  # header row
        nums = re.findall(r'<td[^>]*>\s*([-+]?[\d,]*\.?\d+)', row)
        if nums:
            vals.append(float(nums[0].replace(",", "")))
    return vals or None

def series_fill_vars(inner):
    """The var() expressions used as fills on series elements (class contains dv-series)."""
    out = []
    for el in re.findall(r'<(?:rect|path|circle|polygon|polyline|g)\b[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner):
        fm = re.search(r'fill="([^"]+)"', el) or re.search(r'style="[^"]*fill:\s*([^;"]+)', el)
        if fm:
            out.append(fm.group(1).strip())
    return out

# ---------------- per-chart checks ----------------
def check_chart(attrs, inner, themes, ctx, fileinfo=None):
    """Return (blocking[list], advisory[list]). ctx = per-file journey map (mutated)."""
    B, A = [], []
    raw_dtype = attrs["data-dv-type"]
    dtype = DTYPE_CANON.get(raw_dtype, raw_dtype)
    if dtype not in KNOWN_DTYPES:
        B.append("dv-vocab: data-dv-type=\"%s\" is unknown to this gate — EVERY dtype-keyed rule "
                 "(dv-004, dv-bar-009, dv-bar-007, dv-pie-009/010, dv-line-011) would skip this "
                 "figure in silence. Add it to KNOWN_DTYPES, or to DTYPE_CANON if it is a synonym, "
                 "before shipping the figure." % raw_dtype)
    surface_key = "--raised" if attrs.get("data-surface") == "raised" else "--page"
    svg = "\n".join(re.findall(r'<svg\b.*?</svg>', inner, re.S))

    # #261 D3 — is THIS figure drawn at runtime? Decided once, used by every rule below, so the
    # static and driven arms can never disagree about which artefact they are grading.
    fi = fileinfo or {}
    _fig_i = ctx.get("_fig_i", 0)
    ctx["_fig_i"] = _fig_i + 1
    _fig_id = attrs.get("id") or ""
    _all_segs = re.findall(r'<(?:path|rect|circle|polyline|polygon|g)\b[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner)
    engine = is_engine_drawn(_all_segs, fi.get("html"))
    _art = fi.get("path") or "?"
    _tag = _fig_id or ("fig-%d" % _fig_i)

    # --- DV-D02-A dv-fit scope ---------------------------------------------
    # Bites BOTH ways: a cartesian plot MISSING dv-fit, and an excluded plot CARRYING it.
    # The second direction matters — #27 proved a manifest bites hardest where the author
    # predicted it would pass, and "someone added fit to the donut" is exactly that shape.
    plot_tags = [t for t in re.findall(r'<svg\b[^>]*>', inner)
                 if re.search(r'\bclass="[^"]*\bdv-svg\b', t)]
    if plot_tags:
        with_fit = [t for t in plot_tags if re.search(r'\bclass="[^"]*\bdv-fit\b', t)]
        if dtype in CARTESIAN_DTYPES:
            if len(with_fit) < len(plot_tags):
                msg = ('DV-D02-A: data-dv-type="%s" is a cartesian plot, so DV-D02 covers it — its '
                       'plot <svg class="dv-svg"> must also carry dv-fit (%d of %d do). Responsive '
                       '= compress width, never scale proportionally.'
                       % (raw_dtype, len(with_fit), len(plot_tags)))
                if dtype in DV_FIT_WAIVED:
                    A.append(msg + " WAIVED: " + DV_FIT_WAIVED[dtype])
                else:
                    B.append(msg)
        else:
            if with_fit:
                B.append('DV-D02-A: data-dv-type="%s" carries dv-fit but is OUT of DV-D02 scope — %s'
                         % (raw_dtype, NON_CARTESIAN_DTYPES[dtype]))

    # --- dv-009 flat fills -------------------------------------------------
    for grad in ("linearGradient", "radialGradient", "filter"):
        if re.search(r'<%s\b' % grad, svg):
            B.append("dv-009: <%s> in chart SVG — fills must be flat (no gradient/3D/shadow)." % grad)
    pats = re.findall(r'<pattern\b[^>]*id="([^"]*)"', svg)
    if len(pats) > 1:
        B.append("dv-009: %d <pattern>s — at most ONE (chevron) per chart." % len(pats))
    for pid in pats:
        if "chevron" not in pid.lower():
            B.append("dv-009: <pattern id=\"%s\"> — the one permitted pattern must be the chevron." % pid)

    # --- dv-017 palette-only fills (0 rogue hex on series elements) ---------
    fills = series_fill_vars(inner)
    for f in fills:
        if HEX_RE.fullmatch(f) or (HEX_RE.search(f) and "var(" not in f):
            B.append("dv-017: series fill `%s` is a raw hex — must resolve to a data/* or building-block token." % f)
        elif f not in ("none", "currentColor") and not (f.startswith("var(") or f.startswith("url(")):
            B.append("dv-017: series fill `%s` is not a token/url — palette-only." % f)

    # --- dv-016 >=3:1 RENDERED contrast (series fills + axis/label), per mode ---
    #     computed from the RESOLVED token value against the surface — not an author-declared pair.
    axis_exprs = []
    for el in re.findall(r'<(?:line|path|polyline|text|g)\b[^>]*class="[^"]*dv-(?:axis|label|baseline)[^"]*"[^>]*>', inner):
        sm = re.search(r'(?:stroke|fill)="([^"]+)"', el)
        if sm:
            axis_exprs.append(sm.group(1).strip())
    grid_exprs = []
    for el in re.findall(r'<(?:line|path|polyline)\b[^>]*class="[^"]*dv-grid[^"]*"[^>]*>', inner):
        sm = re.search(r'stroke="([^"]+)"', el)
        if sm:
            grid_exprs.append(sm.group(1).strip())
    for theme in ("light", "dark"):
        vars_ = themes[theme]
        surf = vars_.get(surface_key)
        if not surf:
            continue
        for label, exprs, block in (("series", fills, True), ("axis/label", axis_exprs, True), ("gridline", grid_exprs, False)):
            for expr in exprs:
                hexv = resolve(expr, vars_)
                if not hexv or expr in ("none", "currentColor"):
                    continue
                r = ratio(hexv, surf)
                if r < 3.0:
                    msg = "dv-016 [%s]: %s=%s vs surface %s = %.2f:1 (<3:1) in %s mode." % (label, expr, hexv, surf, r, theme)
                    (B if block else A).append(msg)

    # --- dv-004 >=2px separation on gapless surfaces (donut/pie/stacked) ----
    #     The RULE is mechanism-NEUTRAL: "minimum 2px separation between colour blocks".
    #     This gate used to demand a surface-coloured stroke and nothing else — so a chart that
    #     satisfied dv-004 with real geometry would have FAILED it, and the one available
    #     mechanism is the one that reads as correct on plain page and lies over gridlines.
    #     Dave ruled the geometry route for stacked columns on 2026-07-27; both mechanisms now
    #     pass, and an unmeasurable chart still has to carry the stroke.
    _dv004_route = "n-a"
    if dtype in ("donut", "pie", "stacked"):
        segs = re.findall(r'<(?:path|rect|circle)\b[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner)
        stroke_ok = bool(segs) and all(_seg_has_surface_stroke(s) for s in segs)
        gap_ok, gap_note = _rect_stack_gap(segs) if dtype == "stacked" else (None, "not a rect stack")
        _dv004_route = "driven" if is_engine_drawn(segs, fi.get("html")) else "static"
        if is_engine_drawn(segs, fi.get("html")):
            # s260-D3 — the chart does not exist in the markup; a COMMITTED driven receipt is the
            # evidence. Never a skip: every failure path below is BLOCKING and names the remedy.
            # prefer THIS figure's own record (#261 D3); fall back to the dtype-scoped test-page
            # arm for any artefact the driver does not drive directly.
            ok, msg = driven_dv004_figure(fi.get("path"), raw_dtype, _fig_id, _fig_i,
                                          receipts_path=fi.get("receipts"), root=fi.get("root"))
            if ok is None:
                ok, msg = driven_dv004(fi.get("path"), dtype, raw_dtype,
                                       receipts_path=fi.get("receipts"), root=fi.get("root"))
            (A if ok else B).append(msg)
        elif not stroke_ok and gap_ok is not True:
            if gap_ok is False:
                B.append("dv-004: %s — %s, and no >=2px surface-coloured separating stroke."
                         % (raw_dtype, gap_note))
            else:
                B.append("dv-004: %s segment lacks a >=2px surface-coloured separating stroke "
                         "(geometry not statically measurable here: %s)." % (raw_dtype, gap_note))
    else:
        # s260-D3, the second half — a dv-004 figure the driver RECORDED for this page is graded
        # even though the dtype is outside the gapless-surface set. Silent (None) unless a real
        # measured number exists; it can never invent a rule the receipts do not measure.
        segs = re.findall(r'<(?:path|rect|circle)\b[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner)
        if is_engine_drawn(segs, fi.get("html")):
            ok, msg = driven_dv004_figure(fi.get("path"), raw_dtype, _fig_id, _fig_i,
                                          receipts_path=fi.get("receipts"), root=fi.get("root"))
            if ok is None:
                ok, msg = driven_dv004_recorded(fi.get("path"), raw_dtype,
                                                receipts_path=fi.get("receipts"), root=fi.get("root"))
            if ok is True:
                A.append(msg)
                _dv004_route = "driven"
            elif ok is False:
                B.append(msg)
                _dv004_route = "driven"

    # --- #261 D3: the SIBLINGS on an engine canvas -------------------------
    #     dv-009 / dv-017 / dv-016 / dv-line-011 above all iterate `class="dv-series"` elements
    #     pulled out of the MARKUP. When the engine draws, that list is empty and all four pass
    #     vacuously — proved, not assumed, by _tests/chart-engine/_probe_fail_open.py (0/6 bit).
    #     Same route as dv-004: static OR driven, never skipped.
    if engine:
        sb, sa = driven_siblings(fi.get("path"), dtype, raw_dtype, _fig_id, _fig_i,
                                 receipts_path=fi.get("receipts"), root=fi.get("root"))
        B.extend(sb)
        A.extend(sa)
    for _rule in ("dv-009", "dv-016", "dv-017"):
        route(_art, _tag, _rule, "driven" if engine else "static")
    route(_art, _tag, "dv-line-011", ("driven" if engine else "static") if dtype in _LINEISH else "n-a")
    route(_art, _tag, "dv-004", _dv004_route)

    # --- dv-bar-009 zero baseline (bar-family ONLY; never fires on lines) ---
    if dtype in BAR_FAMILY:
        if attrs.get("data-domain-min") != "0":
            B.append("dv-bar-009: bar-family chart must declare data-domain-min=\"0\" (zero baseline).")

    # --- dv-bar-007 negatives vertical only --------------------------------
    if dtype == "bar":  # horizontal
        vals = table_values(inner) or []
        if any(v < 0 for v in vals):
            B.append("dv-bar-007: horizontal bar has a negative value — negatives are for vertical columns only.")

    # --- dv-pie-009 <=6 slices · dv-pie-010 sum=total ----------------------
    if dtype in ("donut", "pie"):
        vals = table_values(inner) or []
        if len(vals) > 6:
            B.append("dv-pie-009: %d slices — donut/pie capped at 6." % len(vals))
        if "data-total" in attrs and vals:
            declared = float(attrs["data-total"].replace(",", ""))
            if abs(sum(vals) - declared) > max(1.0, 0.005 * declared):
                B.append("dv-pie-010: slice sum %.2f != displayed total %.2f." % (sum(vals), declared))

    # --- dv-line-011 straight lines (no curve commands) --------------------
    if dtype in ("line", "multiline", "spark", "column", "bar", "grouped", "stacked", "kpi", "combo"):
        for path in re.findall(r'<path\b[^>]*class="[^"]*dv-series[^"]*"[^>]*\bd="([^"]+)"', inner):
            if CURVE_CMDS.search(path):
                B.append("dv-line-011: series <path> has a curve command (C/S/Q/T) — series lines must be straight.")
                break
        for poly in re.findall(r'<polyline\b[^>]*class="[^"]*dv-series[^"]*"[^>]*points="([^"]+)"', inner):
            pass  # polylines are inherently straight — presence is fine

    # ===== ADVISORY =====
    # dv-005 tabular alternative
    if not re.search(r'<table\b', inner):
        A.append("dv-005: no real <table> in the chart (a11y spine + tabular alternative).")
    # §04.3 letters when series>=2 — count DISTINCT series (by group id, else by distinct fill token),
    # NOT distinct elements (a single-series column has many bars sharing one fill = ONE series).
    groups = set(re.findall(r'data-series-group="(\d+)"', inner))
    distinct_fills = set(f for f in fills if f.startswith("var("))
    n_series = len(groups) if groups else len(distinct_fills)
    legend_keys = re.findall(r'class="[^"]*dv-key[^"]*"[^>]*>\s*([A-Z])', inner)
    # direct labelling is an ALTERNATIVE colour-independent channel to letters+legend (Dave review #5)
    direct_labelled = attrs.get("data-labelling") == "direct" or "dv-direct" in inner
    if n_series >= 2 and len(legend_keys) < 2 and not direct_labelled:
        A.append("§04.3 letters: %d series but <2 legend letter-keys and not directly labelled (colour must never be the only channel)." % n_series)
    # dv-line-009 spark aspect
    if dtype == "spark":
        vb = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', svg)
        if vb and float(vb.group(2)) > 0 and float(vb.group(1)) / float(vb.group(2)) < 2.5:
            A.append("dv-line-009: spark aspect %.1f:1 is tall for an in-line sparkline (expect wide/flat)." % (float(vb.group(1)) / float(vb.group(2))))
    # dv-014 journey consistency (per-file view scope)
    for el in re.findall(r'<[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner):
        im = re.search(r'data-series-i="(\d+)"', el)
        fm = re.search(r'fill="(var\(--data-[^)]+\))"', el)
        if im and fm:
            ctx.setdefault(im.group(1), set()).add(fm.group(1))
    # vibration — adjacent series-fill pairs (resolve in light mode; series C is mode-stable)
    resolved = [resolve(f, themes["light"]) for f in fills]
    resolved = [h for h in resolved if h]
    for i in range(len(resolved) - 1):
        v = vibration(resolved[i], resolved[i + 1])
        if v["level"] == "HIGH":
            A.append("vibration: adjacent fills %s↔%s shimmer (%.2f:1, %.0f°, sat %.2f) — value-split or gap them."
                     % (resolved[i], resolved[i + 1], v["lum_ratio"], v["hue_sep"], v["sat_min"]))
    return B, A

# ---------------- file driver ----------------
def check_file(path):
    html = open(path).read()
    m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S)
    css = m.group(1) if m else ""
    themes = {"light": theme_vars(css, "light"), "dark": theme_vars(css, "dark")}
    charts = find_charts(html)
    ctx = {}
    results = []
    fileinfo = {"path": path, "html": html}
    for attrs, inner in charts:
        B, A = check_chart(attrs, inner, themes, ctx, fileinfo)
        results.append((attrs.get("data-dv-type", "?"), attrs.get("id", ""), B, A))
    # #261 D3 — requiredAria against the RENDERED DOM, once per file (the manifest is per file).
    # Attached to the first chart so it lands in the blocking channel; a file-level advisory list
    # cannot red, and this rule has to be able to.
    if results:
        ab, aa = driven_aria(path, html)
        if ab or aa:
            results[0][2].extend(ab)
            results[0][3].extend(aa)
            route(path, "file", "requiredAria", "driven")
        elif required_aria_of(html):
            route(path, "file", "requiredAria", "static")
        else:
            route(path, "file", "requiredAria", "n-a")
    # journey-consistency advisory (a series index mapped to >1 fill across the view)
    file_adv = []
    for idx, fillset in ctx.items():
        if str(idx).startswith("_"):
            continue  # #261 D3 bookkeeping (the figure counter), not a series index
        if len(fillset) > 1:
            file_adv.append("dv-014: series index %s bound to multiple fills across the view: %s" % (idx, sorted(fillset)))
    return results, file_adv

def discover():
    # _proforma review surfaces carry the APOLLO-DATAVIZ signature; canon chart SNIPPETS are
    # discovered by filename (wave-2 conductor, 2026-07-22 — the new-surface rule: worker D's
    # Chart-* snippets verified by gate-import pre-wiring, this glob makes it standing).
    proforma = (f for f in glob.glob(os.path.join(PROFORMA_DIR, "*.html")) if SIGNATURE in open(f).read())
    snippets = glob.glob(os.path.join(HERE, "snippets", "Chart-*.reference.html"))
    return sorted(set(proforma) | set(snippets))

def main():
    files = discover()
    lines = ["# DataViz gate — report", "",
             "Charts = semantic SVG + tokens + CSS motion + real-table spine. Blocking + advisory per dossier §06.",
             "Gridline contrast is advisory (decorative, WCAG 1.4.11-exempt); series-fill + axis/label contrast is blocking.", ""]
    any_fail = False
    if not files:
        lines.append("No DataViz surfaces found (no `%s` signature). PASS." % SIGNATURE)
        open(os.path.join(HERE, "_DATAVIZ-GATE.md"), "w").write("\n".join(lines) + "\n")
        print("DataViz gate: no chart surfaces yet — PASS")
        return 0
    for path in files:
        name = os.path.relpath(path, HERE)
        results, file_adv = check_file(path)
        nb = sum(len(B) for _, _, B, _ in results)
        na = sum(len(A) for _, _, _, A in results) + len(file_adv)
        if nb:
            any_fail = True
        print("  [%s] %s  (%d charts, %d blocking, %d advisory)" % ("FAIL" if nb else "PASS", name, len(results), nb, na))
        lines.append("## %s %s — %s" % ("✗" if nb else "✓", name, "FAIL" if nb else "PASS"))
        for dtype, cid, B, A in results:
            tag = ("%s#%s" % (dtype, cid)) if cid else dtype
            for b in B:
                print("     ✗", b)
                lines.append("- ✗ **%s** — %s" % (tag, b))
            for a in A:
                lines.append("- ⚠ %s — %s" % (tag, a))
        for a in file_adv:
            lines.append("- ⚠ %s" % a)
        lines.append("")
    lines += ["---", "Method: `_proforma/_DATAVIZ-METHOD.md`. Dossier: `reviews/DATAVIZ-METHOD-2026-07-16.html` §06.",
              "Advisory checks promote to blocking after a bite-test (ADR-0005 §5): `python3 knowledge/_validate_dataviz.py --selftest`."]
    open(os.path.join(HERE, "_DATAVIZ-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ DataViz gate FAILED — see knowledge/_DATAVIZ-GATE.md")
        return 1
    print("\n✅ DataViz gate passed (%d chart surface file(s))." % len(files))
    return 0

# ---------------- bite-test (a deliberately broken chart MUST fail) ----------------
def selftest():
    THEME = ('<style>[data-theme="light"]{--page:#FFFFFF;--raised:#F3F3F3;--data-series-1:#766682;'
             '--data-series-2:#A45C3A;--dv-axis:#545454;--dv-grid:#EDEDED;--bad:#FFF9C4;}'
             '[data-theme="dark"]{--page:#000000;--raised:#1D1D1D;--data-series-1:#766682;'
             '--data-series-2:#A45C3A;--dv-axis:#9B9B9B;--dv-grid:#3A3A3A;--bad:#222200;}</style>')
    def run(fig, fileinfo=None):
        html = "APOLLO-DATAVIZ" + THEME + fig
        m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S)
        themes = {"light": theme_vars(m.group(1), "light"), "dark": theme_vars(m.group(1), "dark")}
        (attrs, inner) = find_charts(html)[0]
        return check_chart(attrs, inner, themes, {}, fileinfo)
    def has(msgs, tok):
        return any(tok in m for m in msgs)

    GOOD_BAR = ('<figure class="dv" data-dv-type="column" data-domain-min="0">'
                '<svg class="dv-svg dv-fit" viewBox="0 0 100 60"><line class="dv-axis" stroke="var(--dv-axis)" x1="0" y1="60" x2="100" y2="60"/>'
                '<rect class="dv-series" data-series-i="1" fill="var(--data-series-1)" x="0" y="10" width="20" height="50"/></svg>'
                '<table><tr><th>A</th><td>50</td></tr></table>'
                '<ul class="dv-legend"><li><span class="dv-key">A</span> Savings</li></ul></figure>')
    cases = []
    # each: (name, fixture, checker predicate on (B,A))
    cases.append(("GOOD column passes blocking", GOOD_BAR, lambda B, A: len(B) == 0))
    cases.append(("dv-009 gradient", GOOD_BAR.replace("<svg class=\"dv-svg dv-fit\" viewBox=\"0 0 100 60\">",
                  "<svg class=\"dv-svg dv-fit\" viewBox=\"0 0 100 60\"><linearGradient id=\"g\"/>"),
                  lambda B, A: has(B, "dv-009")))

    # --- DV-D02-A dv-fit scope (ruled 2026-07-28 #28) -----------------------
    # Five bites: the two directions, the waiver, the control that must NOT fire, and the
    # partition-totality guard. GOOD_BAR now carries dv-fit — that IS the green control, and it is
    # why "GOOD column passes blocking" above proves the check can stay silent on a compliant chart.
    cases.append(("★ DV-D02-A fires when a cartesian plot LOSES dv-fit",
                  GOOD_BAR.replace('class="dv-svg dv-fit"', 'class="dv-svg"'),
                  lambda B, A: has(B, "DV-D02-A")))
    cases.append(("★ DV-D02-A fires the OTHER way — an excluded donut that CARRIES dv-fit",
                  '<figure class="dv" data-dv-type="donut" data-total="30">'
                  '<svg class="dv-svg dv-fit"><path class="dv-series" fill="var(--data-series-1)" '
                  'stroke="var(--page)" stroke-width="2" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>30</td></tr></table></figure>',
                  lambda B, A: has(B, "DV-D02-A")))
    cases.append(("DV-D02-A silent on an excluded chart with no dv-fit (donut, the normal case)",
                  '<figure class="dv" data-dv-type="donut" data-total="30">'
                  '<svg class="dv-svg"><path class="dv-series" fill="var(--data-series-1)" '
                  'stroke="var(--page)" stroke-width="2" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>30</td></tr></table></figure>',
                  lambda B, A: not has(B, "DV-D02-A")))
    # ★ REPLACED #72. This case previously asserted "the WAIVER demotes scatter to advisory, and
    # names ds-020". That waiver was discharged at #72 (see the provenance in DV_FIT_WAIVED), so
    # the old assertion would now be testing a mechanism that no longer exists. It is replaced by
    # the pair below rather than deleted, because the discharge is exactly the thing a regression
    # would undo quietly: scatter must now go BLOCKING like every other cartesian member, and must
    # still fall silent when compliant. One case per direction — a check that only fires one way
    # cannot tell a fix from a break.
    cases.append(("★ scatter is BLOCKING since the #72 discharge — no waiver left to demote it",
                  '<figure class="dv" data-dv-type="scatter"><svg class="dv-svg">'
                  '<circle class="dv-series" fill="var(--data-series-1)" cx="5" cy="5" r="3"/></svg>'
                  '<table><tr><th>A</th><td>5</td></tr></table></figure>',
                  lambda B, A: has(B, "DV-D02-A") and not has(A, "DV-D02-A")))
    cases.append(("★ scatter WITH dv-fit is silent — the green control for the discharge",
                  '<figure class="dv" data-dv-type="scatter"><svg class="dv-svg dv-fit">'
                  '<circle class="dv-series" fill="var(--data-series-1)" cx="5" cy="5" r="3"/></svg>'
                  '<table><tr><th>A</th><td>5</td></tr></table></figure>',
                  lambda B, A: not has(B, "DV-D02-A") and not has(A, "DV-D02-A")))
    cases.append(("★ h-bar is IN scope after DV-D02-A — the rot the amendment corrected",
                  '<figure class="dv" data-dv-type="bar" data-domain-min="0">'
                  '<svg class="dv-svg"><rect class="dv-series" fill="var(--data-series-1)" '
                  'x="0" y="10" width="20" height="50"/></svg>'
                  '<table><tr><th>A</th><td>50</td></tr></table></figure>',
                  lambda B, A: has(B, "DV-D02-A")))
    cases.append(("dv-009 two patterns", GOOD_BAR.replace("<rect class=\"dv-series\"",
                  "<pattern id=\"chevron\"/><pattern id=\"chevron2\"/><rect class=\"dv-series\""),
                  lambda B, A: has(B, "dv-009")))
    cases.append(("dv-017 raw hex fill", GOOD_BAR.replace('fill="var(--data-series-1)"', 'fill="#A45C3A"'),
                  lambda B, A: has(B, "dv-017")))
    cases.append(("dv-016 low-contrast series", GOOD_BAR.replace('fill="var(--data-series-1)"', 'fill="var(--bad)"'),
                  lambda B, A: has(B, "dv-016")))
    cases.append(("dv-bar-009 missing baseline",
                  '<figure class="dv" data-dv-type="column">' + GOOD_BAR.split(">", 1)[1],
                  lambda B, A: has(B, "dv-bar-009")))
    cases.append(("dv-bar-009 NEVER fires on a line",
                  '<figure class="dv" data-dv-type="line"><svg class="dv-svg" viewBox="0 0 100 60">'
                  '<polyline class="dv-series" points="0,60 50,10" stroke="var(--data-series-1)"/></svg>'
                  '<table><tr><th>A</th><td>1</td></tr></table></figure>',
                  lambda B, A: not has(B, "dv-bar-009")))
    cases.append(("dv-bar-007 negative horizontal bar",
                  '<figure class="dv" data-dv-type="bar" data-domain-min="0"><svg class="dv-svg" viewBox="0 0 100 60">'
                  '<rect class="dv-series" fill="var(--data-series-1)"/></svg>'
                  '<table><tr><th>A</th><td>-5</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-bar-007")))
    cases.append(("dv-pie-009 >6 slices",
                  '<figure class="dv" data-dv-type="donut"><svg class="dv-svg"></svg><table>'
                  + "".join('<tr><th>%d</th><td>10</td></tr>' % i for i in range(7)) + '</table></figure>',
                  lambda B, A: has(B, "dv-pie-009")))
    cases.append(("dv-pie-010 sum!=total",
                  '<figure class="dv" data-dv-type="donut" data-total="100"><svg class="dv-svg">'
                  '<path class="dv-series" stroke="var(--page)" stroke-width="2" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>20</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-pie-010")))
    cases.append(("dv-004 donut without separating stroke",
                  '<figure class="dv" data-dv-type="donut" data-total="30"><svg class="dv-svg">'
                  '<path class="dv-series" fill="var(--data-series-1)" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>30</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-004")))

    # ---- ds-014 / ADR-0016 bites (2026-07-27) ------------------------------------------
    # These exist because dv-004 shipped GREEN on a stacked column with 0.0px separation for
    # weeks. The branch tested `stacked`; the figure said `stacked-column`; the gate never
    # looked. Bite 1 IS that exact figure — it must fail. A gate you cannot prove will fail is
    # a CLAIMED gate, and CLAIMED is where ds-013 lived.
    def _stack(gap_px, dtype="stacked-column", stroke=""):
        """Two-segment stacked column, baseline y=60. Upper segment's bottom is `gap_px` above
        the lower segment's top, so the gap is exact and declared by the caller."""
        return ('<figure class="dv" data-dv-type="%s" data-domain-min="0">'
                '<svg class="dv-svg" viewBox="0 0 100 60">'
                '<rect class="dv-series" fill="var(--data-series-1)"%s x="10" y="30" width="20" height="30"/>'
                '<rect class="dv-series" fill="var(--data-series-2)"%s x="10" y="%s" width="20" height="20"/>'
                '</svg><table><tr><th>A</th><td>30</td></tr><tr><th>B</th><td>20</td></tr></table></figure>'
                % (dtype, stroke, stroke, 10 - gap_px))

    cases.append(("★ dv-004 FIRES on the ds-014 figure — stacked-column, 0.0px gap, no stroke",
                  _stack(0.0), lambda B, A: has(B, "dv-004")))
    cases.append(("★ dv-004 PASSES on 2px of REAL GEOMETRY (Dave's ruling, no stroke needed)",
                  _stack(2.0), lambda B, A: not has(B, "dv-004")))
    cases.append(("dv-004 boundary — 1.9px gap is still a failure",
                  _stack(1.9), lambda B, A: has(B, "dv-004")))
    cases.append(("dv-004 accepts MORE than the minimum (6px gap)",
                  _stack(6.0), lambda B, A: not has(B, "dv-004")))
    cases.append(("dv-004 stroke mechanism still passes with a 0px gap",
                  _stack(0.0, stroke=' stroke="var(--page)" stroke-width="2"'),
                  lambda B, A: not has(B, "dv-004")))
    cases.append(("dv-004 unmeasurable geometry fails SAFE (no x/y/height, no stroke)",
                  '<figure class="dv" data-dv-type="stacked-column" data-domain-min="0">'
                  '<svg class="dv-svg"><path class="dv-series" fill="var(--data-series-1)" d="M0 0"/>'
                  '<path class="dv-series" fill="var(--data-series-2)" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>30</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-004")))
    cases.append(("★ dv-vocab FIRES on a dtype the gate has never heard of",
                  _stack(2.0, dtype="sunburst"), lambda B, A: has(B, "dv-vocab")))
    cases.append(("dv-vocab silent on the three values that were blind (scatter)",
                  '<figure class="dv" data-dv-type="scatter"><svg class="dv-svg">'
                  '<circle class="dv-series" fill="var(--data-series-1)" cx="5" cy="5" r="3"/></svg>'
                  '<table><tr><th>A</th><td>5</td></tr></table></figure>',
                  lambda B, A: not has(B, "dv-vocab")))
    cases.append(("dtype synonym normalises — grouped-column reaches dv-bar-009",
                  '<figure class="dv" data-dv-type="grouped-column"><svg class="dv-svg">'
                  '<rect class="dv-series" fill="var(--data-series-1)" x="0" y="10" width="20" height="50"/>'
                  '</svg><table><tr><th>A</th><td>50</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-bar-009") and not has(B, "dv-vocab")))
    cases.append(("dv-line-011 curved series path",
                  '<figure class="dv" data-dv-type="line"><svg class="dv-svg">'
                  '<path class="dv-series" stroke="var(--data-series-1)" d="M0 0 C10 10 20 0 30 0"/></svg>'
                  '<table><tr><th>A</th><td>1</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-line-011")))
    cases.append(("vibration advisory fires on a shimmer pair",
                  '<figure class="dv" data-dv-type="donut" data-total="20"><svg class="dv-svg">'
                  '<path class="dv-series" fill="var(--data-series-1)" stroke="var(--page)" stroke-width="2" d="M0 0"/>'
                  '<path class="dv-series" fill="var(--vib)" stroke="var(--page)" stroke-width="2" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>10</td></tr></table></figure>'.replace(
                      "var(--vib)", "var(--data-series-2)"),
                  lambda B, A: True))  # exercised; level depends on the pair — just ensure no crash

    # ---- s260-D3 · DRIVEN RECEIPTS for dv-004 on an ENGINE-DRAWN chart --------------------
    # Five bites, each one a different way the route must NOT quietly pass:
    #   missing receipt · stale source hash · one combo below 2px · fresh-and-green ·
    #   and the CONTROL — a static donut that still carries its stroke keeps the static route.
    # The fixtures are built on a throwaway tree, so the bite-test touches no repo file.
    import tempfile as _tf
    _tmp = _tf.mkdtemp(prefix="dv004-bite-")

    ENGINE_DONUT = ('<figure class="dv" data-dv-type="donut" data-total="30">'
                    '<svg class="dv-svg" viewBox="0 0 300 260"></svg>'
                    '<table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>20</td></tr></table></figure>')
    STATIC_DONUT = ('<figure class="dv" data-dv-type="donut" data-total="30">'
                    '<svg class="dv-svg" viewBox="0 0 300 260">'
                    '<path class="dv-series" fill="var(--data-series-1)" stroke="var(--page)" stroke-width="2" d="M0 0"/>'
                    '<path class="dv-series" fill="var(--data-series-2)" stroke="var(--page)" stroke-width="2" d="M0 0"/>'
                    '</svg><table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>20</td></tr></table></figure>')
    ENGINE_HTML = "APOLLO-DATAVIZ dvRender(fig, DATA) <script src=\"../canon/dv-render.js\"></script>"

    def _bite_tree(tag, px_by_combo, source_text="engine v1"):
        """Build a throwaway root + receipts file; returns a fileinfo dict."""
        root = os.path.join(_tmp, tag)
        os.makedirs(os.path.join(root, "canon"), exist_ok=True)
        src = os.path.join(root, "canon", "dv-render-donut.js")
        open(src, "w").write(source_text)
        combos = {}
        for combo, px in px_by_combo.items():
            combos[combo] = {"pageerrors": 0, "console_errors": 0,
                             "figures": {"fig-donut": {"dtype": "donut", "marks": 5,
                                                       "table_rows": 5, "dv004_px": px,
                                                       "dv004_note": "bite fixture"}}}
        rec = {"chromium": "bite", "driven": "2026-09-08T00:00:00Z",
               "themes": ["mono", "legacy", "console", "supercharge"], "modes": ["light", "dark"],
               "pages": {"donut.html": {"sources": {"canon/dv-render-donut.js": _sha256(src)},
                                        "combos": combos}}}
        rpath = os.path.join(root, "_receipts.json")
        json.dump(rec, open(rpath, "w"), indent=1, sort_keys=True)
        return {"path": os.path.join(root, "Chart-donut.reference.html"), "html": ENGINE_HTML,
                "receipts": rpath, "root": root, "_src": src}

    ALL_GREEN = {"%s/%s" % (t, m): 2.109
                 for t in ("mono", "legacy", "console", "supercharge") for m in ("light", "dark")}

    fi_ok = _bite_tree("green", ALL_GREEN)
    cases.append(("★ s260-D3 driven receipt: fresh + all 8 combos >=2px PASSES (and says so)",
                  ENGINE_DONUT, lambda B, A: not has(B, "dv-004")
                  and has(A, "driven receipt") and has(A, "2.109px"), fi_ok))

    ONE_SHORT = dict(ALL_GREEN); ONE_SHORT["console/dark"] = 1.9
    fi_short = _bite_tree("short", ONE_SHORT)
    cases.append(("★ s260-D3 driven receipt: ONE combo at 1.9px is BLOCKING, quoting combo + px",
                  ENGINE_DONUT, lambda B, A: has(B, "dv-004") and has(B, "1.900px")
                  and has(B, "console/dark") and has(B, "driven receipt"), fi_short))

    fi_stale = _bite_tree("stale", ALL_GREEN)
    open(fi_stale["_src"], "w").write("engine v2 — edited after the drive")
    cases.append(("★ s260-D3 driven receipt: STALE source hash is BLOCKING and names the file",
                  ENGINE_DONUT, lambda B, A: has(B, "dv-004") and has(B, "STALE")
                  and has(B, "dv-render-donut.js") and has(B, "_drive_chart_engine.py"), fi_stale))

    fi_missing = {"path": os.path.join(_tmp, "Chart-donut.reference.html"), "html": ENGINE_HTML,
                  "receipts": os.path.join(_tmp, "nope.json"), "root": _tmp}
    cases.append(("★ s260-D3 driven receipt: NO receipt at all is BLOCKING, never a skip",
                  ENGINE_DONUT, lambda B, A: has(B, "dv-004") and has(B, "ENGINE-DRAWN")
                  and has(B, "_drive_chart_engine.py"), fi_missing))

    fi_unmapped = dict(fi_ok, path=os.path.join(_tmp, "green", "Chart-unmapped.reference.html"))
    cases.append(("★ s260-D3 driven receipt: an UNMAPPED engine snippet is BLOCKING",
                  ENGINE_DONUT, lambda B, A: has(B, "dv-004") and has(B, "not mapped"), fi_unmapped))

    cases.append(("★ s260-D3 control: a STATIC donut with a >=2px stroke still passes the STATIC route",
                  STATIC_DONUT, lambda B, A: not has(B, "dv-004")
                  and not has(A, "driven receipt") and not has(B, "driven receipt"), fi_ok))

    # ---- #260 · the ENGINE_TEST_PAGE mapping for the s259-D1 fast-follower types --------------
    # The mapping is DATA, so the bite is on the data: every engine-drawn member must resolve to
    # its own page, and no member may resolve to a page that is not on disk.
    _WANT_MAP = {"Chart-scatter.reference.html": "scatter.html",
                 "Chart-histogram.reference.html": "histogram.html",
                 "Chart-boxplot.reference.html": "boxplot.html",
                 "Chart-bullet.reference.html": "bullet.html",
                 "Chart-candlestick.reference.html": "candlestick.html",
                 "Chart-butterfly-h.reference.html": "butterfly-h.html",
                 "Chart-butterfly-v.reference.html": "butterfly-v.html",
                 "Chart-pie.reference.html": "donut.html"}
    _pages_dir = os.path.join(HERE, "_tests", "chart-engine")
    _map_ok = all(ENGINE_TEST_PAGE.get(k) == v for k, v in _WANT_MAP.items()) and \
        all(os.path.isfile(os.path.join(_pages_dir, p)) for p in set(ENGINE_TEST_PAGE.values()))
    print("  [%s] ★ #260 ENGINE_TEST_PAGE maps every engine-drawn member to a test page that EXISTS"
          % ("ok" if _map_ok else "XX"))
    if not _map_ok:
        missing = [p for p in sorted(set(ENGINE_TEST_PAGE.values()))
                   if not os.path.isfile(os.path.join(_pages_dir, p))]
        print("        want=%s missing_pages=%s" % (_WANT_MAP, missing))

    # ---- #260 · a RECORDED dv-004 figure is graded whatever the dtype (s260-D3, second half) ---
    def _bite_recorded(tag, px, dtype="butterfly-v", fid="fig-bfly"):
        root = os.path.join(_tmp, tag)
        os.makedirs(os.path.join(root, "canon"), exist_ok=True)
        src = os.path.join(root, "canon", "dv-render-butterfly.js")
        open(src, "w").write("engine v1")
        combos = {}
        for t in ("mono", "legacy", "console", "supercharge"):
            for m in ("light", "dark"):
                combos["%s/%s" % (t, m)] = {
                    "pageerrors": 0, "console_errors": 0,
                    "figures": {fid: {"dtype": dtype, "marks": 12, "table_rows": 6,
                                      "dv004_px": px, "dv004_note": "bite fixture"}}}
        rec = {"chromium": "bite", "driven": "2026-09-08T00:00:00Z",
               "themes": ["mono", "legacy", "console", "supercharge"], "modes": ["light", "dark"],
               "pages": {"butterfly-v.html": {"sources": {"canon/dv-render-butterfly.js": _sha256(src)},
                                              "combos": combos}}}
        rpath = os.path.join(root, "_receipts.json")
        json.dump(rec, open(rpath, "w"), indent=1, sort_keys=True)
        return {"path": os.path.join(root, "Chart-butterfly-v.reference.html"),
                "html": ENGINE_HTML, "receipts": rpath, "root": root, "_src": src}

    ENGINE_BFLY = ('<figure class="dv" data-dv-type="butterfly-v" data-domain-min="0">'
                   '<svg class="dv-svg" viewBox="0 0 300 260"></svg>'
                   '<table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>20</td></tr></table></figure>')
    cases.append(("★ #260 recorded dv-004 figure BELOW 2px is BLOCKING outside donut/pie/stacked",
                  ENGINE_BFLY, lambda B, A: has(B, "dv-004") and has(B, "1.500px")
                  and has(B, "whatever the dtype"), _bite_recorded("bfly-red", 1.5)))
    cases.append(("★ #260 recorded dv-004 figure at 2.200px PASSES and says so",
                  ENGINE_BFLY, lambda B, A: not has(B, "dv-004") and has(A, "2.200px"),
                  _bite_recorded("bfly-green", 2.2)))
    cases.append(("★ #260 a receipt that measures NOTHING (dv004_px null) invents no rule",
                  ENGINE_BFLY, lambda B, A: not has(B, "dv-004") and not has(A, "dv-004"),
                  _bite_recorded("bfly-null", None)))

    # ---- #260 · the STALE arm must be REACHABLE for a page the driver measures nothing on ------
    # V2's finding: the no-opinion exit used to run BEFORE the source-hash check, so 12 of 13
    # engine pages could carry a stale receipt and stay green. The pair below is the mutation in
    # miniature — same fixture, one byte of engine source changed.
    _fi_null_stale = _bite_recorded("bfly-null-stale", None)
    open(_fi_null_stale["_src"], "w").write("engine v2 — edited after the drive")
    cases.append(("★ #260 a FRESH receipt with no measured dv-004 figure still passes (no rule invented)",
                  ENGINE_BFLY, lambda B, A: not has(B, "dv-004") and not has(A, "dv-004"),
                  _bite_recorded("bfly-null-fresh", None)))
    cases.append(("★ #260 the SAME receipt with one source hash changed is BLOCKING STALE",
                  ENGINE_BFLY, lambda B, A: has(B, "dv-004") and has(B, "STALE")
                  and has(B, "dv-render-butterfly.js") and has(B, "_drive_chart_engine.py"),
                  _fi_null_stale))
    _fi_no_receipt = dict(_bite_recorded("bfly-none", None),
                          receipts=os.path.join(_tmp, "bfly-none", "nope.json"))
    cases.append(("★ #260 a mapped engine page with NO receipt at all is BLOCKING, never a skip",
                  ENGINE_BFLY, lambda B, A: has(B, "dv-004") and has(B, "ENGINE-DRAWN")
                  and has(B, "_drive_chart_engine.py"), _fi_no_receipt))

    ok = bool(_map_ok)
    for case in cases:
        name, fig, pred = case[0], case[1], case[2]
        fileinfo = case[3] if len(case) > 3 else None
        try:
            B, A = run(fig, fileinfo)
            passed = pred(B, A)
        except Exception as e:
            passed = False
            B, A = ["EXC: %s" % e], []
        print("  [%s] %s" % ("ok" if passed else "XX", name))
        if not passed:
            ok = False
            print("        B=%s" % B)
    __import__("shutil").rmtree(_tmp, ignore_errors=True)
    print("\n%s selftest" % ("✅" if ok else "❌"))
    return 0 if ok else 1

def matrix():
    """#261 D3's receipt: every artefact x figure x rule, and WHICH ROUTE answered it.

    `static OR driven, never skipped` is only checkable if you can see the route. A `?` in this
    table is a rule that answered nothing — the exact silence s260-D3 forbids.
    """
    files = discover()
    for path in files:
        try:
            check_file(path)
        except Exception as e:  # a broken file must not hide the rest of the table
            print("  [EXC] %s — %s" % (os.path.relpath(path, HERE), e))
    # requiredAria is declared once per FILE (the #token-manifest is the file's, not the figure's),
    # so its route is the artefact's and is repeated down the artefact's figure rows.
    per_file = {art: how for art, fig, rule, how in ROUTES if rule == "requiredAria"}
    seen = {}
    for art, fig, rule, how in ROUTES:
        if rule == "requiredAria":
            continue
        seen.setdefault((art, fig), {})[rule] = how
    fig_rules = [r for r in MATRIX_RULES if r != "requiredAria"]
    hdr = "%-36s %-8s " % ("artefact", "figure") + " ".join("%-11s" % r for r in fig_rules) + " requiredAria"
    print(hdr)
    print("-" * len(hdr))
    gaps = 0
    for (art, fig) in sorted(seen):
        row = seen[(art, fig)]
        cells = []
        for r in fig_rules:
            v = row.get(r, "?")
            if v == "?":
                gaps += 1
            cells.append("%-11s" % v)
        aria = per_file.get(art, "?")
        if aria == "?":
            gaps += 1
        print("%-36s %-8s " % (art[:36], fig[:8]) + " ".join(cells) + " " + aria)
    n_driven = sum(1 for v in ROUTES if v[3] == "driven")
    n_static = sum(1 for v in ROUTES if v[3] == "static")
    n_na = sum(1 for v in ROUTES if v[3] == "n-a")
    print("\n%d artefact(s), %d figure-row(s): %d driven · %d static · %d n-a · %d unanswered."
          % (len(files), len(seen), n_driven, n_static, n_na, gaps))
    if gaps:
        print("❌ %d rule(s) answered by NEITHER route — that is the skip s260-D3 forbids." % gaps)
    return 1 if gaps else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--matrix" in sys.argv:
        sys.exit(matrix())
    sys.exit(main())
