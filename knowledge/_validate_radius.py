#!/usr/bin/env python3
"""
_validate_radius.py — radius gate (build-out Phase 0, 2026-07-21).

Shape / border-radius is a THEME FLEX SLOT (ADR-0010; Dave 2026-07-21: divergence
axes — UI greys, shape/border-radius, future input error-condition — are
theme-overridable, NEVER hardcoded; Console = rounded NOW). A hardcoded
`border-radius:0` freezes a component square in every theme, which is exactly the
defect this session de-hardcoded out of canon.css (37 declarations).

RULE — every `border-radius` declaration (comments stripped) must be one of:
  * var(...)      the token route: var(--border-radius-default)
  * 50%           a genuine circle (avatar, radio, spinner, dot)
  * 999px         the pill idiom (badge, switch, tab-bar segment — deliberately
                  fully-round in every theme; distinct from the theme flex slot)
  * inherit
Anything else — `0`, bare px/em, multi-value corner shorthand — is a hardcode.

SCOPE (gate only as wide as its glob — the standing scope rule):
  STRICT (blocking):  canon/canon.css · canon/type.css · MIGRATED snippets
  ADVISORY (census):  the other reference snippets + _proforma tranches — they
                      migrate per-component during Phase 1/2; workers move a file
                      into MIGRATED_SNIPPETS in the same change that rebinds it.

Writes knowledge/_RADIUS-GATE.md. Exits non-zero on any STRICT failure.
Selftest: python3 knowledge/_validate_radius.py --selftest (bite test, ADR-0005 §5).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "_RADIUS-GATE.md")

STRICT_FILES = [
    os.path.join(HERE, "canon", "canon.css"),
    os.path.join(HERE, "canon", "type.css"),
]

# Phase-1 migration ratchet: rebinding a snippet's radius onto the token
# (CSS + manifest + theme-block declarations) and adding it here is ONE change.
MIGRATED_SNIPPETS = {
    # #204 P2 wave (BUILD-PM-registered from lane M/N/P receipts). All six were measured
    # at ZERO advisory hardcodes BEFORE registration (`_validate_radius.py` rc=0,
    # "0 advisory file(s) pending migration"), so this is the completing half of the
    # one-change rule above, not a new exemption. ⚠ Registration here is a GATE ratchet
    # only — it is NOT promotion. All six ship PROPOSED and are unregistered in
    # `gen_showroom.CATEGORIES` (they fall to the "More" bucket) pending Dave's ruling.
    "Popconfirm.reference.html",
    "Footer.reference.html",
    "Layout-utilities.reference.html",
    "Document-row.reference.html",
    "Payment-card-visual.reference.html",
    "Runway-bar.reference.html",
    # Wave 3b, #203 (conductor-registered from lane I/J/K receipts):
    # Wave 3, #209 (conductor-registered from lane A/B/C receipts, measured 0 strict /
    # 0 advisory tree-wide BEFORE registration; Rating + Split-button rebound by the
    # conductor in the same change — the one-change rule). Gate ratchet only, NOT
    # promotion; all nine unregistered in gen_showroom.CATEGORIES pending Dave.
    "Transaction-row.reference.html",
    "Standing-order-mandate-row.reference.html",
    "Limits-meter.reference.html",
    "Range-slider.reference.html",
    "Rating.reference.html",
    "Transfer-list.reference.html",
    "Split-button.reference.html",
    "Fab.reference.html",
    "Back-to-top.reference.html",
    "Command-palette.reference.html",
    "Sidebar-nav.reference.html",
    "Anchor-nav.reference.html",
    "Combobox.reference.html",
    "Multi-select.reference.html",
    "Tags-input.reference.html",
    "Kpi-tile.reference.html",
    "Timeline.reference.html",
    "Avatar-group.reference.html",
    "Button.reference.html",
    "Cards.reference.html",
    "Tabs.reference.html",
    "Modals.reference.html",
    "Account-card.reference.html",
    "Table.reference.html",
    "List-items.reference.html",
    "Action-bar.reference.html",
    "Confirmation.reference.html",
    "Links.reference.html",
    "Video-player.reference.html",
    "Notifications.reference.html",
    "Input-fields.reference.html",
    "Selection-controls.reference.html",
    "Dropdown.reference.html",
    "Slider.reference.html",
    "Icon-button.reference.html",
    "Badge.reference.html",
    "Tags.reference.html",
    "Status-indicator.reference.html",
    "Progress-tracker.reference.html",
    # Phase-2 wave 1 (2026-07-22) — born on role tokens, strict from birth:
    "Form-layout.reference.html",
    "Amount-input.reference.html",
    "Textarea.reference.html",
    "Secure-entry.reference.html",
    "Alert.reference.html",
    "Toast.reference.html",
    "Banner.reference.html",
    "Skeleton-loader.reference.html",
    "Drawer.reference.html",
    "Popover.reference.html",
    "Modal-lightbox.reference.html",
    "Empty-state.reference.html",
    "Stat-card.reference.html",
    "Account-selector.reference.html",
    # Phase-2 wave 2:
    "Data-grid.reference.html",
    "Date-picker.reference.html",
    "Date-range-picker.reference.html",
    # Segmented control (2026-07-24) — atom promoted from View options; square radius, pill = 999 literal:
    "Segmented-control.reference.html",
    "Time-picker.reference.html",
    "File-upload.reference.html",
    "Stepper.reference.html",
    "Chart-bar.reference.html",
    "Chart-line.reference.html",
    "Chart-donut.reference.html",
    "Chart-sparkline.reference.html",
    "Chart-scatter.reference.html",
    "Chart-combo.reference.html",
    # Chart wave 2 (2026-08-05, #95) — born on role tokens, strict from birth:
    "Chart-butterfly-h.reference.html",
    "Chart-butterfly-v.reference.html",
    "Chart-histogram.reference.html",
    "Chart-boxplot.reference.html",
    "Chart-bullet.reference.html",
    "Chart-candlestick.reference.html",
    "Chart-pie.reference.html",
    "Chart-stacked-area.reference.html",
    # First component through the scaffold route (s173-D1, Dave, #174) — born on
    # border-radius/indicator, strict from birth:
    "Progress-bar.reference.html",
}

ADVISORY_GLOBS = [
    os.path.join(HERE, "snippets", "*.reference.html"),
    os.path.join(HERE, "_proforma", "*.html"),
]

# ⛔ #221 — THE CAUSE OF #220-L1 FINDING 11, AND IT WAS WIDER THAN THE FINDING.
# `DECL_RE` was the literal string `border-radius` and nothing else, so EVERY longhand spelling
# of the same declaration walked through a BLOCKING gate. Mutation-driven at HEAD before this
# change, all BLIND: `border-start-start-radius` · `border-end-end-radius` ·
# `border-start-end-radius` · `border-end-start-radius` (L1's four logical mutants) AND
# `border-top-left-radius` · `border-top-right-radius` · `border-bottom-left-radius` ·
# `border-bottom-right-radius` — the four PHYSICAL corner longhands, which L1 did not reach.
# ⛔ THE BLINDNESS WAS ALREADY BEING USED AS AN ESCAPE HATCH, IN WRITING. `canon/canon.css`
# and `snippets/Split-button.reference.html` each carry, on one line, a corner-split spelt as
# physical longhands with this comment beside it: *"the radius gate reads shorthand grammar
# only and a 0-first shorthand cannot satisfy it"*. A conductor at #209 read the gate's
# grammar, found the seam, and routed around it — honestly, in a comment, and nothing in the
# repo recorded it as a GATE defect. That comment is now false; the gate reads all of it.
RADIUS_PROP = (r'border-(?:(?:top|bottom)-(?:left|right)-|(?:start|end)-(?:start|end)-)?radius')
DECL_RE  = re.compile(r'(?<![-\w])(' + RADIUS_PROP + r')\s*:\s*([^;}]+)')
OK_VALUE = re.compile(r'^(var\(.*\)|50%|999px|inherit)$')

# ⛔ THE TIER SPLIT, AND WHY IT IS NOT A WEAKENING — MEASURED BEFORE IT WAS WRITTEN.
# Widening the pattern makes the gate SEE two populations that behave differently on this tree:
#   * the SHORTHAND and the four LOGICAL longhands — **zero occurrences anywhere in the
#     corpus**, so taking them STRICT closes L1's mutation-proven hole at a cost of no reds.
#     They are blocking from this change onward.
#   * the four PHYSICAL corner longhands — **two occurrences, both the #209 corner-split, both
#     `0` beside token-valued siblings**. `0` is NOT in `OK_VALUE` (the selftest has an arm
#     insisting a bare `0` is a hardcode), so taking these strict would turn this BLOCKING gate
#     RED on committed canon at the moment of the repair.
# ⬛ WHETHER `border-top-left-radius:0` BESIDE A TOKENISED SIBLING IS A LEGAL CORNER-SQUARE OR A
# HARDCODE IS A RULING, NOT A REPAIR — it decides whether canon changes or the rule does, and
# both are Dave's. So this arm is BORN ADVISORY and says so on every run: the findings are
# COUNTED, NAMED AND PRINTED IN FULL, never silently dropped, and they do not move the exit
# code. ⚠ A SILENT EXEMPTION WOULD BE THE DEFECT, NOT THE FIX — this is the same posture
# `_build_survey.py` takes with COULD-NOT-ASK, for the same reason.
# ⇒ Promotion to strict is one line (`STRICT_GRAMMAR |= PHYSICAL_CORNER`) plus Dave's word.
# See `notes/_subreports/2026-08-27-221-laneA.md` § RULING-SHAPED QUESTIONS.
PHYSICAL_CORNER = re.compile(r'^border-(?:top|bottom)-(?:left|right)-radius$')

def strip_comments(text):
    # ds-008 (fixed 2026-07-22, ADR-0013 session): HTML comments stripped TOO — snippet
    # header prose like "border-radius:0" tripped the census (Badge + Tags each carried
    # one; ~50 Phase-2 files will carry header prose). CSS comments were always stripped.
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    return re.sub(r'/\*.*?\*/', '', text, flags=re.S)

def check_text(text):
    """-> list of offending `(property, value)` pairs (comments already stripped).

    ⚠ #221 CHANGED THIS RETURN SHAPE from bare values to pairs, deliberately: with eight legal
    spellings in the population, a finding that does not name its PROPERTY cannot be acted on,
    and the report line `border-radius:0` would have been a lie about four of them.
    """
    return [(p, v.strip()) for p, v in DECL_RE.findall(strip_comments(text))
            if not OK_VALUE.match(v.strip())]

def split_tiers(found):
    """-> (strict_eligible, physical_corner_advisory) for a `check_text` result."""
    strict = [(p, v) for p, v in found if not PHYSICAL_CORNER.match(p)]
    corner = [(p, v) for p, v in found if PHYSICAL_CORNER.match(p)]
    return strict, corner

def selftest():
    fails = []
    if check_text(".x{border-radius:var(--border-radius-default);}"):
        fails.append("token route flagged (must pass)")
    if check_text(".x{border-radius:50%;} .y{border-radius:999px;}"):
        fails.append("circle/pill idiom flagged (must pass)")
    if not check_text(".x{border-radius:0;}"):
        fails.append("hardcoded 0 NOT flagged (gate has no teeth)")
    if not check_text(".x{border-radius:4px;}"):
        fails.append("hardcoded px NOT flagged")
    if not check_text(".x{border-radius:0 0 4px 4px;}"):
        fails.append("corner shorthand NOT flagged")
    if check_text("/* border-radius:0 in prose */ .x{border-radius:inherit;}"):
        fails.append("comment mention flagged (comments must be stripped)")
    if check_text("<!-- header prose: SQUARE corners, border-radius:0 by brand -->\n.x{border-radius:var(--border-radius-control);}"):
        fails.append("HTML-comment prose flagged (ds-008 — HTML comments must be stripped)")

    # ── #221 BITE PAIRS for #220-L1 finding 11, both directions, one per proved blindness ──
    # A1 was the firing CONTROL in L1's probe table and is the first arm above; A2/A3 were the
    # mutants that walked through. All eight longhands are driven here, plus the token route
    # through each grammar (the discrimination control — a gate that fires on every longhand
    # would pass the FIRES list and be useless).
    LOGICAL = ["border-start-start-radius", "border-start-end-radius",
               "border-end-start-radius", "border-end-end-radius"]
    PHYSICAL = ["border-top-left-radius", "border-top-right-radius",
                "border-bottom-left-radius", "border-bottom-right-radius"]
    for prop in LOGICAL + PHYSICAL:
        if not check_text(".l1probe{%s:8px;}" % prop):
            fails.append("MUTANT NOT CAUGHT — `%s:8px` is as un-themeable as the shorthand "
                         "and walked through (#220-L1 finding 11)" % prop)
        if not check_text(".l1probe{%s:0;}" % prop):
            fails.append("MUTANT NOT CAUGHT — `%s:0` freezes a corner square in every theme" % prop)
        if check_text(".l1probe{%s:var(--border-radius-control);}" % prop):
            fails.append("TOKEN ROUTE FLAGGED through `%s` — the gate must discriminate, "
                         "not fire on the grammar" % prop)
    # the tier split itself is bitten: a logical longhand is STRICT-eligible, a physical corner
    # longhand is the DECLARED-ADVISORY population, and neither may quietly become the other.
    s, c = split_tiers(check_text(".a{border-start-start-radius:8px} .b{border-top-left-radius:0}"
                                 " .c{border-radius:4px}"))
    if len(s) != 2 or len(c) != 1:
        fails.append("TIER SPLIT WRONG — wanted 2 strict-eligible + 1 physical-corner, got %d + %d"
                     % (len(s), len(c)))
    if any(p == "border-radius" for p, _ in c):
        fails.append("TIER SPLIT WRONG — the shorthand must never fall into the advisory tier")
    # ds-008 must still hold through the widened grammar
    if check_text("/* border-top-left-radius:0 in prose */ .x{border-radius:inherit;}"):
        fails.append("comment mention of a LONGHAND flagged (ds-008 must cover the new grammar)")
    # the lookbehind: a token DEFINITION named after a corner is a mint, not a declaration
    if check_text(":root{--my-border-top-left-radius:8px;}"):
        fails.append("a custom-property DEFINITION was flagged — `(?<![-\\w])` must hold")
    return fails

def main():
    if "--selftest" in sys.argv:
        f = selftest()
        if f:
            print("_validate_radius SELFTEST FAIL:"); [print("  X " + x) for x in f]
            sys.exit(1)
        print("_validate_radius selftest OK")
        return

    strict_fails, advisory, corner_advisory = [], [], []
    for p in STRICT_FILES:
        if not os.path.exists(p):
            continue
        s, c = split_tiers(check_text(open(p).read()))
        rel = os.path.relpath(p, HERE)
        strict_fails += [(rel, prop, v) for prop, v in s]
        corner_advisory += [(rel, prop, v) for prop, v in c]
    snip_dir = os.path.join(HERE, "snippets")
    for pattern in ADVISORY_GLOBS:
        for p in sorted(glob.glob(pattern)):
            name = os.path.basename(p)
            s, c = split_tiers(check_text(open(p).read()))
            rel = os.path.relpath(p, HERE)
            migrated = os.path.dirname(p) == snip_dir and name in MIGRATED_SNIPPETS
            if migrated:
                strict_fails += [(f"snippets/{name}", prop, v) for prop, v in s]
                corner_advisory += [(f"snippets/{name}", prop, v) for prop, v in c]
            elif s or c:
                advisory.append((rel, len(s) + len(c)))

    lines = ["# _RADIUS-GATE — border-radius is token-bound (theme flex slot, ADR-0010)",
             "",
             "*Generated by `_validate_radius.py`. Allowed values: `var(...)`, `50%` (circle),",
             "`999px` (pill idiom), `inherit`. STRICT = canon + migrated snippets (blocking).*",
             ""]
    if strict_fails:
        lines.append(f"## ❌ STRICT failures ({len(strict_fails)})\n")
        lines += [f"- `{f}` → `{prop}:{v}`" for f, prop, v in strict_fails]
    else:
        lines.append("## ✅ STRICT surfaces clean (canon + " +
                     f"{len(MIGRATED_SNIPPETS)} migrated snippet(s))")
    lines.append("")
    # #221 — the newly-VISIBLE population, printed in full and counted, never dropped.
    if corner_advisory:
        lines.append(f"## ⬛ DECLARED ADVISORY — physical corner longhands ({len(corner_advisory)})\n")
        lines.append("*#221 widened this gate's grammar; these declarations were invisible to it "
                     "until now and are reported, not enforced. Whether a corner-square spelt as "
                     "`border-top-left-radius:0` beside token-valued siblings is legal is a "
                     "**RULING** (it decides whether canon changes or the rule does) and is "
                     "⬛ DAVE'S. They do NOT move this gate's exit code.*\n")
        lines += [f"- `{f}` → `{prop}:{v}`" for f, prop, v in corner_advisory]
        lines.append("")
    else:
        lines.append("## ✅ no physical corner longhands in the strict population")
        lines.append("")
    if advisory:
        lines.append(f"## ⚠ ADVISORY — awaiting Phase-1/2 migration ({len(advisory)} file(s))\n")
        lines += [f"- `{f}` — {n} hardcoded declaration(s)" for f, n in advisory]
        lines.append("\n*Migrating a file = rebind its radius onto the token (CSS + manifest + "
                     "theme blocks) AND add it to `MIGRATED_SNIPPETS` in `_validate_radius.py` "
                     "in the same change.*")
    else:
        lines.append("## ✅ no advisory hardcodes remain")
    open(OUT, "w").write("\n".join(lines) + "\n")

    print(f"_validate_radius: {len(strict_fails)} strict fail(s), "
          f"{len(advisory)} advisory file(s) pending migration, "
          f"{len(corner_advisory)} physical corner longhand(s) DECLARED ADVISORY (#221) "
          f"-> _RADIUS-GATE.md")
    for f, prop, v in corner_advisory:
        print(f"  ⬛ DECLARED (not counted, not a verdict): {f}: {prop}:{v}")
    if corner_advisory:
        print("     ⬛ promoting this arm to STRICT is DAVE'S — see "
              "notes/_subreports/2026-08-27-221-laneA.md")
    if strict_fails:
        [print(f"  X {f}: {prop}:{v}") for f, prop, v in strict_fails]
        sys.exit(1)

if __name__ == "__main__":
    main()
