#!/usr/bin/env python3
"""Run the Apollo pack's gates and report three verdicts: pass, FAIL, COULD-NOT-ASK.

This is the runner the CI template calls. You can also run it by hand, from the pack root:

    python3 ci-template/run-gates.py
    python3 ci-template/run-gates.py --browser   # the playwright ones
    python3 ci-template/run-gates.py --list

WHICH GATES RUN. The pack ships `_MANIFEST.json`, and every gate in it carries a verdict that
was MEASURED by running it outside the design system's own repo:

    RUNNABLE   it ran and produced a verdict — these run by default
    NEEDS-DEP  it needs something installed (playwright) — these run with --browser
    REPO-BOUND it only makes sense inside the design system's own repo — these do not ship

THE THREE VERDICTS. A gate exits 0 when it passes and 1 when it finds something. It exits 77
with a line starting `COULD-NOT-ASK:` when it cannot reach something it needs — a missing
browser, a file you have not created yet. That is a refusal, not a failure: it is printed in
full and counted separately, and it does not fail the build. A gate that FAILS does.

PACK CONTEXT, AND WHY THE RUNNER STATES IT (#230 F6). This runner is used in two places that
look identical and are not: an INSTALLED PACK (`_MANIFEST.json` present, no `knowledge/
_build_all.py`) and the design system's OWN SOURCE REPO. Some gates grade the repo's build
wiring, which an installed pack simply does not have. Before this was said out loud, a pristine
pack ran the command the design contract itself ends on and printed `37 pass · 1 FAIL`, exit 1 —
23 correctly shipped gates reported as orphans because the gate reading `_build_all.STEPS` found
no such file and read the silence as "nothing runs them". Nothing was wrong with the pack.

The runner now names which context it is in, and a gate that REFUSES for a repo resource is
counted as could-not-ask and PRINTED IN FULL — never a silent pass, and never a FAIL about the
pack instead of about your work. A gate the manifest measured RUNNABLE that then refuses in a
pack is called out by name at the foot of the run: its verdict wants re-measuring at the next
cut, and saying so is the runner's job, not the reader's.

A BASELINE, IF YOU NEED ONE. Some gates may already be red on the day you adopt the pack —
existing debt in the design system or in your project. `--write-baseline` records exactly which
gates are red today; `--baseline` then fails the build only on gates that were NOT red then. It
is a ratchet, not a mute: every baselined gate is still run and still printed, the file is in
your repo where a reviewer can see it, and a gate that starts passing should be taken out of it.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys

COULD_NOT_ASK = 77
MARKER = "COULD-NOT-ASK:"

# ---------------------------------------------------------------- what a green actually graded
# ⛔ #221 (from #220's L4 audit, finding F11). `ci-template/README.md` promised a designer:
# "A green that graded nothing is not the same as a green that graded something, and the runner
# prints the difference." It did not. Every one of the 35 gates printed an identical bare `pass`,
# including the ones that grade YOUR work and have nothing to look at on day one — the runner
# captured each gate's output and threw it away. A documented consumer for a signal nobody
# emitted: [[instrument-without-a-consumer]], inverted.
#
# The runner does not compute a population. It cannot — only the gate knows what it globbed.
# What it does now is REPORT the gate's own closing line, and read a population out of it using
# the declared patterns below. When nothing parses, it says `population not stated` — never
# zero, never silence. A measuring tool must not guess.
#
# VERDICT WORDS ARE NOT POPULATIONS. `0 failure(s)` is a result; `0 tranche file(s)` is a
# population. Counting the first as the second would report every clean gate as having graded
# nothing, which is the same lie in the other direction.
NOT_A_POPULATION = ("fail", "failure", "error", "warning", "note", "violation", "signal",
                    "exception", "leak", "hex", "unknown", "hole", "miss", "defect", "red")
POP_RE = re.compile(r"(\d[\d,]*)\s+([a-z][a-z\- ]{0,24}?)\(s\)")
# Gates that say it in words instead of digits. Matched as a phrase, not inferred from a zero.
EMPTY_PHRASES = ("no tranche files found", "nothing to grade", "population of zero",
                 "no files to grade")


def population_of(output):
    """(figure, unit, closing_line) read out of a gate's OWN output. figure is None when the
    gate did not state one — which is a reading, not a zero."""
    lines = [l.strip() for l in (output or "").splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    low = last.lower()
    for phrase in EMPTY_PHRASES:
        if phrase in low:
            return 0, "file", last
    for m in POP_RE.finditer(last):
        unit = m.group(2).strip().rstrip("-").split()[-1] if m.group(2).strip() else ""
        if unit.lower() in NOT_A_POPULATION:
            continue
        return int(m.group(1).replace(",", "")), m.group(2).strip() or "item", last
    return None, None, last


def find_pack(start):
    """The pack is the directory that contains _MANIFEST.json. Look here, then upwards."""
    env = os.environ.get("APOLLO_PACK")
    if env:
        return os.path.abspath(env)
    d = os.path.abspath(start)
    for _ in range(6):
        if os.path.exists(os.path.join(d, "_MANIFEST.json")):
            return d
        d = os.path.dirname(d)
    return None


def pack_context(pack):
    """('pack'|'source-repo'|'unknown', one sentence saying how it was decided).

    ⛔ DECIDED ON WHAT IS REACHABLE, NEVER ON AN ENV VAR. `_could_not_ask.py`'s convention
    forbids keying behaviour on "am I in CI" for the reason that applies here too: it makes the
    reading a function of the runner's identity rather than of what the runner can see, and the
    first honest environment to set the variable gets the wrong answer. Two observable facts
    decide it — the manifest a bake writes, and the build orchestrator only the source repo has.
    """
    manifest = os.path.exists(os.path.join(pack, "_MANIFEST.json"))
    build_all = os.path.exists(os.path.join(pack, "knowledge", "_build_all.py"))
    if build_all:
        return "source-repo", ("knowledge/_build_all.py is here, so this is the design system's "
                               "own repo — repo-wiring gates can ask their question")
    if manifest:
        return "pack", ("_MANIFEST.json is here and knowledge/_build_all.py is not, so this is "
                        "an INSTALLED PACK. Gates that grade the source repo's build wiring "
                        "cannot ask their question here and will REFUSE (could-not-ask), which "
                        "is printed in full and is not a failure of your work.")
    return "unknown", ("neither _MANIFEST.json nor knowledge/_build_all.py is here — the runner "
                       "does not know which context this is and will not guess")


def gates_from_manifest(pack, want_browser):
    """Read the gate list and its measured verdicts out of the pack's own manifest."""
    with open(os.path.join(pack, "_MANIFEST.json"), encoding="utf-8") as f:
        man = json.load(f)
    group = [g for g in man["groups"] if g["key"] == "gates"]
    if not group:
        return []
    want = "NEEDS-DEP" if want_browser else "RUNNABLE"
    out = []
    for v in group[0].get("verdicts", []):
        if v["verdict"] != want:
            continue
        path = os.path.join(pack, "knowledge", v["gate"])
        if os.path.exists(path):
            # #219 N2 -> N1 handoff. A gate's ARGV is part of its measured verdict, not a
            # convention the runner is expected to know: the manifest records how the gate was
            # ACTUALLY invoked when its verdict was measured, and the runner replays exactly
            # that. Without this the pack calls `_validate_type_composites.py` bare and a
            # designer meets the design system's whole standing debt as if it were theirs.
            # Read as a string and split, so the manifest's schema does not move.
            out.append((v["gate"], path, shlex.split(v.get("invocation") or "")))
    return sorted(out)


