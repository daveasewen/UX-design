#!/usr/bin/env python3
"""probe_meta_schema.py — P-1: component META vs META SCHEMA sweep (W-45 probe registry).

THE CLASS, from the receipts: at #204 the adversarial verifier (challenge C-8) validated
`knowledge/components/*.meta.json` against `knowledge/components/meta.schema.json` and found
THREE authored metas non-conformant — `document-row` (stateModel enum, unexpected edge types,
non-`$` annotation keys), `payment-card-visual` and `runway-bar` (300-char prose in the
`provenance.source` ENUM). Every one of them had been written, reviewed and committed with the
whole gate chain green: NO GATE VALIDATES A META AGAINST ITS OWN SCHEMA
[[no-gate-parses-the-artefact]]. The fix pass repaired them the same session
(`notes/_receipts/2026-08-19-204-buildpm-claim-table.md` FIX 1: BEFORE 92 metas PASS=88 FAIL=4,
AFTER PASS=91 FAIL=1).

WHAT THIS PROBE DOES: Draft7 validation of every `knowledge/components/*.meta.json` against
`knowledge/components/meta.schema.json`. Loud and named: file · JSON pointer · message.

EXEMPT, declared not silent: `EXAMPLE-button.meta.json` — the pre-existing TEMPLATE the #204
verifier itself put out of scope (it fails `tokenValidation` required-property by design). It
is printed as EXEMPT on every run, never hidden. `--no-exempt` removes the exemption.

★ #311 lane C0 — THREE RULE ARMS the Draft 7 schema cannot express, run after the sweep and counted in
the same findings number (s305-D17/D18/D19/D58, Dave, #305):
  SAME-NAME      a name is a setting OR a slot, never both (s305-D19 + s305-D58): a `props[].name` equal to a
                 `slots` key is refused. Draft 7 cannot compare keys across two members, so the rule lives here.
  SHAPE-UNKNOWN  a setting's `bindsData.shape` must be an ADDRESS into knowledge/shapes.json (a closed store).
  ROLE-UNKNOWN   a slot's `accepts.provides` must name roles in knowledge/roles.json `roles` (s305-D18).
The schema itself refuses `ownText` on anything but a string, a number or an array (s305-D17).

⛔ WHAT IT CANNOT SEE: whether the meta is TRUE. Schema conformance is a grammar check — a meta
can name the wrong token, the wrong component or a nonexistent edge target and pass. It also
cannot see a schema that is itself wrong; widening vs repairing is an OPEN QUESTION TO DAVE
recorded at #204 and this probe does not touch it.

ENVIRONMENT: sandbox (pure python + `jsonschema`). Runs in CI too IF `jsonschema` is present
there — UNVERIFIED by this lane, declared rather than assumed (#173 environment split).

USAGE
  python3 knowledge/_probe_registry/probe_meta_schema.py --check
  python3 knowledge/_probe_registry/probe_meta_schema.py --check --dir <alt-dir>
  python3 knowledge/_probe_registry/probe_meta_schema.py --selftest
EXIT: 0 clean · 1 findings (or a missing dependency, declared) · 2 bad invocation.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
COMPONENTS = os.path.join(ROOT, "knowledge", "components")
SCHEMA = os.path.join(COMPONENTS, "meta.schema.json")
EXEMPT = ("EXAMPLE-button.meta.json",)


def sweep(directory=COMPONENTS, schema_path=None, exempt=EXEMPT, verbose=True):
    """Return (findings, exempt_fails, checked). findings = [(file, pointer, message)]."""
    try:
        import jsonschema
    except ImportError:
        print("⛔ NOT-IN-THIS-ENVIRONMENT: `jsonschema` is not importable. This is a DECLARED "
              "gap, not a pass — the probe refuses to guess (feedback-measuring-tool-must-not-guess).")
        return None, None, 0
    schema_path = schema_path or os.path.join(directory, "meta.schema.json")
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft7Validator(schema)
    findings, exempt_fails, checked = [], [], 0
    for path in sorted(glob.glob(os.path.join(directory, "*.meta.json"))):
        name = os.path.basename(path)
        checked += 1
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            findings.append((name, "<parse>", "not valid JSON — %s" % e))
            continue
        errs = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
        for e in errs:
            ptr = "/".join(str(p) for p in e.absolute_path) or "<root>"
            row = (name, ptr, e.message.replace("\n", " ")[:200])
            (exempt_fails if name in exempt else findings).append(row)
    if verbose:
        for name, ptr, msg in findings:
            print("  ⛔ %s [%s] %s" % (name, ptr, msg))
        for name, ptr, msg in exempt_fails:
            print("  ⚪ EXEMPT (declared, never hidden) %s [%s] %s" % (name, ptr, msg))
    return findings, exempt_fails, checked


def _stores(directory):
    """the two closed stores the rule arms resolve against; they live beside the components directory."""
    k = os.path.dirname(os.path.abspath(directory))
    if not os.path.exists(os.path.join(k, "shapes.json")):   # a selftest copy of components/ alone: read the live stores
        k = os.path.dirname(COMPONENTS)
    shapes = set(json.load(open(os.path.join(k, "shapes.json"), encoding="utf-8"))["shapes"])
    roles = set(json.load(open(os.path.join(k, "roles.json"), encoding="utf-8"))["roles"])
    return shapes, roles


def rules(directory=COMPONENTS, exempt=EXEMPT, verbose=True, stores=None):
    """#311 C0 — the three rule arms (SAME-NAME, SHAPE-UNKNOWN, ROLE-UNKNOWN). Returns [(file, arm, message)]."""
    shapes, roles = stores or _stores(directory)
    out = []
    for path in sorted(glob.glob(os.path.join(directory, "*.meta.json"))):
        name = os.path.basename(path)
        if name in exempt:
            continue
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue                      # the sweep already names a parse failure
        props = [p for p in (doc.get("props") or []) if isinstance(p, dict)]
        slots = {k: v for k, v in (doc.get("slots") or {}).items() if not k.startswith("$") and isinstance(v, dict)}
        for p in props:
            if p.get("name") in slots:
                out.append((name, "SAME-NAME", "%r is both a setting and a slot (s305-D19/D58: one or the other)" % p["name"]))
            sh = (p.get("bindsData") or {}).get("shape") if isinstance(p.get("bindsData"), dict) else None
            if sh is not None and sh not in shapes:
                out.append((name, "SHAPE-UNKNOWN", "setting %r binds shape %r, not in knowledge/shapes.json" % (p.get("name"), sh)))
        for sn, sd in slots.items():
            for r in ((sd.get("accepts") or {}).get("provides") or []):
                if r not in roles:
                    out.append((name, "ROLE-UNKNOWN", "slot %r accepts role %r, not in knowledge/roles.json" % (sn, r)))
    if verbose:
        for f, arm, msg in out:
            print("  ⛔ %s [%s] %s" % (f, arm, msg))
    return out


