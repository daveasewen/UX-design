#!/usr/bin/env python3
"""_audit_props_axes.py - LANE 1 of the s136-D1 enactment: MEASURE ONLY.

Inventories every component meta's declared props against the three-axis model
ruled by Dave at s136-D1:

  (A) PARAMETERS - values live in props; every visual prop declares a spine
      token binding ("binds"); free hex/px forbidden.
  (B) VARIANTS   - switches live as mutation-keys on their owning node; a
      variant travels with its node through any slot.
  (C) SLOTS      - content injects through contract-typed slots; "slots" is the
      only new meta.json key.
  (D) FORK BAN   - anything off-axis is a fork.

THIS SCRIPT DOES NOT MIGRATE ANYTHING. It writes one JSON audit file.

DECISION PROCEDURE (declared, so a reader can disagree with the rule rather
than with a number). Each prop gets exactly one verdict:

  PARAM_BOUND        prop carries a "binds" key -> clause A satisfied, PROVEN.
  PARAM_UNBOUND      prop is a visual VALUE by type (number/scale/fixed/layout/
                     pair/date) but declares no "binds" -> clause A names it a
                     param and requires a binding it does not have. Measured
                     defect, not a classification guess.
  VARIANT_DECLARED   enum prop whose values are a subset of, or equal to, the
                     names in this meta's own "variants" array -> the switch is
                     PROVEN to be a variant of this node.
  VARIANT_SHAPED     enum or boolean prop with no such corroboration. It has
                     the SHAPE of a mutation-key (a closed switch) but nothing
                     in the artefact proves it is one. Reported separately from
                     VARIANT_DECLARED on purpose.
  SLOT_SHAPED        prop that injects content: type in {array, table} or name
                     in the explicit content-injection list below. No meta
                     declares a "slots" key, so NO slot can be PROVEN; this is
                     shape only.
  UNCLASSIFIABLE     everything the ruling AS WRITTEN does not reach. Sub-cause
                     is recorded in "why" - the honest categories are:
                       text-content   free text (string) that is neither a
                                      value binding nor a contract-typed slot.
                                      The text-param refinement is FLOATED, not
                                      ruled, so it stays unclassified.
                       behaviour      function/mechanism props (handlers). The
                                      three axes have no behaviour axis.
                       untyped        type absent or unrecognised.

UNKNOWN IS NEVER DEFAULTED. A prop is only called a param, variant or slot when
the artefact carries the evidence named above.

Corpus / glob: knowledge/components/*.meta.json - the LIVE component corpus.
designer-skills-v1/ and designer-skills-v2/ are RELEASE PACKS (frozen
snapshots) and are deliberately NOT audited here; second-system-govuk/ is a
different design system.

Usage:  python3 knowledge/_audit_props_axes.py [--out PATH]
Exit 0 on success. Fails LOUD and NAMED on any unreadable meta.
"""
import argparse
import glob
import json
import os
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOB = "knowledge/components/*.meta.json"
DEFAULT_OUT = "reviews/PROPS-AXES-AUDIT-2026-08-09-s139-v1.json"

VALUE_TYPES = {"number", "scale", "fixed", "layout", "pair", "date"}
SWITCH_TYPES = {"enum", "boolean"}
CONTAINER_TYPES = {"array", "table"}
BEHAVIOUR_TYPES = {"function", "mechanism"}
CONTENT_NAMES = {
    "content", "children", "slot", "slots", "actions", "items", "body",
    "footer", "header", "rows", "columns", "data", "series", "slices",
}


def fail(msg):
    print("FAIL _audit_props_axes.py: " + msg, file=sys.stderr)
    sys.exit(2)


