#!/usr/bin/env python3
"""
_gate_fallback_drift_221.py — ⬛ ADVISORY AT BIRTH. Every `var(--token,#literal)` fallback a
generator authors must be a value CANON ITSELF RESOLVES for that token.

⛔ ADVISORY, AND IT SAYS SO IN ITS OWN HEADER. It is not in `_build_all.py` and not in
`gates.yml`. Promotion to blocking is DAVE'S WORD (derivation governance) — nothing here promotes
itself, and the exit code below is a report, not a build verdict, until he says otherwise.

WHY IT EXISTS (#221, from #220 audit L3 finding F-1)
  `s220-D1` built a genuinely new assertion — *"a fallback that has DRIFTED from canon is a red,
  in either direction"* — into ONE generator, as bite 12 of `gen_bento_matrix_217.py`. That bite
  reads only its own module's `rules` string. The page-chrome preamble it checks is copied,
  near-verbatim, into FOUR sibling generators, and there it was unchecked. Sixteen cause sites
  stood drifted across five files, including one FIVE LINES BELOW the s220-D1 repair in the very
  file that repair landed in: `--focus: var(--focus-ring,#1A1A1A)` — a BLACK focus ring where the
  ruled ring is `#305A85`/`#4587A7`, wrong in 8 of 8 theme x mode. [[gate-glob-scope-rule]]: the
  rule was only ever as wide as its gate's glob. This gate is the glob.

WHY IT MATTERS EVEN THOUGH NOTHING RENDERS IT TODAY
  Every shipped page `<link>`s `../knowledge/canon/canon.css`, so the fallback never fires and the
  generators say so out loud (*"the fallbacks are the fence"*). But a fence built out of values
  canon never produces fails SAFE-LOOKING: the day canon does not load — a pack export, a moved
  file, an offline copy, a designer opening a page outside the repo — the chrome paints the wrong
  border and a black focus ring, with no visible signature that anything is wrong.

THREE VERDICTS, AND THE THIRD IS THE ONE BITE 12 COULD NOT SAY
  DRIFTED       canon resolves the token, and the literal is not one of canon's answers.  -> RED
  LOCAL-DRIFT   a page-local alias is declared `--x: var(--canon,#A)` and consumed as
                `var(--x,#B)` with A != B — two colours behind one name.                  -> RED
  UNCHECKED     canon cannot resolve the token in ANY theme x mode, so NOTHING is compared.
                Bite 12 swallowed the `KeyError` and the row vanished silently; every radius,
                hit-area and ring-width fallback in this chrome (~40 sites) was therefore never
                compared to anything, and `0px` happening to be the house default is exactly the
                shape #204 measured as invisible. Here it is DECLARED, counted and printed.
                ⛔ A DECLARED HOLE, NOT A PASS — it does not turn the gate red, because a
                non-colour store is not wired into this resolver yet; that is priced, not done.
                [[unmatched-grep-is-not-an-absence]] / F-2 of the L3 audit.

RUN IT
  python3 knowledge/_render/_gate_fallback_drift_221.py            # the whole generator glob
  python3 knowledge/_render/_gate_fallback_drift_221.py --verbose  # every fallback, classified
  python3 knowledge/_render/_gate_fallback_drift_221.py --selftest # planted defect, both ways
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# ⛔ THE GLOB IS THE RULE. Widen this and the rule widens with it; narrow it and the rule silently
# stops being true of whatever fell out [[gate-glob-scope-rule]].
GLOB = os.path.join(HERE, "*.py")
THEMES = ("mono", "legacy", "console", "supercharge")
MODES = ("light", "dark")

FB_RE = re.compile(r"var\(\s*(--[a-z0-9-]+)\s*,\s*(#[0-9A-Fa-f]{6})\s*\)")
DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*var\(\s*--[a-z0-9-]+\s*,\s*(#[0-9A-Fa-f]{6})\s*\)")


def _resolver():
    """The repo's OWN resolver, never a private copy of the cascade. Refuses loudly if it cannot
    be imported — a gate that silently falls back to its own model of canon is measuring itself
    [[measuring-tool-must-not-guess]]."""
    import gen_bento_matrix_217 as M
    return M.resolve_token


_ANSWER_CACHE = {}


def canon_answers(tok, resolve):
    """`set()` of every value canon resolves for `tok` across theme x mode. EMPTY means canon has
    no opinion — which is a DIFFERENT fact from 'the literal disagrees', and the two must never be
    collapsed into one silent skip."""
    if tok not in _ANSWER_CACHE:
        out = set()
        for th in THEMES:
            for md in MODES:
                try:
                    out.add(resolve(tok, th, md).upper())
                except Exception:      # KeyError and anything else the store raises
                    pass
        _ANSWER_CACHE[tok] = out
    return _ANSWER_CACHE[tok]


def scan_source(src, resolve):
    """-> (drifted, local_drift, unchecked) for one generator's source text."""
    fbs = sorted({(t, h.upper()) for t, h in FB_RE.findall(src)})
    local = {t: h.upper() for t, h in DECL_RE.findall(src)}
    drifted, local_drift, unchecked = [], [], []
    for tok, lit in fbs:
        ans = canon_answers(tok, resolve)
        if ans:
            if lit not in ans:
                drifted.append((tok, lit, sorted(ans)))
        elif tok in local:
            if lit != local[tok]:
                local_drift.append((tok, lit, local[tok]))
        else:
            unchecked.append((tok, lit))
    return drifted, local_drift, unchecked


