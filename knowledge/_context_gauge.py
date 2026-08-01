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

Token measurement uses tiktoken (cl100k_base). ⛔ Without it this script REFUSES by
default rather than silently estimating — #74, the same defect class #59 fixed at the
chain seam (the silent chars/4 path under-reported by 414 tape and nothing said so;
[[measuring-tool-must-not-guess]]: observe don't infer, UNKNOWN never defaulted).
`--estimate` makes the chars/4 heuristic legal, and every output line it touches is
labelled ESTIMATED so the number cannot wear a measurement's clothes.
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
AMBER_AT = 0.50
RED_AT = 0.60


def estimate_tokens(text: str, allow_estimate: bool = False) -> tuple[int, str]:
    """Return (token_count, method). Refuses rather than silently estimating — #74.

    The old signature fell back to chars/4 on ANY exception, unlabelled at every call
    site, so a degraded sandbox produced a number indistinguishable from a measurement.
    Fail LOUD and NAMED (a-crash-is-not-a-fail): the refusal states the cause and the
    remedy; the estimate path exists only behind an explicit opt-in and says what it is.
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text)), "tiktoken/cl100k_base"
    except Exception as e:
        if allow_estimate:
            # 1 token ~= 4 chars of English prose. A gauge, not a measurement — labelled.
            return len(text) // 4, "chars/4 heuristic — ESTIMATED, not measured"
        raise SystemExit(
            "⛔ NOT CAPTURED — UNMEASURED. tiktoken is unavailable "
            f"({type(e).__name__}: {e}), and this gauge does not silently estimate (#74; "
            "the chars/4 path under-reported by 414 tape with nothing saying so). "
            "Remedy: pip install tiktoken --break-system-packages   — or re-run with "
            "--estimate to accept a chars/4 figure LABELLED as an estimate.")


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
    ap.add_argument("--estimate", action="store_true",
                    help="Accept a chars/4 ESTIMATE when tiktoken is unavailable (#74: "
                         "without this flag, a degraded measurer refuses loudly).")
    args = ap.parse_args()

    if args.path:
        with open(args.path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    transcript_tokens, method = estimate_tokens(text, allow_estimate=args.estimate)
    total = transcript_tokens + args.baseline
    fraction = total / args.window
    label, action = band(fraction)
    if "ESTIMATED" in method:
        label = f"{label} (ESTIMATED)"

    print(f"Context gauge  {bar(fraction)}  {fraction*100:5.1f}%  {label}")
    print(f"  transcript ~{transcript_tokens:,} tok  + baseline {args.baseline:,}  "
          f"= ~{total:,} / {args.window:,}")
    print(f"  method: {method}")
    print(f"  -> {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
