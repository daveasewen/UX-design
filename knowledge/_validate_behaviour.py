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
    fails = []
    n = len(js.encode("utf-8"))
    if n > MAX_BYTES:
        fails.append(f"{label}: {n} bytes > {MAX_BYTES} (ADR-0015 size gate)")
    for rx, why in BANNED:
        if rx.search(js):
            fails.append(f"{label}: banned pattern — {why}")
    r = len(RESIZE_RE.findall(js))
    if r != 1:
        fails.append(f"{label}: {r} window resize listeners — exactly ONE, rAF-debounced (ADR-0015)")
    if r and ("requestAnimationFrame" not in js or "cancelAnimationFrame" not in js):
        fails.append(f"{label}: resize listener is not rAF-debounced (requestAnimationFrame + cancelAnimationFrame expected)")
    return fails, n


def check_member(html, label):
    return [f"{label}: external <script src> — snippets stay self-contained (ADR-0015)"] \
        if EXT_SRC_RE.search(html) else []


def run():
    reg = json.load(open(REG))
    fails, rows = [], []
    for gname, g in reg.get("component-type", {}).items():
        if gname.startswith("$") or not isinstance(g, dict):
            continue
        behs = g.get("$behaviour") or {}
        if not behs:
            continue
        members = [m for m in (g.get("$members") or {}) if not m.startswith("$")]
        for bname, beh in behs.items():
            sp = os.path.join(HERE, beh["source"])
            if not os.path.exists(sp):
                fails.append(f"{gname}/{bname}: source knowledge/{beh['source']} missing")
                continue
            f, n = check_source(open(sp).read(), f"{gname}/{bname} ({beh['source']})")
            fails += f
            rows.append((f"{gname}/{bname}", beh["source"], n, len(members)))
        for m in members:
            mp = os.path.join(HERE, "snippets", m + ".reference.html")
            if os.path.exists(mp):
                fails += check_member(open(mp).read(), f"{gname}: {m}")
    return fails, rows


def write_report(fails, rows):
    L = ["# Behaviour-contract gate (ADR-0015)", "",
         "Source ≤16KB · no polling/network · single rAF-debounced resize · DEF-003 boundary · members carry no external script src.", ""]
    for name, src, n, nm in rows:
        L.append(f"- **{name}** — `knowledge/{src}` · {n} bytes ({n / 1024:.1f} KB of 16 KB) · {nm} member(s)")
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
    if not check_source(ok_src + "window.addEventListener('resize',f);", "T")[0]:
        fails.append("second resize listener not caught")
    if not check_source("var x=1;", "T")[0]:
        fails.append("zero resize listeners not caught (fit must respond to resize)")
    big = ok_src + "/*" + "x" * MAX_BYTES + "*/"
    if not any("size gate" in x for x in check_source(big, "T")[0]):
        fails.append("oversize source not caught")
    if not check_member('<script src="https://cdn.example/x.js"></script>', "T"):
        fails.append("external script src not caught")
    if check_member('<script>var a=1;</script>', "T"):
        fails.append("inline script wrongly flagged")
    live, _ = run()
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
    fails, rows = run()
    write_report(fails, rows)
    if fails:
        print("Behaviour-contract gate FAILED:"); [print("  X " + f) for f in fails]
        sys.exit(1)
    for name, src, n, nm in rows:
        print(f"  [PASS] {name} — {n} bytes ({n / 1024:.1f} KB of 16), {nm} member(s)")
    print("Behaviour-contract gate OK — see knowledge/_BEHAVIOUR-GATE.md")


if __name__ == "__main__":
    main()
