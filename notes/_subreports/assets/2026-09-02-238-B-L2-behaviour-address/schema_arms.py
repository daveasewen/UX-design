#!/usr/bin/env python3
"""
schema_arms.py — #238 lane B. Drives the PROPOSED meta schema (meta.schema.proposed.json) the way
knowledge/_build_integrity.py drives the live one (Draft7Validator, RefResolver base_uri=""):

  1. every live knowledge/components/*.meta.json (EXAMPLE excluded) still validates — BY ADDITION
     means the 136 untouched metas cannot go red;
  2. every one of the 20 PROPOSED typed objects (behaviour-migration.json) validates when put in
     place of the prose on a COPY of its meta;
  3. a mutation set — each arm is a planted defect in a typed object and MUST go red, beside a
     green control; an arm that stays green is reported as a defect of the SCHEMA.

Run from the repo root:  python3 notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/schema_arms.py
Exit 0 only if every expectation held.
"""
import copy, glob, json, os, sys
import jsonschema

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.getcwd()
COMP = os.path.join(REPO, "knowledge", "components")
schema = json.load(open(os.path.join(HERE, "meta.schema.proposed.json"), encoding="utf-8"))
live_schema = json.load(open(os.path.join(COMP, "meta.schema.json"), encoding="utf-8"))
V = jsonschema.Draft7Validator(schema, resolver=jsonschema.RefResolver(base_uri="", referrer=schema))
VL = jsonschema.Draft7Validator(live_schema, resolver=jsonschema.RefResolver(base_uri="", referrer=live_schema))
mig = json.load(open(os.path.join(HERE, "behaviour-migration.json"), encoding="utf-8"))


def errs(v, obj):
    return ["%s: %s" % ("/".join(str(x) for x in e.path) or "(root)", e.message[:140])
            for e in sorted(v.iter_errors(obj), key=lambda e: list(e.path))]


ok = True
def report(label, good, detail=""):
    global ok
    ok = ok and good
    print(("  ✅ " if good else "  ❌ ") + label + (" — " + detail if detail else ""))


print("## 1. the live population against the PROPOSED schema (by-addition: nothing may go red)")
metas = sorted(f for f in glob.glob(os.path.join(COMP, "*.meta.json"))
               if not os.path.basename(f).startswith("EXAMPLE"))
red_live, red_prop = [], []
for f in metas:
    d = json.load(open(f, encoding="utf-8"))
    if errs(VL, d):
        red_live.append(os.path.basename(f))
    e = errs(V, d)
    if e:
        red_prop.append((os.path.basename(f), e[:2]))
report("%d metas validate against the LIVE schema (control)" % (len(metas) - len(red_live)),
       not red_live, "red on live: %s" % red_live if red_live else "")
report("%d/%d metas validate against the PROPOSED schema" % (len(metas) - len(red_prop), len(metas)),
       not red_prop, "; ".join("%s %s" % r for r in red_prop) if red_prop else "")
prose = [f for f in metas if "behaviour" in json.load(open(f, encoding="utf-8"))]
report("the %d prose `behaviour` values take the LEGACY branch (still legal during migration)" % len(prose),
       len(prose) == 20 and not any(errs(V, json.load(open(f, encoding="utf-8"))) for f in prose))

print("## 2. the 20 PROPOSED typed objects, each in place of its prose, on a COPY of the meta")
bad = []
for it in mig["items"]:
    d = json.load(open(os.path.join(REPO, it["meta"]), encoding="utf-8"))
    d2 = copy.deepcopy(d)
    d2["behaviour"] = it["proposed"]
    e = errs(V, d2)
    if e:
        bad.append((it["slug"], e))
    # and the SAME typed object must be REJECTED by the LIVE schema? No — the live schema types
    # behaviour as object|array|string, so a typed object is legal there too (it is an object).
    # That is why the ratchet is a GATE, not the schema: report it, do not assert it.
report("%d/20 proposed objects validate" % (20 - len(bad)), not bad,
       "; ".join("%s: %s" % (s, e[:2]) for s, e in bad) if bad else "")
typed_ok_on_live = sum(1 for it in mig["items"]
                       if not errs(VL, dict(json.load(open(os.path.join(REPO, it["meta"]), encoding="utf-8")), behaviour=it["proposed"])))
