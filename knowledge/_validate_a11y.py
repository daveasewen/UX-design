#!/usr/bin/env python3
"""
_validate_a11y.py — accessibility enforcement gate for gated reference snippets.

Verification = enforcement (not a nudge). This gate fails the build when a snippet
regresses on a deterministic, statically-checkable WCAG criterion:

  FAIL (gating):
    * 2.3.3 / motion sensitivity — any snippet that animates (transition/animation/
      @keyframes) MUST carry a `prefers-reduced-motion: reduce` block. A canonical
      reference that animates with no reduced-motion escape hatch is a defect.

    * 2.5.8 Target Size (Minimum, AA) — interactive controls (button / a[href] /
      [role=button|switch|tab|option]) with a declared CSS box under 24px in EITHER
      dimension and no ::before/::after hit-area expander for that selector.
      PROMOTED from warn tier by the aid-009 ruling (Dave, 2026-07-03): 24 is the
      hard floor. (Was AND-semantics <24×24; EITHER-dimension is the SC's reading.)

  WARN (reported, non-gating — needs a human/visual call):
    * target size < 44 — the HSBC DEFAULT is 44×44 (ID-26 + axs-003 "existing 44×44
      guidance takes priority"; 24 is the exception tier, not the goal). Advisory
      per the same aid-009 ruling: signal 24–43, promotion only with the exception
      outs (spacing/equivalent/inline/UA/essential) modelled. Decorative inner
      glyphs (.dot/.thumb/svg) are excluded; only the focusable element flags.

Writes _A11Y-GATE.md and exits non-zero iff there is >=1 FAIL.
"""
import re, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")

MOTION = re.compile(r'transition\s*:|animation\s*:|@keyframes', re.I)
# selectors that denote the focusable control itself (not a decorative child).
# This regex is a LITERAL, hand-maintained name list — kept for the selector shapes it already
# recognises (button, a.foo, .close, ...). It is NOT the whole vocabulary any more; see the
# CTRL-vocabulary sweep below, which is the ds-015/`dv-vocab`-shaped fix for what this regex
# structurally cannot see (ds-016 §5, `_DS-IMPROVEMENTS.md` ds-015: "Same hand-maintained-vocabulary
# class as the dtype fork that produced ds-014 ... CTRL is UNSWEPT").
CTRL = re.compile(r'(^|[\s,>])(button|a\.[\w-]+|\.x|\.close|\.clear|\.trigger|\.moves\s+button|\.handle|\.page|\.step)\b', re.I)
DECOR = re.compile(r'(svg|\.dot|\.thumb|\.bar\b|::before|::after)', re.I)

# ---- CTRL vocabulary sweep (ds-015 §5 / `_FUTURE-STATE.md` call (5), RULED GO 2026-07-27) --------
# The literal CTRL regex above is a closed, hand-maintained list of selector SHAPES. It structurally
# cannot recognise a real interactive control that doesn't happen to match one of those shapes —
# e.g. `.dv-leg-sw` in Chart-line.reference.html, which markup declares `role="checkbox"
# tabindex="0"` (a genuine operable ARIA widget) but which no literal-name pattern will ever match.
# That is the SAME defect class as `dv-vocab` (ds-014): a hand-enumerated vocabulary silently drops
# anything it wasn't told about, and the drop reads as "not a control" rather than "unrecognised".
#
# Fixed the `dv-vocab` way: normalise ONCE, off the markup's own ARIA role vocabulary (not off
# selector text), and FAIL LOUD on any role value this gate has never classified — never enumerate
# selector exceptions inline, never let an unknown default to skip/pass.
#
# The two sets below are a TOTAL partition, closed over the roles the corpus actually uses today
# (scanned 2026-08-01: `grep -ohE 'role="[a-zA-Z]+"' knowledge/snippets/*.reference.html | sort -u`
# returned exactly these 27). A role outside both sets is not silently ignored — see
# `_unknown_role_check` below, which FAILS the build rather than treating the unknown as either
# interactive or decorative.
INTERACTIVE_ROLES = {
    "checkbox", "combobox", "menuitem", "option", "radio", "slider", "switch", "tab",
}
NON_INTERACTIVE_ROLES = {
    "alert", "dialog", "grid", "group", "img", "list", "listbox", "listitem", "menu",
    "presentation", "progressbar", "radiogroup", "region", "separator", "status",
    "tablist", "tabpanel", "timer", "tooltip",
}

_TAG_RE = re.compile(r'<([a-zA-Z][\w-]*)((?:\s+[a-zA-Z_:][\w:.-]*(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'))?)*)\s*/?>')
_ATTR_RE = re.compile(r'([a-zA-Z_:][\w:.-]*)\s*=\s*"([^"]*)"')
_ROLE_RE = re.compile(r'\brole\s*=\s*"([a-zA-Z]+)"')

def unknown_roles(s):
    """Any role="..." value in the markup not classified into either partition above."""
    return sorted({r for r in _ROLE_RE.findall(s)
                   if r not in INTERACTIVE_ROLES and r not in NON_INTERACTIVE_ROLES})

def interactive_classes(s):
    """Class tokens carried by any element the markup itself declares operable: a native
    <button>, an <a href>, anything with a tabindex attribute, or an explicit interactive
    ARIA role. This is how `.dv-leg-sw` (role="checkbox" tabindex="0") enters CTRL scope
    without a literal selector-name being hand-added for it."""
    out = set()
    for m in _TAG_RE.finditer(s):
        tag, attr_str = m.group(1).lower(), m.group(2)
        attrs = dict(_ATTR_RE.findall(attr_str))
        is_interactive = (
            tag == "button"
            or (tag == "a" and "href" in attrs)
            or "tabindex" in attrs
            or attrs.get("role") in INTERACTIVE_ROLES
        )
        if is_interactive and "class" in attrs:
            out.update(attrs["class"].split())
    return out

