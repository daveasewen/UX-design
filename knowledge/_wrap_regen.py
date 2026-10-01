#!/usr/bin/env python3
"""_wrap_regen.py — the regen serial, run ONCE, in its fixed order, then every `--check`.

Built #306 lane W1 for `s306-D4` phase 1 (Dave, 2026-09-28 16:58 BST, "go on both"; the design
page's proof for this phase is "rebuilds from 5 to 1"; ★ #307, by addition: the target is 1 PER COMMIT,
because the 5b follow-up's line lands in the ⏱ delta `_CHAIN.md` slices, so its own rebuild is intended). It replaces the per-lane `regen.sh`
(#306 T, U, V) and the #303–#305 wrap seats' hand-typed serials (`_regen.log`, `_regen-2.log`,
`_regen-3.log`, `_regen-5b.log`, `_regen-checks.log` at #305: five rebuilds in one wrap).

★ #307 (2026-09-28, by addition — Dave's 19:58 "fix the two phase-1 gaps the #306 wrap did by hand"):
step 0 below, `_gen_titles.py --session N` (runbook step 4b), was listed under this tool in the
runbook's PHASE 1 table but was NOT in the serial, so the #306 wrap ran it by hand after the gate
failed TITLE GENERATION. It is now step 0, and `--session N` is REQUIRED for `--run` and
`--checks-only` (a run without it is refused before anything writes). Its own `--check` only proves
the two titles still derive; the verdict also reads `knowledge/_gen_titles_receipt.json` and calls
it STALE unless the receipt was written for session N.

THE ORDER, and why each position (the record: `_HANDOFF-156` § THINGS A COLD SEAT SHOULD KNOW,
`notes/_lanes/306/U/regen.sh`, `notes/_subreports/2026-09-27-304-W5c-node-titles.md` § 2):
  0. knowledge/_gen_titles.py --session N — the two titles + knowledge/_gen_titles_receipt.json
                                             (step 4b); reads only GOOD-MORNING.md's banner and
                                             residual line, so it runs after the banner is placed
                                             (this tool runs after the last edit) and nothing reads it
  1. knowledge/_render_rulings.py          — notes/_RULINGS.html from _rulings.json (step 4d)
  2. knowledge/tokens/_build_blast_radius.py — knowledge/tokens/_blast-radius.json, knowledge/_GRAPH-REPORT.md
  3. knowledge/_build_memento_index.py     — the retrieval index (step 2g: after every GM/LS edit)
  4. knowledge/_build_graph_mention_map.py — reads the index's records
  5. knowledge/gen_kg_titles.py --write    — titles for new rulings; MISSING from T's serial on
                                             #306 and CI went red on it (fe243c6c, step [88])
  6. knowledge/_gen_chain.py               — _CHAIN.md, sliced from GM/LS as they now stand
  7. knowledge/_gen_schematic.py           — reads knowledge/_graph-mark-observations.jsonl
  8. knowledge/gen_dashboard.py            — reads the session number out of _CHAIN.md (its own
                                             docstring), so it runs AFTER 6. T and U ran it first,
                                             which is safe mid-session and stale at a wrap.
Then the `--check` of every one of the nine. A write step that fails STOPS the serial (the later
steps read its output); every check runs and each verdict is printed.
★ #312 (phase 3, `s306-D4`, by addition): one CHECK-ONLY step after the nine — `_wrap_views.py --check`, the
freshness arm (limit 7 of `s306-D10`): it regenerates the NEWEST wrap's views from its STORY.md + FACTS.json
and compares them with disk, red on any hand edit; a newest wrap with no STORY.md (the phase-1 path) is a
declared skip, not a red. It writes nothing, so it is not in the serial's write half.

⚠ `_memento_search.py` APPENDS to `knowledge/_graph-mark-observations.jsonl`, and the schematic
reads it, so the two must be committed together or CI's schematic determinism step goes red
(#305 C1). This tool says whether that file differs from HEAD, and lists every output that does,
so the commit's paths file can take them (`--paths-out FILE` appends them, one per line).

Usage (a BARE run prints the plan and runs nothing — the serial writes, so it is asked for by name):
  python3 knowledge/_wrap_regen.py --run --session N [--log FILE] [--paths-out FILE]   # the serial, then the checks
  python3 knowledge/_wrap_regen.py --checks-only --session N                            # the nine --checks alone
  python3 knowledge/_wrap_regen.py [--dry-run]                              # print the plan, run nothing
  python3 knowledge/_wrap_regen.py --selftest                         # fake steps in a temp dir
"""
import argparse
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# check-only steps run after the serial's checks (phase 3, #312): (script, check-args)
EXTRA_CHECKS = [
    ("knowledge/_wrap_views.py", ["--check"]),
]

