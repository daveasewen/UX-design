#!/usr/bin/env python3
"""
gen_radius_derive.py — MINT-TIME radius/padding derivation (s200-D1). PROPOSAL-ONLY output;
the CONSOLE values were minted into the token store at #200 (s200-D2/s200-D3).

Ruling s200-D1 (#200, Dave, 2026-08-18) makes radius/padding derivation a MINT-TIME
mechanism, not a live calc: the generator computes derived values and the mint writes
CONCRETE numbers, so on disk everything the gates parse stays plain. Direction runs
PER FAMILY:

  CARDS              padding derives FROM the minted card radius.
  SEGMENTED CONTROLS padding is hand-tuned per SCALE by Dave; the thumb radius
                     derives as  container_radius - padding  (concentric corners).

All padding steps in 2px so stacked totals snap to the 4px grid (s200-D1 clause d).

SCOPE — THIS SCRIPT DECIDES NOTHING.
  * The card padding FORMULA is PROPOSED, not ruled: max(radius, 8) snapped to 2px.
  * The scale set (small/medium/large) and their paddings (2/4/6) are PROPOSED
    STARTING values — Dave tunes them.
  * The derived-radius FLOOR (2) is PROPOSED.
  Every emitted value carries "$proposed": true. Nothing here lands in canon until
  Dave has seen it rendered (s200-D1: "no derived value lands in canon until Dave
  has seen it rendered").

WRITES — exactly one file: knowledge/_derive-radius-proposal.json
  It does NOT write tokens/*.json, canon, _rulings.json, state or queues, and it
  runs no other generator. Read-only on every input.

FAIL LOUD, NEVER GUESS: an input that cannot be resolved is a REFUSAL (DeriveRefusal,
named), never a silent default. UNKNOWN is never defaulted to a number.

MODES
  (no args)   recompute and WRITE the proposal file
  --check     recompute and COMPARE against the proposal file on disk; rc!=0 on drift
  --selftest  mutation proof: plant a wrong derived value, prove --check detects it

INPUTS
  knowledge/tokens/layout.json                     border-radius family (mono base)
  knowledge/tokens/themes/*.overrides.json         per-theme border-radius/* overrides
"""

import argparse
import copy
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUT = os.path.join(HERE, "tokens", "layout.json")
THEMES_DIR = os.path.join(HERE, "tokens", "themes")
OUT = os.path.join(HERE, "_derive-radius-proposal.json")

# ---------------------------------------------------------------- PROPOSED knobs
PROPOSED_CARD_PADDING_MIN = 8      # PROPOSED — the `8` in max(radius, 8)
PROPOSED_PADDING_STEP = 2          # RULED s200-D1 clause (d): padding steps in 2px
PROPOSED_DERIVED_RADIUS_FLOOR = 2  # PROPOSED — floor for derived thumb radii
PROPOSED_SCALES = {                # PROPOSED starting paddings, 2px steps
    "small": 2,
    "medium": 4,
    "large": 6,
}

# Themes to derive for. mono is the BASE (layout.json itself, no overrides file).
THEMES = ["apollo-console", "mono", "apollo-legacy", "apollo-supercharge"]
THEME_FILE = {
    "apollo-console": "apollo-console.overrides.json",
    "apollo-legacy": "apollo-legacy.overrides.json",
    "apollo-supercharge": "apollo-supercharge.overrides.json",
}

# border-radius/container is now a MINTED TOKEN (s200-D2 / s200-D3, #200, 2026-08-18):
# the base role lives in layout.json (aliasing border-radius/default like every other
# role) and console overrides it to 20. The former PROPOSED_CONTAINER_SLOT constant here
# was a DECLARED TEMPORARY standing in for the unminted slot; it is DELETED (write-once,
# ADR-0017) and 'container' is now resolved from the store like control/surface/indicator.


class DeriveRefusal(Exception):
    """A named, loud refusal. Never caught to produce a default."""


def refuse(what, why):
    raise DeriveRefusal("REFUSE [%s]: %s" % (what, why))


def load_json(path, what):
    if not os.path.exists(path):
        refuse(what, "input file missing: %s" % path)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        refuse(what, "input is not valid JSON (%s): %s" % (path, exc))


