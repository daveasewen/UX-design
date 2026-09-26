#!/usr/bin/env python3
"""R5 / 5a — generate an A2UI v0.9.1-shaped catalogue FROM the Apollo metas (probe, not canon).

Reads (never writes) knowledge/components/*.meta.json, meta.schema.json, shapes.json,
showroom/index.json, and the reader's own joins (knowledge/_compose_slice.py: load_graph,
_component_row, governs_for, obeys_for) for the rulings each part obeys.
Writes ONLY into this lane folder:
  catalogue-all.json        every real meta (137) as a catalogue entry
  catalogue-dashboard.json  the dashboard's parts (DASH below) — the PoC's first catalogue
  catalogue-report.json     per-meta gap codes, field coverage, schema-error publication map
Run:  python3 notes/_lanes/304/R5/gen_catalogue.py      (system python3; stdlib + jsonschema 3.2 for meta.schema.json)
Then: $HOME/.r5venv/bin/python notes/_lanes/304/R5/validate_a2ui.py   (draft 2020-12 check against the fetched spec)
"""
import json, glob, os, sys, hashlib, time, re

LANE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
K = os.path.join(ROOT, "knowledge")
sys.path.insert(0, K)
t0 = time.perf_counter()
import _compose_slice as reader          # the reader's joins, reused not re-implemented
import jsonschema                        # 3.2.0 at the seat: draft-7, as _build_integrity.py uses

CT = "https://a2ui.org/specification/v0_9/common_types.json#/$defs/"
CATALOG_ID_ALL = "https://apollo.invalid/catalogs/apollo-all/v0.0.1-probe/catalog.json"
CATALOG_ID_DASH = "https://apollo.invalid/catalogs/apollo-dashboard/v0.0.1-probe/catalog.json"
RESERVED = {"id", "component", "accessibility", "weight", "child", "children"}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def pascal(slug):
    return "".join(w[:1].upper() + w[1:] for w in re.split(r"[-_ ]+", slug) if w)

# ---- inputs ------------------------------------------------------------------------------
g = reader.load_graph(K)                                  # 137 real metas (EXAMPLE-* skipped by the reader)
schema = json.load(open(os.path.join(K, "components", "meta.schema.json")))
V = jsonschema.Draft7Validator(schema, resolver=jsonschema.RefResolver(base_uri="", referrer=schema))
shapes = json.load(open(os.path.join(K, "shapes.json")))["shapes"]
show = {c["slug"].lower(): c for c in json.load(open(os.path.join(ROOT, "showroom", "index.json")))["components"]}
# NB showroom slugs are lower-case; 7 meta filenames are capitalised (Chart-boxplot …) — matched case-insensitively
tb = json.load(open(os.path.join(K, "components", "template-dashboard.meta.json")))
tbb = json.load(open(os.path.join(K, "components", "template-dashboard-bento.meta.json")))
DASH_SOURCES = {
    "template-dashboard.$composes": [r.split(":", 1)[1] for r in tb["$composes"]],
    "template-dashboard-bento.$composes": [r.split(":", 1)[1] for r in tbb["$composes"]],
    "proposal v2 worked example (line chart, list)": ["chart-line", "list-items"],
    "#261 dashboard metas (A4 [132])": ["data-grid", "filter-toolbar-bar", "kpi-tile", "legend"],
}
DASH = sorted({s for v in DASH_SOURCES.values() for s in v})

