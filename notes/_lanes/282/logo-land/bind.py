#!/usr/bin/env python3
"""s282-D5 step 4 — RE-BIND the 8 logo nodes. HAND-AUTHORED, and that is RULING-SHAPED.

The ratified generator (notes/_lanes/277/icons-propose/gen_kg_icons.py --land --ratified
s277-D4) was run first and DID NOT pick the new rules up: `governedBy` is in its
NULL_ONLY_TYPES tuple and its only governedBy route is `declare(...)`, which always writes
t=null. GOVERNS_LOGO_RX is used solely to COUNT rulings that name a logo .svg for the
declared-null `why` string — measured: the regen changed exactly 6 lines, "0 rules whose
file is logos.md" -> "7" and "0 rulings name a logo .svg" -> "8", and drew no edge. So the
edges below are hand-authored in the same shape as the file's existing edges.
"""
import json, pathlib, collections

P = pathlib.Path("/sessions/tender-hopeful-allen/mnt/UX-design/knowledge/_logo_nodes.json")
d = json.loads(P.read_text(encoding="utf-8"))

HEX = [f"logo:hexagon-{t}-{c}" for t in ("dark", "light") for c in ("colour", "mono")]
MB  = [f"logo:masterbrand-{t}-{c}" for t in ("dark", "light") for c in ("colour", "mono")]

before_edges = len(d["edges"])
before_gov = [e for e in d["edges"] if e["type"] == "governedBy"]
assert all(e["t"] is None for e in before_gov), "expected all governedBy declared-null"
print("governedBy edges before:", len(before_gov), "all null:", True)

# drop the declared nulls this ruling resolves
d["edges"] = [e for e in d["edges"] if e["type"] != "governedBy"]

WHY_HEX = ("s282-D5 (Dave 2026-09-18, his own export) rules the hexagon alone legal on the "
           "nav-rail head, app tile and favicon (Create Direct approval AND 'HSBC' in view, "
           "va25-016's conditions) and in responsive layouts at tablet-portrait and mobile "
           "where the Masterbrand does not fit. Blocker B3 is closed: the standard is ours "
           "and it is in logos.md")
WHY_MAST = ("s282-D5 (Dave 2026-09-18) rules the masthead default = full colour on both "
            "grounds in all four themes (q2 a x4); the rule names the variant va25-015's "
            "masthead contract requires")
WHY_CS = ("s282-D5 (Dave 2026-09-18) rules the digital vertical clear-space FLOOR: "
          ">= 0.25 x logo height snapped UP to the 4px grid (24->8 28->8 32->8 36->12 "
          "40->12). HORIZONTAL clear space is NOT stated and is NOT ruled")

def edge(s, t, why):
    return {"s": s, "t": t, "type": "governedBy", "fam": "assets",
            "ruling": "s282-D5", "authored": "hand", "why": why,
            "$note": "HAND-AUTHORED under s282-D5. The ratified generator cannot draw this "
                     "edge: governedBy is in its NULL_ONLY_TYPES tuple, so a regen restores "
                     "a declared null here. RULING-SHAPED — see the #282 lane LL report."}

new = []
for s in HEX:
    new.append(edge(s, "rule:logo26-010", WHY_HEX))
for s in MB:
    new.append(edge(s, "rule:logo26-008", WHY_MAST))
    new.append(edge(s, "rule:logo26-009", WHY_CS))
d["edges"].extend(new)

# the declared-null register: the governedBy entries are resolved and leave it
kept = [u for u in d["unresolved"] if u["type"] != "governedBy"]
resolved = [u for u in d["unresolved"] if u["type"] == "governedBy"]
d["unresolved"] = kept

d["edge_types"]["governedBy"] = (
    "RESOLVED 2026-09-18 by s282-D5 — declared-null-only from #277 until Dave ruled the "
    "logo rules into logos.md. 12 edges, all drawn, all HAND-AUTHORED (the generator's "
    "governedBy route only declares nulls). A regen will re-declare the nulls; re-apply "
    "notes/_lanes/282/logo-land/bind.py after any gen_kg_icons.py --land")
d["$description"] = (
    "RATIFIED _logo_nodes.json under s277-D4 (#277 lane RI; s269-D1 STEP 4). Regenerate "
    "with `gen_kg_icons.py --land --ratified s277-D4`; never hand-edit — EXCEPT the 12 "
    "`governedBy` edges, which s282-D5 (Dave 2026-09-18) resolved and which the generator "
    "cannot draw. Re-apply notes/_lanes/282/logo-land/bind.py after any regeneration.")
d["$s282-D5"] = {
    "ruled": "2026-09-18, Dave, on his own export notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json",
    "what": "the 4 hexagon nodes bind to rule:logo26-010 (hexagon-only); the 4 masterbrand "
            "nodes bind to rule:logo26-008 (masthead default) and rule:logo26-009 (clear-space floor)",
    "generatorVerdict": "gen_kg_icons.py --land --ratified s277-D4 was RUN FIRST and did not "
                        "pick the new rules up: governedBy is in NULL_ONLY_TYPES; the regen "
                        "changed 6 `why` lines only (0->7 rules whose file is logos.md, "
                        "0->8 rulings naming a logo .svg) and drew 0 edges",
    "rulingShaped": "the hand-authoring, and the widening of edge_types.governedBy from "
                    "DECLARED-NULL ONLY to a drawn type, are the conductor's choice of "
                    "route, not Dave's word",
    "resolvedNulls": [u["source"] for u in resolved],
}

P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
c = collections.Counter(e["type"] for e in d["edges"])
print("edges before/after:", before_edges, "->", len(d["edges"]))
print("by type:", dict(sorted(c.items())))
print("governedBy drawn:", sum(1 for e in d["edges"] if e["type"] == "governedBy" and e["t"]))
print("unresolved before/after:", len(kept) + len(resolved), "->", len(kept))
