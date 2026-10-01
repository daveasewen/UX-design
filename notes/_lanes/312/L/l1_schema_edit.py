#!/usr/bin/env python3
"""l1_schema_edit.py — #312 lane L1: add the four neutral-spec fields (s311-D4) to meta.schema.json.

By addition only. Appends `anatomy`, `states`, `emits`, `bindings` and the `$extracted` marker to
`properties`, four definitions, a `dependencies` clause (a drafted field needs its marker), and extends
the s210-D5 alias fence so an `aliasOf` meta can carry none of the four. Round-trips the file with
`json.dumps(indent=2, ensure_ascii=False) + '\\n'` (byte-exact on the untouched text; proven before the edit).

USAGE: python3 notes/_lanes/312/L/l1_schema_edit.py [--check]
  --check   dry run: print what would change, write nothing.
"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SCHEMA = os.path.join(ROOT, "knowledge", "components", "meta.schema.json")

HOLE = "^\\{(props|state)\\.[A-Za-z0-9_.-]+\\}$"
FOUR = ["anatomy", "states", "emits", "bindings"]

DEFINITIONS = {
    "specHole": {
        "description": "s311-D4 (#311, Dave; #312 lane L1): a HOLE in the neutral spec — `{props.<name>}` is filled from a setting at render time, `{state.<name>}` from the machine's current state. The string form is the whole value; a hole is never embedded inside a longer literal (the emitter substitutes the value, not a substring).",
        "type": "string",
        "pattern": HOLE
    },
    "anatomyNode": {
        "description": "s311-D4: ONE ELEMENT of a part's anatomy tree. `part` is the part's name (lower-kebab, unique in the tree; the extraction resolves every name to an element in the snippet, s311-D4 phase-1 gate). `tag` is the HTML element. `attrs` are the attributes the emitter writes, literal or a hole (`\"aria-selected\": \"{state.selected}\"` is how a STATE sets an attribute; `\"{props.label}\"` is a prop hole). `aria` holds `role` and the `aria-*` attributes apart from the rest so the APG checklist (_validate_apg_keys.py, phase 3) reads them in one place. `slot` names the meta `slots` key this element is the home of. `text` is the element's own text content, literal or a hole. `children` is the ordered subtree. `$`-notes allowed. Part names are checked against Open UI's anatomy research where a page exists (proposal § 05).",
        "type": "object",
        "required": ["part", "tag"],
        "properties": {
            "part": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "tag": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "attrs": {
                "type": "object",
                "additionalProperties": {"type": ["string", "number", "boolean", "null"]}
            },
            "aria": {
                "type": "object",
                "patternProperties": {"^(role|aria-[a-z]+)$": {"type": ["string", "number", "boolean", "null"]}},
                "additionalProperties": False
            },
            "slot": {"type": "string"},
            "text": {"type": "string"},
            "children": {"type": "array", "items": {"$ref": "#/definitions/anatomyNode"}}
        },
        "patternProperties": {"^\\$": {}},
        "additionalProperties": False
    },
    "stateTransition": {
        "description": "s311-D4: one arrow of the part's state machine, Zag-shaped — `from` a state name (or `*` for any), `on` an event (a DOM event, a key name from `keys`, or an emitted event), `to` a state name, optional `guard` (a condition in words or as a `{props.x}` / `{state.y}` test; phase 1 records it, nothing evaluates it yet).",
        "type": "object",
        "required": ["from", "on", "to"],
        "properties": {
            "from": {"type": "string"},
            "on": {"type": "string"},
            "to": {"type": "string"},
            "guard": {"type": "string"}
        },
        "patternProperties": {"^\\$": {}},
        "additionalProperties": False
    },
    "emittedEvent": {
        "description": "s311-D4: one event the part FIRES (a CustomEvent on the host element in E1/E2; a wrapper output in E3). `name` is the event name (lower-kebab; the convention is an `apollo-` prefix so a consumer never confuses it with a DOM listener). `detail` maps each payload key to its type as a word (string, number, boolean, object, array, or a shape address into knowledge/shapes.json); `{}` is an event with no payload. Optional `when` says in one sentence what fires it. This is NOT `behaviour.events`, which stays the list of DOM listeners the snippet attaches (s245-D4).",
        "type": "object",
        "required": ["name", "detail"],
        "properties": {
            "name": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "detail": {"type": "object", "additionalProperties": {"type": "string"}},
            "when": {"type": "string"}
        },
        "patternProperties": {"^\\$": {}},
        "additionalProperties": False
    }
}

PROPERTIES = {
    "anatomy": {
        "description": "s311-D4 (Dave, #311, 2026-10-01, by click: 'In the meta: four new fields'; #312 lane L1 adds the field, L2 drafts it): the part's ANATOMY — the element tree the HTML emitter (E1, phase 2) renders and the Lit element (E2, phase 3) mirrors in light DOM. A tree of anatomyNode ({part, tag, attrs, aria, slot?, text?, children[]}). State attributes are written as holes (`\"aria-expanded\": \"{state.open}\"`), prop holes as `\"{props.label}\"`. The root is the host element. OPTIONAL in phase 1 (s311-D9: added, nothing renamed, nothing renders from it yet); a phase-2 cohort makes it the source its snippet is generated from (s311-D3, behind _validate_roundtrip.py). Drafted from the snippet markup by knowledge/components/extract_spec.py with the `$extracted` marker; `reviewed: false` until Dave has ruled the tree by eye on the cohort's review page. The s210-D5 alias fence bans it on an `aliasOf` meta.",
        "$ref": "#/definitions/anatomyNode"
    },
    "states": {
        "description": "s311-D4: the part's STATE MACHINE as data, the shape Zag machines take (proposal § 05): `states` the state names, `initial` the one it starts in, `transitions` the arrows ({from, on, to, guard?}), `keys` the keyboard map (key name → action word, e.g. ArrowRight: next, Home: first; the APG pattern for the role is the checklist). `transitions` and `keys` are optional inside the field (a passive part has none) but the field itself counts toward full coverage. Distinct from `stateModel` (#305 call 14), which stays the catalogue's prose list of what the part SHOWS in each state; `states` is what it DOES. Extracted from the snippet's <style> state selectors and inline script; carries `$extracted` until reviewed.",
        "type": "object",
        "required": ["states", "initial"],
        "properties": {
            "states": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"type": "string"}},
            "initial": {"type": "string"},
            "transitions": {"type": "array", "items": {"$ref": "#/definitions/stateTransition"}},
            "keys": {"type": "object", "additionalProperties": {"type": "string"}}
        },
        "patternProperties": {"^\\$": {}},
        "additionalProperties": False
    },
    "emits": {
        "description": "s311-D4: the events the part FIRES, with payload types — [{name, detail{}}] (emittedEvent). `behaviour.events` stays beside it as the listener list (s245-D4); the two never merge. The wrappers (E3, phase 4) generate their outputs from this field; the phase-2 gate fires every emitted event at least once in a Playwright run. An empty array is a positive declaration (the part fires nothing), never 'unknown'. Carries `$extracted` until reviewed.",
        "type": "array",
        "items": {"$ref": "#/definitions/emittedEvent"}
    },
    "bindings": {
        "description": "s311-D4: the snippet's #token-manifest `vars` moved into the meta as DTCG references — {\"--tab-ink\": \"{color.text.default}\"}. Keys are the component's CSS custom properties; values are `{group.token}` references (dot-joined path segments; until s311-D8's DTCG generator lands, the resolver reads them against today's slash paths in knowledge/tokens/ by swapping `.` for `/`). Every binding must resolve to a token in knowledge/tokens/ — a GATE rule in the extraction report (s311-D4 phase-1 gate), not a schema rule, because the schema cannot see the token store. In phase 2 gen_snippet_tokens and gen_theme_cascade read this field instead of the snippet and the AUTO-THEMES block regenerates byte-equal. This is the typed successor of the 727 prose entries under `tokens` (M2 § 3); `tokens` is NOT renamed or removed in phase 1. Carries `$extracted` until reviewed.",
        "type": "object",
        "patternProperties": {
            "^--[A-Za-z0-9_-]+$": {"type": "string", "pattern": "^\\{[^{}\\s]+\\}$"},
            "^\\$": {}
        },
        "additionalProperties": False
    },
    "$extracted": {
        "description": "s311-D4 / s311-D9 (#312 lane L1): the DRAFT MARKER on the four neutral-spec fields. Written by knowledge/components/extract_spec.py when it drafts anatomy/states/emits/bindings from the snippet: `by` names the writer (script and lane), `date` the day, `reviewed` false until Dave has ruled the cohort's trees by eye on its review page — nothing drafted stands before that (brief: 'a draft meta carries reviewed:false until then'). Optional `source` is the snippet path read, `sha` the tree it was read at, `fields` which of the four were drafted. The `dependencies` clause makes the marker REQUIRED on any meta carrying one of the four, so no draft can pass as authored.",
        "type": "object",
        "required": ["by", "date", "reviewed"],
        "properties": {
            "by": {"type": "string", "minLength": 1},
            "date": {"type": "string", "pattern": "^20[0-9]{2}-[0-9]{2}-[0-9]{2}$"},
            "reviewed": {"type": "boolean"},
            "source": {"type": "string"},
            "sha": {"type": "string", "pattern": "^[0-9a-f]{7,40}$"},
            "fields": {"type": "array", "uniqueItems": True, "items": {"enum": FOUR}}
        },
        "patternProperties": {"^\\$": {}},
        "additionalProperties": False
    }
}


def main():
    check = "--check" in sys.argv[1:]
    raw = open(SCHEMA, encoding="utf-8").read()
    s = json.loads(raw)
    assert json.dumps(s, indent=2, ensure_ascii=False) + "\n" == raw, "schema does not round-trip byte-exact; stop"
    changes = []
    for k, v in DEFINITIONS.items():
        if k not in s["definitions"]:
            s["definitions"][k] = v; changes.append("definitions.%s" % k)
    for k, v in PROPERTIES.items():
        if k not in s["properties"]:
            s["properties"][k] = v; changes.append("properties.%s" % k)
    # the s210-D5 alias fence: an aliasOf meta carries none of the four
    fence = next(a for a in s["allOf"] if a.get("if", {}).get("required") == ["aliasOf"])
    banned = fence["then"]["not"]["anyOf"]
    have = {tuple(b["required"]) for b in banned}
    for f in FOUR + ["$extracted"]:
        if (f,) not in have:
            banned.append({"required": [f]}); changes.append("aliasFence+%s" % f)
    if "$comment" in fence and "s311-D4" not in fence["$comment"]:
        fence["$comment"] += " · #312 lane L1 (s311-D4): the four neutral-spec fields (anatomy, states, emits, bindings) and their $extracted marker join the fence — the spec of an alias lives in the meta it points at, so an alias draws none of them."
        changes.append("aliasFence.$comment")
    dep = s.setdefault("dependencies", {})
    for f in FOUR:
        if f not in dep:
            dep[f] = ["$extracted"]; changes.append("dependencies.%s" % f)
    if "$comment" not in s:
        s["$comment"] = "s311-D4 / #312 lane L1: `dependencies` (Draft 7) — any of the four neutral-spec fields on a meta REQUIRES the `$extracted` marker, so a drafted field is never mistaken for a reviewed one; the marker's `reviewed` flag is what Dave's ruling flips. To hand-author one of the four later, write the marker with `by` naming the author and `reviewed: true` with the ruling in a `$why`."
        changes.append("$comment")
    out = json.dumps(s, indent=2, ensure_ascii=False) + "\n"
    print("changes: %d" % len(changes))
    for c in changes:
        print("  + " + c)
    if check:
        print("--check: nothing written (%d → %d bytes)" % (len(raw.encode()), len(out.encode())))
        return 0
    open(SCHEMA, "w", encoding="utf-8").write(out)
    print("written: %s (%d → %d bytes)" % (SCHEMA, len(raw.encode()), len(out.encode())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
