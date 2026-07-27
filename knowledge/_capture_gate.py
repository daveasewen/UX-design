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
    --lane (S-D2, ruled 2026-07-26): a SPIN-OFF-LANE session runs `--wrap --lane` —
    skips ONLY the GOOD-MORNING header check (lanes are ruled OUTSIDE the GM queue,
    _LIVE-STATE §🔀 is still their record so that check still bites). Noted in output
    so the skip is visible, never silent.
    S-D3 (ruled 2026-07-26): wrap mode reports to STDOUT ONLY — it no longer writes
    `_CAPTURE-GATE.md`, which is build mode's committed report (wrap used to clobber
    it with a transient session verdict).
    HONEST SKIP — MEMORY.md dangling-pointer check: the memory store lives outside the
    repo, invisible to the shell and to every gate (runbook step 3). Memory-side fields
    are ritual discipline, checked by the session with file tools at step 3 — UNENFORCED
    by design (D1a). Claiming otherwise would be the false inscription this programme
    exists to stop.

Usage:  python3 knowledge/_capture_gate.py             # build mode (blocking)
        python3 knowledge/_capture_gate.py --wrap      # wrap mode (session-run)
        python3 knowledge/_capture_gate.py --wrap --lane  # lane session wrap (skips GM check)
        python3 knowledge/_capture_gate.py --selftest  # bite-test, one fixture per FAIL class
