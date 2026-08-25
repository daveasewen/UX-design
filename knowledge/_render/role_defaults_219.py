#!/usr/bin/env python3
"""
role_defaults_219.py — THE TWELVE SHIPPED BENTO ROLE DEFAULTS (s219-D1), ONE HOME.

WHY IT EXISTS — s219-D1 (#219, Dave, 2026-08-25), his words:
  "I'll give you the defaults for each, but what I want is options during the edit pass that
   Apollo will have in the end. I don't think its as simple as one decision for each theme,
   certainly not for the gallery."
  "I basically want all the options available for edit mode but these are the defaults."
The ruling closes a role setting as a DEFAULT plus an EDIT-PASS OPTION SET, and names the twelve
verbatim tuner exports (three types x four themes) as the SHIPPED DEFAULTS.

⛔ NOTHING HERE IS TYPED. The twelve state blocks are PARSED out of Dave's own receipt,
`notes/_receipts/2026-08-25-219-role-defaults-exports.md`, at import time. A default re-typed into
Python is a second copy of a decision, and the copy is the one that goes stale
([[write-once-principle-floated-192]] / ADR-0017: live facts get ONE home and everything else
holds an address). The receipt is the home; this module is its parser.
⛔ AND IT IMPORTS NOTHING OF THE RENDER STACK — deliberately. `gen_foundations_217` imports
`gen_bento_matrix_217`, so a defaults table living in either of them cannot be read by the other
without a cycle. This module imports only the standard library, so BOTH may consume it: the
explorer's boot STATE and the library's compiled settings can be the same twelve values rather
than two tables that agree today.

WHAT A CONSUMER GETS
  DEFAULTS[type][theme]        -> the export's `state` block (the RULING)
  RESOLVED[type][theme]        -> the export's `resolved` block (the RECEIPT: pixels Dave saw)
  SPACING_STOPS                -> s219-D1 (4), the ruled stop set {1, 2, 4, 16, 24, 40}
  DIALS[type]                  -> the dial names that type's grammar carries
  spacing_px(word)             -> "40px" for a ruled stop; a NAMED refusal otherwise
  state(type, theme)           -> one state block, refusing loudly on an unknown pair

⚠ THE `resolved` BLOCKS ARE RECEIPTS, NOT SETTINGS ([[premise-ages-faster-than-rule]]). They are
what the tuner measured in the tab the export was taken in, all twelve in `mode: light`. They are
carried so a probe can cross-check a minted value against the pixels Dave actually approved — the
mono gallery caption resolving `rgb(240, 240, 240)` is how `--surface-subtle` was IDENTIFIED as
the token behind his `capBg: grey`. They are never the source of a declaration.
⚠ EVERY `resolved` BLOCK IN THE DISPLAY SET SAYS `"role": "brochureware"` — the tuner's resolver
still emits the pre-s217-D5 word for the role s217-D5 renamed DISPLAY. The exports are frozen
history and keep the old word; `TYPE_ROLE` in gen_bento_matrix_217 is the ONE place the rename
lives, and consumers ask it rather than reading the receipt's word.

RUN IT
  python3 knowledge/_render/role_defaults_219.py --table     # the twelve, as parsed
  python3 knowledge/_render/role_defaults_219.py --selftest  # the parse, probed
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
RECEIPT = os.path.join(ROOT, "notes", "_receipts", "2026-08-25-219-role-defaults-exports.md")

# The order Dave's own matrix uses, and the order every table in the library prints.
THEMES = ["mono", "legacy", "console", "supercharge"]
TYPES = ["dashboard", "display", "gallery"]

# ⬛ s219-D1 (4) — THE SPACING RAILS. Dave option-selected the six stops: "These six stops".
# The edit pass picks AMONG stops; a free value is not reachable and widening the set is a ruling.
# ⚠ THIS IS WIDER THAN THE EXPLORER'S CONTROL AS SHIPPED. `gen_bento_matrix_217.SPACINGS` carries
# three (1 / 24 / 40) — the s217-D5 trio — and Dave's display defaults use 2 and 16, which that
# control cannot currently reach. The gap is REPORTED by `unreachable_stops()` rather than papered
# over here: a default no control can select is a default nobody can return to after an edit.
SPACING_STOPS = ["1", "2", "4", "16", "24", "40"]

# ⚠ THE SUB-BENTO LADDER IS NOT MIRRORED HERE, DELIBERATELY. s217-D6 ruled it as Dave's typed
# ladder (1,2,4,8,12,16,20,24) and s219-D1 (4) re-rules every spacing dial onto the six rails, so
# a copy in this module would have been a THIRD answer to a question already re-ruled once today
# ([[premise-ages-faster-than-rule]]). The live control is `gen_bento_matrix_217.SUB_STOPS`, and
# `gen_foundations_217.validate_settings("dashboard")` asks the defaults against THAT — so a sub
# default the shipped slider cannot reach is a complaint, whichever ladder is in force.

# The dial grammar per type, taken from the exports themselves at parse time and asserted against
# this table — so a receipt that grew or lost a dial is a LOUD refusal, not a quiet KeyError.
DIALS = {
    "dashboard": ["mainSpacing", "subSpacing", "keylines", "pageBg", "bentoBg"],
    "display": ["spacing", "keylines", "pageBg", "bentoBg"],
    "gallery": ["spacing", "keylines", "mode", "edge", "rounding", "pageBg", "bentoBg", "capBg"],
}


class RoleDefaultsError(Exception):
    """A parse that cannot answer must REFUSE by name. A defaults table that fell back to a
    plausible value would ship a wall nobody ruled and no gate would fire."""


_TYPE_H2 = re.compile(r"^##\s+([A-Z]+)\s*$", re.M)
_THEME_H3 = re.compile(r"^###\s+([a-z]+)\s*$", re.M)
_FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)


def _parse(path=RECEIPT):
    """-> (defaults, resolved, receipt_theme). The receipt's twelve export blocks, keyed
    [type][theme], with the HEADINGS as the authority for which theme a block belongs to.

    ⛔ THE HEADING RULES, NOT THE `resolved.theme` FIELD, and #218 is why: two of that session's
    four exports were taken in the legacy tab and their `resolved` blocks say `legacy` for a mono
    and a supercharge setting. The heading is Dave's label; `resolved.theme` is the tab the
    measurement was taken in. Both are kept, and a disagreement is REPORTED rather than smoothed
    ([[premise-ages-faster-than-rule]])."""
    if not os.path.exists(path):
        raise RoleDefaultsError(
            "the #219 role-defaults receipt is not on disk (%s) — the twelve shipped defaults have "
            "no home to be read from, and this module will not invent them." % path)
    src = open(path, encoding="utf-8").read()
    # Walk the document once, carrying the current ## TYPE and ### theme headings.
    marks = []
    for m in _TYPE_H2.finditer(src):
        marks.append((m.start(), "type", m.group(1).lower()))
    for m in _THEME_H3.finditer(src):
        marks.append((m.start(), "theme", m.group(1).lower()))
    for m in _FENCE.finditer(src):
        marks.append((m.start(), "block", m.group(1)))
    marks.sort(key=lambda x: x[0])

    defaults, resolved, receipt_theme = {}, {}, {}
    cur_type = cur_theme = None
    for _pos, kind, val in marks:
        if kind == "type":
            cur_type = val if val in TYPES else None
        elif kind == "theme":
            cur_theme = val
        elif kind == "block":
            if cur_type is None or cur_theme is None:
                continue
            try:
                obj = json.loads(val)
            except ValueError as e:
                raise RoleDefaultsError("the %s/%s export block is not valid JSON (%s)"
                                        % (cur_type, cur_theme, e))
            if obj.get("type") != cur_type:
                raise RoleDefaultsError(
                    "the block under '## %s / ### %s' declares type %r — the receipt's own "
                    "headings and its JSON disagree about which grammar this is"
                    % (cur_type.upper(), cur_theme, obj.get("type")))
            if cur_theme not in THEMES:
                raise RoleDefaultsError("unknown theme heading %r in the receipt" % cur_theme)
            defaults.setdefault(cur_type, {})[cur_theme] = dict(obj["state"])
            resolved.setdefault(cur_type, {})[cur_theme] = dict(obj.get("resolved") or {})
            receipt_theme.setdefault(cur_type, {})[cur_theme] = (
                (obj.get("resolved") or {}).get("theme"))

    missing = [(t, th) for t in TYPES for th in THEMES
               if th not in defaults.get(t, {})]
    if missing:
        raise RoleDefaultsError(
            "the receipt does not carry all twelve exports — missing %s. s219-D1 (3) rules the "
            "TWELVE as the shipped defaults; a partial set is not a default set." % missing)
    for t in TYPES:
        for th in THEMES:
            got = sorted(defaults[t][th])
            if got != sorted(DIALS[t]):
                raise RoleDefaultsError(
                    "%s/%s carries dials %s — this module's grammar for %s is %s. A receipt that "
                    "grew or lost a dial must refuse, not be read through a stale shape."
                    % (t, th, got, t, sorted(DIALS[t])))
    return defaults, resolved, receipt_theme


DEFAULTS, RESOLVED, RECEIPT_RESOLVED_THEME = _parse()


def state(type_, theme):
    """-> ONE export state block. An unknown pair is a NAMED refusal, never a default."""
    try:
        return DEFAULTS[type_][theme]
    except KeyError:
        raise RoleDefaultsError(
            "no #219 default for type=%r theme=%r — the ruled set is %s x %s"
            % (type_, theme, TYPES, THEMES))


def spacing_px(word):
    """-> the CSS length for a ruled spacing stop (s219-D1 (4)). ⛔ A value off the rails is a
    refusal: the edit pass picks among stops, and a free number is not a reachable state."""
    if str(word) not in SPACING_STOPS:
        raise RoleDefaultsError(
            "spacing %r is not one of the ruled stops %s (s219-D1 (4)); widening the set is a "
            "ruling, not a build decision." % (word, "/".join(SPACING_STOPS)))
    return "%spx" % word


def unreachable_stops(control_stops):
    """-> the ruled stops a CONTROL cannot reach. `control_stops` is the consumer's own option set
    (e.g. [s[0] for s in gen_bento_matrix_217.SPACINGS]).

    ⚠ REPORTED, NEVER REPAIRED HERE. s219-D1 (2) rules that all dials are available in edit mode;
    a ruled stop with no control is an edit-pass value the designer cannot return to. Which
    control grows, and where, is the explorer's own build to make."""
    return [s for s in SPACING_STOPS if s not in list(control_stops)]


