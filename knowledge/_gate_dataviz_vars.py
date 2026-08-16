#!/usr/bin/env python3
"""_gate_dataviz_vars.py — the chart var-resolution gate (ds-0NN, priced #184, built #190).

THE CLASS (MEASURED, not reasoned — #184 mutation drive, `s184-D3`):
a `rect` carrying `fill="var(--status-breach)"` with **no declaration of `--status-breach`
anywhere** paints BLACK and was reported as a pass by **thirteen of thirteen** gates. Black
is a plausible chart colour, so the defect has no visible signature to a reader who was not
looking for it. The exact shape is what a half-finished rename leaves behind.

WHY THE EXISTING C2 GATE CANNOT SEE IT — the join that nothing made.
`_validate_property_resolves.py` scans `<style>` blocks and `style=""` attributes. A chart's
colours do not live there: they live in SVG **presentation attributes** (`fill=`, `stroke=`).
C2 reads a snippet's DECLARATIONS and a snippet's `<style>` USES; it never reads the uses that
sit in markup. Same class as ds-039: no gate parses the artefact in the consumer's grammar
[[no-gate-parses-the-artefact]]. This gate parses the markup.

WHAT IT DOES
  1. collects every `var(--x)` inside a colour-bearing SVG presentation attribute
  2. resolves `--x` per THEME (mono · legacy · console · supercharge), following alias
     chains transitively, against: the file's own <style>/inline CSS, every stylesheet it
     actually <link>s, and canon.css (base block + that theme's `[data-apollo-theme]` block)
  3. FAILS LOUD AND NAMED on any reference that resolves in NO theme — file:line, the var
     name, and the literal attribute text are printed. Exit 1.
  4. WARNS (never exits non-zero) on a reference that resolves in SOME themes but not all —
     that is a per-theme hole, reported as a measurement, not prescribed away.

★ WHAT THIS GATE CAN AND CANNOT SEE (published, not buried — [[gate-narrows-its-own-rule]])
  CAN see   a colour presentation attribute naming a custom property declared NOWHERE the
            file can reach, in any theme. That is exactly the #184 shape.
  CAN see   a broken ALIAS CHAIN: `fill="var(--a)"` where `--a: var(--b)` and `--b` is
            declared nowhere. C2's declared/used split cannot join those either.
  CANNOT    per-SELECTOR scope. Declared in the file ⇒ counted as reachable. Catching a
  see       selector-scope miss needs a render, and belongs with render-verify.
  CANNOT    anything a JS string builds at runtime (`el.setAttribute('fill', ...)`).
  see       `<script>` bodies are skipped deliberately, like C2 skips behaviour blocks.
  CANNOT    a var that resolves to the WRONG colour. Presence of resolution only.
  see
  ⚠ A green run means "no markup-level unresolvable colour reference in the glob". It does
    NOT mean the charts are right.

GLOB — this gate rules only as wide as this list [[gate-glob-scope-rule]]:
    knowledge/snippets/*.reference.html
    knowledge/snippets/DataViz-interactive.html
    knowledge/_proforma/*.html
Widening it is a visible edit to GLOBS, never an inference.

WARN-vs-BLOCK: the canon entry says "FAIL LOUD on an unresolvable name", so nowhere-resolving
is exit 1. The partial-theme WARN tier is a BUILDER'S PICK, not a ruling — Dave may make it
bite. Wiring in `_build_all.py` is NON-BLOCKING (advisory); making it blocking is Dave's.

CONSUMER: `_build_all.py` gate chain (advisory tier). Run standalone:
    python3 knowledge/_gate_dataviz_vars.py            # gate  (exit 1 on unresolvable)
    python3 knowledge/_gate_dataviz_vars.py --selftest # plant-then-detect arms + controls
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
import shutil
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)

GLOBS = [
    "knowledge/snippets/*.reference.html",
    "knowledge/snippets/DataViz-interactive.html",
    "knowledge/_proforma/*.html",
]

CANON = os.path.join(ROOT, "canon", "canon.css")

# The four themes. Mono is the BASE (no [data-apollo-theme] block of its own); the other
# three are override blocks in canon.css. Source of truth: tokens/themes/_themes.json `attr`.
THEMES = ["mono", "legacy", "console", "supercharge"]

# Colour-bearing SVG presentation attributes. Only these — a `class="var(--x)"` is not a
# colour reference, and widening this set is a visible edit.
COLOUR_ATTRS = ("fill", "stroke", "stop-color", "flood-color", "lighting-color", "color")

STYLE_RE   = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT_RE  = re.compile(r"<script[^>]*>.*?</script>", re.S | re.I)
LINK_RE    = re.compile(r"""<link[^>]+rel=["']stylesheet["'][^>]*>""", re.I)
HREF_RE    = re.compile(r"""href=["']([^"']+)["']""", re.I)
INLINE_RE  = re.compile(r"""\sstyle=["']([^"']*)["']""", re.I)
DECL_RE    = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]*)")
USE_RE     = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*([,)])")
ATTR_RE    = re.compile(
    r"""\b(%s)\s*=\s*(["'])(.*?)\2""" % "|".join(COLOUR_ATTRS), re.I | re.S)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


