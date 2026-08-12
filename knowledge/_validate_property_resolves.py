#!/usr/bin/env python3
"""
C2 — the wide fail-loud gate.  RULED by Dave 2026-07-27 (ds-018, review v1).

    "A declaration referencing a custom property that resolves nowhere in its own
     scope is a BUILD FAILURE, not a silent fallback."

WHY THIS EXISTS
---------------
ds-018: `.dv-leg-reset:disabled` referenced `--border-disabled` and `--text-disabled`.
Both are declared on ten `.cn-*` FORM scopes and on ZERO chart scopes.  CSS does not
fall back to the previous cascade value when a `var()` fails — the declaration becomes
invalid-at-computed-value-time and the property takes its *initial* value.  For
`border-color` that is `currentColor`, so the DEAD control rendered at ink: 17.40:1
against a page where the LIVE control's border sat at 1.31:1.  Thirteen times the
contrast, on the disabled state, silently, for as long as the component has shipped.

It was instance FIVE of the silent-lookup class (ds-010 · ds-013 · ds-016 · ds-018,
plus the `--data-text-on-series` near-miss the Chart-bar spine documents in a comment).
Every instance was found by eye or by accident.  None was found by a gate.  This is
the gate.

★ WHAT THIS GATE CAN AND CANNOT SEE — read before trusting a green run.
A gate that quietly narrows its own rule is a documented failure mode in this repo
(see MEMORY `gate-narrows-its-own-rule`), so the limits are published, not buried:

  CAN see   a `var(--x)` with no fallback where `--x` is declared NOWHERE the file
            can reach (its own <style> blocks, its own inline style="" attributes,
            or a stylesheet it actually <link>s).  That is exactly the ds-018 shape.

  CANNOT    per-SELECTOR scope.  `--x` declared only on `.cn-input` and consumed on
  see       `.dv-legrow` resolves nowhere at runtime, but both live in one file, so
            this gate reads it as declared.  Catching that needs a real cascade —
            i.e. a render — and belongs with the render-verify harness, not here.
            ⚠ DO NOT read a green run as "no silent lookups remain".  It means
            "no file-scope-invisible lookups remain".

  CANNOT    anything a JS string builds at runtime.  Behaviour blocks are skipped
  see       deliberately; `<style>` and inline `style=""` are the surfaces.

C3 was NOT rejected when Dave selected C2 — it was simply not selected, and it catches
a resolved-but-WRONG ladder (a disabled control out-contrasting its own enabled state)
that C2 is blind to by construction.  It stays a live candidate.  Do not let this gate's
existence be read as closing it.

Usage:
    python3 knowledge/_validate_property_resolves.py            # gate (exit 1 on fail)
    python3 knowledge/_validate_property_resolves.py --selftest # bite-tests + green control
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import os
import re
import sys
import glob
import tempfile
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)

# Only as wide as its glob — and the glob is stated here so widening is a visible edit.
GLOBS = [
    "knowledge/snippets/*.reference.html",
    "knowledge/_proforma/*.html",
]

# Properties the browser supplies. A reference to one of these is never "unresolved".
# (Empty today; kept as the explicit escape hatch so nobody adds one silently in code.)
BUILTIN = set()

# Custom properties a file may legitimately receive from OUTSIDE its own document —
# i.e. set by a host page or a harness at runtime. Each entry needs a reason.
# ⚠ Adding to this list is an ENFORCEMENT DECISION. It weakens the gate for that name
#   everywhere the glob reaches. Per derivation governance, additions are Dave's.
EXTERNALLY_PROVIDED = {
    # name: reason
}

STYLE_RE  = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
LINK_RE   = re.compile(r"""<link[^>]+rel=["']stylesheet["'][^>]*>""", re.I)
HREF_RE   = re.compile(r"""href=["']([^"']+)["']""", re.I)
INLINE_RE = re.compile(r"""\sstyle=["']([^"']*)["']""", re.I)
DECL_RE   = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")
# capture the delimiter so `var(--x, fallback)` can be treated as safe
USE_RE    = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*([,)])")

