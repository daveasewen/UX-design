#!/usr/bin/env python3
"""
gen_projections.py — project the ONE design contract into the three host files.

THE PROBLEM THIS EXISTS FOR. An assistant can start cold: no skill invoked, one short
prompt ("build me a dashboard"). Nothing loads, it improvises, and the designer files a
bug against a design system that was never consulted. The remedy is a contract the host
reads before anything else — and every host wants it in a different file:

    CLAUDE.md                        repo root      Claude / Claude Code
    AGENTS.md                        repo root      the open agents convention
    .github/copilot-instructions.md  .github/       GitHub Copilot (the primary corp path)

Three files saying the same thing is three files that drift. So there is ONE source —
`DESIGN-CONTRACT.md`, beside this script — and the three are GENERATED from it, byte for
byte, each carrying a header that says where to edit instead.

    python3 cold-start/gen_projections.py            # write the projections
    python3 cold-start/gen_projections.py --check     # verify in sync (build gate)
    python3 cold-start/gen_projections.py --selftest  # plant drift, prove --check sees it

--check is BYTE-DERIVED: it renders what each projection should be and compares the whole
file. A hand-edit of one word anywhere in a projection is red. That is the point — the
header asks for the source to be edited, and this is what makes the ask enforceable
rather than decorative.

TWO REFUSALS, both deliberate:

  * THE LINE BUDGET. The contract may not exceed 40 lines. Hosts truncate and readers
    skim; a contract that runs long is a contract whose last rule is never read. Depth
    belongs in the skills. Over budget, this script writes NOTHING and says by how much.

  * NO SILENT WRITE FROM A STALE SOURCE. Rendering is one function used by the writer,
    the checker and the selftest, so they cannot disagree about what correct looks like.

⚠ THE PROJECTIONS ARE TEMPLATES, NOT PLACEMENT. They are written into
`cold-start/projections/`. Getting them to the paths above in a designer's own project is
a separate step, and `verify_placement.py` beside this file is what reports on it.

⚠ THIS PACK ALREADY SHIPS ITS OWN `.github/copilot-instructions.md` (the Memento boot
rules). The projection here is the DESIGN contract, a different document with a different
job. Whether the two are merged in the shipped pack or kept apart is a placement
decision, not this generator's to make — it owns `cold-start/projections/` and nothing
else.

⚠ NO `_helpgate` IMPORT. The repo's shared help gate resolves by walking up for
`_helpgate.py`; from `cold-start/` that walk finds nothing in the repo and nothing in an
unzipped pack either. Rather than ship an import that works on one side of the release
boundary, the guard is inlined below — same contract, no walk.
"""
import os
import shutil
import sys
import tempfile

# ---------------------------------------------------------------- inline help gate (#158 class)
# A generator must never reach a write on the --help path. Inlined for the reason in the
# docstring; behaviour is the shared gate's: print the docstring, exit 0, write nothing.
if __name__ == "__main__" and ("-h" in sys.argv[1:] or "--help" in sys.argv[1:]):
    print((__doc__ or "").strip())
    sys.exit(0)

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = "DESIGN-CONTRACT.md"
PROJECTIONS_DIR = "projections"

# The contract's hard budget. Front-loaded and short, or it does not get read.
LINE_BUDGET = 40

# key -> (path under projections/, host name, path a designer must place it at)
HOSTS = (
    ("claude", "CLAUDE.md", "Claude", "CLAUDE.md"),
    ("agents", "AGENTS.md", "AGENTS.md agent hosts", "AGENTS.md"),
    ("copilot", os.path.join(".github", "copilot-instructions.md"),
     "GitHub Copilot", ".github/copilot-instructions.md"),
)

HEADER_FMT = ("<!-- GENERATED from cold-start/{source} for {host} — edit the source, not this "
              "file: python3 cold-start/gen_projections.py -->")


# ---------------------------------------------------------------- rendering (one function)
def read_source(base=HERE):
    """The contract's text, and the refusal if it is over budget."""
    path = os.path.join(base, SOURCE_NAME)
    if not os.path.exists(path):
        raise RuntimeError("no source contract at %s — nothing to project." % path)
    text = open(path, encoding="utf-8").read()
    n = len(text.splitlines())
    if n > LINE_BUDGET:
        raise RuntimeError(
            "REFUSED: %s is %d lines, %d over the %d-line budget. A contract that runs long "
            "is one whose last rule never gets read — cut it, or move the depth into a skill. "
            "Nothing was written." % (SOURCE_NAME, n, n - LINE_BUDGET, LINE_BUDGET))
    return text


def render(host_name, source_text):
    """The bytes a projection must contain. The ONLY definition of correct."""
    header = HEADER_FMT.format(host=host_name, source=SOURCE_NAME)
    return header + "\n\n" + source_text.lstrip("\n")


