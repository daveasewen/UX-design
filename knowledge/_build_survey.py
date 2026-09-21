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

★ #193 — THREE VERDICTS, NOT TWO. A step may PASS, FAIL, or REFUSE: exit 77 plus a
`COULD-NOT-ASK:` line (`_could_not_ask.py`) means the step could not reach an input HERE and
said so in its own words — a gitignored token cache, an uninstalled browser, an evidence file
outside the committed tree. Those are COUNTED and PRINTED IN FULL, and excluded from the exit
code, because a job that goes red for a fact about the RUNNER teaches its readers to ignore red.
⚠ The exclusion is only honest because the refusals are LOUD: a silent skip would be the defect,
not the fix. Real FAILs still fail, and a step that is MISSING or TIMED OUT still fails too —
nobody asked it and it never said why, which is not the same thing as a refusal.

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
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity

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

    failed, passed, skipped, errored, refused = [], [], [], [], []
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
        elif cna.is_refusal(r.returncode):
            # ★ #193 — THE THIRD VERDICT. The step did not pass and did not fail: it declared, in
            # its own words, that the input it needed is unreachable HERE (a gitignored token
            # cache, an uninstalled browser, an evidence file outside the committed tree). It is
            # COUNTED, PRINTED WITH ITS OWN REASON, and excluded from the exit code — a silent
            # skip would be the defect, not the fix [[measuring-tool-must-not-guess]].
            reason = cna.reason_in(r.stdout + r.stderr)
            refused.append((i, label, script, args, reason))
            print(f"  ⊘ [{i:>2}] {label[:62]}  COULD-NOT-ASK")
        else:
            # First meaningful failure line — QUOTED, never summarised into a count.
            lines = [l for l in (r.stdout + r.stderr).splitlines()
                     if any(m in l for m in ("✗", "❌", "FAIL", "Error", "Traceback"))]
            failed.append((i, label, script, args, r.returncode,
                           lines[0].strip()[:150] if lines else "(no ✗/FAIL line — see full output)"))
            print(f"  ❌ [{i:>2}] {label[:62]}  exit {r.returncode}")

    print("\n" + "=" * 78)
    print(f"SURVEY: {len(passed)} pass · {len(failed)} FAIL · {len(refused)} COULD-NOT-ASK "
          f"(self-declared refusals) · {len(errored)} unaskable (missing/timed out) · "
          f"{len(skipped)} not asked (mutating)"
          + (f" · {outside} outside --range {rng[0]}:{rng[1]} (not asked)" if rng else ""))
    print("⚠ 'not asked' is NOT 'passing' — it is excluded from the exit code, deliberately.")
    print("⚠ 'COULD-NOT-ASK' is NOT 'passing' either. It is a step that named the input it could\n"
          "  not reach, so the job does not go red for an ENVIRONMENT fact dressed as an artefact\n"
          "  verdict (#173/#183, generalised #193). Every one is printed in full below. A step\n"
          "  that timed out or is MISSING is a different thing and still fails: nobody asked it\n"
          "  and it never said why.")
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
    if refused:
        print(f"\nCOULD-NOT-ASK ({len(refused)}) — each step's OWN words about the input it could "
              f"not reach.\nThese do NOT fail the survey; they also do not pass. If one of them "
              f"is here because the\nenvironment is wrong rather than because the input is "
              f"genuinely unreachable, FIX THE ENVIRONMENT:")
        for i, label, script, args, reason in refused:
            print(f"\n  [{i}] {label}")
            print(f"      python3 knowledge/{script} {' '.join(args)}   (exit {cna.EXIT})")
            # ⚠ a refusal with no marked line is REPORTED AS SUCH, never given a manufactured
            # reason — the convention's whole point is that the gate says why, not the survey.
            no_words = ("(exit 77 but NO `COULD-NOT-ASK:` line — the step used the convention's "
                        "code without its words; see its full output)")
            print(f"      {reason or no_words}")
    if errored:
        print(f"\nUNASKABLE ({len(errored)}) — nobody asked these and they never said why "
              f"(missing script / timeout). Counted as failures:")
        for i, label, script, why in errored:
            print(f"  [{i}] {label} — {why}")
    if skipped and not include_mut:
        print(f"\nNOT ASKED ({len(skipped)} mutating steps) — run --include-mutating on a clean "
              f"tree to include them:")
        for i, label, script, args in skipped[:8]:
            print(f"  [{i}] {label[:66]}")
        if len(skipped) > 8:
            print(f"  … and {len(skipped) - 8} more")

    # ★ s294-D1 — THE RUN IS RECORDED, so the green count has a source of truth to be read from.
    if "--no-record" in sys.argv:
        print("\n⚠ --no-record: this run is NOT in the verdict ledger, so nothing downstream can "
              "quote it. The chain's green count keeps saying whatever the last recorded run said.")
    else:
        where, why = record_run(
            steps_on_disk=len(all_steps), rng=rng, timeout=timeout, include_mut=include_mut,
            passed=[i for i, _l in passed], failed=[r[0] for r in failed],
            refused=[r[0] for r in refused], errored=[r[0] for r in errored],
            skipped=[r[0] for r in skipped])
        print(f"\n— recorded → {where}" if where else
              f"\n⚠ NOT RECORDED — {why}. The run happened; the ledger does not know it, and "
              f"`_gen_chain.build_verdict_line()` will say the green count is NOT DERIVABLE "
              f"rather than invent one.")
    return 1 if (failed or errored) else 0


