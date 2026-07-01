#!/usr/bin/env python3
"""One-command rebuild of every derived view, in dependency order.

The generators must run in this order because later ones read earlier outputs:
  1. compliance/_build_compliance_kg.py      -> compliance/rules/, graph-index.json
  2. tokens/_build_blast_radius.py           -> tokens/_blast-radius.json, _GRAPH-REPORT.md
  3. _build_xref_index.py                    -> _XREF-INDEX.json/.md   (needs 1 + 2)
  4. _build_review_queue.py                  -> _REVIEW-QUEUE.json/.md
  5. _build_dark_mode_audit.py               -> _DARK-MODE-AUDIT.json/.md (needs 2)
  6. _build_surface_contrast_audit.py        -> _TEXT-CONTRAST-AUDIT.json/.md (needs _contrast_utils)
  7. _build_indicator_contrast_audit.py      -> _INDICATOR-CONTRAST-AUDIT.json/.md (needs _contrast_utils)
  8. _build_integrity.py                     -> _INTEGRITY-REPORT.md   (the gate; needs 3)

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
    ("cross-reference index", "_build_xref_index.py"),
    ("sutherland acceptance fixtures", "_build_sutherland_fixtures.py"),
    ("states-completeness probe (advisory)", "_build_states_probe.py"),
    ("review queue", "_build_review_queue.py"),
    ("dark-mode coverage audit", "_build_dark_mode_audit.py"),
    ("text/icon contrast audit", "_build_surface_contrast_audit.py"),
    ("indicator/accent contrast audit", "_build_indicator_contrast_audit.py"),
    ("dark-surface flatness gate", "_validate_dark_surfaces.py"),
    ("snippet gate", "_validate_snippets.py"),
    ("icon-source gate", "_validate_icons.py"),
    ("a11y gate", "_validate_a11y.py"),
    ("coverage gate", "_validate_coverage.py"),
    ("integrity lint (gate)", "_build_integrity.py"),
]

rc = 0
for i, (label, rel) in enumerate(STEPS, 1):
    path = os.path.join(HERE, rel)
    print(f"\n=== [{i}/{len(STEPS)}] {label} — {rel} ===")
    r = subprocess.run([sys.executable, path])
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
        elif "icon" in label:
            print(f"\n❌ icon-source gate failed (exit {r.returncode}) — see knowledge/_ICON-SOURCE-AUDIT.md")
            rc = rc or r.returncode
        elif "a11y" in label:
            print(f"\n❌ a11y gate failed (exit {r.returncode}) — see knowledge/_A11Y-GATE.md")
            rc = rc or r.returncode
        elif "coverage" in label:
            print(f"\n❌ coverage gate failed (exit {r.returncode}) — see knowledge/_COVERAGE-GATE.md")
            rc = rc or r.returncode
        elif "surface" in label:
            print(f"\n❌ dark-surface gate failed (exit {r.returncode}) — see knowledge/_DARK-SURFACE-AUDIT.md")
            rc = rc or r.returncode
        else:
            print(f"\n❌ step '{label}' failed (exit {r.returncode}) — aborting")
            sys.exit(r.returncode)

if rc == 0:
    print("\n✅ all generators ran and the integrity + contrast gates passed.")
else:
    print("\n❌ build gate failed — see the reports above.")
sys.exit(rc)
