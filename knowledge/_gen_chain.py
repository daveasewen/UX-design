#!/usr/bin/env python3
"""Generate `_CHAIN.md` — the read chain as a FILE, so a cold session can read it cheaply.

WHY THIS EXISTS (#41, measured, Dave's ruling).
-----------------------------------------------
The read chain has been "CUT" since #33 and the cut has never been enforceable, because the
instruction describing it lives *inside the 433-line file it is trying to make cheap*.

    contract price of the chain ......  3,838 tape
    what #41's opener actually paid ... 28,653 harness-tokens

Not carelessness. **`Read` cannot read less than a file.** A session that opens
`GOOD-MORNING.md` pays for all 18,434 tape to discover it should have stopped at line 21.
Five sessions called the chain CUT while every one of them paid full price for it.

⇒ The fix is not a rule and not a discipline. It is a SMALLER FILE. Generate the chain, point
memory at it, and the expensive thing stops being the first thing anyone touches.

WHAT THIS IS NOT
----------------
⚠ **Not the brief's item 1.** That one moves §A and §C out of `GOOD-MORNING.md`, and the survey
at #41 found it blocked by `STAND-004` — a gate that exists *specifically* to stop §A leaving
that file, after §A was eroded in a rewrite on 2026-07-18. Six modules hard-reference GM's
sections by path and the index selftest pins §A's children to `file == "GOOD-MORNING.md"`.
This generator changes **no file, no gate, and no module**. It is additive and reversible by
deleting one file.

⚠ **Not a fourth mechanism.** The Friday brief names "adding a fourth mechanism" as a thing that
will undo the programme. This adds no cap, no block and no judgment: it copies bytes that
already exist into a smaller container. Nothing here can refuse a session anything.

THE ONE RULE THAT KEEPS IT HONEST
---------------------------------
★ **The chain text comes from `_capture_gate.chain_parts` — the same slicer the gate MEASURES
with.** Not a copy of its logic; the function itself. So "the chain is 3,838 tape" and "here is
the chain" can never describe different text. A second slicer here would be the exact drift
class `read_chain_tk`'s own docstring refuses.

⚠ Generated files rot when nothing checks them. `--check` regenerates in memory and compares,
and it is wired into `_build_all.py`, so a stale `_CHAIN.md` fails the build rather than quietly
serving a previous session's record to a cold reader — the #32 defect, which is precisely the
failure mode a chain file is most exposed to.

USAGE
    python3 knowledge/_gen_chain.py              # write _CHAIN.md
    python3 knowledge/_gen_chain.py --check      # exit 1 if _CHAIN.md is stale (build step)
    python3 knowledge/_gen_chain.py --selftest   # the bites
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_NAME = "_CHAIN.md"

sys.path.insert(0, HERE)

# #193 — the COULD-NOT-ASK convention this module INVENTED at #183, now formalised so consumers
# can recognise it (exit 77 + a `COULD-NOT-ASK:` line). See `_could_not_ask.py`'s docstring.
import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity

# ⛔ #221 (from #220's L4 audit, findings F6 and F8). EVERY PATH AND EVERY ID IN THE WRAPPER
# BELOW USED TO BE TYPED, and typed `knowledge/…`. This file runs byte-identical in two trees —
# this repo, and every shipped Gumdrop pack, where the same scripts live under
# `memento-package/machinery/`. So the ONE file a cold session is told to read, and told never
# to hand-edit, handed a designer three paths that do not exist in their project and five
# `gm:` fetch ids that refuse on their index. It is the same class as the retrieval signpost
# (F3) but in the boot file. A typed path cannot be right in two trees.
#
# The paths are now RESOLVED against the tree this generator is actually running in, and the
# fetch-id examples are printed only when the live index really carries `gm:` records. An
# example that refuses when followed is worse than no example.


def _invocation_base():
    """The directory a reader of the chain runs commands FROM, resolved, not assumed.

    In a shipped pack that is the pack root (the folder with `_MANIFEST.json`, which is the
    VS Code workspace root and the cwd every pack doc says to use). In this repo there is no
    manifest above `knowledge/`, so it is the repo root. Same code, both trees."""
    d = HERE
    while True:
        if os.path.isfile(os.path.join(d, "_MANIFEST.json")) and \
                os.path.isdir(os.path.join(d, "knowledge")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.dirname(HERE)
        d = parent


def _in_a_pack():
    """True when this file is running inside a shipped Apollo pack rather than the source repo.

    Same marker `_invocation_base()` uses — `_MANIFEST.json` beside `knowledge/` — asked as a
    yes/no. Keyed on the TREE, never on a hostname, a user or a CI variable, so it gives the
    same answer to anyone holding the same pack."""
    d = HERE
    while True:
        if os.path.isfile(os.path.join(d, "_MANIFEST.json")) and \
                os.path.isdir(os.path.join(d, "knowledge")):
            return True
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def _cmd(script_name, *extra_dirs):
    """`python3 <path>` for a sibling script, relative to the invocation base — or, if the
    script is genuinely not there, its bare name, so the sentence never names a fiction."""
    base = _invocation_base()
    for d in (HERE,) + tuple(extra_dirs):
        p = os.path.join(d, script_name)
        if os.path.isfile(p):
            return "python3 " + os.path.relpath(p, base)
    return "python3 " + script_name


def _retrieval_ids():
    """The `gm:` orientation examples — ONLY if the live index actually carries them.

    L4 drove all five ids the typed sentence named and every one refused
    (`fetch: unknown id 'gm:DOFIRST' — REFUSING`). A boot file that hands a reader five dead
    ids has taught them the tool is broken on their first use of it."""
    idx = os.path.join(HERE, "_memento-index.json")
    try:
        with open(idx, encoding="utf-8") as f:
            ids = [r.get("id", "") for r in json.load(f).get("records", [])]
    except Exception:
        return ""
    gm = [i for i in ids if i.startswith("gm:")]
    if not gm:
        return ""
    return (" §A orientation is `gm:A`; the queue is `gm:C1`…; the archives, briefs, runbooks "
            "and ledgers are all indexed.")


BANNER = """<!-- GENERATED by {gen_cmd_bare} — DO NOT HAND-EDIT.
     Edit GOOD-MORNING.md / _LIVE-STATE.md and regenerate; `--check` is a build step. -->

# The read chain — everything a cold session must read, and nothing else

