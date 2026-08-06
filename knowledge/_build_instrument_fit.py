#!/usr/bin/env python3
"""Build _INSTRUMENT-FIT.md — can each rule's gate OBSERVE the property the rule names?

WHY THIS EXISTS (ds-015, 2026-07-27; Dave: "maybe we are checking the wrong thing").
ADR-0016's register asks *is there a check, and can it fail?* (PROVEN/CLAIMED/UNPROVEN).
This asks the question that sits ON TOP of that one:

    a check can be PROVEN and still measure a PROXY that does not track its rule.

The founding case is `aid-009`: the rule names "a minimum 44x44px target area"; the gate
calls its check "target size" — THE VOCABULARY MATCHES. The narrowing is in the INSTRUMENT.
A static regex observes a *declared box*; the rule is about a *target*. The two decouple
the instant the property is carried by a mechanism (::before expander, token, transform),
and at that point the gate goes QUIET, not RED. 7 of 67 snippets are actually measured
and the gate reports "0 failures".

THE LADDER — what an instrument can observe, in ascending power:
  I0 STATIC   text/regex/AST over source bytes. Sees what is WRITTEN.
  I1 DOM      a parsed tree. Sees structure + relationships. NOT the cascade.
  I2 RENDER   computed styles, geometry, composited colour. Needs a browser.
  I3 EYE      human judgment. Not mechanisable in principle. Never a defect.

A gate is UNDER-INSTRUMENTED when its rule's property needs a rung ABOVE the gate's own.
That gate can pass forever without ever observing the thing it is named for.

=============================== ANTI-FALSE-FIX ===============================
1. DO NOT read "UNDER-INSTRUMENTED" as "the components fail". It means UNMEASURED.
   ds-015's diamond is the case in point: the check is blind; that is not evidence
   the corpus is non-compliant, and a static parse cannot tell the difference.
2. DO NOT "fix" a gap by widening the pattern table until the row goes green.
   The rule side is tagged from the rule's own TEXT. If a tag is wrong, the fix is
   to correct the tag WITH ITS EVIDENCE STRING, not to retune until the report is quiet.
3. DO NOT let UNKNOWN default into I0. An unclassified rule silently filed as
   "static is adequate" is precisely the lie this tool exists to expose. UNKNOWN is
   a first-class, reported bucket. Its count is a finding about the pattern table.
4. THE GATE SIDE IS OBSERVED, NEVER GUESSED. It keys on imports and API calls.
   A bare-word detector reports `_validate_proforma.py` as RENDER because the file
   says "monochrome" and "demo-chrome" (MEASURED, 2026-07-27) — overstating gate
   strength, which is the WRONG DIRECTION for a fitness audit. Bite 2 pins this.
5. INSTRUMENT FIT IS NOT ENACTMENT. A matched instrument says the gate CAN see the
   property, not that it does, nor that the ruling is live. That is ADR-0016's job.
   Both registers are needed; neither substitutes for the other.
==============================================================================

Usage:  python3 knowledge/_build_instrument_fit.py [--check] [--selftest]
        --check     exit 1 if the report on disk is stale (build-step mode, ADVISORY)
        --selftest  run the bites (they must be able to FAIL, or this tool is CLAIMED)
"""
import os, re, sys, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "_INSTRUMENT-FIT.md")
RULES_INDEX = os.path.join(HERE, "guidelines", "_rules-index.json")

LADDER = ["I0-STATIC", "I1-DOM", "I2-RENDER", "I3-EYE"]
RANK = {name: i for i, name in enumerate(LADDER)}


def rung(name):
    """Fail loud on any instrument code outside the ladder (bite 6)."""
    if name not in RANK:
        raise ValueError("unknown instrument code %r — the ladder is %s" % (name, LADDER))
    return RANK[name]


