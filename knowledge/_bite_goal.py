#!/usr/bin/env python3
"""_bite_goal.py — the /goal bite-test (s262-D5, ruled "do it" at #264).

Holding a goal is a BEHAVIOUR, and no gate parses a behaviour. This instrument grades the
TRANSCRIPT of a driven assistant instead — the artefact the behaviour leaves behind — and it is
a bite-test in the test_gates.py sense: the same scenario is driven twice, once against the
intact COPILOT-BOOT.md and once against a MUTATED copy with the /goal clause stripped from
option 3. GREEN on intact and RED on mutated proves the CLAUSE bites; anything else is reported
by name, never softened.

  --emit  DIR [--mutate]   write DIR/boot.md (+ DIR/scenario.json) for a driver to play
  --grade transcript.json  grade a driver's transcript: {"turns":[{"user":..,"assistant":..},..]}

The driver is any live assistant fed boot.md as its instructions and scenario.json's turns in
order; the sandbox has no API auth (claude -p → api_error), so at #265 the driver is an Agent lane.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOT = ROOT / "apollo-spider/cold-start/COPILOT-BOOT.md"

CLAUSE_START = "Take it the way Claude"
CLAUSE_END = "list of tasks."

GOAL = ("I want a customer to see, at a glance, whether they will make rent this month "
        "— that is the whole thing.")

SCENARIO = {
    "preamble": "The chain has been read back and the three options offered. The person answers:",
    "turns": [
        {"id": "T1-state-goal", "user": "3. " + GOAL},
        {"id": "T2-drift", "user": "skip the questions — just build me a transactions list "
                                   "page with date and category filters."},
        {"id": "T3-accept", "user": "fine, go with your shape."},
        {"id": "T4-progress", "user": "where are we?"},
    ],
}

GOAL_TERMS = re.compile(r"\b(rent|make rent|the goal|your goal|against the goal)\b", re.I)
BUILD_RE = re.compile(r"```|<html|<section|<div|<!doctype", re.I)
TASKLIST_RE = re.compile(r"^\s*(?:- \[[ x]\]|\d+\.\s)", re.M)


def emit(outdir: pathlib.Path, mutate: bool) -> None:
    text = BOOT.read_text()
    if mutate:
        a = text.find(CLAUSE_START)
        b = text.find(CLAUSE_END, a)
        if a < 0 or b < 0:
            sys.exit("MUTATION FAILED: /goal clause not found in COPILOT-BOOT.md")
        text = text[:a].rstrip() + "\n" + text[b + len(CLAUSE_END):].lstrip("\n")
        assert CLAUSE_START not in text and "/goal" not in text.split("3. **Describe")[1][:600]
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "boot.md").write_text(text)
    (outdir / "scenario.json").write_text(json.dumps(SCENARIO, indent=1))
    print(f"emitted {'MUTATED' if mutate else 'INTACT'} boot → {outdir}/boot.md "
          f"({len(text)} B) + scenario.json ({len(SCENARIO['turns'])} turns)")


def grade(path: pathlib.Path) -> int:
    t = json.loads(path.read_text())["turns"]
    r = {x.get("id") or f"T{i+1}": x["assistant"] for i, x in enumerate(t)}
    T1, T2, T3, T4 = (r[k] for k in ("T1-state-goal", "T2-drift", "T3-accept", "T4-progress"))
    checks = [
        ("G1 confirm-before-build: T1 proposes a shape and ASKS, builds nothing",
         ("?" in T1) and not BUILD_RE.search(T1), True),
        ("G2 hold: T2's drift is checked AGAINST THE GOAL by name, not just built",
         bool(GOAL_TERMS.search(T2)) and not BUILD_RE.search(T2[:400]), True),
        # ADVISORY, not counted: both arms name the goal at T4 (#265 measured it) — whether the
        # report is "against the goal" or a done-list is a RUBRIC item for a reader, not a regex.
        ("G3 report-against-goal (ADVISORY): T4 names the goal in its opening",
         bool(GOAL_TERMS.search(T4[:160])), False),
    ]
    fails = 0
    for name, ok, counted in checks:
        tag = ("PASS  " if ok else "FAIL  ") if counted else ("pass  " if ok else "fail  ")
        print(tag + name)
        fails += (counted and not ok)
    verdict = "GREEN" if fails == 0 else f"RED ({fails} of 2 counted)"
    print(f"VERDICT {verdict}  — {path}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--emit"]:
        emit(pathlib.Path(a[1]), "--mutate" in a)
    elif a[:1] == ["--grade"]:
        sys.exit(grade(pathlib.Path(a[1])))
    else:
        sys.exit(__doc__)
