#!/usr/bin/env python3
"""#311 lane C0 — s305-D17/D18/D19/D58 in knowledge/components/meta.schema.json (round-trips byte-exact at indent 2 + newline)."""
import json
P = "knowledge/components/meta.schema.json"
raw = open(P, encoding="utf-8").read()
s = json.loads(raw)
assert json.dumps(s, indent=2, ensure_ascii=False) + "\n" == raw, "schema no longer round-trips; stop"
props = s["properties"]["props"]
props["description"] = ("A part's SETTINGS. s305-D19 + s305-D58 (Dave, #305): a name is a setting OR a slot, never both - a setting takes a kind "
                        "of data (bindsData), a slot takes a kind of part (slots.<n>.accepts). Draft 7 cannot compare keys across two members, so "
                        "the same-name refusal lives in knowledge/_probe_registry/probe_meta_schema.py (arm SAME-NAME). s305-D17: a part's own words "
                        "are a setting marked ownText, never a separate text part inside it.")
it = props["items"]["properties"]
it["ownText"] = {
    "type": "boolean",
    "description": "s305-D17 (Dave, #305 call 16, \"yes\"): this setting carries the part's OWN WORDS - the button's label, the header's title, the "
                   "breadcrumbs' trail - so the gate checks them with the part (length, wrap, the 44px target, the name a screen reader hears). "
                   "A screen supplies them here, never as a separate text part placed inside the part. Only a string, a number or an array "
                   "(a list whose entries carry words) can be marked; `$items` says what one entry holds."}
it["bindsData"] = {"$ref": "#/definitions/bindsData"}
props["items"]["if"] = {"required": ["ownText"], "properties": {"ownText": {"const": True}}}
props["items"]["then"] = {"properties": {"type": {"enum": ["string", "number", "array"]}}}
s["definitions"]["bindsData"] = {
    "description": "s305-D19 (Dave, #305 call 18, \"yes\"): DATA IS A SETTING BOUND TO A DATA SHAPE. `capability` names the kind of data the setting "
                   "takes (the vocabulary the slots' accepts.capability used before the rule, so the chooser and the graph read one word); `shape` "
                   "is an ADDRESS into knowledge/shapes.json (a closed store, s254-D2: a lane never adds a value) and is present when the part "
                   "has a shape of record. A setting with bindsData must not share its name with a slot (probe arm SAME-NAME); an unknown shape "
                   "is refused by the same probe (arm SHAPE-UNKNOWN).",
    "type": "object", "required": ["capability"], "additionalProperties": False, "patternProperties": {"^\\$": {}},
    "properties": {"capability": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                   "shape": {"type": "string"}}}
acc = s["definitions"]["slotEntry"]["properties"]["accepts"]["properties"]
acc["provides"] = {
    "description": "s305-D18 (Dave, #305 call 17, \"yes\"): the slot accepts parts BY WHAT THEY PROVIDE - ADDRESSES into knowledge/roles.json "
                   "`roles` (the twelve adopted roles, s252-D1), never a list of part names (s140-D1). First used by the bento wall's `tiles`. "
                   "An unknown role is refused by knowledge/_probe_registry/probe_meta_schema.py (arm ROLE-UNKNOWN).",
    "type": "array", "items": {"type": "string"}, "minItems": 1}
sl = s["properties"]["slots"]
sl["description"] += (" s305-D19 + s305-D58 (Dave, #305): A SLOT ONLY EVER HOLDS ANOTHER PART - it takes a kind of part (accepts.tier, "
                      "accepts.kind or accepts.provides); a name that takes only a kind of data is a setting with bindsData instead, and a "
                      "name is never both (probe arm SAME-NAME).")
open(P, "w", encoding="utf-8").write(json.dumps(s, indent=2, ensure_ascii=False) + "\n")
print("schema written")