def as_px(value, what):
    """Coerce a token $value to an integer px. 20 / '20' / '20px' all legal.
    Anything else REFUSES — no guessing."""
    if value is None:
        refuse(what, "radius value is absent (None) — UNKNOWN is never defaulted")
    if isinstance(value, bool):
        refuse(what, "radius value is a bool, not a dimension: %r" % (value,))
    if isinstance(value, (int, float)):
        if float(value) != int(value):
            refuse(what, "radius value is fractional (%r); px derivation needs integers" % (value,))
        return int(value)
    if isinstance(value, str):
        raw = value.strip()
        if raw.endswith("px"):
            raw = raw[:-2].strip()
        try:
            num = float(raw)
        except ValueError:
            refuse(what, "radius value %r is not a parseable px dimension" % (value,))
        if num != int(num):
            refuse(what, "radius value is fractional (%r)" % (value,))
        return int(num)
    refuse(what, "radius value has unusable type %s: %r" % (type(value).__name__, value))


def base_radii():
    """Mono base radii from layout.json's border-radius family."""
    doc = load_json(LAYOUT, "layout.json")
    fam = doc.get("border-radius")
    if not isinstance(fam, dict):
        refuse("layout.json", "no 'border-radius' family object found")
    out = {}
    for role, node in fam.items():
        if role.startswith("$"):
            continue
        if not isinstance(node, dict):
            refuse("layout.json border-radius/%s" % role, "role node is not an object")
        if "$value" not in node:
            refuse("layout.json border-radius/%s" % role, "role node carries no $value")
        out[role] = as_px(node["$value"], "layout.json border-radius/%s" % role)
    if not out:
        refuse("layout.json", "border-radius family resolved to zero roles")
    return out


def theme_radii(theme):
    """Resolved radii for one theme: mono base, then that theme's overrides."""
    resolved = dict(base_radii())
    provenance = {r: "layout.json border-radius/%s (mono base)" % r for r in resolved}

    if theme != "mono":
        fname = THEME_FILE.get(theme)
        if fname is None:
            refuse("theme %s" % theme, "no overrides filename registered for this theme")
        doc = load_json(os.path.join(THEMES_DIR, fname), "%s overrides" % theme)
        ov = doc.get("overrides")
        if not isinstance(ov, dict):
            refuse("%s overrides" % theme, "no 'overrides' object found")
        hits = {k: v for k, v in ov.items() if k.startswith("border-radius/")}
        # An override of border-radius/default re-bases every role that ALIASES it.
        # In layout.json control/surface/indicator all carry $alias -> default.
        layout = load_json(LAYOUT, "layout.json")["border-radius"]
        if "border-radius/default" in hits:
            newdef = as_px(hits["border-radius/default"].get("$value"),
                           "%s border-radius/default" % theme)
            for role, node in layout.items():
                if role.startswith("$"):
                    continue
                if role == "default" or (isinstance(node, dict)
                                         and node.get("$alias") == "border-radius/default"):
                    resolved[role] = newdef
                    provenance[role] = "%s override border-radius/default (alias)" % theme
        for key, node in hits.items():
            role = key.split("/", 1)[1]
            if role == "default":
                provenance["default"] = "%s override border-radius/default" % theme
                continue
            if not isinstance(node, dict):
                refuse("%s %s" % (theme, key), "override node is not an object")
            resolved[role] = as_px(node.get("$value"), "%s %s" % (theme, key))
            provenance[role] = "%s override %s" % (theme, key)
        if not hits:
            provenance["$note"] = ("%s declares NO border-radius override — it inherits "
                                   "the mono base verbatim." % theme)

    # container: MINTED ROLE (s200-D2/s200-D3). It is resolved by the ordinary role walk
    # above — base from layout.json (alias to border-radius/default), overridden per theme
    # where a theme declares it. No constant, no fallback, no invention: if the store does
    # not carry the role, that is a REFUSAL, not a guessed number.
    if "container" not in resolved:
        refuse("theme %s" % theme,
               "border-radius/container is absent from the resolved role set — it is a "
               "MINTED role (s200-D2/s200-D3) and must come from layout.json; "
               "UNKNOWN is never defaulted")
    return resolved, provenance


def snap2(n, what):
    """Snap to the nearest even px (the 2px padding step, s200-D1 clause d).
    Ties (odd values) round UP — an odd n is exactly between two even numbers."""
    if not isinstance(n, int):
        refuse(what, "snap2 needs an int, got %r" % (n,))
    return n if n % 2 == 0 else n + 1


def card_padding(radius):
    """PROPOSED formula: max(radius, 8) snapped to 2px."""
    return snap2(max(radius, PROPOSED_CARD_PADDING_MIN), "card padding")


