#!/usr/bin/env python3
"""check_manifest.py — checks an Apollo adapter manifest WITHOUT the Apollo repo.

Standard library only. Put it in the same folder as schema.json, parts.json,
apollo-tokens.json and the manifest, then:

    python3 check_manifest.py manifest.json

Exit 0 = the manifest is valid (the terminal says PASS and prints the counts).
Exit 1 = it is not; every problem is printed with the path into the file.

What it checks (the same rules the Apollo repo's gate applies):
  * shape, against schema.json (required keys, types, enums, patterns, no extra keys)
  * every binding names exactly one Apollo meta (a slug in parts.json) or one role
  * every Apollo prop named in a binding is a prop that meta really has
  * the status ladder: rendered needs evidence.render; accepted needs evidence.accepted
    (Dave's word) too; a jump is refused
  * at rendered or accepted, nothing may still be null
  * an enum hole carries a values map; other holes do not
  * a null state is echoed in unmapped.states with a reason
  * every token row points at an Apollo SEMANTIC token that exists (apollo-tokens.json);
    primitive palette paths (color.*) are refused
  * the unmapped list is present, names every Apollo meta the manifest does not bind,
    and names nothing twice

The core between the CORE START / CORE END markers is byte-identical to the one in
knowledge/_validate_adapter.py in the Apollo repo; the repo's selftest checks that.
"""
import json
import os
import re
import sys

# ---- CORE START (byte-identical in knowledge/_validate_adapter.py and the kit checker) ----
STATUS_RANK = {"unverified": 0, "rendered": 1, "accepted": 2}
PRIMITIVE_ROOTS = {"color"}      # the palette file: never a mapping target (ADR-0008)


def _type_ok(value, typ):
    if isinstance(typ, list):
        return any(_type_ok(value, t) for t in typ)
    if typ == "object":
        return isinstance(value, dict)
    if typ == "array":
        return isinstance(value, list)
    if typ == "string":
        return isinstance(value, str)
    if typ == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if typ == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if typ == "boolean":
        return isinstance(value, bool)
    if typ == "null":
        return value is None
    return True


def _deref(ref, root):
    node = root
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


def schema_check(instance, schema, root, path="$", out=None):
    """A small JSON-Schema walker: type, const, enum, pattern, minLength, minItems,
    required, properties, additionalProperties, items, $ref. Returns a list of
    'path: problem' strings. Not a full validator — it covers exactly the keywords
    adapters/schema.json uses, so the kit and the repo agree without a dependency."""
    out = [] if out is None else out
    if "$ref" in schema:
        schema = dict(_deref(schema["$ref"], root), **{k: v for k, v in schema.items() if k != "$ref"})
    if "type" in schema and not _type_ok(instance, schema["type"]):
        out.append("%s: expected %s, got %s" % (path, schema["type"], type(instance).__name__))
        return out
    if "const" in schema and instance != schema["const"]:
        out.append("%s: must be %r" % (path, schema["const"]))
    if "enum" in schema and instance not in schema["enum"]:
        out.append("%s: %r is not one of %s" % (path, instance, schema["enum"]))
    if isinstance(instance, str):
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            out.append("%s: %r does not match %s" % (path, instance, schema["pattern"]))
        if "minLength" in schema and len(instance) < schema["minLength"]:
            out.append("%s: must not be empty" % path)
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            out.append("%s: needs at least %d item(s)" % (path, schema["minItems"]))
        if "items" in schema:
            for i, item in enumerate(instance):
                schema_check(item, schema["items"], root, "%s[%d]" % (path, i), out)
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                out.append("%s: missing required key %r" % (path, key))
        props = schema.get("properties", {})
        for key, val in instance.items():
            if key in props:
                schema_check(val, props[key], root, "%s.%s" % (path, key), out)
            elif "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                if ap is False:
                    out.append("%s: unknown key %r" % (path, key))
                elif isinstance(ap, dict):
                    schema_check(val, ap, root, "%s.%s" % (path, key), out)
    return out


