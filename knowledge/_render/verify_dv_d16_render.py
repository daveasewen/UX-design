#!/usr/bin/env python3
"""DV-D16 (wording ②) enactment proof — EVERY stacked surface in the repo.

★ #219 — DV-D16b IS FORWARD-BINDING ("every stacked surface, not Chart-bar alone"), so this probe
is no longer one file wide. `--target` selects a surface and `--target all` runs every one:

  snippet    knowledge/snippets/Chart-bar.reference.html   · cb5, 3 deep, dv-004 by GEOMETRIC GAP
  proforma   knowledge/_proforma/DataViz-interactive.html  · stk1, 4 deep, dv-004 by 2px STROKE

The two surfaces differ in three ways that a single hard-coded probe cannot see, so each is a
PROFILE rather than a copy: the figure's `data-dv-type` token, the on-segment key element, and
which half of dv-004's ≥2px rule the file uses. Nothing is relaxed to make the second surface
pass — the stroke profile asserts CONTIGUITY plus a declared ≥2px page-coloured stroke, which is
the same 2px boundary arriving by the other route.

Two halves, and BOTH are meant to be run:

  --static   parses the target and RE-DERIVES every emitted
             `--b*` from the file's own rect `y`/`height` attributes (the ENACTED geometry, DV-D14 —
             never the data labels), then asserts the curve assignment, the registrations and the
             transform composition. Document-vs-document, and it says so.
  --render   drives a real Chromium, PAUSES the shared timeline at sampled frames, and measures the
             rendered boxes. This is the half that can see whether the stack actually stays
             contiguous while it grows, whether all segments are moving AT ONCE (wording ②, not the
             reversed serial wording ①), and whether each segment is really on its own curve.

  --mutate <arm>   applies ONE break to an in-memory/temp copy and expects the named check to FIRE.
                   Arms (10): b-value · self-swap · curve-drop · ease-token-swap · ease-token-value ·
                   key-delay-drop · translate-term · rest-scale · rect-count · wording-1
                   (`--mutate all` runs every arm.) A probe that cannot go red proves nothing.
                   Each PROFILE carries its own arm table, keyed on its own literals — an arm that
                   changes nothing reports itself a DANGLE rather than passing quietly.

★ #219 ADDED THE `wording-1` CHECK, AND IT IS THE ONE THAT GUARDS THE REVERSAL. DV-D16a was ruled
and then reversed inside one session: wording ① ("segment 2 starts when segment 1 lands") is
DO-NOT-BUILD, and its signature is per-rect `animation-delay` / `animation-duration` /
`animation-timing-function`. `_gen_dataviz_charts.py` was still emitting exactly that on the
pro-forma's stacked figure eighteen sessions after the reversal, and Chart-bar still carried the
inert 45ms/rect stagger the enactment left behind. Both are gone, and WORDING-1 is what keeps them
gone: a stacked rect that declares its own timing is RED by name, on every surface.

s218-D5 UPDATED THE EXPECTATIONS THIS PROBE ASSERTS — it did not merely add to them:
  (1) the two curved positions are the HOUSE tokens `var(--grow-ease-in)` / `var(--grow-ease-out)`,
      NOT the CSS keywords `ease-in` / `ease-out`. The old keyword expectation is GONE: a file that
      still says `ease-out` there is now RED (arm: ease-token-swap). The token VALUES are asserted
      too — --grow-ease-out must be --grow's own curve and --grow-ease-in its exact reversal, so a
      token that drifts out of the family cannot pass by merely existing (arm: ease-token-value).
      The render half no longer hard-codes the curve maths: it READS the two beziers out of the
      file it is about to render, so the measurement and the artefact can never disagree by
      staleness.
  (2) the on-segment letter keys are DELAYED by one full growth. Statically that is an
      animation-delay longhand AFTER the generic shorthand (arm: key-delay-drop); in the render
      half it is MEASURED — every key is at opacity 0 while the stack is still moving, and every
      key HAS arrived once the fade completes (a key that never appears is not a fix).

⚠ SCOPE, DECLARED: the render half measures GEOMETRY only, so it does not stand up the HSBC font
farm (_RUNBOOK-render-verify.md § 5) — no assertion here depends on the face. It is not a substitute
for the font-bearing render checks, and it does not clear a "render-verify OWED" note about type.
"""
import argparse, glob, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIP = os.path.join(ROOT, "snippets", "Chart-bar.reference.html")
DUR_MS = 760.0
MIN_GAP = 2.0                     # dv-004 — Dave's ruled >=2px segment boundary
# NOT a tolerance anyone chose: the chart generators emit `y` and `height` rounded to ONE decimal
# place, so two edges that are contiguous in the maths can disagree on paper by up to 0.05 + 0.05.
# This is the precision of the artefact, and a contiguity assertion tighter than it is a false red.
EMIT_ULP = 0.1

