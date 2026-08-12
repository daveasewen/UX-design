#!/usr/bin/env python3
"""_import_axe_rules.py — import the SC leg from an external, machine-readable
automatable-check registry (axe-core), per the 2026-07-10 design direction:
"Import, don't hand-type, the SC<->rule leg."

Reads the vendored snapshot at _vendor/axe-core-rules-snapshot.json (see
_vendor/_INGEST-NOTES.md for provenance + how to refresh it — no live network
call at build time, matching the rest of knowledge/ building fully offline).

This is DIFFERENT from _build_verification_edges.py's verified_by:
  - verified_by   = an executable check WE run, wired into OUR build, with a
                    current pass/fail result. "Is this actually enforced here."
  - external_automatable_refs = off-the-shelf tooling that EXISTS for this SC,
                    whether or not we've adopted it yet. "Could this be
                    verified cheaply, if we wired an axe-core rule up."
Advisory only — does not gate the build, does not itself verify anything.

W3C ACT Rules Format was checked (2026-07-14) and NOT ingested this pass — no
structured export was found without scraping ~500 individual rule pages. See
_vendor/_INGEST-NOTES.md for what was checked and the deferred approach.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))          # knowledge/compliance
RULES = os.path.join(HERE, "rules")
GRAPH_INDEX = os.path.join(HERE, "graph-index.json")
SNAPSHOT = os.path.join(HERE, "_vendor", "axe-core-rules-snapshot.json")

TAGRE = re.compile(r"^wcag(\d+)$")


def tag_to_sc(tag):
    m = TAGRE.match(tag)
    if not m:
        return None
    digits = m.group(1)
    if len(digits) < 3:
        return None  # principle+guideline alone isn't a full SC (e.g. plain level tags slip through if ever untagged)
    return f"{digits[0]}.{digits[1]}.{digits[2:]}"


def main():
    if not os.path.exists(GRAPH_INDEX):
        print("ERROR: compliance/graph-index.json not found — run _build_compliance_kg.py first.")
        sys.exit(0)  # advisory: never aborts the build
    if not os.path.exists(SNAPSHOT):
        print(f"WARN: {SNAPSHOT} missing — skipping external-automatable-refs import (advisory, non-gating).")
        sys.exit(0)

    index = json.load(open(GRAPH_INDEX))
    snap = json.load(open(SNAPSHOT))

    # sc -> [{source, rule_id, description, url}]
    by_sc = {}
    for rule_id, meta in snap.get("rules", {}).items():
        scs = set()
        for t in meta.get("tags", []):
            sc = tag_to_sc(t)
            if sc:
                scs.add(sc)
        for sc in scs:
            by_sc.setdefault(sc, []).append({
                "source": snap.get("source", "axe-core"),
                "source_version": snap.get("source_version"),
                "rule_id": rule_id,
                "description": meta.get("description"),
                "url": meta.get("helpUrl"),
            })

    our_scs = sorted(index.get("by_sc", {}))
    verification = (index.get("verification") or {}).get("by_sc", {})

    refs_for_our_graph = {sc: by_sc.get(sc, []) for sc in our_scs}
    index["external_automatable_refs"] = {
        "$description": "SC -> off-the-shelf automatable checks that EXIST for it (currently: axe-core OSS rules), independent of whether WE have wired one up. Contrast with 'verification' (verified_by) which is only about checks actually running in THIS build. See knowledge/compliance/_import_axe_rules.py.",
        "source": "axe-core",
        "source_version": snap.get("source_version"),
        "snapshotted": snap.get("snapshotted"),
        "generated": datetime.date.today().isoformat(),
        "by_sc": refs_for_our_graph,
    }
    json.dump(index, open(GRAPH_INDEX, "w"), indent=2, ensure_ascii=False)

    # patch individual rule files
    for sc in our_scs:
        refs = refs_for_our_graph.get(sc) or []
        rule_id = None
        for rid in index.get("rules", []):
            if rid.startswith(f"wcag-{sc}-"):
                rule_id = rid
                break
        if not rule_id:
            continue
        rule_path = os.path.join(RULES, rule_id + ".json")
        if not os.path.exists(rule_path):
            continue
        rule = json.load(open(rule_path))
        rule["external_automatable_refs"] = refs
        json.dump(rule, open(rule_path, "w"), indent=2, ensure_ascii=False)

    # --- report ---
    covered = [sc for sc in our_scs if refs_for_our_graph.get(sc)]
    uncovered = [sc for sc in our_scs if not refs_for_our_graph.get(sc)]
    easy_wins = [sc for sc in covered if not verification.get(sc)]  # covered by axe, not yet wired into our build
    already_wired = [sc for sc in covered if verification.get(sc)]

    L = [
        "# External automatable-check refs (axe-core import)",
        "",
        f"> Off-the-shelf automatable checks that EXIST for each SC in our compliance graph, imported from axe-core "
        f"v{snap.get('source_version')} ({snap.get('snapshotted')}) — see `compliance/_vendor/_INGEST-NOTES.md` for provenance. "
        "Advisory, does not gate the build. This is NOT the same as `verified_by`: it says tooling is *available*, "
        "not that *we* run it.",
        "",
        f"**{len(covered)}/{len(our_scs)} of our SCs have at least one axe-core rule tagged against them.** "
        f"{len(uncovered)} have no OSS axe-core coverage at all — genuinely manual/bespoke territory for now.",
        "",
        f"## Easy wins — axe-core covers it, we haven't wired it up ({len(easy_wins)})",
        "",
    ]
    if easy_wins:
        L += ["| SC | axe-core rule(s) |", "|---|---|"]
        for sc in easy_wins:
            rules_str = ", ".join(f"`{r['rule_id']}`" for r in refs_for_our_graph[sc])
            L.append(f"| {sc} | {rules_str} |")
    else:
        L.append("_None._")
    L += ["", f"## Already wired (verified_by set independently of this import) ({len(already_wired)})", ""]
    if already_wired:
        L += ["| SC | axe-core rule(s) |", "|---|---|"]
        for sc in already_wired:
            rules_str = ", ".join(f"`{r['rule_id']}`" for r in refs_for_our_graph[sc])
            L.append(f"| {sc} | {rules_str} |")
    else:
        L.append("_None._")
    L += ["", f"## No OSS axe-core coverage found ({len(uncovered)})", "", "| SC |", "|---|"]
    for sc in uncovered:
        L.append(f"| {sc} |")
    L += [
        "",
        "## W3C ACT Rules Format",
        "",
        "Checked 2026-07-14, **not ingested this pass** — no structured export found without scraping ~500 "
        "individual rule pages. See `compliance/_vendor/_INGEST-NOTES.md` for what was checked and the deferred approach.",
        "",
    ]
    open(os.path.join(os.path.dirname(HERE), "_EXTERNAL-AUTOMATABLE-REFS.md"), "w").write("\n".join(L) + "\n")

    print(f"external-automatable-refs: {len(covered)}/{len(our_scs)} SCs have axe-core coverage "
          f"({len(easy_wins)} easy-win, {len(already_wired)} already wired, {len(uncovered)} uncovered)")
    sys.exit(0)  # advisory — never gates


if __name__ == "__main__":
    main()
