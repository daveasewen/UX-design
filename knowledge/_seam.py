#!/usr/bin/env python3
"""_seam.py — THE LANE-SEAM CHECK. Four blocks, run before every lane is cut and after every
lane lands. Born #283 on Dave's two words at the opener; the fourth block added #285.

WHY (measured, three sessions). #277 crossed the 256,000 hard line under pressure. #281 read
the gauge every turn and overruled it every turn. #282 did not read it at all between two
lanes and breached by 81,559 — the largest on record. The arc points AWAY from the instrument.
The check-in exists and is law at the OPENER; nothing made it law at the SEAM, which is where
the lanes are cut and where the fill actually moves. Dave, #283 opener, on "I'll read it at
every lane seam and say the number in chat": *"can we do this in every session"*. On clearing
scratch before a lane at 99% disk: *"good, maybe we make this a regular check- more mechanical"*.

WHAT IT PRINTS — FIVE BLOCKS, quotable verbatim in chat, nothing else:
  FILL  <now> real / <turns> turns · boot <boot> · <verdict against the three lines>
  DISK  /sessions <pct>% · <free> KB free · <verdict>
  INSEAT <tokens> cl100k own tool output since the last seam · <n> results · <verdict>
  SCRATCH <n> own entries · <removed|kept> · <kept-list>
  STANDING — the standing constraints, one per line, verbatim from `_standing.md`, then
            STANDING <n> lines · <tokens> cl100k

THE INSEAT BLOCK — THE DELEGATION LAPSE, AS A NUMBER (#286 lane T, building #285's move 2:
*"THE SEAM'S IN-SEAT ARM — `_seam.py` measures the conductor's own tool-output tokens since the
last seam and warns above a threshold"*). #284 MEASURED the lapse and could not make it
mechanical: the conductor did lane work in seat four times — the disk lever and its spec (~15K),
SIX runs of the commit script (~30K), two screenshots, the window research — while *"the one
delegated lane cost the conductor's window about 300 tokens"*. That is the whole argument, and
until now it existed only in prose, once, in a handoff. This arm reads the conductor's OWN
transcript (non-sidechain `tool_result` blocks), counts what has landed in the seat SINCE THE
LAST SEAM, and prints it every time the seam runs — so the lapse is a reading at every seam
rather than a finding at one wrap. It separates LANE RETURNS (the `Task`/`Agent` tool's own
results — the cost of delegating, which is the cheap half of #284's number) from everything
else, because the verdict is about work done IN SEAT, not about work routed out of it.
⚠ ADVISORY and ESTIMATE-ONLY: cl100k over the transcript's tool-result text, never a FILL claim
(FILL above is `_checkin.py`'s REAL reading). The threshold is PICKED, not ruled — see
INSEAT_WARN_TK. The since-marker is a gitignored state file; a missing or unmatched marker is
NAMED on the line ("since transcript start"), never silently treated as zero.

THE STANDING BLOCK — WHY IT IS LAST (#285, Dave: *"yes to the seam re-quoting the standing
constraints"*). Everything read at a session's opener — handoff, chain, check-in, ~80K — becomes
the MIDDLE of the context the moment work starts, and standing rules buried there drift out of
attention (lost-in-the-middle / U-shaped attention). The seam already runs before and after every
lane; re-quoting the constraints at its TAIL puts them at the RECENCY end every time. The block
prints LAST for exactly that reason and must not be moved above SCRATCH.
⚠ `knowledge/_standing.md` is a DRAFT until Dave approves it; the seam re-quotes, it never inscribes.
Missing file → `STANDING — knowledge/_standing.md ABSENT`, and the run still exits 0.

VERDICTS are the ruled lines, imported from `_gauge_tokens.py`, never restated here:
  STOP_LINE_TK 180,000 (s260-D2/s271-D1) → past it: "STOP LINE PASSED — wrap before the next lane"
  TOLERATED_TK 220,000 (s272-D93)       → past it: "OUTSIDE TOLERANCE — no more lanes"
  BUDGET_HARD  256,000                  → past it: "HARD LINE BREACHED"

SCRATCH is cleaned MECHANICALLY (the current user's own top-level entries under /tmp and
/var/tmp — the only litter anyone can ever remove, see `_gate_scratch_hygiene.py`), with ONE
keep-list: the git shim the mount needs (`/tmp/gitshim`), which ritual step 4c deleted at #282.
Anything on the keep-list is named as kept, never silently skipped.

⚠ ADVISORY, DELIBERATELY. It reports; it never blocks and never exits non-zero on a reading.
The obligation it carries is the CONDUCTOR'S: quote the FILL line in chat at every seam. A
seam that runs it and does not quote it has not run it. Promotion to blocking is Dave's.

Usage:
  python3 knowledge/_seam.py               # the five blocks; own scratch IS cleaned
  python3 knowledge/_seam.py --no-clean    # read only
  python3 knowledge/_seam.py --no-standing # suppress the STANDING block
  python3 knowledge/_seam.py --no-inseat   # suppress the INSEAT block (and do not move its marker)
  python3 knowledge/_seam.py --selftest    # verdict + keep-list + INSEAT + STANDING arms
"""
import os, sys, json, subprocess, argparse, glob