Build mode writes _CAPTURE-GATE.md; wrap mode is stdout-only (S-D3). Exits non-zero on any FAIL."""
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

# ---------------------------------------------------------------- pre-flight stamp
# RULED by Dave 2026-07-27 (_RUNBOOK-context-gauge.md § ★ Half 0b — "the gauge must be a
# THROTTLE, not a thermometer"). The handoff must carry the pre-flight estimate it was priced
# with, in the canonical form:
#
#   pre-flight: fill 40% + job 12% + wrap 5% = 57% AMBER · reserve 15% ring-fenced
#
# ⚠ WHAT THIS CHECKS AND WHAT IT CANNOT (anti-false-fix clause 3 of the runbook section):
# it checks the FORM of the stamp — that three terms are present (the wrap is the one
# historically omitted), that they sum to the stated total, and that the named band matches
# the band table. It CANNOT check whether the fill figure is honest, and it CANNOT observe
# whether a mid-job re-price happened. Those are discipline, not enforcement. Do NOT "fix"
# this gate by having it invent its own fill estimate: it has no access to the token tally,
# and a guessed number wearing a gate's authority is the failure this programme exists to stop.
BANDS = ((45, "GREEN"), (60, "AMBER"), (10 ** 9, "RED"))  # Dave recalibrated 2026-07-25
WRAP_FLOOR = 5      # runbook: "WRAP (~5%)" — soft, hence WARN not FAIL
RESERVE_FENCE = 15  # runbook § Half 0b: ring-fenced, NOT an addend
PREFLIGHT_RE = re.compile(r"^\s*>?\s*\**pre-?flight\**\s*[:—-]", re.I)
TERM_RE = {k: re.compile(r"\b%s\b\D{0,4}(\d+)" % k, re.I) for k in ("fill", "job", "wrap")}
TOTAL_RE = re.compile(r"=\s*[~≈]?\s*(\d+)")
BAND_WORD_RE = re.compile(r"\b(GREEN|AMBER|RED)\b", re.I)
RESERVE_RE = re.compile(r"\breserve\b\D{0,4}(\d+)", re.I)

# ---------------------------------------------------------------- section growth contracts
# GM-D1(a) / D5(a) / D6(a) / D7(a) / D8(a), ruled 2026-07-27 (`notes/_MEMENTO-DECISIONS.md`
# § GM growth-contracts; enacted here + `_RUNBOOK-capture-ritual.md` steps 2e/2f).
# The architecture: every GM section declares a growth contract — what it may contain · cap ·
# roll target · retirement test — and §A alone is standing and uncapped.
#
# This block enforces the CAP half only. The typed-content and retirement halves are ritual
# discipline, and saying so is the point: see the anti-false-fix note below.
#
# ⚠ WRAP MODE ONLY, and the reason is sequencing. These budgets describe the state a WRAP must
# leave behind. In build mode they would fail every build from the moment they shipped until the
# first compaction pass ran — a gate red for a reason no build can fix, which teaches the team to
# ignore it. Wrap mode is still BLOCKING in its mode; none of this is advisory.
#
# ⚠ WHAT THIS CANNOT SEE — do not "fix" it by teaching it to guess (same discipline as the
# pre-flight block above, and the reason that one has held):
#   · whether DO-FIRST's content is of the four PERMITTED TYPES (2e) — a line count is blind to a
#     restated body wearing a pointer's clothes;
#   · whether a notice is retirement-DUE — 2e's four tests key on live targets, elapsed terms and
#     struck sources, none of which are in this file;
#   · whether a move was VERBATIM.
# Its job is the one thing it can observe exactly: how big each region is.
SECTION_RE = (
    ("DO-FIRST", re.compile(r"^##\s*⬛\s*DO TH", re.I)),
    ("§A",       re.compile(r"^#\s*§A\b")),
    ("§B",       re.compile(r"^#\s*§B\b")),
    ("§C",       re.compile(r"^#\s*§C\b")),
)
SECTION_CAPS = {"DO-FIRST": (120, 180), "§C": (150, 225)}  # (warn, BLOCK) — block = cap+50%, D8(a)
SECTION_EXEMPT = {"§A"}    # standing + uncapped by ruling: measured and reported, NEVER charged
SECTION_RETIRED = {"§B"}   # D4(a) deleted it into the banner — its reappearance IS the failure
SECTION_REQUIRED = ("DO-FIRST", "§A", "§C")

# 2f: the session-strata stack. It is excluded from §C's cap by D6(a) — which is only checkable if
# it is DELIMITED, so 2f requires the marker below. ⚠ Excluding a region from a cap without giving
# it a rule of its own is precisely how "splitting buys headroom"; the region's rule is D5(a) —
# GM keeps LATEST ONLY — so the gate counts blocks, not lines. One block is the whole contract.
STRATA_HEAD_RE = re.compile(r"^###\s*⏱\s*SESSION STRATA\b", re.I)
STRATA_BLOCK_RE = re.compile(r"^####\s")
STRATA_MAX_BLOCKS = 1

# D7(a) size stamps, AS AMENDED 2026-07-27 (Dave, this window — see `notes/_MEMENTO-DECISIONS.md`
# § GM-D7 amendment). The original D7 set GM ≤ 8K tk whole-file. Measured with tiktoken, that is
# unreachable while §A is untouchable: GM = 25,618 tk of which **§A alone = 4,208 tk = 53% of the
# whole 8K**, leaving ~3.8K for banners + DO-FIRST + §C, which today are 19,869. The proposal's own
# predicted post-pass outcome (450–500 ln = 12.3–13.7K tk) would have BLOCKED at 8K+50%.
# ⇒ RULED: **the budget applies to the COMPACTABLE REGION** (everything but §A), and the whole-file
# figure is ALWAYS published beside it so true cold-start cost is never hidden by the exclusion.
# §A is excluded from the budget exactly as it is already excluded from the line caps — charging a
# section you may not touch is not a budget, it is a permanent debt.
SIZE_BUDGET_TK = {"compactable": 8000}   # warn at cap · BLOCK at cap+50% (12,000), per D8(a)
BYTES_PER_TOKEN = 3.53     # MEASURED on GM, tiktoken cl100k_base, 2026-07-27. NOT the chars/4 rule
#                            of thumb: this corpus runs ~13% denser because of its ★ ⚠ ⛔ · — load,
#                            so every earlier chars/4 token estimate of these files read LOW.
SIZE_STAMP_RE = re.compile(r"^\s*>?\s*\**size\**\s*[:—-]\s*(.+)$", re.I)
SIZE_TK_RE = re.compile(r"\bGM\b\D{0,12}?([\d.]+)\s*K\s*tk", re.I)  # K is REQUIRED: without it
#   "GM 25618 tk" would parse as 25.6M and pass a drift check by accident. One canonical form.
SIZE_TOLERANCE = 0.10      # a stamp is a claim about a measurable thing; 10% drift = re-stamp

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


def band_for(total):
    """The band table, read not recalled (runbook § READ THE BAND TABLE)."""
    for ceiling, name in BANDS:
        if total < ceiling:
            return name
    return "RED"


def check_preflight(text, label="GOOD-MORNING.md"):
    """FORM check on the pre-flight stamp. Returns (fails, warns).

    Bites on the three failures actually observed: the wrap term omitted (2026-07-27 #2),
    a band asserted from memory instead of the table (twice), and arithmetic that doesn't
    close. Everything it cannot see is named in the module header, not implied away."""
    fails, warns = [], []
    line = next((ln for ln in text.splitlines() if PREFLIGHT_RE.match(ln)), None)
    if line is None:
        return ([f"{label}: no `pre-flight:` stamp — the handoff must carry the estimate the "
                 f"session was priced with (runbook § ★ Half 0b). Form: `pre-flight: fill N% + "
                 f"job N% + wrap N% = N% BAND · reserve 15% ring-fenced`"], warns)

    terms = {}
    for key, rx in TERM_RE.items():
        m = rx.search(line)
        if m:
            terms[key] = int(m.group(1))
    missing = [k for k in ("fill", "job", "wrap") if k not in terms]
    if missing:
        fails.append(f"{label}: pre-flight stamp has {len(terms)} of 3 terms — missing "
                     f"{', '.join(missing)}. \"A pre-flight estimate that does not include the "
                     f"wrap is not a pre-flight estimate\"")

    tm = TOTAL_RE.search(line)
    bm = BAND_WORD_RE.search(line)
    if not tm:
        fails.append(f"{label}: pre-flight stamp states no projected total (`= N%`)")
    if not bm:
        fails.append(f"{label}: pre-flight stamp names no band — state the NUMBER and the BAND "
                     f"together so a mismatch is visible in one glance")

    if tm and not missing:
        total, summed = int(tm.group(1)), sum(terms[k] for k in ("fill", "job", "wrap"))
        if abs(total - summed) > 1:  # 1 point of rounding slack
            fails.append(f"{label}: pre-flight arithmetic does not close — "
                         f"{terms['fill']}+{terms['job']}+{terms['wrap']} = {summed}, "
                         f"stamp says {total}")
    if tm and bm:
        total, named, truth = int(tm.group(1)), bm.group(1).upper(), band_for(int(tm.group(1)))
        if named != truth:
            fails.append(f"{label}: pre-flight band MIS-READ — {total}% is {truth} by the band "
                         f"table, stamp says {named}. Quote the table, never recall it")

    if terms.get("wrap", WRAP_FLOOR) < WRAP_FLOOR:
        warns.append(f"{label}: wrap reserved at {terms['wrap']}% (runbook says ~{WRAP_FLOOR}%) "
                     f"— the ritual is not free")
    if not RESERVE_RE.search(line):
        warns.append(f"{label}: pre-flight names no ring-fenced reserve (~{RESERVE_FENCE}%) — "
                     f"the fence is what makes the gauge a throttle rather than a thermometer")
    return fails, warns


def section_spans(lines):
    """Split GOOD-MORNING.md into its contracted regions. Returns {name: (start, end)} in lines.

    ⚠ The caller fails LOUD on a missing required marker rather than measuring nothing and
    reporting green. A structural check that silently measures zero is the "cheerful 0 deviations"
    failure this corpus has already been bitten by (the type sweep reading ZERO without
    --allow-file-access-from-files, and reporting success)."""
    hits = []
    for name, rx in SECTION_RE:
        for i, ln in enumerate(lines):
            if rx.match(ln):
                hits.append((i, name))
                break
    hits.sort()
    return {name: (i, hits[n + 1][0] if n + 1 < len(hits) else len(lines))
            for n, (i, name) in enumerate(hits)}


def measure_tokens(text):
    """Returns (tokens, method). tiktoken when present (OBSERVED); otherwise the MEASURED byte
    divisor, labelled ESTIMATE. Both are declared and they are never silently mixed — a number
    whose method is unstated is the thing this gate exists to prevent."""
    try:
        import tiktoken
        return len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"
    except Exception:
        return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)")


def check_budgets(repo):
    """GM section line caps (D1a/D6a) + the D7 size stamp. Returns (fails, warns, notes)."""
    fails, warns, notes = [], [], []
    gm_path = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm_path):
        return ["GOOD-MORNING.md: missing — ritual step 2"], warns, notes
    with open(gm_path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    spans = section_spans(lines)

    missing = [n for n in SECTION_REQUIRED if n not in spans]
    if missing:
        return ([f"GOOD-MORNING.md: section marker(s) not found ({', '.join(missing)}) — "
                 f"ritual step 2"], warns, notes)
    for name in SECTION_RETIRED:
        if name in spans:
            fails.append(f"GOOD-MORNING.md: {name} present — ritual step 2")

    # 2f strata stack: excluded from §C's cap (D6a), governed by block COUNT instead (D5a).
    strata_lines, c_start, c_end = 0, *spans["§C"]
    for i in range(c_start, c_end):
        if STRATA_HEAD_RE.match(lines[i]):
            j, blocks = i + 1, 0
            while j < c_end and not re.match(r"^#{1,3}\s", lines[j]):
                blocks += bool(STRATA_BLOCK_RE.match(lines[j]))
                j += 1
            strata_lines = j - i
            if blocks > STRATA_MAX_BLOCKS:
                fails.append(f"GOOD-MORNING.md: strata stack holds {blocks} blocks "
                             f"(max {STRATA_MAX_BLOCKS}) — ritual step 2f")
            break

    for name, (s, e) in sorted(spans.items(), key=lambda kv: kv[1][0]):
        n = e - s
        if name in SECTION_EXEMPT:
            notes.append(f"{name}: {n} lines — EXEMPT by ruling (standing, uncapped): measured "
                         f"and reported, never charged.")
            continue
        if name not in SECTION_CAPS:
            continue
        if name == "§C":
            n -= strata_lines
        warn_at, block_at = SECTION_CAPS[name]
        step = "2e" if name == "DO-FIRST" else "2"
        if n >= block_at:
            fails.append(f"GOOD-MORNING.md {name}: {n} lines, block {block_at} — ritual step {step}")
        elif n > warn_at:
            warns.append(f"GOOD-MORNING.md {name}: {n} lines, cap {warn_at} — ritual step {step}")

    # ---- D7 size stamp: measure first, then check what the file CLAIMS against the measurement
    tk, method = measure_tokens(text)
    a_s, a_e = spans["§A"]
    exempt_tk = measure_tokens("\n".join(lines[a_s:a_e]))[0]
    compactable = tk - exempt_tk
    chain = tk
    ls_path = os.path.join(repo, "_LIVE-STATE.md")
    if os.path.exists(ls_path):
        with open(ls_path, encoding="utf-8") as f:
            chain += measure_tokens(f.read())[0]
    # ⚠ The whole-file figure leads, ALWAYS. The budget excludes §A; the published cost does not.
    # An exclusion that also hides the total would understate exactly the cold-start cost that the
    # D9 measured floor exists to make honest.
    notes.append(f"SIZE measured ({method}): GM {tk} tk WHOLE FILE · of which §A {exempt_tk} tk "
                 f"exempt · compactable {compactable} tk (the budgeted figure) · chain {chain} tk")

    stamp = next((m for m in (SIZE_STAMP_RE.match(ln) for ln in lines[:HEADER_LINES]) if m), None)
    if stamp is None:
        fails.append("GOOD-MORNING.md: no `size:` stamp — ritual step 2")
    else:
        cm = SIZE_TK_RE.search(stamp.group(1))
        if not cm:
            fails.append("GOOD-MORNING.md: `size:` stamp carries no GM figure — ritual step 2")
        else:
            claimed = float(cm.group(1)) * 1000
            if abs(claimed - tk) / max(tk, 1) > SIZE_TOLERANCE:
                fails.append(f"GOOD-MORNING.md: `size:` stamp claims {claimed:.0f} tk, measured "
                             f"{tk} tk — ritual step 2")

    budget = SIZE_BUDGET_TK["compactable"]
    if compactable >= budget * 1.5:
        fails.append(f"GOOD-MORNING.md compactable: {compactable} tk, block "
                     f"{budget * 1.5:.0f} — ritual step 2")
    elif compactable > budget:
        warns.append(f"GOOD-MORNING.md compactable: {compactable} tk, cap {budget} — ritual step 2")
    return fails, warns, notes


def wrap_checks(repo, today, lane=False):
    fails, warns, notes = [], [], []
    iso = today.isoformat()
    targets = [("_LIVE-STATE.md", '"Last refreshed"'), ("GOOD-MORNING.md", "header date")]
    if lane:
        targets = targets[:1]
        notes.append("LANE WRAP (--lane, S-D2): GOOD-MORNING header check SKIPPED — lane "
                     "sessions are ruled outside the GM queue; _LIVE-STATE §🔀 is their "
                     "record and its check still bites.")
        notes.append("LANE WRAP: pre-flight-stamp check SKIPPED too — the stamp lives in "
                     "GOOD-MORNING.md, which lane sessions do not write.")
        notes.append("LANE WRAP: section growth contracts (2e/2f) SKIPPED — same reason. A lane "
                     "session cannot be charged for a file it is ruled out of writing.")
    else:
        gm = os.path.join(repo, "GOOD-MORNING.md")
        if os.path.exists(gm):
            with open(gm, encoding="utf-8") as f:
                f_, w_ = check_preflight(f.read())
            fails += f_
            warns += w_
        f_, w_, n_ = check_budgets(repo)
        fails += f_
        warns += w_
        notes += n_
        notes.append("PRE-FLIGHT stamp: FORM checked only (3 terms · arithmetic · band-vs-table). "
                     "Whether the fill figure is honest, and whether a mid-job re-price actually "
                     "happened, are NOT observable here — discipline, not enforcement "
                     "(_RUNBOOK-context-gauge.md § ★ Half 0b).")
    for fname, label in targets:
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


def run(mode="build", repo=REPO, report=REPORT, today=None, lane=False):
    today = today or datetime.date.today()
    fails, warns, notes = [], [], []
    scoped = in_scope(repo)
    for p in scoped:
        f, w = check_file(p, repo)
        fails += f
        warns += w
    if mode == "wrap":
        report = None  # S-D3: wrap is stdout-only — _CAPTURE-GATE.md belongs to build mode
        f, w, n = wrap_checks(repo, today, lane=lane)
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


# One fixture per pre-flight FAIL class. The first two are the failures ACTUALLY OBSERVED:
# the wrap term omitted (2026-07-27 #2, 58→63) and a band asserted from memory (twice).
PREFLIGHT_FIXTURES = [
    ("missing", "> **COMMIT STATE.** Context gauge at authoring: RED ~72%.\n", True),
    ("two-term (wrap omitted)",
     "pre-flight: fill 38% + job 15% = 53% AMBER · reserve 15% ring-fenced\n", True),
    ("arithmetic does not close",
     "pre-flight: fill 40% + job 12% + wrap 5% = 70% RED · reserve 15% ring-fenced\n", True),
    ("band mis-read (70 called AMBER)",
     "pre-flight: fill 50% + job 15% + wrap 5% = 70% AMBER · reserve 15% ring-fenced\n", True),
    ("band mis-read at the boundary (60 is RED)",
     "pre-flight: fill 40% + job 15% + wrap 5% = 60% AMBER · reserve 15% ring-fenced\n", True),
    ("green control",
     "pre-flight: fill 40% + job 12% + wrap 5% = 57% AMBER · reserve 15% ring-fenced\n", False),
    ("green control, boundary GREEN (44)",
     "pre-flight: fill 30% + job 9% + wrap 5% = 44% GREEN · reserve 15% ring-fenced\n", False),
]


def selftest_preflight():
    """Bite-test the pre-flight FORM check — every class must FAIL, controls must pass."""
    failures = []
    for name, text, should_fail in PREFLIGHT_FIXTURES:
        f_, _ = check_preflight(text, label="fixture")
        if should_fail and not f_:
            failures.append(f"pre-flight [{name}]: expected FAIL, check stayed green — "
                            f"the check does not bite")
        if not should_fail and f_:
            failures.append(f"pre-flight [{name}]: expected green, got {f_}")
    # the band table itself, read not recalled: boundaries are the twice-observed failure
    for total, want in ((44, "GREEN"), (45, "AMBER"), (59, "AMBER"), (60, "RED"), (72, "RED")):
        got = band_for(total)
        if got != want:
            failures.append(f"band_for({total}) = {got}, table says {want}")
    # the reserve must NOT be counted into the sum — if it ever is, the fence became padding
    f_, _ = check_preflight("pre-flight: fill 40% + job 12% + wrap 5% = 72% RED · reserve 15%\n",
                            label="fixture")
    if not f_:
        failures.append("pre-flight: a stamp that ADDED the ring-fenced reserve into its total "
                        "passed — the fence has silently become a fourth addend (runbook § Half "
                        "0b anti-false-fix 1)")
    return failures


FAT = " ".join(f"word{i}" for i in range(120))  # ~200 tk of line, for isolating the SIZE check
#   from the LINE check: a fixture that trips both proves neither (attribute-the-diff).


def _gm_fixture(do_first=10, sec_a=10, sec_c=10, with_b=False, strata_blocks=0,
                strata_pad=0, drop=(), stamp=None, fat_c=0, fat_a=0):
    """Synthetic GOOD-MORNING.md for the budget bites.

    `stamp=None` ⇒ a CORRECT stamp is computed for the finished text, so the green control is
    genuinely green rather than green by omission (attribute-the-diff: a control that passes for
    the wrong reason cannot license the fixtures that fail)."""
    out = ["# Good morning", "SIZESTAMP", ""]
    if "DO-FIRST" not in drop:
        out += ["## ⬛ DO THIS FIRST", ""] + [f"do line {i}" for i in range(do_first)]
    if "§A" not in drop:
        out += ["# §A · ORIENTATION", ""] + [f"a line {i}" for i in range(sec_a)]
        out += [f"{FAT} {i}" for i in range(fat_a)]
    if with_b:
        out += ["# §B · THIS SESSION", "", "b line"]
    if "§C" not in drop:
        out += ["# §C · QUEUE", ""] + [f"c line {i}" for i in range(sec_c)]
        out += [f"{FAT} {i}" for i in range(fat_c)]
        if strata_blocks:
            out.append("### ⏱ SESSION STRATA")
            for b in range(strata_blocks):
                out += [f"#### 2026-07-2{b} #{b}"] + [f"s line {i}" for i in range(strata_pad)]
    body = "\n".join(out) + "\n"
    if stamp is not None:
        return body.replace("SIZESTAMP", stamp)
    text = body.replace("SIZESTAMP", "> **size:** GM 0.00K tk · chain 0.00K tk · measured x")
    for _ in range(3):  # converges: the stamp's own length barely moves the count
        tk, _m = measure_tokens(text)
        text = body.replace("SIZESTAMP", f"> **size:** GM {tk / 1000:.2f}K tk · "
                                         f"chain {tk / 1000:.2f}K tk · measured x")
    return text


# GM-D8(a): "ships with bites — an over-budget fixture must go RED, plus a bite-the-bite."
# The last three entries ARE the bite-the-bite: they prove the gate's *exemptions and exclusions*
# work. A cap that fires on everything is as broken as one that fires on nothing, and only a
# passing control makes a failing fixture mean anything.
BUDGET_FIXTURES = [
    ("DO-FIRST over block (266 ln, real value at ruling)", dict(do_first=266), True),
    ("§C over block",                                      dict(sec_c=260), True),
    ("§B present (D4 deleted it)",                         dict(with_b=True), True),
    ("required marker missing",                            dict(drop=("§C",)), True),
    ("strata stack 2 blocks deep (D5: LATEST only)",       dict(strata_blocks=2, strata_pad=3), True),
    ("no size stamp",                                      dict(stamp="(no stamp here)"), True),
    ("size stamp STALE (claims 0.10K)",
     dict(stamp="> **size:** GM 0.10K tk · chain 0.10K tk · measured x"), True),
    ("size stamp with no K (25618 must not read as 25.6M)",
     dict(stamp="> **size:** GM 25618 tk · chain 1 tk"), True),
    # D7-as-amended: the SIZE budget, isolated from the LINE caps by fat lines rather than many
    # lines — a fixture that trips both checks at once proves neither of them.
    ("compactable over size block (80 fat §C lines, under the LINE cap)",
     dict(sec_c=5, fat_c=80), True),
    ("green control — every region inside contract",       dict(), False),
    ("§A 400 lines — EXEMPT must actually exempt",         dict(sec_a=400), False),
    ("§C over block ONLY via strata — exclusion must hold",
     dict(sec_c=100, strata_blocks=1, strata_pad=200), False),
    # ★ THE BITE FOR DAVE'S 2026-07-27 AMENDMENT. A §A fat enough to blow a whole-file budget on
    # its own must NOT fail, or the exclusion he ruled is decorative. This is the fixture that
    # would have caught the original D7 before it shipped.
    ("§A alone > the whole budget — exclusion must protect it",
     dict(fat_a=90), False),
]


def selftest_budgets():
    """Bite-test the section growth contracts (2e/2f)."""
    failures = []
    with tempfile.TemporaryDirectory() as td:
        for name, kw, should_fail in BUDGET_FIXTURES:
            with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(_gm_fixture(**kw))
            f_, _w, _n = check_budgets(td)
            if should_fail and not f_:
                failures.append(f"budget [{name}]: expected FAIL, gate stayed green — "
                                f"the cap does not bite")
            if not should_fail and f_:
                failures.append(f"budget [{name}]: expected green, got {f_}")
    # The budget number is a RULED value (Dave, 2026-07-27 — D7 amendment). Pin it, so a later
    # convenience edit has to be a deliberate act with a ledger entry behind it rather than a
    # quiet re-dial: promotion of values is Dave's alone (derivation governance).
    if SIZE_BUDGET_TK != {"compactable": 8000}:
        failures.append(f"SIZE_BUDGET_TK = {SIZE_BUDGET_TK}, ruled {{'compactable': 8000}} — "
                        f"re-dialling is Dave's, and updating this pin is part of doing it")
    return failures


def selftest():
    failures = selftest_preflight() + selftest_budgets()
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
        # S-D2 lane-flag bite-test: stale GM must FAIL a plain wrap and be SKIPPED with --lane
        stale = datetime.date(2026, 7, 27)
        with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
            f.write(f"Last refreshed: {stale.isoformat()}\n")
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write("header dated 2026-07-25 (stale)\n")
        f_plain, _, _ = wrap_checks(td, stale, lane=False)
        f_lane, _, n_lane = wrap_checks(td, stale, lane=True)
        if not any("GOOD-MORNING" in x for x in f_plain):
            failures.append("wrap without --lane: stale GM header did not FAIL — check dead")
        if any("GOOD-MORNING" in x for x in f_lane):
            failures.append("--lane still FAILs on GM header — S-D2 flag does not bite")
        if not any("SKIPPED" in x for x in n_lane):
            failures.append("--lane skip is silent — must be noted in output")
        # S-D3 bite-test: a wrap run must NOT write the report file
        rpt = os.path.join(td, "_CG-TEST.md")
        run(mode="wrap", repo=td, report=rpt, today=stale, lane=True)
        if os.path.exists(rpt):
            failures.append("wrap mode wrote a report file — S-D3 clobber fix regressed")
    if failures:
        for x in failures:
            print(f"  ❌ selftest: {x}")
        return 1
    print("  ✅ capture-gate selftest: all failure classes bite; green control passes")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(mode="wrap" if "--wrap" in sys.argv else "build",
                 lane="--lane" in sys.argv))
