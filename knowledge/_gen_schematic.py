#!/usr/bin/env python3
"""Generate `reviews/MEMENTO-SCHEMATIC-<date>-v2.html` — the whole Memento mechanism, drawn,
with **every figure read off disk at generation time**.

WHY THIS EXISTS (#125 §0, Dave's own pick; rolled #125 → #126 → built #127)
--------------------------------------------------------------------------
The ask was *"one live HTML diagram of the whole Memento mechanism — chain, store, search,
marks, gates, package — driven from the real file inventory so it could not drift."*

★ **"so it could not drift" is the load-bearing clause, and v1 is the proof it is needed.**
`reviews/MEMENTO-SCHEMATIC-2026-07-26-v1.html` is HAND-AUTHORED, referenced by no generator,
and asserts *"27 blocking validators in a 55-step build"*. Disk at #127 is **30 validators in a
98-step build**. Nothing re-checked it, so nothing caught it. That is this project's central
class verbatim — [[no-gate-parses-the-artefact]], generalised at #125:

    a claim that was true when it was written, has gone false, and nothing re-checks it.

⇒ **No number in the output HTML is typed by a human.** Every figure is a call into a reader
that opens a real file. Prose in this module describes ROLES (what a subsystem is FOR), which is
the one kind of sentence that does not carry a perishable measurement.

THE THREE RULES THAT KEEP IT HONEST
-----------------------------------
1. **REFUSES, NEVER GUESSES.** A reader that cannot read returns `Unmeasured(reason)` and the
   artefact renders a visible ⛔ cell naming the reason. A declared gap passes; a silent one
   fails. There is no default number anywhere in this file
   [[measuring-tool-must-not-guess]] [[a-crash-is-not-a-fail]].

2. **ONE SLICER, NEVER A SECOND.** The build-step count comes from `_gen_chain._steps_in` — the
   function itself, not a copy of its logic — because `_CHAIN.md`'s banner and this diagram must
   not be able to publish different counts of the same object (`s125-D1`). This module *does*
   carry its own row-level reader (`build_rows`, it needs labels and args, which `_steps_in`
   does not return), and `selftest()` bites that the two agree on the COUNT. A parallel slicer
   that is never cross-checked is the drift class, not the fix.

3. **EVERY PANEL DECLARES WHAT RE-CHECKS IT.** For each subsystem the artefact lists the
   `_build_all.py` steps that touch its scripts, with each step's real routing kind
   (ABORT / GATE / ADVISORY), read from `ROUTE_ROWS`. **A subsystem with no steps renders a red
   "⛔ NOTHING RE-CHECKS THIS".** That is the question #125 says to ask of every claim, wired
   into the artefact so it is asked on every regeneration rather than remembered.
   ⚠ This module holds itself to that rule: it reports its own wiring status, and while it is
   unwired the artefact says so in red about itself.

DETERMINISM — AND WHY THERE IS NO CLOCK IN THE OUTPUT
-----------------------------------------------------
`--check` regenerates in memory and asserts the committed file is byte-identical. That makes any
wall-clock value poison: a `datetime.now()` in the output would make the check fail on the second
day for a file nobody touched, and a check that cries wolf gets disabled. **Nothing time-derived
is rendered.** The date in the FILENAME is a version label, typed once, and it names a release,
not a measurement. `selftest()` bites determinism directly (two builds, byte-compared).

⚠ DECLARED ENVIRONMENT DEPENDENCE, same posture as `_gen_chain.py`: two figures are read through
tools rather than files — token sizes need `tiktoken` (else the measurer drops tier and SAYS SO
in the unit word) and the #62 verdict coverage needs `git show`. On a machine without them the
artefact renders honest refusals and `--check` will report stale. That is the refusal working:
the alternative is publishing a number produced by a weaker instrument under a healthy one's name.

USAGE
    python3 knowledge/_gen_schematic.py            # write the HTML
    python3 knowledge/_gen_schematic.py --check    # exit 1 if the committed file is stale
    python3 knowledge/_gen_schematic.py --selftest # the bites
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import ast
import collections
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity

VERSION = "v2"
RELEASE_DATE = "2026-08-07"          # version label on the FILENAME, not a measurement
OUT_REL = os.path.join("reviews", f"MEMENTO-SCHEMATIC-{RELEASE_DATE}-{VERSION}.html")
V1_REL = os.path.join("reviews", "MEMENTO-SCHEMATIC-2026-07-26-v1.html")

# ⚠ TYPED, and deliberately so: this is a fixed historical event (the commit whose message is
# "Ask all 75 steps (75 pass · 0 FAIL)"), not a count. Everything derived FROM it is measured.
# Same constant, same reason, as `_gen_chain.VERDICT_SHA` — imported from there, never re-typed.


class Unmeasured:
    """A figure that could NOT be read. Carries the reason; renders as a visible ⛔ cell.

    ⛔ Never falsy-tested into a zero and never string-formatted into a number. The whole point
    is that an unreadable figure looks DIFFERENT from a readable one in the artefact.
    """

    __slots__ = ("why",)

    def __init__(self, why):
        self.why = str(why)

    def __repr__(self):                                        # pragma: no cover - debugging
        return f"Unmeasured({self.why!r})"


def _fact(label, value, source):
    """One measured row: (label, value|Unmeasured, provenance string)."""
    return (label, value, source)


def _read(label, source, fn):
    """Run a reader, turning ANY exception into a NAMED refusal rather than a crash or a zero."""
    try:
        return _fact(label, fn(), source)
    except Exception as e:                       # noqa: BLE001 - deliberate: name, never guess
        return _fact(label, Unmeasured(f"{type(e).__name__}: {e}"), source)


# =============================================================================================
# READERS OVER `_build_all.py` — the step table and its routing
# =============================================================================================

class BuildTableError(Exception):
    """Raised when STEPS/ROUTE_ROWS cannot be READ. Never returns a partial table."""


def _assign(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name
                                                for t in node.targets):
            return node.value
    raise BuildTableError(f"no top-level `{name} = [...]` in _build_all.py")


def build_rows(repo=ROOT):
    """[(label, script, args)] for every entry in `_build_all.py`'s STEPS, via AST.

    ⚠ A second reader over the same object `_gen_chain._steps_in` counts — justified only
    because it returns MORE (labels, scripts, args) and cross-checked in `selftest()` so the two
    cannot disagree about the count. Regex over this file would be the wrong instrument: the
    step list contains commented-out rows and multi-line strings that a regex reads as data.
    """
    path = os.path.join(repo, "knowledge", "_build_all.py")
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    node = _assign(tree, "STEPS")
    if not isinstance(node, (ast.List, ast.Tuple)):
        raise BuildTableError(f"STEPS is a {type(node).__name__}, not a literal list")
    rows = []
    for e in node.elts:
        if not isinstance(e, (ast.Tuple, ast.List)) or len(e.elts) < 2:
            raise BuildTableError(f"a STEPS entry is not a (label, script[, args]) tuple: "
                                  f"{ast.dump(e)[:80]}")
        label, script = e.elts[0], e.elts[1]
        if not (isinstance(label, ast.Constant) and isinstance(script, ast.Constant)):
            raise BuildTableError("a STEPS entry's label/script is not a literal")
        args = []
        if len(e.elts) > 2 and isinstance(e.elts[2], (ast.List, ast.Tuple)):
            args = [a.value for a in e.elts[2].elts if isinstance(a, ast.Constant)]
        rows.append((label.value, script.value, tuple(args)))
    return rows


def route_kinds(repo=ROOT):
    """{step label -> 'ABORT'|'GATE'|'ADVISORY'} from `ROUTE_ROWS`, via AST.

    The kind is a bare NAME (`ABORT`, not `"abort"`) in the source, so the AST gives the
    constant's identifier directly — which is the word a reader wants anyway.
    """
    path = os.path.join(repo, "knowledge", "_build_all.py")
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    node = _assign(tree, "ROUTE_ROWS")
    out = {}
    for e in node.elts:
        if not isinstance(e, (ast.Tuple, ast.List)) or len(e.elts) < 2:
            raise BuildTableError("a ROUTE_ROWS entry is not a (label, kind, remedy) tuple")
        label, kind = e.elts[0], e.elts[1]
        if not isinstance(label, ast.Constant):
            raise BuildTableError("a ROUTE_ROWS label is not a literal")
        out[label.value] = kind.id if isinstance(kind, ast.Name) else str(getattr(kind, "value", "?"))
    return out


def rechecks_for(scripts, repo=ROOT):
    """[(step label, kind)] — the build steps that RUN any of `scripts`.

    ★ This is the artefact's answer to *"what re-checks this?"*, computed rather than asserted.
    An empty list is the interesting case and the renderer paints it red.
    """
    kinds = route_kinds(repo)
    want = set(scripts)
    out = []
    for label, script, args in build_rows(repo):
        if script in want:
            flag = " ".join(args)
            out.append((f"{label}{(' ' + flag) if flag else ''}", kinds.get(label, "UNROUTED")))
    return out


# =============================================================================================
# THE SIX SUBSYSTEMS — one fact reader each. Every value opens a real file.
# =============================================================================================

def _jload(repo, rel):
    with open(os.path.join(repo, rel), encoding="utf-8") as f:
        return json.load(f)


def _measurer():
    """`_capture_gate`, or a NAMED refusal. Token sizes are the one figure needing a tool."""
    import _capture_gate as cg
    return cg


def _unit_word():
    import _gen_chain as gc
    return gc.unit_word(_measurer())


# ---------------------------------------------------------------------------------------------
# ★ #193 — THE COULD-NOT-ASK CLAUSE, THE SAME DISEASE #173/#183 FOUND, THE SAME SHAPE OF REMEDY.
#
# MEASURED, not assumed: a bare checkout of THIS commit (no `API-KEY.txt`, no
# `knowledge/.token-cache.json` — both gitignored, `.gitignore:57,58`) renders this page with
# `8,246 tape (cl100k ESTIMATE)` where the committed file says `12,871 real`. So:
#   · `--check` reported "STALE — a figure in it no longer matches disk", a verdict about the
#     ARTEFACT dressed over a fact about the ENVIRONMENT [[gate-cannot-pass-in-one-environment]];
#   · `--selftest` failed on the CAPTION GEOMETRY arm (`worst: (39, 'chain')`) — because the
#     fallback's unit WORD is longer than `real`, the caption overflowed its box. A geometry
#     complaint that is really an instrument complaint is the same lie in fancier dress.
#
# ⇒ Both paths now ASK THE TIER FIRST and refuse by the ruled convention (`_could_not_ask.py`,
# exit 77 + a `COULD-NOT-ASK:` line) rather than accusing the page. ⚠ The refusal is keyed on the
# UNIT WORDS THE COMMITTED FILE CARRIES vs the tier reachable here — never on "am I in CI", which
# would recreate the #173 lie in a new shape.
_TIER_FIGURE = None


def stamped_tiers(text):
    """The tiers the ON-DISK page was rendered in, read out of its own figures.

    Returns a `set` of `'real'` · `'cl100k'` · `'estimate'`, EMPTY when the page carries no
    recognisable unit word. ⚠ An empty set is NOT "fine" and is never defaulted to the live tier:
    a page whose unit cannot be read cannot be compared, and the caller says so
    [[measuring-tool-must-not-guess]].

    ★ It reads the FIGURES, not a footer, because this artefact has no single fixed-point
    sentence — every token figure carries its own unit word, and a page rendered in two tiers is
    itself a fact worth seeing rather than averaging away.
    """
    global _TIER_FIGURE
    if _TIER_FIGURE is None:
        import re
        import _gen_chain as gc
        alt = "|".join(re.escape(w) for w in sorted(gc._UNIT_WORDS.values(), key=len, reverse=True))
        _TIER_FIGURE = (re.compile(r"[\d,]+\s+(" + alt + ")"),
                        {w: t for t, w in gc._UNIT_WORDS.items()})
    rx, by_word = _TIER_FIGURE
    return {by_word[m] for m in rx.findall(text or "") if m in by_word}


def tier_refusal(subject, have_text, extra=""):
    """A `_could_not_ask.EXIT` when this environment cannot reproduce the committed page's unit,
    else `None` — so both `check()` and `selftest()` ask the identical question in one place.

    ⚠ Deliberately asked BEFORE any comparison. A tier divergence makes EVERY token figure differ
    for a reason that has nothing to do with the tree; if the byte compare (or the caption
    measurement) ran first it would always win and the honest answer would be unreachable — the
    ordering `_gen_chain.check()` established at #183, for the same reason.
    """
    import _gen_chain as gc
    try:
        live = _measurer().measurement_tier()
    except Exception as ex:                                # pragma: no cover - import guard
        return cna.refuse(subject, f"the tier probe itself is unreachable ({ex}); no verdict is "
                                   f"offered in either direction.")
    stamped = stamped_tiers(have_text)
    if not stamped:
        return cna.refuse(subject, "the committed page carries NO READABLE UNIT WORD on any "
                                   "token figure, so the instrument it was rendered with cannot "
                                   f"be compared with this environment's ({live}). A REFUSAL, "
                                   "not a content verdict: regenerate with "
                                   "`python3 knowledge/_gen_schematic.py`.")
    if live not in stamped:
        return cna.refuse(subject, (
            f"MEASUREMENT REFUSAL, NOT A CONTENT VERDICT IN EITHER DIRECTION. The committed page "
            f"carries figures in {sorted(gc._UNIT_WORDS.get(t, t) for t in stamped)}; the only "
            f"tier reachable in THIS environment is `{gc._UNIT_WORDS.get(live, live)}` ({live}). "
            f"Every token figure would differ for that reason alone. ⚠ `real` is reachable ONLY "
            f"via `API-KEY.txt` or `knowledge/.token-cache.json` and BOTH ARE GITIGNORED (#173, "
            f"proven by single-variable isolation), so a bare checkout can never agree with a "
            f"`real` page. Give this environment the same measurer, or re-ask where it is "
            f"reachable — this artefact's content is UNKNOWN here and is reported as unknown "
            f"rather than guessed.{extra}"))
    return None


def facts_chain(repo=ROOT):
    """CHAIN — the boot path. What a cold session pays to become oriented."""
    out = []

    def _chain_tk():
        cg = _measurer()
        text = open(os.path.join(repo, "_CHAIN.md"), encoding="utf-8").read()
        return f"{cg.measure_tokens(text)[0]:,} {_unit_word()}"

    def _gm_tk():
        cg = _measurer()
        text = open(os.path.join(repo, "GOOD-MORNING.md"), encoding="utf-8").read()
        return f"{cg.measure_tokens(text)[0]:,} {_unit_word()}"

    def _pct():
        cg = _measurer()
        c = cg.measure_tokens(open(os.path.join(repo, "_CHAIN.md"), encoding="utf-8").read())[0]
        g = cg.measure_tokens(open(os.path.join(repo, "GOOD-MORNING.md"), encoding="utf-8").read())[0]
        return f"{100.0 * c / g:.0f}% of GOOD-MORNING.md"

    out.append(_read("`_CHAIN.md` — what boot costs", "measured by `_capture_gate.measure_tokens`", _chain_tk))
    out.append(_read("`GOOD-MORNING.md` — the file it replaces at boot", "measured by `_capture_gate.measure_tokens`", _gm_tk))
    out.append(_read("the CUT — chain as a share of GM", "both sides measured, ratio computed", _pct))

    def _lines():
        n = sum(1 for _ in open(os.path.join(repo, "_CHAIN.md"), encoding="utf-8"))
        return f"{n:,} lines"
    out.append(_read("`_CHAIN.md` size on disk", "line count of the generated file", _lines))

    def _steps_now():
        import _gen_chain as gc
        n, distinct, why = gc.build_steps_now(repo)
        if n is None:
            raise BuildTableError(why)
        dup = "" if n == distinct else f" ⚠ {n - distinct} DUPLICATE label(s)"
        return f"{n} steps ({distinct} distinct labels){dup}"
    out.append(_read("build steps the chain banner reports", "`_gen_chain.build_steps_now` → `_build_all.py` AST (`s125-D1`)", _steps_now))

    def _verdict():
        import _gen_chain as gc
        now, _d, why_n = gc.build_steps_now(repo)
        then, _d2, why_t = gc.build_steps_at(gc.VERDICT_SHA, repo)
        if now is None:
            raise BuildTableError(why_n)
        if then is None:
            raise BuildTableError(why_t)
        return (f"{then} of {now} — {now - then} steps have NEVER been in a green verdict "
                f"(#62, `{gc.VERDICT_SHA}`)")
    out.append(_read("steps the last green verdict actually covered", "`_gen_chain.build_steps_at` → `git show <sha>:_build_all.py` AST", _verdict))
    return out


def facts_store(repo=ROOT):
    """STORE — the record itself: open work, rulings, ledger, dossiers."""
    out = []

    def _state_counts():
        import _state
        c = _state.counts(_state.load(os.path.join(repo, "knowledge", "_state.json")))
        return (f"{c['total']} items · {c['live']} live · {c['by_owner']['dave']} Dave's · "
                f"{c['by_owner']['claude']} mine")
    out.append(_read("`_state.json` — open work", "`_state.counts()` over the store", _state_counts))

    def _uncond():
        import _state
        c = _state.counts(_state.load(os.path.join(repo, "knowledge", "_state.json")))
        return (f"{c['unconditioned']} UNCONDITIONED · {c['conditioned']} carry a close condition")
    out.append(_read("items that can actually close", "`_state.counts()`", _uncond))

    def _legacy():
        import _state
        return f"{len(_state.LEGACY_IDS)} ids — a FROZEN set that may only shrink"
    out.append(_read("the inherited debt", "`len(_state.LEGACY_IDS)`", _legacy))

    def _rulings():
        r = _jload(repo, "knowledge/_rulings.json")["rulings"]
        return f"{len(r)} rulings across {len({x['ruled'] for x in r})} sessions"
    out.append(_read("`_rulings.json` — what Dave decided", "`len()` over the parsed store", _rulings))

    def _by():
        r = _jload(repo, "knowledge/_rulings.json")["rulings"]
        c = collections.Counter(x["by"] for x in r)
        return " · ".join(f"{k}: {v}" for k, v in sorted(c.items()))
    out.append(_read("who ruled them", "histogram of the `by` field", _by))

    def _ledger():
        p = os.path.join(repo, "notes", "_MEMENTO-DECISIONS.md")
        text = open(p, encoding="utf-8").read()
        heads = sum(1 for ln in text.splitlines() if ln.startswith("## "))
        cg = _measurer()
        return f"{heads} sections · {cg.measure_tokens(text)[0]:,} {_unit_word()}"
    out.append(_read("`notes/_MEMENTO-DECISIONS.md` — the ledger", "`## ` heading count + `measure_tokens`", _ledger))

    def _dossiers():
        d = os.path.join(repo, "_DECISION-HISTORY")
        n = len([f for f in os.listdir(d) if f.endswith(".md") and f != "README.md"])
        return f"{n} session dossiers"
    out.append(_read("`_DECISION-HISTORY/` — the long-form record", "directory listing, `*.md` minus README", _dossiers))
    return out


def facts_search(repo=ROOT):
    """SEARCH — retrieval. The reason everything else is allowed to stay big."""
    out = []

    def _records():
        return f"{len(_jload(repo, 'knowledge/_memento-index.json')['records']):,} records"
    out.append(_read("`_memento-index.json` — the corpus", "`len(records)` in the generated index", _records))

    def _kinds():
        recs = _jload(repo, "knowledge/_memento-index.json")["records"]
        c = collections.Counter(r["kind"] for r in recs)
        top = " · ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))
        return f"{len(c)} kinds — {top}"
    out.append(_read("what is IN the corpus", "histogram of the `kind` field", _kinds))

    def _genby():
        return _jload(repo, "knowledge/_memento-index.json")["$generated_by"].split("—")[0].strip()
    out.append(_read("who builds the index", "the index's own `$generated_by` stamp", _genby))

    def _cases():
        import _memento_search as ms
        return f"{len(ms.SELFTEST_CASES)} known-answer cases · {len(ms.KIND_ORDER)} ranked buckets"
    out.append(_read("what the search selftest asks", "`len(_memento_search.SELFTEST_CASES)`", _cases))

    def _caps():
        import _memento_search as ms
        return (f"{sum(ms.DEFAULT_CAP.values())} results across {len(ms.DEFAULT_CAP)} buckets "
                f"— `--all` lifts it")
        # ⛔ the DEFAULT hides rulings: [[retrieval-default-hides-the-ruling]]
    out.append(_read("the default cap (why `--all` exists)", "`sum(_memento_search.DEFAULT_CAP.values())`", _caps))

    def _lex():
        return f"{len(_jload(repo, 'knowledge/_consult-lexicon.json')['synonyms'])} synonym groups"
    out.append(_read("`_consult-lexicon.json` — query expansion", "`len(synonyms)`", _lex))
    return out


def facts_marks(repo=ROOT):
    """MARKS — the graph, and the observation window that decided what a mark MEANS."""
    out = []

    def _obs():
        p = os.path.join(repo, "knowledge", "_graph-mark-observations.jsonl")
        rows = [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()]
        return f"{len(rows):,} observations over {len({r['date'] for r in rows})} dates"
    out.append(_read("`_graph-mark-observations.jsonl`", "parsed line by line (JSONL)", _obs))

    def _doors():
        p = os.path.join(repo, "knowledge", "_graph-mark-observations.jsonl")
        rows = [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()]
        c = collections.Counter(r.get("door") for r in rows)
        return " · ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0]))))
    out.append(_read("which door was observed", "histogram of the `door` field", _doors))

    def _marked():
        p = os.path.join(repo, "knowledge", "_graph-mark-observations.jsonl")
        rows = [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()]
        n = sum(1 for r in rows if r.get("superseded_by"))
        return f"{n:,} of {len(rows):,} carried a supersession mark"
    out.append(_read("how often a mark fired", "count of non-empty `superseded_by`", _marked))

    def _graph():
        g = _jload(repo, "knowledge/_decision-graph.json")
        return f"{len(g['nodes'])} nodes · {len(g['edges'])} typed edges"
    out.append(_read("`_decision-graph.json`", "`len(nodes)` / `len(edges)`", _graph))

    def _mmap():
        return f"{len(_jload(repo, 'knowledge/_graph-mention-map.json')['map'])} joined nodes"
    out.append(_read("`_graph-mention-map.json` — the graph↔index join", "`len(map)`", _mmap))
    return out


def facts_gates(repo=ROOT):
    """GATES — the machinery that re-checks everything else. Including, now, this file."""
    out = []

    def _validators():
        d = os.path.join(repo, "knowledge")
        n = [f for f in os.listdir(d) if f.startswith("_validate_") and f.endswith(".py")]
        return f"{len(n)} `_validate_*.py` on disk"
    out.append(_read("validators", "directory listing of `knowledge/_validate_*.py`", _validators))

    def _steps():
        return f"{len(build_rows(repo))} steps in `_build_all.py`"
    out.append(_read("the build", "AST of `STEPS`", _steps))

    def _routing():
        kinds = route_kinds(repo)
        rows = build_rows(repo)
        c = collections.Counter(kinds.get(lbl, "UNROUTED") for lbl, _s, _a in rows)
        return " · ".join(f"{k} {v}" for k, v in sorted(c.items()))
    out.append(_read("how a red is routed", "AST of `ROUTE_ROWS`, joined to STEPS by exact label", _routing))

    def _blocking():
        kinds = route_kinds(repo)
        rows = build_rows(repo)
        block = sum(1 for lbl, _s, _a in rows if kinds.get(lbl) in ("ABORT", "GATE"))
        return f"{block} of {len(rows)} steps can stop or fail the build"
    out.append(_read("how much of it actually bites", "ABORT+GATE over all steps", _blocking))

    def _selftests():
        rows = build_rows(repo)
        n = sum(1 for _l, _s, a in rows if "--selftest" in a)
        m = sum(1 for _l, _s, a in rows if "--check" in a)
        return f"{n} `--selftest` steps · {m} `--check` (determinism) steps"
    out.append(_read("tests of the tests", "`--selftest` / `--check` args in STEPS", _selftests))

    def _exempt():
        import _validate_wiring as vw
        if not vw.EXEMPT:
            return "0 — every validator on disk is WIRED (`EXEMPT` is empty, `s125-D2`)"
        return f"{len(vw.EXEMPT)} exempt: " + " · ".join(sorted(vw.EXEMPT))
    out.append(_read("validators exempt from wiring", "`len(_validate_wiring.EXEMPT)`", _exempt))
    return out


def facts_package(repo=ROOT):
    """PACKAGE — what ships. Copies only, and every copy delta-audited (Dave's #64 boundary)."""
    out = []

    def _files():
        base = os.path.join(repo, "memento-package")
        n = sum(1 for r, ds, fs in os.walk(base)
                if "__pycache__" not in r for f in fs)
        return f"{n} files (excluding `__pycache__`)"
    out.append(_read("`memento-package/`", "recursive walk, bytecode cache excluded by name", _files))

    def _copies():
        import _validate_package_delta as pd
        return (f"{len(pd.VERBATIM_SET)} verbatim: " + " · ".join(f"`{n}`" for n in pd.VERBATIM_SET))
    out.append(_read("files copied out of `knowledge/` verbatim", "`_validate_package_delta.VERBATIM_SET`", _copies))

    def _twice():
        import _validate_package_delta as pd
        return f"`{pd.COPY_A}` and `{pd.COPY_B}` — audited against each other"
    out.append(_read("and copied TWICE, into two surfaces", "`COPY_A` / `COPY_B`", _twice))

    def _shim():
        import _validate_package_delta as pd
        n = (len(pd.PORTED_FUNCS_A) + len(pd.PORTED_CONSTS_A) + len(pd.PORTED_CONSTS_B))
        return (f"{n} names ported into `{pd.SHIM_NAME}` from 2 sources "
                f"(@ `{pd.PORT_COMMIT_A}` / `{pd.PORT_COMMIT_B}`), each AST-extracted and hashed")
    out.append(_read("shimmed code, and how drift is caught", "`PORTED_FUNCS_A` + `PORTED_CONSTS_A` + `PORTED_CONSTS_B`", _shim))

    def _known():
        import _validate_package_delta as pd
        return f"{len(pd.KNOWN_FILES)} names — anything else in a machinery folder is a FAIL"
    out.append(_read("the machinery allowlist", "`len(_validate_package_delta.KNOWN_FILES)`", _known))
    return out


def facts_self(repo=ROOT):
    """THIS ARTEFACT — held to its own rule. An artefact that exempts itself is v1 again."""
    out = []

    def _figures():
        n = ok = bad = 0
        for s in SUBSYSTEMS:
            if s["key"] == "self":
                continue
            for _lbl, val, _src in s["facts"](repo):
                n += 1
                bad += isinstance(val, Unmeasured)
        ok = n - bad
        return f"{n} figures rendered — {ok} MEASURED, {bad} declared UNMEASURED"
    # ⚠ NAMED EXACTLY. This tally excludes the four rows of THIS panel (counting them would
    # recurse), so it may NOT be labelled "every figure in this page" — it isn't, and this page
    # is the wrong place to be loose about what a number covers.
    out.append(_read("figures in the six subsystem panels above",
                     "counted by re-running each subsystem reader; excludes this panel's own "
                     "4 rows, which would recurse", _figures))

    def _typed():
        return "0 — the only typed strings are role prose, file paths and the version label"
    out.append(_read("figures typed by a human", "by construction; `--check` proves the file matches", _typed))

    def _wired():
        rows = rechecks_for(("_gen_schematic.py",), repo)
        if not rows:
            return Unmeasured("`_gen_schematic.py` has NO row in `_build_all.py`'s STEPS — "
                              "nothing re-checks this artefact yet. Wiring it moves the step "
                              "count, which moves `_CHAIN.md`'s generated banner, so it is one "
                              "commit's work and it is NOT this sub's to take.")
        return f"{len(rows)} step(s): " + " · ".join(f"{k} — {l}" for l, k in rows)
    out.append(_read("what re-checks THIS file", "`rechecks_for('_gen_schematic.py')` over STEPS", _wired))

    def _orphan_selftests():
        have = {s for _l, s, a in build_rows(repo) if "--selftest" in a}
        d = os.path.join(repo, "knowledge")
        defs = []
        for f in sorted(os.listdir(d)):
            if not f.endswith(".py"):
                continue
            try:
                tree = ast.parse(open(os.path.join(d, f), encoding="utf-8").read())
            except SyntaxError:
                continue
            if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "selftest"
                   for n in tree.body):
                defs.append(f)
        missing = [f for f in defs if f not in have]
        return (f"{len(defs)} modules define a module-level `selftest()`; "
                f"{len(missing)} have NO `--selftest` row in STEPS — " +
                " · ".join(f"`{m}`" for m in missing))
    out.append(_read("the same question, asked of every selftest",
                     "module-level `def selftest` (AST) minus `--selftest` scripts in STEPS. "
                     "⚠ Counts PRESENCE of a row, not execution — a module may still run its "
                     "selftest inside `__main__`; that is the unit `_validate_wiring.py` uses too",
                     _orphan_selftests))
    return out