def _is_null_hole(binding):
    """True when the binding still carries an OPEN null: a name owed and not yet read. A null
    prop or slot that is echoed in the binding's unmapped list with a reason is a CLOSED gap,
    not a hole — their library has no counterpart, and that has been said."""
    t = binding.get("theirs", {})
    if t.get("component") is None or t.get("import") is None:
        return True
    if binding.get("source") is None:
        return True
    um = binding.get("unmapped", {}) if isinstance(binding.get("unmapped"), dict) else {}
    closed_props = {r.get("apollo") for r in um.get("props", []) if isinstance(r, dict)}
    closed_slots = {r.get("apollo") for r in um.get("slots", []) if isinstance(r, dict)}
    for p in binding.get("props", []):
        if p.get("theirs") is None and p.get("apollo") not in closed_props:
            return True
    for s in binding.get("slots", []):
        if (s.get("theirs") is None or s.get("kind") is None) and s.get("apollo") not in closed_slots:
            return True
    return False


def semantic_check(manifest, ctx, file_stem=None):
    """Rules the schema cannot state. ctx: slugs (set), roles (set), providers (role ->
    [slugs]), meta_props (slug -> set of prop names, may be partial), tokens (set of
    spine paths incl. groups). Returns (errors, warnings, counts)."""
    errors, warnings = [], []
    slugs, roles = ctx["slugs"], ctx["roles"]
    providers = ctx.get("providers", {})
    meta_props = ctx.get("meta_props", {})
    tokens = ctx.get("tokens")

    lib = manifest.get("library", {})
    if file_stem and lib.get("id") and lib["id"] != file_stem:
        errors.append("library.id %r must equal the file stem %r" % (lib["id"], file_stem))

    covered, seen_meta, seen_role = set(), set(), set()
    counts = {"bindings": 0, "named": 0, "unmapped": 0, "by_status": {"unverified": 0, "rendered": 0, "accepted": 0},
              "open_holes": 0, "token_rows": 0}
    for i, b in enumerate(manifest.get("bindings", [])):
        at = "$.bindings[%d]" % i
        if not isinstance(b, dict):
            continue
        counts["bindings"] += 1
        if isinstance(b.get("theirs"), dict) and b["theirs"].get("component"):
            counts["named"] += 1
        ap = b.get("apollo", {}) if isinstance(b.get("apollo"), dict) else {}
        keys = [k for k in ("meta", "role") if k in ap]
        if len(keys) != 1:
            errors.append("%s.apollo: exactly ONE of meta or role, got %s" % (at, keys or "neither"))
            continue
        if "meta" in ap:
            slug = ap["meta"]
            if slug not in slugs:
                errors.append("%s.apollo.meta: UNKNOWN META %r — not a slug in the parts list" % (at, slug))
            elif slug in seen_meta:
                errors.append("%s.apollo.meta: %r is bound twice" % (at, slug))
            seen_meta.add(slug)
            covered.add(slug)
            known = meta_props.get(slug)
            if known is not None:
                for j, p in enumerate(b.get("props", [])):
                    if isinstance(p, dict) and p.get("apollo") not in known:
                        errors.append("%s.props[%d].apollo: %r is not a prop of meta %r (its props: %s)"
                                      % (at, j, p.get("apollo"), slug, ", ".join(sorted(known)) or "none"))
        else:
            role = ap["role"]
            if role not in roles:
                errors.append("%s.apollo.role: UNKNOWN ROLE %r — not in the role list (%s)"
                              % (at, role, ", ".join(sorted(roles))))
            elif role in seen_role:
                errors.append("%s.apollo.role: %r is bound twice" % (at, role))
            else:
                covered.update(providers.get(role, []))
            seen_role.add(role)
            if b.get("props"):
                warnings.append("%s: a role binding carries props; props belong to a meta row (a role has none)" % at)

        status = b.get("status")
        ev = b.get("evidence", {}) if isinstance(b.get("evidence"), dict) else {}
        if status in counts["by_status"]:
            counts["by_status"][status] += 1
        rank = STATUS_RANK.get(status, -1)
        if rank >= 1 and not ev.get("render"):
            errors.append("%s.status: STATUS JUMP — %r needs evidence.render (a side-by-side render on record)" % (at, status))
        if rank >= 2 and not ev.get("accepted"):
            errors.append("%s.status: STATUS JUMP — accepted needs evidence.accepted (Dave's word and the date)" % at)
        if rank < 2 and ev.get("accepted"):
            errors.append("%s.evidence.accepted: present at status %r — only an accepted binding carries Dave's word" % (at, status))
        null_hole = _is_null_hole(b)
        if null_hole:
            counts["open_holes"] += 1
            if rank >= 1:
                errors.append("%s: status %r but a name is still null (component, import, source, a prop or a slot)" % (at, status))
        for j, p in enumerate(b.get("props", [])):
            if not isinstance(p, dict):
                continue
            if p.get("hole") == "enum" and not isinstance(p.get("values"), dict):
                errors.append("%s.props[%d]: an enum hole needs a `values` map (Apollo value -> theirs)" % (at, j))
            if p.get("hole") != "enum" and "values" in p:
                errors.append("%s.props[%d]: `values` is for enum holes only" % (at, j))
        um = b.get("unmapped", {}) if isinstance(b.get("unmapped"), dict) else {}
        echoed_states = {r.get("apollo") for r in um.get("states", []) if isinstance(r, dict)}
        for sname, how in (b.get("states") or {}).items():
            if how is None and sname not in echoed_states:
                errors.append("%s.states.%s: null, but not echoed in unmapped.states with a reason" % (at, sname))
        echoed_events = {r.get("apollo") for r in um.get("events", []) if isinstance(r, dict)}
        for ename, how in (b.get("events") or {}).items():
            if how is None and ename not in echoed_events:
                errors.append("%s.events.%s: null, but not echoed in unmapped.events with a reason" % (at, ename))

    tm = manifest.get("tokens", {}) if isinstance(manifest.get("tokens"), dict) else {}
    for i, row in enumerate(tm.get("map", []) if isinstance(tm.get("map"), list) else []):
        if not isinstance(row, dict):
            continue
        counts["token_rows"] += 1
        ref = row.get("apollo") or ""
        path = ref[1:-1] if ref.startswith("{") and ref.endswith("}") else ref
        root = path.split(".")[0]
        if root in PRIMITIVE_ROOTS:
            errors.append("$.tokens.map[%d].apollo: %s is a PRIMITIVE palette path — map onto a semantic token (ADR-0008)" % (i, ref))
        elif tokens is not None and path not in tokens:
            errors.append("$.tokens.map[%d].apollo: %s does not resolve to any Apollo token or group" % (i, ref))

    um = manifest.get("unmapped")
    if not isinstance(um, dict) or "items" not in um:
        errors.append("$.unmapped: REQUIRED and missing — a manifest must say what it does not map, even when that is nothing")
    else:
        listed = []
        for i, row in enumerate(um.get("items", []) if isinstance(um.get("items"), list) else []):
            if not isinstance(row, dict):
                continue
            s = row.get("apollo")
            listed.append(s)
            if s not in slugs:
                errors.append("$.unmapped.items[%d].apollo: UNKNOWN META %r" % (i, s))
            if s in covered:
                errors.append("$.unmapped.items[%d].apollo: %r is both bound and unmapped" % (i, s))
        counts["unmapped"] = len(listed)
        dupes = sorted({s for s in listed if listed.count(s) > 1})
        if dupes:
            errors.append("$.unmapped.items: listed twice: %s" % ", ".join(dupes))
        missing = sorted(slugs - covered - set(listed))
        if missing:
            errors.append("$.unmapped.items: %d Apollo meta(s) neither bound nor listed as unmapped: %s%s"
                          % (len(missing), ", ".join(missing[:12]), " …" if len(missing) > 12 else ""))
    return errors, warnings, counts