def build():
    themes = {}
    for theme in THEMES:
        radii, prov = theme_radii(theme)
        card_r = radii["surface"]
        pad = card_padding(card_r)

        segs = {}
        container_r = radii["container"]
        for scale, spad in PROPOSED_SCALES.items():
            if spad % PROPOSED_PADDING_STEP != 0:
                refuse("scale %s" % scale,
                       "padding %d does not step in %dpx (s200-D1 clause d)"
                       % (spad, PROPOSED_PADDING_STEP))
            raw = container_r - spad
            floored = max(raw, PROPOSED_DERIVED_RADIUS_FLOOR)
            square_conflict = (container_r == 0)
            segs[scale] = {
                "$proposed": True,
                "padding": spad,
                "$paddingStatus": "PROPOSED starting value (2px step) — Dave tunes",
                "container_radius": container_r,
                "thumb_radius_raw": raw,
                "thumb_radius": 0 if square_conflict else floored,
                "floor_applied": (not square_conflict) and (floored != raw),
                "formula": "thumb_radius = container_radius - padding, floored at %d (PROPOSED)"
                           % PROPOSED_DERIVED_RADIUS_FLOOR,
                "inputs": {"container_radius": container_r, "padding": spad},
                "$squareThemeConflict": square_conflict,
                "$squareThemeNote": (
                    "container radius is 0 (square theme): the PROPOSED floor of %d would "
                    "round a deliberately-square theme's thumb. Emitted as 0 and FLAGGED — "
                    "the floor-vs-square precedence is Dave's to rule, not this script's."
                    % PROPOSED_DERIVED_RADIUS_FLOOR) if square_conflict else None,
            }

        themes[theme] = {
            "radii": {k: v for k, v in radii.items() if not k.startswith("$")},
            "radii_provenance": prov,
            "card": {
                "$proposed": True,
                "radius_role": "surface",
                "radius": card_r,
                "padding": pad,
                "formula": "padding = max(radius, %d) snapped to %dpx (PROPOSED, s200-D1)"
                           % (PROPOSED_CARD_PADDING_MIN, PROPOSED_PADDING_STEP),
                "inputs": {"radius": card_r, "min": PROPOSED_CARD_PADDING_MIN,
                           "snap": PROPOSED_PADDING_STEP},
                "container_variant": {
                    "$proposed": True,
                    "radius_role": "container (MINTED role, s200-D2/s200-D3)",
                    "radius": container_r,
                    "padding": card_padding(container_r),
                    "inputs": {"radius": container_r, "min": PROPOSED_CARD_PADDING_MIN,
                               "snap": PROPOSED_PADDING_STEP},
                },
            },
            "segmented": segs,
        }

    return {
        "$schema": "apollo/derive-radius-proposal/1",
        "$generator": "knowledge/gen_radius_derive.py",
        "$ruling": "s200-D1 (#200, 2026-08-18) — mint-time derivation mechanism",
        "$status": "PROPOSAL ONLY — nothing here is minted, nothing here is canon.",
        "$proposed": True,
        "$decidesNothing": [
            "card padding formula max(radius, 8) snapped to 2px — PROPOSED (Claude's pick)",
            "scale set small/medium/large — PROPOSED",
            "scale paddings 2/4/6 — PROPOSED starting values, Dave tunes",
            "derived-radius floor of 2 — PROPOSED",
        ],
        "$mintedAt200": {
            "$ruling": "s200-D2 minted, s200-D3 narrowed scope to CONSOLE ONLY",
            "$note": (
                "These values are no longer proposals for apollo-console — they are minted "
                "tokens on disk. Everything else in this file, and EVERY value for mono / "
                "apollo-legacy / apollo-supercharge, remains PROPOSAL ONLY and UNRATIFIED "
                "(s200-D3: squares-stay-square and the dropped 2px floor are open until Dave "
                "tunes or rules them). data-mark stays PROPOSED, untouched."
            ),
            "console_minted": {
                "border-radius/container": 20,
                "padding/segmented-control": {"small": 2, "medium": 4, "large": 6},
                "border-radius/segmented-thumb": {"small": 18, "medium": 16, "large": 14},
                "padding/card/internal": 20,
            },
            "$formulaStatus": (
                "the card padding formula max(radius,8) snap-2 is STILL PROPOSED (s200-D1 "
                "scope limit); only the RESULTING console value was minted, after Dave saw "
                "it rendered."
            ),
        },
        "$knobs": {
            "card_padding_min": PROPOSED_CARD_PADDING_MIN,
            "padding_step": PROPOSED_PADDING_STEP,
            "derived_radius_floor": PROPOSED_DERIVED_RADIUS_FLOOR,
            "scales": dict(PROPOSED_SCALES),
        },
        "$inputs": [
            "knowledge/tokens/layout.json (border-radius family)",
            "knowledge/tokens/themes/apollo-console.overrides.json",
            "knowledge/tokens/themes/apollo-legacy.overrides.json",
            "knowledge/tokens/themes/apollo-supercharge.overrides.json",
        ],
        "themes": themes,
    }