# =============================================================================================
# THE TABLE. Prose here describes ROLES; every figure comes from the readers above.
# =============================================================================================

SUBSYSTEMS = [
    {
        "key": "chain", "n": "①", "title": "CHAIN",
        "role": "The cold-start door. One generated file carries the entire boot contract, so a "
                "session pays for the contract instead of the archive it lives in.",
        "shape": "GOOD-MORNING.md + _LIVE-STATE.md → _gen_chain.py → _CHAIN.md",
        "scripts": ("_gen_chain.py", "_capture_gate.py", "_gm_usage.py", "_gm_move.py",
                    "_gauge_tokens.py"),
        "facts": facts_chain,
    },
    {
        "key": "store", "n": "②", "title": "STORE",
        "role": "The record. Open work, Dave's rulings, the ledger and the long-form dossiers — "
                "the things a session must not re-decide because they were already decided.",
        "shape": "_state.json · _rulings.json · notes/_MEMENTO-DECISIONS.md · _DECISION-HISTORY/",
        "scripts": ("_build_live_state.py", "_build_states_probe.py", "_roll_state.py",
                    "_gen_lanes.py", "_build_enactment_register.py"),
        "facts": facts_store,
    },
    {
        "key": "search", "n": "③", "title": "SEARCH",
        "role": "Retrieval. The reason the record is allowed to stay large: nothing is a reading "
                "list, everything is a query. Ask for what you need; never read a file to find "
                "out whether you need it.",
        "shape": "_build_memento_index.py → _memento-index.json → _memento_search.py / _search_core.py",
        "scripts": ("_build_memento_index.py", "_memento_search.py", "_search_core.py",
                    "_build_consult_index.py", "_consult.py"),
        "facts": facts_search,
    },
    {
        "key": "marks", "n": "④", "title": "MARKS",
        "role": "Supersession. A retrieved record can be dead; a mark says a live record MENTIONS "
                "a dead node, which is not the same claim as the record being dead. The "
                "observation window that settled that distinction is on disk, not in memory.",
        "shape": "_decision-graph.json + _memento-index.json → _build_graph_mention_map.py → marks",
        "scripts": ("_build_graph_mention_map.py", "_build_decision_graph.py"),
        "facts": facts_marks,
    },
    {
        "key": "gates", "n": "⑤", "title": "GATES",
        "role": "The re-checkers. Everything above is a claim; this is the only part of the "
                "mechanism whose job is to notice when a claim has gone false.",
        "shape": "_build_all.py STEPS → validators, generators, determinism checks, selftests",
        "scripts": ("_validate_wiring.py", "_validate_standing_instructions.py",
                    "_validate_assertions.py", "_build_integrity.py"),
        "facts": facts_gates,
    },
    {
        "key": "package", "n": "⑥", "title": "PACKAGE",
        "role": "What ships. The mechanism without the project: copies only, never moves, and "
                "every copy delta-audited against its source (Dave's #64 boundary).",
        "shape": "knowledge/*.py → memento-package/machinery/ (×2 surfaces) → dist / claude-plugin",
        "scripts": ("_validate_package_delta.py",),
        "facts": facts_package,
    },
    {
        "key": "self", "n": "⚑", "title": "THIS ARTEFACT",
        "role": "The diagram holds itself to the rule it draws. v1 asserted 27 validators in a "
                "55-step build and nothing re-checked it; the figures below are this page "
                "answering the same question about itself.",
        "shape": "_gen_schematic.py → reviews/MEMENTO-SCHEMATIC-…-v2.html (--check asserts freshness)",
        "scripts": ("_gen_schematic.py",),
        "facts": facts_self,
    },
]