def classify(prop, variant_names):
    name = prop.get("name")
    ptype = prop.get("type")
    if name is None or ptype is None:
        return "UNCLASSIFIABLE", "untyped", "prop lacks name or type"
    if "binds" in prop:
        return "PARAM_BOUND", "binds-present", "declares binds=%r" % (prop["binds"],)
    if ptype in BEHAVIOUR_TYPES:
        return ("UNCLASSIFIABLE", "behaviour",
                "type=%s - the three axes have no behaviour axis" % ptype)
    if ptype in CONTAINER_TYPES or name in CONTENT_NAMES:
        return ("SLOT_SHAPED", "content-injection",
                "type=%s name=%s injects content; no slots key exists to type "
                "the contract" % (ptype, name))
    if ptype in VALUE_TYPES:
        return ("PARAM_UNBOUND", "value-type-no-binds",
                "type=%s is a visual value; clause A requires binds, absent" % ptype)
    if ptype == "enum":
        vals = prop.get("values") or []
        if vals and variant_names and set(vals) <= variant_names:
            return ("VARIANT_DECLARED", "values-match-variants",
                    "values %s are declared variants of this node" % (sorted(vals),))
        return ("VARIANT_SHAPED", "closed-switch",
                "enum with no corroborating variants[] entry")
    if ptype == "boolean":
        return ("VARIANT_SHAPED", "boolean-switch",
                "boolean two-state switch, no variants[] entry")
    if ptype == "string":
        return ("UNCLASSIFIABLE", "text-content",
                "free text - text-param refinement is FLOATED, not ruled")
    return ("UNCLASSIFIABLE", "untyped", "unrecognised type=%s" % ptype)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(REPO, GLOB)))
    if not files:
        fail("glob %s matched ZERO files - refusing to write an empty audit" % GLOB)

    components = []
    totals = Counter()
    why_totals = Counter()
    metas_with_binds = 0
    metas_with_slots = 0

    for path in files:
        rel = os.path.relpath(path, REPO)
        try:
            with open(path) as fh:
                meta = json.load(fh)
        except Exception as exc:
            fail("cannot parse %s: %s" % (rel, exc))
        if not isinstance(meta, dict):
            fail("%s is not a JSON object" % rel)

        variant_names = set()
        for v in meta.get("variants") or []:
            if isinstance(v, dict) and v.get("name"):
                variant_names.add(v["name"])

        props = meta.get("props") or []
        if not isinstance(props, list):
            fail("%s props is not an array" % rel)

        rows = []
        counts = Counter()
        for prop in props:
            if not isinstance(prop, dict):
                fail("%s has a non-object prop" % rel)
            verdict, why, note = classify(prop, variant_names)
            counts[verdict] += 1
            totals[verdict] += 1
            why_totals[why] += 1
            rows.append({
                "prop": prop.get("name"),
                "type": prop.get("type"),
                "verdict": verdict,
                "why": why,
                "note": note,
            })
        if any("binds" in p for p in props if isinstance(p, dict)):
            metas_with_binds += 1
        if "slots" in meta:
            metas_with_slots += 1

        components.append({
            "file": rel,
            "name": meta.get("name"),
            "category": meta.get("category"),
            "props_declared": len(props),
            "variants_declared": len(meta.get("variants") or []),
            "has_slots_key": "slots" in meta,
            "counts": dict(sorted(counts.items())),
            "props": rows,
        })

    out = {
        "$id": "PROPS-AXES-AUDIT-2026-08-09-s139-v1",
        "$generated_by": "knowledge/_audit_props_axes.py",
        "$ruling": "s136-D1 (three-axis model: params / variants / slots)",
        "$lane": "LANE 1 - MEASURE ONLY. No migration, no fixes, no key rollout.",
        "$glob": GLOB,
        "$glob_rationale": (
            "the LIVE component corpus. designer-skills-v1/ and -v2/ are "
            "release packs (frozen snapshots, never auto-synced); "
            "second-system-govuk/ is a different design system. The rule "
            "reported here is only as wide as this glob."
        ),
        "$verdict_vocabulary": {
            "PARAM_BOUND": "prop declares binds - clause A PROVEN",
            "PARAM_UNBOUND": "visual value type, binds absent - clause A defect",
            "VARIANT_DECLARED": "enum values are declared variants of this node",
            "VARIANT_SHAPED": "switch-shaped, no corroboration in the artefact",
            "SLOT_SHAPED": "content-injecting, no slots key exists to type it",
            "UNCLASSIFIABLE": "the ruling as written does not reach this prop",
        },
        "summary": {
            "metas_audited": len(components),
            "props_audited": sum(totals.values()),
            "metas_with_any_binds": metas_with_binds,
            "metas_with_slots_key": metas_with_slots,
            "by_verdict": dict(sorted(totals.items())),
            "unclassifiable_by_cause": dict(sorted(
                (k, v) for k, v in why_totals.items()
                if k in ("text-content", "behaviour", "untyped"))),
        },
        "components": components,
    }

    outpath = os.path.join(REPO, args.out)
    with open(outpath, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % args.out)
    print("metas=%d props=%d" % (len(components), sum(totals.values())))
    for k, v in sorted(totals.items()):
        print("  %-18s %d" % (k, v))
    print("metas with any props.binds: %d/%d" % (metas_with_binds, len(components)))
    print("metas with slots key:       %d/%d" % (metas_with_slots, len(components)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