class GateError(RuntimeError):
    """Unreadable / missing target. A crash is not a fail — this is raised, named, exit 2."""


def _strip_comments(css):
    return COMMENT_RE.sub(" ", css)


def _theme_of(selector):
    """Which theme a rule's declarations belong to. None => base (reachable in all themes)."""
    for t in THEMES[1:]:
        if 'data-apollo-theme="%s"' % t in selector or "data-apollo-theme='%s'" % t in selector:
            return t
    return None


def parse_css_by_theme(css):
    """{theme_or_None: {name: value}} — a brace scanner, so @media/@supports nest safely."""
    css = _strip_comments(css)
    out = {None: {}}
    for t in THEMES[1:]:
        out[t] = {}
    stack, buf, i, n = [], [], 0, len(css)
    while i < n:
        c = css[i]
        if c == "{":
            stack.append("".join(buf).strip())
            buf = []
        elif c == "}":
            body = "".join(buf)
            sel = " ".join(stack)
            for name, value in DECL_RE.findall(body):
                out.setdefault(_theme_of(sel), {})[name] = value.strip()
            buf = []
            if stack:
                stack.pop()
        else:
            buf.append(c)
        i += 1
    # a trailing unclosed block still surrenders its declarations
    if buf:
        sel = " ".join(stack)
        for name, value in DECL_RE.findall("".join(buf)):
            out.setdefault(_theme_of(sel), {})[name] = value.strip()
    return out


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise GateError("UNREADABLE TARGET %s — %s" % (path, exc))


def file_declarations(path, text):
    """Declarations a document can reach: own <style>, own style="", every <link> it makes."""
    css, linked = [], []
    for m in STYLE_RE.finditer(text):
        css.append(m.group(1))
    for m in INLINE_RE.finditer(text):
        css.append(m.group(1))
    for tag in LINK_RE.findall(text):
        href = HREF_RE.search(tag)
        if not href:
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), href.group(1)))
        if os.path.isfile(target):
            css.append(_read(target))
            linked.append(os.path.relpath(target, REPO))
        else:
            # a <link> that 404s is its own defect — surface it, never swallow it
            linked.append("MISSING:" + href.group(1))
    return parse_css_by_theme("\n".join(css)), linked


def merge(a, b):
    out = {k: dict(v) for k, v in a.items()}
    for k, v in b.items():
        out.setdefault(k, {}).update(v)
    return out


def resolves(name, decls, theme, seen=None):
    """Does --name bottom out in THEME? Follows alias chains; a fallback counts as safe."""
    seen = seen or set()
    if name in seen:
        return False           # a cycle resolves to nothing
    seen = seen | {name}
    value = decls.get(theme, {}).get(name)
    if value is None:
        value = decls.get(None, {}).get(name)
    if value is None:
        return False
    refs = USE_RE.findall(value)
    if not refs:
        return True
    for ref, delim in refs:
        if delim == ",":       # var(--x, fallback) always paints something
            continue
        if not resolves(ref, decls, theme, seen):
            return False
    return True


