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

# ------------------------------------------------------------------- ds-023 — THE BAND
# ★★ RE-STATED BY DAVE #36: THIS IS A BAND, NOT A CEILING — and 45 was NEVER a ceiling. The
# `FAIL at >= 45` this file shipped from #31 to #36 was the OPPOSITE of what he wanted: the
# gate was refusing the very zone it existed to steer sessions into.
#
# HIS WORDS, #36: "the whole 45% was a misunderstanding, it just creates the band, between 45
# and 60, that I'd prefer the full price with wrap to sit in" · "hitting around 60% every time
# for the full price I can live with, it's safe-ish" · 63 tolerable, RARE, and MARKED.
#
# ⚠ THE UNIT IS THE FULL PRICE — "front-load + context GM + job + wrap", his enumeration. The
# wrap is INSIDE the number, which is why landing at ~60 is safe rather than reckless: at 60
# the wrap has already been PAID, not merely scheduled. That is the property the old `< 45`
# derivation was reaching for — and it bought it twice, once in the arithmetic and once again
# in the threshold, which is exactly how 15 points of margin went missing.
#
# ⚠ WHERE THE OLD RULE CAME FROM, because the provenance IS the lesson. Dave ruled the NUMBER
# at #31; a DELEGATED AGENT picked FAIL as its enforcement. #34's `<= 45` -> `< 45` sharpening
# settled which SIDE of 45 counts, never whether 45 BLOCKS. So nobody ever ruled the block.
# Its cost: an honestly-priced job landing in the low 50s — THE INTENDED ZONE — had either to
# mark a `RESERVE SPEND` receipt for a spend that was never over budget, or be quietly
# under-priced to fit. ds-023's own escape-hatch note (below) names under-pricing as the thing
# it exists to prevent; the enforcement was manufacturing it. **warn != block.**
#
# THE SHAPE NOW:
#     <  45        below the band — allowed, and NOTED. Chronic under-pricing is the documented
#                  failure this band replaced, not a virtue.
#     45 .. 60     ★ THE PREFERRED BAND. Passes clean. This is the TARGET, not the tolerance.
#     61 .. 63     tolerable, but RARE and MARKED — needs `RESERVE SPEND — forked to Dave`.
#     >  63        ⚠ UNRULED BY DAVE. The pre-#36 escape-hatch SHAPE is preserved rather than
#                  replaced (marked -> WARN, unmarked -> FAIL), precisely because inventing a
#                  fresh enforcement here would repeat #31's mistake in the same file.
#                  FORKED TO DAVE at #37 — see `_DS-IMPROVEMENTS.md` ds-023.
#
# In flight the stop-and-wrap trigger is still 60 MINUS THE PRICED WRAP, and it MOVES WITH THE
# WRAP PRICE. A session with an expensive wrap must stop earlier; that is the whole mechanism.
BAND_FLOOR = 45          # Dave #36 — the PREFERRED BAND's floor. NOT a ceiling. Never was one.
HARD_STOP = 60           # Dave's, ratified #30, re-affirmed #36 as "the line" — and LIVABLE
MARKED_MAX = 63          # Dave #36 — "tolerable, rare, marked". Above this is UNRULED.
# ⚠ THE ESCAPE HATCH IS DELIBERATE AND IS NOT A LOOPHOLE. A ceiling with no way past it gets
# worked around by quietly under-pricing the job, which would destroy the only honest number in
# the stamp. So over-ceiling is permitted — but ONLY as an explicit, marked, forked act:
# crossing the line is a QUESTION PUT TO DAVE (runbook, anti-false-fix 2), so the marker names
# him. Unmarked over-ceiling FAILS; marked over-ceiling WARNS and leaves a receipt in the file.
RESERVE_SPEND_RE = re.compile(r"RESERVE SPEND\b[^.]{0,40}?\bforked to Dave\b", re.I)

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
# ds-022 (#34). ⚠ ONE SHAPE, DECLARED ONCE — `_gm_move.py` imports these rather than writing its
# own copy. Two parsers for one line format is the drift class, and #32 was caused by exactly
# that: a `#### ` heading one reader accepted and another refused.
STRATA_KEY_RE = re.compile(r"^####\s+\d{4}-\d{2}-\d{2}\s+#\d+\b")
HOLE_RE = re.compile(r"^\s*>?\s*\**HOLE\**\s+#\d+\b", re.I)
# ★ ABSENT — the THIRD state, ruled by Dave #34. HOLE and ABSENT are not synonyms and the
# difference is the whole point:
#   HOLE   #N — a POSITIVE claim: that session wrote no stratum, and we know it.
#   ABSENT #N — a claim about the RECORD, not the session: no block was found, and whether one
#               was ever written is UNKNOWN. Countable as an unknown; asserts nothing about #N.
# #9/#10/#11/#19 have no block and no note. Writing HOLE for them would have made the log read
# complete at the price of four invented facts — the confident-false-inscription failure this
# programme exists to prevent, committed to tidy a file. ABSENT gets the countable dataset with
# no fabricated cause. ⚠ A remedy is measured too: do not let ABSENT decay into HOLE's meaning.
ABSENT_RE = re.compile(r"^\s*>?\s*\**ABSENT\**\s+#\d+\b", re.I)
SESSION_NO_RE = re.compile(r"#(\d+)\b")
# ★★ #37 — THIS REGEX HAD NEVER WORKED, and only a fallback hid it. It read
#     r"★\s*LATEST.*?#(\d+)\b"
# unanchored, so `.search()` found the FIRST text anywhere in GM mentioning "★ LATEST" — which
# is PROSE in the header (`… header + ★ LATEST + the LS LATEST delta … (#29→#36 …)`) — and
# returned **#29**. It was never reached while `_current_session_no` preferred the §C stratum,
# so a broken reader sat behind a working one for as long as the working one kept winning.
# ⇒ **A fallback path is UNTESTED CODE until something forces it.** Promoting the banner to
# authoritative at #37 is what exposed this, inside the same window.
# Third appearance of substring-vs-structure here (#35's usage probe read prose MENTIONING
# `section-usage` as a record; ds-016's index reads rules by text): **match the STRUCTURE — a
# blockquoted heading — not the words.** ⚠ Banner headings are BLOCKQUOTED: `> ## ★ LATEST …`.
BANNER_SESSION_RE = re.compile(r"^\s*>?\s*#{1,6}\s*★\s*LATEST\b.*?#(\d+)\b", re.M)


def _key_session(line):
    """The session number out of a `#### <date> #<N>` key or a `HOLE #<N>` line, or None.
    ⚠ None rather than a guess: an unparseable key is UNKNOWN, and defaulting it to a number
    would let a malformed block satisfy a continuity check it should have failed."""
    m = SESSION_NO_RE.search(line.split("#### ", 1)[-1] if line.startswith("#### ") else line)
    return int(m.group(1)) if m else None


def _stratum_session_no(gm_text):
    """The newest §C stratum key's session number, or None. This is written by ritual step 2f."""
    for ln in gm_text.splitlines():
        if STRATA_KEY_RE.match(ln):
            n = _key_session(ln)
            if n is not None:
                return n
    return None


def _current_session_no(gm_text):
    """This session's number, read from GM's ★ LATEST banner, with the §C stratum as a
    CROSS-CHECK rather than the source.

    ★★ #37 — THE ORDER WAS INVERTED, AND THE INVERSION BLINDED ds-022's CONTINUITY CHECK.
    This used to read the §C stratum key FIRST and fall back to the banner. But the stratum is
    written by ritual step 2f — **the very step whose omission `gauge_log_continuity` exists to
    catch.** So a session that skipped 2f left the clock un-advanced; the check then validated
    a stale-but-compliant predecessor and passed. It is not an off-by-one that self-corrects:
    the clock stops at the last compliant session and stays there, so the check reports GREEN
    for as long as the lapse continues, and reports it *more* confidently the longer it runs.

    MEASURED AT #37, on the live repo: GM's newest stratum was `#### 2026-07-29 #35` while the
    banner read `#36`. The check therefore asked "does #34 have a block?", found one, and
    announced "the 2f split landed" — with **#35 AND #36 both absent from the log.**

    ⇒ **An auditor may not take its clock from the artefact it audits.** The banner (written at
    steps 2c/2d, a different step, by a different edit) is now the source. Disagreement between
    banner and stratum is not noise to be reconciled — it is the POSITIVE SIGNAL that 2f was
    skipped, and `gauge_log_continuity` raises it rather than quietly preferring one.

    Returns None if the banner is illegible; the caller then WARNS that the check is unarmed
    rather than passing quietly."""
    m = BANNER_SESSION_RE.search(gm_text)
    if m:
        return int(m.group(1))
    # ⚠ Fallback ONLY when the banner is unreadable. It is deliberately the weaker source now:
    # if we are here, the file is already malformed, and a stale number is better than none —
    # but the caller is told the check is degraded.
    return _stratum_session_no(gm_text)

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
# ================================================================ ds-021 — THE TWO UNITS
# RULED 2026-07-28 #31 as (b) with (c) folded in as standing practice — a DELEGATED pick
# ("whatever you recommend"). CONFIRMED by Dave #34, who also named the units.
#
# THE FINDING (#30, measured, not inferred). Every cap in this file was denominated in
# tiktoken cl100k tokens. The window is not charged in cl100k tokens. Two files, one session:
#     GOOD-MORNING.md   16,107 tape → 25,355 bill   (1.57×)
#     _LIVE-STATE.md    18,818 tape → 29,103 bill   (1.55×)
# So a gate reporting "99.2% of block" described a file that actually cost half as much again,
# and five sessions of careful measurement never caught it — because the gate was never WRONG,
# it was PRECISE IN THE WRONG UNIT. That is the whole class ([[measure-dont-convert-units]]:
# a proxy measured carefully, then reported as the quantity itself).
#
# THE UNITS, named by Dave #34 ("you choose"), collision-checked across the corpus first —
# `tick` collides 118×, `ruler` reads as `RULED`, which this repo is full of:
#     tape — what tiktoken cl100k_base counts.  A tape measure tells you the SIZE.
#     bill — what the window actually charges.  The bill tells you the COST.
# ★ THE MNEMONIC IS THE RULE: **the tape is not the bill.** Every token number this gate emits,
#   every size stamp, and every banner figure NAMES ITS UNIT. A bare token count is a defect.
#
# ⚠ THE RATIO IS PROVISIONAL. n=2, one session, two files — it is NOT a corpus constant, and a
# third measurement could move it. (c) is folded in as standing PRACTICE rather than skipped:
# every wrap logs one tape/bill pair into `notes/_GAUGE-LOG.md` (free — the chain is read
# anyway), and at n>=4 the constant goes to Dave to rule. Until then conversion is a LAST
# RESORT: where a real bill measurement exists, USE IT and do not convert.
MEASURED_PAIRS = [                 # (label, tape, bill, date, session) — APPEND, never edit.
    ("GOOD-MORNING.md", 16107, 25355, "2026-07-28", 30),
    ("_LIVE-STATE.md",  18818, 29103, "2026-07-28", 30),
]
RATIO_FIRM_N = 4                   # below this the ratio is provisional and may not be ruled
TAPE_TO_BILL = 1.57                # GM's measured pair, NOT the 1.55 corpus average. Every cap
#                                    below is GM-derived, so restating them with GM's own ratio
#                                    is the honest conversion; the average would silently loosen
#                                    a GM cap by ~1%. Re-dialling this is Dave's.