# ---- prop mapping: meta prop type -> A2UI JSON Schema --------------------------------------
def map_prop(p):
    """Returns (schema or None, loss-note or None)."""
    t = p.get("type")
    d = p.get("$note") or ""
    if t == "enum":
        vals = p.get("values")
        if not isinstance(vals, list) or not vals:
            return None, "enum with no values list"
        vals = [str(v) for v in vals]
        s = {"type": "string", "enum": vals}
        if p.get("default") is not None and str(p["default"]) in vals:
            s["default"] = str(p["default"])
        return s, None
    if t == "boolean":
        return {"$ref": CT + "DynamicBoolean"}, None
    if t in ("string", "date"):
        return {"$ref": CT + "DynamicString"}, (None if t == "string" else "date carried as DynamicString (A2UI has no date type)")
    if t == "number":
        return {"$ref": CT + "DynamicNumber"}, None
    if t in ("array",) or (isinstance(t, str) and t.startswith("array<")):
        return {"oneOf": [{"type": "array"}, {"$ref": CT + "DataBinding"}]}, "array items untyped (meta gives no item schema)"
    if t == "object":
        return {"oneOf": [{"type": "object"}, {"$ref": CT + "DataBinding"}]}, "object untyped (meta gives no member schema)"
    if t in ("component", "slot"):
        return {"$ref": CT + "ComponentId"}, None
    if t == "table":
        return {"$ref": CT + "DataBinding"}, "type 'table' bound by path only: no row/column schema in the meta"
    return None, "type %r has no A2UI mapping" % t

def status_of(slug, m):
    sh = show.get(slug.lower())
    st = m.get("$status")
    when = m.get("when") or ""
    if isinstance(when, str) and when.strip().upper().startswith("NEVER"):
        return "deprecated", "meta when = NEVER (superseded)"
    if sh:
        s = sh.get("status")
        if isinstance(st, str) and "PROPOSED" in st.upper():
            return s or "beta", "showroom/index.json status=%s; meta $status PROPOSED" % s
        return s, "showroom/index.json"
    return None, "no showroom entry"

def rulings_of(m, row):
    gov = reader.governs_for([row], g)
    ob = reader.obeys_for([row], g, "")
    return ({"governs": sorted({r.get("ref") or r.get("id") for r in gov}),
             "obeysAuthored": sorted({r["id"] for r in ob if r.get("class") == "authored"}),
             "obeysDerived": sorted({r["id"] for r in ob if r.get("class") == "derived"}),
             "obeysRoutedCount": sum(1 for r in ob if str(r.get("class", "")).startswith("routed"))})

