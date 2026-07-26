#!/usr/bin/env python3
"""Capture gate (_RUNBOOK-capture-ritual.md § "The gate") + Memento §4.1 provenance/status.

Built 2026-07-26 under the Memento dream-pass lane rulings (ledger:
notes/_MEMENTO-DECISIONS.md — D1a repo-side-only · D2 five-value vocab · D3 one script).

TWO MODES, one script (D3):

  BUILD MODE (default — wired into _build_all.py, BLOCKING):
    Provenance/status fields on NEW repo capture surfaces. Scope (D1a, honest per the
    gate-glob-scope rule — the rule is only as wide as this glob):
      notes/YYYY-MM-DD-*.md          (non-underscore-prefixed, date >= CUTOVER)
      _DECISION-HISTORY/YYYY-MM-DD-*.md  (date >= CUTOVER)
    CUTOVER = 2026-07-26. No corpus retrofit — the gate fires on new files, not history
    (assertion-propagation lesson: gate the flip, don't chase the past).
    Canonical field lines (plain lowercase keys, line-start, within the first 40 lines):
      provenance: <session-id> · <YYYY-MM-DD>
      status: observed | inferred | ruled | floated | standing
    FAIL — missing `status:` · unknown status value · `status: ruled` with no ledger
           pointer after the value · `provenance:` present but with no parseable date.
    WARN — missing `provenance:` (session-id is soft; titles rotate) · a `ruled` pointer
           whose path-like token matches no file.

  WRAP MODE (--wrap — run BY THE SESSION at capture-ritual time, not in the build):
    Everything above, plus the runbook's original capture checks:
    FAIL — `_LIVE-STATE.md` "Last refreshed" is not today · `GOOD-MORNING.md` header
           zone doesn't carry today's date.
    WARN — uncommitted changes (nudge to commit before close).
    HONEST SKIP — MEMORY.md dangling-pointer check: the memory store lives outside the
    repo, invisible to the shell and to every gate (runbook step 3). Memory-side fields
    are ritual discipline, checked by the session with file tools at step 3 — UNENFORCED
    by design (D1a). Claiming otherwise would be the false inscription this programme
    exists to stop.

Usage:  python3 knowledge/_capture_gate.py             # build mode (blocking)
        python3 knowledge/_capture_gate.py --wrap      # wrap mode (session-run)
        python3 knowledge/_capture_gate.py --selftest  # bite-test, one fixture per FAIL class
Writes _CAPTURE-GATE.md; exits non-zero on any FAIL."""
import datetime
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
REPORT = os.path.join(HERE, "_CAPTURE-GATE.md")

CUTOVER = datetime.date(2026, 7, 26)
VOCAB = {"observed", "inferred", "ruled", "floated", "standing"}  # D2: five values
HEADER_LINES = 40

DATE_PREFIX_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")
STATUS_RE = re.compile(r"^status:\s*(\S+)\s*(.*)$")
PROV_RE = re.compile(r"^provenance:\s*(.+)$")
ISO_DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
PATHISH_RE = re.compile(r"[\w./_-]+\.md")


def file_date(basename):
    m = DATE_PREFIX_RE.match(basename)
    if not m:
        return None
    try:
        return datetime.date(*map(int, m.groups()))
    except ValueError:
        return None


def in_scope(repo):
    out = []
    for pat in ("notes/*.md", "_DECISION-HISTORY/*.md"):
        for p in sorted(glob.glob(os.path.join(repo, pat))):
            b = os.path.basename(p)
            if b.startswith("_"):
                continue  # ledgers/indexes/receipts are exempt (D1a scope)
            d = file_date(b)
            if d and d >= CUTOVER:
                out.append(p)
    return out


def check_file(path, repo):
    """Returns (fails, warns) for one file."""
    fails, warns = [], []
    rel = os.path.relpath(path, repo)
    try:
        with open(path, encoding="utf-8") as f:
            head = [next(f, "") for _ in range(HEADER_LINES)]
    except OSError as e:
        return [f"{rel}: unreadable — {e}"], []

    status_line = prov_line = None
    for ln in head:
        if status_line is None:
            m = STATUS_RE.match(ln)
            if m:
                status_line = m
        if prov_line is None:
            m = PROV_RE.match(ln)
            if m:
                prov_line = m

    if status_line is None:
        fails.append(f"{rel}: missing `status:` line (vocab: {' | '.join(sorted(VOCAB))})")
    else:
        val = status_line.group(1).rstrip(".,;·")
        rest = status_line.group(2).strip(" ·-—→>")
        if val not in VOCAB:
            fails.append(f"{rel}: unknown status `{val}` (vocab: {' | '.join(sorted(VOCAB))})")
        elif val == "ruled":
            if not rest:
                fails.append(f"{rel}: `status: ruled` names no ledger — promotion is Dave's "
                             f"alone and must point at its ledger/ADR entry")
            else:
                pm = PATHISH_RE.search(rest)
                if pm and not os.path.exists(os.path.join(repo, pm.group(0))):
                    warns.append(f"{rel}: ruled-pointer `{pm.group(0)}` matches no file")

    if prov_line is None:
        warns.append(f"{rel}: missing `provenance:` line (soft — add `<session-id> · <date>`)")
    else:
        dm = ISO_DATE_RE.search(prov_line.group(1))
        ok = False
        if dm:
            try:
                datetime.date(*map(int, dm.groups()))
                ok = True
            except ValueError:
                pass
        if not ok:
            fails.append(f"{rel}: `provenance:` carries no parseable YYYY-MM-DD date "
                         f"(take it from `date`, never from belief — T-D12)")
    return fails, warns