# =============================================================================================
# RENDER
# =============================================================================================

def md(s):
    """Escape, then honour the two markdown marks used in this module's prose."""
    s = html.escape(str(s), quote=False)
    if s.count("`") % 2 == 0:
        s = "".join(p if i % 2 == 0 else f"<code>{p}</code>" for i, p in enumerate(s.split("`")))
    if s.count("**") % 2 == 0:
        s = "".join(p if i % 2 == 0 else f"<b>{p}</b>" for i, p in enumerate(s.split("**")))
    return s


def value_html(v):
    if isinstance(v, Unmeasured):
        return f'<span class="un">⛔ UNMEASURED — {md(v.why)}</span>'
    return md(v)


def _plain(v, cap=None):
    """A short, tag-free form for the SVG. Refusals stay visibly refusals."""
    if isinstance(v, Unmeasured):
        return "⛔ UNMEASURED"
    cap = CAP_CHARS if cap is None else cap
    t = str(v).replace("`", "")
    return t if len(t) <= cap else t[:cap - 1] + "…"


def _box(x, y, w, h, accent, n, title, sub, dashed=False):
    """A labelled box. ★ Each `<text>` carries `data-right` — the inside edge of its own box —
    so the render probe can assert NUMERICALLY that no label overflows its container.

    ⚠ This attribute exists because the first render of this diagram had a subtitle running
    straight out through the right-hand border, and the probe passed: it only checked the SVG
    viewBox, so text that escaped its BOX but stayed on the CANVAS read as fine. Seeing the PNG
    caught it. The assertion is the repair — the eye should not be the only thing that can.
    """
    d = ' stroke-dasharray="5 4"' if dashed else ""
    right = x + w - 10
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="var(--paper)" '
        f'stroke="var(--ink)" stroke-width="1.5"{d}/>'
        f'<rect x="{x}" y="{y}" width="5" height="{h}" fill="{accent}"/>'
        f'<text x="{x + 16}" y="{y + 24}" class="bt" data-right="{right}">'
        f'{md(n)} {md(title)}</text>'
        f'<text x="{x + 16}" y="{y + 43}" class="bs" data-right="{right}">{md(sub)}</text>')


