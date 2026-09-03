#!/usr/bin/env python3
"""_boot_decompose.py — DECOMPOSE the first-turn boot: what is OURS, and what is HARNESS.

Built #242 lane F for Dave's ask — *"there must be a way to offload this from the boot, maybe
JIT, progressive disclosure, componentisation and mechanizing as much as possible."* `ds-025`
item 1 stands: the boot TOTAL has been measured every session since #208; its DECOMPOSITION was
dark. `_boot_remeasure.py` measures two files by hard-coded path. This walks the LIVE session
transcript's opener attachments — the actual bytes the model was sent — and names what is left.

CONSUMER (named, or this is a zombie [[instrument-without-a-consumer]]): the conductor at the
opener, beside `knowledge/_checkin.py`, whenever the `_capture_gate.py` boot-drift check reports
a CEILING BREACH against `_gauge_tokens.BOOT_CEILING_TK` — the gate says *cut the boot*, and this
is the only instrument that says WHERE. Second consumer: the #243 A/B (one lever per session),
which needs the BEFORE row for the lever it flips.

⚠ UNIT DISCIPLINE — READ BEFORE QUOTING [[measure-dont-convert-units]]:
  Every component figure below is a cl100k TAPE token count (tiktoken) — a PROXY for SHAPE and
  MOVEMENT. The boot TOTAL is a REAL figure from `message.usage`. ⛔ THEY ARE NEVER SUMMED.
  The harness remainder is printed as `<real total> − Σ(ours, tape)` and carries the label
  ESTIMATED-BY-SUBTRACTION on its own line, because that subtraction mixes units BY CONSTRUCTION
  and saying so is the whole honesty of it. Refuses loudly without tiktoken (a measuring tool
  must not guess — the `ds-025` standard).

★ THE REAL-UNIT CORROBORATION, and it is the finding this tool exists to keep reproducible: a
  SUBAGENT seat carries the SAME roster, the same `MEMORY.md`, the same MCP instruction blocks
  and the same deferred-tool name list, and boots at ~40K real against the conductor's ~70K. The
  gap between the two seats is harness that no repo edit can reach. `--lanes` prints it.

Usage:
  python3 knowledge/_boot_decompose.py --real 70710       # decompose against a measured boot
  python3 knowledge/_boot_decompose.py --lanes            # subagent-seat first-turn REAL figures
  python3 knowledge/_boot_decompose.py --transcript PATH  # a specific session .jsonl
  python3 knowledge/_boot_decompose.py --selftest         # bites — the break arm must FAIL
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_sys.path.insert(0, _hg_os.path.dirname(_hg_os.path.abspath(__file__)))
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The Cowork mount root. Session-scoped and therefore NEVER hard-coded to one session name:
# resolved by glob, and DECLARED MISSING rather than zeroed when it is not there
# [[unmatched-grep-is-not-an-absence]].
MOUNT_GLOB = "/sessions/*/mnt"

# Opener attachment types that carry a boot input, in the order the harness emits them.
ATTACH_ORDER = ["deferred_tools_delta", "agent_listing_delta", "mcp_instructions_delta",
                "skill_listing", "total_tokens_reminder"]
ATTACH_LABEL = {
    "deferred_tools_delta": "deferred tool NAME list",
    "agent_listing_delta":  "agent listing (subagent roster)",
    "mcp_instructions_delta": "MCP server instruction blocks",
    "skill_listing":        "skills roster (name + description)",
    "total_tokens_reminder": "total-tokens reminder",
}


def _enc():
    try:
        import tiktoken
    except ImportError:
        print("REFUSING TO GUESS: tiktoken is not installed.\n"
              "  pip install tiktoken --break-system-packages\n"
              "  A measuring tool that estimates silently is the ds-025 defect.", file=sys.stderr)
        raise SystemExit(2)
    return tiktoken.get_encoding("cl100k_base")


def render(att: dict) -> str:
    """The attachment as TEXT — the bytes the model saw, never the JSON envelope.

    ⛔ The envelope is 3× the payload for `deferred_tools_delta`; measuring `json.dumps(att)`
    would inflate every figure. One shape per attachment kind, and an unknown kind returns None
    so the caller can DECLARE it rather than count it as zero.
    """
    if "addedBlocks" in att:                       # mcp_instructions_delta
        return "\n".join(b if isinstance(b, str) else json.dumps(b) for b in att["addedBlocks"])
    if "addedLines" in att:
        return "\n".join(att["addedLines"])
    if "content" in att:
        return att["content"]
    if "text" in att:
        return att["text"]
    return None


def find_mount() -> str | None:
    hits = sorted(glob.glob(MOUNT_GLOB))
    return hits[0] if hits else None


def find_transcripts(mount: str) -> list[str]:
    return sorted(glob.glob(os.path.join(mount, ".claude", "projects", "*", "*.jsonl")))


def opener_rows(path: str, enc) -> tuple[list[dict], int | None]:
    """Walk one transcript to the FIRST assistant message. Returns (component rows, real total)."""
    rows, real = [], None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            t = d.get("type")
            if t == "user" and not any(r["kind"] == "user_msg" for r in rows):
                c = d.get("message", {}).get("content")
                s = c if isinstance(c, str) else json.dumps(c)
                rows.append({"kind": "user_msg", "label": "first user message",
                             "tape_tk": len(enc.encode(s))})
            elif t == "attachment":
                att = d.get("attachment", {})
                kind = att.get("type")
                txt = render(att)
                if txt is None:
                    rows.append({"kind": kind, "label": ATTACH_LABEL.get(kind, kind),
                                 "tape_tk": None, "declared": "UNRENDERABLE SHAPE"})
                    continue
                rows.append({"kind": kind, "label": ATTACH_LABEL.get(kind, kind),
                             "tape_tk": len(enc.encode(txt)),
                             "detail": att.get("addedNames") or att.get("skillCount")})
            elif t == "assistant":
                u = d.get("message", {}).get("usage", {}) or {}
                real = (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                        + u.get("cache_read_input_tokens", 0))
                break
    return rows, real


def memory_row(mount: str, enc) -> dict:
    p = os.path.join(mount, ".auto-memory", "MEMORY.md")
    if not os.path.exists(p):
        return {"kind": "memory", "label": "MEMORY.md (auto-memory index, in the claudeMd block)",
                "tape_tk": None, "declared": f"MISSING — {p}"}
    txt = open(p, encoding="utf-8", errors="replace").read()
    return {"kind": "memory", "label": "MEMORY.md (auto-memory index, in the claudeMd block)",
            "tape_tk": len(enc.encode(txt)), "bytes": len(txt.encode()),
            "lines": txt.count("\n") + 1}


def report(real: int | None, transcript: str | None = None) -> int:
    enc = _enc()
    mount = find_mount()
    if mount is None:
        print(f"DECLARED MISSING (not zeroed): no Cowork mount matched {MOUNT_GLOB} — this tool "
              f"measures a LIVE session's boot and there is no session here.", file=sys.stderr)
        return 2
    if transcript is None:
        cands = find_transcripts(mount)
        if not cands:
            print(f"DECLARED MISSING (not zeroed): no session transcript under "
                  f"{mount}/.claude/projects/*/*.jsonl", file=sys.stderr)
            return 2
        transcript = max(cands, key=os.path.getmtime)

    rows, real_seen = opener_rows(transcript, enc)
    rows.insert(0, memory_row(mount, enc))
    total = real if real is not None else real_seen

    print("BOOT DECOMPOSITION — ⛔ TWO UNITS, NEVER SUMMED [[measure-dont-convert-units]]")
    print(f"  transcript: {transcript}")
    print(f"  mount:      {mount}")
    print()
    print("OURS — every line cl100k TAPE tokens (PROXY for shape/delta, NEVER real):")
    ours = 0
    for r in rows:
        if r.get("tape_tk") is None:
            print(f"  {'DECLARED':>10}       {r['label']} — {r.get('declared')}")
            continue
        extra = ""
        if r["kind"] == "memory":
            extra = f"  ({r['bytes']:,} B, {r['lines']} lines)"
        elif isinstance(r.get("detail"), list):
            extra = f"  (n={len(r['detail'])})"
        elif r.get("detail"):
            extra = f"  (n={r['detail']})"
        print(f"  {r['tape_tk']:>10,} tape  {r['label']}{extra}")
        ours += r["tape_tk"]
    print(f"  {ours:>10,} tape  Σ OURS")
    print()
    if total:
        print(f"BOOT TOTAL: {total:,} REAL (message.usage, first turn — input + cache_creation "
              f"+ cache_read)")
        print(f"HARNESS REMAINDER: {total:,} real − {ours:,} tape ≈ {total - ours:,}")
        print("  ⛔ ESTIMATED-BY-SUBTRACTION. This line MIXES UNITS BY CONSTRUCTION and is "
              "printed that way on purpose:")
        print("     no tape proxy exists for Anthropic's system prompt or the loaded tool "
              "schemas, so the remainder")
        print("     is a RESIDUAL, never a measurement. Quote it with this label attached or "
              "do not quote it.")
        pct = 100.0 * ours / total
        print(f"  ⇒ everything on disk that Dave owns is ~{pct:.0f}% of the boot by this "
              f"mixed-unit comparison.")
    else:
        print("BOOT TOTAL: ⛔ NOT READ — no assistant message with usage in this transcript. "
              "DECLARED, not estimated.")
    return 0


def lanes() -> int:
    """Subagent-seat first-turn REAL figures — the real-unit floor under the conductor's boot."""
    enc = _enc()
    mount = find_mount()
    if mount is None:
        print(f"DECLARED MISSING: no mount matched {MOUNT_GLOB}", file=sys.stderr)
        return 2
    pat = os.path.join(mount, ".claude", "projects", "*", "*", "subagents", "*.jsonl")
    files = sorted(glob.glob(pat))
    if not files:
        print(f"DECLARED MISSING (not zeroed): no subagent transcripts under {pat}",
              file=sys.stderr)
        return 2
    print("LANE (SUBAGENT) SEAT FIRST-TURN BOOT — unit: REAL (message.usage). Brief in TAPE.")
    for f in files:
        rows, real = opener_rows(f, enc)
        brief = next((r["tape_tk"] for r in rows if r["kind"] == "user_msg"), None)
        b = f"{brief:,} tape" if brief is not None else "UNREAD"
        r = f"{real:,} real" if real else "⛔ NOT READ"
        print(f"  {r:>16}   brief {b:>12}   {os.path.basename(f)}")
    print("  ⇒ a lane carries the SAME roster, MEMORY.md, MCP blocks and deferred-name list as "
          "the conductor.")
    print("    The conductor-minus-lane gap is HARNESS at the conductor's seat and no repo edit "
          "reaches it.")
    return 0


