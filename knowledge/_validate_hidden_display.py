#!/usr/bin/env python3
"""[hidden]-vs-author-display sweep — ADVISORY. Never blocks, never writes.

WHY THIS EXISTS — the defect, measured, not imagined. The UA stylesheet carries
`[hidden]{display:none}` at specificity (0,1,0). ANY author `display:` rule that matches the
same element and is not beaten on specificity/order therefore WINS, and the element renders
while its `hidden` attribute tells assistive technology it is gone. #218 W3 finding F1 drove
the consequence in a real snippet: `Command-palette.reference.html`'s `#cp2-o1` shipped
`hidden` in the markup, `.cp-opt{display:flex}` painted it anyway, and a phantom option sat in
the a11y tree of a listbox the specimen calls EMPTY. Dave ruled the one-line fix at cause in
that file (`s218-D5` clause 3) and, in the same breath, put THE REPO-WIDE SWEEP on the gates
backlog as a class candidate. This is that sweep. The class was never swept; only the one
instance was fixed [[gate-dont-patch]].

WHAT IT CHECKS, per `knowledge/snippets/*.reference.html`:
  For every element that CAN CARRY `hidden` — statically in the markup, or dynamically because
  the snippet's own script assigns/sets/toggles the attribute on it — is there an author
  `display:` declaration that would match it and beat the `[hidden]` sheet, with no author
  `[hidden]{display:none}` remedy of sufficient specificity to restore it?

THREE POPULATIONS, kept apart because they carry different certainty:
  STATIC   — `hidden` is in the committed markup. The strongest signal.
  DYNAMIC  — the script sets `hidden`; the target's selector is RESOLVED from the script's own
             binding (`querySelector('.x')` / `getElementById('x')` / `querySelectorAll(...)`).
  UNRESOLVED — the script sets `hidden` on an expression this reader cannot resolve to a
             selector. DECLARED AND COUNTED, never silently dropped: an unresolvable target is
             a gap in THIS INSTRUMENT'S REACH, not evidence that the file is clean
             [[measuring-tool-must-not-guess]].

DELIBERATE OVER-INCLUSION — why this is ADVISORY and not blocking. The matcher grades the
SUBJECT COMPOUND of each selector (its last compound: tag / .class / #id / [attr] /
pseudo-class) and IGNORES combinators — `.a .b{display:flex}` is treated as matching any `.b`.
A real browser would first check that a `.a` ancestor exists. So this check can name a pair
that cannot actually collide in the rendered DOM. That is the correct bias for a triage
instrument (a missed phantom is invisible; a named non-collision costs one look) but it is the
exact reason findings here are TRIAGE INPUT, not repairs. Some findings will be INTENTIONAL.

NOT A RENDER TEST. This reads bytes. `_validate_state_contrast.py` drives a real browser and
already skips `display:none` subtrees; it would never SEE this defect, because the defect's
whole symptom is that the element is NOT display:none. A rendering gate cannot ask "should this
have been hidden?" — only the markup's own `hidden` attribute states that intent.

GATE-GLOB-SCOPE: globs `knowledge/snippets/*.reference.html` and ONLY that
[[gate-glob-scope-rule]]. Writes nothing, anywhere — so it has no #158 write-by-default surface.

USAGE
    python3 knowledge/_validate_hidden_display.py              # sweep the real corpus
    python3 knowledge/_validate_hidden_display.py --selftest   # the bites, both directions
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
sys.path.insert(0, HERE)
from _htmlmask import mask_comments  # noqa: E402  — the ONE shared HTML-comment mask (#218)

CORPUS = os.path.join("snippets", "*.reference.html")

# A CSS comment is masked the same length-preserving way HTML comments are, so every offset
# below still addresses the raw bytes and every line number stays true.
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT_RE = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S | re.I)

# A bare `hidden` attribute on an open tag. `aria-hidden` / `data-hidden` are excluded by the
# preceding-char guard; a quoted "hidden" inside another attribute value is excluded by
# requiring whitespace before it and `>`, `/`, or whitespace after.
OPEN_TAG_RE = re.compile(r"<([a-zA-Z][-\w]*)((?:\"[^\"]*\"|'[^']*'|[^>\"'])*)>")
BARE_HIDDEN_RE = re.compile(r"(?:^|\s)hidden(?=\s|/|$|=)")
CLASS_RE = re.compile(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""")
ID_RE = re.compile(r"""\bid\s*=\s*(?:"([^"]*)"|'([^']*)')""")

