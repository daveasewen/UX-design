#!/usr/bin/env python3
"""_gate_release_audit.py — is the PACK SHIP LIST still a function of the tree, and does the
baked pack still match it?

★ THE DEFECT CLASS THIS EXISTS FOR, in the repo's own words. v2 shipped from a hand-written
copy-list, and its receipt records what that cost: *"v1's copy-list had gone stale — never
shipped canon/type.css nor tokens/themes/"*. A copy-list is a claim about the tree that nothing
re-measures. Apollo — Spider replaced it with a GENERATED manifest — and a generated file is only better than
a typed one while something re-generates it and compares. That is this gate.

THREE QUESTIONS, THREE POSTURES, and the split is the house rule: a MECHANICAL determinism check
BLOCKS; anything PROMOTION-FLAVOURED advises, because promotion is Dave's word (s219-D4(2)).

  --manifest-check   BLOCKING. Rebuild the manifest from the generator at the manifest's OWN
                     recorded commit, using the stored gate probe, and compare BYTE FOR BYTE.
                     Different ⇒ the ship list on disk is not what the generator produces, which
                     means it was hand-edited or the generator moved underneath it. One command
                     fixes it and the remedy says so. This asks nothing about whether the cut is
                     RIGHT — only whether the file is what it claims to be.

  --pack             BLOCKING, with a REFUSAL as its resting state. If a zip exists in
                     apollo-spider/dist/, its contents are checked against the manifest and
                     against the commit's own blobs (the generator's `check_pack`). If NO zip
                     exists, that is not a failure and not a pass: it is COULD-NOT-ASK (77) —
                     nothing is baked because the release is Dave's word and the manifest still
                     reads PROPOSED. The survey counts a 77 as a third verdict and excludes it
                     from its exit code, so this gate can be BLOCKING today without being born
                     red [[gate-cannot-pass-in-one-environment]].

  --drift            ADVISORY. The manifest is a function of a NAMED COMMIT. As the repo moves,
                     the ship list ages: a release cut from an old commit ships old content.
                     That is a real fact and it is NOT a defect — cutting a release from an older
                     commit is a legitimate choice, and WHEN to re-cut is ⬛ DAVE'S (s219-D4(2)).
                     So this arm reports the distance and never gates a push. It exits non-zero
                     when the manifest is behind, in the house's advisory shape: routed ADVISORY
                     in `_build_all.py`, `continue-on-error: true` in CI.

⛔ WHAT THIS GATE MUST NEVER DO: decide that a pack should be released, or promote the manifest's
status. `status: PROPOSED -> RATIFIED` is Dave's word and the build script already refuses to
bake without it. This gate only measures.

Usage:
    python3 knowledge/_release/_gate_release_audit.py --manifest-check
    python3 knowledge/_release/_gate_release_audit.py --pack
    python3 knowledge/_release/_gate_release_audit.py --drift
    python3 knowledge/_release/_gate_release_audit.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse, glob, json, os, subprocess, sys

import _could_not_ask as cna

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _gen_pack_manifest as gen  # noqa: E402 — the generator IS the reference implementation

ROOT = gen.ROOT
DIST = os.path.join(ROOT, "apollo-spider", "dist")
REMEDY = ("python3 knowledge/_release/_gen_pack_manifest.py --probe --commit <sha> && "
          "python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit <sha>")


def _load_manifest():
    if not os.path.exists(gen.MANIFEST_PATH):
        return None, cna.refuse("the pack manifest",
                                "there is no manifest at %s — nothing has been proposed yet. "
                                "Generate it: %s" % (gen.MANIFEST_PATH, REMEDY))
    with open(gen.MANIFEST_PATH, encoding="utf-8") as f:
        return f.read(), None


def manifest_check():
    """BLOCKING. The manifest on disk vs a fresh generation at its own recorded commit."""
    text, refusal = _load_manifest()
    if refusal is not None:
        return refusal
    man = json.loads(text)
    sha = man.get("commit", "")

    r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", sha + "^{commit}"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return cna.refuse("the pack manifest",
                          "the manifest names commit %s, which is not reachable in this "
                          "checkout — a fresh generation cannot be made to compare against. "
                          "(A shallow clone or a rewritten history does this; it is not a "
                          "verdict about the manifest.)" % sha[:12])
    if not os.path.exists(gen.PROBE_PATH):
        return cna.refuse("the pack manifest",
                          "the gate probe at %s is missing, and the manifest's gate verdicts "
                          "are MEASURED from it — regenerating without it would guess. Run the "
                          "probe: %s" % (gen.PROBE_PATH, REMEDY))
    probe = json.load(open(gen.PROBE_PATH, encoding="utf-8"))
    if probe.get("commit") != sha:
        print("❌ the gate probe was run at %s but the manifest is for %s — one of them is "
              "stale. Re-run both: %s" % ((probe.get("commit") or "?")[:12], sha[:12], REMEDY))
        return 1

    fresh = gen.canonical(gen.build_manifest(sha, probe))
    if fresh == text:
        print("PASS — the manifest at %s is byte-identical to a fresh generation at %s "
              "(%d files, sha256 %s)"
              % (os.path.relpath(gen.MANIFEST_PATH, ROOT), sha[:12],
                 man["totals"]["files"], gen.manifest_hash(text)[:16]))
        return 0

    # Name WHAT differs, not just THAT it differs — a diff of two 1,500-path JSON files is not
    # a remedy [[gate-must-quote-what-it-forbids]].
    now, was = json.loads(fresh), man
    gone = sorted(set(gen.all_paths(was)) - set(gen.all_paths(now)))
    new = sorted(set(gen.all_paths(now)) - set(gen.all_paths(was)))
    kw = {g["key"] for g in was["groups"]}
    kn = {g["key"] for g in now["groups"]}
    print("❌ THE SHIP LIST ON DISK IS NOT WHAT THE GENERATOR PRODUCES at %s." % sha[:12])
    print("   on disk: %d files, sha256 %s" % (was["totals"]["files"], gen.manifest_hash(text)[:16]))
    print("   fresh:   %d files, sha256 %s" % (now["totals"]["files"], gen.manifest_hash(fresh)[:16]))
    if kn - kw:
        print("   GROUPS the generator now declares that the file does not: %s" % sorted(kn - kw))
    if kw - kn:
        print("   GROUPS in the file that the generator no longer declares: %s" % sorted(kw - kn))
    if new:
        print("   %d path(s) a fresh generation SHIPS that the file does not, first: %s"
              % (len(new), new[:5]))
    if gone:
        print("   %d path(s) the file ships that a fresh generation does not, first: %s"
              % (len(gone), gone[:5]))
    print("   REMEDY: regenerate — never hand-edit the manifest. %s" % REMEDY)
    return 1


def packs():
    return sorted(glob.glob(os.path.join(DIST, "Apollo-Spider-v*.zip")))


def pack_check():
    """BLOCKING when a pack exists; a REFUSAL when none does (the release is Dave's word)."""
    text, refusal = _load_manifest()
    if refusal is not None:
        return refusal
    man = json.loads(text)
    zips = packs()
    if not zips:
        return cna.refuse(
            "the baked pack",
            "there is no zip in apollo-spider/dist/, so there is no pack to audit. That is "
            "the expected resting state: the manifest reads %r and s219-D4(2) makes the release "
            "Dave's word, not this gate's. The moment a pack is baked this check starts biting."
            % str(man.get("status", ""))[:40])
    sha = man["commit"]
    # ⛔ #220 (first two-release day): the manifest is a LIVE fact and speaks for exactly ONE
    # version — man["version"]. Auditing an OLDER frozen zip against the CURRENT manifest is a
    # category error that made this arm structurally red the moment a second release existed
    # (v1.0.0 can never match v1.0.1's manifest — 33 named "missing" paths that were never in
    # its cut). Older zips are FROZEN HISTORY under _gate_frozen_release.py's jurisdiction
    # (content_sha256 in the ledger); this arm now names them SKIPPED rather than failing them.
    want = str(man.get("version", "")).strip()
    current = [z for z in zips
               if os.path.basename(z) == "Apollo-Spider-%s.zip" % want]
    if not current:
        print("❌ the manifest reads version %r and NO zip in dist/ carries it "
              "(zips present: %s) — the manifest names a release nobody baked."
              % (want, ", ".join(os.path.basename(z) for z in zips)))
        return 1
    bad = 0
    for z in zips:
        if z not in current:
            print("SKIPPED — %s is FROZEN HISTORY (not the manifest's %s); its integrity is "
                  "_gate_frozen_release.py's jurisdiction, not this arm's"
                  % (os.path.relpath(z, ROOT), want))
            continue
        fails = gen.check_pack(z, man, sha)
        if fails:
            bad += 1
            print("❌ %s does NOT match the manifest at %s:" % (os.path.relpath(z, ROOT), sha[:12]))
            for f in fails:
                print("   " + f)
        else:
            print("PASS — %s matches the manifest at %s"
                  % (os.path.relpath(z, ROOT), sha[:12]))
    return 1 if bad else 0


def drift():
    """ADVISORY. How far the ship list is behind the tree. Re-cutting is ⬛ DAVE'S."""
    text, refusal = _load_manifest()
    if refusal is not None:
        return refusal
    man = json.loads(text)
    sha = man["commit"]
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    head = r.stdout.strip()
    if r.returncode != 0 or not head:
        return cna.refuse("the pack ship list", "HEAD is not resolvable in this checkout")
    if head == sha:
        print("PASS — the manifest was generated at HEAD (%s). The ship list is current."
              % sha[:12])
        return 0
    c = subprocess.run(["git", "rev-list", "--count", "%s..HEAD" % sha],
                       cwd=ROOT, capture_output=True, text=True)
    if c.returncode != 0:
        return cna.refuse("the pack ship list",
                          "the manifest's commit %s is not an ancestor of HEAD in this checkout "
                          "— the distance cannot be measured" % sha[:12])
    n = c.stdout.strip() or "?"
    print("ADVISORY — the manifest was generated at %s; HEAD is %s, %s commit(s) later."
          % (sha[:12], head[:12], n))
    print("  A pack cut now would ship the tree as it stood at %s. That may be exactly right." % sha[:12])
    print("  ⬛ WHETHER TO RE-CUT IS DAVE'S (s219-D4(2)): a release is explicit, versioned, his word.")
    print("  If he says re-cut: %s" % REMEDY)
    return 1


def selftest():
    fails, n = [], [0]

    def bite(name, ok, why=""):
        n[0] += 1
        if not ok:
            fails.append("[%s] %s" % (name, why))

    # ---- the manifest check must be a REAL byte compare, proven in BOTH directions on a copy.
    text, refusal = _load_manifest()
    bite("manifest/present", refusal is None, "no manifest to test against")
    if refusal is None:
        man = json.loads(text)
        probe = json.load(open(gen.PROBE_PATH, encoding="utf-8")) if os.path.exists(gen.PROBE_PATH) else None
        bite("probe/present", probe is not None, "no gate probe on disk")
        if probe is not None and probe.get("commit") == man.get("commit"):
            fresh = gen.canonical(gen.build_manifest(man["commit"], probe))
            bite("manifest/matches-a-fresh-generation", fresh == text,
                 "the manifest on disk is NOT what the generator produces — that is the gate's "
                 "own subject and it is red right now")
            # the mutation: one path removed from the file must be SEEN
            mutant = json.loads(text)
            for g in mutant["groups"]:
                if g["paths"]:
                    g["paths"] = g["paths"][1:]
                    g["files"] -= 1
                    break
            bite("manifest/mutation-is-seen", gen.canonical(mutant) != fresh,
                 "a manifest with a path removed must not compare equal")
            bite("manifest/hash-bites",
                 gen.manifest_hash(gen.canonical(mutant)) != gen.manifest_hash(fresh),
                 "the hash must change when the content does")

    # ---- the pack arm's resting state is a REFUSAL, and a refusal is not a pass
    rc = pack_check()
    if packs():
        bite("pack/verdict-is-a-verdict", rc in (0, 1),
             "a pack exists, so the arm must return a real verdict, got %r" % rc)
    else:
        bite("pack/refuses-when-nothing-is-baked", cna.is_refusal(rc),
             "with no zip in dist/ the arm must REFUSE (77), never pass silently; got %r" % rc)
    bite("pack/refusal-is-not-zero", not cna.is_refusal(0),
         "the convention's exit code must not collide with a pass")

    # ---- #220 two-release scoping: the arm audits ONLY the manifest's own version; a frozen
    # older zip must be SKIPPED (never failed), and a manifest naming an unbaked version is RED.
    if refusal is None and len(packs()) >= 2:
        bite("pack/frozen-history-is-skipped-not-failed", rc == 0,
             "with the current zip green, an older frozen zip must not turn the arm red "
             "(the pre-#220 category error); got rc=%r" % rc)
    if refusal is None and packs():
        # mutation: hide the manifest's own zip from the glob — the arm must go RED
        # (a manifest naming a release nobody baked), never skip-everything-and-pass.
        _want = str(json.loads(text).get("version", "")).strip()
        _cur = "Apollo-Spider-%s.zip" % _want
        _all = packs()
        _g = globals()
        _real_packs = _g["packs"]
        _g["packs"] = lambda: [z for z in _all if os.path.basename(z) != _cur]
        try:
            _mut_rc = pack_check() if _g["packs"]() else None
        finally:
            _g["packs"] = _real_packs
        if _mut_rc is not None:
            bite("pack/unbaked-version-is-red", _mut_rc == 1,
                 "a manifest naming a version with no zip must be RED, not a "
                 "skip-everything pass; got %r" % _mut_rc)

    # ---- the drift arm must never be able to say PASS while the commits differ
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    head = r.stdout.strip()
    man_commit = json.loads(text)["commit"] if refusal is None else ""
    d = drift()
    if head and man_commit:
        bite("drift/reads-the-distance", (d == 0) == (head == man_commit),
             "drift must be green exactly when the manifest is AT head (head=%s manifest=%s "
             "rc=%r)" % (head[:12], man_commit[:12], d))

    print("selftest: %d bites, %d fail(s)" % (n[0], len(fails)))
    for f in fails:
        print("  RED " + f)
    return not fails


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    # `--check` is the surveyable spelling of `--manifest-check`: `_build_survey.py` only RUNS a
    # step whose every argument is in its NON_MUTATING set (`--check` / `--selftest`), so a
    # read-only check that wants to be asked by the survey has to say `--check`.
    ap.add_argument("--check", action="store_true", help="alias for --manifest-check")
    ap.add_argument("--manifest-check", action="store_true")
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--drift", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if a.manifest_check or a.check:
        sys.exit(manifest_check())
    if a.pack:
        sys.exit(pack_check())
    if a.drift:
        sys.exit(drift())
    ap.print_help()


if __name__ == "__main__":
    main()
