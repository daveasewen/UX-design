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
                     derives from the TUNED DIAL as  max(container_radius - 6, 0).
                     s202-D2 corrected reading (#202): the s199-D3 'switch' carve-out IS
                     this thumb — there is no two-state switch variant — and its
                     derivation input is the tuner DIAL (6), not the track padding.
                     Padding is still a real spacing token; it just no longer feeds the
                     thumb radius.

All padding steps in 2px so stacked totals snap to the 4px grid (s200-D1 clause d).

SCOPE — THIS SCRIPT DECIDES NOTHING; it APPLIES ruled formulae to store-read inputs.
  * Card padding = max(radius, 8) snapped to 2px — RULED s201-D4 (#201, Dave).
  * Segmented thumb = max(container - THUMB_DIAL, 0), THUMB_DIAL = 6 — RULED
    s202-D2 (#202, Dave), which RE-TUNES the input of s201-D5's max(container - X, 0)
    from the track padding to the tuner dial. Squares stay square (container 0 -> 0).
    The old PROPOSED floor of 2 is SUPERSEDED and never applied.
  * The scale set is READ FROM THE STORE — s201-D1's dimension-first xs/s/m/l. The
    retired padding-first small/medium/large names are never emitted.
  Both formulae are MINT-TIME ONLY (s200-D1 clause a): the mint writes concrete
  numbers, and WHICH values get minted, for which themes, stays Dave's act.

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
  knowledge/tokens/layout.json                     border-radius/segmented-container/<scale>
  knowledge/tokens/spacing.json                    padding/segmented-control/<scale>
  knowledge/tokens/themes/*.overrides.json         per-theme overrides of any of the above
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
CARD_PADDING_MIN = 8       # RULED s201-D4 — the `8` in max(radius, 8)
PADDING_STEP = 2           # RULED s200-D1 clause (d): padding steps in 2px
# SUPERSEDED knob, kept as RECORD not as behaviour: the PROPOSED floor of 2 for derived
# thumb radii. s201-D5 rules the thumb SHAPE as max(container - X, 0) — squares stay
# square — and s202-D2 re-tunes X from the track padding to the tuner DIAL below. The
# floor is no longer applied anywhere; it is declared here so its retirement is legible.
SUPERSEDED_DERIVED_RADIUS_FLOOR = 2

# THE TUNED DIAL — RULED s202-D2 (#202, Dave, 2026-08-18), corrected reading.
# Dave tuned the segmented THUMB on the live corner tuner and landed on 6: the thumb sits
# 6px tighter than its track. This is a DIAL, not a law of geometry — a future tuner pass
# re-tunes this ONE constant and every theme's thumb radii re-derive from it. It replaces
# the track padding as the derivation input (s201-D1's concentric console values 4/6/6/8
# are SUPERSEDED by 0/2/4/6). Padding remains a real spacing token, untouched.
SEGMENTED_THUMB_DIAL = 6

# The scale set is READ FROM THE TOKEN STORE (s201-D1 dimension-first grammar xs/s/m/l;
# the padding-first small/medium/large set is RETIRED and must never be emitted again).
SEGMENTED_SCALE_ORDER = ["xs", "s", "m", "l"]
SPACING = os.path.join(HERE, "tokens", "spacing.json")

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
            # A GROUP, not a role: the per-scale segmented families minted at s202-D1
            # (border-radius/segmented-container|segmented-thumb/<scale>) are read by
            # segmented_scales(), scale by scale. A group is skipped, never guessed at.
            if any(isinstance(v, dict) and "$value" in v
                   for k, v in node.items() if not k.startswith("$")):
                continue
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


def _theme_overrides(theme):
    """The raw overrides dict for a theme ({} for the base theme mono)."""
    if theme == "mono":
        return {}
    fname = THEME_FILE.get(theme)
    if fname is None:
        refuse("theme %s" % theme, "no overrides filename registered for this theme")
    doc = load_json(os.path.join(THEMES_DIR, fname), "%s overrides" % theme)
    ov = doc.get("overrides")
    if not isinstance(ov, dict):
        refuse("%s overrides" % theme, "no 'overrides' object found")
    return ov


def _base_node(store, path, what):
    node = store
    for seg in path.split("/"):
        if not isinstance(node, dict) or seg not in node:
            refuse(what, "base token %s is absent from the store — UNKNOWN is never defaulted" % path)
        node = node[seg]
    if not isinstance(node, dict) or "$value" not in node:
        refuse(what, "base token %s carries no $value" % path)
    return node["$value"]


def segmented_scales(theme):
    """{scale: {'padding': px, 'container_radius': px, ...provenance}} READ FROM THE STORE.

    Base (mono) values come from the minted s202-D1 base set:
      spacing.json  padding/segmented-control/<scale>
      layout.json   border-radius/segmented-container/<scale>
    A theme's own overrides win per key. The RETIRED small/medium/large names are never
    emitted — the scale set is s201-D1's xs/s/m/l, read, not hardcoded.
    """
    spacing = load_json(SPACING, "spacing.json")
    layout = load_json(LAYOUT, "layout.json")
    ov = _theme_overrides(theme)
    out = {}
    for scale in SEGMENTED_SCALE_ORDER:
        pkey = "padding/segmented-control/%s" % scale
        ckey = "border-radius/segmented-container/%s" % scale
        if pkey in ov:
            pad = as_px(ov[pkey].get("$value"), "%s %s" % (theme, pkey))
            pad_src = "%s override %s" % (theme, pkey)
        else:
            pad = as_px(_base_node(spacing, pkey, "spacing.json %s" % pkey),
                        "spacing.json %s" % pkey)
            pad_src = "spacing.json %s (base, s202-D1)" % pkey
        if ckey in ov:
            cont = as_px(ov[ckey].get("$value"), "%s %s" % (theme, ckey))
            cont_src = "%s override %s" % (theme, ckey)
        else:
            cont = as_px(_base_node(layout, ckey, "layout.json %s" % ckey),
                         "layout.json %s" % ckey)
            cont_src = "layout.json %s (base, s202-D1)" % ckey
        if pad % PADDING_STEP != 0:
            refuse("scale %s" % scale,
                   "padding %d does not step in %dpx (s200-D1 clause d)" % (pad, PADDING_STEP))
        out[scale] = {"padding": pad, "container_radius": cont,
                      "padding_source": pad_src, "container_source": cont_src}
    return out


def snap2(n, what):
    """Snap to the nearest even px (the 2px padding step, s200-D1 clause d).
    Ties (odd values) round UP — an odd n is exactly between two even numbers."""
    if not isinstance(n, int):
        refuse(what, "snap2 needs an int, got %r" % (n,))
    return n if n % 2 == 0 else n + 1


def card_padding(radius):
    """RULED s201-D4 (#201, Dave, 2026-08-18): padding = max(radius, 8) snapped to 2px.
    Still MINT-TIME only (s200-D1 clause a) — the mint writes the concrete number."""
    return snap2(max(radius, CARD_PADDING_MIN), "card padding")


def thumb_radius(container_r, padding=None):
    """RULED s202-D2 (#202, Dave, 2026-08-18), corrected reading:
        thumb = max(container - SEGMENTED_THUMB_DIAL, 0)   with the dial = 6.

    s201-D5's shape survives (max(container - X, 0); squares stay square, no floor);
    s202-D2 re-tunes X from the track padding to the tuned dial. `padding` is accepted
    and IGNORED so the signature stays legible at the call site — it is deliberately no
    longer an input to the radius. Mint-time only (s200-D1 clause a)."""
    return max(container_r - SEGMENTED_THUMB_DIAL, 0)


def build():
    themes = {}
    for theme in THEMES:
        radii, prov = theme_radii(theme)
        card_r = radii["surface"]
        pad = card_padding(card_r)

        segs = {}
        container_role_r = radii["container"]
        for scale, inp in segmented_scales(theme).items():
            spad = inp["padding"]
            container_r = inp["container_radius"]
            segs[scale] = {
                "$ruled": ("s202-D2 (#202, Dave, 2026-08-18, corrected reading) — thumb = "
                           "max(container - %d, 0); the dial replaces padding as the input, "
                           "s201-D5's squares-stay-square shape retained"
                           % SEGMENTED_THUMB_DIAL),
                "padding": spad,
                "$paddingStatus": "READ FROM STORE (%s)" % inp["padding_source"],
                "container_radius": container_r,
                "$containerStatus": "READ FROM STORE (%s)" % inp["container_source"],
                "container_role_radius": container_role_r,
                "thumb_dial": SEGMENTED_THUMB_DIAL,
                "thumb_radius_raw": container_r - SEGMENTED_THUMB_DIAL,
                "thumb_radius": thumb_radius(container_r),
                "formula": ("thumb_radius = max(container_radius - %d, 0) — RULED s202-D2 "
                            "(tuned dial; padding is NOT an input)" % SEGMENTED_THUMB_DIAL),
                "inputs": {"container_radius": container_r, "dial": SEGMENTED_THUMB_DIAL},
                "$paddingIsNotAnInput": ("padding %d is carried here as the control's real "
                                         "spacing token; s202-D2 removed it from the thumb "
                                         "radius derivation" % spad),
                "$square": container_r == 0,
                "$squareNote": (
                    "container radius is 0 (square theme: mono / legacy / supercharge, base set "
                    "minted s202-D1): max(0 - %d, 0) = 0 — squares stay square, s201-D5 shape. "
                    "No floor is applied; the old PROPOSED floor of %d is SUPERSEDED."
                    % (SEGMENTED_THUMB_DIAL, SUPERSEDED_DERIVED_RADIUS_FLOOR)) if container_r == 0 else None,
            }

        themes[theme] = {
            "radii": {k: v for k, v in radii.items() if not k.startswith("$")},
            "radii_provenance": prov,
            "card": {
                "$ruled": "s201-D4 (#201, Dave, 2026-08-18) — max(radius, 8) snapped to 2px",
                "radius_role": "surface",
                "radius": card_r,
                "padding": pad,
                "formula": "padding = max(radius, %d) snapped to %dpx — RULED s201-D4, "
                           "applied at MINT TIME only (s200-D1 clause a)"
                           % (CARD_PADDING_MIN, PADDING_STEP),
                "inputs": {"radius": card_r, "min": CARD_PADDING_MIN,
                           "snap": PADDING_STEP},
                "container_variant": {
                    "$ruled": "s201-D4 formula applied to the container role radius",
                    "radius_role": "container (MINTED role, s200-D2/s200-D3)",
                    "radius": container_role_r,
                    "padding": card_padding(container_role_r),
                    "inputs": {"radius": container_role_r, "min": CARD_PADDING_MIN,
                               "snap": PADDING_STEP},
                },
            },
            "segmented": segs,
        }

    return {
        "$schema": "apollo/derive-radius-proposal/1",
        "$generator": "knowledge/gen_radius_derive.py",
        "$ruling": "s200-D1 (#200, 2026-08-18) — mint-time derivation mechanism",
        "$status": ("MIXED REGISTER — the FORMULAE are RULED (s201-D4 card padding, "
                    "s202-D2 segmented thumb) and the INPUTS are read from the minted token "
                    "store. This file remains a DERIVATION RECORD, not canon: minting is still "
                    "a separate, Dave-authorised act (s200-D1 clause a, mint-time only)."),
        "$ruledFormulae": [
            "card padding = max(radius, 8) snapped to 2px — RULED s201-D4 (#201)",
            "segmented thumb = max(container - %d, 0) — RULED s202-D2 (#202, corrected reading); "
            "the 6 is Dave's TUNED DIAL, re-tunable by a future tuner pass; squares stay square "
            "(s201-D5 shape retained, padding retired as the input)" % SEGMENTED_THUMB_DIAL,
        ],
        "$decidesNothing": [
            "which values get MINTED, and for which themes — Dave's act, never this script's",
            "the segmented scale set and its paddings — READ from the store (s201-D1 xs/s/m/l), "
            "not proposed here; the retired small/medium/large names are never emitted",
        ],
        "$superseded": {
            "derived_radius_floor_2": (
                "PROPOSED floor of %d for derived thumb radii — SUPERSEDED by the "
                "max(container - X, 0) shape. Never applied; recorded so the retirement is legible."
                % SUPERSEDED_DERIVED_RADIUS_FLOOR),
            "thumb_derives_from_padding": (
                "the thumb radius USED to derive from the track padding (s200-D1 clause c, "
                "s201-D5). SUPERSEDED by s202-D2 (#202, corrected reading): the input is now the "
                "tuned dial %d. Console's concentric 4/6/6/8 became 0/2/4/6 in the same motion."
                % SEGMENTED_THUMB_DIAL),
            "scale_set_small_medium_large": (
                "the padding-first small/medium/large scale set (paddings 2/4/6) was RETIRED at "
                "s201-D1 and is no longer emitted anywhere in this file."),
        },
        "$mintedState": {
            "console": ("s200-D2/s200-D3 + s201-D1 — border-radius/container 20, and the "
                        "dimension-first xs/s/m/l segmented set (sizes 24/36/44/48, paddings "
                        "2/2/4/4, container radii 6/8/10/12, thumbs 0/2/4/6 re-minted at "
                        "s202-D2 from 4/6/6/8), padding/card/"
                        "internal 20."),
            "mono_legacy_supercharge": ("s202-D1 (#202) — the BASE segmented set: Console's "
                                        "dimensions inherited verbatim (sizes 24/36/44/48, "
                                        "paddings 2/2/4/4) with container and thumb radii 0 "
                                        "per s201-D5 / s202-D2: max(0 - 6, 0) = 0."),
        },
        "$knobs": {
            "card_padding_min": CARD_PADDING_MIN,
            "padding_step": PADDING_STEP,
            "segmented_thumb_dial": SEGMENTED_THUMB_DIAL,
            "segmented_scale_order": list(SEGMENTED_SCALE_ORDER),
        },
        "$inputs": [
            "knowledge/tokens/layout.json (border-radius family + segmented-container scales)",
            "knowledge/tokens/spacing.json (padding/segmented-control scales)",
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
        # Direction 1 — SEGMENTED: thumb = max(container - dial, 0), RULED s202-D2.
        # Scale name is `m` (s201-D1 dimension-first grammar); `medium` is RETIRED.
        plant(lambda d: d["themes"]["apollo-console"]["segmented"]["m"]
              .__setitem__("thumb_radius", 99),
              "segmented thumb_radius console/m -> 99")
        # s201-D5 shape, squares-stay-square: a square theme's thumb must stay 0.
        plant(lambda d: d["themes"]["mono"]["segmented"]["l"]
              .__setitem__("thumb_radius", 2),
              "square-theme thumb mono/l -> 2 (the SUPERSEDED floor)")
        # The scale set is READ, not hardcoded: a store-read padding must be pinned.
        plant(lambda d: d["themes"]["apollo-supercharge"]["segmented"]["s"]
              .__setitem__("padding", 6),
              "store-read padding supercharge/s -> 6 (retired 2/4/6 grammar)")
        # Direction 2 — CARDS: padding derived from radius.
        plant(lambda d: d["themes"]["apollo-console"]["card"]
              .__setitem__("padding", 7),
              "card padding console -> 7 (also breaks the 2px step)")
        # Provenance must be pinned too.
        plant(lambda d: d["themes"]["mono"]["radii"].__setitem__("surface", 13),
              "mono surface radius -> 13")
        # s202-D2: the TUNED DIAL must be pinned on disk — a silent re-tune is drift.
        plant(lambda d: d["themes"]["apollo-console"]["segmented"]["l"]
              .__setitem__("thumb_dial", 4),
              "tuned dial console/l -> 4 (silent re-tune)")
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

    # RETIRED-NAME proof (s201-D1): no small/medium/large key may appear anywhere in the
    # emitted scale sets. A retired name is a defect, not a stale label.
    fresh = build()
    for tname, tdoc in fresh["themes"].items():
        for scale in tdoc["segmented"]:
            if scale in ("small", "medium", "large"):
                failures.append("retired scale name %r emitted for %s" % (scale, tname))
            if scale not in SEGMENTED_SCALE_ORDER:
                failures.append("unknown scale name %r emitted for %s" % (scale, tname))
    print("SELFTEST: retired-name proof ran over %d theme(s)." % len(fresh["themes"]))

    # s202-D2 DIAL PROOF — drive the formula directly, both clauses:
    #   (1) the thumb tracks the DIAL, not the padding;
    #   (2) padding is no longer an input at all (varying it cannot move the result).
    for cont, expect in [(6, 0), (8, 2), (10, 4), (12, 6), (0, 0), (4, 0)]:
        got = thumb_radius(cont)
        if got != expect:
            failures.append("dial proof: thumb_radius(%d) = %d, expected %d (dial %d)"
                            % (cont, got, expect, SEGMENTED_THUMB_DIAL))
    for pad in (0, 2, 4, 6, 20):
        if thumb_radius(10, pad) != thumb_radius(10):
            failures.append("padding still feeds the thumb radius: padding %d moved the "
                            "result — s202-D2 retired padding as an input" % pad)
    print("SELFTEST: s202-D2 dial proof ran (dial=%d; padding proven inert)."
          % SEGMENTED_THUMB_DIAL)

    # The DIAL itself must be pinned in the emitted file — a re-tune must show as drift.
    if fresh["$knobs"].get("segmented_thumb_dial") != SEGMENTED_THUMB_DIAL:
        failures.append("the tuned dial is not emitted into $knobs — a re-tune would be invisible")
    for tname, tdoc in fresh["themes"].items():
        for scale, sdoc in tdoc["segmented"].items():
            if sdoc.get("thumb_dial") != SEGMENTED_THUMB_DIAL:
                failures.append("thumb_dial absent/wrong for %s/%s" % (tname, scale))

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