# Script-side ways to put the attribute on an element.
# The receiver of a `hidden` write: everything back to the nearest whitespace/statement break.
# Deliberately permissive — a call chain (`pick(x()).hidden = …`) must be SEEN and declared
# unresolvable, not missed because the regex only understood bare identifiers.
HIDDEN_WRITE_RE = re.compile(
    r"""([^\s;{}=\n]+)\s*\.hidden\s*=(?!=)|"""
    r"""([^\s;{}=\n]+)\s*\.(?:set|toggle|remove)Attribute\(\s*['"]hidden['"]""")
BIND_RE = re.compile(
    r"""(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*[^;\n]*?"""
    r"""(?:querySelectorAll|querySelector)\(\s*['"]([^'"]+)['"]""")
BIND_ID_RE = re.compile(
    r"""(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*[^;\n]*?"""
    r"""getElementById\(\s*['"]([^'"]+)['"]""")
# `x.forEach(s => s.hidden = ...)` — the iteration variable inherits x's binding.
FOREACH_RE = re.compile(
    r"""([A-Za-z_$][\w$]*)\s*\.forEach\(\s*\(?\s*([A-Za-z_$][\w$]*)""")

DISPLAY_DECL_RE = re.compile(r"(?<![-\w])display\s*:\s*([^;{}!]+)", re.I)


JS_COMMENT_RE = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)


def _blank(s):
    """Replace every non-newline byte with a space — the length- and line-preserving blank."""
    return re.sub(r"[^\n]", " ", s)


def _mask_css_comments(css):
    """Blank CSS comment bytes, PRESERVING length and newlines — same contract as the HTML
    mask, so a span taken from the masked text addresses the same raw bytes."""
    return CSS_COMMENT_RE.sub(lambda m: _blank(m.group(0)), css)


def _isolate(pattern, text, transform=lambda s: s):
    """Keep ONLY the group-1 bodies matched by `pattern`, blanking everything else — with the
    file's line structure intact, so every offset and every line number this gate prints
    addresses THE FILE, not a re-joined extract. A line number that names the wrong line is the
    ds-021 defect [[measure-dont-convert-units]]; it was live in this gate's first draft and is
    the reason the isolation is done this way rather than by `findall` + `join`."""
    out, last = [], 0
    for m in pattern.finditer(text):
        out.append(_blank(text[last:m.start(1)]))
        out.append(transform(m.group(1)))
        last = m.end(1)
    out.append(_blank(text[last:]))
    return "".join(out)


def specificity(compound):
    """(ids, classes+attrs+pseudo-classes, types) for ONE compound selector — CSS's own
    three-tuple, comparable with plain tuple ordering."""
    ids = len(re.findall(r"#[-\w]+", compound))
    cls = (len(re.findall(r"\.[-\w]+", compound))
           + len(re.findall(r"\[[^\]]*\]", compound))
           + len(re.findall(r"(?<!:):[-\w]+(?:\([^)]*\))?", compound)))
    typ = len(re.findall(r"(?:^|[\s>+~])([a-zA-Z][-\w]*)", compound))
    return (ids, cls, typ)


def subject_compound(selector):
    """The LAST compound of a selector — the element the rule actually styles."""
    return re.split(r"[\s>+~]+", selector.strip())[-1] or selector.strip()


def parse_rules(css):
    """[(selector_part, subject_compound, display_value, line, at_rule_context)] for every
    comma-part of every rule that declares `display`. At-rule bodies are walked, not skipped —
    a `display` inside `@media print` is still an author declaration."""
    out = []
    depth_stack = []
    i, n = 0, len(css)
    buf_start = 0
    while i < n:
        ch = css[i]
        if ch == "{":
            head = css[buf_start:i].strip()
            if head.startswith("@"):
                depth_stack.append(head.split("{")[0].strip())
                buf_start = i + 1
                i += 1
                continue
            # A style rule: find its matching close brace.
            j, d = i + 1, 1
            while j < n and d:
                if css[j] == "{":
                    d += 1
                elif css[j] == "}":
                    d -= 1
                j += 1
            body = css[i + 1:j - 1]
            dm = DISPLAY_DECL_RE.search(body)
            if dm:
                # The line of the SELECTOR'S FIRST REAL BYTE — `buf_start` is where the
                # previous rule ended, which is a run of whitespace earlier and would name a
                # blank line (or line 1 for the first rule in the sheet).
                raw_head = css[buf_start:i]
                head_pos = buf_start + (len(raw_head) - len(raw_head.lstrip()))
                line = css[:head_pos].count("\n") + 1
                ctx = " ".join(depth_stack)
                for part in head.split(","):
                    part = part.strip()
                    if part:
                        out.append((part, subject_compound(part),
                                    dm.group(1).strip(), line, ctx))
            buf_start = j
            i = j
            continue
        if ch == "}":
            if depth_stack:
                depth_stack.pop()
            buf_start = i + 1
        i += 1
    return out