# ---------------------------------------------------------------- the surfaces (DV-D16b)
# `sep` is WHICH HALF of dv-004 the file uses, not a tolerance:
#   "gap"    — the ruled 2px is empty page between the rects (Chart-bar's DV-D14 geometry)
#   "stroke" — the rects are contiguous and the ruled 2px is a page-coloured stroke on them
# `reduce` is how the file honours prefers-reduced-motion:
#   "neutralise" — a global `reduce` block zeroes animation-duration
#   "gated"      — every entry animation lives inside the no-preference block, so `reduce` has
#                  nothing to neutralise; asserted by proving the float rules appear ONCE, inside.
PROFILES = {
    "snippet": dict(
        path=SNIP,
        fig_re=r'<figure class="dv dv-animate" data-dv-type="stacked-column".*?</figure>',
        scope='figure.dv-animate[data-dv-type="stacked-column"]',
        js_fig='figure[data-dv-type="stacked-column"]',
        key='text.dv-barkey',
        key_generic=r'\.dv-animate\s+text\.dv-barkey\s*\{[^}]*animation:\s*dvFade[^}]*\}',
        sep="gap", stroke=0.0, reduce="neutralise"),
    "proforma": dict(
        path=os.path.join(ROOT, "_proforma", "DataViz-interactive.html"),
        fig_re=r'<figure class="dv" data-dv-type="stacked".*?</figure>',
        scope='.dv-animate figure[data-dv-type="stacked"]',
        js_fig='figure[data-dv-type="stacked"]',
        key='text.dv-key-el',
        key_generic=r'\.dv-animate\s+text\.dv-key-el:not\(\[data-rise\]\):not\(\.dv-anno\)'
                    r'[^{]*\{[^}]*animation:\s*dvFade[^}]*\}',
        sep="stroke", stroke=2.0, reduce="gated"),
}

# ---------------------------------------------------------------- easing maths
def _bez(p1x, p1y, p2x, p2y):
    def bx(t): return 3*(1-t)**2*t*p1x + 3*(1-t)*t*t*p2x + t**3
    def by(t): return 3*(1-t)**2*t*p1y + 3*(1-t)*t*t*p2y + t**3
    def f(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo+hi)/2
            if bx(mid) < x: lo = mid
            else: hi = mid
        return by((lo+hi)/2)
    return f

# s218-D5 (1): the curved positions are TOKENS now, and the maths is READ OFF THE ARTEFACT.
# `linear` stays a keyword because linear is linear — there is no house kin for it.
FIRST_CURVE = "var(--grow-ease-in)"
LAST_CURVE  = "var(--grow-ease-out)"

def _bez_decl(html, name):
    """the four numbers of a `--<name>:cubic-bezier(a,b,c,d)` declaration, or None."""
    m = re.search(r'--%s:\s*cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)'
                  % re.escape(name), html)
    return tuple(float(g) for g in m.groups()) if m else None

def house_curves(html):
    """{position-keyword -> easing fn} built from the FILE's own tokens. No hard-coded maths."""
    ein, eout = _bez_decl(html, "grow-ease-in"), _bez_decl(html, "grow-ease-out")
    return {FIRST_CURVE: _bez(*ein) if ein else None,
            "linear":    lambda x: x,
            LAST_CURVE:  _bez(*eout) if eout else None}

# ---------------------------------------------------------------- parsing
def figure_block(html, P):
    m = re.search(P["fig_re"], html, re.S)
    return m.group(0) if m else None

def attr(tag, name, default=None):
    m = re.search(r'\s%s="([^"]*)"' % name, tag)
    return m.group(1) if m else default

def columns(fig):
    """rects grouped by x, each column ordered BOTTOM-first (largest y first)."""
    rects = re.findall(r'<rect class="dv-series"[^>]*>(?:</rect>)?', fig)
    cols = {}
    for t in rects:
        cols.setdefault(attr(t, "x"), []).append(t)
    for x in cols:
        cols[x].sort(key=lambda t: -float(attr(t, "y")))
    return rects, cols

