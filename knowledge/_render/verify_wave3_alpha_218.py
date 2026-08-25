#!/usr/bin/env python3
"""
verify_wave3_alpha_218.py — #218 wave-3 LANE α (FORMS).

WHAT THIS LANE ACTUALLY PRODUCED, AND WHY IT IS A VERIFIER AND NOT EIGHT SNIPPETS
  The lane brief (notes/_briefs/2026-08-25-218-wave3-lanes-brief.md) asked for EIGHT new
  form-family snippets, drawn from the wave-3 draft in notes/_receipts/2026-08-24-crank-charts.md
  ("From the measured v3 (78 Gap): lane α — Inputs & forms P1 (8: …)").

  That draft read the WRONG COLUMN of reviews/ITINERARY-STATUS-2026-08-21-v3.json.

    · `itinerary_status`  is the 2026-07-14 planning spreadsheet's frozen status column.
                          Counter over 124 rows: {Gap: 78, Gated: 39, Partial: 7}   <- the 78
    · `derived`           is what the generator MEASURED against the working tree.
                          Counter over 124 rows: {GATED: 121, ASSET-SYSTEM: 1,
                                                  ASSET-ONLY: 1, GAP: 1}
    · `$true_gaps`        == [86]  (row 86, "Brand mark / logo", derived ASSET-ONLY)
    · `$drift_counts`     == {AGREES: 40, "STALE — itinerary UNDERSTATES the store": 84}

  The register DECLARES its own drift, in a field the draft did not read. All eight lane-α rows
  (13–20) carry derived "GATED" and drift "STALE — itinerary UNDERSTATES the store". Every one of
  the eight artefacts is present in the store TODAY on all five of the register's own signals.

  Building the eight would therefore have produced EIGHT DUPLICATES of gated canonical artefacts,
  and handed them to the conductor's regen serial. So this lane built the instrument that proves
  the artefact instead, and returned the finding. (#210's lesson; "queue vs canon disagree ⇒ the
  queue is the defect"; "premise ages faster than rule".)

WHAT IT REFUSES TO DO
  It does not read the verdict out of the register and re-print it — that would be a tautology,
  green whether or not a single file exists. Every presence check probes the WORKING TREE
  directly (filesystem, `_validate_radius.MIGRATED_SNIPPETS`, canon.css text) and is required to
  go RED in the --break arm. The register is read only for the two DRIFT checks, which are
  claims ABOUT the register and are the controls (green in both arms).

THE --break ARM (a verifier that cannot fail proves nothing)
  --break rebuilds the store in a session-suffixed mutant dir with the eight lane-α artefacts
  REMOVED (snippet + meta + showroom page), and the canon .cn- rules for those eight stripped.
  Every store/*/present check must go RED there BY NAME. If a store check is green in the break
  arm it is not measuring the store, and the run reports FAILED.

  ⚠ CONTROLS. `control/register-readable` and `control/store-root-populated` must be GREEN IN
  BOTH ARMS. A red control in the break arm means the arm proved nothing (e.g. the mutant dir
  never got built) and the whole run is reported FAILED rather than passed.

USAGE
  python3 knowledge/_render/verify_wave3_alpha_218.py           # the real tree — all green
  python3 knowledge/_render/verify_wave3_alpha_218.py --break   # artefacts removed — store checks red

  Mutant dir: $AW_MUTANT_DIR, default /var/tmp/218w3a-alpha-s218wa (session-suffixed per the
  shared-/var/tmp class fix — a foreign-owned fixed path refuses a fresh seat).

No browser, no network, no font farm: every claim this lane makes is a claim about files.
"""

import importlib.util
import json
import os
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REGISTER = REPO / "reviews" / "ITINERARY-STATUS-2026-08-21-v3.json"
MUTANT = Path(os.environ.get("AW_MUTANT_DIR", "/var/tmp/218w3a-alpha-s218wa"))

# itinerary row -> (row name, store slug).  Slugs are the register's OWN `slugs` field, not guesses.
LANE_ALPHA = {
    13: ("Form layout + validation",          "form-layout",       "Form-layout"),
    14: ("Date picker",                       "date-picker",       "Date-picker"),
    15: ("Date-range picker",                 "date-range-picker", "Date-range-picker"),
    16: ("Time picker",                       "time-picker",       "Time-picker"),
    17: ("Number / currency (amount) input",  "amount-input",      "Amount-input"),
    18: ("File upload / dropzone",            "file-upload",       "File-upload"),
    19: ("OTP / PIN / secure entry",          "secure-entry",      "Secure-entry"),
    20: ("Textarea",                          "textarea",          "Textarea"),
}

