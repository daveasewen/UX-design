#!/usr/bin/env python3
"""DV-D16 (wording ②) enactment proof — Chart-bar's stacked column.

Two halves, and BOTH are meant to be run:

  --static   parses `knowledge/snippets/Chart-bar.reference.html` and RE-DERIVES every emitted
             `--b*` from the file's own rect `y`/`height` attributes (the ENACTED geometry, DV-D14 —
             never the data labels), then asserts the curve assignment, the registrations and the
             transform composition. Document-vs-document, and it says so.
  --render   drives a real Chromium, PAUSES the shared timeline at sampled frames, and measures the
             rendered boxes. This is the half that can see whether the stack actually stays
             contiguous while it grows, whether all segments are moving AT ONCE (wording ②, not the
             reversed serial wording ①), and whether each segment is really on its own curve.

  --mutate <arm>   applies ONE break to an in-memory/temp copy and expects the named check to FIRE.
                   Arms: b-value · self-swap · curve-drop · translate-term · rect-count
                   (`--mutate all` runs every arm.) A probe that cannot go red proves nothing.

⚠ SCOPE, DECLARED: the render half measures GEOMETRY only, so it does not stand up the HSBC font
farm (_RUNBOOK-render-verify.md § 5) — no assertion here depends on the face. It is not a substitute
for the font-bearing render checks, and it does not clear a "render-verify OWED" note about type.
"""
import argparse, glob, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIP = os.path.join(ROOT, "snippets", "Chart-bar.reference.html")
DUR_MS = 760.0
MIN_GAP = 2.0                     # dv-004 — Dave's ruled >=2px segment boundary

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
CURVES = {"ease-in": _bez(.42, 0, 1, 1), "linear": lambda x: x, "ease-out": _bez(0, 0, .58, 1)}

# ---------------------------------------------------------------- parsing
def figure_block(html):
    m = re.search(r'<figure class="dv dv-animate" data-dv-type="stacked-column".*?</figure>', html, re.S)
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
def static_checks(html, verbose=True):
    F = []                                          # failures, each NAMED
    def say(s):
        if verbose: print("   " + s)
    fig = figure_block(html)
    if not fig:
        return ["MISSING-FIGURE: no figure[data-dv-type=\"stacked-column\"] in the snippet"]
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
            lbl = "x=%s seg%d (%s)" % (x, i+1, attr(t, "aria-label"))
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
            # rest-state boundary, the dv-004 mirror (also proves --b is on the ENACTED geometry)
            if i:
                # SVG y grows DOWNWARD: col[i] sits ABOVE col[i-1], so the boundary is the
                # lower rect's TOP minus the upper rect's bottom edge.
                gap = float(attr(col[i-1], "y")) - (float(attr(col[i], "y")) + float(attr(col[i], "height")))
                if gap + 1e-9 < MIN_GAP:
                    F.append("DV-004-REST: %s boundary is %.2fpx (< %.1f)" % (lbl, gap, MIN_GAP))
    say("--b values re-derived from y/height attributes and matched; --self indices bottom-up OK")

    # -- (b) per-segment curves on ONE shared timeline ------------------------------------------
    m = re.search(r'figure\.dv-animate\[data-dv-type="stacked-column"\]\s*svg\.dv-svg\{([^}]*)\}', html)
    if not m:
        F.append("TIMELINE-RULE: no `figure.dv-animate[data-dv-type=\"stacked-column\"] svg.dv-svg` "
                 "rule — nothing animates the shared progress numbers")
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
                want = "ease-in" if pos == 1 else ("ease-out" if pos == len(parsed) else "linear")
                if curve != want:
                    F.append("CURVE: segment %d of %d is `%s`, DV-D16 rules `%s` "
                             "(first ease-in - intermediates linear - last ease-out)"
                             % (pos, len(parsed), curve, want))
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

    # -- registrations + keyframes, and the transform composition -------------------------------
    for n in range(1, depth + 1):
        if not re.search(r'@property\s+--dvf%d\{[^}]*syntax:"<number>"[^}]*inherits:true[^}]*'
                         r'initial-value:1;[^}]*\}' % n, html):
            F.append("REGISTER: --dvf%d is not registered <number>/inherits:true/initial-value:1 "
                     "(unregistered custom properties do not animate, and the initial value is the "
                     "JS-off / unsupported-@property landing frame)" % n)
        if not re.search(r'@keyframes dvStackF%d\{from\{--dvf%d:0;\} to\{--dvf%d:1;\}\}' % (n, n, n), html):
            F.append("KEYFRAMES: @keyframes dvStackF%d is missing or is not 0 -> 1" % n)
    rm = re.search(r'figure\.dv-animate\[data-dv-type="stacked-column"\]\s*rect\.dv-series'
                   r'\[data-grow="up"\]\{(.*?)\}\s*\n\s*\}', html, re.S)
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
    if not re.search(r'@media \(prefers-reduced-motion:no-preference\)\{[^@]*?figure\.dv-animate'
                     r'\[data-dv-type="stacked-column"\]', html, re.S):
        F.append("REDUCED-MOTION: the stacked float rules are not inside a "
                 "(prefers-reduced-motion:no-preference) block — under `reduce` the transform would "
                 "still apply and the chart could rest off its final frame")
    if not re.search(r'@media \(prefers-reduced-motion: reduce\)\{[^}]*animation-duration:\.01ms !important',
                     html, re.S):
        F.append("REDUCED-MOTION: the global reduce block no longer neutralises animation-duration")

    # -- DEF-003: nothing here may add JS -------------------------------------------------------
    if re.search(r'dvf1|dvStackF|--self', "".join(re.findall(r'<script[^>]*>(.*?)</script>', html, re.S))):
        F.append("DEF-003: the float mechanism leaked into <script> — it must be pure CSS")
    return F

