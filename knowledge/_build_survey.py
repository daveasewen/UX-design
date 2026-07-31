#!/usr/bin/env python3
"""_build_survey.py — the FULL failure set in one pass, instead of the first failure only.

★ WHY THIS EXISTS (Dave, #61: *"we are circling the problem and never getting anywhere"*).
`_build_all.py` aborts on the first failing step (`:299-301`, the catch-all branch). That is
correct for a build — you do not want step 40 running on step 8's broken output — but it makes
the tool's control flow dictate the METHOD. Discovery becomes serial: fix step 8, learn about
step 10, fix step 10, learn about step N. Each round costs a session, and no session ever sees
how deep the hole is. #61 burned a window going 8 → 10 and still could not tell Dave whether
two steps were broken or twenty.

⇒ This does not build anything. It ASKS EVERY GATING STEP INDEPENDENTLY and reports all of
them, so the next session starts with the whole list instead of the next item.

⛔ SAFETY — THE REASON THIS IS NOT JUST `_build_all.py --keep-going`. A build step REGENERATES
derived files, and an aborted build leaves the tree PARTIALLY regenerated: at #61 that gutted
33 `knowledge/compliance/**` files, and the reconcile waved them through as "just derived
output" (restored `d7cd152`). So by DEFAULT this runs ONLY steps whose arguments are
`--selftest` / `--check` — the ones that assert without writing. Mutating steps are LISTED and
SKIPPED, never silently omitted: you can see exactly what was not asked.
`--include-mutating` exists, requires a dirty-tree refusal to pass first, and should be run on
a clean tree you are willing to `git checkout`.

⚠ A SKIPPED STEP IS NOT A PASSING STEP. The summary counts them separately and the exit code
ignores them. A survey that let "not asked" blend into "fine" would be the confident-blank
class this repo refuses everywhere else.

Usage:
    python3 knowledge/_build_survey.py                 # non-mutating steps only (safe)
    python3 knowledge/_build_survey.py --include-mutating   # everything (needs clean tree)
    python3 knowledge/_build_survey.py --timeout 30    # per-step seconds (default 25)
    python3 knowledge/_build_survey.py --range 1:20    # steps 1..20 only (1-based, inclusive)

⚠ WHY --range EXISTS (#62): the sandbox kills any foreground call at ~45s and NOTHING
survives a call boundary, so a full mutating pass cannot fit one call — #47's build died at
step 73 by exactly this wall. Chunks run in STEPS order across calls; the TREE persists
between calls, so consecutive ranges reproduce the serial build. Out-of-range steps are
counted in their own bucket, never blended into "not asked (mutating)".
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Args that make a step ASSERT rather than WRITE. Anything not on this list is treated as
# mutating — fail safe, never fail open. ⚠ Add to this list only after reading the step's
# source and confirming it writes nothing; a wrong entry here gets a tree gutted.
NON_MUTATING = {"--selftest", "--check"}


def steps():
    """`(label, script, args)` for every entry in `_build_all.STEPS`, or refuse with a reason.

    ⛔ READS THE STEPS WITH `ast`, AND MUST NEVER `import _build_all`. The first cut of this
    imported it — reasoning, correctly in the abstract, that a second parser is a second source
    of truth (the one-slicer argument `chain_parts` is built on). **`_build_all.py` has ZERO
    `__name__ == "__main__"` guards: importing it RUNS THE WHOLE BUILD.** So the safer-looking
    choice executed the exact thing this module exists to avoid executing, and gutted 33
    `knowledge/compliance/**` files a second time in one session — after I had already written
    the warning about it into two commit messages.
    ★ The lesson is not "check for a main guard". It is that **`import` is not a read.** A
    survey tool whose act of looking changes the thing surveyed is not an instrument.
    ⚠ `ast.literal_eval` is not used either — the entries contain module-level names in some
    positions; `ast.parse` + structural walk reads the literals without evaluating anything.
    """
    path = os.path.join(HERE, "_build_all.py")
    if not os.path.exists(path):
        return None, "_build_all.py is missing — survey NOT run, not assumed empty"
    import ast
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except SyntaxError as e:
        return None, f"_build_all.py does not parse ({e}) — survey REFUSES, it does not guess"

    raw = None
    for node in tree.body:                       # module level only — STEPS is a top-level name
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "STEPS" for t in node.targets):
            raw = node.value
    if raw is None or not isinstance(raw, (ast.List, ast.Tuple)):
        return None, ("no module-level `STEPS` list found in _build_all.py — the survey has "
                      "nothing to ask. A REFUSAL, not a clean bill of health: reporting "
                      "'0 failures' because 0 steps were found is worse than no survey at all.")

    def lit(n):
        return n.value if isinstance(n, ast.Constant) else None

    out, unreadable = [], 0
    for entry in raw.elts:
        if not isinstance(entry, (ast.Tuple, ast.List)) or len(entry.elts) < 2:
            unreadable += 1
            continue
        label, script = lit(entry.elts[0]), lit(entry.elts[1])
        if not isinstance(label, str) or not isinstance(script, str):
            unreadable += 1
            continue
        args = []
        if len(entry.elts) > 2 and isinstance(entry.elts[2], (ast.List, ast.Tuple)):
            args = [a for a in (lit(x) for x in entry.elts[2].elts) if isinstance(a, str)]
        out.append((label, script, args))
    if not out:
        return None, "STEPS parsed to zero readable entries — REFUSING rather than reporting green"
    how = f"{len(out)} steps read from _build_all.STEPS by ast (never imported)"
    if unreadable:
        # ⚠ DECLARED, never swallowed: a step this parser could not read is a step nobody asked.
        how += f" · ⚠ {unreadable} entr(ies) UNREADABLE and therefore NOT surveyed"
    return out, how


def main():
    include_mut = "--include-mutating" in sys.argv
    timeout = 25
    if "--timeout" in sys.argv:
        try:
            timeout = int(sys.argv[sys.argv.index("--timeout") + 1])
        except Exception:
            print("✗ --timeout needs an integer"); return 2
    rng = None
    if "--range" in sys.argv:
        try:
            a, b = sys.argv[sys.argv.index("--range") + 1].split(":")
            rng = (int(a), int(b))
            if rng[0] > rng[1] or rng[0] < 1:
                raise ValueError
        except Exception:
            print("✗ --range needs A:B, 1-based step indices, inclusive, A<=B"); return 2

    all_steps, how = steps()
    if all_steps is None:
        print(f"✗ survey REFUSED — {how}"); return 2
    print(f"— {how} · per-step timeout {timeout}s · "
          f"{'ALL steps (mutating included)' if include_mut else 'non-mutating steps only'}\n")

    if include_mut:
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        if dirty and "--resume" in sys.argv:
            # ★ #62: a chunked mutating pass is MID-BUILD dirty BY DESIGN — the build is
            # non-atomic (step 1 rewrites compliance wholesale; verification{} and
            # external_automatable_refs{} are rebuilt by LATER steps — _build_all.py's own
            # docstring, lines 5-21). --resume continues over exactly that state. It PRINTS
            # the dirt it resumes over, so damage attribution keeps its baseline: the last
            # commit, never this intermediate state.
            print("⚠ --resume: proceeding over a dirty tree. The dirt below must be the PRIOR\n"
                  "  chunk's regeneration — if you cannot name why every path is dirty, STOP.\n"
                  "  (#61's 'gutted' state IS this state: stripped-not-yet-re-enriched, healed\n"
                  "  only by a COMPLETE pass over the remaining steps.)")
            for p in dirty.splitlines():
                print(f"    {p}")
        elif dirty:
            print("✗ REFUSING --include-mutating on a dirty tree. Mutating steps rewrite derived\n"
                  "  files; if they abort you cannot tell your own edits from the damage. Commit\n"
                  "  or stash first. (#61: an aborted build gutted 33 compliance files and the\n"
                  "  reconcile waved them through as 'just derived output'.)\n"
                  "  Continuing a CHUNKED --range pass whose dirt is the prior chunk's own\n"
                  "  regeneration? That is what --resume is for — it declares the dirt it\n"
                  "  resumes over instead of blessing it.")
            return 2

    failed, passed, skipped, errored = [], [], [], []
    outside = 0
    for i, (label, script, args) in enumerate(all_steps, 1):
        if rng and not (rng[0] <= i <= rng[1]):
            outside += 1; continue
        mutating = not (args and all(a in NON_MUTATING for a in args))
        if mutating and not include_mut:
            skipped.append((i, label, script, args)); continue
        path = os.path.join(HERE, script)
        if not os.path.exists(path):
            errored.append((i, label, script, "script MISSING")); continue
        try:
            r = subprocess.run([sys.executable, path] + args, cwd=ROOT,
                               capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            errored.append((i, label, script, f"TIMEOUT >{timeout}s — not a verdict"))
            print(f"  ⏱ [{i:>2}] {label[:62]}"); continue
        if r.returncode == 0:
            passed.append((i, label)); print(f"  ✅ [{i:>2}] {label[:62]}")
        else:
            # First meaningful failure line — QUOTED, never summarised into a count.
            lines = [l for l in (r.stdout + r.stderr).splitlines()
                     if any(m in l for m in ("✗", "❌", "FAIL", "Error", "Traceback"))]
            failed.append((i, label, script, args, r.returncode,
                           lines[0].strip()[:150] if lines else "(no ✗/FAIL line — see full output)"))
            print(f"  ❌ [{i:>2}] {label[:62]}  exit {r.returncode}")

    print("\n" + "=" * 78)
    print(f"SURVEY: {len(passed)} pass · {len(failed)} FAIL · {len(errored)} could-not-ask · "
          f"{len(skipped)} not asked (mutating)"
          + (f" · {outside} outside --range {rng[0]}:{rng[1]} (not asked)" if rng else ""))
    print("⚠ 'not asked' is NOT 'passing' — it is excluded from the exit code, deliberately.")
    if rng:
        print("⚠ A RANGED SURVEY IS A PARTIAL VERDICT: only a full pass over all steps, or "
              "consecutive ranges covering them, says anything about the build.")
    if failed:
        print(f"\nTHE FULL FAILURE SET ({len(failed)}) — this is the number no single "
              f"`_build_all.py` run can tell you:")
        for i, label, script, args, rc, first in failed:
            print(f"\n  [{i}] {label}")
            print(f"      python3 knowledge/{script} {' '.join(args)}   (exit {rc})")
            print(f"      {first}")
    if errored:
        print(f"\nCOULD NOT ASK ({len(errored)}) — a refusal, not a verdict in either direction:")
        for i, label, script, why in errored:
            print(f"  [{i}] {label} — {why}")
    if skipped and not include_mut:
        print(f"\nNOT ASKED ({len(skipped)} mutating steps) — run --include-mutating on a clean "
              f"tree to include them:")
        for i, label, script, args in skipped[:8]:
            print(f"  [{i}] {label[:66]}")
        if len(skipped) > 8:
            print(f"  … and {len(skipped) - 8} more")
    return 1 if (failed or errored) else 0


if __name__ == "__main__":
    sys.exit(main())
