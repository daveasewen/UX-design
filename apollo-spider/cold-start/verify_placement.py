#!/usr/bin/env python3
"""
verify_placement.py — is the design contract actually where the hosts will read it?

Run this in YOUR OWN project, from its root:

    python3 cold-start/verify_placement.py
    python3 cold-start/verify_placement.py --root ../my-product

The contract only works if the file is in the exact place the host looks. Each host has
its own place and none of them will tell you it found nothing — they simply start with no
rules, improvise, and the first sign of trouble is a screen that ignores the design
system. This script is the thing that tells you.

    CLAUDE.md                        project root   Claude
    AGENTS.md                        project root   agent hosts reading AGENTS.md
    .github/copilot-instructions.md  .github/       GitHub Copilot

Three states per host, and the middle one is the one worth having a script for:

    PLACED    the file is there and it carries the contract
    NO RULES  the file is missing — that host starts cold
    NO RULES  the file is there but the contract is NOT in it (an older instructions file,
              or a merge that dropped it). Present is not the same as correct, and this is
              the failure a "does the file exist" check reads as a pass.

⚠ THE BARE RUN IS ADVISORY AND ALWAYS EXITS 0. It reports; it never blocks and it never
writes. Not every project uses every host, and a missing CLAUDE.md in a Copilot-only shop is a
fact rather than a fault. Read the warnings and decide.

★★ `--require` IS THE BUILD-TIME ARM, AND #230 IS WHY IT EXISTS.

    python3 cold-start/verify_placement.py --require --root <dir>   # exit 1 on any cold host

The #230 rehearsal ran this script on a pristine `Apollo-Spider-v1.0.5` unzip. It printed,
unprompted and correctly:

    NO RULES   CLAUDE.md                       Claude — no file at this path
    NO RULES   AGENTS.md                       AGENTS.md agent hosts — no file at this path
    NO RULES   .github/copilot-instructions.md GitHub Copilot — the file exists but the design
                                               contract is not in it
    ⚠ 3 of 3 hosts start COLD here.

…and exited 0, and nothing in the install path ran it at all. Three of the pack's five pass
beats had no instruction to fire from, and the instrument that could have said so had no
consumer [[instrument-without-a-consumer]]. The advisory exit is right for a DESIGNER'S
project and wrong for a BAKE, so the two runs are now different commands: the designer's is
unchanged, and `--require` is what `build-designer-pack.sh` calls over the staged pack before
it zips. A pack whose own hosts are cold no longer becomes a release.

⚠ ADVISORY AND BLOCKING ARE THE SAME READING. `--require` does not re-implement the check —
it runs `inspect()` and refuses on the same rows the bare run prints. Two copies of a test
drift; one reading with two exit policies cannot.

`--selftest` plants each state in a throwaway directory and fails loud if the check cannot see
it — including BOTH exit policies, driven rather than asserted. A checker nobody has watched go
red has proved nothing.
"""
import os
import shutil
import sys
import tempfile

if __name__ == "__main__" and ("-h" in sys.argv[1:] or "--help" in sys.argv[1:]):
    print((__doc__ or "").strip())
    sys.exit(0)

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "DESIGN-CONTRACT.md")

# The phrases that say "the contract is in this file". One is the contract's first
# instruction; the other opens the five rules. BOTH are required, because a merge that keeps
# the opening line and drops the rules is exactly the failure this check exists for — one
# marker read PLACED for a gutted contract, and for an inverted one. --selftest asserts both
# are still present in DESIGN-CONTRACT.md, so a reword cannot silently blind this check.
MARKERS = ("Declare the lane, in your first reply.",   # §1 — the lane
           "**Never invent.**")                        # §3 — the rules block

HOSTS = (
    ("Claude", "CLAUDE.md"),
    ("AGENTS.md agent hosts", "AGENTS.md"),
    ("GitHub Copilot", os.path.join(".github", "copilot-instructions.md")),
)


def inspect(root):
    """[(host, relpath, state, detail)] — state is 'placed' | 'missing' | 'no-contract'."""
    rows = []
    for host, rel in HOSTS:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            rows.append((host, rel, "missing", "no file at this path"))
            continue
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError as e:
            rows.append((host, rel, "no-contract", "could not be read: %s" % e))
            continue
        absent = [m for m in MARKERS if m not in text]
        if not absent:
            rows.append((host, rel, "placed", "carries the contract"))
        elif len(absent) == len(MARKERS):
            rows.append((host, rel, "no-contract",
                         "the file exists but the design contract is not in it"))
        else:
            rows.append((host, rel, "no-contract",
                         "the file carries part of the contract but not all of it — missing: "
                         + " / ".join(repr(m) for m in absent)))
    return rows