# =========================================================== s294-D1 — THE BUILD-VERDICT LEDGER
# ★ WHY THIS EXISTS (Dave, `s294-D1`, ruled #294 2026-09-21). The most-read sentence in the
# project — *"75 of 144 steps green (#62, `18c7789`)"* — derived its DENOMINATOR from
# `_build_all.py`'s AST and its NUMERATOR from a pinned sha, so the denominator moved on its own
# and the numerator did not: the sentence got quietly wronger every time the build grew.
# `s125-D1` already ruled this exact shape once, and its `watch` field forbids the helpful
# hand-correction BY NAME. So the numerator needed a SOURCE OF TRUTH, and there wasn't one:
# ⛔ MEASURED AT THIS SEAT 2026-09-21 — this module PRINTED its verdict and wrote nothing. No CI
# run record, no verdict ledger, nothing in the repo that a generator could read. A number can
# only be generated from a thing that exists, so the thing is built here, at the instrument that
# takes the reading, and NOT in the renderer that publishes it (one slicer, `s125-D1`'s (2)).
#
# ⚠ WHY INDICES AND NOT COUNTS. A full mutating pass cannot fit one call (#47 died at step 73;
# this module's own docstring says so), and at #294 a full NON-mutating pass did not fit either —
# measured: the host's call cap cut it off. So a verdict is assembled from CHUNKS, which means
# counts cannot be added (two chunks may overlap) — the STEP INDICES are recorded and unioned.
# ⚠ AND THE NEWEST RECORD WINS PER STEP, not per file: a step that failed in an early chunk and
# passes in a later one is GREEN, and the disagreement is COUNTED and PUBLISHED rather than
# smoothed, because a step whose verdict changed inside one sha is a fact about the runner.
LEDGER = os.path.join(ROOT, "notes", "_BUILD-VERDICT-LOG.jsonl")
_LEDGER_FIELDS = ("passed", "failed", "refused", "errored", "skipped")


def _head_sha():
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, timeout=20)
        if r.returncode == 0:
            return r.stdout.strip(), None
        return None, f"git rev-parse failed rc={r.returncode}"
    except (OSError, subprocess.SubprocessError) as e:
        return None, f"git unavailable ({e})"


