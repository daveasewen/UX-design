#!/usr/bin/env python3
"""Reproduce DRIVE 3 exactly: flip ONE byte inside a spliced region of the real regenerated
page, then run the gate on the mutant. Deterministic — the anchor is a literal, not an offset,
so it survives a re-mint of the page.

  python3 notes/_subreports/assets/2026-09-02-235-L1-receipt-gate/mutate.py   # from repo root
"""
import os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _validate_receipt as VR
PAGE = os.path.join(ROOT, "dashboards", "international-banking-dashboard.regen-v2-receipt.html")
h = open(PAGE, encoding="utf-8").read()
txt, (a, b) = VR.region_bytes(h, "Stat-card#markup")
i = txt.find("2,450.00")
assert i > 0, "anchor '2,450.00' not found inside Stat-card#markup"
off = a + i                                   # ONE byte: '2' -> '3'
out = os.path.join(tempfile.mkdtemp(), "mutated.html")
open(out, "w", encoding="utf-8").write(h[:off] + "3" + h[off + 1:])
print("mutated ONE byte at page offset %d (was %r, now '3')" % (off, h[off]))
sys.exit(subprocess.call([sys.executable,
                          os.path.join(ROOT, "knowledge", "_validate_receipt.py"), out]))