STALE = "STALE — itinerary UNDERSTATES the store"

RESULTS = []  # (name, ok, detail)


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def load_migrated(root):
    """MIGRATED_SNIPPETS as the radius gate itself defines it — imported, never re-parsed."""
    path = root / "knowledge" / "_validate_radius.py"
    spec = importlib.util.spec_from_file_location("_vr_alpha218", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))       # the gate imports its sibling `_helpgate`
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return {s.lower() for s in mod.MIGRATED_SNIPPETS}


def build_mutant():
    """Copy the store, then REMOVE the eight lane-α artefacts. One respect differs: their presence."""
    if MUTANT.exists():
        shutil.rmtree(MUTANT)
    MUTANT.mkdir(parents=True, exist_ok=True)
    for rel in ("knowledge/snippets", "knowledge/components", "showroom", "knowledge/canon"):
        src = REPO / rel
        dst = MUTANT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.png", "*.jpg", "*.jpeg", "*.webp"))
    for sibling in ("_validate_radius.py", "_helpgate.py"):
        src = REPO / "knowledge" / sibling
        if src.exists():
            shutil.copy2(src, MUTANT / "knowledge" / sibling)

    # strip the eight from MIGRATED_SNIPPETS
    vr = MUTANT / "knowledge" / "_validate_radius.py"
    text = vr.read_text()
    # ⚠ entries are the CAPITALISED FILENAME ("Form-layout.reference.html"), not the slug — the
    # first --break run stripped nothing because this matched on the slug, and the arm reported
    # FAILED rather than laundering the partial mutation as a pass. That is the arm earning its keep.
    for _row, (_n, _slug, fname) in LANE_ALPHA.items():
        text = re.sub(r"""^[ \t]*["']%s\.reference\.html["'],?[ \t]*(#.*)?\n""" % re.escape(fname),
                      "", text, flags=re.M | re.I)
    vr.write_text(text)

    # remove snippet + meta + showroom page, and the canon .cn- rules for each
    canon = MUTANT / "knowledge" / "canon" / "canon.css"
    css = canon.read_text()
    for _row, (_n, slug, fname) in LANE_ALPHA.items():
        for p in (MUTANT / "knowledge" / "snippets" / ("%s.reference.html" % fname),
                  MUTANT / "knowledge" / "components" / ("%s.meta.json" % slug),
                  MUTANT / "showroom" / ("%s.html" % slug)):
            if p.exists():
                p.unlink()
        css = re.sub(r"\.cn-%s[\w-]*\b" % re.escape(slug.split("-")[0]), ".cn-REMOVED", css)
    canon.write_text(css)
    return MUTANT


