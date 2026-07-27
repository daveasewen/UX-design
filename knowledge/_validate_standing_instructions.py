#!/usr/bin/env python3
"""_validate_standing_instructions.py — the hook that catches escaped standing instructions.

Dave 2026-07-18: "there must be a hook for catching and adding new useful ones."

THE PROBLEM IT SOLVES. On 2026-07-18 a manual audit found that GOOD-MORNING.md referenced
only 2 of 9 runbooks, and omitted AGENTS.md, MODEL-ROUTING.md, _PROFORMA-RULES.md,
_DS-IMPROVEMENTS.md and _ICON-GAPS.md — plus eight standing agent rules that existed only
in memory. Manual audits find these once; they do not keep finding them. Someone adds the
tenth runbook and nothing tells the next cold session it exists.

WHAT IT CHECKS (repo-side referential completeness)
  STAND-001  every runbook is reachable from the cold-start spine — directly from
             GOOD-MORNING.md, or via the generated _RUNBOOKS.md index which it references
  STAND-002  every standing document (AGENTS, MODEL-ROUTING, *-RULES, *-DECISIONS,
             _DS-IMPROVEMENTS, _ICON-GAPS) is referenced from the spine
  STAND-003  any file declaring `STANDING:` in its first 40 lines must be referenced —
             the self-declaration route, so a new kind of standing doc can opt in without
             this gate needing to know about it in advance
  STAND-004  GOOD-MORNING.md still carries its own structural spine: the two names,
             §A/★ LATEST banner/§C (GM-D4: §B deleted, the banner is the session record),
             and §A's standing-instruction note. §A is the section most at risk
             because it is the only one that does not change each session; on 2026-07-18 a
             from-scratch rewrite silently reduced its instruction to two words.

WHAT IT CANNOT CHECK — BE HONEST ABOUT THIS
  Memory files live OUTSIDE the repo (the Claude memory directory), so this gate cannot see
  them. Eight of the escaped rules found on 07-18 were memory-only. A repo gate can enforce
  that every standing rule IN THE REPO is reachable; it cannot enforce that every rule in
  memory has been written into the repo. That half stays a human step — step 3 of
  _RUNBOOK-capture-ritual.md. Do not let a green gate here imply the memory side is clean.

Usage:  python3 knowledge/_validate_standing_instructions.py
        python3 knowledge/_validate_standing_instructions.py --selftest
Exit non-zero on any violation (blocking). Wired into _build_all.py.
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPINE = [os.path.join(ROOT, "GOOD-MORNING.md"), os.path.join(HERE, "_RUNBOOKS.md")]

# Files that are standing by their nature. Globs, so new ones are caught automatically.
STANDING_GLOBS = [
    os.path.join(HERE, "_RUNBOOK-*.md"),
    os.path.join(ROOT, "AGENTS.md"),
    os.path.join(ROOT, "MODEL-ROUTING.md"),
    os.path.join(HERE, "_proforma", "_*-RULES.md"),
    os.path.join(HERE, "_proforma", "_*-DECISIONS.md"),
    os.path.join(HERE, "_DS-IMPROVEMENTS.md"),
    os.path.join(HERE, "_ICON-GAPS.md"),
]
# Where a new standing doc can opt in by saying so in its own head matter.
SELF_DECLARE = re.compile(r"^[\s>#*_\-]*STANDING:", re.M)

REQUIRED_IN_GOOD_MORNING = [
    (r"RENAME .*CHAT", "the retrospective rename line (capture-ritual step 4b)"),
    (r"TITLE .*CHAT", "the next-session title line (capture-ritual step 4b)"),
    (r"^#\s*§A", "§A Orientation heading"),
    (r"STANDING SECTION", "§A's standing-instruction note — the bit that erodes"),
    # GM-D4(a), 2026-07-27 (`notes/_MEMENTO-DECISIONS.md` § GM growth-contracts): §B is DELETED;
    # the ★ LATEST banner formally absorbs its spec. The spine asserts the banner, not the dead heading.
    # (Phase-1 gap closed at the phase-2 pass: this line still demanded §B while the capture gate
    #  failed on §B's presence — two gates enforcing opposite structures.)
    (r"^>\s*##\s*★ LATEST", "the ★ LATEST session banner (GM-D4: the banner IS the session record)"),
    (r"^#\s*§C", "§C Queue heading"),
]


def spine_text():
    out = []
    for p in SPINE:
        if os.path.exists(p):
            out.append(open(p, encoding="utf-8").read())
    return "\n".join(out)


def standing_files():
    seen = []
    for g in STANDING_GLOBS:
        seen += glob.glob(g)
    # self-declared: any md in knowledge/ or root saying STANDING: near the top
    for g in (os.path.join(HERE, "*.md"), os.path.join(ROOT, "*.md"),
              os.path.join(HERE, "_proforma", "*.md")):
        for p in glob.glob(g):
            try:
                head = "".join(open(p, encoding="utf-8").readlines()[:40])
            except OSError:
                continue
            if SELF_DECLARE.search(head):
                seen.append(p)
    # the spine itself is not "referenced by" the spine
    return sorted({os.path.abspath(p) for p in seen} - {os.path.abspath(p) for p in SPINE})


def run():
    gm_path = os.path.join(ROOT, "GOOD-MORNING.md")
    if not os.path.exists(gm_path):
        print("  ✗ STAND-004  GOOD-MORNING.md is missing — the cold-start spine is gone")
        return 1
    gm = open(gm_path, encoding="utf-8").read()
    text = spine_text()
    viol = []

    for p in standing_files():
        name = os.path.basename(p)
        if name not in text:
            code = "STAND-003" if SELF_DECLARE.search(
                "".join(open(p, encoding="utf-8").readlines()[:40])) else (
                "STAND-001" if name.startswith("_RUNBOOK-") else "STAND-002")
            viol.append((code, name, os.path.relpath(p, ROOT)))

    for pat, what in REQUIRED_IN_GOOD_MORNING:
        if not re.search(pat, gm, re.M | re.I):
            viol.append(("STAND-004", what, "GOOD-MORNING.md"))

    for code, what, where in viol:
        if code == "STAND-004":
            print(f"  ✗ {code}  GOOD-MORNING.md has lost {what}")
        else:
            print(f"  ✗ {code}  {what} is not referenced from the cold-start spine  ({where})")

    if viol:
        print(f"\nSTANDING-INSTRUCTIONS GATE FAIL — {len(viol)} unreachable or missing.")
        print("  A standing rule nothing points to will not survive the next cold session.")
        print("  Fix: reference it from GOOD-MORNING.md §A (or let _RUNBOOKS.md cover runbooks).")
        return 1

    n = len(standing_files())
    print(f"STANDING-INSTRUCTIONS GATE PASS — {n} standing doc(s) reachable from the spine; "
          "GOOD-MORNING structure intact.")
    print("  NOTE: memory files live outside the repo and CANNOT be checked here — "
          "capture-ritual step 3 is still a human step.")
    return 0


def selftest():
    assert SELF_DECLARE.search("STANDING: keep this\n")
    assert SELF_DECLARE.search("> **STANDING:** keep this\n")
    assert not SELF_DECLARE.search("this is not standing: really\n")
    files = standing_files()
    assert files, "should discover standing docs"
    assert any("_RUNBOOK-git-commit.md" in f for f in files), "must discover the git runbook"
    print(f"selftest OK — discovers {len(files)} standing docs by glob + STANDING: self-declaration.")
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    selftest()
    sys.exit(run())
