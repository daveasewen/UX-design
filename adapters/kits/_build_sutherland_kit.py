#!/usr/bin/env python3
"""_build_sutherland_kit.py — REPO SIDE (not part of the kit). Derives the Sutherland kit's data files and adapters/sutherland-react.json
from the Apollo metas, so nothing in them is typed by hand. Run from the repo root:

    python3 adapters/kits/_build_sutherland_kit.py --write

Writes (repo-relative):
  adapters/sutherland-react.json                       the first manifest (4 empty rows, nothing mapped)
  adapters/kits/sutherland-react/manifest.json          the starter the Copilot agent fills
  adapters/kits/sutherland-react/parts.json             the parts list (roles, props, slots, states, events)
  adapters/kits/sutherland-react/apollo-tokens.json     semantic token paths by name (no values)
  adapters/kits/sutherland-react/schema.json            a copy of adapters/schema.json

Dry by default: no flag prints what it would write. #312 lane N1 (s311-D7).
Not a gate; not wired. Re-run it when a cohort meta changes, then re-run the gate.
"""
import glob
import importlib.util
import json
import os
import shutil
import sys

KITS = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(KITS, "sutherland-react")
ROOT = os.path.abspath(os.path.join(KITS, "..", ".."))
KNOW = os.path.join(ROOT, "knowledge")
COMP = os.path.join(KNOW, "components")
ADAPTERS = os.path.join(ROOT, "adapters")
TODAY = "2026-10-01"

# the four metas that carried an empty codeBindings placeholder slot (2026-06-22, all TODO, no Sutherland
# name in any of them) first, then cohort one (L's brief, #312) by nearest slug. #314 SW: "switch" now finds
# its own meta (s313-D56, Dave: "Four parts" — "it asks for a switch, not for the second tree inside
# selection controls"); it pointed at the selection-controls family before the split
BOUND = ["cards", "list-items", "status-indicator", "table"]
COHORT_ONE = [
    ("button", "button"), ("tabs", "tabs"), ("table", "table"), ("date picker", "date-picker"),
    ("metric", "metric"), ("menus", "dropdown"), ("accordion", "accordion"), ("slider", "slider"),
    ("switch", "switch"), ("text input", "input-fields"), ("select", "dropdown"),
    ("dialog", "modals"), ("tooltip", "tooltip"), ("pagination", "pagination"),
    ("notification", "notifications"),
]
SEMANTIC_FILES = ["semantic-colour.json", "spacing.json", "typography.json", "typography-composites.json",
                  "elevation.json", "icon-scale.json", "layout.json", "motion.json", "opacity.json"]
HOLE = {"enum": "enum", "boolean": "boolean", "string": "string", "number": "number",
        "array": "data", "object": "data", "node": "node", "function": "handler"}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def metas():
    out = {}
    for p in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
        stem = os.path.basename(p)[:-len(".meta.json")]
        if stem.startswith("EXAMPLE-"):
            continue
        out[stem] = load(p)
    return out


def states_of(m):
    sm = m.get("stateModel")
    if isinstance(sm, dict) and isinstance(sm.get("states"), list):
        return {s: (sm.get(s) if isinstance(sm.get(s), str) else None) for s in sm["states"]}
    for p in m.get("props", []):
        if p.get("name") in ("state", "tabState", "itemState") and p.get("type") == "enum":
            return {v: None for v in p.get("values", [])}
    return {}


def events_of(m):
    b = m.get("behaviour")
    if isinstance(b, dict) and isinstance(b.get("events"), list):
        return list(b["events"])
    return []


