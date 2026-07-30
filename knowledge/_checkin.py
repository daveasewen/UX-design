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
  UNMEASURED the boot half — system prompt, tool schemas, MEMORY.md index.
             `ds-025` item 1 STANDS: no `system` record type exists in that
             file. It is printed as UNMEASURED and is NEVER defaulted to a
             constant [[feedback-measuring-tool-must-not-guess]].

  UNIT       `tape`, cl100k. ⚠ D1 rules cl100k UNVERIFIED against Claude's own
             tokenizer (p50k reads +8.6–11.1% on this corpus). Labelled on
             every line rather than silently assumed.

  KIND       THROUGHPUT, not fill. A cumulative log is not a resident-context
             reading [[measure-dont-convert-units]]. Compaction/eviction would
             break the equivalence and is not observable from here.

NO PERCENTAGE WITHOUT A NAMED DENOMINATOR — D2 (c). `DEFAULT_WINDOW = 200_000`
was a TRUE OBSERVED FIGURE GONE STALE (`e7f8b87`, matching a harness warning),
and 613,386 tape ran through a session against it. A ratio is printed only if
you pass `--window` and it is captioned with the number you passed.

FAILS LOUD without tiktoken. `_context_gauge.py` silently estimates and
under-reports by 414 tape; that defect is not reproduced here.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import json
import os
import sys

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


def main() -> int:
    ap = argparse.ArgumentParser(description="On-demand context check-in.")
    ap.add_argument("path", nargs="?", help="Transcript jsonl (default: newest mounted).")
    ap.add_argument("--window", type=int, default=None,
                    help="Denominator for a ratio. NAMED in the output. Omitted = no ratio.")
    ap.add_argument("--json", action="store_true", help="Machine-readable.")
    args = ap.parse_args()

    path = find_transcript(args.path)
    enc = encoder()

    by_type: dict[str, int] = {}
    records = 0
    stamps: list[str] = []
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
        by_type[kind] = by_type.get(kind, 0) + len(enc.encode(json.dumps(payload)))

    measured = sum(by_type.values())

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
            "measured_tape_cl100k": measured, "by_type": by_type,
            "records": records, "lag_seconds": lag,
            "boot_half": None, "unit": "tape/cl100k (D1: UNVERIFIED proxy)",
            "kind": "throughput, cumulative — NOT a fill reading",
        }, indent=2))
        return 0

    print("HOW HOT ARE WE")
    print(f"  transcript   {os.path.basename(path)}  ({records} records)")
    if lag is not None:
        state = "LIVE" if lag < 300 else f"STALE by {lag/60:.0f} min — treat with suspicion"
        print(f"  freshness    last record {lag:.0f}s behind now — {state}")
    print()
    print(f"  MEASURED     {measured:>9,} tape  (conversation half, cl100k)")
    for k in sorted(by_type, key=lambda k: -by_type[k]):
        print(f"    {k:<10} {by_type[k]:>9,}")
    print(f"  UNMEASURED   {'boot half':>9}  system prompt + tool schemas + MEMORY.md")
    print("               ds-025 item 1 STANDS — no `system` record exists here.")
    print("               NOT defaulted to a constant.")
    print()
    if args.window:
        print(f"  ratio        {measured / args.window:.0%} of the {args.window:,} you passed")
        print("               ⚠ that denominator is YOURS, not observed. The absolute")
        print("               figure above is the only honest one (D2 c).")
    else:
        print("  ratio        NONE — no denominator named. Pass --window to get one.")
    print()
    print("  ⚠ UNIT  tape/cl100k. D1 rules this an UNVERIFIED proxy for Claude's tokenizer.")
    print("  ⚠ KIND  THROUGHPUT, cumulative. Not a fill reading; compaction unobservable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
