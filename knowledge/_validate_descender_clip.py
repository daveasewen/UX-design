#!/usr/bin/env python3
"""_validate_descender_clip.py — the descender-clip gate (ds-005).

WHY THIS EXISTS
---------------
The canon leading-trim strategy applies `text-box-trim:trim-both; text-box-edge:cap alphabetic`
to label elements. `cap alphabetic` trims the box to the cap-height…baseline span — which is
exactly what optically centres a label against an adjacent icon/dot. BUT when that same label
ALSO truncates (`overflow:hidden` + `text-overflow:ellipsis`), the descender (g/y/p/q) sits
*below* the alphabetic baseline — outside the trimmed box — and is CLIPPED. Render-confirmed
2026-07-19: "Savings" renders "Savin*q*s" on the Masthead dropdown title.

THE RULE (universal, so nobody has to remember the decision tree):
  Every rule that TRUNCATES a text label (`text-overflow:ellipsis`) must ALSO carry the
  descender-safe override on the same selector — `text-box-edge:text text` (full glyph box,
  keeps the ellipsis, descenders survive) OR `overflow:visible` (short atoms; no ellipsis).
  Applying `text-box-edge:text text` to a label that isn't trimmed is a harmless no-op
  (text-box-edge does nothing without text-box-trim), so the rule is safe everywhere.

`text-overflow:ellipsis` is the high-precision signal for "visible truncating text label":
sr-only patterns use `clip:rect(...)` not ellipsis; layout containers (.note/.track/.player/
.panel/avatar) use `overflow:hidden` WITHOUT ellipsis. So this gate has no known false positives.

Ruling: ds-005 decision-tree extension (knowledge/_DS-IMPROVEMENTS.md), Dave 2026-07-19
("do it right — gate it, keep cap alphabetic as the default").

⚠️ TO A FUTURE SESSION — the scattered `text-box-edge:text text` overrides on truncating
labels are NOT a bug and NOT a stray inconsistency to "clean up". They ARE the ds-005 fix; each
one prevents a real, render-confirmed descender clip. Removing one is the exact regression this
gate exists to catch — the build will go red and point you straight back here. Do not design a
"fix". CONSULT first (`python3 knowledge/_consult.py "descender clip"`).

Usage:  python3 knowledge/_validate_descender_clip.py <file.css|file.html> [more ...]
        python3 knowledge/_validate_descender_clip.py --selftest
        python3 knowledge/_validate_descender_clip.py         # build mode: gate DEFAULT_TARGETS
Exit non-zero on any un-overridden truncating label (blocking). Wired into _build_all.py.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, sys, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
ELLIPSIS = re.compile(r"text-overflow\s*:\s*ellipsis", re.I)
OVR_TEXTBOX = re.compile(r"text-box-edge\s*:\s*text\s+text", re.I)
OVR_VISIBLE = re.compile(r"overflow\s*:\s*visible", re.I)


def _norm(sel: str) -> str:
    """Normalise one selector for comparison: collapse whitespace, strip."""
    return re.sub(r"\s+", " ", sel).strip()


def _selectors(sel_group: str):
    """Split a comma selector list into normalised parts."""
    return [_norm(s) for s in sel_group.split(",") if _norm(s)]


def read_css(path: str) -> str:
    """CSS from a .css file, or the concatenated <style> blocks of an .html file.
    Inline style="" attributes are intentionally NOT scanned — the override is a
    companion class rule, which an inline style cannot carry."""
    with open(path, encoding="utf-8") as f:
        t = f.read()
    if not path.endswith((".css",)):
        t = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", t, flags=re.S | re.I))
    # Strip CSS comments so they can't glue onto the following selector.
    return re.sub(r"/\*.*?\*/", "", t, flags=re.S)


def check(css: str, where: str):
    """Return a list of (selector, where) for truncating labels lacking the override."""
    # Pass 1 — collect every selector that HAS a descender-safe override anywhere in the file.
    covered = set()
    for m in RULE.finditer(css):
        body = m.group(2)
        if OVR_TEXTBOX.search(body) or OVR_VISIBLE.search(body):
            for s in _selectors(m.group(1)):
                covered.add(s)
    # Pass 2 — every truncating rule must have all its selectors covered.
    viol = []
    for m in RULE.finditer(css):
        sel_group, body = m.group(1), m.group(2)
        if not ELLIPSIS.search(body):
            continue
        # a rule that truncates AND carries its own override is fine
        if OVR_TEXTBOX.search(body) or OVR_VISIBLE.search(body):
            continue
        for s in _selectors(sel_group):
            if s not in covered:
                viol.append((s, where))
    return viol


# =================================================================================================
# LEG 2 — THE SPECIFICITY LEG (#214, G1).  "Written" is not "wins."
# -------------------------------------------------------------------------------------------------
# Leg 1 above compares authored selector STRINGS: it asks only whether SOME rule bearing this exact
# selector declares the override. It has no model of the cascade. Measured #214: every reference
# snippet carries its own private copy of the global leading-trim rule
#     :is(button,a,label,span,…,input[type=text],…):not(:has(svg)){text-box-edge:cap alphabetic;}
# whose specificity is (0,1,2) — `:is()` takes its MOST SPECIFIC argument (`input[type=text]`,
# (0,1,1)), plus `:not(:has(svg))` which takes `:has(svg)` → (0,0,1). A bare single-class override
# `.sn-label{text-box-edge:text text;}` is (0,1,0). It LOSES. The label keeps `cap alphabetic` and
# every descender below the baseline is clipped by the label's own overflow:hidden — while leg 1
# reports the file green, because the string is present. Render-measured in canon.css:4714-4723:
# computed text-box-edge came back `cap alphabetic`, clipBelow 4.00px; after promotion to the
# two-class descendant form, clipBelow 0.00.
#
# THE RULE THIS LEG ENFORCES: every `text-box-edge:text text` override must OUT-SPECIFY (or tie and
# follow) every `text-box-edge:cap alphabetic` trim rule that could match the same subject element.
# An override that cannot win is cascade-dead and is reported by selector pair, loudly and by name.
#
# Deliberately scoped to `text-box-edge:text text` overrides. `overflow:visible` (leg 1's other
# accepted override) works by a different mechanism — it removes the clipping box, not the trimmed
# edge — so it is not subject to this comparison.
# =================================================================================================

TRIM_EDGE = re.compile(r"text-box-edge\s*:\s*cap\s+alphabetic", re.I)
_IDENT = re.compile(r"[-\w]")
# Functional pseudos that take the specificity of their most specific argument.
_MOST_SPECIFIC_ARG = {"is", "not", "has", "matches", "-webkit-any", "-moz-any"}
_PSEUDO_ELEMENTS_1COLON = {"before", "after", "first-line", "first-letter"}


def _split_top(s: str, sep: str = ","):
    """Split on `sep` at nesting depth 0 (parens and brackets are nesting)."""
    out, depth, buf = [], 0, []
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(buf)); buf = []
        else:
            buf.append(ch)
    out.append("".join(buf))
    return [p.strip() for p in out if p.strip()]


def specificity(sel: str):
    """CSS specificity (a, b, c) for one complex selector, `:is()`-aware.

    Implements the Selectors-4 rules that actually bite here:
      · `:is()` / `:not()` / `:has()` take the specificity of their MOST SPECIFIC argument
      · `:where()` contributes ZERO
      · `:nth-child(… of S)` is one pseudo-class plus the most specific S
    """
    a = b = c = 0
    i, n = 0, len(sel)
    while i < n:
        ch = sel[i]
        if ch == "#":
            j = i + 1
            while j < n and _IDENT.match(sel[j]): j += 1
            a += 1; i = j
        elif ch == ".":
            j = i + 1
            while j < n and _IDENT.match(sel[j]): j += 1
            b += 1; i = j
        elif ch == "[":
            depth, j = 1, i + 1
            while j < n and depth:
                if sel[j] == "[": depth += 1
                elif sel[j] == "]": depth -= 1
                j += 1
            b += 1; i = j
        elif ch == ":":
            if i + 1 < n and sel[i + 1] == ":":          # ::pseudo-element
                j = i + 2
                while j < n and _IDENT.match(sel[j]): j += 1
                c += 1; i = j
                continue
            j = i + 1
            while j < n and _IDENT.match(sel[j]): j += 1
            name = sel[i + 1:j].lower()
            if j < n and sel[j] == "(":                  # functional pseudo-class
                depth, k = 1, j + 1
                while k < n and depth:
                    if sel[k] == "(": depth += 1
                    elif sel[k] == ")": depth -= 1
                    k += 1
                args = sel[j + 1:k - 1]
                if name in _MOST_SPECIFIC_ARG:
                    best = (0, 0, 0)
                    for arg in _split_top(args):
                        best = max(best, specificity(arg))
                    a += best[0]; b += best[1]; c += best[2]
                elif name == "where":
                    pass                                  # contributes nothing
                elif name in ("nth-child", "nth-last-child"):
                    b += 1
                    m = re.search(r"\bof\b(.*)$", args, re.I | re.S)
                    if m:
                        best = (0, 0, 0)
                        for arg in _split_top(m.group(1)):
                            best = max(best, specificity(arg))
                        a += best[0]; b += best[1]; c += best[2]
                else:
                    b += 1
                i = k
            else:
                c += 1 if name in _PSEUDO_ELEMENTS_1COLON else 0
                b += 0 if name in _PSEUDO_ELEMENTS_1COLON else 1
                i = j
        elif ch.isalpha() or ch in "*-_":
            j = i
            while j < n and _IDENT.match(sel[j]): j += 1
            if j == i: j = i + 1                          # bare `*`
            if sel[i:j] != "*": c += 1
            i = j
        else:
            i += 1                                        # combinator / whitespace
    return (a, b, c)


def _subject(sel: str) -> str:
    """The SUBJECT compound of a complex selector — the rightmost compound, which is the element
    the rule actually styles. Splits on top-level combinators only."""
    depth, buf, last = 0, [], ""
    for ch in sel:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if depth == 0 and ch in " >+~\t\n":
            if buf: last = "".join(buf); buf = []
        else:
            buf.append(ch)
    return ("".join(buf) if buf else last).strip()


def _top_classes(compound: str):
    """Class names at the TOP level of a compound (not inside :is()/:not()/…)."""
    stripped, depth, out = [], 0, []
    for ch in compound:
        if ch in "([": depth += 1
        if depth == 0: stripped.append(ch)
        if ch in ")]": depth -= 1
    return set(re.findall(r"\.([-\w]+)", "".join(stripped)))


def _tags(compound: str):
    """Element names this compound can match, or None for 'any element'."""
    stripped, depth = [], 0
    for ch in compound:
        if ch in "([": depth += 1
        if depth == 0: stripped.append(ch)
        if ch in ")]": depth -= 1
    bare = re.match(r"^([-\w]+)", "".join(stripped).strip())
    if bare:
        return {bare.group(1).lower()}
    m = re.search(r":is\(", compound)
    if m:
        depth, k = 1, m.end()
        while k < len(compound) and depth:
            if compound[k] == "(": depth += 1
            elif compound[k] == ")": depth -= 1
            k += 1
        tags = set()
        for arg in _split_top(compound[m.end():k - 1]):
            t = _tags(_subject(arg))
            if t is None:
                return None
            tags |= t
        return tags or None
    return None


def _could_match_same(trim_sel: str, ovr_subject: str) -> bool:
    """Conservatively: could this trim rule apply to the element the override styles?
    Returns False only when we can PROVE they are disjoint — an unprovable case is reported,
    because a silent skip is exactly the hole leg 1 already has."""
    t_sub = _subject(trim_sel)
    t_tags, o_tags = _tags(t_sub), _tags(ovr_subject)
    if t_tags is not None and o_tags is not None and not (t_tags & o_tags):
        return False
    # the trim rule's own top-level classes must be satisfiable by the override's subject
    if not _top_classes(t_sub) <= _top_classes(ovr_subject):
        return False
    return True


def check_specificity(css: str, where: str):
    """Return (ovr_selector, trim_selector, ovr_spec, trim_spec, where) for cascade-DEAD overrides."""
    trims, ovrs = [], []
    for idx, m in enumerate(RULE.finditer(css)):
        sel_group, body = m.group(1), m.group(2)
        # NB: _selectors() splits on EVERY comma, which shreds a `:is(a,b,c)` list. Leg 2 must
        # split only at nesting depth 0 or it compares against selector fragments.
        if TRIM_EDGE.search(body):
            for s in _split_top(_norm(sel_group)):
                trims.append((idx, s, specificity(s)))
        if OVR_TEXTBOX.search(body):
            for s in _split_top(_norm(sel_group)):
                ovrs.append((idx, s, specificity(s)))
    dead = []
    for o_idx, o_sel, o_spec in ovrs:
        o_sub = _subject(o_sel)
        for t_idx, t_sel, t_spec in trims:
            if not _could_match_same(t_sel, o_sub):
                continue
            # the override loses if the trim is more specific, or ties and comes later
            if t_spec > o_spec or (t_spec == o_spec and t_idx > o_idx):
                dead.append((o_sel, t_sel, o_spec, t_spec, where))
                break
    return dead


def _fmt(sp):
    return f"({sp[0]},{sp[1]},{sp[2]})"


# -------------------------------------------------------------------------------------------------
# THE canon.css TRANCHE — REPORT-ONLY, AND IT IS A SHRINK-ONLY RATCHET, NOT A WAIVER.
#
# The specificity leg was born (#214) to catch the 18 cascade-dead overrides in the reference
# snippets, which Dave authorised repairing and which ARE repaired. Driving it surfaced a SECOND,
# larger tranche nobody had measured: 48 cascade-dead overrides in canon.css, including several the
# file's own comments record as REPAIRED and render-measured.
#
# THE CAUSE (arithmetic, from the file itself — NOT render-proven, see the residual):
#   The absorb step that copies a snippet into canon prefixes `.cn-<component>` onto BOTH the trim
#   rule and the override — but the trim rule's `:is()` ARGUMENTS get prefixed too. So:
#       snippet trim  :is(…,input[type=text],…):not(:has(svg))                       (0,1,2)
#       canon   trim  .cn-x :is(…,.cn-x input[type=text],…):not(:has(svg))           (0,3,2)   +2 classes
#       snippet ovr   .sn .sn-label                                                  (0,2,0)
#       canon   ovr   .cn-x .sn .sn-label                                            (0,3,0)   +1 class
#   The trim gains ONE MORE CLASS than the override does. A repair that wins in the snippet LOSES
#   in canon. The prefixer is not specificity-preserving, and it inverts exactly the fix ds-005
#   exists to protect.
#
# ⛔ NOT REPAIRED HERE ON PURPOSE. It is a 48-selector cross-file class remedy on a gated canon,
# it is Dave's call (canon.css:9316 says so in as many words — "the cross-file ds-005 class remedy
# is Dave's call, not a repair's"), and the render leg that would PROVE it (G2) is priced-not-built.
# Blocking it today would fail a build for a defect nobody has been authorised to fix.
#
# So the count below is a RATCHET: exceed it and the gate goes RED, come in under it and the gate
# tells you to lower the number. It can only ever shrink. It cannot rot into a silent pass.
# -------------------------------------------------------------------------------------------------
SPECIFICITY_RATCHET = {
    os.path.join("canon", "canon.css"): 48,   # measured #214, post-snippet-repair. SHRINK ONLY.
}


def _ratchet_key(where: str):
    for k in SPECIFICITY_RATCHET:
        if where.replace("\\", "/").endswith(k.replace("\\", "/")):
            return k
    return None


def run(paths):
    total, dead_total, ratchet = [], [], {}
    for p in paths:
        try:
            css = read_css(p)
        except OSError as e:
            print(f"  ! cannot read {p}: {e}"); total.append(("<unreadable>", p)); continue
        where = os.path.relpath(p)
        v = check(css, where)
        for sel, w in v:
            print(f"  ✗ truncating label without descender-safe override: "
                  f"`{sel}` ({w}) — add `{sel}{{text-box-edge:text text;}}` (ds-005)")
        total += v
        d = check_specificity(css, where)
        key = _ratchet_key(where)
        if key is not None:
            ratchet[key] = ratchet.get(key, 0) + len(d)
            for o_sel, t_sel, o_spec, t_spec, w in d:
                print(f"  ⚠ (report-only, ratcheted) cascade-dead override `{o_sel}` {_fmt(o_spec)} "
                      f"loses {_fmt(t_spec)} in {w}")
            continue
        for o_sel, t_sel, o_spec, t_spec, w in d:
            t_short = t_sel if len(t_sel) <= 72 else t_sel[:69] + "…"
            print(f"  ✗ CASCADE-DEAD descender override: `{o_sel}` {_fmt(o_spec)} in {w}\n"
                  f"      LOSES to the leading-trim rule `{t_short}` {_fmt(t_spec)} in the same file.\n"
                  f"      The declaration is present but never applies — the label still renders with\n"
                  f"      `cap alphabetic` and clips its descenders. Promote it to a descendant form\n"
                  f"      that out-specifies the trim (see knowledge/canon/canon.css:4714-4724).")
        dead_total += d

    # ---- the shrink-only ratchet on the report-only tranche -------------------------------------
    ratchet_fail = False
    for key, allowed in SPECIFICITY_RATCHET.items():
        seen = ratchet.get(key)
        if seen is None:
            continue                                    # that file was not in this run's targets
        if seen > allowed:
            print(f"\n✗ SPECIFICITY RATCHET BROKEN — {key}: {seen} cascade-dead override(s), "
                  f"allowance {allowed}. You have ADDED {seen - allowed}. This number may only "
                  f"shrink. Fix the new one(s) or explain to Dave why the class grew.")
            ratchet_fail = True
        elif seen < allowed:
            print(f"\n↓ SPECIFICITY RATCHET CAN TIGHTEN — {key}: {seen} cascade-dead override(s), "
                  f"allowance {allowed}. Lower SPECIFICITY_RATCHET to {seen} in "
                  f"knowledge/_validate_descender_clip.py so the ground you won cannot be given back.")
        else:
            print(f"\n⚠ REPORT-ONLY TRANCHE HOLDING — {key}: {seen} cascade-dead descender "
                  f"override(s), at the allowance. NOT a pass: these labels clip today. The absorb "
                  f"prefixer is the cause (see the block above SPECIFICITY_RATCHET). ⛔ The repair is "
                  f"a cross-file class remedy on gated canon — Dave's call, not a lane's.")
    if ratchet_fail:
        return 1
    if total or dead_total:
        if total:
            print(f"\nDESCENDER-CLIP GATE FAIL — {len(total)} truncating label(s) carry no "
                  f"descender-safe override at all. Add `text-box-edge:text text` to each.")
        if dead_total:
            print(f"\nDESCENDER-CLIP GATE FAIL (specificity leg) — {len(dead_total)} descender-safe "
                  f"override(s) are CASCADE-DEAD: written, but out-specified by the leading-trim rule "
                  f"in the same file, so the descenders clip anyway.")
        print("See knowledge/_DS-IMPROVEMENTS.md ds-005.")
        return 1
    print(f"DESCENDER-CLIP GATE PASS — every truncating label is descender-safe AND every "
          f"descender-safe override wins its cascade ({len(paths)} file(s)).")
    return 0


def selftest():
    clips = ".a{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}"
    fixed = clips + "\n.a{text-box-edge:text text;}"
    fixed_inline = ".b{overflow:hidden;text-overflow:ellipsis;text-box-edge:text text;}"
    fixed_group = (".c .x{overflow:hidden;text-overflow:ellipsis;}\n"
                   ".d .y{overflow:hidden;text-overflow:ellipsis;}\n"
                   ".c .x, .d .y{text-box-edge:text text;}")
    visible_ok = ".e{text-overflow:ellipsis;overflow:visible;}"
    container = ".note{overflow:hidden;padding:12px;}"        # no ellipsis -> not a label -> ignored
    sronly = ".sr{overflow:hidden;white-space:nowrap;clip:rect(0 0 0 0);}"  # no ellipsis -> ignored
    assert [s for s, _ in check(clips, "t")] == [".a"], check(clips, "t")
    assert check(fixed, "t") == [], "companion override should pass"
    assert check(fixed_inline, "t") == [], "same-rule override should pass"
    assert check(fixed_group, "t") == [], f"comma-group override should cover both, got {check(fixed_group,'t')}"
    assert check(visible_ok, "t") == [], "overflow:visible is a valid override"
    assert check(container, "t") == [], "non-ellipsis container must be ignored"
    assert check(sronly, "t") == [], "sr-only (clip:rect, no ellipsis) must be ignored"
    print("selftest OK — flags un-overridden ellipsis labels; accepts text-text / overflow-visible / "
          "same-rule / comma-group overrides; ignores containers + sr-only.")

    # ---- leg 2: specificity ----------------------------------------------------------------
    assert specificity(".a") == (0, 1, 0), specificity(".a")
    assert specificity("span") == (0, 0, 1)
    assert specificity(".a .b") == (0, 2, 0)
    assert specificity("input[type=text]") == (0, 1, 1)
    assert specificity(":is(span,input[type=text])") == (0, 1, 1), specificity(":is(span,input[type=text])")
    assert specificity(":not(:has(svg))") == (0, 0, 1)
    assert specificity(":where(.a,.b)") == (0, 0, 0)
    assert specificity("#x") == (1, 0, 0)
    TRIM = (":is(button,a,label,span,input[type=text]):not(:has(svg))"
            "{text-box-trim:trim-both;text-box-edge:cap alphabetic;}")
    assert specificity(":is(button,a,label,span,input[type=text]):not(:has(svg))") == (0, 1, 2)
    dead_case = TRIM + "\n.sn-label{overflow:hidden;text-overflow:ellipsis;text-box-edge:text text;}"
    d = check_specificity(dead_case, "t")
    assert len(d) == 1 and d[0][0] == ".sn-label", d
    assert check(dead_case, "t") == [], "leg 1 is blind to this — that is the whole point of leg 2"
    live_case = TRIM + "\n.sn .sn-label{overflow:hidden;text-overflow:ellipsis;text-box-edge:text text;}"
    assert check_specificity(live_case, "t") == [], check_specificity(live_case, "t")
    # a file with no trim rule at all cannot have a cascade-dead override
    assert check_specificity(".sn-label{text-box-edge:text text;}", "t") == []
    # a trim rule that provably cannot match the override's subject is not compared
    assert check_specificity("td:not(:has(svg)){text-box-edge:cap alphabetic;}\n"
                             "span.lbl{text-box-edge:text text;}", "t") == []
    # equal specificity, trim LATER in source order -> override still loses
    assert len(check_specificity(".lbl{text-box-edge:text text;}\n"
                                 ".any{text-box-edge:cap alphabetic;}", "t")) == 0  # .any != .lbl subject
    assert len(check_specificity(".lbl{text-box-edge:text text;}\n"
                                 "span{text-box-edge:cap alphabetic;}", "t")) == 0  # (0,0,1) < (0,1,0)
    print("selftest OK (specificity leg) — :is()/:not()/:has()/:where() resolved; cascade-dead "
          "single-class override caught where leg 1 is blind; two-class form accepted.")
    return 0


# Files whose truncating labels MUST be descender-safe today (build mode).
DEFAULT_TARGETS = (
    [os.path.join(HERE, "canon", "type.css"),
     os.path.join(HERE, "canon", "canon.css")]
    + sorted(glob.glob(os.path.join(HERE, "snippets", "*.html")))
    + sorted(glob.glob(os.path.join(HERE, "_proforma", "*.html")))
)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    if args:
        sys.exit(run(args))
    rc = selftest()
    rc = run([p for p in DEFAULT_TARGETS if os.path.exists(p)]) or rc
    sys.exit(rc)