def part_entry(slug, m):
    props = []
    for p in m.get("props", []):
        if not isinstance(p, dict) or "name" not in p:
            continue
        row = {"name": p["name"], "type": p.get("type"), "hole": HOLE.get(p.get("type"), "string")}
        if p.get("values"):
            row["values"] = list(p["values"])
        if "default" in p:
            row["default"] = p["default"]
        if p.get("$note"):
            row["note"] = p["$note"][:240]
        props.append(row)
    slots = []
    sl = m.get("slots")
    if isinstance(sl, dict):
        for name, spec in sl.items():
            if name.startswith("$") or not isinstance(spec, dict):
                continue
            slots.append({"name": name, "required": bool(spec.get("required")), "use": (spec.get("use") or "")[:240],
                          "accepts": spec.get("accepts")})
    return {
        "slug": slug,
        "name": m.get("name"),
        "role": m.get("provides"),
        "category": m.get("category"),
        "kind": m.get("kind"),
        "purpose": (m.get("purpose") or "")[:400],
        "variants": [v.get("name") for v in m.get("variants", []) if isinstance(v, dict)],
        "props": props,
        "slots": slots,
        "states": states_of(m),
        "events": events_of(m),
        "metaFile": "knowledge/components/%s.meta.json" % slug,
    }


def binding_from_meta(slug, m, legacy):
    props = []
    for p in m.get("props", []):
        if not isinstance(p, dict) or "name" not in p:
            continue
        row = {"apollo": p["name"], "theirs": None, "hole": HOLE.get(p.get("type"), "string")}
        if row["hole"] == "enum":
            row["values"] = {v: None for v in p.get("values", [])}
        row["source"] = None
        props.append(row)
    slots = []
    if isinstance(m.get("slots"), dict):
        for name, spec in m["slots"].items():
            if not name.startswith("$") and isinstance(spec, dict):
                slots.append({"apollo": name, "theirs": None, "kind": None, "source": None})
    b = {
        "apollo": {"meta": slug},
        "theirs": {"component": None, "import": None, "file": None},
        "props": props,
        "slots": slots,
        "status": "unverified",
        "source": None,
        "$legacy": legacy,
        "$notes": "Row opened #312 N1. %s carried an empty codeBindings placeholder slot (2026-06-22, every field TODO); it is kept verbatim under $legacy and holds no Sutherland name. Every name on the Sutherland side is null: nothing has been read and nothing is mapped. The kit at adapters/kits/sutherland-react/ fills it on the machine that has Sutherland's source." % ("knowledge/components/%s.meta.json" % slug),
    }
    return b


