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
import hashlib
import importlib
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

# #23 (ruled Dave 2026-07-28): the section-usage probe's tier, routed at ONE call-site line.
# PROMOTED #24 (2026-07-28): O1′ started — the data's consumer arrived — so the ruled trigger
# fired and the flag + its selftest pin flipped together, one deliberate edit pair (M10's
# pattern). A missing/malformed stratum usage line now FAILS the wrap. Vocabulary +
# validation live in _gm_usage.py — the ONLY copy.
SECTION_USAGE_BLOCKING = True

# #25 (Dave, mid-flight 2026-07-28): the KG forcing function — the wrap wants consult
# TESTIMONY (retrieval receipts, or the honest negative). ADVISORY at birth (the M10/#23
# pattern); promotion to BLOCKING is Dave's word, on the probe's record. Flag + its
# selftest pin move only as a pair. Line format + validation live in _search_core.py —
# the ONLY copy (the mover≠gate lesson: imported, never re-implemented).
CONSULT_RECEIPT_BLOCKING = False

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

# ---------------------------------------------------------------- M-set, ruled 2026-07-27 #17
# `notes/_MEMENTO-DECISIONS.md` § ★ M-SET · brief `notes/_briefs/2026-07-27-memento-hardening-brief.md`.
# Three regions that the D7 amendment measured and PUBLISHED but never budgeted. Publishing a
# number nobody is accountable for is how the compactable region reached 21K before anyone looked.
#
# M7 — §A: **WARN ONLY, and it can never block.** GM-D7-am is explicit that §A is uncapped by
#   ruling — Dave's words were "not even a guard banner" — so the FIRST draft of this item (a hard
#   cap) was caught at inscription and revised. Two warn triggers, and the steady state is SILENT:
#     (a) GROWTH — §A is bigger than the last wrap stamped AND no banner line names a §A change;
#     (b) BACKSTOP — an absolute ceiling, so drift accumulated over many wraps still surfaces once.
#   Nothing here may be read as an instruction to trim §A. It reports; Dave rules.
SECTION_A_WARN_TK = 4500   # §A measured 4,208 tk at the ruling (2026-07-27) — headroom is deliberate
STAMP_PRECISION_TK = 100   # the stamp writes §A as `N.NK tk`, so its granularity is 100 tk. Growth
#   below the instrument's own precision is NOT an observation — compare with this slack or every
#   wrap warns on its own rounding ([[measure-dont-convert-units]]: the unit you state in bounds
#   the claim you may make).
SIZE_A_RE = re.compile(r"§A\D{0,12}?([\d.]+)\s*K\s*tk", re.I)   # K REQUIRED, as for GM above
#
# M8 — the BANNER region (file top → the line before DO-FIRST: header + ★ LATEST + ★ PRIOR).
#   It had no budget and is the densest prose in the file. Measured with the EXISTING region
#   parser (`section_spans`) — a second parser is precisely the drift class this block exists to
#   prevent, so if that parser ever cannot isolate the region, this check refuses to measure.
BANNER_BUDGET_TK = (4000, 5000)    # (warn, BLOCK) — measured 2,103 tk at enactment
#
# M10 — the READ CHAIN (GM + _LIVE-STATE.md), the GM-D7-am contract, now actually measured.
#   ⚠ **ADVISORY — it does not block.** RULED by Dave 2026-07-27 #18, after enactment measured the
#   chain at 28,843 tk: already past the 28,000 the M-set had written as a BLOCK, and the brief's
#   own quoted figure (29,193) was too. Both numbers stand exactly as ruled; only the TIER moved,
#   on the M9(a) pattern the brief itself chose — advisory first, promote once seen working.
#   **28,000 is therefore the PROMOTION THRESHOLD, not a stop:** when a wrap measures the chain
#   under it, arm the block. This comment is the only record of that trigger — don't delete it.
#   ⚠ AND the first draft of this check printed "roll _LIVE-STATE deltas (ritual step 2d)" as the
#   remedy. That advice was WRONG and would have sent a reader at a region that cannot pay:
#   measured at enactment, the three retained deltas total 1,422 tk against a 12,694 tk standing
#   body, and LS was ALREADY at its ruled LATEST+2 retention — so the prescribed fix was both
#   unavailable and insufficient. **A budget check reports its measurement; it does not prescribe
#   the region.** (The "gate narrows its own rule" class: the exit code ages well, the advice text
#   does not.)
CHAIN_BUDGET_TK = (24000, 28000)   # (warn, PROMOTION THRESHOLD) — advisory, never blocks

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


# M6 (2026-07-27): a fresh sandbox loses pip state, and tiktoken vanished TWICE inside 24 hours.
# Each time the gate did the honest thing — fell back to bytes/3.53 and SAID so — but a stamp
# measured by estimate is a weaker claim than one measured by the encoder, and nobody noticed
# until the second time. ONE quiet install attempt, at most once per process.
# ⚠ The fallback is NOT touched by this. Auto-heal must never make the estimate path quieter;
# healing is a convenience, the self-description is the contract.
_TIKTOKEN_HEAL_TRIED = False


def _heal_tiktoken():
    """One `pip install tiktoken` attempt per process. True iff the module imports afterwards.
    Never raises and never prints — a failed heal is a non-event, the fallback covers it.
    `CAPTURE_GATE_NO_HEAL=1` suppresses the attempt; that is how the selftest reaches the
    fallback path on a machine where tiktoken IS installed."""
    global _TIKTOKEN_HEAL_TRIED
    if _TIKTOKEN_HEAL_TRIED or os.environ.get("CAPTURE_GATE_NO_HEAL"):
        return False
    _TIKTOKEN_HEAL_TRIED = True
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "tiktoken",
                        "--break-system-packages", "-q"],
                       capture_output=True, timeout=60)
        importlib.invalidate_caches()
        importlib.import_module("tiktoken")
        return True
    except Exception:
        return False