def _arrow(pts, dashed=False, label=None, lx=0, ly=0):
    d = ' stroke-dasharray="4 4"' if dashed else ""
    path = " ".join(f"{'M' if i == 0 else 'L'}{x} {y}" for i, (x, y) in enumerate(pts))
    out = (f'<path d="{path}" fill="none" stroke="var(--ink)" stroke-width="1.5"{d} '
           f'marker-end="url(#ah)"/>')
    if label:
        out += f'<text x="{lx}" y="{ly}" class="al">{md(label)}</text>'
    return out


def _hl(facts, idx, fmt):
    """A compact box caption built from an already-measured fact. Refusals PROPAGATE — a box
    never shows a number the panel below it is refusing to show."""
    v = facts[idx][1]
    return v if isinstance(v, Unmeasured) else fmt(v)


def headlines(repo=ROOT):
    """{key: short caption} for the map. Composed from the panel readers, never re-measured —
    a second measurement of the same thing is exactly how a map and its legend drift apart."""
    ch, st, se = facts_chain(repo), facts_store(repo), facts_search(repo)
    mk, ga, pk = facts_marks(repo), facts_gates(repo), facts_package(repo)

    def _two(a, b, fmt):
        if isinstance(a, Unmeasured):
            return a
        if isinstance(b, Unmeasured):
            return b
        return fmt(a, b)

    return {
        "chain": _hl(ch, 0, lambda v: f"boot costs {v}"),
        "store": _hl(st, 3, lambda v: v.replace("rulings across", "rulings ·")),
        "search": _hl(se, 0, lambda v: f"{v} indexed"),
        "marks": _hl(mk, 0, lambda v: v),
        "gates": _two(ga[1][1], ga[0][1],
                      lambda a, b: f"{a.split(' in ')[0]} · {b.split(' `')[0]} validators"),
        "package": _two(pk[0][1], pk[1][1],
                        lambda a, b: f"{a.split(' (')[0]} · {b.split(':')[0]} copies"),
    }


