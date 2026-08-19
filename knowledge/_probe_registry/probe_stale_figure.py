#!/usr/bin/env python3
"""probe_stale_figure.py — P-5: CARRIED FIGURES vs LIVE MEASUREMENT (W-45 probe registry).

THE CLASS, from the receipts: a number is measured once, written into a living document (or a
memory hook), and then CARRIED. The tree moves; the figure does not. #203 caught it three
times in one session on ONE figure — the type-composite debt was carried as **1,101** while
the gate measured **1,097**:
  · `notes/_receipts/2026-08-19-203-wave3-laneE-data-display.md:35` — "STALE — it is 1,097"
  · `notes/_receipts/2026-08-19-203-wave3-laneF-flow-load.md:38` — same, with the gate line
  · `notes/_receipts/2026-08-19-203-wave3-laneC-money-secure.md:205,274` — "re-stamp the debt"
and #173 flagged two stale INVENTORY documents on the same principle
(`knowledge/_REVIEW-SIGNOFF.md:271` — "~38 components, ~20 P1 gaps" against 75 snippets).
[[premise-ages-faster-than-rule]] · [[measure-dont-convert-units]]: a COUNT is not a
MEASUREMENT until something re-runs it.

WHAT THIS PROBE DOES: for each RULE below it (a) re-measures the figure LIVE, read-only, and
(b) greps the LIVING documents for a carried number of that figure's shape. A mismatch is a
finding, printed with file:line, the carried number and the live one.

⚠ THE GLOB IS THE WHOLE DESIGN. It covers LIVING documents only:
    knowledge/_LIVE-STATE.md · GOOD-MORNING.md · AGENTS.md · README.md · knowledge/README.md
Receipts, briefs and archives are DELIBERATELY EXCLUDED: they are FROZEN HISTORY and a figure
that was true when written is not stale, it is dated (ADR-0017 write-once — live facts have ONE
home, history is frozen). Scanning them would produce hundreds of "findings" nobody may act on,
which is how a probe teaches its reader to ignore it. Widen with `--glob` deliberately.

RULES (each is a live, READ-ONLY re-measurement):
  R1 snippets      `<n> snippet(s)`            = count of knowledge/snippets/*.reference.html
  R2 metas         `<n> meta(s)`               = count of knowledge/components/*.meta.json
  R3 showroom      `<n>-page showroom`         = count of showroom/*.html
  R4 type debt     `type-composite debt … <n>` = `_validate_type_composites.py` on its own
                   DEFAULT_TARGETS, parsed from `TYPE GATE FAIL — <n> violation(s)`.
                   ⚠ That script writes ONLY under `--ratchet`; this probe never passes it.
  R5 open items    `<n> open item(s)`          = `state == open` rows in knowledge/_state.json

⛔ WHAT IT CANNOT SEE: any figure with no rule (the rule table is the scope, and it is short —
five figures out of hundreds this repo carries) · a figure written in words · a stale figure in
a FROZEN document, deliberately · a figure that is stale in the same direction as its live
measurement (both wrong) · memory hooks, which live outside the repo entirely — the 1,101 case
was carried in a MEMORY HOOK, and this probe cannot reach there. That gap is DECLARED, not
designed away.

ENVIRONMENT: sandbox (pure python + one read-only subprocess).

USAGE
  python3 knowledge/_probe_registry/probe_stale_figure.py --check
  python3 knowledge/_probe_registry/probe_stale_figure.py --check --glob 'knowledge/*.md'
  python3 knowledge/_probe_registry/probe_stale_figure.py --measure   # just the live figures
  python3 knowledge/_probe_registry/probe_stale_figure.py --selftest
EXIT: 0 clean · 1 findings (or a live measurement that REFUSED — never defaulted to a pass).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob as globmod, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_GLOBS = ["knowledge/_LIVE-STATE.md", "GOOD-MORNING.md", "AGENTS.md", "README.md",
                 "knowledge/README.md"]


def _count(pattern):
    return len(globmod.glob(os.path.join(ROOT, pattern)))


def _m_snippets():
    return _count("knowledge/snippets/*.reference.html")


def _m_metas():
    return _count("knowledge/components/*.meta.json")


def _m_showroom():
    return _count("showroom/*.html")


def _m_open_items():
    doc = json.load(open(os.path.join(ROOT, "knowledge", "_state.json"), encoding="utf-8"))
    return sum(1 for it in doc.get("items", []) if (it.get("state") or "").lower() == "open")


def _m_type_debt():
    """Re-run the type gate READ-ONLY (no --ratchet, which is its only writing path).
    REFUSES loudly rather than guessing if the summary line cannot be parsed."""
    script = os.path.join(ROOT, "knowledge", "_validate_type_composites.py")
    spec = importlib.util.spec_from_file_location("_vtc_ro", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    targets = [p for p in mod.DEFAULT_TARGETS if os.path.exists(p)]
    p = subprocess.run([sys.executable, script] + targets, cwd=ROOT, capture_output=True,
                       text=True)
    m = re.search(r"TYPE GATE FAIL — (\d+) violation", p.stdout or "")
    if not m:
        raise RuntimeError("could not parse `TYPE GATE FAIL — <n> violation` from the gate's "
                           "own output (rc=%d) — REFUSED, not defaulted" % p.returncode)
    return int(m.group(1))


# (id, pattern, live measurement, unit, STRICT)
# STRICT=True means the bare shape (`<n> metas`) is ambiguous — it matches DELTA prose ("8
# metas edited") as readily as a carried total — so a totalising context is REQUIRED. This was
# not a design guess: the probe's first drive on the real tree at #206 produced 6 false
# positives of exactly that shape in GOOD-MORNING.md, and the precision arm in the selftest is
# now the fence. STRICT=False rules carry their own totalising noun in the pattern.
RULES = [
    ("R1", r"\b([\d,]+)\s+(?:canon\s+)?snippets?\b", _m_snippets, "snippets", True),
    ("R2", r"\b([\d,]+)\s+metas?\b", _m_metas, "component metas", True),
    ("R3", r"\b([\d,]+)[- ]page showroom\b", _m_showroom, "showroom pages", False),
    ("R4", r"type[- ]composite debt[^\d\n]{0,40}([\d,]+)", _m_type_debt, "type-composite debt",
     False),
    ("R5", r"\b([\d,]+)\s+open items?\b", _m_open_items, "open store items", False),
]

# A line carrying any of these is DELTA or FROZEN-HISTORY prose inside a living document —
# "8 metas edited" in a commit-state entry is a true statement about a past commit, not a
# carried inventory. Skipping them is the ADR-0017 boundary applied line by line.
HISTORY_MARKERS = ("commit-state", "landed", "→", "->", " added", "edited", "wave-",
                   "wave ", "step ", "(new)", "new)", "since ")
# For STRICT rules the number must sit in a TOTALISING context to count as a carried figure.
TOTALISING_RE = re.compile(r"\(|\btotal\b|\ball\b|\blibrary\b|\bcurrentl|\bthere are\b|"
                           r"\bwe have\b|\bwe ship\b|\bships?\b|\binventory\b|\bcount\b|"
                           r"\bexists?\b|\bstands? at\b", re.I)


def measure(verbose=True):
    """{rule_id: int} live figures. A rule that cannot be measured is REFUSED and returned as
    None — never silently dropped, never defaulted (feedback-measuring-tool-must-not-guess)."""
    live, refusals = {}, []
    for rid, _pat, fn, unit, _strict in RULES:
        try:
            live[rid] = fn()
        except Exception as e:
            live[rid] = None
            refusals.append((rid, unit, str(e)[:160]))
        if verbose:
            print("  live %s %-22s = %s" % (rid, unit,
                                            live[rid] if live[rid] is not None else "REFUSED"))
    for rid, unit, why in refusals:
        print("  ⛔ REFUSED %s (%s): %s" % (rid, unit, why))
    return live, refusals


def scan(paths, live, verbose=True):
    findings = []
    for path in paths:
        rel = os.path.relpath(path, ROOT)
        if not os.path.exists(path):
            continue
        for lineno, line in enumerate(open(path, encoding="utf-8", errors="replace")
                                      .read().splitlines(), 1):
            low = line.lower()
            if any(mk in low for mk in HISTORY_MARKERS):
                continue
            for rid, pat, _fn, unit, strict in RULES:
                if live.get(rid) is None:
                    continue
                if strict and not TOTALISING_RE.search(line):
                    continue
                for m in re.finditer(pat, line, re.I):
                    carried = int(m.group(1).replace(",", ""))
                    if carried != live[rid]:
                        findings.append((rel, rid, "%s:%d carries %s as %s — live measurement "
                                         "says %d" % (rel, lineno, unit, m.group(1), live[rid])))
    if verbose:
        for _rel, _rid, detail in findings:
            print("  ⛔ STALE-FIGURE %s" % detail)
    return findings


def check(patterns=None):
    patterns = patterns or DEFAULT_GLOBS
    paths = []
    for pat in patterns:
        paths += sorted(globmod.glob(os.path.join(ROOT, pat)))
    live, refusals = measure()
    findings = scan(paths, live)
    print("P-5 stale-figure grep: %d living doc(s) over %s · %d rule(s) live · %d REFUSED · "
          "%d finding(s)" % (len(paths), patterns, len([v for v in live.values()
                                                        if v is not None]), len(refusals),
                             len(findings)))
    print("PROBE P-5 — findings=%d" % (len(findings) + len(refusals)))
    return 1 if (findings or refusals) else 0


def selftest():
    """PLANT-THEN-DETECT, both directions, DRIVING the probe on a real living document with a
    real live measurement — never asserting on the probe's clause."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="p5-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    live, refusals = measure(verbose=True)
    if all(v is None for v in live.values()):
        print("⛔ selftest cannot run: every live measurement refused (declared, not a pass).")
        return 1

    src = None
    for cand in DEFAULT_GLOBS:
        p = os.path.join(ROOT, cand)
        if os.path.exists(p):
            src = p
            break
    if src is None:
        print("⛔ selftest cannot run: no living document in the default glob (declared).")
        return 1
    work = os.path.join(tmp, os.path.basename(src))
    shutil.copyfile(src, work)
    base = scan([work], live, verbose=False)
    print("  · baseline on a copy of %s: %d finding(s)" % (os.path.basename(src), len(base)))

    # PLANT the exact #203 shape: a carried figure one step off the live measurement
    planted = []
    for rid, _pat, _fn, unit, _s in RULES:
        if live.get(rid) is None:
            continue
        wrong = live[rid] + 4                       # 1,101 vs 1,097 — the real delta, verbatim
        if rid == "R3":
            planted.append("The %d-page showroom." % wrong)
        elif rid == "R4":
            planted.append("Type-composite debt is %s." % format(wrong, ","))
        elif rid == "R5":
            planted.append("There are %d open items." % wrong)
        else:
            planted.append("We ship %d %s." % (wrong, "snippets" if rid == "R1" else "metas"))
    open(work, "a", encoding="utf-8").write("\n\nPLANTED (selftest):\n" + "\n".join(planted))
    after = scan([work], live, verbose=False)
    new = [f for f in after if f not in base]
    caught_rules = {rid for _rel, rid, _d in new}
    for rid, _pat, _fn, unit, _s in RULES:
        if live.get(rid) is None:
            continue
        if rid not in caught_rules:
            fails.append("PLANT NOT CAUGHT: %s (%s) — a carried figure %d off the live %s went "
                         "unseen" % (rid, unit, 4, live[rid]))
        else:
            print("  ✅ plant caught (%s %s): %s" % (rid, unit,
                                                     [d for _r, i, d in new if i == rid][0][-88:]))

    # CONTROL — the CORRECT figure must NOT fire, or the probe cries wolf on every true number
    shutil.copyfile(src, work)
    ok_lines = []
    for rid, _pat, _fn, unit, _s in RULES:
        if live.get(rid) is None:
            continue
        n = live[rid]
        ok_lines.append({"R3": "The %d-page showroom." % n,
                         "R4": "Type-composite debt is %s." % format(n, ","),
                         "R5": "There are %d open items." % n}.get(
                             rid, "We ship %d %s." % (n, "snippets" if rid == "R1" else "metas")))
    open(work, "a", encoding="utf-8").write("\n\nCONTROL (selftest):\n" + "\n".join(ok_lines))
    ctrl = scan([work], live, verbose=False)
    if ctrl != base:
        fails.append("CONTROL FIRED: a CORRECT carried figure was reported stale — %s"
                     % [d for _r, _i, d in ctrl if (None, _i, d) not in base][:1])
    else:
        print("  ✅ control held: figures matching the live measurement produce no finding")

    # PRECISION CONTROL — the false-positive shapes the probe's FIRST DRIVE actually produced
    # at #206 (GOOD-MORNING.md delta prose). None of these may become a finding.
    shutil.copyfile(src, work)
    open(work, "a", encoding="utf-8").write(
        "\n\nPRECISION CONTROL (selftest — real shapes from the #206 first drive):\n"
        "> **commit-state #95:** 8 snippets + 8 metas + 3 receipts (NEW)\n"
        "- SIX NEW P2 COMPONENTS ARE BUILT: LIBRARY 85 → 91, each with a snippet, a meta\n"
        "- wave-2: 5 snippets + 5 metas edited\n")
    prec = scan([work], live, verbose=False)
    if prec != base:
        fails.append("PRECISION CONTROL FIRED: delta/history prose was reported as a stale "
                     "carried figure — %s" % [d for _r, _i, d in prec][-2:])
    else:
        print("  ✅ precision control held: delta and commit-state prose produce no finding "
              "(the 6 false positives from the #206 first drive stay closed)")

    # direction 2 — remove the plant, back to baseline
    shutil.copyfile(src, work)
    restored = scan([work], live, verbose=False)
    if restored != base:
        fails.append("REMOVAL NOT GREEN: restored doc gave %d finding(s), baseline %d"
                     % (len(restored), len(base)))
    else:
        print("  ✅ removal green: with the plant gone the probe returns to baseline (%d)"
              % len(base))

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-5 selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ P-5 selftest PASS — every rule's planted stale figure detected against a LIVE "
          "measurement, correct figures silent, removal green.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    if "--measure" in argv:
        live, refusals = measure()
        sys.exit(1 if refusals else 0)
    pats = [argv[i + 1] for i, a in enumerate(argv) if a == "--glob"]
    sys.exit(check(pats or None))