# ---- the entry ---------------------------------------------------------------------------
report = {"$generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "entries": {}}
components, xall = {}, {}
FROM = {}   # entry field -> meta source paths (for the schema-error publication map)
for slug, m in sorted(g["metas"].items()):
    cid = pascal(slug)
    gaps, loss, fr = [], [], {}
    path = os.path.join(ROOT, m["$path"])
    raw = json.load(open(path))
    serr = sorted(V.iter_errors(raw), key=lambda e: list(e.path))
    serr_rows = [{"path": "/".join(str(x) for x in e.path) or "(root)", "msg": e.message[:140]} for e in serr]
    if serr_rows:
        gaps.append("G-SCHEMA")
    props, required = {"component": {"const": cid}}, ["component"]
    fr["component"] = ["name"]
    for p in (m.get("props") or []):
        if not isinstance(p, dict) or not p.get("name"):
            loss.append("prop entry not an object with a name"); continue
        n = p["name"]
        if n in RESERVED:
            gaps.append("G-PROP-COLLISION"); loss.append("prop %r collides with an A2UI reserved name" % n); continue
        s, note = map_prop(p)
        if s is None:
            gaps.append("G-PROP-UNMAPPED"); loss.append("prop %r: %s" % (n, note)); continue
        if note:
            loss.append("prop %r: %s" % (n, note))
        if p.get("$note"):
            s = dict(s, description=str(p["$note"])[:300])
        props[n] = s; fr[n] = ["props"]
    if not m.get("props"):
        gaps.append("G-PROPS-NONE")
    vs = [v.get("name") for v in (m.get("variants") or []) if isinstance(v, dict) and v.get("name")]
    if vs:
        key = "variant" if "variant" not in props else "apolloVariant"
        if key != "variant":
            loss.append("meta already has a prop named 'variant'; variants carried as 'apolloVariant'")
        props[key] = {"type": "string", "enum": vs, "default": vs[0],
                      "description": "Apollo variants (meta.variants); first listed is the default by this probe's convention, not a ruling."}
        fr[key] = ["variants"]
    else:
        gaps.append("G-VARIANTS-NONE")
    slots = m.get("slots")
    if isinstance(slots, dict) and slots:
        for sn, sd in slots.items():
            if sn.startswith("$"):
                continue
            if sn in ("id", "component", "accessibility", "weight"):
                loss.append("slot %r collides with an A2UI reserved name" % sn); gaps.append("G-PROP-COLLISION"); continue
            if sn in props:
                # the meta declares a PARAM and a SLOT under one name (three-axis model, s136-D1);
                # an A2UI property can be only one of them. Probe convention: the slot wins, the
                # param's constraint is kept in the description and logged as a loss.
                gaps.append("G-SLOT-PROP-SAME-NAME")
                loss.append("slot %r shares its name with a prop; prop constraint moved into the slot description" % sn)
                pd = props.pop(sn).get("description", "")
            else:
                pd = ""
            multiple = bool(isinstance(sd, dict) and sd.get("multiple"))
            props[sn] = {"$ref": CT + ("ChildList" if multiple else "ComponentId"),
                         "description": (str((sd or {}).get("use", "")) + ((" | param: " + pd) if pd else ""))[:500]}
            fr[sn] = ["slots"]
            if isinstance(sd, dict) and sd.get("required") is True:
                required.append(sn)
            if isinstance(sd, dict) and sd.get("accepts"):
                loss.append("slot %r accepts %s: A2UI cannot constrain a child's type; the gate must" % (sn, json.dumps(sd["accepts"])))
    else:
        gaps.append("G-SLOTS")
    shape = m.get("shape")
    if not shape:
        gaps.append("G-SHAPE")
    elif shape not in shapes:
        gaps.append("G-SHAPE-UNRESOLVED")
    if not m.get("when"):
        gaps.append("G-WHEN")
    st, st_src = status_of(slug, m)
    if st is None:
        gaps.append("G-STATUS")
    elif st == "deprecated":
        gaps.append("G-DEPRECATED")
    elif st != "stable":
        gaps.append("G-STATUS-BETA")
    row = reader._component_row(m, 0, [], [], g)
    rul = rulings_of(m, row)
    if not (rul["governs"] or rul["obeysAuthored"] or rul["obeysDerived"]):
        gaps.append("G-RULINGS")
    a11y = m.get("accessibility") or {}
    when = m.get("when") or ""
    gate, _, prose = when.partition("—") if isinstance(when, str) else ("", "", "")
    x = {
        "slug": slug, "meta": m["$path"], "metaSha256": sha(path),
        "level": (show.get(slug.lower()) or {}).get("level"), "status": st, "statusSource": st_src,
        "provides": m.get("provides"), "answers": m.get("answers"), "shape": shape,
        "span": m.get("span"), "priority": m.get("priority"),
        "when": {"gate": gate.strip() or None, "prose": prose.strip() or None} if when else None,
        "variants": [{"name": v.get("name"), "use": v.get("use")} for v in (m.get("variants") or []) if isinstance(v, dict)],
        "slots": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("$")} for k, v in (slots or {}).items()
                  if isinstance(v, dict) and not k.startswith("$")} or None,
        "states": m.get("stateModel"),
        "accessibility": {"role": a11y.get("role") or a11y.get("roles"), "relatedSC": a11y.get("relatedSC")},
        "snippet": row.get("snippet"),
        "rulings": rul,
    }
    fr.update({"x-apollo.states": ["stateModel"], "x-apollo.accessibility": ["accessibility/role", "accessibility/roles", "accessibility/relatedSC"],
               "x-apollo.when": ["when"], "x-apollo.slots": ["slots"], "x-apollo.variants": ["variants"],
               "x-apollo.shape": ["shape"], "x-apollo.span": ["span"], "x-apollo.priority": ["priority"],
               "x-apollo.provides": ["provides"], "x-apollo.answers": ["answers"], "description": ["purpose", "when"]})
    purpose = (m.get("purpose") or "").strip()
    desc = purpose + ((" When: " + gate.strip()) if gate.strip() else "")
    entry = {
        "type": "object",
        "description": desc[:1200],
        "allOf": [
            {"$ref": CT + "ComponentCommon"},
            {"$ref": "#/$defs/CatalogComponentCommon"},
            {"type": "object", "properties": props, "required": required},
        ],
        "unevaluatedProperties": False,
    }
    components[cid] = entry
    xall[cid] = x
    FROM[cid] = fr
    report["entries"][cid] = {"slug": slug, "gaps": sorted(set(gaps)), "loss": loss, "schemaErrors": serr_rows,
                              "propsMapped": len([k for k in props if k != "component"]), "status": st}

