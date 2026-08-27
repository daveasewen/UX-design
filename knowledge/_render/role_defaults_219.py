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

⬛ AND THE RECEIPT IS NOT THE LAST WORD — s220-D2 (2), #220, 2026-08-27. Dave superseded two dials
of his own console gallery export in chat: "if you are asking for a default lets go with rounded
corner image with transparent capsule" and, over the light/dark pair, "I guess this would be the
default for the two modes." A supersession is APPLIED OVER the parse by `SUPERSESSIONS` below; the
receipt is never rewritten. His word outranks his own export (the s219-D2 (1) latest-wins pattern),
and the export stays on disk as the RECEIPT of what he approved at #219.

WHAT A CONSUMER GETS
  DEFAULTS[type][theme]        -> the SHIPPED default: the export's `state` block with every ruled
                                  supersession applied (the RULING as it stands today)
  RECEIPT_DEFAULTS[type][theme]-> the export's `state` block AS PARSED, frozen history
  SUPERSESSIONS                -> the ruled overrides, each naming its ruling, the receipt's word,
                                  the word that replaced it and Dave's own sentence
  RESOLVED[type][theme]        -> the export's `resolved` block (the RECEIPT: pixels Dave saw)
  RESOLVED_SUPERSEDED[type][theme] -> {receipt field: why} — the `resolved` readbacks a supersession
                                  has made STALE, so a probe declares the divergence instead of
                                  cross-checking a shipped page against a retired default
  SPACING_STOPS                -> s219-D1 (4), the ruled stop set {1, 2, 4, 16, 24, 40}
  DIALS[type]                  -> the dial names that type's grammar carries
  MODES                        -> the two modes a default answers for (s220-D2 (2): ONE default,
                                  both modes — the twelve state blocks carry no mode axis)
  spacing_px(word)             -> "40px" for a ruled stop; a NAMED refusal otherwise
  state(type, theme)           -> one state block, refusing loudly on an unknown pair
  default_for_mode(t, th, m)   -> the same block for `light` and for `dark`; an unknown mode is a
                                  NAMED refusal. This is s220-D2 (2)'s "default for the two modes"
                                  as machinery rather than as a comment.

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


RECEIPT_DEFAULTS, RESOLVED, RECEIPT_RESOLVED_THEME = _parse()

# ---------------------------------------------------------------------------
# ⬛ s220-D2 (2) — THE CONSOLE GALLERY DEFAULT BECOMES CHORD TWO, IN BOTH MODES
# ---------------------------------------------------------------------------
# Dave, #220, off reviews/CORRECTION-READINGS-2026-08-27-v1.html:
#   "these 4 are all \"legal\". but if you are asking for a default lets go with rounded corner
#    image with transparent capsule"
#   and over the light/dark pair: "I guess this would be the default for the two modes"
# s219-D3(3) names that pair CHORD TWO — `rounding: corners` on the image, `capBg: transparent`.
# It supersedes s219-D2 (3)'s capsule default AND the console-gallery capsule+grey rows of the
# s219-D1 (3) tuner exports, and it aligns console's gallery default with legacy and supercharge.
#
# ⛔ THE SUPERSESSION IS A LAYER, NOT AN EDIT. The receipt
# (`notes/_receipts/2026-08-25-219-role-defaults-exports.md`) is a RECEIPT — the twelve verbatim
# exports Dave took in his own tuner. Rewriting a row of it to match a later ruling would destroy
# the evidence of what he approved at #219 and leave the supersession invisible
# ([[header-wins-over-audit]]: add to a ratified record, never trim it). So the parse above is kept
# whole as `RECEIPT_DEFAULTS`, and every override below states the word it replaces — which is
# ASSERTED against the receipt at import time, so an edited receipt is a LOUD refusal rather than
# a silently absorbed change.
#
# ⛔ NOTHING HERE REMOVES AN OPTION. s220-D2 (1): "these 4 are all 'legal'" — all four caption
# treatments stay reachable in the edit pass. A supersession moves the DEFAULT and touches no
# option set; readings A and B, which would have removed options, are REJECTED by the same ruling.
# The option space lives in `gen_bento_matrix_217` (ROUNDINGS / GROUND_RAMP / capbg_for) and this
# module cannot reach it — the separation is the guarantee, and `gen_foundations_217`'s selftest
# asserts it where both are in scope.
#
# ⛔ MONO IS NOT HERE, AND ITS ABSENCE IS THE RULING. s220-D2 (3) leaves mono's gallery default
# (`capBg: grey`) EXPRESSLY OPEN — asked in chat, not ruled — so it keeps grey until Dave's word.
# `no_supersession` below is a positive statement of that, not an oversight, and the selftest bites
# it in both directions.
SUPERSESSIONS = [
    {
        "type": "gallery", "theme": "console", "dial": "rounding",
        "was": "capsule", "now": "corners",
        "ruled_by": "s220-D2 (2)",
        "supersedes": "s219-D2 (3) · the s219-D1 (3) console gallery export",
        "modes": "both — one default, identical in light and dark",
        "dave": "if you are asking for a default lets go with rounded corner image with "
                "transparent capsule",
    },
    {
        "type": "gallery", "theme": "console", "dial": "capBg",
        "was": "grey", "now": "transparent",
        "ruled_by": "s220-D2 (2)",
        "supersedes": "the s219-D1 (3) console gallery export (capsule + grey ground)",
        "modes": "both — one default, identical in light and dark",
        "dave": "I guess this would be the default for the two modes",
    },
]