def run(paths=None, verbose=False):
    resolve = _resolver()
    files = sorted(paths if paths is not None else glob.glob(GLOB))
    tot_d, tot_l, tot_u, scanned = [], [], [], 0
    for p in files:
        if os.path.basename(p) == os.path.basename(__file__):
            continue
        try:
            src = open(p, encoding="utf-8").read()
        except OSError as exc:                                  # a crash is not a fail
            print("REFUSED, NAMED: cannot read %s (%s)" % (p, exc))
            return 2
        if not FB_RE.search(src):
            continue
        scanned += 1
        d, l, u = scan_source(src, resolve)
        rel = os.path.relpath(p, os.path.dirname(os.path.dirname(HERE)))
        for tok, lit, ans in d:
            tot_d.append((rel, tok, lit, ans))
        for tok, lit, decl in l:
            tot_l.append((rel, tok, lit, decl))
        for tok, lit in u:
            tot_u.append((rel, tok, lit))
        if verbose:
            print("  %-52s %d fallback(s) · %d drifted · %d local-drift · %d unchecked"
                  % (rel, len(set(FB_RE.findall(src))), len(d), len(l), len(u)))
    print("fallback-drift gate (ADVISORY, #221) — %d generator source(s) carrying var() fallbacks, "
          "glob %s" % (scanned, os.path.relpath(GLOB, os.path.dirname(os.path.dirname(HERE)))))
    for rel, tok, lit, ans in tot_d:
        print("  ⛔ DRIFTED     %s :: var(%s,%s) — canon answers %s"
              % (rel, tok, lit, ", ".join(ans)))
    for rel, tok, lit, decl in tot_l:
        print("  ⛔ LOCAL-DRIFT %s :: var(%s,%s) — the alias itself declares %s"
              % (rel, tok, lit, decl))
    print("  ⬛ UNCHECKED: %d fallback(s) on tokens this resolver answers in NO theme and NO mode "
          "— DECLARED, not passed (%s)"
          % (len(tot_u), ", ".join(sorted({t for _, t, _ in tot_u})[:8]) or "none"))
    if tot_d or tot_l:
        print("❌ %d drifted + %d local-drift. A fallback must be a value canon RESOLVES for that "
              "token. ⬛ ADVISORY — this is a report; promotion to blocking is Dave's."
              % (len(tot_d), len(tot_l)))
        return 1
    print("✅ every var() fallback literal in the glob is one of canon's own answers for its token.")
    return 0


def selftest():
    """⛔ MUTATION BOTH WAYS, per claim. A green scan proves nothing on its own — the pre-#221 tree
    was green under bite 12 too, because bite 12's glob was one file wide."""
    resolve = _resolver()
    fails, ran = [], []

    def bite(name, got, want):
        ran.append(name)
        if got != want:
            fails.append("%s\n     got:  %r\n     want: %r" % (name, got, want))

    clean = ".fx{ --line-2: var(--border-strong,#808080); --focus: var(--focus-ring,#305A85); }\n" \
            ".badge{border:1px solid var(--line-2,#808080);}"
    bite("1 · a CLEAN preamble scans green in all three buckets",
         scan_source(clean, resolve), ([], [], []))
    # ⬛ the exact defect this gate was built from: the pre-#221 focus-ring fallback.
    planted = clean.replace("var(--focus-ring,#305A85)", "var(--focus-ring,#1A1A1A)")
    d, l, u = scan_source(planted, resolve)
    bite("2 · ⬛ MUTANT — the pre-#221 `var(--focus-ring,#1A1A1A)` goes RED, by name, with canon's "
         "own answers printed beside it",
         ([(t, h) for t, h, _ in d], sorted(a for _, _, ans in d for a in ans), l, u),
         ([("--focus-ring", "#1A1A1A")], ["#305A85", "#4587A7"], [], []))
    # ⬛ second arm: the page-local alias whose consumer disagrees with its own declaration.
    planted2 = clean.replace("var(--line-2,#808080);}", "var(--line-2,#767676);}")
    d2, l2, u2 = scan_source(planted2, resolve)
    bite("3 · ⬛ MUTANT — a page-local alias consumed with a literal its own declaration does not "
         "carry goes RED (the second-arm class)",
         (d2, l2, u2), ([], [("--line-2", "#767676", "#808080")], []))
    bite("4 · …and removing the mutation clears it again — both directions, not just the red",
         scan_source(planted2.replace("var(--line-2,#767676);}", "var(--line-2,#808080);}"),
                     resolve),
         ([], [], []))
    # ⬛ F-2: the silent skip is now a DECLARED bucket, never an implied pass.
    dr, lo, un = scan_source(".fx{ --radius: var(--border-radius-surface,0px); "
                             "--tap: var(--target-min,44px); }".replace("0px", "#000000")
                             .replace("44px", "#123456"), resolve)
    bite("5 · ⛔ F-2 · a token canon resolves in NO theme and NO mode is reported UNCHECKED, not "
         "swallowed — the hole is declared, and it does not read as coverage",
         (dr, lo, sorted(t for t, _ in un)),
         ([], [], ["--border-radius-surface", "--target-min"]))
    # ⬛ the glob is the rule: prove it actually reaches every sibling generator, not just one.
    reach = sorted(os.path.basename(p) for p in glob.glob(GLOB)
                   if FB_RE.search(open(p, encoding="utf-8").read()))
    for want in ("gen_bento_canon_217.py", "gen_bento_roles_217.py", "gen_foundations_217.py",
                 "gen_gallery_compare_217.py", "_bento_recut_219.py", "gen_bento_matrix_217.py"):
        bite("6 · the glob REACHES %s (a rule is only as wide as its gate's glob)" % want,
             want in reach, True)
    if fails:
        print("_gate_fallback_drift_221 --selftest: %d BITE(S) FAILED" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        return 1
    print("_gate_fallback_drift_221 --selftest OK — %d bites (mutation driven BOTH ways). "
          "⬛ ADVISORY at birth." % len(ran))
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    return run(verbose="--verbose" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