def main():
    broken = "--break" in sys.argv
    root = build_mutant() if broken else REPO

    # ---- controls: green in BOTH arms -------------------------------------------------
    reg = None
    try:
        reg = json.loads(REGISTER.read_text())
        check("control/register-readable", isinstance(reg.get("rows"), list) and len(reg["rows"]) == 124,
              "%d rows" % len(reg.get("rows", [])))
    except Exception as exc:                                    # a crash is not a fail — name it
        check("control/register-readable", False, "%s: %s" % (type(exc).__name__, exc))

    n_snips = len(list((root / "knowledge" / "snippets").glob("*.reference.html")))
    check("control/store-root-populated", n_snips > 100, "%d snippets present" % n_snips)

    # ---- the DRIFT claims: about the register, so green in both arms ------------------
    if reg:
        rows = reg["rows"]
        itin = Counter(r["itinerary_status"] for r in rows)
        der = Counter(r["derived"] if isinstance(r["derived"], str) else r["derived"].get("verdict")
                      for r in rows)
        check("drift/itinerary-column-says-78-gap", itin.get("Gap") == 78,
              "itinerary_status Gap=%s (the figure the wave-3 draft quoted)" % itin.get("Gap"))
        check("drift/derived-column-says-1-gap", der.get("GAP") == 1,
              "derived GAP=%s GATED=%s" % (der.get("GAP"), der.get("GATED")))
        check("drift/true-gaps-is-row-86-only", reg.get("$true_gaps") == [86],
              "$true_gaps=%s" % reg.get("$true_gaps"))
        check("drift/register-declares-84-stale", (reg.get("$drift_counts") or {}).get(STALE) == 84,
              "$drift_counts=%s" % json.dumps(reg.get("$drift_counts")))
        for row, (name, _slug, _f) in LANE_ALPHA.items():
            r = rows[row - 1]
            d = r["derived"] if isinstance(r["derived"], str) else r["derived"].get("verdict")
            check("drift/row-%d-derived-GATED-not-Gap" % row,
                  r["itinerary_status"] == "Gap" and d == "GATED" and r["drift"] == STALE,
                  "%s | itinerary=%s derived=%s" % (name, r["itinerary_status"], d))

    # ---- the STORE claims: probe the tree; MUST go red under --break ------------------
    try:                                        # a crash is not a fail — name it, never default it
        migrated = load_migrated(root)
        check("control/migrated-set-loaded", len(migrated) > 0, "%d entries" % len(migrated))
    except Exception as exc:
        check("control/migrated-set-loaded", False, "%s: %s" % (type(exc).__name__, exc))
        migrated = set()
    canon_css = (root / "knowledge" / "canon" / "canon.css").read_text()
    for row, (_name, slug, fname) in LANE_ALPHA.items():
        snippet = root / "knowledge" / "snippets" / ("%s.reference.html" % fname)
        meta = root / "knowledge" / "components" / ("%s.meta.json" % slug)
        showroom = root / "showroom" / ("%s.html" % slug)
        rules = len(re.findall(r"\.cn-%s\b" % re.escape(slug.split("-")[0]), canon_css))
        check("store/row-%d/%s/snippet-present" % (row, slug), snippet.exists(),
              "%s (%s B)" % (snippet.name, snippet.stat().st_size if snippet.exists() else 0))
        check("store/row-%d/%s/meta-present" % (row, slug), meta.exists(), meta.name)
        check("store/row-%d/%s/showroom-present" % (row, slug), showroom.exists(), showroom.name)
        check("store/row-%d/%s/migrated" % (row, slug),
              ("%s.reference.html" % slug) in migrated, "in MIGRATED_SNIPPETS")
        check("store/row-%d/%s/canon-rules" % (row, slug), rules > 0, "%d .cn- rules" % rules)

    # ---- report ----------------------------------------------------------------------
    store = [r for r in RESULTS if r[0].startswith("store/")]
    ctrl = [r for r in RESULTS if r[0].startswith("control/")]
    drift = [r for r in RESULTS if r[0].startswith("drift/")]
    for name, ok, detail in RESULTS:
        print("%s  %-46s %s" % ("PASS" if ok else "FAIL", name, detail))

    print("-" * 96)
    if broken:
        ctrl_ok = all(ok for _n, ok, _d in ctrl)
        store_red = [n for n, ok, _d in store if ok]
        drift_ok = all(ok for _n, ok, _d in drift)
        print("--break arm: controls %s | drift(control) %d/%d green | store %d/%d RED by name"
              % ("GREEN" if ctrl_ok else "RED", sum(ok for _n, ok, _d in drift), len(drift),
                 len(store) - len(store_red), len(store)))
        if not ctrl_ok:
            print("FAILED: a control went red — the arm proved nothing.")
            return 1
        if store_red:
            print("FAILED: these store checks stayed green with the artefacts removed: %s"
                  % ", ".join(store_red))
            return 1
        if not drift_ok:
            print("FAILED: a drift control went red in the break arm.")
            return 1
        print("OK: every store check is a real measurement (it can fail); the drift finding holds.")
        return 0

    failed = [n for n, ok, _d in RESULTS if not ok]
    print("green arm: %d/%d checks green (%d control · %d drift · %d store)"
          % (len(RESULTS) - len(failed), len(RESULTS), len(ctrl), len(drift), len(store)))
    if failed:
        print("FAILED by name: %s" % ", ".join(failed))
        return 1
    print("OK: all eight lane-α rows are GATED in the store; the '8 to build' premise is a "
          "stale-column artefact. TRUE gaps in the register: row 86 only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
