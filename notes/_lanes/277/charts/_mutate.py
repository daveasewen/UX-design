#!/usr/bin/env python3
"""_mutate.py — the mutation harness for lane CO's author (#277).

A bite that cannot fail is not a test, and a mutation test proves the CLAUSE,
not the feature. Each mutant is a one-line edit to _author_metas.py's source;
the harness runs its `--selftest` in an ISOLATED tree and records which bites
turned RED. Nothing in the repo is written: the mutant lives under
<scratch>/mutroot/notes/_lanes/277/charts/ with knowledge/ symlinked in
read-only, and the tree is removed at the end.

A MUTANT THAT SURVIVES IS A FINDING, NOT A PASS (the brief says so).

    python3 notes/_lanes/277/charts/_mutate.py [scratch-dir]
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
SRC = (LANE / "_author_metas.py").read_text(encoding="utf-8")

# (id, description of the defect the mutant injects, anchor, replacement)
MUTANTS = [
    ("M1", "a REGEX-TIER false positive is admitted — the exact s274-D12 / s276-D5 'Avatar' case",
     '        ("rule:dv-bar-001",',
     '        ("rule:va25-013", "a name-match false positive of the kind s276-D5 refuses by name, forty plus"),\n        ("rule:dv-bar-001",'),
    ("M2", "a rule is SILENTLY dropped — removed from RULES and never declared in DROPPED (the s214-D6 failure)",
     '        ("rule:dv-bar-010", "Well spaced', '        ("rule:dv-bar-XXX", "Well spaced'),
    ("M3", "the two spark rules are attached to chart-line after all (the review-by-eye is skipped)",
     '    "chart-line": [\n        ("dv-line-009"',
     '    "chart-line": [\n        ("dv-line-00X"'),
    ("M4", "a family rule from data-visualisation.md leaks into a component meta",
     '        ("rule:dv-pie-001",',
     '        ("rule:dv-016", "the family-level contrast rule, smuggled into a component meta while Q2 is open"),\n        ("rule:dv-pie-001",'),
    ("M5", "an authored $why is emptied — the edge becomes inference wearing a ref",
     '("rule:dv-bar-009", "The zero baseline is mandatory for every bar chart: the meta\'s antiPatterns cite this rule by id and name data-domain-min=\\"0\\" as the mechanism.")',
     '("rule:dv-bar-009", "")'),
    ("M6", "a $why is reused verbatim on two rules",
     '("rule:dv-bar-002", "Axis titles on both axes unless the labels are obvious — the get-out clause is the reason this is a judgement the author makes per instance, and the meta\'s axis tokens have to carry either way.")',
     '("rule:dv-bar-002", "A title that reflects the main insight is this meta\'s optional `title` prop, and the rule is why the slot exists at all rather than a bare chart frame.")'),
    ("M7", "a $why is a RESTATEMENT of the rule text instead of an authored binding",
     '("rule:dv-pie-011", "Always indicate rounding: the value',
     '("rule:dv-pie-011", "Always indicate when values are rounded. Always indicate when values are rounded.") if 0 else ("rule:dv-pie-011", "Always indicate when values are rounded. Always indicate when values are rounded.") # ("rule:dv-pie-011", "Always indicate rounding: the value'),
    ("M8", "the splice EATS a byte of the live meta instead of purely inserting (the #179 class)",
     '    out = text[:at] + ins + text[at:]',
     '    out = text[:at] + ins + text[at + 1:]'),
    ("M9", "the splice RE-DUMPS the meta instead of a textual span (#179 proper)",
     '    text = open(src, encoding="utf-8").read()',
     '    text = json.dumps(json.load(open(src, encoding="utf-8")), indent=2, ensure_ascii=False)'),
    ("M10", "OUT is repointed at the live component directory",
     'OUT = os.path.join(HERE, "proposed-metas")', 'OUT = os.path.join(COMPONENTS)'),
    ("M11", "a ux: ref is authored, widening past the ruling's filename-join scope",
     '        ("rule:dv-line-001",',
     '        ("ux:pr-fitts", "a grade-A law citation, which s276-D5 did not put in this lane\'s scope at all"),\n        ("rule:dv-line-001",'),
    ("M12", "a declared drop loses its reason — the drop becomes silent in all but name",
     '("dv-pie-003", "\'Doughnut centre', '("dv-pie-003", "donut") if 0 else ("dv-pie-003", "donut") # ("dv-pie-003", "\'Doughnut centre'),
    ("M13", "a rule id is invented that is not in _rules-index.json",
     '        ("rule:dv-line-011",', '        ("rule:dv-line-012",'),
    ("M14", "the per-file counts are taken from the BRIEF's line instead of measured (10/11/11/19 mis-ordered)",
     'len(bf[FAMILY_FILE])) == (11, 11, 10, 19))',
     'len(bf[FAMILY_FILE])) == (10, 11, 11, 19))'),
    ("M15", "the Q2 family matrix loses a rule — option (b)'s count would be understated",
     '    "dv-018": {"chart-line"', '    "dv-018x": {"chart-line"'),
    ("M16", "a cross-file binding is smuggled in with no declaration (lane TO declared its one)",
     '        ("rule:dv-pie-008",',
     '        ("rule:dv-bar-009", "a cross-file binding from the bar spec, taken without any declaration at all"),\n        ("rule:dv-pie-008",'),
]

BITE_RX = re.compile(r"^\s*(OK|FAIL)\s+bite\s+(\d+)\s+—", re.M)


def main():
    scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    root = scratch / "mutroot"
    lane = root / "notes" / "_lanes" / "277" / "charts"
    lane.mkdir(parents=True, exist_ok=True)
    link = root / "knowledge"
    if not link.exists():
        link.symlink_to(REPO / "knowledge")

    def run(text):
        p = lane / "_author_metas.py"
        p.write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, str(p), "--selftest"],
                           capture_output=True, text=True, timeout=300)
        out = r.stdout + r.stderr
        return sorted(int(n) for st, n in BITE_RX.findall(out) if st == "FAIL"), "Traceback" in out

    red, crash = run(SRC)
    print("BASELINE red=%s crashed=%s — %s\n" % (
        red, crash, "PASS" if not red and not crash else "BROKEN, fix before mutating"))

    rows, survived = [], []
    for mid, desc, old, new in MUTANTS:
        if SRC.count(old) != 1 or old == new:
            rows.append((mid, desc, "PATCH-MISS (anchor x%d)" % SRC.count(old)))
            survived.append(mid)
            continue
        r, crashed = run(SRC.replace(old, new, 1))
        if r:
            v = "RED " + ",".join(map(str, r))
        elif crashed:
            v = "CRASH (the mutant did not even run)"
            survived.append(mid)
        else:
            v = "GREEN — THE MUTANT SURVIVED"
            survived.append(mid)
        rows.append((mid, desc, v))

    w = max(len(r[1]) for r in rows)
    for mid, desc, v in rows:
        print("  %-4s %-*s -> %s" % (mid, w, desc, v))
    print("\n" + ("ALL %d MUTANTS CAUGHT" % len(MUTANTS) if not survived
                  else "SURVIVORS: %s — A SURVIVOR IS A FINDING, NOT A PASS" % survived))
    shutil.rmtree(root, ignore_errors=True)
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