print("  · note: %d/20 proposed objects ALSO pass the LIVE schema (it types behaviour as object|array|string) — "
      "the schema change is what makes the SHAPE checkable, not what makes the object legal" % typed_ok_on_live)

print("## 3. mutation arms — each planted defect must go RED against the proposed schema")
base_meta = json.load(open(os.path.join(REPO, "knowledge/components/date-picker.meta.json"), encoding="utf-8"))
good = next(it for it in mig["items"] if it["slug"] == "date-picker")["proposed"]


def arm(label, mutate, expect_red=True, must_mention=None):
    d = copy.deepcopy(base_meta)
    b = copy.deepcopy(good)
    mutate(b)
    d["behaviour"] = b
    e = errs(V, d)
    hit = bool(e)
    detail = e[0] if e else "no error"
    if must_mention and hit:
        hit = any(must_mention in x for x in e)
        if not hit:
            detail = "red, but not for the planted reason: " + e[0]
    report(("RED  " if expect_red else "GREEN") + " " + label, hit == expect_red, detail if (hit != expect_red or expect_red) else "")


arm("control — the proposed object as proposed", lambda b: None, expect_red=False)
arm("script: wrong grammar (a bare filename)", lambda b: b.__setitem__("script", "Date-picker.js"), must_mention="script")
arm("script: node-id grammar (snippet:… — the OTHER candidate grammar, refused by (a))", lambda b: b.__setitem__("script", "snippet:Date-picker.reference.html#script"), must_mention="script")
arm("script: fragment other than #script", lambda b: b.__setitem__("script", "knowledge/snippets/Date-picker.reference.html#script:2"), must_mention="script")
arm("script: a .css file", lambda b: b.__setitem__("script", "knowledge/canon/canon.css"), must_mention="script")
arm("script: key deleted (typed object without its discriminator falls to LEGACY — see note)", lambda b: b.pop("script"), expect_red=False)
arm("partial: key deleted", lambda b: b.pop("partial"), must_mention="partial")
arm("partial: not a registry-shaped name (uppercase)", lambda b: b.__setitem__("partial", "DV-Behaviour"), must_mention="partial")
arm("fallback: key deleted", lambda b: b.pop("fallback"), must_mention="fallback")
arm("fallback: empty string (null is the honest form, '' is a dodge)", lambda b: b.__setitem__("fallback", ""), must_mention="fallback")
arm("events: not an array", lambda b: b.__setitem__("events", "click"), must_mention="events")
arm("events: duplicate entries", lambda b: b.__setitem__("events", ["click", "click"]), must_mention="events")
arm("events: a non-DOM-shaped name", lambda b: b.__setitem__("events", ["Click Me"]), must_mention="events")
arm("events: key deleted (OPTIONAL — rC Q3 is open)", lambda b: b.pop("events"), expect_red=False)
arm("an extra prose key beside the typed fields (the prose must live under $note)", lambda b: b.__setitem__("keyboard", "Arrows move by day"), must_mention="keyboard")
arm("$unproven: names a field that does not exist", lambda b: b.__setitem__("$unproven", ["motion"]), must_mention="$unproven")
arm("$note: a number", lambda b: b.__setitem__("$note", 7), must_mention="$note")
arm("script null + fallback null (passive-but-undeclared is LEGAL by schema; the gate/ratchet owns it)", lambda b: (b.__setitem__("script", None), b.__setitem__("fallback", None)), expect_red=False)
arm("legacy prose control — a plain string still validates", lambda b: None, expect_red=False)
d = copy.deepcopy(base_meta); d["behaviour"] = "Passive display list — no states."
report("GREEN legacy prose (string) validates during migration", not errs(V, d))
d = copy.deepcopy(base_meta); d["behaviour"] = 42
report("RED   behaviour: a number is neither prose nor an address", bool(errs(V, d)))

print("\nNOTE on the `script`-deleted arm: the discriminator is the `script` key, so a typed object with "
      "no `script` is read as LEGACY prose and stays green here. That is the price of keeping the prose "
      "legal during migration; it closes when the legacy branch is retired (Dave's), and until then the "
      "GENERATOR refuses a #behaviour-manifest for a meta without `script` and the gate reports it UNPROVEN.")
print("\nSCHEMA ARMS: " + ("PASS ✅" if ok else "FAIL ❌"))
sys.exit(0 if ok else 1)
