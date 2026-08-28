#!/usr/bin/env python3
"""_gate_artefact_fresh.py — ⬛ ADVISORY AT BIRTH (#221). The committed report vs a fresh run.

⛔ THE FALSE GREEN THIS EXISTS FOR (#220-L1 finding 7, measured, not argued). Some gates in this
repo do not ASSERT about an artefact — they REWRITE one. `_validate_a11y.py` produces
`_A11Y-GATE.md`; `_validate_advisory.py` produces `_ADVISORY-SIGNALS.md`; and so on. Every one of
them exits 0 while doing it, so the fleet reads them as passing. But:

  * they carry **no `--check` arm**, so `_build_survey.py` — whose `NON_MUTATING` set is
    `{--selftest, --check}` — cannot ask them and correctly LISTS them instead;
  * `_build_all.py` regenerates them and then **never compares**;
  * `.github/workflows/gates.yml` has **no `git diff --exit-code`** after the build, so CI
    writes fresh copies of these reports and throws them away.

⇒ Nothing in the repo could say whether a published gate report still describes the tree. L1
measured all five stale at `707e5aa` — 654→664 a11y notes, 123→130 advisory signals, 26 changed
theme-provenance rows, 19→21 integrity warnings, one missing instrument-fit row — with a
discrimination control beside it (four other writer-gates produced byte-identical output), so
the method separates stale from fresh rather than reporting churn.

⬛ ADVISORY, AND PROMOTION IS DAVE'S. Advisory-at-birth matches the house pattern
(`_gate_minted_consumption.py`, `_validate_hidden_display.py`); blocking would match the 16
generator `--check`s that already gate determinism. #220-L1's ruling-shaped question 3 puts the
choice to him and recommends advisory until it has been green for a session. This file does not
decide it: `--check` prints its findings and exits 0 unless `--strict` is passed, and nothing in
the tree passes `--strict`.

⚠ HOW IT MEASURES, STATED PLAINLY BECAUSE IT TOUCHES TRACKED FILES. There is no way to ask a
script with no `--check` arm what it WOULD write without letting it write. So each row is:
snapshot the artefact's bytes → run the script → compare → **restore the snapshot in a `finally`**.
The tree is byte-identical either side, and the run prints the md5 before and after so a reader
can verify that claim rather than take it. A crash between the run and the restore would leave a
FRESH artefact on disk, which `git status` shows and which is the safe direction to fail in; it is
declared here rather than hidden.

⚠ ITS POPULATION IS A DECLARED TABLE, NOT A DISCOVERY, AND THAT IS A LIMITATION NOT A DESIGN.
Two static scans were run over `knowledge/` while building this: a narrow one (`open(..., "w")`
with a resolvable constant) found 15 scripts and MISSED four of L1's five; a broad one (any write
call plus any tracked artefact name in the source) found 44 and includes obvious false positives.
A static reading of who writes what is unreliable in BOTH directions
[[unmatched-grep-is-not-an-absence]], so the table below is the empirically-measured set and
`--discover` reports what the table does not cover, as a TODO rather than a verdict.

Usage:
    python3 knowledge/_gate_artefact_fresh.py --check       # advisory: report drift, exit 0
    python3 knowledge/_gate_artefact_fresh.py --check --strict   # exit 1 on drift (nothing wires this)
    python3 knowledge/_gate_artefact_fresh.py --discover    # candidates not in the table
    python3 knowledge/_gate_artefact_fresh.py --selftest    # known-answer test, both directions
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
# ⛔ #158 WRITE-BY-DEFAULT, NO-ARGS LEG — and this gate needs it MORE than most, not less.
# To ask "would a fresh run differ?" of a script with no `--check` arm, this one must let that
# script write and then restore the bytes. A bare invocation would therefore rewrite five
# tracked reports on somebody's behalf without them having stated any intention at all. The
# restore makes that safe; it does not make it legitimate. Refuse the bare run.
from _helpgate import write_gate as _write_gate  # noqa: E402 - after the path walk, by necessity
_write_gate(__file__, writes="(transiently) knowledge/_A11Y-GATE.md, _ADVISORY-SIGNALS.md, "
                             "_THEME-PROVENANCE-GATE.md, _INTEGRITY-REPORT.md, _INSTRUMENT-FIT.md "
                             "+ .json, _RADIUS-GATE.md, _NO-HARDCODE-GATE.md — each restored")
import glob
import hashlib
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity

HERE = os.path.dirname(os.path.abspath(__file__))

# (script, argv, [artefacts it rewrites], why it is here)
# The five are #220-L1 finding 7's measured set; the last two are #221's own repairs, added
# because a gate this lane just changed is exactly the kind whose report goes quietly stale.
ROWS = [
    ("_validate_a11y.py", [], ["_A11Y-GATE.md"],
     "L1: 654 -> 664 notes, 1300 -> 1310 controls at 707e5aa"),
    ("_validate_advisory.py", [], ["_ADVISORY-SIGNALS.md"],
     "L1: 123 -> 130 signals"),
    ("_validate_theme_provenance.py", [], ["_THEME-PROVENANCE-GATE.md"],
     "L1: 26 rows changed"),
    ("_build_integrity.py", [], ["_INTEGRITY-REPORT.md"],
     "L1: 19 -> 21 warnings, 1030 -> 1035 leaf tokens, 41 -> 42 groups; imports jsonschema"),
    ("_build_instrument_fit.py", [], ["_INSTRUMENT-FIT.md", "_instrument-fit.json"],
     "L1: adds the missing _validate_hidden_display.py row"),
    ("_validate_radius.py", [], ["_RADIUS-GATE.md"],
     "#221 repaired its grammar; its report is published and nothing compared it"),
    ("_validate_no_hardcode.py", [], ["_NO-HARDCODE-GATE.md"],
     "#221 repaired its reader; same reason"),
]

# Scripts a static scan flags as writers that this table deliberately does NOT cover, each with
# the reason. A row here is a claim that can rot, so `--discover` re-checks the list every run.
NOT_COVERED = {
    "_build_memento_index.py": "has its own --check arm, wired as a step; already asked",
    "_gen_chain.py": "has --check, wired, and refuses on tier (#183/#193)",
    "_validate_kg.py": "the static scan matched `_rulings.json` as a READ, not a write",
    "_validate_state_contrast.py": "browser-bound; its artefact is written only in the render job",
}


def md5(path):
    if not os.path.exists(path):
        return None
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def summarise(before, after):
    """A one-line, human-readable delta. Counts, never a diff dump."""
    if before is None:
        return "artefact did not exist before the run"
    b, a = before.decode("utf-8", "replace").splitlines(), after.decode("utf-8", "replace").splitlines()
    added = [x for x in a if x not in b][:3]
    gone = [x for x in b if x not in a][:3]
    bits = ["%d line(s) -> %d" % (len(b), len(a))]
    for x in gone:
        bits.append("- " + x.strip()[:90])
    for x in added:
        bits.append("+ " + x.strip()[:90])
    return " | ".join(bits)


def compare_row(script, argv, artefacts):
    """-> (verdict, detail). Snapshot, run, compare, RESTORE. Never leaves the tree dirty."""
    paths = [os.path.join(HERE, a) for a in artefacts]
    missing = [a for a, p in zip(artefacts, paths) if not os.path.exists(p)]
    if missing:
        return "COULD-NOT-ASK", "artefact(s) not on disk: %s" % ", ".join(missing)
    snapshot = {p: open(p, "rb").read() for p in paths}
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, script)] + argv,
                           capture_output=True, text=True, timeout=300, cwd=HERE)
        out = (r.stdout + r.stderr)
        if cna.is_refusal(r.returncode):
            return "COULD-NOT-ASK", "the writer itself refused: " + out.strip().splitlines()[0][:160]
        if "ModuleNotFoundError" in out or "ImportError" in out:
            return "COULD-NOT-ASK", "a dependency is not importable here: " + \
                   next((l for l in out.splitlines() if "Error" in l), "")[:160]
        drifted = []
        for p in paths:
            fresh = open(p, "rb").read()
            if fresh != snapshot[p]:
                drifted.append("%s: %s" % (os.path.basename(p), summarise(snapshot[p], fresh)))
        if drifted:
            return "STALE", " ;; ".join(drifted)
        return "FRESH", "byte-identical (%d artefact(s))" % len(paths)
    except subprocess.TimeoutExpired:
        return "COULD-NOT-ASK", "the writer timed out at 300s"
    finally:
        # ⛔ THE RESTORE IS NOT OPTIONAL AND NOT CONDITIONAL. Every path this function can leave
        # by goes through here, including the exception paths.
        for p, blob in snapshot.items():
            if md5(p) != hashlib.md5(blob).hexdigest():
                open(p, "wb").write(blob)


def discover():
    """Candidate writer-gates the table does not name. A TODO list, never a verdict."""
    tracked = set(subprocess.run(["git", "ls-files"], cwd=os.path.dirname(HERE),
                                 capture_output=True, text=True).stdout.split())
    covered = {r[0] for r in ROWS} | set(NOT_COVERED)
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "_validate_*.py")) +
                    glob.glob(os.path.join(HERE, "_gate_*.py")) +
                    glob.glob(os.path.join(HERE, "_build_*.py"))):
        name = os.path.basename(f)
        if name in covered:
            continue
        t = open(f, encoding="utf-8", errors="replace").read()
        if not re.search(r'\.write_text\(|open\([^)]*["\']w["\']', t):
            continue
        named = sorted({m.group(1) for m in re.finditer(r'"([A-Za-z0-9_.\-]+\.(?:md|json|html))"', t)
                        if "knowledge/" + m.group(1) in tracked})
        if named:
            out.append((name, named))
    return out


def check(strict=False):
    print("artefact-freshness comparer (⬛ ADVISORY at birth, #221) — %d declared row(s)" % len(ROWS))
    print("  method: snapshot -> run the writer -> compare -> RESTORE. The tree is byte-identical")
    print("  either side; the md5 line below is the receipt, not a promise.")
    tally = {"FRESH": 0, "STALE": 0, "COULD-NOT-ASK": 0}
    stale_rows = []
    for script, argv, artefacts, why in ROWS:
        before = {a: md5(os.path.join(HERE, a)) for a in artefacts}
        verdict, detail = compare_row(script, argv, artefacts)
        after = {a: md5(os.path.join(HERE, a)) for a in artefacts}
        restored = before == after
        tally[verdict] = tally.get(verdict, 0) + 1
        mark = {"FRESH": "✅", "STALE": "⚠", "COULD-NOT-ASK": "⬛"}[verdict]
        print("  %s %-34s %-14s %s" % (mark, script, verdict, detail[:150]))
        if not restored:
            print("     ⛔ RESTORE FAILED — the tracked artefact is NOT what it was. "
                  "before=%s after=%s. Restore it by hand before committing." % (before, after))
        if verdict == "STALE":
            stale_rows.append((script, artefacts, why))
    print("  tally: %d FRESH · %d STALE · %d COULD-NOT-ASK" %
          (tally["FRESH"], tally["STALE"], tally["COULD-NOT-ASK"]))
    if stale_rows:
        print("  ⚠ A STALE ROW IS A PUBLISHED REPORT THAT NO LONGER DESCRIBES THE TREE. It is not")
        print("    a build failure — the fix is to regenerate and commit the artefact, which is a")
        print("    REGENERATION and therefore obeys the ordered-serial rule (#210).")
        for script, artefacts, why in stale_rows:
            print("      · %s -> %s   [L1: %s]" % (script, ", ".join(artefacts), why))
    if strict and stale_rows:
        return 1
    if strict:
        return 0
    print("  ⬛ ADVISORY: exit 0 regardless of drift. Promotion to blocking is DAVE'S "
          "(#220-L1 ruling-shaped Q3).")
    return 0


def selftest():
    """Known-answer test, both directions, on a SYNTHETIC writer in a scratch dir."""
    fails = []
    d = tempfile.mkdtemp(prefix="artefact-fresh-selftest-")
    try:
        art = os.path.join(d, "_FIXTURE.md")
        writer = os.path.join(d, "_fixture_writer.py")
        open(art, "w").write("one\ntwo\n")

        # ① a writer that reproduces the artefact byte for byte must read FRESH
        open(writer, "w").write("open(%r,'w').write('one\\ntwo\\n')\n" % art)
        v, _ = _compare_at(writer, [], [art])
        if v != "FRESH":
            fails.append("a byte-identical writer read %r, wanted FRESH" % v)

        # ② the SAME artefact with a writer that produces something else must read STALE —
        #    one variable apart from ①, which is what makes ① a control and not a coincidence
        open(writer, "w").write("open(%r,'w').write('one\\ntwo\\nthree\\n')\n" % art)
        v, detail = _compare_at(writer, [], [art])
        if v != "STALE":
            fails.append("a drifting writer read %r, wanted STALE" % v)
        if "three" not in detail:
            fails.append("the STALE detail did not name the added line: %r" % detail)

        # ③ ⛔ THE CLAUSE THIS GATE LIVES OR DIES ON: after a STALE verdict the artefact on disk
        #    must be EXACTLY what it was. A comparer that leaves the tree dirty is worse than no
        #    comparer, because the next reader commits its output by accident.
        if open(art).read() != "one\ntwo\n":
            fails.append("RESTORE FAILED after a STALE verdict — the fixture was left rewritten")

        # ④ a writer that refuses (77) must read COULD-NOT-ASK, never STALE and never FRESH
        open(writer, "w").write("import sys; print('COULD-NOT-ASK: fixture'); sys.exit(77)\n")
        v, _ = _compare_at(writer, [], [art])
        if v != "COULD-NOT-ASK":
            fails.append("a refusing writer read %r, wanted COULD-NOT-ASK" % v)

        # ⑤ a missing artefact is a refusal, not a pass
        v, _ = _compare_at(writer, [], [os.path.join(d, "_NOPE.md")])
        if v != "COULD-NOT-ASK":
            fails.append("a missing artefact read %r, wanted COULD-NOT-ASK" % v)

        # ⑥ the real table must name real files — a row pointing at nothing would make every
        #    run a quiet COULD-NOT-ASK, which is the confident-blank shape this repo refuses
        for script, _argv, artefacts, _why in ROWS:
            if not os.path.exists(os.path.join(HERE, script)):
                fails.append("table row names a script that is not on disk: %s" % script)
            for a in artefacts:
                if not os.path.exists(os.path.join(HERE, a)):
                    fails.append("table row names an artefact that is not on disk: %s" % a)
    finally:
        for f in glob.glob(os.path.join(d, "*")):
            os.remove(f)
        os.rmdir(d)
    print("artefact-freshness selftest: 6 arm(s) · %d failure(s)" % len(fails))
    for f in fails:
        print("  ⛔ " + f)
    return 1 if fails else 0


def _compare_at(script_path, argv, artefacts):
    """`compare_row` against absolute paths, for the selftest's synthetic fixtures."""
    global HERE
    real = HERE
    HERE = os.path.dirname(script_path)
    try:
        return compare_row(os.path.basename(script_path), argv,
                           [os.path.basename(a) for a in artefacts])
    finally:
        HERE = real


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if "--discover" in sys.argv:
        rows = discover()
        print("discover — candidate writer-gates NOT in this gate's table (%d):" % len(rows))
        for name, arts in rows:
            print("  · %-34s names %s" % (name, ", ".join(arts[:4])))
        print("  ⚠ A CANDIDATE IS NOT A FINDING. This is a static reading and it is unreliable in")
        print("    both directions — it over-matches a file that merely NAMES an artefact, and it")
        print("    missed four of the five rows above when it was first run. Each candidate needs")
        print("    one empirical run before it earns a table row.")
        print("  deliberately not covered, with reasons:")
        for k, v in sorted(NOT_COVERED.items()):
            print("    · %-34s %s" % (k, v))
        return 0
    return check(strict="--strict" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