# (type, theme) pairs a ruling has EXPRESSLY left alone, so an absence can be read as a decision.
NO_SUPERSESSION = {
    ("gallery", "mono"): "s220-D2 (3) — mono's gallery default (capBg: grey) is EXPRESSLY OPEN: "
                         "asked in chat, not ruled. It keeps grey until Dave's word.",
}

# The two modes a default answers for. ⛔ NOT A NEW AXIS: the twelve state blocks carry no mode
# dimension and s220-D2 (2) rules that they should not — "the default for the two modes" is ONE
# default that both modes render. The tuple exists so `default_for_mode` can refuse a third word.
MODES = ("light", "dark")


def _apply_supersessions(receipt):
    """-> (live defaults, {(type,theme): {resolved field: why}}). LOUD on any disagreement.

    ⛔ THE `was` FIELD IS A GATE, NOT A COMMENT. If the receipt no longer says what the
    supersession claims to be superseding, the two records have drifted and this module refuses
    rather than applying an override to a word nobody ruled about
    ([[premise-ages-faster-than-rule]])."""
    live = {t: {th: dict(s) for th, s in per.items()} for t, per in receipt.items()}
    stale = {}
    # which `resolved` readback each dial's pixels live under, so a superseded dial can name the
    # receipt field it has made stale instead of leaving a probe to cross-check a retired default.
    field_for = {"capBg": "captionBackground", "bentoBg": "bentoBackground",
                 "pageBg": "pageBackground", "rounding": "tileRadiusPx",
                 "keylines": "tileBorderPx"}
    for sup in SUPERSESSIONS:
        t, th, dial = sup["type"], sup["theme"], sup["dial"]
        if t not in live or th not in live[t]:
            raise RoleDefaultsError(
                "%s supersedes %s/%s, which the receipt does not carry" % (sup["ruled_by"], t, th))
        if dial not in DIALS[t]:
            raise RoleDefaultsError(
                "%s supersedes the dial %r, which is not part of the %s grammar (%s)"
                % (sup["ruled_by"], dial, t, "/".join(DIALS[t])))
        if (t, th) in NO_SUPERSESSION:
            raise RoleDefaultsError(
                "%s supersedes %s/%s, which is EXPRESSLY left alone: %s"
                % (sup["ruled_by"], t, th, NO_SUPERSESSION[(t, th)]))
        got = receipt[t][th][dial]
        if got != sup["was"]:
            raise RoleDefaultsError(
                "%s says it supersedes %s/%s.%s = %r, but the receipt says %r. The receipt is "
                "FROZEN HISTORY and a supersession may not be applied to a word nobody ruled "
                "about — reconcile the two records before this module can answer."
                % (sup["ruled_by"], t, th, dial, sup["was"], got))
        if sup["was"] == sup["now"]:
            raise RoleDefaultsError(
                "%s supersedes %s/%s.%s with the value it already has (%r) — an override that "
                "changes nothing is a record of a decision that did not happen"
                % (sup["ruled_by"], t, th, dial, sup["now"]))
        live[t][th][dial] = sup["now"]
        fld = field_for.get(dial)
        if fld:
            stale.setdefault(t, {}).setdefault(th, {})[fld] = (
                "%s moved %s from %r to %r; this readback is the pixel the RETIRED default "
                "resolved and no longer describes the shipped page"
                % (sup["ruled_by"], dial, sup["was"], sup["now"]))
    return live, stale


