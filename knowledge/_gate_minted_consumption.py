#!/usr/bin/env python3
"""_gate_minted_consumption.py — the MINTED-TOKEN CONSUMPTION inventory (ADVISORY, built #219 lane 5).

THE CLASS — the exact reverse of `_gate_dataviz_vars.py`.
`_gate_dataviz_vars` catches a `var(--x)` with NO DECLARATION: a use with no mint, which paints
silent black. Nothing catches the mirror image: a DECLARATION with NO USE — a token minted into
`canon.css`, carrying a value Dave ruled, that no component ever names. It renders nothing, so it
has no visible signature at all; it is invisible to every one of the 13+ gates, because each of
them asks "does this use resolve?" and none asks "is this mint read?".

The shape is what a half-finished ENACTMENT leaves behind. #219 caught two live instances by hand:
the s202-D1 segmented radii (minted #202, first consumed #219 — 17 sessions dark) and
`--padding-card-internal` (ruled s201-D4, minted console-only, consumed by nothing today). Both
were found by a person looking, not by an instrument.

⚠ WHY THIS IS ADVISORY AND MUST STAY ADVISORY UNTIL DAVE RULES
An unconsumed mint is NOT a defect on its face. Three different things wear the same shape:
  (1) a forgotten wire      — the ruling names a consumer and nobody wired it. A real defect.
  (2) a reserved slot       — minted deliberately, ahead of the component that will read it.
  (3) a mechanical shadow   — see ALIAS-SHADOW below; nobody authored it at all.
No presence test can tell (1) from (2). Separating them needs a DECLARATION on the token
(`$consumer` / `$reserved`), which is a store-schema change and therefore Dave's. Until then this
gate MEASURES and never blocks. Promotion is Dave's word, not a builder's pick.

THE TWO FALSE-POSITIVE CLASSES, SUBTRACTED EXPLICITLY
A naive "declared but never `var()`-ed" sweep over `canon.css` is wrong twice over, because two
whole families of custom properties are consumed by a mechanism that is not CSS at all:

  ALIAS-TARGET — the token path is an `$alias` TARGET in a base store. `gen_theme_cascade`
    resolves those in PYTHON at MINT time (`base_value()` follows `$alias`; `_expand_aliases()`
    materialises the effective override), so the value travels by the token path, never by a CSS
    `var()`. Proof on real data: supercharge overrides `color/neutral/15`; `background/default`
    carries `"$alias": {"light": "color/neutral/15"}`; canon.css base `:root` reads
    `--color-neutral-15:#FFFFFF` / `--background-default:#FFFFFF`, and the supercharge block reads
    `--color-neutral-15:#F7F6F4` / `--background-default:#F7F6F4`. The second value could ONLY have
    arrived down the alias edge — and `var(--color-neutral-15)` appears nowhere in the repo.
    Emitting the primitive as a CSS custom property is arguably surplus; it is NOT an orphan.

  ALIAS-SHADOW — a theme-tier declaration whose path the theme's override file does not declare,
    but which is alias-reachable from a path it does. `_expand_aliases` materialises an effective
    override for EVERY such path, consumed or not. Nobody authored these; they are the mechanical
    shadow of a DNA-tier override. Reporting them as "forgotten wires" would be twenty findings
    where there is one generator-scope question.

WHAT IT REPORTS (advisory, exit 0 unless it cannot run)
    declared / consumed / ALIAS-TARGET / ALIAS-SHADOW / ORPHAN, split base tier vs theme tier,
    every ORPHAN named with its tier, its themes and its canon.css line.

★ WHAT THIS GATE CAN AND CANNOT SEE (published, not buried)
  CAN see   a custom property declared in canon.css that no `var()` in the CONSUMER GLOB names.
  CAN see   the tier and theme of the declaration, so "console minted it and nothing reads it"
            is distinguishable from "everything reads it except supercharge".
  CANNOT    a var consumed only from a file outside the CONSUMER GLOB (reviews/ is excluded on
  see       purpose: a review page consuming a token proves a specimen, not a system).
  CANNOT    a var consumed by a name a script BUILDS at runtime (`style.setProperty('--'+k)`).
  see       String-built names are unanalysable; a token reached only that way reads as an orphan.
  CANNOT    whether an orphan SHOULD have a consumer. That is a ruling, never a measurement.
  see
  CANNOT    a mint that IS consumed but by the WRONG surface. Presence of a use only.
  see
  ⚠ A run with zero orphans would mean "every canon.css declaration is named somewhere in the
    glob". It would NOT mean the tokens are wired to the right places.

CONSUMER GLOB — this gate rules only as wide as this list [[gate-glob-scope-rule]]:
    the whole repo tree, extensions .css .html .js .py .json .md .svg, MINUS EXCLUDE_DIRS below.
    Widening or narrowing it is a visible edit to EXCLUDE_DIRS, never an inference.

CONSUMER: `_build_all.py` gate chain, ADVISORY tier. Run standalone:
    python3 knowledge/_gate_minted_consumption.py             # inventory (always exit 0)
    python3 knowledge/_gate_minted_consumption.py --orphans   # + the full ORPHAN listing
    python3 knowledge/_gate_minted_consumption.py --selftest  # 10 arms, both directions + mutants
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
import json
import shutil
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
CANON = os.path.join(ROOT, "canon", "canon.css")
TOKENS = os.path.join(ROOT, "tokens")
THEMES_DIR = os.path.join(TOKENS, "themes")

# Directories a consumer may NOT live in. reviews/ and _review/ are excluded on purpose (a review
# page consuming a token proves a specimen, not a system); the rest are archives, vendored copies
# and prose. This list IS the glob — see the docstring.
EXCLUDE_DIRS = {
    ".git", "__pycache__", "node_modules",
    "reviews", "_review", "runs", "outputs", "notes",
    "_to_delete", "_retired", "archive", "_DECISION-HISTORY",
    "second-system-govuk", "designer-skills-v1", "designer-skills-v2", "memento-package",
}
EXT = (".css", ".html", ".js", ".py", ".json", ".md", ".svg")

# A generator that PRINTS a var name is not a consumer of it — these prefixes emit canon.css.
GENERATOR_PREFIXES = ("knowledge/canon/gen_", "knowledge/gen_", "knowledge/_render/gen_")

# SELF-EXCLUSION, declared rather than hidden. This file's docstring quotes real var names as
# WORKED EXAMPLES; without this line the gate reads its own prose and reports the example token
# as consumed — which is exactly the "instrument that measures itself" defect it exists to avoid.
# Caught on the first real run: `--color-neutral-15` came back consumed, by this file.
SELF = os.path.join("knowledge", os.path.basename(os.path.abspath(__file__)))

DECL_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")
USE_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")
THEME_ATTR_RE = re.compile(r'\[data-apollo-theme=["\']([a-z-]+)["\']\]')


class GateError(RuntimeError):
    """Unreadable / missing / empty target. A crash is not a fail — raised, named, exit 2."""


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise GateError("UNREADABLE TARGET %s — %s" % (path, exc))


def _strip_comments(css):
    """Blank comments out but KEEP their newlines — a line number that shifts is a lie."""
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)


def declarations(css):
    """{var: {'base': line|None, 'themes': {theme: line}}} — a brace scanner, so @media nests.

    A declaration is BASE-tier if no enclosing selector carries [data-apollo-theme]; otherwise it
    belongs to that theme. Both tiers are recorded: the same name is commonly declared in both.
    """
    css = _strip_comments(css)
    out = {}
    stack, buf, line = [], [], 1
    for ch in css:
        if ch == "\n":
            line += 1
        if ch == "{":
            stack.append(["".join(buf).strip(), line])
            buf = []
        elif ch == "}":
            body = "".join(buf)
            sel = " ".join(s for s, _ in stack)
            open_line = stack[-1][1] if stack else line
            m = THEME_ATTR_RE.search(sel)
            for mm in DECL_RE.finditer(body):
                ln = open_line + body[:mm.start()].count("\n")
                rec = out.setdefault(mm.group(1), {"base": None, "themes": {}})
                if m:
                    rec["themes"].setdefault(m.group(1), ln)
                elif rec["base"] is None:
                    rec["base"] = ln
            buf = []
            if stack:
                stack.pop()
        else:
            buf.append(ch)
    return out


def consumers(root, exclude=None, ext=EXT):
    """{var: {relpath, ...}} for every `var(--x)` in the CONSUMER GLOB. Generators excluded."""
    exclude = EXCLUDE_DIRS if exclude is None else exclude
    used = {}
    seen_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for fn in filenames:
            if not fn.endswith(ext):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            if rel.startswith(GENERATOR_PREFIXES) or rel == SELF:
                continue
            seen_files += 1
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            for name in set(USE_RE.findall(text)):
                used.setdefault(name, set()).add(rel)
    if not seen_files:
        raise GateError("EMPTY CONSUMER POPULATION — no scannable file under %s "
                        "(a gate with nothing to scan cannot fail; that is not a pass)" % root)
    return used


# ---------------------------------------------------------------- token-store knowledge
def _normalize(seg):
    """Byte-identical to gen_theme_cascade.normalize — the var-name grammar has ONE definition."""
    return re.sub(r"[^a-z0-9]+", "-", str(seg).lower()).strip("-")


def var_name(path):
    return "--" + "-".join(_normalize(s) for s in path.split("/"))


def _cascade():
    """Import the generator that OWNS the path->var mapping. Never re-implement it here."""
    sys.path.insert(0, os.path.join(ROOT, "canon"))
    try:
        import gen_theme_cascade as g
        return g
    except Exception as exc:                                    # noqa: BLE001 - fail loud, named
        raise GateError("CANNOT IMPORT gen_theme_cascade (%s) — refusing to classify blind: "
                        "without its alias_map() the two false-positive classes cannot be "
                        "subtracted and every primitive would read as an orphan" % exc)


def alias_target_vars(cascade):
    """{var: [token path, ...]} for every path that is an $alias TARGET in a base store.

    These are consumed at MINT time, in Python, by base_value()/_expand_aliases — never by CSS."""
    out = {}
    for path, edge in cascade.alias_map().items():
        for target in edge.values():
            out.setdefault(var_name(target), set()).add(target)
    return {k: sorted(v) for k, v in out.items()}


def declared_override_vars(themes_dir):
    """{var: {theme, ...}} for paths a theme's override FILE actually declares (authored wires)."""
    out = {}
    if not os.path.isdir(themes_dir):
        raise GateError("MISSING TARGET themes dir %s" % themes_dir)
    for fn in sorted(os.listdir(themes_dir)):
        if not fn.endswith(".overrides.json"):
            continue
        try:
            doc = json.load(open(os.path.join(themes_dir, fn), encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise GateError("UNREADABLE OVERRIDE SET %s — %s" % (fn, exc))
        theme = doc.get("$theme") or fn.split(".")[0]
        for key in (doc.get("overrides") or {}):
            out.setdefault(var_name(key), set()).add(theme)
    return out


# ---------------------------------------------------------------- the run
ALIAS_TARGET = "ALIAS-TARGET"
ALIAS_SHADOW = "ALIAS-SHADOW"
ORPHAN = "ORPHAN"


def run(canon_path=None, root=None, themes_dir=None, exclude=None,
        subtract_alias_targets=True, subtract_alias_shadows=True, quiet=False):
    """Returns (decls, used, classed, stats).

    `subtract_alias_targets` / `subtract_alias_shadows` are MUTANT HOOKS — the selftest drives
    them False to prove each subtraction is load-bearing. Never pass False from a real run.
    """
    canon_path = canon_path or CANON
    root = root or REPO
    themes_dir = themes_dir or THEMES_DIR
    if not os.path.isfile(canon_path):
        raise GateError("MISSING TARGET canon.css at %s — refusing to run a gate blind" % canon_path)
    decls = declarations(_read(canon_path))
    if not decls:
        raise GateError("EMPTY POPULATION — %s declares no custom properties "
                        "(a gate with nothing to inventory cannot fail)" % canon_path)
    used = consumers(root, exclude)

    cascade = _cascade()
    targets = alias_target_vars(cascade) if subtract_alias_targets else {}
    authored = declared_override_vars(themes_dir)

    classed = {}
    for name, rec in decls.items():
        if used.get(name):
            continue                                            # consumed — nothing to say
        if name in targets:
            classed[name] = (ALIAS_TARGET, rec, targets[name])
        elif (subtract_alias_shadows and rec["themes"]
              and name not in authored and rec["base"] is not None):
            # theme-tier emission the override FILE never declared, standing on a base
            # declaration: _expand_aliases materialised it. Nobody authored this wire.
            classed[name] = (ALIAS_SHADOW, rec, [])
        else:
            classed[name] = (ORPHAN, rec, [])

    base_n = sum(1 for r in decls.values() if r["base"] is not None)
    theme_n = sum(1 for r in decls.values() if r["themes"])
    stats = {
        "declared": len(decls), "base_tier": base_n, "theme_tier": theme_n,
        "consumed": sum(1 for n in decls if used.get(n)),
        "unconsumed": len(classed),
        ALIAS_TARGET: sum(1 for c, _, _ in classed.values() if c == ALIAS_TARGET),
        ALIAS_SHADOW: sum(1 for c, _, _ in classed.values() if c == ALIAS_SHADOW),
        ORPHAN: sum(1 for c, _, _ in classed.values() if c == ORPHAN),
        "orphan_theme_tier": sum(1 for c, r, _ in classed.values()
                                 if c == ORPHAN and r["themes"]),
    }
    if not quiet:
        report(classed, stats)
    return decls, used, classed, stats


def orphans(classed):
    return sorted((n, r) for n, (c, r, _t) in classed.items() if c == ORPHAN)


def report(classed, stats, listing=False):
    print("minted-token consumption inventory (ADVISORY) — canon.css declares %d custom "
          "propert%s (base tier %d · theme tier %d)"
          % (stats["declared"], "y" if stats["declared"] == 1 else "ies",
             stats["base_tier"], stats["theme_tier"]))
    print("  consumed by a var() in the glob ......... %d" % stats["consumed"])
    print("  unconsumed .............................. %d" % stats["unconsumed"])
    print("    ├─ %-12s (mint-time $alias) ..... %d" % (ALIAS_TARGET, stats[ALIAS_TARGET]))
    print("    ├─ %-12s (alias expansion) ..... %d" % (ALIAS_SHADOW, stats[ALIAS_SHADOW]))
    print("    └─ %-12s (declared, never read) %d   [%d of them minted per-theme]"
          % (ORPHAN, stats[ORPHAN], stats["orphan_theme_tier"]))
    if listing:
        print("\nORPHANS — declared in canon.css, named by no var() in the glob:")
        for name, rec in orphans(classed):
            where = []
            if rec["base"] is not None:
                where.append("base:%d" % rec["base"])
            where += ["%s:%d" % (t, l) for t, l in sorted(rec["themes"].items())]
            print("  %-46s %s" % (name, " · ".join(where)))
    print("\n⚠ ADVISORY: an unconsumed mint is not a defect on its face — a forgotten wire and a "
          "reserved slot wear the same shape, and no presence test can tell them apart. "
          "Promotion to blocking needs a $consumer/$reserved declaration on the token, and is "
          "Dave's word.")


# ---------------------------------------------------------------- selftest
def _fixture():
    """A real-canon tempdir the arms can mutate. Copies canon/ + tokens/, never the repo."""
    tmp = tempfile.mkdtemp(prefix="mintcons-")
    work = os.path.join(tmp, "knowledge")
    os.makedirs(work)
    shutil.copytree(os.path.join(ROOT, "canon"), os.path.join(work, "canon"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(TOKENS, os.path.join(work, "tokens"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    return tmp, os.path.join(work, "canon", "canon.css"), os.path.join(work, "tokens", "themes")


def _plant(canon_path, decl, theme="console"):
    """Append a declaration into a REAL theme block, so the arm drives the real parser."""
    css = _read(canon_path)
    needle = '[data-apollo-theme="%s"] .cn-tabs{' % theme
    if needle not in css:
        raise GateError("SELFTEST FIXTURE BROKEN — %s not in canon copy" % needle)
    open(canon_path, "w", encoding="utf-8").write(css.replace(needle, needle + "\n  " + decl, 1))


def _selftest():
    ok = True
    n = [0]

    def bite(label, good, detail=""):
        nonlocal ok
        n[0] += 1
        print("  [%d] %-62s %s%s" % (n[0], label, "PASS" if good else "FAIL",
                                     ("  — " + detail) if detail else ""))
        ok = ok and good

    tmp, canon, themes = _fixture()
    try:
        # ARM 1 — green control on the REAL canon: it parses, and the classes are non-empty.
        _d, _u, classed, stats = run(canon, REPO, themes, quiet=True)
        bite("green control: real canon.css parses and classifies",
             stats["declared"] > 500 and stats["consumed"] > 0 and stats[ORPHAN] > 0,
             "declared=%d consumed=%d orphan=%d" % (stats["declared"], stats["consumed"],
                                                    stats[ORPHAN]))

        # ARM 2 — bite-the-bite: a var everything reads must NOT be classed at all.
        live = "--border-radius-default"
        bite("a heavily-consumed var (%s) is not flagged" % live, live not in classed,
             classed.get(live, ("(absent)",))[0])

        # ARM 3 — PLANT an orphan into a real theme block. MUST be detected BY NAME.
        _plant(canon, "--gate-selftest-orphan: #123456;")
        _d, _u, classed, stats = run(canon, REPO, themes, quiet=True)
        got = classed.get("--gate-selftest-orphan")
        bite("plant --gate-selftest-orphan in a console block -> ORPHAN",
             bool(got) and got[0] == ORPHAN, got[0] if got else "NOT DETECTED")

        # ARM 4 — same name, now CONSUMED from inside the glob. MUST NOT be flagged.
        consumer_dir = os.path.join(tmp, "knowledge", "snippets")
        os.makedirs(consumer_dir, exist_ok=True)
        open(os.path.join(consumer_dir, "Selftest.reference.html"), "w").write(
            "<style>.x{color:var(--gate-selftest-orphan);}</style>")
        _d, _u, classed, stats = run(canon, tmp, themes, quiet=True)
        bite("same name, now var()-ed by a file in the glob -> not flagged",
             "--gate-selftest-orphan" not in classed,
             classed.get("--gate-selftest-orphan", ("(absent)",))[0])

        # ARM 5 — the consumer moved into reviews/: EXCLUDED, so it flags again. Proves the
        # glob is real and not decorative.
        os.makedirs(os.path.join(tmp, "reviews"), exist_ok=True)
        shutil.move(os.path.join(consumer_dir, "Selftest.reference.html"),
                    os.path.join(tmp, "reviews", "Selftest.html"))
        _d, _u, classed, stats = run(canon, tmp, themes, quiet=True)
        got = classed.get("--gate-selftest-orphan")
        bite("consumer moved to reviews/ (excluded) -> ORPHAN again",
             bool(got) and got[0] == ORPHAN, got[0] if got else "NOT DETECTED")

        # ARM 6 — FALSE-POSITIVE CLASS 1 EXCLUDED: an $alias target is ALIAS-TARGET, not ORPHAN.
        fp = "--color-neutral-15"
        _d, _u, classed, stats = run(canon, REPO, themes, quiet=True)
        got = classed.get(fp)
        bite("$alias target %s classed ALIAS-TARGET, not ORPHAN" % fp,
             bool(got) and got[0] == ALIAS_TARGET, got[0] if got else "NOT CLASSED AT ALL")

        # ARM 7 — MUTANT: disable the $alias subtraction. The SAME var MUST go red as ORPHAN —
        # proves the subtraction is load-bearing and not a decorative branch.
        _d, _u, mclassed, _s = run(canon, REPO, themes, subtract_alias_targets=False, quiet=True)
        got = mclassed.get(fp)
        bite("MUTANT subtract_alias_targets=False -> %s goes ORPHAN" % fp,
             bool(got) and got[0] == ORPHAN, got[0] if got else "NOT CLASSED")

        # ARM 8 — FALSE-POSITIVE CLASS 2 EXCLUDED + its own mutant, in one arm.
        shadow = "--tooltip-background"
        _d, _u, classed, _s = run(canon, REPO, themes, quiet=True)
        _d, _u, mclassed, _s = run(canon, REPO, themes, subtract_alias_shadows=False, quiet=True)
        a = classed.get(shadow)
        b = mclassed.get(shadow)
        bite("%s ALIAS-SHADOW, and ORPHAN under the mutant" % shadow,
             bool(a) and a[0] == ALIAS_SHADOW and bool(b) and b[0] == ORPHAN,
             "%s / mutant %s" % (a[0] if a else "?", b[0] if b else "?"))

        # ARM 9 — missing canon.css must ERROR, never silently pass.
        try:
            run(os.path.join(tmp, "knowledge", "canon", "NOPE.css"), REPO, themes, quiet=True)
            bite("missing canon.css -> ran anyway", False)
        except GateError as exc:
            bite("missing canon.css -> GateError", True, str(exc)[:52])

        # ARM 10 — an EMPTY consumer population must ERROR. A gate with nothing to scan
        # cannot fail, and that is not a pass [[instrument-without-a-consumer]].
        empty = os.path.join(tmp, "empty")
        os.makedirs(empty, exist_ok=True)
        try:
            run(canon, empty, themes, quiet=True)
            bite("empty consumer population -> ran anyway", False)
        except GateError as exc:
            bite("empty consumer population -> GateError", True, str(exc)[:52])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%s (%d bites)" % ("✅ selftest PASS — the inventory can flag, can stop flagging, and "
                               "both false-positive subtractions are mutation-proved"
                               if ok else "❌ selftest FAIL", n[0]))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    try:
        _decls, _used, _classed, _stats = run(quiet=True)
        report(_classed, _stats, listing="--orphans" in sys.argv)
    except GateError as exc:
        print("❌ minted-consumption inventory could not run: %s" % exc)
        sys.exit(2)
    # ADVISORY: orphans are REPORTED, never gated. Promotion is Dave's (see the docstring).
    sys.exit(0)