def measure_tokens(text):
    """Returns (tokens, method). tiktoken when present (OBSERVED); otherwise the MEASURED byte
    divisor, labelled ESTIMATE. Both are declared and they are never silently mixed — a number
    whose method is unstated is the thing this gate exists to prevent."""
    try:
        tiktoken = importlib.import_module("tiktoken")
    except Exception:
        if _heal_tiktoken():
            tiktoken = importlib.import_module("tiktoken")
        else:
            return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                    f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)")
    return len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"


# ⚠ §A HASH CONVENTION — PINNED HERE, and this is the only implementation. Recovered the hard way
# at #17, when a wrong-shape probe read `70e61b93…` and cost an abort mid-wrap; `git diff` against
# HEAD is what proved §A had not in fact changed. The digest is taken over the lines from `# §A`
# up to the line BEFORE `# §C`, joined with '\n', plus a TRAILING newline — `999b1e3d…` today.
# M5's mover MUST call this function rather than re-derive the slice: any other shape produces a
# different digest that looks just as authoritative and means nothing.
def section_a_digest(lines, spans):
    """sha256 of §A in the PINNED shape. Raises if the file lacks either marker — a digest over
    a region you could not locate is worse than no digest (it reads as evidence)."""
    return hashlib.sha256(
        ("\n".join(lines[spans["§A"][0]:spans["§C"][0]]) + "\n").encode("utf-8")).hexdigest()


def strata_extent(lines, spans):
    """(#lines, #blocks) of the 2f stratum stack inside §C — the D6(a) exclusion region.
    Extracted from check_budgets at M5 (2026-07-28) so the mover's projected-count guard
    and this gate walk the SAME implementation: two copies of an exclusion is how one of
    them drifts. Behaviour identical to the inline original — the BUDGET_FIXTURES strata
    bites (2-blocks FAIL · exclusion-must-hold control) prove it."""
    if "§C" not in spans:
        return 0, 0
    c_start, c_end = spans["§C"]
    for i in range(c_start, c_end):
        if STRATA_HEAD_RE.match(lines[i]):
            j, blocks = i + 1, 0
            while j < c_end and not re.match(r"^#{1,3}\s", lines[j]):
                blocks += bool(STRATA_BLOCK_RE.match(lines[j]))
                j += 1
            return j - i, blocks
    return 0, 0


def charged_line_counts(lines, spans):
    """{section: line count as the caps CHARGE it} — §C net of the strata exclusion, every
    other section gross. The ONLY implementation of the charging rule: check_budgets reports
    against it and `_gm_move.py` imports it (M5 — the mover must never re-derive what the
    gate charges; a mover charging §C gross would refuse moves the gate permits, which is
    the #19 prose-stricter-than-its-gate failure rebuilt in code)."""
    strata_lines, _blocks = strata_extent(lines, spans)
    return {name: (e - s - strata_lines if name == "§C" else e - s)
            for name, (s, e) in spans.items()}


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
    # Walk lives in strata_extent()/charged_line_counts() since M5 (2026-07-28) — shared
    # with the mover's projected-count guard, behaviour identical (see those docstrings).
    _strata_lines, strata_blocks = strata_extent(lines, spans)
    if strata_blocks > STRATA_MAX_BLOCKS:
        fails.append(f"GOOD-MORNING.md: strata stack holds {strata_blocks} blocks "
                     f"(max {STRATA_MAX_BLOCKS}) — ritual step 2f")

    counts = charged_line_counts(lines, spans)
    for name, (s, e) in sorted(spans.items(), key=lambda kv: kv[1][0]):
        n = counts[name]
        if name in SECTION_EXEMPT:
            notes.append(f"{name}: {n} lines — EXEMPT by ruling (standing, uncapped): measured "
                         f"and reported, never charged.")
            continue
        if name not in SECTION_CAPS:
            continue
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

    # ---- M8: the banner region gets a sub-budget of its own.
    # ⚠ The exclusion of §A is only sound while §A sits BELOW DO-FIRST. If the file is ever
    # reordered, this refuses to measure rather than quietly charge an exempt section to a
    # budget — fail loud on the unknown, never guess (the dv-vocab lesson).
    b_end = spans["DO-FIRST"][0]
    if spans["§A"][0] < b_end:
        fails.append("GOOD-MORNING.md: §A precedes DO-FIRST, so the banner region can no longer "
                     "be isolated from the exempt section — the M8 budget REFUSES to measure "
                     "rather than charge §A. Restore the order, or re-rule the region.")
    else:
        banner_tk = measure_tokens("\n".join(lines[:b_end]))[0]
        b_warn, b_block = BANNER_BUDGET_TK
        notes.append(f"BANNER region: {banner_tk} tk (file top → DO-FIRST: header + ★ LATEST + "
                     f"★ PRIOR) · warn {b_warn} / block {b_block}")
        if banner_tk >= b_block:
            fails.append(f"GOOD-MORNING.md banner region: {banner_tk} tk, block {b_block} — "
                         f"roll a banner to _GM-ARCHIVE.md (ritual step 2c)")
        elif banner_tk > b_warn:
            warns.append(f"GOOD-MORNING.md banner region: {banner_tk} tk, cap {b_warn} — "
                         f"ritual step 2c")

    # ---- M10: the read chain (GM + _LIVE-STATE), the D7 chain contract now measured. ADVISORY.
    c_warn, c_promote = CHAIN_BUDGET_TK
    if chain > c_warn:
        warns.append(f"read chain (GM + _LIVE-STATE): {chain} tk, cap {c_warn} tk — ADVISORY "
                     f"(blocking arms once a wrap measures it under {c_promote}). Measure both "
                     f"files before picking a region to trim: this check knows the total, not "
                     f"where the weight sits, and the deltas are rarely where it sits.")

    # ---- M7: §A size line — WARN ONLY, growth-triggered. It can never block and never orders
    # a trim; GM-D7-am ("not even a guard banner") is honoured by the SILENCE of the steady state.
    a_claim = SIZE_A_RE.search(stamp.group(1)) if stamp else None
    if a_claim is None:
        notes.append(f"§A baseline UNSET: the `size:` stamp carries no §A figure, so growth "
                     f"cannot be observed this wrap. Measured {exempt_tk} tk — stamp it "
                     f"(`§A N.NK tk`) to arm the growth trigger. Unset, not assumed clean.")
    else:
        claimed_a = float(a_claim.group(1)) * 1000
        # ⚠ The suppressor must read the banner PROSE, not the size stamp — once §A is stamped,
        # the stamp itself contains the string "§A" on every single wrap, which would suppress
        # the trigger permanently and silently. Caught by its own bite at enactment.
        banner_names_a = any("§A" in ln and not SIZE_STAMP_RE.match(ln)
                             for ln in lines[:spans["DO-FIRST"][0]])
        if exempt_tk - claimed_a > STAMP_PRECISION_TK and not banner_names_a:
            warns.append(f"§A grew {claimed_a:.0f} → {exempt_tk} tk and no banner line names a "
                         f"§A change — say what changed in the ★ LATEST banner, or re-stamp. "
                         f"WARN ONLY: §A is uncapped by ruling and this can never force a trim.")
    if exempt_tk > SECTION_A_WARN_TK:
        warns.append(f"§A {exempt_tk} tk, past the {SECTION_A_WARN_TK} tk backstop — ADVISORY. "
                     f"§A is uncapped by ruling (GM-D7-am); this is a look-at-it, never a "
                     f"trim order.")
    return fails, warns, notes


