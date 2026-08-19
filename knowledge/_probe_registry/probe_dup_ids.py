#!/usr/bin/env python3
"""probe_dup_ids.py — P-2: duplicate `id` + unresolved IDREF scan over review surfaces (W-45).

THE CLASS, from the receipts: at #204 the adversarial verifier (NEW-1) found the four-theme
review pages repeat every `id` once per theme pane — eight panes, one id set. An
`aria-labelledby` IDREF resolves to the FIRST match in document order, so **seven of the eight
panes' progressbars took their accessible name from the mono/light pane**, and `pcv-contactless`
×8 was the same shape for an SVG reference (duplicate ids are also invalid HTML). Every gate in
the chain was green: the pages are hand-built review artefacts and NOTHING PARSES THEM IN THE
CONSUMER'S GRAMMAR [[no-gate-parses-the-artefact]]. Repaired the same session by suffixing every
id `--<theme>-<mode>` and rewriting each reference INSIDE ITS OWN PANE
(`notes/_receipts/2026-08-19-204-buildpm-claim-table.md` FIX 2 — six pages, DUP=0, unresolved_aria=0).

WHAT THIS PROBE DOES, per file:
  · collects every `id="…"` and reports any that appears more than once (FAIL tier)
  · resolves every IDREF-bearing attribute (`aria-labelledby/describedby/controls/owns/flowto/
    activedescendant/details/errormessage`, `for`, `headers`) token by token — an unresolved
    token is a FAIL-tier finding
  · resolves `href="#…"` / `xlink:href="#…"` fragments as a WARN tier, REPORTED but NOT counted
    as a finding. Why: #204 declared the placeholder demo links (`#doc-jun`, `#top`, …) a
    pre-existing specimen habit and an open design decision, NOT a duplicate-id defect. That
    judgment is inherited here rather than silently re-litigated.

GLOB — this probe rules only as wide as this list [[gate-glob-scope-rule]]:
    reviews/REVIEW-*.html      (the surfaces Dave rules from; where the class was found)
Widen with `--glob '<pattern>'` (repeatable); widening is a visible argument, never an inference.

⛔ WHAT IT CANNOT SEE: ids or references built by JavaScript at runtime · whether a resolved
reference points at the RIGHT element (presence only) · duplicate ids that are semantically
fine because their panes are never simultaneously in the a11y tree (there is no such case in
this repo today, but the probe cannot tell) · anything outside the glob.

ENVIRONMENT: sandbox (pure python, regex over markup — no browser, no jsdom).

USAGE
  python3 knowledge/_probe_registry/probe_dup_ids.py --check
  python3 knowledge/_probe_registry/probe_dup_ids.py --check --glob 'reviews/*.html'
  python3 knowledge/_probe_registry/probe_dup_ids.py --selftest
EXIT: 0 clean · 1 findings.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob as globmod, os, re, shutil, sys, tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_GLOBS = ["reviews/REVIEW-*.html"]

ID_RE = re.compile(r"""\sid\s*=\s*["']([^"']+)["']""")
IDREF_ATTRS = ("aria-labelledby", "aria-describedby", "aria-controls", "aria-owns",
               "aria-flowto", "aria-activedescendant", "aria-details", "aria-errormessage",
               "for", "headers")
IDREF_RE = re.compile(r"""\s(%s)\s*=\s*["']([^"']*)["']""" % "|".join(IDREF_ATTRS))
FRAG_RE = re.compile(r"""\s(?:xlink:)?href\s*=\s*["']#([^"']+)["']""")


def scan_file(path):
    """(dups, unresolved, frag_misses, n_ids) for one file. Line numbers included."""
    text = open(path, encoding="utf-8", errors="replace").read()
    ids = ID_RE.findall(text)
    counts = Counter(ids)
    dups = sorted((i, n) for i, n in counts.items() if n > 1)
    idset = set(ids)
    unresolved, frag = [], []
    for lineno, line in enumerate(text.splitlines(), 1):
        for attr, val in IDREF_RE.findall(line):
            for tok in val.split():
                if tok and tok not in idset:
                    unresolved.append((lineno, attr, tok))
        for tok in FRAG_RE.findall(line):
            if tok not in idset:
                frag.append((lineno, tok))
    return dups, unresolved, frag, len(ids)


def scan(paths, verbose=True):
    """Return (findings, warns). findings = [(path, kind, detail)] — FAIL tier."""
    findings, warns = [], []
    for path in paths:
        rel = os.path.relpath(path, ROOT)
        dups, unresolved, frag, n_ids = scan_file(path)
        for i, n in dups:
            findings.append((rel, "DUPLICATE-ID", "%r appears %d× — an IDREF resolves to the "
                                                  "FIRST match only" % (i, n)))
        for lineno, attr, tok in unresolved:
            findings.append((rel, "UNRESOLVED-IDREF", "%s:%d %s=%r resolves to no id"
                             % (rel, lineno, attr, tok)))
        for lineno, tok in frag:
            warns.append((rel, "FRAGMENT-MISS", "%s:%d href='#%s' targets no id (WARN tier — "
                          "#204 declared placeholder demo links a design question, not this "
                          "class)" % (rel, lineno, tok)))
        if verbose:
            status = "⛔" if (dups or unresolved) else "OK"
            print("  %-3s %-58s ids=%3d DUP=%d unresolved_idref=%d frag_miss=%d"
                  % (status, rel[-58:], n_ids, len(dups), len(unresolved), len(frag)))
    if verbose:
        for rel, kind, detail in findings:
            print("  ⛔ %s · %s · %s" % (rel, kind, detail))
        for rel, kind, detail in warns[:12]:
            print("  ⚠ %s" % detail)
        if len(warns) > 12:
            print("  ⚠ … %d more WARN-tier fragment misses (not findings)" % (len(warns) - 12))
    return findings, warns


def resolve(patterns, root=ROOT):
    out = []
    for pat in patterns:
        out += sorted(globmod.glob(os.path.join(root, pat)))
    return out


def check(patterns=None):
    patterns = patterns or DEFAULT_GLOBS
    paths = resolve(patterns)
    findings, warns = scan(paths)
    print("P-2 duplicate-ID/IDREF scan: %d file(s) over %s · %d finding(s) · %d WARN-tier "
          "fragment miss(es)" % (len(paths), patterns, len(findings), len(warns)))
    if not paths:
        print("⚠ THE GLOB MATCHED NOTHING — an empty population is not a pass "
              "(unmatched-grep-is-not-an-absence).")
        print("PROBE P-2 — findings=1")
        return 1
    print("PROBE P-2 — findings=%d" % len(findings))
    return 1 if findings else 0


def selftest():
    """PLANT-THEN-DETECT on a REAL review page, both directions — the probe is DRIVEN on a
    planted artefact, never asserted against its own clause."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="p2-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    src = sorted(globmod.glob(os.path.join(ROOT, "reviews", "REVIEW-*.html")))
    if not src:
        print("⛔ selftest cannot run: no reviews/REVIEW-*.html to plant into (declared).")
        return 1
    src = src[0]
    work = os.path.join(tmp, os.path.basename(src))
    shutil.copyfile(src, work)

    base, base_warns = scan([work], verbose=False)
    print("  · baseline on a copy of %s: %d finding(s), %d warn(s)"
          % (os.path.basename(src), len(base), len(base_warns)))

    text = open(work, encoding="utf-8", errors="replace").read()
    ids = ID_RE.findall(text)
    if not ids:
        print("⛔ selftest cannot run: the chosen page carries no ids (declared).")
        return 1
    victim = ids[0]
    # plant 1 — a genuine DUPLICATE of a real id (#204 NEW-1 shape)
    # plant 2 — an aria-labelledby pointing at an id that exists nowhere
    planted = text.replace("</body>", '<span id="%s"></span>\n'
                                      '<div aria-labelledby="p2-selftest-nonexistent"></div>\n'
                                      "</body>" % victim, 1)
    if planted == text:
        planted = text + ('<span id="%s"></span>'
                          '<div aria-labelledby="p2-selftest-nonexistent"></div>' % victim)
    open(work, "w", encoding="utf-8").write(planted)
    after, _ = scan([work], verbose=False)
    new = [f for f in after if f not in base]
    kinds = {k for _p, k, _d in new}
    if "DUPLICATE-ID" not in kinds:
        fails.append("PLANT NOT CAUGHT: a duplicated real id (%r) produced no DUPLICATE-ID "
                     "finding" % victim)
    else:
        print("  ✅ plant caught (DUPLICATE-ID): %s" % [d for _p, k, d in new
                                                        if k == "DUPLICATE-ID"][0][:90])
    if "UNRESOLVED-IDREF" not in kinds:
        fails.append("PLANT NOT CAUGHT: aria-labelledby to a nonexistent id produced no "
                     "UNRESOLVED-IDREF finding")
    else:
        print("  ✅ plant caught (UNRESOLVED-IDREF): %s" % [d for _p, k, d in new
                                                            if k == "UNRESOLVED-IDREF"][0][:90])

    # direction 2 — remove the plants, the probe must return to baseline
    shutil.copyfile(src, work)
    restored, _ = scan([work], verbose=False)
    if restored != base:
        fails.append("REMOVAL NOT GREEN: restored page gave %d finding(s), baseline %d"
                     % (len(restored), len(base)))
    else:
        print("  ✅ removal green: with the plants gone the probe returns to baseline (%d)"
              % len(base))

    # control — the WARN tier must NOT count as a finding (the #204 inherited judgment)
    open(work, "w", encoding="utf-8").write(
        open(src, encoding="utf-8", errors="replace").read()
        .replace("</body>", '<a href="#p2-selftest-no-such-target">x</a></body>', 1))
    warn_findings, warn_warns = scan([work], verbose=False)
    if warn_findings != base:
        fails.append("WARN TIER LEAKED: a bare fragment miss became a finding — #204's declared "
                     "residual would be re-litigated on every run")
    elif len(warn_warns) <= len(base_warns):
        fails.append("WARN TIER BLIND: a planted fragment miss was not even reported as a WARN")
    else:
        print("  ✅ tier control: a planted `href='#…'` miss is REPORTED as WARN and does NOT "
              "become a finding")

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-2 selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ P-2 selftest PASS — planted duplicate id and dangling IDREF both detected on a "
          "REAL page, removal green, WARN tier held.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    pats = [argv[i + 1] for i, a in enumerate(argv) if a == "--glob"]
    sys.exit(check(pats or None))