def wrap_checks(repo, today):
    fails, warns, notes = [], [], []
    iso = today.isoformat()
    for fname, label in (("_LIVE-STATE.md", '"Last refreshed"'), ("GOOD-MORNING.md", "header date")):
        p = os.path.join(repo, fname)
        if not os.path.exists(p):
            fails.append(f"{fname}: missing")
            continue
        with open(p, encoding="utf-8") as f:
            head = "".join(f.readline() for _ in range(HEADER_LINES))
        if iso not in head:
            fails.append(f"{fname}: {label} zone does not carry today ({iso}) — refresh it "
                         f"(ritual steps 1 / 2) before closing")
    try:
        r = subprocess.run(["git", "-C", repo, "status", "--porcelain"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            n = len(r.stdout.strip().splitlines())
            warns.append(f"git: {n} uncommitted path(s) — commit before close (step 5)")
    except Exception as e:  # git absent — advisory only
        warns.append(f"git check skipped ({e})")
    notes.append("HONEST SKIP — memory-store checks (MEMORY.md pointers, memory-file fields): "
                 "outside the repo, invisible to this gate. Session checks them by hand at "
                 "ritual step 3 (D1a — unenforced by design).")
    return fails, warns, notes


def run(mode="build", repo=REPO, report=REPORT, today=None):
    today = today or datetime.date.today()
    fails, warns, notes = [], [], []
    scoped = in_scope(repo)
    for p in scoped:
        f, w = check_file(p, repo)
        fails += f
        warns += w
    if mode == "wrap":
        f, w, n = wrap_checks(repo, today)
        fails += f
        warns += w
        notes += n

    lines = [f"# Capture gate report — mode: {mode}",
             f"*Generated {today.isoformat()} by `_capture_gate.py`. "
             f"Scope: {len(scoped)} file(s) at/after cutover {CUTOVER.isoformat()}.*", ""]
    for title, items in (("FAIL", fails), ("WARN", warns), ("NOTE", notes)):
        if items:
            lines.append(f"## {title}")
            lines += [f"- {i}" for i in items]
            lines.append("")
    if not fails and not warns:
        lines.append("✅ Green — all scoped surfaces carry provenance + status.")
    if report:
        with open(report, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    for i in fails:
        print(f"  ❌ FAIL {i}")
    for i in warns:
        print(f"  ⚠️  WARN {i}")
    for i in notes:
        print(f"  ▫️  {i}")
    print(f"capture gate [{mode}]: {len(scoped)} in scope · "
          f"{len(fails)} fail · {len(warns)} warn")
    return 1 if fails else 0


# ---------------------------------------------------------------- selftest
FIXTURES = {
    # one fixture per FAIL class + one green control (attribute-the-diff: the control
    # proves the gate passes well-formed input, so a red run is the input's fault)
    "2026-07-26-missing-status.md": "# t\n\nprovenance: sess-x · 2026-07-26\n\nbody\n",
    "2026-07-26-unknown-status.md": "# t\n\nprovenance: sess-x · 2026-07-26\nstatus: vibes\n",
    "2026-07-26-ruled-no-pointer.md": "# t\n\nprovenance: sess-x · 2026-07-26\nstatus: ruled\n",
    "2026-07-26-bad-date.md": "# t\n\nprovenance: sess-x · yesterday-ish\nstatus: observed\n",
    "2026-07-26-good.md": ("# t\n\nprovenance: sess-x · 2026-07-26\n"
                           "status: ruled · _DECISION-HISTORY/README.md\n"),
}


def selftest():
    failures = []
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        os.makedirs(os.path.join(td, "_DECISION-HISTORY"))
        # the good fixture's pointer must resolve inside the fixture repo
        os.makedirs(os.path.join(td, "_DECISION-HISTORY"), exist_ok=True)
        with open(os.path.join(td, "_DECISION-HISTORY", "README.md"), "w") as f:
            f.write("fixture ledger\n")
        for name, body in FIXTURES.items():
            with open(os.path.join(td, "notes", name), "w", encoding="utf-8") as f:
                f.write(body)
        for name in FIXTURES:
            f_, w_ = check_file(os.path.join(td, "notes", name), td)
            should_fail = "good" not in name
            if should_fail and not f_:
                failures.append(f"{name}: expected FAIL, gate stayed green — gate does not bite")
            if not should_fail and f_:
                failures.append(f"{name}: expected green, got {f_}")
        # whole-run must exit non-zero on the fixture set (4 bad + 1 good)
        rc = run(mode="build", repo=td, report=None,
                 today=datetime.date(2026, 7, 26))
        if rc == 0:
            failures.append("run() returned 0 over a fixture set with known failures")
    if failures:
        for x in failures:
            print(f"  ❌ selftest: {x}")
        return 1
    print("  ✅ capture-gate selftest: all failure classes bite; green control passes")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(mode="wrap" if "--wrap" in sys.argv else "build"))
