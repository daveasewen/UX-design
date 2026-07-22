#!/usr/bin/env python3
"""
_validate_partials.py — the re-implementation RATCHET for registered partials (ADR-0013).

Gate the condition, don't patch instances: once a rule is a registered partial
(knowledge/component-types.json $partials), implementing that rule LOCALLY is the
defect class this tier exists to kill (pre-ADR-0013 ground truth: 7 snippets carried
Button's scale-press by copy, 4 pressed with translateY — drifted physics).

RULE — press-physics-shaped CSS (a rule whose selector carries :hover/:active and
whose body sets transform to a scale()/translate()) may live ONLY:
  * inside the source atom's PARTIAL block, or
  * inside a consumer's generated AUTO-PARTIAL block.

SCOPE (ratchet, the radius-gate pattern — census -> advisory -> blocking):
  STRICT (blocking):  registry MEMBERS, on their mapped control selector, outside
                      the marked blocks. transform:none is exempt (guards/overrides).
  ADVISORY (census):  every other press-physics-shaped rule in every snippet —
                      the observed-duplication worklist groups accrete from
                      (ADR-0013 ruling 3: accretion from OBSERVED duplication only).

Writes knowledge/_PARTIALS-GATE.md. Exits non-zero on any STRICT failure.
Selftest: python3 knowledge/_validate_partials.py --selftest (bite test, ADR-0005 §5).
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
REG  = os.path.join(HERE, "component-types.json")
OUT  = os.path.join(HERE, "_PARTIALS-GATE.md")

MARKED = re.compile(
    r'/\* ===== (?:AUTO-)?PARTIAL [\w-]+ START[^\n]*===== \*/.*?/\* ===== (?:AUTO-)?PARTIAL [\w-]+ END ===== \*/',
    re.S)
STYLE  = re.compile(r'<style>(.*?)</style>', re.S)
RULE   = re.compile(r'([^{}]+)\{([^{}]*)\}')
PHYSICS = re.compile(r'transform\s*:\s*[^;}]*(?:scale\(|translate[XY]?\()')

def strip_marked(css):
    return MARKED.sub("", css)

def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)

def physics_rules(css):
    """[(selector, body)] of press-physics-shaped rules (outside marked blocks;
    caller strips). Detector: :hover/:active selector + scale()/translate() body."""
    out = []
    for sel, body in RULE.findall(strip_comments(strip_marked(css))):
        s = sel.strip()
        if "@" in s.split("\n")[-1][:1]:
            continue
        if (":active" in s or ":hover" in s) and PHYSICS.search(body):
            out.append((s.replace("\n", " ").strip(), body.strip()))
    return out

def sel_hits(selector, control_sel):
    """Does this rule's selector target the member's mapped control?"""
    return re.search(re.escape(control_sel) + r'(?![\w-])', selector) is not None

def member_map(reg):
    """{snippet-name: [(group, partial, control_selector)]} for every registry member."""
    out = {}
    for gname, g in reg.get("component-type", {}).items():
        if gname.startswith("$"):
            continue
        for pname, partial in (g.get("$partials") or {}).items():
            root = partial["rootSelector"]
            for mname, mconf in (g.get("$members") or {}).items():
                sel = root if mconf.get("role") == "source" else mconf.get("selector", root)
                out.setdefault(mname, []).append((gname, pname, sel))
    return out

def scan(reg):
    strict, census = [], []
    members = member_map(reg)
    for path in sorted(glob.glob(os.path.join(SNIP, "*.reference.html"))):
        name = os.path.basename(path).replace(".reference.html", "")
        m = STYLE.search(open(path).read())
        if not m:
            continue
        rules = physics_rules(m.group(1))
        if not rules:
            continue
        mapped = members.get(name, [])
        for sel, body in rules:
            hit = next(((g, p, cs) for g, p, cs in mapped if sel_hits(sel, cs)), None)
            if hit:
                strict.append((name, sel, f"{hit[0]}/{hit[1]}"))
            else:
                census.append((name, sel))
    return strict, census

def selftest():
    fails = []
    # 1. a local physics rule on a mapped selector = strict-shaped detection
    css = ".btn:active{transform:scale(.95);}"
    if not physics_rules(css):
        fails.append("local scale press NOT detected (gate has no teeth)")
    if not physics_rules(".nav button:active{transform:translateY(1px);}"):
        fails.append("translateY press NOT detected")
    # 2. transform:none (guards) must pass
    if physics_rules(".btn:hover{transform:none;} .btn:disabled:hover{transform:none; filter:none;}"):
        fails.append("transform:none guard flagged (must pass)")
    # 3. content inside marked blocks is exempt
    marked = ("/* ===== AUTO-PARTIAL p START (g) ===== */\n"
              ".btn:active{transform:scale(.95);}\n"
              "/* ===== AUTO-PARTIAL p END ===== */")
    if physics_rules(marked):
        fails.append("physics inside AUTO-PARTIAL markers flagged (must be exempt)")
    marked_src = marked.replace("AUTO-PARTIAL", "PARTIAL")
    if physics_rules(marked_src):
        fails.append("physics inside source PARTIAL markers flagged (must be exempt)")
    # 4. non-:active/:hover transforms (checked dots, keyframes) must pass
    if physics_rules('[aria-checked="true"] .dot{transform:scale(1);} to{transform:rotate(360deg);}'):
        fails.append("non-interactive transform flagged (must pass)")
    # 5. selector mapping: .btn does not hit .btn-x; compound selectors hit
    if sel_hits(".btn-x:active", ".btn"):
        fails.append(".btn-x wrongly treated as the mapped .btn control")
    if not sel_hits(".nav button:active", ".nav button"):
        fails.append("compound mapped selector not matched")
    # 6. comment prose never counts (the ds-008 lesson, applied here from birth)
    if physics_rules("/* .btn:active{transform:scale(.9);} in prose */ .x{color:red}"):
        fails.append("comment prose flagged (comments must be stripped)")
    return fails

def main():
    if "--selftest" in sys.argv:
        f = selftest()
        if f:
            print("_validate_partials SELFTEST FAIL:"); [print("  X " + x) for x in f]
            sys.exit(1)
        print("_validate_partials selftest OK")
        return

    reg = json.load(open(REG))
    strict, census = scan(reg)

    lines = ["# _PARTIALS-GATE — registered partials may not be re-implemented locally (ADR-0013)",
             "",
             "*Generated by `_validate_partials.py`. Press-physics-shaped CSS (:hover/:active +",
             "transform scale()/translate()) must come from the partial: the atom's PARTIAL block or a",
             "generated AUTO-PARTIAL block. STRICT = registry members on their mapped control selector",
             "(blocking). CENSUS = observed duplication elsewhere — the accretion worklist, not failures.*",
             ""]
    if strict:
        lines.append(f"## ❌ STRICT failures ({len(strict)})\n")
        lines += [f"- `{n}` → `{s}` re-implements `{p}` locally" for n, s, p in strict]
    else:
        lines.append("## ✅ STRICT clean — no member re-implements a registered partial")
    lines.append("")
    if census:
        lines.append(f"## ⚠ CENSUS — press-physics outside the registry ({len(census)} rule(s))\n")
        lines.append("*Candidates for future group membership (accrete from OBSERVED duplication —")
        lines.append("ADR-0013 ruling 3). Joining = markers + vars + manifest binds + registry entry.*\n")
        lines += [f"- `{n}` → `{s}`" for n, s in census]
    else:
        lines.append("## ✅ census empty")
    open(OUT, "w").write("\n".join(lines) + "\n")

    print(f"_validate_partials: {len(strict)} strict fail(s), {len(census)} census rule(s) -> _PARTIALS-GATE.md")
    if strict:
        [print(f"  X {n}: {s} re-implements {p}") for n, s, p in strict]
        sys.exit(1)

if __name__ == "__main__":
    main()