def compound_matches(compound, tag, classes, ids):
    """Does this subject compound match an element with this tag / classes / id?

    COMBINATOR-BLIND BY DESIGN (see the module docstring): only the subject compound is
    graded. Attribute selectors other than [hidden] are treated as POSSIBLY matching — a
    triage instrument must not clear a pair it cannot decide.
    """
    for want_id in re.findall(r"#([-\w]+)", compound):
        if want_id not in ids:
            return False
    for want_cls in re.findall(r"\.([-\w]+)", compound):
        if want_cls not in classes:
            return False
    head = re.match(r"^([a-zA-Z][-\w]*)", compound)
    if head and tag != "*" and head.group(1).lower() not in (tag.lower(), "*"):
        return False
    return True


def has_combinator(selector):
    """True when the selector states an ANCESTOR/SIBLING condition this reader does not check.
    Findings from such a painter are POSSIBLE, not CERTAIN — the tier split is the whole
    difference between a triage list and a list of lies [[measuring-tool-must-not-guess]]."""
    return bool(re.search(r"[\s>+~]", selector.strip()))


def _element_key(tag, classes, ids, line, origin):
    return (tag, tuple(sorted(classes)), tuple(sorted(ids)), line, origin)


def hidden_bearers(markup, script_text):
    """(static, dynamic, unresolved) — elements that can carry `hidden`.

    static/dynamic are element keys; unresolved is a list of DECLARED script expressions this
    reader could not resolve to a selector.
    """
    static, dynamic, unresolved = [], [], []
    for m in OPEN_TAG_RE.finditer(markup):
        tag, attrs = m.group(1), m.group(2)
        if tag.lower() in ("style", "script"):
            continue
        stripped = CLASS_RE.sub(" ", ID_RE.sub(" ", attrs))
        stripped = re.sub(r"""=\s*(?:"[^"]*"|'[^']*')""", "= ", stripped)
        if not BARE_HIDDEN_RE.search(stripped):
            continue
        cm = CLASS_RE.search(attrs)
        im = ID_RE.search(attrs)
        classes = set(((cm.group(1) or cm.group(2)) if cm else "").split())
        ids = set(filter(None, [((im.group(1) or im.group(2)) if im else "")]))
        static.append(_element_key(tag, classes, ids, markup[:m.start()].count("\n") + 1,
                                   "STATIC"))

    binds = {}
    for bm in BIND_RE.finditer(script_text):
        binds[bm.group(1)] = ("sel", bm.group(2))
    for bm in BIND_ID_RE.finditer(script_text):
        binds[bm.group(1)] = ("id", bm.group(2))
    for fm in FOREACH_RE.finditer(script_text):
        if fm.group(1) in binds:
            binds.setdefault(fm.group(2), binds[fm.group(1)])

    for hm in HIDDEN_WRITE_RE.finditer(script_text):
        expr = (hm.group(1) or hm.group(2) or "").strip()
        line = script_text[:hm.start()].count("\n") + 1
        root = re.split(r"[.\[(]", expr)[0]
        if root not in binds:
            src = script_text.splitlines()[line - 1].strip()
            unresolved.append((src[:120], line))
            continue
        kind, val = binds[root]
        if kind == "id":
            dynamic.append(_element_key("*", set(), {val}, line, "DYNAMIC"))
        else:
            sub = subject_compound(val)
            tag = (re.match(r"^([a-zA-Z][-\w]*)", sub) or [None, "*"])[1] or "*"
            dynamic.append(_element_key(tag, set(re.findall(r"\.([-\w]+)", sub)),
                                        set(re.findall(r"#([-\w]+)", sub)), line, "DYNAMIC"))
    return static, dynamic, unresolved