# strip CSS comments before scanning, or a commented-out example counts as a use
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def css_of(path, text):
    """Every chunk of CSS this document actually applies, plus what it links."""
    chunks = []
    for m in STYLE_RE.finditer(text):
        chunks.append(m.group(1))
    for m in INLINE_RE.finditer(text):
        chunks.append(m.group(1))
    linked = []
    for tag in LINK_RE.findall(text):
        href = HREF_RE.search(tag)
        if not href:
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), href.group(1)))
        if os.path.isfile(target):
            with open(target, encoding="utf-8") as fh:
                chunks.append(fh.read())
            linked.append(os.path.relpath(target, REPO))
        else:
            # a <link> that 404s is its own defect — surface it, never swallow it
            linked.append("MISSING:" + href.group(1))
    return chunks, linked


def scan(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    chunks, linked = css_of(path, text)
    declared, used = set(), {}
    for chunk in chunks:
        clean = COMMENT_RE.sub(" ", chunk)
        for m in DECL_RE.finditer(clean):
            declared.add(m.group(1))
        for m in USE_RE.finditer(clean):
            name, delim = m.group(1), m.group(2)
            if delim == ",":
                continue          # has a fallback — resolving nowhere is then declared intent
            used.setdefault(name, 0)
            used[name] += 1
    unresolved = {
        n: c for n, c in used.items()
        if n not in declared and n not in BUILTIN and n not in EXTERNALLY_PROVIDED
    }
    missing_links = [l for l in linked if l.startswith("MISSING:")]
    return unresolved, missing_links, len(declared), len(used)


def run(paths, quiet=False):
    fails = 0
    checked = 0
    for path in paths:
        checked += 1
        unresolved, missing_links, ndecl, nused = scan(path)
        rel = os.path.relpath(path, REPO)
        for href in missing_links:
            fails += 1
            if not quiet:
                print("  ❌ FAIL %s: <link> to %s does not exist — a 404 stylesheet "
                      "is SILENT in the browser (ds-013)" % (rel, href[len("MISSING:"):]))
        for name, count in sorted(unresolved.items()):
            fails += 1
            if not quiet:
                print("  ❌ FAIL %s: `%s` referenced %d× with no fallback and declared "
                      "nowhere this file can reach — the declaration is invalid at "
                      "computed-value time and the property silently takes its INITIAL "
                      "value (ds-018)" % (rel, name, count))
    if not quiet:
        print("property-resolves gate (C2): %d file(s), %d failure(s)" % (checked, fails))
    return fails


def collect():
    paths = []
    for g in GLOBS:
        paths.extend(sorted(glob.glob(os.path.join(REPO, g))))
    return paths


# ── selftest ────────────────────────────────────────────────────────────────────
# Every gate ships a bite proving it can FAIL. A gate that has never been seen to go
# red is not evidence — the repo has been bitten by exactly that five sessions running.
def selftest():
    ok = True
    tmp = tempfile.mkdtemp(prefix="c2-selftest-")
    try:
        real = os.path.join(REPO, "knowledge/snippets/Chart-bar.reference.html")
        with open(real, encoding="utf-8") as fh:
            src = fh.read()

        # ── GREEN CONTROL: the real file, untouched, must pass ──
        green = os.path.join(tmp, "green.reference.html")
        # rewrite the type.css link so it still resolves from the temp dir
        rebased = src.replace('href="../canon/type.css"',
                              'href="%s"' % os.path.join(REPO, "knowledge/canon/type.css"))
        with open(green, "w", encoding="utf-8") as fh:
            fh.write(rebased)
        n = run([green], quiet=True)
        print("  [%s] green control — the shipping file passes (%d failure(s))"
              % ("PASS" if n == 0 else "FAIL", n))
        ok &= (n == 0)

        # ── BITE 1: the ds-018 shape itself — reintroduce the undeclared reference ──
        bite1 = os.path.join(tmp, "bite1.reference.html")
        b1 = rebased.replace(
            "border-color:var(--line); color:var(--data-control-label-disabled);",
            "border-color:var(--border-disabled); color:var(--text-disabled);")
        assert b1 != rebased, "bite 1 did not apply — the anchor moved, FIX THE BITE"
        with open(bite1, "w", encoding="utf-8") as fh:
            fh.write(b1)
        n = run([bite1], quiet=True)
        print("  [%s] bite 1 — ds-018 reintroduced (--border-disabled/--text-disabled): "
              "%d failure(s), expected 2" % ("PASS" if n == 2 else "FAIL", n))
        ok &= (n == 2)

        # ── BITE 2: --muted, the sibling defect this pass also closed ──
        bite2 = os.path.join(tmp, "bite2.reference.html")
        b2 = rebased.replace("border-color:var(--data-control-swatch-off);",
                             "border-color:var(--muted);")
        assert b2 != rebased, "bite 2 did not apply — the anchor moved, FIX THE BITE"
        with open(bite2, "w", encoding="utf-8") as fh:
            fh.write(b2)
        n = run([bite2], quiet=True)
        print("  [%s] bite 2 — --muted reintroduced: %d failure(s), expected 1"
              % ("PASS" if n == 1 else "FAIL", n))
        ok &= (n == 1)

        # ── BITE 3: a var WITH a fallback must NOT fail (declared intent) ──
        bite3 = os.path.join(tmp, "bite3.reference.html")
        b3 = rebased.replace("border-color:var(--data-control-swatch-off);",
                             "border-color:var(--nowhere-at-all, #808080);")
        assert b3 != rebased, "bite 3 did not apply — the anchor moved, FIX THE BITE"
        with open(bite3, "w", encoding="utf-8") as fh:
            fh.write(b3)
        n = run([bite3], quiet=True)
        print("  [%s] bite 3 — var() WITH a fallback is intent, not a defect: "
              "%d failure(s), expected 0" % ("PASS" if n == 0 else "FAIL", n))
        ok &= (n == 0)

        # ── BITE 4: a <link> that 404s — ds-013's shape ──
        bite4 = os.path.join(tmp, "bite4.reference.html")
        b4 = rebased.replace('rel="stylesheet" href="%s"'
                             % os.path.join(REPO, "knowledge/canon/type.css"),
                             'rel="stylesheet" href="./does-not-exist.css"')
        assert b4 != rebased, "bite 4 did not apply — the anchor moved, FIX THE BITE"
        with open(bite4, "w", encoding="utf-8") as fh:
            fh.write(b4)
        n = run([bite4], quiet=True)
        print("  [%s] bite 4 — 404 stylesheet is caught, not swallowed: %d failure(s), "
              "expected ≥1" % ("PASS" if n >= 1 else "FAIL", n))
        ok &= (n >= 1)

        # ── BITE THE BITE: neuter the detector, the selftest must notice ──
        saved = globals()["USE_RE"]
        globals()["USE_RE"] = re.compile(r"var\(\s*(--nothing-matches-this)\s*([,)])")
        n = run([bite1], quiet=True)
        globals()["USE_RE"] = saved
        print("  [%s] bite-the-bite — a blinded detector reports 0 on a known-bad file "
              "(%d), so the bites above are measuring something"
              % ("PASS" if n == 0 else "FAIL", n))
        ok &= (n == 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("  %s C2 selftest: %s" % ("✅" if ok else "❌",
                                    "all failure classes bite; green control passes"
                                    if ok else "SELFTEST FAILED — do not trust this gate"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())

    fails = run(collect())

    # ── ADVISORY BY CONSTRUCTION, and deliberately so ────────────────────────────
    # C2 is RULED BLOCKING. It ships advisory for exactly as long as it takes to clear
    # the backlog it found on its first run, because the alternative was worse in two
    # specific ways and both have bitten this repo before:
    #
    #   · going blocking today means clearing 10 pre-existing failures NOW, and three of
    #     them (--phys-size on Alert/Empty-state/Popover, --mark across 7 pro-forma files)
    #     need VALUES. Value promotion is Dave's alone — derivation governance. An agent
    #     inventing four numbers to turn a build green is the exact failure the rule exists
    #     to prevent.
    #   · narrowing the glob to charts would go green today and would be the
    #     `gate-narrows-its-own-rule` failure in its purest form: the rule Dave ruled is
    #     corpus-wide, and a gate whose glob is smaller than its rule silently redefines
    #     the rule as whatever it happens to check.
    #
    # So: the rule stays WIDE, the findings are PUBLISHED, and nothing is faked green.
    # ⇒ PROMOTION IS A ONE-LINE EDIT: add ["--strict"] to the build step in _build_all.py.
    #   Do it the moment the worklist below is empty. An advisory gate that is never
    #   promoted is a gate that has quietly become documentation.
    strict = "--strict" in sys.argv
    if fails and not strict:
        print("  ⚠ ADVISORY — C2 is RULED BLOCKING but ships advisory until the backlog")
        print("    above is cleared. Promote by adding [\"--strict\"] to the _build_all.py step.")
        print("    ⛔ Do NOT clear it by inventing values: --mark and --phys-size are Dave's.")
    sys.exit(1 if (fails and strict) else 0)