def _norm(text):
    """Strip blockquote/list chrome and collapse whitespace. Comparing NORMALISED regions rather
    than lines is what makes the receipts proxy rewrap-immune: re-flowing a paragraph moves every
    line boundary but preserves the character sequence, so a rewrap produces no removals and a
    genuine deletion still does."""
    text = re.sub(r"(?m)^[>\s]*(?:[-*·]\s+)?", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def retirement_receipts(repo):
    """M9 — BLOCKING in wrap mode (ruled Dave 2026-07-28 #22) — a PROXY for 2e's retirement
    tests, and naming that is the whole point.

    2e says a retired DO-FIRST notice is archived verbatim. The gate cannot see 2e's actual
    tests (they key on live targets, elapsed terms and struck sources, none of which are in
    these files) and it cannot see whether a move was verbatim. It observes exactly one thing:
    a line left DO-FIRST since HEAD and no text in `_GM-ARCHIVE.md` carries it.

    Advisory first per the brief; SEEN WORKING at #18 (fired and was right — "this is the
    seeing"); PROMOTED by Dave at #22. The known limit STANDS: it sees text vanish, not
    retirement-DUE, so a false fire is possible on a correct wrap — the answer is archive the
    line (or say why no receipt is owed) and re-run the wrap, one visible beat, no lost work."""
    warns, notes = [], []
    gm = os.path.join(repo, "GOOD-MORNING.md")
    arch = os.path.join(repo, "_GM-ARCHIVE.md")
    if not (os.path.exists(gm) and os.path.exists(arch)):
        return warns, notes
    try:
        r = subprocess.run(["git", "-C", repo, "show", "HEAD:GOOD-MORNING.md"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            notes.append("retirement receipts: no HEAD copy of GOOD-MORNING.md — check skipped "
                         "(this is the honest skip, not a pass)")
            return warns, notes
        old_lines = r.stdout.splitlines()
    except Exception as e:
        notes.append(f"retirement receipts: skipped ({e}) — not a pass")
        return warns, notes

    with open(gm, encoding="utf-8") as f:
        new_lines = f.read().splitlines()
    old_spans, new_spans = section_spans(old_lines), section_spans(new_lines)
    if "DO-FIRST" not in old_spans or "DO-FIRST" not in new_spans:
        notes.append("retirement receipts: DO-FIRST marker absent one side — check skipped")
        return warns, notes
    region = lambda ls, sp: ls[sp["DO-FIRST"][0]:sp["DO-FIRST"][1]]
    new_norm = _norm("\n".join(region(new_lines, new_spans)))
    with open(arch, encoding="utf-8") as f:
        arch_norm = _norm(f.read())

    orphans = []
    for ln in region(old_lines, old_spans):
        n = _norm(ln)
        if not re.search(r"[A-Za-z0-9]", n) or n in new_norm:
            continue
        if n not in arch_norm:
            orphans.append(ln.strip()[:90])
    if orphans:
        warns.append(f"retirement receipts (BLOCKING, Dave #22): {len(orphans)} DO-FIRST line(s) left the "
                     f"worklist since HEAD with no matching text in _GM-ARCHIVE.md — archive "
                     f"them verbatim (ritual step 2c/2e) or say why they needed no receipt. "
                     f"First: “{orphans[0]}”")
    else:
        notes.append("retirement receipts: every DO-FIRST line removed since HEAD is findable "
                     "in _GM-ARCHIVE.md (proxy — verbatim-ness and retirement-DUE are not "
                     "observable here).")
    return warns, notes


def section_usage_probe(repo):
    """#23 (ruled Dave 2026-07-28, lane 1 step 2): the session stratum carries a
    `section-usage` line (U/R/C testimony, FORM-checked only — honesty stays the
    session's, the pre-flight-stamp precedent) and a `section-sizes` line
    (code-measured). Accumulated in _GAUGE-LOG.md as strata roll, usage × size is the
    dataset LS-trim-vs-defer (P4b) and the JIT premise wait on. Tier routed at the call
    site by SECTION_USAGE_BLOCKING (promoted to BLOCKING at O1′ start, #24 — the #23
    trigger); the note below reads the flag so this text cannot age."""
    issues, notes = [], []
    gm = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm):
        return issues, notes
    with open(gm, encoding="utf-8") as f:
        lines = f.read().splitlines()
    idx = next((i for i, ln in enumerate(lines) if STRATA_HEAD_RE.match(ln)), None)
    if idx is None:
        notes.append("section-usage: strata marker absent — probe skipped (honest skip, "
                     "not a pass)")
        return issues, notes
    try:
        sys.path.insert(0, HERE)
        import _gm_usage
    except Exception as e:
        issues.append(f"section-usage: _gm_usage.py unimportable ({e}) — probe cannot run; "
                      f"fix it, never close blind")
        return issues, notes
    issues += _gm_usage.validate_stratum("\n".join(lines[idx:]))
    if not issues:
        notes.append("section-usage: stratum carries well-formed usage + sizes lines "
                     "(FORM only — whether a C is honest is not observable here).")
    notes.append("section-usage tier: %s (read from SECTION_USAGE_BLOCKING — #23 ruled the "
                 "trigger, #24 fired it; flag + selftest pin move only as a pair)."
                 % ("BLOCKING" if SECTION_USAGE_BLOCKING else "ADVISORY"))
    return issues, notes


def index_freshness_check(repo):
    """#32 — RETRIEVAL MUST NOT SERVE A PREVIOUS SESSION'S RECORD.

    Measured at #32's opener: `_memento_search.py --fetch gm:LATEST` returned **#29's
    banner** while the file carried #31's. Cause chain, all three links verified against
    the repo rather than reasoned about:
      1. the index regenerates in `_build_all.py` — but the WRAP rewrites GM/LS *after*
         the session's last build, so retrieval is structurally one session behind;
      2. the index could not regenerate at all: #30's ds-022 repair wrote a `#### ` block
         in a form `_build_memento_index.py` refuses, so the step exited 1;
      3. `_build_all.py` was therefore RED for two sessions and BOTH wraps committed over
         it, because **the wrap gate does not run the build**.

    So this check is not "is the index tidy" — it is the gate that closes link 3. It
    rebuilds the records IN-PROCESS (no subprocess: the sandbox call-boundary lesson) and
    byte-compares against what is on disk. Stale ⇒ FAIL with the one command that fixes it.

    ⚠ Deliberately NOT an mtime comparison. mtimes are reset by any checkout and would
    read GREEN on a file that had been reverted — the DV-D17 shape, where a test that can
    only see absence passes a full revert. Content is the only honest witness."""
    fails, notes = [], []
    try:
        sys.path.insert(0, HERE)
        import _build_memento_index as bmi
    except Exception as e:
        fails.append(f"retrieval index: _build_memento_index.py unimportable ({e}) — the "
                     f"freshness check cannot run; fix it, never close blind")
        return fails, notes
    try:
        records, errors = bmi.build_records()
    except Exception as e:
        fails.append(f"retrieval index: rebuild raised ({e}) — retrieval is unverifiable "
                     f"this wrap")
        return fails, notes
    if errors:
        fails.append("retrieval index: the corpus REFUSES to index — %s%s · run "
                     "`python3 knowledge/_build_memento_index.py` and fix the source. "
                     "(This is exactly how the build went red at #30 and stayed red.)"
                     % (errors[0], "" if len(errors) == 1 else f" (+{len(errors) - 1} more)"))
        return fails, notes
    if not os.path.exists(bmi.OUT_PATH):
        fails.append("retrieval index: ABSENT — every `_memento_search.py` call this "
                     "session was unbacked; run `python3 knowledge/_build_memento_index.py`")
        return fails, notes
    with open(bmi.OUT_PATH, encoding="utf-8") as f:
        on_disk = f.read()
    if bmi.render(records) != on_disk:
        fails.append("retrieval index is STALE — it does not match GOOD-MORNING.md / "
                     "_LIVE-STATE.md as they now stand, so `_memento_search.py` is serving "
                     "a PREVIOUS session's record. Run "
                     "`python3 knowledge/_build_memento_index.py` and stage the result "
                     "(ritual step 2g). This is the #32 defect — do not close over it.")
    else:
        notes.append("retrieval index: FRESH — %d records byte-match the live corpus, so "
                     "retrieval-first quotes this session's truth." % len(records))
    return fails, notes


def consult_receipt_probe(repo):
    """#25 (Dave, mid-flight — the KG forcing function, floated 2026-07-27, scoped into
    O2′ by him): the session stratum carries a `consult-receipts` line — the queries run
    this window with their retrieved ids (`"query" → id · id ; …`), or the honest
    negative (`none — <why>`). FORM-checked only (the section-usage / pre-flight-stamp
    precedent — whether the queries were actually run stays the session's honesty).
    Format + validation IMPORTED from _search_core.py — the only copy."""
    issues, notes = [], []
    gm = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm):
        return issues, notes
    with open(gm, encoding="utf-8") as f:
        lines = f.read().splitlines()
    idx = next((i for i, ln in enumerate(lines) if STRATA_HEAD_RE.match(ln)), None)
    if idx is None:
        notes.append("consult-receipts: strata marker absent — probe skipped (honest skip, "
                     "not a pass)")
        return issues, notes
    try:
        sys.path.insert(0, HERE)
        import _search_core
    except Exception as e:
        issues.append(f"consult-receipts: _search_core.py unimportable ({e}) — probe cannot "
                      f"run; fix it, never close blind")
        return issues, notes
    hits = []
    for i, ln in enumerate(lines[idx:], start=idx):
        m = _search_core.RECEIPT_LINE_RE.match(ln)
        if m:
            hits.append((i, m))
    if not hits:
        issues.append("consult-receipts: stratum carries NO consult-receipts line — the KG "
                      "forcing function (#25) wants testimony: `> **consult-receipts #N:** "
                      "\"query\" → id · id` or `none — <why>`")
    for i, m in hits:
        for e in _search_core.validate_receipt_payload(m.group(2)):
            issues.append(f"consult-receipts (line {i + 1}): {e}")
    if hits and not issues:
        notes.append("consult-receipts: stratum carries well-formed testimony (FORM only — "
                     "whether the queries were run is not observable here).")
    notes.append("consult-receipts tier: %s (read from CONSULT_RECEIPT_BLOCKING — #25 born "
                 "ADVISORY; promotion is Dave's word, flag + pin move as a pair)."
                 % ("BLOCKING" if CONSULT_RECEIPT_BLOCKING else "ADVISORY"))
    return issues, notes


def lane_routing_check(repo):
    """O1′ #24 (ruled Dave, option-select ×4 all recommended): the eager GM §C·1 ROUTING
    line must AGREE with knowledge/_lanes.json — drift between the eager line and the
    records is the confident-false-inscription class, so it FAILS the wrap (BLOCKING by
    ruling, pick 3). All logic lives in _gen_lanes.py and is IMPORTED — one implementation,
    never a second copy (the mover≠gate lesson)."""
    fails, notes = [], []
    gm = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm):
        return fails, notes
    sys.path.insert(0, HERE)
    try:
        import _gen_lanes
    except Exception as e:
        return [f"lane-routing: _gen_lanes.py unimportable ({e}) — check cannot run; "
                f"fix it, never close blind"], notes
    lanes, errs = _gen_lanes.load_lanes()
    if errs:
        return [f"lane-routing: records invalid — {e}" for e in errs], notes
    with open(gm, encoding="utf-8") as f:
        issues = _gen_lanes.check_routing_line(f.read(), lanes)
    fails += [f"lane-routing: {i}" for i in issues]
    if not fails:
        notes.append(f"lane-routing: GM eager ROUTING line agrees with {len(lanes)} lane "
                     f"records (BLOCKING — O1′ #24; records are the truth).")
    return fails, notes


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
        notes.append("LANE WRAP: section growth contracts (2e/2f), the banner/§A/chain budgets, "
                     "the retirement-receipts proxy, the section-usage probe, the "
                     "consult-receipt probe and the lane-routing check are all SKIPPED — same "
                     "reason. A lane session cannot be charged for a file it is ruled out of "
                     "writing.")
        notes.append("LANE WRAP: the #32 retrieval-index freshness check is SKIPPED — a lane "
                     "session does not write GM/LS, so it cannot stale the index. ⚠ If lanes "
                     "ever gain a write path into either file, this exemption must go with it.")
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
        f_, n_ = retirement_receipts(repo)      # M9 — receipts proxy, BLOCKING (Dave #22)
        fails += f_
        notes += n_
        i_, n_ = section_usage_probe(repo)      # #23 built · #24 BLOCKING (tier = this line)
        (fails if SECTION_USAGE_BLOCKING else warns).extend(i_)
        notes += n_
        i_, n_ = consult_receipt_probe(repo)    # #25 — KG forcing function, ADVISORY at birth
        (fails if CONSULT_RECEIPT_BLOCKING else warns).extend(i_)
        notes += n_
        f_, n_ = index_freshness_check(repo)     # #32 — retrieval must not serve a stale record
        fails += f_                              # BLOCKING at birth: the failure it catches
        notes += n_                              # (build red, unnoticed) already cost 2 sessions
        f_, n_ = lane_routing_check(repo)       # O1′ #24 — eager line ↔ records, BLOCKING
        fails += f_
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
                strata_pad=0, drop=(), stamp=None, fat_c=0, fat_a=0,
                fat_banner=0, banner_extra=None, stamp_a=None, ls_text=None):
    """Synthetic GOOD-MORNING.md for the budget bites.

    `stamp=None` ⇒ a CORRECT stamp is computed for the finished text, so the green control is
    genuinely green rather than green by omission (attribute-the-diff: a control that passes for
    the wrong reason cannot license the fixtures that fail).

    M-set additions: `fat_banner` grows the banner region (M8) · `banner_extra` injects a banner
    line, which is how the M7 growth trigger's "a banner names §A" suppressor is bitten ·
    `stamp_a` overrides the stamped §A figure (a float to claim one, `False` to omit it)."""
    out = ["# Good morning", "SIZESTAMP", ""]
    if banner_extra:
        out.append(banner_extra)
    out += [f"{FAT} banner {i}" for i in range(fat_banner)]
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
    # the §A figure the stamp will CLAIM: measured by default, so the control is silent under the
    # M7 growth trigger for the right reason rather than because the trigger is unarmed.
    b_lines = body.splitlines()
    b_spans = section_spans(b_lines)
    if stamp_a is None and {"§A", "§C"} <= set(b_spans):
        a_s, a_e = b_spans["§A"]
        stamp_a = measure_tokens("\n".join(b_lines[a_s:a_e]))[0] / 1000
    a_part = "" if stamp_a in (None, False) else f"§A {stamp_a:.2f}K tk · "
    text = body.replace("SIZESTAMP", "> **size:** GM 0.00K tk · chain 0.00K tk · measured x")
    for _ in range(3):  # converges: the stamp's own length barely moves the count
        tk, _m = measure_tokens(text)
        text = body.replace("SIZESTAMP", f"> **size:** GM {tk / 1000:.2f}K tk · {a_part}"
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


# ---------------------------------------------------------------- M-set bites (2026-07-27 #18)
# Every check added by the M-set ships a bite that PROVES IT FIRES, plus the control that proves
# it stays quiet — one without the other licenses nothing. Two of these (M7 growth, M8 banner)
# are WARN-level, so they cannot ride on `selftest_budgets`, which inspects fails only; adding a
# fourth tuple element there would have churned a ruled fixture table for no gain.
def _warns_for(td, **kw):
    with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
        f.write(_gm_fixture(**kw))
    f_, w_, n_ = check_budgets(td)
    return f_, w_, n_


def selftest_growth():
    """Bite-test M6 (tiktoken heal/fallback) · M7 (§A warn) · M8 (banner) · M10 (chain) ·
    the pinned §A digest · M9 (retirement receipts)."""
    failures = []

    # ---- M6: the fallback must stay REACHABLE and must still describe itself as an ESTIMATE.
    saved, os.environ["CAPTURE_GATE_NO_HEAL"] = os.environ.get("CAPTURE_GATE_NO_HEAL"), "1"
    sys.modules["tiktoken"] = None          # makes `import tiktoken` raise, as a missing module does
    try:
        n, method = measure_tokens("hello world " * 50)
        if "ESTIMATE" not in method or "tiktoken absent" not in method:
            failures.append(f"M6: with tiktoken absent the method read {method!r} — the fallback "
                            f"must keep saying it is an estimate")
        if n <= 0:
            failures.append("M6: fallback returned a non-positive count")
    finally:
        del sys.modules["tiktoken"]
        if saved is None:
            os.environ.pop("CAPTURE_GATE_NO_HEAL", None)
        else:
            os.environ["CAPTURE_GATE_NO_HEAL"] = saved
    if measure_tokens("hello")[1] == "tiktoken cl100k_base":
        pass                                 # healthy env: the OBSERVED path is the one in use
    elif "ESTIMATE" not in measure_tokens("hello")[1]:
        failures.append("M6: measure_tokens returned an undeclared method")

    with tempfile.TemporaryDirectory() as td:
        # ---- M8: banner budget — fires at warn, fires at block, silent for a normal banner.
        # FAT measures 240 tk/line, so 17 lines ≈ 4.1K (warn band) and 30 ≈ 7.3K (block). The
        # numbers are MEASURED, not assumed: the first draft guessed ~200 tk/line, put the warn
        # fixture at 5.4K, and bit as a block instead.
        _f, w, _n = _warns_for(td, fat_banner=17)
        if not any("banner region" in x for x in w):
            failures.append("M8: a 17-fat-line banner did not WARN — the sub-budget does not bite")
        f, _w, _n = _warns_for(td, fat_banner=30)
        if not any("banner region" in x for x in f):
            failures.append("M8: a 30-fat-line banner did not BLOCK")
        _f, w, _n = _warns_for(td)
        if any("banner region" in x for x in w):
            failures.append("M8: an ordinary banner warned — the budget fires on everything")

        # ---- M10: chain budget, ADVISORY. The fixture repo has no _LIVE-STATE, so chain == GM.
        f, w, _n = _warns_for(td, fat_c=5, fat_a=160)
        if not any("read chain" in x for x in w):
            failures.append("M10: an over-cap chain did not WARN — the budget does not bite")
        if any("read chain" in x for x in f):
            failures.append("M10: a chain finding reached FAILS — Dave ruled it ADVISORY "
                            "(2026-07-27 #18); blocking arms only once a wrap measures the "
                            "chain under the promotion threshold")
        _f, w, _n = _warns_for(td)
        if any("read chain" in x for x in w):
            failures.append("M10: a small chain warned — the budget fires on everything")
        # the remedy text must NOT prescribe a region: measured at enactment, the deltas the old
        # text pointed at could not have paid the difference. Pin the correction.
        _f, w, _n = _warns_for(td, fat_c=5, fat_a=160)
        if any("step 2d" in x for x in w if "read chain" in x):
            failures.append("M10: the chain warn prescribes rolling deltas again — it knows the "
                            "total, not where the weight sits")

        # ---- M7: §A. WARN-ONLY is the ruling, so a §A fixture must never appear in `fails`.
        _f, w, _n = _warns_for(td, fat_a=30)          # ~6K tk of §A, past the 4,500 backstop
        if not any("backstop" in x for x in w):
            failures.append("M7: §A past the backstop did not warn")
        f, _w, _n = _warns_for(td, fat_a=30)
        if any("§A" in x for x in f):
            failures.append("M7: a §A finding reached FAILS — the ruling is WARN-ONLY and "
                            "'not even a guard banner' (GM-D7-am). It may never block.")
        # growth: stamp claims less than §A measures, and no banner line mentions §A
        _f, w, _n = _warns_for(td, sec_a=40, stamp_a=0.01)
        if not any("grew" in x for x in w):
            failures.append("M7: §A growth against a smaller stamped baseline did not warn")
        # …and the suppressor: a banner line that NAMES §A must silence it (steady state = quiet)
        _f, w, _n = _warns_for(td, sec_a=40, stamp_a=0.01,
                               banner_extra="> ★ LATEST — §A rewritten this session")
        if any("grew" in x for x in w):
            failures.append("M7: a banner naming §A did not suppress the growth warn — the "
                            "trigger will wallpaper the header")
        # …and an ABSENT §A figure must be reported UNSET, never assumed clean
        _f, _w, n = _warns_for(td, stamp_a=False)
        if not any("baseline UNSET" in x for x in n):
            failures.append("M7: a stamp with no §A figure passed silently — unknown must be "
                            "declared, never defaulted")

        # ---- the PINNED §A digest: right shape reproduces, wrong shape does not.
        text = _gm_fixture()
        lines = text.splitlines()
        spans = section_spans(lines)
        want = hashlib.sha256(
            ("\n".join(lines[spans["§A"][0]:spans["§C"][0]]) + "\n").encode()).hexdigest()
        if section_a_digest(lines, spans) != want:
            failures.append("§A digest: does not match the PINNED shape (§A → line before §C, "
                            "'\\n'.join, trailing newline)")
        wrong = hashlib.sha256("\n".join(lines[spans["§A"][0]:spans["§C"][0]]).encode()).hexdigest()
        if wrong == want:
            failures.append("§A digest: the trailing-newline variant collides — the bite cannot "
                            "tell the shapes apart, so it proves nothing")

    # ---- M9: the receipts proxy needs a real git repo, so it gets its own fixture.
    with tempfile.TemporaryDirectory() as td:
        git = ["git", "-C", td, "-c", "user.email=t@t", "-c", "user.name=t"]
        try:
            if subprocess.run(git[:3] + ["init", "-q"], capture_output=True,
                              timeout=30).returncode != 0:
                raise RuntimeError("git init failed")
            with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(_gm_fixture(do_first=6))
            open(os.path.join(td, "_GM-ARCHIVE.md"), "w", encoding="utf-8").write("# archive\n")
            subprocess.run(git + ["add", "-A"], capture_output=True, timeout=30)
            subprocess.run(git + ["commit", "-qm", "fixture"], capture_output=True, timeout=30)
            # remove a DO-FIRST line, archive NOTHING -> the proxy must warn
            with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(_gm_fixture(do_first=6).replace("do line 3\n", ""))
            w, _n = retirement_receipts(td)
            if not any("retirement receipts" in x for x in w):
                failures.append("M9: a DO-FIRST line vanished with no archive text and the proxy "
                                "stayed quiet")
            # now archive it -> the proxy must go quiet (else it fires on everything)
            open(os.path.join(td, "_GM-ARCHIVE.md"), "a", encoding="utf-8").write("do line 3\n")
            w, _n = retirement_receipts(td)
            if any("retirement receipts" in x for x in w):
                failures.append("M9: an archived line still warned — the receipt is not read")
            # a pure REWRAP must produce no removals at all (the normalisation's whole job)
            with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(_gm_fixture(do_first=6).replace("do line 4\ndo line 5",
                                                        "do line 4 do\nline 5"))
            w, _n = retirement_receipts(td)
            if any("retirement receipts" in x for x in w):
                failures.append("M9: a rewrap read as a retirement — the proxy is line-shaped, "
                                "not content-shaped, and will cry wolf every compaction")
        except Exception as e:
            failures.append(f"M9: bite could not run ({e}) — an untested check must not ship")

    # ---- RULED VALUES, pinned (same discipline as SIZE_BUDGET_TK). Promotion of values is
    # Dave's alone, so a convenience re-dial has to be a deliberate act with a ledger line behind
    # it. The chain pin covers the TIER as much as the numbers: re-arming M10's block before a
    # wrap has measured the chain under 28,000 would reverse a ruling by editing a tuple.
    for name, got, want in (("CHAIN_BUDGET_TK", CHAIN_BUDGET_TK, (24000, 28000)),
                            ("BANNER_BUDGET_TK", BANNER_BUDGET_TK, (4000, 5000)),
                            ("SECTION_A_WARN_TK", SECTION_A_WARN_TK, 4500)):
        if got != want:
            failures.append(f"{name} = {got}, ruled {want} (2026-07-27 M-set) — re-dialling is "
                            f"Dave's, and updating this pin is part of doing it")
    return failures


def selftest_usage():
    """#23 — the section-usage probe fires on missing/malformed and stays quiet on good
    (tier-agnostic, the M9 selftest's shape), plus the tier pin (M10's pattern)."""
    failures = []
    sys.path.insert(0, HERE)
    try:
        import _gm_usage
    except Exception as e:
        return [f"usage: _gm_usage unimportable in selftest ({e})"]
    good = (_gm_usage.GOOD_USAGE +
            "\n> **section-sizes #23 (t):** GM HDR:1 · LS HDR:1")
    if _gm_usage.validate_stratum(good):
        failures.append("usage: good stratum must stay quiet")
    if not any("MISSING" in i for i in _gm_usage.validate_stratum("> nothing here")):
        failures.append("usage: missing line must fire")
    if not any("MALFORMED" in i for i in _gm_usage.validate_stratum(
            good.replace("SPIN:R", "SPIN:X"))):
        failures.append("usage: malformed line must fire, and say MALFORMED")
    if not SECTION_USAGE_BLOCKING:
        failures.append("usage tier pin: SECTION_USAGE_BLOCKING is False but the ruled tier "
                        "is BLOCKING since O1′ started (#24, the #23 trigger fired) — a "
                        "demotion is a ruling; flip flag AND this pin together (one "
                        "deliberate pair)")
    return failures


def selftest_lanes():
    """O1′ #24 — the lane-routing check's dependency FIRES from this harness (drift and
    missing-line must fail; good fixture stays quiet). The deep refusal bites live in
    `_gen_lanes.py --selftest` (its own build step) — this proves the gate's import path."""
    failures = []
    sys.path.insert(0, HERE)
    try:
        import _gen_lanes
    except Exception as e:
        return [f"lanes: _gen_lanes unimportable in selftest ({e})"]
    fx = [{"id": "lane-x", "name": "X", "state": "active", "born": "#1", "until": "u",
           "blocked_by": [], "receipts": "r", "sequence": []}]
    good_gm = "**⛔ ROUTING (records: knowledge/_lanes.json): ACTIVE lane-x.**"
    if _gen_lanes.check_routing_line(good_gm, fx):
        failures.append("lanes: good routing fixture must stay quiet")
    if not _gen_lanes.check_routing_line("no routing here", fx):
        failures.append("lanes: missing routing line must fire")
    if not _gen_lanes.check_routing_line(good_gm.replace("ACTIVE", "BLOCKED"), fx):
        failures.append("lanes: state drift must fire")
    return failures


def selftest_receipts():
    """#25: the consult-receipt probe's failure classes bite, and the tier pin holds."""
    failures = []
    if CONSULT_RECEIPT_BLOCKING is not False:
        failures.append("receipts: CONSULT_RECEIPT_BLOCKING pin — expected False (ADVISORY "
                        "at birth, #25); a flip must land WITH its ruled promotion and "
                        "update this pin in the same edit (the M10 pattern)")
    try:
        sys.path.insert(0, HERE)
        import _search_core
    except Exception as e:
        return failures + [f"receipts: _search_core unimportable in selftest ({e})"]
    if _search_core.validate_receipt_payload(
            '"two lanes" → ledger:two-lanes · lane:lane-1-memento'):
        failures.append("receipts: known-good payload refused — validator broken")
    if not _search_core.validate_receipt_payload("none"):
        failures.append("receipts: bare `none` passed — the honest-negative bite is dead")
    with tempfile.TemporaryDirectory() as td:
        gm = os.path.join(td, "GOOD-MORNING.md")
        base = "# GM\n### ⏱ SESSION STRATA\n\n#### 2026-07-28 #25\n"
        with open(gm, "w", encoding="utf-8") as f:
            f.write(base)
        i_, _ = consult_receipt_probe(td)
        if not any("NO consult-receipts" in x for x in i_):
            failures.append("receipts: missing stratum line did not raise — probe dead")
        with open(gm, "w", encoding="utf-8") as f:
            f.write(base + "> **consult-receipts #25:** none — selftest fixture window\n")
        i_, _ = consult_receipt_probe(td)
        if i_:
            failures.append(f"receipts: well-formed honest negative raised: {i_}")
        with open(gm, "w", encoding="utf-8") as f:
            f.write(base + "> **consult-receipts #25:** \"query with no ids\" → \n")
        i_, _ = consult_receipt_probe(td)
        if not i_:
            failures.append("receipts: malformed payload (empty ids) passed — bite dead")
    return failures


def selftest_index_freshness():
    """#32 — four bites, and the FIRST one is the load-bearing pair.

    A check that only ever reports failure passes a revert that deletes it (the DV-D17
    lesson, and the reason ds-019 was withdrawn). So bite 1 asserts the check goes GREEN
    on a fresh index AND says so in its notes: delete the comparison and bite 1 dies with
    it, not just bites 2-4."""
    print("\n-- index freshness (#32) --")
    failures = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] index-freshness: {name}")
        if not cond:
            failures.append(f"index-freshness: {name}")

    sys.path.insert(0, HERE)
    import _build_memento_index as bmi
    real_build, real_out = bmi.build_records, bmi.OUT_PATH
    recs = [{"id": "x", "kind": "k", "file": "f", "line": 1, "head": "h", "text": "t"}]
    try:
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "idx.json")
            bmi.OUT_PATH = p
            bmi.build_records = lambda: (list(recs), [])
            with open(p, "w", encoding="utf-8") as f:
                f.write(bmi.render(recs))
            f_, n_ = index_freshness_check(td)
            bite("FRESH index passes and reports it (the detectable-when-present half)",
                 not f_ and any("FRESH" in x for x in n_))
            with open(p, "w", encoding="utf-8") as f:
                f.write(bmi.render([dict(recs[0], head="a PREVIOUS session's head")]))
            f_, _ = index_freshness_check(td)
            bite("STALE index fails — the #32 defect itself",
                 any("STALE" in x for x in f_))
            os.remove(p)
            f_, _ = index_freshness_check(td)
            bite("ABSENT index fails", any("ABSENT" in x for x in f_))
            with open(p, "w", encoding="utf-8") as f:
                f.write(bmi.render(recs))
            bmi.build_records = lambda: ([], ["notes/_GAUGE-LOG.md:219: `#### ` block outside"])
            f_, _ = index_freshness_check(td)
            bite("corpus REFUSAL fails and names the offending source (the #30 case)",
                 any("REFUSES to index" in x and "_GAUGE-LOG" in x for x in f_))
    finally:
        bmi.build_records, bmi.OUT_PATH = real_build, real_out
    return failures


def selftest():
    failures = (selftest_preflight() + selftest_budgets() + selftest_growth()
                + selftest_usage() + selftest_lanes() + selftest_receipts()
                + selftest_index_freshness())
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