# ---------------------------------------------------------------- static half
def static_checks(html, P, verbose=True):
    F = []                                          # failures, each NAMED
    SCOPE = re.escape(P["scope"])
    def say(s):
        if verbose: print("   " + s)
    fig = figure_block(html, P)
    if not fig:
        return ["MISSING-FIGURE: no %s figure in %s" % (P["scope"], os.path.basename(P["path"]))]
    rects, cols = columns(fig)

    # -- non-trivial count guard: a probe that reads 0==0 is the mutant-dangle defect ------------
    if len(rects) < 3:
        F.append("RECT-COUNT: only %d stacked rects parsed — the probe would be vacuous (need >=3)"
                 % len(rects))
        return F
    say("stacked rects parsed: %d in %d columns (guard: >=3)" % (len(rects), len(cols)))

    depth = max(len(v) for v in cols.values())

    # -- (a) FLOAT: every emitted --b re-derived from the artefact's own geometry ---------------
    for x, col in sorted(cols.items(), key=lambda kv: float(kv[0])):
        for i, t in enumerate(col):
            style = attr(t, "style", "")
            got = dict(re.findall(r'--b(\d+):\s*([0-9.]+)px', style))
            want = {str(j+1): attr(col[j], "height") for j in range(i)}
            lbl = "x=%s seg%d (%s)" % (x, i+1, attr(t, "aria-label") or attr(t, "data-tip", "?"))
            if set(got) != set(want):
                F.append("BELOW-SET: %s emits --b%s, geometry says --b%s"
                         % (lbl, sorted(got) or "-", sorted(want) or "-"))
            for k in sorted(set(got) & set(want)):
                if abs(float(got[k]) - float(want[k])) > 1e-9:
                    F.append("BELOW-VALUE: %s --b%s=%spx but the rect below it is %spx tall"
                             % (lbl, k, got[k], want[k]))
            self_ = re.search(r'--self:\s*var\(--dvf(\d+)\)', style)
            if not self_:
                F.append("SELF-MISSING: %s carries no --self progress var" % lbl)
            elif int(self_.group(1)) != i + 1:
                F.append("SELF-INDEX: %s is segment %d from the bottom but rides --dvf%s"
                         % (lbl, i+1, self_.group(1)))
            # ★ #219 WORDING-1 — the reversal, inscribed. wording ① is per-rect timing; wording ②
            # puts the whole timeline on the <svg> and leaves the rect declaring only WHICH
            # progress number is its own. A rect that carries its own delay/duration/timing
            # function is either the reversed shape or its dead residue, and both read as ①.
            for prop in ("animation-delay", "animation-duration", "animation-timing-function"):
                if prop in style:
                    F.append("WORDING-1: %s declares `%s` — DV-D16a wording ① (serial, "
                             "segment-waits-for-segment) was REVERSED in its own session and is "
                             "DO-NOT-BUILD; under wording ② the shared timeline lives on the "
                             "<svg> and no stacked rect carries timing of its own" % (lbl, prop))
            # rest-state boundary, the dv-004 mirror (also proves --b is on the ENACTED geometry)
            if i:
                # SVG y grows DOWNWARD: col[i] sits ABOVE col[i-1], so the boundary is the
                # lower rect's TOP minus the upper rect's bottom edge.
                gap = float(attr(col[i-1], "y")) - (float(attr(col[i], "y")) + float(attr(col[i], "height")))
                if P["sep"] == "gap":
                    if gap + 1e-9 < MIN_GAP:
                        F.append("DV-004-REST: %s boundary is %.2fpx (< %.1f)" % (lbl, gap, MIN_GAP))
                elif abs(gap) > EMIT_ULP + 1e-9:
                    F.append("DV-004-REST: %s is a STROKE-separated surface, so its rects must be "
                             "contiguous for the 2px stroke to sit on the shared edge — measured "
                             "%.2fpx of geometry between them" % (lbl, gap))
        if P["sep"] == "stroke":
            # the other half of dv-004 on this surface: the boundary IS the stroke, so its width
            # and its colour are the ruled 2px, and a presence check is not enough.
            for t in col:
                sw, sc = attr(t, "stroke-width"), attr(t, "stroke")
                if sw is None or float(sw) + 1e-9 < MIN_GAP:
                    F.append("DV-004-STROKE: a stacked rect declares stroke-width=%s — this surface "
                             "carries the ruled >=%.1fpx boundary as a stroke, so a thinner one IS "
                             "a thinner boundary" % (sw, MIN_GAP))
                if sc != "var(--page)":
                    F.append("DV-004-STROKE: a stacked rect strokes `%s`, not var(--page) — a "
                             "boundary that is not the page colour is a hairline, not a separation"
                             % sc)
    say("--b values re-derived from y/height attributes and matched; --self indices bottom-up OK")
    say("no stacked rect declares its own timing (wording ① cannot come back unseen)")

    # -- (b) per-segment curves on ONE shared timeline ------------------------------------------
    svg_rule = SCOPE + r'\s*svg\.dv-svg\{([^}]*)\}'
    m = re.search(svg_rule, html)
    if not m:
        F.append("TIMELINE-RULE: no `%s svg.dv-svg` rule — nothing animates the shared progress "
                 "numbers" % P["scope"])
    else:
        items = [i.strip() for i in re.sub(r'\s+', ' ', m.group(1)).split("animation:")[1].rstrip(";").split(",")]
        parsed = []
        for it in items:
            mm = re.match(r'(dvStackF(\d+))\s+var\(--grow-dur\)\s+(\S+)\s+both', it)
            if not mm:
                F.append("TIMELINE-SHAPE: cannot parse animation item %r "
                         "(want `dvStackF<n> var(--grow-dur) <curve> both`)" % it)
            else:
                parsed.append((int(mm.group(2)), mm.group(3)))
        if parsed:
            if len(parsed) < depth:
                F.append("TIMELINE-DEPTH: %d progress animations for a stack %d deep"
                         % (len(parsed), depth))
            for pos, (idx, curve) in enumerate(parsed, start=1):
                if idx != pos:
                    F.append("TIMELINE-ORDER: item %d animates dvStackF%d" % (pos, idx))
                want = FIRST_CURVE if pos == 1 else (LAST_CURVE if pos == len(parsed) else "linear")
                if curve != want:
                    F.append("CURVE: segment %d of %d is `%s`, DV-D16's positional rule + s218-D5's "
                             "house family rule `%s` (first %s - intermediates linear - last %s; "
                             "the bare CSS keywords were retired at s218-D5)"
                             % (pos, len(parsed), curve, want, FIRST_CURVE, LAST_CURVE))
            say("curves: " + " - ".join("seg%d %s" % p for p in parsed) + "  (one shared var(--grow-dur))")
        # one shared duration, and it is the file's own 760ms
        dm = re.search(r'--grow-dur:\s*([0-9.]+)ms', html)
        if not dm:
            F.append("DURATION-VAR: --grow-dur is not declared")
        elif abs(float(dm.group(1)) - DUR_MS) > 1e-9:
            F.append("DURATION-VAR: --grow-dur is %sms, expected %.0fms" % (dm.group(1), DUR_MS))
        gm = re.search(r'--grow:\s*([0-9.]+)ms', html)
        if gm and dm and gm.group(1) != dm.group(1):
            F.append("DURATION-DRIFT: --grow is %sms but --grow-dur is %sms — one gesture, one number"
                     % (gm.group(1), dm.group(1)))

    # -- (b2) s218-D5 (1): the two curve tokens ARE the house family, not merely present ----------
    #    Declared-and-wrong is the failure mode a presence check cannot see, so the VALUES are
    #    asserted: --grow-ease-out is --grow's own curve, --grow-ease-in is its exact reversal
    #    (1-x2, 1-y2, 1-x1, 1-y1). Both are re-derived from the file, never from a memory of them.
    house = re.search(r'--grow:\s*[0-9.]+ms\s+cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,'
                      r'\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)', html)
    ein, eout = _bez_decl(html, "grow-ease-in"), _bez_decl(html, "grow-ease-out")
    if not house:
        F.append("TOKEN: --grow carries no cubic-bezier — the house curve the family is named for "
                 "cannot be read, so nothing can be checked against it")
    for nm, val in (("--grow-ease-in", ein), ("--grow-ease-out", eout)):
        if val is None:
            F.append("TOKEN: %s is not declared as a cubic-bezier(...) — s218-D5 moved the stacked "
                     "curves onto the house tokens; a missing token means the animation falls back "
                     "to the initial `ease` and the family claim is false" % nm)
    if house and eout is not None:
        h = tuple(float(g) for g in house.groups())
        if any(abs(a - b) > 1e-9 for a, b in zip(h, eout)):
            F.append("TOKEN: --grow-ease-out is cubic-bezier%s but --grow's own curve is "
                     "cubic-bezier%s — the token has drifted OUT of the house family" % (eout, h))
        if ein is not None:
            rev = (1 - h[2], 1 - h[3], 1 - h[0], 1 - h[1])
            if any(abs(a - b) > 1e-9 for a, b in zip(rev, ein)):
                F.append("TOKEN: --grow-ease-in is cubic-bezier%s, the exact reversal of the house "
                         "curve is cubic-bezier%s — the two ends are no longer one gesture read "
                         "forwards and backwards" % (ein, rev))
        say("house family: --grow-ease-out=cubic-bezier%s (= --grow), --grow-ease-in=cubic-bezier%s"
            % (eout, ein))

    # -- (b3) s218-D5 (2): the stacked letter keys wait one full growth ---------------------------
    #    The delay is a LONGHAND that must sit AFTER the generic `animation:` shorthand (which
    #    resets animation-delay to 0s) and INSIDE the no-preference block. Order is load-bearing,
    #    so it is asserted by POSITION, not merely by presence.
    kd = re.search(SCOPE + r'\s*' + re.escape(P["key"]) + r'[^{}]*\{'
                   r'\s*animation-delay:\s*var\(--grow-dur\)[^}]*\}', html)
    gen = re.search(P["key_generic"], html)
    if not kd:
        F.append("KEY-DELAY: no `%s %s` rule delaying the fade by var(--grow-dur) — s218-D5 (2) "
                 "retired the mid-flight " % (P["scope"], P["key"]) +
                 "adrift key; without the delay a key fades in ON a segment that is still scaling "
                 "AND floating, and labels a fill that is not there yet")
    elif gen and gen.start() > kd.start():
        F.append("KEY-DELAY-ORDER: the generic `animation:dvFade` shorthand is declared AFTER the "
                 "stacked delay longhand, so it resets animation-delay to 0s and the delay is dead")
    else:
        say("stacked letter keys delayed by var(--grow-dur), after the generic dvFade shorthand")

    # -- registrations + keyframes, and the transform composition -------------------------------
    for n in range(1, depth + 1):
        if not re.search(r'@property\s+--dvf%d\{[^}]*syntax:"<number>"[^}]*inherits:true[^}]*'
                         r'initial-value:1;[^}]*\}' % n, html):
            F.append("REGISTER: --dvf%d is not registered <number>/inherits:true/initial-value:1 "
                     "(unregistered custom properties do not animate, and the initial value is the "
                     "JS-off / unsupported-@property landing frame)" % n)
        if not re.search(r'@keyframes dvStackF%d\{from\{--dvf%d:0;\} to\{--dvf%d:1;\}\}' % (n, n, n), html):
            F.append("KEYFRAMES: @keyframes dvStackF%d is missing or is not 0 -> 1" % n)
    rm = re.search(SCOPE + r'\s*rect\.dv-series\[data-grow="up"\]\{(.*?)\}\s*\n', html, re.S)
    if not rm:
        F.append("RECT-RULE: no stacked rect rule — the rects would still run the shared dvGrowY "
                 "and would grow from their own fixed anchors (the DV-D16 (a) defect)")
    else:
        body = re.sub(r'\s+', '', rm.group(1))
        if "animation:none" not in body:
            F.append("RECT-RULE: stacked rects do not cancel the generic dvGrowY animation")
        if "transform-box:fill-box" not in body or "transform-origin:bottom" not in body:
            F.append("RECT-RULE: transform-box/transform-origin missing — scaleY would not be "
                     "anchored to the segment's own bottom edge")
        if "scaleY(var(--self" not in body:
            F.append("RECT-RULE: scaleY does not read the per-rect --self progress")
        used = sorted({int(k) for c in cols.values() for t in c
                       for k in re.findall(r'--b(\d+):', attr(t, "style", ""))})
        for n in used:
            term = "var(--b%d,0px)*(1-var(--dvf%d))" % (n, n)
            if term not in body:
                F.append("COMPOSE: the translate has no `%s` term, so segments riding --b%d would "
                         "track the WRONG height mid-flight" % (term, n))
        say("transform composes translateY(sum of %d below-terms) . scaleY(--self); dvGrowY cancelled"
            % len(used))

    # -- reduced motion: the float lives inside no-preference, and reduce lands on the final frame
    if not re.search(r'@media \(prefers-reduced-motion:no-preference\)\{[^@]*?' + SCOPE, html, re.S):
        F.append("REDUCED-MOTION: the stacked float rules are not inside a "
                 "(prefers-reduced-motion:no-preference) block — under `reduce` the transform would "
                 "still apply and the chart could rest off its final frame")
    if P["reduce"] == "neutralise":
        if not re.search(r'@media \(prefers-reduced-motion: reduce\)\{[^}]*animation-duration:\.01ms !important',
                         html, re.S):
            F.append("REDUCED-MOTION: the global reduce block no longer neutralises animation-duration")
    else:
        # "gated": there is no reduce block to neutralise anything, so the ONLY thing standing
        # between `reduce` and a moving chart is that the float rules appear exactly once, inside
        # the no-preference block. A second copy anywhere else silently defeats the whole floor.
        n_scope = len(re.findall(SCOPE + r'\s*(?:svg\.dv-svg|rect\.dv-series)', html))
        if n_scope != 2:
            F.append("REDUCED-MOTION: %d `%s` timeline/rect rules found, expected exactly 2 (the "
                     "shared-timeline rule and the rect rule) — on a no-preference-GATED surface a "
                     "stray copy outside the block is the whole reduced-motion defect"
                     % (n_scope, P["scope"]))

    # -- DEF-003: nothing here may add JS -------------------------------------------------------
    if re.search(r'dvf1|dvStackF|--self', "".join(re.findall(r'<script[^>]*>(.*?)</script>', html, re.S))):
        F.append("DEF-003: the float mechanism leaked into <script> — it must be pure CSS")
    return F