DEFAULTS, RESOLVED_SUPERSEDED = _apply_supersessions(RECEIPT_DEFAULTS)


def supersession_rows():
    """-> the ruled overrides as flat rows, for a manifest or a report. The receipt's word is
    carried BESIDE the live one — a supersession that printed only the new value would read as if
    the export had always said it."""
    return [{"type": s["type"], "theme": s["theme"], "dial": s["dial"],
             "receipt": s["was"], "shipped": s["now"], "ruled_by": s["ruled_by"],
             "supersedes": s["supersedes"], "modes": s["modes"], "dave": s["dave"]}
            for s in SUPERSESSIONS]


def superseded_dials(type_, theme):
    """-> {dial: the receipt's retired word} for one intersection; {} where nothing was ruled."""
    return {s["dial"]: s["was"] for s in SUPERSESSIONS
            if s["type"] == type_ and s["theme"] == theme}


def state(type_, theme):
    """-> ONE export state block. An unknown pair is a NAMED refusal, never a default."""
    try:
        return DEFAULTS[type_][theme]
    except KeyError:
        raise RoleDefaultsError(
            "no #219 default for type=%r theme=%r — the ruled set is %s x %s"
            % (type_, theme, TYPES, THEMES))


def default_for_mode(type_, theme, mode):
    """-> the shipped default block for ONE mode. ⬛ s220-D2 (2) — "I guess this would be the
    default for the two modes": there is ONE default and both modes render it, so this returns the
    SAME block for `light` and for `dark`.

    ⛔ IT EXISTS TO BE ASKED, NOT TO BRANCH. A caller that wants a per-mode default has to widen
    this function, and widening it is a ruling — which is the whole difference between a default
    that happens to be the same in both modes today and one Dave ruled identical
    ([[translate-prose-into-machinery]]). An unknown mode is a NAMED refusal, never a default."""
    if mode not in MODES:
        raise RoleDefaultsError(
            "mode %r is not one of %s — a default answers for the two modes (s220-D2 (2)) and a "
            "third mode is not a thing this grammar has." % (mode, "/".join(MODES)))
    return state(type_, theme)


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
    """-> the twelve SHIPPED defaults, one line each, for a human and for the report. A dial a
    ruling superseded prints the receipt's retired word beside it — a table that showed only the
    live value would read as if the export had always said it."""
    out = []
    for t in TYPES:
        for th in THEMES:
            s, sup = DEFAULTS[t][th], superseded_dials(t, th)
            bits = []
            for d in DIALS[t]:
                bits.append("%s=%s%s" % (d, s[d],
                                         " (was %s)" % sup[d] if d in sup else ""))
            out.append("  %-9s %-11s %s" % (t, th, " · ".join(bits)))
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
    # ⬛ s220-D2 (2) — THE CONSOLE GALLERY DEFAULT IS CHORD TWO, AND THE RECEIPT STILL SAYS CAPSULE.
    # Both halves are asserted: the shipped pair, and the frozen row it superseded. A bite that
    # only checked the new value would go green the day someone "tidied" the receipt to match, and
    # the evidence of what Dave approved at #219 would be gone with no gate firing.
    live_console = DEFAULTS["gallery"]["console"]
    if (live_console["rounding"], live_console["capBg"]) != ("corners", "transparent"):
        fails.append("s220-D2 (2) rules the console gallery default CHORD TWO — rounding=corners, "
                     "capBg=transparent; the live table says rounding=%s, capBg=%s"
                     % (live_console["rounding"], live_console["capBg"]))
    rec_console = RECEIPT_DEFAULTS["gallery"]["console"]
    if (rec_console["rounding"], rec_console["capBg"]) != ("capsule", "grey"):
        fails.append("the #219 receipt's console gallery export no longer reads capsule + grey "
                     "(it reads %s + %s) — s219-D2 (3) and the export are FROZEN HISTORY and the "
                     "supersession layer is what moves the shipped default, never the receipt"
                     % (rec_console["rounding"], rec_console["capBg"]))
    # ⬛ s220-D2 (2) — ONE DEFAULT, BOTH MODES. Driven through the accessor rather than asserted in
    # prose, and the third mode is driven too: a refusal nobody tries to cross is not a fence
    # ([[instrument-without-a-consumer]]).
    if default_for_mode("gallery", "console", "light") != \
            default_for_mode("gallery", "console", "dark"):
        fails.append("s220-D2 (2) rules ONE console gallery default for the two modes; "
                     "default_for_mode returns two different blocks")
    try:
        default_for_mode("gallery", "console", "auto")
        fails.append("default_for_mode accepted a mode outside %s — an unknown mode must be a "
                     "NAMED refusal, never a default" % (MODES,))
    except RoleDefaultsError:
        pass
    # ⬛ s220-D2 (3) — MONO'S GALLERY DEFAULT IS UNCHANGED, and the absence is asserted as a
    # DECISION. Three clauses: the live block is byte-identical to the receipt's, no supersession
    # names mono, and the ground is still `grey`. ⛔ A later lane that moves mono to match console
    # reds here by name rather than sliding through on the console bite.
    if DEFAULTS["gallery"]["mono"] != RECEIPT_DEFAULTS["gallery"]["mono"]:
        fails.append("s220-D2 (3) leaves mono's gallery default EXPRESSLY OPEN — the live block "
                     "must equal the receipt's, and it does not (%s vs %s)"
                     % (DEFAULTS["gallery"]["mono"], RECEIPT_DEFAULTS["gallery"]["mono"]))
    if superseded_dials("gallery", "mono"):
        fails.append("a supersession names gallery/mono, which s220-D2 (3) leaves OPEN: %s"
                     % superseded_dials("gallery", "mono"))
    # ⬛ THE SUPERSESSION LAYER TOUCHES NOTHING IT DOES NOT NAME. Every other intersection must be
    # the receipt's, unchanged — a default switch that leaked would be exactly the removal
    # s220-D2 (1) rejects, and the leak would be invisible one intersection at a time.
    named = {(s["type"], s["theme"]) for s in SUPERSESSIONS}
    leaked = sorted("%s/%s" % (t, th) for t in TYPES for th in THEMES
                    if (t, th) not in named and DEFAULTS[t][th] != RECEIPT_DEFAULTS[t][th])
    if leaked:
        fails.append("the supersession layer changed %s, which no ruling names — a default switch "
                     "that reaches an intersection it did not name is a change nobody ruled"
                     % leaked)
    # and inside the one intersection it DOES name, only the two ruled dials moved.
    moved = sorted(d for d in DIALS["gallery"]
                   if DEFAULTS["gallery"]["console"][d] != RECEIPT_DEFAULTS["gallery"]["console"][d])
    if moved != ["capBg", "rounding"]:
        fails.append("s220-D2 (2) moves exactly `rounding` and `capBg` on console gallery; "
                     "the layer moved %s" % moved)
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
    print("\nRULED SUPERSESSIONS — applied over the receipt, which is FROZEN HISTORY:")
    if not SUPERSESSIONS:
        print("  (none)")
    for r in supersession_rows():
        print("  %s/%s.%s  %s → %s   [%s, %s]\n     supersedes %s\n     Dave: \"%s\""
              % (r["type"], r["theme"], r["dial"], r["receipt"], r["shipped"],
                 r["ruled_by"], r["modes"], r["supersedes"], r["dave"]))
    for (t, th), why in sorted(NO_SUPERSESSION.items()):
        print("  ⛔ %s/%s EXPRESSLY OPEN — %s" % (t, th, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