def bill_of(tape):
    """Derive a bill figure from a tape figure. LAST RESORT — prefer a measured bill."""
    return int(round(tape * TAPE_TO_BILL))


def fmt_units(tape, bill=None):
    """The canonical dual-unit rendering, and the only one. A derived bill is MARKED derived,
    because an unmarked derived number is precisely the ds-021 defect: it reads as a
    measurement and it is not one. Cf. `_MEASURING-TOOL-MUST-NOT-GUESS`: observe, don't infer;
    publish the evidence; never default the unknown."""
    if bill is None:
        return f"{tape:,} tape / ~{bill_of(tape):,} bill (derived ×{TAPE_TO_BILL}, PROVISIONAL)"
    return f"{tape:,} tape / {bill:,} bill (both measured)"


def ratio_status():
    """One line on how firm the ratio is. Reported every wrap so the provisional never quietly
    hardens into canon by being carried long enough."""
    n = len(MEASURED_PAIRS)
    if n < RATIO_FIRM_N:
        return (f"tape→bill ratio PROVISIONAL: n={n} of {RATIO_FIRM_N} measured pairs, using "
                f"×{TAPE_TO_BILL} (GM's own). Not a corpus constant; log this wrap's pair.")
    obs = [b / t for _l, t, b, _d, _s in MEASURED_PAIRS]
    return (f"tape→bill ratio: n={n} pairs, observed {min(obs):.3f}–{max(obs):.3f}, using "
            f"×{TAPE_TO_BILL} — n>={RATIO_FIRM_N} reached, PUT THE CONSTANT TO DAVE to rule.")


SIZE_STAMP_RE = re.compile(r"^\s*>?\s*\**size\**\s*[:—-]\s*(.+)$", re.I)
SIZE_TK_RE = re.compile(r"\bGM\b\D{0,12}?([\d.]+)\s*K\s*(tape|tk)\b", re.I)  # K is REQUIRED:
#   without it "GM 25618 tk" would parse as 25.6M and pass a drift check by accident.
#   ds-021 (#34): `tape` is the canonical unit; bare `tk` is the LEGACY spelling and is still
#   accepted, but it WARNS. ⚠ It is accepted deliberately — a regex that hard-failed on the old
#   form would have blocked the very wrap that rewrites the stamp, i.e. a gate that cannot be
#   satisfied from the state it is introduced in. PROMOTION TRIGGER: once a wrap passes with no
#   legacy-unit warning, make `tape` mandatory here and delete the `|tk` branch. This comment is
#   the only record of that trigger — it ships WITH its consumer (the warn below), per ds-024.
LEGACY_UNIT_RE = re.compile(r"\b\d[\d.]*\s*K\s*tk\b", re.I)
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
SIZE_A_RE = re.compile(r"§A\D{0,12}?([\d.]+)\s*K\s*(tape|tk)\b", re.I)  # K REQUIRED, as for GM
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
#
# ★★ RE-POINTED 2026-07-28 #33, when Dave ruled the EAGER READ CHAIN (GM-D7-am) CUT.
#   Everything above stands as ruled and is not trimmed — it is the record of what M10 was. What
#   changed is the REFERENT, not the ruling: until #33 the "chain" was GM + _LIVE-STATE in full,
#   because the contract told every session to read both files end to end. The new contract is
#   **header + ★ LATEST banner + the _LIVE-STATE LATEST delta**; §A and §C stay in the file and
#   are reached by retrieval (`_memento_search.py`). Measured at the cut:
#       old referent (GM + LS whole)   34,094 tk cl100k  ≈ 52,846 charged  ≈ 26.4 pts
#       new referent (HDR+LATEST+delta) 3,410 tk cl100k  ≈  5,286 charged  ≈  2.6 pts
#   ⚠ **THE PROMOTION TRIGGER IS DISARMED, DELIBERATELY, AND THIS IS DAVE'S CALL TO RE-MAKE.**
#   The old comment said: arm the block once a wrap measures the chain under 28,000. Re-pointing
#   satisfies that instantly — 3,410 < 28,000 — but it is satisfied **by redefinition, not by
#   achievement**, and arming a 28,000 block against a 3,410 tk chain would create precisely the
#   thing ds-024 named: an instrument nobody reads, that can never fire. So the threshold does NOT
#   auto-arm. The numbers below are AGENT-DERIVED from one measurement and are ADVISORY until Dave
#   rules them (derivation governance: the engine never derives-and-promotes).
#   ⚠ AND the corpus figure is published on every wrap regardless. The chain got 90% cheaper; the
#   corpus did not get smaller, it got *deferred*. A budget that reported only the chain would hide
#   the retrieval surface exactly the way the D7 amendment warned an §A exclusion would hide GM.
CHAIN_BUDGET_TK = (4500, 6000)     # (warn, BLOCK-CANDIDATE) — ADVISORY, agent-derived, awaiting
#                                    Dave. Measured 3,410 tk at the cut; warn leaves ~32% headroom.
CORPUS_BUDGET_TK = 36000           # (warn only) — GM + LS whole, the RETRIEVAL SURFACE. Never
#                                    blocks: it is the thing the cut made cheap to carry, not the
#                                    thing the cut made small. 34,094 tk at the cut.

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
    """FORM check on the pre-flight stamp, plus the ds-023 CEILING. Returns (fails, warns, notes).

    Bites on the three failures actually observed: the wrap term omitted (2026-07-27 #2),
    a band asserted from memory instead of the table (twice), and arithmetic that doesn't
    close. Everything it cannot see is named in the module header, not implied away.

    ⚠ The third return value is new at #34 and is not decoration. ds-023's stop line
    (`HARD_STOP − the priced wrap`) is only useful on the PASSING path — a session that is
    within its ceiling is exactly the one that still needs telling where to stop. Folding it
    into `warns` would have made the good path noisy and taught sessions to skim the warnings;
    dropping it would have shipped a computed number with no reader, which is ds-024's class."""
    fails, warns, notes = [], [], []
    line = next((ln for ln in text.splitlines() if PREFLIGHT_RE.match(ln)), None)
    if line is None:
        return ([f"{label}: no `pre-flight:` stamp — the handoff must carry the estimate the "
                 f"session was priced with (runbook § ★ Half 0b). Form: `pre-flight: fill N% + "
                 f"job N% + wrap N% = N% BAND · reserve 15% ring-fenced`"], warns, notes)

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

    # ---- ds-023: THE BAND. Everything above this point is a FORM check — it asks whether the
    # stamp is well-formed. This is the first thing here that asks whether the PLAN IS ALLOWED.
    # ★★ RE-STATED BY DAVE #36 — see the ds-023 header block. 45 is the FLOOR of the preferred
    # band, not a ceiling; the `>= 45 -> FAIL` this replaced was a delegated agent's pick and
    # was refusing the zone Dave wants sessions to land in. Do not re-tighten it without a
    # ruling from him, in his words, quoted at the site.
    if tm and not missing:
        total = int(tm.group(1))
        stop_at = HARD_STOP - terms["wrap"]
        if total < BAND_FLOOR:
            notes.append(
                f"{label}: pre-flight {total}% is BELOW the {BAND_FLOOR}–{HARD_STOP}% preferred "
                f"band (Dave #36). Allowed — but a price that keeps landing under the band is "
                f"the UNDER-PRICING this band replaced, not thrift. Check the full price really "
                f"includes front-load + context GM + job + wrap. In flight, STOP AT {stop_at}% "
                f"({HARD_STOP} − the {terms['wrap']}%-priced wrap).")
        elif total <= HARD_STOP:
            notes.append(
                f"{label}: pre-flight {total}% is IN the {BAND_FLOOR}–{HARD_STOP}% preferred "
                f"band (Dave #36: \"where I'd prefer the full price with wrap to sit\"). This is "
                f"the target, not a tolerance — no receipt required. In flight, STOP AT "
                f"{stop_at}% ({HARD_STOP} − the {terms['wrap']}%-priced wrap): {HARD_STOP} is "
                f"where the wrap has FINISHED, not where it starts.")
        elif total <= MARKED_MAX:
            if RESERVE_SPEND_RE.search(line):
                warns.append(
                    f"{label}: pre-flight {total}% is over the {HARD_STOP}% line but within the "
                    f"{MARKED_MAX}% tolerance — ALLOWED, marked and forked to Dave. His word "
                    f"(#36) is that this is TOLERABLE **and RARE**: a session that marks this "
                    f"every wrap has re-dialled the line by habit rather than by ruling. In "
                    f"flight, STOP AT {stop_at}% ({HARD_STOP} − the {terms['wrap']}%-priced "
                    f"wrap).")
            else:
                fails.append(
                    f"{label}: pre-flight {total}% is over the {HARD_STOP}% line (ds-023). Dave #36 "
                    f"allows up to {MARKED_MAX}% but only RARE and MARKED — so either CUT THE "
                    f"JOB back into the {BAND_FLOOR}–{HARD_STOP}% band, or declare the overrun "
                    f"IN ADVANCE and mark it `RESERVE SPEND — forked to Dave`. What is not "
                    f"allowed is discovering it afterwards: #30, #31, #32 and #33 all exceeded "
                    f"their own projections. ⚠ Do NOT under-price the job to fit — that is the "
                    f"failure this band exists to prevent.")
        else:
            # ⚠ > MARKED_MAX is UNRULED BY DAVE. The pre-#36 escape-hatch SHAPE is preserved
            # deliberately (marked -> WARN, unmarked -> FAIL) rather than replaced with an
            # invented harder stop: picking an enforcement Dave never ruled is the exact defect
            # #36 found in this file. The message says so, so the gap cannot go quiet.
            hatch = (f"⚠ above {MARKED_MAX}% is UNRULED — Dave has ruled the band "
                     f"({BAND_FLOOR}–{HARD_STOP}) and the marked tolerance ({MARKED_MAX}), and "
                     f"nothing beyond. This gate keeps the pre-#36 shape here rather than "
                     f"inventing a stop he did not pick; FORKED TO DAVE, ds-023.")
            if RESERVE_SPEND_RE.search(line):
                warns.append(
                    f"{label}: pre-flight {total}% is beyond the {MARKED_MAX}% tolerance, marked "
                    f"and forked to Dave — allowed on the receipt. {hatch} In flight, STOP AT "
                    f"{stop_at}% ({HARD_STOP} − the {terms['wrap']}%-priced wrap).")
            else:
                fails.append(
                    f"{label}: pre-flight {total}% is beyond the {MARKED_MAX}% tolerance and "
                    f"UNMARKED (ds-023) — CUT THE JOB, or declare it in advance and mark it "
                    f"`RESERVE SPEND — forked to Dave`. {hatch}")

    if terms.get("wrap", WRAP_FLOOR) < WRAP_FLOOR:
        warns.append(f"{label}: wrap reserved at {terms['wrap']}% (runbook says ~{WRAP_FLOOR}%) "
                     f"— the ritual is not free")
    if not RESERVE_RE.search(line):
        warns.append(f"{label}: pre-flight names no ring-fenced reserve (~{RESERVE_FENCE}%) — "
                     f"the fence is what makes the gauge a throttle rather than a thermometer")
    return fails, warns, notes


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