def is_ctrl(sel, interactive_cls):
    """CTRL membership: the legacy literal-name regex, OR a class token this selector carries
    that markup elsewhere declared operable (the sweep's contribution)."""
    if CTRL.search(sel):
        return True
    sel_classes = re.findall(r'\.([\w-]+)', sel)
    return any(c in interactive_cls for c in sel_classes)

def css_blocks(s):
    for m in re.finditer(r'([.#][\w.\-:\s>+]+)\{([^}]*)\}', s):
        yield m.group(1).strip(), m.group(2)

def check(fp):
    s = open(fp).read()
    name = os.path.basename(fp).replace('.reference.html', '')
    fails, warns = [], []

    if MOTION.search(s) and 'prefers-reduced-motion' not in s:
        fails.append("animates but has no `prefers-reduced-motion: reduce` block (2.3.3)")

    bad_roles = unknown_roles(s)
    if bad_roles:
        fails.append("CTRL vocabulary: unknown ARIA role(s) %s — this gate cannot classify "
                     "them as interactive or structural, so it cannot tell whether the elements "
                     "carrying them are in scope for 2.5.8. Add each to INTERACTIVE_ROLES or "
                     "NON_INTERACTIVE_ROLES in _validate_a11y.py before shipping (dv-vocab shape: "
                     "fail loud, never let an unknown default to skip)." % bad_roles)

    interactive_cls = interactive_classes(s)
    for sel, body in css_blocks(s):
        if not is_ctrl(sel, interactive_cls) or DECOR.search(sel):
            continue
        w = re.search(r'(?<![\w-])width\s*:\s*(\d+)px', body)
        h = re.search(r'(?<![\w-])height\s*:\s*(\d+)px', body)
        if not (w and h):
            continue
        wv, hv = int(w.group(1)), int(h.group(1))
        # An explicit hit-area expander for THIS selector exempts both tiers, because static CSS
        # cannot size the expander — the render axis owns that check.
        #
        # ds-015 (2026-07-27, Dave: "maybe we are checking the wrong thing"): the exemption is
        # CORRECT but it was SILENT, and silence is what made it dangerous. Adopting the expander —
        # i.e. doing the right thing — removed a component from aid-009's sample, and the render
        # axis it defers to DOES NOT EXIST YET (the hit-area gate is still PENDING DAVE SIGN-OFF,
        # notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md). Measured at the time:
        # 7 of 14 eligible control selectors exempted, 7 actually measured, across 67 snippets —
        # and the gate reported "0 failures".
        #
        # ⚠ ANTI-FALSE-FIX: do NOT "fix" this by deleting the exemption and failing these
        # selectors. They are not known to be non-compliant; they are known to be UNMEASURED, and
        # a static parse cannot tell the difference (it cannot read `min-width:var(--hit,44px)`,
        # and it cannot see a `transform` standing the target on its corner — the Chart-line
        # diamond, caught by elementFromPoint at render, never by this gate). Failing them would
        # trade a blind pass for a blind fail. The exemption stands until the render axis lands;
        # what changed here is only that it now DECLARES ITSELF and can be counted.
        if re.search(re.escape(sel) + r'\s*::(before|after)', s):
            warns.append(f"`{sel}` is {wv}×{hv}px — EXEMPT via a ::before hit-area expander, "
                         f"NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; "
                         f"the render-axis hit-area gate owes this one.")
            continue
        if min(wv, hv) < 24:
            fails.append(f"`{sel}` is {wv}×{hv}px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)")
        elif min(wv, hv) < 44:
            warns.append(f"`{sel}` is {wv}×{hv}px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out")
    return name, fails, warns

def main():
    rows = [check(fp) for fp in sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))]
    nfail = sum(len(f) for _, f, _ in rows)
    nwarn = sum(len(w) for _, _, w in rows)

    lines = ["# A11y gate — _validate_a11y.py", "",
             f"**{len(rows)} snippet(s)** · **{nfail} failure(s)** · **{nwarn} warning(s)**",
             "", "Gating: reduced-motion (2.3.3) · target size <24 floor (2.5.8, aid-009 ruling 2026-07-03). "
             "Reported: target size 24–43 vs the 44×44 HSBC default (aid-009).", "",
             "Library bar (aqa-003, ruled 2026-07-03): the canon is LIBRARY-GRADE — guideline "
             "and recommendation tiers bind it, not just standards.", ""]
    for name, fails, warns in rows:
        if not fails and not warns:
            continue
        lines.append(f"## {name}")
        for f in fails:
            lines.append(f"- 🔴 FAIL — {f}")
        for w in warns:
            lines.append(f"- 🟡 warn — {w}")
        lines.append("")
    if nfail == 0 and nwarn == 0:
        lines.append("_No issues._")
    open(os.path.join(HERE, "_A11Y-GATE.md"), "w").write("\n".join(lines) + "\n")

    print(f"a11y gate: {len(rows)} snippet(s), {nfail} failure(s), {nwarn} warning(s)")
    if nfail:
        for name, fails, _ in rows:
            for f in fails:
                print(f"  FAIL {name}: {f}")
    sys.exit(1 if nfail else 0)

if __name__ == "__main__":
    main()