_d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import _gauge_tokens as G
import _gate_scratch_hygiene as H

KEEP = ("/tmp/gitshim",)          # the mount's git shim — deleted by 4c at #282, never again
DISK_WARN_PCT = 90                # same PICKED figure as _checkin.DISK_WARN_PCT
STANDING_PATH = os.path.join(_d, "_standing.md")
STANDING_TK_CEILING = 300         # the tail must stay a TAIL — the selftest holds the block here

# ── INSEAT constants ──────────────────────────────────────────────────────────────────────────
# ⚠ INSEAT_WARN_TK IS PICKED, NOT RULED — the same standing as DISK_WARN_PCT above, and it is
# named as picked so nobody reads it as Dave's line. WHAT PICKED IT, from #284's own measured
# numbers: the disk lever done in seat cost ~15,000 and the six commit runs ~30,000, while the
# one DELEGATED lane cost the conductor ~300. 10,000 sits between those two worlds — above any
# plausible reading-and-routing turn, below every in-seat lane #284 recorded. Promotion to a
# ruled line, or to blocking, is DAVE'S; this arm reports and never exits non-zero on a reading.
INSEAT_WARN_TK = 10_000
# The since-marker. `outputs/` is gitignored (see .gitignore "scratch render output"), so the
# state never dirties the tree at the commit seam. ⛔ NOT /tmp: THIS FILE'S OWN SCRATCH ARM
# deletes the user's top-level /tmp entries, so a marker there would be eaten by the next run.
INSEAT_STATE = os.path.join(os.path.dirname(_d), "outputs", "_seam-inseat-state.json")
# The conductor's transcript. Single-sourced from `_checkin.py` rather than re-spelled here.
LANE_TOOLS = ("Task", "Agent")    # a lane's RETURN is a delegation cost, not in-seat lane work


def fill_verdict(now: int) -> str:
    if now >= G.BUDGET_HARD:
        return f"⛔⛔ HARD LINE BREACHED (+{now - G.BUDGET_HARD:,} over {G.BUDGET_HARD:,})"
    if now >= G.TOLERATED_TK:
        return f"⛔ OUTSIDE TOLERANCE {G.TOLERATED_TK:,} — no more lanes, wrap"
    if now >= G.STOP_LINE_TK:
        return f"⚠ STOP LINE {G.STOP_LINE_TK:,} PASSED — tolerated to {G.TOLERATED_TK:,}; wrap before the next lane"
    return f"✅ {G.STOP_LINE_TK - now:,} real under the {G.STOP_LINE_TK:,} stop line"


def disk_verdict(pct: float) -> str:
    return "⛔ NEAR FULL — no render lane until cleared" if pct >= DISK_WARN_PCT else "✅"


def checkin_json(window: int) -> dict:
    r = subprocess.run([sys.executable, os.path.join(_d, "_checkin.py"), "--window", str(window),
                        "--no-block", "--no-rehearse", "--no-grades", "--json"],
                       capture_output=True, text=True, timeout=300)
    return json.loads(r.stdout)


def scratch_line(clean: bool) -> str:
    own = H.mine()
    kept = [p for p in own if p in KEEP]
    rm = [p for p in own if p not in KEEP]
    if not own:
        return "SCRATCH 0 own entries · clean"
    done = []
    if clean:
        done = [p for p in rm if H._rm(p)]
    parts = [f"SCRATCH {len(own)} own entr{'y' if len(own) == 1 else 'ies'}"]
    parts.append(f"removed {len(done)}/{len(rm)}" if clean else f"{len(rm)} removable (--no-clean)")
    if kept:
        parts.append("kept " + ", ".join(kept))
    return " · ".join(parts)


