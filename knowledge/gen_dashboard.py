#!/usr/bin/env python3
"""
gen_dashboard.py — the generated progress dashboard ("mission control").

RULED by Dave at #164: *"this is a priority after the side quest, it will really help
me"*. Brief: `_BRIEF-progress-dashboard-2026-08-13-v1.md`. Two design rulings, his:
(1) the component library is **Mono** — the page consumes `knowledge/canon/canon.css`'s
gated `.cn-*` component scopes and `canon/type.css` composites, inventing nothing;
(2) the aesthetic is the **swiss-design-system** skill — typographic grid, hairline
section rules, the accent-dash label pattern, white space as structure.

SAME LAW AS THE SHOWROOM: built FROM THE STORES, never hand-edited, regenerated as a
build step, so it cannot rot. If a number is wrong, the store is wrong — fix the store
and regenerate. The dashboard REPORTS; it never repairs.

Sources (every panel names its own):
  knowledge/_state.json        — open work, owners, close conditions, the 19-item
                                 UNCONDITIONED legacy set
  knowledge/_rulings.json      — the ruling count and the tail
  knowledge/_governs.py        — RUN here, never asserted: the provenance-gap set
  knowledge/_binds-ratchet.json, knowledge/_type_ratchet.json — the debt ratchets
  _CHAIN.md, _LIVE-STATE.md    — session position
  _FUTURE-STATE.md             — the forward lane
  live gate runs               — the gates-health strip is MEASURED at generation

PRIORITY (#165, Dave: *I generate the priorities, he overrules*):
  The order on this page is a SCORE COMPUTED HERE from the weighted criteria in
  `CRITERIA`, whose weights are printed on the page. (The COUNT is deliberately not
  written down in prose anywhere — it was "six" until Dave's #168 DC2 dropped effort,
  and a typed count goes stale the moment a criterion moves [[premise-ages-faster-than-rule]].
  Every sentence that needs the number now computes `len(CRITERIA)`.) It is labelled PROPOSAL on every surface it touches,
  it is never written back to a store, and it is regenerated every build — so it cannot
  rot into a decision. Dave overrules with an OPTIONAL `priority_override` integer on a
  `_state.json` item (1 = first), validated when present by `_state.py` and displayed as
  "DAVE OVERRULED → n". ⛔ No override value is authored by this program, ever.
  Where an input does not exist in the store the item is scored AND flagged LOW
  CONFIDENCE with the missing inputs NAMED — `links` is empty across the corpus, which
  is measured and reported on the page as a flagged problem, not repaired here.

DETERMINISM: no timestamps, no git sha. The page's only clock is the session number it
reads out of `_CHAIN.md` plus the measurements themselves, so `--check` means "the
dashboard disagrees with the stores or with a live gate", never "a day has passed".

ACCESSIBILITY LAW APPLIED (standing, Dave):
  * dyslexia — exec summary FIRST, in prose, at 21px; no bullet walls above the fold
  * astigmatism — **no meaning is ever carried by hue alone.** Every verdict is a WORD
    (PASS / FAIL / DEBT / DAVE'S / MINE). Colour is redundant confirmation only.
  * two-red law (s151-D1) + the green mirror (s155-D1), MONO ONLY, light background:
    red #DA1A00-on-white, green #137F3C-on-white. Dark values (#F6604C / #66CC8D) are
    NOT used because this page renders light-only — declared, not smuggled.
  * the Swiss accent is #305A85, a blue already in the repo's legacy information fill.
    It is DECORATIVE ONLY (label dashes, rules) and carries no status meaning — blue
    and green are Dave's stable hues.

Usage:
  python3 knowledge/gen_dashboard.py            # write dashboard/index.html
  python3 knowledge/gen_dashboard.py --check    # regenerate, compare, rc=1 if stale
  python3 knowledge/gen_dashboard.py --no-gates # skip the live gate runs (fast draft)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import concurrent.futures as _fut
import html as htmlmod
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# The gate module is imported, not re-described. The `effort` field NAME and its legal rung
# VALUES have exactly one definition (`_state.py`), and a scorer that spelled them itself
# would keep scoring a vocabulary the gate had moved on from [[ban-scoped-to-a-name]].
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import _state  # noqa: E402 - after the path insert, by necessity
import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity
OUTD = os.path.join(ROOT, "dashboard")
OUT = os.path.join(OUTD, "index.html")

E = lambda s: htmlmod.escape(str(s), quote=True)          # noqa: E731

# ---------------------------------------------------------------------------
# PROJECT — s172-D1, Dave, #172. Every `_state.json` item carries a stored `project`
# ('apollo' | 'memento'), gated on the way in by `_state.py`. This page RENDERS it and
# offers a filter; it does not assign, infer or repair one.
#
# ⚠ THE LABEL IS A WORD, NEVER A HUE. Standing accessibility law on this page: no meaning
# is carried by colour alone, and red/yellow are Dave's unstable hues besides. The project
# tag is the literal word APOLLO or MEMENTO in the ink colour, boxed by a hairline exactly
# like the owner tag beside it — the box is structure, not signal.
#
# ⛔ THE ENUM IS IMPORTED, NOT RESPELLED. `_state.PROJECT_VALUES` is the one definition;
# a label map typed here that grew a third key would render a project the gate refuses,
# and one that lost a key would silently render nothing [[ban-scoped-to-a-name]]. The map
# below is CHECKED against the gate's enum at build time and the build REFUSES on a fork.
PROJECT_LABEL = {"apollo": "APOLLO", "memento": "MEMENTO"}

# ⬛ THE TWO AMBIGUOUS DEFAULTS — DAVE'S CALL, FLAGGED IN WORDS ON THE PAGE.
# The 37 assignments written into the store at #172 are DEFAULTS proposed for Dave's eye.
# Two of them were declared ambiguous at proposal time and are marked `check` next to their
# label so his eye lands on them first.
#
# ⚠ WHY THIS LIVES HERE AND NOT IN THE STORE. An `ambiguous: true` field in `_state.json`
# would read back as a fact ABOUT THE ITEM. It is not: it is a statement about the
# CONFIDENCE OF MY OWN GUESS, and inscribing my uncertainty as store state is how a guess
# becomes a datum [[feedback-measuring-tool-must-not-guess]]. It is a rendering annotation,
# it is regenerated every build, and it is DELETED — not edited — the moment Dave rules
# the two items, because at that point the flag is answered, not merely stale.
#
# ⛔ AND IT CANNOT POINT AT A GHOST: `build()` REFUSES if an id here is not in the store.
PROJECT_CHECK = ("W-14", "G12")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# GATES — RUN, never asserted. Read-only invocations only.
#
# ⛔ `_validate_type_composites.py --ratchet` is DELIBERATELY NOT USED: it WRITES
# _type_ratchet.json when the count shrinks, and a reporting surface must not mutate a
# store. We run the plain (read-only) gate, read the baseline, and compute the
# comparison here — labelled as computed, with the owning gate named.
# ---------------------------------------------------------------------------
GATES = [
    ("snippets",        ["_validate_snippets.py"],              "every snippet against the canon contract"),
    ("binds-resolve",   ["_validate_binds_resolve.py"],         "every binds address resolves to a real token leaf"),
    ("binds-ratchet",   ["_validate_binds_ratchet.py"],         "metas carrying binds may only grow"),
    ("palette-tier",    ["_validate_palette_tier.py"],          "every theme names a palette per family (s157-D2)"),
    ("theme-cascade",   ["canon/gen_theme_cascade.py", "--check"], "the projected cascade matches canon.css"),
    ("showroom",        ["gen_showroom.py", "--check"],         "the 75 component pages are in sync"),
    ("provenance",      ["_governs.py", "--selftest"],          "every ruling points a reader at canon"),
    ("type-composites", ["_validate_type_composites.py"],       "raw type declarations outside the composites"),
]

GATE_TIMEOUT = 120


def _run_gate(spec):
    name, argv, why = spec
    env = dict(os.environ)
    env.setdefault("TMPDIR", "/var/tmp")                       # ENOSPC pothole n=6/n=7
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, argv[0])] + argv[1:],
                           cwd=ROOT, env=env, capture_output=True, text=True,
                           timeout=GATE_TIMEOUT)
        rc, out = p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        rc, out = 124, "TIMEOUT after %ds — no verdict" % GATE_TIMEOUT
    except Exception as exc:                                   # a crash is not a fail
        rc, out = 125, "CRASHED, NAMED: %s" % exc
    lines = [ln.rstrip() for ln in out.splitlines() if ln.strip()]
    headline = lines[-1] if lines else "(no output)"
    return {"name": name, "why": why, "rc": rc, "headline": headline,
            "cmd": "python3 knowledge/" + " ".join(argv), "lines": lines}


def run_gates(enabled=True):
    if not enabled:
        return []
    with _fut.ThreadPoolExecutor(max_workers=len(GATES)) as ex:
        return list(ex.map(_run_gate, GATES))


# ---------------------------------------------------------------------------
# ★ #193 — WHY `--check` HAD TO GAIN A COULD-NOT-ASK PATH, MEASURED BEFORE IT WAS BUILT.
#
# This page BAKES LIVE GATE RESULTS (the eight above) into its own prose: "11 checks, 4 rulings,
# nobody else's to answer" is not a store read, it is `_governs.py --selftest`'s verdict rendered
# as a sentence. So `--check` is only a question about the STORES when this environment can run
# those gates on the same inputs.
#
# It cannot. Single-variable isolation, a bare clone of this very commit vs. the working tree:
# the clone renders "14 checks, 6 rulings" and three extra FAIL lines, every one of them of the
# form *"ruling ds-034 points at `outputs/_FINDING-…-v1.md` … which does not exist"*. Those
# evidence files exist here and are NOT TRACKED BY GIT, so a checkout cannot have them. Nothing
# about the dashboard, the stores, or the rulings changed — the gate was answering a different
# question because it was looking at a different tree, and `--check` reported that as
# "dashboard/index.html is OUT OF SYNC", an accusation aimed at the artefact
# [[gate-cannot-pass-in-one-environment]].
#
# ⇒ THE CLAUSE: when the page differs AND a live gate's own output names a path OUTSIDE THE
# COMMITTED TREE, `--check` refuses (COULD-NOT-ASK) and NAMES the gate and the path. It does not
# say the page is stale, because it cannot know.
# ⛔ KEYED ON THE UNTRACKED PATH, NEVER ON "am I in CI". Commit those evidence files and this
# environment answers again — on any machine, with no env var anywhere in the path.
# ⚠ AND IT STILL BITES: with no untracked path named by any gate, a real divergence is still a
# FAILURE (exit 1). Both directions are driven in `refusal_selftest()`.
# ⚠ The extension must be ALPHABETIC. The first cut allowed `[A-Za-z0-9]` and duly reported the
# contrast ratio `5.22/17.40` as an untracked path — a refusal keyed on noise is a refusal that
# will one day fire for no reason, which is exactly how a gate stops being read.
_PATHLIKE = re.compile(r"[`'\"]([A-Za-z0-9_][A-Za-z0-9_./\-]*\.[A-Za-z]{1,5})[`'\"]")


def untracked_inputs(gates, repo=ROOT):
    """`[(gate_name, path), …]` — repo-relative paths a live gate NAMED that git does not track.

    An untracked path is an input this environment may have and a checkout cannot (or the exact
    reverse), so any verdict resting on it is a verdict about the runner. ⚠ Refuses to guess: if
    `git` itself cannot be asked, that is returned as its own named entry rather than silently
    yielding an empty list, which would read as "all inputs are committed"
    [[measuring-tool-must-not-guess]].

    ★ #221 — A BARE BASENAME IS A NAME, NOT A ROOT-RELATIVE PATH.
    `git ls-files -- _inscribe_ruling.py`, asked from the repo root, answers *"is that file
    tracked AT THE ROOT"* — and it is not; it lives at `knowledge/_inscribe_ruling.py`. Gates
    name their siblings by bare name as a matter of course (`_governs.py --selftest`'s remedy
    sentence is the live instance), so the exact-path question classified a **tracked** file as
    untracked, `mismatch_verdict()` refused on every single run where the page differed, and its
    FAIL branch became UNREACHABLE — a BLOCKING build step that could not accuse its own
    artefact [[instrument-without-a-consumer]]. The clause the refusal is FOR is unchanged: a
    token carrying a slash still asks the exact-path question; a bare token is asked *"is a file
    of this NAME tracked anywhere in the tree?"* and is only reported when the answer is no.
    """
    cand = {}
    for g in gates or []:
        for ln in g.get("lines", []):
            for m in _PATHLIKE.findall(ln):
                if m.startswith("/") or ".." in m:
                    continue
                cand.setdefault(m, g["name"])
    if not cand:
        return []
    pathspec = sorted(cand)
    pathspec += ["*/" + t for t in sorted(cand) if "/" not in t]     # bare token, tracked ANYWHERE
    try:
        p = subprocess.run(["git", "ls-files", "--"] + pathspec, cwd=repo,
                           capture_output=True, text=True, timeout=30)
        if p.returncode != 0:
            return [("git", "REFUSED: `git ls-files` exited %d (%s) — which inputs are committed "
                            "is UNKNOWN here" % (p.returncode, p.stderr.strip()[:120]))]
        tracked = set(p.stdout.split("\n"))
    except Exception as exc:                                   # a crash is not a fail
        return [("git", "REFUSED, NAMED: %s — which inputs are committed is UNKNOWN here" % exc)]
    names = set(os.path.basename(t) for t in tracked if t)
    def _missing(path):
        return path not in tracked if "/" in path else path not in names
    return sorted((gate, path) for path, gate in cand.items() if _missing(path))


def mismatch_verdict(gates):
    """The verdict when the rendered page differs from the committed one: `77` when a live gate
    read an input outside the committed tree, else `1`. Extracted so BOTH branches are driven by
    `refusal_selftest()` rather than asserted about — a refusal path nothing exercises is the
    [[instrument-without-a-consumer]] class, and a refusal that swallows the staleness verdict is
    worse than the staleness.
    """
    outside = untracked_inputs(gates)
    if outside:
        named = "; ".join("%s names `%s`" % (g, p) for g, p in outside[:6])
        more = "" if len(outside) <= 6 else " (and %d more)" % (len(outside) - 6)
        return cna.refuse(
            "dashboard/index.html",
            "the page differs, but a live gate baked into it is reading INPUTS OUTSIDE "
            "THE COMMITTED TREE, so its verdict — and therefore this page — cannot be "
            "reproduced here: %s%s. Every one of those paths is untracked, so an "
            "environment that has them and one that does not will render different "
            "prose from the SAME commit. This is a REFUSAL, not a staleness verdict in "
            "either direction: the page's agreement with the stores is UNKNOWN here and "
            "is reported as unknown. Ask it where those inputs are present (a working "
            "tree that holds them), or commit them." % (named, more))
    print("gen_dashboard --check FAIL — dashboard/index.html is OUT OF SYNC with the "
          "stores or with a live gate result. Re-run `python3 knowledge/gen_dashboard.py`.")
    return 1


def refusal_selftest(arm):
    """#193 arms, driven through the real functions. `arm(name, ok, detail)` is the caller's."""
    real_fail = [{"name": "provenance", "lines": [
        "FAIL _governs: ruling ds-034 is missing a `status` value",
        "FAIL _governs: ruling ds-035 points at `knowledge/_rulings.json` (in "
        "`knowledge/_rulings.json…`) which does not exist"]}]
    # ★ DIRECTION 1 — the refusal must NOT fire when every path a gate named is committed. This
    # is the arm that stops the cure being worse than the disease: a real divergence still FAILS.
    import io as _io0
    import contextlib as _ctx0
    with _ctx0.redirect_stdout(_io0.StringIO()):    # the FAIL lines below are arms, not verdicts
        tracked_rc, empty_rc = mismatch_verdict(real_fail), mismatch_verdict([])
    arm("a mismatch whose gate output names only TRACKED paths is a FAILURE (1), not a refusal",
        untracked_inputs(real_fail) == [] and tracked_rc == 1,
        "untracked_inputs saw %r" % (untracked_inputs(real_fail),))
    arm("…and with no gate output at all it is STILL a failure (no gates, no excuse)",
        empty_rc == 1, "an empty gate set produced a refusal")
    # ★ DIRECTION 2 — the refusal fires on the input that is genuinely unreachable elsewhere.
    ghost = "outputs/__no_such_evidence_file_2026__.md"
    unreachable = [{"name": "provenance", "lines": [
        "FAIL _governs: ruling ds-034 points at `%s` which does not exist" % ghost]}]
    found = untracked_inputs(unreachable)
    arm("an UNTRACKED path named by a live gate is detected, and attributed to its gate",
        found == [("provenance", ghost)], repr(found))
    import io as _io
    import contextlib as _ctx
    _b = _io.StringIO()
    with _ctx.redirect_stdout(_b):
        rc = mismatch_verdict(unreachable)
    out = _b.getvalue()
    arm("…and that mismatch REFUSES with the convention's exit code (77), never 1",
        cna.is_refusal(rc), "got %r" % rc)
    arm("the refusal is machine-readable and NAMES the gate and the path",
        (cna.reason_in(out) or "").startswith(cna.MARKER) and ghost in out and "provenance" in out,
        out[:200])
    arm("the refusal does NOT accuse the page of being out of sync",
        "OUT OF SYNC" not in out, out[:200])
    # ★ DIRECTION 3 (#221) — THE BARE BASENAME, both ways. This is the arm that keeps the FAIL
    # branch reachable: `_governs.py --selftest` names `_inscribe_ruling.py` by bare name on
    # every run, and while that read as untracked the gate could return 0 or 77 and never 1.
    sibling = [{"name": "provenance", "lines": [
        "remedy: inscribe it with `_inscribe_ruling.py` — never by hand"]}]
    import io as _io1
    import contextlib as _ctx1
    with _ctx1.redirect_stdout(_io1.StringIO()):
        bare_rc = mismatch_verdict(sibling)
    arm("a BARE BASENAME that is tracked somewhere in the tree is NOT an untracked input",
        untracked_inputs(sibling) == [], repr(untracked_inputs(sibling)))
    arm("…so a mismatch whose only named token is a tracked sibling FAILS (1), never refuses (77)",
        bare_rc == 1, "got %r — the FAIL branch is unreachable again" % (bare_rc,))
    ghost_bare = "__no_such_sibling_2026__.py"
    bare_absent = [{"name": "provenance", "lines": [
        "FAIL _governs: run `%s` first" % ghost_bare]}]
    arm("…and a bare basename tracked NOWHERE is still detected, so the refusal keeps its clause",
        untracked_inputs(bare_absent) == [("provenance", ghost_bare)],
        repr(untracked_inputs(bare_absent)))