# ---------------------------------------------------------------- mutations
MUTATIONS = {
 "b-value":       (lambda h: h.replace("--b1:42.1px", "--b1:41.1px", 1), "BELOW-VALUE"),
 "self-swap":     (lambda h: h.replace("--b1:42.1px; --b2:73.6px; --self:var(--dvf3)",
                                       "--b1:42.1px; --b2:73.6px; --self:var(--dvf2)", 1), "SELF-INDEX"),
 # ⚠ s218-D5 re-pointed this arm's TEXT: the old literal ("... ease-out both") no longer exists in
 # the file, so left alone the arm would have changed nothing and reported itself a DANGLE.
 "curve-drop":    (lambda h: h.replace("dvStackF3 var(--grow-dur) var(--grow-ease-out) both",
                                       "dvStackF3 var(--grow-dur) linear both", 1), "CURVE"),
 # s218-D5 (1) — the REGRESSION arm: the keyword the ruling retired, put back.
 "ease-token-swap":(lambda h: h.replace("dvStackF1 var(--grow-dur) var(--grow-ease-in) both",
                                        "dvStackF1 var(--grow-dur) ease-in both", 1), "CURVE"),
 # s218-D5 (1) — the token DECLARED BUT WRONG arm: still a cubic-bezier, no longer the family.
 "ease-token-value":(lambda h: h.replace("--grow-ease-in:cubic-bezier(.64,0,.78,.39)",
                                         "--grow-ease-in:cubic-bezier(.42,0,1,1)", 1), "TOKEN"),
 # s218-D5 (2) — the delay removed: statically KEY-DELAY, and in the render half KEY-EARLY.
 "key-delay-drop":(lambda h: h.replace(
                     'figure.dv-animate[data-dv-type="stacked-column"] text.dv-barkey'
                     '{animation-delay:var(--grow-dur);}', "", 1), "KEY-DELAY"),
 "translate-term":(lambda h: h.replace(" + var(--b2,0px) * (1 - var(--dvf2))", "", 1), "COMPOSE"),
 # render-only arm: proves the REST probes (end frame, reduced motion, JS-off) can go red at all.
 "rest-scale":    (lambda h: h.replace("scaleY(var(--self,1))", "scaleY(calc(var(--self,1) * 0.8))", 1),
                   "END"),
 "rect-count":    (lambda h: re.sub(r'(<figure class="dv dv-animate" data-dv-type="stacked-column".*?</figure>)',
                                    lambda m: re.sub(r'<rect class="dv-series"[^>]*></rect>\s*', "", m.group(1), count=10),
                                    h, flags=re.S), "RECT-COUNT"),
 # ★ #219 — THE REVERSAL ARM. wording ①'s residue, put back on one rect.
 "wording-1":     (lambda h: h.replace('style="--b1:42.1px; --self:var(--dvf2)"',
                                       'style="animation-delay:45ms; animation-duration:400ms; '
                                       'animation-timing-function:linear; --b1:42.1px; '
                                       '--self:var(--dvf2)"', 1), "WORDING-1"),
}

