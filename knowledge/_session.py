#!/usr/bin/env python3
"""_session.py — WHICH SESSION IS ACTUALLY RUNNING, and does every witness agree?

provenance: #89, built on the #87-D1 acceptance drill (Dave: N = 2 consecutive cold-session
passes — routing · reproducible counts · honest certification). status: built #89, UNPROVEN
until it has refused a real defect in a real session.

★ THE FINDING THIS FILE EXISTS FOR (#89, measured before a line was written):
   drill legs 2 (routing) and 3 (honest certification) are NOT two defects. They are ONE.
   Every artefact that names a session number is written BY the session it names, so the
   corpus is its own only witness — and `_gen_chain.py --check` compares the chain against
   GOOD-MORNING.md, which means a GM that is a session stale regenerates a chain that is
   CONSISTENTLY stale and `--check` goes GREEN. The two mechanisms agree with each other
   and are both wrong. `_gen_chain.build()` says so itself, in a comment, and has since #73:
       "it canNOT catch a skipped wrap — said plainly here because overselling a gate is
        how greens stop meaning anything."
   That named gap is what this module fills.

⛔ AND THE HARDER HALF, DECLARED RATHER THAN PAPERED OVER:
   at #86's boot, NO DISK WITNESS COULD HAVE CAUGHT IT. #85 booted, worked, and closed
   without writing anything; GM's banner (#84) and title (#85) stayed internally consistent;
   any commit #85 made was subject-stamped FROM that banner. Nothing on disk knew. Adding a
   cleverer cross-check between existing files could not have helped, because every one of
   them was silent for the same reason.
   ⇒ The fix is not a smarter check. It is a NEW WITNESS that is written at BOOT rather than
   at wrap: `_SESSIONS.jsonl`. A session that records its own arrival cannot later be
   invisible, and the NEXT session then boots into evidence that a predecessor opened and
   never closed. The witness has to exist before it can be consulted — which is why this is
   an append-only log and not another derived file.

★ WHAT IT STILL CANNOT DO, SAID HERE SO NO GREEN IS OVERSOLD:
   if a session never runs `record()` at all, it is invisible to this module exactly as #85
   was invisible to the corpus. This narrows the window from "always undetectable" to
   "undetectable only if the very first boot step is skipped" — a real improvement and NOT
   a closed hole. Priced, not claimed.

USAGE
    python3 knowledge/_session.py                      # verdict from disk (the boot check)
    python3 knowledge/_session.py --declare 89         # I am #89 — check every witness agrees
    python3 knowledge/_session.py --record boot --n 89 # append the arrival record
    python3 knowledge/_session.py --record wrap --n 89 # append the departure record
    python3 knowledge/_session.py --acknowledge "..."  # legal form for a REAL, declared gap
    python3 knowledge/_session.py --selftest           # mutation-tested bites, both directions

Exit codes: 0 = every witness agrees (or a gap is DECLARED) · 1 = REFUSED, cause named.
⚠ A DECLARED gap passes; a SILENT one fails. That asymmetry is the whole mechanism (#56).
"""

import json
import os
import re
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOG_NAME = "_SESSIONS.jsonl"

# ---------------------------------------------------------------- witnesses

HANDOFF_RE = re.compile(r"^_HANDOFF-(\d+)")
TITLE_RE = re.compile(r"\*\*TITLE THE NEXT CHAT →\*\*\s*`[^`\n]*?#(\d+)")
BANNER_RE = re.compile(r"##\s*★\s*LATEST\s*—[^\n]*?#(\d+)")


def log_path(repo=ROOT):
    return os.path.join(repo, "knowledge", LOG_NAME)


