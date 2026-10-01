#!/usr/bin/env python3
"""_validate_adapter.py — the ADAPTER MANIFEST gate (s311-D7, Apollo for other libraries).

s311-D7 (Dave, #311, 2026-10-01, by click on the recommendation): "Adapter manifest per
library, Apollo governs, theirs renders." s311-D9: the S2 schema starts now. This gate
reads every manifest under adapters/*.json against adapters/schema.json and the rules the
schema cannot state, and — given a composed screen and a library — refuses any part on
that screen with no binding and no declared Apollo-native fallback.

WHAT IT CHECKS (blocking)
  AD-001  shape: the manifest validates against adapters/schema.json (required keys,
          types, enums, patterns, no unknown keys). A small stdlib walker, not jsonschema,
          so the kit checker Dave carries to a machine without the repo gives the same
          verdict (its core is byte-identical to this file's; the selftest proves it).
  AD-002  every binding names exactly ONE Apollo meta (a slug of knowledge/components/
          <slug>.meta.json) or ONE role (a key of knowledge/roles.json). An unknown slug or
          role refuses, loud and named. Nothing is bound twice.
  AD-003  every Apollo prop a binding names is a prop that meta really declares.
  AD-004  the status ladder. unverified -> rendered ONLY with evidence.render (a
          side-by-side render on record) -> accepted ONLY with evidence.accepted (Dave's
          word and the date). A jump refuses. Dave's word at a lower status refuses too.
  AD-005  at rendered or accepted nothing is null (component, import, source, prop, slot).
  AD-006  an enum hole carries its values map; no other hole does. A null state or
          event is echoed in the binding's unmapped list with a reason.
  AD-007  every token row resolves to an Apollo token or group in knowledge/tokens/
          (the DTCG spine, via _validate_dtcg.build_spine) and is SEMANTIC: a primitive
          palette path (color.*) refuses (ADR-0008: never inherit a consumer's primitive).
  AD-008  the unmapped list is REQUIRED (schema) and COMPLETE: every meta in the corpus
          (knowledge/components/*.meta.json minus EXAMPLE-*) is either bound — by its own
          row, or by a row for the role it provides — or listed by slug with a reason and
          a declared fallback. Nothing is both. The corpus is the metas on disk, so the
          list goes stale the day a meta is added and the gate says so.
  AD-009  --screen: a composed screen's parts are its cn-<slug> scopes; each must be
          bound, or unmapped with fallback "apollo-native". A part unmapped with fallback
          "none", or absent from the manifest, refuses the screen for that library.

CONSUMERS
  * knowledge/_tests/test_gates.py runs `--selftest` (SELFTEST_ARMS) — a reader from day one.
  * knowledge/_build_all.py STEPS: the gate and its selftest, with ROUTE_ROWS rows.
  * OWED, NOT BUILT: the receipt mint (gen_provenance_receipt.py) recording which library
    rendered each part, and the release gate that reads this file in place of the four
    empty `codeBindings` placeholder slots still in cards / list-items / status-indicator /
    table metas (2026-06-22, every field TODO: they hold no Sutherland name and are not a
    mapping). They come OUT at the first release whose gate reads the manifest (N1 report).

Usage:  python3 knowledge/_validate_adapter.py                 # gate: every adapters/*.json
        python3 knowledge/_validate_adapter.py --manifest PATH # one file (any path)
        python3 knowledge/_validate_adapter.py --screen PAGE.html --library sutherland-react
        python3 knowledge/_validate_adapter.py --selftest      # plants 3 bad + clean controls
        python3 knowledge/_validate_adapter.py --json          # machine-readable result
Exit 0 pass · 1 fail · 2 bad invocation · 77 COULD-NOT-ASK (adapters/ or knowledge/components/ unreachable, e.g. an installed pack).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import argparse
import copy
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

KNOW = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(KNOW)
ADAPTERS = os.path.join(ROOT, "adapters")
SCHEMA = os.path.join(ADAPTERS, "schema.json")
KIT = os.path.join(ADAPTERS, "kits", "sutherland-react")
COMPONENTS = os.path.join(KNOW, "components")
ROLES = os.path.join(KNOW, "roles.json")

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


# ---- the REPO side: the context comes from the tree, not from a parts list ----

def meta_corpus(components=COMPONENTS):
    """slug -> meta dict, for every knowledge/components/*.meta.json except EXAMPLE-*."""
    out = {}
    for p in sorted(glob.glob(os.path.join(components, "*.meta.json"))):
        stem = os.path.basename(p)[:-len(".meta.json")]
        if stem.startswith("EXAMPLE-"):
            continue
        try:
            out[stem] = load_json(p)
        except Exception as exc:        # noqa: BLE001 - a meta that does not parse is another gate's red
            out[stem] = {"$unparseable": str(exc)}
    return out


def spine_paths(know=KNOW):
    """Every token + group path in the DTCG spine, via _validate_dtcg's own index."""
    spec = importlib.util.spec_from_file_location("_validate_dtcg", os.path.join(know, "_validate_dtcg.py"))
    dtcg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dtcg)
    files, _excluded = dtcg.corpus_files(know)
    tokens, groups, _per_file = dtcg.build_spine(files)
    return set(tokens) | set(groups)


def ctx_from_repo(know=KNOW):
    metas = meta_corpus(os.path.join(know, "components"))
    roles = set(load_json(os.path.join(know, "roles.json")).get("roles", {}).keys())
    providers, provides, meta_props = {}, {}, {}
    for slug, m in metas.items():
        meta_props[slug] = {p.get("name") for p in m.get("props", []) if isinstance(p, dict)}
        role = m.get("provides")
        if isinstance(role, str):
            provides[slug] = role
            providers.setdefault(role, []).append(slug)
    return {"slugs": set(metas), "roles": roles, "providers": providers, "provides": provides,
            "meta_props": meta_props, "tokens": spine_paths(know)}


def manifests(adapters=ADAPTERS):
    """The manifests the gate grades: adapters/*.json except schema.json. Kits are not graded
    here (a kit's manifest is a starter until it comes back and is filed as adapters/<id>.json)."""
    return sorted(p for p in glob.glob(os.path.join(adapters, "*.json"))
                  if os.path.basename(p) != "schema.json")


def gate(paths=None, ctx=None, as_json=False):
    schema = load_json(SCHEMA)
    ctx = ctx or ctx_from_repo()
    paths = manifests() if paths is None else paths
    ok_all, results = True, []
    print("adapter-manifest gate (s311-D7) — %d manifest(s) under adapters/" % len(paths))
    for p in paths:
        # the id-equals-stem rule holds for FILED manifests (adapters/<id>.json); a one-off
        # --manifest on any other path is graded on its content alone
        stem = os.path.basename(p)[:-5] if os.path.dirname(os.path.abspath(p)) == ADAPTERS else None
        try:
            manifest = load_json(p)
        except Exception as exc:        # noqa: BLE001
            print("  ⛔ %s: not valid JSON — %s" % (p, exc))
            ok_all = False
            results.append({"file": p, "ok": False, "errors": ["not valid JSON: %s" % exc]})
            continue
        errors, warnings, counts = validate_manifest(manifest, schema, ctx, stem)
        label = os.path.relpath(p, ROOT) if os.path.abspath(p).startswith(ROOT + os.sep) else p
        ok = report(errors, warnings, counts, label)
        ok_all &= ok
        results.append({"file": label, "ok": ok, "errors": errors,
                        "warnings": warnings, "counts": counts})
    if as_json:
        print(json.dumps({"ok": ok_all, "results": results}, indent=2))
    return ok_all


def screen_gate(page, library, ctx=None):
    path = os.path.join(ADAPTERS, library + ".json")
    if not os.path.isfile(path):
        print("⛔ no manifest for library %r at %s" % (library, os.path.relpath(path, ROOT)))
        return False
    ctx = ctx or ctx_from_repo()
    manifest = load_json(path)
    with open(page, encoding="utf-8") as fh:
        html = fh.read()
    refused, allowed = screen_check(html, manifest, ctx)
    for part, why in allowed:
        print("  ✓ %s — %s" % (part, why))
    for part, why in refused:
        print("  ⛔ REFUSED %s — %s" % (part, why))
    print("%s %s for %s — %d part(s) allowed, %d refused"
          % ("PASS" if not refused else "FAIL", os.path.relpath(page, ROOT) if page.startswith(ROOT) else page,
             library, len(allowed), len(refused)))
    return not refused


# ---- selftest: plants its fixtures in a tempdir; never writes into the repo ----

def _clean_fixture(ctx):
    """A minimal VALID manifest: cards bound by meta, the rest unmapped."""
    rest = sorted(ctx["slugs"] - {"cards"})
    return {
        "manifest": {"schemaVersion": "1.0", "written": "2026-10-01", "by": "selftest"},
        "library": {"id": "selftest-lib", "name": "Selftest", "runtime": "react", "package": None,
                    "version": None, "source": {"repo": None}},
        "bindings": [{
            "apollo": {"meta": "cards"},
            "theirs": {"component": None, "import": None},
            "props": [{"apollo": "type", "theirs": None, "hole": "enum", "values": {}}],
            "slots": [],
            "status": "unverified",
            "source": None,
        }],
        "tokens": {"resolver": {"name": "selftest", "sets": {"apollo": {"sources": [{"$ref": "knowledge/tokens/semantic-colour.json"}]}},
                                "resolutionOrder": [{"$ref": "#/sets/apollo"}]},
                   "map": [{"theirs": "--x", "apollo": "{text.default}", "status": "unverified", "source": None}]},
        "unmapped": {"$why": "selftest: only cards is bound",
                     "items": [{"apollo": s, "reason": "selftest", "fallback": "none"} for s in rest]},
    }


def selftest():
    schema = load_json(SCHEMA)
    ctx = ctx_from_repo()
    fails = []

    def arm(name, manifest, expect_fail, marker=None):
        errors, _w, _c = validate_manifest(manifest, schema, ctx, "selftest-lib")
        bit = bool(errors)
        hit = (marker is None) or any(marker in e for e in errors)
        ok = (bit == expect_fail) and (hit if expect_fail else True)
        print("  %s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else " — errors=%r" % errors[:3]))
        if not ok:
            fails.append(name)

    clean = _clean_fixture(ctx)
    arm("control: the clean fixture passes", clean, False)

    m = copy.deepcopy(clean); del m["unmapped"]
    arm("bite 1: a manifest with NO unmapped list refuses", m, True, "unmapped")

    m = copy.deepcopy(clean); m["bindings"].append({"apollo": {"role": "no-such-role"}, "theirs": {"component": None, "import": None},
                                                  "props": [], "slots": [], "status": "unverified", "source": None})
    arm("bite 2: an unknown role refuses, loud and named", m, True, "UNKNOWN ROLE")

    m = copy.deepcopy(clean); m["bindings"][0]["status"] = "accepted"
    arm("bite 3: a status jump to accepted with no evidence refuses", m, True, "STATUS JUMP")

    m = copy.deepcopy(clean); m["bindings"][0]["status"] = "rendered"
    arm("bite 3b: a jump to rendered with no render on record refuses", m, True, "STATUS JUMP")

    m = copy.deepcopy(clean); m["bindings"][0]["evidence"] = {"accepted": {"by": "Dave", "date": "2026-10-01"}}
    arm("bite 3c: Dave's word on an unverified binding refuses", m, True, "evidence.accepted")

    m = copy.deepcopy(clean); m["unmapped"]["items"].pop()
    arm("bite 4: an unmapped list that misses a meta refuses", m, True, "neither bound nor listed")

    m = copy.deepcopy(clean); m["unmapped"]["items"].append({"apollo": "cards", "reason": "x", "fallback": "none"})
    arm("bite 5: a meta both bound and unmapped refuses", m, True, "both bound and unmapped")

    m = copy.deepcopy(clean); m["tokens"]["map"][0]["apollo"] = "{color.primary}"
    arm("bite 6: a token row onto a primitive palette path refuses", m, True, "PRIMITIVE")

    m = copy.deepcopy(clean); m["tokens"]["map"][0]["apollo"] = "{text.no-such-rung}"
    arm("bite 7: a token row that resolves to nothing refuses", m, True, "does not resolve")

    m = copy.deepcopy(clean); m["bindings"][0]["apollo"] = {"meta": "no-such-meta"}
    m["unmapped"]["items"].append({"apollo": "cards", "reason": "x", "fallback": "none"})
    arm("bite 8: an unknown meta slug refuses", m, True, "UNKNOWN META")

    m = copy.deepcopy(clean); m["bindings"][0]["props"][0]["apollo"] = "no-such-prop"
    arm("bite 9: a prop the meta does not declare refuses", m, True, "is not a prop of meta")

    m = copy.deepcopy(clean); m["bindings"][0]["extra"] = 1
    arm("bite 10: an unknown key refuses (shape)", m, True, "unknown key")

    # the screen arm: cn-cards is bound; cn-button is unmapped fallback none -> refused;
    # flip button to apollo-native -> allowed.
    html = '<div class="cn-cards"></div><button class="cn-button c-button">x</button>'
    refused, _a = screen_check(html, clean, ctx)
    ok = [p for p, _ in refused] == ["button"]
    print("  %s bite 11: a screen using an unmapped part with fallback none is refused" % ("PASS" if ok else "FAIL"))
    if not ok:
        fails.append("bite 11")
    m = copy.deepcopy(clean)
    for row in m["unmapped"]["items"]:
        if row["apollo"] == "button":
            row["fallback"] = "apollo-native"
    refused, _a = screen_check(html, m, ctx)
    ok = refused == []
    print("  %s control: the same screen passes once button declares an Apollo-native fallback" % ("PASS" if ok else "FAIL"))
    if not ok:
        fails.append("screen control")

    # the real manifests on disk must pass (so the bites above are not pre-existing breakage)
    ok = gate(ctx=ctx)
    print("  %s control: every adapters/*.json on disk passes" % ("PASS" if ok else "FAIL"))
    if not ok:
        fails.append("disk control")

    # the kit: its core is byte-identical to this file's, and its checker passes the starter
    # manifest and bites a mutant, without the repo (run from a tempdir copy of the kit).
    kit_checker = os.path.join(KIT, "check_manifest.py")
    if os.path.isfile(kit_checker):
        mine = _core_region(os.path.abspath(__file__))
        theirs = _core_region(kit_checker)
        ok = mine is not None and mine == theirs
        print("  %s kit: check_manifest.py's CORE is byte-identical to this gate's" % ("PASS" if ok else "FAIL"))
        if not ok:
            fails.append("kit core drift")
        kit_schema = load_json(os.path.join(KIT, "schema.json"))
        ok = kit_schema == schema
        print("  %s kit: schema.json in the kit equals adapters/schema.json" % ("PASS" if ok else "FAIL"))
        if not ok:
            fails.append("kit schema drift")
        with tempfile.TemporaryDirectory(prefix="adapter-kit-") as tmp:
            import shutil
            kdir = os.path.join(tmp, "kit")
            shutil.copytree(KIT, kdir)
            r = subprocess.run([sys.executable, os.path.join(kdir, "check_manifest.py"), os.path.join(kdir, "manifest.json")],
                               capture_output=True, text=True, timeout=120)
            ok = r.returncode == 0 and "PASS" in r.stdout
            print("  %s kit: the starter manifest passes the kit checker outside the repo" % ("PASS" if ok else "FAIL"))
            if not ok:
                fails.append("kit starter")
                print(r.stdout[-600:], r.stderr[-300:])
            mut = load_json(os.path.join(kdir, "manifest.json"))
            del mut["unmapped"]
            with open(os.path.join(kdir, "mutant.json"), "w", encoding="utf-8") as fh:
                json.dump(mut, fh)
            r = subprocess.run([sys.executable, os.path.join(kdir, "check_manifest.py"), os.path.join(kdir, "mutant.json")],
                               capture_output=True, text=True, timeout=120)
            ok = r.returncode == 1 and "unmapped" in r.stdout
            print("  %s kit: the kit checker bites a mutant with no unmapped list" % ("PASS" if ok else "FAIL"))
            if not ok:
                fails.append("kit bite")
    else:
        print("  ⚠ kit checker absent at %s — kit arms skipped" % kit_checker)

    print("\nselftest: %d arm(s) failed" % len(fails) + (": " + ", ".join(fails) if fails else ""))
    return not fails


def _core_region(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    a, b = text.find("# ---- CORE START"), text.find("# ---- CORE END ----")
    return text[a:b] if a >= 0 and b > a else None


def main():
    ap = argparse.ArgumentParser(description="adapter-manifest gate (s311-D7)")
    ap.add_argument("--manifest", help="validate one manifest file (any path)")
    ap.add_argument("--screen", help="a composed screen (.html) to grade for --library")
    ap.add_argument("--library", help="the library id (adapters/<id>.json) a --screen is graded for")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(0 if selftest() else 1)
    if args.screen:
        if not args.library:
            print("⛔ --screen needs --library <id>")
            sys.exit(2)
        sys.exit(0 if screen_gate(args.screen, args.library) else 1)
    if not os.path.isfile(SCHEMA) or not os.path.isdir(COMPONENTS):
        # #173 / #230 class: a gate that cannot pass in one environment. An installed pack
        # ships knowledge/ without adapters/ (and a bare kit has no knowledge/), so the honest
        # verdict is the ruled third one — exit 77, COULD-NOT-ASK, the missing input named —
        # never a red about a question this run could not ask.
        import _could_not_ask as cna
        missing = "adapters/schema.json" if not os.path.isfile(SCHEMA) else "knowledge/components/"
        cna.refuse("adapter-manifest gate (s311-D7)", "%s is not reachable from %s — nothing can be graded here" % (missing, ROOT))
        sys.exit(cna.EXIT)
    paths = [args.manifest] if args.manifest else None
    sys.exit(0 if gate(paths, as_json=args.json) else 1)


if __name__ == "__main__":
    main()
