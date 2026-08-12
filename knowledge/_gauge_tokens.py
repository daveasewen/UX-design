#!/usr/bin/env python3
"""The context gauge's UNIT and its BUDGET — real Claude tokens against an absolute line.

RULED BY DAVE #56, and it retires the percentage band inside the gauge.

★ WHAT WAS WRONG, and it deadlocked the stamp for THIRTEEN CONSECUTIVE SESSIONS. Every term in
the old pre-flight stamp was a *percentage of the window*. A percentage needs a denominator; the
window's harness half is unreachable from inside any mount (`ds-025` item 1); so the denominator
had no value and `check_preflight` — which failed on any missing term — voided the whole stamp.
One unobservable quantity suppressed every observable one. That is precisely the failure
**D10 (c)** exists to prevent (*"publish the measured / estimated split on every reading"* —
half a measurement, LABELLED, beats a whole guess), committed inside the instrument that rules it.

★★ THE FIX IS A CHANGE OF UNIT, NOT A BETTER ESTIMATE. Priced in absolute tokens, the stamp
never needs the window size at all. `boot + job + wrap` is a sum of absolute quantities checked
against an absolute line. Nothing in it divides by anything.

⚠ THE BAND WAS NOT CONVERTED, IT WAS REPLACED — and the distinction is load-bearing.
`45 / 60 / 63` were percentages *of the window*; turning them into tokens would mean multiplying
by the exact quantity nobody can observe. So these are NEW thresholds with their own provenance,
below. [[measure-dont-convert-units]] — a conversion wearing a measurement's clothes is the
thing that class warns about.

THE UNIT: real Claude tokens, from `client.messages.count_tokens()`. `cl100k` (tiktoken) stays
as the OFFLINE FALLBACK ONLY and every figure derived from it is LABELLED as an estimate.
⚠ Do NOT convert cl100k figures with a fixed ratio and call the result real: the per-register
spread measured at #53 was **1.486–1.664**, so one ratio cannot re-denominate a mixed corpus.
Measured here for reference, never as a converter: `_CHAIN.md` = 4,384 tape / **6,897 real**.
"""
from __future__ import annotations
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "claude-opus-5"
ENDPOINT = "https://api.anthropic.com/v1/messages/count_tokens"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".token-cache.json")

