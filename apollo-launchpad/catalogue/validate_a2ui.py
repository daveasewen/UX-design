#!/usr/bin/env python3
"""Launchpad step one — the A2UI harness: the generated catalogue against the fetched A2UI v0.9.1 spec
(draft 2020-12), plus the mutation set that proves the harness bites (#312 lane C1, grown from the R5
probe notes/_lanes/304/R5/validate_a2ui.py + validate_mutations.py).

Needs jsonschema >= 4.18 with `referencing` (apollo-launchpad/requirements.txt; the seat's own python has
3.2, so use $HOME/.launchpad-venv/bin/python there). Spec files: a2ui-v0.9.1/ (FETCHED.txt has the hashes).

Checks, per catalogue:
  C1  the catalogue is a valid 2020-12 schema document (the metaschema does NOT descend into `components`,
      hence E0);
  C2  the inline-Catalog form (client_capabilities $defs/Catalog) on the {catalogId, components} projection;
  per entry:
  E0  the entry itself passes the 2020-12 metaschema;
  E1  a minimal instance (id, component, every required setting and slot) validates against the entry;
  E2  the same instance plus an unknown property is REJECTED (unevaluatedProperties holds);
  E3  an updateComponents message carrying the entry as root validates against server_to_client.json with
      catalog.json resolved to THIS catalogue;
  E4  a FULL instance (every setting and slot filled, optional ones too) validates, so every property's
      $ref is reached (R5's M2 only bit on a required property; the control catalogue is exempt);
  N1  an unknown component name is rejected through the same resolution (proves E3 resolves to ours);
  N2  a missing required slot is rejected.
Control: the official basic catalogue runs through the same checks first.

Run:  python validate_a2ui.py [--out <dir>]        writes <out>/a2ui-validation.json, exit 1 on any invalid entry
      python validate_a2ui.py --mutations          five one-change breaks of the dashboard catalogue, all must be CAUGHT
"""
import json, os, sys, copy, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "a2ui-v0.9.1")
OUT_DEFAULT = os.path.join(HERE, "out")
CATALOG_URI = "https://a2ui.org/specification/v0_9/catalog.json"   # what server_to_client's relative "catalog.json" resolves to
CT = "https://a2ui.org/specification/v0_9/common_types.json#/$defs/"

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

load = lambda p: json.load(open(p))
ct = load(os.path.join(SPEC, "json_common_types.json"))
s2c = load(os.path.join(SPEC, "json_server_to_client.json"))
caps = load(os.path.join(SPEC, "json_client_capabilities.json"))
basic = load(os.path.join(SPEC, "catalogs_basic_catalog.json"))


def registry(cat):
    res = lambda d: Resource.from_contents(d, default_specification=DRAFT202012)
    reg = Registry().with_resources([(ct["$id"], res(ct)), (s2c["$id"], res(s2c)), (caps["$id"], res(caps)),
                                     (CATALOG_URI, res(cat))])
    if cat.get("$id") and cat["$id"] != CATALOG_URI:
        reg = reg.with_resource(cat["$id"], res(cat))
    return reg


def errs(schema, inst, reg):
    v = Draft202012Validator(schema, registry=reg)
    return [("/".join(str(p) for p in e.absolute_path) or "(root)") + ": " + e.message[:160] for e in v.iter_errors(inst)]


def fill(sch):
    """A value that satisfies one property schema of an entry (settings are A2UI data; slots are ids)."""
    ref = sch.get("$ref", "")
    if ref.endswith("ChildList"):
        return ["child-1"]
    if ref.endswith("ComponentId"):
        return "child-1"
    if ref.endswith("DynamicString"):
        return "x"
    if ref.endswith("DynamicNumber"):
        return 1
    if ref.endswith("DynamicBoolean"):
        return True
    if ref.endswith("Action"):
        return {"event": {"name": "probe"}}
    if "enum" in sch:
        return sch["enum"][0]
    if "const" in sch:
        return sch["const"]
    for alt in sch.get("oneOf") or sch.get("anyOf") or []:
        if alt.get("type") == "array":
            return []
        if alt.get("type") == "object":
            return {}
        if alt.get("$ref"):
            return fill(alt)
    return "x"


def minimal(cid, entry):
    inst = {"id": "root", "component": cid}
    for part in entry.get("allOf", []):
        for r in part.get("required") or []:
            if r not in inst:
                inst[r] = fill((part.get("properties") or {}).get(r, {}))
    return inst


def full(cid, entry):
    """Every property filled (optional ones too), so a dangling $ref on an optional setting is reached (E4)."""
    inst = {"id": "root", "component": cid}
    for part in entry.get("allOf", []):
        for k, sch in (part.get("properties") or {}).items():
            if k not in inst:
                inst[k] = fill(sch)
    return inst


