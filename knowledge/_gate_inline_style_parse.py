#!/usr/bin/env python3
"""_gate_inline_style_parse.py — ⬛ ADVISORY AT BIRTH (#221). The FIRST parser in the static leg.

⛔ THE CLASS (#122, [[no-gate-parses-the-artefact]]): *the first gate is a PARSE in the
consumer's grammar.* #220-L1 finding 16 measured that this repo's static gate leg has **no HTML
parser and no CSS parser anywhere in it** — eight BLOCKING gates read HTML/CSS artefacts with
`re` alone (`_validate_dataviz.py`, `_validate_compose.py`, `_validate_a11y.py`,
`_validate_grid.py`, `_validate_radius.py`, `_validate_css_governed.py`,
`_validate_no_hardcode.py`, `_validate_property_resolves.py`). None imports `html.parser`,
`ElementTree`, or any CSS parser; the CASCADE is invisible to all of them.

⛔ WHAT IT COST, MEASURED, NOT ARGUED. L1's finding 12 planted
`<div style="padding:13px;border-radius:7px;border-width:5px">` in a pro-forma and the BLOCKING
DEF-004 gate exited **0** — because `_validate_no_hardcode.styles()` read `<style>` blocks and
nothing else. Three hardcoded values, in the least overridable place in CSS, through the gate
whose entire stated purpose is *"styling must be a token so MODES can override it"*.

⚠ THIS IS A SEED, NOT AN OCEAN, AND THE SCOPE IS THE POINT. #221 fixed that specific hole at
cause inside `_validate_no_hardcode.py` — with a REGEX, because that is the reader the tree
already had (`_validate_compose.py:57`) and a repair should not smuggle in a dependency. This
file is the separate, honest answer to the CLASS: ONE parser, over the NARROWEST population
where a parser would have caught a proved false green — the `style=""` attributes of
`knowledge/_proforma/*.html` — asked in the consumer's own grammar. The other seven regex gates
are PRICED in `notes/_subreports/2026-08-27-221-laneA.md`, not built here.

★ WHAT IT CAN SAY THAT NO REGEX GATE CAN. Beyond finding hardcodes, it reports the
**PARSER-vs-REGEX DELTA**: attributes a real HTML parser sees that the tree's `style="([^"]*)"`
pattern does not. Single quotes, entity-escaped values, attributes broken across a newline, an
attribute on a tag whose earlier attribute contains a quote — each is a live way to put a
declaration into an artefact that every current gate is blind to. That delta is the evidence for
whether the class is worth the rest of the money.

⬛ ADVISORY AT BIRTH AND IT SAYS SO ON EVERY RUN. Exit 0 unless `--strict`, and nothing in this
repo passes `--strict`. Promotion, and any question about whether a parser dependency may enter
the stdlib-only gate set, is DAVE'S — `html.parser` is stdlib, so this seed costs no dependency;
a CSS parser would not be, and that is exactly the question the ocean would raise.

Usage:
    python3 knowledge/_gate_inline_style_parse.py --check      # advisory report, exit 0
    python3 knowledge/_gate_inline_style_parse.py --check --strict
    python3 knowledge/_gate_inline_style_parse.py --selftest   # known-answer test, both ways
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
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA = os.path.join(HERE, "_proforma")

# The property families DEF-004 governs, in the same words `_validate_no_hardcode.py` uses.
# ⚠ DELIBERATELY THE SAME SCOPE, NOT A WIDER ONE. A seed gate that also invented new rules
# would make its own findings unfalsifiable against the gate it is measuring.
SPACING = r'(?:padding|margin|gap|row-gap|column-gap)(?:-(?:top|right|bottom|left|inline|block|inline-start|inline-end|block-start|block-end))?'
BORDERW = (r'(?:border(?:-(?:top|right|bottom|left|inline|block|'
           r'inline-start|inline-end|block-start|block-end))?(?:-width)?|outline(?:-width)?)')
RADIUS = r'(?:border(?:-(?:(?:top|bottom)-(?:left|right)|(?:start|end)-(?:start|end)))?-radius)'
GOVERNED = re.compile(r'^(?:%s|%s|%s)$' % (SPACING, RADIUS, BORDERW))

# What the tree's existing readers see, quoted so the DELTA is measured against the real thing
# rather than against a straw man. `_validate_compose.py:57` and (since #221)
# `_validate_no_hardcode.styles()` both use exactly this.
TREE_ATTR_RE = re.compile(r'style="([^"]*)"')


class StyleAttrParser(HTMLParser):
    """Collect every `style` attribute value, in the consumer's grammar.

    ⚠ `convert_charrefs` is left at its default True, so `&#58;` in an attribute value arrives
    as `:` — which is the whole point: the browser resolves it, and a regex over raw source
    never does.
    """

    def __init__(self):
        super().__init__()
        self.found = []          # (tag, line, value)
        self.parse_errors = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k and k.lower() == "style" and v:
                self.found.append((tag, self.getpos()[0], v))

    handle_startendtag = handle_starttag

    def error(self, message):    # py<3.9 compatibility; never silent
        self.parse_errors.append(message)


def declarations(value):
    """-> [(prop, val)] from one style attribute value."""
    out = []
    for decl in value.split(";"):
        if ":" not in decl:
            continue
        prop, _, val = decl.partition(":")
        out.append((prop.strip().lower(), val.strip()))
    return out


def raw_px(val):
    """A px that is NOT inside a var() fallback — the DEF-004 test, unchanged."""
    return bool(re.search(r'\d+px', re.sub(r'var\([^)]*\)', '', val)))


def read_file(path):
    """-> (findings, delta, errors). Fails LOUD and NAMED; never returns a silent empty."""
    html = open(path, encoding="utf-8", errors="replace").read()
    p = StyleAttrParser()
    errors = list(p.parse_errors)
    try:
        p.feed(html)
        p.close()
    except Exception as e:                      # [[a-crash-is-not-a-fail]]
        errors.append("%s: %s" % (type(e).__name__, e))
    findings = []
    for tag, line, value in p.found:
        for prop, val in declarations(value):
            if GOVERNED.match(prop) and raw_px(val):
                # ⚠ THE CSS-TRIANGLE EXCEPTION IS SCOPED TO THE WHOLE DECLARATION BLOCK, NOT TO
                # ONE DECLARATION — and this gate's own bite is why. In a `<style>` rule the
                # idiom is the shorthand `border:3px solid transparent`, so "transparent" and
                # the px sit in ONE value and a per-declaration test works. In an attribute the
                # same intent is routinely spelt `border-width:3px;border-color:transparent`,
                # three declarations apart, and a per-declaration test flags it. The FIXTURE was
                # right and the reading was wrong.
                if prop.startswith(("border", "outline")) and "transparent" in value:
                    continue
                findings.append((os.path.basename(path), line, tag, prop, val))
    # ⛔ THE DELTA, IN BOTH DIRECTIONS — this is the #122 argument made numerical.
    #   PARSER-ONLY  = a declaration the browser applies and the tree's regex cannot see.
    #   REGEX-ONLY   = text the tree's regex reads as a live style attribute and the browser
    #                  never applies (inside a comment, inside a <script>, inside a text node).
    # The second is the more interesting half: it is not a blind spot, it is a HALLUCINATION,
    # and a gate that fires on it accuses an artefact of a defect it does not have.
    seen_by_regex = set(TREE_ATTR_RE.findall(html))
    seen_by_parser = {v for _t, _l, v in p.found}
    delta = [(os.path.basename(path), line, tag, value)
             for tag, line, value in p.found if value not in seen_by_regex]
    regex_only = [(os.path.basename(path), v) for v in sorted(seen_by_regex - seen_by_parser)]
    return findings, delta, errors, regex_only


def check(paths, strict=False):
    print("inline-style parse gate (⬛ ADVISORY at birth, #221 — the #122 seed)")
    print("  reader: html.parser (stdlib) · population: %d file(s) · scope: DEF-004's own "
          "property families" % len(paths))
    all_find, all_delta, all_err, all_regex_only, n_attrs = [], [], [], [], 0
    for p in paths:
        f, d, e, ro = read_file(p)
        all_find += f
        all_delta += d
        all_regex_only += ro
        all_err += [(os.path.basename(p), x) for x in e]
        parser = StyleAttrParser()
        try:
            parser.feed(open(p, encoding="utf-8", errors="replace").read())
            parser.close()
            n_attrs += len(parser.found)
        except Exception as ex:
            all_err.append((os.path.basename(p), "%s: %s" % (type(ex).__name__, ex)))
    print("  %d style attribute(s) parsed · %d hardcode finding(s) · %d PARSER-ONLY (the regex "
          "is blind) · %d REGEX-ONLY (the regex hallucinates)"
          % (n_attrs, len(all_find), len(all_delta), len(all_regex_only)))
    for name, line, tag, prop, val in all_find[:40]:
        print("  ⚠ %s:%d <%s style=\"…%s:%s…\"> — raw px in a style attribute; DEF-004 says "
              "styling must be a token so MODES can override it" % (name, line, tag, prop, val))
    for name, line, tag, value in all_delta[:20]:
        print("  ⬛ PARSER-ONLY: %s:%d <%s> carries a style attribute the tree's "
              "`style=\"([^\"]*)\"` pattern does not match: %r" % (name, line, tag, value[:70]))
    for name, value in all_regex_only[:20]:
        print("  ⬛ REGEX-ONLY: %s — the tree's pattern reads this as a live style attribute; a "
              "parse of the static document does NOT. It is in a comment, a <script> string, or "
              "a text node: %r" % (name, value[:70]))
    if all_regex_only:
        print("     ⚠ READ THIS CAREFULLY BEFORE ACTING ON IT — a REGEX-ONLY hit is not")
        print("       automatically the regex being wrong. The one on this tree today is inside a")
        print("       `card.innerHTML='…'` string, so the static parse is right about the DOCUMENT")
        print("       and the value is nonetheless real at RUNTIME. The honest conclusion is that")
        print("       NEITHER reader is authoritative over injected markup, and this gate reports")
        print("       the disagreement rather than picking a winner. [[measure-dont-convert-units]]")
    if all_err:
        print("  ⛔ PARSE ERRORS — a crash is not a fail, and these are named rather than swallowed:")
        for name, e in all_err[:10]:
            print("     · %s: %s" % (name, e))
    if not all_find and not all_delta and not all_err:
        print("  ✅ every style attribute in the population parses, and every declaration in one "
              "is either untouched by DEF-004 or already a token.")
    if strict:
        return 1 if (all_find or all_err) else 0
    print("  ⬛ ADVISORY: exit 0 regardless. This is ONE parser over the NARROWEST population "
          "where a parser would have caught a proved false green (#220-L1 finding 12).")
    print("  ⬛ Widening it to the other seven regex gates is PRICED, not built, and whether a "
          "non-stdlib CSS parser may enter the gate set is DAVE'S.")
    return 0


# ── KNOWN-ANSWER TEST ────────────────────────────────────────────────────────────────────────
# Every arm is a PAIR. The FIRES arms plant a declaration and demand a finding; the SILENT arms
# are the discrimination controls. The DELTA arms are the ones that justify the whole file: each
# is a real artefact shape that a browser applies and the tree's regex reader cannot see.
FIRES = [
    ("the exact #220-L1 finding-12 mutant, three hardcodes in one attribute",
     '<div style="padding:13px;border-radius:7px;border-width:5px">x</div>', 3),
    ("a logical longhand in an attribute", '<div style="margin-block-start:9px">x</div>', 1),
    ("a corner radius longhand in an attribute", '<i style="border-top-left-radius:7px"></i>', 1),
    ("an attribute on a self-closing tag", '<img style="padding-inline:11px"/>', 1),
]
SILENT = [
    ("the token route", '<div style="padding:var(--space-2);border-width:var(--bw-1)">x</div>'),
    ("px inside a var() fallback", '<div style="gap:var(--space-2, 8px)">x</div>'),
    ("geometry is the other axis", '<div style="width:13px;top:4px;font-size:12px">x</div>'),
    ("a transparent border is a shape, not a stroke",
     '<div style="border-width:3px;border-style:solid;border-color:transparent">x</div>'),
    ("no style attribute at all", '<div class="ok">x</div>'),
    ("a <style> BLOCK is not this gate's business — that is _validate_no_hardcode.py's",
     '<style>.x{padding:13px}</style>'),
]
# ⚠ THIS LIST IS SHORTER THAN ITS FIRST DRAFT, AND THAT IS THE BITE DOING ITS JOB. Two shapes
# were proposed as parser-only and the selftest refused both, correctly: an attribute broken
# across a NEWLINE is matched by `style="([^"]*)"` (a negated character class already spans
# lines), and an attribute FOLLOWING one that contains a double quote is matched too. Both
# hypotheses were wrong. They are recorded here rather than deleted, because a delta list padded
# with shapes the regex already handles would inflate the one number this gate exists to report.
DELTA = [
    ("a single-quoted attribute", "<div style='padding:13px'>x</div>"),
    ("an entity-escaped colon — the browser resolves it, a source regex never does",
     '<div style="padding&#58;13px">x</div>'),
]
# The other direction: text the tree's regex reads as a live style attribute and no browser
# applies. A gate that fires on one of these accuses an artefact of a defect it does not have.
REGEX_ONLY = [
    ("a style attribute inside an HTML comment",
     '<!-- <div style="padding:13px">was here</div> -->'),
    ("a style attribute inside a <script> string",
     '<script>var s = \'<div style="padding:13px">\';</script>'),
]


def selftest():
    import tempfile
    fails = []
    d = tempfile.mkdtemp(prefix="inline-style-selftest-")

    def at(fragment):
        p = os.path.join(d, "probe.html")
        open(p, "w").write("<html><body>%s</body></html>" % fragment)
        try:
            return read_file(p)
        finally:
            os.remove(p)

    try:
        for name, frag, least in FIRES:
            f, _d, e, _ro = at(frag)
            if len(f) < least:
                fails.append("PLANTED DEFECT NOT CAUGHT — %s (wanted >=%d, got %d)"
                             % (name, least, len(f)))
            if e:
                fails.append("PARSE ERROR on a fixture that must parse — %s: %s" % (name, e))
        for name, frag in SILENT:
            f, _d, e, _ro = at(frag)
            if f:
                fails.append("CLEAN INPUT FLAGGED — %s (got %s)" % (name, f))
            if e:
                fails.append("PARSE ERROR on a clean fixture — %s: %s" % (name, e))
        # ⛔ THE ARMS THAT JUSTIFY THE FILE. Each must be (a) seen by the parser and (b) NOT
        # seen by the tree's regex — a delta arm that both readers catch proves nothing.
        for name, frag in DELTA:
            _f, delta, _e, _ro = at(frag)
            if not delta:
                fails.append("DELTA ARM EMPTY — %s: the parser did not report an attribute the "
                             "tree's regex misses, so this gate's reason for existing is "
                             "unproven on that shape" % name)
        for name, frag in REGEX_ONLY:
            _f, _delta, _e, ro = at(frag)
            if not ro:
                fails.append("REGEX-ONLY ARM EMPTY — %s: the gate did not report a string the "
                             "tree's pattern reads as a live attribute and the browser ignores"
                             % name)
            if not TREE_ATTR_RE.findall(frag):
                fails.append("REGEX-ONLY ARM WRONG — %s: the tree's pattern does not match it "
                             "either, so the fixture proves nothing" % name)
        # CONTROL for both deltas: a plain double-quoted attribute must be in NEITHER bucket, or
        # every attribute would be in one and the numbers would be noise
        _f, delta, _e, ro = at('<div style="padding:13px">x</div>')
        if delta or ro:
            fails.append("DELTA CONTROL FAILED — a plain double-quoted attribute landed in a "
                         "delta bucket (parser-only=%s regex-only=%s)" % (delta, ro))
        # population control: the gate must have something to read
        if not population():
            fails.append("POPULATION EMPTY — the gate would print a green over nothing")
    finally:
        os.rmdir(d)
    print("inline-style parse selftest: %d planted · %d clean · %d parser-only · %d regex-only "
          "+ 2 controls · %d failure(s)"
          % (len(FIRES), len(SILENT), len(DELTA), len(REGEX_ONLY), len(fails)))
    for f in fails:
        print("  ⛔ " + f)
    return 1 if fails else 0


def population():
    return sorted(f for f in glob.glob(os.path.join(PROFORMA, "*.html"))
                  if 'id="icon-manifest"' in open(f, encoding="utf-8", errors="replace").read())


def main():
    if "--selftest" in sys.argv:
        return selftest()
    return check(population(), strict="--strict" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
