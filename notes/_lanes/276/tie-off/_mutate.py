#!/usr/bin/env python3
"""_mutate.py — the mutation harness for lane TO's two builders (#276).

A bite that cannot fail is not a test, and a mutation test proves the CLAUSE,
not the feature. Each mutant is a one-line edit to a builder's source; the
harness runs that builder's `--selftest` in an ISOLATED tree and records which
bites turned RED. Nothing in the repo is written: the mutant lives under
<scratch>/mutroot/notes/_lanes/276/tie-off/ with knowledge/ symlinked in
read-only, and the tree is removed at the end.

    python3 notes/_lanes/276/tie-off/_mutate.py [scratch-dir]
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
RULES_SRC = (LANE / "_build_rules.py").read_text(encoding="utf-8")
METAS_SRC = (LANE / "_author_metas.py").read_text(encoding="utf-8")

# (id, target script, description, anchor, replacement)
MUTANTS = [
    ("M1", "rules", "an AAA criterion is graded serious (the corpus's AAA=minor pattern broken)",
     'spacing ≥ 1.5× that; resize to 200% with no horizontal scrolling to read a line.", "minor"),',
     'spacing ≥ 1.5× that; resize to 200% with no horizontal scrolling to read a line.", "serious"),'),
    ("M2", "rules", "the pending-EN-301-549 clause is stamped on every rule, not just the 2.2 three",
     '    if sc in WCAG22_NEW:', '    if True:'),
    ("M3", "rules", "an eighteenth criterion is smuggled in",
     'WHY_SEVERITY = {', 'FACTS = FACTS + [("9.9.9", "made-up", "Made Up", "A", ["2.2"], "manual", "x" * 60, "minor")]\n\nWHY_SEVERITY = {'),
    ("M4", "rules", "2.4.13 is demoted to AA (the AAA set no longer matches the ruling set)",
     '"Focus Appearance", "AAA", ["2.2"],', '"Focus Appearance", "AA", ["2.2"],'),
    ("M5", "rules", "the internal policy sentence is retyped instead of copied from the corpus",
     'POLICY = ("HSBC digital accessibility framework', 'POLICY = ("HSBC accessibility framework'),
    ("M6", "rules", "the file id stops matching the W3C page slug",
     '        "id": "wcag-%s-%s" % (sc, slug),', '        "id": "wcag-%s-%s" % (sc, slug.split("-")[0]),'),
    ("M7", "rules", "applies_to is guessed instead of left for the generator to derive",
     '        "applies_to": [],', '        "applies_to": ["Button", "Links"],'),
    ("M8", "rules", "a WCAG 2.2 addition claims to have existed in 2.1",
     '"Redundant Entry", "A", ["2.2"],', '"Redundant Entry", "A", ["2.1", "2.2"],'),
    ("M9", "rules", "a rule is graded critical (a tier the corpus reserves for 2.1.1/2.1.2/4.1.2)",
     '"paste), object recognition, or user-provided personal content is offered.", "serious"),',
     '"paste), object recognition, or user-provided personal content is offered.", "critical"),'),
    ("M10", "rules", "the dry run counts a null as resolved without the sc actually being present",
     '    after = have | proposed', '    after = have'),
    ("M11", "rules", "external_automatable_refs is hand-typed instead of left to the axe importer",
     '        "external_automatable_refs": [],',
     '        "external_automatable_refs": [{"source": "axe-core", "rule_id": "guessed"}],'),
    ("M12", "rules", "OUT is repointed at the live compliance corpus",
     'OUT = os.path.join(HERE, "proposed-rules")', 'OUT = os.path.join(K, "compliance", "rules")'),
    ("M13", "metas", "a regex-style false positive is admitted (va25-013, the exact s274-D12 case)",
     '        ("rule:ctkt-002",', '        ("rule:va25-013", "a false positive of the kind s274-D12 refused, forty characters long"),\n        ("rule:ctkt-002",'),
    ("M14", "metas", "a ux: ref that is not one of the six grade-A laws",
     '        ("ux:pr-hick", "ctkt-003 orders a group', '        ("ux:pr-affordance", "ctkt-003 orders a group'),
    ("M15", "metas", "an authored $why is emptied — the edge becomes inference wearing a ref",
     '("rule:ctkb-009", "Buttons are always rectangular, never rounded — a shape token fixed for this atom."),',
     '("rule:ctkb-009", ""),'),
    ("M16", "metas", "the splice EATS a byte of the live meta instead of purely inserting",
     '    out = text[:at] + ins + text[at:]',
     '    out = text[:at] + ins + text[at + 1:]'),
    ("M17", "metas", "icon-button claims a rule Button itself does not obey",
     '        ("rule:ctkb-002", "This meta says it shares Button\'s four-level',
     '        ("rule:ctkl-004", "This meta says it shares Button\'s four-level'),
    ("M18", "metas", "one $why is reused verbatim on two components",
     '        ("rule:ctkb-009", "Buttons are always rectangular, never rounded — a shape token fixed for this atom."),\n        ("rule:ctkb-010"',
     '        ("rule:ctkb-009", "Always rectangular, never rounded — a shape token shared with Button."),\n        ("rule:ctkb-010"'),
]

BITE_RX = re.compile(r"^\s*(OK|FAIL)\s+bite\s+(\d+)\s+—", re.M)
SCRIPT = {"rules": "_build_rules.py", "metas": "_author_metas.py"}


def main():
    scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    root = scratch / "mutroot"
    lane = root / "notes" / "_lanes" / "276" / "tie-off"
    lane.mkdir(parents=True, exist_ok=True)
    link = root / "knowledge"
    if not link.exists():
        link.symlink_to(REPO / "knowledge")

    def run(which, text):
        p = lane / SCRIPT[which]
        p.write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, str(p), "--selftest"],
                           capture_output=True, text=True, timeout=300)
        out = r.stdout + r.stderr
        return sorted(int(n) for st, n in BITE_RX.findall(out) if st == "FAIL"), "Traceback" in out

    src = {"rules": RULES_SRC, "metas": METAS_SRC}
    for which in ("rules", "metas"):
        red, crash = run(which, src[which])
        print("BASELINE %-6s red=%s crashed=%s — %s" % (
            which, red, crash, "PASS" if not red and not crash else "BROKEN, fix before mutating"))
    print()

    rows, survived = [], []
    for mid, which, desc, old, new in MUTANTS:
        s = src[which]
        if s.count(old) != 1 or old == new:
            rows.append((mid, which, desc, "PATCH-MISS (anchor x%d)" % s.count(old)))
            survived.append(mid)
            continue
        red, crashed = run(which, s.replace(old, new, 1))
        if red:
            v = "RED " + ",".join(map(str, red))
        elif crashed:
            v = "CRASH (the mutant did not even run)"
            survived.append(mid)
        else:
            v = "GREEN — THE MUTANT SURVIVED"
            survived.append(mid)
        rows.append((mid, which, desc, v))

    w = max(len(r[2]) for r in rows)
    for mid, which, desc, v in rows:
        print("  %-4s %-6s %-*s -> %s" % (mid, which, w, desc, v))
    print("\n" + ("ALL %d MUTANTS CAUGHT" % len(MUTANTS) if not survived else "SURVIVORS: %s" % survived))
    shutil.rmtree(root, ignore_errors=True)
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