def screen_parts(html):
    """The parts a composed screen uses: its cn-<slug> scopes (lower-case)."""
    return sorted({m for m in re.findall(r"\bcn-([a-z0-9][a-z0-9-]*)", html)})


def screen_check(html, manifest, ctx):
    """Refuse any part on a composed screen with no binding and no declared
    Apollo-native fallback. Returns (refused, allowed) lists of (part, why)."""
    slugs = ctx["slugs"]
    lower = {s.lower(): s for s in slugs}
    providers = ctx.get("providers", {})
    provides = ctx.get("provides", {})          # slug -> role
    bound_meta, bound_role = set(), set()
    for b in manifest.get("bindings", []):
        ap = b.get("apollo", {})
        if "meta" in ap:
            bound_meta.add(ap["meta"])
        elif "role" in ap:
            bound_role.add(ap["role"])
    fallback = {}
    for row in (manifest.get("unmapped", {}) or {}).get("items", []):
        fallback[row.get("apollo")] = row.get("fallback")
    refused, allowed = [], []
    for part in screen_parts(html):
        slug = lower.get(part)
        if slug is None:
            allowed.append((part, "not an Apollo meta (a layout scope or a bare prefix) — not graded"))
            continue
        if slug in bound_meta:
            allowed.append((slug, "bound by meta"))
        elif provides.get(slug) in bound_role:
            allowed.append((slug, "bound by role %r" % provides[slug]))
        elif fallback.get(slug) == "apollo-native":
            allowed.append((slug, "unmapped, fallback apollo-native declared"))
        elif slug in fallback:
            refused.append((slug, "unmapped with fallback 'none' — no binding and no declared Apollo-native fallback"))
        else:
            refused.append((slug, "not in the manifest at all — neither bound nor unmapped"))
    return refused, allowed


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate_manifest(manifest, schema, ctx, file_stem=None):
    """Shape then meaning. Returns (errors, warnings, counts)."""
    errors = schema_check(manifest, schema, schema)
    sem_err, warnings, counts = semantic_check(manifest, ctx, file_stem)
    return errors + sem_err, warnings, counts


