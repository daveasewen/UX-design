#!/usr/bin/env python3
"""Launchpad step one — the catalogue selftest: T1.1–T1.7 of notes/_lanes/312/C/SPEC-launchpad-day-one.md § 11,
plus the gate's own bite (#312 lane C1). Exit 1 on any failure; the receipt is what the lane report pastes.

Run:  $HOME/.launchpad-venv/bin/python apollo-launchpad/catalogue/selftest.py      (needs jsonschema >= 4.18 + referencing)
Writes nothing under the repo: every build goes to a temp dir and is compared with out/ by bytes.
"""
import json, os, sys, time, tempfile, shutil, subprocess, copy, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
sys.path.insert(0, HERE)
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

try:
    import referencing  # noqa
    from jsonschema import Draft202012Validator  # noqa
except Exception as e:
    print("selftest needs jsonschema >= 4.18 with referencing (%s).\n  python3 -m venv $HOME/.launchpad-venv && "
          "$HOME/.launchpad-venv/bin/pip install -r apollo-launchpad/requirements.txt" % e)
    sys.exit(2)

import gen_catalogue as gen
import validate_a2ui as va

rows, failed = [], 0


def check(tid, ok, detail):
    global failed
    rows.append((tid, "PASS" if ok else "FAIL", detail))
    if not ok:
        failed += 1


