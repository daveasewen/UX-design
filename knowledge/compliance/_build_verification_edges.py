#!/usr/bin/env python3
"""_build_verification_edges.py — layer the VERIFIED edge onto the compliance graph.

Context (2026-07-14 design direction, folded into ADR-0003's reopened thread):
`compliance/graph-index.json`'s applies_to is the CLAIMED edge — a component
meta asserts it satisfies a WCAG SC. That's bookkeeping, not enforcement. This
generator adds the second, orthogonal edge type Dave specified: verified_by —
non-null only where an executable check is actually wired into the build AND
currently passes. Turns "which SCs are covered" into "which SCs are covered
vs which are only claimed."

This is a THIN layer, not a new source of truth: it reads the evidence that
other generators/gates already produce (contrast audits, the a11y gate) and
annotates the compliance rule files + graph-index.json with what it found.
It does not run any checks itself and does not gate the build — advisory only,
same as the other bookkeeping steps in _build_all.py. Must run AFTER the
generators/gates whose output it reads (see _build_all.py step order).

VERIFY_MAP below is hand-authored and deliberately small: only SCs with a real,
currently-running, machine-checkable mechanism are listed. Every other SC in
the compliance graph is left verified_by: null — that is the honest answer for
a manual/semi-automated check.type today, not a gap in this script.

Granularity caveat (logged, not hidden): the contrast audits check design
TOKENS, not components directly. A component's verified_by=pass for 1.4.3/1.4.11
means "the tokens available to bind for text/icon colour all clear the
threshold in the current store," not "this exact component instance was
tested." True per-component verification for those two SCs needs the
token-blast-radius join (component -> tokens it binds -> are those tokens
clean) — flagged as NEXT, not built here. The a11y gate (2.3.3, 2.5.8) DOES
check per snippet, i.e. per component, today — see 'granularity' below.
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))          # knowledge/compliance
ROOT = os.path.dirname(HERE)                                # knowledge/
RULES = os.path.join(HERE, "rules")
GRAPH_INDEX = os.path.join(HERE, "graph-index.json")


def read_json(path):
    if not os.path.exists(path):
        return None
    return json.load(open(path))


def contrast_result(artifact_name, poor_key="poor_contrast"):
    """pass iff the audit ran and recorded zero non-allowlisted failures."""
    data = read_json(os.path.join(ROOT, artifact_name))
    if data is None:
        return None, "artifact not found — run the audit first"
    poor = data.get(poor_key, [])
    return ("pass" if not poor else "fail"), None


def a11y_gate_result(sc_marker):
    """Count FAIL lines in _A11Y-GATE.md mentioning this SC. No JSON export
    exists for this gate yet, so we parse the human-readable report — every
    FAIL line already embeds its SC in parentheses (see _validate_a11y.py)."""
    path = os.path.join(ROOT, "_A11Y-GATE.md")
    if not os.path.exists(path):
        return None, "artifact not found — run the a11y gate first"
    text = open(path).read()
    fail_lines = [l for l in text.splitlines() if l.strip().startswith("- 🔴 FAIL")]
    matching = [l for l in fail_lines if sc_marker in l]
    return ("fail" if matching else "pass"), None


TODAY = datetime.date.today().isoformat()

# sc -> (script, artifact, mechanism, granularity, result_fn)
VERIFY_MAP = {
    "1.4.3": (
        "_build_surface_contrast_audit.py", "_TEXT-CONTRAST-AUDIT.json",
        "Every text/icon token in the store is contrast-checked at 4.5:1 against its worst-case dark surface; gates the build on any non-allowlisted failure.",
        "token",
        lambda: contrast_result("_TEXT-CONTRAST-AUDIT.json"),
    ),
    "1.4.11": (
        "_build_indicator_contrast_audit.py", "_INDICATOR-CONTRAST-AUDIT.json",
        "Brand/RAG/interactive-state tokens are contrast-checked at 3:1 against their worst-case dark surface; gates the build on any non-allowlisted failure.",
        "token",
        lambda: contrast_result("_INDICATOR-CONTRAST-AUDIT.json"),
    ),
    "2.3.3": (
        "_validate_a11y.py", "_A11Y-GATE.md",
        "Every reference snippet is scanned for transition/animation/@keyframes usage; if present, a prefers-reduced-motion escape hatch is required. Gates the build per snippet (= per component).",
        "component",
        lambda: a11y_gate_result("2.3.3"),
    ),
    "2.5.8": (
        "_validate_a11y.py", "_A11Y-GATE.md",
        "Every interactive control's declared CSS box is measured against the 24px hard floor (aid-009 ruling); below-floor with no hit-area expander gates the build per snippet (= per component). The 24-43px band is reported as a warning, not gated — that part stays semi-automated by design.",
        "component",
        lambda: a11y_gate_result("2.5.8"),
    ),
}


def main():
    index = read_json(GRAPH_INDEX)
    if index is None:
        print("ERROR: compliance/graph-index.json not found — run _build_compliance_kg.py first.")
        sys.exit(0)  # advisory step: never aborts the build

    verification = {}
    rows = []
    for sc in sorted(index.get("by_sc", {})):
        if sc not in VERIFY_MAP:
            verification[sc] = None
            rows.append((sc, "unverified", None, None, None))
            continue
        script, artifact, mechanism, granularity, result_fn = VERIFY_MAP[sc]
        result, err = result_fn()
        if result is None:
            verification[sc] = None
            rows.append((sc, "unverified", None, None, err))
            continue
        vb = {
            "script": script, "artifact": artifact, "mechanism": mechanism,
            "granularity": granularity, "result": result, "checked": TODAY,
        }
        verification[sc] = vb
        rows.append((sc, "verified", result, granularity, None))

        # patch the individual rule file
        rule_id = None
        for rid in index.get("rules", []):
            if rid.startswith(f"wcag-{sc}-"):
                rule_id = rid
                break
        if rule_id:
            rule_path = os.path.join(RULES, rule_id + ".json")
            rule = read_json(rule_path)
            if rule is not None:
                rule["verified_by"] = vb
                json.dump(rule, open(rule_path, "w"), indent=2, ensure_ascii=False)

    index["verification"] = {
        "$description": "SC -> verified_by-or-null. null = applies_to is asserted only, no executable check wired into the build. Non-null = an executable check runs in _build_all.py and this is its current result. See knowledge/compliance/_build_verification_edges.py.",
        "generated": TODAY,
        "totals": {
            "sc": len(verification),
            "verified": sum(1 for v in verification.values() if v is not None),
            "unverified": sum(1 for v in verification.values() if v is None),
        },
        "by_sc": verification,
    }
    json.dump(index, open(GRAPH_INDEX, "w"), indent=2, ensure_ascii=False)

    # --- human-readable report ---
    verified_rows = [r for r in rows if r[1] == "verified"]
    unverified_rows = [r for r in rows if r[1] == "unverified"]
    L = [
        "# Compliance graph — verified edges",
        "",
        "> Layers the VERIFIED edge (`verified_by`) onto the compliance graph's existing CLAIMED edge (`applies_to`). "
        "Generated by `_build_verification_edges.py` — advisory, does not gate the build. Regenerate via `knowledge/_build_all.py` "
        "(must run after the contrast audits and the a11y gate).",
        "",
        f"**{len(verified_rows)}/{len(rows)} SCs have an executable check wired into the current build.** "
        f"The other {len(unverified_rows)} are applies_to-only — asserted by component metas, not machine-checked. "
        "That is expected for genuinely manual SCs (e.g. 2.1.1 Keyboard) and is not itself a defect.",
        "",
        "## Verified",
        "",
        "| SC | Result | Granularity | Script |",
        "|---|---|---|---|",
    ]
    for sc, _, result, granularity, _ in verified_rows:
        badge = "✅ pass" if result == "pass" else "❌ fail"
        script = VERIFY_MAP[sc][0]
        L.append(f"| {sc} | {badge} | {granularity} | `{script}` |")
    L += ["", "## Unverified (applies_to only)", ""]
    if unverified_rows:
        L += ["| SC | Note |", "|---|---|"]
        for sc, _, _, _, err in unverified_rows:
            L.append(f"| {sc} | {err or 'no executable check in this build'} |")
    else:
        L.append("_None — every SC has a wired check._")
    L += [
        "",
        "## Granularity caveat",
        "",
        "`1.4.3` and `1.4.11` are verified at **token** granularity — every colour token in the store clears the "
        "threshold, not \"this exact component instance was audited.\" Getting to true per-component verification for "
        "those two needs the token blast-radius join (component -> tokens it binds -> are those tokens clean) — "
        "logged as next work, not built here. `2.3.3` and `2.5.8` verify at **component** granularity already, because "
        "the a11y gate runs per reference snippet (one per component).",
        "",
    ]
    open(os.path.join(ROOT, "_VERIFICATION-EDGES.md"), "w").write("\n".join(L) + "\n")

    print(f"verification edges: {len(verified_rows)}/{len(rows)} SCs verified "
          f"({sum(1 for r in verified_rows if r[2]=='fail')} failing), {len(unverified_rows)} applies_to-only")
    for sc, status, result, granularity, err in rows:
        if status == "verified":
            print(f"  {'✅' if result=='pass' else '❌'} {sc}: {result} ({granularity})")
    sys.exit(0)  # advisory — never gates


if __name__ == "__main__":
    main()