def strip_volatile(doc):
    d = copy.deepcopy(doc)
    d.pop("$generatedAt", None)
    return d


def write(doc):
    doc = dict(doc)
    doc["$generatedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    return doc


def diff_paths(a, b, path=""):
    out = []
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        return ["%s: type %s != %s" % (path or "/", type(a).__name__, type(b).__name__)]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append("%s/%s: only on disk (%r)" % (path, k, b[k]))
            elif k not in b:
                out.append("%s/%s: only recomputed (%r)" % (path, k, a[k]))
            else:
                out += diff_paths(a[k], b[k], "%s/%s" % (path, k))
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append("%s: length %d != %d" % (path, len(a), len(b)))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out += diff_paths(x, y, "%s[%d]" % (path, i))
    elif a != b:
        out.append("%s: recomputed %r != on-disk %r" % (path, a, b))
    return out


def check():
    fresh = build()
    if not os.path.exists(OUT):
        print("DRIFT: proposal file absent — %s" % OUT, file=sys.stderr)
        return 2
    disk = load_json(OUT, "proposal file")
    diffs = diff_paths(strip_volatile(fresh), strip_volatile(disk))
    if diffs:
        print("DRIFT: %d difference(s) between recomputed proposal and %s"
              % (len(diffs), os.path.basename(OUT)), file=sys.stderr)
        for d in diffs[:40]:
            print("  " + d, file=sys.stderr)
        return 1
    print("CHECK OK — proposal file matches recomputation (%d themes)."
          % len(fresh["themes"]))
    return 0


def selftest():
    """Mutation proof, both directions of s200-D1's mechanism."""
    failures = []
    if not os.path.exists(OUT):
        print("SELFTEST cannot run: proposal file absent. Run the generator first.",
              file=sys.stderr)
        return 2
    original = open(OUT, "r", encoding="utf-8").read()

    def plant(mutate, label):
        doc = json.loads(original)
        mutate(doc)
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2)
        rc = check()
        print("  planted [%s] -> check rc=%d %s"
              % (label, rc, "DETECTED" if rc != 0 else "*** MISSED ***"))
        if rc == 0:
            failures.append(label)

    try:
        print("SELFTEST: planting wrong derived values...")
        # Direction 1 — SEGMENTED: thumb radius = container - padding.
        plant(lambda d: d["themes"]["apollo-console"]["segmented"]["medium"]
              .__setitem__("thumb_radius", 99),
              "segmented thumb_radius console/medium -> 99")
        # Direction 2 — CARDS: padding derived from radius.
        plant(lambda d: d["themes"]["apollo-console"]["card"]
              .__setitem__("padding", 7),
              "card padding console -> 7 (also breaks the 2px step)")
        # Provenance must be pinned too.
        plant(lambda d: d["themes"]["mono"]["radii"].__setitem__("surface", 13),
              "mono surface radius -> 13")
    finally:
        with open(OUT, "w", encoding="utf-8") as fh:
            fh.write(original)

    print("SELFTEST: restored the real proposal file.")
    rc = check()
    if rc != 0:
        failures.append("restore did not return the file to a clean state")

    # Refusal proof: an unresolvable input must REFUSE, not default.
    for bad in [None, "auto", 4.5, True, {}]:
        try:
            as_px(bad, "selftest")
        except DeriveRefusal:
            pass
        else:
            failures.append("as_px(%r) returned a value instead of refusing" % (bad,))
    print("SELFTEST: refusal path proven for %d unresolvable inputs." % 5)

    if failures:
        print("SELFTEST FAILED:", file=sys.stderr)
        for f in failures:
            print("  " + f, file=sys.stderr)
        return 1
    print("SELFTEST OK — every planted defect was detected; refusals fired loud.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true",
                    help="recompute and compare against the proposal file; rc!=0 on drift")
    ap.add_argument("--selftest", action="store_true",
                    help="mutation proof: plant wrong derived values, prove detection")
    args = ap.parse_args()
    try:
        if args.selftest:
            return selftest()
        if args.check:
            return check()
        doc = write(build())
        print("WROTE %s (%d themes) — PROPOSAL ONLY, nothing minted."
              % (os.path.relpath(OUT, HERE), len(doc["themes"])))
        return 0
    except DeriveRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
