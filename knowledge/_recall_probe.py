#!/usr/bin/env python3
"""_recall_probe.py — the per-session BLIND RECALL PROBE, ruled `s214-D3` (Dave, 2026-08-21).

CONSUMER (named, because an instrument without a consumer is the defect):
    THE CONDUCTOR, at EVERY check-in past 150,000 FILL, and mandatorily while the session is
    inside the 200,000–256,000 CONDITIONAL BAND (`s214-D1`, condition (3); the band section of
    `knowledge/_RUNBOOK-context-gauge.md`). The conductor plants once, early, then quizzes
    itself blind at each check-in. One miss CLOSES the band for that session and judgment work
    stops immediately. The probe outlives the band: it is the standing defence against a silent
    model-version recall regression on this seat.

UNIT DISCIPLINE (say the unit, never convert one into another):
    This tool measures RECALL — a BOOLEAN PER KEY, hit or miss, n = number of planted keys.
    It is NOT a token measurement, it is not a percentage of a window, and its verdict may never
    be quoted as a gauge figure. FILL is measured by `knowledge/_gauge_tokens.py` / `_checkin.py`
    and by nothing here.

THE HASH DESIGN, AND WHAT IT DOES AND DOES NOT BUY:
    The plant file stores keys, question phrasings, a per-key random salt and
    sha256(salt + normalized answer). The PLAINTEXT ANSWERS EXIST NOWHERE ON DISK — only in the
    window. So a green verdict cannot be produced by reading this store. It CAN still be produced
    by scrolling back to the plant output in the transcript, and no hash can prevent that; the
    design makes that failure DETECTABLE-BY-HONESTY, which is why the honesty rule is printed in
    the tool's own output rather than left to memory.
    ⚠ A green probe is NECESSARY, NEVER SUFFICIENT (`s214-D1`): synthetic recall does not predict
    downstream synthesis, which is why judgment work stays illegal in-band regardless.

USAGE
    python3 knowledge/_recall_probe.py --plant   --session 214
    python3 knowledge/_recall_probe.py --quiz    --session 214
    python3 knowledge/_recall_probe.py --check   --session 214 K3=turquoise K7=41 ...
    python3 knowledge/_recall_probe.py --check   --session 214 --stdin   < answers.json
    python3 knowledge/_recall_probe.py --status  --session 214
    python3 knowledge/_recall_probe.py --selftest

EXIT CODES:  0 GREEN · 1 RED (recall miss / selftest leg failed) · 2 REFUSED (loud and named:
bad usage, malformed input, missing or already-present plant file). A crash is not a fail — the
parse helpers fail loud and named, and every refusal says which file and which key.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import random
import re
import secrets
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HONESTY_RULE = ("Answer from window memory. Re-reading the transcript, this store, or the plant "
                "output is the defect this instrument exists to catch.")

# Fact material. Each fact = one CATEGORY (fixes the question phrasing), one SUBJECT, one VALUE.
# Categories are drawn without replacement so no two facts are alike in shape as well as content.
CATEGORIES = {
    "colour":   ("what colour is {subject}?",
                 ["turquoise", "ochre", "magenta", "slate grey", "olive", "crimson",
                  "pale gold", "indigo", "rust orange", "seafoam"]),
    "number":   ("what number is painted on {subject}?",
                 [str(n) for n in (7, 12, 19, 23, 31, 41, 47, 58, 63, 77, 84, 91)]),
    "city":     ("which city is {subject} in?",
                 ["Valparaiso", "Trondheim", "Nagasaki", "Cordoba", "Gdansk", "Hobart",
                  "Bergen", "Palermo", "Halifax", "Dunedin"]),
    "material": ("what is {subject} made of?",
                 ["brass", "cedar", "granite", "enamel", "hemp rope", "cast iron",
                  "smoked glass", "terracotta", "zinc", "walnut"]),
    "weather":  ("what was the weather at {subject}?",
                 ["sleet", "sea fog", "flat calm", "hailstones", "thunder", "dry heat",
                  "drizzle", "gale"]),
}
SUBJECTS = ["the harbor crane", "the night ferry", "the observatory door", "the market clock",
            "the fishing hut", "the tram depot", "the lighthouse stair", "the customs shed",
            "the bell tower", "the pilot boat", "the reading room", "the freight lift",
            "the weather mast", "the tannery gate", "the signal box"]


# ------------------------------------------------------------------ paths, refusals, normalizing
def probe_dir() -> str:
    """The plant store. `APOLLO_PROBE_DIR` exists so `--selftest` can drive the REAL code path
    against a temp dir — the selftest must never write into the live `_probe/`."""
    return os.environ.get("APOLLO_PROBE_DIR") or os.path.join(HERE, "_probe")


def plant_path(session: int) -> str:
    return os.path.join(probe_dir(), f"session-{session}.json")


def refuse(msg: str) -> "NoReturn":  # noqa: F821
    print(f"⛔ RECALL PROBE REFUSED: {msg}", file=sys.stderr)
    sys.exit(2)


def normalize(s: str) -> str:
    """casefold · strip · collapse whitespace · drop trailing sentence punctuation.
    Deliberately narrow: it forgives typing, never meaning."""
    s = re.sub(r"\s+", " ", str(s)).strip().casefold()
    return s.rstrip(".,!?;:").strip()


def _iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_plant(session: int) -> dict:
    path = plant_path(session)
    if not os.path.isfile(path):
        refuse(f"no plant file for session {session} at {path}. Plant first "
               f"(`--plant --session {session}`) — an unplanted probe is not a green one.")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError) as e:
        refuse(f"plant file {path} is unreadable ({type(e).__name__}: {e}). "
               f"It is the only record of the salts; do not repair it by hand — re-plant.")
    if not isinstance(data, dict) or not isinstance(data.get("facts"), list) or not data["facts"]:
        refuse(f"plant file {path} has no `facts` list — malformed, named, not guessed at.")
    return data


# ---------------------------------------------------------------------------------------- PLANT
def cmd_plant(session: int) -> int:
    path = plant_path(session)
    if os.path.exists(path):
        refuse(f"a plant already exists for session {session} at {path} "
               f"(planted_at {load_plant(session).get('planted_at', '?')}). "
               f"A silent re-plant would reset the very memory under test. One plant per session.")
    os.makedirs(probe_dir(), exist_ok=True)

    cats = random.sample(sorted(CATEGORIES), 4)
    subs = random.sample(SUBJECTS, 4)
    keys = random.sample([f"K{n}" for n in range(1, 10)], 4)

    facts, printable = [], []
    for key, cat, subject in zip(keys, cats, subs):
        question_tpl, values = CATEGORIES[cat]
        value = random.choice(values)
        salt = secrets.token_hex(16)
        facts.append({"key": key, "category": cat,
                      "question": f"{key} — " + question_tpl.format(subject=subject),
                      "salt": salt,
                      "sha256": hashlib.sha256((salt + normalize(value)).encode()).hexdigest()})
        printable.append(f"probe-fact {key}: {subject} is {value}")

    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"session": session, "planted_at": _iso(), "n": len(facts), "facts": facts},
                  fh, indent=1)
        fh.write("\n")

    print("=" * 78)
    print(f"RECALL PROBE — PLANT, session {session}   (s214-D3)")
    print("=" * 78)
    print("READ THESE INTO THE WINDOW NOW. They are printed ONCE and stored only as salted")
    print("hashes — the plaintext exists nowhere on disk and cannot be recovered from the store.")
    print("")
    for line in printable:
        print(f"    {line}")
    print("")
    print(f"Store (hashes + salts + questions only): {path}")
    print(f"Quiz at every check-in past 150K FILL:   --quiz --session {session}")
    print(HONESTY_RULE)
    print("=" * 78)
    return 0


# ----------------------------------------------------------------------------------------- QUIZ
def cmd_quiz(session: int) -> int:
    data = load_plant(session)
    print("=" * 78)
    print(f"RECALL PROBE — QUIZ, session {session}   (planted {data.get('planted_at', '?')})")
    print("=" * 78)
    print(HONESTY_RULE)
    print("")
    for f in data["facts"]:
        print(f"    {f['question']}")
    print("")
    keys = " ".join(f"{f['key']}=<answer>" for f in data["facts"])
    print(f"Then: python3 knowledge/_recall_probe.py --check --session {session} {keys}")
    print("Measures RECALL (boolean per key, n=%d) — never a token figure." % len(data["facts"]))
    print("=" * 78)
    return 0


# ---------------------------------------------------------------------------------------- CHECK
def parse_pairs(pairs: list[str], use_stdin: bool) -> dict:
    given: dict[str, str] = {}
    if use_stdin:
        raw = sys.stdin.read()
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            refuse(f"--stdin expected a JSON object of key→answer; got {raw[:80]!r} "
                   f"(JSONDecodeError: {e}).")
        if not isinstance(obj, dict):
            refuse(f"--stdin JSON must be an OBJECT of key→answer, got {type(obj).__name__}.")
        given.update({str(k): str(v) for k, v in obj.items()})
    for p in pairs:
        if "=" not in p:
            refuse(f"answer {p!r} is not a `key=value` pair. Malformed input is refused, never "
                   f"silently dropped — a dropped answer would score as a MISS and close the band.")
        k, v = p.split("=", 1)
        k = k.strip()
        if not k:
            refuse(f"answer {p!r} has an empty key.")
        if k in given:
            refuse(f"key {k!r} was answered twice — ambiguous input is refused, not resolved.")
        given[k] = v
    if not given:
        refuse("no answers supplied. Pass `key=value` pairs or `--stdin` with a JSON object.")
    return given


def cmd_check(session: int, pairs: list[str], use_stdin: bool) -> int:
    data = load_plant(session)
    given = parse_pairs(pairs, use_stdin)
    expected = {f["key"]: f for f in data["facts"]}

    unknown = sorted(set(given) - set(expected))
    if unknown:
        refuse(f"answers given for key(s) {unknown} that were never planted for session "
               f"{session} (planted: {sorted(expected)}). Refused rather than ignored.")

    hits, misses = [], []
    for key, f in expected.items():
        if key not in given:
            misses.append((key, "NO ANSWER GIVEN — a missing key counts as a miss"))
            continue
        got = hashlib.sha256((f["salt"] + normalize(given[key])).encode()).hexdigest()
        (hits if got == f["sha256"] else misses).append(
            (key, "" if got == f["sha256"] else f"answered {normalize(given[key])!r} — wrong"))

    print("=" * 78)
    print(f"RECALL PROBE — CHECK, session {session}   (n={len(expected)} keys, boolean recall)")
    print("=" * 78)
    for key in sorted(expected):
        miss = dict(misses).get(key)
        print(f"    ✗ {key}  {miss}" if miss is not None else f"    ✓ {key}")
    print("")

    verdict = "GREEN" if not misses else "RED"
    if misses:
        print(f"RED — recall MISSED on: {', '.join(sorted(k for k, _ in misses))}")
        print("BAND CLOSED for this session per s214-D1 condition (3) — judgment work stops")
    else:
        print(f"GREEN — {len(hits)}/{len(expected)} recalled. The s214-D1 band stays legal on "
              f"condition (3).")
        print("⚠ Necessary, never sufficient: judgment work remains illegal in-band regardless.")
    print("=" * 78)

    data["last_check"] = {"at": _iso(), "verdict": verdict,
                          "missed": sorted(k for k, _ in misses)}
    try:
        with open(plant_path(session), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1)
            fh.write("\n")
    except OSError as e:
        print(f"⚠ verdict NOT recorded to the store ({type(e).__name__}: {e}) — the verdict "
              f"above still stands; the residual is that the check-in status line cannot see it.",
              file=sys.stderr)
    return 0 if verdict == "GREEN" else 1


# --------------------------------------------------------------------------------------- STATUS
def cmd_status(session: int) -> int:
    """One line, for a check-in to consume. Always rc 0 — a status read is not a verdict."""
    path = plant_path(session)
    if not os.path.isfile(path):
        print(f"PROBE:  session {session} NOT PLANTED — the s214-D1 band is NOT legal "
              f"(condition (3) unmet). Plant: --plant --session {session}")
        return 0
    data = load_plant(session)
    last = data.get("last_check")
    if not last:
        print(f"PROBE:  planted {data.get('planted_at', '?')}, n={data.get('n', '?')} — "
              f"NO CHECK RECORDED yet. Quiz: --quiz --session {session}")
    else:
        tail = "" if last["verdict"] == "GREEN" else f" (missed {', '.join(last['missed'])})"
        print(f"PROBE:  planted {data.get('planted_at', '?')}, n={data.get('n', '?')} — last "
              f"check {last['at']} {last['verdict']}{tail}")
    return 0


# ------------------------------------------------------------------------------------- SELFTEST
def _run(args: list[str], env: dict, stdin: str | None = None) -> tuple[int, str]:
    p = subprocess.run([sys.executable, os.path.abspath(__file__)] + args, env=env,
                       input=stdin, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def cmd_selftest() -> int:
    """Drives the REAL code path end-to-end in a temp dir (never the live `_probe/`), and proves
    the gate BOTH WAYS as `s214-D3` demands: a gate that cannot go red is a zombie."""
    fails: list[str] = []

    def leg(name: str, ok: bool, detail: str = "") -> None:
        print(f"  {'✓' if ok else '✗'} {name}{(' — ' + detail) if detail else ''}")
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, APOLLO_PROBE_DIR=tmp)
        print("RECALL PROBE — SELFTEST (temp store: %s)" % tmp)

        rc, out = _run(["--plant", "--session", "999"], env)
        facts = dict(re.findall(r"probe-fact (\S+): .+? is (.+)$", out, re.M))
        leg("plant runs rc 0 and prints 4 facts", rc == 0 and len(facts) == 4,
            f"rc={rc}, parsed {sorted(facts)}")
        if len(facts) != 4:
            print("  (cannot continue without planted facts)")
            return 1

        store = json.load(open(os.path.join(tmp, "session-999.json")))
        blob = json.dumps(store).casefold()
        leaked = [k for k, v in facts.items() if normalize(v) in blob]
        leg("plaintext answers absent from the store", not leaked, f"leaked: {leaked}")

        rc, qout = _run(["--quiz", "--session", "999"], env)
        leg("quiz rc 0, carries the honesty rule verbatim, leaks no answer",
            rc == 0 and HONESTY_RULE in qout
            and not any(normalize(v) in qout.casefold() for v in facts.values()))

        rc, out = _run(["--check", "--session", "999"]
                       + [f"{k}={v}" for k, v in facts.items()], env)
        leg("MUTATION (green): all-correct answers → rc 0 GREEN",
            rc == 0 and "GREEN" in out, f"rc={rc}")

        wrong = dict(facts)
        victim = sorted(wrong)[0]
        wrong[victim] = "definitely-not-the-answer"
        rc, out = _run(["--check", "--session", "999"]
                       + [f"{k}={v}" for k, v in wrong.items()], env)
        leg("MUTATION (red): one wrong answer → rc 1 RED, names the key, closes the band",
            rc == 1 and "RED" in out and victim in out
            and "BAND CLOSED for this session per s214-D1 condition (3)" in out, f"rc={rc}")

        short = {k: v for k, v in facts.items() if k != victim}
        rc, out = _run(["--check", "--session", "999"] + [f"{k}={v}" for k, v in short.items()],
                       env)
        leg("MUTATION (red): a MISSING key → rc 1 RED, counted as a miss",
            rc == 1 and "RED" in out and "NO ANSWER GIVEN" in out, f"rc={rc}")

        rc, out = _run(["--check", "--session", "999", "K1", "no-equals-sign"], env)
        leg("malformed input → rc 2, loud and named", rc == 2 and "REFUSED" in out, f"rc={rc}")

        rc, out = _run(["--check", "--session", "999", "--stdin"], env, stdin="not json{")
        leg("malformed --stdin JSON → rc 2, loud and named", rc == 2 and "REFUSED" in out,
            f"rc={rc}")

        rc, out = _run(["--plant", "--session", "999"], env)
        leg("double plant → rc 2 refusal (no silent re-plant)",
            rc == 2 and "already exists" in out, f"rc={rc}")

        rc, out = _run(["--check", "--session", "998", "K1=x"], env)
        leg("check with no plant file → rc 2, named", rc == 2 and "no plant file" in out,
            f"rc={rc}")

        rc, out = _run(["--status", "--session", "999"], env)
        leg("status line rc 0 and reports the recorded verdict",
            rc == 0 and "PROBE:" in out and "RED" in out, f"rc={rc}")

    print("")
    if fails:
        print(f"SELFTEST RED — {len(fails)} leg(s) failed: {fails}")
        return 1
    print("SELFTEST GREEN — mutation-proven BOTH ways; the gate can go red.")
    return 0


# ----------------------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--plant", action="store_true")
    ap.add_argument("--quiz", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--session", type=int)
    ap.add_argument("--stdin", action="store_true", help="read answers as a JSON object on stdin")
    ap.add_argument("answers", nargs="*", help="key=value pairs, for --check")
    a = ap.parse_args()

    modes = [m for m in ("plant", "quiz", "check", "status", "selftest") if getattr(a, m)]
    if len(modes) != 1:
        refuse(f"exactly one of --plant/--quiz/--check/--status/--selftest is required, got "
               f"{modes or 'none'}.")
    if modes[0] == "selftest":
        return cmd_selftest()
    if a.session is None:
        refuse(f"--{modes[0]} requires --session N.")
    if modes[0] == "plant":
        return cmd_plant(a.session)
    if modes[0] == "quiz":
        return cmd_quiz(a.session)
    if modes[0] == "status":
        return cmd_status(a.session)
    return cmd_check(a.session, a.answers, a.stdin)


if __name__ == "__main__":
    sys.exit(main())