# The pro-forma's arms — same ten breaks, keyed on ITS literals. Not a copy of the table above:
# a shared arm table would either dangle on one surface or silently test the other one twice.
MUTATIONS_PROFORMA = {
 "b-value":       (lambda h: h.replace("--b1:68.4px", "--b1:67.4px", 1), "BELOW-VALUE"),
 "self-swap":     (lambda h: h.replace("--self:var(--dvf4)", "--self:var(--dvf3)", 1), "SELF-INDEX"),
 "curve-drop":    (lambda h: h.replace("dvStackF4 var(--grow-dur) var(--grow-ease-out) both",
                                       "dvStackF4 var(--grow-dur) linear both", 1), "CURVE"),
 "ease-token-swap":(lambda h: h.replace("dvStackF1 var(--grow-dur) var(--grow-ease-in) both",
                                        "dvStackF1 var(--grow-dur) ease-in both", 1), "CURVE"),
 "ease-token-value":(lambda h: h.replace("--grow-ease-in:cubic-bezier(.64,0,.78,.39)",
                                         "--grow-ease-in:cubic-bezier(.42,0,1,1)", 1), "TOKEN"),
 "key-delay-drop":(lambda h: h.replace("animation-delay:var(--grow-dur);}", "}", 1), "KEY-DELAY"),
 "translate-term":(lambda h: h.replace(" + var(--b3,0px) * (1 - var(--dvf3))", "", 1), "COMPOSE"),
 "rest-scale":    (lambda h: h.replace("scaleY(var(--self,1))", "scaleY(calc(var(--self,1) * 0.8))", 1),
                   "END"),
 "rect-count":    (lambda h: re.sub(r'(<figure class="dv" data-dv-type="stacked".*?</figure>)',
                                    lambda m: re.sub(r'<rect class="dv-series"[^>]*>(?:<title>.*?</title>)?</rect>\s*',
                                                     "", m.group(1), count=14, flags=re.S),
                                    h, flags=re.S), "RECT-COUNT"),
 # the DEFECT THIS LANE REMOVED, put back: the serial timing the generator emitted until #219.
 "wording-1":     (lambda h: h.replace('style="--b1:68.4px; --self:var(--dvf2)"',
                                       'style="animation-delay:420ms; animation-duration:400ms; '
                                       'animation-timing-function:linear; --b1:68.4px; '
                                       '--self:var(--dvf2)"', 1), "WORDING-1"),
 # the STROKE half of dv-004 on this surface — a boundary that stops being the page colour.
 "stroke-colour": (lambda h: h.replace('stroke="var(--page)" stroke-width="2"',
                                       'stroke="var(--line)" stroke-width="2"', 1), "DV-004-STROKE"),
}

