#!/usr/bin/env python3
"""_gate_doc_rows.py — the new-doc-needs-a-store-row gate (W-20, forgotten-document class #185).

THE CLASS: a document with no `_state.json` row is invisible to every carry — two documents
lived weeks unseen (#185). This gate makes the PRESENCE of a row a checked condition for
new tracked documents, per [[gate-inside-the-growth-loop]]: gate the presence, not the drift.

POPULATION: git-tracked files matching notes/_briefs/* or _BRIEF-* whose first-add date
(git log --diff-filter=A, one pass, no --follow) is >= BASELINE_DATE.
BASELINE_DATE = "2026-08-15" is PICKED, not derived — it is the earliest date covering both
known offenders of the class; Dave may rule his own number. Earlier docs are a frozen legacy
set by date, exempt exactly as _state.LEGACY_IDS is.

A doc COUNTS AS ROWED when some item's `home` field names it (path or basename). `home` ONLY:
a prose MENTION in another row's body is not a row FOR the doc [[gate-must-quote-what-it-forbids]]
— the actual #185 offender was MENTIONED in W-18's body at #186 while still unrowed, so a
whole-text matcher cannot see the class's own founding case (proven in this gate's first draft).

FAILURE IS LOUD AND NAMED (a crash is not a fail): each unrowed doc is printed with its
add-date; exit 1. The fix is one `_state.add()` call through the store's own writer —
this gate never writes anything.

CONSUMER: run `python3 knowledge/_gate_doc_rows.py --check` at the capture ritual /
pre-commit seam. Declared at birth: not yet routed in any build script — the conductor
wires or prices that (an instrument without a consumer cannot fail).

Selftest drives the gate on REAL data both directions:
  fail-arm: the store as of commit 6b98be3 (#186 — before W-26/W-27 existed) against
            today's population — the gate MUST flag the 2026-08-16 briefs (the actual
            pre-row state of the class's offender, from git history).
  pass-arm: the live store — expected clean today; if not, that is a live finding, and
            the selftest still passes provided the fail-arm proved the gate can fail.
  mutation-arm: the live store text with one known reference deleted — MUST be flagged
            (guards against a matcher loosened into always-true).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import subprocess, sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "knowledge", "_state.json")
BASELINE_DATE = "2026-08-15"  # PICKED, not derived — Dave may rule (see docstring)
PATTERNS = ["notes/_briefs", "_BRIEF-"]
FAIL_ARM_COMMIT = "6b98be3"  # #186 — the offender's pre-row store state

def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout

def staged_adds():
    """[(date, path)] for brief-class docs ADDED IN THE INDEX and not yet committed.

    #207 postscript — THE SINGLE-COMMIT BLINDSPOT. `population()` reads `git log`, which by
    construction only knows about docs that are ALREADY COMMITTED. So the gate could only
    ever fail on the commit AFTER the one that introduced an unrowed doc: a session that adds
    a brief and commits once — the ordinary shape of a wrap — ships it unrowed and unseen,
    and the gate reports PASS while doing it. That is the forgotten-document class walking
    straight through its own gate.

    The staged set is the missing half: files with an ADD in the index against HEAD are the
    docs THIS commit is about to introduce. They carry today's date because that is the date
    the commit will bear; the gate's frozen-legacy cutoff then treats them exactly like any
    other new doc. Empty index (nothing staged) => empty list, and the gate behaves as before.
    """
    from datetime import date
    try:
        out = _git("diff", "--cached", "--diff-filter=A", "--name-only",
                   "--", "notes/_briefs", "_BRIEF-*")
    except subprocess.CalledProcessError:
        # No HEAD to diff against (a virgin repo). NOT silently treated as "nothing staged" —
        # said out loud, because a silent empty here would restore the exact blindspot.
        print("⚠ staged-add scan REFUSED: `git diff --cached` failed (no HEAD?) — the "
              "current commit's adds are NOT covered by this run")
        return []
    today = date.today().isoformat()
    return sorted((today, p.strip()) for p in out.splitlines() if p.strip())


def population(staged=None):
    """[(add_date, path)] for brief-class docs in scope: committed adds on/after
    BASELINE_DATE, PLUS the adds staged in the CURRENT commit (#207 postscript).

    `staged` is injectable so the selftest can plant one without touching the real index.
    """
    out = _git("log", "--diff-filter=A", "--format=C %as", "--name-only",
               "--", "notes/_briefs", "_BRIEF-*")
    date, first_seen = None, {}
    for line in out.splitlines():
        if line.startswith("C "):
            date = line[2:].strip()
        elif line.strip():
            p = line.strip()
            if any(p.startswith(t) or os.path.basename(p).startswith("_BRIEF-") for t in PATTERNS):
                first_seen[p] = date  # log is newest-first; last write wins = oldest = first add
    tracked = set(_git("ls-files").splitlines())
    pop = {p: d for p, d in first_seen.items() if p in tracked and d >= BASELINE_DATE}
    for d, p in (staged_adds() if staged is None else staged):
        if any(p.startswith(t) or os.path.basename(p).startswith("_BRIEF-") for t in PATTERNS) \
                and d >= BASELINE_DATE:
            pop.setdefault(p, d)   # a committed first-add date WINS over today's stamp
    return sorted((d, p) for p, d in pop.items())

def _homes(store_text):
    import json
    d = json.loads(store_text)
    items = d["items"] if isinstance(d, dict) and "items" in d else d
    return [str(it.get("home", "")) for it in items]

def unrowed(store_text, pop):
    homes = _homes(store_text)
    # #215 CLASS FIX (Dave: "always real fixes never patches, they just get lost"): a home that
    # ends in "/" is a DIRECTORY ADDRESS — it rows every file beneath it. Introduced for asset
    # sets (e.g. a research doc's screenshot directory), where one row per PNG would be noise
    # that hides signal, while an unrowed asset stays invisible to every carry. The row still
    # exists, still carries owner/state/close-condition — only the address form widened.
    dir_homes = [h for h in homes if h.rstrip().endswith("/")]
    missing = []
    for d, p in pop:
        base = os.path.basename(p)
        if any(p in h or base in h for h in homes):
            continue
        if any(p.startswith(dh.rstrip()) for dh in dir_homes):
            continue
        missing.append((d, p))
    return missing

def check():
    with open(STORE) as f:
        text = f.read()
    staged = staged_adds()
    pop = population(staged=staged)
    miss = unrowed(text, pop)
    print(f"doc-row gate: population {len(pop)} (added >= {BASELINE_DATE}, PICKED) · "
          f"of which staged-in-THIS-commit {len(staged)} (#207 postscript: the single-commit "
          f"blindspot) · unrowed {len(miss)}")
    for d, p in miss:
        print(f"  ⛔ UNROWED: {p} (added {d}) — invisible to every carry; fix = one _state.add() row")
    if miss:
        print("⛔ FAIL — the forgotten-document class is present.")
        return 1
    print("✅ PASS — every in-scope document has a store row.")
    return 0

def selftest():
    pop = population()
    if not pop:
        print("⛔ SELFTEST BROKEN: empty population — the gate has nothing to see.")
        return 1
    # fail-arm: real pre-row store from git history
    old = _git("show", f"{FAIL_ARM_COMMIT}:knowledge/_state.json")
    miss_old = unrowed(old, pop)
    if not miss_old:
        print(f"⛔ SELFTEST FAIL-ARM: gate saw NOTHING against {FAIL_ARM_COMMIT}'s store — it cannot fail.")
        return 1
    print(f"✅ fail-arm: {len(miss_old)} unrowed against {FAIL_ARM_COMMIT} store: "
          + ", ".join(p for _, p in miss_old))
    # pass-arm: live store (informational; a live flag is a finding, not a selftest fail)
    with open(STORE) as f:
        live = f.read()
    miss_live = unrowed(live, pop)
    print(f"{'⚠ pass-arm: LIVE FINDING — ' + str(len(miss_live)) + ' unrowed now' if miss_live else '✅ pass-arm: live store clean'}")
    # staged-arm (#208): the single-commit blindspot. A doc that exists ONLY in the index
    # must enter the population and be flagged when unrowed. Planted, not staged for real —
    # this arm must never touch the git index. Both directions: absent from the default
    # population, present the moment the staged set names it.
    ghost = "notes/_briefs/9999-99-99-__staged-arm-not-a-real-file.md"
    assert not any(p == ghost for _, p in population(staged=[])), \
        "⛔ STAGED-ARM setup: the ghost doc is somehow already in the committed population"
    from datetime import date as _date
    pop_staged = population(staged=[(_date.today().isoformat(), ghost)])
    if not any(p == ghost for _, p in pop_staged):
        print("⛔ SELFTEST STAGED-ARM: a doc added in the CURRENT commit did not enter the "
              "population — the #207 single-commit blindspot is back.")
        return 1
    if not any(p == ghost for _, p in unrowed(live, pop_staged)):
        print("⛔ SELFTEST STAGED-ARM: the staged doc entered the population but was not "
              "flagged unrowed — the gate sees it and says nothing.")
        return 1
    print(f"✅ staged-arm: a doc present ONLY in the index is seen and flagged "
          f"({len(staged_adds())} real staged add(s) in this tree right now).")
    # mutation-arm: delete one known reference from the live text; gate must flag it.
    # The victim must be a CURRENTLY-ROWED doc: picking pop[-1] blindly could pick an unrowed
    # one (e.g. a staged add), and then the arm passes without deleting anything — vacuous.
    rowed = [p for _, p in pop if not any(p == q for _, q in unrowed(live, pop))]
    if not rowed:
        print("⛔ SELFTEST MUTATION-ARM: no rowed doc to mutate — arm is vacuous, not green.")
        return 1
    # #215: a directory-home-covered doc has NO per-file reference to delete — replace() would
    # be a no-op and the arm vacuous. The victim must be a doc whose own path/basename appears
    # in the store text; the directory clause gets its own arm below.
    per_file_rowed = [p for p in rowed
                      if (p in live or os.path.basename(p) in live)]
    if not per_file_rowed:
        print("⛔ SELFTEST MUTATION-ARM: no per-file-rowed doc to mutate — arm is vacuous, not green.")
        return 1
    victim = per_file_rowed[-1]
    key = victim if victim in live else os.path.basename(victim)
    mutated = live.replace(key, "X" * len(key))
    if not any(p == victim for _, p in unrowed(mutated, pop)):
        print(f"⛔ SELFTEST MUTATION-ARM: reference to {victim} deleted, gate did not flag — matcher is always-true.")
        return 1
    print(f"✅ mutation-arm: deleting the {victim} reference is flagged.")
    # directory-arm (#215, both ways): a doc covered ONLY by a directory home must (a) be
    # covered now, and (b) become UNROWED the moment the directory home is deleted. If no
    # directory home exists in the store, the arm reports itself absent rather than passing.
    dir_homes = [h for h in _homes(live) if h.rstrip().endswith("/")]
    dir_covered = [p for _, p in pop
                   if not (p in live or os.path.basename(p) in live)
                   and any(p.startswith(dh.rstrip()) for dh in dir_homes)]
    if dir_covered:
        dvictim = dir_covered[-1]
        dh = next(h for h in dir_homes if dvictim.startswith(h.rstrip()))
        dmutated = live.replace(dh, "X" * len(dh))
        if any(p == dvictim for _, p in unrowed(live, pop)):
            print(f"⛔ SELFTEST DIRECTORY-ARM: {dvictim} flagged despite a live directory home — clause dead.")
            return 1
        if not any(p == dvictim for _, p in unrowed(dmutated, pop)):
            print(f"⛔ SELFTEST DIRECTORY-ARM: directory home {dh} deleted, {dvictim} not flagged — clause always-true.")
            return 1
        print(f"✅ directory-arm: {dvictim} covered by {dh}; deleting that home is flagged.")
    else:
        print("▫ directory-arm: no directory-home-covered doc in population — arm not exercised (reported, not passed).")
    print("✅ SELFTEST PASS — the green can fail (both non-green arms shown above).")
    return 0

if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
