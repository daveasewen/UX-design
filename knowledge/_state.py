#!/usr/bin/env python3
"""`_state.json` — the task store. THE substrate change (#88, on Dave's #85-D1).

WHAT THIS REPLACES, precisely
-----------------------------
`_capture_gate.dofirst_index()` (`:1416`) runs `DOFIRST_ITEM_RE` over `GOOD-MORNING.md`'s prose
and renders a presence index. That is a RENDERER, not a store: an item's identity is its position
in a document, and it has no state, no owner, no age, and — the decisive omission — no stated
condition under which it would be finished. An item with no close condition cannot be closed; it
can only be DELETED, and deletion is correctly forbidden by [[home-by-addition-then-cut]] until a
probe proves the fact lives elsewhere. Items are therefore structurally immortal.

This module gives items identity and a close condition, and gates the condition on the way in.

⛔ WHAT THE #88 PROBE KILLED, AND WHY THIS FILE IS SMALLER THAN THE PROPOSAL ASKED FOR
--------------------------------------------------------------------------------------
`_MEMENTO-REBUILD-PROPOSAL-2026-08-02-v1.md` is #85's, and #88 probed it before building on it.
Three of its premises did not survive, and the survivors are what this file implements:

1. **"`closes_when` is the missing field" — FALSE as of #87.** `knowledge/_GOVERNING-RECORDS.md`
   already carries 17 rows, each with a ratified `closes_when`, ruled at #86-D1/D2 (Dave: "Yes,
   firm — record them"). So this store ABSORBS that register rather than inventing its concept.
   The register stays the human-readable face; this file is the machine-readable one, and
   `_migrate_state.py` GENERATES one from the other so they cannot disagree.

2. **"The list only grows" — UNPROVEN, and the reproducible series says otherwise.** The
   proposal's "95 item-slots over 12 sessions, 84 distinct" is not reproducible by any probe
   (same defect class as #86's "118 markers" → ~40). Replaying `DOFIRST_ITEM_RE` over the newest
   GM commit of each of the last 12 sessions gives 19 distinct item numbers, and the per-session
   series is 18,18,18,19,19,19,19,19,19,19,19,19 — FLAT, not accreting.
   ⇒ The case for this store is NOT "the list grows". It is that a flat list of 19 items which
   can never close is worse than a list that moves: immortality, not growth, is the defect.
   Stating this here because a rebuild justified by a dead number is how the next session
   inherits a false premise [[premise-ages-faster-than-rule]].

3. **"Extend `_decision-graph.json` with a `process` node type — same shape it already has" —
   FALSE.** Nodes have NO `type` field at all (100/100 absent), no node-level `state`, and the
   file runs TWO disagreeing lifecycle vocabularies: node `status` (accepted 85 · superseded 8 ·
   amended 6 · proposed 1) and a separate top-level `state` map (LIVE 84 · DEAD 8 · AMENDED 7 ·
   OPEN 1) — 85 vs 84 for the same population. Edge types have drifted to NINE, not the six the
   standing open item names.
   ⇒ #88 does NOT fold the graph. Reconciling two lifecycle vocabularies is a RULING, Dave's, and
   an agent quietly picking one is exactly the class of move the governing register exists to
   catch. This store LINKS to graph node ids (`links`) and leaves the graph alone. The
   reconciliation enters the register as its own row with its own `closes_when`.

THE GATE, AND WHY IT IS SHAPED THIS WAY
---------------------------------------
`check()` enforces: **you cannot open an item without stating what would end it.**

The 19 inherited DOFIRST items have no close condition and cannot be given one by an agent —
inventing a close condition for Dave's open work is the same overreach as inventing his ruling.
So they enter as `closes_when: null` with `condition: "UNCONDITIONED"`, and the gate treats them
as a DECLARED debt: a declared gap passes, a silent one fails [[instrument-without-a-consumer]].

⛔ The debt is FROZEN, not tolerated. `LEGACY_IDS` pins the exact inherited set at birth. Any id
outside that frozen set MUST carry a `closes_when` — so the unconditioned population can only
ever shrink. This is [[gate-inside-the-growth-loop]]: gate the PRESENCE of the defect, not its
drift, or the exemption becomes the new default and the store inherits the disease it replaces.

⚠ `check()` is BLOCKING by design and says so. A gate that only warns cannot make items mortal,
and a gate that does not run cannot fail [[instrument-without-a-consumer]] — its call site in
the capture ritual is the thing that makes this file real, not the code here.
"""

from __future__ import annotations
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "_state.json")

SCHEMA = 1

# ---- the vocabulary. ONE lifecycle, unlike the graph's two. ------------------------------------
# ⚠ Deliberately NOT reusing the decision-graph's `status` words (`accepted`/`superseded`/...).
# Those describe a DESIGN DECISION's life; these describe a PIECE OF WORK's life. Borrowing the
# vocabulary would fuse two domains that close for different reasons — and the graph is already
# the cautionary tale, running two vocabularies that disagree by one.
STATES = ("open", "blocked", "ruled", "done", "dropped", "parked")
# `parked` added #195 — MECHANICAL enactment of s194-D2, whose text moves W-34 open → parked
# with a named external trigger; the wrap wrote the state before this vocabulary learned the
# word, so step 25 refused an honest statement ([[honest-refusal-needs-a-legal-form]]).
LIVE_STATES = ("open", "blocked", "ruled")      # still costs a session something — parked does NOT
OWNERS = ("dave", "claude")

CONDITIONED = "stated"
UNCONDITIONED = "UNCONDITIONED"

# ⚠ `project` is IN this tuple, not beside it (s172-D1). One list of required fields, or the
# gate and the docs fork the moment somebody edits one of them [[ban-scoped-to-a-name]]. The
# missing-field refusal below appends the enum and the reason when `project` is what is absent,
# so the refusal still quotes what it forbids [[gate-must-quote-what-it-forbids]].
REQUIRED = ("id", "title", "state", "opened", "owner", "condition", "closes_when", "links",
            "home", "project")

