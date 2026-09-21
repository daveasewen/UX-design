#!/usr/bin/env python3
"""`_gen_size_stamp.py` — GOOD-MORNING.md's `size:` figures, GENERATED at the ritual step.

★ WHY THIS EXISTS — `s294-D8` (Dave, ruled #294, 2026-09-21), and it is the SAME RULING SHAPE AS
`s125-D1`: *a figure that has gone stale twice will go stale a third time, so the fix is not a
fresher value but removing the human from the loop that produces it.*

THE PREMISE, AS MEASURED AND INSCRIBED AT #294. The front page carries a `size:` stamp giving its
own length. It had UNDERSTATED the generated figure at six of the last seven wrap commits, by a
growing gap, and at one session the two series disagreed IN SIGN — the published conclusion was
the opposite of what the file had actually done. The weak form landed at `03605215` (the word
"exact" dropped from the line, nothing else moved). This is the strong form: **the figures are
written by this script, at ritual step 2, and no wrap sub types them.**

WHAT IS GENERATED, AND WHAT IS DELIBERATELY NOT
-----------------------------------------------
GENERATED: the **GM**, **LS** and **corpus GM+LS** figures (K-form and full-digit form), their
UNIT WORD, and the `measured <date>` date. Each pair is one measurement written twice, so a
reader who quotes either gets the same number.
NOT GENERATED, and the omission is declared rather than silent:
  · **§A** — a DIFFERENT OBJECT from a different instrument (`_gm_usage.py`'s section split, not
    a whole-file `measure_tokens` reading). `GOOD-MORNING.md:500` already says in terms that the
    two are never reconciled and never averaged [[measure-dont-convert-units]]. A generator that
    wrote both from one measurement would be the conversion that line forbids.
  · **the session ordinal** (`at the #293 wrap`) — a LABEL naming a fixed event, like
    `_gen_chain.VERDICT_SHA`. A label cannot go stale the way a COUNT does.
  · **every other word on the line** — the drift narration, the §A probe, the banner-cap reading.
    Those are this-session prose and belong to whoever writes them.

THE FIXED POINT, AND WHY IT IS NOT OPTIONAL
-------------------------------------------
⚠ **The stamp measures a region that contains it.** Writing `35,336` where `36,009` stood changes
GM's length, which changes the figure. So this ITERATES: render → measure the WHOLE file →
re-render → repeat until the stamped figures equal the measured ones. Same machinery, same
reasoning and the same refusal as `_gen_chain.build()`'s footer fixed point (#46/#47).
⛔ **IT CAN OSCILLATE** — crossing a width boundary (`99,999` → `100,000`) changes the rendered
length, which can change the measurement back. That is a 2-cycle and this module **REFUSES** it
rather than picking the prettier half. A stamp that silently picked one end of an oscillation
would be a confident blank wearing a number.
⚠ NOTHING THAT VARIES PER PASS MAY ENTER THE LINE — no pass count, no elapsed time. The ONLY
per-pass variables in the rendered text are the figures themselves. The pass count is reported on
stdout, where it is observable without being self-referential.

THE TIER IS WRITTEN, NEVER ASSUMED
----------------------------------
The unit word is the tier the measurement was actually taken in: `real` (#82-D1's tier, reachable
via `API-KEY.txt` / the token cache) or `tape` (observed cl100k). ⛔ On the ESTIMATE tier this
REFUSES with `COULD-NOT-ASK` (exit 77, `_could_not_ask.py`) rather than stamping a divisor guess
under a measured unit word — the #173/#183 lesson: a verdict about the ARTEFACT must never be
dressed over a fact about the ENVIRONMENT. `--check` refuses the same way when the tier it can
reach differs from the tier the committed stamp is written in (`_gen_chain.stamped_tier()`'s
posture, copied deliberately: two graders of one vocabulary is the drift class this repo argues
against everywhere).

THE GRADER'S CONTRACT IS KEPT, NOT REPLACED
-------------------------------------------
`_capture_gate.py` owns the grade: `SIZE_TK_RE` parses the K-form and FAILS past
`SIZE_TOLERANCE` (10%). ★ Both are IMPORTED here, never re-typed — no constant moved, and this
module cannot drift from the gate that grades it. The generated form is inside `SIZE_TK_RE`'s
existing vocabulary (`tape|tk|real`), **so no regex widening is owed and `_capture_gate.py` is
not touched by this enactment.**
⚠ `--check` is deliberately TWO checks at TWO TIERS:
  1. **DRIFT past the gate's own tolerance → exit 1.** The gate's contract, unchanged. It stays
     at 10% and not at byte-equality on purpose: `s214-D6`'s chain figure and ritual step 5b land
     AFTER the declare-last stamp and move both files by single-digit-percent tape (the #241
     rule), so a byte-equal check would be red at every wrap by construction — a gate that cannot
     pass from the state it is introduced in.
  2. **FORM: the line does not carry this generator's marker → WARN (exit 0), not fail.** That is
     the arm which makes "no wrap sub types it" observable rather than hoped for. ⬛ **BORN AS A
     WARN AND THE TIER IS DAVE'S TO RE-DIAL**, for the reason `_capture_gate.py:918` states about
     its own legacy branch: a FAIL here would block the very wrap that first writes the generated
     form. **PROMOTION TRIGGER: once one wrap has passed with the marker present, `--fail-on-form`
     becomes the default and this comment is the only record of that trigger** (ds-024: a rule
     ships with its reader).

USAGE
    python3 knowledge/_gen_size_stamp.py --write     # ritual step 2, DECLARE-LAST
    python3 knowledge/_gen_size_stamp.py --check     # drift vs the gate's tolerance (build step)
    python3 knowledge/_gen_size_stamp.py --selftest  # the bites
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import _could_not_ask as cna              # noqa: E402 - after the path insert, by necessity
import _capture_gate as gate              # noqa: E402 - the grader; its constants are imported

GM = "GOOD-MORNING.md"
LS = "_LIVE-STATE.md"

# ★ THE MARKER. Its presence is how `--check` can tell a GENERATED stamp from a typed one. It
# replaces the phrase the line carried while the figure was hand-taken ("hand-taken at wrap"), so
# the one sentence a reader meets says which loop produced the number.
MARKER = "GENERATED at wrap by `_gen_size_stamp.py`"
HAND_PHRASES = ("hand-taken at wrap", "hand-typed at wrap")

MAX_PASSES = 8          # a fixed point that has not converged by 8 is not converging

# The three figure sites. Each is (K-form, unit word, full-digit form) for ONE measurement, so a
# substitution cannot make the two spellings of one number disagree. `\*\*` and the parenthesis
# are matched literally: the prose around them is NOT this module's business.
_FIG_RE = {
    "gm":     re.compile(r"(\bGM\s*\*\*)([\d.]+)(K\s+)(tape|tk|real)(\*\*\s*\()([\d,]+)"),
    # ⚠ The `+` lookbehind is not decoration: without it `LS` matches inside `corpus GM+LS`, the
    # site two lines down, and the LS figure gets written over the corpus figure. Measured — it
    # did exactly that on the first run of the selftest below. [[silent-lookup-failure-class]]
    "ls":     re.compile(r"(?<![+\w])(LS\s*\*\*)([\d.]+)(K\s+)(tape|tk|real)(\*\*\s*\()([\d,]+)"),
    "corpus": re.compile(r"(\bcorpus GM\+LS\s*\*\*)([\d.]+)(K\s+)(tape|tk|real)(\*\*\s*\()([\d,]+)"),
}
_DATE_RE = re.compile(r"(measured\s+)(\d{4}-\d{2}-\d{2})")

UNIT_BY_TIER = {"real": "real", "cl100k": "tape"}


class SizeStampError(Exception):
    """Raised when the stamp cannot be READ or RENDERED. Never returns a number instead."""


def stamp_index(text):
    """The 0-based index of the `size:` line inside the header region, or raise.

    ⚠ Bounded by `_capture_gate.HEADER_LINES` — the SAME window the grader searches, imported
    rather than re-typed. A generator that wrote outside the region the gate reads would be
    written-but-not-measured (the #41 second-consumer drift).
    """
    lines = text.split("\n")
    for i, ln in enumerate(lines[:gate.HEADER_LINES]):
        if gate.SIZE_STAMP_RE.match(ln):
            return i
    raise SizeStampError(f"no `size:` stamp in {GM}'s first {gate.HEADER_LINES} lines — "
                         f"ritual step 2 has never run here; NOT invented")


def measure(gm_text, ls_text):
    """`(figs, tier)` — GM, LS and the corpus, measured with the GRADER's own instrument.

    ⛔ Refuses the ESTIMATE tier by raising: see the module docstring. The corpus is GM+LS, the
    same sum `_capture_gate`'s `SIZE measured` note publishes, so the stamp and the gate's own
    note can never describe different objects.
    """
    gm_tk, gm_method = gate.measure_tokens(gm_text)
    ls_tk, ls_method = gate.measure_tokens(ls_text)
    t_gm, t_ls = gate._tier_of(gm_method), gate._tier_of(ls_method)
    if t_gm != t_ls:
        raise SizeStampError(f"GM measured on the {t_gm} tier and LS on the {t_ls} tier — two "
                             f"tiers are never summed into one corpus figure "
                             f"[[measure-dont-convert-units]]")
    if t_gm not in UNIT_BY_TIER:
        raise SizeStampError(f"the only reachable tier is {t_gm!r} ({gm_method}) — a byte-divisor "
                             f"ESTIMATE is not stamped under a measured unit word")
    return {"gm": gm_tk, "ls": ls_tk, "corpus": gm_tk + ls_tk}, t_gm


def render(line, figs, unit, when):
    """The `size:` line with every generated figure substituted. Prose is left alone.

    Raises if a site is absent: a silently-unwritten figure is the stale stamp this replaces.
    """
    out = line
    for key, rx in _FIG_RE.items():
        n = figs[key]
        new, hits = rx.subn(
            lambda m: f"{m.group(1)}{n / 1000:.1f}{m.group(3)}{unit}{m.group(5)}{n:,}", out)
        if hits != 1:
            raise SizeStampError(f"the `{key}` figure site matched {hits} time(s) in the `size:` "
                                 f"line — expected exactly 1. The line's shape changed; this "
                                 f"REFUSES rather than writing a figure somewhere else")
        out = new
    out, dhits = _DATE_RE.subn(lambda m: f"{m.group(1)}{when}", out)
    if dhits != 1:
        raise SizeStampError(f"the `measured <date>` site matched {dhits} time(s) — expected 1")
    for phrase in HAND_PHRASES:
        out = out.replace(phrase, MARKER)
    if MARKER not in out:
        # The line was written before the marker existed and carries no hand phrase either: say
        # so where it is read, next to the figure whose provenance it names.
        out = out.replace("(" + f"{figs['gm']:,}", "(" + f"{figs['gm']:,} — {MARKER};", 1)
    return out


def generate(gm_text, ls_text, when=None):
    """`(new_gm_text, figs, tier, passes)` at the FIXED POINT, or raise.

    ★ The loop is the whole point: pass 1's substitution changes GM's length, so pass 1's figure
    is wrong the instant it is written. Convergence is when the text stops moving.
    """
    when = when or datetime.date.today().isoformat()
    seen = []
    text = gm_text
    for p in range(1, MAX_PASSES + 1):
        figs, tier = measure(text, ls_text)
        lines = text.split("\n")
        i = stamp_index(text)
        lines[i] = render(lines[i], figs, UNIT_BY_TIER[tier], when)
        nxt = "\n".join(lines)
        if nxt == text:
            return text, figs, tier, p
        if nxt in seen:
            raise SizeStampError(
                f"the fixed point OSCILLATES (a {len(seen) - seen.index(nxt) + 1}-cycle at pass "
                f"{p}) — almost certainly a comma/width boundary. REFUSING rather than publishing "
                f"the prettier half of a cycle; re-run when the file has moved, or widen the "
                f"figure's rendered width deliberately")
        seen.append(text)
        text = nxt
    raise SizeStampError(f"no fixed point after {MAX_PASSES} passes — REFUSING to stamp a figure "
                         f"the file disagrees with")


def stamped(text):
    """`(figs, unit)` as the file CLAIMS them, parsed with the grader's own `SIZE_TK_RE` where it
    has one. Returns `None` for a site the file does not carry — never a zero."""
    line = text.split("\n")[stamp_index(text)]
    out, unit = {}, None
    for key, rx in _FIG_RE.items():
        m = rx.search(line)
        if m:
            out[key] = int(m.group(6).replace(",", ""))
            unit = unit or m.group(4)
    return out, unit


def check(repo=ROOT, fail_on_form=False):
    """`(exit_code, lines)` — the build step. Drift past the GATE's tolerance fails; a missing
    generator marker warns (see the docstring's promotion trigger)."""
    msgs = []
    try:
        with open(os.path.join(repo, GM), encoding="utf-8") as f:
            gm_text = f.read()
        with open(os.path.join(repo, LS), encoding="utf-8") as f:
            ls_text = f.read()
    except OSError as e:
        return 1, [f"✗ cannot read the artefacts: {e}"]
    try:
        claim, claim_unit = stamped(gm_text)
        figs, tier = measure(gm_text, ls_text)
    except SizeStampError as e:
        cna.refuse("_gen_size_stamp --check", str(e))
        return cna.EXIT, []
    want_unit = UNIT_BY_TIER[tier]
    if claim_unit and claim_unit.lower() != want_unit:
        # A tier divergence is a fact about THIS RUNNER, not a verdict on the artefact (#183).
        cna.refuse("_gen_size_stamp --check",
                   f"the committed stamp is written in `{claim_unit}` and the only tier reachable "
                   f"here is `{want_unit}` — the figures are not comparable, so this is a REFUSAL "
                   f"and not a staleness verdict")
        return cna.EXIT, []
    rc = 0
    for key in sorted(figs):
        if key not in claim:
            msgs.append(f"✗ the `size:` stamp carries no {key.upper()} figure — ritual step 2")
            rc = 1
            continue
        drift = abs(claim[key] - figs[key]) / max(figs[key], 1)
        verdict = "✅" if drift <= gate.SIZE_TOLERANCE else "✗"
        msgs.append(f"{verdict} {key.upper():>6}: stamped {claim[key]:,} · measured "
                    f"{figs[key]:,} {want_unit} · drift {drift * 100:.2f}% "
                    f"(tolerance {gate.SIZE_TOLERANCE * 100:.0f}%, `_capture_gate.SIZE_TOLERANCE`)")
        if drift > gate.SIZE_TOLERANCE:
            rc = 1
    if MARKER not in gm_text.split("\n")[stamp_index(gm_text)]:
        msgs.append(f"⚠ the `size:` line carries no generator marker ({MARKER!r}) — the figure "
                    f"was TYPED, which `s294-D8` rules it may not be. Run `--write` at ritual "
                    f"step 2." + ("" if fail_on_form else "  [WARN tier at birth — see the "
                                                          "module docstring's promotion trigger]"))
        if fail_on_form:
            rc = 1
    return rc, msgs


def write(repo=ROOT, when=None):
    """Ritual step 2. Writes GM once, at the fixed point, or writes nothing at all."""
    with open(os.path.join(repo, GM), encoding="utf-8") as f:
        gm_text = f.read()
    with open(os.path.join(repo, LS), encoding="utf-8") as f:
        ls_text = f.read()
    new, figs, tier, passes = generate(gm_text, ls_text, when=when)
    if new != gm_text:
        with open(os.path.join(repo, GM), "w", encoding="utf-8") as f:
            f.write(new)
    return figs, tier, passes, new != gm_text


# =================================================================================== THE BITES
def selftest():
    """Plant the defect, then detect it. A green that cannot fail is an assertion, not a test
    [[gate-must-quote-what-it-forbids]] — so every arm below asserts BOTH that the healthy form
    passes AND that the mutated form fails, with the reason named."""
    import tempfile
    fails, n = [], [0]

    def bite(name, ok):
        n[0] += 1
        if not ok:
            fails.append(f"[{name}]")

    # ⚠ FORCED ONTO THE cl100k TIER. The `real` tier needs a key and a network; a selftest whose
    # verdict depends on either is a test of the runner. Same env switch `_capture_gate`'s own
    # selftests use, so there is one vocabulary for this, not two.
    was = os.environ.get(gate._REAL_TIER_ENV)
    os.environ[gate._REAL_TIER_ENV] = "1"
    try:
        head = "# X\n\n"
        stamp = ("> **size:** GM **1.0K tape** (1,000 — hand-taken at wrap) · LS **1.0K tape** "
                 "(1,000 real) · corpus GM+LS **2.0K tape** (2,000 real) · measured 1999-01-01\n")
        body = "\n".join(f"line {i} of filler prose for the fixed point" for i in range(400))
        gm = head + stamp + body
        ls = "\n".join(f"live state line {i}" for i in range(300))

        # ---- the healthy path: a real fixed point, and it MOVED the figures off the planted lie.
        new, figs, tier, passes = generate(gm, ls, when="2026-09-21")
        bite("generate reaches a fixed point", passes >= 1)
        bite("the tier is the forced cl100k one", tier == "cl100k")
        bite("the planted 1,000 is GONE from the GM figure", figs["gm"] != 1000)
        bite("the GM figure is the WHOLE file's measurement, not the slice",
             figs["gm"] == gate.measure_tokens(new)[0])
        bite("the corpus is GM+LS and nothing else", figs["corpus"] == figs["gm"] + figs["ls"])
        bite("the K-form and the full-digit form agree",
             f"{figs['gm'] / 1000:.1f}K" in new.split("\n")[stamp_index(new)] and f"{figs['gm']:,}" in new)
        bite("the date site was written", "measured 2026-09-21" in new)
        bite("the hand phrase is REPLACED by the generator marker",
             MARKER in new and "hand-taken at wrap" not in new)
        bite("the grader's own regex parses the generated form",
             gate.SIZE_TK_RE.search(gate.SIZE_STAMP_RE.match(new.split("\n")[stamp_index(new)]).group(1))
             is not None)
        # ★ THE ONE THAT MATTERS: the gate that GRADES this must pass on what this WRITES. Two
        # modules agreeing by inspection is how the #90 escape happened.
        claim = float(gate.SIZE_TK_RE.search(new.split("\n")[stamp_index(new)]).group(1)) * 1000
        bite("the generated stamp is INSIDE the gate's tolerance",
             abs(claim - figs["gm"]) / figs["gm"] <= gate.SIZE_TOLERANCE)
        bite("re-running on the output is a no-op (idempotent)",
             generate(new, ls, when="2026-09-21")[0] == new)

        # ---- planted defect 1: the figure site is gone. MUST refuse, never write elsewhere.
        try:
            generate(head + "> **size:** GM is big · measured 1999-01-01\n" + body, ls)
            bite("a missing figure site REFUSES", False)
        except SizeStampError as e:
            bite("a missing figure site REFUSES", "REFUSES" in str(e) or "matched 0" in str(e))

        # ---- planted defect 2: no `size:` stamp at all.
        try:
            stamp_index(head + body)
            bite("an absent stamp REFUSES rather than inventing one", False)
        except SizeStampError as e:
            bite("an absent stamp REFUSES rather than inventing one", "NOT invented" in str(e))

        # ---- planted defect 3: the ESTIMATE tier. A divisor guess is never stamped.
        real_mt = gate.measure_tokens
        gate.measure_tokens = lambda t: (len(t) // 4, "bytes/3.53 (ESTIMATE)")
        try:
            try:
                generate(gm, ls)
                bite("the ESTIMATE tier REFUSES", False)
            except SizeStampError as e:
                bite("the ESTIMATE tier REFUSES", "ESTIMATE" in str(e))
        finally:
            gate.measure_tokens = real_mt

        # ---- planted defect 4: two tiers, one corpus. Never summed.
        calls = [0]

        def two_tiers(t):
            calls[0] += 1
            return (len(t) // 4, "real" if calls[0] == 1 else "tiktoken cl100k_base")
        gate.measure_tokens = two_tiers
        try:
            try:
                generate(gm, ls)
                bite("two tiers are never summed into one corpus", False)
            except SizeStampError as e:
                bite("two tiers are never summed into one corpus", "two\ntiers" in str(e)
                     or "two tiers" in str(e))
        finally:
            gate.measure_tokens = real_mt

        # ---- planted defect 5: --check must FAIL on a stale stamp and PASS on a fresh one.
        with tempfile.TemporaryDirectory() as td:
            def put(gm_text):
                with open(os.path.join(td, GM), "w", encoding="utf-8") as f:
                    f.write(gm_text)
                with open(os.path.join(td, LS), "w", encoding="utf-8") as f:
                    f.write(ls)
            put(new)
            rc_ok, msgs_ok = check(td)
            bite("--check PASSES on a freshly generated stamp", rc_ok == 0)
            bite("--check's PASS names the tolerance it used",
                 any("tolerance" in m for m in msgs_ok))
            bite("--check does not warn about the marker on a generated stamp",
                 not any("no generator marker" in m for m in msgs_ok))
            # the drift bite: a 3x lie is past any 10% tolerance.
            liar = new.split("\n")
            _si = stamp_index(new)
            liar[_si] = _FIG_RE["gm"].sub(
                lambda m: f"{m.group(1)}{figs['gm'] * 3 / 1000:.1f}{m.group(3)}{m.group(4)}"
                          f"{m.group(5)}{figs['gm'] * 3:,}", liar[_si])
            put("\n".join(liar))
            rc_bad, msgs_bad = check(td)
            bite("--check FAILS on a stamp that drifted past the gate's tolerance", rc_bad == 1)
            bite("--check's failure QUOTES both figures and the drift",
                 any("drift" in m and "measured" in m for m in msgs_bad))
            # the form bite: the marker is what tells a generated stamp from a typed one.
            typed = new.replace(MARKER, "hand-taken at wrap")
            put(typed)
            rc_warn, msgs_warn = check(td)
            bite("a TYPED stamp is reported (the `s294-D8` act, named)",
                 any("was TYPED" in m for m in msgs_warn))
            bite("the form arm is a WARN at birth, not a fail", rc_warn == 0)
            bite("the form arm BLOCKS when the dial is flipped", check(td, fail_on_form=True)[0] == 1)
    finally:
        if was is None:
            os.environ.pop(gate._REAL_TIER_ENV, None)
        else:
            os.environ[gate._REAL_TIER_ENV] = was
    return fails, n[0]


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        fs, nb = selftest()
        print("\n".join(fs) if fs else f"_gen_size_stamp selftest: {nb} bites, all GREEN")
        sys.exit(1 if fs else 0)
    if "--check" in sys.argv:
        rc, out = check(fail_on_form="--fail-on-form" in sys.argv)
        for m in out:
            print(m)
        sys.exit(rc)
    if "--write" in sys.argv:
        try:
            figs, tier, passes, moved = write()
        except SizeStampError as e:
            cna.refuse("_gen_size_stamp --write", str(e))
            sys.exit(cna.EXIT)
        print(f"{'WROTE' if moved else 'already at the fixed point'} — GM {figs['gm']:,} · "
              f"LS {figs['ls']:,} · corpus {figs['corpus']:,} {UNIT_BY_TIER[tier]} "
              f"({tier} tier) · fixed point in {passes} pass(es)")
        sys.exit(0)
    print(__doc__.strip().splitlines()[0])
    print("→ --write (ritual step 2) · --check (build step) · --selftest (the bites)")
    sys.exit(2)
