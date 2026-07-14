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
other generators/gates already produce (contrast audits, the a11y gate, the
token blast-radius index) and annotates the compliance rule files +
graph-index.json with what it found. It does not run any checks itself and
does not gate the build — advisory only, same as the other bookkeeping steps
in _build_all.py. Must run AFTER the generators/gates whose output it reads
(see _build_all.py step order).

VERIFY_MAP below is hand-authored and deliberately small: only SCs with a real,
currently-running, machine-checkable mechanism are listed. Every other SC in
the compliance graph is left verified_by: null — that is the honest answer for
a manual/semi-automated check.type today, not a gap in this script.

Granularity (2026-07-14, updated): 1.4.3 and 1.4.11 now verify at COMPONENT
granularity via the token blast-radius join (component -> tokens it binds ->
are those tokens clean), not just at token granularity — see
`contrast_component_join()`. A component only gets a real pass/fail if the
blast-radius scan actually found it binding one of the audited tokens;
otherwise it's flagged "not_covered", which is an honest gap (either the
component genuinely doesn't touch text/icon or indicator colour, or the
blast-radius scanner's meta-text matching missed it — see its own
docstring caveat about prose-only references). 2.3.3 and 2.5.8 already
verified at component granularity (the a11y gate runs per reference snippet).
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))          # knowledge/compliance
ROOT = os.path.dirname(HERE)                                # knowledge/
RULES = os.path.join(HERE, "rules")
GRAPH_INDEX = os.path.join(HERE, "graph-index.json")
BLAST_RADIUS = os.path.join(ROOT, "tokens", "_blast-radius.json")


def read_json(path):
    if not os.path.exists(path):
        return None
    return json.load(open(path))


def contrast_component_join(artifact_name, applies_to_components, poor_key="poor_contrast"):
    """Join a token-level contrast audit down to component granularity via the
    blast-radius reverse index (component -> tokens it binds).

    Returns (overall_result, per_component dict, coverage note, error-or-None).
    per_component[component] in {"pass","fail","not_covered"}.
    "not_covered" = blast-radius found no audited token bound by this
    component — not claimed as a pass, logged as a real gap instead.
    """
    audit = read_json(os.path.join(ROOT, artifact_name))
    if audit is None:
        return None, {}, None, "audit artifact not found — run it first"
    blast = read_json(BLAST_RADIUS)
    if blast is None:
        return None, {}, None, "tokens/_blast-radius.json not found — run tokens/_build_blast_radius.py first"

    audited_tokens = audit.get("tokens", {})          # token -> {status, ...}
    by_component = blast.get("by_component", {})       # component -> [tokens]
    poor = audit.get(poor_key, [])
    overall = "pass" if not poor else "fail"

    per_component = {}
    for comp in applies_to_components:
        bound = set(by_component.get(comp, []))
        relevant = bound & set(audited_tokens)
        if not relevant:
            per_component[comp] = "not_covered"
            continue
        statuses = {audited_tokens[t]["status"] for t in relevant}
        per_component[comp] = "fail" if "POOR_CONTRAST" in statuses else "pass"

    covered = sum(1 for v in per_component.values() if v != "not_covered")
    coverage = f"{covered}/{len(applies_to_components)} applies_to components have a bound audited token"
    return overall, per_component, coverage, None


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
# result_fn signature varies: contrast SCs take applies_to_components (bound below);
# a11y SCs take none. Resolved per-SC in main().
VERIFY_MAP = {
    "1.4.3": (
        "_build_surface_contrast_audit.py + tokens/_build_blast_radius.py", "_TEXT-CONTRAST-AUDIT.json",
        "Every text/icon token in the store is contrast-checked at 4.5:1 against its worst-case dark surface (gates the build); joined down to component granularity via the token blast-radius reverse index.",
        "component",
        "contrast", "_TEXT-CONTRAST-AUDIT.json",
    ),
    "1.4.11": (
        "_build_indicator_contrast_audit.py + tokens/_build_blast_radius.py", "_INDICATOR-CONTRAST-AUDIT.json",
        "Brand/RAG/interactive-state tokens are contrast-checked at 3:1 against their worst-case dark surface (gates the build); joined down to component granularity via the token blast-radius reverse index.",
        "component",
        "contrast", "_INDICATOR-CONTRAST-AUDIT.json",
    ),
    "2.3.3": (
        "_validate_a11y.py", "_A11Y-GATE.md",
        "Every reference snippet is scanned for transition/animation/@keyframes usage; if present, a prefers-reduced-motion escape hatch is required. Gates the build per snippet (= per component).",
        "component",
        "a11y", "2.3.3",
    ),
    "2.5.8": (
        "_validate_a11y.py", "_A11Y-GATE.md",
        "Every interactive control's declared CSS box is measured against the 24px hard floor (aid-009 ruling); below-floor with no hit-area expander gates the build per snippet (= per component). The 24-43px band is reported as a warning, not gated — that part stays semi-automated by design.",
        "component",
        "a11y", "2.5.8",
    ),
}