ARMS = {"snippet": MUTATIONS, "proforma": MUTATIONS_PROFORMA}

# ---------------------------------------------------------------- render half
PROBE = r"""
(T) => {
  const fig = document.querySelector('__FIG__');
  const svg = fig.querySelector('svg.dv-svg');
  if (svg.getBoundingClientRect().width < 100) return {error:'wrong svg node'};
  document.getAnimations().forEach(a => { try { a.pause(); a.currentTime = T; } catch(e){} });
  const cols = {};
  for (const r of svg.querySelectorAll('rect.dv-series')) {
    const b = r.getBoundingClientRect();
    const k = r.getAttribute('x');
    (cols[k] = cols[k] || []).push({top:+b.top.toFixed(3), bottom:+b.bottom.toFixed(3),
                                    h:+b.height.toFixed(3), H:+r.getAttribute('height'),
                                    label:r.getAttribute('aria-label')});
  }
  for (const k in cols) cols[k].sort((p,q)=>q.top-p.top);   // bottom-first
  const base = svg.querySelector('line.dv-axis').getBoundingClientRect().top;
  // s218-D5 (2): the letter keys' RENDERED opacity at this frame. Measured, not inferred from
  // the rule — animation-delay + fill-mode `both` is exactly the pair that is easy to get wrong.
  const keys = [...svg.querySelectorAll('__KEY__')]
                 .map(t => ({ch:t.textContent.trim(), o:+(+getComputedStyle(t).opacity).toFixed(3)}));
  // user-unit -> screen scale, so an assertion in SVG units survives a viewBox the page rescales
  // (the pro-forma's fitCharts() rewrites it; JS-off leaves it at the authored aspect).
  const ctm = svg.getScreenCTM();
  return {cols, base:+base.toFixed(3), keys, scale:+(ctm ? ctm.d : 1).toFixed(6),
          dvf:__DVF__.map(n=>getComputedStyle(svg).getPropertyValue('--dvf'+n).trim())};
}
"""

REST = r"""
() => {
  const fig = document.querySelector('__FIG__');
  const svg = fig.querySelector('svg.dv-svg');
  const cols = {};
  for (const r of svg.querySelectorAll('rect.dv-series')) {
    const b = r.getBoundingClientRect();
    (cols[r.getAttribute('x')] = cols[r.getAttribute('x')] || []).push(
      {top:+b.top.toFixed(3), bottom:+b.bottom.toFixed(3), h:+b.height.toFixed(3),
       H:+r.getAttribute('height'), label:r.getAttribute('aria-label')});
  }
  for (const k in cols) cols[k].sort((p,q)=>q.top-p.top);
  const ctm = svg.getScreenCTM();
  return {cols, scale:+(ctm ? ctm.d : 1).toFixed(6)};
}
"""


def stroke_box(cols, scale, SW):
    """DOES the measured box include the 2px separation stroke? MEASURED at rest, never assumed.

    ⚠ #219, DRIVEN AND SURPRISING: on Chromium 151 `getBoundingClientRect()` on these transformed
    SVG rects returns the FILL box — the stroke is NOT in it. Assuming the opposite (the textbook
    reading) put every mid-flight height 0.05 low and opened phantom 0.6–1.25px "gaps" in a stack
    that was in fact perfectly contiguous: a false red that reads exactly like a real defect.
    So the convention is determined from the rest frame — where measured/H is 1.0 if the stroke is
    outside the box and (H+SW)/H if it is inside — and the answer drives the maths. A third answer
    means the probe does not understand what it is measuring, and says so instead of guessing.
    Returns the effective stroke to remove from each measurement."""
    if SW <= 0:
        return 0.0, "no stroke on this surface"
    r = [c["h"] / (c["H"] * scale) for col in cols.values() for c in col]
    fill = all(abs(v - 1.0) < 0.02 for v in r)
    incl = all(abs(v - (c["H"] + SW) / c["H"]) < 0.02
               for col in cols.values() for v, c in zip([x["h"] / (x["H"] * scale) for x in col], col))
    if fill and not incl:
        return 0.0, "engine reports the FILL box — the %.1fpx stroke is outside it" % SW
    if incl and not fill:
        return SW, "engine reports the STROKE box — %.1fpx removed from every measurement" % SW
    return None, ("STROKE-BOX: rest-frame measured/geometry ratios are %s — neither the fill box "
                  "(1.0) nor the stroke box; the probe cannot say what it is measuring"
                  % [round(v, 4) for v in r[:4]])


def degeom(col, SW):
    """Remove a stroke that the engine puts INSIDE the measured box. A scaleY(f) scales the stroke
    with the fill, so such an engine measures f*(H+SW) where the geometry is f*H; recovering it is
    exact, not a fudge. SW=0 is the identity — the path Chromium 151 takes (see stroke_box)."""
    if SW <= 0:
        return col
    out = []
    for c in col:
        g = c["h"] * c["H"] / (c["H"] + SW)
        pad = (c["h"] - g) / 2.0
        d = dict(c)
        d["h"], d["top"], d["bottom"] = g, c["top"] + pad, c["bottom"] - pad
        out.append(d)
    return out


