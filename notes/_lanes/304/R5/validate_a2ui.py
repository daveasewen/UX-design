#!/usr/bin/env python3
"""R5 / 5a — validate the generated catalogues against the fetched A2UI v0.9.1 spec (draft 2020-12).
Needs jsonschema >= 4.18 (referencing). Seat: $HOME/.r5venv/bin/python notes/_lanes/304/R5/validate_a2ui.py
Writes ONLY a2ui-validation.json in this lane folder. Spec files: a2ui-v0.9.1/ (see FETCHED.txt).
Checks, per catalogue:  C1 the catalogue is a valid 2020-12 schema document (NB the metaschema does NOT
  descend into `components` — mutation M1 found this — hence E0);
  C2 the inline-Catalog form (client_capabilities $defs/Catalog) — the published file form is not the inline form;
  per entry: E0 the entry itself passes the 2020-12 metaschema; E1 a minimal instance (id, component, required slots) validates against the entry;
             E2 the same instance plus an unknown property is REJECTED (unevaluatedProperties holds);
             E3 an updateComponents message carrying a root Column-free surface (the entry as root) validates
                against server_to_client.json with catalog.json resolved to THIS catalogue.
Control: the official basic catalogue runs through C1/C2/E1-E3 with a Text instance first.
"""
import json, os, sys, copy, time
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

LANE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(LANE, "a2ui-v0.9.1")
load = lambda p: json.load(open(p))
ct = load(os.path.join(SPEC, "json_common_types.json"))
s2c = load(os.path.join(SPEC, "json_server_to_client.json"))
caps = load(os.path.join(SPEC, "json_client_capabilities.json"))
basic = load(os.path.join(SPEC, "catalogs_basic_catalog.json"))
CATALOG_URI = "https://a2ui.org/specification/v0_9/catalog.json"   # what server_to_client's relative "catalog.json" resolves to

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

def minimal(cid, entry):
    inst = {"id": "root", "component": cid}
    for part in entry.get("allOf", []):
        req = part.get("required") or []
        pr = part.get("properties") or {}
        for r in req:
            if r in inst:
                continue
            sch = pr.get(r, {})
            ref = sch.get("$ref", "")
            if ref.endswith("ChildList"):
                inst[r] = ["child-1"]
            elif ref.endswith("ComponentId"):
                inst[r] = "child-1"
            elif ref.endswith("DynamicString"):
                inst[r] = "x"
            elif ref.endswith("Action"):
                inst[r] = {"event": {"name": "probe"}}
            elif "enum" in sch:
                inst[r] = sch["enum"][0]
            else:
                inst[r] = "x"
    return inst