> **This file is GENERATED and it is the whole contract.** It carries `GOOD-MORNING.md`'s header
> and ★ LATEST banner, plus `_LIVE-STATE.md`'s ⏱ LATEST delta — the three things GM-D7-am names
> (CUT #33 on Dave's ruling). **If you have read this file, you have read the chain.**
>
> ⚠ **Do NOT now open `GOOD-MORNING.md` to "check".** It is {gm_tk:,} {unit}; this file already
> carries the part of it a cold session needs, and the rest is retrieval surface you are not
> meant to pay for at boot. That reflex is the thing this file
> exists to stop — five sessions called the chain CUT and every one of them paid full price.
>
> ★ **Everything else is RETRIEVAL, never a reading list:**
> `{search_cmd} "<q>"` → `--fetch <id>`.{retrieval_ids}
> **Ask for what you need; do not read a file to find out whether you need it.**

---
"""

FOOTER = """

---

*(Chain ends. **{file_tk:,} {unit} — the unit is THE WHOLE FILE**, this generated wrapper included:
the number in this sentence is the size of the file containing it, held exact by a fixed point.
`GOOD-MORNING.md` is {gm_tk:,} {unit} and stays whole for retrieval; you have paid for
{chain_pct:.0f}% of it. Under 40% is this generator's own floor — above it, the wrapper is
carrying more than the slice, and `--selftest` says so by name.)*
"""

# ⛔ #82 — THE UNIT WORD IS MEASURED, NOT TYPED. Both templates above said `tape` as a literal
# for 49 sessions. The moment #82-D1 wired the real counter the NUMBERS became real tokens while
# the WORD stayed `tape` — a real measurement wearing the estimator's name, in the one file every
# cold session reads. That is the ds-021 defect reappearing one layer out: the defect was never
# the arithmetic, it is a claim about a unit that nothing checks.
# ★ So the word is asked of the instrument on every build. Offline, the chain will honestly say
# `tape (cl100k ESTIMATE)` — which is the point: a chain generated by a weaker instrument must
# SAY SO to the session reading it, rather than inherit a label from a healthier machine.
_UNIT_WORDS = {"real": "real", "cl100k": "tape (cl100k ESTIMATE)",
               "estimate": "bytes ESTIMATE"}


def unit_word(cg):
    """The display word for the tier the measurer is on RIGHT NOW. ⚠ Unknown tiers are NOT
    defaulted to a friendly word — an unrecognised tier is named in the output so it cannot pass
    as one of the three. [[measuring-tool-must-not-guess]]: UNKNOWN is never defaulted."""
    tier = cg.measurement_tier()
    return _UNIT_WORDS.get(tier, f"UNRECOGNISED-TIER({tier})")


# ---------------------------------------------------------------------------------------------
# ★ #173 FINDING → THE COULD-NOT-ASK REMEDY (queued at #173, built #183).
#
# THE DEFECT, proven at #173 by single-variable isolation and written down so it is never
# re-derived: `real` token measurement is reachable by exactly two routes — `API-KEY.txt` or
# `knowledge/.token-cache.json` — and BOTH ARE GITIGNORED (`.gitignore:57,58`). A CI checkout has
# neither, so it can only stamp `tape (cl100k ESTIMATE)` where the COMMITTED `_CHAIN.md` says
# `real`. The regenerated text can therefore NEVER byte-match, and `check()` handed that straight
# to its byte comparison, which could only ever call it "_CHAIN.md is STALE". Dropping the cache
# file into a clone flipped `--check` from 1 to 0 with nothing else touched — one variable.
#
# ⇒ That is a verdict about the ARTEFACT dressed over a fact about the ENVIRONMENT: gate [107]
# was STALE in CI and FRESH locally ON THE SAME COMMIT. A gate that disagrees with itself across
# environments is not reporting on the artefact [[gate-cannot-pass-in-one-environment]].
#
# ★ THE SHAPE IS #59's, ONE TIER OUT, AND DELIBERATELY SO. #59 refused when the instrument was
# DEGRADED (no tiktoken at all). That refusal fires from `build()` and covers the `estimate` tier
# only, because `measurement_degraded()` must NOT be widened to "not real" — `_gen_chain.build()`
# consumes it as a HARD refusal, so widening it makes `_CHAIN.md` UNGENERABLE offline and kills
# the one artefact a cold session cannot start without (`_capture_gate.py`'s own ⛔ note above
# `_REAL_TIER_ENV`). So the widening happens HERE, in `check()` ONLY, where the consequence is a
# declared unknown rather than an unbuildable chain: `write()` is untouched and an offline build
# still honestly stamps its own weaker tier.
#
# THE CLAUSE: when the tier a measurement would use RIGHT NOW differs from the tier the committed
# file is STAMPED with, `--check` exits COULD-NOT-ASK — a refusal, not a verdict in either
# direction — and it must NOT say STALE. Same posture the #58/#59 bites already enforce for the
# degraded case: report the MEASUREMENT, never prescribe the region [[gate-narrows-its-own-rule]].
_TIER_BY_UNIT_WORD = {word: tier for tier, word in _UNIT_WORDS.items()}
_STAMP_RE = re.compile(r"\*\*[\d,]+ (.+?) — the unit is THE WHOLE FILE\*\*")


def stamped_tier(text):
    """The tier the ON-DISK chain was stamped with, read out of its own footer sentence.

    Returns `'real'` · `'cl100k'` · `'estimate'`, or `None` when the footer is absent or carries
    a word this module does not recognise. ⚠ `None` is NOT "fine" and is never defaulted to the
    live tier: an unreadable stamp means the comparison CANNOT BE MADE, and the caller says so
    rather than inventing an agreement [[measuring-tool-must-not-guess]].

    ★ It reads the FOOTER, not the banner, because the footer is the fixed-point sentence — the
    one figure in the file that is the size of the file containing it, so its unit word is the
    unit the whole artefact was built in, never a quoted figure from GM's own prose.
    """
    m = _STAMP_RE.search(text or "")
    if not m:
        return None
    return _TIER_BY_UNIT_WORD.get(m.group(1).strip())

# ---------------------------------------------------------------------------------------------
# ★ s125-D1 (DAVE, RULED #125, ENACTED #126) — THE BUILD-STEP COUNT IS GENERATED, NOT TYPED.
#
# The chain banner carried `"ALL 75 STEPS ASKED AND GREEN (#62)"` as PROSE. It was true when
# written (`18c7789`, len(STEPS) == 75) and went false silently as steps were added; #125 measured
# disk at 98 and Dave ruled the figure becomes GENERATED **explicitly over a third re-stamp**.
# ★ The class: *a claim that was true when written, went false, and nothing re-checks it*
# [[no-gate-parses-the-artefact]]. A fourth re-stamp would have re-armed it.
#
# ⛔ TWO NUMBERS, NOT ONE — and conflating them is how the re-stamp would have LIED. The live
# count (98) and the count the green verdict actually covered (75, at `VERDICT_SHA`) are different
# facts. Substituting only the live number would have published *"ALL 98 STEPS ASKED AND GREEN
# (#62)"* — a sentence no one ever measured, manufactured by the very fix meant to stop
# manufactured claims. So BOTH ends are read from an AST, and the SHORTFALL is computed.
#
# ★ WHY THE SUBSTITUTION HAPPENS IN `_capture_gate.chain_parts` AND NOT HERE, despite the ruling
# naming this file: `chain_parts` is THE ONE SLICER — `read_chain_tk` measures exactly what it
# returns and this module writes exactly what it returns, so text injected downstream of it would
# be written-but-not-measured. That is the second-consumer drift #41 extracted the slicer to make
# impossible, and it is the same reason `dofirst_index` is composed there rather than here (see
# its comment at `_capture_gate.chain_parts`). The READER lives here, as ruled; the SLICER calls
# it. [[instruction-right-cause-wrong]]
#
# ⚠ REFUSES, NEVER GUESSES. No git, no `_build_all.py`, no `STEPS` assignment, a non-literal list
# — every one of them yields a NAMED refusal that is published in the chain as an UNMEASURED gap.
# A declared gap passes; a silent one fails. [[measuring-tool-must-not-guess]]
BUILD_VERDICT_MARK = "{{BUILD_VERDICT}}"

# The commit whose message is "Ask all 75 steps (75 pass · 0 FAIL) …" — the sole provenance of
# the "#62 green" claim. ⚠ This SHA is typed, and that is deliberate: it names a fixed historical
# event, so it cannot go stale the way a COUNT does. Everything derived FROM it is measured.
VERDICT_SHA = "18c7789"


class BuildStepCountError(Exception):
    """Raised by `_steps_in` when a step count cannot be READ. Never returns a number."""


def _steps_in(source, where):
    """`len(STEPS)` and the number of DISTINCT labels, from `_build_all.py` source, via AST.

    ⚠ Distinct labels are returned alongside the length because #125's probe closed the 75-vs-97
    question by showing they were 1:1 at BOTH ends — same object, stale by N. A generator that
    published only `len()` could not tell a genuine growth from a duplicated row.
    """
    import ast
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise BuildStepCountError(f"{where} does not parse ({e})")
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(getattr(t, "id", None) == "STEPS" for t in node.targets):
            continue
        if not isinstance(node.value, (ast.List, ast.Tuple)):
            raise BuildStepCountError(
                f"{where}: STEPS is not a literal list/tuple ({type(node.value).__name__}) — "
                f"its length is not statically knowable, so it is NOT counted")
        labels = [e.elts[0].value for e in node.value.elts
                  if isinstance(e, (ast.Tuple, ast.List)) and e.elts
                  and isinstance(e.elts[0], ast.Constant)]
        return len(node.value.elts), len(set(labels))
    raise BuildStepCountError(f"{where}: no top-level `STEPS = [...]` assignment found")


def build_steps_now(repo=ROOT):
    """(n, distinct, None) for the WORKING TREE, or (None, None, reason)."""
    path = os.path.join(repo, "knowledge", "_build_all.py")
    if not os.path.exists(path):
        return None, None, f"`{path}` is absent"
    try:
        with open(path, encoding="utf-8") as f:
            return (*_steps_in(f.read(), "_build_all.py (working tree)"), None)
    except BuildStepCountError as e:
        return None, None, str(e)


def build_steps_at(sha, repo=ROOT):
    """(n, distinct, None) for `_build_all.py` AS OF `sha`, or (None, None, reason)."""
    import subprocess
    try:
        out = subprocess.run(["git", "show", f"{sha}:knowledge/_build_all.py"],
                             cwd=repo, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError) as e:
        return None, None, f"git unavailable ({e})"
    if out.returncode != 0:
        return None, None, (f"`git show {sha}:knowledge/_build_all.py` failed rc="
                            f"{out.returncode} ({out.stderr.strip()[:120]})")
    try:
        return (*_steps_in(out.stdout, f"_build_all.py @ {sha}"), None)
    except BuildStepCountError as e:
        return None, None, str(e)


def build_verdict_line(repo=ROOT):
    """The GENERATED build-verdict sentence for the chain banner. NEVER a typed count.

    ⚠ Width-stable with respect to the fixed point: nothing here depends on the file-size figure
    `build()` is solving for, so this cannot induce the 2-cycle that `build()` refuses on.
    """
    now, now_lab, why_now = build_steps_now(repo)
    if now is None:
        return (f"⛔ **BUILD VERDICT: UNMEASURED — the build-step count could not be read "
                f"({why_now}).** Not defaulted to a number; `s125-D1` makes this figure "
                f"GENERATED, and a generator that guesses is the defect it replaced.")
    dup = "" if now == now_lab else f" ⚠ **{now - now_lab} DUPLICATE label(s)**"
    then, _then_lab, why_then = build_steps_at(VERDICT_SHA, repo)
    if then is None:
        return (f"⛔ **BUILD VERDICT: {now} steps on disk{dup} — GENERATED from "
                f"`_build_all.py`'s AST (`s125-D1`). The #62 green verdict's COVERAGE is "
                f"UNMEASURED ({why_then}) — a declared gap, not a pass.**")
    gap = now - then
    if gap <= 0:
        return (f"⛔ **BUILD VERDICT: {now} steps on disk{dup}; #62's green verdict covered "
                f"{then} (`{VERDICT_SHA}`) — GENERATED at both ends (`s125-D1`).**")
    return (f"⛔ **BUILD VERDICT: {then} of {now} steps green (#62, `{VERDICT_SHA}`) — "
            f"{gap} steps have NEVER been in a green verdict.**{dup} Both counts GENERATED "
            f"from `_build_all.py`'s AST at each end; the shortfall is computed (`s125-D1`).")


# ⚠ #47 — THE COST ASYMMETRY, AND IT DECIDES WHERE PROSE GOES IN THIS MODULE.
# Comments in this `.py` are read by whoever maintains the generator: a handful of times, by
# choice. Text inside `BANNER` / `FOOTER` is read by EVERY cold session, forever, and is charged
# against the cap those sessions are trying to stay under. ⇒ **be generous here, miserly there.**
# ★ Measured, this session: the first draft of the re-pointed footer explained the ruling, the
# unit change and the history in the FILE. It cost **+107 tape on every future cold read** — the
# fix growing the region it exists to govern ([[gate-inside-the-growth-loop]]), caught only
# because the fixed point now reports slice-vs-wrapper separately. The narration moved to the
# banner and the ledger, where it is retrieval and nobody pays for it at boot. What stayed in the
# footer is the one thing a cold reader cannot get elsewhere: WHICH UNIT THE NUMBER IS IN.
# ⚠ A transitional note ("the old figure was the slice") was drafted here and REMOVED for the
# same reason — it is a claim with an expiry date, sited in the most expensive text in the repo.

# ★ #47 — HOW MANY TIMES `build()` MAY RE-RENDER BEFORE IT REFUSES.
# The footer publishes the size of the file the footer is inside, so the figure is SELF-
# REFERENTIAL and cannot be written in one pass. #46 named the problem without seeing it was a
# blocker: *"a self-referential delta cannot be written before the edit that changes it."*
# The resolution is a fixed point — render, measure the WHOLE text, re-render with that number,
# repeat until the stamped figure equals the measured one. It converges on pass 2 or 3 whenever
# the digit count is stable, which it is either side of a comma boundary.
# ⚠ NOTHING THAT VARIES PER PASS MAY APPEAR IN `FOOTER`. The first draft of this stamped the pass
# COUNT into the file — which changes the text on every pass, so the thing being measured moved
# with the measurement and convergence was never guaranteed. The pass count is reported in the
# `detail` string instead, where it is observable without being self-referential. ★ The general
# rule, and it is the whole reason a fixed point works here: the ONLY per-pass variable in the
# rendered text is the figure itself.
# ⚠ IT CAN OSCILLATE. Crossing a width boundary (999→1,000) changes the rendered length, which
# can change the measurement back. That is a 2-cycle, and this module REFUSES a 2-cycle rather
# than picking the prettier half — same posture as every other failure path here. A stamp that
# silently picked one end of an oscillation would be exactly the "confident blank" the module
# docstring refuses, wearing a number instead of a blank.
MAX_FIXED_POINT_PASSES = 8


def state_block():
    """The GENERATED open-work section (#88). Rendered from `_state.json`, never from prose.

    ★ WHY THIS IS ADDITIVE AND NOT YET A SWAP. The hand-authored presence index still sits in
    `GOOD-MORNING.md` and still reaches the chain through `cg.chain_parts`. Removing it in the
    same motion that adds this would be a cut before a probe proved the facts live elsewhere,
    which is the one thing [[home-by-addition-then-cut]] forbids — and it would do it on the boot
    path, where a mistake costs every future session. So: ADD now, verify against the prose for
    the two drill passes (#87-D1, N=2), CUT at the swap. The duplication is the declared price of
    doing it in the right order, and it is small and bounded because this block prints ids and
    counts, not bodies.

    ⛔ REFUSES rather than guesses, inheriting `build()`'s posture. A boot path that renders an
    empty-but-plausible worklist because a store failed to load hands a cold session a confident
    blank — strictly worse than a named refusal [[a-crash-is-not-a-fail]].

    ⚠ Width-stable by construction: nothing here depends on the file-size figure the fixed point
    is solving for, so this block cannot induce the 2-cycle that `build()` refuses on.
    """
    try:
        import _state
    except Exception as e:                                    # pragma: no cover - import guard
        return ("\n\n---\n\n> ⛔ **OPEN WORK: NOT RENDERED** — `_state.py` did not import "
                f"({e}). This is a REFUSAL, not an empty worklist.\n")
    try:
        doc = _state.load()
        ok, fails, notes = _state.check(doc)
        c = _state.counts(doc)
    except _state.StateError as e:
        return ("\n\n---\n\n> ⛔ **OPEN WORK: NOT RENDERED** — the store refused to load "
                f"({e}). NOT read as zero items.\n")

    ls = _state.live(doc)
    dave = [i for i in ls if i["owner"] == "dave"]
    mine = [i for i in ls if i["owner"] == "claude"]

    def ids(seq):
        return " · ".join(f"`{i['id']}`" for i in seq)

    out = [
        "\n\n---\n\n",
        "## ⬛ OPEN WORK — GENERATED from `_state.json`. **The row count IS the count.**\n\n",
        f"> **{c['total']} items · {c['live']} live · {c['by_owner']['dave']} Dave's · "
        f"{c['by_owner']['claude']} mine · {c['conditioned']} carry a stated close condition · "
        f"**{c['unconditioned']} UNCONDITIONED**.**\n",
        "> *Every figure in this block is computed from the store at generation time. No number "
        "here was typed by anyone — that is the point of it (#86 measured a typed inventory of "
        "\"118 markers\" against a real ~40; #85's \"95 slots / 84 distinct\" is not reproducible "
        "by any probe in this repo).*\n",
    ]
    if c["unconditioned"]:
        out.append(
            f"> ⚠ **DECLARED DEBT — {c['unconditioned']} inherited items have NO close "
            f"condition and therefore cannot close.** They are exempt as a FROZEN set "
            f"(`_state.LEGACY_IDS`, size {len(_state.LEGACY_IDS)}) which may only shrink; a NEW "
            f"item is refused without one. **Each needs Dave's word — an agent inventing a "
            f"close condition for his open work is the same overreach as inventing his "
            f"ruling.**\n")
    # ⛔ The heading is COMPUTED, not asserted. It read "each with a ratified `closes_when`" for
    # exactly one render, while five of its own rows printed "none stated" directly underneath —
    # a summary line contradicted by the data it summarises, on the boot path, in the session
    # whose entire subject is that typed claims rot. Caught by reading the artefact, which is the
    # only thing that ever catches it [[enactment-register-adr-0016]].
    n_cond = sum(1 for i in dave if i["closes_when"])
    n_un = len(dave) - n_cond
    out.append(f">\n> **DAVE'S ({len(dave)}) — {n_cond} with a ratified `closes_when`, "
               f"{n_un} with NONE:**\n")
    for i in sorted(dave, key=lambda x: (x["closes_when"] is None, x["id"])):
        cw = i["closes_when"] or "⛔ **none stated — cannot close until you name one**"
        out.append(f"> - `{i['id']}` **{i['title']}** — *closes when:* {cw}\n")
    out.append(f">\n> **MINE ({len(mine)}), ids only — bodies are in the store, not here:** "
               f"{ids(mine)}\n")
    out.append(f">\n> ⚠ store gate: **{'PASS' if ok else 'FAIL'}**"
               + ("" if ok else f" — {len(fails)} failure(s): {fails[0]}")
               # #221/F6 — resolved, not typed: `_state.py` sits beside this script in the
               # repo and one level up (`memento-package/`) in a shipped pack.
               + ". Bodies, conditions and provenance: `%s`.\n"
                 % _cmd("_state.py", os.path.dirname(HERE)))
    return "".join(out)


def build(repo=ROOT):
    """Return `(text, detail)` for the chain file, or `(None, reason)` on refusal.

    ⚠ REFUSES rather than guesses, inheriting `chain_parts`' posture: a generator that emits an
    empty-but-plausible chain on a parse failure hands a cold session a confident blank, which is
    strictly worse than no file at all. Every failure path returns a REASON.

    ★ #59 — REFUSES BEFORE MEASURING ANYTHING IF THE INSTRUMENT ITSELF IS DEGRADED, and this is
    a DISTINCT refusal from every other one below it. Every size figure this function's fixed
    point produces — `gm_tk`, `slice_tk`, the footer's own `file_tk` — comes from
    `cg.measure_tokens(...)[0]`; every call site here and in `chain_parts`/`read_chain_tk`
    discards `[1]`, the method, even though `measure_tokens` DECLARES it. So when tiktoken is
    unavailable (a fresh sandbox with no pip state — `_capture_gate.py`'s own M6 note: "vanished
    TWICE inside 24 hours") and the byte-divisor ESTIMATE stands in for it, this function
    produces numbers that disagree with a tiktoken-measured `_CHAIN.md` for a reason that has
    nothing to do with GOOD-MORNING.md or _LIVE-STATE.md changing — and the old code handed that
    straight to `check()`'s byte comparison, which could only ever call it "_CHAIN.md is STALE".
    MEASURED, this session (#59): forcing the ESTIMATE fallback against a `_CHAIN.md` that
    `--check` had JUST called fresh, with git status clean and not one byte of GM/LS touched in
    between, flips the verdict to STALE — see this file's `selftest`, the #59 bites, for the
    reproduction and `_capture_gate.measurement_degraded` for the instrument-health probe.
    ⇒ A degraded instrument is refused HERE, before any measuring happens, so neither `check()`
    nor `write()` downstream ever gets to hand out a content verdict — PASS or FAIL — that was
    actually built on a guess. Both callers already print whatever reason `build()` returns on a
    `None`, so this refusal reaches them for free, worded distinctly from "STALE" and from
    "MISSING", with no new branch needed in either.
    """
    try:
        import _capture_gate as cg
    except Exception as e:                                    # pragma: no cover - import guard
        return None, f"_capture_gate unavailable ({e}) — chain NOT generated, not assumed empty"

    if cg.measurement_degraded():
        return None, (
            "the token measurer is running on the ESTIMATE fallback, not the real tiktoken "
            "encoder (tiktoken unavailable, or its encoding file could not be loaded, in this "
            "process) — chain NOT generated/verified. This is a MEASUREMENT REFUSAL, not a "
            "content verdict in either direction: every size figure build() would bake into "
            "the file is measured on the wrong instrument, so a byte comparison right now would "
            "be noise wearing a verdict, whichever way it fell. Re-run once tiktoken is "
            "installed and can reach openaipublic.blob.core.windows.net (the cl100k_base "
            "encoding file) — see _capture_gate.measure_tokens / measurement_degraded."
        )

    gm_path = os.path.join(repo, "GOOD-MORNING.md")
    if not os.path.exists(gm_path):
        return None, "GOOD-MORNING.md is missing — nothing to generate a chain from"
    with open(gm_path, encoding="utf-8") as f:
        gm_text = f.read()
    gm_lines = gm_text.splitlines()

    gm_part, delta, how = cg.chain_parts(repo, gm_lines)
    if gm_part is None:
        return None, how

    gm_tk = cg.measure_tokens(gm_text)[0]
    slice_tk, chain_detail = cg.read_chain_tk(repo, gm_lines)
    if slice_tk is None:
        return None, chain_detail

    # ---- #73: THE TITLE, FIRST (#72 (f), enacted on Dave's word; he asked to see the generator
    # first — the change is this block and nothing else). The forward title lapsed three sessions
    # running and #72's diagnosis was POSITION, not absence: it sat below six banner paragraphs.
    # So the generated chain now opens with it, above the banners. The #N assertion below catches
    # a STALE title (a wrap that forgot to mint the next one); it canNOT catch a skipped wrap —
    # said plainly here because overselling a gate is how greens stop meaning anything.
    # ⚠ The title also still appears inside gm_part (the header slice is VERBATIM by contract);
    # the ~60-tape duplication is the price of position and is declared, not hidden.
    import re
    m_title = re.search(r"\*\*TITLE THE NEXT CHAT →\*\*\s*(`[^`\n]+`)", gm_text)
    m_latest = re.search(r"##\s*★\s*LATEST\s*—[^\n]*?#(\d+)", gm_text)
    title_block = ""
    if m_title:
        title = m_title.group(1)
        t_n = re.search(r"#(\d+)", title)
        l_n = int(m_latest.group(1)) if m_latest else None
        if t_n and l_n is not None:
            t_i = int(t_n.group(1))
            if t_i != l_n + 1:
                return None, (
                    f"the NEXT-CHAT title names #{t_i} but ★ LATEST is #{l_n} — a wrap must "
                    f"hand the next session its own title (#{l_n + 1}). This is the STALE-title "
                    f"check (#72 (f)); it cannot see a skipped wrap. Fix the `TITLE THE NEXT "
                    f"CHAT` line in GOOD-MORNING.md and regenerate.")
            title_block = (
                f"> **YOU ARE #{t_i}. TITLE THIS CHAT →** {title}\n"
                f"> *(read it back in your opener — the chat half of the ritual is ungateable, "
                f"which is why this line is FIRST)*\n\n---\n\n")
        else:
            title_block = f"> **TITLE THIS CHAT →** {title}\n\n---\n\n"

    body = gm_part if delta is None else gm_part + "\n\n---\n\n" + delta
    body = title_block + body + state_block()
    # ⚠ Every published figure here is MEASURED with the gate's own tokenizer, never derived from
    # line counts or character lengths. A COUNT IS NOT A MEASUREMENT — the standing lesson.
    gm_part_tk = cg.measure_tokens(gm_part)[0]
    _u = unit_word(cg)
    # #221/F6: the wrapper's paths and id examples are RESOLVED in the tree this run is in.
    # `gen_cmd_bare` is the invocation, minus the `python3 `, because the DO-NOT-HAND-EDIT
    # comment names a file rather than giving a command.
    head = BANNER.format(gm_tk=gm_tk, unit=_u,
                         gen_cmd_bare=_cmd(os.path.basename(__file__)).replace("python3 ", ""),
                         search_cmd=_cmd("_memento_search.py"),
                         retrieval_ids=_retrieval_ids())

    def render(file_tk):
        foot = FOOTER.format(file_tk=file_tk, gm_tk=gm_tk, unit=_u,
                             chain_pct=100.0 * file_tk / gm_tk if gm_tk else 0.0)
        return head + "\n" + body + foot

    # ---- THE FIXED POINT (#47, Dave's ruling on open 16 (a)+(c)).
    # Seeded from the SLICE, which is a strict LOWER BOUND: the wrapper only ever adds text, so
    # the first render can never overshoot. Each pass stamps the previous measurement and
    # re-measures the whole rendered file; convergence is the stamped figure EQUALLING the
    # measured one, which is the only state in which the sentence in the footer is true.
    guess, seen = slice_tk, {}
    for n in range(1, MAX_FIXED_POINT_PASSES + 1):
        text = render(guess)
        # ⛔ CORRECTED AT SOURCE #83 — THE METHOD NOW TRAVELS WITH THE NUMBER, as `measure_tokens`
        # has DECLARED it should since it was written. This call site read `[0]`, discarding the
        # method, and then hard-coded the word `tape` into every string below. Since #82-D1 that
        # number is REAL, so this reader was publishing the RETIRED unit's name for a figure the
        # chain's own footer publishes as `real` — the SAME 11,032, two units, two files. The
        # docstring at :153-157 flagged the discard; nobody flagged that the LABEL was a lie.
        # ★ Not relabelled to a hard-coded 'real' either: that would claim a tier the fallback
        # cannot deliver. The label is now whatever was actually used. [[measure-dont-convert-units]]
        measured, how = cg.measure_tokens(text)
        if measured == guess:
            return text, (f"{chain_detail} · FILE {measured:,} {how} = slice {slice_tk:,} + "
                          f"wrapper {measured - slice_tk:,} · fixed point in {n} pass(es)")
        if measured in seen:
            # ⚠ A 2-cycle. REFUSE — do not pick the prettier end. Both ends are false: whichever
            # is stamped, the file's real size is the other one. This is the "cheerful zero"
            # class wearing a plausible number, and it is worse than a blank because it looks
            # measured. The remedy is a width-stable footer, and it is a code fix, not a retry.
            return None, (f"_CHAIN.md figure does NOT converge — it oscillates between "
                          f"{measured:,} and {guess:,} {how} (pass {seen[measured]} vs {n}). The "
                          f"footer's rendered width changes with the figure it publishes. Chain "
                          f"NOT generated: a stamp picked from one end of an oscillation is a "
                          f"confident wrong number, which is worse than no file.")
        seen[measured], guess = n, measured
    return None, (f"_CHAIN.md figure did not settle in {MAX_FIXED_POINT_PASSES} passes "
                  f"(last {guess:,} tape). Chain NOT generated, not stamped with a guess.")


def write(repo=ROOT):
    text, detail = build(repo)
    if text is None:
        print(f"  ✗ _CHAIN.md NOT generated — {detail}")
        return 1
    out = os.path.join(repo, OUT_NAME)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        import _capture_gate as cg
        tk, how = cg.measure_tokens(text)          # #83: the method travels with the number
        print(f"  ✅ {OUT_NAME}: {tk:,} {how} · {detail}")
    except Exception:                                          # pragma: no cover
        print(f"  ✅ {OUT_NAME} written · {detail}")
    return 0


def check(repo=ROOT):
    """Determinism check — the `gen_canon_components` pattern.

    ⚠ Compares CONTENT, never mtime. The retrieval index was bitten by exactly this (#32: it
    served a two-session-old record because freshness was judged by timestamp), and a chain file
    is the single artefact where a stale copy does the most damage — it is the FIRST thing read
    and the reader has no reason to doubt it.
    """
    text, detail = build(repo)
    if text is None:
        print(f"  ✗ _CHAIN.md check FAILED — {detail}")
        return 1
    out = os.path.join(repo, OUT_NAME)
    if not os.path.exists(out):
        # #221/F6 — the refusal names the command IN THIS TREE, resolved, never `knowledge/…`.
        print(f"  ✗ {OUT_NAME} is MISSING — run `{_cmd(os.path.basename(__file__))}` "
              f"and stage it")
        return 1
    with open(out, encoding="utf-8") as f:
        have = f.read()

    # ---- #173 → #183: COULD-NOT-ASK, and it is asked BEFORE the byte comparison ON PURPOSE.
    # A tier divergence makes EVERY size figure in `text` differ from `have` for a reason that
    # has nothing to do with GOOD-MORNING.md or _LIVE-STATE.md changing. If the byte compare ran
    # first it would always win, and the honest answer would be unreachable — the same ordering
    # #59 established for the degraded case, one tier out. See `stamped_tier()` above.
    try:
        import _capture_gate as _cg_tier
        live_tier = _cg_tier.measurement_tier()
    except Exception as ex:                                # pragma: no cover - import guard
        return cna.refuse(OUT_NAME, f"the tier probe itself is unreachable ({ex}); no "
                          f"freshness verdict is offered in either direction.")
    stamp = stamped_tier(have)
    if stamp is None:
        return cna.refuse(OUT_NAME, f"the committed file carries NO READABLE UNIT STAMP "
                          f"in its footer fixed-point sentence, so the tier it was measured in "
                          f"cannot be compared with this environment's ({live_tier}). This is a "
                          f"REFUSAL, not a content verdict: regenerate with "
                          f"`{_cmd(os.path.basename(__file__))}`.")
    if stamp != live_tier:
        return cna.refuse(OUT_NAME, f"MEASUREMENT REFUSAL, NOT A FRESHNESS "
              f"VERDICT IN EITHER DIRECTION. The "
              f"committed file is stamped `{_UNIT_WORDS.get(stamp, stamp)}` ({stamp}); the only "
              f"tier reachable in THIS environment is `{_UNIT_WORDS.get(live_tier, live_tier)}` "
              f"({live_tier}). Every size figure would differ for that reason alone, so a byte "
              f"comparison right now would be noise wearing a verdict, whichever way it fell. "
              f"⚠ `real` is reachable ONLY via `API-KEY.txt` or `knowledge/.token-cache.json` "
              f"and BOTH ARE GITIGNORED (#173, proven by single-variable isolation) — so a bare "
              f"checkout can never agree with a `real` stamp. Give this environment the same "
              f"measurer, or re-ask where it is reachable. The freshness of {OUT_NAME} is "
              f"UNKNOWN and is reported as unknown rather than guessed.")

    if have != text:
        print(f"  ✗ {OUT_NAME} is STALE — it does not match GOOD-MORNING.md / _LIVE-STATE.md as "
              f"they now stand, so a cold session would read a PREVIOUS session's record as if it "
              f"were current. Run `{_cmd(os.path.basename(__file__))}` and stage the result.")
        return 1
    print(f"  ✅ {OUT_NAME} is FRESH — byte-matches the live chain · {detail}")
    return 0


def selftest():
    """Bites. Selftests are BUILD STEPS here — a gate that ships without one is documentation."""
    import tempfile
    import shutil
    fails = []

    def bite(what, ok):
        print(f"    {'✓' if ok else '✗'} {what}")
        if not ok:
            fails.append(what)

    text, detail = build(ROOT)
    bite("generates against the live repo (no refusal on a healthy tree)", text is not None)

    if text is not None:
        import _capture_gate as cg
        gm_lines = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().splitlines()
        gm_part, delta, _how = cg.chain_parts(ROOT, gm_lines)
        chain_tk, _d = cg.read_chain_tk(ROOT, gm_lines)
        gm_tk, gm_tier = cg.measure_tokens(open(os.path.join(ROOT, "GOOD-MORNING.md"),
                                                encoding="utf-8").read())

        bite("carries the GM header+LATEST term VERBATIM (not a summary of it)", gm_part in text)
        bite("carries the LS ⏱ LATEST delta VERBATIM", delta is None or delta in text)
        # ★ The point of the whole exercise: the file must actually be small. A chain file that
        #   is not much smaller than GM buys nothing and would be worse than nothing, because it
        #   adds a second thing to keep fresh. Assert the CUT, not just the content.
        # ⛔ #219 — THE UNIT IN THIS LABEL WAS A HARDCODED LITERAL, AND IT WAS OFTEN A LIE.
        # Both figures come from `cg.measure_tokens`, which returns whatever tier THIS environment
        # can reach — `real` where a key or the token cache is present, the estimate tier in a bare
        # checkout. The label said `tape` unconditionally, so a locally-measured `real` pair was
        # printed under the wrong unit and the two environments' readings looked like the same
        # measurement disagreeing. Naming a figure with a unit it was not measured in is the ds-021
        # defect this very selftest asserts against the footer three bites below
        # [[measure-dont-convert-units]]. The tier is now READ, never assumed, and the ratio is
        # printed beside the floor so the margin is legible instead of re-derived.
        # ⚠ WHAT THIS DOES NOT DO, DELIBERATELY: the `0.40` and the assertion are UNTOUCHED. The
        # bite is genuinely RED at #219 and it is red in EVERY reachable unit — measured on the
        # same bytes at HEAD 04bd5f0: real 45.56%, cl100k tape 45.83%, chars 46.10%, a spread of
        # 0.27pp. So this is NOT the #173 stale-in-CI class and must not be dressed as one: a
        # COULD-NOT-ASK refusal here would hide a real red behind an environment excuse, which is
        # the #173 defect run backwards. Why it is red — and what to do about a ratio between two
        # files that grow on different cycles — is a RULING, written up for Dave, not patched here.
        out_tk, out_tier = cg.measure_tokens(text)
        ratio = out_tk / gm_tk if gm_tk else float("inf")
        bite(f"is materially smaller than GOOD-MORNING.md ({out_tk:,} vs {gm_tk:,} "
             f"{unit_word(cg)}, {ratio:.1%} of it, floor <40%; tier measured, not assumed: "
             f"{out_tier})",
             out_tk < 0.40 * gm_tk)
        # ★ #219 — THE RATIO'S PRECONDITION, ASSERTED RATHER THAN ASSUMED. A ratio is only a
        # measurement if BOTH sides came off the SAME measurer; a numerator in `real` over a
        # denominator in the estimate tier is a number with no unit, and it would read as a
        # ~1.6× swing that nothing in the output would explain. Nothing compares them today —
        # which is exactly why the claim needs a bite rather than a comment [[measure-dont-convert-units]].
        bite(f"BOTH SIDES OF THE RATIO ARE ON ONE MEASURER — chain `{out_tier}` vs "
             f"GOOD-MORNING `{gm_tier}`, so the percentage above has a unit",
             out_tier == gm_tier)
        # ★ #47 — RE-POINTED from the SLICE to the FILE, and STRENGTHENED while it was open.
        # The old bite asserted only that *a* measurement appeared in the text, which the slice
        # figure satisfied for three sessions while the file went unmeasured — the bite passed
        # throughout the defect open 16 records. This asserts the FIXED-POINT INVARIANT instead:
        # the stamped figure IS the size of the file it is stamped in. That is a property no
        # hand-maintained stamp can hold, and it is the whole point of the re-point.
        bite("STAMP IS EXACT — the published figure equals this file's own measured size",
             f"**{cg.measure_tokens(text)[0]:,} {unit_word(cg)}" in text)
        bite("published figure is the FILE, not the slice — the two differ and the file is bigger",
             cg.measure_tokens(text)[0] > chain_tk and f"**{chain_tk:,} {unit_word(cg)}" not in text)
        bite("footer NAMES THE UNIT — a bare token count is a defect (ds-021)",
             "the unit is THE WHOLE FILE" in text and "wrapper included" in text)
        bite("says GENERATED / DO-NOT-HAND-EDIT at the very top (line 1)",
             text.splitlines()[0].lstrip().startswith("<!-- GENERATED"))
        bite("tells the reader NOT to open GOOD-MORNING.md to check",
             "Do NOT now open" in text)
        bite("names retrieval as the door for everything else", "_memento_search.py" in text)
        # ---- s125-D1 (#126): THE BUILD-STEP FIGURE IS GENERATED, AND THIS RE-CHECKS IT.
        # ★ These bites exist because the number they guard went false in silence for ~50
        # sessions while every gate in the repo stayed green: the `size:` stamp audit matched a
        # REGEX, and no gate parsed the prose beside it [[no-gate-parses-the-artefact]].
        # ⚠ The second bite is the load-bearing one — it does not check that *a* number is
        # present (the old defect satisfied that for 50 sessions), it re-derives `len(STEPS)`
        # from disk AT TEST TIME and asserts the chain publishes THAT. It is the answer to
        # "what re-checks this?", which is the question the whole class turns on.
        bite("the {{BUILD_VERDICT}} marker NEVER leaks into the chain unrendered",
             "{{BUILD_VERDICT}}" not in text)
        _n, _lab, _why = build_steps_now(ROOT)
        # ⛔ #221/F10 — THE ENVIRONMENT SPLIT, DECLARED. `_build_all.py` is this repo's build
        # runner; it is deliberately NOT on the pack's ship list. So in a Gumdrop project this
        # bite could never pass, no matter what the designer did — and `memento-package/README.md`
        # tells them "All bites should pass". A gate that cannot pass in one environment is a
        # defect in the gate, not a verdict about the tree [[gate-cannot-pass-in-one-environment]].
        # ⚠ Declared, never silent: in a pack the bite is REPLACED by a named line saying the
        # subject is absent BY DESIGN. In this repo an absent `_build_all.py` is still a failure,
        # exactly as before — the arm below is the one that keeps that true.
        if _n is None and _in_a_pack():
            bite("build-step figure: NOT APPLICABLE in a pack — `_build_all.py` is this design "
                 "system's own build runner and does not ship (declared, not skipped)", True)
        elif _n is None:
            bite(f"build-step count is readable from _build_all.py's AST ({_why})", False)
        else:
            bite(f"BUILD-STEP FIGURE IS RE-DERIVED AND MATCHES DISK ({_n} steps, measured now)",
                 f" {_n} steps" in text or f"of {_n} steps" in text)
            bite("no DUPLICATE step labels are being counted as growth", _n == _lab,
                 ) if _n != _lab else bite("step labels are 1:1 with rows (no duplicates)", True)
        # ⛔ REFUSAL BITE — the figure must go UNMEASURED, by name, rather than default to a
        # number. A measuring tool that guesses is the defect this replaced.
        try:
            _steps_in("NOT_STEPS = [1, 2, 3]\n", "<bite>")
            bite("an absent STEPS assignment REFUSES BY NAME (never returns a count)", False)
        except BuildStepCountError as _e:
            bite("an absent STEPS assignment REFUSES BY NAME (never returns a count)",
                 "no top-level" in str(_e))
        try:
            _steps_in("STEPS = list(x for x in [])\n", "<bite>")
            bite("a NON-LITERAL STEPS refuses rather than counting something else", False)
        except BuildStepCountError as _e:
            bite("a NON-LITERAL STEPS refuses rather than counting something else",
                 "not a literal" in str(_e))

        # ---- #73 (f): the title rides ABOVE the banners, and a stale title refuses.
        bite("TITLE BLOCK IS FIRST — above the verbatim GM slice (position was the defect)",
             "TITLE THIS CHAT" in text and text.index("TITLE THIS CHAT") < text.index(gm_part[:40]))

    # determinism: two builds of an unchanged tree are byte-identical
    t2, _ = build(ROOT)
    bite("DETERMINISTIC — two builds of an unchanged tree are byte-identical", text == t2)

    # --check must FAIL on a stale file, not pass it. The failure class that matters most.
    tmp = tempfile.mkdtemp()
    try:
        for n in ("GOOD-MORNING.md", "_LIVE-STATE.md"):
            src = os.path.join(ROOT, n)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(tmp, n))
        write(tmp)
        bite("--check PASSES on a freshly generated file", check(tmp) == 0)

        # ---- #59: a DEGRADED instrument must REFUSE, and must NEVER be reported as staleness.
        # This is the reproduction of the #58 flicker: same bytes on disk, same GM/LS content,
        # zero real drift — the check flipped from FRESH to STALE anyway because the MEASURER
        # changed underneath it. Forces the ESTIMATE fallback with the same technique
        # `_capture_gate.py`'s own M6 bite uses (`sys.modules["tiktoken"] = None` +
        # `CAPTURE_GATE_NO_HEAL=1`), against THIS SAME tmp tree one line after `check(tmp)` just
        # called it fresh with a healthy tiktoken — so any refusal below can only be attributed
        # to the instrument, never to content.
        import io
        import contextlib
        import _capture_gate as cg
        # ⛔ #82 — `CAPTURE_GATE_NO_REAL` MUST BE SET TOO, AND THIS IS THE THIRD SITE OF ONE
        # CLASS. The idiom "hide tiktoken, therefore the measurer is degraded" was sound until
        # #82-D1 put a REAL tier ABOVE the whole cascade: on a machine with a key, hiding
        # tiktoken now degrades nothing and this arm silently stops reaching the refusal it
        # exists to prove. It FAILED here rather than passing by bypass, which is the bite
        # working — but the two sibling arms in `_capture_gate.py` (M6, #59) needed the same
        # repair, so the rule is general: **forcing a fallback now means suppressing EVERY tier
        # above it, not just the one you were thinking of.** [[scope-blindness-gate-vocabulary]]
        _envs = ("CAPTURE_GATE_NO_HEAL", "CAPTURE_GATE_NO_REAL")
        saved_envs = {k: os.environ.get(k) for k in _envs}
        for _k in _envs:
            os.environ[_k] = "1"
        sys.modules["tiktoken"] = None
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                degraded_rc = check(tmp)
            degraded_out = buf.getvalue()
            bite("--check on a degraded instrument still exits non-zero (refuses, not a silent "
                 "pass)", degraded_rc == 1)
            bite("--check's message does NOT call it STALE — that misnames a measurement "
                 "problem as a content problem (the #58 defect, reproduced here)",
                 "STALE" not in degraded_out.upper())
            bite("--check's message names the DEGRADED INSTRUMENT so the cause is legible",
                 "ESTIMATE" in degraded_out)
        finally:
            del sys.modules["tiktoken"]
            for _k, _v in saved_envs.items():
                os.environ.pop(_k, None) if _v is None else os.environ.__setitem__(_k, _v)
        # instrument restored — the SAME tree (untouched by any of the above) must report FRESH
        # again, proving the refusal above was the instrument and not a side effect on the tree.
        bite("instrument restored — the SAME fresh tree reports FRESH again, unharmed",
             check(tmp) == 0)

        # ---- #173 → #183: THE COULD-NOT-ASK CLAUSE, MUTATION-PROVEN AT THE STAMP.
        # ★ The mutation is on the STAMP, not on the environment, and that is deliberate. Driving
        # this arm by forcing the fallback would only bite on a machine where `real` is reachable
        # in the first place — i.e. the arm would be silently unreachable in exactly the
        # environment the defect lives in, which is the very shape #173 found
        # [[gate-cannot-pass-in-one-environment]]. Rewriting the committed file's own unit word to
        # a DIFFERENT tier's word reproduces the divergence identically and bites everywhere.
        # It also proves the ORDERING: the mutated file is byte-different too, so if the byte
        # compare ran first this arm would read STALE and the honest answer would be unreachable.
        chain_p = os.path.join(tmp, OUT_NAME)
        fresh_text = open(chain_p, encoding="utf-8").read()
        live_stamp = stamped_tier(fresh_text)
        bite("the freshly written chain carries a READABLE unit stamp (the clause has something "
             "to compare — an unreadable stamp would make the arm below vacuous)",
             live_stamp in _UNIT_WORDS)
        other = next(t for t in _UNIT_WORDS if t != live_stamp)
        mutated = fresh_text.replace(f" {_UNIT_WORDS[live_stamp]} — the unit is THE WHOLE FILE",
                                     f" {_UNIT_WORDS[other]} — the unit is THE WHOLE FILE")
        bite("the stamp mutation actually changed the file (a plant that did not plant would "
             "make every bite below an assertion)", mutated != fresh_text)
        open(chain_p, "w", encoding="utf-8").write(mutated)
        bite("stamped_tier() reads the MUTATED stamp back as the other tier",
             stamped_tier(open(chain_p, encoding="utf-8").read()) == other)
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            div_rc = check(tmp)
        div_out = buf2.getvalue()
        bite("--check on a tier divergence exits non-zero (refuses, never a silent pass)",
             div_rc != 0)
        # #193 — THE CONVENTION, NOT JUST THE PROSE. #183 printed the words and exited 1, which
        # no consumer could tell from a real failure: the survey printed "0 could-not-ask" beside
        # "❌ [109] exit 1". The refusal is only a third verdict if it is MACHINE-READABLE.
        bite("--check exits the COULD-NOT-ASK code (77), not the failure code",
             cna.is_refusal(div_rc))
        bite("--check calls it COULD-NOT-ASK", "COULD-NOT-ASK" in div_out)
        bite("the refusal's first marked line is machine-readable by `cna.reason_in`",
             (cna.reason_in(div_out) or "").startswith(cna.MARKER))
        bite("--check does NOT call it STALE — a tier divergence is a measurement problem and "
             "naming it staleness is the #173 defect, reproduced here",
             "STALE" not in div_out.upper())
        bite("the refusal NAMES BOTH TIERS, so a reader can see which two instruments disagreed "
             "rather than being handed a shrug",
             f"({live_stamp})" in div_out and f"({other})" in div_out)
        # ARM: an UNREADABLE stamp is could-not-ask too, never a quiet pass.
        open(chain_p, "w", encoding="utf-8").write(
            fresh_text.replace(" — the unit is THE WHOLE FILE", " — the unit is the whole file"))
        buf3 = io.StringIO()
        with contextlib.redirect_stdout(buf3):
            nostamp_rc = check(tmp)
        nostamp_out = buf3.getvalue()
        bite("--check on an UNREADABLE stamp refuses with the convention's code",
             cna.is_refusal(nostamp_rc))
        bite("--check calls an unreadable stamp COULD-NOT-ASK, not STALE",
             "COULD-NOT-ASK" in nostamp_out and "STALE" not in nostamp_out)
        # CONTROL — restore the untouched fresh bytes; the SAME tree must report FRESH again,
        # proving the two refusals above were the STAMP and not damage to the tree.
        open(chain_p, "w", encoding="utf-8").write(fresh_text)
        bite("stamp restored — the SAME tree reports FRESH again, so the clause does not "
             "false-fire on an agreeing stamp", check(tmp) == 0)

        with open(os.path.join(tmp, OUT_NAME), "a", encoding="utf-8") as f:
            f.write("\ndrift\n")
        # ★ #193 — THE OTHER DIRECTION, and it is the arm that keeps the refusal honest. A gate
        # whose refusal swallows its purpose is worse than the disease: with the stamp AGREEING
        # (restored above), a real staleness must still be a FAILURE — exit 1, never 77.
        drift_rc = check(tmp)
        bite("--check FAILS on a hand-edited file (the stale-record class)", drift_rc == 1)
        bite("and that failure is a FAILURE, not a refusal — a real staleness on the reachable "
             "tier still exits 1, so the COULD-NOT-ASK path did not swallow the gate",
             not cna.is_refusal(drift_rc))
        os.remove(os.path.join(tmp, OUT_NAME))
        bite("--check FAILS when the file is missing entirely", check(tmp) == 1)
        # ---- #73 (f): a STALE title must REFUSE, mutation-tested both arms. The live repo run
        # at the top of this selftest is the passing arm (title #N == latest #N + 1); this arm
        # rewrites the title to equal ★ LATEST's own number — the exact state a skipped mint
        # leaves behind — and the build must refuse with both numbers named.
        gm_live = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
        import re as _re
        _ml = _re.search(r"##\s*★\s*LATEST\s*—[^\n]*?#(\d+)", gm_live)
        _mt = _re.search(r"(\*\*TITLE THE NEXT CHAT →\*\*\s*`)[^`\n]*#(\d+)", gm_live)
        if _ml and _mt:
            stale = _re.sub(r"(\*\*TITLE THE NEXT CHAT →\*\*\s*`[^`\n]*?#)\d+",
                            r"\g<1>" + _ml.group(1), gm_live, count=1)
            with open(os.path.join(tmp, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
                f.write(stale)
            t4, r4 = build(tmp)
            bite("REFUSES a STALE title (title #N == ★ LATEST #N, the skipped-mint state)",
                 t4 is None and isinstance(r4, str) and "STALE-title" in r4)
        else:
            bite("stale-title arm UNMEASURED — live GM lacks an extractable title/#N pair", False)

        # refusal: no ★ LATEST banner ⇒ REFUSE, never emit a confident blank
        with open(os.path.join(tmp, "GOOD-MORNING.md"), "w", encoding="utf-8") as f:
            f.write("# nothing here\n")
        t3, r3 = build(tmp)
        bite("REFUSES (with a reason) when GM has no ★ LATEST banner — no cheerful blank",
             t3 is None and isinstance(r3, str) and len(r3) > 20)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if fails:
        print(f"  ✗ _gen_chain selftest: {len(fails)} bite(s) failed")
        return 1
    print("  ✅ _gen_chain selftest: all bites pass")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--check" in sys.argv:
        sys.exit(check())
    sys.exit(write())
