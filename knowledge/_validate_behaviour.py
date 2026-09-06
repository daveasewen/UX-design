#!/usr/bin/env python3
"""Behaviour-contract gate (ADR-0015) — Dave's "light/fast/responsive" made EXECUTABLE.

The dataviz behaviour partial (knowledge/canon/dv-behaviour.js, injected into registered
chart snippets by gen_component_partials.py) carries a GATED performance contract, not an
aspirational one. This gate checks every behaviour SOURCE registered in
knowledge/component-types.json ($behaviour blocks), plus its member snippets:

  BLOCKING — on the source file:
    size        ≤ 16 KB of CODE-ONLY bytes (ADR-0015 §4 + Amendment 3, Dave #250 2026-09-06,
                option (e)): comments and blank lines are stripped AT MEASURE TIME (the source
                files are never modified). The cap is a COMPLEXITY forcing function — Amendment
                1's own words — and a comment is not complexity, so the unit is the code. Both
                raw and code-only bytes are reported so the delta stays visible. The caps did
                NOT move: 16 KB per source, 34 KB per page.
  BLOCKING — on the group:
    page        ≤ 34 KB of code-only bytes summed PER MEMBER PAGE from each member's `consumes`
                declaration (ADR-0015 Amendment 2 + Amendment 3). The worst member page is the
                group's figure — before #250 this summed every source in the registry, which is
                a registry sum, not a page.
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
        python3 knowledge/_validate_behaviour.py --mutate code-pad      # +4000 B code   → RED
        python3 knowledge/_validate_behaviour.py --mutate comment-pad   # +4000 B comment→ GREEN
        python3 knowledge/_validate_behaviour.py --mutate string-slash  # // in a string → code
Writes _BEHAVIOUR-GATE.md; exits non-zero on any blocking failure."""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "component-types.json")
REPORT = os.path.join(HERE, "_BEHAVIOUR-GATE.md")
MAX_BYTES = 16 * 1024  # per SOURCE, code-only (ADR-0015 §4 + A3). UNMOVED at #250 — Dave's option
# (e) changed the UNIT, not the value: "the cap is a complexity forcing function" (A1's own words),
# comments are not complexity, so the measured thing is the code. A moved cap would have been the
# re-dial he declined; a re-measured cap is the same cap asked the question it was written to ask.
# PAGE budget across ALL of a group's sources — added 2026-07-26 when the legend model was split
# into a second source (dv-legend.js). Dave's ruling on the cap fork was "split AND re-scope the
# gate", precisely so the 16KB stayed a PAGE constraint instead of silently becoming a per-file
# one that any future split could route around. Per-source cap = legibility; page sum = weight.
PAGE_BYTES = 34 * 1024  # ⚠ RE-DIALLED 32→34KB by DAVE, #96 2026-08-05: the 32KB cap predates the
# 8 wave-2 members; his "extend fitOne() now" (#96-D1 ⑥) collided with it at 32,871 after the
# addition was shaved twice. His pick from three options (re-dial / marked waiver / park), receipted
# notes/_MEMENTO-DECISIONS.md § ★ #96. The PAGE-not-per-file scope is UNCHANGED (his 07-26 ruling).
# ⚠ UNMOVED at #250 2026-09-06 (Dave, option (e), ADR-0015 Amendment 3). What changed is the unit
# (code-only bytes) and the summation (per member page via `consumes`, not per registry group).

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


# --- CODE-ONLY MEASUREMENT (ADR-0015 Amendment 3, Dave #250 2026-09-06, option (e)) ------------
# Identifiers/keywords after which a `/` opens a REGEX literal rather than a division. Without
# this list `return /x/.test(s)` would be read as division and the rest of the file mis-scanned.
_KW_BEFORE_REGEX = {
    "return", "typeof", "case", "in", "of", "new", "delete", "void", "do", "else", "yield",
    "await", "instanceof", "throw",
}


def _regex_can_start(prev, prev_word):
    """Standard previous-significant-token heuristic: a `/` after a value (identifier, number,
    `)`, `]`) is division; anywhere else it opens a regex literal."""
    if prev == "":
        return True
    if prev_word and prev_word in _KW_BEFORE_REGEX:
        return True
    if prev.isalnum() or prev in "_$)]":
        return False
    return True