def check_file(path, text=None):
    """Findings for ONE snippet: list of (kind, message). Never raises on odd markup."""
    if text is None:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    name = os.path.basename(path)
    masked = mask_comments(text)          # HTML comments cannot plant or hide a rule
    # Three views of the SAME file, each keeping the file's own line structure:
    css = _isolate(STYLE_RE, masked, _mask_css_comments)
    script_text = _isolate(SCRIPT_RE, masked,
                           lambda s: JS_COMMENT_RE.sub(lambda m: _blank(m.group(0)), s))
    markup = SCRIPT_RE.sub(lambda m: _blank(m.group(0)),
                           STYLE_RE.sub(lambda m: _blank(m.group(0)), masked))

    rules = parse_rules(css)
    painters = [r for r in rules if r[2].split()[0].lower() != "none"]
    remedies = [r for r in rules
                if r[2].split()[0].lower() == "none" and "[hidden]" in r[1].lower()]

    static, dynamic, unresolved = hidden_bearers(markup, script_text)
    findings = []
    for tag, classes, ids, line, origin in static + dynamic:
        cls, idset = set(classes), set(ids)
        # CERTAIN painters (no combinator) are graded FIRST — one element reports its
        # strongest signal, never a POSSIBLE one that happened to be earlier in the sheet.
        ordered = sorted(painters, key=lambda r: has_combinator(r[0]))
        for sel, sub, disp, rline, ctx in ordered:
            if "[hidden]" in sub.lower():
                continue          # a painter GATED on [hidden] is a deliberate override
            if not compound_matches(sub, tag, cls, idset):
                continue
            pspec = specificity(sub)
            covered = None
            for rsel, rsub, _d, rrline, _c in remedies:
                probe = re.sub(r"\[hidden\]", "", rsub, flags=re.I) or "*"
                if compound_matches(probe, tag, cls, idset) and specificity(rsub) >= pspec:
                    covered = (rsel, rrline)
                    break
            if covered:
                continue
            weaker = [r for r in remedies
                      if compound_matches(re.sub(r"\[hidden\]", "", r[1], flags=re.I) or "*",
                                          tag, cls, idset)]
            why = (f"; the file's only matching [hidden] remedy `{weaker[0][0]}` "
                   f"(line {weaker[0][3]}) is WEAKER at {specificity(weaker[0][1])}"
                   if weaker else "; the file has NO matching `[hidden]{display:none}` remedy")
            where = ("class=" + ".".join(sorted(cls))) if cls else \
                    ("id=" + ",".join(sorted(idset)) if idset else "tag=" + tag)
            tier = origin + ("?" if has_combinator(sel) else "")
            if tier.endswith("?"):
                why += (f" ⚠ POSSIBLE ONLY: `{sel}` states an ancestor/sibling condition this "
                        f"reader does not check, so the pair may never meet in the real DOM")
            findings.append((
                tier,
                f"{name}: {tier} hidden-bearing <{tag}> ({where}) at line {line} is painted "
                f"by `{sel}{{display:{disp}}}` (line {rline}"
                f"{', inside ' + ctx if ctx else ''}, specificity {pspec}){why} — the UA "
                f"`[hidden]{{display:none}}` is (0,1,0) and loses, so the element renders while "
                f"`hidden` tells AT it is gone (#218 W3 F1 class, s218-D5 clause 3)"))
            break
    for expr, line in unresolved:
        findings.append((
            "UNRESOLVED",
            f"{name}: line {line} sets `hidden` — `{expr}` — but this reader cannot "
            f"resolve the receiver to a selector, so the element is UNCHECKED, which "
            f"is a gap in this instrument's reach, NOT evidence the file is clean"))
    return findings