# ── THE IN-SEAT ARM (#286 lane T, #285's move 2) ─────────────────────────────────────────────
def _block_text(b) -> str:
    """The text of one `tool_result` content block, whatever shape the record carries.

    Deliberately total: a block whose content is a string, a list of {type:text} parts, or
    anything else all yield SOMETHING measurable. An unreadable shape is measured as its own
    JSON rather than silently dropped — a tool result that vanishes from the count is the one
    failure this arm cannot afford [[measuring-tool-must-not-guess]].
    """
    c = b.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        out = []
        for part in c:
            if isinstance(part, dict):
                out.append(part.get("text") or json.dumps(part, ensure_ascii=False))
            else:
                out.append(str(part))
        return "\n".join(out)
    return "" if c is None else json.dumps(c, ensure_ascii=False)


def inseat_scan(records: list, after_uuid=None) -> dict:
    """PURE. Given transcript records (newest last) and the previous seam's marker, return the
    conductor's own tool output since that marker, split from the lane returns.

    WHAT COUNTS AS IN SEAT: a `type == "user"` record with `isSidechain` false carrying
    `tool_result` blocks — i.e. output that landed in the CONDUCTOR'S window. A sidechain
    record is a subagent's own traffic and is never the conductor's cost.
    WHAT IS SPLIT OUT: results whose `tool_use_id` was issued by a `Task`/`Agent` call — a
    lane's RETURN. It is a real cost in the seat, but it is the cost of DELEGATING; the verdict
    is about the other number. Both are printed.
    ⚠ An `after_uuid` that is not in `records` means the transcript was replaced or compacted:
    the scan runs from the START and says so (`resumed=False`), never from a guessed offset.
    """
    ids = [r.get("uuid") for r in records]
    start = 0
    resumed = False
    if after_uuid and after_uuid in ids:
        start = ids.index(after_uuid) + 1
        resumed = True
    lane_ids = set()
    for r in records:                      # the whole file: a lane's tool_use may predate the marker
        msg = r.get("message") or {}
        for b in msg.get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in LANE_TOOLS:
                lane_ids.add(b.get("id"))
    own, lane = [], []
    for r in records[start:]:
        if r.get("type") != "user" or r.get("isSidechain"):
            continue
        msg = r.get("message") or {}
        for b in msg.get("content") or []:
            if not isinstance(b, dict) or b.get("type") != "tool_result":
                continue
            (lane if b.get("tool_use_id") in lane_ids else own).append(_block_text(b))
    return {"own": own, "lane": lane, "resumed": resumed,
            "last_uuid": ids[-1] if ids else None, "scanned": len(records) - start}


