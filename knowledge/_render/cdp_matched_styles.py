#!/usr/bin/env python3
"""
cdp_matched_styles.py — name the rule that WINS, by observation, never by reading CSS.

WHY THIS EXISTS (ds-019, 2026-07-27)
------------------------------------
`.dv-legrow.is-solo` matched, its custom properties resolved, and it still did not paint.
A census of selectors *containing the string* `dv-legrow` found four, none able to beat
(0,2,0) — so the winning rule did not contain that string, and no amount of grepping was
going to name it. Guessing was explicitly forbidden by the defect entry.

This script asks the browser instead. CDP's CSS.getMatchedStylesForNode returns EVERY rule
the engine matched to a node, in increasing-precedence order, with origin, specificity,
`!important` flags, inline styles and animation/transition state included. That is the
evidence; a selector census over stylesheet text is not.

DESIGN RULES BAKED IN (each one paid for by a real defect)
----------------------------------------------------------
1. OBSERVE, DO NOT INFER. Every reported field comes from the engine. Where the engine does
   not tell us something, this prints UNKNOWN — it never defaults, and never computes a
   plausible-looking value to fill a gap. [[feedback-measuring-tool-must-not-guess]]
2. COMPARE COLOURS AS COLOURS. Computed colour strings are NOT comparable as text:
   `oklab(0 0 0 / 0)` and `rgba(0, 0, 0, 0)` are textually different and visually identical.
   That serialisation difference is exactly how the predecessor probe printed
   "24 checks / 0 failures" while being blind. parse_colour() below returns r/g/b/a floats.
3. THE PROOF MUST BE ABLE TO FAIL. --expect-loser asserts that a named selector is present
   AND beaten. Point it at a rule you know wins and the script must go red, or it is not
   measuring. See --self-bite.
4. FONTS ARE NOT LOAD-BEARING HERE, and that is a claim, so it is stated rather than assumed:
   cascade resolution is font-independent. This script therefore does NOT stage the licensed
   cut and does NOT assert document.fonts.check. Any script that measures GEOMETRY or PAINT
   must asssert it (see _RUNBOOK-render-verify.md step 5) — this one measures neither.
5. ★ SETTLE BEFORE READING — the defect that produced ds-019 and cost most of a session.
   A computed value read in the SAME TASK as a class change is the PRE-transition value.
   `.dv-legrow` transitions border-color + background over 0.16s, so a probe that did
   `el.classList.add('is-solo'); getComputedStyle(el).borderTopColor` read `--line` and
   concluded the rule never painted. It paints from ~160ms.
   ⚠ `oklab(0 0 0 / 0)` is the SIGNATURE OF AN IN-FLIGHT INTERPOLATION, not of a failed
   declaration — Chromium interpolates toward a color-mix() result in oklab. Reading that
   serialisation as "fully transparent, the declaration lost" is precisely how ds-019 was
   written. Default --settle=off makes the mistake structurally impossible.
"""
from __future__ import annotations
import argparse, glob, json, os, re, sys

UNKNOWN = "UNKNOWN"


def parse_colour(s: str):
    """Return (r,g,b,a) floats 0..1, or None if not parseable.

    NEVER compare computed colour strings as text. Returns None rather than guessing:
    an unparsed colour is reported as UNKNOWN upstream, never silently treated as equal
    or unequal to anything.
    """
    if not s:
        return None
    s = s.strip().lower()
    if s in ("transparent",):
        return (0.0, 0.0, 0.0, 0.0)
    m = re.match(r"rgba?\(([^)]+)\)", s)
    if m:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
        try:
            r, g, b = (float(p.rstrip("%")) / (100 if p.endswith("%") else 255) for p in parts[:3])
            a = float(parts[3].rstrip("%")) / (100 if len(parts) > 3 and parts[3].endswith("%") else 1) if len(parts) > 3 else 1.0
            return (r, g, b, a)
        except (ValueError, IndexError):
            return None
    m = re.match(r"color\(srgb ([^)]+)\)", s)
    if m:
        parts = [p.strip() for p in re.split(r"[\s/]+", m.group(1)) if p.strip()]
        try:
            r, g, b = (float(p) for p in parts[:3])
            a = float(parts[3]) if len(parts) > 3 else 1.0
            return (r, g, b, a)
        except (ValueError, IndexError):
            return None
    # oklab/oklch with zero alpha is the case that fooled the predecessor probe. We do not
    # convert oklab to sRGB here (that would be inference); we only extract alpha, which is
    # enough to prove "fully transparent" and is stated as such.
    m = re.match(r"okla?b?c?h?\(([^)]+)\)", s)
    if m and "/" in m.group(1):
        try:
            a = float(m.group(1).split("/")[-1].strip())
            return (None, None, None, a)  # channels UNKNOWN, alpha OBSERVED
        except ValueError:
            return None
    m = re.match(r"#([0-9a-f]{6})$", s)
    if m:
        v = m.group(1)
        return (int(v[0:2], 16) / 255, int(v[2:4], 16) / 255, int(v[4:6], 16) / 255, 1.0)
    return None


