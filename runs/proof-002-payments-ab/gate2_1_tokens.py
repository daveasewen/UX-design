#!/usr/bin/env python3
"""
gate2_1_tokens.py — brand-token-fidelity gate ("gate 2.1").

Gate 2 asks "is the screen internally sound?" Gate 2.1 asks the canon question
gate 2 is blind to: "does the screen use the design system's actual token VALUES,
or just approximate the brand?" This is the check that separates a canon-faithful
composer from a commodity generator that got the vibe but not the tokens.

It loads the real palette from knowledge/tokens and DERIVES the semantic anchors
(success, primary) from semantic-colour.json — nothing hand-coded — then checks a
screen's declared `styles`.

  BLOCK: positive/success colour must be the canon success token (not a generic
         green); primary colour must be the canon red; corners square.
  WARN:  off-palette colour drift; ALL-CAPS labels (HSBC type is sentence case).

Usage:  python3 gate2_1_tokens.py <screen.json>
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.abspath(os.path.join(HERE, "..", "..", "knowledge", "tokens"))

def norm(h): return h.strip().upper()

def walk(node, path, out):
    if isinstance(node, dict):
        v = node.get("$value")
        if isinstance(v, str) and v.startswith("#"):
            out.append((path, norm(v)))
        for k, val in node.items():
            if k.startswith("$"):
                continue
            walk(val, f"{path}/{k}".strip("/"), out)

def load_canon():
    items = []
    for fn in ("semantic-colour.json", "colour.json"):
        p = os.path.join(TOK, fn)
        if os.path.exists(p):
            walk(json.load(open(p, encoding="utf-8")), "", items)
    allowed = {v for _, v in items}
    positive = {v for pth, v in items if "success" in pth.lower()}
    primary = {v for pth, v in items if pth.lower().startswith("primary/background/default")}
    return allowed, positive, primary

findings = []
def rec(cid, sev, ok, msg): findings.append((cid, sev, ok, msg))

def run(screen, allowed, positive, primary):
    st = screen.get("styles", {})

    # TOKEN-1 — positive/success must be a canon success token
    pos = norm(st["positive_color"]) if st.get("positive_color") else None
    cov = screen.get("coverage_banner", {})
    cov_text = norm(cov["text_color"]) if cov.get("text_color") else None
    bad = sorted({c for c in (pos, cov_text) if c and c not in positive})
    if bad:
        rec("TOKEN-1", "BLOCK", False,
            f"positive/success rendered in {', '.join(bad)} — not a canon success token "
            f"(expected {sorted(positive)}).")
    else:
        rec("TOKEN-1", "BLOCK", True, f"positive/success uses the canon success token {sorted(positive)}.")

    # TOKEN-2 — primary must be the canon brand red
    prim = norm(st["primary_color"]) if st.get("primary_color") else None
    if prim and prim not in primary:
        rec("TOKEN-2", "BLOCK", False, f"primary colour {prim} is not canon ({sorted(primary)}).")
    else:
        rec("TOKEN-2", "BLOCK", True,
            "primary colour is the canon brand red." if prim else "no primary colour declared.")

    # TOKEN-3 — square corners (angular brand)
    br = st.get("border_radius_px")
    if br not in (0, None):
        rec("TOKEN-3", "BLOCK", False, f"corners not square (border-radius {br}px); HSBC is angular (0).")
    else:
        rec("TOKEN-3", "BLOCK", True, "square corners (angular brand respected).")

    # TOKEN-4 — off-canon palette drift (advisory)
    used = [norm(c) for c in st.get("palette_used", [])]
    off = [c for c in used if c not in allowed]
    if off:
        rec("TOKEN-4", "WARN", False, f"{len(off)}/{len(used)} colours are off-canon: {', '.join(off)}")
    else:
        rec("TOKEN-4", "WARN", True, "every colour is a canon token value.")

    # TYPE-1 — sentence case (advisory)
    caps = screen.get("labels_uppercase", [])
    rec("TYPE-1", "WARN", not caps,
        f"{len(caps)} ALL-CAPS labels (HSBC type is sentence case)." if caps else "sentence-case labels.")

def main():
    if len(sys.argv) < 2:
        print("usage: gate2_1_tokens.py <screen.json>"); sys.exit(2)
    screen = json.load(open(sys.argv[1], encoding="utf-8"))
    allowed, positive, primary = load_canon()
    if not positive or not primary:
        print("could not load canon anchors from", TOK); sys.exit(2)
    run(screen, allowed, positive, primary)

    blocks = [f for f in findings if f[1] == "BLOCK"]
    warns = [f for f in findings if f[1] == "WARN"]
    bfail = [f for f in blocks if not f[2]]
    wfail = [f for f in warns if not f[2]]
    out = ["# Gate 2.1 — brand-token fidelity",
           f"*Screen: {screen.get('screen')}*\n",
           f"**Verdict: {'🔴 FAIL' if bfail else '✅ PASS'}** — {len(bfail)}/{len(blocks)} blocking, "
           f"{len(wfail)}/{len(warns)} advisory.\n", "## Blocking"]
    for c, s, ok, m in blocks: out.append(f"- {'✅' if ok else '🔴'} **{c}** — {m}")
    out.append("\n## Advisory")
    for c, s, ok, m in warns: out.append(f"- {'✅' if ok else '🟡'} **{c}** — {m}")
    print("\n".join(out))
    sys.exit(1 if bfail else 0)

if __name__ == "__main__":
    main()
