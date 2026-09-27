#!/usr/bin/env python3
"""
_validate_a11y.py — accessibility enforcement gate for gated reference snippets.

Verification = enforcement (not a nudge). This gate fails the build when a snippet
regresses on a deterministic, statically-checkable WCAG criterion:

  FAIL (gating):
    * 2.3.3 / motion sensitivity — any snippet that animates (transition/animation/
      @keyframes) MUST carry a `prefers-reduced-motion: reduce` block.
    * CTRL vocabulary — an ARIA role this gate has never classified fails loud
      rather than defaulting to "not a control" (dv-vocab shape, ds-014/ds-015).
    * 2.5.8 Target Size (Minimum, AA) — any CONTROL whose measured target is under
      the 24px floor in EITHER dimension, with no hit-expander that reaches the
      floor and no claimed exception. (aid-009, Dave 2026-07-03.)

  WARN (reported, non-gating):
    * CONTROL 24–43 vs the 44 HSBC default (axs-003 / ID-26 / aid-009).
      ⚠ `s114-D6` (Dave, #114) RULES this BLOCKING — and ORDERS it AFTER the
      measurement redesign (`s114-D5`, this rebuild) lands. Flip CONTROL_TIER_44
      to "fail" to enact it; the sequence is part of Dave's ruling, so do not
      flip it in the same pass that lands the redesign.
    * DATA MARK under 24 (`s116-D1`, Dave, #116: marks are exempt from the 44
      control target, NOT exempt from the check — 24 is their floor, justified by
      the table fallback every chart carries). Dave's ruling attaches an OWED
      MEASUREMENT *before* this goes blocking, so it reports and does not gate.
      Flip MARK_TIER to "fail" once he has ruled on the measured population.
    * UNMEASURED — a control whose box is layout-determined, or a mark whose
      geometry is not statically derivable. Reported, never guessed
      [[measuring-tool-must-not-guess]].

WHAT CHANGED AT #116 (s114-D5), and why it is one build and not two:
  The old target check asked "is this a control?" of CSS SELECTOR TEXT against a
  hand-maintained name list, and "how big is it?" of a `width:Npx` regex on the
  same rule body. That produced six PHANTOM failures (decorative children of
  >=44px controls, flagged because the matcher tested ancestor class tokens as
  well as the subject) AND the axs-003 detector quirk (real controls — `.dv-vt`,
  `.dv-tbl-toggle`, every `<summary>` — never checked at all). Same cause, two
  symptom sets. The measurement now runs off the MARKUP through `_a11y_target.py`:
  a real element tree, a real subject-aware cascade, resolved custom properties.
  Read that module's header before changing any of this.

Writes _A11Y-GATE.md and exits non-zero iff there is >=1 FAIL.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SNIP = os.path.join(HERE, "snippets")

from _a11y_target import (                                    # noqa: E402
    analyse, unknown_roles, TARGET_CONTROL, TARGET_MARK, FLOOR, EXCEPTION_ATTR,
)

MOTION = re.compile(r'transition\s*:|animation\s*:|@keyframes', re.I)

# ---- gate tiers. Each is a RULED sequence point, not a knob to turn to pass. --
CONTROL_TIER_44 = "warn"   # -> "fail" enacts s114-D6 (ordered AFTER s114-D5)
MARK_TIER = "warn"         # -> "fail" enacts s116-D1's blocking half, which Dave
                           #    ordered after the sub-24 population is measured
                           #    and put to him. The measurement is in this report.


def check(fp):
    s = open(fp).read()
    name = os.path.basename(fp).replace('.reference.html', '')
    fails, warns, notes = [], [], []

    if MOTION.search(s) and 'prefers-reduced-motion' not in s:
        fails.append("animates but has no `prefers-reduced-motion: reduce` block (2.3.3)")

    root, _sheet, controls, marks = analyse(s)

    bad = unknown_roles(root)
    if bad:
        fails.append("CTRL vocabulary: unknown ARIA role(s) %s — this gate cannot classify "
                     "them as interactive or structural, so it cannot tell whether the "
                     "elements carrying them are in scope for 2.5.8. Add each to "
                     "INTERACTIVE_ROLES or NON_INTERACTIVE_ROLES in _a11y_target.py before "
                     "shipping (dv-vocab shape: fail loud, never let an unknown default to "
                     "skip)." % bad)

    for r in controls:
        who = "`%s`" % r.el.descr()
        if r.verdict == "fail":
            fails.append("%s — %s" % (who, r.detail))
        elif r.verdict == "warn":
            (fails if CONTROL_TIER_44 == "fail" else warns).append(
                "%s — %s" % (who, r.detail))
        elif r.verdict == "unmeasured":
            notes.append("%s — UNMEASURED: %s" % (who, r.detail))
        elif r.verdict == "exception":
            notes.append("%s — %s" % (who, r.detail))

    for r in marks:
        who = "`%s`" % r.el.descr()
        if r.verdict == "under":
            (fails if MARK_TIER == "fail" else warns).append(
                "DATA MARK %s — %s (s116-D1: marks carry the 24 floor, not the 44 target)"
                % (who, r.detail))
        elif r.verdict == "unmeasured":
            notes.append("DATA MARK %s — UNMEASURED: %s" % (who, r.detail))

    return name, fails, warns, notes, controls, marks


def _tally(rows):
    c = {"pass": 0, "warn": 0, "fail": 0, "unmeasured": 0, "exception": 0, "under": 0}
    for _n, _f, _w, _no, controls, marks in rows:
        for r in controls:
            c[r.verdict] += 1
        for r in marks:
            c[r.verdict] += 1
    return c


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--selftest" in argv:
        return selftest()

    rows = [check(fp) for fp in sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))]
    nfail = sum(len(f) for _, f, _, _, _, _ in rows)
    nwarn = sum(len(w) for _, _, w, _, _, _ in rows)
    nnote = sum(len(n) for _, _, _, n, _, _ in rows)

    n_ctrl = sum(len(c) for *_x, c, _m in rows)
    n_mark = sum(len(m) for *_x, _c, m in rows)
    under = [(n, r) for n, _f, _w, _no, _c, marks in rows for r in marks
             if r.verdict == "under"]
    under_files = {}
    for n, _r in under:
        under_files[n] = under_files.get(n, 0) + 1

    lines = [
        "# A11y gate — _validate_a11y.py", "",
        f"**{len(rows)} snippet(s)** · **{nfail} failure(s)** · **{nwarn} warning(s)** · "
        f"**{nnote} note(s)**", "",
        f"Measured MARKUP-DRIVEN (s114-D5, rebuilt #116): **{n_ctrl} control(s)** and "
        f"**{n_mark} focusable data mark(s)** enumerated from the markup, sized through a "
        f"subject-aware cascade with `var()` resolved. Engine + declared gaps: "
        f"`knowledge/_a11y_target.py`.", "",
        "Gating: reduced-motion (2.3.3) · unknown ARIA role · CONTROL target under the "
        f"{FLOOR}px floor (2.5.8, aid-009). "
        f"Reported: CONTROL {FLOOR}–{TARGET_CONTROL - 1} vs the {TARGET_CONTROL} HSBC "
        f"default (axs-003; `s114-D6` promotes this to blocking, ordered after this "
        f"rebuild) · DATA MARK under {TARGET_MARK} (`s116-D1`) · UNMEASURED boxes.", "",
        "Library bar (aqa-003, ruled 2026-07-03): the canon is LIBRARY-GRADE — guideline "
        "and recommendation tiers bind it, not just standards.", "",
        "## Owed measurement — data marks below 24 (`s116-D1`, for Dave)", "",
        f"**{len(under)} focusable data mark(s) fall below the {TARGET_MARK}px dense-case "
        f"minimum**, across {len(under_files)} snippet(s):", "",
    ]
    for n in sorted(under_files):
        lines.append(f"- `{n}` — {under_files[n]}")
    lines += ["",
              "NOT WAIVED and NOT REMEDIED here: `s116-D1` orders this measurement BEFORE the "
              "mark tier goes blocking. `MARK_TIER` in this file is the single switch.", ""]

    for name, fails, warns, notes, _c, _m in rows:
        if not fails and not warns and not notes:
            continue
        lines.append(f"## {name}")
        for f in fails:
            lines.append(f"- 🔴 FAIL — {f}")
        for w in warns:
            lines.append(f"- 🟡 warn — {w}")
        for n in notes:
            lines.append(f"- ⚪ note — {n}")
        lines.append("")
    if nfail == 0 and nwarn == 0 and nnote == 0:
        lines.append("_No issues._")
    open(os.path.join(HERE, "_A11Y-GATE.md"), "w").write("\n".join(lines) + "\n")

    print(f"a11y gate: {len(rows)} snippet(s), {nfail} failure(s), {nwarn} warning(s), "
          f"{nnote} note(s) · {n_ctrl} controls + {n_mark} marks measured · "
          f"{len(under)} mark(s) below {TARGET_MARK}")
    if nfail:
        for name, fails, _w, _n, _c, _m in rows:
            for f in fails:
                print(f"  FAIL {name}: {f}")
    return 1 if nfail else 0


# =============================================================== BITE TEST
# Every new gate ships one AND wires it. The clauses below are kept SEPARATE on
# purpose: #104's lesson is that a mutation which only exercises the DETECTION
# clause never proves the REMEDIATION clause. So each is mutated on its own —
# D-* mutations break detection, R-* mutations break remediation, and a fix that
# silences one must leave the other still biting.
_HEAD = """<!doctype html><html><head><style>
:root{--control-h:32px; --hit:44px;}
%s
</style></head><body>%s</body></html>"""


def _run(css, body):
    _root, _sheet, controls, marks = analyse(_HEAD % (css, body))
    return controls, marks


def _verdicts(controls):
    return [(r.el.descr(), r.verdict, r.detail) for r in controls]


def selftest():
    ok, bad = 0, []

    def expect(label, got, want):
        nonlocal ok
        if got == want:
            ok += 1
        else:
            bad.append("%s: expected %r, got %r" % (label, want, got))

    # ---- DETECTION clause ------------------------------------------------
    # D1 — a <button> sized by a custom property is READ, not skipped. This is the
    #      literal-px blindness that hid `.dv-vt{height:var(--control-h)}`.
    c, _ = _run(".vt{height:var(--control-h); width:var(--control-h);}",
                '<button class="vt">x</button>')
    expect("D1 var()-sized control detected", (c[0].verdict, c[0].h), ("warn", 32.0))

    # D2 — a <summary> is a control. The old allowlist never contained one.
    c, _ = _run("summary{height:16px; width:16px;}",
                "<details><summary>View as table</summary><p>t</p></details>")
    expect("D2 summary is enumerated", [r.verdict for r in c], ["fail"])

    # D3 — an element the markup declares operable by ROLE ALONE enters scope. No
    #      tabindex here on purpose: with one, the tabindex clause would carry the
    #      test and the role vocabulary could be deleted without the suite noticing.
    c, _ = _run(".sw{width:12px; height:12px;}", '<span class="sw" role="checkbox"></span>')
    expect("D3 role-declared control detected", [r.verdict for r in c], ["fail"])

    # D3b — and TABINDEX alone also enters scope, independently of role. This is
    #       how the corpus's `.dv-leg-sw` (role + tabindex) would stay covered if
    #       either half were dropped.
    c, _ = _run(".sw{width:12px; height:12px;}", '<span class="sw" tabindex="0"></span>')
    expect("D3b tabindex-declared control detected", [r.verdict for r in c], ["fail"])

    # D6 — `min-width:0` is a flexbox RESET, not a 0px target. The width beside it is
    #      a percentage on purpose: with a px width the max() hides the bug, so the
    #      clause would not bite. Read as a size, this control is 0px wide and fails —
    #      the phantom-failure shape one layer down (it flagged every text field).
    c, _ = _run(".b{width:100%; min-width:0; height:44px;}", '<button class="b">x</button>')
    expect("D6 a min-*:0 reset is not a declared size",
           [r.verdict for r in c], ["unmeasured"])

    # D7 — `a[href]` is in the ruled control set. A bare `<a>` with no href is not.
    c, _ = _run(".l{width:16px; height:16px;}",
                '<a class="l" href="#x">go</a><a class="l">anchor</a>')
    expect("D7 a[href] is a control, a bare anchor is not",
           [r.verdict for r in c], ["fail"])

    # D8 — a focusable `<g>` wrapper is sized from the shape it wraps. The corpus
    #      puts tabindex on the group and the geometry on an inner <circle>.
    _c, m = _run("", '<svg viewBox="0 0 100 100" width="100" height="100">'
                     '<g class="dv-marker" tabindex="0"><circle r="5.5" cx="50" cy="50"/>'
                     "</g></svg>")
    expect("D8 <g> marker measured from its child shape",
           [(r.verdict, r.w) for r in m], [("under", 11.0)])

    # D10 — an arc segment (donut/pie) is measured on its RADIAL THICKNESS and its
    #       mid-radius arc length, not a bbox. A thin ring is a thin target however
    #       wide the slice is; without this the shape falls through to `unmeasured`
    #       and a thin donut would silently escape the 24 floor.
    _c, m = _run("", '<svg viewBox="0 0 300 300" width="300" height="300">'
                     '<path class="dv-series dv-marker" tabindex="0" data-ro="100" '
                     'data-ri="92" data-a1="0" data-a2="90" d="M0 0"/></svg>')
    expect("D10 thin arc segment measured on radial thickness",
           [(r.verdict, round(r.h, 1)) for r in m], [("under", 8.0)])

    # D11 — MUTATION of D10: the same arc at canon thickness passes.
    _c, m = _run("", '<svg viewBox="0 0 300 300" width="300" height="300">'
                     '<path class="dv-series dv-marker" tabindex="0" data-ro="100" '
                     'data-ri="60" data-a1="0" data-a2="90" d="M0 0"/></svg>')
    expect("D11 canon-thickness arc segment passes", [r.verdict for r in m], ["pass"])

    # D9 — SVG user units are scaled by the svg's own width/viewBox ratio. Unscaled,
    #      this 15-unit rect reads 15 and fails; scaled 2x it is a compliant 30.
    _c, m = _run("", '<svg viewBox="0 0 100 100" width="200" height="200">'
                     '<rect class="dv-series" tabindex="0" width="15" height="15"/></svg>')
    expect("D9 SVG user units are scaled to CSS px",
           [(r.verdict, r.w) for r in m], [("pass", 30.0)])

    # D4 — a data mark is measured against 24, not 44, and not skipped.
    _c, m = _run("", '<svg viewBox="0 0 100 100" width="100" height="100">'
                     '<rect class="dv-series" tabindex="0" width="10" height="40"/></svg>')
    expect("D4 data mark measured at the 24 floor",
           [(r.verdict, r.target) for r in m], [("under", TARGET_MARK)])

    # ---- DECORATION clause (the six phantoms) ----------------------------
    # P1 — an aria-hidden child of a compliant control is NOT a control. The old
    #      matcher flagged `.as-trigger .chev` because it tested ancestor tokens.
    c, _ = _run(".t{min-height:44px; min-width:44px;} .t .chev{width:16px; height:16px;}",
                '<button class="t"><span class="chev" aria-hidden="true"></span></button>')
    expect("P1 decorative child is not a control", [r.verdict for r in c], ["pass"])

    # P2 — MUTATION of P1: make the same child focusable and it MUST be flagged.
    #      Proves P1 passes by classification, not by a blanket child-skip.
    c, _ = _run(".t{min-height:44px; min-width:44px;} .t .chev{width:16px; height:16px;}",
                '<button class="t"><span class="chev" role="button" tabindex="0">'
                '</span></button>')
    expect("P2 the same box, made operable, IS flagged",
           sorted(r.verdict for r in c), ["fail", "pass"])

    # P3 — SUBJECT SCOPING. `.panel .b` must not size a `.b` that is not inside a
    #      `.panel`. This is the ancestor-blind matcher itself, isolated: P1/P2
    #      pass by classification even with the matcher broken, so without P3 the
    #      old `is_ctrl` could be restored wholesale and the suite stay green.
    c, _ = _run(".b{width:44px; height:44px;} .panel .b{width:16px; height:16px;}",
                '<button class="b">out</button>')
    expect("P3 a descendant-scoped rule does not size an unscoped control",
           [(r.verdict, r.w) for r in c], [("pass", 44.0)])

    # P4 — MUTATION of P3's neighbour: the SAME rule DOES apply in scope.
    c, _ = _run(".b{width:44px; height:44px;} .panel .b{width:16px; height:16px;}",
                '<div class="panel"><button class="b">in</button></div>')
    expect("P4 the same rule applies when the ancestor is present",
           [(r.verdict, r.w) for r in c], [("fail", 16.0)])

    # P5 — a passive `aria-hidden` specimen is not an operable control. Isolated
    #      because P1's chevron is excluded by tag/role anyway.
    c, _ = _run(".b{width:16px; height:16px;}",
                '<div aria-hidden="true"><button class="b">demo</button></div>')
    expect("P5 aria-hidden specimen is out of scope", [r.verdict for r in c], [])

    # D5 — a data mark in the 24–43 band PASSES: marks carry the 24 floor, not the
    #      44 control target (s116-D1). D4 alone cannot see this — 10x40 is under
    #      both thresholds, so raising TARGET_MARK to 44 leaves D4 green.
    _c, m = _run("", '<svg viewBox="0 0 100 100" width="100" height="100">'
                     '<rect class="dv-series" tabindex="0" width="30" height="30"/></svg>')
    expect("D5 a 30x30 mark passes at 24 and is NOT held to 44",
           [r.verdict for r in m], ["pass"])

    # ---- REMEDIATION clause (separate from detection, per #104) ----------
    # R1 — a canon ::before expander that REACHES the target is a measured pass.
    c, _ = _run(".b{height:32px; width:32px;} "
                '.b::before{content:""; position:absolute; min-width:var(--hit,44px); '
                "min-height:var(--hit,44px);}",
                '<button class="b">x</button>')
    expect("R1 compliant expander passes", [r.verdict for r in c], ["pass"])

    # R2 — MUTATION of R1: the SAME control, expander shrunk under the floor, must
    #      FAIL. The old gate exempted any selector that merely HAD a ::before, so
    #      this mutation could not have been caught by a detection test at all.
    c, _ = _run(".b{height:32px; width:32px;} "
                '.b::before{content:""; position:absolute; min-width:16px; min-height:16px;}',
                '<button class="b">x</button>')
    expect("R2 under-floor expander is not a remediation",
           [r.verdict for r in c], ["fail"])

    # R3 — MUTATION of R1: an expander between the floor and the default warns; it
    #      neither passes silently (the old blind exemption) nor fails.
    c, _ = _run(".b{height:32px; width:32px;} "
                '.b::before{content:""; position:absolute; min-width:36px; min-height:36px;}',
                '<button class="b">x</button>')
    expect("R3 partial expander warns", [r.verdict for r in c], ["warn"])

    # R4 — a claimed 2.5.8 exception discharges, and CARRIES ITS REASON. An
    #      exception with no written reason is not a legal discharge.
    c, _ = _run(".b{height:16px; width:16px;}",
                '<button class="b" %s="inline in a sentence of text (2.5.8 inline out)">x'
                "</button>" % EXCEPTION_ATTR)
    expect("R4 claimed exception discharges", [r.verdict for r in c], ["exception"])
    expect("R4 exception records its reason", "inline in a sentence" in c[0].detail, True)

    # R5 — MUTATION of R4: a WHITESPACE-ONLY reason must not discharge. Empty-string
    #      would be caught by truthiness alone; only whitespace proves the strip.
    c, _ = _run(".b{height:16px; width:16px;}",
                '<button class="b" %s="   ">x</button>' % EXCEPTION_ATTR)
    expect("R5 a reasonless exception does not discharge", [r.verdict for r in c], ["fail"])

    # ---- HONESTY clause --------------------------------------------------
    # H1 — a layout-determined box comes back UNMEASURED, never a guessed pass.
    c, _ = _run(".b{padding:12px 16px;}", '<button class="b">x</button>')
    expect("H1 layout-determined box is unmeasured", [r.verdict for r in c], ["unmeasured"])

    # H2 — but a half-measured box under the floor still FAILS (EITHER-dimension
    #      semantics, aid-009): the unknown axis cannot rescue a known 4px.
    c, _ = _run(".b{width:100%; height:4px;}",
                '<div class="b" role="slider" tabindex="0"></div>')
    expect("H2 one known axis under the floor still fails",
           [r.verdict for r in c], ["fail"])

    print("a11y target selftest: %d clause(s) green, %d failing" % (ok, len(bad)))
    for b in bad:
        print("  ✗ " + b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