def basic_mode(cat):
    return cat.get("catalogId", "").startswith("https://a2ui.org/")


def run(cat, label):
    out = {"label": label, "catalogId": cat.get("catalogId"), "entries": {}}
    t = time.perf_counter()
    try:
        Draft202012Validator.check_schema(cat); out["C1_valid_2020_12_schema"] = True
    except Exception as e:
        out["C1_valid_2020_12_schema"] = False; out["C1_error"] = str(e)[:300]
    reg = registry(cat)
    proj = {k: cat[k] for k in ("catalogId", "components") if k in cat}
    out["C2_inline_projection_errors"] = errs({"$ref": caps["$id"] + "#/$defs/Catalog"}, proj, reg)[:12]
    ok = 0
    for cid, entry in cat["components"].items():
        inst = minimal(cid, entry)
        needs = [v for k, v in inst.items() if k not in ("id", "component") and v in ("child-1", ["child-1"])]
        comps = [inst]
        if needs:
            if basic_mode(cat):
                comps.append({"id": "child-1", "component": "Text", "text": "x"})
            else:
                child = minimal(cid, entry); child["id"] = "child-1"
                for k, v in list(child.items()):          # the child must not itself need children
                    if v in ("child-1", ["child-1"]):
                        child[k] = "root" if v == "child-1" else ["root"]
                comps.append(child)
        e1 = errs({"$ref": CATALOG_URI + "#/components/" + cid}, inst, reg)
        try:
            e4 = errs({"$ref": CATALOG_URI + "#/components/" + cid}, full(cid, entry), reg)
        except Exception as ex:                      # an unresolvable $ref raises inside referencing
            e4 = ["raised %s: %s" % (type(ex).__name__, str(ex)[:120])]
        e2 = errs({"$ref": CATALOG_URI + "#/components/" + cid}, dict(inst, probeUnknownProperty=1), reg)
        msg = {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": comps}}
        e3 = errs({"$ref": s2c["$id"]}, msg, reg)
        try:
            Draft202012Validator.check_schema(entry); e0 = []
        except Exception as ex:
            e0 = [str(ex).splitlines()[0][:200]]
        r = {"E0_entry_is_valid_schema": not e0, "E0_errors": e0, "E1_minimal_valid": not e1, "E1_errors": e1[:4],
             "E2_unknown_prop_rejected": bool(e2), "E3_updateComponents_valid": not e3, "E3_errors": e3[:4],
             "E4_full_valid": not e4, "E4_errors": e4[:4], "instance": inst}
        r["valid"] = (r["E0_entry_is_valid_schema"] and r["E1_minimal_valid"] and r["E2_unknown_prop_rejected"]
                      and r["E3_updateComponents_valid"] and (r["E4_full_valid"] or basic_mode(cat)))
        ok += r["valid"]
        out["entries"][cid] = r
    out["entries_valid"] = ok
    n1 = {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": [{"id": "root", "component": "NotInThisCatalogue"}]}}
    out["N1_unknown_component_rejected"] = bool(errs({"$ref": s2c["$id"]}, n1, reg))
    req = [(cid, e) for cid, e in cat["components"].items() if len(e["allOf"][-1].get("required", [])) > 1]
    if req:
        cid, e = req[0]
        n2 = {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": [{"id": "root", "component": cid}]}}
        out["N2_missing_required_rejected"] = {"component": cid, "rejected": bool(errs({"$ref": s2c["$id"]}, n2, reg))}
    out["entries_total"] = len(cat["components"])
    out["seconds"] = round(time.perf_counter() - t, 3)
    out["ok"] = (out["C1_valid_2020_12_schema"] and ok == out["entries_total"] and out["N1_unknown_component_rejected"]
                 and (out.get("N2_missing_required_rejected", {"rejected": True})["rejected"]))
    return out


# ---- the mutation set: a harness that passes everything proves nothing --------------------------
def mutations(cat):
    """Five one-change breaks of a catalogue, in memory; each must be CAUGHT by run(). Returns rows."""
    ids = sorted(cat["components"])
    def props(c, cid):
        return c["components"][cid]["allOf"][-1]["properties"]
    def first_with(pred):
        for cid in ids:
            if pred(cat["components"][cid]):
                return cid
        return ids[0]
    enum_cid = first_with(lambda e: any("enum" in v for k, v in e["allOf"][-1]["properties"].items() if k != "component"))
    enum_prop = next(k for k, v in cat["components"][enum_cid]["allOf"][-1]["properties"].items() if k != "component" and "enum" in v)
    ref_cid = first_with(lambda e: any("$ref" in v for k, v in e["allOf"][-1]["properties"].items() if k != "component"))
    ref_prop = next(k for k, v in cat["components"][ref_cid]["allOf"][-1]["properties"].items() if k != "component" and "$ref" in v)
    M = []
    c = copy.deepcopy(cat); props(c, enum_cid)[enum_prop] = {"type": "strin"}; M.append(("M1 illegal JSON Schema type (%s.%s)" % (enum_cid, enum_prop), c))
    c = copy.deepcopy(cat); props(c, ref_cid)[ref_prop] = {"$ref": CT + "ChildLst"}; M.append(("M2 dangling $ref into common_types (%s.%s)" % (ref_cid, ref_prop), c))
    c = copy.deepcopy(cat); c["components"][ids[0]]["unevaluatedProperties"] = True; M.append(("M3 entry accepts unknown props (%s; E2 must catch)" % ids[0], c))
    c = copy.deepcopy(cat); props(c, ids[1])["component"] = {"const": ids[1] + "X"}; M.append(("M4 discriminator const mismatch (%s)" % ids[1], c))
    c = copy.deepcopy(cat); c["$defs"]["anyComponent"]["oneOf"] = [x for x in c["$defs"]["anyComponent"]["oneOf"] if not x["$ref"].endswith("/" + ids[-1])]; M.append(("M5 part missing from anyComponent (%s; E3 must catch)" % ids[-1], c))
    rows = []
    for name, c in M:
        try:
            r = run(c, name)
            caught = not r["ok"]
            detail = "C1=%s entries %d/%d" % (r["C1_valid_2020_12_schema"], r["entries_valid"], r["entries_total"])
        except Exception as e:
            caught, detail = True, "raised %s: %s" % (type(e).__name__, str(e)[:90])
        rows.append({"mutation": name, "caught": caught, "detail": detail})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=OUT_DEFAULT, help="where catalogue-*.json live; a2ui-validation.json is written beside them")
    ap.add_argument("--mutations", action="store_true", help="run the mutation set on catalogue-dashboard.json; writes nothing")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    if a.mutations:
        cat = load(os.path.join(a.out, "catalogue-dashboard.json"))
        rows = mutations(cat)
        for r in rows:
            print("%-60s %s  (%s)" % (r["mutation"], "CAUGHT" if r["caught"] else "NOT CAUGHT", r["detail"]))
        n = sum(r["caught"] for r in rows)
        print("mutations caught %d/%d" % (n, len(rows)))
        return 0 if n == len(rows) else 1
    res = {"$spec": open(os.path.join(SPEC, "FETCHED.txt")).read().splitlines(),
           "$validator": "jsonschema Draft202012Validator + referencing"}
    b = run(basic, "CONTROL: official basic catalogue v0.9.1")
    res["control_basic"] = {k: v for k, v in b.items() if k != "entries"}
    res["control_basic"]["invalid_entries"] = {k: v["E1_errors"] + v["E3_errors"] for k, v in b["entries"].items() if not v["valid"]}
    rc = 0
    for fn in ("catalogue-dashboard.json", "catalogue-all.json"):
        p = os.path.join(a.out, fn)
        if not os.path.exists(p):
            continue
        r = run(load(p), fn)
        res[fn] = r
        if not a.quiet:
            print("%-26s C1 %s  entries valid %d/%d  C2 projection errors %d  N1 %s  N2 %s  %.3fs" % (
                fn, r["C1_valid_2020_12_schema"], r["entries_valid"], r["entries_total"], len(r["C2_inline_projection_errors"]),
                r["N1_unknown_component_rejected"], r.get("N2_missing_required_rejected", {}).get("rejected"), r["seconds"]))
            for k, v in [(k, v) for k, v in r["entries"].items() if not v["valid"]][:12]:
                print("  INVALID", k, v["E0_errors"][:1], v["E1_errors"][:2], v["E3_errors"][:2], v["E4_errors"][:2], "E2", v["E2_unknown_prop_rejected"])
        if not r["ok"]:
            rc = 1
    if not a.quiet:
        print("CONTROL basic: C1 %s valid %d/%d (minimal-instance builder limits: %s)" % (
            b["C1_valid_2020_12_schema"], b["entries_valid"], b["entries_total"], sorted(res["control_basic"]["invalid_entries"])))
    json.dump(res, open(os.path.join(a.out, "a2ui-validation.json"), "w"), indent=1, ensure_ascii=False)
    return rc


if __name__ == "__main__":
    sys.exit(main())