SVG_W, BOX_W = 872, 240        # box width sized so a 32-char caption clears its border at 11.5px
GATES_W = BOX_W * 2 + 40       # ⑤ spans the first two columns; the 40px gap holds the ship arrow
# ⛔ COMPUTED FROM BOX_W, and it had to be. The first version typed `32` with a comment claiming
# it was "derived from the geometry, not guessed" — and a mutation shrinking BOX_W to 150 left the
# bite GREEN while every caption overflowed. A derivation written in PROSE is not a derivation;
# it is the same claim-nothing-re-checks this whole artefact is about, committed inside the file
# that argues against it. 6.5 approximates the average glyph advance at 11.5px sans; it is a cheap
# OFFLINE proxy, and the authoritative check is the `data-right` attribute a render probe reads.
CAP_CHARS = int((BOX_W - 32) / 6.5)
COL = (16, 316, 616)           # three column origins; centres are +BOX_W/2


def svg(repo=ROOT):
    """The map. Every headline figure in it is a reader's return value, never a literal."""
    h = {k: _plain(v) for k, v in headlines(repo).items()}
    c0, c1, c2 = COL
    m0, m1, m2 = c0 + BOX_W // 2, c1 + BOX_W // 2, c2 + BOX_W // 2
    B, G, R = "var(--blue)", "var(--green)", "var(--red)"
    parts = [
        f'<svg viewBox="0 0 {SVG_W} 452" role="img" xmlns="http://www.w3.org/2000/svg" '
        'aria-label="How the six Memento subsystems connect">',
        '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" fill="var(--ink)"/></marker></defs>',
        '<text x="16" y="12" class="rl">BOOT</text>',
        _box(c0, 22, BOX_W, 62, "var(--line)", "", "the two written files",
             "GOOD-MORNING · _LIVE-STATE", dashed=True),
        _box(c1, 18, BOX_W, 70, B, "①", "CHAIN", h["chain"]),
        _box(c2, 22, BOX_W, 62, "var(--line)", "", "a cold session orients",
             "and reads nothing else", dashed=True),
        _arrow([(c0 + BOX_W, 53), (c1 - 6, 53)]),
        _arrow([(c1 + BOX_W, 53), (c2 - 6, 53)]),
        '<text x="16" y="134" class="rl">RECORD → RETRIEVAL</text>',
        _box(c0, 144, BOX_W, 70, G, "②", "STORE", h["store"]),
        _box(c1, 144, BOX_W, 70, B, "③", "SEARCH", h["search"]),
        _box(c2, 144, BOX_W, 70, B, "④", "MARKS", h["marks"]),
        _arrow([(c0 + BOX_W, 179), (c1 - 6, 179)]),
        _arrow([(c1 + BOX_W, 179), (c2 - 6, 179)]),
        _arrow([(m0, 144), (m0, 112), (m1, 112), (m1, 94)], label="generated from the spine",
               lx=m0 + 18, ly=108),
        # ⚠ Geometry banked from a render, not guessed: the return path corners at m1+40 so the
        # GATES→SEARCH arrow at m1 passes it without a crossing, and the "copies only" arrow
        # runs LEFT-to-RIGHT (the first draft ran c1+BOX_W+60 → c2-6, i.e. six pixels BACKWARDS,
        # so its head pointed into GATES — visible in the PNG, invisible to every assertion).
        _arrow([(m2, 214), (m2, 238), (m1 + 40, 238), (m1 + 40, 220)], dashed=True,
               label="a mark says a LIVE record mentions a DEAD node", lx=m1 + 56, ly=254),
        '<text x="16" y="288" class="rl">GUARD → SHIP</text>',
        _box(c0, 298, GATES_W, 76, R, "⑤", "GATES", h["gates"]),
        _box(c2, 298, BOX_W, 76, G, "⑥", "PACKAGE", h["package"]),
        _arrow([(m0, 298), (m0, 224)], label="re-checks", lx=m0 + 10, ly=272),
        _arrow([(m1, 298), (m1, 224)]),
        _arrow([(c0 + GATES_W + 8, 336), (c2 - 6, 336)], dashed=True, label="copies only",
               lx=c0 + GATES_W + 12, ly=358),
        '<text x="16" y="404" class="cap">Solid = a real file feeds the next thing. '
        'Dashed = a relationship, not a pipeline.</text>',
        '<text x="16" y="422" class="cap">Every figure above is read off disk when this page '
        'is generated. Nothing in it was typed.</text>',
        '<text x="16" y="440" class="cap">v1 of this diagram typed its figures. They were true '
        'in July and false by August, and nothing noticed.</text>',
        "</svg>",
    ]
    return "\n".join(parts)