# ---------------------------------------------------------------------------- selftest
def _selftest():
    fails = []

    def bite(label, ok, quote=None):
        print(f"  {'✓' if ok else '✗'} {label}")
        if quote:
            print(f"      quoted: {quote}")
        if not ok:
            fails.append(label)

    def fx(style, body, script=""):
        return (f"<html><head><style>{style}</style></head><body>{body}"
                f"<script>{script}</script></body></html>")

    # 1 — RED direction, STATIC: painted, no remedy.
    f = check_file("F.reference.html", fx(".x{display:flex}", '<div class="x" hidden>o</div>'))
    hit = [m for k, m in f if k == "STATIC"]
    bite("STATIC defect is CAUGHT and names the class, the painting rule and the missing remedy",
         bool(hit) and "class=x" in hit[0] and "display:flex" in hit[0]
         and "NO matching" in hit[0], hit[0] if hit else None)

    # 2 — GREEN direction: the s218-D5 remedy shape clears it. A check that cannot go green
    #     on the ruled fix would condemn Dave's own ruling.
    f = check_file("F.reference.html",
                   fx(".x{display:flex} .x[hidden]{display:none}", '<div class="x" hidden>o</div>'))
    bite("the RULED remedy `.x[hidden]{display:none}` clears the finding (no false positive on "
         "the s218-D5 fix shape)", [m for k, m in f if k == "STATIC"] == [])

    # 3 — a remedy WEAKER than the painter is not a remedy; the message must say so.
    f = check_file("F.reference.html",
                   fx(".a.b{display:flex} [hidden]{display:none}",
                      '<div class="a b" hidden>o</div>'))
    hit = [m for k, m in f if k == "STATIC"]
    bite("a LOWER-specificity [hidden] remedy is still caught, and the message quotes both "
         "specificities", bool(hit) and "WEAKER" in hit[0], hit[0] if hit else None)

    # 4 — comment masking, BOTH comment grammars. A rule that only exists inside a comment is
    #     not a rule; a defect planted in a comment must not be reported.
    f = check_file("F.reference.html",
                   fx("/* .x{display:flex} */", '<div class="x" hidden>o</div>'))
    bite("a painting rule inside a CSS comment is NOT counted (comment-masked)",
         [m for k, m in f if k == "STATIC"] == [])
    f = check_file("F.reference.html",
                   fx(".x{display:flex}", '<!-- <div class="x" hidden>o</div> -->'))
    bite("a hidden-bearing element inside an HTML comment is NOT counted (shared _htmlmask)",
         [m for k, m in f if k == "STATIC"] == [])

    # 5 — DYNAMIC: the attribute arrives from script, the selector is resolved from the binding.
    f = check_file("F.reference.html",
                   fx(".y{display:grid}", '<div class="y">o</div>',
                      "const el = document.querySelector('.y'); el.hidden = true;"))
    hit = [m for k, m in f if k == "DYNAMIC"]
    bite("a script-set `hidden` on a querySelector-bound element is RESOLVED and caught",
         bool(hit) and "class=y" in hit[0], hit[0] if hit else None)
    f = check_file("F.reference.html",
                   fx(".y{display:grid}", '<div class="y">o</div><ul id="L"></ul>',
                      "const ss = document.querySelectorAll('.y');"
                      " ss.forEach(s => s.hidden = true);"))
    bite("the forEach iteration variable inherits its list's binding (querySelectorAll)",
         any(k == "DYNAMIC" for k, _ in f))

    # 6 — UNRESOLVED is DECLARED, never dropped.
    f = check_file("F.reference.html",
                   fx(".z{display:flex}", '<div class="z">o</div>',
                      "pick(whatever()).hidden = true;"))
    hit = [m for k, m in f if k == "UNRESOLVED"]
    bite("an unresolvable script target is DECLARED as UNCHECKED, not silently dropped",
         bool(hit) and "NOT evidence" in hit[0], hit[0] if hit else None)

    # 7 — a painter GATED on [hidden] is a deliberate override, not the defect.
    f = check_file("F.reference.html",
                   fx(".x[hidden]{display:flex}", '<div class="x" hidden>o</div>'))
    bite("a painter whose own selector carries [hidden] is read as a deliberate override, "
         "not the defect", [m for k, m in f if k == "STATIC"] == [])

    # 8 — the #218 instance, on the REAL file, in BOTH directions. The one measured case is the
    #     only proof available that this reader agrees with a browser [[mutation-tests-the-clause]].
    cp = os.path.join(HERE, "snippets", "Command-palette.reference.html")
    if os.path.exists(cp):
        raw = open(cp, encoding="utf-8").read()
        base = [m for k, m in check_file(cp, raw) if k in ("STATIC", "DYNAMIC")]
        bite("REAL #218 case: Command-palette carries NO CERTAIN finding with the ruled fix "
             "in place (the check can go green on Dave's own remedy)", base == [],
             base[0] if base else None)
        broke = raw.replace(
            ".cp[hidden],.cp-opt[hidden],.cp-empty[hidden],.cp-group[hidden]{display:none}",
            "/* remedy removed by the selftest mutant */")
        got = [m for k, m in check_file(cp, broke) if k in ("STATIC", "DYNAMIC")]
        bite("REAL #218 case MUTANT: delete the ruled one-line remedy and the ORIGINAL "
             "phantom option is named again, by file, class and rule",
             bool(got) and any("cp-opt" in m or "cp2-o1" in m for m in got),
             got[0] if got else None)
        bite("REAL #218 case MUTANT is CERTAIN-tier, not a hedged POSSIBLE — the one measured "
             "instance of this class must land in the tier that means it",
             any(k == "STATIC" for k, _ in check_file(cp, broke)))
    else:
        bite("REAL #218 case: Command-palette.reference.html present to test against", False)

    # 9 — EVERY line number this gate prints addresses THE FILE. The first draft printed a
    #     style-block-relative number (painter at "line 170" for a rule really on line 220) —
    #     a figure named with the wrong frame is the ds-021 class, and it is asserted, not
    #     assumed [[measure-dont-convert-units]].
    doc = ("<html>\n<head>\n<style>\n\n\n.x{display:flex}\n</style>\n</head>\n<body>\n"
           '<div class="x" hidden>o</div>\n</body></html>')
    f = check_file("F.reference.html", doc)
    want_css = doc.splitlines().index(".x{display:flex}") + 1
    want_el = doc.splitlines().index('<div class="x" hidden>o</div>') + 1
    bite(f"line numbers are FILE-relative, not block-relative (painter line {want_css}, "
         f"element line {want_el})",
         bool(f) and f"at line {want_el}" in f[0][1] and f"(line {want_css}" in f[0][1],
         f[0][1] if f else None)

    # 10 — JS comments are masked too. Prose ABOUT the defect must not be reported AS the
    #      defect — Command-palette's own warning comment did exactly that in the first draft.
    f = check_file("F.reference.html",
                   fx(".z{display:flex}", '<div class="z">o</div>',
                      "// never write el.hidden = !on and drop the CSS rule\n"))
    bite("a `hidden` write inside a JS comment is NOT counted (prose about the defect is not "
         "the defect)", f == [], f[0][1] if f else None)

    # 11 — the tier split itself, both directions. A combinator-blind hit must NOT be sold as
    #     certain, and a combinator-free hit must NOT be hedged.
    f = check_file("F.reference.html",
                   fx(".wrap span{display:block}", '<div><span class="q" hidden>o</span></div>'))
    bite("an ANCESTOR-conditioned painter lands in the POSSIBLE tier and says why",
         [k for k, _ in f] == ["STATIC?"] and "POSSIBLE ONLY" in f[0][1], f[0][1] if f else None)
    f = check_file("F.reference.html",
                   fx(".wrap span{display:block} .q{display:flex}",
                      '<div><span class="q" hidden>o</span></div>'))
    bite("when BOTH a certain and a possible painter match, the element reports the CERTAIN "
         "one (strongest signal wins, not sheet order)", [k for k, _ in f] == ["STATIC"])

    print(f"{'❌' if fails else '✅'} _validate_hidden_display selftest: "
          f"{len(fails)} bite(s) failed" if fails else
          "✅ _validate_hidden_display selftest: all bites pass")
    return 1 if fails else 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    root = HERE
    targets = sorted(glob.glob(os.path.join(root, CORPUS)))
    order = ["STATIC", "DYNAMIC", "STATIC?", "DYNAMIC?", "UNRESOLVED"]
    rows, counts = [], dict((k, 0) for k in order)
    for p in targets:
        f = check_file(p)
        for k, _m in f:
            counts[k] = counts.get(k, 0) + 1
        if f:
            rows.append((os.path.basename(p), f))
    print("[hidden]-vs-author-display sweep — ADVISORY, non-gating "
          "(#218 W3 F1 class, s218-D5 clause 3)")
    print(f"{len(targets)} snippet(s) scanned, {len(rows)} with signals · "
          + " · ".join(f"{counts[k]} {k}" for k in order) + "\n")
    for name, f in rows:
        print(f"## {name} — {len(f)} signal(s)")
        for kind, msg in sorted(f, key=lambda x: order.index(x[0])):
            print(f"  [{kind}] {msg}")
        print()
    if not rows:
        print("no signals.")
    print("⚠ TRIAGE INPUT, NOT A REPAIR LIST. CERTAIN tiers (STATIC/DYNAMIC) name a painter "
          "with no ancestor condition. `?` tiers are combinator-blind and may never meet in "
          "the real DOM. UNRESOLVED is this instrument's own blind spot, not a clean bill.")
    sys.exit(0)   # advisory: never blocks


if __name__ == "__main__":
    main()