def ctx_from_parts(parts, tokens_doc):
    """Build the validation context from the kit's parts.json + apollo-tokens.json."""
    slugs = set(parts.get("allSlugs", []))
    providers, provides, meta_props = {}, {}, {}
    for p in parts.get("parts", []):
        slug = p["slug"]
        slugs.add(slug)
        meta_props[slug] = {pr["name"] for pr in p.get("props", [])}
        if p.get("role"):
            provides[slug] = p["role"]
    for slug, role in parts.get("provides", {}).items():
        provides.setdefault(slug, role)
    for slug, role in provides.items():
        providers.setdefault(role, []).append(slug)
    roles = set(parts.get("roles", [])) | set(providers)
    tokens = set(tokens_doc.get("tokens", [])) | set(tokens_doc.get("groups", [])) if tokens_doc else None
    return {"slugs": slugs, "roles": roles, "providers": providers, "provides": provides,
            "meta_props": meta_props, "tokens": tokens}


def report(errors, warnings, counts, label):
    for w in warnings:
        print("  ⚠ " + w)
    for e in errors:
        print("  ⛔ " + e)
    verdict = "PASS" if not errors else "FAIL"
    print("%s %s — binding rows %d (%d with their component named · unverified %d · rendered %d · accepted %d, %d with open holes) · unmapped %d · token rows %d · %d error(s), %d warning(s)"
          % (verdict, label, counts["bindings"], counts["named"], counts["by_status"]["unverified"], counts["by_status"]["rendered"],
             counts["by_status"]["accepted"], counts["open_holes"], counts["unmapped"], counts["token_rows"],
             len(errors), len(warnings)))
    return not errors
# ---- CORE END ----


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    manifest_path = argv[0]
    schema_path = os.path.join(here, "schema.json")
    parts_path = os.path.join(here, "parts.json")
    tokens_path = os.path.join(here, "apollo-tokens.json")
    for p in (manifest_path, schema_path, parts_path, tokens_path):
        if not os.path.isfile(p):
            print("⛔ missing file: %s (keep the kit folder together)" % p)
            return 1
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:      # noqa: BLE001 - a broken JSON file is the first thing to report
        print("⛔ %s is not valid JSON: %s" % (manifest_path, exc))
        return 1
    schema = load_json(schema_path)
    ctx = ctx_from_parts(load_json(parts_path), load_json(tokens_path))
    stem = os.path.splitext(os.path.basename(manifest_path))[0]
    stem = stem if stem != "manifest" else None     # the kit's working name is not the library id
    errors, warnings, counts = validate_manifest(manifest, schema, ctx, stem)
    ok = report(errors, warnings, counts, os.path.basename(manifest_path))
    if ok:
        print("Hand this file back as it is. Its library.id is %r; Apollo will file it as adapters/%s.json."
              % (manifest.get("library", {}).get("id"), manifest.get("library", {}).get("id")))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