# --------------------------------------------------------------------------- THE BUDGET
# ⛔ TWO NUMBERS, TWO DIFFERENT KINDS OF AUTHORITY. Do not blur them.
#
# BUDGET_HARD is SOURCED, not picked: 256,000 is the largest context at which Claude's recall
# has been PUBLICLY MEASURED and still holds — 93% on MRCR v2 at 256K, falling to 76% at 1M
# (verified #56 against Anthropic's context-engineering guidance and the published benchmarks).
# ⚠ Anthropic's own framing is "a performance gradient rather than a hard cliff", so this is the
# last measured-good point, NOT an edge where something breaks. Above it we are extrapolating.
#
# BUDGET_WORKING is DAVE'S, ruled #56 in this session. It is the line jobs are priced against;
# the gap to HARD is the room a job needs when it turns out bigger than its estimate.
#
# ★★ THE #53 LESSON, MECHANISED RATHER THAN DOCUMENTED. `assert_budget_clears_floor()` below
# refuses to let a budget ship that sits at or under its own floor. #53 found the M8 banner cap
# set to 5,000 against a floor of 4,998 — compliance was arithmetically impossible, and three
# sessions shaved ratified record trying to obey it. A cap must be DERIVED, and a derivation
# that lands under its own floor is not a strict cap, it is a broken one. [[translate-prose-into-machinery]]
BUDGET_HARD = 256_000        # SOURCED — last publicly measured-good recall point (93% MRCR v2)
BUDGET_WORKING = 200_000     # SOURCED — the line jobs are priced against
# ⛔ PROVENANCE CORRECTED #58b, BY DAVE, AND THE CORRECTION IS THE POINT. This line read "DAVE'S,
# ruled #56" for three sessions. He: *"BTW the 200K and 256K come from established research, its
# been worked out already."* ⇒ BOTH are SOURCED; neither is a preference he can be talked out of,
# and 200,000 was never his to re-dial by fiat. ★ A number attributed to the wrong authority is
# argued with differently — a preference invites negotiation, a measurement does not. His shape
# for the two, same message: **do not reach 200,000 · 200,000–256,000 is DANGEROUS · past 256,000
# everything goes badly.**
# ⛔ AMBER IS **PICKED**, NOT DERIVED — RULED BY DAVE, #59. 80% of working is a round fraction, not a
# derivation; labelling it DERIVED made it immune to the very rule that should have caught it
# ("derive a cap, never pick it" — RULED #53 · gate-asserted #56 · second remedy #58; three dates
# that had collapsed into one citation). ★ THE FORMULA IS THE RULING, THE NUMBER IS NOT:
#     stop = wall − wrap − step        # each term tagged MEASURED or ESTIMATED
# and the HIGH end of BOTH terms is reserved, or neither (a stop line reserved at the MEDIAN step is
# under water half the time by construction). ⚠ DO NOT stack a step reserve on top of an amber that
# already contains one — that is a RESERVE ON A RESERVE, ~10K/window, invisible because each layer is
# individually defensible. ★★ `wrap` IS NOW MEASURABLE AND WAS FIRST MEASURED AT #59: 42,434+ real
# tokens against the inherited ~25,000 folklore ⇒ low by ≥1.7×. n=1; needs 2–3 more before the line
# moves. NO BEHAVIOUR CHANGE HERE — the value is untouched by ruling; only the label was a lie.
BUDGET_AMBER = 160_000       # PICKED (see above) — where a job should stop taking on more