CSS = """
  :root{ --ink:#1A1A1A; --paper:#FFFFFF; --line:#D7D7D7; --muted:#5A5A5A; --wash:#F4F4F4;
         --blue:#305A85; --green:#2E6B4F; --red:#B92F1E; --amber:#F0B13A; }
  *{box-sizing:border-box; margin:0}
  body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; color:var(--ink);
       background:var(--paper); padding:44px 32px 72px; max-width:1120px; margin:0 auto;
       line-height:1.5; font-size:15px}
  h1{font-size:30px; font-weight:700; letter-spacing:-.015em}
  .sub{color:var(--muted); font-size:13.5px; margin:8px 0 6px}
  code{font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.88em;
       background:var(--wash); padding:1px 4px; border-radius:2px}
  h2{font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
     color:var(--muted); margin:44px 0 14px; border-top:1px solid var(--line); padding-top:12px}
  .rule{border:2px solid var(--ink); background:var(--wash); padding:18px 22px; margin:26px 0 8px}
  .rule b{font-size:16px; display:block; margin-bottom:6px}
  .rule p{font-size:13.5px; color:var(--muted); margin-top:6px}
  .mapwrap{overflow-x:auto; border:1px solid var(--line); padding:18px 16px; background:var(--paper)}
  .mapwrap svg{display:block; min-width:812px; width:100%; height:auto}
  svg text{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; fill:var(--ink)}
  svg .bt{font-size:15px; font-weight:700}
  svg .bs{font-size:11.5px; fill:var(--muted)}
  svg .rl{font-size:10px; font-weight:700; letter-spacing:.12em; fill:var(--muted)}
  svg .al{font-size:10.5px; fill:var(--muted)}
  svg .cap{font-size:11px; fill:var(--muted)}
  .panel{border:1px solid var(--line); border-left:5px solid var(--blue); padding:18px 22px;
         margin-bottom:18px; break-inside:avoid}
  .panel.store,.panel.package{border-left-color:var(--green)}
  .panel.gates{border-left-color:var(--red)}
  .panel.self{border-left-color:var(--ink); background:var(--wash)}
  .panel h3{font-size:19px; font-weight:700; margin-bottom:4px}
  .panel .role{font-size:13.5px; color:var(--muted); max-width:74ch}
  .panel .shape{font-family:ui-monospace,Menlo,Consolas,monospace; font-size:11.5px;
                color:var(--muted); margin-top:8px; overflow-wrap:anywhere}
  table{border-collapse:collapse; width:100%; margin-top:14px; font-size:13px}
  th{text-align:left; font-size:10.5px; letter-spacing:.09em; text-transform:uppercase;
     color:var(--muted); border-bottom:1px solid var(--ink); padding:0 10px 6px 0; font-weight:700}
  td{border-bottom:1px solid var(--line); padding:8px 10px 8px 0; vertical-align:top}
  td.k{width:27%; font-weight:600}
  td.v{width:41%}
  td.p{width:32%; font-size:11.5px; color:var(--muted)}
  .un{color:var(--red); font-weight:600}
  .rc{margin-top:14px; font-size:12.5px}
  .rc b{font-size:10.5px; letter-spacing:.09em; text-transform:uppercase; color:var(--muted)}
  .rc ul{list-style:none; margin-top:6px}
  .rc li{padding:3px 0; border-bottom:1px dotted var(--line); color:var(--muted)}
  .kind{display:inline-block; font-size:10px; font-weight:700; letter-spacing:.06em;
        padding:1px 6px; margin-right:8px; border:1px solid var(--ink); color:var(--ink)}
  .kind.ABORT{background:var(--ink); color:var(--paper)}
  .kind.GATE{background:var(--amber)}
  .kind.ADVISORY{background:var(--paper); color:var(--muted); border-color:var(--line)}
  .kind.UNROUTED{background:var(--red); color:var(--paper); border-color:var(--red)}
  .nore{border:2px solid var(--red); color:var(--red); padding:10px 12px; margin-top:12px;
        font-size:13px; font-weight:600}
  .foot{margin-top:44px; border-top:1px solid var(--line); padding-top:14px; font-size:12px;
        color:var(--muted)}
  /* ⚠ Narrow layout, corrected after a 480px render was LOOKED AT: setting only `td{display:
     block}` leaves the anonymous table box sizing the cells, so the rows stacked but held ~57%
     of the width with a dead column beside them, under a three-column header that no longer
     described anything. The whole table has to leave table layout together. */
  @media (max-width:720px){ body{padding:28px 18px 56px} h1{font-size:24px}
    table,tbody,tr,td{display:block} thead{display:none}
    /* ⚠ specificity, measured: the wide rules are `td.k{width:27%}` (0,1,1), so a bare
       `td{width:auto}` here loses and the stacked cells stayed at 27% — 106px of a 394px
       table. The narrow override has to carry the class too. */
    td.k,td.v,td.p{width:auto}
    tr{padding:8px 0; border-bottom:1px solid var(--line)}
    td{border-bottom:none; padding:0 0 3px}
    td.k{font-weight:700} td.p{padding-bottom:0} table{font-size:13px; margin-top:10px} }
"""