def code_only(js):
    """Return `js` with `//` line comments, `/* */` block comments and blank lines removed.

    ⛔ MEASURE TIME ONLY — this never writes anything; the canon sources keep every provenance
    byte they carry. It is a hand-rolled scanner, NOT a regex, precisely so that a `//` inside a
    string ("http://x") or inside a regex literal (/a\\/\\/b/) is never mistaken for a comment.

    LIMITATION, declared and bitten (`--mutate string-slash`, `--mutate regex-slash`): regex-vs-
    division is a heuristic. A `/` following an identifier is read as division, so a regex opened
    immediately after an unlisted keyword-like token (see _KW_BEFORE_REGEX) would be mis-scanned.
    Every construct in the live canon sources is covered; the failure mode is over-counting a
    stray tail as code, i.e. it errs toward a LARGER figure, never a smaller one."""
    out = []
    i, n = 0, len(js)
    prev, prev_word = "", ""
    while i < n:
        c = js[i]
        nxt = js[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "/":                       # line comment — drop to EOL
            while i < n and js[i] != "\n":
                i += 1
            continue
        if c == "/" and nxt == "*":                       # block comment — drop to */
            i += 2
            while i < n and not (js[i] == "*" and i + 1 < n and js[i + 1] == "/"):
                i += 1
            i += 2
            continue
        if c in "'\"`":                                   # string / template literal — verbatim
            q = c
            out.append(c)
            i += 1
            while i < n:
                if js[i] == "\\":
                    out.append(js[i:i + 2]); i += 2; continue
                out.append(js[i])
                if js[i] == q:
                    i += 1; break
                i += 1
            prev, prev_word = q, ""
            continue
        if c == "/" and _regex_can_start(prev, prev_word):  # regex literal — verbatim
            out.append(c)
            i += 1
            in_class = False
            while i < n:
                ch = js[i]
                if ch == "\\":
                    out.append(js[i:i + 2]); i += 2; continue
                out.append(ch); i += 1
                if ch == "[":
                    in_class = True
                elif ch == "]":
                    in_class = False
                elif ch == "\n" or (ch == "/" and not in_class):
                    break
            prev, prev_word = "/", ""
            continue
        out.append(c)
        if not c.isspace():
            prev = c
            prev_word = (prev_word + c) if (c.isalnum() or c in "_$") else ""
        i += 1
    return "\n".join(ln for ln in "".join(out).split("\n") if ln.strip())


def measure(js):
    """(raw bytes, code-only bytes) for one source."""
    return len(js.encode("utf-8")), len(code_only(js).encode("utf-8"))


def CODE_PAD(n):
    """>= n bytes of REAL executable code (no comments) — the padding every size bite needs now
    that the unit is code-only. A comment pad would leave the bite green and toothless."""
    unit = "zz+=1;"
    return "var zz=0;" + unit * (max(0, n - 9) // len(unit) + 1)


def COMMENT_PAD(n):
    """>= n bytes of pure block comment — the control for CODE_PAD."""
    return "\n/*" + "c" * max(1, n - 4) + "*/"


def check_source(js, label):
    """PER-SOURCE checks: size + banned patterns. Anything that is a PAGE invariant (the byte
    budget in aggregate, the single resize listener) belongs in check_group — a source is not
    the unit a browser loads, a member page is.

    Size is measured in CODE-ONLY bytes since #250 (ADR-0015 A3). Banned patterns are still
    matched against the RAW text: a banned call commented out is not a violation, but neither is
    it worth the false-negative risk of scanning a stripped copy — the raw scan is the strict
    reading and it is the one that was already in force."""
    fails = []
    n, code = measure(js)
    if code > MAX_BYTES:
        fails.append(f"{label}: {code} code-only bytes ({n} raw) > {MAX_BYTES} (ADR-0015 size gate)")
    for rx, why in BANNED:
        if rx.search(js):
            fails.append(f"{label}: banned pattern — {why}")
    return fails, n, code


def check_group(sources, label, names=None, consumes=None):
    """PAGE-LEVEL checks across every source a member page loads together.

    Both of these were per-SOURCE until 2026-07-26 and were wrong the moment a group carried
    two sources: the sum was unpoliced (two 16KB files pass a 16KB cap), and the "exactly one
    resize listener" rule failed a second source for having zero — even though zero is correct
    for a source with nothing to reflow. The invariant was always about the PAGE.

    #250 (ADR-0015 A3) closes the second half of that same defect. The budget's name said PAGE
    while the code summed the whole REGISTRY, so a member that declares
    `consumes: ["dv-behaviour"]` was charged for dv-legend and dv-donut-sweep it never loads.
    Amendment 2 added `consumes` and asserted "budgets untouched · _validate_behaviour.py
    unmodified" — that sentence is the seam, and this is where it is sewn. The group's figure is
    now the WORST member page, i.e. the heaviest thing a browser actually loads.

    `names`/`consumes` are optional so the unit bites can still hand in bare source lists; with
    them absent the legacy whole-group sum is used and reported as one synthetic member."""
    fails = []
    sizes = [len(code_only(js).encode("utf-8")) for js in sources]
    if names and consumes:
        by_name = dict(zip(names, sizes))
        per_member = []
        for m in sorted(consumes):
            want = consumes[m] or list(by_name)
            unknown = [w for w in want if w not in by_name]
            if unknown:
                fails.append(f"{label}: {m} declares consumes {unknown} — not a behaviour of this group")
            per_member.append((m, sum(by_name[w] for w in want if w in by_name), [w for w in want]))
    else:
        per_member = [(label, sum(sizes), list(names or []))]
    worst_m, worst, _ = max(per_member, key=lambda t: t[1])
    if worst > PAGE_BYTES:
        fails.append(f"{label}: worst member page {worst_m} loads {worst} code-only bytes > "
                     f"{PAGE_BYTES} (ADR-0015 page budget — splitting a source does not buy headroom)")
    js = "\n".join(sources)
    r = len(RESIZE_RE.findall(js))
    if r != 1:
        fails.append(f"{label}: {r} window resize listeners across the group — exactly ONE, rAF-debounced (ADR-0015)")
    if r and ("requestAnimationFrame" not in js or "cancelAnimationFrame" not in js):
        fails.append(f"{label}: resize listener is not rAF-debounced (requestAnimationFrame + cancelAnimationFrame expected)")
    return fails, worst, per_member


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
        mem = {m: v for m, v in (g.get("$members") or {}).items() if not m.startswith("$")}
        members = list(mem)
        # ADR-0015 A2: `consumes` ABSENT = every group behaviour (the universal default).
        consumes = {m: list((v or {}).get("consumes") or []) if isinstance(v, dict) else []
                    for m, v in mem.items()}
        srcs, names = [], []
        for bname, beh in behs.items():
            sp = os.path.join(HERE, beh["source"])
            if not os.path.exists(sp):
                fails.append(f"{gname}/{bname}: source knowledge/{beh['source']} missing")
                continue
            js = open(sp).read()
            srcs.append(js)
            names.append(bname)
            f, n, code = check_source(js, f"{gname}/{bname} ({beh['source']})")
            fails += f
            rows.append((f"{gname}/{bname}", beh["source"], n, code, len(members)))
        if srcs:
            f, worst, per_member = check_group(srcs, f"{gname} (page budget)", names,
                                               consumes if members else None)
            fails += f
            totals[gname] = (worst, len(srcs), per_member)
        for m in members:
            mp = os.path.join(HERE, "snippets", m + ".reference.html")
            if os.path.exists(mp):
                fails += check_member(open(mp).read(), f"{gname}: {m}")
    return fails, rows, totals


def write_report(fails, rows, totals):
    L = ["# Behaviour-contract gate (ADR-0015)", "",
         "Per source ≤16KB (legibility) · per member page ≤34KB (page weight) · no polling/network · "
         "ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.",
         "",
         "**Unit: CODE-ONLY bytes** — `//` and `/* */` comments and blank lines are stripped at "
         "measure time (ADR-0015 Amendment 3, Dave #250 2026-09-06, option (e)). Source files are "
         "never modified. The caps did not move. Page figures sum each member's `consumes` "
         "declaration (Amendment 2), so the group's number is the WORST member page.", ""]
    for name, src, n, code, nm in rows:
        L.append(f"- **{name}** — `knowledge/{src}` · **{code} code-only bytes** "
                 f"({code / 1024:.1f} KB of 16 KB) · {n} raw, {n - code} comment/blank · {nm} member(s)")
    L.append("")
    for gname, (worst, k, per_member) in sorted(totals.items()):
        pct = 100 * worst / PAGE_BYTES
        L.append(f"- **{gname} — page budget (worst member):** {worst} code-only bytes "
                 f"({worst / 1024:.1f} KB of 34 KB, {pct:.0f}%) across {k} source(s)")
        for m, tot, want in sorted(per_member, key=lambda t: -t[1]):
            L.append(f"    - `{m}` — {tot} bytes · consumes {', '.join(want) or '(all)'}")
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
    f = check_source(ok_src, "T")[0]
    if f:
        fails.append("clean source failed: %s" % "; ".join(f))
    if not check_source(ok_src + "setInterval(x,50);", "T")[0]:
        fails.append("setInterval not caught")
    if not check_source(ok_src + "fetch('/x');", "T")[0]:
        fails.append("fetch not caught")
    if not check_source(ok_src + "el.style.transform='scale(2)';", "T")[0]:
        fails.append("style.transform not caught")
    # ⚠ Since #250 the unit is CODE-ONLY, so the oversize pad must be REAL CODE. A comment pad
    # here would silently stop biting — the exact rot the A3 unit change makes possible.
    big = ok_src + CODE_PAD(MAX_BYTES + 512)
    if not any("size gate" in x for x in check_source(big, "T")[0]):
        fails.append("oversize source not caught")
    # --- code-only unit bites (#250, ADR-0015 A3) ---
    if code_only("var a=1; // tail\n/* block */\nvar b=2;\n\n") != "var a=1; \nvar b=2;":
        fails.append("code_only did not strip line/block comments and blank lines")
    if code_only('var u="http://x//y";') != 'var u="http://x//y";':
        fails.append("code_only ate a // inside a STRING literal — that is code, not a comment")
    if code_only("var re=/a\\/\\/b/; // gone") != "var re=/a\\/\\/b/; ":
        fails.append("code_only ate a // inside a REGEX literal — that is code, not a comment")
    if code_only("var q=6/2/1; // gone") != "var q=6/2/1; ":
        fails.append("code_only mis-read division as a regex literal")
    if code_only("function f(s){return /x/.test(s);} // gone") \
            != "function f(s){return /x/.test(s);} ":
        fails.append("code_only mis-read a regex after `return` as division")
    _com = ok_src + "\n/*" + "c" * 4000 + "*/"
    if measure(_com)[1] != measure(ok_src)[1]:
        fails.append("4000 bytes of COMMENT changed the code-only figure — comments are not complexity")
    if measure(_com)[0] <= measure(ok_src)[0]:
        fails.append("raw figure did not move when 4000 comment bytes were added — raw is still reported")
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
    # #250: the pads are CODE, not comment — see the oversize bite above for why.
    pad = CODE_PAD(MAX_BYTES - 64)
    if check_source(pad, "T")[0]:
        fails.append("page-budget bite is malformed — each pad must pass the per-source cap")
    if not any("page budget" in x for x in check_group([ok_src, pad, pad, pad], "T")[0]):
        fails.append("page budget not caught — splitting a source must not buy headroom")
    # --- consumes-aware page sum (#250, ADR-0015 A3 + A2) ---
    # Three sources; a narrow member loading only the light one must NOT be charged for the two
    # it declared away — that over-charge is what the registry-sum measured before #250.
    f3, worst3, pm3 = check_group([ok_src, pad, pad, pad], "T", ["a", "b", "c", "d"],
                                  {"wide": ["a", "b", "c", "d"], "narrow": ["a"]})
    if not any("page budget" in x for x in f3):
        fails.append("consumes-aware page budget: the WIDE member's overage was not caught")
    if dict((m, t) for m, t, _ in pm3)["narrow"] != measure(ok_src)[1]:
        fails.append("consumes-aware page budget: a narrow member was charged for sources it "
                     "declared away (ADR-0015 A2 consumes ignored)")
    if check_group([ok_src, pad, pad, pad], "T", ["a", "b", "c", "d"], {"narrow": ["a"]})[0]:
        fails.append("consumes-aware page budget: an all-narrow group wrongly failed — the group "
                     "figure is the WORST MEMBER PAGE, not the registry sum")
    if not any("not a behaviour of this group" in x for x in
               check_group([ok_src], "T", ["a"], {"m": ["nope"]})[0]):
        fails.append("consumes naming an unknown behaviour not caught")
    if not check_member('<script src="https://cdn.example/x.js"></script>', "T"):
        fails.append("external script src not caught")
    if check_member('<script>var a=1;</script>', "T"):
        fails.append("inline script wrongly flagged")
    live, _, _ = run()
    if live:
        fails.append("LIVE registry failing: %s" % "; ".join(live))
    return fails


# --- MUTATION HARNESS (#250) — house style borrowed from _validate_fit_physics.py --mutate -----
# ⛔ These mutate an IN-MEMORY COPY of a live canon source. No file on disk is ever written or
# restored, because none is ever touched. Each mutation declares the verdict it EXPECTS; the run
# exits 0 only when the gate actually returned that verdict (s182-D1: the claim carries its probe).
MUTATIONS = {
    "code-pad": ("+4000 bytes of REAL CODE appended to dv-behaviour.js", "RED"),
    "comment-pad": ("+4000 bytes of COMMENT appended to dv-behaviour.js", "GREEN"),
    "string-slash": ("a // inside a STRING LITERAL, which is code and must be counted", "RED"),
}


def mutate(name):
    reg = json.load(open(REG))
    beh = reg["component-type"]["dataviz"]["$behaviour"]["dv-behaviour"]
    src = os.path.join(HERE, beh["source"])
    base = open(src).read()
    braw, bcode = measure(base)
    if name == "code-pad":
        js = base + "\n" + CODE_PAD(4000)
    elif name == "comment-pad":
        js = base + COMMENT_PAD(4000)
    else:
        # 4000 bytes of code that LOOKS like a comment to a naive stripper: if `//` inside a
        # string were treated as a comment this would measure as ~0 added bytes and stay GREEN.
        js = base + "\n" + "var u=\"" + "//x" * 1333 + "\";"
    f, raw, code = check_source(js, "MUTATION %s (dv-behaviour.js)" % name)
    got = "RED" if any("size gate" in x for x in f) else "GREEN"
    what, want = MUTATIONS[name]
    print("MUTATION %s — %s" % (name, what))
    print("  baseline : raw %d · code-only %d · cap %d" % (braw, bcode, MAX_BYTES))
    print("  mutated  : raw %d (+%d) · code-only %d (+%d)" % (raw, raw - braw, code, code - bcode))
    for x in f:
        print("  X " + x)
    print("  expected %s · got %s — %s" % (want, got, "OK" if got == want else "MUTATION NOT PROVEN"))
    return 0 if got == want else 1


def main():
    if "--mutate" in sys.argv:
        i = sys.argv.index("--mutate")
        name = sys.argv[i + 1] if len(sys.argv) > i + 1 else ""
        if name not in MUTATIONS:
            print("--mutate takes one of: " + " · ".join(sorted(MUTATIONS))); sys.exit(2)
        sys.exit(mutate(name))
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
    for name, src, n, code, nm in rows:
        print(f"  [PASS] {name} — {code} code-only bytes ({code / 1024:.1f} KB of 16) "
              f"· {n} raw, {n - code} comment/blank · {nm} member(s)")
    for gname, (worst, k, per_member) in sorted(totals.items()):
        print(f"  [PASS] {gname} page budget — worst member {worst} code-only bytes "
              f"({worst / 1024:.1f} KB of 34) across {k} source(s)")
        for m, tot, want in sorted(per_member, key=lambda t: -t[1]):
            print(f"         {m:28s} {tot:6d}  consumes {', '.join(want) or '(all)'}")
    print("Behaviour-contract gate OK — see knowledge/_BEHAVIOUR-GATE.md")


if __name__ == "__main__":
    main()
