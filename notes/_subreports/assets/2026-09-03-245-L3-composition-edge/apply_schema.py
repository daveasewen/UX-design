#!/usr/bin/env python3
"""L3 #245 — PROPOSED schema fragment: `groupsWith` beside `mustNotNeighbour` in
knowledge/components/meta.schema.json (line 216, the `#/definitions/edge` form).

⛔ NEVER writes the live schema. Writes ONLY:
  knowledge/_tmp/l3-245/groupsWith.schema.fragment.json   the one property, on its own
  knowledge/_tmp/l3-245/meta.schema.proposed.json         the live schema + the fragment, BY ADDITION
  knowledge/_tmp/l3-245/meta.schema.proposed.diff         unified diff live -> proposed
Text surgery on ONE anchor (the mustNotNeighbour line inside `edges.properties`); refuses if the
anchor is not found exactly once; Draft7Validator.check_schema before writing (L2's apply_schema shape).
Schema changes are Dave's: template-dashboard-bento.meta.json:154 — "that is a SCHEMA change and is
his, not a worker lane's."
"""
import difflib, json, os, sys
import jsonschema

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LIVE = os.path.join(ROOT, "knowledge", "components", "meta.schema.json")
OUT = os.path.dirname(os.path.abspath(__file__))

ANCHOR = '        "mustNotNeighbour": { "type": "array", "items": { "$ref": "#/definitions/edge" } },\n'
FRAGMENT = {
    "groupsWith": {
        "type": "array",
        "items": {"$ref": "#/definitions/edge"},
        "description": (
            "PROPOSED #245 L3 (s234-D4, Dave: 'grouping lives ONCE in the KG and is derived everywhere "
            "else'). The POSITIVE composition edge, the counterpart of mustNotNeighbour: this component "
            "shares a GROUP with the referenced component — a group being members that answer ONE "
            "question the user came with (rB, #234: nobody groups by content type). Same edge form as "
            "every other entry ({ref: <node-id>|null, $note}); ref:null where the partner is not a node "
            "in the grammar (a group has no node-id today) — flagged for Dave's eye, never invented. "
            "Consumers DERIVE from it: the rails grouping dial (gen_bento_matrix_217.py), rule 7b, the "
            "composition gate. Never copy the fact into a second home."
        ),
    }
}
NEW_LINE = ('        "groupsWith": ' + json.dumps(FRAGMENT["groupsWith"], ensure_ascii=False) + ',\n')


def main():
    live_text = open(LIVE, encoding="utf-8").read()
    n = live_text.count(ANCHOR)
    if n != 1:
        print("REFUSED: anchor found %d times, need exactly 1" % n)
        return 2
    proposed_text = live_text.replace(ANCHOR, ANCHOR + NEW_LINE)
    proposed = json.loads(proposed_text)
    jsonschema.Draft7Validator.check_schema(proposed)
    assert "groupsWith" in proposed["properties"]["edges"]["properties"]
    keys = list(proposed["properties"]["edges"]["properties"].keys())
    assert keys.index("groupsWith") == keys.index("mustNotNeighbour") + 1, keys
    open(os.path.join(OUT, "groupsWith.schema.fragment.json"), "w", encoding="utf-8").write(
        json.dumps(FRAGMENT, indent=2, ensure_ascii=False) + "\n")
    open(os.path.join(OUT, "meta.schema.proposed.json"), "w", encoding="utf-8").write(proposed_text)
    diff = "".join(difflib.unified_diff(
        live_text.splitlines(True), proposed_text.splitlines(True),
        "knowledge/components/meta.schema.json (LIVE)",
        "knowledge/_tmp/l3-245/meta.schema.proposed.json (PROPOSED)", n=2))
    open(os.path.join(OUT, "meta.schema.proposed.diff"), "w", encoding="utf-8").write(diff)
    added = [l for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    print("anchor line (live): %d" % (live_text[:live_text.index(ANCHOR)].count("\n") + 1))
    print("diff: +%d / -%d lines (by addition)" % (len(added), len(removed)))
    print("live schema sha256 unchanged: %s" % __import__("hashlib").sha256(open(LIVE, "rb").read()).hexdigest()[:16])
    print("wrote fragment, proposed schema, diff -> %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