# ---------------------------------------------------------------- mutations
MUTATIONS = {
 "b-value":       (lambda h: h.replace("--b1:42.1px", "--b1:41.1px", 1), "BELOW-VALUE"),
 "self-swap":     (lambda h: h.replace("--b1:42.1px; --b2:73.6px; --self:var(--dvf3)",
                                       "--b1:42.1px; --b2:73.6px; --self:var(--dvf2)", 1), "SELF-INDEX"),
 "curve-drop":    (lambda h: h.replace("dvStackF3 var(--grow-dur) ease-out both",
                                       "dvStackF3 var(--grow-dur) linear both", 1), "CURVE"),
 "translate-term":(lambda h: h.replace(" + var(--b2,0px) * (1 - var(--dvf2))", "", 1), "COMPOSE"),
 # render-only arm: proves the REST probes (end frame, reduced motion, JS-off) can go red at all.
 "rest-scale":    (lambda h: h.replace("scaleY(var(--self,1))", "scaleY(calc(var(--self,1) * 0.8))", 1),
                   "END"),
 "rect-count":    (lambda h: re.sub(r'(<figure class="dv dv-animate" data-dv-type="stacked-column".*?</figure>)',
                                    lambda m: re.sub(r'<rect class="dv-series"[^>]*></rect>\s*', "", m.group(1), count=10),
                                    h, flags=re.S), "RECT-COUNT"),
}

# ---------------------------------------------------------------- render half
PROBE = r"""
(T) => {
  const fig = document.querySelector('figure[data-dv-type="stacked-column"]');
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
  return {cols, base:+base.toFixed(3),
          dvf:[1,2,3].map(n=>getComputedStyle(svg).getPropertyValue('--dvf'+n).trim())};
}
"""

REST = r"""
() => {
  const fig = document.querySelector('figure[data-dv-type="stacked-column"]');
  const svg = fig.querySelector('svg.dv-svg');
  const cols = {};
  for (const r of svg.querySelectorAll('rect.dv-series')) {
    const b = r.getBoundingClientRect();
    (cols[r.getAttribute('x')] = cols[r.getAttribute('x')] || []).push(
      {top:+b.top.toFixed(3), bottom:+b.bottom.toFixed(3), h:+b.height.toFixed(3),
       H:+r.getAttribute('height'), label:r.getAttribute('aria-label')});
  }
  for (const k in cols) cols[k].sort((p,q)=>q.top-p.top);
  return {cols};
}
"""

