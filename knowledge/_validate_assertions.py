#!/usr/bin/env python3
"""_validate_assertions.py — the VERACITY gate. Re-tests claims that can rot.

Dave 2026-07-18: "how do we fix this permanently?"

THE INCIDENT THAT PROMPTED IT
  A memory file asserted "the sandbox has NO Univers Next for HSBC font" and repeated it in
  five places across sixteen months. The licensed fonts had been sitting in the repo since
  2024-03-25. The claim was TRUE when written and silently became false. Consequences: every
  specimen sheet carried a caveat that was not true, renders were labelled "layout only" when
  they could have shown the real face, and font metrics were treated as unmeasurable when they
  were one os.path.exists() away.

  Same session, the inverse: a BLOCKER saying "Latin webfont missing" was struck as false on the
  strength of finding the *desktop* set — a different licence class. A true claim discarded.
  Both directions end with the record wrong.

THE INSIGHT
  "The sandbox has no Univers" was mechanically checkable the entire time. It did not rot for
  want of thinking; it rotted because a CHECKABLE claim was stored as UNVERIFIABLE PROSE, in a
  place no gate could read, with nothing to re-test it. So:

      Every environment claim that CAN be reduced to a predicate MUST carry one,
      and the predicate gets re-evaluated on every build.

  Rulings, judgements and preferences are NOT in scope — they do not go stale by themselves.
  Facts about the world do.

HOW THIS DIFFERS FROM _validate_standing_instructions.py
  That gate is REFERENTIAL — is every standing doc reachable from the cold-start spine.
  This one is VERACIOUS — is what we say still TRUE. A document can be perfectly reachable
  and perfectly wrong. They are complementary and both are needed.

THE FIELD THAT DOES THE REAL WORK: 'asserted_in'
  When a predicate flips, the gate names EVERY document that now contains a false statement.
  That is precisely what was missing: the "no Univers" claim lived in at least five places and
  nothing connected them, so correcting one would have left four wrong. Fan-out is the failure
  mode; the registry makes fan-out visible.

MEMORY ENTRIES
  Listed as 'memory:<slug>'. The gate cannot READ them — memory lives outside the repo. But it
  CAN name them in the failure output, which converts an invisible dependency into an explicit
  instruction. That is the most this gate can honestly do for the memory side, and pretending
  otherwise would be the same error again.

BLOCKERS GET AN EXPIRY
  A blocker stops work, and therefore stops the work that would disprove it — the highest
  rot-risk claim in the system, and the most expensive when wrong. Past its recheck window the
  gate WARNS even while the predicate still holds, so somebody re-tests it deliberately rather
  than inheriting it.

Usage:  python3 knowledge/_validate_assertions.py
        python3 knowledge/_validate_assertions.py --selftest
Exit non-zero if any assertion's predicate no longer holds. Wired into _build_all.py.
"""
import json, os, sys, glob as globlib
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REGISTRY = os.path.join(HERE, "_assertions.json")
REPORT = os.path.join(HERE, "_ASSERTIONS.md")


# ---------------------------------------------------------------- roots
# A predicate used to assume ROOT — the repo — and so could only ever express
# "present in the repo". Some true, checkable, expensive-to-not-know facts live
# OUTSIDE the repo but INSIDE the sandbox mount: sessions #109/#111/#112 each paid
# 8–9K of fill reading .auto-memory/MEMORY.md into context for a number that
# `bash` produces at zero fill, because nothing said the file was reachable on disk.
#
# So the root is now a NAMED, EXPLICIT part of the predicate record. It is not
# inferred from the glob and it is not silently assumed: an assertion that omits
# it is malformed and the selftest says so. `repo` preserves the old behaviour
# exactly, so no existing assertion changes meaning.
#
# `mount` is resolved by walking up from ROOT for a `.../<session>/mnt` ancestor —
# the sandbox layout. Off-sandbox there is no such ancestor and the root is
# UNRESOLVED, which is reported LOUD and NAMED rather than defaulted to ROOT.
# Defaulting it would make a mount claim quietly re-assert a repo fact — the exact
# class of error this registry exists to stop.

class RootUnresolved(Exception):
    pass


def _mount_root():
    p = ROOT
    while True:
        parent = os.path.dirname(p)
        if parent == p:
            raise RootUnresolved(
                f"root 'mount' unresolvable: no '<session>/mnt' ancestor of ROOT={ROOT} "
                f"(running outside the sandbox mount)")
        if os.path.basename(p) == "mnt":
            return p
        p = parent