# ---------------------------------------------------------------------------
# STORE READS
# ---------------------------------------------------------------------------
def read_state():
    s = _json(os.path.join(HERE, "_state.json"))
    items = s["items"]
    return {
        "items": items,
        "open": [i for i in items if i["state"] == "open"],
        "blocked": [i for i in items if i["state"] == "blocked"],
        "done": [i for i in items if i["state"] == "done"],
    }


def kanban_columns(items, prio=None):
    """The kanban board, DERIVED — the store has no status/lifecycle field.

    ⛔ NOTHING IS INVENTED. `_state.json` items carry no `status`, `lane`, `phase` or
    `priority` key (checked: all 37 items expose exactly id/title/body/state/opened/
    owner/condition/closes_when/links/home/provenance, plus optional owner_inferred and
    closed_by). The only lifecycle axes that EXIST are:
        * `state`      — open | blocked | done
        * `condition`  — UNCONDITIONED | stated  (i.e. whether `closes_when` is set)
    So the columns are the product of those two, and the panel SAYS SO on the page. The
    derivation is stated, not smuggled in as if the store had shipped these columns.
    """
    cols = [
        {"key": "unconditioned", "name": "No close condition",
         "rule": "state = open AND condition = UNCONDITIONED",
         "note": "the frozen legacy set — may only shrink", "items": []},
        {"key": "conditioned", "name": "Open, condition stated",
         "rule": "state = open AND condition = stated",
         "note": "has a checkable closes_when", "items": []},
        {"key": "blocked", "name": "Blocked",
         "rule": "state = blocked", "note": "the store's own word", "items": []},
        {"key": "done", "name": "Done",
         "rule": "state = done", "note": "carries closed_by", "items": []},
    ]
    by = {c["key"]: c for c in cols}
    for i in items:
        st = i.get("state")
        if st == "done":
            k = "done"
        elif st == "blocked":
            k = "blocked"
        elif i.get("condition") == "UNCONDITIONED":
            k = "unconditioned"
        else:
            k = "conditioned"
        by[k]["items"].append(i)
    for c in cols:
        if prio and c["key"] != "done":
            c["items"] = sort_by_priority(c["items"], prio)
        else:
            c["items"].sort(key=lambda x: x["id"])
    return cols


# ---------------------------------------------------------------------------
# PRIORITY — A PROPOSAL. Derived at generation, never stored.
#
# RULED by Dave (#165): *Claude generates the priorities, Dave overrules.* So this is
# computed here, regenerated every build, and can therefore not rot — and it is
# labelled PROPOSAL everywhere it appears. The overrule channel is the OPTIONAL
# `priority_override` integer on a `_state.json` item (schema #165, gated in
# `_state.py`). ⛔ NO VALUE IS AUTHORED HERE OR IN THE STORE: the field is absent on
# every item until Dave writes one. An agent that both proposes a priority and writes
# it into the store has ruled its own priority and read it back as if it were his.
#
# ⚠ CONFIDENCE IS PART OF THE NUMBER. Where a criterion's input does not exist in the
# store, the item does NOT get a clean score — it gets the score AND a LOW-CONFIDENCE
# flag naming exactly which inputs were missing. A tidy number computed from thin data
# is the failure this whole page exists to avoid [[measuring-tool-must-not-guess]].
# ---------------------------------------------------------------------------
DEADLINE_SET = "Friday 2026-08-14"
_RISK_RE = re.compile(r"\b(gate|gates|validate|selftest|test|instrument|ratchet|"
                      r"mutation|coverage|regress)", re.I)
_DEADLINE_RE = re.compile(r"\b(friday|2026-08-1[34]|deadline|before the wrap)\b", re.I)
_DECISION_RE = re.compile(r"\b(dave|rule[sd]?|ruling|decide|decision|ratif|approve|"
                          r"his word|overrule)", re.I)

# ⛔ THE EFFORT CRITERION IS GONE — Dave's #168 review export, DC2 (s168-D1 PENDING, minted
# at the #168 wrap, not here). What it removed is the LENGTH PROXY: `1 − len(body)/1200`,
# weight 0.15. Dave's objection is the one the proxy's own page text already admitted — it
# measures the PROSE, not the work — and until real `effort` values exist there is nothing
# else for that criterion to read. A criterion whose only input is a proxy Dave has rejected
# does not get to keep 15% of the vote [[measuring-tool-must-not-guess]].
#
# HOW THE REMAINING WEIGHT IS HANDLED: PROPORTIONAL RENORMALIZATION, declared here.
#   · Leaving the five raw weights as-is is not an available option — they sum to 0.85, and
#     the build gate at the bottom of this file REFUSES a score presented as /100 whose
#     weights are not a weighted mean. So "leave as-is" would have to be enacted as
#     "silently print a score out of 85 and call it 100", which is the defect, not the fix.
#   · Re-typing five new absolute weights would be me re-weighting Dave's criteria under
#     cover of a deletion. He accepted the ranking SHAPE at DC3 in the same export.
#   ⇒ Least-surprising: keep his RATIOS exactly (30:20:15:10:10) and divide by their sum.
#     Every surviving pair of criteria stands in precisely the relationship he accepted; the
#     only thing that changed is that effort's 0.15 is no longer in the denominator.
#
# ⚠ The gated OPTIONAL `effort` FIELD MECHANISM IS INTACT and deliberately untouched:
# `_state.py` still validates it, `EFFORT_SCORE` still exists, and the page still COUNTS how
# many items carry one. What no longer exists is a code path that READS it into the score. If
# a real `effort` value ever lands, whether and how it re-enters the ranking is a DESIGN
# QUESTION FOR DAVE, not a hole for an agent to fill — the field is left unread on purpose.

# (key, column name, RAW RATIO, what it measures, where the input comes from)
_CRITERIA_RAW = [
    ("unlock",   "Unlock",          0.30,
     "how much other work this item is blocking",
     "the item's <code>links</code> array, plus inbound links from other items"),
    ("rot",      "Rot risk",        0.20,
     "cost of delay — how long it has been open, and whether it can even be closed",
     "<code>opened</code> (session number) and <code>condition</code>"),
    ("deadline", "Deadline",        0.15,
     "proximity to the %s set" % DEADLINE_SET,
     "the item's OPTIONAL <code>deadline</code> (ISO date) where present — otherwise "
     "<strong>PROXY ONLY</strong>: a prose scan of <code>title</code>/<code>body</code>/"
     "<code>closes_when</code>."),
    ("risk",     "Risk reduction",  0.10,
     "does closing this close a gate-coverage hole",
     "PROXY ONLY — prose signal (gate / selftest / ratchet / coverage)"),
    ("load",     "Decision relief", 0.10,
     "does finishing this take a decision OFF Dave's plate",
     "<code>owner</code> plus a prose scan for a pending decision"),
]

# The renormalization itself. COMPUTED, never typed — a hand-typed 0.3529 would be a number
# nobody could attribute back to Dave's 0.30 [[measure-dont-convert-units]].
_RATIO_SUM = sum(c[2] for c in _CRITERIA_RAW)
CRITERIA = [(k, n, w / _RATIO_SUM, d, s) for k, n, w, d, s in _CRITERIA_RAW]
WEIGHTS_SUM = round(sum(c[2] for c in CRITERIA), 4)   # must be 1.0; asserted at build