def inseat_tokens(texts: list):
    """cl100k count of the tool-result text this arm measured — the honest unit, NAMED on the
    line it prints on. ⚠ ESTIMATE-ONLY by declaration (ds-021 (C), registered in
    `_capture_gate.py::MEASURERS['_seam.py']`): it never calls `_gauge_tokens.count()` and is
    never a FILL claim. Unavailable tiktoken returns None and the line says `?`, never a guess.
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return sum(len(enc.encode(t)) for t in texts)
    except Exception:
        return None


def inseat_verdict(own_tk) -> str:
    if own_tk is None:
        return "? UNMEASURED — tiktoken unavailable; the cost is not guessed"
    if own_tk >= INSEAT_WARN_TK:
        return (f"⚠ {own_tk:,} in seat since the last seam, over the PICKED {INSEAT_WARN_TK:,} "
                f"— this is lane work being done in the seat (#284's lapse); ROUTE IT")
    return f"✅ under the PICKED {INSEAT_WARN_TK:,} in-seat line"


def _read_state(path: str = INSEAT_STATE) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def _write_state(transcript: str, last_uuid, path: str = INSEAT_STATE) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"transcript": transcript, "last_uuid": last_uuid}, fh)
    except Exception:
        pass                       # ADVISORY: a marker that cannot be written costs a reading, never a run


def find_transcript():
    """The conductor's transcript, by `_checkin.py`'s OWN glob (single-sourced, never re-spelled).
    Returns None rather than exiting — `_checkin.find_transcript` sys.exits, which is right for a
    check-in and wrong for an advisory block that must never take the seam down."""
    try:
        import _checkin
        hits = glob.glob(_checkin.TRANSCRIPT_GLOB)
    except Exception:
        return None
    return max(hits, key=os.path.getmtime) if hits else None


def inseat_block(state_path: str = INSEAT_STATE, move_marker: bool = True) -> str:
    """The INSEAT line as it prints. ADVISORY: every failure is NAMED, never fatal, never zero."""
    path = find_transcript()
    if not path:
        return ("INSEAT UNREADABLE — no transcript under _checkin.TRANSCRIPT_GLOB. This is an "
                "ABSENCE OF A MATCH, not a proven absence of in-seat work; NOT read as 0.")
    try:
        with open(path, encoding="utf-8") as fh:
            records = [json.loads(ln) for ln in fh if ln.strip()]
    except Exception as e:
        return f"INSEAT UNREADABLE — {type(e).__name__}: {e} (NOT read as 0)"
    st = _read_state(state_path)
    after = st.get("last_uuid") if st.get("transcript") == path else None
    r = inseat_scan(records, after)
    own_tk, lane_tk = inseat_tokens(r["own"]), inseat_tokens(r["lane"])
    if move_marker:
        _write_state(path, r["last_uuid"], state_path)
    since = "since the last seam" if r["resumed"] else "since transcript start (no prior seam marker)"
    own_s = "?" if own_tk is None else f"{own_tk:,}"
    lane_s = "?" if lane_tk is None else f"{lane_tk:,}"
    return (f"INSEAT {own_s} cl100k own tool output {since} · {len(r['own'])} results "
            f"(+{len(r['lane'])} lane returns, {lane_s} cl100k) · {inseat_verdict(own_tk)}")


def standing_lines(path: str = STANDING_PATH) -> list:
    """The constraint lines of `_standing.md`, verbatim — header and frontmatter skipped.

    THE PARSE, deliberately dumb: everything up to and including the first `---` rule is the
    header and is dropped; every non-empty line after it is a constraint, printed as written.
    A file with no rule prints every non-empty line that is not a `#` heading.
    """
    src = open(path, encoding="utf-8").read()
    body = src.split("\n---\n", 1)[1] if "\n---\n" in src else src
    return [ln.strip() for ln in body.splitlines()
            if ln.strip() and not ln.strip().startswith("#")]


def standing_tokens(lines: list) -> str:
    """cl100k count of the printed block — the honest unit, named on the line it prints on."""
    try:
        import tiktoken
        return f"{len(tiktoken.get_encoding('cl100k_base').encode(chr(10).join(lines))):,}"
    except Exception:
        return "?"


def standing_block(path: str = STANDING_PATH) -> list:
    """The block as it prints. ADVISORY: an absent or unreadable file is NAMED, never fatal."""
    rel = os.path.relpath(path, os.path.dirname(_d))
    if rel.startswith(".."):        # outside the repo — name it as given, never as a ../ climb
        rel = path
    try:
        lines = standing_lines(path)
    except FileNotFoundError:
        return [f"STANDING — {rel} ABSENT"]
    except Exception as e:
        return [f"STANDING — UNREADABLE {type(e).__name__}: {e}"]
    if not lines:
        return [f"STANDING — {rel} EMPTY"]
    return ["STANDING"] + lines + [f"STANDING {len(lines)} lines · {standing_tokens(lines)} cl100k"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--window", type=int, default=G.BUDGET_WORKING)
    ap.add_argument("--no-clean", action="store_true")
    ap.add_argument("--no-standing", action="store_true")
    ap.add_argument("--no-inseat", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        d = checkin_json(a.window)
        f = d["fill"]
        if f.get("available"):
            print(f"FILL  {f['now']:,} real / {f['turns']} turns · boot {f['boot']:,} · "
                  f"{fill_verdict(f['now'])}")
        else:
            print("FILL  UNREADABLE — the check-in could not read the transcript; say so, do not guess")
        for r in d["disk"]:
            if r["mount"] == "/sessions":
                if r["available"]:
                    print(f"DISK  /sessions {r['pct']:.1f}% · {r['free_kb']:,} KB free · "
                          f"{disk_verdict(r['pct'])}")
                else:
                    print(f"DISK  /sessions UNREADABLE — {r['reason']}")
    except Exception as e:          # the reading failed — named, never defaulted
        print(f"FILL  UNREADABLE — {type(e).__name__}: {e}")
    if not a.no_inseat:            # BEFORE scratch, and never after STANDING (see the docstring)
        print(inseat_block())
    print(scratch_line(clean=not a.no_clean))
    if not a.no_standing:          # LAST, always — the recency end is the whole point
        print("\n".join(standing_block()))
    return 0


def selftest() -> int:
    fails = []
    arms = [(0, "under"), (G.STOP_LINE_TK, "STOP LINE"), (G.TOLERATED_TK, "OUTSIDE TOLERANCE"),
            (G.BUDGET_HARD, "HARD LINE BREACHED")]
    for now, expect in arms:
        v = fill_verdict(now)
        if expect not in v:
            fails.append(f"[fill {now}] expected '{expect}' in '{v}'")
    if "NEAR FULL" not in disk_verdict(DISK_WARN_PCT) or "NEAR FULL" in disk_verdict(DISK_WARN_PCT - 1):
        fails.append("[disk edge] warn threshold wrong")
    # keep-list arm: a path on KEEP is never in the removable set
    own = list(KEEP) + ["/tmp/x-litter"]
    rm = [p for p in own if p not in KEEP]
    if KEEP[0] in rm or "/tmp/x-litter" not in rm:
        fails.append(f"[keep-list] {rm}")
    # ── INSEAT arms (#286). Driven on HAND-BUILT records, in memory: no transcript, no state
    # file, no /tmp (this file's own scratch arm eats /tmp). Each arm names the class it bites.
    def rec(uuid, typ, content, side=False):
        return {"uuid": uuid, "type": typ, "isSidechain": side,
                "message": {"content": content}}
    recs = [
        rec("u1", "assistant", [{"type": "tool_use", "id": "t1", "name": "Bash"}]),
        rec("u2", "user", [{"type": "tool_result", "tool_use_id": "t1", "content": "IN SEAT"}]),
        rec("u3", "assistant", [{"type": "tool_use", "id": "t2", "name": "Task"}]),
        rec("u4", "user", [{"type": "tool_result", "tool_use_id": "t2", "content": "LANE RETURN"}]),
        rec("u5", "user", [{"type": "tool_result", "tool_use_id": "t3", "content": "SUBAGENT"}], side=True),
        rec("u6", "assistant", [{"type": "tool_use", "id": "t4", "name": "Read"}]),
        rec("u7", "user", [{"type": "tool_result", "tool_use_id": "t4",
                            "content": [{"type": "text", "text": "AFTER THE MARKER"}]}]),
    ]
    s_all = inseat_scan(recs, None)
    if s_all["own"] != ["IN SEAT", "AFTER THE MARKER"]:
        fails.append(f"[inseat own] wrong set: {s_all['own']}")
    if s_all["lane"] != ["LANE RETURN"]:
        fails.append(f"[inseat lane split] a Task result was not split out: {s_all['lane']}")
    if s_all["resumed"] or s_all["last_uuid"] != "u7":
        fails.append(f"[inseat marker] resumed={s_all['resumed']} last={s_all['last_uuid']}")
    s_since = inseat_scan(recs, "u4")          # the marker arm: only what landed AFTER it
    if s_since["own"] != ["AFTER THE MARKER"] or not s_since["resumed"]:
        fails.append(f"[inseat since-marker] {s_since['own']} resumed={s_since['resumed']}")
    s_lost = inseat_scan(recs, "nosuchuuid")   # a replaced/compacted transcript: from the START,
    if s_lost["resumed"] or len(s_lost["own"]) != 2:   # and SAID so — never a guessed offset
        fails.append(f"[inseat lost marker] resumed={s_lost['resumed']} own={len(s_lost['own'])}")
    if "⚠" not in inseat_verdict(INSEAT_WARN_TK) or "⚠" in inseat_verdict(INSEAT_WARN_TK - 1):
        fails.append("[inseat threshold] warn edge wrong")
    if "UNMEASURED" not in inseat_verdict(None):
        fails.append("[inseat unmeasured] a missing count must NAME itself, never read as 0")
    if inseat_tokens(["hello world"]) is None:
        fails.append("[inseat tiktoken] unavailable — the cost is UNMEASURED, never guessed")
    # STANDING arm: the block prints, it is the LAST block, and it stays a tail (≤ ceiling)
    blk = standing_block()
    if blk[0] != "STANDING" or len(blk) < 3:
        fails.append(f"[standing] block did not print: {blk[0]}")
    else:
        body = blk[1:-1]
        if not blk[-1].startswith(f"STANDING {len(body)} lines · "):
            fails.append(f"[standing] tally line wrong: {blk[-1]}")
        tk = blk[-1].split("·")[-1].strip().split()[0].replace(",", "")
        if tk == "?":
            fails.append("[standing] tiktoken unavailable — the cost is UNMEASURED, never guessed")
        elif int(tk) > STANDING_TK_CEILING:
            fails.append(f"[standing] {tk} cl100k over the {STANDING_TK_CEILING} ceiling")
    print("\n".join(fails) if fails else f"seam selftest: {len(arms) + 3 + 8} arms, all GREEN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