def quiet_build(**kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return gen.build(**kw)


def write_set(d, dash, allc, rep):
    os.makedirs(d, exist_ok=True)
    for fn, obj in (("catalogue-dashboard.json", dash), ("catalogue-all.json", allc), ("catalogue-report.json", rep)):
        open(os.path.join(d, fn), "w", encoding="utf-8").write(gen.dump(obj))


tmp = tempfile.mkdtemp(prefix="launchpad-selftest-")
try:
    # ---- T1.0 the gate: out/ is fresh against the metas (the committed catalogue IS the API)
    prev_dash, prev_all = gen.load_prev(os.path.join(OUT, "catalogue-dashboard.json")), gen.load_prev(os.path.join(OUT, "catalogue-all.json"))
    metas_sha = (prev_dash or {}).get("x-apollo", {}).get("catalogue", {}).get("metas_sha")
    t = time.perf_counter()
    dash, allc, rep, secs = quiet_build(metas_sha=metas_sha, prev_dash=prev_dash, prev_all=prev_all)
    d1 = os.path.join(tmp, "run1"); write_set(d1, dash, allc, rep)
    # the API file byte-equal; the report through gen.report_comparable (its provenance stamps —
    # git HEAD, the input files' hashes — move with every commit and are not the catalogue; #312 lane V)
    same = (os.path.exists(os.path.join(OUT, "catalogue-dashboard.json"))
            and open(os.path.join(OUT, "catalogue-dashboard.json"), "rb").read() == open(os.path.join(d1, "catalogue-dashboard.json"), "rb").read()
            and os.path.exists(os.path.join(OUT, "catalogue-report.json"))
            and gen.report_comparable(json.load(open(os.path.join(OUT, "catalogue-report.json")))) == gen.report_comparable(rep))
    check("T1.0", same, "out/catalogue-dashboard.json byte-equal + catalogue-report.json equal (stamps masked) a fresh build (%s %s, %d parts)" % (
        dash["x-apollo"]["catalogue"]["version"], dash["x-apollo"]["catalogue"]["sha256"][:12], len(dash["components"]))
          if same else "out/ is STALE or missing against the metas: run gen_catalogue.py")

    # ---- T1.1 the document validates (C1) and every entry passes E0–E4, N1, N2
    r = va.run(dash, "dashboard")
    check("T1.1", r["ok"], "C1 %s · entries %d/%d · C2 projection errors %d · N1 %s · N2 %s" % (
        r["C1_valid_2020_12_schema"], r["entries_valid"], r["entries_total"], len(r["C2_inline_projection_errors"]),
        r["N1_unknown_component_rejected"], r.get("N2_missing_required_rejected")))
    bad = {k: (v["E0_errors"] + v["E1_errors"] + v["E3_errors"] + v["E4_errors"])[:2] for k, v in r["entries"].items() if not v["valid"]}
    if bad:
        rows.append(("T1.1", "    ", "invalid: %s" % json.dumps(bad)[:400]))
    ra = va.run(allc, "all")
    check("T1.1b", ra["ok"], "by-product catalogue-all: entries %d/%d valid" % (ra["entries_valid"], ra["entries_total"]))

    # ---- T1.2 the mutation set bites
    mu = va.mutations(dash)
    check("T1.2", all(m["caught"] for m in mu), "mutations caught %d/%d: %s" % (
        sum(m["caught"] for m in mu), len(mu), "; ".join(m["mutation"].split(" (")[0] + ("" if m["caught"] else " NOT CAUGHT") for m in mu)))

    # ---- T1.3 L1 = L2 for the published set; L1/L2/L3 printed with reasons (R5's summarise rule)
    CONTENT = ("DynamicString", "DynamicNumber", "DataBinding", "ChildList", "ComponentId")
    levels, short = {}, []
    for cid, entry in dash["components"].items():
        x = entry["x-apollo"]; e = rep["entries"][x["slug"]]; g = set(e["gaps"])
        l1 = r["entries"][cid]["valid"]
        l2 = l1 and e["published"]
        content = any(c in json.dumps(v) for k, v in entry["allOf"][-1]["properties"].items() if k != "component" for c in CONTENT)
        blocks = sorted(g & {"G-WHEN", "G-SHAPE", "G-SHAPE-UNRESOLVED", "G-STATUS", "G-STATUS-BETA", "G-RULINGS"})
        if not content:
            blocks.append("G-NO-CONTENT")
        l3 = l2 and not blocks
        levels[cid] = (l1, l2, l3)
        if not l3:
            short.append("%s:%s" % (x["slug"], "+".join(blocks)))
    n1, n2, n3 = (sum(1 for v in levels.values() if v[i]) for i in range(3))
    check("T1.3", n1 == n2 == len(levels), "L1 %d · L2 %d · L3 %d of %d; short of L3: %s" % (n1, n2, n3, len(levels), ", ".join(short)))

    # ---- T1.4 no same-name loss anywhere published
    sn_all, sn_dash = rep["counts"]["same_name_losses_all"], rep["counts"]["same_name_losses_dashboard"]
    check("T1.4", sn_all == 0 and sn_dash == 0, "G-SLOT-PROP-SAME-NAME: dashboard %d, all %d (R5 measured 4 / 27)" % (sn_dash, sn_all))

    # ---- T1.5 metric carries both aliases; neither alias is its own entry
    mx = dash["components"].get("Metric", {}).get("x-apollo", {})
    check("T1.5", sorted(mx.get("aliases", [])) == ["kpi-tile", "stat-card"] and "StatCard" not in dash["components"] and "KpiTile" not in dash["components"],
          "Metric.aliases = %s; StatCard entry %s, KpiTile entry %s" % (mx.get("aliases"), "StatCard" in dash["components"], "KpiTile" in dash["components"]))

    # ---- T1.6 determinism and the version policy
    dash2, allc2, rep2, _ = quiet_build(metas_sha=metas_sha, prev_dash=prev_dash, prev_all=prev_all)
    d2 = os.path.join(tmp, "run2"); write_set(d2, dash2, allc2, rep2)
    ident = all(open(os.path.join(d1, fn), "rb").read() == open(os.path.join(d2, fn), "rb").read()
                for fn in ("catalogue-dashboard.json", "catalogue-all.json", "catalogue-report.json"))
    check("T1.6", ident, "two builds on metas_sha %s byte-identical (3 files); sha256 %s" % (
        dash["x-apollo"]["catalogue"]["metas_sha"], dash["x-apollo"]["catalogue"]["sha256"][:12]))
    fake_prev = copy.deepcopy(dash); fake_prev["x-apollo"]["catalogue"]["sha256"] = "0" * 64
    d3, _, _, _ = quiet_build(metas_sha=metas_sha, prev_dash=fake_prev, prev_all=None)
    st3 = d3["x-apollo"]["catalogue"]
    d4, _, _, _ = quiet_build(metas_sha=metas_sha, prev_dash=d3, prev_all=None)
    st4 = d4["x-apollo"]["catalogue"]
    bumped = (st3["version"] == gen.bump_patch(dash["x-apollo"]["catalogue"]["version"]) and st3["previous"] == {"version": dash["x-apollo"]["catalogue"]["version"], "sha256": "0" * 64}
              and d3["catalogId"].endswith("/" + st3["version"] + "/catalog.json") and st4["version"] == st3["version"] and st4["previous"] == st3["previous"])
    check("T1.6b", bumped, "entries changed ⇒ %s → %s with previous kept; unchanged ⇒ %s stays" % (dash["x-apollo"]["catalogue"]["version"], st3["version"], st4["version"]))

    # ---- T1.7 the generator's own time, n=3, and the reserved-domain catalogId
    times = [secs]
    for _ in range(2):
        times.append(quiet_build(metas_sha=metas_sha, prev_dash=prev_dash, prev_all=prev_all)[3])
    cid_ok = dash["catalogId"].startswith(gen.CATALOG_BASE + "dashboard/v") and dash["catalogId"] == dash["$id"]
    check("T1.7", cid_ok, "build time n=3: %s s (median %.3f); catalogId %s" % (times, sorted(times)[1], dash["catalogId"]))

    # ---- T1.8 lane L's fields are read if present, never required
    spec_n = rep["counts"]["spec_fields_present"]
    pub_expected = rep["counts"]["metas_real"] - rep["counts"]["aliases"] - rep["counts"]["unpublished_deprecated"] - rep["counts"]["unpublished_schema"]
    check("T1.8", rep["counts"]["published_all"] == pub_expected,
          "x-apollo.spec present on %d dashboard parts (anatomy/states/emits/bindings, s311-D4); published %d = %d metas − %d aliases − %d deprecated − %d schema-failed" % (
              spec_n, rep["counts"]["published_all"], rep["counts"]["metas_real"], rep["counts"]["aliases"], rep["counts"]["unpublished_deprecated"], rep["counts"]["unpublished_schema"]))

    # ---- T1.8b lane L's four fields, when a meta carries them (and the schema allows them), ride under x-apollo.spec
    schema = json.load(open(os.path.join(ROOT, "knowledge", "components", "meta.schema.json")))
    for f in ("anatomy", "states", "emits", "bindings", "$extracted"):
        schema["properties"].setdefault(f, {})       # L1 adds them today; the selftest does not wait for it
    four = {"anatomy": {"part": "metric", "tag": "div", "children": []}, "states": {"states": ["ready"], "initial": "ready"},
            "emits": [{"name": "metric-select", "detail": {}}], "bindings": {"--metric-ink": "{text.default}"},
            "$extracted": {"by": "selftest", "date": "2026-10-01", "reviewed": False}}
    d6, _, rep6, _ = quiet_build(metas_sha=metas_sha, prev_dash=prev_dash, prev_all=prev_all, overlay={"metas": {"metric": four}, "schema": schema})
    spec6 = d6["components"]["Metric"]["x-apollo"].get("spec")
    r6 = va.run(d6, "overlay")
    others_same = all(d6["components"][c] == dash["components"][c] for c in dash["components"] if c != "Metric")
    # the count moves by one unless metric already carries a spec on disk (L2's drafts; #312 lane V — the
    # selftest hard-coded today's zero and went red the moment a real draft landed on a dashboard part)
    spec_expected = spec_n + (0 if dash["components"]["Metric"]["x-apollo"].get("spec") else 1)
    check("T1.8b", spec6 == four and r6["ok"] and others_same and rep6["counts"]["spec_fields_present"] == spec_expected,
          "a meta carrying anatomy/states/emits/bindings publishes them under x-apollo.spec (Metric: %s), entry still A2UI-valid %d/%d, other entries unchanged %s" % (
              sorted(spec6 or {}), r6["entries_valid"], r6["entries_total"], others_same))

    # ---- T1.9 the gate bites: a stale out/ is refused by --check
    d5 = os.path.join(tmp, "stale"); shutil.copytree(d1, d5)
    stale = json.load(open(os.path.join(d5, "catalogue-dashboard.json")))
    stale["components"]["Button"]["allOf"][-1]["properties"]["label"] = {"type": "string"}
    stale["x-apollo"]["catalogue"]["sha256"] = "f" * 64
    open(os.path.join(d5, "catalogue-dashboard.json"), "w", encoding="utf-8").write(gen.dump(stale))
    rc_stale = subprocess.run([sys.executable, os.path.join(HERE, "gen_catalogue.py"), "--check", "--out", d5], capture_output=True, text=True).returncode
    rc_fresh = subprocess.run([sys.executable, os.path.join(HERE, "gen_catalogue.py"), "--check", "--out", d1, "--metas-sha", str(metas_sha)], capture_output=True, text=True).returncode
    check("T1.9", rc_stale == 1 and rc_fresh == 0, "--check on a tampered copy exit %d (want 1); on a fresh copy exit %d (want 0)" % (rc_stale, rc_fresh))
    # ---- T1.9b the gate reads the BODY, not the stamp: an entry tampered under an untouched sha256 is refused
    d6 = os.path.join(tmp, "stale-body"); shutil.copytree(d1, d6)
    body = json.load(open(os.path.join(d6, "catalogue-dashboard.json")))
    body["components"]["Button"]["x-apollo"]["slug"] = "tampered"
    open(os.path.join(d6, "catalogue-dashboard.json"), "w", encoding="utf-8").write(gen.dump(body))
    rc_body = subprocess.run([sys.executable, os.path.join(HERE, "gen_catalogue.py"), "--check", "--out", d6, "--metas-sha", str(metas_sha)], capture_output=True, text=True).returncode
    # and the git stamp alone never stales it: a different --metas-sha on a fresh copy still passes
    rc_sha = subprocess.run([sys.executable, os.path.join(HERE, "gen_catalogue.py"), "--check", "--out", d1, "--metas-sha", "0000000f"], capture_output=True, text=True).returncode
    check("T1.9b", rc_body == 1 and rc_sha == 0, "--check on a body-tampered copy under its old stamp exit %d (want 1); on a fresh copy stamped with another git sha exit %d (want 0)" % (rc_body, rc_sha))

    # ---- T1.10 a data setting takes a binding (#313 lane C1F; lane C3's F2). Every data setting typed
    # object-or-binding or array-or-binding is driven inside its own entry: a bound value passes; literal data
    # passes; a bare word, a non-string path and a binding with a stray key stay refused. Bite: the pre-fix
    # object branch (no `not path`) refuses the bound value again on every object-typed setting.
    reg10 = va.registry(dash)
    data_props = []
    for cid, entry in sorted(dash["components"].items()):
        for k, sch in sorted((entry["allOf"][-1].get("properties") or {}).items()):
            alts = sch.get("oneOf") or []
            if any((a.get("$ref") or "").endswith("DataBinding") for a in alts) and any(a.get("type") in ("object", "array") for a in alts):
                data_props.append((cid, k, "object" if any(a.get("type") == "object" for a in alts) else "array"))

    def entry_ok(cat_, cid, k, v):
        inst = va.full(cid, cat_["components"][cid]); inst[k] = v
        return not va.errs({"$ref": va.CATALOG_URI + "#/components/" + cid}, inst, va.registry(cat_) if cat_ is not dash else reg10)
    bad10, n_obj, bitten = [], 0, 0
    for cid, k, kind in data_props:
        want = [({"path": "/data/x"}, True), ([], True), ("x", False), ({"path": 5}, False), ({"path": "/data/x", "probe": 1}, False)]
        if kind == "object":
            want.append(({"series": [{"name": "a", "values": [1]}]}, True))
        for v, exp in want:
            if entry_ok(dash, cid, k, v) != exp:
                bad10.append("%s.%s %s want %s" % (cid, k, json.dumps(v), "pass" if exp else "refused"))
        if kind == "object":
            n_obj += 1
            pre = copy.deepcopy(dash)
            for br in pre["components"][cid]["allOf"][-1]["properties"][k]["oneOf"]:
                br.pop("not", None)
            bitten += not entry_ok(pre, cid, k, {"path": "/data/x"})
    check("T1.10", data_props and not bad10 and n_obj and bitten == n_obj,
          "data settings taking a binding: %d (%d object-or-binding, %d array-or-binding); bound value passes, literal data passes, "
          "bare word / non-string path / stray key refused on every one%s; bite: the pre-fix oneOf refuses the bound value on %d/%d object-typed settings" % (
              len(data_props), n_obj, len(data_props) - n_obj, (" — WRONG: " + "; ".join(bad10[:4])) if bad10 else "", bitten, n_obj))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("catalogue selftest — %s\n" % ("GREEN" if not failed else "RED (%d)" % failed))
for tid, st, detail in rows:
    print("%-6s %-4s %s" % (tid, st, detail))
print("\ncatalogue %s %s sha256 %s metas_sha %s parts %d" % (dash["x-apollo"]["catalogue"]["name"], dash["x-apollo"]["catalogue"]["version"],
                                                           dash["x-apollo"]["catalogue"]["sha256"], dash["x-apollo"]["catalogue"]["metas_sha"], len(dash["components"])))
sys.exit(1 if failed else 0)