# ---------------------------------------------------------------- rule side
# Published pattern table. Every tag carries the phrase that produced it, so a
# reader can overrule any row without reverse-engineering this file. STRONG
# patterns are domain terms that mean one thing; WEAK ones can appear casually
# and only earn LOW confidence on their own.
PATTERNS = [
    # (tier, strong?, regex, label)
    ("I3-EYE", True, r"\b(tone of voice|plain english|jargon|reassur\w*|friendly|"
                     r"natural[- ]sounding|reads? well|makes sense|feels?\b)", "judgment of language"),
    ("I3-EYE", True, r"\b(appropriate\w*|sparingly|tastef\w*|harmoni\w*|composition|"
                     r"crop\w*|aesthetic|pleasing|balance[ds]?\b)", "aesthetic judgment"),
    ("I3-EYE", False, r"\b(consider|where possible|judg\w*|sense[- ]check)", "discretionary"),

    ("I2-RENDER", True, r"(contrast|\b\d(?:\.\d+)?:1\b|luminance|\bAA\b|\bAAA\b)", "contrast ratio"),
    ("I2-RENDER", True, r"\b(target (area|size)|hit[- ]area|touch target|\d{2}\s*[x×]\s*\d{2}\s*px)",
     "post-layout target geometry"),
    ("I2-RENDER", True, r"\b(overlap\w*|obscur\w*|clip\w*|truncat\w*|overflow|reflow|"
                        r"wraps?\b|z-index|stacking)", "layout outcome"),
    ("I2-RENDER", True, r"\b(computed|rendered|resolves? to|cascade|inherit\w*|"
                        r"visible focus|focus indicator)", "resolved value"),
    ("I2-RENDER", True, r"\b(animation|motion|transition|duration|parallax|auto[- ]?play|"
                        r"reduced motion)", "motion"),
    ("I2-RENDER", True, r"\b(responsive|breakpoint|viewport|zoom|200%|reflow)", "viewport-dependent"),
    ("I2-RENDER", False, r"\b(separation|spacing between|aligned?\b|alignment|centred|centered)",
     "measured spatial relation"),

    ("I1-DOM", True, r"\b(programmatically determinable|heading (order|level|structure)|"
                     r"landmark|aria-|role=|name, role, value|tab order|focus order|"
                     r"reading order)", "structural relationship"),
    ("I1-DOM", False, r"\b(label(l|)ed by|associated with|nested|parent|sibling|"
                      r"semantic\w*|markup|attribute)", "markup relationship"),

    ("I0-STATIC", True, r"\b(sentence case|title case|uppercase|lower ?case|exact string|"
                        r"spelling|naming convention|file ?name|prefix\w*)", "literal text form"),
    ("I0-STATIC", True, r"(#[0-9A-Fa-f]{6}\b|\btoken\w*\b|font-(family|size|weight)|"
                        r"\bnever (use|write)\b|\bmust be\b)", "literal declared value"),
]


def tag_rule(text):
    """-> (instrument, confidence, evidence[]). Max rung wins: a rule needing BOTH a
    literal check and a rendered one needs the rendered one. Over-demanding produces
    noise a reader can dismiss; under-demanding produces silence, which is the failure
    mode this tool exists to catch."""
    hits = []
    for tier, strong, rx, label in PATTERNS:
        m = re.search(rx, text, re.I)
        if m:
            hits.append((tier, strong, label, m.group(0)[:40]))
    if not hits:
        return "UNKNOWN", "none", []
    top = max(hits, key=lambda h: rung(h[0]))[0]
    at_top = [h for h in hits if h[0] == top]
    conf = "high" if any(h[1] for h in at_top) else "low"
    ev = ["%s (%s: '%s')" % (h[2], h[0], h[3]) for h in at_top]
    return top, conf, ev


# ---------------------------------------------------------------- gate side
# OBSERVED capability. Keys on imports and API calls only — see ANTI-FALSE-FIX 4.
RENDER_SIG = re.compile(
    r"(from\s+playwright|import\s+playwright|sync_playwright|async_playwright|"
    r"\.chromium\.launch|\.firefox\.launch|\.webkit\.launch|page\.evaluate|"
    r"puppeteer|browser\.newPage)")
DOM_SIG = re.compile(
    r"(BeautifulSoup|from\s+bs4|html\.parser|HTMLParser|import\s+lxml|from\s+lxml|"
    r"require\(['\"]jsdom|import\s+.*jsdom|parse5|cheerio|xml\.etree)")


def gate_instrument(src):
    if RENDER_SIG.search(src):
        return "I2-RENDER"
    if DOM_SIG.search(src):
        return "I1-DOM"
    return "I0-STATIC"


# Registers and report builders NAME rules in order to talk about them. Counting them as
# gates makes a rule look checked because something DISCUSSED it. OBSERVED 2026-07-27:
# this file's own bite comment cited `icon-005`, and the rule came out FIT with this
# script as its evidence — a self-reference reading as green. Bite 8 pins it.
SELF = os.path.basename(__file__)
NOT_A_GATE = {SELF, "_build_enactment_register.py"}


