#!/usr/bin/env python3
"""Launchpad step one — the catalogue generator: from the Apollo metas to A2UI v0.9.1 catalogue
entries with their when-rules, versioned like an API (#312 lane C1, grown from the R5 probe
notes/_lanes/304/R5/gen_catalogue.py; the shape is notes/_lanes/312/C/SPEC-launchpad-day-one.md § 5).

Reads (never writes) knowledge/components/*.meta.json, meta.schema.json, shapes.json, roles.json,
when-fields.json, showroom/index.json and the reader's own joins (knowledge/_compose_slice.py:
load_graph, _component_row, governs_for, obeys_for) for the rulings each part obeys.
Writes ONLY under apollo-launchpad/catalogue/out/:
  catalogue-dashboard.json   the PoC catalogue (the API: committed)
  catalogue-report.json      losses, tallies, the dashboard derivation, inputs (committed)
  catalogue-all.json         every real part, a by-product nothing reads (git-ignored)

The metas are read as they stand. Lane L's four optional fields (anatomy, states, emits, bindings,
s311-D4) are published under x-apollo.spec when present and never required.

Run:   python3 apollo-launchpad/catalogue/gen_catalogue.py            (system python3; jsonschema 3.2 or 4.x)
Gate:  python3 apollo-launchpad/catalogue/gen_catalogue.py --check    (exit 1 when out/ is stale against the metas)
Also:  --metas-sha <sha>   stamp that git sha instead of HEAD (the committer's exact landing sha)
       --out <dir>         write elsewhere (the selftest uses a temp dir)
Every run is deterministic: no clock, no counter; the same metas give the same bytes (T1.6).
"""
import json, os, sys, hashlib, time, re, argparse, subprocess, io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
K = os.path.join(ROOT, "knowledge")
OUT_DEFAULT = os.path.join(HERE, "out")

CT = "https://a2ui.org/specification/v0_9/common_types.json#/$defs/"
CATALOG_BASE = "https://apollo.invalid/catalogs/apollo-launchpad/"      # reserved domain until a host is real [spec]
FIRST_VERSION = "v0.1.0"
RESERVED = {"id", "component", "accessibility", "weight", "child", "children"}

# the dashboard set is DERIVED, as R5 derived it: the templates' $composes, the worked example's two
# parts and the #261 dashboard metas; then aliases resolve to their owner, deprecated parts drop out,
# and the wall itself joins (s305-D18: the wall holds the tiles).
DASH_EXTRA = {
    "proposal v2 worked example (line chart, list)": ["chart-line", "list-items"],
    "#261 dashboard metas (A4 [132])": ["data-grid", "filter-toolbar-bar", "kpi-tile", "legend"],
    "s305-D18 the wall that holds the tiles": ["template-dashboard-bento"],
}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(open(p, "rb").read())


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def pascal(slug):
    return "".join(w[:1].upper() + w[1:] for w in re.split(r"[-_ ]+", slug) if w)