def gates_by_glob(pack, want_browser):
    """Fallback for a pack with no manifest: every gate file, browser ones last."""
    import glob
    found = []
    for pattern in ("_validate_*.py", "_gate_*.py"):
        found += glob.glob(os.path.join(pack, "knowledge", pattern))
    out = []
    for p in sorted(found):
        text = open(p, encoding="utf-8", errors="replace").read()
        is_browser = "playwright" in text
        if is_browser == want_browser:
            # No manifest ⇒ no measured invocation. Bare is the honest default here: guessing
            # an argv for a gate nothing measured is how a runner invents a verdict.
            out.append((os.path.basename(p), p, []))
    return out


def run_one(path, cwd, pack, timeout, argv=()):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(pack, "knowledge") + os.pathsep + env.get("PYTHONPATH", "")
    try:
        r = subprocess.run([sys.executable, path] + list(argv), cwd=cwd, env=env,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        # A timeout never said why it failed, so it is a failure and not a refusal.
        return 1, "TIMED OUT after %ss" % timeout
    return r.returncode, (r.stdout + r.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--browser", action="store_true",
                    help="run the gates that need playwright instead of the rest")
    ap.add_argument("--list", action="store_true", help="print the gate list and stop")
    ap.add_argument("--timeout", type=int, default=120, help="per-gate seconds (default 120)")
    ap.add_argument("--pack", help="path to the unzipped pack (default: found automatically)")
    ap.add_argument("--baseline", help="a file from --write-baseline: only NEW failures fail")
    ap.add_argument("--write-baseline", help="record today's failures to this file and stop")
    a = ap.parse_args()

    pack = os.path.abspath(a.pack) if a.pack else find_pack(os.path.dirname(os.path.abspath(__file__)))
    if not pack or not os.path.isdir(os.path.join(pack, "knowledge")):
        print("Could not find the Apollo pack. Point at it with --pack <dir> or set "
              "APOLLO_PACK. The pack is the folder that holds knowledge/ and _MANIFEST.json.")
        return 2

    if os.path.exists(os.path.join(pack, "_MANIFEST.json")):
        gates = gates_from_manifest(pack, a.browser)
        source = "_MANIFEST.json"
    else:
        gates = gates_by_glob(pack, a.browser)
        source = "a file scan (no _MANIFEST.json in the pack)"

    context, why = pack_context(pack)
    print("Apollo gates — %d to run, from %s" % (len(gates), source))
    print("pack: %s" % pack)
    print("context: %s — %s" % (context.upper(), why))
    if a.list:
        for name, _, argv in gates:
            print("  " + name + ("  " + " ".join(argv) if argv else ""))
        return 0
    if not gates:
        print("Nothing to run. With --browser this is normal unless the pack ships "
              "browser-driven gates.")
        return 0

    known_red = set()
    if a.baseline:
        if os.path.exists(a.baseline):
            known_red = set(json.load(open(a.baseline, encoding="utf-8")).get("failing", []))
            print("baseline: %d gate(s) recorded as already failing — see %s"
                  % (len(known_red), a.baseline))
        else:
            print("baseline file %s does not exist; every failure counts" % a.baseline)

    cwd = os.getcwd()
    passed, failed, refused = [], [], []
    graded_nothing, unstated = [], []
    for name, path, argv in gates:
        rc, out = run_one(path, cwd, pack, a.timeout, argv)
        if rc == 0:
            passed.append(name)
            n, unit, last = population_of(out)
            if n == 0:
                graded_nothing.append(name)
                note = "graded NOTHING — 0 %s(s)" % (unit or "file")
            elif n is None:
                unstated.append(name)
                note = "population not stated"
            else:
                note = "graded %s %s(s)" % ("{:,}".format(n), unit)
            print("  pass          %-38s %s" % (name, note))
            if last:
                print("                %s" % last[:150])
        elif rc == COULD_NOT_ASK:
            reason = next((l.strip() for l in out.splitlines() if MARKER in l), MARKER)
            refused.append((name, reason))
            print("  could-not-ask %s" % name)
            print("                %s" % reason)
        else:
            failed.append((name, out.strip().splitlines()[-25:]))
            print("  FAIL (%d)      %s" % (rc, name))

    if a.write_baseline:
        with open(a.write_baseline, "w", encoding="utf-8") as f:
            json.dump({"failing": sorted(name for name, _ in failed),
                       "note": "Gates already failing when this baseline was written. Only "
                               "gates NOT listed here fail the build when --baseline is used. "
                               "This list should only ever get shorter."},
                      f, indent=2)
        print("\nwrote %s — %d gate(s) recorded as already failing"
              % (a.write_baseline, len(failed)))
        return 0

    new_fail = [(nm, tail) for nm, tail in failed if nm not in known_red]
    old_fail = [nm for nm, _ in failed if nm in known_red]
    print("\n%d pass · %d FAIL · %d could-not-ask" % (len(passed), len(failed), len(refused)))
    # THE DIFFERENCE THE README PROMISES. Printed even when it is zero-of-zero, because
    # "no gate graded nothing" is itself the reading a designer wants on the day they check.
    if graded_nothing:
        print("  ⚠ %d of those green(s) graded a population of ZERO — they have nothing to look "
              "at yet, which is not the same as finding nothing wrong: %s"
              % (len(graded_nothing), ", ".join(graded_nothing)))
    else:
        print("  (no green graded a population of zero)")
    if unstated:
        print("  (%d green(s) did not state a population; the runner does not invent one: %s)"
              % (len(unstated), ", ".join(unstated)))
    if old_fail:
        print("  (%d of those failures are in the baseline and do not fail the build: %s)"
              % (len(old_fail), ", ".join(old_fail)))
    if refused:
        print("\nRefusals in full — each one names what it could not reach:")
        for name, reason in refused:
            print("  %s\n    %s" % (name, reason))
    # #230 F6 — THE STALE-VERDICT CALLOUT. A gate the manifest MEASURED as RUNNABLE that then
    # refuses in a pack is not a mystery to leave for the reader: its shipped verdict is out of
    # date and the next `--manifest` probe will reclassify it REPO-BOUND (s223-D5/D6), at which
    # point it stops shipping. Saying so is what keeps this a scoped, DECLARED skip rather than a
    # silent one [[instrument-without-a-consumer]].
    if refused and context == "pack":
        declared = {}
        try:
            with open(os.path.join(pack, "_MANIFEST.json"), encoding="utf-8") as f:
                for g in json.load(f).get("groups", []):
                    for v in g.get("verdicts", []):
                        declared[v["gate"]] = v["verdict"]
        except (OSError, ValueError, KeyError):
            declared = {}
        stale = [n for n, _ in refused if declared.get(n) == "RUNNABLE"]
        if stale:
            print("\n  ⚠ %d gate(s) the manifest measured RUNNABLE refused in this pack: %s"
                  % (len(stale), ", ".join(stale)))
            print("    Their shipped verdict is stale, not their refusal. Each one is REPO-BOUND "
                  "here and wants re-measuring at the next cut. Your work was not graded by "
                  "them, and nothing above pretended it was.")
    if failed:
        print("\nFailures:")
        for name, tail in failed:
            print("\n  === %s%s ===" % (name, " (in the baseline)" if name in known_red else ""))
            for line in tail:
                print("  " + line)
    return 1 if new_fail else 0


if __name__ == "__main__":
    sys.exit(main())
