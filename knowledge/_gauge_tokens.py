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

import hashlib
import json
import os
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
BUDGET_WORKING = 200_000     # DAVE'S, ruled #56 — the line jobs are priced against
BUDGET_AMBER = 160_000       # DERIVED — 80% of WORKING: where a job should stop taking on more

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
BOOT_HARNESS_EST = 20_000
BOOT_HARNESS_ERR = 8_000


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


def count(text: str, allow_api: bool = True) -> tuple[int, str]:
    """Return `(tokens, method)`. `method` is 'real' or 'cl100k-estimate' — NEVER dropped.

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
    except ImportError:
        return len(text) // 4, "crude-estimate"


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
        "disk": disk, "disk_method": method,
        "harness": BOOT_HARNESS_EST, "harness_err": BOOT_HARNESS_ERR,
        "harness_method": "estimate — UNREACHABLE from any mount (ds-025 item 1)",
        "total": disk + BOOT_HARNESS_EST,
        "err": BOOT_HARNESS_ERR,
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
            f"({boot['total']:,} = disk {boot['disk']:,} + harness ~{boot['harness']:,}). "
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
    boot = measure_boot()
    print(f"context gauge — unit: REAL Claude tokens ({MODEL})\n")
    print(f"  budget   amber {BUDGET_AMBER:,} · working {BUDGET_WORKING:,} (Dave #56) · "
          f"hard {BUDGET_HARD:,} (SOURCED — 93% MRCR v2)")
    print(f"  boot     {boot['total']:,} ± {boot['err']:,}")
    print(f"    disk      {boot['disk']:>8,}  {boot['disk_method']}")
    print(f"    harness   {boot['harness']:>8,}  ± {boot['harness_err']:,} — {boot['harness_method']}")
    print(f"  ⇒ room for job + wrap: ~{BUDGET_WORKING - boot['total']:,} tokens")
    for f in assert_budget_clears_floor():
        print(f"  ❌ {f}")
    print("\n  ⚠ POSITION MATTERS AS MUCH AS VOLUME. Recall is U-shaped: strongest at the START")
    print("    and END of context, ~30% weaker in the MIDDLE. The chain is read first and the")
    print("    wrap is written last, so the load-bearing material already sits at the two good")
    print("    ends — that is the architecture doing work, and it is why a mid-session finding")
    print("    should be written DOWN rather than carried in the middle of a long window.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
