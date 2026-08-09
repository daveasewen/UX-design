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
import ast                              # #82: the real-tier check must read STRUCTURE, not text
import datetime
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
    "_measure_tokenizer.py": ("calibration",
        "#53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, "
        "flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the "
        "reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS "
        "READER, and a measurement nothing re-reads decays into a rediscovery."),
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

RETIRED_PROSE_WORDS_RE = re.compile(r"\b(tape|bill)\b", re.I)

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
BANNER_BUDGET_FALLBACK_TK = (4000, 5000)   # used ONLY when the archive cannot be measured, and
                                           # NEVER silently — the provenance string says so.
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
CHAIN_BUDGET_TK = (4917, 6417)     # (warn, BLOCK-CANDIDATE) — ADVISORY, agent-derived, awaiting
#                                    Dave. = the ruled (4500, 6000) on the SLICE + the measured
#                                    417-tape wrapper, restated #48 onto the FILE. 3,410 tk was
#                                    the slice at the #33 cut; warn still leaves ~32% headroom.
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


def measure_tokens(text):
    """Returns (tokens, method). REAL Claude tokens when reachable (#82-D1, Dave's); otherwise
    tiktoken when present (OBSERVED); otherwise the MEASURED byte divisor, labelled ESTIMATE.
    All three are declared and they are never silently mixed — a number whose method is unstated
    is the thing this gate exists to prevent.

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


def _tier_probe():
    """The tier a measurement taken RIGHT NOW would use — WITHOUT recording it.

    ★ The snapshot/restore is the point. A health probe is not a measurement, and a probe that
    wrote into `_TIERS_SEEN` would let `measurement_mixed()` fire on its own footprint — an
    instrument manufacturing the very condition it reports. That is
    [[check-after-its-own-remedy]] in miniature, and it is cheaper to forbid here than to debug
    later from a mixed-tier warning nobody can reproduce."""
    snapshot = set(_TIERS_SEEN)
    try:
        return _tier_of(measure_tokens("x")[1])
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
        if bill_of(banner_tk) >= bb_bill:
            fails.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, block "
                         f"~{bb_bill:,} bill — roll a banner to _GM-ARCHIVE.md (ritual step 2c)")
        elif bill_of(banner_tk) > bw_bill:
            warns.append(f"GOOD-MORNING.md banner region: {fmt_units(banner_tk)}, cap "
                         f"~{bw_bill:,} bill — ritual step 2c")

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


BOOT_DRIFT_WINDOW = 6          # how many of the most recent samples form the band

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
BOOT_DRIFT_DECL_RE = re.compile(
    r"boot-drift\s+DECLARED\s+#(?P<sess>\d+)"
    r".{0,40}?mean\s+(?P<mean>[\d,]+)"
    r".{0,60}?constant\s+(?P<const>[\d,]+)\s*(?:±|\+/-)\s*(?P<err>[\d,]+)"
    r".{0,60}?delta\s+(?P<delta>[+-]?[\d,]+)"
    r".{0,200}?refresh\s+PUT\s+TO\s+DAVE",
    re.I | re.S)

BOOT_DRIFT_LEGAL_FORM = (
    "> **boot-drift DECLARED #<N> (<YYYY-MM-DD>):** mean <M> · constant <C> ±<E> · "
    "delta <+/-D> · refresh PUT TO DAVE, unruled.")


def _parse_boot_drift_declarations(text):
    """Every declared-drift entry in the gauge log, as dicts. Never raises."""
    out = []
    for m in BOOT_DRIFT_DECL_RE.finditer(text):
        try:
            out.append({k: int(m.group(k).replace(",", "").replace("+", ""))
                        for k in ("sess", "mean", "const", "err", "delta")})
        except (ValueError, AttributeError):
            continue
    return out


def _parse_boot_samples(text):
    """Pull (session, real-tokens) boot samples out of the gauge log.

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
    good, refused = [], []
    for ln in text.splitlines():
        if "boot" not in ln.lower():
            continue
        m = re.search(r"\bboot\b\s*(?:#\d+\s*=\s*)?([1-9][\d,]{4,})", ln, re.I)
        if not m:
            # A line mentioning boot with no number is prose, not a refusal.
            if re.search(r"\bboot\b\s*(?:#\d+\s*=\s*)?\d", ln, re.I):
                refused.append(ln.strip()[:110])
            continue
        try:
            tk = int(m.group(1).replace(",", ""))
        except ValueError:
            refused.append(ln.strip()[:110])
            continue
        if not (10_000 <= tk <= 200_000):
            refused.append(ln.strip()[:110])
            continue
        sm = re.search(r"#(\d+)", ln)
        good.append((int(sm.group(1)) if sm else -1, tk))
    return good, refused


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
    ±1,178 on seven post-break samples. Nothing in this function was tuned to suit it; what
    WAS fixed is a blind spot found in the same pass — `_parse_boot_samples` matched
    case-sensitively and could not see "**Boot 53,681 real**", so three sessions of samples
    were invisible here. Both readings are in notes/_GAUGE-LOG.md #129.

    ⚠ It does NOT prescribe a value, widen a band, or edit the constant. It reports the
    measurement and names the drift [[gate-narrows-its-own-rule]]. Re-pricing the
    constant is a measurement someone must take and Dave must see — an agent quietly
    re-fitting the number it is being graded against is the gate marking its own
    homework [[check-after-its-own-remedy]].

    FAILS when the mean of the most recent BOOT_DRIFT_WINDOW samples sits further from
    `BOOT_FIRSTTURN_TK` than `BOOT_FIRSTTURN_ERR` allows. Fails LOUD and NAMED if the
    log cannot be parsed — a crash is not a fail [[a-crash-is-not-a-fail]], and neither
    is a silent zero-sample pass.
    """
    fails, notes = [], []
    log = os.path.join(repo, "notes", "_GAUGE-LOG.md")
    if not os.path.exists(log):
        fails.append("boot-drift: notes/_GAUGE-LOG.md is MISSING — the boot constant "
                     "cannot be checked against anything. This is the #109 condition "
                     "(a constant with no consumer), not a clean pass.")
        return fails, notes
    try:
        sys.path.insert(0, HERE)
        import _gauge_tokens as gt
        const, err = gt.BOOT_FIRSTTURN_TK, gt.BOOT_FIRSTTURN_ERR
    except Exception as e:
        fails.append(f"boot-drift: cannot read BOOT_FIRSTTURN_TK/_ERR from "
                     f"_gauge_tokens.py ({e}) — the published constant is UNREADABLE, "
                     f"so it is also unverifiable. Fix, never close blind.")
        return fails, notes

    with open(log, encoding="utf-8") as f:
        samples, refused = _parse_boot_samples(f.read())
    if refused:
        fails.append("boot-drift: %d gauge-log line(s) look like boot readings but do "
                     "NOT parse — %s. The band would be computed off an incomplete "
                     "sample and read GREEN. Fix the parser or the line."
                     % (len(refused), " · ".join(refused[:2])))
        return fails, notes
    if len(samples) < 3:
        fails.append("boot-drift: only %d boot sample(s) found in notes/_GAUGE-LOG.md — "
                     "too few to test the constant against. DECLARED, not passed."
                     % len(samples))
        return fails, notes

    # newest wins per session, then chronological
    by_session = {}
    for sess, tk in samples:
        by_session[sess] = tk
    ordered = [tk for _, tk in sorted(by_session.items())]
    recent = ordered[-BOOT_DRIFT_WINDOW:]
    mean = sum(recent) / len(recent)
    delta = mean - const

    notes.append("boot-drift: constant %s ±%s vs recent mean %s (n=%d, last %d sessions "
                 "of %d parsed) — delta %+d"
                 % (f"{const:,}", f"{err:,}", f"{mean:,.0f}", len(recent),
                    len(recent), len(ordered), delta))

    if abs(delta) > err:
        drift_msg = (
            "boot-drift: `_gauge_tokens.BOOT_FIRSTTURN_TK` = %s ±%s, but the last %d "
            "measured boots average %s — drift %+d, OUTSIDE the constant's own error "
            "bar. Samples: %s."
            % (f"{const:,}", f"{err:,}", len(recent), f"{mean:,.0f}", delta,
               " · ".join(f"{s:,}" for s in recent)))

        # ★ #111-D1 — is the drift DECLARED? Silence fails; an honest declaration passes.
        with open(log, encoding="utf-8") as f:
            decls = _parse_boot_drift_declarations(f.read())
        matched = [d for d in decls
                   if d["const"] == const and d["err"] == err
                   and abs(d["mean"] - mean) <= 1 and abs(d["delta"] - delta) <= 1]
        mismatched = [d for d in decls if d not in matched]

        if matched:
            d = matched[-1]
            notes.append(
                "%s ✅ DECLARED at #%d and DISCHARGED (#111-D1): the declaration states "
                "the same mean, constant, error bar and delta this gate computed, and "
                "records that the refresh is PUT TO DAVE and unruled. The drift is real "
                "and is NOT hidden — that is the whole bar. ⚠ It is still UNFIXED: only "
                "Dave's ruling on the constant closes it."
                % (drift_msg, d["sess"]))
        elif mismatched:
            d = mismatched[-1]
            fails.append(
                "%s ⛔ A boot-drift declaration EXISTS (#%d) but its numbers do NOT match "
                "this gate's computation — it states mean %s / constant %s ±%s / delta "
                "%+d against a measured mean %s / constant %s ±%s / delta %+d. A "
                "declaration that mis-states the drift is worse than none: it is a "
                "session writing itself a pass. Correct the figures — do NOT widen the "
                "error bar and do NOT edit the constant to fit "
                "[[gate-must-quote-what-it-forbids]]."
                % (drift_msg, d["sess"], f"{d['mean']:,}", f"{d['const']:,}",
                   f"{d['err']:,}", d["delta"], f"{mean:,.0f}", f"{const:,}",
                   f"{err:,}", delta))
        else:
            fails.append(
                "%s ⛔ AND IT IS UNDECLARED. ⚠ This is the #109 defect recurring: the "
                "constant is stale and only a measurement can correct it. Re-measure, "
                "put the new figure to Dave, and update the constant — do NOT widen the "
                "error bar to make this pass.\n"
                "    ★ #111-D1 (Dave) — THERE IS A LEGAL WAY FORWARD AND THIS GATE OWES "
                "IT TO YOU. You are not required to fix the drift to close your wrap; "
                "you are required not to hide it. Add ONE line to notes/_GAUGE-LOG.md, "
                "exactly this shape:\n"
                "      %s\n"
                "    filled with the figures above: mean %s · constant %s ±%s · delta "
                "%+d. The declaration must MATCH what this gate computes — wrong figures "
                "fail louder than none. Then this check passes and the constant refresh "
                "goes to Dave as its OWN decision, not as the price of unblocking a wrap."
                % (drift_msg, BOOT_DRIFT_LEGAL_FORM, f"{mean:,.0f}", f"{const:,}",
                   f"{err:,}", delta))
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


def _sig_hit(path):
    return os.path.basename(path).startswith(INSTRUMENT_SIGNATURES)


def instrument_stray_check(repo, dirs=INSTRUMENT_READONLY_DIRS):
    """Return (fails, warns). Untracked paths under read-only asset dirs are FAILS.

    Pass 1: untracked and NOT ignored — anything at all is a stray.
    Pass 2: untracked INCLUDING ignored, filtered to INSTRUMENT_SIGNATURES — so a
    `.gitignore` entry cannot silence a known instrument.

    Never raises: if git cannot be run the gate says so LOUD and NAMED rather than
    returning a green it did not measure [[feedback-measuring-tool-must-not-guess]].
    """
    fails, warns = [], []
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
        strays = sorted(set(found))
        if strays:
            shown = ", ".join(f"`{s}`" for s in strays[:6])
            more = f" (+{len(strays) - 6} more)" if len(strays) > 6 else ""
            fails.append(
                f"INSTRUMENT STRAY: {len(strays)} untracked path(s) under `{d}` — {shown}{more}. "
                f"An instrument has written into a directory it only reads (#138 class; `.uuid*` "
                f"means fontconfig — its `<dir>` is pointed at the repo instead of the /var/tmp "
                f"symlink farm, see `_RUNBOOK-render-verify.md` § SYMLINK FARM). Move them out "
                f"with a SAME-MOUNT `mv` to `_to_delete/` — a `mv` to /var/tmp fails, different "
                f"filesystem. ⛔ Do NOT gitignore them: this gate ignores .gitignore on purpose.")
    return fails, warns


def wrap_checks(repo, today, lane=False):
    fails, warns, notes = [], [], []
    iso = today.isoformat()
    _sf, _sw = instrument_stray_check(repo)     # #138 — runs for LANE wraps too, on purpose:
    fails += _sf                                # a lane session renders like any other.
    warns += _sw
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


def run(mode="build", repo=REPO, report=REPORT, today=None, lane=False, rehearse=False):
    today = today or datetime.date.today()
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
        log_err = _rehearsal_log_append(repo, {
            "date": today.isoformat(), "kind": "rehearse" if rehearse else "wrap-open",
            "fails": len(fails), "structural": len(structural),
            "heals_at_wrap": len(heals), "warns": len(warns),
            "structural_names": [s[:120] for s in structural],
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
        with open(report, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    if rehearse:
        # TERSE BY DESIGN — the window pays for every printed line; the whole point of the
        # rehearsal is that the sandbox does the reading. Structural fails in full (they are
        # the deliverable), everything else as counts.
        for i in structural:
            print(f"  ⛔ STRUCTURAL {i}")
        for i in heals:
            print(f"  ▫️  heals-at-wrap: {i[:100]}")
        print(f"rehearsal [wrap-gate, early]: {len(structural)} STRUCTURAL fail(s) — fix NOW, "
              f"cheap · {len(heals)} heals-at-wrap (ritual steps 1/2) · {len(warns)} warn(s) "
              f"(run --wrap for bodies) · logged → {REHEARSAL_LOG}")
        return 1 if structural else 0
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
        g_fail = _governs.selftest()
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
    saved = {k: os.environ.get(k) for k in _envs}
    for k in _envs:
        os.environ[k] = "1"
    sys.modules["tiktoken"] = None
    try:
        if not measurement_degraded():
            failures.append("#59: measurement_degraded() read False with tiktoken absent — it "
                            "has drifted from measure_tokens()'s own fallback decision")
    finally:
        del sys.modules["tiktoken"]
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
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
        _tier_probe()
        if _TIERS_SEEN:
            failures.append(f"#82-D1: _tier_probe() RECORDED {sorted(_TIERS_SEEN)} into "
                            f"_TIERS_SEEN — a health probe that writes its own footprint lets "
                            f"measurement_mixed() refuse a build on a condition the probe "
                            f"itself created")
    finally:
        _TIERS_SEEN.clear()
        _TIERS_SEEN.update(_snap0)
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
    real_tiktoken = importlib.import_module("tiktoken")
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
        # FAT measures 240 tk/line, so 17 lines ≈ 4.1K (warn band) and 30 ≈ 7.3K (block). The
        # numbers are MEASURED, not assumed: the first draft guessed ~200 tk/line, put the warn
        # fixture at 5.4K, and bit as a block instead.
        _f, w, _n = _warns_for(td, fat_banner=17)
        if not any("banner region" in x for x in w):
            failures.append("M8: a 17-fat-line banner did not WARN — the sub-budget does not bite")
        f, _w, _n = _warns_for(td, fat_banner=30)
        if not any("banner region" in x for x in f):
            failures.append("M8: a 30-fat-line banner did not BLOCK")
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
            ("CHAIN_BUDGET_TK", CHAIN_BUDGET_TK, (4917, 6417),
             "RE-POINTED TWICE, both times the REFERENT and never the ruling. #33 2026-07-28: was "
             "(24000, 28000) against the GM+LS-whole referent, ruled 2026-07-27 M-set → (4500, "
             "6000) against the SLICE. #48 2026-07-30 (open 16 (a), Dave #47): → (4917, 6417) "
             "against the whole _CHAIN.md FILE = the same (4500, 6000) plus the MEASURED 417-tape "
             "wrapper, so the verdict is arithmetically unchanged (ds-021: restate, never silently "
             "tighten). Values still AGENT-DERIVED, still ADVISORY, still awaiting Dave"),
            ("BANNER_BUDGET_FALLBACK_TK", BANNER_BUDGET_FALLBACK_TK, (4000, 5000),
             "⛔ NO LONGER THE CAP — it is the DECLARED FALLBACK only. Born as the cap, ruled "
             "2026-07-27 M-set; RE-EXPRESSED AS A FUNCTION 2026-07-30 #53 on Dave's D4 (a), "
             "because the measurement showed (4000, 5000) sat at the floor plus TWO TAPE "
             "(header 1,968 + 2 × median 1,515 = 4,998) and could not be complied with. The "
             "old pair is retained VERBATIM as the fallback so a repo with no archive behaves "
             "exactly as it always did — ds-021: restate openly, never silently re-dial. The "
             "live cap is `banner_budget_tk()` and publishes its own provenance every run"),
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
    _real_saved = os.environ.get("CAPTURE_GATE_NO_REAL")
    os.environ["CAPTURE_GATE_NO_REAL"] = "1"
    try:
        return _selftest_body()
    finally:
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


def _selftest_body():
    failures = (selftest_real_tier_reachable()
                + selftest_preflight() + selftest_preflight_tokens()
                + selftest_gauge_refusal_seam()          # #79-D1 paired half
                + selftest_budgets() + selftest_strata_exempt() + selftest_units()
                + selftest_cross_instrument_units()       # ds-021 (C), RULED #81-D1
                + selftest_retired_unit_prose()           # ds-021 (C), the `.md` arm
                + selftest_bare_token()
                + selftest_gauge_continuity() + selftest_unkeyed()
                + selftest_growth() + selftest_usage()
                + selftest_lanes() + selftest_receipts() + selftest_index_freshness()
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
        for x in failures:
            print(f"  ❌ selftest: {x}")
        return 1
    print("  ✅ capture-gate selftest: all failure classes bite; green control passes")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--rehearse" in sys.argv:
        # #92: the wrap gate run EARLY, mid-window, where a fix is cheap. Same seam as --wrap;
        # only classification, terseness and the log differ. Consumer: _checkin.py.
        sys.exit(run(rehearse=True, lane="--lane" in sys.argv))
    sys.exit(run(mode="wrap" if "--wrap" in sys.argv else "build",
                 lane="--lane" in sys.argv))