# ---- EFFORT RE-ENTERS AS A CONDITIONAL CRITERION (#168, Option C — s168-D2 PENDING) ---------
# Dave adopted Option C of `notes/_PROPOSAL-effort-gauge-2026-08-13-v1.md`. The ruling is
# minted at the #168 WRAP, by the conductor, NOT here — until then this is machinery standing
# ready, and the store is empty of values, so nothing it does is visible in the ranking yet.
#
# ⛔ WHAT DID **NOT** COME BACK: the length proxy. `1 − len(body)/1200` is gone and stays gone.
# The criterion below reads ONE input — the gated `effort` rung — and when there is no rung
# there is no criterion. A blend of a real input and a rejected proxy is unattributable.
#
# THE COMPANION CLAUSE, which is half the ruling: **absent `effort` ⇒ the criterion DROPS OUT
# and the remaining weights RENORMALIZE.** It is scored as nothing, not as zero: an item with
# no rung is not an item of infinite effort [[measuring-tool-must-not-guess]]. This is the same
# renormalization DC2 already installed above — raw ratios kept verbatim, divided by the sum of
# the ones actually in play — reused, not re-invented, and now evaluated PER ITEM instead of
# once for the module.
#
# ⇒ Two consequences worth stating plainly, because both are easy to read the wrong way:
#   · With effort ABSENT (37/37 items today) the active set is exactly `_CRITERIA_RAW`, the
#     sum is exactly 0.85, and the weights are BIT-IDENTICAL to DC2's. Today's page cannot
#     move. That is the control this change was proven against, not a hope.
#   · With effort PRESENT the active sum is 1.00, so the other five snap back to Dave's own
#     ratified absolutes (0.30 / 0.20 / 0.15 / 0.10 / 0.10) and effort takes 0.15. No new
#     number is typed in either direction — 30:20:15:10:10:15 are his.
#   ⚠ Therefore a PARTIALLY authored store scores two populations under two weightings. That
#     is honest (each item is scored on what it has) but it is NOT a clean comparison, and the
#     page says so where it counts them.
_EFFORT_RAW = ("effort", "Effort (inverse)", 0.15,
               "how big the job is, ESTIMATED in real Claude tokens of job window",
               "the item's OPTIONAL gated <code>effort</code> rung (S/M/L), Dave-authored. "
               "<strong>No proxy</strong>: absent means the criterion does not fire at all and "
               "the remaining weights renormalize.")


def active_criteria(has_effort):
    """The criteria in play FOR ONE ITEM, weights renormalized over the raw ratios present.

    Not a lookup of two hand-written tables — one list, divided by its own sum, so the two
    cases cannot drift apart [[measure-dont-convert-units]]."""
    raw = list(_CRITERIA_RAW) + ([_EFFORT_RAW] if has_effort else [])
    tot = sum(c[2] for c in raw)
    return [(k, n, w / tot, d, s) for k, n, w, d, s in raw]


# rung → sub-score, inverse (small job scores HIGHER, because it unblocks sooner per token).
# ⚠ THE MAPPING IS DECLARED HERE AND NOWHERE ELSE. s168-D2 PENDING, Dave's #168: the rungs are
# ORDINAL — S/M/L are three named bands of job tokens, not a ratio scale — so the 1.0/0.5/0.0
# spacing is a CHOICE (equal steps), inherited unchanged from #166 rather than re-invented by
# this lane. If Dave wants L to score above 0.0, that is a one-line edit here and a ruling.
EFFORT_SCORE = {"S": 1.0, "M": 0.5, "L": 0.0}   # inverse: small scores higher

# ---- THE RUNG EDGES, DERIVED — never typed [[planning-estimate-is-not-a-measurement]] -------
GAUGE_LOG = os.path.join(ROOT, "notes", "_GAUGE-LOG.md")
_JOB_RE = re.compile(r"\bjob ([0-9][0-9,]{3,})\b")


