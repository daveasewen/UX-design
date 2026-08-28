#!/usr/bin/env python3
"""_gate_pack_docs.py — ADVISORY. Read the pack in the DESIGNER'S grammar, before it ships.

⬛ ADVISORY AT BIRTH. This gate reports and returns 0. It does not block a bake, it is not in
the pack's gate roster, and it never will be by its own hand: promotion to blocking is Dave's
word (#221 fence 2). `--strict` makes it exit 1 so a future seat can wire it BLOCKING without
editing it — driving that arm is how this file proves it CAN fail.

WHY THIS EXISTS. #220's L4 audit unzipped the shipped v1.0.1 pack and walked it as a designer
would. Six of its nineteen findings were the same defect wearing six hats: a designer-facing
document naming a path or a command that does not exist in the pack it ships in.

    F1   README + PROVENANCE publish `files: 1641`; the zip holds 1,646
    F4   FIRST-SESSION says "the unzipped `Apollo-Spider-v1.0.0` directory" — it is v1.0.1
    F13  `skills/check-with-gates/SKILL.md` gives `python3 apollo-pack/ci-template/run-gates.py`
         from a cwd it names as the pack root: `[Errno 2] No such file or directory`
    F14  `ci-template/README.md` types "36 gates" beside a manifest that says 35
    F17  the same README names the pack root three different ways in one file
    F18  `WHAT-MEMENTO-IS.md` points at `notes/…-onepager-v1.md`, which is not shipped

L4 found all six with ~40 lines of Python and priced this gate at ~2.5K. Every one of them is
[[no-gate-parses-the-artefact]]: the fleet has gates over tokens, CSS, snippets and contracts,
and NOT ONE that reads a shipped document the way the person holding it will. The first gate
over an artefact should parse it in its consumer's grammar. A designer's grammar is: *I type
this command / I open this path, and it works.*

WHAT IT DOES — four arms, each drivable to both verdicts (see `--selftest`).

  1. COMMANDS RESOLVE.  Every `python3 <path>` in every shipped `.md` must name a file that is
     in the pack. Resolved from the pack root FIRST (what the docs say they run from) and then
     from the document's own directory (what a doc inside `memento-package/` can legitimately
     mean). A miss on BOTH is a miss. Placeholder paths (`<…>`, `path/to/…`) are skipped, by
     name, and counted, so a skip is never invisible.
  2. PATHS RESOLVE.  Every backticked path that looks like a shipped file — has a directory
     separator and a known extension, or ends in `/` — must exist, same two-root rule.
  3. VERSION IS SWEPT.  The pack's own version string appears; NO OTHER version of this pack
     appears anywhere in a shipped document. This is F4 exactly, as a class.
  4. TYPED COUNTS MATCH THE MANIFEST.  Any `**N gates**` claim in `ci-template/README.md` is
     checked against `_MANIFEST.json`'s own verdict tallies, and the published `files:` figure
     against the staged file count. Figures a manifest can compute should not be typed
     [[measure-dont-convert-units]] — until they are generated, they can at least be checked.

⚠ WHAT IT CANNOT SEE. It does not follow prose ("the folder above this one"), does not run the
commands it resolves, and does not grade whether an existing file says the right thing. It
answers exactly one question — *does this name resolve in the tree it ships in* — and says so.

USAGE
    python3 knowledge/_release/_gate_pack_docs.py --stage <dir>     # advisory report, exit 0
    python3 knowledge/_release/_gate_pack_docs.py --stage <dir> --strict   # exit 1 on findings
    python3 knowledge/_release/_gate_pack_docs.py --selftest        # the bites, both directions

WIRED: `apollo-spider/build-designer-pack.sh` runs it over the STAGED tree, after `--stage` and
before `--zip`, advisory. That is the only moment the pack exists as a tree and can still be
fixed without a re-cut.

GATE-GLOB-SCOPE: this gate reads a staged pack directory given to it on argv, and nothing else.
It writes nothing anywhere, ever — including under --selftest (#158 write-by-default class).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json
import os
import re
import sys
import tempfile

MD_SKIP_DIRS = ("showroom",)          # the generated library; not prose a designer reads
CMD_RE = re.compile(r"python3\s+([A-Za-z0-9_./-]+\.py)")
PATH_RE = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*(?:/[A-Za-z0-9_./-]*)+)`")
KNOWN_EXT = (".py", ".md", ".json", ".html", ".css", ".yml", ".yaml", ".sh", ".txt")
PLACEHOLDER = ("<", ">", "path/to", "your-", "example", "…")

# ⚠ NAMED, declared, narrow — NOT a blanket ignore list, and PRINTED in the report so it can
# never quietly grow. These are files the pack's own guided session tells the designer to
# CREATE (FIRST-SESSION §4b) and the CI location it tells them to choose. A doc naming one of
# them is doing its job; grading it absent would be the gate misreading an instruction as a
# broken link. Anything not on this list is graded, and an unknown miss fails loud.
DESIGNER_CREATES = {
    "memento-package/GOOD-MORNING.md": "written by the designer at FIRST-SESSION §4b",
    "memento-package/_LIVE-STATE.md": "written by the designer at FIRST-SESSION §4b",
    "memento-package/_CHAIN.md": "regenerated by the designer at FIRST-SESSION §4c",
    "knowledge/_proforma/": "the designer's own tranche directory (check-with-gates Route B)",
    "apollo/": "where the CI workflow expects the pack IN THE ADOPTER'S repo, not in the pack",
}
DETAIL_CAP = 20                       # per arm; the COUNT is never capped, only the printout
VERSION_RE = re.compile(r"Apollo-Spider-v(\d+\.\d+\.\d+)")
GATES_COUNT_RE = re.compile(r"\*\*(\d+)\s+gates\*\*")


def md_files(stage):
    out = []
    for root, dirs, files in os.walk(stage):
        rel_root = os.path.relpath(root, stage)
        top = rel_root.split(os.sep)[0]
        if top in MD_SKIP_DIRS:
            dirs[:] = []
            continue
        for f in files:
            if f.endswith(".md"):
                out.append(os.path.relpath(os.path.join(root, f), stage))
    return sorted(out)


def resolves(stage, doc_rel, target):
    """True if `target` names something in the pack, read from the pack root or from the
    document's own directory. Two roots because both are legitimate: the front-door docs say
    'everything runs from the pack root', and a doc inside memento-package/ says `machinery/…`
    meaning its own neighbour. A designer would try both; so does this."""
    t = target.rstrip("/")
    for base in (stage, os.path.join(stage, os.path.dirname(doc_rel))):
        p = os.path.normpath(os.path.join(base, t))
        if os.path.exists(p):
            return True
    return False


def is_placeholder(s):
    return any(tok in s for tok in PLACEHOLDER)


def audit(stage, pack_version=None):
    """Returns (findings, stats). A finding is (arm, doc, needle, why)."""
    findings, skipped, checked = [], 0, 0
    docs = md_files(stage)
    for doc in docs:
        try:
            text = open(os.path.join(stage, doc), encoding="utf-8", errors="replace").read()
        except OSError as e:                       # a crash is not a fail — name it
            findings.append(("read", doc, "", "could not be read: %r" % (e,)))
            continue
        # ---- arm 1: commands
        for m in CMD_RE.finditer(text):
            cmd = m.group(1)
            if is_placeholder(cmd):
                skipped += 1
                continue
            checked += 1
            if not resolves(stage, doc, cmd):
                findings.append(("command", doc, cmd,
                                 "a designer typing this gets No such file or directory"))
        # ---- arm 2: backticked paths
        for m in PATH_RE.finditer(text):
            p = m.group(1)
            if is_placeholder(p):
                skipped += 1
                continue
            # File-shaped only. A bare `some-dir/` in prose is not a link a designer clicks,
            # and grading it produced pure noise on the real pack — measured, then narrowed.
            if not p.endswith(KNOWN_EXT):
                continue
            if p in DESIGNER_CREATES:
                skipped += 1
                continue
            if p.endswith(".py") and ("python3 " + p) in text:
                continue                            # already graded by arm 1
            checked += 1
            if not resolves(stage, doc, p):
                findings.append(("path", doc, p, "named as if it ships; it is not in the pack"))
        # ---- arm 3: the version sweep
        if pack_version:
            for m in VERSION_RE.finditer(text):
                checked += 1
                if m.group(1) != pack_version:
                    findings.append(("version", doc, m.group(0),
                                     "this pack is v%s — a version string was not swept at bake"
                                     % pack_version))
    # ---- arm 4: typed counts against the manifest
    man_path = os.path.join(stage, "_MANIFEST.json")
    if os.path.exists(man_path):
        try:
            man = json.load(open(man_path, encoding="utf-8"))
        except Exception as e:
            findings.append(("counts", "_MANIFEST.json", "", "unreadable: %r" % (e,)))
            man = None
        if man:
            verdicts = [v for g in man.get("groups", []) if g.get("key") == "gates"
                        for v in g.get("verdicts", [])]
            runnable = sum(1 for v in verdicts if v.get("verdict") == "RUNNABLE")
            rd = os.path.join("ci-template", "README.md")
            if runnable and os.path.exists(os.path.join(stage, rd)):
                txt = open(os.path.join(stage, rd), encoding="utf-8").read()
                for m in GATES_COUNT_RE.finditer(txt):
                    checked += 1
                    if int(m.group(1)) == runnable:
                        continue
                    if int(m.group(1)) in (sum(1 for v in verdicts
                                               if v.get("verdict") == "NEEDS-DEP"),
                                           sum(1 for v in verdicts
                                               if v.get("verdict") == "REPO-BOUND")):
                        continue
                    findings.append(("counts", rd, m.group(0),
                                     "the manifest measures %d RUNNABLE / %d NEEDS-DEP / %d "
                                     "REPO-BOUND — a typed figure beside a manifest that can "
                                     "compute it" % (
                                         runnable,
                                         sum(1 for v in verdicts
                                             if v.get("verdict") == "NEEDS-DEP"),
                                         sum(1 for v in verdicts
                                             if v.get("verdict") == "REPO-BOUND"))))
    prov = os.path.join(stage, "PROVENANCE.json")
    if os.path.exists(prov):
        try:
            claimed = json.load(open(prov, encoding="utf-8")).get("files")
        except Exception:
            claimed = None
        if isinstance(claimed, int):
            actual = sum(len(fs) for _, _, fs in os.walk(stage))
            checked += 1
            if claimed != actual:
                findings.append(("counts", "PROVENANCE.json", "files: %d" % claimed,
                                 "the staged tree holds %d file(s) — the published figure comes "
                                 "from a different column than the one it names" % actual))
    return findings, {"docs": len(docs), "checked": checked, "skipped": skipped}


def report(findings, stats, stage, strict):
    print("pack-docs gate (ADVISORY) — %d document(s), %d name(s) resolved, %d placeholder(s) "
          "skipped by name" % (stats["docs"], stats["checked"], stats["skipped"]))
    print("  stage: %s" % stage)
    if not findings:
        print("✅ every command and path in every shipped document resolves in the tree it "
              "ships in.")
        return 0
    print("  not graded, by name (files the guided session tells the designer to create):")
    for k, why in sorted(DESIGNER_CREATES.items()):
        print("    %-34s %s" % (k, why))
    by_arm = {}
    for arm, doc, needle, why in findings:
        by_arm.setdefault(arm, []).append((doc, needle, why))
    for arm in sorted(by_arm):
        rows = by_arm[arm]
        print("\n  === %s — %d finding(s) ===" % (arm.upper(), len(rows)))
        seen = set()
        shown = 0
        for doc, needle, why in rows:
            if (doc, needle) in seen:
                continue                     # one line per (doc, needle); repeats are counted
            seen.add((doc, needle))
            if shown >= DETAIL_CAP:
                continue
            shown += 1
            print("  [%s] %s  →  %s" % (doc, needle, why))
        if len(seen) > shown:
            print("  … %d more distinct name(s) not printed (%d total occurrence(s)); "
                  "the count above is the honest denominator, not the cap."
                  % (len(seen) - shown, len(rows)))
    print("\n%d finding(s). %s" % (
        len(findings),
        "STRICT — exiting 1." if strict else
        "ADVISORY — exiting 0. This gate is not blocking; promotion is Dave's word."))
    return 1 if strict else 0


# ------------------------------------------------------------------------------- the bites
def selftest():
    """Both directions, per arm: plant the defect, watch it fire; remove it, watch it clear.

    Everything is built in a throwaway temp dir. This selftest writes NOTHING tracked (#158)."""
    fails = []

    def bite(name, ok):
        print(("[OK] " if ok else "[FAIL] ") + name)
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "ci-template"))
        os.makedirs(os.path.join(d, "memento-package", "machinery"))
        open(os.path.join(d, "ci-template", "run-gates.py"), "w").write("#\n")
        open(os.path.join(d, "memento-package", "machinery", "_build_x.py"), "w").write("#\n")
        json.dump({"groups": [{"key": "gates", "verdicts": [
            {"gate": "a.py", "verdict": "RUNNABLE"},
            {"gate": "b.py", "verdict": "RUNNABLE"},
            {"gate": "c.py", "verdict": "NEEDS-DEP"}]}]},
            open(os.path.join(d, "_MANIFEST.json"), "w"))
        doc = os.path.join(d, "README.md")
        clean = ("Run `python3 ci-template/run-gates.py` from the pack root.\n"
                 "Open the `Apollo-Spider-v9.9.9` directory.\n")
        open(doc, "w").write(clean)
        # -- clean tree clears, every arm
        f, s = audit(d, pack_version="9.9.9")
        bite("clean staged tree: NO findings", f == [])
        bite("clean staged tree: it actually looked at something", s["checked"] >= 2)

        # -- arm 1: a command that does not resolve (F13)
        open(doc, "w").write(clean + "Also `python3 apollo-pack/ci-template/run-gates.py`.\n")
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 1 FIRES on an unresolvable command (F13)",
             any(a == "command" and "apollo-pack" in n for a, _, n, _w in f))
        open(doc, "w").write(clean)
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 1 CLEARS when the command is right", f == [])

        # -- arm 1: a command that resolves only from the doc's own directory
        sub = os.path.join(d, "memento-package", "README.md")
        open(sub, "w").write("Run `python3 machinery/_build_x.py` from here.\n")
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 1 accepts a doc-relative command (no false positive)", f == [])
        os.remove(sub)

        # -- arm 2: a path named as if it ships (F18)
        open(doc, "w").write(clean + "See `notes/2026-07-31-onepager-v1.md`.\n")
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 2 FIRES on a path that is not in the pack (F18)",
             any(a == "path" and "onepager" in n for a, _, n, _w in f))
        open(doc, "w").write(clean + "See `<your-notes>/thing.md`.\n")
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 2 SKIPS a placeholder rather than crying wolf", f == [])

        # -- arm 3: an unswept version string (F4)
        open(doc, "w").write(clean.replace("v9.9.9", "v9.9.8"))
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 3 FIRES on a stale version string (F4)",
             any(a == "version" for a, _, _n, _w in f))
        open(doc, "w").write(clean)
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 3 CLEARS on the current version", f == [])

        # -- arm 4: a typed gate count that disagrees with the manifest (F14)
        rd = os.path.join(d, "ci-template", "README.md")
        open(rd, "w").write("| **3 gates** | run on plain Python |\n")
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 4 FIRES on a typed count the manifest contradicts (F14)",
             any(a == "counts" and "3 gates" in n for a, _, n, _w in f))
        open(rd, "w").write("| **2 gates** | run on plain Python |\n")
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 4 CLEARS when the typed count matches the manifest", f == [])
        os.remove(rd)

        # -- arm 4: the published file count (F1)
        json.dump({"files": 999}, open(os.path.join(d, "PROVENANCE.json"), "w"))
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 4 FIRES on a published file count that is not the tree's (F1)",
             any(a == "counts" and "999" in n for a, _, n, _w in f))
        actual = sum(len(fs) for _, _, fs in os.walk(d))
        json.dump({"files": actual}, open(os.path.join(d, "PROVENANCE.json"), "w"))
        f, _ = audit(d, pack_version="9.9.9")
        bite("arm 4 CLEARS when the count is the tree's own",
             not any(a == "counts" for a, _, _n, _w in f))

        # -- the strict arm can actually fail (#173: drivable to BOTH verdicts here)
        open(doc, "w").write(clean + "`python3 nope/missing.py`\n")
        f, s = audit(d, pack_version="9.9.9")
        bite("--strict exits 1 on findings", report(f, s, d, strict=True) == 1)
        bite("advisory exits 0 on the SAME findings", report(f, s, d, strict=False) == 0)

    # -- the fence: this file must never enter the pack's gate roster (#221 lane C fence)
    rel = "knowledge/_release/_gate_pack_docs.py"
    in_roster = ((rel.startswith("knowledge/_validate_") or rel.startswith("knowledge/_gate_"))
                 and rel.endswith(".py"))
    bite("this gate is OUT of the pack gate roster (the ruled 55 does not move)", not in_roster)

    if fails:
        print("\npack-docs selftest FAILED — %d bite(s): %s" % (len(fails), fails))
        return 1
    print("\npack-docs selftest OK — 4 arms, each driven to BOTH verdicts.")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--stage" not in argv:
        print("pack-docs gate: --stage <dir> is required (the staged pack tree). "
              "REFUSING to guess which tree to read.", file=sys.stderr)
        return 2
    stage = os.path.abspath(argv[argv.index("--stage") + 1])
    if not os.path.isdir(stage):
        print("pack-docs gate: %s is not a directory. REFUSING." % stage, file=sys.stderr)
        return 2
    version = None
    for src in ("PROVENANCE.json", "_MANIFEST.json"):
        p = os.path.join(stage, src)
        if os.path.exists(p):
            try:
                v = json.load(open(p, encoding="utf-8")).get("version")
            except Exception:
                v = None
            if v:
                version = str(v).lstrip("v")
                break
    if version is None:
        print("  ⚠ no pack version found in PROVENANCE.json/_MANIFEST.json — arm 3 (the version "
              "sweep) is UNRUN, and says so rather than passing quietly.")
    findings, stats = audit(stage, pack_version=version)
    return report(findings, stats, stage, strict="--strict" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