# ⛔ THE FROZEN LEGACY SET — the inherited DOFIRST items, pinned at birth (#88).
# These 19 may carry `closes_when: null`. NOTHING ELSE MAY, EVER. Do not add to this tuple:
# growing it is the one edit that would turn a bounded debt back into an unbounded exemption,
# which is the exact failure mode this store exists to end.
LEGACY_IDS = (
    "W-0b", "W-0c", "W-0d", "W-01", "W-02", "W-03", "W-04", "W-05", "W-06", "W-07",
    "W-08", "W-09", "W-10", "W-11", "W-12", "W-13", "W-14", "W-15", "W-16",
)

# s215-D1 (Dave, 2026-08-22): W- widened to 3 digits + up to two-letter suffix. The eight
# #214 stopgaps (W-99za..W-99zh) are GRANDFATHERED VERBATIM — ids are addresses; renaming
# rots every citation (ADR-0017). Next fresh mint is W-100. G scheme untouched.
ID_RE = re.compile(r"^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$")

# ---- `priority_override` — OPTIONAL, DAVE'S ALONE (narrow schema addition, #165) -------------
# The dashboard computes a PROPOSED priority score from the store. Dave overrules it by writing
# an integer rank on the item: 1 = do this first. The field is OPTIONAL and starts ABSENT on
# every item — no agent may author a value, because authoring one would be an agent ruling its
# own priority and then reading its own ruling back as if it were Dave's [[gate-dont-patch]].
#
# ⚠ THIS GATE IS A PRESENCE GATE, NOT A REQUIREMENT: it says nothing about whether the field
# SHOULD be there. It says: **if it is there, it is an integer in range, and it is Dave's.**
# An out-of-range or string rank is worse than an absent one, because it sorts silently.
PRIORITY_OVERRIDE = "priority_override"
PRIORITY_OVERRIDE_MIN = 1
PRIORITY_OVERRIDE_MAX = 999

# ---- `deadline` / `effort` — DE-GAMING THE PROXIES (same presence-gate pattern) -------------
# The dashboard's `deadline` and `effort` criteria are PROXIES: a prose regex over the item's
# own words, and the byte-length of its body. Both are gameable in the literal sense — an item
# scores higher by SAYING "friday" or by having a SHORTER body. A proxy that moves with the
# prose is a measure of the prose, not of the work [[measure-dont-convert-units]].
#
# The fix is a real input, gated on the way in and OPTIONAL exactly like priority_override:
#   deadline: an ISO date "YYYY-MM-DD"        effort: one of S / M / L
# ⛔ NO AGENT MAY AUTHOR A VALUE. Both start ABSENT on every item. Authoring a deadline is
# inventing Dave's schedule; authoring an effort is grading one's own homework and then reading
# the grade back as an input to one's own priority proposal.
#
# ⚠ PRESENCE GATE, NOT A REQUIREMENT: absent is legal and keeps the proxy (still labelled
# PROXY ONLY in the dashboard). Present REPLACES the proxy — so a malformed value is worse than
# an absent one, because it would silently displace the only measurement there is.
DEADLINE = "deadline"
DEADLINE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
EFFORT = "effort"
EFFORT_VALUES = ("S", "M", "L")

# ---- `effort` IS A TOKEN-BANDED RUNG, NOT A T-SHIRT (#168, Option C) ------------------------
# s168-D2 PENDING — minted by Dave at the #168 wrap, not here. Until then this block is a
# PROPOSAL's vocabulary written down, and the gate below enforces only what it already did.
#
# ⚠ THE SPELLING IS UNCHANGED — S / M / L — and that is deliberate: Option C §5.2 asks for
# ZERO schema change, so every value already legal stays legal and the both-direction selftest
# carries over intact. What changes is the STANDARD the letter is picked against.
#
# THE UNIT, NAMED: **real Claude tokens of JOB WINDOW** — `client.messages.count_tokens()`
# tokens (the unit ruled in `_gauge_tokens.py`), counting the JOB ONLY: boot and wrap are
# EXCLUDED, exactly as the `boot + job + wrap` pre-flight blocks in `notes/_GAUGE-LOG.md`
# decompose them. It is NOT wall-clock, NOT lines of code, NOT bytes of prose — bytes of prose
# is the proxy this field exists to kill [[measure-dont-convert-units]].
#
# ⛔ AND DELEGATED SUB SPEND IS EXCLUDED TOO (#168). A sub's tokens are WEEKLY QUOTA, not this
# window's FILL [[budget-vs-quota-vocabulary]] — and they never entered the corpus: the
# `job` numbers in `notes/_GAUGE-LOG.md` are conductor-window figures, so edges derived from
# them cannot price sub spend. An L that means "needs a sub" is therefore a claim about THIS
# window, not a total bill; the two budgets must not be added [[delegation-cost-inversion-110]].
#
#   S — fits BESIDE other work in one window
#   M — IS the window's job
#   L — does NOT fit one window; needs a lane, a sub, or a session of its own
#
# ⛔ THE BAND EDGES ARE NOT TYPED HERE, ON PURPOSE. They are DERIVED AT BUILD from the
# token-priced session blocks in `notes/_GAUGE-LOG.md` by `gen_dashboard.effort_anchors()`,
# which prints them on the page together with the `n` it derived them from. A number typed in
# two files drifts in one of them; an edge with no `n` beside it is a round number somebody
# liked, not a measurement [[planning-estimate-is-not-a-measurement]].
#
# ⚠ AND IT IS STILL AN ESTIMATE. The edges are measured; a rung Dave picks for an item is his
# FORECAST against them. The page must say *estimated*, never *costs*.
#
# ⛔ NO AGENT MAY AUTHOR A VALUE — unchanged and re-stated because a stated standard makes
# authoring feel more defensible, and it is not. The gate cannot tell Dave's "M" from mine.
EFFORT_UNIT = ("real Claude tokens of job window (boot and wrap EXCLUDED, and delegated sub "
               "spend EXCLUDED — a sub's tokens are weekly QUOTA, not this window's fill, and "
               "are not in the blocks these edges derive from), derived from the token-priced "
               "session blocks in notes/_GAUGE-LOG.md")
EFFORT_RUNG_MEANING = {
    "S": "fits beside other work in one window",
    "M": "is the window's job",
    "L": "does not fit one window — needs a lane or a sub",
}