def report(root, out=print):
    rows = inspect(root)
    placed = [r for r in rows if r[2] == "placed"]
    out("Design contract placement — %s" % os.path.abspath(root))
    out("")
    for host, rel, state, detail in rows:
        if state == "placed":
            out("  PLACED     %-31s %s" % (rel, host))
        else:
            out("  NO RULES   %-31s %s — %s" % (rel, host, detail))
    out("")
    if len(placed) == len(rows):
        out("All %d hosts will read the contract before they build." % len(rows))
    else:
        out("⚠ %d of %d hosts start COLD here. An assistant with no rules loaded does not"
            % (len(rows) - len(placed), len(rows)))
        out("  say so — it improvises, and the design system is never consulted.")
        out("")
        out("  Copy the projections into place:")
        for host, rel, state, _detail in rows:
            if state == "no-contract":
                out("    MERGE cold-start/projections/%s INTO %s — do not overwrite it, that "
                    "file may already carry other rules" % (rel, rel))
            elif state != "placed":
                out("    cold-start/projections/%s  ->  %s" % (rel, rel))
        out("")
        out("  If a host is one you do not use, this warning is a fact, not a fault.")
    return rows


def selftest():
    fails = []
    if not os.path.exists(SOURCE):
        fails.append("no DESIGN-CONTRACT.md beside this script")
    else:
        src_text = open(SOURCE, encoding="utf-8").read()
        for m in MARKERS:
            if m not in src_text:
                fails.append("MARKER %r is NOT in DESIGN-CONTRACT.md — the contract was reworded "
                             "and this check now reports 'no contract' for a correctly placed "
                             "file. Update MARKERS." % m)

    tmp = tempfile.mkdtemp(prefix="verify-placement-selftest-")
    try:
        quiet = lambda *_a, **_k: None  # noqa: E731 - the report's text is not under test here

        # 1. an empty project: every host cold
        states = {h: s for h, _r, s, _d in report(tmp, out=quiet)}
        if set(states.values()) != {"missing"}:
            fails.append("an empty project did not read as all-missing: %s" % states)

        # 2. a file that exists but does NOT carry the contract must NOT read as placed
        open(os.path.join(tmp, "CLAUDE.md"), "w").write("# notes\nsome older instructions\n")
        row = [r for r in inspect(tmp) if r[1] == "CLAUDE.md"][0]
        if row[2] != "no-contract":
            fails.append("a file present WITHOUT the contract read as %r — present is not "
                         "correct, and this is the state the check exists for" % row[2])

        # 3. the real projections, placed, read as placed
        proj = os.path.join(HERE, "projections")
        for _host, rel in HOSTS:
            src = os.path.join(proj, rel)
            if not os.path.exists(src):
                fails.append("projection %s is missing — run gen_projections.py" % rel)
                continue
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        states = {r[1]: r[2] for r in inspect(tmp)}
        if set(states.values()) != {"placed"}:
            fails.append("the real projections, correctly placed, did not read as placed: %s"
                         % states)

        # 4. the advisory run really does exit 0 on a cold project (the whole contract of
        #    this script). Driven, not asserted from the source.
        empty = os.path.join(tmp, "cold")
        os.makedirs(empty, exist_ok=True)
        code = run(empty, out=quiet)
        if code != 0:
            fails.append("the advisory run exited %r on a cold project — it must always be 0"
                         % code)

        # 5. a gutted contract — the opening line kept, the rules block dropped — must NOT
        #    read as placed. This is the merge the docstring names, and one marker missed it.
        gutted = os.path.join(tmp, "gutted")
        os.makedirs(gutted, exist_ok=True)
        open(os.path.join(gutted, "CLAUDE.md"), "w", encoding="utf-8").write(
            "# rules\nAlways be nice. %s\n" % MARKERS[0])
        row = [r for r in inspect(gutted) if r[1] == "CLAUDE.md"][0]
        if row[2] != "no-contract":
            fails.append("a contract with the lane line but no rules block read as %r — that "
                         "is the merge this check exists to catch" % row[2])

        # 6. a --root that is not a directory must say so, not report a cold project. Driven
        #    both ways: a path that does not exist, and a path to a real FILE.
        for bad in (os.path.join(tmp, "NO-SUCH-DIR"), SOURCE):
            lines = []
            code = run(bad, out=lines.append)
            if code != 0 or not any("NOT A DIRECTORY" in ln for ln in lines):
                fails.append("--root %s did not report NOT A DIRECTORY (rc=%r): %r"
                             % (bad, code, lines[:2]))

        # ── #230 F1 ARMS 7–10: `--require`, the BUILD-TIME arm, driven in both directions ────
        # ⛔ THE ENTRY POINT IS WHAT IS BITTEN, NOT A PREDICATE. `run()` is called and its EXIT
        # CODE is read [[mutation-tests-the-clause-not-the-feature]] — the defect being fenced
        # is precisely a check that reported correctly and returned 0.
        # 7. a cold project must RED under --require (the exact #230 rehearsal state)
        if run(empty, out=quiet, require=True) == 0:
            fails.append("--require passed on a project where 3 of 3 hosts start COLD. That is "
                         "the #230 F1 defect exactly: the check was always right and always "
                         "exited 0, so nothing in the install path could act on it.")
        # 8. and the CONTROL: the same tree with the projections placed must GO GREEN, or arm 7
        #    is passing because --require can never pass at all.
        if run(tmp, out=quiet, require=True) != 0:
            fails.append("--require failed on a tree where every host carries the contract — a "
                         "build gate that cannot go green blocks every cut and teaches its "
                         "readers to skip it")
        # 9. the advisory run on that SAME cold tree must still exit 0. The designer-facing
        #    contract is unchanged, and this is what proves the two policies did not merge.
        if run(empty, out=quiet) != 0:
            fails.append("the bare advisory run stopped exiting 0 — --require has leaked into "
                         "the designer's run, which is not what the docstring promises")
        # 10. a bad --root REDS under --require. A build gate that shrugs at a mistyped stage
        #     path passes every cut without inspecting anything.
        if run(os.path.join(tmp, "NO-SUCH-DIR"), out=quiet, require=True) == 0:
            fails.append("--require passed on a root it could not inspect — the most confident "
                         "kind of nothing")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return fails