def check_files():
    out = []
    for d in (HERE, os.path.join(HERE, "compliance")):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f in NOT_A_GATE:
                continue
            if re.match(r"(_validate_|_check_|_sweep_|_verify_|_build_|gen_).*\.(py|js)$", f):
                out.append(os.path.join(d, f))
    return out


def rule_aliases(rid):
    """Gates write `dv-004` in full but abbreviate compound ids: `dv-bar-009` appears as
    `bar-009`. Both forms are recorded so a match is always auditable."""
    forms = [rid]
    parts = rid.split("-")
    if len(parts) == 3:
        forms.append("-".join(parts[1:]))
    return forms


def dangling_citations(rules):
    """Rule IDs a gate CITES AS ITS AUTHORITY that the rules index does not contain.

    OBSERVED 2026-07-27, found by bite 1 on its first run. `guidelines/*.md` declares 698
    rule anchors; `_rules-index.json` holds the 465 that carry an enforcement-destiny tag.
    The other 265 are invisible to the index, to `_consult.py`, and to this tool — and
    SEVEN of them are cited by a live gate. `aid-009` (the founding case of ds-015, ruled
    by Dave 2026-07-03) is one: its anchor line carries no destiny tag, so the rule the
    a11y gate enforces cannot be looked up by any tool that reads the index.

    This is the ds-015 shape inverted: there the gate could not see the component; here
    the INDEX cannot see the rule. Same signature — correct markup, failed lookup, silence.
    """
    idx = {r["id"] for r in rules}
    declared = set()
    for f in sorted(glob.glob(os.path.join(HERE, "guidelines", "*.md"))):
        declared |= set(re.findall(r"\{#([a-z0-9]+-\d{3})\}",
                                   open(f, encoding="utf-8").read()))
    untagged = declared - idx
    out = {}
    # DETERMINISM (M3, 2026-07-27): `untagged` is a SET — iterating it seeds `out`'s key
    # order from hash randomisation, so a clean rebuild churned `_instrument-fit.json`
    # (5 ins / 5 del, ZERO content: aid-009/aca-004/avd-006 swapping places). This is the
    # V2-P2 class (7 `sorted()` sites fixed 2026-07-26); this dict escaped that sweep.
    # Sort BOTH the iteration and the emitted keys — do not "simplify" either away.
    for path in check_files():                       # already sorted (see check_files)
        src = open(path, encoding="utf-8", errors="replace").read()
        for rid in sorted(untagged):
            if re.search(r"(?<![\w-])" + re.escape(rid) + r"(?![\w-])", src):
                out.setdefault(rid, []).append(os.path.relpath(path, REPO))
    return {k: out[k] for k in sorted(out)}, len(declared), len(untagged)


def harvest_gates(rules):
    """rule id -> [(gate relpath, instrument, matched form)]. Evidence-based: the gate
    must NAME the rule. No keyword-overlap inference — that is the consult's defect."""
    gates = {}
    for path in check_files():
        src = open(path, encoding="utf-8", errors="replace").read()
        gates[os.path.relpath(path, REPO)] = (src, gate_instrument(src))
    idx = collections.defaultdict(list)
    for r in rules:
        for name, (src, inst) in gates.items():
            for form in rule_aliases(r["id"]):
                if re.search(r"(?<![\w-])" + re.escape(form) + r"(?![\w-])", src):
                    idx[r["id"]].append((name, inst, form))
                    break
    return idx, {k: v[1] for k, v in gates.items()}


# ---------------------------------------------------------------- assemble
def analyse():
    rules = json.load(open(RULES_INDEX, encoding="utf-8"))["rules"]
    idx, gate_inst = harvest_gates(rules)
    rows = []
    for r in rules:
        need, conf, ev = tag_rule(r["rule"])
        gs = idx.get(r["id"], [])
        best = max((g[1] for g in gs), key=rung, default=None)
        if need == "UNKNOWN":
            verdict = "UNTAGGED"
        elif not gs:
            verdict = "UNGATED"
        elif need == "I3-EYE":
            verdict = "EYE-ONLY"
        elif rung(need) > rung(best):
            verdict = "UNDER-INSTRUMENTED"
        else:
            verdict = "FIT"
        rows.append({"id": r["id"], "file": r["file"], "destiny": r["destiny"],
                     "rule": r["rule"], "needs": need, "confidence": conf,
                     "evidence": ev, "gates": [g[0] for g in gs],
                     "gate_instrument": best, "verdict": verdict})
    dangling, declared_n, untagged_n = dangling_citations(rules)
    return rows, gate_inst, dangling, declared_n, untagged_n


