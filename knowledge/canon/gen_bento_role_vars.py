#!/usr/bin/env python3
"""
gen_bento_role_vars.py — THE s219-D3 GENERATION ARM: the dashboard role's per-theme
(outer, inner) spacing pair, delivered as theme-scoped custom properties.

WHAT WAS BROKEN (#287 lane X · #288 lane A). `Template-dashboard-bento.reference.html`
pinned MONO's dashboard pair as literals — `--bento-gutter:40px` on the outer wall and
`--bento-gutter:4px` on each tile-group — and `gen_canon_components.py` projected those
literals into `canon/canon.css` (:18119 / :18121 before this arm). A page in legacy,
console or supercharge therefore got mono's numbers. Dave, #287, verbatim:

  "The problem with the gutters it that they are deliberately different for the themes
   and the gutters are also different for the inner and outer bentos we essentially have
   a structural bento and embedded bentos or tile groupings."

⇒ OUTER and INNER are TWO QUANTITIES, each deliberately per-theme. The template must
deliver the SELECTED theme's pair, not one theme's pair regardless of theme.

WHY A GENERATOR AND NOT FOUR HAND-WRITTEN COPIES. s219-D3 (6): "THE LIBRARY SURFACES THE
FULL EDIT-MODE OPTION SPACE, GENERATED FROM THE RAILS MANIFEST — library, editor and
generator read one generated file so none can drift." Four typed copies of eight numbers
would be a second home for a ruled decision; this module is the third reader of the one
file.

THE SOURCE, ESTABLISHED FROM SOURCE AND NOT ASSUMED
  * `knowledge/_render/_bento_edit_rails.json` is the s219-D3 (6) ONE GENERATED FILE.
    Its `defaults` block carries `$owner: gen_foundations_217.py` and
    `$resolved_from: gen_foundations_217.ROLE_DEFAULTS`, which is
    `role_defaults_219.DEFAULTS` — itself PARSED from Dave's own receipt
    `notes/_receipts/2026-08-25-219-role-defaults-exports.md`, never typed.
  * So the AUTHORITATIVE values are `role_defaults_219.DEFAULTS["dashboard"][theme]`
    `mainSpacing` / `subSpacing`, and the rails file is their published surface.
  * This module READS THE RAILS FILE (s219-D3 (6)'s "one generated file") and REFUSES if
    it has drifted from `role_defaults_219.DEFAULTS`. Neither is allowed to be the quiet
    winner: a divergence is a NAMED refusal, not a silent pick.

⚠ A DISAGREEMENT THIS ARM DOES NOT RESOLVE, AND MUST NOT. For a dashboard whose tiles
are themselves bentos, canon's own role rule (`gen_canon_bento.role_css`) sets the OUTER
gutter to `var(--layout-bento-gutter)` — s217-D2's per-theme structural gutter, mono 0 /
supercharge 0 / legacy 24 / console 24, read from `tokens/layout.json` `layout/bento/gutter`
($value "0px", BASE tier) plus legacy's and console's override sets. s219-D1 (5)'s
`mainSpacing` says mono 40 / legacy 24 / console 40 / supercharge 24. The two ruled sources
DIFFER on mono, console and supercharge. ⛔ This arm delivers from the source s219-D3 NAMES
(the rails manifest / role defaults) and leaves the disagreement standing as a question for
Dave — see `notes/_subreports/2026-09-19-288-A-s219-d3-arm.md`. It does not touch
`--layout-bento-gutter`, whose mono 0 is DOUBTED, not overruled.

WHAT IT EMITS, between AUTO-BENTO-ROLE-VARS markers in `canon/canon.css` (placed after
AUTO-COMPONENTS so the projected template rules can read it, and before AUTO-THEMES so
`gen_theme_cascade.py`'s marker surgery never sees it):

    :root,
    [data-apollo-theme="mono"]{ --bento-dashboard-main:40px; --bento-dashboard-sub:4px; }
    [data-apollo-theme="legacy"]{ --bento-dashboard-main:24px; --bento-dashboard-sub:4px; }
    ...

`:root` carries MONO because mono is the base theme (ADR-0011: one baseline library, four
themes as override sets) — a page that names no theme gets the base, exactly as every other
token does. THE PROPERTIES INHERIT, so the consuming rules need no extra specificity.

WHO CONSUMES IT: `knowledge/snippets/Template-dashboard-bento.reference.html` declares
`--bento-gutter:var(--bento-dashboard-main,40px)` on the wall and
`var(--bento-dashboard-sub,4px)` on each group. THE FALLBACKS ARE MONO's PAIR AND ARE LOAD-
BEARING: no snippet links canon.css (the meta's second $awaitingDave records the probe,
0 of 137), so a standalone snippet document has no theme block to read and must still render
mono correctly. Snippets stay single-theme by convention; the DELIVERED CSS is theme-aware.

Usage:
  python3 knowledge/canon/gen_bento_role_vars.py             # write the canon.css block
  python3 knowledge/canon/gen_bento_role_vars.py --check     # verify in-sync (build gate)
  python3 knowledge/canon/gen_bento_role_vars.py --table     # print the delivered pairs
  python3 knowledge/canon/gen_bento_role_vars.py --selftest  # invariant bite-test
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
# s219-D5 (Q3): the canon generators SHIP with the designer pack, and a designer who
# reaches for one is warned first. NO-OP IN THIS REPO — the guard looks for the pack's
# own _MANIFEST.json marker, which only an unzipped pack has. Same bytes both sides.
from _helpgate import pack_gate as _pack_gate; _pack_gate(__file__, name=__name__, what='the bento role vars')
import json, os, sys

HERE  = os.path.dirname(os.path.abspath(__file__))
KNOW  = os.path.dirname(HERE)
CANON = os.path.join(HERE, "canon.css")
RAILS = os.path.join(KNOW, "_render", "_bento_edit_rails.json")
sys.path.insert(0, os.path.join(KNOW, "_render"))

START = "/* ===== AUTO-BENTO-ROLE-VARS START ===== */"
END   = "/* ===== AUTO-BENTO-ROLE-VARS END ===== */"
# The marker pair this block must sit BEFORE. gen_theme_cascade.py rebuilds everything from
# AUTO-THEMES START onwards; anything after it would be silently destroyed on the next run.
THEMES_ANCHOR = "/* ===== AUTO-THEMES START ===== */"

BASE_THEME = "mono"          # ADR-0011: mono is the baseline library; the others are overrides.
ROLE       = "dashboard"     # the only role whose grammar carries mainSpacing/subSpacing (s219-D1 (5))
DIALS      = (("mainSpacing", "--bento-dashboard-main", "OUTER — the structural bento's gutter"),
              ("subSpacing",  "--bento-dashboard-sub",  "INNER — the embedded bento / tile-group gutter"))


class RoleVarError(RuntimeError):
    """A NAMED refusal. Every path out of this module says which source failed and why."""


# ----------------------------------------------------------------- the one generated file
def rails():
    if not os.path.exists(RAILS):
        raise RoleVarError(
            "the s219-D3 (6) rails manifest is missing at %s — regenerate it with "
            "`python3 knowledge/_render/gen_bento_matrix_217.py --rails`. Refusing to "
            "fall back to a second source." % RAILS)
    return json.load(open(RAILS, encoding="utf-8"))


def themes(R=None):
    R = R or rails()
    t = R.get("themes")
    if not t:
        raise RoleVarError("the rails manifest carries no `themes` list — refusing to guess the four.")
    return list(t)


def pairs():
    """{theme: {"mainSpacing": "40px", "subSpacing": "4px"}} — from the rails manifest,
    CROSS-CHECKED against the owner the manifest itself names. A divergence REFUSES."""
    R = rails()
    try:
        vals = R["defaults"]["values"][ROLE]
    except KeyError as e:
        raise RoleVarError("the rails manifest has no defaults.values.%s — missing key %s" % (ROLE, e))

    import role_defaults_219 as owner          # the $resolved_from chain's far end
    out = {}
    for th in themes(R):
        if th not in vals:
            raise RoleVarError("the rails manifest carries no %s default for theme %r" % (ROLE, th))
        got, own = vals[th], owner.DEFAULTS[ROLE][th]
        one = {}
        for dial, _var, _what in DIALS:
            if str(got.get(dial)) != str(own.get(dial)):
                raise RoleVarError(
                    "DRIFT between the two homes s219-D3 (6) says cannot drift: "
                    "_bento_edit_rails.json says %s/%s %s=%r, role_defaults_219.DEFAULTS "
                    "(its own $resolved_from) says %r. Refusing to pick a winner — "
                    "re-run `gen_bento_matrix_217.py --rails`, and if they still differ "
                    "that is a ruling question, not a generator bug."
                    % (ROLE, th, dial, got.get(dial), own.get(dial)))
            one[dial] = owner.spacing_px(got[dial])   # refuses loudly on a non-stop value
        out[th] = one
    return out


# ------------------------------------------------------------------------------- the block
def block():
    P = pairs()
    order = [BASE_THEME] + [t for t in themes() if t != BASE_THEME]
    L = [START,
         "/* THE s219-D3 GENERATION ARM — the dashboard role's per-theme (OUTER, INNER) spacing",
         "   pair. GENERATED by canon/gen_bento_role_vars.py from the s219-D3 (6) rails manifest",
         "   knowledge/_render/_bento_edit_rails.json, whose own $resolved_from is",
         "   role_defaults_219.DEFAULTS — parsed from Dave's #219 tuner-export receipt, never typed.",
         "   ⛔ DO NOT HAND-EDIT: edit the receipt's ruling, regenerate the rails, re-run this.",
         "",
         "   s219-D1 (5) carries the dashboard grammar's two-dial split; Dave, #287: 'the gutters",
         "   are also different for the inner and outer bentos we essentially have a structural",
         "   bento and embedded bentos or tile groupings'. OUTER = mainSpacing, INNER = subSpacing.",
         "",
         "   ⚠ THIS IS NOT --layout-bento-gutter. That token (s217-D2, mono 0 / supercharge 0 /",
         "   legacy 24 / console 24) is the structural gutter of the display and gallery grammars,",
         "   and canon's own dashboard-of-bentos rule still reads it. The two ruled sources differ",
         "   per theme; s219-D3 names THIS one for the dashboard role, and the divergence is a",
         "   QUESTION PUT to Dave, not a value this generator resolves.",
         "",
         "   :root carries %s because %s is the BASE theme (ADR-0011) — a page that names no" % (BASE_THEME, BASE_THEME),
         "   theme gets the baseline library, exactly as every other token does. */"]
    for th in order:
        sel = (":root,\n[data-apollo-theme=\"%s\"]{" % th) if th == BASE_THEME \
              else ("[data-apollo-theme=\"%s\"]{" % th)
        L.append(sel)
        for dial, var, what in DIALS:
            L.append("  %s:%s;   /* %s (s219-D1 (5) %s) */" % (var, P[th][dial], what, dial))
        L.append("}")
    L.append(END)
    return "\n".join(L)


def render():
    existing = open(CANON, encoding="utf-8").read()
    b = block()
    if START in existing and END in existing:
        head = existing[:existing.index(START)]
        tail = existing[existing.index(END) + len(END):]
        return head + b + tail
    if THEMES_ANCHOR not in existing:
        raise RoleVarError(
            "canon.css has no AUTO-THEMES anchor — refusing to guess a home for the role vars. "
            "The block MUST sit before it: gen_theme_cascade.py rebuilds everything from that "
            "marker onward and would destroy anything placed after it.")
    i = existing.index(THEMES_ANCHOR)
    return existing[:i] + b + "\n\n" + existing[i:]


def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("gen_bento_role_vars SELFTEST FAIL:")
            [print("  X " + f) for f in fails]
            return 1
        print("gen_bento_role_vars selftest OK — 6 bites")
        return 0
    if "--table" in sys.argv:
        P = pairs()
        print("%-12s %-10s %-10s" % ("theme", "OUTER", "INNER"))
        for th in [BASE_THEME] + [t for t in themes() if t != BASE_THEME]:
            print("%-12s %-10s %-10s" % (th, P[th]["mainSpacing"], P[th]["subSpacing"]))
        print("\nsource: knowledge/_render/_bento_edit_rails.json defaults.values.%s "
              "(s219-D3 (6)), cross-checked against role_defaults_219.DEFAULTS." % ROLE)
        return 0
    cur = open(CANON, encoding="utf-8").read()
    new = render()
    if "--check" in sys.argv:
        if cur != new:
            print("gen_bento_role_vars --check: canon.css AUTO-BENTO-ROLE-VARS is OUT OF SYNC "
                  "with knowledge/_render/_bento_edit_rails.json. "
                  "Run: python3 knowledge/canon/gen_bento_role_vars.py", file=sys.stderr)
            return 1
        print("gen_bento_role_vars --check OK — %d themes x 2 dials in sync with the rails manifest."
              % len(themes()))
        return 0
    if new != cur:
        open(CANON, "w", encoding="utf-8").write(new)
        print("Wrote AUTO-BENTO-ROLE-VARS into %s" % CANON)
    else:
        print("AUTO-BENTO-ROLE-VARS already current in %s" % CANON)
    P = pairs()
    print("  " + " · ".join("%s %s/%s" % (t, P[t]["mainSpacing"], P[t]["subSpacing"])
                            for t in [BASE_THEME] + [x for x in themes() if x != BASE_THEME]))
    return 0


def selftest():
    """6 bites: the source chain · the four themes · the two dials · the stop rail ·
    the base-theme seat · the placement invariant."""
    fails = []
    try:
        P = pairs()
    except RoleVarError as e:
        return ["bite 1 FAIL: the source chain refused — %s" % e]

    T = themes()
    if sorted(T) != sorted(["mono", "legacy", "console", "supercharge"]):
        fails.append("bite 2 FAIL: the rails manifest does not carry the four themes — %r" % T)

    # bite 3: the two quantities are DISTINCT — a single number for both is the #287 defect.
    if not any(P[t]["mainSpacing"] != P[t]["subSpacing"] for t in T):
        fails.append("bite 3 FAIL: outer and inner never differ — the two-quantity split "
                     "Dave named at #287 has collapsed")

    # bite 4: every delivered value is on the s219-D1 (4) ruled stop set.
    import role_defaults_219 as owner
    stops = {owner.spacing_px(s) for s in owner.SPACING_STOPS}
    off = [(t, d, P[t][d]) for t in T for d, _v, _w in DIALS if P[t][d] not in stops]
    if off:
        fails.append("bite 4 FAIL: value(s) off the s219-D1 (4) rail {1,2,4,16,24,40}: %r" % off)

    # bite 5: at least two themes must differ from the base, or the arm delivers nothing.
    if not any(P[t] != P[BASE_THEME] for t in T if t != BASE_THEME):
        fails.append("bite 5 FAIL: every theme equals %s — this arm would be a no-op and the "
                     "#287 defect would survive it" % BASE_THEME)

    # bite 6: the block must land BEFORE AUTO-THEMES, or gen_theme_cascade destroys it.
    out = render()
    if START not in out or THEMES_ANCHOR not in out:
        fails.append("bite 6a FAIL: rendered canon.css is missing a required marker")
    elif out.index(START) > out.index(THEMES_ANCHOR):
        fails.append("bite 6b FAIL: the role-vars block sits AFTER AUTO-THEMES START — "
                     "gen_theme_cascade.py would silently destroy it on its next run")
    # and it must be idempotent
    if render() != out:
        fails.append("bite 6c FAIL: render() is not idempotent")
    return fails


if __name__ == "__main__":
    sys.exit(main())
