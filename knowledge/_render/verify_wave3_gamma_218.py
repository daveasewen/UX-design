#!/usr/bin/env python3
"""
verify_wave3_gamma_218.py — #218 wave-3 lane γ (DATA DISPLAY). The lane's verify.

⚠ WHAT THIS INSTRUMENT ACTUALLY VERIFIES, AND WHY IT IS NOT A BUILD VERIFY.

The lane brief (notes/_briefs/2026-08-25-218-wave3-lanes-brief.md) asked lane γ to build three
components — data grid · stat/metric card · empty state — and FIRST to check whether the
charts-kit gap row is a register artefact before building anything for it.

It is. And so are the other three. All FOUR of the lane's rows already resolve to fully gated
components in the store. There was nothing in this lane to build, so the lane's verify is the
instrument that PROVES that, and that would catch the same mis-cut next time.

THE DEFECT CLASS THIS GATE EXISTS FOR (why it is in the repo, not a scratch file — s191-D2):

  reviews/ITINERARY-STATUS-*.json carries TWO status columns per row and they do not agree:

    the FROZEN column   the status CELL from the FROZEN 2026-07-14 spreadsheet snapshot.
                        124 rows, of which 78 read "Gap". It is a 2026-07 photograph.
                        ★ #218: emitted as `itinerary_status_2026_07_14_FROZEN` from v4 on —
                        the bare `itinerary_status` was read as live twice. v1-v3 are
                        write-once and keep the old name, so this gate reads the column
                        through `gen_itinerary_status.frozen_status()`, which spans both.
    `derived`           what the generator MEASURED in the store, five probes deep
                        (snippet · meta · showroom · MIGRATED_SNIPPETS · canon .cn- rules).
                        121 GATED · 1 ASSET-SYSTEM · 1 ASSET-ONLY · 1 GAP.

  Every row in the register whose two columns disagree is stamped
  `drift: "STALE — itinerary UNDERSTATES the store"` — 84 of them. Reading the FROZEN column and
  calling the result a gap list produces a build brief for work that is already done. That is
  exactly what happened to wave 3: all sixteen components across lanes α, β and γ derive GATED.

  So arm G4 asserts the disagreement ON PURPOSE. It is the only arm whose failure would be GOOD
  news — it goes red the day someone reconciles the frozen column, at which point this gate has
  no more reason to exist and should be retired with the drift.

ARMS

  G1 REGISTER-DERIVED   the newest ITINERARY-STATUS register derives GATED (never GAP) for every
                        lane-γ row: 51 data grid · 52 stat/metric card · 53 charts kit ·
                        54 empty state.
  G2 STORE-QUINTET      ⛔ re-MEASURED on disk NOW, not read out of the register. The register is
                        itself a measurement, dated 2026-08-21; a premise ages faster than a rule
                        ([[premise-ages-faster-than-rule]]), so this arm asks a source with a
                        DIFFERENT CLOCK — the working tree — for all five probes per slug.
  G3 CHART-FAMILY       the charts-kit row is not one artefact but the Chart-* family; all 14
                        slugs must carry the full quintet. This is the arm the brief asked for
                        by name.
  G4 COLUMN-CONFUSION   the frozen and measured columns disagree on the lane's rows, and the
                        register's measured GAP total is 1. See above.

BREAK ARM

  --break  builds a MUTANT register + store under $BM_MUTANT_DIR (session-suffixed), flips row 51
           `derived` to GAP and removes Stat-card's meta, and requires G1 and G2 to go red BY
           NAME. Bucketed by name, never by "something failed"
           ([[mutation-tests-the-clause-not-the-feature]]).

Usage:  python3 knowledge/_render/verify_wave3_gamma_218.py
        python3 knowledge/_render/verify_wave3_gamma_218.py --break
Exits non-zero on any failure. No browser, no render env — nothing here needs a paint.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# knowledge/_render/<this file> -> up three to the repo root.
ROOT = os.path.dirname(os.path.dirname(HERE))
REVIEWS = os.path.join(ROOT, "reviews")
# ★ #218 — ONE reader for the frozen column, imported rather than re-typed. This gate reads the
# NEWEST register by design, so it was the consumer the rename would have broken first: a
# `.get("itinerary_status")` against v4 returns None, frozen_gap falls to 0 and G4 reports
# "the columns no longer disagree" — a false green in the shape of a red.
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
from gen_itinerary_status import frozen_status  # noqa: E402

# The lane's four itinerary rows, by number and by the name the frozen snapshot gives them.
LANE_ROWS = {
    51: "Data grid (sort/filter/select/edit)",
    52: "Stat / metric card",
    53: "Charts / data-viz kit",
    54: "Empty state",
}
# Slug -> the snippet basename it must resolve to. Row 52's mechanical slug 'stat-metric-card'
# MISSES the store (the file is Stat-card) — the register resolves it by hand and records why.
# Naming that here keeps the resolution visible instead of buried in a slugify().
GAMMA_SLUGS = {
    "data-grid": "Data-grid.reference.html",
    "stat-card": "Stat-card.reference.html",
    "empty-state": "Empty-state.reference.html",
}
CHART_SLUGS = [
    "chart-bar", "chart-boxplot", "chart-bullet", "chart-butterfly-h", "chart-butterfly-v",
    "chart-candlestick", "chart-combo", "chart-donut", "chart-histogram", "chart-line",
    "chart-pie", "chart-scatter", "chart-sparkline", "chart-stacked-area",
]


def newest_register(reviews_dir):
    """The newest ITINERARY-STATUS json. ⛔ Never hard-code v3: a gate pinned to a filename
    silently measures a stale snapshot the day the next one lands."""
    cands = sorted(
        f for f in os.listdir(reviews_dir)
        if re.match(r"^ITINERARY-STATUS-\d{4}-\d{2}-\d{2}-v\d+\.json$", f)
    )
    if not cands:
        return None, "no ITINERARY-STATUS-*.json in %s" % reviews_dir
    return os.path.join(reviews_dir, cands[-1]), None


def rows_by_n(reg_path):
    with open(reg_path) as fh:
        doc = json.load(fh)
    rows = doc["rows"]
    rows = rows if isinstance(rows, list) else list(rows.values())
    return doc, {r["n"]: r for r in rows}


def snippet_basename(root, slug):
    """The store's basenames are Title-cased with a lowercase tail (Data-grid, not Data-Grid).
    ⚠ macOS is case-INSENSITIVE, so an os.path.exists() on a wrongly-cased name answers True at
    this seat and False in CI. Match against a real directory listing instead."""
    snips = os.path.join(root, "knowledge", "snippets")
    if not os.path.isdir(snips):
        return None
    want = (slug.replace("-", "") + ".reference.html").lower()
    for f in os.listdir(snips):
        if f.replace("-", "").lower() == want:
            return f
    return None


def quintet(root, slug):
    """The five probes, re-measured. Returns (ok_dict, evidence_str)."""
    snip = snippet_basename(root, slug)
    meta = os.path.join(root, "knowledge", "components", "%s.meta.json" % slug)
    # meta files are inconsistently cased in the store (chart-boxplot.meta.json vs
    # Chart-boxplot.meta.json) — resolve by listing, same reason as above.
    metadir = os.path.join(root, "knowledge", "components")
    meta_hit = None
    if os.path.isdir(metadir):
        for f in os.listdir(metadir):
            if f.lower() == "%s.meta.json" % slug.lower():
                meta_hit = f
                break
    page = os.path.join(root, "showroom", "%s.html" % slug)
    radius_src = os.path.join(root, "knowledge", "_validate_radius.py")
    canon_src = os.path.join(root, "knowledge", "canon", "canon.css")
    migrated = False
    if snip and os.path.exists(radius_src):
        with open(radius_src) as fh:
            migrated = ('"%s"' % snip) in fh.read() or ("'%s'" % snip) in fh.read()
    canon_rules = 0
    if os.path.exists(canon_src):
        with open(canon_src) as fh:
            canon_rules = len(re.findall(r"\.cn-%s\b" % re.escape(slug), fh.read()))
    ok = {
        "snippet": bool(snip),
        "meta": bool(meta_hit),
        "showroom": os.path.exists(page),
        "migrated": migrated,
        "canon": canon_rules > 0,
    }
    ev = "snippet=%s meta=%s showroom=%s migrated=%s canon_rules=%d" % (
        snip or "ABSENT", meta_hit or "ABSENT", os.path.basename(page) if ok["showroom"]
        else "ABSENT", migrated, canon_rules)
    return ok, ev


def drive(root, reviews_dir):
    fails = []
    reg_path, err = newest_register(reviews_dir)
    if err:
        return ["G1 REGISTER-DERIVED — %s" % err]
    doc, rows = rows_by_n(reg_path)
    print("register: %s  (%d rows, $status %s)"
          % (os.path.basename(reg_path), len(rows), doc.get("$status", "?")[:48]))

    # ---- G1 REGISTER-DERIVED -------------------------------------------------------------
    print("\nG1 REGISTER-DERIVED")
    for n, name in LANE_ROWS.items():
        r = rows.get(n)
        if r is None:
            fails.append("G1 REGISTER-DERIVED — row %d (%s) missing from the register" % (n, name))
            continue
        d = r.get("derived")
        line = "  row %-3d %-34s frozen=%-8s derived=%-6s" % (
            n, r["name"][:34], frozen_status(r), d)
        if d != "GATED":
            fails.append("G1 REGISTER-DERIVED — row %d (%s) derives %s, not GATED"
                         % (n, r["name"], d))
            print(line + "  ❌")
        else:
            print(line + "  ✅  %s" % r.get("evidence_line", "")[:52])

    # ---- G2 STORE-QUINTET ----------------------------------------------------------------
    print("\nG2 STORE-QUINTET  (re-measured on disk, not read from the register)")
    for slug in sorted(GAMMA_SLUGS):
        ok, ev = quintet(root, slug)
        missing = [k for k, v in ok.items() if not v]
        if missing:
            fails.append("G2 STORE-QUINTET — %s missing %s  [%s]"
                         % (slug, "+".join(missing), ev))
            print("  %-12s ❌ missing %s" % (slug, "+".join(missing)))
        else:
            print("  %-12s ✅ %s" % (slug, ev))

    # ---- G3 CHART-FAMILY -----------------------------------------------------------------
    print("\nG3 CHART-FAMILY  (the brief's named question: is the charts-kit row a real gap?)")
    bad = []
    for slug in CHART_SLUGS:
        ok, ev = quintet(root, slug)
        missing = [k for k, v in ok.items() if not v]
        if missing:
            bad.append("%s(%s)" % (slug, "+".join(missing)))
    if bad:
        fails.append("G3 CHART-FAMILY — %d of %d chart slugs incomplete: %s"
                     % (len(bad), len(CHART_SLUGS), ", ".join(bad)))
        print("  ❌ %d of %d incomplete: %s" % (len(bad), len(CHART_SLUGS), ", ".join(bad)))
    else:
        print("  ✅ all %d chart-* slugs carry the full quintet — the row is a FAMILY, fully "
              "gated, not a gap" % len(CHART_SLUGS))

    # ---- G4 COLUMN-CONFUSION -------------------------------------------------------------
    print("\nG4 COLUMN-CONFUSION  (asserts the two columns DISAGREE — the mis-cut's root cause)")
    counts = doc.get("$counts", {})
    measured_gaps = counts.get("GAP", None)
    if measured_gaps != 1:
        fails.append("G4 COLUMN-CONFUSION — register $counts GAP is %r, expected 1. The measured "
                     "gap total moved; re-read the register before trusting any gap list."
                     % measured_gaps)
        print("  ❌ measured GAP total = %r (expected 1)" % measured_gaps)
    else:
        print("  ✅ measured GAP total = 1 (row 124, Layer-2 variant matrices); "
              "$true_gaps = %s" % doc.get("$true_gaps"))
    frozen_gap = sum(1 for r in rows.values() if frozen_status(r) == "Gap")
    drifted = sum(1 for r in rows.values() if "UNDERSTATES" in (r.get("drift") or ""))
    print("  ·  frozen column reads Gap on %d rows; %d rows stamped "
          "'itinerary UNDERSTATES the store'" % (frozen_gap, drifted))
    if frozen_gap <= counts.get("GAP", 0):
        fails.append("G4 COLUMN-CONFUSION — the frozen and measured columns no longer disagree "
                     "(frozen Gap=%d, measured GAP=%d). If the snapshot has been reconciled, "
                     "RETIRE this gate with the drift." % (frozen_gap, counts.get("GAP", 0)))
        print("  ❌ columns agree — gate has outlived its defect")
    for n in LANE_ROWS:
        r = rows.get(n) or {}
        if r and frozen_status(r) == "Gap" and r.get("derived") == "GATED":
            print("  ·  row %d: frozen 'Gap' vs measured 'GATED' — a brief reading the frozen "
                  "column would have commissioned this build" % n)
    return fails


def build_mutant(root, mutant_dir):
    """Copy just enough of the tree to break: the register + the store paths the arms probe."""
    if os.path.exists(mutant_dir):
        shutil.rmtree(mutant_dir)
    for rel in ("reviews", "knowledge/snippets", "knowledge/components", "showroom",
                "knowledge/canon"):
        src = os.path.join(root, rel)
        dst = os.path.join(mutant_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if rel == "reviews":
            os.makedirs(dst, exist_ok=True)
            for f in os.listdir(src):
                if f.startswith("ITINERARY-STATUS-") and f.endswith(".json"):
                    shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
        elif rel == "showroom":
            os.makedirs(dst, exist_ok=True)
            for f in os.listdir(src):
                if f.endswith(".html"):
                    shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
        else:
            shutil.copytree(src, dst)
    shutil.copy2(os.path.join(root, "knowledge", "_validate_radius.py"),
                 os.path.join(mutant_dir, "knowledge", "_validate_radius.py"))

    # MUTATION 1 — flip row 51's measured verdict to GAP (G1 must name row 51).
    reg_path, _ = newest_register(os.path.join(mutant_dir, "reviews"))
    with open(reg_path) as fh:
        doc = json.load(fh)
    rows = doc["rows"] if isinstance(doc["rows"], list) else list(doc["rows"].values())
    for r in rows:
        if r["n"] == 51:
            r["derived"] = "GAP"
    doc["rows"] = rows
    with open(reg_path, "w") as fh:
        json.dump(doc, fh)

    # MUTATION 2 — remove Stat-card's meta (G2 must name stat-card, missing meta).
    for f in os.listdir(os.path.join(mutant_dir, "knowledge", "components")):
        if f.lower() == "stat-card.meta.json":
            os.remove(os.path.join(mutant_dir, "knowledge", "components", f))
    return mutant_dir


def main():
    if "--break" in sys.argv:
        base = os.environ.get("BM_MUTANT_DIR")
        if not base:
            sys.exit("verify_wave3_gamma_218: --break needs BM_MUTANT_DIR "
                     "(session-suffixed, e.g. /var/tmp/bm-mutant-s218wc)")
        print("⬛ BREAK ARM — mutant tree at %s\n" % base)
        mroot = build_mutant(ROOT, base)
        fails = drive(mroot, os.path.join(mroot, "reviews"))
        # ⬛ INVERTED. Bucketed BY NAME: "something failed" is not the test.
        g1 = [f for f in fails if f.startswith("G1 REGISTER-DERIVED") and "row 51" in f]
        g2 = [f for f in fails if f.startswith("G2 STORE-QUINTET") and "stat-card" in f]
        print()
        if not g1:
            print("⛔ BREAK ARM DID NOT GO RED — row 51 was flipped to GAP and G1 still passed. "
                  "A gate that cannot fail is not a gate. (%d other failure(s))" % len(fails))
            sys.exit(1)
        if not g2:
            print("⛔ BREAK ARM DID NOT GO RED — stat-card's meta was deleted and G2 still "
                  "passed. (%d other failure(s))" % len(fails))
            sys.exit(1)
        print("✅ BREAK ARM RED AS REQUIRED — both clauses named, %d failure(s) total:"
              % len(fails))
        for f in g1 + g2:
            print("  ❌ " + f)
        return

    fails = drive(ROOT, REVIEWS)
    if fails:
        print("\n%d FAILURE(S):" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print("\nOK — lane γ's four itinerary rows all resolve to gated components in the store. "
          "The charts-kit row is a REGISTER ARTEFACT (frozen snapshot cell), not a gap, and so "
          "are rows 51, 52 and 54. Nothing in this lane was buildable.")


if __name__ == "__main__":
    main()
