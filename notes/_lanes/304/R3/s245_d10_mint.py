#!/usr/bin/env python3
"""s245_d10_mint.py ROOT — enact s245-D10 (#245, Dave, 2026-09-03) on the Console override set.

Dave: "The radii is only for console". The ruling's own numbers (ruled text in
knowledge/_rulings.json, s245-D10): control 6 (store 8), surface 8 (store 20), container 12
(store 20); segmented container/thumb xs 4/2, s 6/4, m 8/6, l 10/6, thumb = max(container -
padding, 0); padding NOT touched; default + indicator unchanged; concentric law and s200-D1
clause a untouched. "minting the Console theme tokens through the generator, nothing typed by
hand": the INPUT radii are the ruling's numbers; every THUMB is computed by
gen_radius_derive.thumb_radius() from the store's own padding and must equal the ruling's
readout or this script refuses; padding/card/internal is re-derived by gen_radius_derive
.card_padding() from the new surface radius (s201-D4, RULED: "max(border-radius/surface, 8)
snapped to 2px is now the RULED mint-time derivation for padding/card/internal").

Idempotent: a second run prints ALREADY and writes nothing. Byte-preserving: the file round-trips
through json.dumps(indent=2, ensure_ascii=False) + "\\n" identically (measured #304 R3).
Only $value changes; each $note gains a sentence BY ADDITION (s183-D1 / s188-D2).
"""
import json, os, sys
if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
K = os.path.join(ROOT, "knowledge")
sys.path.insert(0, K)
import gen_radius_derive as g  # noqa: E402  (read-only import: functions only)

P = os.path.join(K, "tokens", "themes", "apollo-console.overrides.json")
src = open(P, encoding="utf-8").read()
doc = json.loads(src)
assert json.dumps(doc, indent=2, ensure_ascii=False) + "\n" == src, "round-trip not byte-identical; refuse"
ov = doc["overrides"]

TAG = "s245-D10 (#245, Dave, 2026-09-03; enacted #304 R3)"
RULED_INPUTS = {  # the ruling's numbers, verbatim
    "border-radius/control": 6, "border-radius/surface": 8, "border-radius/container": 12,
    "border-radius/segmented-container/xs": 4, "border-radius/segmented-container/s": 6,
    "border-radius/segmented-container/m": 8, "border-radius/segmented-container/l": 10,
}
RULED_THUMBS = {"xs": 2, "s": 4, "m": 6, "l": 6}   # the ruling's readout, checked not typed

plan = {}
for k, v in RULED_INPUTS.items():
    plan[k] = (v, "RE-MINTED %d (was %%d) by %s — THE RADIUS CANDIDATE SET FROM THE TUNER IS RULED "
                  "FOR THE CONSOLE THEME ONLY; Dave: “The radii is only for console”. "
                  "Source reviews/RADIUS-TUNER-2026-09-03-v1.html." % (v, TAG))
for sc, want in RULED_THUMBS.items():
    pad = ov["padding/segmented-control/%s" % sc]["$value"]
    cont = RULED_INPUTS["border-radius/segmented-container/%s" % sc]
    got = g.thumb_radius(cont, pad, sc)
    if got != want:
        sys.exit("REFUSE: derived thumb %s = %d but the ruling reads %d" % (sc, got, want))
    plan["border-radius/segmented-thumb/%s" % sc] = (got, (
        "RE-DERIVED %d (was %%d) by %s — DERIVED, NOT TYPED: gen_radius_derive.thumb_radius"
        "(container %d, padding %d, '%s') = max(%d - %d, 0) = %d, equal to the ruling's readout. "
        "Padding untouched per the ruling." % (got, TAG, cont, pad, sc, cont, pad, got)))
cp = g.card_padding(RULED_INPUTS["border-radius/surface"])
plan["padding/card/internal"] = (cp, (
    "RE-DERIVED %d (was %%d) as a CONSEQUENCE of %s re-minting border-radius/surface 20 -> 8: "
    "s201-D4 (RULED) makes max(border-radius/surface, 8) snapped to 2px the mint-time derivation "
    "for this token; gen_radius_derive.card_padding(8) = %d. Consumed by nothing in canon at #304 "
    "(_gate_minted_consumption.py names it), so no pixel moves." % (cp, TAG, cp)))

changed = []
for k, (v, note) in plan.items():
    node = ov[k]
    old = node["$value"]
    if old == v and TAG in node.get("$note", ""):
        continue
    if old == v:
        sys.exit("REFUSE: %s already %s but carries no %s note — investigate" % (k, v, TAG))
    node["$value"] = v
    node["$note"] = node.get("$note", "") + " || " + (note % old)
    changed.append("%s %s -> %s" % (k, old, v))

if not changed:
    print("ALREADY — s245-D10 values present in", os.path.relpath(P, ROOT)); sys.exit(0)
open(P, "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
print("WROTE", os.path.relpath(P, ROOT)); [print("  " + c) for c in changed]