ORDER = ["UNDER-INSTRUMENTED", "UNGATED", "UNTAGGED", "EYE-ONLY", "FIT"]


def render(rows, gate_inst, dangling, declared_n, untagged_n):
    tally = collections.Counter(r["verdict"] for r in rows)
    blocking_under = [r for r in rows
                      if r["verdict"] == "UNDER-INSTRUMENTED" and r["destiny"] == "BLOCKING"]
    L, A = [], None
    A = L.append
    A("# Instrument fit — can the gate OBSERVE the property its rule names?\n")
    A("> GENERATED by `knowledge/_build_instrument_fit.py`. Do not hand-edit.\n>")
    A("> Sits **on top of** ADR-0016. The register asks *is there a check and can it fail?*;")
    A("> this asks *is it looking at the right thing?* **A check can be PROVEN and still")
    A("> measure a proxy that does not track its rule** (`aid-009`, ds-015).\n")
    A("| rung | instrument | sees |")
    A("|---|---|---|")
    A("| I0 | STATIC | source bytes — what is WRITTEN |")
    A("| I1 | DOM | parsed tree — structure and relationships, not the cascade |")
    A("| I2 | RENDER | computed styles, geometry, composited colour — needs a browser |")
    A("| I3 | EYE | human judgment — not mechanisable, never a defect |\n")
    A("| verdict | count | meaning |")
    A("|---|---:|---|")
    A("| **UNDER-INSTRUMENTED** | %d | a gate names it but sits BELOW the rung its property "
      "needs — passes without observing |" % tally["UNDER-INSTRUMENTED"])
    A("| **UNGATED** | %d | no gate names it; the rung shown is the COST of gating it |"
      % tally["UNGATED"])
    A("| **UNTAGGED** | %d | the pattern table could not classify the rule — a finding about "
      "THIS TOOL, never filed as I0 |" % tally["UNTAGGED"])
    A("| **EYE-ONLY** | %d | needs judgment; correctly ungateable |" % tally["EYE-ONLY"])
    A("| **FIT** | %d | the gate's instrument reaches the property |" % tally["FIT"])
    A("| **TOTAL** | %d | |\n" % len(rows))
    A("**%d rules carry a gate that cannot observe them; %d of those are BLOCKING.** "
      "A BLOCKING rule with an under-powered gate is the `aid-009` shape: green, and blind.\n"
      % (tally["UNDER-INSTRUMENTED"], len(blocking_under)))
    A("⚠ **UNDER-INSTRUMENTED means UNMEASURED, not non-compliant.** The components may be "
      "perfectly correct; a static parse cannot tell you either way. Do not 'fix' these by "
      "failing them.\n")

    A("## ⚠ Dangling citations — gates enforcing rules the INDEX cannot see\n")
    A("*`guidelines/*.md` declares **%d** rule anchors. `_rules-index.json` holds the **%d** "
      "that carry an enforcement-destiny tag. The other **%d** are invisible to the index, to "
      "`_consult.py`, and to this register — and the following are cited by a LIVE GATE as its "
      "authority.*\n" % (declared_n, len(rows), untagged_n))
    if dangling:
        A("| cited rule | not in index | cited by |")
        A("|---|---|---|")
        for rid in sorted(dangling):
            A("| `%s` | ✗ | %s |" % (rid, ", ".join("`%s`" % g for g in sorted(set(dangling[rid])))))
        A("")
        A("⚠ **This is ds-015 inverted.** There, the gate could not see the component; here the "
          "INDEX cannot see the rule. Same signature: the markup is correct, the lookup fails, "
          "and nothing reports it. `aid-009` — Dave's 2026-07-03 hit-area ruling and the founding "
          "case of ds-015 — is on this list: its anchor line carries no destiny tag, so the rule "
          "the a11y gate enforces cannot be retrieved by any tool that reads the index.\n")
    else:
        A("*No dangling citations detected.*\n")

    A("## Ranked — under-instrumented, BLOCKING first\n")
    A("| rule | destiny | needs | gate has | gate | property |")
    A("|---|---|---|---|---|---|")
    rank = sorted(blocking_under + [r for r in rows if r["verdict"] == "UNDER-INSTRUMENTED"
                                    and r["destiny"] != "BLOCKING"],
                  key=lambda r: (r["destiny"] != "BLOCKING", -rung(r["needs"]), r["id"]))
    for r in rank:
        A("| `%s` | %s | **%s** | %s | %s | %s |"
          % (r["id"], r["destiny"], r["needs"], r["gate_instrument"],
             ", ".join("`%s`" % g for g in r["gates"]),
             "; ".join(r["evidence"]).replace("|", "\\|")))
    if not rank:
        A("| — | | | | | *none detected* |")
    A("")

    A("## Gate instruments — OBSERVED from imports and API calls\n")
    A("| gate | instrument |")
    A("|---|---|")
    for name in sorted(gate_inst):
        if os.path.basename(name).startswith("_validate_"):
            A("| `%s` | %s |" % (name, gate_inst[name]))
    A("")
    A("*Detected from `sync_playwright` / `.chromium.launch` / `page.evaluate` and DOM-parser "
      "imports — **never from bare words**. A word-based detector reads `_validate_proforma.py` "
      "as RENDER because the file says *monochrome* and *demo-chrome*, overstating gate strength "
      "(MEASURED 2026-07-27; bite 2 pins it).*\n")

    A("## Ungated rules, ranked by the cost of gating them\n")
    ung = collections.Counter(r["needs"] for r in rows if r["verdict"] == "UNGATED")
    A("| rung needed | rules | note |")
    A("|---|---:|---|")
    A("| I0-STATIC | %d | cheapest wins — a regex reaches these |" % ung["I0-STATIC"])
    A("| I1-DOM | %d | needs a parsed tree |" % ung["I1-DOM"])
    A("| I2-RENDER | %d | needs the render harness (`_RUNBOOK-render-verify.md`) |"
      % ung["I2-RENDER"])
    A("")
    A("## Untagged — what the pattern table cannot classify\n")
    unt = [r for r in rows if r["verdict"] == "UNTAGGED"]
    A("*%d rules. This count is a finding about the tool, not the corpus. They are NOT "
      "filed as I0: an unclassified rule recorded as 'static is adequate' is the exact lie "
      "this register exists to expose.*\n" % len(unt))
    for r in unt[:25]:
        A("- `%s` (%s) — %s" % (r["id"], r["destiny"], r["rule"][:110]))
    if len(unt) > 25:
        A("- *… %d more in `_instrument-fit.json`*" % (len(unt) - 25))
    A("")
    return "\n".join(L), tally


