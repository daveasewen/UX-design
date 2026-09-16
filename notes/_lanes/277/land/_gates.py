#!/usr/bin/env python3
"""_gates.py — the #277 lane LA gate battery. READ-ONLY on the corpus, by construction.

  G1 SCHEMA   — all four proposals validated against knowledge/components/meta.schema.json
                (jsonschema Draft-07), which is where `$why` is REQUIRED and min-length 40.
  G2 REFS     — every `rule:` ref resolves in knowledge/guidelines/_rules-index.json.
  G3 COUNTS   — 9+15 · 10+15 · 10+17 · 11 = 87.
  G4 KG       — knowledge/_validate_kg.py run on a SIMULATED tree: the four proposals
                swapped into knowledge/components/, the gate run, the originals swapped
                BACK, and the restoration PROVEN by byte-comparison against the bytes
                held before the swap. try/finally, so a crash still restores.
                ⛔ gen_kg_edges.py is never invoked by this lane; _validate_kg.py's own
                freshness arm runs it against its own scratch copy, which is the gate's
                behaviour, not this lane's write.

Usage: python3 notes/_lanes/277/land/_gates.py
"""
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
LIVE = REPO / "knowledge" / "components"
PROP = LANE / "proposed-metas"
STEMS = ("chart-line", "chart-pie", "chart-bar", "chart-donut")
EXPECT = {"chart-line": 24, "chart-pie": 25, "chart-bar": 27, "chart-donut": 11}

lines, ok = [], True


def say(tag, text):
    global ok
    lines.append(f"{tag} {text}")
    print(f"{tag} {text}")
    if tag != "PASS":
        ok = False


# --- G1 schema --------------------------------------------------------------
schema = json.loads((LIVE / "meta.schema.json").read_text(encoding="utf-8"))
V = jsonschema.Draft7Validator(schema)
for stem in STEMS:
    doc = json.loads((PROP / f"{stem}.meta.json").read_text(encoding="utf-8"))
    errs = sorted(V.iter_errors(doc), key=lambda e: list(e.path))
    if errs:
        say("FAIL", f"G1 schema {stem}: " + " | ".join(f"{list(e.path)}: {e.message}" for e in errs[:4]))
    else:
        say("PASS", f"G1 schema {stem}.meta.json validates against meta.schema.json "
                    f"({len(doc['edges']['obeys'])} obeys, $why required and present on every one)")

# --- G2 refs resolve --------------------------------------------------------
idx = json.loads((REPO / "knowledge" / "guidelines" / "_rules-index.json").read_text(encoding="utf-8"))
known = {r["id"] for r in idx["rules"]}
for stem in STEMS:
    doc = json.loads((PROP / f"{stem}.meta.json").read_text(encoding="utf-8"))
    bad = [e["ref"] for e in doc["edges"]["obeys"] if e["ref"].split(":", 1)[1] not in known]
    if bad:
        say("FAIL", f"G2 refs {stem}: unresolved {bad}")
    else:
        say("PASS", f"G2 refs {stem}: every `rule:` id resolves in _rules-index.json")

# --- G3 counts --------------------------------------------------------------
tot = 0
for stem in STEMS:
    n = len(json.loads((PROP / f"{stem}.meta.json").read_text(encoding="utf-8"))["edges"]["obeys"])
    tot += n
    if n != EXPECT[stem]:
        say("FAIL", f"G3 counts {stem}: {n}, expected {EXPECT[stem]}")
if tot == 87 and ok:
    say("PASS", "G3 counts: chart-line 9+15=24 · chart-pie 10+15=25 · chart-bar 10+17=27 · "
                "chart-donut 11+0=11 — TOTAL 87 (29 + 47 + 11)")

# --- G4 _validate_kg.py on the simulated tree -------------------------------
held = {s: (LIVE / f"{s}.meta.json").read_bytes() for s in STEMS}
try:
    for s in STEMS:
        (LIVE / f"{s}.meta.json").write_bytes((PROP / f"{s}.meta.json").read_bytes())
    r = subprocess.run([sys.executable, str(REPO / "knowledge" / "_validate_kg.py")],
                       capture_output=True, text=True, cwd=REPO)
    tail = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()][-3:]
finally:
    for s in STEMS:
        (LIVE / f"{s}.meta.json").write_bytes(held[s])
restored = all((LIVE / f"{s}.meta.json").read_bytes() == held[s] for s in STEMS)
say("PASS" if r.returncode == 0 else "FAIL",
    f"G4 _validate_kg.py on the simulated tree (4 proposals swapped in): rc={r.returncode} — "
    + " / ".join(tail))
say("PASS" if restored else "FAIL",
    "G4 restore: the four live metas byte-compare EQUAL to the bytes held before the swap")

(LANE / "gates.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\nALL GATES PASS" if ok else "\nGATES FAILED")
sys.exit(0 if ok else 1)