def build():
    ms = metas()
    all_slugs = sorted(ms)
    roles = sorted(load(os.path.join(KNOW, "roles.json"))["roles"].keys())
    provides = {s: m["provides"] for s, m in ms.items() if isinstance(m.get("provides"), str)}

    # ---- the manifest (repo) ----
    bindings = []
    for slug in BOUND:
        legacy = ms[slug].get("codeBindings", {}).get("sutherland-react")
        bindings.append(binding_from_meta(slug, ms[slug], legacy))
    unmapped = [{"apollo": s, "reason": "no Sutherland component has been read for this part yet (the kit fills it)",
                 "fallback": "none"} for s in all_slugs if s not in BOUND]
    manifest = {
        "$schema": "./schema.json",
        "$model": "Apollo adapter manifest for HSBC Sutherland (React). s311-D7: Apollo governs, theirs renders. Each binding maps one Apollo part to the Sutherland component that renders it; `null` means not read yet, never guessed; status climbs only on evidence (rendered needs a side-by-side render on record; accepted needs Dave's word). The unmapped list names every Apollo part this file does not bind. Apollo has no Sutherland mapping yet: no Sutherland component, prop or import name is known. Written #312 N1; four of its rows (cards, list-items, status-indicator, table) replace empty codeBindings placeholder slots from 2026-06-22 that read TODO and named nothing; those slots stay in the metas until the first release whose gate reads this file. Fill it with the kit at adapters/kits/sutherland-react/ on a machine that has Sutherland's source; validate with python3 knowledge/_validate_adapter.py.",
        "manifest": {"schemaVersion": "1.0", "written": TODAY, "by": "#312 lane N1 (Fable); no Sutherland source read",
                     "rulings": ["s311-D7", "s311-D9"],
                     "$notes": "Seeds to reconcile at fill time, not carried as rows here because they name Figma variables, not Sutherland's code: knowledge/tokens/_manifests/sutherland-diffs.json (brand and semantic mode diffs) and sutherland-fixtures.json."},
        "library": {"id": "sutherland-react", "name": "HSBC Sutherland (React component library)", "runtime": "react",
                    "package": None, "version": None, "source": {"repo": None, "commit": None, "readOn": None},
                    "$notes": "package, version and source stay null until the manifest is filled beside Sutherland's source (ADR-0008: Sutherland is a consumer and the first live-fire test, never the template)."},
        "bindings": bindings,
        "tokens": {
            "resolver": {
                "name": "apollo-sutherland-react",
                "version": "2025.10",
                "description": "DTCG resolver: Apollo's semantic set first, Sutherland's set laid over it. Sutherland's sources are empty until their token file is read; the map below then says which of their names land on which Apollo semantic token. The Figma-mode diffs in knowledge/tokens/_manifests/sutherland-diffs.json are the seed to reconcile against, not a source.",
                "sets": {
                    "apollo-semantic": {"sources": [{"$ref": "knowledge/tokens/%s" % f} for f in SEMANTIC_FILES],
                                        "description": "Apollo's semantic tier (s311-D8 moves these to DTCG 2025.10; the paths stay)."},
                    "sutherland": {"sources": [], "description": "Their token source file(s), cited once read."},
                },
                "resolutionOrder": [{"$ref": "#/sets/apollo-semantic"}, {"$ref": "#/sets/sutherland"}],
            },
            "map": [],
        },
        "unmapped": {
            "$why": "Four parts have a row (cards, list-items, status-indicator, table: they once carried an empty placeholder slot), every Sutherland name in them null, nothing mapped; every other Apollo meta is listed here by slug with no fallback declared, so a composed screen for this library is refused until someone decides, part by part, that Apollo's own render stands in.",
            "items": unmapped,
        },
    }

    # ---- the parts list (kit) ----
    chosen, seen = [], set()
    for slug in BOUND:
        chosen.append((slug, "once carried an empty codeBindings placeholder slot (TODO, no Sutherland name)"))
        seen.add(slug)
    aliases = {}
    for asked, slug in COHORT_ONE:
        aliases.setdefault(slug, []).append(asked)
        if slug in seen:
            continue
        seen.add(slug)
        chosen.append((slug, "cohort one"))
    parts = []
    for slug, why in chosen:
        e = part_entry(slug, ms[slug])
        e["why"] = why
        if aliases.get(slug):
            e["askedAs"] = aliases[slug]
        parts.append(e)
    parts_doc = {
        "$model": "The Apollo parts to map, pulled from their metas by adapters/kits/_build_sutherland_kit.py (nothing typed by hand). Each part: its slug (the binding key), role, props with the hole each becomes, slots, states, events, and the meta file they came from. `allSlugs` is every Apollo part by slug so the checker can hold the unmapped list complete; `provides` is slug -> role for every part that has one; `roles` is the fenced role vocabulary (s252-D1).",
        "written": TODAY,
        "order": "The first four once carried an empty codeBindings placeholder slot (2026-06-22, every field TODO, no Sutherland name); nothing about them is known on the Sutherland side. Then cohort one in Dave's order; `askedAs` records the name he used when it differs from the slug: 'menus' and 'select' both resolve to dropdown (the non-native family and the native variant of one meta), 'switch' to selection-controls (its switch variant), 'text input' to input-fields, 'dialog' to modals (its dialog variant), 'notification' to notifications.",
        "roles": roles,
        "parts": parts,
        "provides": provides,
        "allSlugs": all_slugs,
    }

    # ---- the token names (kit) ----
    spec = importlib.util.spec_from_file_location("_validate_dtcg", os.path.join(KNOW, "_validate_dtcg.py"))
    dtcg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dtcg)
    files, _ = dtcg.corpus_files(KNOW)
    tokens, groups, per_file = dtcg.build_spine(files)
    tok = sorted(p for p, (f, _n, _t) in tokens.items() if not p.startswith("color."))
    grp = sorted(g for g in groups if not g.startswith("color."))
    by_type = {}
    for p, (f, _n, t) in tokens.items():
        if not p.startswith("color."):
            by_type.setdefault(t or "untyped", 0)
            by_type[t or "untyped"] += 1
    tokens_doc = {
        "$model": "Apollo's SEMANTIC token paths, names only, for the kit checker to resolve token rows against. A row's `apollo` is written as a DTCG alias: {text.default}. A path with light/dark children is a group and a legal target (the mode resolves at render). The primitive palette (color.*) is left out on purpose: a Sutherland token maps onto a semantic rung, never onto a palette swatch (ADR-0008).",
        "written": TODAY,
        # the real relative path: since s311-D8 the dark context lives at tokens/modes/dark/<base>.json
        # and a basename would print the base file twice (#312 lane V)
        "files": [os.path.relpath(f, ROOT) for f in files if not os.path.basename(f).startswith("colour")],
        "countByType": by_type,
        "tokens": tok,
        "groups": grp,
    }

    # ---- the starter manifest (kit): the repo manifest with cohort one's bindings pre-seeded ----
    starter = json.loads(json.dumps(manifest))
    starter["manifest"]["by"] = "starter written by adapters/kits/_build_sutherland_kit.py, #312 N1; to be filled by the Copilot agent on Dave's work machine"
    starter["$model"] = ("STARTER. " + starter["$model"] + " In this starter every part in parts.json has an empty row with every Sutherland-side name null (nothing is mapped yet); "
                         "the agent fills the nulls from Sutherland's source, moves what has no match into the row's `unmapped` with a reason, and leaves status 'unverified'.")
    bound = {b["apollo"]["meta"] for b in starter["bindings"]}
    for e in parts:
        if e["slug"] in bound:
            continue
        b = binding_from_meta(e["slug"], ms[e["slug"]], None)
        del b["$legacy"]
        b["$notes"] = "Seeded from %s by _build_sutherland_kit.py; every Sutherland-side name is null until read." % e["metaFile"]
        starter["bindings"].append(b)
        bound.add(e["slug"])
    starter["unmapped"]["items"] = [r for r in starter["unmapped"]["items"] if r["apollo"] not in bound]
    starter["unmapped"]["$why"] = ("The %d parts in parts.json carry binding rows (all unverified, Sutherland side null until read); every other Apollo meta is listed here with no fallback declared." % len(bound))

    return manifest, parts_doc, tokens_doc, starter


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    write = "--write" in argv
    manifest, parts_doc, tokens_doc, starter = build()
    outputs = [
        (os.path.join(ADAPTERS, "sutherland-react.json"), dump(manifest)),
        (os.path.join(HERE, "manifest.json"), dump(starter)),
        (os.path.join(HERE, "parts.json"), dump(parts_doc)),
        (os.path.join(HERE, "apollo-tokens.json"), dump(tokens_doc)),
    ]
    for path, text in outputs:
        print("%s %s (%d bytes)" % ("WRITE" if write else "would write", os.path.relpath(path, ROOT), len(text.encode("utf-8"))))
        if write:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
    src, dst = os.path.join(ADAPTERS, "schema.json"), os.path.join(HERE, "schema.json")
    print("%s %s (copy of adapters/schema.json)" % ("WRITE" if write else "would write", os.path.relpath(dst, ROOT)))
    if write:
        shutil.copyfile(src, dst)
    print("bindings %d · starter bindings %d · parts %d · unmapped %d · tokens %d · groups %d"
          % (len(manifest["bindings"]), len(starter["bindings"]), len(parts_doc["parts"]),
             len(manifest["unmapped"]["items"]), len(tokens_doc["tokens"]), len(tokens_doc["groups"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
