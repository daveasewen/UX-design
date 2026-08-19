#!/usr/bin/env python3
"""probe_premise_store.py — P-4: PREMISE-vs-STORE diff for brief-class documents (W-45).

THE CLASS, from the receipts: a brief or snapshot carries a PREMISE about repo state, the state
moves, and the premise is never re-checked — [[premise-ages-faster-than-rule]]. #203 lane H
found a derived snapshot's Status column briefing six lanes at "18/18 already existed", produced
by slug matching, which also produced four FALSE ABSENCES
(`notes/_receipts/2026-08-19-203-wave3b-laneH-itinerary-status.md:30,46`). #204's own brief was
committed with NO STORE ROW at all, which flipped the doc-row gate red the moment it was tracked
(`notes/_receipts/2026-08-19-204-buildpm-claim-table.md` FIX 3 — repaired by adding `W-43`).
Both are the same shape: a DOCUMENT and the STORE disagree, and nothing joins them.

WHAT THIS PROBE DOES, over a glob of premise-carrying documents:
  1. every `W-<n>` task token cited must EXIST in `knowledge/_state.json`   → UNKNOWN-ITEM
  2. every `s<n>-D<n>` ruling token cited must EXIST in `knowledge/_rulings.json`
                                                                            → UNKNOWN-RULING
  3. a line that asserts a task is CLOSED/DONE while the store says `open` (or asserts it is
     OPEN while the store says closed) is a                                 → STATE-CONTRADICTION
     Lines containing `closes_when` are skipped — that is the store's own vocabulary, not an
     assertion about state (an honest refusal needs a legal form; so does an honest quote).
  4. every brief-class document in the glob must be NAMED BY SOME STORE ROW'S `home`
                                                                            → UNROWED-DOC
     (the #185 forgotten-document class; `knowledge/_gate_doc_rows.py` gates the TRACKED
     population, this probe sees UNTRACKED drafts too — that is the gap it adds, not a
     duplicate. It never writes; the repair is one `_state.add()` row, the conductor's.)
     Scoped by the gate's OWN frozen-legacy cutoff: only briefs whose filename date is
     >= `BASELINE_DATE` (2026-08-15, inherited from `_gate_doc_rows.py`, PICKED not derived).

GLOB — rules only as wide as [[gate-glob-scope-rule]]:  notes/_briefs/*.md
Widen with `--glob '<pattern>'` (repeatable).

⛔ WHAT IT CANNOT SEE: whether a premise that cites NO token is stale (most prose premises) ·
whether the store itself is right · figures (that is P-5) · a premise about the world outside
this repo. It is a TOKEN-JOIN, not a comprehension check.

ENVIRONMENT: sandbox (pure python; reads `_state.json` + `_rulings.json`, writes nothing —
`_inscribe_ruling.py` is the only rulings writer and this probe is not it).

USAGE
  python3 knowledge/_probe_registry/probe_premise_store.py --check
  python3 knowledge/_probe_registry/probe_premise_store.py --check --glob 'notes/_briefs/*.md'
  python3 knowledge/_probe_registry/probe_premise_store.py --selftest
EXIT: 0 clean · 1 findings.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob as globmod, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STORE = os.path.join(ROOT, "knowledge", "_state.json")
RULINGS = os.path.join(ROOT, "knowledge", "_rulings.json")
DEFAULT_GLOBS = ["notes/_briefs/*.md"]

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
# INHERITED, not invented: the same frozen-legacy cutoff `knowledge/_gate_doc_rows.py` uses
# (BASELINE_DATE = "2026-08-15", itself PICKED not derived — Dave may rule his own number).
# Briefs dated before it are a frozen legacy set, exempt from the UNROWED-DOC leg exactly as
# they are in the gate; without this the leg reports 55 historical briefs as live findings.
BASELINE_DATE = "2026-08-15"

TASK_RE = re.compile(r"\b(W-\d+)\b")
RULING_RE = re.compile(r"\b(s\d+-D\d+[a-z]?)\b")
CLOSED_RE = re.compile(r"\b(CLOSED|closed|DONE|LANDED|complete[d]?)\b")
OPEN_RE = re.compile(r"\b(OPEN|open|still open|outstanding)\b")


def load_store(store=STORE, rulings=RULINGS):
    s = json.load(open(store, encoding="utf-8"))
    items = {it["id"]: it for it in s.get("items", [])}
    homes = set()
    for it in s.get("items", []):
        h = (it.get("home") or "").strip()
        if h:
            homes.add(h)
            homes.add(os.path.basename(h))
    r = json.load(open(rulings, encoding="utf-8"))
    rule_ids = {x["id"] for x in (r.get("rulings") if isinstance(r, dict) else r)}
    return items, homes, rule_ids


def scan(paths, items, homes, rule_ids, verbose=True):
    findings = []
    for path in paths:
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8", errors="replace").read()
        m = DATE_RE.match(os.path.basename(rel))
        in_scope = bool(m) and m.group(1) >= BASELINE_DATE
        if in_scope and rel not in homes and os.path.basename(rel) not in homes:
            findings.append((rel, "UNROWED-DOC", "%s is named by no store row's `home` — the "
                             "#185 forgotten-document class; the repair is one `_state.add()` "
                             "row and it is the conductor's, not this probe's" % rel))
        for lineno, line in enumerate(text.splitlines(), 1):
            if "closes_when" in line:
                continue
            for tok in set(TASK_RE.findall(line)):
                if tok not in items:
                    findings.append((rel, "UNKNOWN-ITEM", "%s:%d cites %s — no such item in "
                                     "_state.json" % (rel, lineno, tok)))
                    continue
                state = (items[tok].get("state") or "").lower()
                if state == "open" and CLOSED_RE.search(line) and not OPEN_RE.search(line):
                    findings.append((rel, "STATE-CONTRADICTION", "%s:%d asserts %s closed/done; "
                                     "the store says state=open" % (rel, lineno, tok)))
                elif state and state != "open" and OPEN_RE.search(line) \
                        and not CLOSED_RE.search(line):
                    findings.append((rel, "STATE-CONTRADICTION", "%s:%d asserts %s open; the "
                                     "store says state=%s" % (rel, lineno, tok, state)))
            for tok in set(RULING_RE.findall(line)):
                if tok not in rule_ids:
                    findings.append((rel, "UNKNOWN-RULING", "%s:%d cites %s — no such ruling in "
                                     "_rulings.json" % (rel, lineno, tok)))
    if verbose:
        for rel, kind, detail in findings:
            print("  ⛔ %-20s %s" % (kind, detail))
    return findings


def check(patterns=None):
    patterns = patterns or DEFAULT_GLOBS
    paths = []
    for pat in patterns:
        paths += sorted(globmod.glob(os.path.join(ROOT, pat)))
    items, homes, rule_ids = load_store()
    findings = scan(paths, items, homes, rule_ids)
    print("P-4 premise-vs-store diff: %d doc(s) over %s vs %d store item(s) / %d ruling(s) · "
          "%d finding(s)" % (len(paths), patterns, len(items), len(rule_ids), len(findings)))
    if not paths:
        print("⚠ THE GLOB MATCHED NOTHING — an empty population is not a pass.")
        print("PROBE P-4 — findings=1")
        return 1
    print("PROBE P-4 — findings=%d" % len(findings))
    return 1 if findings else 0


def selftest():
    """PLANT-THEN-DETECT on a REAL brief + the REAL store, both directions. The probe is
    DRIVEN; nothing here asserts on the probe's clause."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="p4-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    items, homes, rule_ids = load_store()

    src = sorted(globmod.glob(os.path.join(ROOT, "notes", "_briefs", "*.md")))
    if not src:
        print("⛔ selftest cannot run: no notes/_briefs/*.md to plant into (declared).")
        return 1
    # choose a brief that IS rowed, so the baseline is quiet
    rowed = [p for p in src if os.path.relpath(p, ROOT) in homes
             or os.path.basename(p) in homes]
    src = (rowed or src)[0]
    work = os.path.join(tmp, os.path.basename(src))
    shutil.copyfile(src, work)
    # the copy lives outside the repo, so make the store believe it is homed
    homes_plus = set(homes) | {os.path.relpath(work, ROOT), os.path.basename(work)}

    base = scan([work], items, homes_plus, rule_ids, verbose=False)
    print("  · baseline on a copy of %s: %d finding(s)" % (os.path.basename(src), len(base)))

    open_item = next((i for i, it in items.items()
                      if (it.get("state") or "").lower() == "open" and TASK_RE.fullmatch(i)),
                     None)
    if not open_item:
        print("⛔ selftest cannot run: the store has no open item to contradict (declared).")
        return 1
    plants = ("\n\nPLANTED PREMISE LINES (selftest):\n"
              "- W-99999 is the lane we are building.\n"
              "- %s is CLOSED and shipped.\n"
              "- ruled s99999-D9 by Dave.\n" % open_item)
    open(work, "a", encoding="utf-8").write(plants)
    after = scan([work], items, homes_plus, rule_ids, verbose=False)
    new = [f for f in after if f not in base]
    kinds = {k for _p, k, _d in new}
    for want, why in (("UNKNOWN-ITEM", "a cited task id that is in no store row"),
                      ("STATE-CONTRADICTION", "a doc asserting an OPEN item is closed"),
                      ("UNKNOWN-RULING", "a cited ruling id that is in no rulings row")):
        if want not in kinds:
            fails.append("PLANT NOT CAUGHT: %s — %s produced no finding" % (want, why))
        else:
            print("  ✅ plant caught (%s): %s" % (want, [d for _p, k, d in new
                                                        if k == want][0][-92:]))

    # the UNROWED-DOC leg, planted directly: a brief no store row homes
    orphan = os.path.join(tmp, "2026-08-18-000-orphan-brief.md")  # dated AFTER the baseline
    open(orphan, "w", encoding="utf-8").write("# an orphan brief with no store row\n")
    orphan_findings = scan([orphan], items, homes, rule_ids, verbose=False)
    if not any(k == "UNROWED-DOC" for _p, k, _d in orphan_findings):
        fails.append("PLANT NOT CAUGHT: UNROWED-DOC — a brief no store row homes went unseen")
    else:
        print("  ✅ plant caught (UNROWED-DOC): an unrowed brief is named")

    # control — the FROZEN LEGACY set (dated before BASELINE_DATE) must NOT fire, or the leg
    # reports 55 historical briefs as live findings and the verifier learns to ignore it
    legacy = os.path.join(tmp, "2026-08-01-000-legacy-brief.md")
    open(legacy, "w", encoding="utf-8").write("# a pre-baseline brief with no store row\n")
    if any(k == "UNROWED-DOC" for _p, k, _d in scan([legacy], items, homes, rule_ids,
                                                    verbose=False)):
        fails.append("CONTROL FIRED: a pre-BASELINE_DATE brief was flagged UNROWED — the frozen "
                     "legacy set that _gate_doc_rows.py exempts would become 55 daily findings")
    else:
        print("  ✅ control held: a pre-%s brief is exempt (frozen legacy, gate's own cutoff)"
              % BASELINE_DATE)

    # direction 2 — remove the plants, back to baseline
    shutil.copyfile(src, work)
    restored = scan([work], items, homes_plus, rule_ids, verbose=False)
    if restored != base:
        fails.append("REMOVAL NOT GREEN: restored doc gave %d finding(s), baseline %d"
                     % (len(restored), len(base)))
    else:
        print("  ✅ removal green: with the plants gone the probe returns to baseline (%d)"
              % len(base))

    # control — a `closes_when` line quoting the same words must NOT fire
    open(work, "a", encoding="utf-8").write(
        '\n- closes_when: %s is CLOSED and the wrap lands\n' % open_item)
    ctrl = scan([work], items, homes_plus, rule_ids, verbose=False)
    if ctrl != base:
        fails.append("CONTROL FIRED: a `closes_when` line was read as a state assertion — the "
                     "store's own vocabulary would fail on every brief that quotes it")
    else:
        print("  ✅ control held: a `closes_when` line quoting CLOSED is not a contradiction")

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-4 selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ P-4 selftest PASS — every planted premise/store disagreement detected on a REAL "
          "brief against the REAL store, removal green, control held.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    pats = [argv[i + 1] for i, a in enumerate(argv) if a == "--glob"]
    sys.exit(check(pats or None))
