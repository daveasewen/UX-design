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
import json
import os
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


def main() -> int:
    ap = argparse.ArgumentParser(description="On-demand context check-in.")
    ap.add_argument("path", nargs="?", help="Transcript jsonl (default: newest mounted).")
    ap.add_argument("--window", type=int, default=None,
                    help="Denominator for a ratio. NAMED in the output. Omitted = no ratio.")
    ap.add_argument("--json", action="store_true", help="Machine-readable.")
    args = ap.parse_args()

    path = find_transcript(args.path)
    fill = read_fill(path)   # FILL — read off `usage`, independent of every tape figure below
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
        if fill["compaction_records"]:
            print(f"               ⛔ {fill['compaction_records']} COMPACTION record(s) in `usage.iterations`"
                  " — fill is post-compaction.")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