def attr_uses(text):
    """(line, attr, literal, varname) for every colour presentation attribute reference."""
    scrubbed = SCRIPT_RE.sub(lambda m: " " * len(m.group(0)), text)
    scrubbed = HTML_COMMENT_RE.sub(lambda m: " " * len(m.group(0)), scrubbed)
    hits = []
    for m in ATTR_RE.finditer(scrubbed):
        literal = m.group(0)
        line = scrubbed.count("\n", 0, m.start()) + 1
        for name, delim in USE_RE.findall(m.group(3)):
            if delim == ",":
                continue       # explicit fallback — cannot paint the initial value
            hits.append((line, m.group(1), literal.strip(), name))
    return hits


def run(globs=None, canon_path=None, root=None, quiet=False):
    """Returns (dead, partial, scanned, refs). Raises GateError on an unreadable target."""
    root = root or REPO
    canon_path = canon_path or CANON
    if not os.path.isfile(canon_path):
        raise GateError("MISSING TARGET canon.css at %s — refusing to run a gate blind" % canon_path)
    canon_decls = parse_css_by_theme(_read(canon_path))

    files = []
    for g in (globs or GLOBS):
        files.extend(sorted(glob.glob(os.path.join(root, g))))
    if not files:
        raise GateError("EMPTY POPULATION — globs %s matched no files under %s "
                        "(a gate with nothing to scan cannot fail; that is not a pass)"
                        % (globs or GLOBS, root))

    dead, partial, refs, scanned = [], [], 0, 0
    for path in files:
        text = _read(path)
        uses = attr_uses(text)
        if not uses:
            continue
        scanned += 1
        decls, _linked = file_declarations(path, text)
        decls = merge(canon_decls, decls)
        for line, attr, literal, name in uses:
            refs += 1
            ok = [t for t in THEMES if resolves(name, decls, t)]
            rel = os.path.relpath(path, root)
            if not ok:
                dead.append((rel, line, attr, name, literal))
            elif len(ok) != len(THEMES):
                partial.append((rel, line, attr, name, literal, ok))
    if not quiet:
        report(dead, partial, scanned, refs)
    return dead, partial, scanned, refs


def report(dead, partial, scanned, refs):
    print("dataviz var-resolution gate — %d file(s) with colour presentation attributes, "
          "%d reference(s), %d theme(s): %s" % (scanned, refs, len(THEMES), ", ".join(THEMES)))
    for rel, line, attr, name, literal, ok in partial:
        print("  ⚠ WARN  %s:%d  %s resolves only in %s — %s"
              % (rel, line, name, "+".join(ok), literal[:120]))
    for rel, line, attr, name, literal in dead:
        print("  ❌ DEAD  %s:%d  %s resolves in NO theme (renders SILENT BLACK) — %s"
              % (rel, line, name, literal[:120]))
    if dead:
        print("\n❌ %d unresolvable colour reference(s). CSS does not fall back: the "
              "declaration is invalid-at-computed-value-time and the attribute paints its "
              "initial value — black. Declare the name, or fix the rename that dropped it."
              % len(dead))
    else:
        print("✅ every colour presentation attribute resolves in at least one theme"
              + (" (%d partial-theme warning(s) above)" % len(partial) if partial else ""))