ROOTS = {
    "repo": lambda: ROOT,
    "mount": _mount_root,
}
DEFAULT_ROOT = "repo"          # behaviour-preserving for callers that pass no root
ROOT_KEY = "root"


def resolve_root(a):
    """Named root → absolute path. Unknown name fails LOUD and NAMED, never defaults."""
    name = a.get(ROOT_KEY, DEFAULT_ROOT)
    if name not in ROOTS:
        raise RootUnresolved(f"unknown root {name!r} (known: {sorted(ROOTS)})")
    return name, ROOTS[name]()


# ---------------------------------------------------------------- predicates
# Deliberately tiny. No eval, no arbitrary code, no imports from the registry.
# If a claim cannot be expressed here, it either needs a native check (see NATIVE
# below) or it is not an environment claim and does not belong in the registry.

def _matches(a):
    name, base = resolve_root(a)
    return name, base, globlib.glob(os.path.join(base, a["glob"]), recursive=True)


def p_path_exists(a):
    name, _, hits = _matches(a)
    return bool(hits), f"{len(hits)} match(es) in root={name}"


def p_path_absent(a):
    name, base, hits = _matches(a)
    return not hits, (f"{len(hits)} match(es) in root={name}: "
                      f"{[os.path.relpath(h, base) for h in hits[:4]]}"
                      if hits else f"0 matches in root={name}")


def p_glob_count(a):
    name, _, hits = _matches(a)
    n = len(hits)
    op, want = a.get("op", "eq"), a["n"]
    ok = {"eq": n == want, "gte": n >= want, "lte": n <= want}[op]
    return ok, f"count={n} (want {op} {want}) in root={name}"


def _read(a):
    name, base = resolve_root(a)
    path = os.path.join(base, a["path"])
    if not os.path.exists(path):
        return name, None
    return name, open(path, errors="ignore").read()


def p_file_contains(a):
    name, text = _read(a)
    if text is None:
        return False, f"file missing in root={name}: {a['path']}"
    return a["needle"] in text, f"needle={a['needle']!r} in root={name}"


def p_file_lacks(a):
    name, text = _read(a)
    if text is None:
        return False, f"file missing in root={name}: {a['path']}"
    return a["needle"] not in text, f"needle={a['needle']!r} in root={name}"


VERBS = {
    "path_exists": p_path_exists, "path_absent": p_path_absent,
    "glob_count": p_glob_count, "file_contains": p_file_contains,
    "file_lacks": p_file_lacks,
}


# ---------------------------------------------------------------- native checks
# Some claims cannot be expressed as a glob. Rather than grow a predicate language
# into a programming language, those get a named native function here.

def native_composites_unbound():
    """ASSERT-003 — are the type composites bound in any markup?

    The claim "composites are used in ZERO files" is what makes the TYPE-002 retrofit an
    architectural decision rather than a mechanical edit. When this flips, the binding
    mechanism has been chosen and the ledger entry saying otherwise is stale.
    """
    import re
    n = 0
    for pat in ("knowledge/snippets/*.html", "knowledge/_proforma/*.html", "knowledge/canon/canon.css"):
        for f in globlib.glob(os.path.join(ROOT, pat)):
            t = open(f, errors="ignore").read()
            n += len(re.findall(r'class="[^"]*\bt-(?:cm|ed)-', t))
    return n == 0, f"{n} composite class usage(s) in markup"


# ASSERT-003 RETIRED 2026-07-19 — its clears_when ("a binding mechanism is ruled and the first
# composite is bound in markup") was MET: Dave ruled the .num 24 rung; the countdown numeral is now
# bound to .t-cm-figure-3 via a markup class (collision-forced — bare `.num` hits `.cn-table td.num`).
# The BULK binding mechanism for the remaining elements stays open — re-homed in _TYPE-DECISIONS T-D14,
# not guarded by an assertion. `native_composites_unbound` kept as a tombstone; unregistered below.
NATIVE = {}


# ---------------------------------------------------------------- runner
def check(a):
    """Return (ok, detail). Native check wins if one is registered for this id."""
    if a["id"] in NATIVE:
        return NATIVE[a["id"]]()
    pred = a["predicate"]
    verb = VERBS.get(pred["verb"])
    if not verb:
        return False, f"unknown predicate verb {pred['verb']!r}"
    try:
        return verb(pred)
    except RootUnresolved as e:
        # LOUD and NAMED. A root we cannot resolve is NOT a pass and NOT silently
        # re-pointed at ROOT — the assertion is simply not testable here, and says so.
        return False, f"ROOT UNRESOLVED — {e}"


