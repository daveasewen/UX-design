#!/usr/bin/env python3
"""#304 W3c — patch knowledge/_gen_chain.py: the verdict line's denominator is the AST's (as
the sentence already claims), a run of a different-sized build is DECLARED, and the step-count
bite compares the verdict line's own figure with disk (like with like). Idempotent: refuses if
any anchor is not found exactly once, no-ops if already applied."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "knowledge" / "_gen_chain.py"
src = p.read_text(encoding="utf-8")
if "#304 W3c" in src:
    print("already applied"); sys.exit(0)

def sub(old, new):
    global src
    n = src.count(old)
    if n != 1:
        sys.exit(f"anchor found {n}x, refusing: {old[:80]!r}")
    src = src.replace(old, new)

# ---- 1. the sentence
sub('''    unseen = (f" ⛔ **{len(v['unseen'])} step(s) are in NO record — never asked, never green.**"
              if v["unseen"] else "")
    conf = (f" ⚠ **{v['conflicts']} step(s) changed verdict inside one sha.**"
            if v.get("conflicts") else "")
    return (f"⛔ **BUILD VERDICT: {v['green']} of {v['total']} steps GREEN — {v['fail']} FAIL · "
            f"{v['refused']} COULD-NOT-ASK · {v['errored']} unaskable · "
            f"{v['total'] - v['asked']} NOT ASKED (mutating).**{dup} Green GENERATED from the run "
            f"ledger (`_build_survey.py` @ `{v['sha']}` {v['at'][:10]}{part}, `s294-D1`); total "
            f"from `_build_all.py`'s AST (`s125-D1`)."
            f"{stale}{dirty}{unseen}{conf}{sixty2}")''',
'''    # ★★ #304 W3c — THE DENOMINATOR IS `now`, THE AST'S, BECAUSE THE SENTENCE SAYS SO. Until
    # #304 it printed `v['total']` — the step count the RUN saw — beside the words "total from
    # `_build_all.py`'s AST". The two agree only until the build grows: R4b took STEPS 146 → 148,
    # the newest record still said 146, and the chain published "of 146 steps" while claiming the
    # AST as its source. A provenance the number does not have is a SILENT gap, and this module's
    # rule is that a declared gap passes and a silent one fails. ⇒ The total is the AST's, the
    # green/fail/refused counts stay the RUN's, and when the two builds differ in size the
    # difference is SAID, with the steps the run never saw counted into "in NO record".
    # ⛔ Measured cost of the old shape (CI `36275037261`): `[121]` red in the survey step, and
    # `[13]` red with it — `_capture_gate.py --selftest` calls `_gen_chain.selftest()` — and both
    # went green again the moment ANY survey appended a record at the new size, which is why
    # `[13]` read as a flake (V2: exit 1 once, 77 on three re-asks). It was an ORDERING
    # dependence on the ledger, not chance.
    run_n = v["total"]
    unseen_ix = list(v["unseen"]) + (list(range(run_n + 1, now + 1)) if now > run_n else [])
    if now == run_n:
        grown = ""
    elif now > run_n:
        _new = f"{run_n + 1}" if now == run_n + 1 else f"{run_n + 1}–{now}"
        grown = (f" ⚠ **that run surveyed {run_n} steps; {now} are on disk now — step(s) {_new} "
                 f"are newer than the run.**")
    else:
        grown = (f" ⚠ **that run surveyed {run_n} steps; {now} are on disk now — {run_n - now} "
                 f"step(s) have gone since, so the run's step numbers need not name today's "
                 f"steps.**")
    unseen = (f" ⛔ **{len(unseen_ix)} step(s) are in NO record — never asked, never green.**"
              if unseen_ix else "")
    conf = (f" ⚠ **{v['conflicts']} step(s) changed verdict inside one sha.**"
            if v.get("conflicts") else "")
    return (f"⛔ **BUILD VERDICT: {v['green']} of {now} steps GREEN — {v['fail']} FAIL · "
            f"{v['refused']} COULD-NOT-ASK · {v['errored']} unaskable · "
            f"{run_n - v['asked']} NOT ASKED (mutating).**{dup} Green GENERATED from the run "
            f"ledger (`_build_survey.py` @ `{v['sha']}` {v['at'][:10]}{part}, `s294-D1`); total "
            f"from `_build_all.py`'s AST (`s125-D1`)."
            f"{grown}{stale}{dirty}{unseen}{conf}{sixty2}")


# ★ #304 W3c — THE STEP FIGURE THE VERDICT LINE PUBLISHES, READ BACK OUT OF IT. The step-count
# bite used to ask whether `" 148 steps"` occurred ANYWHERE in the chain, so any other sentence
# carrying the number could satisfy it while the verdict line said something else. Like with
# like: this returns the denominator of every BUILD VERDICT sentence, and nothing else.
VERDICT_FIGURE_RE = re.compile(r"BUILD VERDICT: (?:\\d+ of )?(\\d+) steps")


def verdict_step_figures(text):
    """Every step figure published in a BUILD VERDICT sentence of `text`, as ints."""
    return [int(x) for x in VERDICT_FIGURE_RE.findall(text or "")]''')

# ---- 2. the step-count bite: like with like
sub('''            bite(f"BUILD-STEP FIGURE IS RE-DERIVED AND MATCHES DISK ({_n} steps, measured now)",
                 f" {_n} steps" in text or f"of {_n} steps" in text)''',
'''            _figs = verdict_step_figures(text)
            bite(f"BUILD-STEP FIGURE IS RE-DERIVED AND MATCHES DISK ({_n} steps, measured now)",
                 bool(_figs) and all(x == _n for x in _figs))
            # ★ #304 W3c — the bite above, MUTATED: the verdict sentence's own figure is moved
            # off disk while the true number stays elsewhere in the file. The old substring
            # check would still have found it; the like-with-like read must not.
            _bad = VERDICT_FIGURE_RE.sub(
                lambda m: m.group(0).replace(m.group(1), str(_n + 100)), text, count=1)
            bite("the plant planted — a verdict figure was moved off disk (else the next bite is "
                 "vacuous)", _bad != text and (_n + 100) in verdict_step_figures(_bad))
            bite("a WRONG verdict figure is CAUGHT even with the true count elsewhere in the file",
                 not all(x == _n for x in verdict_step_figures(_bad + f" {_n} steps ")))''')

# ---- 3. the stubbed-ledger arms: denominator is disk's; a different-sized run is DECLARED
sub('''            globals()["_verdict_from_ledger"] = lambda repo=ROOT: ({
                "green": 7, "fail": 2, "refused": 1, "errored": 0, "skipped": 3, "asked": 10,
                "total": 13, "sha": "dead123", "at": "2026-01-02T03:04:05", "dirty": False,
                "records": 1, "conflicts": 0, "malformed": 0, "unseen": [11, 12, 13],
                "partial": False}, None)
            _yes = build_verdict_line(ROOT)
            bite("with a record the GREEN COUNT IS THE RUN'S, not len(STEPS) at a pinned sha",
                 "7 of 13 steps GREEN" in _yes)''',
'''            # ★ #304 W3c — the stub is sized to the build ON DISK. Before #304 it said 13
            # against a 146-step build and asserted "7 of 13", i.e. that the denominator is the
            # RUN's — while the step-count bite above asserted it is DISK's. The two bites could
            # only both pass while run and disk agreed, which is how a build that grew went red.
            _sn = _n if _n else 13
            def _stub(total, unseen):
                return lambda repo=ROOT: ({
                    "green": 7, "fail": 2, "refused": 1, "errored": 0, "skipped": 3, "asked": 10,
                    "total": total, "sha": "dead123", "at": "2026-01-02T03:04:05",
                    "dirty": False, "records": 1, "conflicts": 0, "malformed": 0,
                    "unseen": unseen, "partial": False}, None)
            globals()["_verdict_from_ledger"] = _stub(_sn, [_sn - 2, _sn - 1, _sn])
            _yes = build_verdict_line(ROOT)
            bite("with a record the GREEN COUNT IS THE RUN'S, not len(STEPS) at a pinned sha",
                 f"7 of {_sn} steps GREEN" in _yes)
            bite("a run of the SAME-sized build declares no size difference (no false alarm)",
                 "that run surveyed" not in _yes)
            globals()["_verdict_from_ledger"] = _stub(_sn - 2, [])
            _grew = build_verdict_line(ROOT)
            bite("a run of a SMALLER build: the total is STILL disk's, never the run's",
                 f"7 of {_sn} steps GREEN" in _grew and verdict_step_figures(_grew) == [_sn])
            bite("…and the size difference is DECLARED, naming both counts",
                 f"that run surveyed {_sn - 2} steps; {_sn} are on disk now" in _grew)
            bite("…and the steps the run never saw are counted in NO record, never green",
                 "2 step(s) are in NO record" in _grew)
            globals()["_verdict_from_ledger"] = _stub(_sn + 3, [])
            _shrank = build_verdict_line(ROOT)
            bite("a run of a LARGER build: total is disk's and the vanished steps are DECLARED",
                 verdict_step_figures(_shrank) == [_sn]
                 and "3 step(s) have gone since" in _shrank)
            globals()["_verdict_from_ledger"] = _stub(_sn, [_sn - 2, _sn - 1, _sn])''')

p.write_text(src, encoding="utf-8")
print("patched", p)
