#!/usr/bin/env python3
"""_validate_token_forks.py - the FORK-BAN GATE (s136-D1 clause D), LANE 2.

WHAT IT FORBIDS
---------------
s136-D1 clause D: "the three axes are the only sanctioned variation; anything
off-axis is a fork and a gate failure."

The sanctioned axes for a CSS custom property, as they exist in this repo's
cascade, are:
  * THEME  - [data-apollo-theme="legacy"|"console"|"supercharge"], absent = mono
             (Dave's standing requirement, ds-035 / #108-D3: four themes and the
             flexibility to create more. Divergence ACROSS themes is the feature.)
  * MODE   - [data-theme="light"|"dark"] (plus @media context).

A FORK is therefore: one property NAME resolving to two or more DIFFERENT final
values INSIDE ONE (theme, mode) - i.e. the divergence is carried by component
scope (.cn-*) or some other selector, not by an axis. That is the --pri-hover
class: "a token NAME is not an ADDRESS" (#108).

Divergence across themes  -> BENIGN_THEME_AXIS.
Divergence across modes   -> BENIGN_MODE_AXIS.
No divergence             -> UNIFORM.
Divergence within a (theme, mode) -> FORK.

HOW IT PARSES - the consumer's grammar, not grep
------------------------------------------------
No gate may match names with a regex and call that a measurement. This one:
  1. strips /* */ comments, then walks the stylesheet character by character
     maintaining a brace-depth selector stack, so nested at-rules (@media,
     @supports, @container) carry context;
  2. records every custom-property DECLARATION with its full selector chain,
     at-rule context and 1-based line number;
  3. classifies each selector in a selector list into (theme, mode, scope);
  4. RESOLVES var() chains the way the browser does - substituting the value
     the same element would see, walking the fallback ladder
        (theme,mode,scope) -> (theme,any,scope) -> (theme,mode,ROOT)
        -> (theme,any,ROOT) -> (mono,mode,ROOT) -> (mono,any,ROOT)
     with cycle detection and a depth cap. A chain that cannot be resolved is
     reported as UNRESOLVED and is NEVER silently treated as equal to anything.
  5. compares FINAL RESOLVED VALUES, not declared text. `var(--a)` and `#BA1110`
     compare equal when --a is #BA1110.

WHAT IT REPORTS
---------------
Every fork is quoted: file:line for BOTH conflicting declarations, the selector
each sits under, the declared text and the resolved value. The gate reports the
measurement; it does not prescribe which side is right or which region to change.

GLOB AND WHY
------------
Default glob: knowledge/canon/*.css  (canon.css, type.css).
Reason: this is the generated, live cascade - the only artefact where two
declarations of one name are actually in the same document and therefore
actually compete. The rule is only as wide as this glob (gate-glob-scope-rule).
  * designer-skills-v1/ and -v2/ are RELEASE PACKS (frozen), deliberately out.
  * knowledge/snippets/*.reference.html each form their OWN document; a snippet
    declaration does not compete with canon's unless the snippet links canon.css,
    and #107 measured ZERO snippets that do. They are audited only under
    --collisions, and reported as CROSS_DOCUMENT (cannot bite today), never as
    an in-cascade fork.

DECLARED FORKS
--------------
A fork may be sanctioned by naming it in the ledger JSON (--ledger). Baseline
mode (default) fails only on forks that are NOT in the ledger; --strict fails on
every fork including ledgered ones. Ledger entries are a record of what Dave has
seen, not an excuse: nothing is added to it by this script.

USAGE
  python3 knowledge/_validate_token_forks.py              # gate, baseline mode
  python3 knowledge/_validate_token_forks.py --strict     # fail on all forks
  python3 knowledge/_validate_token_forks.py --json OUT   # write the measurement
  python3 knowledge/_validate_token_forks.py --collisions FILE [FILE...]
                                                          # collision verdicts
EXIT 0 clean, 1 forks found, 2 the gate itself failed (loud and named).
"""
import argparse
import glob as globmod
import json
import os
import re
import sys
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_GLOB = "knowledge/canon/*.css"
DEFAULT_LEDGER = "knowledge/_TOKEN-FORK-LEDGER.json"
MAX_DEPTH = 24


