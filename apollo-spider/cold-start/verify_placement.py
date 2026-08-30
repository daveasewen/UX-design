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

⚠ THIS IS ADVISORY AND ALWAYS EXITS 0. It reports; it never blocks and it never writes.
Not every project uses every host, and a missing CLAUDE.md in a Copilot-only shop is a
fact rather than a fault. Read the warnings and decide.

The one exception is `--selftest`, which is the build-time arm rather than the designer's
run: it plants each state in a throwaway directory and fails loud if the check cannot see
it. A checker nobody has watched go red has proved nothing.
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

# The phrase that says "the contract is in this file". It is the contract's first
# instruction, so a file carrying it carries the part that matters most. --selftest asserts
# it is still present in DESIGN-CONTRACT.md, so a reword cannot silently blind this check.
MARKER = "Declare the lane, in your first reply."

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
        if MARKER in text:
            rows.append((host, rel, "placed", "carries the contract"))
        else:
            rows.append((host, rel, "no-contract",
                         "the file exists but the design contract is not in it"))
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
            if state != "placed":
                out("    cold-start/projections/%s  ->  %s" % (rel, rel))
        out("")
        out("  If a host is one you do not use, this warning is a fact, not a fault.")
    return rows


def selftest():
    fails = []
    if not os.path.exists(SOURCE):
        fails.append("no DESIGN-CONTRACT.md beside this script")
    elif MARKER not in open(SOURCE, encoding="utf-8").read():
        fails.append("MARKER is NOT in DESIGN-CONTRACT.md — the contract was reworded and this "
                     "check now reports 'no contract' for a correctly placed file. Update MARKER.")

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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return fails


def run(root, out=print):
    report(root, out=out)
    return 0


def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("verify_placement SELFTEST FAIL:")
            for f in fails:
                print("  X " + f)
            sys.exit(1)
        print("verify_placement selftest OK — 4 arm(s).")
        return
    root = os.getcwd()
    if "--root" in sys.argv:
        i = sys.argv.index("--root")
        if i + 1 >= len(sys.argv):
            print("--root needs a directory. Reporting on the current one instead.")
        else:
            root = sys.argv[i + 1]
    sys.exit(run(root))


if __name__ == "__main__":
    main()