def git_head(root):
    try:
        return subprocess.run(["git", "-C", root, "--no-optional-locks", "rev-parse", "--short=8", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip() or None
    except Exception:
        return None


def bump_patch(version):
    m = re.match(r"^v(\d+)\.(\d+)\.(\d+)$", version or "")
    if not m:
        return FIRST_VERSION
    return "v%s.%s.%d" % (m.group(1), m.group(2), int(m.group(3)) + 1)


# ---- the build --------------------------------------------------------------------------------
def build(metas_sha=None, prev_dash=None, prev_all=None, overlay=None):
    """Returns (dash_catalogue, all_catalogue, report, seconds). Pure: reads the tree, writes nothing.
    `overlay` is for the selftest only: {"metas": {slug: meta}, "schema": schema} stands in for files on disk,
    so a meta carrying lane L's four fields can be proven without touching the tree."""
    t0 = time.perf_counter()
    sys.path.insert(0, K)
    import _compose_slice as reader          # the reader's joins, reused not re-implemented
    import jsonschema

    g = reader.load_graph(K)
    overlay = overlay or {}
    for slug, om in (overlay.get("metas") or {}).items():
        g["metas"][slug] = dict(g["metas"][slug], **om)
    schema_path = os.path.join(K, "components", "meta.schema.json")
    schema = overlay.get("schema") or json.load(open(schema_path))
    V = jsonschema.Draft7Validator(schema)   # local $refs only; works on 3.2 and 4.x alike
    shapes = json.load(open(os.path.join(K, "shapes.json")))["shapes"]
    roles = json.load(open(os.path.join(K, "roles.json")))["roles"]
    when_fields = list(json.load(open(os.path.join(K, "when-fields.json")))["fields"].keys())
    show = {c["slug"].lower(): c for c in json.load(open(os.path.join(ROOT, "showroom", "index.json")))["components"]}
    field_rx = re.compile(r"(?<![\w.])(" + "|".join(re.escape(f) for f in sorted(when_fields, key=len, reverse=True)) + r")(?![\w.])")

    # -- aliases: slug -> owner slug; owner -> [alias slugs]
    alias_of, aliases_of = {}, {}
    for slug, m in g["metas"].items():
        a = m.get("aliasOf")
        if isinstance(a, dict) and isinstance(a.get("component"), str):
            owner = a["component"].split(":", 1)[-1]
            alias_of[slug] = owner
            aliases_of.setdefault(owner, []).append(slug)
    for k in aliases_of:
        aliases_of[k].sort()

    # -- the dashboard derivation
    sources = {}
    for t in ("template-dashboard", "template-dashboard-bento"):
        tm = g["metas"].get(t) or {}
        sources[t + ".$composes"] = [r.split(":", 1)[1] for r in (tm.get("$composes") or [])]
    sources.update(DASH_EXTRA)
    derived = sorted({s for v in sources.values() for s in v})

    def is_deprecated(m):
        w = m.get("when")
        return isinstance(w, str) and w.strip().upper().startswith("NEVER")

    dash_slugs, dash_steps = [], []
    for s in derived:
        m = g["metas"].get(s)
        if m is None:
            dash_steps.append({"slug": s, "step": "dropped", "why": "no meta"}); continue
        if s in alias_of:
            dash_steps.append({"slug": s, "step": "resolved", "to": alias_of[s], "why": "aliasOf (s210-D5): an alias holds no spec"})
            s = alias_of[s]
        if is_deprecated(g["metas"][s]):
            dash_steps.append({"slug": s, "step": "dropped", "why": "when = NEVER (deprecated): never eligible, not published"}); continue
        if s not in dash_slugs:
            dash_slugs.append(s)
    dash_slugs.sort()

    # -- prop mapping: a meta setting -> an A2UI property schema
    def data_schema(p, note_sink):
        t = p.get("type")
        if t in ("string", "date", "length"):
            s = {"$ref": CT + "DynamicString"}
            if t != "string":
                note_sink.append("%s carried as DynamicString (A2UI has no %s type)" % (t, t))
            return s
        if t == "number":
            return {"$ref": CT + "DynamicNumber"}
        if t == "boolean":
            return {"$ref": CT + "DynamicBoolean"}
        if t == "array" or (isinstance(t, str) and t.startswith("array<")):
            s = {"oneOf": [{"type": "array"}, {"$ref": CT + "DataBinding"}]}
            if not p.get("$items"):
                note_sink.append("array items untyped (meta gives no item schema)")
            return s
        if t in ("object", "table"):
            note_sink.append("type %r bound as an object or a data-model path: no member schema in the meta" % t)
            return {"oneOf": [{"type": "object"}, {"type": "array"}, {"$ref": CT + "DataBinding"}]}
        return None

    def map_prop(p):
        """Returns (schema or None, loss-note or None). A data setting (bindsData) and an own-words setting
        (ownText) are typed as A2UI DATA, never as a ComponentId (s305-D19)."""
        t = p.get("type")
        notes = []
        if (p.get("bindsData") or p.get("ownText")) and t != "enum":
            s = data_schema(p, notes)
            if s is None:
                return None, "type %r has no A2UI data mapping" % t
            return s, ("; ".join(notes) or None)
        if t == "enum":
            # an enum setting that also binds data (chart-bar's `series` mode) stays an enum; the binding
            # rides on x-apollo (data, capability, shape) and the chooser reads it there
            vals = p.get("values")
            if not isinstance(vals, list) or not vals:
                return None, "enum with no values list"
            vals = [str(v) for v in vals]
            s = {"type": "string", "enum": vals}
            if p.get("default") is not None and str(p["default"]) in vals:
                s["default"] = str(p["default"])
            return s, None
        if t in ("component", "slot"):
            # a bare `component` prop with no slot entry: the three-axis model's old form; A2UI reads it as a child
            return {"$ref": CT + "ComponentId"}, "prop type %r read as a ComponentId (no slot entry of that name)" % t
        s = data_schema(p, notes)
        if s is None:
            return None, "type %r has no A2UI mapping" % t
        return s, ("; ".join(notes) or None)

    def status_of(slug, m):
        sh = show.get(slug.lower())
        st = m.get("$status")
        if is_deprecated(m):
            return "deprecated", "meta when = NEVER (superseded)"
        if sh:
            s = sh.get("status")
            if isinstance(st, str) and ("PROPOSED" in st.upper()):
                return s or "beta", "showroom/index.json status=%s; meta $status PROPOSED" % s
            return s, "showroom/index.json"
        return None, "no showroom entry"

    def rulings_of(m, row):
        gov = reader.governs_for([row], g)
        ob = reader.obeys_for([row], g, "")
        return {"governs": sorted({r.get("ref") or r.get("id") for r in gov if (r.get("ref") or r.get("id"))}),
                "obeysAuthored": sorted({r["id"] for r in ob if r.get("class") == "authored"}),
                "obeysDerived": sorted({r["id"] for r in ob if r.get("class") == "derived"}),
                "obeysRoutedCount": sum(1 for r in ob if str(r.get("class", "")).startswith("routed"))}

    def states_of(m):
        sm = m.get("stateModel")
        if isinstance(sm, dict) and isinstance(sm.get("states"), list):
            out = {"states": list(sm["states"])}
            if sm.get("attribute"):
                out["attribute"] = sm["attribute"]
            out["sentences"] = {s: sm[s] for s in sm["states"] if isinstance(sm.get(s), str)}
            return out
        if sm in ("simple", "full"):
            return {"model": sm}
        return None

    def spec_of(m):
        """s311-D4's four fields, read if present, never required (lane L adds them today)."""
        out = {k: m[k] for k in ("anatomy", "states", "emits", "bindings") if k in m}
        if "$extracted" in m:
            out["$extracted"] = m["$extracted"]
        return out or None

    # -- the entries
    components, xapollo, report_entries = {}, {}, {}
    for slug, m in sorted(g["metas"].items()):
        if slug in alias_of:
            report_entries[slug] = {"slug": slug, "component": pascal(slug), "published": False,
                                    "why": "alias of %s (s210-D5): listed on the owner's entry, no entry of its own" % alias_of[slug],
                                    "gaps": ["G-ALIAS"], "loss": [], "schemaErrors": []}
            continue
        cid = pascal(slug)
        gaps, loss = [], []
        path = os.path.join(ROOT, m["$path"])
        raw = json.load(open(path))
        if slug in (overlay.get("metas") or {}):
            raw = dict(raw, **overlay["metas"][slug])
        serr = sorted(V.iter_errors(raw), key=lambda e: list(e.path))
        serr_rows = [{"path": "/".join(str(x) for x in e.path) or "(root)", "msg": e.message[:140]} for e in serr]
        if serr_rows:
            gaps.append("G-SCHEMA")
        props, required = {"component": {"const": cid}}, ["component"]
        settings, data_settings, own_words = [], [], []
        slot_names = {k for k in (m.get("slots") or {}) if not k.startswith("$")}
        for p in (m.get("props") or []):
            if not isinstance(p, dict) or not p.get("name"):
                loss.append("prop entry not an object with a name"); continue
            n = p["name"]
            if n in RESERVED:
                gaps.append("G-PROP-COLLISION"); loss.append("setting %r collides with an A2UI reserved name" % n); continue
            if n in slot_names:
                gaps.append("G-SLOT-PROP-SAME-NAME"); loss.append("setting %r shares its name with a slot (s305-D19 says never both)" % n); continue
            s, note = map_prop(p)
            if s is None:
                gaps.append("G-PROP-UNMAPPED"); loss.append("setting %r: %s" % (n, note)); continue
            if note:
                loss.append("setting %r: %s" % (n, note))
            desc = str(p.get("$note") or "").strip()
            xa = {}
            if p.get("bindsData"):
                bd = p["bindsData"]
                xa["data"] = True
                xa["capability"] = list(bd.get("capability") or [])
                if bd.get("shape"):
                    xa["shape"] = bd["shape"]
                    if bd["shape"] not in shapes:
                        gaps.append("G-SHAPE-UNRESOLVED"); loss.append("setting %r: shape %r is not in shapes.json" % (n, bd["shape"]))
                data_settings.append(n)
                # required when the shape is a data shape and the meta gives no default [spec, refined: a
                # setting with a default (even null) is optional by the meta's own word]
                if "default" not in p and not str(bd.get("shape") or "").startswith("no-data"):
                    required.append(n)
            if p.get("ownText"):
                xa["ownText"] = True
                if p.get("$items"):
                    xa["items"] = str(p["$items"])
                    desc = (desc + " Each entry: " + str(p["$items"])).strip()
                own_words.append(n)
                if "default" not in p:
                    required.append(n)
            if desc:
                s = dict(s, description=desc[:300])
            if xa:
                s = dict(s, **{"x-apollo": xa})
            props[n] = s
            settings.append(n)
        if not m.get("props"):
            gaps.append("G-PROPS-NONE")
        vs = [v.get("name") for v in (m.get("variants") or []) if isinstance(v, dict) and v.get("name")]
        if vs:
            key = "variant" if "variant" not in props else "apolloVariant"
            if key != "variant":
                loss.append("meta already has a setting named 'variant'; variants carried as 'apolloVariant'")
            props[key] = {"type": "string", "enum": vs, "default": vs[0],
                          "description": "Apollo variants (meta.variants); the first listed is the default by the generator's convention, not a ruling."}
        else:
            gaps.append("G-VARIANTS-NONE")
        slots_x = {}
        slots = m.get("slots")
        if isinstance(slots, dict) and slot_names:
            for sn in sorted(slot_names):
                sd = slots[sn]
                if sn in ("id", "component", "accessibility", "weight"):
                    loss.append("slot %r collides with an A2UI reserved name" % sn); gaps.append("G-PROP-COLLISION"); continue
                if not isinstance(sd, dict):
                    loss.append("slot %r is not an object" % sn); continue
                multiple = bool(sd.get("multiple"))
                acc = {k: v for k, v in (sd.get("accepts") or {}).items() if not k.startswith("$")}
                ps = {"$ref": CT + ("ChildList" if multiple else "ComponentId"),
                      "description": str(sd.get("use", ""))[:500],
                      "x-apollo": {"slot": True, "accepts": acc, "multiple": multiple}}
                if sd.get("sameKind"):
                    ps["x-apollo"]["sameKind"] = True
                props[sn] = ps
                slots_x[sn] = {"accepts": acc, "required": bool(sd.get("required")), "multiple": multiple}
                if sd.get("required") is True:
                    required.append(sn)
                for r in acc.get("provides") or []:
                    if r not in roles:
                        gaps.append("G-ROLE-UNRESOLVED"); loss.append("slot %r accepts role %r not in roles.json" % (sn, r))
        else:
            gaps.append("G-SLOTS")
        shape = m.get("shape")
        if not shape:
            gaps.append("G-SHAPE")
        elif shape not in shapes:
            gaps.append("G-SHAPE-UNRESOLVED")
        when = m.get("when") or ""
        if not when:
            gaps.append("G-WHEN")
        gate, _, prose = when.partition("—") if isinstance(when, str) else ("", "", "")
        gate, prose = gate.strip(), prose.strip()
        st, st_src = status_of(slug, m)
        if st is None:
            gaps.append("G-STATUS")
        elif st == "deprecated":
            gaps.append("G-DEPRECATED")
        elif st != "stable":
            gaps.append("G-STATUS-BETA")
        if m.get("provides") and m["provides"] not in roles:
            gaps.append("G-ROLE-UNRESOLVED"); loss.append("provides %r is not in roles.json" % m["provides"])
        row = reader._component_row(m, 0, [], [], g)
        rul = rulings_of(m, row)
        if not (rul["governs"] or rul["obeysAuthored"] or rul["obeysDerived"]):
            gaps.append("G-RULINGS")
        a11y = m.get("accessibility") or {}
        x = {
            "slug": slug, "meta": m["$path"], "metaSha256": sha_file(path),
            "level": (show.get(slug.lower()) or {}).get("level"),
            "status": st, "statusSource": st_src,
            "proposal": bool(st and st != "stable" and st != "deprecated"),     # s305-D20: beta parts publish marked
            "provides": m.get("provides"), "answers": m.get("answers"), "shape": shape,
            "span": m.get("span"), "priority": m.get("priority"),
            "when": ({"gate": gate or None, "prose": prose or None,
                      "fields": sorted(set(field_rx.findall(gate)))} if when else None),
            "variants": [{"name": v.get("name"), "use": v.get("use")} for v in (m.get("variants") or []) if isinstance(v, dict)],
            "settings": settings, "dataSettings": data_settings, "ownWords": own_words,
            "slots": slots_x or None,
            "states": states_of(m),
            "a11y": {"role": a11y.get("role") or a11y.get("roles"), "sc": a11y.get("relatedSC")},
            "snippet": row.get("snippet"),
            "rulings": rul,
            "aliases": aliases_of.get(slug, []),
        }
        spec = spec_of(m)
        if spec:
            x["spec"] = spec
        purpose = (m.get("purpose") or "").strip()
        desc = purpose + ((" When: " + gate) if gate else "")
        entry = {
            "type": "object",
            "description": desc[:1200],
            "allOf": [
                {"$ref": CT + "ComponentCommon"},
                {"$ref": "#/$defs/CatalogComponentCommon"},
                {"type": "object", "properties": props, "required": sorted(set(required), key=required.index)},
            ],
            "unevaluatedProperties": False,
            "x-apollo": x,
        }
        components[cid] = entry
        xapollo[cid] = x
        published = not serr_rows and st != "deprecated"          # R5's L2 rule: the catalogue never publishes drift
        report_entries[slug] = {"slug": slug, "component": cid, "published": published,
                                "why": None if published else ("meta fails meta.schema.json" if serr_rows else "deprecated"),
                                "gaps": sorted(set(gaps)), "loss": loss, "schemaErrors": serr_rows,
                                "settings": len(settings), "dataSettings": len(data_settings), "ownWords": len(own_words),
                                "slots": len(slots_x), "required": [r for r in required if r != "component"], "status": st}

    def catalogue(ids, name, title, version, prev):
        cat_id = CATALOG_BASE + name + "/" + version + "/catalog.json"
        doc = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": cat_id,
            "title": title,
            "description": "Generated from knowledge/components/*.meta.json by apollo-launchpad/catalogue/gen_catalogue.py; "
                           "the metas are the source, this file is the API. Per-entry Apollo data sits under x-apollo "
                           "(an annotation keyword; A2UI ignores it). Beta parts carry x-apollo.proposal: true (s305-D20).",
            "catalogId": cat_id,
            "components": {i: components[i] for i in ids},
            "functions": {},
            "$defs": {
                "anyFunction": {"description": "This catalogue defines no functions (the PoC shows and prepares only, s305-D46); "
                                               "a FunctionCall in a setting value is therefore refused.",
                                "not": {}},
                "CatalogComponentCommon": {"type": "object", "properties": {"weight": {"type": "number"}}},
                "theme": {"type": "object", "properties": {
                    "apolloTheme": {"type": "string", "enum": ["apollo-legacy", "apollo-mono", "apollo-console", "apollo-supercharge"]},
                    "mode": {"type": "string", "enum": ["light", "dark"]}}, "additionalProperties": False},
                "anyComponent": {"oneOf": [{"$ref": "#/components/" + i} for i in ids],
                                 "discriminator": {"propertyName": "component"}},
            },
        }
        api_sha = sha_bytes(canonical({"components": doc["components"], "$defs": doc["$defs"]}))
        # versioned like an API: the patch bumps when any entry's bytes change, else the version and the
        # `previous` pointer carry forward unchanged, so a re-run on the same metas is byte-identical (T1.6)
        prev_stamp = ((prev or {}).get("x-apollo") or {}).get("catalogue") or {}
        previous = None
        if prev_stamp.get("sha256") and prev_stamp.get("version"):
            if prev_stamp["sha256"] == api_sha:
                version, previous = prev_stamp["version"], prev_stamp.get("previous")
            else:
                version, previous = bump_patch(prev_stamp["version"]), {"version": prev_stamp["version"], "sha256": prev_stamp["sha256"]}
            cat_id = CATALOG_BASE + name + "/" + version + "/catalog.json"
            doc["$id"] = doc["catalogId"] = cat_id
        doc["x-apollo"] = {"catalogue": {"name": name, "version": version, "sha256": api_sha,
                                         "metas_sha": metas_sha, "metas_sha256": metas_content_sha,
                                         "parts": [components[i]["x-apollo"]["slug"] for i in ids],
                                         "previous": previous}}
        return doc

    pub_ids = sorted(pascal(s) for s, e in report_entries.items() if e["published"])
    dash_ids = sorted(pascal(s) for s in dash_slugs if report_entries.get(s, {}).get("published"))
    dash_unpublished = [s for s in dash_slugs if not report_entries.get(s, {}).get("published")]
    metas_content_sha = sha_bytes(b"".join(open(os.path.join(ROOT, g["metas"][s]["$path"]), "rb").read()
                                           for s in sorted(g["metas"])))
    metas_sha = metas_sha or git_head(ROOT) or "unknown"
    dash = catalogue(dash_ids, "dashboard", "Apollo Launchpad — the dashboard parts", FIRST_VERSION, prev_dash)
    allc = catalogue(pub_ids, "all", "Apollo Launchpad — every published part (by-product)", FIRST_VERSION, prev_all)

    from collections import Counter
    def tally(slugs):
        c = Counter()
        for s in slugs:
            c.update(report_entries[s]["gaps"])
        return dict(sorted(c.items()))
    report = {
        "catalogue": dash["x-apollo"]["catalogue"],
        "dashboard": {"sources": sources, "derived": derived, "steps": dash_steps, "published": dash_slugs,
                      "unpublished": dash_unpublished, "count": len(dash_ids)},
        "counts": {"metas_real": len(g["metas"]), "aliases": len(alias_of),
                   "published_all": len(pub_ids), "published_dashboard": len(dash_ids),
                   "unpublished_schema": sum(1 for e in report_entries.values() if e["why"] == "meta fails meta.schema.json"),
                   "unpublished_deprecated": sum(1 for e in report_entries.values() if e["why"] == "deprecated"),
                   "schema_errors": sum(len(e["schemaErrors"]) for e in report_entries.values()),
                   "same_name_losses_all": sum(e["gaps"].count("G-SLOT-PROP-SAME-NAME") for e in report_entries.values()),
                   "same_name_losses_dashboard": sum(report_entries[s]["gaps"].count("G-SLOT-PROP-SAME-NAME") for s in dash_slugs),
                   "spec_fields_present": sum(1 for s in dash_slugs if components.get(pascal(s), {}).get("x-apollo", {}).get("spec"))},
        "gapTally": {"all": tally(sorted(report_entries)), "dashboard": tally(dash_slugs)},
        "entries": {s: report_entries[s] for s in sorted(report_entries)},
        "inputs": {"metas_sha": metas_sha, "metas_sha256": metas_content_sha,
                   "meta.schema.json": sha_file(schema_path),
                   "shapes.json": sha_file(os.path.join(K, "shapes.json")),
                   "roles.json": sha_file(os.path.join(K, "roles.json")),
                   "when-fields.json": sha_file(os.path.join(K, "when-fields.json")),
                   "_rulings.json": sha_file(os.path.join(K, "_rulings.json"))},
    }
    return dash, allc, report, round(time.perf_counter() - t0, 3)


def report_comparable(rep):
    """The report with its provenance stamps masked, for --check and the selftest (#312 lane V).
    `inputs` carries the input files' hashes and `catalogue.metas_sha` is git HEAD at build time,
    so a committed report can never carry the sha of the commit that holds it: comparing them made
    --check STALE on every commit (AC1 found, not fixed). The entries' sha256 and the metas' bytes
    (metas_sha256) stay in the comparison; the git stamp and the input hashes are informational."""
    out = {k: v for k, v in rep.items() if k != "inputs"}
    if isinstance(out.get("catalogue"), dict):
        out["catalogue"] = {k: v for k, v in out["catalogue"].items() if k != "metas_sha"}
    return canonical(out)


def dump(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def load_prev(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="refuse (exit 1) when out/ is stale against the metas; writes nothing")
    ap.add_argument("--metas-sha", default=None, help="stamp this git sha as x-apollo.catalogue.metas_sha (default: HEAD)")
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    paths = {"dash": os.path.join(a.out, "catalogue-dashboard.json"),
             "all": os.path.join(a.out, "catalogue-all.json"),
             "report": os.path.join(a.out, "catalogue-report.json")}
    prev_dash, prev_all = load_prev(paths["dash"]), load_prev(paths["all"])
    dash, allc, report, secs = build(a.metas_sha, prev_dash, prev_all)
    if a.check:
        stale = []
        if prev_dash is None:
            stale.append("catalogue-dashboard.json missing")
        else:
            old, new = prev_dash.get("x-apollo", {}).get("catalogue", {}), dash["x-apollo"]["catalogue"]
            if old.get("sha256") != new["sha256"]:
                stale.append("catalogue-dashboard.json: entries changed (sha256 %s -> %s; version would be %s)"
                             % (str(old.get("sha256"))[:12], new["sha256"][:12], new["version"]))
            if old.get("metas_sha256") != new["metas_sha256"]:
                stale.append("catalogue-dashboard.json: the metas' bytes moved (metas_sha256 %s -> %s)"
                             % (str(old.get("metas_sha256"))[:12], new["metas_sha256"][:12]))
        if prev_dash is not None:
            # the BODY on disk, re-hashed — a tampered entry under an untouched stamp is stale too (#312 lane V)
            body_sha = sha_bytes(canonical({"components": prev_dash.get("components"), "$defs": prev_dash.get("$defs")}))
            if body_sha != dash["x-apollo"]["catalogue"]["sha256"]:
                stale.append("catalogue-dashboard.json: the entries on disk differ from a fresh build (body sha256 %s -> %s)"
                             % (body_sha[:12], dash["x-apollo"]["catalogue"]["sha256"][:12]))
        prev_rep = load_prev(paths["report"])
        if prev_rep is None:
            stale.append("catalogue-report.json missing")
        elif report_comparable(prev_rep) != report_comparable(report):
            stale.append("catalogue-report.json differs from a fresh run")
        if stale:
            print("gen_catalogue --check: STALE\n  " + "\n  ".join(stale) + "\n  run: python3 apollo-launchpad/catalogue/gen_catalogue.py")
            return 1
        print("gen_catalogue --check: OK  %s %s sha256 %s… parts %d  (%.3fs)" % (
            dash["x-apollo"]["catalogue"]["name"], dash["x-apollo"]["catalogue"]["version"],
            dash["x-apollo"]["catalogue"]["sha256"][:12], report["counts"]["published_dashboard"], secs))
        return 0
    os.makedirs(a.out, exist_ok=True)
    open(paths["dash"], "w", encoding="utf-8").write(dump(dash))
    open(paths["all"], "w", encoding="utf-8").write(dump(allc))
    open(paths["report"], "w", encoding="utf-8").write(dump(report))
    if not a.quiet:
        c = dash["x-apollo"]["catalogue"]
        print("catalogue %s %s sha256 %s metas_sha %s parts %d  (%.3fs)" % (c["name"], c["version"], c["sha256"][:12], c["metas_sha"], len(c["parts"]), secs))
        print("dashboard:", report["dashboard"]["published"], "unpublished:", report["dashboard"]["unpublished"])
        print("counts:", json.dumps(report["counts"]))
        print("gap tally dashboard:", report["gapTally"]["dashboard"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
