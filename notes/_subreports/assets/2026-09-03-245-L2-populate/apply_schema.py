#!/usr/bin/env python3
"""
apply_schema.py — #238 lane B. Applies behaviour.schema.fragment.json to a COPY of
knowledge/components/meta.schema.json by TEXT SURGERY on two anchors (so the diff against the
live file is the two edits and nothing else — a JSON re-dump would re-format 230 lines).

  python3 apply_schema.py <live meta.schema.json> <out path>

REFUSES (exit 2) if either anchor is not found exactly once, so a moved line 197 can never be
silently skipped [[unmatched-grep-is-not-an-absence]]. Checks the result parses and is a valid
Draft-07 schema before writing. ⛔ Never pointed at the live file by this lane — the live schema
is Dave's to change (v106 brief line 47).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FRAG = json.load(open(os.path.join(HERE, "behaviour.schema.fragment.json"), encoding="utf-8"))

OLD_PROP = '    "behaviour": { "description": "optional behavioural notes", "type": ["object", "array", "string"] },\n'
DEF_ANCHOR = ('        "$note": { "type": "string" }\n'
              '      }\n'
              '    }\n'
              '  },\n'
              '  "properties": {\n')


def indent(obj, n):
    txt = json.dumps(obj, indent=2, ensure_ascii=False)
    pad = " " * n
    return "\n".join((pad + ln) if ln else ln for ln in txt.splitlines())


def main():
    if len(sys.argv) != 3:
        print(__doc__); return 2
    src, out = sys.argv[1], sys.argv[2]
    text = open(src, encoding="utf-8").read()
    if text.count(OLD_PROP) != 1:
        print("REFUSED: the `behaviour` property line was found %d times, expected exactly 1 — "
              "meta.schema.json:197 has moved; re-anchor before applying" % text.count(OLD_PROP)); return 2
    if text.count(DEF_ANCHOR) != 1:
        print("REFUSED: the end-of-definitions anchor was found %d times, expected exactly 1" % text.count(DEF_ANCHOR)); return 2
    new_prop = '    "behaviour": ' + indent(FRAG["properties"]["behaviour"], 4).lstrip() + ",\n"
    new_def = ('        "$note": { "type": "string" }\n'
               '      }\n'
               '    },\n'
               '    "behaviourAddress": ' + indent(FRAG["definitions"]["behaviourAddress"], 4).lstrip() + "\n"
               '  },\n'
               '  "properties": {\n')
    text = text.replace(OLD_PROP, new_prop, 1).replace(DEF_ANCHOR, new_def, 1)
    try:
        obj = json.loads(text)
    except Exception as e:
        print("REFUSED: result is not JSON — %s" % e); return 2
    import jsonschema
    jsonschema.Draft7Validator.check_schema(obj)
    if "behaviourAddress" not in obj["definitions"] or "if" not in obj["properties"]["behaviour"]:
        print("REFUSED: edits did not land where expected"); return 2
    open(out, "w", encoding="utf-8").write(text)
    print("wrote %s (%d bytes; +behaviourAddress definition, behaviour property replaced)" % (out, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