# (script, write-args, check-args, outputs it writes)
SERIAL = [
    ("knowledge/_gen_titles.py", ["--session", "{N}"], ["--session", "{N}", "--check"], ["knowledge/_gen_titles_receipt.json"]),
    ("knowledge/_render_rulings.py", [], ["--check"], ["notes/_RULINGS.html"]),
    ("knowledge/tokens/_build_blast_radius.py", [], ["--check"], ["knowledge/tokens/_blast-radius.json", "knowledge/_GRAPH-REPORT.md"]),
    # s312-D1: the index is gitignored and BUILT, never committed — it still runs here (later steps
    # read it) but names no output to stage; staging an ignored path is refused by git.
    ("knowledge/_build_memento_index.py", [], ["--check"], []),
    ("knowledge/_build_graph_mention_map.py", [], ["--check"], ["knowledge/_graph-mention-map.json"]),
    ("knowledge/gen_kg_titles.py", ["--write"], ["--check"], ["knowledge/_node_titles.json"]),
    ("knowledge/_gen_chain.py", [], ["--check"], ["_CHAIN.md"]),
    ("knowledge/_gen_schematic.py", [], ["--check"], ["reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html"]),
    ("knowledge/gen_dashboard.py", [], ["--check"], ["dashboard/index.html"]),
]
OBSERVATIONS = "knowledge/_graph-mark-observations.jsonl"
TITLES_RECEIPT = "knowledge/_gen_titles_receipt.json"
SESSION_TOKEN = "{N}"


def _needs_session(serial):
    return any(SESSION_TOKEN in a for s in serial for a in list(s[1]) + list(s[2]))


def _bind(args, session):
    return [str(session) if a == SESSION_TOKEN else a for a in args]