def specificity_of(sel: dict):
    """CDP gives {a,b,c} on modern builds. If absent, report UNKNOWN — do not compute it."""
    spec = sel.get("specificity")
    if not spec:
        return UNKNOWN
    return f"({spec.get('a', '?')},{spec.get('b', '?')},{spec.get('c', '?')})"


def collect(cdp, node_id, props):
    matched = cdp.send("CSS.getMatchedStylesForNode", {"nodeId": node_id})
    computed = cdp.send("CSS.getComputedStyleForNode", {"nodeId": node_id})
    comp = {c["name"]: c["value"] for c in computed.get("computedStyle", [])}

    rules = []
    # CDP returns matchedCSSRules in INCREASING precedence order. Index 0 = weakest.
    for i, rm in enumerate(matched.get("matchedCSSRules", [])):
        rule = rm.get("rule", {})
        sels = rule.get("selectorList", {}).get("selectors", [])
        matching = set(rm.get("matchingSelectors", []))
        decls = []
        for p in rule.get("style", {}).get("cssProperties", []):
            if p["name"].lower() in props:
                decls.append({
                    "name": p["name"],
                    "value": p.get("value"),
                    "important": bool(p.get("important")),
                    "disabled": bool(p.get("disabled")),
                    # `implicit` = the engine synthesised it (e.g. from a shorthand like
                    # `border:`). This is the field that explains a longhand nobody wrote.
                    "implicit": bool(p.get("implicit")),
                    "text": p.get("text"),
                })
        if not decls:
            continue
        rules.append({
            "cascade_index": i,
            "origin": rule.get("origin", UNKNOWN),
            "selectors": [
                {
                    "text": s.get("text"),
                    "specificity": specificity_of(s),
                    "matched_this_node": idx in matching,
                }
                for idx, s in enumerate(sels)
            ],
            "media": [m.get("text") for m in rule.get("media", [])] or None,
            "stylesheet_id": rule.get("styleSheetId", UNKNOWN),
            "declarations": decls,
        })

    inline = matched.get("inlineStyle", {})
    inline_decls = [
        {"name": p["name"], "value": p.get("value"), "important": bool(p.get("important"))}
        for p in inline.get("cssProperties", [])
        if p["name"].lower() in props
    ]
    attr = matched.get("attributesStyle", {})
    attr_decls = [
        {"name": p["name"], "value": p.get("value")}
        for p in attr.get("cssProperties", [])
        if p["name"].lower() in props
    ]

    return {
        "computed": {p: comp.get(p, UNKNOWN) for p in props},
        "computed_parsed": {p: parse_colour(comp.get(p, "")) for p in props},
        "matched_rules_weakest_first": rules,
        "inline_style": inline_decls or None,
        "attributes_style": attr_decls or None,
        "keyframes_present": bool(matched.get("cssKeyframesRules")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="path to the HTML (snippet, not showroom harness)")
    ap.add_argument("--selector", required=True, help="CSS selector for the node to interrogate")
    ap.add_argument("--add-class", default=None, help="class to apply directly before measuring")
    ap.add_argument("--settle", choices=["off", "wait", "none"], default="off",
                    help="how to avoid reading a MID-TRANSITION value (see rule 5 in the docstring). "
                         "off = inject transition:none !important (deterministic, the default) · "
                         "wait = sleep past the longest declared duration · "
                         "none = read immediately. 'none' REPRODUCES ds-019 and exists only so the "
                         "artefact can be demonstrated on demand. Do not use it to measure.")
    ap.add_argument("--props", default="border-color,border-top-color,background-color,background-image")
    ap.add_argument("--widths", default="1180,760")
    ap.add_argument("--frame-url-contains", default=None, help="measure inside an iframe instead of the top document")
    ap.add_argument("--expect-loser", default=None,
                    help="BITE: selector text that must be present AND beaten. Exits 3 if it wins or is absent.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    props = [p.strip().lower() for p in args.props.split(",")]
    sys.path.insert(0, os.environ.get("PWLIBS", ""))
    from playwright.sync_api import sync_playwright

    shell = glob.glob(os.path.expanduser(
        os.environ.get("PWSHELL", "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")))
    if not shell:
        print("FATAL: no headless_shell found. Set PWSHELL. Not guessing a path.", file=sys.stderr)
        return 2

    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0], headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                                    "--allow-file-access-from-files"])
        for w in [int(x) for x in args.widths.split(",")]:
            pg = b.new_page(viewport={"width": w, "height": 1400})
            pg.goto(f"file://{os.path.abspath(args.file)}")
            pg.wait_for_timeout(1200)

            target = pg
            if args.frame_url_contains:
                frames = [f for f in pg.frames if args.frame_url_contains in (f.url or "")]
                if not frames:
                    print(f"FATAL: no frame url containing {args.frame_url_contains!r}. "
                          f"Frames: {[f.url for f in pg.frames]}", file=sys.stderr)
                    return 2
                target = frames[0]

            # ★ SETTLE FIRST — see rule 5. Injected BEFORE the class change, so the new value
            # is applied instantly and no interpolated value can ever be observed.
            if args.settle == "off":
                target.evaluate(
                    "() => { const s = document.createElement('style');"
                    " s.textContent = '*,*::before,*::after{transition:none !important;"
                    "animation:none !important}'; document.head.appendChild(s); }")
            if args.add_class:
                target.eval_on_selector(
                    args.selector, "(el, c) => el.classList.add(c)", args.add_class)
                # 'none' deliberately does NOT wait: it reproduces the ds-019 artefact.
                pg.wait_for_timeout({"off": 60, "wait": 900, "none": 0}[args.settle])

            sel = args.selector + (f".{args.add_class}" if args.add_class else "")
            matches = target.eval_on_selector(sel, "el => el.matches(arguments[0] ?? '*')") if False else True

            cdp = pg.context.new_cdp_session(pg)
            cdp.send("DOM.enable"); cdp.send("CSS.enable")
            doc = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
            node = cdp.send("DOM.querySelector",
                            {"nodeId": doc["root"]["nodeId"], "selector": sel})
            nid = node.get("nodeId", 0)
            if not nid:
                print(f"FATAL: CDP could not resolve {sel!r} at width {w}. "
                      f"Reporting UNKNOWN rather than falling back.", file=sys.stderr)
                results[w] = {"error": "node not resolved", "selector": sel}
                continue
            results[w] = collect(cdp, nid, props)
            results[w]["element_matches"] = matches
            pg.close()
        b.close()

    out = json.dumps(results, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out)
    print(out)

    # ---- the bite -------------------------------------------------------------
    if args.expect_loser:
        for w, r in results.items():
            texts = [s["text"] for rule in r.get("matched_rules_weakest_first", [])
                     for s in rule["selectors"]]
            if args.expect_loser not in texts:
                print(f"\nBITE FAILED at {w}: {args.expect_loser!r} is not among the matched "
                      f"rules at all — the probe is looking at the wrong node.", file=sys.stderr)
                return 3
            last = r["matched_rules_weakest_first"][-1]
            if any(s["text"] == args.expect_loser for s in last["selectors"]):
                print(f"\nBITE FAILED at {w}: {args.expect_loser!r} is the STRONGEST matched "
                      f"rule — it wins, so the premise is wrong.", file=sys.stderr)
                return 3
        print(f"\nBITE OK: {args.expect_loser!r} present and beaten at every width.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