def render_checks(path, P, verbose=True):
    sys.path.insert(0, "/var/tmp/pylibs")
    from playwright.sync_api import sync_playwright
    # s218-D5 (1): the curve maths comes from the FILE ABOUT TO BE RENDERED (the mutant included),
    # so the expectation can never be a stale memory of what the tokens used to say.
    src = open(path, encoding="utf-8").read()
    CURVES = house_curves(src)
    depth = max((len(v) for v in columns(figure_block(src, P) or "")[1].values()), default=3)
    SW = P["stroke"]
    WANT_GAP = MIN_GAP if P["sep"] == "gap" else 0.0     # stroke surfaces are contiguous by design
    probe = PROBE.replace("__FIG__", P["js_fig"]).replace("__KEY__", P["key"]) \
                 .replace("__DVF__", repr(list(range(1, depth + 1))))
    rest = REST.replace("__FIG__", P["js_fig"])
    shell = glob.glob(os.environ.get("DVD16_SHELL",
        "/var/tmp/pw-browsers-*/chromium_headless_shell-*/chrome-linux/headless_shell"))
    F = []
    def say(s):
        if verbose: print("   " + s)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1180, "height": 1400})
        pg.goto("file://" + path)
        pg.wait_for_timeout(400)
        # WHAT IS BEING MEASURED, settled before anything is asserted about it (#219).
        r0 = pg.evaluate(probe, DUR_MS)
        if r0.get("error"):
            return F + ["PROBE: " + r0["error"]]
        SW_EFF, why = stroke_box(r0["cols"], r0.get("scale", 1.0) or 1.0, SW)
        if SW_EFF is None:
            # NAME it and carry on with the fill-box reading rather than returning here: a rest
            # frame that is not at full height is ALSO what a broken chart looks like, and the
            # checks below are the ones that say so. Refusing at the first obstacle would report
            # the measurement problem and hide the defect underneath it.
            F.append(why)
            SW_EFF, why = 0.0, why + " [continuing on the fill-box reading]"
        say("box convention: " + why)
        for frac in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
            r = pg.evaluate(probe, DUR_MS * frac)
            if r.get("error"):
                F.append("PROBE: " + r["error"]); break
            s = r.get("scale", 1.0) or 1.0
            growing = 0
            # ⑦ s218-D5 (2) — NO KEY IS PAINTED WHILE THE STACK IS STILL MOVING. Sampled at every
            #    mid-flight frame, including t=1.00: the fade STARTS at var(--grow-dur), so at the
            #    instant growth lands the keys are still at zero. (KEY-LATE below proves they do
            #    arrive — "always invisible" would satisfy this half alone and is not the fix.)
            lit = [k for k in r.get("keys", []) if k["o"] > 0.02]
            if lit:
                F.append("KEY-EARLY t=%.2f: %d letter key(s) painted before the growth lands "
                         "(e.g. `%s` at opacity %s) — the adrift key s218-D5 (2) retired"
                         % (frac, len(lit), lit[0]["ch"], lit[0]["o"]))
            for x, col in sorted(r["cols"].items(), key=lambda kv: float(kv[0])):
                col = degeom(col, SW_EFF)
                if len(col) < 3:
                    F.append("RENDER-COUNT: column x=%s rendered %d segments" % (x, len(col)))
                    continue
                # ① CONTIGUITY — the boundary must hold its ruled separation at EVERY frame.
                #    On a gap surface that separation is 2px of page; on a stroke surface the
                #    geometry is contiguous and the 2px is painted ON the shared edge.
                for i in range(1, len(col)):
                    gap = col[i-1]["top"] - col[i]["bottom"]
                    if abs(gap - WANT_GAP * s) > 0.6:
                        F.append("CONTIGUITY t=%.2f: x=%s boundary %d/%d measured %.2fpx, "
                                 "expected %.2fpx (>0.6px drift = the stack is gapping "
                                 "or overlapping mid-flight)" % (frac, x, i, i+1, gap, WANT_GAP * s))
                    if frac == 1.0 and gap + EMIT_ULP + 1e-6 < WANT_GAP * s:
                        F.append("DV-004-END t=1.00: x=%s boundary %d/%d is %.2fpx (< %.2f)"
                                 % (x, i, i+1, gap, WANT_GAP * s))
                # ② CONCURRENCY — wording ②, and the discriminator against reversed wording ①
                if 0.0 < frac < 1.0:
                    if all(c["h"] > 0.5 for c in col): growing += 1
                    elif frac >= 0.25:
                        F.append("CONCURRENCY t=%.2f: x=%s has a segment still at zero height — "
                                 "that is the SERIAL look wording ① was reversed away from "
                                 "(%s)" % (frac, x, [c["h"] for c in col]))
                # ③ PER-SEGMENT CURVES, measured off the rendered heights
                if 0.0 < frac < 1.0:
                    for i, c in enumerate(col):
                        fn = CURVES[FIRST_CURVE if i == 0 else
                                    (LAST_CURVE if i == len(col)-1 else "linear")]
                        if fn is None:
                            F.append("CURVE-RENDER t=%.2f: the house curve token for position %d is "
                                     "not declared in the file — nothing to measure against"
                                     % (frac, i+1))
                            continue
                        want = fn(frac)
                        got = c["h"] / (c["H"] * s)
                        if abs(got - want) > 0.04:
                            F.append("CURVE-RENDER t=%.2f: %s grew to %.3f of its height, its ruled "
                                     "curve says %.3f" % (frac, c["label"], got, want))
                # ④ the bottom segment stays welded to the baseline
                if abs(col[0]["bottom"] - r["base"]) > 0.8:
                    F.append("BASELINE t=%.2f: x=%s bottom segment sits %.2fpx off the axis"
                             % (frac, x, col[0]["bottom"] - r["base"]))
                if frac == 0.0 and any(c["h"] > 0.5 for c in col):
                    F.append("START t=0.00: x=%s is not collapsed (%s)" % (x, [c["h"] for c in col]))
                if frac == 1.0:
                    for c in col:
                        if abs(c["h"] - c["H"] * s) > 0.6:
                            F.append("END t=1.00: %s rendered %.2fpx of its %.2fpx height"
                                     % (c["label"], c["h"], c["H"] * s))
            say("t=%.2f  dvf=%s  columns fully-growing: %d  keys lit: %d/%d"
                % (frac, r.get("dvf"), growing, len(lit), len(r.get("keys", []))))

        # ⑧ s218-D5 (2), the OTHER half — the keys DO arrive. Sampled one --ease (160ms) past the
        #    delay, with generous slack: a "fix" that simply never shows the keys is not the ruling.
        if not any(f.startswith("PROBE") for f in F):
            r = pg.evaluate(probe, DUR_MS + 400)
            dark = [k for k in r.get("keys", []) if k["o"] < 0.98]
            if not r.get("keys"):
                F.append("KEY-LATE: no %s found in the stacked figure at all — the "
                         "opacity assertions above were vacuous" % P["key"])
            elif dark:
                F.append("KEY-LATE t=grow+400ms: %d letter key(s) still not painted (e.g. `%s` at "
                         "opacity %s) — the delayed fade never completes"
                         % (len(dark), dark[0]["ch"], dark[0]["o"]))
            else:
                say("t=grow+400ms  all %d letter keys at full opacity on settled segments"
                    % len(r["keys"]))

        # ⑤ REDUCED MOTION and ⑥ JS-OFF (DEF-003) — both must REST ON THE FINAL FRAME.
        #    "Reduced" is not "none": the honest form is the finished chart, rendered immediately.
        for name, ctx in (("REDUCED-MOTION",
                           b.new_context(viewport={"width": 1180, "height": 1400},
                                         reduced_motion="reduce")),
                          ("JS-OFF",
                           b.new_context(viewport={"width": 1180, "height": 1400},
                                         java_script_enabled=False))):
            q = ctx.new_page()
            q.goto("file://" + path)
            q.wait_for_timeout(1200)                       # longer than the 760ms gesture
            r = q.evaluate(rest)
            s2 = r.get("scale", 1.0) or 1.0
            for x, col in sorted(r["cols"].items(), key=lambda kv: float(kv[0])):
                col = degeom(col, SW_EFF)
                for c in col:
                    if abs(c["h"] - c["H"] * s2) > 0.6:
                        F.append("%s: %s rests at %.2fpx of its %.2fpx height — not the final frame"
                                 % (name, c["label"], c["h"], c["H"] * s2))
                for i in range(1, len(col)):
                    gap = col[i-1]["top"] - col[i]["bottom"]
                    if gap + 0.6 < WANT_GAP * s2:
                        F.append("%s: x=%s boundary %d/%d is %.2fpx (< %.2f, dv-004)"
                                 % (name, x, i, i+1, gap, WANT_GAP * s2))
            say("%s: %d rects rest at full height, boundaries >= %.2fpx"
                % (name, sum(len(c) for c in r["cols"].values()), WANT_GAP * s2))
            ctx.close()
        b.close()
    return F