def main():
    index = read_json(GRAPH_INDEX)
    if index is None:
        print("ERROR: compliance/graph-index.json not found — run _build_compliance_kg.py first.")
        sys.exit(0)  # advisory step: never aborts the build

    verification = {}
    rows = []  # (sc, status, result, granularity, coverage_or_err, per_component)
    for sc in sorted(index.get("by_sc", {})):
        if sc not in VERIFY_MAP:
            verification[sc] = None
            rows.append((sc, "unverified", None, None, None, None))
            continue
        script, artifact, mechanism, granularity, kind, key = VERIFY_MAP[sc]

        per_component = None
        coverage = None
        if kind == "contrast":
            applies_to_components = index.get("by_sc", {}).get(sc, [])
            result, per_component, coverage, err = contrast_component_join(key, applies_to_components)
        else:
            result, err = a11y_gate_result(key)

        if result is None:
            verification[sc] = None
            rows.append((sc, "unverified", None, None, err, None))
            continue

        vb = {
            "script": script, "artifact": artifact, "mechanism": mechanism,
            "granularity": granularity, "result": result, "checked": TODAY,
        }
        if per_component is not None:
            vb["per_component"] = per_component
            vb["coverage"] = coverage
        verification[sc] = vb
        rows.append((sc, "verified", result, granularity, coverage, per_component))

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
        "$description": "SC -> verified_by-or-null. null = applies_to is asserted only, no executable check wired into the build. Non-null = an executable check runs in _build_all.py and this is its current result. contrast SCs (1.4.3/1.4.11) additionally carry per_component (via the token blast-radius join) and a coverage note. See knowledge/compliance/_build_verification_edges.py.",
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
        "(must run after the contrast audits, the a11y gate, and the token blast-radius index).",
        "",
        f"**{len(verified_rows)}/{len(rows)} SCs have an executable check wired into the current build.** "
        f"The other {len(unverified_rows)} are applies_to-only — asserted by component metas, not machine-checked. "
        "That is expected for genuinely manual SCs (e.g. 2.1.1 Keyboard) and is not itself a defect.",
        "",
        "## Verified",
        "",
        "| SC | Result | Granularity | Coverage |",
        "|---|---|---|---|",
    ]
    for sc, _, result, granularity, coverage, _ in verified_rows:
        badge = "✅ pass" if result == "pass" else "❌ fail"
        L.append(f"| {sc} | {badge} | {granularity} | {coverage or '—'} |")

    L += ["", "## Component-level breakdown — 1.4.3 / 1.4.11 (the blast-radius join)", ""]
    for sc, _, result, granularity, coverage, per_component in verified_rows:
        if not per_component:
            continue
        fails = [c for c, v in per_component.items() if v == "fail"]
        not_covered = [c for c, v in per_component.items() if v == "not_covered"]
        passes = [c for c, v in per_component.items() if v == "pass"]
        L.append(f"### {sc}")
        L.append("")
        L.append(f"{coverage}. {len(passes)} pass, {len(fails)} fail, {len(not_covered)} not_covered.")
        L.append("")
        if fails:
            L.append(f"**Failing:** {', '.join(sorted(fails))}")
            L.append("")
        if not_covered:
            L.append(f"**Not covered** (applies_to claims this SC but the blast-radius scan found no bound audited "
                      f"token — either the component genuinely doesn't touch this colour category, or the scan's "
                      f"meta-text matching missed a prose-only reference): {', '.join(sorted(not_covered))}")
            L.append("")

    L += ["", "## Unverified (applies_to only)", ""]
    if unverified_rows:
        L += ["| SC | Note |", "|---|---|"]
        for sc, _, _, _, err, _ in unverified_rows:
            L.append(f"| {sc} | {err or 'no executable check in this build'} |")
    else:
        L.append("_None — every SC has a wired check._")
    L += [
        "",
        "## Granularity note",
        "",
        "`1.4.3` and `1.4.11` now verify at **component** granularity: the token-level contrast audits are joined "
        "through `tokens/_blast-radius.json` (component -> tokens it binds) down to a per-component pass/fail/not_covered "
        "verdict — see the breakdown above. `2.3.3` and `2.5.8` already verified at component granularity, since the "
        "a11y gate runs per reference snippet (one per component).",
        "",
    ]
    open(os.path.join(ROOT, "_VERIFICATION-EDGES.md"), "w").write("\n".join(L) + "\n")

    print(f"verification edges: {len(verified_rows)}/{len(rows)} SCs verified "
          f"({sum(1 for r in verified_rows if r[2]=='fail')} failing), {len(unverified_rows)} applies_to-only")
    for sc, status, result, granularity, coverage, per_component in rows:
        if status == "verified":
            extra = f" [{coverage}]" if coverage else ""
            print(f"  {'✅' if result=='pass' else '❌'} {sc}: {result} ({granularity}){extra}")
    sys.exit(0)  # advisory — never gates


if __name__ == "__main__":
    main()