def render(repo=ROOT):
    rows = []
    for s in SUBSYSTEMS:
        facts = s["facts"](repo)
        checks = rechecks_for(s["scripts"], repo)
        body = [f'<section class="panel {s["key"]}">',
                f'<h3>{md(s["n"])} &nbsp;{md(s["title"])}</h3>',
                f'<p class="role">{md(s["role"])}</p>',
                f'<p class="shape">{md(s["shape"])}</p>',
                '<table><thead><tr><th>what</th><th>measured now</th><th>read from</th>'
                '</tr></thead><tbody>']
        for label, val, src in facts:
            body.append(f'<tr><td class="k">{md(label)}</td><td class="v">{value_html(val)}</td>'
                        f'<td class="p">{md(src)}</td></tr>')
        body.append("</tbody></table>")
        if checks:
            body.append('<div class="rc"><b>What re-checks this — '
                        f'{len(checks)} step(s) in <code>_build_all.py</code></b><ul>')
            for lbl, kind in checks:
                body.append(f'<li><span class="kind {html.escape(kind)}">{md(kind)}</span>'
                            f'{md(lbl)}</li>')
            body.append("</ul></div>")
        else:
            body.append('<p class="nore">⛔ NOTHING RE-CHECKS THIS — no step in '
                        '<code>_build_all.py</code> runs any of this subsystem\'s scripts. '
                        'A claim here can go false in silence.</p>')
        body.append("</section>")
        rows.append("\n".join(body))

    return f"""<!DOCTYPE html>
<!-- GENERATED by knowledge/_gen_schematic.py — DO NOT HAND-EDIT.
     Every figure below is read off disk at generation time. Regenerate, never patch:
       python3 knowledge/_gen_schematic.py
     `--check` asserts this committed file is byte-identical to a fresh render. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Memento — the whole mechanism ({RELEASE_DATE} {VERSION})</title>
<style>{CSS}</style>
</head>
<body>

<h1>Memento — the whole mechanism</h1>
<p class="sub">Six subsystems: chain · store · search · marks · gates · package. {RELEASE_DATE} ·
{VERSION} · <code>provenance: generated · status: observed</code></p>
<p class="sub">Generated by <code>knowledge/_gen_schematic.py</code> from the real file
inventory. Supersedes <code>{md(V1_REL)}</code>, which was hand-authored.</p>

<div class="rule">
  <b>Read every figure on this page as a measurement, not a description.</b>
  <p>The previous version of this diagram typed its numbers — “27 blocking validators in a
  55-step build”. They were true the day they were written and false within a fortnight, and
  nothing re-checked them. That is this project’s recurring defect stated exactly:
  <b>a claim that was true when it was written, has gone false, and nothing re-checks it.</b></p>
  <p>So: no number here is typed. Each one is a function that opens a real file when this page is
  generated. A figure that cannot be read renders as a red <b>⛔ UNMEASURED</b> with its reason —
  never as a zero, never as a plausible default. And every panel ends with the list of build
  steps that re-check it, computed from <code>_build_all.py</code>, so the question
  <i>“what re-checks this?”</i> is asked on every regeneration instead of being remembered.</p>
</div>

<h2>The map</h2>
<div class="mapwrap">
{svg(repo)}
</div>

<h2>The six subsystems</h2>
{"".join(rows)}

<p class="foot">Regenerate: <code>python3 knowledge/_gen_schematic.py</code> ·
freshness gate: <code>python3 knowledge/_gen_schematic.py --check</code> ·
bites: <code>python3 knowledge/_gen_schematic.py --selftest</code>.<br>
Nothing time-derived is rendered, deliberately: a clock in the output would make
<code>--check</code> fail on the second day for a file nobody touched, and a check that cries
wolf gets switched off. The date in the filename is a version label.</p>

</body>
</html>
"""


# =============================================================================================
# WRITE · CHECK · SELFTEST
# =============================================================================================

DATE_RE = None          # compiled lazily in selftest(); no module-level regex needed elsewhere


def write(repo=ROOT):
    text = render(repo)
    out = os.path.join(repo, OUT_REL)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    un = text.count('class="un"') + text.count("NOTHING RE-CHECKS THIS")
    print(f"  ✅ {OUT_REL}: {len(text):,} bytes · {un} declared gap(s) rendered")
    return 0


def check(repo=ROOT, out_path=None):
    """Freshness — regenerate in memory and demand BYTE identity with the committed file.

    ⚠ Compares CONTENT, never mtime: the retrieval index was bitten by exactly that (#32).
    A stale schematic is the v1 failure verbatim, so this is the whole point of the module.
    """
    out = out_path or os.path.join(repo, OUT_REL)
    shown = os.path.relpath(out, repo) if out_path is None else out   # name the file ACTUALLY read
    if not os.path.exists(out):
        print(f"  ✗ {shown} is MISSING — run `python3 knowledge/_gen_schematic.py`")
        return 1
    with open(out, encoding="utf-8") as f:
        have = f.read()
    # #193 — the tier question, BEFORE the render and the byte compare (see `tier_refusal`).
    refused = tier_refusal(shown, have)
    if refused is not None:
        return refused
    text = render(repo)
    if have != text:
        import difflib
        d = [l for l in difflib.unified_diff(have.splitlines(), text.splitlines(),
                                             "committed", "fresh", n=0, lineterm="")][:12]
        print(f"  ✗ {shown} is STALE — a figure in it no longer matches disk, so the page is "
              f"asserting something that has gone false. Regenerate and stage it.")
        for line in d:
            print(f"      {line[:160]}")
        return 1
    print(f"  ✅ {shown} is FRESH — byte-matches a render against the live tree")
    return 0


