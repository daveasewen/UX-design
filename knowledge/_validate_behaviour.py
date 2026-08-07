#!/usr/bin/env python3
"""Behaviour-contract gate (ADR-0015) — Dave's "light/fast/responsive" made EXECUTABLE.

The dataviz behaviour partial (knowledge/canon/dv-behaviour.js, injected into registered
chart snippets by gen_component_partials.py) carries a GATED performance contract, not an
aspirational one. This gate checks every behaviour SOURCE registered in
knowledge/component-types.json ($behaviour blocks), plus its member snippets:

  BLOCKING — on the source file:
    size        ≤ 16 KB raw (ADR-0015 §4; observed proforma baseline 9.9 KB for the whole
                kit — the cap is headroom, not a target)
    banned      setInterval (polling) · network (fetch / XMLHttpRequest / sendBeacon /
                WebSocket / EventSource) · JS scale-physics (DEF-003 boundary: no
                .style.transform, no transform:scale, no --hs/--ps writes — SVG attribute
                translate for data-driven geometry is explicitly allowed)
    resize      EXACTLY ONE window resize listener, rAF-debounced (requestAnimationFrame +
                cancelAnimationFrame both present)
  BLOCKING — on each member snippet:
    no external <script src> (snippets stay self-contained single-file artefacts)

Sync between source and the injected AUTO-BEHAVIOUR blocks is gen_component_partials.py
--check's job (wired separately in _build_all) — this gate owns the CONTRACT on the source.

Usage:  python3 knowledge/_validate_behaviour.py             # the gate
        python3 knowledge/_validate_behaviour.py --selftest  # bite-test (ADR-0005 §5)
Writes _BEHAVIOUR-GATE.md; exits non-zero on any blocking failure."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "component-types.json")
REPORT = os.path.join(HERE, "_BEHAVIOUR-GATE.md")
MAX_BYTES = 16 * 1024
# PAGE budget across ALL of a group's sources — added 2026-07-26 when the legend model was split
# into a second source (dv-legend.js). Dave's ruling on the cap fork was "split AND re-scope the
# gate", precisely so the 16KB stayed a PAGE constraint instead of silently becoming a per-file
# one that any future split could route around. Per-source cap = legibility; page sum = weight.
PAGE_BYTES = 34 * 1024  # ⚠ RE-DIALLED 32→34KB by DAVE, #96 2026-08-05: the 32KB cap predates the
# 8 wave-2 members; his "extend fitOne() now" (#96-D1 ⑥) collided with it at 32,871 after the
# addition was shaved twice. His pick from three options (re-dial / marked waiver / park), receipted
# notes/_MEMENTO-DECISIONS.md § ★ #96. The PAGE-not-per-file scope is UNCHANGED (his 07-26 ruling).

BANNED = [
    (re.compile(r'\bsetInterval\s*\('), "setInterval (polling)"),
    (re.compile(r'\bfetch\s*\('), "fetch (network)"),
    (re.compile(r'\bXMLHttpRequest\b'), "XMLHttpRequest (network)"),
    (re.compile(r'\bsendBeacon\b'), "sendBeacon (network)"),
    (re.compile(r'\bWebSocket\s*\('), "WebSocket (network)"),
    (re.compile(r'\bEventSource\s*\('), "EventSource (network)"),
    (re.compile(r'\.style\.transform\b'), "JS style.transform (DEF-003 — scale-physics boundary)"),
    (re.compile(r'transform\s*:\s*scale'), "transform:scale assignment (DEF-003)"),
    (re.compile(r'--hs\b|--ps\b'), "--hs/--ps write (DEF-003 press-physics vars)"),
]
RESIZE_RE = re.compile(r'''addEventListener\(\s*['"]resize['"]''')
EXT_SRC_RE = re.compile(r'<script\b[^>]*\bsrc\s*=', re.I)


def check_source(js, label):
    """PER-SOURCE checks: size + banned patterns. Anything that is a PAGE invariant (the byte
    budget in aggregate, the single resize listener) belongs in check_group — a source is not
    the unit a browser loads, a member page is."""
    fails = []
    n = len(js.encode("utf-8"))
    if n > MAX_BYTES:
        fails.append(f"{label}: {n} bytes > {MAX_BYTES} (ADR-0015 size gate)")
    for rx, why in BANNED:
        if rx.search(js):
            fails.append(f"{label}: banned pattern — {why}")
    return fails, n


def check_group(sources, label):
    """PAGE-LEVEL checks across every source a member page loads together.

    Both of these were per-SOURCE until 2026-07-26 and were wrong the moment a group carried
    two sources: the sum was unpoliced (two 16KB files pass a 16KB cap), and the "exactly one
    resize listener" rule failed a second source for having zero — even though zero is correct
    for a source with nothing to reflow. The invariant was always about the PAGE."""
    fails = []
    total = sum(len(js.encode("utf-8")) for js in sources)
    if total > PAGE_BYTES:
        fails.append(f"{label}: {total} bytes across {len(sources)} source(s) > {PAGE_BYTES} "
                     f"(ADR-0015 page budget — splitting a source does not buy headroom)")
    js = "\n".join(sources)
    r = len(RESIZE_RE.findall(js))
    if r != 1:
        fails.append(f"{label}: {r} window resize listeners across the group — exactly ONE, rAF-debounced (ADR-0015)")
    if r and ("requestAnimationFrame" not in js or "cancelAnimationFrame" not in js):
        fails.append(f"{label}: resize listener is not rAF-debounced (requestAnimationFrame + cancelAnimationFrame expected)")
    return fails, total


def check_member(html, label):
    return [f"{label}: external <script src> — snippets stay self-contained (ADR-0015)"] \
        if EXT_SRC_RE.search(html) else []


def run():
    reg = json.load(open(REG))
    fails, rows, totals = [], [], {}
    for gname, g in reg.get("component-type", {}).items():
        if gname.startswith("$") or not isinstance(g, dict):
            continue
        behs = g.get("$behaviour") or {}
        if not behs:
            continue
        members = [m for m in (g.get("$members") or {}) if not m.startswith("$")]
        srcs = []
        for bname, beh in behs.items():
            sp = os.path.join(HERE, beh["source"])
            if not os.path.exists(sp):
                fails.append(f"{gname}/{bname}: source knowledge/{beh['source']} missing")
                continue
            js = open(sp).read()
            srcs.append(js)
            f, n = check_source(js, f"{gname}/{bname} ({beh['source']})")
            fails += f
            rows.append((f"{gname}/{bname}", beh["source"], n, len(members)))
        if srcs:
            f, total = check_group(srcs, f"{gname} (page budget)")
            fails += f
            totals[gname] = (total, len(srcs))
        for m in members:
            mp = os.path.join(HERE, "snippets", m + ".reference.html")
            if os.path.exists(mp):
                fails += check_member(open(mp).read(), f"{gname}: {m}")
    return fails, rows, totals


def write_report(fails, rows, totals):
    L = ["# Behaviour-contract gate (ADR-0015)", "",
         "Per source ≤16KB (legibility) · per group ≤32KB (page weight) · no polling/network · "
         "ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.", ""]
    for name, src, n, nm in rows:
        L.append(f"- **{name}** — `knowledge/{src}` · {n} bytes ({n / 1024:.1f} KB of 16 KB) · {nm} member(s)")
    L.append("")
    for gname, (total, k) in sorted(totals.items()):
        pct = 100 * total / PAGE_BYTES
        L.append(f"- **{gname} — page budget:** {total} bytes ({total / 1024:.1f} KB of 32 KB, "
                 f"{pct:.0f}%) across {k} source(s)")
    L.append("")
    if fails:
        L.append("## ✗ FAILURES")
        L += [f"- {f}" for f in fails]
    else:
        L.append("## ✓ PASS — every behaviour source honours the contract.")
    open(REPORT, "w").write("\n".join(L) + "\n")


def selftest():
    fails = []
    ok_src = ("(function(){var r;window.addEventListener('resize',function(){"
              "cancelAnimationFrame(r);r=requestAnimationFrame(function(){});});}());")
    f, _ = check_source(ok_src, "T")
    if f:
        fails.append("clean source failed: %s" % "; ".join(f))
    if not check_source(ok_src + "setInterval(x,50);", "T")[0]:
        fails.append("setInterval not caught")
    if not check_source(ok_src + "fetch('/x');", "T")[0]:
        fails.append("fetch not caught")
    if not check_source(ok_src + "el.style.transform='scale(2)';", "T")[0]:
        fails.append("style.transform not caught")
    big = ok_src + "/*" + "x" * MAX_BYTES + "*/"
    if not any("size gate" in x for x in check_source(big, "T")[0]):
        fails.append("oversize source not caught")
    # --- group-level bites (added 2026-07-26 with the page-budget re-scope) ---
    if check_group([ok_src], "T")[0]:
        fails.append("clean single-source group failed")
    if check_group([ok_src, "var x=1;"], "T")[0]:
        fails.append("two-source group wrongly failed — a second source may legitimately carry "
                     "zero resize listeners; the invariant is ONE per group")
    if not any("resize" in x for x in check_group([ok_src, ok_src], "T")[0]):
        fails.append("two resize listeners across a group not caught")
    if not any("resize" in x for x in check_group(["var x=1;"], "T")[0]):
        fails.append("zero resize listeners across a group not caught (fit must respond to resize)")
    # sources that EACH pass the 16KB per-source cap but together blow the 34KB page budget
    # (PAGE_BYTES re-dialled 32->34KB by Dave, #96 2026-08-05) — the exact evasion the
    # re-scope exists to close. Two max-size pads (2*16KB=32KB) no longer exceed 34KB on
    # their own, so the bite needs a third pad to still exercise the invariant post re-dial.
    pad = "var x=1;/*" + "y" * (MAX_BYTES - 20) + "*/"
    if check_source(pad, "T")[0]:
        fails.append("page-budget bite is malformed — each pad must pass the per-source cap")
    if not any("page budget" in x for x in check_group([ok_src, pad, pad, pad], "T")[0]):
        fails.append("page budget not caught — splitting a source must not buy headroom")
    if not check_member('<script src="https://cdn.example/x.js"></script>', "T"):
        fails.append("external script src not caught")
    if check_member('<script>var a=1;</script>', "T"):
        fails.append("inline script wrongly flagged")
    live, _, _ = run()
    if live:
        fails.append("LIVE registry failing: %s" % "; ".join(live))
    return fails


def main():
    if "--selftest" in sys.argv:
        f = selftest()
        if f:
            print("_validate_behaviour SELFTEST FAIL:"); [print("  X " + x) for x in f]
            sys.exit(1)
        print("_validate_behaviour selftest OK")
        return
    fails, rows, totals = run()
    write_report(fails, rows, totals)
    if fails:
        print("Behaviour-contract gate FAILED:"); [print("  X " + f) for f in fails]
        sys.exit(1)
    for name, src, n, nm in rows:
        print(f"  [PASS] {name} — {n} bytes ({n / 1024:.1f} KB of 16), {nm} member(s)")
    for gname, (total, k) in sorted(totals.items()):
        print(f"  [PASS] {gname} page budget — {total} bytes ({total / 1024:.1f} KB of 32) across {k} source(s)")
    print("Behaviour-contract gate OK — see knowledge/_BEHAVIOUR-GATE.md")


if __name__ == "__main__":
    main()
