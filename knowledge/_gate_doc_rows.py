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
import subprocess, sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "knowledge", "_state.json")
BASELINE_DATE = "2026-08-15"  # PICKED, not derived — Dave may rule (see docstring)
PATTERNS = ["notes/_briefs", "_BRIEF-"]
FAIL_ARM_COMMIT = "6b98be3"  # #186 — the offender's pre-row store state

def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout

def population():
    """[(add_date, path)] for tracked brief-class docs added on/after BASELINE_DATE."""
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
    return sorted((d, p) for p, d in first_seen.items() if p in tracked and d >= BASELINE_DATE)

def _homes(store_text):
    import json
    d = json.loads(store_text)
    items = d["items"] if isinstance(d, dict) and "items" in d else d
    return [str(it.get("home", "")) for it in items]

def unrowed(store_text, pop):
    homes = _homes(store_text)
    missing = []
    for d, p in pop:
        base = os.path.basename(p)
        if not any(p in h or base in h for h in homes):
            missing.append((d, p))
    return missing

def check():
    with open(STORE) as f:
        text = f.read()
    pop = population()
    miss = unrowed(text, pop)
    print(f"doc-row gate: population {len(pop)} (added >= {BASELINE_DATE}, PICKED) · unrowed {len(miss)}")
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
    # mutation-arm: delete one known reference from the live text; gate must flag it
    victim = pop[-1][1]
    key = victim if victim in live else os.path.basename(victim)
    mutated = live.replace(key, "X" * len(key))
    if not any(p == victim for _, p in unrowed(mutated, pop)):
        print(f"⛔ SELFTEST MUTATION-ARM: reference to {victim} deleted, gate did not flag — matcher is always-true.")
        return 1
    print(f"✅ mutation-arm: deleting the {victim} reference is flagged.")
    print("✅ SELFTEST PASS — the green can fail (both non-green arms shown above).")
    return 0

if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