# ---------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--mutate", default=None)
    ap.add_argument("--target", default="snippet", choices=sorted(PROFILES) + ["all"],
                    help="which stacked surface (DV-D16b is forward-binding; `all` runs every one)")
    a = ap.parse_args()
    if not (a.static or a.render): a.static = a.render = True
    bad = 0

    for tname in (sorted(PROFILES) if a.target == "all" else [a.target]):
        P = PROFILES[tname]
        html = open(P["path"], encoding="utf-8").read()
        rel = os.path.relpath(P["path"], ROOT)

        if a.mutate:
            table = ARMS[tname]
            arms = list(table) if a.mutate == "all" else [a.mutate]
            for arm in arms:
                if arm not in table:
                    print("RED-ARM %-15s [%s] ⛔ no such arm on this surface" % (arm, tname))
                    bad += 1; continue
                fn, expect = table[arm]
                mutated = fn(html)
                if mutated == html:
                    print("RED-ARM %-15s [%s] ⛔ the mutation changed NOTHING — the arm is a dangle"
                          % (arm, tname))
                    bad += 1; continue
                fails = static_checks(mutated, P, verbose=False)
                if a.render:
                    tmp = os.path.join(tempfile.mkdtemp(dir="/var/tmp"), "mutant.html")
                    open(tmp, "w", encoding="utf-8").write(mutated)
                    fails += render_checks(tmp, P, verbose=False)
                hit = [f for f in fails if f.startswith(expect)]
                print("RED-ARM %-15s [%-8s] expect %-14s -> %s"
                      % (arm, tname, expect, "RED, by name" if hit else "⛔ STAYED GREEN"))
                for f in fails[:2]: print("        " + f)
                if not hit: bad += 1
            continue

        if a.static:
            print("STATIC (parse) — %s [%s]" % (rel, tname))
            F = static_checks(html, P)
            print("  %s  (%d failures)" % ("GREEN" if not F else "RED", len(F)))
            for f in F: print("   ✗ " + f)
            bad += len(F)
        if a.render:
            print("RENDER (chromium, timeline paused per frame) — %s [%s]" % (rel, tname))
            F = render_checks(P["path"], P)
            print("  %s  (%d failures)" % ("GREEN" if not F else "RED", len(F)))
            for f in F[:12]: print("   ✗ " + f)
            bad += len(F)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