def expected(base=HERE):
    """{absolute projection path: expected text} for every host."""
    src = read_source(base)
    out = {}
    for _key, rel, host_name, _place in HOSTS:
        out[os.path.join(base, PROJECTIONS_DIR, rel)] = render(host_name, src)
    return out


# ---------------------------------------------------------------- the three arms
def write(base=HERE):
    wrote, same = [], []
    for path, text in expected(base).items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current == text:
            same.append(path)
            continue
        open(path, "w", encoding="utf-8").write(text)
        wrote.append(path)
    return wrote, same


def check(base=HERE):
    """[] when every projection matches the source byte for byte."""
    fails = []
    for path, text in expected(base).items():
        rel = os.path.relpath(path, base)
        if not os.path.exists(path):
            fails.append("%s is MISSING — run the generator." % rel)
            continue
        current = open(path, encoding="utf-8").read()
        if current == text:
            continue
        if current.splitlines()[:1] != text.splitlines()[:1]:
            fails.append("%s: the GENERATED header has been edited or lost." % rel)
        else:
            fails.append("%s: body has DRIFTED from cold-start/%s — it was hand-edited, or the "
                         "source moved and this was not regenerated." % (rel, SOURCE_NAME))
    return fails


def selftest():
    """Plant each defect in a throwaway copy and prove --check goes red for it."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="cold-start-selftest-")
    try:
        base = os.path.join(tmp, "cold-start")
        shutil.copytree(HERE, base, ignore=shutil.ignore_patterns("__pycache__"))
        write(base)

        # 1. a freshly written tree is green
        if check(base):
            fails.append("a freshly generated tree is not green: %s" % check(base))

        # 2. writing twice is a no-op (deterministic)
        wrote, _same = write(base)
        if wrote:
            fails.append("generator is not idempotent — a second run rewrote %s" % wrote)

        victim = os.path.join(base, PROJECTIONS_DIR, HOSTS[0][1])

        # 3. a hand-edited BODY is red
        good = open(victim, encoding="utf-8").read()
        open(victim, "w", encoding="utf-8").write(good.replace("Never invent", "Sometimes invent", 1))
        red = check(base)
        if not any("DRIFTED" in f for f in red):
            fails.append("a hand-edited projection body did NOT go red")
        open(victim, "w", encoding="utf-8").write(good)

        # 4. a stripped header is red
        open(victim, "w", encoding="utf-8").write("\n".join(good.splitlines()[1:]))
        if not any("header" in f for f in check(base)):
            fails.append("a stripped GENERATED header did NOT go red")
        open(victim, "w", encoding="utf-8").write(good)

        # 5. a deleted projection is red
        os.remove(victim)
        if not any("MISSING" in f for f in check(base)):
            fails.append("a deleted projection did NOT go red")
        write(base)

        # 6. an over-budget source REFUSES, and writes nothing
        src = os.path.join(base, SOURCE_NAME)
        keep = open(src, encoding="utf-8").read()
        before = open(victim, encoding="utf-8").read()
        open(src, "w", encoding="utf-8").write(keep + "\npadding\n" * (LINE_BUDGET + 5))
        try:
            write(base)
            fails.append("an over-budget contract was PROJECTED instead of refused")
        except RuntimeError as e:
            if "budget" not in str(e):
                fails.append("the over-budget refusal did not name the budget: %s" % e)
        if open(victim, encoding="utf-8").read() != before:
            fails.append("the over-budget refusal WROTE — it must touch nothing")
        open(src, "w", encoding="utf-8").write(keep)

        # 7. the real source in this repo is inside its budget
        try:
            read_source(HERE)
        except RuntimeError as e:
            fails.append("the shipped contract is over budget: %s" % e)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return fails


def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("gen_projections SELFTEST FAIL:")
            for f in fails:
                print("  X " + f)
            sys.exit(1)
        print("gen_projections selftest OK — 7 arm(s), drift planted and seen.")
        return

    try:
        if "--check" in sys.argv:
            fails = check()
            if fails:
                print("gen_projections --check: the host projections are OUT OF SYNC with "
                      "cold-start/%s." % SOURCE_NAME)
                for f in fails:
                    print("  X " + f)
                print("  Fix the SOURCE, then: python3 cold-start/gen_projections.py")
                sys.exit(1)
            print("gen_projections --check OK — %d projection(s) in sync with cold-start/%s."
                  % (len(HOSTS), SOURCE_NAME))
            return
        wrote, same = write()
        for p in wrote:
            print("wrote %s" % os.path.relpath(p, HERE))
        if not wrote:
            print("gen_projections: no change (%d projection(s) already in sync)." % len(same))
        else:
            print("gen_projections: %d written, %d unchanged." % (len(wrote), len(same)))
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
