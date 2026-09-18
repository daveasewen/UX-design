#!/usr/bin/env python3
"""s282-D5 — re-home the 4 moved rule nodes and mint the 3 new ones in _rule_nodes.json.

HAND-EDIT of a generated file, and RULING-SHAPED: gen_kg_rules.py would do this, and it is
BANNED for this lane (it deletes the 76 hand-authored restsOn lines, s281-D3/s281-D6). So
the four moved rules' `file` and `definedIn` target are re-pointed at logos.md, the
artefact node for logos.md is minted, and logo26-008/009/010 enter with their index text
verbatim. The 76 restsOn lines are asserted intact before and after.
"""
import json, pathlib

K = pathlib.Path("/sessions/tender-hopeful-allen/mnt/UX-design/knowledge")
P = K/"_rule_nodes.json"
d = json.loads(P.read_text(encoding="utf-8"))
idx = {r["id"]: r for r in json.loads((K/"guidelines"/"_rules-index.json").read_text(encoding="utf-8"))["rules"]}

restsOn_before = sum(1 for e in d["edges"] if e["type"] == "restsOn")
nodes_before, edges_before = len(d["nodes"]), len(d["edges"])

MOVED = ["logo26-001", "va25-015", "va25-016", "va25-017"]
NEW = ["logo26-008", "logo26-009", "logo26-010"]
ART = "artefact:knowledge/guidelines/logos.md"
OLDART = {"brand-refresh-assets.md": "artefact:knowledge/guidelines/brand-refresh-assets.md",
          "visual-assets.md": "artefact:knowledge/guidelines/visual-assets.md"}

# 1. the artefact node for logos.md, minted in the shape of its siblings
assert not any(n["id"] == ART for n in d["nodes"])
anchor = next(i for i, n in enumerate(d["nodes"]) if n["id"] == OLDART["visual-assets.md"])
d["nodes"].insert(anchor + 1, {"id": ART, "type": "artefact", "label": "logos.md",
                               "fam": "rules", "docOf": "rules"})

# 2. re-home the four moved rules
rehomed = []
for n in d["nodes"]:
    if n.get("ruleId") in MOVED:
        assert n["file"] == idx[n["ruleId"]]["file"] or idx[n["ruleId"]]["file"] == "logos.md"
        rehomed.append((n["ruleId"], n["file"], "logos.md")); n["file"] = "logos.md"
for e in d["edges"]:
    if e["type"] == "definedIn" and e["s"].replace("rule:", "") in MOVED:
        e["t"] = ART
assert len(rehomed) == 4, rehomed

# 3. mint the three new rules, text VERBATIM from the regenerated index
last = max(i for i, n in enumerate(d["nodes"]) if n.get("ruleId") == "logo26-001")
for k, rid in enumerate(NEW):
    r = idx[rid]
    d["nodes"].insert(last + 1 + k, {
        "id": f"rule:{rid}", "type": "rule", "label": rid, "fam": "rules", "ruleId": rid,
        "file": r["file"], "destinyFull": r["destinyFull"], "text": r["rule"],
        "destiny": r["destiny"]})
    d["edges"].append({"s": f"rule:{rid}", "t": ART, "type": "definedIn", "fam": "rules"})

d["$description"] += (
    " HAND-EDIT 2026-09-18 under s282-D5 (#282 lane LL): logo26-001, va25-015, va25-016 and "
    "va25-017 moved file to logos.md (their definedIn re-pointed at the new "
    "artefact:knowledge/guidelines/logos.md node) and logo26-008/009/010 minted from the "
    "regenerated _rules-index.json, because gen_kg_rules.py is BANNED for that lane — it "
    "would delete the hand-authored restsOn block. RULING-SHAPED: the route is the "
    "conductor's, the rules are Dave's.")

restsOn_after = sum(1 for e in d["edges"] if e["type"] == "restsOn")
assert restsOn_after == restsOn_before == 75, (restsOn_before, restsOn_after)
P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("nodes:", nodes_before, "->", len(d["nodes"]), "| edges:", edges_before, "->", len(d["edges"]))
print("restsOn intact:", restsOn_after)
print("rehomed:", rehomed)