def render_checks(path, verbose=True):
    sys.path.insert(0, "/var/tmp/pylibs")
    from playwright.sync_api import sync_playwright
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
        for frac in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
            r = pg.evaluate(PROBE, DUR_MS * frac)
            if r.get("error"):
                F.append("PROBE: " + r["error"]); break
            growing = 0
            for x, col in sorted(r["cols"].items(), key=lambda kv: float(kv[0])):
                if len(col) < 3:
                    F.append("RENDER-COUNT: column x=%s rendered %d segments" % (x, len(col)))
                    continue
                # ① CONTIGUITY — the boundary must hold its ruled 2px at EVERY frame
                for i in range(1, len(col)):
                    gap = col[i-1]["top"] - col[i]["bottom"]
                    if abs(gap - MIN_GAP) > 0.6:
                        F.append("CONTIGUITY t=%.2f: x=%s boundary %d/%d measured %.2fpx, "
                                 "expected the ruled %.1fpx (>0.6px drift = the stack is gapping "
                                 "or overlapping mid-flight)" % (frac, x, i, i+1, gap, MIN_GAP))
                    if frac == 1.0 and gap + 1e-6 < MIN_GAP:
                        F.append("DV-004-END t=1.00: x=%s boundary %d/%d is %.2fpx (< %.1f)"
                                 % (x, i, i+1, gap, MIN_GAP))
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
                        want = CURVES["ease-in" if i == 0 else
                                      ("ease-out" if i == len(col)-1 else "linear")](frac)
                        got = c["h"] / c["H"]
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
                        if abs(c["h"] - c["H"]) > 0.6:
                            F.append("END t=1.00: %s rendered %.2fpx of its %.1fpx height"
                                     % (c["label"], c["h"], c["H"]))
            say("t=%.2f  dvf=%s  columns fully-growing: %d" % (frac, r.get("dvf"), growing))

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
            r = q.evaluate(REST) if name == "REDUCED-MOTION" else q.evaluate(REST)
            for x, col in sorted(r["cols"].items(), key=lambda kv: float(kv[0])):
                for c in col:
                    if abs(c["h"] - c["H"]) > 0.6:
                        F.append("%s: %s rests at %.2fpx of its %.1fpx height — not the final frame"
                                 % (name, c["label"], c["h"], c["H"]))
                for i in range(1, len(col)):
                    gap = col[i-1]["top"] - col[i]["bottom"]
                    if gap + 1e-6 < MIN_GAP:
                        F.append("%s: x=%s boundary %d/%d is %.2fpx (< %.1f, dv-004)"
                                 % (name, x, i, i+1, gap, MIN_GAP))
            say("%s: %d rects rest at full height, boundaries >= %.1fpx"
                % (name, sum(len(c) for c in r["cols"].values()), MIN_GAP))
            ctx.close()
        b.close()
    return F

# ---------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--mutate", default=None)
    a = ap.parse_args()
    if not (a.static or a.render): a.static = a.render = True
    html = open(SNIP, encoding="utf-8").read()
    bad = 0

    if a.mutate:
        arms = list(MUTATIONS) if a.mutate == "all" else [a.mutate]
        for arm in arms:
            fn, expect = MUTATIONS[arm]
            mutated = fn(html)
            if mutated == html:
                print("RED-ARM %-15s ⛔ the mutation changed NOTHING — the arm is a dangle" % arm)
                bad += 1; continue
            fails = static_checks(mutated, verbose=False)
            if a.render:
                tmp = os.path.join(tempfile.mkdtemp(dir="/var/tmp"), "mutant.html")
                open(tmp, "w", encoding="utf-8").write(mutated)
                fails += render_checks(tmp, verbose=False)
            hit = [f for f in fails if f.startswith(expect)]
            print("RED-ARM %-15s expect %-12s -> %s" % (arm, expect, "RED, by name" if hit else "⛔ STAYED GREEN"))
            for f in fails[:3]: print("        " + f)
            if not hit: bad += 1
        return sys.exit(1 if bad else 0)

    if a.static:
        print("STATIC (parse) — %s" % os.path.relpath(SNIP, ROOT))
        F = static_checks(html)
        print("  %s  (%d failures)" % ("GREEN" if not F else "RED", len(F)))
        for f in F: print("   ✗ " + f)
        bad += len(F)
    if a.render:
        print("RENDER (chromium, timeline paused per frame)")
        F = render_checks(SNIP)
        print("  %s  (%d failures)" % ("GREEN" if not F else "RED", len(F)))
        for f in F[:12]: print("   ✗ " + f)
        bad += len(F)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
