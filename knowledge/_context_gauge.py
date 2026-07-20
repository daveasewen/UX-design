#!/usr/bin/env python3
"""Context gauge — estimate how full the context window is from a transcript dump.

The accurate, OUT-OF-BAND half of the two-part gauge (the cheap always-on half is
the running tally the agent keeps in-head; see _RUNBOOK-context-gauge.md).

Why out-of-band: reading the live transcript into the main agent's context to measure
it burns the very fuel we're trying to conserve. So a throwaway Haiku subagent fetches
the transcript (session_info.read_transcript, full format), dumps it to a file, runs
THIS script, and reports back only three numbers. The bulk never touches the main
agent's window.

Usage:
    python3 _context_gauge.py transcript.txt
    session_info_dump | python3 _context_gauge.py            # reads stdin
    python3 _context_gauge.py transcript.txt --window 200000 --baseline 35000

Token estimate uses tiktoken (cl100k_base) if installed, else a chars/4 heuristic —
accuracy is +/-10-15%, which is all a fuel gauge needs.
"""
import sys
import argparse

# Defaults. Window = model context budget; baseline = the fixed cost already spent at
# session start in THIS environment (big system prompt + all deferred tool defs +
# MEMORY.md index) before any work happens. Measured, adjustable.
DEFAULT_WINDOW = 200_000
DEFAULT_BASELINE = 35_000  # this Cowork env starts heavy; re-measure if it changes

# Band edges as fraction of window. Green: work freely. Amber: get economical, pre-stage
# the handoff. Red: fire the trigger — run the capture ritual, open a fresh session.
AMBER_AT = 0.45
RED_AT = 0.60


def estimate_tokens(text: str) -> tuple[int, str]:
    """Return (token_estimate, method)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text)), "tiktoken/cl100k_base"
    except Exception:
        # 1 token ~= 4 chars of English prose. Good enough for a gauge.
        return len(text) // 4, "chars/4 heuristic"


def band(fraction: float) -> tuple[str, str]:
    if fraction >= RED_AT:
        return "RED", "Fire the trigger: run the capture ritual, open a fresh session."
    if fraction >= AMBER_AT:
        return "AMBER", "Get economical, pre-stage the handoff. Confirm before the next big read."
    return "GREEN", "Work freely."


def bar(fraction: float, width: int = 30) -> str:
    filled = min(width, int(round(fraction * width)))
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def main() -> int:
    ap = argparse.ArgumentParser(description="Estimate context-window fill from a transcript.")
    ap.add_argument("path", nargs="?", help="Transcript text file (omit to read stdin).")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    ap.add_argument("--baseline", type=int, default=DEFAULT_BASELINE,
                    help="Fixed tokens already spent at session start (system prompt etc.).")
    args = ap.parse_args()

    if args.path:
        with open(args.path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    transcript_tokens, method = estimate_tokens(text)
    total = transcript_tokens + args.baseline
    fraction = total / args.window
    label, action = band(fraction)

    print(f"Context gauge  {bar(fraction)}  {fraction*100:5.1f}%  {label}")
    print(f"  transcript ~{transcript_tokens:,} tok  + baseline {args.baseline:,}  "
          f"= ~{total:,} / {args.window:,}")
    print(f"  method: {method}")
    print(f"  -> {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