def catalogue(ids, cat_id, title):
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": cat_id,
        "title": title,
        "description": "PROBE (R5, #304, 2026-09-26). Generated from knowledge/components/*.meta.json; not canon, not ruled. "
                       "Per-entry Apollo data sits in x-apollo (an annotation keyword; A2UI ignores it).",
        "catalogId": cat_id,
        "components": {i: components[i] for i in ids},
        "x-apollo": {i: xall[i] for i in ids},
        "$defs": {
            "CatalogComponentCommon": {"type": "object", "properties": {"weight": {"type": "number"}}},
            "theme": {"type": "object", "properties": {
                "apolloTheme": {"type": "string", "enum": ["apollo-legacy", "apollo-mono", "apollo-console", "apollo-supercharge"]},
                "mode": {"type": "string", "enum": ["light", "dark"]}}, "additionalProperties": False},
            "anyComponent": {"oneOf": [{"$ref": "#/components/" + i} for i in ids],
                             "discriminator": {"propertyName": "component"}},
        },
    }

all_ids = sorted(components)
dash_ids = sorted(pascal(s) for s in DASH if s in g["metas"])
missing = [s for s in DASH if s not in g["metas"]]
json.dump(catalogue(all_ids, CATALOG_ID_ALL, "Apollo — all parts (probe)"), open(os.path.join(LANE, "catalogue-all.json"), "w"), indent=1, ensure_ascii=False)
json.dump(catalogue(dash_ids, CATALOG_ID_DASH, "Apollo — dashboard parts (probe)"), open(os.path.join(LANE, "catalogue-dashboard.json"), "w"), indent=1, ensure_ascii=False)

# ---- the thirteen: which schema errors would the catalogue PUBLISH? ------------------------
def published(cid, err_path):
    head = err_path.split("/")[0]
    for field, srcs in FROM[cid].items():
        for s in srcs:
            if s == head or err_path == s or err_path.startswith(s + "/") or s.startswith(head + "/"):
                return field
    return None
pub = []
for cid, e in report["entries"].items():
    for se in e["schemaErrors"]:
        f = published(cid, se["path"])
        pub.append({"component": cid, "slug": e["slug"], "path": se["path"], "msg": se["msg"],
                    "published": bool(f), "via": f})
report["schemaErrorPublication"] = pub
report["dash"] = {"sources": DASH_SOURCES, "parts": DASH, "missingMetas": missing}
from collections import Counter
def tally(ids):
    c = Counter(); 
    for i in ids:
        c.update(report["entries"][i]["gaps"])
    return dict(sorted(c.items()))
report["gapTally"] = {"all": tally(all_ids), "dashboard": tally(dash_ids)}
report["inputs"] = {"head": os.popen("git -C '%s' --no-optional-locks rev-parse --short=8 HEAD" % ROOT).read().strip(),
                    "_rulings.json": sha(os.path.join(K, "_rulings.json")),
                    "meta.schema.json": sha(os.path.join(K, "components", "meta.schema.json")),
                    "metas_concat_sha256": hashlib.sha256(b"".join(open(os.path.join(ROOT, m["$path"]), "rb").read() for _, m in sorted(g["metas"].items()))).hexdigest()}
report["counts"] = {"metas_real": len(all_ids), "dashboard_parts": len(dash_ids),
                    "schema_valid_metas": sum(1 for e in report["entries"].values() if not e["schemaErrors"]),
                    "schema_errors": sum(len(e["schemaErrors"]) for e in report["entries"].values()),
                    "schema_errors_published": sum(1 for p in pub if p["published"])}
report["seconds"] = round(time.perf_counter() - t0, 3)
json.dump(report, open(os.path.join(LANE, "catalogue-report.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(report["counts"]), "secs", report["seconds"])
print("dash:", dash_ids, "missing:", missing)
print("gap tally all:", report["gapTally"]["all"])
print("gap tally dash:", report["gapTally"]["dashboard"])