# ---------------------------------------------------------------- bites
def selftest():
    """Every proof ships with a bite proving the proof can FAIL. Non-negotiable."""
    fails = []

    def ok(cond, name, detail=""):
        print(("  ✓ " if cond else "  ✗ ") + name + ("" if cond else "  -- " + detail))
        if not cond:
            fails.append(name)

    rows, gate_inst, dangling, declared_n, untagged_n = analyse()
    by = {r["id"]: r for r in rows}

    # BITE 1 — the target-size property, ds-015's subject. icon-005 is the BLOCKING 44x44
    # rule that IS in the index. Its honest verdict is UNGATED: no check names it.
    r = by.get("icon-005")
    ok(r is not None and r["needs"] == "I2-RENDER",
       "bite1a: icon-005 (44x44 target) requires RENDER", "got %s" % (r and r["needs"]))
    ok(r is not None and r["verdict"] == "UNGATED",
       "bite1b: icon-005 is UNGATED — no check names it", "got %s" % (r and r["verdict"]))

    # BITE 1c — the original finding, now CLOSED and INVERTED (#114). It used to assert
    # aid-009 was dangling: cited by a gate, absent from the index. Its own comment said
    # "if this bite ever goes quiet, either the tag was added (good — confirm) or the
    # detector broke (bad)". Confirmed: the ID-26 anchor was re-filed to a [BLOCKING …]
    # destiny tag and the index regenerated, so the citation now RESOLVES. The bite is
    # inverted rather than deleted, so it still reds — if the tag is removed or downgraded
    # out of the indexed destinies, if the index regen is skipped, or if the citation
    # resolver breaks.
    ok("aid-009" in by and "aid-009" not in dangling,
       "bite1c: aid-009 is cited by a gate AND present in the rules index (not dangling)",
       "in-index=%s dangling set = %s" % ("aid-009" in by, sorted(dangling)))
    ok(len(dangling) >= 1 and untagged_n > 0,
       "bite1d: the untagged-anchor population is reported, not silently zero",
       "untagged=%d dangling=%d" % (untagged_n, len(dangling)))

    # BITE 2 — today's observed false positive. 'monochrome'/'demo-chrome' are not a browser.
    ok(gate_inst.get("knowledge/_validate_proforma.py") == "I0-STATIC",
       "bite2: 'chrome' as a WORD does not promote a gate to RENDER",
       "got %s" % gate_inst.get("knowledge/_validate_proforma.py"))

    # BITE 3 — positive control: the detector is not simply always saying STATIC.
    ok(gate_inst.get("knowledge/_validate_state_contrast.py") == "I2-RENDER",
       "bite3: a real Playwright gate IS detected as RENDER",
       "got %s" % gate_inst.get("knowledge/_validate_state_contrast.py"))

    # BITE 4 — UNKNOWN must never default into I0.
    need, conf, _ = tag_rule("Frobnicate the wibble per the quux schedule.")
    ok(need == "UNKNOWN", "bite4: unclassifiable rule -> UNKNOWN, not I0", "got %s" % need)

    # BITE 5 — a matched pair must NOT be flagged (no false alarms).
    need, _, _ = tag_rule("Headings use sentence case; never write uppercase.")
    ok(need == "I0-STATIC" and rung(need) <= rung("I0-STATIC"),
       "bite5: a literal-text rule + a static gate is FIT, not flagged", "got %s" % need)

    # BITE 6 — the ladder fails loud on an unknown code.
    try:
        rung("I9-TELEPATHY")
        ok(False, "bite6: unknown instrument code raises", "it did not raise")
    except ValueError:
        ok(True, "bite6: unknown instrument code raises")

    # BITE 7 — max-rung wins when a rule names both a literal and a rendered property.
    need, _, _ = tag_rule("Token must be #B92F1E and meet a 4.5:1 contrast ratio.")
    ok(need == "I2-RENDER", "bite7: mixed rule takes the HIGHER rung", "got %s" % need)

    # BITE 8 — a register that NAMES a rule is not a gate that CHECKS it. This file cites
    # icon-005 and aid-009 in its own bites; neither may count as evidence of enforcement.
    ok(all(SELF not in g for r in rows for g in r["gates"]),
       "bite8: this script never counts itself as a gate",
       "self-citation leaked into the evidence column")

    print("\nselftest: %d bites, %d failed" % (11, len(fails)))
    return 1 if fails else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    rows, gate_inst, dangling, declared_n, untagged_n = analyse()
    text, tally = render(rows, gate_inst, dangling, declared_n, untagged_n)

    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur.strip() != text.strip():
            print("instrument fit: STALE — re-run knowledge/_build_instrument_fit.py")
            return 1
        print("instrument fit: up to date (%d rules)" % len(rows))
        return 0

    # anti-blind-check: never report a cheerful empty register
    if not rows:
        print("instrument fit: harvested ZERO rules — refusing to write. Check RULES_INDEX.")
        return 2
    open(OUT, "w", encoding="utf-8").write(text + "\n")
    json.dump({"total": len(rows), "tally": dict(tally), "rows": rows,
               "gate_instruments": gate_inst, "dangling_citations": dangling,
               "declared_anchors": declared_n, "untagged_anchors": untagged_n},
              open(os.path.join(HERE, "_instrument-fit.json"), "w"), indent=1)
    print("instrument fit: %d rules -> UNDER-INSTRUMENTED %d · UNGATED %d · UNTAGGED %d · "
          "EYE-ONLY %d · FIT %d  (%s)"
          % (len(rows), tally["UNDER-INSTRUMENTED"], tally["UNGATED"], tally["UNTAGGED"],
             tally["EYE-ONLY"], tally["FIT"], os.path.relpath(OUT, REPO)))
    if dangling:
        print("  ⚠ %d rule IDs cited by gates are ABSENT from the index (%d untagged anchors "
              "of %d declared): %s"
              % (len(dangling), untagged_n, declared_n, ", ".join(sorted(dangling))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
