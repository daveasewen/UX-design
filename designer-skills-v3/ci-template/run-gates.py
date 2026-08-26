#!/usr/bin/env python3
"""Run the Apollo pack's gates and report three verdicts: pass, FAIL, COULD-NOT-ASK.

This is the runner the CI template calls. You can also run it by hand:

    python3 apollo-pack/ci-template/run-gates.py
    python3 apollo-pack/ci-template/run-gates.py --browser   # the playwright ones
    python3 apollo-pack/ci-template/run-gates.py --list

WHICH GATES RUN. The pack ships `_MANIFEST.json`, and every gate in it carries a verdict that
was MEASURED by running it outside the design system's own repo:

    RUNNABLE   it ran and produced a verdict — these run by default
    NEEDS-DEP  it needs something installed (playwright) — these run with --browser
    REPO-BOUND it only makes sense inside the design system's own repo — these do not ship

THE THREE VERDICTS. A gate exits 0 when it passes and 1 when it finds something. It exits 77
with a line starting `COULD-NOT-ASK:` when it cannot reach something it needs — a missing
browser, a file you have not created yet. That is a refusal, not a failure: it is printed in
full and counted separately, and it does not fail the build. A gate that FAILS does.

A BASELINE, IF YOU NEED ONE. Some gates may already be red on the day you adopt the pack —
existing debt in the design system or in your project. `--write-baseline` records exactly which
gates are red today; `--baseline` then fails the build only on gates that were NOT red then. It
is a ratchet, not a mute: every baselined gate is still run and still printed, the file is in
your repo where a reviewer can see it, and a gate that starts passing should be taken out of it.
"""
import argparse
import json
import os
import subprocess
import sys

COULD_NOT_ASK = 77
MARKER = "COULD-NOT-ASK:"


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
            out.append((v["gate"], path))
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
            out.append((os.path.basename(p), p))
    return out


def run_one(path, cwd, pack, timeout):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(pack, "knowledge") + os.pathsep + env.get("PYTHONPATH", "")
    try:
        r = subprocess.run([sys.executable, path], cwd=cwd, env=env,
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

    print("Apollo gates — %d to run, from %s" % (len(gates), source))
    print("pack: %s" % pack)
    if a.list:
        for name, _ in gates:
            print("  " + name)
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
    for name, path in gates:
        rc, out = run_one(path, cwd, pack, a.timeout)
        if rc == 0:
            passed.append(name)
            print("  pass          %s" % name)
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
    if old_fail:
        print("  (%d of those failures are in the baseline and do not fail the build: %s)"
              % (len(old_fail), ", ".join(old_fail)))
    if refused:
        print("\nRefusals in full — each one names what it could not reach:")
        for name, reason in refused:
            print("  %s\n    %s" % (name, reason))
    if failed:
        print("\nFailures:")
        for name, tail in failed:
            print("\n  === %s%s ===" % (name, " (in the baseline)" if name in known_red else ""))
            for line in tail:
                print("  " + line)
    return 1 if new_fail else 0


if __name__ == "__main__":
    sys.exit(main())