def run(cat, label):
    out = {"label": label, "catalogId": cat.get("catalogId"), "entries": {}}
    t = time.perf_counter()
    try:
        Draft202012Validator.check_schema(cat); out["C1_valid_2020_12_schema"] = True
    except Exception as e:
        out["C1_valid_2020_12_schema"] = False; out["C1_error"] = str(e)[:300]
    reg = registry(cat)
    out["C2_inline_Catalog_form_errors"] = errs({"$ref": caps["$id"] + "#/$defs/Catalog"}, cat, reg)[:12]
    proj = {k: cat[k] for k in ("catalogId", "components") if k in cat}
    out["C2b_inline_projection_errors"] = errs({"$ref": caps["$id"] + "#/$defs/Catalog"}, proj, reg)[:12]
    ok = 0
    for cid, entry in cat["components"].items():
        r = {}
        inst = minimal(cid, entry)
        needs = [v for k, v in inst.items() if k not in ("id", "component") and v in ("child-1", ["child-1"])]
        comps = [inst] + ([{"id": "child-1", "component": cid if not basic_mode(cat) else "Text", **({} if not basic_mode(cat) else {"text": "x"})}] if needs else [])
        if needs and not basic_mode(cat):
            comps[1] = minimal(cid, entry); comps[1]["id"] = "child-1"
            for k, v in list(comps[1].items()):     # the child must not itself need children
                if v in ("child-1", ["child-1"]):
                    comps[1][k] = "root" if v == "child-1" else ["root"]
        e1 = errs({"$ref": CATALOG_URI + "#/components/" + cid}, inst, reg)
        bad = dict(inst, probeUnknownProperty=1)
        e2 = errs({"$ref": CATALOG_URI + "#/components/" + cid}, bad, reg)
        msg = {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": comps}}
        e3 = errs({"$ref": s2c["$id"]}, msg, reg)
        try:
            Draft202012Validator.check_schema(entry); e0 = []
        except Exception as ex:
            e0 = [str(ex).splitlines()[0][:200]]
        r = {"E0_entry_is_valid_schema": not e0, "E0_errors": e0, "E1_minimal_valid": not e1, "E1_errors": e1[:4], "E2_unknown_prop_rejected": bool(e2),
             "E3_updateComponents_valid": not e3, "E3_errors": e3[:4], "instance": inst}
        r["valid"] = r["E0_entry_is_valid_schema"] and r["E1_minimal_valid"] and r["E2_unknown_prop_rejected"] and r["E3_updateComponents_valid"]
        ok += r["valid"]
        out["entries"][cid] = r
    out["entries_valid"] = ok
    # harness negatives: prove E3 really resolves catalog.json to THIS catalogue
    first = next(iter(cat["components"]))
    n1 = {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": [{"id": "root", "component": "NotInThisCatalogue"}]}}
    out["N1_unknown_component_rejected"] = bool(errs({"$ref": s2c["$id"]}, n1, reg))
    req = [(cid, e) for cid, e in cat["components"].items() if len(e["allOf"][-1].get("required", [])) > 1]
    if req:
        cid, e = req[0]
        n2 = {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": [{"id": "root", "component": cid}]}}
        out["N2_missing_required_slot_rejected"] = {"component": cid, "rejected": bool(errs({"$ref": s2c["$id"]}, n2, reg))}
    out["entries_total"] = len(cat["components"])
    out["seconds"] = round(time.perf_counter() - t, 3)
    return out

def basic_mode(cat):
    return cat.get("catalogId", "").startswith("https://a2ui.org/")

res = {"$spec": open(os.path.join(SPEC, "FETCHED.txt")).read().splitlines(),
       "$validator": "jsonschema Draft202012Validator + referencing (venv)"}
b = run(basic, "CONTROL: official basic catalogue v0.9.1")
res["control_basic"] = {k: v for k, v in b.items() if k != "entries"}
res["control_basic"]["Text"] = b["entries"].get("Text")
res["control_basic"]["invalid_entries"] = {k: v["E1_errors"] + v["E3_errors"] for k, v in b["entries"].items() if not v["valid"]}
for fn in ("catalogue-dashboard.json", "catalogue-all.json"):
    r = run(load(os.path.join(LANE, fn)), fn)
    res[fn] = r
    print(fn, "C1", r["C1_valid_2020_12_schema"], "entries valid", r["entries_valid"], "/", r["entries_total"],
          "C2 inline-form errors", len(r["C2_inline_Catalog_form_errors"]), "C2b projection errors", len(r["C2b_inline_projection_errors"]), r["seconds"], "s")
    bad = {k: v for k, v in r["entries"].items() if not v["valid"]}
    for k, v in list(bad.items())[:12]:
        print("  INVALID", k, v["E1_errors"][:2], v["E3_errors"][:2], "E2", v["E2_unknown_prop_rejected"])
print("negatives", {k: res[k].get("N1_unknown_component_rejected") for k in ("catalogue-dashboard.json","catalogue-all.json")}, res["catalogue-all.json"].get("N2_missing_required_slot_rejected"))
print("CONTROL basic invalid (minimal-instance builder limits):", {k: v[:1] for k, v in res["control_basic"]["invalid_entries"].items()})
print("CONTROL basic: C1", b["C1_valid_2020_12_schema"], "valid", b["entries_valid"], "/", b["entries_total"],
      "C2 errors", len(b["C2_inline_Catalog_form_errors"]), b["C2_inline_Catalog_form_errors"][:3])
json.dump(res, open(os.path.join(LANE, "a2ui-validation.json"), "w"), indent=1, ensure_ascii=False)
