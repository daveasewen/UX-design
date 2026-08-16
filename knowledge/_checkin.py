#!/usr/bin/env python3
"""How hot are we? — an ON-DEMAND reading of the live session, at any point.

RULED #52 (D-new, Dave's): *"I do need a check-in so I can say how hot are we."*
Today's gauge speaks once, at wrap, which is the moment it is least useful
([[instrument-without-a-consumer]]). This reader answers at any moment.

WHAT IT MEASURES, AND WHAT IT REFUSES TO
------------------------------------------------------------------
The live transcript is at `.claude/projects/<encoded-project>/<sessionId>.jsonl`,
mounted read-only into the sandbox and written LIVE (verified #53: last record
13s behind `date`). It is measured HERE and never loaded into the window, so
the reading costs nothing it is measuring.

  MEASURED   the conversation half — user / assistant / attachment records.
             THROUGHPUT: cumulative, not resident.
  MEASURED   the FILL half — resident context, off `message.usage` (ENACTED #91).
             ⛔ THIS PARAGRAPH USED TO READ "UNMEASURED … `ds-025` item 1 STANDS:
             no `system` record type exists in that file." The premise was true and
             the conclusion did not follow: there is no `system` RECORD, but the
             `usage` field prices the whole call — "prompt caching references the
             entire prompt — tools, system, and messages" (Anthropic, quoted in
             `notes/_briefs/2026-07-31-compaction-and-fill-research.md` § Q3).
             That brief MEASURED boot at 61,582 on 2026-07-31 and this module went
             ~31 sessions still printing UNMEASURED, because nobody wired it
             [[instrument-without-a-consumer]] [[premise-ages-faster-than-rule]].
  UNMEASURED the DECOMPOSITION of boot into system-prompt vs tool-schemas vs
             MEMORY.md. The `usage` field gives the call's sum, not a breakdown.
             ⬛ DAVE'S RULING OWED, asked by the brief 2026-07-31 and never put to
             him: is `ds-025` item 1 the TOTAL (now closeable) or the harness-only
             DECOMPOSITION (still dark)? NEVER defaulted to a constant either way
             [[feedback-measuring-tool-must-not-guess]].

  UNIT       HEADLINE = REAL Claude tokens, via `_gauge_tokens.count()` — #83 (c)
             wires this reader to #82's unit. ONE call on the WHOLE concatenated
             conversation-half blob, never per-record: #82 MEASURED the per-record
             shape at 232 API round-trips on a live transcript, blowing the 45s
             sandbox call wall. `count()` is content-hash cached, so a re-run of an
             UNCHANGED transcript costs nothing. The method ('real' or
             'cl100k-estimate') travels WITH the number and prints on the headline
             line — never 'real' for a figure that fell back.

             BREAKDOWN stays `tape`, cl100k (tiktoken) — UNCHANGED from D1, kept for
             SHAPE only (per-type proportion, not a magnitude). ⚠ D1 rules cl100k
             UNVERIFIED against Claude's own tokenizer (p50k reads +8.6–11.1% on
             this corpus). ⛔ It does NOT sum to the headline and is NEVER scaled or
             converted to match it — converting a proxy into a measurement's
             clothes is #54's defect [[measure-dont-convert-units]].

  KIND       THROUGHPUT, not fill. A cumulative log is not a resident-context
             reading [[measure-dont-convert-units]]. Compaction/eviction would
             break the equivalence and is not observable from here.

NO PERCENTAGE WITHOUT A NAMED DENOMINATOR — D2 (c). `DEFAULT_WINDOW = 200_000`
was a TRUE OBSERVED FIGURE GONE STALE (`e7f8b87`, matching a harness warning),
and 613,386 tape ran through a session against it. A ratio is printed only if
you pass `--window` and it is captioned with the number you passed — computed
against the REAL headline since #83 (c), never against the cl100k breakdown.

FAILS LOUD without tiktoken. `_context_gauge.py` used to silently estimate and
under-report by 414 tape; FIXED #74 — it now refuses by default too, with the
chars/4 path behind an explicit `--estimate` flag that labels its output.

FAILS LOUD on the headline too. `gauge.count()` raises `MeasurementRefused`
(#79-D1) when NEITHER the API nor tiktoken is reachable, and it is PROPAGATED
here named — never caught and quietly downgraded to an estimate.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gauge_tokens as gauge     # noqa: E402 — #83 (c): the REAL headline, ONE call (below)

CONV_TYPES = ("user", "assistant", "attachment")
META_TYPES = ("queue-operation", "last-prompt", "mode")
TRANSCRIPT_GLOB = "/sessions/*/mnt/.claude/projects/*/*.jsonl"


def find_transcript(explicit: str | None) -> str:
    if explicit:
        return explicit
    hits = glob.glob(TRANSCRIPT_GLOB)
    if not hits:
        sys.exit(
            f"NO TRANSCRIPT FOUND under {TRANSCRIPT_GLOB}\n"
            "  This is an ABSENCE OF A MATCH, not a proven absence — name your probe.\n"
            "  Pass a path explicitly if the mount layout has moved."
        )
    return max(hits, key=os.path.getmtime)


def encoder():
    try:
        import tiktoken
    except ImportError:
        sys.exit(
            "REFUSING TO GUESS: tiktoken is not installed.\n"
            "  pip install tiktoken --break-system-packages\n"
            "  A measuring tool that estimates silently is the ds-025 defect."
        )
    return tiktoken.get_encoding("cl100k_base")


def measure_real(text: str) -> tuple[int, str]:
    """THE HEADLINE (#83 c) — one call to `_gauge_tokens.count()` on the WHOLE
    concatenated conversation-half blob, never per-record. #82 MEASURED the
    per-record shape at 232 API round-trips on a live transcript, blowing the
    45s sandbox call wall; `count()` is content-hash cached, so re-running
    against an unchanged transcript costs nothing.

    Mirrors `_capture_gate.py::measure_tokens()`'s own shape — the literal
    `return n, "real"` below is what lets THIS FILE satisfy
    `_produces_real_tier()`'s AST check; a registry pin is never trusted on
    its own word [[gate-must-quote-what-it-forbids]].

    ⛔ `gauge.MeasurementRefused` is deliberately NOT caught here. It
    propagates to the caller, loud and named — catching it and returning an
    estimate instead would be exactly the ds-025 defect this module refuses
    to commit.
    """
    n, method = gauge.count(text)
    if method == "real":
        return n, "real"
    return n, method


# ── FILL — the resident-context half. ENACTED #91; RESEARCHED #59-era and never wired. ──
#
# `notes/_briefs/2026-07-31-compaction-and-fill-research.md` § Q3 established this five days
# and ~31 sessions before this function existed: the answer was already in the transcript,
# unused, while the live gauge kept reporting THROUGHPUT and the read chain kept saying the
# boot half was unmeasurable. [[instrument-without-a-consumer]] — the research was right, the
# consumer was never built. This is the consumer.
#
# Anthropic's documented formula, QUOTED by that brief from primary source:
#     total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
# and: "Prompt caching references the entire prompt — tools, system, and messages (in that
# order)". So this is NOT a conversation-only proxy: the harness and system prompt are inside
# the number. That is what makes it FILL and not throughput.
#
# ⛔ IT IS NEVER CONVERTED TO OR FROM THE THROUGHPUT HEADLINE. They measure different objects.
#    [[measure-dont-convert-units]]
FILL_FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
COMPACTION_DROP = 0.10          # the brief's own threshold: no drop >10% ⇒ no compaction


def _total_in(usage: dict) -> int:
    return sum(int(usage.get(f, 0) or 0) for f in FILL_FIELDS)


def read_fill(path: str) -> dict:
    """Resident context per turn, read off the API's own accounting.

    REFUSES rather than guesses, in three named ways:
      * no usage records at all      -> available=False, reason NAMED. Never a constant.
      * synthetic / all-zero records -> SKIPPED and counted (#59 found a `model:"<synthetic>"`
                                        record with all-zero usage that "would read as 0 if it
                                        landed last" — silently reading 0 as a fill of 0 is the
                                        exact ds-025 defect).
      * records != turns             -> deduped on `message.id`; #59 verified usage is
                                        byte-identical within an id (35 records / 20 turns).

    Two checks that CAN FAIL, so a green here is evidence and not an assertion
    [[six-beat-ladder-ruled]]:
      * `compaction_records` — any `usage.iterations[].type == "compaction"`. The brief proves
        this marker exists and is left behind when compaction fires.
      * `drops` — any turn whose total falls >10% below its predecessor. Fill is monotonic
        absent compaction; a drop is either compaction or a broken read, and BOTH must surface.
    """
    turns: list[dict] = []
    seen: set[str] = set()
    skipped_synthetic = 0
    compaction_records = 0

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get("message") or {}
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                continue
            for it in usage.get("iterations") or []:
                if isinstance(it, dict) and it.get("type") == "compaction":
                    compaction_records += 1
            total = _total_in(usage)
            model = msg.get("model") or "?"
            if total == 0 or "synthetic" in str(model):
                skipped_synthetic += 1
                continue
            mid = msg.get("id") or rec.get("uuid") or f"anon-{len(turns)}"
            if mid in seen:
                continue
            seen.add(mid)
            turns.append({"id": mid, "model": model, "total": total,
                          "raw_in": int(usage.get("input_tokens", 0) or 0),
                          "cache_read": int(usage.get("cache_read_input_tokens", 0) or 0),
                          "out": int(usage.get("output_tokens", 0) or 0)})

    if not turns:
        return {"available": False,
                "reason": ("no `message.usage` record in this transcript — this is an ABSENCE "
                           "OF A MATCH, not a proven absence [[unmatched-grep-is-not-an-absence]]. "
                           "NOT defaulted to a constant."),
                "skipped_synthetic": skipped_synthetic}

    drops = [i for i in range(1, len(turns))
             if turns[i]["total"] < turns[i - 1]["total"] * (1 - COMPACTION_DROP)]
    # Cache continuity: turn N's cache_read + raw_in should reconstruct turn N-1's total.
    # It holds while the cache boundary is stable; a re-creation legitimately breaks it, so
    # this is REPORTED as a count, never asserted as a pass/fail.
    continuous = sum(1 for i in range(1, len(turns))
                     if turns[i]["cache_read"] + turns[i]["raw_in"] == turns[i - 1]["total"])
    return {"available": True,
            "boot": turns[0]["total"],
            "now": turns[-1]["total"],
            "peak": max(t["total"] for t in turns),
            "turns": len(turns),
            "continuous": continuous,
            "continuity_of": len(turns) - 1,
            "drops": drops,
            "compaction_records": compaction_records,
            "skipped_synthetic": skipped_synthetic}


# ───────────────────────────── s186-D1 Q5 — THE FIRED-COMPACTION DECLARED EVENT ─────────────
# RULED #186 (Dave, `s186-D1` Q5): *"a fired compaction becomes a declared one-line event in the
# check-in output"*. Q1 is the frame this line carries: compaction is a PARACHUTE UNDER THE WRAP,
# never a substitute — the wrap stays mandatory [[feedback-wrap-is-not-optional]].
#
# ⛔ FIRED means the MARKER, not a shape. `usage.iterations[].type == "compaction"` is the API's
# own record that it happened. A >10% fill DROP is "compaction OR a broken read" (the brief's own
# words) — it is EVIDENCE OF SOMETHING, not evidence of compaction, and declaring a drop as a
# fired compaction would be [[measure-dont-convert-units]] in event's clothing. Drops keep their
# own separate ⛔ line below and are NAMED here only as a corroborating count when the marker is
# ALSO present.
#
# SURFACE. Zero lines when nothing fired — the whole point of a declared EVENT. One line when it
# has. Precedent for the price: the B3 grade-alert surface, MEASURED at ~105 real tokens (not
# ruled — measured), which is the standing yardstick for an unprompted boot-chain surface.
COMPACTION_EVENT_PREFIX = "  ⛔ COMPACTION FIRED"


def compaction_event(fill: dict) -> str | None:
    """The ONE declared line, or None. Mutation-proven by `--selftest-compaction`."""
    if not fill.get("available"):
        return None
    n = int(fill.get("compaction_records") or 0)
    if n <= 0:
        return None
    drops = len(fill.get("drops") or [])
    corrob = f", {drops} corroborating >10% fill drop(s)" if drops else ""
    return (f"{COMPACTION_EVENT_PREFIX}  {n} `usage.iterations` compaction record(s){corrob}"
            " — FILL below is POST-compaction; the wrap is still owed"
            " (s186-D1 Q1: a parachute under the wrap, never a substitute).")


# ════════════════════════════════════════════════════════════ B2 — THE PLAN BLOCK (`--block`)
#
# The six-line block the Arize harness note calls a "short plan re-injected ahead of noisy
# history". Ours differs in ONE load-bearing way and it is the whole design:
#
#   ★★★ GENERATE-NEVER-INHERIT. The block is a RENDERING of state, never a store. There is no
#   `current.md`, no fifth register, nothing to hand-edit. If the block is wrong, the STATE is
#   wrong — fix the state and regenerate. A block pasted forward from the previous seam is the
#   [[read-chain-is-where-staleness-is-free]] class, and `--verify-block` exists to catch it
#   MECHANICALLY rather than on anybody's memory.
#
# WHAT IS HASHED, AND WHY THAT SPLIT.  `integrity` = sha256 over (the emitted body text, with
# the digest itself blanked) ⊕ (the sha256 of each STATE source's bytes). Three defects each
# land on it from a different direction, which is why one digest is enough:
#     * a hand-edited line          -> the candidate's own text no longer hashes to its digest
#     * a corrupted SOURCE mtime    -> the mtime is IN the hashed text (and is separately
#                                     compared to the file on disk, so the refusal is NAMED)
#     * a block carried across a state change -> the live source sha differs from the one hashed
# ⛔ THE TRANSCRIPT IS DELIBERATELY NOT A HASHED SOURCE. It is written live, every turn; hashing
# it would make every honestly-emitted block invalid within seconds, and a gate that always
# fails is worth exactly as much as one that cannot [[instrument-without-a-consumer]]. It is
# NAMED on the SOURCE line as the BUDGET's provenance and marked `unhashed` there.
#
# ⛔ BUDGET IS EXCLUDED FROM THE FIELD RE-DERIVATION for the same reason: FILL moves every call,
# so comparing it would fail on every honest block. It is hashed as WRITTEN (so it cannot be
# hand-edited) but never re-derived. STOP is state-only on purpose — the volatile part (room to
# the stop line) lives on the BUDGET line, where volatility belongs.
#
# ⛔ NOTHING HERE GUESSES. A source that will not parse yields the literal string `UNKNOWN — …`
# with the probe named, never a default and never a plausible-looking value
# [[feedback-measuring-tool-must-not-guess]]. `UNKNOWN` is hashed like any other text.

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The STATE sources. These three, in this order, are what DONE / DOING / NEXT / STOP are
# derived from, and the SOURCE line names every one of them with its mtime.
BLOCK_STATE_SOURCES = ("_CHAIN.md", "_LIVE-STATE.md", "knowledge/_lanes.json")

# PICKED, NOT DERIVED — and labelled so, because [[gate-narrows-its-own-rule]]: 15 minutes is a
# round number chosen to be shorter than any plausible lane, not a measurement of anything.
# Override with --max-age. It is the leg that catches a block that is textually perfect and
# simply OLD (state unchanged, but the seam it was rendered for is long past).
BLOCK_MAX_AGE_S = 900

BLOCK_FIELDS = ("SOURCE", "DONE", "DOING", "NEXT", "STOP", "BUDGET")
_DIGEST_PLACEHOLDER = "integrity <PENDING>"

LS_DELTA_RE = re.compile(r"^##\s*⏱\s*LATEST DELTA\s*[—-]\s*(.+?)\s*$")
CHAIN_SESSION_RE = re.compile(r"YOU ARE\s+#(\d+)\b")
CHAIN_STOP_RE = re.compile(r"stop line\s*\**\s*([\d][\d,]*)")
# ⚠ `*` and backticks ONLY. `_` is NOT stripped: it is markdown emphasis in prose and a
# character inside every identifier we quote (`total_input_tokens`, `_lanes.json`), and the
# first draft of this line silently rendered `totalinputtokens` — a provenance string that no
# longer names the field it cites [[silent-lookup-failure-class]].
_MD_NOISE_RE = re.compile(r"[*`]+")


def _iso(epoch: float) -> str:
    return _dt.datetime.fromtimestamp(epoch, _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _flatten(s: str, limit: int = 150) -> str:
    """One line, markdown noise stripped, TRUNCATION DECLARED IN THE TEXT (never silent)."""
    s = _MD_NOISE_RE.sub("", s)
    s = " ".join(s.split())
    if len(s) > limit:
        s = s[:limit].rstrip() + " …[TRUNCATED]"
    return s


def read_block_sources(repo: str = REPO) -> dict:
    """Read the state sources. A missing one is a LOUD, NAMED exit — never a silent omission,
    which would render a block whose SOURCE line lies by absence."""
    out: dict[str, dict] = {}
    for rel in BLOCK_STATE_SOURCES:
        path = os.path.join(repo, rel)
        if not os.path.isfile(path):
            sys.exit(
                f"PLAN BLOCK REFUSED: state source {rel!r} does not exist at {path}.\n"
                "  The block is a rendering of state; a missing source is a missing rendering,\n"
                "  not a block with one fewer line. Name the move and fix BLOCK_STATE_SOURCES.")
        data = open(path, "rb").read()
        out[rel] = {"path": path,
                    "mtime": os.path.getmtime(path),
                    "mtime_iso": _iso(os.path.getmtime(path)),
                    "sha": hashlib.sha256(data).hexdigest(),
                    "text": data.decode("utf-8", "replace")}
    return out


def derive_block_fields(src: dict) -> dict:
    """DONE / DOING / NEXT / STOP, each from a NAMED probe on a NAMED source."""
    chain = src["_CHAIN.md"]["text"]
    ls = src["_LIVE-STATE.md"]["text"]

    # ---- session number (labels DOING; it is the chain's own line, not a guess)
    m = CHAIN_SESSION_RE.search(chain)
    session = f"#{m.group(1)}" if m else "#? (UNKNOWN — no `YOU ARE #N` line in _CHAIN.md)"

    # ---- DONE — the last landed delta, from _LIVE-STATE.md's ⏱ LATEST DELTA heading.
    done = None
    for ln in ls.splitlines():
        mm = LS_DELTA_RE.match(ln)
        if mm:
            done = _flatten(mm.group(1))
            break
    if done is None:
        done = ("UNKNOWN — no `## ⏱ LATEST DELTA` heading matched in _LIVE-STATE.md "
                "(probe: LS_DELTA_RE). NOT defaulted.")

    # ---- DOING / NEXT — from the lane records. `active` lanes only; a lane's own step states
    # decide. ⛔ If more than one lane is active the block LISTS THEM ALL rather than picking:
    # picking would be a ruling [[feedback-dont-launder-a-premise-into-a-ruling]].
    try:
        lanes = json.loads(src["knowledge/_lanes.json"]["text"]).get("lanes", [])
    except json.JSONDecodeError as e:
        lanes = None
        doing = f"UNKNOWN — knowledge/_lanes.json does not parse ({e}). NOT defaulted."
        nxt = doing
    if lanes is not None:
        active = [l for l in lanes if l.get("state") == "active"]
        if not active:
            doing = ("UNKNOWN — no lane in state `active` in knowledge/_lanes.json "
                     "(probe: state == 'active'). NOT defaulted.")
            nxt = doing
        else:
            bits, nxts = [], []
            for l in active:
                steps = l.get("sequence") or []
                cur = next((s for s in steps if s.get("state") == "active"), None)
                bits.append(f"{l.get('id')} · " + (
                    _flatten(cur["step"], 90) if cur
                    else "no step marked `active` (lane active, step UNKNOWN)"))
                q = next((s for s in steps if s.get("state") == "queued"), None)
                nxts.append(f"{l.get('id')} · " + (
                    _flatten(q["step"], 90) if q else "no `queued` step left in this lane"))
            doing = _flatten(f"{session} · " + " ‖ ".join(bits), 190)
            nxt = _flatten(" ‖ ".join(nxts), 190)

    # ---- STOP — the stop-line figure as STATED by the chain. ⛔ Never a literal typed here:
    # a constant invented by this script would be a stop line nobody ruled.
    ms = CHAIN_STOP_RE.search(chain)
    if ms:
        stop = (f"FILL {ms.group(1)} real — the stop line as stated in _CHAIN.md "
                f"(probe: CHAIN_STOP_RE); job room = stop line − current FILL, on the BUDGET line")
        stop_n = int(ms.group(1).replace(",", ""))
    else:
        stop = ("UNKNOWN — no `stop line <N>` figure found in _CHAIN.md (probe: CHAIN_STOP_RE). "
                "NOT defaulted to a constant.")
        stop_n = None
    return {"DONE": done, "DOING": doing, "NEXT": nxt, "STOP": stop,
            "_session": session, "_stop_n": stop_n}


def derive_budget(path: str, fill: dict, stop_n: int | None) -> str:
    """The gauge headline, REAL tokens, method travelling WITH the number (#83 c / #56).
    ⛔ No percentage without a named denominator, and no figure without its method."""
    if not fill.get("available"):
        head = f"FILL UNAVAILABLE — {fill.get('reason', 'reason not reported')}"
    else:
        head = (f"FILL {fill['now']:,} real (`message.usage` total_input_tokens, last turn — "
                f"a FLOOR, late by one step) · boot {fill['boot']:,} · peak {fill['peak']:,} "
                f"over {fill['turns']} turns")
        if stop_n is not None:
            room = stop_n - fill["now"]
            head += (f" · room to stop line {room:,}" if room >= 0
                     else f" · ⛔ PAST the stop line by {abs(room):,}")
    try:
        n, method = measure_real(_conversation_blob(path))
        head += f" · throughput {n:,} {method} (gauge.count, ONE call — NOT comparable to FILL)"
    except gauge.MeasurementRefused as e:
        head += (f" · throughput MEASUREMENT REFUSED ({e}) — named, never downgraded to an "
                 f"estimate")
    return _flatten(head, 320)


def _conversation_blob(path: str) -> str:
    """The conversation half, concatenated — the same object `main()` measures, factored out so
    `--block` measures the SAME THING and not a look-alike [[attribute-the-diff]]."""
    parts = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type", "?") in META_TYPES:
            continue
        parts.append(json.dumps(rec.get("message", rec)))
    return "\n".join(parts)


def _source_line(src: dict, transcript: str, rendered: str, digest: str) -> str:
    clauses = [f"{rel} @ {src[rel]['mtime_iso']}" for rel in BLOCK_STATE_SOURCES]
    clauses.append(f"transcript {os.path.basename(transcript)} @ "
                   f"{_iso(os.path.getmtime(transcript))} (BUDGET only, unhashed)")
    clauses.append(f"rendered {rendered}")
    clauses.append(f"integrity {digest}")
    return "SOURCE: " + " · ".join(clauses)


def _digest(body: list[str], src: dict) -> str:
    """sha256 over (the block's own text, digest blanked) ⊕ (each state source's content sha).
    Both halves are load-bearing — see the header block above."""
    # ⚠ `body` ARRIVES WITH THE DIGEST ALREADY BLANKED to `_DIGEST_PLACEHOLDER` — by the caller,
    # both at render (it has not been computed yet) and at verify (it is substituted out). A
    # digest that hashed itself would be uncomputable; a digest that hashed a DIFFERENT blank on
    # each side would never match. Asserted here rather than trusted.
    if _DIGEST_PLACEHOLDER not in body[0]:
        raise ValueError(f"_digest(): body[0] must carry {_DIGEST_PLACEHOLDER!r}, got: {body[0]}")
    canon = {"v": 1, "body": list(body),
             "sources": {rel: src[rel]["sha"] for rel in BLOCK_STATE_SOURCES}}
    blob = json.dumps(canon, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:12]


def render_block(path: str, fill: dict, repo: str = REPO) -> str:
    src = read_block_sources(repo)
    f = derive_block_fields(src)
    budget = derive_budget(path, fill, f["_stop_n"])
    rendered = _iso(_dt.datetime.now(_dt.timezone.utc).timestamp())
    body = [_source_line(src, path, rendered, "<PENDING>"),
            f"DONE:   {f['DONE']}",
            f"DOING:  {f['DOING']}",
            f"NEXT:   {f['NEXT']}",
            f"STOP:   {f['STOP']}",
            f"BUDGET: {budget}"]
    digest = _digest(body, src)
    body[0] = _source_line(src, path, rendered, digest)
    return "\n".join(body)


# ---------------------------------------------------------------- the seam check (`--verify-block`)
_CLAUSE_SRC_RE = re.compile(r"^(?P<rel>[^ ]+) @ (?P<iso>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$")


def verify_block(text: str, path: str, fill: dict, repo: str = REPO,
                 max_age: int = BLOCK_MAX_AGE_S) -> tuple[bool, list[str], list[str]]:
    """Grade a candidate block against LIVE state. Returns (ok, reasons, notes).

    EVERY failing leg is reported, not just the first — [[refusal-names-the-first-obstacle]]:
    the first obstacle a check meets is rarely the binding one, and a block can be stale AND
    hand-edited at once.
    """
    reasons: list[str] = []
    notes: list[str] = []
    lines = [ln for ln in text.splitlines() if ln.strip()]

    # ---- leg 0: SHAPE. Six fields, in order, or it is not a plan block at all.
    got = [ln.split(":", 1)[0].strip() for ln in lines[:len(BLOCK_FIELDS)]]
    if len(lines) != len(BLOCK_FIELDS) or got != list(BLOCK_FIELDS):
        return (False, [f"SHAPE: expected exactly {len(BLOCK_FIELDS)} lines "
                        f"{list(BLOCK_FIELDS)}, got {len(lines)} line(s) {got} — this is not a "
                        f"plan block; nothing further was checked."], notes)

    src = read_block_sources(repo)
    source_line = lines[0]
    clauses = source_line[len("SOURCE:"):].strip().split(" · ")

    declared_mtimes: dict[str, str] = {}
    declared_digest = None
    rendered_iso = None
    for c in clauses:
        if c.startswith("integrity "):
            declared_digest = c.split(" ", 1)[1].strip()
        elif c.startswith("rendered "):
            rendered_iso = c.split(" ", 1)[1].strip()
        elif c.startswith("transcript "):
            continue                              # named, unhashed, deliberately not graded
        else:
            m = _CLAUSE_SRC_RE.match(c)
            if m:
                declared_mtimes[m.group("rel")] = m.group("iso")

    # ---- leg 1: PROVENANCE. Every state source named, and its mtime matching the disk.
    missing = [r for r in BLOCK_STATE_SOURCES if r not in declared_mtimes]
    if missing:
        reasons.append(f"PROVENANCE: SOURCE line does not name {missing} — a block whose "
                       f"provenance line is incomplete cannot be graded against state (P1).")
    for rel, iso in declared_mtimes.items():
        if rel not in src:
            reasons.append(f"PROVENANCE: SOURCE names {rel!r}, which is not a state source "
                           f"({list(BLOCK_STATE_SOURCES)}).")
        elif iso != src[rel]["mtime_iso"]:
            reasons.append(f"MTIME: {rel} declared @ {iso}, on disk @ {src[rel]['mtime_iso']} "
                           f"— the block was rendered against a different state, or the "
                           f"provenance line was edited. REGENERATE, never repair.")
    if declared_digest is None:
        reasons.append("INTEGRITY: no `integrity <hex>` clause on the SOURCE line — an "
                       "unhashed block is indistinguishable from a hand-written one.")

    # ---- leg 2: INTEGRITY. Recompute over the CANDIDATE'S OWN text ⊕ the LIVE source shas.
    if declared_digest is not None:
        probe_body = [source_line.replace(f"integrity {declared_digest}", "integrity <PENDING>")]
        probe_body += lines[1:]
        recomputed = _digest(probe_body, src)
        if recomputed != declared_digest:
            reasons.append(f"INTEGRITY: declared {declared_digest}, recomputed {recomputed} "
                           f"over this block's own text ⊕ live state — the text was edited, or "
                           f"state moved under it. A block is a RENDERING; regenerate it.")

    # ---- leg 3: RE-DERIVATION. Name WHICH field is stale, so the refusal is diagnostic and not
    # merely a hash complaint. BUDGET is excluded BY CONSTRUCTION (it moves every call).
    fresh = derive_block_fields(src)
    for i, field in enumerate(("DONE", "DOING", "NEXT", "STOP"), start=1):
        want = f"{field + ':':<7} {fresh[field]}"
        if lines[i] != want:
            reasons.append(f"NON-REGENERATED: {field} reads\n      {lines[i]}\n"
                           f"    live state renders\n      {want}")
    notes.append("BUDGET was NOT re-derived — FILL moves every call, so equality there would "
                 "fail on every honest block. It is hashed as written, never re-measured.")

    # ---- leg 4: AGE. Textually perfect and simply old.
    if rendered_iso is None:
        reasons.append("AGE: no `rendered <iso>` clause — a block with no render time cannot be "
                       "shown to belong to THIS seam.")
    else:
        try:
            t = _dt.datetime.strptime(rendered_iso, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=_dt.timezone.utc)
            age = (_dt.datetime.now(_dt.timezone.utc) - t).total_seconds()
            notes.append(f"age {age:.0f}s (limit {max_age}s — PICKED, not derived)")
            if age > max_age:
                reasons.append(f"AGE: rendered {age:.0f}s ago, past the {max_age}s limit — "
                               f"carried forward across a seam. GENERATE-NEVER-INHERIT.")
        except ValueError:
            reasons.append(f"AGE: `rendered {rendered_iso}` is not an ISO-8601 UTC stamp.")

    return (not reasons, reasons, notes)


# ------------------------------------------------------- THE SEAM OBLIGATION (`--block` WIRED)
# ⛔ WHY THIS EXISTS AT ALL. `--block`, `--verify-block` and `--selftest-block` were built at
# #178 and WIRED INTO NO SEAM: a correct instrument nobody's workflow demands, which is the
# [[instrument-without-a-consumer]] class minted ~90 times before the rule. This function is the
# CONSUMER. It is called by the DEFAULT check-in run — the thing already law at every lane seam
# ("run `_checkin.py`", [[checkin-is-mandatory-not-optional]]) — so the seam now hands back a
# block that was REGENERATED and GRADED in the same breath, and nobody is ever in the position
# of having a block to paste. It is deliberately NOT a new command and NOT a new state store
# (brief §6 P3): the block remains a rendering, and this is only where the rendering is demanded.
#
# THREE LEGS, and each is one of the brief's BLOCKs:
#   P1 (missing SOURCE provenance) -> `verify_block` leg 1, which grades the block we just
#      rendered against the disk it claims to come from.
#   P2 (not regenerated / input-hash mismatch) -> `verify_block` legs 2+3, on the SAME integrity
#      digest `--block` already emits. ⛔ NOT a second hash and NOT a second store.
#   STATE-UNRESOLVED (new here, and the leg with real teeth at a healthy seam) -> a field that
#      renders `UNKNOWN — …`. `verify_block` CANNOT catch this: an UNKNOWN is honestly rendered,
#      honestly hashed and re-derives identically, so a block full of UNKNOWNs is a VALID block
#      about UNREADABLE state. At a seam that is exactly the thing that must stop the lane — the
#      block's job is to carry DONE/DOING/NEXT/STOP across the seam, and it cannot carry what it
#      could not read. The leg is NAMED separately so the refusal says which
#      [[refusal-names-the-first-obstacle]], and it lives HERE rather than inside `verify_block`
#      because a CANDIDATE block quoting an UNKNOWN faithfully is not thereby forged.
_UNRESOLVED_RE = re.compile(r"\bUNKNOWN\s+—")


def seam_block(path: str, fill: dict, repo: str = REPO,
               max_age: int = BLOCK_MAX_AGE_S) -> tuple[bool, str, list[str], list[str]]:
    """Render the block for THIS seam and grade it on the spot. (ok, block, reasons, notes)."""
    block = render_block(path, fill, repo=repo)
    _ok, reasons, notes = verify_block(block, path, fill, repo=repo, max_age=max_age)
    for line in block.splitlines()[1:]:
        field = line.split(":", 1)[0].strip()
        if field == "BUDGET":
            continue                      # BUDGET names its own refusals in gauge vocabulary
        if _UNRESOLVED_RE.search(line):
            reasons.append(f"STATE-UNRESOLVED: {field} did not resolve from state —\n"
                           f"      {line}\n"
                           f"    The block is a rendering; an UNKNOWN field means the SEAM has "
                           f"no {field}. Fix the state, never the block.")
    return (not reasons, block, reasons, notes)


# ------------------------------------------------------------------ the mutation tests (§8)
# ⛔ A GREEN THAT CANNOT FAIL IS AN ASSERTION [[six-beat-ladder-ruled]]. Every arm below is a
# DRIVE of the real `render_block` / `verify_block` on a real block, and each mutation must be
# rejected FOR ITS OWN NAMED LEG — "rejected somehow" would pass even if the checker had
# collapsed into a rubber stamp that refuses everything, which is why the CONTROL arm (an
# untouched block, which must be ACCEPTED) is part of the same run and not an afterthought.
#
# It runs against a COPY of the state sources in a temp dir (`shutil.copy2`, mtimes preserved),
# so it can move state under a block without touching the repo.

def selftest_block(path: str, fill: dict) -> int:
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="checkin-block-")
    for rel in BLOCK_STATE_SOURCES:
        dst = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(REPO, rel), dst)

    block = render_block(path, fill, repo=tmp)
    arms: list[tuple[str, str, list[str], int]] = []   # name, expect-leg, reasons, verdict

    def drive(name: str, candidate: str, expect_leg: str | None, max_age: int = BLOCK_MAX_AGE_S):
        ok, reasons, _ = verify_block(candidate, path, fill, repo=tmp, max_age=max_age)
        if expect_leg is None:
            good = ok
        else:
            good = (not ok) and any(r.startswith(expect_leg) for r in reasons)
        arms.append((name, expect_leg or "ACCEPT", reasons, good))
        return good

    lines = block.splitlines()

    # CONTROL — untouched. Must be ACCEPTED, or every rejection below proves nothing.
    drive("control: block as emitted", block, None)

    # (a) CORRUPT THE SOURCE MTIME — the brief's first named mutation.
    m = re.search(r"_CHAIN\.md @ (\S+)", lines[0])
    bad_mtime = [lines[0].replace(f"_CHAIN.md @ {m.group(1)}",
                                  "_CHAIN.md @ 1999-01-01T00:00:00Z")] + lines[1:]
    drive("(a) SOURCE mtime corrupted", "\n".join(bad_mtime), "MTIME")

    # (b) HAND-EDIT AN EMITTED BLOCK — the brief's second. The DONE line is retyped; the digest
    #     is left as it was, which is precisely what a human pasting a block forward does.
    hand = list(lines)
    hand[1] = "DONE:   #171 wrapped and everything is fine"
    drive("(b) DONE line hand-edited", "\n".join(hand), "INTEGRITY")

    # (b′) HAND-EDIT + RECOMPUTED DIGEST — defence in depth. Someone who re-hashes their own
    #      forgery still loses, because leg 3 re-derives the field from state.
    forged_body = ["DONE:   #171 wrapped and everything is fine" if i == 1 else ln
                   for i, ln in enumerate(lines)]
    old_digest = re.search(r"integrity (\w+)", lines[0]).group(1)
    probe = [forged_body[0].replace(f"integrity {old_digest}", "integrity <PENDING>")]
    probe += forged_body[1:]
    forged_body[0] = forged_body[0].replace(f"integrity {old_digest}",
                                            f"integrity {_digest(probe, read_block_sources(tmp))}")
    drive("(b′) hand-edited AND re-hashed", "\n".join(forged_body), "NON-REGENERATED")

    # (d) AGE — a textually perfect block carried across a seam. ⚠ RUN BEFORE (c): (c) moves the
    #     temp state permanently, and an arm graded after it would be reported as failing AGE
    #     while actually failing three legs — a contaminated arm proves the wrong thing
    #     [[attribute-the-diff]].
    drive("(d) carried forward (age limit 0s)", block, "AGE", max_age=0)

    # (c) STATE MOVED UNDER THE BLOCK, WITH THE MTIME RESTORED — the stale-block class in its
    #     nastiest form: the provenance line is TRUE and the content is not.
    lanes_p = os.path.join(tmp, "knowledge/_lanes.json")
    st = os.stat(lanes_p)
    doc = json.loads(open(lanes_p, encoding="utf-8").read())
    for lane in doc["lanes"]:
        for step in lane.get("sequence", []):
            if step.get("state") == "queued":
                step["step"] = "MUTATED — a different next step entirely"
                break
    open(lanes_p, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=2))
    os.utime(lanes_p, (st.st_atime, st.st_mtime))          # mtime restored: the leg-1 alibi
    drive("(c) state changed, mtime restored", block, "INTEGRITY")

    # ---------------------------------------------------------------- THE SEAM GATE'S OWN ARMS
    # ⚠ A SECOND, UNCONTAMINATED COPY. Arm (c) above mutated `tmp`'s lanes file permanently; a
    # seam arm graded on it would be reported as failing its own leg while actually failing
    # someone else's mutation [[attribute-the-diff]].
    tmp2 = tempfile.mkdtemp(prefix="checkin-seam-")
    for rel in BLOCK_STATE_SOURCES:
        dst = os.path.join(tmp2, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(REPO, rel), dst)

    def drive_seam(name: str, expect_leg: str | None):
        ok, _blk, reasons, _ = seam_block(path, fill, repo=tmp2)
        good = ok if expect_leg is None else (
            (not ok) and any(r.startswith(expect_leg) for r in reasons))
        arms.append((name, expect_leg or "ACCEPT", reasons, good))
        return good

    # CONTROL — the seam gate on healthy state must CLEAR, or every seam rejection below is a
    # rubber stamp refusing everything.
    drive_seam("seam control: live state", None)

    # (e) STATE THAT WILL NOT PARSE. The block still renders, still hashes, still re-derives —
    #     it is a VALID block about UNREADABLE state, which is precisely the case `verify_block`
    #     cannot see and the seam must refuse.
    lanes2 = os.path.join(tmp2, "knowledge/_lanes.json")
    open(lanes2, "w", encoding="utf-8").write("{ this is not JSON")
    drive_seam("(e) lanes file unparseable -> seam", "STATE-UNRESOLVED")

    print("PLAN BLOCK — MUTATION TESTS (each arm DRIVES the real checker)")
    print(f"  temp state copy: {tmp}")
    for name, expect, reasons, good in arms:
        verdict = "PASS" if good else "⛔ FAIL"
        legs = ", ".join(r.split(":", 1)[0] for r in reasons) or "—"
        print(f"  {verdict:<7} {name:<38} expect {expect:<16} got legs: {legs}")
    failed = [a for a in arms if not a[3]]
    if failed:
        print(f"  ⛔ {len(failed)} arm(s) did not behave as specified — the checker is NOT proven.")
        for name, expect, reasons, _ in failed:
            print(f"     {name}: expected {expect}; reasons were {reasons}")
        return 1
    print(f"  ✅ {len(arms)}/{len(arms)} arms behaved as specified: the control is ACCEPTED and")
    print("     each mutation is REJECTED on its OWN named leg. The green can fail.")
    return 0


# ---------------------------------------------- s186-D1 Q5's mutation test (`--selftest-compaction`)
# ⛔ A GREEN THAT CANNOT FAIL IS AN ASSERTION [[six-beat-ladder-ruled]]. Every arm below DRIVES the
# REAL `read_fill()` on a REAL jsonl file written to a temp dir — not a hand-built dict — so the
# marker has to survive the actual parse. The CONTROL arm (a transcript with NO compaction, which
# must produce NO line) is part of the same run: without it, a clause that emits the line
# unconditionally would pass every other arm [[mutation-tests-the-clause-not-the-feature]].
def selftest_compaction() -> int:
    import tempfile

    def write(recs: list[dict]) -> str:
        fd, p = tempfile.mkstemp(prefix="checkin-compaction-", suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r) + "\n")
        return p

    def turn(mid: str, total: int, iters: list | None = None) -> dict:
        u = {"input_tokens": total, "cache_creation_input_tokens": 0,
             "cache_read_input_tokens": 0, "output_tokens": 10}
        if iters is not None:
            u["iterations"] = iters
        return {"type": "assistant", "message": {"id": mid, "model": "claude-x", "usage": u}}

    arms: list[tuple[str, str, str | None, bool]] = []

    def drive(name: str, recs: list[dict], expect: str) -> None:
        line = compaction_event(read_fill(write(recs)))
        if expect == "NO-LINE":
            good = line is None
        else:
            good = line is not None and line.startswith(COMPACTION_EVENT_PREFIX) and expect in line
        arms.append((name, expect, line, good))

    # CONTROL — a healthy transcript, no marker. MUST emit nothing, or every arm below is a
    # rubber stamp that prints the event whatever the transcript says.
    drive("control: no compaction marker", [turn("a", 1000), turn("b", 1200)], "NO-LINE")

    # (a) THE MARKER FIRED — the ruled case. One line, naming the count.
    drive("(a) one compaction record",
          [turn("a", 1000), turn("b", 1200, [{"type": "compaction"}])],
          "1 `usage.iterations` compaction record(s)")

    # (b) FIRED, WITH A CORROBORATING DROP — the count of drops rides the SAME line, never a
    #     second one, and never re-declares the drop as the event.
    drive("(b) marker + >10% fill drop",
          [turn("a", 10000), turn("b", 1000, [{"type": "compaction"}])],
          "corroborating >10% fill drop(s)")

    # (c) A DROP WITH NO MARKER — the discrimination that makes the event honest. A >10% drop is
    #     "compaction OR a broken read"; declaring it as a fired compaction is the defect. MUST
    #     emit NOTHING here, while the separate drops line (unchanged) still reports it.
    drive("(c) drop only, no marker", [turn("a", 10000), turn("b", 1000)], "NO-LINE")

    # (d) NO USABLE FILL AT ALL — read_fill refuses; the event must refuse with it, never guess.
    drive("(d) no usage records at all",
          [{"type": "user", "message": {"id": "u", "content": "hi"}}], "NO-LINE")

    print("FIRED-COMPACTION DECLARED EVENT (s186-D1 Q5) — MUTATION TESTS")
    print("  each arm DRIVES the real read_fill() on a real jsonl")
    for name, expect, line, good in arms:
        verdict = "PASS" if good else "⛔ FAIL"
        print(f"  {verdict:<7} {name:<34} expect {expect[:44]!r}")
        if not good:
            print(f"          got: {line!r}")
    failed = [a for a in arms if not a[3]]
    if failed:
        print(f"  ⛔ {len(failed)} arm(s) did not behave as specified — the clause is NOT proven.")
        return 1
    print(f"  ✅ {len(arms)}/{len(arms)} arms behaved as specified: the control emits NOTHING and")
    print("     the fired case emits exactly one declared line. The green can fail.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="On-demand context check-in.")
    ap.add_argument("path", nargs="?", help="Transcript jsonl (default: newest mounted).")
    ap.add_argument("--window", type=int, default=None,
                    help="Denominator for a ratio. NAMED in the output. Omitted = no ratio.")
    ap.add_argument("--json", action="store_true", help="Machine-readable.")
    ap.add_argument("--block", action="store_true",
                    help="Emit the six-line plan block (B2), REGENERATED from state. It is a "
                         "rendering, never a store: paste it into a sub-brief, never into the "
                         "next block.")
    ap.add_argument("--verify-block", metavar="FILE",
                    help="Grade a candidate block against LIVE state ('-' = stdin). Exit 3 on "
                         "rejection, with every failing leg named.")
    ap.add_argument("--selftest-block", action="store_true",
                    help="Drive the block's mutation tests (control + 5 mutations). Exit 1 if "
                         "any arm does not behave as specified.")
    ap.add_argument("--selftest-compaction", action="store_true",
                    help="Drive the fired-compaction declared event's mutation tests (s186-D1 "
                         "Q5: control + 4 arms). Exit 1 if any arm does not behave as specified.")
    ap.add_argument("--max-age", type=int, default=BLOCK_MAX_AGE_S,
                    help=f"Seconds a block may be old before --verify-block rejects it "
                         f"(default {BLOCK_MAX_AGE_S}; PICKED, not derived).")
    ap.add_argument("--no-rehearse", action="store_true",
                    help="Skip the wrap-gate rehearsal (#92). Default is to run it: a fail "
                         "found at a check-in costs a cheap edit; the same fail found at wrap "
                         "costs a probe→fix→re-gate round at peak fill (#91-F5).")
    ap.add_argument("--no-grades", action="store_true",
                    help="Skip the B3 grade alerts (s179-D1). ⛔ Skipping is a MEASUREMENT hole: "
                         "the surface's real-token cost is being priced for Dave's B3 review, "
                         "and a boot that skipped it logs no row.")
    ap.add_argument("--no-block", action="store_true",
                    help="Skip the B2 seam block. ⛔ An escape hatch for a broken mount, not a "
                         "convenience: skipping it means the seam has NO graded block and the "
                         "next brief has nothing legitimate to carry.")
    args = ap.parse_args()

    if args.selftest_compaction:
        return selftest_compaction()

    path = find_transcript(args.path)
    fill = read_fill(path)   # FILL — read off `usage`, independent of every tape figure below

    # ---- B2: the plan block. Handled BEFORE the encoder/breakdown work — the block needs the
    # headline and FILL, not the per-type shape, and a seam check should be cheap enough that
    # nobody skips it.
    if args.verify_block:
        raw = (sys.stdin.read() if args.verify_block == "-"
               else open(args.verify_block, encoding="utf-8").read())
        ok, reasons, notes = verify_block(raw, path, fill, max_age=args.max_age)
        print("PLAN BLOCK — SEAM CHECK")
        for n in notes:
            print(f"  ⚠ {n}")
        if ok:
            print("  ✅ ACCEPTED — regenerated from the state on disk, integrity digest matches,")
            print("     every source's mtime matches, no field re-derives differently.")
            return 0
        print(f"  ⛔ BLOCK REJECTED — {len(reasons)} failing leg(s):")
        for i, r in enumerate(reasons, 1):
            print(f"  {i}. {r}")
        print("  ⇒ A block is a RENDERING of state. Do not repair it by hand — fix the state if")
        print("     the state is wrong, then `python3 knowledge/_checkin.py --block` again.")
        return 3

    if args.selftest_block:
        return selftest_block(path, fill)

    if args.block:
        print(render_block(path, fill))
        return 0

    enc = encoder()

    by_type: dict[str, int] = {}
    records = 0
    stamps: list[str] = []
    parts: list[str] = []      # conversation-half payloads, concatenated for the ONE real call
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        records += 1
        kind = rec.get("type", "?")
        if rec.get("timestamp"):
            stamps.append(rec["timestamp"])
        if kind in META_TYPES:
            continue
        payload = rec.get("message", rec)
        payload_json = json.dumps(payload)
        by_type[kind] = by_type.get(kind, 0) + len(enc.encode(payload_json))
        parts.append(payload_json)

    measured = sum(by_type.values())

    # ---- THE HEADLINE (#83 c). ONE gauge.count() call on the WHOLE blob, never per-record —
    # #82 measured 232 round-trips that way; count() is content-hash cached so a re-run of an
    # unchanged transcript is free. MeasurementRefused propagates NAMED, never swallowed.
    try:
        real_measured, real_method = measure_real("\n".join(parts))
    except gauge.MeasurementRefused as e:
        sys.exit(f"HEADLINE REAL MEASUREMENT REFUSED — real Claude tokens unmeasurable:\n{e}")

    # Freshness: is this file still being written? Observed, not assumed.
    lag = None
    if stamps:
        last = max(stamps)
        try:
            t = _dt.datetime.fromisoformat(last.replace("Z", "+00:00"))
            lag = (_dt.datetime.now(_dt.timezone.utc) - t).total_seconds()
        except ValueError:
            pass

    if args.json:
        print(json.dumps({
            "measured_real": real_measured, "measured_real_method": real_method,
            "measured_tape_cl100k": measured, "by_type": by_type,
            "records": records, "lag_seconds": lag,
            "fill": fill,
            "fill_unit": ("REAL Claude tokens, resident context — Anthropic's own "
                          "total_input_tokens (cache_read + cache_creation + input). "
                          "SEPARATE OBJECT from the throughput headline; never converted."),
            "boot_half": (fill.get("boot") if fill.get("available") else None),
            "unit": (f"headline: REAL Claude tokens, method={real_method} — ONE call, "
                     "#82/#83 (c); breakdown: tape/cl100k (D1: UNVERIFIED proxy), SHAPE "
                     "ONLY, does NOT sum to the headline, NEVER scaled to match it"),
            "kind": "throughput, cumulative — NOT a fill reading",
        }, indent=2))
        return 0

    print("HOW HOT ARE WE")
    print(f"  transcript   {os.path.basename(path)}  ({records} records)")
    if lag is not None:
        state = "LIVE" if lag < 300 else f"STALE by {lag/60:.0f} min — treat with suspicion"
        print(f"  freshness    last record {lag:.0f}s behind now — {state}")
    # s186-D1 Q5 — the DECLARED EVENT, at the HEAD where an event belongs, not buried in the FILL
    # block where it lived as narration. Prints ONLY when the marker fired: zero surface otherwise.
    _ce = compaction_event(fill)
    if _ce:
        print(_ce)
    print()
    print(f"  MEASURED     {real_measured:>9,} {real_method}  (conversation half, ONE call — the headline)")
    print()
    print(f"  BREAKDOWN    {measured:>9,} tape  (cl100k, SHAPE ONLY — per-type proportion, not a magnitude)")
    for k in sorted(by_type, key=lambda k: -by_type[k]):
        print(f"    {k:<10} {by_type[k]:>9,}")
    print("               ⛔ different UNIT from the headline above — does NOT sum to it, and")
    print("               is NEVER scaled/converted to match it (converting is #54's defect).")
    # ── FILL — the block this module went 31 sessions without. ENACTED #91. ──
    if not fill.get("available"):
        print(f"  FILL         {'UNAVAILABLE':>9}  ⛔ {fill.get('reason')}")
    else:
        print(f"  FILL         {fill['now']:>9,} real  RESIDENT CONTEXT — what the last call actually sent")
        print(f"    boot       {fill['boot']:>9,} real  first turn = system + tools + MEMORY.md + CLAUDE.md")
        print(f"    peak       {fill['peak']:>9,} real  across {fill['turns']} turns")
        print("               ⛔ ds-025 item 1's TOTAL is MEASURED, not unmeasurable — the")
        print("               `usage` field covers tools + system + messages (Anthropic, quoted")
        print("               in the #59-era brief). What stays dark is the DECOMPOSITION of")
        print("               boot into its sub-parts. Say which of the two you mean.")
        # ⛔ the compaction narration that used to live here is now the DECLARED EVENT printed at
        # the head of this report (s186-D1 Q5, `compaction_event()`). It is not printed twice.
        if fill["drops"]:
            print(f"               ⛔ {len(fill['drops'])} turn(s) DROPPED >10% — compaction or a broken"
                  f" read, at turn index {fill['drops'][:5]}.")
        if fill["skipped_synthetic"]:
            print(f"               ⚠ {fill['skipped_synthetic']} synthetic/zero-usage record(s) SKIPPED (#59).")
        print(f"               ⚠ cache continuity {fill['continuous']}/{fill['continuity_of']}"
              " — reported, not asserted; a cache re-creation breaks it legitimately.")
        print("               ⚠ LATE BY ONE STEP (Dave, #59): this is the prompt of the call")
        print("               that ALREADY RAN. It is a FLOOR. Price the NEXT turn, not the last.")
    print()
    # ── REHEARSAL (#92): the wrap gate, run HERE where a fix is cheap. #91-F5 measured the
    # wrap's binding cost as the gate-failure remediation loop, paid at peak fill. This is the
    # same gate, same seam (run(rehearse=True)), terse output, logged to _REHEARSAL-LOG.jsonl.
    # [[instrument-without-a-consumer]] — this call IS the consumer; without it the rehearsal
    # is a mode nobody runs and #92 built nothing.
    if not args.no_rehearse:
        print("  REHEARSAL   wrap gate, early (same checks as --wrap; #92):")
        try:
            import _capture_gate as _cg
            _cg.run(rehearse=True)
        except Exception as e:  # noqa: BLE001 — loud + named, never silent, never fatal here
            print(f"    ⛔ REHEARSAL DID NOT RUN ({type(e).__name__}: {e}) — the wrap gate's "
                  f"state is UNKNOWN, not green. Run `python3 knowledge/_capture_gate.py "
                  f"--rehearse` by hand.")
        print()
    # ── SEAM — THE PLAN BLOCK (B2, brief §2), WIRED HERE AND ONLY HERE. Same seam as the
    # rehearsal above and for the same reason: the check-in IS the lane seam, so the block is
    # regenerated where the seam already is, never carried into it. Printed for use in a
    # sub-brief / handoff, and GRADED in the same run so a bad seam BLOCKS instead of
    # narrating. ⛔ Do not add a `--seam` flag: an opt-in seam check is one nobody runs.
    seam_rc = 0
    if not args.no_block:
        # ⚠ `repo=REPO` PASSED EXPLICITLY, not left to the default. Python binds a default at
        # DEFINITION time, so `seam_block(path, fill)` reads the REPO this module was imported
        # with and is blind to a test that repoints it — the first drive of this seam end-to-end
        # measured a corrupted temp tree and reported the LIVE one green
        # [[attribute-the-diff]]: a measurement whose SUBJECT is not what you think it is.
        ok, block, reasons, _notes = seam_block(path, fill, repo=REPO, max_age=args.max_age)
        print("  SEAM        plan block (B2) — REGENERATED from state, graded against it:")
        for ln in block.splitlines():
            print(f"    {ln}")
        if ok:
            print("    ✅ SEAM CLEAR — provenance complete, integrity digest matches, every "
                  "field re-derives, no UNKNOWN.")
        else:
            seam_rc = 3
            print(f"    ⛔ SEAM BLOCKED — {len(reasons)} failing leg(s). This block must NOT be "
                  f"carried into a brief or a handoff:")
            for i, r in enumerate(reasons, 1):
                print(f"    {i}. {r}")
            print("    ⇒ Fix the STATE, then re-run the check-in. Never repair the block "
                  "(P1/P2, GENERATE-NEVER-INHERIT). Exit code 3.")
        print()
    # ── B3 GRADE ALERTS — the ONE bounded mitigation of s179-D1, WIRED HERE. ──────────────
    # ⛔ WHY HERE. The ruling puts the alerts on the BOOT CHAIN-READ. This function IS that
    # read's seam: `_checkin.py` is already law at the opener ([[checkin-is-mandatory]]) and
    # already reads _CHAIN.md for the block above, so the alert rides a read that happens
    # anyway and adds NO boot-floor bytes — the sidecar is never in MEMORY.md, which is the
    # whole point of Option B. It is deliberately NOT a flag: an opt-in alert is one nobody
    # sees, and this surface only earns its keep if it is UNPROMPTED.
    # ⚠ NOT RULED PERMANENT. s179-D1 requires the surface's REAL token cost measured first;
    # that is why every printing logs a row to _GRADE-DECISIONS.jsonl with the measured
    # figure. The row is the evidence the B3 review is owed, and it cannot exist unless this
    # runs. A grade row is NEVER written from here — whether a grade CHANGED a retrieval
    # decision is a human statement (`_gardener.py --grade-decision`), never an inference.
    if not args.no_grades:
        try:
            import _gardener as _gd
            _gdoc = _gd.load_grades(os.path.join(REPO, "notes/_dream/_MEMORY-GRADES.json"))
            if not _gdoc:
                print("  GRADES      ⛔ NO SIDECAR — notes/_dream/_MEMORY-GRADES.json absent. "
                      "Grades are UNKNOWN, not clean. Run `python3 knowledge/_gardener.py "
                      "--refresh`.")
            else:
                _alerts = _gd.render_grade_alerts(_gdoc)
                _head = (f"  GRADES      B3 sidecar, refreshed {_gdoc.get('refreshed_at')} — "
                         f"starred/blocked entries ONLY (s179-D1; schema PROVISIONAL):")
                # ⚠ WHAT IS MEASURED: the header + the alert lines — the whole thing a reader
                # actually consumes. NOT measured: the `⚠ SURFACE COST …` line below, because
                # it quotes the figure it would be part of (self-reference), and because it is
                # the INSTRUMENT, not the surface. Its own cost is stated in the runbook and
                # it goes away the moment Dave rules the surface permanent.
                _surface = "\n".join([_head] + _alerts)
                try:
                    _cost, _method = (gauge.count(_surface) if _surface else (0, "empty"))
                except gauge.MeasurementRefused as _e:
                    _cost, _method = (None, f"REFUSED: {_e.__class__.__name__}")
                print(_head)
                if _alerts:
                    for _ln in _alerts:
                        print(f"    {_ln}")
                else:
                    print("    ✅ no starred/blocked entry is STALE — an honest silence: "
                          f"{_gdoc.get('counts', {})} across {_gdoc.get('hooks_seen')} hooks.")
                print(f"    ⚠ SURFACE COST {(f'{_cost:,} real' if _cost is not None else 'UNMEASURED')}"
                      f" ({_method}) for {len(_alerts)} line(s) — MEASURED, not ruled. The fork "
                      f"returns to Dave with this number after one full dream-pass cycle.")
                try:
                    _gd.log_grade_event(REPO, {
                        "kind": "alert", "lines": len(_alerts), "chars": len(_surface),
                        "tokens": _cost, "method": _method,
                        "counts": _gdoc.get("counts", {}),
                        "refreshed_at": _gdoc.get("refreshed_at"),
                        "listed": [a for a in _alerts if a.startswith("⛔")]})
                except Exception as _e:   # noqa: BLE001 — loud + named, never silent
                    print(f"    ⛔ ALERT ROW NOT LOGGED ({type(_e).__name__}: {_e}) — this boot "
                          f"contributes NOTHING to the B3 numbers. Declared, not hidden.")
        except Exception as _e:  # noqa: BLE001 — a fence bit or a broken sidecar, LOUD + NAMED
            print(f"    ⛔ GRADE ALERTS DID NOT RUN ({type(_e).__name__}: "
                  f"{' '.join(str(_e).split())[:220]}) — grades are UNKNOWN, not green.")
        print()
    # ── DREAM-PASS SEAM — #185: a pass that ran + was enacted must be VISIBLE at boot. ─────
    # ⛔ WHY. On 2026-08-16 pass 8 fired 06:10Z, Dave promoted P1–P5 (s183-D1), the enact
    # commit landed 13:11 — and the opener reported "I haven't verified it fired" because no
    # boot surface carried the event. The sidecar alert reports grade COUNTS only; the pass
    # itself had no consumer ([[instrument-without-a-consumer]]). This line is that consumer.
    # Evidence = newest proposals FILE (mtime + its own header) and the GIT LOG — never a
    # banner ([[ritual-output-is-not-evidence]]). Fails LOUD and NAMED, never silent.
    try:
        import glob as _glob
        import subprocess as _sp
        _props = sorted(_glob.glob(os.path.join(REPO, "notes/_dream/[0-9]*-proposals*.md")),
                        key=os.path.getmtime)
        if not _props:
            print("  DREAM       ⛔ NO PROPOSALS FILE FOUND (notes/_dream/) — pass history is "
                  "UNKNOWN, not clean.")
        else:
            _pf = _props[-1]
            _pmt = _dt.datetime.fromtimestamp(os.path.getmtime(_pf))
            _age_h = (_dt.datetime.now() - _pmt).total_seconds() / 3600.0
            with open(_pf, encoding="utf-8") as _fh:
                _first = _fh.readline().strip()  # e.g. "# Dream pass 8 — floated proposals"
            _pm = re.search(r"[Dd]ream pass (\d+)", _first)
            _pn = _pm.group(1) if _pm else "?"
            # enactment: search the log SINCE the pass file's day for a commit naming this pass
            _since = _pmt.strftime("%Y-%m-%d 00:00")
            _out = _sp.run(["git", "-C", REPO, "log", "--since", _since, "-i", "-E",
                            "--grep", rf"(enact|promot).*(dream )?pass {_pn}|dream pass {_pn}.*(enact|promot)",
                            "--format=%h %ad %s", "--date=format:%H:%M"],
                           capture_output=True, text=True, check=True).stdout.strip()
            _flag = "⚠ " if _age_h <= 48 else ""
            _line1 = (f"  DREAM       {_flag}newest = pass {_pn}, file {os.path.basename(_pf)} "
                      f"(mtime {_pmt:%Y-%m-%d %H:%M}, {_age_h:.0f}h ago)")
            print(_line1)
            if _out:
                _c = _out.splitlines()[0]
                print(f"    ✅ ENACT COMMIT EXISTS — `{_c}` (git log, --grep on pass {_pn}; "
                      f"read the proposals file for what was promoted vs still floated).")
            elif _age_h <= 48:
                print(f"    ⚠ NO enact/promote commit names pass {_pn} since {_since} (probe: "
                      f"git log --grep). FRESH PASS, UNRULED OR UNENACTED — proposals await "
                      f"Dave, or enactment used words this probe misses. READ THE FILE.")
            else:
                print(f"    · no enact commit matched since {_since} — pass is >48h old; "
                      f"consult notes/_MEMENTO-DECISIONS.md, not this probe.")
    except Exception as _e:  # noqa: BLE001 — loud + named, never silent
        print(f"  DREAM       ⛔ SEAM DID NOT RUN ({type(_e).__name__}: "
              f"{' '.join(str(_e).split())[:220]}) — pass status UNKNOWN, not green.")
    print()
    if args.window:
        if fill.get("available"):
            print(f"  ratio        {fill['now'] / args.window:.0%} of the {args.window:,} you passed"
                  "  — ON FILL, the comparable unit")
            print("               ★ THIS is the ratio to compare against a stop line. The stop")
            print("               line is in FILL; comparing THROUGHPUT to it is a unit error and")
            print("               it was made every session from #59 to #90.")
        print(f"  ratio (thru) {real_measured / args.window:.0%} of {args.window:,}  ({real_method})"
              " — ⛔ NOT comparable to a fill budget")
        print("               ⚠ that denominator is YOURS, not observed. The absolute")
        print("               figure above is the only honest one (D2 c).")
    else:
        print("  ratio        NONE — no denominator named. Pass --window to get one.")
    print()
    print(f"  ⚠ UNIT  headline = REAL Claude tokens ({real_method}), ONE call — #82's unit,")
    print("          wired here at #83 (c). Breakdown = tape/cl100k (tiktoken); D1 rules that")
    print("          an UNVERIFIED proxy, kept for SHAPE only, never summed/scaled to the")
    print("          headline above.")
    print("  ⚠ KIND  TWO OBJECTS, REPORTED SEPARATELY, NEVER SUMMED OR CONVERTED:")
    print("          headline = THROUGHPUT (cumulative log) · FILL = RESIDENT CONTEXT (`usage`).")
    print("          A stop line is in FILL. Compare FILL to it. #59→#90 compared the other one.")
    if seam_rc:
        print()
        print("  ⛔ EXIT 3 — the SEAM BLOCK above was REJECTED. The reading is still honest; the")
        print("     SEAM is not. Fix the state named in the failing leg before opening the next")
        print("     lane or briefing a sub (brief §2 P1/P2).")
    return seam_rc


if __name__ == "__main__":
    raise SystemExit(main())