def run(root, out=print, require=False):
    # A typo'd --root must not print the tool's most alarming output. Without this, both a
    # non-existent path and a path to a FILE produce a confident "3 of 3 hosts start COLD
    # here" — indistinguishable from a real cold project.
    #
    # ⛔ #230: UNDER `--require`, A BAD ROOT IS A FAILURE, NOT A FACT. The advisory run is
    # allowed to shrug at a path it cannot inspect; a build gate that shrugged would pass every
    # cut whose stage path was mistyped, which is the most confident kind of nothing. Same
    # reading, different consequence — and the consequence is named in the line.
    if not os.path.isdir(root):
        out("NOT A DIRECTORY: %s — nothing was inspected." % root)
        if require:
            out("⛔ --require: a build gate cannot pass on a root it could not inspect.")
            return 1
        return 0
    rows = report(root, out=out)
    if require:
        cold = [r for r in rows if r[2] != "placed"]
        if cold:
            out("")
            out("⛔ --require: %d of %d hosts would start COLD in this tree, so this is not a "
                "shippable pack." % (len(cold), len(rows)))
            out("   The contract is GENERATED into these paths — run "
                "`python3 cold-start/gen_projections.py` and bake again. Do not hand-paste: the "
                "placed files are byte-derived and `gen_projections.py --check` will red on it.")
            return 1
        out("")
        out("✅ --require: all %d hosts carry the contract." % len(rows))
    return 0


def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("verify_placement SELFTEST FAIL:")
            for f in fails:
                print("  X " + f)
            sys.exit(1)
        print("verify_placement selftest OK — 10 arm(s).")
        return
    root = os.getcwd()
    if "--root" in sys.argv:
        i = sys.argv.index("--root")
        if i + 1 >= len(sys.argv):
            print("--root needs a directory. Reporting on the current one instead.")
        else:
            root = sys.argv[i + 1]
    sys.exit(run(root, require="--require" in sys.argv))


if __name__ == "__main__":
    main()
