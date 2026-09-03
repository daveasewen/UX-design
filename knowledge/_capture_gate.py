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

Usage:  python3 knowledge/_capture_gate.py --build     # build mode (blocking) — THE ONLY WRITER
        python3 knowledge/_capture_gate.py --wrap      # wrap mode (session-run), stdout only
        python3 knowledge/_capture_gate.py --wrap --lane  # lane session wrap (skips GM check)
        python3 knowledge/_capture_gate.py --rehearse  # #92 early wrap-gate run, stdout + log
        python3 knowledge/_capture_gate.py --selftest  # bite-test, one fixture per FAIL class
Build mode writes _CAPTURE-GATE.md; wrap mode is stdout-only (S-D3). Exits non-zero on any FAIL.
⛔ ARGV IS A CONTRACT (#218, the #158 write-by-default class): a BARE run and any UNRECOGNISED
flag are REFUSED with exit 2 — they used to fall through to build mode and rewrite the committed
report. `--build` is the only argv that writes; see `argv_refusal()` and its selftest."""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import ast                              # #82: the real-tier check must read STRUCTURE, not text
import datetime
import difflib                           # s188-D2: the 2c carry gate's PAIRING guard (only)
import glob
import hashlib
import importlib
import json                             # #92: the rehearsal log is JSONL, machine lines only
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gauge_tokens as gauge     # noqa: E402 — the UNIT and the BUDGET (Dave #56)
import _roll_state as roll_state  # noqa: E402 — T1 (#77): the roll-residual MEASURER. Imported,
#   never re-derived — roll_claim_check() below is T2, and "one measurer, no second slicer" is
#   the whole point of the split (handoff-testing-regime plan § T2).

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
# (The % BANDS / WRAP_FLOOR / RESERVE_FENCE constants that sat here were RETIRED with the %
#  enforcement path — #74-D3, Dave. History: ledger § #36 / § ★ #74; runbook ds-023 sections.)
# ⚠ THE `#NN` IS NOT COSMETIC — IT WAS A SILENT MIS-TARGET, FOUND #56 WHILE MUTATION-TESTING.
# Banners have written `pre-flight #55:` for many sessions; this regex only accepted a bare
# `pre-flight:`, so `next(...)` skipped the LIVE ★ LATEST stamp at the top of the file and
# matched the first ARCHIVED STRATUM instead — blocks from sessions #49–#51 that say "FIFTH
# consecutive", "SIXTH consecutive" and can never go green because they are ratified history.
# ⇒ For those sessions the pre-flight FAIL was UNFIXABLE BY CONSTRUCTION: writing a perfect
# stamp today could not clear a failure being read off a stratum written weeks earlier.
# ★ [[unmatched-grep-is-not-an-absence]]'s THIRD FACE, live: the check MATCHED, so nothing
# looked broken — but it matched the wrong line, and a matched pattern is not the right pattern.
PREFLIGHT_RE = re.compile(r"^\s*>?\s*\**pre-?flight\**(\s*#\d+)?\**(\s*\([^)]*\))?\**\s*[:—-]", re.I)
# ★ #74 — FIRST-MATCH ATTRIBUTION (the (h) residual, DECLARED at #73). Keyed on the LIVE banner's
# `**#N**` form deliberately: `_gm_fixture`'s banner (`★ LATEST — … (fixture session)`) carries no
# session number, so every existing bare-stamp fixture is graded exactly as before (the #60/affe15d
# lesson — a new check must not orphan the fixture corpus it will be tested against).
LATEST_SESSION_RE = re.compile(r"^\s*>\s*##\s*★\s*LATEST\b[^\n]*?\*\*#(\d+)\*\*", re.M)
# ★ #73 — THE LEGAL REFUSAL FORM for this check (#62's remedy applied to the check that lacked
# it; proposed #72 item (h), enacted on Dave's word #73). A session that declared no pre-flight
# at its opener CANNOT reconstruct one honestly — every number would be invented after the fact,
# and a gate that fails honest behaviour teaches sessions to invent numbers. The exact quoted
# form is the ONLY legal refusal: the glyph run `⛔ NOT CAPTURED — UNMEASURED.` followed by a
# stated reason. Scoped to the exact form so it BITES BOTH WAYS: a near-miss wording FAILS with
# the legal form quoted, a reasonless refusal FAILS, and a line that both refuses and asserts
# numbers FAILS as contradictory testimony. A declared gap passes (as a WARN, staying visible);
# a silent one fails — that asymmetry is the mechanism (Dave #56).
PREFLIGHT_UNMEASURED_RE = re.compile(r"⛔ NOT CAPTURED — UNMEASURED\.\s*\S")
TERM_RE = {k: re.compile(r"\b%s\b\D{0,4}(\d+)" % k, re.I) for k in ("fill", "job", "wrap")}
TOTAL_RE = re.compile(r"=\s*[~≈]?\s*(\d+)")
BAND_WORD_RE = re.compile(r"\b(GREEN|AMBER|RED)\b", re.I)  # used by the #56 TOKEN path

# ------------------------------------------------------------------- ds-023 — RETIRED IN CODE
# ⛔ THE % BAND'S ENFORCEMENT (pins 45/60/63, the grading branch, `band_for`, its fixtures and
# selftest pins) was RETIRED #74-D3 — Dave, explicit option-select, closing the fork standing
# since #58. The path had been DORMANT since #57 (the live stamp is #56's token form) and a
# dormant enforcement is a claim that stopped being true; its one live surface was teaching the
# RETIRED unit in every wrap's notes. ★ THE RULING HISTORY IS NOT DELETED — Dave's #30/#31/#34/
# #36 words, the band's shape, and the delegated-enforcement lesson live in
# `notes/_MEMENTO-DECISIONS.md` (§ #36, § ★ #74) and the runbook's ds-023 sections. What the
# band was FOR — the wrap paid inside the number, the stop line that moves with the wrap price,
# the marked-and-forked escape hatch — carries forward in the #56 TOKEN path below, in real
# tokens (amber 160,000 · working 200,000 · hard 256,000).
# ⚠ The escape-hatch marker survives the retirement because the TOKEN path uses it: crossing
# the working budget is a QUESTION PUT TO DAVE, so the marker names him.
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

# ★ #110-D3 (Dave) — the boot-ceiling gate, BLOCKING at birth.
# Tier is deliberately not WARN. #109 measured `BOOT_HARNESS_EST` sitting 5.6x outside
# its own error bar for ~72 sessions; the constant carried its own "RE-MEASURE WHEN THE
# SESSION SHAPE CHANGES" warning and nothing ever read it. An advisory gate would have
# been one more unread warning [[instrument-without-a-consumer]]. ⚠ Dave has NOT ruled
# warn-vs-block on this one — it is an agent's call pending his word, named here so it
# is visible rather than buried in a tier lookup.
BOOT_DRIFT_BLOCKING = True

# 2f: the session-strata stack. It is excluded from §C's cap by D6(a) — which is only checkable if
# it is DELIMITED, so 2f requires the marker below. ⚠ Excluding a region from a cap without giving
# it a rule of its own is precisely how "splitting buys headroom"; the region's rule is D5(a) —
# GM keeps LATEST ONLY — so the gate counts blocks, not lines. One block is the whole contract.
STRATA_HEAD_RE = re.compile(r"^###\s*⏱\s*SESSION STRATA\b", re.I)
STRATA_BLOCK_RE = re.compile(r"^####\s")
STRATA_MAX_BLOCKS = 1
# #58 (Dave, verbatim, this ruling): "Exempt #40/#41/#42 by name and keep the cap at 1 for live
# strata. They're unrollable for a recorded reason (_GAUGE-LOG.md:399 — keys added
# retroactively), so that's a known permanent condition. Name it, don't bury it in a
# threshold." STRATA_MAX_BLOCKS above binds LIVE blocks only, from this ruling on — the three
# below are the PERMANENT FLOOR these three sessions sit at, not headroom to spend.
#
# WHY THEY ARE PERMANENT, not drift: #40/#41/#42 each wrote real testimony into
# notes/_GAUGE-LOG.md at their own wrap, but never wrote the `#### <date> #<N>` key that marks
# it filed — see notes/_GAUGE-LOG.md:399 ("key added retroactively") and the standing record at
# notes/_GAUGE-LOG.md § "META — UNKEYED #40 #41 #42" (Dave's ruling #54: gate the state shut,
# name the three, never mint a standing fourth vocabulary term for it). The missing keys were
# patched in retroactively to quiet a DIFFERENT check (ds-022 continuity) — so
# notes/_GAUGE-LOG.md now already carries `#40`/`#41`/`#42` as keys, and `_gm_move.py`'s
# `roll_2f` duplicate-key guard (knowledge/_gm_move.py ~line 320, "already carries a block for
# #N") correctly REFUSES to roll them: doing so would split one session's record across two
# places. The guard is right; the blocks are stuck; waiting does not change that.
#
# ⚠ NOT RAISED TO 4 (Dave, same ruling, verbatim): "Not raising the cap to 4 — that's a cap at
# its own floor with no headroom, and #57 skipped 2f the night before, which would have taken
# it straight to 5." A cap sized to exactly today's permanent floor leaves no room for a genuine
# SECOND live block ever to coexist with the three ([[m8-cap-at-its-own-floor]] is the standing
# name for that mistake). The fix is naming the floor and excluding it — the same shape as
# SECTION_EXEMPT below (~line 1261: "measured and reported, never charged").
#
# ⛔ A CLOSED LIST OF THREE, NOT A LICENCE TO ACCUMULATE (Dave, verbatim): "the exemption is a
# named list of three, not a licence to accumulate: if a fourth unrollable block ever turns up,
# fail loud and come back to me." Do NOT add a fourth key here to silence a future FAIL —
# check_budgets() below carries a dedicated fail-loud check that cross-references
# notes/_GAUGE-LOG.md for exactly this condition rather than absorbing it quietly.
STRATA_EXEMPT = {40, 41, 42, 95, 96}   # int form — matches _key_session()'s return type, read below
# ⚠ 95/96 added on DAVE'S #96-D4 ruling (ONE WRITER: only roll_2f writes gauge-log sections;
# pre-existing collisions are marked exceptions by addition, not merged). The #58 list of three
# was CLOSED; extending it took his word — notes/_MEMENTO-DECISIONS.md § ★ #96-D4.
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
    """The HIGHEST §C stratum key's session number, or None. This is written by ritual step 2f.

    ★★ #44 — RULED BY DAVE: HIGHEST NUMBER WINS, FILE ORDER IS NOT CONSULTED.
    This used to return the FIRST `STRATA_KEY_RE` match and call it "the newest". That is only
    true in a file stacked newest-first, and GM's §C strata are stacked OLDEST-first — so at the
    five blocks live when this was found (#38 #40 #41 #42 #43) it returned **38** and told
    ds-022 that step 2f had not run when it had. ⚠ The remedy line ds-022 prints in that state
    invites a `HOLE #<N>` row for a session that is not missing — i.e. the false read was one
    step from FORGING a row, which the #43 ruling on present-but-unkeyed forbids.

    ⚠ Do NOT "fix" this class by reordering a file to suit its reader. Dave's ruling dissolves
    the ordering question here rather than settling it: max() is correct in a file stacked
    either way, and cannot silently break when an order changes. The naming ("which end is
    newest") remains UNRULED for `roll_2f` and the archives, which stack the other way."""
    nos = [n for n in (_key_session(ln) for ln in gm_text.splitlines()
                       if STRATA_KEY_RE.match(ln)) if n is not None]
    return max(nos) if nos else None


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
# ⛔ AMENDED 2026-07-29 #39, RULED BY DAVE — THE BLOCK IS WITHDRAWN, THE WARN STANDS.
# The comment above states this cap's purpose in its own words: *"true cold-start cost."* That was
# correct when written on 2026-07-27. **#33 then CUT the read chain** (2026-07-28), and a cold session
# now reads three things — GM header → ★ LATEST → the ⏱ LATEST delta of `_LIVE-STATE.md`.
# MEASURED #39 (Lane A, tiktoken cl100k): chain 4,801 tape · compactable 12,734 tape.
# ⇒ **~8,000 of the tape this cap governs is NEVER PAID AT BOOT.** It is retrieval surface: growth
# here costs a retrieval, not a cold start. The cap has been charging boot prices for a queue.
#
# ★ WHY A BLOCK HERE WAS ACTIVELY HARMFUL, not merely inert. The block fires at WRAP — after the
# session's record is written — so the only response available is to cut something already written.
# #35 did six trimming rounds, #38 did three, and the region grew through both. #38 measured the
# reason: retiring a VERIFIED-DEAD item netted **+16 tape**, because a retirement must leave a
# legible clause and the clause costs what the line cost. ⇒ the region has a FLOOR that retirement
# cannot lower, the block cannot be satisfied by removing dead weight, and the only thing left to
# cut is live record. **The gate was inside the growth loop, not braking it.**
#
# ⚠ WHAT IS *NOT* CLAIMED, and the ds-023 precedent is why this is spelled out. NOT that GM should
# grow unbounded. NOT that 8,000/12,000 were wrong numbers — they may be exactly right for the CHAIN,
# which is untested. The shape (`budget applies to the compactable region`) remains Dave's D8(a).
# What is withdrawn is one thing only: **a BLOCK on a region whose growth is free at boot.**
# ds-023 is the standing cautionary case — there, an enforcement Dave never ruled hardened into a
# gate. Here the enforcement is being removed by Dave's word, #39, and recorded as his.
#
# ⬛ THE REPLACEMENT IS OWED, NOT DONE — Thursday's brief, and this comment is the receipt for that.
# The expensive region (M10 `read_chain_tk`, 4,801 tape) is still ADVISORY. Un-blocking the free
# region without blocking the costly one leaves NOTHING binding on cold-start cost. That swap is the
# job: block what costs, warn on what does not. Until it lands, a session can grow the chain unchecked
# — **this is a KNOWN, DECLARED gap for ~one day, not an oversight.**
# ⚠ AND THE STANDING WARNING, Dave #39, in his words: *"we've done this before, assumed everything is
# okay just for everything to grunge up again."* The WARN below is deliberately kept for that reason —
# an un-instrumented region is how the compactable region reached 21K before anyone looked (line 357).
SIZE_BUDGET_TK = {"compactable": 8000, "compactable_block": None}
#   "compactable"       — WARN threshold, tape. Dave's D7 amendment 2026-07-27, UNCHANGED.
#   "compactable_block" — BLOCK threshold, tape. `None` = ADVISORY, no block. Withdrawn #39.
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


# ============================================ ds-021 (C) — THE CROSS-INSTRUMENT UNIT GATE
# RULED #81-D1 (Dave), shape (C) of four, with his condition attached verbatim: *"be careful,
# i want rigorousness, check for peripheral effects."* ⚠ THE UNIT ITSELF WAS NOT REOPENED — he
# ruled it at #54 (ONE unit, real tokens; `cl100k` a labelled estimator, "never a unit a cap is
# stated in"). Only the ENACTMENT SHAPE was open. Blast-radius sweep, run BEFORE this code:
# `notes/2026-08-02-81-cross-instrument-gate-blast-radius.md`.
#
# ⛔ WHY (C) AND NOT A BIGGER FIX — and it is the finding that picked the shape. MEASURED #81,
# same input, same process: `_gauge_tokens.count()` reads `_CHAIN.md` at 10,766 tokens method
# 'real'; `measure_tokens()` below reads the same file at 6,816, method 'tiktoken cl100k_base'.
# `_capture_gate.py:58` ALREADY imports `_gauge_tokens as gauge`. The real measurer is in this
# file's own namespace and every size stamp is produced by the other one. The defect was never a
# missing capability — it is TWO INSTRUMENTS IN ONE PROCESS DISAGREEING ABOUT WHAT THEY MEASURE,
# with nothing in the repo positioned to notice. That is what this gate watches.
#
# ★ WHAT IT CHECKS IS PRESENCE, NEVER THE LIVE READING. The tempting gate — "every size claim
# must be a REAL measurement" — REFUSES A CORRECT STATE: a sandbox with no key and no network
# can only estimate, honestly, and #79-D1 already ruled that an honest refusal is right there.
# Such a gate would make the build unrunnable offline. Same class as ds-022 (d) vs `roll_2f`:
# a new gate making a correct state unreachable. So: gate the VOCABULARY, not the number.
#
# ★★ AND THE ASYMMETRY IS THE PROJECT'S OWN — a DECLARED gap passes, a SILENT one fails.
# An estimate-only measurer that SAYS SO is a WARN and ships. An unregistered one is a FAIL.

TOKEN_COUNT_CALL_RE = re.compile(r"""get_encoding\(\s*["']cl100k_base["']\s*\)""")

# ⚠ SCOPED TO A `return`, DELIBERATELY. Matching a bare "real" anywhere would be satisfied by
# this very comment block — the USE-vs-MENTION problem, which no syntax reaches and only SCOPE
# saves. A method value is something a function RETURNS; that is the only form checked.
REAL_TIER_RE = re.compile(r"^\s*return\b.*['\"]real['\"]", re.M)


def _produces_real_tier(src):
    """True iff `src` contains a RETURN whose value is a TUPLE ending in the literal `'real'`.

    ⛔ BORN FROM A MUTATION THAT SHOULD HAVE BITTEN AND DID NOT (#82). `REAL_TIER_RE` above is
    scoped to a `return`, which closed the USE-vs-MENTION hole #81 correctly worried about — a
    comment merely SAYING "real" cannot satisfy it. It does not close the two holes underneath:

      1. **A CLASSIFIER IS NOT A PRODUCER.** `_tier_of()` ends `return "real"` — it SORTS method
         strings, it never measures anything. Deleting the real tier out of `measure_tokens()`
         left that line standing, so the regex still matched and the audit still read GREEN.
      2. **A TEST FIXTURE IS NOT CODE.** This file contains the string literal
         `'    return n, "real"\\n'` as a bite fixture. Scanned as text it is indistinguishable
         from the thing it is a fixture FOR.

    ★ Both holes are unreachable by any regex, because both turn on what a line IS rather than
    what it says — and that is precisely [[gate-must-quote-what-it-forbids]]'s point pushed one
    level further: where SCOPE is not enough, read the STRUCTURE. The AST knows a string constant
    is not a statement and a bare return is not a tuple; text never will.

    ★ The tuple requirement is not a trick — it is this project's own rule made checkable: *the
    method travels WITH the number, as a tuple, on purpose* (`measure_tokens`' docstring). A
    producer hands back `(n, 'real')`. Anything returning the bare word is talking ABOUT the
    tier, not reporting one.

    ⚠ `SyntaxError` PROPAGATES. A file that will not parse must not be silently regraded by a
    weaker instrument — the caller reports it by name."""
    for node in ast.walk(ast.parse(src)):
        if (isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple)
                and node.value.elts):
            last = node.value.elts[-1]
            if isinstance(last, ast.Constant) and last.value == "real":
                return True
    return False

# The registry. A file under `knowledge/` that counts tokens and is NOT named here FAILS — that
# is the half which catches the NEXT instrument, and it is the whole reason Dave picked (C).
#   'real'         — has a REAL tier; VERIFIED against source, never trusted from this table
#   'estimate-only'— declared gap: WARNS by name, every run, and does not block
#   'calibration'  — measures BOTH to compare them; not a measurer in service
MEASURERS = {
    "_gauge_tokens.py": ("real",
        "count() returns (n, 'real') from the token-counting API; cl100k is the LABELLED "
        "fallback and `len(text)//4` was removed at #79-D1 in favour of MeasurementRefused."),
    # ⛔ `_measure_tokenizer.py` — ENTRY RETIRED `s241-D2` (D4 of the #241 ritual diet, on Dave's
    # "apply"), and the FILE was `git rm`'d in the same motion, because this pin and that file
    # only make sense together: leave the pin and the loop below FAILS ("it no longer exists");
    # leave the file and the gate WARNS about a zombie at every wrap, forever. #53 built it, #77
    # flagged it at zero Python consumers, #81 re-probed and found STILL zero, and every wrap
    # since has printed that finding instead of acting on it. This is the project's own rule
    # ([[instrument-without-a-consumer]]) applied to the project's own instrument.
    # ⚠ THE PROBE, NAMED, so the deletion is falsifiable: `grep -rn "_measure_tokenizer" .`
    # returns 0 import sites; the surviving hits are PROSE (`_governs.py` ×3 quote it as the
    # cautionary tale, `notes/` records it, `knowledge/_rulings.json` names it in a ruling's
    # file list). None of those executes it.
    # ⛔ AND THE ONE CONSUMER THAT IS NOT AN IMPORT, DECLARED RATHER THAN SMOOTHED: entry 40 of
    # `notes/_dream/_MEMORY-GRADES.json` grades a memory hook on "all 6 paths named in the hook
    # FILE resolve (first: `knowledge/_measure_tokenizer.py`; probe: os.path.exists …)". That
    # grade will DROP at the next dream pass. It is a path-resolution grade, not an importer,
    # so this cut proceeds as briefed — but the hook wants re-pointing at the history that
    # replaced it, and no agent may edit Dave's memory store to hide the consequence.
    "_capture_gate.py": ("real",
        "✅ #82-D1 (Dave): measure_tokens() tries gauge.count() FIRST and returns (n, 'real'); "
        "cl100k and the bytes divisor are kept UNTOUCHED beneath it as labelled fallbacks, so "
        "an offline build still runs and #59's guards still mean what they meant. THE WORD FOR "
        "REAL NOW EXISTS HERE — measurement_tier(). ⚠ measurement_degraded() was deliberately "
        "NOT widened to 'not real': _gen_chain.py:196 consumes it as a HARD REFUSAL and would "
        "have become an offline build-killer. measurement_mixed() guards the fixed point "
        "instead. ⛔ WHAT IT WAS, kept because the entry must still carry WHY this gate exists: "
        "from #81 this file was 'estimate-only' — THE ds-021 DEFECT ITSELF. measure_tokens() "
        "could return only 'tiktoken cl100k_base' or a bytes ESTIMATE, so measurement_degraded() "
        "asked 'is this an estimate?' and cl100k answered 'no, healthy'. THE VOCABULARY HAD NO "
        "WORD FOR REAL (#80's root cause, confirmed at source #81). It was a CODE change and it "
        "moves the GM size stamps, ds-025's floor and the amber line — which is why it was "
        "priced and put to Dave rather than smuggled into #81's window."),
    "_context_gauge.py": ("estimate-only",
        "REFUSES without tiktoken unless --estimate labels the output (#74). Honest about "
        "estimate-vs-nothing; still blind to cl100k-vs-real."),
    "_checkin.py": ("real",
        "✅ #83 (c) (Dave's): the HEADLINE now runs through measure_real(), which calls "
        "gauge.count() ONCE on the whole concatenated conversation-half blob and returns "
        "(n, 'real') — never per-record; #82 measured the per-record shape at 232 API "
        "round-trips, past the 45s sandbox call wall, and count() is content-hash cached so a "
        "re-run is free. gauge.MeasurementRefused is NOT caught in this file — it propagates "
        "named to the caller rather than being swallowed into a quieter estimate. WHAT STAYED "
        "TAPE: the PER-TYPE BREAKDOWN is still tiktoken cl100k (encoder(), unchanged from D1), "
        "kept for SHAPE only — it does NOT sum to the headline and is NEVER scaled to match it "
        "(#54's defect); the footer says so explicitly on its own line."),
    "_boot_remeasure.py": ("estimate-only",
        "BUILT #214 under `s214-D5` half 2 (per-session boot re-measure over the mounted "
        "disk-resident boot inputs), and REGISTERED HERE AT THE WRAP THAT SHIPPED IT — the "
        "ds-021 (C) bite caught it unregistered on its first gate run, which is the birth-catch "
        "the bite exists for. It counts in tiktoken cl100k ONLY and can name NO real tier: its "
        "output is a TAPE PROXY kept for SHAPE and DELTA across sessions, and the row that owns "
        "it (`W-99za`) already declares exactly that — this entry MIRRORS that declaration, it "
        "does not make a new one. ⛔ Its figures are NEVER summed with, scaled to, or compared "
        "against a `real` measurement [[measure-dont-convert-units]]; the consumer is the "
        "boot-band re-base sitting, which is DAVE'S."),
    "_boot_decompose.py": ("estimate-only",
        "BUILT #242 lane F (the boot DECOMPOSITION `_boot_remeasure.py`'s two hard-coded paths "
        "could not give), REGISTERED AT THE WRAP THAT SHIPPED IT — ds-021 (C) caught it "
        "unregistered on its first gate run, which is the birth-catch the bite exists for. WHY "
        "'estimate-only': every component figure it prints is a cl100k TAPE count over the "
        "DISK-RESIDENT boot inputs; a REAL boot figure comes only from `message.usage`, which "
        "this file never sees — it takes the real total as `--real N` from the caller and prints "
        "the harness remainder as `<real> − Σ(ours, tape)` labelled ESTIMATED-BY-SUBTRACTION, "
        "because that subtraction mixes units BY CONSTRUCTION. ⛔ Its tape figures are never "
        "summed with, scaled to, or compared against a `real` measurement "
        "[[measure-dont-convert-units]]."),
    "_memory_cap_check.py": ("estimate-only",
        "BUILT #244 lane C (the mechanised `MEMORY.md` cap), REGISTERED AT #244 lane V — ds-021 "
        "(C) caught it unregistered on its first gate run, which is the birth-catch the bite "
        "exists for. WHY 'estimate-only': cl100k tape of a non-repo file; never a real-token "
        "claim. The file it grades is the Cowork auto-memory index resolved through the "
        "`/sessions/*/mnt` glob, so it is OUTSIDE the repo and no `message.usage` figure can "
        "ever be taken over it — the only reading available is a tiktoken cl100k TAPE count, "
        "kept for SHAPE and DELTA (the `s243-D1` stub measured 1,502 tape against a "
        "MEMORY_CAP_TAPE of 1,802). ⛔ Its tape figures are never summed with, scaled to, or "
        "compared against a `real` measurement [[measure-dont-convert-units]]; the arm it "
        "feeds (`memory_cap_check`) is ADVISORY (`MEMORY_CAP_BLOCKING = False`) precisely "
        "because the graded file does not exist on a non-Cowork tree "
        "[[gate-cannot-pass-in-one-environment]]."),
}


def unit_vocabulary_audit(repo):
    """The ds-021 (C) cross-instrument check. Returns `(failures, warnings)`.

    ⚠ IT READS SOURCE, NOT BEHAVIOUR, ON PURPOSE. Behaviour depends on whether tiktoken is
    installed and whether a key is present — both environmental, neither a property of the
    repo. A gate whose verdict flips with the network is not a gate. What IS a repo property:
    which files count tokens, and whether each can NAME a real tier.

    Three bites, and each fails for a DISTINCT reason:
      1. an UNREGISTERED counting site        — the next instrument, caught at birth
      2. a registry entry whose file stopped counting — the pin rotted; stale pins are how a
         green survives a deletion (#78's P0 was exactly an aged pin)
      3. a 'real' claim the source does not support — the table lying about the code
    """
    failures, warnings = [], []
    kdir = os.path.join(repo, "knowledge")
    if not os.path.isdir(kdir):
        return failures, warnings

    found = {}
    for fn in sorted(os.listdir(kdir)):
        if not fn.endswith(".py"):
            continue
        try:
            with open(os.path.join(kdir, fn), encoding="utf-8") as fh:
                src = fh.read()
        except OSError:
            continue
        # ⚠ The gate must not detect ITSELF via this very regex's own source text. The pattern
        # is built from a character class so the literal never appears here in matchable form.
        if TOKEN_COUNT_CALL_RE.search(src):
            found[fn] = src

    for fn, src in found.items():
        if fn not in MEASURERS:
            failures.append(
                f"ds-021 (C): `knowledge/{fn}` counts tokens (cl100k) and is NOT in MEASURERS "
                f"— an UNREGISTERED measurer. Every counting site declares whether it can name "
                f"a REAL tier; this one declares nothing, which is how the last one got 27 "
                f"sessions of silence. Add it to MEASURERS with 'real', 'estimate-only' or "
                f"'calibration' and say WHY.")
            continue
        tier, why = MEASURERS[fn]
        if tier == "real":
            try:
                ok = _produces_real_tier(src)
            except SyntaxError as e:
                failures.append(
                    f"ds-021 (C): `knowledge/{fn}` is pinned 'real' but will not PARSE "
                    f"({e.__class__.__name__}: {e.msg} line {e.lineno}) — a file that cannot be "
                    f"parsed must never be graded 'probably fine' by a regex that skimmed it. "
                    f"[[measuring-tool-must-not-guess]]: observe, never infer.")
                ok = True          # already reported; do not also report it as capability-less
            if not ok:
                failures.append(
                    f"ds-021 (C): MEASURERS claims `knowledge/{fn}` has a REAL tier, but its "
                    f"source contains no RETURN of the form `(…, 'real')` — the registry is "
                    f"asserting a capability the code does not have. A table that can lie about "
                    f"the code is worse than no table: it launders an estimate into a "
                    f"measurement.")
        elif tier == "estimate-only":
            warnings.append(
                f"ds-021 (C) DECLARED GAP — `knowledge/{fn}` counts in cl100k and cannot name a "
                f"REAL tier. {why}")
        elif tier == "calibration":
            warnings.append(f"ds-021 (C) CALIBRATION — `knowledge/{fn}`. {why}")

    for fn, (tier, _why) in MEASURERS.items():
        if fn not in found:
            failures.append(
                f"ds-021 (C): MEASURERS pins `knowledge/{fn}` as a '{tier}' measurer, but it no "
                f"longer counts tokens (or no longer exists). A stale pin is a green that "
                f"cannot fail — retire the entry deliberately, or restore the call site.")

    return failures, warnings


# ============================================ retired-unit PROSE AUDIT — the `.md` arm
# NEW, DELIBERATELY SEPARATE FROM `unit_vocabulary_audit` ABOVE. That function reads CODE —
# which files in `knowledge/*.py` COUNT tokens. This one reads PROSE — which files in
# `knowledge/*.md` TEACH the retired `tape`/`bill` duality (SUPERSEDED #56 — see
# `_RUNBOOK-context-gauge.md` § ⬛ RETIRED UNITS AND BANDS) without saying it is retired. Same
# family of defect — a retired thing rots unwatched wherever nothing reads it
# ([[gate-inside-the-growth-loop]]) — different corpus, different question, so a different
# function; entangling the two would make an edit to one risk the other silently.
#
# ⛔ SCOPE — Dave's condition A, LOAD-BEARING, stated here AND in every failure string below
# (his reasoning, verbatim: a gate that doesn't say what it excludes will later be read as
# "the prose is gated", which is this whole thread's founding defect eating its own tail).
# THIS COVERS `tape`/`bill` ONLY. The retired PERCENTAGE band (45%/60%/63%) is explicitly OUT
# OF SCOPE — a SEPARATE retirement with its own history section, blocked on Dave's ds-023
# re-denomination — and this audit must never be read as covering it.
RETIRED_PROSE_SCOPE_NOTE = (
    "covers `tape`/`bill` only; the retired percentage band is OUT OF SCOPE, blocked on "
    "Dave's ds-023 re-denomination")

RETIRED_PROSE_WORDS_RE = re.compile(r"(?<!duct )(?<!duct-)\b(tape|bill)\b", re.I)
# ⚠ `duct tape`/`duct-tape` EXCLUDED (s163-D1). The homonym was measured at #84 as 2 of the 11
# then-live hits and named there as "a REGEX defect ... cheaply fixable, not a refutation of the
# design"; the lookbehinds fix the WORD-SENSE, they do not exempt any unit prose — `tape` alone
# still matches everywhere else.

# ⚠ ATX HEADINGS ONLY (`#` … `######`). Surveyed all 93 `knowledge/*.md` files before writing
# this: no Setext (`===`/`---`-underlined) headings anywhere in the corpus — this is the house
# style, not an assumption.
MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

# ⚠ THE STRUCTURAL FENCE (exemption device (i)). A heading whose TEXT names one of these words
# opens a fence that runs until the next heading at EQUAL-OR-SHALLOWER depth. Pins WHERE prose
# may live, never HOW it is worded. Live example: `### ⬛ RETIRED UNITS AND BANDS — HISTORY, NOT
# INSTRUCTION` in `_RUNBOOK-context-gauge.md`.
FENCE_HEADING_RE = re.compile(r"\b(RETIRED|HISTORY|SUPERSEDED)\b", re.I)

# ⚠ ENUMERATE EXEMPTIONS, NEVER VIOLATIONS — Dave's brief, not a style choice made here. A list
# of phrases that FORGIVE is safe to extend: a false negative here is a hit that still fails
# and gets caught next run. A list of phrases that CONDEMN inverts the risk: a false negative
# there is a SILENT PASS, read next session as "clean". Same direction
# [[gate-must-quote-what-it-forbids]] chose, for the same reason. This is exemption device
# (ii), the INLINE declaration: a hit's own region (nearest preceding heading -> next heading,
# REGARDLESS of depth — this device is regional, not structural like the fence above) is
# exempt if ANY of these appear in it. Verified against the two live sections this audit must
# pass (`_RUNBOOK-context-gauge.md` § ★★ THE FLOOR IS NOT WILLPOWER and § Half 2) — every
# marker below is quoted from one of those two, not invented.
DECLARATION_MARKERS = (
    "historical",
    "HISTORY",
    "RETIRED",
    "SUPERSEDED",
    "the unit live when",
    "NOT re-denominated",
    "SHAPE ONLY",
    "sideband",
)

# ⚠ THE GATE'S OWN GENERATED OUTPUT IS NOT PROSE, AND SCANNING IT WOULD MAKE THIS AUDIT
# PERMANENTLY, UNFIXABLY RED OVER ITS OWN SIBLING'S WORDS. `_CAPTURE-GATE.md` (== REPORT) is
# rewritten WHOLE on every build; nobody authors it, so it can carry neither a heading fence
# nor an inline declaration, and `unit_vocabulary_audit`'s own WARN text legitimately quotes
# `tape` every run (`_checkin.py`'s footer, "UNIT tape/cl100k"). Same self-detection hole the
# `.py` audit above already guards against by construction (its regex is built so it cannot
# match its own source) — this is that same guard, shaped for a file instead of a literal.
_GENERATED_REPORT_BASENAME = os.path.basename(REPORT)


def _md_headings(lines):
    """[(line_idx, depth, text), ...] for every ATX heading in `lines`."""
    out = []
    for i, ln in enumerate(lines):
        m = MD_HEADING_RE.match(ln)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


def _md_fence_spans(headings, n_lines):
    """Exemption device (i). [(start, end), ...] half-open line-index spans, one per heading
    whose text matches `FENCE_HEADING_RE`, each running to the next heading at
    equal-or-shallower depth (or EOF)."""
    spans = []
    for idx, (i, depth, text) in enumerate(headings):
        if not FENCE_HEADING_RE.search(text):
            continue
        end = n_lines
        for j, depth2, _t in headings[idx + 1:]:
            if depth2 <= depth:
                end = j
                break
        spans.append((i, end))
    return spans


def _md_region(headings, line_no, n_lines):
    """Exemption device (ii)'s region for one hit at `line_no`: (start, end, heading_text) =
    nearest preceding heading (any depth) -> next heading (any depth). Deliberately NOT
    depth-aware — device (ii) is regional, only device (i) above is structural."""
    start, end, heading_text = 0, n_lines, "(no heading above this line)"
    for i, _depth, text in headings:
        if i <= line_no:
            start, heading_text = i, text
        else:
            end = i
            break
    return start, end, heading_text


def retired_unit_prose_audit(repo):
    """The `.md` arm of the retired-unit vocabulary audit. Sibling to `unit_vocabulary_audit`
    above, deliberately not entangled with it. Returns `(failures, warnings)`.

    ⛔ SCOPE: covers `tape`/`bill` ONLY; the retired percentage band is OUT OF SCOPE, blocked
    on Dave's ds-023 re-denomination (his condition A — a gate that doesn't say what it
    excludes will later be read as "the prose is gated", which is this whole thread's founding
    defect eating its own tail). Every failure string below repeats this line for the same
    reason it is repeated here: a scope statement that lives in only one place is a scope
    statement one deletion away from silently widening.

    `unit_vocabulary_audit` reads CODE: which files in `knowledge/*.py` COUNT tokens. This
    reads PROSE: which files in `knowledge/*.md` TEACH `tape`/`bill` (SUPERSEDED #56) without
    saying so. A hit is exempt two ways, both author-declared, never inferred:
      (i)  the STRUCTURAL FENCE — under a heading matching `FENCE_HEADING_RE`, exempt until
           the next heading at equal-or-shallower depth.
      (ii) an INLINE DECLARATION — the hit's own region (nearest preceding heading -> next
           heading) contains one of `DECLARATION_MARKERS`.
    Everything else FAILS LOUD — [[gate-must-quote-what-it-forbids]]: enumerating exemptions
    rather than violations means an unrecognised region can never pass by accident.

    ⛔ PINS WHERE `tape`/`bill` MAY APPEAR, NEVER HOW THE SENTENCE IS PHRASED. `STOP_LINE_HOMES`
    elsewhere in this file pins exact wording, and that bug BLOCKED a session's wrap when
    someone faithfully re-denominated a ruling into words the pin didn't recognise. This audit
    has no ruling-specific string anywhere — only the bare words and a small, generic marker
    vocabulary — so a faithful rewrite that keeps (or gains) a declaration still passes."""
    failures, warnings = [], []
    kdir = os.path.join(repo, "knowledge")
    if not os.path.isdir(kdir):
        return failures, warnings

    for fn in sorted(os.listdir(kdir)):
        if not fn.endswith(".md") or fn == _GENERATED_REPORT_BASENAME:
            continue
        try:
            with open(os.path.join(kdir, fn), encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except OSError:
            continue

        headings = _md_headings(lines)
        fences = _md_fence_spans(headings, len(lines))

        for i, ln in enumerate(lines):
            m = RETIRED_PROSE_WORDS_RE.search(ln)
            if not m:
                continue
            if any(start <= i < end for start, end in fences):
                continue                                   # device (i): fenced, exempt
            r_start, r_end, heading_text = _md_region(headings, i, len(lines))
            region_text = "\n".join(lines[r_start:r_end]).lower()
            if any(marker.lower() in region_text for marker in DECLARATION_MARKERS):
                continue                                   # device (ii): declared, exempt
            failures.append(
                f"retired-unit prose ({RETIRED_PROSE_SCOPE_NOTE}): `knowledge/{fn}`:{i + 1} "
                f"says {m.group(0)!r} in region \"{heading_text}\" (heading at line "
                f"{r_start + 1}), with NEITHER exemption — not inside a fence headed "
                f"RETIRED|HISTORY|SUPERSEDED, and no inline declaration in its own region "
                f"(recognised: {', '.join(DECLARATION_MARKERS)}). Two remedies: (1) move this "
                f"text inside a HISTORY/RETIRED/SUPERSEDED-headed fence, or (2) add one of the "
                f"recognised markers to this region as an inline declaration — never rephrase "
                f"the sentence itself.")

    return failures, warnings


SIZE_STAMP_RE = re.compile(r"^\s*>?\s*\**size\**\s*[:—-]\s*(.+)$", re.I)
SIZE_TK_RE = re.compile(r"\bGM\b\D{0,12}?([\d.]+)\s*K\s*(tape|tk|real)\b", re.I)  # K is REQUIRED:
# ⛔ #82-D1 ADDED `real`, and the omission was not cosmetic: the re-stamped header led with
# `GM **43,370 real**`, this regex did not match it, and the search ran ON and locked onto
# `27.2K tape` — a figure inside #81's KEPT HISTORICAL declaration. The gate then reported a
# 16,170-token drift with total confidence. ★ A parser that keeps scanning after a miss does not
# fail; it finds the WRONG number and grades it. [[silent-lookup-failure-class]].
#   without it "GM 25618 tk" would parse as 25.6M and pass a drift check by accident.
#   ds-021 (#34): `tape` is the canonical unit; bare `tk` is the LEGACY spelling and is still
#   accepted, but it WARNS. ⚠ It is accepted deliberately — a regex that hard-failed on the old
#   form would have blocked the very wrap that rewrites the stamp, i.e. a gate that cannot be
#   satisfied from the state it is introduced in. PROMOTION TRIGGER: once a wrap passes with no
#   legacy-unit warning, make `tape` mandatory here and delete the `|tk` branch. This comment is
#   the only record of that trigger — it ships WITH its consumer (the warn below), per ds-024.
LEGACY_UNIT_RE = re.compile(r"\b\d[\d.]*\s*K\s*tk\b", re.I)
SIZE_TOLERANCE = 0.10      # a stamp is a claim about a measurable thing; 10% drift = re-stamp

# ================================================== open 15 — THE CHAIN FIGURE HAS A LIVE ASSERTION
# ENACTED #49. Born #45, homeless until #46 copied it up, BLOCKED on open 16 until #48 closed it.
#
# THE DEFECT. `SIZE_TK_RE` above validates the **GM** figure and nothing else. Every other
# `chain`-near-`stamp` occurrence in this file was a TEST FIXTURE (#45's probe), never a live
# check — so the one number the whole #33 read-chain cut exists to govern was the one figure in
# the stamp with nothing behind it. #45 retired the hand copy and pointed at the generated one in
# `_CHAIN.md`'s footer, which made the corpus correct *that day* and left the door open. #46 then
# hand-added a chain figure twice and caught itself; #48 did it a third time and caught itself.
# ★ Three sessions self-caught the same act. That is a behaviour holding a line a mechanism should
# ([[gate-inside-the-growth-loop]]), and it is what `guards: SIZE_TK_RE` was waiting for.
#
# ⚠ WHY THIS BANS PRESENCE RATHER THAN CHECKING DRIFT — the tier is mine and is DECLARED, not
# smuggled. A drift check on a hand figure PASSES at the moment of writing (the wrap copies a
# number that is true when it copies it) and only bites a session later. That check would license
# the re-add and then punish whoever inherits it — a cap that fires after the writing can only be
# paid in live record. Banning presence fails the wrap that performs the act, while it can still
# undo it for free. ⬛ FAIL-vs-WARN is Dave's to re-dial; the message says so.
#
# ⚠ SCOPED TO THE `size:` STAMP, DELIBERATELY. `GOOD-MORNING.md:488` carries
# `the CHAIN only (**~4.1K tape**` inside a dated stratum — a historical record of what one
# session's boot cost, which is TRUE and must stay. A repo-wide ban would forge a defect out of
# correct history: report the measurement, never prescribe the region [[gate-narrows-its-own-rule]].
#
# The alternation covers every form the hand copy has actually taken, taken from `git log`, not
# imagined: `chain **4.4K tape` (#44) · `chain 3.56K tape` (#39) · `chain 34.7K tk` (legacy unit,
# #30) · `_CHAIN.md **4.6K tape`. `\D{0,12}?` spans the markdown (`**`, `~`, `(`) without ever
# crossing a digit, so `chain 4,065 → 4,400` and the `417-tape` wrapper prose do not match.
#
# ⛔ WIDENED #94 — the #90 escape, closed where it happened. #90's first stamp wrote
# `chain 13,277 real` beside "measured AFTER the regen", and this regex — bound to the
# `… N K tape|tk` form — walked it straight past the check written to forbid it (caught by
# re-reading the artefact, DECLARED at GM's `size:` line #90, left OPEN; the #94 chain title
# carried the close order). TWO holes, both read off the escape itself, not imagined:
#   (a) the unit vocabulary stopped at the RETIRED spellings (`tape|tk`) — the live unit has
#       been `real` since #82-D1 (ruled #54), so the gate forbade only the forms nobody would
#       write and missed the one everybody would;
#   (b) only `K`-forms matched — a full-digit figure (`13,277`) never could.
# Units are normalised ONCE (tape|tk|real|bill|tokens), not enumerated per session
# [[scope-blindness-gate-vocabulary]]. Group layout: (1)=K-form number, (2)=full-digit number,
# (3)=unit — the open-15 consumer at `chain_hand` parses (1)*1000 or (2) de-commaed.
# A unit-less figure (`chain 4,065 → 4,400`) STILL passes: that is open 23's declared cost,
# deliberately unchanged — closing it silently here would annex a hole Dave knows is open.
CHAIN_STAMP_RE = re.compile(
    r"(?<![A-Za-z])_?CHAIN(?:\.md)?\b\D{0,12}?"
    r"(?:([\d.]+)\s*K|(\d{1,3}(?:,\d{3})+|\d{4,}))\s*"
    r"(tape|tk|real|bill|tokens?)\b",
    re.I)

# ---------------------------------------------------------------- open 25, built 2026-07-30 #51
# `BARE_TOKEN_RE` — ds-021's rule finally gets an enforcer instead of a sentence.
#
# THE RULE IT ENFORCES is already canon and already stated in two places that cannot check it:
# `tape` is what tiktoken counts, `bill` is what the window charges, and **a figure with no unit
# word beside it is a defect** because a reader quotes it without re-measuring. `:2342` already
# bites exactly this for the M10 note (`"a bare token count is a defect"`) — one hand-placed
# check on one line. This generalises it to the `size:` stamp, which ds-021 calls the THIRD home
# and the worst place for an unnamed unit (`:1046`). It is `ds-024`'s class discharged: a rule
# that lived only as prose in `_RUNBOOK-context-gauge.md` now ships with a reader.
#
# ⚠ WARN, NOT FAIL, AND THE TIER IS DECLARED. On the day it was built it fired TWICE on the
# INHERITED stamp (`§A **4.2K (EXEMPT)**`, `corpus **58.7K**`). A FAIL would have blocked the
# wrap and forced same-session edits to inherited record under time pressure — the exact motion
# [[gate-inside-the-growth-loop]] warns about, where a cap firing after the writing is paid in
# live record. WARN reports; Dave rules the tier. ⬛ HIS to re-dial, like every tier here.
#
# ⚠ `K` IS REQUIRED, AND THAT NARROWING IS OPEN 23's, INHERITED KNOWINGLY. `SIZE_TK_RE` and
# `SIZE_A_RE` both require it and open 23 already records that `CHAIN_STAMP_RE` "catches only the
# `K` form". Requiring it here is what keeps the check off `#50`, `2026-07-30`, `18%` and `11 ln`
# without an exclusion list nobody can maintain — a scope control that is structural rather than
# enumerated ([[scope-blindness-gate-vocabulary]]: normalise once, don't enumerate). The cost is
# stated plainly: a bare `4,917` in the stamp would pass. That is open 23, not a new hole.
#
# ⚠ SCOPED TO GM's `size:` STAMP — and the spec said "GM/LS". MEASURED at build: `_LIVE-STATE.md`
# carries NO `size:` stamp, so the LS half of the spec has no surface to bind to. The check is
# GM-scoped because that is where the stamp is, not because LS was judged exempt. If LS ever
# grows a stamp this must be re-pointed. **Report the measurement, never prescribe the region**
# [[gate-narrows-its-own-rule]] — and never invent a surface to satisfy a spec.
#
# ⚠ IT IS NOT OPEN 24 AND MUST NOT BE READ AS IT. Open 24 is a ban on a line MEASURING ITSELF;
# that ban bites the sentence that carries it, which is why #51 left it alone on Dave's warning.
# This one never judges its own output: the scope is the stamp, and the warning text lives in the
# gate. The self-bite control in `selftest_bare_token` asserts that, rather than assuming it.
BARE_TOKEN_RE = re.compile(
    r"(?<![#\w.])(\d[\d,]*(?:\.\d+)?\s*K)\b"
    r"(?!\s*\**\s*(?:tape|bill|tk|tokens?|bytes?|ln|lines?)\b)", re.I)
BARE_TOKEN_UNITS = ("tape", "bill", "tk", "tokens", "bytes", "ln", "lines")

# ---------------------------------------------------------------- #60-D8, built 2026-07-31 #61
# `notes/_MEMENTO-DECISIONS.md` § ★ #60 · #60-D8 — RULED (Dave): the next-chat title is a LABEL,
# capped and gated. MEASURED #60: the `TITLE THE NEXT CHAT` line had grown to 1,073 tape / 3,950
# chars — 18% of the ENTIRE 5,969-tape cold-boot read chain (it is copied verbatim into
# `_CHAIN.md`) — with ZERO consumers anywhere in the toolchain: a repo-wide grep for
# `TITLE THE NEXT CHAT`, `TITLE_RE`, `next_chat`, `chat_title` finds nothing that parses it. Canon
# already said "Titles are LABELS — role comes from Dave's opener line" three lines below it in
# GOOD-MORNING.md. The rule was correct and ungated, so it grew for sixty sessions.
# ⛔ A RULE WITH NO GATE IS A PREFERENCE — that is the finding this check exists to close, and it
# SUPERSEDES `_RUNBOOK-capture-ritual.md` step 4b's #28 ruling ("Title SIZE is a DISCIPLINE, NOT A
# GATE… un-blocked, not ungated"): the advisory-only posture #28 chose is the exact mechanism that
# let this grow unchecked for thirty-two sessions. The runbook carries a correction note pointing
# here, by ADDITION, not a silent rewrite of #28's own text.
# ⚠ FAILS LOUD ON ABSENCE, not just on overflow — an absent title must not read as a pass; #60-D8
# caps the line, it does not licence deleting it.
TITLE_CAP_TAPE = 120
TITLE_LINE_RE = re.compile(r"^\s*>?\s*\*\*TITLE THE NEXT CHAT\b.*$", re.I)

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
SECTION_A_WARN_TK = 7200   # RESTAMPED REAL s212-D11 2026-08-21 (was 4500 cl100k; §A measured 4,208
#   cl100k at the 2026-07-27 ruling = 6,957 real today; restatement not re-dial, same headroom rule;
#   receipt notes/_receipts/2026-08-21-212-g9-ds023-remeasurement.md). The old warn was a pure unit
#   artefact once measurement_tier() went real. Headroom is deliberate, as it always was.
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
#   ⛔ THE CAP IS NO LONGER A CONSTANT — RULED BY DAVE #53 ON D4 (a), AND THE REASON IS THE
#   MEASUREMENT THAT LICENSED IT. The region structurally holds a standing HEADER plus TWO
#   banners (2c keeps ★ LATEST + one ★ PRIOR). Measured #53: header 1,968 tape; median archived
#   banner 1,515 tape across n=58 in `_GM-ARCHIVE.md` ⇒ **floor = 1,968 + 2×1,515 = 4,998 tape,
#   against a block of 5,000.** The cap was set at the floor plus TWO TAPE, so it was never
#   breached for fatness — compliance was arithmetically impossible from the day it was written,
#   and #49/#51 both shaved live record trying to satisfy it (#51 cut 624 tape and the region was
#   STILL at BLOCK). ★ A constant could only be re-picked; a DERIVED cap cannot be raised by fiat
#   and FALLS on its own if banners get leaner — which is Dave's leanness condition discharged
#   MECHANICALLY rather than by discipline, and the same shape he gave D3's amber.
BANNER_BUDGET_FALLBACK_TK = (6400, 7800)   # used ONLY when the archive cannot be measured, and
                                           # NEVER silently — the provenance string says so.
#   RESTAMPED REAL s212-D11 2026-08-21 (was (4000, 5000) cl100k; no artefact of its own — restated
#   through the ruling-day floor arithmetic; path currently unreachable, n=211 >= BANNER_ARCHIVE_MIN_N;
#   receipt notes/_receipts/2026-08-21-212-g9-ds023-remeasurement.md).
# ★★ `s241-D2` — THE ★ LATEST BANNER'S OWN HARD CAP (S1 of the #241 ritual diet, Dave's
# "apply" to the RECOMMENDED DEFAULT PACKAGE of
# notes/_subreports/2026-09-02-241-lane-D-ritual-diet.md, option (a) of its ruling-shaped Q1).
#
# ⚠ THIS IS A DIFFERENT OBJECT FROM THE M8 REGION BUDGET ABOVE, and conflating them is the
# whole reason a cap was needed. M8 measures `file top → DO-FIRST` — header + ★ LATEST + ★ PRIOR
# together — and its cap is DERIVED from the archive, so it moves as banners lean out. It cannot
# bound ONE banner, because two lean banners and one obese one measure the same. THIS bounds the
# ★ LATEST banner ALONE, and it is PICKED, not derived: it is a contract about how much a wrap
# may write, not a description of what wraps have written.
# MEASURED at the moment of ruling (tiktoken cl100k, this tree, 2026-09-02): the #240 ★ LATEST
# banner is 3,353 tape over 13 substantive lines — 2.8× the cap. Lane D measured the same 3,353
# independently, and measured the ⏱ LATEST DELTA that duplicates it at 1,746.
# ⛔ THE PITFALL, STATED WHERE THE NUMBER IS (lane D, Consequences (c)): a shorter banner can
# silently lose the DECLARED GAP. The verbosity being cut is partly the honesty contract doing
# its job — "a declared gap passes, a silent one fails" is enforced by PROSE, not by a field. A
# banner written to 10 lines that drops its declarations has not obeyed this cap, it has evaded
# it, and no gate here can tell the difference. That half is Dave's and the wrap author's.
BANNER_LATEST_CAP_LINES = 10               # `s241-D2` — substantive lines (blank/`>`-only free)
BANNER_LATEST_CAP_TK = 1200                # `s241-D2` — the ★ LATEST banner alone, cl100k
# ⚠ EFFECTIVE FROM, not retroactive. Banners are RATIFIED RECORD: #49/#51/#153 all shaved
# inscribed record to quiet a budget and that is the failure mode this project has already paid
# for three times. A banner written BEFORE the cap warns and is left alone; a banner written
# UNDER the cap fails. Same shape as `BOOT_CEILING_FROM_SESSION` (s240-D2), same reason.
BANNER_LATEST_CAP_FROM_SESSION = 241       # `s241-D2` — #241's wrap is the first bound by it
BANNER_ARCHIVE_MIN_N = 10                  # below this the median is not a measurement
BANNER_HEADROOM_PCTL = 75                  # block admits two 75th-percentile banners


def _banner_unit_samples(repo):
    """Tape size of every archived banner. The dataset the cap is derived FROM.

    ⚠ Returns [] rather than guessing when the archive is absent or unparseable — a cap that
    invents its own dataset is the exact defect this whole block exists to record.
    """
    path = os.path.join(repo, "_GM-ARCHIVE.md")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        arc = f.read()
    parts = re.split(r"^>?\s*#{1,6}\s*★\s*(?:LATEST|PRIOR)\b", arc, flags=re.M)[1:]
    if not parts:
        return []
    sizes = sorted(measure_tokens(p)[0] for p in parts)
    # The final split swallows whatever trails the last banner, so it is not a banner sample.
    return sizes[:-1] if len(sizes) > 1 else sizes


def banner_budget_tk(repo, gm_lines, latest_idx):
    """(warn, block, provenance) — DERIVED from the live floor, not picked. Dave #53, D4 (a).

    warn  = header + 2 × MEDIAN archived banner   (the floor: what the region cannot go below)
    block = header + 2 × p75 archived banner      (the floor plus measured headroom)

    Both round UP to the nearest 100 so the published number is readable, never down — rounding
    a cap down would silently tighten it, which is the ds-021 move this file bans.
    """
    samples = _banner_unit_samples(repo)
    if len(samples) < BANNER_ARCHIVE_MIN_N or latest_idx is None:
        w, b = BANNER_BUDGET_FALLBACK_TK
        return w, b, (f"FALLBACK ({w:,}/{b:,}) — the archive yielded {len(samples)} banner "
                      f"sample(s), under the {BANNER_ARCHIVE_MIN_N} a median needs. "
                      f"DECLARED, never silent.")
    header = measure_tokens("\n".join(gm_lines[:latest_idx]))[0]
    med = samples[len(samples) // 2]
    p75 = samples[min(len(samples) - 1, (len(samples) * BANNER_HEADROOM_PCTL) // 100)]
    up = lambda n: -(-int(n) // 100) * 100
    return up(header + 2 * med), up(header + 2 * p75), (
        f"DERIVED — header {header:,} + 2 × banner (median {med:,} / p{BANNER_HEADROOM_PCTL} "
        f"{p75:,}), n={len(samples)} archived banners")


BANNER_LATEST_RE = re.compile(r"^>?\s*#{1,6}\s*★\s*LATEST\b", re.M)
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
# ★★ RESTATED 2026-07-30 #48 — THE UNIT CHANGED, THE VERDICT DID NOT. open 16 (a), Dave #47.
#   Until now these numbers were denominated in the SLICE (`read_chain_tk`). They are now
#   denominated in the whole `_CHAIN.md` FILE (`chain_file_tk`) — the thing a cold session opens,
#   which is the slice plus `_gen_chain`'s `BANNER` + `FOOTER`. Nothing was tightened: both ends
#   moved by the MEASURED wrapper so that today's pass/fail is arithmetically unchanged.
#       MEASURED at `b8b388e`, tiktoken cl100k:  file 4,604 = slice 4,187 + wrapper 417
#       old:  slice 4,187 vs warn 4,500  →  PASS, 313 tape of headroom
#       new:  file  4,604 vs warn 4,917  →  PASS, 313 tape of headroom   (identical)
#   ⚠ `bill_of()` is a monotone linear map, so restating both sides preserves the comparison the
#   consumer actually makes, not merely the tape figures. This is the `ds-021` precedent enacted
#   (`_capture_gate.py` § ds-021, and the same move that file made at :344): **RESTATE OPENLY,
#   NEVER SILENTLY TIGHTEN.** A re-point that also moved the verdict would be a re-dial wearing a
#   unit change, and the drift pin below would have been the only thing left telling the truth.
#   ⚠ **417 IS A SNAPSHOT, NOT A CONSTANT.** The wrapper renders `gm_tk` and two percentages, so
#   it moves by a token or two every wrap — Dave's #47 brief said 418 and it was 417 by the time
#   this was built, twelve hours later. It is pinned here on purpose: a budget that tracked the
#   wrapper automatically would silently absorb wrapper GROWTH, which is exactly the region this
#   check exists to expose ([[gate-inside-the-growth-loop]]). Moving it is a deliberate act with a
#   ledger line, like every other value in the pin below.
#   ⛔ THE TIER IS UNTOUCHED: still ADVISORY, still AGENT-DERIVED, still AWAITING DAVE. Re-pointing
#   the unit is not promotion, and the engine never derives-and-promotes.
CHAIN_BUDGET_TK = (7700, 10000)    # RESTAMPED REAL s212-D11 2026-08-21, RULED BY DAVE (was
#                                    (4917, 6417) cl100k, agent-derived: the ruled (4500, 6000) on
#                                    the SLICE + the 417-tape wrapper, restated #48 onto the FILE).
#                                    Restatement not re-dial: REAL(file at #48 baseline) x
#                                    (cap / cl100k at #48), baseline reproduced exactly. ⚠ The
#                                    chain measures 19,189 real today — the warn STILL FIRES after
#                                    restamp; that is real growth, not unit noise. Receipt
#                                    notes/_receipts/2026-08-21-212-g9-ds023-remeasurement.md.
CORPUS_BUDGET_TK = 55700           # RESTAMPED REAL s212-D11 2026-08-21, RULED BY DAVE (was 36000
#                                    cl100k, agent-derived; 34,094 cl100k measured at the #33 cut,
#                                    reproduced exactly, = 55,700-equivalent real with the same
#                                    headroom). (warn only) — GM + LS whole, the RETRIEVAL SURFACE;
#                                    never blocks. ⚠ Corpus measures 184,746 real today — the warn
#                                    STILL FIRES after restamp; that is real growth (3.3x), not
#                                    unit noise. Receipt
#                                    notes/_receipts/2026-08-21-212-g9-ds023-remeasurement.md.

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


# ---------------------------------------------------------------- #56 — THE ABSOLUTE STAMP
# ★★ RULED BY DAVE #56. The percentage stamp deadlocked for THIRTEEN CONSECUTIVE SESSIONS
# because every one of its terms divided by the window, and the window's harness half is
# unreachable (`ds-025` item 1). One unobservable denominator voided four observable terms —
# the exact failure D10 (c) forbids, committed inside the instrument that rules it.
#
# ⚠ ADDITIVE ON PURPOSE, AND THIS IS NOT INDECISION. The percentage path below stays LIVE and
# green; this one runs when the stamp is written in the new form. Dave's #55 ruling was to
# correct by ADDITION rather than by trimming ratified record, and the same logic applies to
# machinery: the new path proves itself over a few sessions, THEN the old one is cut in a
# deliberate pass. [[home-by-addition-then-cut]] — never both motions at once.
# ⚠ MARKDOWN-TOLERANT BY NECESSITY, NOT BY TASTE — bitten #56, in the same wrap that built this.
# The first real stamp read `= **96,897 of 200,000**` and the dispatch did not fire, because the
# fixtures were written in plain text while every banner in this corpus is bold-laden. The check
# then fell through to the DEPRECATED percentage path and reported a nonsense failure.
# ★ EXACTLY THE `PREFLIGHT_RE` DEFECT THIS SESSION FOUND, REPEATED ONE FUNCTION LATER: a pattern
# that matches the form the AUTHOR OF THE TEST writes, not the form the RECORD is written in.
# ⇒ the bold-laden form is now a FIXTURE, so this cannot regress quietly.
_A = r"[\s*_]*"          # markdown emphasis + whitespace, any amount
# ⛔ #58: the number group MUST BEGIN WITH A DIGIT. It was `([\d,]+)`, which matches a BARE COMMA —
# so the prose mention "…before the job, and that is a LAPSE…" matched `job` + `,`, and `_n(",")`
# raised ValueError and took the WHOLE GATE DOWN with a traceback. ★★ A CRASH IS NOT A FAIL: a
# failing check reports and the wrap continues to the next check; a crashing one reports NOTHING,
# about ANY check, and the session cannot tell a broken gate from a clean one. Measured, not
# reasoned: `ABS_TERM_RE['job'].search(banner).group(1)` returned `','` on the live #58 banner.
# ★ Requiring the leading digit also fixes the USE-vs-MENTION half for free — `search` walks past
# a mention that has no number after it and finds the real term. ⚠ RESIDUAL, DECLARED, NOT FIXED:
# a prose mention followed by a number (e.g. "the job, 3 of them, ran") would still win, because
# scope is what saves USE-vs-MENTION and syntax cannot ([[gate-must-quote-what-it-forbids]]).
ABS_TERM_RE = {k: re.compile(r"\b%s\b%s(\d[\d,]*)" % (k, _A), re.I)
               for k in ("boot", "job", "wrap")}
ABS_TOTAL_RE = re.compile(r"=%s(\d[\d,]*)%sof%s(\d[\d,]*)" % (_A, _A, _A), re.I)
# A term may be DECLARED unobservable and still pass. A term that is silently absent may not.
# ★ That asymmetry IS the fix: it is what makes "publish the split" cheaper than staying blank.
UNOBSERVABLE_RE = re.compile(r"\bunobservable\b\s*\(([^)]{3,})\)", re.I)


def _n(s):
    # ⛔ #58: FAIL LOUD AND NAMED, never a bare ValueError from inside a check. Defence in depth —
    # the regex above should now make this unreachable, and a guard whose trigger is unreachable is
    # exactly the one that fires the day someone widens the pattern again.
    t = s.replace(",", "")
    if not t.isdigit():
        raise ValueError(f"_n(): {s!r} carries no digits — a pre-flight term matched punctuation, "
                         f"not a number. This is the #58 crash class: widen ABS_TERM_RE and the "
                         f"gate stops reporting on EVERY check, not just this one.")
    return int(t)


def check_preflight_tokens(line, label="GOOD-MORNING.md"):
    """The pre-flight stamp in REAL CLAUDE TOKENS against an ABSOLUTE budget (Dave #56).

    Form: `pre-flight: boot N (disk N measured · harness ~N est ±N) + job N est + wrap N est
           = N of 200,000 — BAND`

    ⚠ Nothing here divides by anything. That is the whole design: the check needs no window
    size, so no unobservable quantity can suppress it. A term whose value cannot be measured is
    written as an estimate and LABELLED; a term that cannot be estimated at all is declared
    `unobservable (<reason>)` and the stamp still publishes everything else.
    """
    fails, warns, notes = [], [], []
    terms, declared = {}, set()
    for key, rx in ABS_TERM_RE.items():
        m = rx.search(line)
        if m:
            terms[key] = _n(m.group(1))
    for m in UNOBSERVABLE_RE.finditer(line):
        for key in ABS_TERM_RE:
            if re.search(r"\b%s\b[^.·]{0,60}unobservable" % key, line, re.I):
                declared.add(key)

    missing = [k for k in ("boot", "job", "wrap") if k not in terms and k not in declared]
    if missing:
        fails.append(
            f"{label}: pre-flight stamp is SILENT on {', '.join(missing)}. D10 (c): publish the "
            f"measured/estimated split — a term you cannot measure is written as an ESTIMATE "
            f"with its error bar, or declared `unobservable (<reason>)`. What is not allowed is "
            f"leaving it out, because that is how one unknown suppressed the whole stamp for "
            f"thirteen sessions.")

    tm = ABS_TOTAL_RE.search(line)
    if not tm:
        fails.append(f"{label}: pre-flight stamp states no total against a budget "
                     f"(`= N of {gauge.BUDGET_WORKING:,}`)")
        return fails, warns, notes

    total, budget = _n(tm.group(1)), _n(tm.group(2))
    if budget != gauge.BUDGET_WORKING:
        fails.append(f"{label}: pre-flight prices against {budget:,}, but the ruled working "
                     f"budget is {gauge.BUDGET_WORKING:,} (Dave #56). Re-dialling it is his "
                     f"word — and changing `_gauge_tokens.BUDGET_WORKING` is part of doing it.")

    if not missing:
        summed = sum(terms.get(k, 0) for k in ("boot", "job", "wrap"))
        if summed and abs(total - summed) > max(1000, summed // 100):
            fails.append(f"{label}: pre-flight arithmetic does not close — "
                         f"{'+'.join(f'{terms.get(k, 0):,}' for k in ('boot', 'job', 'wrap'))} "
                         f"= {summed:,}, stamp says {total:,}")

    bm = BAND_WORD_RE.search(line)
    if not bm:
        fails.append(f"{label}: pre-flight names no band — state the NUMBER and the BAND "
                     f"together so a mismatch is visible in one glance")
    else:
        truth = gauge.band_for(total)
        if bm.group(1).upper() != truth:
            fails.append(f"{label}: pre-flight band MIS-READ — {total:,} is {truth} against the "
                         f"ruled budget, stamp says {bm.group(1).upper()}. Quote the thresholds "
                         f"in `_gauge_tokens.py`, never recall them")

    stop_at = gauge.BUDGET_WORKING - terms.get("wrap", 0)
    if total > gauge.BUDGET_HARD:
        # ⛔ ALWAYS a fail, marked or not — and the reason is EVIDENTIAL, not a preference.
        # 256,000 is the largest context at which Claude's recall has been publicly MEASURED
        # (93% MRCR v2). Past it we are not spending a reserve, we are extrapolating off the end
        # of the data. A marker cannot buy evidence that does not exist.
        fails.append(
            f"{label}: pre-flight {total:,} is past the HARD line ({gauge.BUDGET_HARD:,}). "
            f"That line is SOURCED, not picked: it is the last context length at which Claude's "
            f"recall has been publicly measured (93% on MRCR v2, falling to 76% at 1M). Beyond "
            f"it there is no measurement to reason from, so `RESERVE SPEND` does NOT buy the "
            f"overrun — SPLIT THE JOB across windows, or delegate part of it to a subagent with "
            f"its own budget.")
    elif total > gauge.BUDGET_WORKING:
        if RESERVE_SPEND_RE.search(line):
            warns.append(
                f"{label}: pre-flight {total:,} is over the working budget "
                f"({gauge.BUDGET_WORKING:,}) but inside the hard line — ALLOWED, marked and "
                f"forked to Dave. ⚠ RARE: a session marking this every wrap has re-dialled the "
                f"budget by habit rather than by ruling.")
        else:
            fails.append(
                f"{label}: pre-flight {total:,} is over the working budget "
                f"({gauge.BUDGET_WORKING:,}, Dave #56) and UNMARKED. Either CUT THE JOB back "
                f"inside the budget, DELEGATE part of it to a subagent with its own window, or "
                f"declare the overrun IN ADVANCE and mark it `RESERVE SPEND — forked to Dave`. "
                f"⚠ Do NOT under-price the job to fit — that is the failure this budget exists "
                f"to prevent.")
    elif total < gauge.BUDGET_AMBER:
        notes.append(
            f"{label}: pre-flight {total:,} is below {gauge.BUDGET_AMBER:,} — comfortable. "
            f"Check the price really includes boot + job + wrap: a price that keeps landing far "
            f"under budget is under-pricing, not thrift. In flight, STOP AT {stop_at:,} "
            f"({gauge.BUDGET_WORKING:,} − the {terms.get('wrap', 0):,}-priced wrap).")
    else:
        notes.append(
            f"{label}: pre-flight {total:,} is inside the working budget "
            f"({gauge.BUDGET_WORKING:,}). In flight, STOP AT {stop_at:,} "
            f"({gauge.BUDGET_WORKING:,} − the {terms.get('wrap', 0):,}-priced wrap): the budget "
            f"is where the wrap has FINISHED, not where it starts.")

    # ★ POSITION, NOT JUST VOLUME — published on every path, because it is the cheaper lever and
    # no session will look it up. Recall is U-shaped: strongest at the START and END of context,
    # ~30% weaker in the MIDDLE (Anthropic: "a performance gradient rather than a hard cliff").
    # ⇒ a finding made mid-window is sitting in the weakest region and must be WRITTEN DOWN.
    notes.append(
        f"{label}: ⚠ position matters as much as volume — recall is U-shaped, ~30% weaker in "
        f"the MIDDLE of a window than at either end. The chain is read first and the wrap "
        f"written last, so canon already sits at the strong ends. A finding made MID-window "
        f"does not: write it to its home when you find it, do not carry it to the wrap.")
    return fails, warns, notes


def check_preflight(text, label="GOOD-MORNING.md"):
    """Grade the LATEST session's pre-flight stamp. Returns (fails, warns, notes).

    Since #74 there are exactly THREE outcomes: the #56 TOKEN stamp (dispatched to
    `check_preflight_tokens`, which owns the budget grading), the #73 legal refusal
    (declared gap -> WARN), or a FAIL naming the legal forms — the % path that used to be
    graded here was RETIRED #74-D3 (see the ds-023 header block). Attribution comes first
    (#74): a stamp is graded only if it belongs to the ★ LATEST banner's session.

    ⚠ The third return value is #34's and is not decoration: the stop line is only useful on
    the PASSING path — a session within budget is exactly the one that still needs telling
    where to stop. Folding it into `warns` would teach sessions to skim warnings; dropping it
    would ship a computed number with no reader (ds-024's class)."""
    fails, warns, notes = [], [], []
    line = next((ln for ln in text.splitlines() if PREFLIGHT_RE.match(ln)), None)
    if line is None:
        return ([f"{label}: no `pre-flight:` stamp — the handoff must carry the estimate the "
                 f"session was priced with (runbook § ★ Half 0b). Form (Dave #56, REAL TOKENS): "
                 f"`pre-flight: boot N (disk N measured · harness ~N est ±N) + job N est + "
                 f"wrap N est = N of {gauge.BUDGET_WORKING:,} — BAND`"], warns, notes)

    # ---- #74: FIRST-MATCH ATTRIBUTION (the (h) residual, declared at #73, its own motion here).
    # `next()` above takes the FIRST stamp in file order, so when the LATEST banner carried no
    # stamp of its own, an OLDER session's line was graded in its place — #72 was graded on #71's
    # wording, and a verdict about the WRONG session is worse than no verdict (the
    # [[wrap-skipped-chain-certifies-wrong-session]] class: never pair a message from one run
    # with a status from another). Attribute BEFORE grading. Scoped to text whose ★ LATEST banner
    # names `**#N**` — see LATEST_SESSION_RE's header for why fixtures are untouched.
    ml = LATEST_SESSION_RE.search(text)
    if ml:
        want = ml.group(1)
        mtag = PREFLIGHT_RE.match(line)
        tag = (mtag.group(1) or "").replace("#", "").strip() if mtag else ""
        if not tag:
            fails.append(
                f"{label}: the first pre-flight stamp carries NO session tag while the ★ LATEST "
                f"banner names #{want} — an untagged stamp cannot be PROVEN to grade the latest "
                f"wrap, which is the #72-graded-on-#71 defect wearing a passing face. Tag this "
                f"session's stamp `pre-flight #{want}:`.")
            return fails, warns, notes
        if tag != want:
            fails.append(
                f"{label}: the first pre-flight stamp is #{tag} but the ★ LATEST banner names "
                f"#{want} — the LATEST wrap carries no stamp of its own, so an OLDER session's "
                f"line was about to be graded in its place (the exact (h) residual, observed "
                f"live at #72). Stamp THIS session's pre-flight; a wrap never inherits one.")
            return fails, warns, notes

    # ---- #73: the legal refusal (PREFLIGHT_UNMEASURED_RE, see its header). Checked BEFORE the
    # #56 dispatch so a refusing line is never asked for arithmetic it honestly does not have.
    if "NOT CAPTURED" in line:
        asserts_numbers = bool(TOTAL_RE.search(line) or ABS_TOTAL_RE.search(line)
                               or any(rx.search(line) for rx in TERM_RE.values()))
        if not PREFLIGHT_UNMEASURED_RE.search(line):
            fails.append(
                f"{label}: pre-flight refusal is NOT in the legal form. The only legal refusal "
                f"is the exact `⛔ NOT CAPTURED — UNMEASURED.` followed by the reason — scoped "
                f"to the quoted glyphs so it cannot be produced by accident, and a reasonless "
                f"or reworded refusal is a silent gap wearing a declared one's clothes.")
        elif asserts_numbers:
            fails.append(
                f"{label}: pre-flight line both REFUSES (`⛔ NOT CAPTURED — UNMEASURED`) and "
                f"asserts terms or a total — contradictory testimony. Declare the numbers OR "
                f"the refusal, never both on one line.")
        else:
            warns.append(
                f"{label}: pre-flight is `⛔ NOT CAPTURED — UNMEASURED` with the reason stated "
                f"— LEGAL since #73 (#62's remedy, proposed #72 (h)). The declared gap passes "
                f"and stays visible; the fix that makes this form rare is pricing at the "
                f"OPENER, not a better wrap.")
        return fails, warns, notes

    # ---- #56 DISPATCH. `= N of N` is the absolute form's signature and no percentage stamp can
    # produce it, so the two paths cannot be confused. ⚠ The percentage path below is DEPRECATED
    # but still live and still green — see the ADDITIVE note at ABS_TERM_RE.
    if ABS_TOTAL_RE.search(line):
        return check_preflight_tokens(line, label=label)

    # ---- ⛔ THE % PATH IS RETIRED — #74-D3 (Dave, explicit option-select; standing fork since
    # #58). The (45/60/63) percentage band and its grading branch lived here DORMANT from #57
    # (the live stamp moved to #56's token form, which the dispatch above catches first) — a
    # dormant enforcement is a claim that stopped being true, and its revival path was exactly
    # the silent-wrong-unit defect #58 corrected in prose. The ruled numbers and their history
    # are NOT deleted — they live in `notes/_MEMENTO-DECISIONS.md` (§ #36, § ★ #74) and the
    # runbook's ds-023 sections, which still record HOW the band was ruled. Only the enforcement
    # code is gone. A stamp reaching here is in NO legal form, and the fail says which forms are.
    fails.append(
        f"{label}: pre-flight stamp is in no legal form. The %-form (`fill N% + job N% + wrap "
        f"N% = N%`) was RETIRED #74-D3 (Dave) — the gauge is denominated in REAL TOKENS (#56). "
        f"Legal: the #56 token stamp (`pre-flight #N: boot N (disk N measured · harness ~N est "
        f"±N) + job N est + wrap N est = N of {gauge.BUDGET_WORKING:,} — BAND`) or the #73 "
        f"refusal (`⛔ NOT CAPTURED — UNMEASURED.` + reason).")
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

# ★ #61 — THE PRESENCE INDEX. Born from a defect Dave found: #60 added DO-FIRST items 9–12 and
# NOTHING in the read chain revealed they existed, so a cold session could not even know to
# retrieve them. That is a PRESENCE defect, not a drift one — [[gate-inside-the-growth-loop]] —
# and the remedy is not to paste the bodies in.
#
# ★★ MEASURED BEFORE DESIGNED, and the measurement inverted the task:
#     items 9–12 VERBATIM ... 331 tape, and leaves 0b–8 still invisible
#     ALL 13 items as an index ... 181 tape, and nothing is invisible
# ⇒ the compact index of EVERY open item is CHEAPER than the full text of the four missing ones.
# Full DO-FIRST is 2,583 tape and would breach CHAIN_BUDGET_TK's block candidate by 1,090.
#
# ⚠ GENERATED, NEVER HAND-MAINTAINED. A hand-kept index reproduces the exact defect it exists to
# fix — the next session adds item 13 and forgets the index. Deriving it from the item headings
# makes the authoring gap structurally impossible rather than merely detectable.
# ⛔ WHAT THIS DOES NOT CLOSE, stated because a silent gap is the failing kind: a STALE committed
# `_CHAIN.md` still slips, because `_build_all.py:184-186` writes then checks (#60's ⛔ finding,
# check-after-its-own-remedy). This closes AUTHORING, not STALENESS. Do not read it as both.
OUT_CHAIN = "_CHAIN.md"          # must match `_gen_chain.OUT_NAME` — asserted in selftest
DOFIRST_ITEM_RE = re.compile(r"^>\s*\*\*(\d+[a-z]?)\.\s*(.+)$")
DOFIRST_HOOK_MAX = 46            # chars per hook — a BYTE bound, deliberately
DOFIRST_INDEX_TK_MAX = 700       # ⚠ the whole index, MEASURED — see below
# ⛔ RAISED 420 → 700 AT #82, DELIBERATELY AND WITH THE REASON, because the gate itself demands
# exactly that rather than a silent drift. ★ NOTHING GREW. The ceiling was calibrated against a
# `cl100k` measurement and #82-D1 changed the INSTRUMENT underneath it, so the same index that
# measured ~340 now measures 531 and the ceiling silently tightened by ~1.55×. ⚠ 700 is NOT a
# conversion of 420 — converting is the defect (#54, Dave). It is a headroom figure picked over
# the MEASURED 531 in the unit now in force, AGENT-PICKED AND PROVISIONAL, awaiting Dave.
# ⚠⚠ AND IT IS A CLASS, NOT AN INSTANCE: every ceiling in this repo stated in `tape` is now
# being compared against REAL tokens and is ~1.55× tighter than whoever set it intended. The
# M10 chain warn and the banner-region warn are the same effect. They need RE-MEASURING against
# their purpose, one at a time — not a multiplier pass.
# ⛔ RAISED 700 → 800 AT #110, DELIBERATELY AND WITH THE REASON, same class as the #82 raise —
# this time GROWTH, not an instrument change. #110 closed DO-FIRST item 18 (one hook freed) and
# opened three genuinely new open items (25, 26, and the partial-split update to 23) that #109's
# own boot-floor finding produced; the measured index reached 726 against the 700 ceiling with
# hooks already compacted (three candidate items merged into one, #110's own items kept to
# minimal noun-phrase hooks). 800 is a headroom figure over the measured 726, AGENT-PICKED AND
# PROVISIONAL, awaiting Dave — not a conversion, not a multiplier, and not touched again without
# a fresh measurement.


def dofirst_index(gm_lines):
    """Compact presence index of every open DO-FIRST item: `(text, how)` or `(None, reason)`.

    ⚠ BOUNDS MAGNITUDE, NOT JUST COUNT. #60 found the strata gate bounding live-block COUNT while
    `charged_line_counts` exempted the region's BYTES — *"a gap each gate believes the other
    closes"*. An index whose hooks may grow freely is that same shape with a new name, so the hook
    is truncated per item AND the assembled index is measured against a ceiling. A count of 13 is
    not a measurement of 13 items — [[measure-dont-convert-units]].

    ⚠ REFUSES rather than emitting an empty-but-plausible index, inheriting this module's posture:
    a chain that silently reports NO open work is worse than one that reports none at all.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import _gm_usage
    except Exception as e:                                    # pragma: no cover - import guard
        return None, f"_gm_usage unavailable ({e}) — presence index NOT built, not assumed empty"
    rx = dict(_gm_usage.GM_VOCAB).get("DOFIRST")
    others = [r for k, r in _gm_usage.GM_VOCAB if k != "DOFIRST" and r is not None]
    start = next((i for i, ln in enumerate(gm_lines) if rx.match(ln)), None)
    if start is None:
        return None, ("GOOD-MORNING.md has no ⬛ DO THIS FIRST section — presence index NOT built. "
                      "The chain would otherwise tell a cold session there is no open work, which "
                      "is a confident false negative, not a small index.")
    end = next((i for i in range(start + 1, len(gm_lines))
                if any(r.match(gm_lines[i]) for r in others)), len(gm_lines))

    items = []
    for ln in gm_lines[start:end]:
        m = DOFIRST_ITEM_RE.match(ln)
        if not m:
            continue
        num, rest = m.group(1), m.group(2)
        # Hook = the item's own opening clause, to the first em-dash or bold-close, truncated.
        hook = re.split(r"—|\*\*", rest, maxsplit=1)[0]
        hook = re.sub(r"[`*_]", "", hook).strip(" .,:;")
        hook = re.sub(r"\s+", " ", hook)
        if len(hook) > DOFIRST_HOOK_MAX:
            hook = hook[:DOFIRST_HOOK_MAX].rsplit(" ", 1)[0] + "…"
        items.append((num, hook or "(unhooked — see body)"))

    if not items:
        # ⚠ RAW pattern, never `!r`. `repr()` doubles every backslash, so the "quoted" pattern is
        # not the one a reader can grep for — a gate that quotes what it forbids in a mangled form
        # is a weaker version of not quoting it at all ([[gate-must-quote-what-it-forbids]]).
        # Caught by a mutation-test arm, not by re-reading this line.
        return None, (f"⬛ DO THIS FIRST found at line {start + 1} but ZERO items matched "
                      f"`{DOFIRST_ITEM_RE.pattern}` — presence index NOT built. Either the section "
                      f"is genuinely empty (say so deliberately) or the item form changed and this "
                      f"parser went blind; both are refusals, and a blind parser must never be "
                      f"mistaken for an empty queue.")

    body = " · ".join(f"`{n}` {h}" for n, h in items)
    text = (f"> **⬛ OPEN WORKLIST — PRESENCE INDEX ({len(items)} items, GENERATED). "
            f"Every open item is named; NO bodies are here — `--fetch gm:DOFIRST`.**\n"
            f"> {body}\n"
            f"> **QUEUE — `gm:C1` strands · `gm:C2` ruling batch (Dave's) · `gm:C4` enact-queue.**")
    tk = measure_tokens(text)[0]
    if tk > DOFIRST_INDEX_TK_MAX:
        return None, (f"presence index is {tk:,} tape, over its {DOFIRST_INDEX_TK_MAX:,} ceiling — "
                      f"NOT emitted. This is the bound doing its job: the index sits in the most "
                      f"expensive text in the repo, so it is capped by BYTES and not merely by item "
                      f"count. Shorten the item headings in GOOD-MORNING.md, or raise this ceiling "
                      f"deliberately with a reason — do not let it drift upward silently.")
    return text, f"{len(items)} items, {tk:,} tape (ceiling {DOFIRST_INDEX_TK_MAX:,})"


def chain_parts(repo, gm_lines):
    """The READ CHAIN as **TEXT**: `(gm_part, delta, how)`, or `(None, None, reason)` on refusal.

    ⚠ THIS IS THE ONE SLICER. `read_chain_tk` measures exactly what this returns and
    `_gen_chain.py` writes exactly what this returns, so **the chain we measure and the chain
    we hand a cold session cannot describe different text.** Extracted #41 for that reason: the
    generator was a second consumer, and a second consumer with its own slicer is the same
    drift class the docstring below already refuses.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import _gm_usage
    except Exception as e:                                    # pragma: no cover - import guard
        return None, None, f"_gm_usage unavailable ({e}) — chain UNMEASURED, not assumed clean"

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
        return None, None, ("GOOD-MORNING.md has no ★ LATEST banner — the chain's whole session "
                            "record is that banner, so this is a refusal to measure, not a small chain")
    gm_part = "\n".join(gm_lines[:l_end])

    # ★ #61 — the presence index rides INSIDE the one slicer, deliberately. `_gen_chain.py` writes
    # what this returns and `read_chain_tk` measures what this returns; appending the index in the
    # generator instead would give the generator its own slice, which is the exact second-consumer
    # drift this function was extracted (#41) to make impossible.
    # ⛔ A FAILED INDEX DECLARES ITSELF; IT DOES NOT REFUSE THE CHAIN. The first cut of this DID
    # refuse — and it broke four M10 bites at once, routing every minimal fixture down the
    # UNMEASURED path. `_region_end`'s docstring, eight lines up, had already named the trap:
    # *"a chain that cannot be measured because `C4` moved is over-coupled … The chain depends on
    # ★ LATEST and ⏱ DELTAS; nothing else may break it."* ★ I applied this module's refusal
    # posture to a term that is not allowed to have it, and — exactly as that docstring predicts —
    # it was **caught by a bite, not by re-reading the code**.
    # ★ THE GOVERNING RULE IS THE OTHER ONE: **a DECLARED gap passes, a SILENT one fails.** So an
    # unbuildable index emits a LOUD line saying the worklist is unrepresented, which is what
    # #60 actually lacked — the items were absent with nothing saying so. Measurement survives;
    # invisibility does not. Asserting the index EXISTS on the live tree is a gate's job
    # (`dofirst_index_present_check`), not the slicer's.
    idx, idx_how = dofirst_index(gm_lines)
    gm_part = gm_part + "\n" + (idx if idx is not None else (
        "> ⚠ **PRESENCE INDEX UNAVAILABLE — the open worklist is NOT represented in this chain.** "
        f"{idx_how} ⇒ retrieve `gm:DOFIRST` by hand; do NOT read this chain as evidence that "
        "there is no open work."))

    # ★ s125-D1 (Dave, RULED #125, ENACTED #126) — THE BUILD-STEP FIGURE IS SUBSTITUTED **HERE**,
    # inside the ONE SLICER, for the identical reason the presence index is composed here and not
    # in the generator: `read_chain_tk` measures exactly what this function returns and
    # `_gen_chain.py` writes exactly what it returns. Text injected in the generator would be
    # WRITTEN BUT NOT MEASURED — the second-consumer drift #41 extracted this function to make
    # impossible. The AST READER lives in `_gen_chain.py`, as the ruling names; only the splice is
    # here. [[instruction-right-cause-wrong]]
    # ⛔ A FAILED SUBSTITUTION DECLARES ITSELF AND DOES NOT REFUSE THE CHAIN — same posture as the
    # index directly above, and for the same reason: the chain depends on ★ LATEST and ⏱ DELTAS,
    # and nothing else may break it. A DECLARED gap passes; a SILENT one fails.
    if "{{BUILD_VERDICT}}" in gm_part:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import _gen_chain
            _verdict = _gen_chain.build_verdict_line(repo)
        except Exception as e:                                # pragma: no cover - import guard
            _verdict = ("⛔ **BUILD VERDICT: NOT RENDERED** — the generated step figure could not "
                        f"be produced ({e}). This is a REFUSAL, not a green build.")
        gm_part = gm_part.replace("{{BUILD_VERDICT}}", _verdict)

    ls_path = os.path.join(repo, "_LIVE-STATE.md")
    if not os.path.exists(ls_path):
        return gm_part, None, "_LIVE-STATE absent (no delta term)"
    with open(ls_path, encoding="utf-8") as f:
        ls_lines = f.read().splitlines()
    d_s, d_e = _region_end(ls_lines, _gm_usage.LS_VOCAB, "DELTAS")
    if d_s is None:
        return None, None, "_LIVE-STATE.md has no ⏱ delta section — chain UNMEASURED, not assumed zero"
    body = ls_lines[d_s:d_e]
    # The LATEST delta ends where the next ⏱ heading begins. If there is no second one, the
    # whole section IS the latest delta — say which case was taken, never silently assume.
    nxt = next((i for i, ln in enumerate(body) if i > 0 and LS_DELTA_RE.match(ln)), None)
    delta = "\n".join(body[:nxt] if nxt else body)
    how = f"LATEST delta only (of {len(body)} delta lines)" if nxt else "whole ⏱ section (single delta)"
    return gm_part, delta, how


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
    gm_part, delta, how = chain_parts(repo, gm_lines)
    if gm_part is None:
        return None, how
    gm_tk = measure_tokens(gm_part)[0]
    if delta is None:
        return gm_tk, f"GM header+LATEST {gm_tk} tk · {how}"
    d_tk = measure_tokens(delta)[0]
    return gm_tk + d_tk, f"GM header+LATEST {gm_tk} tk · LS {how} {d_tk} tk"


# ================================================== open 16 (a) — THE CAP MUST BIND THE FILE
# ENACTED #48 on Dave's #47 ruling ((a)+(c); (c) landed at `62b6e1e`, this is (a)).
#
# THE DEFECT, measured #46 and true at #44 and #45 as well. `read_chain_tk` above measures the
# SLICE — the bytes `chain_parts` cuts out of GM and LS. What a cold session actually opens is
# `_CHAIN.md`, which is that slice PLUS `_gen_chain.py`'s `BANNER` and `FOOTER`. The wrapper is
# charged to every cold reader and, until this function existed, **to no cap at all**: the gate
# could report the chain comfortably UNDER its warn while the file a session opens sat OVER it,
# and did, at #44, #45, #46 and #47. ★ A third unit nobody had named — the slice is not the file,
# the same shape as `the tape is not the bill` one level down ([[measure-dont-convert-units]]).
#
# ⚠ WHY THIS IS A SEPARATE FUNCTION AND NOT A FIX INSIDE `read_chain_tk`. `_gen_chain.build()`
# CALLS `read_chain_tk` — it needs the slice as the seed for its fixed point. Measuring the file
# from inside the slicer would be unbounded recursion, not a circular import. So the slice keeps
# its own honest meaning and the FILE gets its own measurement, and the two are published side by
# side so the wrapper's size is always attributable rather than inferred.
#
# ⚠ THE IMPORT IS LAZY, DELIBERATELY (Dave's spec, #47). `_gen_chain` imports `_capture_gate`;
# a module-level import here would close the cycle at import time and break both modules for
# every other consumer. Lazy also keeps the cost where it belongs: nothing that does not ask for
# the file figure pays for a chain render.
def chain_file_tk(repo):
    """Measure what a cold session ACTUALLY OPENS: the whole `_CHAIN.md` file, wrapper included.

    Returns `(file_tk, detail)`, or `(None, reason)` on refusal.

    ⚠ It measures `_gen_chain.build()`'s OUTPUT, not the bytes currently on disk, and that is
    deliberate. Every other figure this gate publishes is derived live from `GOOD-MORNING.md` and
    `_LIVE-STATE.md`; a cap read off a stale `_CHAIN.md` would bless the size of a PREVIOUS
    session's chain. Staleness is a different failure with its own detector — `_gen_chain --check`,
    a blocking build step — so nothing here is left uncovered by measuring the live render.

    ⚠ It REFUSES rather than falling back to the slice. Returning the slice when the file cannot
    be measured would report a number ~400 tape LOW under a label that says FILE, which is the
    exact defect open 16 records, reintroduced as an error path. UNKNOWN is never defaulted.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import _gen_chain                                     # LAZY — see the block comment above
    except Exception as e:                                    # pragma: no cover - import guard
        return None, (f"_gen_chain unavailable ({e}) — chain FILE UNMEASURED. NOT substituted with "
                      f"the slice: that is ~400 tape low and would read as the file.")
    try:
        text, detail = _gen_chain.build(repo)
    except Exception as e:                                    # pragma: no cover - defensive
        return None, f"_gen_chain.build() raised ({e}) — chain FILE UNMEASURED, not assumed equal"
    if text is None:
        return None, f"_CHAIN.md is not generatable — {detail}"
    return measure_tokens(text)[0], detail


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


# ==================================== #82-D1 — THE REAL TIER (Dave's ruling, this session) ===
# RULED #82-D1: *wire `measure_tokens()` to the native counter, and re-stamp the LIVE budget
# claims in the same pass.* ⚠ THE UNIT WAS NOT REOPENED — it is his, ruled #54 (ONE unit, real
# tokens; `cl100k` a labelled estimator, *"never a unit a cap is stated in"*). #81 built the gate
# that NAMED this defect and registered this file `estimate-only`. This is the fix it pointed at.
#
# ★ THE SHAPE IS ADD-ON-TOP, NEVER REPLACE, and that is the load-bearing decision. The
# cl100k → bytes cascade below is UNTOUCHED and keeps its exact method strings, so #59's two
# guards, M6's bites and every pinned label still mean precisely what they meant. A real reading
# is tried FIRST; where it is unreachable this function behaves exactly as it did yesterday.
# Replacing the cascade would have welded a UNIT change to a FALLBACK rewrite —
# [[conflated-fix-guarantees-recurrence]]: one sentence, two problems, one fixed.
#
# ⛔ WHAT I DELIBERATELY DID **NOT** WIDEN — MEASURED, NOT ASSUMED. The obvious follow-through is
# to redefine `measurement_degraded()` as "not real". DO NOT. `_gen_chain.py:156` consumes it as
# a HARD REFUSAL (`return None, …`), so widening it makes `_CHAIN.md` UNGENERABLE on any machine
# without a key or a network — the build dies offline, and the read chain is the one artefact a
# cold session cannot start without. That is [[unkeyed-gate-vs-roll2f-tension]] exactly: a new
# gate making a CORRECT state unreachable. cl100k is deterministic and self-consistent, so a
# chain measured ENTIRELY on it converges honestly and says so. The thing that must never happen
# is a chain measured on TWO tiers — and that is what `measurement_mixed()` below watches, which
# is a check that can actually FAIL rather than one that forbids an honest offline build.
#
# ⚠ AND IT CORRECTS #81's OWN BLAST-RADIUS NOTE AT SOURCE. That note lists
# `_validate_package_delta.py` (6 refs) as a `measurement_degraded()` consumer reaching the
# SHIPPED package. MEASURED #82 by quoting all six: they are SYMBOL-PARITY checks —
# `PORTED_FUNCS_A` (:86) names the function, ARM2(b) (:479) deletes it to prove the check bites.
# **Not one reads the return value.** The package risk was real for the NAME and nil for the
# SEMANTICS. The risk that note did NOT name is the `_gen_chain.py` refusal above.
# [[unmatched-grep-is-not-an-absence]] — a MATCHED grep is not a presence either; quote the line.
_REAL_TIER_ENV = "CAPTURE_GATE_NO_REAL"   # set to force the pre-#82 cascade (selftests use it)
_TIERS_SEEN = set()                       # every tier this PROCESS has actually measured with


def _tier_of(method):
    """The TIER a method string belongs to: `'real'` · `'cl100k'` · `'estimate'`. ONE place,
    because two readers of one vocabulary is the drift class this entire file argues against."""
    if method == "real":
        return "real"
    return "estimate" if "ESTIMATE" in method else "cl100k"


def encoder_home_module():
    """The `_encoder_home` module this file's bootstrap loaded, or None when it found none.

    ⚠ A READ of what the bootstrap already did — it never imports, never searches, never
    falls back. Apollo's own tree carries no `_encoder_home.py` above `knowledge/`, so
    `_eh_mod` is never bound there, this returns None, and the measurement cascade below is
    byte-for-byte the behaviour it had before `s222-D3`. In the released pack the bootstrap
    DOES bind it, and `measure_tokens` can reach the pack's own exact encoder."""
    return globals().get("_eh_mod")


def measure_tokens(text):
    """Returns (tokens, method). REAL Claude tokens when reachable (#82-D1, Dave's); otherwise
    tiktoken when present (OBSERVED); otherwise — `s222-D3` — the pack's OWN exact cl100k
    engine over its vendored data, which names itself; otherwise the MEASURED byte divisor,
    labelled ESTIMATE. Every tier is declared and they are never silently mixed — a number
    whose method is unstated is the thing this gate exists to prevent.

    ⚠ #59 — THE ENCODE CALL IS BEHIND A GUARD NOW TOO, NOT JUST THE IMPORT. `get_encoding()`
    fetches cl100k_base's BPE ranks file over the network on a cold cache (tiktoken's own
    `read_file_cached`, keyed off `tempfile.gettempdir()`), and this line used to sit UNGUARDED
    below the try/except: a healthy `import tiktoken` followed by a failed fetch (cold cache +
    a network hiccup) raised straight out of this function — a crash, with no ESTIMATE fallback
    and no label, which is a worse failure than the one this function's docstring already
    refuses to allow. Same failure class as the import guard just above; there is no reason the
    second half of one operation should be held to a lower standard than the first."""
    # ---- #82-D1: the REAL tier. `gauge` is `_gauge_tokens`, imported at :58 since #56 and never
    # once called from here — the cure was in this file's own namespace for 25 sessions.
    # ⚠ `count()` raises MeasurementRefused (#79-D1) when it can reach NOTHING, and that is not
    # this function's failure to report: control falls into the cascade below, which labels
    # itself. Never to silence — there is no path here that returns an unlabelled number.
    if not os.environ.get(_REAL_TIER_ENV):
        try:
            n, how = gauge.count(text)
            if how == "real":
                _TIERS_SEEN.add("real")
                return n, "real"
        except Exception:
            pass
    try:
        tiktoken = importlib.import_module("tiktoken")
    except Exception:
        if not _heal_tiktoken():
            # ---- s222-D3: the PACK'S OWN EXACT ENGINE, before any estimate. Same vendored
            # cl100k data, real pretokenizer + merges, equality-gated against tiktoken. It
            # NAMES ITSELF (`purepy cl100k_base (exact, equality-gated)`) — never borrows the
            # library's label, because a fallback wearing the real library's name is a silent
            # fallback. This is the cl100k TIER, not a new one: the numbers are byte-identical
            # by construction and by gate, so a chain stamped by one engine still byte-matches
            # a check by the other. Nothing here can return an unlabelled number.
            _eh = encoder_home_module()
            if _eh is not None:
                try:
                    _n, _which = _eh.count(text)
                    _TIERS_SEEN.add("cl100k")
                    return _n, _which
                except Exception:
                    pass
            _TIERS_SEEN.add("estimate")
            return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                    f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)")
        tiktoken = importlib.import_module("tiktoken")
    try:
        out = len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"
    except Exception:
        _TIERS_SEEN.add("estimate")
        return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken installed, encoder unloadable)")
    _TIERS_SEEN.add("cl100k")
    return out


_PROBE_VERDICT = None   # W-273 S1 (#227): the per-process probe verdict, beside _TIERS_SEEN


def _tier_probe():
    """The tier a measurement of NOVEL text taken RIGHT NOW would use — WITHOUT recording it.

    ⛔ RE-DESIGNED (#227, W-273 S1, Dave's word on the #226 draft brief): the old probe
    measured the one-character string "x" — permanently cached in `.token-cache.json` — so
    `gauge.count()`'s cache-hit branch answered "real" REGARDLESS of API reachability. Driven
    live at #226: probe said `real` while a novel nonce measured `cl100k-estimate`, key
    present, API unreachable. The probe now measures a NONCE (cache-miss by construction), so
    the answer is the tier a real measurement would actually get. Price, declared: ONE ~10-token
    API call per process when reachable. The verdict is held per process — reachability within
    one process run is one fact, and a probe per call would turn a health check into a
    metronome. `_cache_write=False` keeps the nonce out of the content-keyed cache (the #226
    fake-real arm seeded one junk row; the kwarg removes the class at the root).

    ★ The snapshot/restore stays — it is the point. A health probe is not a measurement, and a
    probe that wrote into `_TIERS_SEEN` would let `measurement_mixed()` fire on its own
    footprint — an instrument manufacturing the very condition it reports. That is
    [[check-after-its-own-remedy]] in miniature, and it is cheaper to forbid here than to debug
    later from a mixed-tier warning nobody can reproduce."""
    global _PROBE_VERDICT
    if _PROBE_VERDICT is not None:
        return _PROBE_VERDICT
    snapshot = set(_TIERS_SEEN)
    nonce = "tier-probe nonce " + os.urandom(16).hex()
    try:
        try:
            _PROBE_VERDICT = _tier_of(gauge.count(nonce, _cache_write=False)[1])
        except gauge.MeasurementRefused:
            # Neither the API nor tiktoken — the cascade's LOWER tiers (s222-D3 vendored
            # engine, bytes ESTIMATE) are what a real measurement would get; measure_tokens
            # names them, and its inner gauge.count refuses again so no cache write happens.
            _PROBE_VERDICT = _tier_of(measure_tokens(nonce)[1])
        return _PROBE_VERDICT
    finally:
        _TIERS_SEEN.clear()
        _TIERS_SEEN.update(snapshot)


def measurement_tier():
    """`'real'` · `'cl100k'` · `'estimate'` — what a measurement taken now would be. ★ THIS is
    the word the vocabulary lacked (#80's root cause, confirmed at source #81): the reason a
    RULED unit sat unenacted for 26 sessions was that no function in this file could SAY 'real',
    so `measurement_degraded()` asked *'is this an estimate?'* and cl100k answered *no, healthy*.
    A stamp that names its tier can be checked; one that cannot, cannot."""
    return _tier_probe()


def measurement_mixed():
    """True iff this PROCESS has measured with more than one tier.

    ⚠ BORN FROM THE FIXED POINT, not from tidiness. `_gen_chain.py` iterates `_CHAIN.md` to a
    fixed point in which the file asserts its own size; real and cl100k differ by ~1.5×, so a run
    that reached the API on one iteration and fell back on the next would either oscillate
    forever or bake two units into one file — and both failures look exactly like a content
    change from the outside. This is the check #59's reasoning implies once a third tier exists:
    #59 refused a chain built on a GUESS; this refuses one built on TWO INSTRUMENTS.

    ★ It watches what actually happened, never what is reachable — [[measure-dont-convert-units]]
    and #81's own rule that a gate checks vocabulary and history, not a live reading it might be
    honestly unable to take."""
    return len(_TIERS_SEEN) > 1


def measurement_tiers_seen():
    """The tiers this process measured with, sorted — for a caller that must NAME them in a
    refusal. A refusal that cannot say WHICH two instruments disagreed is a shrug."""
    return sorted(_TIERS_SEEN)


def measurement_degraded():
    """True iff `measure_tokens()` is running on the ESTIMATE fallback right now, rather than
    the real tiktoken encoder. Probes a 1-character string — cheap, and it is the SAME call a
    real measurement makes, so this cannot drift from what a real measurement would report (a
    second, hand-rolled health check would be exactly the drift class every "ONE SLICER"
    comment in this file already refuses to repeat).

    ⚠ #59 — BORN because `_gen_chain.py`'s `build()` calls `measure_tokens(...)[0]` at every
    site and never once looks at `[1]`: the method was always DECLARED, just never READ by its
    main consumer. A generator whose fixed point bakes size figures straight into a file cannot
    tell a genuine content change from an instrument that quietly started guessing — that is the
    one fact it needs in order to tell the two apart, offered as its own function so `build()`
    can ask the question BEFORE it measures anything, rather than infer it after the fact from a
    mismatch that looks identical either way.

    Call this to gate a VERDICT (stale vs. cannot-measure-reliably), never to gate a MEASUREMENT
    itself — a caller that skips measuring because this returned True would just be adding a
    second, undeclared fallback next to the one this file already owns.

    ⛔ #82-D1 — ITS MEANING IS UNCHANGED ON PURPOSE, AND THE REASON IS WRITTEN DOWN ABOVE
    `measure_tokens`. It still asks *"is this reading a GUESS?"*, NOT *"is this reading REAL?"*.
    Widening it to mean 'not real' would turn `_gen_chain.py:156`'s refusal into an offline
    build-killer. `measurement_tier()` is where the finer question now lives; `measurement_mixed()`
    is where the fixed point is protected. Three questions, three functions, one vocabulary."""
    return _tier_probe() == "estimate"


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
    """(#lines, #blocks, block_keys) of the 2f stratum stack inside §C — the D6(a) exclusion
    region. Extracted from check_budgets at M5 (2026-07-28) so the mover's projected-count guard
    and this gate walk the SAME implementation: two copies of an exclusion is how one of
    them drifts. Behaviour identical to the inline original — the BUDGET_FIXTURES strata
    bites (2-blocks FAIL · exclusion-must-hold control) prove it.

    block_keys ADDED #58 (for STRATA_EXEMPT — see its ruling comment above): the session number
    off each block's own `#### <date> #<N>` heading, via `_key_session`, in file order — or
    `None` for a block whose heading carries no parseable key. #lines and #blocks are UNCHANGED
    in shape and meaning; both existing call sites were updated to unpack three values instead
    of two. A `None` entry must be treated as LIVE by any caller matching against STRATA_EXEMPT
    — an unparseable key must never silently match an exemption it cannot actually claim."""
    if "§C" not in spans:
        return 0, 0, []
    c_start, c_end = spans["§C"]
    for i in range(c_start, c_end):
        if STRATA_HEAD_RE.match(lines[i]):
            j, blocks, keys = i + 1, 0, []
            while j < c_end and not re.match(r"^#{1,3}\s", lines[j]):
                if STRATA_BLOCK_RE.match(lines[j]):
                    blocks += 1
                    keys.append(_key_session(lines[j]))
                j += 1
            return j - i, blocks, keys
    return 0, 0, []


def charged_line_counts(lines, spans):
    """{section: line count as the caps CHARGE it} — §C net of the strata exclusion, every
    other section gross. The ONLY implementation of the charging rule: check_budgets reports
    against it and `_gm_move.py` imports it (M5 — the mover must never re-derive what the
    gate charges; a mover charging §C gross would refuse moves the gate permits, which is
    the #19 prose-stricter-than-its-gate failure rebuilt in code)."""
    strata_lines, _blocks, _keys = strata_extent(lines, spans)
    return {name: (e - s - strata_lines if name == "§C" else e - s)
            for name, (s, e) in spans.items()}


def _gauge_log_session_keys(repo):
    """Session numbers already keyed (`#### <date> #<N>`) in notes/_GAUGE-LOG.md, or `None` if
    the file does not exist (e.g. a fixture repo in the self-test harness — the caller MUST
    treat that as SKIPPED, never as an empty set: a missing file is not proof that no block is
    unrollable). ADDED #58, for the fail-loud-on-a-fourth check in check_budgets().

    Reads the SAME condition `_gm_move.py`'s roll_2f duplicate-key guard tests
    (knowledge/_gm_move.py ~line 320-325: `seen = [s for s in (_key_session(ln) for ln in
    flog.lines if STRATA_KEY_RE.match(ln)) if s is not None]`) — same regex, same key parser,
    on purpose: a second hand-rolled copy of that condition is exactly the drift class
    strata_extent()'s own docstring warns about."""
    log_path = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    if not os.path.exists(log_path):
        return None
    with open(log_path, encoding="utf-8") as f:
        log_lines = f.read().splitlines()
    return {n for n in (_key_session(ln) for ln in log_lines if STRATA_KEY_RE.match(ln))
            if n is not None}


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
    _strata_lines, strata_blocks, strata_keys = strata_extent(lines, spans)
    # #58: STRATA_MAX_BLOCKS binds LIVE blocks only — the closed exempt list (ruling + reason at
    # STRATA_EXEMPT's definition above) is measured and reported, never charged, the same shape
    # as SECTION_EXEMPT just below. A key of `None` (unparseable heading) can never match the
    # exempt set, so it counts as live — behaviour for an ordinary over-cap block is UNCHANGED.
    exempt_present = [k for k in strata_keys if k in STRATA_EXEMPT]
    live_blocks = strata_blocks - len(exempt_present)
    if exempt_present:
        notes.append(
            "GOOD-MORNING.md strata " + ", ".join(f"#{k}" for k in exempt_present) +
            ": EXEMPT by ruling (Dave #58 — permanently unrollable, notes/_GAUGE-LOG.md:399 "
            "key added retroactively; § META — UNKEYED #40 #41 #42): measured and reported, "
            "never charged.")
    if live_blocks > STRATA_MAX_BLOCKS:
        fails.append(f"GOOD-MORNING.md: strata stack holds {live_blocks} live block(s) "
                     f"(max {STRATA_MAX_BLOCKS}; {len(exempt_present)} exempt by ruling #58, "
                     f"not counted) — ritual step 2f")
    # ⚠ FAIL LOUD ON A FOURTH (Dave #58, verbatim): "the exemption is a named list of three, not
    # a licence to accumulate: if a fourth unrollable block ever turns up, fail loud and come
    # back to me." A block is unrollable in the SAME way #40/#41/#42 are exactly when its key is
    # already present in notes/_GAUGE-LOG.md — that is the literal condition `_gm_move.py`'s
    # roll_2f duplicate-key guard tests (~line 320: "already carries a block for #N"). Checked
    # here cheaply (one extra file read, the same STRATA_KEY_RE/_key_session pair roll_2f itself
    # uses — read, not re-derived) so a newly-stuck block gets a message naming the actual
    # condition instead of reading as an ordinary overflow. If notes/_GAUGE-LOG.md is absent
    # (e.g. a fixture repo) this specific check is silently SKIPPED, not passed — see
    # _gauge_log_session_keys's docstring.
    gauge_log_keys = _gauge_log_session_keys(repo)
    if gauge_log_keys is not None:
        newly_unrollable = [k for k in strata_keys
                            if k is not None and k in gauge_log_keys and k not in STRATA_EXEMPT]
        if newly_unrollable:
            fails.append(
                "GOOD-MORNING.md: strata block(s) " +
                ", ".join(f"#{k}" for k in newly_unrollable) +
                " already keyed in notes/_GAUGE-LOG.md — roll_2f's duplicate-key guard will "
                "refuse them, the same permanent condition #40/#41/#42 are stuck in. "
                "STRATA_EXEMPT is a CLOSED list of three (Dave #58): this is a NEW unrollable "
                "block and needs Dave's ruling, not an addition to the list.")

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

    # ---- #60-D8: TITLE THE NEXT CHAT is a LABEL, capped and BLOCKING (Dave's ruling — see the
    # TITLE_CAP_TAPE/TITLE_LINE_RE comment above for the full measurement and the #28 supersession).
    title_line = next((ln for ln in lines[:HEADER_LINES] if TITLE_LINE_RE.match(ln)), None)
    if title_line is None:
        fails.append(
            "GOOD-MORNING.md: no `TITLE THE NEXT CHAT` line found in the header — ritual step "
            "2/4b. An ABSENT title must not read as a pass: #60-D8 caps the line, it does not "
            "licence deleting it.")
    else:
        title_tape, title_method = measure_tokens(title_line)
        if title_tape > TITLE_CAP_TAPE:
            fails.append(
                f"GOOD-MORNING.md: `TITLE THE NEXT CHAT` line measures {title_tape} tape "
                f"({title_method}), cap {TITLE_CAP_TAPE} tape (RULED #60-D8) — ritual step 2/4b. "
                f"The title is a LABEL: at 1,073 tape it was 18% of the 5,969-tape read chain "
                f"with ZERO consumers anywhere in the toolchain. REMEDY: shorten it back to a "
                f"label — role comes from Dave's opener line, never the title.")
        else:
            notes.append(f"TITLE THE NEXT CHAT: {title_tape} tape ({title_method}) — cap "
                         f"{TITLE_CAP_TAPE} tape, RULED #60-D8.")

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
    # open 16 (a), #48: the SLICE above is kept and still published — it is what `chain_parts` cuts
    # and what the generator seeds from — but the CAP now binds the FILE, because the file is what a
    # cold session opens. Both figures ride together so the wrapper is always ATTRIBUTABLE.
    chain_file, chain_file_detail = chain_file_tk(repo)
    # ⚠ The whole-file figure leads, ALWAYS. The budget excludes §A; the published cost does not.
    # An exclusion that also hides the total would understate exactly the cold-start cost that the
    # D9 measured floor exists to make honest. Post-#33 the same principle covers the corpus: the
    # chain got 90% cheaper, the corpus did not get smaller — it got DEFERRED. Publish both.
    chain_txt = f"{chain} tk ({chain_detail})" if chain is not None else f"UNMEASURED — {chain_detail}"
    file_txt = (f"{chain_file:,} tape (the CAPPED unit)" if chain_file is not None
                else f"UNMEASURED — {chain_file_detail}")
    notes.append(f"SIZE measured ({method}): GM {tk} tk WHOLE FILE · of which §A {exempt_tk} tk "
                 f"exempt · compactable {compactable} tk (the budgeted figure) · "
                 f"READ CHAIN {chain_txt} · CHAIN FILE {file_txt} · "
                 f"corpus (GM+LS, the retrieval surface) {corpus} tk")

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

        # ---- open 15 (#49): the chain figure is now ASSERTED, and asserted against the FILE.
        # ⚠ It reports the live measurement in the same breath as the refusal, because a gate that
        # only forbids teaches nothing about where the truth lives. UNKNOWN is never defaulted: if
        # `chain_file_tk` refused, the ban still stands and the message says the figure is
        # UNMEASURED and why, rather than substituting the slice (~400 tape low, open 16's defect).
        chain_hand = CHAIN_STAMP_RE.search(stamp.group(1))
        if chain_hand:
            if chain_file is None:
                truth = f"UNMEASURED — {chain_file_detail}"
            else:
                # #94: group(1) = K-form (`4.4K`), group(2) = full-digit form (`13,277`) —
                # the widened regex guarantees exactly one is non-None.
                hand = (float(chain_hand.group(1)) * 1000 if chain_hand.group(1) is not None
                        else float(chain_hand.group(2).replace(",", "")))
                drift = abs(hand - chain_file) / max(chain_file, 1)
                truth = (f"the FILE measures {chain_file:,} tape right now, so this copy is already "
                         f"{drift * 100:.1f}% out" if drift > SIZE_TOLERANCE else
                         f"the FILE measures {chain_file:,} tape, so this copy happens to be "
                         f"accurate TODAY — which is not a defence, it is the failure mode: a hand "
                         f"copy of a generated number is only ever accurate on the day it is written")
            fails.append(
                f"GOOD-MORNING.md: `size:` stamp carries a HAND-WRITTEN chain figure "
                f"({chain_hand.group(0).strip()!r}) — RETIRED #45 and it must not come back. "
                f"{truth}. Its ONE home is `_CHAIN.md`'s footer, where `_gen_chain` generates it "
                f"as a fixed point (exact by construction) and `--check` blocks a stale one. "
                f"REMEDY: delete the figure from the stamp; quote the footer if a reader needs it. "
                f"⬛ This fails on PRESENCE, not on drift, because a drift check would pass the "
                f"wrap that re-adds the figure and bite the one that inherits it — #46 and #48 "
                f"each caught this by hand, which is a behaviour doing a mechanism's job. "
                f"The FAIL tier is agent-picked and awaiting Dave; the retirement is not. "
                f"— ritual step 2, open 15")

        # ---- open 25 (#51): ds-021's unit rule, enforced. A figure in the stamp with no unit
        # word beside it cannot be quoted safely, because `tape` and `bill` are different
        # quantities and the stamp is the surface readers quote WITHOUT re-measuring (ds-021's
        # "third home", `:1046` above). The remedy is ADDITION — name the unit — never a cut,
        # so this warn can be discharged without touching a single figure [[home-by-addition]].
        bare = [m.group(1).strip() for m in BARE_TOKEN_RE.finditer(stamp.group(1))]
        if bare:
            warns.append(
                f"GOOD-MORNING.md `size:` stamp carries {len(bare)} figure(s) with NO unit word "
                f"beside them: {', '.join(repr(b) for b in bare)}. ds-021 canon is `tape` (what "
                f"tiktoken counts) beside `bill` (what the window charges) — a bare count leaves "
                f"the reader to guess which, and the stamp is the one surface quoted without "
                f"re-measuring. REMEDY IS ADDITION: write the unit after the figure "
                f"(`{bare[0]} tape`); nothing needs cutting and no figure needs changing. "
                f"⚠ MEASURE before you name the unit — do not copy the neighbouring figure's "
                f"word on the assumption it is the same quantity. Accepted unit words: "
                f"{', '.join('`%s`' % u for u in BARE_TOKEN_UNITS)}. "
                f"⬛ WARN not FAIL, and the tier is agent-picked and awaiting Dave: this fired on "
                f"INHERITED record the day it was built, and a block would have forced live edits "
                f"to that record under wrap pressure. ⚠ `K` is REQUIRED to match, so a bare "
                f"`4,917` still passes — that is open 23's limitation, declared, not a new hole. "
                f"— ritual step 2, open 25")

    # ---- ds-021: the cap BINDS ON BILL. Both numbers are reported, the unit is named on each.
    # ⚠ Today this is arithmetically identical to binding on tape, BY DESIGN — the ruling says
    # RESTATED at current real value, not silently tightened, and both sides of the comparison
    # are currently derived through the same ratio. What it buys is (i) nobody can read a tape
    # figure as a cost again, and (ii) the moment a REAL bill measurement arrives the cap binds
    # on the measured thing and the ratio stops mattering. A conversion applied to both sides
    # cancels; the naming does not.
    budget = SIZE_BUDGET_TK["compactable"]
    block_tk = SIZE_BUDGET_TK["compactable_block"]        # None = ADVISORY, withdrawn #39
    budget_bill = bill_of(budget)
    compact_bill = bill_of(compactable)
    if block_tk is None:
        # ⛔ BLOCK WITHDRAWN #39 (Dave). This region is RETRIEVAL SURFACE — since #33 cut the read
        # chain, its growth is not paid at cold start. Reported, never enforced. The message says so
        # out loud, because a number with no stated referent is what let this cap outlive its purpose.
        notes.append(f"COMPACTABLE region: {fmt_units(compactable)} · warn {budget:,} tape / "
                     f"~{budget_bill:,} bill · BLOCK WITHDRAWN #39 — ADVISORY. This region is "
                     f"RETRIEVAL surface, not the cold-start chain (#33): growth here costs a "
                     f"retrieval, never a boot. ⬛ The cold-start cap now MEASURES THE RIGHT THING "
                     f"(the whole `_CHAIN.md` file, #48) but is still ADVISORY — arming it is "
                     f"Dave's, see M10 chain_file_tk / CHAIN_BUDGET_TK.")
        if compact_bill > budget_bill:
            warns.append(f"GOOD-MORNING.md compactable: {fmt_units(compactable)}, warn "
                         f"~{budget_bill:,} bill — ADVISORY, never a trim order. ⚠ If this number "
                         f"is climbing session on session, that is the grunge signal: say so in the "
                         f"banner and re-open the contract. Do NOT shave live record to quiet it.")
    else:
        block_bill = bill_of(block_tk)
        notes.append(f"COMPACTABLE region: {fmt_units(compactable)} · warn {budget:,} tape / "
                     f"~{budget_bill:,} bill · block {block_tk:,} tape / ~{block_bill:,} bill")
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
        _m = BANNER_LATEST_RE.search("\n".join(lines[:b_end]))
        _lat = len("\n".join(lines[:b_end])[:_m.start()].splitlines()) if _m else None
        b_warn, b_block, b_prov = banner_budget_tk(repo, lines, _lat)
        bw_bill, bb_bill = bill_of(b_warn), bill_of(b_block)
        notes.append(f"BANNER region: {fmt_units(banner_tk)} (file top → DO-FIRST: header + "
                     f"★ LATEST + ★ PRIOR) · warn {b_warn:,} tape / ~{bw_bill:,} bill · block "
                     f"{b_block:,} tape / ~{bb_bill:,} bill · cap {b_prov}")
        # ★ M8 TIER KEYS ON WHETHER THE REMEDY IS LEGAL — Dave 2026-08-11 (#154, "fix it
        # properly"), closing DO-FIRST 11 (born #58). The block's only remedy is a 2c roll, and
        # 2c KEEPS ★ LATEST + one ★ PRIOR: with ≤1 PRIOR in the region there is nothing that may
        # legally move, so the fail demanded either shaving ratified record (#49/#51/#153 all did)
        # or an index-refused roll (proven-by-reversal, #58). A gate may not demand an action the
        # contracts forbid — the M10 comment above already states the law ("a budget check reports
        # its measurement; it does not prescribe the region"); this applies it to M8's own tier.
        # With ≥2 PRIORs a roll IS available and the block stands exactly as before. At the
        # minimum, the overage is banner FATNESS, pressure lands on the NEXT banner at authoring
        # time, and the derived cap falls on its own as archived banners lean out (D4 (a) — the
        # leanness condition discharges mechanically). Report; never a trim order; Dave rules.
        n_prior = sum(1 for ln in lines[:b_end] if _BANNER_PRIOR_START_RE.match(ln))
        if bill_of(banner_tk) >= bb_bill:
            if n_prior >= 2:
                fails.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, block "
                             f"~{bb_bill:,} bill — roll a banner to _GM-ARCHIVE.md (ritual step 2c)")
            else:
                warns.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, block "
                             f"~{bb_bill:,} bill — AT 2c MINIMUM ({n_prior} PRIOR): no banner may "
                             f"legally roll, so no fail is issued for an action the contract "
                             f"forbids (DO-FIRST 11 class, closed #154). The weight is banner "
                             f"fatness against the archive's p{BANNER_HEADROOM_PCTL} — write the "
                             f"NEXT banner leaner; never shave inscribed record to quiet this.")
        elif bill_of(banner_tk) > bw_bill:
            warns.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, cap "
                         f"~{bw_bill:,} bill — ritual step 2c")

        # ---- ★ LATEST BANNER HARD CAP (`s241-D2`, S1). See the constant block for what this
        # measures and why it is not M8. Bounded by DO-FIRST as well as by the next ★ PRIOR: a
        # banner cannot run past the section that follows it, and a region that silently ran to
        # EOF would make the cap fire on the whole file.
        _lat_i = next((i for i, ln in enumerate(lines[:b_end])
                       if BANNER_LATEST_RE.match(ln)), None)
        if _lat_i is not None:
            _lat_end = next((j for j in range(_lat_i + 1, b_end)
                             if _BANNER_PRIOR_START_RE.match(lines[j])), b_end)
            _lat_text = "\n".join(lines[_lat_i:_lat_end])
            _lat_tk = measure_tokens(_lat_text)[0]
            _lat_lines = [ln for ln in _lat_text.splitlines()
                          if ln.strip() not in ("", ">")]
            _lat_m = re.search(r"#(\d+)", lines[_lat_i])
            _lat_sess = int(_lat_m.group(1)) if _lat_m else None
            _over = []
            if len(_lat_lines) > BANNER_LATEST_CAP_LINES:
                _over.append(f"{len(_lat_lines)} substantive lines against a cap of "
                             f"{BANNER_LATEST_CAP_LINES}")
            if _lat_tk > BANNER_LATEST_CAP_TK:
                _over.append(f"{_lat_tk:,} tape against a cap of "
                             f"{BANNER_LATEST_CAP_TK:,}")
            if _over:
                _msg = (f"LATEST BANNER CAP (`s241-D2`: {BANNER_LATEST_CAP_LINES} lines / "
                        f"{BANNER_LATEST_CAP_TK:,} tape, and the ⏱ LATEST DELTA is the sole "
                        f"home for gauge / declared-skip / not-done detail): GOOD-MORNING.md's "
                        f"★ LATEST banner is over by "
                        + " and ".join(_over) + ". ")
                if _lat_sess is not None and _lat_sess >= BANNER_LATEST_CAP_FROM_SESSION:
                    fails.append(
                        _msg + f"This banner is #{_lat_sess}, written AT OR AFTER the cap's "
                        f"first bound session (#{BANNER_LATEST_CAP_FROM_SESSION}) — write it "
                        f"under the cap. ⚠ Under the cap means SHORTER, never QUIETER: a "
                        f"declared gap that is dropped to fit has evaded this cap, not met it.")
                else:
                    warns.append(
                        _msg + f"PRE-CAP RECORD (banner "
                        f"#{_lat_sess if _lat_sess is not None else '?'} < "
                        f"#{BANNER_LATEST_CAP_FROM_SESSION}) — NOT a fail and NOT to be "
                        f"rewritten. Ratified record is never shaved to quiet a budget "
                        f"(#49/#51/#153 each did and each was wrong); the weight lands on the "
                        f"NEXT banner, at authoring time.")

    # ---- M10, RE-POINTED #33 (referent) and again #48 (UNIT): the READ CHAIN is header +
    # ★ LATEST + the LS LATEST delta, and the thing MEASURED against the cap is the whole
    # `_CHAIN.md` FILE that carries them — slice + `_gen_chain`'s wrapper. open 16 (a), Dave #47.
    # ⚠ The cap moved with the unit, by the SAME measured wrapper, so today's verdict is
    # arithmetically identical (ds-021 precedent: RESTATE openly, never silently tighten).
    # ADVISORY still, and the numbers are still agent-derived pending Dave (see the constant block).
    c_warn, c_block = CHAIN_BUDGET_TK
    # ⚠ Both messages lead with a UNIQUE tag. The first draft had the bites match on the substring
    # "read chain" — which also appears inside the corpus warn's own explanatory prose, so a fat-§A
    # fixture "warned the chain" when the chain had in fact measured 60 tk. A bite that matches on
    # a phrase two different messages share is not a bite. Tag, then match the tag.
    if chain_file is None:
        warns.append(f"M10 read chain UNMEASURED — {chain_file_detail} (slice: {chain_detail}). "
                     f"Not defaulted, not assumed clean: a chain budget that reports 0 on a parse "
                     f"failure reads GREEN on a broken file. Fix the structure, then re-run.")
    # ⚠ THE BLOCK-CANDIDATE BRANCH — ruled Dave 2026-08-02 (dream pass 4, P2 half (a)), enacted #128.
    # Until now `c_block` was unpacked and printed and NEVER COMPARED: a chain at the warn and a chain
    # a thousand tape past the block-candidate emitted the identical message, so the second tier was
    # decoration. This branch makes the tier VISIBLE. It is STILL ADVISORY and deliberately a WARN —
    # arming it, re-dialling it or retiring it is Dave's word alone, and nothing here may block.
    # Its tag is UNIQUE ("M10 read chain OVER THE BLOCK-CANDIDATE") so a bite cannot match the warn
    # tier's prose by substring — the lesson recorded three lines above this one.
    elif bill_of(chain_file) > bill_of(c_block):
        warns.append(f"M10 read chain OVER THE BLOCK-CANDIDATE — THE WHOLE `_CHAIN.md` FILE, which "
                     f"is what a cold session opens: {fmt_units(chain_file)}, PAST the "
                     f"block-candidate {c_block:,} tape / ~{bill_of(c_block):,} bill (warn "
                     f"{c_warn:,} tape / ~{bill_of(c_warn):,} bill). ⚠ STILL ADVISORY AND STILL A "
                     f"WARN — this tier has never been armed; arming, re-dialling or retiring it is "
                     f"Dave's word alone, and the numbers remain agent-derived. {chain_file_detail}. "
                     f"This check knows the total, not where the weight sits — measure the terms "
                     f"before picking one to trim, and note that the wrapper is the ONE term no "
                     f"editing of GM or _LIVE-STATE can move.")
    elif bill_of(chain_file) > bill_of(c_warn):
        warns.append(f"M10 read chain — THE WHOLE `_CHAIN.md` FILE, which is what a cold session "
                     f"opens: {fmt_units(chain_file)}, warn {c_warn:,} tape / "
                     f"~{bill_of(c_warn):,} bill · block-candidate {c_block:,} tape / "
                     f"~{bill_of(c_block):,} bill — ADVISORY, numbers agent-derived and awaiting "
                     f"Dave. {chain_file_detail}. This check knows the total, not where the weight "
                     f"sits — measure the terms before picking one to trim, and note that the "
                     f"wrapper is the ONE term no editing of GM or _LIVE-STATE can move.")
    else:
        notes.append(f"M10 read chain (whole `_CHAIN.md` file, the unit a cold session pays): "
                     f"{fmt_units(chain_file)} · warn {c_warn:,} tape / ~{bill_of(c_warn):,} bill "
                     f"(ADVISORY) · {chain_file_detail}. {ratio_status()}")
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


# ---------------------------------------------------------------------------- #54: the stop line
# ★★ WHY THIS IS A POSITIVE ASSERTION AND NOT A BAN, WHICH IS THE WHOLE DESIGN.
# The defect: `_RUNBOOK-context-gauge.md` stated ds-023's stop line correctly in one section
# (`60 − the priced wrap`; "60 is where the wrap has FINISHED, not where it starts") and
# CONTRADICTED it in two others ("RED ≥60% — fire the full trigger"), and
# `_RUNBOOK-capture-ritual.md` propagated the wrong half. Which rule a session got depended on
# which line it happened to land on. Dave, #54: *"the 60% is the total with the wrap included,
# it was never supposed to be 60 plus wrap."*
#
# ⚠ A BAN ON THE WRONG PHRASING IS UNREACHABLE HERE. The corrected prose QUOTES the old wrong
# form in order to mark it as wrong ("THIS LINE USED TO SAY …"), and so does this comment. A
# regex cannot separate USE from MENTION — [[gate-must-quote-what-it-forbids]], already paid for
# at open 24. ⇒ **Assert the RULING'S PRESENCE instead.** A positive assertion cannot be tripped
# by a quotation of what it forbids, and it fails on the thing that actually matters: someone
# editing the stop line back out, or a new home stating the trigger without it.
STOP_LINE_HOMES = {
    "knowledge/_RUNBOOK-context-gauge.md": (
        "60 − the priced wrap",
        "60 is where the wrap has FINISHED",
    ),
    "knowledge/_RUNBOOK-capture-ritual.md": (
        "60 − the priced wrap",
    ),
}


def stop_line_consistency(repo):
    """ds-023's stop line must be STATED in every home that triggers the ritual. Returns
    (fails, notes). BLOCKING at birth — unlike the usual advisory-first convention, because this
    is not a new rule being trialled: it is a ruling from #31, enacted #34, that was silently
    contradicted for eleven sessions and cost the same conversation repeatedly."""
    fails, notes = [], []
    missing_any = False
    for rel, required in STOP_LINE_HOMES.items():
        path = os.path.join(repo, *rel.split("/"))
        if not os.path.exists(path):
            notes.append(f"stop-line: {rel} absent — UNMEASURED, not passed.")
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        gone = [s for s in required if s not in text]
        if gone:
            missing_any = True
            fails.append(
                f"ds-023 stop line: {rel} no longer states {gone!r}. The in-flight trigger is "
                f"`60 − the priced wrap`, NOT a gauge reading of 60 — 60 is where the wrap has "
                f"FINISHED. If this was edited out, the file is back to the #54 state where the "
                f"corpus contradicted itself and sessions got whichever rule they landed on. "
                f"Re-state it, or re-rule it with Dave (the numbers are his).")
    if not missing_any:
        notes.append(f"ds-023 stop line: STATED in all {len(STOP_LINE_HOMES)} trigger homes "
                     f"(reconciled #54 — the runbook used to contradict itself).")
    return fails, notes


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


# ─────────────────────────────────────────────────────────────────────────────────────────────
# ★ THE OPTIONAL `subs` LINE — a SMALL GATE on an OPTIONAL line (Dave #168, option 2).
#
# The gauge-log block is hand-written by the conductor at wrap: there is NO writer, every
# production path only READS this file. Dave ruled ONE optional line into the block convention:
#
#     subs <N> tokens (n=<count>)
#
# — the total delegated SUB tokens for the session and the number of subs. Unit: REAL CLAUDE
# TOKENS, and it is a QUOTA figure, not window FILL [[budget-vs-quota-vocabulary]] — subs cost
# almost nothing in this window and 5–10× in the weekly quota, so the two must never be added
# together or graded against the stop line.
#
# ⛔ ABSENT IS LEGAL AND IS NEVER DEFAULTED. A wrap that measured no sub figures writes NO line;
# an UNKNOWN is never turned into a zero [[feedback-measuring-tool-must-not-guess]]. This check
# therefore says NOTHING when the line is absent — it only grades a line that IS there.
#
# ⚠ WHY THE WORD `job` IS FORBIDDEN ON THIS LINE, and why that is the POINT of the gate rather
# than a style rule: `gen_dashboard.py:332` sweeps this whole file with
# `_JOB_RE = re.compile(r"\bjob ([0-9][0-9,]{3,})\b")` and every match becomes a datapoint in the
# corpus the S/M/L effort-rung EDGES are derived from. A subs line spelled `subs job 40,000 …`
# would silently enter that corpus and move the band edges — a contamination with no error, no
# crash and no reader [[instrument-without-a-consumer]]. The containment is cheap here and
# uncatchable downstream, so it lives here.
SUBS_LINE_BLOCKING = True   # ⚠ TIER DECLARED, NOT RULED: blocking at birth because the damage it
                            # prevents is SILENT (a moved band edge nobody can see). Dave ruled
                            # the LINE and the GATE, not the tier; downgrading is this constant.

# Candidate detection is deliberately NARROW: a line whose lead token — after markdown quote and
# bold noise — is the word `subs`. Prose elsewhere in the log that merely mentions subs is out of
# scope, and saying so is cheaper than a parser that guesses [[gate-glob-scope-rule]].
SUBS_CANDIDATE_RE = re.compile(r"^\s*>?\s*\**\s*subs\b", re.I)
# The FORM, exact. Comma-grouping allowed in N; both numbers must be positive integers.
SUBS_FORM_RE = re.compile(
    r"^\s*>?\s*\**\s*subs\**\s+(\d{1,3}(?:,\d{3})+|\d+)\s+tokens\s+\(n=(\d+)\)\**\s*$", re.I)
SUBS_JOB_WORD_RE = re.compile(r"\bjob\b", re.I)
_SUBS_EXPECTED = "subs <N> tokens (n=<count>)   e.g.  subs 128,400 tokens (n=3)"


def gauge_log_subs_line(repo):
    """Grade the OPTIONAL `subs <N> tokens (n=<count>)` line in notes/_GAUGE-LOG.md.

    Returns (fails, notes). ABSENT ⇒ silent pass (nothing is added to either list beyond the
    positive note that the check ran) — absence is LEGAL. PRESENT ⇒ the form is exact, or a
    LOUD NAMED refusal quoting the expected form.

    ⚠ Fails LOUD and NAMED if the file cannot be read — a crash is not a fail
    [[a-crash-is-not-a-fail]] and neither is an unreadable file passing quietly."""
    fails, notes = [], []
    log = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    if not os.path.exists(log):
        notes.append("subs-line: no notes/_GAUGE-LOG.md — UNMEASURED, not assumed clean.")
        return fails, notes
    try:
        with open(log, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as e:
        fails.append(f"subs-line: notes/_GAUGE-LOG.md is UNREADABLE ({e}) — the optional "
                     f"`subs` line cannot be graded, and an unreadable file is not a clean one.")
        return fails, notes

    cands = [(i + 1, ln) for i, ln in enumerate(lines) if SUBS_CANDIDATE_RE.match(ln)]
    if not cands:
        notes.append("subs-line: no `subs …` line in notes/_GAUGE-LOG.md — LEGAL and NOT "
                     "defaulted. The line is optional; a wrap with no sub figures writes none.")
        return fails, notes

    for lineno, ln in cands:
        if SUBS_JOB_WORD_RE.search(ln):
            fails.append(
                f"subs-line CONTAMINATION at notes/_GAUGE-LOG.md:{lineno}: the word `job` "
                f"appears on a `subs` line — {ln.strip()!r}. ⛔ FORBIDDEN: gen_dashboard.py's "
                f"`_JOB_RE` (\\bjob <number>\\b) sweeps this file and every match becomes a "
                f"datapoint in the corpus the S/M/L effort-rung EDGES are derived from, so this "
                f"line would silently MOVE a band edge with no error and no reader. "
                f"Expected form, exactly: `{_SUBS_EXPECTED}`.")
            continue
        m = SUBS_FORM_RE.match(ln)
        if not m:
            fails.append(
                f"subs-line MALFORMED at notes/_GAUGE-LOG.md:{lineno}: {ln.strip()!r} is not the "
                f"ruled form. Expected, exactly: `{_SUBS_EXPECTED}` — N a positive integer "
                f"(comma-grouping allowed), `tokens` spelled out, and the sub COUNT as `(n=<int>)`. "
                f"Unit: REAL Claude tokens of QUOTA, never window fill. ⛔ Do NOT 'fix' this by "
                f"deleting the line if you HAVE the figures, and do NOT invent figures to satisfy "
                f"it if you do not — ABSENT is legal, a wrong number is not.")
            continue
        n_tok = int(m.group(1).replace(",", ""))
        n_subs = int(m.group(2))
        if n_tok <= 0 or n_subs <= 0:
            fails.append(
                f"subs-line at notes/_GAUGE-LOG.md:{lineno}: {ln.strip()!r} carries a "
                f"non-positive figure (tokens={n_tok}, n={n_subs}). A wrap that delegated nothing "
                f"OMITS the line; a zero is a claim, not an absence "
                f"[[feedback-measuring-tool-must-not-guess]]. Expected: `{_SUBS_EXPECTED}`.")
            continue
        notes.append(f"subs-line: notes/_GAUGE-LOG.md:{lineno} parses — {n_tok:,} sub tokens "
                     f"(QUOTA, real) across n={n_subs}. Form OK, `job` absent.")
    return fails, notes


# ─────────────────────────────────────────────────────────────────────────────────────────────
# ds-022 (d) — PRESENT BUT UNKEYED, the FOURTH STATE. Gated shut by Dave's ruling at #54.
#
# THE STATE, in the words of the record that raised it (`notes/_GAUGE-LOG.md` § META #41
# (second)): a session whose *testimony* EXISTS in `_GAUGE-LOG.md` but which never wrote a
# `#### <date> #<N>` key — so `STRATA_KEY_RE` is blind to it and `gauge_log_continuity` reports
# "left NO block" about a session that had in fact testified. #41 declined to write `HOLE #40`
# and was right to: `HOLE` is a POSITIVE claim of absence, the evidence was two screens up, and
# the marker would have forged the dataset the throttle is re-derived from.
#
# ⬛ DAVE'S RULING (#54, `notes/_GAUGE-LOG.md` § META — UNKEYED #40 #41 #42): **gate it shut,
# and mark the three.** ★ NOT a standing fourth vocabulary term. His reasoning, kept in his
# shape: the state is an artefact of *testimony* and *key* being two separate acts, so the wrap
# is gated to make it UNREACHABLE going forward and only the sessions that already reached it
# get a name. **A vocabulary term for a state that should not be possible is a permanent tax;
# prevention is not.**
#
# ★ WHY THE SCOPE IS ONE FILE — the #43 ruling's scope, not a convenience. `roll_2f` CANNOT
# produce this state: `_RUNBOOK-capture-ritual.md` § ds-022 lists "a post-mortem with no
# `#### <date> #<N>` key, which would be invisible to the check below" among the things the
# mover makes impossible. The only way in is the HAND-WRITTEN append the same step licenses
# ("append-only, one block per session"), and hand-writing produced all three cases.
# ⇒ **testimony in `_GAUGE-LOG.md` with no key in `_GAUGE-LOG.md` is a FILING ERROR, repaired
# by keying.** Testimony still sitting in `GOOD-MORNING.md` §C is a DIFFERENT state — an
# unrolled stratum, which is `roll_2f`'s job and ds-022 (a)'s alarm. This check must not annex
# it, and a wider glob here would make it fire on every session between wrap and roll.
#
# ⚠ WHY THIS IS NOT A DUPLICATE OF ds-022 (a). That check asks "did session N−1 leave a block?"
# — it looks for the PRESENCE of a key. This one asks the mirror question: "is there testimony
# that no key accounts for?" A file can fail (a) and fail (d) about the SAME session for
# opposite reasons, and at #41 it did — (a) was red while naming an absence that was not there.
# [[unmatched-grep-is-not-an-absence]], from the other side: a failed lookup is not an absence.
UNKEYED_BLOCKING = True

# The closed vocabulary of TESTIMONY labels, read OFF THE LIVE RECORD rather than imagined —
# `grep -nE '^\*\*[^*]*#[0-9]+' notes/_GAUGE-LOG.md` returned 18 lines at #55 and all 18 were
# classified by hand. `HOLE` and `ABSENT` are deliberately absent from this tuple: they are the
# DECLARATIONS that discharge the check, not testimony that needs discharging.
# ⚠ THE LIST IS NOT THE GUARD, and this is the whole safety argument. An unrecognised label is
# NOT silently ignored — `_UNKEYED_ANY_RE` and the second arm below catch it. Enumerating a
# vocabulary is exactly what [[scope-blindness-gate-vocabulary]] warns produces a blind gate;
# the rule it gives is "normalise once and FAIL LOUD on unknown". This tuple is the normalise
# half. The second arm is the fail-loud half, and without it this constant would be a liability.
TESTIMONY_LABELS = ("META", "ERRORS", "PRE-FLIGHT", "PAIR", "CLOSED", "BAND", "FILL", "OUTCOME")
# `[^#]*?` cannot cross a `#`, so the label must be the token immediately before the number —
# match the STRUCTURE, not the words. This is the fourth appearance of substring-vs-structure in
# this file (#35's usage probe, ds-016's index, #37's banner regex) and the first to be written
# knowing it: `**RAISED AT #41, OPEN THIRTEEN SESSIONS…` is PROSE about #41, not #41 testifying,
# and an unanchored search for "#41 near a bold line" cannot tell the two apart.
_TESTIMONY_RE = re.compile(r"^\*\*[^#]*?\b(%s)\s+#(\d+)\b" % "|".join(TESTIMONY_LABELS))
_UNKEYED_ANY_RE = re.compile(r"^\*\*[^#]*?#(\d+)\b")


def unkeyed_testimony(repo):
    """ds-022 (d) — BLOCKING AT BIRTH (Dave #54). Returns (fails, notes).

    ⚠ Blocking at birth breaks this file's advisory-first convention, and the reason is on the
    record rather than in a preference. The state was raised at #41 and stayed OPEN for thirteen
    sessions; the remedy actually applied in the meantime was a RETROACTIVE key, added to quiet
    the parser while the ruling was outstanding. That patch made three unrolled sessions look
    rolled, which is why #53's handoff — *"2f IS 12 BLOCKS DEEP … roll all 12"* — was never a
    runnable instruction. It was 9. **An advisory tier here licenses precisely the patch that
    caused the damage**, so the tier is the finding, not a default.

    ⚠ WHAT IT CANNOT SEE, said plainly so nobody reads more into a green: whether the testimony
    under a key is ABOUT that session, and whether its content is honest. It settles one thing —
    that every session the file testifies about is accounted for by a key or a declaration. Do
    not teach it to grade prose; ds-022 (a)'s docstring makes the same refusal for the same
    reason."""
    fails, notes = [], []
    log = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    if not os.path.exists(log):
        notes.append("ds-022 (d) unkeyed: no notes/_GAUGE-LOG.md — UNMEASURED, not assumed "
                     "clean. (An absent file is not a clean file; the M10 refusal pattern.)")
        return fails, notes

    with open(log, encoding="utf-8") as f:
        lines = f.read().splitlines()

    keyed = {n for n in (_key_session(ln) for ln in lines
                         if STRATA_KEY_RE.match(ln)) if n is not None}
    declared = {n for n in (_key_session(ln) for ln in lines
                            if HOLE_RE.match(ln) or ABSENT_RE.match(ln)) if n is not None}
    accounted = keyed | declared

    testimony, unclassified = {}, {}
    for ln in lines:
        m = _TESTIMONY_RE.match(ln)
        if m:
            testimony.setdefault(int(m.group(2)), ln)
            continue
        m = _UNKEYED_ANY_RE.match(ln)
        if m:
            unclassified.setdefault(int(m.group(1)), ln)

    def _quote(ln):
        ln = ln.strip()
        return ln if len(ln) <= 110 else ln[:107] + "…"

    for n in sorted(set(testimony) - accounted):
        fails.append(
            f"ds-022 (d) PRESENT BUT UNKEYED: notes/_GAUGE-LOG.md carries testimony for "
            f"session #{n} with no `#### <date> #{n}` key and no `HOLE #{n}`/`ABSENT #{n}` "
            f"line, so every parser in this file is blind to it — including ds-022 (a), which "
            f"will report that #{n} \"left NO block\" and invite a HOLE line that would be "
            f"FALSE. The line: {_quote(testimony[n])} "
            f"FIX — write the key above the testimony you just wrote: "
            f"`#### <date> #{n} — <descriptor>`. ⛔ Do NOT declare `HOLE #{n}`: HOLE is a "
            f"positive claim that the session wrote nothing, and the evidence above disproves "
            f"it. ⛔ Do NOT roll it with `roll_2f` either — the duplicate-key guard will refuse "
            f"once a key exists here, and it is right to. This is the fourth state Dave ruled "
            f"UNREACHABLE at #54: testimony and key are ONE act.")

    for n in sorted(set(unclassified) - accounted - set(testimony)):
        fails.append(
            f"ds-022 (d) UNCLASSIFIED MARKER: notes/_GAUGE-LOG.md has a bold-lead line naming "
            f"session #{n}, which has no key and no HOLE/ABSENT line — and the label is not one "
            f"this check recognises ({', '.join(TESTIMONY_LABELS)}). It is REFUSING TO GUESS "
            f"rather than passing, because a vocabulary gate that ignores what it does not "
            f"recognise is how this repo has gone blind before. The line: {_quote(unclassified[n])} "
            f"FIX — if it IS testimony, key #{n} and add its label to `TESTIMONY_LABELS`; if it "
            f"is prose that merely mentions #{n}, either key/declare #{n} or reword so the "
            f"number is not in a structural position. ★ Note this arm stays SILENT whenever "
            f"#{n} is accounted for, so it costs nothing on a clean file.")

    if not fails:
        notes.append(
            f"ds-022 (d) unkeyed: {len(testimony)} session(s) testify in notes/_GAUGE-LOG.md "
            f"and every one is accounted for — {len(keyed)} keyed · {len(declared)} declared "
            f"HOLE/ABSENT · {len(unclassified)} unclassified bold-lead mention(s), all of them "
            f"about accounted sessions. (Said out loud on the passing path: a check that is "
            f"silent when it succeeds cannot be told apart from one that is dead.)")
    return fails, notes


# ─────────────────────────────────────────────────────────────────────────────────────────────
# T2 (#77) — roll_claim_check. Handoff testing regime, RULED #77 (ledger § ★ #77;
# notes/2026-08-02-handoff-testing-regime-plan.md). ⚠ R3 CORRECTION, found at ledger read-back
# (the plan's own top block): the commit-vs-wrap dichotomy the plan floated was FALSE — #74-D1
# already runs `_capture_gate.py --wrap` from `_git_commit.sh` (the WARN/`--wrap` mode split).
# Enactment shape: this check lives INSIDE `wrap_checks()` — the existing #74-D1 consumer
# delivers it at the commit seam. No new wiring in the shell script beyond T3's headline work.
#
# Seam it closes: the DURABILITY seam (#73/#75/#76's forward-claim class — a banner authored
# before the last state change, falsified by that change). T1 (`_roll_state.py`) measures the
# actual roll state; this check grades any roll-residual line in the ★ LATEST banner against
# that measurement.
ROLL_CLAIM_BLOCKING = True

# ---- the ONE legal home for the claim, scoped to the EXACT quoted form per
# [[gate-must-quote-what-it-forbids]]: the GENERATED form `_roll_state.py` itself prints — the
# canonical line this whole mechanism exists to make the banner carry instead of authored prose.
# ⛔ #77 (2026-08-02): there used to be a SECOND arm here — an AUTHORED-form regex reading
# `2c`/`2d`/`2f` adjacent to `NOT run|OK|rolled` anywhere in the banner. It false-fired on
# RATIFIED #76 banner text at its very first live `--wrap` run: once on the narration word
# "RESIDUAL" in the ★ LATEST heading ("THE CHAIN BOOTED ME ON A FALSE RESIDUAL"), once on the
# banner QUOTING #75's claim verbatim ("the 2c/2d/2f rolls were NOT run", attributed to #75,
# italicised, discussing a PAST session's defect). USE vs MENTION is unreachable by syntax — no
# regex can tell a fresh claim from a quotation of an old one sitting in the SAME banner — only
# SCOPE saves it, exactly the house precedent at `ABS_TERM_RE` above (#58: requiring the leading
# digit fixed USE-vs-MENTION "for free" there; here the anchor is the GENERATED marker itself).
# The fix is not a smarter regex for arm (ii); it is DELETING arm (ii). This check now has
# exactly one legal home for the claim — the generated line — so prose is narration BY
# DEFINITION: there is nowhere else the claim is allowed to live, so anything else is not a
# rival claim to adjudicate, it is commentary. Widening the old vocabulary (adding exceptions
# for "narration" or "quotation") was rejected as the #58-class fix: it enumerates escapes into
# a gate that should instead not be looking there at all
# ([[scope-blindness-gate-vocabulary]]).
_ROLL_GENERATED_RE = re.compile(
    r"residual\s*\(GENERATED\s*#(\d+)\)[:*\s]*"
    r"2c\s+(OK|OVER)\s*\(banners\s+(\d+)/2\)\s*[·.]\s*"
    r"2d\s+(OK|OVER)\s*\(deltas\s+(\d+)/3\)\s*[·.]\s*"
    r"2f\s+(OK|OVER)\s*\(strata\s+(\d+),\s*log\s*#(\d+)\)", re.I)
# The ANCHOR used to find candidate lines before full parsing — deliberately narrower than
# `_ROLL_GENERATED_RE` itself (which requires the whole shape to match). A line can anchor here
# and still fail to parse (a mangled paste); that is a NAMED parse failure, not a crash and not
# a second guess at what the line meant.
_ROLL_GENERATED_ANCHOR_RE = re.compile(r"\*\*\s*residual\s*\(GENERATED", re.I)
_BANNER_LATEST_START_RE = re.compile(r"^\s*>?\s*#{1,6}\s*★\s*LATEST\b")
_BANNER_PRIOR_START_RE = re.compile(r"^\s*>?\s*#{1,6}\s*★\s*PRIOR\b")


def _latest_banner_region(gm_text):
    """The ★ LATEST banner's own text — heading to the next ★ PRIOR heading, or EOF. Same
    anchor family as `BANNER_SESSION_RE`/`LATEST_SESSION_RE` (blockquoted, line-start `> ## ★`
    — the #37 lesson: match the STRUCTURE, never an unanchored substring). Returns None if no
    ★ LATEST heading is found (a different check already fails the wrap for that; not re-raised
    here)."""
    lines = gm_text.splitlines()
    start = next((i for i, ln in enumerate(lines) if _BANNER_LATEST_START_RE.match(ln)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines))
               if _BANNER_PRIOR_START_RE.match(lines[i])), len(lines))
    return "\n".join(lines[start:end])


def roll_claim_check(repo):
    """T2 (#77) — grades the ★ LATEST banner's roll-residual claim against `_roll_state.py`'s
    live measurement. Returns (fails, warns, notes).

    GENERATED-LINE-ONLY SCOPE (#77, 2026-08-02 — replaces the two-arm design that lived here
    through its first live run). The claim's only legal home is the line `_roll_state.py`
    prints; this check finds that line by its anchor (`**residual (GENERATED`), parses it, and
    grades it. It scans NO other line — a heading that narrates "RESIDUAL" and a paragraph that
    quotes a past session's claim verbatim are both prose, and prose is not scanned, because the
    claim has exactly one legal home and that isn't it. See the `_ROLL_GENERATED_ANCHOR_RE`
    comment above for why the old authored-form arm was deleted rather than widened: it
    false-fired on RATIFIED #76 text (the heading word + a quoted, attributed #75 claim) at its
    first live `--wrap` run — USE vs MENTION is unreachable by syntax, only SCOPE saves it.

    Presence-gating, not just contradiction-gating: ZERO generated lines is itself a FAIL (the
    ritual step was skipped, not merely unverifiable), and MORE THAN ONE is a FAIL (duplicate
    homes for a claim that gets exactly one).
    """
    fails, warns, notes = [], [], []
    gm_path = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm_path):
        notes.append("roll-claim check: no GOOD-MORNING.md — UNMEASURED, not assumed clean.")
        return fails, warns, notes
    with open(gm_path, encoding="utf-8") as f:
        gm_text = f.read()
    region = _latest_banner_region(gm_text)
    if region is None:
        notes.append("roll-claim check: no ★ LATEST banner found — UNMEASURED (a different "
                     "check already fails the wrap for this state; not re-raised here).")
        return fails, warns, notes

    candidates = [ln for ln in region.splitlines() if _ROLL_GENERATED_ANCHOR_RE.search(ln)]

    if not candidates:
        fails.append(
            "roll-claim check: no generated residual line in ★ LATEST — run "
            "`python3 knowledge/_roll_state.py` and paste its line into the banner (ritual "
            "step 2; #77-D1). The claim's only legal home is that generated line; its absence "
            "is itself the finding, not a warn.")
        return fails, warns, notes

    if len(candidates) > 1:
        fails.append(
            f"roll-claim check: {len(candidates)} generated residual lines in the ★ LATEST "
            f"banner — the claim has exactly one legal home, not several (duplicate homes). "
            f"Lines: " + " | ".join(c.strip()[:150] for c in candidates))
        return fails, warns, notes

    line = candidates[0]
    m = _ROLL_GENERATED_RE.search(line)
    if not m:
        fails.append(
            "roll-claim check: a line anchors the generated form (`**residual (GENERATED`) but "
            "does not parse against its full shape — fail loud and named rather than guess at "
            "what it meant. Expected: `residual (GENERATED #N): 2c OK|OVER (banners n/2) · 2d "
            "OK|OVER (deltas n/3) · 2f OK|OVER (strata n, log #K) — _roll_state.py · date`. "
            f"Line: {line.strip()[:200]}")
        return fails, warns, notes

    try:
        measured = roll_state.measure(repo)
    except roll_state.Unparseable as e:
        fails.append(
            f"roll-claim check: the banner carries a generated residual line but "
            f"_roll_state.py cannot measure the tree to grade it ({e}). "
            f"Line: {line.strip()[:200]}")
        return fails, warns, notes

    rendered = roll_state.render_line(measured)
    claim = (int(m.group(1)), m.group(2).upper(), int(m.group(3)),
             m.group(4).upper(), int(m.group(5)), m.group(6).upper(),
             int(m.group(7)), int(m.group(8)))
    actual = (measured["session_no"],
              "OK" if measured["banners"] <= 2 else "OVER", measured["banners"],
              "OK" if measured["deltas"] <= 3 else "OVER", measured["deltas"],
              "OK" if measured["strata_live"] <= 1 else "OVER", measured["strata_live"],
              measured["log_newest"])
    if claim != actual:
        fails.append(
            f"roll-claim check: GENERATED-form residual contradicts the measured tree. "
            f"Banner: {line.strip()[:200]} — Measured (re-derived via _roll_state.py, one "
            f"measurer, no second slicer): {rendered}")
    else:
        notes.append(f"roll-claim check: the ★ LATEST banner's generated residual line is "
                     f"consistent with the measured tree ({rendered}).")
    return fails, warns, notes


# ------------------------------------------------ THE STALE-TOP-ITEM FENCE (s161-D4, #161)
# ★ WRAP MODE ONLY, and BLOCKING at birth by Dave's word ("okay do it" on a read-back that named
# block-not-warn). THE DEFECT IT ENDS, verbatim: #160's wrap wrote *"`s142-D1` is the next
# window's top item"* while `knowledge/_rulings.json` already carried
# `s142-D1.status = "RULED #142, ENACTED #143: …"`. Two sessions carried that false "owed", and
# NOTHING compared the claim to the store the wrap already parses. A warn under wrap heat is a
# warn nobody reads [[instrument-without-a-consumer]] [[premise-ages-faster-than-rule]].
STALE_TOP_BLOCKING = True

_RULING_ID_RE = re.compile(r"\bs\d+-D\d+\b")

# ★ SCOPE BY HOME, NOT BY PROSE — the #77 lesson this module already learned the hard way
# (`roll_claim_check`: *"USE vs MENTION is unreachable by syntax, only SCOPE saves it"*). An
# owed-work claim's ONE legal home is the wrap's hand-off line, `residual → #N:`, at line start
# (blockquote/bold chrome allowed). A narrative sentence that QUOTES a past residual mid-line —
# e.g. #161's own banner, *"#160's `residual → #161` opened with …"* — does NOT match this
# anchor and is never scanned.
_RESIDUAL_HOME_RE = re.compile(r"^\s*>?\s*\**\s*residual\s*(?:→|->)\s*#\d+", re.I)

# The owed-work vocabulary, QUOTED not paraphrased ([[gate-must-quote-what-it-forbids]]).
_OWED_CONTEXT_RES = (
    re.compile(r"top item", re.I),
    re.compile(r"\bowed\b", re.I),
    re.compile(r"next window", re.I),
    re.compile(r"next session's top", re.I),
    re.compile(r"\bnew top\b", re.I),        # the residual-line shorthand `[0 — NEW TOP]`
)

# ⚠ THE CONTEXT WINDOW IS NARROW AND ITS WIDTH IS THE RULE. A residual line is one very long
# line carrying ~20 unrelated items; "same line" is far too wide a claim-context. The owed
# phrase must fall within ±STALE_TOP_WINDOW characters of the cited id — the adjacent clause,
# not the paragraph.
STALE_TOP_WINDOW = 160


def _asserts_enacted(text):
    """True iff `text` contains an UNNEGATED `enacted`. ONE predicate, TWO consumers, on
    purpose: it reads the store's `status` field AND the claim's own context window, so the
    gate can never call a status "enacted" by one rule and a citation "enacted" by another.

    `\\benacted\\b` cannot match inside `unenacted` (no word boundary), and an immediately
    preceding `not` / `not-` / `never` (as in `RULED-NOT-ENACTED`) is skipped."""
    for m in re.finditer(r"\benacted\b", text, re.I):
        pre = text[max(0, m.start() - 12):m.start()].lower()
        if re.search(r"(?:not|never)\s*-?\s*$", pre):
            continue
        return True
    return False


def _rulings_status_map(repo):
    """{ruling id: status string} from `knowledge/_rulings.json`, or (None, reason). Fails LOUD
    and NAMED rather than degrading into an empty map — an unreadable store must read as
    UNMEASURED, never as "no ruling contradicts this claim" ([[a-crash-is-not-a-fail]])."""
    path = os.path.join(repo, "knowledge", "_rulings.json")
    if not os.path.exists(path):
        return None, "knowledge/_rulings.json does not exist"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        rows = data["rulings"] if isinstance(data, dict) else data
        return {r["id"]: str(r.get("status", "")) for r in rows if r.get("id")}, None
    except Exception as e:                                      # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


# ════════════════════════════════════ THE 2c CARRY GATE — s188-D2 (Dave, RULED #188) ═══════
# THE RULE IT ENFORCES, verbatim from the ruling: *"The 2c carry rule's 'AGES +1, WORDING
# UNCHANGED' invariant gains exactly one exit: a carried claim's wording may change ONLY to
# record a retraction, and the edit MUST cite its receipt (the run or commit that proved the
# claim false), the same way a repo claim cites git log. An edit without a receipt token is
# refused by the carry gate exactly as today."*
#
# ⚠ DECLARED AT BIRTH, because the ruling's premise says "exactly as today" and TODAY IS NOT
# WHAT IT SOUNDS LIKE: before this build there was NO carry gate in code at all. `s183-D1` P2
# and the "AGES +1, WORDING UNCHANGED" invariant lived ONLY as prose in
# `_RUNBOOK-capture-ritual.md` §2c — a rule no machine had ever refused anything under
# [[instrument-without-a-consumer]]. So the carve-out could not be added to an existing gate:
# the gate is BUILT HERE and the carve-out is built INTO it, which is why both directions have
# to be mutation-proven before it blocks (they are: `--selftest`, the (C*) bites).
#
# THE IDENTITY PROBLEM, and why the age bracket solves it. A wording-change check needs to pair
# an item across two banners, and wording is the very thing that moved. The pairing key is the
# thing `s128-D2` made mandatory and this gate does NOT invent: the AGE BRACKET. A carry ages
# by exactly one per wrap, so a PRIOR item at `[N]` pairs with a LATEST item at `[N+1]`, and the
# pair is only accepted when the two texts are ALSO near-identical (`CARRY_SIM_MIN`). Both
# conditions must hold, which is what keeps this off unrelated items that merely share an age.
#
# ⛔ WHAT IT DOES NOT DO. It does not detect a DROPPED carry (that is 2c's EXIT CHECK, prose,
# and widening this gate to presence would duplicate a rule at a second home). It does not
# judge whether a retraction is TRUE — only that the edit cites a receipt a reader can follow.
# ★ BLOCKING AT BIRTH, because s188-D2 says "refused" and a warn is not a refusal — but the
#   base rate was MEASURED BEFORE THE FLAG WAS SET, not assumed. The gate was driven on the
#   last TEN archived wrap pairs in `_GM-ARCHIVE.md` (each rebuilt into a LATEST/PRIOR
#   fixture): 11 un-receipted rewordings total — 1 · 0 · 7 · 0 · 0 · 1 · 0 · 2 · 0 · 0. Every
#   sampled one is the SAME shape and none is cosmetic: a carry TRUNCATED as it ages, dropping
#   the evidence pointer it was born with (`… not instrumented (s172-D3(e))` → `… not
#   instrumented`; `ELEVEN _governs FAILS — s179's own two were fixed to 0; the remainder is
#   RATIFIED RECORD` → `ELEVEN _governs FAILS — RATIFIED RECORD`). That is exactly the drift
#   the invariant exists to stop, at ~1 per wrap, which a wrap can afford to fix.
#   ⚠ AN EARLIER PAIRING KEY (similarity ratio) SCORED 72 ON THE SAME TEN WRAPS. The extra 61
#   were FALSE PAIRS, not findings — the number moved because the KEY changed, and it is
#   recorded here so nobody re-quotes 72 as a measurement of anything.
CARRY_GATE_BLOCKING = True       # s188-D2 built #189, mutation-proven both directions first
CARRY_SIM_MIN = 0.86             # ⚠ PICKED, NOT DERIVED — the same standing as
                                 # `GRADE_AGING_DAYS` and `STALE_AFTER_SESSIONS`. It is a
                                 # PAIRING guard, not a verdict: below it the two items are
                                 # not treated as the same carry at all.
# ⚠ THE QUALIFIER CLASS CARRIES A COMMA SINCE #214, AND THAT COMMA IS THE WHOLE REPAIR.
# The banner form `[2, DAVE'S]` has been in use since #212, and this regex could not see it:
# the bracket survived `_carry_norm`'s stripping, so a carry re-typed at AGES +1 EXACTLY AS THE
# 2c INVARIANT DEMANDS compared as CHANGED. #213 MEASURED the blindness and reported it as
# unrepaired (its banner residual ⑤). #214 hit the consequence: with sixteen re-typed carries a
# pair finally matched on title, and `carry_wording_check` — which is BLOCKING — refused a wrap
# whose carries were verbatim-correct, quoting a diff consisting ONLY of the age digits it was
# supposed to have stripped. ⛔ THAT IS A GATE THAT CANNOT PASS ON CORRECT BEHAVIOUR
# [[gate-cannot-pass-in-one-environment]], which is the one shape the ritual says must never be
# left standing — it teaches sessions to fake the artefact rather than fix the parser
# [[honest-refusal-needs-a-legal-form]]. Widened, and mutation-driven BOTH ways at #214:
# an AGES+1-only edit now passes silently, and a real wording change still FAILS unreceipted.
# ⛔ NO THRESHOLD, TIER OR POLICY MOVED — `CARRY_GATE_BLOCKING` is untouched and the s183-D1 /
# s188-D2 contract is unchanged. This lets the gate MEASURE what it was already required to.
_AGE_RE = re.compile(r"\[(\d+)(?:\s*[,—-][^\]]*)?\]")
_RETRACTION_MARKER_RE = re.compile(r"RETRACT(?:ED|ION)|STRUCK|~~", re.I)
_RECEIPT_SESSION_RE = re.compile(r"#\d{1,4}\b")
_RECEIPT_INSCRIPTION_RE = re.compile(r"s\d{2,4}-D\d+|`[^`]+\.(?:py|md|json|css|html|sh)[^`]*`"
                                     r"|\b[0-9a-f]{7,40}\b")
_RESIDUAL_LINE_RE = re.compile(r"^>?\s*\*\*residual\s*→\s*#(\d+)", re.I)
# ★ s225-D2 (#225, Dave's): the carry lists LEFT the GM banners for `_CARRIES.md`; both GM
# residual lines are now POINTERS carrying this marker. From #226 the gate FOLLOWS the pointer
# (re-pointed here per the owed item GM:34 names) — before this, it read the pointer lines
# themselves, found ~nothing aged, and reported a clean-looking `0 aged carries`, which is the
# silent state [[roll-pointer-is-not-an-absence]] this resolver exists to make loud.
_POINTER_MARKER_RE = re.compile(r"THIS LINE IS A POINTER", re.I)
CARRIES_FILE = "_CARRIES.md"


def _resolve_residual_pointer(repo, line, fails, notes):
    """Follow a POINTER residual line into `_CARRIES.md`; return the line to grade.

    A non-pointer line returns unchanged — pre-s225-D2 banners (and every archived fixture)
    still grade in place. A pointer that resolves to NOTHING appends a FAIL and returns None:
    an unreachable carry set means the s188-D2 invariant cannot be measured, and this gate is
    BLOCKING — it refuses by name rather than passing on an absence
    [[measuring-tool-must-not-guess]].
    """
    if not _POINTER_MARKER_RE.search(line):
        return line
    m = re.search(r"\*\*residual\s*→\s*#(\d+):?\*\*", line)
    if not m:
        fails.append("2c carry gate: a POINTER residual line names no `#N` — it cannot be "
                     "resolved into `%s`, so the carry set is UNREACHABLE. Refused, never "
                     "silently clean." % CARRIES_FILE)
        return None
    n = m.group(1)
    path = os.path.join(repo, CARRIES_FILE)
    if not os.path.exists(path):
        fails.append("2c carry gate: residual → #%s is a POINTER but `%s` does not exist — "
                     "the carry set is UNREACHABLE. A pointer that resolves to nothing is "
                     "the failure this gate exists for, not an absence." % (n, CARRIES_FILE))
        return None
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if ("**residual → #%s:**" % n) in ln and not _POINTER_MARKER_RE.search(ln):
                notes.append("2c carry gate: residual → #%s resolved from its GM pointer "
                             "into `%s` (the s225-D2 home) — pairing runs on the REAL list."
                             % (n, CARRIES_FILE))
                return ln
    fails.append("2c carry gate: residual → #%s is a POINTER but `%s` has no matching "
                 "`**residual → #%s:**` list line — the carry set is UNREACHABLE (refused, "
                 "never silently clean)." % (n, CARRIES_FILE, n))
    return None


def _carry_norm(seg):
    """Normalise a carry segment for comparison: age bracket, marks and emphasis removed."""
    s = _AGE_RE.sub(" ", seg)
    s = re.sub(r"[*_`~]+", " ", s)
    s = re.sub(r"[⚠⬛✅★⛔⚙·•]+", " ", s)
    return " ".join(s.split()).casefold()


def _carry_title(seg):
    """The carry's IDENTITY: its normalised text before the first em dash (s128-D2's shape,
    `⚠ **TITLE [N]** — body`). A retraction strikes the title but keeps its words, so the key
    survives exactly the edit the carve-out permits."""
    head = re.split(r"—", seg, 1)[0]
    return _carry_norm(head)


def _carry_items(residual_line):
    """The `·`-separated carry segments of one residual line that CARRY AN AGE.

    A segment with no `[N]` bracket is this session's NEW item (`[NEW — 0]` is stripped to 0 by
    `_AGE_RE`, so new items DO carry age 0 and pair with `[1]` next wrap — which is exactly the
    contract). Returns [(age:int, segment:str)].
    """
    # ⛔ STRIP THE LINE'S OWN PREFIX FIRST. `> **residual → #189:**` differs from `→ #190` by
    # construction every single wrap, and leaving it inside the first segment made the FIRST
    # carry on every banner read as "reworded" — caught by the (C1) bite before this gate was
    # wired, which is the whole reason the bite is a PAIR and not a smoke test.
    body = re.sub(r"^>?\s*\*\*residual\s*→\s*#\d+:?\*\*", "", residual_line.strip())
    out = []
    for seg in body.split("·"):
        m = _AGE_RE.search(seg)
        if m and len(_carry_norm(seg)) >= 20:      # a bare bracket is not a carry
            out.append((int(m.group(1)), seg.strip()))
    return out


def retraction_receipt(text):
    """(ok, why-NOT). The carve-out's ONE test, applied to the CHANGED wording.

    s188-D2 requires TWO things of a wording change, and this function refuses each by name:
      1. it must SAY it is a retraction (marker: RETRACTED / RETRACTION / STRUCK / ~~strike~~)
      2. it must CITE the receipt — a session `#N` *and* an inscription a reader can open
         (a ruling id `sNNN-DN`, a backticked repo path, or a commit sha)
    ⛔ A marker without a receipt is the failure this gate exists for: "we changed our minds"
    is prose; "#182 proved it false, inscribed at `s183-D1`" is a record.
    """
    if not _RETRACTION_MARKER_RE.search(text):
        return False, ("the wording changed but says NOTHING about a retraction — the 2c "
                       "invariant is AGES +1, WORDING UNCHANGED, and the only exit (s188-D2) "
                       "is a retraction that names itself (RETRACTED / STRUCK / ~~struck~~)")
    has_session = bool(_RECEIPT_SESSION_RE.search(text))
    has_inscription = bool(_RECEIPT_INSCRIPTION_RE.search(text))
    if has_session and has_inscription:
        return True, ""
    missing = []
    if not has_session:
        missing.append("the SESSION that proved it false (`#N`)")
    if not has_inscription:
        missing.append("WHERE the correction is inscribed (a ruling id `sNNN-DN`, a backticked "
                       "repo path, or a commit sha)")
    return False, ("a retraction WITHOUT its receipt is refused (s188-D2) — missing "
                   + " and ".join(missing))


def carry_wording_check(repo):
    """s188-D2 — the 2c carry gate. Returns (fails, notes). BLOCKING (`CARRY_GATE_BLOCKING`).

    Pairs every aged carry on the ★ PRIOR banner's `residual → #N` line with the same carry on
    the ★ LATEST banner's line (`[N]` → `[N+1]`, near-identical text). Identical wording passes
    silently. CHANGED wording passes ONLY with a retraction receipt, and FAILS without one,
    quoting both texts so the reader can see exactly what moved.
    """
    fails, notes = [], []
    gm_path = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm_path):
        notes.append("2c carry gate: no GOOD-MORNING.md — UNMEASURED, not assumed clean.")
        return fails, notes
    with open(gm_path, encoding="utf-8") as f:
        gm_text = f.read()
    lines = gm_text.splitlines()
    latest_start = next((i for i, ln in enumerate(lines)
                         if _BANNER_LATEST_START_RE.match(ln)), None)
    prior_start = next((i for i, ln in enumerate(lines)
                        if _BANNER_PRIOR_START_RE.match(ln)), None)
    if latest_start is None or prior_start is None or prior_start <= latest_start:
        notes.append("2c carry gate: no ★ LATEST + ★ PRIOR pair found — UNMEASURED. ⛔ Not a "
                     "pass: with one banner there is nothing to carry FROM, and the banner "
                     "structure itself is graded by other checks.")
        return fails, notes
    prior_end = next((i for i in range(prior_start + 1, len(lines))
                      if _BANNER_PRIOR_START_RE.match(lines[i])), len(lines))

    def _residual(lo, hi):
        return next((lines[i] for i in range(lo, hi) if _RESIDUAL_LINE_RE.match(lines[i].strip())
                     or "**residual → #" in lines[i]), None)

    latest_line = _residual(latest_start, prior_start)
    prior_line = _residual(prior_start, prior_end)
    if latest_line is None or prior_line is None:
        notes.append("2c carry gate: one of the two banners has no `**residual → #N:**` line — "
                     "UNMEASURED. The roll-claim check (T2 #77) grades that line's presence; "
                     "this gate refuses to invent a carry set from prose.")
        return fails, notes

    # ★ s225-D2 re-point (#226): a residual line that is a POINTER is followed into
    # `_CARRIES.md` and the REAL list graded; an unresolvable pointer is a FAIL above.
    latest_line = _resolve_residual_pointer(repo, latest_line, fails, notes)
    prior_line = _resolve_residual_pointer(repo, prior_line, fails, notes)
    if latest_line is None or prior_line is None:
        return fails, notes

    latest_items = _carry_items(latest_line)
    prior_items = _carry_items(prior_line)
    by_age = {}
    for age, seg in latest_items:
        by_age.setdefault(age, []).append(seg)
    checked = changed = 0
    for age, seg in prior_items:
        norm = _carry_norm(seg)
        cands = by_age.get(age + 1, [])
        if not cands:
            continue                     # dropped, consumed, or not aged — 2c's EXIT CHECK
        if any(_carry_norm(c) == norm for c in cands):
            checked += 1
            continue                     # AGES +1, WORDING UNCHANGED — the invariant holds
        # ⚠ SIMILARITY IS NOT THE PAIRING KEY — the TITLE IS. Two attempts were driven before
        # this one and both were wrong on real data: a ratio-only guard missed the dominant
        # shape (carries are TRUNCATED, not paraphrased — the evidence pointer falls off the
        # end, and a 25% truncation scores ~0.85), and a shared-opening guard missed the case
        # the ruling is actually about (a STRUCK retraction diverges early, by design). The
        # banner's own grammar gives a structural key for free: every carry is
        # `⚠ **TITLE [N]** — body`, and a retraction strikes the TITLE but keeps its words. So
        # the key is the normalised text BEFORE the first em dash, and the ratio is reported
        # as evidence, never used as the test.
        key = _carry_title(seg)
        best = next((c for c in cands if _carry_title(c) == key and key), None)
        if best is None:
            continue                     # not the same carry — no pairing, no claim
        ratio = difflib.SequenceMatcher(None, norm, _carry_norm(best)).ratio()
        checked += 1
        changed += 1
        ok, why = retraction_receipt(best)
        if ok:
            notes.append(f"2c carry gate: `[{age}]`→`[{age + 1}]` wording CHANGED and carries "
                         f"its retraction receipt (s188-D2 carve-out) — {_flat_carry(best)}")
        else:
            fails.append(
                f"2c CARRY WORDING CHANGED WITHOUT A RETRACTION RECEIPT (s188-D2) — "
                f"`[{age}]`→`[{age + 1}]`, {ratio:.2f} similar. {why}.\n"
                f"        WAS (#PRIOR): {_flat_carry(seg)}\n"
                f"        NOW (LATEST): {_flat_carry(best)}\n"
                f"        Remedy: restore the wording verbatim, OR strike it as a retraction "
                f"naming the session that disproved it and where the correction is inscribed "
                f"(_RUNBOOK-capture-ritual.md §2c, s183-D1 P2 / s188-D2).")
    if prior_items and checked == 0:
        notes.append(
            "2c carry gate: NOTHING PAIRED — the LATEST banner carries BY REFERENCE (the "
            "'PRIOR CARRIES, AGES +1, WORDING UNCHANGED' sentence pointing at the PRIOR "
            "banner) rather than re-typing the list. ⛔ THAT IS NOT A PASS: with no re-typed "
            "text there is nothing for this gate to compare, and it says so instead of "
            "reporting a clean run [[measuring-tool-must-not-guess]].")
    notes.append(f"2c carry gate (s188-D2): {len(prior_items)} aged carries on the PRIOR "
                 f"residual, {checked} paired into LATEST, {changed} reworded, "
                 f"{len(fails)} without a receipt. ⛔ Pairing key = the age bracket + "
                 f"the title before the em dash (STRUCTURAL); an unpaired carry is NOT graded here — "
                 f"presence is 2c's EXIT CHECK, prose.")
    return fails, notes


def _flat_carry(s, n=140):
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def stale_top_item_check(repo):
    """s161-D4 (Dave, RULED #161) — a wrap may not certify an OWED-WORK claim that cites a
    ruling id whose `_rulings.json` status already says ENACTED. Returns (fails, notes).
    BLOCKING (`STALE_TOP_BLOCKING`); a flip must land with its own ruling and edit that pin.

    ⚠ SCOPE, DOCUMENTED BECAUSE THE NARROWNESS IS THE DESIGN:

      SURFACES — the two wrap-authored texts this gate already reads: `GOOD-MORNING.md` and
      `_CHAIN.md`, and within each ONLY the ★ LATEST banner region (`_latest_banner_region`,
      the same slicer `roll_claim_check` uses). No other file, no other region.

      LINES — only lines whose START is the hand-off home `residual → #N:` (`_RESIDUAL_HOME_RE`).
      Prose is NOT scanned. This is the #77 finding applied unchanged: the authored-prose arm of
      the roll-claim check false-fired on RATIFIED text at its first live run, and was deleted
      rather than widened.

      CONTEXT — an owed phrase counts only inside ±`STALE_TOP_WINDOW` (160) characters of the
      cited id, i.e. the
      adjacent clause. Vocabulary: "top item" · "owed" · "next window" · "next session's top" ·
      "new top".

      USE vs MENTION — a window that ALSO carries an unnegated `enacted` is a HISTORY/EVIDENCE
      citation ("enacted per s142-D1", "CONSUMED: … the wave was enacted at #143"), not an owed
      claim, and is EXEMPT — declared in a note, never silently. `RULED-NOT-ENACTED` and
      `unenacted` are not enactment citations and do not exempt.

      REPORTED, NOT PRESCRIBED — a fail quotes the claiming line and the store's status
      VERBATIM and says nothing about which of the two is wrong; that is the session's call.
    """
    fails, notes = [], []
    statuses, err = _rulings_status_map(repo)
    if statuses is None:
        notes.append(f"stale-top-item fence: `knowledge/_rulings.json` UNREADABLE ({err}) — "
                     f"the fence is UNMEASURED this wrap. That is NOT the same as 'no owed "
                     f"claim is contradicted'.")
        return fails, notes

    scanned = 0
    for fname in ("GOOD-MORNING.md", OUT_CHAIN):
        path = os.path.join(repo, fname)
        if not os.path.exists(path):
            notes.append(f"stale-top-item fence: {fname} missing — UNMEASURED, not assumed clean.")
            continue
        with open(path, encoding="utf-8") as f:
            region = _latest_banner_region(f.read())
        if region is None:
            notes.append(f"stale-top-item fence: {fname} has no ★ LATEST banner — UNMEASURED "
                         f"(a different check already fails the wrap for that state).")
            continue
        for ln in region.splitlines():
            if not _RESIDUAL_HOME_RE.match(ln):
                continue
            scanned += 1
            for m in _RULING_ID_RE.finditer(ln):
                rid = m.group(0)
                win = ln[max(0, m.start() - STALE_TOP_WINDOW):m.end() + STALE_TOP_WINDOW]
                trips = [r.pattern for r in _OWED_CONTEXT_RES if r.search(win)]
                if not trips:
                    continue
                if _asserts_enacted(win):
                    notes.append(f"stale-top-item fence: {fname} residual line cites {rid} in an "
                                 f"owed-shaped context ({', '.join(trips)}) but the SAME clause "
                                 f"cites its enactment — read as HISTORY/EVIDENCE, EXEMPT by "
                                 f"scope. Clause: …{win.strip()}…")
                    continue
                status = statuses.get(rid)
                if status is None:
                    notes.append(f"stale-top-item fence: {fname} residual line claims owed work "
                                 f"for {rid}, which is NOT IN `_rulings.json` — UNMEASURED for "
                                 f"that id, not cleared. Clause: …{win.strip()}…")
                    continue
                if _asserts_enacted(status):
                    fails.append(
                        f"stale-top-item fence ({fname}, s161-D4): the wrap certifies OWED work "
                        f"for {rid} — matched {', '.join(trips)} — but the store says it is "
                        f"ENACTED. CLAIM (verbatim): \"{ln.strip()[:400]}\" — STORE (verbatim, "
                        f"`knowledge/_rulings.json` § {rid} .status): \"{status[:400]}\". One of "
                        f"the two is stale; this gate does not say which.")
    notes.append(f"stale-top-item fence (s161-D4): {scanned} `residual → #N` line(s) scanned "
                 f"across GOOD-MORNING.md + {OUT_CHAIN} ★ LATEST banners, id pattern "
                 f"`s\\d+-D\\d+`, context ±{STALE_TOP_WINDOW} chars — {len(fails)} fail(s).")
    return fails, notes


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


# ★ #244 — THE MECHANISED `MEMORY.md` CAP, carried unbuilt from #242 and #243.
# Lane F measured the pre-stub auto-memory index at 3,569 cl100k tape — the largest line of OURS
# in a 70,710 boot — and `s243-D1` cut it to a stub. Nothing then stopped it regrowing, one hook
# at a time, invisibly. `knowledge/_memory_cap_check.py` grades it; this is its wrap consumer, so
# it is not a zombie instrument [[instrument-without-a-consumer]].
#
# ⛔ ADVISORY AT BIRTH. It appends to WARNS, never to FAILS. The tier lives at the one line below
# and promotion to BLOCKING is DAVE'S WORD (the #111/#161/#163 pattern: warn, ratify, then flip).
# ⚠ AND IT MUST STAY ADVISORY UNTIL THE ENV QUESTION IS ANSWERED: the file graded LIVES OUTSIDE
# THE REPO (a Cowork mount), so on any tree that is not a live Cowork session there is nothing to
# measure. A blocking check that cannot pass in one environment is the trap this repo already
# named [[gate-cannot-pass-in-one-environment]] — so absence here is a DECLARED NOTE, never a
# warn and never a fail, and the check is honest that it did not run.
MEMORY_CAP_BLOCKING = False


def memory_cap_check(repo):
    """★ #244 — the auto-memory index must stay under its derived cap. Returns (warns, notes).

    ⚠ UNIT: cl100k TAPE throughout [[measure-dont-convert-units]]. Never converted to real,
    never summed with a `message.usage` figure. The cap and its provenance live in
    `_memory_cap_check.py` (MEMORY_CAP_TAPE, derived #244 from a measured base) — ONE
    implementation, imported, never a second copy here (the mover≠gate lesson).
    """
    warns, notes = [], []
    sys.path.insert(0, HERE)
    try:
        import _memory_cap_check as mcc
    except Exception as e:
        return [f"memory-cap: `knowledge/_memory_cap_check.py` unimportable ({e}) — the check "
                f"cannot run; fix it, never close blind"], notes
    path, how = mcc.resolve_path()
    if path is None:
        # DECLARED, not zeroed, and not a warn: there is genuinely no index on this tree.
        notes.append(f"memory-cap: DID NOT RUN — {how}. This is UNKNOWN, not a pass: the "
                     f"auto-memory index is a Cowork surface outside this repo.")
        return warns, notes
    try:
        m = mcc.measure(path)
    except Exception as e:
        return [f"memory-cap: {path} unreadable ({e}) — declared, never graded 0"], notes
    over, line = mcc.grade(m)
    if over:
        warns.append(f"memory-cap ({'BLOCKING' if MEMORY_CAP_BLOCKING else 'ADVISORY'}): {line}")
    else:
        notes.append(f"memory-cap: {line} ({how}; cap provenance: {mcc.CAP_PROVENANCE})")
    return warns, notes


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


def dofirst_index_present_check(repo):
    """★ #61 — every open DO-FIRST item must be NAMED in the generated `_CHAIN.md`.

    The defect this exists for, in Dave's words at the #61 opener: *#60 left DO-FIRST items 9–12
    outside the read chain.* They were real, open, and a cold session had no way to learn they
    existed. **That is a PRESENCE defect** — [[gate-inside-the-growth-loop]]: gate the PRESENCE,
    not the drift.

    ⚠ THIS IS THE CONSUMER FOR THE DECLARED GAP. `chain_parts` deliberately does NOT refuse when
    the index cannot be built — refusing over-couples the chain and broke four M10 bites when it
    was tried. It emits a loud UNAVAILABLE line instead. **A declared gap that nothing ever reads
    is just a quieter silence** ([[instrument-without-a-consumer]]), so the assertion lives here,
    on the live tree, where a fixture cannot be hurt by it.

    ⚠ SCOPE, STATED SO IT IS NOT OVERSOLD. This asserts every item is NAMED in the chain file on
    disk. It does NOT close chain STALENESS — `_build_all.py:184-186` still writes then checks
    (#60's ⛔ finding), so a chain regenerated and then verified in the same breath proves only
    that the generator is deterministic. What this catches is an item that reaches GOOD-MORNING.md
    and never reaches the chain at all, which is precisely the #60 shape.
    """
    fails, notes = [], []
    gm_path, chain_path = os.path.join(repo, "GOOD-MORNING.md"), os.path.join(repo, OUT_CHAIN)
    if not os.path.exists(gm_path) or not os.path.exists(chain_path):
        return fails, notes
    with open(gm_path, encoding="utf-8") as f:
        gm_lines = f.read().splitlines()
    idx, how = dofirst_index(gm_lines)
    if idx is None:
        return [f"dofirst-index: the presence index could not be built, so the read chain does "
                f"NOT represent the open worklist — {how}"], notes
    with open(chain_path, encoding="utf-8") as f:
        chain = f.read()
    # ⚠ Assert each item INDIVIDUALLY and QUOTE the missing ones. A bare count would be the very
    # error this corpus keeps re-learning: a count is not a measurement, and "14 items" tells you
    # nothing about WHICH one fell out ([[measure-dont-convert-units]]).
    nums = [m.group(1) for m in (DOFIRST_ITEM_RE.match(l) for l in gm_lines) if m]
    missing = [n for n in nums if f"`{n}` " not in chain]
    if missing:
        fails.append(f"dofirst-index: {len(missing)} open DO-FIRST item(s) are in GOOD-MORNING.md "
                     f"but NOT named in {OUT_CHAIN} — {', '.join(missing)}. A cold session reading "
                     f"the chain cannot learn they exist. Run `python3 knowledge/_gen_chain.py` "
                     f"and stage the result. (This is the #60 defect: items 9-12, silently absent.)")
    else:
        notes.append(f"dofirst-index: all {len(nums)} open DO-FIRST items are named in {OUT_CHAIN} "
                     f"({how}) — presence gated, staleness NOT (see docstring).")
    return fails, notes


# ⛔ #241 — `BOOT_DRIFT_WINDOW = 6` IS GONE. The window is no longer this module's to pick: it is
# `s240-D1`'s n, and it lives beside the band it defines (`_gauge_tokens.BOOT_BAND_WINDOW = 7`),
# read at check time. A second copy here is the copy-chain class the ruling exists to end.
# ★ #241 — THE CEILING'S REGIME BOUNDARY, and it is DECLARED rather than smuggled.
# `s240-D2` defines the ceiling as the first measured boot AFTER the #240 roster diet and
# `s241-D1` fixes its value at 70,000 from that boot (69,092 at #241). Every reading in this log
# from #240 and earlier is PRE-DIET — a different regime, the #111-D2 clause ("don't fit a
# constant across a structural break") applied in the other direction. Grading those against a
# post-diet ceiling would paint the log red for a condition that no longer exists, so they are
# NOT graded against it — and they are NAMED in a note rather than silently skipped.
BOOT_CEILING_FROM_SESSION = 241

# ★★ #111-D1 (Dave) — THE LEGAL DECLARED-AND-PROCEED FORM.
# Dave, #111, on being asked warn-vs-block: *"Keep it BLOCKING, but the gate as built has
# no legal discharge — that's the defect, not the tier … That way the gate bites SILENCE,
# not reality, which is the asymmetry this repo already runs on: a declared gap passes, a
# silent one fails. As built it bites reality, so it traps a session that has done nothing
# wrong and can't legally proceed. No session should ever be blocked with no honest way
# forward."*
#
# ⚠ THE DECLARATION CANNOT LAUNDER. It discharges ONLY if the mean, constant, error bar
# and delta it states MATCH what this gate independently computes. A declaration carrying
# different numbers is a WORSE failure than no declaration at all — that is a session
# writing itself a pass — and it is failed separately and louder below.
# ⚠ IT ALSO CANNOT GO STALE. It is matched against the CURRENT computation, so last
# session's declaration cannot discharge this session's drift [[read-chain-is-where-staleness-is-free]].
# ⛔ #241 — THE LEGACY FORM. It names a `constant` that NO LONGER EXISTS (`s240-D1` retired
# `BOOT_FIRSTTURN_TK`), so it can no longer discharge anything. It is kept, and kept MATCHING,
# for exactly one reason: the ~30 lines already written in this shape across notes/_GAUGE-LOG.md
# are RATIFIED RECORD. A parser that stopped recognising them would read them as MISMATCHED
# declarations and fail the gate until a session re-stamped history to suit the new code — the
# one outcome this log's whole discipline forbids. They are recognised, reported as HISTORY,
# and never re-stamped [[read-chain-is-where-staleness-is-free]].
BOOT_DRIFT_LEGACY_RE = re.compile(
    r"boot-drift\s+DECLARED\s+#(?P<sess>\d+)"
    r".{0,40}?mean\s+(?P<mean>[\d,]+)"
    r".{0,60}?constant\s+(?P<const>[\d,]+)\s*(?:±|\+/-)\s*(?P<err>[\d,]+)"
    r".{0,60}?delta\s+(?P<delta>[+-]?[\d,]+)"
    r".{0,200}?refresh\s+PUT\s+TO\s+DAVE",
    re.I | re.S)

# ★★ #241 — THE LIVE FORM, RE-POINTED AT THE DERIVED BAND (`s240-D1`).
# It states what the gate now computes: the NEWEST reading, the band DERIVED from the last n
# sessions, the delta between them, and the shrink-only CEILING it was also graded against.
# ⚠ It carries no `constant` and asks for no `refresh` — there is nothing left to re-base, which
# is the entire point of `s240-D1`. What it still does is the #111-D1 asymmetry, unchanged: a
# DECLARED gap passes, a SILENT one fails, and a declaration whose figures do not match this
# gate's own computation fails LOUDER than no declaration at all.
BOOT_DRIFT_DECL_RE = re.compile(
    r"boot-drift\s+DECLARED\s+#(?P<sess>\d+)"
    r".{0,60}?newest\s+(?P<newest>[\d,]+)"
    r".{0,80}?derived\s+band\s+(?P<mean>[\d,]+)\s*(?:±|\+/-)\s*(?P<err>[\d,]+)"
    r".{0,40}?n\s*=\s*(?P<n>\d+)"
    r".{0,80}?delta\s+(?P<delta>[+-]?[\d,]+)"
    r".{0,80}?ceiling\s+(?P<ceiling>[\d,]+)",
    re.I | re.S)

BOOT_DRIFT_LEGAL_FORM = (
    "> **boot-drift DECLARED #<N> (<YYYY-MM-DD>):** newest <R> · derived band <M> ±<S> "
    "(n=<n>, #<first>–#<last>) · delta <+/-D> · ceiling <C> · DERIVED at check time per "
    "`s240-D1`; NOT a re-base and no constant was edited.")


def _parse_boot_drift_declarations(text):
    """Every LIVE (derived-band) declared-drift entry in the gauge log, as dicts. Never raises."""
    out = []
    for m in BOOT_DRIFT_DECL_RE.finditer(text):
        try:
            out.append({k: int(m.group(k).replace(",", "").replace("+", ""))
                        for k in ("sess", "newest", "mean", "err", "n", "delta", "ceiling")})
        except (ValueError, AttributeError):
            continue
    return out


def _parse_legacy_boot_declarations(text):
    """Every PRE-`s240-D1` declared-drift entry — reported as history, never graded."""
    out = []
    for m in BOOT_DRIFT_LEGACY_RE.finditer(text):
        try:
            out.append({k: int(m.group(k).replace(",", "").replace("+", ""))
                        for k in ("sess", "mean", "const", "err", "delta")})
        except (ValueError, AttributeError):
            continue
    return out


# ★★ #218 — A DELTA BESIDE `boot` IS NOT A READING, AND UNTIL NOW NOTHING SAID SO.
#
# THE CLASS: this parser reads "a number near the word boot" as A MEASUREMENT OF BOOT. The gauge
# log's own prose is full of numbers that sit beside `boot` and are NOT boot — they are the
# DRIFT: "boot drift of 8,942" (#218), "declared boot … 2,345 over the band" (#215). Two failure
# modes, and the quiet one is the worse one:
#   · a SMALL delta (`boot 2,345 over the band`) lands outside the 10,000–200,000 sanity range
#     and is REFUSED — which fails the whole gate, loudly, on a line that was perfectly honest;
#   · a LARGE delta (`boot 12,345 over the band`) lands INSIDE the range and is counted as a
#     BOOT SAMPLE. The band is then computed off a number that was never a boot, and reads GREEN.
# ⛔ THE REMEDY UNTIL NOW WAS PROSE DISCIPLINE — #218's own wrap brief instructed the wrap sub to
# "phrase as 'boot drift of 8,942'" to dodge the parser, and `_CHAIN.md` carries that as the
# #215 pothole AVOIDED, NOT FIXED. A rule that lives in a brief is a rule that dies with it.
# ⇒ The distinction is now IN THE PARSER, in three named shapes, and deltas are RETURNED rather
# than dropped: an unmatched line is not an absence, and neither is a silently skipped one.
# ⚠ SCOPE, HONESTLY: the reading regex itself is UNCHANGED. Widening what counts as a reading
# would move the live drift window — a band-adjacent effect, and the band is Dave's.
BOOT_DELTA_WORD_RE = re.compile(
    r"\bboot[\s\-]*(?:drift|delta)\b\s*(?:of\s+)?([+-]?[\d,]*\d)", re.I)
# A SIGNED number beside boot is never a reading — a boot is a quantity, not a movement.
BOOT_SIGNED_RE = re.compile(r"\bboot\b\s*(?:#\d+\s*=\s*)?([+-][\d,]*\d)", re.I)
# …and the qualifier AFTER the number that turns it into a comparison against the band.
# ⚠ `vs` and `against` are deliberately NOT here: "#112 boot 55,025 vs #111 55,733" is two
# READINGS compared, a shape live in this log — the list is the specification, measured on it.
#
# ✅ #219 — THE QUIET HALF WAS STILL OPEN FOR VOCABULARY OUTSIDE THE LIST, AND IT WAS MEASURED.
# Driven against the parser at #219: `boot 12,345 higher than the band`, `boot 12,345 more than
# the constant` and `boot 12,345 away from the band` ALL came back as READINGS — i.e. the exact
# #218 failure mode (a delta entering the band's sample set and reading green), reached by three
# ordinary English phrasings the list did not name. The comparative forms are added below.
# ⛔ THE ADDITIONS ARE TIGHT ON PURPOSE, AND THAT IS THE WHOLE DESIGN. `higher/lower/more/less`
# only count when `than` follows, and `away` only when `from` follows, because a BARE preposition
# after a reading is ordinary prose about a real boot — `boot 55,025 from the first turn` is a
# READING, and a loose `from` in this list would eat it. That control is asserted in the selftest.
# ⚠ MEASURED NO-OP ON THE LIVE WINDOW, which is why this is not a band move: against the whole of
# `notes/_GAUGE-LOG.md` the reading count is 73 BEFORE and 73 AFTER, 0 readings reclassified. It
# hardens the shape the parser will meet NEXT; it does not re-price anything Dave has ruled.
BOOT_DELTA_TAIL_RE = re.compile(
    r"^[\s*_`,)\]]*(?:over|under|above|below|outside|out\s+of|past|beyond|off"
    r"|(?:higher|lower|more|less)\s+than|away\s+from|adrift)\b", re.I)

# ★★ #241 — A STRAY `#N` LATER IN THE LINE IS NOT THE READING'S SESSION, AND UNTIL NOW IT WAS.
#
# THE CLASS: the ordinal was taken as `re.search(r"#(\d+)", line)` — the FIRST `#N` ANYWHERE in
# the line, whether it labelled the reading or merely cited a ruling, another session, or a
# worklist row. Two ways that bites, and #240's own declaration recorded BOTH live:
#   · #239's `PREMISES WERE CHECKED` line restates its own boot (75,619) and cites `#238` in a
#     later clause ⇒ the reading was filed under 238, OVERWRITING #238's real 75,336 and putting
#     #239's ONE reading into the window TWICE. Declared at notes/_GAUGE-LOG.md's #240 line.
#   · eleven `Context gauge at authoring:` lines restate their own session's boot and cite
#     `#56-D1` (the UNIT ruling) ⇒ all eleven filed under session 56, one clobbering the next.
# ⇒ THE ORDINAL NOW COMES FROM LABEL POSITION OR FROM THE ENCLOSING STRATUM, never from a
# citation buried in prose. A `#N` counts as the label only if it sits in the line's opening
# 60 characters AND before the boot figure it is supposed to label — which is exactly where
# every reading shape in this log carries it (`**pre-flight #100 …:** boot …`,
# `**post-mortem #239:** … boot …`, `> boot #95 = 65,657 real`). Otherwise the reading belongs
# to the `#### <date> #N` stratum it is written inside, which is the honest default: a session's
# own block is where a session's own boot is recorded.
# ⚠ MEASURED DIFF ON THE LIVE LOG, not asserted: 105 readings parsed BEFORE and AFTER, 0 gained,
# 0 lost, 14 re-attributed — the #239 line, the eleven `Context gauge` restatements, one #125
# line and one unlabelled `**pre-flight:**` that had been filed under the -1 bucket. The window
# the band is computed over changes by exactly one member: #238 gets its own 75,336 back.
BOOT_STRATUM_RE = re.compile(r"^#{2,6}\s+\d{4}-\d{2}-\d{2}\s+#(\d+)\s*$")
BOOT_LABEL_ORD_MAXCOL = 60     # how far into a line a `#N` may sit and still be its LABEL


def _parse_boot_samples(text):
    """Pull boot samples out of the gauge log. Returns (good, refused, deltas).

    `good`   — [(session, real-tokens)], the readings.
    `refused`— lines that look like a boot reading and do NOT parse (never skipped).
    `deltas` — [(line, number)] recognised as DRIFT, not boot: reported, never counted.

    Line-based on purpose. The log records boot in at least four shapes across its
    history (`boot #95 = 65,657 real`, `pre-flight #100 ...: boot 64,940 real`,
    `boot 64,892 (disk ...`, `boot 65,041 real (n=12;`) and a single clever regex
    over the whole file silently drops the shapes it did not anticipate. Anything
    that looks like a boot line but does not parse is returned as REFUSED, never
    skipped — an unmatched line here is not an absence [[unmatched-grep-is-not-an-absence]].
    """
    # ⛔ FIXED #129, and it is the same class the docstring above is about. The match was
    # CASE-SENSITIVE, and the post-mortem lines since #125 begin the sentence with the word:
    # "**Boot 53,681 real**". Those lines did not parse, did not refuse, and were not counted —
    # they were INVISIBLE, which is the one outcome the refused/good split exists to prevent.
    # Three consecutive sessions of evidence (#125, #126) sat in the log unread by the gate that
    # grades the constant they disagree with. An unmatched grep is not an absence
    # [[unmatched-grep-is-not-an-absence]]. Fix is the flag, not a second regex.
    rows, refused, deltas = _parse_boot_rows(text)
    return [(r["session"], r["tk"]) for r in rows], refused, deltas


def _parse_boot_rows(text):
    """The same walk as `_parse_boot_samples`, with the PROVENANCE kept.

    Returns `(rows, refused, deltas)` where each row is
    `{session, tk, stratum, lineno, line}`. ONE implementation, two views — `s241-D2` needed to
    know WHICH LINES produced a reading and a second walk here would be a second answer to the
    same question, which is the drift class this file refuses everywhere else.
    """
    rows, refused, deltas = [], [], []
    stratum = None                     # the `#### <date> #N` block currently being read (#241)

    def _num(s):
        return int(s.replace(",", "").replace("+", ""))

    for _no, ln in enumerate(text.splitlines(), 1):
        h = BOOT_STRATUM_RE.match(ln.strip())
        if h:
            stratum = int(h.group(1))
            continue
        if "boot" not in ln.lower():
            continue
        line_deltas = []
        # ---- SHAPE 1: `boot drift/delta of N` — named as a movement by the prose itself.
        for dm in BOOT_DELTA_WORD_RE.finditer(ln):
            line_deltas.append((ln.strip()[:110], _num(dm.group(1))))
        # ---- SHAPE 2: `boot +N` / `boot -N` — a sign makes it a movement whatever it says.
        for sm_ in BOOT_SIGNED_RE.finditer(ln):
            line_deltas.append((ln.strip()[:110], _num(sm_.group(1))))
        m = re.search(r"\bboot\b\s*(?:#\d+\s*=\s*)?([1-9][\d,]{4,})", ln, re.I)
        if not m:
            # A line mentioning boot with no number is prose, not a refusal — and a line whose
            # only number was one of the delta shapes above is ACCOUNTED FOR, not refused.
            if re.search(r"\bboot\b\s*(?:#\d+\s*=\s*)?\d", ln, re.I) and not line_deltas:
                refused.append(ln.strip()[:110])
            deltas += line_deltas
            continue
        # ---- SHAPE 3: `boot N over/under/outside the band` — the number is a comparison, and
        # this is the shape #215 had to WRITE AROUND and #218 was briefed to avoid.
        deltas += line_deltas
        if BOOT_DELTA_TAIL_RE.match(ln[m.end():]):
            deltas.append((ln.strip()[:110], _num(m.group(1))))
            continue
        try:
            tk = int(m.group(1).replace(",", ""))
        except ValueError:
            refused.append(ln.strip()[:110])
            continue
        if not (10_000 <= tk <= 200_000):
            refused.append(ln.strip()[:110])
            continue
        # ★ #241 — LABEL POSITION, THEN STRATUM, NEVER A CITATION. See BOOT_STRATUM_RE above.
        sm = re.search(r"#(\d+)", ln)
        if sm and sm.start() < BOOT_LABEL_ORD_MAXCOL and sm.start() < m.start(1):
            sess = int(sm.group(1))
        else:
            sess = stratum if stratum is not None else -1
        rows.append({"session": sess, "tk": tk, "stratum": stratum,
                     "lineno": _no, "line": ln.strip()[:110]})
    return rows, refused, deltas


# ★★ `s241-D2` — ONE STRATUM, ONE FIRST-TURN FIGURE (S5 of the #241 ritual diet).
#
# THE DEFECT, IN #240's OWN WORDS AND ITS OWN BLOCK: a session stratum that states its
# first-turn figure TWICE puts ONE reading into the band's window TWICE and pushes a real
# session's reading out of it. `derived_boot_band()` already dedupes at the READER (first
# reading per ordinal wins) — that is a shield, and a shield is not a fix: the log still says
# two different things about one boot, and the next consumer to walk it without the dedupe
# inherits the whole defect. THIS is the fix at the SOURCE: a stratum that says it twice fails
# LOUD, by session number, with both lines quoted.
#
# ⛔ EFFECTIVE FROM `BOOT_DOUBLE_COUNT_FROM_SESSION`, AND THE REASON IS MEASURED, NOT TIMID:
# 18 session ordinals in the live `notes/_GAUGE-LOG.md` already carry more than one reading
# (110, 113, 118, 127, 169, 173, 174, 216-223, 225, 226, 239 — probe:
# `Counter(s for s, _ in _parse_boot_samples(log)[0])`). A retroactive fail could never pass in
# this repo, and a gate that cannot pass is a gate that gets routed around
# [[gate-cannot-pass-in-one-environment]]. History is reported as a NOTE with its count; the
# rule binds the strata written from #241 on, which are the ones anyone can still write
# correctly. Same shape and same reason as `BOOT_CEILING_FROM_SESSION`.
BOOT_DOUBLE_COUNT_FROM_SESSION = 241       # `s241-D2` — first stratum bound by the rule


def boot_stratum_double_count_check(repo):
    """(fails, notes) — a session may state its boot figure ONCE in notes/_GAUGE-LOG.md."""
    fails, notes = [], []
    log = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    if not os.path.exists(log):
        return fails, notes          # boot_constant_drift_check already fails loud on absence
    with open(log, encoding="utf-8") as f:
        rows, _refused, _deltas = _parse_boot_rows(f.read())
    by_session = {}
    for r in rows:
        by_session.setdefault(r["session"], []).append(r)
    dupes = {k: v for k, v in by_session.items() if len(v) > 1}
    bound = {k: v for k, v in dupes.items() if k >= BOOT_DOUBLE_COUNT_FROM_SESSION}
    legacy = sorted(k for k in dupes if k < BOOT_DOUBLE_COUNT_FROM_SESSION)
    for sess in sorted(bound):
        rs = bound[sess]
        fails.append(
            "boot double-count: session #%d states a first-turn figure %d times in "
            "notes/_GAUGE-LOG.md (`s241-D2`: ONCE, in the `post-mortem #N:` line). One reading "
            "counted twice displaces a real session from the derived band's window — %s. "
            "Delete the restatement, or move the figure OUT of the boot vocabulary if it is a "
            "comparison rather than a reading."
            % (sess, len(rs),
               " · ".join("line %d “%s…”" % (r["lineno"], r["line"][:70]) for r in rs)))
    if legacy:
        notes.append(
            "boot double-count: %d PRE-RULE session ordinal(s) carry more than one reading "
            "(#%s) and are NOT graded — `s241-D2` binds strata from #%d. They are held harmless "
            "by `derived_boot_band()`'s one-reading-per-ordinal dedupe, which is a shield, not a "
            "repair: the log still says two things about one boot."
            % (len(legacy), ", #".join(str(x) for x in legacy),
               BOOT_DOUBLE_COUNT_FROM_SESSION))
    return fails, notes


def boot_constant_drift_check(repo):
    """★ #110-D3 — THE PUBLISHED BOOT CONSTANT MUST STILL MATCH WHAT IS MEASURED.

    #109 found `_gauge_tokens.py` publishing a boot floor of 30,499 against a real
    75,899 — wrong by 45,400, roughly half the stop line. Two defects fed it, and only
    one of them was a coding error. The other was that NOTHING EVER COMPARED THE
    CONSTANT TO THE MEASUREMENTS SITTING NEXT TO IT. The samples were in the gauge log
    the whole time. That is what this gate is: the comparison, made mechanically, every
    wrap.

    ✅ #129, 2026-08-08 — THE GATE DID ITS JOB AND THE ANSWER FINALLY CAME BACK. The 75,899
    above is HISTORY, not the current floor: `s129-D1` re-based `BOOT_FIRSTTURN_TK` to 54,859
    ±1,178 on seven post-break samples. (✅ #171: `s171-D1` re-based again to 56,158 ±849
    on the drifted post-#164 series — this gate fired the drift at #170 and Dave took the
    refresh at #171. This function reads the live constants; nothing here was tuned.)
    Nothing in this function was tuned to suit it; what
    WAS fixed is a blind spot found in the same pass — `_parse_boot_samples` matched
    case-sensitively and could not see "**Boot 53,681 real**", so three sessions of samples
    were invisible here. Both readings are in notes/_GAUGE-LOG.md #129.

    ⚠ It does NOT prescribe a value, widen a band, or edit the constant. It reports the
    measurement and names the drift [[gate-narrows-its-own-rule]]. Re-pricing the
    constant is a measurement someone must take and Dave must see — an agent quietly
    re-fitting the number it is being graded against is the gate marking its own
    homework [[check-after-its-own-remedy]].

    ✅ #241, `s240-D1`/`s240-D2`/`s241-D1` — THERE IS NO CONSTANT LEFT TO GRADE AGAINST, and
    that is the fix, not a loosening. This check now grades the NEWEST reading twice:
      · against the BAND DERIVED at check time from the last `BOOT_BAND_WINDOW` sessions'
        readings (mean ± sample spread) — a step change beyond the spread goes red, and slow
        drift never needs a re-base because there is no constant to re-base; and
      · against `BOOT_CEILING_TK`, the ONE typed number left — shrink-only, Dave's to move.
        The ceiling is graded per READING, not against a mean: one boot over it fails by name.
    The #111-D1 legal discharge is unchanged in principle and re-pointed in wording: a DECLARED
    gap passes, a SILENT one fails, and a declaration that mis-states the figures fails louder
    than none. Fails LOUD and NAMED if the log cannot be parsed — a crash is not a fail
    [[a-crash-is-not-a-fail]], and neither is a silent zero-sample pass.
    """
    fails, notes = [], []
    log = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    if not os.path.exists(log):
        fails.append("boot-drift: notes/_GAUGE-LOG.md is MISSING — the boot band is DERIVED "
                     "from that file (`s240-D1`), so with it absent there is no band and "
                     "nothing to check. This is the #109 condition (a rule with no "
                     "consumer), not a clean pass.")
        return fails, notes
    try:
        sys.path.insert(0, HERE)
        import _gauge_tokens as gt
        ceiling, window, sigma = gt.BOOT_CEILING_TK, gt.BOOT_BAND_WINDOW, gt.BOOT_BAND_SIGMA
        derive = gt.derived_boot_band
    except Exception as e:
        fails.append(f"boot-drift: cannot read BOOT_CEILING_TK / BOOT_BAND_WINDOW / "
                     f"BOOT_BAND_SIGMA / derived_boot_band from _gauge_tokens.py ({e}) — the "
                     f"ruled ceiling and the band's window are UNREADABLE, so they are also "
                     f"unverifiable. Fix, never close blind.")
        return fails, notes

    with open(log, encoding="utf-8") as f:
        samples, refused, deltas = _parse_boot_samples(f.read())
    if deltas:
        # ★ #218 — NEVER SILENT. A recognised delta is a number this gate deliberately did NOT
        # count; saying so is what stops the next reader re-deriving the pothole from scratch.
        notes.append("boot-drift: %d line(s) state a DRIFT beside `boot`, not a reading, and "
                     "were NOT counted as samples (#218 parser split) — e.g. %s"
                     % (len(deltas), " · ".join(f"{n:,} in “{ln[:60]}…”" for ln, n in deltas[:2])))
    if refused:
        fails.append("boot-drift: %d gauge-log line(s) look like boot readings but do "
                     "NOT parse — %s. The band would be computed off an incomplete "
                     "sample and read GREEN. Fix the parser or the line."
                     % (len(refused), " · ".join(refused[:2])))
        return fails, notes
    if len(samples) < 3:
        fails.append("boot-drift: only %d boot sample(s) found in notes/_GAUGE-LOG.md — "
                     "too few to derive a band from. DECLARED, not passed."
                     % len(samples))
        return fails, notes

    # ★ `s240-D1` — THE BAND IS DERIVED HERE, and by the ONE function that owns the arithmetic.
    # The dedupe (one reading per SESSION, never per line) lives in `derived_boot_band` with the
    # #240 finding it exists to kill; this gate does not re-implement it beside it.
    band = derive(samples, n=window)
    if band is None:
        fails.append(
            "boot-drift: fewer than n=%d SESSIONS carry a boot reading in "
            "notes/_GAUGE-LOG.md, so `s240-D1`'s band cannot be derived — %d reading(s) "
            "across %d session ordinal(s). DECLARED, not passed: a band that cannot be "
            "computed is not a band that passed."
            % (window, len(samples), len({s for s, _ in samples})))
        return fails, notes
    mean, spread, reads, sessions = band
    newest, newest_sess = reads[-1], sessions[-1]
    delta = newest - mean

    red_line = sigma * spread
    notes.append(
        "boot-drift: DERIVED band %s ±%s (`s240-D1`, n=%d sessions #%d–#%d: %s) · newest "
        "#%d %s · delta %+d · red beyond ±%s (%g× the spread) · ceiling %s "
        "(`s241-D1`, shrink-only)"
        % (f"{mean:,.0f}", f"{spread:,.0f}", len(reads), sessions[0], sessions[-1],
           " · ".join(f"{s:,}" for s in reads), newest_sess, f"{newest:,}", delta,
           f"{red_line:,.0f}", sigma, f"{ceiling:,}"))

    # ---- ARM 1: THE CEILING. One typed number, graded per READING, LOUD and NAMED.
    over = [(s, tk) for s, tk in zip(sessions, reads)
            if s >= BOOT_CEILING_FROM_SESSION and tk > ceiling]
    pre = [(s, tk) for s, tk in zip(sessions, reads)
           if s < BOOT_CEILING_FROM_SESSION and tk > ceiling]
    if pre:
        notes.append(
            "boot-drift: %d reading(s) in the window sit above the ceiling but are PRE-DIET "
            "(session < #%d) and are NOT graded against it — %s. `s240-D2` sets the ceiling "
            "from the FIRST POST-DIET boot; grading the old regime by it would be fitting a "
            "constant across a structural break (#111-D2). Named, never silently skipped."
            % (len(pre), BOOT_CEILING_FROM_SESSION,
               " · ".join(f"#{s} {tk:,}" for s, tk in pre)))
    if over:
        fails.append(
            "boot-drift CEILING BREACH: `_gauge_tokens.BOOT_CEILING_TK` = %s and %d "
            "post-diet reading(s) EXCEED it — %s. ⛔ `s240-D2`/`s241-D1` make this number "
            "SHRINK-ONLY: boot may go DOWN past it and never up, and the remedy is to CUT "
            "THE BOOT, never to raise the literal. Raising it is Dave's word alone and is "
            "not a price a wrap may pay to unblock itself "
            "[[gate-must-quote-what-it-forbids]]."
            % (f"{ceiling:,}", len(over), " · ".join(f"#{s} {tk:,}" for s, tk in over)))

    # ---- ARM 2: THE DERIVED BAND. Step change out, slow drift in — see BOOT_BAND_SIGMA.
    if abs(delta) <= red_line:
        return fails, notes

    drift_msg = (
        "boot-drift: the newest boot reading (#%d, %s) sits %+d from the band DERIVED "
        "from the last n=%d sessions (%s ±%s) — past the %g× red line of ±%s, i.e. a STEP "
        "CHANGE rather than drift. Readings: %s."
        % (newest_sess, f"{newest:,}", delta, len(reads), f"{mean:,.0f}",
           f"{spread:,.0f}", sigma, f"{red_line:,.0f}",
           " · ".join(f"{s:,}" for s in reads)))

    # ★ #111-D1 — is the step DECLARED? Silence fails; an honest declaration passes.
    with open(log, encoding="utf-8") as f:
        log_text = f.read()
    decls = _parse_boot_drift_declarations(log_text)
    legacy = _parse_legacy_boot_declarations(log_text)
    matched = [d for d in decls
               if d["ceiling"] == ceiling and d["n"] == len(reads)
               and abs(d["newest"] - newest) <= 1 and abs(d["mean"] - mean) <= 1
               and abs(d["err"] - spread) <= 1 and abs(d["delta"] - delta) <= 1]
    mismatched = [d for d in decls if d not in matched]
    if legacy:
        notes.append(
            "boot-drift: %d PRE-`s240-D1` declaration(s) in the log state a `constant` that "
            "no longer exists (newest #%d). They are RATIFIED RECORD, are read as HISTORY, "
            "and are NOT re-stamped to suit this code — the gate does not rewrite the log "
            "it grades [[read-chain-is-where-staleness-is-free]]."
            % (len(legacy), legacy[-1]["sess"]))

    if matched:
        d = matched[-1]
        notes.append(
            "%s ✅ DECLARED at #%d and DISCHARGED (#111-D1): the declaration states the "
            "same newest reading, derived band, window, delta and ceiling this gate "
            "computed. The step is real and is NOT hidden — that is the whole bar."
            % (drift_msg, d["sess"]))
    elif mismatched:
        d = mismatched[-1]
        fails.append(
            "%s ⛔ A boot-drift declaration EXISTS (#%d) but its numbers do NOT match this "
            "gate's computation — it states newest %s / band %s ±%s (n=%d) / delta %+d / "
            "ceiling %s against a computed newest %s / band %s ±%s (n=%d) / delta %+d / "
            "ceiling %s. A declaration that mis-states the step is worse than none: it is "
            "a session writing itself a pass. Correct the FIGURES — the band is derived, "
            "so there is nothing to widen and nothing to re-base "
            "[[gate-must-quote-what-it-forbids]]."
            % (drift_msg, d["sess"], f"{d['newest']:,}", f"{d['mean']:,}", f"{d['err']:,}",
               d["n"], d["delta"], f"{d['ceiling']:,}", f"{newest:,}", f"{mean:,.0f}",
               f"{spread:,.0f}", len(reads), delta, f"{ceiling:,}"))
    else:
        fails.append(
            "%s ⛔ AND IT IS UNDECLARED.\n"
            "    ★ #111-D1 (Dave) — THERE IS A LEGAL WAY FORWARD AND THIS GATE OWES IT TO "
            "YOU. You are not required to explain the step to close your wrap; you are "
            "required not to hide it. Add ONE line to notes/_GAUGE-LOG.md, exactly this "
            "shape:\n"
            "      %s\n"
            "    filled with the figures above: newest %s · derived band %s ±%s (n=%d, "
            "#%d–#%d) · delta %+d · ceiling %s. The declaration must MATCH what this gate "
            "computes — wrong figures fail louder than none. ⚠ And note what is NOT asked "
            "for any more: no re-base, no refresh put to Dave, no constant edited. "
            "`s240-D1` retired all three."
            % (drift_msg, BOOT_DRIFT_LEGAL_FORM, f"{newest:,}", f"{mean:,.0f}",
               f"{spread:,.0f}", len(reads), sessions[0], sessions[-1], delta,
               f"{ceiling:,}"))
    return fails, notes


def title_generation_check(repo):
    """#120 residual ⓪ (Dave, #119 post-wrap): both wrap-time titles must be MECHANISED, not
    hand-authored prose. `_gen_titles.py` derives RENAME (chat-only, RULED #28 — never written
    into GOOD-MORNING.md) and NEXT-TITLE (written to the GM header, already gated separately by
    TITLE_LINE_RE/TITLE_CAP_TAPE above). Because RENAME is never persisted to GOOD-MORNING.md by
    design, the ONLY witness that it was generated (rather than typed from memory) is the
    receipt `_gen_titles_receipt.json` that `_gen_titles.py` writes alongside its stdout print.
    This check asserts BOTH lines are present in that receipt, well-formed, and generated
    against the banner still on disk (not a stale receipt from a prior session's wrap).
    BLOCKING at birth — same posture as the wiring gate: an un-consulted witness is a witness
    that does not exist. Returns (fails, notes)."""
    fails, notes = [], []
    receipt_path = os.path.join(repo, "knowledge", "_gen_titles_receipt.json")
    if not os.path.exists(receipt_path):
        fails.append(
            "TITLE GENERATION: no `knowledge/_gen_titles_receipt.json` found — "
            "`python3 knowledge/_gen_titles.py --session <N>` was not run this wrap. RENAME "
            "and NEXT-TITLE must be MECHANISED (#120 residual ⓪), never hand-authored prose.")
        return fails, notes
    try:
        with open(receipt_path, encoding="utf-8") as f:
            receipt = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fails.append(f"TITLE GENERATION: `_gen_titles_receipt.json` unreadable "
                     f"({type(e).__name__}: {e}) — re-run `_gen_titles.py`.")
        return fails, notes

    rename = receipt.get("rename", "")
    next_title = receipt.get("next_title", "")
    if not rename or not rename.startswith("RENAME THIS SESSION →"):
        fails.append(f"TITLE GENERATION: receipt's `rename` line missing or malformed: {rename!r}")
    if not next_title or not next_title.startswith("NEXT SESSION TITLE →"):
        fails.append(f"TITLE GENERATION: receipt's `next_title` line missing or malformed: "
                     f"{next_title!r}")

    gm_path = os.path.join(repo, "GOOD-MORNING.md")
    if os.path.exists(gm_path):
        with open(gm_path, encoding="utf-8") as f:
            gm_text = f.read()
        m = re.search(r"^>\s*##\s*★\s*LATEST\s*—.*$", gm_text, re.M)
        if m:
            sm = re.search(r"\*\*#(\d+)\*\*", m.group(0))
            if sm:
                current_banner_session = int(sm.group(1))
                receipt_banner_session = receipt.get("meta", {}).get("banner_session")
                if receipt_banner_session != current_banner_session:
                    fails.append(
                        f"TITLE GENERATION: receipt was generated against banner #"
                        f"{receipt_banner_session}, but GOOD-MORNING.md's banner is now #"
                        f"{current_banner_session} — STALE receipt from an earlier wrap. "
                        f"Re-run `_gen_titles.py` after this session's own banner is written.")

    if not fails:
        notes.append(f"TITLE GENERATION: receipt present, both lines well-formed "
                     f"(RENAME session #{receipt.get('meta', {}).get('declared_session')}, "
                     f"NEXT-TITLE for #{receipt.get('meta', {}).get('next_session')}) — "
                     f"#120 residual ⓪.")
    return fails, notes


# ★ THE INSTRUMENT-STRAY GATE (#138, Dave's — "i just want a solid fix").
#
# THE CLASS, and it took two instances in two sessions to name it: AN INSTRUMENT WRITING INTO THE
# TREE IT MEASURES. First instance `s137-D1` — the verification instruments append to
# `notes/_REHEARSAL-LOG.jsonl`, so verifying a commit dirtied the tree and refused the very push
# the ruling exists to allow. Second instance #138 — `FONTCONFIG_FILE`'s `<dir>` pointed at
# `knowledge/assets/fonts/_desktop/TTF/` (#136's ENOSPC fix), so every render run left `.uuid`,
# `.uuid.LCK` and `.uuid.TMP-XXXXXX` behind, untracked.
#
# ⚠ WHY THIS LIVES AT THE WRAP SEAM AND NOT IN `_build_all.py`. Until now the ONLY thing that
# caught a stray was the `--push` clean-tree assertion, which fires at the last possible moment,
# after the work, and now carries an exclusion list that can widen. The obvious home — the build
# selftest — is SANDBOX-IMPOSSIBLE (~49 s against the ~45 s call kill), which is exactly how
# `--selftest` sat RED for three consecutive wraps [[instrument-without-a-consumer]]. A gate that
# does not run in the mode the work happens in cannot fail, and a green that cannot fail is an
# assertion. This runs every wrap and every rehearsal.
#
# ⚠ TWO PASSES, AND THE SECOND ONE IS THE POINT. Pass 1 respects `.gitignore` — MEASURED #138:
# `knowledge/assets` carries 60 untracked-but-ignored paths (`.DS_Store`, the unlicensed Helvetica
# Armenian webfonts), so a gate that ignored `.gitignore` wholesale would fire on every single
# wrap, and noise is how a gate gets switched off. Pass 2 then re-checks the SAME dirs WITHOUT
# `--exclude-standard`, filtered to instrument signatures only, so adding `.uuid*` to a
# `.gitignore` CANNOT blind this gate. Dave refused an ignore rule at #137 on the grounds that it
# hides an instrument still writing where it must not; pass 2 makes that refusal structural
# instead of remembered. ★ A gate must quote what it forbids — the signatures are named below.
#
# SCOPE, STATED HONESTLY: asset directories only — inputs that instruments READ and humans do not
# hand-author, so an untracked path there is an instrument's. It does NOT police the whole tree;
# untracked work-in-progress elsewhere is legitimate mid-session.
INSTRUMENT_READONLY_DIRS = ("knowledge/assets",)
# Basename prefixes an instrument leaves behind. `.uuid`, `.uuid.LCK`, `.uuid.TMP-XXXXXX` are
# fontconfig's directory-identity marker, its lock, and its atomic-write temp (#136 observed,
# #138 reproduced). Add a prefix here when a THIRD instrument is caught; do not widen to a
# wildcard — the list is the specification.
INSTRUMENT_SIGNATURES = (".uuid",)

# ★★ THE `s217-D1` RE-SCOPE (#218 gates wave) — THE PREMISE ABOVE AGED, AND THE RULE DID NOT.
#
# WHAT AGED: this gate keys on UNTRACKED, and its scope note argues untracked-under-assets ⇒
# instrument. `s217-D1` (#217) then made `knowledge/assets/photography-web/` a COMMITTED SURFACE
# — web-sized derivatives MINTED BY A NAMED GENERATOR and committed, while the 2.5 GB originals
# stay NON-REPO behind the #211 `.gitignore` fence. So a legitimate `--derivatives` run now
# produces exactly the shape this gate was built to forbid: at the #218 wrap it FAILED on **236
# untracked paths** and cleared only because they were staged. A gate that fires on ruled,
# correct work is a gate on its way to being switched off [[premise-ages-faster-than-rule]].
#
# ⛔ WHAT DID NOT CHANGE, AND MUST NOT: an instrument writing where it only reads is still a FAIL,
# INSIDE these directories too. The re-scope is not an exemption for a PATH — it is a
# recognition of a PRODUCT. Three things are graded separately below:
#   1. INSTRUMENT_SIGNATURES (`.uuid*`) — a FAIL anywhere, committed surface included. A
#      derivative directory is the easiest place for fontconfig to hide, not the hardest.
#   2. A basename matching the surface's own `product` pattern — a NOTE: unstaged output of the
#      named generator, destined for the commit the ruling requires. Never silent (the push
#      clean-tree assert will still meet it, and the note says so).
#   3. ANYTHING ELSE under the surface — still a FAIL. The pattern is the specification: a
#      stray `.DS_Store`, a temp file or a hand-dropped `.jpg` with no `-wNNN` size suffix is
#      NOT a product of `--derivatives` and is not licensed by `s217-D1`.
# ⚠ ADDING A DIRECTORY HERE IS A RULING-BACKED ACT, not a convenience: the entry must name the
# ruling that made the surface committed and the generator that mints it, and both are printed
# in the note, so a reader can check the licence without leaving the output.
COMMITTED_SURFACE_DIRS = {
    "knowledge/assets/photography-web": {
        # `<slug>-w<width>.<ext>` — the shape `_build_photo_manifest.py --derivatives` mints and
        # the shape `_PHOTOGRAPHY-MANIFEST.md`'s `derivative` column records.
        "product": re.compile(r"^[^/]+-w\d{2,5}\.(?:jpe?g|png|webp)$", re.I),
        "ruling": "s217-D1",
        "generator": "python3 knowledge/_build_photo_manifest.py --derivatives",
    },
}


def _sig_hit(path):
    return os.path.basename(path).startswith(INSTRUMENT_SIGNATURES)


def _committed_surface(path):
    """(dir, spec) if `path` sits under a ruled committed surface, else (None, None)."""
    for d, spec in COMMITTED_SURFACE_DIRS.items():
        if path == d or path.startswith(d.rstrip("/") + "/"):
            return d, spec
    return None, None


def _is_ruled_product(path):
    """True only for a basename matching its own surface's product pattern. An instrument
    signature is NEVER a product — rule 1 above outranks rule 2, in this order, on purpose."""
    if _sig_hit(path):
        return False
    _d, spec = _committed_surface(path)
    return bool(spec) and bool(spec["product"].match(os.path.basename(path)))


def instrument_stray_check(repo, dirs=INSTRUMENT_READONLY_DIRS):
    """Return (fails, warns, notes). Untracked paths under read-only asset dirs are FAILS,
    EXCEPT the ruled committed-surface products of COMMITTED_SURFACE_DIRS, which are NOTES.

    Pass 1: untracked and NOT ignored — anything that is not a ruled product is a stray.
    Pass 2: untracked INCLUDING ignored, filtered to INSTRUMENT_SIGNATURES — so a
    `.gitignore` entry cannot silence a known instrument, committed surface or not.

    Never raises: if git cannot be run the gate says so LOUD and NAMED rather than
    returning a green it did not measure [[feedback-measuring-tool-must-not-guess]].
    """
    fails, warns, notes = [], [], []
    for d in dirs:
        found, failed_to_run = [], False
        for args, keep in ((["--exclude-standard"], lambda p: True), ([], _sig_hit)):
            cmd = ["git", "ls-files", "--others"] + args + ["--", d]
            try:
                r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=20)
            except (OSError, subprocess.SubprocessError) as e:  # noqa: BLE001
                warns.append(f"⛔ INSTRUMENT-STRAY GATE DID NOT RUN for `{d}` "
                             f"({type(e).__name__}: {e}) — this is UNKNOWN, not clean. "
                             f"Run `git ls-files --others -- {d}` by hand before wrapping.")
                failed_to_run = True
                break
            if r.returncode != 0:
                warns.append(f"⛔ INSTRUMENT-STRAY GATE DID NOT RUN for `{d}` "
                             f"(git exit {r.returncode}: {r.stderr.strip()[:160]}) — UNKNOWN, "
                             f"not clean.")
                failed_to_run = True
                break
            found += [x for x in r.stdout.splitlines() if x.strip() and keep(x)]
        if failed_to_run:
            continue
        untracked = sorted(set(found))
        strays = [p for p in untracked if not _is_ruled_product(p)]
        products = [p for p in untracked if _is_ruled_product(p)]
        if strays:
            shown = ", ".join(f"`{s}`" for s in strays[:6])
            more = f" (+{len(strays) - 6} more)" if len(strays) > 6 else ""
            fails.append(
                f"INSTRUMENT STRAY: {len(strays)} untracked path(s) under `{d}` — {shown}{more}. "
                f"An instrument has written into a directory it only reads (#138 class; `.uuid*` "
                f"means fontconfig — its `<dir>` is pointed at the repo instead of the /var/tmp "
                f"symlink farm, see `_RUNBOOK-render-verify.md` § SYMLINK FARM). Move them out "
                f"with a SAME-MOUNT `mv` to `_to_delete/` — a `mv` to /var/tmp fails, different "
                f"filesystem. ⛔ Do NOT gitignore them: this gate ignores .gitignore on purpose. "
                f"⚠ If one of these IS a ruled committed-surface product, its directory and "
                f"filename pattern belong in `COMMITTED_SURFACE_DIRS` with the ruling that made "
                f"it committed — never by widening this check.")
        # ★ The s217-D1 recognition, and it is a NOTE rather than silence: unstaged output is
        # still something the push's clean-tree assert will meet, so the reader is told the
        # count, the licence and the next move. [[unmatched-grep-is-not-an-absence]]
        for surface in sorted({_committed_surface(p)[0] for p in products}):
            spec = COMMITTED_SURFACE_DIRS[surface]
            mine = [p for p in products if _committed_surface(p)[0] == surface]
            notes.append(
                f"INSTRUMENT-STRAY re-scope ({spec['ruling']}): {len(mine)} untracked path(s) "
                f"under `{surface}` match the ruled product pattern "
                f"`{spec['product'].pattern}` — NOT instrument strays. That directory is a "
                f"COMMITTED SURFACE minted by `{spec['generator']}`, so these are unstaged "
                f"work: STAGE them (the push clean-tree assert still refuses an unstaged tree). "
                f"⛔ An instrument signature under the same directory is STILL a fail.")
    return fails, warns, notes


# ★★ THE REGISTER-vs-STORE JOIN (#212 finding 3, built #218) — ADVISORY AT BIRTH.
#
# THE CLASS, and #212 proved it with three rows: `knowledge/_GOVERNING-RECORDS.md` (the standing
# register of Dave-owed close conditions) and `knowledge/_state.json` (the worklist store) hold
# the SAME facts and NOTHING JOINS THEM. G3, G7 and G8 were CLOSED in the store at #161 and read
# OPEN on the register for FIFTY-ONE SESSIONS, until a human happened to look. G18 runs the other
# way: a row in the store with no register row at all, so the register never carried it.
# ⇒ Two homes for one fact is a duplicate-home defect (ADR-0017 WRITE-ONCE); this gate cannot
# merge the homes, but it can make their disagreement IMPOSSIBLE TO CARRY SILENTLY.
#
# ⛔ ADVISORY AT BIRTH, AND THE TIER IS NOT AN AGENT'S TO MOVE. Promotion to BLOCKING is Dave's
# word (the #111/#161/#163 pattern: warn provisionally, ratify, then flip). It warns from day one
# rather than gating, because its inputs include HAND-WRITTEN status prose and a first red would
# land on the register's own author.
#
# ★ A DECLARED GAP PASSES, A SILENT ONE FAILS — the asymmetry this repo already runs on (#111-D1).
# The register's closing paragraph names G18 as a known, deliberate absence ("exists as a row in
# `knowledge/_state.json` and has **no row here**"), so the join reports it as DECLARED, not as
# drift. Fabricating a row to silence a gate is the failure; naming the gap is the remedy.
GOV_ROW_RE = re.compile(r"^\|\s*(G\d+[a-z]?)\s*\|(.*)\|(.*)\|(.*)\|\s*$")
GOV_ID_RE = re.compile(r"^G\d+[a-z]?$")
# The register's own legal declaration for a store row it deliberately does not carry.
GOV_DECLARED_GAP_RE = re.compile(r"`(G\d+[a-z]?)`(?:(?!\n\n).){0,400}?no row\s+here", re.S)
# status cell → store state. The register writes prose; the store writes a vocabulary.
GOV_STATUS_TO_STATE = (("CLOSED", "done"), ("PARKED", "parked"), ("OPEN", "open"))


def _gov_status(cell):
    """The register's status word for a row, or None if the cell says nothing legal.
    ⚠ FIRST-WORD-WINS is wrong here and would lie: a CLOSED cell routinely quotes the word
    OPEN in its history ("read OPEN for 51 sessions"). The marked verdict is what counts —
    `✅ **CLOSED …` / `✅ **PARKED …` — and a bare leading `OPEN` only when nothing is marked."""
    for word, state in GOV_STATUS_TO_STATE[:2]:
        if re.search(r"✅\s*\**\s*%s\b" % word, cell):
            return word, state
    if re.match(r"\s*\**\s*OPEN\b", cell):
        return "OPEN", "open"
    return None, None


def governing_records_join_check(repo):
    """Join `_GOVERNING-RECORDS.md` against `_state.json`. Returns (warns, notes). ADVISORY."""
    warns, notes = [], []
    reg_path = os.path.join(repo, "knowledge", "_GOVERNING-RECORDS.md")
    store_path = os.path.join(repo, "knowledge", "_state.json")
    if not (os.path.exists(reg_path) and os.path.exists(store_path)):
        # DECLARED, never silent — a fixture tree is not a state tree.
        return warns, [f"REGISTER↔STORE JOIN SKIPPED — "
                       f"{'register' if not os.path.exists(reg_path) else 'store'} not present "
                       f"under {repo}. NOT a pass: the join was not made here."]
    try:
        with open(reg_path, encoding="utf-8") as f:
            reg_text = f.read()
        with open(store_path, encoding="utf-8") as f:
            store = json.load(f)
    except (OSError, ValueError) as e:                                # noqa: BLE001
        return ([f"REGISTER↔STORE JOIN DID NOT RUN ({type(e).__name__}: {e}) — this is UNKNOWN, "
                 f"not agreement. Read both files by hand before wrapping."], notes)

    register = {}
    for ln in reg_text.splitlines():
        m = GOV_ROW_RE.match(ln)
        if m:
            register[m.group(1)] = m.group(4)
    declared_gaps = set(GOV_DECLARED_GAP_RE.findall(reg_text))
    rows = [it for it in store.get("items", []) if GOV_ID_RE.match(str(it.get("id", "")))]
    store_state = {it["id"]: (it.get("state") or "UNKNOWN") for it in rows}

    if not register or not rows:
        return warns, [f"REGISTER↔STORE JOIN SKIPPED — {len(register)} register row(s) vs "
                       f"{len(rows)} store row(s); one side is empty, so there is nothing to "
                       f"join. NOT a pass."]

    for gid in sorted(set(store_state) - set(register), key=lambda s: (len(s), s)):
        if gid in declared_gaps:
            notes.append(f"REGISTER↔STORE JOIN: `{gid}` is in `_state.json` "
                         f"(state `{store_state[gid]}`) with no register row — DECLARED in "
                         f"`_GOVERNING-RECORDS.md` as a known gap, so it passes. A declared gap "
                         f"passes; a silent one does not (#111-D1).")
        else:
            warns.append(f"REGISTER↔STORE JOIN (advisory): `{gid}` exists in `_state.json` "
                         f"(state `{store_state[gid]}`) but has NO ROW in "
                         f"`_GOVERNING-RECORDS.md` — the register has never carried it (the #212 "
                         f"G18 shape). Either add the row WITH a `closes_when` (new rows enter "
                         f"only that way) or DECLARE the gap in the register's own prose.")
    for gid in sorted(set(register) - set(store_state), key=lambda s: (len(s), s)):
        warns.append(f"REGISTER↔STORE JOIN (advisory): register row `{gid}` has no item in "
                     f"`_state.json` — the worklist cannot surface a governing item it does not "
                     f"hold. Mint the store row, or say in the register why it has none.")
    for gid in sorted(set(register) & set(store_state), key=lambda s: (len(s), s)):
        word, mapped = _gov_status(register[gid])
        if word is None:
            warns.append(f"REGISTER↔STORE JOIN (advisory): register row `{gid}`'s status cell "
                         f"states no legal verdict — `{register[gid].strip()[:90]}`. UNKNOWN is "
                         f"never defaulted to agreement; write `OPEN`, `✅ CLOSED …` or "
                         f"`✅ PARKED …`.")
            continue
        if mapped != store_state[gid]:
            warns.append(f"REGISTER↔STORE JOIN (advisory): `{gid}` DISAGREES — register says "
                         f"`{word}`, `_state.json` says `{store_state[gid]}`. This is the #212 "
                         f"finding-3 shape exactly (G3/G7/G8 read OPEN on the register for 51 "
                         f"sessions after the store closed them). Fix the LAGGING home; the "
                         f"closure is inscribed in its owning ledger first, then marked here.")
    if not warns:
        notes.append(f"REGISTER↔STORE JOIN: {len(register)} register row(s) joined against "
                     f"{len(rows)} `_state.json` row(s) — ids and statuses AGREE "
                     f"({len(declared_gaps)} declared gap(s)). ADVISORY at birth; promotion to "
                     f"blocking is Dave's.")
    return warns, notes


# ★★ THE REGEN-SERIAL COMPLETENESS CHECK (#221) — ADVISORY AT BIRTH.
#
# THE CLASS: the regen serial set is ORDERED, and a wave that regenerates a SUBSET of it commits
# artefacts that disagree with the generators standing beside them. #210 paid ~6 CI reds for
# exactly that. The remedy has been carried as PROSE in every divvy brief since — "run the WHOLE
# serial per wave, ramp first, index last" — and by #221 THREE separate conductors had restated it
# by hand in three briefs. A rule that must be re-typed by every conductor is a rule with no
# instrument [[gate-dont-patch]]; this is the instrument.
#
# ⛔ WHAT IT CAN AND CANNOT SEE, SAID BEFORE IT SPEAKS [[feedback-measuring-tool-must-not-guess]].
# git records WHICH ARTEFACTS CHANGED. It does not record WHICH SCRIPTS RAN, so "ramp first, index
# last" is only half observable from this seat, and the halves are reported separately rather than
# blended into one confident verdict [[measure-dont-convert-units]]:
#   • MEMBERSHIP is observable, and it is the half that actually cost the CI reds: the wave changed
#     artefacts owned by serial members i…j and left a member INSIDE that span untouched.
#   • ORDER is observable ONLY while the wave is still UNCOMMITTED, because only then were the
#     artefacts' mtimes written by this machine in this session. Once committed, mtime is checkout
#     noise, and this arm DECLARES ITSELF UNOBSERVABLE rather than grade on rubbish (#173: a gate
#     that cannot pass in one environment is a defect — one that SAYS SO is not).
#
# ★ NOTHING BELOW IS TYPED, and that is the whole design. The serial's ORDER is PARSED out of
# `_build_all.py::STEPS`, which is its one home (ADR-0017 WRITE-ONCE — this ADDRESSES that home,
# it never copies it), and an artefact's OWNER is read from the artefact's own generation banner.
# ⛔ Parsed with `ast`, never imported: executing `_build_all.py` to learn its own step order would
# put the build's module-level code on the wrap path, and a measuring instrument must not be able
# to start a build [[instrument-without-a-consumer]] in reverse.
# ⚠ A provenance claim is believed ONLY when the script it names is ITSELF a serial member. Prose
# that merely says the word "generated" proves nothing [[unmatched-grep-is-not-an-absence]], and
# `_REVIEW-SIGNOFF.md` really does carry the sentence "generated review inherits them".
#
# ⛔ ADVISORY AT BIRTH. The tier lives at REGEN_SERIAL_BLOCKING and promotion is DAVE'S WORD, not
# an agent's. It warns rather than gates because its population is derived from hand-written
# banners, and a first red would land on a conductor mid-wrap.
REGEN_SERIAL_BLOCKING = False
# The serial's terminal member, named by the standing ritual ("`_build_memento_index.py` LAST",
# `_RUNBOOK-capture-ritual.md` step 2g). ⚠ ADDRESSED, not invented: this is the ONE member the
# `index last` half of the rule speaks about, and the termination arm asks about no other.
REGEN_SERIAL_INDEX = "_build_memento_index.py"
# The generation banner. A line must BOTH carry one of these markers AND name a serial member.
_REGEN_MARK_RE = re.compile(r"[Gg]enerated|GENERATED|[Rr]egenerated?\s+by|AUTO-GENERATED|DO NOT EDIT")
_REGEN_PY_RE = re.compile(r"\b([A-Za-z0-9_][A-Za-z0-9_./-]*\.py)\b")
# Provenance lives in a header. Never read a multi-megabyte artefact whole to find it.
_REGEN_SCAN_BYTES = 8192
_REGEN_EXTS = (".md", ".html", ".css", ".json", ".svg")


def _regen_serial_positions(repo):
    """`{script basename: FIRST position in _build_all.py::STEPS}`, PARSED not executed.

    Returns (positions, error). `error` is a LOUD, NAMED string — never an empty dict wearing a
    green's clothes [[a-crash-is-not-a-fail]].
    """
    path = os.path.join(repo, "knowledge", "_build_all.py")
    if not os.path.exists(path):
        return None, "no `knowledge/_build_all.py` under this tree"
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=path)
    except (OSError, SyntaxError, ValueError) as e:                   # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"
    node = None
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "STEPS" for t in stmt.targets):
            node = stmt.value
            break
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None, "`STEPS` is not a module-level list/tuple in `_build_all.py`"
    positions = {}
    for i, el in enumerate(node.elts):
        if isinstance(el, (ast.Tuple, ast.List)) and len(el.elts) >= 2:
            s = el.elts[1]
            if isinstance(s, ast.Constant) and isinstance(s.value, str):
                positions.setdefault(os.path.basename(s.value), i)
    if not positions:
        return None, "`STEPS` parsed but named no scripts"
    return positions, None


def _regen_owner(abs_path, positions):
    """The serial script that CLAIMS `abs_path` in its own generation banner, or None."""
    try:
        with open(abs_path, encoding="utf-8", errors="replace") as f:
            head = f.read(_REGEN_SCAN_BYTES)
    except OSError:
        return None
    for ln in head.splitlines():
        if not _REGEN_MARK_RE.search(ln):
            continue
        for m in _REGEN_PY_RE.finditer(ln):
            name = os.path.basename(m.group(1))
            if name in positions:
                return name
    return None


def _regen_owned_map(repo, positions):
    """`{serial script: [tracked artefacts it claims]}` across the whole tracked tree.

    This is the population the MEMBERSHIP arm needs: without it the check could say which members
    a wave HIT but never which it SKIPPED, and a gate that cannot name the omission is the #210
    lesson restated rather than enforced.
    """
    out = _git_out(repo, "ls-files")
    if out is None:
        return None
    owned = {}
    for rel in out.splitlines():
        rel = rel.strip()
        if not rel.endswith(_REGEN_EXTS):
            continue
        owner = _regen_owner(os.path.join(repo, rel), positions)
        if owner:
            owned.setdefault(owner, []).append(rel)
    return owned


def regen_serial_check(repo, sha=None):
    """Did this wave run the WHOLE ordered serial, or a subset? Returns (warns, notes). ADVISORY."""
    warns, notes = [], []
    positions, err = _regen_serial_positions(repo)
    if positions is None:
        return warns, [f"REGEN SERIAL SKIPPED — the serial's own home is unreadable ({err}). "
                       f"NOT a pass: the ordered set was never read, so nothing was compared."]
    if sha is None:
        wrap = _last_wrap_commit(repo)
        if wrap is None:
            return warns, [f"REGEN SERIAL SKIPPED — no `after #<n>` wrap commit is visible under "
                           f"{repo}, so the wave has no start point. NOT a pass."]
        sha = wrap[0]
    changed = _changed_since(repo, sha, ".")
    if changed is None:
        return ([f"REGEN SERIAL DID NOT RUN — git could not name the set changed since "
                 f"`{sha[:7]}`. This is UNKNOWN, not a clean wave."], notes)
    # ⚡ The ownership map is a whole-tree header sweep (~1,400 files, ~8 s). It is only needed
    # once the wave is KNOWN to contain a serial artefact, so ask the cheap question first: are
    # any of THESE changed paths claimed? Most wraps regenerate nothing and stop on the next line.
    changed_set = set(changed)
    if not any(_regen_owner(os.path.join(repo, rel), positions) for rel in changed
               if rel.endswith(_REGEN_EXTS)):
        return warns, [f"REGEN SERIAL: {len(changed)} path(s) changed since `{sha[:7]}`, none of "
                       f"them an artefact claimed by a serial member — no regen wave in evidence, "
                       f"so there is no serial to complete."]
    owned = _regen_owned_map(repo, positions)
    if owned is None:
        return ([f"REGEN SERIAL DID NOT RUN — `git ls-files` could not answer under {repo}, so "
                 f"the artefact-ownership map is UNKNOWN, not empty."], notes)

    hit = sorted({s for s, arts in owned.items() if changed_set.intersection(arts)},
                 key=lambda s: positions[s])
    if not hit:
        return warns, [f"REGEN SERIAL: {len(changed)} path(s) changed since `{sha[:7]}` include a "
                       f"claimed artefact, but none is TRACKED under a serial member's ownership "
                       f"(a new, uncommitted artefact). Nothing to complete; NOT a full pass."]

    lo, hi = positions[hit[0]], positions[hit[-1]]
    skipped = sorted((s for s, arts in owned.items()
                      if lo < positions[s] < hi and not changed_set.intersection(arts)),
                     key=lambda s: positions[s])
    span = (f"`{hit[0]}` (step {lo}) … `{hit[-1]}` (step {hi})" if len(hit) > 1
            else f"`{hit[0]}` (step {lo}) alone")

    # ---- ARM 1, MEMBERSHIP: a hole inside the span is the #210 shape exactly.
    if skipped:
        warns.append(
            f"REGEN SERIAL (advisory): this wave regenerated {span}, but "
            f"{len(skipped)} serial member(s) INSIDE that span were NOT re-run — "
            + " · ".join(f"`{s}` (step {positions[s]})" for s in skipped[:6])
            + (f" (+{len(skipped) - 6} more)" if len(skipped) > 6 else "")
            + ". The regen serial set is ORDERED and is run WHOLE per wave, ramp first, index "
              "last — #210 paid ~6 CI reds for exactly this subset. Re-run the skipped members "
              "in step order, or say in the wrap record why this wave legitimately stops short.")

    # ---- ARM 2, TERMINATION. ⛔ NARROW ON PURPOSE. The obvious generalisation — "the highest
    # -positioned member that owns an artefact must always be in the wave" — is WIDER THAN THE
    # RULE, and a gate may only be as wide as the rule it enforces [[gate-glob-scope-rule]]. The
    # standing discipline names ONE terminal member, the memento index (`_RUNBOOK-capture-ritual`
    # step 2g: "`_build_memento_index.py` LAST"), because that is the step whose output must
    # describe the tree every other step just rewrote. So this arm asks about THAT member and
    # nothing else, and declares itself inapplicable rather than guessing a terminal.
    if REGEN_SERIAL_INDEX not in owned:
        notes.append(f"REGEN SERIAL — TERMINATION ARM INAPPLICABLE (declared): `"
                     f"{REGEN_SERIAL_INDEX}` claims no tracked artefact in this tree, so "
                     f"`index last` cannot be observed here. NOT a pass.")
    elif positions.get(REGEN_SERIAL_INDEX, -1) > hi:
        warns.append(
            f"REGEN SERIAL (advisory): this wave regenerated {span} but did NOT re-run "
            f"`{REGEN_SERIAL_INDEX}` (step {positions[REGEN_SERIAL_INDEX]}), which the capture "
            f"ritual runs LAST (step 2g) precisely so the corpus describes the tree the earlier "
            f"steps just rewrote. Run it last, or say in the wrap record why this wave does not.")

    # ---- ARM 3, ORDER: only honest while the wave is uncommitted. Otherwise DECLARE the blindness.
    dirty_out = _git_out(repo, "diff", "--name-only")
    dirty = {p.strip() for p in (dirty_out or "").splitlines() if p.strip()}
    stamps = []
    for s in hit:
        arts = [a for a in owned[s] if a in changed_set]
        if not all(a in dirty for a in arts):
            stamps = None
            break
        try:
            stamps.append((positions[s], s, max(os.path.getmtime(os.path.join(repo, a))
                                                for a in arts)))
        except OSError:
            stamps = None
            break
    if stamps is None or len(stamps) < 2:
        notes.append("REGEN SERIAL — ORDER ARM UNOBSERVABLE (declared, not passed): mtimes only "
                     "testify while the wave is still uncommitted in this working tree. Part of "
                     "this wave is already committed, so run order cannot be read from this seat "
                     "and is NOT being graded [[a-crash-is-not-a-fail]].")
    else:
        inversions = [(a, b) for (_pa, a, ma), (_pb, b, mb) in zip(stamps, stamps[1:])
                      if ma > mb]
        if inversions:
            warns.append(
                "REGEN SERIAL (advisory): the serial ran OUT OF ORDER — "
                + " · ".join(f"`{a}` was regenerated AFTER `{b}`, which follows it in `STEPS`"
                             for a, b in inversions[:4])
                + ". Ramp first, index last: a later member built against an earlier member's "
                  "stale output is the #210 red wearing a full-serial disguise.")
        else:
            notes.append(f"REGEN SERIAL: order arm OBSERVABLE (wave uncommitted) and CLEAN — "
                         f"{len(stamps)} member(s) regenerated in `STEPS` order.")

    if not warns:
        notes.append(f"REGEN SERIAL: wave since `{sha[:7]}` regenerated {span}; no member inside "
                     f"the span was skipped and the terminal member is accounted for "
                     f"({len(owned)} of {len(positions)} serial members own tracked artefacts). "
                     f"ADVISORY at birth; promotion to blocking is Dave's.")
    return warns, notes


# ★★ THE SHARED-HELPER SINGLE-IMPLEMENTATION COMPARER (#221) — ADVISORY AT BIRTH.
#
# THE CLASS: `mask_comments` was written TWICE, once in each of two generators, with no gate
# comparing them (W-92 residual). #211 fixed the INSTANCE properly — `_htmlmask.py` is now the one
# implementation and both generators import it — and each consumer carries a bite asserting
# `mask_comments.__module__ == "_htmlmask"`.
#
# ⛔ WHAT THOSE TWO BITES CANNOT SEE, WHICH IS WHY THIS EXISTS. They are asserted BY THE TWO KNOWN
# CONSUMERS, about themselves. A THIRD file that writes its own `def mask_comments` tomorrow is
# invisible to both: neither bite runs in it, and nothing in the tree counts the implementations.
# That is the duplicate-home defect re-opening by addition rather than by edit — the shape
# ADR-0017 (WRITE-ONCE) exists to forbid, and the shape a per-consumer assertion structurally
# cannot catch [[green-tests-cannot-see-scope]].
# ⇒ This is the COMPARER: it counts implementations across the whole tracked tree and names every
# consumer that reaches the helper by any route other than the one home.
#
# ⚠ PARSED IN THE CONSUMER'S GRAMMAR, never grepped [[no-gate-parses-the-artefact]]: `ast`, so a
# `def mask_comments` inside a docstring, a comment or a string literal cannot fake a duplicate,
# and a real one cannot hide behind odd whitespace. A file this checkout cannot parse is reported
# as UNREADABLE, never counted as clean [[a-crash-is-not-a-fail]].
#
# ⛔ ADVISORY AT BIRTH. Tier lives at SHARED_HELPER_BLOCKING; promotion is DAVE'S WORD.
# ⛔ AND IT COMPARES ONLY — it never rewrites a generator. Consolidating a real second
# implementation is a refactor with a ruling attached, and this gate's job is to make the
# duplicate impossible to carry SILENTLY, not to pick the survivor.
SHARED_HELPER_BLOCKING = False
# helper name → the ONE module that may define it (basename of its home).
SHARED_HELPERS = {"mask_comments": "_htmlmask.py"}


def shared_helper_dedup_check(repo):
    """One implementation per shared helper, tree-wide. Returns (warns, notes). ADVISORY."""
    warns, notes = [], []
    out = _git_out(repo, "ls-files", "*.py")
    if out is None:
        return ([f"SHARED HELPER: the dedup comparer DID NOT RUN — `git ls-files` could not "
                 f"answer under {repo}. UNKNOWN, not a single implementation."], notes)
    files = [p.strip() for p in out.splitlines() if p.strip().endswith(".py")]
    if not files:
        return warns, [f"SHARED HELPER dedup SKIPPED — no tracked `.py` under {repo}. NOT a pass."]
    defs, importers, callers, unreadable = {}, {}, {}, []
    for rel in files:
        try:
            with open(os.path.join(repo, rel), encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=rel)
        except (OSError, SyntaxError, ValueError, UnicodeDecodeError) as e:   # noqa: BLE001
            unreadable.append(f"`{rel}` ({type(e).__name__})")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in SHARED_HELPERS:
                defs.setdefault(node.name, []).append(rel)
            elif isinstance(node, ast.ImportFrom):
                for a in node.names:
                    if a.name in SHARED_HELPERS:
                        importers.setdefault(a.name, {})[rel] = node.module or ""
            elif isinstance(node, ast.Name) and node.id in SHARED_HELPERS:
                callers.setdefault(node.id, set()).add(rel)
    if unreadable:
        warns.append(f"SHARED HELPER (advisory): {len(unreadable)} tracked `.py` file(s) could "
                     f"NOT be parsed, so they were NOT searched for a duplicate implementation — "
                     + " · ".join(unreadable[:4])
                     + ". UNKNOWN is never counted as clean.")
    for helper, home in sorted(SHARED_HELPERS.items()):
        homes = sorted(defs.get(helper, []))
        legal = [p for p in homes if os.path.basename(p) == home]
        strays = [p for p in homes if os.path.basename(p) != home]
        if not homes:
            warns.append(f"SHARED HELPER (advisory): `{helper}()` is DECLARED to live in `{home}` "
                         f"but NOTHING in the tracked tree defines it. Either the home moved and "
                         f"SHARED_HELPERS is stale, or the helper is gone and its consumers are "
                         f"broken — an unmatched search is not an absence.")
            continue
        if strays:
            warns.append(
                f"SHARED HELPER (advisory): `{helper}()` has {len(homes)} implementations and may "
                f"have ONE — its home is `{home}`, and it is ALSO defined in "
                + " · ".join(f"`{p}`" for p in strays[:5])
                + (f" (+{len(strays) - 5} more)" if len(strays) > 5 else "")
                + ". This is the W-92 duplicate-home defect re-opening BY ADDITION (ADR-0017 "
                  "WRITE-ONCE). ⛔ Which implementation survives is a REFACTOR WITH A RULING "
                  "ATTACHED — this gate names the duplicate, it does not pick the winner.")
        elif not legal:
            warns.append(f"SHARED HELPER (advisory): `{helper}()` is defined only in "
                         + " · ".join(f"`{p}`" for p in homes)
                         + f", never in its declared home `{home}`.")
        for rel, module in sorted(importers.get(helper, {}).items()):
            if module and os.path.basename(home)[:-3] not in module.split("."):
                warns.append(f"SHARED HELPER (advisory): `{rel}` imports `{helper}` from "
                             f"`{module}`, not from `{home[:-3]}` — a second route to a shared "
                             f"helper is a second implementation waiting to happen.")
        blind = sorted(callers.get(helper, set()) - set(importers.get(helper, {})) - set(homes))
        if blind:
            notes.append(f"SHARED HELPER: {len(blind)} file(s) name `{helper}` without a direct "
                         f"`from {home[:-3]} import` — "
                         + " · ".join(f"`{p}`" for p in blind[:4])
                         + ". Re-exported or locally aliased; NOT flagged, but named so a reader "
                           "can check the route rather than assume it.")
        if not strays and legal:
            notes.append(f"SHARED HELPER: `{helper}()` has exactly ONE implementation "
                         f"(`{legal[0]}`) and {len(importers.get(helper, {}))} importer(s) across "
                         f"{len(files)} tracked `.py` file(s). ADVISORY at birth; promotion to "
                         f"blocking is Dave's.")
    return warns, notes


# ------------------------------------------- ★ #218 — FILED SUB-REPORTS, THE CITATION CHECK
# `s218-D7`: every sub writes its full report to `notes/_subreports/` and returns a STUB. The
# stub is the ONLY thing the conductor sees in chat, which imports one specific failure mode —
# THE UNREAD POINTER. A report filed and never opened is worse than no report: the window closes
# believing the lane reported, and the finding set goes into history unread. So the wrap REFUSES
# to close over a filed report that this session's own record does not name BY PATH.
#
# ⚠ WHAT "NEWER THAN THE LAST WRAP" MEANS HERE, MECHANICALLY. The last wrap is the most recent
# commit whose subject opens `after #<n>` — the capture-ritual commit convention (`git log`
# confirms it: `after #218 …`, `after #215 …`). Population = every `notes/_subreports/*.md` that
# has CHANGED against that commit (tracked: `git diff`) or does not exist in it at all
# (untracked: `git ls-files --others`). No wrap commit, or no git ⇒ LOUD UNKNOWN, never a pass:
# a check that cannot bound its own window has not measured anything [[a-crash-is-not-a-fail]].
#
# ⚠ AND THE CITATION SURFACE IS SCOPED THE SAME WAY, which is the half that keeps this honest.
# If any file anywhere counted as a citation, the check would be nearly always-true — the report
# itself would satisfy it. The surface is THIS SESSION'S record only: the ★ LATEST banner regions
# of `GOOD-MORNING.md` / `_CHAIN.md`, plus the receipts that are themselves new or changed since
# the last wrap. A receipt untouched since the last wrap is a PRIOR session's record and does not
# cite anything for this one [[gate-glob-scope-rule]].
#
# ⛔ ADVISORY AT BIRTH. It appends to WARNS, never to FAILS. Promotion to blocking is DAVE'S
# WORD, not an agent's — the one line below is the only place that changes, and it does not
# change here (the #111/#161/#163 pattern: warn provisionally, ratify, then flip).
SUBREPORT_CITE_BLOCKING = False
SUBREPORT_DIR = os.path.join("notes", "_subreports")
SUBREPORT_TEMPLATE = "_TEMPLATE.md"
SUBREPORT_RECEIPTS = os.path.join("notes", "_receipts")
# The two PARSED lines of the skeleton (`notes/_subreports/_TEMPLATE.md`). Quoted exactly as the
# template writes them, per [[gate-must-quote-what-it-forbids]] — and parsed rather than
# eyeballed because the stub's figures are COPIED from these lines: an unparseable COUNTS line
# means the stub's numbers came from somewhere else [[no-gate-parses-the-artefact]].
# ⛔ #221 — THE GATE AND ITS OWN TEMPLATE DISAGREED, AND THE TEMPLATE IS THE INSTRUCTION.
# `_TEMPLATE.md:45` prescribes ``COUNTS: findings `<N>` · ruling-shaped `<N>` · UNPROVEN `<N>` ``
# — BACKTICKED, because that is how this project writes a figure. The pattern demanded BARE
# digits, so a sub that followed the skeleton exactly produced a line this gate called
# unparseable. MEASURED at #221 across `notes/_subreports/`: **37 of 44** filed reports carrying a
# COUNTS line failed the parse, the #220 audit reports among them — i.e. the check had been
# reporting "no parseable COUNTS line" about reports whose COUNTS line was CORRECT.
# ⇒ Fixed on the GATE, not on 37 reports: where a queue and its canon disagree, the defect is the
# side that is not the instruction [[feedback-survey-before-build]]. The figure may now wear the
# repo's ordinary decoration (backticks and/or bold) and nothing else is loosened — the three
# fields, their order and their separator are still the specification, and a malformed line still
# fails (driven both ways in `selftest_subreport_citation`).
# ⚠ AND THE SECOND HALF, MEASURED THE SAME WAY: many lanes carry the three required fields IN
# ORDER and then keep going (`… · UNPROVEN 5 · new gates 19 · selftest bites 4`). The three
# figures the stub copies are all present and parseable, so the trailing continuation is not a
# defect — anchoring hard at `$` was. Widening for it takes the parse from 13/44 to 24/44.
# ⛔ AND NO FURTHER, DELIBERATELY. A third form exists (`COUNTS: 14 findings · 3 ruling-shaped`,
# the figure BEFORE the noun, 3 more reports) and it is NOT accepted here: that is a change to the
# CONTRACT's vocabulary, not to its decoration, and "do not loosen it blind" is the #218 lesson on
# this very check. It is filed as a ruling-shaped question instead [[feedback-dont-launder-a-premise-into-a-ruling]].
_CNT = r"[`*]{0,3}(\d+)[`*]{0,3}"
SUBREPORT_COUNTS_RE = re.compile(
    r"^\s*[`*]{0,2}COUNTS:[`*]{0,2}\s*findings\s+" + _CNT + r"\s*·\s*ruling-shaped\s+" + _CNT
    + r"\s*·\s*UNPROVEN\s+" + _CNT + r"(?:\s*[·`*].*)?$", re.M)
SUBREPORT_REPLAY_RE = re.compile(r"^REPLAY-THESE:\s*(\S.*)$", re.M)
SUBREPORT_QUESTIONS_RE = re.compile(r"^#{1,6}\s*RULING-SHAPED QUESTIONS\s*$", re.M)
WRAP_COMMIT_SUBJECT_RE = re.compile(r"^after\s+#\d+\b")


def _git_out(repo, *args):
    """stdout of a git call under `repo`, or None if git could not answer. Never a silent ''."""
    try:
        r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, timeout=30)
    except Exception:                                                 # noqa: BLE001
        return None
    return r.stdout if r.returncode == 0 else None


def _last_wrap_commit(repo, limit=400):
    """(sha, subject) of the most recent capture-ritual commit, or None if none is visible."""
    out = _git_out(repo, "log", "-n", str(limit), "--format=%H%x09%s")
    if out is None:
        return None
    for line in out.splitlines():
        sha, _tab, subj = line.partition("\t")
        if WRAP_COMMIT_SUBJECT_RE.match(subj.strip()):
            return sha, subj.strip()
    return None


def _is_subreport(rel):
    """A repo-relative path that is a FILED REPORT — flat, `.md`, and not the skeleton.
    `assets/<stem>/…` sits under the same directory and is EVIDENCE, never a document."""
    rel = rel.strip().replace("\\", "/")
    d = SUBREPORT_DIR.replace("\\", "/")
    if not rel.startswith(d + "/"):
        return False
    tail = rel[len(d) + 1:]
    return "/" not in tail and tail.endswith(".md") and tail != SUBREPORT_TEMPLATE


def _changed_since(repo, sha, pathspec):
    """Repo-relative paths under `pathspec` that differ from `sha` OR are untracked. None if git
    could not answer either half — a partial answer here would silently narrow the population."""
    tracked = _git_out(repo, "diff", "--name-only", sha, "--", pathspec)
    others = _git_out(repo, "ls-files", "--others", "--exclude-standard", "--", pathspec)
    if tracked is None or others is None:
        return None
    return sorted({p.strip() for p in (tracked + "\n" + others).splitlines() if p.strip()})


def subreport_citation_check(repo):
    """`s218-D7` — a filed sub-report newer than the last wrap must be CITED BY PATH in this
    session's own record. Returns (warns, notes). ADVISORY at birth."""
    warns, notes = [], []
    sub_abs = os.path.join(repo, SUBREPORT_DIR)
    if not os.path.isdir(sub_abs):
        return warns, [f"FILED SUB-REPORTS: no `{SUBREPORT_DIR}/` under {repo} — nothing filed "
                       f"here, so nothing to cite. NOT a pass: the check did not run."]
    wrap = _last_wrap_commit(repo)
    if wrap is None:
        return ([f"FILED SUB-REPORTS: the citation check DID NOT RUN — no commit whose subject "
                 f"opens `after #<n>` is visible under {repo} (no git, or no capture-ritual "
                 f"commit in the last 400). This is UNKNOWN, not agreement: list "
                 f"`{SUBREPORT_DIR}/` by hand and check every report is named in the receipt."],
                notes)
    sha, subj = wrap
    changed = _changed_since(repo, sha, SUBREPORT_DIR)
    if changed is None:
        return ([f"FILED SUB-REPORTS: the citation check DID NOT RUN — `git diff`/`git ls-files` "
                 f"gave no answer under {repo}. UNKNOWN, not agreement."], notes)
    population = [p for p in changed if _is_subreport(p) and os.path.exists(os.path.join(repo, p))]
    if not population:
        return warns, [f"FILED SUB-REPORTS: none filed since the last wrap "
                       f"(`{sha[:7]} {subj[:60]}`) — nothing to cite."]

    # ---- the citation surface, scoped to THIS session's record (see the header comment).
    surfaces, surface_names = [], []
    for fname in ("GOOD-MORNING.md", "_CHAIN.md"):
        p = os.path.join(repo, fname)
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    region = _latest_banner_region(f.read())
            except OSError:
                region = None
            if region:
                surfaces.append(region)
                surface_names.append(f"{fname} ★ LATEST banner")
    receipts = _changed_since(repo, sha, SUBREPORT_RECEIPTS) or []
    for rel in receipts:
        p = os.path.join(repo, rel)
        if rel.endswith(".md") and os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    surfaces.append(f.read())
                surface_names.append(rel)
            except OSError:
                pass
    blob = "\n".join(surfaces)

    uncited = [p for p in population if p not in blob]
    for p in uncited:
        warns.append(
            f"FILED SUB-REPORT UNCITED (advisory): `{p}` was filed since the last wrap "
            f"(`{sha[:7]}`) and NO path citation for it exists in this session's record "
            f"({', '.join(surface_names) or 'no receipt or banner found at all'}). `s218-D7` "
            f"hands the conductor a STUB and makes the FILE the authority — a filed report the "
            f"session record never names is the unread pointer, and it goes into history unread. "
            f"Cite it by path in the receipt (or the ★ LATEST banner), or say in the receipt why "
            f"it is deliberately not carried. ⛔ ADVISORY at birth; promotion is Dave's.")

    # ---- the PARSE half: the stub's figures are copied off these two lines, so they must parse.
    for p in population:
        try:
            with open(os.path.join(repo, p), encoding="utf-8") as f:
                text = f.read()
        except OSError as e:                                          # noqa: BLE001
            warns.append(f"FILED SUB-REPORT UNREADABLE (advisory): `{p}` — {e}")
            continue
        if not SUBREPORT_COUNTS_RE.search(text):
            warns.append(
                f"FILED SUB-REPORT COUNTS (advisory): `{p}` carries no parseable COUNTS line. "
                f"The skeleton's form is exactly `COUNTS: findings <N> · ruling-shaped <N> · "
                f"UNPROVEN <N>` on its own line — parsed, not prose, because the stub's figures "
                f"are copied off it and a stub figure that was retyped is the defect `s218-D7` "
                f"exists to stop. Template: `{SUBREPORT_DIR}/{SUBREPORT_TEMPLATE}`.")
        if not SUBREPORT_REPLAY_RE.search(text):
            warns.append(
                f"FILED SUB-REPORT REPLAY (advisory): `{p}` carries no `REPLAY-THESE:` line. A "
                f"deferral must be DECLARED and PRICED — write the paths with their token "
                f"prices, or exactly `REPLAY-THESE: none — the stub carries everything.`")
        if not SUBREPORT_QUESTIONS_RE.search(text):
            warns.append(
                f"FILED SUB-REPORT QUESTIONS (advisory): `{p}` has no `RULING-SHAPED QUESTIONS` "
                f"heading. The section is mandatory even when the answer is 'none' — it is what "
                f"stops a sub's generated prose from arriving as a decision.")
    if not warns:
        notes.append(f"FILED SUB-REPORTS: {len(population)} report(s) filed since `{sha[:7]}`, "
                     f"every one cited by path in this session's record and carrying a parseable "
                     f"COUNTS / REPLAY-THESE / RULING-SHAPED QUESTIONS skeleton. Surfaces read: "
                     f"{', '.join(surface_names)}. ADVISORY at birth; promotion is Dave's.")
    return warns, notes


def plan_block_check(repo):
    """B2 SEAM OBLIGATION AT THE WRAP SEAM (brief `_BRIEF-borrowed-instruments-…-v2.md` §2,
    ruled s179-D1). Returns (fails, warns).

    ⛔ WHAT IT GRADES, AND WHY NOT THE OBVIOUS THING. It does NOT verify a stored block — there
    is no stored block and there must never be one (§6 P3: a `current.md` is the duplicate-home
    defect the register system exists to prevent). It grades **whether the state on disk STILL
    RENDERS a plan block at all**: it drives `_checkin.py`'s own renderer — the SAME code the
    seam prints, imported, never re-implemented [[a-new-tier-silently-bypasses-its-tests]] — and
    FAILS if any of DONE/DOING/NEXT/STOP comes back `UNKNOWN — …`.

    That is the wrap-seam half of P1/P2. The check-in half (`_checkin.py` default run) refuses to
    hand a bad block FORWARD into a brief; this half refuses to CLOSE a session whose state the
    next session's block cannot be rendered from — the read-chain staleness class, caught at the
    seam where it becomes durable [[check-after-its-own-remedy]].

    ⚠ BUDGET AND THE TRANSCRIPT ARE NOT TOUCHED HERE. `derive_block_fields` is state-only; the
    gate must not need a live transcript or tiktoken to run, or it becomes a gate that cannot
    pass in one environment [[gate-cannot-pass-in-one-environment]].
    """
    fails, warns = [], []
    if not os.path.exists(os.path.join(repo, "_CHAIN.md")):
        # DECLARED, never silent: a fixture tree is not a state tree, and a gate that fails on
        # every temp dir gets muted rather than fixed.
        return fails, [f"B2 PLAN BLOCK check SKIPPED — no `_CHAIN.md` under {repo}, so this is "
                       f"not a state tree. NOT a pass: the seam was not graded here."]
    try:
        sys.path.insert(0, os.path.join(repo, "knowledge"))
        import _checkin
        fields = _checkin.derive_block_fields(_checkin.read_block_sources(repo))
    except SystemExit as e:                                       # read_block_sources refuses loud
        return ([f"B2 PLAN BLOCK: state does not render a block — {str(e)[:400]}"], warns)
    except Exception as e:                                        # noqa: BLE001
        return ([f"B2 PLAN BLOCK: the renderer did not run ({type(e).__name__}: {e}) — the seam "
                 f"obligation is UNKNOWN, not met. Run `python3 knowledge/_checkin.py` and read "
                 f"the SEAM section."], warns)
    for field in ("DONE", "DOING", "NEXT", "STOP"):
        if re.search(r"\bUNKNOWN\s+—", fields.get(field, "")):
            fails.append(f"B2 PLAN BLOCK: {field} does not resolve from state — "
                         f"`{fields[field][:200]}`. A wrap may not close on state the next "
                         f"seam's block cannot be rendered from. Fix the state (the probe is "
                         f"named in the string), then re-run `python3 knowledge/_checkin.py`.")
    return fails, warns


def wrap_checks(repo, today, lane=False):
    fails, warns, notes = [], [], []
    iso = today.isoformat()
    _bf, _bw = plan_block_check(repo)           # B2 seam obligation — LANE wraps too: a lane
    fails += _bf                                # seam is the seam this block exists for.
    warns += _bw
    _sf, _sw, _sn = instrument_stray_check(repo)  # #138 — runs for LANE wraps too, on purpose:
    fails += _sf                                  # a lane session renders like any other.
    warns += _sw
    notes += _sn                                  # ★ #218: the s217-D1 committed-surface note
    # ★ #218 — the register↔store join (#212 finding 3). ADVISORY AT BIRTH: it appends to WARNS,
    # never to FAILS. ⛔ Promotion to blocking is DAVE'S WORD, not an agent's — the line below is
    # the only place that changes, and it does not change here.
    _jw, _jn = governing_records_join_check(repo)
    warns += _jw
    notes += _jn
    # ★ #221 — the regen-serial completeness check (#210's ~6 CI reds, restated by hand in three
    # conductors' briefs). ADVISORY AT BIRTH: it appends to WARNS, never to FAILS. ⛔ The tier
    # lives at REGEN_SERIAL_BLOCKING and promotion to blocking is DAVE'S WORD, not an agent's.
    _rw, _rn = regen_serial_check(repo)
    (fails if REGEN_SERIAL_BLOCKING else warns).extend(_rw)
    notes += _rn
    # ★ #221 — the shared-helper single-implementation comparer (W-92's residual, the half the two
    # per-consumer bites structurally cannot see). ADVISORY AT BIRTH; tier at SHARED_HELPER_BLOCKING.
    _hw, _hn = shared_helper_dedup_check(repo)
    (fails if SHARED_HELPER_BLOCKING else warns).extend(_hw)
    notes += _hn
    # ★ #218 `s218-D7` — the filed-sub-report citation check. Runs for LANE wraps too, on purpose:
    # a lane delegates subs like any other session, and its receipt is its record. ADVISORY AT
    # BIRTH — the tier lives at SUBREPORT_CITE_BLOCKING and promotion is DAVE'S WORD.
    _cw, _cn = subreport_citation_check(repo)
    (fails if SUBREPORT_CITE_BLOCKING else warns).extend(_cw)
    notes += _cn
    # ★ #244 — the mechanised `MEMORY.md` cap. ADVISORY AT BIRTH; tier at MEMORY_CAP_BLOCKING.
    # Runs for LANE wraps too: every seat pays the index in its boot, lane or not.
    _mw, _mn = memory_cap_check(repo)
    (fails if MEMORY_CAP_BLOCKING else warns).extend(_mw)
    notes += _mn
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
        notes.append("LANE WRAP: the roll-claim check (T2, #77) is SKIPPED too — same reason, "
                     "the residual it grades lives in GOOD-MORNING.md.")
        notes.append("LANE WRAP: the stale-top-item fence (s161-D4, #161) is SKIPPED — its "
                     "scope is the `residual → #N` home in the GOOD-MORNING/_CHAIN ★ LATEST "
                     "banners, which lane sessions do not write. ⚠ If lanes ever gain a "
                     "hand-off line of their own, this exemption must go with it.")
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
        i_, n_ = boot_constant_drift_check(repo)  # ★ #110-D3 — the constant must still
        (fails if BOOT_DRIFT_BLOCKING else warns).extend(i_)   # match what is measured
        notes += n_
        f_, n_ = boot_stratum_double_count_check(repo)  # ★ `s241-D2` (S5) — one stratum, one
        fails += f_                                     # first-turn figure. BLOCKING at birth:
        notes += n_                                     # #240 declared the defect live.
        f_, n_ = lane_routing_check(repo)       # O1′ #24 — eager line ↔ records, BLOCKING
        fails += f_
        notes += n_
        f_, n_ = dofirst_index_present_check(repo)  # ★ #61 — every open item NAMED in the chain.
        fails += f_                              # BLOCKING at birth, and deliberately so: the
        notes += n_                              # failure it catches (items 9-12 invisible to a
                                                 # cold session) already happened once, unnoticed.
        f_, w_, n_ = gauge_log_continuity(repo)  # ds-022 (a) #34 — the 2f split must LAND.
        fails += f_                              # BLOCKING: three wraps in a row skipped the
        warns += w_                              # step, and #29's overrun cause is gone for good.
        notes += n_
        f_, n_ = gauge_log_subs_line(repo)       # ★ #168 — the OPTIONAL `subs N tokens (n=N)`
        (fails if SUBS_LINE_BLOCKING else warns).extend(f_)   # line. ABSENT is legal and silent;
        notes += n_                              # PRESENT must parse, and must not carry `job`
                                                 # (gen_dashboard's _JOB_RE would eat it).
        f_, n_ = stop_line_consistency(repo)     # ds-023 #54 — the stop line is `60 − wrap`, and
        fails += f_                              # the runbook contradicted itself for 11 sessions.
        notes += n_
        f_, n_ = unkeyed_testimony(repo)         # ds-022 (d) #55 — the FOURTH STATE, gated shut
        (fails if UNKEYED_BLOCKING else warns).extend(f_)   # by Dave #54. BLOCKING at birth: the
        notes += n_                              # advisory years are what let the retroactive
                                                 # key patch stand, and that patch is why the
                                                 # #53 handoff said 12 when the record said 9.
        f_, w_, n_ = roll_claim_check(repo)      # T2 #77 — the roll-residual vs _roll_state.py
        (fails if ROLL_CLAIM_BLOCKING else warns).extend(f_)   # cross-check, wired at the R3
        warns += w_                              # commit seam via the existing #74-D1 consumer
        notes += n_                              # (this call, inside wrap_checks() itself).
        f_, n_ = stale_top_item_check(repo)      # ★ s161-D4 #161 — an owed-work claim citing a
        (fails if STALE_TOP_BLOCKING else warns).extend(f_)   # ruling the store already calls
        notes += n_                              # ENACTED. BLOCKING at birth by Dave's word: the
                                                 # failure it catches carried a false "owed" for
                                                 # TWO sessions, refuted the whole time by the
                                                 # store this same wrap already parses.
        f_, n_ = carry_wording_check(repo)       # ★ s188-D2 #188 — the 2c carry gate: AGES +1,
        (fails if CARRY_GATE_BLOCKING else warns).extend(f_)   # WORDING UNCHANGED, with ONE
        notes += n_                              # exit — a retraction that cites its receipt.
                                                 # ★ BLOCKING at birth; the measured base rate
                                                 # is at CARRY_GATE_BLOCKING (11 in 10 wraps,
                                                 # all genuine truncation-drops).
        f_, n_ = title_generation_check(repo)    # #120 residual ⓪ — RENAME+NEXT-TITLE must be
        fails += f_                              # MECHANISED (`_gen_titles.py`), not hand-typed
        notes += n_                              # prose; BLOCKING, receipt is the only witness.
        notes.append(f"PRE-FLIGHT stamp: graded in REAL TOKENS (Dave #56 — amber "
                     f"{gauge.BUDGET_AMBER:,} · working {gauge.BUDGET_WORKING:,} · hard "
                     f"{gauge.BUDGET_HARD:,}); the % band's enforcement was RETIRED #74-D3 "
                     f"(history: ledger § #36, runbook ds-023). Whether the fill figure is "
                     f"HONEST is still not observable here — and the wrap term is RING-FENCED "
                     f"at any mid-session re-price (#74-D2, runbook § Half 0b (a′)).")
        notes.append("PRE-FLIGHT stamp: FORM checked only. Whether the fill figure is honest, "
                     "and whether a mid-job re-price actually happened, are NOT observable "
                     "here — discipline, not enforcement (_RUNBOOK-context-gauge.md § ★ Half 0b).")
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


# ---------------------------------------------------------------- rehearsal (#92)
# ★ #92 — THE REHEARSAL. #91-F5 measured that the wrap's binding cost is the GATE-FAILURE
# REMEDIATION LOOP (6 fails × probe→fix→re-gate, every round paid at the fullest point in the
# window — 44,211 real at #91 WITHOUT the runbook read). The remedy is not a smarter gate but
# an EARLIER one: the SAME wrap-mode run, invoked mid-window (consumer: `_checkin.py`), where a
# fix costs a cheap edit instead of a peak-fill round trip. This is #33's read-chain cut applied
# to the other end of the session, on the term F5 measured as binding.
#
# TWO RULES, both from standing memory:
#   1. SAME SEAM, NEVER A COPY — rehearsal calls run(mode="wrap") itself. A parallel checklist
#      would drift from the gate it predicts ([[check-after-its-own-remedy]]).
#   2. THE ALLOWLIST QUOTES WHAT IT EXCUSES — only the two date-stamp fails that ritual steps
#      1/2 mechanically rewrite may be classed "heals-at-wrap", matched against the gate's own
#      fail strings, scoped to the two filenames. Anything else — including a date fail on any
#      OTHER file — is STRUCTURAL: fix it now. ([[gate-must-quote-what-it-forbids]])
#
# THE LOG (`notes/_REHEARSAL-LOG.jsonl`, append-only machine lines): every rehearse AND every
# real wrap-mode run appends {date, kind, fails, structural, heals_at_wrap, warns}. That is the
# instrument #91-F5 ordered ("measure fails-at-wrap-open across sessions before trimming
# anything") — wrap-open counts build the distribution, and repeated wrap-mode lines in one
# session count the remediation rounds themselves. The log is written by the gate and read by
# humans/sessions; it is NOT the gauge log and MUST NOT be — a session writing its own
# post-mortem into `notes/_GAUGE-LOG.md` jams `roll_2f` (#91's own double-entry fail).
REHEARSAL_LOG = os.path.join("notes", "_REHEARSAL-LOG.jsonl")

HEALS_AT_WRAP_RES = (
    # wrap_checks() date-stamp fails, verbatim shape, scoped to the ONLY two files whose
    # stamps the ritual itself refreshes (steps 1/2). Quoted, not paraphrased.
    re.compile(r'^GOOD-MORNING\.md: header date zone does not carry today \(\d{4}-\d{2}-\d{2}\)'),
    re.compile(r'^_LIVE-STATE\.md: "Last refreshed" zone does not carry today \(\d{4}-\d{2}-\d{2}\)'),
)


def classify_rehearsal(fails):
    """Split gate fails into (heals_at_wrap, structural). Scoped allowlist; default STRUCTURAL."""
    heals, structural = [], []
    for f in fails:
        (heals if any(rx.match(f) for rx in HEALS_AT_WRAP_RES) else structural).append(f)
    return heals, structural


def _rehearsal_log_append(repo, entry):
    """Append one JSON line. Loud + named on failure, never raises — a broken log line must
    not block a wrap ([[a-crash-is-not-a-fail]] — the reader fails loud, the writer degrades loud)."""
    try:
        path = os.path.join(repo, REHEARSAL_LOG)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        return None
    except Exception as e:  # noqa: BLE001
        return f"⚠ REHEARSAL LOG NOT WRITTEN ({type(e).__name__}: {e}) — the fails-at-wrap-open series has a hole HERE, dated."


# ─────────────────────────────────────────────────────────────────────────────────────────────
# ★ `s241-D2` — THE WARN DELTA (D1 + S7 of the #241 ritual diet, on Dave's "apply").
#
# WHAT IT COSTS TODAY, MEASURED, NOT ASSUMED: one `--wrap` run printed 268 lines / 16,222 tape
# (tiktoken cl100k over the captured stdout, 2026-09-02, this tree), of which the WARN block is
# 17 items / 1,793 tape — and it is the SAME 17 every run, 59 `wrap-open` runs logged on
# 2026-09-02 alone. Lane D's report priced the class; these figures are this lane's own.
#
# ⛔ THE PITFALL THIS SHAPE EXISTS TO AVOID — "a warn that stops being printed stops being
# seen" (lane D, Consequences (e)). So NOTHING becomes invisible here: every warn's NAME prints
# on every run. What the delta suppresses is the BODY of a warn that has not moved since the
# previous logged run. New or changed ⇒ full text, always. No previous record ⇒ everything in
# full, and it says so.
#
# ⚠ IDENTITY, NOT EQUALITY. Warn bodies carry live figures ("33,507 tape", "10 uncommitted
# path(s)"), so keying on the exact string would mark every warn CHANGED every run and the
# delta would save nothing while claiming to. The KEY normalises digit-runs to `#` over the
# first WARN_SIG_KEY_CHARS characters; a second digest over the FULL text is what makes a moved
# figure show up as CHANGED rather than silently unchanged. Both are stored, both are short:
# the record grows by ~16 bytes per warn, not by the warn.
WARN_SIG_KEY_CHARS = 80        # how much of a warn is its IDENTITY (s241-D2)
WARN_NAME_CHARS = 56           # how much of an unchanged warn's name prints on the one-liner


def _warn_sig(w):
    """`(key8, full8)` — the stable identity of a warn and a digest of its exact wording."""
    key = re.sub(r"\d[\d,]*", "#", w.strip())[:WARN_SIG_KEY_CHARS]
    return (hashlib.sha1(key.encode("utf-8")).hexdigest()[:8],
            hashlib.sha1(w.strip().encode("utf-8")).hexdigest()[:8])


def _previous_rehearsal_record(repo):
    """The last logged record that carries `warn_sigs`, or None. Read BEFORE this run appends.

    ⚠ Returns None rather than {} on any failure — an unreadable log must make the printer fall
    back to FULL output, never to a confident empty delta that hides every warn at once
    [[a-crash-is-not-a-fail]].
    """
    path = os.path.join(repo, REHEARSAL_LOG)
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:                                              # noqa: BLE001
        return None
    for ln in reversed(lines):
        ln = ln.strip()
        if not ln:
            continue
        try:
            rec = json.loads(ln)
        except Exception:                                          # noqa: BLE001
            continue
        if isinstance(rec, dict) and rec.get("warn_sigs"):
            return rec
    return None


def _warn_delta_lines(warns, prev):
    """(`full`, `oneliner`) — which warns print whole, and the one line naming the rest.

    `full` is the list of warns to print verbatim (NEW or CHANGED, or everything when there is
    no comparable record). `oneliner` is None when there is nothing to summarise.
    """
    if not warns:
        return [], None
    if not prev:
        return list(warns), None
    known = set(prev.get("warn_sigs") or [])
    known_keys = {sig.split(":")[0] for sig in known}
    full, unchanged = [], []
    for w in warns:
        k, d = _warn_sig(w)
        if f"{k}:{d}" in known:
            unchanged.append(w)
        elif k in known_keys:
            full.append("CHANGED SINCE " + str(prev.get("date", "?")) + " — " + w)
        else:
            full.append("NEW SINCE " + str(prev.get("date", "?")) + " — " + w)
    if not unchanged:
        return full, None
    names = " · ".join(re.sub(r"\s+", " ", w.strip())[:WARN_NAME_CHARS] for w in unchanged)
    # ⚠ A WARN THAT DISAPPEARED IS ALSO A MOVE, and the NEW/CHANGED split cannot show it — a
    # dropped warn leaves no row to print. So the counts are stated whenever they differ. Losing
    # a warn is usually good news; "usually" is not a reason to let it happen unannounced.
    n_prev = prev.get("warns")
    moved = ("" if n_prev is None or n_prev == len(warns) else
             f" ⚠ THE SET MOVED: {n_prev} warn(s) at that record, {len(warns)} now.")
    return full, (moved + (" " if moved else "")
                  + f"{len(unchanged)} UNCHANGED warn(s) since the {prev.get('kind', '?')} record "
                  f"of {prev.get('date', '?')} — NAMED, bodies suppressed (`s241-D2`); run "
                  f"`python3 knowledge/_capture_gate.py --wrap --warns-full` for the bodies: "
                  f"{names}")


def run(mode="build", repo=REPO, report=REPORT, today=None, lane=False, rehearse=False,
        warns_full=False):
    today = today or datetime.date.today()
    prev_rec = None          # `s241-D2` — the warn-delta baseline; only wrap/rehearse set it
    if rehearse:
        mode = "wrap"    # SAME SEAM — the rehearsal IS a wrap-mode run, only classified + logged
        report = None
    fails, warns, notes = [], [], []
    scoped = in_scope(repo)
    for p in scoped:
        f, w = check_file(p, repo)
        fails += f
        warns += w
    # ---- ds-021 (C), RULED #81-D1. The cross-instrument unit audit, in BOTH modes.
    f, w = unit_vocabulary_audit(repo)
    fails += f
    warns += w

    # ---- retired-unit vocabulary audit, the `.md` arm.
    # ⛔⛔ BUILT #84, UNWIRED #84, AND ITS UNWIRING REASON WAS RE-MEASURED AND HALF-CORRECTED
    #     AT #84'S WRAP, ON A COLD BUDGET. DO NOT RE-WIRE, AND DO NOT DELETE, WITHOUT READING ALL
    #     OF THIS. The first version of this comment was authored past Dave's 200,000 working line.
    #
    # WHAT SURVIVED RE-MEASUREMENT (re-run at the wrap, not quoted from the build):
    #   · TRUE POSITIVES 1 of 2 — NOT the "0/1" this comment first claimed. #83 rotted TWO regions
    #     of `_RUNBOOK-context-gauge.md`, and the first measurement scoped its re-enactment to ONE.
    #     Re-run against the WHOLE pre-fix file (`git show HEAD:` at #84), the audit FIRES, and
    #     correctly, on `## Entry points`:723 — "`_checkin.py` (Half-2 throughput check-in,
    #     `tape`/cl100k)", a stale unit index with no declaration anywhere in its region.
    #     It stays BLIND to the `### Half 2` half, and that half is the interesting one: the rot
    #     there was a FALSE CLAIM ABOUT WHICH UNIT A TOOL REPORTS, wearing a CORRECT retirement
    #     disclaimer. Word-presence cannot see it, and device (ii) actively EXEMPTS it — the
    #     region says RETIRED/HISTORY three times, about a different thing.
    #     ⇒ this arm catches STALE INDEXES. It cannot catch FALSE CLAIMS. Both are real rot.
    #   ★★ AND THE MUTATION THAT MATTERS, run at #84: `selftest_retired_unit_prose`'s POSITIVE
    #     CONTROL — the two named regions Dave said must never go red — is GREEN AGAINST THE
    #     ROTTED TREE TOO. Both halves pass on the pre-fix file. A control that passes on the very
    #     defect it was written beside is an assertion, not a test. It pins the regions against a
    #     rewrite; it can never witness a re-rot. [[gate-must-quote-what-it-forbids]]
    #   · FALSE POSITIVES: 11 live, but "11/11 correct prose" is NOT established and is WITHDRAWN.
    #     2 are `_ROBUSTNESS-PORTABILITY.md`'s homonym "duct tape" — a REGEX defect in
    #     RETIRED_PROSE_WORDS_RE, cheaply fixable, not a refutation of the design.
    #     Of the 9 in `_DS-IMPROVEMENTS.md`, 7 are correct prose (dated historical readings, which
    #     #82-D1 rules must NOT be re-denominated, plus live description of the ds-021(c) machinery
    #     #81-D1 KEPT). But :1376-1377 is a present-tense `★ Status: ENACTED #34` line asserting
    #     "Caps bind on `bill`" — superseded by #54/#56 — in a region with no retirement marker.
    #     That is arguably a TRUE positive, i.e. the same defect class, in a second file.
    #
    # ⛔⛔ THE PREMISE PREVIOUSLY WRITTEN HERE IS DEAD. STRUCK #84 AT SOURCE, IN THE PLACE THAT
    # CARRIED IT. It read: "`tape`/`bill` is NOT a retired vocabulary — ds-021-C, RULED #81-D1
    # (Dave): 'tape/bill machinery KEPT as labelled legacy, not retired'."
    # ★ THE QUOTE IS VERBATIM AND THE SCOPE IS WRONG. #81-D1's PRIMARY record
    # (`notes/_MEMENTO-DECISIONS.md` § ★ #81) keeps the tape/bill **MACHINERY** — the constants,
    # `bill_of`/`fmt_units`/`ratio_status`, the three selftests pinning them, and the `ds-021 (c)`
    # n>=4 ratio fork that is Dave's. It says NOTHING about `.md` prose. And the SAME record, under
    # "⬛ STILL OPEN, DECLARED", names the opposite: "`_RUNBOOK-context-gauge.md`:463-505 still
    # teaches the RETIRED tape/bill system". ⇒ THE RULING SESSION ITSELF CALLED THE PROSE RETIRED
    # WHILE KEEPING THE CODE. `TITLE_CAP_TAPE = 120` (~:873) is likewise a live cap in CODE and
    # says nothing about prose either.
    # ★★ ONE MECHANISM, TWO PURPOSES, OPPOSITE ANSWERS — and the dead reading was taken off a
    # GENERATED REPORT LINE, which this project's standing rule forbids: repo-state claims are
    # verified against `git log` or a real run, never a banner.
    # [[premise-ages-faster-than-rule]] [[unmatched-grep-is-not-an-absence]]
    #
    # ⇒ WHERE THAT LEAVES IT. Dave RULED this arm at #84 ("option 1, both conditions") and the
    # ruling STANDS — it is NOT chasing a vocabulary he kept. It stays UNWIRED anyway, for the one
    # reason that survived: as BUILT it is a WORD-PRESENCE check, and the defect it was
    # commissioned for is a FALSE CLAIM. Re-wiring today would also block every wrap on 11 live
    # hits, at least 2 of which are a regex bug.
    # PARKED, NOT DELETED — the code, its 5 mutation tests and BOTH measurements are the evidence.
    # ⬛ FORKED TO DAVE WITH A NAMED SUCCESSOR: the cross-instrument CLAIM check — `.md` prose
    # that names an instrument AND states its unit must agree with `MEASURERS`. Checked at #84:
    # it WOULD have caught the `### Half 2` rot (prose said `tape` for `_checkin.py`; MEASURERS
    # says `real`), and `MEASURERS` already covers the instruments prose actually names
    # (`_checkin.py` 12 mentions in `knowledge/*.md`, `_capture_gate.py` 29). It is a GLOB
    # WIDENING of the shape Dave already ruled at #81-D1, not a new shape. See the #84 dossier.
    # An unwired gate cannot fail and is not an achievement; it is declared, not claimed.
    # [[instrument-without-a-consumer]]
    #
    # ✅ WIRED, BLOCKING — s163-D1 (Dave, #163): "flip to block". The two conditions that kept
    # it parked at #84 are both discharged and were re-measured before this line was written:
    # (1) the `duct tape` homonym is fixed IN THE REGEX (lookbehinds at RETIRED_PROSE_WORDS_RE,
    # word-sense only — no unit prose exempted); (2) the remaining live hits were cleared BY
    # DECLARATION, never by rephrasing — `_BANKRUPTCY-ARCHIVE.md` (historical marker) and
    # `_DS-IMPROVEMENTS.md` ds-021 (SUPERSEDED marker on the #84-named true positive). Audit
    # measured 0 fails live at wiring time. s161-D2's provisional WARN is superseded by this
    # ruling; G18 closes. The #84 caveat STANDS as scope, not as a bar: this arm catches STALE
    # INDEXES, not FALSE CLAIMS — the cross-instrument claim check remains Dave's open successor.
    f, w = retired_unit_prose_audit(repo)
    fails += f
    warns += w

    # ---- THE TRIGGER INDEX, built #81 (Dave's open item (e)) — AND THIS IS ITS CONSUMER.
    # ⛔ The reason it is called HERE and not offered as a command: `_measure_tokenizer.py` was a
    # correct instrument with ZERO consumers for fourteen sessions, and #80 re-derived what it
    # already knew. An index nothing consults repeats that exactly. The gate runs every build and
    # every wrap, so the rulings governing today's diff are surfaced whether or not anyone
    # thought to ask — which is the entire point, since you cannot search for what you do not
    # suspect. [[instrument-without-a-consumer]] [[retrieval-default-hides-the-ruling]]
    try:
        import _governs
        _hits = _governs.surface({_governs._norm(p) for p in _governs.changed_files()})
        if _hits:
            notes.append(_governs.render(_hits, "files touched this session"))
    except Exception as _e:                                     # noqa: BLE001
        # ⚠ A NOTE, NOT A FAIL, AND THE DISTINCTION IS RULED BY WHAT THIS THING IS. The index is
        # a READER of decided things; it can never make a correct tree incorrect, so it must not
        # be able to block a wrap. But it says so LOUD and NAMED — a silently absent reader is
        # the failure it was built to end, and `IndexUnreadable` exists so this line can never
        # degrade into "no rulings govern this".
        notes.append(f"⚠ TRIGGER INDEX DID NOT RUN ({type(_e).__name__}: {_e}) — no ruling was "
                     f"surfaced for this session's diff. That is NOT the same as 'nothing is "
                     f"governed'. Run `python3 knowledge/_governs.py` by hand before assuming a "
                     f"topic is undecided.")

    if mode == "wrap":
        report = None  # S-D3: wrap is stdout-only — _CAPTURE-GATE.md belongs to build mode
        f, w, n = wrap_checks(repo, today, lane=lane)
        fails += f
        warns += w
        notes += n
        # ---- #92: EVERY wrap-mode run logs its fail count — rehearsals build the early series,
        # real wraps build the fails-at-wrap-open distribution #91-F5 ordered, and repeated
        # wrap lines within one session ARE the remediation-round count. Append-only, machine.
        heals, structural = classify_rehearsal(fails)
        # ⚠ READ BEFORE THE APPEND, or the delta compares this run against ITSELF and every warn
        # reads UNCHANGED for the wrong reason (`s241-D2`).
        prev_rec = _previous_rehearsal_record(repo)
        log_err = _rehearsal_log_append(repo, {
            "date": today.isoformat(), "kind": "rehearse" if rehearse else "wrap-open",
            "fails": len(fails), "structural": len(structural),
            "heals_at_wrap": len(heals), "warns": len(warns),
            "structural_names": [s[:120] for s in structural],
            # `s241-D2`: ~16 bytes per warn, and it is what makes NEW/CHANGED separable from
            # "the same 17 as yesterday". Bodies are NOT logged — this is an index, not a copy.
            "warn_sigs": ["%s:%s" % _warn_sig(w) for w in warns],
        })
        if log_err:
            warns.append(log_err)

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
        veto = selftest_write_veto(report)
        if veto:
            # ⛔ LOUD AND NAMED, never a silent skip: the caller asked for a write and did not get
            # one, and a wrap that believes it wrote its report is worse than one that failed.
            sys.stderr.write(veto + "\n")
        else:
            with open(report, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

    if rehearse:
        # TERSE BY DESIGN — the window pays for every printed line; the whole point of the
        # rehearsal is that the sandbox does the reading. Structural fails in full (they are
        # the deliverable), everything else as counts.
        # ★ `s241-D2` (D1 of the #241 ritual diet). What this print already was, MEASURED before
        # the change rather than inherited from the report that recommended it: the check-in's
        # rehearsal block is 3 lines / ~180 tape, NOT the 130-line 7,534-tape dump lane D
        # attributed to it — that figure is `--wrap`'s stdout (lane D's own probe ran
        # `cg.run(mode="wrap")`, its line 102) and is S7's subject, not D1's. So D1's saving is
        # NOT ~22,400/session; the honest number is in this lane's report. What was genuinely
        # MISSING and is added here is the second half of D1's clause: the warn NAMES, whenever
        # the warn set has moved since the last logged run. Until now a warn could appear,
        # disappear or change wording between two rehearsals and the only trace was a count.
        for i in structural:
            print(f"  ⛔ STRUCTURAL {i}")
        for i in heals:
            print(f"  ▫️  heals-at-wrap: {i[:100]}")
        moved, _same_line = _warn_delta_lines(warns, None if warns_full else prev_rec)
        if prev_rec and moved:
            print(f"  ⚠️  {len(moved)} warn(s) NEW or CHANGED since the "
                  f"{prev_rec.get('kind', '?')} record of {prev_rec.get('date', '?')} — named "
                  f"here because a moved warn that prints only as a count is invisible:")
            for i in moved:
                print(f"      · {re.sub(chr(10), ' ', i)[:160]}")
        n_prev = (prev_rec or {}).get("warns")
        drift = "" if n_prev is None else f" (was {n_prev} at the last logged run)"
        print(f"rehearsal [wrap-gate, early]: {len(structural)} STRUCTURAL fail(s) — fix NOW, "
              f"cheap · {len(heals)} heals-at-wrap (ritual steps 1/2) · {len(warns)} warn(s)"
              f"{drift} (run --wrap for bodies) · logged → {REHEARSAL_LOG}")
        return 1 if structural else 0
    for i in fails:
        print(f"  ❌ FAIL {i}")
    # ★ `s241-D2` (S7 of the #241 ritual diet): NEW or CHANGED warns print in full; the ones
    # that have not moved since the last logged run print as a count PLUS THEIR NAMES on one
    # line. Nothing goes unseen — only the repeated bodies stop being paid for. `--warns-full`
    # restores the old print in one flag, and the delta says which record it compared against,
    # so the suppression can never be mistaken for a clean run.
    _warn_full, _warn_one = _warn_delta_lines(warns, None if warns_full else prev_rec)
    for i in _warn_full:
        print(f"  ⚠️  WARN {i}")
    if _warn_one:
        print(f"  ⚠️  WARNS {_warn_one}")
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
    # ---- #74-D3: the % form is RETIRED — every %-form stamp now FAILS naming the legal forms.
    # The old ds-023 band fixtures (the twice-flipped 57% control and the 45/60/63 boundary
    # arms) went with the enforcement they proved; their history — the strongest single proof
    # that the #31 delegated enforcement was never Dave's — is preserved in the ledger § #36
    # and § ★ #74. One arm remains to pin the retirement itself:
    ("#74-D3: a %-form stamp — FAILS, naming the retirement and the legal forms",
     "pre-flight: fill 40% + job 12% + wrap 5% = 57% AMBER · reserve 15% ring-fenced\n", True),
    # ---- #73: the LEGAL REFUSAL (#62's remedy — PREFLIGHT_UNMEASURED_RE's header is the law).
    # All four arms were run as MUTATIONS against the live check before being written down.
    ("#73: exact legal refusal + reason — passes as a DECLARED gap (warns, no fail)",
     "> **pre-flight #72:** ⛔ NOT CAPTURED — UNMEASURED. No pre-flight was declared at the "
     "opener and none is reconstructed after the fact.\n", False),
    ("#73: a refusal NOT in the legal form — FAILS (the #71 wording, graded live at #72)",
     "> **pre-flight #71:** ⛔ NOT CAPTURED — no live pre-flight was declared this session.\n",
     True),
    ("#73: refusal AND numbers on one line — contradictory testimony, FAILS",
     "> **pre-flight #72:** ⛔ NOT CAPTURED — UNMEASURED. Though fill 40% + job 12% + wrap 5% "
     "= 57% AMBER.\n", True),
    ("#73: the legal glyphs with NO reason after the stop — FAILS (both ways means both ways)",
     "> **pre-flight #72:** ⛔ NOT CAPTURED — UNMEASURED.\n", True),
]


# ---- #56 — THE ABSOLUTE-STAMP FIXTURES. ⚠ Every one of these was run as a MUTATION before it
# was written down: the check was confirmed to go RED on the failing form and GREEN on the
# control. A fixture list assembled without that step asserts that the code does what its author
# intended, which is not the same as testing it [[gate-must-quote-what-it-forbids]].
_ABS_OK = ("pre-flight #56: boot 26,897 (disk 6,897 measured · harness ~20,000 est ±8,000) + "
           "job 45,000 est + wrap 20,000 est = 91,897 of 200,000 — GREEN\n")
PREFLIGHT_TOKEN_FIXTURES = [
    ("control — priced, in budget, all three terms labelled", _ABS_OK, False),
    # ⛔ #58, AND IT TOOK THE WHOLE GATE DOWN, NOT JUST THIS CHECK. The live #58 banner mentioned
    # a term in PROSE before stating it — "…before the job, and that is a LAPSE…" — and the old
    # `([\d,]+)` group matched the BARE COMMA, so `_n(',')` raised a bare ValueError and the wrap
    # printed a traceback instead of a verdict on any of its 39 checks. ★★ A CRASH IS NOT A FAIL.
    # This fixture is the mention-then-state shape, and it must stay GREEN with the real numbers
    # parsed: mutation-tested #58, both arms — restore `([\d,]+)` and it raises again.
    ("#58: a PROSE MENTION before the real term must not crash, and must not win",
     "pre-flight #58 (no band was written before the job, and that is a LAPSE): boot 30,633 "
     "measured + job 70,000 est + wrap 25,000 est = 125,633 of 200,000 — GREEN\n", False),
    # ★ THE D10 (c) PAIR, and it is the whole point of the rewrite. A term that is DECLARED
    # unobservable passes; the identical stamp with that term merely ABSENT fails. Silence is
    # the only thing being punished — which is what makes publishing cheaper than refusing.
    ("D10 (c): a DECLARED-unobservable term passes",
     "pre-flight #56: boot 26,897 measured + job unobservable (scope unruled) + wrap 20,000 est "
     "= 46,897 of 200,000 — GREEN\n", False),
    ("D10 (c): the SAME term silently absent FAILS",
     "pre-flight #56: boot 26,897 measured + wrap 20,000 est = 46,897 of 200,000 — GREEN\n", True),
    ("arithmetic that does not close FAILS",
     "pre-flight #56: boot 26,897 measured + job 45,000 est + wrap 20,000 est "
     "= 150,000 of 200,000 — GREEN\n", True),
    ("band mis-read against the ruled thresholds FAILS", _ABS_OK.replace("GREEN", "AMBER"), True),
    ("AMBER stated correctly passes",
     "pre-flight #56: boot 26,897 measured + job 120,000 est + wrap 30,000 est "
     "= 176,897 of 200,000 — AMBER\n", False),
    ("over the working budget, UNMARKED — FAILS",
     "pre-flight #56: boot 26,897 measured + job 150,000 est + wrap 30,000 est "
     "= 206,897 of 200,000 — RED\n", True),
    ("over the working budget, MARKED — allowed, warns",
     "pre-flight #56: boot 26,897 measured + job 150,000 est + wrap 30,000 est "
     "= 206,897 of 200,000 — RED · RESERVE SPEND — forked to Dave\n", False),
    # ⛔ THE ASYMMETRY THAT MATTERS: the marker buys the WORKING overrun and does NOT buy the
    # HARD one. Past 256,000 there is no published measurement of Dave's model to reason from,
    # and a receipt cannot manufacture evidence. Split the job or delegate it.
    ("past the HARD line — FAILS EVEN WHEN MARKED",
     "pre-flight #56: boot 26,897 measured + job 200,000 est + wrap 40,000 est "
     "= 266,897 of 200,000 — RED · RESERVE SPEND — forked to Dave\n", True),
    ("a stamp priced against a budget nobody ruled FAILS",
     _ABS_OK.replace("of 200,000", "of 500,000"), True),
    # ⚠ THE MIS-TARGET BITE, #56. Before the `#NN` widening, PREFLIGHT_RE skipped the live
    # banner and matched an ARCHIVED stratum instead. This fixture pins the live form.
    ("the LIVE banner form `pre-flight #NN:` is the line that gets checked", _ABS_OK, False),
    # ★★ THE HOUSE-STYLE FIXTURE — this is the ACTUAL first stamp, bold and all, and it FAILED
    # on its first run because the fixtures above are plain text. A gate tested only against the
    # form its author types is tested against the wrong corpus.
    ("the REAL bold-laden banner form parses (the #56 bite)",
     "> **pre-flight #56:** boot 26,897 (disk 6,897 **measured**, real · harness ~20,000 "
     "**est ±8,000**, `ds-025` item 1) + job 45,000 **est** + wrap 25,000 **est** "
     "= **96,897 of 200,000 — GREEN**.\n", False),
]


def selftest_preflight_tokens():
    """Bite-test the ABSOLUTE stamp (Dave #56). Controls green, every failing class red."""
    failures = []
    for name, text, should_fail in PREFLIGHT_TOKEN_FIXTURES:
        f_, _w, _n = check_preflight(text, label="fixture")
        if should_fail and not f_:
            failures.append(f"pre-flight/tokens [{name}]: expected FAIL, stayed green — "
                            f"the check does not bite")
        if not should_fail and f_:
            failures.append(f"pre-flight/tokens [{name}]: expected green, got {f_}")
    # the budget thresholds, pinned. Two DIFFERENT authorities and the pin records which is which.
    if (gauge.BUDGET_AMBER, gauge.BUDGET_WORKING, gauge.BUDGET_HARD) != (160_000, 200_000, 256_000):
        failures.append(
            f"budget = {(gauge.BUDGET_AMBER, gauge.BUDGET_WORKING, gauge.BUDGET_HARD)}, ruled "
            f"(160,000 / 200,000 / 256,000) at #56. WORKING is DAVE'S; HARD is SOURCED (93% "
            f"MRCR v2 at 256K); AMBER is derived at 80% of working. Re-dialling WORKING is his "
            f"word — updating this pin is part of doing it.")
    # ⛔ THE #53 GUARD, asserted rather than trusted: a budget under its own floor is unobeyable.
    # ⚠ PAIRED HALF OF #79-D1 (Dave: *"make it refuse"*). This reaches the gauge by
    # assert_budget_clears_floor() -> measure_boot() -> count(), and count() now RAISES
    # rather than returning a crude estimate. Bare, that raise would kill this 39+-check
    # gate mid-sweep and it would report NOTHING. [[a-crash-is-not-a-fail]]
    # ★ The refusal is recorded as a FAILURE, never waved through: an UNMEASURABLE floor is
    # not a cleared floor. UNKNOWN is never defaulted [[feedback-measuring-tool-must-not-guess]].
    try:
        failures += [f"budget floor: {x}" for x in gauge.assert_budget_clears_floor()]
    except gauge.MeasurementRefused as e:
        failures.append(
            f"budget floor: ⛔ UNMEASURABLE — the #53 guard could not run, because the gauge "
            f"refused to guess. This gate is REPORTING, not crashing, and the floor is "
            f"UNKNOWN rather than clear. Cause, as the gauge named it: {e}")
    # the U-shape note must reach every path — an instrument with no reader is ds-024's class.
    _f, _w, n_ = check_preflight(_ABS_OK, label="fixture")
    if not any("U-shaped" in x for x in n_):
        failures.append("pre-flight/tokens: the position note did not publish. Recall is weakest "
                        "in the MIDDLE of a window, which is where mid-session findings sit — "
                        "that is the cheaper lever than shrinking anything, and no session will "
                        "look it up unless the gate says it.")
    return failures


def selftest_gauge_refusal_seam():
    """⛔ THE PAIRED HALF OF #79-D1, TESTED AT THE SEAM — not at either end of it.

    Dave ruled the gauge must REFUSE. The risk that ruling creates does not live in the gauge;
    it lives HERE. A raise arriving inside a 39+-check sweep kills the sweep, and a gate that
    dies reports NOTHING — strictly worse than the estimate it replaced. So the subject under
    test is the HANDLER. [[a-crash-is-not-a-fail]] [[instrument-without-a-consumer]]
    """
    failures = []

    # (1) ⛔ GATE THE PRESENCE, NOT THE DRIFT. The whole pairing rests on MeasurementRefused
    # being catchable by `except Exception`. Re-parent it to BaseException — and SystemExit is
    # the standing precedent in this repo, so that is the direction the pull comes from — and
    # every paired handler still COMPILES while silently ceasing to catch.
    if not issubclass(gauge.MeasurementRefused, Exception):
        failures.append(
            "[gauge seam] gauge.MeasurementRefused is not a subclass of Exception. Every "
            "`except Exception` handler paired with it still compiles and silently stops "
            "catching — reinstating the crash #79-D1 was ruled to prevent.")

    # (2) THE BITE: make the floor call refuse, and prove this gate REPORTS rather than dies.
    real = gauge.assert_budget_clears_floor

    def _refuse(*_a, **_k):
        raise gauge.MeasurementRefused("tiktoken unavailable — REFUSING TO GUESS (fixture)")

    gauge.assert_budget_clears_floor = _refuse
    try:
        out = None
        try:
            out = selftest_preflight_tokens()
        except BaseException as e:      # noqa: BLE001 — catching the crash IS the measurement
            failures.append(
                f"[gauge seam] selftest_preflight_tokens() CRASHED instead of reporting when "
                f"the gauge refused: {type(e).__name__}: {e}")
        if out is not None:
            named = [x for x in out if "UNMEASURABLE" in x]
            if not named:
                failures.append(
                    "[gauge seam] the gauge refused and this gate returned NO failure naming "
                    "it — an UNMEASURABLE floor waved through as a CLEARED floor. UNKNOWN must "
                    "never default to OK [[feedback-measuring-tool-must-not-guess]].")
            elif len(named) != 1:
                failures.append(
                    f"[gauge seam] expected exactly ONE named failure for the refusal, got "
                    f"{len(named)} — a gate that reports one cause N times trains its reader "
                    f"to skim.")
            elif "REFUSING TO GUESS (fixture)" not in named[0]:
                failures.append(
                    f"[gauge seam] loud but NOT NAMED — the gauge's own stated cause did not "
                    f"survive into the report: {named[0]!r}")
    finally:
        gauge.assert_budget_clears_floor = real

    # (3) CONTROL. Without this, arm (2) passes just as well if the handler fires
    # unconditionally — a green that cannot distinguish the two states is an assertion.
    if any("UNMEASURABLE" in x for x in selftest_preflight_tokens()):
        failures.append(
            "[gauge seam] the refusal failure fires while the gauge is HEALTHY — the handler "
            "is reporting a state that did not occur.")

    return failures


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
    # ---- #74: FIRST-MATCH ATTRIBUTION arms. All four run as MUTATIONS before being written
    # down. The banner line is the LIVE `**#N**` form; the bare-stamp fixtures above never carry
    # it, which is itself the fifth arm (fixture text must be graded exactly as before).
    _B74 = "> ## ★ LATEST — 2026-08-01 (Sat **#74**, fixture)\n"
    _S = "> **pre-flight #{}:** ⛔ NOT CAPTURED — UNMEASURED. Fixture reason stated.\n"
    for name, text, should_fail in [
        ("#74 attribution: stamp tagged with the LATEST session — passes (control)",
         _B74 + _S.format(74), False),
        ("#74 attribution: OLDER session's stamp under a stampless LATEST — FAILS "
         "(the #72-graded-on-#71 defect)", _B74 + _S.format(73), True),
        ("#74 attribution: untagged stamp under a numbered LATEST — FAILS (unattributable)",
         _B74 + "> **pre-flight:** ⛔ NOT CAPTURED — UNMEASURED. Fixture reason stated.\n", True),
        ("#74 attribution: no numbered LATEST banner — bare stamp graded as before (fixture "
         "corpus unharmed)", _S.format(73), False),
    ]:
        f_, _w, _n = check_preflight(text, label="fixture")
        if should_fail and not f_:
            failures.append(f"pre-flight [{name}]: expected FAIL, check stayed green — "
                            f"the attribution check does not bite")
        if not should_fail and f_:
            failures.append(f"pre-flight [{name}]: expected green, got {f_}")

    # ---- #74-D3 (Dave): the ds-023 %-band selftest block that sat here — the band table
    # check, the reserve-addend arm, the receipt/stop-line/anti-habit/under-pricing bites and
    # the (45, 60, 63) pin — was RETIRED WITH THE ENFORCEMENT IT PROVED. What those arms
    # guarded (the escape-hatch receipt, the moving stop line, the anti-habit rule, the
    # under-pricing note) lives on in the TOKEN path and ITS fixtures/selftest; the history of
    # the twice-flipped 57% control and the #31 delegated-enforcement lesson is in the ledger
    # (§ #36, § ★ #74). One arm here pins the retirement: the %-form FAIL fixture in
    # PREFLIGHT_FIXTURES above, which names #74-D3 and the legal forms.

    return failures


FAT = " ".join(f"word{i}" for i in range(120))  # ~200 tk of line, for isolating the SIZE check
#   from the LINE check: a fixture that trips both proves neither (attribute-the-diff).


def _gm_fixture(do_first=10, sec_a=10, sec_c=10, with_b=False, strata_blocks=0,
                strata_pad=0, drop=(), stamp=None, fat_c=0, fat_a=0,
                fat_banner=0, banner_extra=None, stamp_a=None, ls_text=None, latest=True,
                strata_keys=None, title=True):
    """Synthetic GOOD-MORNING.md for the budget bites.

    `stamp=None` ⇒ a CORRECT stamp is computed for the finished text, so the green control is
    genuinely green rather than green by omission (attribute-the-diff: a control that passes for
    the wrong reason cannot license the fixtures that fail).

    M-set additions: `fat_banner` grows the banner region (M8) · `banner_extra` injects a banner
    line, which is how the M7 growth trigger's "a banner names §A" suppressor is bitten ·
    `stamp_a` overrides the stamped §A figure (a float to claim one, `False` to omit it).

    `strata_keys` ADDED #58 (STRATA_EXEMPT bites): an explicit list of session numbers, e.g.
    `[40, 41, 42]`, used for the `#### <date> #<N>` headings INSTEAD of the auto-generated
    `#0 #1 #2 …` sequence. Purely ADDITIVE — every existing caller leaves it `None` and gets
    byte-identical output to before this parameter existed; passing it is what lets a fixture
    name specific (e.g. exempt) session numbers rather than only sequential ones. When given,
    its length is what emits (so `strata_blocks` alone is no longer required alongside it)."""
    # ⛔ #61 — THE TITLE LINE IS NOT DECORATION IN THIS FIXTURE, IT IS LOAD-BEARING.
    # `affe15d` (#60) added `check_budgets`'s TITLE_LINE_RE assertion and did NOT teach this
    # fixture to satisfy it. Every green-expected budget bite then failed for a reason unrelated
    # to what it tests — 9 failures, ONE cause — and because `_build_all.py:52` runs
    # `--selftest` through the catch-all abort branch, the whole build DIED AT STEP 8 OF 75.
    # MEASURED, not traced: exit 1 in 6s; steps 9–75 never ran; CI runs `_build_all.py`.
    # ★ The gate that was added to make a rule bite bit the build instead, and nothing noticed
    # because #60 ran `--wrap` (which passes) and never ran `--selftest` or the build.
    # ⚠ `title=False` is how the ABSENT-title path is bitten deliberately — an absent title must
    # still fail loudly, per #60-D8. Do not remove that arm to make this fixture simpler.
    out = ["# Good morning", "SIZESTAMP", ""]
    if title:
        out.append("> **TITLE THE NEXT CHAT →** `Apollo - #N fixture (read _CHAIN.md ONLY)`")
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
        if strata_blocks or strata_keys:
            out.append("### ⏱ SESSION STRATA")
            # strata_keys=None reproduces the ORIGINAL sequence (`key = b`) exactly — existing
            # callers that only ever pass strata_blocks/strata_pad see byte-identical output.
            n_blocks = len(strata_keys) if strata_keys is not None else strata_blocks
            for b in range(n_blocks):
                key = strata_keys[b] if strata_keys is not None else b
                out += [f"#### 2026-07-2{b} #{key}"] + [f"s line {i}" for i in range(strata_pad)]
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
    # ★★ #49, FOUND BY open 15's OWN POSITIVE CONTROL, and it is the better half of that bite.
    # This second term read `chain {tk}K tape` from #34 until now — so the GREEN CONTROL that
    # licenses every fixture in `BUDGET_FIXTURES` was modelling the exact hand copy #45 retired,
    # and modelling it WRONG (it stamped the GM figure under a `chain` label). Fifteen sessions of
    # green controls asserted that a stamp carrying a hand chain figure is correct. #45's probe
    # named three fixture sites (`:1844`, `:1846`, `:2050`); the GENERATOR that mints them on every
    # default fixture was not among them — a survey of occurrences missed the thing producing them.
    # Now `corpus`, which is a real stamp field and is nobody's generated number.
    text = body.replace("SIZESTAMP", "> **size:** GM 0.00K tape · corpus 0.00K tape · measured x")
    for _ in range(3):  # converges: the stamp's own length barely moves the count
        tk, _m = measure_tokens(text)
        text = body.replace("SIZESTAMP", f"> **size:** GM {tk / 1000:.2f}K tape · {a_part}"
                                         f"corpus {tk / 1000:.2f}K tape · measured x")
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
    # #58: STRATA_EXEMPT bites. #40/#41/#42 are the CLOSED exempt list (ruling + reason at
    # STRATA_EXEMPT's own definition, ~line 198) — these three prove the exemption actually
    # exempts, that it does not become a blanket licence once a live block joins the stack, and
    # that the cap still bites past it. `strata stack 2 blocks deep` just above is fixture (d)
    # from the verification plan: two NON-exempt blocks (#0 #1) still FAIL, unchanged.
    ("strata: 3 exempt blocks only (#40/#41/#42, Dave #58) — must PASS",
     dict(strata_keys=[40, 41, 42], strata_pad=3), False),
    ("strata: 3 exempt + 1 live block — must PASS (cap 1 on the LIVE count)",
     dict(strata_keys=[40, 41, 42, 99], strata_pad=3), False),
    ("strata: 3 exempt + 2 live blocks — must FAIL (cap 1 still bites past the exemption)",
     dict(strata_keys=[40, 41, 42, 99, 100], strata_pad=3), True),
    ("no size stamp",                                      dict(stamp="(no stamp here)"), True),
    # ⚠ #49: both of these said `chain` until open 15 was enacted. They are EXPECTED-fail fixtures,
    # so the new ban would not have turned them red — it would have made them fail for a reason
    # their own names do not state, which is how a suite stops meaning what it says. Re-labelled
    # `corpus` so each still fails for exactly the defect it is named after.
    ("size stamp STALE (claims 0.10K)",
     dict(stamp="> **size:** GM 0.10K tk · corpus 0.10K tk · measured x"), True),
    ("size stamp with no K (25618 must not read as 25.6M)",
     dict(stamp="> **size:** GM 25618 tk · corpus 1 tk"), True),
    # D7-as-amended: the SIZE budget, isolated from the LINE caps by fat lines rather than many
    # lines — a fixture that trips both checks at once proves neither of them.
    # ⛔ FLIPPED True→False 2026-07-29 #39 WITH the block's withdrawal — flag and fixture move as a
    # pair, the standing discipline in this file. This fixture is NOT deleted: it still proves the
    # region is MEASURED, and it is the bite that turns red the moment a block is restored, which is
    # exactly what Thursday's chain-cap swap will do. Keeping it is how the swap gets caught by a test
    # rather than by a session noticing.
    ("compactable over size WARN, block withdrawn #39 — advisory, must NOT fail",
     dict(sec_c=5, fat_c=80), False),
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
    # ⛔ PIN MOVED 2026-07-29 #39, WITH the ruling, as a pair. The WARN value 8000 is UNCHANGED and
    # still Dave's D7 amendment; what moved is `compactable_block`: 12,000 (derived cap×1.5) → None.
    # ⚠ `None` is a DECLARED ADVISORY STATE, not an absent value — the distinction matters, because
    # a missing key would read as an oversight and this is a ruling. Restoring a block is Dave's, and
    # moving this pin is part of doing it.
    if SIZE_BUDGET_TK != {"compactable": 8000, "compactable_block": None}:
        failures.append(f"SIZE_BUDGET_TK = {SIZE_BUDGET_TK}, ruled "
                        f"{{'compactable': 8000, 'compactable_block': None}} (#39, block WITHDRAWN "
                        f"— the region is retrieval surface, not cold-start cost) — re-dialling is "
                        f"Dave's, and updating this pin is part of doing it")
    return failures


def selftest_strata_exempt():
    """MUTATION-TEST for STRATA_EXEMPT (Dave #58). A green here must be an assertion that CAN
    go red, not one that cannot — that is the only way it proves the exemption is load-bearing
    rather than the cap having silently stopped biting for some unrelated reason. Mutates the
    module-level set, asserts RED, restores it inside `finally` (a failed assertion must never
    leave every test that runs after this one in the same process mutated), then asserts GREEN
    again on the restored set.

    ⚠ THE BASE FIXTURE IS 3 EXEMPT + 1 LIVE, NOT 3 EXEMPT ALONE, AND THE ARITHMETIC IS WHY.
    With only #40/#41/#42 present, live_blocks = 3 − 3 = 0 under the true set; dropping one key
    from STRATA_EXEMPT moves it to 3 − 2 = 1, which is STILL <= STRATA_MAX_BLOCKS(1) — a green
    that a single-key mutation cannot disturb, which would prove nothing (caught by this test
    itself on its first run: the naive 3-block fixture stayed green after the mutation). Adding
    one live block first (#99) means the SAME one-key mutation moves live_blocks from 4−3=1
    (in cap) to 4−2=2 (over cap) — the mutation a reviewer would actually write, made to bite."""
    failures = []
    fixture = _gm_fixture(strata_keys=[40, 41, 42, 99], strata_pad=3)
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write(fixture)

        # ---- baseline: 3 exempt + 1 live, unmutated STRATA_EXEMPT, must be GREEN (cap 1, live
        # count 1), and the note must actually NAME all three exempt blocks — an exemption that
        # is not reported is silent, which is exactly what #58 ruled against ("measured and
        # reported, never charged", mirroring SECTION_EXEMPT).
        f_, _w, n_ = check_budgets(td)
        if f_:
            failures.append(f"strata-exempt: baseline (unmutated, 3 exempt + 1 live) was not "
                            f"green — {f_}")
        if not any("#40" in x and "#41" in x and "#42" in x and "EXEMPT" in x for x in n_):
            failures.append(f"strata-exempt: baseline published no note naming all three exempt "
                            f"blocks. Got notes={n_}")

        # ---- MUTATION: drop #42 from the closed list. The fixture is unchanged (still exactly
        # #40/#41/#42/#99) — if the exemption is load-bearing, one fewer exempt key must turn a
        # block that used to be exempt into a live one and trip the cap (2 live vs cap 1).
        global STRATA_EXEMPT
        original = STRATA_EXEMPT
        try:
            STRATA_EXEMPT = original - {42}
            f_, _w, _n = check_budgets(td)
            if not any("strata" in x.lower() for x in f_):
                failures.append(f"strata-exempt MUTATION: removing #42 from the exempt set did "
                                f"NOT turn the 4-block fixture red — got fails={f_}. A green "
                                f"that cannot be made red is an assertion, not evidence")
        finally:
            STRATA_EXEMPT = original

        # ---- RESTORE: same fixture, original set — must be green again, proving the red above
        # was caused by the mutation and not by some other side effect of the test itself.
        f_, _w, _n = check_budgets(td)
        if f_:
            failures.append(f"strata-exempt: restoring the original STRATA_EXEMPT did not "
                            f"return the fixture to green — {f_}")
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


def selftest_bare_token():
    """open 25 (#51) — `BARE_TOKEN_RE` proved BOTH ways: it bites, and it stops where it should.

    ★ THE POSITIVE CONTROL LEADS, on the house rule: a check that fires on everything is noise
    and gets routed around within one wrap, and a failure-only suite reads green after a revert
    that deletes the comparison entirely (#32's lesson, restated at `:2070`)."""
    failures = []

    def _open25(warns):
        return [x for x in warns if "open 25" in x]

    with tempfile.TemporaryDirectory() as td:
        # ---- 1. POSITIVE CONTROL. The default fixture stamps every field in `tape` (`:2043`).
        _f, w, _n = _warns_for(td)
        if _open25(w):
            failures.append(f"open 25: an ORDINARY, fully unit-named stamp warned — the check "
                            f"fires on everything, which makes it noise. Was: {_open25(w)}")

        # ---- 2. THE BITE, on the forms that were REALLY THERE. Both taken from `GOOD-MORNING.md`'s
        # live `size:` stamp as it stood at build time (#51), not invented — the same discipline
        # `CHAIN_STAMP_RE` uses when it takes its forms from `git log` rather than imagination.
        for bare_form, figure in (("§A **4.2K (EXEMPT)**", "4.2K"),
                                  ("corpus **58.7K**", "58.7K")):
            _f, w, _n = _warns_for(
                td, stamp=f"> **size:** GM 1.00K tape · {bare_form} · measured x")
            hit = next(iter(_open25(w)), None)
            if hit is None:
                failures.append(f"open 25: the stamp form {bare_form!r} did NOT warn. This is one "
                                f"of the two forms live in GM's stamp the day the check was built, "
                                f"so a regex that misses it enforces nothing that was actually "
                                f"wrong")
            elif figure not in hit:
                failures.append(f"open 25: the warn for {bare_form!r} does not QUOTE the offending "
                                f"figure {figure!r}. A count is not a measurement and a gate that "
                                f"only forbids teaches nothing — name the thing. Was: {hit}")
            elif "ADDITION" not in hit:
                failures.append(f"open 25: the warn for {bare_form!r} does not say the remedy is "
                                f"ADDITION. Discharge here NEVER requires a cut, and a warn that "
                                f"reads as 'remove something' invites the one motion "
                                f"[[home-by-addition-then-cut]] forbids. Was: {hit}")

        # ---- 3. ★★ THE SCOPE CONTROL, and it is the load-bearing bite — the GM:488 lesson
        # generalised. GM's BODY is full of true, dated records of what things measured; a stamp
        # ban that escaped into body prose would forge defects out of correct history. Same
        # string, outside the stamp: must pass clean.
        _f, w, _n = _warns_for(td, banner_extra="> - boot read the chain only (**~4.1K**, not GM's)")
        if _open25(w):
            failures.append(f"open 25 SCOPE: a bare figure in BANNER PROSE warned — the check has "
                            f"escaped the `size:` stamp and is now judging body prose, which would "
                            f"forge a defect out of GM's own true history. Was: {_open25(w)}")

        # ---- 4. ★★ THE USE/MENTION CONTROL — and it is the one that taught #51 something.
        #
        # It was WRITTEN as a self-bite control: feed the gate's own warn text back through its own
        # regex and assert it comes back clean, on the theory that a ban tripping on the sentence
        # explaining it is open 23's false-positive risk in sharper form. ⛔ IT FIRED ON THE FIRST
        # RUN, AND IT WAS RIGHT TO. The warn QUOTES the offending figure (`'58.7K'`) because bite 2
        # above REQUIRES it to — a gate that will not name the thing it found teaches nothing. So
        # the message necessarily contains a bare figure, and the regex cannot tell that it is
        # MENTIONING one rather than USING one.
        #
        # ★ THE FINDING, and it is open 24's shape one level down: a syntactic ban cannot
        # distinguish use from mention, so it can never be made safe by making it cleverer. What
        # makes it safe is SCOPE — the check reads `stamp.group(1)` and nothing else, so the warn
        # text is unreachable by construction (bite 3 proves the stopping point). ⇒ The honest test
        # is not "is the message clean" but the two below. Laundering the message to get green here
        # would have removed the quote and broken bite 2 — a false fix that reads as a pass.
        _f, w, _n = _warns_for(td, stamp="> **size:** GM 1.00K tape · corpus **58.7K** · measured x")
        msg = next(iter(_open25(w)), "")
        # (a) INVERTED BITE. The message MUST still contain a matchable figure, because it must
        # quote the defect. If this ever goes clean, someone has "fixed" the self-bite by deleting
        # the quotation — which silently guts the gate's usefulness while looking like tidying.
        if msg and not BARE_TOKEN_RE.search(msg):
            failures.append("open 25 USE/MENTION: the warn text no longer contains the bare figure "
                            "it is reporting. That is not the check getting safer — it means the "
                            "quotation was removed, and a gate that will not name what it found is "
                            "the thing bite 2 exists to prevent. Restore the quote; the safety here "
                            "comes from SCOPE, never from laundering the message.")
        # (b) THE REAL SAFETY PROPERTY, asserted rather than assumed: the check judges the stamp
        # ONLY. Pasted into a stamp — the one way this text could ever reach the scope — the warn
        # SHOULD flag, and that is correct behaviour, not a self-bite.
        # ⚠ the window is taken AROUND the regex's own match, not off the front of the string: the
        # first draft sliced `msg[:80]`, which stops before the quoted figure, so the paste carried
        # no bare figure and the bite failed for a reason that had nothing to do with the property
        # under test. A control that tests the wrong string is not a control [[attribute-the-diff]].
        _m = BARE_TOKEN_RE.search(msg) if msg else None
        _window = msg[max(0, _m.start() - 30):_m.end() + 2] if _m else ""
        _f, w2, _n = _warns_for(td, stamp=f"> **size:** GM 1.00K tape · {_window} · measured x")
        if msg and not _open25(w2):
            failures.append("open 25 USE/MENTION: the gate's own warn text, pasted INTO a stamp, "
                            "did not flag. The check must judge its own words by the same rule as "
                            "anyone else's once they enter its scope — an exemption for the gate's "
                            "own prose is how a rule stops applying to the thing that wrote it.")

        # ---- 5. UNIT COVERAGE. Every accepted word must actually suppress, or the remedy the warn
        # prescribes fails for whoever follows it — a gate that names a fix it does not honour.
        for unit in BARE_TOKEN_UNITS:
            _f, w, _n = _warns_for(
                td, stamp=f"> **size:** GM 1.00K tape · corpus **58.7K {unit}** · measured x")
            if _open25(w):
                failures.append(f"open 25: the unit word {unit!r} did NOT suppress the warn, but "
                                f"the warn text OFFERS it as the remedy. Following this gate's own "
                                f"advice would leave it still firing")

        # ---- 6. THE NARROWING IS PINNED, NOT JUST COMMENTED. `K` is required, so a bare `4,917`
        # passes. That is open 23's limitation inherited knowingly, and it is asserted HERE so that
        # widening the regex trips a bite instead of silently changing the check's scope
        # [[gate-glob-scope-rule]]: a rule is only as wide as the thing that enforces it.
        _f, w, _n = _warns_for(td, stamp="> **size:** GM 1.00K tape · corpus 4,917 · measured x")
        if _open25(w):
            failures.append("open 25 SCOPE: a bare `4,917` (no `K`) warned. That may well be an "
                            "IMPROVEMENT — but it is a WIDENING of open 23's declared scope, and "
                            "the comment above still tells the next reader it passes. Re-read that "
                            "comment and open 23 before deleting this bite.")

    return failures


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

    # ---- ds-023 stop line (#54). ★ MUTATION-TESTED BOTH WAYS, because a presence check that has
    # never been seen to go red is an assertion about the corpus, not a test of the gate.
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "knowledge"), exist_ok=True)
        _rb = os.path.join(td, "knowledge", "_RUNBOOK-context-gauge.md")
        _cr = os.path.join(td, "knowledge", "_RUNBOOK-capture-ritual.md")
        with open(_rb, "w", encoding="utf-8") as f:
            f.write("stop line is 60 − the priced wrap\n60 is where the wrap has FINISHED\n")
        with open(_cr, "w", encoding="utf-8") as f:
            f.write("run it at 60 − the priced wrap\n")
        f_, n_ = stop_line_consistency(td)
        if f_:
            failures.append(f"ds-023 stop line: both homes state the ruling and the check still "
                            f"failed ({f_})")
        if not any("all 2 trigger homes" in x for x in n_):
            failures.append("ds-023 stop line: green path did not publish the homes count")
        # MUTATION: edit the ruling back out of ONE home — the exact #54 regression.
        with open(_cr, "w", encoding="utf-8") as f:
            f.write("Also run it mid-session when the context gauge reads Red (>=60%).\n")
        f_, _n = stop_line_consistency(td)
        if not f_ or "capture-ritual" not in f_[0]:
            failures.append("ds-023 stop line: the ruling was edited out of the capture ritual "
                            "and the check stayed GREEN — this is the #54 defect returning, and "
                            "a presence gate that cannot go red is not a gate")
        # ⚠ AND THE USE/MENTION CONTROL: prose that QUOTES the wrong form in order to correct it
        # must still pass. A ban-shaped gate fails this; that is why this one is presence-shaped.
        with open(_cr, "w", encoding="utf-8") as f:
            f.write("THIS LINE USED TO SAY 'run it when the gauge reads Red (>=60%)' and that "
                    "was WRONG. The trigger is 60 − the priced wrap.\n")
        f_, _n = stop_line_consistency(td)
        if f_:
            failures.append(f"ds-023 stop line: correcting prose that QUOTES the wrong form was "
                            f"refused ({f_}) — use/mention, open 24's trap, in a new place")

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


def selftest_subs_line():
    """★ #168 bites for the OPTIONAL `subs` line. The POSITIVE cases lead — including the
    ABSENT case, which is the one a revert would silently break: a check that fails an absent
    optional line is worse than no check, because it would force wraps to INVENT figures."""
    failures = []

    def _log(td, body):
        os.makedirs(os.path.join(td, "notes"), exist_ok=True)
        with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
            f.write(body)
        return td

    _HEAD = "# log\n\n#### 2026-08-13 #168\n> **post-mortem #168:** body.\n"

    # ---- 1. ABSENT ⇒ PASS, and it must SAY it passed (a silent pass is indistinguishable
    # from a dead check).
    with tempfile.TemporaryDirectory() as td:
        f_, n_ = gauge_log_subs_line(_log(td, _HEAD))
        if f_:
            failures.append(f"subs-line: an ABSENT optional line FAILED ({f_}) — absence is "
                            f"legal by ruling and must never be defaulted into a figure")
        if not any("LEGAL and NOT" in x for x in n_):
            failures.append("subs-line: the absent case said nothing — a check that is silent "
                            "when it succeeds cannot be told from one that never ran")

    # ---- 2. VALID lines ⇒ PASS. Both grouped and ungrouped N, bare and quoted/bolded.
    for good in ("subs 128,400 tokens (n=3)\n",
                 "subs 940 tokens (n=1)\n",
                 "> **subs 128,400 tokens (n=3)**\n"):
        with tempfile.TemporaryDirectory() as td:
            f_, n_ = gauge_log_subs_line(_log(td, _HEAD + good))
            if f_:
                failures.append(f"subs-line: the VALID line {good.strip()!r} failed ({f_}) — a "
                                f"gate that rejects the ruled form teaches wraps to omit it")
            if not any("parses" in x for x in n_):
                failures.append(f"subs-line: {good.strip()!r} parsed but published no note")

    # ---- 3. MALFORMED ⇒ NAMED FAIL, one class per bite [[mutation-tests-the-clause-not-the-feature]]
    bad = [
        ("bad number (not an integer)", "subs 12.4K tokens (n=3)\n", "MALFORMED"),
        ("no number at all", "subs tokens (n=3)\n", "MALFORMED"),
        ("missing n= count", "subs 128,400 tokens\n", "MALFORMED"),
        ("n= present but empty", "subs 128,400 tokens (n=)\n", "MALFORMED"),
        ("count not a number", "subs 128,400 tokens (n=three)\n", "MALFORMED"),
        ("unit word dropped", "subs 128,400 (n=3)\n", "MALFORMED"),
        ("zero tokens — a claim, not an absence", "subs 0 tokens (n=3)\n", "non-positive"),
        ("zero subs — a claim, not an absence", "subs 128,400 tokens (n=0)\n", "non-positive"),
        ("⛔ the word `job` — _JOB_RE contamination",
         "subs job 128,400 tokens (n=3)\n", "CONTAMINATION"),
        ("⛔ `job` in a trailing gloss is still swept",
         "subs 128,400 tokens (n=3) — excludes job window\n", "CONTAMINATION"),
    ]
    for name, line, want in bad:
        with tempfile.TemporaryDirectory() as td:
            f_, _n = gauge_log_subs_line(_log(td, _HEAD + line))
            if not f_:
                failures.append(f"subs-line [{name}]: expected FAIL, stayed green — "
                                f"{line.strip()!r} would be written and believed")
            elif not any(want in x for x in f_):
                failures.append(f"subs-line [{name}]: failed, but not with the {want} refusal — "
                                f"got {f_}")
            elif not any(_SUBS_EXPECTED in x for x in f_):
                failures.append(f"subs-line [{name}]: the refusal does not QUOTE the expected "
                                f"form, so it names a defect without naming the repair")

    # ---- 4. THE CONTAMINATION IS PROVED AGAINST THE REAL DOWNSTREAM REGEX, not a paraphrase of
    # it. If gen_dashboard's `_JOB_RE` is ever widened/narrowed, this bite is what notices that
    # this gate's scope no longer matches the thing it exists to protect.
    _job_re = re.compile(r"\bjob ([0-9][0-9,]{3,})\b")
    if not _job_re.search("subs job 128,400 tokens (n=3)"):
        failures.append("subs-line: the `job` bite above no longer models gen_dashboard's "
                        "_JOB_RE — re-read gen_dashboard.py:332 before trusting this gate's "
                        "containment claim [[attribute-the-diff]]")
    if _job_re.search("subs 128,400 tokens (n=3)"):
        failures.append("subs-line: a WELL-FORMED subs line matches gen_dashboard's _JOB_RE — "
                        "the ruled form itself contaminates the effort corpus, which is a "
                        "defect in the FORM, not in this gate. Escalate; do not patch here.")
    return failures


def selftest_unkeyed():
    """ds-022 (d) bites (#55). The POSITIVE case leads, on the same reasoning as the suite
    above: a suite that only proves failures reads GREEN after a revert that deletes the
    comparison entirely, which is #32's lesson and the reason ds-019 was withdrawn.

    ★ THE FIXTURE IS THE HISTORICAL CASE, not an invented one. Bites 1 and 2 are #40 with and
    without its key — the same two lines, one edit apart — so the suite tests the defect that
    actually happened rather than a tidier cousin of it. #54's `roll_2f` fixture had to be
    rebuilt as a sandwich for the same reason: a fixture that cannot distinguish a half-fix
    from a fix reads green on the half-fix."""
    failures = []

    def _log(td, body):
        os.makedirs(os.path.join(td, "notes"), exist_ok=True)
        with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
            f.write(body)
        return td

    # #40's testimony, verbatim in shape from notes/_GAUGE-LOG.md lines 403–407.
    T40 = ("**tape/bill PAIR #40 (ds-021 (c) — the standing per-wrap log entry).** Measured…\n"
           "\n**⛔ META #40 — `roll_2f` FOR #38 IS REFUSED.** The chronological guard…\n")

    with tempfile.TemporaryDirectory() as td:
        _log(td, "# log\n\n#### 2026-07-29 #40 — Opus solo\n\n" + T40)
        f_, n_ = unkeyed_testimony(td)
        if f_:
            failures.append(f"ds-022 (d): KEYED testimony failed ({f_}) — the check fires on the "
                            f"good case, which is the state every compliant wrap is in, and it "
                            f"would be routed around within one session")
        if not any("every one is accounted for" in x for x in n_):
            failures.append("ds-022 (d): the passing case said NOTHING. A check that is silent "
                            "when it succeeds cannot be told apart from a dead one — and this "
                            "one is new, so nobody has a prior for what its green looks like")

    with tempfile.TemporaryDirectory() as td:
        # ★★ THE DEFECT ITSELF: the identical testimony with the key removed. This is the state
        # the live file was in from #40 until the retroactive patch — thirteen sessions.
        _log(td, "# log\n\n#### 2026-07-29 #39 — Opus\npost-mortem\n\n" + T40)
        f_, _n = unkeyed_testimony(td)
        if not any("PRESENT BUT UNKEYED" in x for x in f_):
            failures.append("ds-022 (d): testimony with NO key did not fail — this is the fourth "
                            "state itself, the one Dave ruled UNREACHABLE at #54, and the whole "
                            "reason this function exists")
        if any("HOLE #40" in x and "Do NOT declare" not in x for x in f_):
            failures.append("ds-022 (d): the remedy invited a `HOLE #40` line. HOLE is a POSITIVE "
                            "claim that the session wrote nothing, the testimony above disproves "
                            "it, and ds-022 (a)'s remedy line inviting exactly this is what #41 "
                            "refused to obey. A gate must not talk a session into a forgery")

    with tempfile.TemporaryDirectory() as td:
        # The escape hatch has to work HERE too, or a session that legitimately wrote no stratum
        # but did leave a META note can never close.
        _log(td, "# log\n\n#### 2026-07-29 #39 — Opus\nx\n\n**HOLE #40 — no stratum.**\n\n" + T40)
        f_, _n = unkeyed_testimony(td)
        if f_:
            failures.append(f"ds-022 (d): a DECLARED HOLE still failed ({f_}) — without the hatch "
                            f"this blocks correct behaviour, and a gate that fails on correct "
                            f"behaviour teaches sessions to fake blocks")

    with tempfile.TemporaryDirectory() as td:
        # ★ THE DISCRIMINATION BITE. Prose ABOUT a session is not that session TESTIFYING, and
        # telling them apart is the only thing the regex anchoring buys. Verbatim from line 560.
        _log(td, "# log\n\n#### 2026-07-29 #39 — Opus\nx\n\n"
                 "**RAISED AT #41, OPEN THIRTEEN SESSIONS, SETTLED THIS WINDOW.** The state…\n")
        f_, _n = unkeyed_testimony(td)
        if any("PRESENT BUT UNKEYED" in x for x in f_):
            failures.append("ds-022 (d): PROSE about #41 was classified as #41 TESTIFYING. This "
                            "is substring-vs-structure for the fourth time in this file (#35's "
                            "usage probe, ds-016's index, #37's banner regex) — the label must "
                            "be the token immediately before the number, not merely nearby")
        if not any("UNCLASSIFIED MARKER" in x for x in f_):
            failures.append("ds-022 (d): an unrecognised bold-lead line naming an UNACCOUNTED "
                            "session passed silently. Refusing to guess must mean refusing, not "
                            "ignoring")

    with tempfile.TemporaryDirectory() as td:
        # ★★ THE ANTI-BLINDNESS BITE, and the one that makes TESTIMONY_LABELS safe to be a list.
        # A marker type nobody has invented yet must not be a free pass.
        _log(td, "# log\n\n#### 2026-07-29 #39 — Opus\nx\n\n**FROBNICATE #99 — a new marker.**\n")
        f_, _n = unkeyed_testimony(td)
        if not any("UNCLASSIFIED MARKER" in x for x in f_):
            failures.append("ds-022 (d): a NEW marker label for an unkeyed session passed — the "
                            "enumerated vocabulary has become a blind spot, which is the exact "
                            "failure [[scope-blindness-gate-vocabulary]] names. Enumerate and "
                            "fail loud, never enumerate and hope")

    with tempfile.TemporaryDirectory() as td:
        # ⚠ AND THE COST BITE. The unclassified arm must stay SILENT about accounted sessions,
        # or it emits two fails against today's committed, correct record every wrap — and a
        # gate that cries on correct state is one nobody reads. [[instrument-without-a-consumer]]
        _log(td, "# log\n\n#### 2026-07-29 #41 — Opus\nx\n\n"
                 "**RAISED AT #41, OPEN THIRTEEN SESSIONS.** The state…\n")
        f_, _n = unkeyed_testimony(td)
        if f_:
            failures.append(f"ds-022 (d): prose about an ACCOUNTED session raised {len(f_)} "
                            f"fail(s) ({f_}) — the check must be free on a clean file or it is "
                            f"noise, and noise is how a blocking gate gets disarmed")

    with tempfile.TemporaryDirectory() as td:
        f_, n_ = unkeyed_testimony(td)
        if f_ or not any("UNMEASURED" in x for x in n_):
            failures.append("ds-022 (d): a MISSING _GAUGE-LOG.md did not announce itself as "
                            "UNMEASURED — an absent file is not a clean file")

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
        # ⚠ #49: this fixture read `· chain 1.00K tk ·` until open 15 was enacted, and it was one of
        # the three fixture-only `chain`-near-`stamp` strings #45's probe found. It now says
        # `corpus`, because the legacy UNIT is what this bite is about and `GM 1.00K tk` exercises
        # it alone. Changed rather than left: a fixture that trips a fail no bite asserts is a
        # silent tolerance, and the chain string now belongs to the M10 STAMP BITE, which owns it.
        _f, w_, _n = _warns_for(td, stamp="> **size:** GM 1.00K tk · corpus 1.00K tk · measured x")
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


def selftest_cross_instrument_units():
    """ds-021 (C) bites — RULED #81-D1 (Dave), with his condition attached: *"be careful, i want
    rigorousness, check for peripheral effects."*

    ★ Every bite below fails for a DISTINCT reason, and each one is MUTATION-TESTED by being
    re-enacted against a fixture that should trip it. A suite where one broken assumption turns
    every check red proves only that something is wrong; it cannot say WHAT, and the next
    session re-diagnoses it from scratch — which is the #80 defect wearing a test's clothes.
    """
    failures = []

    # ---- 1. POSITIVE CONTROL FIRST. Prove the audit passes on the LIVE repo before proving it
    # can fail — a failure-only suite reads green after a revert that deletes the comparison.
    live_f, live_w = unit_vocabulary_audit(REPO)
    if live_f:
        failures.append(f"ds-021 (C): the live repo FAILS its own unit audit ({live_f[0]}) — "
                        f"the registry and the code have diverged")
    # ⛔ #82-D1 REPLACED THIS BITE RATHER THAN DELETING IT, and the distinction matters. Until
    # this session the two checks here read: *the audit MUST warn, and it must name
    # `_capture_gate.py` as the estimate-only measurer.* Both were correct — this file WAS the
    # ds-021 defect. Dave's #82-D1 fixed the defect, so a check pinned to its presence would
    # fail forever on a repo that had done the right thing. ★ THE OLD BITE IS NOT LOST: it is
    # INVERTED. What must now be true is the stronger claim — this file is registered `real` AND
    # the registry's word is VERIFIED against source, never trusted from the table.
    # [[invariant-cannot-discriminate-reversal]]: assert the DELTA, then re-enact the OLD ruling
    # to prove the new check can still bite. The re-enactment is bite 3 below.
    _tier, _why = MEASURERS["_capture_gate.py"]
    if _tier != "real":
        failures.append(f"#82-D1: `_capture_gate.py` is registered {_tier!r}, not 'real' — Dave "
                        f"ruled the native counter wired at #82; a registry that disagrees with "
                        f"the ruling is the ds-021 defect pointing the other way")
    _self_src = open(os.path.join(REPO, "knowledge", "_capture_gate.py"),
                     encoding="utf-8").read()
    if not _produces_real_tier(_self_src):
        failures.append("#82-D1: this file is registered 'real' but its SOURCE contains no "
                        "RETURN of the form `(…, 'real')` — the registry's word is never "
                        "trusted, and a table claiming a tier the code cannot produce is worse "
                        "than a declared gap")
    # ★ THE STRUCTURE-vs-TEXT BITES. Each re-enacts a state where the OLD regex read GREEN and
    # the code was wrong — [[invariant-cannot-discriminate-reversal]]. Without these,
    # `_produces_real_tier` is a green that cannot fail.
    if _produces_real_tier('def _tier_of(m):\n    return "real"\n'):
        failures.append("#82-D1: a CLASSIFIER returning the bare word 'real' satisfied the "
                        "real-tier check — this is the exact mutation that did NOT bite at #82 "
                        "and let a file with its measurer removed still read as capable")
    if _produces_real_tier('x = \'    return n, "real"\\n\'   # a bite FIXTURE, not code\n'):
        failures.append("#82-D1: a STRING LITERAL shaped like a real return satisfied the check "
                        "— a test fixture would then certify the thing it is a fixture for")
    if not _produces_real_tier('def m(t):\n    return 7, "real"\n'):
        failures.append("#82-D1: a genuine `return n, 'real'` producer did NOT satisfy the "
                        "check — the structure rule is too tight and every real tier now reads "
                        "as absent, which fails the repo for doing the right thing")
    try:
        _produces_real_tier("def broken(:\n")
        failures.append("#82-D1: an UNPARSEABLE source did not raise — it would be graded by "
                        "silence, and a file nothing can read is not a file that passed")
    except SyntaxError:
        pass
    if any("_capture_gate.py" in w for w in live_w):
        failures.append("#82-D1: the audit still WARNS about `_capture_gate.py` after the real "
                        "tier landed — either the fix did not take or the audit is reading a "
                        "stale registry, and both publish an estimate wearing a measurement's "
                        "clothes")

    # ---- 2. THE UNREGISTERED-MEASURER BITE. This is the half that catches the NEXT instrument,
    # and it is the entire reason Dave chose (C) over (A), (B) or (D).
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        # Copy the registered files' *signatures* only — a fixture repo, not a clone.
        for fn in MEASURERS:
            tier, _ = MEASURERS[fn]
            body = 'get_encoding("cl100k_base")\n'
            if tier == "real":
                body += 'def f():\n    return n, "real"\n'
            with open(os.path.join(k, fn), "w", encoding="utf-8") as fh:
                fh.write(body)
        f_clean, _w = unit_vocabulary_audit(td)
        if f_clean:
            failures.append(f"ds-021 (C): a fixture matching the registry exactly still FAILED "
                            f"({f_clean[0]}) — the audit cannot be satisfied from a correct "
                            f"state, which is the ds-022 class (a gate that forbids a legal "
                            f"configuration)")
        # now add an interloper — a new file that counts tokens and declares nothing
        with open(os.path.join(k, "_new_instrument.py"), "w", encoding="utf-8") as fh:
            fh.write('enc = get_encoding("cl100k_base")\n')
        f_new, _w = unit_vocabulary_audit(td)
        if not any("_new_instrument.py" in x and "UNREGISTERED" in x for x in f_new):
            failures.append("ds-021 (C): a NEW cl100k counting site was not caught as "
                            "UNREGISTERED — this bite IS the ruling's purpose; without it the "
                            "gate only describes today's defect and catches no future one")

    # ---- 3. THE ROTTED-PIN BITE. A registry entry whose file stopped counting is a green that
    # cannot fail — #78's P0 was exactly an aged pin, and the red there was the reader working.
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "knowledge"))
        with open(os.path.join(td, "knowledge", "_gauge_tokens.py"), "w", encoding="utf-8") as fh:
            fh.write('get_encoding("cl100k_base")\ndef f():\n    return n, "real"\n')
        f_rot, _w = unit_vocabulary_audit(td)
        if not any("_capture_gate.py" in x and "no longer counts" in x for x in f_rot):
            failures.append("ds-021 (C): a registry entry pointing at a file that no longer "
                            "counts tokens did NOT fail — stale pins are how a suite stays "
                            "green across a deletion")

    # ---- 4. THE LYING-REGISTRY BITE. `real` is VERIFIED against source, never trusted from the
    # table. A table that can lie about the code launders an estimate into a measurement.
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        for fn in MEASURERS:
            with open(os.path.join(k, fn), "w", encoding="utf-8") as fh:
                fh.write('get_encoding("cl100k_base")\n')   # NB: no `return … "real"` anywhere
        f_lie, _w = unit_vocabulary_audit(td)
        if not any("claims" in x and "REAL tier" in x for x in f_lie):
            failures.append("ds-021 (C): MEASURERS claimed a REAL tier for a file whose source "
                            "has no `return … 'real'`, and the audit believed the table — the "
                            "registry must be checked AGAINST the code, never taken on trust")

    # ---- 5. THE SCOPE BITE — USE vs MENTION. `REAL_TIER_RE` is anchored to a `return` on
    # purpose: a bare "real" anywhere would be satisfied by the gate's own comments, and this
    # very file is stuffed with the word. Prove prose does NOT satisfy it.
    if REAL_TIER_RE.search('# this module returns a "real" measurement, honestly\n'):
        failures.append("ds-021 (C): REAL_TIER_RE matched a COMMENT mentioning 'real' — the "
                        "USE-vs-MENTION hole, which no syntax closes and only SCOPE saves. The "
                        "gate would then pass any file that merely talks about real tokens")
    if not REAL_TIER_RE.search('    return n, "real"\n'):
        failures.append("ds-021 (C): REAL_TIER_RE did NOT match a genuine `return n, \"real\"` — "
                        "the scoping is too tight and every real tier now reads as absent")

    # ---- 6. THE TRIGGER INDEX MUST BE PRESENT AND MUST FAIL LOUD. Its whole reason for
    # existing is that a reader which degrades to silence is indistinguishable from a clean
    # bill of health. If `_governs` cannot be imported, this gate's consumer is gone.
    try:
        import _governs
        # #194 — THE THIRD VERDICT, wired at the one arm that actually reads the live tree.
        # `_governs.selftest()` walks every evidence pointer in `_rulings.json` against the
        # filesystem. Some of those pointers name gitignored `outputs/` artefacts: present on the
        # machine that wrote them, absent from ANY clean checkout. That is why this step was green
        # locally and red in CI on 711bfd1 — the gate's verdict was a function of where it ran.
        # An unreachable input REFUSES (77) and names itself; anything else still FAILS (1).
        # See `_governs.checkout_cannot_hold()` for the key, and why it is git and not an env var.
        g_ref: list[str] = []
        g_fail = _governs.selftest(refusals=g_ref)
        for _gr in g_ref:
            SELFTEST_REFUSALS.append(f"trigger index: {_gr}")
        if g_fail:
            # ⛔ WIDENED #130 (`s130-D2`). This reported `g_fail[0]` ALONE. At #127 that made
            # *"one rotten pointer"* out of THIRTY: the count was never published, so every fail
            # after the first was INVISIBLE, and a repair of the first would have re-run the gate,
            # seen a different single line, and called it a new defect. A reporter that truncates
            # its own evidence cannot be distinguished from a reporter with nothing left to say
            # [[a-crash-is-not-a-fail]]. The COUNT leads, then EVERY line as its own failure.
            failures.append(f"trigger index: `_governs.py` selftest is RED — {len(g_fail)} "
                            f"failure(s), ALL listed below — the consumer of _rulings.json is "
                            f"broken, so rulings stop surfacing and the #80 re-derivation "
                            f"becomes possible again")
            for _gf in g_fail:
                failures.append(f"trigger index: `_governs.py` selftest — {_gf}")
        if not any(r["id"] == "ds-021" for r in
                   _governs.surface({"knowledge/_capture_gate.py"})):
            failures.append("trigger index: editing `_capture_gate.py` surfaces no ds-021 "
                            "ruling — the exact lookup whose absence let #80 re-derive a "
                            "settled decision 26 sessions after Dave made it")
    except Exception as e:                                       # noqa: BLE001
        # ⚠ `Exception`, NOT `ImportError`. Mutation M4 made the index unreachable and
        # `IndexUnreadable` came straight out through a narrower clause, CRASHING this function
        # and taking all 39+ checks with it. A crash is not a fail: it reports "something died"
        # where a named failure would say which seam broke, and the next session re-diagnoses it
        # from a traceback. ★ Same shape #79-D1 reasoned about from the other side — there the
        # question was whether a BaseException would slip `except Exception`; here it is whether
        # a legitimate named refusal escapes a clause too narrow to hold it. Both answers come
        # from the same rule: the handler's breadth is a property of the CALL SITE.
        # [[a-crash-is-not-a-fail]]
        failures.append(f"trigger index: `_governs.py` did not answer ({type(e).__name__}: "
                        f"{str(e).splitlines()[0]}) — ds-021 (C) ships as a PAIR (audit + "
                        f"reader) and half a pair is an instrument with no consumer, which is "
                        f"the defect it was built to end")

    return failures


def selftest_retired_unit_prose():
    """The `.md` arm's bites — `retired_unit_prose_audit()`. A separate suite from
    `selftest_cross_instrument_units()` above, for the same reason the two audit functions are
    separate: different corpus, different failure class, and a shared suite would make an edit
    to one risk silently breaking a bite that tests the other.

    ★ Every bite fails for a DISTINCT reason and is mutation-tested against a temp-tree fixture
    built to trip it — a green that can't fail is an assertion, not a test."""
    failures = []

    # ---- POSITIVE CONTROL FIRST — the two live sections Dave fixed THIS session specifically
    # so this audit could ship. His own words: "if it goes red on either, your exemption logic
    # is wrong — do not fix the prose to suit the gate." This does NOT assert the whole
    # `knowledge/` corpus is clean (measurably, as of this session, it is not — see the
    # session's own report for the residual list); it asserts these two NAMED regions never
    # regress, which is the acceptance bar Dave actually stated.
    live_f, _live_w = retired_unit_prose_audit(REPO)
    _gauge_md = "_RUNBOOK-context-gauge.md"
    for _home in ("THE FLOOR IS NOT WILLPOWER", "Half 2"):
        if any(_gauge_md in x and _home in x for x in live_f):
            failures.append(f"retired-unit prose (.md): live `{_gauge_md}` § {_home} FAILS — "
                            f"Dave: 'if it goes red on either, your exemption logic is wrong "
                            f"— do not fix the prose to suit the gate'")

    # ---- 1. THE UNDECLARED, UNFENCED BITE. This is the whole point of the .md arm: prose that
    # teaches the retired duality without saying it is retired must FAIL LOUD.
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        with open(os.path.join(k, "_fixture.md"), "w", encoding="utf-8") as fh:
            fh.write("## Some live section\n\n"
                      "This prose still teaches tape and bill as though nothing had "
                      "changed, with nothing else attached nearby that could excuse it.\n")
        f1, _w1 = retired_unit_prose_audit(td)
        if not f1:
            failures.append("retired-unit prose (.md): an UNDECLARED, UNFENCED `tape` "
                            "mention did not fail — a retired unit taught as live rots "
                            "unwatched, which is the entire reason this arm exists")

    # ---- 2. THE FENCE BITE (exemption device (i)). `tape`/`bill` under a heading matching
    # RETIRED|HISTORY|SUPERSEDED must be exempt until the next heading at equal-or-shallower
    # depth — proving the fence actually exempts, not merely exists.
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        with open(os.path.join(k, "_fixture.md"), "w", encoding="utf-8") as fh:
            fh.write("### RETIRED UNITS — HISTORY, NOT INSTRUCTION\n\n"
                      "#### Old readings\n\n"
                      "This nested sub-section says tape and bill freely, many times: "
                      "tape, bill, tape.\n\n"
                      "### The next live section\n\n"
                      "Nothing lives here that this audit would ever flag.\n")
        f2, _w2 = retired_unit_prose_audit(td)
        if f2:
            failures.append(f"retired-unit prose (.md): `tape`/`bill` INSIDE a "
                            f"RETIRED-headed fence still failed ({f2[0]}) — the fence must "
                            f"actually exempt its own span, not just exist in the file")

    # ---- 3. THE STOP_LINE_HOMES SHAPE, RE-ENACTED. `STOP_LINE_HOMES` elsewhere in this file
    # pins EXACT WORDING, and that bug BLOCKED a session's wrap when a ruling was faithfully
    # re-denominated into words the pin did not recognise. This audit must not repeat it: a
    # ruling reworded in NEW language (never matching either live docstring example verbatim)
    # must still pass as long as a declaration marker survives the rewrite.
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        with open(os.path.join(k, "_fixture.md"), "w", encoding="utf-8") as fh:
            fh.write("## A ruling, reworded this session\n\n"
                      "The cap used to bind on `bill`; that duality is SUPERSEDED and the "
                      "old word is kept only so a past reading still parses as what it "
                      "was.\n")
        f3, _w3 = retired_unit_prose_audit(td)
        if f3:
            failures.append(f"retired-unit prose (.md): a RULING REWORDED IN NEW LANGUAGE "
                            f"still failed ({f3[0]}) — this is the STOP_LINE_HOMES shape "
                            f"that blocked a session's wrap (a check pinned to exact "
                            f"phrasing punishes a faithful rewrite); this audit pins WHERE "
                            f"`tape`/`bill` may appear, never HOW the sentence is phrased, "
                            f"and must not repeat that bug")

    # ---- 4. THE PERCENTAGE-BAND EXCLUSION BITE. `45%`/`60%` outside any fence, with no
    # tape/bill word anywhere near, must be GREEN — proving the OUT-OF-SCOPE exclusion (Dave's
    # condition A) is a real, exercised absence of a check, not merely an unexercised claim.
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        with open(os.path.join(k, "_fixture.md"), "w", encoding="utf-8") as fh:
            fh.write("## Live band section, no fence, no declaration\n\n"
                      "Bands were read as GREEN <45%, AMBER 45-60%, RED >=60%, and this "
                      "paragraph names neither of the two words this audit watches for.\n")
        f4, _w4 = retired_unit_prose_audit(td)
        if f4:
            failures.append(f"retired-unit prose (.md): a bare `45%`/`60%` mention with NO "
                            f"tape/bill word FAILED ({f4[0]}) — the percentage band is "
                            f"explicitly OUT OF SCOPE (condition A); this proves the "
                            f"exclusion is a real absence of a check, not an accident of "
                            f"the fixture never trying")

    # ---- 5. CONDITION A ITSELF MUST BE ENFORCED, NOT JUST WRITTEN. Dave's condition A: the
    # scope statement belongs in every failure string, not only the docstring. Reuse bite 1's
    # shape and assert the scope substance is IN the returned text — an unenforced condition is
    # a comment, and if a future edit deletes the scope clause from the f-string, THIS bite
    # goes red.
    with tempfile.TemporaryDirectory() as td:
        k = os.path.join(td, "knowledge")
        os.makedirs(k)
        with open(os.path.join(k, "_fixture.md"), "w", encoding="utf-8") as fh:
            fh.write("## Heading\n\nStill teaches tape with nothing declared nearby.\n")
        f5, _w5 = retired_unit_prose_audit(td)
        ok = (f5 and "tape" in f5[0].lower() and "bill" in f5[0].lower()
              and "out of scope" in f5[0].lower() and "ds-023" in f5[0])
        if not ok:
            failures.append("retired-unit prose (.md): condition A's scope sentence "
                            "(`tape`/`bill` ONLY, percentage band OUT OF SCOPE, blocked on "
                            "ds-023) is NOT present in the failure text — Dave's condition "
                            "A, and an unenforced condition is a comment, not a gate")

    return failures


def selftest_growth():
    """Bite-test M6 (tiktoken heal/fallback) · #59 (measurement_degraded() + the guarded
    get_encoding() path) · M7 (§A warn) · M8 (banner) · M10 (chain) · the pinned §A digest ·
    M9 (retirement receipts)."""
    failures = []

    # ---- M6: the fallback must stay REACHABLE and must still describe itself as an ESTIMATE.
    # ⚠ #82-D1 — `CAPTURE_GATE_NO_REAL` IS SET ALONGSIDE `CAPTURE_GATE_NO_HEAL`, and without it
    # this arm silently stopped testing anything. The real tier sits ABOVE the whole cascade, so
    # a machine with a key returns 'real' and never reaches the code M6 exists to bite. The arm
    # would have gone GREEN by BYPASS — [[gate-must-quote-what-it-forbids]]: a green that cannot
    # fail is an assertion. Hiding tiktoken is no longer sufficient to reach the fallback.
    _envs = ("CAPTURE_GATE_NO_HEAL", "CAPTURE_GATE_NO_REAL")
    saved = {k: os.environ.get(k) for k in _envs}
    for k in _envs:
        os.environ[k] = "1"
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
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    # ⚠ 'real' JOINS THE DECLARED SET HERE (#82-D1). Before, an unrecognised method fell to the
    # `elif` and was reported as UNDECLARED — which is exactly what a correct real reading would
    # have done. The set is exhaustive by construction: `_tier_of` knows three tiers and no more.
    _m = measure_tokens("hello")[1]
    if _m in ("real", "tiktoken cl100k_base"):
        pass                                 # healthy env: an OBSERVED path is the one in use
    elif "ESTIMATE" not in _m:
        failures.append(f"M6: measure_tokens returned an undeclared method {_m!r}")

    # ---- #59: measurement_degraded() must track measure_tokens()'s OWN fallback exactly. It is
    # a second reader of the same fact (`_gen_chain.build()` trusts it ALONE to decide whether to
    # refuse), so if it could disagree with measure_tokens() the refusal could fire on a healthy
    # instrument or — worse — stay silent on a degraded one. Same forcing technique as M6, above.
    # ⚠ #82-D1: same bypass hazard as M6 — the real tier must be suppressed too, or this arm
    # tests a path it never reaches.
    # ⚠ W-273 S1 (#227): the probe verdict is now HELD PER PROCESS, so an arm that flips the
    # environment mid-process must clear the hold or it reads the pre-flip verdict — the arm
    # simulates a different process state, and the clear is part of the simulation.
    global _PROBE_VERDICT
    saved = {k: os.environ.get(k) for k in _envs}
    for k in _envs:
        os.environ[k] = "1"
    sys.modules["tiktoken"] = None
    try:
        _PROBE_VERDICT = None
        if not measurement_degraded():
            failures.append("#59: measurement_degraded() read False with tiktoken absent — it "
                            "has drifted from measure_tokens()'s own fallback decision")
    finally:
        del sys.modules["tiktoken"]
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    _PROBE_VERDICT = None    # W-273 S1: same reason — the healthy-restored check is a new state
    if measurement_degraded():
        failures.append("#59: measurement_degraded() read True with a healthy tiktoken restored "
                        "— it would refuse every build() forever, not just a genuinely degraded one")

    # ---- #82-D1: THE THREE NEW READERS MUST EACH BE ABLE TO FAIL, and the probe must not
    # manufacture the condition it reports. Ordered so each bite is isolated to one claim.
    if measurement_tier() not in ("real", "cl100k", "estimate"):
        failures.append(f"#82-D1: measurement_tier() answered {measurement_tier()!r} — outside "
                        f"the three-tier vocabulary, so a stamp could name a tier no gate knows")
    if _tier_of("real") != "real" or _tier_of("tiktoken cl100k_base") != "cl100k" \
            or _tier_of(f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)") != "estimate":
        failures.append("#82-D1: _tier_of() mis-sorted one of the three LIVE method strings — "
                        "the tier vocabulary has drifted from what measure_tokens() returns, "
                        "which is the two-instruments-in-one-namespace defect all over again")
    # ★ The probe-pollution bite. `_tier_probe` snapshots and restores `_TIERS_SEEN`; if that
    # restore is ever dropped, a lone health check makes measurement_mixed() true by itself and
    # the fixed-point guard starts refusing builds on its own footprint.
    # ⛔ THE SET IS EMPTIED FIRST, AND THAT IS THE WHOLE BITE. Written the obvious way —
    # snapshot, probe, compare — this check MUTATION-TESTED GREEN: by the time it runs, the
    # process has already measured with cl100k, so a probe that records 'cl100k' adds a member
    # the set ALREADY HAS and the comparison sees nothing. The defect was invisible precisely
    # because the suite was healthy. [[invariant-cannot-discriminate-reversal]] — the assertion
    # has to be made where the delta can EXIST, not merely where it is convenient to read.
    _snap0 = set(_TIERS_SEEN)
    _TIERS_SEEN.clear()
    try:
        _PROBE_VERDICT = None    # W-273 S1: a held verdict would skip the measurement and
        _tier_probe()            # trivially pass this bite — clear it so the probe really runs
        if _TIERS_SEEN:
            failures.append(f"#82-D1: _tier_probe() RECORDED {sorted(_TIERS_SEEN)} into "
                            f"_TIERS_SEEN — a health probe that writes its own footprint lets "
                            f"measurement_mixed() refuse a build on a condition the probe "
                            f"itself created")
    finally:
        _TIERS_SEEN.clear()
        _TIERS_SEEN.update(_snap0)
    # ---- W-273 S1 (#227): THE OLD LIE MUST STAY DEAD. The pre-#227 probe measured "x" —
    # permanently cached — so with the API dead it still answered 'real' (driven live at #226:
    # probe said real, a novel nonce measured cl100k-estimate). Re-enacted, not asserted: the
    # API is forced dead, the held verdict cleared, and the probe must NOT say 'real' — and it
    # must not have seeded its nonce into the content-keyed cache.
    _saved_verdict, _saved_read_key = _PROBE_VERDICT, gauge.read_key
    _rows_before = len(gauge._cache())
    try:
        gauge.read_key = lambda: None          # the API is unreachable, deterministically
        _PROBE_VERDICT = None                  # force a fresh probe past the per-process hold
        _v = _tier_probe()
        if _v == "real":
            failures.append("W-273 S1: _tier_probe() said 'real' with the API dead — the "
                            "cached-'x' lie is back: the probe is not measuring novel text")
        if len(gauge._cache()) != _rows_before:
            failures.append("W-273 S1: the probe changed the token-cache row count — a health "
                            "probe seeded a junk row into a content-keyed cache")
    finally:
        gauge.read_key = _saved_read_key
        _PROBE_VERDICT = _saved_verdict
    # ★ And mixed-tier detection must be able to say YES, not merely default to NO. Re-enacted
    # here rather than asserted: a guard proved only in its passing state is an assertion.
    _snap = set(_TIERS_SEEN)
    try:
        _TIERS_SEEN.update({"real", "cl100k"})
        if not measurement_mixed():
            failures.append("#82-D1: measurement_mixed() read False with TWO tiers recorded — "
                            "the fixed point is unguarded and _CHAIN.md can bake two units")
        if measurement_tiers_seen() != sorted(_TIERS_SEEN):
            failures.append("#82-D1: measurement_tiers_seen() cannot NAME the tiers it saw — a "
                            "refusal that will not say which instruments disagreed is a shrug")
    finally:
        _TIERS_SEEN.clear()
        _TIERS_SEEN.update(_snap)
    if len(_TIERS_SEEN) <= 1 and measurement_mixed():
        failures.append("#82-D1: measurement_mixed() read True on a single-tier process — it "
                        "would refuse every build forever, #59's failure mode in a new coat")

    # ---- #59: the get_encoding()/encode() half of measure_tokens must ALSO degrade to a
    # labelled ESTIMATE rather than crash uncaught — before this fix only the `import tiktoken`
    # line was guarded. Monkeypatch get_encoding to fail the way a cold-cache network fetch fails
    # (tiktoken.load.read_file_cached -> requests.get -> raise_for_status), WITHOUT touching the
    # import path, so this bite is isolated to the second guard and cannot be satisfied by M6's.
    # ⛔ THIS ARM NEEDS THE REAL MODULE — it monkeypatches it. On a machine without tiktoken the
    # import used to raise ModuleNotFoundError straight out of selftest_growth() and the WHOLE
    # suite died with a traceback: a crash, which is not a fail. [[a-crash-is-not-a-fail]] — a
    # parse/measure helper must fail LOUD and NAMED and DECLARE what the gap leaves unproven.
    # ⚠ It must NOT silently pass either: a declared gap passes, a silent one fails. So the
    # absence is reported as a NAMED REFUSAL in `failures`, in gauge.MeasurementRefused's idiom.
    try:
        real_tiktoken = importlib.import_module("tiktoken")
    except ImportError as e:
        failures.append(
            f"#59 REFUSING TO GUESS: tiktoken is not importable in this interpreter "
            f"({sys.executable}) — {e}. This arm MONKEYPATCHES the real module, so it cannot "
            f"run at all without it, and it will not be skipped in silence. UNPROVEN while "
            f"absent: (a) that a failing get_encoding()/encode() degrades to a labelled "
            f"ESTIMATE rather than crashing uncaught, and (b) that measure_tokens() returns to "
            f"the OBSERVED 'tiktoken cl100k_base' reading once the encoder is restored. "
            f"INSTALL RECIPE: `pip install tiktoken regex --no-deps --break-system-packages "
            f"--target /tmp/pylibs` then re-run with `PYTHONPATH=/tmp/pylibs`; or let "
            f"`_heal_tiktoken()` do its one `pip install tiktoken` attempt on a networked box.")
    else:
        real_get_encoding = real_tiktoken.get_encoding

        def _boom(*_a, **_k):
            raise RuntimeError("simulated: cl100k_base.tiktoken fetch failed (no network / cold cache)")
        real_tiktoken.get_encoding = _boom
        try:
            n, method = measure_tokens("hello world")
            if "ESTIMATE" not in method:
                failures.append(f"#59: a failing get_encoding() was not caught — method read "
                                f"{method!r} instead of falling back to the ESTIMATE")
            if n <= 0:
                failures.append("#59: fallback from a failed get_encoding() returned a non-positive count")
        finally:
            real_tiktoken.get_encoding = real_get_encoding
        if measure_tokens("hello")[1] != "tiktoken cl100k_base":
            failures.append("#59: get_encoding restored but measure_tokens did not return to OBSERVED")

    with tempfile.TemporaryDirectory() as td:
        # ---- M8: banner budget — fires at warn, fires at block, silent for a normal banner.
        # FAT measures ~240 tk/line (MEASURED, not assumed: the first draft guessed ~200 tk/line,
        # put the warn fixture at 5.4K, and bit as a block instead). s212-D11 (2026-08-21) CLASS
        # FIX: the fixture SIZES are now DERIVED from the live fallback pair instead of hardcoded —
        # the restamp to (6400, 7800) broke the old hardcoded 17/30-line fixtures, which is the
        # fixture-hardcoding class biting its own selftest. Warn fixture aims mid-band; block
        # fixture aims comfortably past block so ±10% per-line drift stays on the right side.
        _m8_w, _m8_b = BANNER_BUDGET_FALLBACK_TK
        _m8_warn_lines = max(1, round(((_m8_w + _m8_b) / 2) / 240))
        _m8_block_lines = _m8_b // 240 + 4
        _f, w, _n = _warns_for(td, fat_banner=_m8_warn_lines)
        if not any("banner region" in x for x in w):
            failures.append("M8: a 17-fat-line banner did not WARN — the sub-budget does not bite")
        # ★ M8 TIER-BY-LEGALITY (#154, closing DO-FIRST 11) — both arms asserted, both ways.
        # (a) AT MINIMUM: the fixture has ★ LATEST and NO ★ PRIOR, so no roll is legal; an
        # over-block region must land in WARNS, say why, and must NOT fail — the old fail here
        # demanded a forbidden action (proven-by-reversal #58; #49/#51/#153 shaved record for it).
        f, w, _n = _warns_for(td, fat_banner=_m8_block_lines)
        if any("banner region" in x for x in f):
            failures.append("M8: an over-block region AT the 2c minimum FAILED — the gate is "
                            "demanding a roll the 2c contract forbids (DO-FIRST 11, closed #154)")
        if not any("AT 2c MINIMUM" in x for x in w):
            failures.append("M8: an over-block region at the 2c minimum did not WARN with the "
                            "AT-2c-MINIMUM tag — the downgrade must declare its reason, or it is "
                            "indistinguishable from the budget simply not biting")
        # (b) ROLLABLE: two ★ PRIORs present ⇒ a 2c roll IS legal and the block stands as ruled.
        # This is the mutation control on (a): if the tier key were dead code, this arm would
        # warn too and the pair would catch it.
        _two_priors = ("> ## ★ PRIOR — fixture prior A\n> - prior body line\n"
                       "> ## ★ PRIOR — fixture prior B\n> - prior body line")
        f, _w, _n = _warns_for(td, fat_banner=_m8_block_lines, banner_extra=_two_priors)
        if not any("roll a banner" in x for x in f):
            failures.append("M8: an over-block region WITH a rollable ★ PRIOR did not BLOCK — "
                            "the legality key has widened the downgrade past its licence "
                            "(gate-narrows-its-own-rule, inverted)")
        _f, w, n = _warns_for(td)
        if any("banner region" in x for x in w):
            failures.append("M8: an ordinary banner warned — the budget fires on everything")

        # ---- M8 cap PROVENANCE (Dave #53, D4 (a)): the cap is DERIVED, and when it cannot be
        # derived it must SAY SO. A silent fallback is the defect the whole re-expression
        # exists to remove, so both arms are asserted — the green is a mutation test, not a
        # claim. The fixture repo carries no archive, so this arm must read FALLBACK.
        if not any("cap FALLBACK" in x for x in n):
            failures.append("M8: no archive present and the cap did not DECLARE a fallback — "
                            "a silently-fallen-back cap is indistinguishable from a measured one")
        # The mutation: give it an archive and the same call must switch to DERIVED.
        _n_min = BANNER_ARCHIVE_MIN_N
        with open(os.path.join(td, "_GM-ARCHIVE.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(f"## ★ PRIOR — {i}\nbody line for banner {i}\n"
                              for i in range(_n_min + 2)))
        _w2, _b2, prov2 = banner_budget_tk(td, ["# h", "> ## ★ LATEST x", "b"], 1)
        if not prov2.startswith("DERIVED"):
            failures.append(f"M8: an archive of {_n_min + 2} banners did not produce a DERIVED "
                            f"cap — the function is pinned to its fallback ({prov2})")
        if _b2 < _w2:
            failures.append("M8: derived block is below derived warn — the cap is inverted")
        os.remove(os.path.join(td, "_GM-ARCHIVE.md"))

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

        # ★ #48 — THE UNIT BITE (open 16 (a), Dave #47). The cap must bind the FILE, not the slice.
        # ⚠ This is the bite the old suite COULD NOT HAVE HAD, and its absence is the whole of
        # open 16: for four sessions every M10 bite here passed while the wrapper went unmeasured,
        # because they all asked "did it warn?" and none asked "warned about WHAT SIZE?". A revert
        # of `chain_file_tk` would put the slice figure back and leave every other bite in this
        # block green. So assert the NUMBER, and assert the FILE exceeds the SLICE — if the two are
        # ever equal, the wrapper has stopped being counted and the defect is back.
        if chain_note is not None:
            m_slice = re.search(r"READ CHAIN (\d+) tk", chain_note)
            m_file = re.search(r"CHAIN FILE ([\d,]+) tape", chain_note)
            if m_file is None:
                failures.append(f"M10 UNIT BITE: no CHAIN FILE figure is published, so the cap is "
                                f"measuring the slice again and the wrapper every cold session pays "
                                f"for is uncapped (open 16). Note was: {chain_note}")
            elif m_slice is not None:
                fl, sl = int(m_file.group(1).replace(",", "")), int(m_slice.group(1))
                if fl <= sl:
                    failures.append(f"M10 UNIT BITE: the FILE figure ({fl:,}) does not exceed the "
                                    f"SLICE ({sl:,}) — the wrapper adds text unconditionally, so "
                                    f"equality means one of the two is not measuring what it says")
        # …and the budget line must NAME its unit. A bare number under a moved unit is the ds-021
        # defect exactly: precise, and in the wrong unit, with nothing on the surface to say so.
        m10_note = next((x for x in n if x.startswith("M10 read chain")), None)
        if m10_note is not None and "_CHAIN.md" not in m10_note:
            failures.append(f"M10 UNIT BITE: the chain budget line does not name `_CHAIN.md` as its "
                            f"unit — ds-021, a bare token count is a defect. Note was: {m10_note}")

        # ★ #49 — THE M10 STAMP BITE (open 15, born #45). For four sessions the chain figure had
        # NO live assertion: `SIZE_TK_RE` validates the GM figure and every other chain-near-stamp
        # string in this file was a fixture. These bites are what makes `guards: SIZE_TK_RE` true.
        #
        # ★ THE POSITIVE CONTROL LEADS, and here it is doing double duty — it proves the check is
        # not firing on everything (a fail that always fires is deleted within one wrap) AND it is
        # the SCOPE control's first half.
        _f, _w, _n2 = _warns_for(td)
        if any("HAND-WRITTEN chain figure" in x for x in _f):
            failures.append("open 15: an ORDINARY stamp tripped the chain-figure ban. The check "
                            "fires on everything, which makes it noise and gets it routed around")
        # The forms are REAL — every one taken from `git log` on GOOD-MORNING.md, not invented:
        # `chain **4.4K tape` (#44) · `chain 3.56K tape` (#39) · `chain 34.7K tk` (#30, legacy unit)
        # · `chain 13,277 real` (#90 — THE ESCAPE VERBATIM: live unit, full digits, no K; this is
        #   the form the pre-#94 regex demonstrably passed — re-enacted before widening, no match).
        # `chain 13.3K real` is the one non-observed form here, DECLARED as such: it is the K×real
        # cell the unit-normalisation opens, one keystroke from the escape, tested so the vocabulary
        # widening is proven on both digit shapes rather than assumed.
        for hand in ("chain **4.4K tape**", "chain 3.56K tape", "chain 34.7K tk",
                     "chain 13,277 real", "chain 13.3K real"):
            f_, _w, _n3 = _warns_for(td, stamp=f"> **size:** GM 1.00K tape · {hand} · measured x")
            hit = next((x for x in f_ if "HAND-WRITTEN chain figure" in x), None)
            if hit is None:
                failures.append(f"open 15: the stamp form {hand!r} did NOT fail. This is one of "
                                f"the shapes the hand copy has actually taken in this repo's "
                                f"history, so a regex that misses it leaves the door #45 retired "
                                f"the figure to close standing open")
            elif "_CHAIN.md" not in hit or "RETIRED #45" not in hit:
                failures.append(f"open 15: the refusal for {hand!r} does not name the retirement "
                                f"or the figure's real home. A gate that only forbids teaches the "
                                f"next session nothing — report the measurement. Was: {hit}")
        # ★ NEGATIVE CONTROL, #94: the documented non-match stays a non-match after the widening.
        # `chain 4,065 → 4,400` is the regex comment's own example of unit-less transition prose;
        # if the widened alternation catches it, the ban has grown past what it quotes — open 23's
        # bare-figure cost is DECLARED open and must not be annexed silently by this fix.
        f_, _w, _n5 = _warns_for(td, stamp="> **size:** GM 1.00K tape · chain 4,065 → 4,400 · "
                                           "measured x")
        if any("HAND-WRITTEN chain figure" in x for x in f_):
            failures.append("open 15 #94 SCOPE: the unit-less transition `chain 4,065 → 4,400` "
                            "tripped the ban — the widening escaped its declared scope; open 23's "
                            "cost was meant to stay open, not be closed by accident")
        # ★★ THE SCOPE CONTROL, and it is the load-bearing bite. `GOOD-MORNING.md:488` really does
        # carry `the CHAIN only (**~4.1K tape**` inside a dated stratum — a TRUE record of one
        # session's boot cost. A repo-wide ban would forge a defect out of correct history. This
        # asserts the ban stops at the stamp: same string, outside it, must pass clean.
        f_, _w, _n4 = _warns_for(td, fat_c=1)
        stratum_form = "Boot read the CHAIN only (**~4.1K tape**, not GM's 19.4K)"
        if CHAIN_STAMP_RE.search(stratum_form) is None:
            failures.append("open 15 SCOPE: the regex no longer matches the live GM:488 stratum "
                            "form, so this control has stopped controlling anything — re-derive "
                            "it from the file before trusting the bite above")
        if any("HAND-WRITTEN chain figure" in x for x in f_):
            failures.append("open 15 SCOPE: a fixture with NO chain figure in its stamp still "
                            "failed — the ban has escaped the stamp and is now judging body prose, "
                            "which would fail GM's own true history (line 488)")

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
    # ⚠ #48: RE-POINTED A SECOND TIME, and again the REFERENT moved rather than the ruling — from
    # the SLICE to the whole `_CHAIN.md` FILE (open 16 (a), Dave #47). Both ends moved by the
    # measured 417-tape wrapper, so the verdict is arithmetically identical; the pin fires on the
    # numbers, which is right, and the note below is where the reason has to live. ★ The test of a
    # restatement is that it is BORING TODAY: if this change had also moved a pass to a warn, it
    # would be a re-dial wearing a unit change, and this pin would be the only honest record left.
    for name, got, want, note in (
            ("CHAIN_BUDGET_TK", CHAIN_BUDGET_TK, (7700, 10000),
             "RE-POINTED TWICE, both times the REFERENT and never the ruling. #33 2026-07-28: was "
             "(24000, 28000) against the GM+LS-whole referent, ruled 2026-07-27 M-set → (4500, "
             "6000) against the SLICE. #48 2026-07-30 (open 16 (a), Dave #47): → (4917, 6417) "
             "against the whole _CHAIN.md FILE = the same (4500, 6000) plus the MEASURED 417-tape "
             "wrapper, so the verdict is arithmetically unchanged (ds-021: restate, never silently "
             "tighten). Values still AGENT-DERIVED, still ADVISORY, still awaiting Dave. "
             "s212-D11 2026-08-21: RESTAMPED REAL (7700, 10000), RULED BY DAVE — no longer "
             "agent-derived; still fires today on real growth (chain 19,189 real)"),
            ("BANNER_BUDGET_FALLBACK_TK", BANNER_BUDGET_FALLBACK_TK, (6400, 7800),
             "⛔ NO LONGER THE CAP — it is the DECLARED FALLBACK only. Born as the cap, ruled "
             "2026-07-27 M-set; RE-EXPRESSED AS A FUNCTION 2026-07-30 #53 on Dave's D4 (a), "
             "because the measurement showed (4000, 5000) sat at the floor plus TWO TAPE "
             "(header 1,968 + 2 × median 1,515 = 4,998) and could not be complied with. The "
             "old pair is retained VERBATIM as the fallback so a repo with no archive behaves "
             "exactly as it always did — ds-021: restate openly, never silently re-dial. The "
             "live cap is `banner_budget_tk()` and publishes its own provenance every run. "
             "s212-D11 2026-08-21: fallback pair RESTAMPED REAL (6400, 7800), RULED BY DAVE; "
             "path unreachable today (n=211 >= min 10)"),
            ("SECTION_A_WARN_TK", SECTION_A_WARN_TK, 7200,
             "ruled 2026-07-27 M-set; s212-D11 2026-08-21: RESTAMPED REAL 7200, RULED BY DAVE — "
             "the old 4500 warn was a pure unit artefact once measurement went real"),
            ("CORPUS_BUDGET_TK", CORPUS_BUDGET_TK, 55700,
             "born #33 2026-07-28, AGENT-DERIVED from 34,094 tk measured, warn-only, awaiting Dave. "
             "s212-D11 2026-08-21: RESTAMPED REAL 55700, RULED BY DAVE — no longer awaiting; "
             "still fires today on real growth (corpus 184,746 real, 3.3x)"),
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


def selftest_stale_top():
    """s161-D4 (#161) — the stale-top-item fence bites, and the bite is THE CHECK'S.

    RED FIXTURE = THE REAL #160 TEXT, not a convenient one: the sentence
    `_DECISION-HISTORY/2026-08-12-160-*.md:90` actually carried — *"`s142-D1` is the next
    window's top item"* — placed in its legal home (`residual → #161:`) against a store whose
    `s142-D1.status` says `RULED #142, ENACTED #143`. That is the defect verbatim.

    MUTATION CONTROL: neuter the check's discriminator (`_OWED_CONTEXT_RES = ()`) and the RED
    fixture must PASS. Without it a green here proves only that SOMETHING failed, not that this
    check failed [[mutation-tests-the-clause-not-the-feature]]."""
    print("\n-- stale-top-item fence (s161-D4, #161) --")
    failures = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] stale-top: {name}")
        if not cond:
            failures.append(f"stale-top: {name}")

    bite("STALE_TOP_BLOCKING pin is True (BLOCKING at birth, s161-D4 — a flip must land WITH "
         "its ruled demotion and edit this pin in the same edit; the M10 pattern)",
         STALE_TOP_BLOCKING is True)

    store = {"rulings": [
        {"id": "s142-D1", "status": "RULED #142, ENACTED #143: 113 of 114 ruled rows landed."},
        {"id": "s116-D4", "status": "RULED #116. NOT ENACTED — characterisation owed first."},
    ]}

    def fixture(td, residual):
        os.makedirs(os.path.join(td, "knowledge"), exist_ok=True)
        with open(os.path.join(td, "knowledge", "_rulings.json"), "w", encoding="utf-8") as f:
            json.dump(store, f)
        banner = ("# GM\n\n> ## ★ LATEST — 2026-08-12 (Wed **#161**)\n"
                  f"{residual}\n\n> ## ★ PRIOR — 2026-08-11 (#160)\n"
                  "> - a prior banner that must never be scanned\n")
        for name in ("GOOD-MORNING.md", OUT_CHAIN):
            with open(os.path.join(td, name), "w", encoding="utf-8") as f:
                f.write(banner)

    # ---- 1. THE RED FIXTURE — the real #160 sentence in the residual home.
    RED = ("> **residual → #162:** ⬛ **① The wave.** `s142-D1` is the next window's top item, "
           "and the argument for that ordering is this session.")
    with tempfile.TemporaryDirectory() as td:
        fixture(td, RED)
        f_, n_ = stale_top_item_check(td)
        bite("the REAL #160 claim FAILS (the defect itself)",
             any("s142-D1" in x and "ENACTED" in x for x in f_))
        bite("the fail quotes the CLAIMING LINE verbatim",
             any("is the next window's top item" in x for x in f_))
        bite("the fail quotes the STORE's status verbatim",
             any("RULED #142, ENACTED #143" in x for x in f_))
        bite("it fires once per surface — GM and the chain both scanned", len(f_) == 2)
        bite("the note reports the measurement (lines scanned + window), never a remedy",
             any("residual → #N` line(s) scanned" in x and "±160" in x for x in n_))

        # ---- 2. MUTATION CONTROL — neuter the discriminator, the RED fixture must pass.
        global _OWED_CONTEXT_RES
        real = _OWED_CONTEXT_RES
        try:
            _OWED_CONTEXT_RES = ()
            f_, _ = stale_top_item_check(td)
            bite("MUTATION: with the owed vocabulary emptied the RED fixture PASSES — the bite "
                 "above is THIS check's, not some other check's", not f_)
        finally:
            _OWED_CONTEXT_RES = real

    # ---- 3. GREEN CONTROL — an owed claim citing a genuinely OPEN ruling must pass.
    with tempfile.TemporaryDirectory() as td:
        fixture(td, "> **residual → #162:** ⬛ **① `s116-D4` — THE 72 CONTROLS [0 — NEW TOP]**, "
                    "characterisation still owed before the promote.")
        f_, _ = stale_top_item_check(td)
        bite("GREEN: an owed claim on a ruling the store calls NOT ENACTED passes", not f_)

    # ---- 4. USE vs MENTION — a history/evidence citation must not trip it.
    with tempfile.TemporaryDirectory() as td:
        fixture(td, "> **residual → #162:** ✅ *CONSUMED: **#160 residual ① — the `s142-D1` "
                    "wave was owed** (KILLED AS A PREMISE: it was enacted at #143).*")
        f_, n_ = stale_top_item_check(td)
        bite("USE vs MENTION: an owed-shaped clause that cites its own enactment is EXEMPT",
             not f_ and any("EXEMPT by scope" in x for x in n_))

    # ---- 5. SCOPE — the same sentence in PROSE (not the residual home) is not scanned.
    with tempfile.TemporaryDirectory() as td:
        fixture(td, "> - #160's `residual → #161` said `s142-D1` is the next window's top item.")
        f_, _ = stale_top_item_check(td)
        bite("SCOPE: the identical sentence in a narrative line is NOT scanned (#77's lesson)",
             not f_)

    # ---- 6. An unreadable store reads UNMEASURED, never clean.
    with tempfile.TemporaryDirectory() as td:
        fixture(td, RED)
        os.remove(os.path.join(td, "knowledge", "_rulings.json"))
        f_, n_ = stale_top_item_check(td)
        bite("an absent store is UNMEASURED and SAYS SO — never silently green",
             not f_ and any("UNMEASURED" in x for x in n_))
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


def _handoff_fixture(td, session_no, claim_line, log_keys=(), gm_archive_keys=(),
                     ls_archive_keys=(), banners=2, deltas=3, heading_note=None):
    """A minimal repo for `roll_claim_check` fixtures — a ★ LATEST banner naming `session_no`,
    carrying `claim_line` as its bullet(s) (a single string, a list of strings, or none, if
    `claim_line` is None), plus every surface `_roll_state.py` needs to measure cleanly (so the
    fixture exercises the CHECK, not an UNPARSEABLE short-circuit).

    `heading_note`, added #77 for the MENTION-IMMUNITY fixture: appended into the ★ LATEST
    heading itself (after its own em-dash, mirroring the live #76 shape where the narration word
    "RESIDUAL" sits IN THE HEADING, not in a bullet) — so a fixture can pin that the heading is
    never scanned either, not just the bullets."""
    os.makedirs(os.path.join(td, "notes"), exist_ok=True)
    heading = f"> ## ★ LATEST — 2026-08-01 (Sat **#{session_no}**, fixture"
    if heading_note:
        heading += f" — {heading_note}"
    heading += ")"
    gm = ["# Good morning", "", heading]
    claim_lines = [] if claim_line is None else (
        list(claim_line) if isinstance(claim_line, (list, tuple)) else [claim_line])
    for cl in claim_lines:
        gm.append(f"> - {cl}")
    for i in range(banners - 1):
        gm.append(f"> ## ★ PRIOR — fixture prior {i}")
    gm.append("### ⏱ SESSION STRATA")
    with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(gm) + "\n")
    ls = [f"## ⏱ LATEST DELTA — fixture #{session_no}"]
    for i in range(deltas - 1):
        ls.append(f"## ⏱ PRIOR DELTA — fixture prior {i}")
    with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(ls) + "\n")
    with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
        f.write(("\n".join(f"#### 2026-08-01 #{k}" for k in log_keys) + "\n") if log_keys else "\n")
    with open(os.path.join(td, "_GM-ARCHIVE.md"), "w", encoding="utf-8") as f:
        f.write(("\n".join(f"## Batch 2026-08-01 #{k} — fixture" for k in gm_archive_keys) + "\n")
                if gm_archive_keys else "\n")
    with open(os.path.join(td, "_LIVE-STATE-ARCHIVE.md"), "w", encoding="utf-8") as f:
        f.write(("\n".join(f"## ⏱ PRIOR DELTA — 2026-08-01 (**#{k}**, fixture)"
                           for k in ls_archive_keys) + "\n") if ls_archive_keys else "\n")
    return td


def selftest_handoff_history():
    """T4 (#77) — the regression corpus. One fixture per historical re-enactment named in the
    handoff-testing-regime plan's failure inventory (notes/2026-08-02-handoff-testing-regime-plan.md
    § the evidence base), each MUTATION-RUN live before being written down (receipts: the build
    session's own report). #70/#71 (skipped wrap) is a DECLARED NON-CATCH — the plan's own
    words: "it cannot fire inside a session that never runs the wrap at all... the next
    session's title check catches it one session late, and that stays the only net." Asserted
    below by running THAT net's own selftest, not by faking a fixture for a class this regime
    was never going to catch."""
    failures = []

    # ⛔ #77 SEMANTICS CHANGE (2026-08-02): the two-arm design below was replaced by GENERATED-
    # LINE-ONLY SCOPE after arm (ii) false-fired live on RATIFIED #76 banner text (the docstring
    # above `roll_claim_check` and the `_ROLL_GENERATED_ANCHOR_RE` comment carry the full story).
    # The historical fixtures below still PIN each defect class — #75/#73's re-enactments now
    # RED on ABSENCE of a generated line rather than on a graded contradiction, because that is
    # what the new design actually does when a banner carries only authored prose: the claim's
    # one legal home is missing, full stop. The mutation still DISCRIMINATES the #75/#73 states
    # (a banner that never adopted T1's generated line still fails the wrap), it just names a
    # different, more honest reason — "you never ran `_roll_state.py`" beats "your prose parsed
    # wrong", because the prose was never the fix; the generated line always was.

    # ---- #75 (semantics changed #77): banner carries ONLY the authored claim `2f NOT run`
    # (the live #75/#76 defect's own wording) with NO generated line anywhere in ★ LATEST. Old
    # verdict: RED on a graded contradiction (`log #74` vs the authored claim). New verdict: RED
    # on ABSENCE — the authored line is prose now, never scanned, so the only thing left to grade
    # is "is there a generated line at all", and there is not one. Still catches the #75 state.
    with tempfile.TemporaryDirectory() as td:
        _handoff_fixture(td, 75, "2f NOT run", log_keys=(74,), gm_archive_keys=(74,),
                         ls_archive_keys=(73,))
        f_, _w, _n = roll_claim_check(td)
        if len(f_) != 1 or "no generated residual line in ★ LATEST" not in f_[0]:
            failures.append(f"#75 fixture (post-#77 semantics): expected exactly one ABSENCE "
                            f"FAIL, got {f_}")

    # ---- #73 (semantics changed #77): a residual authored in free prose, outside any legal
    # form. Old verdict: RED naming "matches NEITHER legal form". New verdict: RED on ABSENCE —
    # this prose is not scanned at all now (it never anchors `**residual (GENERATED`), so it is
    # invisible to the check exactly like any other banner sentence, and the check still fails
    # the wrap because no generated line exists anywhere in the banner.
    with tempfile.TemporaryDirectory() as td:
        _handoff_fixture(td, 73, "the residual is mostly fine, some rolls happened",
                         log_keys=(72,), gm_archive_keys=(72,), ls_archive_keys=(71,))
        f_, _w, _n = roll_claim_check(td)
        if len(f_) != 1 or "no generated residual line in ★ LATEST" not in f_[0]:
            failures.append(f"#73 fixture (post-#77 semantics): expected exactly one ABSENCE "
                            f"FAIL, got {f_}")

    # ---- #72: UNCHANGED — a GENERATED-form residual whose numbers contradict the measured
    # tree still FAILS on contradiction, exactly as before. `log #71` claimed, `#70` is what the
    # fixture's own _GAUGE-LOG.md carries. (Bold markers included — `**residual (GENERATED …`
    # is the anchor itself, per the live `_roll_state.py` output shape.)
    with tempfile.TemporaryDirectory() as td:
        _handoff_fixture(
            td, 72,
            "**residual (GENERATED #72):** 2c OK (banners 2/2) · 2d OK (deltas 3/3) · 2f OK "
            "(strata 0, log #71) — _roll_state.py · 2026-08-01",
            log_keys=(70,), gm_archive_keys=(71,), ls_archive_keys=(70,))
        f_, _w, _n = roll_claim_check(td)
        if not any("GENERATED-form residual contradicts the measured tree" in x for x in f_):
            failures.append(f"#72 fixture: expected a GENERATED-form contradiction FAIL, got {f_}")

    # ---- NEW #77: MENTION IMMUNITY — the exact live #76 false-fire, pinned so it can never
    # return. A banner whose ★ LATEST HEADING narrates the bare word "RESIDUAL" (no anchor) AND
    # whose bullets QUOTE a past session's claim verbatim ("the 2c/2d/2f rolls were NOT run",
    # attributed, about #75, not this session) — PLUS a correct generated line for the CURRENT
    # session — must be GREEN, grading only the generated line. This is the fixture that would
    # have FAILED before Edit 1 (the two-arm design flagged both the heading and the quote).
    with tempfile.TemporaryDirectory() as td:
        heading_note = ("THE CHAIN BOOTED ME ON A FALSE RESIDUAL — narration only, no legal "
                        "home here")
        quoted = ("THE BANNER QUOTES A PAST SESSION VERBATIM. #75's banner said "
                 '*"the 2c/2d/2f rolls were NOT run"*; a retrospective quote about #75, not a '
                 "fresh claim about this session.")
        _handoff_fixture(td, 76, [quoted], log_keys=(75,), gm_archive_keys=(75,),
                         ls_archive_keys=(74,), heading_note=heading_note)
        measured = roll_state.measure(td)
        line = roll_state.render_line(measured, today=datetime.date(2026, 8, 2))
        _handoff_fixture(td, 76, [quoted, line[2:]], log_keys=(75,), gm_archive_keys=(75,),
                         ls_archive_keys=(74,), heading_note=heading_note)
        f_, _w, n_ = roll_claim_check(td)
        if f_:
            failures.append(f"MENTION IMMUNITY fixture: heading narration + a quoted past "
                            f"claim + a correct generated line should be GREEN, got fails: {f_}")
        elif not any("consistent with the measured tree" in x for x in n_):
            failures.append("MENTION IMMUNITY fixture: the passing case said nothing")
        # ⚠ MUTATION RECEIPT (both old arms, re-enacted standalone — the exact regex text this
        # session read off the file BEFORE Edit 1 deleted it; HEAD has no committed copy of the
        # two-arm design to `git show`, since T1/T2 were built and never committed in the same
        # session that found the live defect, so this is the only re-enactment available, and it
        # is faithful — verbatim regex literals, not a paraphrase): classified the heading line
        # as "unknown" (→ old code's "matches NEITHER legal form" FAIL) and the quoted-claim
        # bullet as "authored" (→ old code grades `2c` against the tree as a live claim it never
        # was) — both false positives, live receipt in this session's report.

    # ---- NEW #77: duplicate generated lines → RED. The claim has exactly one legal home; two
    # candidate lines means the check cannot know which one is authoritative and refuses rather
    # than picking one silently.
    with tempfile.TemporaryDirectory() as td:
        _handoff_fixture(td, 79, None, log_keys=(78,), gm_archive_keys=(78,),
                         ls_archive_keys=(77,))
        measured = roll_state.measure(td)
        line = roll_state.render_line(measured, today=datetime.date(2026, 8, 2))
        _handoff_fixture(td, 79, [line[2:], line[2:]], log_keys=(78,), gm_archive_keys=(78,),
                         ls_archive_keys=(77,))
        f_, _w, _n = roll_claim_check(td)
        if not any("duplicate homes" in x for x in f_):
            failures.append(f"duplicate-generated-lines fixture: expected a duplicate-homes "
                            f"FAIL, got {f_}")

    # ---- #58 crash-shape, re-enacted on THE SURVIVING PARSER (arm (ii) is gone, so the crash
    # class now lives entirely inside `_ROLL_GENERATED_RE`'s own digit groups): (a) a prose
    # mention with a bare comma sitting BEFORE the real generated line must not crash and must
    # grade the real line, the mention itself simply never anchoring and so never being looked
    # at; (b) a line that DOES anchor (`**residual (GENERATED`) but is corrupted in the #58 bare-
    # comma shape inside its own digit group must not crash either — it must FAIL loud and named
    # as an unparseable generated line, never guess a value out of punctuation.
    with tempfile.TemporaryDirectory() as td:
        mention = ("no residual was written before the job, and that is a LAPSE — 2f NOT run, "
                  "2c OK, state pending")
        _handoff_fixture(td, 58, [mention], log_keys=(57,), gm_archive_keys=(57,),
                         ls_archive_keys=(56,))
        measured = roll_state.measure(td)
        line = roll_state.render_line(measured, today=datetime.date(2026, 8, 2))
        _handoff_fixture(td, 58, [mention, line[2:]], log_keys=(57,), gm_archive_keys=(57,),
                         ls_archive_keys=(56,))
        try:
            f_, _w, n_ = roll_claim_check(td)
        except Exception as e:
            failures.append(f"#58 crash-shape (mention-then-generated): roll_claim_check "
                            f"RAISED ({e}) — a crash is not a fail")
        else:
            if f_:
                failures.append(f"#58 crash-shape (mention-then-generated): the prose mention "
                                f"(bare comma, no anchor) should be ignored and the real "
                                f"generated line graded clean, got fails: {f_}")
            elif not any("consistent with the measured tree" in x for x in n_):
                failures.append("#58 crash-shape (mention-then-generated): passing case said "
                                "nothing")
    with tempfile.TemporaryDirectory() as td:
        malformed = ("**residual (GENERATED #58):** 2c OK (banners ,/2) · 2d OK (deltas 3/3) · "
                    "2f OK (strata 0, log #57) — _roll_state.py · 2026-08-01")
        _handoff_fixture(td, 58, [malformed], log_keys=(57,), gm_archive_keys=(57,),
                         ls_archive_keys=(56,))
        try:
            f_, _w, _n = roll_claim_check(td)
        except Exception as e:
            failures.append(f"#58 crash-shape (anchored malformed, bare comma): roll_claim_check "
                            f"RAISED ({e}) — a crash is not a fail")
        else:
            if not any("does not parse against its full shape" in x for x in f_):
                failures.append(f"#58 crash-shape (anchored malformed, bare comma): expected a "
                                f"named parse-failure FAIL, got {f_}")

    # ---- Green control: the canonical GENERATED line, matching the measured tree exactly, and
    # the passing path SAYS so (a silent pass cannot be told apart from a dead check).
    with tempfile.TemporaryDirectory() as td:
        _handoff_fixture(td, 77, None, log_keys=(76,), gm_archive_keys=(76,),
                         ls_archive_keys=(75,))
        measured = roll_state.measure(td)
        line = roll_state.render_line(measured, today=datetime.date(2026, 8, 2))
        _handoff_fixture(td, 77, line[2:], log_keys=(76,), gm_archive_keys=(76,),
                         ls_archive_keys=(75,))
        f_, _w, n_ = roll_claim_check(td)
        if f_:
            failures.append(f"green control: the canonical generated line, matching the "
                            f"measured tree, FAILED: {f_}")
        if not any("consistent with the measured tree" in x for x in n_):
            failures.append("green control: the passing case said nothing")

    # ---- #70/#71 (skipped wrap): DECLARED NON-CATCH, not faked here. The regime's only net for
    # this class is `_gen_chain.py`'s stale-title bite (one session late) — assert it is still
    # live, by running ITS OWN selftest, rather than duplicating it as a fixture in this file.
    sys.path.insert(0, HERE)
    try:
        import _gen_chain
        rc = _gen_chain.selftest()
        if rc != 0:
            failures.append("#70/#71 non-catch: _gen_chain.py --selftest is NOT green — the "
                            "regime's only net for a skipped wrap (the stale-title bite, one "
                            "session late) is broken")
    except Exception as e:
        failures.append(f"#70/#71 non-catch: could not run _gen_chain.py's own selftest ({e})")

    return failures


def selftest_real_tier_reachable():
    """#82-D1 — the ONE arm that lets the real tier off its leash, and it exists because
    `selftest()` puts it ON one (see the block there).

    ⚠ IT MUST NOT FAIL ON AN OFFLINE MACHINE. Reaching the API is an ENVIRONMENT fact, not a
    correctness fact, and #79-D1 already ruled that an honest refusal is the right behaviour
    where nothing is reachable. So this arm asserts what is true in EVERY environment: whatever
    tier comes back is one the vocabulary knows, and the tier the registry CLAIMS is the tier the
    source can PRODUCE. It reports the observed tier so a reader can see which path ran, because
    a test that runs two different ways and says which is honest; one that hides it is not."""
    failures = []
    saved = os.environ.pop("CAPTURE_GATE_NO_REAL", None)
    try:
        tier = measurement_tier()
        if tier not in ("real", "cl100k", "estimate"):
            failures.append(f"#82-D1: with the real tier UNSUPPRESSED the measurer answered "
                            f"{tier!r} — outside the three-tier vocabulary")
        print(f"  ▫️  #82-D1 real tier UNSUPPRESSED for one probe: observed {tier!r} "
              f"({'API reachable' if tier == 'real' else 'offline/absent — legal, and declared'})")
    finally:
        if saved is not None:
            os.environ["CAPTURE_GATE_NO_REAL"] = saved
    return failures


def selftest():
    # ⛔ #82-D1 — THE SELFTEST RUNS ON THE DETERMINISTIC TIER, AND THIS IS A DECLARED CHOICE.
    # MEASURED this session: with the real tier live the suite made **232 API round-trips** (the
    # content cache went 19 → 251 entries) at ~0.24s each and blew past the sandbox's 45s call
    # wall; suppressed, the identical suite is **16.3s, EXIT=0**. The reason is structural, not
    # incidental — a selftest measures hundreds of SYNTHETIC fixtures, every one a fresh content
    # hash and therefore a guaranteed cache miss.
    #
    # ★ THE JUSTIFICATION IS NOT SPEED, IT IS WHAT THE NUMBERS ARE FOR. A fixture's token count
    # is never published against a budget; it exists to prove a code path bites. The rule this
    # project actually holds — ONE instrument per PUBLISHED number — is untouched: the build and
    # wrap paths, which is where every stamp is produced, run on the real tier.
    # ⚠ And the suppression is not silent. `selftest_real_tier_reachable()` unsuppresses for one
    # probe and PRINTS the tier it observed, so a run always says which instrument it reached.
    # [[instrument-without-a-consumer]] — a switch nothing reports on is a switch nobody audits.
    # ★ #221 — arm the selftest write-door veto for the whole run (see selftest_write_veto).
    # Set here rather than inside `_selftest_body` so that EVERY arm, including any added later,
    # is covered by construction and not by an author's memory.
    global _SELFTEST_ACTIVE
    _SELFTEST_ACTIVE = True
    _real_saved = os.environ.get("CAPTURE_GATE_NO_REAL")
    os.environ["CAPTURE_GATE_NO_REAL"] = "1"
    try:
        return _selftest_body()
    finally:
        _SELFTEST_ACTIVE = False
        if _real_saved is None:
            os.environ.pop("CAPTURE_GATE_NO_REAL", None)
        else:
            os.environ["CAPTURE_GATE_NO_REAL"] = _real_saved


def selftest_rehearsal():
    """#92 — the rehearsal's classifier, log and rc, mutation-tested WITH a control.
    A green that can't fail is an assertion ([[six-beat-ladder-ruled]])."""
    failures = []
    iso = "2026-08-05"
    gm_fail = (f"GOOD-MORNING.md: header date zone does not carry today ({iso}) — refresh it "
               f"(ritual steps 1 / 2) before closing")
    ls_fail = (f'_LIVE-STATE.md: "Last refreshed" zone does not carry today ({iso}) — refresh '
               f"it (ritual steps 1 / 2) before closing")
    structural_sample = "pre-flight: fill 40% + job 12% + wrap 5% = 57% AMBER — retired % form"
    # ---- MUTATION: the allowlist is scoped to TWO filenames. The SAME date-fail shape on any
    # other file must stay STRUCTURAL — an allowlist that matches by shape alone would silently
    # excuse a real defect ([[gate-must-quote-what-it-forbids]], [[ban-scoped-to-a-name]]).
    other_file = f"OTHER.md: header date zone does not carry today ({iso}) — refresh it"
    heals, structural = classify_rehearsal([gm_fail, ls_fail, structural_sample, other_file])
    if len(heals) != 2:
        failures.append(f"rehearsal classifier: expected exactly the 2 ritual-refreshed date "
                        f"fails as heals-at-wrap, got {len(heals)}: {heals}")
    if structural_sample not in structural or other_file not in structural:
        failures.append(f"rehearsal classifier: a structural fail or an out-of-scope date fail "
                        f"escaped STRUCTURAL — allowlist over-matches: {structural}")
    # ---- CONTROL: empty in, empty out — the classifier invents nothing.
    if classify_rehearsal([]) != ([], []):
        failures.append("rehearsal classifier control: non-empty output from empty input")
    # ---- INTEGRATION on a fixture tree: rc, the JSONL log, and both `kind`s.
    stale = datetime.date(2026, 7, 27)
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
            f.write("Last refreshed: 2026-07-25\n")
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write("header dated 2026-07-25 (stale)\n")
        rpt = os.path.join(td, "_CG-REHEARSE-TEST.md")
        rc = run(rehearse=True, repo=td, report=rpt, today=stale)
        if rc != 1:
            failures.append(f"rehearse on a fixture with structural fails returned {rc}, not 1")
        if os.path.exists(rpt):
            failures.append("rehearse wrote a report file — must be stdout-only like --wrap (S-D3)")
        log = os.path.join(td, REHEARSAL_LOG)
        if not os.path.exists(log):
            failures.append("rehearse did not append to the rehearsal log — the fails-at-wrap-"
                            "open series (#91-F5's ordered measurement) has no writer")
        else:
            entries = [json.loads(l) for l in open(log, encoding="utf-8") if l.strip()]
            e = entries[-1]
            if e.get("kind") != "rehearse":
                failures.append(f"log kind: expected 'rehearse', got {e.get('kind')}")
            if e.get("fails") != e.get("structural", 0) + e.get("heals_at_wrap", 0):
                failures.append(f"log arithmetic broken: {e}")
            if e.get("heals_at_wrap", 0) < 2:
                failures.append(f"log: both date fails should classify heals-at-wrap, got {e}")
            run(mode="wrap", repo=td, today=stale)
            entries = [json.loads(l) for l in open(log, encoding="utf-8") if l.strip()]
            if len(entries) != 2 or entries[-1].get("kind") != "wrap-open":
                failures.append(f"a real wrap-mode run must append a 'wrap-open' line — got "
                                f"{[x.get('kind') for x in entries]}")
    return failures


def selftest_plan_block_check():
    """B2 SEAM OBLIGATION — three arms, each DRIVING the real `plan_block_check` on a real tree.
    ⛔ The CONTROL (a faithful copy of live state, which must be GREEN) is part of the same run:
    without it, an arm that goes red proves only that the check refuses everything."""
    failures = []
    import shutil
    sources = ("_CHAIN.md", "_LIVE-STATE.md", "knowledge/_lanes.json")

    def tree(td):
        for rel in sources:
            dst = os.path.join(td, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(REPO, rel), dst)

    # CONTROL — live state copied faithfully: the seam obligation is MET.
    with tempfile.TemporaryDirectory() as td:
        tree(td)
        f_, w_ = plan_block_check(td)
        if f_:
            failures.append(f"plan-block CONTROL: faithful state copy FAILED the seam check — "
                            f"the check refuses everything, so its reds prove nothing: {f_}")
    # (i) STATE THAT WILL NOT RENDER — lanes file unparseable. DOING/NEXT go UNKNOWN.
    with tempfile.TemporaryDirectory() as td:
        tree(td)
        with open(os.path.join(td, "knowledge/_lanes.json"), "w", encoding="utf-8") as f:
            f.write("{ not JSON at all")
        f_, _ = plan_block_check(td)
        if not any("B2 PLAN BLOCK" in x and "DOING" in x for x in f_):
            failures.append(f"plan-block: an unparseable lanes file did NOT fail the wrap seam "
                            f"— the wrap would close on state no block renders from: {f_}")
    # (ii) A MISSING STATE SOURCE — the loud refusal must arrive as a FAIL, not a crash.
    with tempfile.TemporaryDirectory() as td:
        tree(td)
        os.remove(os.path.join(td, "_LIVE-STATE.md"))
        f_, _ = plan_block_check(td)
        if not any("B2 PLAN BLOCK" in x for x in f_):
            failures.append(f"plan-block: a missing state source did not surface as a FAIL: {f_}")
    # (iii) NOT A STATE TREE — declared skip, never a silent pass.
    with tempfile.TemporaryDirectory() as td:
        f_, w_ = plan_block_check(td)
        if f_ or not any("SKIPPED" in x for x in w_):
            failures.append(f"plan-block: an empty tree must SKIP with the skip DECLARED, "
                            f"got fails={f_} warns={w_}")
    return failures


def selftest_governing_join():
    """★ #218 — THE REGISTER↔STORE JOIN, DRIVEN IN BOTH DIRECTIONS, on the #212 rows by name.

    ⚠ The fixture reproduces the SHAPE of the real drift (`G3` closed in the store, OPEN on the
    register) rather than a toy, because the thing under test is a prose-vs-vocabulary join and
    a toy fixture would not carry the register's habit of QUOTING the word OPEN inside a CLOSED
    cell — which is precisely how a first-word-wins reader would lie.
    """
    failures = []

    def tree(td, rows, store_states, tail=""):
        os.makedirs(os.path.join(td, "knowledge"), exist_ok=True)
        with open(os.path.join(td, "knowledge", "_GOVERNING-RECORDS.md"), "w",
                  encoding="utf-8") as f:
            f.write("| id | Item | closes_when | status |\n|---|---|---|---|\n")
            for gid, status in rows:
                f.write(f"| {gid} | a live value | Dave's word | {status} |\n")
            f.write("\n" + tail + "\n")
        with open(os.path.join(td, "knowledge", "_state.json"), "w", encoding="utf-8") as f:
            json.dump({"items": [{"id": gid, "state": st}
                                 for gid, st in store_states]}, f)
        return governing_records_join_check(td)

    agree = [("G1", "✅ **PARKED #212** — `s212-D5`, conditional park."),
             ("G3", "✅ **CLOSED #161** — `s161-D2`. ⚠ This row read OPEN for 51 sessions."),
             ("G4", "OPEN — remedy RULED OFFLOAD (`s212-D6`), enactment rowed `W-99b`.")]
    agree_store = [("G1", "parked"), ("G3", "done"), ("G4", "open")]

    # ---- GREEN CONTROL, and it doubles as the first-word-wins bite: G3's CLOSED cell contains
    # the word OPEN. A reader that scanned for it would call this a disagreement.
    with tempfile.TemporaryDirectory() as td:
        w_, n_ = tree(td, agree, agree_store)
        if w_:
            failures.append(f"join: an AGREEING register+store warned — {w_[0][:140]}")
        if not any("AGREE" in x for x in n_):
            failures.append("join: agreement was not stated — a silent green cannot be audited")

    # ---- ARM 1 (#212 finding 3, verbatim shape): store closed, register still OPEN.
    with tempfile.TemporaryDirectory() as td:
        w_, _n = tree(td, [("G3", "OPEN — Dave rules warn vs block")], [("G3", "done")])
        if not any("`G3` DISAGREES" in x for x in w_):
            failures.append(f"join: register OPEN vs store done did NOT warn — the #212 drift "
                            f"would ride again: {w_}")

    # ---- ARM 2: a store row with no register row, UNDECLARED (the G18 shape before the note).
    with tempfile.TemporaryDirectory() as td:
        w_, _n = tree(td, [("G3", "✅ **CLOSED #161**")], [("G3", "done"), ("G18", "done")])
        if not any("G18" in x and "NO ROW" in x for x in w_):
            failures.append(f"join: an unregistered store row passed silently: {w_}")

    # ---- ARM 3 (the other direction): the SAME gap, DECLARED in the register's own prose, must
    # pass as a NOTE. A declared gap passes, a silent one does not (#111-D1).
    with tempfile.TemporaryDirectory() as td:
        w_, n_ = tree(td, [("G3", "✅ **CLOSED #161**")], [("G3", "done"), ("G18", "done")],
                      tail=("⚠ **FOUND AT THE #212 WRAP AND REPORTED, NOT REPAIRED:** `G18` "
                            "exists as a row in `knowledge/_state.json` and has **no row\n"
                            "here**, so the register has never carried it."))
        if any("G18" in x for x in w_):
            failures.append(f"join: a DECLARED gap still warned — declaration must discharge it: "
                            f"{w_}")
        if not any("G18" in x and "DECLARED" in x for x in n_):
            failures.append(f"join: a declared gap was passed SILENTLY rather than named: {n_}")

    # ---- ARM 4: a register row with no store item.
    with tempfile.TemporaryDirectory() as td:
        w_, _n = tree(td, [("G3", "✅ **CLOSED #161**"), ("G99", "OPEN")], [("G3", "done")])
        if not any("G99" in x and "no item" in x for x in w_):
            failures.append(f"join: a register row absent from the store passed silently: {w_}")

    # ---- ARM 5: an illegible status cell is UNKNOWN, never defaulted to agreement.
    with tempfile.TemporaryDirectory() as td:
        w_, _n = tree(td, [("G3", "probably fine, ask Dave")], [("G3", "done")])
        if not any("no legal verdict" in x for x in w_):
            failures.append(f"join: an unreadable status cell was treated as agreement: {w_}")

    # ---- ARM 6: absent inputs ⇒ a DECLARED skip, never a green.
    with tempfile.TemporaryDirectory() as td:
        w_, n_ = governing_records_join_check(td)
        if w_ or not any("SKIPPED" in x and "NOT a pass" in x for x in n_):
            failures.append(f"join: a tree with no register/store must SKIP out loud — "
                            f"warns={w_} notes={n_}")

    # ---- ARM 7 (tier pin, the M10 pattern): this gate is ADVISORY AT BIRTH. It must reach the
    # wrap's WARNS and never its FAILS — promotion is Dave's, and a silent promotion by an agent
    # is exactly what this pin exists to catch.
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        tree(td, [("G3", "OPEN — Dave rules warn vs block")], [("G3", "done")])
        with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
            f.write("Last refreshed: 2026-07-27\n")
        f_, w_, _n = wrap_checks(td, datetime.date(2026, 7, 27), lane=True)
        if any("REGISTER↔STORE JOIN" in x for x in f_):
            failures.append("join: the check reached the wrap's FAILS — it is ADVISORY at birth "
                            "and its promotion is Dave's word, not an edit")
        if not any("REGISTER↔STORE JOIN" in x for x in w_):
            failures.append(f"join: the check is not wired into wrap_checks at all — an "
                            f"instrument with no consumer cannot fail: {w_[:2]}")
    return failures


def selftest_boot_delta_parse():
    """★ #218 — A DELTA BESIDE `boot` IS NOT A READING. Fixtures are the #215 and #218 lines
    VERBATIM from `notes/_GAUGE-LOG.md`, plus the two POTHOLE forms those lines were written
    around. The last arm drives `boot_constant_drift_check` on a real fixture log, because the
    clause being tested is "the delta does not enter the mean" — an arithmetic claim, not a
    classification one [[mutation-tests-the-clause-not-the-feature]].
    """
    failures = []

    def parse(s):
        g_, r_, d_ = _parse_boot_samples(s)
        return [tk for _, tk in g_], r_, [n for _, n in d_]

    # ---- VERBATIM, notes/_GAUGE-LOG.md #215 post-mortem: a READING with a delta elsewhere.
    line215 = ("> **post-mortem #215:** ★ **THREE MOMENTS, STATED SEPARATELY AND NEVER ROUNDED "
               "INTO ONE ANOTHER** [[measure-dont-convert-units]]: **boot 60,248 real** — ⛔ "
               "**OUT of the `s208-D1` band (56,749 ± 1,154 → 55,595–57,903) by 2,345, DECLARED "
               "at the opener and NOT corrected into the constant**")
    g_, r_, d_ = parse(line215)
    if g_ != [60248] or r_:
        failures.append(f"boot parse: the #215 post-mortem line VERBATIM must read 60,248 and "
                        f"refuse nothing — got good={g_} refused={len(r_)}")

    # ---- VERBATIM, the #215 premises line — the phrasing the author had to REACH FOR.
    line215b = ("> the brief declared boot drift of 2,345 over the band — **band read at "
                "source**, `knowledge/_gauge_tokens.py:178-179`")
    g_, r_, d_ = parse(line215b)
    if g_ or r_ or d_ != [2345]:
        failures.append(f"boot parse: `boot drift of 2,345` must be a DELTA and nothing else — "
                        f"got good={g_} refused={len(r_)} deltas={d_}")

    # ---- VERBATIM, notes/_GAUGE-LOG.md #218 declaration.
    line218 = ("> ⚠ #218's own boot — 66,845 real, a boot drift of 8,942 — is NOT in this mean: "
               "it reaches this log when #218's stratum rolls at the #219 wrap.")
    g_, r_, d_ = parse(line218)
    if d_ != [8942] or r_:
        failures.append(f"boot parse: the #218 line's `boot drift of 8,942` must be a DELTA and "
                        f"refuse nothing — got deltas={d_} refused={len(r_)}")

    # ---- THE POTHOLE, both halves. These are the shapes the briefs told humans to avoid; the
    # rule now lives here instead. (a) the LOUD half: a small delta used to be REFUSED, which
    # fails the whole gate on an honest line.
    g_, r_, d_ = parse("> the brief declared boot 2,345 over the band")
    if r_ or d_ != [2345] or g_:
        failures.append(f"boot parse: `boot 2,345 over the band` must be a DELTA, not a refusal "
                        f"— got good={g_} refused={r_} deltas={d_}")
    # (b) THE QUIET HALF, and it is the dangerous one: a delta big enough to look like a boot
    # used to be counted as a SAMPLE and the band read GREEN over it.
    g_, r_, d_ = parse("> boot 12,345 over the band, DECLARED and not corrected")
    if g_ or d_ != [12345]:
        failures.append(f"boot parse: `boot 12,345 over the band` was counted as a READING — "
                        f"a delta is in the band's sample set: good={g_} deltas={d_}")
    # (c) a signed number beside boot is a movement whatever the words say.
    g_, r_, d_ = parse("> boot +8,942 against the s208-D1 band")
    if g_ or d_ != [8942]:
        failures.append(f"boot parse: `boot +8,942` must be a DELTA — got good={g_} deltas={d_}")

    # ---- CONTROLS (attribute-the-diff): every historical READING shape still reads, including
    # the `vs` shape, which is TWO readings compared and must NOT be swallowed by the tail rule.
    for src, want in (("- **boot #95 = 65,657 real** (`message.usage` first turn; n=1)", 65657),
                      ("> **pre-flight #100 (declared):** boot 64,940 real + job", 64940),
                      ("> **pre-flight:** boot 26,897 (disk 6,897 **measured**, real", 26897),
                      ("> boot 65,041 real (n=12; the post-break cluster)", 65041),
                      ("> **Boot 53,681 real** — the #129 case, sentence-initial", 53681),
                      ("> **★ measurement banked, free:** #112 boot 55,025 vs #111 55,733", 55025)):
        g_, r_, d_ = parse(src)
        if want not in g_ or r_ or d_:
            failures.append(f"boot parse: CONTROL `{src[:44]}…` no longer reads as {want:,} — "
                            f"good={g_} refused={len(r_)} deltas={d_}; the split has eaten a "
                            f"real sample shape")
    # ---- ✅ #219, THE QUIET HALF, COMPARATIVE PHRASINGS. Each of these came back as a READING
    # before the tail list was widened — the #218 failure mode reached by ordinary English the
    # list did not name. Both directions are asserted: the comparison is EXCLUDED here, and the
    # bare-preposition CONTROLS below prove the widening did not eat a real reading with it.
    for src in ("> boot 12,345 higher than the band, DECLARED at the opener",
                "> boot 12,345 lower than the s208-D1 constant",
                "> boot 12,345 more than the band allows",
                "> boot 12,345 less than the published floor",
                "> boot 12,345 away from the band",
                "> boot 12,345 adrift of the band"):
        g_, r_, d_ = parse(src)
        if g_ or d_ != [12345]:
            failures.append(f"boot parse: `{src[:46]}…` is a COMPARISON, not a reading — it "
                            f"entered the band's sample set: good={g_} deltas={d_}")
    # ---- THE OVER-WIDENING CONTROLS (attribute-the-diff, the other direction). A bare
    # preposition after a real reading is prose ABOUT a boot, not a comparison against a band —
    # if `from`/`more`/`away` were in the list unqualified these would silently stop being samples.
    # ⚠ THE QUALIFIER WORD MUST TOUCH THE NUMBER or the control is blind: the tail regex only
    # scans punctuation and whitespace after the digits, so an intervening word (`… 55,025 real,
    # from …`) shields the line from ANY tail list and the arm proves nothing. Measured #219: the
    # first draft of these controls put `real` in the gap and stayed green under a deliberately
    # over-widened list [[mutation-tests-the-clause-not-the-feature]].
    for src, want in (("> **pre-flight #301:** boot 55,025 from the first turn", 55025),
                      ("> boot 55,025, more of the same story", 55025),
                      ("> boot 55,025 away in the archive stratum", 55025)):
        g_, r_, d_ = parse(src)
        if want not in g_ or d_:
            failures.append(f"boot parse: OVER-WIDENING — CONTROL `{src[:46]}…` stopped reading "
                            f"as {want:,}: good={g_} deltas={d_}; the tail list is eating prose")

    # ---- and a genuine unparseable reading must STILL refuse (the #129 guarantee).
    g_, r_, d_ = parse("> **pre-flight #9:** boot 999 real")
    if not r_ or g_ or d_:
        failures.append(f"boot parse: an out-of-range `boot 999` must still REFUSE — got "
                        f"good={g_} refused={r_} deltas={d_}")

    # ---- THE STRATUM/ORDINAL ARM (#241). A reading citing another session LATER in the line
    # must NOT be filed under that citation, and an unlabelled reading must fall to its stratum.
    # Driven on the exact two shapes the live log carries.
    strat = ("#### 2026-09-02 #401\n"
             "> **post-mortem #401:** **boot 70,001 real** — the canonical figure\n"
             "> **✅ AND THE PREMISES WERE CHECKED** … `_checkin.py` reads **boot 70,001**, "
             "agreeing to the token, and the #400 stratum's lesson already has a home.\n"
             "#### 2026-09-02 #402\n"
             "> **pre-flight:** boot 70,002 real — no ordinal of its own\n")
    g_, _r_, _d_ = _parse_boot_samples(strat)      # the ORDINALS are the subject — not `parse`
    if sorted(g_) != [(401, 70001), (401, 70001), (402, 70002)]:
        failures.append(f"boot ordinal (#241): a citation later in the line, or an unlabelled "
                        f"reading, was mis-filed — got {sorted(g_)}, wanted both #401 readings "
                        f"under 401 and the bare pre-flight under its #402 stratum")

    # ---- THE ARITHMETIC ARM: drive the real check against the DERIVED band (`s240-D1`).
    # n readings ON one figure ⇒ spread 0, delta 0 ⇒ green; the same log plus a fat delta line
    # must STAY green, because the delta is not a sample. And one reading per SESSION, never per
    # line: the same session stating its figure twice must not enter the window twice (#240).
    try:
        sys.path.insert(0, HERE)
        import _gauge_tokens as gt
        window, ceiling = gt.BOOT_BAND_WINDOW, gt.BOOT_CEILING_TK
    except Exception as e:                                            # noqa: BLE001
        SELFTEST_REFUSALS.append(f"boot-delta arithmetic arm: _gauge_tokens unreadable ({e})")
        return failures
    # ⚠ UNDER the ceiling on purpose — this arm tests the BAND arithmetic, and a fixture that
    # also breached the ceiling would fail for the other reason and prove nothing about it.
    flat = ceiling - 1_000
    base = 300 + BOOT_CEILING_FROM_SESSION      # every fixture session is POST-diet
    readings = "\n".join(f"> **pre-flight #{n}:** boot {flat:,} real"
                         for n in range(base, base + window))
    for extra, label in (("", f"{window} readings on one figure"),
                         (f"\n> ⚠ boot {flat * 2:,} over the band, DECLARED", "…plus a DELTA"),
                         ("\n> ⚠ a boot drift of 99,999 was declared at the opener",
                          "…plus a drift-of line"),
                         (f"\n> **post-mortem #{base + window - 1}:** boot {flat:,} real",
                          "…plus the SAME session's figure restated (#240 dedupe)")):
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, "notes"))
            with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
                f.write(readings + extra + "\n")
            f_, n_ = boot_constant_drift_check(td)
            if f_:
                failures.append(f"boot-drift arithmetic ({label}): the gate FAILED on a log whose "
                                f"readings are identical and under the ceiling — {f_[0][:150]}")
            if extra and "post-mortem" not in extra and not any(
                    "state a DRIFT beside" in x for x in n_):
                failures.append(f"boot-drift arithmetic ({label}): the delta was skipped SILENTLY "
                                f"— a number this gate declines to count must be named")
    # ---- AND THE BAND MUST BITE ON A STEP, AND NOT ON DRIFT (`s240-D1`'s whole clause, driven
    # in BOTH directions — a check proven only in the red direction has not been proven).
    # SLOW DRIFT: each session +40 on a ~1,300 spread ⇒ inside the band ⇒ GREEN, no re-base.
    drift_log = "\n".join(
        f"> **pre-flight #{base + i}:** boot {flat - 600 + i * 200:,} real"
        for i in range(window))
    # STEP CHANGE: the same series, newest jumped 6,000 ⇒ outside the spread ⇒ RED.
    step_log = "\n".join(
        f"> **pre-flight #{base + i}:** "
        f"boot {(flat - 600 + i * 200) - (6_000 if i == window - 1 else 0):,} real"
        for i in range(window))
    for src, want_red, label in ((drift_log, False, "slow drift"),
                                 (step_log, True, "step change")):
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, "notes"))
            with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
                f.write(src + "\n")
            f_, _n_ = boot_constant_drift_check(td)
            got_red = any("STEP CHANGE" in x for x in f_)
            if got_red != want_red:
                failures.append(
                    f"boot-drift band (`s240-D1`, {label}): expected "
                    f"{'RED' if want_red else 'GREEN'}, got fails={[x[:110] for x in f_]}")

    # ---- AND THE CEILING MUST BITE, BY NAME. Same fixture, one reading over `BOOT_CEILING_TK`.
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        with open(os.path.join(td, "notes", "_GAUGE-LOG.md"), "w", encoding="utf-8") as f:
            f.write(readings
                    + f"\n> **pre-flight #{base + window}:** boot {ceiling + 1:,} real\n")
        f_, n_ = boot_constant_drift_check(td)
        if not any("CEILING BREACH" in x for x in f_):
            failures.append(f"boot-drift ceiling (`s241-D1`): a post-diet reading of "
                            f"{ceiling + 1:,} did NOT fail the shrink-only ceiling by name — "
                            f"fails={[x[:90] for x in f_]}")
    return failures


def selftest_regen_serial():
    """★ #221 — THE REGEN-SERIAL COMPLETENESS CHECK, DRIVEN IN BOTH DIRECTIONS.

    Every arm runs the REAL `regen_serial_check` against a REAL git repo whose `_build_all.py`
    carries a REAL `STEPS` list — the parse is half of what is being tested, so a hand-built dict
    would grade the wrong thing [[mutation-tests-the-clause-not-the-feature]]. The #210 shape (a
    wave that skips a member INSIDE its own span) is planted and then REMOVED, so the arm is shown
    red AND green rather than only red.
    """
    failures = []
    steps_src = (
        "STEPS = [\n"
        "    ('ramp', 'gen_ramp_fixture.py'),\n"
        "    ('middle', 'gen_middle_fixture.py'),\n"
        "    ('later', 'gen_later_fixture.py'),\n"
        "    ('index', '_build_memento_index.py'),\n"
        "]\n")
    with tempfile.TemporaryDirectory() as td:
        git = ["git", "-C", td, "-c", "user.email=t@t", "-c", "user.name=t"]
        try:
            if subprocess.run(git[:3] + ["init", "-q"], capture_output=True,
                              timeout=30).returncode != 0:
                raise RuntimeError("git init failed")
        except Exception as e:                                        # noqa: BLE001
            SELFTEST_REFUSALS.append(f"regen-serial: git unavailable in this checkout ({e})")
            return failures

        def put(rel, body):
            p = os.path.join(td, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(body)
            return p

        def art(script, n=1):
            return f"# fixture\n*Generated 2026-08-27 by `{script}`.*\n{'x' * n}\n"

        put("knowledge/_build_all.py", steps_src)
        put("knowledge/_RAMP.md", art("gen_ramp_fixture.py"))
        put("knowledge/_MIDDLE.md", art("gen_middle_fixture.py"))
        put("knowledge/_LATER.md", art("gen_later_fixture.py"))
        put("knowledge/_INDEX.md", art("_build_memento_index.py"))
        put("notes/plain.md", "no banner here, nothing claims this file\n")
        subprocess.run(git + ["add", "-A"], capture_output=True, timeout=30)
        subprocess.run(git + ["commit", "-qm", "fixture base"], capture_output=True, timeout=30)
        sha = (_git_out(td, "rev-parse", "HEAD") or "").strip()
        if not sha:
            SELFTEST_REFUSALS.append("regen-serial: the fixture repo took no commit")
            return failures

        # ---- ARM 0, THE SERIAL PARSE ITSELF: order is READ from STEPS, never assumed.
        pos, err = _regen_serial_positions(td)
        if err or not pos or pos.get("gen_ramp_fixture.py") != 0 \
                or pos.get("_build_memento_index.py") != 3:
            failures.append(f"regen-serial: `STEPS` did not parse into positions — err={err} "
                            f"pos={pos}. Every arm below reads order from this parse.")
            return failures

        # ---- GREEN CONTROL (attribute-the-diff): a wave touching nothing owned says so, quietly.
        put("notes/plain.md", "edited, still claimed by nobody\n")
        w_, n_ = regen_serial_check(td, sha=sha)
        if w_ or not any("no regen wave in evidence" in x for x in n_):
            failures.append(f"regen-serial CONTROL: a wave with no serial artefact in it did not "
                            f"read as 'no regen wave' — warns={w_[:1]} notes={n_[:1]}. Every red "
                            f"below would be unattributable.")

        # ---- ARM 1, THE #210 SHAPE: ramp + later + index re-run, the MIDDLE member skipped.
        for rel, script in (("knowledge/_RAMP.md", "gen_ramp_fixture.py"),
                            ("knowledge/_LATER.md", "gen_later_fixture.py"),
                            ("knowledge/_INDEX.md", "_build_memento_index.py")):
            put(rel, art(script, 2))
        w_, _n = regen_serial_check(td, sha=sha)
        if not any("NOT re-run" in x and "gen_middle_fixture.py" in x for x in w_):
            failures.append(f"regen-serial: a wave that SKIPPED `gen_middle_fixture.py` inside its "
                            f"own span passed — this is the #210 subset defect exactly, and the "
                            f"check is blind to it: {w_}")

        # ---- ARM 2 (mutation control): re-run the skipped member; the warn must CLEAR.
        put("knowledge/_MIDDLE.md", art("gen_middle_fixture.py", 2))
        w_, _n = regen_serial_check(td, sha=sha)
        if any("NOT re-run" in x for x in w_):
            failures.append(f"regen-serial: the membership warn did NOT clear when the whole "
                            f"serial was run — the check fires on everything and so proves "
                            f"nothing: {w_}")

        # ---- ARM 3, `index last`: the index left behind must be named, and named SPECIFICALLY.
        subprocess.run(git + ["add", "-A"], capture_output=True, timeout=30)
        subprocess.run(git + ["commit", "-qm", "full serial"], capture_output=True, timeout=30)
        sha2 = (_git_out(td, "rev-parse", "HEAD") or "").strip()
        put("knowledge/_RAMP.md", art("gen_ramp_fixture.py", 3))
        put("knowledge/_MIDDLE.md", art("gen_middle_fixture.py", 3))
        w_, _n = regen_serial_check(td, sha=sha2)
        if not any("_build_memento_index.py" in x and "did NOT re-run" in x for x in w_):
            failures.append(f"regen-serial: a wave that regenerated members and left the memento "
                            f"index behind passed — `index last` is unenforced: {w_}")

        # ---- ARM 4, ORDER, and it is the arm that must not overclaim. The wave is UNCOMMITTED,
        # so mtimes testify: ramp stamped AFTER the index is a serial run backwards.
        put("knowledge/_INDEX.md", art("_build_memento_index.py", 3))
        base = os.path.getmtime(os.path.join(td, "knowledge/_MIDDLE.md"))
        os.utime(os.path.join(td, "knowledge/_RAMP.md"), (base + 50, base + 50))
        os.utime(os.path.join(td, "knowledge/_INDEX.md"), (base - 50, base - 50))
        w_, _n = regen_serial_check(td, sha=sha2)
        if not any("OUT OF ORDER" in x for x in w_):
            failures.append(f"regen-serial: the ramp regenerated AFTER the index did not read as "
                            f"out of order — `ramp first, index last` is unenforced: {w_}")

        # ---- ARM 5 (mutation control): stamp them in STEPS order; the order warn must CLEAR.
        for i, rel in enumerate(("knowledge/_RAMP.md", "knowledge/_MIDDLE.md",
                                 "knowledge/_INDEX.md")):
            os.utime(os.path.join(td, rel), (base + i, base + i))
        w_, n_ = regen_serial_check(td, sha=sha2)
        if any("OUT OF ORDER" in x for x in w_):
            failures.append(f"regen-serial: an in-order wave was called out of order — the order "
                            f"arm fires on everything: {w_}")
        if not any("order arm OBSERVABLE" in x for x in n_):
            failures.append(f"regen-serial: an uncommitted, in-order wave did not report the order "
                            f"arm as OBSERVABLE — silence here is indistinguishable from a skip: "
                            f"{n_}")

    # ---- ARM 6: no serial home ⇒ a DECLARED skip, never a green. [[a-crash-is-not-a-fail]]
    with tempfile.TemporaryDirectory() as td:
        w_, n_ = regen_serial_check(td)
        if w_ or not any("SKIPPED" in x and "NOT a pass" in x for x in n_):
            failures.append(f"regen-serial: a tree with no `_build_all.py` must SKIP OUT LOUD — "
                            f"warns={w_} notes={n_}")

    # ---- ARM 7 (tier pin, the M10 pattern): ADVISORY AT BIRTH. It must reach the wrap's WARNS
    # and never its FAILS — a silent promotion by an agent is what this pin exists to catch.
    if REGEN_SERIAL_BLOCKING:
        failures.append("regen-serial: REGEN_SERIAL_BLOCKING is True — this check was promoted "
                        "to blocking without Dave's word. Promotion is HIS, not an edit's.")
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
            f.write("Last refreshed: 2026-07-27\n")
        f_, w_, n_ = wrap_checks(td, datetime.date(2026, 7, 27), lane=True)
        if any("REGEN SERIAL" in x for x in f_):
            failures.append("regen-serial: the check reached the wrap's FAILS — it is ADVISORY at "
                            "birth and its promotion is Dave's word, not an edit")
        if not any("REGEN SERIAL" in x for x in list(w_) + list(n_)):
            failures.append(f"regen-serial: the check is not wired into wrap_checks at all — an "
                            f"instrument with no consumer cannot fail: {(list(w_) + list(n_))[:2]}")
    return failures


def selftest_shared_helper_dedup():
    """★ #221 — THE SHARED-HELPER COMPARER, DRIVEN BOTH WAYS, INCLUDING THE GREP TRAP.

    The arm that matters most is the one where a `def mask_comments` sits INSIDE A STRING: a
    grep-shaped implementation would call that a duplicate and cry wolf, and a gate that cries
    wolf gets switched off. Parsing in the consumer's own grammar is the claim, so it is the claim
    that gets tested [[no-gate-parses-the-artefact]].
    """
    failures = []
    with tempfile.TemporaryDirectory() as td:
        git = ["git", "-C", td, "-c", "user.email=t@t", "-c", "user.name=t"]
        try:
            if subprocess.run(git[:3] + ["init", "-q"], capture_output=True,
                              timeout=30).returncode != 0:
                raise RuntimeError("git init failed")
        except Exception as e:                                        # noqa: BLE001
            SELFTEST_REFUSALS.append(f"shared-helper: git unavailable in this checkout ({e})")
            return failures

        def put(rel, body):
            p = os.path.join(td, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(body)
            subprocess.run(git + ["add", rel], capture_output=True, timeout=30)
            return p

        put("knowledge/_htmlmask.py", "def mask_comments(html):\n    return html\n")
        put("knowledge/gen_one.py", "from _htmlmask import mask_comments\nx = mask_comments('a')\n")

        # ---- GREEN CONTROL (attribute-the-diff): one home, one legal importer.
        w_, n_ = shared_helper_dedup_check(td)
        if w_ or not any("exactly ONE implementation" in x for x in n_):
            failures.append(f"shared-helper CONTROL: a single-implementation tree did not read "
                            f"clean — warns={w_[:1]} notes={n_[:1]}; every red below would be "
                            f"unattributable")

        # ---- ARM 1, THE W-92 SHAPE RE-OPENING BY ADDITION: a second implementation appears.
        dup = put("knowledge/gen_two.py", "def mask_comments(html):\n    return html.upper()\n")
        w_, _n = shared_helper_dedup_check(td)
        if not any("may have ONE" in x and "gen_two.py" in x for x in w_):
            failures.append(f"shared-helper: a SECOND `def mask_comments` passed — the comparer is "
                            f"blind to the exact defect it was built for: {w_}")

        # ---- ARM 2 (mutation control): remove the duplicate; the warn must CLEAR.
        os.remove(dup)
        subprocess.run(git + ["rm", "-q", "--cached", "knowledge/gen_two.py"],
                       capture_output=True, timeout=30)
        w_, _n = shared_helper_dedup_check(td)
        if any("may have ONE" in x for x in w_):
            failures.append(f"shared-helper: the duplicate warn did NOT clear once the duplicate "
                            f"was gone — the check fires on everything: {w_}")

        # ---- ARM 3, THE GREP TRAP: a `def mask_comments` inside a STRING is not an implementation.
        put("knowledge/gen_doc.py",
            'HELP = """\ndef mask_comments(html):\n    ...\n"""\n# a docstring, not a definition\n')
        w_, _n = shared_helper_dedup_check(td)
        if any("may have ONE" in x for x in w_):
            failures.append(f"shared-helper: a `def mask_comments` inside a STRING was counted as "
                            f"a duplicate — this comparer is grep-shaped, not ast-shaped, and "
                            f"will cry wolf until someone switches it off: {w_}")

        # ---- ARM 4: a second ROUTE to the helper is a second implementation waiting to happen.
        put("knowledge/gen_three.py", "from _sneaky import mask_comments\n")
        w_, _n = shared_helper_dedup_check(td)
        if not any("not from `_htmlmask`" in x and "gen_three.py" in x for x in w_):
            failures.append(f"shared-helper: an import of `mask_comments` from the WRONG module "
                            f"passed silently: {w_}")
        os.remove(os.path.join(td, "knowledge/gen_three.py"))
        subprocess.run(git + ["rm", "-q", "--cached", "knowledge/gen_three.py"],
                       capture_output=True, timeout=30)

        # ---- ARM 5: an unparseable file is UNKNOWN, never counted as clean.
        put("knowledge/broken.py", "def mask_comments(  <<< not python\n")
        w_, _n = shared_helper_dedup_check(td)
        if not any("could NOT be parsed" in x and "broken.py" in x for x in w_):
            failures.append(f"shared-helper: an unparseable `.py` was silently skipped — a file "
                            f"the comparer could not read is UNKNOWN, not clean: {w_}")
        os.remove(os.path.join(td, "knowledge/broken.py"))
        subprocess.run(git + ["rm", "-q", "--cached", "knowledge/broken.py"],
                       capture_output=True, timeout=30)

        # ---- ARM 6: the home itself disappearing must be LOUD, not a quiet zero.
        os.remove(os.path.join(td, "knowledge/_htmlmask.py"))
        subprocess.run(git + ["rm", "-q", "--cached", "knowledge/_htmlmask.py"],
                       capture_output=True, timeout=30)
        w_, _n = shared_helper_dedup_check(td)
        if not any("NOTHING in the tracked tree defines it" in x for x in w_):
            failures.append(f"shared-helper: the helper's home vanished and the comparer reported "
                            f"no implementations as if that were fine: {w_}")

    # ---- ARM 7: a tree git cannot answer for is UNKNOWN, never a single implementation.
    with tempfile.TemporaryDirectory() as td:
        w_, n_ = shared_helper_dedup_check(td)
        if not (any("DID NOT RUN" in x for x in w_) or any("SKIPPED" in x for x in n_)):
            failures.append(f"shared-helper: a non-repo tree neither refused nor declared a skip — "
                            f"warns={w_} notes={n_}")

    # ---- ARM 8 (tier pin, the M10 pattern): ADVISORY AT BIRTH; promotion is Dave's word.
    if SHARED_HELPER_BLOCKING:
        failures.append("shared-helper: SHARED_HELPER_BLOCKING is True — promoted to blocking "
                        "without Dave's word. Promotion is HIS, not an edit's.")
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
            f.write("Last refreshed: 2026-07-27\n")
        f_, w_, n_ = wrap_checks(td, datetime.date(2026, 7, 27), lane=True)
        if any("SHARED HELPER" in x for x in f_):
            failures.append("shared-helper: the comparer reached the wrap's FAILS — it is ADVISORY "
                            "at birth and its promotion is Dave's word, not an edit")
        if not any("SHARED HELPER" in x for x in list(w_) + list(n_)):
            failures.append(f"shared-helper: not wired into wrap_checks at all — an instrument "
                            f"with no consumer cannot fail: {(list(w_) + list(n_))[:2]}")
    return failures


def selftest_instrument_stray():
    """★ #218 — THE INSTRUMENT-STRAY GATE, DRIVEN. It had NO selftest for eighty sessions:
    built #138, wired the same day, and never once proven to bite in a test
    [[instrument-without-a-consumer]]. Every arm below runs the REAL `instrument_stray_check`
    against a REAL git repo — a fixture tree with no `.git` only proves the refusal path.

    The `s217-D1` re-scope is driven in BOTH directions (the two-way rule): a ruled product
    must NOT fail, and an instrument signature in the SAME directory must STILL fail.
    """
    failures = []
    surface = "knowledge/assets/photography-web"
    with tempfile.TemporaryDirectory() as td:
        git = ["git", "-C", td, "-c", "user.email=t@t", "-c", "user.name=t"]
        try:
            if subprocess.run(git[:3] + ["init", "-q"], capture_output=True,
                              timeout=30).returncode != 0:
                raise RuntimeError("git init failed")
        except Exception as e:                                        # noqa: BLE001
            SELFTEST_REFUSALS.append(f"instrument-stray: git unavailable in this checkout ({e})")
            return failures

        def put(rel, body="x"):
            p = os.path.join(td, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(body)
            return p

        def drive():
            return instrument_stray_check(td)

        # A committed derivative + a committed control file: the surface must exist as a
        # TRACKED directory, or "untracked" is not the thing being tested.
        put(f"{surface}/already-w1600.jpg")
        put("knowledge/assets/fonts/README.md")
        subprocess.run(git + ["add", "-A"], capture_output=True, timeout=30)
        subprocess.run(git + ["commit", "-qm", "fixture"], capture_output=True, timeout=30)

        # ---- GREEN CONTROL (attribute-the-diff): a clean tree fails nothing and notes nothing.
        f_, w_, n_ = drive()
        if f_ or n_:
            failures.append(f"instrument-stray: a CLEAN tree was not silent — fails={f_[:1]} "
                            f"notes={n_[:1]}; every red below would be unattributable")

        # ---- ARM 1 (#138's original catch, unchanged): a fontconfig stray anywhere under assets.
        p = put("knowledge/assets/fonts/.uuid")
        f_, _w, _n = drive()
        if not any("INSTRUMENT STRAY" in x for x in f_):
            failures.append("instrument-stray: `.uuid` under knowledge/assets did NOT fail — "
                            "the #138 catch is dead")
        os.remove(p)

        # ---- ARM 2 (the re-scope, direction A): ruled products are NOT strays, and say so.
        put(f"{surface}/gettyimages-999-w1600.jpg")
        put(f"{surface}/eyeem-100014108-97994792-w800.webp")
        f_, _w, n_ = drive()
        if f_:
            failures.append(f"instrument-stray: s217-D1 derivatives still FAIL — the re-scope "
                            f"does not bite: {f_}")
        if not any("s217-D1" in x and "COMMITTED SURFACE" in x for x in n_):
            failures.append(f"instrument-stray: the products were exempted SILENTLY — the note "
                            f"must name the ruling and the generator, got {n_}")

        # ---- ARM 3 (the re-scope, direction B — THE ONE THAT MATTERS): an instrument signature
        # inside the committed surface is STILL a fail. A path exemption would swallow this.
        p = put(f"{surface}/.uuid")
        f_, _w, _n = drive()
        if not any("INSTRUMENT STRAY" in x for x in f_):
            failures.append("instrument-stray: `.uuid` INSIDE the committed surface passed — "
                            "the re-scope has become a path exemption, which is the defect")
        os.remove(p)

        # ---- ARM 4: a NON-product under the surface is still a stray. The pattern IS the spec.
        for rel, why in ((f"{surface}/scratch.txt", "wrong extension"),
                         (f"{surface}/photo.jpg", "no -wNNN size suffix")):
            p = put(rel)
            f_, _w, _n = drive()
            if not any("INSTRUMENT STRAY" in x for x in f_):
                failures.append(f"instrument-stray: `{rel}` ({why}) passed — the product pattern "
                                f"is not being applied, the whole directory is")
            os.remove(p)

        # ---- ARM 5 (pass 2, unblinded): a .gitignore CANNOT silence a signature, committed
        # surface or not. This is the #137 refusal made structural, re-driven on the new scope.
        put(".gitignore", ".uuid*\n")
        p = put(f"{surface}/.uuid.LCK")
        f_, _w, _n = drive()
        if not any("INSTRUMENT STRAY" in x for x in f_):
            failures.append("instrument-stray: a gitignored `.uuid.LCK` under the committed "
                            "surface passed — pass 2 has been blinded by .gitignore")
        os.remove(p)
        os.remove(os.path.join(td, ".gitignore"))

    # ---- ARM 6: no git at all ⇒ LOUD UNKNOWN, never a green it did not measure.
    with tempfile.TemporaryDirectory() as td:
        f_, w_, _n = instrument_stray_check(td)
        if f_ or not any("DID NOT RUN" in x for x in w_):
            failures.append(f"instrument-stray: a non-repo tree must warn UNKNOWN, not pass "
                            f"silently — fails={f_} warns={w_}")
    return failures


def selftest_subreport_citation():
    """★ #218 `s218-D7` — THE FILED-REPORT CITATION CHECK, DRIVEN ON A REAL GIT REPO.

    ⛔ Every arm runs the REAL `subreport_citation_check` against a real repo with a real
    `after #NNN` wrap commit in its history. A fixture tree with no `.git` only proves the
    refusal path, and an advisory check that has never been seen to fire is an instrument
    without a consumer [[instrument-without-a-consumer]].

    The two clauses that could quietly become always-true both get a NEGATIVE control:
      · the POPULATION — the template and an `assets/**` file must never enter it;
      · the CITATION SURFACE — a citation in a receipt UNCHANGED since the last wrap must NOT
        count, or the surface is "the whole repo" and the check can never fire.

    ★ #221 adds the COUNTS-PARSE arm. The pattern demanded BARE digits while the skeleton every
    sub is told to copy writes the figures in BACKTICKS, so 37 of 44 filed reports were called
    unparseable for obeying the template. The arm below drives the template's OWN form first —
    a gate must be tested against the instruction it enforces, not against the shape its author
    happened to imagine [[no-gate-parses-the-artefact]] — and keeps four malformed lines RED so
    the widening cannot rot into "anything containing the word COUNTS".
    """
    failures = []
    GOOD = ("# r\n\nCOUNTS: findings 3 · ruling-shaped 1 · UNPROVEN 2\n\n"
            "## RULING-SHAPED QUESTIONS\n\nnone\n\nREPLAY-THESE: none — the stub carries everything.\n")

    # ---- ★ #221, THE COUNTS PARSE. The FIRST fixture is the skeleton's own line, verbatim from
    # `notes/_subreports/_TEMPLATE.md:45` with its backticks — the form the gate used to reject.
    for line, why in (
            ("COUNTS: findings `18` · ruling-shaped `5` · UNPROVEN `4`",
             "the TEMPLATE's own backticked form (`_TEMPLATE.md:45`)"),
            ("COUNTS: findings 18 · ruling-shaped 5 · UNPROVEN 4", "the bare form"),
            ("**COUNTS:** findings **3** · ruling-shaped **1** · UNPROVEN **0**", "a bolded line"),
            ("**COUNTS:** findings 9 · ruling-shaped 7 · UNPROVEN 5 · new gates 19",
             "the three required fields followed by a lane's extra ones")):
        if not SUBREPORT_COUNTS_RE.search(line):
            failures.append(f"COUNTS parse: {why} did NOT parse — `{line[:70]}`. A sub that obeys "
                            f"the skeleton must not be told its COUNTS line is unreadable.")
    # ---- and the mutation control: the widening must not have eaten the specification.
    for line, why in (
            ("COUNTS: findings 18 · UNPROVEN 4", "a MISSING field"),
            ("COUNTS: findings many · ruling-shaped 5 · UNPROVEN 4", "a non-numeric figure"),
            ("COUNTS: ruling-shaped 5 · findings 18 · UNPROVEN 4", "the fields OUT OF ORDER"),
            ("COUNTS: findings 18, ruling-shaped 5, UNPROVEN 4", "comma separators, not `·`")):
        if SUBREPORT_COUNTS_RE.search(line):
            failures.append(f"COUNTS parse: {why} was ACCEPTED — `{line[:70]}`. The decoration was "
                            f"loosened, not the contract; three fields, in order, separated by "
                            f"`·` is still the specification.")
    with tempfile.TemporaryDirectory() as td:
        git = ["git", "-C", td, "-c", "user.email=t@t", "-c", "user.name=t"]
        try:
            if subprocess.run(git[:3] + ["init", "-q"], capture_output=True,
                              timeout=30).returncode != 0:
                raise RuntimeError("git init failed")
        except Exception as e:                                        # noqa: BLE001
            SELFTEST_REFUSALS.append(f"subreport citation: git unavailable in this checkout ({e})")
            return failures

        def put(rel, body="x\n"):
            p = os.path.join(td, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(body)
            return p

        def rm(rel):
            os.remove(os.path.join(td, rel))

        def commit(subject):
            subprocess.run(git + ["add", "-A"], capture_output=True, timeout=30)
            subprocess.run(git + ["commit", "-qm", subject], capture_output=True, timeout=30)

        REPORT_REL = "notes/_subreports/2026-08-25-218-cZ-fixture.md"
        STALE_RECEIPT = "notes/_receipts/2026-08-01-100-prior-session.md"

        # ---- the pre-wrap history: a receipt that ALREADY names the report path (the surface
        # control), the template, and then the wrap commit itself.
        put("notes/_subreports/_TEMPLATE.md", "skeleton\n")
        put(STALE_RECEIPT, f"a PRIOR session's receipt, naming {REPORT_REL} in passing\n")
        commit("#217 2026-08-24 — work")
        put("_LIVE-STATE.md", "Last refreshed: 2026-08-24\n")   # ⚠ a second commit needs a diff
        commit("after #217 2026-08-24 — capture ritual")
        if _last_wrap_commit(td) is None:
            SELFTEST_REFUSALS.append("subreport citation: the fixture repo took no commits in "
                                     "this checkout — every arm below would be vacuous")
            return failures

        # ---- ARM 0, GREEN CONTROL (attribute-the-diff): nothing filed ⇒ no warns, and the
        # note SAYS nothing was filed rather than reporting a clean pass it did not measure.
        w_, n_ = subreport_citation_check(td)
        if w_ or not any("none filed since the last wrap" in x for x in n_):
            failures.append(f"subreport cite: an empty population was not reported as empty — "
                            f"warns={w_[:1]} notes={n_[:1]}; every red below is unattributable")

        # ---- ARM 1, THE RED: a filed report nobody cites. This is the whole check.
        put(REPORT_REL, GOOD)
        w_, _n = subreport_citation_check(td)
        if not any("FILED SUB-REPORT UNCITED" in x and REPORT_REL in x for x in w_):
            failures.append(f"subreport cite: an UNCITED filed report did not warn — the "
                            f"unread-pointer check is dead: {w_}")

        # ---- ARM 2, THE SURFACE CONTROL (the one that matters): the stale receipt names the
        # path VERBATIM and has not changed since the wrap. It must NOT satisfy the citation,
        # or the surface is the whole repo and the check can never fire.
        if REPORT_REL not in open(os.path.join(td, STALE_RECEIPT), encoding="utf-8").read():
            failures.append("subreport cite: ARM 2 fixture is broken — the stale receipt does "
                            "not name the path, so the arm proves nothing")
        elif not any("FILED SUB-REPORT UNCITED" in x for x in subreport_citation_check(td)[0]):
            failures.append("subreport cite: a citation in a receipt UNCHANGED since the last "
                            "wrap satisfied the check — the surface is unscoped, so a PRIOR "
                            "session's prose can green a report this session never opened")

        # ---- ARM 3, THE PASS: a receipt written THIS session, citing by path.
        put("notes/_receipts/2026-08-25-218-crank.md",
            f"this session's receipt · filed report `{REPORT_REL}` read at reconcile\n")
        w_, n_ = subreport_citation_check(td)
        if any("FILED SUB-REPORT UNCITED" in x for x in w_):
            failures.append(f"subreport cite: a report cited by path in THIS session's receipt "
                            f"still warned — the pass path does not exist: {w_}")
        if not any("every one cited by path" in x for x in n_):
            failures.append(f"subreport cite: the clean case left no note naming its surfaces: {n_}")
        rm("notes/_receipts/2026-08-25-218-crank.md")

        # ---- ARM 4: the ★ LATEST banner is a citation surface too, and only the LATEST region.
        put("GOOD-MORNING.md",
            f"> ## ★ LATEST — 2026-08-25 (**#218**, wrap)\n> filed: `{REPORT_REL}`\n\n"
            f"> ## ★ PRIOR — 2026-08-24 (**#217**, wrap)\n> prose\n")
        if any("FILED SUB-REPORT UNCITED" in x for x in subreport_citation_check(td)[0]):
            failures.append("subreport cite: a path cited in the ★ LATEST banner still warned")
        put("GOOD-MORNING.md",
            f"> ## ★ LATEST — 2026-08-25 (**#218**, wrap)\n> prose\n\n"
            f"> ## ★ PRIOR — 2026-08-24 (**#217**, wrap)\n> filed: `{REPORT_REL}`\n")
        if not any("FILED SUB-REPORT UNCITED" in x for x in subreport_citation_check(td)[0]):
            failures.append("subreport cite: a citation in the ★ PRIOR banner counted — the "
                            "banner surface is not scoped to ★ LATEST")
        rm("GOOD-MORNING.md")

        # ---- ARM 5, POPULATION CONTROLS: neither the skeleton nor evidence is a report.
        rm(REPORT_REL)
        put("notes/_subreports/_TEMPLATE.md", "skeleton, EDITED since the wrap\n")
        put("notes/_subreports/assets/2026-08-25-218-cZ-fixture/probe.md", "evidence\n")
        put("notes/_subreports/assets/2026-08-25-218-cZ-fixture/shot.png", "binary-ish\n")
        w_, n_ = subreport_citation_check(td)
        if w_ or not any("none filed" in x for x in n_):
            failures.append(f"subreport cite: the template and `assets/**` entered the "
                            f"population — the glob is wider than the rule: {w_}")

        # ---- ARM 6, THE PARSE HALF, one bite per clause. Control: GOOD warns none of the three.
        for body, marker, why in (
                (GOOD.replace("COUNTS: findings 3 · ruling-shaped 1 · UNPROVEN 2",
                              "COUNTS: three findings, one ruling-shaped, two unproven"),
                 "FILED SUB-REPORT COUNTS", "a PROSE counts line"),
                (GOOD.replace("COUNTS: findings 3 · ruling-shaped 1 · UNPROVEN 2", ""),
                 "FILED SUB-REPORT COUNTS", "no counts line at all"),
                (GOOD.replace("REPLAY-THESE: none — the stub carries everything.", ""),
                 "FILED SUB-REPORT REPLAY", "no REPLAY-THESE line"),
                (GOOD.replace("## RULING-SHAPED QUESTIONS", "## Questions"),
                 "FILED SUB-REPORT QUESTIONS", "the mandatory section renamed away")):
            put(REPORT_REL, body)
            w_, _n = subreport_citation_check(td)
            if not any(marker in x for x in w_):
                failures.append(f"subreport cite: {why} did not warn `{marker}` — the gate does "
                                f"not parse the artefact it grades: {w_}")
        put(REPORT_REL, GOOD)
        w_, _n = subreport_citation_check(td)
        if any(m in x for m in ("COUNTS", "REPLAY", "QUESTIONS") for x in w_):
            failures.append(f"subreport cite: the well-formed skeleton warned on a parse clause "
                            f"— the parser is refusing its own template: {w_}")

        # ---- ARM 7: no `after #<n>` commit in history ⇒ LOUD UNKNOWN, never a silent pass.
        with tempfile.TemporaryDirectory() as td2:
            subprocess.run(["git", "-C", td2, "init", "-q"], capture_output=True, timeout=30)
            os.makedirs(os.path.join(td2, SUBREPORT_DIR))
            with open(os.path.join(td2, REPORT_REL), "w", encoding="utf-8") as f:
                f.write(GOOD)
            w_, _n = subreport_citation_check(td2)
            if not any("DID NOT RUN" in x for x in w_):
                failures.append(f"subreport cite: a repo with no capture-ritual commit must "
                                f"declare UNKNOWN, not pass silently — warns={w_}")

    # ---- ARM 8: no `notes/_subreports/` at all ⇒ DECLARED skip, not a pass.
    with tempfile.TemporaryDirectory() as td:
        w_, n_ = subreport_citation_check(td)
        if w_ or not any("NOT a pass" in x for x in n_):
            failures.append(f"subreport cite: a tree with no sub-report directory must DECLARE "
                            f"the skip — warns={w_} notes={n_}")
    return failures


def _carry_gm(latest_items, prior_items, latest_no=189, prior_no=188):
    """A two-banner GOOD-MORNING fixture whose residual lines carry exactly what is asked."""
    def resid(n, items):
        return "> **residual → #%d:** " % n + " · ".join(items)
    return "\n".join([
        "> ## ★ LATEST — 2026-08-16 (Sun **#%d**, wrap)" % latest_no,
        resid(latest_no + 1, latest_items),
        "",
        "> ## ★ PRIOR — 2026-08-16 (Sun **#%d**, wrap)" % prior_no,
        resid(prior_no + 1, prior_items),
        "",
    ]) + "\n"


def selftest_carry_gate():
    """s188-D2 — THE CARVE-OUT, BOTH DIRECTIONS. Every bite states its CONTROL.

    ⛔ The whole point of the ruling is asymmetry: the SAME wording change passes WITH a
    receipt and is refused WITHOUT one. So every bite here is a PAIR, and the pair differs by
    the receipt alone — otherwise the green proves only that the parser runs.
    """
    failures = []
    WAS = ("⚠ **THE MONDAY SLOT IS UNSCHEDULED [3]** — no scheduler row exists for it, "
           "checked live this session")

    def run(latest_item, prior_item=WAS):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(_carry_gm([latest_item], [prior_item]))
            return carry_wording_check(td)

    # (C1) THE INVARIANT — same wording, age +1 ⇒ silent pass. This is the CONTROL for all below.
    f_, n_ = run(WAS.replace("[3]", "[4]"))
    if f_:
        failures.append(f"carry gate: an UNCHANGED carry aged +1 was refused — the gate is "
                        f"biting the normal case, which would refuse every wrap: {f_}")
    if not any("1 paired" in x or "paired into LATEST" in x for x in n_):
        failures.append(f"carry gate: the unchanged case produced no receipt note: {n_}")

    # (C2) REWORDED, NO RECEIPT ⇒ REFUSED, and the refusal QUOTES both texts.
    f_, _ = run("⚠ **THE MONDAY SLOT IS UNSCHEDULED [4]** — no scheduler row exists for it")
    if not any("WITHOUT A RETRACTION RECEIPT" in x for x in f_):
        failures.append(f"carry gate: a reworded carry with NO receipt was NOT refused — "
                        f"s188-D2's 'refused exactly as today' half is dead: {f_}")
    elif not (any("WAS (#PRIOR)" in x and "NOW (LATEST)" in x for x in f_)):
        failures.append(f"carry gate: the refusal did not quote BOTH texts — a reader cannot "
                        f"see what moved: {f_}")

    # (C3) THE CARVE-OUT — the SAME change, struck WITH a receipt ⇒ ACCEPTED. (C2 is its control.)
    f_, n_ = run("⚠ ~~THE MONDAY SLOT IS UNSCHEDULED~~ **[4]** — **RETRACTED at #182**, the "
                 "slot IS scheduled; correction inscribed at `s183-D1`")
    if f_:
        failures.append(f"carry gate: a retraction WITH its receipt was refused — the s188-D2 "
                        f"carve-out does not exist: {f_}")
    if not any("carries its retraction receipt" in x for x in n_):
        failures.append(f"carry gate: an accepted carve-out left no note naming it: {n_}")

    # (C4) HALF A RECEIPT IS NOT A RECEIPT — each half refused BY NAME. Control: (C3) passes.
    for label, item, want in (
            ("marker + session, no inscription",
             "⚠ ~~THE MONDAY SLOT IS UNSCHEDULED~~ **[4]** — RETRACTED at #182", "WHERE"),
            ("marker + inscription, no session",
             "⚠ ~~THE MONDAY SLOT IS UNSCHEDULED~~ **[4]** — RETRACTED, see `s183-D1`",
             "SESSION"),
            ("changed with NO marker at all",
             "⚠ **THE MONDAY SLOT IS UNSCHEDULED [4]** — corrected, see `s183-D1` at #182",
             "says NOTHING about a retraction")):
        f_, _ = run(item)
        if not any(want in x for x in f_):
            failures.append(f"carry gate: {label} was not refused by name (wanted {want!r}): "
                            f"{f_}")

    # (C5) THE PAIRING KEY MUST BITE BOTH WAYS. An UNRELATED item at the next age is NOT the
    #      same carry and must NOT be graded as a rewording (a false fire here refuses honest
    #      wraps); the near-identical one at the next age MUST be.
    f_, _ = run("⚠ **THE BASE RED 30 IS UNCHANGED [4]** — rag/text/on-dark, 3.14:1")
    if f_:
        failures.append(f"carry gate: an UNRELATED item at age+1 was graded as a rewording — "
                        f"the similarity guard is not holding: {f_}")
    f_, _ = run(WAS.replace("[3]", "[9]"))          # right wording, WRONG age ⇒ no pair
    if f_:
        failures.append(f"carry gate: a carry whose age did not go +1 was paired anyway: {f_}")

    # (C6) NO GM / NO RESIDUAL ⇒ DECLARED UNMEASURED, never a silent clean run.
    with tempfile.TemporaryDirectory() as td:
        f_, n_ = carry_wording_check(td)
        if f_ or not any("UNMEASURED" in x for x in n_):
            failures.append(f"carry gate: a missing GOOD-MORNING.md must DECLARE unmeasured: "
                            f"fails={f_} notes={n_}")
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write("> ## ★ LATEST — (#189)\n> prose\n\n> ## ★ PRIOR — (#188)\n> prose\n")
        f_, n_ = carry_wording_check(td)
        if f_ or not any("UNMEASURED" in x for x in n_):
            failures.append(f"carry gate: banners with no residual line must DECLARE "
                            f"unmeasured: fails={f_} notes={n_}")

    # (C7) POINTER MODE — s225-D2 moved the lists to `_CARRIES.md` and left POINTERS on both
    #      GM banners; the #225 wrap measured the gate going quiet on exactly that shape.
    #      Each bite is again a PAIR with its control, and the resolver's refusals are driven
    #      too — a pointer to nothing must be a FAIL, never a clean-looking `0 aged carries`.
    PTR = ("⛔ **THIS LINE IS A POINTER, NOT THE LIST** — the set lives at `_CARRIES.md` "
           "§ `## residual → #%d`")

    def run_ptr(latest_item, prior_item=WAS, carries=True, sections=(190, 189)):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(_carry_gm([PTR % 190], [PTR % 189]))
            if carries:
                body = []
                if 190 in sections:
                    body.append("> **residual → #190:** " + latest_item)
                if 189 in sections:
                    body.append("> **residual → #189:** " + prior_item)
                with open(os.path.join(td, CARRIES_FILE), "w", encoding="utf-8") as f:
                    f.write("# carries\n\n## residual → #190\n\n%s\n" % "\n\n".join(body))
            return carry_wording_check(td)

    # (C7a) CONTROL — unchanged carry aged +1, lists in _CARRIES.md ⇒ silent pass, resolver
    #        notes name the crossing, and the pair is COUNTED (a `0 aged carries` here is the
    #        #225 blindness reborn behind the resolver).
    f_, n_ = run_ptr(WAS.replace("[3]", "[4]"))
    if f_:
        failures.append(f"carry gate (pointer): an UNCHANGED carry aged +1 across files was "
                        f"refused: {f_}")
    if not any("resolved from its GM pointer" in x for x in n_):
        failures.append(f"carry gate (pointer): the resolver left no note naming the "
                        f"crossing: {n_}")
    if not any("1 paired" in x or "paired into LATEST" in x for x in n_):
        failures.append(f"carry gate (pointer): the resolved pair was not counted — the gate "
                        f"is quiet behind the pointer, the exact #225 blindness: {n_}")

    # (C7b) REWORDED IN _CARRIES.md, NO RECEIPT ⇒ REFUSED — the invariant crossed files intact.
    f_, _ = run_ptr("⚠ **THE MONDAY SLOT IS UNSCHEDULED [4]** — no scheduler row exists for it")
    if not any("WITHOUT A RETRACTION RECEIPT" in x for x in f_):
        failures.append(f"carry gate (pointer): a reworded carry behind the pointer was NOT "
                        f"refused — s188-D2 did not survive the s225-D2 move: {f_}")

    # (C7c) POINTER, NO _CARRIES.md AT ALL ⇒ FAIL naming UNREACHABLE. Control: (C7a).
    f_, _ = run_ptr(WAS.replace("[3]", "[4]"), carries=False)
    if not any("UNREACHABLE" in x for x in f_):
        failures.append(f"carry gate (pointer): a pointer with no {CARRIES_FILE} must FAIL "
                        f"naming the unreachable set, never pass on an absence: {f_}")

    # (C7d) POINTER WHOSE SECTION IS MISSING ⇒ FAIL naming UNREACHABLE. Control: (C7a).
    f_, _ = run_ptr(WAS.replace("[3]", "[4]"), sections=(189,))
    if not any("UNREACHABLE" in x for x in f_):
        failures.append(f"carry gate (pointer): a pointer whose `residual → #N` list line is "
                        f"absent from {CARRIES_FILE} must FAIL by name: {f_}")
    return failures


# ⛔ #194 — THE SELFTEST'S COULD-NOT-ASK CHANNEL, one home for the whole suite.
# Sub-suites return `list[str]` of FAILURES and that contract is untouched; an arm that discovers
# its INPUT is unreachable appends here instead, and `_selftest_body()` turns a run that has only
# refusals into exit 77 with a marked line naming each one. Module-level because the sub-suites
# are called as a flat sum expression; CLEARED at the top of every body so a second call in one
# process cannot inherit the first's refusals.
SELFTEST_REFUSALS: list = []


def _selftest_body():
    SELFTEST_REFUSALS.clear()
    failures = (selftest_carry_gate()          # ★ s188-D2 — the 2c carve-out, both directions
                + selftest_instrument_stray()    # ★ #218 — #138's gate, driven at last + s217-D1
                + selftest_argv_contract()       # ★ #218 — the #158 write-by-default class
                + selftest_boot_delta_parse()    # ★ #218 — a delta beside `boot` is not a boot
                + selftest_governing_join()      # ★ #218 — #212 finding 3, ADVISORY at birth
                + selftest_regen_serial()        # ★ #221 — the ordered serial, whole per wave
                + selftest_shared_helper_dedup() # ★ #221 — W-92's residual: ONE implementation
                + selftest_subreport_citation()  # ★ #218 `s218-D7` — the unread-pointer check
                + selftest_plan_block_check()    # B2 seam obligation, s179-D1 — wired at write
                + selftest_real_tier_reachable()
                + selftest_preflight() + selftest_preflight_tokens()
                + selftest_gauge_refusal_seam()          # #79-D1 paired half
                + selftest_budgets() + selftest_strata_exempt() + selftest_units()
                + selftest_cross_instrument_units()       # ds-021 (C), RULED #81-D1
                + selftest_retired_unit_prose()           # ds-021 (C), the `.md` arm
                + selftest_bare_token()
                + selftest_gauge_continuity() + selftest_unkeyed()
                + selftest_subs_line()                    # ★ #168 — the optional `subs` line
                + selftest_growth() + selftest_usage()
                + selftest_lanes() + selftest_receipts() + selftest_index_freshness()
                + selftest_stale_top()                    # ★ s161-D4, RULED #161
                + selftest_handoff_history()
                + selftest_rehearsal())    # #92 — wired HERE, at write time: a suite a new
                                           # tier silently bypasses is #82's defect verbatim
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
        # ★ A REAL RED OUTRANKS A REFUSAL. If anything actually failed, the refusals are still
        # PRINTED (never swallowed) but the exit code is 1: a refusal must never be the reason a
        # measured failure went unreported, which is the one way this convention could do harm.
        for x in failures:
            print(f"  ❌ selftest: {x}")
        for x in SELFTEST_REFUSALS:
            print(f"  ⊘ selftest COULD-NOT-ASK (not counted): {x}")
        return 1
    if SELFTEST_REFUSALS:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import _could_not_ask as cna
        print(f"  ⊘ capture-gate selftest: every reachable arm passed; "
              f"{len(SELFTEST_REFUSALS)} arm(s) could not be asked in this checkout")
        return cna.refuse(
            "_capture_gate.py --selftest",
            f"{len(SELFTEST_REFUSALS)} arm(s) read an input this checkout cannot hold — "
            + " · ".join(SELFTEST_REFUSALS)
            + " ⇒ THIS IS NOT A SKIP: every other arm passed here, and these arms have their "
              "proof of record on a tree that carries the ignored artefacts (a working session's "
              "own repo), never on a bare clone.")
    print("  ✅ capture-gate selftest: all failure classes bite; green control passes")
    return 0


# ---------------------------------------------------------------- the argv contract (#218)
# ★★ THE #158 WRITE-BY-DEFAULT CLASS, BOTH ITS LEGS, CLOSED ON THIS SCRIPT.
#
# ⛔ WHAT WAS ACTUALLY MEASURED, because the carried finding named the wrong door and a wrong
# premise is worth more corrected than repeated [[premise-ages-faster-than-rule]]. The #218 wrap
# recorded "`--selftest` WRITES `_CAPTURE-GATE.md`". DRIVEN at #218's gates wave with a CONTENT
# CANARY in the report file: `--selftest`, `--rehearse` and `--wrap` all left the canary intact —
# none of them writes. `--selftest` passes `report=None` explicitly and both wrap-shaped modes are
# nulled inside `run()` by `S-D3`. THE REAL DOOR IS ARGV ITSELF, and it is two doors:
#   (a) THE BARE RUN. `python3 knowledge/_capture_gate.py` with no argument at all fell through
#       to build mode and rewrote the committed report. A bare run is not a stated intention —
#       #158 residual ⑤, the no-args leg, and the same shape that let `_audit_props_axes.py`
#       overwrite a dated review artefact.
#   (b) THE UNKNOWN FLAG, which is the wider half and had never been named: argv carried NO
#       CONTRACT, so ANY unrecognised token — `--check`, `--dry-run`, a typo'd `--warp` — was
#       silently taken as "build mode" and WROTE. That is #157's gen_showroom defect exactly
#       (an unrecognised argv entry taken as a filter because nothing parsed argv).
# ⇒ The write now lives behind ONE explicitly-named flag, `--build`, and every other argv shape
# either does something read-shaped or REFUSES loud and named. Marker strings are stable so a
# test can assert them: `REFUSED (write-gate)` (the no-args leg, the project's own #158 marker)
# and `REFUSED (argv contract)` (the unknown/ambiguous leg).
CG_MODES = ("--build", "--wrap", "--rehearse", "--selftest")
# `--warns-full` (s241-D2): the escape hatch for the D1/S7 warn delta — prints every warn
# body even when it has not moved since the last logged run. It is a MODIFIER, never a mode:
# the delta is the default because the default is what gets paid for 59 times a day.
CG_MODIFIERS = ("--lane", "--warns-full")
CG_FLAGS = CG_MODES + CG_MODIFIERS
CG_USAGE = ("legal argv: `--build` (the ONLY writing mode — regenerates knowledge/_CAPTURE-GATE.md) "
            "· `--wrap [--lane]` (stdout only, S-D3) · `--rehearse [--lane]` (stdout + the "
            "rehearsal log) · `--selftest` · `--warns-full` (modifier: unchanged "
            "warns print their bodies too, `s241-D2`) · `--help`")
ARGV_REFUSAL_MARKER = "REFUSED (argv contract)"

# ★★ #221 — THE THIRD LEG OF THE #158 WRITE-BY-DEFAULT CLASS: A SELFTEST AIMED AT THE REAL FILE.
#
# ⛔ THE PREMISE THAT AGED, RECORDED BECAUSE A CORRECTED ONE IS WORTH MORE THAN A REPEATED ONE
# [[premise-ages-faster-than-rule]]. Every #221 lane was briefed that `--selftest` WRITES the
# tracked `knowledge/_CAPTURE-GATE.md` and told to restore it afterwards. DRIVEN at #221: it does
# not. `--selftest` passes `report=None`, both wrap modes are nulled by S-D3, and the two argv
# legs refuse. Measured three ways on the real file — md5 identical before and after a full run,
# mtime unmoved, `git status` clean — plus a filesystem-hook probe that counted ZERO python-level
# `open(w)`/`remove`/`rename`/`copy` calls aimed at that path across a whole selftest.
#
# ⇒ SO WHY THIS EXISTS. The argv contract closes the doors that EXIST; it cannot close the door a
# future arm OPENS. `selftest()` calls `run()` many times, and the only thing standing between an
# arm that passes `report=REPORT` (a copy-paste from the `--build` arm, say) and a transient
# verdict landing in a committed report is an author remembering. That is the #158 class itself —
# a write reachable without a stated intention — and a class fix must make it IMPOSSIBLE, not
# unlikely [[gate-dont-patch]]. A pure function, so it can be TESTED rather than trusted, and so
# the test needs no write to prove the refusal.
_SELFTEST_ACTIVE = False
SELFTEST_WRITE_MARKER = "REFUSED (selftest write-door)"


def selftest_write_veto(report):
    """A refusal string if this write must not happen, else None.

    The ONE rule: while a selftest is running, the TRACKED report is off limits. Scratch paths
    (the canary fixtures) stay writable — a selftest that cannot write anywhere could not prove
    `--build` still works.
    """
    if not _SELFTEST_ACTIVE or not report:
        return None
    try:
        same = os.path.realpath(report) == os.path.realpath(REPORT)
    except OSError:                                                   # noqa: BLE001
        same = os.path.abspath(report) == os.path.abspath(REPORT)
    if not same:
        return None
    return (f"✖ {SELFTEST_WRITE_MARKER}: a selftest arm aimed a report write at the TRACKED "
            f"{REPORT}. Selftests write to scratch fixtures, never to the committed artefact "
            f"(#158 write-by-default class, selftest leg). The write was REFUSED, not silently "
            f"skipped — point the arm at a tempdir canary instead.")


def argv_refusal(argv):
    """The contract, as a pure function so it can be TESTED rather than trusted.

    Returns a refusal string for an argv this script must not act on, or None to proceed.
    ⚠ Order matters and is deliberate: an UNKNOWN flag is named before anything else, because
    the unknown flag is the one that used to be silently absorbed into a write.
    """
    if any(a in ("-h", "--help", "--usage") for a in argv):
        return None            # help_gate owns those and has already exited 0 in a real run
    args = list(argv)
    unknown = [a for a in args if a not in CG_FLAGS]
    if unknown:
        return (f"✖ {ARGV_REFUSAL_MARKER}: unrecognised argument(s) "
                f"{', '.join(repr(a) for a in unknown)}. This script used to treat ANY "
                f"unrecognised argv as build mode and WRITE the committed report (#158 "
                f"write-by-default class, unknown-flag leg; #157's gen_showroom defect). "
                f"Refusing instead. {CG_USAGE}")
    if not args:
        return (f"✖ REFUSED (write-gate): _capture_gate.py WRITES {REPORT} in build mode and was "
                f"invoked with NO ARGUMENTS. A bare run is not a stated intention (#158 "
                f"write-by-default class, no-args leg). Pass `--build` to confirm the write, or "
                f"`--wrap` / `--rehearse` / `--selftest` for the read-shaped runs. {CG_USAGE}")
    modes = [a for a in CG_MODES if a in args]
    if not modes:
        return (f"✖ {ARGV_REFUSAL_MARKER}: `--lane` is a MODIFIER, not a mode — on its own it "
                f"would have fallen through to build mode and written {REPORT}. Say which run "
                f"you mean. {CG_USAGE}")
    if len(modes) > 1:
        return (f"✖ {ARGV_REFUSAL_MARKER}: more than one mode asked for "
                f"({', '.join(modes)}) — refusing rather than picking one silently. {CG_USAGE}")
    if "--lane" in args and modes[0] not in ("--wrap", "--rehearse"):
        return (f"✖ {ARGV_REFUSAL_MARKER}: `--lane` modifies the WRAP seam (S-D2) and means "
                f"nothing beside `{modes[0]}`. {CG_USAGE}")
    return None


def main(argv):
    """The single entry point. Every write this script can perform is downstream of here."""
    refusal = argv_refusal(argv)
    if refusal:
        sys.stderr.write(refusal + "\n")
        return 2
    lane = "--lane" in argv
    if "--selftest" in argv:
        return selftest()
    if "--rehearse" in argv:
        # #92: the wrap gate run EARLY, mid-window, where a fix is cheap. Same seam as --wrap;
        # only classification, terseness and the log differ. Consumer: _checkin.py.
        return run(rehearse=True, lane=lane, warns_full="--warns-full" in argv)
    if "--wrap" in argv:
        return run(mode="wrap", lane=lane, warns_full="--warns-full" in argv)
    return run(mode="build")     # `--build`, and ONLY `--build`, reaches the report writer


def selftest_argv_contract():
    """★ #218 — THE ARGV CONTRACT, DRIVEN, AND THE WRITE PROVEN NOT TO HAPPEN.

    ⛔ Not a string check: each read-shaped argv is run against a REAL fixture repo with a
    CONTENT CANARY in the report path, and the canary is re-read afterwards. A gate that only
    asserted `report is None` would be grading its own bookkeeping, not the file on disk
    [[mutation-tests-the-clause-not-the-feature]].
    """
    failures = []
    # ---- the refusal half: every shape that used to reach a write must now refuse.
    for argv, marker, why in (
            ([], "REFUSED (write-gate)", "the bare run (no-args leg)"),
            (["--check"], ARGV_REFUSAL_MARKER, "an unknown flag (the silent-absorb leg)"),
            (["--warp"], ARGV_REFUSAL_MARKER, "a typo'd mode"),
            (["--lane"], ARGV_REFUSAL_MARKER, "a modifier with no mode"),
            (["--build", "--wrap"], ARGV_REFUSAL_MARKER, "two modes at once"),
            (["--build", "--lane"], ARGV_REFUSAL_MARKER, "--lane on a non-wrap mode"),
            (["--wrap", "--nope"], ARGV_REFUSAL_MARKER, "a good flag beside a bad one")):
        got = argv_refusal(argv)
        if not got or marker not in got:
            failures.append(f"argv contract: {why} ({argv}) was NOT refused with `{marker}` — "
                            f"got {got!r}. This argv reaches the report writer.")
    # ---- the proceed half (mutation control): the legal shapes must NOT be refused.
    for argv in ([ "--build"], ["--wrap"], ["--wrap", "--lane"], ["--rehearse"],
                 ["--rehearse", "--lane"], ["--selftest"], ["--help"], ["--wrap", "--help"]):
        if argv_refusal(argv):
            failures.append(f"argv contract: legal argv {argv} was REFUSED "
                            f"({argv_refusal(argv)[:90]}) — the contract is too tight")
    # ---- the canary half: prove the read-shaped modes leave the report file untouched.
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes"))
        with open(os.path.join(td, "_LIVE-STATE.md"), "w", encoding="utf-8") as f:
            f.write("Last refreshed: 2026-07-25\n")
        with open(os.path.join(td, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write("header dated 2026-07-25 (stale)\n")
        canary_path = os.path.join(td, "_CG-CANARY.md")
        stale = datetime.date(2026, 7, 27)
        for kwargs, label in ((dict(mode="wrap"), "--wrap"),
                              (dict(rehearse=True), "--rehearse")):
            with open(canary_path, "w", encoding="utf-8") as f:
                f.write("CANARY\n")
            run(repo=td, report=canary_path, today=stale, **kwargs)
            if open(canary_path, encoding="utf-8").read().strip() != "CANARY":
                failures.append(f"argv contract: `{label}` OVERWROTE the report file — S-D3 "
                                f"regressed and a transient verdict is sitting in a committed "
                                f"report")
        # and the write path must actually write, or the flag is a lie
        with open(canary_path, "w", encoding="utf-8") as f:
            f.write("CANARY\n")
        run(mode="build", repo=td, report=canary_path, today=stale)
        if open(canary_path, encoding="utf-8").read().strip() == "CANARY":
            failures.append("argv contract: `--build` did NOT write the report — the one "
                            "explicit write path is dead, so the build's own report will rot")

    # ---- ★ #221, THE SELFTEST LEG. Driven as a PURE FUNCTION, on purpose: proving "a selftest
    # cannot write the tracked report" by letting a selftest try to write the tracked report
    # would, if the guard were broken, destroy the very artefact under test. The veto is the
    # clause; the clause is what gets driven [[mutation-tests-the-clause-not-the-feature]].
    saved = _SELFTEST_ACTIVE
    try:
        globals()["_SELFTEST_ACTIVE"] = True
        got = selftest_write_veto(REPORT)
        if not got or SELFTEST_WRITE_MARKER not in got:
            failures.append(f"selftest write-door: a report write aimed at the TRACKED {REPORT} "
                            f"during a selftest was NOT vetoed — got {got!r}. The #158 class is "
                            f"open on its selftest leg.")
        for scratch in (os.path.join(tempfile.gettempdir(), "_CG-SCRATCH.md"), None):
            if selftest_write_veto(scratch):
                failures.append(f"selftest write-door: a SCRATCH write ({scratch!r}) was vetoed "
                                f"too — a selftest that cannot write anywhere cannot prove "
                                f"`--build` still works. The veto is too wide.")
        globals()["_SELFTEST_ACTIVE"] = False
        if selftest_write_veto(REPORT):
            failures.append("selftest write-door: the veto fired OUTSIDE a selftest — `--build` "
                            "is the ruled write path and this would kill it.")
    finally:
        globals()["_SELFTEST_ACTIVE"] = saved
    return failures


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