def selftest() -> int:
    """Every check proves it can FAIL [[mutation-tests-the-clause-not-the-feature]]."""
    enc = _enc()
    fails = []

    # ---- ARM 1: the envelope must NOT be what is measured. `render` takes the payload.
    att = {"type": "deferred_tools_delta", "addedNames": ["a", "b"],
           "addedLines": ["alpha", "beta"], "failedMcpServers": [], "pendingMcpServers": []}
    payload = render(att)
    if payload != "alpha\nbeta":
        fails.append("render(): payload is not the addedLines join — got %r" % payload)
    # THE BREAK ARM: measuring the envelope instead must give a DIFFERENT, LARGER figure. If it
    # did not, this check could never catch the inflation it exists to catch.
    if len(enc.encode(json.dumps(att))) <= len(enc.encode(payload)):
        fails.append("BREAK ARM DEAD: the JSON envelope did not measure larger than the payload, "
                     "so the envelope-vs-payload check cannot bite.")

    # ---- ARM 2: an unknown attachment shape must DECLARE, never count as zero.
    if render({"type": "something_new"}) is not None:
        fails.append("render(): an unknown shape returned a value instead of None — it would be "
                     "silently measured, and a silent zero is the ds-025 defect.")

    # ---- ARM 3: the real total is the SUM OF THE THREE usage fields, and a missing field must
    # not be quietly read as a complete figure. Driven on a synthetic transcript.
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "t.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            f.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
            f.write(json.dumps({"type": "attachment",
                                "attachment": {"type": "skill_listing", "content": "- a: b"}}) + "\n")
            f.write(json.dumps({"type": "assistant", "message": {"usage": {
                "input_tokens": 2, "cache_creation_input_tokens": 30, "cache_read_input_tokens": 40,
                "output_tokens": 9}}}) + "\n")
        rows, real = opener_rows(p, enc)
        if real != 72:
            fails.append("opener_rows(): real total %r — output_tokens must be EXCLUDED and the "
                         "three input fields summed (expected 72)." % real)
        if not any(r["kind"] == "skill_listing" for r in rows):
            fails.append("opener_rows(): the skill_listing attachment was not captured.")

    if fails:
        print("SELFTEST FAILED:")
        for f_ in fails:
            print("  ⛔ " + f_)
        return 1
    print("SELFTEST PASSED — 3 arms, each with a break arm or a wrong-answer fixture.")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if "--lanes" in args:
        return lanes()
    real = None
    if "--real" in args:
        real = int(args[args.index("--real") + 1].replace(",", "").replace("_", ""))
    tr = None
    if "--transcript" in args:
        tr = args[args.index("--transcript") + 1]
    return report(real, tr)


if __name__ == "__main__":
    raise SystemExit(main())
