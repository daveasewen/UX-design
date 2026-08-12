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


def matches(ruling: dict, targets: set[str]) -> bool:
    """A ruling governs a target if any `governs` entry matches a path (by suffix, so a
    repo-relative entry matches an absolute path) or a bare symbol name.

    ⚠ Suffix matching is deliberate and it is the loose direction on purpose: a MISSED ruling
    is the failure this file exists to prevent, and a spurious extra ruling costs three lines of
    reading. The asymmetry is the design, not sloppiness.
    """
    for g in ruling.get("governs", []):
        gn = _norm(g)
        for t in targets:
            if gn == t or t.endswith("/" + gn) or gn.endswith("/" + t):
                return True
            if "/" not in gn and gn in t.replace("/", " ").split():
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


def selftest() -> list[str]:
    """Bites, each failing for a DISTINCT reason. A green that cannot fail is an assertion."""
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
                    failures.append(f"_governs: ruling {r['id']} points at `{t}` (in `{e[:70]}…`) "
                                    f"which does not exist — a pointer index whose pointers rot "
                                    f"is worse than none")

    # 6. ⚓ THE ANCHOR FORM (#127) — ONE BITE PER CLAUSE. A bundle proved by a single bite is a
    #    bundle that is not proved. Fixtures are REAL repo files on purpose: a tempfile cannot
    #    exercise the REPO-relative resolution, which is the thing under test.

    # 6a. POSITIVE CONTROL FIRST, again. Everything below is failure-only, and a failure-only
    #     suite reads green after a revert that deletes the feature entirely.
    anchored = [(r["id"], e) for r in rulings for e in r.get("evidence", [])
                if evidence_form(e) == "anchor"]  # #148 chat/#119 commit are legal, never anchors
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
        fs = selftest()
        print("\n".join(f"  FAIL {f}" for f in fs) if fs else
              "  _governs.py selftest: all bites green")
        return 1 if fs else 0

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