def selftest():
    """Bites. A `--check` that cannot fail is an assertion, not a test — so arms 5-8 BREAK
    something and demand a red."""
    import re
    import tempfile
    fails = []

    def bite(what, ok):
        print(f"    {'✓' if ok else '✗'} {what}")
        if not ok:
            fails.append(what)

    # ---- #193: THE TIER QUESTION IS ASKED FIRST, AND IT IS ASKED OF THE SELFTEST TOO.
    # MEASURED in a bare clone of this commit: with the key/cache absent, the caption-geometry
    # arm goes red with `worst: (39, 'chain')` — not because a caption was mis-sized, but because
    # `tape (cl100k ESTIMATE)` is 16 characters longer than `real` and the figure it labels sits
    # in a fixed box. The arms below measure a page rendered by THIS environment's instrument;
    # where that instrument cannot reproduce the committed page's unit, they are measuring a
    # different artefact and their red is a fact about the runner. So: refuse, name it, and say
    # WHERE the proof is reachable — never a silent skip, never an env-var opt-out.
    _committed = os.path.join(ROOT, OUT_REL)
    if os.path.exists(_committed):
        with open(_committed, encoding="utf-8") as _f:
            _have = _f.read()
        _ref = tier_refusal(
            f"{OUT_REL} --selftest", _have,
            extra=" ⇒ THESE BITES ARE NOT SKIPPED, THEY ARE UNASKABLE HERE: they are asked in "
                  "full wherever `real` is reachable (any session holding `API-KEY.txt` or the "
                  "token cache), and that run is the proof of record.")
        if _ref is not None:
            return _ref

    text = render(ROOT)
    bite("renders against the live repo without refusing wholesale", len(text) > 6000)

    # 1 — determinism. `--check` is meaningless without it.
    bite("two consecutive renders are byte-identical (determinism)", render(ROOT) == text)

    # 2 — NO CLOCK. A wall-clock value would make --check fail on day two for an untouched file.
    dates = set(re.findall(r"\d{4}-\d{2}-\d{2}", text)) - {RELEASE_DATE, "2026-07-26"}
    bite(f"no unexpected date-shaped string in the output (found {sorted(dates)})", not dates)

    # 3 — ONE SLICER. This module's row reader must agree with `_gen_chain._steps_in`, the
    #     function `_CHAIN.md`'s banner counts with. Two readers of one object that are never
    #     compared is the drift class, not a redundancy.
    import _gen_chain as gc
    n_canon, _d, why = gc.build_steps_now(ROOT)
    bite(f"step count agrees with _gen_chain._steps_in ({len(build_rows(ROOT))} vs {n_canon})",
         n_canon is not None and len(build_rows(ROOT)) == n_canon)

    # 4 — every step is ROUTED, so no badge in the page is a guess.
    # ⚠ SCOPE, learned from a mutation that did NOT bite: deleting a ROUTE_ROWS row for
    # `gen_runbook_index.py` left this arm GREEN, because that step belongs to no subsystem and
    # so is never RENDERED. The rendered-page arm can only see the ~36 steps it prints — it is a
    # true claim about the ARTEFACT and was being read as a claim about the BUILD
    # [[mutation-tests-the-clause-not-the-feature]]. Both are asserted now, separately and named.
    bite("no step RENDERED on the page carries an UNROUTED badge",
         'class="kind UNROUTED"' not in text)
    kinds = route_kinds(ROOT)
    unrouted = [l for l, _s, _a in build_rows(ROOT) if l not in kinds]
    bite(f"and the STEPS ↔ ROUTE_ROWS join is TOTAL over all {len(build_rows(ROOT))} steps, "
         f"rendered or not ({len(unrouted)} unrouted)", not unrouted)

    # 5 — the re-check reader DISCRIMINATES. A reader that always returned rows could not
    #     produce the red "NOTHING RE-CHECKS THIS" arm, and a reader that always returned []
    #     would paint the whole page red. Both arms are asserted.
    bite("rechecks_for finds real steps for a wired script (_gen_chain.py)",
         len(rechecks_for(("_gen_chain.py",), ROOT)) > 0)
    bite("rechecks_for returns EMPTY for a script with no step (the red arm can fire)",
         rechecks_for(("__no_such_script__.py",), ROOT) == [])

    # 6 — MUTATION: a hand-patched artefact must fail `check`. This is the exact v1 defect —
    #     someone edits a figure in the HTML instead of regenerating — so it gets a real bite.
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "out.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        bite("check() PASSES on a faithful copy", check(ROOT, out_path=p) == 0)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text.replace("</body>", "<p>27 blocking validators</p></body>"))
        patched_rc = check(ROOT, out_path=p)
        bite("check() FAILS on a hand-patched copy (mutation)", patched_rc == 1)
        # ★ #193 — THE ARM THAT KEEPS THE REFUSAL HONEST. The mutation above leaves every unit
        # word AGREEING with this environment, so the tier clause must NOT fire: a real content
        # break on the reachable tier is a FAILURE (1), never a refusal (77). A gate whose
        # could-not-ask path swallows its own purpose is worse than the disease it cures.
        bite("and that failure is a FAILURE, not a refusal — the tier clause does not swallow "
             "a real staleness on the reachable tier", not cna.is_refusal(patched_rc))
        # ★ #193 — THE OTHER DIRECTION. Rewriting the copy's UNIT WORDS to a tier this
        # environment cannot reach reproduces the #173 divergence exactly, and bites on ANY
        # machine — driving it by removing the API key would only bite where `real` is reachable
        # in the first place, i.e. the arm would be unreachable in the very environment the
        # defect lives in [[gate-cannot-pass-in-one-environment]].
        gc_units = gc._UNIT_WORDS
        here_tier = _measurer().measurement_tier()
        other = next(t for t in gc_units if t != here_tier)
        moved = text.replace(f" {gc_units[here_tier]}", f" {gc_units[other]}")
        bite("the unit-word mutation actually changed the file (a plant that did not plant "
             "would make the arms below assertions)", moved != text)
        with open(p, "w", encoding="utf-8") as f:
            f.write(moved)
        bite("stamped_tiers() reads the MUTATED page back as the other tier",
             other in stamped_tiers(moved) and here_tier not in stamped_tiers(moved))
        import contextlib as _ctx
        import io as _io
        _buf = _io.StringIO()
        with _ctx.redirect_stdout(_buf):
            tier_rc = check(ROOT, out_path=p)
        tier_out = _buf.getvalue()
        bite("check() REFUSES (exit 77) when the committed page's unit is unreachable here",
             cna.is_refusal(tier_rc))
        bite("and it does NOT call it STALE — a tier divergence is a measurement problem, and "
             "naming it staleness is the #173 defect reproduced",
             "STALE" not in tier_out.upper() and cna.MARKER in tier_out)
        bite("the refusal NAMES BOTH instruments, so a reader can see which two disagreed",
             gc_units[other] in tier_out and gc_units[here_tier] in tier_out)
        os.remove(p)
        bite("check() FAILS when the artefact is missing", check(ROOT, out_path=p) == 1)

    # 7 — MUTATION: an unreadable source must REFUSE BY NAME, not crash and not default.
    #     Built by pointing the readers at an EMPTY tree, which is the cheapest honest break.
    #     ⚠ The first draft of this arm asserted that ALL store facts refuse, and it went red
    #     against a healthy repo — because one of them (`LEGACY_IDS`) reads a CODE CONSTANT, not
    #     a repo file, so an empty tree cannot break it. The over-broad assertion was the bug,
    #     not the reader. Rewritten to PAIR a live run against a dead one, which discriminates:
    #     file-backed facts must flip to Unmeasured, and the constant-backed one must NOT — so
    #     the bite also fails if a constant quietly becomes file-backed, or vice versa.
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "knowledge"))
        live = facts_store(ROOT)
        dead = facts_store(tmp)
        bite("a missing store never raises — every fact is a str or an Unmeasured",
             all(isinstance(v, (str, Unmeasured)) for _l, v, _s in dead))
        flipped = [(l, v) for (l, v, _s) in dead if isinstance(v, Unmeasured)]
        held = [l for (l, v, _s) in dead if not isinstance(v, Unmeasured)]
        bite(f"file-backed facts flip to Unmeasured on an empty tree ({len(flipped)} of "
             f"{len(dead)})", len(flipped) >= 5)
        bite("every refusal NAMES its cause (exception type + message, not a bare 'error')",
             all(len(v.why) > 12 and ":" in v.why for _l, v in flipped))
        bite(f"the ONLY fact that survives an empty tree is the code constant ({held})",
             held == ["the inherited debt"])
        same = dict((l, v) for l, v, _s in live)
        bite("and it returns the SAME value in both trees (it is not repo-derived)",
             same["the inherited debt"] == dict((l, v) for l, v, _s in dead)["the inherited debt"])
        bite("an Unmeasured renders as a visible ⛔ cell, never as a number",
             'class="un"' in value_html(flipped[0][1]) and "⛔" in value_html(flipped[0][1]))

    # 7b — MAP CAPTIONS MUST FIT THEIR BOX. Found by SEEING the first render: a caption ran
    #      straight out through the box border while the probe passed, because the probe only
    #      checked the SVG viewBox. Two repairs, both kept: this width bite, and a `data-right`
    #      attribute on every `<text>` so an external render probe can assert containment too.
    #      ⚠ The cap is COMPUTED from BOX_W (`CAP_CHARS`) — an earlier draft typed 32 and a
    #      mutation shrinking BOX_W to 150 left this arm green while every caption overflowed.
    caps = {k: v for k, v in headlines(ROOT).items() if not isinstance(v, Unmeasured)}
    long = {k: len(v) for k, v in caps.items() if len(_plain(v, cap=10 ** 6)) > CAP_CHARS}
    bite(f"every map caption fits its box at CAP_CHARS={CAP_CHARS} (worst: "
         f"{max(((len(v), k) for k, v in caps.items()), default=(0, '-'))})", not long)
    #      ⚠ The first draft of this arm asserted a TYPED difference between two counts and was
    #      simply wrong arithmetic — a bite that fails for a reason unrelated to what it guards
    #      is noise. It now asserts the INVARIANT instead: every box label carries the attribute.
    boxed = text.count('class="bt"') + text.count('class="bs"')
    bite(f"every box label declares the inside edge of its own box ({boxed} labels, "
         f"{text.count('data-right')} attributes)", boxed == text.count("data-right") and boxed > 0)

    # 8 — the artefact must be able to say the ugly thing about ITSELF.
    self_facts = {l: v for l, v, _s in facts_self(ROOT)}
    bite("the page reports its OWN re-check status (red while unwired, computed either way)",
         "what re-checks THIS file" in self_facts)
    # ⚠ the self-tally must NOT claim to cover the panel it lives in
    bite("the figure tally names its own scope (it excludes this panel, and says so)",
         any(k.startswith("figures in the six subsystem panels") for k in self_facts))

    if fails:
        print(f"  ✗ _gen_schematic selftest: {len(fails)} bite(s) failed")
        return 1
    print("  ✅ _gen_schematic selftest: all bites pass")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--check" in sys.argv:
        sys.exit(check())
    sys.exit(write())