def check(directory=COMPONENTS):
    findings, exempt_fails, checked = sweep(directory)
    if findings is None:
        print("PROBE P-1 — findings=UNKNOWN (dependency missing)")
        return 1
    ruled = rules(directory)
    print("P-1 meta-schema sweep: %d meta(s) checked · %d finding(s) · %d exempt failure(s) "
          "(%s)" % (checked, len(findings), len(exempt_fails), ", ".join(EXEMPT)))
    print("P-1 rule arms (s305-D17/D18/D19/D58): SAME-NAME · SHAPE-UNKNOWN · ROLE-UNKNOWN — %d finding(s)" % len(ruled))
    print("PROBE P-1 — findings=%d" % (len(findings) + len(ruled)))
    return 1 if (findings or ruled) else 0


def selftest():
    """PLANT-THEN-DETECT, both directions, DRIVING THE PROBE on a real planted artefact
    [[mutation-tests-the-clause-not-the-feature]] — a copy of the REAL meta directory, with a
    real schema violation written into a real meta file."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="p1-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    work = os.path.join(tmp, "components")
    shutil.copytree(COMPONENTS, work)

    # direction 1 — CLEAN: the copied tree must behave exactly like the live one
    base, base_exempt, checked = sweep(work, verbose=False)
    if base is None:
        print("⛔ selftest cannot run: jsonschema missing (declared, not a pass)")
        return 1
    print("  · baseline on a copy of the real tree: %d meta(s), %d finding(s), %d exempt"
          % (checked, len(base), len(base_exempt)))

    # direction 2 — PLANT the EXACT #204 shape into a real meta and DRIVE the probe
    victim = os.path.join(work, "progress-bar.meta.json")
    if not os.path.exists(victim):
        victim = sorted(p for p in glob.glob(os.path.join(work, "*.meta.json"))
                        if os.path.basename(p) not in EXEMPT)[0]
    doc = json.load(open(victim, encoding="utf-8"))
    doc["stateModel"] = "interactive"          # #204 C-8 defect 1, verbatim
    doc["howThisDiffersFromFileUpload"] = "a non-$ annotation key"  # #204 C-8 defect 3
    json.dump(doc, open(victim, "w", encoding="utf-8"), indent=2)
    planted, _, _ = sweep(work, verbose=False)
    new = [f for f in planted if f not in base]
    if not new:
        fails.append("PLANT NOT CAUGHT: a `stateModel: interactive` + non-$ key planted in %s "
                     "produced no new finding" % os.path.basename(victim))
    else:
        print("  ✅ plant caught: %s" % "; ".join("%s [%s] %s" % f for f in new[:2]))

    # direction 2b — #311 C0: one plant per new clause, each on a fresh copy, each must be caught
    base_rules = rules(work, verbose=False)
    print("  · rule-arm baseline on the copy: %d finding(s)" % len(base_rules))

    def _fresh():
        shutil.rmtree(work)
        shutil.copytree(COMPONENTS, work)

    def _plant(fname, mutate):
        pth = os.path.join(work, fname)
        d = json.load(open(pth, encoding="utf-8"))
        mutate(d)
        json.dump(d, open(pth, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    def _p_same(d):          # re-open the clash s305-D19 closed: chart-line's data setting gets its slot back
        d.setdefault("slots", {})["data"] = {"accepts": {"capability": ["chart-dataset"]}, "use": "planted"}

    def _p_shape(d):
        next(p for p in d["props"] if p.get("bindsData"))["bindsData"]["shape"] = "planted × nothing"

    def _p_role(d):
        d["slots"]["tiles"]["accepts"]["provides"] = ["headline-metric", "planted-role"]

    def _p_owntext(d):       # ownText on a boolean: the schema clause
        next(p for p in d["props"] if p.get("type") == "boolean")["ownText"] = True

    for label, fname, mut, arm in (
            ("SAME-NAME", "chart-line.meta.json", _p_same, "SAME-NAME"),
            ("SHAPE-UNKNOWN", "chart-line.meta.json", _p_shape, "SHAPE-UNKNOWN"),
            ("ROLE-UNKNOWN", "template-dashboard-bento.meta.json", _p_role, "ROLE-UNKNOWN"),
            ("ownText on a boolean (schema)", "accordion.meta.json", _p_owntext, None)):
        _fresh()
        if not os.path.exists(os.path.join(work, fname)):
            fails.append("PLANT %s: %s is not in the tree" % (label, fname))
            continue
        _plant(fname, mut)
        if arm:
            got = [r for r in rules(work, verbose=False) if r not in base_rules and r[1] == arm]
        else:
            s2, _, _ = sweep(work, verbose=False)
            got = [f for f in s2 if f not in base and f[0] == fname]
        if got:
            print("  ✅ plant caught (%s): %s" % (label, " ".join(str(x) for x in got[0])[:160]))
        else:
            fails.append("PLANT NOT CAUGHT: %s planted in %s produced no new finding" % (label, fname))
    if base_rules:
        fails.append("CONTROL: the live tree carries %d rule-arm finding(s); the baseline must be 0" % len(base_rules))

    # direction 3 — REMOVE the plant, the probe must go back to baseline (silence)
    shutil.rmtree(work)
    shutil.copytree(COMPONENTS, work)
    after, _, _ = sweep(work, verbose=False)
    after_rules = rules(work, verbose=False)
    if after_rules != base_rules:
        fails.append("REMOVAL NOT GREEN (rule arms): restored tree gave %d, baseline was %d" % (len(after_rules), len(base_rules)))
    if after != base:
        fails.append("REMOVAL NOT GREEN: restored tree gave %d finding(s), baseline was %d"
                     % (len(after), len(base)))
    else:
        print("  ✅ removal green: with the plant gone the probe returns to baseline (%d)"
              % len(base))

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-1 selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ P-1 selftest PASS — planted schema defect detected on a REAL meta, removal green.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    d = COMPONENTS
    if "--dir" in argv:
        d = argv[argv.index("--dir") + 1]
    sys.exit(check(d))