def fail(msg):
    print("FAIL _validate_token_forks.py: " + msg, file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------- parsing ----

def strip_comments(text):
    """Remove /* */ comments, preserving newlines so line numbers stay true."""
    out = []
    i, n = 0, len(text)
    while i < n:
        if text[i] == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            if j == -1:
                out.append("\n" * text.count("\n", i))
                break
            out.append("\n" * text.count("\n", i, j))
            i = j + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def parse_declarations(text, path):
    """Walk the stylesheet, yielding custom-property declarations in context.

    Returns list of dicts: selector, at_rules, prop, value, line.
    """
    src = strip_comments(text)
    decls = []
    stack = []          # list of (kind, text) where kind in {"sel", "at"}
    buf = []
    line = 1
    i, n = 0, len(src)
    while i < n:
        ch = src[i]
        if ch == "\n":
            line += 1
            buf.append(ch)
            i += 1
            continue
        if ch == "{":
            head = "".join(buf).strip()
            buf = []
            if head.startswith("@"):
                stack.append(("at", head))
            else:
                stack.append(("sel", head))
            i += 1
            continue
        if ch == "}":
            if not stack:
                fail("%s: unbalanced '}' at line %d" % (path, line))
            stack.pop()
            buf = []
            i += 1
            continue
        if ch == ";":
            decl = "".join(buf).strip()
            buf = []
            i += 1
            if decl.startswith("--") and ":" in decl:
                prop, _, value = decl.partition(":")
                sels = [k for kind, k in stack if kind == "sel"]
                ats = [k for kind, k in stack if kind == "at"]
                if not sels:
                    continue
                decls.append({
                    "file": path,
                    "line": line - decl.count("\n"),
                    "selector": " ".join(sels),
                    "at_rules": tuple(ats),
                    "prop": prop.strip(),
                    "value": value.strip(),
                })
            continue
        buf.append(ch)
        i += 1
    if stack:
        fail("%s: %d unclosed block(s) at EOF" % (path, len(stack)))
    return decls


# ------------------------------------------------------------- contexting ----

RE_APOLLO = re.compile(r'\[data-apollo-theme="([^"]+)"\]')
RE_MODE = re.compile(r'\[data-theme="([^"]+)"\]')
RE_CN = re.compile(r'\.(cn-[A-Za-z0-9_-]+)')


def context_of(selector_part):
    """(theme, mode, scope) for ONE selector out of a comma list."""
    m = RE_APOLLO.search(selector_part)
    theme = m.group(1) if m else "mono"
    m = RE_MODE.search(selector_part)
    mode = m.group(1) if m else "any"
    cns = RE_CN.findall(selector_part)
    if cns:
        scope = "." + cns[-1]
    else:
        bare = RE_APOLLO.sub("", RE_MODE.sub("", selector_part)).strip()
        bare = bare.replace(":root", "").strip()
        scope = "ROOT" if bare == "" else bare
    return theme, mode, scope


def split_selector_list(selector):
    return [s.strip() for s in selector.split(",") if s.strip()]


def build_index(decls):
    """(theme, mode, scope, prop) -> last declaration wins (source order)."""
    index = {}
    contexts = []
    for d in decls:
        for part in split_selector_list(d["selector"]):
            theme, mode, scope = context_of(part)
            key = (theme, mode, scope, d["prop"])
            rec = dict(d)
            rec["theme"], rec["mode"], rec["scope"] = theme, mode, scope
            rec["selector_part"] = part
            index[key] = rec
            contexts.append(rec)
    return index, contexts


# ------------------------------------------------------------- resolution ----

RE_VAR = re.compile(r'var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,([^()]*(?:\([^()]*\)[^()]*)*))?\)')


def lookup_ladder(theme, mode, scope):
    """The order a browser's cascade would consult, most specific first."""
    ladder = [(theme, mode, scope), (theme, "any", scope)]
    if scope != "ROOT":
        ladder += [(theme, mode, "ROOT"), (theme, "any", "ROOT")]
    if theme != "mono":
        ladder += [("mono", mode, scope), ("mono", "any", scope),
                   ("mono", mode, "ROOT"), ("mono", "any", "ROOT")]
    seen, out = set(), []
    for k in ladder:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


def resolve(value, theme, mode, scope, index, depth=0, seen=None):
    """Substitute var() chains as the element under (theme,mode,scope) sees them."""
    if depth > MAX_DEPTH:
        return "UNRESOLVED(depth>%d)" % MAX_DEPTH
    seen = set() if seen is None else seen
    out = value
    for _ in range(MAX_DEPTH):
        m = RE_VAR.search(out)
        if not m:
            break
        name, fallback = m.group(1), m.group(2)
        if name in seen:
            return "UNRESOLVED(cycle:%s)" % name
        hit = None
        for key in lookup_ladder(theme, mode, scope):
            cand = index.get(key + (name,))
            if cand is not None:
                hit = cand
                break
        if hit is not None:
            sub = resolve(hit["value"], theme, mode, scope, index,
                          depth + 1, seen | {name})
        elif fallback is not None:
            sub = resolve(fallback.strip(), theme, mode, scope, index,
                          depth + 1, seen | {name})
        else:
            sub = "UNRESOLVED(%s)" % name
        out = out[:m.start()] + sub + out[m.end():]
    return normalise(out)


def normalise(v):
    v = " ".join(v.split()).lower().rstrip(";").strip()
    m = re.fullmatch(r'#([0-9a-f])([0-9a-f])([0-9a-f])', v)
    if m:
        v = "#" + "".join(c * 2 for c in m.groups())
    return v


# ------------------------------------------------------------------ gate -----

def measure(index, contexts):
    """Per property name, per (theme,mode): distinct resolved values by scope."""
    by_prop = defaultdict(lambda: defaultdict(dict))  # prop -> (t,m) -> scope -> rec
    for rec in contexts:
        r = dict(rec)
        r["resolved"] = resolve(rec["value"], rec["theme"], rec["mode"],
                                rec["scope"], index)
        by_prop[rec["prop"]][(rec["theme"], rec["mode"])][rec["scope"]] = r
    forks, verdicts = [], {}
    for prop, groups in sorted(by_prop.items()):
        prop_forked = False
        for (theme, mode), scopes in sorted(groups.items()):
            vals = defaultdict(list)
            for scope, r in scopes.items():
                vals[r["resolved"]].append(r)
            if len(vals) > 1:
                prop_forked = True
                ordered = sorted(vals.items(), key=lambda kv: kv[1][0]["line"])
                a = ordered[0][1][0]
                for value_b, recs in ordered[1:]:
                    b = recs[0]
                    forks.append({
                        "prop": prop,
                        "theme": theme,
                        "mode": mode,
                        "a": quote(a),
                        "b": quote(b),
                    })
        distinct_across = {r["resolved"] for g in groups.values()
                           for r in g.values()}
        if prop_forked:
            verdict = "FORK"
        elif len(distinct_across) == 1:
            verdict = "UNIFORM"
        else:
            themes = {t for (t, m) in groups}
            modes = {m for (t, m) in groups}
            if len(themes) > 1 and len(modes) > 1:
                verdict = "BENIGN_THEME_AND_MODE_AXIS"
            elif len(themes) > 1:
                verdict = "BENIGN_THEME_AXIS"
            elif len(modes) > 1:
                verdict = "BENIGN_MODE_AXIS"
            else:
                verdict = "BENIGN_UNCLASSIFIED_AXIS"
        verdicts[prop] = {
            "verdict": verdict,
            "contexts": sum(len(s) for s in groups.values()),
            "distinct_resolved_values": len(distinct_across),
        }
    return forks, verdicts


def quote(r):
    return {
        "file_line": "%s:%d" % (r["file"], r["line"]),
        "selector": r["selector_part"],
        "theme": r["theme"], "mode": r["mode"], "scope": r["scope"],
        "declared": r["value"],
        "resolved": r["resolved"],
    }


def load_ledger(path):
    full = os.path.join(REPO, path)
    if not os.path.exists(full):
        return {}, False
    try:
        with open(full) as fh:
            data = json.load(fh)
    except Exception as exc:
        fail("ledger %s unreadable: %s" % (path, exc))
    entries = data.get("declared_forks")
    if not isinstance(entries, dict):
        fail("ledger %s has no 'declared_forks' object" % path)
    return entries, True


SELFTEST_CLEAN = """
:root { --brand: #DB0011; --pri-hover: var(--brand); }
[data-apollo-theme="legacy"] { --brand: #A8000B; }
.cn-button { --pri-hover: var(--brand); }
[data-apollo-theme="legacy"] .cn-button { --pri-hover: var(--brand); }
"""

SELFTEST_FORKED = """
:root { --brand: #DB0011; --pri-hover: var(--brand); }
[data-apollo-theme="legacy"] { --brand: #A8000B; }
.cn-button { --pri-hover: #626262; }
"""


def selftest():
    """Two bites, in memory, no repo bytes touched.

    1. clean sheet: --pri-hover resolves to #db0011 in mono and #a8000b in
       legacy -> BENIGN_THEME_AXIS, NOT a fork (the four-theme requirement).
    2. forked sheet: .cn-button disagrees with :root inside mono -> FORK.
    A green that cannot fail is an assertion, so both directions are driven.
    """
    ok = True
    for label, css, want in (("clean", SELFTEST_CLEAN, "BENIGN_THEME_AXIS"),
                             ("forked", SELFTEST_FORKED, "FORK")):
        decls = parse_declarations(css, "<selftest-%s>" % label)
        index, contexts = build_index(decls)
        forks, verdicts = measure(index, contexts)
        got = verdicts.get("--pri-hover", {}).get("verdict")
        good = got == want
        ok = ok and good
        print("  selftest %-6s --pri-hover -> %-18s want %-18s %s"
              % (label, got, want, "OK" if good else "FAIL"))
        if label == "forked" and forks:
            print("     quoted: %s vs %s"
                  % (forks[0]["a"]["resolved"], forks[0]["b"]["resolved"]))
    print("selftest %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--glob", default=DEFAULT_GLOB)
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--collisions", nargs="*")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    files = sorted(globmod.glob(os.path.join(REPO, args.glob)))
    if not files:
        fail("glob %s matched ZERO files - a gate with no subject cannot fail"
             % args.glob)

    decls = []
    for path in files:
        rel = os.path.relpath(path, REPO)
        with open(path) as fh:
            decls += parse_declarations(fh.read(), rel)
    if not decls:
        fail("parsed ZERO custom-property declarations from %d file(s)" % len(files))

    index, contexts = build_index(decls)
    forks, verdicts = measure(index, contexts)
    ledger, ledger_found = load_ledger(args.ledger)

    undeclared = [f for f in forks if f["prop"] not in ledger]
    reportable = forks if args.strict else undeclared

    print("_validate_token_forks.py - FORK-BAN GATE (s136-D1 clause D)")
    print("  glob      : %s  (%d file(s))" % (args.glob, len(files)))
    print("  parsed    : %d declarations, %d (theme,mode,scope) contexts"
          % (len(decls), len(contexts)))
    print("  names     : %d" % len(verdicts))
    tally = defaultdict(int)
    for v in verdicts.values():
        tally[v["verdict"]] += 1
    for k in sorted(tally):
        print("    %-28s %d" % (k, tally[k]))
    print("  ledger    : %s (%d declared fork(s))"
          % (args.ledger if ledger_found else args.ledger + " ABSENT", len(ledger)))
    print("  mode      : %s" % ("STRICT" if args.strict else "baseline"))

    for f in reportable:
        print("")
        print("FORK  %s  theme=%s mode=%s" % (f["prop"], f["theme"], f["mode"]))
        for side in ("a", "b"):
            q = f[side]
            print("   %s  %s" % (q["file_line"], q["selector"]))
            print("      %s: %s   ->  %s"
                  % (f["prop"], q["declared"], q["resolved"]))

    if args.collisions:
        collision_report(args.collisions, verdicts)

    if args.json_out:
        out = {
            "$id": "TOKEN-FORK-MEASUREMENT-2026-08-09-s139-v1",
            "$generated_by": "knowledge/_validate_token_forks.py",
            "$ruling": "s136-D1 clause D (fork ban)",
            "$glob": args.glob,
            "$axes_sanctioned": ["theme (data-apollo-theme)", "mode (data-theme)"],
            "summary": {
                "files": len(files),
                "declarations": len(decls),
                "contexts": len(contexts),
                "names": len(verdicts),
                "by_verdict": dict(sorted(tally.items())),
                "forks_total": len(forks),
                "forks_undeclared": len(undeclared),
            },
            "verdicts": verdicts,
            "forks": forks,
        }
        with open(os.path.join(REPO, args.json_out), "w") as fh:
            json.dump(out, fh, indent=1)
        print("\nwrote %s" % args.json_out)

    if reportable:
        print("\nGATE RED: %d fork(s)%s"
              % (len(reportable), "" if args.strict else " not in the ledger"))
        return 1
    print("\nGATE GREEN: no %sfork" % ("" if args.strict else "undeclared "))
    return 0


def collision_report(paths, canon_verdicts):
    """Names declared BOTH in the glob and in the named documents.

    These are CROSS_DOCUMENT: separate documents do not share a cascade, so they
    cannot fork today. Reported so the set is measured, not fixed.
    """
    print("\n--- COLLISION SET (cross-document, cannot bite unless linked) ---")
    files = []
    for p in paths:
        files += sorted(globmod.glob(os.path.join(REPO, p)))
    names = set()
    for path in files:
        with open(path) as fh:
            names |= set(re.findall(r'(--[A-Za-z0-9_-]+)\s*:', fh.read()))
    hit = sorted(names & set(canon_verdicts))
    print("documents=%d  names_declared=%d  colliding_with_glob=%d"
          % (len(files), len(names), len(hit)))
    tally = defaultdict(list)
    for n in hit:
        tally[canon_verdicts[n]["verdict"]].append(n)
    for k in sorted(tally):
        print("  %-28s %d" % (k, len(tally[k])))
    for k in sorted(tally):
        for n in tally[k]:
            print("    %-28s %s" % (n, k))


if __name__ == "__main__":
    sys.exit(main())
