#!/usr/bin/env python3
"""THE TRIGGER INDEX READER — Dave's open item (e), built #81 2026-08-02.

⛔ THE DEFECT THIS EXISTS TO KILL, stated once so it is never re-derived a fourth time.

#54 (Dave) ruled the token unit: ONE unit, real Claude tokens, cl100k demoted to a labelled
estimator. That ruling is STORED IN TEN PLACES — `notes/_MEMENTO-DECISIONS.md:1716`,
`notes/_GAUGE-LOG.md:461`, `knowledge/_DS-IMPROVEMENTS.md:1422` and EIGHT `_DECISION-HISTORY`
dossiers. Twenty-six sessions later #80 re-measured the same ratio from scratch and nearly filed
it as a discovery. #81 started down the identical path and was stopped by Dave, not by the repo:

    "we've identified this as a problem already, again we are going round in circles"
    "we seem to have a knowledge transfer problem between sessions, isn't this being stored
     anywhere?"

★★ IT WAS STORED. STORAGE WAS NEVER THE PROBLEM. Every mechanism this project has for
remembering is WRITE-optimised, and every mechanism for READING is triggered by SUSPICION —
`_memento_search.py` answers what you ask, and you only ask about what you already suspect
exists. Searching the archive for this very topic at #81 returned THE CURRENT WEEK'S BANNERS,
because retrieval ranks recency above rulings ([[retrieval-default-hides-the-ruling]]).

⇒ SO THE TRIGGER IS NOT A SEARCH, AND MUST NOT BE. It is THE WORK ITSELF. `git diff --name-only`
already knows which files a session touched; `_rulings.json` knows which rulings govern them.
Touch a governed file and you are TOLD, whether or not it occurred to you to ask. That is the
whole mechanism and it is deliberately not clever — the clever version is a better search, and a
better search still has to be CALLED by someone who suspects.

★ THIS SHIPS WITH ITS READER, WHICH IS THE POINT OF IT. `_measure_tokenizer.py` was a correct,
re-runnable instrument with ZERO consumers for fourteen sessions, and its measurement decayed
into a rediscovery precisely because nothing re-read it ([[instrument-without-a-consumer]]).
An index nothing consults would be the same failure wearing this file's name. Hence: wired into
`_capture_gate.py`'s build AND its wrap, not offered as a command someone might remember.

USAGE
    python3 knowledge/_governs.py                    # rulings governing the working tree's diff
    python3 knowledge/_governs.py --since HEAD~3     # ... over a wider range
    python3 knowledge/_governs.py --file knowledge/_capture_gate.py
    python3 knowledge/_governs.py --symbol measure_tokens
    python3 knowledge/_governs.py --all
    python3 knowledge/_governs.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_rulings.json")


class IndexUnreadable(RuntimeError):
    """⚠ LOUD AND NAMED, never a silent empty list.

    An index that fails open is worse than no index: it reports "no rulings govern this" in the
    exact voice it would use if it had checked, which is the confident-false-inscription this
    whole project exists to prevent. A caller that cannot read the index must SAY SO.
    Same shape as `MeasurementRefused` (#79-D1) and adopted deliberately, not by coincidence.
    """


def load(path: str | None = None) -> list[dict]:
    # ⚠ RESOLVED AT CALL TIME, NOT IN THE SIGNATURE. `path: str = INDEX` binds the default when
    # this function is DEFINED, so reassigning `_governs.INDEX` afterwards silently kept reading
    # the old file — the module-level constant looked like the single source of truth and was
    # not. Found by mutation M4 at birth: the "index unreachable" mutation stayed GREEN because
    # the selftest could not actually reach the path it thought it was breaking. ★ Exactly the
    # class this repo keeps re-learning — a green that cannot fail is an assertion, and here the
    # assertion was hiding inside Python's default-argument semantics.
    path = path or INDEX
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError as e:
        raise IndexUnreadable(
            f"⛔ TRIGGER INDEX MISSING — {path} is not there ({e}). No ruling can be surfaced, "
            f"so a session is free to re-derive a settled decision. Restore it from git; do NOT "
            f"proceed on the assumption that nothing is governed.") from e
    except json.JSONDecodeError as e:
        raise IndexUnreadable(
            f"⛔ TRIGGER INDEX UNPARSEABLE — {path} is not valid JSON ({e}). Fix the file. An "
            f"unparseable index must never degrade to 'nothing is governed'.") from e
    rulings = data.get("rulings")
    if not isinstance(rulings, list) or not rulings:
        raise IndexUnreadable(
            f"⛔ TRIGGER INDEX EMPTY — {path} parsed but carries no `rulings` list. An empty "
            f"index and a healthy index with no match are indistinguishable to a caller, which "
            f"is exactly the silent-lookup class.")
    return rulings


def _norm(s: str) -> str:
    return s.strip().replace("\\", "/").lstrip("./").lower()


def matches(ruling: dict, targets: set[str]) -> bool:
    """A ruling governs a target if any `governs` entry matches a path (by suffix, so a
    repo-relative entry matches an absolute path) or a bare symbol name.

    ⚠ Suffix matching is deliberate and it is the loose direction on purpose: a MISSED ruling
    is the failure this file exists to prevent, and a spurious extra ruling costs three lines of
    reading. The asymmetry is the design, not sloppiness.
    """
    for g in ruling.get("governs", []):
        gn = _norm(g)
        for t in targets:
            if gn == t or t.endswith("/" + gn) or gn.endswith("/" + t):
                return True
            if "/" not in gn and gn in t.replace("/", " ").split():
                return True
    return False


def changed_files(since: str | None = None) -> list[str]:
    """Files the session has touched. THIS is the trigger — no one has to remember to ask."""
    cmds = ([["git", "diff", "--name-only", since]] if since else
            [["git", "diff", "--name-only"], ["git", "diff", "--name-only", "--cached"],
             ["git", "ls-files", "--others", "--exclude-standard"]])
    out: list[str] = []
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        if r.returncode == 0:
            out.extend(x for x in r.stdout.splitlines() if x.strip())
    return sorted(set(out))


def surface(targets: set[str], rulings: list[dict] | None = None) -> list[dict]:
    return [r for r in (rulings if rulings is not None else load()) if matches(r, targets)]


def render(hits: list[dict], because: str) -> str:
    if not hits:
        return ""
    lines = [f"⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING ({because}) — "
             f"{len(hits)} found. READ BEFORE RE-DERIVING:"]
    for r in hits:
        lines.append(f"  ▸ {r['id']} — RULED {r['ruled']} ({r['date']}, {r['by']}): {r['says']}")
        lines.append(f"      status: {r.get('status', 'unstated')}")
        if r.get("watch"):
            lines.append(f"      ⚠ {r['watch']}")
        for e in r.get("evidence", []):
            lines.append(f"      evidence: {e}")
    lines.append("  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is "
                 "Dave's alone.")
    return "\n".join(lines)


def selftest() -> list[str]:
    """Bites, each failing for a DISTINCT reason. A green that cannot fail is an assertion."""
    failures: list[str] = []
    rulings = load()

    # 1. POSITIVE CONTROL FIRST — a failure-only suite reads green after a revert that deletes
    #    the comparison entirely. Prove the index HITS before proving it misses.
    hit = surface({"knowledge/_capture_gate.py"}, rulings)
    if not hit:
        failures.append("_governs: `knowledge/_capture_gate.py` matched NO ruling — it is "
                        "governed by ds-021 at minimum; the matcher is dead")
    if not any(r["id"] == "ds-021" for r in hit):
        failures.append("_governs: _capture_gate.py did not surface ds-021 — the exact ruling "
                        "#80 re-derived and #81 started to re-derive again")

    # 2. THE SYMBOL PATH, which is the one that catches an edit inside an ungoverned-looking file
    if not any(r["id"] == "ds-021" for r in surface({"measure_tokens"}, rulings)):
        failures.append("_governs: the bare symbol `measure_tokens` surfaced no ruling — a "
                        "session editing it by name would be told nothing")

    # 3. THE NEGATIVE CONTROL. If everything matches everything, the index is decoration.
    if surface({"knowledge/_totally_unrelated_xyzzy.py"}, rulings):
        failures.append("_governs: an unrelated path matched a ruling — the matcher is too "
                        "loose to carry information")

    # 4. ⛔ THE FAIL-LOUD SEAM. An unreadable index must RAISE, never return []. This is the
    #    whole difference between this file and the search it replaces.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bad = os.path.join(td, "broken.json")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("{not json")
        try:
            load(bad)
            failures.append("_governs: an UNPARSEABLE index did not raise — it degraded to "
                            "'nothing is governed', which is the silent-lookup class this file "
                            "was built to end")
        except IndexUnreadable:
            pass
        except Exception as e:
            failures.append(f"_governs: unparseable index raised {type(e).__name__}, not "
                            f"IndexUnreadable — the failure must be NAMED or the caller reports "
                            f"'something went wrong' and the next session re-diagnoses it")
        empty = os.path.join(td, "empty.json")
        with open(empty, "w", encoding="utf-8") as fh:
            json.dump({"rulings": []}, fh)
        try:
            load(empty)
            failures.append("_governs: an EMPTY index did not raise — empty and no-match are "
                            "indistinguishable to a caller")
        except IndexUnreadable:
            pass
        missing = os.path.join(td, "nope.json")
        try:
            load(missing)
            failures.append("_governs: a MISSING index did not raise")
        except IndexUnreadable:
            pass

    # 5. Every entry carries what a reader needs. A pointer with no evidence is a second copy
    #    of canon waiting to happen.
    for r in rulings:
        for field in ("id", "ruled", "date", "by", "says", "governs", "evidence", "status"):
            if not r.get(field):
                failures.append(f"_governs: ruling {r.get('id', '?')!r} is missing `{field}` — "
                                f"an entry that cannot point a reader at canon IS canon, and "
                                f"this file must never become the eleventh copy")
        for e in r.get("evidence", []):
            # #119: `commit <sha>` is a LEGAL pointer form — verified against git, not the
            # filesystem. Before this, an honest commit pointer had no legal form here and
            # real hashes were reported as rot ([[honest-refusal-needs-a-legal-form]] class).
            if e.startswith("commit "):
                sha = e.split()[1]
                ok = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                                    cwd=REPO, capture_output=True).returncode == 0
                if not ok:
                    failures.append(f"_governs: ruling {r['id']} points at `{e}` which is not "
                                    f"a commit in this repo — a pointer index whose pointers "
                                    f"rot is worse than none")
                continue
            p = os.path.join(REPO, e.split(":")[0])
            if not os.path.exists(p):
                failures.append(f"_governs: ruling {r['id']} points at `{e}` which does not "
                                f"exist — a pointer index whose pointers rot is worse than none")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Which rulings govern what you are touching?")
    ap.add_argument("--since", help="git ref to diff against (default: working tree)")
    ap.add_argument("--file", action="append", default=[])
    ap.add_argument("--symbol", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        fs = selftest()
        print("\n".join(f"  FAIL {f}" for f in fs) if fs else
              "  _governs.py selftest: all bites green")
        return 1 if fs else 0

    try:
        rulings = load()
    except IndexUnreadable as e:
        print(str(e), file=sys.stderr)
        return 2

    if a.all:
        print(render(rulings, "--all"))
        return 0

    targets = {_norm(x) for x in (a.file + a.symbol)}
    because = "explicit"
    if not targets:
        files = changed_files(a.since)
        targets = {_norm(f) for f in files}
        because = f"{len(files)} file(s) touched" + (f" since {a.since}" if a.since else "")
        if not files:
            print("  no changed files — nothing to check")
            return 0

    hits = surface(targets, rulings)
    print(render(hits, because) if hits
          else f"  no ruling governs the {len(targets)} target(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