# ---- `project` — WHICH BODY OF WORK THIS ITEM BELONGS TO (s172-D1, Dave, #172) ---------------
# ⛔ NOT a presence-OPTIONAL field like priority_override / deadline / effort. Those three are
# Dave's to author and start ABSENT. This one is REQUIRED on every item, because the question it
# answers — *which project is this?* — has an answer for every item that exists, and an item with
# no answer is not "unassigned", it is an item nobody looked at.
#
# THE TWO NAMES ARE A CLOSED ENUM, deliberately. A free-text project name forks on the first
# typo ("Memento" / "memento" / "memento-lane") and every filter downstream then silently drops
# rows it cannot match — the same silent-sort defect the priority_override gate exists to stop.
# Widening the enum is a RULING, Dave's; it is not a value an agent picks while adding an item.
#
# ⚠ WHAT THIS FIELD DOES *NOT* CARRY. It is a grouping label, not a lifecycle, not an owner, and
# not a priority. The 37 values written at #172 are DEFAULTS proposed for Dave's eye against the
# assignment list in the s172-D1 batch; two of them (W-14, G12) were declared AMBIGUOUS at
# proposal time and the dashboard flags them in WORDS. This module does not know which two, and
# must not: an ambiguity flag stored here would read back as a fact about the item rather than
# as an open question about my own guess [[feedback-measuring-tool-must-not-guess]].
PROJECT = "project"
PROJECT_VALUES = ("apollo", "memento")


class StateError(Exception):
    """Raised loud and NAMED. A crash is not a fail [[a-crash-is-not-a-fail]] — callers that
    cannot distinguish a malformed store from a store with no items will report the wrong thing,
    so the two paths are different exception surfaces, not one silent empty list."""


# ---- load / save -------------------------------------------------------------------------------

def load(path=STORE):
    if not os.path.exists(path):
        raise StateError(f"{os.path.basename(path)} is MISSING — the store is not assumed empty")
    with open(path, encoding="utf-8") as f:
        try:
            doc = json.load(f)
        except json.JSONDecodeError as e:
            raise StateError(f"{os.path.basename(path)} is not valid JSON ({e}) — REFUSING to "
                             f"treat a parse failure as an empty worklist")
    if doc.get("meta", {}).get("schema") != SCHEMA:
        raise StateError(f"schema mismatch: store says {doc.get('meta', {}).get('schema')!r}, "
                         f"this module implements {SCHEMA}")
    return doc


