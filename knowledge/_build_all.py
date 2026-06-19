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
Exits non-zero if the integrity gate (step 8) finds any ERROR — so this is the
single command to trust the knowledge base after editing metas or tokens.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("compliance knowledge graph", "compliance/_build_compliance_kg.py"),
    ("token blast-radius + graph report", "tokens/_build_blast_radius.py"),
    ("cross-reference index", "_build_xref_index.py"),
    ("review queue", "_build_review_queue.py"),
    ("dark-mode coverage audit", "_build_dark_mode_audit.py"),
    ("text/icon contrast audit", "_build_surface_contrast_audit.py"),
    ("indicator/accent contrast audit", "_build_indicator_contrast_audit.py"),
    ("integrity lint (gate)", "_build_integrity.py"),
]

rc = 0
for i, (label, rel) in enumerate(STEPS, 1):
    path = os.path.join(HERE, rel)
    print(f"\n=== [{i}/{len(STEPS)}] {label} — {rel} ===")
    r = subprocess.run([sys.executable, path])
    if r.returncode != 0:
        # integrity is the only step allowed to gate the build (contrast audits are warnings)
        if rel.endswith("_build_integrity.py"):
            print(f"\n❌ integrity gate failed (exit {r.returncode}) — see knowledge/_INTEGRITY-REPORT.md")
            rc = r.returncode
        elif "contrast" in label:
            print(f"\n⚠️  step '{label}' completed with warnings — see knowledge/_*-CONTRAST-AUDIT.md")
        else:
            print(f"\n❌ step '{label}' failed (exit {r.returncode}) — aborting")
            sys.exit(r.returncode)

if rc == 0:
    print("\n✅ all generators ran and the integrity gate passed.")
sys.exit(rc)
