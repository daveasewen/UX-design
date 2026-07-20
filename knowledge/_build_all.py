#!/usr/bin/env python3
"""One-command rebuild of every derived view, in dependency order.

The generators must run in this order because later ones read earlier outputs:
  1. compliance/_build_compliance_kg.py      -> compliance/rules/, graph-index.json
                                                 (NOTE: this rewrites graph-index.json wholesale — any
                                                 verification{}/external_automatable_refs{} block from a
                                                 PRIOR run is gone after this step. Both must be rebuilt
                                                 fresh every run, in the order below.)
  2. tokens/_build_blast_radius.py           -> tokens/_blast-radius.json, _GRAPH-REPORT.md
  3. _build_xref_index.py                    -> _XREF-INDEX.json/.md   (needs 1 + 2)
  4. _build_review_queue.py                  -> _REVIEW-QUEUE.json/.md
  5. _build_dark_mode_audit.py               -> _DARK-MODE-AUDIT.json/.md (needs 2)
  6. _build_surface_contrast_audit.py        -> _TEXT-CONTRAST-AUDIT.json/.md (needs _contrast_utils)
  7. _build_indicator_contrast_audit.py      -> _INDICATOR-CONTRAST-AUDIT.json/.md (needs _contrast_utils)
  8. compliance/_build_verification_edges.py -> compliance/graph-index.json (verification block) + rules/*.json (verified_by)
                                                 (needs 1, 2 (blast-radius join), 6, 7 and the a11y gate — runs after all of them)
  9. compliance/_import_axe_rules.py         -> graph-index.json (external_automatable_refs) + rules/*.json
                                                 (needs 1 AND 8 — its "already wired" cross-check reads the
                                                 verification{} block, so it MUST run after step 8, not before.
                                                 Reads the vendored axe-core snapshot in compliance/_vendor/, no network.)
  10. _build_integrity.py                    -> _INTEGRITY-REPORT.md   (the gate; needs 3)

Run:  python3 knowledge/_build_all.py
Exits non-zero if EITHER gate fails: the integrity lint (step 8, any ERROR) or
the contrast audits (steps 6-7, any non-allowlisted token below its dark-mode
threshold). Both run to completion first so every report is fresh. This is the
single command to trust the knowledge base after editing metas or tokens.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("compliance knowledge graph", "compliance/_build_compliance_kg.py"),
    ("token blast-radius + graph report", "tokens/_build_blast_radius.py"),
    ("guideline rules index (gate)", "guidelines/gen_rules_index.py"),
    ("runbook index (generated)", "gen_runbook_index.py"),
    ("standing-instructions reachability gate", "_validate_standing_instructions.py"),
    # Sibling to the above, and deliberately adjacent: that gate asks "is every standing
    # doc REACHABLE"; this one asks "is what we say still TRUE". A doc can be perfectly
    # reachable and perfectly wrong — which is how "the sandbox has no Univers" survived
    # 16 months while the fonts sat in the repo (Dave, 2026-07-18: "how do we fix this
    # permanently?"). Registry: _assertions.json.
    ("assertion veracity gate — claims that can rot", "_validate_assertions.py"),
    ("cross-reference index", "_build_xref_index.py"),
    ("sutherland acceptance fixtures", "_build_sutherland_fixtures.py"),
    ("states-completeness probe (advisory)", "_build_states_probe.py"),
    ("_LIVE-STATE staleness gate (advisory, ADR-0007)", "_build_live_state.py"),
    ("advisory signals — prose rules (advisory)", "_validate_advisory.py"),
    ("review queue", "_build_review_queue.py"),
    ("dark-mode coverage audit", "_build_dark_mode_audit.py"),
    ("text/icon contrast audit", "_build_surface_contrast_audit.py"),
    ("indicator/accent contrast audit", "_build_indicator_contrast_audit.py"),
    ("icon contrast delta — brand 4.5 vs 3 (advisory)", "_build_icon_contrast_delta.py"),
    ("dark-surface flatness gate", "_validate_dark_surfaces.py"),
    ("snippet gate", "_validate_snippets.py"),
    ("Legacy-colour leakage gate (Mono) — no Legacy-only colour in a Mono surface", "_validate_legacy_leak.py"),
    ("token-tier gate (_STANDARDS.md §1)", "_validate_token_tiers.py"),
    ("icon-source gate", "_validate_icons.py"),
    ("a11y gate", "_validate_a11y.py"),
    ("coverage gate", "_validate_coverage.py"),
    ("pro-forma universal gate", "_validate_proforma.py"),
    ("pro-forma CSS-governed motion gate (DEF-003)", "_validate_css_governed.py"),
    ("pro-forma no-hardcode styling gate (DEF-004)", "_validate_no_hardcode.py"),
    ("4px-grid gate (DEF-005)", "_validate_grid.py"),
    ("type-binding blast-radius gate (canon/type.css)", "_validate_type_blast_radius.py"),
    ("descender-clip gate (ds-005) — truncating labels stay descender-safe", "_validate_descender_clip.py"),
    ("DataViz chart gate (semantic SVG + tokens + table spine)", "_validate_dataviz.py"),
    ("reverse-text edge-extremity check {#col26-020} (advisory)", "_validate_edge_extremity.py"),
    ("compliance verification edges — applies_to vs verified_by (advisory)", "compliance/_build_verification_edges.py"),
    ("external automatable-check refs — axe-core import (advisory)", "compliance/_import_axe_rules.py"),
    # The consult read-side tool (reviews/CONSOLIDATION-AUDIT-2026-07-18.html §3): a
    # problem-domain query index over rules/rulings/assertions/gates/ADRs/defects/open
    # items, plus a CLI that answers "what governs X?" in one step. Index regenerates every
    # build so it cannot rot; the selftest is advisory until the tool has earned trust.
    ("consult index — problem-domain query surface", "_build_consult_index.py"),
    ("consult tool selftest (advisory)", "_consult.py", ["--selftest"]),
    ("integrity lint (gate)", "_build_integrity.py"),
]

rc = 0
for i, step in enumerate(STEPS, 1):
    label, rel = step[0], step[1]
    extra_args = list(step[2]) if len(step) > 2 else []
    path = os.path.join(HERE, rel)
    print(f"\n=== [{i}/{len(STEPS)}] {label} — {rel} ===")
    r = subprocess.run([sys.executable, path] + extra_args)
    if r.returncode != 0:
        # Gating steps: integrity lint AND the contrast audits. They run to the
        # end (so you get every report) then the build exits non-zero.
        if rel.endswith("_build_integrity.py"):
            print(f"\n❌ integrity gate failed (exit {r.returncode}) — see knowledge/_INTEGRITY-REPORT.md")
            rc = rc or r.returncode
        elif "contrast" in label:
            print(f"\n❌ contrast gate failed (exit {r.returncode}) — see knowledge/_*-CONTRAST-AUDIT.md")
            rc = rc or r.returncode
        elif "snippet" in label:
            print(f"\n❌ snippet gate failed (exit {r.returncode}) — see knowledge/_SNIPPET-AUDIT.md")
            rc = rc or r.returncode
        elif "leakage" in label:
            print(f"\n❌ Legacy-colour leakage gate failed (exit {r.returncode}) — a Mono surface resolves to a Legacy-only colour (e.g. the success teal #00847F). Rebind onto the R-D14 token (rag/*-background / -glyph); do NOT add the hex to exceptions. See knowledge/_LEGACY-LEAK-GATE.md")
            rc = rc or r.returncode
        elif "token-tier" in label:
            print(f"\n❌ token-tier gate failed (exit {r.returncode}) — a component references a primitive, or a $value drifted from its $alias; see knowledge/_TOKEN-TIER-AUDIT.md")
            rc = rc or r.returncode
        elif "icon" in label:
            print(f"\n❌ icon-source gate failed (exit {r.returncode}) — see knowledge/_ICON-SOURCE-AUDIT.md")
            rc = rc or r.returncode
        elif "a11y" in label:
            print(f"\n❌ a11y gate failed (exit {r.returncode}) — see knowledge/_A11Y-GATE.md")
            rc = rc or r.returncode
        elif "coverage" in label:
            print(f"\n❌ coverage gate failed (exit {r.returncode}) — see knowledge/_COVERAGE-GATE.md")
            rc = rc or r.returncode
        elif "no-hardcode" in label:
            print("pro-forma no-hardcode styling gate failed (exit %d) — see knowledge/_NO-HARDCODE-GATE.md" % r.returncode)
            rc = rc or r.returncode
        elif "CSS-governed" in label:
            print(f"\n❌ pro-forma CSS-governed motion gate failed (exit {r.returncode}) — see knowledge/_CSS-GOVERNED-GATE.md")
            rc = rc or r.returncode
        elif "4px-grid" in label:
            print(f"\n❌ 4px-grid gate (DEF-005) failed (exit {r.returncode}) — off-grid layout value(s); see _validate_grid.py output")
            rc = rc or r.returncode
        elif "blast-radius" in label:
            print(f"\n❌ type-binding blast-radius gate failed (exit {r.returncode}) — a global type-composite selector is unregistered or its blast radius escaped; see knowledge/_TYPE-BLAST-GATE.md")
            rc = rc or r.returncode
        elif "descender-clip" in label:
            print(f"\n❌ descender-clip gate (ds-005) failed (exit {r.returncode}) — a truncating label (text-overflow:ellipsis) lacks `text-box-edge:text text`, so cap-alphabetic trim will clip its descenders (g/y/p/q). This is NOT a stray override to remove — the override IS the fix; add it. See _validate_descender_clip.py + _DS-IMPROVEMENTS.md ds-005.")
            rc = rc or r.returncode
        elif "pro-forma" in label:
            print(f"\n❌ pro-forma universal gate failed (exit {r.returncode}) — see knowledge/_PROFORMA-GATE.md")
            rc = rc or r.returncode
        elif "DataViz" in label:
            print(f"\n❌ DataViz chart gate failed (exit {r.returncode}) — see knowledge/_DATAVIZ-GATE.md")
            rc = rc or r.returncode
        elif "surface" in label:
            print(f"\n❌ dark-surface gate failed (exit {r.returncode}) — see knowledge/_DARK-SURFACE-AUDIT.md")
            rc = rc or r.returncode
        elif "standing-instructions" in label:
            print(f"\n❌ standing-instructions gate failed (exit {r.returncode}) — a standing doc is unreachable from GOOD-MORNING/_RUNBOOKS, or GOOD-MORNING has lost part of its structure. A rule nothing points to will not survive the next cold session.")
            rc = rc or r.returncode
        elif "rules index" in label:
            print(f"\n❌ rules-index gate failed (exit {r.returncode}) — duplicate/missing/malformed rule IDs in guidelines/")
            rc = rc or r.returncode
        elif "advisory" in label.lower():
            # advisory steps never gate/abort — they report and the build continues
            print(f"\n⚠ advisory step '{label}' reported findings (exit {r.returncode}) — non-gating")
        else:
            print(f"\n❌ step '{label}' failed (exit {r.returncode}) — aborting")
            sys.exit(r.returncode)

if rc == 0:
    print("\n✅ all generators ran and the integrity + contrast gates passed.")
else:
    print("\n❌ build gate failed — see the reports above.")
sys.exit(rc)