def save(doc, path=STORE):
    doc["items"] = sorted(doc["items"], key=_sort_key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _sort_key(it):
    m = re.match(r"^([A-Z])-?([0-9]+)([a-z]?)$", it["id"])
    if not m:
        return (9, 0, "", it["id"])
    fam = {"W": 0, "G": 1}.get(m.group(1), 9)
    return (fam, int(m.group(2)), m.group(3), it["id"])


# ---- home pointers: the ROT CLASS (#168) -------------------------------------------------------
# Every `home` written at birth (#88) was `<path>:<line>`. GOOD-MORNING.md is a ROLLING surface:
# each session prepends a banner, so every line number below the banner moves. Measured #168: all
# 19 W-* homes were off by exactly 16 lines — every one of them resolved to a DIFFERENT item's
# prose, and nothing complained, because nothing ever RESOLVED a home [[instrument-without-a-
# consumer]]. The standing store was citing a rolling surface.
#
# The repair is an ADDRESS CHANGE, not a re-count: `<path>#<literal anchor>` — a substring that
# must occur EXACTLY ONCE in the file. An anchor moves WITH the text it names; a line number does
# not. Re-counting the lines would have fixed the 19 instances and left the class intact.
#
# ⚠ `<path>:<line>` is still ACCEPTED — `_GOVERNING-RECORDS.md` is a standing table whose rows do
# not roll, and its 18 homes all resolved correctly at #168. The form is reported, never rewritten
# on Dave's behalf.
HOME_ANCHOR = "#"

# ⬛ DAVE'S DIAL, DELIBERATELY OFF. `False` ⇒ an unresolvable home is a NOTE. `True` ⇒ it is a
# BLOCKING failure, and `_state.py` is an ABORT step in `_build_all.py` (#166), so flipping this
# stops the build at the bad pointer. Both directions are mutation-tested in selftest(), so the
# promotion is PROVEN available, not assumed. Flipping it is a one-word, one-line reversal.
HOME_ROT_BLOCKING = True  # flipped by Dave, #168 — a rotten home pointer is a build stop


def resolve_home(home, root=None):
    """Resolve one `home` against the filesystem. Returns `(status, detail)`.

    status ∈ {"empty", "missing-file", "anchor-ok", "anchor-absent", "anchor-ambiguous",
              "line-ok", "line-past-eof"}
    A FAIL is named and quotes what it forbids [[gate-must-quote-what-it-forbids]]. A file this
    module cannot see is `missing-file` — NOT silently passed, and NOT guessed at.
    """
    if root is None:
        root = os.path.dirname(HERE)
    home = (home or "").strip()
    if not home:
        return ("empty", "no home recorded")
    if home.endswith("/"):
        # #215 DIRECTORY ADDRESS (paired with _gate_doc_rows.py's directory-home clause —
        # one grammar, two consumers): the home is a directory whose files the row owns.
        # Resolves iff the directory exists and is non-empty; an empty dir is a rotted home.
        dp = os.path.join(root, home.rstrip("/"))
        if not os.path.isdir(dp):
            return ("missing-file", f"directory {home!r} does not exist under {root}")
        n = len([e for e in os.listdir(dp) if not e.startswith(".")])
        if n == 0:
            return ("anchor-absent", f"directory {home!r} exists but is EMPTY — a rotted home")
        return ("anchor-ok", f"{home} exists, {n} file(s)")
    if HOME_ANCHOR in home:
        rel, anchor = home.split(HOME_ANCHOR, 1)
        kind = "anchor"
    elif ":" in home and home.rsplit(":", 1)[1].isdigit():
        rel, anchor = home.rsplit(":", 1)
        kind = "line"
    else:
        rel, anchor, kind = home, None, "file"
    fp = os.path.join(root, rel)
    if not os.path.isfile(fp):
        return ("missing-file", f"{rel!r} does not exist under {root}")
    with open(fp, encoding="utf-8") as f:
        text = f.read()
    if kind == "file":
        return ("anchor-ok", f"{rel} exists (no anchor to resolve)")
    if kind == "anchor":
        n = text.count(anchor)
        if n == 1:
            ln = text[:text.index(anchor)].count("\n") + 1
            return ("anchor-ok", f"{rel}: anchor {anchor!r} unique, currently line {ln}")
        if n == 0:
            return ("anchor-absent", f"{rel}: anchor {anchor!r} NOT FOUND")
        return ("anchor-ambiguous", f"{rel}: anchor {anchor!r} occurs {n}× — not an address")
    ln = int(anchor)
    lines = text.splitlines()
    if ln > len(lines):
        return ("line-past-eof", f"{rel}: line {ln} is past EOF ({len(lines)} lines)")
    return ("line-ok", f"{rel}:{ln} reads {lines[ln - 1][:60]!r} — UNVERIFIED: a line number "
                       f"cannot say whether that is the RIGHT line")


def check_homes(items, root=None):
    """`(fails, note)` over every item's `home`. The note is a MEASUREMENT of the two forms —
    it moves with the data, so it cannot be read as decoration."""
    fails, by_status = [], {}
    for it in items:
        st, detail = resolve_home(it.get("home"), root)
        by_status[st] = by_status.get(st, 0) + 1
        if st in ("empty", "missing-file", "anchor-absent", "anchor-ambiguous", "line-past-eof"):
            fails.append(f"{it.get('id', '<no id>')} home UNRESOLVABLE — {detail}")
    if not items:
        return fails, ""
    n_anchor = by_status.get("anchor-ok", 0)
    n_line = by_status.get("line-ok", 0)
    note = (f"home pointers: {n_anchor} resolve by ANCHOR (rot-proof), {n_line} are still "
            f"`path:line` (UNVERIFIABLE by content — the #168 rot class), {len(fails)} "
            f"UNRESOLVABLE. Blocking = {HOME_ROT_BLOCKING} (Dave's dial).")
    return fails, note


# ---- the gate ----------------------------------------------------------------------------------

def check(doc=None, path=STORE):
    """Return `(ok: bool, failures: list[str], notes: list[str])`.

    BLOCKING. Every failure names the item and quotes the offending value — a gate that reports
    "3 items invalid" cannot be acted on, and one that reports a count instead of the thing it
    forbids is [[gate-must-quote-what-it-forbids]].
    """
    if doc is None:
        doc = load(path)
    fails, notes = [], []
    items = doc.get("items")
    if not isinstance(items, list):
        raise StateError("store has no `items` list")

    seen = {}
    for it in items:
        iid = it.get("id", "<no id>")

        missing = [k for k in REQUIRED if k not in it]
        if missing:
            # A bare "missing required field(s) project" tells the reader the NAME and nothing
            # about what a legal value is, so the next hand-edit invents one. The refusal
            # carries the enum [[gate-must-quote-what-it-forbids]].
            why = ""
            if PROJECT in missing:
                why = (f" — {PROJECT!r} is REQUIRED on every item (s172-D1) and must be exactly "
                       f"one of {PROJECT_VALUES}. Every item belongs to a body of work; an item "
                       f"with no project is not 'unassigned', it is an item nobody classified, "
                       f"and it would vanish from every filtered view on the dashboard without "
                       f"ever being counted as missing")
            fails.append(f"{iid}: missing required field(s) {', '.join(missing)}{why}")
            continue

        if not ID_RE.match(iid):
            fails.append(f"{iid}: id does not match {ID_RE.pattern!r}")
        if iid in seen:
            fails.append(f"{iid}: duplicate id — ids are stable and NEVER reused")
        seen[iid] = it

        if it["state"] not in STATES:
            fails.append(f"{iid}: state {it['state']!r} not in {STATES}")
        if it["owner"] not in OWNERS:
            fails.append(f"{iid}: owner {it['owner']!r} not in {OWNERS}")
        if not isinstance(it["opened"], int):
            fails.append(f"{iid}: opened {it['opened']!r} is not a session number")
        if not str(it.get("title", "")).strip():
            fails.append(f"{iid}: title is empty")

        # ---- `project` — REQUIRED, CLOSED ENUM (s172-D1). Present-but-wrong is the case this
        # arm exists for: absent is caught above, and a value outside the enum is WORSE than an
        # absent one because it reads as a classification while matching no filter.
        pv = it[PROJECT]
        if pv not in PROJECT_VALUES:
            fails.append(
                f"{iid}: {PROJECT} is {pv!r} — must be exactly one of {PROJECT_VALUES}. This is "
                f"a CLOSED enum, not a free-text label: a near-miss spelling classifies the item "
                f"in the store and then matches no filter on any surface that reads it, so the "
                f"item disappears from every project view while the store still claims it has a "
                f"project. Widening this enum is Dave's ruling, not a value picked at add time")

        # ---- THE CLOSE CONDITION. This is the whole point of the file. ----
        cond, cw = it["condition"], it["closes_when"]
        if cond == CONDITIONED:
            if not isinstance(cw, str) or not cw.strip():
                fails.append(f"{iid}: condition={CONDITIONED!r} but closes_when is {cw!r} — "
                             f"claiming a condition without stating one is worse than admitting "
                             f"there is none, because it passes")
            elif len(cw.strip()) < 12:
                fails.append(f"{iid}: closes_when {cw!r} is too short to be checkable — a "
                             f"condition that cannot be checked cannot fire")
        elif cond == UNCONDITIONED:
            if cw is not None:
                fails.append(f"{iid}: condition={UNCONDITIONED!r} but closes_when is {cw!r} — "
                             f"say which it is")
            if iid not in LEGACY_IDS:
                fails.append(
                    f"{iid}: UNCONDITIONED and NOT in the frozen legacy set. You cannot open an "
                    f"item without stating what would end it. The 19 inherited items are "
                    f"exempt because an agent may not invent Dave's close conditions; a NEW "
                    f"item has no such excuse.")
        else:
            fails.append(f"{iid}: condition {cond!r} must be {CONDITIONED!r} or {UNCONDITIONED!r}")

        # ---- OPTIONAL priority_override — validated ONLY when PRESENT (#165) ----
        if PRIORITY_OVERRIDE in it:
            v = it[PRIORITY_OVERRIDE]
            if isinstance(v, bool) or not isinstance(v, int):
                fails.append(f"{iid}: {PRIORITY_OVERRIDE} is {v!r} — an override must be an "
                             f"integer rank (1 = first). A rank that is not a number sorts "
                             f"silently and wrongly, which is worse than no override at all")
            elif not (PRIORITY_OVERRIDE_MIN <= v <= PRIORITY_OVERRIDE_MAX):
                fails.append(f"{iid}: {PRIORITY_OVERRIDE} {v!r} is outside "
                             f"{PRIORITY_OVERRIDE_MIN}..{PRIORITY_OVERRIDE_MAX} — a rank of "
                             f"{v!r} is not a rank, it is a typo that outranks everything")

        # ---- OPTIONAL deadline / effort — validated ONLY when PRESENT (#166 de-gaming) ----
        if DEADLINE in it:
            v = it[DEADLINE]
            if not isinstance(v, str) or not DEADLINE_RE.match(v):
                fails.append(f"{iid}: {DEADLINE} is {v!r} — a deadline must be an ISO date "
                             f"'YYYY-MM-DD'. A date the scorer cannot parse does not fail "
                             f"loudly, it quietly falls back to the prose proxy it replaced")
            else:
                y, m, d = (int(x) for x in v.split("-"))
                try:
                    import datetime as _dt
                    _dt.date(y, m, d)
                except ValueError:
                    fails.append(f"{iid}: {DEADLINE} {v!r} is well-shaped but not a real "
                                 f"calendar date — shape is not validity")
        if EFFORT in it:
            v = it[EFFORT]
            if v not in EFFORT_VALUES:
                fails.append(f"{iid}: {EFFORT} is {v!r} — effort must be one of "
                             f"{EFFORT_VALUES}. A free-text size is not a size; it is prose, "
                             f"and prose is the proxy this field exists to replace. "
                             f"The rungs are TOKEN-BANDED (#168 Option C, s168-D2 pending): "
                             f"the unit is {EFFORT_UNIT}; "
                             + " · ".join(f"{k} = {m}" for k, m in EFFORT_RUNG_MEANING.items())
                             + ". Band edges are NOT typed here — gen_dashboard.effort_anchors() "
                               "derives them at build and prints them with their n")

        if it["state"] in ("done", "dropped") and not str(it.get("closed_by", "")).strip():
            fails.append(f"{iid}: state={it['state']!r} with no `closed_by` — a close is a "
                         f"claim and carries its receipt")

    # ---- the declared debt, REPORTED not hidden ----
    unconditioned = [i["id"] for i in items if i.get("condition") == UNCONDITIONED]
    stale_legacy = [i for i in LEGACY_IDS if i not in seen]
    if unconditioned:
        notes.append(f"DECLARED DEBT: {len(unconditioned)} item(s) carry no close condition "
                     f"({', '.join(unconditioned)}). Frozen set size {len(LEGACY_IDS)} — this "
                     f"number may only fall. Each needs Dave's word, not an agent's guess.")
    ranks = [i[PRIORITY_OVERRIDE] for i in items
             if isinstance(i.get(PRIORITY_OVERRIDE), int) and not isinstance(i.get(PRIORITY_OVERRIDE), bool)]
    if ranks:
        dupes = sorted({r for r in ranks if ranks.count(r) > 1})
        notes.append(f"{len(ranks)} item(s) carry a Dave {PRIORITY_OVERRIDE}; these outrank the "
                     f"dashboard's proposed score wherever they appear."
                     + (f" ⚠ rank(s) {dupes} are used more than once — ties break by id, which is "
                        f"arbitrary, not a judgement." if dupes else ""))
    n_dl = sum(1 for i in items if DEADLINE in i)
    n_ef = sum(1 for i in items if EFFORT in i)
    live_n = sum(1 for i in items if i.get("state") in LIVE_STATES)
    if n_dl or n_ef:
        notes.append(f"real-input coverage: {n_dl} item(s) carry a {DEADLINE}, {n_ef} carry an "
                     f"{EFFORT}; on those items the dashboard's PROXY is REPLACED. The rest of "
                     f"the {live_n} live item(s) are still scored by prose scan / body length.")
    else:
        notes.append(f"real-input coverage: 0 of {live_n} live item(s) carry a {DEADLINE} or "
                     f"{EFFORT} — the dashboard's deadline and effort columns are ENTIRELY "
                     f"PROXY. The fields exist and are gated; only Dave may fill them.")
    # ---- the project split, MEASURED (s172-D1). The note moves with the data — a constant
    # note is decoration, not a measurement [[measure-dont-convert-units]].
    by_project = {p: sum(1 for i in items if i.get(PROJECT) == p) for p in PROJECT_VALUES}
    if items:
        notes.append(f"project split: "
                     + " · ".join(f"{p} {n}" for p, n in by_project.items())
                     + f" (of {len(items)} items). The values written at #172 are DEFAULTS "
                       f"proposed for Dave's eye, not his ruling on each item.")
    if stale_legacy:
        notes.append(f"legacy ids retired since birth: {', '.join(stale_legacy)} "
                     f"(frozen set may shrink; it may never grow)")

    h_fails, h_note = check_homes(items)
    if h_note:
        notes.append(h_note)
    if h_fails:
        (fails if HOME_ROT_BLOCKING else notes).extend(h_fails)

    return (not fails), fails, notes


def add(doc, **fields):
    """Add an item. REFUSES without a close condition — the refusal is the feature."""
    it = {"links": [], "home": "", **fields}
    it.setdefault("condition", CONDITIONED if it.get("closes_when") else UNCONDITIONED)
    doc["items"].append(it)
    ok, fails, _ = check(doc)
    if not ok:
        mine = [f for f in fails if f.startswith(str(it.get("id")))]
        if mine:
            doc["items"].remove(it)
            raise StateError("REFUSED: " + "; ".join(mine))
    return it


# ---- queries the chain renders from ------------------------------------------------------------

def live(doc):
    return [i for i in doc["items"] if i["state"] in LIVE_STATES]


def counts(doc):
    """The counts the chain prints. GENERATED — never typed into prose.

    ★ #88's whole reason for existing: a typed count lies (#86 measured "118 markers" → ~40; the
    proposal's "95/84" is not reproducible by any probe). This function IS the count."""
    items = doc["items"]
    by_state = {s: sum(1 for i in items if i["state"] == s) for s in STATES}
    return {
        "total": len(items),
        "live": len(live(doc)),
        "by_state": by_state,
        "by_owner": {o: sum(1 for i in live(doc) if i["owner"] == o) for o in OWNERS},
        "unconditioned": sum(1 for i in items if i["condition"] == UNCONDITIONED),
        "conditioned": sum(1 for i in items if i["condition"] == CONDITIONED),
    }


def render_index(doc, width=None):
    """One-line presence index for the chain. No bodies, no truncation to 46 chars —
    the store holds the body, so the index does not have to carry it."""
    ls = live(doc)
    return " · ".join(f"`{i['id']}` {i['title']}" for i in ls)


# ---- selftest: MUTATION-TESTED, both directions ------------------------------------------------

def selftest():
    """Re-enact the defect the gate exists to catch. A green that cannot fail is an assertion,
    not a test [[gate-must-quote-what-it-forbids]] — so every bite below asserts BOTH that the
    healthy form passes AND that the mutated form fails, with the reason named."""
    fails = []
    n_bites = [0]   # COUNTED, never typed — a hand-typed bite count is the same defect
                    # class as a hand-typed item count [[measure-dont-convert-units]].

    def bite(name, doc, want_ok, want_substr=None):
        n_bites[0] += 1
        try:
            ok, fs, _ = check(doc)
        except StateError as e:
            ok, fs = False, [f"StateError: {e}"]
        if ok != want_ok:
            fails.append(f"[{name}] expected ok={want_ok}, got ok={ok} ({fs})")
            return
        if want_substr and not any(want_substr in f for f in fs):
            fails.append(f"[{name}] failed as expected but for the WRONG reason — "
                         f"wanted {want_substr!r} in {fs}")

    def healthy():
        return {"meta": {"schema": SCHEMA}, "items": [dict(
            id="G1", title="a governing item", state="open", opened=86, owner="dave",
            condition=CONDITIONED, closes_when="Dave ratifies 700 or names his own number",
            links=[], home="knowledge/_GOVERNING-RECORDS.md", project=PROJECT_VALUES[0])]}

    # 1. control
    bite("control/healthy passes", healthy(), True)

    # 2. THE CENTRAL BITE — a new item with no close condition must be REFUSED
    d = healthy(); d["items"][0]["condition"] = UNCONDITIONED; d["items"][0]["closes_when"] = None
    bite("new item, no condition, REFUSED", d, False, "frozen legacy set")

    # 3. a legacy id may be unconditioned — the exemption is real, and bounded
    d = healthy(); d["items"][0].update(id=LEGACY_IDS[0], condition=UNCONDITIONED, closes_when=None)
    bite("legacy id, unconditioned, ALLOWED", d, True)

    # 4. claiming a condition without stating one — the worst case, because it passes a naive gate
    d = healthy(); d["items"][0]["closes_when"] = "   "
    bite("condition claimed, none stated", d, False, "worse than admitting")

    # 5. an uncheckable stub condition
    d = healthy(); d["items"][0]["closes_when"] = "later"
    bite("condition too short to check", d, False, "too short to be checkable")

    # 6. condition + closes_when disagreeing the other way
    d = healthy(); d["items"][0]["condition"] = UNCONDITIONED
    bite("unconditioned but carries a condition", d, False, "say which it is")

    # 7. vocabulary drift — an unknown condition word must not be waved through
    d = healthy(); d["items"][0]["condition"] = "pending"
    bite("unknown condition word", d, False, "must be")

    # 8. duplicate ids
    d = healthy(); d["items"].append(dict(d["items"][0]))
    bite("duplicate id", d, False, "NEVER reused")

    # 9. a close with no receipt
    d = healthy(); d["items"][0]["state"] = "done"
    bite("closed with no closed_by", d, False, "carries its receipt")

    # 10. missing field
    d = healthy(); del d["items"][0]["closes_when"]
    bite("missing required field", d, False, "missing required field")

    # 11. a malformed store must RAISE, not read as empty
    try:
        check({"meta": {"schema": SCHEMA}})
        fails.append("[malformed store] expected StateError, got a clean read")
    except StateError:
        pass

    # ---- priority_override, the OPTIONAL field (#165). A presence gate must prove BOTH
    # directions: absent is legal (or the gate has quietly made it required), and every
    # malformed present value bites with its own named reason.
    # 12a. control — the field ABSENT must still pass, or the "optional" claim is false
    d = healthy(); d["items"][0].pop(PRIORITY_OVERRIDE, None)
    bite("override absent is LEGAL", d, True)

    # 12b. a real Dave rank passes
    d = healthy(); d["items"][0][PRIORITY_OVERRIDE] = 1
    bite("override 1 passes", d, True)

    # 12c. a string rank — the silent-sort defect
    d = healthy(); d["items"][0][PRIORITY_OVERRIDE] = "1"
    bite("override as string REFUSED", d, False, "must be an integer rank")

    # 12d. a bool is an int in Python — the trap this bite exists for
    d = healthy(); d["items"][0][PRIORITY_OVERRIDE] = True
    bite("override as bool REFUSED", d, False, "must be an integer rank")

    # 12e/f. out of range, both ends
    d = healthy(); d["items"][0][PRIORITY_OVERRIDE] = 0
    bite("override 0 REFUSED", d, False, "is not a rank")
    d = healthy(); d["items"][0][PRIORITY_OVERRIDE] = PRIORITY_OVERRIDE_MAX + 1
    bite("override above max REFUSED", d, False, "is not a rank")

    # 12g. duplicate ranks are a NOTE, never a failure — Dave may deliberately tie
    d = healthy()
    d["items"][0][PRIORITY_OVERRIDE] = 2
    twin = dict(d["items"][0]); twin["id"] = "G2"; d["items"].append(twin)
    ok2, _, notes2 = check(d)
    if not ok2 or not any("more than once" in n for n in notes2):
        fails.append("[duplicate override ranks] expected a PASS carrying a tie NOTE, "
                     f"got ok={ok2} notes={notes2}")

    # ---- deadline / effort, the DE-GAMING fields (#166). Same two-direction discipline:
    # absent must stay legal, every malformed present value must bite with a named reason,
    # and each bite is mutation-proved by the paired healthy form directly above it.
    # 14a. absent is legal — or "optional" is a lie and the store is now unloadable
    d = healthy(); d["items"][0].pop(DEADLINE, None); d["items"][0].pop(EFFORT, None)
    bite("deadline/effort absent is LEGAL", d, True)

    # 14b. a real ISO date passes
    d = healthy(); d["items"][0][DEADLINE] = "2026-08-14"
    bite("deadline ISO passes", d, True)

    # 14c. prose in the deadline slot — the exact thing the field replaces
    d = healthy(); d["items"][0][DEADLINE] = "friday"
    bite("deadline as prose REFUSED", d, False, "must be an ISO date")

    # 14d. wrong shape (UK order) must not be waved through
    d = healthy(); d["items"][0][DEADLINE] = "14-08-2026"
    bite("deadline wrong shape REFUSED", d, False, "must be an ISO date")

    # 14e. a non-string date
    d = healthy(); d["items"][0][DEADLINE] = 20260814
    bite("deadline as int REFUSED", d, False, "must be an ISO date")

    # 14f. SHAPE IS NOT VALIDITY — a well-formed impossible date
    d = healthy(); d["items"][0][DEADLINE] = "2026-02-30"
    bite("deadline impossible date REFUSED", d, False, "not a real calendar date")

    # 14g. effort enum passes, all three rungs
    for _v in EFFORT_VALUES:
        d = healthy(); d["items"][0][EFFORT] = _v
        bite(f"effort {_v} passes", d, True)

    # 14h. free text in the effort slot
    d = healthy(); d["items"][0][EFFORT] = "small"
    bite("effort free-text REFUSED", d, False, "must be one of")

    # 14i. case matters — 's' is not 'S', and a silently-accepted lowercase would fork the enum
    d = healthy(); d["items"][0][EFFORT] = "s"
    bite("effort lowercase REFUSED", d, False, "must be one of")

    # 14j. a number is not a size
    d = healthy(); d["items"][0][EFFORT] = 3
    bite("effort as int REFUSED", d, False, "must be one of")

    # 14j-2. #168 Option C: the REFUSAL must carry the rung STANDARD, not just the enum.
    # A refusal that says "must be one of ('S','M','L')" tells the reader the spelling and
    # nothing about what he is picking against — and an unstandardised rung is exactly the
    # arbitrariness this change exists to remove [[gate-must-quote-what-it-forbids]].
    d = healthy(); d["items"][0][EFFORT] = "XL"
    bite("effort refusal names the UNIT", d, False, "real Claude tokens of job window")
    d = healthy(); d["items"][0][EFFORT] = "XL"
    bite("effort refusal names the L rung's meaning", d, False,
         "does not fit one window")

    # 14j-3. the rung vocabulary and the gate's enum are ONE set, not two that agree today.
    # Two lists that must match are a fork waiting for a session that edits one of them.
    if tuple(EFFORT_RUNG_MEANING) != EFFORT_VALUES:
        fails.append(f"[effort rungs] EFFORT_RUNG_MEANING keys "
                     f"{tuple(EFFORT_RUNG_MEANING)!r} != EFFORT_VALUES {EFFORT_VALUES!r} — "
                     f"the documented vocabulary and the enforced enum have forked, so the "
                     f"gate now refuses a rung the page tells Dave to author, or accepts one "
                     f"it never defined")
    n_bites[0] += 1

    # 14j-4. ⛔ THE UNIT IS NOT A PLACEHOLDER. A unit string that stops naming tokens turns
    # the field back into a t-shirt size and no other test would notice.
    # ⚠ THE `sub` CLAUSE IS PART OF THE UNIT, NOT COMMENTARY (#168): a unit that stops saying
    # delegated spend is out reads as a TOTAL bill, and quota would get added to fill.
    if ("token" not in EFFORT_UNIT or "job window" not in EFFORT_UNIT
            or "sub" not in EFFORT_UNIT):
        fails.append(f"[effort unit] EFFORT_UNIT no longer names real tokens of job window with "
                     f"delegated sub spend excluded: {EFFORT_UNIT!r} — an unnamed or widened "
                     f"unit is the defect [[measure-dont-convert-units]]")
    n_bites[0] += 1

    # 14k. the coverage NOTE must move with the data — a constant note is not a measurement
    d = healthy()
    _, _, n_none = check(d)
    d["items"][0][DEADLINE] = "2026-08-14"; d["items"][0][EFFORT] = "M"
    _, _, n_some = check(d)
    if not any("ENTIRELY" in n for n in n_none) or not any("1 item(s) carry a deadline" in n
                                                           for n in n_some):
        fails.append(f"[coverage note] the real-input note did not follow the data: "
                     f"{n_none} vs {n_some}")

    # ---- `project`, the REQUIRED closed enum (s172-D1). Unlike priority_override/deadline/
    # effort this is NOT a presence-optional field, so the two directions to prove are
    # inverted: ABSENT must FAIL (or "required" is a lie), and every legal name must PASS.
    # 16a. every name in the enum passes — a gate that only ever saw one value has not been
    #      shown to accept the other, and the other is half the corpus
    for _p in PROJECT_VALUES:
        d = healthy(); d["items"][0][PROJECT] = _p
        bite(f"project {_p!r} passes", d, True)

    # 16b. THE CENTRAL BITE — an item with no project must be REFUSED, and the refusal must
    #      name the field, not just count a missing key
    d = healthy(); del d["items"][0][PROJECT]
    bite("project ABSENT is REFUSED", d, False, "missing required field(s) project")

    # 16c. ...and the refusal must carry the ENUM, or the next hand-edit invents a value
    d = healthy(); del d["items"][0][PROJECT]
    bite("project refusal names the legal values", d, False, str(PROJECT_VALUES))

    # 16d. a value outside the enum — the silent-filter defect. WORSE than absent: it reads as
    #      a classification and matches nothing.
    d = healthy(); d["items"][0][PROJECT] = "apollo-ux"
    bite("project outside the enum REFUSED", d, False, "CLOSED enum")

    # 16e. case matters — 'Apollo' is not 'apollo'; a silently-accepted capital forks the enum
    d = healthy(); d["items"][0][PROJECT] = "Apollo"
    bite("project wrong case REFUSED", d, False, "CLOSED enum")

    # 16f. a non-string is not a project name
    d = healthy(); d["items"][0][PROJECT] = None
    bite("project None REFUSED", d, False, "CLOSED enum")

    # 16g. empty string — the "I filled it in" case that fills nothing in
    d = healthy(); d["items"][0][PROJECT] = ""
    bite("project empty string REFUSED", d, False, "CLOSED enum")

    # 16h. the split NOTE must move with the data, or it is decoration wearing a measurement's
    #      clothes — the exact defect `counts()` exists to end
    d = healthy()
    twin = dict(d["items"][0]); twin["id"] = "G3"; twin[PROJECT] = PROJECT_VALUES[1]
    d["items"].append(twin)
    _, _, n_split = check(d)
    if not any(f"{PROJECT_VALUES[0]} 1" in n and f"{PROJECT_VALUES[1]} 1" in n for n in n_split):
        fails.append(f"[project split note] the note did not follow the data: {n_split}")
    n_bites[0] += 1

    # 16i. `project` is IN `REQUIRED`, not beside it. Two lists that must agree are a fork
    #      waiting for the session that edits one of them [[ban-scoped-to-a-name]].
    if PROJECT not in REQUIRED:
        fails.append(f"[project required] {PROJECT!r} is not in REQUIRED {REQUIRED!r} — the "
                     f"enum arm would still fire, but the missing-field arm would not, so an "
                     f"item with no project at all could reach a KeyError instead of a refusal")
    n_bites[0] += 1

    # 16j. ⛔ THE ENUM IS NOT A PLACEHOLDER. If the two names drift, every filter that reads
    #      them silently empties, and no other arm here would notice.
    if PROJECT_VALUES != ("apollo", "memento"):
        fails.append(f"[project enum] PROJECT_VALUES is {PROJECT_VALUES!r} — s172-D1 ruled the "
                     f"two names 'apollo' and 'memento'. Widening or renaming this enum is "
                     f"Dave's ruling; if he has ruled it, this arm is the one to change, "
                     f"deliberately, with his word attached")
    n_bites[0] += 1

    # 13. counts are computed, not stored — mutate an item, the count must move
    d = healthy()
    before = counts(d)["live"]
    d["items"][0]["state"] = "done"
    if counts(d)["live"] != before - 1:
        fails.append("[counts move] counts() did not follow the data — it is not a measurement")

    # 15. THE HOME-POINTER ROT CLASS (#168) — driven on a REAL temp tree, both directions, and
    # both sides of Dave's dial. A resolver tested only against strings would pass while every
    # pointer in the store aimed at the wrong line, which is exactly what happened #88→#167.
    import tempfile
    _hn = 0
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR", "/var/tmp")) as td:
        os.makedirs(os.path.join(td, "knowledge"), exist_ok=True)
        with open(os.path.join(td, "ROLL.md"), "w", encoding="utf-8") as f:
            f.write("banner\nbanner\n> **1. THE ITEM\nbody\n> **2. TWIN\n> **2. TWIN\n")

        def harm(name, home, want_status):
            nonlocal _hn
            _hn += 1
            st, detail = resolve_home(home, root=td)
            if st != want_status:
                fails.append(f"[home {name}] wanted {want_status!r}, got {st!r} ({detail})")
            return detail

        d1 = harm("anchor resolves", "ROLL.md#> **1. THE ITEM", "anchor-ok")
        if "line 3" not in d1:
            fails.append(f"[home anchor line] resolver did not report the LIVE line: {d1}")
        harm("anchor absent FAILS", "ROLL.md#> **9. GONE", "anchor-absent")
        harm("anchor ambiguous FAILS", "ROLL.md#> **2. TWIN", "anchor-ambiguous")
        harm("missing file FAILS", "NOPE.md#x", "missing-file")
        harm("empty home FAILS", "", "empty")
        harm("line form accepted", "ROLL.md:3", "line-ok")
        harm("line past EOF FAILS", "ROLL.md:99", "line-past-eof")

        # THE ROT ITSELF: the anchor still resolves after the surface ROLLS; the line number
        # silently points at different prose. This arm is the whole argument for the change.
        with open(os.path.join(td, "ROLL.md"), "w", encoding="utf-8") as f:
            f.write("NEW BANNER\n" * 4 + "> **1. THE ITEM\nbody\n> **2. TWIN\n")
        _hn += 1
        st_a, det_a = resolve_home("ROLL.md#> **1. THE ITEM", root=td)
        st_l, det_l = resolve_home("ROLL.md:3", root=td)
        if st_a != "anchor-ok" or "line 5" not in det_a:
            fails.append(f"[home ROLL survival] anchor did not follow the roll: {st_a} {det_a}")
        if "NEW BANNER" not in det_l:
            fails.append(f"[home ROLL rot] the line form should now quote the WRONG prose, "
                         f"proving the class: {det_l}")

        # Dave's dial, BOTH positions — a promotion nobody has driven is not available.
        bad = {"items": [dict(healthy()["items"][0], home="NOPE.md#x")]}
        global HOME_ROT_BLOCKING
        was = HOME_ROT_BLOCKING
        try:
            HOME_ROT_BLOCKING = False
            bite("home rot NOTE-only while dial is off", bad, True)
            HOME_ROT_BLOCKING = True
            bite("home rot BLOCKS when Dave flips the dial", bad, False, "home UNRESOLVABLE")
        finally:
            HOME_ROT_BLOCKING = was

    # +4 non-`bite()` arms: the malformed-store raise, the duplicate-rank NOTE, the
    # coverage NOTE, and the counts-move arm. `_hn` counts the home-resolver arms, which are
    # COUNTED by the harness, never typed [[measure-dont-convert-units]].
    return fails, n_bites[0] + 4 + _hn


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        fs, n = selftest()
        print("\n".join(fs) if fs else f"_state selftest: {n} bites, all GREEN")
        sys.exit(1 if fs else 0)
    ok, fails, notes = check()
    d = load()
    c = counts(d)
    print(f"items {c['total']} · live {c['live']} · conditioned {c['conditioned']} · "
          f"UNCONDITIONED {c['unconditioned']}")
    print(f"  by state: {c['by_state']}")
    print(f"  live by owner: {c['by_owner']}")
    for n in notes:
        print(f"  ⚠ {n}")
    for f in fails:
        print(f"  ⛔ {f}")
    sys.exit(0 if ok else 1)