# --------------------------------------------------------------------------- THE BOOT
# The floor every session pays before it does anything. TWO HALVES, and they are known to
# DIFFERENT standards — which is the whole point of publishing the split (D10 (c)).
#
# DISK half: MEASURED, exactly, every run — `_CHAIN.md` plus whatever else the session read.
#
# HARNESS half: system prompt, tool schemas, deferred-tool list, MCP server instructions.
# UNREACHABLE from every mount (`ds-025` item 1) and it has been treated as a blocker since #37.
# ★ IT IS NOT A BLOCKER, AND THIS IS THE ARGUMENT THAT UNSTUCK IT: an error of ±8,000 tokens on
# a 200,000 budget is ±4%, and there is no job whose go/no-go flips on 4%. We were holding a
# PLANNING ESTIMATE to a standard built for a PUBLISHED MEASUREMENT. "A measuring tool must not
# guess" governs what we assert as fact; it was never a ban on estimating, and reading it as one
# is what produced thirteen blank stamps. So: estimate it, LABEL it, carry the error bar, move on.
# ⚠ RE-MEASURE WHEN THE SESSION SHAPE CHANGES — a new MCP server or plugin moves this figure.
# ⛔ #109 — THE NUMBER ABOVE WAS WRONG BY 3.3x AND THE MODEL UNDER IT WAS WRONG TOO.
# The ARGUMENT survives untouched: estimate it, label it, carry the error bar, move on. What
# failed was (a) the value and (b) the SHAPE. Measured first-turn boot is ~65,400 real, not
# 20,000 — 5.6x outside the +/-8,000 bar. And "boot = disk + harness" added a file read at
# turn TWO (`_CHAIN.md`) to a constant standing for turn ONE: two different moments summed as
# if they were halves of one thing. The +/-4% defence was sound arithmetic on a wrong premise;
# 45,400 against the 150,929 stop line is 30%, and that DOES flip a go/no-go.
#
# WHAT IS NOW MEASURED (real tokens, `message.usage` first turn, n=5 — #103 65,023 ·
# #104 64,765 · #105 67,370 · #107 65,046 · #109 64,778; err = half-range, and that spread
# IS the session-shape variation the old warning below was worried about):
#     first turn      ~65,400  MEASURED whole
#       MEMORY.md       8,470  MEASURED (#109, tokenised off the mounted auto-memory)
#       remainder      56,308  system prompt + tool schemas + deferred-tool list + MCP
#                              server instructions + CLAUDE.md -- BOUNDED and NAMED, but
#                              not yet split. THIS is what `ds-025` item 1 still means.
#     + _CHAIN.md      10,499  MEASURED, and ADDITIVE -- it lands at turn 2, on TOP of boot
#     = floor         ~75,900  before a word of work
# ⚠ RE-MEASURE WHEN THE SESSION SHAPE CHANGES — a new MCP server or plugin moves this figure.
#   That warning was already here, correct, and unactioned for ~72 sessions. It is not a note;
#   it is a task. [[instrument-without-a-consumer]] [[premise-ages-faster-than-rule]]
#
# ✅ RE-BASED #129, 2026-08-08 — `s129-D1`, DAVE'S CALL, TAKEN AT LAST.
# The block above stood while SEVEN consecutive same-unit, same-moment measurements landed
# BELOW it. Every one is `message.usage` on the FIRST TURN — the same instrument, the same
# moment in the session, as the n=5 pre-break series above:
#     #111 55,733 · #113 54,038 · #117 54,807 · #118 54,404 · #125 53,681 · #126 53,997 ·
#     #127 54,375     (n=7, min 53,681, max 55,733, spread 2,052)
# The structural break sits between #109 and #111 (pre-break #103–#109 mean 65,337; step
# ≈10,478 real). #111-D2 — "don't fit a constant across a structural break" — is now SPENT:
# the post-break series has been a PLATEAU since #117 (n=3 mean 54,859, spread inside the old
# ±1,400 noise band) and four further samples have landed inside it without extending a slide.
# ⛔ THE RULED VALUE IS 54,859 — the n=3 post-break mean Dave was shown at #117 and picked at
# #129. It is NOT the n=7 mean, which is 54,434. Both figures are published here on purpose:
# a session that re-derives 54,434 and "corrects" the constant by hand is doing the thing this
# project keeps having to un-do. The ruled figure is a RULING; the n=7 mean is EVIDENCE.
# The error bar is widened to 1,178 = the half-range needed for the bar around 54,859 to cover
# the whole observed post-break series (54,859 − 53,681 = 1,178 > 55,733 − 54,859 = 874). Same
# method as before (half-range), re-measured, not re-argued.
# ⛔ WHAT DID **NOT** MOVE, AND MAY NOT: the wrap-open stop line (150,929), BUDGET_WORKING
# (200,000), BUDGET_AMBER (160,000) and BUDGET_HARD (256,000). A cheaper boot moves the ROOM,
# never the LINE — the stop line carries no boot term. Measured effect of this re-base, at the
# chain size on disk at #129: floor 81,335 → 70,794, room for job + wrap 118,665 → 129,206.
# ⚠ DECLARED RESIDUAL, not a defect and not silently fixed: the SEVEN samples are FIRST-TURN
# readings, and the published "floor" is first turn + `_CHAIN.md` (turn 2). Prose across the
# repo has been comparing a first-turn measurement to the two-term floor and calling it "below
# the 75,899 floor"; that comparison mixes moments. Re-basing the FIRST-TURN term is the
# defensible act and is what is done here, so the published floor now computes as
# 54,859 + the live measured chain, not as a flat 54,859. Nothing is asserted about the chain
# term, which is measured every run anyway. [[measure-dont-convert-units]]
BOOT_FIRSTTURN_TK = 54_859
BOOT_FIRSTTURN_ERR = 1_178