# ---------------------------------------------------------------- selftest
def _selftest():
    """Plant-then-detect on a REAL snippet copy. Every arm drives the gate, not a helper."""
    ok = True
    tmp = tempfile.mkdtemp(prefix="dvvars-")
    try:
        work = os.path.join(tmp, "knowledge")
        os.makedirs(os.path.join(work, "snippets"))
        shutil.copytree(os.path.join(ROOT, "canon"), os.path.join(work, "canon"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        src = os.path.join(ROOT, "snippets", "Chart-bar.reference.html")
        dst = os.path.join(work, "snippets", "Chart-bar.reference.html")
        shutil.copyfile(src, dst)
        g = ["knowledge/snippets/*.reference.html"]
        canon = os.path.join(work, "canon", "canon.css")

        # ARM 1 — green control: the real file, untouched, must be clean.
        dead, partial, scanned, refs = run(g, canon, tmp, quiet=True)
        good = (not dead) and scanned == 1 and refs > 0
        print("  [1] green control (real Chart-bar, %d refs) -> %d dead : %s"
              % (refs, len(dead), "PASS" if good else "FAIL"))
        ok &= good

        # ARM 2 — plant an UNDECLARED var in a fill attribute. MUST bite.
        text = _read(dst)
        planted = text.replace('fill="var(--', 'fill="var(--gate-selftest-ghost)" data-x="var(--', 1)
        open(dst, "w").write(planted)
        dead, _p, _s, _r = run(g, canon, tmp, quiet=True)
        good = any(n == "--gate-selftest-ghost" for _f, _l, _a, n, _lit in dead)
        print("  [2] plant undeclared --gate-selftest-ghost -> %d dead %s : %s"
              % (len(dead), [d[3] for d in dead], "PASS" if good else "FAIL"))
        ok &= good

        # ARM 3 — bite-the-bite: same shape but DECLARED. MUST NOT bite (guards always-true).
        open(dst, "w").write(planted.replace(
            "<style>", "<style>:root{--gate-selftest-ghost:#123456}", 1))
        dead, _p, _s, _r = run(g, canon, tmp, quiet=True)
        good = not any(n == "--gate-selftest-ghost" for _f, _l, _a, n, _lit in dead)
        print("  [3] same name, now DECLARED -> %d dead : %s"
              % (len(dead), "PASS" if good else "FAIL"))
        ok &= good

        # ARM 4 — broken ALIAS CHAIN: declared, but its value points nowhere. MUST bite.
        open(dst, "w").write(planted.replace(
            "<style>", "<style>:root{--gate-selftest-ghost:var(--gate-selftest-void)}", 1))
        dead, _p, _s, _r = run(g, canon, tmp, quiet=True)
        good = any(n == "--gate-selftest-ghost" for _f, _l, _a, n, _lit in dead)
        print("  [4] alias chain --ghost -> --void (undeclared) -> %d dead : %s"
              % (len(dead), "PASS" if good else "FAIL"))
        ok &= good

        # ARM 5 — theme-partial: declared ONLY inside a console block. WARN, never DEAD.
        open(dst, "w").write(planted.replace(
            "<style>", '<style>[data-apollo-theme="console"]{--gate-selftest-ghost:#123456}', 1))
        dead, partial, _s, _r = run(g, canon, tmp, quiet=True)
        good = (not any(n == "--gate-selftest-ghost" for _f, _l, _a, n, _lit in dead)
                and any(p[3] == "--gate-selftest-ghost" and p[5] == ["console"] for p in partial))
        print("  [5] declared in console block only -> partial=%s : %s"
              % ([(p[3], p[5]) for p in partial], "PASS" if good else "FAIL"))
        ok &= good

        # ARM 6 — fallback is safe: var(--void, #ccc) paints. MUST NOT bite.
        open(dst, "w").write(text.replace(
            'fill="var(--', 'fill="var(--gate-selftest-void, #cccccc)" data-x="var(--', 1))
        dead, _p, _s, _r = run(g, canon, tmp, quiet=True)
        good = not any(n == "--gate-selftest-void" for _f, _l, _a, n, _lit in dead)
        print("  [6] var(--void, #ccc) fallback -> %d dead : %s"
              % (len(dead), "PASS" if good else "FAIL"))
        ok &= good

        # ARM 7 — MISSING target must ERROR, never silently skip.
        os.remove(dst)
        try:
            run(g, canon, tmp, quiet=True)
            print("  [7] empty population -> ran anyway : FAIL")
            ok = False
        except GateError as e:
            print("  [7] empty population -> GateError: %s : PASS" % str(e)[:60])

        # ARM 8 — missing canon.css must ERROR, never silently skip.
        shutil.copyfile(src, dst)
        try:
            run(g, os.path.join(work, "canon", "NOPE.css"), tmp, quiet=True)
            print("  [8] missing canon.css -> ran anyway : FAIL")
            ok = False
        except GateError as e:
            print("  [8] missing canon.css -> GateError: %s : PASS" % str(e)[:60])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%s" % ("✅ selftest PASS — the gate can fail, and fails on the right shapes"
                    if ok else "❌ selftest FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    try:
        dead, partial, scanned, refs = run()
    except GateError as exc:
        print("❌ dataviz var-resolution gate could not run: %s" % exc)
        sys.exit(2)
    sys.exit(1 if dead else 0)