def _receipt_stale(repo, session):
    """None when the titles receipt was written for `session`; otherwise the named reason."""
    import json
    path = os.path.join(repo, TITLES_RECEIPT)
    try:
        got = json.load(open(path, encoding="utf-8"))["meta"]["declared_session"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        return f"{TITLES_RECEIPT} unreadable ({type(e).__name__})"
    return None if got == session else f"{TITLES_RECEIPT} is #{got}, not #{session}"


def _order_ok(serial):
    """The positions the record fixes. Returns a list of named violations (empty = fine)."""
    names = [s[0].rsplit("/", 1)[-1] for s in serial]
    bad = []
    need = ["_gen_titles.py", "_render_rulings.py", "_build_blast_radius.py", "_build_memento_index.py",
            "_build_graph_mention_map.py", "gen_kg_titles.py", "_gen_chain.py", "_gen_schematic.py"]
    pos = [names.index(n) if n in names else -1 for n in need]
    if -1 in pos:
        bad.append("missing: " + ", ".join(n for n, p in zip(need, pos) if p < 0))
    elif pos != sorted(pos):
        bad.append("order broken: " + " → ".join(names))
    if "gen_dashboard.py" in names and "_gen_chain.py" in names and names.index("gen_dashboard.py") < names.index("_gen_chain.py"):
        bad.append("gen_dashboard.py runs before _gen_chain.py (it reads the session number out of _CHAIN.md)")
    kg = [s for s in serial if s[0].endswith("gen_kg_titles.py")]
    if kg and kg[0][1] != ["--write"]:
        bad.append("gen_kg_titles.py must run with --write (its bare form is a dry run)")
    gt = [s for s in serial if s[0].endswith("_gen_titles.py")]
    if gt and (gt[0][1] != ["--session", SESSION_TOKEN] or "--check" in gt[0][1]):
        bad.append("_gen_titles.py must run with --session N and without --check (--check writes no receipt)")
    return bad


def _changed(repo, path):
    """True / False against HEAD; None when git cannot say."""
    tracked = subprocess.run(["git", "--no-optional-locks", "ls-files", "--error-unmatch", path], cwd=repo,
                             capture_output=True).returncode == 0
    if not tracked:
        return os.path.exists(os.path.join(repo, path))
    r = subprocess.run(["git", "--no-optional-locks", "diff", "--quiet", "HEAD", "--", path], cwd=repo)
    return None if r.returncode not in (0, 1) else r.returncode == 1


def _run(repo, argv, log):
    t = time.time()
    p = subprocess.run([sys.executable] + argv, cwd=repo, capture_output=True, text=True,
                       env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1"})
    tail = next((l for l in reversed((p.stdout + p.stderr).splitlines()) if l.strip()), "")[:220]
    line = f"{' '.join(argv)} rc={p.returncode} ({time.time() - t:.0f}s) :: {tail.strip()}"
    print(line, flush=True)
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return p.returncode


def run(repo=REPO, serial=SERIAL, log=None, checks_only=False, paths_out=None, session=None, extra_checks=None):
    bad = _order_ok(serial)
    if bad and serial is SERIAL:
        print("⛔ REFUSED — the serial's order is broken:", "; ".join(bad), flush=True); return 2
    if _needs_session(serial) and session is None:
        print("⛔ REFUSED — --session N is required (step 0, _gen_titles.py, titles session N); nothing ran",
              flush=True); return 2
    if log:
        open(log, "w").close()
    rc_all = 0
    if not checks_only:
        print("--- serial (writes)")
        for script, wargs, _, _ in serial:
            if _run(repo, [script] + _bind(wargs, session), log) != 0:
                print(f"⛔ the serial STOPPED at {script} — the later steps read its output"); return 1
    print("--- checks")
    stale = []
    for script, _, cargs, _ in serial:
        if _run(repo, [script] + _bind(cargs, session), log) != 0:
            stale.append(script); rc_all = 1
    extras = EXTRA_CHECKS if (extra_checks is None and serial is SERIAL) else (extra_checks or [])
    for script, cargs in extras:
        if _run(repo, [script] + _bind(cargs, session), log) != 0:
            stale.append(script + " (check-only)"); rc_all = 1
    if any(s[0].endswith("_gen_titles.py") for s in serial) and session is not None:
        why = _receipt_stale(repo, session)
        if why:
            stale.append(f"_gen_titles.py ({why})"); rc_all = 1
    outs = [o for s in serial for o in s[3]] + [OBSERVATIONS]
    moved = [o for o in outs if _changed(repo, o)]
    obs = _changed(repo, OBSERVATIONS)
    print(f"--- verdict: {len(serial) - len(stale)} of {len(serial)} checks fresh"
          + (f"; STALE: {', '.join(stale)}" if stale else ""))
    print(f"--- differs from HEAD ({len(moved)}): " + (", ".join(moved) if moved else "none"))
    print(f"--- {OBSERVATIONS}: " + ("CHANGED vs HEAD — commit it WITH the schematic" if obs
                                    else "unchanged vs HEAD" if obs is False else "UNKNOWN (git could not say)"))
    if paths_out and moved:
        with open(paths_out, "a", encoding="utf-8") as f:
            f.write("".join(m + "\n" for m in moved))
        print(f"--- appended {len(moved)} path(s) to {paths_out}")
    return rc_all


def selftest():
    ok = True

    def bite(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok = ok and bool(cond)

    bite("the real serial's order holds (8 fixed positions, titles --write, dashboard after the chain)",
         _order_ok(SERIAL) == [])
    bite("gen_kg_titles.py is in the serial (the #306 CI red)", any(s[0].endswith("gen_kg_titles.py") for s in SERIAL))
    bite("_gen_titles.py --session N is in the serial (the #306 wrap ran it by hand)",
         any(s[0].endswith("_gen_titles.py") and s[1] == ["--session", SESSION_TOKEN] for s in SERIAL))
    notitles = [s for s in SERIAL if not s[0].endswith("_gen_titles.py")]
    bite("a serial without _gen_titles.py is named missing", any("missing: _gen_titles.py" in b for b in _order_ok(notitles)))
    nosess = [(s[0], [] if s[0].endswith("_gen_titles.py") else s[1], s[2], s[3]) for s in SERIAL]
    bite("_gen_titles.py without --session is named", any("_gen_titles.py must run" in b for b in _order_ok(nosess)))
    bite("the real serial REFUSES without --session, before anything writes", run(serial=SERIAL, session=None) == 2)
    swapped = list(SERIAL); swapped[5], swapped[6] = swapped[6], swapped[5]
    bite("a swapped pair is named as an order break", any("order broken" in b for b in _order_ok(swapped)))
    dropped = [s for s in SERIAL if not s[0].endswith("gen_kg_titles.py")]
    bite("a dropped member is named", any("missing: gen_kg_titles.py" in b for b in _order_ok(dropped)))
    early = [SERIAL[-1]] + SERIAL[:-1]
    bite("the dashboard before the chain is named", any("gen_dashboard" in b for b in _order_ok(early)))
    nowrite = [(s[0], [] if s[0].endswith("gen_kg_titles.py") else s[1], s[2], s[3]) for s in SERIAL]
    bite("titles without --write is named", any("--write" in b for b in _order_ok(nowrite)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init", "-q", td], check=True)
        mk = lambda n, body: open(os.path.join(td, n), "w").write(body)
        mk("a.py", "import sys,os\nif '--check' in sys.argv: sys.exit(0 if os.path.exists('A') else 1)\nopen('A','w').write('a')\nprint('wrote A')\n")
        mk("b.py", "import sys,os\nif '--check' in sys.argv: sys.exit(1)\nopen('B','w').write(open('A').read()+'b')\n")
        mk("c.py", "import sys\nsys.exit(3)\n")
        mk("d.py", "import sys\nopen('D','w').write('d')\n")
        fake = [("a.py", [], ["--check"], ["A"]), ("b.py", [], ["--check"], ["B"])]
        log = os.path.join(td, "log.txt")
        rc = run(td, fake, log=log)
        bite("fake serial runs in order (b read a's output) and a stale check sets rc 1",
             rc == 1 and open(os.path.join(td, "B")).read() == "ab")
        bite("the log has one line per run (2 writes + 2 checks)", len(open(log).read().splitlines()) == 4)
        rc = run(td, [("c.py", [], ["--check"], []), ("d.py", [], ["--check"], ["D"])])
        bite("a failing write STOPS the serial (d never ran)", rc == 1 and not os.path.exists(os.path.join(td, "D")))
        mk("e.py", "import sys\nopen('E','w').write(' '.join(sys.argv[1:]))\n")
        tok = [("e.py", ["--session", SESSION_TOKEN], ["--session", SESSION_TOKEN], ["E"])]
        bite("a {N} serial without a session is REFUSED and runs nothing",
             run(td, tok) == 2 and not os.path.exists(os.path.join(td, "E")))
        run(td, tok, session=307)
        bite("{N} is bound to the session number", open(os.path.join(td, "E")).read() == "--session 307")
        os.makedirs(os.path.join(td, "knowledge"))
        mk(TITLES_RECEIPT, '{"meta": {"declared_session": 306}}')
        bite("a titles receipt for another session is named STALE", "#306, not #307" in (_receipt_stale(td, 307) or ""))
        bite("a titles receipt for this session passes", _receipt_stale(td, 306) is None)
    print("wrap-regen selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true", help="run the serial (writes), then every --check")
    ap.add_argument("--checks-only", action="store_true")
    ap.add_argument("--log"); ap.add_argument("--paths-out")
    ap.add_argument("--session", type=int, help="the session being wrapped; REQUIRED with --run / --checks-only (step 0 titles it)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.dry_run or not (a.run or a.checks_only):
        bad = _order_ok(SERIAL)
        for i, (s, w, c, o) in enumerate(SERIAL):
            print(f"{i}. python3 {s} {' '.join(w)}".rstrip() + f"   → {', '.join(o)}   check: {' '.join(c)}")
        for s, c in EXTRA_CHECKS:
            print(f"+. python3 {s} {' '.join(c)}   (check-only, writes nothing — phase 3 freshness arm)")
        print("order:", "OK" if not bad else "; ".join(bad))
        return 0 if not bad else 2
    return run(log=a.log, checks_only=a.checks_only, paths_out=a.paths_out, session=a.session)


if __name__ == "__main__":
    sys.exit(main())