def stale_blocker(a):
    """A blocker past its recheck window: WARN even when the predicate still holds."""
    if a.get("kind") != "blocker" or "recheck_days" not in a:
        return None
    try:
        last = datetime.strptime(a["last_verified"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return "no parsable last_verified"
    age = (date.today() - last).days
    if age > a["recheck_days"]:
        return f"last verified {age}d ago, window is {a['recheck_days']}d"
    return None


def run():
    reg = json.load(open(REGISTRY))
    assertions = reg["assertions"]
    fails, warns, lines = [], [], []
    lines.append("# Assertion register — veracity report\n")
    lines.append("*GENERATED by `_validate_assertions.py` on every build — do not hand-edit.*\n")
    lines.append("*Environment claims that can rot, each re-tested against reality. "
                 "Judgement and rulings are deliberately out of scope.*\n")

    for a in assertions:
        ok, detail = check(a)
        warn = stale_blocker(a)
        mark = "✓" if ok else "✗"
        print(f"  [{mark}] {a['id']} {a['kind']:<12} {detail}")
        if not ok:
            fails.append((a, detail))
        if warn:
            warns.append((a, warn))
            print(f"      ⚠ {warn}")

        lines.append(f"\n## {mark} {a['id']} — {a['kind']}\n")
        lines.append(f"**Claim:** {a['claim']}\n")
        lines.append(f"- check: `{detail}`")
        if a.get("consequence"):
            lines.append(f"- consequence: {a['consequence']}")
        if a.get("clears_when"):
            lines.append(f"- clears when: {a['clears_when']}")
        lines.append(f"- asserted in: {', '.join('`%s`' % s for s in a['asserted_in'])}")
        lines.append(f"- last verified: {a['last_verified']}")
        if warn:
            lines.append(f"- ⚠ **STALE:** {warn}")

    if fails:
        print("\n" + "=" * 72)
        print("ASSERTION FAILURE — the world changed and these documents now disagree with it.")
        print("=" * 72)
        for a, detail in fails:
            print(f"\n  {a['id']}: {a['claim']}")
            print(f"    reality: {detail}")
            print(f"    ⇒ CORRECT THESE, all of them — a claim fixed in one place and left in")
            print(f"      four others is how the original rot happened:")
            for src in a["asserted_in"]:
                tag = "  (MEMORY — outside the repo, no gate can reach it; fix by hand)" \
                    if src.startswith("memory:") else ""
                print(f"        · {src}{tag}")

    if warns:
        print(f"\n  ⚠ {len(warns)} blocker(s) past their recheck window — re-test deliberately:")
        for a, w in warns:
            print(f"      {a['id']}: {w}")
            print(f"        clears when: {a.get('clears_when', '—')}")

    open(REPORT, "w").write("\n".join(lines) + "\n")

    if fails:
        print(f"\nASSERTION GATE FAIL — {len(fails)} of {len(assertions)} claim(s) no longer true.")
        return 1
    print(f"\n✅ assertion gate passed — {len(assertions)} claim(s) still true"
          + (f", {len(warns)} stale warning(s)." if warns else "."))
    return 0


def wellformed(a):
    """Registry well-formedness. Raises AssertionError, named, on the offending id."""
    assert a["asserted_in"], f"{a['id']} must declare where it is asserted — that field IS the fix"
    assert a["predicate"]["verb"] in VERBS or a["id"] in NATIVE, f"{a['id']} bad verb"
    assert ROOT_KEY in a["predicate"], (
        f"{a['id']} predicate must declare its root EXPLICITLY — an assumed root is how a "
        f"mount claim silently becomes a repo claim")
    # .get, not [] — if the clause above is ever weakened this must still fail NAMED, not crash.
    assert a["predicate"].get(ROOT_KEY) in ROOTS, \
        f"{a['id']} unknown root {a['predicate'].get(ROOT_KEY)!r} (known: {sorted(ROOTS)})"
    assert a.get("kind") != "blocker" or "recheck_days" in a, \
        f"{a['id']} is a blocker and must carry recheck_days"
    return True


def selftest():
    """Bite-test every verb. A gate that cannot fail is worse than no gate — it
    manufactures confidence. (Lesson from the type gate that reported clean on the
    very badge that motivated it, 2026-07-18.)"""
    ok, _ = p_path_exists({"glob": "knowledge/_assertions.json"})
    assert ok, "path_exists must find a file that is there"
    ok, _ = p_path_exists({"glob": "knowledge/__nope__/*.xyz"})
    assert not ok, "path_exists must fail on a missing file"

    # --- explicit root, both directions -------------------------------------
    ok, d = p_path_exists({"root": "repo", "glob": "knowledge/_assertions.json"})
    assert ok and "root=repo" in d, "explicit root=repo must behave exactly as the old default"
    try:
        mnt = _mount_root()
    except RootUnresolved:
        mnt = None
    if mnt:
        # HIT: a file that exists in the mount but NOT in the repo.
        ok, d = p_path_exists({"root": "mount", "glob": ".auto-memory/MEMORY.md"})
        assert ok and "root=mount" in d, f"root=mount must reach outside the repo — got {d}"
        # MISS: same glob under the repo root finds nothing — the roots are distinct.
        ok, _ = p_path_exists({"root": "repo", "glob": ".auto-memory/MEMORY.md"})
        assert not ok, "the mount file must NOT be reachable from root=repo (roots must differ)"
    ok, d = p_path_exists({"root": "repo", "glob": "knowledge/__nope__/*.xyz"})
    assert not ok, "explicit root must still miss a missing file"
    ok, _ = p_path_absent({"glob": "knowledge/__nope__/*.xyz"})
    assert ok, "path_absent must pass when nothing matches"
    ok, _ = p_path_absent({"glob": "knowledge/_assertions.json"})
    assert not ok, "path_absent must FAIL when the thing exists — the Univers case"
    ok, _ = p_file_contains({"path": ".gitignore", "needle": "knowledge/assets/fonts/"})
    assert ok, "file_contains must find a present needle"
    ok, _ = p_file_lacks({"path": ".gitignore", "needle": "zzz-not-present-zzz"})
    assert ok, "file_lacks must pass on an absent needle"
    ok, _ = p_glob_count({"glob": "knowledge/_validate_*.py", "op": "gte", "n": 1})
    assert ok, "glob_count gte must work"
    reg = json.load(open(REGISTRY))
    ids = [a["id"] for a in reg["assertions"]]
    assert len(ids) == len(set(ids)), "assertion ids must be unique"
    for a in reg["assertions"]:
        wellformed(a)
    mutation_tests()
    print(f"selftest OK — {len(VERBS)} verbs bite-tested, {len(NATIVE)} native check(s), "
          f"{len(ids)} assertion(s) well-formed, 3 mutation(s) killed.")
    return 0


def mutation_tests():
    """Each mutation re-enacts a WRONG version of one clause and asserts a check dies.
    A mutation proves the CLAUSE it kills — not the feature. Named accordingly."""

    # M1 — kills the clause "root 'mount' resolves to the MOUNT, not to ROOT".
    # This is the literal old behaviour (predicates assumed ROOT). If the mount root
    # were still ROOT, the mount-reachability assertion would read as FALSE.
    if _mount_root_or_none():
        orig = ROOTS["mount"]
        ROOTS["mount"] = lambda: ROOT
        try:
            ok, _ = p_path_exists({"root": "mount", "glob": ".auto-memory/MEMORY.md"})
            assert not ok, "M1 did not kill: assumed-ROOT mount still found the mount file"
        finally:
            ROOTS["mount"] = orig
        ok, _ = p_path_exists({"root": "mount", "glob": ".auto-memory/MEMORY.md"})
        assert ok, "M1 restore failed — mount root not put back"

    # M2 — kills the clause "an UNKNOWN root fails LOUD and NAMED, never defaults to repo".
    # Mutant premise: a bogus root silently falls back to ROOT and the check passes.
    ok, detail = check({"id": "MUT-002", "predicate":
                        {"verb": "path_exists", "root": "no-such-root",
                         "glob": "knowledge/_assertions.json"}})
    assert not ok, "M2 did not kill: an unknown root defaulted instead of failing"
    assert "ROOT UNRESOLVED" in detail and "no-such-root" in detail, \
        f"M2 did not kill: failure is not NAMED — {detail!r}"

    # M3 — kills the clause "every registry predicate declares its root EXPLICITLY".
    # Mutant: a rootless assertion record. The well-formedness clause must reject it.
    bad = {"id": "MUT-003", "kind": "environment", "asserted_in": ["mutation"],
           "predicate": {"verb": "path_exists", "glob": "x"}}
    killed = False
    try:
        wellformed(bad)
    except AssertionError as e:
        killed = "EXPLICITLY" in str(e)
    assert killed, "M3 did not kill: wellformed() accepted a rootless predicate"


def _mount_root_or_none():
    try:
        return _mount_root()
    except RootUnresolved:
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    rc = selftest()
    sys.exit(run() or rc)