def effort_anchors(path=GAUGE_LOG):
    """Derive the S/M/L band edges from the token-priced session blocks in `_GAUGE-LOG.md`.

    Unit: **real Claude tokens of JOB window** — boot and wrap excluded, which is what the
    log's own `boot N + job N + wrap N` pre-flight decomposition means by `job`.

    THE RULE, stated so the edges are attributable and not "numbers I liked":
      · corpus = every `job <number>` in the log (both est and measured blocks — the log does
        not separate them in a machine-readable way, and saying so is cheaper than a parser
        that guesses [[no-gate-parses-the-artefact]]);
      · S/M edge = the corpus's LOWER QUARTILE, M/L edge = its UPPER QUARTILE;
      · both rounded HARD, to the nearest 5,000, because 21 self-selected blocks out of 147
        cannot support a sharper edge than that.
    The quartiles are used rather than the mean because two 118,000 blocks (#68/#69) are
    opener ESTIMATES from before boot was measurable and would drag any mean upward.

    ⛔ Fails LOUD and NAMED — a crash is not a fail [[a-crash-is-not-a-fail]]. Read-only: this
    function must never write to the gauge log, whose block grammar is gated by
    `_build_memento_index.py` (ds-024)."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        raise SystemExit("gen_dashboard REFUSING: cannot read the gauge log at %s (%s). The "
                         "effort rung edges are DERIVED from it; typing them here instead "
                         "would be inventing the measurement the rungs exist to carry."
                         % (os.path.relpath(path, ROOT), e))
    vals = sorted(int(m.group(1).replace(",", "")) for m in _JOB_RE.finditer(text))
    if len(vals) < 8:
        raise SystemExit("gen_dashboard REFUSING: only %d token-priced `job` blocks found in "
                         "%s — a quartile over fewer than 8 points is a number with a "
                         "decimal point, not a band edge." % (len(vals), os.path.relpath(path, ROOT)))

    def _q(p):                       # linear-interpolated quantile, then rounded HARD
        k = (len(vals) - 1) * p
        f = int(k)
        lo, hi = vals[f], vals[min(f + 1, len(vals) - 1)]
        return lo + (hi - lo) * (k - f)

    rnd = lambda x: int(round(x / 5000.0) * 5000       # noqa: E731 - the hard rounding, once
                        )
    return {"n": len(vals), "min": vals[0], "max": vals[-1],
            "median": vals[len(vals) // 2],
            "s_edge": rnd(_q(0.25)), "l_edge": rnd(_q(0.75)),
            "source": os.path.relpath(path, ROOT)}


# ---- the REAL inputs (#166), where present. Gated in `_state.py`; ABSENT on every item
# until Dave writes one, so today every one of these paths is dark. `EFFORT_SCORE` and the
# rung machinery moved UP, next to `active_criteria()` — one place, above their first use.
# ⚠ `deadline` still falls back to a PROSE PROXY when absent; `effort` no longer falls back
# to anything, and that difference between the two fields is deliberate (#168 Option C).


def _deadline_score(value, horizon=None):
    """Return 0..1 for a real ISO `deadline`, or None when there is no usable field.

    None is the signal to fall back to the PROXY — it is NEVER silently read as 0.0,
    because a zero and an unmeasured thing are different claims
    [[measuring-tool-must-not-guess]]."""
    if not isinstance(value, str):
        return None
    import datetime as _dt
    try:
        due = _dt.date.fromisoformat(value)
    except ValueError:
        return None
    try:
        ref = _dt.date.fromisoformat((horizon or "").strip().split()[-1])
    except (ValueError, IndexError):
        ref = _dt.date.today()
    days = (due - ref).days
    if days <= 0:
        return 1.0              # due, or overdue
    return max(0.0, min(1.0, 1.0 - days / 30.0))


def _prose(i):
    return " ".join(str(i.get(k) or "") for k in ("title", "body", "closes_when"))


def score_item(i, session, inbound, links_corpus_empty):
    """Return (score 0–100, per-criterion sub-scores, list of MISSING INPUT names).

    Every branch that cannot measure records a missing input by NAME — it never
    silently substitutes zero and reports the total as if it were whole."""
    sub, missing = {}, []

    # --- unlock -------------------------------------------------------------
    n_links = len(i.get("links") or [])
    n_in = inbound.get(i["id"], 0)
    if links_corpus_empty:
        missing.append(("unlock", "no item in the store carries any links, so the "
                        "dependency graph cannot be read"))
        sub["unlock"] = 0.0
    else:
        sub["unlock"] = min(1.0, (n_links + 2 * n_in) / 6.0)

    # --- rot ----------------------------------------------------------------
    opened = i.get("opened")
    if not isinstance(opened, int) or opened <= 0:
        missing.append(("age", "opened is %r — the item's birth session is unknown, so "
                        "cost-of-delay cannot be measured" % opened))
        age_part = 0.0
    else:
        try:
            age_part = min(1.0, max(0, int(session) - opened) / 60.0)
        except (TypeError, ValueError):
            missing.append(("age", "the session number could not be read from _CHAIN.md"))
            age_part = 0.0
    sub["rot"] = min(1.0, age_part + (0.4 if i.get("condition") == "UNCONDITIONED" else 0.0))

    # --- effort: PRESENT ⇒ scored from the rung. ABSENT ⇒ DROPS OUT, never zeroed --------
    # #168 Option C (s168-D2 pending, Dave's). The length proxy DC2 removed does not return:
    # the only input is the gated rung. When there is no rung there is no `sub["effort"]` and
    # no row in this item's criteria — `active_criteria(False)` renormalizes without it, which
    # is the same list DC2 already used, so an item with no rung scores exactly as it does
    # today. An absent estimate is NOT an estimate of zero [[measuring-tool-must-not-guess]].
    #
    # ⛔ Note what is NOT here: no `missing.append(("effort", …))`. A dropped criterion is not
    # a missing INPUT — the score never claimed to include it, so flagging it would report a
    # hole in a total that has no such hole, and would light LOW CONFIDENCE on all 37 items
    # for a term none of them is being scored on.
    _eff = i.get(_state.EFFORT)
    has_effort = _eff in EFFORT_SCORE
    if has_effort:
        sub["effort"] = EFFORT_SCORE[_eff]
    elif _eff is not None:
        # Present but not a legal rung. `_state.check()` should have REFUSED this store, so
        # reaching here means the gate did not run — say so by NAME rather than falling into
        # the absent path, which would silently launder a malformed value into "no estimate".
        missing.append(("effort", "the item carries effort=%r, which is not one of %r — the "
                        "gate should have refused it; the criterion is DROPPED for this item "
                        "and the remaining weights renormalize" % (_eff, _state.EFFORT_VALUES)))

    # --- deadline -----------------------------------------------------------
    dl = i.get("deadline")
    dl_score = _deadline_score(dl, DEADLINE_SET)
    if dl_score is not None:
        sub["deadline"] = dl_score
    else:
        if dl is not None:
            missing.append(("deadline", "the item carries deadline=%r, which is not an ISO "
                            "date — the gate should have refused it; falling back to the "
                            "prose PROXY and saying so" % (dl,)))
        missing.append(("deadline", "the item has no `deadline` field — the score reads a "
                        "prose scan of the item's own words as a PROXY, so an item scores "
                        "higher by SAYING 'friday'"))
        sub["deadline"] = 1.0 if _DEADLINE_RE.search(_prose(i)) else 0.0

    # --- risk reduction -----------------------------------------------------
    sub["risk"] = min(1.0, len(set(m.group(0).lower() for m in
                                   _RISK_RE.finditer(_prose(i)))) / 3.0)

    # --- decision-load relief ----------------------------------------------
    if i.get("owner") == "claude":
        sub["load"] = 1.0 if _DECISION_RE.search(_prose(i)) else 0.4
    else:
        sub["load"] = 0.0

    # The weighted mean over THIS ITEM's active criteria. `CRITERIA` (the module-level,
    # effort-absent list) is what the page PRINTS; this is what the item is SCORED on, and
    # the two are the same list whenever the item has no rung — which is every item today.
    crit = active_criteria(has_effort)
    # ⛔ A criterion in the active set with no sub-score is a KeyError one line down, and a
    # traceback is not a refusal [[a-crash-is-not-a-fail]]. Name the criterion and the item,
    # because "KeyError: 'effort'" tells the next reader neither.
    _absent = [k for k, _n, _w, _d, _s in crit if k not in sub]
    if _absent:
        raise SystemExit("gen_dashboard REFUSING: item %r has criteria %r in its active set "
                         "with no sub-score computed. The active-criteria list and the scoring "
                         "branches above have forked — a weighted mean over a term that was "
                         "never measured is not a score." % (i.get("id"), _absent))
    total = sum(w * sub[k] for k, _n, w, _d, _s in crit)
    return int(round(total * 100)), sub, missing


def priorities(items, session):
    """Score every LIVE item (open/blocked). Done items are not ranked — a finished
    thing has no priority, and giving it one would put it in the queue."""
    links_corpus_empty = not any(i.get("links") for i in items)
    inbound = {}
    for i in items:
        for l in (i.get("links") or []):
            key = str(l).strip()
            inbound[key] = inbound.get(key, 0) + 1
    out = {}
    for i in items:
        if i.get("state") in ("done", "dropped"):
            continue
        s, sub, missing = score_item(i, session, inbound, links_corpus_empty)
        ov = i.get("priority_override")
        ov = ov if isinstance(ov, int) and not isinstance(ov, bool) else None
        out[i["id"]] = {"score": s, "sub": sub, "missing": missing, "override": ov}
    ranked = sorted(out.items(),
                    key=lambda kv: (0 if kv[1]["override"] is not None else 1,
                                    kv[1]["override"] if kv[1]["override"] is not None else 0,
                                    -kv[1]["score"], kv[0]))
    for n, (iid, rec) in enumerate(ranked, 1):
        rec["rank"] = n
    return {"by_id": out, "ranked": [iid for iid, _ in ranked],
            "links_corpus_empty": links_corpus_empty,
            "n_overrides": sum(1 for r in out.values() if r["override"] is not None)}


def links_coverage(items):
    """MEASURED, never repaired (Dave, #165: sparse links is a FLAGGED PROBLEM).

    The dashboard reports the coverage number and queues the backfill as Dave's work.
    Backfilling links would be an agent inventing the dependency graph it then scores
    itself against — a closed loop with no reader in it."""
    total = len(items)
    withl = sum(1 for i in items if i.get("links"))
    live = [i for i in items if i.get("state") not in ("done", "dropped")]
    return {"total": total, "with_links": withl,
            "pct": (100.0 * withl / total) if total else 0.0,
            "live_total": len(live),
            "live_with_links": sum(1 for i in live if i.get("links"))}


def sort_by_priority(group, prio):
    """Rank order: an OVERRULE always wins; then the proposed score; then id."""
    def key(i):
        r = prio["by_id"].get(i["id"])
        if not r:
            return (2, 0, 0, i["id"])
        if r["override"] is not None:
            return (0, r["override"], 0, i["id"])
        return (1, 0, -r["score"], i["id"])
    return sorted(group, key=key)


def project_counts(items):
    """The split, COUNTED from the store — never typed. `unknown` is reported separately
    rather than folded into either project: an item the gate somehow let through with no
    project must show up as a hole, not be quietly absorbed into a total."""
    c = {p: sum(1 for i in items if i.get("project") == p) for p in _state.PROJECT_VALUES}
    c["unknown"] = sum(1 for i in items if i.get("project") not in _state.PROJECT_VALUES)
    c["total"] = len(items)
    return c


def proj_attr(i):
    """The filter key as a data attribute. An item with no legal project gets `none`, which
    every filter shows — a row that cannot be classified must never be silently filtered
    away, because then the one item that needs looking at is the one you cannot see."""
    p = i.get("project")
    return ' data-project="%s"' % E(p if p in PROJECT_LABEL else "none")


def proj_tag(i):
    """The project label, as a WORD. Never a hue, never a dot, never a colour-coded border."""
    p = i.get("project")
    lab = PROJECT_LABEL.get(p)
    if lab is None:
        return ('<span class="proj proj-none">NO PROJECT</span>'
                '<span class="chk">the store has no legal project on this item</span>')
    out = '<span class="proj proj-%s">%s</span>' % (E(p), E(lab))
    if i.get("id") in PROJECT_CHECK:
        out += '<span class="chk">check</span>'
    return out


def counted(selector, n, cls="n"):
    """A number the filter must be able to RE-COUNT. It is generated correct for the
    unfiltered page; when a filter is on, the script re-counts the very elements this
    selector names, so a filtered heading can never keep quoting the unfiltered total."""
    return '<span class="%s" data-cnt="%s">%d</span>' % (cls, E(selector), n)


def short_title(t, n=64):
    """Trim for a card. The FULL title is on the two plates below — this is a glance
    surface, so a trim here loses nothing that the page does not also show in full."""
    t = re.sub(r"\s+", " ", str(t)).strip()
    if len(t) <= n:
        return t, False
    cut = t[:n].rsplit(" ", 1)[0]
    return (cut or t[:n]) + "…", True


def read_rulings():
    r = _json(os.path.join(HERE, "_rulings.json"))
    rs = r["rulings"]
    return {"n": len(rs), "tail": rs[-1], "rulings": rs}


def provenance_gaps(gate_result):
    """The provenance-gap set, taken VERBATIM from the live _governs run.

    ⛔ NOT authored here. Missing governs/evidence/status values are DAVE'S to supply;
    inventing one would be inventing provenance. We display the gate's own words."""
    if not gate_result:
        return {"fails": [], "ids": [], "measured": False}
    fails = [ln.strip() for ln in gate_result["lines"] if ln.strip().startswith("FAIL")]
    ids = []
    for ln in fails:
        m = re.search(r"ruling '?([a-zA-Z0-9\-]+)'?", ln)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return {"fails": fails, "ids": ids, "measured": True}


def read_session():
    chain = _read(os.path.join(ROOT, "_CHAIN.md"))
    m = re.search(r"YOU ARE #(\d+)", chain)
    session = m.group(1) if m else "unknown"
    t = re.search(r"TITLE THIS CHAT →\*\*\s*`([^`]+)`", chain)
    title = t.group(1) if t else ""
    ls = _read(os.path.join(ROOT, "_LIVE-STATE.md"))
    r = re.search(r"Last refreshed: (\d{4}-\d{2}-\d{2})", ls)
    refreshed = r.group(1) if r else "unknown"
    return {"session": session, "title": title, "refreshed": refreshed}


def read_ratchets():
    binds = _json(os.path.join(HERE, "_binds-ratchet.json"))
    typ = _json(os.path.join(HERE, "_type_ratchet.json"))
    return {"binds": binds, "type": typ}


def type_debt(gate_result, baseline):
    """Measured type-composite count vs the declared shrink-only baseline.

    The comparison is COMPUTED HERE (the owning gate is `--ratchet`, which writes and
    is therefore not run by a reporting surface). Label it as such on the page."""
    if not gate_result:
        return {"count": None, "baseline": baseline, "delta": None}
    m = None
    for ln in gate_result["lines"]:
        m = re.search(r"TYPE GATE FAIL — (\d+) violation", ln) or m
    count = int(m.group(1)) if m else None
    return {"count": count, "baseline": baseline,
            "delta": (count - baseline) if count is not None else None}


def read_future_state():
    txt = _read(os.path.join(ROOT, "_FUTURE-STATE.md"))
    blocks = re.split(r"^## ", txt, flags=re.M)[1:]
    out = []
    for b in blocks:
        head = b.splitlines()[0].strip()
        st = re.search(r"\*\*Status:\*\*\s*`([^`]+)`", b)
        born = re.search(r"\[born ([^\]·]+)", b)
        out.append({"title": head,
                    "status": st.group(1) if st else "unstated",
                    "born": born.group(1).strip() if born else ""})
    return out


def wave_claim(rulings):
    """The 114-row bind wave. This is a CLAIM QUOTED FROM THE STORE (s162-D1), not a
    measurement taken here — the page says so."""
    for r in rulings:
        blob = json.dumps(r)
        m = re.search(r"(?:CLOSED|closed)\s*114/114", blob)
        if m:
            return {"id": r["id"], "text": "114/114 — wave CLOSED", "ruled": r.get("ruled", "")}
    return None


# ---------------------------------------------------------------------------
# RENDER
# ---------------------------------------------------------------------------
CSS = """
:root{
  --dash-accent:#305A85;          /* DECORATIVE ONLY — carries no status meaning */
  --dash-red:#DA1A00;             /* s151-D1, on white */
  --dash-green:#137F3C;           /* s155-D1 mirror, on white */
  --dash-ink:#1A1A1A;
  --dash-mute:#545454;
  --dash-rule:#D7D8D6;
  --dash-band:#F3F3F3;
  --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
  --dash-font:"Univers Next for HSBC","Helvetica Neue",Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box;}
body{margin:0;background:#FFFFFF;color:var(--dash-ink);font-family:var(--dash-font);
  -webkit-font-smoothing:antialiased;}
.wrap{max-width:1200px;margin:0 auto;padding:0 var(--s4);}
section{padding:var(--s6) 0;border-top:1px solid var(--dash-rule);}
section:first-of-type{border-top:0;}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dash-accent);display:flex;align-items:center;gap:.5rem;margin:0 0 var(--s3);}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--dash-accent);}
h1{font-size:3.5625rem;line-height:1.04;font-weight:300;margin:0 0 var(--s3);letter-spacing:0;}
h2{font-size:2.125rem;line-height:1.15;font-weight:300;margin:0 0 var(--s3);}
h3{font-size:1.1875rem;line-height:1.2;font-weight:500;margin:0 0 var(--s2);}
p{line-height:1.75;margin:0 0 var(--s2);}
.lede p{font-size:21px;line-height:1.75;max-width:68ch;}
.lede p strong{font-weight:500;}
.meta{font-size:14px;color:var(--dash-mute);line-height:1.6;}
.sourceline{font-size:12px;color:var(--dash-mute);letter-spacing:.04em;margin-top:var(--s3);}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em;}

/* verdict words — the WORD is the signal; colour only repeats it */
.v{font-weight:500;letter-spacing:.06em;text-transform:uppercase;font-size:13px;
  white-space:nowrap;}
.v-pass{color:var(--dash-green);}
.v-fail{color:var(--dash-red);}
.v-debt{color:var(--dash-ink);}
.v-note{color:var(--dash-mute);}

table.strip{width:100%;border-collapse:collapse;}
table.strip th{text-align:left;font-size:12px;font-weight:500;letter-spacing:.12em;
  text-transform:uppercase;color:var(--dash-mute);padding:0 var(--s2) .6rem 0;
  border-bottom:1px solid var(--dash-rule);}
table.strip td{padding:.9rem var(--s2) .9rem 0;border-bottom:1px solid var(--dash-rule);
  vertical-align:top;font-size:15px;line-height:1.5;}
table.strip td.head{max-width:52ch;color:var(--dash-mute);}
table.strip td.gate{font-weight:500;}

.plates{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--dash-rule);}
.plate{padding:var(--s4) var(--s4) var(--s4) 0;}
.plate + .plate{border-left:1px solid var(--dash-rule);padding-left:var(--s4);}
.plate h3 .n{font-weight:300;font-size:2.125rem;display:block;line-height:1;margin-bottom:.4rem;}
ul.items{list-style:none;margin:0;padding:0;}
ul.items li{padding:var(--s2) 0;border-bottom:1px solid var(--dash-rule);}
ul.items li .id{font-size:12px;letter-spacing:.1em;color:var(--dash-mute);}
ul.items li .ti{font-size:16px;font-weight:500;line-height:1.4;display:block;margin:.2rem 0;}
ul.items li .cw{font-size:14px;color:var(--dash-mute);line-height:1.55;}

/* kanban — a GLANCE surface. Columns are DERIVED (state × condition); the derivation
   rule is printed in every column head, because a column nobody can trace is a claim. */
.kb{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:1px solid var(--dash-rule);}
.kb .col{padding:var(--s3) var(--s3) var(--s3) 0;min-width:0;}
.kb .col + .col{border-left:1px solid var(--dash-rule);padding-left:var(--s3);}
.kb .colhead{margin:0 0 var(--s3);}
.kb .colhead .n{display:block;font-size:2.125rem;font-weight:300;line-height:1;margin-bottom:.3rem;}
.kb .colhead .nm{display:block;font-size:15px;font-weight:500;line-height:1.25;letter-spacing:.02em;}
.kb .colhead .rule{display:block;font-size:12px;color:var(--dash-mute);line-height:1.5;margin-top:.35rem;}
.kb .cards{list-style:none;margin:0;padding:0;}
.kb .card{border:1px solid var(--dash-rule);padding:.65rem .7rem;margin:0 0 .5rem;background:#FFFFFF;}
.kb .card .cid{font-size:12px;letter-spacing:.1em;color:var(--dash-mute);display:block;}
.kb .card .ct{font-size:15px;font-weight:500;line-height:1.35;display:block;margin:.25rem 0 .35rem;
  overflow-wrap:anywhere;}
.kb .card .own{font-size:11px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid currentColor;padding:.1rem .35rem;display:inline-block;}
.kb .card .own-dave{color:var(--dash-ink);}
.kb .card .own-claude{color:var(--dash-mute);}
.kb .card .inf{font-size:11px;letter-spacing:.06em;color:var(--dash-mute);margin-left:.4rem;}
.kb .col-blocked .colhead .nm{color:var(--dash-red);}
.kb .col-done .colhead .nm{color:var(--dash-green);}
.kb .col-blocked .card{border-left:3px solid var(--dash-red);}
.kb .col-done .card{border-left:3px solid var(--dash-green);}
.kb .empty{font-size:14px;color:var(--dash-mute);}

/* project (s172-D1) — the label is a WORD. The hairline box is structure, matching the
   owner tag beside it; no status, priority or project meaning is carried by hue anywhere
   on this page. `check` is likewise a word, in ink, not a colour. */
.proj{font-size:11px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid currentColor;padding:.1rem .35rem;display:inline-block;
  color:var(--dash-ink);}
.proj-memento{color:var(--dash-mute);}
.proj-none{color:var(--dash-ink);}
.chk{font-size:11px;letter-spacing:.06em;color:var(--dash-mute);margin-left:.4rem;
  font-style:italic;}
.kb .card .proj{margin-right:.3rem;}
ul.items li .proj{margin-right:.4rem;}
table.pri td.projc .proj{white-space:nowrap;}

/* the filter bar. Buttons are WORDS with their generated counts; the state line says in a
   sentence what is being shown, so a filtered page never looks like the whole page. */
.pfilter{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;margin:0 0 var(--s3);
  padding:var(--s2) 0;border-top:1px solid var(--dash-rule);
  border-bottom:1px solid var(--dash-rule);}
.pfilter .pfl{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dash-mute);margin-right:.3rem;}
.pfilter button{font-family:inherit;font-size:13px;font-weight:500;letter-spacing:.08em;
  text-transform:uppercase;color:var(--dash-ink);background:#FFFFFF;cursor:pointer;
  border:1px solid var(--dash-rule);padding:.4rem .8rem;}
.pfilter button:hover{border-color:var(--dash-ink);}
.pfilter button:focus-visible{outline:2px solid var(--dash-accent);outline-offset:2px;}
.pfilter button[aria-pressed="true"]{background:var(--dash-ink);color:#FFFFFF;
  border-color:var(--dash-ink);}
.pfilter button b{font-weight:300;margin-left:.35rem;}
.pfilter .pfstate{font-size:13px;color:var(--dash-mute);margin-left:auto;}
/* THE FILTER ITSELF — one attribute on <body>, pure CSS from there. Items with
   data-project="none" are shown under EVERY filter, on purpose. */
body[data-project-filter="apollo"] [data-project="memento"],
body[data-project-filter="memento"] [data-project="apollo"]{display:none;}
@media (max-width:820px){ .pfilter .pfstate{margin-left:0;flex-basis:100%;} }
@media print{ .pfilter{display:none;} body[data-project-filter] [data-project]{display:revert;} }

/* priority — a PROPOSAL. The word PROPOSAL is on every surface that shows a score. */
.kb .card .pri{display:block;font-size:12px;letter-spacing:.06em;color:var(--dash-mute);
  margin:.35rem 0 .3rem;line-height:1.4;}
.kb .card .pri b{font-weight:500;color:var(--dash-ink);}
.kb .card .lowconf{font-weight:500;color:var(--dash-ink);}
.kb .card .ovr{font-weight:500;color:var(--dash-ink);letter-spacing:.08em;}
ul.items li .pri{font-size:13px;color:var(--dash-mute);display:block;margin-bottom:.15rem;}
ul.items li .pri b{font-weight:500;color:var(--dash-ink);}
table.pri{width:100%;border-collapse:collapse;}
table.pri th{text-align:left;font-size:12px;font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:var(--dash-mute);padding:0 .8rem .6rem 0;
  border-bottom:1px solid var(--dash-rule);vertical-align:bottom;}
table.pri th.num,table.pri td.num{text-align:right;padding-right:.8rem;}
table.pri td{padding:.75rem .8rem .75rem 0;border-bottom:1px solid var(--dash-rule);
  font-size:15px;line-height:1.5;vertical-align:top;}
table.pri td.rk{font-size:1.1875rem;font-weight:300;}
table.pri td.ti{max-width:46ch;}
table.pri td.ti .id{font-size:12px;letter-spacing:.1em;color:var(--dash-mute);
  display:block;margin-bottom:.15rem;}
table.pri td.flag{font-size:12px;color:var(--dash-mute);max-width:38ch;line-height:1.5;}
table.pri td.sc{font-weight:500;white-space:nowrap;}
table.pri tr.has-ovr td{background:var(--dash-band);}
/* narrow: the six per-criterion sub-scores drop out. The SCORE and the LOW-CONFIDENCE
   flag never drop — a number without its confidence is the thing we refuse to print.
   The weights table above still declares every criterion at every width. */
@media (max-width:900px){
  table.pri th.subcol,table.pri td.subcol,
  table.pri th.ownc,table.pri td.ownc{display:none;}
  table.pri{table-layout:fixed;}
  table.pri td.ti{max-width:none;}
  table.pri td,table.pri th{padding-right:.5rem;}
  table.pri th.num:first-child,table.pri td.rk{width:2.2rem;}
  table.pri td.flag{max-width:none;}
}
.wtable{width:100%;border-collapse:collapse;margin-bottom:var(--s3);}
.wtable th{text-align:left;font-size:12px;font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:var(--dash-mute);padding:0 .8rem .6rem 0;
  border-bottom:1px solid var(--dash-rule);}
.wtable td{padding:.7rem .8rem;border-bottom:1px solid var(--dash-rule);font-size:15px;
  line-height:1.55;vertical-align:top;padding-left:0;}
.wtable td.w{font-size:1.1875rem;font-weight:300;white-space:nowrap;}
.wtable td.src{color:var(--dash-mute);font-size:13px;max-width:44ch;}

.band{background:var(--dash-band);}
.band .wrap{padding-top:var(--s6);padding-bottom:var(--s6);}
ol.fails{margin:0;padding-left:1.4rem;}
ol.fails li{font-size:15px;line-height:1.6;padding:.45rem 0;max-width:100ch;}

.future{display:grid;grid-template-columns:1fr;gap:0;}
.future .row{display:grid;grid-template-columns:9rem 1fr;gap:var(--s3);
  padding:var(--s2) 0;border-bottom:1px solid var(--dash-rule);align-items:baseline;}
.future .row .st{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--dash-mute);}
.future .row .ti{font-size:16px;line-height:1.5;max-width:80ch;}

@media (max-width:1000px){
  .kb{grid-template-columns:1fr 1fr;}
  .kb .col{border-left:0;padding-left:0;padding-right:var(--s3);}
  .kb .col:nth-child(2n){border-left:1px solid var(--dash-rule);padding-left:var(--s3);}
  .kb .col:nth-child(n+3){border-top:1px solid var(--dash-rule);}
}
@media (max-width:820px){
  h1{font-size:2.6875rem;}
  .kb{grid-template-columns:1fr;}
  .kb .col,.kb .col:nth-child(2n){border-left:0;padding-left:0;}
  .kb .col + .col{border-top:1px solid var(--dash-rule);}
  .plates{grid-template-columns:1fr;}
  .plate + .plate{border-left:0;border-top:1px solid var(--dash-rule);padding-left:0;}
  .future .row{grid-template-columns:1fr;gap:.2rem;}
}
@media print{ body{color:#000;} }
"""


# The project filter, s172-D1. The ONLY script on this page, and deliberately small.
#
# ⚠ IT IS A VIEW, NOT A STATE. It flips one attribute on <body>; the hiding itself is CSS.
# Nothing is written to a store, nothing is remembered across a reload, and no number is
# computed by hand — every count it prints is a COUNT OF THE DOM under the same predicate
# the CSS hides by, so a heading cannot keep quoting an unfiltered total while showing a
# filtered list [[measure-dont-convert-units]].
#
# ⚠ AND IT DEGRADES: with scripting off, `data-project-filter` is never set, the CSS rules
# are inert, and every item is shown with its project printed as a word beside it.
PROJECT_JS = """<script>
(function(){
  var body=document.body,
      btns=Array.prototype.slice.call(document.querySelectorAll('.pfilter button')),
      st=document.getElementById('pfstate'),
      cnt=Array.prototype.slice.call(document.querySelectorAll('[data-cnt]')),
      NAME={all:'all',apollo:'APOLLO',memento:'MEMENTO'};
  if(!btns.length){return;}
  function shown(el,f){
    if(f==='all'){return true;}
    var p=el.getAttribute('data-project');
    return p===f||p==='none';           /* an unclassifiable item is never hidden */
  }
  function apply(f){
    body.setAttribute('data-project-filter',f);
    btns.forEach(function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-pf')===f));});
    var total=0;
    cnt.forEach(function(el){
      var n=0;
      Array.prototype.forEach.call(document.querySelectorAll(el.getAttribute('data-cnt')),
        function(x){ if(shown(x,f)){n++;} });
      el.textContent=n;
      if(el.className.indexOf('kbtotal')>-1){total=n;}
    });
    if(st){
      st.textContent = (f==='all')
        ? ('Showing all '+total+' items.')
        : ('Showing '+NAME[f]+' only \\u2014 '+total+' items. The rest are hidden, not gone.');
    }
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(){apply(b.getAttribute('data-pf'));});
  });
  apply('all');
})();
</script>"""


def verdict(rc, name):
    if name == "type-composites":
        return ("DEBT", "v-debt")
    if rc == 0:
        return ("PASS", "v-pass")
    if rc in (124, 125):
        return ("NO VERDICT", "v-note")
    return ("FAIL", "v-fail")


def pri_badge(iid, prio):
    """The card/plate badge. PROPOSAL unless Dave has overruled — and an overrule says so
    in his words, not in a colour."""
    r = prio["by_id"].get(iid)
    if not r:
        return ""
    if r["override"] is not None:
        return ('<span class="pri"><span class="ovr">DAVE OVERRULED &rarr; %d</span></span>'
                % r["override"])
    flag = (' &middot; <span class="lowconf">LOW CONFIDENCE</span>, %d input(s) missing'
            % len(r["missing"])) if r["missing"] else ""
    return ('<span class="pri">PROPOSAL &middot; rank <b>%d</b> &middot; score <b>%d</b>/100%s</span>'
            % (r["rank"], r["score"], flag))


def render(state, rulings, gaps, session, ratchets, tdebt, future, gates, wave, kanban,
           prio, cov):
    o = []
    a = o.append
    dave = sort_by_priority([i for i in state["open"] if i.get("owner") == "dave"], prio)
    mine = sort_by_priority([i for i in state["open"] if i.get("owner") == "claude"], prio)
    unconditioned = [i for i in state["open"] if i.get("condition") == "UNCONDITIONED"]
    pc = project_counts(state["items"])
    check_ids = [i for i in state["items"] if i["id"] in PROJECT_CHECK]
    n_fail = sum(1 for g in gates if g["rc"] != 0 and g["name"] != "type-composites")
    n_pass = sum(1 for g in gates if g["rc"] == 0)

    a("<!DOCTYPE html>")
    a('<html lang="en" data-apollo-theme="mono">')
    a("<head>")
    a('<meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1">')
    a("<title>Mission control — Apollo progress dashboard</title>")
    a("<!--")
    a("  GENERATED by knowledge/gen_dashboard.py FROM THE STORES. DO NOT HAND-EDIT.")
    a("  If a number here is wrong, the STORE is wrong: fix the store, regenerate.")
    a("  `python3 knowledge/gen_dashboard.py --check` is the build gate.")
    a("-->")
    a('<link rel="stylesheet" href="../knowledge/canon/type.css">')
    a('<link rel="stylesheet" href="../knowledge/canon/canon.css">')
    a("<style>%s</style>" % CSS)
    a("</head>")
    a('<body data-theme="light">')

    # ---- masthead + exec summary -----------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">Apollo · mission control · session #%s</p>' % E(session["session"]))
    a("<h1>Where the work stands</h1>")
    a('<div class="lede">')
    a("<p><strong>%d things are open.</strong> %d of them are yours to rule, %d are mine to build. "
      "%d of the open items still have no checkable close condition — they are the frozen legacy set, "
      "and that set may only shrink." % (len(state["open"]), len(dave), len(mine), len(unconditioned)))
    if gates:
        a("<p>%d of %d gates were run just now and passed; %s. "
          "The type-composite gate is not counted as a pass or a fail — it reports declared debt, "
          "which is a third thing." % (n_pass, len(gates),
                                       ("%d failed" % n_fail) if n_fail else "none failed"))
    if gaps["measured"]:
        a("<p>The provenance gate is the one that is red, and it is red on purpose: %d checks fail "
          "across %d rulings that are missing a <code>governs</code>, <code>evidence</code> or "
          "<code>status</code> value. <strong>Those values are yours and nobody else&rsquo;s</strong> — "
          "authoring them would be inventing provenance, so this page lists them and stops."
          % (len(gaps["fails"]), len(gaps["ids"])))
    if tdebt["delta"] is not None and tdebt["delta"] > 0:
        a("<p><span class=\"v v-fail\">Ratchet breach</span> — the type-composite count measures "
          "<strong>%d</strong> against a declared, shrink-only baseline of <strong>%d</strong>. "
          "That is %d more than the ratchet permits. Measured here; not fixed here."
          % (tdebt["count"], tdebt["baseline"], tdebt["delta"]))
    a("<p>The order everything is shown in is a <strong>PROPOSAL</strong> — a score I compute "
      "from the store at build time, out of %d weighted criteria printed in full below. "
      "It is not a ruling and it does not persist: you overrule it by writing a "
      "<code>priority_override</code> rank on the item, and an overruled item says "
      "<strong>DAVE OVERRULED</strong> wherever it appears. %s"
      % (len(CRITERIA),
         "<strong>No item carries an override yet</strong> — the field is absent everywhere, "
         "because a priority I write into the store and then read back is not your judgement, "
         "it is mine wearing your name.</p>" if not prio["n_overrides"] else
         "%d item(s) currently carry your override.</p>" % prio["n_overrides"]))
    # ⚠ the %s above is now the SECOND slot — %d len(CRITERIA) is the first.
    a("<p><span class=\"v v-fail\">Flagged problem</span> — <strong>%d of %d items carry any "
      "<code>links</code></strong> (%.0f%%). The dependency graph the score's heaviest "
      "criterion (Unlock, weight %.3f) needs <em>does not exist in the data</em>, so every "
      "score on this page is flagged LOW CONFIDENCE and the unlock column reads zero for "
      "everything. This is MEASURED and QUEUED, not repaired: backfilling links would mean "
      "inventing the dependency graph and then scoring against my own invention. It is "
      "yours, and it is %s work.</p>"
      % (cov["with_links"], cov["total"], cov["pct"], CRITERIA[0][2], DEADLINE_SET))
    a("<p>Everything on this page was read out of the stores or measured by running the thing. "
      "Nothing is asserted from memory.</p>")
    a("</div>")
    a('<p class="sourceline">SOURCES · knowledge/_state.json · knowledge/_rulings.json · '
      'live gate runs · _CHAIN.md · _LIVE-STATE.md (last refreshed %s) · _FUTURE-STATE.md</p>'
      % E(session["refreshed"]))
    a("</div></section>")

    # ---- project: the label + the filter (s172-D1) -------------------------
    a('<section><div class="wrap">')
    a('<p class="label">Project &mdash; which body of work each item belongs to</p>')
    a("<h2>%d Apollo, %d Memento</h2>" % (pc["apollo"], pc["memento"]))
    a("<p class=\"meta\"><strong>These are my proposed defaults, not your ruling.</strong> "
      "You ruled that every item carries a stored <code>project</code> and that new items "
      "cannot be added without one; the <em>values</em> below are the assignment I proposed, "
      "written into <code>_state.json</code> for your eye. Change any of them by editing the "
      "item&rsquo;s <code>project</code> in the store and regenerating &mdash; this page "
      "reports the store, it does not decide.</p>")
    if check_ids:
        a("<p class=\"meta\"><strong>%d of them I could not call, and they say so.</strong> "
          "Anywhere those items appear, the word <em>check</em> sits next to the project "
          "label: %s. They are not marked by colour, and they are not marked as wrong &mdash; "
          "they are marked as MINE TO GUESS AND YOURS TO SETTLE.</p>"
          % (len(check_ids),
             "; ".join("<strong>%s</strong> (I put it in %s) &mdash; %s"
                       % (E(i["id"]), E(PROJECT_LABEL.get(i.get("project"), "NO PROJECT")),
                          E(short_title(i["title"], 70)[0]))
                       for i in check_ids)))
    if pc["unknown"]:
        a("<p><span class=\"v v-fail\">Flagged problem</span> &mdash; <strong>%d item(s) carry "
          "no legal project</strong>. The store gate should make this impossible, so if you are "
          "reading this sentence the gate did not run. Those items show <strong>NO PROJECT</strong> "
          "as a word and are shown under every filter, never hidden.</p>" % pc["unknown"])
    a('<div class="pfilter" role="group" aria-label="Filter every panel by project">')
    a('<span class="pfl">Show</span>')
    a('<button type="button" data-pf="all" aria-pressed="true">All <b>%d</b></button>' % pc["total"])
    for p in _state.PROJECT_VALUES:
        a('<button type="button" data-pf="%s" aria-pressed="false">%s <b>%d</b></button>'
          % (E(p), E(PROJECT_LABEL[p].title()), pc[p]))
    a('<span class="pfstate" id="pfstate">Showing all %d items.</span>' % pc["total"])
    a("</div>")
    a("<noscript><p class=\"meta\">Scripting is off, so the buttons above do nothing and every "
      "item on this page is shown. Nothing is lost: every card, plate entry and priority row "
      "prints its project as a word regardless of the filter.</p></noscript>")
    a("<p class=\"meta\">The filter is a VIEW, not a state. It touches the board, the two "
      "plates and the priority table; it does not touch the stores, and it is not remembered "
      "&mdash; reload and you are back to all %d. Counts in the headings below <strong>re-count "
      "themselves</strong> when you filter, so a filtered heading never quotes an unfiltered "
      "total. Priority <strong>ranks do not renumber</strong>: rank 3 means third out of the "
      "whole backlog, and it keeps saying 3 in a filtered view, because a rank that changes "
      "with the view is not a rank.</p>" % pc["total"])
    a('<p class="sourceline">SOURCE &middot; knowledge/_state.json, field <code>project</code>, '
      'counted at generation. Legal values are the closed enum in <code>knowledge/_state.py</code> '
      '(<code>%s</code>), REQUIRED on every item and refused loudly when absent or misspelt. '
      'No project value is authored by this page.</p>'
      % E(" | ".join(_state.PROJECT_VALUES)))
    a("</div></section>")

    # ---- gates health strip ----------------------------------------------
    if gates:
        a('<section><div class="wrap">')
        a('<p class="label">Gates health — measured at generation, never asserted</p>')
        a("<h2>Eight gates, run just now</h2>")
        a('<table class="strip"><thead><tr>'
          "<th>Gate</th><th>Verdict</th><th>rc</th><th>What it proves</th><th>Its own last line</th>"
          "</tr></thead><tbody>")
        for g in gates:
            word, cls = verdict(g["rc"], g["name"])
            a("<tr><td class=\"gate\">%s</td><td><span class=\"v %s\">%s</span></td>"
              "<td>%d</td><td class=\"head\">%s</td><td class=\"head\">%s</td></tr>"
              % (E(g["name"]), cls, word, g["rc"], E(g["why"]), E(g["headline"][:180])))
        a("</tbody></table>")
        a('<p class="sourceline">Each row is a real subprocess run from this generator '
          '(read-only invocations only). <code>--ratchet</code> is deliberately NOT run: it writes '
          'a store, and a reporting surface must not repair what it reports.</p>')
        a("</div></section>")

    # ---- progress toward atomic ------------------------------------------
    a('<section class="band"><div class="wrap">')
    a('<p class="label">Progress toward atomic</p>')
    a("<h2>The counts that move</h2>")
    a('<div class="cn-stat-card"><div class="board" style="max-width:none">')

    def card(label, value, note):
        a('<div class="stat-card" role="group" aria-label="%s">' % E(label))
        a('<p class="lbl16 t-cm-caption">%s</p>' % E(label))
        a('<span class="amt t-cm-figure-3"><span>%s</span></span>' % E(value))
        a('<span class="delta"><span class="t-cm-figure-6">%s</span></span>' % E(note))
        a("</div>")

    card("Rulings recorded", rulings["n"], "tail %s" % rulings["tail"]["id"])
    card("Rulings with a provenance gap", len(gaps["ids"]) if gaps["measured"] else "—",
         "Dave's to supply")
    card("Open items", len(state["open"]), "%d yours · %d mine" % (len(dave), len(mine)))
    card("Open with no close condition", len(unconditioned), "frozen legacy set, shrink-only")
    card("Items carrying links", "%d/%d" % (cov["with_links"], cov["total"]),
         "%.0f%% — the dependency graph, MEASURED" % cov["pct"])
    card("Items with your override", prio["n_overrides"],
         "yours to set; none authored here")
    card("Metas carrying binds", "%d/%d" % (ratchets["binds"]["floor"], ratchets["binds"]["corpus"]),
         "floor may only rise")
    if tdebt["count"] is not None:
        card("Type-composite debt", tdebt["count"],
             "baseline %d · delta %+d" % (tdebt["baseline"], tdebt["delta"]))
    if wave:
        card("The s142-D1 bind wave", "114/114", "claimed by %s, not measured here" % wave["id"])
    a("</div></div>")
    a('<p class="sourceline">Mono <code>.cn-stat-card</code> from knowledge/canon/canon.css — the '
      'gated component, unmodified. SOURCES · _rulings.json · _state.json · _binds-ratchet.json · '
      '_type_ratchet.json · the live _governs run.</p>')
    a("</div></section>")

    # ---- priority PROPOSAL ------------------------------------------------
    live_items = [i for i in state["items"] if i["id"] in prio["by_id"]]
    a('<section><div class="wrap">')
    a('<p class="label">Priority &mdash; a PROPOSAL, not a ruling</p>')
    a("<h2>My proposed order, and the weights it came from</h2>")
    a("<p class=\"meta\">You ruled that I generate the priorities and you overrule them. This is "
      "the generated half. It is <strong>computed at build time from the store</strong>, never "
      "written back into it, so it cannot rot and it cannot quietly become a decision. %d "
      "criteria, each scored 0&ndash;1, combined with the declared weights below into a score "
      "out of 100. <strong>The weights themselves are a proposal too</strong> &mdash; change any "
      "number in the table and the order changes; nothing about them is ratified.</p>"
      % len(CRITERIA))
    a("<p class=\"meta\"><strong>There used to be a sixth criterion, and you removed it.</strong> "
      "&ldquo;Effort (inverse)&rdquo; carried 0.15 of the weight and, with no real "
      "<code>effort</code> values in the store, its only input was the BYTE LENGTH of an "
      "item&rsquo;s body text &mdash; a proxy for how much had been written about a job, not "
      "for how big the job is. Dropped on your #168 review (DC2). The remaining weights are "
      "your original ratios &mdash; 30&#8239;:&#8239;20&#8239;:&#8239;15&#8239;:&#8239;10&#8239;:"
      "&#8239;10 &mdash; divided by their own sum, so every criterion stands in exactly the "
      "relationship to every other that it did before; only the removed 0.15 left the "
      "denominator. <strong>It has since come back as a CONDITIONAL criterion</strong> "
      "&mdash; the block under the table &mdash; but the byte-length proxy has not, and will "
      "not: the criterion now has one input, and no input means no criterion.</p>")
    a('<table class="wtable"><thead><tr><th>Criterion</th><th>Weight</th>'
      "<th>What it measures</th><th>Where the input comes from</th></tr></thead><tbody>")
    # 3dp, not 2 — the renormalized weights are thirds-of-0.85 and at 2dp they would print
    # a column that visibly does not add to the TOTAL underneath it.
    for key, name, w, desc, src in CRITERIA:
        a("<tr><td><strong>%s</strong></td><td class=\"w\">%.3f</td><td>%s</td>"
          "<td class=\"src\">%s</td></tr>" % (E(name), w, E(desc), src))
    a("<tr><td><strong>TOTAL</strong></td><td class=\"w\">%.3f</td><td colspan=\"2\" "
      "class=\"src\">Score = 100 &times; &Sigma;(weight &times; criterion). Deadline set: "
      "<strong>%s</strong>.</td></tr>" % (WEIGHTS_SUM, E(DEADLINE_SET)))
    a("</tbody></table>")

    # ---- THE EFFORT RUNGS — the standard, printed so it travels with the number ----------
    # Option C of notes/_PROPOSAL-effort-gauge-2026-08-13-v1.md. s168-D2 is PENDING: minted
    # at the #168 wrap by you, not by the lane that built this. The edges below are DERIVED
    # from the gauge log at every build and printed with the n they came from, so drift is
    # visible rather than silent [[planning-estimate-is-not-a-measurement]].
    _an = effort_anchors()
    _eff_w = dict((k, w) for k, _n2, w, _d2, _s2 in active_criteria(True))
    a("<div>")   # plain wrapper — no invented class name; the page's CSS is gated canon
    a("<p class=\"meta\"><strong>Effort is back &mdash; as a rung measured in TOKENS, and only "
      "where you have written one.</strong> The unit is <strong>real Claude tokens of job "
      "window</strong> (boot and wrap excluded) &mdash; the unit this project already rules and "
      "logs, not t-shirt sizes and not bytes of prose. <strong>Delegated sub spend is excluded "
      "too:</strong> a sub&rsquo;s tokens are weekly quota, not this window&rsquo;s fill, and "
      "they are not in the logged blocks these edges come from &mdash; so an <strong>L</strong> "
      "that needs a sub is a claim about this window, never a total bill. The three rungs mean "
      "this:</p>")
    a('<table class="wtable"><thead><tr><th>Rung</th><th>What it means</th>'
      "<th>Job tokens, estimated</th><th>Scores</th></tr></thead><tbody>")
    _bands = {"S": "&le;&#8239;%s" % f"{_an['s_edge']:,}",
              "M": "%s &ndash; %s" % (f"{_an['s_edge']:,}", f"{_an['l_edge']:,}"),
              "L": "&gt;&#8239;%s" % f"{_an['l_edge']:,}"}
    for _r in _state.EFFORT_VALUES:
        a("<tr><td><strong>%s</strong></td><td>%s</td><td class=\"w\">%s</td>"
          "<td class=\"w\">%.2f</td></tr>"
          % (E(_r), E(_state.EFFORT_RUNG_MEANING[_r]), _bands[_r], EFFORT_SCORE[_r]))
    a("</tbody></table>")
    a("<p class=\"sourceline\">EDGES DERIVED, NOT TYPED &mdash; lower and upper quartile of the "
      "<strong>%d</strong> token-priced session blocks in <code>%s</code> (range %s&ndash;%s "
      "job tokens, median %s), rounded hard to the nearest 5,000 because %d self-selected "
      "blocks cannot support a sharper edge. They move as the log grows; that is why they are "
      "printed rather than stored.</p>"
      % (_an["n"], E(_an["source"]), f"{_an['min']:,}", f"{_an['max']:,}",
         f"{_an['median']:,}", _an["n"]))
    a("<p class=\"meta\"><strong>A rung is your ESTIMATE against a measured standard &mdash; it "
      "is not a measurement of the job, and the page will never print it as one.</strong> "
      "Writing <code>\"effort\": \"M\"</code> on an item is a forecast; the edges it is judged "
      "against are the measured history. Two more things worth knowing before you author any: "
      "<strong>(1) absent is legal and costs nothing</strong> &mdash; an item with no rung has "
      "no effort criterion at all, and its remaining weights renormalize, so it is scored on "
      "what it has rather than penalised for what it lacks; "
      "<strong>(2) a rung changes the whole row&rsquo;s weighting</strong> &mdash; with a rung "
      "present, effort takes %.2f and your other five snap back to their absolutes "
      "(%s). So a partly-authored store ranks two populations under two weightings; that is "
      "honest per item, but it is not a clean comparison across items. "
      "<strong>Today: %d of %d items carry a rung, so nothing below has moved.</strong> "
      "&#9940; No agent may author a value &mdash; every rung on this page will be yours. "
      "<em>s168-D2 PENDING</em>: the machinery is built and proven, the ruling is minted at "
      "the wrap.</p>"
      % (_eff_w["effort"],
         E(" / ".join("%s %.2f" % (n, _eff_w[k]) for k, n, _w, _d3, _s3 in _CRITERIA_RAW)),
         sum(1 for i in state["items"] if i.get("effort") in EFFORT_SCORE),
         len(state["items"])))
    a("</div>")
    # ⚠ MEASURED, NOT TYPED. This paragraph used to assert "there is no effort field, no
    # deadline field" — true when written, and it would have gone quietly false the moment
    # the fields landed [[premise-ages-faster-than-rule]]. It now counts them.
    _all = state["items"]
    _n_eff = sum(1 for i in _all if i.get("effort") in EFFORT_SCORE)
    _n_dl = sum(1 for i in _all if _deadline_score(i.get("deadline"), DEADLINE_SET) is not None)
    a("<p class=\"meta\"><strong>Some inputs are proxies, and the table says which.</strong> "
      "<code>opened</code>, <code>condition</code> and <code>owner</code> are real fields. "
      "<code>deadline</code> is an OPTIONAL real field that <em>replaces</em> its proxy when "
      "present &mdash; today it is present on <strong>%d</strong> of %d items, so the proxy is "
      "what runs everywhere else. <code>effort</code> is also an optional gated field, present "
      "on <strong>%d</strong> items, and it is <strong>read where present and nowhere else</strong>: "
      "unlike <code>deadline</code> it has NO proxy to fall back on, so an item without one is "
      "scored on the other criteria, renormalized, rather than guessed at. "
      "<code>links</code> is empty on %d of %d items. Where an input was missing, the score "
      "carries a LOW-CONFIDENCE flag naming it. A clean-looking number from thin data is the one "
      "thing this page must never print.</p>" % (_n_dl, cov["total"], _n_eff,
                                                 cov["total"] - cov["with_links"],
                                                 cov["total"]))
    _sc = sorted(r["score"] for r in prio["by_id"].values())
    if _sc:
        a("<p class=\"meta\"><strong>How much this ranking actually separates the work: not much, "
          "and here is the number.</strong> The %d scored items span <strong>%d to %d</strong> "
          "out of 100 across <strong>%d distinct values</strong>, so the gap between rank 1 and "
          "rank %d is %d points. That is what a ranking looks like when its heaviest criterion "
          "has no data: the order below is a tie-break, not a verdict. It gets sharper the "
          "moment <code>links</code> exists.</p>"
          % (len(_sc), _sc[0], _sc[-1], len(set(_sc)), len(_sc), _sc[-1] - _sc[0]))
    seen_why, legend = set(), []
    for r in prio["by_id"].values():
        for short, why in r["missing"]:
            if short not in seen_why:
                seen_why.add(short)
                legend.append((short, why))
    if legend:
        a("<p class=\"meta\"><strong>What the missing-input words in the last column mean.</strong> "
          + " ".join("<strong>%s</strong> — %s." % (E(s), E(w)) for s, w in legend) + "</p>")
    a('<table class="pri"><thead><tr><th class="num">#</th><th>Item</th>'
      '<th class="projc">Project</th><th class="ownc">Owner</th>'
      '<th class="num">Score</th>')
    for _k, name, w, _d, _s in CRITERIA:
        a('<th class="num subcol">%s<br>%.2f</th>' % (E(name), w))
    a("<th>Confidence</th></tr></thead><tbody>")
    for iid in prio["ranked"]:
        it = next(i for i in live_items if i["id"] == iid)
        r = prio["by_id"][iid]
        t, _ = short_title(it["title"], 72)
        a('<tr class="%s"%s>' % ("has-ovr" if r["override"] is not None else "", proj_attr(it)))
        a('<td class="num rk">%d</td>' % r["rank"])
        a('<td class="ti"><span class="id">%s</span> %s</td>' % (E(iid), E(t)))
        a('<td class="projc">%s</td>' % proj_tag(it))
        a('<td class="ownc">%s</td>' % ("DAVE" if it.get("owner") == "dave" else "CLAUDE"))
        if r["override"] is not None:
            a('<td class="num sc">DAVE OVERRULED &rarr; %d</td>' % r["override"])
        else:
            a('<td class="num sc">%d <span class="v v-note">PROPOSAL</span></td>' % r["score"])
        for k, _n, _w, _d, _s in CRITERIA:
            a('<td class="num subcol">%.2f</td>' % r["sub"][k])
        a('<td class="flag">%s</td>' % (
            ("<strong>LOW CONFIDENCE</strong><br>missing: "
             + E(" · ".join(m[0] for m in r["missing"])))
            if r["missing"] else "all inputs present"))
        a("</tr>")
    a("</tbody></table>")
    a('<p class="sourceline">SOURCE · knowledge/_state.json, every item where state is not done '
      'or dropped, scored by <code>gen_dashboard.py::score_item()</code> at generation. '
      'The override channel is the OPTIONAL <code>priority_override</code> integer (1 = first, '
      'range 1–999), validated when present by <code>knowledge/_state.py</code> and wired into '
      '_build_all.py as a routed step. ⛔ No override value has been authored by me, here or in '
      'the store.</p>')
    a("</div></section>")

    # ---- links coverage — REPORTED, queued, never repaired ----------------
    a('<section class="band"><div class="wrap">')
    a('<p class="label">Flagged problem &mdash; the dependency graph does not exist</p>')
    a("<h2>%d of %d items carry links &mdash; %.0f%%</h2>"
      % (cov["with_links"], cov["total"], cov["pct"]))
    a("<p>Among the %d live items it is <strong>%d</strong>. <code>links</code> is a required "
      "field, so it is present on every item &mdash; and empty on almost all of them. The "
      "consequence is concrete and it is on this page: the heaviest criterion in the score "
      "above (Unlock, weight %.3f) has nothing to read, contributes zero to every item, and "
      "the remaining %.3f of weight is doing all the work of ranking your backlog.</p>"
      % (cov["live_total"], cov["live_with_links"], CRITERIA[0][2], 1 - CRITERIA[0][2]))
    a("<p><strong>Queued as your work for the %s set, not repaired here.</strong> I could "
      "populate <code>links</code> by guessing which item blocks which from the prose &mdash; "
      "and then the score would rank your backlog against a dependency graph I invented and "
      "you never saw. That is a closed loop with no reader in it. The number is reported; the "
      "backfill waits for you.</p>" % E(DEADLINE_SET))
    a('<p class="sourceline">SOURCE · knowledge/_state.json, counted at generation. This panel '
      'moves on its own the moment links are written — it is a measurement, not a note.</p>')
    a("</div></section>")

    # ---- kanban (quick visual reference) ---------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">Board — quick visual reference</p>')
    a("<h2>%s items, four columns</h2>"
      % counted(".kb li.card", len(state["items"]), cls="kbtotal"))
    a('<p class="meta"><strong>The columns are DERIVED, not stored.</strong> '
      '<code>_state.json</code> has no <code>status</code>, <code>lane</code>, '
      '<code>phase</code> or <code>priority</code> field — the only lifecycle axes that '
      'exist in the data are <code>state</code> (open / blocked / done) and '
      '<code>condition</code> (UNCONDITIONED / stated, i.e. whether a '
      '<code>closes_when</code> is set). <code>project</code> IS stored (you ruled it at '
      '#172) — it is a grouping label, not a lifecycle, so it makes a filter and not a '
      'column. Each column head prints the exact rule that put '
      'items in it, so you can check the derivation rather than trust it. Owner is the '
      'store&rsquo;s <code>owner</code>, written as a WORD; where the store marks it '
      'inferred the card says <em>inferred</em>. <strong>Cards are ordered by the proposed '
      'priority score</strong> (an overruled card sits at the top of its column); the Done '
      'column stays in id order, because a finished thing has no priority.</p>')
    a('<div class="kb">')
    for c in kanban:
        a('<div class="col col-%s">' % E(c["key"]))
        a('<div class="colhead">%s<span class="nm">%s</span>'
          '<span class="rule">%s<br>%s</span></div>'
          % (counted(".kb .col-%s li.card" % c["key"], len(c["items"])),
             E(c["name"]), E(c["rule"]), E(c["note"])))
        if not c["items"]:
            a('<p class="empty">None.</p>')
        else:
            a('<ul class="cards">')
            for i in c["items"]:
                t, trimmed = short_title(i["title"])
                own = "DAVE" if i.get("owner") == "dave" else "CLAUDE"
                ocls = "own-dave" if i.get("owner") == "dave" else "own-claude"
                inf = '<span class="inf">inferred</span>' if i.get("owner_inferred") else ""
                a('<li class="card"%s><span class="cid">%s</span>'
                  '<span class="ct" title="%s">%s</span>%s'
                  '<span class="own %s">%s</span>%s<br>%s</li>'
                  % (proj_attr(i), E(i["id"]), E(i["title"]), E(t),
                     pri_badge(i["id"], prio), ocls, own, inf, proj_tag(i)))
            a("</ul>")
        a("</div>")
    a("</div>")
    a('<p class="sourceline">SOURCE · knowledge/_state.json, every item, no filter. Titles are '
      'trimmed for the glance only — the full title of every OPEN item is on the two plates '
      'below. The board REPORTS the store; it does not re-classify, re-prioritise or move '
      'anything. Red on the blocked column and green on the done column (s151-D1 / s155-D1, '
      'light mode) repeat the column&rsquo;s own word; no meaning is carried by hue.</p>')
    a("</div></section>")

    # ---- the two plates ---------------------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">The two plates</p>')
    a("<h2>What is on your plate, and what is on mine</h2>")
    a('<p class="meta">Owner comes from <code>_state.json</code>. Where the store marks the owner '
      'as inferred, the item says so — an inference is not a ruling. <strong>Both plates are in '
      'proposed-priority order</strong>, highest score first, with any item you have overruled '
      'lifted to the top of its plate; the badge on each item says which of the two it is.</p>')
    a('<div class="plates">')
    for title, group, who, pkey in (("Dave&rsquo;s plate", dave, "DAVE'S", "dave"),
                                    ("My plate", mine, "MINE", "mine")):
        a('<div class="plate plate-%s">' % E(pkey))
        a("<h3>%s%s <span class=\"v v-note\">%s</span></h3>"
          % (counted(".plate-%s ul.items > li" % pkey, len(group)), title, who))
        a('<ul class="items">')
        for i in group:
            cond = i.get("closes_when") or "NO CLOSE CONDITION — frozen legacy item"
            inf = " · owner inferred" if i.get("owner_inferred") else ""
            a("<li%s>%s%s<span class=\"id\">%s%s</span><span class=\"ti\">%s</span>"
              "<span class=\"cw\">Closes when: %s</span></li>"
              % (proj_attr(i), pri_badge(i["id"], prio), proj_tag(i),
                 E(i["id"]), E(inf), E(i["title"]), E(cond)))
        a("</ul></div>")
    a("</div>")
    a('<p class="sourceline">SOURCE · knowledge/_state.json (items where state = open).</p>')
    a("</div></section>")

    # ---- provenance gap ---------------------------------------------------
    if gaps["measured"] and gaps["fails"]:
        a('<section class="band"><div class="wrap">')
        a('<p class="label">Yours alone — the provenance gap</p>')
        a("<h2>%d checks, %d rulings, nobody else&rsquo;s to answer</h2>"
          % (len(gaps["fails"]), len(gaps["ids"])))
        a("<p>These are the live words of <code>knowledge/_governs.py --selftest</code>, run by this "
          "generator. Each one wants a <code>governs</code>, <code>evidence</code> or "
          "<code>status</code> value on a ruling in <code>_rulings.json</code>. "
          "<strong>No value has been drafted, guessed, or suggested here</strong> — a provenance "
          "field authored by an agent is a false inscription, which is the failure this gate exists "
          "to catch. Rulings affected: %s.</p>" % E(", ".join(gaps["ids"])))
        a('<ol class="fails">')
        for f in gaps["fails"]:
            a("<li>%s</li>" % E(f))
        a("</ol>")
        a('<p class="sourceline">SOURCE · live run, <code>python3 knowledge/_governs.py '
          '--selftest</code>. The gate could not run at all for five sessions (#158–#163) because '
          '_build_all.py aborted above it — see _LIVE-STATE.md #164.</p>')
        a("</div></section>")

    # ---- future-state lane ------------------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">The forward lane</p>')
    a("<h2>%d things held for later</h2>" % len(future))
    a('<p class="meta">Read straight out of <code>_FUTURE-STATE.md</code>. Status is the file&rsquo;s '
      'own word. Nothing here has been promoted, re-prioritised or re-worded.</p>')
    a('<div class="future">')
    for f in future:
        a('<div class="row"><span class="st">%s</span><span class="ti">%s</span></div>'
          % (E(f["status"]), E(re.sub(r"[*`]", "", f["title"]))))
    a("</div>")
    a('<p class="sourceline">SOURCE · _FUTURE-STATE.md.</p>')
    a("</div></section>")

    # ---- footer -----------------------------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">How to read this page</p>')
    a("<p class=\"meta\">Generated by <code>knowledge/gen_dashboard.py</code> from the stores; it is "
      "never hand-edited. <code>--check</code> regenerates and compares, so a stale dashboard fails "
      "the build rather than lying quietly. It carries no timestamp on purpose: its clock is the "
      "session number in <code>_CHAIN.md</code> (#%s) and the measurements themselves.</p>"
      % E(session["session"]))
    a("<p class=\"meta\">Components are Mono, from <code>knowledge/canon/canon.css</code> — nothing "
      "new was invented. Layout follows the swiss-design-system skill. Every verdict is a WORD "
      "first; the two-red law (red #DA1A00) and its green mirror (#137F3C) are applied on white, "
      "light mode only, as redundant confirmation. The blue rules and dashes are decorative and "
      "carry no meaning.</p>")
    a("<p class=\"meta\">This page reports. It does not repair, rule, or promote anything.</p>")
    a("</div></section>")
    a(PROJECT_JS)
    a("</body></html>")
    return "\n".join(o) + "\n"


def build(with_gates=True, gates_sink=None):
    gates = run_gates(with_gates)
    # #193 — the caller may need the SAME gate results this page was rendered from; re-running
    # them would be a second measurement of a moving target (two readers of one object, the
    # drift class). One run, handed out.
    if gates_sink is not None:
        gates_sink.extend(gates)
    gmap = {g["name"]: g for g in gates}
    state = read_state()
    rulings = read_rulings()
    gaps = provenance_gaps(gmap.get("provenance"))
    ratchets = read_ratchets()
    tdebt = type_debt(gmap.get("type-composites"), ratchets["type"]["baseline"])
    session = read_session()
    # ---- s172-D1 REFUSALS, at BUILD, in the path `--check` runs every build. A constant
    # typed in this file that nothing checks is exactly the class the store gate exists to
    # end, so the two project constants are proved against the live data here rather than
    # in a selftest nothing runs [[instrument-without-a-consumer]].
    if tuple(PROJECT_LABEL) != _state.PROJECT_VALUES:
        raise SystemExit("gen_dashboard REFUSING: PROJECT_LABEL keys %r have forked from the "
                         "gate's enum %r. This page would render a project the store refuses, "
                         "or silently render nothing for one the store accepts."
                         % (tuple(PROJECT_LABEL), _state.PROJECT_VALUES))
    _ids = {i["id"] for i in state["items"]}
    _ghosts = [i for i in PROJECT_CHECK if i not in _ids]
    if _ghosts:
        raise SystemExit("gen_dashboard REFUSING: PROJECT_CHECK names %r, which is not in "
                         "_state.json. An ambiguity flag pointing at an item that no longer "
                         "exists is a note about nothing, and it would sit on this page "
                         "unfalsifiable. If the item was closed or renamed, drop it from "
                         "PROJECT_CHECK deliberately." % (_ghosts,))
    if abs(WEIGHTS_SUM - 1.0) > 1e-9:                    # a score out of 100 that isn't
        raise SystemExit("gen_dashboard REFUSING: CRITERIA weights sum to %r, not 1.0 — a "
                         "score presented as /100 must be a weighted mean, not an arbitrary "
                         "total." % WEIGHTS_SUM)
    prio = priorities(state["items"], session["session"])
    cov = links_coverage(state["items"])
    return render(state, rulings, gaps, session, ratchets, tdebt,
                  read_future_state(), gates, wave_claim(rulings["rulings"]),
                  kanban_columns(state["items"], prio), prio, cov)


def effort_selftest():
    """Both-direction arms for the #168 effort rung machinery (s168-D2 pending, Dave's).

    ⛔ These exist because the arms that proved this change at build time would otherwise have
    been run ONCE, by the lane that wrote it — and a test that only ever ran in the session
    that authored the code cannot catch the session that edits it
    [[instrument-without-a-consumer]]. Every arm re-enacts a defect: a green that cannot fail
    is an assertion, not a test.

    ⛔ NO STORE IS TOUCHED and NO VALUE IS AUTHORED: the rungs below are planted on a
    throwaway in-memory copy of one item, never written back.
    """
    import copy
    fails, n = [], 0

    def arm(name, cond, detail=""):
        nonlocal n
        n += 1
        if not cond:
            fails.append("[%s] %s" % (name, detail))

    items = read_state()["items"]
    session = read_session()["session"]
    tgt = next(i["id"] for i in items if i.get("state") not in ("done", "dropped"))

    def score(rung):
        it = copy.deepcopy(items)
        for i in it:
            if i["id"] == tgt:
                i.pop(_state.EFFORT, None)
                if rung is not None:
                    i[_state.EFFORT] = rung
        return priorities(it, session)["by_id"][tgt]

    # 1. ABSENT ⇒ the criterion is not there at all. Not zero, not flagged missing.
    r0 = score(None)
    arm("absent ⇒ no effort sub-score", "effort" not in r0["sub"], repr(r0["sub"]))
    arm("absent ⇒ NOT reported as a missing input",
        not any(m[0] == "effort" for m in r0["missing"]),
        "a dropped criterion is not a hole in the total")

    # 2. Each rung scores AS MAPPED, and the mapping is monotone S > M > L.
    got = {}
    for rung in _state.EFFORT_VALUES:
        r = score(rung)
        got[rung] = r["score"]
        arm("rung %s scored from the field" % rung,
            r["sub"].get("effort") == EFFORT_SCORE[rung],
            "sub=%r wanted %r" % (r["sub"].get("effort"), EFFORT_SCORE[rung]))
        exp = int(round(100 * sum(w * r["sub"][k] for k, _n, w, _d, _s in active_criteria(True))))
        arm("rung %s total is the weighted mean over the ACTIVE criteria" % rung,
            exp == r["score"], "recomputed %d vs %d" % (exp, r["score"]))
    arm("the rungs are ordered S > M > L", got["S"] > got["M"] > got["L"], repr(got))
    arm("a rung MOVES the score off the absent baseline",
        got["S"] != r0["score"] and got["L"] != r0["score"],
        "planting a rung that changes nothing would mean the field is not being read")

    # 3. A malformed rung is DROPPED and NAMED — never laundered into "no estimate", and
    #    never scored 0.0, which would silently rank it as the most expensive job there is.
    rx = score("XL")
    arm("illegal rung is not scored", "effort" not in rx["sub"], repr(rx["sub"]))
    arm("illegal rung is NAMED as a missing input",
        any(m[0] == "effort" for m in rx["missing"]), repr(rx["missing"]))
    arm("illegal rung falls to the renorm path, NOT to 0.0",
        rx["score"] == r0["score"], "%d vs absent %d" % (rx["score"], r0["score"]))

    # 4. Both weightings are weighted MEANS, and the absent case is bit-identical to the
    #    module-level CRITERIA the page prints. This is the control the whole change rests on.
    for has, label in ((False, "absent"), (True, "present")):
        s = sum(w for _k, _n, w, _d, _s in active_criteria(has))
        arm("weights sum to 1.0 (%s)" % label, abs(s - 1.0) < 1e-9, repr(s))
    arm("absent-case weights ARE the printed CRITERIA",
        [round(w, 9) for _k, _n, w, _d, _s in active_criteria(False)]
        == [round(c[2], 9) for c in CRITERIA],
        "the page would print weights no item is scored on")
    arm("present-case restores Dave's absolutes",
        [round(w, 4) for _k, _n, w, _d, _s in active_criteria(True)]
        == [0.30, 0.20, 0.15, 0.10, 0.10, 0.15],
        "with all six raw ratios in play the weights ARE the ratios, unrenormalized")

    # 5. THE VOCABULARY IS ONE SET. The scorer's mapping and the gate's enum must not fork.
    arm("EFFORT_SCORE keys == the gate's enum",
        tuple(EFFORT_SCORE) == _state.EFFORT_VALUES,
        "%r vs %r" % (tuple(EFFORT_SCORE), _state.EFFORT_VALUES))

    # 6. The anchors reader: parses the real log, and REFUSES loudly rather than crashing or
    #    guessing when it cannot [[a-crash-is-not-a-fail]].
    an = effort_anchors()
    arm("anchors read the real gauge log", an["n"] >= 8 and 0 < an["s_edge"] < an["l_edge"],
        repr(an))
    arm("edges are rounded hard (nearest 5,000)",
        an["s_edge"] % 5000 == 0 and an["l_edge"] % 5000 == 0, repr(an))
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        thin = os.path.join(td, "thin.md")
        with open(thin, "w", encoding="utf-8") as fh:
            fh.write("#### 2026-01-01 #1\n> job 40,000\n> job 50,000\n")
        try:
            effort_anchors(thin)
            arm("thin corpus REFUSED", False, "a quartile over 2 points was accepted")
        except SystemExit as e:
            arm("thin corpus REFUSED, and the refusal names the count",
                "only 2" in str(e), str(e))
        try:
            effort_anchors(os.path.join(td, "nope.md"))
            arm("unreadable log REFUSED", False, "a missing gauge log was accepted")
        except SystemExit as e:
            arm("unreadable log REFUSED, and the refusal names the file",
                "cannot read the gauge log" in str(e), str(e))

    # 7. ⛔ THE AUTHORSHIP RULE, ASSERTED AGAINST THE LIVE STORE. Not a comment — a test.
    authored = [i["id"] for i in items if _state.EFFORT in i]
    arm("no effort value is authored in the store (Dave's alone)",
        not authored, "found rungs on %r — if these are Dave's, this arm is the one to "
                      "change, deliberately, with his word attached" % (authored,))

    # 8. #193 — the COULD-NOT-ASK path, both directions, driven through the real functions.
    refusal_selftest(arm)
    return fails, n


def main(argv):
    if "--selftest" in argv:
        fails, n = effort_selftest()
        for f in fails:
            print("  FAIL " + f)
        print("gen_dashboard effort selftest: %d arms, %s"
              % (n, "all GREEN" if not fails else "%d RED" % len(fails)))
        return 1 if fails else 0
    # `--anchors`: print the DERIVED effort rung edges and the corpus they came from, and
    # exit. Report-only, and deliberately not a second source of truth — it prints exactly
    # what the page prints, from the same call, so the two cannot disagree. (The reader is
    # already CONSUMED by every build via render(); this flag is for reading it by hand, not
    # the thing that makes it real [[instrument-without-a-consumer]].)
    if "--anchors" in argv:
        an = effort_anchors()
        print("effort rung edges — DERIVED from %s (#168 Option C, s168-D2 pending)" % an["source"])
        print("  unit: %s" % _state.EFFORT_UNIT)
        print("  corpus: n=%d priced `job` blocks · min %s · median %s · max %s"
              % (an["n"], f"{an['min']:,}", f"{an['median']:,}", f"{an['max']:,}"))
        for r in _state.EFFORT_VALUES:
            band = ({"S": "<= %s" % f"{an['s_edge']:,}",
                     "M": "%s - %s" % (f"{an['s_edge']:,}", f"{an['l_edge']:,}"),
                     "L": ">  %s" % f"{an['l_edge']:,}"})[r]
            print("  %s  %-22s  %-22s scores %.2f"
                  % (r, band, _state.EFFORT_RUNG_MEANING[r], EFFORT_SCORE[r]))
        print("  ⚠ ESTIMATED, not measured: the edges are measured history; a rung on an "
              "item is Dave's forecast against them. 0 values are authored by any agent.")
        return 0
    check = "--check" in argv
    with_gates = "--no-gates" not in argv
    gates_seen = []
    html = build(with_gates, gates_sink=gates_seen)
    if check:
        if not os.path.exists(OUT):
            print("gen_dashboard --check FAIL — %s does not exist." % os.path.relpath(OUT, ROOT))
            return 1
        cur = _read(OUT)
        if cur != html:
            # #193 — before accusing the page, ask whether this environment could reach the
            # inputs the page was rendered from. See `untracked_inputs()` above for the
            # single-variable isolation that found this.
            return mismatch_verdict(gates_seen)
        print("gen_dashboard --check OK — dashboard/index.html in sync.")
        return 0
    os.makedirs(OUTD, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("gen_dashboard — wrote %s (%d bytes)." % (os.path.relpath(OUT, ROOT), len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
