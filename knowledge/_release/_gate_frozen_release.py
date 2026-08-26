#!/usr/bin/env python3
"""_gate_frozen_release.py — s114-D4 ENFORCED BY MACHINE: a shipped release is FROZEN.

★ WHY THIS EXISTS. `s114-D4` has been the rule since #114 and `s219-D4(5)` restates it for v3:
a released pack is frozen; you do not edit a release, you cut a new one. Until now NOTHING
checked it. The rule lived in prose, in a memory hook, and in the habit of whoever happened to
be reading — which is the [[instrument-without-a-consumer]] shape inverted: a rule with no gate.
The failure it prevents is quiet and permanent: someone "fixes" a typo inside
`designer-skills-v2/`, the zip a designer downloaded last month and the folder in the repo now
disagree, and there is no version anywhere that says which one they hold.

WHAT IS FROZEN, AND HOW IT IS RECORDED. `_frozen-releases.json` is a LEDGER, one row per
release. Each row names the release's SURFACE (path prefixes), the COMMIT the surface was
recorded at, the file count, and a CONTENT HASH — sha256 over `path <blob-sha>` lines, sorted.
The ledger is SEEDED BY MEASUREMENT (`--seed`), never typed: a hand-typed hash is a claim about
the tree that nothing re-measures, which is the exact defect v3's generated manifest exists to
end [[measure-dont-convert-units]].

THE THREE ARMS, and each one can fail on its own:

  1. THE SURFACE ARM (blocking). Measure each release's surface at the commit under test and
     compare to the recorded hash. Different ⇒ RED, with every changed / added / removed path
     NAMED (a gate must quote what it forbids). This is the arm that catches the typo-fix.

  2. THE WORKING-TREE ARM (blocking). `git status --porcelain` over the same prefixes, untracked
     files included. It catches the same edit ONE STEP EARLIER — before the commit exists — and
     it is why an untracked zip appearing in a frozen `dist/` is reported rather than ignored.

  3. THE LAUNDERING ARM (blocking, and the reason the ledger is not a rubber stamp). A ledger
     you can re-seed at will is not a freeze: you edit v2, re-run `--seed`, and the surface arm
     goes green again having recorded the edit as the new truth. So this arm reads the ledger AT
     THE PARENT COMMIT and compares row by row. If a row's `content_sha256` or `baseline_commit`
     MOVED while its `version` STAYED THE SAME, that is a re-record without a bump ⇒ RED.
     Moving a frozen surface is legal — it is what cutting v3.0.1 means — but it must be spelled
     as a version, which is `s114-D4`'s whole point: *explicit, versioned, Dave's word*.

⛔ WHAT THIS GATE DOES NOT DECIDE. Whether a release SHOULD be cut, and what version it carries,
is Dave's word (`s219-D4(2)`). This gate only refuses to let the question go unasked. It has no
opinion about the contents of a pack, only about whether a frozen one moved in silence.

COULD-NOT-ASK (`knowledge/_could_not_ask.py`, exit 77): the laundering arm needs the parent
commit's ledger blob, which a shallow clone cannot reach and which does not exist on the commit
that first lands the ledger. That is a refusal, not a verdict, and it is keyed on the UNREACHABLE
INPUT — never on "am I in CI" [[gate-cannot-pass-in-one-environment]]. A refusal never masks a
real red: if any arm finds a violation the exit is 1, refusals or not.

Usage:
    python3 knowledge/_release/_gate_frozen_release.py               # HEAD + working tree
    python3 knowledge/_release/_gate_frozen_release.py --at <rev>    # a named commit
    python3 knowledge/_release/_gate_frozen_release.py --no-worktree # commit arm only (CI)
    python3 knowledge/_release/_gate_frozen_release.py --seed        # RE-RECORD (see below)
    python3 knowledge/_release/_gate_frozen_release.py --selftest

  ⚠ `--seed` REWRITES the ledger from measurement. Run it when a release is deliberately cut or
  re-cut, and bump that row's `version` in the same edit — arm 3 exists to catch the case where
  you did not.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile

import _could_not_ask as cna

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))
LEDGER_REL = "knowledge/_release/_frozen-releases.json"

# The surfaces, and the ONE place they are declared. A release's surface is a set of path
# prefixes, because "the release" is not always a whole directory: v3's frozen surface is the
# BAKED ZIP, not the build script and not the skills — those are the machinery that makes the
# next release, and freezing them would freeze the next cut before it was made.
SURFACES = [
    ("designer-skills-v1", ["designer-skills-v1/"], "v1",
     "The first designer pack. Hand-cut, superseded, kept for history."),
    ("designer-skills-v2", ["designer-skills-v2/"], "v2",
     "The shipped v2 pack, baked from 7071538. s219-D4(1) copies its four SKILL.md FORWARD for "
     "refresh — copying out is reading, and reading is not a change."),
    ("designer-skills-v3", ["designer-skills-v3/dist/"], "v3.0.0",
     "v3's frozen surface is the BAKED ZIP in dist/, nothing else. build-designer-pack.sh, "
     "ci-template/ and skills/ are the machinery that cuts the release and stay editable."),
]


# ---------------------------------------------------------------------------------------------
# git plumbing — non-raising, because reachability is a QUESTION here, not an assumption
# ---------------------------------------------------------------------------------------------

def git(root, *args):
    r = subprocess.run(["git"] + list(args), cwd=root, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def rev_ok(root, rev):
    rc, out, _ = git(root, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    return out.strip() if rc == 0 else ""


def surface_at(root, rev, prefixes):
    """path -> blob sha for every TRACKED file under the prefixes, at a named commit."""
    out = {}
    for pfx in prefixes:
        rc, txt, err = git(root, "ls-tree", "-r", rev, "--", pfx)
        if rc != 0:
            raise RuntimeError("git ls-tree failed for %s: %s" % (pfx, err.strip()[:200]))
        for line in txt.splitlines():
            if not line.strip():
                continue
            meta, path = line.split("\t", 1)
            _mode, kind, sha = meta.split()
            if kind == "blob":
                out[path] = sha
    return out


def content_sha(surface):
    """sha256 over `path <blob>` lines, sorted. A hash of WHAT IS THERE, not of when."""
    body = "\n".join("%s %s" % (p, surface[p]) for p in sorted(surface))
    return hashlib.sha256(body.encode()).hexdigest()


def blob_at(root, rev, path):
    rc, txt, _ = git(root, "show", "%s:%s" % (rev, path))
    return txt if rc == 0 else None


# ---------------------------------------------------------------------------------------------
# the ledger
# ---------------------------------------------------------------------------------------------

def ledger_path(root):
    return os.path.join(root, LEDGER_REL)


def read_ledger(root):
    p = ledger_path(root)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def seed(root, rev):
    """Measure every surface at `rev` and WRITE the ledger. Measurement, never a claim."""
    sha = rev_ok(root, rev)
    if not sha:
        raise RuntimeError("'%s' is not a commit in %s" % (rev, root))
    rows = []
    for rid, prefixes, version, note in SURFACES:
        surf = surface_at(root, sha, prefixes)
        rows.append(dict(id=rid, version=version, surface=list(prefixes),
                         baseline_commit=sha, files=len(surf),
                         content_sha256=content_sha(surf), note=note))
    doc = {
        "_README": ("FROZEN-RELEASE LEDGER (s114-D4, s219-D4(5)). One row per shipped release. "
                    "Every field here is MEASURED by knowledge/_release/_gate_frozen_release.py "
                    "--seed — never hand-typed. Editing a frozen surface means cutting a NEW "
                    "release: change the files, re-seed, and BUMP that row's `version` in the "
                    "same commit. Re-seeding without a bump is caught by the gate's laundering "
                    "arm, which reads this file at the parent commit."),
        "schema": "apollo-frozen-releases/1",
        "seeded_at": sha,
        "releases": rows,
    }
    text = json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    with open(ledger_path(root), "w", encoding="utf-8") as f:
        f.write(text)
    return doc


# ---------------------------------------------------------------------------------------------
# the three arms
# ---------------------------------------------------------------------------------------------

def arm_surface(root, rev, led):
    """Recorded hash vs measured hash, with every differing path NAMED."""
    fails = []
    for row in led["releases"]:
        surf = surface_at(root, rev, row["surface"])
        got = content_sha(surf)
        if got == row["content_sha256"]:
            continue
        base = row.get("baseline_commit", "")
        detail = ""
        if base and rev_ok(root, base):
            was = surface_at(root, base, row["surface"])
            changed = sorted(p for p in set(was) & set(surf) if was[p] != surf[p])
            added = sorted(set(surf) - set(was))
            removed = sorted(set(was) - set(surf))
            bits = []
            if changed:
                bits.append("%d CHANGED: %s" % (len(changed), ", ".join(changed[:5])))
            if added:
                bits.append("%d ADDED: %s" % (len(added), ", ".join(added[:5])))
            if removed:
                bits.append("%d REMOVED: %s" % (len(removed), ", ".join(removed[:5])))
            detail = " — " + "; ".join(bits) if bits else ""
        fails.append("FROZEN RELEASE MOVED: %s (version %s) no longer matches the ledger "
                     "(recorded %s, measured %s)%s"
                     % (row["id"], row.get("version", "?"),
                        row["content_sha256"][:12], got[:12], detail))
    return fails


def arm_worktree(root, led):
    """The same edit, caught one step earlier — before it is a commit."""
    fails = []
    for row in led["releases"]:
        rc, txt, err = git(root, "status", "--porcelain", "--untracked-files=all", "--",
                           *row["surface"])
        if rc != 0:
            continue
        lines = [l for l in txt.splitlines() if l.strip()]
        if lines:
            fails.append("FROZEN RELEASE DIRTY IN THE WORKING TREE: %s — %d path(s): %s"
                         % (row["id"], len(lines), "; ".join(l.strip() for l in lines[:5])))
    return fails


def arm_laundering(root, rev, led):
    """A re-record without a version bump. Returns (fails, refusal_reason_or_None)."""
    parent = rev_ok(root, rev + "^")
    if not parent:
        return [], ("the parent of %s is not reachable in this checkout, so the ledger's "
                    "previous state cannot be read" % rev[:12])
    prev_text = blob_at(root, parent, LEDGER_REL)
    if prev_text is None:
        return [], ("%s does not exist at %s — this commit is where the ledger lands, so there "
                    "is no previous recording to compare against" % (LEDGER_REL, parent[:12]))
    try:
        prev = json.loads(prev_text)
    except ValueError as e:
        return ["the ledger at %s is not valid JSON (%s) — a corrupt baseline cannot certify "
                "anything" % (parent[:12], e.__class__.__name__)], None
    was = {r["id"]: r for r in prev.get("releases", [])}
    fails = []
    for row in led["releases"]:
        old = was.get(row["id"])
        if not old:
            continue
        moved = (old.get("content_sha256") != row.get("content_sha256")
                 or old.get("baseline_commit") != row.get("baseline_commit"))
        if moved and old.get("version") == row.get("version"):
            fails.append("RE-RECORDED WITHOUT A VERSION BUMP: %s still says version %s, but its "
                         "recording moved (%s -> %s). s114-D4: a release is explicit and "
                         "VERSIONED — re-seeding the ledger is not a substitute for cutting a "
                         "new version."
                         % (row["id"], row.get("version", "?"),
                            (old.get("content_sha256") or "?")[:12],
                            (row.get("content_sha256") or "?")[:12]))
    return fails, None


def check(root, rev, worktree=True, quiet=False):
    """Returns an exit code: 0 green, 1 a real violation, 77 nothing could be asked."""
    def say(*a):
        if not quiet:
            print(*a)

    led = read_ledger(root)
    if led is None:
        return cna.refuse(LEDGER_REL,
                          "there is no frozen-release ledger at %s, so there is nothing "
                          "recorded to compare a surface against. Seed it: python3 "
                          "knowledge/_release/_gate_frozen_release.py --seed" % LEDGER_REL)
    sha = rev_ok(root, rev)
    if not sha:
        return cna.refuse(rev, "'%s' is not a commit reachable in this checkout" % rev)

    fails = list(arm_surface(root, sha, led))
    asked = 1
    if worktree:
        fails += arm_worktree(root, led)
        asked += 1
    lfails, refusal = arm_laundering(root, sha, led)
    fails += lfails
    if refusal is None:
        asked += 1

    say("frozen-release gate — %d release(s) at %s" % (len(led["releases"]), sha[:12]))
    for row in led["releases"]:
        say("  %-20s version %-8s %4d file(s)  %s"
            % (row["id"], row.get("version", "?"), row.get("files", 0),
               row["content_sha256"][:12]))
    if refusal is not None:
        say("  " + cna.MARKER + " laundering arm: " + refusal)

    if fails:
        say("\n%d FROZEN-RELEASE VIOLATION(S):" % len(fails))
        for f in fails:
            say("  ❌ " + f)
        return 1
    if asked == 0:
        return cna.refuse("frozen releases", "no arm could be asked")
    say("\nPASS — %d arm(s) asked, no frozen surface moved." % asked)
    return 0


# ---------------------------------------------------------------------------------------------
# selftest — driven on a FIXTURE REPO, never on Dave's index
# ---------------------------------------------------------------------------------------------

def _fixture(tmp):
    """A tiny real git repo with the same shape: a frozen v2 surface and a ledger."""
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "designer-skills-v2"))
    os.makedirs(os.path.join(root, "knowledge", "_release"))
    for a in (["init", "-q", "-b", "main"], ["config", "user.email", "f@x"],
              ["config", "user.name", "fixture"]):
        git(root, *a)
    with open(os.path.join(root, "designer-skills-v2", "README.md"), "w") as f:
        f.write("v2 pack, shipped and frozen\n")
    with open(os.path.join(root, "designer-skills-v2", "SKILL.md"), "w") as f:
        f.write("# a skill\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "v2")
    return root


def _run(root, *args):
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--root", root] + list(args),
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def selftest():
    fails, n = [], [0]

    def bite(name, ok, why=""):
        n[0] += 1
        if not ok:
            fails.append("[%s] %s" % (name, why))

    # ---- pure-function arms
    bite("content_sha/stable", content_sha({"a": "1", "b": "2"}) == content_sha({"b": "2", "a": "1"}),
         "the hash must not depend on dict order")
    bite("content_sha/bites", content_sha({"a": "1"}) != content_sha({"a": "2"}),
         "a changed blob must change the hash")
    bite("content_sha/notices-a-new-file", content_sha({"a": "1"}) != content_sha({"a": "1", "b": "2"}),
         "an ADDED file must change the hash")

    tmp = tempfile.mkdtemp(prefix="frozen-gate-selftest-")
    try:
        root = _fixture(tmp)
        # the gate needs its own file reachable from the fixture; --root only redirects the tree
        rc, out = _run(root, "--seed")
        bite("seed/writes-a-ledger", rc == 0 and os.path.exists(ledger_path(root)), out[-300:])
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "ledger")

        rc, out = _run(root)
        bite("clean/green", rc == 0, "a freshly seeded, untouched tree must be green: " + out[-300:])

        # ---- ARM 1 + 2: an edit to a v2 tracked file must go RED BY NAME
        p = os.path.join(root, "designer-skills-v2", "README.md")
        with open(p, "a") as f:
            f.write("one more line\n")
        rc, out = _run(root)
        bite("worktree/bites", rc == 1 and "designer-skills-v2/README.md" in out,
             "an uncommitted edit to a frozen file must be RED by name: " + out[-400:])
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "sneaky typo fix")
        rc, out = _run(root, "--no-worktree")
        bite("surface/bites", rc == 1 and "designer-skills-v2/README.md" in out,
             "a COMMITTED edit to a frozen file must be RED by name: " + out[-400:])
        bite("surface/says-moved", "FROZEN RELEASE MOVED" in out, out[-300:])

        # ---- ARM 3: re-seeding without a bump launders the edit — and must not
        rc, out = _run(root, "--seed")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "re-seed, no bump")
        rc, out = _run(root, "--no-worktree")
        bite("laundering/bites", rc == 1 and "WITHOUT A VERSION BUMP" in out,
             "re-seeding a moved surface without bumping the version must stay RED: " + out[-400:])

        # ---- the escape hatch WORKS: same move, version bumped, green
        led = read_ledger(root)
        for row in led["releases"]:
            if row["id"] == "designer-skills-v2":
                row["version"] = "v2.0.1"
        with open(ledger_path(root), "w") as f:
            f.write(json.dumps(led, indent=2, sort_keys=True) + "\n")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "cut v2.0.1")
        rc, out = _run(root, "--no-worktree")
        bite("bump/green", rc == 0,
             "a declared version bump is the legal way to move a frozen surface: " + out[-400:])

        # ---- a ledger that is not there is a REFUSAL, not a pass
        os.remove(ledger_path(root))
        rc, out = _run(root, "--no-worktree")
        bite("no-ledger/refuses", rc == cna.EXIT and cna.MARKER in out,
             "a missing ledger must refuse (77), never read as green: " + out[-300:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("selftest: %d bites, %d fail(s)" % (n[0], len(fails)))
    for f in fails:
        print("  RED " + f)
    return not fails


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    # `--check` is the surveyable spelling of the default run. `_build_survey.py` only RUNS a
    # step whose every argument is in its NON_MUTATING set (`--check` / `--selftest`) — a step
    # with no arguments at all is treated as mutating and merely listed. This gate writes
    # nothing, so it should be asked by the survey, and that means it has to say `--check`.
    ap.add_argument("--check", action="store_true", help="run the check (the default)")
    ap.add_argument("--at", default="HEAD", help="the commit to check (default HEAD)")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="repo root (the selftest's fixture)")
    ap.add_argument("--no-worktree", action="store_true",
                    help="commit arm only — the working tree is not asked")
    ap.add_argument("--seed", action="store_true", help="RE-RECORD the ledger from measurement")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if a.seed:
        doc = seed(a.root, a.at)
        print("seeded %s at %s" % (LEDGER_REL, doc["seeded_at"][:12]))
        for row in doc["releases"]:
            print("  %-20s version %-8s %4d file(s)  %s"
                  % (row["id"], row["version"], row["files"], row["content_sha256"][:12]))
        print("\n⚠ If a frozen surface MOVED, bump that row's `version` in this same commit — "
              "the laundering arm is what checks you did.")
        return
    sys.exit(check(a.root, a.at, worktree=not a.no_worktree))


if __name__ == "__main__":
    main()
