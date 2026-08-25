#!/usr/bin/env python3
"""_gate_doc_rows.py — the new-doc-needs-a-store-row gate (W-20, forgotten-document class #185).

THE CLASS: a document with no `_state.json` row is invisible to every carry — two documents
lived weeks unseen (#185). This gate makes the PRESENCE of a row a checked condition for
new tracked documents, per [[gate-inside-the-growth-loop]]: gate the presence, not the drift.

POPULATION: git-tracked files matching notes/_briefs/*, _BRIEF-* or notes/_subreports/*.md
whose first-add date (git log --diff-filter=A, one pass, no --follow) is >= BASELINE_DATE.

★ #218 — THE GLOB WIDENED TO FILED SUB-REPORTS (`s218-D7`). A filed sub-report is a document in
exactly the sense this gate means: it carries a lane's whole finding set, the conductor cites it
by path, and with no `_state.json` row it is invisible to every carry the moment its window
closes — the #185 class, one level down. So it fails here exactly as a brief does. ONE name is
exempt, `notes/_subreports/_TEMPLATE.md` (EXEMPT_BASENAMES): it is the skeleton, not a report,
and rowing it would teach that a store row is bookkeeping rather than a carry.
⚠ Directory homes still apply (the #215 clause): a single `notes/_subreports/` home in the store
rows every report beneath it. That is the intended shape for a busy conductor window — the row
still carries owner/state/close-condition, and per-report rows remain legal for reports that
need their own close condition.
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
SUBREPORT_DIR = "notes/_subreports"          # ★ #218, `s218-D7` — filed sub-reports
SUBREPORT_EXT = ".md"                        # the glob is `notes/_subreports/*.md`, nothing else
EXEMPT_BASENAMES = {"_TEMPLATE.md"}          # the skeleton is not a report [[gate-glob-scope-rule]]
FAIL_ARM_COMMIT = "6b98be3"  # #186 — the offender's pre-row store state
GIT_PATHSPEC = ("notes/_briefs", "_BRIEF-*", SUBREPORT_DIR)


def in_population(p):
    """Is this repo-relative path a document this gate grades? ONE definition, used by both the
    committed scan and the staged scan — two copies of a membership test drift, and the drift
    would show up as a silently NARROWER population, which is this gate failing open."""
    p = p.strip()
    if not p:
        return False
    base = os.path.basename(p)
    if p.startswith(SUBREPORT_DIR + "/"):
        # the glob is FLAT and `.md` only: assets/ live under this directory and are not documents
        return (base not in EXEMPT_BASENAMES
                and base.endswith(SUBREPORT_EXT)
                and p.count("/") == SUBREPORT_DIR.count("/") + 1)
    return any(p.startswith(t) for t in PATTERNS) or base.startswith("_BRIEF-")

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
                   "--", *GIT_PATHSPEC)
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
               "--", *GIT_PATHSPEC)
    date, first_seen = None, {}
    for line in out.splitlines():
        if line.startswith("C "):
            date = line[2:].strip()
        elif line.strip():
            p = line.strip()
            if in_population(p):
                first_seen[p] = date  # log is newest-first; last write wins = oldest = first add
    tracked = set(_git("ls-files").splitlines())
    pop = {p: d for p, d in first_seen.items() if p in tracked and d >= BASELINE_DATE}
    for d, p in (staged_adds() if staged is None else staged):
        if in_population(p) and d >= BASELINE_DATE:
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
    # ---- SUB-REPORT ARM (★ #218, `s218-D7`), driven BOTH WAYS on the same planted set. The
    # widened glob is worthless if it only ever says yes: the template and the evidence
    # directory must be proven OUT of the population by the same call that proves a report IN
    # [[mutation-tests-the-clause-not-the-feature]].
    from datetime import date as _date2
    _today = _date2.today().isoformat()
    sr = f"{SUBREPORT_DIR}/9999-99-99-000-zz-not-a-real-report.md"
    must_be_out = [
        (f"{SUBREPORT_DIR}/_TEMPLATE.md", "the skeleton — EXEMPT BY NAME"),
        (f"{SUBREPORT_DIR}/assets/9999-99-99-000-zz/screenshot.png", "evidence, not a document"),
        (f"{SUBREPORT_DIR}/assets/9999-99-99-000-zz/notes.md", "an .md UNDER assets/ is evidence"),
        (f"{SUBREPORT_DIR}/README.txt", "not `.md` — the glob is `*.md`"),
    ]
    if not in_population(sr):
        print(f"⛔ SELFTEST SUB-REPORT ARM: {sr} is NOT in the population — the s218-D7 glob "
              f"widening does not bite; a filed report can ship with no store row.")
        return 1
    for path, why in must_be_out:
        if in_population(path):
            print(f"⛔ SELFTEST SUB-REPORT ARM: {path} entered the population ({why}) — the "
                  f"glob is wider than the rule it enforces.")
            return 1
    pop_sr = population(staged=[(_today, sr), (_today, f"{SUBREPORT_DIR}/_TEMPLATE.md")])
    if not any(p == sr for _, p in unrowed(live, pop_sr)):
        print("⛔ SELFTEST SUB-REPORT ARM: a staged filed report was not flagged unrowed — the "
              "gate sees it and says nothing.")
        return 1
    if any(p.endswith("_TEMPLATE.md") for _, p in pop_sr):
        print("⛔ SELFTEST SUB-REPORT ARM: the template reached the population even when staged.")
        return 1
    print(f"✅ sub-report arm: `{SUBREPORT_DIR}/*.md` is graded like a brief; `_TEMPLATE.md`, "
          f"`assets/**` and non-`.md` files are proven OUT (4 negative controls).")
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