def read_log(repo=ROOT):
    """Every record, oldest first. A malformed line FAILS LOUD and NAMED — never skipped.

    ⚠ [[a-crash-is-not-a-fail]]: a parse helper that swallows a bad line turns a corrupted
    witness into a confident silence, which is the exact failure mode this module exists to
    end. Bad line ⇒ ValueError naming the line number.
    """
    p = log_path(repo)
    if not os.path.exists(p):
        return []
    out = []
    with open(p, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception as e:
                raise ValueError(f"{LOG_NAME}:{i} is not valid JSON ({e}) — the session witness "
                                 f"is CORRUPT and must not be read past. Repair the line; do "
                                 f"not delete it (an append-only log that loses records is not "
                                 f"a witness).")
            if not isinstance(rec, dict) or "n" not in rec or "event" not in rec:
                raise ValueError(f"{LOG_NAME}:{i} lacks 'n' or 'event' — refusing to guess.")
            out.append(rec)
    return out


def record(n, event, repo=ROOT, **extra):
    """Append one arrival/departure record. Append-only by construction: mode 'a'."""
    if event not in ("boot", "wrap"):
        raise ValueError(f"event must be 'boot' or 'wrap', got {event!r}")
    rec = {"n": int(n), "event": event,
           "ts": datetime.datetime.now().isoformat(timespec="seconds")}
    rec.update(extra)
    os.makedirs(os.path.dirname(log_path(repo)), exist_ok=True)
    with open(log_path(repo), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def witnesses(repo=ROOT):
    """Every independent claim on disk about which session is which.

    Returns a dict of witness -> value (None where a witness is absent, NEVER defaulted to a
    number — [[feedback-measuring-tool-must-not-guess]]: UNKNOWN is a value, 0 is a lie).
    """
    w = {"gm_banner": None, "gm_title": None, "handoff_max": None,
         "log_last_boot": None, "log_unwrapped": None}

    gm = os.path.join(repo, "GOOD-MORNING.md")
    if os.path.exists(gm):
        with open(gm, encoding="utf-8") as f:
            text = f.read()
        m = BANNER_RE.search(text)
        if m:
            w["gm_banner"] = int(m.group(1))
        m = TITLE_RE.search(text)
        if m:
            w["gm_title"] = int(m.group(1))

    ns = [int(m.group(1)) for m in
          (HANDOFF_RE.match(f) for f in os.listdir(repo)) if m]
    if ns:
        w["handoff_max"] = max(ns)

    recs = read_log(repo)
    boots = [r["n"] for r in recs if r["event"] == "boot"]
    wraps = {r["n"] for r in recs if r["event"] == "wrap"}
    if boots:
        w["log_last_boot"] = max(boots)
        unwrapped = sorted({n for n in boots if n not in wraps})
        w["log_unwrapped"] = unwrapped or None
    return w


# ---------------------------------------------------------------- verdict

def verdict(repo=ROOT, declared=None, acknowledge=None):
    """(exit_code, lines). Every refusal NAMES the disagreeing witnesses and their values.

    ⚠ The rules are ordered cheapest-cause-first so the printed reason is the ROOT one, not
    a downstream symptom.
    """
    lines, refusals = [], []
    try:
        w = witnesses(repo)
    except ValueError as e:
        return 1, [f"⛔ REFUSED — {e}"]

    lines.append("WITNESSES (None = absent, never defaulted)")
    for k in ("gm_banner", "gm_title", "handoff_max", "log_last_boot", "log_unwrapped"):
        lines.append(f"  {k:<16} {w[k]}")
    if declared is not None:
        lines.append(f"  {'declared':<16} {declared}")
    lines.append("")

    b, t, h, unwrapped = w["gm_banner"], w["gm_title"], w["handoff_max"], w["log_unwrapped"]

    # R1 — the stale-title arm, restated so this module stands alone. `_gen_chain` owns the
    # build-time copy; a boot check that has to import the generator to answer "which session
    # am I" has made the boot path more expensive, not safer.
    if b is not None and t is not None and t != b + 1:
        refusals.append(
            f"R1 STALE TITLE — ★ LATEST is #{b} so the next chat must be #{b + 1}, but the "
            f"TITLE line names #{t}. A wrap did not mint the next session's title.")

    # R2 — THE SKIPPED-WRAP ARM. This is the one no existing mechanism could reach: it is
    # answered by the boot log, not by any file the corpus generates about itself.
    if unwrapped:
        target = declared if declared is not None else t
        stranded = [n for n in unwrapped if target is None or n < target]
        if stranded:
            refusals.append(
                f"R2 SKIPPED WRAP — session(s) {stranded} recorded a boot and never recorded a "
                f"wrap, and you are opening #{target}. Their findings were never inscribed and "
                f"the chain you just read certifies the WRONG session. Wrap them, or declare "
                f"the gap: --acknowledge \"<why>\".")

    # R3 — a handoff numbered AT OR PAST the session the chain routes you to means the chain
    # has already been overtaken on disk. [[premise-ages-faster-than-rule]]
    if h is not None and t is not None and h >= t:
        refusals.append(
            f"R3 CHAIN OVERTAKEN — _HANDOFF-{h}-*.md exists but the chain routes you to #{t}. "
            f"A handoff outranks the chain; read it before trusting anything above.")

    # R4 — you said who you are and the boot path disagrees. Silent disagreement is the #86
    # failure; this makes it fatal.
    # ⛔ CAUGHT #89 BY RUNNING THIS AT THE SEAM IT GUARDS, AND THE FIRST CUT WAS WRONG:
    # `gm_title` names the NEXT session, so its meaning FLIPS across the wrap. BEFORE the wrap
    # the running session is `gm_title`; AFTER it, the running session is `gm_banner` and the
    # title has already been minted for its successor. The first cut compared against the title
    # only, so it REFUSED the correct post-wrap state — a gate that makes a legitimate state
    # unreachable [[unkeyed-gate-vs-roll2f-tension]], and the exact shape of
    # [[invariant-cannot-discriminate-reversal]]: one mechanism, two purposes, opposite answers.
    # BOTH are legal; anything else is a genuine disagreement and still refuses.
    if declared is not None and (t is not None or b is not None) \
            and declared != t and declared != b:
        refusals.append(
            f"R4 ROUTING DISAGREEMENT — you declared #{declared}; the boot path routes to "
            f"#{t} (pre-wrap) and its ★ LATEST banner certifies #{b} (post-wrap). You match "
            f"NEITHER, so one of you is a session behind and it is not safe to guess which.")

    if not refusals:
        lines.append("✅ PASS — every witness present agrees.")
        return 0, lines

    if acknowledge:
        lines.append("⛔ DECLARED GAP — PASSES BECAUSE IT WAS DECLARED, NOT BECAUSE IT IS CLEAN.")
        lines.append(f"   reason given: {acknowledge}")
        lines.extend("   " + r for r in refusals)
        lines.append("   ⚠ A DECLARED gap passes; a SILENT one fails. This is on the record.")
        return 0, lines

    lines.append("⛔ REFUSED — the boot path cannot be trusted as read:")
    lines.extend("   " + r for r in refusals)
    lines.append("")
    lines.append("   Legal forms: fix the cause, or state a REAL gap with --acknowledge \"<why>\".")
    return 1, lines


# ---------------------------------------------------------------- selftest

def selftest():
    """Bites assert BOTH directions. A green that cannot fail is an assertion, not a test."""
    import tempfile
    import shutil

    fails = []

    def bite(name, ok):
        print(("  ok   " if ok else "  FAIL ") + name)
        if not ok:
            fails.append(name)

    def mkrepo(banner, title, handoffs=(), log=()):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "knowledge"), exist_ok=True)
        with open(os.path.join(d, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            if banner is not None:
                f.write(f"> ## ★ LATEST — 2026-08-02 (Sun **#{banner}**, OPUS 5)\n")
            if title is not None:
                f.write(f"> **TITLE THE NEXT CHAT →** `Apollo - #{title}: whatever`\n")
        for n in handoffs:
            open(os.path.join(d, f"_HANDOFF-{n}-x.md"), "w").close()
        for n, ev in log:
            record(n, ev, repo=d)
        return d

    print("_session.py selftest")

    # --- R0: the clean case passes, and is the control every other bite is read against.
    d = mkrepo(88, 89, handoffs=(86, 87), log=[(88, "boot"), (88, "wrap"), (89, "boot")])
    bite("clean state PASSES", verdict(d, declared=89)[0] == 0)

    # --- R1 stale title, both directions.
    d1 = mkrepo(88, 91, log=[(88, "boot"), (88, "wrap")])
    code, out = verdict(d1)
    bite("R1 REFUSES a stale title", code == 1 and any("R1" in l for l in out))
    bite("R1 does NOT fire on a correct title", not any("R1" in l for l in verdict(d)[1]))

    # --- R2 THE #86 RE-ENACTMENT. [[invariant-cannot-discriminate-reversal]] demands the OLD
    # defect be replayed, not a paraphrase of it: #85 boots, never wraps, #86 opens.
    d2 = mkrepo(84, 85, log=[(84, "boot"), (84, "wrap"), (85, "boot")])
    code, out = verdict(d2, declared=86)
    bite("R2 CATCHES the #85/#86 skipped wrap (the defect that motivated the drill)",
         code == 1 and any("R2 SKIPPED WRAP" in l for l in out))
    # ⚠ CAUGHT BY MUTATION #89, KEPT AS A LESSON: this bite first read `any("[85]" in l ...)`
    # against the WHOLE verdict, and stayed GREEN when R2 was mutated away — because "[85]"
    # also prints in the WITNESSES header as `log_unwrapped [85]`. It passed for the wrong
    # reason. A bite must grep the LINE THAT CARRIES THE CLAIM, not the whole report.
    bite("R2 names the stranded session by number (on the R2 line itself)",
         any("R2 SKIPPED WRAP" in l and "[85]" in l for l in out))
    # ...and the SAME state with the wrap present must go green, or R2 is firing on the wrong
    # thing (a check that fails for every input is not discriminating either).
    d2b = mkrepo(85, 86, log=[(84, "boot"), (84, "wrap"), (85, "boot"), (85, "wrap")])
    bite("R2 goes SILENT once the wrap is recorded", verdict(d2b, declared=86)[0] == 0)

    # --- R3 chain overtaken, both directions.
    d3 = mkrepo(88, 89, handoffs=(89,), log=[(88, "boot"), (88, "wrap")])
    code, out = verdict(d3)
    bite("R3 REFUSES when a handoff has overtaken the chain",
         code == 1 and any("R3" in l for l in out))
    bite("R3 does NOT fire on older handoffs", not any("R3" in l for l in verdict(d)[1]))

    # --- R4 routing disagreement, both directions.
    code, out = verdict(d, declared=90)
    bite("R4 REFUSES when the declaration and the chain disagree",
         code == 1 and any("R4" in l for l in out))
    bite("R4 does NOT fire when they agree", verdict(d, declared=89)[0] == 0)
    # ★ THE POST-WRAP ARM — added #89 after the live gate refused a CORRECT state. Once #89 has
    # wrapped, the banner certifies #89 and the title has been minted for #90; the running
    # session now matches the BANNER, not the title. Both are legal.
    dpw = mkrepo(89, 90, log=[(89, "boot")])
    bite("R4 accepts the POST-WRAP state (declared == banner, title already minted for next)",
         verdict(dpw, declared=89)[0] == 0)
    bite("R4 still REFUSES a declaration matching NEITHER witness",
         verdict(dpw, declared=87)[0] == 1)

    # --- the legal form: a declared gap PASSES, and says on the record that it did.
    code, out = verdict(d2, declared=86, acknowledge="wrap owed, running the wrap now")
    bite("a DECLARED gap PASSES (exit 0)", code == 0)
    bite("a declared gap is MARKED, not silently clean",
         any("DECLARED GAP" in l for l in out) and any("R2" in l for l in out))

    # --- the witness must fail LOUD on corruption, never read past it.
    d4 = mkrepo(88, 89, log=[(88, "boot")])
    with open(log_path(d4), "a", encoding="utf-8") as f:
        f.write("{not json\n")
    code, out = verdict(d4)
    bite("a CORRUPT witness REFUSES and names the line",
         code == 1 and any("CORRUPT" in l for l in out))

    # --- absent witnesses are UNKNOWN, never defaulted to a number.
    d5 = mkrepo(None, None)
    w = witnesses(d5)
    bite("absent witnesses are None, not 0",
         w["gm_banner"] is None and w["gm_title"] is None and w["handoff_max"] is None)

    # --- append-only: recording twice keeps BOTH records.
    n_before = len(read_log(d5))
    record(1, "boot", repo=d5)
    record(1, "boot", repo=d5)
    bite("the log is append-only (both records kept)", len(read_log(d5)) == n_before + 2)

    for p in (d, d1, d2, d2b, d3, d4, d5, dpw):
        shutil.rmtree(p, ignore_errors=True)

    print(f"\n{len(fails)} failure(s)" if fails else "\nall bites green")
    return 1 if fails else 0


# ---------------------------------------------------------------- cli

if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())

    def opt(name, cast=str):
        if name in argv:
            i = argv.index(name)
            if i + 1 < len(argv):
                return cast(argv[i + 1])
        return None

    if "--record" in argv:
        ev = opt("--record")
        n = opt("--n", int)
        if n is None:
            sys.exit("--record needs --n <session number>")
        r = record(n, ev)
        print(f"— recorded: {json.dumps(r, ensure_ascii=False)}")
        sys.exit(0)

    code, out = verdict(declared=opt("--declare", int), acknowledge=opt("--acknowledge"))
    print("\n".join(out))
    sys.exit(code)