def _cache() -> dict:
    try:
        with open(CACHE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def read_key() -> str | None:
    """The key never appears in output, in the repo, or in any log. `API-KEY.txt` is gitignored."""
    for name in ("API-KEY.txt", ".env.local"):
        p = os.path.join(REPO, name)
        if not os.path.exists(p):
            continue
        for line in open(p, encoding="utf-8"):
            s = line.strip().strip('"').strip("'")
            if s.startswith("ANTHROPIC_API_KEY="):
                s = s.split("=", 1)[1].strip().strip('"').strip("'")
            if s.startswith("sk-ant-"):
                return s
    return None


class MeasurementRefused(RuntimeError):
    """⛔ RAISED WHEN THE GAUGE CANNOT MEASURE. RULED #79-D1 by Dave: *"make it refuse"* —
    chosen over a LOUDER ESTIMATE and over leaving it to the session-start self-heal.

    ★ NOT `SystemExit`, and the divergence from precedent is deliberate. The two refusals
    already shipped — `_context_gauge.py::estimate_tokens()` (#74) and `_checkin.py` — are
    CLI ENTRY POINTS, where killing the process IS the report. `count()` is a LIBRARY
    function reached from inside a 39+-check gate. `SystemExit` is a `BaseException`, so a
    maintainer writing the obvious `except Exception` handler would silently reinstate the
    crash, and a gate that dies mid-sweep reports NOTHING — strictly worse than the
    estimate it replaced. [[a-crash-is-not-a-fail]]
    ⚠ PAIRED: the handler in `_capture_gate.py::selftest_preflight_tokens()` is the other
    half of this ruling. Neither half is correct alone.
    """


def count(text: str, allow_api: bool = True) -> tuple[int, str]:
    """Return `(tokens, method)`. `method` is 'real' or 'cl100k-estimate' — NEVER dropped.

    ⛔ REFUSES (`MeasurementRefused`) when neither method is reachable. ★ Note what this
    docstring has promised since it was written: exactly TWO methods. The code carried a
    THIRD — `len(text)//4`, labelled 'crude-estimate' — that no spec ever claimed and no
    ruling ever backed. #79's ARM C is what finally bit on it. This change does not add a
    behaviour; it makes the code match a contract that was already written down.

    ⚠ The method travels WITH the number, as a tuple, on purpose. A function returning a bare
    int invites a caller to publish an estimate as a measurement, which is the `ds-021` defect
    that put an OpenAI tokenizer's output into every price this project ever quoted.

    Cached on a content hash: `_CHAIN.md` is regenerated every build but rarely CHANGES, so the
    common case costs no API call at all. ⚠ The cache is keyed on content, never on mtime — the
    same mistake `index_freshness_check` exists to catch.
    """
    h = hashlib.sha256(text.encode()).hexdigest()[:32]
    c = _cache()
    if h in c:
        return c[h], "real"

    key = read_key() if allow_api else None
    if key:
        body = json.dumps({"model": MODEL,
                           "messages": [{"role": "user", "content": text}]}).encode()
        req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
            "x-api-key": key, "anthropic-version": "2023-06-01",
            "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                n = json.load(r)["input_tokens"]
            c[h] = n
            try:
                with open(CACHE, "w", encoding="utf-8") as f:
                    json.dump(c, f)
            except Exception:
                pass          # a cache that cannot write is slow, not wrong
            return n, "real"
        except (urllib.error.URLError, OSError, KeyError, ValueError):
            pass              # fall through to the LABELLED estimate — never to silence

    try:
        import tiktoken
        return len(tiktoken.get_encoding("cl100k_base").encode(text)), "cl100k-estimate"
    except ImportError as e:
        # ⛔ #79-D1. The old line here was `return len(text) // 4, "crude-estimate"`.
        # ★ NAME THE CAUSE AND THE REMEDY — loud is not enough, it has to be NAMED, or the
        # caller reports "something failed" and the next session re-derives the diagnosis.
        raise MeasurementRefused(
            "⛔ NOT MEASURED — the gauge REFUSES to guess. tiktoken is unavailable "
            f"({type(e).__name__}: {e}) and the token-counting API was not reachable "
            "either (no key, or the call failed).\n"
            "  Remedy: pip install tiktoken --break-system-packages\n"
            "  WHY there is no --estimate escape here: the crude chars/4 path under-reported "
            "by 414 tape with nothing saying so, and every price this project quoted inherited "
            "it. Dave ruled #79 that the gauge must REFUSE rather than estimate more loudly. "
            "Re-opening that is his word, not a caller's flag. [[measure-dont-convert-units]]"
        ) from e


def measure_boot(repo: str = REPO) -> dict:
    """The floor, published as a SPLIT — D10 (c)'s form, not a single number.

    Returns disk (measured), harness (estimated, with its error bar), the total, and the
    method. ⚠ Nothing here is ever collapsed into one figure by this function: a caller that
    wants one has to add them itself, and in doing so has to see which half is which.
    """
    chain = os.path.join(repo, "_CHAIN.md")
    disk, method = (0, "absent")
    if os.path.exists(chain):
        with open(chain, encoding="utf-8") as f:
            disk, method = count(f.read())
    return {
        "chain": disk, "chain_method": method,
        "firstturn": BOOT_FIRSTTURN_TK, "firstturn_err": BOOT_FIRSTTURN_ERR,
        "firstturn_method": (
            "MEASURED — `message.usage` first turn, RE-BASED #129 (`s129-D1`) to the "
            "post-break plateau: ruled 54,859, n=7 observed 53,681–55,733 (n=7 mean 54,434, "
            "published as evidence, NOT as the constant); err = half-range covering the "
            "series. The pre-break n=5 constant was 65,400. Covers system "
            "prompt + tool schemas + deferred-tool list + MCP instructions + MEMORY.md + "
            "CLAUDE.md. Its INTERNAL split is what `ds-025` item 1 now means (MEMORY.md "
            "8,470 lit at #109; 56,308 remainder still unsplit)."),
        "total": disk + BOOT_FIRSTTURN_TK,
        "err": BOOT_FIRSTTURN_ERR,
    }


def assert_budget_clears_floor(repo: str = REPO) -> list[str]:
    """⛔ THE #53 GUARD. A budget at or under its own floor makes compliance impossible.

    #53 found `M8` blocking at 5,000 against a measured floor of 4,998, and three sessions
    shaved ratified record trying to obey a gate that could not be obeyed. This runs the
    arithmetic instead of trusting that nobody will make that mistake again.
    """
    boot = measure_boot(repo)
    fails = []
    if BUDGET_WORKING <= boot["total"]:
        fails.append(
            f"BUDGET_WORKING ({BUDGET_WORKING:,}) is at or under the measured floor "
            f"({boot['total']:,} = first turn {boot['firstturn']:,} + chain {boot['chain']:,}). "
            f"Compliance is arithmetically impossible — the #53 defect. RAISE the budget or "
            f"CUT the floor; do NOT ask sessions to shave live record to fit.")
    if BUDGET_AMBER >= BUDGET_WORKING or BUDGET_WORKING >= BUDGET_HARD:
        fails.append(
            f"budget thresholds are out of order: amber {BUDGET_AMBER:,} < working "
            f"{BUDGET_WORKING:,} < hard {BUDGET_HARD:,} must hold.")
    return fails


def band_for(total: int) -> str:
    """The band, read from the constants above — never recalled, never re-derived at a call site."""
    if total < BUDGET_AMBER:
        return "GREEN"
    if total <= BUDGET_WORKING:
        return "AMBER"
    return "RED"


def main() -> int:
    # ⚠ THIRD CONSUMER OF THE #79-D1 REFUSAL, and it needs its OWN handler. A CLI that dies
    # in a traceback has technically "failed loud", but it has not failed NAMED — the reader
    # gets a stack, not the remedy. Same ruling, different report shape at each seam.
    try:
        boot = measure_boot()
    except MeasurementRefused as e:
        print(f"{e}", file=sys.stderr)
        return 2
    print(f"context gauge — unit: REAL Claude tokens ({MODEL})\n")
    print(f"  budget   amber {BUDGET_AMBER:,} · working {BUDGET_WORKING:,} (Dave #56) · "
          f"hard {BUDGET_HARD:,} (SOURCED — 93% MRCR v2)")
    print(f"  boot     {boot['total']:,} ± {boot['err']:,}")
    print(f"    + chain   {boot['chain']:>8,}  {boot['chain_method']} — ADDITIVE, lands at turn 2")
    print(f"    first turn{boot['firstturn']:>8,}  ± {boot['firstturn_err']:,} — {boot['firstturn_method']}")
    print(f"  ⇒ room for job + wrap: ~{BUDGET_WORKING - boot['total']:,} tokens")
    for f in assert_budget_clears_floor():
        print(f"  ❌ {f}")
    print("\n  ⚠ POSITION MATTERS AS MUCH AS VOLUME. Recall is U-shaped: strongest at the START")
    print("    and END of context, ~30% weaker in the MIDDLE. The chain is read first and the")
    print("    wrap is written last, so the load-bearing material already sits at the two good")
    print("    ends — that is the architecture doing work, and it is why a mid-session finding")
    print("    should be written DOWN rather than carried in the middle of a long window.")
    return 0


def selftest() -> int:
    """Bite-tests for the counting path (A), the cache (B), and degraded-measurement
    honesty (C) -- plus (D) the budget-guard LOGIC, tested relative to whatever the live
    constants are. This module shipped 238 lines with ZERO selftest; every wrap is graded
    through it and it had never been proven (session #79, P5).

    XX Does NOT re-pin the ruled budget triple. `(BUDGET_AMBER, BUDGET_WORKING, BUDGET_HARD)
    == (160_000, 200_000, 256_000)` has exactly ONE authority -- `_capture_gate.py`\'s
    `selftest_preflight_tokens()`, which asserts it by importing this module. A second
    literal copy here would be the exact defect [[gate-must-quote-what-it-forbids]] warns
    about. Arm D checks the GUARD\'s LOGIC (ordering + floor-clearing), never the numbers.

    Runs entirely OFFLINE and touches neither the real `.token-cache.json` nor the real
    `API-KEY.txt`: `CACHE`/`REPO` are swapped to an isolated tempdir for the duration and
    restored -- even on exception -- before this function returns.
    """
    failures: list[str] = []
    global CACHE, REPO
    _orig_cache, _orig_repo, _orig_urlopen = CACHE, REPO, urllib.request.urlopen
    tmpdir = tempfile.mkdtemp(prefix="gauge-selftest-")
    CACHE = os.path.join(tmpdir, ".token-cache.json")
    REPO = tmpdir

    def _arm(name, fn):
        try:
            fn()
        except Exception as e:
            failures.append(f"[{name}] CRASHED rather than failing named: "
                            f"{type(e).__name__}: {e}")

    try:
        # ================================================================== ARM A
        def _arm_a():
            fixtures = [
                ("", 0),
                ("hello world", 2),
                ("The quick brown fox jumps over the lazy dog.", 10),
                ("café résumé — token test 日本語", 12),
                ("a" * 100, 13),
            ]
            try:
                import tiktoken  # noqa: F401 -- presence probe; absence is ARM C's subject
            except ImportError:
                failures.append("[A counting path] tiktoken not installed in this "
                                "environment -- cannot verify exact cl100k_base counts. "
                                "pip install tiktoken --break-system-packages")
                return
            for text, want in fixtures:
                n, method = count(text, allow_api=False)
                if method != "cl100k-estimate":
                    failures.append(f"[A counting path] {text!r}: expected method "
                                    f"'cl100k-estimate', got {method!r}")
                elif n != want:
                    failures.append(f"[A counting path] {text!r}: expected {want} "
                                    f"tokens, got {n} -- the cl100k_base tier drifted")
        _arm("A counting path", _arm_a)

        # ================================================================== ARM B
        calls = [0]

        class _FakeResp:
            def __init__(self, payload):
                self._b = json.dumps(payload).encode()
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False
            def read(self):
                return self._b

        def _fake_urlopen(req, timeout=20):
            calls[0] += 1
            payload = json.loads(req.data.decode())
            content = payload["messages"][0]["content"]
            return _FakeResp({"input_tokens": len(content)})  # content-sensitive, not fixed

        def _arm_b1():
            with open(os.path.join(tmpdir, "API-KEY.txt"), "w", encoding="utf-8") as f:
                f.write("sk-ant-selftest-fixture-key")
            urllib.request.urlopen = _fake_urlopen
            try:
                text = "ARM B1 fixture text -- cache round-trip probe"
                want = len(text)
                n1, m1 = count(text, allow_api=True)
                n2, m2 = count(text, allow_api=True)
            finally:
                urllib.request.urlopen = _orig_urlopen
            if (n1, m1) != (want, "real"):
                failures.append(f"[B1 cache] cold read: expected ({want}, 'real'), "
                                f"got {(n1, m1)}")
            if (n2, m2) != (n1, m1):
                failures.append(f"[B1 cache] warm (cached) read {(n2, m2)} != "
                                f"cold read {(n1, m1)} -- a hit must return the SAME "
                                f"answer as the read that populated it")
            if calls[0] != 1:
                failures.append(f"[B1 cache] network called {calls[0]} time(s) for 2 "
                                f"identical count() calls -- the second read did not "
                                f"hit the cache")
        _arm("B1 cache hit fidelity", _arm_b1)

        def _arm_b2():
            calls[0] = 0
            urllib.request.urlopen = _fake_urlopen
            try:
                t_same = "ARM B2 -- identical content probe"
                t_diff = "ARM B2 -- identical content probe, CHANGED (longer text)"
                same_a = count(t_same, allow_api=True)
                same_b = count(t_same, allow_api=True)
                diff_c = count(t_diff, allow_api=True)
            finally:
                urllib.request.urlopen = _orig_urlopen
            if same_a != same_b:
                failures.append(f"[B2 cache] identical content produced different "
                                f"answers: {same_a} vs {same_b}")
            if calls[0] != 2:
                failures.append(f"[B2 cache] expected exactly 2 network calls (one "
                                f"per DISTINCT content, the repeat must be a hit), "
                                f"got {calls[0]}")
            if diff_c[0] != len(t_diff):
                failures.append(f"[B2 cache] changed content returned {diff_c[0]}, "
                                f"expected a FRESH measurement of {len(t_diff)} -- "
                                f"the cache is not content-keyed (staleness bug: a "
                                f"content change was served the OLD text's answer)")
        _arm("B2 content-hash keying (not mtime)", _arm_b2)

        def _arm_b3b4():
            global CACHE
            CACHE = os.path.join(tmpdir, "does-not-exist.json")
            if _cache() != {}:
                failures.append("[B3 cache] _cache() on a missing file did not "
                                "return {} -- it must fail SOFT")
            CACHE = os.path.join(tmpdir, "corrupt.json")
            try:
                with open(CACHE, "w", encoding="utf-8") as f:
                    f.write("{not valid json,,,")
                if _cache() != {}:
                    failures.append("[B4 cache] _cache() on a corrupt file did not "
                                    "return {} -- it must fail SOFT")
                try:
                    count("text measured while the cache file on disk is corrupt",
                          allow_api=False)
                except Exception as e:
                    failures.append(f"[B4 cache] count() crashed on a corrupt cache "
                                    f"file instead of falling through: "
                                    f"{type(e).__name__}: {e}")
            finally:
                # ALWAYS restore, even if _cache()/count() raised above (a mutation
                # that breaks B3/B4 must not leak a corrupt CACHE path into ARM C/D).
                CACHE = os.path.join(tmpdir, ".token-cache.json")
        _arm("B3/B4 _cache() fails soft on missing/corrupt file", _arm_b3b4)

        try:
            os.remove(os.path.join(tmpdir, "API-KEY.txt"))
        except OSError:
            pass
        # From here on no key is discoverable via REPO -- arms C/D cannot reach the
        # network branch even though urllib.request.urlopen is back to the real one.

        # ================================================================== ARM C
        def _arm_c():
            had = "tiktoken" in sys.modules
            prev = sys.modules.get("tiktoken")
            sys.modules["tiktoken"] = None  # simulate ImportError, no real uninstall
            try:
                try:
                    n, method = count("ARM C -- tiktoken-unavailable probe",
                                      allow_api=False)
                    failures.append(
                        f"[C degraded-measurement honesty] tiktoken unavailable: "
                        f"count() did NOT refuse -- returned ({n}, {method!r}) rather "
                        f"than raising. ds-025: 'a measuring tool that estimates "
                        f"silently is the defect'. Precedent already in this repo: "
                        f"_context_gauge.py::estimate_tokens() raises SystemExit by "
                        f"default here (#74) and _checkin.py 'FAILS LOUD without "
                        f"tiktoken'; _gauge_tokens.py::count() has no equivalent -- "
                        f"it falls through to len(text)//4, labelled "
                        f"'crude-estimate', unconditionally.")
                except BaseException as e:  # a legal refusal may be SystemExit, not Exception
                    msg = str(e)
                    if not msg or "tiktoken" not in msg.lower():
                        failures.append(
                            f"[C degraded-measurement honesty] count() raised "
                            f"{type(e).__name__} but the message does not name the "
                            f"cause ({msg!r}) -- fail LOUD AND NAMED, not just loud "
                            f"[[a-crash-is-not-a-fail]]")
            finally:
                if had:
                    sys.modules["tiktoken"] = prev
                else:
                    sys.modules.pop("tiktoken", None)
        _arm("C degraded-measurement honesty (ds-025)", _arm_c)

        # ================================================================== ARM D
        def _arm_d():
            fails_at_rest = assert_budget_clears_floor()
            if fails_at_rest:
                failures.append(f"[D budget guard] assert_budget_clears_floor() is "
                                f"NOT clean at rest: {fails_at_rest}")
            if band_for(BUDGET_AMBER - 1) != "GREEN":
                failures.append("[D band_for] one token below amber must be GREEN")
            if band_for(BUDGET_AMBER) != "AMBER":
                failures.append("[D band_for] exactly at amber must be AMBER")
            if band_for(BUDGET_WORKING) != "AMBER":
                failures.append("[D band_for] exactly at working must still be "
                                "AMBER (RED starts strictly ABOVE working)")
            if band_for(BUDGET_WORKING + 1) != "RED":
                failures.append("[D band_for] one token above working must be RED")
        _arm("D budget-guard logic (band_for / assert_budget_clears_floor)", _arm_d)

    finally:
        CACHE, REPO = _orig_cache, _orig_repo
        urllib.request.urlopen = _orig_urlopen
        shutil.rmtree(tmpdir, ignore_errors=True)

    if failures:
        for x in failures:
            print(f"  ERR {x}")
        print(f"\n_gauge_tokens.py selftest FAILED -- {len(failures)} named failure(s).")
        return 1
    print("_gauge_tokens.py selftest OK -- counting path exact on 5 fixtures; cache "
         "hit fidelity + content-hash keying + corrupt-file robustness all bite; "
         "degraded-measurement honesty holds; band/floor guard logic verified "
         "relative to the live constants.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(main())