def record_run(steps_on_disk, rng, timeout, include_mut, **buckets):
    """Append ONE record for this run. Returns `(path, None)` or `(None, why_not)`.

    ⚠ NEVER RAISES INTO THE SURVEY. The survey's verdict is the product; the ledger is a
    by-product, and a by-product that can abort the product is a worse instrument than no
    by-product at all. Every failure path returns a REASON, which `main()` prints.
    """
    import datetime
    import json
    sha, why = _head_sha()
    if sha is None:
        return None, f"the HEAD sha could not be read ({why}) — a verdict with no tree is not a verdict"
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    rec = {"at": datetime.datetime.now().isoformat(timespec="seconds"),
           "sha": sha, "dirty": bool(dirty), "steps_on_disk": steps_on_disk,
           "range": list(rng) if rng else None, "timeout": timeout,
           "include_mutating": bool(include_mut), "tool": "_build_survey.py"}
    rec.update({k: sorted(buckets.get(k, [])) for k in _LEDGER_FIELDS})
    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    except OSError as e:
        return None, f"the ledger could not be written ({e})"
    return LEDGER, None


def verdict_from_ledger(repo=ROOT, ledger=None):
    """`(verdict_dict, None)` for the newest recorded tree, or `(None, why_not)`.

    ⛔ REFUSES, NEVER GUESSES — the `s125-D1` posture, inherited deliberately. No file, no
    records, an unreadable record, a record with no steps: every one of them yields a NAMED
    reason that the chain PUBLISHES as an unmeasured gap. A declared gap passes; a silent one
    fails [[measuring-tool-must-not-guess]].
    """
    import json
    path = ledger or os.path.join(repo, "notes", "_BUILD-VERDICT-LOG.jsonl")
    if not os.path.exists(path):
        return None, (f"no verdict ledger at `{os.path.relpath(path, repo)}` — no surveyed run "
                      f"has ever been recorded in this tree")
    recs, malformed = [], 0
    try:
        with open(path, encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    r = json.loads(ln)
                except ValueError:
                    malformed += 1
                    continue
                if isinstance(r, dict) and r.get("sha") and r.get("steps_on_disk"):
                    recs.append(r)
                else:
                    malformed += 1
    except OSError as e:
        return None, f"the verdict ledger could not be read ({e})"
    if not recs:
        return None, (f"the verdict ledger has no readable record"
                      + (f" ({malformed} malformed line(s))" if malformed else ""))
    newest = recs[-1]
    same = [r for r in recs if r.get("sha") == newest["sha"]]
    # per-step verdict, newest record wins; conflicts COUNTED, never smoothed.
    verdict, conflicts = {}, 0
    for r in same:
        for bucket in _LEDGER_FIELDS:
            for i in r.get(bucket) or []:
                if i in verdict and verdict[i] != bucket:
                    conflicts += 1
                verdict[i] = bucket
    total = max(r.get("steps_on_disk") or 0 for r in same)
    counts = {b: sum(1 for v in verdict.values() if v == b) for b in _LEDGER_FIELDS}
    seen = set(verdict)
    return {
        "green": counts["passed"], "fail": counts["failed"], "refused": counts["refused"],
        "errored": counts["errored"], "skipped": counts["skipped"],
        "asked": counts["passed"] + counts["failed"] + counts["refused"] + counts["errored"],
        "total": total, "sha": newest["sha"], "at": newest.get("at", "?"),
        "dirty": any(r.get("dirty") for r in same), "records": len(same),
        "conflicts": conflicts, "malformed": malformed,
        "unseen": sorted(i for i in range(1, total + 1) if i not in seen),
        "partial": any(r.get("range") for r in same),
    }, None


def selftest():
    """Plant the defect, then detect it. The ledger is a NEW source of truth for the single
    most-read sentence in the project, so every refusal path is asserted, not assumed."""
    import json
    import tempfile
    fails, n = [], [0]

    def bite(name, ok):
        n[0] += 1
        if not ok:
            fails.append(f"[{name}]")

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "led.jsonl")
        # ---- refusal 1: no file. Never a number, never a zero.
        v, why = verdict_from_ledger(td, p)
        bite("an absent ledger REFUSES", v is None and "no surveyed run" in why)
        # ---- refusal 2: present but unreadable content.
        open(p, "w").write("{not json\n")
        v, why = verdict_from_ledger(td, p)
        bite("an unreadable ledger REFUSES rather than reporting 0 green",
             v is None and "no readable record" in why and "malformed" in why)
        # ---- the healthy path, in TWO CHUNKS, the way a real pass has to run.
        def rec(**kw):
            base = {"sha": "aaa1111", "steps_on_disk": 10, "at": "2026-09-21T10:00:00",
                    "dirty": False, "range": None}
            base.update(kw)
            return json.dumps(base) + "\n"
        with open(p, "w") as f:
            f.write(rec(range=[1, 5], passed=[1, 2, 3], failed=[4], skipped=[5]))
            f.write(rec(range=[6, 10], passed=[6, 7], refused=[8], errored=[9], skipped=[10]))
        v, why = verdict_from_ledger(td, p)
        bite("two chunks UNION into one verdict", v is not None and v["green"] == 5)
        bite("the buckets are not blended", v["fail"] == 1 and v["refused"] == 1
             and v["errored"] == 1 and v["skipped"] == 2)
        bite("asked EXCLUDES the skipped (not asked is not passing)", v["asked"] == 8)
        bite("a chunked pass is declared PARTIAL", v["partial"] is True)
        bite("nothing is unseen when the chunks cover the build", v["unseen"] == [])
        # ---- planted defect: a gap in the coverage must be VISIBLE, not counted as green.
        with open(p, "w") as f:
            f.write(rec(range=[1, 3], passed=[1, 2, 3]))
        v, _ = verdict_from_ledger(td, p)
        bite("an uncovered range is reported as UNSEEN, never as green",
             v["green"] == 3 and v["unseen"] == [4, 5, 6, 7, 8, 9, 10])
        # ---- planted defect: a verdict that CHANGED inside one sha is counted and published.
        with open(p, "w") as f:
            f.write(rec(failed=[1]))
            f.write(rec(passed=[1]))
        v, _ = verdict_from_ledger(td, p)
        bite("the newest record wins per step", v["green"] == 1 and v["fail"] == 0)
        bite("the disagreement is COUNTED, not smoothed", v["conflicts"] == 1)
        # ---- planted defect: an OLD tree's records must not be mixed into the newest verdict.
        with open(p, "w") as f:
            f.write(rec(sha="old0000", passed=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
            f.write(rec(sha="new1111", passed=[1]))
        v, _ = verdict_from_ledger(td, p)
        bite("records from an older sha are NOT unioned into the newest tree's verdict",
             v["green"] == 1 and v["sha"] == "new1111")
        # ---- the writer's round trip: what record_run writes, verdict_from_ledger reads.
        global LEDGER
        was, LEDGER = LEDGER, p
        try:
            os.remove(p)
            where, why = record_run(steps_on_disk=4, rng=None, timeout=25, include_mut=False,
                                    passed=[1, 2], failed=[3], skipped=[4])
            bite("record_run writes a record (or names why it could not)",
                 where is not None or why is not None)
            if where:
                v, _ = verdict_from_ledger(td, p)
                bite("the writer's record is readable by the reader (one format, one place)",
                     v is not None and v["green"] == 2 and v["total"] == 4)
                bite("a full pass is NOT flagged partial", v["partial"] is False)
            else:
                bite("the writer's record is readable by the reader (one format, one place)", False)
                bite("a full pass is NOT flagged partial", False)
        finally:
            LEDGER = was
    return fails, n[0]


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        fs, nb = selftest()
        print("\n".join(fs) if fs else f"_build_survey selftest: {nb} bites, all GREEN")
        sys.exit(1 if fs else 0)
    sys.exit(main())