LS_DELTA_RE = re.compile(r"^##\s*⏱")


def read_chain_tk(repo, gm_lines):
    """Measure the GM-D7-am READ CHAIN **as re-pointed #33**: GM header + ★ LATEST banner +
    the `_LIVE-STATE.md` LATEST delta. Returns `(chain_tk, detail)`; `(None, reason)` if a
    region cannot be isolated.

    ⚠ It REUSES `_gm_usage.split_sections` — the same parser the memento index is built from —
    instead of growing a second one here. A second parser is exactly the drift class the M8
    block exists to prevent, and a chain measured by a different splitter than the one the
    retrieval door uses would drift silently against the thing it claims to describe.

    ⚠ It REFUSES rather than guesses. Every failure path returns a REASON, never a number and
    never a zero: a budget check that defaults to 0 on a parse failure reports GREEN on a
    broken file, which is the "cheerful zero" this corpus has already been bitten by.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import _gm_usage
    except Exception as e:                                    # pragma: no cover - import guard
        return None, f"_gm_usage unavailable ({e}) — chain UNMEASURED, not assumed clean"

    def _region_end(lines, vocab, start_id):
        """First line index of `start_id`'s marker, and where its region ends — using the SAME
        regexes `_gm_usage` splits on, but WITHOUT demanding the whole vocabulary validate.

        ⚠ The first draft of this called `split_sections(..., unknown_check=...)` and refused the
        whole measurement when any unrelated marker was missing — a chain that cannot be measured
        because `C4b` moved is over-coupled, and it silently routed every fixture down the
        UNMEASURED path. The chain depends on ★ LATEST and ⏱ DELTAS; nothing else may break it.
        Caught by a bite, not by re-reading the code."""
        rx = dict(vocab).get(start_id)
        if rx is None:
            return None, None
        start = next((i for i, ln in enumerate(lines) if rx.match(ln)), None)
        if start is None:
            return None, None
        others = [r for k, r in vocab if k != start_id and r is not None]
        end = next((i for i in range(start + 1, len(lines))
                    if any(r.match(lines[i]) for r in others)), len(lines))
        return start, end

    # HDR runs file-top → LATEST, and LATEST → the next marker. Contiguous, so one slice carries
    # both: the chain's GM term is "everything above the end of the ★ LATEST banner".
    _s, l_end = _region_end(gm_lines, _gm_usage.GM_VOCAB, "LATEST")
    if l_end is None:
        return None, ("GOOD-MORNING.md has no ★ LATEST banner — the chain's whole session record "
                      "is that banner, so this is a refusal to measure, not a small chain")
    gm_part = "\n".join(gm_lines[:l_end])
    gm_tk = measure_tokens(gm_part)[0]

    ls_path = os.path.join(repo, "_LIVE-STATE.md")
    if not os.path.exists(ls_path):
        return gm_tk, f"GM header+LATEST {gm_tk} tk · _LIVE-STATE absent (no delta term)"
    with open(ls_path, encoding="utf-8") as f:
        ls_lines = f.read().splitlines()
    d_s, d_e = _region_end(ls_lines, _gm_usage.LS_VOCAB, "DELTAS")
    if d_s is None:
        return None, "_LIVE-STATE.md has no ⏱ delta section — chain UNMEASURED, not assumed zero"
    body = ls_lines[d_s:d_e]
    # The LATEST delta ends where the next ⏱ heading begins. If there is no second one, the
    # whole section IS the latest delta — say which case was taken, never silently assume.
    nxt = next((i for i, ln in enumerate(body) if i > 0 and LS_DELTA_RE.match(ln)), None)
    delta = "\n".join(body[:nxt] if nxt else body)
    d_tk = measure_tokens(delta)[0]
    how = f"LATEST delta only (of {len(body)} delta lines)" if nxt else "whole ⏱ section (single delta)"
    return gm_tk + d_tk, f"GM header+LATEST {gm_tk} tk · LS {how} {d_tk} tk"


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
    # CORPUS = GM + _LIVE-STATE whole. Until #33 this variable was called `chain`, because the
    # contract made a session read all of it. After the cut it is the RETRIEVAL SURFACE: still
    # carried, no longer read on arrival. Renamed so the two can never again be confused.
    corpus = tk
    ls_path = os.path.join(repo, "_LIVE-STATE.md")
    if os.path.exists(ls_path):
        with open(ls_path, encoding="utf-8") as f:
            corpus += measure_tokens(f.read())[0]
    chain, chain_detail = read_chain_tk(repo, lines)
    # ⚠ The whole-file figure leads, ALWAYS. The budget excludes §A; the published cost does not.
    # An exclusion that also hides the total would understate exactly the cold-start cost that the
    # D9 measured floor exists to make honest. Post-#33 the same principle covers the corpus: the
    # chain got 90% cheaper, the corpus did not get smaller — it got DEFERRED. Publish both.
    chain_txt = f"{chain} tk ({chain_detail})" if chain is not None else f"UNMEASURED — {chain_detail}"
    notes.append(f"SIZE measured ({method}): GM {tk} tk WHOLE FILE · of which §A {exempt_tk} tk "
                 f"exempt · compactable {compactable} tk (the budgeted figure) · "
                 f"READ CHAIN {chain_txt} · corpus (GM+LS, the retrieval surface) {corpus} tk")

    stamp = next((m for m in (SIZE_STAMP_RE.match(ln) for ln in lines[:HEADER_LINES]) if m), None)
    if stamp is None:
        fails.append("GOOD-MORNING.md: no `size:` stamp — ritual step 2")
    else:
        # ---- ds-021: the stamp is the THIRD home. It is the number a reader quotes without
        # re-measuring, so it is the one place an unnamed unit does the most damage.
        if LEGACY_UNIT_RE.search(stamp.group(1)):
            warns.append("GOOD-MORNING.md `size:` stamp still spells the measured unit `tk` — "
                         "ds-021 canon is `tape` (what tiktoken counts) beside `bill` (what the "
                         "window charges). Re-stamp in both units, naming each. WARN this wrap "
                         "only: when a wrap passes clean here, `tape` becomes mandatory in "
                         "SIZE_TK_RE and the legacy branch is deleted.")
        cm = SIZE_TK_RE.search(stamp.group(1))
        if not cm:
            fails.append("GOOD-MORNING.md: `size:` stamp carries no GM figure — ritual step 2")
        else:
            claimed = float(cm.group(1)) * 1000
            if abs(claimed - tk) / max(tk, 1) > SIZE_TOLERANCE:
                fails.append(f"GOOD-MORNING.md: `size:` stamp claims {claimed:.0f} tk, measured "
                             f"{tk} tk — ritual step 2")

    # ---- ds-021: the cap BINDS ON BILL. Both numbers are reported, the unit is named on each.
    # ⚠ Today this is arithmetically identical to binding on tape, BY DESIGN — the ruling says
    # RESTATED at current real value, not silently tightened, and both sides of the comparison
    # are currently derived through the same ratio. What it buys is (i) nobody can read a tape
    # figure as a cost again, and (ii) the moment a REAL bill measurement arrives the cap binds
    # on the measured thing and the ratio stops mattering. A conversion applied to both sides
    # cancels; the naming does not.
    budget = SIZE_BUDGET_TK["compactable"]
    budget_bill, block_bill = bill_of(budget), bill_of(int(budget * 1.5))
    compact_bill = bill_of(compactable)
    notes.append(f"COMPACTABLE region: {fmt_units(compactable)} · warn {budget:,} tape / "
                 f"~{budget_bill:,} bill · block {int(budget * 1.5):,} tape / ~{block_bill:,} bill")
    if compact_bill >= block_bill:
        fails.append(f"GOOD-MORNING.md compactable: {fmt_units(compactable)}, block "
                     f"~{block_bill:,} bill — ritual step 2")
    elif compact_bill > budget_bill:
        warns.append(f"GOOD-MORNING.md compactable: {fmt_units(compactable)}, cap "
                     f"~{budget_bill:,} bill — ritual step 2")

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
        bw_bill, bb_bill = bill_of(b_warn), bill_of(b_block)
        notes.append(f"BANNER region: {fmt_units(banner_tk)} (file top → DO-FIRST: header + "
                     f"★ LATEST + ★ PRIOR) · warn {b_warn:,} tape / ~{bw_bill:,} bill · block "
                     f"{b_block:,} tape / ~{bb_bill:,} bill")
        if bill_of(banner_tk) >= bb_bill:
            fails.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, block "
                         f"~{bb_bill:,} bill — roll a banner to _GM-ARCHIVE.md (ritual step 2c)")
        elif bill_of(banner_tk) > bw_bill:
            warns.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, cap "
                         f"~{bw_bill:,} bill — ritual step 2c")

    # ---- M10, RE-POINTED #33: the READ CHAIN is header + ★ LATEST + the LS LATEST delta.
    # ADVISORY, and the budget numbers are agent-derived pending Dave (see the constant block).
    c_warn, c_block = CHAIN_BUDGET_TK
    # ⚠ Both messages lead with a UNIQUE tag. The first draft had the bites match on the substring
    # "read chain" — which also appears inside the corpus warn's own explanatory prose, so a fat-§A
    # fixture "warned the chain" when the chain had in fact measured 60 tk. A bite that matches on
    # a phrase two different messages share is not a bite. Tag, then match the tag.
    if chain is None:
        warns.append(f"M10 read chain UNMEASURED — {chain_detail}. Not defaulted, not assumed "
                     f"clean: a chain budget that reports 0 on a parse failure reads GREEN on a "
                     f"broken file. Fix the structure, then re-run.")
    elif bill_of(chain) > bill_of(c_warn):
        warns.append(f"M10 read chain (header + ★ LATEST + LS latest delta): {fmt_units(chain)}, "
                     f"warn {c_warn:,} tape / ~{bill_of(c_warn):,} bill · block-candidate "
                     f"{c_block:,} tape / ~{bill_of(c_block):,} bill — ADVISORY, numbers "
                     f"agent-derived and awaiting Dave. {chain_detail}. This check knows the "
                     f"total, not where the weight sits — measure the three terms before picking "
                     f"one to trim.")
    else:
        notes.append(f"M10 read chain: {fmt_units(chain)} · warn {c_warn:,} tape / "
                     f"~{bill_of(c_warn):,} bill (ADVISORY). {ratio_status()}")
    # ---- The corpus rides alongside, always, warn-only. Post-cut it is what retrieval must
    # serve, not what a session reads; it is reported so the deferral can never read as a deletion.
    if bill_of(corpus) > bill_of(CORPUS_BUDGET_TK):
        warns.append(f"M10 corpus (GM + _LIVE-STATE whole): {fmt_units(corpus)}, warn "
                     f"{CORPUS_BUDGET_TK:,} tape / ~{bill_of(CORPUS_BUDGET_TK):,} bill — the "
                     f"RETRIEVAL SURFACE, not the chain a session reads. WARN ONLY: growth here "
                     f"costs a retrieval, not a cold start. Never a trim order.")
    else:
        notes.append(f"M10 corpus (retrieval surface): {fmt_units(corpus)} · warn "
                     f"{CORPUS_BUDGET_TK:,} tape / ~{bill_of(CORPUS_BUDGET_TK):,} bill")

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
    if bill_of(exempt_tk) > bill_of(SECTION_A_WARN_TK):
        warns.append(f"§A {fmt_units(exempt_tk)}, past the {SECTION_A_WARN_TK:,} tape / "
                     f"~{bill_of(SECTION_A_WARN_TK):,} bill backstop — ADVISORY. §A is uncapped "
                     f"by ruling (GM-D7-am); this is a look-at-it, never a trim order.")
    return fails, warns, notes


def gauge_log_continuity(repo):
    """ds-022 (a), the guard on (c): session N's wrap FAILS unless session N−1 left a block —
    or an explicit HOLE line — in `notes/_GAUGE-LOG.md`. Returns (fails, warns, notes).

    ⚠ THE HOLE ESCAPE HATCH IS LOAD-BEARING, not politeness. Some sessions legitimately write
    no stratum (a lane wrap, an aborted window). Without a way to say so, this check would block
    a wrap whose predecessor was correct — and a gate that fails on correct behaviour teaches
    sessions to FAKE blocks, which would poison the exact dataset the throttle is re-derived
    from. #14 is the proof it works: its absence was flagged, so #14 is countable. #9, #10, #11
    and #19 are absent with nothing said, so the file cannot state whether they ever existed.

    ⚠ WHAT IT CANNOT SEE: whether the block's CONTENT is a real post-mortem. It checks presence
    and continuity — the two things a grep can settle. Do not teach it to grade prose."""
    fails, warns, notes = [], [], []
    log = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    gm = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(log) or not os.path.exists(gm):
        notes.append("ds-022 continuity: no _GAUGE-LOG.md or no GOOD-MORNING.md — UNMEASURED, "
                     "not assumed clean.")
        return fails, warns, notes

    with open(gm, encoding="utf-8") as f:
        gm_text = f.read()
    with open(log, encoding="utf-8") as f:
        log_lines = f.read().splitlines()

    cur = _current_session_no(gm_text)
    if cur is None:
        warns.append("ds-022 continuity: could not read this session's number from "
                     "GOOD-MORNING.md — the check is UNARMED this wrap and says so rather than "
                     "passing quietly. (It reads the `★ LATEST` banner's `#<N>` first, then "
                     "falls back to the `#### <date> #<N>` §C stratum key.)")
        return fails, warns, notes

    # ★★ THE CLOCK CROSS-CHECK, #37. The banner and the §C stratum are written by DIFFERENT
    # ritual steps (2c/2d vs 2f). When they disagree, the later step did not run — and that is
    # precisely the condition under which this whole check used to go blind, because it took
    # its own clock from 2f's output. Reported as a FAIL, not reconciled: the disagreement is
    # the finding. ⚠ Do not "fix" a red here by editing the banner to match the stratum; the
    # remedy is to run 2f, or to declare the gap with a HOLE line.
    strat = _stratum_session_no(gm_text)
    if strat is not None and strat != cur:
        fails.append(
            f"ds-022 continuity: GM's ★ LATEST banner says #{cur} but the newest §C stratum "
            f"key says #{strat} — ritual step 2f did not run for "
            f"{'this session' if strat < cur else 'the banner’s session'}. This is the "
            f"self-hiding failure found at #37: the continuity check used to read its own "
            f"clock from the stratum, so a skipped 2f froze the clock at the last compliant "
            f"session and the check reported GREEN indefinitely (measured: banner #36 vs "
            f"stratum #35, while #35 AND #36 were both missing from _GAUGE-LOG.md). Run 2f, "
            f"or declare the gap with `HOLE #<N> — <why>`.")

    have = {n for n in (_key_session(ln) for ln in log_lines
                        if STRATA_KEY_RE.match(ln)) if n is not None}
    holes = {n for n in (_key_session(ln) for ln in log_lines
                         if HOLE_RE.match(ln)) if n is not None}
    absent = {n for n in (_key_session(ln) for ln in log_lines
                          if ABSENT_RE.match(ln)) if n is not None}
    prev = cur - 1
    if prev in have:
        notes.append(f"ds-022 continuity: #{prev} has a block in notes/_GAUGE-LOG.md — the 2f "
                     f"split landed. (n={len(have)} recorded · {len(holes)} declared holes · "
                     f"{len(absent)} ABSENT-unknown. {ratio_status()})")
    elif prev in holes:
        notes.append(f"ds-022 continuity: #{prev} is a DECLARED HOLE — countable, which is the "
                     f"whole difference between #14 and #9/#10/#11/#19.")
    elif prev in absent:
        warns.append(f"ds-022 continuity: #{prev} is marked ABSENT — no block found, and whether "
                     f"one was ever written is UNKNOWN. ⚠ WARN, not pass: ABSENT is a statement "
                     f"about the RECORD, not a licence to skip 2f. If YOU wrote no stratum, say "
                     f"so with `HOLE #{prev} — <why>`; ABSENT is for gaps nobody can account for.")
    else:
        fails.append(
            f"ds-022: session #{prev} left NO block and NO hole line in notes/_GAUGE-LOG.md, "
            f"so this wrap (#{cur}) cannot proceed. Ritual step 2f splits the older stratum — "
            f"post-mortem to the log, commit-state to _GM-ARCHIVE.md — and #26/#28/#29 all "
            f"rolled WHOLE into the archive instead. #29 is why this check exists: the only RED "
            f"session on the board, the only measured overrun cause, and its band is gone. "
            f"FIX: roll it with `_gm_move.py --ops` op `roll_2f` (which cannot half-do it), or "
            f"— if #{prev} genuinely wrote no stratum — declare it: "
            f"`HOLE #{prev} — <why>` in notes/_GAUGE-LOG.md.")
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


# #35: the usage HISTORY probe's tier. ADVISORY AT BIRTH, deliberately — the dataset it
# reads is eleven sessions old and has never been read, so its first act must be to PUBLISH,
# not to block a wrap on a threshold nobody has ruled. ★ PROMOTION TRIGGER, recorded here so
# it cannot be lost the way ds-021/022/023 were for three sessions: promote to BLOCKING when
# Dave rules the remedy for the standing candidate list (OFFLOAD / TRIM / KEEP, per id) — at
# that point the check becomes "no section sits never-cited and long-unread without a
# recorded ruling", which is enforceable. Flag + its selftest pin move only as a pair.
USAGE_HISTORY_BLOCKING = False


def usage_history_probe(repo):
    """#35: READ the accumulated `section-usage` testimony as a SERIES, and say what it shows.

    ★ WHY THIS EXISTS. `section_usage_probe` above FORM-checks one line per wrap and the
    lines then accumulate in `_GAUGE-LOG.md` — where, for eleven sessions, NOTHING read them.
    Its own docstring names the dataset as what LS-trim-vs-defer waits on; the waiting had no
    end because no code ever looked. ds-024's class exactly: an instrument shipped without its
    reader. This is the reader.

    ⚠ IT PUBLISHES; IT DOES NOT PRESCRIBE. The remedies (OFFLOAD to the retrieval index /
    TRIM as durably recorded elsewhere / KEEP) are Dave's, per derivation governance, and the
    published text says so on every run.

    ⚠ AND IT IS NOT A WINDOW-COST CLAIM. #33 cut the read chain to header → ★ LATEST → the LS
    LATEST delta; every id this names sits OUTSIDE that chain and is no longer paid eagerly.
    What it measures is RECORD cost — carried, rolled and gated prose nobody consults — which
    is a real cost and a different one. Do not let the two be quoted as each other."""
    issues, notes = [], []
    try:
        sys.path.insert(0, HERE)
        import _gm_usage
    except Exception as e:
        issues.append(f"usage-history: _gm_usage.py unimportable ({e}) — the series is "
                      f"UNREAD, never assumed clean")
        return issues, notes
    report, rows, refusals = _gm_usage.history_report(repo)
    if refusals:
        issues += [f"usage-history: {r}" for r in refusals]
        return issues, notes
    if not rows:
        notes.append("usage-history: no testimony found — UNMEASURED, not assumed clean.")
        return issues, notes
    cands = _gm_usage.deferral_candidates(_gm_usage.usage_streaks(rows))
    notes.append("usage-history: %d sessions of testimony read as a series "
                 "(`python3 knowledge/_gm_usage.py --history` prints the full table)."
                 % len(rows))
    if cands:
        notes.append("usage-history ⬛ %d sections NEVER CITED in %d sessions and unread %d+ "
                     "running: %s. Remedy UNRULED (OFFLOAD / TRIM / KEEP — Dave's, not this "
                     "gate's). Threshold %d is %s."
                     % (len(cands), len(rows), _gm_usage.DEFER_STREAK,
                        ", ".join(k for k, _ in cands), _gm_usage.DEFER_STREAK,
                        _gm_usage.DEFER_STREAK_STATUS))
    else:
        notes.append("usage-history: no section is both never-cited and long-unread.")
    notes.append("usage-history tier: %s (read from USAGE_HISTORY_BLOCKING — promotion "
                 "trigger is Dave ruling the candidate list; flag + selftest pin move as a "
                 "pair)." % ("BLOCKING" if USAGE_HISTORY_BLOCKING else "ADVISORY"))
    return issues, notes


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
                f_, w_, n_ = check_preflight(f.read())
            notes += n_
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
        i_, n_ = usage_history_probe(repo)      # #35 — the series READER, ADVISORY at birth
        (fails if USAGE_HISTORY_BLOCKING else warns).extend(i_)
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
        f_, w_, n_ = gauge_log_continuity(repo)  # ds-022 (a) #34 — the 2f split must LAND.
        fails += f_                              # BLOCKING: three wraps in a row skipped the
        warns += w_                              # step, and #29's overrun cause is gone for good.
        notes += n_
        notes.append(f"PRE-FLIGHT stamp: ds-023 is a BAND (Dave #36) — the FULL price "
                     f"(front-load + context GM + job + wrap) is preferred in "
                     f"{BAND_FLOOR}–{HARD_STOP}%; {HARD_STOP} is the line and is livable; up to "
                     f"{MARKED_MAX}% is tolerable when RARE and MARKED "
                     f"(`RESERVE SPEND — forked to Dave`); above {MARKED_MAX} is UNRULED. Plus "
                     f"the FORM check below. Whether the fill figure is HONEST is still not "
                     f"observable here — and the BOOT it rests on was first measured at #37.")
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
    # ⚠ THE HISTORY OF THIS CONTROL IS THE EVIDENCE — do not delete it, it has flipped TWICE.
    #     "fill 40% + job 12% + wrap 5% = 57% AMBER"
    # passed at birth (FORM check only) · FAILED from #34 (over the 45 "ceiling") · and PASSES
    # again from #37, because Dave #36 re-stated 45 as the FLOOR of the preferred band. A fixture
    # that flips back to its original value is the strongest single proof that the #31 delegated
    # enforcement was never his — the control was right, then wrong, then right again, and only
    # the enforcement moved. It is a live fixture below, not a comment.
    ("below the band (44)",
     "pre-flight: fill 24% + job 12% + wrap 8% = 44% GREEN · reserve 15% ring-fenced\n", False),
    ("below the band, boundary (44)",
     "pre-flight: fill 30% + job 9% + wrap 5% = 44% GREEN · reserve 15% ring-fenced\n", False),
    # ---- ds-023 BAND fixtures (Dave #36). ⚠ Band WORDS must match the table or the mis-read
    # check fires and the fixture proves the wrong thing: 45–59 AMBER, 60+ RED.
    ("ds-023: 45 is the BAND FLOOR — passes (FLIPPED from #34's FAIL, Dave #36)",
     "pre-flight: fill 32% + job 5% + wrap 8% = 45% AMBER · reserve 15% ring-fenced\n", False),
    ("ds-023: 57 IN the band, UNMARKED — passes (the twice-flipped control)",
     "pre-flight: fill 40% + job 12% + wrap 5% = 57% AMBER · reserve 15% ring-fenced\n", False),
    ("ds-023: 60 is the line and is LIVABLE — passes",
     "pre-flight: fill 40% + job 12% + wrap 8% = 60% RED · reserve 15% ring-fenced\n", False),
    ("ds-023: 62 over the line, UNMARKED — must FAIL",
     "pre-flight: fill 42% + job 12% + wrap 8% = 62% RED · reserve 15% ring-fenced\n", True),
    ("ds-023: 62 over the line but MARKED — allowed, warns not fails",
     "pre-flight: fill 42% + job 12% + wrap 8% = 62% RED · reserve 15% ring-fenced · "
     "RESERVE SPEND — forked to Dave\n", False),
    ("ds-023: 70 beyond the marked tolerance, UNMARKED — must FAIL (>63 UNRULED)",
     "pre-flight: fill 50% + job 12% + wrap 8% = 70% RED · reserve 15% ring-fenced\n", True),
]


def selftest_preflight():
    """Bite-test the pre-flight FORM check — every class must FAIL, controls must pass."""
    failures = []
    for name, text, should_fail in PREFLIGHT_FIXTURES:
        f_, _w, _n = check_preflight(text, label="fixture")
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
    f_, _w, _n = check_preflight("pre-flight: fill 40% + job 12% + wrap 5% = 72% RED · reserve 15%\n",
                                 label="fixture")
    if not f_:
        failures.append("pre-flight: a stamp that ADDED the ring-fenced reserve into its total "
                        "passed — the fence has silently become a fourth addend (runbook § Half "
                        "0b anti-false-fix 1)")

    # ---- ds-023, AS RE-STATED BY DAVE #36. The FIXTURES above prove the band passes and fails
    # in the right places. These prove the three things a pass/fail table cannot see: that the
    # escape hatch leaves a RECEIPT rather than silence, that the stop line is PUBLISHED, and
    # ★ that marking a stamp which never needed marking produces NO receipt.
    #
    # ⚠ THIS BLOCK MOVED FROM 48% TO 62% AT #37, AND THE MOVE IS THE POINT. Under the #31
    # enforcement, 48% was "over the ceiling" and had to carry a receipt — for a spend that was
    # never over budget. That is the manufactured under-pricing #36 found. 48% is now simply IN
    # the band, and the receipt machinery starts where Dave actually put the line: past 60.
    marked = ("pre-flight: fill 42% + job 12% + wrap 8% = 62% RED · reserve 15% ring-fenced · "
              "RESERVE SPEND — forked to Dave\n")
    f_, w_, n_ = check_preflight(marked, label="fixture")
    if f_:
        failures.append(f"ds-023: a MARKED over-line spend failed ({f_}) — a line with no "
                        f"declared way past it gets worked around by under-pricing the job, "
                        f"which corrupts the only honest number in the stamp")
    if not any("RESERVE SPEND" in x or "forked to Dave" in x for x in w_):
        failures.append("ds-023: a marked over-line spend passed SILENTLY — the marker is a "
                        "receipt, and a receipt nobody emits is not a receipt. Dave must be "
                        "able to see, later, that the line was crossed deliberately")
    if not any("STOP AT 52%" in x for x in w_):
        failures.append(f"ds-023: the over-line path did not publish the stop line "
                        f"(expected 'STOP AT 52%' = {HARD_STOP} − an 8%% wrap), got {w_}")

    # ★ THE ANTI-HABIT BITE, NEW AT #37 — the direct test of the defect #36 found. A stamp that
    # is comfortably INSIDE the band must produce NO receipt even if it carries the marker,
    # because a gate that accepts receipts for non-events teaches sessions to mark everything,
    # and a marker that appears on every wrap has re-dialled the line by habit rather than by
    # ruling. Under the #31 enforcement this exact stamp emitted a warning; that was the bug.
    in_band_marked = ("pre-flight: fill 30% + job 10% + wrap 8% = 48% AMBER · reserve 15% "
                      "ring-fenced · RESERVE SPEND — forked to Dave\n")
    f_, w_, _n = check_preflight(in_band_marked, label="fixture")
    if f_:
        failures.append(f"ds-023: an IN-BAND stamp (48%) failed ({f_}) — 45–60 is Dave's "
                        f"preferred band and must pass clean")
    if any("RESERVE SPEND" in x or "forked to Dave" in x for x in w_):
        failures.append(f"ds-023: an IN-BAND stamp (48%) emitted an over-line receipt ({w_}). "
                        f"THIS IS THE #36 DEFECT ITSELF — the gate charging a receipt for a "
                        f"spend that was never over budget. 48 is inside 45–60; nothing to "
                        f"declare")

    # ★ THE UNDER-PRICING BITE, added #37 AFTER A MUTATION SURVIVED. Deleting the below-band
    # branch entirely (`if total < BAND_FLOOR` -> `if total < 0`) left every other ds-023
    # assertion green — so the one branch that guards against CHRONIC UNDER-PRICING, which is
    # the failure Dave's band exists to replace, was completely untested. An unread note is
    # ds-024's class (an instrument shipped without its consumer); an unasserted one is worse,
    # because it can be deleted without a single test going red.
    f_, _w, n_ = check_preflight(
        "pre-flight: fill 20% + job 8% + wrap 8% = 36% GREEN · reserve 15% ring-fenced\n",
        label="fixture")
    if f_:
        failures.append(f"ds-023: a below-band stamp (36%) FAILED ({f_}) — under the band is "
                        f"allowed, it is only noted")
    if not any("BELOW" in x and "under-pricing" in x.lower() for x in n_):
        failures.append(f"ds-023: a below-band stamp (36%) published no under-pricing note. "
                        f"Dave's band replaced a regime that manufactured under-pricing; a "
                        f"price that keeps landing under 45 is the symptom, and this note is "
                        f"the only place the gate can say so. Got {n_}")

    # the stop line must appear on the PASSING path too — that is the session that still has
    # room to overrun, and the one every previous overrun happened in.
    ok = "pre-flight: fill 24% + job 12% + wrap 8% = 44% GREEN · reserve 15% ring-fenced\n"
    f_, _w, n_ = check_preflight(ok, label="fixture")
    if f_:
        failures.append(f"ds-023: a within-ceiling stamp failed ({f_})")
    if not any("STOP AT 52%" in x for x in n_):
        failures.append(f"ds-023: the within-ceiling path published no stop line — a computed "
                        f"number with no reader is ds-024's class, and this is the path where "
                        f"the number still matters. Got {n_}")
    # and it must MOVE with the wrap price — a stop line that is really a constant is a lie
    pricier = "pre-flight: fill 19% + job 10% + wrap 15% = 44% GREEN · reserve 15% ring-fenced\n"
    _f, _w, n2 = check_preflight(pricier, label="fixture")
    if not any("STOP AT 45%" in x for x in n2):
        failures.append(f"ds-023: the stop line did not move with the wrap price (15%% wrap ⇒ "
                        f"stop at {HARD_STOP} − 15 = 45), got {n2}. An expensive wrap MUST stop "
                        f"the session earlier; that is the entire mechanism")

    # ---- the ruled numbers, pinned. ALL THREE ARE DAVE'S, all from #36 except 60, which he
    # ratified at #30 and re-affirmed at #36 as "the line" and livable. ⚠ THE ONE-POINT SLACK
    # THAT SAT HERE FROM #34 IS GONE, and not because it was resolved — the question ("does 45
    # pass or fail?") stopped existing when he re-stated 45 as the band's FLOOR. A contradiction
    # can be dissolved by a better framing instead of settled by a threshold; that is the #36
    # lesson and it is why this pin now carries three numbers rather than two.
    if (BAND_FLOOR, HARD_STOP, MARKED_MAX) != (45, 60, 63):
        failures.append(f"ds-023: band = {(BAND_FLOOR, HARD_STOP, MARKED_MAX)}, ruled "
                        f"(45, 60, 63) by Dave #36 — 45–60 is the PREFERRED BAND for the FULL "
                        f"price (front-load + context GM + job + wrap), 60 is the line and is "
                        f"livable, 63 is tolerable when RARE and MARKED. Re-dialling any of "
                        f"them is his, and updating this pin is part of doing it")
    # ⚠ ABOVE 63 IS UNRULED — pinned as a KNOWN GAP so it cannot be quietly filled in later by
    # an agent the way `>= 45 -> FAIL` was at #31. If Dave rules it, this assertion is what he
    # is changing; until then the gate keeps the old escape-hatch shape and says so out loud.
    if not any("UNRULED" in x for x in check_preflight(
            "pre-flight: fill 50% + job 12% + wrap 8% = 70% RED · reserve 15% ring-fenced\n",
            label="fixture")[0]):
        failures.append("ds-023: a >63% pre-flight no longer names the UNRULED gap. That gap is "
                        "load-bearing — #31 proved an agent will fill a silence with an "
                        "enforcement Dave never picked. Say UNRULED, or get his ruling")
    # the boundaries, bitten. 45 and 60 are INCLUSIVE passes; 61+ needs a mark; >63 is unruled.
    for total, marked, want_fail in ((44, False, False), (45, False, False), (59, False, False),
                                     (60, False, False), (61, False, True), (61, True, False),
                                     (63, False, True), (63, True, False), (64, False, True)):
        stamp = (f"pre-flight: fill {total - 20}% + job 12% + wrap 8% = {total}% "
                 f"{band_for(total)} · reserve 15% ring-fenced"
                 + (" · RESERVE SPEND — forked to Dave\n" if marked else "\n"))
        f_, _w, _n = check_preflight(stamp, label="fixture")
        got_fail = any("ds-023" in x for x in f_)
        if got_fail != want_fail:
            failures.append(f"ds-023 boundary: {total}% (marked={marked}) band-fail={got_fail}, "
                            f"ruled {want_fail} (Dave #36: {BAND_FLOOR}–{HARD_STOP} is the "
                            f"PREFERRED band and passes clean; {MARKED_MAX} tolerable when "
                            f"marked; 45 is a FLOOR, never a ceiling)")
    return failures


FAT = " ".join(f"word{i}" for i in range(120))  # ~200 tk of line, for isolating the SIZE check
#   from the LINE check: a fixture that trips both proves neither (attribute-the-diff).


def _gm_fixture(do_first=10, sec_a=10, sec_c=10, with_b=False, strata_blocks=0,
                strata_pad=0, drop=(), stamp=None, fat_c=0, fat_a=0,
                fat_banner=0, banner_extra=None, stamp_a=None, ls_text=None, latest=True):
    """Synthetic GOOD-MORNING.md for the budget bites.

    `stamp=None` ⇒ a CORRECT stamp is computed for the finished text, so the green control is
    genuinely green rather than green by omission (attribute-the-diff: a control that passes for
    the wrong reason cannot license the fixtures that fail).

    M-set additions: `fat_banner` grows the banner region (M8) · `banner_extra` injects a banner
    line, which is how the M7 growth trigger's "a banner names §A" suppressor is bitten ·
    `stamp_a` overrides the stamped §A figure (a float to claim one, `False` to omit it)."""
    out = ["# Good morning", "SIZESTAMP", ""]
    # ★ LATEST is in the fixture by DEFAULT from #33 on: after the GM-D7-am cut the banner is the
    # chain's whole GM term, so a fixture without one cannot exercise M10 at all — every bite would
    # take the UNMEASURED path and a failure-only suite would still read green. `latest=False` is
    # how the refusal path is bitten on purpose.
    if latest:
        out += ["> ## ★ LATEST — 2026-07-28 (fixture session)", "> - one session-record line", ""]
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
    # ds-021 (#34): the fixture stamps in `tape`, the canonical unit. It MUST model the canon and
    # not the legacy spelling — a fixture stamped `tk` would trip the new legacy-unit warn on every
    # bite, and the usual fix (widen the assertions to tolerate it) is how a gate gets taught to
    # accept the thing it was built to retire. The legacy path keeps its own dedicated bite below.
    a_part = "" if stamp_a in (None, False) else f"§A {stamp_a:.2f}K tape · "
    text = body.replace("SIZESTAMP", "> **size:** GM 0.00K tape · chain 0.00K tape · measured x")
    for _ in range(3):  # converges: the stamp's own length barely moves the count
        tk, _m = measure_tokens(text)
        text = body.replace("SIZESTAMP", f"> **size:** GM {tk / 1000:.2f}K tape · {a_part}"
                                         f"chain {tk / 1000:.2f}K tape · measured x")
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


def selftest_gauge_continuity():
    """ds-022 (a) bites (#34). The POSITIVE case leads, deliberately: a suite that only proves
    failures reads green after a revert that deletes the comparison entirely (#32's lesson)."""
    failures = []

    def _repo(td, gm_session, log_body):
        os.makedirs(os.path.join(td, "notes"), exist_ok=True)
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write(f"# Good morning\n\n#### 2026-07-28 #{gm_session}\nstratum body\n")
        with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
            f.write(log_body)
        return td

    with tempfile.TemporaryDirectory() as td:
        _repo(td, 34, "# log\n\n#### 2026-07-28 #33\npost-mortem\n")
        f_, _w, n_ = gauge_log_continuity(td)
        if f_:
            failures.append(f"ds-022: a COMPLETE record failed ({f_}) — the check fires on the "
                            f"good case and would be routed around within one wrap")
        if not any("the 2f split landed" in x for x in n_):
            failures.append("ds-022: the passing case said nothing — a check that is silent "
                            "when it succeeds cannot be distinguished from one that is dead")

    # ★★ THE CLOCK BITES, #37. Everything above builds GM with a stratum and NO banner, so it
    # exercises only the fallback. That is exactly how the real defect survived: the primary
    # reader was never forced, so nobody found out it was broken. These three force it.
    def _repo_bannered(td, banner_n, stratum_n, log_body):
        os.makedirs(os.path.join(td, "notes"), exist_ok=True)
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            # ⚠ The decoy is DELIBERATELY first in the file, mimicking GM's real header, where
            # prose naming "★ LATEST" precedes the actual banner. The old unanchored regex
            # returned #29 from a line of this exact shape on the live repo.
            f.write("# Good morning\n\n> **read the chain — header + ★ LATEST + the LS "
                    "delta** (#29→#36: eight consecutive).\n\n"
                    f"> ## ★ LATEST — 2026-07-29 (Wed **morning #{banner_n}**, OPUS solo)\n\n"
                    f"#### 2026-07-28 #{stratum_n}\nstratum body\n")
        with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
            f.write(log_body)
        return td

    with tempfile.TemporaryDirectory() as td:
        # (i) the banner is the SOURCE and the decoy prose must not win.
        _repo_bannered(td, 34, 34, "# log\n\n#### 2026-07-28 #33\npost-mortem\n")
        got = _current_session_no(open(os.path.join(td, "GOOD-MORNING.md"),
                                       encoding="utf-8").read())
        if got != 34:
            failures.append(f"ds-022 clock: banner reader returned {got}, expected 34. If it "
                            f"returned 29 it matched the DECOY PROSE — the #37 defect exactly: "
                            f"match the blockquoted heading STRUCTURE, never the words")
        f_, _w, _n = gauge_log_continuity(td)
        if f_:
            failures.append(f"ds-022 clock: banner and stratum AGREE at 34 and the record is "
                            f"complete, but the check failed ({f_})")

    with tempfile.TemporaryDirectory() as td:
        # (ii) ★ THE SELF-HIDING CASE. Banner #36, stratum #35 — 2f was skipped, and #35's block
        # is missing. Pre-#37 this reported GREEN because the clock came from the stratum and
        # so validated #34. It must now fail on the DISAGREEMENT, independently of the block.
        _repo_bannered(td, 36, 35, "# log\n\n#### 2026-07-28 #34\npost-mortem\n")
        f_, _w, _n = gauge_log_continuity(td)
        if not any("did not run" in x for x in f_):
            failures.append("ds-022 clock: banner #36 vs stratum #35 did not fail. This is the "
                            "#37 finding itself — an auditor taking its clock from the artefact "
                            "it audits freezes at the last compliant session and reports GREEN "
                            "forever. The disagreement IS the signal that step 2f was skipped")

    with tempfile.TemporaryDirectory() as td:
        # (iii) and the fallback must still work when there is genuinely no banner, or every
        # pre-#37 fixture above silently stops testing anything.
        _repo(td, 34, "# log\n\n#### 2026-07-28 #33\npost-mortem\n")
        if _current_session_no(open(os.path.join(td, "GOOD-MORNING.md"),
                                    encoding="utf-8").read()) != 34:
            failures.append("ds-022 clock: with no banner present the stratum fallback did not "
                            "fire — a degraded path that stops working is worse than none")

    with tempfile.TemporaryDirectory() as td:
        _repo(td, 34, "# log\n\n#### 2026-07-28 #31\npost-mortem\n")
        f_, _w, _n = gauge_log_continuity(td)
        if not any("left NO block" in x for x in f_):
            failures.append("ds-022: a MISSING N−1 block did not fail — this is the #26/#28/#29 "
                            "defect itself, and the reason #29's overrun cause is unrecoverable")

    with tempfile.TemporaryDirectory() as td:
        _repo(td, 34, "# log\n\n#### 2026-07-28 #31\nx\n\nHOLE #33 — lane wrap, no stratum\n")
        f_, _w, n_ = gauge_log_continuity(td)
        if f_:
            failures.append(f"ds-022: a DECLARED HOLE still failed ({f_}) — without the escape "
                            f"hatch this gate blocks correct behaviour, and a gate that fails "
                            f"on correct behaviour teaches sessions to fake blocks, which "
                            f"poisons the dataset the reserve is re-derived from")
        if not any("DECLARED HOLE" in x for x in n_):
            failures.append("ds-022: the hole was accepted SILENTLY — #14 is countable precisely "
                            "because its absence was said out loud")

    # ★ ABSENT is the THIRD state (Dave #34) and must behave as NEITHER of the other two: it
    # cannot FAIL (the gap is historical and unfixable) and it cannot pass SILENTLY (that would
    # make it a free skip for 2f, i.e. HOLE without the honesty).
    with tempfile.TemporaryDirectory() as td:
        _repo(td, 34, "# log\n\n#### 2026-07-28 #31\nx\n\nABSENT #33 — no block found; cause unknown\n")
        f_, w_, _n = gauge_log_continuity(td)
        if f_:
            failures.append(f"ds-022: ABSENT still FAILED ({f_}) — the four historical gaps can "
                            f"never be filled, so a failing ABSENT blocks every future wrap")
        if not any("ABSENT" in x for x in w_):
            failures.append("ds-022: ABSENT passed SILENTLY — it would become a free skip for "
                            "step 2f, which is HOLE with the honesty removed")

    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"), exist_ok=True)
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write("# Good morning\n\nno session number anywhere\n")
        with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
            f.write("# log\n")
        f_, w_, _n = gauge_log_continuity(td)
        if f_ or not any("UNARMED" in x for x in w_):
            failures.append("ds-022: an unreadable session number did not announce itself as "
                            "UNARMED — an unmeasurable check must say so, never pass quietly "
                            "(the M10 refusal pattern)")
    return failures


def selftest_units():
    """ds-021 bites (#34). The unit machinery is now load-bearing for EVERY cap in this file, so
    it gets the full treatment: the legacy-unit warn must FIRE, the canonical form must be
    SILENT, and the derived/measured distinction must survive rendering — an unmarked derived
    number is the exact defect ds-021 was raised about, so a formatter that loses the marking
    reintroduces the bug in the tool built to fix it."""
    failures = []

    # ---- 1. THE POSITIVE CONTROL FIRST. A failure-only suite reads green after a revert that
    # deletes the whole comparison (the #32 lesson, and the reason index-freshness leads with its
    # fresh-passes bite). Prove the canonical stamp is accepted AND quiet.
    with tempfile.TemporaryDirectory() as td:
        _f, w_, _n = _warns_for(td)
        if any("spells the measured unit" in x for x in w_):
            failures.append("ds-021: the canonical `tape` stamp tripped the LEGACY warn — the "
                            "gate is now warning about its own canon, which will train sessions "
                            "to ignore the message")

    # ---- 2. THE LEGACY FORM MUST BITE. Accepted, but never silently.
    with tempfile.TemporaryDirectory() as td:
        _f, w_, _n = _warns_for(td, stamp="> **size:** GM 1.00K tk · chain 1.00K tk · measured x")
        if not any("spells the measured unit" in x for x in w_):
            failures.append("ds-021: a `tk`-spelled stamp did NOT warn — the legacy unit would "
                            "then survive forever behind a regex that quietly accepts it, which "
                            "is the ds-024 class (a tolerance nobody is accountable for)")
        # and it must still PARSE, or the transition blocks the wrap that performs it
        if any("carries no GM figure" in x for x in _f):
            failures.append("ds-021: the legacy stamp stopped parsing — the migration would "
                            "block the very wrap that rewrites the stamp")

    # ---- 3. DERIVED vs MEASURED must be visible in the rendering, not just in the caller's head.
    derived, measured = fmt_units(1000), fmt_units(1000, 1570)
    if "derived" not in derived or "PROVISIONAL" not in derived:
        failures.append(f"ds-021: fmt_units() rendered a DERIVED bill without marking it "
                        f"({derived!r}) — an unmarked derived number reads as a measurement, "
                        f"which is ds-021 itself")
    if "measured" not in measured or "derived" in measured:
        failures.append(f"ds-021: fmt_units() mislabelled a MEASURED pair ({measured!r})")
    if "tape" not in derived or "bill" not in derived:
        failures.append(f"ds-021: fmt_units() emitted a number without naming its unit "
                        f"({derived!r}) — the one thing this ruling exists to prevent")

    # ---- 4. The ratio must announce its own provisionality, and must FLIP to a fork when the
    # evidence firms. A constant that hardens by being carried long enough is the prose-drift
    # class; this is the check that makes n=4 arrive as a question to Dave rather than as silence.
    if "PROVISIONAL" not in ratio_status():
        failures.append(f"ds-021: ratio_status() does not declare itself provisional at "
                        f"n={len(MEASURED_PAIRS)} — below RATIO_FIRM_N it always must")
    saved = MEASURED_PAIRS[:]
    try:
        MEASURED_PAIRS.extend([("fixture-a", 1000, 1550, "2026-07-28", 34),
                               ("fixture-b", 1000, 1560, "2026-07-28", 34)])
        firm = ratio_status()
        if "PUT THE CONSTANT TO DAVE" not in firm:
            failures.append(f"ds-021: at n={len(MEASURED_PAIRS)} the ratio did not fork to Dave "
                            f"({firm!r}) — the engine never derives-and-promotes, so reaching "
                            f"the evidence threshold has to SAY something or nothing happens")
    finally:
        MEASURED_PAIRS[:] = saved

    return failures


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

        # ---- M10, RE-POINTED #33: the chain is header + ★ LATEST + the LS latest delta.
        # The fixture repo has no _LIVE-STATE, so chain == the GM banner term alone.
        #
        # ★ THE POSITIVE BITE COMES FIRST, AND IT IS THE LOAD-BEARING ONE. A failure-only suite
        # survives a revert that deletes the whole comparison: if `read_chain_tk` were reverted to
        # returning None, every "did it warn?" bite below would still pass, because an UNMEASURED
        # chain never warns. This bite proves the measurement HAPPENS and reports a number.
        _f, _w, n = _warns_for(td)
        chain_note = next((x for x in n if "READ CHAIN" in x), None)
        if chain_note is None:
            failures.append("M10: no READ CHAIN note published at all — the measurement is gone")
        elif "UNMEASURED" in chain_note:
            failures.append(f"M10 POSITIVE BITE: an ordinary fixture reported the chain as "
                            f"UNMEASURED — the measurement is broken and every warn-bite below "
                            f"would pass anyway. Note was: {chain_note}")
        elif not re.search(r"READ CHAIN \d+ tk", chain_note):
            failures.append(f"M10 POSITIVE BITE: the chain note carries no number — {chain_note}")

        # ★ THE RE-POINT CONTROL. Under the OLD definition (GM + LS whole) a fat §A/§C blew the
        # chain budget. Under the new one they are not in the chain at all. This bite is what
        # proves the re-point actually took, rather than the constant merely having been edited.
        _f, w, _n = _warns_for(td, fat_c=5, fat_a=160)
        if any("M10 read chain" in x for x in w):
            failures.append("M10: a fat §A/§C warned the CHAIN — the re-point did not take. "
                            "After the GM-D7-am cut (#33) §A and §C are retrieval, not chain; "
                            "if they still charge the chain the budget measures the old contract.")

        # …and the chain DOES bite on the region that is actually in it: the banner.
        _f, w, _n = _warns_for(td, fat_banner=24)
        if not any("M10 read chain" in x for x in w):
            failures.append("M10: a 24-fat-line banner did not warn the chain — the budget does "
                            "not bite on the one region the chain is made of")
        f, _w, _n = _warns_for(td, fat_banner=24)
        if any("M10 read chain" in x for x in f):
            failures.append("M10: a chain finding reached FAILS — ADVISORY by ruling (Dave "
                            "2026-07-27 #18), and #33's re-pointed numbers are agent-derived and "
                            "still awaiting him. It may not block.")
        _f, w, _n = _warns_for(td)
        if any("M10 read chain" in x for x in w):
            failures.append("M10: an ordinary chain warned — the budget fires on everything")
        # the remedy text must NOT prescribe a region: measured at enactment, the deltas the old
        # text pointed at could not have paid the difference. Pin the correction.
        _f, w, _n = _warns_for(td, fat_banner=24)
        if any("step 2d" in x for x in w if "M10 read chain" in x):
            failures.append("M10: the chain warn prescribes rolling deltas again — it knows the "
                            "total, not where the weight sits")

        # ★ THE REFUSAL PATH. No ★ LATEST banner ⇒ UNMEASURED and SAID SO — never 0, never green.
        _f, w, n = _warns_for(td, latest=False)
        if not any("UNMEASURED" in x for x in list(w) + list(n)):
            failures.append("M10: a GOOD-MORNING with no ★ LATEST banner did not report the chain "
                            "UNMEASURED — a budget that defaults to zero on a parse failure reads "
                            "GREEN on a broken file")

        # ---- The CORPUS rides alongside and must be published on every wrap, warned or not:
        # the cut deferred the corpus, it did not shrink it, and a report that dropped it would
        # let a 90% cheaper chain read as a 90% smaller record.
        _f, _w, n = _warns_for(td)
        if not any("corpus" in x for x in n):
            failures.append("M10: the corpus figure is not published — the chain got cheap, the "
                            "corpus got DEFERRED; hiding it repeats the exclusion D7 warned about")

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
    # ⚠ #33: CHAIN_BUDGET_TK was RE-POINTED, not re-dialled. The pin fired when the numbers moved
    # and it was RIGHT to — that is the whole point of it. What changed is the REFERENT: Dave ruled
    # the eager read chain cut, so "the chain" stopped meaning GM + _LIVE-STATE whole (34,094 tk)
    # and started meaning header + ★ LATEST + the LS latest delta (3,410 tk, measured at the cut).
    # The 2026-07-27 numbers described a measurement the repo has retired; keeping them would pin
    # the gate to a contract that no longer exists. The new numbers are AGENT-DERIVED from a single
    # measurement and are ADVISORY UNTIL DAVE RULES THEM. Both are kept here so the re-point can
    # never be read as a quiet re-dial, and so the old ruling stays legible after the change.
    for name, got, want, note in (
            ("CHAIN_BUDGET_TK", CHAIN_BUDGET_TK, (4500, 6000),
             "RE-POINTED #33 2026-07-28 — was (24000, 28000) against the GM+LS-whole referent, "
             "ruled 2026-07-27 M-set. New values AGENT-DERIVED, ADVISORY, awaiting Dave"),
            ("BANNER_BUDGET_TK", BANNER_BUDGET_TK, (4000, 5000), "ruled 2026-07-27 M-set"),
            ("SECTION_A_WARN_TK", SECTION_A_WARN_TK, 4500, "ruled 2026-07-27 M-set"),
            ("CORPUS_BUDGET_TK", CORPUS_BUDGET_TK, 36000,
             "born #33 2026-07-28, AGENT-DERIVED from 34,094 tk measured, warn-only, awaiting Dave"),
            # ds-021, enacted #34. The ratio is the load-bearing number now — every cap in this
            # file binds through it — so it gets the same pin as the caps it converts. ⚠ It is
            # PROVISIONAL at n=2 and firming it is a RULING, not a re-dial: when n>=4, the
            # constant goes to Dave and this pin moves with his word, not with the arithmetic.
            # #35, the series reader. ADVISORY at birth BY DESIGN — a threshold nobody ruled
            # must not block a wrap. Pinned so the flag and this line move as a PAIR: the
            # promotion is Dave ruling the candidate list, never a quiet flip.
            ("USAGE_HISTORY_BLOCKING", USAGE_HISTORY_BLOCKING, False,
             "born #35 2026-07-29 — ADVISORY until Dave rules OFFLOAD/TRIM/KEEP per candidate"),
            ("_gm_usage.DEFER_STREAK", __import__("_gm_usage").DEFER_STREAK, 6,
             "born #35 2026-07-29 — AGENT-PROPOSED, one below the smallest measured "
             "never-cited streak; moving it is Dave's, and the full table publishes regardless"),
            ("TAPE_TO_BILL", TAPE_TO_BILL, 1.57,
             "ds-021 enacted #34 2026-07-28 — GM's OWN measured pair (16,107 tape → 25,355 "
             "bill), deliberately NOT the 1.55 corpus average. PROVISIONAL at n=2"),
            ("RATIO_FIRM_N", RATIO_FIRM_N, 4,
             "ds-021 (c) folded in as standing practice — the ratio may not be ruled a corpus "
             "constant below n=4 measured pairs"),
            # The two seed pairs are the EVIDENCE the ratio rests on. MEASURED_PAIRS is
            # append-only, so the pin covers the seeds by value and never the list length —
            # pinning the length would fire on every legitimate wrap that logs a pair, which is
            # how a gate teaches sessions to stop logging.
            ("MEASURED_PAIRS[:2]", MEASURED_PAIRS[:2],
             [("GOOD-MORNING.md", 16107, 25355, "2026-07-28", 30),
              ("_LIVE-STATE.md", 18818, 29103, "2026-07-28", 30)],
             "ds-021's founding measurement, #30 — append below it, never edit it")):
        if got != want:
            failures.append(f"{name} = {got}, pinned {want} ({note}) — re-dialling is Dave's, "
                            f"and updating this pin is part of doing it")
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
    failures = (selftest_preflight() + selftest_budgets() + selftest_units()
                + selftest_gauge_continuity() + selftest_growth() + selftest_usage()
                + selftest_lanes() + selftest_receipts() + selftest_index_freshness())
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