def used_stops():
    """-> the stops the twelve defaults actually SIT on, main and sub, measured off the parse."""
    main, sub = set(), set()
    for t in TYPES:
        for th in THEMES:
            s = DEFAULTS[t][th]
            main.add(s.get("spacing") or s.get("mainSpacing"))
            if "subSpacing" in s:
                sub.add(s["subSpacing"])
    return sorted(main, key=lambda v: int(v)), sorted(sub, key=lambda v: int(v))


def table():
    """-> the twelve, one line each, for a human and for the report."""
    out = []
    for t in TYPES:
        for th in THEMES:
            s = DEFAULTS[t][th]
            out.append("  %-9s %-11s %s" % (t, th, " · ".join(
                "%s=%s" % (d, s[d]) for d in DIALS[t])))
    return "\n".join(out)


def selftest():
    fails = []
    main, sub = used_stops()
    off = [v for v in main if v not in SPACING_STOPS]
    if off:
        fails.append("main spacing values off the ruled rails: %s" % off)
    off_sub = [v for v in sub if v not in SPACING_STOPS]
    if off_sub:
        fails.append("sub spacing values off the ruled rails %s: %s" % (SPACING_STOPS, off_sub))
    # s219-D1 (5) hand-computed against the ruling's own sentence, never read off the parse.
    want_main = {"legacy": "24", "mono": "40", "console": "40", "supercharge": "24"}
    want_sub = {"legacy": "4", "mono": "4", "console": "4", "supercharge": "2"}
    for th in THEMES:
        got = DEFAULTS["dashboard"][th]
        if got["mainSpacing"] != want_main[th] or got["subSpacing"] != want_sub[th]:
            fails.append("dashboard/%s is %s/%s — s219-D1 (5) names %s/%s"
                         % (th, got["mainSpacing"], got["subSpacing"],
                            want_main[th], want_sub[th]))
    # s219-D2 (2) / (3) / (4), likewise hand-computed off the ruling's words.
    if sorted({DEFAULTS["gallery"][th]["edge"] for th in THEMES}) != ["square"]:
        fails.append("s219-D2 (2) rules SQUARE the gallery default in all four themes")
    if DEFAULTS["gallery"]["console"]["rounding"] != "capsule":
        fails.append("s219-D2 (3) rules the console gallery rounding CAPSULE")
    on = sorted("%s/%s" % (t, th) for t in TYPES for th in THEMES
                if DEFAULTS[t][th]["keylines"] == "on")
    if on != ["display/legacy", "gallery/legacy"]:
        fails.append("s219-D2 (4) rules keylines ON only in legacy display and legacy gallery; "
                     "the parse says %s" % on)
    if DEFAULTS["gallery"]["mono"]["capBg"] != "grey":
        fails.append("s219-D2 (1) supersedes the mono caption ground to light grey")
    # the receipt's own pixel readback for that supersession, so the token behind `grey` stays
    # identifiable from the data rather than from a comment
    if RESOLVED["gallery"]["mono"].get("captionBackground") != "rgb(240, 240, 240)":
        fails.append("the mono gallery receipt no longer resolves rgb(240, 240, 240) — the "
                     "identification of --surface-subtle rests on that readback")
    if fails:
        print("role_defaults_219 --selftest: %d FAILURE(S)" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        return 1
    print("role_defaults_219 --selftest OK — 12 exports parsed from %s"
          % os.path.relpath(RECEIPT, ROOT))
    print("   main stops used %s · sub stops used %s · ruled rails %s"
          % (main, sub, SPACING_STOPS))
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    print("THE TWELVE #219 SHIPPED DEFAULTS (s219-D1), parsed from %s\n"
          % os.path.relpath(RECEIPT, ROOT))
    print(table())
    return 0


if __name__ == "__main__":
    sys.exit(main())
