#!/usr/bin/env python3
"""THE TRIGGER INDEX READER — Dave's open item (e), built #81 2026-08-02.

⛔ THE DEFECT THIS EXISTS TO KILL, stated once so it is never re-derived a fourth time.

#54 (Dave) ruled the token unit: ONE unit, real Claude tokens, cl100k demoted to a labelled
estimator. That ruling is STORED IN TEN PLACES — `notes/_MEMENTO-DECISIONS.md:1716`,
`notes/_GAUGE-LOG.md:461`, `knowledge/_DS-IMPROVEMENTS.md:1422` and EIGHT `_DECISION-HISTORY`
dossiers. Twenty-six sessions later #80 re-measured the same ratio from scratch and nearly filed
it as a discovery. #81 started down the identical path and was stopped by Dave, not by the repo:

    "we've identified this as a problem already, again we are going round in circles"
    "we seem to have a knowledge transfer problem between sessions, isn't this being stored
     anywhere?"

★★ IT WAS STORED. STORAGE WAS NEVER THE PROBLEM. Every mechanism this project has for
remembering is WRITE-optimised, and every mechanism for READING is triggered by SUSPICION —
`_memento_search.py` answers what you ask, and you only ask about what you already suspect
exists. Searching the archive for this very topic at #81 returned THE CURRENT WEEK'S BANNERS,
because retrieval ranks recency above rulings ([[retrieval-default-hides-the-ruling]]).

⇒ SO THE TRIGGER IS NOT A SEARCH, AND MUST NOT BE. It is THE WORK ITSELF. `git diff --name-only`
already knows which files a session touched; `_rulings.json` knows which rulings govern them.
Touch a governed file and you are TOLD, whether or not it occurred to you to ask. That is the
whole mechanism and it is deliberately not clever — the clever version is a better search, and a
better search still has to be CALLED by someone who suspects.

★ THIS SHIPS WITH ITS READER, WHICH IS THE POINT OF IT. `_measure_tokenizer.py` was a correct,
re-runnable instrument with ZERO consumers for fourteen sessions, and its measurement decayed
into a rediscovery precisely because nothing re-read it ([[instrument-without-a-consumer]]).
An index nothing consults would be the same failure wearing this file's name. Hence: wired into
`_capture_gate.py`'s build AND its wrap, not offered as a command someone might remember.

USAGE
    python3 knowledge/_governs.py                    # rulings governing the working tree's diff
    python3 knowledge/_governs.py --since HEAD~3     # ... over a wider range
    python3 knowledge/_governs.py --file knowledge/_capture_gate.py
    python3 knowledge/_governs.py --symbol measure_tokens
    python3 knowledge/_governs.py --all
    python3 knowledge/_governs.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_rulings.json")


class IndexUnreadable(RuntimeError):
    """⚠ LOUD AND NAMED, never a silent empty list.

    An index that fails open is worse than no index: it reports "no rulings govern this" in the
    exact voice it would use if it had checked, which is the confident-false-inscription this
    whole project exists to prevent. A caller that cannot read the index must SAY SO.
    Same shape as `MeasurementRefused` (#79-D1) and adopted deliberately, not by coincidence.
    """


def load(path: str | None = None) -> list[dict]:
    # ⚠ RESOLVED AT CALL TIME, NOT IN THE SIGNATURE. `path: str = INDEX` binds the default when
    # this function is DEFINED, so reassigning `_governs.INDEX` afterwards silently kept reading
    # the old file — the module-level constant looked like the single source of truth and was
    # not. Found by mutation M4 at birth: the "index unreachable" mutation stayed GREEN because
    # the selftest could not actually reach the path it thought it was breaking. ★ Exactly the
    # class this repo keeps re-learning — a green that cannot fail is an assertion, and here the
    # assertion was hiding inside Python's default-argument semantics.
    path = path or INDEX
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError as e:
        raise IndexUnreadable(
            f"⛔ TRIGGER INDEX MISSING — {path} is not there ({e}). No ruling can be surfaced, "
            f"so a session is free to re-derive a settled decision. Restore it from git; do NOT "
            f"proceed on the assumption that nothing is governed.") from e
    except json.JSONDecodeError as e:
        raise IndexUnreadable(
            f"⛔ TRIGGER INDEX UNPARSEABLE — {path} is not valid JSON ({e}). Fix the file. An "
            f"unparseable index must never degrade to 'nothing is governed'.") from e
    rulings = data.get("rulings")
    if not isinstance(rulings, list) or not rulings:
        raise IndexUnreadable(
            f"⛔ TRIGGER INDEX EMPTY — {path} parsed but carries no `rulings` list. An empty "
            f"index and a healthy index with no match are indistinguishable to a caller, which "
            f"is exactly the silent-lookup class.")
    return rulings


def _norm(s: str) -> str:
    return s.strip().replace("\\", "/").lstrip("./").lower()


# ── ⚓ THE DURABLE POINTER FORM, built #127 ───────────────────────────────────────────────────
ANCHOR_SEP = "#"


CHAT_POINTER_RE = re.compile(r"chat #\d+\b")
# #148: a path-shaped token — MUST contain a `/` AND end in a dotted extension, so `s142-D1`,
# a bare date, or a token ADDRESS like `border-radius/surface` can never be claimed as a path.
# Repo-root files keep the legacy whole-string fast-path in the caller.
# ⚠ The FINAL segment permits dots in its stem (#164): `Tooltip.reference.html` — a real,
# existing file — was extracted as `knowledge/snippets/Tooltip.reference` by a stem class that
# excluded `.`, and reported as ROT. Double-extension filenames are the norm in `snippets/`, so
# the extractor, not the pointer, was wrong. Greedy+backtracking still stops at the last dot-run:
# `x.html. Next` yields `x.html`, and a segment with no dot at all still fails to match.
PATHISH_RE = re.compile(r"[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*/[A-Za-z0-9_.\-]*[A-Za-z0-9_\-]\.[A-Za-z0-9]+")


def is_chat_pointer(pointer: str) -> bool:
    """`chat #<n> ...` — live-transcript provenance, a LEGAL pointer form (#148, s148-D1).

    Deliberately narrow: the literal word `chat`, one space, `#`, digits. Checked BEFORE the
    anchor predicate so `chat #143 …` is never claimed as a `<path>#<anchor>` on a file named
    `chat`. It verifies NOTHING on disk and says so — the transcript is not in the repo; an
    honest unverifiable pointer beats a false rot report."""
    return bool(CHAT_POINTER_RE.match(pointer))


def is_anchor_pointer(pointer: str) -> bool:
    """`<path>#<literal text>` — and nothing else may claim to be one.

    ⚠ DELIBERATELY NARROW. `notes/_MEMENTO-DECISIONS.md SS #125` also contains a `#`; if this
    predicate claimed it, a broken PROSE pointer would be re-diagnosed as a broken ANCHOR and its
    real error message would be lost. A path with a space in it is not a path.
    """
    path, sep, anchor = pointer.partition(ANCHOR_SEP)
    return bool(sep) and bool(anchor.strip()) and bool(path.strip()) and " " not in path.strip()


def is_commit_pointer(pointer: str) -> bool:
    """`commit <sha> ...` — verified against git, not the filesystem (#119)."""
    return pointer.startswith("commit ")


def evidence_form(pointer: str) -> str:
    """★ THE ONE PLACE an evidence string is classified. Both readers MUST call this.

    ⛔ THE DEFECT THIS EXISTS TO KILL, reproduced #150. `s148-D1` gave live-chat provenance a
    legal form and it was enacted in the SELFTEST ONLY: `render()` — the default lister, the
    path a human actually reads — kept asking `is_anchor_pointer()` first and reported all
    sixteen `chat #<n>` pointers as "whose FILE `chat` does not exist". The selftest was GREEN
    the whole time, so nothing could ever have caught it: two code paths, one ruling, one of
    them never learned it ([[conflated-fix-guarantees-recurrence]]). Re-stating the ladder in a
    second place would guarantee a third divergence, so the ladder lives HERE and only here.

    Order is load-bearing and is the #148 order: `commit ` and `chat #<n>` are claimed BEFORE
    the anchor predicate, or the word `chat` is read as a file named `chat`.

    Returns one of: `commit` · `chat` · `anchor` · `path` (the legacy `<path>` / `<path>:<int>`
    / annotated-dialect forms, resolved against the filesystem by the caller).
    """
    if is_commit_pointer(pointer):
        return "commit"
    if is_chat_pointer(pointer):
        return "chat"
    if is_anchor_pointer(pointer):
        return "anchor"
    return "path"


# ---------------------------------------------------------------------------------------------
# ★ s177-D1 — THE STANDING EVIDENCE-FORMAT RULE, and the classifier it needs. RULED #177,
# enforcement check PRICED AND QUEUED there (`s172-D3`(e): a new instrument is never built in the
# same breath as the finding that motivates it), BUILT #183.
#
# The rule, verbatim from `_rulings.json` § `s177-D1`:
#   "an evidence pointer into any file the capture ritual rolls (GOOD-MORNING.md banners,
#    notes/_GAUGE-LOG.md strata, _LIVE-STATE.md deltas) is invalid on arrival — point at the
#    commit or the chat"
#
# WHERE IT CAME FROM, so it is never re-derived: `s171-D1`'s surviving anchor pointed into
# `notes/_GAUGE-LOG.md`, which the 2f roll rewrites every wrap. A pointer into a rolling artefact
# is not "at risk of rotting" — it is GUARANTEED to rot, and the failure it produces is
# indistinguishable from an ordinary repoint job, which is why five consecutive sessions read it
# as rot and none of them checked [[read-chain-is-where-staleness-is-free]].
#
# ⛔ THE SCOPE IS INSCRIPTION TIME, AND ONLY INSCRIPTION TIME. "Invalid ON ARRIVAL" is the
# ruling's own wording and it is load-bearing: this list is NOT consulted by `--selftest` or by
# `render()`. Wiring it into either would turn eleven `s175`/`s176` evidence-format entries that
# Dave RATIFIED into new reds, i.e. it would re-litigate ratified record by machine
# [[header-wins-over-audit]] — add, never trim. The ONE consumer is
# `_inscribe_ruling.py`'s R6, which is the only sanctioned writer of `_rulings.json`; nothing
# already inscribed is re-judged by this function [[instrument-without-a-consumer]] names the
# opposite risk, and R6 is the named consumer that answers it.
#
# ⚠ THE LIST IS THE RULING'S LIST, ENUMERATED, NEVER INFERRED. No heuristic guesses which files
# roll — a guessing classifier here would silently start refusing legal pointers the day someone
# renamed a file [[measuring-tool-must-not-guess]]. Adding a file to this tuple is a RULING, not
# a maintenance edit.
ROLLING_FILES = (
    "GOOD-MORNING.md",      # ★ LATEST banner + the residual line — rolled to _GM-ARCHIVE.md
    "notes/_GAUGE-LOG.md",  # the strata the 2f roll rewrites every wrap
    "_LIVE-STATE.md",       # the ⏱ LATEST delta — rolled to _LIVE-STATE-ARCHIVE.md
)


def rolling_target(pointer: str) -> str | None:
    """The rolling file an evidence pointer aims into, or `None` if it aims at nothing that rolls.

    Only the `anchor` and `path` forms can aim at a file at all: `commit ` and `chat #<n>` are the
    two forms the ruling names as the CURE, and they are returned `None` unconditionally rather
    than pattern-matched — a chat line that happens to mention `GOOD-MORNING.md` in its prose is
    not a pointer into it, and a check that cannot tell USE from MENTION is a check that forbids
    talking about the problem [[gate-must-quote-what-it-forbids]].

    The path is compared as a PATH — exact match, or the file's own basename at the repo root —
    never as a substring, so `_GM-ARCHIVE.md` (which is where the banners roll TO, and which does
    not itself roll) is not caught by the `GOOD-MORNING.md` entry.
    """
    if evidence_form(pointer) in ("commit", "chat"):
        return None
    path = pointer.split(ANCHOR_SEP, 1)[0]
    path = path.split(" ", 1)[0].rstrip(":").strip()
    if path.count(":") and path.rsplit(":", 1)[-1].isdigit():
        path = path.rsplit(":", 1)[0]
    path = path.lstrip("./")
    for rolling in ROLLING_FILES:
        if path == rolling or path == os.path.basename(rolling):
            return rolling
    return None


def resolve_anchor(pointer: str) -> tuple[int | None, str]:
    """Resolve `<path>#<literal>` to the line it sits on TODAY. Returns `(lineno, error)`.

    ⛔ THE DEFECT THIS EXISTS TO KILL, found #127, stated once so it is never re-derived.

    `s121-D1` carried `canon.css:5548 RAG roundel policy`. That pointer was TRUE WHEN WRITTEN: at
    `e3174d1` — the tree the ruling was made against — `knowledge/canon/canon.css:5548` IS the
    `Drift: RAG ROUNDEL POLICY` note the ruling cites as its >=4.5:1 precedent. Five sessions
    later the construct sits at 6451 and line 5548 is `--alpha-84: 0.84;`, an unrelated token in
    an unrelated block.

    ★ AND NOTHING COULD EVER HAVE CAUGHT IT. The evidence check verifies `e.split(":")[0]` — the
    FILE — and never looks at the integer at all. A line number in a file that moved 903 lines in
    five sessions was GREEN BY CONSTRUCTION. This entry only went red because its file part was
    also wrong: a bare `canon.css` never resolvable from the repo root, so it was born red at
    #121 and five green wraps reported the file, never the line. ⇒ Repointing it at
    `knowledge/canon/canon.css:5548` would have restored green WHILE POINTING AT THE WRONG
    CONSTRUCT. That is the re-stamp, and avoiding it is the whole reason this function exists.

    ⇒ Same shape as `_gen_chain._steps_in()` (`s125-D1`, enacted #126): a figure that keeps going
    stale is not hand-corrected, it is DERIVED. The index stores the ANCHOR — durable, meaningful,
    greppable — and the integer is computed here on every run and stored nowhere at all. This is
    the answer to "what re-checks this?": the resolver does, on every selftest and every render.

    AMBIGUITY IS RED, never a best guess. A pointer resolving to three places has not been
    re-checked, it has been guessed, and a guess wearing a line number is exactly the
    confident-false inscription the project exists to prevent.
    """
    path, _, anchor = pointer.partition(ANCHOR_SEP)
    path, anchor = path.strip(), anchor.strip()
    full = os.path.join(REPO, path)
    if not os.path.isfile(full):
        return None, (f"points at `{pointer}` whose FILE `{path}` does not exist — a pointer "
                      f"index whose pointers rot is worse than none")
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            hits = [i for i, ln in enumerate(fh, 1) if anchor in ln]
    except OSError as exc:
        return None, (f"cannot READ `{path}` to resolve anchor `{anchor}` ({exc}) — unreadable is "
                      f"not absent, and must never be reported as a clean miss")
    if not hits:
        return None, (f"points at `{pointer}` — the file is there but the ANCHOR TEXT IS GONE. "
                      f"The construct was renamed, moved out or deleted: say WHICH. Do not "
                      f"repoint at whatever currently looks right — that is the #127 re-stamp")
    if len(hits) > 1:
        shown = ", ".join(str(h) for h in hits[:5]) + ("…" if len(hits) > 5 else "")
        return None, (f"points at `{pointer}` — the anchor matches {len(hits)} lines ({shown}). "
                      f"An ambiguous anchor is not a pointer; narrow the literal until unique")
    return hits[0], ""


def names_a_directory(gn: str) -> bool:
    """True iff a normalised `governs` entry points at a real DIRECTORY in this repo.

    ⛔ #208 — SUCH AN ENTRY IS UNDER-SPECIFIED, AND IT GOVERNS NOTHING. Two live entries are of
    this shape (`s202-D3` → `knowledge`, `opacity-primitives-4pct` → `knowledge/`) and they are
    DECLARED by name in `selftest()`, never swallowed. See `matches()`.
    """
    if not gn:
        return False
    return os.path.isdir(os.path.join(REPO, gn.rstrip("/")))


def matches(ruling: dict, targets: set[str]) -> bool:
    """A ruling governs a target if any `governs` entry matches a path (by suffix, so a
    repo-relative entry matches an absolute path) or a bare symbol name.

    ⚠ Suffix matching on FILE names is deliberate and it is the loose direction on purpose: a
    MISSED ruling is the failure this file exists to prevent, and a spurious extra ruling costs
    three lines of reading. The asymmetry is the design, not sloppiness.

    ⛔ #208 — THE ARM THAT WAS TOO LOOSE, AND WHY IT WENT. What stood here also matched a bare
    entry against ANY PATH SEGMENT of the target:

        if "/" not in gn and gn in t.replace("/", " ").split():

    For a bare entry that happens to name a DIRECTORY (`s202-D3` governs `knowledge`), that arm
    made the ruling govern EVERY FILE IN THE REPO'S BIGGEST DIRECTORY — including
    `knowledge/_totally_unrelated_xyzzy.py`, the selftest's own negative control, which is why
    the `_governs` selftest and its consumer `_capture_gate.py --selftest` ([13]) were standing
    red for sessions. For every OTHER bare entry the arm was dead weight: a bare entry matching
    a target's BASENAME is already caught by `t.endswith("/" + gn)`, and a bare SYMBOL target is
    already caught by `gn == t`. Its ONLY distinct effect was directory-segment matching.

    ⛔ AND NO DIRECTORY SCOPE WAS PUT IN ITS PLACE, DELIBERATELY. The obvious-looking fix — read
    a trailing `/` as "everything under here" — WIDENS a live ruling: `opacity-primitives-4pct`
    ("Opacity primitives run in 4% steps") carries `knowledge/`, today a no-op, and a subtree
    reading would hand it the whole `knowledge/` tree. Narrowing a mis-scoped entry to nothing
    and SAYING SO is honest; widening one silently is the [[gate-glob-scope-rule]] failure with
    the sign flipped. ⬛ What these two rulings govern is DAVE'S (via `_inscribe_ruling.py`, the
    only legal writer) — `selftest()` names both entries on every run and prints the remedy.
    """
    for g in ruling.get("governs", []):
        gn = _norm(g)
        if not gn or names_a_directory(gn):
            continue
        for t in targets:
            if gn == t or t.endswith("/" + gn) or gn.endswith("/" + t):
                return True
    return False


def changed_files(since: str | None = None) -> list[str]:
    """Files the session has touched. THIS is the trigger — no one has to remember to ask."""
    cmds = ([["git", "diff", "--name-only", since]] if since else
            [["git", "diff", "--name-only"], ["git", "diff", "--name-only", "--cached"],
             ["git", "ls-files", "--others", "--exclude-standard"]])
    out: list[str] = []
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        if r.returncode == 0:
            out.extend(x for x in r.stdout.splitlines() if x.strip())
    return sorted(set(out))


def surface(targets: set[str], rulings: list[dict] | None = None) -> list[dict]:
    return [r for r in (rulings if rulings is not None else load()) if matches(r, targets)]


def render(hits: list[dict], because: str) -> str:
    if not hits:
        return ""
    lines = [f"⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING ({because}) — "
             f"{len(hits)} found. READ BEFORE RE-DERIVING:"]
    for r in hits:
        lines.append(f"  ▸ {r['id']} — RULED {r['ruled']} ({r['date']}, {r['by']}): {r['says']}")
        lines.append(f"      status: {r.get('status', 'unstated')}")
        if r.get("watch"):
            lines.append(f"      ⚠ {r['watch']}")
        for e in r.get("evidence", []):
            # ★ THE INTEGER IS DERIVED HERE, at read time, and stored nowhere (#127). A reader
            #   gets a line number that is true NOW, or an explicit refusal — never a stale one
            #   presented in the same confident voice as a checked one.
            # ★ #150: classified by the SHARED `evidence_form()`, never by a second copy of the
            #   ladder. `chat #<n>` / `commit <sha>` render VERBATIM — they are legal and
            #   unverifiable-by-design, not rot.
            if evidence_form(e) == "anchor":
                path, _, anchor = e.partition(ANCHOR_SEP)
                ln, err = resolve_anchor(e)
                e = (f"{path.strip()}:{ln} — {anchor.strip()}" if ln
                     else f"{e}  ⛔ UNRESOLVED — {err}")
            lines.append(f"      evidence: {e}")
    lines.append("  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is "
                 "Dave's alone.")
    return "\n".join(lines)


def checkout_cannot_hold(rel: str) -> bool:
    """True iff THIS REPO'S OWN IGNORE RULES exclude `rel` — so no clean checkout can carry it.

    ⛔ #194 — THE KEY FOR A COULD-NOT-ASK REFUSAL, and the reason it is this and nothing else.
    An evidence pointer at a path under `outputs/` resolves on the machine that WROTE it and can
    never resolve in a bare clone, because `.gitignore` excludes it. On 711bfd1 that is precisely
    why `_capture_gate.py --selftest` was green locally and RED in CI ([13]): three pointers on
    ds-034/ds-035 name gitignored `outputs/_FINDING-…` and `_PARTITION-…` files. Reporting that
    as "a pointer index whose pointers rot" is the #173 lie in a new shape — a verdict that is a
    function of WHERE it ran [[gate-cannot-pass-in-one-environment]].

    ⚠ AND IT MUST NOT SILENCE REAL ROT, which is the whole risk of adding a refusal. This asks
    git, not an env var and not a path prefix: a TRACKED file that was deleted is NOT ignored, so
    it still fails, loudly, everywhere. `git check-ignore` exits 0 for ignored, 1 for not, and
    128 when it cannot answer — and 128 is read as NOT IGNORED on purpose, so an unreadable git
    falls to the FAILING side. A refusal you cannot prove is not a refusal
    [[measuring-tool-must-not-guess]].
    """
    return subprocess.run(["git", "check-ignore", "-q", "--", rel],
                          cwd=REPO, capture_output=True).returncode == 0


def selftest(refusals: list[str] | None = None) -> list[str]:
    """Bites, each failing for a DISTINCT reason. A green that cannot fail is an assertion.

    `refusals` — #194, the COULD-NOT-ASK channel (`_could_not_ask.py`). Pass a list and evidence
    pointers this CHECKOUT cannot hold (see `checkout_cannot_hold`) are collected there instead
    of counted as failures. ⚠ OPT-IN by design: with no list passed, they stay FAILURES exactly
    as before, so no caller that has not been taught the third verdict is silently softened.
    Either way each one is PRINTED — an unreachable input is never inferred from silence.
    """
    failures: list[str] = []
    rulings = load()

    # 1. POSITIVE CONTROL FIRST — a failure-only suite reads green after a revert that deletes
    #    the comparison entirely. Prove the index HITS before proving it misses.
    hit = surface({"knowledge/_capture_gate.py"}, rulings)
    if not hit:
        failures.append("_governs: `knowledge/_capture_gate.py` matched NO ruling — it is "
                        "governed by ds-021 at minimum; the matcher is dead")
    if not any(r["id"] == "ds-021" for r in hit):
        failures.append("_governs: _capture_gate.py did not surface ds-021 — the exact ruling "
                        "#80 re-derived and #81 started to re-derive again")

    # 2. THE SYMBOL PATH, which is the one that catches an edit inside an ungoverned-looking file
    if not any(r["id"] == "ds-021" for r in surface({"measure_tokens"}, rulings)):
        failures.append("_governs: the bare symbol `measure_tokens` surfaced no ruling — a "
                        "session editing it by name would be told nothing")

    # 3. THE NEGATIVE CONTROL. If everything matches everything, the index is decoration.
    if surface({"knowledge/_totally_unrelated_xyzzy.py"}, rulings):
        failures.append("_governs: an unrelated path matched a ruling — the matcher is too "
                        "loose to carry information")

    # 3a. #208 — THE PRECISION ARMS, BOTH DIRECTIONS, on SYNTHETIC rulings so they are exercised
    #     whatever the live corpus happens to hold (a bite that depends on today's data is a
    #     bite that quietly stops biting). One arm per clause.
    _bare_dir = {"id": "SYNTH-bare-dir", "governs": ["knowledge"]}
    _slash_dir = {"id": "SYNTH-slash-dir", "governs": ["knowledge/"]}
    if matches(_bare_dir, {"knowledge/_totally_unrelated_xyzzy.py"}):
        failures.append("_governs: a bare entry `knowledge` matched a PATH SEGMENT — the #208 "
                        "too-loose arm is back and one ruling governs the whole tree again")
    if matches(_slash_dir, {"knowledge/_totally_unrelated_xyzzy.py"}):
        failures.append("_governs: a `knowledge/` entry matched a file under it — #208 refuses "
                        "subtree scope on purpose (it would WIDEN opacity-primitives-4pct); a "
                        "directory entry governs nothing and is DECLARED instead")
    if not matches({"id": "SYNTH-file", "governs": ["_capture_gate.py"]},
                   {"knowledge/_capture_gate.py"}):
        failures.append("_governs: a bare FILE name stopped matching its repo-relative path — "
                        "the #208 narrowing cut too deep; basename suffix matching must stand")
    if not matches({"id": "SYNTH-sym", "governs": ["measure_tokens"]}, {"measure_tokens"}):
        failures.append("_governs: a bare SYMBOL stopped matching itself — the #208 narrowing "
                        "cut too deep; the symbol path is the one that catches an edit inside "
                        "an ungoverned-looking file")
    if matches({"id": "SYNTH-near", "governs": ["_capture_gate.py"]},
               {"knowledge/_capture_gate_helpers.py"}):
        failures.append("_governs: `_capture_gate.py` matched `_capture_gate_helpers.py` — a "
                        "NEAR MISS must miss, or the suffix arm is prefix-matching")

    # 3b. ⬛ DECLARED, NEVER SILENT (#208). A `governs` entry that names a real DIRECTORY is
    #     under-specified: it used to govern that whole subtree by accident (bare form) or
    #     nothing at all (slash form), and it now governs nothing in BOTH forms. Printing it by
    #     name is the difference between a narrowing and a disappearance.
    #     ⛔ NOT a failure: what a ruling governs is DAVE'S, and a matcher may not re-scope a
    #     ruling by going red at it. Re-scoping goes through `_inscribe_ruling.py`.
    #     ⚠ TWO SHAPES, AND ONLY ONE OF THEM CHANGED BEHAVIOUR. A directory entry CONTAINING a
    #     `/` (`knowledge/tokens`, `knowledge/snippets/`) never matched a file path before #208
    #     either — the old arm 3 required a bare token — so those are a PRE-EXISTING
    #     under-specification, counted in one line, not shouted 32 times into every capture-gate
    #     run. A BARE directory token is the one that lost reach here, and it is named in full.
    _dir_slashed: list[str] = []
    for r in rulings:
        for g in r.get("governs", []):
            gn = _norm(g)
            if not names_a_directory(gn):
                continue
            if "/" in gn:  # ⚠ the OLD arm 3's own guard was `"/" not in gn` — same test, so
                           #   this classifies by what actually changed, not by what looks tidy
                _dir_slashed.append(f"{r['id']}→{g}")
                continue
            print(f"_governs: ⬛ DECLARED (#208) — ruling {r['id']} governs the BARE token `{g}`, "
                  f"which is a real DIRECTORY. Before #208 it matched every path carrying a "
                  f"`{gn.rstrip('/')}` segment (the too-loose arm, and the reason the negative "
                  f"control and [13] were red); it now governs NOTHING. REACH LOST HERE. "
                  f"Remedy: name the files/symbols it really governs, via `_inscribe_ruling.py` "
                  f"— the only legal writer of _rulings.json. ⛔ That scope is Dave's call, not "
                  f"this gate's.")
    if _dir_slashed:
        print(f"_governs: ⬛ DECLARED (#208) — {len(_dir_slashed)} `governs` entr(ies) name a "
              f"DIRECTORY with a path separator; they governed no file BEFORE #208 and govern "
              f"none after (unchanged, pre-existing under-specification, not a #208 narrowing): "
              f"{', '.join(_dir_slashed)}")

    # 4. ⛔ THE FAIL-LOUD SEAM. An unreadable index must RAISE, never return []. This is the
    #    whole difference between this file and the search it replaces.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bad = os.path.join(td, "broken.json")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("{not json")
        try:
            load(bad)
            failures.append("_governs: an UNPARSEABLE index did not raise — it degraded to "
                            "'nothing is governed', which is the silent-lookup class this file "
                            "was built to end")
        except IndexUnreadable:
            pass
        except Exception as e:
            failures.append(f"_governs: unparseable index raised {type(e).__name__}, not "
                            f"IndexUnreadable — the failure must be NAMED or the caller reports "
                            f"'something went wrong' and the next session re-diagnoses it")
        empty = os.path.join(td, "empty.json")
        with open(empty, "w", encoding="utf-8") as fh:
            json.dump({"rulings": []}, fh)
        try:
            load(empty)
            failures.append("_governs: an EMPTY index did not raise — empty and no-match are "
                            "indistinguishable to a caller")
        except IndexUnreadable:
            pass
        missing = os.path.join(td, "nope.json")
        try:
            load(missing)
            failures.append("_governs: a MISSING index did not raise")
        except IndexUnreadable:
            pass

    # 5. Every entry carries what a reader needs. A pointer with no evidence is a second copy
    #    of canon waiting to happen.
    for r in rulings:
        for field in ("id", "ruled", "date", "by", "says", "governs", "evidence", "status"):
            if not r.get(field):
                failures.append(f"_governs: ruling {r.get('id', '?')!r} is missing `{field}` — "
                                f"an entry that cannot point a reader at canon IS canon, and "
                                f"this file must never become the eleventh copy")
        for e in r.get("evidence", []):
            # #119: `commit <sha>` is a LEGAL pointer form — verified against git, not the
            # filesystem. Before this, an honest commit pointer had no legal form here and
            # real hashes were reported as rot ([[honest-refusal-needs-a-legal-form]] class).
            form = evidence_form(e)  # #150: the SHARED classifier — see `evidence_form()`
            if form == "commit":
                sha = e.split()[1]
                ok = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                                    cwd=REPO, capture_output=True).returncode == 0
                if not ok:
                    failures.append(f"_governs: ruling {r['id']} points at `{e}` which is not "
                                    f"a commit in this repo — a pointer index whose pointers "
                                    f"rot is worse than none")
                continue
            # #148 (s148-D1): `chat #<n> ...` is a LEGAL pointer form — live-transcript
            # provenance, DECLARED unverifiable from the filesystem (the transcript is not in
            # the repo). Same class as the `commit ` form above
            # ([[honest-refusal-needs-a-legal-form]]): without it the anchor predicate claimed
            # the word `chat` as a path and four rulings' honest provenance was reported as
            # rot — found by the #148 full `_build_all.py` drive, a dead-runner casualty.
            if form == "chat":
                continue
            # ⚓ #127: the ANCHOR form is checked by CONTENT, not by an integer. See
            # `resolve_anchor` for the defect it kills; the legacy `<path>` and `<path>:<int>`
            # forms fall through to the existence check below, unchanged.
            if form == "anchor":
                # s177-D1 (dream-pass 7 P4a): a SUPERSEDED ruling's anchor is RETIRED, not
                # repointed — enacting the successor rewrites the very line the anchor names
                # (s129-D1's anchor died the moment s171-D1 landed in _gauge_tokens.py), so
                # resolving it is a permanent false-red, one per re-based constant, forever.
                # ⛔ The skip PRINTS every skipped anchor, never swallows: a silent skip
                # would let a mislabelled `superseded_by` hide real rot.
                sup = r.get("superseded_by")
                if sup:
                    print(f"_governs: SKIPPED anchor on superseded ruling {r['id']} "
                          f"(superseded_by {sup}): `{e[:80]}`")
                    continue
                _ln, err = resolve_anchor(e)
                if err:
                    failures.append(f"_governs: ruling {r['id']} {err}")
                continue
            p = os.path.join(REPO, e.split(":")[0])
            if os.path.exists(p):
                continue  # legacy `<path>` / `<path>:<int>` fast-path — anything green before #148 stays green
            # #148 (s148-D1): the #135–#145 corpus wrote evidence as `<path> (note)`,
            # `<path> - note`, `a · b · c`, or `prose: <path>` — 16 honest annotated pointers
            # reported as rot by the split(":") read. Extract every path-shaped token (must
            # contain a `/`); EACH must exist. A string with NO token is prose wearing an
            # evidence slot — still red: prose provenance has the `chat #<n>` / `commit ` legal
            # forms ([[honest-refusal-needs-a-legal-form]]).
            tokens = [t.rstrip(".") for t in PATHISH_RE.findall(e)]
            if not tokens:
                failures.append(f"_governs: ruling {r['id']} evidence `{e}` carries NO pointer "
                                f"— prose provenance needs the `chat #<n>`/`commit ` legal "
                                f"form, never a bare sentence")
                continue
            for t in tokens:
                if not os.path.exists(os.path.join(REPO, t)):
                    if checkout_cannot_hold(t):
                        # #194: UNREACHABLE INPUT, not rot. Said out loud either way.
                        msg = (f"ruling {r['id']}'s evidence `{t}` is excluded by this repo's "
                               f"own .gitignore — no checkout can hold it, so whether it has "
                               f"rotted is UNASKABLE here; the machine that wrote it is where "
                               f"that question has an answer")
                        print(f"_governs: COULD-NOT-ASK — {msg}")
                        (refusals if refusals is not None else failures).append(msg)
                        continue
                    failures.append(f"_governs: ruling {r['id']} points at `{t}` (in `{e[:70]}…`) "
                                    f"which does not exist — a pointer index whose pointers rot "
                                    f"is worse than none")

    # 6. ⚓ THE ANCHOR FORM (#127) — ONE BITE PER CLAUSE. A bundle proved by a single bite is a
    #    bundle that is not proved. Fixtures are REAL repo files on purpose: a tempfile cannot
    #    exercise the REPO-relative resolution, which is the thing under test.

    # 6a. POSITIVE CONTROL FIRST, again. Everything below is failure-only, and a failure-only
    #     suite reads green after a revert that deletes the feature entirely.
    anchored = [(r["id"], e) for r in rulings for e in r.get("evidence", [])
                if evidence_form(e) == "anchor"  # #148 chat/#119 commit are legal, never anchors
                and not r.get("superseded_by")]  # s177-D1: a superseded ruling's anchor is
                # RETIRED — asking it to resolve against live code is a permanent false-red.
                # NOT silent: section 5 above PRINTS every skipped anchor before this runs.
    if not anchored:
        failures.append("_governs: NO evidence pointer is in anchor form — either the form was "
                        "reverted out of the index or it never landed. The anchor bites below "
                        "cannot fail, so they are asserting, not testing")
    for rid, e in anchored:
        ln, err = resolve_anchor(e)
        if err or ln is None:
            failures.append(f"_governs: anchor positive control — ruling {rid}'s `{e}` did not "
                            f"resolve ({err or 'no line returned'})")
            continue
        # 6b. ROUND TRIP. Re-read the resolved line and prove it really holds the anchor. Without
        #     this the bite passes on ANY integer the resolver cares to return — the #125
        #     `parse()`-faking-`{"ratio":1}` shape, where a return value was the stale claim.
        path, _, anchor = e.partition(ANCHOR_SEP)
        with open(os.path.join(REPO, path.strip()), encoding="utf-8", errors="replace") as fh:
            got = fh.readlines()[ln - 1]
        if anchor.strip() not in got:
            failures.append(f"_governs: anchor ROUND TRIP failed for {rid} — resolved "
                            f"{path.strip()}:{ln} does not contain `{anchor.strip()}`. The "
                            f"resolver is returning a number, not a location")

    # ⚠ ASSEMBLED AT RUNTIME, NOT WRITTEN AS ONE LITERAL. Spelled out whole it would occur in
    #   THIS file, and the day a fixture points here the 'absent' bite would find ITSELF and pass
    #   for the wrong reason. The self-reference trap is cheap to fall into and free to avoid.
    absent = "zzz" + "_anchor_absent_" + "xyzzy"
    # 6c. Anchor text GONE from a file that exists — the case the old check could not see at all.
    if not resolve_anchor(f"knowledge/_rulings.json{ANCHOR_SEP}{absent}")[1]:
        failures.append("_governs: an ABSENT anchor resolved — the anchor form is checking the "
                        "file's EXISTENCE and not its CONTENT, which is the old defect wearing "
                        "new syntax")
    # 6d. Missing file — the legacy guarantee must survive inside the new form.
    if not resolve_anchor(f"knowledge/_no_such_file_{absent}.py{ANCHOR_SEP}x")[1]:
        failures.append("_governs: an anchor on a MISSING FILE resolved")
    # 6e. Ambiguity is RED, not a first-match guess.
    if not resolve_anchor(f"knowledge/_governs.py{ANCHOR_SEP}failures.append(")[1]:
        failures.append("_governs: an AMBIGUOUS anchor resolved to a single line — a pointer "
                        "matching many places has been guessed, not re-checked")
    # 6f. PREDICATE NEGATIVE CONTROL. These two must NOT be claimed as anchors, or a broken
    #     legacy/prose pointer is re-diagnosed as a broken anchor and its real error is lost.
    for not_anchor in ("canon.css:5548 RAG roundel policy",
                       "notes/_MEMENTO-DECISIONS.md SS #125"):
        if is_anchor_pointer(not_anchor):
            failures.append(f"_governs: `{not_anchor}` was claimed as an anchor pointer — the "
                            f"predicate is too loose and the legacy path check is bypassed")
    # 6g. CHAT POINTER FORM (#148, s148-D1) — one bite per clause, both directions. The
    #     positive control exists in the REAL corpus too (four rulings carry `chat #<n>`
    #     evidence), but a synthetic pair keeps the clause biting if those entries are edited.
    if not is_chat_pointer("chat #999 (live) - synthetic positive"):
        failures.append("_governs: `chat #999 …` was NOT recognised as a chat pointer — the "
                        "#148 legal form has been reverted and honest live-chat provenance "
                        "will be reported as rot again")
    for not_chat in ("chxt #135 mutation control", "chat 135 no hash", "chatter #1 prefix-trap"):
        if is_chat_pointer(not_chat):
            failures.append(f"_governs: `{not_chat}` was claimed as a chat pointer — the "
                            f"predicate is too loose; a typo’d path could pass unverified")
    # 6h. PATH EXTRACTION (#148) — the annotated-pointer read, one bite per clause.
    if PATHISH_RE.findall("prose with no pointer in it at all"):
        failures.append("_governs: extraction found a path in pure prose — too loose, a "
                        "sentence could pass as evidence")
    if PATHISH_RE.findall("s142-D1's own record (no slash, not a path)"):
        failures.append("_governs: extraction claimed a slashless token as a path — the `/` "
                        "requirement has been lost")
    if PATHISH_RE.findall("radius {console:12 via border-radius/surface} token address"):
        failures.append("_governs: extraction claimed a token ADDRESS as a path — the "
                        "dotted-extension requirement has been lost (s135-D1's false rot, #148)")
    if [t.rstrip(".") for t in PATHISH_RE.findall("see reviews/zzz_no_such_xyzzy.html - note")] \
            != ["reviews/zzz_no_such_xyzzy.html"]:
        failures.append("_governs: extraction failed to lift the exact annotated path — the "
                        "#148 dialect read is broken and rot reports are unreliable")

    # 6i. ⛔ THE SECOND READER (#150). Everything above tests the SELFTEST's ladder. `render()`
    #     is the path a human reads, and for two sessions it carried its own copy of that ladder
    #     with the #148 clause missing — sixteen legal `chat #<n>` pointers printed as rot while
    #     this suite read green. So the bite DRIVES THE FEATURE: render the real corpus and
    #     assert no legal form is reported UNRESOLVED. A predicate test cannot see this; only
    #     running the other reader can ([[mutation-tests-the-clause-not-the-feature]]).
    for rid, e in [(r["id"], e) for r in rulings for e in r.get("evidence", [])
                   if evidence_form(e) in ("chat", "commit")]:
        out = render([{"id": rid, "ruled": "x", "date": "x", "by": "x", "says": "x",
                       "evidence": [e]}], "selftest 6i")
        if "UNRESOLVED" in out:
            failures.append(f"_governs: render() reported the LEGAL {evidence_form(e)} pointer "
                            f"`{e[:60]}…` ({rid}) as UNRESOLVED — the lister is not using "
                            f"`evidence_form()` and s148-D1 is enacted in one reader only")
    if "UNRESOLVED" not in render([{"id": "zzz", "ruled": "x", "date": "x", "by": "x",
                                    "says": "x", "evidence":
                                    [f"knowledge/_no_such_{'xyzzy'}.py#anchor"]}], "selftest 6i"):
        failures.append("_governs: render() did NOT report a genuinely rotten anchor as "
                        "UNRESOLVED — 6i's positive bite above cannot fail, so it is asserting")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Which rulings govern what you are touching?")
    ap.add_argument("--since", help="git ref to diff against (default: working tree)")
    ap.add_argument("--file", action="append", default=[])
    ap.add_argument("--symbol", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        rf: list[str] = []
        fs = selftest(refusals=rf)
        print("\n".join(f"  FAIL {f}" for f in fs) if fs else
              "  _governs.py selftest: all bites green"
              + (f" ({len(rf)} pointer(s) UNASKABLE in this checkout)" if rf else ""))
        # #194 — a REAL failure outranks a refusal: 1 wins over 77 whenever both are present, so
        # a refusal can never be the reason a red went unreported.
        if fs:
            return 1
        if rf:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import _could_not_ask as cna
            return cna.refuse("_governs.py --selftest",
                              f"{len(rf)} evidence pointer(s) name paths this checkout cannot "
                              f"hold: " + " · ".join(rf))
        return 0

    try:
        rulings = load()
    except IndexUnreadable as e:
        print(str(e), file=sys.stderr)
        return 2

    if a.all:
        print(render(rulings, "--all"))
        return 0

    targets = {_norm(x) for x in (a.file + a.symbol)}
    because = "explicit"
    if not targets:
        files = changed_files(a.since)
        targets = {_norm(f) for f in files}
        because = f"{len(files)} file(s) touched" + (f" since {a.since}" if a.since else "")
        if not files:
            print("  no changed files — nothing to check")
            return 0

    hits = surface(targets, rulings)
    print(render(hits, because) if hits
          else f"  no ruling governs the {len(targets)} target(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
