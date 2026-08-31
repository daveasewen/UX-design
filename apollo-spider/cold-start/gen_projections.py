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

THREE REFUSALS, all deliberate:

  * THE LINE BUDGET. The contract may not exceed 40 lines. Hosts truncate and readers
    skim; a contract that runs long is a contract whose last rule is never read. Depth
    belongs in the skills. Over budget, this script writes NOTHING and says by how much.

  * THE BYTE BUDGET. 4096 bytes, because bytes are what a host actually truncates on and
    lines are not. Forty 20,000-character lines is inside the line budget and is not a
    short contract. Same refusal shape: nothing written, the overage named.

  * NO SILENT WRITE FROM A STALE SOURCE. Rendering is one function used by the writer,
    the checker and the selftest, so they cannot disagree about what correct looks like.

⚠ THE PROJECTIONS ARE TEMPLATES, NOT PLACEMENT. They are written into
`cold-start/projections/`. Getting them to the paths above in a designer's own project is
a separate step, and `verify_placement.py` beside this file is what reports on it.

⚠ THE COPILOT PROJECTION IS A MERGE, AND THAT IS THE POINT. This pack ships its own
`.github/copilot-instructions.md` (the Memento boot rule, the operating rules, the skills
table, the pointer to the `.github/prompts/` slash commands) and Copilot reads exactly that
path. A standalone design-contract projection at the same path could only arrive by
destroying it — so the copilot projection is GENERATED FROM BOTH SOURCES: the design
contract first, then `---`, then the pack's own boot file verbatim. One generated file, two
sources, nothing lost when a designer puts it in place. Edit either source and regenerate;
never hand-edit the merged projection. (Ruled #227, s227-D5 / red-team B2.)

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
BYTE_BUDGET = 4096   # what a host actually truncates on; 40 long lines is not "short"

# key -> (path under projections/, host name, path a designer must place it at)
HOSTS = (
    ("claude", "CLAUDE.md", "Claude", "CLAUDE.md"),
    ("agents", "AGENTS.md", "AGENTS.md agent hosts", "AGENTS.md"),
    ("copilot", os.path.join(".github", "copilot-instructions.md"),
     "GitHub Copilot", ".github/copilot-instructions.md"),
)

# The SECOND source, and only the copilot host merges it: the pack's own boot file, which
# lives at the same path Copilot reads. Relative to this script, so it resolves identically
# in the repo and in an unzipped pack. See the merge note in the docstring.
MERGE_HOSTS = {"copilot"}
MERGE_SOURCE_REL = os.path.join("..", ".github", "copilot-instructions.md")
MERGE_JOIN = "\n\n---\n\n"

HEADER_FMT = ("<!-- GENERATED from cold-start/{source} for {host} — edit the source, not this "
              "file: python3 cold-start/gen_projections.py -->")

MERGED_HEADER_FMT = ("<!-- GENERATED for {host} by MERGING cold-start/{source} with this pack's "
                     "own .github/copilot-instructions.md — edit either SOURCE, never this "
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
    nb = len(text.encode("utf-8"))
    if nb > BYTE_BUDGET:
        raise RuntimeError(
            "REFUSED: %s is %d bytes, %d over the %d-byte budget. Hosts truncate on bytes, "
            "not on lines — a contract inside the line budget can still be too long to "
            "survive one. Cut it, or move the depth into a skill. Nothing was written."
            % (SOURCE_NAME, nb, nb - BYTE_BUDGET, BYTE_BUDGET))
    return text


def read_merge_source(base=HERE):
    """The pack's own copilot boot file — the second source of the merged projection."""
    path = os.path.normpath(os.path.join(base, MERGE_SOURCE_REL))
    if not os.path.exists(path):
        raise RuntimeError(
            "no boot file at %s — the copilot projection is a MERGE of the design contract "
            "and this pack's own Copilot instructions, and half of it is missing. Nothing "
            "was written." % path)
    return open(path, encoding="utf-8").read()


def render(host_name, source_text, merge_text=None):
    """The bytes a projection must contain. The ONLY definition of correct."""
    fmt = MERGED_HEADER_FMT if merge_text is not None else HEADER_FMT
    header = fmt.format(host=host_name, source=SOURCE_NAME)
    body = source_text.lstrip("\n")
    if merge_text is not None:
        body = body.rstrip("\n") + MERGE_JOIN + merge_text.lstrip("\n")
    return header + "\n\n" + body


def expected(base=HERE):
    """{absolute projection path: expected text} for every host."""
    src = read_source(base)
    merged = read_merge_source(base) if MERGE_HOSTS else None
    out = {}
    for key, rel, host_name, _place in HOSTS:
        extra = merged if key in MERGE_HOSTS else None
        out[os.path.join(base, PROJECTIONS_DIR, rel)] = render(host_name, src, extra)
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
        # the second source lives one level up from cold-start/ in both the repo and the
        # unzipped pack — the throwaway tree has to carry it too, or the merge cannot render.
        merge_src = os.path.normpath(os.path.join(base, MERGE_SOURCE_REL))
        os.makedirs(os.path.dirname(merge_src), exist_ok=True)
        shutil.copyfile(os.path.normpath(os.path.join(HERE, MERGE_SOURCE_REL)), merge_src)
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

        # 7. the real source in this repo is inside BOTH budgets
        try:
            read_source(HERE)
        except RuntimeError as e:
            fails.append("the shipped contract is over budget: %s" % e)

        # 8. a source inside the LINE budget but over the BYTE budget REFUSES. One long
        #    line is what the line count cannot see, and it is what a host truncates on.
        before = open(victim, encoding="utf-8").read()
        open(src, "w", encoding="utf-8").write(keep.rstrip("\n") + "\n" + ("x" * (BYTE_BUDGET * 2)) + "\n")
        try:
            write(base)
            fails.append("a 2x-over-BYTE-budget contract was PROJECTED instead of refused")
        except RuntimeError as e:
            if "byte budget" not in str(e):
                fails.append("the over-byte refusal did not name the byte budget: %s" % e)
        if open(victim, encoding="utf-8").read() != before:
            fails.append("the over-byte refusal WROTE — it must touch nothing")
        open(src, "w", encoding="utf-8").write(keep)
        write(base)

        # 9. the copilot projection really is the MERGE, and drift in EITHER source is red.
        cop = os.path.join(base, PROJECTIONS_DIR, HOSTS[2][1])
        cop_text = open(cop, encoding="utf-8").read()
        if "MERGING" not in cop_text.splitlines()[0]:
            fails.append("the copilot projection does not carry the merged header")
        boot_head = open(merge_src, encoding="utf-8").read().splitlines()[0]
        if boot_head not in cop_text:
            fails.append("the copilot projection does not carry the pack's own boot file — "
                         "placing it would still destroy the boot rules (red-team B2)")
        keep_boot = open(merge_src, encoding="utf-8").read()
        open(merge_src, "w", encoding="utf-8").write(
            keep_boot.replace("Read the chain only", "Read whatever you like", 1))
        if not any("DRIFTED" in f for f in check(base)):
            fails.append("an edit to the SECOND source did NOT make the merged projection red")
        open(merge_src, "w", encoding="utf-8").write(keep_boot)
        if check(base):
            fails.append("restoring the second source did not return the tree to green")

        # 10. a MISSING second source refuses loudly rather than silently un-merging.
        os.rename(merge_src, merge_src + ".moved")
        try:
            check(base)
            fails.append("a missing boot file did not refuse — the merge half-vanished quietly")
        except RuntimeError as e:
            if "MERGE" not in str(e).upper():
                fails.append("the missing-boot-file refusal did not name the merge: %s" % e)
        os.rename(merge_src + ".moved", merge_src)
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
        print("gen_projections selftest OK — 10 arm(s), drift planted and seen.")
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
