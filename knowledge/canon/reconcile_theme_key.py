#!/usr/bin/env python3
"""
reconcile_theme_key.py — move a project from the OLD theme key `legacy` to `common`.

    python3 knowledge/canon/reconcile_theme_key.py                 # DRY RUN — shows every edit
    python3 knowledge/canon/reconcile_theme_key.py --root ../mine    # dry run, somewhere else
    python3 knowledge/canon/reconcile_theme_key.py --write           # actually rewrite
    python3 knowledge/canon/reconcile_theme_key.py --selftest        # prove it, both directions

WHY THIS EXISTS (s227-D8(b), #227). Designers say **Common**. The code key is `legacy`, and
every place the two names met carried a parenthetical to reconcile them. Dave: *"reconcile
them, but not this week."*

The key is NOT being swapped out from under anyone. `canon.css` now answers to BOTH names —
every rule it emits for the theme carries `[data-apollo-theme="legacy"]` **and**
`[data-apollo-theme="common"]`, the old one first and unchanged (s227-D8(a), declared in
`knowledge/tokens/themes/_themes.json` as `attrAliases`). So a page that says `legacy` keeps
working forever and a page that says `common` works too. Nothing has to be rewritten.

This script is for when you WANT to. It rewrites the attribute VALUE in your own files so
your markup says the word you say out loud. It is not required, it is not a migration
deadline, and running it changes nothing about how the page renders — both keys resolve to
the same rules.

WHAT IT TOUCHES, EXACTLY

Only the theme attribute's value, in these five spellings:

    data-apollo-theme="legacy"          HTML, double quotes
    data-apollo-theme='legacy'          HTML, single quotes
    [data-apollo-theme="legacy"]        a CSS selector in YOUR stylesheet
    [data-apollo-theme='legacy']        the same, single quotes
    setAttribute('data-apollo-theme', 'legacy')   JS, either quote style

The bare word "legacy" is NEVER rewritten. It is an ordinary English word that appears in
comments, class names, file paths and prose, and a tool that rewrote all of it would do far
more damage than the inconsistency it fixes.

⛔ IT REFUSES TO TOUCH `knowledge/canon/canon.css` AND THE THEME REGISTRY. Those are where
both keys are DEFINED. Rewriting `legacy` out of canon.css would delete the compatibility
half of the alias and break every page that has not been converted — which is the exact
failure the alias exists to prevent. If you point `--root` at a directory containing them,
they are listed as SKIPPED, by name, with this reason.

DRY RUN IS THE DEFAULT. Nothing is written without `--write`. Exit code is 0 whether or not
there is anything to do; this is a convenience, not a gate.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import os
import re
import shutil
import sys
import tempfile

OLD_KEY = "legacy"
NEW_KEY = "common"

# Extensions worth opening. A binary or an image cannot carry the attribute.
TEXT_EXT = (".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
            ".md", ".json", ".svg", ".php", ".erb", ".hbs", ".jinja", ".j2", ".xml")

# Directories never worth walking into.
SKIP_DIRS = {".git", "node_modules", "__pycache__", "dist", "build", ".next", ".venv",
             "venv", "_to_delete", "coverage"}

# ⛔ THE PROTECTED SET — where BOTH keys are defined. Rewriting here removes the
# compatibility half of the alias, which breaks every unconverted page.
PROTECTED_BASENAMES = {"canon.css", "_themes.json", "gen_theme_cascade.py",
                       "reconcile_theme_key.py"}

# The five spellings, and what each becomes. Written as (pattern, replacement) so the
# selftest can drive every one of them individually.
PATTERNS = [
    (re.compile(r'(data-apollo-theme\s*=\s*")%s(")' % OLD_KEY), r"\g<1>%s\g<2>" % NEW_KEY),
    (re.compile(r"(data-apollo-theme\s*=\s*')%s(')" % OLD_KEY), r"\g<1>%s\g<2>" % NEW_KEY),
    (re.compile(r'(\[data-apollo-theme\s*=\s*")%s("\])' % OLD_KEY), r"\g<1>%s\g<2>" % NEW_KEY),
    (re.compile(r"(\[data-apollo-theme\s*=\s*')%s('\])" % OLD_KEY), r"\g<1>%s\g<2>" % NEW_KEY),
    (re.compile(r"""(setAttribute\(\s*['"]data-apollo-theme['"]\s*,\s*['"])%s(['"])""" % OLD_KEY),
     r"\g<1>%s\g<2>" % NEW_KEY),
]


def rewrite(text):
    """(new_text, hits). Pure — no file touched, so the dry run and the write cannot disagree."""
    hits = 0
    for pat, repl in PATTERNS:
        text, n = pat.subn(repl, text)
        hits += n
    return text, hits


def scan(root):
    """[(relpath, hits, new_text)] for every file with something to change, plus the
    protected files it deliberately left alone: ([changes], [skipped])."""
    changes, skipped = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if not name.lower().endswith(TEXT_EXT):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            try:
                text = open(path, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            new, hits = rewrite(text)
            if not hits:
                continue
            if name in PROTECTED_BASENAMES:
                skipped.append((rel, hits))
                continue
            changes.append((rel, hits, new))
    return changes, skipped


def run(root, write=False, out=print):
    if not os.path.isdir(root):
        out("NOT A DIRECTORY: %s — nothing was inspected." % root)
        return 0
    changes, skipped = scan(root)
    out("Theme key reconcile — %s" % os.path.abspath(root))
    out("  %s  ->  %s   (the attribute VALUE only; the bare word is never touched)"
        % (OLD_KEY, NEW_KEY))
    out("")
    if not changes and not skipped:
        out("Nothing to do — no file here sets data-apollo-theme to %r." % OLD_KEY)
        return 0
    total = 0
    for rel, hits, new in changes:
        total += hits
        out("  %-6s %3d  %s" % ("WRITE" if write else "would", hits, rel))
        if write:
            open(os.path.join(root, rel), "w", encoding="utf-8").write(new)
    for rel, hits in skipped:
        out("  SKIP     %3d  %s — this is where BOTH keys are defined; rewriting it would "
            "delete the compatibility half of the alias" % (hits, rel))
    out("")
    if write:
        out("%d occurrence(s) rewritten across %d file(s)." % (total, len(changes)))
    else:
        out("DRY RUN — nothing was written. %d occurrence(s) across %d file(s) would change."
            % (total, len(changes)))
        out("Run it again with --write when you are happy with the list.")
    out("Either key keeps working: canon answers to both. This is cosmetic, not a migration.")
    return 0


def selftest():
    fails = []
    tmp = tempfile.mkdtemp(prefix="reconcile-theme-key-selftest-")
    try:
        quiet = lambda *_a, **_k: None  # noqa: E731

        # 1. every spelling is rewritten — driven one at a time, so a broken pattern cannot
        #    hide behind a working one.
        spellings = [
            '<html data-apollo-theme="legacy">',
            "<html data-apollo-theme='legacy'>",
            '[data-apollo-theme="legacy"] .thing{color:red}',
            "[data-apollo-theme='legacy'] .thing{color:red}",
            "el.setAttribute('data-apollo-theme', 'legacy');",
        ]
        for src in spellings:
            new, hits = rewrite(src)
            if hits != 1 or OLD_KEY in new or NEW_KEY not in new:
                fails.append("spelling not rewritten: %r -> %r (%d hit)" % (src, new, hits))

        # 2. THE BARE WORD SURVIVES. This is the whole safety argument for the tool.
        for src in ('<!-- legacy notes -->', 'class="legacy-panel"', 'src="legacy/app.js"',
                    'const legacy = true;', '# the legacy theme, historically',
                    'data-theme="legacy"'):
            new, hits = rewrite(src)
            if hits or new != src:
                fails.append("the bare word was rewritten in %r -> %r" % (src, new))

        # 3. DRY RUN WRITES NOTHING — driven on a real file, compared byte for byte.
        page = os.path.join(tmp, "page.html")
        body = '<html data-apollo-theme="legacy"><body data-theme="light"></body></html>\n'
        open(page, "w", encoding="utf-8").write(body)
        run(tmp, write=False, out=quiet)
        if open(page, encoding="utf-8").read() != body:
            fails.append("the DRY RUN wrote to disk — it must be a read")

        # 4. --write does write, and is idempotent.
        run(tmp, write=True, out=quiet)
        after = open(page, encoding="utf-8").read()
        if 'data-apollo-theme="common"' not in after or OLD_KEY in after:
            fails.append("--write did not convert the page: %r" % after)
        run(tmp, write=True, out=quiet)
        if open(page, encoding="utf-8").read() != after:
            fails.append("a second --write moved the file again — not idempotent")

        # 5. THE PROTECTED FILES ARE REFUSED, even with --write. Removing `legacy` from
        #    canon.css deletes the compatibility half of the alias.
        prot = os.path.join(tmp, "canon.css")
        pbody = '[data-apollo-theme="legacy"] .cn-x{--a:1}\n'
        open(prot, "w", encoding="utf-8").write(pbody)
        lines = []
        run(tmp, write=True, out=lines.append)
        if open(prot, encoding="utf-8").read() != pbody:
            fails.append("canon.css WAS REWRITTEN — the alias's compatibility half was deleted")
        if not any("SKIP" in ln and "canon.css" in ln for ln in lines):
            fails.append("canon.css was skipped SILENTLY — the skip must be named")

        # 6. a --root that is not a directory says so rather than reporting an empty project.
        lines = []
        run(os.path.join(tmp, "NO-SUCH-DIR"), write=False, out=lines.append)
        if not any("NOT A DIRECTORY" in ln for ln in lines):
            fails.append("a non-directory --root did not say so")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return fails


def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("reconcile_theme_key SELFTEST FAIL:")
            for f in fails:
                print("  X " + f)
            sys.exit(1)
        print("reconcile_theme_key selftest OK — 6 arm(s), both directions driven.")
        return
    root = os.getcwd()
    if "--root" in sys.argv:
        i = sys.argv.index("--root")
        if i + 1 >= len(sys.argv):
            print("--root needs a directory. Using the current one instead.")
        else:
            root = sys.argv[i + 1]
    sys.exit(run(root, write="--write" in sys.argv))


if __name__ == "__main__":
    main()
