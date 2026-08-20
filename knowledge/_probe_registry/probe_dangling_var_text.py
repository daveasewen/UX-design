#!/usr/bin/env python3
"""probe_dangling_var_text.py — P-8: `var(--x)` WITH `--x` DECLARED NOWHERE REACHABLE (W-45 registry).

THE CLASS: a rule reads a custom property the file never declares. CSS does not error — the
declaration is INVALID AT COMPUTED-VALUE TIME, so the property falls back to `inherit` or to its
initial value. Sometimes that is BLACK; sometimes it is *the right answer by accident*, which is
worse, because then nothing visible can ever show it.

  · #184 `knowledge/_DS-IMPROVEMENTS.md:1973` — a `<rect fill="var(--status-breach)"` with the
    property declared nowhere painted PURE BLACK and was reported a PASS by thirteen of thirteen
    gates. [[dangling-dataviz-var-renders-silent-black]]
  · #210 wave-6 lane B, `notes/_receipts/2026-08-20-210-wave6-laneB-p3-templates.md:151` —
    "`--muted` DANGLED IN TWO FILES AND **NOTHING VISIBLE COULD EVER HAVE SHOWN IT**": two
    templates borrowed Confirmation's `color:var(--muted)` and never declared `--muted`, so the
    colour fell to `inherit` — and `--muted` is text/secondary, which in Mono is the SAME HEX as
    text/default. Invisible by construction. Repaired by declaring it in both theme blocks.

P-3 asks this question FROM PIXELS and needs a browser. This probe asks it FROM TEXT, in the
sandbox, over the whole snippet library — the cheap tier that runs everywhere, per the #173
environment split.

WHAT THIS PROBE DOES, per file:
  1. collects the EXTERNAL VOCABULARY by PARSING every `<link rel=stylesheet>` the file actually
     carries, resolved relative to the file (measured today: `../canon/type.css`, which declares
     `--uf/--cap/--desc/--slot`). ⛔ The allowlist is READ FROM THE STYLESHEET, never hand-typed —
     a typed allowlist is a carried figure and rots [[premise-ages-faster-than-rule]].
  2. collects every custom-property DECLARATION reachable in the file — deliberately BROADLY:
     any `--x:` in the ACTIVE document (all `<style>` blocks including the AUTO-TOKENS block,
     inline `style="--x:…"`, and `element.style.setProperty('--x', …)` in scripts). Broad
     collection means fewer FALSE POSITIVES, which is the trade this probe is tuned for.
  3. collects every `var(--x)` REFERENCE from the NARROW scope: `<style>` blocks and inline
     `style` attributes only.
  4. flags a reference with NO declaration AND NO FALLBACK. `var(--x, #fff)` is exempt: a
     fallback is the author saying out loud that the property may be absent.

⛔ HTML COMMENTS ARE BLANKED BEFORE ANYTHING IS COLLECTED, and that is not a detail — it is how
this probe found its first live catch. A declaration sitting inside `<!-- … -->` is not CSS. When
a flagged property IS declared, but only inside a commented-out region, the finding says
`COMMENTED-OUT` rather than `ABSENT`, because the repair is completely different.

GLOB — this probe rules only as wide as this list [[gate-glob-scope-rule]]:
    knowledge/snippets/*.reference.html
Widen with `--glob '<pattern>'` (repeatable); widening is a visible argument, never an inference.

⛔ WHAT IT CANNOT SEE:
  · CASCADE. It asks "is this name declared ANYWHERE in the file", not "is it declared on an
    ancestor of the element that reads it". A `--x` declared on `.a` and read on an unrelated
    `.b` is dangling AT RUNTIME and this probe calls it clean. That is P-3's job (pixels) and
    `_gate_dataviz_vars.py`'s (per-selector scope) — this is the cheapest tier, not the best one.
  · a var that resolves to the WRONG value · a var declared but never read (dead, not dangling)
  · properties injected by a stylesheet this file does not `<link>`, or by script from another
    file, or by a `@property` descriptor in a sheet outside the resolved links
  · a reference built by string concatenation in JS · anything outside the glob.

ENVIRONMENT: sandbox (pure python, CSS text — no browser).

USAGE
  python3 knowledge/_probe_registry/probe_dangling_var_text.py --check
  python3 knowledge/_probe_registry/probe_dangling_var_text.py --check --glob 'reviews/*.html'
  python3 knowledge/_probe_registry/probe_dangling_var_text.py --selftest
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
DEFAULT_GLOBS = ["knowledge/snippets/*.reference.html"]

STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
INLINE_STYLE_RE = re.compile(r"""\sstyle\s*=\s*(["'])(.*?)\1""", re.S)
LINK_RE = re.compile(r"""<link\b[^>]*\bhref\s*=\s*["']([^"']+\.css)["'][^>]*>""", re.I)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
DECL_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")
SETPROP_RE = re.compile(r"""setProperty\(\s*["'](--[A-Za-z0-9_-]+)["']""")
VAR_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")


def _blank(pattern, text):
    """Erase matches but KEEP newlines — line numbers stay honest."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def declarations_in(css_text):
    return set(DECL_RE.findall(_blank(CSS_COMMENT_RE, css_text)))


def external_vocabulary(path, raw):
    """PARSE every linked stylesheet this file actually carries. Returns (names, sources).
    A link that does not resolve on disk is REPORTED, never silently treated as empty."""
    names, sources, missing = set(), [], []
    base = os.path.dirname(os.path.abspath(path))
    for href in LINK_RE.findall(_blank(HTML_COMMENT_RE, raw)):
        if "://" in href:
            missing.append(href + " (remote — not parsed)")
            continue
        target = os.path.normpath(os.path.join(base, href))
        if not os.path.exists(target):
            missing.append(href)
            continue
        names |= declarations_in(open(target, encoding="utf-8", errors="replace").read())
        sources.append(os.path.relpath(target, ROOT))
    return names, sources, missing


def var_refs(text):
    """[(name, has_fallback, line)] — each `var(` scanned independently, so a var nested inside
    another var's fallback gets its own honest verdict."""
    out = []
    for m in VAR_RE.finditer(text):
        i, depth, fallback = m.end(), 1, False
        while i < len(text) and depth:
            c = text[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == "," and depth == 1:
                fallback = True
                break
            i += 1
        out.append((m.group(1), fallback, text.count("\n", 0, m.start()) + 1))
    return out


def scan_file(path):
    """(findings, stats) for one file."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    live = _blank(HTML_COMMENT_RE, raw)

    ext, ext_src, ext_missing = external_vocabulary(path, raw)
    declared = declarations_in(live) | set(SETPROP_RE.findall(live))
    commented_only = declarations_in(
        "\n".join(m.group(0) for m in HTML_COMMENT_RE.finditer(raw))) - declared

    scope = "\n".join(STYLE_RE.findall(live))
    scope += "\n" + "\n".join(v for _q, v in INLINE_STYLE_RE.findall(live))
    scope = _blank(CSS_COMMENT_RE, scope)

    rel = os.path.relpath(path, ROOT)
    findings, refs = [], var_refs(scope)
    for name, fallback, line in refs:
        if fallback or name in declared or name in ext:
            continue
        # ⚠ `line` is the line WITHIN the concatenated <style>/inline scope, not the file — the
        # scope is stitched from several blocks. Reported as `style-scope line N` so it is never
        # misread as a file line [[measure-dont-convert-units]]: name the unit.
        where = "%s (style-scope line %d)" % (rel, line)
        if name in commented_only:
            findings.append((rel, "COMMENTED-OUT", name,
                             "%s `var(%s)` — %s IS declared in this file, but ONLY inside an "
                             "HTML comment, so it is not CSS and the reference dangles at "
                             "runtime" % (where, name, name)))
        else:
            findings.append((rel, "ABSENT", name,
                             "%s `var(%s)` — %s is declared nowhere reachable in this file (no "
                             "<style> block, no inline style, no setProperty, and not in the "
                             "linked stylesheet(s) %s) and the reference carries no fallback"
                             % (where, name, name, ext_src or "(none)")))
    stats = {"refs": len(refs), "declared": len(declared), "ext": len(ext),
             "ext_src": ext_src, "ext_missing": ext_missing}
    return findings, stats


def scan(paths, verbose=True):
    findings, missing_links = [], []
    for path in paths:
        f, st = scan_file(path)
        findings += f
        if st["ext_missing"]:
            missing_links.append((os.path.relpath(path, ROOT), st["ext_missing"]))
        if verbose and f:
            print("  ⛔ %-52s refs=%-4d declared=%-4d external=%-3d DANGLING=%d"
                  % (os.path.relpath(path, ROOT)[-52:], st["refs"], st["declared"],
                     st["ext"], len(f)))
    if verbose:
        for rel, kind, name, detail in findings:
            print("  ⛔ %s · %s · %s" % (rel, kind, detail))
        for rel, hrefs in missing_links:
            print("  ⚠ %s links stylesheet(s) that do not resolve on disk: %s — their "
                  "vocabulary could NOT be parsed and is NOT in the allowlist (declared, not "
                  "assumed empty)" % (rel, hrefs))
    return findings


def resolve(patterns, root=ROOT):
    out = []
    for pat in patterns:
        out += sorted(globmod.glob(os.path.join(root, pat)))
    return out


def check(patterns=None):
    patterns = patterns or DEFAULT_GLOBS
    paths = resolve(patterns)
    findings = scan(paths)
    by_kind = Counter(k for _r, k, _n, _d in findings)
    by_name = Counter(n for _r, _k, n, _d in findings)
    print("P-8 dangling-var TEXT scan: %d file(s) over %s · %d finding(s) in %d file(s) · "
          "by kind %s" % (len(paths), patterns, len(findings),
                          len({r for r, _k, _n, _d in findings}), dict(by_kind)))
    if findings:
        print("  distinct properties: %s" % dict(by_name))
    if not paths:
        print("⚠ THE GLOB MATCHED NOTHING — an empty population is not a pass "
              "(unmatched-grep-is-not-an-absence).")
        print("PROBE P-8 — findings=1")
        return 1
    print("PROBE P-8 — findings=%d" % len(findings))
    return 1 if findings else 0


def selftest():
    """PLANT-THEN-DETECT on a REAL snippet, and the PLANT IS VERIFIED TO HAVE PLANTED before any
    catch is asserted. ⛔ [[mutation-tests-the-clause-not-the-feature]] — a plant that never
    planted, followed by a green assert, is the blind-harness class this repo has paid for four
    times. Every arm below checks the PARSED STATE of the fixture first."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="p8-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))

    src = None
    for p in resolve(DEFAULT_GLOBS):
        f, st = scan_file(p)
        if not f and st["refs"] > 5 and st["ext"] and not st["ext_missing"]:
            src = p
            break
    if not src:
        print("⛔ selftest cannot run: no clean snippet with var() references AND a resolvable "
              "linked stylesheet to plant into (declared, never assumed).")
        return 1
    # ⛔ THE FIXTURE MUST KEEP ITS LINKS. A bare copy into a flat temp dir silently breaks
    # `href="../canon/type.css"`, the external vocabulary parses to EMPTY, and the allowlist arm
    # passes vacuously — the blind-harness shape again. So the relative link targets are
    # replicated beside the fixture and the replication is ASSERTED below, not assumed.
    workdir = os.path.join(tmp, os.path.basename(os.path.dirname(os.path.abspath(src))))
    os.makedirs(workdir, exist_ok=True)
    work = os.path.join(workdir, os.path.basename(src))
    shutil.copyfile(src, work)
    for href in LINK_RE.findall(open(src, encoding="utf-8", errors="replace").read()):
        if "://" in href:
            continue
        origin = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(src)), href))
        dest = os.path.normpath(os.path.join(workdir, href))
        if os.path.exists(origin):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(origin, dest)
    raw = open(work, encoding="utf-8", errors="replace").read()
    base, base_st = scan_file(work)
    print("  · fixture %s — refs=%d declared=%d external=%d from %s · baseline findings=%d"
          % (os.path.basename(src), base_st["refs"], base_st["declared"], base_st["ext"],
             base_st["ext_src"], len(base)))
    if not base_st["ext"]:
        fails.append("ALLOWLIST EMPTY: the external vocabulary parsed from %s is empty — the "
                     "allowlist arm below would pass vacuously" % base_st["ext_src"])
    else:
        print("  ✅ allowlist was BUILT BY PARSING, not typed: %d name(s) from %s"
              % (base_st["ext"], base_st["ext_src"]))

    live = _blank(HTML_COMMENT_RE, raw)
    m = list(STYLE_RE.finditer(live))
    if not m:
        print("⛔ selftest cannot run: the fixture has no live <style> block to plant into.")
        return 1
    end = m[-1].end(1)

    def plant_and_scan(css):
        open(work, "w", encoding="utf-8").write(raw[:end] + css + raw[end:])
        f, _st = scan_file(work)
        scope = "\n".join(STYLE_RE.findall(_blank(HTML_COMMENT_RE,
                          open(work, encoding="utf-8").read())))
        return f, {n for n, _fb, _l in var_refs(_blank(CSS_COMMENT_RE, scope))}

    # ---- ARM 1: a bare dangling reference must be SEEN by the parser, then must BITE.
    f1, seen1 = plant_and_scan("\n.p8-selftest{ color:var(--p8-selftest-nope); }\n")
    print("  · PLANT VERIFICATION — fixture re-parsed: `--p8-selftest-nope` present in the "
          "collected var() references = %s" % ("--p8-selftest-nope" in seen1))
    if "--p8-selftest-nope" not in seen1:
        fails.append("THE PLANT DID NOT PLANT: the reference is not in the parsed reference set "
                     "— any 'catch' below would be a blind harness")
    new = [x for x in f1 if x not in base]
    if not [x for x in new if x[2] == "--p8-selftest-nope" and x[1] == "ABSENT"]:
        fails.append("PLANT NOT CAUGHT: a verified dangling `var(--p8-selftest-nope)` produced "
                     "no ABSENT finding (got %r)" % new)
    else:
        print("  ✅ plant caught (ABSENT): %s" % new[0][3][:100])

    # ---- ARM 2: HEAL. Declare the property in the same file — the probe must go quiet.
    f2, seen2 = plant_and_scan("\n.p8-selftest{ --p8-selftest-nope:#123456; "
                               "color:var(--p8-selftest-nope); }\n")
    if "--p8-selftest-nope" not in seen2:
        fails.append("HEAL ARM DID NOT PLANT: the reference vanished from the fixture entirely, "
                     "so its silence proves nothing")
    elif [x for x in f2 if x not in base]:
        fails.append("HEAL NOT GREEN: declaring the property in the same file left %d finding(s)"
                     % len([x for x in f2 if x not in base]))
    else:
        print("  ✅ heal green: the SAME reference, with `--p8-selftest-nope` declared beside "
              "it, is silent — the probe reacts to the declaration, not to the name")

    # ---- ARM 3: REMOVAL. Restore the pristine file, back to baseline.
    shutil.copyfile(src, work)
    f3, _st = scan_file(work)
    if f3 != base:
        fails.append("REMOVAL NOT GREEN: restored fixture gave %d finding(s), baseline %d"
                     % (len(f3), len(base)))
    else:
        print("  ✅ removal green: the restored fixture returns to baseline (%d)" % len(base))

    # ---- ARM 4: FALLBACK CONTROL. `var(--x, …)` is the author saying it may be absent.
    f4, seen4 = plant_and_scan("\n.p8-selftest{ color:var(--p8-selftest-fb, #fff); }\n")
    if "--p8-selftest-fb" not in seen4:
        fails.append("FALLBACK ARM DID NOT PLANT: the reference is not in the parsed set")
    elif [x for x in f4 if x not in base]:
        fails.append("FALLBACK LEAKED: `var(--x, #fff)` was flagged — a declared fallback is an "
                     "explicit contract, not a defect")
    else:
        print("  ✅ fallback control: `var(--p8-selftest-fb, #fff)` is NOT a finding")

    # ---- ARM 5: EXTERNAL VOCABULARY. A name the LINKED stylesheet declares must not fire.
    ext_name = sorted(external_vocabulary(work, raw)[0])[0] if base_st["ext"] else None
    if ext_name:
        f5, seen5 = plant_and_scan("\n.p8-selftest{ font-family:var(%s); }\n" % ext_name)
        if ext_name not in seen5:
            fails.append("EXTERNAL ARM DID NOT PLANT: %s is not in the parsed set" % ext_name)
        elif [x for x in f5 if x not in base]:
            fails.append("ALLOWLIST FAILED: `var(%s)`, declared in the LINKED stylesheet, was "
                         "flagged — canon-provided vocabulary is legal" % ext_name)
        else:
            print("  ✅ external vocabulary: `var(%s)`, parsed out of %s, is NOT a finding"
                  % (ext_name, base_st["ext_src"]))

    # ---- ARM 6: THE COMMENTED-OUT SHAPE — the #210 root cause, and it must be NAMED, not
    # merely counted. A declaration inside an HTML comment is not CSS.
    open(work, "w", encoding="utf-8").write(
        raw[:end] + "\n.p8-selftest{ color:var(--p8-selftest-hidden); }\n" + raw[end:]
        + "\n<!-- :root{ --p8-selftest-hidden:#654321; } -->\n")
    f6, _st6 = scan_file(work)
    hidden = [x for x in f6 if x[2] == "--p8-selftest-hidden"]
    if not hidden:
        fails.append("COMMENTED-OUT PLANT NOT CAUGHT: a declaration inside `<!-- -->` was "
                     "treated as live CSS — the exact defect this probe found at #210")
    elif hidden[0][1] != "COMMENTED-OUT":
        fails.append("COMMENTED-OUT MISLABELLED: reported as %r, not COMMENTED-OUT — the repair "
                     "for a commented-out declaration is not the repair for an absent one"
                     % hidden[0][1])
    else:
        print("  ✅ commented-out shape: a declaration living only inside `<!-- -->` is caught "
              "AND named COMMENTED-OUT, not ABSENT")

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-8 selftest: %d failure(s)" % len(fails))
        for x in fails:
            print("   " + x)
        return 1
    print("✅ P-8 selftest PASS — the plant was VERIFIED to have planted (parsed state, not "
          "assumed), it bit, declaring the property healed it, removal went green, fallbacks and "
          "the PARSED canon vocabulary stayed quiet, and the commented-out shape is named.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    pats = [argv[i + 1] for i, a in enumerate(argv) if a == "--glob"]
    sys.exit(check(pats or None))
